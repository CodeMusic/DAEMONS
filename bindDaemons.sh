#!/usr/bin/env bash
# Build an edition if needed, then run it.
#
#   ./bindDaemons.sh                      CONTENT edition, GBA
#   ./bindDaemons.sh context              CONTEXT edition, GBA
#   ./bindDaemons.sh --classic            CONTENT edition, Game Boy
#   ./bindDaemons.sh context --classic    CONTEXT edition, Game Boy
#   ./bindDaemons.sh --debug              GBA testing build
#   ./bindDaemons.sh --classic --debug    Game Boy testing build
#   ./bindDaemons.sh --ai                 CONTENT edition, GBA, played by a model
#   ./bindDaemons.sh --clean
#
# TWO ENGINES, ON PURPOSE.
#
# The Game Boy build (pokered) is where the vertical slice actually is. The
# GBA build (pokefirered) is a spike: it is being evaluated for whether
# abilities, item descriptions and a real scripting language are worth
# rebuilding 334 files for. Neither is the loser yet, so neither is deleted,
# and --classic is how you reach the one that currently has a game in it.
#
#   engine/     -> ../pokered-daemons       CONTENT = _RED,     CONTEXT = _BLUE
#   engineGba/  -> ../pokefirered-daemons   CONTENT = firered,  CONTEXT = leafgreen
#
# The edition split survives the port unchanged, which is the first good sign:
# both disassemblies ship the same game twice and differ by a build flag.
#
# --debug builds a separate ROM with its own save, so a debug run never touches
# a real playthrough. Both engines have one, but they are not the same thing:
#
#   --classic --debug   upstream's own debug mode.
#                       SELECT on the title screen opens the menu -- start with
#                       a party, fly anywhere, the usual hooks.
#                       hold B skips trainer battles and some NPC scripts.
#
#   --debug             ours. pokefirered ships no debug build at all, so this
#                       is one we added: a new game starts with six daemons
#                       picked for their ABILITIES, one of each KIND of item so
#                       the description window can be read, all eight badges and
#                       999999.
#                       hold B walks through grass unmolested.
#
# The GBA one is scaffolding for the 9.3 spike rather than a general debug menu:
# it exists to put abilities and item descriptions in front of you quickly,
# because those are the two things being evaluated. With DAEMONS_DEBUG=0 the
# retail builds still match their .sha1 byte for byte.
#
# Saves live beside the ROM and survive rebuilds, so a playthrough is not lost
# when you change a line.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

EDITION=content
CLEAN=0
DEBUG=0
CLASSIC=0
AI=0
for arg in "$@"; do
  case "$arg" in
    content|context) EDITION="$arg" ;;
    --classic)       CLASSIC=1 ;;
    --clean)         CLEAN=1 ;;
    --debug)         DEBUG=1 ;;
    --ai)            AI=1 ;;
    *) echo "usage: ./bindDaemons.sh [content|context] [--classic] [--clean] [--debug] [--ai]" >&2; exit 1 ;;
  esac
done

if [[ $AI -eq 1 && $CLASSIC -eq 1 ]]; then
  echo "--ai is GBA only: the harness reads pokefirered's RAM by symbol name." >&2
  exit 1
fi

if [[ $CLASSIC -eq 1 ]]; then
  DIR=engine
  EMU=SameBoy
  EMU_HINT="brew install --cask sameboy"
  if [[ $DEBUG -eq 1 ]]; then
    TARGET="${EDITION}-debug"
    case "$EDITION" in
      content) ROM=daemonsContentDebug.gbc ;;
      context) ROM=daemonsContextDebug.gbc ;;
    esac
  else
    TARGET="$EDITION"
    case "$EDITION" in
      content) ROM=daemonsContent.gbc ;;
      context) ROM=daemonsContext.gbc ;;
    esac
  fi
  command -v rgbasm >/dev/null || { echo "rgbds missing — run: brew install rgbds" >&2; exit 1; }
else
  DIR=engineGba
  EMU=mGBA
  EMU_HINT="brew install --cask mgba"
  case "$EDITION" in
    content) TARGET=firered ;;
    context) TARGET=leafgreen ;;
  esac
  [[ $DEBUG -eq 1 ]] && TARGET="${TARGET}_debug"
  # pokefirered names the ROM after the build, so the debug build gets its own
  # file and therefore its own .sav.
  ROM="poke${TARGET}.gba"
  # agbcc lives inside the engine checkout; the ARM binutils it calls do not.
  export PATH="/opt/homebrew/bin:$PATH"
  command -v arm-none-eabi-as >/dev/null || {
    echo "ARM toolchain missing — run: brew install arm-none-eabi-gcc" >&2; exit 1; }
  [[ -x "$DIR/tools/agbcc/bin/agbcc" ]] || {
    echo "agbcc not installed into $DIR/tools/agbcc." >&2
    echo "  git clone https://github.com/pret/agbcc /tmp/agbcc" >&2
    echo "  cd /tmp/agbcc && ./build.sh && ./install.sh $PWD/$DIR" >&2; exit 1; }
fi

[[ -d "$DIR" ]] || { echo "$DIR is missing — run ./setup.sh" >&2; exit 1; }
[[ $CLEAN -eq 1 ]] && make -C "$DIR" clean >/dev/null

echo "building ${TARGET} (${DIR})…"
make -C "$DIR" "$TARGET" -j8 >/dev/null

if [[ $DEBUG -eq 1 ]]; then
  if [[ $CLASSIC -eq 1 ]]; then
    echo "  debug build: SELECT on the title screen opens the menu; hold B to skip battles."
  else
    echo "  debug build: a new game starts with a party, a bag, all badges and 999999; hold B to avoid grass."
  fi
fi

if [[ ! -d "/Applications/$EMU.app" ]]; then
  echo "No $EMU found. Try: $EMU_HINT" >&2
  echo "ROM is at: $PWD/$DIR/$ROM" >&2
  exit 1
fi

# macOS `open` against an already-running emulator holding this exact path
# just focuses the window -- it does not reload the file. So a rebuilt ROM
# silently does nothing and you sit there listening to the old one, which is
# exactly what happened with Route 1. Quit it first; both emulators flush
# their save on a graceful quit, so nothing is lost.
if pgrep -x "$EMU" >/dev/null 2>&1; then
  echo "  ${EMU} is already running -- quitting it so the new ROM actually loads"
  osascript -e "quit app \"$EMU\"" >/dev/null 2>&1 || true
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    pgrep -x "$EMU" >/dev/null 2>&1 || break
    /bin/sleep 0.3
  done
fi

echo "binding ${TARGET} → ${EMU}"
open -a "$EMU" "$DIR/$ROM"

# ---------------------------------------------------------------- --ai -----
#
# WHAT THIS MODE IS. Clad3815/gpt-play-pokemon-firered drives mGBA over a Lua
# socket and reads the game out of RAM -- no screenshots anywhere, which is the
# fact that makes a small local model viable at all. It resolves game state by
# SYMBOL NAME out of a pokefirered.sym, and its loader honours FIRERED_SYM_PATH.
#
# WHY THE SYMBOLS ARE REGENERATED EVERY RUN, AND WHY IT MATTERS MORE THAN IT
# LOOKS. Their .sym describes retail FireRed. Measured against ours:
#
#     EWRAM + IWRAM (live state)     892 symbols,  99.3% agree
#     ROM           (static data)  48804 symbols,   3.8% agree
#
# So their file against our ROM reads party, position and battle state
# CORRECTLY, and move names, item names and THE TYPE CHART as garbage. That is
# the worst failure available -- it looks like it is working. tools/gbasym.py
# emits ours from the ELF, so it cannot drift.
if [[ $AI -eq 1 ]]; then
  HARNESS="../gpt-play-pokemon-firered"
  [[ -d "$HARNESS" ]] || {
    echo "AI harness missing at $HARNESS -- run ./setup.sh" >&2; exit 1; }

  echo
  echo "generating symbols from this build…"
  python3 tools/gbasym.py --write

  # LiteLLM, not the model server directly: the harness calls /v1/responses and
  # local servers only speak /v1/chat/completions. See ai/litellm/README.md --
  # and note the bridge is opt-in per model, so a config without
  # use_chat_completions_api 404s on the first call and looks like a network
  # fault rather than a setting.
  #
  # FIND THE PROXY. The tailnet name first, because it is the one that works
  # from anywhere; the .local name second for a LAN with no tailnet; the IP
  # last. Whichever answers /health/liveliness wins.
  LLM_HOST="${DAEMONS_LLM_HOST:-}"
  if [[ -z "$LLM_HOST" ]]; then
    for h in roverbyteseer roverbyteseer.local 10.0.0.136; do
      if curl -fsS --max-time 3 "http://$h:4000/health/liveliness" >/dev/null 2>&1; then
        LLM_HOST="$h"; break
      fi
    done
  fi
  [[ -n "$LLM_HOST" ]] || {
    echo "no LiteLLM proxy on roverbyteseer / .local / 10.0.0.136:4000" >&2
    echo "  is it running?  ssh roverbyte@10.0.0.136 'launchctl list | grep litellm'" >&2
    exit 1; }
  : "${OPENAI_BASE_URL:=http://$LLM_HOST:4000/v1}"

  # THE KEY IS FETCHED, NEVER STORED HERE. It lives in ~/.litellm.env on the
  # proxy host at mode 0600. Copying it into this repo, a dotfile or a shell
  # history is how it ends up somewhere it should not be -- and it already
  # reached a chat log once and had to be rotated.
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    OPENAI_API_KEY="$(ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=6 \
      "roverbyte@$LLM_HOST" 'sed -n "s/^LITELLM_MASTER_KEY=//p" ~/.litellm.env' 2>/dev/null || true)"
  fi
  [[ -n "$OPENAI_API_KEY" ]] || {
    echo "could not read the LiteLLM key from roverbyte@$LLM_HOST" >&2
    echo "  set up the key once:  ssh-copy-id roverbyte@$LLM_HOST" >&2
    exit 1; }
  : "${OPENAI_MODEL:=daemons}"
  : "${OPENAI_MODEL_PATHFINDING:=daemons-pathfinding}"
  export OPENAI_MODEL_PATHFINDING
  export OPENAI_BASE_URL OPENAI_API_KEY OPENAI_MODEL
  export FIRERED_SYM_PATH="$PWD/ai/pokefirered.sym"
  export FIRERED_BRIDGE_STRICT_SYMBOLS=1   # fail loudly, never read zeroes

  mkdir -p ai/logs
  echo "starting bridge and agent…"
  ( cd "$HARNESS" && python3 firered_mgba_bridge.py ) >ai/logs/bridge.log 2>&1 &
  echo "  bridge  pid $!  -> ai/logs/bridge.log"
  ( cd "$HARNESS/server" && npm start ) >ai/logs/agent.log 2>&1 &
  echo "  agent   pid $!  -> ai/logs/agent.log"

  cat <<AIEOF

  model     $OPENAI_MODEL via $OPENAI_BASE_URL
  key       read from roverbyte@$LLM_HOST:~/.litellm.env
  symbols   ai/pokefirered.sym (this build)

  ONE STEP IS STILL YOURS. mGBA 0.10.5 has no --script; that landed in 0.11.
  In mGBA: Tools -> Scripting -> File -> Load script, and choose

      $PWD/$HARNESS/mgba/scripts/FireRedBridgeSocketServer.lua

  Then the dashboard:  cd $HARNESS/frontend && python3 -m http.server 5173
  Stop everything:     kill %1 %2
AIEOF
fi

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

# --help before anything else, so it works with no engines checked out and no
# toolchain installed -- which is exactly when someone needs to read it.
usage() {
  cat <<'USAGE'
bindDaemons.sh — build an edition of CONTEXT / CONTENT and run it.

  ./bindDaemons.sh                     CONTENT, GBA        -> mGBA
  ./bindDaemons.sh context             CONTEXT, GBA
  ./bindDaemons.sh --classic           CONTENT, Game Boy   -> SameBoy
  ./bindDaemons.sh context --classic   CONTEXT, Game Boy

EDITIONS
  content        the default. firered on GBA, _RED on the Game Boy
  context        leafgreen on GBA, _BLUE on the Game Boy
                 The two differ by a build flag and share a byte-identical
                 type chart -- an argument that changed by cartridge would
                 not be one.

FLAGS
  --classic      the Game Boy build (pokered). The GBA build is the one being
                 worked on; --classic is how you reach the older one.
  --debug        a separate ROM with its own save, so a debug run never
                 touches a playthrough.
                   GBA      a party picked for their ABILITIES, one of each
                            KIND of item, all eight MARKS, 999999.
                            Hold B to walk through grass.
                   --classic  upstream's own debug menu on SELECT.
                            Hold B to skip battles.
  --ai           GBA only. A model plays it, through engineAi and a LiteLLM
                 proxy on the tailnet. See ai/README.md
  --fresh        start with an empty history. The agent PERSISTS its history
                 to engineAi/server/gpt_data/history.json and reloads it on
                 every start, so a restart is a resume, not a new run -- one
                 file reached 1.08 MB and 93 items, and both models kept
                 replaying a sentence from hours earlier because it was still
                 in there. The old files are moved aside, never deleted.
  --model NAME   use a specific model instead of the "daemons" group. Names
                 come from tools/ai_models.py, which reads them out of LM
                 Studio -- e.g. qwen3-vl-8b, minicpm-v-4-6.
  --full-schema  give the agent all eight action variants. Default is lean:
                 the three that only annotate (add_marker, delete_marker,
                 restart_console) are dropped. Measured warm, lean and full are
                 the same speed -- 3.7s against 3.8s -- so this is about giving
                 a small model three fewer branches to confuse, not latency.
  --stop         stop a running --ai: bridge, agent, dashboard and mGBA.
                 Ctrl+C only stops the foreground, so this is the one that
                 actually ends a run. --ai calls it for you if a previous run
                 is still up.
  --clean        make clean first
  --help         this

WHEN IT BREAKS
  make vanilla-check     builds pristine upstream in a throwaway worktree and
                         checks the hashes. If vanilla matches, the toolchain
                         is fine and the break is ours.
  ./setup.sh             re-clones the three engines, fixes their branches, and
                         reports what is missing.
USAGE
  # Last, because it is the one thing that has to be typed by hand -- and
  # printed with the path THIS machine has, resolved through the symlink:
  # Lua does not expand ~, and mGBA's scripting box is a REPL, not a picker.
  local lua=""
  [[ -d engineAi/mgba/scripts ]] &&
    lua="$(cd engineAi/mgba/scripts && pwd -P)/FireRedBridgeSocketServer.lua"
  cat <<USAGE

THE --ai MANUAL STEP
  mGBA 0.10.5 has no --script (that landed in 0.11), so once per emulator
  launch: Tools -> Scripting, paste this in, press Run. Then close the window
  -- the script lives as long as the EMULATOR, not the window.

      dofile("${lua:-<run ./setup.sh first>}")
USAGE
}
for arg in "$@"; do
  case "$arg" in -h|--help|help) usage; exit 0 ;; esac
done

# The processes --ai starts. One list, used to stop a previous run before
# starting and by --stop, so the two can never disagree about what to kill.
DASH_PORT="${DAEMONS_DASH_PORT:-5173}"
AI_PIDFILE="ai/logs/run.pids"

# PIDS, NOT PATTERNS. "gpt-play-pokemon-firered-daemons/server" matched nothing:
# pkill -f matches the COMMAND LINE, and the agent's is `npm start` and
# `node index.js` -- neither contains a directory. So the agent survived every
# --stop and every --ai, and an instance from before the repo was renamed went
# on running with a stale __dirname, reading prompts from a path that no longer
# existed. Recording the pids we actually start is exact, and cannot hit an
# unrelated node.
AI_PROCS=("firered_mgba_bridge.py" "http.server $DASH_PORT")
# ai_stop [keep-emulator]
#
# THE EMULATOR IS THE ODD ONE OUT. --stop should take mGBA down; the cleanup at
# the start of a run must NOT, because by then this script has already
# relaunched it -- quitting it there would kill the emulator the run is about
# to use, and the symptom would be an agent that never connects to a socket
# nobody is holding.
ai_stop() {
  local found=0 pat n keep="${1:-}" pid
  # the pids this script recorded, plus their children -- npm start forks node,
  # and killing only npm leaves the agent orphaned and still running
  if [[ -f "$AI_PIDFILE" ]]; then
    while read -r pid; do
      [[ -n "$pid" ]] || continue
      kill -0 "$pid" 2>/dev/null || continue
      found=1
      pkill -P "$pid" 2>/dev/null || true
      kill "$pid" 2>/dev/null || true
    done < "$AI_PIDFILE"
  fi
  for pat in "${AI_PROCS[@]}"; do
    pgrep -f "$pat" >/dev/null 2>&1 || continue
    found=1
    pkill -f "$pat" 2>/dev/null || true
  done
  if [[ "$keep" != "keep-emulator" ]] && pgrep -x mGBA >/dev/null 2>&1; then
    osascript -e 'quit app "mGBA"' >/dev/null 2>&1; found=1
  fi
  [[ $found -eq 1 ]] || { echo "nothing was running"; return 0; }

  # WAIT, THEN SAY. SIGTERM is asynchronous: checking straight after pkill sees
  # a process mid-shutdown and reports a failure that is not one -- or, worse,
  # reports success while something is still holding :8000 and the next --ai
  # dies on bind. So this waits for them to actually go, and escalates only
  # what refuses.
  for n in 1 2 3 4 5 6 7 8 9 10; do
    still_running() {
      for pat in "${AI_PROCS[@]}"; do pgrep -f "$pat" >/dev/null 2>&1 && return 0; done
      [[ -f "$AI_PIDFILE" ]] && while read -r pid; do
        [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null && return 0
      done < "$AI_PIDFILE"
      return 1
    }
    still_running || break
    sleep 1
  done
  for pat in "${AI_PROCS[@]}"; do
    pgrep -f "$pat" >/dev/null 2>&1 && { echo "  $pat ignored SIGTERM — sending SIGKILL"; pkill -9 -f "$pat" 2>/dev/null || true; }
  done
  sleep 1
  local left=0
  for pat in "${AI_PROCS[@]}"; do pgrep -f "$pat" >/dev/null 2>&1 && left=1; done
  for pid in $(cat "$AI_PIDFILE" 2>/dev/null); do kill -0 "$pid" 2>/dev/null && left=1; done
  rm -f "$AI_PIDFILE"
  [[ $left -eq 0 ]] && echo "stopped the AI run" || echo "some processes are still alive — check: pgrep -fl 'node index.js'"
}
for arg in "$@"; do
  case "$arg" in --stop|--ai-stop) ai_stop; exit 0 ;; esac
done

EDITION=content
CLEAN=0
DEBUG=0
CLASSIC=0
AI=0
FULL_SCHEMA=0
FRESH=0
WANT_MODEL=""
for arg in "$@"; do
  if [[ "$WANT_MODEL" == "__next__" ]]; then WANT_MODEL="$arg"; continue; fi
  case "$arg" in
    content|context) EDITION="$arg" ;;
    --classic)       CLASSIC=1 ;;
    --clean)         CLEAN=1 ;;
    --debug)         DEBUG=1 ;;
    --ai)            AI=1 ;;
    --full-schema)   FULL_SCHEMA=1 ;;
    --fresh)         FRESH=1 ;;
    --model)         WANT_MODEL="__next__" ;;
    *) echo "unknown argument: $arg" >&2; usage >&2; exit 1 ;;
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
# WHAT THIS MODE IS. engineAi -- our fork of Clad3815/gpt-play-pokemon-firered
# -- drives mGBA over a Lua
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
  HARNESS="engineAi"
  [[ -d "$HARNESS" ]] || {
    echo "AI harness missing at ./$HARNESS -- run ./setup.sh" >&2; exit 1; }

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
  # history is how it ends up somewhere it should not be.
  #
  # AND IT OVERRIDES ANY OPENAI_API_KEY ALREADY IN THE ENVIRONMENT. Respecting
  # a pre-set value is the usual courtesy and exactly wrong here: a real
  # `sk-proj-...` exported from ~/.zshrc was sent to LiteLLM, which answered
  # `400 No connected db.` -- its way of saying "unknown bearer", since it
  # treats anything that is not the master key as a virtual key needing a
  # database. An hour reads like a proxy fault when it is the wrong key.
  #
  # Worse than confusing: it points a real OpenAI credential at a local proxy
  # that never needed one. When OPENAI_BASE_URL is ours, the key must be ours.
  if [[ -n "${OPENAI_API_KEY:-}" && "${OPENAI_API_KEY}" != sk-daemons-* ]]; then
    echo "  note      ignoring the OPENAI_API_KEY in your environment;"
    echo "            --ai talks to LiteLLM, which wants its own key"
  fi
  OPENAI_API_KEY="$(ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=6 \
    "roverbyte@$LLM_HOST" 'sed -n "s/^LITELLM_MASTER_KEY=//p" ~/.litellm.env' 2>/dev/null || true)"
  [[ -n "$OPENAI_API_KEY" ]] || {
    echo "could not read the LiteLLM key from roverbyte@$LLM_HOST" >&2
    echo "  set up the key once:  ssh-copy-id roverbyte@$LLM_HOST" >&2
    exit 1; }
  : "${OPENAI_MODEL:=${WANT_MODEL:-daemons}}"
  : "${OPENAI_MODEL_PATHFINDING:=daemons-pathfinding}"
  export OPENAI_MODEL_PATHFINDING

  # CONTEXT GROWS UNTIL THE HARNESS FOLDS IT. It summarises when the running
  # total passes OPENAI_TOKEN_LIMIT, so cost per step climbs to that ceiling,
  # drops, and climbs again -- one run was already at 114,627 tokens after a
  # handful of steps, 95,075 of them cached.
  #
  # The harness defaults to 250,000, which is a hair under qwen3-vl-8b's
  # 262,144 and leaves no room for the summary call itself. And it is DOUBLE
  # what gemma-3-4b can hold (131,072), so that model would overflow and fail
  # before ever reaching the summariser -- the crash would look like the model
  # breaking rather than the limit being wrong for it.
  : "${OPENAI_TOKEN_LIMIT:=200000}"
  export OPENAI_TOKEN_LIMIT
  DAEMONS_SCHEMA=$([[ $FULL_SCHEMA -eq 1 ]] && echo full || echo lean)
  export DAEMONS_SCHEMA
  # LiteLLM's /responses bridge rejects a function_call_output whose `output`
  # is an array -- the harness's way of attaching a screenshot to a tool
  # result. Verified against the proxy: string passes, list is a flat 400
  # "Invalid type for 'input'". Left off; the images go in a user message
  # instead, which is the same content.
  : "${DAEMONS_EXTEND_TOOL_OUTPUT:=0}"
  export DAEMONS_EXTEND_TOOL_OUTPUT
  : "${DAEMONS_DUMP_INPUT:=$PWD/ai/logs/last-input.json}"
  export DAEMONS_DUMP_INPUT
  export OPENAI_BASE_URL OPENAI_API_KEY OPENAI_MODEL
  export FIRERED_SYM_PATH="$PWD/ai/pokefirered.sym"
  export FIRERED_BRIDGE_STRICT_SYMBOLS=1   # fail loudly, never read zeroes

  # Resolved through the symlink and made absolute, because Lua does not
  # expand ~ and the REPL is where this path actually gets pasted.
  LUA_PATH="$(cd "$HARNESS/mgba/scripts" && pwd -P)/FireRedBridgeSocketServer.lua"
  # DEPENDENCIES, CHECKED RATHER THAN ASSUMED. The bridge died on import with
  # ModuleNotFoundError: requests, and the only visible symptom was the agent
  # logging ECONNREFUSED against :8000 forever -- which reads as "the bridge is
  # not up yet" rather than "the bridge crashed on line 11".
  # A VENV, BECAUSE PATH IS NOT A DEPENDENCY MANAGER. This machine has four
  # python3s, and THIS SCRIPT chooses one of them: the GBA branch above puts
  # /opt/homebrew/bin first so agbcc can find the ARM binutils, which also puts
  # Homebrew's python3 ahead of conda's. So the interpreter the bridge runs on
  # is a side effect of the toolchain fix, and "pip install" typed in any shell
  # aims somewhere else. Two rounds of installing into the wrong Python.
  #
  # bpvenv already set the precedent for exactly this problem. Same answer.
  BRIDGE_VENV="ai/bridgevenv"
  if [[ ! -x "$BRIDGE_VENV/bin/python" ]]; then
    echo "creating the bridge venv (once)…"
    # Homebrew's 3.13 is externally managed, so it can build a venv but cannot
    # be pip-installed into directly. The venv sidesteps that too.
    python3 -m venv "$BRIDGE_VENV" || {
      echo "could not create $BRIDGE_VENV with $(command -v python3)" >&2; exit 1; }
  fi
  PYBIN="$PWD/$BRIDGE_VENV/bin/python"
  "$PYBIN" -c 'import importlib.util as u,sys
sys.exit(0 if all(u.find_spec(m) for m in ("fastapi","uvicorn","pydantic","dotenv","requests")) else 1)' 2>/dev/null || {
    echo "installing bridge dependencies into $BRIDGE_VENV…"
    "$PYBIN" -m pip install -q --upgrade pip >/dev/null 2>&1
    "$PYBIN" -m pip install -q -r "$HARNESS/requirements.txt" || {
      echo "pip install failed — see above" >&2; exit 1; }
  }
  [[ -d "$HARNESS/server/node_modules" ]] || {
    echo "agent dependencies missing — run:" >&2
    echo "    (cd $HARNESS/server && npm ci)" >&2; exit 1; }

  # STOP THE PREVIOUS RUN FIRST, AND WAIT FOR IT. Ctrl+C only stops whatever is
  # in the foreground, so a previous run's bridge is usually still holding
  # :8000 -- and a bare pkill here would move on before it let go, so the new
  # bridge would die on bind and the agent would talk to nothing. ai_stop is
  # the same function --stop uses: it waits, escalates, and verifies.
  if pgrep -f "firered_mgba_bridge.py" >/dev/null 2>&1 ||
     pgrep -f "gpt-play-pokemon-firered-daemons/server" >/dev/null 2>&1 ||
     pgrep -f "http.server $DASH_PORT" >/dev/null 2>&1; then
    echo "a previous --ai is still running; stopping it first…"
    ai_stop keep-emulator
  fi

  # THE HARNESS RESUMES BY DEFAULT, AND THAT IS INVISIBLE. Say how much history
  # is being loaded, because a 1 MB history.json is the difference between an
  # agent thinking and an agent replaying a transcript of its worst turns.
  GPT_DATA="$HARNESS/server/gpt_data"
  if [[ $FRESH -eq 1 && -d "$GPT_DATA" ]]; then
    ARCHIVE="$GPT_DATA/../gpt_data_$(date +%Y%m%d-%H%M%S)"
    mv "$GPT_DATA" "$ARCHIVE"
    echo "  history   cleared (previous run archived to $(basename "$ARCHIVE"))"
  elif [[ -f "$GPT_DATA/history.json" ]]; then
    H=$(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))))" "$GPT_DATA/history.json" 2>/dev/null || echo "?")
    K=$(( $(wc -c < "$GPT_DATA/history.json") / 1024 ))
    echo "  history   RESUMING ${H} items, ${K} KB — pass --fresh to start clean"
  fi

  mkdir -p ai/logs
  : > "$AI_PIDFILE"
  echo "starting bridge and agent…"
  echo "  python    $PYBIN"
  ( cd "$HARNESS" && "$PYBIN" firered_mgba_bridge.py ) >ai/logs/bridge.log 2>&1 &
  echo $! >> "$AI_PIDFILE"; echo "  bridge  pid $!  -> ai/logs/bridge.log"
  ( cd "$HARNESS/server" && npm start ) >ai/logs/agent.log 2>&1 &
  echo $! >> "$AI_PIDFILE"; echo "  agent   pid $!  -> ai/logs/agent.log"
  # The dashboard is part of the run rather than a line to copy afterwards --
  # and being in AI_PROCS means --stop takes it down with everything else.
  if lsof -nP -iTCP:"$DASH_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "  dash    :$DASH_PORT already in use — left alone"
  else
    ( cd "$HARNESS/frontend" && python3 -m http.server "$DASH_PORT" ) \
      >ai/logs/dashboard.log 2>&1 &
    echo $! >> "$AI_PIDFILE"; echo "  dash    pid $!  -> http://localhost:$DASH_PORT"
  fi

  cat <<AIEOF

  model     $OPENAI_MODEL via $OPENAI_BASE_URL
  key       read from roverbyte@$LLM_HOST:~/.litellm.env
  symbols   ai/pokefirered.sym (this build)

  ONE STEP IS STILL YOURS. mGBA 0.10.5 has no --script; that landed in 0.11.
  Tools -> Scripting opens a box with a Run button -- that box is a Lua REPL,
  not a file picker, and a bare path fails with "unexpected symbol near '~'".
  Paste this and press Run:

      dofile("$LUA_PATH")

  Dashboard:            http://localhost:$DASH_PORT  (already started)

  STOP EVERYTHING:      ./bindDaemons.sh --stop

  Ctrl+C only stops whatever is in the foreground -- the bridge and the agent
  are started by this script and outlive it, so they need the line above.
AIEOF
fi

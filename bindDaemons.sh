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
# The GBA build (pokefirered) is where the game is. It was opened as a spike --
# were abilities, item descriptions and a real scripting language worth
# rebuilding 334 files for? -- and vision.md 9.3 records that it answered in a
# day and the project moved. The Game Boy build (pokered) is kept as the
# reference the port tools read from: it still builds and runs its slice, and
# --classic reaches it. It is not updated further.
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
  --nested-tools upstream's single execute_action wrapping a union of actions.
                 Default is flat, one tool per action, because qwen emits 27
                 duplicate calls through the union and exactly one when the
                 actions are separate tools. Note minicpm cannot tool-call
                 through LM Studio at all -- its XML dialect needs SGLang or
                 vLLM's parser -- so this flag is for another serving layer.
  --fresh        start with an empty history. The agent PERSISTS its history
                 to engineAi/server/gpt_data/history.json and reloads it on
                 every start, so a restart is a resume, not a new run -- one
                 file reached 1.08 MB and 93 items, and both models kept
                 replaying a sentence from hours earlier because it was still
                 in there. The old files are moved aside, never deleted --
                 and the archive is swept to the most recent 5 runs, since
                 --fresh is what creates them. DAEMONS_KEEP_RUNS changes the
                 number; 0 keeps everything.
  --mind NAME    which mind plays (engineAi T-555; ai/README.md): mind, the
                 default -- ask the companion's hub which mind it is using
                 (today the Tiiny) and play on it; tiiny, the Tiiny directly;
                 seer, LiteLLM on roverbyteseer:4000; openrouter, hosted and
                 PAID, never chosen for you. DAEMONS_TIINY_MODEL=35b|9b picks
                 the model on the Tiiny (35b is the measured choice).
  --model NAME   a specific model name on that mind instead of its default.
                 Alone, it means seer (or openrouter for an or- name, which is
                 PAID). Names come from ai/litellm/config.yaml and from
                 tools/ai_models.py, which reads them out of LM Studio.
  --simple-schema  drop the three action variants that only annotate
                 (add_marker, delete_marker, restart_console), leaving five.
                 Full is now the default: markers are what draw doors and
                 stairs onto the dashboard map, and a run without them is
                 harder for a watching human to follow than it is for the
                 agent to produce. Measured warm, the two are the same speed
                 -- 3.7s against 3.8s -- so this only ever bought a small
                 model three fewer branches to confuse, never latency.
                 --full-schema is still accepted and is now a no-op.
  --stop         stop a running --ai: bridge, agent, dashboard and mGBA.

Each line of inner voice is clickable in the dashboard and speaks in the INDEX
voice. It goes to the internal n8n by default; set DAEMONS_VOICE_URL to the
public relay to reach it from away, or to "" to turn it off.
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
  # Found by GLOB rather than typed. The script was renamed once and this line
  # went on printing the old path, which is worse than printing nothing: what
  # it prints is pasted straight into an emulator by hand.
  local lua=""
  if [[ -d engineAi/mgba/scripts ]]; then
    local dir; dir="$(cd engineAi/mgba/scripts && pwd -P)"
    for f in "$dir"/*BridgeSocketServer.lua; do [[ -f $f ]] && lua="$f"; done
  fi
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
FULL_SCHEMA=1   # full is the default now; --simple-schema opts out
FRESH=0
NESTED_TOOLS=0
WANT_MODEL=""
WANT_MIND=""
for arg in "$@"; do
  if [[ "$WANT_MODEL" == "__next__" ]]; then WANT_MODEL="$arg"; continue; fi
  if [[ "$WANT_MIND" == "__next__" ]]; then WANT_MIND="$arg"; continue; fi
  case "$arg" in
    content|context) EDITION="$arg" ;;
    --classic)       CLASSIC=1 ;;
    --clean)         CLEAN=1 ;;
    --debug)         DEBUG=1 ;;
    --ai)            AI=1 ;;
    --full-schema)   FULL_SCHEMA=1 ;;   # kept: it is in shell history
    --simple-schema) FULL_SCHEMA=0 ;;
    --lean-schema)   FULL_SCHEMA=0 ;;
    --fresh)         FRESH=1 ;;
    --nested-tools)  NESTED_TOOLS=1 ;;
    --model)         WANT_MODEL="__next__" ;;
    --mind)          WANT_MIND="__next__" ;;
    *) echo "unknown argument: $arg" >&2; usage >&2; exit 1 ;;
  esac
done

# THE DEFAULT IS A MIND, NOT A MODEL (engineAi T-555, 2026-11-14). It used to be or-muse-glimmer -- OpenRouter, paid
# -- and is now `mind`: the harness asks the companion's hub which mind it is using and plays on it. The resolution
# (hub, Tiiny, seer, keys, the store rule for OpenRouter) lives in engineAi's server/src/ai/mind.js, so it is the same
# whether this script or anything else starts the agent. --model alone keeps its old meaning: a LiteLLM name.
if [[ -n "$WANT_MODEL" && -z "$WANT_MIND" ]]; then
  case "$WANT_MODEL" in or-*) WANT_MIND=openrouter ;; *) WANT_MIND=seer ;; esac
fi

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
  # The ROM carries our edition's name -- engineGba's Makefile renames it from
  # retail's pokefirered.gba. The debug build still gets its own file, and
  # therefore its own .sav.
  case "$EDITION" in
    content) ROM=daemonsContent ;;
    context) ROM=daemonsContext ;;
  esac
  [[ $DEBUG -eq 1 ]] && ROM="${ROM}_debug"
  ROM="${ROM}.gba"
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

  # WHICH MIND PLAYS: engineAi's server/src/ai/mind.js resolves DAEMONS_MIND into an endpoint, a model and a key
  # (fetched over ssh, never stored here) when the agent starts. Local minds are spoken to in chat completions through
  # its src/ai/chatBridge.js; OpenRouter keeps the Responses API through LiteLLM, with store off.
  # Exported only when --mind (or --model) asks: otherwise the dashboard's Mind card, kept in engineAi's
  # server/mind.local.json, decides -- and with nothing chosen there either, it is `mind`, local, never paid.
  [[ -n "$WANT_MIND" ]] && DAEMONS_MIND="$WANT_MIND"
  case "${DAEMONS_MIND:-}" in
    ""|mind|tiiny|seer) ;;
    openrouter) echo "  note      DAEMONS_MIND=openrouter is PAID: every turn is billed" ;;
    *) echo "--mind $DAEMONS_MIND: choose mind, tiiny, seer or openrouter" >&2; exit 1 ;;
  esac
  [[ -n "${DAEMONS_MIND:-}" ]] && export DAEMONS_MIND
  [[ -n "$WANT_MODEL" ]] && export DAEMONS_MODEL="$WANT_MODEL"
  unset OPENAI_BASE_URL
  # The proxy host still matters for the voice button below (n8n lives beside it) and is handed to mind.js for seer:
  # the tailnet name first, then the LAN name, then the IP. Not fatal: mind and tiiny do not need it.
  LLM_HOST="${DAEMONS_LLM_HOST:-}"
  if [[ -z "$LLM_HOST" ]]; then
    for h in roverbyteseer roverbyteseer.local 10.0.0.136; do
      if curl -fsS --max-time 3 "http://$h:4000/health/liveliness" >/dev/null 2>&1; then
        LLM_HOST="$h"; break
      fi
    done
  fi
  : "${LLM_HOST:=roverbyteseer}"
  export DAEMONS_SEER_HOST="$LLM_HOST"
  : "${DAEMONS_PATHFINDER:=local}"
  export DAEMONS_PATHFINDER
  : "${DAEMONS_DUMP_INPUT:=$PWD/ai/logs/last-input.json}"
  export DAEMONS_DUMP_INPUT
  export FIRERED_SYM_PATH="$PWD/ai/pokefirered.sym"
  export FIRERED_BRIDGE_STRICT_SYMBOLS=1   # fail loudly, never read zeroes

  # Resolved through the symlink, made absolute, and found by GLOB -- because
  # Lua does not expand ~, the REPL is where this path actually gets pasted,
  # and the script has been renamed once already. The usage block does the
  # same; a name typed in two places is a name that goes stale in one.
  LUA_PATH=""
  for f in "$(cd "$HARNESS/mgba/scripts" && pwd -P)"/*BridgeSocketServer.lua; do
    [[ -f $f ]] && LUA_PATH="$f"
  done
  [[ -n $LUA_PATH ]] ||
    { echo "no *BridgeSocketServer.lua in $HARNESS/mgba/scripts" >&2; exit 1; }
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
  # Resolved BEFORE the mv below, because after it $GPT_DATA does not exist and
  # `cd "$GPT_DATA/.."` fails -- which is exactly how the first version of the
  # sweep aborted the whole launch under `set -e`. I tested the pruning block
  # in isolation and never once ran it after the move it depends on.
  RUN_ROOT="$(cd "$HARNESS/server" && pwd)"
  if [[ $FRESH -eq 1 && -d "$GPT_DATA" ]]; then
    ARCHIVE="$RUN_ROOT/gpt_data_$(date +%Y%m%d-%H%M%S)"
    mv "$GPT_DATA" "$ARCHIVE"
    echo "  history   cleared (previous run archived to $(basename "$ARCHIVE"))"
    # --fresh clears the AGENT, not the SAVE. Worth saying out loud: the two
    # come apart, and an agent with no notes standing in the middle of a run
    # will happily set "leave the first town" as its objective.
    echo "  note      the game SAVE is untouched -- if the ROM is mid-run, the"
    echo "            agent wakes there with no notes. It is told so."

    # --fresh ARCHIVES, so --fresh is what accumulates: 33 directories and
    # 55 MB had built up without anyone deciding to keep them, the largest a
    # single 17 MB history. Sweeping here rather than on every launch means
    # the tidy-up happens at the moment you already said "start clean", and
    # never deletes anything while a run might still want it.
    #
    # KEEP the most recent few. A run you want to look at is a run from
    # today; beyond that they are just the shape of a history that was
    # already replaced. DAEMONS_KEEP_RUNS=0 disables the sweep entirely.
    #
    # NO mapfile HERE. This script's shebang is `env bash`, and /bin/bash on
    # macOS is still 3.2, which has no mapfile -- it would fail, the `|| true`
    # would swallow it, and the sweep would silently prune nothing while
    # printing nothing. That is the exact "looks like it worked" failure this
    # project keeps getting bitten by. `ls -dt | tail -n +N` into a plain
    # while-read is portable to 3.2 and does the same job.
    KEEP_RUNS="${DAEMONS_KEEP_RUNS:-5}"
    if [[ "$KEEP_RUNS" -gt 0 ]]; then
      PRUNED=0
      FREED=$( cd "$RUN_ROOT" && du -ck $(ls -dt gpt_data_* 2>/dev/null | tail -n +$((KEEP_RUNS + 1))) 2>/dev/null | tail -1 | cut -f1 )
      # ls -dt is newest-first, so tail -n +N is everything past the Nth.
      while IFS= read -r OLD; do
        [[ -n "$OLD" ]] || continue
        rm -rf "$RUN_ROOT/$OLD"
        PRUNED=$((PRUNED + 1))
      done < <( cd "$RUN_ROOT" && ls -dt gpt_data_* 2>/dev/null | tail -n +$((KEEP_RUNS + 1)) )
      if [[ $PRUNED -gt 0 ]]; then
        echo "  archives  pruned $PRUNED old run(s), $(( ${FREED:-0} / 1024 )) MB freed (keeping $KEEP_RUNS)"
      fi
      # The mechanical history fold writes multi-MB backups every time the
      # summariser fails, which is the one that grows fastest when something
      # is wrong -- exactly when you are least likely to be watching disk.
      BK="$HARNESS/server/backup"
      if [[ -d "$BK" ]]; then
        PRUNED_BK=0
        while IFS= read -r OLD; do
          [[ -n "$OLD" ]] || continue
          rm -f "$BK/$OLD"
          PRUNED_BK=$((PRUNED_BK + 1))
        done < <( ls -t "$BK" 2>/dev/null | tail -n +$((KEEP_RUNS + 1)) )
        [[ $PRUNED_BK -gt 0 ]] && echo "  backups   pruned $PRUNED_BK old history backup(s)"
      fi
    fi
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

  mind      ${DAEMONS_MIND:-the dashboard's Mind card, or mind}${DAEMONS_MODEL:+ ($DAEMONS_MODEL)} -- the agent's log names what it chose, '[mind] ...'
  keys      fetched over ssh when the agent starts, never stored
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

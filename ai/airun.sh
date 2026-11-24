#!/usr/bin/env bash
# C-496 (the user, 2026-11-23, by multiple choice): AN AI RUN-THROUGH, started and ended from THE ENGINE ROOM's IN PLAY
# (THE HANDS run this on the computer: companion server/src/jobs.ts, ai-start and ai-stop). It is `bindDaemons.sh --ai`
# made safe to start from anywhere:
#
#   - ITS OWN SAVE. The run plays a copy of the newest CONTENT build, daemonsAI.gba, in ~/.local/share/daemons-ai/, and
#     mGBA keeps daemonsAI.sav beside it -- the AI's own playthrough, carried on at every START, with its own notes
#     (gpt_data/) beside it. The player's own daemonsContent.sav is never opened.
#   - NO MANUAL STEP. mGBA 0.11 (~/Applications/mGBA-0.11.app, beside 0.10.5) loads the bridge's script with --script.
#   - NOTHING OF YOURS CLOSED. A new mGBA instance of its own (open -n); an mGBA already open is left as it is.
#   - NO BUILD. It plays what was last built (engineGba/daemonsContent.gba and its .elf, for the symbols), so a START
#     never races another build.
#   - A LOCAL MIND ONLY. DAEMONS_MIND is mind (the hub's -- the Tiiny), tiiny or seer; openrouter, which is paid, is
#     refused (CLAUDE.md: the paid playtester is never run).
#   - REPORTED. ai/inplay_beat.py tells the hub it is in play -- its save, its screen -- and ends the run when IN PLAY's
#     END is pressed.
#
#   ai/airun.sh start | stop | status
#
# On this Mac for now; C-497 tries it on roverbyteseer and asks the user whether to move it there.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"
AI_DIR="${DAEMONS_AI_DIR:-$HOME/.local/share/daemons-ai}"
MGBA_APP="${DAEMONS_MGBA_APP:-$HOME/Applications/mGBA-0.11.app}"
PIDS="$ROOT/ai/logs/airun.pids"
HUB="${HANDS_HUB:-${DAEMONS_HUB:-http://daemons-hearth:4730}}"
KEY="${HANDS_KEY:-${DAEMONS_HUB_KEY:-}}"
HARNESS="$ROOT/engineAi"
PY=~/.pyenv/shims/python3; [[ -x $PY ]] || PY=python3

say() { echo "airun: $*"; }
alive() { [[ -f $PIDS ]] && while read -r p _; do kill -0 "$p" 2>/dev/null && return 0; done < "$PIDS"; return 1; }

stop() {
  [[ -f $PIDS ]] || { say "no run-through is going"; return 0; }
  # the reporter first (its goodbye tells the hub), then the agent and bridge, then the run's own mGBA -- by pid, never
  # by name, so the player's emulator is never touched
  while read -r p what; do
    # stopped by the reporter itself (the hub asked the run to end): it is ending on its own, and this is its child
    [[ $what == reporter && -n ${AIRUN_FROM_REPORTER:-} ]] && continue
    kill -0 "$p" 2>/dev/null || continue
    pkill -TERM -P "$p" 2>/dev/null || true
    kill -TERM "$p" 2>/dev/null || true
    say "stopped $what ($p)"
  done < <(tac "$PIDS" 2>/dev/null || tail -r "$PIDS")
  rm -f "$PIDS"
}

status() { if alive; then say "a run-through is going:"; cat "$PIDS"; else say "no run-through is going"; fi; }

start() {
  alive && { say "a run-through is already going -- END it in IN PLAY, or: ai/airun.sh stop"; exit 1; }
  # a run started by bindDaemons.sh --ai holds the same ports
  if lsof -nP -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1 || lsof -nP -iTCP:8888 -sTCP:LISTEN >/dev/null 2>&1; then
    say "the bridge's ports (8000, 8888) are in use -- another AI run (bindDaemons.sh --ai) is going; stop it first"; exit 1
  fi
  case "${DAEMONS_MIND:-mind}" in
    mind|tiiny|seer) export DAEMONS_MIND="${DAEMONS_MIND:-mind}" ;;
    *) say "DAEMONS_MIND=${DAEMONS_MIND}: only a local mind plays from here (mind, tiiny, seer) -- never the paid one"; exit 1 ;;
  esac
  [[ -x "$MGBA_APP/Contents/MacOS/mGBA" ]] || { say "no mGBA 0.11 at $MGBA_APP (it needs --script)"; exit 1; }
  ROM="$ROOT/engineGba/daemonsContent.gba" ELF="$ROOT/engineGba/daemonsContent.elf"
  [[ -f $ROM && -f $ELF ]] || { say "no CONTENT build in engineGba -- build it once (make -C engineGba firered)"; exit 1; }
  LUA=""; for f in "$(cd "$HARNESS/mgba/scripts" && pwd -P)"/*BridgeSocketServer.lua; do [[ -f $f ]] && LUA="$f"; done
  [[ -n $LUA ]] || { say "no bridge script in engineAi/mgba/scripts"; exit 1; }
  BRIDGE_PY="$ROOT/ai/bridgevenv/bin/python"
  [[ -x $BRIDGE_PY ]] || { say "no bridge venv yet -- run ./bindDaemons.sh --ai once to make it"; exit 1; }
  [[ -d "$HARNESS/server/node_modules" ]] || { say "the agent's dependencies are missing: (cd engineAi/server && npm ci)"; exit 1; }

  mkdir -p "$AI_DIR" "$ROOT/ai/logs"
  cp "$ROM" "$AI_DIR/daemonsAI.gba"                  # the newest build; daemonsAI.sav beside it is the AI's own
  say "symbols from this build…"
  "$PY" tools/gbasym.py --write >/dev/null
  export FIRERED_SYM_PATH="$ROOT/ai/pokefirered.sym" FIRERED_BRIDGE_STRICT_SYMBOLS=1
  export DAEMONS_PATHFINDER="${DAEMONS_PATHFINDER:-local}" DAEMONS_DUMP_INPUT="$ROOT/ai/logs/last-input.json"
  # its own notes too, beside its own save -- not the ones bindDaemons.sh --ai's runs leave (engineAi's DAEMONS_DATA_DIR)
  export DAEMONS_DATA_DIR="$AI_DIR/gpt_data"
  unset OPENAI_BASE_URL
  : > "$PIDS"

  open -n -a "$MGBA_APP" --args --script "$LUA" "$AI_DIR/daemonsAI.gba"
  for _ in $(seq 1 40); do lsof -nP -iTCP:8888 -sTCP:LISTEN >/dev/null 2>&1 && break; sleep 0.5; done
  EMU_PID=$(lsof -nP -t -iTCP:8888 -sTCP:LISTEN 2>/dev/null | head -1 || true)
  [[ -n $EMU_PID ]] || { say "mGBA did not open the bridge's port 8888 (see the mGBA window)"; exit 1; }
  echo "$EMU_PID mgba" >> "$PIDS"
  ( cd "$HARNESS" && exec "$BRIDGE_PY" firered_mgba_bridge.py ) > "$ROOT/ai/logs/airun-bridge.log" 2>&1 < /dev/null &
  echo "$! bridge" >> "$PIDS"
  ( cd "$HARNESS/server" && exec npm start ) > "$ROOT/ai/logs/airun-agent.log" 2>&1 < /dev/null &
  echo "$! agent" >> "$PIDS"
  ID="ai-$(date +%Y%m%d-%H%M%S)"
  # the reporter; when the hub asks the run to end (exit 3), the whole run is stopped
  ( "$PY" "$ROOT/ai/inplay_beat.py" --hub "$HUB" --key "$KEY" --id "$ID" --save "$AI_DIR/daemonsAI.sav" \
        --frame "$HARNESS/tmp_screenshots/gba_raw.png" --device "$(scutil --get ComputerName 2>/dev/null || hostname)" \
      > "$ROOT/ai/logs/airun-report.log" 2>&1 || rc=$?
    [[ ${rc:-0} -eq 3 ]] && AIRUN_FROM_REPORTER=1 "$ROOT/ai/airun.sh" stop >> "$ROOT/ai/logs/airun-report.log" 2>&1 || true ) \
    >> "$ROOT/ai/logs/airun-report.log" 2>&1 < /dev/null &   # nothing of the job's own output held open: it ends at once
  echo "$! reporter" >> "$PIDS"
  disown -a
  say "started $ID on $DAEMONS_MIND: mGBA $EMU_PID, logs in ai/logs/airun-*.log"
}

case "${1:-}" in
  start) start ;;
  stop) stop ;;
  status) status ;;
  *) echo "ai/airun.sh start | stop | status" >&2; exit 1 ;;
esac

#!/usr/bin/env bash
# Build an edition if needed, then run it.
#
#   ./bindDaemons.sh                      CONTENT edition (default)
#   ./bindDaemons.sh context              CONTEXT edition
#   ./bindDaemons.sh content --clean
#   ./bindDaemons.sh content --debug      with upstream's debug mode
#
# --debug builds a separate ROM (daemonsContentDebug.gbc) with its own save,
# so a debug run never touches a real playthrough. In it:
#
#   SELECT on the title screen   debug menu -- start a game with a party,
#                                fly anywhere, all the usual test hooks
#   hold B                       skip trainer battles, the Safari step
#                                counter, and some NPC scripts
#
# It is a testing build and not the game: it is not part of `make all`, and
# nothing in it is balanced or intended to be experienced.
#
# Saves live beside the ROM as daemonsContent.sav / daemonsContext.sav and
# survive rebuilds, so a playthrough is not lost when you change a line.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

EDITION=content
CLEAN=0
DEBUG=0
for arg in "$@"; do
  case "$arg" in
    content|context) EDITION="$arg" ;;
    --clean)         CLEAN=1 ;;
    --debug)         DEBUG=1 ;;
    *) echo "usage: ./bindDaemons.sh [content|context] [--clean] [--debug]" >&2; exit 1 ;;
  esac
done

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

[[ $CLEAN -eq 1 ]] && make -C engine clean >/dev/null

echo "building ${TARGET}…"
make -C engine "$TARGET" >/dev/null

if [[ $DEBUG -eq 1 ]]; then
  echo "  debug build: SELECT on the title screen opens the menu; hold B to skip battles."
fi

EMU=""
for app in SameBoy mGBA OpenEmu RetroArch; do
  [[ -d "/Applications/$app.app" ]] && { EMU="$app"; break; }
done

if [[ -z "$EMU" ]]; then
  echo "No emulator found. Try: brew install --cask sameboy" >&2
  echo "ROM is at: $PWD/engine/$ROM" >&2
  exit 1
fi

# macOS `open` against an already-running emulator holding this exact path
# just focuses the window -- it does not reload the file. So a rebuilt ROM
# silently does nothing and you sit there listening to the old one, which is
# exactly what happened with Route 1. Quit it first; SameBoy flushes SRAM on
# a graceful quit, so nothing is lost.
if pgrep -x "$EMU" >/dev/null 2>&1; then
  echo "  ${EMU} is already running -- quitting it so the new ROM actually loads"
  osascript -e "quit app \"$EMU\"" >/dev/null 2>&1 || true
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    pgrep -x "$EMU" >/dev/null 2>&1 || break
    /bin/sleep 0.3
  done
fi

echo "binding ${TARGET} → ${EMU}"
open -a "$EMU" "engine/$ROM"

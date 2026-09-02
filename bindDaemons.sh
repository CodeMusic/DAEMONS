#!/usr/bin/env bash
# Build an edition if needed, then run it.
#
#   ./bindDaemons.sh                      CONTENT edition, GBA
#   ./bindDaemons.sh context              CONTEXT edition, GBA
#   ./bindDaemons.sh --classic            CONTENT edition, Game Boy
#   ./bindDaemons.sh context --classic    CONTEXT edition, Game Boy
#   ./bindDaemons.sh --debug              GBA testing build
#   ./bindDaemons.sh --classic --debug    Game Boy testing build
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
for arg in "$@"; do
  case "$arg" in
    content|context) EDITION="$arg" ;;
    --classic)       CLASSIC=1 ;;
    --clean)         CLEAN=1 ;;
    --debug)         DEBUG=1 ;;
    *) echo "usage: ./bindDaemons.sh [content|context] [--classic] [--clean] [--debug]" >&2; exit 1 ;;
  esac
done

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

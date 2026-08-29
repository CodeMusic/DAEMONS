#!/usr/bin/env bash
# Build an edition if needed, then run it.
#
#   ./bindDaemons.sh              CONTENT edition (default)
#   ./bindDaemons.sh context      CONTEXT edition
#   ./bindDaemons.sh content --clean
#
# Saves live beside the ROM as daemonsContent.sav / daemonsContext.sav and
# survive rebuilds, so a playthrough is not lost when you change a line.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

EDITION="${1:-content}"
case "$EDITION" in
  content) ROM=daemonsContent.gbc ;;
  context) ROM=daemonsContext.gbc ;;
  *) echo "usage: ./bindDaemons.sh [content|context] [--clean]" >&2; exit 1 ;;
esac

[[ "${2:-}" == "--clean" ]] && make -C engine clean >/dev/null

echo "building ${EDITION}…"
make -C engine "$EDITION" >/dev/null

EMU=""
for app in SameBoy mGBA OpenEmu RetroArch; do
  [[ -d "/Applications/$app.app" ]] && { EMU="$app"; break; }
done

if [[ -z "$EMU" ]]; then
  echo "No emulator found. Try: brew install --cask sameboy" >&2
  echo "ROM is at: $PWD/engine/$ROM" >&2
  exit 1
fi

echo "binding ${EDITION} → ${EMU}"
open -a "$EMU" "engine/$ROM"

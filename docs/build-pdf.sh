#!/usr/bin/env bash
# Render docs/vision.md to a versioned PDF snapshot.
#
#   ./docs/build-pdf.sh 1.2            -> the design bible at that version
#   ./docs/build-pdf.sh lineage.md     -> any other doc in docs/
#
# Needs pandoc and Google Chrome. The v1.0 snapshot was cut with wkhtmltopdf,
# which is no longer installed; Chrome's print-to-pdf is the replacement and
# targets the same A4 page.
set -euo pipefail

ARG="${1:?usage: build-pdf.sh <version|file.md>   e.g. build-pdf.sh 1.2   |   build-pdf.sh lineage.md}"
DOCS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$ARG" == *.md ]]; then
  SRC="$DOCS/$ARG"
  OUT="$DOCS/${ARG%.md}.pdf"
  TITLE="CONTEXT / CONTENT — ${ARG%.md}"
else
  SRC="$DOCS/vision.md"
  OUT="$DOCS/CONTEXT-CONTENT-design-bible-v${ARG}.pdf"
  TITLE="CONTEXT / CONTENT — design bible v${ARG}"
fi
[ -f "$SRC" ] || { echo "no such doc: $SRC" >&2; exit 1; }
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || { echo "Chrome not found at $CHROME" >&2; exit 1; }

printf '<style>\n' > "$TMP/head.html"
cat "$DOCS/style.css" >> "$TMP/head.html"
printf '\n</style>\n' >> "$TMP/head.html"

pandoc "$SRC" \
  --from=gfm --to=html5 --standalone \
  --metadata pagetitle="$TITLE" \
  --include-in-header="$TMP/head.html" \
  --output="$TMP/bible.html"

"$CHROME" --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer --print-to-pdf-no-header \
  --print-to-pdf="$TMP/out.pdf" "file://$TMP/bible.html" 2>/dev/null

mv "$TMP/out.pdf" "$OUT"
echo "wrote $OUT"

#!/usr/bin/env bash
# Render docs/vision.md to a versioned PDF snapshot.
#
#   ./docs/build-pdf.sh 1.2            -> the design bible at that version
#   ./docs/build-pdf.sh lineage.md     -> any other markdown doc in docs/
#   ./docs/build-pdf.sh items.html     -> a styled html doc, printed as-is
#
# Needs pandoc and Google Chrome. The v1.0 snapshot was cut with wkhtmltopdf,
# which is no longer installed; Chrome's print-to-pdf is the replacement and
# targets the same A4 page.
set -euo pipefail

ARG="${1:?usage: build-pdf.sh <version|file.md>   e.g. build-pdf.sh 1.2   |   build-pdf.sh lineage.md}"
DOCS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Chrome can write the whole PDF and then crash on its way out (2026-11-11: a
# teardown watchdog, exit 2), and under set -e that exit used to abort before the
# mv, leaving no PDF and no message. Judge the run by the file, not the exit code.
print_pdf() {
  local out="$1" url="$2"
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-sandbox \
    --no-pdf-header-footer --print-to-pdf-no-header \
    --print-to-pdf="$out" "$url" 2>/dev/null || true
  [ -s "$out" ] || { echo "Chrome wrote no PDF for $url" >&2; exit 1; }
}

if [[ "$ARG" == *.html ]]; then
  # An html doc is already styled and already standalone -- Chrome prints it
  # directly, no pandoc and no style.css. This is how type-chart.pdf is cut.
  SRC="$DOCS/$ARG"
  OUT="$DOCS/${ARG%.html}.pdf"
  [ -f "$SRC" ] || { echo "no such doc: $SRC" >&2; exit 1; }
  CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  [ -x "$CHROME" ] || { echo "Chrome not found at $CHROME" >&2; exit 1; }
  TMPD="$(mktemp -d)"; trap 'rm -rf "$TMPD"' EXIT
  print_pdf "$TMPD/out.pdf" "file://$SRC"
  mv "$TMPD/out.pdf" "$OUT"
  echo "wrote $OUT"
  exit 0
fi

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

print_pdf "$TMP/out.pdf" "file://$TMP/bible.html"

mv "$TMP/out.pdf" "$OUT"
echo "wrote $OUT"

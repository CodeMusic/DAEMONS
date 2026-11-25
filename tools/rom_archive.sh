#!/bin/bash
# T-637 (the user, 2026-11-25: "roverbyteseer keeps them all ... my local macbook pro here only keeps the last 2 weeks
# worth of rom releases"): every ROM release is kept on roverbyteseer's external drive, and this machine keeps two weeks.
#
#   tools/rom_archive.sh            copy every release there, then remove here what is older than two weeks
#   tools/rom_archive.sh --dry-run  say what it would copy and remove
#
# 1. Copies all of ROM RELEASE/ (never CART BACKUPS -- those are private files, T-636) into the archive there. It never
#    deletes anything in the archive: the archive only grows (trim it by hand if its space ever runs short).
# 2. For each release group whose newest release was made before the cutoff (KEEP_DAYS ago), it removes HERE only the
#    files git ignores (the ROMs, DEBUG/, PATCHES/) and only once every one of them has the same SHA-1 in the archive.
#    The tracked notes, PDFs and .release.json stay, so git sees no change.
# When roverbyteseer or its drive can't be reached it says so and changes nothing here.
set -uo pipefail
HOST="${ROM_ARCHIVE_HOST:-roverbyte@roverbyteseer}"
DEST="${ROM_ARCHIVE_DEST:-/Volumes/CODE_Backup/DAEMONS ROM ARCHIVE}"   # moves to THE HOARD once it exists (C-500)
KEEP_DAYS="${ROM_ARCHIVE_KEEP_DAYS:-14}"
DRY=0; [[ "${1:-}" == "--dry-run" ]] && DRY=1
cd "$(dirname "$0")/.." || exit 1
R="ROM RELEASE"
say() { echo "$(date '+%Y-%m-%d %H:%M') rom_archive: $*"; }
# rsync 3.2.4+ sends its paths unparsed by the remote shell (protected args): the rsync destination is NOT escaped
SSH=(ssh -o BatchMode=yes -o ConnectTimeout=10 "$HOST")
q() { printf '%q' "$1"; }

"${SSH[@]}" "test -d $(q "$(dirname "$DEST")") && mkdir -p $(q "$DEST/$R")" 2>/dev/null \
  || { say "$HOST or its drive ($(dirname "$DEST")) can't be reached; nothing changed"; exit 0; }

# 1. copy everything (no --delete: the archive keeps every release ever made)
if (( DRY )); then
  say "would copy: $(rsync -a --dry-run --itemize-changes --exclude 'CART BACKUPS' --exclude .DS_Store -e "ssh -o BatchMode=yes" \
      "$R/" "$HOST:$DEST/$R/" | grep -c '^<f') files"
else
  rsync -a --exclude 'CART BACKUPS' --exclude .DS_Store -e "ssh -o BatchMode=yes" "$R/" "$HOST:$DEST/$R/"; rc=$?
  # 24: a file vanished mid-copy (a release sealing its group meanwhile) -- harmless, the SHA-1 check below decides
  (( rc == 0 || rc == 24 )) || { say "the copy failed (rsync $rc); nothing removed here"; exit 1; }
fi

# 2. trim here: groups whose newest release is older than the cutoff
cutoff=$(date -v-"${KEEP_DAYS}"d '+%Y-%m-%dT%H:%M:%S')
freed=0
latest=$(ls -d "$R"/v*.x 2>/dev/null | sort -V | tail -1)   # never trimmed: romrelease.py seals it from these files
for g in "$R"/v*.x; do
  [[ -d "$g" && "$g" != "$latest" ]] || continue
  newest=$(find "$g" -name .release.json -exec grep -ho '"made": *"[^"]*"' {} + 2>/dev/null | sed 's/.*"\([^"]*\)"$/\1/' | sort | tail -1)
  [[ -n "$newest" && "$newest" < "$cutoff" ]] || continue
  files=()
  while IFS= read -r f; do [[ "$(basename "$f")" == .DS_Store ]] || files+=("$f"); done \
    < <(git ls-files -o -i --exclude-standard -- "$g")
  (( ${#files[@]} )) || continue
  kb=$(du -skc "${files[@]}" | tail -1 | cut -f1)
  if (( DRY )); then say "would remove here: ${g#$R/} (${#files[@]} files, $((kb/1024)) MB; made $newest)"; continue; fi
  here=$(shasum "${files[@]}" | sort -k2)
  there=$("${SSH[@]}" "cd $(q "$DEST") && shasum $(for f in "${files[@]}"; do q "$f"; printf ' '; done)" 2>/dev/null | sort -k2)
  if [[ "$here" == "$there" ]]; then
    rm -f "${files[@]}" && find "$g" -depth -type d -empty -delete
    freed=$((freed + kb)); say "removed here: ${g#$R/} (${#files[@]} files; the archive has them, checked by SHA-1)"
  else
    say "kept ${g#$R/}: its SHA-1s differ in the archive"
  fi
done
(( DRY )) || say "done; freed $((freed/1024)) MB here"
exit 0

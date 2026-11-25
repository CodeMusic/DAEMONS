#!/bin/bash
# T-636 (the user, 2026-11-25: "the private files are very important and cannot get lost ... zip up the private files
# add a password ... along with a script to repopulate them if a catastrophe event ever happened"): once a week, on
# roverbyteseer, every private file goes into one AES-256 7-Zip archive on its external drive, names and all encrypted.
#
#   tools/private_archive.sh             make this week's archive (run weekly by ca.codemusic.private-archive)
#   tools/private_archive.sh --dry-run   list what would go in, and how much
#
# What goes in (paths relative to the home folder, so a restore lands the same on either machine):
#   - every path Syncthing shares between the two machines: the !/ lines of each repo's .stignore (T-636), so the
#     archive and the sync never disagree about what is private
#   - ROM RELEASE/CART BACKUPS (the user's own cart dumps; carried here by egg_sync, E-20)
#   - daemons-eudaimonia/data/ (roverbyteseer's live site: accounts, spaces, saves), without its logs
#   - the key files ~/.redmine.env and ~/.eudaimonia-site.env
# Each archive carries MANIFEST.sha256, every file's SHA-256, which private_restore.sh checks on the way back out.
# The password is read from this machine's keychain (service daemons-private-archive) -- never from a file, never
# written down here. Archives older than the newest KEEP are removed. The restore script and its README are copied
# beside the archives, so the drive alone is enough to recover. Nothing is ever pushed anywhere.
set -uo pipefail
DEST="${PRIVATE_ARCHIVE_DEST:-/Volumes/CODE_Backup/DAEMONS PRIVATE ARCHIVE}"   # moves to THE HOARD with C-500
KEEP="${PRIVATE_ARCHIVE_KEEP:-12}"
SERVICE=daemons-private-archive
SEVENZ=/opt/homebrew/bin/7zz
DRY=0; [[ "${1:-}" == "--dry-run" ]] && DRY=1
TOOLS="$(cd "$(dirname "$0")" && pwd)"
say() { echo "$(date '+%Y-%m-%d %H:%M') private_archive: $*"; }
cd "$HOME" || exit 1

list=$(mktemp); trap 'rm -f "$list"; rm -rf "${stage:-}"' EXIT
add() { [[ -e "$1" ]] && printf '%s\n' "$1" >> "$list"; }
for repo in Projects/DAEMONS Projects/daemons-companion; do
  [[ -f "$repo/.stignore" ]] || { say "no $repo/.stignore -- the sync's list of private paths is missing"; exit 1; }
  while IFS= read -r p; do
    for m in $repo/$p; do add "$m"; done        # a pattern such as gfx/drafts/crystal_back_* expands here
  done < <(sed -n 's:^!/::p' "$repo/.stignore")
done
add "Projects/DAEMONS/ROM RELEASE/CART BACKUPS"
add Projects/daemons-eudaimonia/data
add .redmine.env
add .eudaimonia-site.env

files=$(mktemp)
while IFS= read -r p; do find "$p" -type f ! -name .DS_Store ! -name '*.log' ! -path '*/.stversions/*'; done < "$list" | sort > "$files"
n=$(wc -l < "$files" | tr -d ' ')
mb=$(tr '\n' '\0' < "$files" | xargs -0 du -k 2>/dev/null | awk '{s+=$1} END{print int(s/1024)}')
if (( DRY )); then say "would archive $n files, $mb MB, from:"; sed 's/^/    /' "$list"; rm -f "$files"; exit 0; fi

[[ -d "$(dirname "$DEST")" ]] || { say "the drive ($(dirname "$DEST")) isn't mounted; nothing made"; exit 1; }
pw="${PRIVATE_ARCHIVE_PASSWORD:-$(security find-generic-password -s "$SERVICE" -w 2>/dev/null)}"
[[ -n "$pw" ]] || { say "no password in the keychain (service $SERVICE); see docs/PRIVATE_BACKUP.md"; exit 1; }
mkdir -p "$DEST" && chmod 700 "$DEST"

# the manifest travels inside the archive, at its root
stage=$(mktemp -d); tr '\n' '\0' < "$files" | xargs -0 shasum -a 256 > "$stage/MANIFEST.sha256"
out="$DEST/daemons-private-$(date +%Y-%m-%d).7z"; tmp="$out.partial"; rm -f "$tmp"
if "$SEVENZ" a -t7z -mhe=on -mx=5 -p"$pw" -bso0 -bsp0 "$tmp" @"$files" && \
   (cd "$stage" && "$SEVENZ" a -t7z -mhe=on -p"$pw" -bso0 -bsp0 "$tmp" MANIFEST.sha256) && \
   "$SEVENZ" t -p"$pw" -bso0 -bsp0 "$tmp"; then
  mv -f "$tmp" "$out"; chmod 600 "$out"
  say "made $(basename "$out"): $n files, $mb MB in, $(du -m "$out" | cut -f1) MB out; tested"
else
  rm -f "$tmp" "$files"; say "the archive failed; the last good one is kept"; exit 1
fi
rm -f "$files"; unset pw

# the way back, beside the archives
cp "$TOOLS/private_restore.sh" "$DEST/"
git -C "$TOOLS/.." show HEAD:docs/PRIVATE_BACKUP.md > "$DEST/README.md" 2>/dev/null   # works in a sparse checkout too
old=$(ls -1 "$DEST"/daemons-private-*.7z 2>/dev/null | sort | awk -v k="$KEEP" '{a[NR]=$0} END{for(i=1;i<=NR-k;i++) print a[i]}')
[[ -n "$old" ]] && while IFS= read -r f; do rm -f "$f" && say "removed the old $(basename "$f")"; done <<< "$old"
exit 0

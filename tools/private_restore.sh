#!/bin/bash
# T-636: the way back from tools/private_archive.sh. Works from the repository or from the copy kept beside the
# archives on roverbyteseer's drive; needs only 7-Zip (brew install sevenzip) and the archive's password.
#
#   private_restore.sh ARCHIVE.7z                 unpack into a new folder beside you, and check every file's SHA-256
#   private_restore.sh ARCHIVE.7z --into DIR      unpack into DIR instead (it must not exist yet)
#   private_restore.sh ARCHIVE.7z --in-place      unpack, check, then put every file back under your home folder:
#                                                 missing files are added, older ones replaced, and any file it
#                                                 replaces is kept beside it as NAME.before-restore
#
# The password is asked for (never typed on the command line); on a machine whose keychain holds it (service
# daemons-private-archive) it is read from there. Nothing is changed until every file in the archive checks out.
set -uo pipefail
SEVENZ=$(command -v 7zz || command -v 7z || echo /opt/homebrew/bin/7zz)
[[ -x "$SEVENZ" ]] || { echo "7-Zip is needed: brew install sevenzip"; exit 1; }
arc="${1:-}"; [[ -f "$arc" ]] || { sed -n '2,13p' "$0"; exit 1; }
mode=check; into="./private-restore-$(date +%Y%m%d-%H%M%S)"
case "${2:-}" in --into) into="${3:?--into needs a folder}";; --in-place) mode=place;; "") ;; *) echo "unknown: $2"; exit 1;; esac
[[ -e "$into" ]] && { echo "$into already exists; choose a new folder"; exit 1; }

pw="${PRIVATE_ARCHIVE_PASSWORD:-$(security find-generic-password -s daemons-private-archive -w 2>/dev/null)}"
[[ -n "$pw" ]] || { read -r -s -p "Archive password: " pw; echo; }

mkdir -p "$into" && chmod 700 "$into"
"$SEVENZ" x -p"$pw" -bso0 -bsp0 -o"$into" "$arc" || { echo "could not open the archive (wrong password?)"; rm -rf "$into"; exit 1; }
unset pw
(cd "$into" && shasum -a 256 -c --quiet MANIFEST.sha256) || { echo "SOME FILES DO NOT MATCH THE MANIFEST; nothing placed. Unpacked in $into"; exit 1; }
n=$(wc -l < "$into/MANIFEST.sha256" | tr -d ' ')
echo "all $n files unpacked into $into and checked against the manifest"

if [[ "$mode" == place ]]; then
  (cd "$into" && rsync -a --update --backup --suffix=.before-restore --exclude MANIFEST.sha256 ./ "$HOME/") \
    || { echo "putting the files back failed part way; the unpacked copy is still in $into"; exit 1; }
  echo "put back under $HOME (newer files there were left alone; replaced ones kept as *.before-restore)"
  rm -rf "$into"
fi

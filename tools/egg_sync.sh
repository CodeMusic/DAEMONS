#!/bin/bash
# E-20 (the user, 2026-11-23: "please automate syncing new releases to roverbyteseer"): THE EASTER EGG on roverbyteseer
# plays the newest release, so each new one is carried there from this machine, where the releases are made.
#
#   tools/egg_sync.sh            carry what is missing (run hourly by the login agent ca.codemusic.egg-sync)
#   tools/egg_sync.sh --dry-run  say what it would carry
#
# It carries ONLY what the egg needs -- the newest release's two ROMs and its PATCHES/, and ROM RELEASE/CART BACKUPS when
# they changed -- into roverbyteseer's slim DAEMONS checkout, where git ignores them exactly as it does here, so they
# can never be pushed. Older releases' ROMs there are pruned to the newest KEEP. When roverbyteseer can't be reached
# (this laptop away from the tailnet) it says so and stops: the next hour tries again. It never deletes anything here.
set -uo pipefail
HOST="${EGG_SYNC_HOST:-roverbyte@roverbyteseer}"
REMOTE="${EGG_SYNC_DAEMONS:-Projects/DAEMONS}"          # relative to the remote home
KEEP="${EGG_SYNC_KEEP:-3}"
DRY=0; [[ "${1:-}" == "--dry-run" ]] && DRY=1
cd "$(dirname "$0")/.." || exit 1
R="ROM RELEASE"
say() { echo "$(date '+%Y-%m-%d %H:%M') egg_sync: $*"; }
ssh_() { ssh -o BatchMode=yes -o ConnectTimeout=10 "$HOST" "$@" 2>/dev/null; }

# the newest release that has both editions and its patches -- the one the egg plays
newest=""
while IFS= read -r d; do
  [[ -f "$d/daemonsContent.gba" && -f "$d/daemonsContext.gba" && -d "$d/PATCHES" ]] && newest="$d"
done < <(ls -d "$R"/v*.x/v*/ 2>/dev/null | sed 's:/$::' | sort -V)
[[ -n "$newest" ]] || { say "no release here with both ROMs and PATCHES"; exit 0; }

ssh_ true || { say "$HOST can't be reached; trying again next hour"; exit 0; }

files=("$newest/daemonsContent.gba" "$newest/daemonsContext.gba" "$newest/PATCHES")
here=$(cd "$newest" && shasum daemonsContent.gba daemonsContext.gba PATCHES/*.bps)
there=$(ssh_ "cd '$REMOTE/$newest' 2>/dev/null && shasum daemonsContent.gba daemonsContext.gba PATCHES/*.bps")
carry=()
[[ "$here" == "$there" ]] || carry+=("${files[@]}")
if [[ -d "$R/CART BACKUPS" ]]; then
  ch=$(cd "$R/CART BACKUPS" && find . -type f ! -name .DS_Store -exec shasum {} + | sort)
  ct=$(ssh_ "cd '$REMOTE/$R/CART BACKUPS' 2>/dev/null && find . -type f ! -name .DS_Store -exec shasum {} + | sort")
  [[ "$ch" == "$ct" ]] || carry+=("$R/CART BACKUPS")
fi

if (( ${#carry[@]} )); then
  if (( DRY )); then say "would carry: ${carry[*]}"; else
    # nothing carried may be a file git would track there: the same .gitignore as here decides
    for f in "${carry[@]}"; do git check-ignore -q "$f" || git check-ignore -q "$f/x.gba" || { say "refused: $f is not ignored by git"; exit 1; }; done
    if tar -cf - "${carry[@]}" | ssh -o BatchMode=yes -o ConnectTimeout=10 "$HOST" "cd '$REMOTE' && tar -xpf - && chmod -R go-rwx '$R/CART BACKUPS' 2>/dev/null; true"; then
      there=$(ssh_ "cd '$REMOTE/$newest' && shasum daemonsContent.gba daemonsContext.gba PATCHES/*.bps")
      [[ "$here" == "$there" ]] && say "carried ${newest#$R/} (and what else changed); checked by SHA-1" || { say "carried ${newest#$R/} but its SHA-1s differ there"; exit 1; }
    else say "the copy to $HOST failed; trying again next hour"; exit 1; fi
  fi
else
  say "roverbyteseer already has ${newest#$R/}"
fi

# prune: on roverbyteseer only, the ROMs and patches of all but the newest KEEP releases (the tracked notes stay)
old=$(ssh_ "cd '$REMOTE' && for d in '$R'/v*.x/v*/; do [ -f \"\${d}daemonsContent.gba\" ] && echo \"\${d%/}\"; done" | sort -V |
      awk -v k="$KEEP" '{a[NR]=$0} END{for(i=1;i<=NR-k;i++) print a[i]}')
while IFS= read -r d; do
  [[ -z "$d" ]] && continue
  if (( DRY )); then say "would prune ${d#$R/} there"; else
    ssh_ "cd '$REMOTE' && rm -f '$d/daemonsContent.gba' '$d/daemonsContext.gba' && rm -rf '$d/PATCHES'" && say "pruned ${d#$R/} there"
  fi
done <<< "$old"
exit 0

#!/bin/bash
# tickets_nightly.sh -- the tickets, mirrored to GitHub every night (T-581; the user, 2026-11-17: "we have nightly
# backups, and mirror the content (and include the back up) to github").
#
# Runs on the author's Mac from launchd (ca.codemusic.tickets-nightly, 04:45, after roverbyteseer's 03:30 backup and the
# 04:30 pull of it). It works in its OWN slim clones under ~/.local/share/daemons-tickets, never the shared checkout,
# so it cannot take another session's work into its commit.
#
#   truth = files    (until the cut-over): files -> Redmine (`sync`), then prove Redmine rebuilds the files exactly.
#   truth = redmine  (after it): Redmine -> both TODO files (`mirror`, which refuses to drop any ticket).
#   Either way: `export` writes every ticket with its history to docs/tickets/redmine-export.json, the secrets check
#   runs, and only the TODO files and the export are committed (by path) and pushed. The raw database dump never is:
#   it holds keys and password hashes, and stays on roverbyteseer and in ~/Backups/redmine-roverbyteseer.
#
# The mode is the one word in ~/.local/share/daemons-tickets/truth (default: files). Log: nightly.log beside it.
set -uo pipefail
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin

BASE="$HOME/.local/share/daemons-tickets"
D="$BASE/DAEMONS"
C="$BASE/daemons-companion"
MAIN="$HOME/Projects/DAEMONS"           # only for docs/private (the secrets patterns), linked in, never written
PY=/usr/bin/python3
TRUTH=$(tr -d '[:space:]' < "$BASE/truth" 2>/dev/null || true); TRUTH=${TRUTH:-files}
SIGN="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"

log()  { echo "$(date '+%F %T') $*"; }
fail() { log "FAILED: $*"; exit 1; }

setup() {   # first run only: slim clones, and the links tickets.py and check_secrets.py expect
  mkdir -p "$BASE"
  if [ ! -d "$D/.git" ]; then
    git clone -q --depth 1 --filter=blob:none --sparse https://github.com/CodeMusic/DAEMONS.git "$D" || return 1
    git -C "$D" sparse-checkout set --no-cone /.gitignore /docs/TODO.md /docs/tickets/ /tools/tickets.py \
      /tools/tickets_nightly.sh /tools/check_secrets.py || return 1
  fi
  [ -d "$C/.git" ] || git clone -q --depth 1 https://github.com/CodeMusic/daemons-companion.git "$C" || return 1
  ln -sfn "$C" "$D/companion"
  [ -d "$MAIN/docs/private" ] && ln -sfn "$MAIN/docs/private" "$D/docs/private"
  return 0
}

fresh() { git -C "$1" fetch -q --depth 1 origin main && git -C "$1" reset -q --hard origin/main; }

secrets_ok() {   # the DAEMONS clone through check_secrets.py; the companion's TODO through the same patterns
  ( cd "$D" && $PY tools/check_secrets.py --quiet ) || return 1
  $PY - "$D/docs/private/secrets_patterns.txt" "$C/TODO.md" <<'EOF'
import re, sys
from pathlib import Path
pat = Path(sys.argv[1])
if not pat.exists():
    print("secrets: no patterns here; companion TODO not checked"); sys.exit(0)
rx = [re.compile(l.strip()) for l in pat.read_text().splitlines()
      if l.strip() and not l.strip().startswith("#")]
hits = sum(1 for line in Path(sys.argv[2]).read_text().split("\n") for r in rx if r.search(line))
if hits:
    print(f"secrets: {hits} line(s) of the companion's TODO match a pattern (not shown)"); sys.exit(1)
EOF
}

commit_push() {   # repo, message, paths...
  local repo=$1 msg=$2; shift 2
  git -C "$repo" add -- "$@"
  if git -C "$repo" diff --cached --quiet -- "$@"; then log "$(basename "$repo"): nothing changed"; return 0; fi
  git -C "$repo" commit -q -m "$msg" -m "$SIGN" -- "$@" || return 1
  git -C "$repo" push -q origin HEAD:main || return 2
  log "$(basename "$repo"): pushed $(git -C "$repo" rev-parse --short HEAD)"
}

log "start (truth: $TRUTH)"
# A release in progress must not get a ticket commit pushed into the middle of it (The Subtle Layer, 2026-11-17: a
# HOLD is only a message, and a push during one is not refused). Wait while a release runs or a lane holds the lock
# file, checking every 5 minutes for up to 3 hours; then skip the night rather than push into it.
HOLD_FILE="$HOME/.cache/daemons/release.hold"
releasing() {
  [ -e "$HOLD_FILE" ] && { echo "the hold file ($(head -c 120 "$HOLD_FILE" 2>/dev/null))"; return 0; }
  p=$(pgrep -fl '^[^ ]*python[0-9.]*( -[^ ]+)* [^ ]*(romrelease|check_fresh_clone|ghrelease|releasedocs)\.py|^[^ ]*make .*(firered|leafgreen)' | head -1)
  [ -n "$p" ] && { echo "a release process (${p:0:80})"; return 0; }
  return 1
}
for wait in $(seq 1 36); do
  why=$(releasing) || break
  [ "$wait" -eq 36 ] && { log "skipped: a release was still in progress after 3 hours -- $why"; exit 0; }
  [ "$wait" -eq 1 ] && log "waiting: $why"
  sleep 300
done
setup || fail "could not clone"
for attempt in 1 2 3; do
  fresh "$D" && fresh "$C" || fail "could not fetch"
  cd "$D" || fail "no clone"
  if [ "$TRUTH" = redmine ]; then
    # a row someone wrote into a TODO file by hand becomes a ticket rather than being refused or lost
    $PY tools/tickets.py sync --write --create-only | grep -v -E '^  .*: [0-9]+/' || fail "create-only sync"
    $PY tools/tickets.py mirror --from-redmine --write || fail "the mirror refused (a ticket in the files is not in Redmine); nothing committed"
  else
    $PY tools/tickets.py sync --write | grep -v -E '^  .*: [0-9]+/' || fail "sync"
    $PY tools/tickets.py mirror --from-redmine | grep -E 'current|differs|REFUSED' || true
  fi
  $PY tools/tickets.py export || fail "export"
  secrets_ok || fail "a secrets pattern matched; nothing committed"
  day=$(date +%F)
  commit_push "$D" "Tickets nightly $day: the Redmine export (T-581)" docs/TODO.md docs/tickets/redmine-export.json
  r=$?
  if [ $r -eq 0 ] && [ "$TRUTH" = redmine ]; then
    commit_push "$C" "Tickets nightly $day: TODO.md mirrored from Redmine (T-581)" TODO.md; r=$?
  fi
  [ $r -eq 0 ] && { log "done"; exit 0; }
  [ $r -eq 1 ] && fail "commit"
  log "push refused (someone pushed first); starting again from origin ($attempt/3)"
done
fail "push refused three times"

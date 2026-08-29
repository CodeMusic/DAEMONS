#!/usr/bin/env bash
# Reconstruct the working setup after a fresh clone.
#
#   git clone https://github.com/CodeMusic/DAEMONS.git
#   cd DAEMONS && ./setup.sh
#
# Idempotent — safe to run again any time something looks wrong.
# See docs/two-repo-pattern.md for why it is built this way.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

ENGINE_REPO="https://github.com/CodeMusic/pokered-daemons.git"
UPSTREAM="https://github.com/pret/pokered.git"
ENGINE_DIR="../pokered-daemons"
BRANCH="context-content"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

say "1/4  engine checkout"
if [[ -d "$ENGINE_DIR/.git" ]]; then
  echo "     already present at $(cd "$ENGINE_DIR" && pwd)"
else
  git clone "$ENGINE_REPO" "$ENGINE_DIR"
  git -C "$ENGINE_DIR" checkout "$BRANCH"
fi

say "2/4  remotes"
if ! git -C "$ENGINE_DIR" remote | grep -qx upstream; then
  git -C "$ENGINE_DIR" remote add upstream "$UPSTREAM"
  echo "     added upstream -> pret/pokered"
else
  echo "     upstream already set"
fi
git -C "$ENGINE_DIR" remote -v | sed 's/^/     /'

say "3/4  symlink"
ln -sfn "$ENGINE_DIR" engine
ls -la engine | sed 's/^/     /'

say "4/4  toolchain"
if command -v rgbasm >/dev/null; then
  echo "     rgbds $(rgbasm --version 2>&1 | head -1)"
else
  echo "     rgbds MISSING — run: brew install rgbds" >&2
  exit 1
fi

say "ready"
cat <<'EOS'
     make content        build the CONTENT edition
     make context        build the CONTEXT edition
     make play           build and launch
     make vanilla-check  prove the toolchain against pristine upstream
EOS

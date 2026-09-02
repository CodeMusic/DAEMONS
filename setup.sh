#!/usr/bin/env bash
# Reconstruct the working setup after a fresh clone.
#
#   git clone https://github.com/CodeMusic/DAEMONS.git
#   cd DAEMONS && ./setup.sh
#
# Idempotent — safe to run again any time something looks wrong.
# See docs/two-repo-pattern.md for why it is built this way.
#
# There are two engines now. The Game Boy one holds the vertical slice; the
# GBA one is a spike being evaluated. Neither is vendored: both carry
# Nintendo-derived graphics and this repo promises not to distribute them.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

BRANCH="context-content"
say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

engine() { # name  link  repo  upstream
  local name="$1" link="$2" repo="$3" up="$4" dir="../$(basename "$repo" .git)"
  if [[ -d "$dir/.git" ]]; then
    echo "     $name already at $(cd "$dir" && pwd)"
  else
    git clone "$repo" "$dir"
    git -C "$dir" checkout "$BRANCH" 2>/dev/null || git -C "$dir" checkout -b "$BRANCH"
  fi
  git -C "$dir" remote | grep -qx upstream || git -C "$dir" remote add upstream "$up"
  ln -sfn "$dir" "$link"
  echo "     $link -> $dir  (upstream $(basename "$up" .git))"
}

say "1/3  engines"
engine "classic" engine    "https://github.com/CodeMusic/pokered-daemons.git" \
                           "https://github.com/pret/pokered.git"
engine "gba"     engineGba "https://github.com/CodeMusic/pokefirered-daemons.git" \
                           "https://github.com/pret/pokefirered.git"

say "2/3  toolchains"
if command -v rgbasm >/dev/null; then
  echo "     rgbds    $(rgbasm --version 2>&1 | head -1)"
else
  echo "     rgbds    MISSING — brew install rgbds" >&2
fi
export PATH="/opt/homebrew/bin:$PATH"
if command -v arm-none-eabi-as >/dev/null; then
  echo "     arm      $(arm-none-eabi-as --version 2>&1 | head -1)"
else
  echo "     arm      MISSING — brew install arm-none-eabi-gcc" >&2
fi
# agbcc is a compiler built from source and installed INTO the engine
# checkout, so it does not survive a fresh clone of the fork either.
if [[ -x engineGba/tools/agbcc/bin/agbcc ]]; then
  echo "     agbcc    installed in engineGba/tools/agbcc"
else
  echo "     agbcc    MISSING — building it now"
  rm -rf /tmp/agbcc
  git clone --quiet --depth 1 https://github.com/pret/agbcc.git /tmp/agbcc
  ( cd /tmp/agbcc && ./build.sh >/dev/null && ./install.sh "$PWD/engineGba" >/dev/null )
  echo "     agbcc    built and installed"
fi

say "3/3  emulators"
for pair in "SameBoy:sameboy" "mGBA:mgba"; do
  app="${pair%%:*}"; cask="${pair##*:}"
  if [[ -d "/Applications/$app.app" ]]; then echo "     $app"
  else echo "     $app MISSING — brew install --cask $cask" >&2; fi
done

say "ready"
cat <<'EOS'
     ./bindDaemons.sh              CONTENT on GBA
     ./bindDaemons.sh --classic    CONTENT on Game Boy (this is where the slice is)
     make content                  classic build only
     make vanilla-check            prove the classic toolchain
EOS

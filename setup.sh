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
  local name="$1" link="$2" repo="$3" up="$4"
  # Parameter expansion, not $(basename) -- the subshell came back empty in at
  # least one shell here, which collapsed dir to ".." and made git try to clone
  # over the parent directory.
  local slug="${repo##*/}"; slug="${slug%.git}"
  local dir="../$slug"
  [[ -d "$dir/.git" ]] || git clone "$repo" "$dir"
  git -C "$dir" remote | grep -qx upstream || git -C "$dir" remote add upstream "$up"

  # Always ensure the branch, not just on a fresh clone. An earlier version
  # only did this inside the clone arm, so a checkout that already existed was
  # left on whatever branch it happened to be on -- which is exactly what a
  # re-clone leaves you with: master, and none of the work, and no obvious
  # sign that anything is wrong.
  local now; now="$(git -C "$dir" branch --show-current)"
  if [[ "$now" != "$BRANCH" ]]; then
    git -C "$dir" fetch --quiet origin
    if git -C "$dir" show-ref --quiet "refs/remotes/origin/$BRANCH"; then
      git -C "$dir" checkout --quiet -B "$BRANCH" --track "origin/$BRANCH"
      echo "     $name was on $now — switched to $BRANCH"
    else
      git -C "$dir" checkout --quiet -b "$BRANCH"
      echo "     $name was on $now — created $BRANCH"
    fi
  fi
  ln -sfn "$dir" "$link"
  echo "     $link -> $dir  ($(git -C "$dir" branch --show-current), upstream ${up##*/})"
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
  echo "     agbcc    MISSING — building it now (a few minutes)"
  rm -rf /tmp/agbcc
  git clone --quiet --depth 1 https://github.com/pret/agbcc.git /tmp/agbcc
  # Resolve the destination BEFORE the cd. install.sh takes a path, and $PWD
  # inside that subshell is /tmp/agbcc -- an earlier version passed
  # "$PWD/engineGba" from in there, installed the compiler into
  # /tmp/agbcc/engineGba, and cheerfully printed "built and installed".
  target="$(cd engineGba && pwd -P)"
  # agbcc is a 1998 compiler built by a 2026 one. It emits a wall of
  # deprecated-prototype warnings that are not a problem, so a normal run does
  # not look like a failure.
  ( cd /tmp/agbcc && ./build.sh && ./install.sh "$target" ) >/tmp/agbcc-install.log 2>&1 \
    || { echo "     agbcc BUILD FAILED — see /tmp/agbcc-install.log" >&2; exit 1; }
  # And check it actually landed, rather than trusting the exit code.
  [[ -x engineGba/tools/agbcc/bin/agbcc ]] \
    || { echo "     agbcc did not land in engineGba/tools/agbcc" >&2; exit 1; }
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

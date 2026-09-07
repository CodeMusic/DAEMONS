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

say "1/5  engines"
engine "classic" engine    "https://github.com/CodeMusic/pokered-daemons.git" \
                           "https://github.com/pret/pokered.git"
engine "gba"     engineGba "https://github.com/CodeMusic/pokefirered-daemons.git" \
                           "https://github.com/pret/pokefirered.git"

say "2/5  toolchains"
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

say "3/5  emulators"
for pair in "SameBoy:sameboy" "mGBA:mgba"; do
  app="${pair%%:*}"; cask="${pair##*:}"
  if [[ -d "/Applications/$app.app" ]]; then echo "     $app"
  else echo "     $app MISSING — brew install --cask $cask" >&2; fi
done

# ---- 4/4 the AI harness --------------------------------------------------
#
# THIRD-PARTY AND TREATED AS SUCH. This is not one of ours: no upstream remote,
# no branch of ours, and it is cloned shallow. It drives mGBA over a Lua socket
# and reads the game out of RAM -- no screenshots anywhere, which is the fact
# that makes a small local model viable for it at all.
#
# ONE PATCH, AND IT IS INERT WITHOUT THE ENV VAR. The client is constructed as
# `new OpenAI({ apiKey })` with no baseURL, so it can only ever reach OpenAI.
# patches/ai-local-model.patch adds `baseURL: process.env.OPENAI_BASE_URL ||
# undefined`, which falls back to api.openai.com exactly as before when unset.
say "4/5  ai harness"
AI_DIR="../gpt-play-pokemon-firered"
if [[ -d "$AI_DIR/.git" ]]; then
  echo "     present  $AI_DIR"
else
  git clone --quiet --depth 1 \
    https://github.com/Clad3815/gpt-play-pokemon-firered.git "$AI_DIR" \
    && echo "     cloned   $AI_DIR" || echo "     clone FAILED — --ai will not work" >&2
fi
if [[ -d "$AI_DIR/.git" ]]; then
  if grep -q "OPENAI_BASE_URL" "$AI_DIR/server/src/core/openaiClient.js" 2>/dev/null; then
    echo "     patched  local-model endpoint already applied"
  elif git -C "$AI_DIR" apply "$PWD/patches/ai-local-model.patch" 2>/dev/null; then
    echo "     patched  local-model endpoint"
  else
    echo "     patch did not apply — see patches/ai-local-model.patch" >&2
  fi
fi

# ---- 5/5 the model proxy ------------------------------------------------
#
# Nothing here is installed by this script: LiteLLM lives on roverbyteseer, and
# Tailscale needs a browser login against an account this script cannot have.
# What it CAN do is say which of the three steps is missing, in order, so a new
# machine does not have to remember any of it. See ai/litellm/README.md.
say "5/5  model proxy"
TS_APP="/Applications/Tailscale.app/Contents/MacOS/Tailscale"
if [[ -x "$TS_APP" ]]; then
  # The CLI is inside the bundle, not on PATH -- `command -v tailscale` finds
  # nothing on a machine that has it, which is confusing enough to say once.
  if "$TS_APP" status >/dev/null 2>&1; then
    echo "     tailscale  up ($("$TS_APP" status --json 2>/dev/null | grep -o '"DNSName":"[^"]*"' | head -1 | cut -d'"' -f4))"
  else
    echo "     tailscale  installed but LOGGED OUT — run: $TS_APP up" >&2
  fi
else
  echo "     tailscale  MISSING — brew install --cask tailscale, then: $TS_APP up" >&2
fi

LLM_HOST=""
for h in roverbyteseer roverbyteseer.local 10.0.0.136; do
  if curl -fsS --max-time 3 "http://$h:4000/health/liveliness" >/dev/null 2>&1; then
    LLM_HOST="$h"; break
  fi
done
if [[ -n "$LLM_HOST" ]]; then
  echo "     litellm    up at http://$LLM_HOST:4000"
  if ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 "roverbyte@$LLM_HOST" \
       'test -f ~/.litellm.env' 2>/dev/null; then
    echo "     key        readable over ssh (never copied into this repo)"
  else
    echo "     key        NOT readable — run: ssh-copy-id roverbyte@$LLM_HOST" >&2
  fi
else
  echo "     litellm    unreachable on :4000 — only needed for ./bindDaemons.sh --ai" >&2
fi

say "ready"
cat <<'EOS'
     ./bindDaemons.sh              CONTENT on GBA
     ./bindDaemons.sh --classic    CONTENT on Game Boy (this is where the slice is)
     make content                  classic build only
     ./bindDaemons.sh --ai         CONTENT on GBA, played by a model
     make vanilla-check            prove the classic toolchain
EOS

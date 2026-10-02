#!/usr/bin/env bash
# Open the theatre's emulator (engine.md section 5, step 1) without touching the user's.
#
#   tools/theatre_start.sh                  CONTENT's debug ROM, as a scratch copy, in a NEW mGBA
#   tools/theatre_start.sh context          CONTEXT's
#   tools/theatre_start.sh --fresh          ...and delete the scratch save first (a new game)
#   tools/theatre_start.sh --alongside      open it even though the user has an mGBA running
#   tools/theatre_start.sh --dry-run        say what it would do, and do nothing
#
# WHY THIS EXISTS (engine.md trap 40). `open -a mGBA <rom>` with mGBA already running does not start
# a second emulator: macOS hands the ROM to the running one, and it replaces whatever game the user
# had open in that window. On 2026-10-02 a session did exactly that. No save file changed, but any
# play since the user's last in-game save would have been gone, and nothing said so.
#
# So this refuses when any mGBA is running that it did not start, and asks first if it is run from a
# terminal. Otherwise it opens with `open -n` -- always a separate instance -- and passes the ROM as
# an ARGUMENT rather than a document, so the theatre's instance carries `.theatre/` in its command
# line and can be told from the user's (`pgrep -fl mGBA`).
#
# The ROM is a copy under .theatre/rom/ (gitignored): mGBA keeps its save beside the ROM, so the copy
# gets a save of its own and the user's daemonsContent*.sav is never opened. The save survives
# between runs -- the rebuilt ROM is copied over the same file, as section 5 drives it -- until --fresh.
#
# It cannot load the script for you. mGBA's Qt menus appear only while it is the FRONTMOST app, so
# Tools > Scripting... needs it brought forward by its pid (printed below) -- never `open -a mGBA` or
# `osascript ... activate`, which may raise the user's instance instead.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
edition=content fresh=0 alongside=0 dry=0
for a in "$@"; do
  case "$a" in
    content|context) edition="$a" ;;
    --fresh)         fresh=1 ;;
    --alongside)     alongside=1 ;;
    --dry-run)       dry=1 ;;
    -h|--help)       sed -n '2,26p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "theatre_start: unknown argument '$a' (try --help)" >&2; exit 64 ;;
  esac
done

if [[ $edition == content ]]; then name=daemonsContent_debug target=firered_debug
else                            name=daemonsContext_debug target=leafgreen_debug; fi
ROM="$ROOT/engineGba/$name.gba"
SCRATCH="$ROOT/.theatre/rom"
COPY="$SCRATCH/theatre_$edition.gba"

if [[ ! -e "$ROOT/engineGba" ]]; then
  echo "theatre_start: no engineGba/ here -- a worktree has no engine symlinks (CLAUDE.md, Worktrees)." >&2
  exit 1
fi
if [[ ! -f "$ROM" ]]; then
  echo "theatre_start: $ROM is not built:  make -C engineGba $target -j8" >&2
  exit 1
fi

# -- who is already running ------------------------------------------------------------------------
# Every mGBA, split into ours (its command line names .theatre/) and everyone else's -- the user's.
ours=() theirs=()
while read -r pid cmd; do
  [[ -z "$pid" ]] && continue
  if [[ "$cmd" == *"/.theatre/"* ]]; then ours+=("$pid"); else theirs+=("$pid"); fi
done < <(pgrep -x mGBA | while read -r p; do echo "$p $(ps -o command= -p "$p" 2>/dev/null)"; done)

if (( ${#ours[@]} )); then
  echo "theatre_start: the theatre's mGBA is already running (pid ${ours[*]})."
  echo "  Rebuilt ROM? Copy it over and reload in THAT window -- the script survives a reload:"
  echo "    cp \"$ROM\" \"$COPY\""
  exit 0
fi

if (( ${#theirs[@]} )) && (( !alongside )); then
  echo "theatre_start: mGBA is already running (pid ${theirs[*]}) and it is not the theatre's." >&2
  echo "  That is the user's emulator. \`open -a mGBA <rom>\` would load the scratch ROM INTO it and" >&2
  echo "  lose whatever they were playing (engine.md trap 40). This opens a separate instance, which" >&2
  echo "  is safe, but a second mGBA on their screen is still theirs to agree to." >&2
  if [[ -t 0 && -t 1 ]]; then
    read -r -p "  Open a separate theatre instance beside it? [y/N] " yn
    [[ "$yn" == [yY]* ]] || { echo "  Not opened."; exit 2; }
  else
    echo "  Ask the user, then run again with --alongside -- or ask them to quit theirs." >&2
    exit 2
  fi
fi

# -- open ------------------------------------------------------------------------------------------
if (( dry )); then
  echo "theatre_start (dry run): would copy $ROM"
  echo "                          to $COPY$( (( fresh )) && echo ', deleting its save first')"
  echo "                          and run: open -n -a mGBA --args \"$COPY\""
  exit 0
fi

mkdir -p "$SCRATCH"
(( fresh )) && rm -f "${COPY%.gba}.sav"
cp -f "$ROM" "$COPY"
open -n -a mGBA --args "$COPY"

pid=""
for _ in $(seq 1 50); do
  pid=$(pgrep -f "mGBA.app/Contents/MacOS/mGBA $COPY" | head -1 || true)
  [[ -n "$pid" ]] && break
  sleep 0.1
done

echo "theatre_start: opened $(basename "$COPY") in a new mGBA${pid:+ (pid $pid)}."
echo "  Now, with THAT window frontmost (its menus are not there otherwise): Tools > Scripting..., and in"
echo "  its input line:"
echo "    dofile(\"$ROOT/tools/theatre.lua\")"
echo "  Then drive it with .theatre/run.sh (engine.md section 5)."

#!/usr/bin/env python3
"""EASY CHAT keeps a second copy of the vocabulary. Bring it into line.

    python3 tools/port_easychat.py [--write]

T-15. `src/data/easy_chat/` is twenty-four files and it had never been touched
by a naming pass, so `ABILITY_CACOPHONY` was `NO CHANNEL` in `abilities.h` and
still `MAGNET PULL` here. port_vocab is fenced out of the directory on purpose
-- a rename learned from one table landing inside a word from another turned
`MAGNET PULL` into `SIGNAL GAIN PULL` -- so this is the pass that does it
properly.

The scope is smaller than the directory suggests, and that is the finding:
easy chat stores SPECIES and MOVES as constants, so those already read as ours
through gSpeciesNames and gMoveNames. Only the ABILITY names are duplicated as
strings, and only in easy_chat_group_status.h.

DERIVED, not listed: the map is abilities.h diffed against upstream, so a
future ability rename travels here by re-running this rather than by anyone
remembering that this file exists.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
PATH = os.path.join(GBA, "src/data/easy_chat/easy_chat_group_status.h")


def upstream(rel):
    r = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def main():
    rel = "src/data/text/abilities.h"
    pat = r'\[ABILITY_(\w+)\] = _\("([^"]*)"\)'
    was = dict(re.findall(pat, upstream(rel)))
    now = dict(re.findall(pat, open(os.path.join(GBA, rel), encoding="utf-8").read()))
    renames = {was[k]: now[k] for k in was if k in now and was[k] != now[k]}
    print("  %d ability renames learned from abilities.h" % len(renames))

    raw = open(PATH, encoding="utf-8").read()
    hits, rc = 0, 0
    for m in list(re.finditer(r'(sEasyChatWord_\w+\[\] = _\(")([^"]*)("\))', raw)):
        old = m.group(2)
        if old not in renames:
            continue
        new = renames[old]
        #  Easy chat draws into a fixed grid and vanilla's widest word sets it.
        #  Every ability name is already inside ABILITY_NAME_LENGTH, so this is
        #  a guard rather than an expectation -- but an unguarded assumption is
        #  the thing this project keeps finding afterwards.
        if len(new) > max(len(w) for w in re.findall(r'_\("([^"]*)"\)', raw)):
            print("  !! %s is wider than anything easy chat ships" % new); rc = 1
            continue
        raw = raw.replace(m.group(0), m.group(1) + new + m.group(3), 1)
        hits += 1
    print("  %d of easy chat's own strings were a renamed ability" % hits)

    left = [w for w in re.findall(r'_\("([^"]*)"\)', raw) if w in renames]
    if left:
        print("  !! %d still vanilla: %s" % (len(left), ", ".join(left[:6]))); rc = 1

    if "--write" in sys.argv and rc == 0:
        open(PATH, "w", encoding="utf-8").write(raw)
        print("  written %s" % os.path.relpath(PATH, ROOT))
    elif rc == 0:
        print("  (report only; pass --write)")
    return rc


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Every name this fork has used and retired, and what now stands in its place (T-246).

    python3 tools/gbaretired.py            # report
    python3 tools/gbaretired.py --write     # write tools/retired_names.json

check_lexicon's stale-name pass learns {vanilla -> ours} by diffing against upstream, which sees two ends of a
rename and nothing in between. A name WE gave and later took back is invisible to it: TMs were PATCHES before they
were PLUGINS (T-245), MAROWAK was CAIRNLING before it was COREFILE, and every line written in between kept the
middle name. This walks the git history of each name table in engineGba/ and records every name a designator has
had, so the check can refuse the middle ones too.

Two kinds of retired name are kept apart, because only one of them can be swept:

  * RETIRED -- no longer anybody's name. A line that says it is wrong, and check_lexicon says so.
  * MOVED   -- now somebody ELSE's name (PORYGON was SENTINEL; SENTINEL is MAGNEMITE now). A line that says it
              might mean either, so no check can decide; they are listed for a person to read, and the Game
              Corner and the Trainer Tower, where the designator sits beside the name, are checked directly.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(ROOT, "tools/retired_names.json")
WRITE = "--write" in sys.argv

#  Retired as a NAME, still used as a word on purpose. Each says why.
STILL_PROSE = {
    "TEAM CORPUS": "the organisation; CORPUS STAFF is only its trainer class",
    "CLARIFIER": "the module's full name on the R-and-D requisition sign (CC-7 COGNITIVE CLARIFIER MODULE)",
}

TABLES = [
    ("src/data/text/move_names.h", r'\[(MOVE_\w+)\]\s*=\s*_\("([^"]+)"\)', False),
    ("src/data/text/species_names.h", r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]+)"\)', False),
    ("src/data/text/abilities.h", r'\[(ABILITY_\w+)\]\s*=\s*_\("([^"]+)"\)', False),
    ("src/data/text/trainer_class_names.h", r'\[(TRAINER_CLASS_\w+)\]\s*=\s*_\("([^"]+)"\)', False),
    ("src/data/items.json", r'"english":\s*"([^"]+)",\s*\n\s*"itemId":\s*"(ITEM_\w+)"', True),
    #  T-247: places and types were renamed more than once too, and were not read here.
    ("src/data/region_map/region_map_sections.json", r'"id":\s*"(MAPSEC_\w+)",[^}]*?"name":\s*"([^"]+)"', False),
    ("src/battle_main.c", r'\[(TYPE_\w+)\]\s*=\s*_\("(\w+)"\)', False),
]


def git(*args):
    return subprocess.run(["git", "-C", GBA] + list(args), capture_output=True, text=True).stdout


def pairs(text, pat, swapped):
    return [(b, a) if swapped else (a, b) for a, b in re.findall(pat, text)]


def main():
    upstream = set(git("rev-list", "upstream/master").split())
    history, current, vanilla = {}, {}, set()
    for path, pat, swapped in TABLES:
        for rev in git("log", "--format=%H", "--", path).split():
            if rev in upstream:
                continue                     # vanilla's own history is the diff's business, not ours
            for key, name in pairs(git("show", "%s:%s" % (rev, path)), pat, swapped):
                history.setdefault(name, set()).add(key)
        for key, name in pairs(open(os.path.join(GBA, path), encoding="utf-8").read(), pat, swapped):
            current[key] = name
        vanilla |= {n for _, n in pairs(git("show", "upstream/master:" + path), pat, swapped)}
    owners = {}
    for key, name in current.items():
        owners.setdefault(name, set()).add(key)
    retired, moved = {}, {}
    for name, keys in sorted(history.items()):
        if name in vanilla or name in STILL_PROSE or len(name) < 4 or re.search(r"[a-z]", name):
            continue
        was = sorted(k for k in keys if current.get(k) != name)
        if not was:
            continue
        if name in owners:
            moved[name] = {"was": was, "now": sorted(owners[name])}
        elif len({current.get(k) for k in was}) == 1 and current.get(was[0]):
            retired[name] = current[was[0]]
    out = {"retired": retired, "moved": moved}
    text = json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    have = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    print("  %d retired names, %d moved to something else" % (len(retired), len(moved)))
    if text != have:
        print("  tools/retired_names.json %s" % ("written" if WRITE else "is out of date -- run with --write"))
        if WRITE:
            open(OUT, "w", encoding="utf-8").write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

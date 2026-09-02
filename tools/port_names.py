#!/usr/bin/env python3
"""Carry a renamed name table from the Game Boy build into the GBA build.

    python3 tools/port_names.py            # report only
    python3 tools/port_names.py --write

The two engines store the same table completely differently -- `dname "PING"`
in index order on one side, `[SPECIES_SPEAROW] = _("PING")` keyed by constant
on the other -- but the RENAME is the same fact in both. So this does not try
to map index to constant. It diffs our table against upstream's to learn
{vanilla name -> our name}, then substitutes on the vanilla string, which is
exact and needs no arithmetic.

Only names we actually changed are touched. Everything still vanilla stays
vanilla, so a half-ported table is obvious rather than silently mixed.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

# Some renames have nowhere to land, and that is a FACT ABOUT THE PORT rather
# than a bug. In Gen 3 badges are not items at all -- `items.h` contains the
# string BADGE zero times -- so the eight MARKS have no item slot to be renamed
# into. They live as flags and a Trainer Card display. Listing them here keeps
# them from being reported as failures every run without letting them be
# silently dropped: they are named, with the reason.
KNOWN_MISSING = {
    "src/data/items.json": (
        "badges are not items in Gen 3; the MARKS are flags plus a card",
        {"BOULDERBADGE", "CASCADEBADGE", "THUNDERBADGE", "RAINBOWBADGE",
         "SOULBADGE", "MARSHBADGE", "VOLCANOBADGE", "EARTHBADGE"},
    ),
}

TABLES = [
    # gb source, gb macro, gba file, name limit, format
    ("data/pokemon/names.asm", "dname", "src/data/text/species_names.h", 10, "c"),
    ("data/items/names.asm",   "li",    "src/data/items.json",           14, "json"),
]

def gb_list(path, macro):
    return [m.group(1) for m in
            re.finditer(r'%s\s+"([^"]*)"' % macro, open(os.path.join(GB, path)).read())]

def upstream_list(path, macro):
    txt = subprocess.run(["git", "-C", GB, "show", "upstream/master:" + path],
                         capture_output=True, text=True).stdout
    return [m.group(1) for m in re.finditer(r'%s\s+"([^"]*)"' % macro, txt)]

rc = 0
for src, macro, dst, limit, fmt in TABLES:
    ours, van = gb_list(src, macro), upstream_list(src, macro)
    if len(ours) != len(van):
        sys.exit("%s: %d entries here, %d upstream -- tables are out of step" % (src, len(ours), len(van)))
    renames = {v: o for v, o in zip(van, ours) if v != o}
    print("%s -> %s" % (src, dst))
    print("  %d renamed of %d" % (len(renames), len(ours)))

    too_long = {v: o for v, o in renames.items() if len(o) > limit}
    for v, o in sorted(too_long.items()):
        print("  !! %s is %d chars, limit is %d" % (o, len(o), limit)); rc = 1

    path = os.path.join(GBA, dst)
    text = open(path).read()
    reason, expected = KNOWN_MISSING.get(dst, ("", set()))
    done, missing, skipped = 0, [], []
    for v, o in sorted(renames.items()):
        if fmt == "c":
            pat, rep = r'(= _\(")%s("\),)' % re.escape(v), r'\g<1>%s\g<2>' % o
            already = '_("%s")' % o
        else:
            # The file stores non-ASCII escaped -- POKé is POK\\u00e9 on disk --
            # so match the way it is spelled there, not the way we read it. And
            # match case-insensitively: Gen 1 wrote OAK's PARCEL, Gen 3 writes
            # OAK'S PARCEL, and that is the same item.
            esc = json.dumps(v)[1:-1]
            pat = r'("english": ")%s(")' % re.escape(esc)
            rep = r'\g<1>%s\g<2>' % json.dumps(o)[1:-1]
            already = '"english": "%s"' % json.dumps(o)[1:-1]
        flags = re.IGNORECASE if fmt == "json" else 0
        text, n = re.subn(pat, rep, text, flags=flags)
        if n: done += n
        elif already in text: done += 1                # already ported
        elif v in expected: skipped.append(v)
        else: missing.append(v)
    if skipped:
        print("  %d with no slot -- %s:" % (len(skipped), reason))
        print("     " + " ".join(sorted(skipped)))
    for v in missing:
        print("  !! no slot found for vanilla name %s" % v); rc = 1
    print("  %d/%d placed" % (done, len(renames) - len(skipped)))
    if WRITE and not missing and not too_long:
        open(path, "w").write(text)
        print("  written")
sys.exit(rc)

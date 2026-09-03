#!/usr/bin/env python3
"""Carry our type assignments into the GBA build.

    python3 tools/port_types.py [--write]

This was missed, and it showed: ROVERCUB was reading GROWTH / CORRUPT on the
Index, because the GBA still had vanilla Bulbasaur's GRASS/POISON while the
Game Boy build has had it as single-type GRASS -- GROWTH -- all along. The
starter you are handed in the first five minutes was carrying the bias-and-
poisoning type, which is close to the opposite of what it is.

Renaming a type does not retype a species. Two different tables, and only one
of them had been ported.

Only species we actually retyped are touched; everything else keeps upstream's.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
DST = os.path.join(GBA, "src/data/pokemon/species_info.h")

# pokered writes the same table two ways; PSYCHIC carries a suffix because
# PSYCHIC collides with the move of that name.
def gb_to_gba(t):
    return "TYPE_" + (t[:-5] if t.endswith("_TYPE") else t)

def types_of(text):
    m = re.search(r'db\s+([A-Z_]+)\s*,\s*([A-Z_]+)\s*;\s*type', text)
    return (m.group(1), m.group(2)) if m else None

changed = subprocess.run(["git", "-C", GB, "diff", "--name-only", "upstream/master",
                          "--", "data/pokemon/base_stats/"],
                         capture_output=True, text=True).stdout.split()
FIX = {"nidoranf": "NIDORAN_F", "nidoranm": "NIDORAN_M",
       "farfetchd": "FARFETCHD", "mrmime": "MR_MIME"}

text = open(DST).read()
rc, placed = 0, 0
for path in sorted(changed):
    slug = os.path.basename(path)[:-4]
    ours = types_of(open(os.path.join(GB, path)).read())
    if not ours:
        print("  !! no type line in %s" % path); rc = 1; continue
    key = "SPECIES_" + FIX.get(slug, slug.upper())
    a, b = gb_to_gba(ours[0]), gb_to_gba(ours[1])
    pat = re.compile(r'(\[%s\]\s*=\s*\{.*?\.types = \{)[^}]*(\})' % re.escape(key), re.S)
    new, n = pat.subn(lambda m: m.group(1) + "%s, %s" % (a, b) + m.group(2), text, count=1)
    if not n:
        print("  !! no %s in species_info.h" % key); rc = 1; continue
    text = new; placed += 1
    print("  %-12s %s / %s" % (slug, a, b))
print("  %d/%d retyped" % (placed, len(changed)))
if WRITE and rc == 0:
    open(DST, "w").write(text)
    print("  written")
sys.exit(rc)

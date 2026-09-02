#!/usr/bin/env python3
"""Search a GBA ROM for a string, through the game's own charmap.

    python3 tools/gbastr.py CONTENT CONTEXT EMERGENT

Gen 3 encodes text with charmap.txt exactly as Gen 1 does, so grepping a .gba
for ASCII finds nothing and proves nothing. The Game Boy side learned this the
hard way -- a stale intermediate shipped vanilla sprites through four ROMs
while every other check passed. Compiling is not evidence. This is the GBA
equivalent of decoding with the charmap: it encodes the string the way the
build does, then looks for those exact bytes.
"""
import sys, os, re

ENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engineGba")
CMAP = {}
for ln in open(os.path.join(ENG, "charmap.txt"), encoding="utf-8"):
    m = re.match(r"'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*$", ln)
    if m:
        CMAP.setdefault(m.group(1), int(m.group(2), 16))

def encode(s):
    try:
        return bytes(CMAP[c] for c in s)
    except KeyError as e:
        sys.exit("no charmap entry for %s" % e)

roms = [f for f in sorted(os.listdir(ENG)) if f.endswith(".gba")]
words = sys.argv[1:] or sys.exit(__doc__)
for rom in roms:
    data = open(os.path.join(ENG, rom), "rb").read()
    hits = ["%s:%s" % (w, "yes" if encode(w) in data else "NO") for w in words]
    print("  %-26s %s" % (rom, "  ".join(hits)))

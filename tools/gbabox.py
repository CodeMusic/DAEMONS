#!/usr/bin/env python3
"""Replace the Index's caught marker with a box.

    python3 tools/gbabox.py [--write]

The Index marks a bound daemon with a POKé BALL, which is the one place the
old noun survives as a PICTURE rather than a word. 3.1's acquisition line is
USERBOX -> ADMINBOX -> SUPERBOX -> ROOTBOX, so the mark should be a box.

Drawn in the marker's own palette rather than a new one: 6 is the dark edge,
3 the light face, 7 the band across it. The red and orange the ball used (14
and 15) go unused, which is invariant 5 doing its job by itself -- nothing in
the Index is coloured for decoration.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(ROOT, "engineGba/graphics/pokedex/caught_marker.png")
WRITE = "--write" in sys.argv

# 0 transparent, 6 edge, 3 face, 7 band -- a crate, banded twice
BOX = [
    "06666660",
    "63333336",
    "63777736",
    "63333336",
    "63333336",
    "63777736",
    "63333336",
    "06666660",
]

im = Image.open(PNG)
if im.size != (8, 8):
    sys.exit("  !! caught marker is %dx%d, expected 8x8" % im.size)
px = im.load()
before = sorted({px[x, y] for x in range(8) for y in range(8)})
for y, row in enumerate(BOX):
    for x, c in enumerate(row):
        px[x, y] = int(c, 16)
after = sorted({px[x, y] for x in range(8) for y in range(8)})
print("  palette before %s" % before)
print("  palette after  %s   (14 and 15 were the ball's red and orange)" % after)
if WRITE:
    im.save(PNG)
    print("  written: %s" % os.path.relpath(PNG, ROOT))

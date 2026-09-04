#!/usr/bin/env python3
"""Carry the eight MARKS onto the GBA trainer card.

    python3 tools/gbamarks.py [--write]

The Game Boy sheet is sixteen 16x16 cells: each MARK twice, once light and once
dark. The dark one is the art -- library, gradient descent, waveform, scatter
and fit, simplex, frame, thermometer, funnel -- and together they are a
toolkit, which is what 7.14 asked for.

Gen 3 stores its eight badges as one 128x16 strip, 4bpp, sharing a palette that
already carries a grey ramp: 1 white, 2/3/4 progressively darker, 15 black,
and 0 transparent. So invariant 5 costs nothing here -- greyscale IS the
palette, and the port is a straight remap of four Game Boy shades onto it.

The one judgement is WHICH WHITE. White inside a glyph is part of the drawing;
white outside it is the card showing through. Flood-filling from the border
tells them apart, which a per-pixel map cannot.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB  = os.path.join(ROOT, "engine/gfx/trainer_card/badges.png")
GBA = os.path.join(ROOT, "engineGba/graphics/trainer_card/badges.png")
WRITE = "--write" in sys.argv

# Game Boy shade -> Gen 3 palette index, on the ramp the badge palette already has
SHADE = {255: 1, 170: 3, 85: 4, 0: 15}
TRANSPARENT = 0
MARKS = ["SLATE", "SLOPE", "SENSE", "FIT", "SKEW", "FRAME", "HEAT", "TRUE"]

gb = Image.open(GB).convert("L")
dst = Image.open(GBA)
if dst.size != (128, 16):
    sys.exit("  !! GBA badge strip is %dx%d, expected 128x16" % dst.size)

out = dst.copy()
op = out.load()
for i, name in enumerate(MARKS):
    cell = gb.crop((0, (i * 2 + 1) * 16, 16, (i * 2 + 1) * 16 + 16))   # the dark one
    src = cell.load()
    # outside is whatever white the border reaches; anything else white is drawn
    outside, edge = set(), [(x, y) for x in range(16) for y in (0, 15)] + \
                          [(x, y) for y in range(16) for x in (0, 15)]
    while edge:
        x, y = edge.pop()
        if (x, y) in outside or not (0 <= x < 16 and 0 <= y < 16) or src[x, y] != 255:
            continue
        outside.add((x, y))
        edge += [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    shades = set()
    for y in range(16):
        for x in range(16):
            v = src[x, y]
            shades.add(v)
            op[i * 16 + x, y] = TRANSPARENT if (x, y) in outside else SHADE.get(v, 15)
    print("  %-6s MARK  shades %-18s %d px transparent"
          % (name, sorted(shades), len(outside)))

if WRITE:
    out.save(GBA)
    print("  written: %s" % os.path.relpath(GBA, ROOT))

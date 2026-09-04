#!/usr/bin/env python3
"""Turn the PP glyph into MP.

    python3 tools/gbamana.py [--write]

`{PP}` is not two letters -- it is ONE compressed glyph, `F9 06`, which the
text engine resolves to cell 0x106 of the same latin font sheet. The summary
screen draws it at x=36 and the move's PP number at x=46, so the whole label
lives in TEN PIXELS. "MANA" is twenty-four and would run straight over the
number, in hard-coded offsets.

MP is the same two characters, so every literal -- "PP ", "PP was restored.",
the items PP UP and PP MAX -- changes width by nothing. Only the glyph has to
be drawn, and only its left half: the right half is already a P.

The font's own M is six pixels wide where this glyph allows five, so the M
here is the FOUR-pixel one from `latin_small`, which was designed for exactly
this width. Shadow is generated the way the sheet does it, one down and right.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "engineGba/graphics/fonts")
WRITE = "--write" in sys.argv
GLYPH = 0x106
INK, SHADOW, BG = 1, 2, 3

# latin_small's M: four wide, seven tall, and unmistakably an M at this size
M = ["#..#", "####", "#..#", "#..#", "#..#", "#..#", "#..#"]

SHEETS = [("latin_normal", 16, 16), ("latin_male", 16, 16),
          ("latin_female", 16, 16), ("latin_small", 8, 16)]

rc = 0
for name, cw, ch in SHEETS:
    path = os.path.join(FONTS, name + ".png")
    im = Image.open(path)
    px = im.load()
    cols = im.width // cw
    r, c = divmod(GLYPH, cols)
    x0, y0 = c * cw, r * ch
    ink = [(x, y) for y in range(ch) for x in range(cw) if px[x0 + x, y0 + y] == INK]
    if not ink:
        print("  !! %s: cell 0x%X has no ink" % (name, GLYPH)); rc = 1; continue
    left = min(x for x, _ in ink)
    top = min(y for _, y in ink)
    width = max(x for x, _ in ink) - left + 1
    half = width // 2                      # the glyph is P then P
    if half < len(M[0]):
        # latin_small packs each P into three pixels and an M is not an M at
        # three. It is never drawn there -- {PP} appears once, in FONT_NORMAL --
        # so declining is better than shipping a glyph that collides.
        print("  %-14s half is %d px; the M needs %d. Left alone (unused here)."
              % (name, half, len(M[0])))
        continue
    # clear the left half back to the sheet's own background, then draw the M
    for y in range(top - 1, top + len(M) + 2):
        for x in range(left, left + half):
            if 0 <= y < ch:
                px[x0 + x, y0 + y] = BG
    for dy, row in enumerate(M):
        for dx, ch_ in enumerate(row):
            if ch_ != "#":
                continue
            px[x0 + left + dx, y0 + top + dy] = INK
            sx, sy = left + dx + 1, top + dy + 1
            if sx < left + half and sy < ch and px[x0 + sx, y0 + sy] != INK:
                px[x0 + sx, y0 + sy] = SHADOW
    print("  %-14s glyph at (%3d,%3d)  ink %2dpx wide, half %d" % (name, x0, y0, width, half))
    if WRITE:
        im.save(path)
if WRITE and rc == 0:
    print("  written: 4 sheets")
sys.exit(rc)

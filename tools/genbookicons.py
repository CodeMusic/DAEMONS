#!/usr/bin/env python3
"""The TEXTBOOK's chapter marks (T-223): each floor's board, shrunk to a 16x16 slate.

    python3 tools/genbookicons.py            # report
    python3 tools/genbookicons.py --write    # engineGba/graphics/book/chapter_icons.png

A chapter in the TEXTBOOK is a floor of CALLOW SCHOOL, and every floor's board already carries its subject
in chalk (gbainterior.py, school_board_motif): the table, a ring with a dot in it, lines that fade with age,
three drawers and one thing across two, a worn link, a balance that is not level, a line struck through. So the
book draws the same seven marks, and a player who has stood in the room recognises the chapter before reading
its name. One mark per floor, stacked 16x16 top to bottom, floor 1 first.

The PNG is indexed and the INDICES are the contract, not the colours: book_reader.c loads its own palette and
reads these as 11 frame, 12 slate, 13 chalk, 14 faint chalk, 0 nothing. The build turns it into .4bpp.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "engineGba", "graphics", "book", "chapter_icons.png")
WRITE = "--write" in sys.argv

FRAME, SLATE, CHALK, FAINT = 11, 12, 13, 14


def slate():
    g = [[0] * 16 for _ in range(16)]
    for y in range(2, 14):
        for x in range(1, 15):
            g[y][x] = FRAME if y in (2, 13) or x in (1, 14) else SLATE
    return g


def px(g, x, y, c):
    if 2 <= x <= 13 and 3 <= y <= 12:
        g[y][x] = c


def mark(floor):
    g = slate()
    if floor == 1:                                   # LANGUAGE: the table, a lattice of equal cells
        for x in (4, 7, 10):
            for y in range(4, 12):
                px(g, x, y, FAINT)
        for y in (6, 9):
            for x in range(3, 13):
                px(g, x, y, CHALK)
    elif floor == 2:                                 # ATTENTION: one ring, a dot in it, marks nobody looked at
        for (x, y) in ((6, 5), (7, 5), (8, 5), (9, 5), (5, 6), (10, 6), (5, 7), (10, 7),
                       (5, 8), (10, 8), (6, 9), (7, 9), (8, 9), (9, 9)):
            px(g, x, y, CHALK)
        px(g, 7, 7, CHALK); px(g, 8, 7, CHALK)
        for (x, y) in ((3, 4), (12, 10), (3, 11), (12, 4)):
            px(g, x, y, FAINT)
    elif floor == 3:                                 # MEMORY: lines of writing, fainter the older they are
        for k, (c, end) in enumerate(((FAINT, 9), (FAINT, 11), (CHALK, 10), (CHALK, 12))):
            y = 4 + k * 2
            for x in range(3, end + 1):
                if (x + k) % 4 != 0:
                    px(g, x, y, c)
    elif floor == 4:                                 # CATEGORIES: three drawers, and one thing across two
        for bx in (3, 7, 11):
            for y in range(5, 11):
                px(g, bx - 1, y, FAINT); px(g, bx + 1, y, FAINT)
            px(g, bx, 5, FAINT); px(g, bx, 10, FAINT)
        px(g, 11, 8, CHALK)
        for x in range(3, 8):                        # the one that will not stay in a drawer
            px(g, x, 7, CHALK)
    elif floor == 5:                                 # LEARNING: nodes, faint links, one link worn heavy
        nodes = ((3, 5), (3, 10), (8, 4), (8, 11), (12, 7))
        for (x, y) in ((4, 6), (5, 8), (6, 9), (5, 5), (6, 5), (9, 5), (10, 10), (11, 9)):
            px(g, x, y, FAINT)
        for t in range(0, 6):                        # the one that has been used a great deal
            px(g, 4 + t, 10 - (t * 3) // 5 + 0, CHALK)
        for (x, y) in nodes:
            px(g, x, y, CHALK)
    elif floor == 6:                                 # BIAS: a balance that is not level
        for y in range(6, 12):
            px(g, 8, y, CHALK)
        for x in range(6, 11):
            px(g, x, 11, CHALK)
        for t in range(0, 10):
            px(g, 3 + t, 4 + t // 3, CHALK)
        px(g, 3, 5, FAINT); px(g, 4, 5, FAINT); px(g, 12, 8, FAINT); px(g, 11, 8, FAINT)
    elif floor == 7:                                 # ERROR: a line struck through, and the right one under it
        for x in range(3, 12):
            if x % 3:
                px(g, x, 5, FAINT)
        for x in range(3, 12):
            px(g, x, 6, FAINT)
        for x in range(3, 10):
            if x % 3:
                px(g, x, 9, CHALK)
        px(g, 10, 10, CHALK); px(g, 11, 9, CHALK); px(g, 12, 8, CHALK)
    return g


def main():
    img = Image.new("P", (16, 16 * 7), 0)
    pal = [0] * 48
    for i, c in {11: (150, 110, 60), 12: (36, 52, 44), 13: (232, 230, 220), 14: (130, 140, 132)}.items():
        pal[i * 3:i * 3 + 3] = c
    img.putpalette(pal + [0] * (768 - 48))
    for f in range(1, 8):
        g = mark(f)
        for y in range(16):
            for x in range(16):
                img.putpixel((x, (f - 1) * 16 + y), g[y][x])
    if not WRITE:
        print("  would write %s (7 marks, 16x112)" % os.path.relpath(OUT, ROOT))
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT)
    print("  wrote %s" % os.path.relpath(OUT, ROOT))
    return 0


sys.exit(main())

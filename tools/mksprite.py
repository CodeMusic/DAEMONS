#!/usr/bin/env python3
"""Crop a generated sprite to its subject, square it, and write a Game Boy PNG.

    python3 tools/mksprite.py gfx/front/artsai.png engine/gfx/pokemon/front/mew.png 40

Generated art arrives wide with the creature floating in white. Gen 1 sprites
are square (5x5, 6x6 or 7x7 tiles), so a straight resize squashes the subject.
This finds the ink, squares the box around it, adds a small margin and only
then resamples -- which is the difference between a rabbit and a wide rabbit.

Output is 2-bit greyscale, four levels, background at level 3, matching what
pret's own front sprites are. rgbgfx inverts on the way in, so level 3 is the
lightest on screen. Check it in the game; do not assume.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import read_png, resample, write_png

def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    src, dst, size = sys.argv[1], sys.argv[2], int(sys.argv[3])
    w, h, lum = read_png(src)

    # Ink is anything meaningfully darker than the paper.
    INK = 235
    xs = [x for y in range(h) for x in range(w) if lum(x, y) < INK]
    ys = [y for y in range(h) for x in range(w) if lum(x, y) < INK]
    if not xs:
        sys.exit("no ink found -- is the background white?")
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    print("  ink box %dx%d at (%d,%d) in a %dx%d image" % (bw, bh, x0, y0, w, h))

    # Square it about the subject's centre, then breathe.
    side = int(max(bw, bh) * 1.08)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    sx, sy = cx - side // 2, cy - side // 2

    def padded(x, y):
        # Outside the source is paper, not black.
        if 0 <= x < w and 0 <= y < h:
            return lum(x, y)
        return 255

    grid = resample(side, side, lambda x, y: padded(sx + x, sy + y), size, size)

    # Even thresholds waste a shade. Generated art puts the paper and the
    # creature's lightest fur in the same bucket, and the mid greys land on one
    # level, so a four-tone sprite comes out with three tones and a hole in it.
    # So: hold the paper at 3, then spread whatever ink remains across 0-2 by
    # its own range. Vanilla Mew uses all four; so should we.
    PAPER = 238
    ink = [v for row in grid for v in row if v < PAPER]
    lo, hi = (min(ink), max(ink)) if ink else (0, 255)
    span = max(1, hi - lo)
    q = [[3 if v >= PAPER else min(2, 3 * (v - lo) // span) for v in row]
         for row in grid]

    # Box-averaging dissolves a one-pixel black outline into mid grey. Vanilla
    # Mew is 207 pixels of level 0 against a 1144-pixel ground; a straight
    # average of this art gave 13. So the outline is carried separately: if a
    # genuinely black source pixel falls in an output cell, that cell is black.
    # Darkest-wins, the way a hand pixel artist would do it -- and without it a
    # white creature has no edge against white paper at all.
    # ...but darkest-wins is only safe at gentle reductions. At 25:1 an output
    # cell holds 625 source pixels, and letting a single black one blacken the
    # cell bloats a one-pixel outline into a blob -- the first attempt gave 306
    # pixels of level 0 and an unreadable rabbit. So require the cell to be
    # meaningfully dark, not merely touched by dark.
    OUTLINE, COVER = 55, 0.34
    step = side / size
    for dy in range(size):
        for dx in range(size):
            x0i, x1i = int(dx*step), max(int(dx*step)+1, int((dx+1)*step))
            y0i, y1i = int(dy*step), max(int(dy*step)+1, int((dy+1)*step))
            dark = tot = 0
            for yy in range(y0i, y1i):
                for xx in range(x0i, x1i):
                    tot += 1
                    if padded(sx+xx, sy+yy) < OUTLINE: dark += 1
            if tot and dark >= tot * COVER:
                q[dy][dx] = 0

    write_png(dst, q, 2)

    from collections import Counter
    c = Counter(v for row in q for v in row)
    print("  wrote %s at %dx%d" % (dst, size, size))
    print("  levels: " + "  ".join("%d:%d" % (k, c[k]) for k in sorted(c)))
    if c[3] < size * size * 0.25:
        print("  !! background is only %d%% -- the subject may be cropped too tight."
              % (100 * c[3] // (size * size)))

main()

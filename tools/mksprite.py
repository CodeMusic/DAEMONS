#!/usr/bin/env python3
"""Crop a generated sprite to its subject, box it, and write a Game Boy PNG.

    python3 tools/mksprite.py in.png out.png 56          # square, a daemon slot
    python3 tools/mksprite.py in.png out.png 40x56       # the title figure

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
    src, dst, spec = sys.argv[1], sys.argv[2], sys.argv[3]
    # A daemon slot is square; the title figure is 40x56. "WxH" keeps the
    # subject's proportions instead of squashing a standing person into a box.
    if "x" in spec:
        size_w, size_h = (int(v) for v in spec.lower().split("x"))
    else:
        size_w = size_h = int(spec)
    size = size_w
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

    # Box it about the subject's centre at the target's aspect, then breathe.
    aspect = size_w / size_h
    side_h = int(max(bh, bw / aspect) * 1.08)
    side_w = int(round(side_h * aspect))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    sx, sy = cx - side_w // 2, cy - side_h // 2
    side = side_h

    def padded(x, y):
        # Outside the source is paper, not black.
        if 0 <= x < w and 0 <= y < h:
            return lum(x, y)
        return 255

    grid = resample(side_w, side_h, lambda x, y: padded(sx + x, sy + y),
                    size_w, size_h)

    # Even thresholds waste a shade. Generated art puts the paper and the
    # creature's lightest fur in the same bucket, and the mid greys land on one
    # level, so a four-tone sprite comes out with three tones and a hole in it.
    # So: hold the paper at 3, then spread whatever ink remains across 0-2 by
    # its own range. Vanilla Mew uses all four; so should we.
    PAPER = 238
    ink = sorted(v for row in grid for v in row if v < PAPER)
    if ink:
        # Spreading the ink linearly over its range assumes the tones are evenly
        # distributed, and bold-outlined art is not: SEEKMUSAI's thick black
        # lines drag so many averaged cells low that 25% of the sprite came out
        # level 0 and level 1 was used 19 times. Cut at the ink's own thirds
        # instead, so all four tones carry roughly equal weight whatever the art
        # happens to look like.
        c1, c2 = ink[len(ink)//3], ink[2*len(ink)//3]
    else:
        c1 = c2 = 0
    q = [[3 if v >= PAPER else (0 if v <= c1 else 1 if v <= c2 else 2) for v in row]
         for row in grid]

    # The outline threshold cannot be a constant, and it cannot be a percentile
    # either. ARTSAI's art is 2.8% true black, so a fixed 55 caught it exactly;
    # S.T.A.R.R.'s art has no black at all -- its outline is grey at 112-127 and
    # its fill grey at 144-175 -- so 55 never fired once and the body came out a
    # slab with no edge. A percentile then landed in the empty space below both.
    #
    # But line work is always a *separate cluster*, darker than the fill with a
    # gap after it. So find the widest empty stretch in the ink histogram and cut
    # there. ARTSAI's gap is 16-159 and S.T.A.R.R.'s is 128-143; both give the
    # right answer for the right reason.
    hist = [0]*256
    for y in range(0, side_h, 2):
        for x in range(0, side_w, 2):
            v = padded(sx+x, sy+y)
            if v < PAPER: hist[v] += 1
    ink_n = sum(hist)
    floor_n = max(1, ink_n // 400)          # ignore stray anti-aliasing
    # Start at the darkest ink there actually is. S.T.A.R.R.'s art has nothing
    # below 112, so searching from zero finds 111 bins of nothing and cuts
    # there -- a gap under the outline rather than the gap after it.
    first = next((v for v in range(256) if hist[v] > floor_n), 0)
    best = (0, 55)
    run = None
    for v in range(first+1, 256):
        if hist[v] <= floor_n:
            if run is None: run = v
        else:
            if run is not None and v-run > best[0]:
                best = (v-run, (run+v)//2)
            run = None
    OUTLINE, COVER = best[1], 0.34
    # ...and when the art simply has no line work to find -- a generator that
    # was asked for a black outline and returned a grey one -- the gap search
    # has nothing to lock onto. An explicit override beats a cleverer guess.
    for a in sys.argv[4:]:
        if a.startswith("--outline="): OUTLINE = int(a.split("=")[1])
        # Bold-outlined art needs a higher bar. A 10px line at 24:1 covers less
        # than half a cell, so 0.34 catches every cell the line merely grazes
        # and doubles its width -- SEEKMUSAI came out 25% black with level 1
        # used six times. Raise it and only cells sitting on the line go black.
        if a.startswith("--cover="): COVER = float(a.split("=")[1])
    print("  outline threshold %d (gap search said %d)" % (OUTLINE, best[1]))
    stepx, stepy = side_w / size_w, side_h / size_h
    for dy in range(size_h):
        for dx in range(size_w):
            x0i, x1i = int(dx*stepx), max(int(dx*stepx)+1, int((dx+1)*stepx))
            y0i, y1i = int(dy*stepy), max(int(dy*stepy)+1, int((dy+1)*stepy))
            dark = tot = 0
            for yy in range(y0i, y1i):
                for xx in range(x0i, x1i):
                    tot += 1
                    if padded(sx+xx, sy+yy) < OUTLINE: dark += 1
            if tot and dark >= tot * COVER:
                q[dy][dx] = 0

    if "--solid" in sys.argv:
        # OAM sprites make the LIGHTEST level transparent, so paper inside the
        # outline is a hole -- a white lab coat vanishes and leaves a ghost.
        #
        # The flood has to run on the SOURCE, not on the 40x56 result. At the
        # target size the outline is one pixel and full of gaps, so a flood
        # started there leaks straight into the coat and finds nothing. At
        # source resolution the outline is six to eight pixels thick and closed.
        from collections import deque
        PAPER_LV, BG = 3, 240
        outside = bytearray(w * h)
        todo = deque([(x, y) for x in range(w) for y in (0, h - 1)] +
                     [(x, y) for y in range(h) for x in (0, w - 1)])
        while todo:
            x, y = todo.popleft()
            if not (0 <= x < w and 0 <= y < h) or outside[y * w + x]: continue
            if lum(x, y) < BG: continue
            outside[y * w + x] = 1
            todo.extend(((x+1, y), (x-1, y), (x, y+1), (x, y-1)))
        lifted = 0
        for gy in range(size_h):
            for gx in range(size_w):
                if q[gy][gx] != PAPER_LV: continue
                px_ = sx + int((gx + 0.5) * stepx)
                py_ = sy + int((gy + 0.5) * stepy)
                if 0 <= px_ < w and 0 <= py_ < h and not outside[py_ * w + px_]:
                    q[gy][gx] = 2; lifted += 1
        print("  solid: %d interior paper pixels lifted off transparent" % lifted)

    write_png(dst, q, 2)

    from collections import Counter
    c = Counter(v for row in q for v in row)
    print("  wrote %s at %dx%d" % (dst, size_w, size_h))
    print("  levels: " + "  ".join("%d:%d" % (k, c[k]) for k in sorted(c)))
    if c[3] < size_w * size_h * 0.25:
        print("  !! background is only %d%% -- the subject may be cropped too tight."
              % (100 * c[3] // (size_w * size_h)))

main()

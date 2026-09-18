#!/usr/bin/env python3
"""T-131 batch 2: two things cleandraft.py does not take, fixed after it.

PREEMPT is desaturated (see desaturate). SECTOR's back was drawn inside a pale box (its border is ~(232,235,232)); cleandraft's fill stopped at the box, so the
box is filled out here from its own corner. And grass the model drew under HEAP and BACKBONE is scenery, not an accent:
saturated green pixels are cleared. Run after cleandraft.py, from the repo root."""
from PIL import Image

def unbox(path, seed=(1, 1), tol=14):
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    while px[seed][3] == 0:                     # the outermost ring is already clear: start on the box itself
        seed = (seed[0] + 1, seed[1] + 1)
    ref = px[seed][:3]; todo, seen = [seed], set()
    while todo:
        x, y = todo.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y))
        r, g, b, a = px[x, y]
        if a == 0 or max(abs(r - ref[0]), abs(g - ref[1]), abs(b - ref[2])) > tol:
            continue
        px[x, y] = (0, 0, 0, 0)
        todo += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    im.save(path)

def degrass(path):
    im = Image.open(path).convert("RGBA"); px = im.load(); n = 0
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a and g > r + 25 and g > b + 25:
                px[x, y] = (0, 0, 0, 0); n += 1
    im.save(path); return n

def desaturate(path):
    """PREEMPT's front came back painted blue and orange, not grey: gbasprite.py read the blue body as an accent too
    near LOGIC's hue and turned it red. Every pixel to its own luminance, so the type ramp colours the whole body."""
    im = Image.open(path).convert("RGBA"); px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a:
                l = (r * 299 + g * 587 + b * 114) // 1000
                px[x, y] = (l, l, l, a)
    im.save(path)

# PREEMPT is desaturated as a DRAFT, before cleandraft paints the streak markers -- so this runs first, with
# `fix.py grey`, and cleandraft.py then reads preempt_*_grey.png.
import sys
if sys.argv[1:] == ["grey"]:
    import shutil
    for v in ("front", "back"):
        shutil.copy("gfx/drafts/batch2/preempt_%s.png" % v, "gfx/drafts/batch2/preempt_%s_grey.png" % v)
        desaturate("gfx/drafts/batch2/preempt_%s_grey.png" % v)
    sys.exit()

unbox("gfx/drafts/batch2/clean/sector_back.png")
for f in ("heap_back", "backbone_front", "backbone_back", "heap_front"):
    print(f, degrass("gfx/drafts/batch2/clean/%s.png" % f), "green pixels cleared")

#!/usr/bin/env python3
"""T-131 batch 12: SLURP, DRAGNET, RESENTMENT and FOSSILNET are drawn in colour, and greying a DRAFT can make a pale part match the background,
so the fill took part of it. Here the coloured draft is cleaned first, and the CLEANED sprite is greyed afterwards,
every pixel but gbasprite.py's four streak markers. Run after cleandraft.py, from the repo root."""
import ast
from PIL import Image

tree = ast.parse(open("tools/gbasprite.py").read())
MARKS = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "STREAK_MARKERS" for t in n.targets))
MARKS = {tuple(m) for m in (MARKS.values() if isinstance(MARKS, dict) else MARKS)}

def grey_but_markers(path):
    im = Image.open(path).convert("RGBA"); px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a and (r, g, b) not in MARKS:
                l = (r * 299 + g * 587 + b * 114) // 1000
                px[x, y] = (l, l, l, a)
    im.save(path)

grey_but_markers("gfx/drafts/batch12/clean/slurp_front.png")
grey_but_markers("gfx/drafts/batch12/clean/slurp_back.png")
grey_but_markers("gfx/drafts/batch12/clean/dragnet_front.png")
grey_but_markers("gfx/drafts/batch12/clean/dragnet_back.png")
grey_but_markers("gfx/drafts/batch12/clean/resentment_front.png")
grey_but_markers("gfx/drafts/batch12/clean/resentment_back.png")
grey_but_markers("gfx/drafts/batch12/clean/fossilnet_front.png")
grey_but_markers("gfx/drafts/batch12/clean/fossilnet_back.png")

def unbox(path, seed=(1, 1), tol=14):
    """FERRY's front and TRACKER's back were drawn on a box the background fill stopped at (batch 5's tool)."""
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    while px[seed][3] == 0:
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

unbox("gfx/drafts/batch12/clean/ferry_front.png")
unbox("gfx/drafts/batch12/clean/tracker_back.png")

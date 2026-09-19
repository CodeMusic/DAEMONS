#!/usr/bin/env python3
"""T-131 batch 11: SHELL is drawn pink, and greying a DRAFT can make a pale part match the background,
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

grey_but_markers("gfx/drafts/batch11/clean/shell_front.png")
grey_but_markers("gfx/drafts/batch11/clean/shell_back.png")

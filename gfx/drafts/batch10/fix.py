#!/usr/bin/env python3
"""T-131 batch 10: MIME, HANDLER and JETSTREAM are drawn in colour (JETSTREAM's blue turned gold), and greying a DRAFT can make a pale part match the background,
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

grey_but_markers("gfx/drafts/batch10/clean/mime_front.png")
grey_but_markers("gfx/drafts/batch10/clean/mime_back.png")
grey_but_markers("gfx/drafts/batch10/clean/handler_front.png")
grey_but_markers("gfx/drafts/batch10/clean/handler_back.png")

def unshadow_below(path, y0, keep):
    """HANDLER stands on a shadow ellipse that meets its legs: below y0, everything outside the leg columns goes."""
    im = Image.open(path).convert("RGBA"); px = im.load()
    for y in range(y0, im.size[1]):
        for x in range(im.size[0]):
            if not (keep[0] <= x <= keep[1]):
                px[x, y] = (0, 0, 0, 0)
    im.save(path)

unshadow_below("gfx/drafts/batch10/clean/handler_front.png", 56, (28, 40))
unshadow_below("gfx/drafts/batch10/clean/handler_back.png", 57, (28, 39))
grey_but_markers("gfx/drafts/batch10/clean/jetstream_front.png")
grey_but_markers("gfx/drafts/batch10/clean/jetstream_back.png")

#!/usr/bin/env python3
"""T-131 batch 8: Five drafts are coloured (TARPIT, UPSTREAM, REAPER, BADSEED, ENSEMBLE), and greying a DRAFT can make a pale part match the background,
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

def unbg(path, ref=(58, 61, 62), tol=10):
    """REAPER's charcoal background, enclosed between its legs where the fill cannot reach: every pixel of that
    colour goes. Run on the coloured clean, before greying, while the body is still green and cannot match."""
    im = Image.open(path).convert("RGBA"); px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a and max(abs(r - ref[0]), abs(g - ref[1]), abs(b - ref[2])) <= tol:
                px[x, y] = (0, 0, 0, 0)
    im.save(path)

unbg("gfx/drafts/batch8/clean/reaper_front.png")
unbg("gfx/drafts/batch8/clean/reaper_back.png", ref=(72, 72, 72), tol=5)   # the back's draft had its own grey

def unground(path, y0=52, light=225):
    """A white ground strip under the feet: light pixels at the bottom of the frame."""
    im = Image.open(path).convert("RGBA"); px = im.load()
    for y in range(y0, im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a and min(r, g, b) >= light:
                px[x, y] = (0, 0, 0, 0)
    im.save(path)

unground("gfx/drafts/batch8/clean/reaper_front.png")
unground("gfx/drafts/batch8/clean/reaper_back.png")

grey_but_markers("gfx/drafts/batch8/clean/tarpit_front.png")
grey_but_markers("gfx/drafts/batch8/clean/tarpit_back.png")
grey_but_markers("gfx/drafts/batch8/clean/upstream_front.png")
grey_but_markers("gfx/drafts/batch8/clean/upstream_back.png")
grey_but_markers("gfx/drafts/batch8/clean/reaper_front.png")
grey_but_markers("gfx/drafts/batch8/clean/reaper_back.png")
grey_but_markers("gfx/drafts/batch8/clean/badseed_front.png")
grey_but_markers("gfx/drafts/batch8/clean/badseed_back.png")
grey_but_markers("gfx/drafts/batch8/clean/ensemble_front.png")
grey_but_markers("gfx/drafts/batch8/clean/ensemble_back.png")

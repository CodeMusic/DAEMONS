#!/usr/bin/env python3
"""T-166 second pass: every pick is greyed after cleaning,
all but the streak markers, since several were drawn in colour (the foxes orange, INSTINCT pink). Run after cleandraft.py."""
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

def unbox(path, seed=(1, 1), tol=14):
    """MULTICAST's views and IMPULSE's back were drawn on a box the background fill stopped at (batch 5's tool)."""
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


def unbg(path, ref, tol=14):
    """MULTICAST's dark box sits inside a pale strip the fill took, so it is not reached from any corner: every
    pixel of the box's colour goes. Safe here because the bat itself is pale."""
    im = Image.open(path).convert("RGBA"); px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a and max(abs(r - ref[0]), abs(g - ref[1]), abs(b - ref[2])) <= tol:
                px[x, y] = (0, 0, 0, 0)
    im.save(path)


def keep_largest(path):
    """What the box left -- the pale strips above and below it, and specks: everything but the largest shape goes."""
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size; seen = set(); comps = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and (x, y) not in seen:
                comp, todo = [], [(x, y)]
                while todo:
                    p = todo.pop()
                    if p in seen or not (0 <= p[0] < w and 0 <= p[1] < h) or not px[p][3]:
                        continue
                    seen.add(p); comp.append(p)
                    todo += [(p[0] + dx, p[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
                comps.append(comp)
    comps.sort(key=len)
    for c in comps[:-1]:
        for p in c:
            px[p] = (0, 0, 0, 0)
    im.save(path)

grey_but_markers("gfx/drafts/t166/clean2/chiller_back.png")
grey_but_markers("gfx/drafts/t166/clean2/ensemble_back.png")
grey_but_markers("gfx/drafts/t166/clean2/ferry_back.png")
grey_but_markers("gfx/drafts/t166/clean2/hauntproc_back.png")
grey_but_markers("gfx/drafts/t166/clean2/inference_back.png")
grey_but_markers("gfx/drafts/t166/clean2/ping_back.png")
grey_but_markers("gfx/drafts/t166/clean2/pipeline_back.png")
grey_but_markers("gfx/drafts/t166/clean2/ramrod_back.png")
grey_but_markers("gfx/drafts/t166/clean2/resentment_back.png")
grey_but_markers("gfx/drafts/t166/clean2/revenant_back.png")
grey_but_markers("gfx/drafts/t166/clean2/sentinel_back.png")
grey_but_markers("gfx/drafts/t166/clean2/smogstack_back.png")
grey_but_markers("gfx/drafts/t166/clean2/wisp_back.png")
grey_but_markers("gfx/drafts/t166/clean2/wildfire_back.png")
grey_but_markers("gfx/drafts/t166/clean2/whim_back.png")
grey_but_markers("gfx/drafts/t166/clean2/blindspot_back.png")
grey_but_markers("gfx/drafts/t166/clean2/seedling_back.png")
grey_but_markers("gfx/drafts/t166/clean2/spawn_back.png")
grey_but_markers("gfx/drafts/t166/clean2/fossilnet_back.png")
grey_but_markers("gfx/drafts/t166/clean2/grievance_back.png")

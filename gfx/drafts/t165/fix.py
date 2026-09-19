#!/usr/bin/env python3
"""T-165: PIXELBYTE's back and FORGE's front were drawn on a pale box the background fill stopped at. The box goes
first and the streaks are painted AFTER, on the fixed drawing -- cleaned once more from an 8x upscale on a flat ground, so
cleandraft.py places them on the body and never on the box. FORGE's front came in colour and is greyed last,
every pixel but the streak markers (batch 15's rule). Run from the repo root, after the first cleandraft.py pass."""
import ast, subprocess, sys
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



C = "gfx/drafts/t165/clean/"


def restreak(name, ground):
    """8x the fixed drawing onto flat blue and clean it again with --streaks: one art pixel per 8x8 block comes back.
    The ground is per drawing: PIXELBYTE's white head meets the edge of its outline, so a white ground floods into
    it; FORGE's thin pale horns read as the white edge line cleandraft.py strips beside a blue one"""
    im = Image.open(C + name + ".png").convert("RGBA")
    big = Image.new("RGBA", (512, 512), ground + (255,))
    big.alpha_composite(im.resize((512, 512), Image.NEAREST))
    tmp = "/tmp/t165_%s_8x.png" % name
    big.convert("RGB").save(tmp)
    out = subprocess.run(["python3", "tools/cleandraft.py", tmp, C + name + ".png", "--streaks"], capture_output=True, text=True)
    print(name, out.stdout.strip().splitlines()[-1] if out.stdout else out.stderr)


def unfloor(path, y0, dark=90):
    """FORGE stands on a pale floor ellipse around its hooves: from y0 down only the dark hooves stay"""
    im = Image.open(path).convert("RGBA"); px = im.load()
    for y in range(y0, im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a and (r * 299 + g * 587 + b * 114) // 1000 >= dark:
                px[x, y] = (0, 0, 0, 0)
    im.save(path)


def unbox_band(path, lo, hi):
    """flood from the border through pixels whose grey sits in [lo, hi): PIXELBYTE's box is 222-226 and its white
    head 240, so a band stops at the head where a tolerance around the seed (the box shades unevenly) did not"""
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    todo = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    seen = set()
    while todo:
        x, y = todo.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y))
        r, g, b, a = px[x, y]
        if a and not (lo <= (r * 299 + g * 587 + b * 114) // 1000 < hi):
            continue
        px[x, y] = (0, 0, 0, 0)
        todo += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    im.save(path)


unbox_band(C + "pixelbyte_back.png", 212, 234)
keep_largest(C + "pixelbyte_back.png")
unbox(C + "forge_front.png")
keep_largest(C + "forge_front.png")
restreak("pixelbyte_back", (40, 90, 200))
restreak("forge_front", (255, 255, 255))
grey_but_markers(C + "forge_front.png")
unfloor(C + "forge_front.png", 51)

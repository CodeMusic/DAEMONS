#!/usr/bin/env python3
"""T-176 batch 1: three drafts sit on a grey box the background fill stopped at, and MUTEX's back came back in
colour. The box goes first, then the largest shape is kept, and the coloured one is greyed -- every pixel but
gbasprite.py's four streak markers (batch 15's rule). Run from the repo root, after cleandraft.py."""
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


C = "gfx/drafts/t176/clean/"


def restreak(name, ground=(40, 90, 200)):
    im = Image.open(C + name + ".png").convert("RGBA")
    big = Image.new("RGBA", (512, 512), ground + (255,))
    big.alpha_composite(im.resize((512, 512), Image.NEAREST))
    tmp = "/tmp/t176_%s_8x.png" % name
    big.convert("RGB").save(tmp)
    out = subprocess.run(["python3", "tools/cleandraft.py", tmp, C + name + ".png", "--streaks"], capture_output=True, text=True)
    print("  %-18s %s" % (name, (out.stdout or out.stderr).strip().splitlines()[-1]))


def unbox_band(path, lo, hi):
    """a flood from the border through greys in [lo, hi): DRUM's and MAGTAPE's boxes shade unevenly, so a tolerance
    around one seed leaves half the box behind (T-165 met the same thing on PIXELBYTE)"""
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


BOXED = ("drum_front", "drum_back", "magtape_front", "monolith_front") if "--batch1" in sys.argv else ("trust_back", "elation_back")
GREY = ("mutex_back",) if "--batch1" in sys.argv else ("mood_front", "cunning_back")
for name in BOXED:
    unbox(C + name + ".png")
    unbox_band(C + name + ".png", 96, 200)
    keep_largest(C + name + ".png")
    restreak(name)
for name in GREY:
    grey_but_markers(C + name + ".png")
    print("  greyed %s" % name)
print("  fixed %d boxes" % len(BOXED))

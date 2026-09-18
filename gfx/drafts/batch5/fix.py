#!/usr/bin/env python3
"""T-131 batch 5: what cleandraft.py does not take, fixed after it (batch 2's fix.py, the same two tools).

CAPSULE's front was drawn on a grey square the background fill stopped at.
Run after cleandraft.py, from the repo root."""
from PIL import Image

def unbox(path, seed=(1, 1), tol=14):
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

def unline(path, rows=4):
    """A ground line: every opaque pixel in the bottom rows that is part of a run wider than the subject's foot."""
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    for y in range(h - rows - 4, h):
        run = [x for x in range(w) if px[x, y][3]]
        if len(run) > w // 2:
            for x in run:
                px[x, y] = (0, 0, 0, 0)
    im.save(path)

unbox("gfx/drafts/batch5/clean/capsule_front.png")

def unshadow(path, y0, ref, tol=10):
    """LULL stands on a drop shadow the fill could not take (it touches the feet): a flat grey band below y0."""
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    for y in range(y0, h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a and max(abs(r - ref[0]), abs(g - ref[1]), abs(b - ref[2])) <= tol:
                px[x, y] = (0, 0, 0, 0)
    #  the band's edge pixels are another grey; once an empty row separates them from the feet, they go too
    rows = [any(px[x, y][3] for x in range(w)) for y in range(h)]
    gap = next((y for y in range(y0, h) if not rows[y]), None)
    if gap is not None:
        for y in range(gap, h):
            for x in range(w):
                px[x, y] = (0, 0, 0, 0)
    im.save(path)

unshadow("gfx/drafts/batch5/clean/lull_front.png", 45, (122, 124, 131))
unshadow("gfx/drafts/batch5/clean/lull_back.png", 45, (139, 139, 144))

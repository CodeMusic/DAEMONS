#!/usr/bin/env python3
"""T-131 batch 4: what cleandraft.py does not take, fixed after it (batch 2's fix.py, the same two tools).

LOOP's front was drawn on a dark square the background fill stopped at; its back stands on a white ground line.
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

unbox("gfx/drafts/batch4/clean/loop_front.png")
unline("gfx/drafts/batch4/clean/loop_back.png")

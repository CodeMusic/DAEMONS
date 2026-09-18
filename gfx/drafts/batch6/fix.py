#!/usr/bin/env python3
"""T-131 batch 6: what cleandraft.py does not take, fixed after it (batch 2's fix.py, the same two tools).

TAPPOINT's two views were drawn on a dark square the background fill stopped at.
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

# the square has a darker rim, so the fill starts on its face, a few pixels in
unbox("gfx/drafts/batch6/clean/tappoint_front.png", seed=(12, 12), tol=16)
unbox("gfx/drafts/batch6/clean/tappoint_back.png", seed=(12, 12), tol=16)

def unrim(path):
    """What is left of the square once its face is gone: a one-pixel rim, which is any opaque pixel with at most
    two opaque 4-neighbours whose run along its row or column is a line, not a body. Repeated until none go."""
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    op = lambda x, y: 0 <= x < w and 0 <= y < h and px[x, y][3] > 0
    while True:
        gone = [(x, y) for y in range(h) for x in range(w) if op(x, y) and
                sum(op(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) <= 2 and
                not (op(x, y - 1) and op(x, y + 1) and (op(x - 1, y) or op(x + 1, y)))
                and ((op(x - 1, y) or op(x + 1, y)) != (op(x, y - 1) or op(x, y + 1)))]
        if not gone:
            break
        for x, y in gone:
            px[x, y] = (0, 0, 0, 0)
    im.save(path)

unrim("gfx/drafts/batch6/clean/tappoint_front.png")
unrim("gfx/drafts/batch6/clean/tappoint_back.png")

def despeck(path, size=4):
    """The rim's corners, left as detached specks: any opaque component of fewer than `size` pixels goes."""
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size; seen = set()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and (x, y) not in seen:
                comp, todo = [], [(x, y)]
                while todo:
                    p = todo.pop()
                    if p in seen or not (0 <= p[0] < w and 0 <= p[1] < h) or not px[p][3]:
                        continue
                    seen.add(p); comp.append(p)
                    todo += [(p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)]
                if len(comp) < size:
                    for p in comp:
                        px[p] = (0, 0, 0, 0)
    im.save(path)

despeck("gfx/drafts/batch6/clean/tappoint_front.png")
despeck("gfx/drafts/batch6/clean/tappoint_back.png")

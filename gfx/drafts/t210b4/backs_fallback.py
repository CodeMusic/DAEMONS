#!/usr/bin/env python3
"""T-210 batch 4: the backs no seed turned away, made T-166's way (gfx/drafts/t166/fourth.py, its deface() copied
here rather than imported, since that script runs on import). SIDE-ON: the cleaned front mirrored. FACE-ON: mirrored
with the face removed, looked for only in the head's rows (read off each front's silhouette). Run from the repo root."""
import ast, statistics
from PIL import Image

tree = ast.parse(open("tools/gbasprite.py").read())
MARKS = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "STREAK_MARKERS" for t in n.targets))
MARKS = {tuple(m) for m in (MARKS.values() if isinstance(MARKS, dict) else MARKS)}
C = "gfx/drafts/t210b4/clean"
SIDE = ["datagram", "tradewind", "warmstart"]
FACE = {"gestalt": (16, 34), "inkling": (10, 28)}

def lum(p): return (p[0] * 299 + p[1] * 587 + p[2] * 114) // 1000
def sat(p): return max(p[:3]) - min(p[:3])

def deface(im, rows):
    px = im.load(); w, h = im.size
    op = lambda x, y: 0 <= x < w and 0 <= y < h and px[x, y][3] > 0
    def feature(x, y):
        p = px[x, y]
        if not op(x, y) or p[:3] in MARKS:
            return False
        if not all(op(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):   # the outline stays
            return False
        return lum(p) < 70 or (sat(p) > 40)
    todo = {(x, y) for y in range(*rows) for x in range(w) if feature(x, y)}
    for _ in range(12):
        if not todo:
            break
        done = set()
        for x, y in todo:
            ns = [px[x + dx, y + dy] for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)
                  if (x + dx, y + dy) not in todo and op(x + dx, y + dy) and px[x + dx, y + dy][:3] not in MARKS
                  and lum(px[x + dx, y + dy]) >= 70 and sat(px[x + dx, y + dy]) <= 40]
            if len(ns) >= 3:
                l = int(statistics.median(lum(n) for n in ns))
                px[x, y] = (l, l, l, 255); done.add((x, y))
        todo -= done
    return im

for n in SIDE:
    Image.open("%s/%s_front.png" % (C, n)).convert("RGBA").transpose(Image.FLIP_LEFT_RIGHT).save("%s/%s_back.png" % (C, n))
    print("  %-10s back  mirrored" % n)
for n, rows in FACE.items():
    im = Image.open("%s/%s_front.png" % (C, n)).convert("RGBA").transpose(Image.FLIP_LEFT_RIGHT)
    deface(im, rows).save("%s/%s_back.png" % (C, n))
    print("  %-10s back  mirrored, face removed in rows %d-%d" % (n, rows[0], rows[1]))

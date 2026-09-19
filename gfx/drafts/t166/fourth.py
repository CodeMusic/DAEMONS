#!/usr/bin/env python3
"""T-166, the last 26 (decided by the user 2026-09-19: "split them").

SIDE-ON daemons take their approved front, MIRRORED, as the back: a side view already faces the foe, which is what
many Gen 3 back sprites are. FACE-ON daemons take the mirrored front with the FACE REMOVED -- no model would turn them:
eyes, beak and mouth are the dark or saturated pixels INSIDE the head's outline (not touching the transparent edge,
not a streak marker), and each is filled with the median of the body pixels around it, repeated until none is left.
What remains reads as the plain back of the same shape."""
import ast, statistics
from PIL import Image

tree = ast.parse(open("tools/gbasprite.py").read())
MARKS = {tuple(m) for m in next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
         and any(getattr(t, "id", "") == "STREAK_MARKERS" for t in n.targets))}
SIDE = ["nozzle", "jetstream", "turbulence", "stub", "upstream", "hotpath", "overdrive", "illusion", "starr", "handler",
        "emergence", "escalate", "fixation"]
FACE = {  # the rows (of 64) the head occupies, read off each front: the face is only looked for there
    "coldread": (8, 30), "vigilance": (6, 38), "bristle": (10, 50), "apathy": (14, 40), "broadcast": (12, 30),
    "cryogen": (14, 36), "grasp": (8, 28), "imitation": (10, 30), "omen": (8, 30), "repay": (12, 40), "simmer": (18, 42),
    "singular": (4, 24), "axiomkick": (6, 32)}

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
    Image.open("gfx/daemons/%s_front.png" % n).convert("RGBA").transpose(Image.FLIP_LEFT_RIGHT).save("gfx/drafts/t166/clean4/%s_back.png" % n)
for n, rows in FACE.items():
    im = Image.open("gfx/daemons/%s_front.png" % n).convert("RGBA").transpose(Image.FLIP_LEFT_RIGHT)
    deface(im, rows).save("gfx/drafts/t166/clean4/%s_back.png" % n)

#!/usr/bin/env python3
"""T-174: the nine candidates beside the art in the game, each CUT at the size the game shows it.

    python3 gfx/drafts/t174/judge.py            # -> gfx/drafts/t174/judge.png

Judging a restyle at 904px is how a portrait gets approved and then disappoints in play: the speckle, the thinned
hem and the lost face all arrive in the REDUCTION. So every cell here goes through gbachar's own cut and palette
fit -- 15 colours at 64x64, 25 or 31 at 64x96 -- and is then blown up with NEAREST, which shows the sprite and not
the drawing.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gbachar

D = "gfx/drafts/t174"
SEEDS = ["1917", "7", "r2"]
WHO = [  # name, the gbachar job it would replace
    ("holt", "holt"), ("vera", "vera"), ("init", "init"), ("cairn", "cairn"), ("scorn", "scorn"),
    ("al_speech", "al_speech"), ("al_early", "al_early"), ("al_late", "al_late"), ("al_champion", "al_champion"),
]


def cell(src, job):
    j = dict(job); j["src"] = src
    c, hold = gbachar.cut(j)
    out, _ = gbachar.index(c, hold, j)
    a = np.asarray(out.convert("RGB")).copy()
    a[np.asarray(hold) == 0] = (248, 248, 246)          # the key is not a colour anyone judges
    return Image.fromarray(a)


def main():
    S = 4
    groups = []
    for name, jobname in WHO:
        job = gbachar.JOBS[jobname]
        shots = [("in game", cell(job["src"], job))]
        for seed in SEEDS:
            p = "%s/alt2/%s_%s.png" % (D, name, seed)
            if os.path.exists(os.path.join(ROOT, p)):
                shots.append(("seed " + seed, cell(p, dict(job, hue=False))))
        groups.append((name, job["size"], shots))
    CW, RH = 64 * S + 12, 96 * S + 34
    COLS, ROWS = 2, (len(groups) + 1) // 2
    out = Image.new("RGB", (COLS * (4 * CW + 22), ROWS * RH + 10), (40, 44, 52))
    d = ImageDraw.Draw(out)
    for i, (name, size, shots) in enumerate(groups):
        gx, gy = (i // ROWS) * (4 * CW + 22) + 10, (i % ROWS) * RH + 8
        d.text((gx, gy), name.upper(), fill=(250, 220, 150))
        for j, (label, im) in enumerate(shots):
            x = gx + j * CW
            d.rectangle([x, gy + 16, x + 64 * S + 4, gy + 20 + size[1] * S + 14], fill=(250, 250, 248))
            out.paste(im.resize((64 * S, size[1] * S), Image.NEAREST), (x + 2, gy + 18))
            d.text((x + 4, gy + 22 + size[1] * S), label if label != "seed r2" else "round 2",
                   fill=(60, 60, 64) if label == "in game" else (20, 80, 140))
    out.save(os.path.join(ROOT, D, "judge.png"))
    print("  -> %s/judge.png" % D)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""T-178: each redraw cut at 64x64, beside the portrait the game shows now.

    python3 gfx/drafts/t178/judge.py            # -> gfx/drafts/t178/judge.png

Both sides go through gbachar's own cut and palette fit, so the comparison is the sprite and not the drawing --
and both carry T-177's outline, so what is being judged is the DRAWING, not the edge.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = "/Users/christopherhicks/Projects/DAEMONS"
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import importlib.util
spec = importlib.util.spec_from_file_location("gc", "tools/gbachar.py")
gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gc)

WHO = [("beauty", "p_beauty"), ("gamer", "p_gamer"), ("ranger_m", "p_ranger_m"),
       ("ranger_f", "p_ranger_f"), ("juggler", "p_juggler")]
SEEDS = ["1917", "42"]
D = "gfx/drafts/t178/alt"


def cell(src, job):
    j = dict(job); j["src"] = src
    c, hold = gc.cut(j)
    out, _ = gc.index(c, hold, j)
    a = np.asarray(out.convert("RGB")).copy()
    a[np.asarray(hold) == 0] = (248, 248, 246)
    return Image.fromarray(a)


def main():
    S = 5
    rows = []
    for name, jobname in WHO:
        job = gc.JOBS[jobname]
        shots = [("in game", cell(job["src"], job))]
        for s in SEEDS:
            p = "%s/%s_%s.png" % (D, name, s)
            if os.path.exists(p):
                try:
                    shots.append(("seed " + s, cell(p, dict(job, hue=False))))
                except Exception as e:
                    print("  %s seed %s did not cut: %s" % (name, s, e))
        rows.append((name, shots))
    CW, RH = 64 * S + 12, 64 * S + 34
    out = Image.new("RGB", (3 * CW + 16, len(rows) * RH + 10), (40, 44, 52))
    d = ImageDraw.Draw(out)
    for r, (name, shots) in enumerate(rows):
        y = r * RH + 8
        d.text((6, y), name.upper(), fill=(250, 220, 150))
        for i, (label, im) in enumerate(shots):
            x = i * CW + 76
            d.rectangle([x, y, x + 64 * S + 4, y + 64 * S + 18], fill=(250, 250, 248))
            out.paste(im.resize((64 * S, 64 * S), Image.NEAREST), (x + 2, y + 2))
            d.text((x + 4, y + 64 * S + 4), label, fill=(60, 60, 64) if label == "in game" else (20, 80, 140))
    out.save("gfx/drafts/t178/judge.png")
    print("  -> gfx/drafts/t178/judge.png")


if __name__ == "__main__":
    main()

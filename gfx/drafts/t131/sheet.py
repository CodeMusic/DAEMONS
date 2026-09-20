#!/usr/bin/env python3
"""T-131's twelve: every draft beside its own alternative, for the pick.

    python3 gfx/drafts/t131/sheet.py            # -> gfx/drafts/t131/sheet.png

Four cells a species: front at each seed, then back at each seed. Nothing is cleaned yet -- the pick comes first,
because cleaning a draft that will not be used is the slowest part of a batch.
"""
import os, sys
from PIL import Image, ImageDraw

ROOT = "/Users/christopherhicks/Projects/DAEMONS"
D = os.path.join(ROOT, "gfx/drafts/t131/alt")
WHO = ["poll", "watchdog", "pilot", "sounding", "starved", "quota",
       "fakeroot", "duplex", "warning", "cache", "triton", "phoenix"]
SEEDS = ["1917", "42", "r27", "r21917"]
C = 150


def main():
    cols = [(v, s) for v in ("front", "back") for s in SEEDS]
    W, H = len(cols) * (C + 6) + 96, len(WHO) * (C + 8) + 22
    out = Image.new("RGB", (W, H), (34, 36, 42))
    d = ImageDraw.Draw(out)
    for j, (v, s) in enumerate(cols):
        d.text((96 + j * (C + 6), 6), "%s %s" % (v, s.replace("r2", "r2 seed ")), fill=(150, 200, 235) if not s.startswith("r2") else (250, 190, 140))
    for i, name in enumerate(WHO):
        y = 20 + i * (C + 8)
        d.text((6, y + C // 2), name.upper(), fill=(250, 220, 150))
        for j, (v, s) in enumerate(cols):
            p = os.path.join(D, "%s_%s_%s.png" % (name, v, s))
            if not os.path.exists(p):
                continue
            im = Image.open(p).convert("RGB").resize((C, C), Image.LANCZOS)
            out.paste(im, (96 + j * (C + 6), y))
    out.save(os.path.join(ROOT, "gfx/drafts/t131/sheet2.png"))
    print("  -> gfx/drafts/t131/sheet2.png")


if __name__ == "__main__":
    main()

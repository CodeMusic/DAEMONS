#!/usr/bin/env python3
"""The healthbox mark for THRASHING (T-187; vision.md 9.15).

    python3 tools/genthrashicon.py            # preview to /tmp/thrash_icon.png
    python3 tools/genthrashicon.py --write     # into graphics/battle_interface/healthbox_elements.png

THE RULE, WHICH IS WHAT THIS TICKET WAS WAITING FOR. Vanilla's healthbox shows the five STATUS1 states and
nothing else, and the reason given is that the rest are volatile. That is not our reason -- our statuses are
states of mind, and a player who cannot see their daemon is in one cannot reason about it. But marking every
volatile state turns the healthbox into a dashboard, which is a different game's screen.

So: THE HEALTHBOX NAMES WHAT PERSISTS AND MARKS WHAT DOES NOT. The five that follow a daemon out of the
battle are words -- LEK, THR, SUS, HNG, OVR -- and the one that exists only inside it is a MARK, with no
letters. The difference in KIND is drawn rather than stated, and the tag space stays for things that keep.

It also settles an accident: THRASHING's own three letters are taken. THR is THROTTLED.

WHERE IT GOES. healthbox_elements.png is 40x3 tiles, and battle_interface.c says "tiles 36 through 38 are
unused" -- a three-tile hole exactly one status icon wide, reserved by vanilla and never filled. Tile N sits
at x = (N % 40) * 8, so the slot is x 288..311, y 0..7.

WHICH INDICES. gbagfx converts this sheet by index % 16, which every existing icon confirms: SUS uses
50/51/60, THR 34/35/44, HNG 66/67/76 -- all of them 2, 3 and 12 in their own block. 12 is the one colour
FillPalette replaces at runtime with sStatusIconColors[], so 12 is the ground and 2 is the mark.
"""
import os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEET = os.path.join(ROOT, "engineGba/graphics/battle_interface/healthbox_elements.png")
PREVIEW = "/tmp/thrash_icon.png"
WRITE = "--write" in sys.argv
X0, TEMPLATE_X = 288, 216            # the free slot, and SUS which lends its pill
LIGHT, SHADOW, GROUND = 2, 3, 12     # nibbles, not palette entries


def draw(a):
    #  the pill itself is copied from SUS, so the shape is identical to its five neighbours and only what is
    #  inside it differs -- which is the whole point: same badge, no letters.
    for y in range(8):
        for x in range(24):
            a[y][X0 + x] = {2: LIGHT, 3: SHADOW, 12: GROUND}[int(a[y][TEMPLATE_X + x]) % 16]
    for y in range(1, 7):            # clear the letters back to the ground colour
        for x in range(2, 18):
            a[y][X0 + x] = GROUND

    #  A sawtooth: down, up, down, up, across the badge. Not tracking straight, drawn rather than named.
    pts = [(2, 5), (5, 2), (8, 5), (11, 2), (14, 5), (17, 2)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for s in range(steps + 1):
            x = x0 + (x1 - x0) * s // steps
            y = y0 + (y1 - y0) * s // steps
            a[y][X0 + x] = LIGHT
            if y + 1 < 7:            # one pixel of weight, so it survives at 24x8 on a lit ground
                a[y + 1][X0 + x] = LIGHT
    return a


def main():
    im = Image.open(SHEET)
    a = np.array(im)
    before = a.copy()
    a = draw(a)
    out = Image.fromarray(a, "P")
    out.putpalette(im.getpalette())
    print("  the mark, at tiles 36-38 (x %d..%d):" % (X0, X0 + 23))
    for y in range(8):
        print("    " + "".join(".#+"[[LIGHT, SHADOW, GROUND].index(int(a[y][X0 + x]))] for x in range(24)))
    out.crop((X0 - 96, 0, X0 + 32, 8)).resize((128 * 6, 8 * 6), Image.NEAREST).convert("RGB").save(PREVIEW)
    print("  its four neighbours and it -> %s" % PREVIEW)
    if WRITE:
        out.save(SHEET)
        print("  written graphics/battle_interface/healthbox_elements.png")


if __name__ == "__main__":
    main()

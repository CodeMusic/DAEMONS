#!/usr/bin/env python3
"""The overworld disc a PLUGIN or DRIVER lies on the ground as (T-208; vision.md 1.6).

    python3 tools/gendisc.py            # preview to /tmp/plugin_disc.png
    python3 tools/gendisc.py --write    # graphics/object_events/pics/misc/plugin_disc.png

An item lying in the overworld is one sprite for everything, so a routine you install looks exactly like a
potion. A PLUGIN and a DRIVER are the two things in this game that are INSTALLED rather than consumed, and
a disc is what an installer came on -- so the ground says what kind of thing is on it before you reach it.

29 of them are lying about the world: TM50 in VICTORY ROAD, HM07 in the ICEFALL CAVE, and so on.

FORMAT. A 16x16 overworld pic is two frames of 2x2 tiles in a 16x32 sheet (`overworld_frame(pic, 2, 2, n)`),
and the second frame is what an inanimate object shows when nothing is animating it -- so both are drawn the
same. Sixteen colours, entry 0 transparent, and it borrows the ITEM BALL's own palette slot so no new
palette tag is spent.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "engineGba/graphics/object_events/pics/misc/plugin_disc.png")
PREVIEW = "/tmp/plugin_disc.png"
WRITE = "--write" in sys.argv

#  Matched to the item ball's own palette so the slot it borrows already holds these.
PAL = [(0, 0, 0), (16, 16, 20), (248, 248, 248), (176, 184, 200), (96, 108, 130),
       (64, 72, 90), (216, 224, 236), (140, 160, 200)]
PAL += [(0, 0, 0)] * (16 - len(PAL))
INK, LIT, MID, DARK, SHEEN, HOLE = 1, 2, 3, 4, 6, 5


def frame():
    px = [[0] * 16 for _ in range(16)]
    #  a disc seen at the overworld's angle: a wide ellipse, an ink edge, a bright arc across the top left,
    #  and the hole in the middle that makes it a disc and not a coin.
    for y in range(16):
        for x in range(16):
            dx, dy = (x - 7.5) / 7.0, (y - 9.0) / 4.6
            r = dx * dx + dy * dy
            if r <= 1.0:
                px[y][x] = MID if r > 0.55 else LIT
            elif r <= 1.30:
                px[y][x] = INK
    for y in range(16):                          # the sheen, upper left
        for x in range(16):
            dx, dy = (x - 7.5) / 7.0, (y - 9.0) / 4.6
            if dx * dx + dy * dy <= 0.95 and (dx + dy) < -0.55:
                px[y][x] = SHEEN
    for y in range(16):                          # the hole
        for x in range(16):
            dx, dy = (x - 7.5) / 1.7, (y - 9.0) / 1.15
            if dx * dx + dy * dy <= 1.0:
                px[y][x] = DARK
            elif dx * dx + dy * dy <= 2.1:
                px[y][x] = INK
    return px


def main():
    f = frame()
    im = Image.new("P", (16, 32))
    im.putpalette([v for c in PAL for v in c])
    im.putdata([c for row in f for c in row] * 2)     # both frames the same; it is inanimate
    im.resize((16 * 10, 32 * 10), Image.NEAREST).convert("RGB").save(PREVIEW)
    for row in f:
        print("    " + "".join(" .123456789"[c] if c < 10 else "?" for c in row))
    print("  -> %s" % PREVIEW)
    if WRITE:
        im.save(OUT)
        print("  written %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()

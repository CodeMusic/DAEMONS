#!/usr/bin/env python3
"""OPUS's item icon, authored in code (T-197; vision.md 4.2).

    python3 tools/genopusicon.py            # preview to /tmp/opus_icon.png
    python3 tools/genopusicon.py --write    # graphics/items/icons/opus.png + its palette

IT BORROWED THE UP-GRADE'S until now, which was defensible -- a small device, and an addition to something --
but two items sharing a look is a thing a player notices and cannot unsee.

WHAT IT IS. An opus number is how a catalogue files a work, so the object is an INDEX CARD: a pale card, one
ruled margin down the left, and a single mark written in that margin. Nothing else. It says what OPUS does
without saying what OPUS is, which is the same restraint the rest of it keeps.

FORMAT. Gen 3 item icons are 24x24, mode "P", sixteen colours, with entry 0 transparent, and the palette
ships beside the picture as a JASC .pal the build turns into a .gbapal.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PREVIEW = "/tmp/opus_icon.png"
WRITE = "--write" in sys.argv

#  The ink is the project's own (T-177/T-184), so the card is outlined in the same black as every daemon.
PAL = [
    (0, 0, 0),          # 0 transparent
    (16, 16, 20),       # 1 ink
    (243, 241, 232),    # 2 card, lit
    (226, 223, 210),    # 3 card
    (198, 194, 178),    # 4 card, shaded
    (150, 146, 132),    # 5 the ruled margin
    (96, 112, 138),     # 6 the mark in the margin
]
PAL += [(0, 0, 0)] * (16 - len(PAL))


def draw():
    px = [[0] * 24 for _ in range(24)]

    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px[y][x] = c

    rect(3, 4, 20, 19, 3)                       # the card
    rect(3, 4, 20, 5, 2)                        # lit along the top
    rect(3, 18, 20, 19, 4)                      # shaded along the bottom
    for x in range(3, 21):                      # the outline
        px[3][x] = px[20][x] = 1
    for y in range(3, 21):
        px[y][2] = px[y][21] = 1
    px[3][2] = px[3][21] = px[20][2] = px[20][21] = 0      # corners off, so it reads as a card

    for y in range(5, 19):                      # the ruled margin, down the left
        px[y][6] = 5
    for x in range(9, 19):                      # the body of the card: lines of writing
        for y in (8, 11, 14, 17):
            px[y][x] = 5                        # the card's own shade was too near the card to read at 24px

    #  and the mark in the margin, which is the whole point of the object, so it is the boldest thing on it:
    #  a short stroke beside the second line, in the one colour nothing else uses.
    for y in range(8, 12):
        px[y][4] = px[y][5] = 6
    return px


def main():
    px = draw()
    im = Image.new("P", (24, 24))
    im.putpalette([v for c in PAL for v in c])
    im.putdata([c for row in px for c in row])
    im.resize((24 * 8, 24 * 8), Image.NEAREST).convert("RGB").save(PREVIEW)
    print("  the card, the margin rule, and the one mark in it -> %s" % PREVIEW)
    if WRITE:
        im.save(os.path.join(GBA, "graphics/items/icons/opus.png"))
        with open(os.path.join(GBA, "graphics/items/icon_palettes/opus.pal"), "w") as fh:
            fh.write("JASC-PAL\n0100\n16\n")
            for c in PAL:
                fh.write("%d %d %d\n" % c)
        print("  written graphics/items/icons/opus.png and icon_palettes/opus.pal")


if __name__ == "__main__":
    main()

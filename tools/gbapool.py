#!/usr/bin/env python3
"""The POOL is a rack of slots (T-207; decided by the user, 2026-09-24).

    python3 tools/gbapool.py            # report
    python3 tools/gbapool.py --write     # graphics/interface/bag_male.png, bag_female.png, bag.pal

T-193 renamed BAG to POOL and the picture stayed vanilla's rucksack. The user chose the rack -- "a memory pool is a
set of slots" -- and added the reason the picture matters at all: "we need the computer visual if we use the word
POOL, otherwise people will jump to swimming."

The drawing is ours, in gfx/ui/pool_rack.png at three times size, and this tool is the only way it reaches the
ROM. The bag sheet is four 64x64 frames: 0 is the rest pose, 1 is BOXES, 2 ITEMS, 3 KEY ITEMS
(item_menu_icons.c's sAnim_Bag_Open*Pocket). EACH POCKET LIGHTS ONE DRAWER -- ITEMS the first, KEY ITEMS the
second, BOXES the third -- and the rest pose lights none.

THE LIGHT IS NOT GREEN. The approved drawing lit its drawers green; T-209's rule is that the UI's own colours may
not use a type's hue (colour carries the chart, 9.4), and green reads as GROWTH. So a lit drawer glows the warm
cream of the house palette's paper (T-209, INK AND PAPER).
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SRC = os.path.join(ROOT, "gfx/ui/pool_rack.png")
OUTS = [os.path.join(GBA, "graphics/interface/bag_male.png"), os.path.join(GBA, "graphics/interface/bag_female.png")]
PAL = os.path.join(GBA, "graphics/interface/bag.pal")
WRITE = "--write" in sys.argv

GROUND = (250, 249, 245)                 # the drawing's paper, which is transparency in the game
TRANSPARENT = (82, 205, 180)             # vanilla's index 0 for this sheet
GREEN = (110, 200, 140)
LIT = (255, 240, 180)
HANDLES = [13, 22, 31, 40, 49]           # first row of each drawer's handle, top to bottom
LIGHT_X = (44, 45, 46)
FRAME_DRAWER = [None, 2, 0, 1]           # rest, BOXES, ITEMS, KEY ITEMS


def main():
    src = Image.open(SRC).convert("RGB").resize((64, 64), Image.NEAREST)
    spx = src.load()
    for y in range(64):                                  # no drawer lit in the base
        for x in LIGHT_X:
            if spx[x, y] == GREEN:
                spx[x, y] = spx[43, y]
    colours = [TRANSPARENT] + sorted({c for c in src.getdata() if c != GROUND}) + [LIT]
    assert len(colours) <= 16, colours
    index = {c: i for i, c in enumerate(colours)}
    sheet = Image.new("P", (64, 256), 0)
    sheet.putpalette([v for c in colours + [(0, 0, 0)] * (16 - len(colours)) for v in c] + [0] * (768 - 48))
    px = sheet.load()
    for f, drawer in enumerate(FRAME_DRAWER):
        for y in range(64):
            for x in range(64):
                c = spx[x, y]
                px[x, f * 64 + y] = 0 if c == GROUND else index[c]
        if drawer is not None:
            for y in (HANDLES[drawer], HANDLES[drawer] + 1):
                for x in LIGHT_X:
                    px[x, f * 64 + y] = index[LIT]
    pal = "JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in colours + [(0, 0, 0)] * (16 - len(colours)))
    changed = open(PAL, newline="").read().replace("\r\n", "\n") != pal or any(list(Image.open(o).getdata()) != list(sheet.getdata()) for o in OUTS)
    print("  the POOL %s" % ("is to be the rack" if changed else "is already the rack"))
    if WRITE and changed:
        for o in OUTS:
            sheet.save(o)
        open(PAL, "w").write(pal)
        print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())

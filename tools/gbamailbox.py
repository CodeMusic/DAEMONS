#!/usr/bin/env python3
"""Our own mailbox, wherever vanilla's stood (T-91; vision.md 9.22).

    python3 tools/gbamailbox.py            # preview to /tmp/mailbox.png (vanilla | ours, in row 2 and in Blanche's row 10)
    python3 tools/gbamailbox.py --write    # the four General tiles, in place

Vanilla's mailbox is four General tiles (352, 353, 368, 369) drawn by one General
block and by a copy in each of Blanche's and Brazen's tilesets -- the paler one
in Blanche only because its copy points at row 10, which is row 2 made pale index
for index. So the mailbox is redrawn once, in place, in row 2's index roles, and
every town gets it: Blanche's is pale for free.

The drawing: a rural mailbox with a rounded top, seen from the front and a little
above -- a dark mouth under the lid, a latch, a raised flag -- on a square post.
No warm colour: the flag is ink, because in Blanche row 2's reds would come out
as row 10's rose, and the lab keeps Blanche's only warm note (9.22).

VANILLA'S LID stood a cell higher: every mailbox has a block above it whose top
layer draws General tiles 336 and 337 (General 353, and one block each in
Cerulean, Blanche, Saffron and Sevii 4-5). Ours is whole in its own cell, so
those two tiles are cleared to transparent -- left alone they drew vanilla's lid
above ours, an echo of the old mailbox. Nothing else outdoors draws them.

The Building tileset (every interior) numbers its own tiles 336..369 and is not
touched: this writes the General sheet only.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
PREVIEW = "/tmp/mailbox.png"
WRITE = "--write" in sys.argv
TILES = (352, 353, 368, 369)          # top-left, top-right, bottom-left, bottom-right
LID = (336, 337)                      # vanilla's lid, in the block above: cleared

# row 2 roles: 1 white, 2 pale, 3 light, 4 mid, 5 grey, 6 dark, 7 ink; . transparent
ART = [
    "................",
    "..........77....",
    "....7777777777..",
    "...72111111177..",
    "..7211111111467.",
    "..7211111111467.",
    "..7666666666647.",
    "..7677777777647.",
    "..7666666666647.",
    "..7322222222347.",
    "..7322225522347.",
    "..7433333333447.",
    "...7777777777...",
    "......7447......",
    "......7457......",
    ".....774577.....",
]


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    assert len(ART) == 16 and all(len(r) == 16 for r in ART)
    # the flag stands up right of the lid: a staff and a pennant
    art = [list(r) for r in ART]
    for y in range(0, 6):
        art[y][13] = "7"
    art[0][13] = art[0][14] = art[1][14] = art[1][15] = "7"
    px = [[0 if ch == "." else int(ch) for ch in row] for row in art]

    path = os.path.join(PD, "tiles.png")
    img = Image.open(path); p = img.load()
    new = img.copy(); n = new.load()
    for q, t in enumerate(TILES):
        ox, oy = (q % 2) * 8, (q // 2) * 8
        for y in range(8):
            for x in range(8):
                n[(t % 16) * 8 + x, (t // 16) * 8 + y] = px[oy + y][ox + x]
    for t in LID:
        for y in range(8):
            for x in range(8):
                n[(t % 16) * 8 + x, (t // 16) * 8 + y] = 0

    rows = {"row 2": read_pal(os.path.join(PD, "palettes/02.pal")),
            "Blanche's row 10": read_pal(os.path.join(GBA, "data/tilesets/secondary/pallet_town/palettes/10.pal"))}
    sheet = Image.new("RGB", (16 * 4 + 24, 16), (110, 170, 100))
    for k, pal in enumerate(rows.values()):
        for side, src in enumerate((p, n)):
            for q, t in enumerate(TILES):
                for y in range(8):
                    for x in range(8):
                        v = src[(t % 16) * 8 + x, (t // 16) * 8 + y]
                        if v:
                            sheet.putpixel((k * 40 + side * 18 + (q % 2) * 8 + x, (q // 2) * 8 + y), pal[v])
    sheet.resize((sheet.width * 8, sheet.height * 8), Image.NEAREST).save(PREVIEW)
    print("  preview %s (vanilla | ours in row 2, then vanilla | ours in Blanche's row 10)" % PREVIEW)
    if WRITE:
        new.save(path)
        print("  written: General tiles %s, and vanilla's lid %s cleared" % (TILES, LID))


if __name__ == "__main__":
    main()

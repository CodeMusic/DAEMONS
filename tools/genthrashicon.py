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
#  (destination tile, source tile) for each battler. Battler 0 uses the three tiles vanilla itself reserved
#  and never filled; the other three had nowhere to go, so the sheet gains a fourth row and they sit in it.
#  Each one copies ITS OWN battler's SUS icon, because the badge is shaped differently per healthbox -- a
#  check confirmed battler 0's icons are not battler 1's.
SLOTS = [(36, 27), (120, 77), (123, 92), (126, 107)]
SHEET_ROWS = 4                       # was 3; tiles 120-159 are the new row
#  WHY THE FOUR VARIANTS EXIST, which is not what it looks like: the badges are the SAME SHAPE, and what
#  differs is the palette index of the ground. UpdateStatusIconInHealthbox does `pltAdder += battlerId + 12`
#  and fills ONE entry, so battler 0's ground is nibble 12, battler 1's is 13, and so on. Copying battler 0's
#  tiles for everyone would have drawn every opponent's badge in whatever colour that slot happened to hold.
LIGHT, SHADOW = 2, 3                 # nibbles, not palette entries
GROUND_BASE = 12                     # + the battler


def tile_xy(n):
    return (n % 40) * 8, (n // 40) * 8


def draw_one(a, dst, src, battler):
    dx, dy = tile_xy(dst)
    sx, sy = tile_xy(src)
    GROUND = GROUND_BASE + battler
    #  the pill itself is copied, so the shape is identical to its five neighbours and only what is inside
    #  it differs -- which is the whole point: same badge, no letters.
    for y in range(8):
        for x in range(24):
            n = int(a[sy + y][sx + x]) % 16
            a[dy + y][dx + x] = LIGHT if n == LIGHT else (SHADOW if n == SHADOW else GROUND)
    for y in range(1, 7):            # clear the letters back to the ground colour
        for x in range(2, 18):
            a[dy + y][dx + x] = GROUND

    #  A sawtooth: down, up, down, up, across the badge. Not tracking straight, drawn rather than named.
    pts = [(2, 5), (5, 2), (8, 5), (11, 2), (14, 5), (17, 2)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for t in range(steps + 1):
            x = x0 + (x1 - x0) * t // steps
            y = y0 + (y1 - y0) * t // steps
            a[dy + y][dx + x] = LIGHT
            if y + 1 < 7:            # one pixel of weight, so it survives at 24x8 on a lit ground
                a[dy + y + 1][dx + x] = LIGHT


def draw(a):
    for battler, (dst, src) in enumerate(SLOTS):
        draw_one(a, dst, src, battler)
    return a


def main():
    im = Image.open(SHEET)
    a = np.array(im)
    #  the sheet grows by one row of forty tiles. gBattleInterface_Gfx is declared [][32] and indexed by
    #  tile, and nothing anywhere counts them, so a longer blob costs only ROM.
    want = SHEET_ROWS * 8
    if a.shape[0] < want:
        pad = np.zeros((want - a.shape[0], a.shape[1]), dtype=a.dtype)
        a = np.concatenate([a, pad], axis=0)
    a = draw(a)
    out = Image.fromarray(a, "P")
    out.putpalette(im.getpalette())
    print("  the sheet is %dx%d now (%d tiles)" % (a.shape[1], a.shape[0], (a.shape[1] // 8) * (a.shape[0] // 8)))
    for battler, (dst, src) in enumerate(SLOTS):
        dx, dy = tile_xy(dst)
        used = sorted({int(a[dy + y][dx + x]) % 16 for y in range(8) for x in range(24)})
        print("  battler %d: tiles %d-%d from %d, nibbles %s" % (battler, dst, dst + 2, src, used))
    out.crop((192, 0, 320, 8)).resize((128 * 6, 8 * 6), Image.NEAREST).convert("RGB").save(PREVIEW)
    print("  battler 0's, beside its neighbours -> %s" % PREVIEW)
    if WRITE:
        out.save(SHEET)
        print("  written graphics/battle_interface/healthbox_elements.png")


if __name__ == "__main__":
    main()

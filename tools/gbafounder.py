#!/usr/bin/env python3
"""Put CRYSTAL CLEAR in the photograph on the Quicksilver lab's wall.

    python3 tools/gbafounder.py            # report, and preview to /tmp/founder.png
    python3 tools/gbafounder.py --write    # data/tilesets/secondary/lab/tiles.png

vision.md 2987: "Quicksilver keeps a photograph of the lab's founder." 3428:
the lab on Quicksilver IS CLEAR LABORATORY, her building -- so the founder in
the frame is Crystal, and vanilla's photo was Dr. Fuji's bald yellow head.

THE PHOTO IS MAP TILES, NOT A SPRITE. The sign at (4, 1) on
CinnabarIsland_PokemonLab_Entrance sits on metatile 797, and the frame spans
the one above it, 789. Their TOP LAYERS carry the picture:

    789: tiles 650 651, rows 4-7 of each   -> the top four rows of the picture
    797: tiles 666 667, rows 0-5 of each   -> the bottom six rows

inside a red frame, so the picture is ELEVEN PIXELS WIDE AND TEN TALL: tile
650 or 666 columns 2-7, then 651 or 667 columns 0-4. Nothing outside those
pixels is touched -- the frame, its outline and its shadow stay vanilla's.

ALL FOUR TILES BELONG TO THE PHOTO ALONE (checked below, not assumed): 650,
651 and 666, 667 are used by no other metatile, so redrawing them cannot
repaint anything else in the building.

THE PALETTE IS THE BUILDING TILESET'S ROW 0, and it decides what she can wear.
It has three golds, white and near-white, a dark navy, greys, a sky blue, a
blue, greens and reds -- and no purple. So: her gold fur in its own three
steps, the white muzzle, navy eyes and nose, the coat's white collar with grey
lapels, and her top in the blue, which is the nearest the row has.

At eleven pixels a portrait is a head and a collar. The ears are what say fox;
they go to the very top of the frame.
"""
import os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
TILES = os.path.join(GBA, "data/tilesets/secondary/lab/tiles.png")
PRIMARY_METATILES = os.path.join(GBA, "data/tilesets/primary/building/metatiles.bin")
LAB_METATILES = os.path.join(GBA, "data/tilesets/secondary/lab/metatiles.bin")
PAL0 = os.path.join(GBA, "data/tilesets/primary/building/palettes/00.pal")
PREVIEW = "/tmp/founder.png"
WRITE = "--write" in sys.argv
NUM_TILES_IN_PRIMARY = NUM_METATILES_IN_PRIMARY = 640

# Palette row 0 of the Building tileset, by index:
#   1 navy  2 grey  3 light grey  4 white  5 gold, dark  6 gold  7 gold, light
#   8 blue  9 sky  10 near-white
PHOTO = [
    "99599999599",   # the ear tips
    "95659995659",
    "95665556659",   # the top of the head, between the ears
    "95666666659",
    "95616661659",   # the eyes
    "95744644759",   # the white muzzle
    "99544144599",   # the nose
    "99954445999",   # the chin
    "94443834449",   # the coat's collar, grey lapels, her top in blue
    "44434843444",
]

# Where each row of the picture lands: (tile, row inside that tile).
ROWS = [(650, 651, r) for r in range(4, 8)] + [(666, 667, r) for r in range(0, 6)]
LEFT_COLS = range(2, 8)    # picture x 0-5 in the left tile
RIGHT_COLS = range(0, 5)   # picture x 6-10 in the right tile
OURS = {650, 651, 666, 667}
PHOTO_METATILES = {789, 797}


def tile_origin(tile):
    i = tile - NUM_TILES_IN_PRIMARY
    return (i % 16) * 8, (i // 16) * 8


def users(tile):
    found = set()
    for path, base in ((PRIMARY_METATILES, 0), (LAB_METATILES, NUM_METATILES_IN_PRIMARY)):
        data = open(path, "rb").read()
        for m in range(len(data) // 16):
            if any((t & 0x3FF) == tile for t in struct.unpack_from("<8H", data, m * 16)):
                found.add(base + m)
    return found


assert len(PHOTO) == 10 and all(len(r) == 11 for r in PHOTO), "the picture is 11x10"
rc = 0
for tile in sorted(OURS):
    u = users(tile)
    extra = u - PHOTO_METATILES - ({805} if tile in (682, 683) else set())
    if extra:
        print("  !! tile %d is also used by metatiles %s -- redrawing it would repaint them" % (tile, sorted(extra)))
        rc = 1
if rc:
    sys.exit(rc)

img = Image.open(TILES)
assert img.mode == "P", img.mode
px = img.load()
changed = 0
for y, (left, right, row) in enumerate(ROWS):
    for x, col in enumerate(LEFT_COLS):
        tx, ty = tile_origin(left)
        v = int(PHOTO[y][x], 16)
        changed += px[tx + col, ty + row] != v
        px[tx + col, ty + row] = v
    for x, col in enumerate(RIGHT_COLS):
        tx, ty = tile_origin(right)
        v = int(PHOTO[y][6 + x], 16)
        changed += px[tx + col, ty + row] != v
        px[tx + col, ty + row] = v
print("  the founder's photo: %d of 110 pixels differ from what is on disk" % changed)

# Preview: the four tiles as they sit on the wall, in palette row 0, at x16.
pal = [tuple(map(int, l.split())) for l in open(PAL0).read().replace("\r", "").split("\n")[3:19]]
wall = Image.new("RGB", (16, 16), (213, 213, 172))
for (tile, ox, oy) in ((650, 0, 0), (651, 8, 0), (666, 0, 8), (667, 8, 8)):
    tx, ty = tile_origin(tile)
    for yy in range(8):
        for xx in range(8):
            v = px[tx + xx, ty + yy]
            if v:
                wall.putpixel((ox + xx, oy + yy), pal[v])
wall.resize((256, 256), Image.NEAREST).save(PREVIEW)
print("  preview %s" % PREVIEW)

if WRITE:
    img.save(TILES)
    print("  written %s" % os.path.relpath(TILES, ROOT))

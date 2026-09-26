#!/usr/bin/env python3
"""The Guide's shelf on ONE ISLAND: one book pulled out, and the gap it leaves (T-297, the map-hints pilot).

    python3 tools/gbaguideshelf.py            # report, and a preview in the scratch dir
    python3 tools/gbaguideshelf.py --write    # two tiles and two metatiles appended to GenericBuilding2,
                                              # and OneIsland_House2's map script sets them

THE RULE (the user, 2026-09-26): every special find is findable blind first, and REVEAL only makes legible what
a sharp eye could already see. The Guide sits in the blue bookcase of ONE ISLAND's second house -- a bookcase
every house in the game has. So ONE book in it is pulled out: the red spine in the upper row is a pixel wider
and a pixel taller, standing proud over the shelf's lip and catching the light. Nothing says so. Once the Guide
is taken the same place shows a GAP, which is what the shelf's own line has said since T-300: "a shelf with a gap".

WHY NEW METATILES AND NOT AN EDIT. The bookcase is drawn from the PRIMARY Building tileset, which every building
in the game shares; recolouring it there would pull a book out of every bookcase in Kanto. The two variants are
appended to the house's SECONDARY tileset instead -- GenericBuilding2, which eighteen layouts use, but a
metatile nobody else points at changes nothing for them.

THE PIXELS. The bookcase's lower-right top-layer tile (primary 0x251) holds three small spines on its fourth and
fifth rows: grey (2), tan (6) and red (d, column 3). OUT widens the red one into column 2 and raises it into row
2, over the dark shelf line, with the light red (e) on its upper-left pixel. GAP fills the red spine's two
pixels with the bookcase's dark back (1).
"""
import os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
PRIMARY = os.path.join(GBA, "data/tilesets/primary/building")
SECONDARY = os.path.join(GBA, "data/tilesets/secondary/generic_building_2")
SHELF_METATILE = 278            # the bookcase's lower half, at (1,1) in OneIsland_House2
SOURCE_TILE = 0x251             # its lower-right top-layer tile: the three spines
SHELF_XY = (1, 1)


def primary_tile(t):
    im = Image.open(os.path.join(PRIMARY, "tiles.png"))
    w = im.width // 8
    return [[im.getpixel(((t % w) * 8 + x, (t // w) * 8 + y)) for x in range(8)] for y in range(8)]


def variants():
    src = primary_tile(SOURCE_TILE)
    assert src[3][3] == 0xD and src[4][3] == 0xD, "the red spine is not where it was: %r" % src[3:5]
    out = [row[:] for row in src]
    for y in (2, 3, 4):
        out[y][2] = out[y][3] = 0xD
    out[2][2] = 0xE
    gap = [row[:] for row in src]
    gap[3][3] = gap[4][3] = 0x1
    return out, gap


def main():
    out, gap = variants()
    tiles = Image.open(os.path.join(SECONDARY, "tiles.png"))
    meta = open(os.path.join(SECONDARY, "metatiles.bin"), "rb").read()
    attrs = open(os.path.join(SECONDARY, "metatile_attributes.bin"), "rb").read()
    n_tiles = (tiles.width // 8) * (tiles.height // 8)
    n_meta = len(meta) // 16
    base = open(os.path.join(PRIMARY, "metatiles.bin"), "rb").read()[SHELF_METATILE * 16:SHELF_METATILE * 16 + 16]
    battr = open(os.path.join(PRIMARY, "metatile_attributes.bin"), "rb").read()[SHELF_METATILE * 4:SHELF_METATILE * 4 + 4]
    entries = list(struct.unpack("<8H", base))
    assert entries[7] & 0x3FF == SOURCE_TILE, hex(entries[7])

    #  Already written? The last two metatiles are ours if they point at the last two tiles.
    last = [struct.unpack_from("<8H", meta, (n_meta - k) * 16)[7] & 0x3FF for k in (2, 1)] if n_meta >= 2 else []
    done = False
    used = max((y * (tiles.width // 8) + x) for y in range(tiles.height // 8) for x in range(tiles.width // 8)
               if any(tiles.getpixel((x * 8 + i, y * 8 + j)) for i in range(8) for j in range(8)))
    if last and all(t >= 640 for t in last):
        done = last == [640 + used - 1, 640 + used]
    print("  GenericBuilding2: %d tiles in the sheet (last drawn %d), %d metatiles" % (n_tiles, used, n_meta))
    if done:
        print("  already written: metatiles %d (out) and %d (gap)" % (640 + n_meta - 2, 640 + n_meta - 1))
        return 640 + n_meta - 2
    t_out, t_gap = used + 1, used + 2
    print("  will append tiles %d, %d and metatiles %d (out), %d (gap)" % (t_out, t_gap, 640 + n_meta, 640 + n_meta + 1))
    if not WRITE:
        print("  report only; pass --write")
        return None
    rows_needed = (t_gap // (tiles.width // 8)) + 1
    if rows_needed * 8 > tiles.height:
        grown = Image.new("P", (tiles.width, rows_needed * 8), 0)
        grown.putpalette(tiles.getpalette())
        grown.paste(tiles, (0, 0))
        tiles = grown
    for t, px in ((t_out, out), (t_gap, gap)):
        w = tiles.width // 8
        for y in range(8):
            for x in range(8):
                tiles.putpixel(((t % w) * 8 + x, (t // w) * 8 + y), px[y][x])
    tiles.save(os.path.join(SECONDARY, "tiles.png"), bits=4)
    new_meta = meta
    for t in (t_out, t_gap):
        e = entries[:]
        e[7] = (e[7] & ~0x3FF) | (640 + t)
        new_meta += struct.pack("<8H", *e)
    open(os.path.join(SECONDARY, "metatiles.bin"), "wb").write(new_meta)
    open(os.path.join(SECONDARY, "metatile_attributes.bin"), "wb").write(attrs + battr + battr)
    #  NOT THE LAYOUT. OneIsland_House2 draws LAYOUT_HOUSE3, which fifteen island houses share -- writing the shelf
    #  into its map.bin pulled a book out in all of them. The house's own map script sets (1,1) on load instead,
    #  to OUT or to GAP by FLAG_GOT_GUIDE (data/maps/OneIsland_House2/scripts.inc).
    print("  written: tiles, metatiles and attributes; the house's map script places them")
    return 640 + n_meta


if __name__ == "__main__":
    main()

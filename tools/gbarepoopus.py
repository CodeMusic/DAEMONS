#!/usr/bin/env python3
"""THE REPO's door, and OPUS's golden ticket (T-312, found playing, 2026-09-26).

    python3 tools/gbarepoopus.py            # report
    python3 tools/gbarepoopus.py --write    # LAYOUT_MART's floor, the doormat, and the ticket's metatile

THE SHELF IN FRONT OF THE DOOR. The REPO's plan (replanned 2026-09-15) put a small wooden unit at (4-5, 5-6),
square in front of the door, with the shelf-watcher standing beside it: walking in meant walking round it. The
user: "I don't think that shelf should be there, and OPUS should be on the first row of shelves to the right."
So the unit is floor now -- in every REPO, because all twelve share LAYOUT_MART and the shelf was in the way in all
of them -- and the doormat loses the shadow the unit cast on its top edge. Floor follows the room's own checker:
odd rows the 676/677 pair, even rows 686/687, the second of each pair on even columns.

THE TICKET. OPUS moves to the bottom end of the right-hand shelving, (8,6). The user asked for "some unusual symbol
that could make the user curious... a golden ticket shimmer on the shelf, removed once you pick it up": a small
gold card tucked over that bin's white label, one tan perforation pixel in it. It is a metatile of the REPO
tileset set by CALLOW's REPO's own map script until FLAG_GOT_OPUS, so no other REPO shows it.
"""
import os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
REPO = os.path.join(GBA, "data/tilesets/secondary/repo")
LAYOUT = os.path.join(GBA, "data/layouts/Mart/map.bin")
W = 11
FLOOR = {(4, 4): 687, (4, 5): 677, (5, 5): 676, (4, 6): 687, (5, 6): 686, (6, 7): 677}
UNIT = {(4, 5), (5, 5), (4, 6), (5, 6)}
#  the doormat's top row without the unit's shadow: the clean top tiles of its left end (0x314 edge, 0x315 middle)
MAT = {710: (0x7315, 0x7315, 0xA317, 0xA317), 711: (0x7315, 0x7714, 0xA317, 0x7716)}
BIN = 706                       # the right shelving's bottom end, at (8,6)
BIN_TILE = 0x30C                # its top-left tile: the bin's white label
TICKET = [(0, 3, 4), (0, 4, 4), (0, 5, 4), (0, 6, 4), (0, 7, 4),
          (1, 3, 4), (1, 4, 8), (1, 5, 4), (1, 6, 4), (1, 7, 4),
          (2, 3, 4), (2, 4, 4), (2, 5, 4), (2, 6, 4), (2, 7, 4)]   # (row, column, palette index): light gold, one tan


def main():
    bd = bytearray(open(LAYOUT, "rb").read())
    meta = bytearray(open(os.path.join(REPO, "metatiles.bin"), "rb").read())
    attrs = open(os.path.join(REPO, "metatile_attributes.bin"), "rb").read()
    tiles = Image.open(os.path.join(REPO, "tiles.png"))
    tw = tiles.width // 8
    at = lambda x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
    todo = [(xy, at(*xy) & 0x3FF, mt) for xy, mt in FLOOR.items() if at(*xy) & 0x3FF != mt]
    mat = [mt for mt, e in MAT.items() if struct.unpack_from("<4H", meta, (mt - 640) * 16) != e]
    n_meta = len(meta) // 16
    last = struct.unpack_from("<8H", meta, (n_meta - 1) * 16)
    base = struct.unpack_from("<8H", meta, (BIN - 640) * 16)
    has_ticket = last[1:] == base[1:] and last[0] != base[0]
    print("  floor: %d of %d tiles to lay (%s)" % (len(todo), len(FLOOR), ", ".join("%s" % (xy,) for xy, _, _ in todo) or "done"))
    print("  doormat: %s" % ("to clean: %s" % mat if mat else "clean"))
    print("  ticket: %s" % ("metatile %d" % (640 + n_meta - 1) if has_ticket else "to draw, as metatile %d" % (640 + n_meta)))
    if not WRITE:
        print("  report only; pass --write")
        return
    for xy, _, mt in todo:
        old = at(*xy)
        #  collision off where the unit stood; everything else keeps its bits
        new = (old & ~0x3FF) | mt
        if xy in UNIT:
            new &= ~(3 << 10)
        struct.pack_into("<H", bd, (xy[1] * W + xy[0]) * 2, new)
    open(LAYOUT, "wb").write(bytes(bd))
    for mt in mat:
        struct.pack_into("<4H", meta, (mt - 640) * 16, *MAT[mt])
    if not has_ticket:
        used = max(i for i in range(tw * (tiles.height // 8))
                   if any(tiles.getpixel(((i % tw) * 8 + x, (i // tw) * 8 + y)) for x in range(8) for y in range(8)))
        t = used + 1
        if t >= tw * (tiles.height // 8):
            grown = Image.new("P", (tiles.width, tiles.height + 8), 0)
            grown.putpalette(tiles.getpalette())
            grown.paste(tiles, (0, 0))
            tiles = grown
        src = BIN_TILE - 640
        for y in range(8):
            for x in range(8):
                tiles.putpixel(((t % tw) * 8 + x, (t // tw) * 8 + y),
                               tiles.getpixel(((src % tw) * 8 + x, (src // tw) * 8 + y)))
        for row, col, idx in TICKET:
            tiles.putpixel(((t % tw) * 8 + col, (t // tw) * 8 + row), idx)
        tiles.save(os.path.join(REPO, "tiles.png"), bits=4)
        e = list(base)
        e[0] = (e[0] & ~0x3FF) | (640 + t)
        meta += struct.pack("<8H", *e)
        attrs += attrs[(BIN - 640) * 4:(BIN - 640) * 4 + 4]
        open(os.path.join(REPO, "metatile_attributes.bin"), "wb").write(attrs)
        print("  ticket drawn as tile %d, metatile %d" % (640 + t, 640 + n_meta))
    open(os.path.join(REPO, "metatiles.bin"), "wb").write(bytes(meta))
    print("  written")


if __name__ == "__main__":
    main()

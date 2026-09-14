#!/usr/bin/env python3
"""Reclaim the tiles nothing draws from Blanche's tileset.

    python3 tools/gbacompact.py            # report
    python3 tools/gbacompact.py --write    # blank orphaned blocks, repack the tiles

T-53, T-55, T-58 and T-59 each drew INTO gTileset_PalletTown rather than over
it, and every one left what it replaced behind: vanilla's house and ground
tiles, and the blocks that drew them. With 342 of 384 slots gone, the next
redraw there has nowhere to go.

WHAT IS KEPT is what something can still reach:

  - every block drawn by ANY map that loads this tileset -- Blanche, and Route 1
    and Route 21 North, which draw a few of Blanche's blocks at their edges;
  - every block a script or the door code names by id (metatile_labels.h);
  - every tile those blocks draw, and the animated slots, which do not move:
    TilesetAnim_PalletTown writes its frames to slots 800..807 by number.

Every other block is blanked to zeros -- ids never shift, so nothing that names
a block by number can land on the wrong one -- and the surviving tiles are
packed down around the pinned slots, with every block's entries rewritten to
the new slots (flip bits and palette rows kept).
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
RULES = os.path.join(GBA, "tileset_rules.mk")
LABELS = os.path.join(GBA, "include/constants/metatile_labels.h")
TILESET = "gTileset_PalletTown"
PINNED = set(range(160, 168))          # anim/flower -> 800, anim/water -> 804
WRITE = "--write" in sys.argv


def main():
    layouts = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    metas = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    n_meta = len(metas) // 16
    tiles_img = Image.open(os.path.join(SD, "tiles.png")); tp = tiles_img.load()
    rules = open(RULES).read()
    rule = r"(secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )(\d+)"
    num_tiles = int(re.search(rule, rules).group(2))

    keep_blocks = set()
    for l in layouts:
        if l.get("secondary_tileset") != TILESET:
            continue
        for key in ("blockdata_filepath", "border_filepath"):
            data = open(os.path.join(GBA, l[key]), "rb").read()
            keep_blocks |= {struct.unpack_from("<H", data, i)[0] & 0x3FF for i in range(0, len(data), 2)}
    section = open(LABELS).read().split("// " + TILESET)[1].split("\n\n")[0]
    named = {int(v, 16) for v in re.findall(r"#define METATILE_\w+\s+0x([0-9A-Fa-f]+)", section)}
    keep_blocks |= named
    keep_blocks = {m for m in keep_blocks if 640 <= m < 640 + n_meta}

    used = set(PINNED)
    for m in keep_blocks:
        for t in struct.unpack_from("<8H", metas, (m - 640) * 16):
            if t & 0x3FF >= 640:
                used.add((t & 0x3FF) - 640)
    assert max(used) < num_tiles, "a kept block draws past -num_tiles"

    # pack: pinned slots stay, the rest fill from 0 upward around them
    order = sorted(used - PINNED)
    remap, nxt = {s: s for s in PINNED}, 0
    for s in order:
        while nxt in PINNED:
            nxt += 1
        remap[s] = nxt
        nxt += 1
    total = max(max(remap.values()) + 1, max(PINNED) + 1)

    orphan_blocks = [m for m in range(640, 640 + n_meta) if m not in keep_blocks and any(struct.unpack_from("<8H", metas, (m - 640) * 16))]
    print("  %d blocks reachable (%d named by id), %d orphaned blocks blanked" % (len(keep_blocks), len(named), len(orphan_blocks)))
    print("  %d tiles drawn of %d, packed to %d (%d slots freed)" % (len(used), num_tiles, total, num_tiles - total))

    new_img = Image.new("P", (128, ((total + 15) // 16) * 8)); new_img.putpalette(tiles_img.getpalette()); np_ = new_img.load()
    for old, new in remap.items():
        for i in range(64):
            np_[(new % 16) * 8 + i % 8, (new // 16) * 8 + i // 8] = tp[(old % 16) * 8 + i % 8, (old // 16) * 8 + i // 8]
    for m in range(640, 640 + n_meta):
        if m not in keep_blocks:
            struct.pack_into("<8H", metas, (m - 640) * 16, *([0] * 8))
            continue
        e = list(struct.unpack_from("<8H", metas, (m - 640) * 16))
        for i, t in enumerate(e):
            if t & 0x3FF >= 640:
                e[i] = (t & ~0x3FF) | (640 + remap[(t & 0x3FF) - 640])
        struct.pack_into("<8H", metas, (m - 640) * 16, *e)

    if WRITE:
        new_img.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(metas)
        open(RULES, "w").write(re.sub(rule, lambda mm: mm.group(1) + str(total), rules))
        print("  written: tiles.png, metatiles.bin, -num_tiles %d" % total)


main()

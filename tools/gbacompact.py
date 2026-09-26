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
    TilesetAnim_PalletTown writes its frames to slots 800..807 and 953..956
    by number.

THE ANIMATED SLOTS HOLD THEIR OWN FRAME 0, and only it. T-58 let the pond's lower
water tiles de-duplicate onto its upper two, so 806 and 807 were handed to birch
crowns -- and every animation tick painted water over the trees. Before packing,
any tile squatting in a pinned slot is moved out and its blocks repointed, frame
0 is written back, and the pond's bottom quadrants are pointed at 804 + quadrant.

Every other block is blanked to zeros -- ids never shift, so nothing that names
a block by number can land on the wrong one -- and the surviving tiles are
packed down around the pinned slots, with every block's entries rewritten to
the new slots (flip bits and palette rows kept).
"""
import json, os, re, struct, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driftguard import refuse_over_later_work

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
RULES = os.path.join(GBA, "tileset_rules.mk")
LABELS = os.path.join(GBA, "include/constants/metatile_labels.h")
TILESET = "gTileset_PalletTown"
PINNED = set(range(160, 168)) | set(range(313, 317))   # anim/flower -> 800, anim/water -> 804, anim/deep -> 953
ANIMS = {160: "flower", 164: "water", 313: "deep"}
WRITE = "--write" in sys.argv


def main():
    refuse_over_later_work("gbacompact")          # T-293: its files carry later work; generator_drift.json says what
    layouts = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    metas = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    n_meta = len(metas) // 16
    tiles_img = Image.open(os.path.join(SD, "tiles.png")); tp = tiles_img.load()
    rules = open(RULES).read()
    rule = r"(secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )(\d+)"
    num_tiles = int(re.search(rule, rules).group(2))

    # the animated slots: evict squatters, restore frame 0, point the pond at its own quadrants
    def tile(img_px, n):
        return tuple(img_px[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] for i in range(64))
    grown = Image.new("P", (128, max(tiles_img.height, ((num_tiles + 16) // 16) * 8)))
    grown.putpalette(tiles_img.getpalette()); grown.paste(tiles_img, (0, 0)); tp = grown.load()
    evicted = 0
    for first, name in ANIMS.items():
        frame = Image.open(os.path.join(SD, "anim", name, "0.png")).load()
        for q in range(4):
            want = tuple(frame[(q % 2) * 8 + i % 8, (q // 2) * 8 + i // 8] for i in range(64))
            slot_n = first + q
            if tile(tp, slot_n) == want:
                continue
            moved_to = num_tiles; num_tiles += 1; evicted += 1
            if (moved_to // 16) * 8 + 8 > grown.height:
                bigger = Image.new("P", (128, grown.height + 8)); bigger.putpalette(grown.getpalette()); bigger.paste(grown, (0, 0))
                grown = bigger; tp = grown.load()
            for i, v in enumerate(tile(tp, slot_n)):
                tp[(moved_to % 16) * 8 + i % 8, (moved_to // 16) * 8 + i // 8] = v
            for i, v in enumerate(want):
                tp[(slot_n % 16) * 8 + i % 8, (slot_n // 16) * 8 + i // 8] = v
            for m in range(n_meta):
                e = list(struct.unpack_from("<8H", metas, m * 16))
                is_pond = all(640 + 164 <= (t & 0x3FF) <= 640 + 167 for t in e[:4])
                for j, t in enumerate(e):
                    if (t & 0x3FF) == 640 + slot_n and not (name == "water" and is_pond and j < 4):
                        e[j] = (t & ~0x3FF) | (640 + moved_to)
                struct.pack_into("<8H", metas, m * 16, *e)
    for m in range(n_meta):
        e = list(struct.unpack_from("<8H", metas, m * 16))
        for first in (164, 313):                  # water and deep water animate by quadrant
            if all(640 + first <= (t & 0x3FF) <= 640 + first + 3 for t in e[:4]):
                e[:4] = [(t & ~0x3FF) | (640 + first + j) for j, t in enumerate(e[:4])]
                struct.pack_into("<8H", metas, m * 16, *e)
    tiles_img = grown
    print("  animated slots: %d squatters moved out, frame 0 restored" % evicted)

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

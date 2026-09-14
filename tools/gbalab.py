#!/usr/bin/env python3
"""Draw CRYSTAL CLEAR's lab, from outside, into Blanche (T-53, vision.md 9.22).

    python3 tools/gbalab.py            # preview to /tmp/lab_exterior.png
    python3 tools/gbalab.py --write    # tiles, metatiles, the map, the door
    python3 tools/gbalab.py --door     # the door animation alone, from the drawing

The design is 9.22's, from the concept drafts made with the n8n workflow's
kind: environment -- B's long symmetrical front and window rhythm, the front
elevation's flat slate roof, gold door frame, blank gold plate and stone plinth:

    pale stone walls, a flat slate roof with a parapet and a skylight, four
    tall two-pane windows on sills, and ONE line of gold -- the door frame and
    the plate above it. No lettering: the sign says her name; CLEAR belongs to
    the gold leaf at Quicksilver.

WHERE IT GOES, measured rather than assumed:

  THE FOOTPRINT is Blanche (13..19, 9..13): seven blocks by five. The top row
  is half grass, so the picture is 112x80 with its top eight rows transparent
  and the grass underneath left as it is.

  ALL THE ART IS THE TOP LAYER, in Blanche's own row 9 -- which already holds
  whites, greys, glass blues and five golds. Bottom layers are grass, exactly as
  vanilla's were.

  EVERY CELL GETS ITS OWN BLOCK. Vanilla reused one block across four roof
  cells, so a skylight in one would have appeared in all four. The new blocks
  are appended after the tileset's existing 89, each copying the attributes of
  the block it replaces, and the map is repointed with its collision and
  elevation bits kept. THE DOOR CELL KEEPS BLOCK 684: the warp and the door
  animation are both keyed to METATILE_PalletTown_OaksLabDoor.

  THE TILES ARE APPENDED, de-duplicated, after slot 76 -- the tileset holds 384
  and used 76 -- so nothing another block draws is repainted, and
  tileset_rules.mk's -num_tiles is raised to match.

  THE DOOR OPENS AS HER DOOR. The door is two cells tall, so the animation is
  too: graphics/door_anims/oaks_lab.png is three 16x32 frames (closed, half,
  open) cut from the door cell and the cell above it, and field_door.c plays
  it as DOOR_SIZE_1x2 in row 9. It was 16x16 at first, and only the lower half
  of the door opened. --door redraws it alone, since --write runs once.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
TS = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
PRIMARY = os.path.join(GBA, "data/tilesets/primary/general")
RULES = os.path.join(GBA, "tileset_rules.mk")
DOOR_PNG = os.path.join(GBA, "graphics/door_anims/oaks_lab.png")
PREVIEW = "/tmp/lab_exterior.png"
WRITE = "--write" in sys.argv
DOOR_ONLY = "--door" in sys.argv

NUM_TILES_IN_PRIMARY = NUM_METATILES_IN_PRIMARY = 640
SECONDARY_TILE_ROOM = 1024 - 640
ROW = 9
X0, Y0, COLS, ROWS = 13, 9, 7, 5              # the footprint, in blocks
DOOR_CELL = (16, 13)
DOOR_METATILE = 684                           # METATILE_PalletTown_OaksLabDoor
GRASS = 19 | (0 << 12)                        # the common ground tile, row 0
FIRST_NEW_SLOT = 76                           # the tileset's own -num_tiles

# Row 9, by index:
#   1 white stone   2 stone        3 stone line   4 plinth, parapet
#   5 slate light   6 slate        7 outline, dark slate
#   8 glass light   9 glass        10 glass dark
#   11..15 golds: 11 palest, 12 pale, 13 mid, 14 deep, 15 warm
W, H = COLS * 16, ROWS * 16


def draw():
    c = [[0] * W for _ in range(H)]

    def rect(x0, y0, x1, y1, v):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c[y][x] = v

    def hline(x0, x1, y, v):
        rect(x0, y, x1, y, v)

    def vline(x, y0, y1, v):
        rect(x, y0, x, y1, v)

    # --- the roof, seen from above: rows 8..39
    rect(0, 8, W - 1, 39, 7)                      # outline
    rect(1, 9, W - 2, 38, 4)                      # the parapet
    hline(1, W - 2, 9, 3)                         # its lit top edge
    rect(4, 12, W - 5, 34, 6)                     # the flat slate inside it
    hline(4, W - 5, 12, 7)                        # the parapet's inner shadow
    vline(4, 12, 34, 7)
    for y in (19, 27):                            # panel seams
        hline(5, W - 5, y, 5)
    # a flat skylight toward the back, off-centre as B's dormer was
    rect(70, 15, 93, 29, 7)
    rect(71, 16, 92, 28, 3)
    rect(73, 18, 90, 26, 9)
    for i in range(6):                            # one glint across the glass
        c[19 + i // 2][75 + i] = 8
    hline(73, 90, 26, 10)
    # the parapet's front lip, then the shadow it throws on the wall
    rect(1, 35, W - 2, 37, 4)
    hline(1, W - 2, 35, 3)
    hline(0, W - 1, 38, 5)
    hline(0, W - 1, 39, 7)

    # --- the wall: rows 40..79
    rect(0, 40, W - 1, H - 1, 7)
    rect(1, 40, W - 2, 71, 1)
    hline(1, W - 2, 40, 3)                        # the eave's shadow
    hline(1, W - 2, 41, 2)
    for i, y in enumerate((48, 56, 64)):          # stone courses, joints staggered
        hline(1, W - 2, y, 3)
        for x in range(4 + 6 * (i % 2), W - 2, 12):
            vline(x, y - 7, y - 1, 2)
    # the plinth
    rect(1, 72, W - 2, 77, 4)
    hline(1, W - 2, 72, 3)
    hline(1, W - 2, 77, 5)
    hline(0, W - 1, H - 1, 7)

    # --- four tall windows on sills, two panes each
    for x0 in (10, 28, 72, 90):
        x1 = x0 + 11
        rect(x0, 45, x1, 68, 6)                   # frame
        rect(x0 + 1, 46, x1 - 1, 67, 9)           # glass
        rect(x0 + 1, 46, x0 + 2, 49, 8)           # the light catches the corner
        hline(x0 + 1, x1 - 1, 56, 3)              # the mullion between panes
        hline(x0 + 1, x1 - 1, 67, 10)
        hline(x0 - 1, x1 + 1, 69, 3)              # the sill
        hline(x0 - 1, x1 + 1, 70, 4)

    # --- the door, the ONE line of gold, and the blank plate
    rect(50, 44, 61, 76, 14)                      # gold frame
    rect(51, 45, 60, 76, 13)
    rect(52, 46, 59, 76, 10)                      # the door itself, glazed
    rect(53, 47, 58, 75, 9)
    rect(53, 47, 54, 51, 8)
    vline(56, 47, 75, 10)                         # its two leaves
    c[62][58] = 12                                # the handle
    c[62][54] = 12
    rect(49, 77, 62, 78, 3)                       # the step
    rect(52, 41, 59, 43, 14)                      # the plate: gold, and blank
    hline(53, 58, 42, 12)
    return c


def door_frames(c):
    """Closed, half, open -- the door cell and the one above it, as drawn, then
    the leaves parting. 16x32 each: DOOR_SIZE_1x2 draws the pair."""
    dx, dy = (DOOR_CELL[0] - X0) * 16, (DOOR_CELL[1] - 1 - Y0) * 16
    cell = [row[dx:dx + 16] for row in c[dy:dy + 32]]
    frames = [cell]
    for gap in (2, 4):
        f = [r[:] for r in cell]
        for y in range(32):
            for x in range(16):
                gx = dx + x
                if 53 <= gx <= 58 and c[dy + y][gx] in (8, 9, 10):
                    if 56 - gap <= gx <= 55 + gap:
                        f[y][x] = 7                    # the room behind it is dark
        frames.append(f)
    for f in frames:                                   # a door frame is never see-through
        for y in range(32):
            for x in range(16):
                if f[y][x] == 0:
                    f[y][x] = 1
    return frames


def write_door(frames, p9):
    door = Image.new("P", (16, 96))
    door.putpalette([v for rgb in p9 for v in rgb] + [0] * 720)
    dp = door.load()
    for i, f in enumerate(frames):
        for y in range(32):
            for x in range(16):
                dp[x, i * 32 + y] = f[y][x]
    door.save(DOOR_PNG)


def pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    canvas = draw()
    if DOOR_ONLY:
        write_door(door_frames(canvas), pal(os.path.join(TS, "palettes/09.pal")))
        print("  written: %s, three 16x32 frames" % DOOR_PNG)
        return
    layout = [l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
              if l.get("name") == "PalletTown_Layout"][0]
    bd_path = os.path.join(GBA, layout["blockdata_filepath"])
    bd = bytearray(open(bd_path, "rb").read())
    Wmap = layout["width"]

    tiles_img = Image.open(os.path.join(TS, "tiles.png"))
    assert tiles_img.mode == "P", tiles_img.mode
    metas = bytearray(open(os.path.join(TS, "metatiles.bin"), "rb").read())
    attrs = bytearray(open(os.path.join(TS, "metatile_attributes.bin"), "rb").read())
    n_meta = len(metas) // 16
    per_attr = len(attrs) // n_meta

    # Already applied? The lab's cells then point past the vanilla block count.
    first_cell = struct.unpack_from("<H", bd, (Y0 * Wmap + X0) * 2)[0] & 0x3FF
    if first_cell >= 640 + 89 and WRITE:
        raise SystemExit("  the lab is already drawn in (cell 13,9 is block %d); restore the files to redraw" % first_cell)

    # Cut the picture into 8x8 tiles, de-duplicated.
    slots, new_tiles = {}, []
    def tile_at(px, py):
        key = tuple(canvas[py + y][px + x] for y in range(8) for x in range(8))
        if not any(key):
            return 0                                   # fully transparent: tile 0
        if key not in slots:
            slots[key] = FIRST_NEW_SLOT + len(new_tiles)
            new_tiles.append(key)
        return (NUM_TILES_IN_PRIMARY + slots[key]) | (ROW << 12)

    cell_meta = {}
    for cy in range(ROWS):
        for cx in range(COLS):
            x, y = X0 + cx, Y0 + cy
            raw = struct.unpack_from("<H", bd, (y * Wmap + x) * 2)[0]
            old = raw & 0x3FF
            old_entries = struct.unpack_from("<8H", metas, (old - 640) * 16)
            bottom = list(old_entries[:4]) if cy == 0 else [GRASS] * 4   # the half-grass top row keeps its grass
            top = [tile_at(cx * 16 + tx * 8, cy * 16 + ty * 8) for ty in (0, 1) for tx in (0, 1)]
            cell_meta[(x, y)] = (old, raw, bottom + top)

    total_tiles = FIRST_NEW_SLOT + len(new_tiles)
    assert total_tiles <= SECONDARY_TILE_ROOM, "the tileset holds %d tiles" % SECONDARY_TILE_ROOM
    new_blocks = sum(1 for k in cell_meta if k != DOOR_CELL)
    print("  %d new tiles (slots %d..%d), %d new blocks (%d..%d), door stays block %d"
          % (len(new_tiles), FIRST_NEW_SLOT, total_tiles - 1, new_blocks, 640 + n_meta, 640 + n_meta + new_blocks - 1, DOOR_METATILE))

    # The tiles image, grown to hold them.
    rows_needed = (total_tiles + 15) // 16
    grown = Image.new("P", (128, max(tiles_img.height, rows_needed * 8)))
    grown.putpalette(tiles_img.getpalette())
    grown.paste(tiles_img, (0, 0))
    gp = grown.load()
    for key, slot in slots.items():
        sx, sy = (slot % 16) * 8, (slot // 16) * 8
        for i, v in enumerate(key):
            gp[sx + i % 8, sy + i // 8] = v

    # Blocks: the door's is rewritten in place; every other cell gets a new one.
    next_id = 640 + n_meta
    for (x, y), (old, raw, entries) in sorted(cell_meta.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if (x, y) == DOOR_CELL:
            struct.pack_into("<8H", metas, (DOOR_METATILE - 640) * 16, *entries)
            continue
        metas += struct.pack("<8H", *entries)
        attrs += attrs[(old - 640) * per_attr:(old - 640 + 1) * per_attr]
        struct.pack_into("<H", bd, (y * Wmap + x) * 2, (raw & ~0x3FF) | next_id)
        next_id += 1

    # Preview: the lab in its place, on row 9 and the grass under it.
    p9 = pal(os.path.join(TS, "palettes/09.pal"))
    prim_tiles = Image.open(os.path.join(PRIMARY, "tiles.png")); prim_meta = open(os.path.join(PRIMARY, "metatiles.bin"), "rb").read()
    pals = {n: pal(os.path.join(PRIMARY if n < 7 else TS, "palettes/%02d.pal" % n)) for n in range(13)}
    view = Image.new("RGB", ((COLS + 2) * 16, (ROWS + 2) * 16)); vp = view.load()
    for yy in range(ROWS + 2):
        for xx in range(COLS + 2):
            mx, my = X0 - 1 + xx, Y0 - 1 + yy
            m = struct.unpack_from("<H", bd, (my * Wmap + mx) * 2)[0] & 0x3FF
            src, k = (prim_meta, m) if m < 640 else (metas, m - 640)
            e = struct.unpack_from("<8H", src, k * 16)
            for layer in (0, 1):
                for q in range(4):
                    t = e[layer * 4 + q]; idx = t & 0x3FF; p = (t >> 12) & 0xF
                    img, i = (prim_tiles, idx) if idx < 640 else (grown, idx - 640)
                    ip = img.load()
                    for ty in range(8):
                        for tx in range(8):
                            sx, sy = (i % 16) * 8 + (tx if not (t >> 10) & 1 else 7 - tx), (i // 16) * 8 + (ty if not (t >> 11) & 1 else 7 - ty)
                            v = ip[sx, sy] if sy < img.height else 0
                            if layer and v == 0:
                                continue
                            vp[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = pals.get(p, pals[0])[v]
    frames = door_frames(canvas)
    strip = Image.new("RGB", (16 * 3 + 8, 32), (40, 40, 40))
    for i, f in enumerate(frames):
        for y in range(32):
            for x in range(16):
                strip.putpixel((i * 19 + x, y), p9[f[y][x]])
    sheet = Image.new("RGB", (view.width * 4, view.height * 4 + 32 * 4 + 8), (40, 40, 40))
    sheet.paste(view.resize((view.width * 4, view.height * 4), Image.NEAREST), (0, 0))
    sheet.paste(strip.resize((strip.width * 4, 128), Image.NEAREST), (0, view.height * 4 + 8))
    sheet.save(PREVIEW)
    print("  preview %s" % PREVIEW)

    if WRITE:
        grown.save(os.path.join(TS, "tiles.png"))
        open(os.path.join(TS, "metatiles.bin"), "wb").write(metas)
        open(os.path.join(TS, "metatile_attributes.bin"), "wb").write(attrs)
        open(bd_path, "wb").write(bd)
        write_door(frames, p9)
        rules = open(RULES).read()
        new_rules, n = re.subn(r"(secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+",
                               lambda m: m.group(1) + str(total_tiles), rules)
        assert n == 1, "tileset_rules.mk rule for pallet_town not found"
        open(RULES, "w").write(new_rules)
        print("  written: tiles.png, metatiles.bin, metatile_attributes.bin, PalletTown map.bin, oaks_lab door, -num_tiles %d" % total_tiles)


main()

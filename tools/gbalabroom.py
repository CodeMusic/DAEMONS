#!/usr/bin/env python3
"""Draw CRYSTAL CLEAR's lab, from inside (T-57, vision.md 9.22).

    python3 tools/gbalabroom.py            # preview to /tmp/lab_room.png (before | after)
    python3 tools/gbalabroom.py --write    # gTileset_BlancheLab, rebuilt; the room repointed

The design is 9.22's, from the n8n interior drafts -- A's layout, angle and
pale palette, with B's lived-in details:

    a working lab, lived in. Pale plaster and a pale stone floor. The computer
    on the back wall; a desk of loose papers and an open notebook; two plain
    posters; the INDEX unit with a gold trim and her note pinned to it; tall
    shelves of journals. Oak's red machine is the PORT -- a cabinet of docking
    slots, two grey BOXES in it, cables to the wall. A work bench for the three
    boxes. Low shelves crammed with worn journals. Two plants and a mat.

EVERY PIECE STAYS ON ITS TILE, so the computer, the posters, the INDEX unit and
her note, the bench, the people, the walls and the exit keep their scripts and
collision. The block ATTRIBUTES are copied cell by cell, so the behaviours come
along: the computer, the two signposts, the shelves' MB_BOOKSHELF, the exit.

ONE TILE, ONE PALETTE ROW. Walls and floor use only the six neutrals every row
shares (indices 1..6), and each object family has its own row:

    row 7   computer, posters, INDEX unit, the gold trim, the note
    row 8   shelves and journals
    row 9   the desk, its papers, the notebook
    row 10  the PORT and its boxes and cables, the bench
    row 11  plants and the mat

so a tile an object shares with the floor still resolves to one row, and a tile
where two object rows meet is refused rather than miscoloured.

WHAT DRAWS OVER THE PLAYER is vanilla's, cell by cell: where a block's layer
type is 0 and its top layer held art (the PORT's top edge, the low shelves'
tops), the object's pixels there go in the top layer over the floor. Everything
else is composited into the bottom layer.

THE TILESET IS REBUILT, not appended to. It is this room's alone since T-54,
no script names or changes one of its blocks, and the room needs more tiles
than the old tileset had free.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/building")
SD = os.path.join(GBA, "data/tilesets/secondary/blanche_lab")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/lab_room.png"
WRITE = "--write" in sys.argv

CORE = [(250, 248, 242), (230, 226, 216), (208, 202, 190), (172, 166, 156), (116, 110, 108), (56, 52, 60)]
ROWS = {
    7:  [(236, 228, 204), (70, 72, 90), (40, 52, 64), (120, 196, 180), (190, 236, 220), (240, 214, 120), (212, 170, 72), (150, 112, 40), (246, 236, 180)],
    8:  [(214, 180, 132), (180, 140, 96), (130, 96, 64), (54, 70, 110), (120, 78, 52), (122, 52, 60), (60, 98, 74), (96, 112, 134), (214, 202, 170)],
    9:  [(214, 180, 132), (180, 140, 96), (130, 96, 64), (252, 250, 244), (222, 216, 198), (60, 80, 130), (120, 78, 52), (170, 60, 60), (236, 228, 204)],
    10: [(190, 196, 204), (140, 148, 160), (86, 94, 108), (30, 32, 38), (110, 220, 140), (240, 180, 70), (60, 90, 110), (214, 180, 132), (130, 96, 64)],
    11: [(140, 196, 120), (88, 150, 86), (52, 100, 62), (206, 140, 100), (160, 98, 70), (110, 64, 48), (190, 168, 120), (150, 124, 84), (104, 84, 60)],
}
W, H = 13 * 16, 14 * 16


def palette(row):
    return [(255, 0, 255)] + CORE + ROWS[row]


def draw():
    base = [[2] * W for _ in range(H)]
    obj = [[None] * W for _ in range(H)]          # (row, index) or None

    def b_rect(x0, y0, x1, y1, v):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                base[y][x] = v

    def o_rect(row, x0, y0, x1, y1, v):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                obj[y][x] = (row, v)

    def o_px(row, x, y, v):
        if 0 <= x < W and 0 <= y < H:
            obj[y][x] = (row, v)

    # ------------------------------------------------------------ the room
    # the floor: pale stone, one slab per block, faint grout, a lit corner
    for cy in range(2, 13):
        for cx in range(13):
            x0, y0 = cx * 16, cy * 16
            b_rect(x0, y0, x0 + 15, y0 + 15, 2)
            b_rect(x0, y0 + 15, x0 + 15, y0 + 15, 3)
            b_rect(x0 + 15, y0, x0 + 15, y0 + 15, 3)
            if (cx * 3 + cy * 5) % 7 == 0:          # a worn slab here and there
                b_rect(x0 + 4, y0 + 9, x0 + 6, y0 + 9, 3)
            base[y0 + 1][x0 + 1] = 1
    # the back wall: plaster, a picture rail, a skirting board, its shadow
    b_rect(0, 0, W - 1, 31, 2)
    b_rect(0, 0, W - 1, 1, 6)
    b_rect(0, 2, W - 1, 3, 4)
    b_rect(0, 14, W - 1, 14, 3)
    b_rect(0, 27, W - 1, 27, 4)
    b_rect(0, 28, W - 1, 30, 5)
    b_rect(0, 31, W - 1, 31, 6)
    b_rect(0, 32, W - 1, 35, 4)
    # the side walls, a sliver each side
    b_rect(0, 0, 2, H - 17, 5)
    b_rect(0, 0, 0, H - 17, 6)
    b_rect(W - 3, 0, W - 1, H - 17, 5)
    b_rect(W - 1, 0, W - 1, H - 17, 6)
    # the front wall, and the doorway at 5..7
    b_rect(0, H - 16, W - 1, H - 1, 5)
    b_rect(0, H - 16, W - 1, H - 15, 4)
    b_rect(0, H - 1, W - 1, H - 1, 6)
    b_rect(80, H - 16, 127, H - 1, 3)

    # ------------------------------------------------------------ the back wall
    R = 7   # the computer, on a grey counter
    o_rect(R, 16, 18, 63, 29, 3)               # counter
    o_rect(R, 16, 18, 63, 18, 6)
    o_rect(R, 16, 26, 63, 29, 5)
    o_rect(R, 20, 4, 43, 19, 6)                # monitor
    o_rect(R, 21, 5, 42, 17, 3 + 6)            # screen (index 9: dark)
    for y in (7, 10, 13):
        o_rect(R, 23, y, 23 + (14 if y != 10 else 9), y, 10)
    o_rect(R, 23, 7, 26, 7, 11)
    o_rect(R, 28, 20, 34, 22, 5)               # its stand
    o_rect(R, 46, 21, 60, 24, 4)               # the keyboard
    for x in range(47, 60, 3):
        o_px(R, x, 22, 1)
    o_rect(R, 50, 8, 58, 17, 4)                # a second unit, humming
    o_px(R, 56, 10, 10)
    o_px(R, 56, 13, 12)

    R = 9   # the desk, lived in
    o_rect(R, 64, 16, 95, 29, 8)
    o_rect(R, 64, 16, 95, 17, 7)
    o_rect(R, 64, 27, 95, 29, 9)
    o_rect(R, 64, 16, 64, 29, 6)
    o_rect(R, 95, 16, 95, 29, 6)
    for x0, y0, x1, y1 in ((66, 18, 74, 24), (71, 20, 79, 26), (86, 18, 93, 23)):
        o_rect(R, x0, y0, x1, y1, 10)          # loose papers
        o_rect(R, x0, y1, x1, y1, 11)
        for y in range(y0 + 2, y1, 2):
            o_rect(R, x0 + 1, y, x1 - 2, y, 12)
    o_rect(R, 80, 19, 91, 25, 13)              # an open notebook
    o_rect(R, 81, 20, 85, 24, 10)
    o_rect(R, 86, 20, 90, 24, 10)
    o_rect(R, 86, 20, 86, 24, 11)
    for y in (21, 23):
        o_rect(R, 82, y, 84, y, 12)
        o_rect(R, 87, y, 89, y, 12)
    o_px(R, 76, 18, 14)                        # a red pencil

    R = 7   # two plain posters
    for x0 in (98, 114):
        o_rect(R, x0, 6, x0 + 12, 24, 5)
        o_rect(R, x0 + 1, 7, x0 + 11, 23, 7)
        o_rect(R, x0 + 3, 9, x0 + 9, 9, 8)
        for y in (13, 16, 19):
            o_rect(R, x0 + 3, y, x0 + 9, y, 4)

    R = 7   # the INDEX unit, the gold, and the note pinned to it
    o_rect(R, 130, 5, 142, 25, 6)
    o_rect(R, 131, 6, 141, 24, 3)
    o_rect(R, 131, 6, 141, 7, 13)              # gold trim, top
    o_rect(R, 131, 23, 141, 24, 14)            # and below
    o_rect(R, 131, 8, 141, 8, 12)
    o_rect(R, 133, 11, 139, 16, 9)             # its window
    o_rect(R, 134, 12, 136, 13, 10)
    o_rect(R, 138, 17, 143, 25, 15)            # the note
    o_rect(R, 138, 17, 143, 17, 4)
    o_px(R, 140, 16, 6)                        # its pin
    for y in (19, 21, 23):
        o_rect(R, 139, y, 142, y, 8)

    R = 8   # tall shelves of journals
    o_rect(R, 146, 3, 205, 30, 9)
    o_rect(R, 147, 4, 204, 29, 8)
    shelf_colours = [10, 11, 12, 13, 14, 15, 11, 10, 13, 12]
    for sy in (5, 18):
        o_rect(R, 148, sy + 11, 203, sy + 12, 7)
        x, k = 148, 0
        while x < 203:
            wdt = 2 + (k * 7) % 3
            top = sy + (k * 5) % 3
            o_rect(R, x, top, min(202, x + wdt - 1), sy + 10, shelf_colours[k % len(shelf_colours)])
            o_rect(R, x, top, min(202, x + wdt - 1), top, 6)
            x += wdt + 1
            k += 1

    # ------------------------------------------------------------ the PORT
    R = 10
    for x in (6, 9):                           # cables down from the wall
        o_rect(R, x, 36, x, 58 + (x - 6), 9)
    o_rect(R, 6, 58, 17, 58, 9)
    o_rect(R, 9, 61, 17, 61, 9)
    o_rect(R, 17, 54, 46, 95, 6)               # the cabinet
    o_rect(R, 18, 55, 45, 94, 8)
    o_rect(R, 18, 55, 45, 62, 7)               # its top, catching the light
    o_rect(R, 18, 63, 45, 63, 9)
    slots = ((21, 67), (33, 67), (21, 80), (33, 80))
    for i, (sx, sy) in enumerate(slots):
        o_rect(R, sx, sy, sx + 9, sy + 9, 9)   # a docking slot
        o_rect(R, sx + 1, sy + 1, sx + 8, sy + 8, 10)
        if i in (0, 3):                        # a BOX, docked
            o_rect(R, sx + 1, sy + 1, sx + 8, sy + 8, 7)
            o_rect(R, sx + 2, sy + 2, sx + 7, sy + 5, 13)
            o_px(R, sx + 6, sy + 7, 11)
        else:
            o_px(R, sx + 4, sy + 8, 12)        # empty: an amber light waits
    o_rect(R, 18, 92, 45, 94, 9)

    # ------------------------------------------------------------ the bench
    R = 10
    o_rect(R, 128, 66, 175, 78, 15)
    o_rect(R, 129, 67, 174, 76, 14)
    o_rect(R, 129, 67, 174, 67, 7)
    o_rect(R, 128, 78, 175, 82, 15)
    for lx in (131, 170):
        o_rect(R, lx, 83, lx + 3, 93, 15)

    # ------------------------------------------------------------ low shelves of worn journals
    R = 8
    for x0, x1 in ((3, 79), (128, 204)):
        o_rect(R, x0, 120, x1, 127, 7)         # the top, from above
        o_rect(R, x0, 120, x1, 120, 6)
        o_rect(R, x0, 126, x1, 127, 8)
        o_rect(R, x0, 128, x1, 143, 9)         # the front
        for sy in (129, 136):
            x, k = x0 + 2, (x0 // 3)
            while x < x1 - 1:
                wdt = 2 + (k * 5) % 2
                top = sy + (k * 3) % 2
                o_rect(R, x, top, min(x1 - 2, x + wdt - 1), sy + 5, shelf_colours[k % len(shelf_colours)])
                x += wdt + 1
                k += 1
            o_rect(R, x0, sy + 6, x1, sy + 6, 8)
        for y in range(144, 148):
            for x in range(x0, x1 + 1):
                obj[y][x] = None
                base[y][x] = 4

    # ------------------------------------------------------------ plants and the mat
    R = 11   # two potted plants: a terracotta pot with a lip, a full crown of leaves
    for px0 in (1, W - 16):
        o_rect(R, px0 + 4, 200, px0 + 11, 207, 11)          # the pot
        o_rect(R, px0 + 10, 201, px0 + 11, 207, 12)         # its shaded side
        o_rect(R, px0 + 5, 207, px0 + 10, 207, 12)
        o_rect(R, px0 + 3, 198, px0 + 12, 200, 10)          # its lip
        o_rect(R, px0 + 3, 200, px0 + 12, 200, 12)
        blobs = ((8, 193, 4.2), (4, 195, 3.2), (12, 195, 3.2), (5, 189, 3.2), (11, 189, 3.2), (8, 186, 2.6))
        inside = lambda x, y: any((x - bx) ** 2 + (y - by) ** 2 <= r * r for bx, by, r in blobs)
        for y in range(180, 200):
            for lx in range(0, 16):
                if not inside(lx, y):
                    continue
                edge = not all(inside(lx + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if edge:
                    c = 9
                else:
                    near = min(blobs, key=lambda bl: (lx - bl[0]) ** 2 + (y - bl[1]) ** 2)
                    c = 7 if (lx - near[0]) + (y - near[1]) < -1 else 8
                o_px(R, px0 + lx, y, c)
        for lx, y in ((8, 190), (8, 191), (5, 192), (11, 192), (8, 196)):   # where leaves overlap
            o_px(R, px0 + lx, y, 9)
    o_rect(R, 84, 194, 123, 206, 15)
    o_rect(R, 85, 195, 122, 205, 14)
    o_rect(R, 88, 199, 119, 200, 13)
    return base, obj


def pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, colours):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in colours]
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


def main():
    base, obj = draw()
    layout = [l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
              if l.get("name") == "PalletTown_ProfessorOaksLab_Layout"][0]
    assert layout["secondary_tileset"] == "gTileset_BlancheLab", "T-54 first"
    # it reads vanilla's layering off the blocks it replaces, so it runs once
    if WRITE and pal(os.path.join(SD, "palettes/07.pal")) == palette(7):
        raise SystemExit("  already drawn: the room's blocks are this tool's, not vanilla's (git checkout blanche_lab and the map to redraw)")
    bd_path = os.path.join(GBA, layout["blockdata_filepath"]); bd = bytearray(open(bd_path, "rb").read())
    border_path = os.path.join(GBA, layout["border_filepath"]); border = open(border_path, "rb").read()
    Wm, Hm = layout["width"], layout["height"]
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    pattr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    old_meta = open(os.path.join(SD, "metatiles.bin"), "rb").read()
    old_attr = open(os.path.join(SD, "metatile_attributes.bin"), "rb").read()
    border_ids = [struct.unpack_from("<H", border, i * 2)[0] & 0x3FF for i in range(len(border) // 2)]
    print("  border blocks:", border_ids)
    assert all(b < 640 for b in border_ids), "the border draws this tileset's own blocks; handle it before rebuilding"

    def old(m):
        if m < 640:
            return struct.unpack_from("<8H", prim, m * 16), pattr[m * 4:(m + 1) * 4]
        return struct.unpack_from("<8H", old_meta, (m - 640) * 16), old_attr[(m - 640) * 4:(m - 639) * 4]

    tiles, tile_slot = [bytes(64)], {bytes(64): 0}
    def add_tile(px):
        key = bytes(px)
        if key not in tile_slot:
            tile_slot[key] = len(tiles)
            tiles.append(key)
        return tile_slot[key]

    def quadrant(cx, cy, q, layer):
        """layer 'base+obj' composite, 'base' only, or 'obj' only; returns (pixels, row)."""
        x0, y0 = cx * 16 + (q % 2) * 8, cy * 16 + (q // 2) * 8
        rows, px = set(), []
        for y in range(y0, y0 + 8):
            for x in range(x0, x0 + 8):
                o = obj[y][x]
                if o is not None and layer != "base":
                    rows.add(o[0]); px.append(o[1])
                elif layer == "obj":
                    px.append(0)
                else:
                    px.append(base[y][x])
        if len(rows) > 1:
            raise SystemExit("  !! cell (%d,%d) quadrant %d mixes palette rows %s" % (cx, cy, q, sorted(rows)))
        return px, (rows.pop() if rows else 7)

    metas, attrs, meta_id = [], [], {}
    for cy in range(Hm):
        for cx in range(Wm):
            raw = struct.unpack_from("<H", bd, (cy * Wm + cx) * 2)[0]
            e, a = old(raw & 0x3FF)
            layer_type = (struct.unpack("<I", a)[0] >> 29) & 7
            entries = [0] * 8
            for q in range(4):
                over = layer_type == 0 and (e[4 + q] & 0x3FF)
                if over:
                    px, row = quadrant(cx, cy, q, "base")
                    entries[q] = (640 + add_tile(px)) | (7 << 12)
                    opx, orow = quadrant(cx, cy, q, "obj")
                    entries[4 + q] = ((640 + add_tile(opx)) | (orow << 12)) if any(opx) else 0
                else:
                    px, row = quadrant(cx, cy, q, "base+obj")
                    entries[q] = (640 + add_tile(px)) | (row << 12)
            key = (tuple(entries), bytes(a))
            if key not in meta_id:
                meta_id[key] = 640 + len(metas)
                metas.append(entries); attrs.append(bytes(a))
            struct.pack_into("<H", bd, (cy * Wm + cx) * 2, (raw & ~0x3FF) | meta_id[key])

    assert len(tiles) <= 384 and len(metas) <= 384, (len(tiles), len(metas))
    print("  %d tiles, %d blocks (the room is %d cells)" % (len(tiles), len(metas), Wm * Hm))

    tiles_img = Image.new("P", (128, ((len(tiles) + 15) // 16) * 8))
    tp = tiles_img.load()
    for n, t in enumerate(tiles):
        for i, v in enumerate(t):
            tp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] = v
    flat = [c for col in palette(7) for c in col]
    tiles_img.putpalette(flat + [0] * (768 - len(flat)))

    # preview: the room before, and after, as the tiles and palettes will draw it
    pals_new = {r: palette(r) for r in ROWS}
    def render_new():
        img = Image.new("RGB", (Wm * 16, Hm * 16)); o = img.load()
        for cy in range(Hm):
            for cx in range(Wm):
                m = struct.unpack_from("<H", bd, (cy * Wm + cx) * 2)[0] & 0x3FF
                e = metas[m - 640]
                for layer in (0, 1):
                    for q in range(4):
                        t = e[layer * 4 + q]
                        if layer and not t:
                            continue
                        key = tiles[(t & 0x3FF) - 640]; p = pals_new.get((t >> 12) & 0xF, pals_new[7])
                        for i, v in enumerate(key):
                            if layer and v == 0:
                                continue
                            o[cx * 16 + (q % 2) * 8 + i % 8, cy * 16 + (q // 2) * 8 + i // 8] = p[v]
        return img
    after = render_new()
    before_path = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/crystal_lab_interior_x2.png"
    sheet = Image.new("RGB", (Wm * 16 * 2 + 8, Hm * 16), (30, 30, 30))
    if os.path.exists(before_path):
        sheet.paste(Image.open(before_path).convert("RGB").resize((Wm * 16, Hm * 16)), (0, 0))
    sheet.paste(after, (Wm * 16 + 8, 0))
    sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(PREVIEW)
    print("  preview %s" % PREVIEW)

    if WRITE:
        tiles_img.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(b"".join(struct.pack("<8H", *e) for e in metas))
        open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(b"".join(attrs))
        open(bd_path, "wb").write(bd)
        for r in ROWS:
            write_pal(os.path.join(SD, "palettes/%02d.pal" % r), palette(r))
        rules = open(RULES).read()
        rules, n = re.subn(r"(secondary/blanche_lab/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+",
                           lambda mm: mm.group(1) + str(len(tiles)), rules)
        assert n == 1
        open(RULES, "w").write(rules)
        print("  written: tiles.png, metatiles.bin, attributes, palettes 07..11, the room's map.bin, -num_tiles %d" % len(tiles))


main()

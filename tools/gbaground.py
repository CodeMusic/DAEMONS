#!/usr/bin/env python3
"""Draw Blanche's ground (T-58, vision.md 9.22).

    python3 tools/gbaground.py            # preview to /tmp/blanche_ground.png (now | after)
    python3 tools/gbaground.py --write    # Blanche's tiles, blocks, rows 7 and 12, anims, border

The design is 9.22's, from the n8n terrain drafts -- B's shapes, A's colours:

    short silver-green grass almost white at the tips, white chalk paths,
    round white-barked birches seen from above, white daisies in the bed,
    and a clear pale pond with a rim of pale stone.

THE GROUND IS DERIVED FROM VANILLA'S, pixel by pixel. Every tile Blanche's ground
draws is read back through its own palette and each colour is given a job --
grass, a light or dark tuft, path, a speck, the path's shaded edge -- so every
curve of every path and every grass plot around the houses keeps vanilla's
shape, and only the colours of the jobs change. Three things are not recoloured
but drawn new, because a pale conifer is still a conifer: the birches (one per
2x2 tree, inside its own box), the daisies, and the pond's water and rim.

NOTHING SHARED IS REDRAWN. The ground blocks are mostly the General tileset's,
drawn by about 180 maps, so every tile is drawn fresh into Blanche's tileset and
every block that changes is either one of Blanche's own (rewritten in place, so
the door cells keep the block ids field_door.c animates) or a copy of a common
one. The border's four tree blocks are pointed at the copies too.

TWO ROWS. Row 7 is the ground, the pond and the flowers; row 12 is the birches.
Their indices 1..8 are the same eight ground colours, so a tile where a tree
stands on grass or a daisy on the path still resolves to one row. Route 1 and
Route 21 North load this tileset too, and the tool refuses to write if either
draws rows 7 or 12.

WHAT DRAWS OVER THE PLAYER is vanilla's quadrant by quadrant: where a block had
top-layer art, the new art goes in the top layer; everything else is composited
into the bottom.

THE FLOWERS AND THE WATER MOVE. The shared ones animate General's slots, which
Blanche no longer draws, so their frames are written to anim/flower and
anim/water and TilesetAnim_PalletTown copies them to slots 800 and 804.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/blanche_ground.png"
WRITE = "--write" in sys.argv

GROUND_COLOURS = [(196, 212, 186), (230, 238, 222), (172, 192, 166), (140, 162, 138),
                  (238, 238, 230), (252, 252, 248), (218, 218, 208), (214, 222, 204)]
ROW7 = [(255, 0, 255)] + GROUND_COLOURS + [(84, 90, 96), (214, 230, 234), (186, 210, 220), (152, 184, 202),
                                           (230, 228, 222), (180, 178, 172), (132, 132, 120)]
ROW12 = [(255, 0, 255)] + GROUND_COLOURS + [(84, 90, 96), (246, 246, 242), (226, 236, 222), (196, 214, 196),
                                            (160, 182, 164), (124, 146, 130), (70, 74, 80)]
GRASS, TIP, TUFT, DARK, CHALK, SPECK, SHADE, EDGE = range(1, 9)
OUTLINE, WATER, RIPPLE, DEEP, STONE, JOINT, EYE = range(9, 16)          # row 7
BARK, LEAF_L, LEAF_M, LEAF_D, LEAF_X, BAND = range(10, 16)               # row 12

GROUND_ROWS = {0, 1, 4, 6, 11, 12}
TREE_BLOCKS = {14, 15, 20, 21, 22, 23, 28, 29, 30, 31, 36, 37, 38, 39}
TREE_ANCHORS = {14, 28, 30}
FLOWER_BLOCK, SIGN_BLOCK = 4, 3
POND_BLOCKS = {291, 298, 299, 300, 721, 722}
# vanilla's colour -> its job, per palette row
JOBS = {11: {12: CHALK, 5: SPECK, 6: SHADE, 7: EDGE, 8: EDGE, 13: GRASS},
        0: {13: GRASS, 12: TIP, 14: TUFT, 15: DARK, 8: EDGE, 1: TIP, 2: GRASS, 3: TUFT, 4: DARK}}
SLOT_FLOWER, SLOT_WATER = 160, 164                                        # 800 and 804
FLOWER_FRAMES, WATER_FRAMES = 4, 8


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, colours):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in colours]
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


def water(x, y, f):
    u, v = (x + 2 * f) % 16, y % 16
    if (v == 3 and 1 <= u <= 6) or (v == 11 and 9 <= u <= 14):
        return RIPPLE
    if (v == 4 and 3 <= u <= 5) or (v == 12 and 11 <= u <= 13):
        return DEEP
    if (u, v) in ((12, 6), (4, 14)):
        return SPECK
    return WATER


def daisies(f):
    """one cell of the bed, frame f: {(x, y): (row, index)} in cell coordinates.
    Three full heads and a bud: white petals two pixels out, a grey ring to hold
    them against pale grass, a dark eye, dark leaves -- bold at 16x16."""
    px = {}
    for k, (cx, cy, big) in enumerate(((4, 4, True), (11, 6, True), (6, 11, True), (13, 13, False))):
        for dx, dy in ((0, 3), (0, 4)):
            px[(cx + dx, cy + dy)] = (7, TUFT)                            # the stem stays put
        for dx in (-2, -1, 1, 2):
            px[(cx + dx, cy + 3 + (abs(dx) == 1))] = (7, DARK)            # leaves
        cx += (0, 1, 0, -1)[(f + k) % 4] if big else 0                    # the head sways
        r = 2 if big else 1
        petals = {(cx + dx, cy + dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1)
                  if 0 < abs(dx) + abs(dy) <= r + (big and 0)} | ({(cx + dx, cy + dy) for dx in (-1, 1) for dy in (-1, 1)} if big else set())
        ring = {(x + dx, y + dy) for (x, y) in petals for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - petals - {(cx, cy)}
        for c in ring:
            px[c] = (7, JOINT)
        for c in petals:
            px[c] = (7, SPECK)
        px[(cx, cy)] = (7, EYE)
    return {(x, y): c for (x, y), c in px.items() if 0 <= x < 16 and 0 <= y < 16}


def birch():
    """one tree in its 32x32 box: {(x, y): index} in row 12"""
    px = {}
    for y in range(22, 31):                                                # the trunk, below the crown
        px[(14, y)] = OUTLINE
        px[(17, y)] = LEAF_X
        for x in (15, 16):
            px[(x, y)] = BAND if (y, x) in ((24, 15), (25, 15), (27, 16), (28, 16)) else BARK
    for x in range(10, 22):                                                # its shadow
        px[(x, 31)] = DARK
    for x in (11, 12, 19, 20):
        px[(x, 30)] = DARK
    lobes = ((16, 12, 12.5), (8, 15, 7.5), (24, 15, 7.5), (16, 5, 8), (10, 8, 6.5), (22, 8, 6.5))
    inside = lambda x, y: any((x - cx) ** 2 + (y - cy) ** 2 <= r * r for cx, cy, r in lobes)
    crown = {(x, y) for y in range(26) for x in range(32) if inside(x + 0.5, y + 0.5)}
    for (x, y) in crown:
        edge = any((x + dx, y + dy) not in crown for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if edge:
            px[(x, y)] = OUTLINE
            continue
        s = (x - 16) + (y - 10) * 1.2
        c = LEAF_L if s < -9 else LEAF_M if s < 2 else LEAF_D if s < 11 else LEAF_X
        if (x * 7 + y * 3) % 11 == 0 and c > LEAF_L:
            c -= 1
        elif (x * 5 + y * 9) % 13 == 0 and c < LEAF_X:
            c += 1
        px[(x, y)] = c
    return px


def main():
    layouts = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    lay = [l for l in layouts if l.get("name") == "PalletTown_Layout"][0]
    bd_path = os.path.join(GBA, lay["blockdata_filepath"]); bd = bytearray(open(bd_path, "rb").read())
    border_path = os.path.join(GBA, lay["border_filepath"]); border = bytearray(open(border_path, "rb").read())
    W, H = lay["width"], lay["height"]
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    pattr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    metas = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attrs = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    pt, st = Image.open(os.path.join(PD, "tiles.png")), Image.open(os.path.join(SD, "tiles.png"))
    ptp, stp = pt.load(), st.load()
    pals = {n: read_pal(os.path.join(PD if n < 7 else SD, "palettes/%02d.pal" % n)) for n in range(13)}
    rules = open(RULES).read()
    num_tiles = int(re.search(r"secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles (\d+)", rules).group(1))
    if WRITE and pals[7][1:9] == GROUND_COLOURS:
        raise SystemExit("  already drawn: row 7 is this tool's (git checkout pallet_town, the map and its border to redraw)")
    assert num_tiles == SLOT_FLOWER, "the anim slots assume the tileset ends at %d; it ends at %d" % (SLOT_FLOWER, num_tiles)

    def entries(m):
        return struct.unpack_from("<8H", prim if m < 640 else metas, (m if m < 640 else m - 640) * 16)

    def attr(m):
        return bytes(pattr[m * 4:(m + 1) * 4]) if m < 640 else bytes(attrs[(m - 640) * 4:(m - 639) * 4])

    # The other maps that load this tileset: which blocks, and do they draw rows 7 or 12?
    shared_blocks = set()
    for l in layouts:
        if l.get("secondary_tileset") == "gTileset_PalletTown" and l["name"] != lay["name"]:
            other = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
            ids = {struct.unpack_from("<H", other, i)[0] & 0x3FF for i in range(0, len(other), 2)}
            shared_blocks |= {m for m in ids if m >= 640}
            rows = {(t >> 12) & 0xF for m in ids for t in entries(m) if t & 0x3FF}
            assert not rows & {7, 12}, "%s draws rows %s" % (l["name"], sorted(rows & {7, 12}))

    cell = lambda x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF

    def vanilla_pixel(t, tx, ty):
        i = t & 0x3FF
        src, j, hh = (ptp, i, pt.height) if i < 640 else (stp, i - 640, st.height)
        sx = (j % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx)
        sy = (j // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
        return src[sx, sy] if sy < hh else 0

    def is_ground(m, t, layer):
        return bool(t & 0x3FF) and ((t >> 12) & 0xF) in GROUND_ROWS and not (m == SIGN_BLOCK and layer == 1)

    # ------------------------------------------------------------ the canvases
    base = [[GRASS] * (W * 16) for _ in range(H * 16)]
    obj = [[None] * (W * 16) for _ in range(H * 16)]
    for y in range(H):
        for x in range(W):
            m = cell(x, y); e = entries(m)
            for q in range(4):
                t = e[q]
                for ty in range(8):
                    for tx in range(8):
                        X, Y = x * 16 + (q % 2) * 8 + tx, y * 16 + (q // 2) * 8 + ty
                        if m in POND_BLOCKS:
                            base[Y][X] = water(X, Y, 0)
                        elif m in TREE_BLOCKS:
                            base[Y][X] = TIP if (X % 16, Y % 16) in ((3, 5), (11, 13)) else TUFT if (X % 16, Y % 16) in ((4, 4), (12, 12)) else GRASS
                        elif is_ground(m, t, 0):
                            p = (t >> 12) & 0xF
                            base[Y][X] = JOBS.get(p, {}).get(vanilla_pixel(t, tx, ty), GRASS)
    tree = birch()
    anchors = [(x, y) for y in range(H) for x in range(W) if cell(x, y) in TREE_ANCHORS]
    covered = {}
    for ax, ay in anchors:
        for dx in (0, 1):
            for dy in (0, 1):
                if ay + dy < H:
                    covered.setdefault((ax + dx, ay + dy), []).append((ax, ay))
        for (px, py), c in tree.items():
            X, Y = ax * 16 + px, ay * 16 + py
            if Y < H * 16:
                obj[Y][X] = (12, c)
    trees = {(x, y) for y in range(H) for x in range(W) if cell(x, y) in TREE_BLOCKS}
    assert set(covered) == trees and all(len(v) == 1 for v in covered.values()), "trees do not pair into 2x2 boxes"
    flower_cells = [(x, y) for y in range(H) for x in range(W) if cell(x, y) == FLOWER_BLOCK]
    bed = daisies(0)
    for x, y in flower_cells:
        for (px, py), c in bed.items():
            obj[y * 16 + py][x * 16 + px] = c
    # the rim: exactly the quadrants vanilla gave top-layer art
    for y in range(H):
        for x in range(W):
            m = cell(x, y)
            if m not in POND_BLOCKS:
                continue
            e = entries(m)
            for q in range(4):
                if not e[4 + q] & 0x3FF:
                    continue
                qx, qy = x * 16 + (q % 2) * 8, y * 16 + (q // 2) * 8
                left, right = cell(x - 1, y) not in POND_BLOCKS, cell(x + 1, y) not in POND_BLOCKS
                top = y == 0 or cell(x, y - 1) not in POND_BLOCKS
                for ty in range(8):
                    for tx in range(8):
                        X, Y = qx + tx, qy + ty
                        lx, ly = X - x * 16, Y - y * 16
                        c = None
                        if top and ly < 8:
                            c = OUTLINE if ly == 0 else JOINT if ly == 6 or (ly > 0 and X % 8 == 7) else None if ly == 7 else STONE
                        if left and lx < 8 and c is None:
                            c = OUTLINE if lx == 0 else JOINT if lx == 6 or (lx > 0 and Y % 8 == 7) else None if lx == 7 else STONE
                        if right and lx >= 8 and c is None:
                            c = OUTLINE if lx == 15 else JOINT if lx == 9 or (lx < 15 and Y % 8 == 7) else None if lx == 8 else STONE
                        if c is not None:
                            obj[Y][X] = (7, c)

    # ------------------------------------------------------------ tiles
    tiles, slot = [], {}
    def put(px, at=None):
        key = bytes(px)
        if key in slot:
            return slot[key]
        n = num_tiles + len(tiles)
        assert at is None or n == at, (n, at)
        slot[key] = n
        tiles.append(px)
        return n

    def flower_frame(f):
        bed_f = daisies(f); out = []
        for q in range(4):
            out.append([bed_f.get(((q % 2) * 8 + i % 8, (q // 2) * 8 + i // 8), (0, 0))[1] for i in range(64)])
        return out

    def water_frame(f):
        return [[water((q % 2) * 8 + i % 8, (q // 2) * 8 + i // 8, f) for i in range(64)] for q in range(4)]

    for q, px in enumerate(flower_frame(0)):
        put(px, SLOT_FLOWER + q)
    for q, px in enumerate(water_frame(0)):
        put(px, SLOT_WATER + q)

    def quadrant(x, y, q, what):
        rows, px = set(), []
        for i in range(64):
            X, Y = x * 16 + (q % 2) * 8 + i % 8, y * 16 + (q // 2) * 8 + i // 8
            o = obj[Y][X]
            if o is not None and what != "base":
                rows.add(o[0]); px.append(o[1])
            elif what == "obj":
                px.append(0)
            else:
                px.append(base[Y][X])
                if base[Y][X] > 8:
                    rows.add(7)
        if len(rows) > 1:
            raise SystemExit("  !! cell (%d,%d) quadrant %d mixes rows %s" % (x, y, q, sorted(rows)))
        return px, (rows.pop() if rows else 7)

    new_cells = {}
    for y in range(H):
        for x in range(W):
            m = cell(x, y); e = list(entries(m)); out = list(e)
            for q in range(4):
                b, t = e[q], e[4 + q]
                bottom, top = is_ground(m, b, 0), is_ground(m, t, 1)
                if top:
                    px, row = quadrant(x, y, q, "obj")
                    out[4 + q] = (put(px) + 640) | (row << 12) if any(px) else 0
                    if bottom:
                        px, row = quadrant(x, y, q, "base")
                        out[q] = (put(px) + 640) | (row << 12)
                elif bottom:
                    px, row = quadrant(x, y, q, "base" if t & 0x3FF else "all")
                    out[q] = (put(px) + 640) | (row << 12)
            new_cells[(x, y)] = tuple(out)

    pond_tiles = {new_cells[(x, y)][q] & 0x3FF for (x, y) in new_cells if cell(x, y) in POND_BLOCKS for q in range(4)}
    assert pond_tiles <= set(range(640 + SLOT_WATER, 640 + SLOT_WATER + 4)), "pond water left the animated slots: %s" % sorted(pond_tiles)
    bed_tiles = {new_cells[c][4 + q] & 0x3FF for c in flower_cells for q in range(4)}
    assert bed_tiles <= set(range(640 + SLOT_FLOWER, 640 + SLOT_FLOWER + 4)), "the daisies left the animated slots: %s" % sorted(bed_tiles)

    # ------------------------------------------------------------ blocks
    variants = {}
    for c, out in new_cells.items():
        variants.setdefault(cell(*c), []).append((c, out))
    ids, in_place, copies = {}, 0, 0
    for m in sorted(variants):
        a = attr(m)
        for c, out in variants[m]:
            if out == tuple(entries(m)):
                continue
            key = (out, a)
            if key not in ids:
                if m >= 640 and m not in shared_blocks and m not in ids.values():
                    struct.pack_into("<8H", metas, (m - 640) * 16, *out)
                    ids[key] = m; in_place += 1
                else:
                    ids[key] = 640 + len(metas) // 16
                    metas += struct.pack("<8H", *out); attrs += a; copies += 1
            raw = struct.unpack_from("<H", bd, (c[1] * W + c[0]) * 2)[0]
            struct.pack_into("<H", bd, (c[1] * W + c[0]) * 2, (raw & ~0x3FF) | ids[key])
    for i, c in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
        struct.pack_into("<H", border, i * 2, (struct.unpack_from("<H", border, i * 2)[0] & ~0x3FF) | cell(*c))
    total = num_tiles + len(tiles)
    assert total <= 384 and len(metas) // 16 <= 384, (total, len(metas) // 16)
    print("  %d trees, %d daisy cells, %d tiles drawn (slots %d..%d), %d blocks rewritten in place, %d copies, border -> %s"
          % (len(anchors), len(flower_cells), len(tiles), num_tiles, total - 1, in_place, copies,
             [struct.unpack_from("<H", border, i * 2)[0] & 0x3FF for i in range(4)]))

    # ------------------------------------------------------------ preview: now | after
    grown = Image.new("P", (128, ((total + 15) // 16) * 8))
    grown.putpalette(st.getpalette()); grown.paste(st, (0, 0)); gp = grown.load()
    for n, px in enumerate(tiles):
        s = num_tiles + n
        for i, v in enumerate(px):
            gp[(s % 16) * 8 + i % 8, (s // 16) * 8 + i // 8] = v

    def pale5(c):
        r, g, b = [v >> 3 for v in c]; grey = (r * 77 + g * 150 + b * 29) >> 8
        lift = 108 if grey > 18 else 67 if grey > 12 else 31
        r += int((grey - r) * 141 / 256); g += int((grey - g) * 141 / 256); b += int((grey - b) * 141 / 256)
        r += ((31 - r) * lift + 128) >> 8; g += ((31 - g) * lift + 128) >> 8; b += ((31 - b) * lift + 128) >> 8
        return (r << 3, g << 3, b << 3)

    def render(metas_now, tiles_img, P, bd_now):
        img = Image.new("RGB", (W * 16, H * 16)); o = img.load(); tl = tiles_img.load()
        for y in range(H):
            for x in range(W):
                m = struct.unpack_from("<H", bd_now, (y * W + x) * 2)[0] & 0x3FF
                e = struct.unpack_from("<8H", prim if m < 640 else metas_now, (m if m < 640 else m - 640) * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = e[layer * 4 + q]; i = t & 0x3FF
                        src, j, hh = (ptp, i, pt.height) if i < 640 else (tl, i - 640, tiles_img.height)
                        for ty in range(8):
                            for tx in range(8):
                                sx = (j % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx)
                                sy = (j // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                v = src[sx, sy] if sy < hh else 0
                                if layer and v == 0:
                                    continue
                                o[x * 16 + (q % 2) * 8 + tx, y * 16 + (q // 2) * 8 + ty] = P[(t >> 12) & 0xF][v]
        return img
    washed = {n: ([p[0]] + [pale5(c) for c in p[1:]] if n < 7 or n in (11, 12) else p) for n, p in pals.items()}
    now = render(open(os.path.join(SD, "metatiles.bin"), "rb").read(), st, washed, open(bd_path, "rb").read())
    after_p = dict(washed); after_p[7] = ROW7; after_p[12] = ROW12; after_p[11] = pals[11]
    after = render(metas, grown, after_p, bd)
    sheet = Image.new("RGB", (W * 16 * 2 + 8, H * 16), (30, 30, 30))
    sheet.paste(now, (0, 0)); sheet.paste(after, (W * 16 + 8, 0))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (now | after)" % PREVIEW)

    if WRITE:
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(metas)
        open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attrs)
        open(bd_path, "wb").write(bd)
        open(border_path, "wb").write(border)
        write_pal(os.path.join(SD, "palettes/07.pal"), ROW7)
        write_pal(os.path.join(SD, "palettes/12.pal"), ROW12)
        flat = [c for col in ROW7 for c in col]
        for name, frames in (("flower", [flower_frame(f) for f in range(FLOWER_FRAMES)]),
                             ("water", [water_frame(f) for f in range(WATER_FRAMES)])):
            os.makedirs(os.path.join(SD, "anim", name), exist_ok=True)
            for f, quads in enumerate(frames):
                im = Image.new("P", (16, 16)); im.putpalette(flat + [0] * (768 - len(flat))); ip = im.load()
                for q, px in enumerate(quads):
                    for i, v in enumerate(px):
                        ip[(q % 2) * 8 + i % 8, (q // 2) * 8 + i // 8] = v
                im.save(os.path.join(SD, "anim", name, "%d.png" % f))
        rules = re.sub(r"(secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+",
                       lambda mm: mm.group(1) + str(total), rules)
        open(RULES, "w").write(rules)
        print("  written: tiles.png, metatiles, attributes, rows 07 and 12, map.bin, border.bin, anim/flower 0..%d, anim/water 0..%d, -num_tiles %d"
              % (FLOWER_FRAMES - 1, WATER_FRAMES - 1, total))


main()

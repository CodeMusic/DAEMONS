#!/usr/bin/env python3
"""Draw Blanche's two houses as two different buildings (T-59, vision.md 9.22).

    python3 tools/gbahouses.py            # preview to /tmp/blanche_houses.png (now | after)
    python3 tools/gbahouses.py --write    # tiles, blocks, rows 9 and 11, the map

T-55 made both houses pale, and a pale copy of one vanilla house is still two
copies of one house. They are two households, so they are two buildings:

    THE PLAYER'S HOUSE is a timber cottage -- weatherboard walls, a steep shingle
    roof with a stone chimney and an attic dormer, a small porch over the door,
    window boxes. An ordinary family home, which is the point next to the Clears.

    THE CLEARS' HOUSE (Al and Vera, 4.29) is the lab's pale stone -- a hipped slate
    roof, tall narrow windows, a stone door surround -- with a glasshouse of white
    frames and plants on its right. Vera just looks; the house is built for
    looking, and nothing says so.

ON VANILLA'S FOOTPRINT. Each house keeps its 5x5 cells, its collision and its
door, and the door cell is not redrawn at all: both doors are block 675, which
field_door.c animates, so the two houses share one door and each draws its own
frame around it -- the cottage a porch, the stone house a lintel and jambs.

WHAT DRAWS OVER THE PLAYER is vanilla's quadrant by quadrant: where vanilla had
house art in the top layer the new art goes there, over the ground; where it had
house art in the bottom layer the new art replaces it and must be opaque.

TWO ROWS. The cottage is drawn in row 11, free since T-58. The stone house is
drawn in the lab's row 9 -- the same whites, greys, slate and glass, which is
what makes it read as the same family -- with the two indices the lab never
uses, 11 and 15, turned into the glasshouse's greens. The tool refuses to write
if anything in any map loading this tileset draws row 9's 11 or 15, or row 11.

The player's house blocks are rewritten in place; the Clears' house gets copies.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/blanche_houses.png"
WRITE = "--write" in sys.argv

DOOR_BLOCK = 675
HOUSE_ROW = 10                  # what T-55 drew both houses in
FOOT_X = {"player": 5, "clears": 14}
FOOT_Y = 3                      # the roof's lower half; the canvas starts 8px into this row
CW, CH = 80, 72

COTTAGE = [(255, 0, 255), (250, 250, 246), (234, 232, 224), (208, 206, 198), (178, 176, 170),
           (192, 200, 210), (160, 170, 184), (126, 136, 152), (98, 106, 122), (62, 64, 72),
           (208, 228, 238), (152, 182, 202), (204, 200, 194), (162, 158, 152), (172, 192, 166), (126, 150, 126)]
PLANT_L, PLANT_D = (172, 192, 166), (120, 146, 122)

# cottage indices (row 11)
WHITE, BOARD, BSHADE, BLINE, SH_L, SH_M, SH_D, RIDGE, OUT, GLASS, GLASSD, CHIM, CHIMD, LEAF, LEAFD = range(1, 16)
# stone house indices (row 9, the lab's)
W1, ST2, ST3, ST4, SL5, SL6, SL7, GL8, GL9, GL10, PL11, PL15 = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, colours):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in colours]
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


class Canvas:
    def __init__(self):
        self.p = [[0] * CW for _ in range(CH)]

    def rect(self, x0, y0, x1, y1, v):
        for y in range(max(0, y0), min(CH, y1 + 1)):
            for x in range(max(0, x0), min(CW, x1 + 1)):
                self.p[y][x] = v

    def px(self, x, y, v):
        if 0 <= x < CW and 0 <= y < CH:
            self.p[y][x] = v


def window(c, x0, y0, x1, y1, frame, glass, dark, bar):
    c.rect(x0, y0, x1, y1, frame)
    c.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, glass)
    for y in range(y0 + 1, y1):
        for x in range(x0 + 1, x1):
            if (x - x0) + (y - y0) > (x1 - x0) + (y1 - y0) - 5:
                c.px(x, y, dark)
    c.rect((x0 + x1) // 2, y0 + 1, (x0 + x1) // 2, y1 - 1, bar)
    c.rect(x0 + 1, (y0 + y1) // 2, x1 - 1, (y0 + y1) // 2, bar)


def cottage():
    c = Canvas()
    # the roof: shingle courses, staggered joints, a ridge, bargeboards, an eave
    c.rect(1, 1, 78, 38, SH_M)
    c.rect(1, 1, 78, 1, OUT)
    c.rect(2, 2, 77, 2, RIDGE)
    for y in range(3, 36):
        course = (y - 3) // 4
        if (y - 3) % 4 == 3:
            c.rect(2, y, 77, y, SH_D)
        elif (y - 3) % 4 == 0:
            c.rect(2, y, 77, y, SH_L)
        for x in range(2, 78):
            if (x + (4 if course % 2 else 0)) % 8 == 0 and (y - 3) % 4 != 3:
                c.px(x, y, SH_D)
    c.rect(0, 1, 1, 38, OUT)
    c.rect(78, 1, 79, 38, OUT)
    c.rect(1, 36, 78, 36, SH_D)
    c.rect(0, 37, 79, 37, RIDGE)
    c.rect(0, 38, 79, 38, OUT)
    # the chimney
    c.rect(59, 0, 68, 1, OUT)
    c.rect(59, 2, 68, 14, OUT)
    c.rect(60, 2, 67, 13, CHIM)
    c.rect(66, 2, 67, 13, CHIMD)
    for y in (5, 9, 13):
        c.rect(60, y, 65, y, CHIMD)
    # the attic dormer
    for y in range(12, 23):
        half = (y - 12) + 1
        c.rect(40 - half, y, 39 + half, y, SH_M if y > 12 else OUT)
        c.px(40 - half, y, OUT); c.px(39 + half, y, OUT)
    c.rect(29, 22, 50, 22, OUT)
    c.rect(30, 23, 49, 33, BOARD)
    c.rect(29, 23, 29, 33, OUT); c.rect(50, 23, 50, 33, OUT)
    c.rect(29, 34, 50, 34, OUT)
    window(c, 34, 24, 45, 32, WHITE, GLASS, GLASSD, WHITE)
    # the walls: weatherboard, corner boards, an eave shadow, a stone footing
    c.rect(0, 39, 79, 71, BOARD)
    for y in range(39, 69):
        if y % 3 == 2:
            c.rect(2, y, 77, y, BLINE)
    c.rect(0, 39, 79, 39, BLINE)
    c.rect(0, 40, 79, 40, BSHADE)
    c.rect(0, 39, 0, 71, OUT); c.rect(1, 39, 2, 68, WHITE)
    c.rect(79, 39, 79, 71, OUT); c.rect(77, 39, 78, 68, WHITE)
    c.rect(0, 69, 79, 70, CHIMD); c.rect(0, 71, 79, 71, OUT)
    # windows, and boxes under the two on the right
    window(c, 4, 45, 12, 57, WHITE, GLASS, GLASSD, WHITE)
    c.rect(3, 57, 13, 57, OUT)
    for x0 in (41, 60):
        window(c, x0, 44, x0 + 14, 57, WHITE, GLASS, GLASSD, WHITE)
        c.rect(x0 - 1, 44, x0 - 1, 57, OUT); c.rect(x0 + 15, 44, x0 + 15, 57, OUT)
        c.rect(x0 - 1, 59, x0 + 15, 62, BLINE)
        c.rect(x0 - 1, 62, x0 + 15, 62, OUT)
        for k, x in enumerate(range(x0, x0 + 15, 2)):
            c.px(x, 58 - (k % 2), LEAF)
            c.px(x + 1, 58, LEAFD)
            c.px(x, 59, LEAFD if k % 3 else LEAF)
    # the porch over the door (the door cell itself is vanilla's and is not drawn)
    for y in range(44, 55):
        half = min(11, (y - 44) + 2)
        c.rect(24 - half, y, 23 + half, y, SH_M if (y - 44) % 3 else SH_D)
        c.px(24 - half, y, OUT); c.px(23 + half, y, OUT)
    c.rect(12, 55, 35, 55, OUT)
    for x in (13, 34):
        c.rect(x, 56, x + 1, 68, WHITE)
        c.rect(x - 1 if x == 13 else x + 2, 56, x - 1 if x == 13 else x + 2, 68, OUT)
    return c


def stone():
    c = Canvas()
    # the hipped slate roof over the main house, x 0..51: a long ridge, short hips
    for y in range(3, 39):
        t = (y - 3) / 33
        xl, xr = round(6 * (1 - t)), round(45 + 6 * t)
        if y >= 36:
            xl, xr = 0, 51
        c.rect(xl, y, xr, y, SL5)
        c.px(xl, y, SL7); c.px(xr, y, SL7)
        if 3 < y < 36:
            c.px(xl + 1, y, SL6); c.px(xr - 1, y, SL6)
    c.rect(6, 3, 45, 3, SL7)
    c.rect(7, 4, 44, 4, ST4)
    for y in range(8, 36, 4):
        t = (y - 3) / 33
        c.rect(round(6 * (1 - t)) + 2, y, round(45 + 6 * t) - 2, y, SL6)
    c.rect(0, 36, 51, 36, SL6)
    c.rect(0, 37, 51, 38, SL7)
    # the walls: pale stone, staggered joints, quoins, a plinth
    c.rect(0, 39, 51, 71, ST2)
    c.rect(0, 39, 51, 40, ST4)
    for y in range(41, 68):
        if (y - 41) % 6 == 5:
            c.rect(1, y, 50, y, ST3)
        else:
            for x in range(1, 51):
                if (x + (6 if ((y - 41) // 6) % 2 else 0)) % 12 == 0:
                    c.px(x, y, ST3)
    for y in range(41, 68):
        c.rect(0, y, 0, y, SL6)
        c.rect(1, y, 3 if ((y - 41) // 6) % 2 else 5, y, ST3 if (y - 41) % 6 == 5 else W1)
    c.rect(0, 68, 51, 70, ST4); c.rect(0, 71, 51, 71, SL6)
    # tall narrow windows with sills
    for x0 in (4, 38):
        c.rect(x0 - 1, 43, x0 + 9, 65, SL6)
        window(c, x0, 44, x0 + 8, 64, W1, GL8, GL9, W1)
        c.rect(x0 - 2, 66, x0 + 10, 66, ST4)
        c.rect(x0 - 2, 67, x0 + 10, 67, SL6)
    # a stone surround for the shared door: a lintel and two jambs
    c.rect(13, 51, 34, 55, ST4)
    c.rect(13, 51, 34, 51, SL6)
    c.rect(13, 55, 34, 55, SL6)
    c.rect(23, 51, 24, 55, ST3)
    for x in (13, 33):
        for y in range(56, 70):
            c.rect(x, y, x + 1, y, ST3 if (y // 4) % 2 else ST4)
        c.rect(x - 1 if x == 13 else x + 2, 56, x - 1 if x == 13 else x + 2, 69, SL6)
    # the glasshouse, x 52..79: a lower glass roof and glass walls on white frames
    c.rect(51, 20, 79, 71, W1)
    for y in range(21, 40):                                              # the roof: pale panes, sloping bars
        for x in range(52, 79):
            if x in (58, 65, 72) or (y - 21) % 6 == 5:
                continue
            c.px(x, y, ST3 if y < 30 else ST2)
    for y in range(21, 40, 3):
        c.px(53 + (y % 5), y, W1)
    c.rect(51, 19, 79, 19, SL7)
    c.rect(51, 20, 51, 39, SL7); c.rect(79, 19, 79, 71, SL7)
    c.rect(52, 39, 78, 40, SL6)
    for y in range(41, 69):                                              # the walls: clear panes
        for x in range(52, 79):
            if x in (58, 65, 72) or y == 54:
                continue
            c.px(x, y, ST2 if (x - y) % 11 else GL8)
    # plants behind the lower panes, and in the upper ones a few leaves
    import math
    for k, (cx, cy, r) in enumerate(((55, 62, 4), (61, 58, 6), (68, 62, 5), (75, 57, 5), (56, 48, 3), (69, 47, 4), (76, 45, 3))):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r and 52 <= x <= 78 and 41 <= y <= 68 \
                        and x not in (58, 65, 72) and y != 54:
                    c.px(x, y, PL15 if (x - cx) + (y - cy) > 1 else PL11)
    for x in range(53, 78, 7):
        c.rect(x, 66, x + 3, 68, ST4)
    c.rect(52, 69, 78, 70, ST4); c.rect(51, 71, 79, 71, SL6)
    return c


def main():
    layouts = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    lay = [l for l in layouts if l.get("name") == "PalletTown_Layout"][0]
    bd_path = os.path.join(GBA, lay["blockdata_filepath"]); bd = bytearray(open(bd_path, "rb").read())
    W, H = lay["width"], lay["height"]
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    metas = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attrs = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    pt, st = Image.open(os.path.join(PD, "tiles.png")), Image.open(os.path.join(SD, "tiles.png"))
    ptp, stp = pt.load(), st.load()
    pals = {n: read_pal(os.path.join(PD if n < 7 else SD, "palettes/%02d.pal" % n)) for n in range(13)}
    rules = open(RULES).read()
    rule = r"(secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )(\d+)"
    num_tiles = int(re.search(rule, rules).group(2))
    if WRITE and pals[11] == COTTAGE:
        raise SystemExit("  already drawn: row 11 is the cottage's (git checkout pallet_town and the map to redraw)")

    def entries(m):
        return struct.unpack_from("<8H", prim if m < 640 else metas, (m if m < 640 else m - 640) * 16)

    def pixel(t, tx, ty):
        i = t & 0x3FF
        src, j, hh = (ptp, i, pt.height) if i < 640 else (stp, i - 640, st.height)
        sy = (j // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
        return src[(j % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0

    # every map that loads this tileset: nothing may draw row 11, or row 9's 11 and 15
    shared = set()
    for l in layouts:
        if l.get("secondary_tileset") != "gTileset_PalletTown":
            continue
        data = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        ids = {struct.unpack_from("<H", data, i)[0] & 0x3FF for i in range(0, len(data), 2)}
        if l["name"] != lay["name"]:
            shared |= {m for m in ids if m >= 640}
        for m in ids:
            for t in entries(m):
                p = (t >> 12) & 0xF
                if not t & 0x3FF:
                    continue
                assert p != 11, "%s draws row 11 (block %d)" % (l["name"], m)
                if p == 9:
                    used = {pixel(t, x, y) for x in range(8) for y in range(8)}
                    assert not used & {11, 15}, "%s draws row 9's index %s (block %d)" % (l["name"], sorted(used & {11, 15}), m)

    designs = {"player": (cottage(), 11), "clears": (stone(), 9)}
    tiles, slot = [], {}
    def put(px):
        key = bytes(px)
        if key not in slot:
            slot[key] = num_tiles + len(tiles); tiles.append(px)
        return slot[key]

    cell_out = {}
    for name, (canvas, row) in designs.items():
        hx = FOOT_X[name]
        for cy in range(5):
            for cx in range(5):
                x, y = hx + cx, FOOT_Y + cy
                m = struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
                if m == DOOR_BLOCK:
                    continue
                e = list(entries(m)); out = list(e)
                for q in range(4):
                    qx, qy = cx * 16 + (q % 2) * 8, cy * 16 + (q // 2) * 8 - 8
                    house = lambda t: bool(t & 0x3FF) and ((t >> 12) & 0xF) == HOUSE_ROW
                    hb, ht = house(e[q]), house(e[4 + q])
                    if qy < 0:
                        assert not hb and not ht, (name, x, y, q)
                        continue
                    px = [canvas.p[qy + i // 8][qx + i % 8] for i in range(64)]
                    if hb:
                        if 0 in px:
                            raise SystemExit("  !! %s (%d,%d) q%d: the bottom layer was house and the drawing has a hole" % (name, x, y, q))
                        out[q] = (put(px) + 640) | (row << 12)
                        if ht:
                            out[4 + q] = 0
                    elif ht:
                        out[4 + q] = ((put(px) + 640) | (row << 12)) if any(px) else 0
                    elif any(px):
                        print("  .. %s (%d,%d) q%d has no house layer; %d pixels dropped" % (name, x, y, q, sum(1 for v in px if v)))
                cell_out[(x, y)] = (m, tuple(out))

    ids, in_place, copies = {}, 0, 0
    for (x, y), (m, out) in sorted(cell_out.items()):
        a = bytes(attrs[(m - 640) * 4:(m - 639) * 4])
        key = (out, a)
        if key not in ids:
            if x < FOOT_X["clears"] and m not in shared and m not in ids.values():
                struct.pack_into("<8H", metas, (m - 640) * 16, *out); ids[key] = m; in_place += 1
            else:
                ids[key] = 640 + len(metas) // 16
                metas += struct.pack("<8H", *out); attrs += a; copies += 1
        raw = struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
        struct.pack_into("<H", bd, (y * W + x) * 2, (raw & ~0x3FF) | ids[key])
    total = num_tiles + len(tiles)
    assert total <= 384 and len(metas) // 16 <= 384, (total, len(metas) // 16)
    print("  %d tiles drawn (slots %d..%d), %d blocks rewritten in place, %d copies for the Clears' house"
          % (len(tiles), num_tiles, total - 1, in_place, copies))

    grown = Image.new("P", (128, ((total + 15) // 16) * 8))
    grown.putpalette(st.getpalette()); grown.paste(st, (0, 0)); gp = grown.load()
    for n, px in enumerate(tiles):
        s = num_tiles + n
        for i, v in enumerate(px):
            gp[(s % 16) * 8 + i % 8, (s // 16) * 8 + i // 8] = v
    row9 = list(pals[9]); row9[11], row9[15] = PLANT_L, PLANT_D

    def render(metas_now, tiles_img, P, bd_now):
        img = Image.new("RGB", (W * 16, H * 16)); o = img.load(); tl = tiles_img.load()
        for yy in range(H):
            for xx in range(W):
                m = struct.unpack_from("<H", bd_now, (yy * W + xx) * 2)[0] & 0x3FF
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
                                o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = P[(t >> 12) & 0xF][v]
        return img.crop((3 * 16, 2 * 16, 21 * 16, 9 * 16))
    now = render(open(os.path.join(SD, "metatiles.bin"), "rb").read(), st, pals, open(bd_path, "rb").read())
    after_p = dict(pals); after_p[11] = COTTAGE; after_p[9] = row9
    after = render(metas, grown, after_p, bd)
    sheet = Image.new("RGB", (now.width, now.height * 2 + 6), (30, 30, 30))
    sheet.paste(now, (0, 0)); sheet.paste(after, (0, now.height + 6))
    sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(PREVIEW)
    print("  preview %s (now above, after below)" % PREVIEW)

    if WRITE:
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(metas)
        open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attrs)
        open(bd_path, "wb").write(bd)
        write_pal(os.path.join(SD, "palettes/11.pal"), COTTAGE)
        write_pal(os.path.join(SD, "palettes/09.pal"), row9)
        open(RULES, "w").write(re.sub(rule, lambda mm: mm.group(1) + str(total), rules))
        print("  written: tiles.png, metatiles, attributes, rows 09 and 11, map.bin, -num_tiles %d" % total)


main()

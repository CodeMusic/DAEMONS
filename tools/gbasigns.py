#!/usr/bin/env python3
"""Blanche's signs say something (vision.md 9.22).

    python3 tools/gbasigns.py            # preview to /tmp/blanche_signs.png
    python3 tools/gbasigns.py --write    # tiles, blocks, the map

Vanilla's signboards carry a squiggle that reads as Japanese at a glance, and
T-55 only paled it. At 16 pixels a board holds three letters of a 3x5 font, so
the signs say short words, in the pale fence row (10) with its darkest grey as ink:

    THE TOWN SIGN (9,11) widens over the fence post beside it (8,11) and reads
    BLANCHE -- seven letters, the most a 32-pixel board holds.
    THE LAB SIGN (16,16) reads LAB, on its own block: it shared the town's.
    THE TRAINER TIPS POST (5,14) shows a question mark.
    ROUTE 1'S SIGN (9,31), inside the pale stretch gbaroutes.py drew, reads RT1.

A sign already drawn is left alone, so adding one re-runs the tool safely.

The text box each sign opens is unchanged; the board is only its cover. Each
cell keeps its ground in the bottom layer and its attributes and collision; the
board replaces the top layer, and every changed cell gets a new block.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/blanche_signs.png"
WRITE = "--write" in sys.argv
ROW = 10
WHITE, PALE, LIGHT, MID, GREY, SHADE, INK = 1, 2, 3, 4, 5, 6, 7

FONT = {
    "A": ("010", "101", "111", "101", "101"), "B": ("110", "101", "110", "101", "110"),
    "C": ("011", "100", "100", "100", "011"), "E": ("111", "100", "110", "100", "111"),
    "H": ("101", "101", "111", "101", "101"), "L": ("100", "100", "100", "100", "111"),
    "N": ("101", "111", "111", "101", "101"), "?": ("111", "001", "011", "000", "010"),
    "R": ("110", "101", "110", "101", "101"), "T": ("111", "010", "010", "010", "010"),
    "1": ("010", "110", "010", "010", "111"),
}
SIGNS = [
    # (layout, cells, text, style)
    ("PalletTown_Layout", [(8, 11), (9, 11)], "BLANCHE", "board"),
    ("PalletTown_Layout", [(16, 16)], "LAB", "board"),
    ("PalletTown_Layout", [(5, 14)], "?", "post"),
    ("Route1_Layout", [(9, 31)], "RT1", "board"),
]


def draw(width, text, style):
    c = [[0] * width for _ in range(16)]
    def rect(x0, y0, x1, y1, v):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c[y][x] = v
    if style == "board":
        edge = 0 if len(text) * 4 - 1 > width - 6 else 1   # a long word takes the whole width
        rect(edge, 1, width - 1 - edge, 11, INK)           # the board
        rect(edge + 1, 2, width - 2 - edge, 10, WHITE)
        rect(edge + 1, 10, width - 2 - edge, 10, LIGHT)
        rect(edge + 1, 2, width - 2 - edge, 2, PALE)
        for px in (3, width - 5):                          # two legs
            rect(px, 12, px + 1, 14, GREY)
            rect(px + 1, 12, px + 1, 14, SHADE)
        rect(2, 15, width - 3, 15, MID)                    # its shadow
    else:
        rect(3, 1, 12, 10, INK)                            # a small board on one post
        rect(4, 2, 11, 9, WHITE)
        rect(4, 9, 11, 9, LIGHT)
        rect(7, 11, 8, 14, GREY)
        rect(8, 11, 8, 14, SHADE)
        rect(5, 15, 10, 15, MID)
    ink_w = len(text) * 4 - 1
    x = (width - ink_w) // 2
    y = 4 if style == "board" else 3
    for ch in text:
        for dy, bits in enumerate(FONT[ch]):
            for dx, b in enumerate(bits):
                if b == "1":
                    c[y + dy][x + dx] = INK
        x += 4
    return c


def main():
    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    metas = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attrs = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    pattr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    st = Image.open(os.path.join(SD, "tiles.png")); stp = st.load()
    rules = open(RULES).read()
    rule = r"(secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )(\d+)"
    num_tiles = int(re.search(rule, rules).group(2))

    existing = lambda n: [stp[(n % 16) * 8 + k % 8, (n // 16) * 8 + k // 8] for k in range(64)]
    tiles, slot = [], {}
    def put(px):
        key = bytes(px)
        if key not in slot:
            slot[key] = num_tiles + len(tiles); tiles.append(px)
        return slot[key]

    maps, new_blocks = {}, 0
    for name, cells, text, style in SIGNS:
        lay = layouts[name]
        if name not in maps:
            path = os.path.join(GBA, lay["blockdata_filepath"])
            maps[name] = (path, bytearray(open(path, "rb").read()), lay["width"])
        path, bd, W = maps[name]
        cell = lambda x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
        art = draw(16 * len(cells), text, style)
        quads = [[[art[(q // 2) * 8 + k // 8][i * 16 + (q % 2) * 8 + k % 8] for k in range(64)] for q in range(4)] for i in range(len(cells))]
        def drawn(i, x, y):
            m = cell(x, y)
            if m < 640:
                return False
            e = struct.unpack_from("<8H", metas, (m - 640) * 16)
            for q in range(4):
                t, want = e[4 + q], quads[i][q]
                if not any(want):
                    if t & 0x3FF:
                        return False
                elif not (640 <= (t & 0x3FF) < 640 + num_tiles and (t >> 12) == ROW and existing((t & 0x3FF) - 640) == want):
                    return False
            return True
        if all(drawn(i, x, y) for i, (x, y) in enumerate(cells)):
            print("  %s %s: already drawn" % (name, text))
            continue
        for i, (x, y) in enumerate(cells):
            m = cell(x, y)
            e = list(struct.unpack_from("<8H", prim if m < 640 else metas, (m if m < 640 else m - 640) * 16))
            a = bytes(pattr[m * 4:(m + 1) * 4]) if m < 640 else bytes(attrs[(m - 640) * 4:(m - 639) * 4])
            for q in range(4):
                e[4 + q] = ((put(quads[i][q]) + 640) | (ROW << 12)) if any(quads[i][q]) else 0
            nid = 640 + len(metas) // 16
            metas += struct.pack("<8H", *e); attrs += a; new_blocks += 1
            raw = struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
            struct.pack_into("<H", bd, (y * W + x) * 2, (raw & ~0x3FF) | nid)
        print("  %s %s: drawn" % (name, text))
    total = num_tiles + len(tiles)
    assert total <= 384 and len(metas) // 16 <= 384
    print("  %d tiles (slots %d..%d), %d new blocks" % (len(tiles), num_tiles, total - 1, new_blocks))

    pal = [tuple(map(int, l.split())) for l in open(os.path.join(SD, "palettes/10.pal")).read().replace("\r", "").split("\n")[3:19]]
    sheet = Image.new("RGB", (len(SIGNS) * 40, 16), (200, 212, 190))
    x0 = 0
    for _, cells, text, style in SIGNS:
        art = draw(16 * len(cells), text, style)
        for y in range(16):
            for x in range(16 * len(cells)):
                if art[y][x]:
                    sheet.putpixel((x0 + x, y), pal[art[y][x]])
        x0 += 16 * len(cells) + 8
    sheet.resize((sheet.width * 8, sheet.height * 8), Image.NEAREST).save(PREVIEW)
    print("  preview %s" % PREVIEW)

    if WRITE:
        grown = Image.new("P", (128, ((total + 15) // 16) * 8)); grown.putpalette(st.getpalette()); grown.paste(st, (0, 0)); gp = grown.load()
        for n, px in enumerate(tiles):
            s = num_tiles + n
            for k, v in enumerate(px):
                gp[(s % 16) * 8 + k % 8, (s // 16) * 8 + k // 8] = v
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(metas)
        open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attrs)
        for path, bd, W in maps.values():
            open(path, "wb").write(bd)
        open(RULES, "w").write(re.sub(rule, lambda mm: mm.group(1) + str(total), rules))
        print("  written: tiles.png, metatiles, attributes, map.bin, -num_tiles %d" % total)


main()

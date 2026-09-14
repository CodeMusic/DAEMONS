#!/usr/bin/env python3
"""The sketch on the station table (T-84; vision.md 9.22, 4.6).

    python3 tools/gbastation.py            # preview to /tmp/station.png
    python3 tools/gbastation.py --write    # the Mansion tileset's row 9, two tiles, one block, the station map

Under the visitor log, a sheet of paper with one rabbit drawn three times --
4.6's three forms, in order: vivid purple and faceted, then split, then white
with a facet left where the light catches it. It names nobody and says nothing
about the session: 4.10's rule is that the session itself is never shown, and
this is only a drawing somebody left.

The sheet covers the table cell below the book, on the top layer
over the table, in the Mansion tileset's palette row 9, which nothing else in
that tileset draws. Its text is read with the log.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SD = os.path.join(GBA, "data/tilesets/secondary/pokemon_mansion")
PD = os.path.join(GBA, "data/tilesets/primary/building")
RULES = os.path.join(GBA, "tileset_rules.mk")
MAP = os.path.join(GBA, "data/layouts/Route21_North_Station/map.bin")
PREVIEW = "/tmp/station.png"
WRITE = "--write" in sys.argv
W = 11
CELL = (5, 7)                                 # the table cell under the book
ROW = 9
COLOURS = {1: (232, 226, 210), 2: (186, 178, 160), 3: (104, 100, 116), 4: (206, 128, 230), 5: (130, 64, 160),
           6: (255, 255, 255), 7: (214, 204, 232)}
# 16x16: paper (1), its edge (2), pencil (3); purple (4) with facets (5); white (6) with one facet (7).
# One rabbit, three times, left to right: faceted, split, whole.
BUNNY = ["X.X.", "X.X.", "X.X.", "XXX.", "XEXX", "XXX.", ".XX.", "XXXX", "XXXX", "XXXX", "X.X."]
def sketch():
    g = [[1] * 16 for _ in range(16)]
    for x in range(16):
        g[0][x] = 2; g[15][x] = 2
    for stage, x0 in enumerate((1, 6, 11)):
        for y, row in enumerate(BUNNY):
            for x, ch in enumerate(row):
                if ch == ".":
                    continue
                X, Y = x0 + x, 2 + y
                if ch == "E":
                    g[Y][X] = 3; continue
                purple = stage == 0 or (stage == 1 and x < 2)
                if purple:
                    g[Y][X] = 5 if (x + y) % 3 == 0 else 4
                else:
                    g[Y][X] = 7 if (stage == 2 and (x, y) == (1, 8)) else 6
        for x in range(4):
            g[13][x0 + x] = 3
    return ["".join(str(v) for v in row) for row in g]
SKETCH = sketch()


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, cols):
    open(path, "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols))


def main():
    meta = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attr = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    bd = bytearray(open(MAP, "rb").read())
    raw = struct.unpack_from("<H", bd, (CELL[1] * W + CELL[0]) * 2)[0]; m = raw & 0x3FF
    e = list(struct.unpack_from("<8H", meta, (m - 640) * 16))
    if (e[4] >> 12) & 0xF == ROW:
        print("  the sketch is already on the table"); return
    rules = open(RULES).read()
    key = "secondary/pokemon_mansion/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles "
    at = rules.index(key) + len(key); n = int(rules[at:].split()[0])
    img = Image.open(os.path.join(SD, "tiles.png"))
    need = ((n + 4 + 15) // 16) * 8
    grown = Image.new("P", (128, max(img.height, need))); grown.putpalette(img.getpalette()); grown.paste(img, (0, 0)); gp = grown.load()
    for q in range(4):
        s = n + q
        for y in range(8):
            for x in range(8):
                gp[(s % 16) * 8 + x, (s // 16) * 8 + y] = int(SKETCH[(q // 2) * 8 + y][(q % 2) * 8 + x])
        e[4 + q] = (640 + s) | (ROW << 12)
    nid = 640 + len(meta) // 16
    meta += struct.pack("<8H", *e); attr += attr[(m - 640) * 4:(m - 639) * 4]
    struct.pack_into("<H", bd, (CELL[1] * W + CELL[0]) * 2, (raw & ~0x3FF) | nid)
    pal = read_pal(os.path.join(SD, "palettes/%02d.pal" % ROW))
    for i, c in COLOURS.items():
        pal[i] = c
    prev = Image.new("RGB", (16, 16))
    for y in range(16):
        for x in range(16):
            prev.putpixel((x, y), COLOURS[int(SKETCH[y][x])])
    prev.resize((160, 160), Image.NEAREST).save(PREVIEW)
    print("  block %#x at %s copies %#x with the sketch on top; preview %s" % (nid, CELL, m, PREVIEW))
    if WRITE:
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(meta); open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attr)
        open(MAP, "wb").write(bd)
        write_pal(os.path.join(SD, "palettes/%02d.pal" % ROW), pal)
        open(RULES, "w").write(rules[:at] + str(n + 4) + rules[at + len(str(n)):])
        print("  written: Mansion tiles (-num_tiles %d), block, row 9, the station map" % (n + 4))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""THE SCHOLAR'S HOUSE in Brazen, as a stone study (vision.md 4.23; chosen from concepts 2026-09-14).

    python3 tools/gbascholar.py            # preview to /tmp/scholar.png (drawn | as the game's rows will show it)
    python3 tools/gbascholar.py --write    # Brazen's tileset: new tiles, new blocks, row 7's spare colours, both maps

WHY IT LOOKS LIKE THIS. The Owl lives in the bought city and keeps his own counsel,
so his is the one house in Brazen that is not brass: grey fieldstone, a dark slate
roof with a lamp lit in a round window, windows full of books, a stone arch and a
brass plaque at the door, ivy up one corner, a stone owl at the ridge. Nobody says
why it is different.

HOW IT GOES IN. Every Brazen house is drawn by the same blocks, so the scholar's
twenty-four cells get blocks of their own, appended to Brazen's tileset; each new
block keeps the original's bottom layer and attributes and draws the study in the
top layer, as Brazen's houses do. The door cell keeps block 644, which the door
animation is keyed to -- the arch is drawn around it. The same house stands in
SaffronCity_Connection's copy of the city and is replaced there too.

COLOUR. The stone, slate and ivy come from Brazen's own greys and greens; row 7,
which only the BENCHMARK's pillars use and only in indices 1..4, gives its eleven
spare indices to the books, the lamp, the wood and the brass. Each 8x8 tile takes
whichever row draws it best; transparent pixels exist only where the roof row
shows the ground.

TILES go into slots no used block references, including the sixteen the sheet can
still grow into; it stops if they do not fit.
"""
import json, math, os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SD = os.path.join(GBA, "data/tilesets/secondary/saffron_city")
PD = os.path.join(GBA, "data/tilesets/primary/general")
PREVIEW = "/tmp/scholar.png"
WRITE = "--write" in sys.argv
MAX_TILES = MAX_BLOCKS = 384
HOUSES = {"LAYOUT_SAFFRON_CITY": (41, 34), "LAYOUT_SAFFRON_CITY_CONNECTION": (31, 27)}
HOUSE = [[661, 662, 662, 662, 663], [669, 670, 670, 670, 671], [677, 678, 647, 655, 679], [664, 694, 695, 687, 668], [672, 651, 644, 652, 676]]
DOOR = (2, 4)
ROW7 = {5: (172, 189, 205), 6: (123, 123, 131), 7: (65, 74, 106), 8: (150, 66, 58), 9: (74, 98, 142), 10: (98, 128, 80),
        11: (202, 172, 92), 12: (92, 66, 44), 13: (60, 42, 30), 14: (240, 196, 110), 15: (196, 146, 80)}
ROWS = (2, 3, 7, 8, 9, 10, 11, 12)        # the rows a tile may be drawn in

INK = (65, 74, 106)
STONE, STONEL, STONED, MORTAR = (148, 164, 180), (172, 189, 205), (123, 123, 131), (90, 90, 115)
SLATE, SLATEL, SLATED = (90, 90, 115), (123, 123, 131), (65, 74, 106)
IVY, IVYL = (82, 131, 90), (139, 189, 148)
LAMP, LAMPD, WOOD, WOODD, BRASS = (240, 196, 110), (196, 146, 80), (92, 66, 44), (60, 42, 30), (202, 172, 92)
BOOKS = [(150, 66, 58), (74, 98, 142), (98, 128, 80), (202, 172, 92)]


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, cols):
    open(path, "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols))


# ---------------------------------------------------------------- the drawing, 80x80, None where the ground shows
def draw():
    """Drawn for the tile grid: textures repeat every 8 pixels, and everything but the ivy and the plaque is
    symmetric about the house's centre line, so its left and right tiles are one tile and its mirror."""
    p = [[None] * 80 for _ in range(80)]

    def px(x, y, c):
        if 0 <= x < 80 and 0 <= y < 80:
            p[y][x] = c

    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px(x, y, c)

    def mirror(x0, x1, y0, y1):
        """copy the left-hand drawing in columns x0..x1 onto its mirror image on the right"""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                p[y][79 - x] = p[y][x]

    def courses(y0, y1, base, lit, joint):
        # courses four pixels deep, a lit top line, two-pixel joints on the 8-pixel grid, staggered course to course
        for y in range(y0, y1 + 1):
            for x in range(80):
                v = base
                if y % 4 == 0:
                    v = joint
                elif y % 4 == 1:
                    v = lit
                elif x % 8 in ((7, 0) if (y // 4) % 2 == 0 else (3, 4)):
                    v = joint
                px(x, y, v)

    # the slate roof, cell rows 0..2, its outline and the eave in shadow
    courses(4, 43, SLATE, SLATEL, SLATED)
    rect(0, 3, 79, 3, INK); rect(0, 4, 0, 47, INK); rect(79, 4, 79, 47, INK)
    rect(1, 44, 78, 46, SLATED); rect(0, 47, 79, 47, INK)
    # the round window in the roof, a lamp lit inside, its glazing bars -- centred on a tile corner
    cx, cy, r = 40, 24, 10
    for y in range(cy - r - 2, cy + r + 2):
        for x in range(cx - r - 2, cx + r + 2):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= r - 2:
                px(x, y, LAMP if d < 5 else LAMPD)
            elif d <= r:
                px(x, y, STONEL)
            elif d <= r + 1.3:
                px(x, y, INK)
    rect(39, cy - 8, 40, cy + 7, WOODD); rect(cx - 8, 23, cx + 7, 24, WOODD)
    # a stone owl at the ridge, symmetric, centred
    for y, row in enumerate(["X....X", "XXXXXX", "XoXXoX", "XXvvXX"]):
        for x, ch in enumerate(row):
            if ch != ".":
                px(37 + x, y, {"X": STONEL, "o": INK, "v": BRASS}[ch])
    # fieldstone walls, cell rows 3..4, under the eave's shadow
    courses(48, 79, STONE, STONEL, MORTAR)
    rect(1, 48, 78, 49, SLATED); rect(0, 48, 0, 79, INK); rect(79, 48, 79, 79, INK)
    # a tall window, lamplit, shelves of books behind a glazing bar -- drawn left, mirrored right
    rect(3, 51, 15, 75, STONEL); rect(3, 76, 15, 76, STONED); rect(2, 51, 2, 76, INK); rect(16, 51, 16, 76, INK)
    rect(5, 53, 13, 73, WOOD)
    for sy in (53, 60, 67):
        for x in range(5, 14):
            h = 3 + x % 3
            rect(x, sy + 5 - h, x, sy + 5, BOOKS[x % 4])
        rect(5, sy + 6, 13, sy + 6, WOODD)
    rect(9, 53, 9, 73, LAMPD)
    mirror(2, 16, 51, 76)
    # the door's stone arch, symmetric about the door
    rect(28, 58, 31, 79, STONEL); rect(28, 56, 39, 63, STONEL)
    for k in range(5):
        rect(31 + k, 55 - k // 2, 39, 55 - k // 2, STONEL)
    rect(27, 56, 27, 79, INK); rect(34, 52, 39, 52, INK); rect(32, 79, 39, 79, MORTAR)
    mirror(27, 39, 52, 79)
    # the brass plaque, and ivy up the left corner
    rect(53, 65, 56, 69, BRASS); px(53, 65, LAMP); rect(53, 70, 56, 70, WOODD)
    for (x, y) in ((1, 77), (2, 75), (1, 73), (3, 72), (2, 70), (4, 68), (3, 66), (1, 65)):
        rect(x, y, x + 1, y + 1, IVY); px(x + 1, y, IVYL)
    return p


# ---------------------------------------------------------------- tiles, blocks, maps
def hflip(t):
    return tuple(t[(i // 8) * 8 + 7 - i % 8] for i in range(64))


def vflip(t):
    return tuple(t[(7 - i // 8) * 8 + i % 8] for i in range(64))


def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    meta = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attr = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    sheet = Image.open(os.path.join(SD, "tiles.png")); sp = sheet.load()
    pals = {r: read_pal(os.path.join(PD, "palettes/%02d.pal" % r)) for r in range(7)}
    pals.update({r: read_pal(os.path.join(SD, "palettes/%02d.pal" % r)) for r in range(7, 13)})
    for k, c in ROW7.items():
        pals[7][k] = c
    art = draw()

    # which blocks the maps will still use once both houses are replaced, and so which tiles are taken
    maps = {}
    for lid, (hx, hy) in HOUSES.items():
        l = layouts[lid]; W = l["width"]
        bd = bytearray(open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read())
        for j in range(5):
            for i in range(5):
                assert struct.unpack_from("<H", bd, ((hy + j) * W + hx + i) * 2)[0] & 0x3FF == HOUSE[j][i], "%s is not the house at (%d,%d)" % (lid, hx, hy)
        maps[lid] = (l, bd)
    used_blocks = set()
    for l in layouts.values():
        if l.get("secondary_tileset") != "gTileset_SaffronCity":
            continue
        d = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        W = l["width"]; hx, hy = HOUSES.get(l["id"], (-99, -99))
        for n in range(len(d) // 2):
            x, y = n % W, n // W
            if 0 <= x - hx < 5 and 0 <= y - hy < 5 and (x - hx, y - hy) != DOOR:
                continue
            used_blocks.add(struct.unpack_from("<H", d, n * 2)[0] & 0x3FF)
    taken = {0}
    for b in used_blocks:
        if b >= 640 and (b - 640 + 1) * 16 <= len(meta):
            taken |= {(t & 0x3FF) - 640 for t in struct.unpack_from("<8H", meta, (b - 640) * 16) if (t & 0x3FF) >= 640}
    free = [n for n in range(MAX_TILES) if n not in taken]

    # quantize each quadrant into its best row; transparent stays 0, opaque never is
    existing = {}
    for n in taken:
        if n < (sheet.height // 8) * 16:
            existing.setdefault(tuple(sp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] for i in range(64)), n)
    new_tiles, cells, err_total = {}, {}, 0
    for j in range(5):
        for i in range(5):
            if (i, j) == DOOR:
                continue
            entries = []
            for q in range(4):
                x0, y0 = i * 16 + (q % 2) * 8, j * 16 + (q // 2) * 8
                pix = [art[y0 + k // 8][x0 + k % 8] for k in range(64)]
                if all(c is None for c in pix):
                    entries.append(0); continue
                best = None
                for r in ROWS:
                    idx, err = [], 0
                    for c in pix:
                        if c is None:
                            idx.append(0); continue
                        k, e = min(((k, sum((c[m] - pals[r][k][m]) ** 2 for m in range(3))) for k in range(1, 16)), key=lambda t: t[1])
                        idx.append(k); err += e
                    if best is None or err < best[1]:
                        best = (r, err, tuple(idx))
                r, err, idx = best; err_total += err
                ref = None
                for flip, f in ((0, lambda t: t), (0x400, hflip), (0x800, vflip), (0xC00, lambda t: hflip(vflip(t)))):
                    t = f(idx)
                    if t in existing:
                        ref = ("old", existing[t], flip); break
                    if t in new_tiles:
                        ref = ("new", new_tiles[t], flip); break
                if ref is None:
                    new_tiles[idx] = len(new_tiles); ref = ("new", new_tiles[idx], 0)
                entries.append((ref, r))
            cells[(i, j)] = entries
    print("  24 cells: %d new tiles (%d slots free), mean squared error per pixel %.1f" % (len(new_tiles), len(free), err_total / (24 * 256)))
    if len(new_tiles) > len(free):
        raise SystemExit("  does not fit")
    slot = {n: free[k] for k, n in enumerate(sorted(new_tiles.values()))}

    # the blocks: the original bottom layer and attributes, the study on top
    nblocks = len(meta) // 16
    made, block_of = {}, {}
    for (i, j), entries in cells.items():
        orig = HOUSE[j][i] - 640
        e = list(struct.unpack_from("<8H", meta, orig * 16))
        for q, ent in enumerate(entries):
            if ent == 0:
                e[4 + q] = 0
            else:
                (kind, n, flip), r = ent
                e[4 + q] = (640 + (n if kind == "old" else slot[n])) | flip | (r << 12)
        key = (tuple(e), bytes(attr[orig * 4:orig * 4 + 4]))
        if key not in made:
            made[key] = 640 + nblocks + len(made)
        block_of[(i, j)] = made[key]
    print("  %d new blocks (%d of %d used)" % (len(made), nblocks + len(made), MAX_BLOCKS))
    if nblocks + len(made) > MAX_BLOCKS:
        raise SystemExit("  too many blocks")

    # preview: the drawing | the rows as the game will show them, on a ground colour
    out = Image.new("RGB", (80 * 2 + 8, 80), (40, 40, 40)); o = out.load()
    inv = {v: k for k, v in new_tiles.items()}
    for (i, j), entries in cells.items():
        for q, ent in enumerate(entries):
            x0, y0 = i * 16 + (q % 2) * 8, j * 16 + (q // 2) * 8
            for k in range(64):
                c = art[y0 + k // 8][x0 + k % 8]
                o[x0 + k % 8, y0 + k // 8] = c if c else (213, 213, 164)
                if ent == 0:
                    v = 0
                else:
                    (kind, n, flip), r = ent
                    tile = inv[n] if kind == "new" else next(t for t, m in existing.items() if m == n)
                    for f, fn in ((0x400, hflip), (0x800, vflip)):
                        if flip & f:
                            tile = fn(tile)
                    v = tile[k]
                o[88 + x0 + k % 8, y0 + k // 8] = pals[ent[1]][v] if ent and v else (213, 213, 164)
    out.resize((out.width * 4, out.height * 4), Image.NEAREST).save(PREVIEW)
    print("  preview %s" % PREVIEW)

    if WRITE:
        rows = max(sheet.height // 8, (max(slot.values(), default=0) // 16) + 1)
        grown = Image.new("P", (128, rows * 8)); grown.putpalette(sheet.getpalette()); grown.paste(sheet, (0, 0)); gp = grown.load()
        for tile, n in new_tiles.items():
            s = slot[n]
            for k, v in enumerate(tile):
                gp[(s % 16) * 8 + k % 8, (s // 16) * 8 + k // 8] = v
        grown.save(os.path.join(SD, "tiles.png"))
        for (e, a), b in sorted(made.items(), key=lambda t: t[1]):
            meta += struct.pack("<8H", *e); attr += a
        open(os.path.join(SD, "metatiles.bin"), "wb").write(meta)
        open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attr)
        write_pal(os.path.join(SD, "palettes/07.pal"), pals[7])
        for lid, (l, bd) in maps.items():
            hx, hy = HOUSES[lid]; W = l["width"]
            for (i, j), b in block_of.items():
                n = ((hy + j) * W + hx + i) * 2
                raw = struct.unpack_from("<H", bd, n)[0]
                struct.pack_into("<H", bd, n, (raw & ~0x3FF) | b)
            open(os.path.join(GBA, l["blockdata_filepath"]), "wb").write(bd)
        rules = os.path.join(GBA, "tileset_rules.mk"); text = open(rules).read()
        key = "$(TILESETGFXDIR)/secondary/saffron_city/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles "
        if key in text:
            at = text.index(key) + len(key); old = text[at:].split()[0]
            text = text[:at] + str(rows * 16) + text[at + len(old):]
            open(rules, "w").write(text)
        print("  written: tiles.png (%d rows), %d blocks appended, palette row 7, both maps" % (rows, len(made)))


if __name__ == "__main__":
    main()

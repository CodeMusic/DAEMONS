#!/usr/bin/env python3
"""The world's own grass: our greens, our tufts, leafier tall grass (T-61, vision.md 9.22).

    python3 tools/gbagrass.py            # preview to /tmp/world_grass.png (before | after)
    python3 tools/gbagrass.py --write    # palettes, tiles.png, the grass field effects

THE GREENS. Vanilla's grass is a cool mint-teal and its leaves a lime; ours is a
meadow green and a deeper, warmer leaf, with brown trunks. The exact vanilla
colours are replaced wherever they occur in an outdoor palette -- the General
tileset's rows, the 25 secondary tilesets outdoor maps load (a town's paths and
fences meet grass in its own rows, so the mint is there too), and the grass
field effects -- so no seam can open between a tile that changed and one that
did not. Only these exact colours move; nothing that merely resembles them.

THE TUFTS. The sixteen plain grass tiles (588..591, 604..607, 620..623,
636..639) get our sprig instead of vanilla's -- a small V of two blades, one lit
-- and a few paired dots, each kept a pixel inside its tile, so any grass tile
still sits against any other.

THE TALL GRASS (68, 69, 84, 85; block 13 on 5503 cells) is a leafier clump: broad
tapered leaves fanning from the root, shaded and outlined, with the plain grass
colour at its edges so a field of it still tiles. The walking effect and the
landing tufts are redrawn from the same clump, in the indices general_1.pal
gives the same jobs, so the sprite matches the tile it parts.

Blanche's pale tall grass (gbaroutes.py) was derived from vanilla's clump
earlier and keeps that shape until it is re-derived.
"""
import json, math, os, re, struct, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driftguard import refuse_over_later_work

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
FX = os.path.join(GBA, "graphics/field_effects")
PREVIEW = "/tmp/world_grass.png"
WRITE = "--write" in sys.argv

# vanilla colour -> ours
GREENS = {
    (115, 205, 164): (124, 192, 104),   # grass
    (164, 230, 197): (174, 220, 146),   # grass, lit
    (65, 180, 139):  (88, 160, 84),     # tuft
    (24, 164, 106):  (58, 132, 70),     # tuft, dark
    (139, 222, 189): (146, 204, 120),   # the mint under trees
    (189, 255, 139): (204, 236, 132),   # leaf, lit
    (131, 213, 98):  (132, 188, 84),    # leaf
    (57, 148, 49):   (66, 128, 58),     # leaf, dark
    (57, 139, 49):   (66, 128, 58),
    (57, 90, 16):    (42, 82, 44),      # leaf, deepest
    (57, 82, 0):     (42, 82, 44),
    (49, 65, 0):     (34, 64, 38),
    (115, 98, 98):   (132, 98, 70),     # trunk
    (65, 57, 49):    (76, 54, 42),      # trunk, dark
}
GRASS_TILES = [588, 589, 590, 591, 604, 605, 606, 607, 620, 621, 622, 623, 636, 637, 638, 639]
TALL = (68, 69, 84, 85)
# row 0 (and general_1) index jobs
LIT, LEAF, DARK, DEEP = 1, 2, 3, 4
BASE, GLIGHT, TUFT, TDARK = 13, 12, 14, 15
PREVIEW_MAPS = [("Route1_Layout", 0, 2, 24, 16), ("CeladonCity_Layout", 18, 0, 24, 14)]


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, colours):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in colours]
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


def secondary_dir(symbol):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    for d in os.listdir(os.path.join(GBA, "data/tilesets/secondary")):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(GBA, "data/tilesets/secondary", d)


# ---------------------------------------------------------------- drawing
def grass_tile(n):
    """8x8 of plain grass with at most one of our sprigs, chosen by the tile's own number."""
    t = [[BASE] * 8 for _ in range(8)]
    h = (n * 2654435761) & 0xFFFFFFFF
    if (h >> 5) % 3:                                 # two tiles in three carry a sprig
        x, y = (h >> 9) % 4 + 2, (h >> 13) % 4 + 2
        t[y - 1][x - 1] = GLIGHT                     # the lit blade
        t[y - 1][x + 1] = TUFT                       # the other
        t[y][x] = TDARK                              # where they meet
    if (h >> 19) % 4 == 0:                           # one in four, a pair of dots
        dx, dy = (h >> 23) % 5 + 1, (h >> 27) % 6 + 1
        if t[dy][dx] == BASE and t[dy][dx + 1] == BASE:
            t[dy][dx] = TUFT; t[dy][dx + 1] = TUFT
    return t


def clump():
    """16x16 of tall grass: narrow blades fanning up from three roots, over a
    darker mass of grass, so a field of it reads as one field, not as shrubs."""
    c = [[BASE] * 16 for _ in range(16)]
    for y in range(5, 16):                           # the mass the blades stand in
        for x in range(16):
            if y >= 7 or 3 <= x <= 12:
                c[y][x] = TUFT
    blades = [(3, (-3.0, 3.0)), (3, (-0.5, 1.0)), (3, (2.0, 4.0)),
              (8, (-2.5, 0.0)), (8, (0.5, -0.5)), (8, (3.0, 1.5)),
              (13, (-2.0, 4.0)), (13, (0.5, 1.0)), (13, (3.0, 3.0))]
    for rx, (dx, ty) in blades:
        root, tip = (rx, 15.5), (rx + dx, ty)
        length = math.hypot(tip[0] - root[0], tip[1] - root[1])
        nx, ny = -(tip[1] - root[1]) / length, (tip[0] - root[0]) / length
        for s_ in range(101):
            p_ = s_ / 100
            cx, cy = root[0] + (tip[0] - root[0]) * p_, root[1] + (tip[1] - root[1]) * p_
            w = 1.35 * (1 - p_) + 0.35
            for o in (-1.0, -0.5, 0.0, 0.5, 1.0):
                if abs(o) > w:
                    continue
                x, y = int(math.floor(cx + nx * o)) % 16, int(math.floor(cy + ny * o))
                if 0 <= y < 16:
                    c[y][x] = LIT if o < -0.4 and p_ > 0.3 else DARK if o > 0.4 else LEAF
    for x in range(16):                              # roots in shadow
        if c[15][x] in (LEAF, LIT):
            c[15][x] = DEEP
        elif c[15][x] == TUFT:
            c[15][x] = TDARK
    return c


def effect_frames(cl):
    """tall_grass.png: 5 frames of 16x16, as vanilla's -- the clump's lower half,
    the whole clump, then leaves thrown up in three steps."""
    lower = [[(v if y >= 9 and v != BASE else 0) for v in row] for y, row in enumerate(cl)]
    full = [row[:] for row in cl]
    def with_bits(bits, colour):
        f = [row[:] for row in lower]
        for x, y in bits:
            f[y][x] = colour
            if x + 1 < 16 and f[y][x + 1] == 0:
                f[y][x + 1] = LEAF if colour == LIT else colour
        return f
    return [lower, full,
            with_bits([(2, 3), (5, 1), (10, 2), (13, 4), (3, 7), (12, 7), (7, 5)], LIT),
            with_bits([(3, 5), (11, 4), (1, 9), (14, 9)], LIT),
            with_bits([(4, 6), (10, 8)], GLIGHT)]


def jump_frames():
    """jump_tall_grass.png: 2 frames of 16x16 (4 of 16x8) -- leaves flung out, then settling."""
    f = [[[0] * 16 for _ in range(8)] for _ in range(4)]
    pts = [[(3, 2), (12, 2), (1, 4), (14, 4), (5, 6), (10, 6)],
           [(2, 1), (13, 1), (0, 4), (15, 4), (4, 6), (11, 6)],
           [(2, 2), (13, 2), (0, 4), (14, 4), (4, 6), (10, 6)],
           [(2, 3), (12, 3), (1, 5), (14, 5), (5, 7), (10, 7)]]
    for k, frame in enumerate(f):
        for x, y in pts[k]:
            frame[y][x] = LIT if k < 2 else GLIGHT
            if x + 1 < 16:
                frame[y][x + 1] = LEAF if k < 2 else TUFT
    return f


def main():
    refuse_over_later_work("gbagrass")          # T-293: its files carry later work; generator_drift.json says what
    layouts = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    outdoor = sorted({l["secondary_tileset"] for l in layouts if l.get("primary_tileset") == "gTileset_General"})
    pal_files = [os.path.join(PD, "palettes/%02d.pal" % n) for n in range(7)]
    for sym in outdoor:
        d = secondary_dir(sym)
        if d:
            pal_files += [os.path.join(d, "palettes/%02d.pal" % n) for n in range(7, 13)]
    pal_files += [os.path.join(FX, "palettes/general_1.pal")]
    changed, entries = {}, 0
    for path in pal_files:
        old = read_pal(path); new = [GREENS.get(c, c) for c in old]
        if new != old:
            changed[path] = new; entries += sum(1 for a, b in zip(old, new) if a != b)
    print("  %d palette entries in %d files move onto our greens" % (entries, len(changed)))

    tiles = Image.open(os.path.join(PD, "tiles.png")); new_tiles = tiles.copy(); ntp = new_tiles.load()
    for n in GRASS_TILES:
        t = grass_tile(n)
        for y in range(8):
            for x in range(8):
                ntp[(n % 16) * 8 + x, (n // 16) * 8 + y] = t[y][x]
    cl = clump()
    for q, n in enumerate(TALL):
        for y in range(8):
            for x in range(8):
                ntp[(n % 16) * 8 + x, (n // 16) * 8 + y] = cl[(q // 2) * 8 + y][(q % 2) * 8 + x]
    tg = Image.open(os.path.join(FX, "pics/tall_grass.png")).copy(); tgp = tg.load()
    for k, f in enumerate(effect_frames(cl)):
        for y in range(16):
            for x in range(16):
                tgp[x, k * 16 + y] = f[y][x]
    jg = Image.open(os.path.join(FX, "pics/jump_tall_grass.png")).copy(); jgp = jg.load()
    for k, f in enumerate(jump_frames()):
        for y in range(8):
            for x in range(16):
                jgp[x, k * 8 + y] = f[y][x]

    # preview: two grassy maps before and after, and the effect frames
    L = {l.get("name"): l for l in layouts}
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    panels = []
    for name, x0, y0, w, h in PREVIEW_MAPS:
        lay = L[name]; sd = secondary_dir(lay["secondary_tileset"])
        bd = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read(); W = lay["width"]
        sm = open(os.path.join(sd, "metatiles.bin"), "rb").read()
        st = Image.open(os.path.join(sd, "tiles.png")); stp = st.load()
        pair = []
        for after in (False, True):
            src_tiles = (new_tiles if after else tiles).load()
            pals = []
            for n in range(13):
                path = os.path.join(PD if n < 7 else sd, "palettes/%02d.pal" % n)
                pals.append(changed.get(path, read_pal(path)) if after else read_pal(path))
            img = Image.new("RGB", (w * 16, h * 16)); o = img.load()
            for y in range(y0, y0 + h):
                for x in range(x0, x0 + w):
                    m = struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
                    e = struct.unpack_from("<8H", prim if m < 640 else sm, (m if m < 640 else m - 640) * 16)
                    for layer in (0, 1):
                        for q in range(4):
                            t = e[layer * 4 + q]; i = t & 0x3FF
                            src, j, hh = (src_tiles, i, tiles.height) if i < 640 else (stp, i - 640, st.height)
                            for ty in range(8):
                                for tx in range(8):
                                    sy = (j // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                    v = src[(j % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                                    if layer and v == 0:
                                        continue
                                    o[(x - x0) * 16 + (q % 2) * 8 + tx, (y - y0) * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
            pair.append(img)
        panels.append(pair)
    fxpal_old = read_pal(os.path.join(FX, "palettes/general_1.pal"))
    fxpal_new = changed.get(os.path.join(FX, "palettes/general_1.pal"), fxpal_old)
    fx = Image.new("RGB", (16 * 5 + 16 * 3, 16 * 2 + 8), (40, 40, 40))
    orig = Image.open(os.path.join(FX, "pics/tall_grass.png")).load()
    for k in range(5):
        for y in range(16):
            for x in range(16):
                if orig[x, k * 16 + y]:
                    fx.putpixel((k * 16 + x, y), fxpal_old[orig[x, k * 16 + y]])
                if tgp[x, k * 16 + y]:
                    fx.putpixel((k * 16 + x, 24 + y - 8 + 8), fxpal_new[tgp[x, k * 16 + y]])
    width = panels[0][0].width * 2 + 8
    height = sum(a.height for a, _ in panels) + 8 * len(panels) + fx.height * 4
    sheet = Image.new("RGB", (width, height), (30, 30, 30)); yy = 0
    for a, b in panels:
        sheet.paste(a, (0, yy)); sheet.paste(b, (a.width + 8, yy)); yy += a.height + 8
    sheet.paste(fx.resize((fx.width * 4, fx.height * 4), Image.NEAREST), (0, yy))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (before | after: %s; the walking effect below, vanilla above ours)" % (PREVIEW, ", ".join(n for n, *_ in PREVIEW_MAPS)))

    if WRITE:
        for path, colours in changed.items():
            write_pal(path, colours)
        new_tiles.save(os.path.join(PD, "tiles.png"))
        tg.save(os.path.join(FX, "pics/tall_grass.png"))
        jg.save(os.path.join(FX, "pics/jump_tall_grass.png"))
        print("  written: %d palettes, tiles.png (16 grass tiles, the tall grass clump), tall_grass.png, jump_tall_grass.png" % len(changed))


if __name__ == "__main__":
    main()

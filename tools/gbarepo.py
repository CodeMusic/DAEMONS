#!/usr/bin/env python3
"""THE REPO inside: its shelves hold labelled package bins (T-65; vision.md 9.23).

    python3 tools/gbarepo.py            # preview to /tmp/repo.png (before | after)
    python3 tools/gbarepo.py --write    # the Mart tileset: tiles, blocks re-pointed in place, palette row 10

A REPO is where packages are kept and fetched by name, so its shelving holds bins,
each with a white label -- not a shop's jars and bottles. Two pieces of furniture
change and nothing else does: the wall cabinet behind the counter side (cells
x7..9, rows 0..2) and the aisle gondolas (x7..8, rows 3..6, and the half-unit at
x10, which reuses the same blocks). Their top-layer entries are re-pointed in
place to new tiles, so every REPO changes and no map is touched; the floor beneath,
the counter, the clerk and the scripts keep their tiles.

The old shelf tiles are the Building tileset's, shared by department stores,
gyms and houses, so they are left alone; the new tiles go into the Mart tileset,
which had 36. The bins' ambers go in the Mart tileset's palette row 10, which was
empty -- THE REPO's colour is golden amber (9.23).
"""
import json, os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SD = os.path.join(GBA, "data/tilesets/secondary/mart")
PD = os.path.join(GBA, "data/tilesets/primary/building")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/repo.png"
WRITE = "--write" in sys.argv
MAX_TILES = 384
ROW = 10
PALETTE = [(255, 0, 255), (58, 56, 70), (104, 106, 118), (156, 160, 170), (206, 210, 216), (240, 242, 244),
           (120, 78, 34), (170, 116, 52), (212, 160, 76), (238, 204, 120), (250, 232, 176),
           (96, 98, 120), (246, 246, 238), (70, 140, 150), (214, 108, 70), (0, 0, 0)]
OUT, STEELD, STEEL, STEELL, STEELW, BIND, BINM, BIN, BINL, BINW, INK, LABEL, TEAL, RED = range(1, 15)

# (block, [(entry, art, art x, art y)])
CABINET = [(658, [(6, 0, 0), (7, 8, 0)]), (659, [(6, 16, 0), (7, 24, 0)]), (660, [(6, 32, 0), (7, 40, 0)]),
           (666, [(4, 0, 8), (5, 8, 8), (6, 0, 16), (7, 8, 16)]), (667, [(4, 16, 8), (5, 24, 8), (6, 16, 16), (7, 24, 16)]),
           (668, [(4, 32, 8), (5, 40, 8), (6, 32, 16), (7, 40, 16)]),
           (674, [(4, 0, 24), (5, 8, 24)]), (675, [(4, 16, 24), (5, 24, 24)]), (676, [(4, 32, 24), (5, 40, 24)])]
GONDOLA = [(662, [(6, 0, 0), (7, 8, 0)]), (663, [(6, 16, 0), (7, 24, 0)])] + \
          [(b, [(4, x, y), (5, x + 8, y), (6, x, y + 8), (7, x + 8, y + 8)]) for b, x, y in
           ((670, 0, 8), (671, 16, 8), (678, 0, 24), (679, 16, 24), (686, 0, 40), (687, 16, 40))]


def canvas(w, h):
    return [[0] * w for _ in range(h)]


def rect(g, x0, y0, x1, y1, v):
    for y in range(max(0, y0), min(len(g), y1 + 1)):
        for x in range(max(0, x0), min(len(g[0]), x1 + 1)):
            g[y][x] = v


def bin_(g, x0, y0, w, h):
    """a package bin seen from the front and a little above: a lit lip, a darker body, a white label with a line of ink"""
    rect(g, x0, y0, x0 + w - 1, y0 + h - 1, OUT)
    rect(g, x0 + 1, y0 + 1, x0 + w - 2, y0 + 1, BINW)
    rect(g, x0 + 1, y0 + 2, x0 + w - 2, y0 + h - 2, BIN)
    rect(g, x0 + w - 2, y0 + 2, x0 + w - 2, y0 + h - 2, BINM)
    rect(g, x0 + 1, y0 + h - 2, x0 + w - 2, y0 + h - 2, BINM)
    lw = max(3, w - 4)
    lx = x0 + (w - lw) // 2; ly = y0 + 3
    rect(g, lx, ly, lx + lw - 1, ly + 2, LABEL); rect(g, lx + 1, ly + 1, lx + lw - 2, ly + 1, INK)


def cabinet():
    """48x32: a steel wall unit, three bays of two shelves, a bin in each"""
    g = canvas(48, 32)
    rect(g, 0, 0, 47, 31, OUT); rect(g, 1, 1, 46, 3, STEELW); rect(g, 1, 4, 46, 30, STEELD)
    for bx in (1, 17, 33):
        for sy in (5, 17):
            rect(g, bx + 1, sy, bx + 13, sy + 10, STEELD)
            bin_(g, bx + 2, sy + 1, 12, 10)
            rect(g, bx, sy + 11, bx + 14, sy + 11, STEELL)
    for x in (16, 32):
        rect(g, x, 4, x, 30, STEEL)
    rect(g, 1, 30, 46, 30, STEEL)
    return g


def gondola():
    """32x56: an aisle unit seen from above and the front -- a cap, three tiers of bins, a base in shadow"""
    g = canvas(32, 56)
    rect(g, 1, 0, 30, 55, OUT)
    rect(g, 2, 1, 29, 5, STEELW); rect(g, 2, 5, 29, 5, STEELL)                    # the cap
    rect(g, 2, 6, 29, 51, STEELD)
    for n, ty in enumerate((7, 22, 37)):
        bin_(g, 3, ty, 13, 12); bin_(g, 16, ty, 13, 12)
        rect(g, 2, ty + 12, 29, ty + 13, STEELL); rect(g, 2, ty + 14, 29, ty + 14, STEEL)
    rect(g, 2, 52, 29, 54, STEEL); rect(g, 2, 54, 29, 54, STEELD)                 # the base
    rect(g, 2, 1, 2, 51, STEELL); rect(g, 29, 6, 29, 51, STEEL)
    return g


def hflip(t):
    return tuple(t[(i // 8) * 8 + 7 - i % 8] for i in range(64))


def vflip(t):
    return tuple(t[(7 - i // 8) * 8 + i % 8] for i in range(64))


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    meta = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read()); original = bytes(meta)
    sheet = Image.open(os.path.join(SD, "tiles.png")); sp = sheet.load()
    rules = open(RULES).read()
    key = "$(TILESETGFXDIR)/secondary/mart/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles "
    at = rules.index(key) + len(key); num_tiles = int(rules[at:].split()[0])
    tile_px = lambda img, n: tuple(img[(n % 16) * 8 + k % 8, (n // 16) * 8 + k // 8] % 16 for k in range(64))

    want = []
    for art, cells in ((cabinet(), CABINET), (gondola(), GONDOLA)):
        for block, entries in cells:
            for e, ax, ay in entries:
                want.append((block, e, tuple(art[ay + k // 8][ax + k % 8] for k in range(64))))
    rewritten = {(b, e) for b, e, _ in want}

    users = [l for l in layouts.values() if l.get("secondary_tileset") == "gTileset_Mart"]
    used = set()
    for l in users:
        d = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        used |= {struct.unpack_from("<H", d, i * 2)[0] & 0x3FF for i in range(len(d) // 2)}
    taken = {0}
    for b in used:
        if b >= 640 and (b - 639) * 16 <= len(meta):
            for e, t in enumerate(struct.unpack_from("<8H", meta, (b - 640) * 16)):
                if (b, e) not in rewritten and (t & 0x3FF) >= 640:
                    taken.add((t & 0x3FF) - 640)
    free = [n for n in range(MAX_TILES) if n not in taken]
    new = {}
    for block, e, px in want:
        if not any(px):
            struct.pack_into("<H", meta, (block - 640) * 16 + e * 2, 0); continue
        ref = None
        for flip, f in ((0, lambda t: t), (0x400, hflip), (0x800, vflip), (0xC00, lambda t: hflip(vflip(t)))):
            t = f(px)
            if t in new:
                ref = (new[t], flip); break
        if ref is None:
            new[px] = free[len(new)]; ref = (new[px], 0)
        struct.pack_into("<H", meta, (block - 640) * 16 + e * 2, (640 + ref[0]) | ref[1] | (ROW << 12))
    print("  %d entries rewritten; %d new tiles (%d slots free)" % (len(want), len(new), len(free)))
    total = max([num_tiles] + [s + 1 for s in new.values()])
    grown = Image.new("P", (128, max(sheet.height, ((total + 15) // 16) * 8))); grown.putpalette(sheet.getpalette()); grown.paste(sheet, (0, 0)); gp = grown.load()
    for px, s in new.items():
        for k, v in enumerate(px):
            gp[(s % 16) * 8 + k % 8, (s // 16) * 8 + k // 8] = v

    # preview: the whole shop, before | after
    pals = [read_pal(os.path.join(PD, "palettes/%02d.pal" % r)) for r in range(7)] + [read_pal(os.path.join(SD, "palettes/%02d.pal" % r)) for r in range(7, 13)]
    after_pals = list(pals); after_pals[ROW] = PALETTE
    pmeta = open(os.path.join(PD, "metatiles.bin"), "rb").read(); ptiles = Image.open(os.path.join(PD, "tiles.png")).load()
    l = layouts["LAYOUT_MART"]; W, H = l["width"], l["height"]; bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()

    def render(mt, tiles, P):
        out = Image.new("RGB", (W * 16, H * 16)); o = out.load()
        for y in range(H):
            for x in range(W):
                m = struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
                src, k = (pmeta, m) if m < 640 else (mt, m - 640)
                if (k + 1) * 16 > len(src):
                    continue
                ent = struct.unpack_from("<8H", src, k * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = ent[layer * 4 + q]; i = t & 0x3FF
                        for ty in range(8):
                            for tx in range(8):
                                sx = 7 - tx if t & 0x400 else tx; sy = 7 - ty if t & 0x800 else ty
                                v = (ptiles[(i % 16) * 8 + sx, (i // 16) * 8 + sy] if i < 640 else tiles[((i - 640) % 16) * 8 + sx, ((i - 640) // 16) * 8 + sy]) % 16
                                if layer and v == 0:
                                    continue
                                o[x * 16 + (q % 2) * 8 + tx, y * 16 + (q // 2) * 8 + ty] = P[(t >> 12) & 15][v]
        return out
    before, after = render(original, sp, pals), render(bytes(meta), gp, after_pals)
    out = Image.new("RGB", (W * 32 + 8, H * 16), (30, 30, 30)); out.paste(before, (0, 0)); out.paste(after, (W * 16 + 8, 0))
    out.resize((out.width * 2, out.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (before | after)" % PREVIEW)

    if WRITE:
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(meta)
        open(os.path.join(SD, "palettes/%02d.pal" % ROW), "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in PALETTE))
        if total != num_tiles:
            open(RULES, "w").write(rules[:at] + str(total) + rules[at + len(str(num_tiles)):])
        print("  written: the Mart tileset (%d tiles), palette row %d" % (total, ROW))


if __name__ == "__main__":
    main()

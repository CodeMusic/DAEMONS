#!/usr/bin/env python3
"""Restyle a town's building KIT through the sprite server (T-164's pilot, 2026-09-19): Doldrum's houses.

    python3 tools/gbarestyle.py --draft                  # render the house, restyle it (drafts in gfx/drafts/t164/pilot/)
    python3 tools/gbarestyle.py --pick FILE              # preview the tileset with FILE applied (before | after)
    python3 tools/gbarestyle.py --pick FILE --write      # write it into the tileset
    ... --keep-colour                                    # the restyle's lightness, the town's own hues

WHAT T-164'S TRIAL SETTLED: from words the model draws vignettes, not tiles; restyling the art already in the game at
about 0.6 improves a building and keeps its footprint. So this restyles the house AS RENDERED and writes the result
back into the tiles it was drawn from.

WHY THE KIT, NOT THE HOUSE. Doldrum's houses are built from one shared kit: the left house's 18 blocks also build the
right house and the houses to the north, and its 27 kit tiles appear in other blocks too. The tileset has 33 free tile
slots of 384, so a private copy of one house (~100 tiles) does not fit -- and a town whose houses match is the point. So
each KIT TILE is rewritten in place: its new pixels are read back from every place the restyled house draws it (flips
undone, occurrences averaged), and every block that draws it, anywhere, changes with it.

WHERE THE COLOURS GO. The kit is drawn in rows 12 and 8, whose indices mean things to tiles outside the kit, so the
restyle gets a row of its own: ROW 7, freed by moving its four colours into row 10's unused indices 10..13 (row 7's
seven tiles are drawn only in row 7, and the tileset has no animation). The kit tiles are then drawn in row 7 with a
15-colour palette fitted to the restyle.

WHAT DOES NOT MOVE: every block id, every collision and behaviour attribute, the door (block 664, animated by
field_door.c, not redrawn), primary tiles, and TRANSPARENCY -- a kit pixel that was index 0 stays 0, so a top-layer
tile still shows the ground behind it and the roof still draws over the player where it did.
"""
import json, os, struct, subprocess, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
SD = os.path.join(GBA, "data/tilesets/secondary/cerulean_city")
OUT = os.path.join(ROOT, "gfx/drafts/t164/pilot")
LAYOUT = "CeruleanCity_Layout"
HOUSE = (21, 25, 26, 28)             # cells x0, y0, x1, y1 of the left house (door at 23,28)
MARGIN = 1
DOOR = 664
KIT_ROWS = (12, 8)
FREE_ROW, INTO_ROW, INTO_SLOTS = 7, 10, (10, 11, 12, 13)
STYLE = ("a small town house with a blue-grey slate roof with visible tiles and cream plaster walls with wooden trim, "
         "pixel art, Game Boy Advance RPG overworld tileset style, top-down three-quarter view, crisp 16-bit pixels, "
         "flat even lighting")
NEG = ("text, letters, watermark, people, characters, border, frame, vignette, blurry, photorealistic, 3d render, "
       "perspective distortion, extra windows, extra doors")


def read_pal(n):
    d = PD if n < 7 else SD
    return [tuple(map(int, l.split())) for l in open(os.path.join(d, "palettes/%02d.pal" % n)).read().replace("\r", "").split("\n")[3:19]]


def write_pal(n, cols):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % tuple(c) for c in cols]
    open(os.path.join(SD, "palettes/%02d.pal" % n), "wb").write(("\r\n".join(lines) + "\r\n").encode())


class TS:
    def __init__(self):
        self.lay = [l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("name") == LAYOUT][0]
        self.W, self.H = self.lay["width"], self.lay["height"]
        self.bd = open(os.path.join(GBA, self.lay["blockdata_filepath"]), "rb").read()
        self.prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
        self.sec = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
        self.pt = Image.open(os.path.join(PD, "tiles.png")); self.st = Image.open(os.path.join(SD, "tiles.png")).copy()
        self.pals = {n: read_pal(n) for n in range(13)}

    def block(self, x, y):
        return struct.unpack_from("<H", self.bd, (y * self.W + x) * 2)[0] & 0x3FF

    def entries(self, m):
        return list(struct.unpack_from("<8H", self.prim if m < 640 else self.sec, (m if m < 640 else m - 640) * 16))

    def tile_px(self, t, tx, ty):
        i = t & 0x3FF
        img, j = (self.pt, i) if i < 640 else (self.st, i - 640)
        sx = (j % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx)
        sy = (j // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
        return img.getpixel((sx, sy)) if sy < img.height else 0

    def render(self, x0, y0, x1, y1):
        img = Image.new("RGB", ((x1 - x0 + 1) * 16, (y1 - y0 + 1) * 16)); o = img.load()
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                e = self.entries(self.block(x, y))
                for layer in (0, 1):
                    for q in range(4):
                        t = e[layer * 4 + q]
                        for ty in range(8):
                            for tx in range(8):
                                v = self.tile_px(t, tx, ty)
                                if layer and v == 0:
                                    continue
                                o[(x - x0) * 16 + (q % 2) * 8 + tx, (y - y0) * 16 + (q // 2) * 8 + ty] = self.pals[(t >> 12) & 0xF][v]
        return img


def region():
    x0, y0, x1, y1 = HOUSE
    return x0 - MARGIN, y0 - MARGIN, x1 + MARGIN, y1 + MARGIN


def draft():
    os.makedirs(OUT, exist_ok=True)
    ts = TS(); r = region()
    now = ts.render(*r); now.save(os.path.join(OUT, "now.png"))
    src = now.resize((now.width * 8, now.height * 8), Image.NEAREST); src.save(os.path.join(OUT, "src.png"))
    for dn in ("0.55", "0.62"):
        for seed in (1917, 42):
            subprocess.run(["python3", os.path.join(ROOT, "tools/spriteforge.py"), "i2i", "--out", os.path.join(OUT, "restyle_%s_%d" % (dn[2:], seed)),
                            "--image", os.path.join(OUT, "src.png"), "--denoise", dn, "--seed", str(seed), "--prompt", STYLE, "--negative", NEG])


def native(path, w, h):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    return np.array([[np.median(a[y*8+2:y*8+6, x*8+2:x*8+6].reshape(-1, 3), axis=0) for x in range(w)] for y in range(h)])


def fit_palette(pixels, n=15, iters=25):
    """k-means in RGB, seeded by luminance quantiles so dark outlines keep their own entries."""
    px = np.array(pixels, float); lum = px @ [0.299, 0.587, 0.114]
    order = np.argsort(lum); c = px[order[np.linspace(0, len(px) - 1, n).astype(int)]]
    for _ in range(iters):
        lab = ((px[:, None, :] - c[None]) ** 2).sum(2).argmin(1)
        for k in range(n):
            if (lab == k).any():
                c[k] = px[lab == k].mean(0)
    return [tuple(int(round(v)) for v in col) for col in c]


def apply(pick, write):
    ts = TS(); r = region(); x0, y0, x1, y1 = HOUSE
    before = ts.render(8, 7, 39, 29)                   # rendered FIRST: everything below edits the tiles in memory
    now = np.asarray(ts.render(*r)).astype(int)
    new = native(pick, now.shape[1], now.shape[0])
    if "--keep-colour" in sys.argv:
        #  The model saturates: Doldrum's muted roofs came back bright cyan. Keep the restyle's LIGHTNESS (its detail and
        #  shading) and take each pixel's HUE and CHROMA from the house as it is now, so the town keeps its colours.
        from skimage import color
        lab_new = color.rgb2lab(new.astype(float) / 255); lab_now = color.rgb2lab(now.astype(float) / 255)
        lab_new[..., 1:] = lab_now[..., 1:]
        new = np.clip(color.lab2rgb(lab_new) * 255, 0, 255)
    # 1. the kit: every secondary tile a house quadrant draws in a kit row (never the door)
    occ = {}                                          # kit tile -> {(tx,ty): [rgb, ...]}
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            m = ts.block(x, y)
            if m == DOOR:
                continue
            for k, t in enumerate(ts.entries(m)):
                i = t & 0x3FF
                if i < 640 or ((t >> 12) & 0xF) not in KIT_ROWS:
                    continue
                q = k % 4
                for ty in range(8):
                    for tx in range(8):
                        if ts.tile_px(t, tx, ty) == 0:
                            continue
                        sx = 7 - tx if (t >> 10) & 1 else tx; sy = 7 - ty if (t >> 11) & 1 else ty    # into the tile's own frame
                        px = new[(y - r[1]) * 16 + (q // 2) * 8 + ty, (x - r[0]) * 16 + (q % 2) * 8 + tx]
                        occ.setdefault(i, {}).setdefault((sx, sy), []).append(px)
    kit = sorted(occ)
    avg = {i: {p: np.mean(v, axis=0) for p, v in occ[i].items()} for i in kit}
    pal = fit_palette([c for i in kit for c in avg[i].values()])
    row = [(0, 0, 0)] + pal                           # index 0 transparent
    # 2. row 7 -> row 10's spare slots, so row 7 is free
    sec = ts.sec; st = ts.st.load()
    r10 = list(ts.pals[INTO_ROW]); r7 = ts.pals[FREE_ROW]
    remap = {}
    for k, slot in zip(range(1, 5), INTO_SLOTS):
        r10[slot] = r7[k]; remap[k] = slot
    moved = set()
    for b in range(len(sec) // 16):
        e = list(struct.unpack_from("<8H", sec, b * 16))
        for k, t in enumerate(e):
            if (t >> 12) & 0xF == FREE_ROW and (t & 0x3FF) >= 640:
                i = t & 0x3FF
                if i not in moved:
                    j = i - 640
                    for yy in range(8):
                        for xx in range(8):
                            v = st[(j % 16) * 8 + xx, (j // 16) * 8 + yy]
                            st[(j % 16) * 8 + xx, (j // 16) * 8 + yy] = remap.get(v, v)
                    moved.add(i)
                e[k] = (t & 0x0FFF) | (INTO_ROW << 12)
        struct.pack_into("<8H", sec, b * 16, *e)
    # 3. the kit tiles, redrawn in row 7: each pixel the nearest restyled colour; transparency kept
    P = np.array(pal, float)
    for i in kit:
        j = i - 640
        for yy in range(8):
            for xx in range(8):
                if st[(j % 16) * 8 + xx, (j // 16) * 8 + yy] == 0:
                    continue
                c = avg[i].get((xx, yy))
                if c is None:
                    continue                          # a pixel this house never shows: nearest by its old colour below
                st[(j % 16) * 8 + xx, (j // 16) * 8 + yy] = 1 + int(((P - c) ** 2).sum(1).argmin())
        # any pixel the house never drew (other buildings use it) maps by its OLD colour into the new row
    for i in kit:
        j = i - 640
        for yy in range(8):
            for xx in range(8):
                if (xx, yy) in avg[i]:
                    continue
                v = ts.st.getpixel(((j % 16) * 8 + xx, (j // 16) * 8 + yy))
                if v:
                    rows = [(t >> 12) & 0xF for b in range(len(sec) // 16) for t in struct.unpack_from("<8H", sec, b * 16) if (t & 0x3FF) == i]
                    old = np.array(ts.pals[rows[0] if rows else 12][v], float)
                    st[(j % 16) * 8 + xx, (j // 16) * 8 + yy] = 1 + int(((P - old) ** 2).sum(1).argmin())
    for b in range(len(sec) // 16):
        e = list(struct.unpack_from("<8H", sec, b * 16))
        for k, t in enumerate(e):
            if (t & 0x3FF) in occ:
                e[k] = (t & 0x0FFF) | (FREE_ROW << 12)
        struct.pack_into("<8H", sec, b * 16, *e)
    # 4. preview: the whole house row of Doldrum, now | after
    ts.pals[FREE_ROW] = row; ts.pals[INTO_ROW] = r10
    after = ts.render(8, 7, 39, 29)
    sheet = Image.new("RGB", (before.width, before.height * 2 + 8), (30, 30, 30))
    sheet.paste(before, (0, 0)); sheet.paste(after, (0, before.height + 8))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(os.path.join(OUT, "preview.png"))
    print("  %d kit tiles restyled into row %d; row %d's %d tiles moved to row %d slots %s; preview %s"
          % (len(kit), FREE_ROW, FREE_ROW, len(moved), INTO_ROW, INTO_SLOTS, os.path.join(OUT, "preview.png")))
    if write:
        ts.st.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(sec)
        write_pal(FREE_ROW, row); write_pal(INTO_ROW, r10)
        print("  written: tiles.png, metatiles.bin, palettes %02d and %02d (attributes, blocks and the map untouched)" % (FREE_ROW, INTO_ROW))


if __name__ == "__main__":
    if "--draft" in sys.argv:
        draft()
    elif "--pick" in sys.argv:
        apply(sys.argv[sys.argv.index("--pick") + 1], "--write" in sys.argv)
    else:
        print(__doc__)

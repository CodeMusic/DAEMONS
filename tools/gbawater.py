#!/usr/bin/env python3
"""The world's water in the pond's ripple dashes (T-61, vision.md 9.22).

    python3 tools/gbawater.py            # preview to /tmp/world_water.png (before | after)
    python3 tools/gbawater.py --write    # the two water groups' animation frames, and frame 0 in tiles.png

Every sea, lake and river in the General tileset is one of two animated 2x2
groups, placed in quadrant order and never flipped:

    416..419   open water, 72 blocks on 63 maps       anim/water_current_landwatersedge, tiles 0..3
    464..467   shallow island water, 43 blocks, 14 maps   anim/sandwatersedge, tiles 0..3

Only those eight tiles are redrawn, in all eight frames. The rocks, sand edges,
halos, currents and waterfalls that share the strips keep vanilla's drawing.

THE PATTERN IS BLANCHE'S POND'S LANGUAGE -- short ripple dashes on a 16-pixel
period -- given more to do at sea: three dashes of different lengths, each with
a lighter middle, two drifting right and one left so the surface shimmers
rather than slides, and a single speck. The pale water and the sea read as the
same water, one of them drained.

THE SAME TILE DRAWS IN TWO ROWS. Blocks put these tiles in row 4 (the blues) or
row 6 (the deeper blues), so the pattern only uses indices that mean the same
thing in both: 6 the body, 5 a step lighter, 3 lighter again, 1 the speck.
Open water is 6 with 5 dashes; shallow water is 5 with 3 dashes and 6 beneath.
"""
import importlib.util, json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbaground", os.path.join(ROOT, "tools", "gbaground.py"))
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
PREVIEW = "/tmp/world_water.png"
WRITE = "--write" in sys.argv
FRAMES = 8
BODY, DASH, CREST, SPECK = range(4)
GROUPS = [
    # (first tile, anim strip, role -> palette index)
    (416, "water_current_landwatersedge", {BODY: 6, DASH: 5, CREST: 3, SPECK: 1}),
    (464, "sandwatersedge", {BODY: 5, DASH: 3, CREST: 1, SPECK: 1}),
]
# (row, first u, last u, crest u's, drift per frame)
DASHES = [(2, 2, 7, (4, 5), 2), (7, 10, 13, (), -2), (12, 5, 9, (7,), 2)]
SPECKS = [(13, 4)]


def ripple(x, y, f):
    for v, u0, u1, crests, drift in DASHES:
        if y % 16 == v:
            u = (x - drift * f) % 16
            if u0 <= u <= u1:
                return CREST if u in crests else DASH
    if any((x % 16, y % 16) == (sx, sy) for sx, sy in SPECKS) and f % 4 < 2:
        return SPECK
    return BODY
PREVIEW_MAPS = [("SSAnne_Exterior_Layout", 0, 0, 24, 14), ("FourIsland_Layout", 0, 0, 24, 14)]


def water_tile(mapping, q, f):
    return [mapping[ripple((q % 2) * 8 + i % 8, (q // 2) * 8 + i // 8, f)] for i in range(64)]


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def secondary_dir(symbol):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    for d in os.listdir(os.path.join(GBA, "data/tilesets/secondary")):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(GBA, "data/tilesets/secondary", d)
    raise SystemExit("no directory for %s" % symbol)


def main():
    tiles = Image.open(os.path.join(PD, "tiles.png")); tp = tiles.load()
    new_tiles = tiles.copy(); ntp = new_tiles.load()
    strips = {}
    for first, strip, mapping in GROUPS:
        frames = []
        for f in range(FRAMES):
            path = os.path.join(PD, "anim", strip, "%d.png" % f)
            im = Image.open(path).copy(); ip = im.load()
            for q in range(4):
                for i, v in enumerate(water_tile(mapping, q, f)):
                    ip[(q % 2) * 8 + i % 8, (q // 2) * 8 + i // 8] = v
            frames.append((path, im))
        strips[strip] = frames
        for q in range(4):
            n = first + q
            for i, v in enumerate(water_tile(mapping, q, 0)):
                ntp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] = v

    # preview: two watery maps, as tiles.png draws them (frame 0)
    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    ppals = [read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)]
    panels = []
    for name, x0, y0, w, h in PREVIEW_MAPS:
        lay = layouts[name]; sd = secondary_dir(lay["secondary_tileset"])
        bd = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read(); W = lay["width"]
        sm = open(os.path.join(sd, "metatiles.bin"), "rb").read()
        st = Image.open(os.path.join(sd, "tiles.png")); stp = st.load()
        pals = ppals + [read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
        pair = []
        for prim_tiles in (tp, ntp):
            img = Image.new("RGB", (w * 16, h * 16)); o = img.load()
            for y in range(y0, y0 + h):
                for x in range(x0, x0 + w):
                    m = struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
                    e = struct.unpack_from("<8H", prim if m < 640 else sm, (m if m < 640 else m - 640) * 16)
                    for layer in (0, 1):
                        for q in range(4):
                            t = e[layer * 4 + q]; i = t & 0x3FF
                            src, j, hh = (prim_tiles, i, tiles.height) if i < 640 else (stp, i - 640, st.height)
                            for ty in range(8):
                                for tx in range(8):
                                    sy = (j // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                    v = src[(j % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                                    if layer and v == 0:
                                        continue
                                    o[(x - x0) * 16 + (q % 2) * 8 + tx, (y - y0) * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
            pair.append(img)
        panels.append(pair)
    sheet = Image.new("RGB", (panels[0][0].width * 2 + 8, sum(a.height for a, _ in panels) + 8 * (len(panels) - 1)), (30, 30, 30))
    yy = 0
    for a, b in panels:
        sheet.paste(a, (0, yy)); sheet.paste(b, (a.width + 8, yy)); yy += a.height + 8
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (before | after: %s)" % (PREVIEW, ", ".join(n for n, *_ in PREVIEW_MAPS)))

    if WRITE:
        for strip, frames in strips.items():
            for path, im in frames:
                im.save(path)
        new_tiles.save(os.path.join(PD, "tiles.png"))
        print("  written: %s frames 0..%d, tiles.png slots 416..419 and 464..467" % (" and ".join(strips), FRAMES - 1))


main()

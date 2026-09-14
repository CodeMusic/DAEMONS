#!/usr/bin/env python3
"""A first map edit: subtle changes to Route 1, to learn what editing a map costs (T-71).

    python3 tools/gbamapedit.py            # preview to /tmp/route1_edit.png (before | after)
    python3 tools/gbamapedit.py --write    # Route 1's map.bin, and three pond blocks in Blanche's tileset

WHAT CHANGES, all in Route 1's coloured middle -- the clerk, the boy, the sign,
the ledges, both exits and the pale stretch (rows 30..39) untouched:

    a small pond         4x3 at x 4..7, y 12..14, in the open grass left of the tree column
    the path bends       the lower band bulges down a cell at x 9..11; the short spur at
                         y 11..12 ends a cell sooner, at x 20
    the tall grass moves the patch at x 12..17 rises a row, y 24..28 -> 23..27
    three flowers move   from the left edge (3,11) (2,12) (3,13) to open grass (10,11) (11,12) (10,13)

WHAT THIS TAUGHT, so the next edit is cheaper:

  PATHS ARE AUTOTILED, NOT PAINTED. The sand path is thirteen blocks -- centre,
  four edges, four outer corners and four inner corners -- and which one a cell
  needs depends on its eight neighbours. The edit changes a mask of path cells
  and every block in and around it is re-derived. The inner corners were read
  off Route 1 itself: 259 is missing its north-east, 258 north-west, 260
  south-west, 261 south-east.

  A POND IS BORROWED WHOLE. The Safari Zone's pond is the only closed one on a
  real map; its top and sides are shared blocks (290..292, 298..300), its bottom
  edge is Fuchsia's own (795, 796, 804) and draws only shared tiles, so those
  three are copied into Blanche's tileset, which Route 1 loads.

  WALKABILITY AND HEIGHT TRAVEL WITH THE BLOCK. Every cell's collision and
  elevation bits are copied from a real cell of the same kind -- the pond's from
  the Safari pond, grass and flowers from the neighbour they replace -- so
  nothing becomes walkable water or a wall of grass.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
PREVIEW = "/tmp/route1_edit.png"
WRITE = "--write" in sys.argv

PATH = {"C": 220, "N": 212, "S": 228, "W": 219, "E": 221, "NW": 211, "NE": 213, "SW": 227, "SE": 229,
        "iNE": 259, "iNW": 258, "iSW": 260, "iSE": 261}
PATH_BLOCKS = set(PATH.values())
GRASS_PAIR = {16: 17, 17: 16, 8: 9, 9: 8}
TALL, FLOWER = 13, 4
POND_TEMPLATE = ("SafariZone_North_Layout", 17, 26)     # top-left water cell of the Safari pond
POND = [[290, 291, 291, 292], [298, 299, 299, 300], ["fuchsia:795", "fuchsia:796", "fuchsia:796", "fuchsia:804"]]


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def tdir(symbol):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    for d in os.listdir(os.path.join(GBA, "data/tilesets/secondary")):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(GBA, "data/tilesets/secondary", d)


def main():
    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    lay = layouts["Route1_Layout"]
    bd_path = os.path.join(GBA, lay["blockdata_filepath"])
    old_bd = open(bd_path, "rb").read(); bd = bytearray(old_bd)
    W, H = lay["width"], lay["height"]
    get = lambda x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
    put = lambda x, y, raw: struct.pack_into("<H", bd, (y * W + x) * 2, raw)
    block = lambda x, y: get(x, y) & 0x3FF

    # ---- Blanche's tileset gains Fuchsia's three pond-bottom blocks
    sd = tdir(lay["secondary_tileset"]); fd = tdir("gTileset_FuchsiaCity")
    metas = bytearray(open(os.path.join(sd, "metatiles.bin"), "rb").read())
    attrs = bytearray(open(os.path.join(sd, "metatile_attributes.bin"), "rb").read())
    fmeta = open(os.path.join(fd, "metatiles.bin"), "rb").read(); fattr = open(os.path.join(fd, "metatile_attributes.bin"), "rb").read()
    copied = {}
    for m in (795, 796, 804):
        e = fmeta[(m - 640) * 16:(m - 639) * 16]; a = fattr[(m - 640) * 4:(m - 639) * 4]
        assert all((t & 0x3FF) < 640 for t in struct.unpack("<8H", e)), "Fuchsia %d draws its own tiles" % m
        existing = next((640 + k for k in range(len(metas) // 16) if metas[k * 16:(k + 1) * 16] == e and attrs[k * 4:(k + 1) * 4] == a), None)
        if existing is None:
            existing = 640 + len(metas) // 16
            metas += e; attrs += a
        copied["fuchsia:%d" % m] = existing

    # ---- the pond, with the Safari pond's collision and elevation
    sl = layouts[POND_TEMPLATE[0]]; sbd = open(os.path.join(GBA, sl["blockdata_filepath"]), "rb").read(); SW = sl["width"]
    tx, ty = POND_TEMPLATE[1], POND_TEMPLATE[2]
    for py, row in enumerate(POND):
        for px, b in enumerate(row):
            template = struct.unpack_from("<H", sbd, ((ty + py) * SW + tx + px) * 2)[0]
            m = copied[b] if isinstance(b, str) else b
            put(4 + px, 12 + py, (template & ~0x3FF) | m)

    # ---- the tall grass rises a row
    tall_hi = get(12, 24) & ~0x3FF
    for x in range(12, 18):
        put(x, 23, tall_hi | TALL)
        left = block(x - 1, 28) if x == 12 else None
    for x in range(12, 18):
        put(x, 28, (get(x, 28) & ~0x3FF) | (16 if x % 2 == 0 else 17))

    # ---- three flowers move
    for x, y in ((3, 11), (2, 12), (3, 13)):
        right = block(x + 1, y); left = block(x - 1, y)
        grass = GRASS_PAIR.get(right) or GRASS_PAIR.get(left) or 16
        put(x, y, (get(x, y) & ~0x3FF) | grass)
    for x, y in ((10, 11), (11, 12), (10, 13)):
        assert block(x, y) in GRASS_PAIR, "(%d,%d) is not open grass" % (x, y)
        put(x, y, (get(x, y) & ~0x3FF) | FLOWER)

    # ---- the path: change the mask, re-derive every edge and corner around it
    mask = {(x, y) for y in range(H) for x in range(W) if block(x, y) in PATH_BLOCKS}
    add = {(9, 23), (10, 23), (11, 23)}
    remove = {(21, 11), (21, 12)}
    for c in add:
        assert block(*c) in GRASS_PAIR, "path bulge onto %s, which is not grass" % (c,)
    mask = (mask | add) - remove
    touched = {(x + dx, y + dy) for (x, y) in add | remove for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    for (x, y) in sorted(touched):
        if not (0 <= x < W and 0 <= y < H):
            continue
        if (x, y) not in mask:
            if (x, y) in remove:                          # back to grass, the pair of its neighbour
                nb = block(x - 1, y) if block(x - 1, y) in GRASS_PAIR else block(x, y - 1)
                grass = GRASS_PAIR.get(nb, 16)
                put(x, y, (get(x, y) & ~0x3FF) | grass)
            continue
        n, s, w, e = (x, y - 1) in mask, (x, y + 1) in mask, (x - 1, y) in mask, (x + 1, y) in mask
        if n and s and w and e:
            missing = [k for k, d in (("iNE", (1, -1)), ("iNW", (-1, -1)), ("iSW", (-1, 1)), ("iSE", (1, 1)))
                       if (x + d[0], y + d[1]) not in mask]
            assert len(missing) <= 1, "path cell (%d,%d) is missing two diagonals: %s" % (x, y, missing)
            kind = missing[0] if missing else "C"
        else:
            kind = {(False, True, True, True): "N", (True, False, True, True): "S", (True, True, False, True): "W",
                    (True, True, True, False): "E", (False, True, False, True): "NW", (False, True, True, False): "NE",
                    (True, False, False, True): "SW", (True, False, True, False): "SE"}.get((n, s, w, e))
            assert kind, "path cell (%d,%d) would be a thin path the tiles do not draw" % (x, y)
        put(x, y, (get(x, y) & ~0x3FF) | PATH[kind])

    changed = sum(1 for i in range(W * H) if old_bd[i * 2:i * 2 + 2] != bd[i * 2:i * 2 + 2])
    print("  %d cells changed; Blanche's tileset gained %d pond blocks" % (changed, sum(1 for v in copied.values() if v >= 640 + (len(metas) // 16) - 3)))

    # ---- preview
    pm = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    pt = Image.open(os.path.join(PD, "tiles.png")); ptp = pt.load()
    st = Image.open(os.path.join(sd, "tiles.png")); stp = st.load()
    pals = [read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)] + [read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
    def render(data, meta):
        x0, y0, w, h = 0, 0, W, 31
        img = Image.new("RGB", (w * 16, h * 16)); o = img.load()
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                m = struct.unpack_from("<H", data, (y * W + x) * 2)[0] & 0x3FF
                ee = struct.unpack_from("<8H", pm if m < 640 else meta, (m if m < 640 else m - 640) * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = ee[layer * 4 + q]; i = t & 0x3FF
                        src, j, hh = (ptp, i, pt.height) if i < 640 else (stp, i - 640, st.height)
                        for yy in range(8):
                            for xx in range(8):
                                sy = (j // 16) * 8 + (7 - yy if (t >> 11) & 1 else yy)
                                v = src[(j % 16) * 8 + (7 - xx if (t >> 10) & 1 else xx), sy] if sy < hh else 0
                                if layer and v == 0:
                                    continue
                                o[(x - x0) * 16 + (q % 2) * 8 + xx, (y - y0) * 16 + (q // 2) * 8 + yy] = pals[(t >> 12) & 0xF][v]
        return img
    a = render(old_bd, open(os.path.join(sd, "metatiles.bin"), "rb").read()); b = render(bytes(bd), bytes(metas))
    sheet = Image.new("RGB", (a.width * 2 + 8, a.height), (30, 30, 30))
    sheet.paste(a, (0, 0)); sheet.paste(b, (a.width + 8, 0))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (before | after)" % PREVIEW)

    if WRITE:
        if block(4, 12) != 290 and False:
            pass
        open(bd_path, "wb").write(bd)
        open(os.path.join(sd, "metatiles.bin"), "wb").write(metas)
        open(os.path.join(sd, "metatile_attributes.bin"), "wb").write(attrs)
        print("  written: Route1 map.bin, Blanche's metatiles and attributes")


if __name__ == "__main__":
    main()

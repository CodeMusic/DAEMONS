#!/usr/bin/env python3
"""The world's own tree: a round broadleaf in place of vanilla's conifer (T-61, vision.md 9.22).

    python3 tools/gbatrees.py            # report and preview to /tmp/world_trees.png (before | after)
    python3 tools/gbatrees.py --write    # the tree tiles in the General tileset

WHY THIS IS NOT A REPAINT. Vanilla's tree is 32 pixels wide and 48 tall -- two
cells by three -- and a tileset has no "tree" tile, only pieces of trees reused
across dozens of blocks, flipped and not. In a forest the trees stack every 32
pixels, each crown covering the trunk of the tree above, and a forest cell is
its own set of pieces: the bottom of one tree and the top of the next in one
tile. A new tree has to be drawn into every piece exactly where the old one was.

SO EVERY PIECE IS TRACED BACK TO A SCENE. Two scenes are built from the game's
own blocks: a standalone tree on grass (14/15, 30/31, 38/39), and a forest three
trees wide and three deep (28/29 over 20/21 over 28/29 over 20/21 over 36/37).
The trees' positions in each are known. Every tile drawn in row 0 is matched as
an 8x8 window into a scene -- at every 8-pixel position, mirrored or not --
comparing only the trees' own colours (indices 1..6), so grass under a tree
does not matter. The same window is then cut from the same scene built from
the new tree. A tile with tree colours that fits no window is left alone and
listed: bushes, hedges, flowers and tall grass are expected there.

THE NEW TREE is a round, lumpy broadleaf crown on a short trunk with a shadow at
its foot, lit from above so it is its own mirror image (vanilla reuses pieces
flipped). Where the old tree or its shadow was and the new one is not, a
bottom-layer tile gets grass and a top-layer tile gets transparency.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
PREVIEW = "/tmp/world_trees.png"
WRITE = "--write" in sys.argv

LIT, LEAF, DARK, DEEP, BARK, BARKD = 1, 2, 3, 4, 5, 6
MINT, GLIGHT, BASE, TUFT, TDARK = 8, 12, 13, 14, 15
TREE_COLOURS = {1, 2, 3, 4, 5, 6}
SHADOW_COLOURS = {MINT, TUFT, TDARK}
TW, TH = 32, 48
SCENES = [
    # (name, block grid, tree top-left positions in scene pixels, drawn back to front)
    ("standalone", [[16, 17, 16, 17, 16, 17], [16, 17, 14, 15, 16, 17], [16, 17, 30, 31, 16, 17], [16, 17, 38, 39, 16, 17]],
     [(32, 16)]),
    ("forest", [[28, 29, 28, 29, 28, 29], [20, 21, 20, 21, 20, 21], [28, 29, 28, 29, 28, 29],
                [20, 21, 20, 21, 20, 21], [36, 37, 36, 37, 36, 37]],
     [(x, y) for y in (-32, 0, 32) for x in (0, 32, 64)]),
    # a forest column with open ground on its right (vanilla's 31/23 edge pieces), and on its left (30/22)
    ("forest, right edge", [[28, 29, 28, 31, 16, 17], [20, 21, 20, 23, 16, 17], [28, 29, 28, 31, 16, 17],
                            [20, 21, 20, 23, 16, 17], [36, 37, 36, 37, 16, 17]],
     [(x, y) for y in (-32, 0, 32) for x in (0, 32)]),
    ("forest, left edge", [[16, 17, 30, 29, 28, 29], [16, 17, 22, 21, 20, 21], [16, 17, 30, 29, 28, 29],
                           [16, 17, 22, 21, 20, 21], [16, 17, 36, 37, 36, 37]],
     [(x, y) for y in (-32, 0, 32) for x in (32, 64)]),
]
PREVIEW_MAPS = [("Route1_Layout", 0, 8, 24, 14), ("ViridianCity_Layout", 0, 0, 24, 16), ("Route2_Layout", 0, 0, 24, 16)]


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def secondary_dir(symbol):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    for d in os.listdir(os.path.join(GBA, "data/tilesets/secondary")):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(GBA, "data/tilesets/secondary", d)


def broadleaf():
    """32x48, row-0 indices, 0 = nothing. Symmetric about x = 15.5."""
    t = [[0] * TW for _ in range(TH)]
    cx = 15.5
    for y in range(TH):                                   # the shadow at its foot
        for x in range(TW):
            if ((x - cx) / 12.5) ** 2 + ((y - 43.5) / 4.0) ** 2 <= 1:
                t[y][x] = TDARK if ((x - cx) / 9.5) ** 2 + ((y - 43.5) / 2.8) ** 2 <= 1 else TUFT
    for y in range(32, 46):                               # the trunk, mostly under the crown
        for x in range(13, 19):
            t[y][x] = BARKD if x in (13, 18) or y >= 44 else BARK
    for y in (40, 42):
        t[y][15] = BARKD; t[y][16] = BARKD
    # a crown big enough that in a forest, where trees stack every 32 pixels, each
    # crown runs into the next and the wood reads as one mass, not a stack of lollipops
    lobes = [(0.0, 17.0, 13.5), (-8.0, 21.0, 8.0), (8.0, 21.0, 8.0), (-7.0, 11.0, 7.0), (7.0, 11.0, 7.0),
             (0.0, 8.0, 6.5), (-11.0, 27.0, 5.5), (11.0, 27.0, 5.5), (-5.0, 31.0, 6.5), (5.0, 31.0, 6.5)]
    covering = lambda x, y: [(dx, cy, r) for dx, cy, r in lobes if (x - (cx + dx)) ** 2 + (y - cy) ** 2 <= r * r]
    crown = {(x, y) for y in range(TH) for x in range(TW) if covering(x + 0.5, y + 0.5)}
    for (x, y) in crown:
        if any((x + dx, y + dy) not in crown for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            t[y][x] = DEEP
            continue
        k = min((y + 0.5 - (cy - r)) / (2 * r) for dx, cy, r in covering(x + 0.5, y + 0.5))
        shade = LIT if k < 0.28 else LEAF if k < 0.62 else DARK
        mx = min(x, TW - 1 - x)                           # texture, mirrored
        if (mx * 5 + y * 3) % 7 == 0 and shade != LIT:
            shade -= 1
        elif (mx * 3 + y * 7) % 11 == 0 and shade != DARK:
            shade += 1
        t[y][x] = shade
    return t


def main():
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    tiles_img = Image.open(os.path.join(PD, "tiles.png")); tp = tiles_img.load()
    n_tiles = (tiles_img.height // 8) * 16
    tile = lambda n: [[tp[(n % 16) * 8 + x, (n // 16) * 8 + y] for x in range(8)] for y in range(8)]
    new_tree = broadleaf()

    scenes = []
    for name, grid, trees in SCENES:
        H, W = len(grid) * 16, len(grid[0]) * 16
        old = {0: [[None] * W for _ in range(H)], 1: [[None] * W for _ in range(H)]}
        for cy, row in enumerate(grid):
            for cxi, m in enumerate(row):
                e = struct.unpack_from("<8H", prim, m * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = e[layer * 4 + q]; i = t & 0x3FF
                        if layer and not i:
                            continue
                        for ty in range(8):
                            for tx in range(8):
                                v = tp[(i % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), (i // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)]
                                X, Y = cxi * 16 + (q % 2) * 8 + tx, cy * 16 + (q // 2) * 8 + ty
                                if v in TREE_COLOURS:
                                    old[layer][Y][X] = v
        shadow = [[False] * W for _ in range(H)]          # where a vanilla tree's foot shadow falls
        for tx0, ty0 in trees:
            for y in range(34, TH):
                for x in range(2, TW - 2):
                    X, Y = tx0 + x, ty0 + y
                    if 0 <= X < W and 0 <= Y < H:
                        shadow[Y][X] = True
        new = [[None] * W for _ in range(H)]
        for tx0, ty0 in trees:                             # back to front: upper trees first
            for y in range(TH):
                for x in range(TW):
                    v = new_tree[y][x]; X, Y = tx0 + x, ty0 + y
                    if v and 0 <= X < W and 0 <= Y < H:
                        if v in (TUFT, TDARK) and new[Y][X] is not None:
                            continue                       # a shadow never covers tree already drawn
                        new[Y][X] = v
        for mir in (False, True):
            f = (lambda img: [list(reversed(r)) for r in img]) if mir else (lambda img: img)
            scenes.append((name + (" mirrored" if mir else ""), {0: f(old[0]), 1: f(old[1])}, f(new), f(shadow), W, H))

    used_row0, top_layer, bottom_layer = set(), set(), set()
    for m in range(len(prim) // 16):
        for j, t in enumerate(struct.unpack_from("<8H", prim, m * 16)):
            if t & 0x3FF and (t >> 12) & 0xF == 0:
                used_row0.add(t & 0x3FF)
                (top_layer if j >= 4 else bottom_layer).add(t & 0x3FF)

    matches, unmatched = {}, []
    for n in sorted(used_row0):
        if n >= n_tiles:
            continue
        T = tile(n)
        if sum(1 for r in T for v in r if v in TREE_COLOURS) < 4:
            continue
        found = None
        layers = ([0] if n in bottom_layer else []) + ([1] if n in top_layer else [])
        for sc, layer in ((sc, layer) for layer in layers for sc in scenes):
            name, olds, new, shadow, W, H = sc
            old = olds[layer]
            for oy in range(0, H - 7, 8):
                for ox in range(0, W - 7, 8):
                    ok = True
                    for y in range(8):
                        for x in range(8):
                            tv, pv = T[y][x], old[oy + y][ox + x]
                            if (tv in TREE_COLOURS or pv is not None) and tv != pv:
                                ok = False; break
                        if not ok:
                            break
                    if ok:
                        found = (sc, ox, oy); break
                if found:
                    break
            if found:
                break
        if found:
            matches[n] = found
        else:
            unmatched.append(n)
    by_scene = {}
    for sc, ox, oy in matches.values():
        by_scene[sc[0]] = by_scene.get(sc[0], 0) + 1
    print("  %d tiles traced to a scene %s; %d with tree colours fit none: %s" % (len(matches), by_scene, len(unmatched), unmatched))

    new_img = tiles_img.copy(); np_ = new_img.load()
    for n, (sc, ox, oy) in matches.items():
        name, olds, new, shadow, W, H = sc
        old = [[a if a is not None else b for a, b in zip(r0, r1)] for r0, r1 in zip(olds[0], olds[1])]
        T = tile(n)
        is_top = n in top_layer and any(v == 0 for r in T for v in r)
        for y in range(8):
            for x in range(8):
                nv, ov, sh = new[oy + y][ox + x], old[oy + y][ox + x], shadow[oy + y][ox + x]
                if nv is not None:
                    v = 0 if (is_top and nv in (TUFT, TDARK)) else nv
                elif ov is not None or (sh and T[y][x] in SHADOW_COLOURS):
                    v = 0 if is_top else BASE
                else:
                    v = T[y][x]
                np_[(n % 16) * 8 + x, (n // 16) * 8 + y] = v

    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    ppals = [read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)]
    panels = []
    for name, x0, y0, w, h in PREVIEW_MAPS:
        lay = layouts[name]; sd = secondary_dir(lay["secondary_tileset"])
        bd = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read(); Wm, Hm = lay["width"], lay["height"]
        h = min(h, Hm - y0)
        sm = open(os.path.join(sd, "metatiles.bin"), "rb").read()
        st = Image.open(os.path.join(sd, "tiles.png")); stp = st.load()
        pals = ppals + [read_pal(os.path.join(sd, "palettes/%02d.pal" % k)) for k in range(7, 13)]
        pair = []
        for src_img in (tiles_img, new_img):
            sp = src_img.load()
            img = Image.new("RGB", (w * 16, h * 16)); o = img.load()
            for y in range(y0, y0 + h):
                for x in range(x0, x0 + w):
                    m = struct.unpack_from("<H", bd, (y * Wm + x) * 2)[0] & 0x3FF
                    e = struct.unpack_from("<8H", prim if m < 640 else sm, (m if m < 640 else m - 640) * 16)
                    for layer in (0, 1):
                        for q in range(4):
                            t = e[layer * 4 + q]; i = t & 0x3FF
                            src, j, hh = (sp, i, src_img.height) if i < 640 else (stp, i - 640, st.height)
                            for ty in range(8):
                                for tx in range(8):
                                    sy = (j // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                    v = src[(j % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                                    if layer and v == 0:
                                        continue
                                    o[(x - x0) * 16 + (q % 2) * 8 + tx, (y - y0) * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
            pair.append(img)
        panels.append(pair)
    width = max(a.width for a, _ in panels) * 2 + 8
    sheet = Image.new("RGB", (width, sum(a.height for a, _ in panels) + 8 * (len(panels) - 1)), (30, 30, 30)); yy = 0
    for a, b in panels:
        sheet.paste(a, (0, yy)); sheet.paste(b, (a.width + 8, yy)); yy += a.height + 8
    sheet.save(PREVIEW)
    print("  preview %s (before | after: %s)" % (PREVIEW, ", ".join(n for n, *_ in PREVIEW_MAPS)))

    if WRITE:
        new_img.save(os.path.join(PD, "tiles.png"))
        print("  written: tiles.png, %d tree tiles" % len(matches))


main()

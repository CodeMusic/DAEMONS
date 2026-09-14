#!/usr/bin/env python3
"""Blanche's pale runs out along its two roads (vision.md 9.22).

    python3 tools/gbaroutes.py            # preview to /tmp/blanche_roads.png (now | after)
    python3 tools/gbaroutes.py --write    # tiles, blocks, both routes' maps

Standing in Blanche you can see into Route 1 and Route 21 North, and at the map
edge the birches became conifers and the pond became vanilla's blue sea -- the
look switched exactly where the eye was. So the first stretch of each road is
drawn the way Blanche is, and the colour comes back inside the route, as you
walk out of the pale town:

    ROUTE 1, rows 30..39     birches, pale grass and tall grass, chalk path,
                             pale stone ledges, daisies, pale fences
    ROUTE 21 NORTH, rows 0..9   birches, pale grass, pale fences, and Blanche's
                             channel of clear water with its stone rim, until
                             just before it opens into the sea

Both stretches start and end on a tree boundary, so no tree is half one kind.

DERIVED THE WAY THE GROUND WAS (gbaground.py, whose drawing this imports): every
ground colour is given its job, so paths, tufts, tall grass and the curve of
every ledge keep vanilla's shape. Ledges become pale stone. Fences and the route
sign keep their own tiles and are pointed at Blanche's row 10, which is pale row
2 index for index. The tall grass keeps its behaviour, so wild daemons still
wait in it.

TILES ARE SHARED WITH BLANCHE'S where the pixels agree -- the birches, the
grass, the daisies, the water -- so the roads cost only what Blanche did not
already draw. Every changed cell gets a copy of its block with its attributes.
"""
import importlib.util, json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbaground", os.path.join(ROOT, "tools", "gbaground.py"))
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/blanche_roads.png"
WRITE = "--write" in sys.argv

STRETCHES = [("Route1_Layout", 30, 40), ("Route21_North_Layout", 0, 10)]
JOBS = dict(G.JOBS)
JOBS[5] = {10: G.CHALK, 1: G.SPECK, 6: G.SHADE, 7: G.SHADE, 8: G.SHADE, 9: G.SHADE, 11: G.SHADE, 12: G.SHADE,
           13: G.EDGE, 14: G.EDGE, 15: G.GRASS, 2: G.SHADE, 3: G.JOINT if hasattr(G, "JOINT") else G.SHADE}
JOBS[3] = {1: G.SPECK, 2: G.SPECK, 3: G.SHADE, 4: G.SHADE, 5: 14, 6: 9, 7: 9, 15: G.GRASS}   # a fence post in row 7
LEDGE = {4: 14, 9: 13, 10: 13, 11: 13, 12: 14, 13: 14, 14: 9}                               # row 1 rock -> pale stone
REPOINT_ROW = {2: 10}                                                                       # fences and signs
# Route 1's vertical fence ends, where a post stands in the same tile as grass and
# a tree: the post goes to the top layer in row 10, the grass and birch under it
POST_BLOCKS = {682, 683, 690, 698}
GROUND_ROWS = {0, 1, 3, 4, 5, 6}


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    pattr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    metas = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attrs = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    old_metas = bytes(metas)
    pt, st = Image.open(os.path.join(PD, "tiles.png")), Image.open(os.path.join(SD, "tiles.png"))
    ptp, stp = pt.load(), st.load()
    pals = {n: read_pal(os.path.join(PD if n < 7 else SD, "palettes/%02d.pal" % n)) for n in range(13)}
    rules = open(RULES).read()
    rule = r"(secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )(\d+)"
    num_tiles = int(re.search(rule, rules).group(2))

    def entries(m, src=None):
        return struct.unpack_from("<8H", prim if m < 640 else (src or metas), (m if m < 640 else m - 640) * 16)

    def attr(m):
        return bytes(pattr[m * 4:(m + 1) * 4]) if m < 640 else bytes(attrs[(m - 640) * 4:(m - 639) * 4])

    def vanilla_pixel(t, tx, ty):
        i = t & 0x3FF
        src, j, hh = (ptp, i, pt.height) if i < 640 else (stp, i - 640, st.height)
        sy = (j // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
        return src[(j % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0

    # every tile Blanche already has, so the roads reuse them
    slot = {}
    for n in range(num_tiles):
        key = bytes(stp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] for i in range(64))
        if not G.SLOT_WATER <= n < G.SLOT_WATER + 4:      # water is placed by quadrant, never matched
            slot.setdefault(key, n)
    tiles = []
    def put(px):
        key = bytes(px)
        if key not in slot:
            slot[key] = num_tiles + len(tiles); tiles.append(px)
        return slot[key]

    is_ground = lambda t: bool(t & 0x3FF) and ((t >> 12) & 0xF) in GROUND_ROWS
    maps, ids, copies = {}, {}, 0
    for name, y0, y1 in STRETCHES:
        lay = layouts[name]
        bd_path = os.path.join(GBA, lay["blockdata_filepath"]); bd = bytearray(open(bd_path, "rb").read())
        W, H = lay["width"], lay["height"]
        cell = lambda x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
        if WRITE and all(cell(x, y) not in G.TREE_BLOCKS for x in range(W) for y in range(y0, y1)):
            raise SystemExit("  already drawn: %s rows %d..%d have no vanilla trees left" % (name, y0, y1 - 1))
        CW, CH = W * 16, H * 16
        base = {}
        obj = {}
        post = {}
        blocks = {(x, y): cell(x, y) for x in range(W) for y in range(y0, y1)}
        for (x, y), m in blocks.items():
            e = entries(m)
            for q in range(4):
                t = e[q]
                for ty in range(8):
                    for tx in range(8):
                        X, Y = x * 16 + (q % 2) * 8 + tx, y * 16 + (q // 2) * 8 + ty
                        if m in G.POND_BLOCKS:
                            base[(X, Y)] = G.water(X, Y, 0)
                        elif m in G.TREE_BLOCKS:
                            base[(X, Y)] = G.TIP if (X % 16, Y % 16) in ((3, 5), (11, 13)) else G.TUFT if (X % 16, Y % 16) in ((4, 4), (12, 12)) else G.GRASS
                        elif m in POST_BLOCKS and (t >> 12) & 0xF == 3:
                            v = vanilla_pixel(t, tx, ty)
                            base[(X, Y)] = G.GRASS
                            if 1 <= v <= 7:
                                post[(X, Y)] = v
                        elif is_ground(t):
                            base[(X, Y)] = JOBS.get((t >> 12) & 0xF, {}).get(vanilla_pixel(t, tx, ty), G.GRASS)
                # ledges: row 1 rock in the top layer, recoloured into pale stone
                t = e[4 + q]
                if m not in G.POND_BLOCKS and t & 0x3FF and (t >> 12) & 0xF == 1:
                    for ty in range(8):
                        for tx in range(8):
                            v = vanilla_pixel(t, tx, ty)
                            if v:
                                obj[(x * 16 + (q % 2) * 8 + tx, y * 16 + (q // 2) * 8 + ty)] = (7, LEDGE.get(v, 13))
        # birches, top to bottom so a lower crown covers the trunk above it; only on tree cells
        tree = G.birch()
        anchors = {(x, y) for (x, y), m in blocks.items() if m in G.TREE_ANCHORS}
        # a tree whose left half a fence took over still has its right half: anchor it from that
        RIGHT, BOTTOM = {15, 21, 23, 29, 31, 37, 39}, {20, 21, 22, 23, 36, 37, 38, 39}
        reach = lambda ax, ay: {(ax + dx, ay + dy) for dx in (0, 1) for dy in (0, 1)}
        reached = set().union(*(reach(*a) for a in anchors)) if anchors else set()
        for (x, y), m in blocks.items():
            if m in G.TREE_BLOCKS and (x, y) not in reached:
                a = (x - (m in RIGHT), y - (m in BOTTOM))
                anchors.add(a); reached |= reach(*a)
        anchors = sorted(anchors, key=lambda a: (a[1], a[0]))
        covered = set()
        for ax, ay in anchors:
            for (px, py), c in tree.items():
                cx, cy = (ax * 16 + px) // 16, (ay * 16 + py) // 16
                if blocks.get((cx, cy)) in G.TREE_BLOCKS or blocks.get((cx, cy)) in POST_BLOCKS:
                    obj[(ax * 16 + px, ay * 16 + py)] = (12, c)
                    covered.add((cx, cy))
        missing = [c for c, m in blocks.items() if m in G.TREE_BLOCKS and c not in covered]
        assert not missing, "%s: tree cells no birch reaches: %s" % (name, missing[:6])
        bed = G.daisies(0)
        for (x, y), m in blocks.items():
            if m == G.FLOWER_BLOCK:
                for (px, py), c in bed.items():
                    obj[(x * 16 + px, y * 16 + py)] = c
            if m in G.POND_BLOCKS:
                e = entries(m)
                for q in range(4):
                    if not e[4 + q] & 0x3FF:
                        continue
                    left = blocks.get((x - 1, y), cell(x - 1, y) if x else -1) not in G.POND_BLOCKS
                    right = blocks.get((x + 1, y), cell(x + 1, y) if x < W - 1 else -1) not in G.POND_BLOCKS
                    for ty in range(8):
                        for tx in range(8):
                            X, Y = x * 16 + (q % 2) * 8 + tx, y * 16 + (q // 2) * 8 + ty
                            lx = X - x * 16
                            c = None
                            if left and lx < 8:
                                c = G.OUTLINE if lx == 0 else G.JOINT if lx == 6 or (lx > 0 and Y % 8 == 7) else None if lx == 7 else G.STONE
                            if right and lx >= 8 and c is None:
                                c = G.OUTLINE if lx == 15 else G.JOINT if lx == 9 or (lx < 15 and Y % 8 == 7) else None if lx == 8 else G.STONE
                            if c is not None:
                                obj[(X, Y)] = (7, c)

        def quadrant(x, y, q, what):
            rows, px = set(), []
            for i in range(64):
                X, Y = x * 16 + (q % 2) * 8 + i % 8, y * 16 + (q // 2) * 8 + i // 8
                o = obj.get((X, Y))
                if o is not None and what != "base":
                    rows.add(o[0]); px.append(o[1])
                elif what == "obj":
                    px.append(0)
                else:
                    b = base.get((X, Y), G.GRASS); px.append(b)
                    if b > 8:
                        rows.add(7)
            if len(rows) > 1:
                raise SystemExit("  !! %s (%d,%d) q%d mixes rows %s" % (name, x, y, q, sorted(rows)))
            return px, (rows.pop() if rows else 7)

        for (x, y), m in sorted(blocks.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            e = list(entries(m)); out = list(e)
            for q in range(4):
                b, t = e[q], e[4 + q]
                bottom, top = is_ground(b), is_ground(t)
                if t & 0x3FF and (t >> 12) & 0xF in REPOINT_ROW:
                    out[4 + q] = (t & 0x0FFF) | (REPOINT_ROW[(t >> 12) & 0xF] << 12)
                if top:
                    px, row = quadrant(x, y, q, "obj")
                    out[4 + q] = (put(px) + 640) | (row << 12) if any(px) else 0
                    if bottom:
                        px, row = quadrant(x, y, q, "base")
                        out[q] = (put(px) + 640) | (row << 12)
                elif bottom:
                    px, row = quadrant(x, y, q, "base" if t & 0x3FF else "all")
                    out[q] = (put(px) + 640) | (row << 12)
                if m in G.POND_BLOCKS and bottom:
                    out[q] = (640 + G.SLOT_WATER + q) | (7 << 12)
                if m in POST_BLOCKS:
                    px, row = quadrant(x, y, q, "all")
                    out[q] = (put(px) + 640) | (row << 12)
                    pp = [post.get((x * 16 + (q % 2) * 8 + i % 8, y * 16 + (q // 2) * 8 + i // 8), 0) for i in range(64)]
                    out[4 + q] = ((put(pp) + 640) | (10 << 12)) if any(pp) else 0
            out = tuple(out)
            if out == tuple(e):
                continue
            key = (out, attr(m))
            if key not in ids:
                ids[key] = 640 + len(metas) // 16
                metas += struct.pack("<8H", *out); attrs += attr(m); copies += 1
            raw = struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
            struct.pack_into("<H", bd, (y * W + x) * 2, (raw & ~0x3FF) | ids[key])
        maps[name] = (bd_path, bd, W, y0, y1)

    total = num_tiles + len(tiles)
    print("  %d tiles drawn (slots %d..%d), %d blocks copied; tileset now %d/384 tiles, %d/384 blocks"
          % (len(tiles), num_tiles, total - 1, copies, total, len(metas) // 16))
    assert total <= 384 and len(metas) // 16 <= 384

    grown = Image.new("P", (128, ((total + 15) // 16) * 8)); grown.putpalette(st.getpalette()); grown.paste(st, (0, 0)); gp = grown.load()
    for n, px in enumerate(tiles):
        s = num_tiles + n
        for i, v in enumerate(px):
            gp[(s % 16) * 8 + i % 8, (s // 16) * 8 + i // 8] = v

    def render(name, metas_now, tiles_img, bd_now, W, y0, y1):
        img = Image.new("RGB", (W * 16, (y1 - y0) * 16)); o = img.load(); tl = tiles_img.load()
        for y in range(y0, y1):
            for x in range(W):
                m = struct.unpack_from("<H", bd_now, (y * W + x) * 2)[0] & 0x3FF
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
                                o[x * 16 + (q % 2) * 8 + tx, (y - y0) * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
        return img
    panels = []
    for name, (bd_path, bd, W, y0, y1) in maps.items():
        panels.append((render(name, old_metas, st, open(bd_path, "rb").read(), W, y0, y1), render(name, metas, grown, bd, W, y0, y1)))
    width = max(a.width for a, _ in panels) * 2 + 8
    height = sum(a.height for a, _ in panels) + 8 * (len(panels) - 1)
    sheet = Image.new("RGB", (width, height), (30, 30, 30)); yy = 0
    for a, b in panels:
        sheet.paste(a, (0, yy)); sheet.paste(b, (a.width + 8, yy)); yy += a.height + 8
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (now | after; Route 1's end above, Route 21 North's start below)" % PREVIEW)

    if WRITE:
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(metas)
        open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attrs)
        for name, (bd_path, bd, W, y0, y1) in maps.items():
            open(bd_path, "wb").write(bd)
        open(RULES, "w").write(re.sub(rule, lambda mm: mm.group(1) + str(total), rules))
        print("  written: tiles.png, metatiles, attributes, %s, -num_tiles %d" % (", ".join(maps), total))


if __name__ == "__main__":
    main()

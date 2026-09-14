#!/usr/bin/env python3
"""Vanilla boards that still carried red squiggle lettering (T-86; vision.md 4.4, 9.22, 9.23).

    python3 tools/gbaislandsigns.py            # preview to /tmp/island_signs.png (before | after)
    python3 tools/gbaislandsigns.py --write    # tiles, blocks, the two maps

QUICKSILVER'S LAB BOARD (9..10, 9..10). Reading it says SCORN SOLUTIONS, then
that gold leaf has been laid over something and where it has lifted the older
letters show, then CLEAR LABORATORY (4.4, T-30). So the board is drawn as that:
gold leaf with SCORN raised on it, and its lower right corner peeled back in a
curl, showing a paler board beneath with fragments of darker, older lettering --
too little to read. The picture shows the lifting; the text box names it. Row 5,
whose golds these are, on the top layer over the lab wall, with its two legs in
the row below.

BRAZEN'S TWO RED ROUNDELS (42 and 50, 13..14) were vanilla's GYM markers in front
of the PROOF HALL and the BENCHMARK. The BENCHMARK's becomes the MARK board every
other BENCHMARK town has; the PROOF HALL's reads QED, which is how a proof ends.
Both are copies of Brazen's own sign blocks, which the two had shared.

ONE ISLAND'S NET CENTER BOARD (15, 6). It is General's block 2, the ordinary
signpost every map shares, so it is copied into the Sevii 1-3 tileset rather
than redrawn: the board reads NET in the 3x5 face, in row 2's greys.

Each changed cell gets a new block with the original's bottom layer, attributes
and collision; tiles go into slots no block draws, else onto the end. Neither
board is within seven cells of a connection (engine.md trap 14). A board already
drawn is left alone.
"""
import importlib.util, json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbaemblems", os.path.join(ROOT, "tools", "gbaemblems.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/island_signs.png"
WRITE = "--write" in sys.argv


def tdir(symbol):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    for d in os.listdir(os.path.join(GBA, "data/tilesets/secondary")):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(GBA, "data/tilesets/secondary", d)


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def grid(w, h):
    return [[0] * w for _ in range(h)]


def rect(g, x0, y0, x1, y1, v):
    for y in range(max(0, y0), min(len(g), y1 + 1)):
        for x in range(max(0, x0), min(len(g[0]), x1 + 1)):
            g[y][x] = v


def word(g, x0, y0, text, v, keep=lambda x, y: True):
    for y, row in enumerate(E.word(text)):
        for x, b in enumerate(row):
            if b and keep(x0 + x, y0 + y):
                g[y0 + y][x0 + x] = v


def gold_leaf_board():
    """32x16 in row 5: board y 0..10, legs y 11..15."""
    WHITE, LIGHT, GREY, DARK, OUT, CREAM, GOLD, GOLDD, AMBER, BRIGHT, GOLD2, GOLD3 = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    g = grid(32, 16)
    rect(g, 0, 0, 31, 10, OUT); rect(g, 1, 1, 30, 9, AMBER)       # an amber frame round the leaf
    lifted = lambda x, y: (x - 20) + (y - 1) * 1.6 >= 13        # the peeled corner, lower right
    for y in range(2, 9):
        for x in range(2, 30):
            if lifted(x, y):
                g[y][x] = LIGHT if (x + y) % 5 else WHITE    # the older, paler board underneath
            else:                                            # the leaf: bright on top, brushed, deeper below
                g[y][x] = BRIGHT if y == 2 else BRIGHT if (x - y) % 6 == 0 else GOLD3 if y < 6 else GOLD
    word(g, 6, 3, "SCORN", DARK, keep=lambda x, y: not lifted(x, y))
    for y, row in enumerate(E.word("SCORN")):                    # each gold letter casts a line of amber under it
        for x, b in enumerate(row):
            if b and not lifted(6 + x, 4 + y) and g[4 + y][6 + x] not in (DARK,) and 4 + y <= 8:
                g[4 + y][6 + x] = AMBER
    for x0, y0, text in ((21, 6, "L"), (25, 6, "A")):              # older letters, cut off by the edge of the leaf
        word(g, x0, y0, text, DARK, keep=lambda x, y: lifted(x, y) and y <= 9)
    edge = [(x, y) for y in range(1, 10) for x in range(1, 31) if lifted(x, y) and not lifted(x - 1, y)]
    for x, y in edge:                                                # the curl: a bright rolled lip on the leaf's edge
        g[y][x - 1] = CREAM
        if x - 2 >= 1:
            g[y][x - 2] = GOLDD
    for x in (8, 23):                                                # two legs
        rect(g, x, 11, x + 1, 14, GREY); rect(g, x + 1, 11, x + 1, 14, DARK)
    rect(g, 6, 15, 25, 15, LIGHT)                                    # its shadow
    return g, 5


def net_board():
    """16x16 in row 2: a board on two legs reading NET."""
    WHITE, PALE, LIGHT, MID, GREY, DARK, OUT = 1, 2, 3, 4, 5, 6, 7
    g = grid(16, 16)
    rect(g, 1, 1, 14, 11, OUT); rect(g, 2, 2, 13, 10, WHITE)
    rect(g, 2, 2, 13, 2, PALE); rect(g, 2, 10, 13, 10, LIGHT)
    word(g, 3, 4, "NET", OUT)
    for x in (3, 11):
        rect(g, x, 12, x + 1, 14, GREY); rect(g, x + 1, 12, x + 1, 14, DARK)
    rect(g, 2, 15, 13, 15, MID)
    return g, 2


def mark_board():
    """16x24 in row 5: the BENCHMARK's board, as the other seven towns have it, reading MARK."""
    WHITE, LIGHT, GREY, DARK, OUT, BRIGHT, GOLD3 = 1, 2, 3, 4, 5, 10, 12
    g = grid(16, 24)
    rect(g, 0, 1, 15, 14, OUT); rect(g, 1, 2, 14, 13, WHITE)
    rect(g, 1, 2, 14, 2, BRIGHT); rect(g, 1, 13, 14, 13, LIGHT)
    word(g, 1, 6, "MARK", OUT)
    rect(g, 2, 12, 13, 12, GOLD3)
    for x in (3, 11):
        rect(g, x, 15, x + 1, 22, GREY); rect(g, x, 15, x, 22, LIGHT)
        rect(g, x - 1, 23, x + 2, 23, DARK)
    return g, 5


def qed_board():
    """16x24 in row 2: the PROOF HALL's board. A proof ends in QED; the board says only that."""
    WHITE, PALE, LIGHT, MID, GREY, DARK, OUT = 1, 2, 3, 4, 5, 6, 7
    g = grid(16, 24)
    rect(g, 1, 1, 14, 14, OUT); rect(g, 2, 2, 13, 13, WHITE)
    rect(g, 2, 2, 13, 2, PALE); rect(g, 2, 13, 13, 13, LIGHT)
    word(g, 3, 6, "QED", OUT)
    rect(g, 3, 12, 12, 12, MID)
    for x in (3, 11):
        rect(g, x, 15, x + 1, 22, GREY); rect(g, x + 1, 15, x + 1, 22, DARK)
        rect(g, x - 1, 23, x + 2, 23, MID)
    return g, 2


# (map, tileset, art, [(cell x, cell y, art x of the cell's left, art y of the cell's top)])
SIGNS = [
    ("CinnabarIsland", "gTileset_CinnabarIsland", gold_leaf_board, [(9, 9, 0, -8), (10, 9, 16, -8), (9, 10, 0, 8), (10, 10, 16, 8)]),
    ("OneIsland", "gTileset_SeviiIslands123", net_board, [(15, 6, 0, 0)]),
    ("SaffronCity", "gTileset_SaffronCity", mark_board, [(50, 13, 0, -8), (50, 14, 0, 8)]),
    ("SaffronCity", "gTileset_SaffronCity", qed_board, [(42, 13, 0, -8), (42, 14, 0, 8)]),
]


def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    pattr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    rules = open(RULES).read()
    pt = Image.open(os.path.join(PD, "tiles.png")); ptp = pt.load()
    panels, writes = [], []
    maps_open, sets_open = {}, {}
    for mp, ts, artf, cells in SIGNS:
        art, row = artf()
        j = json.load(open(os.path.join(GBA, "data/maps", mp, "map.json"))); l = layouts[j["layout"]]
        bd_path = os.path.join(GBA, l["blockdata_filepath"]); W = l["width"]
        bd = maps_open.setdefault(bd_path, bytearray(open(bd_path, "rb").read()))
        d = tdir(ts)
        if d not in sets_open:
            key_ = "secondary/%s/tiles.4bpp: %%.4bpp: %%.png\n\t$(GFX) $< $@ -num_tiles " % os.path.basename(d)
            at_ = rules.index(key_) + len(key_)
            sets_open[d] = dict(meta=bytearray(open(os.path.join(d, "metatiles.bin"), "rb").read()),
                                attr=bytearray(open(os.path.join(d, "metatile_attributes.bin"), "rb").read()),
                                img=Image.open(os.path.join(d, "tiles.png")), key=key_, n=int(rules[at_:].split()[0]), total=None,
                                disk_meta=open(os.path.join(d, "metatiles.bin"), "rb").read(), disk_img=Image.open(os.path.join(d, "tiles.png")))
        st_ = sets_open[d]
        meta, attr, key, img = st_["meta"], st_["attr"], st_["key"], st_["img"]
        n = st_["total"] or st_["n"]; ip = img.load()
        referenced = {(struct.unpack_from("<H", meta, i * 2)[0] & 0x3FF) - 640 for i in range(len(meta) // 2)}
        free = [s for s in range(n) if s not in referenced and (s // 16 + 1) * 8 <= img.height] + list(range(n, 384))
        placed = {}

        def quadrant(ax, ay, q):
            px = []
            for k in range(64):
                x, y = ax + (q % 2) * 8 + k % 8, ay + (q // 2) * 8 + k // 8
                px.append(art[y][x] if 0 <= x < len(art[0]) and 0 <= y < len(art) else 0)
            return tuple(px)

        before = bytes(bd); new_tiles = {}
        already = True
        plan = []
        for x, y, ax, ay in cells:
            raw = struct.unpack_from("<H", bd, (y * W + x) * 2)[0]; m = raw & 0x3FF
            e = list(struct.unpack_from("<8H", prim if m < 640 else meta, (m if m < 640 else m - 640) * 16))
            a = pattr[m * 4:(m + 1) * 4] if m < 640 else bytes(attr[(m - 640) * 4:(m - 639) * 4])
            want = [quadrant(ax, ay, q) for q in range(4)]
            for q in range(4):
                t = e[4 + q]
                if any(want[q]):
                    if not ((t & 0x3FF) >= 640 and (t >> 12) == row):
                        already = False
                    else:
                        s = (t & 0x3FF) - 640
                        if tuple(ip[(s % 16) * 8 + k % 8, (s // 16) * 8 + k // 8] for k in range(64)) != want[q]:
                            already = False
            plan.append((x, y, raw, e, a, want))
        if already:
            print("  %s: the board is already drawn" % mp)
        else:
            for x, y, raw, e, a, want in plan:
                for q in range(4):
                    if any(want[q]):
                        if want[q] not in placed:
                            s = free.pop(0); placed[want[q]] = s; new_tiles[s] = want[q]
                        e[4 + q] = (640 + placed[want[q]]) | (row << 12)
                    elif (e[4 + q] >> 12) in (2, 5) or (e[4 + q] & 0x3FF) in (304, 305, 320, 321):
                        e[4 + q] = 0                        # the old board's leftovers go
                nid = 640 + len(meta) // 16
                meta += struct.pack("<8H", *e); attr += a
                struct.pack_into("<H", bd, (y * W + x) * 2, (raw & ~0x3FF) | nid)
            total = max([n] + [s + 1 for s in new_tiles])
            assert total <= 384 and len(meta) // 16 <= 384
            g = Image.new("P", (128, max(img.height, ((total + 15) // 16) * 8))); g.putpalette(img.getpalette()); g.paste(img, (0, 0)); gp = g.load()
            for s, px in new_tiles.items():
                for k, v in enumerate(px):
                    gp[(s % 16) * 8 + k % 8, (s // 16) * 8 + k // 8] = v
            print("  %s: %d tiles, %d blocks" % (mp, len(new_tiles), len(plan)))
            st_["img"], st_["total"] = g, total
            img, ip = g, g.load()
            if d not in [w[0] for w in writes]:
                writes.append((d, bd_path))
            elif bd_path not in [w[1] for w in writes]:
                writes.append((d, bd_path))

        # preview around the board
        pals = [read_pal(os.path.join(PD, "palettes/%02d.pal" % k)) for k in range(7)] + [read_pal(os.path.join(d, "palettes/%02d.pal" % k)) for k in range(7, 13)]
        old_meta, old_img = st_["disk_meta"], st_["disk_img"]
        def render(data, mt, timg):
            tp = timg.load()
            x0, y0 = min(c[0] for c in cells) - 3, min(c[1] for c in cells) - 3
            out = Image.new("RGB", (8 * 16, 7 * 16)); o = out.load()
            for yy in range(7):
                for xx in range(8):
                    X_, Y_ = x0 + xx, y0 + yy
                    if not (0 <= X_ < W and 0 <= Y_ < l["height"]):
                        continue
                    m = struct.unpack_from("<H", data, (Y_ * W + X_) * 2)[0] & 0x3FF
                    buf, k = (prim, m) if m < 640 else (mt, m - 640)
                    if (k + 1) * 16 > len(buf):
                        continue
                    ee = struct.unpack_from("<8H", buf, k * 16)
                    for layer in (0, 1):
                        for q in range(4):
                            t = ee[layer * 4 + q]; i = t & 0x3FF
                            src, jj, hh = (ptp, i, pt.height) if i < 640 else (tp, i - 640, timg.height)
                            for ty in range(8):
                                for tx in range(8):
                                    sy = (jj // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                    v = src[(jj % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                                    if layer and v == 0:
                                        continue
                                    o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
            return out
        panels.append((render(before, old_meta, old_img), render(bytes(bd), bytes(meta), img)))

    sheet = Image.new("RGB", (8 * 16 * 2 + 8, (7 * 16 + 8) * len(panels)), (30, 30, 30))
    for k, (a, b) in enumerate(panels):
        sheet.paste(a, (0, k * (7 * 16 + 8))); sheet.paste(b, (8 * 16 + 8, k * (7 * 16 + 8)))
    sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save(PREVIEW)
    print("  preview %s (before | after: Quicksilver, One Island)" % PREVIEW)

    if WRITE:
        done_sets = set()
        for d, bd_path in writes:
            open(bd_path, "wb").write(maps_open[bd_path])
            if d in done_sets:
                continue
            done_sets.add(d); st_ = sets_open[d]
            st_["img"].save(os.path.join(d, "tiles.png"))
            open(os.path.join(d, "metatiles.bin"), "wb").write(st_["meta"]); open(os.path.join(d, "metatile_attributes.bin"), "wb").write(st_["attr"])
            if st_["total"] and st_["total"] > st_["n"]:
                rules = open(RULES).read(); at = rules.index(st_["key"]) + len(st_["key"])
                open(RULES, "w").write(rules[:at] + str(st_["total"]) + rules[at + len(str(st_["n"])):])
        print("  written: %d boards" % len(writes))


if __name__ == "__main__":
    main()

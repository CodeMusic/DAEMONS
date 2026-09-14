#!/usr/bin/env python3
"""The sandbar across Route 21, where the pale sea meets the blue (T-73, T-74; vision.md 9.22).

    python3 tools/gbasandbar.py            # preview to /tmp/sandbar.png (seen from North | seen from South)
    python3 tools/gbasandbar.py --write    # both routes' maps, Blanche's and Quicksilver's tilesets

PLAYTEST, 2026-09-14. Sailing from Route 21 North into South garbled the pale
water, and the line where pale became blue looked rigid.

WHY IT GARBLED. A connection draws seven rows of the neighbour with THIS map's
tileset (gbaseams.py). Route 21 North loads Blanche's tileset and South loads
Quicksilver's, so from South the pale water's ids meant Quicksilver blocks.

WHY AN ISLAND, NOT A LINE. The map border is the same block everywhere round a
map, and you can see it whenever you are within seven cells of a side: North's
border is pale water and South's is blue. So any water the player can see has to
match the border of the map they are standing in -- pale everywhere North, blue
everywhere South -- and water in view at the moment of crossing would change
colour under them. The only thing that satisfies both is land across the whole
width, deep enough that no water is in view as you step over the join:

    North row 41        the top edge, pale water behind gold sand
    North 42            sand, and the hatch at x 11
    North 43 .. South 4 sand, the join in the middle of it
    South 5             the bottom edge
    South 6             open water

The sand is gold all the way, not chalk: its body is the primary tileset's, which
draws the same from either side, and a bar that was chalk on one half and gold
on the other would be the seam this replaces.

THE ONE TRICK. The two sides and the bottom edge sit inside both seven-row bands,
and each has a sliver of water beside the border. So those five blocks, and the
water row below, are given the SAME ids in both tilesets and a different drawing
in each: in Blanche's the sliver is pale, in Quicksilver's it is blue. Whichever
map you stand in, the sliver matches your border. Quicksilver's tileset is padded
with blank blocks up to those ids. gbaseams.py is told about exactly these ids.

In Blanche's tileset a pale edge is two layers: the pale water animation below
(slots 804..807) and vanilla's sand edge on top, its sand in four unused slots of
row 12 and its water transparent, on the COVERED layer so it stays under the
player. The hatch is sand below and a ladder in row 10's greys on top, behaviour
LADDER, so stepping on it warps.
"""
import importlib.util, json, os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbaground", os.path.join(ROOT, "tools", "gbaground.py"))
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
BD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
CD = os.path.join(GBA, "data/tilesets/secondary/cinnabar_island")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/sandbar.png"
WRITE = "--write" in sys.argv

W = 24
NORTH_TOP, NORTH_H = 41, 50          # the bar starts at North row 41
SOUTH_EDGE, SOUTH_WATER = 5, 6       # its bottom edge and the water under it, South rows
HATCH_AT = (11, 42)
SAND_HI, WATER_HI = 12, 4            # collision/elevation bits: sand walks at 3, water at 1

EDGE = {"NW": 268, "N": 269, "NE": 270, "W": 276, "C": 277, "E": 278, "SW": 284, "S": 285, "SE": 286}
IDS = {"W": 947, "E": 948, "SW": 949, "S": 950, "SE": 951, "NW": 952, "N": 953, "NE": 954, "HATCH": 955}
PALE_WATER, BLUE_WATER = 880, 299    # Blanche's shallow pale water, the primary blue
DUAL = {IDS[k]: EDGE[k] for k in ("W", "E", "SW", "S", "SE")}
DUAL[PALE_WATER] = BLUE_WATER        # Quicksilver's block at this id draws this primary block

SEA_EDGE_TILES = range(424, 430)
WATER_IDX = {1, 3, 5, 6}             # row 4's water; the rest of an edge tile is shore and sand
TOP_ROW = 12
TOP_SLOTS = {13: 5, 14: 6, 15: 7, 4: 8, 7: 8}
HATCH_ROW = 10
HATCH_ROLES = {"O": 7, "H": 2, "R": 4, "D": 6, "L": 3}
HATCH = ["................",
         "..OOOOOOOOOOOO..",
         ".OHHHHHHHHHHHHO.",
         ".OHRRRRRRRRRRRO.",
         ".ORODDDDDDDDORO.",
         ".ORODLDDDDLDORO.",
         ".ORODLLLLLLDORO.",
         ".ORODLDDDDLDORO.",
         ".ORODLDDDDLDORO.",
         ".ORODLLLLLLDORO.",
         ".ORODLDDDDLDORO.",
         ".ORODLDDDDLDORO.",
         ".ORODLLLLLLDORO.",
         ".ORRRRRRRRRRRRO.",
         ".OOOOOOOOOOOOOO.",
         "................"]
MB_LADDER = 0x61
LAYER_COVERED = 1


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, cols):
    open(path, "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols))


def num_tiles_rule(rules, name):
    key = "secondary/%s/tiles.4bpp: %%.4bpp: %%.png\n\t$(GFX) $< $@ -num_tiles " % name
    at = rules.index(key) + len(key)
    return at, int(rules[at:].split()[0])


def main():
    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    north, south = layouts["Route21_North_Layout"], layouts["Route21_South_Layout"]
    nb_path, sb_path = os.path.join(GBA, north["blockdata_filepath"]), os.path.join(GBA, south["blockdata_filepath"])
    old_n, old_s = open(nb_path, "rb").read(), open(sb_path, "rb").read()
    nbd, sbd = bytearray(old_n), bytearray(old_s)
    if struct.unpack_from("<H", nbd, (NORTH_TOP * W) * 2)[0] & 0x3FF == IDS["NW"]:
        print("  the sandbar is already drawn"); return

    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    pattr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    pt = Image.open(os.path.join(PD, "tiles.png")); ptp = pt.load()
    bmeta = bytearray(open(os.path.join(BD, "metatiles.bin"), "rb").read())
    battr = bytearray(open(os.path.join(BD, "metatile_attributes.bin"), "rb").read())
    cmeta = bytearray(open(os.path.join(CD, "metatiles.bin"), "rb").read())
    cattr = bytearray(open(os.path.join(CD, "metatile_attributes.bin"), "rb").read())
    old_bmeta, old_cmeta, old_battr, old_cattr = bytes(bmeta), bytes(cmeta), bytes(battr), bytes(cattr)
    assert len(bmeta) // 16 == IDS["W"] - 640, "Blanche's tileset has %d blocks; the ids here assume %d" % (len(bmeta) // 16, IDS["W"] - 640)
    assert len(cmeta) // 16 <= min(DUAL) - 640, "Quicksilver's tileset already reaches id %d" % (640 + len(cmeta) // 16)
    pentries = lambda m: list(struct.unpack_from("<8H", prim, m * 16))
    pattr_of = lambda m: struct.unpack_from("<I", pattr, m * 4)[0]

    rules = open(RULES).read()
    at, num_tiles = num_tiles_rule(rules, "pallet_town")
    bt = Image.open(os.path.join(BD, "tiles.png")); btp = bt.load()
    have = {bytes(btp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] for i in range(64)): n for n in range(num_tiles)}
    new_tiles = []
    def tile(px):
        key = bytes(px)
        if key not in have:
            have[key] = num_tiles + len(new_tiles); new_tiles.append(key)
        return 640 + have[key]

    # ---- row 12's four slots must be free, and row 10's hatch colours are already there
    row12 = read_pal(os.path.join(BD, "palettes/%02d.pal" % TOP_ROW))
    for k in range(len(bmeta) // 16):
        for t in struct.unpack_from("<8H", bmeta, k * 16):
            if (t >> 12) & 0xF == TOP_ROW and t & 0x3FF >= 640:
                j = (t & 0x3FF) - 640
                clash = {btp[(j % 16) * 8 + i % 8, (j // 16) * 8 + i // 8] for i in range(64)} & set(TOP_SLOTS.values())
                assert not clash, "row 12 slots %s are drawn by block %d" % (sorted(clash), 640 + k)
    row4 = read_pal(os.path.join(PD, "palettes/04.pal")); row7 = read_pal(os.path.join(BD, "palettes/07.pal"))
    for src, slot in TOP_SLOTS.items():
        row12[slot] = row7[11] if src in (4, 7) else row4[src]

    # ---- Blanche's blocks: pale water below, vanilla's sand edge on top
    def pale_edge(kind):
        e = pentries(EDGE[kind]); out = [0] * 8
        for q in range(4):
            t = e[q]; i, row = t & 0x3FF, (t >> 12) & 0xF
            if row == 4 and i in SEA_EDGE_TILES:
                src = [ptp[(i % 16) * 8 + k % 8, (i // 16) * 8 + k // 8] for k in range(64)]
                assert set(src) <= WATER_IDX | set(TOP_SLOTS), "tile %d uses %s" % (i, sorted(set(src) - WATER_IDX - set(TOP_SLOTS)))
                out[q] = (640 + G.SLOT_WATER + q) | (7 << 12)
                out[4 + q] = tile([0 if v in WATER_IDX else TOP_SLOTS[v] for v in src]) | (t & 0x0C00) | (TOP_ROW << 12)
            else:
                assert row == 5, "block %d quadrant %d is neither sea edge nor sand" % (EDGE[kind], q)
                out[q] = t
        a = (pattr_of(EDGE[kind]) & ~(7 << 29)) | (LAYER_COVERED << 29)
        return out, a

    hatch_px = [[HATCH_ROLES.get(ch, 0) for ch in row] for row in HATCH]
    def hatch():
        e = pentries(EDGE["C"]); out = list(e[:4]) + [0] * 4
        for q in range(4):
            out[4 + q] = tile([hatch_px[(q // 2) * 8 + k // 8][(q % 2) * 8 + k % 8] for k in range(64)]) | (HATCH_ROW << 12)
        a = (pattr_of(EDGE["C"]) & ~0x1FF & ~(7 << 29)) | MB_LADDER | (LAYER_COVERED << 29)
        return out, a

    order = sorted(IDS.items(), key=lambda kv: kv[1])
    for kind, mid in order:
        assert len(bmeta) // 16 == mid - 640
        e, a = hatch() if kind == "HATCH" else pale_edge(kind)
        bmeta += struct.pack("<8H", *e); battr += struct.pack("<I", a)

    # ---- Quicksilver's blocks at the dual ids: vanilla's own, blue
    while len(cmeta) // 16 < max(DUAL) - 640 + 1:
        cmeta += bytes(16); cattr += bytes(4)
    for mid, p in DUAL.items():
        k = mid - 640
        cmeta[k * 16:(k + 1) * 16] = prim[p * 16:(p + 1) * 16]
        cattr[k * 4:(k + 1) * 4] = pattr[p * 4:(p + 1) * 4]

    # ---- the maps
    def put(bd, x, y, m, hi):
        struct.pack_into("<H", bd, (y * W + x) * 2, (hi << 10) | m)
    for y in range(NORTH_TOP - 1, NORTH_H):                       # the old sand patch at rows 40..41 goes under water
        for x in range(W):
            if y == NORTH_TOP - 1 and struct.unpack_from("<H", nbd, (y * W + x) * 2)[0] & 0x3FF in range(908, 921):
                put(nbd, x, y, PALE_WATER, WATER_HI)
    rows = [(nbd, y) for y in range(NORTH_TOP, NORTH_H)] + [(sbd, y) for y in range(0, SOUTH_EDGE + 1)]
    for n, (bd, y) in enumerate(rows):
        first, last = n == 0, n == len(rows) - 1
        for x in range(W):
            side = "W" if x == 0 else "E" if x == W - 1 else ""
            kind = ("N" if first else "S" if last else "") + side
            kind = {"": "C", "N": "N", "S": "S"}.get(kind, kind)
            if (bd is nbd) and (x, y) == HATCH_AT:
                m = IDS["HATCH"]
            elif kind == "C":
                m = EDGE["C"]
            else:
                m = IDS[kind]
            put(bd, x, y, m, SAND_HI)
    for x in range(W):
        put(sbd, x, SOUTH_WATER, PALE_WATER, WATER_HI)

    total = num_tiles + len(new_tiles)
    print("  Blanche: %d tiles added (now %d/384), %d blocks (now %d/384); Quicksilver: %d blocks (was %d)" % (
        len(new_tiles), total, len(IDS), len(bmeta) // 16, len(cmeta) // 16, len(old_cmeta) // 16))
    assert total <= 384 and len(bmeta) // 16 <= 384 and len(cmeta) // 16 <= 384

    grown = Image.new("P", (128, ((total + 15) // 16) * 8)); grown.putpalette(bt.getpalette()); grown.paste(bt, (0, 0)); gp = grown.load()
    for n, key in enumerate(new_tiles):
        s = num_tiles + n
        for i, v in enumerate(key):
            gp[(s % 16) * 8 + i % 8, (s // 16) * 8 + i // 8] = v

    # ---- preview: the join as each map's player sees it, border included
    ct = Image.open(os.path.join(CD, "tiles.png"))
    def pals(sd, override=None):
        p = [read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)] + \
            [read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
        for row, cols in (override or {}).items():
            p[row] = cols
        return p
    def view(meta, tiles, pl, border):
        rows_from = [(nbd, y) for y in range(30, NORTH_H)] + [(sbd, y) for y in range(0, 12)]
        B = 3
        img = Image.new("RGB", ((W + 2 * B) * 16, len(rows_from) * 16)); o = img.load(); tp = tiles.load()
        for r, (bd, y) in enumerate(rows_from):
            for x in range(-B, W + B):
                m = struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF if 0 <= x < W else border
                src = prim if m < 640 else meta; k = m if m < 640 else m - 640
                if (k + 1) * 16 > len(src):
                    continue
                e = struct.unpack_from("<8H", src, k * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = e[layer * 4 + q]; i = t & 0x3FF
                        s_, j, hh = (ptp, i, pt.height) if i < 640 else (tp, i - 640, tiles.height)
                        for yy in range(8):
                            for xx in range(8):
                                sy = (j // 16) * 8 + (7 - yy if (t >> 11) & 1 else yy)
                                v = s_[(j % 16) * 8 + (7 - xx if (t >> 10) & 1 else xx), sy] if sy < hh else 0
                                if layer and v == 0:
                                    continue
                                o[(x + B) * 16 + (q % 2) * 8 + xx, r * 16 + (q // 2) * 8 + yy] = pl[(t >> 12) & 0xF][v]
        return img
    nborder = struct.unpack_from("<H", open(os.path.join(GBA, north["border_filepath"]), "rb").read(), 0)[0] & 0x3FF
    sborder = struct.unpack_from("<H", open(os.path.join(GBA, south["border_filepath"]), "rb").read(), 0)[0] & 0x3FF
    a = view(bytes(bmeta), grown, pals(BD, {TOP_ROW: row12}), nborder)
    b = view(bytes(cmeta), ct, pals(CD), sborder)
    sheet = Image.new("RGB", (a.width * 2 + 8, a.height), (255, 0, 255)); sheet.paste(a, (0, 0)); sheet.paste(b, (a.width + 8, 0))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (North rows 30..49 and South 0..11: as North's player sees them | as South's)" % PREVIEW)

    if WRITE:
        open(nb_path, "wb").write(nbd); open(sb_path, "wb").write(sbd)
        grown.save(os.path.join(BD, "tiles.png"))
        open(os.path.join(BD, "metatiles.bin"), "wb").write(bmeta); open(os.path.join(BD, "metatile_attributes.bin"), "wb").write(battr)
        open(os.path.join(CD, "metatiles.bin"), "wb").write(cmeta); open(os.path.join(CD, "metatile_attributes.bin"), "wb").write(cattr)
        write_pal(os.path.join(BD, "palettes/%02d.pal" % TOP_ROW), row12)
        open(RULES, "w").write(rules[:at] + str(total) + rules[at + len(str(num_tiles)):])
        print("  written: Route 21 North and South maps, Blanche's tiles (-num_tiles %d), blocks and row 12, Quicksilver's blocks" % total)


if __name__ == "__main__":
    main()

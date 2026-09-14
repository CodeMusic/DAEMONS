#!/usr/bin/env python3
"""Where a connection draws the neighbour wrong (T-73, engine.md trap 14).

    python3 tools/gbaseams.py              # every connection whose two maps load different secondary tilesets
    python3 tools/gbaseams.py Route1       # only connections touching maps whose name contains this

WHY. fieldmap.c's Fill*Connection copies MAP_OFFSET (7) rows or columns of the
neighbouring map into this map's grid, and every cell in that grid is drawn with
THIS map's tilesets. A primary block (id < 640) draws the same everywhere. A
secondary block draws whatever the id means in the tileset that happens to be
loaded -- so Route 1's birches, which are Blanche's blocks, draw as Callow's
buildings when you stand in Callow and look south.

A secondary block within 7 cells of an edge passes only if it draws the same in
both tilesets: the same eight entries, the same pixels for every secondary tile
it uses, and the same colours in every secondary palette row it uses. Vanilla
relies on exactly that in a few places (towns share blocks copied from one
another), so this compares what is drawn rather than refusing every id >= 640.

NO BLOCK MAY BE "DUAL". The first sandbar gave one id a different drawing in
each tileset, so each side would see its own; it glitched anyway, because the
engine does not redraw the screen when you cross -- the cells already on screen
keep the tile numbers and palette rows they were drawn with (trap 14). Only a
block that draws the same in both tilesets is safe.

AND THE BORDER. A map's border is drawn past its sides, and is on screen at a
crossing within seven cells of a side. A secondary border block beside a
connection to a different tileset is reported too; it is safe only if the map
keeps the player seven cells in from that side where they cross (gbasandbar.py).

Reported per side: the map whose cells are wrong, the neighbour whose tileset
draws them, and the rows or columns they sit in.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
BAND = 7
FILTER = sys.argv[1] if len(sys.argv) > 1 else ""
# secondary borders that are known to be kept off screen at the crossing, and by what
BORDER_KEPT_OFF = {"Route21_North": "gbasandbar.py: the arms keep the crossing seven cells in from both sides"}


def tdir(symbol):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    for d in os.listdir(os.path.join(GBA, "data/tilesets/secondary")):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(GBA, "data/tilesets/secondary", d)
    raise SystemExit("no directory for %s" % symbol)


class Tileset:
    def __init__(self, symbol):
        d = tdir(symbol)
        self.name = symbol
        self.metas = open(os.path.join(d, "metatiles.bin"), "rb").read()
        img = Image.open(os.path.join(d, "tiles.png"))
        self.w, self.h = img.size
        self.px = img.load()
        self.pal = {}
        for row in range(7, 13):
            p = os.path.join(d, "palettes/%02d.pal" % row)
            lines = open(p).read().replace("\r", "").split("\n")[3:19] if os.path.exists(p) else []
            self.pal[row] = [tuple(map(int, l.split())) for l in lines]

    def entries(self, m):
        k = m - 640
        if (k + 1) * 16 > len(self.metas):
            return None
        return struct.unpack_from("<8H", self.metas, k * 16)

    def tile(self, i):
        j = i - 640
        x0, y0 = (j % 16) * 8, (j // 16) * 8
        if y0 + 8 > self.h:
            return None
        return tuple(self.px[x0 + x, y0 + y] for y in range(8) for x in range(8))


def same_block(m, a, b):
    ea, eb = a.entries(m), b.entries(m)
    if ea is None or eb is None or ea != eb:
        return False
    for layer, t in enumerate(ea):
        i, row = t & 0x3FF, (t >> 12) & 0xF
        pix = None
        if i >= 640:
            ta, tb = a.tile(i), b.tile(i)
            if ta != tb:
                return False
            pix = ta
        if row >= 7:
            if pix is None:
                continue                                   # a primary tile in a secondary row: judged by its colours below
            used = set(pix) - ({0} if layer >= 4 else set())
            pa, pb = a.pal.get(row, []), b.pal.get(row, [])
            if any((pa[u] if u < len(pa) else None) != (pb[u] if u < len(pb) else None) for u in used):
                return False
    return True


def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    maps = {}
    for d in os.listdir(os.path.join(GBA, "data/maps")):
        p = os.path.join(GBA, "data/maps", d, "map.json")
        if os.path.exists(p):
            j = json.load(open(p))
            maps[j["id"]] = (d, j)
    tilesets = {}
    def ts(sym):
        if sym not in tilesets:
            tilesets[sym] = Tileset(sym)
        return tilesets[sym]
    grids = {}
    def grid(lay):
        if lay["name"] not in grids:
            bd = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read()
            grids[lay["name"]] = struct.unpack("<%dH" % (len(bd) // 2), bd)
        return grids[lay["name"]]

    total = 0
    for mid, (dname, j) in sorted(maps.items()):
        for c in j.get("connections") or []:
            if c["direction"] not in ("up", "down", "left", "right") or c["map"] not in maps:
                continue
            nname, nj = maps[c["map"]]
            if FILTER and FILTER not in dname and FILTER not in nname:
                continue
            la, lb = layouts[j["layout"]], layouts[nj["layout"]]
            if la["secondary_tileset"] == lb["secondary_tileset"]:
                continue
            # the neighbour's cells, drawn with THIS map's tileset
            A, B = ts(la["secondary_tileset"]), ts(lb["secondary_tileset"])
            g, W, H = grid(lb), lb["width"], lb["height"]
            off = c["offset"]
            if c["direction"] in ("up", "down"):
                ys = range(H - BAND, H) if c["direction"] == "up" else range(0, BAND)
                xs = [x for x in range(W) if 0 <= x + off < la["width"]]
                cells = [(x, y) for y in ys for x in xs]
            else:
                xs = range(W - BAND, W) if c["direction"] == "left" else range(0, BAND)
                ys = [y for y in range(H) if 0 <= y + off < la["height"]]
                cells = [(x, y) for x in xs for y in ys]
            bad = {}
            for x, y in cells:
                m = g[y * W + x] & 0x3FF
                if m >= 640 and not same_block(m, A, B):
                    bad.setdefault(m, []).append((x, y))
            if bad:
                n = sum(len(v) for v in bad.values()); total += n
                rows = sorted({y for v in bad.values() for _, y in v}); cols = sorted({x for v in bad.values() for x, _ in v})
                print("  %-28s seen from %-22s %4d cells, %2d blocks  rows %s  cols %s" % (
                    nname, dname, n, len(bad), "%d..%d" % (rows[0], rows[-1]), "%d..%d" % (cols[0], cols[-1])))
            border = open(os.path.join(GBA, lb["border_filepath"]), "rb").read()
            sec_border = sorted({struct.unpack_from("<H", border, i)[0] & 0x3FF for i in range(0, len(border), 2)} - set(range(640)))
            if sec_border and not all(same_block(m, A, B) for m in sec_border):
                note = BORDER_KEPT_OFF.get(nname)
                print("  %-28s border %s is secondary, on screen crossing from %s%s" % (nname, sec_border, dname, "  (kept off: %s)" % note if note else ""))
                if not note:
                    total += 1
    print("  %d cells draw wrong across a connection" % total)
    return total


if __name__ == "__main__":
    sys.exit(1 if main() else 0)

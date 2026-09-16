#!/usr/bin/env python3
"""A BENCHMARK's roof is not somewhere to stand (vision.md 9.23).

    python3 tools/gbaroofs.py            # report the roof cells that can be walked on
    python3 tools/gbaroofs.py --write    # block them in each town's map.bin

tools/gbacivic.py draws a BENCHMARK as a colonnade five rows tall -- from the door
row up to a flat roof four rows above it. Vanilla's gym drew that top row as an
overhang on ground the player could walk on, so in most towns the player walked
out onto our roof. Every roof cell the colonnade draws is blocked here. The row
behind it stays open in every town, so no path closes.

The buildings are found exactly as gbacivic.py finds them -- by the door warp,
the door block, and the building's own blocks either side -- reading through
tools/gbacivictown.json to the original blocks where a town redrew a cell.
"""
import importlib.util, json, os, struct, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbacivic", os.path.join(ROOT, "tools", "gbacivic.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
WRITE = "--write" in sys.argv
ROOF_DY = -4


def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(C.GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    prim = open(os.path.join(C.PD, "metatiles.bin"), "rb").read()
    btiles = {t & 0x3FF for m in C.GROUP["BENCHMARK"] for t in struct.unpack_from("<8H", prim, m * 16)
              if t & 0x3FF and (t >> 12) & 0xF in C.BUILDING_ROWS}
    secs = {}

    def is_building(tileset, m):
        if m >= 640 and tileset not in secs:
            secs[tileset] = open(os.path.join(C.tdir(tileset, "secondary"), "metatiles.bin"), "rb").read()
        buf, k = (prim, m) if m < 640 else (secs[tileset], m - 640)
        if (k + 1) * 16 > len(buf):
            return False
        return any(t & 0x3FF and (t >> 12) & 0xF in C.BUILDING_ROWS and (t & 0x3FF) in btiles
                   for t in struct.unpack_from("<8H", buf, k * 16))

    town_cells = json.load(open(C.TOWN_MANIFEST))["cells"] if os.path.exists(C.TOWN_MANIFEST) else {}
    total = given_back = 0
    for mp in sorted(os.listdir(os.path.join(C.GBA, "data/maps"))):
        p = os.path.join(C.GBA, "data/maps", mp, "map.json")
        if not os.path.exists(p):
            continue
        j = json.load(open(p)); l = layouts.get(j["layout"])
        if not l or l["primary_tileset"] != "gTileset_General":
            continue
        path = os.path.join(C.GBA, l["blockdata_filepath"])
        bd = bytearray(open(path, "rb").read()); W, H = l["width"], l["height"]; ts = l["secondary_tileset"]
        # What vanilla left WALKABLE at that row is ground under an overhang, not roof surface, and
        # blocking it took a walkway away in four towns (T-121). Read upstream and never block there.
        up = subprocess.run(["git", "-C", C.GBA, "show", "upstream/master:" + l["blockdata_filepath"]],
                            capture_output=True).stdout
        restored = []
        town = town_cells.get(mp, {})
        cell = lambda x, y: town.get("%d,%d" % (x, y), struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF)
        has = lambda x, y: 0 <= x < W and 0 <= y < H and is_building(ts, cell(x, y)) and cell(x, y) not in C.SIGN_BLOCKS
        blocked = []
        for w in j["warp_events"]:
            x, y = w["x"], w["y"]
            if not (w["dest_map"].endswith("_GYM") and 0 <= x < W and 0 <= y < H and cell(x, y) == C.KINDS["_GYM"][1]):
                continue
            left = 0
            while has(x + left - 1, y - 1) or has(x + left - 1, y - 2):
                left -= 1
            right = 0
            while has(x + right + 1, y - 1) or has(x + right + 1, y - 2):
                right += 1
            Y = y + ROOF_DY
            for dx in range(left, right + 1):
                X = x + dx
                if not (0 <= X < W and 0 <= Y < H) or cell(X, Y) in C.SIGN_BLOCKS:
                    continue
                raw = struct.unpack_from("<H", bd, (Y * W + X) * 2)[0]
                off = (Y * W + X) * 2
                if up and len(up) >= off + 2 and (int.from_bytes(up[off:off + 2], "little") >> 10) & 3 == 0:
                    if (raw >> 10) & 3:                        # we blocked ground vanilla let you stand on
                        struct.pack_into("<H", bd, off, raw & 0x3FF)
                        restored.append((X, Y))
                    continue
                if (raw >> 10) & 3 == 0:                       # collision 0: walkable
                    struct.pack_into("<H", bd, (Y * W + X) * 2, (raw & 0x3FF) | (1 << 10))
                    blocked.append((X, Y))
            print("  %-16s BENCHMARK door (%d,%d), columns %+d..%+d: roof cells blocked %s" % (mp, x, y, left, right, blocked or "none"))
        if restored:
            print("  %-16s gave back %d cell(s) vanilla left walkable: %s" % (mp, len(restored), restored))
        if blocked or restored:
            total += len(blocked); given_back += len(restored)
            if WRITE:
                open(path, "wb").write(bd)
    print("  %d roof cells %s; %d walkable cells given back (T-121)"
          % (total, "blocked and written" if WRITE else "to block (run with --write)", given_back))


if __name__ == "__main__":
    main()

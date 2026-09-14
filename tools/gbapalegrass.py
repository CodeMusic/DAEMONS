#!/usr/bin/env python3
"""Blanche's pale tall grass, re-derived from the world's new blades (T-61, vision.md 9.22).

    python3 tools/gbapalegrass.py            # preview to /tmp/pale_grass.png (now | after)
    python3 tools/gbapalegrass.py --write    # the four pale tall grass tiles in gTileset_PalletTown

gbaroutes.py drew the pale tall grass on Route 1 and Route 21 North from
vanilla's clump, before T-61 replaced it everywhere else with a field of narrow
blades. So the pale stretch still had the old shape.

The pale tall grass is two blocks (Route 1's and Route 21 North's), both drawing
the same four tiles and nothing else. They are redrawn in place from gbagrass.py's
clump, each of its row-0 jobs given Blanche's colour for that job:

    the grass under it   GRASS        the darker mass   TUFT       its shadow   DARK
    a blade's lit edge   SPECK        a blade           TIP        its far side GRASS
    the roots            DARK

so the blades stand lighter than the mass they grow from, as the coloured ones
do. gbagrassfx.py gives the walking effect the same colour per job.
"""
import importlib.util, json, os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
G = load("gbaground")
W = load("gbagrass")

GBA = os.path.join(ROOT, "engineGba")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
PREVIEW = "/tmp/pale_grass.png"
WRITE = "--write" in sys.argv
TALL_GRASS_BEHAVIOUR = 0x02
JOB = {W.BASE: G.GRASS, W.GLIGHT: G.TIP, W.TUFT: G.TUFT, W.TDARK: G.DARK,
       W.LIT: G.SPECK, W.LEAF: G.TIP, W.DARK: G.GRASS, W.DEEP: G.DARK}


def main():
    metas = open(os.path.join(SD, "metatiles.bin"), "rb").read()
    attrs = open(os.path.join(SD, "metatile_attributes.bin"), "rb").read()
    n = len(metas) // 16
    grass = [640 + k for k in range(n) if struct.unpack_from("<I", attrs, k * 4)[0] & 0x1FF == TALL_GRASS_BEHAVIOUR]
    assert grass, "no tall grass blocks in Blanche's tileset"
    quads = {}
    for m in grass:
        e = struct.unpack_from("<8H", metas, (m - 640) * 16)
        assert not any(t & 0x3FF for t in e[4:]), "block %d has a top layer" % m
        for q, t in enumerate(e[:4]):
            assert (t >> 12) & 0xF == 7 and not (t >> 10) & 3, "block %d quadrant %d is not a plain row-7 tile" % (m, q)
            quads.setdefault(t & 0x3FF, set()).add(q)
    users = {}
    for k in range(n):
        for t in struct.unpack_from("<8H", metas, k * 16):
            if (t & 0x3FF) in quads:
                users.setdefault(t & 0x3FF, set()).add(640 + k)
    for tile, qs in quads.items():
        assert len(qs) == 1, "tile %d is drawn in more than one quadrant" % tile
        assert users[tile] <= set(grass), "tile %d is also drawn by %s" % (tile, sorted(users[tile] - set(grass)))
    print("  tall grass blocks %s, tiles %s" % (grass, sorted(quads)))

    cl = W.clump()
    img = Image.open(os.path.join(SD, "tiles.png")); new = img.copy(); npx = new.load()
    for tile, qs in quads.items():
        q = next(iter(qs)); s = tile - 640
        for y in range(8):
            for x in range(8):
                npx[(s % 16) * 8 + x, (s // 16) * 8 + y] = JOB[cl[(q // 2) * 8 + y][(q % 2) * 8 + x]]

    pal = G.ROW7
    sheet = Image.new("RGB", (16 * 4 * 2 + 8, 16 * 3), (30, 30, 30))
    for side, src in enumerate((img, new)):
        sp = src.load()
        for cy in range(3):
            for cx in range(4):
                for tile, qs in quads.items():
                    q = next(iter(qs)); s = tile - 640
                    for y in range(8):
                        for x in range(8):
                            sheet.putpixel((side * (64 + 8) + cx * 16 + (q % 2) * 8 + x, cy * 16 + (q // 2) * 8 + y),
                                           pal[sp[(s % 16) * 8 + x, (s // 16) * 8 + y]])
    sheet.resize((sheet.width * 6, sheet.height * 6), Image.NEAREST).save(PREVIEW)
    print("  preview %s (now | after, a 4x3 field)" % PREVIEW)
    if WRITE:
        new.save(os.path.join(SD, "tiles.png"))
        print("  written: tiles.png, %d tiles" % len(quads))


main()

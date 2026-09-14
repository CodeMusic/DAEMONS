#!/usr/bin/env python3
"""The sandbar across Route 21, where the pale sea meets the blue (T-73, T-74, T-83; vision.md 9.22).

    python3 tools/gbasandbar.py            # preview to /tmp/sandbar.png (seen from North | seen from South)
    python3 tools/gbasandbar.py --write    # both routes' maps, and one primary block

WHAT IT IS. A bar of gold sand three rows deep across the whole sea at North rows
41..43, the hatch on it at (11,42); and below it two arms of sand down both sides
to the join (x 0..6 and 17..23, rows 44..49), so the only way on to South is by
surfing the channel between them, x 7..16.

WHY IT IS SHAPED LIKE THAT -- ALL OF IT IS THE ENGINE, NOT TASTE.

  1. A connection draws seven rows of the neighbour with THIS map's tileset
     (engine.md trap 14). So North rows 43..49 and South rows 0..6 hold only
     primary blocks, which draw the same whichever tileset is loaded.

  2. AND THE SCREEN IS NOT REDRAWN WHEN YOU CROSS. LoadMapFromCameraTransition
     loads the new map's tiles and palettes into VRAM but leaves the tilemap as
     it was: every cell already on screen keeps the tile number and palette row
     it was drawn with, now pointing at the other tileset's tiles and colours.
     The first sandbar (T-74) gave its edges the same ids in both tilesets with a
     different drawing in each; the drawings were right and the screen still
     showed Blanche's, in Quicksilver's palette row 7 -- pure blue and black.
     So whatever is on screen at the moment of crossing must be primary too.

  3. THE BORDER COUNTS. Past a map's sides the engine draws its border block, and
     Route 21 North's border is Blanche's pale water. If it is on screen when you
     cross, it garbles the same way. You see seven cells either side of you, so
     the crossing has to happen at least seven cells in from both edges: that is
     the channel, and the arms are what keep you in it. The arms' last row is
     solid, so nobody can surf off them across the join at the sides.

The bar's top edge meets pale water, so it is Blanche's two-layer edge from the
first sandbar (block 953, pale water below and vanilla's sand edge on top). Its
body, the arms and every edge that meets blue water are primary. The one inner
corner vanilla never drew -- sand missing only its south-east -- is a new
primary block made from vanilla's own corner tile, unflipped.
"""
import json, os, struct, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
BD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
CD = os.path.join(GBA, "data/tilesets/secondary/cinnabar_island")
PREVIEW = "/tmp/sandbar.png"
WRITE = "--write" in sys.argv
BEFORE = "fb6f7ec66^"                 # the engine before the first sandbar: the sea rows and Quicksilver's tileset

W = 24
BAR = (41, 43)                        # North rows
ARMS = (range(0, 7), range(17, 24))   # columns, North rows 44..49
CHANNEL = range(7, 17)
HATCH_AT = (11, 42)
SAND_HI, WATER_HI, SOLID = 12, 4, 1   # collision/elevation bits: sand at 3, water at 1; bit 0 blocks

PALE_TOP_EDGE, HATCH = 953, 955       # Blanche's, from the first sandbar
C, S_EDGE, W_EDGE, E_EDGE, SW, SE, I_SW = 277, 285, 276, 278, 284, 286, 301
I_SE = 552                            # a blank primary block, drawn here
BLUE = 299


def git_bytes(path):
    return subprocess.run(["git", "-C", GBA, "show", "%s:%s" % (BEFORE, path)], capture_output=True, check=True).stdout


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    north, south = layouts["Route21_North_Layout"], layouts["Route21_South_Layout"]
    nb_path, sb_path = os.path.join(GBA, north["blockdata_filepath"]), os.path.join(GBA, south["blockdata_filepath"])
    old_n, old_s = open(nb_path, "rb").read(), open(sb_path, "rb").read()
    nbd = bytearray(old_n); sbd = bytearray(git_bytes(south["blockdata_filepath"]))
    before_n = git_bytes(north["blockdata_filepath"])
    get = lambda bd, x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
    put = lambda bd, x, y, m, hi: struct.pack_into("<H", bd, (y * W + x) * 2, (hi << 10) | m)
    if get(nbd, 7, 44) & 0x3FF == BLUE and get(nbd, 0, 44) & 0x3FF == C:
        print("  the sandbar is already this shape"); return

    prim = bytearray(open(os.path.join(PD, "metatiles.bin"), "rb").read())
    pattr = bytearray(open(os.path.join(PD, "metatile_attributes.bin"), "rb").read())
    bmeta = open(os.path.join(BD, "metatiles.bin"), "rb").read()
    assert len(bmeta) // 16 > HATCH - 640, "Blanche's tileset lacks the first sandbar's blocks"

    # ---- the inner corner vanilla never drew: sand with only its south-east missing
    e = list(struct.unpack_from("<8H", prim, I_SW * 16))
    corner = e[2]                                          # 429, row 4, h-flipped: water in the bottom-left
    new = [e[0], e[1], e[3], (corner & ~0x0C00), 0, 0, 0, 0]  # unflipped, it sits bottom-right
    if any(struct.unpack_from("<8H", prim, I_SE * 16)):
        assert list(struct.unpack_from("<8H", prim, I_SE * 16)) == new, "primary block %d is not blank" % I_SE
    struct.pack_into("<8H", prim, I_SE * 16, *new)
    pattr[I_SE * 4:(I_SE + 1) * 4] = pattr[I_SW * 4:(I_SW + 1) * 4]

    # ---- North: back to the sea as it was, then the bar, the arms and the channel
    for y in range(BAR[0] - 1, 50):
        for x in range(W):
            nbd[(y * W + x) * 2:(y * W + x) * 2 + 2] = before_n[(y * W + x) * 2:(y * W + x) * 2 + 2]
    for x in range(15, 20):                                # the pale sand patch that stood here goes under water
        if get(nbd, x, BAR[0] - 1) & 0x3FF in range(908, 921):
            put(nbd, x, BAR[0] - 1, 880, WATER_HI)
    for x in range(W):
        put(nbd, x, 41, PALE_TOP_EDGE, SAND_HI)
        put(nbd, x, 42, HATCH if (x, 42) == HATCH_AT else C, SAND_HI)
        arm = x in ARMS[0] or x in ARMS[1]
        kind = C if arm else S_EDGE
        if x == ARMS[0][-1]:
            kind = I_SE
        if x == ARMS[1][0]:
            kind = I_SW
        put(nbd, x, 43, kind, SAND_HI)
    for y in range(44, 50):
        last = y == 49
        for x in range(W):
            if x in CHANNEL:
                put(nbd, x, y, BLUE, WATER_HI); continue
            if x == ARMS[0][-1]:
                kind = SE if last else E_EDGE
            elif x == ARMS[1][0]:
                kind = SW if last else W_EDGE
            else:
                kind = S_EDGE if last else C
            put(nbd, x, y, kind, SOLID | SAND_HI if last else SAND_HI)

    # ---- the report: nothing but primary blocks where a crossing can see
    bad = [(x, y) for y in range(43, 50) for x in range(W) if get(nbd, x, y) & 0x3FF >= 640] + \
          [(x, "S%d" % y) for y in range(0, 7) for x in range(W) if get(sbd, x, y) & 0x3FF >= 640]
    assert not bad, "secondary blocks where a crossing can see: %s" % bad[:8]
    print("  bar at North rows 41..43, arms x 0..6 and 17..23 to row 49, channel x 7..16; South rows 0..6 as they were")

    # ---- preview, border included, from each side
    pt = Image.open(os.path.join(PD, "tiles.png")); ptp = pt.load()
    def view(bd_rows, sd, border, meta_prim):
        smeta = open(os.path.join(sd, "metatiles.bin"), "rb").read()
        st = Image.open(os.path.join(sd, "tiles.png")); stp = st.load()
        pals = [read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)] + [read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
        B = 7
        img = Image.new("RGB", ((W + 2 * B) * 16, len(bd_rows) * 16)); o = img.load()
        for r, (bd, y) in enumerate(bd_rows):
            for x in range(-B, W + B):
                m = get(bd, x, y) & 0x3FF if 0 <= x < W else border
                src = meta_prim if m < 640 else smeta; k = m if m < 640 else m - 640
                if (k + 1) * 16 > len(src):
                    continue
                ee = struct.unpack_from("<8H", src, k * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = ee[layer * 4 + q]; i = t & 0x3FF
                        s_, j, hh = (ptp, i, pt.height) if i < 640 else (stp, i - 640, st.height)
                        for yy in range(8):
                            for xx in range(8):
                                sy = (j // 16) * 8 + (7 - yy if (t >> 11) & 1 else yy)
                                v = s_[(j % 16) * 8 + (7 - xx if (t >> 10) & 1 else xx), sy] if sy < hh else 0
                                if layer and v == 0:
                                    continue
                                o[(x + B) * 16 + (q % 2) * 8 + xx, r * 16 + (q // 2) * 8 + yy] = pals[(t >> 12) & 0xF][v]
        return img
    nborder = struct.unpack_from("<H", open(os.path.join(GBA, north["border_filepath"]), "rb").read(), 0)[0] & 0x3FF
    sborder = struct.unpack_from("<H", open(os.path.join(GBA, south["border_filepath"]), "rb").read(), 0)[0] & 0x3FF
    from_north = view([(nbd, y) for y in range(34, 50)] + [(sbd, y) for y in range(0, 7)], BD, nborder, bytes(prim))
    from_south = view([(nbd, y) for y in range(43, 50)] + [(sbd, y) for y in range(0, 12)], CD, sborder, bytes(prim))
    sheet = Image.new("RGB", (from_north.width * 2 + 8, max(from_north.height, from_south.height)), (255, 0, 255))
    sheet.paste(from_north, (0, 0)); sheet.paste(from_south, (from_north.width + 8, 0))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (North rows 34..49 + South 0..6 with North's tileset and border | North 43..49 + South 0..11 with South's)" % PREVIEW)

    if WRITE:
        open(nb_path, "wb").write(nbd); open(sb_path, "wb").write(sbd)
        open(os.path.join(PD, "metatiles.bin"), "wb").write(prim); open(os.path.join(PD, "metatile_attributes.bin"), "wb").write(pattr)
        for f in ("metatiles.bin", "metatile_attributes.bin"):       # Quicksilver's tileset loses the dual ids that never worked
            open(os.path.join(CD, f), "wb").write(git_bytes("data/tilesets/secondary/cinnabar_island/" + f))
        print("  written: Route 21 North and South, primary block %d, Quicksilver's tileset as it was" % I_SE)


if __name__ == "__main__":
    main()

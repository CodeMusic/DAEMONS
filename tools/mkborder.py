#!/usr/bin/env python3
"""
Turn an SGB border design of any size into the two files pokered wants.

    python3 tools/mkborder.py gfx/borders/content_border.png content

Emits into engine/gfx/sgb/:
    <name>_border.png       128x48, 2bpp — the bank of <=96 unique tiles
    <name>_border.tilemap   32x28 tile indices + attribute bytes

The SGB border is NOT an image. It is a bank of at most 96 unique 8x8 tiles
plus a tilemap arranging them, coloured at runtime by SGB palettes. The centre
160x144 window is forced blank — that is where the game screen appears.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import OrderedDict
from gbimg import read_png, resample, quantise, write_png

W, H = 256, 224
WIN_X, WIN_Y, WIN_W, WIN_H = 48, 40, 160, 144
MAX_TILES = 96

def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    src, name = sys.argv[1], sys.argv[2]
    sw, sh, lum = read_png(src)
    print("source %dx%d -> %dx%d" % (sw, sh, W, H))
    g = quantise(resample(sw, sh, lum, W, H))

    for y in range(WIN_Y, WIN_Y+WIN_H):
        for x in range(WIN_X, WIN_X+WIN_W): g[y][x] = 3

    tiles, tilemap = OrderedDict(), []
    for ty in range(H//8):
        for tx in range(W//8):
            key = tuple(g[ty*8+py][tx*8+px] for py in range(8) for px in range(8))
            if key not in tiles: tiles[key] = len(tiles)
            tilemap.append(tiles[key])

    n = len(tiles)
    print("unique tiles: %d  (budget %d)" % (n, MAX_TILES))
    if n > MAX_TILES:
        print("\nOVER BUDGET by %d tiles. To reduce:" % (n - MAX_TILES))
        print("  - repeat ONE motif across each edge instead of varying it")
        print("  - make all four corners identical (mirrored)")
        print("  - remove scattered lighter/darker accents; they cost a tile each")
        print("  - align every shape to the 8x8 grid so tiles repeat exactly")
        sys.exit(1)

    out = "engine/gfx/sgb"
    bank = [[3]*128 for _ in range(48)]
    for key, idx in tiles.items():
        bx, by = (idx % 16)*8, (idx//16)*8
        for py in range(8):
            for px in range(8): bank[by+py][bx+px] = key[py*8+px]
    write_png(os.path.join(out, "%s_border.png" % name), bank, 2)

    tm = bytearray()
    for idx in tilemap: tm += bytes([idx, 0x00])
    open(os.path.join(out, "%s_border.tilemap" % name), 'wb').write(bytes(tm))
    print("wrote %s/%s_border.png and .tilemap" % (out, name))

if __name__ == "__main__": main()

#!/usr/bin/env python3
"""
Generate an SGB border procedurally, inside the 96-tile budget.

    python3 tools/genborder.py content
    python3 tools/genborder.py context

A halftone frame is geometry, not illustration. Building it from a repeating
cell makes the tile budget trivial to hit and lands every dot on the grid.
Gemini's illustrated versions came in at 496 and 523 unique tiles.

  content — one dot grid. The thing itself, repeating, self-identical.
  context — two grids at an offset. Nothing new is drawn; the pattern is the
            relationship between them. True moire never repeats and so cannot
            be tiled at all; this is a repeating unit that READS as moire.

Format notes, all verified against vanilla gfx/sgb/red_border.* :
  * tile bank is a 128x48 2bpp greyscale PNG = 96 tiles, no PLTE
  * rgbgfx INVERTS greyscale: PNG level 3 -> colour index 0. So in the PNG,
    higher value = lighter on screen. Level 3 is the light ground.
  * tilemap is 896 entries of (tile, attribute). Attribute bit layout is
    SNES: (attr >> 2) & 7 = palette. Vanilla uses palettes 4/5/6 = PAL_SGB1/2/3
    and 0x40 for X-flip. We use one palette, 4, so every border entry is $10.
  * the centre 160x144 is covered by the Game Boy screen. Vanilla fills it
    with tile $00 attribute $00; tile 0 is therefore reserved and flat.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import OrderedDict
from gbimg import write_png

W, H = 256, 224
WIN_X, WIN_Y, WIN_W, WIN_H = 48, 40, 160, 144
MAX_TILES = 96
GROUND, ATTR = 3, 0x10          # light ground; palette 4 = PAL_SGB1

def disc(cx, cy, x, y, r):
    dx, dy = x - cx, y - cy
    return dx*dx + dy*dy <= r*r

def build(mode):
    g = [[GROUND]*W for _ in range(H)]
    tw, th = W//8, H//8
    wx0, wy0, wx1, wy1 = WIN_X//8, WIN_Y//8, (WIN_X+WIN_W)//8, (WIN_Y+WIN_H)//8
    for ty in range(th):
        for tx in range(tw):
            if wx0 <= tx < wx1 and wy0 <= ty < wy1:
                continue                                   # under the screen
            # ring: 0 = touching the window, larger = further out
            d = 0
            if tx < wx0:  d = max(d, wx0-1-tx)
            if tx >= wx1: d = max(d, tx-wx1)
            if ty < wy0:  d = max(d, wy0-1-ty)
            if ty >= wy1: d = max(d, ty-wy1)
            r, ink = [(1,0), (2,0), (3,1), (3,0)][min(d, 3)]
            for py in range(8):
                for px in range(8):
                    v = GROUND
                    if disc(3.5, 3.5, px, py, r):
                        v = ink
                    if mode == 'context':
                        # the second grid, offset half a cell: interference
                        if disc(-0.5, -0.5, px, py, r) or disc(7.5, 7.5, px, py, r):
                            v = min(v, 2)
                    g[ty*8+py][tx*8+px] = v
            # a rule against the screen, so the window reads as a frame
            if d == 0:
                if tx == wx0-1: 
                    for py in range(8): g[ty*8+py][tx*8+7] = 0
                if tx == wx1:
                    for py in range(8): g[ty*8+py][tx*8]   = 0
                if ty == wy0-1:
                    for px in range(8): g[ty*8+7][tx*8+px] = 0
                if ty == wy1:
                    for px in range(8): g[ty*8][tx*8+px]   = 0
    return g

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('content', 'context'):
        sys.exit(__doc__)
    name = sys.argv[1]
    g = build(name)
    tw, th = W//8, H//8
    wx0, wy0, wx1, wy1 = WIN_X//8, WIN_Y//8, (WIN_X+WIN_W)//8, (WIN_Y+WIN_H)//8

    blank = tuple([GROUND]*64)
    tiles = OrderedDict([(blank, 0)])          # tile 0 reserved, flat
    tilemap = []
    for ty in range(th):
        for tx in range(tw):
            if wx0 <= tx < wx1 and wy0 <= ty < wy1:
                tilemap.append((0, 0x00))      # covered by the screen
                continue
            key = tuple(g[ty*8+py][tx*8+px] for py in range(8) for px in range(8))
            if key not in tiles:
                tiles[key] = len(tiles)
            tilemap.append((tiles[key], ATTR))

    n = len(tiles)
    print("%s: %d unique tiles (budget %d)" % (name, n, MAX_TILES))
    if n > MAX_TILES:
        sys.exit("over budget")
    assert len(tilemap) == 896, len(tilemap)

    out = "engine/gfx/sgb"
    bank = [[GROUND]*128 for _ in range(48)]
    for key, idx in tiles.items():
        bx, by = (idx % 16)*8, (idx//16)*8
        for py in range(8):
            for px in range(8):
                bank[by+py][bx+px] = key[py*8+px]
    write_png(os.path.join(out, "%s_border.png" % name), bank, 2)
    tm = bytearray()
    for idx, attr in tilemap:
        tm += bytes([idx, attr])
    open(os.path.join(out, "%s_border.tilemap" % name), 'wb').write(bytes(tm))
    print("  wrote %s_border.png (128x48) and .tilemap (896 entries)" % name)
    for y in range(0, H, 4):
        print("  " + ''.join(' .:#'[3-g[y][x]] for x in range(0, W, 2)))

if __name__ == "__main__":
    main()

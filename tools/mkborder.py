#!/usr/bin/env python3
"""
Turn a 256x224 SGB border design into the two files pokered wants.

    python3 tools/mkborder.py design.png red

Emits, into engine/gfx/sgb/:
    <name>_border.png       128x48, 2bpp greyscale — the bank of <=96 unique tiles
    <name>_border.tilemap   32x28 tile indices + attribute bytes

The Super Game Boy border is NOT an image. It is a bank of at most 96 unique
8x8 tiles plus a tilemap arranging them, coloured at runtime by SGB palettes.
This script does the deduplication and tells you if the design blows the budget.

The centre 160x144 window must be blank — that is where the game screen shows.
"""
import sys, zlib, struct, os
from collections import OrderedDict

W, H = 256, 224
WIN_X, WIN_Y, WIN_W, WIN_H = 48, 40, 160, 144      # the game screen window
MAX_TILES = 96

def read_png(path):
    d = open(path, 'rb').read()
    pos, idat, plte = 8, b'', None
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos+4])[0]
        typ, data = d[pos+4:pos+8], d[pos+8:pos+8+ln]
        if typ == b'IHDR': w, h, bd, ct = struct.unpack('>IIBB', data[:10])
        elif typ == b'IDAT': idat += data
        elif typ == b'PLTE': plte = data
        pos += 12 + ln
    if ct not in (0, 2, 3, 6):
        sys.exit("unsupported PNG colour type %d" % ct)
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ct] * (bd // 8 or 1)
    stride = (w * {0: bd, 2: bd*3, 3: bd, 4: bd*2, 6: bd*4}[ct] + 7) // 8
    raw = zlib.decompress(idat); rows = []; prev = bytearray(stride); i = 0
    for _ in range(h):
        f = raw[i]; i += 1; line = bytearray(raw[i:i+stride]); i += stride
        for x in range(stride):
            a = line[x-bpp] if x >= bpp else 0
            b = prev[x]; c = prev[x-bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x]+a) & 255
            elif f == 2: line[x] = (line[x]+b) & 255
            elif f == 3: line[x] = (line[x]+((a+b) >> 1)) & 255
            elif f == 4:
                p = a+b-c; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line)); prev = line
    def lum(x, y):
        if ct == 2:  r, g, b = rows[y][x*3:x*3+3]; return (r*299+g*587+b*114)//1000
        if ct == 6:  r, g, b = rows[y][x*4:x*4+3]; return (r*299+g*587+b*114)//1000
        if ct == 3:
            idx = rows[y][x]; r, g, b = plte[idx*3:idx*3+3]
            return (r*299+g*587+b*114)//1000
        if bd == 8:  return rows[y][x]
        v = (rows[y][x*bd//8] >> (8-bd-(x*bd) % 8)) & ((1 << bd)-1)
        return v * 255 // ((1 << bd)-1)
    return w, h, lum

def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    src, name = sys.argv[1], sys.argv[2]
    w, h, lum = read_png(src)
    if (w, h) != (W, H): sys.exit("design must be exactly %dx%d, got %dx%d" % (W, H, w, h))

    # quantise luminance to the 4 Game Boy values (3 = lightest)
    def q(x, y): return 3 - min(3, lum(x, y) * 4 // 256)

    # the window must be blank; force it so a stray pixel cannot cost a tile
    def val(x, y):
        if WIN_X <= x < WIN_X+WIN_W and WIN_Y <= y < WIN_Y+WIN_H: return 3
        return q(x, y)

    tiles, tilemap = OrderedDict(), []
    for ty in range(H//8):
        for tx in range(W//8):
            key = tuple(val(tx*8+px, ty*8+py) for py in range(8) for px in range(8))
            if key not in tiles: tiles[key] = len(tiles)
            tilemap.append(tiles[key])

    print("unique tiles: %d  (budget %d)" % (len(tiles), MAX_TILES))
    if len(tiles) > MAX_TILES:
        print("\nOVER BUDGET by %d. Make the pattern repeat more:" % (len(tiles)-MAX_TILES))
        print("  - use one motif tiling across each edge, not a unique illustration")
        print("  - keep corners simple and mirror them")
        print("  - align everything to the 8x8 grid so tiles repeat exactly")
        sys.exit(1)

    out = "engine/gfx/sgb"
    bank_w, bank_h = 128, 48                       # 16x6 tiles = 96
    grid = [[3]*bank_w for _ in range(bank_h)]
    for key, idx in tiles.items():
        bx, by = (idx % 16)*8, (idx//16)*8
        for py in range(8):
            for px in range(8):
                grid[by+py][bx+px] = key[py*8+px]
    stride = (bank_w*2+7)//8; raw = b''
    for row in grid:
        line = bytearray(stride)
        for x, v in enumerate(row): line[x//4] |= (v << (6-2*(x % 4)))
        raw += b'\x00'+bytes(line)
    def chunk(t, d):
        c = t+d; return struct.pack('>I', len(d))+c+struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', bank_w, bank_h, 2, 0, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
    open(os.path.join(out, "%s_border.png" % name), 'wb').write(png)

    tm = bytearray()
    for idx in tilemap: tm += bytes([idx, 0x00])   # tile, attribute (palette 0)
    open(os.path.join(out, "%s_border.tilemap" % name), 'wb').write(bytes(tm))
    print("wrote %s/%s_border.png and .tilemap" % (out, name))

if __name__ == "__main__": main()

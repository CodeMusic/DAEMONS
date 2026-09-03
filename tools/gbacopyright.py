#!/usr/bin/env python3
"""Redraw the GBA copyright screen.

    python3 tools/gbacopyright.py [--write]

The Game Boy version of this screen was a raw tile bank walked by PlaceString,
and the whole design came out of a 31-tile budget. The GBA one is a tile bank
AND A TILEMAP -- graphics/intro/copyright.png is a deduplicated atlas, and
copyright.bin is a 32x32 map of indices into it -- which is more work and far
more freedom: the text can sit anywhere on the 30x20 screen instead of on three
consecutive rows.

Both decompress to the start of their VRAM blocks, so tile indices are 0-based
into our own atlas and nothing has to be offset. Tile 0 must be blank, because
everything the map does not name is 0.

The typeface is the same one the Game Boy screen uses -- vanilla's copyright
font, lifted pixel-for-pixel, plus the glyphs it never had. Reused rather than
redrawn so the two editions of this screen are recognisably the same object.

    (c)'11-'26  CODEMUSIC
    (c)'11-'26  SeeingSharp
    (c)'11-'26  Psychology/Code
"""
import importlib.util, os, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

spec = importlib.util.spec_from_file_location("gc", os.path.join(HERE, "gencopyright.py"))
gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gc)

SCREEN_W, SCREEN_H = 30, 20          # tiles
INK, SHADOW = 1, 2                   # palette indices; 0 is the background

LINES = ["@'11-'26  CODEMUSIC",
         "@'11-'26  SeeingSharp",
         "@'11-'26  Psychology/Code"]

SPACE = 4                            # the font has no space glyph

def glyph(ch):
    return None if ch == " " else gc.F['(c)' if ch == '@' else ch]

def draw(text):
    """One line of glyphs on a transparent strip, 1px between them."""
    w = sum(SPACE if glyph(c) is None else len(glyph(c)[0]) + 1 for c in text)
    g = [[0] * (w + 2) for _ in range(8)]
    x = 0
    for ch in text:
        rows = glyph(ch)
        if rows is None:
            x += SPACE; continue
        for r, row in enumerate(rows):
            for i, px in enumerate(row):
                if px == '#':
                    g[r][x + i] = INK
        x += len(rows[0]) + 1
    return g, w

# --- compose the screen ----------------------------------------------------
canvas = [[0] * (SCREEN_W * 8) for _ in range(SCREEN_H * 8)]
strips = [draw(l) for l in LINES]
top = (SCREEN_H * 8 - len(LINES) * 12) // 2
for n, (g, w) in enumerate(strips):
    ox = (SCREEN_W * 8 - w) // 2
    oy = top + n * 12
    for y in range(8):
        for x in range(w):
            if g[y][x]:
                canvas[oy + y][ox + x] = g[y][x]
                # a one-pixel drop shadow, which is what stops five-pixel
                # glyphs vanishing on a GBA screen
                if canvas[oy + y + 1][ox + x + 1] == 0:
                    canvas[oy + y + 1][ox + x + 1] = SHADOW

# --- dedup into an atlas ---------------------------------------------------
bank, index, tmap = [], {}, []
for ty in range(SCREEN_H):
    for tx in range(SCREEN_W):
        t = tuple(tuple(canvas[ty*8 + r][tx*8 + c] for c in range(8)) for r in range(8))
        if t not in index:
            index[t] = len(bank); bank.append(t)
        tmap.append((ty, tx, index[t]))
blank = tuple(tuple(0 for _ in range(8)) for _ in range(8))
assert bank[0] == blank, "tile 0 must be blank -- the map's empty cells are 0"
print("  %d unique tiles from %d cells" % (len(bank), SCREEN_W * SCREEN_H))

# --- write -----------------------------------------------------------------
COLS = 8
rows = (len(bank) + COLS - 1) // COLS
aw, ah = COLS * 8, rows * 8
atlas = [[0] * aw for _ in range(ah)]
for i, t in enumerate(bank):
    bx, by = (i % COLS) * 8, (i // COLS) * 8
    for r in range(8):
        for c in range(8):
            atlas[by + r][bx + c] = t[r][c]

pal = [(0, 0, 0), (248, 248, 248), (96, 96, 112)] + [(0, 0, 0)] * 13

def write_png4(path, g, palette, w, h):
    plte = b"".join(bytes(c) for c in palette)
    raw = b""
    for row in g:
        packed = bytearray()
        for i in range(0, len(row), 2):
            packed.append((row[i] << 4) | row[i + 1])
        raw += b"\x00" + bytes(packed)
    def ch(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c))
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n"
        + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 4, 3, 0, 0, 0))
        + ch(b"PLTE", plte) + ch(b"IDAT", zlib.compress(raw)) + ch(b"IEND", b""))

# 32x32 entries, 2 bytes each: tile index in the low 10 bits, palette 0.
binmap = bytearray(32 * 32 * 2)
for ty, tx, i in tmap:
    o = (ty * 32 + tx) * 2
    binmap[o] = i & 0xFF
    binmap[o + 1] = (i >> 8) & 0x03

print("  atlas %dx%d, tilemap %d bytes" % (aw, ah, len(binmap)))
if WRITE:
    write_png4(os.path.join(GBA, "graphics/intro/copyright.png"), atlas, pal, aw, ah)
    open(os.path.join(GBA, "graphics/intro/copyright.bin"), "wb").write(bytes(binmap))
    # The palette is a separate .pal beside it.
    body = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in pal]
    open(os.path.join(GBA, "graphics/intro/copyright.pal"), "wb").write(
        ("\r\n".join(body) + "\r\n").encode())
    print("  written")

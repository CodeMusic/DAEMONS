#!/usr/bin/env python3
"""Redraw the type badges in graphics/interface/menu_info.png.

    python3 tools/gbatypes.py [--write]

The badges are pixel art, not strings -- gTypeNames feeds the move-select
window, and these are what the summary screen and the Index actually draw.
Each is 32x12 at a tile offset given by sMenuInfoIcons in src/list_menu.c, and
its index is the type constant plus one.

SIX CHARACTERS, and that is not a choice. The face is four pixels wide on a
five-pixel pitch, so six letters fill the badge edge to edge -- measured off
vanilla's own NORMAL, GROUND and DRAGON, all of which are exactly thirty
pixels of ink. Seven would need thirty-five.

THE FACE IS NOT DRAWN HERE. It is lifted out of graphics/fonts/latin_small.png,
which is FONT_SMALL -- the game's own half-width face, and already exactly four
pixels of ink on a five-pixel pitch. An earlier version of this tool drew its
own alphabet at that size and got three letters wrong in ways that only show up
in a word: a two-pixel stem made T read as I, and a W that tapered read as V,
so GROWTH came out GROHTH and FLOW came out FLOV. The shipped font solves all
three -- T has a one-pixel stem, V comes to a point, W does not.

Glyph cells are 8x16, thirty-two to a row, indexed by the charmap byte, so 'A'
is 0xBB. Colour 1 is the ink; the sheet's own shadow (colour 2) is discarded
and regenerated here, because the badge needs it on eight different grounds.

Which is why vanilla ships FIGHT, ELECTR and PSYCHC. It truncates, and it drops
a vowel, and we do the same for the seven- and eight-letter names:

    CONTENT -> CONTNT      ENTROPY  -> ENTRPY
    CORRUPT -> CORRPT      CONTEXT  -> CONTXT
    STRATUM -> STRATM      EMERGENT -> EMRGNT
                           HARDENED -> HARDND

CONTNT and CONTXT still differ in the middle rather than at the end, which is
the pair that most needs to stay apart at a glance.

Only the text is redrawn. Each badge keeps its own background colour and its
rounded corners, because the colour is how a type is recognised before the word
is read -- and 9.4 already spent that colour on meaning.
"""
import os, struct, sys, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PNG = os.path.join(GBA, "graphics/interface/menu_info.png")
WRITE = "--write" in sys.argv
WHITE, SHADOW = 0x1F, 0x1E
TEXT_TOP, PITCH, START_X = 2, 5, 1

# type badge tile offsets, from sMenuInfoIcons in src/list_menu.c
BADGES = [
    ("CONTNT", 0x20), ("LOGIC",  0x64), ("VECTOR", 0x60), ("CORRPT", 0x80),
    ("STRATM", 0x48), ("LEGACY", 0x44), ("SWARM",  0x6C), ("LATENT", 0x68),
    ("HARDND", 0x88), ("ENTRPY", 0x24), ("FLOW",   0x28), ("GROWTH", 0x2C),
    ("SIGNAL", 0x40), ("CONTXT", 0x84), ("FROZEN", 0x4C), ("EMRGNT", 0xA0),
    ("OPAQUE", 0x8C),
]

FONT = os.path.join(GBA, "graphics/fonts/latin_small.png")
CELL_W, CELL_H, CELLS_PER_ROW = 8, 16, 32
GLYPH_TOP, GLYPH_ROWS, INK = 4, 8, 1   # 7 rows of cap plus Q's tail
CHAR_A = 0xBB                          # charmap.txt: 'A'


def load(p):
    d = open(p, "rb").read(); i = 8; idat = b""; hdr = None; plte = None
    while i < len(d):
        ln = struct.unpack(">I", d[i:i+4])[0]; t = d[i+4:i+8]; c = d[i+8:i+8+ln]
        if t == b"IHDR": hdr = struct.unpack(">IIBBBBB", c)
        elif t == b"PLTE": plte = c
        elif t == b"IDAT": idat += c
        i += 12 + ln
    w, h, bd = hdr[0], hdr[1], hdr[2]
    raw = zlib.decompress(idat); stride = (w * bd + 7) // 8
    out = bytearray(); prev = bytearray(stride); o = 0
    for _ in range(h):
        f = raw[o]; o += 1; line = bytearray(raw[o:o+stride]); o += stride
        for x in range(stride):
            a = line[x-1] if x >= 1 else 0
            b = prev[x]; c2 = prev[x-1] if x >= 1 else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                pp = a + b - c2; pa, pb, pc = abs(pp-a), abs(pp-b), abs(pp-c2)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c2)) & 255
        out += line; prev = line
    if bd == 8:
        return w, h, plte, [[out[y*stride + x] for x in range(w)] for y in range(h)]
    # sub-byte depths pack several pixels per byte, high bits first
    per, mask = 8 // bd, (1 << bd) - 1
    return w, h, plte, [[(out[y*stride + x // per] >> (8 - bd - bd * (x % per))) & mask
                         for x in range(w)] for y in range(h)]

def save(p, w, h, plte, px):
    raw = b"".join(b"\x00" + bytes(row) for row in px)
    def ch(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c))
    open(p, "wb").write(b"\x89PNG\r\n\x1a\n"
        + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 3, 0, 0, 0))
        + ch(b"PLTE", plte) + ch(b"IDAT", zlib.compress(raw)) + ch(b"IEND", b""))

def readface():
    """Lift A-Z out of FONT_SMALL as ink masks, 4 wide and 8 tall."""
    fw, fh, _, fpx = load(FONT)
    face = {}
    for i in range(26):
        idx = CHAR_A + i
        cx = (idx % CELLS_PER_ROW) * CELL_W
        cy = (idx // CELLS_PER_ROW) * CELL_H + GLYPH_TOP
        rows = ["".join("#" if fpx[cy + r][cx + c] == INK else "."
                        for c in range(4)) for r in range(GLYPH_ROWS)]
        assert any("#" in r for r in rows), "no ink in cell %#x" % idx
        face[chr(ord("A") + i)] = rows
    return face

F = readface()
w, h, plte, px = load(PNG)
rc = 0
for name, off in BADGES:
    if len(name) > 6:
        print("  !! %s is %d characters; six is the badge" % (name, len(name))); rc = 1; continue
    x0, y0 = (off % 16) * 8, (off // 16) * 8
    # the background is whatever fills the badge's own interior
    bg = px[y0 + 1][x0 + 16]
    for y in range(2, 11):
        for x in range(1, 31):
            px[y0 + y][x0 + x] = bg
    # centre the word: six letters is 30px, fewer is narrower
    span = len(name) * PITCH
    ox = x0 + START_X + (30 - span) // 2
    for n, chx in enumerate(name):
        rows = F[chx]
        gx = ox + n * PITCH
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                if v != "#": continue
                px[y0 + TEXT_TOP + r][gx + c] = WHITE
                if px[y0 + TEXT_TOP + r + 1][gx + c + 1] == bg:
                    px[y0 + TEXT_TOP + r + 1][gx + c + 1] = SHADOW
    print("  %-7s at (%2d,%2d)  bg %02X" % (name, x0, y0, bg))
if WRITE and rc == 0:
    save(PNG, w, h, plte, px)
    print("  written")
sys.exit(rc)

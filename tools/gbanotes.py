#!/usr/bin/env python3
"""Draw the presents scene's particles: code becoming music.

    python3 tools/gbanotes.py [--write]

9.14: the field starts as 0 and 1 in flat code colour and becomes MUSICAL
NOTES in colour, and the change happens inside each particle's own animation
so the staggered lifetimes convert the field gradually rather than all at once.

The engine already does all of that. sparkles_small is an 8x8 sprite with a
FOUR-FRAME loop and sparkles_big is 32x32 with four more, both on one shared
palette -- so the transformation is four drawings and a palette, and not one
line of new code.

    small   0  ->  1  ->  note  ->  note, lit
    big     four notes, four colours

Not prompted for. A quaver at eight pixels square is about a dozen lit pixels
and no image model places a dozen pixels; these are drawn here, in palette,
the way the MARKS and the Index box were.

The palette is two ramps in one bank: 2-5 is the code, flat and cold, and
6-13 are the note colours. Nothing fades between them -- a particle simply
stops being one thing and starts being the other, which is the whole point.
"""
import os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GF = os.path.join(ROOT, "engineGba/graphics/intro/game_freak")
WRITE = "--write" in sys.argv

#            0 is transparent, 1 the outline, 2-5 the code, 6-13 the notes
PALETTE = [(0, 0, 0), (16, 16, 40),
           (0, 80, 72), (0, 144, 128), (64, 216, 192), (160, 248, 232),
           (216, 48, 120), (248, 120, 64), (248, 216, 72), (120, 216, 96),
           (72, 168, 248), (168, 112, 248), (248, 168, 200), (248, 248, 248),
           (128, 128, 160), (0, 0, 0)]

# ---------------------------------------------------------------- the small
# Four 8x8 frames. The first two are the digits, flat and cold; the second two
# are a note, and it lights.
ZERO = ["..###...",
        ".#...#..",
        ".#...#..",
        ".#...#..",
        ".#...#..",
        ".#...#..",
        "..###...",
        "........"]
ONE  = ["...##...",
        "..###...",
        "...##...",
        "...##...",
        "...##...",
        "...##...",
        "..####..",
        "........"]
NOTE = ["....##..",
        "....#.#.",
        "....##..",
        "....#...",
        "....#...",
        "..####..",
        ".####...",
        "..##...."]

def frame(rows, ink):
    return [[ink if c == '#' else 0 for c in r] for r in rows]

SMALL = [frame(ZERO, 3), frame(ONE, 4), frame(NOTE, 7), frame(NOTE, 8)]

# ------------------------------------------------------------------ the big
# Four 32x32 notes, four colours. A quaver, a beamed pair, a crotchet and a
# semiquaver -- different enough to read as MUSIC rather than as one repeated
# shape, which a shimmering field needs.
def blob(g, cx, cy, rx, ry, ink):
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if 0 <= x < 32 and 0 <= y < 32 and \
               ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                g[y][x] = ink

def stem(g, x, y0, y1, ink, w=2):
    for y in range(y0, y1 + 1):
        for k in range(w):
            if 0 <= x + k < 32 and 0 <= y < 32:
                g[y][x + k] = ink

def flag(g, x, y, ink):
    for i in range(7):
        for k in range(3):
            if 0 <= x + i // 2 + k < 32 and 0 <= y + i < 32:
                g[y + i][x + i // 2 + k] = ink

def beam(g, x0, x1, y, ink, h=3):
    for x in range(x0, x1 + 1):
        for k in range(h):
            g[y + k + (x - x0) // 6][x] = ink

def big_quaver(ink):
    g = [[0] * 32 for _ in range(32)]
    stem(g, 17, 5, 24, ink); flag(g, 19, 5, ink); blob(g, 14, 24, 6, 4, ink)
    return g

def big_pair(ink):
    g = [[0] * 32 for _ in range(32)]
    stem(g, 8, 6, 22, ink); stem(g, 23, 6, 18, ink)
    beam(g, 8, 24, 5, ink); blob(g, 6, 23, 5, 3, ink); blob(g, 21, 19, 5, 3, ink)
    return g

def big_crotchet(ink):
    g = [[0] * 32 for _ in range(32)]
    stem(g, 18, 4, 23, ink); blob(g, 14, 24, 7, 5, ink)
    return g

def big_semiquaver(ink):
    g = [[0] * 32 for _ in range(32)]
    stem(g, 17, 4, 24, ink); flag(g, 19, 4, ink); flag(g, 19, 11, ink)
    blob(g, 14, 24, 6, 4, ink)
    return g

BIG = [big_quaver(6), big_pair(9), big_crotchet(11), big_semiquaver(8)]

# ---------------------------------------------------------------- write them
def save(path, frames, fw, fh, cols):
    w, h = fw * cols, fh * ((len(frames) + cols - 1) // cols)
    im = Image.new("P", (w, h), 0)
    pal = []
    for c in PALETTE:
        pal += list(c)
    im.putpalette(pal[:48 * 1] + [0] * (768 - len(pal)) if False else pal)
    px = im.load()
    for i, g in enumerate(frames):
        ox, oy = (i % cols) * fw, (i // cols) * fh
        for y in range(fh):
            for x in range(fw):
                px[ox + x, oy + y] = g[y][x]
    used = sorted({px[x, y] for y in range(h) for x in range(w)})
    print("  %-22s %dx%d, %d frames, indices %s"
          % (os.path.basename(path), w, h, len(frames), used))
    if WRITE:
        im.save(path)

save(os.path.join(GF, "sparkles_small.png"), SMALL, 8, 8, 2)
save(os.path.join(GF, "sparkles_big.png"), BIG, 32, 32, 1)

if WRITE:
    # the .gbapal rule prefers .pal, so the colours have to be written there
    with open(os.path.join(GF, "sparkles.pal"), "w") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in PALETTE:
            f.write("%d %d %d\n" % c)
    print("  written: two sheets and the palette")

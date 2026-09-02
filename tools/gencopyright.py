#!/usr/bin/env python3
"""Redraw the copyright screen's three lines.

    python3 tools/gencopyright.py

The screen is built from raw tiles, not from the game font: PlaceString walks a
list of tile IDs that LoadCopyrightTiles has just copied into vChars2 $60. That
gives exactly 31 tiles ($60-$7E; $7F has to stay the blank the text-box tiles
left there, because the string uses it as a space), and every line has to fit
inside that one budget.

    (c)'11-'26  CODEMUSIC        <- gfx/title/gamefreak_inc.png, 7 tiles
    (c)'11-'26  SeeingSharp      <- 8 tiles
    (c)'11-'26  Psychology/Code  <- 11 tiles
                                    + 5 for the stamp = 31

The typeface is the vanilla copyright font, lifted pixel-for-pixel out of the
old strip: 2px strokes, caps on rows 1-5, x-height on rows 2-5, descenders to
row 6. Twelve glyphs it never had (S P h l g p y / 0 1 2 -) are drawn here in
the same idiom. CODEMUSIC keeps the bolder splash face from gensplash.py -- it
is the top line and should carry the weight.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import write_png

ENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
INK, PAPER = 0, 3

# Recovered from the strip this replaces. Rows are the full 8; a glyph's
# vertical position is part of its shape, so nothing here is re-baselined.
V = {
 '(c)': ".#####./##...##/#.###.#/#.#...#/#.###.#/##...##/.#####./.......",
 "'":   "##/.#/../../../../../..",
 '6':   "...../.####/##.../#####/##.##/#####/...../.....",
 'C':   "...../.####/###../###../###../.####/...../.....",
 'a':   "...../...../.####/##.##/#####/.####/...../.....",
 'c':   "..../..../####/##../##../####/..../....",
 'd':   "...../...##/.####/##.##/##.##/.####/...../.....",
 'e':   "..../..../.###/####/###./.###/..../....",
 'i':   "../##/../##/##/##/../..",
 'n':   "...../...../####./##.##/##.##/##.##/...../.....",
 'o':   "...../...../.###./##.##/##.##/.###./...../.....",
 'r':   "...../...../####./###.#/##..#/##.../...../.....",
 's':   "...../...../.####/####./.####/####./...../.....",
}
# Drawn to match: same weight, same rows, same 1px sidebearing.
N = {
 '1':   "..../.##./###./.##./.##./####/..../....",
 '2':   "...../####./...##/.###./##.../#####/...../.....",
 '-':   "..../..../..../####/..../..../..../....",
 '/':   "...../...##/..###/.###./###../##.../...../.....",
 'S':   "...../.####/##.../.###./...##/####./...../.....",
 'P':   "...../####./##.##/####./##.../##.../...../.....",
 'h':   "...../##.../##.../####./##.##/##.##/...../.....",
 'l':   "../##/##/##/##/##/../..",
 'g':   "...../...../.####/##.##/.####/...##/####./.....",
 'p':   "...../...../####./##.##/####./##.../##.../.....",
 'y':   "...../...../##.##/##.##/.####/...##/####./.....",
}
F = {k: v.split('/') for d in (V, N) for k, v in d.items()}

def strip(text, tiles):
    """Set `text` left-aligned in a `tiles`-wide canvas, 1px between glyphs."""
    w = tiles * 8
    g = [[PAPER] * w for _ in range(8)]
    x = 0
    for ch in text:
        rows = F['(c)' if ch == '@' else ch]
        for r, row in enumerate(rows):
            for i, px in enumerate(row):
                if px == '#':
                    g[r][x + i] = INK
        x += len(rows[0]) + 1
    if x - 1 > w:
        sys.exit("'%s' is %d px, will not fit %d tiles" % (text, x - 1, tiles))
    return g

# One canvas, because the three runs have to land on tile boundaries in the
# order the tile IDs are numbered.
LINES = [("@'11-'26", 5), ("SeeingSharp", 8), ("Psychology/Code", 11)]
out = [[] for _ in range(8)]
base = 0x60
for text, tiles in LINES:
    print("  $%02X-$%02X  %s" % (base, base + tiles - 1, text))
    base += tiles
    for r, row in enumerate(strip(text, tiles)):
        out[r] += row
write_png(os.path.join(ENG, "gfx/splash/copyright.png"), out, 2)
print("  gfx/splash/copyright.png %dx8" % len(out[0]))

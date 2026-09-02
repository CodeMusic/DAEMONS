#!/usr/bin/env python3
"""Draw the CodeMusic splash tiles: a falling note, a braced-note mark, wordmarks.

    python3 tools/gensplash.py

Replaces the GAME FREAK intro assets in place. All four are 2-bit greyscale at
the exact sizes the engine expects, and they follow the convention the vanilla
splash tiles use: background at level 3, ink at level 1. These render through a
palette rather than as black line art, so level 0 is never used.

Monochrome on purpose. Invariant 5 spends colour once, at the Review Board, and
a colourful splash before forty hours of grey reads as a limitation rather than
a choice. The ideas here are line and shape, and lose nothing without hue.

Everything is drawn rather than generated: 8x8 is one tile, and the sprite doc
already rules out generating anything under 16x16.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import write_png

ENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
# The vanilla splash does not use one convention: the star and the mark ink at
# level 1, while every text strip inks at level 0. They render through
# different palettes. Applying one value to all four made the wordmark a shade
# too light, which is what "a bit thin" looked like.
INK, PAPER = 1, 3
TEXT_INK = 0

def grid(art):
    return [[INK if c == '#' else (2 if c == '+' else PAPER) for c in row] for row in art]

# A quaver. The splash already flings this diagonally across the screen, so the
# star becoming a note makes the animation a glissando without touching code.
NOTE8 = [
    "....###.",
    "....#..#",
    "....#.#.",
    "....#...",
    "....#...",
    "..###...",
    ".#####..",
    "..###...",
]

# { note } -- braces are unambiguously code, a note unambiguously music, and
# neither needs explaining. 16x24, the GAME FREAK mark's exact footprint.
MARK = [
    "...##.......##..",
    "..##.........##.",
    "..#...........#.",
    "..#...........#.",
    "..#....###....#.",
    "..#....#..#...#.",
    "..#....#...#..#.",
    ".##....#......##",
    "##.....#.......#",
    "##.....#.......#",
    ".##....#......##",
    "..#..###......#.",
    "..#.#####.....#.",
    "..#..###......#.",
    "..#...........#.",
    "..#...........#.",
    "..#...........#.",
    "..#...........#.",
    "..#...........#.",
    "..#...........#.",
    "..#...........#.",
    "..#...........#.",
    "..##.........##.",
    "...##.......##..",
]

# Recovered from the earlier CODEMUSIC wordmark (engine 9a12df41) rather than
# redrawn. The 5x7 one-pixel font written first was too thin at this size --
# these are two-pixel strokes over five rows, proportional, and they hold.
# P R N T did not exist in the original nine letters and are drawn to match.
F = {
 'C':[".####","##...","##...","##...",".####"],
 'O':[".###.","##.##","##.##","##.##",".###."],
 'D':["####.","##.##","##.##","##.##","####."],
 'E':["####","##..","###.","##..","####"],
 'M':["##...##","###.###","##.#.##","##...##","##...##"],
 'U':["##.##","##.##","##.##","##.##",".###."],
 'S':[".####","##...",".###.","...##","####."],
 'I':["##","##","##","##","##"],
 'P':["####.","##.##","####.","##...","##..."],
 'R':["####.","##.##","####.","##.##","##.##"],
 'N':["##..##","###.##","##.###","##.###","##..##"],
 'T':["######","..##..","..##..","..##..","..##.."],
 ' ':["","","","",""],
}

def strip(text, w, h=8):
    glyphs = [F[c] for c in text]
    widths = [(4 if c == ' ' else len(F[c][0])) for c in text]
    width = sum(widths) + len(text) - 1
    if width > w:
        sys.exit("'%s' is %d px, will not fit %d" % (text, width, w))
    g = [[PAPER]*w for _ in range(h)]
    x = (w - width)//2
    for c, gw in zip(text, widths):
        for r, row in enumerate(F[c]):
            for i, px in enumerate(row):
                if px == '#':
                    g[r+1][x+i] = TEXT_INK
        x += gw + 1
    return g

JOBS = [("gfx/splash/falling_star.png",      grid(NOTE8)),
        ("gfx/splash/gamefreak_logo.png",    grid(MARK)),
        ("gfx/splash/gamefreak_presents.png", strip("CODEMUSIC PRESENTS", 104)),
        ("gfx/title/gamefreak_inc.png",      strip("CODEMUSIC", 56))]

for path, g in JOBS:
    write_png(os.path.join(ENG, path), g, 2)
    print("  %-40s %dx%d" % (path, len(g[0]), len(g)))

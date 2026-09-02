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
INK, PAPER = 1, 3

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

F = {
 'C':[".###.","#...#","#....","#....","#....","#...#",".###."],
 'O':[".###.","#...#","#...#","#...#","#...#","#...#",".###."],
 'D':["###..","#..#.","#...#","#...#","#...#","#..#.","###.."],
 'E':["#####","#....","#....","####.","#....","#....","#####"],
 'M':["#...#","##.##","#.#.#","#...#","#...#","#...#","#...#"],
 'U':["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
 'S':[".####","#....","#....",".###.","....#","....#","####."],
 'I':["#####","..#..","..#..","..#..","..#..","..#..","#####"],
 'p':[".....",".....","####.","#...#","####.","#....","#...."],
 'r':[".....",".....","#.###","##...","#....","#....","#...."],
 'e':[".....",".....",".###.","#...#","#####","#....",".###."],
 's':[".....",".....",".####","#....",".###.","....#","####."],
 'n':[".....",".....","#.##.","##..#","#...#","#...#","#...#"],
 't':["..#..","..#..","#####","..#..","..#..","..#.#","...#."],
 ' ':["....."]*7,
}

def strip(text, w, h=8):
    adv = {c: (3 if c == ' ' else 6) for c in set(text)}
    width = sum(adv[c] for c in text) - 1
    if width > w:
        sys.exit("'%s' is %d px, will not fit %d" % (text, width, w))
    g = [[PAPER]*w for _ in range(h)]
    x = (w - width)//2
    for c in text:
        for r, row in enumerate(F[c]):
            for i, p in enumerate(row):
                if p == '#':
                    g[r][x+i] = INK
        x += adv[c]
    return g

JOBS = [("gfx/splash/falling_star.png",      grid(NOTE8)),
        ("gfx/splash/gamefreak_logo.png",    grid(MARK)),
        ("gfx/splash/gamefreak_presents.png", strip("CODEMUSIC presents", 104)),
        ("gfx/title/gamefreak_inc.png",      strip("CODEMUSIC", 72))]

for path, g in JOBS:
    write_png(os.path.join(ENG, path), g, 2)
    print("  %-40s %dx%d" % (path, len(g[0]), len(g)))

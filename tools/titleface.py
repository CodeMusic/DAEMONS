#!/usr/bin/env python3
"""Light the title figure's face.

    python3 tools/titleface.py [--show]

Run AFTER converting generated art into gfx/title/player.png. It rewrites the
head, and nothing else.

Craft rule 6 says this game is funny in its ordinary moments. A wide flat brim
shadows a face by construction, so every generated sample came back with the
face in darkness -- at 40x56 that collapses to a black void with three light
pixels in it, and the player reads as a silhouette in a game whose antagonist
is written as genuinely warm. The art was arguing against the writing.

At this size a face is about ten pixels across, which means it is pixel art no
matter where the illustration came from. So it is drawn here rather than hoped
for from the generator.

Small marks, and as few of them as possible. The lit area is nine pixels by
three, so every dark mark placed in it fragments it: two-pixel eyes read as a
visor, a three-pixel mouth reads as a grimace, and rounding the corners split
the light into two patches and put the visor back. One pixel per eye and two
for the mouth is the entire face.

The real constraint is that the hat is enormous and leaves the head three rows.
Vanilla gives its trainer roughly ten. If this face is ever to carry more than
an expression, the hat has to come up, not the face get busier.

The head sits under the brim at rows 7-10, columns 15-25 -- four rows, and the
shoulders start at row 11, so brow, eyes and mouth get one row each. Row 7
stays solid: that is the shadow the brim casts, and it is what makes the hat
read as a hat rather than a halo.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import read_png, write_png

ENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
DST = os.path.join(ENG, "gfx/title/player.png")
X0, Y0 = 15, 7

#      15         25
FACE = [
    "###########",   # 7  the brim's shadow, kept solid
    "#.........#",   # 8  brow
    "#..#...#..#",   # 9  eyes -- one pixel each, and that is enough
    "#....##...#",   # 10 a small mouth
]
LV = {"#": 0, ":": 1, ".": 2, " ": 3}

w, h, lum = read_png(DST)
g = [[min(3, lum(x, y) * 4 // 256) for x in range(w)] for y in range(h)]
for dy, row in enumerate(FACE):
    for dx, c in enumerate(row):
        g[Y0 + dy][X0 + dx] = LV[c]
write_png(DST, g, 2)
print("  lit the face on %s" % os.path.relpath(DST, os.path.dirname(ENG)))
if "--show" in sys.argv:
    for y in range(0, 20):
        print("  %2d %s" % (y, "".join("#:. "[v] for v in g[y])))

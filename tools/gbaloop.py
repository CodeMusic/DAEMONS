#!/usr/bin/env python3
"""Draw the mark behind CODEMUSIC.

    python3 tools/gbaloop.py [--write]

The slot held GAME FREAK's gold flame: 32x64, two tones on a dark ground.

Ours is two rings crossing -- a feedback loop stood upright. The LOWER one is
code and the UPPER one is music, each drawn semi-monochrome in its own cold or
warm ramp so neither is more than one colour of thing. Where they overlap, and
only there, the palette gets bright.

That is 9.14's sanctioned spend stated as a shape: COLOUR IS WHAT ARRIVES WHEN
TWO THINGS THAT DISAGREE CONNECT. The scene then spends the next few seconds
proving it with the particles, and nothing says so.

Shading is by angle rather than by a light source -- the outer upper-left of
each ring is its light tone and the inner lower-right its dark one -- which at
this size reads as roundness without costing a ramp.
"""
import math, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GF = os.path.join(ROOT, "engineGba/graphics/intro/game_freak")
WRITE = "--write" in sys.argv
W, H = 32, 64

#           0 is the scene's own dark ground, kept
PALETTE = [(24, 40, 72), (0, 0, 0),
           (0, 72, 96), (0, 144, 176), (96, 216, 240),      # 2-4  code, cold
           (128, 32, 72), (216, 56, 120), (248, 144, 176),  # 5-7  music, warm
           (248, 232, 120), (248, 248, 248),                # 8-9  where they meet
           (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

CODE, MUSIC, MEET = (2, 3, 4), (5, 6, 7), (8, 9)

def ring(cx, cy, rx, ry, t):
    """Points on an elliptical band, with the angle each sits at."""
    out = {}
    for y in range(H):
        for x in range(W):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if 1.0 - t <= d <= 1.0 + t:
                out[(x, y)] = math.atan2(y - cy, x - cx)
    return out

def tone(ramp, ang):
    """Upper-left of the ring is its light tone, lower-right its dark one."""
    lit = math.cos(ang - math.radians(225))
    return ramp[2] if lit > 0.45 else (ramp[0] if lit < -0.45 else ramp[1])

music = ring(16, 21, 11.5, 13.5, 0.30)
code  = ring(16, 43, 11.5, 13.5, 0.30)

g = [[0] * W for _ in range(H)]
for (x, y), a in music.items():
    g[y][x] = tone(MUSIC, a)
for (x, y), a in code.items():
    g[y][x] = MEET[1] if (x, y) in music else tone(CODE, a)
# a soft halo on the crossing, so the meeting reads as light rather than as a join
for (x, y) in list(music.keys() | code.keys()):
    if g[y][x] == MEET[1]:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and g[ny][nx] not in MEET and g[ny][nx] != 0:
                g[ny][nx] = MEET[0]

im = Image.new("P", (W, H), 0)
pal = []
for c in PALETTE:
    pal += list(c)
im.putpalette(pal)
px = im.load()
for y in range(H):
    for x in range(W):
        px[x, y] = g[y][x]
meet = sum(1 for y in range(H) for x in range(W) if g[y][x] in MEET)
print("  logo 32x64, indices %s, %d pixels where they meet"
      % (sorted({g[y][x] for y in range(H) for x in range(W)}), meet))

if WRITE:
    im.save(os.path.join(GF, "logo.png"))
    with open(os.path.join(GF, "logo.pal"), "w") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in PALETTE:
            f.write("%d %d %d\n" % c)
    print("  written: logo and palette")

#!/usr/bin/env python3
"""Draw the player as they stand on the title screen, with the daemons cycling past.

    python3 tools/gentitle.py [--show]

gfx/title/player.png is 40x56 and is drawn as OAM sprites beside whichever
daemon the title screen is currently showing. Level 3 is transparent.

Same character as the overworld sprite and built to the same rules -- the brim
is the widest thing on the figure, the coat reaches the ground, and the sleeves
are separated from the torso by TONE rather than by a gap. At 40px there is
finally room for the thing the 16x16 sprite could only imply: the unit itself,
held down at the side. 1.3 calls it a machine you offer a daemon as a host, so
it is drawn as one -- a vent line, an indicator, a port, and no seam anywhere
that would let it open.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import write_png

ENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
W, H, CLEAR = 40, 56, 3
g = [[CLEAR] * W for _ in range(H)]

def px(x, y, v):
    if 0 <= x < W and 0 <= y < H: g[y][x] = v

def rect(x0, y0, x1, y1, v=0, fill=None):
    if fill is not None:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): px(x, y, fill)
    for x in range(x0, x1 + 1): px(x, y0, v); px(x, y1, v)
    for y in range(y0, y1 + 1): px(x0, y, v); px(x1, y, v)

def ellipse(cx, cy, rx, ry, v=0, fill=None):
    for y in range(H):
        for x in range(W):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 0.82 and fill is not None: px(x, y, fill)
            elif d <= 1.0: px(x, y, v)

def band(y0, y1, x0, x1, v):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): px(x, y, v)

def outline():
    """Any ink pixel touching transparency becomes the black edge."""
    edge=[]
    for y in range(H):
        for x in range(W):
            if g[y][x] == CLEAR: continue
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if not (0 <= nx < W and 0 <= ny < H) or g[ny][nx] == CLEAR:
                    edge.append((x, y)); break
    for x, y in edge: px(x, y, 0)

# --- the coat -------------------------------------------------------------
band(29, 48, 10, 29, 1)                       # torso
band(30, 47, 10, 13, 2)                       # left sleeve
band(30, 47, 26, 29, 2)                       # right sleeve
for y in range(49, 56):                       # the hem, flaring to the ground
    w = 11 + (y - 49)
    band(y, y, 20 - w, 19 + w, 1)
outline()
for y in range(30, 48):                       # sleeve seams, inside the silhouette
    px(14, y, 0); px(25, y, 0)
for y in range(31, 47):                       # the strap, shoulder to opposite hip
    x = 24 - (y - 31) * 9 // 15
    px(x, y, 0); px(x + 1, y, 0)
band(44, 47, 10, 13, 2); band(44, 47, 26, 29, 2)   # cuffs stay light
band(29, 30, 15, 24, 0)                       # collar

# --- the unit, held at the right hand --------------------------------------
rect(28, 44, 38, 53, 0, fill=1)
band(47, 48, 30, 35, 2)                       # vent
rect(34, 50, 36, 51, 0, fill=2)               # indicator
band(46, 51, 38, 38, 0)                       # port side

# --- head and hat ----------------------------------------------------------
band(17, 27, 14, 25, 2)                       # face
rect(13, 16, 26, 28, 0)
band(21, 22, 17, 18, 0); band(21, 22, 21, 22, 0)   # eyes
ellipse(20, 14, 19, 3, 0, fill=1)             # brim
rect(14, 3, 25, 14, 0, fill=1)                # crown
band(11, 13, 14, 25, 0)                       # hatband

write_png(os.path.join(ENG, "gfx/title/player.png"), g, 2)
print("  gfx/title/player.png %dx%d" % (W, H))
if "--show" in sys.argv:
    for r in g: print("   " + "".join("#:. "[v] for v in r))

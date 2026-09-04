#!/usr/bin/env python3
"""Draw the title screen's particles: what crosses the gap, and what happens there.

    python3 tools/gbabloom.py [--write]

The slot held FireRed's fire, rising off the floor. 9.14 spends it differently:
particles leave EACH creature and travel toward the other, and the ten frames
the engine already gives every particle carry the whole life.

    0-2   from CODEMUSAI -- 0 and 1, cold, flickering
    3-5   from CAREMUSAI -- a note, warm
    6-9   the BLOOM, where the two arrive at the same place

Which is the same sentence as the presents scene and the mark behind it: colour
is what arrives when two things that disagree connect. Three scenes saying one
thing, and none of them saying it.

Ten frames of 16x16, four tiles each, forty tiles -- exactly the 0x500 the
sheet already reserves. Nothing about the sprite or its size changes.
"""
import math, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
S = 16

#           0 transparent | 1-3 code, cold | 4-6 music, warm | 7-10 the bloom
PALETTE = [(0, 0, 0),
           (16, 72, 112), (48, 160, 216), (152, 232, 248),
           (128, 24, 80), (216, 56, 136), (248, 160, 208),
           (248, 176, 56), (248, 224, 128), (248, 248, 200), (248, 248, 248),
           (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

def grid():
    return [[0] * S for _ in range(S)]

def stamp(g, rows, ox, oy, ink):
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == '#' and 0 <= ox + x < S and 0 <= oy + y < S:
                g[oy + y][ox + x] = ink

ZERO = ["####", "#..#", "#..#", "#..#", "#..#", "####"]
ONE  = [".##.", "###.", ".##.", ".##.", ".##.", "####"]
NOTE = ["...##", "...#.#", "...##", "...#", "...#", "####", "###"]

def code_mote(bright):
    g = grid()
    stamp(g, ZERO if bright else ONE, 6, 5, 2 if bright else 3)
    return g

def music_mote(ink):
    g = grid()
    stamp(g, NOTE, 5, 5, ink)
    return g

def bloom(step):
    """A ring that opens and thins. The last frame is nearly gone, which is why
    the sprite is destroyed on animEnded rather than on a timer."""
    g = grid()
    # The ring must stay INSIDE its own sprite. At 16x16 the furthest a pixel
    # sits from the centre is about 10.6, so a radius of 11 is a frame that
    # draws nothing -- which is what the last one was doing.
    r = 1.5 + step * 2.6
    thick = 2.4 - step * 0.3
    ink = (10, 9, 8, 7)[step]
    for y in range(S):
        for x in range(S):
            d = math.hypot(x - 7.5, y - 7.5)
            if abs(d - r) <= thick / 2:
                g[y][x] = ink
    if step == 0:                       # the first frame is a point of light
        for y in range(6, 10):
            for x in range(6, 10):
                g[y][x] = 10
    return g

FRAMES = [code_mote(False), code_mote(True), code_mote(False),
          music_mote(5), music_mote(6), music_mote(5),
          bloom(0), bloom(1), bloom(2), bloom(3)]

im = Image.new("P", (S, S * len(FRAMES)), 0)
pal = []
for c in PALETTE:
    pal += list(c)
im.putpalette(pal)
px = im.load()
for i, g in enumerate(FRAMES):
    for y in range(S):
        for x in range(S):
            px[x, i * S + y] = g[y][x]

used = sorted({px[x, y] for y in range(im.height) for x in range(im.width)})
print("  %d frames of %dx%d = %d tiles (the sheet reserves 40); indices %s"
      % (len(FRAMES), S, S, len(FRAMES) * 4, used))

if WRITE:
    for rel in ("graphics/title_screen/firered/flames.png",
                "graphics/title_screen/leafgreen/leaves.png"):
        im.save(os.path.join(GBA, rel))
        print("  written: %s" % rel)

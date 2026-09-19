#!/usr/bin/env python3
"""T-163: MISSINGNO, an homage (decided by the user 2026-09-18).

The original is a backwards-L block of scrambled tile data. This keeps the shape and makes the scramble legible: the
block is a dark body filled with columns of falling green code -- a bright head glyph and a trail fading down the
column. It is generated, not drawn by the model, because it IS code; a fixed seed makes it rebuild identically.
The body is mid-dark grey so gbasprite.py ramps it to CORRUPT's mould (MISSINGNO is POISON/MYSTERY); the greens are
far enough from CORRUPT's hue that the build keeps them as accents -- a glitch that the colour rule does not touch.
Writes 512x512 drafts (8px per art pixel, the spriteforge grid) for cleandraft.py."""
import random
from PIL import Image

GLYPHS = [  # 3x4 bit patterns: fragments of katakana-like marks and digits
    ["111", "001", "010", "100"], ["101", "111", "001", "001"], ["110", "010", "011", "010"], ["111", "100", "111", "001"],
    ["010", "111", "010", "010"], ["100", "110", "101", "110"], ["011", "100", "010", "001"], ["111", "101", "101", "111"],
    ["001", "011", "101", "001"], ["110", "001", "010", "111"],
]
BODY, EDGE = (72, 74, 72), (8, 10, 8)
TRAIL = [(200, 255, 200), (40, 230, 90), (20, 180, 70), (10, 130, 50), (5, 90, 35)]

def inside(x, y, flip):
    if flip:
        x = 63 - x
    return (40 <= x <= 57 and 5 <= y <= 58) or (6 <= x <= 57 and 40 <= y <= 58)   # the backwards L

def draw(seed, flip):
    rnd = random.Random(seed)
    art = [[None] * 64 for _ in range(64)]
    for y in range(64):
        for x in range(64):
            if inside(x, y, flip):
                edge = any(not inside(x + dx, y + dy, flip) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                art[y][x] = EDGE if edge else BODY
    for cx, head in [(cx, h) for cx in range(4, 60, 4) for h in (rnd.randrange(0, 26), rnd.randrange(30, 56))]:
        for k, cy in enumerate(range(head, 64, 5)):  # two drops a column; falling: bright head, fading trail
            if k >= len(TRAIL) or rnd.random() < 0.18:
                continue
            g = rnd.choice(GLYPHS)
            for gy in range(4):
                for gx in range(3):
                    x, y = cx + gx, cy + gy
                    if g[gy][gx] == "1" and 0 <= y < 64 and art[y][x] == BODY:
                        art[y][x] = TRAIL[k]
    im = Image.new("RGB", (512, 512), (255, 255, 255))
    px = im.load()
    for y in range(64):
        for x in range(64):
            if art[y][x]:
                for yy in range(8):
                    for xx in range(8):
                        px[x * 8 + xx, y * 8 + yy] = art[y][x]
    return im

draw(1996, False).save("gfx/drafts/t163/missingno_front.png")   # the year the original was first seen
draw(2026, True).save("gfx/drafts/t163/missingno_back.png")     # the back: the same block from behind, other code

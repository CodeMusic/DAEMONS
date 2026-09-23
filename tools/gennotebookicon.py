#!/usr/bin/env python3
"""The NOTEBOOK's item icon, authored in code (T-216; docs/school.md 9).

    python3 tools/gennotebookicon.py            # preview to /tmp/notebook_icon.png
    python3 tools/gennotebookicon.py --write    # graphics/items/icons/notebook.png + its palette

WHAT IT IS. A bound notebook, closed, with an elastic band down the right and its page edges showing --
the thing a researcher keeps, not a thing a shop sells.

WHY THE COVER IS CONTEXT'S COLOUR. Invariant 5: colour carries the argument or it is not used. The Index
holds what a daemon IS; the notebook holds what happened AROUND it -- and the two editions of this game are
called CONTENT and CONTEXT. So the cover is CONTEXT's hue, read out of gbasprite.py's TYPE_COLOR at run time
rather than copied, as the PLUGIN discs are (T-211). Nothing in the game says why, and nothing may.

FORMAT. 24x24, mode "P", sixteen colours, entry 0 transparent; the palette ships beside the picture as a
JASC .pal the build turns into a .gbapal (the same as OPUS's, T-197).
"""
import os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv


def context_hue():
    src = open(os.path.join(ROOT, "tools/gbasprite.py"), encoding="utf-8").read()
    body = re.search(r'TYPE_COLOR = \{(.*?)\n\}', src, re.S).group(1)
    r, g, b = re.search(r'"PSYCHIC":\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\)', body).groups()
    return int(r), int(g), int(b)


def shade(c, t):
    return tuple(max(0, min(255, int(v * t))) for v in c)


def lift(c, t):
    return tuple(min(255, int(v + (255 - v) * t)) for v in c)


hue = context_hue()
PAL = [
    (0, 0, 0),              # 0 transparent
    (16, 16, 20),           # 1 ink -- the project's one outline black (T-184)
    lift(hue, 0.35),        # 2 cover, lit
    hue,                    # 3 cover
    shade(hue, 0.70),       # 4 cover, shade
    shade(hue, 0.45),       # 5 spine
    (243, 241, 232),        # 6 page edge, lit
    (214, 210, 196),        # 7 page edge
    (60, 58, 66),           # 8 band
] + [(0, 0, 0)] * 7

W = H = 24
px = [[0] * W for _ in range(H)]


def rect(x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[y][x] = c


# pages first, peeking out right and bottom
rect(6, 4, 19, 21, 7)
for y in range(5, 21, 2):
    px[y][19] = 6
for x in range(7, 19, 2):
    px[21][x] = 6
# the cover
rect(5, 3, 18, 20, 3)
rect(6, 4, 17, 6, 2)          # the lit top edge
rect(5, 3, 7, 20, 5)          # the spine
rect(16, 7, 18, 20, 4)        # shade toward the band
rect(15, 3, 15, 20, 8)        # the elastic band
# a label, blank -- nobody wrote a title on it
rect(9, 8, 13, 11, 6)
# the outline
for y in range(2, 23):
    for x in range(4, 21):
        if px[y][x] == 0 and any(0 <= y + dy < H and 0 <= x + dx < W and px[y + dy][x + dx] not in (0, 1)
                                 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            px[y][x] = 1

img = Image.new("P", (W, H))
flat = []
for c in PAL:
    flat += list(c)
img.putpalette(flat + [0] * (768 - len(flat)))
img.putdata([c for row in px for c in row])

if WRITE:
    img.save(os.path.join(GBA, "graphics/items/icons/notebook.png"))
    with open(os.path.join(GBA, "graphics/items/icon_palettes/notebook.pal"), "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in PAL))
    print("  written graphics/items/icons/notebook.png and icon_palettes/notebook.pal")
else:
    img.convert("RGB").resize((W * 8, H * 8), Image.NEAREST).save("/tmp/notebook_icon.png")
    print("  preview /tmp/notebook_icon.png  cover", hue)

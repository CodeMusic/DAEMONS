#!/usr/bin/env python3
"""The NOTEBOOK's, the TEXTBOOK's and the DIPLOMA's item icons, authored in code (T-216, T-219; docs/school.md 6, 9).

    python3 tools/gennotebookicon.py            # preview to /tmp/notebook_icon.png
    python3 tools/gennotebookicon.py --write    # graphics/items/icons/notebook.png + its palette

WHAT IT IS. A bound notebook, closed, with an elastic band down the right and its page edges showing --
the thing a researcher keeps, not a thing a shop sells.

THE TEXTBOOK (T-219) is the same object in CONTENT's hue, with a title band instead of an elastic: the
textbook holds what things ARE, the notebook what happened AROUND them. The two editions, again, and unsaid.

THE DIPLOMA (T-218) is a rolled certificate tied with a ribbon, in paper and ink and nothing else: a diploma
has no type, so it gets no hue -- the same rule the exam's own screen keeps.

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


def type_hue(key):
    src = open(os.path.join(ROOT, "tools/gbasprite.py"), encoding="utf-8").read()
    body = re.search(r'TYPE_COLOR = \{(.*?)\n\}', src, re.S).group(1)
    r, g, b = re.search(r'"%s":\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\)' % key, body).groups()
    return int(r), int(g), int(b)


def shade(c, t):
    return tuple(max(0, min(255, int(v * t))) for v in c)


def lift(c, t):
    return tuple(min(255, int(v + (255 - v) * t)) for v in c)


def make(hue, textbook):
    PAL = [
        (0, 0, 0), (16, 16, 20), lift(hue, 0.35), hue, shade(hue, 0.70), shade(hue, 0.45),
        (243, 241, 232), (214, 210, 196), (60, 58, 66),
    ] + [(0, 0, 0)] * 7
    W = H = 24
    px = [[0] * W for _ in range(H)]

    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px[y][x] = c

    rect(6, 4, 19, 21, 7)
    for y in range(5, 21, 2):
        px[y][19] = 6
    for x in range(7, 19, 2):
        px[21][x] = 6
    rect(5, 3, 18, 20, 3)
    rect(6, 4, 17, 6, 2)
    rect(5, 3, 7, 20, 5)
    rect(16, 7, 18, 20, 4)
    if textbook:
        rect(8, 9, 18, 11, 5)            # a title band across the cover, and two ruled lines on it
        rect(10, 10, 16, 10, 6)
        rect(9, 14, 15, 14, 4); rect(9, 16, 13, 16, 4)
    else:
        rect(15, 3, 15, 20, 8)           # the elastic band
        rect(9, 8, 13, 11, 6)            # a label, blank -- nobody wrote a title on it
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
    return img, PAL


def make_diploma():
    PAL = [(0, 0, 0), (16, 16, 20), (243, 241, 232), (222, 218, 204), (190, 184, 166), (60, 58, 66), (96, 92, 104)] + [(0, 0, 0)] * 9
    W = H = 24
    px = [[0] * W for _ in range(H)]
    for y in range(8, 16):                  # the roll: lit along the top, shaded along the bottom
        for x in range(4, 21):
            px[y][x] = 2 if y < 11 else (3 if y < 14 else 4)
    for y in range(8, 16):                  # the rolled ends, curling
        px[y][4] = 4; px[y][20] = 3; px[y][19] = 4
    for y in range(7, 17):                  # the ribbon round its middle
        px[y][11] = 5; px[y][12] = 6
    for (x, y) in ((10, 17), (9, 18), (8, 19), (13, 17), (14, 18), (15, 19)):
        px[y][x] = 5                        # and its two tails
    for y in range(1, 23):
        for x in range(1, 23):
            if px[y][x] == 0 and any(px[y + dy][x + dx] not in (0, 1) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[y][x] = 1
    img = Image.new("P", (W, H))
    flat = []
    for c in PAL:
        flat += list(c)
    img.putpalette(flat + [0] * (768 - len(flat)))
    img.putdata([c for row in px for c in row])
    return img, PAL


for stem, key, textbook in (("notebook", "PSYCHIC", False), ("textbook", "NORMAL", True), ("diploma", None, None)):
    img, PAL = make_diploma() if stem == "diploma" else make(type_hue(key), textbook)
    if WRITE:
        img.save(os.path.join(GBA, "graphics/items/icons/%s.png" % stem))
        with open(os.path.join(GBA, "graphics/items/icon_palettes/%s.pal" % stem), "w", newline="\r\n") as f:
            f.write("JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in PAL))
        print("  written graphics/items/icons/%s.png and its palette" % stem)
    else:
        img.convert("RGB").resize((24 * 8, 24 * 8), Image.NEAREST).save("/tmp/%s_icon.png" % stem)
        print("  preview /tmp/%s_icon.png" % stem)

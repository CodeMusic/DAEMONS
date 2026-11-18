#!/usr/bin/env python3
"""DAVID's COMPASS, the bag's icon (T-586, the user 2026-11-17; DRAFT, drawn in code).

    python3 tools/gencompass.py            # report whether the engine's icon and palette match, and a 4x preview
    python3 tools/gencompass.py --write    # write graphics/items/icons/compass.png and icon_palettes/compass.pal

A small round compass in the house look: a dark rim, a paper face with a faint graph-paper cross, four ticks and a
needle, red to the north. Nothing on it is lettered -- at 24px a letter would be a smudge, and the rose's letters are
the screen's (src/daemons_compass.c draws the rose itself, with the same paper, ink, teal and red).
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
ICON = "graphics/items/icons/compass.png"
PAL = "graphics/items/icon_palettes/compass.pal"

#  The screen's colours (sCompassPal, RGB555 x 8), so the icon and the rose are one object.
PALETTE = [
    (0, 0, 0),          # 0 none
    (240, 240, 216),    # 1 paper
    (184, 216, 208),    # 2 grid
    (144, 184, 176),    # 3 rule
    (40, 64, 72),       # 4 ink
    (88, 120, 128),     # 5 ink, lighter
    (200, 56, 48),      # 6 red
    (24, 144, 136),     # 7 teal
    (56, 80, 88),       # 8 dark
] + [(0, 0, 0)] * 7


def icon():
    px = [[0] * 24 for _ in range(24)]
    cx, cy = 11.5, 11.5
    for y in range(24):
        for x in range(24):
            r2 = (x - cx) ** 2 + (y - cy) ** 2
            if r2 <= 10.6 ** 2:
                px[y][x] = 4                            # the rim
            if r2 <= 9.4 ** 2:
                px[y][x] = 7 if (x + y) % 9 == 0 and r2 > 8.4 ** 2 else 5   # a teal glint on the bezel
            if r2 <= 8.2 ** 2:
                px[y][x] = 1                            # the face
    for k in range(5, 19):                              # the cross, faint
        px[11][k] = px[11][k] if px[11][k] != 1 else 2
        px[12][k] = px[12][k] if px[12][k] != 1 else 2
        px[k][11] = px[k][11] if px[k][11] != 1 else 2
        px[k][12] = px[k][12] if px[k][12] != 1 else 2
    for x, y in ((11, 4), (12, 4), (11, 19), (12, 19), (4, 11), (4, 12), (19, 11), (19, 12)):
        px[y][x] = 3                                    # four ticks
    for y in range(5, 19):                              # the needle, a long diamond: red north, dark south
        xs = (11, 12) if y < 8 or y > 15 else (10, 11, 12, 13)
        for x in xs:
            px[y][x] = 6 if y < 12 else 8
    for x, y in ((11, 11), (12, 11), (11, 12), (12, 12)):
        px[y][x] = 4                                    # the pin
    im = Image.new("P", (24, 24))
    im.putpalette([c for rgb in PALETTE for c in rgb] + [0] * (768 - 48))
    im.putdata([v for row in px for v in row])
    return im


def jasc():
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in PALETTE)


def main():
    im = icon()
    want_pal = jasc()
    ip, pp = os.path.join(ENGINE, ICON), os.path.join(ENGINE, PAL)
    same_icon = os.path.exists(ip) and list(Image.open(ip).getdata()) == list(im.getdata()) and \
        Image.open(ip).getpalette()[:48] == im.getpalette()[:48]
    same_pal = os.path.exists(pp) and open(pp, newline="").read() == want_pal
    if same_icon and same_pal:
        print("gencompass: the icon and its palette are current")
        return
    if not WRITE:
        prev = os.path.join(os.environ.get("TMPDIR", "/tmp"), "gencompass_preview.png")
        im.convert("RGB").resize((96, 96), Image.NEAREST).save(prev)
        print("gencompass: would write %s%s (preview %s)" % ("" if same_icon else ICON + " ",
                                                             "" if same_pal else PAL, prev))
        return
    im.save(ip)
    with open(pp, "w", newline="") as f:
        f.write(want_pal)
    print("gencompass: wrote %s and %s" % (ICON, PAL))


if __name__ == "__main__":
    main()

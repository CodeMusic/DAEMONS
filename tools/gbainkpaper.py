#!/usr/bin/env python3
"""INK AND PAPER for the screens that still wore vanilla's theme (T-209; decided by the user, 2026-09-24).

    python3 tools/gbainkpaper.py            # report
    python3 tools/gbainkpaper.py --write     # the POOL's screen palettes and the STREAM's

"It looks too much like TeachyTV." The STREAM wore TeachyTV's yellow frame and the POOL vanilla's orange and teal.
The house palette the user chose is the books': near-black frames, warm paper, one brass accent -- and its rule is
9.4's: colour carries the type chart, so no UI colour may be a type's hue. Everything maps by ROLE:

  * a warm, saturated colour (the frames' orange and yellow) becomes INK, darkest to lightest, and only its
    lightest highlight becomes the one BRASS accent;
  * everything else -- the teal ground, the navy, the greys, the creams -- falls on one ramp from INK to PAPER
    by lightness, so a dark thing stays dark and text stays legible against what it sat on.

Index 0 of every sixteen is transparency and is never touched. Text colours (bag_window_pal.pal) are not in the
list: they are read as colours, and changing them is a different question.
"""
import colorsys, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
PNGS = [("graphics/item_menu/bg.png", 16), ("graphics/teachy_tv/tiles.png", 64)]   # the STREAM loads four rows of it
PALS = ["graphics/item_menu/bg_female.pal"]

#  THE BADGE (the user, 2026-09-25: "the intro showed a logo, but I didn't see it say STREAM"). Row 2 of the STREAM's
#  palette is the title badge's alone (screen.bin's row-2 cells are all transparent), and mapping it by lightness put
#  the cloud, the letters and their shadow on the SAME grey -- the word was there and could not be seen. So the badge
#  is mapped by what each index draws, not how light it is: a paper card on the black ground, the letters in ink with
#  the brass accent as their shadow, the play mark in ink and the wave in brass.
BADGE_ROW = 2
BADGE = {1: 4, 2: 7, 3: 7, 4: 6, 5: 0, 6: 1, 7: "b", 8: 5, 9: 0, 10: 4, 11: "b", 12: 4, 13: 5}   # index -> RAMP step, "b" brass

RAMP = [(30, 27, 29), (58, 52, 50), (96, 88, 82), (150, 140, 128), (200, 188, 164), (226, 216, 194), (246, 238, 218), (252, 248, 236)]
BRASS = [(110, 82, 36), (150, 116, 54), (190, 150, 72), (222, 186, 112)]


def lum(c):
    return (c[0] * 77 + c[1] * 150 + c[2] * 29) / 256


def ink(c):
    if c in RAMP or c in BRASS or c == (255, 0, 255):
        return c
    h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in c))
    if s > 0.4 and (h < 0.17 or h > 0.95) and 0.15 < l < 0.9:       # warm and saturated: the frames and the gold
        #  the frames go to INK -- "near-black frames" -- and only their lightest highlight keeps the one brass
        return BRASS[2] if l > 0.62 else RAMP[0 if l < 0.35 else 1 if l < 0.5 else 2]
    return min(RAMP, key=lambda r: abs(lum(r) - lum(c)))


def read_pal(p):
    lines = open(p, newline="").read().replace("\r\n", "\n").split("\n")
    n = int(lines[2])
    return [tuple(int(v) for v in lines[3 + i].split()) for i in range(n)]


def write_pal(p, cols):
    open(p, "w").write("JASC-PAL\n0100\n%d\n" % len(cols) + "".join("%d %d %d\n" % c for c in cols))


def main():
    changed = []
    for rel, n in PNGS:
        p = os.path.join(GBA, rel)
        im = Image.open(p)
        pal = im.getpalette()
        n = min(n, len(pal) // 3)
        cols = [tuple(pal[i:i + 3]) for i in range(0, 3 * n, 3)]
        new = [cols[i] if i % 16 == 0 else ink(cols[i]) for i in range(n)]
        if rel.startswith("graphics/teachy_tv/"):
            for i, role in BADGE.items():
                new[16 * BADGE_ROW + i] = BRASS[2] if role == "b" else RAMP[role]
        if new != cols:
            changed.append(rel)
            if WRITE:
                im.putpalette([v for c in new for v in c] + pal[3 * n:])
                im.save(p)
    for rel in PALS:
        p = os.path.join(GBA, rel)
        cols = read_pal(p)
        new = [cols[i] if i % 16 == 0 else ink(cols[i]) for i in range(len(cols))]
        if new != cols:
            changed.append(rel)
            if WRITE:
                write_pal(p, new)
    for c in changed or ["every screen already in ink and paper"]:
        print("  " + c + (" -> ink and paper" if changed else ""))
    if WRITE and changed:
        print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())

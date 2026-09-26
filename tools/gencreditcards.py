#!/usr/bin/env python3
"""The four daemon cards in the credits: ROVERBYTE, MUSAI, ARTSAI and STARR (T-290).

    python3 tools/gencreditcards.py            # report, and a preview in the scratch dir
    python3 tools/gencreditcards.py --write    # graphics/credits/<name>_1.png and _2.png

FireRed's credits stop four times on a card: the creature's front picture, then the same creature twice more,
larger, as the picture grows toward the viewer. The front picture already came from the species slot and so was
ours; the two larger ones were vanilla's CHARIZARD, VENUSAUR, BLASTOISE and PIKACHU, drawn once, full size, in a
game that shows no Pokemon anywhere else. The user named the four daemons that belong there (2026-09-26).

The larger pictures are made from the daemon's OWN front picture, so a card can never disagree with the
daemon: scaled smoothly in colour, then put back on the daemon's sixteen colours, because the card is drawn in
the palette LoadMonPicInWindow has just loaded for the front picture. Each card keeps its window's size -- the
three windows of a card are laid out by hand in credits.c -- and the figure sits on the bottom edge, centred.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

#  card slot (vanilla's name, kept by credits.c's windows) -> the daemon, its species folder, and the two sizes
CARDS = [
    ("charizard", "roverbyte", "venusaur", (80, 80), (96, 104)),
    ("venusaur",  "musai",     "eevee",    (80, 80), (96, 80)),
    ("blastoise", "artsai",    "mew",      (80, 80), (80, 96)),
    ("pikachu",   "starr",     "mewtwo",   (80, 80), (96, 96)),
]


def palette(folder):
    rows = [l.split() for l in open(os.path.join(GBA, "graphics/pokemon", folder, "normal.pal")).read().splitlines()[3:19]]
    return [tuple(int(v) for v in r) for r in rows if r]


def card(folder, size):
    pal = palette(folder)
    src = Image.open(os.path.join(GBA, "graphics/pokemon", folder, "front.png"))
    idx = src.load()
    w, h = src.size
    rgba = Image.new("RGBA", (w, h))
    px = rgba.load()
    for y in range(h):
        for x in range(w):
            i = idx[x, y]
            px[x, y] = (0, 0, 0, 0) if i == 0 else pal[i] + (255,)
    box = rgba.getbbox()
    fig = rgba.crop(box)
    scale = min(size[0] / fig.width, size[1] / fig.height)
    fig = fig.resize((max(1, round(fig.width * scale)), max(1, round(fig.height * scale))), Image.LANCZOS)
    out = Image.new("P", size, 0)
    out.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    ox, oy = (size[0] - fig.width) // 2, size[1] - fig.height
    fp, op = fig.load(), out.load()
    for y in range(fig.height):
        for x in range(fig.width):
            r, g, b, a = fp[x, y]
            if a < 128:
                continue
            op[ox + x, oy + y] = min(range(1, len(pal)), key=lambda i: (pal[i][0] - r) ** 2 + (pal[i][1] - g) ** 2 + (pal[i][2] - b) ** 2)
    return out


def main():
    previews = []
    for slot, name, folder, s1, s2 in CARDS:
        a, b = card(folder, s1), card(folder, s2)
        previews += [a, b]
        print("  %-9s card: %-9s (%s)  %dx%d and %dx%d" % (slot, name.upper(), folder, s1[0], s1[1], s2[0], s2[1]))
        if WRITE:
            a.save(os.path.join(GBA, "graphics/credits", name + "_1.png"), bits=4)
            b.save(os.path.join(GBA, "graphics/credits", name + "_2.png"), bits=4)
    if not WRITE:
        print("  report only; pass --write")
    return previews


if __name__ == "__main__":
    main()

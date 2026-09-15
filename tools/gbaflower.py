#!/usr/bin/env python3
"""Our own town flower (T-97; vision.md 9.22).

    python3 tools/gbaflower.py            # preview to /tmp/flower.png (vanilla's five frames | ours, on the lawn)
    python3 tools/gbaflower.py --write    # the five animation frames and the four static General tiles

Vanilla's flower -- two round red blooms on a bed of leaves, swaying -- is one
16x16 animation of five frames that src/tileset_anims.c copies over General tiles
508..511 on every map with the General tileset. Blanche draws its own white one
(pallet_town/anim/flower) and is not touched.

OURS IS A DIFFERENT PLANT, NOT A RECOLOUR: two tulips, cupped heads on straight
stems, with long pointed leaves -- a silhouette nobody reads as vanilla's. It
stays in General row 0's own reds and greens (indices 9 peach, 10 coral, 11 red;
2, 3, 4, 13, 14, 15 greens), because row 0 is every lawn in the game and has no
other flower colour to give; no new hue is added for decoration (9.4). The heads
sway a pixel either way across the five frames, as vanilla's did, and the static
tiles hold frame 0 so the tileset reads right before the animation first runs.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
ANIM = os.path.join(PD, "anim/flower")
PREVIEW = "/tmp/flower.png"
WRITE = "--write" in sys.argv
TILES = (508, 509, 510, 511)
SWAY = (0, 1, 0, -1, 0)                 # the heads' x offset in each of the five frames

# a tulip head, 5 wide: R red, C coral, P peach
HEAD = [
    "R.R.R",
    "RCRCR",
    "RCPCR",
    "RCCCR",
    ".RRR.",
]


def frame(sway):
    px = [[0] * 16 for _ in range(16)]

    def put(x, y, v):
        if 0 <= x < 16 and 0 <= y < 16:
            px[y][x] = v

    # leaves first: long, pointed, from the ground; dark edge (4), body (14, 15), light vein (13)
    for (x0, lean) in ((1, 1), (7, -1), (9, 1), (14, -1)):
        for k in range(7):
            y = 15 - k
            x = x0 + (lean * k) // 3
            put(x, y, 15 if k < 5 else 14); put(x + 1, y, 13 if k < 3 else 14)
            put(x - 1, y, 4) if k < 4 else None
    # two tulips: stems (3), heads that sway; the right one a little lower
    for (cx, top, lean) in ((4, 2, 0), (11, 4, 1)):
        sx = sway * (1 if lean == 0 else 1)
        for y in range(top + 5, 15):
            off = sx if y < top + 8 else 0
            put(cx + off, y, 3)
        for dy, row in enumerate(HEAD):
            for dx, ch in enumerate(row):
                if ch != ".":
                    put(cx - 2 + dx + sx, top + dy, {"R": 11, "C": 10, "P": 9}[ch])
        put(cx + 1 + sx, top + 5, 4)                    # the shade under the cup
    return px


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    pal = read_pal(os.path.join(PD, "palettes/00.pal"))
    frames = [frame(s) for s in SWAY]
    lawn = pal[13]
    sheet = Image.new("RGB", (5 * 20, 40), (40, 40, 40))
    for row, src in enumerate(("vanilla", "ours")):
        for i in range(5):
            if src == "vanilla":
                im = Image.open(os.path.join(ANIM, "%d.png" % i)); p = im.load()
                get = lambda x, y: p[x, y]
            else:
                get = lambda x, y, f=frames[i]: f[y][x]
            for y in range(16):
                for x in range(16):
                    v = get(x, y)
                    sheet.putpixel((i * 20 + x, row * 20 + y), pal[v] if v else lawn)
    sheet.resize((sheet.width * 8, sheet.height * 8), Image.NEAREST).save(PREVIEW)
    print("  preview %s (top: vanilla's five frames; bottom: ours)" % PREVIEW)
    if WRITE:
        template = Image.open(os.path.join(ANIM, "0.png"))
        for i, f in enumerate(frames):
            im = template.copy(); p = im.load()
            for y in range(16):
                for x in range(16):
                    p[x, y] = f[y][x]
            im.save(os.path.join(ANIM, "%d.png" % i))
        path = os.path.join(PD, "tiles.png"); tiles = Image.open(path); tp = tiles.load()
        for q, t in enumerate(TILES):
            for y in range(8):
                for x in range(8):
                    tp[(t % 16) * 8 + x, (t // 16) * 8 + y] = frames[0][(q // 2) * 8 + y][(q % 2) * 8 + x]
        tiles.save(path)
        print("  written: %s/0..4.png and General tiles %s" % (os.path.relpath(ANIM, GBA), TILES))


if __name__ == "__main__":
    main()

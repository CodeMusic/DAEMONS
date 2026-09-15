#!/usr/bin/env python3
"""The ordinary signpost's face, without vanilla's red lettering (T-86; vision.md 9.22).

    python3 tools/gbasignface.py            # preview to /tmp/signface.png (vanilla | ours, in row 2)
    python3 tools/gbasignface.py --write    # the four General tiles, in place

General block 2 is the signpost every outdoor map stands up -- Slate's city sign on
its fence, the police notice, every route marker -- and its face (General tiles
304, 305, 320, 321, in row 2) carried vanilla's red squiggle, which reads as the
letters of a word nobody in this world writes. The face is redrawn once, in place,
so every signpost changes together: the board, its frame and its legs stay; the
red goes, and two lines of dark grey writing take its place, which says "a sign"
without saying anything.

Blanche's two copies of the block draw the same tiles and change with it. The
Building tileset (every interior) has its own tiles 304..321 and is not touched.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD = os.path.join(ROOT, "engineGba", "data/tilesets/primary/general")
PREVIEW = "/tmp/signface.png"
WRITE = "--write" in sys.argv
TILES = (304, 305, 320, 321)          # top-left, top-right, bottom-left, bottom-right

# row 2 indices, as vanilla's face has them except rows 5..8, where the red letters were
FACE = [
    "3377773333777733",
    "7774477777744777",
    "7111111111111117",
    "7111111111111117",
    "7333333333333337",
    "7366666366666337",
    "7333333333333337",
    "7366636666663337",
    "7333333333333337",
    "7333333333333337",
    "7554445555544457",
    "7333333333333337",
    "7777777777777777",
    "5574755555574755",
    "5577755555577755",
    "5555555555555555",
]


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    assert len(FACE) == 16 and all(len(r) == 16 for r in FACE)
    path = os.path.join(PD, "tiles.png")
    img = Image.open(path); p = img.load()
    new = img.copy(); n = new.load()
    for q, t in enumerate(TILES):
        for y in range(8):
            for x in range(8):
                n[(t % 16) * 8 + x, (t // 16) * 8 + y] = int(FACE[(q // 2) * 8 + y][(q % 2) * 8 + x], 16)
    pal = read_pal(os.path.join(PD, "palettes/02.pal"))
    sheet = Image.new("RGB", (40, 16), (120, 180, 110))
    for side, src in enumerate((p, n)):
        for q, t in enumerate(TILES):
            for y in range(8):
                for x in range(8):
                    v = src[(t % 16) * 8 + x, (t // 16) * 8 + y]
                    if v:
                        sheet.putpixel((side * 22 + (q % 2) * 8 + x, (q // 2) * 8 + y), pal[v])
    sheet.resize((sheet.width * 8, sheet.height * 8), Image.NEAREST).save(PREVIEW)
    print("  preview %s (vanilla | ours)" % PREVIEW)
    if WRITE:
        new.save(path)
        print("  written: General tiles %s" % (TILES,))


if __name__ == "__main__":
    main()

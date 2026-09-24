#!/usr/bin/env python3
"""HALFTONE Tower's stones are TOMBSTONES, in the database sense (T-249, 2026-09-24).

    python3 tools/gbatombstones.py            # report
    python3 tools/gbatombstones.py --write     # engineGba/data/tilesets/secondary/pokemon_tower/tiles.png

THE DECISION (the user's, 2026-09-23). The tower keeps its stones and they stay TOMBSTONES -- the marker a database
keeps for a deleted record, so that every copy learns it was deleted. Half the town reads a grave, half a deletion
record, which is 4.5's split in one object. But the sprite must not look like vanilla's gravestone: it becomes an
ENCASED SCREEN, green marks on black, in a housing still shaped like a headstone.

WHAT IS REDRAWN. The stone is one 16x16 drawing in three places: tiles 39/40/55/56 (the stone standing on the top
layer) and two floor-layer copies, 108/109/124/125 and 110/111/126/127, which differ only in the floor around them.
The outline, the rounded top and the plinth are kept -- that is what still reads as a headstone -- and the face
inside the housing, columns 4-11 of rows 3-11, becomes a screen: a dark field with three lines of marks and a bezel
under it.

BY SLOT, NOT BY COLOUR. The purple stones draw with palette 7 and the gold ones with palette 8, and both keep the
dark slate in slot 1 and a green in slot 8, so one drawing gives a purple housing and a gold one, each with a green
screen. The tower is grey (8.6a), so the marks have to read by VALUE: slot 1 is luminance ~86 and slot 8 ~155 in
both palettes.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TILES = os.path.join(ROOT, "engineGba/data/tilesets/secondary/pokemon_tower/tiles.png")
WRITE = "--write" in sys.argv
STONES = [(39, 40, 55, 56), (108, 109, 124, 125), (110, 111, 126, 127)]

#  columns 4..11 of rows 3..11; '.' is the dark screen (slot 1), '8' a mark, the rest the housing's own slots
FACE = [
    "a......a",
    "a.88.8.a",
    "a......a",
    "f.8.88.c",
    "b......a",
    "b.888..a",
    "b......a",
    "baaaaaaa",
    "bbbbbbba",
]
SLOT = {".": 1, "8": 8, "a": 10, "b": 11, "c": 12, "f": 15}


def at(px, tiles, x, y):
    t = tiles[(y // 8) * 2 + (x // 8)]
    return (t % 16) * 8 + x % 8, (t // 16) * 8 + y % 8


def main():
    img = Image.open(TILES)
    px = img.load()
    changed = 0
    for tiles in STONES:
        for r, row in enumerate(FACE):
            for c, ch in enumerate(row):
                xy = at(px, tiles, 4 + c, 3 + r)
                if px[xy] != SLOT[ch]:
                    px[xy] = SLOT[ch]
                    changed += 1
    print("  %d stone pixels %s" % (changed, "redrawn" if WRITE and changed else "to redraw" if changed
                                     else "-- the tower's stones are already screens"))
    if WRITE and changed:
        img.save(TILES)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""The storage screen's two painted labels, without vanilla's word (2026-09-23).

    python3 tools/genstoragelabels.py            # report
    python3 tools/genstoragelabels.py --write    # engineGba/graphics/pokemon_storage/menu.png

The DAEMON storage screen is ours in every line of text and still said PKMN DATA over the daemon's panel and
PARTY POKeMON on the button that shows the party -- because both are PAINTED into the tile sheet, not printed,
and no text sweep can see a picture. Found walking a new debug game's boxes.

The honest words are already on the sheet: the panel is DATA and the button is PARTY. So nothing is drawn: the
vanilla word is ERASED to its label's own background and what remains is centred in the same tiles. The sheet is
read from upstream every run, so this is a re-run and never an edit of its own output.

  PKMN DATA      rows 4-13, x 14-39 erased, DATA (x 42-65) moved to the middle of the label (x 8-79)
  PARTY POKeMON  rows 18-27, x 96-127 erased, and the N that runs on into the two tiles at (48,48) and (56,48); PARTY
                 (x 70-92) moved to the middle of the button, which is x 68-127 plus that end tile
"""
import io, os, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
REL = "graphics/pokemon_storage/menu.png"
WRITE = "--write" in sys.argv


def move(px, x0, x1, y0, y1, dx, fill):
    band = {(x, y): px[x, y] for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    for (x, y) in band:
        px[x, y] = fill
    for (x, y), v in band.items():
        px[x + dx, y] = v


def main():
    raw = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + REL], check=True, capture_output=True).stdout
    im = Image.open(io.BytesIO(raw)); im.load(); px = im.load()

    # ---- PKMN DATA -> DATA. The label's background is index 2.
    for x in range(14, 40):
        for y in range(4, 14):
            px[x, y] = 2
    width = 65 - 42 + 1
    move(px, 42, 65, 4, 13, (8 + (79 - 8 + 1 - width) // 2) - 42, 2)

    # ---- PARTY POKeMON -> PARTY. Letters are indices 23 and 24 on background 30.
    for x in range(96, 128):
        for y in range(18, 28):
            if px[x, y] in (23, 24):
                px[x, y] = 30
    for x in range(48, 60):         # the N is split across two tiles, (48,48) and (56,48)
        for y in range(48, 56):
            if px[x, y] in (23, 24):
                px[x, y] = 30
    width = 92 - 70 + 1
    button = (127 - 68 + 1) + 7
    move(px, 70, 92, 18, 27, (68 + (button - width) // 2) - 70, 30)

    path = os.path.join(GBA, REL)
    same = list(Image.open(path).getdata()) == list(im.getdata())
    print("  storage labels: %s" % ("unchanged" if same else "written" if WRITE else "would change"))
    if WRITE and not same:
        im.save(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

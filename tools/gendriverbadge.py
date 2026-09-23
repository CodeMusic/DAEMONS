#!/usr/bin/env python3
"""The TOOLKIT's badge on a DRIVER's row says DRV, not HM (T-199; vision.md 2.8).

    python3 tools/gendriverbadge.py            # report
    python3 tools/gendriverbadge.py --write    # engineGba/graphics/tm_case/hm.png

The TOOLKIT prints a small plate before each DRIVER where a PLUGIN prints its count, and vanilla's plate says HM
-- the one vanilla word left on a screen whose every other word is ours (found playing T-199, 2026-09-23). The
plate, its palette and its size are vanilla's, read from upstream; only the letters are redrawn, in the same
three-pixel face: DRV, as HM abbreviated its word.
"""
import io, os, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
REL = "graphics/tm_case/hm.png"
WRITE = "--write" in sys.argv
PLATE, INK = 6, 7
GLYPHS = {"D": ["77.", "7.7", "7.7", "7.7", "7.7", "77."],
          "R": ["77.", "7.7", "7.7", "77.", "7.7", "7.7"],
          "V": ["7.7", "7.7", "7.7", "7.7", "7.7", ".7."]}


def main():
    raw = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + REL], check=True, capture_output=True).stdout
    im = Image.open(io.BytesIO(raw)); px = im.load()
    for y in range(3, 9):
        for x in range(2, 14):
            px[x, y] = PLATE
    for k, ch in enumerate("DRV"):
        for dy, row in enumerate(GLYPHS[ch]):
            for dx, c in enumerate(row):
                if c == "7":
                    px[2 + k * 4 + dx, 3 + dy] = INK
    path = os.path.join(GBA, REL)
    same = list(Image.open(path).getdata()) == list(im.getdata())
    print("  the DRIVER badge: %s" % ("unchanged" if same else "written" if WRITE else "would change"))
    if WRITE and not same:
        im.save(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

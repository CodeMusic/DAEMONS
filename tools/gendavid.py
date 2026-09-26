#!/usr/bin/env python3
"""DAVID, the player's brother, drawn from DAD: the S.S. ANNE's CAPTAIN (T-313, DRAFT art).

    python3 tools/gendavid.py            # report, and a preview in the scratch dir
    python3 tools/gendavid.py --write    # graphics/object_events/pics/people/david.png

The user, 2026-09-26: DAVID looks like DAD, black hair and all -- refined, conservative, fond of boats -- and he
captains the S.S. ANNE. So he is DAD's sheet (the family's animal, drawn from MOM's by gendad.py), in uniform:

  * a white captain's cap over the hair: a white crown, a black brim, a gold badge on the front view;
  * DAD's olive shirt (6) becomes white (14); the gold at its edges (5) stays, now the epaulettes.

Everything else is DAD's, index for index, in the same NPC_WHITE palette, so the two read as father and son.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DAD = os.path.join(GBA, "graphics/object_events/pics/people/dad.png")
DAVID = os.path.join(GBA, "graphics/object_events/pics/people/david.png")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))
WHITE, BLACK, GOLD, SHIRT = 14, 15, 5, 6


def draw():
    dad = Image.open(DAD)
    out = dad.copy()
    px = out.load()
    for f in range(out.width // 16):
        x0 = 16 * f
        row = [x for x in range(x0, x0 + 16) if px[x, 10]]
        l, r = min(row), max(row)
        for x in range(l, r + 1):
            px[x, 9] = BLACK                                   # the brim
        for y in (7, 8):
            for x in range(l, r + 1):
                px[x, y] = BLACK if x in (l, r) else WHITE      # the crown
        for x in range(l + 1, r):
            px[x, 6] = BLACK if x in (l + 1, r - 1) else WHITE
        for x in range(l + 2, r - 1):
            px[x, 5] = BLACK
        if f == 0:                                             # the badge, facing you
            mid = (l + r) // 2
            px[mid, 7] = px[mid + 1, 7] = GOLD
        for y in range(16, 32):
            for x in range(x0, x0 + 16):
                if px[x, y] == SHIRT:
                    px[x, y] = WHITE
    return out


def main():
    david = draw()
    print("  DAVID: %dx%d from DAD's sheet, a cap and a white uniform" % david.size)
    os.makedirs(SCRATCH, exist_ok=True)
    prev = Image.new("RGBA", (david.width * 2 + 8, 32), (40, 40, 40, 255))
    prev.paste(Image.open(DAD).convert("RGBA"), (0, 0))
    prev.paste(david.convert("RGBA"), (david.width + 8, 0))
    prev.resize((prev.width * 5, prev.height * 5), Image.NEAREST).save(os.path.join(SCRATCH, "david_preview.png"))
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % SCRATCH)
        return
    david.save(DAVID, bits=4)
    print("  written")


if __name__ == "__main__":
    main()

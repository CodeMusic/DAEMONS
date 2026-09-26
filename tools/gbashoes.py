#!/usr/bin/env python3
"""The RUNNING SHOES show who gave them (T-256): MOM's make the feet yellow with black trim, DAD's black with red.

    python3 tools/gbashoes.py            # report what would change
    python3 tools/gbashoes.py --write    # the player's sheets and graphics/object_events/palettes/player.pal

WHY IT NEEDED TWO FREE COLOURS. The player's sixteen are shared by every one of their sheets, and the shoes were
index 6 (the near-black soles) and 5 (the dark grey above them), which the figure also uses elsewhere -- recolour
6 and the coat's shadows change with it. But 12 and 13 are used only by the surf, fishing, item and VS SEEKER
sheets, for a tan and a cream that each sit beside a colour the sheet already has (12 by 8, 13 by 9). So:

  1. every player sheet's 12 goes to 8 and 13 to 9 -- by eye the same -- which frees both indices everywhere;
  2. on the sheets where the feet show (walking, running, fishing, holding an item), a SOLE is index 6 at the very
     bottom of its column in the last three rows, and its TRIM is the 5 just above it; soles go to 12, trims to 13;
  3. player.pal's 12 and 13 become the old sole and trim colours, so nothing changes until the shoes are given.

The engine then sets 12 and 13 whenever it loads the player's palette (event_object_movement.c, T-256): the old
colours without shoes, MOM's yellow and black, or DAD's black and red by FLAG_SHOES_FROM_DAD. The fishing line and
the surf sheet's arms are 6 too, and neither is ever the bottom of a column in the last three rows.
"""
import glob, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
PAL = os.path.join(GBA, "graphics/object_events/palettes/player.pal")
WRITE = "--write" in sys.argv
FREE = {12: 8, 13: 9}
SOLE, TRIM = 12, 13
OLD_SOLE, OLD_TRIM = 6, 5
FEET = ("normal", "surf_run", "fish", "item")


def shoe_positions(im):
    """-> {(x, y): SOLE|TRIM}, found whether or not the sheet is masked yet (a sole is 6 or already 12)"""
    px = im.load()
    out = {}
    for x in range(im.width):
        for y in range(im.height - 1, -1, -1):
            v = px[x, y]
            if v in (0, 15):
                continue
            if v in (OLD_SOLE, SOLE) and y >= im.height - 3:
                out[(x, y)] = SOLE
                if y > 0 and px[x, y - 1] in (OLD_TRIM, TRIM):
                    out[(x, y - 1)] = TRIM
            break
    return out


def main():
    total = 0
    for path in sorted(glob.glob(os.path.join(PEOPLE, "red_*.png")) + glob.glob(os.path.join(PEOPLE, "green_*.png"))):
        im = Image.open(path)
        pal = im.getpalette()
        name = os.path.basename(path)[:-4].split("_", 1)[1]
        shoes = shoe_positions(im) if name in FEET else {}
        px = im.load()
        freed = shod = 0
        for y in range(im.height):
            for x in range(im.width):
                v = px[x, y]
                want = shoes.get((x, y), FREE.get(v, v))
                if want != v:
                    px[x, y] = want
                    if (x, y) in shoes:
                        shod += 1
                    else:
                        freed += 1
        if freed or shod:
            print("  %-26s %4d pixels off 12/13, %3d shoe pixels" % (os.path.basename(path), freed, shod))
            total += 1
            if WRITE:
                im.putpalette(pal)
                im.save(path, bits=4)
    lines = open(PAL, newline="").read().split("\r\n" if "\r\n" in open(PAL, newline="").read() else "\n")
    rows = [tuple(int(v) for v in l.split()) for l in lines[3:19]]
    want = list(rows)
    want[SOLE], want[TRIM] = rows[OLD_SOLE], rows[OLD_TRIM]
    if want != rows:
        print("  player.pal: 12 and 13 become the old sole and trim, %s and %s" % (rows[OLD_SOLE], rows[OLD_TRIM]))
        total += 1
        if WRITE:
            nl = "\r\n" if "\r\n" in open(PAL, newline="").read() else "\n"
            out = lines[:3] + ["%d %d %d" % c for c in want] + lines[19:]
            open(PAL, "w", newline="").write(nl.join(out))
    if not total:
        print("  the shoes are masked; nothing to do")
    elif not WRITE:
        print("  report only; pass --write")


if __name__ == "__main__":
    main()

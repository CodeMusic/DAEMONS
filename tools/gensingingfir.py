#!/usr/bin/env python3
"""The singing fir on the S.S. ANNE's pier (T-10, DRAFT art).

    python3 tools/gensingingfir.py            # report, and a preview in the scratch dir
    python3 tools/gensingingfir.py --write    # graphics/object_events/pics/misc/singing_fir.png

The user, 2026-09-26/27: the grove's tree sings O CHRISTMAS TREE, and it "should subtly look like a Christmas tree";
it stands in ARDOR by the S.S. ANNE, where the old legend put something under the truck. So: a fir, three tiers,
with a star and a handful of baubles in the source painting's own note colours (yellow, purple, orange). Subtly --
six baubles, not tinsel.

One 16x32 frame in NPC_GREEN's sixteen colours, so it spends no palette of its own: greens for the needles, the
brown for the trunk, the yellows for the star, pink and purple and the skin orange for the baubles.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_green.pal")
OUT = os.path.join(GBA, "graphics/object_events/pics/misc/singing_fir.png")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

LIGHT, MID, DARK, TRUNK, STAR, STAR_DARK, PURPLE, ORANGE = 8, 9, 10, 4, 5, 6, 12, 3
TIERS = [(3, 10, 1, 4), (8, 18, 2, 6), (15, 27, 3, 7)]      # (top row, bottom row, half-width at top, at bottom)
BAUBLES = [(8, 7, STAR), (6, 12, PURPLE), (10, 15, ORANGE), (5, 21, STAR), (9, 24, PURPLE), (11, 20, ORANGE)]


def jasc(path):
    lines = open(path, newline="").read().replace("\r\n", "\n").split("\n")
    return [tuple(int(v) for v in l.split()) for l in lines[3:19]]


def draw():
    im = Image.new("P", (16, 32), 0)
    im.putpalette([v for c in jasc(PAL) for v in c] + [0] * (768 - 48))
    px = im.load()
    cx = 7.5
    for top, bottom, w0, w1 in reversed(TIERS):              # the upper tiers overlap the lower
        for y in range(top, bottom + 1):
            w = w0 + (w1 - w0) * (y - top) / max(1, bottom - top)
            l, r = int(round(cx - w)), int(round(cx + w))
            for x in range(max(0, l), min(15, r) + 1):
                edge = x in (l, r) or y == bottom
                px[x, y] = DARK if edge else (LIGHT if x < cx - w / 3 else MID)
    for y in range(28, 32):                                   # the trunk
        for x in (7, 8):
            px[x, y] = TRUNK
    for x, y in ((7, 1), (8, 1), (7, 2), (8, 2), (6, 2), (9, 2), (7, 0), (8, 3)):   # the star
        px[x, y] = STAR
    px[7, 3] = STAR_DARK
    for x, y, c in BAUBLES:
        px[x, y] = c
    return im


def main():
    fir = draw()
    print("  the singing fir: 16x32, NPC_GREEN, %d baubles" % len(BAUBLES))
    os.makedirs(SCRATCH, exist_ok=True)
    fir.convert("RGBA").resize((16 * 8, 32 * 8), Image.NEAREST).save(os.path.join(SCRATCH, "singing_fir_preview.png"))
    old = Image.open(OUT) if os.path.exists(OUT) else None
    if old is not None and list(old.getdata()) == list(fir.getdata()):
        print("  singing_fir.png is current")
        return
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % SCRATCH)
        return
    fir.save(OUT, bits=4)
    print("  written")


if __name__ == "__main__":
    main()

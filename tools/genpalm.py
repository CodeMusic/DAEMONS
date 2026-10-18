#!/usr/bin/env python3
"""The palm on FINDERS BEACH (T-417 P3, DRAFT art) -- and on ROUTE 2 and BREATHVERSE (2026-10-18).

    python3 tools/genpalm.py            # report, and a preview in the scratch dir
    python3 tools/genpalm.py --write    # graphics/object_events/pics/misc/beach_palm.png

The user, 2026-10-17 (docs/private/draft-play-2026-10-17.md 2): the FLUTE lies under a palm on FINDERS BEACH
(OneIsland_TreasureBeach), on the sand's northern point at (9,19); the user, 2026-10-18, moved the FLUTE to BREATHVERSE (tools/gbabreathverse.py), whose way in and way out
are this palm too, and left FINDERS BEACH's as scenery. FRLG has no palm in any tileset, so the palm is an
object, drawn like the singing fir: inanimate, in NPC_GREEN's sixteen colours so it spends no palette of its own
(PALSLOT_NPC_3, the tag's own slot -- engine.md trap 17).

One 32x32 frame: a trunk leaning a little east as it rises, banded where the old fronds fell, and a crown of eight
fronds drooping from the top, three coconuts under them. Drawn by hand in Python after spriteforge's 512x512 draft
(seed 4171: a palm on a sand island), whose lean, banding and drooping fronds it follows.
"""
import math, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_green.pal")
OUT = os.path.join(GBA, "graphics/object_events/pics/misc/beach_palm.png")
RULES = os.path.join(GBA, "spritesheet_rules.mk")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

# npc_green: 8 light green  9 green  10 dark green  4 dark red-brown  6 olive gold  7 dark olive  3 tan
LIGHT, MID, DARK, BARK, BARK_LIGHT, BARK_DARK, TAN = 8, 9, 10, 4, 6, 7, 3
CROWN = (17.5, 9.0)
#  (angle in degrees from east, counter-clockwise; length in pixels; how far it droops at the tip)
FRONDS = [(172, 14, 7), (140, 12, 6), (108, 9, 4), (75, 9, 4), (40, 12, 6), (8, 14, 7), (205, 9, 3), (-25, 9, 3)]
NUTS = [(16, 11), (19, 11), (17, 12)]


def jasc(path):
    lines = open(path, newline="").read().replace("\r\n", "\n").split("\n")
    return [tuple(int(v) for v in l.split()) for l in lines[3:19]]


def draw():
    W = H = 32
    g = [[0] * W for _ in range(H)]

    def put(x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < W and 0 <= y < H:
            g[y][x] = c

    # the trunk: from the sand at the bottom middle up to the crown, leaning east
    for y in range(31, int(CROWN[1]) + 1, -1):
        t = (31 - y) / (31 - CROWN[1])
        cx = 15.5 + 2.0 * t * t
        half = 1.6 - 0.6 * t
        l, r = int(round(cx - half)), int(round(cx + half))
        band = (y % 3 == 0)
        for x in range(l, r + 1):
            put(x, y, BARK_DARK if band else (BARK_LIGHT if x < cx else BARK))
        put(l - 1, y, BARK_DARK)
        put(r + 1, y, BARK_DARK)

    # the fronds: a spine drooping toward its tip, leaflets either side shading light above and dark below
    for ang, length, droop in FRONDS:
        a = math.radians(ang)
        steps = length * 4
        for k in range(steps + 1):
            s = k / steps
            x = CROWN[0] + s * length * math.cos(a)
            y = CROWN[1] - s * length * math.sin(a) + droop * s * s
            w = 2.2 * (1 - s) + 0.6
            for d in range(-3, 4):
                if abs(d) > w:
                    continue
                c = LIGHT if d < 0 else (MID if d == 0 else DARK)
                put(x, y + d * 0.6, c if abs(d) < w - 0.5 else DARK)

    # three coconuts in the shade of the crown
    for x, y in NUTS:
        put(x, y, BARK)
    put(16, 11, TAN)

    # an outline: every empty pixel beside the frond ink, in the darkest green, under the crown only
    ink = [[g[y][x] for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            if ink[y][x] == 0 and y < 22:
                near = [ink[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                        if 0 <= x + dx < W and 0 <= y + dy < H]
                if any(c in (LIGHT, MID) for c in near):
                    g[y][x] = DARK

    im = Image.new("P", (W, H), 0)
    im.putpalette([v for c in jasc(PAL) for v in c] + [0] * (768 - 48))
    px = im.load()
    for y in range(H):
        for x in range(W):
            px[x, y] = g[y][x]
    return im


def ensure_rule():
    target = "$(OBJEVENTGFXDIR)/misc/beach_palm.4bpp"
    s = open(RULES).read()
    if target + ":" in s:
        return False
    open(RULES, "w").write(s.rstrip("\n") + "\n\n%s: %%.4bpp: %%.png\n\t$(GFX) $< $@ -mwidth 4 -mheight 4\n" % target)
    return True


def main():
    im = draw()
    print("  the palm: one 32x32 frame, NPC_GREEN, %d fronds, %d coconuts" % (len(FRONDS), len(NUTS)))
    os.makedirs(SCRATCH, exist_ok=True)
    bg = Image.new("RGBA", im.size, (232, 216, 160, 255))
    pal = jasc(PAL)
    rgba = Image.new("RGBA", im.size)
    rgba.putdata([pal[i] + ((255,) if i else (0,)) for i in im.getdata()])
    bg.alpha_composite(rgba)
    bg.resize((32 * 10, 32 * 10), Image.NEAREST).save(os.path.join(SCRATCH, "palm_preview.png"))
    old = Image.open(OUT) if os.path.exists(OUT) else None
    rule = os.path.exists(RULES) and "beach_palm.4bpp:" in open(RULES).read()
    if old is not None and list(old.getdata()) == list(im.getdata()) and rule:
        print("  beach_palm.png is current")
        return
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % SCRATCH)
        return
    im.save(OUT, bits=4)
    ensure_rule()
    print("  written")


if __name__ == "__main__":
    main()

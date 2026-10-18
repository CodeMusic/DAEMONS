#!/usr/bin/env python3
"""CONTEXT's FLUTE, lying on BREATHVERSE's sand beside the palm (T-417, the user 2026-10-18; DRAFT art).

    python3 tools/genflute.py            # report, and a preview in the scratch dir
    python3 tools/genflute.py --write    # graphics/object_events/pics/misc/breath_flute.png

The user, 2026-10-18: the FLUTE moves from FINDERS BEACH to BREATHVERSE, a small islet reached through a palm on
ROUTE 2, and lies beside the islet's palm "drawn as its own sprite", picked up there. One 16x16 inanimate frame, drawn
by hand in Python as tools/genpalm.py drew the palm: a bamboo flute lying level on the sand -- a cane body
in the palm's own gold and olive, a node ring near each end, four finger holes and the mouth hole, a dark olive
outline, a highlight along its top. In NPC_GREEN's sixteen colours (the palm's), so it spends no palette of its own
(PALSLOT_NPC_3, the tag's own slot -- engine.md trap 17).
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_green.pal")
OUT = os.path.join(GBA, "graphics/object_events/pics/misc/breath_flute.png")
RULES = os.path.join(GBA, "spritesheet_rules.mk")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

# npc_green: 1 pale  5 gold  6 olive gold  7 dark olive  4 dark red-brown
PALE, GOLD, OLIVE, INK, HOLE = 1, 5, 6, 7, 4
#  the flute lies level (a slope stair-steps at this size and reads as a broken stick), its axis a row above the foot
X0, X1 = 1, 14
NODES = (2, 12)                                          # the node rings, as x along the body
HOLES = (4, 6, 8, 10)                                    # finger holes, a pixel of cane between each
MOUTH = 13


def jasc(path):
    lines = open(path, newline="").read().replace("\r\n", "\n").split("\n")
    return [tuple(int(v) for v in l.split()) for l in lines[3:19]]


def draw():
    W = H = 16
    g = [[0] * W for _ in range(H)]
    centre = lambda x: 10.0                                # the axis's y at x

    for x in range(X0, X1 + 1):
        cy = centre(x)
        top = int(round(cy - 1.0))
        for y, c in ((top, PALE), (top + 1, GOLD), (top + 2, OLIVE)):
            g[y][x] = c
    for x in NODES:                                      # a node: a darker ring across the cane
        top = int(round(centre(x) - 1.0))
        g[top][x], g[top + 1][x], g[top + 2][x] = OLIVE, OLIVE, INK
    for hx in HOLES + (MOUTH,):
        x = int(round(hx))
        g[int(round(centre(x) - 1.0)) + 1][x] = HOLE
    # an outline round the cane, in the darkest olive
    ink = [row[:] for row in g]
    for y in range(H):
        for x in range(W):
            if ink[y][x] == 0 and any(0 <= x + dx < W and 0 <= y + dy < H and ink[y + dy][x + dx]
                                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g[y][x] = INK

    im = Image.new("P", (W, H), 0)
    im.putpalette([v for c in jasc(PAL) for v in c] + [0] * (768 - 48))
    px = im.load()
    for y in range(H):
        for x in range(W):
            px[x, y] = g[y][x]
    return im


def ensure_rule():
    target = "$(OBJEVENTGFXDIR)/misc/breath_flute.4bpp"
    s = open(RULES).read()
    if target + ":" in s:
        return False
    open(RULES, "w").write(s.rstrip("\n") + "\n\n%s: %%.4bpp: %%.png\n\t$(GFX) $< $@ -mwidth 2 -mheight 2\n" % target)
    return True


def main():
    im = draw()
    print("  the FLUTE: one 16x16 frame, NPC_GREEN, %d holes and the mouth, %d nodes" % (len(HOLES), len(NODES)))
    os.makedirs(SCRATCH, exist_ok=True)
    bg = Image.new("RGBA", im.size, (232, 216, 160, 255))
    pal = jasc(PAL)
    rgba = Image.new("RGBA", im.size)
    rgba.putdata([pal[i] + ((255,) if i else (0,)) for i in im.getdata()])
    bg.alpha_composite(rgba)
    bg.resize((16 * 16, 16 * 16), Image.NEAREST).save(os.path.join(SCRATCH, "flute_preview.png"))
    old = Image.open(OUT) if os.path.exists(OUT) else None
    rule = os.path.exists(RULES) and "breath_flute.4bpp:" in open(RULES).read()
    if old is not None and list(old.getdata()) == list(im.getdata()) and rule:
        print("  breath_flute.png is current")
        return
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % SCRATCH)
        return
    im.save(OUT, bits=4)
    ensure_rule()
    print("  written")


if __name__ == "__main__":
    main()

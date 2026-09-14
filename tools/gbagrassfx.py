#!/usr/bin/env python3
"""The grass that flicks up under your feet in Blanche's tall grass is pale too (vision.md 9.22).

    python3 tools/gbagrassfx.py            # preview to /tmp/blanche_grass_fx.png
    python3 tools/gbagrassfx.py --write    # graphics/field_effects/palettes/blanche_grass.pal

Walking through tall grass spawns a field-effect sprite -- the blades parting
round your feet, and the tufts when you land from a ledge. Its colours come from
general_1.pal, which every map shares, so on Route 1's pale tall grass it was
still vanilla's deep green.

This writes a copy of general_1.pal with only its grass greens moved onto
Blanche's eight ground colours (gbaground.py), each green to the job it does in
the sprite: the bright leaf tips, the body, the shade and the dark base. The
water blues and everything else stay, so the copy is a drop-in for the same
sprite sheet. field_effect_helpers.c loads it under its own tag when the grass
cell underfoot is drawn in Blanche's ground row.
"""
import importlib.util, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbaground", os.path.join(ROOT, "tools", "gbaground.py"))
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

GBA = os.path.join(ROOT, "engineGba")
SRC = os.path.join(GBA, "graphics/field_effects/palettes/general_1.pal")
OUT = os.path.join(GBA, "graphics/field_effects/palettes/blanche_grass.pal")
SHEETS = ["graphics/field_effects/pics/tall_grass.png", "graphics/field_effects/pics/jump_tall_grass.png"]
PREVIEW = "/tmp/blanche_grass_fx.png"
WRITE = "--write" in sys.argv

C = {n: G.GROUND_COLOURS[n - 1] for n in range(1, 9)}          # GRASS, TIP, TUFT, DARK, CHALK, SPECK, SHADE, EDGE
# Each index takes the colour its job has in Blanche's tall grass TILE
# (gbapalegrass.py), so the parted grass is the grass it parts. An earlier pass
# darkened the body to stand out, and it sat on the pale field as a dark band;
# what stands out now is only what should -- the thrown leaves, near white.
MOVE = {1: C[G.SPECK], 2: C[G.TIP], 3: C[G.GRASS], 4: C[G.DARK], 5: C[G.DARK],
        12: C[G.TIP], 13: C[G.GRASS], 14: C[G.TUFT], 15: C[G.DARK]}


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    src = read_pal(SRC)
    pale = [MOVE.get(i, c) for i, c in enumerate(src)]
    sheet = Image.new("RGB", (16 * 4 + 12, 80), (40, 40, 40))
    x0 = 0
    for rel in SHEETS:
        im = Image.open(os.path.join(GBA, rel)); px = im.load()
        for pal in (src, pale):
            for y in range(im.height):
                for x in range(im.width):
                    v = px[x, y]
                    sheet.putpixel((x0 + x, y), pal[v] if v else G.GROUND_COLOURS[0])
            x0 += im.width + 4
    sheet.resize((sheet.width * 6, sheet.height * 6), Image.NEAREST).save(PREVIEW)
    print("  preview %s (tall grass vanilla | pale, then the landing tufts)" % PREVIEW)
    if WRITE:
        lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in pale]
        open(OUT, "wb").write(("\r\n".join(lines) + "\r\n").encode())
        print("  written: %s" % OUT)


main()

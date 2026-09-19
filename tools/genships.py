#!/usr/bin/env python3
"""The three large overworld objects still drawn as vanilla's (T-167, batch B; vision.md 9.4).

    python3 tools/genships.py            # preview to /tmp/ships_ow.png (ours above, vanilla's below)
    python3 tools/genships.py --write    # the three sheets, and the two ships' palettes, in place

genmisc.py drew batch A as letter grids; these are 64 and 128 pixels wide, so they are drawn here from shapes
instead -- still EVERY PIXEL AUTHORED, vanilla used only as measurement (size, frame count, which way the bow
points, where the hull sits in the frame), never traced.

    birth_island_stone.png   32x32   the ANNEX's stone   a faceted shard, standing where she stood
    seagallop.png            64x64   SEAGALLOP HI-SPEED  a hydrofoil: a white hull lifted clear on two foils
    ss_anne.png             128x64   the S.S. ANNE       an ocean liner, navy-hulled, one great funnel

THE STONE MAY USE ONLY INDICES 1-3. `SetDeoxysTrianglePalette` loads one of eleven deoxys_rock_N palettes over
the first four colours every time the player returns to the field, and the puzzle's progress IS that recolour
(grey to red, dark to light in every one of them) -- so 1 is the outline and shade, 2 the body, 3 the lit
facet, and its .pal is left alone because the game never shows it.

THE SHIPS OWN THEIR PALETTES. Both sit in PALSLOT_NPC_SPECIAL under a tag of their own, so these colours are
chosen, not borrowed, and written to their .pal here (the .gbapal is generated). Both are one frame, bow to the
LEFT as vanilla's are: sAnimTable_Standard mirrors a west frame for east, and the cutscenes move them assuming it.
ss_anne keeps its conversion rule (-mwidth 8 -mheight 4); the Seagallop's 64x64 needs none.
"""
import os, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import GBA

PREVIEW = "/tmp/ships_ow.png"
WRITE = "--write" in sys.argv
MISC = os.path.join(GBA, "graphics/object_events/pics/misc")
PALS = os.path.join(GBA, "graphics/object_events/palettes")


def canvas(w, h):
    img = Image.new("P", (w, h), 0)
    return img, ImageDraw.Draw(img)


def outline(img, ink, skip=()):
    """ink every empty pixel that touches the silhouette (4-neighbour), except against indices in skip"""
    px, (w, h) = img.load(), img.size
    hits = []
    for y in range(h):
        for x in range(w):
            if px[x, y]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and px[nx, ny] and px[nx, ny] not in skip and px[nx, ny] != ink:
                    hits.append((x, y)); break
    for p in hits:
        px[p] = ink


# ================================================================ the ANNEX's stone
# 1 outline and shadow facet   2 body   3 lit facet   (the puzzle recolours exactly these)

def stone():
    img, d = canvas(32, 32)
    # a shard leaning a little to the right: five corners, apex off-centre
    body = [(13, 11), (18, 13), (22, 29), (16, 30), (10, 29), (11, 18)]
    d.polygon(body, fill=2)
    d.polygon([(13, 11), (18, 13), (16, 30), (14, 22)], fill=3)          # the lit face, towards the light
    d.polygon([(18, 13), (22, 29), (16, 30)], fill=1)                    # the face turned away
    d.line([(13, 12), (14, 22)], fill=3)                                 # a glint down the near edge
    d.line([(12, 24), (14, 27)], fill=1)                                 # one old crack in the body
    outline(img, 1)
    return img


# ================================================================ SEAGALLOP HI-SPEED
SEA_PAL = [
    (65, 123, 180),    # 0  transparent (the sea's own blue, so a stray edge reads as water)
    (24, 32, 56),      # 1  outline
    (248, 248, 248),   # 2  hull white
    (208, 216, 232),   # 3  hull shade
    (144, 156, 184),   # 4  underside
    (40, 168, 160),    # 5  teal livery
    (24, 104, 112),    # 6  teal, dark
    (40, 56, 88),      # 7  window
    (136, 200, 232),   # 8  glass light
    (232, 176, 56),    # 9  amber lamp
    (88, 96, 112),     # 10 foil steel
    (200, 232, 248),   # 11 spray
    (40, 88, 150),     # 12 water shadow
    (120, 128, 148),   # 13 steel light
    (255, 255, 255),   # 14 white spark
    (16, 16, 24),      # 15 black
]


def seagallop():
    img, d = canvas(64, 64)
    # the shadow the hull throws on the water, under the foils
    d.rectangle([10, 59, 56, 60], fill=12)
    # foils: two struts down into the water, a blade on each, spray where the blades cut
    for sx in (13, 48):
        d.rectangle([sx, 49, sx + 1, 56], fill=10)
        d.line([(sx - 5, 57), (sx + 6, 57)], fill=10)
        d.line([(sx - 4, 56), (sx + 5, 56)], fill=13)
        d.point([(sx - 6, 58), (sx - 7, 57), (sx + 7, 58), (sx - 5, 59)], fill=11)
    # hull: a long wedge, the bow a sharp point at the left
    d.polygon([(2, 44), (10, 38), (60, 38), (61, 44), (59, 49), (9, 49)], fill=2)
    d.rectangle([9, 47, 59, 49], fill=4)                                  # the underside in shade
    d.line([(4, 44), (60, 44)], fill=5)                                   # the livery: a teal line bow to stern,
    d.line([(6, 45), (60, 45)], fill=6)                                   # thickening aft like a wake
    d.polygon([(40, 43), (60, 41), (60, 46), (44, 46)], fill=5)
    d.line([(44, 46), (60, 46)], fill=6)
    # the cabin: rounded at the front, a band of dark glass wrapping it
    d.polygon([(16, 37), (20, 29), (54, 29), (56, 37)], fill=3)
    d.rectangle([22, 28, 53, 29], fill=2)
    d.polygon([(18, 35), (21, 31), (54, 31), (55, 35)], fill=7)
    for wx in range(26, 54, 5):                                           # mullions between the panes
        d.line([(wx, 31), (wx, 35)], fill=3)
    d.line([(21, 32), (24, 32)], fill=8)                                  # light on the forward glass
    d.point([(19, 34), (20, 33)], fill=8)
    # the wheelhouse on the roof, a mast and its lamp
    d.rectangle([24, 25, 36, 28], fill=2)
    d.rectangle([26, 26, 34, 27], fill=7)
    d.line([(28, 26), (30, 26)], fill=8)
    d.rectangle([44, 19, 44, 28], fill=10)
    d.line([(41, 21), (47, 21)], fill=10)
    d.point((44, 18), fill=9)
    # a row of portholes along the hull, and a bow lamp
    for px_ in range(14, 58, 4):
        d.point((px_, 41), fill=7)
    d.point((5, 43), fill=9)
    outline(img, 1, skip=(12, 11))
    return img


# ================================================================ the S.S. ANNE
ANNE_PAL = [
    (57, 115, 180),    # 0  transparent
    (16, 16, 40),      # 1  outline
    (40, 56, 104),     # 2  hull navy
    (72, 96, 152),     # 3  hull navy, lit
    (176, 48, 40),     # 4  boot-top red
    (248, 248, 240),   # 5  superstructure white
    (208, 212, 224),   # 6  white in shade
    (152, 160, 184),   # 7  grey
    (32, 40, 64),      # 8  window
    (200, 160, 104),   # 9  deck planking
    (152, 112, 72),    # 10 planking, dark
    (232, 168, 48),    # 11 funnel amber
    (176, 112, 32),    # 12 amber, dark
    (40, 88, 152),     # 13 water shadow
    (136, 200, 232),   # 14 porthole light
    (8, 8, 16),        # 15 black
]


def ss_anne():
    img, d = canvas(128, 64)
    d.rectangle([12, 58, 118, 60], fill=13)                               # her shadow on the water
    # hull: a raked bow at the left, a rounded counter stern at the right
    d.polygon([(2, 40), (123, 40), (125, 44), (122, 52), (118, 57), (14, 57), (6, 48)], fill=2)
    d.polygon([(4, 41), (123, 41), (124, 43), (5, 43)], fill=3)           # light along the sheer
    d.polygon([(10, 53), (121, 53), (118, 57), (14, 57)], fill=4)         # the red below the waterline
    for px_ in range(18, 118, 5):                                         # two rows of portholes
        d.point((px_, 46), fill=14)
    for px_ in range(20, 116, 5):
        d.point((px_, 49), fill=14)
    # the deck, seen from a little above: planking from bow to stern
    d.polygon([(6, 37), (121, 37), (123, 40), (2, 40)], fill=9)
    for px_ in range(10, 120, 6):
        d.point((px_, 38), fill=10)
        d.point((px_ + 3, 39), fill=10)
    # superstructure: three tiers set back from the bow, the bridge forward on the second
    d.rectangle([30, 28, 110, 36], fill=5)
    d.rectangle([30, 35, 110, 36], fill=6)
    for wx in range(34, 108, 4):
        d.rectangle([wx, 31, wx + 1, 32], fill=8)
    d.rectangle([40, 20, 100, 27], fill=5)
    d.rectangle([40, 26, 100, 27], fill=6)
    d.rectangle([42, 22, 52, 24], fill=8)                                 # the bridge windows, wide
    d.line([(43, 22), (45, 22)], fill=14)
    for wx in range(56, 98, 4):
        d.rectangle([wx, 22, wx + 1, 23], fill=8)
    d.rectangle([54, 14, 92, 19], fill=6)
    d.rectangle([54, 14, 92, 15], fill=5)
    for wx in range(58, 90, 6):
        d.point((wx, 17), fill=8)
    # lifeboats slung along the top tier, amber like the funnel
    for bx in range(60, 100, 10):
        d.rectangle([bx, 25, bx + 5, 26], fill=11)
        d.line([(bx + 1, 26), (bx + 4, 26)], fill=12)
    # one great funnel, raked aft, a dark band at the top
    d.polygon([(70, 13), (72, 2), (84, 2), (84, 13)], fill=11)
    d.polygon([(79, 13), (81, 2), (84, 2), (84, 13)], fill=12)
    d.rectangle([72, 2, 84, 4], fill=15)
    # a foremast with a stay down to the bow, and a flag at the stern
    d.line([(24, 8), (24, 36)], fill=7)
    d.line([(21, 14), (27, 14)], fill=7)
    d.line([(24, 9), (8, 36)], fill=7)
    d.line([(118, 30), (118, 36)], fill=7)
    d.rectangle([119, 30, 121, 32], fill=4)
    outline(img, 1, skip=(13, 7))
    return img


def write_pal(path, pal):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in pal))


SHEETS = [   # file, maker, palette (None = keep the file's own)
    ("birth_island_stone.png", stone, None),
    ("seagallop.png", seagallop, ("seagallop.pal", SEA_PAL)),
    ("ss_anne.png", ss_anne, ("ss_anne.pal", ANNE_PAL)),
]


def main():
    built, tiles = [], []
    for filename, maker, palinfo in SHEETS:
        old = Image.open(os.path.join(MISC, filename))
        img = maker()
        assert img.size == old.size, (filename, img.size, old.size)
        pal = palinfo[1] if palinfo else [tuple(old.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
        if filename == "birth_island_stone.png":
            used = set(img.getdata()) - {0}
            assert used <= {1, 2, 3}, "the puzzle recolours only 1-3: %s" % sorted(used)
        flat = [c for rgb in pal for c in rgb]
        img.putpalette(flat + [0] * (768 - len(flat)))
        built.append((filename, img, palinfo))
        tiles.append((img, old))
    S = 4
    W = sum(max(a.width, b.width) * S + 16 for a, b in tiles)
    H = 64 * S * 2 + 16
    out = Image.new("RGB", (W, H), (60, 60, 60)); x = 0
    for img, old in tiles:
        for k, im in enumerate((img, old)):
            bg = Image.new("RGB", im.size, (96, 150, 200))
            bg.paste(im.convert("RGB"), (0, 0), Image.frombytes("L", im.size, bytes(255 if i else 0 for i in im.getdata())))
            out.paste(bg.resize((im.width * S, im.height * S), Image.NEAREST), (x, k * (H // 2)))
        x += max(img.width, old.width) * S + 16
    out.save(PREVIEW)
    print("  %d sheets -> preview %s (ours above, vanilla's below)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img, palinfo in built:
            img.save(os.path.join(MISC, filename), bits=4)
            if palinfo:
                write_pal(os.path.join(PALS, palinfo[0]), palinfo[1])
        print("  written: %s, and seagallop.pal, ss_anne.pal" % ", ".join(f for f, _, _ in built))


if __name__ == "__main__":
    main()

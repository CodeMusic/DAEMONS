#!/usr/bin/env python3
"""T-485 DRAFT: OSRIC HATTER's house on QUICKSILVER -- the exterior, the island before and after, the room, and him.

    ~/.pyenv/versions/3.12.2/bin/python3 gfx/drafts/t485/draw_t485.py      # writes the PNGs beside this file

A draft for the user's sheet, NOT a build: nothing here touches the engine. It reads the island's own render
(tools/reviewsheet.py map ... CinnabarIsland, rebuilt into the scratch file passed as argv[1], or island_before.png
here) and the QUICKSILVER people's palette, and draws:

  hat_1x.png / hat_3x.png         the leaning top hat, 3x3 cells (48x48) at CinnabarIsland (9..11, 11..13), in
                                  palette row 12 of secondary/cinnabar_island (unused: no block draws it), 15 colours
  hat_cells.png                   the drawing cut into its 8 cells and 8x8 tiles, the unique count against the 30 free
  island_before.png / island_after.png (1x) and island_before_after_3x.png
  room_1x.png / room_3x.png       the room, on LAYOUT_HOUSE1's 11x9 plan (door mat and warp at (4,7) kept)
  osric_hatter.png                the overworld sheet, 144x32, nine 16x32 frames in vanilla's order, indexed
  osric_hatter_sheet.png          front, back and side at 6x, in his own palette and in QUICKSILVER's
  t485_sheet.png                  everything on one contact sheet
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
GBA = os.path.join(ROOT, "engineGba")

# ---------------------------------------------------------------- palette row 12 (secondary/cinnabar_island)
ROW12 = [
    (124, 192, 104),  # 0  transparent (the island's key colour, as rows 8..11)
    (40, 34, 48),     # 1  outline and the card's ink
    (58, 52, 70),     # 2  felt, shaded side
    (84, 76, 100),    # 3  felt
    (112, 104, 130),  # 4  felt, lit side and the crown's top
    (150, 142, 170),  # 5  felt highlight (the sheen on the nap)
    (112, 50, 104),   # 6  band, dark
    (176, 86, 158),   # 7  band: THE SUBTLE LAYER's purple, #B0569E (4.39's pulse midpoint)
    (240, 232, 208),  # 8  the price card
    (200, 186, 150),  # 9  the card's shade
    (132, 84, 66),    # 10 door wood
    (84, 54, 46),     # 11 door, dark
    (236, 201, 140),  # 12 the porthole's lamp
    (226, 232, 240),  # 13 quicksilver
    (160, 170, 186),  # 14 quicksilver, shade
    (197, 172, 106),  # 15 the hat's shadow on the sand (the sand's own shade)
]


def hat():
    """48x48, indexed into ROW12; 0 is transparent. Cell (2,0) -- x 32..47, y 0..15 -- stays empty: it is the
    old man's square at (11,11), and the crown leans away from him."""
    im = Image.new("P", (48, 48), 0)
    im.putpalette(sum(ROW12, ()))
    p = im.load()

    def put(x, y, c):
        if 0 <= x < 48 and 0 <= y < 48 and not (x >= 32 and y < 16):
            p[x, y] = c

    # the shadow first, lower right (the light is from the upper left, as every landmark's)
    for y in range(40, 48):
        for x in range(30, 48):
            if ((x - 38) / 10.0) ** 2 + ((y - 45) / 3.2) ** 2 <= 1:
                put(x, y, 15)

    # the brim: an ellipse seen from above, centre (24, 42), rx 22, ry 5
    bcx, bcy, brx, bry = 24, 42, 22, 5
    for y in range(36, 48):
        for x in range(0, 48):
            e = ((x - bcx) / brx) ** 2 + ((y - bcy) / bry) ** 2
            if e <= 1:
                put(x, y, 4 if y < bcy else (3 if y < bcy + 3 else 2))
    for y in range(36, 48):  # outline the brim
        for x in range(0, 48):
            e = ((x - bcx) / brx) ** 2 + ((y - bcy) / bry) ** 2
            if e <= 1:
                ins = all(((x + dx - bcx) / brx) ** 2 + ((y + dy - bcy) / bry) ** 2 <= 1
                          for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if not ins:
                    put(x, y, 1)

    # the crown: leaning left as it rises -- base x 12..35 at y 41, top x 4..27 at y 6 (a little flared)
    def edges(y):
        t = (41 - y) / 35.0
        return 12 + (4 - 12) * t, 35 + (27 - 35) * t

    for y in range(6, 42):
        l, r = edges(y)
        L, R = int(round(l)), int(round(r))
        for x in range(L, R + 1):
            u = (x - l) / max(1.0, (r - l))
            c = 4 if u < 0.24 else (3 if u < 0.72 else 2)
            if 0.10 <= u < 0.16:
                c = 5
            put(x, y, c)
        put(L, y, 1); put(R, y, 1)

    # the crown's top, seen from above: an ellipse at (15.5, 6), rx 11.5, ry 3
    tcx, tcy, trx, tr_y = 15.5, 6, 11.5, 3
    for y in range(2, 11):
        for x in range(0, 32):
            e = ((x - tcx) / trx) ** 2 + ((y - tcy) / tr_y) ** 2
            if e <= 1:
                ins = all(((x + dx - tcx) / trx) ** 2 + ((y + dy - tcy) / tr_y) ** 2 <= 1
                          for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                put(x, y, 4 if ins else 1)
    for x in range(8, 15):  # a sheen across the top
        put(x, 5, 5)

    # the band, above the door: y 27..31, following the lean
    for y in range(27, 32):
        l, r = edges(y)
        L, R = int(round(l)), int(round(r))
        for x in range(L + 1, R):
            u = (x - l) / (r - l)
            put(x, y, 6 if (y in (27, 31) or u > 0.72) else 7)

    # the price card, tucked into the band at the front right, its foot behind the band: 10/6
    cx0, cy0, cw, ch = 17, 19, 17, 10
    for y in range(cy0, cy0 + ch):
        for x in range(cx0, cx0 + cw):
            edge = x in (cx0, cx0 + cw - 1) or y == cy0
            put(x, y, 1 if edge else (9 if y == cy0 + ch - 2 else 8))
    glyph = {
        "1": [".#", "##", ".#", ".#", ".#"],
        "0": ["###", "#.#", "#.#", "#.#", "###"],
        "/": ["..#", "..#", ".#.", "#..", "#.."],
        "6": ["###", "#..", "###", "#.#", "###"],
    }
    gx = cx0 + 2
    for ch_ in "10/6":
        g = glyph[ch_]
        for yy, row in enumerate(g):
            for xx, c in enumerate(row):
                if c == "#":
                    put(gx + xx, cy0 + 2 + yy, 1)
        gx += len(g[0]) + 1
    for y in range(27, 32):  # the band passes in front of the card's foot
        for x in range(cx0, cx0 + cw):
            l, r = edges(y)
            if l < x < r:
                put(x, y, 6 if y in (27, 31) else 7)
            elif x >= r:
                put(x, y, 1 if y in (27, 31) else 9)

    # the porthole, on the lit side, a lamp lit inside: centre (11, 15)
    for y in range(12, 21):
        for x in range(4, 15):
            dd = (x - 11) ** 2 + (y - 15) ** 2
            if dd <= 9:
                put(x, y, 12)
            elif dd <= 16:
                put(x, y, 1)
    put(10, 14, 13); put(9, 15, 13)

    # the door: an arch cut into the crown's foot, the brim its step -- the door cell is (10,13), x 16..31
    for y in range(32, 46):
        for x in range(19, 29):
            arch = y >= 35 or ((x - 23.5) / 5.0) ** 2 + ((y - 35) / 3.0) ** 2 <= 1
            if arch:
                put(x, y, 11 if (x in (19, 28) or y == 32) else 10)
    for y in range(32, 46):  # its outline
        for x in range(18, 30):
            if p[x, y] not in (10, 11):
                n = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                if any(0 <= a < 48 and 0 <= b < 48 and p[a, b] in (10, 11) for a, b in n):
                    put(x, y, 1)
    for y in range(38, 46):  # planks, and a knob
        put(23, y, 11)
    put(26, 40, 12)
    for x in range(18, 30):  # the step: the brim runs on under the door, lit
        put(x, 45, 4); put(x, 46, 3)
    for x in range(17, 31):
        put(x, 47, 1)

    # quicksilver, beaded on the brim
    for (x, y) in ((6, 42), (40, 43), (13, 45), (35, 46)):
        put(x, y, 13); put(x + 1, y, 14)
    return im


def tiles_report(h):
    """Cut the hat into its cells and 8x8 tiles and count unique tiles, flips shared, empties dropped."""
    px = h.load()
    cells = [(cx, cy) for cy in range(3) for cx in range(3) if (cx, cy) != (2, 0)]
    seen, n_empty, total = set(), 0, 0
    for cx, cy in cells:
        for ty in range(2):
            for tx in range(2):
                x0, y0 = cx * 16 + tx * 8, cy * 16 + ty * 8
                t = tuple(tuple(px[x0 + i, y0 + j] for i in range(8)) for j in range(8))
                total += 1
                if all(v == 0 for r in t for v in r):
                    n_empty += 1
                    continue
                forms = {t, tuple(r[::-1] for r in t), t[::-1], tuple(r[::-1] for r in t[::-1])}
                if not (forms & seen):
                    seen.add(t)
    return len(seen), n_empty, total


# ---------------------------------------------------------------- the stoat
# his own palette: QUICKSILVER's people's (npc_town_quicksilver.pal) with two slots turned to the band's purple
def town_pal():
    v = open(os.path.join(GBA, "graphics/object_events/palettes/npc_town_quicksilver.pal")).read().split()[3:]
    v = [int(x) for x in v]
    return [tuple(v[i:i + 3]) for i in range(0, 48, 3)]


def own_pal():
    p = town_pal()
    p[5] = (176, 86, 158)  # light blue -> the band's purple (only his hat band and bow use 5 and 6)
    p[6] = (112, 50, 104)  # blue -> band, dark
    return p

# K outline 13 · F felt 4 · f felt lit 3 · B band 5 · b band dark 6 · C card 7 · R fur 10 · T fur lit 9
# W cream 8 · E eye/nose 15 · V waistcoat 12 · O bow 11 · G grey shoe 4 · t tail tip 13
KEY = {".": 0, "K": 13, "F": 4, "f": 3, "B": 5, "b": 6, "C": 7, "R": 10, "T": 9, "W": 8, "E": 15, "V": 12,
       "O": 11, "N": 15, "G": 13}

FRONT = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "...KKKKKKKK.....",
    "..KfFFFFFFFK....",
    "..KfFFFFFFFK....",
    "...KfFFFFFFK....",
    "...KfFFFFFCK....",
    "...KBBBBBBCK....",
    "...KbBBBBBbK....",
    ".KKKKKKKKKKKKK..",
    "..KRRKKKKKKRRK..",
    "..KRRRRRRRRRRK..",
    "..KRERRRRRRERK..",
    "..KTWWWWWWWWTK..",
    "..KWWWWWNWWWWK..",
    "...KWWWWWWWWK...",
    "....KKWWWWKK....",
    "...KVVOOOOVVK...",
    "..KRVVWWWWVVRK..",
    "..KRVVWWWWVVRK..",
    "..KTVVWWWWVVTK..",
    "...KVVWWWWVVK...",
    "...KRRRRRRRRK...",
    "...KRRRKKRRRK...",
    "...KRRK..KRRK...",
    "...KGGK..KGGK...",
    "...KKKK..KKKK...",
    "................",
]
BACK = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    ".....KKKKKKKK...",
    "....KfFFFFFFFK..",
    "....KfFFFFFFFK..",
    "....KfFFFFFFK...",
    "....KfFFFFFFK...",
    "....KBBBBBBBK...",
    "....KbBBBBBbK...",
    "..KKKKKKKKKKKKK.",
    "..KRRKKKKKKRRK..",
    "..KRRRRRRRRRRK..",
    "..KRRRRRRRRRRK..",
    "..KTRRRRRRRRTK..",
    "..KRRRRRRRRRRK..",
    "...KRRRRRRRRK...",
    "....KKRRRRKK....",
    "...KVVVVVVVVK...",
    "..KRVVVVVVVVRK..",
    "..KRVVVVVVVVRK..",
    "..KTVVVVVVVVTK..",
    "...KVVVVVVVVKKK.",
    "...KRRRRRRRRKRRK",
    "...KRRRKKRRRKGGK",
    "...KRRK..KRRKKK.",
    "...KGGK..KGGK...",
    "...KKKK..KKKK...",
    "................",
]
SIDE = [  # facing left (west); the engine mirrors it for east
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "....KKKKKKK.....",
    "...KfFFFFFFK....",
    "...KfFFFFFFK....",
    "....KfFFFFFK....",
    "....KCFFFFFK....",
    "....KCBBBBBK....",
    "....KbBBBBbK....",
    "..KKKKKKKKKKKK..",
    "....KRRRRRKRRK..",
    "...KRRRRRRRRRK..",
    "..KKERRRRRRRRK..",
    ".KNWWWRRRRRRK...",
    "..KWWWWWRRRRK...",
    "...KKWWWRRRK....",
    ".....KWWWKK.....",
    ".....KOVVVK.....",
    ".....KVVRRK.....",
    ".....KVVRRK.....",
    ".....KVVTTK..KK.",
    ".....KVVVVK.KGGK",
    ".....KRRRRKKRRK.",
    ".....KRRRRRRRK..",
    ".....KRRKRRKK...",
    ".....KGGKGGK....",
    ".....KKKKKKK....",
    "................",
]


def walk(frame, step):
    """A walk frame: one foot lifted a pixel, the other planted (vanilla's two-step)."""
    old = [list(r) for r in frame]
    f = [list(r) for r in frame]
    half = range(0, 8) if step == 0 else range(8, 16)
    for x in half:  # lift this half's leg by one row
        for y in (28, 29, 30):
            f[y - 1][x] = old[y][x]
        f[30][x] = "."
    return ["".join(r) for r in f]


def to_img(rows, pal):
    im = Image.new("P", (16, 32), 0)
    im.putpalette(sum(pal, ()))
    px = im.load()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            px[x, y] = KEY[c]
    return im


def stoat_sheet(pal):
    """vanilla's nine: face S, N, W, then walk S x2, N x2, W x2."""
    frames = [FRONT, BACK, SIDE, walk(FRONT, 0), walk(FRONT, 1), walk(BACK, 0), walk(BACK, 1),
              walk(SIDE, 0), walk(SIDE, 1)]
    sheet = Image.new("P", (144, 32), 0)
    sheet.putpalette(sum(pal, ()))
    for i, f in enumerate(frames):
        sheet.paste(to_img(f, pal), (i * 16, 0))
    return sheet


# ---------------------------------------------------------------- the room, on LAYOUT_HOUSE1's plan (11x9)
def hand(d, cx, cy, ang, ln, col, w=1):
    a = math.radians(ang - 90)
    d.line([(cx, cy), (cx + ln * math.cos(a), cy + ln * math.sin(a))], fill=col, width=w)


def clockface(d, cx, cy, r, rim, face=(240, 232, 208), ink=(40, 34, 48)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=face, outline=rim)
    if r >= 5:
        for k in range(12):
            a = math.radians(k * 30 - 90)
            d.point((cx + (r - 1.5) * math.cos(a), cy + (r - 1.5) * math.sin(a)), fill=ink)
    # half past three: the minute hand at the six, the hour hand halfway from three to four
    hand(d, cx, cy, 180, r - 1.5, ink)
    hand(d, cx, cy, 105, max(2, r * 0.55), ink)


def room(stoat_side):
    W, H = 176, 144
    im = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(im)
    INK = (40, 34, 48)
    # the back wall, rows 0..1: plum paper in stripes, a wainscot
    for x in range(W):
        d.line([(x, 0), (x, 31)], fill=(98, 62, 92) if (x // 4) % 2 else (112, 72, 104))
    d.rectangle([0, 24, W - 1, 31], fill=(132, 84, 66)); d.line([(0, 24), (W, 24)], fill=(170, 120, 86))
    d.line([(0, 31), (W, 31)], fill=INK)
    # the floor, rows 2..7: boards
    for y in range(32, 128):
        for x in range(W):
            c = (176, 132, 88) if ((y - 32) // 6) % 2 == 0 else (164, 122, 80)
            if (x + ((y - 32) // 6) * 23) % 40 == 0:
                c = (128, 92, 62)
            im.putpixel((x, y), c)
    for y in range(38, 128, 6):
        d.line([(0, y), (W, y)], fill=(140, 102, 70))
    # the bottom wall, row 8, and the door mat at (4,7) where LAYOUT_HOUSE1 has it
    d.rectangle([0, 128, W - 1, H - 1], fill=(40, 34, 48))
    d.rectangle([52, 114, 91, 126], fill=(150, 60, 70), outline=INK)
    d.rectangle([64, 116, 79, 124], outline=(200, 130, 110))

    # the clocks, every one at half past three
    # a grandfather clock, cell (1, 0..1)
    d.rectangle([17, 0, 30, 33], fill=(92, 58, 44), outline=INK)
    d.rectangle([19, 18, 28, 30], fill=(70, 44, 36), outline=INK)
    d.line([(23.5, 18), (23.5, 27)], fill=(200, 170, 90)); d.ellipse([21, 25, 26, 30], fill=(220, 186, 96), outline=INK)
    clockface(d, 23.5, 9, 6, INK)
    # wall clocks: round (3,0), a tall oval (5,0), a small square (7,0), a cuckoo (9,0), an odd one (0,0)
    clockface(d, 56, 10, 6, INK)
    d.ellipse([83, 2, 92, 20], fill=(150, 142, 170), outline=INK); clockface(d, 87.5, 9, 4, INK)
    d.rectangle([115, 4, 126, 15], fill=(132, 84, 66), outline=INK); clockface(d, 120.5, 9.5, 4, INK)
    d.polygon([(146, 2), (154, 6), (154, 20), (138, 20), (138, 6)], fill=(116, 76, 56), outline=INK)
    clockface(d, 146, 12, 4, INK)
    d.rectangle([144, 3, 147, 5], fill=(40, 34, 48))  # the cuckoo's door, shut
    clockface(d, 6, 9, 3, INK); clockface(d, 166, 18, 3, INK); clockface(d, 70, 19, 3, INK)
    clockface(d, 101, 18, 3, INK)
    # a mantel clock and a carriage clock on the sideboard, cells (5..7, 1)
    d.rectangle([80, 22, 127, 31], fill=(110, 70, 54), outline=INK)
    clockface(d, 92, 19, 3, INK); clockface(d, 112, 19, 3, INK)
    # a fallen pocket watch on the floor by the door, still at half past three
    clockface(d, 132, 112, 3, INK)
    d.line([(135, 112), (142, 116)], fill=(226, 232, 240))

    # the long table, cells (2..8, 4..5): a cloth, laid for many
    tx0, tx1, ty0, ty1 = 34, 141, 64, 93
    d.rectangle([tx0, ty0, tx1, ty1], fill=(240, 236, 226), outline=INK)
    d.rectangle([tx0, ty1 - 4, tx1, ty1], fill=(210, 204, 196), outline=INK)
    for x in range(tx0 + 6, tx1, 9):
        d.point((x, ty1 - 2), fill=(176, 86, 158))
    # chairs: backs along row 3, seats along row 6, one at the foot (1,4); his, tall, at the head (9,4)
    for i, cx in enumerate(range(2, 9)):
        x = cx * 16
        d.rectangle([x + 3, 44, x + 12, 62], fill=(132, 84, 66), outline=INK)        # back, row 3
        d.rectangle([x + 5, 47, x + 10, 58], fill=(176, 86, 158) if i % 2 else (112, 50, 104))
        d.rectangle([x + 3, 96, x + 12, 104], fill=(132, 84, 66), outline=INK)        # seat, row 6
        d.line([(x + 4, 105), (x + 4, 109)], fill=INK); d.line([(x + 11, 105), (x + 11, 109)], fill=INK)
    d.rectangle([19, 70, 30, 88], fill=(132, 84, 66), outline=INK)                    # the foot, (1,4)
    d.rectangle([146, 56, 159, 90], fill=(84, 54, 46), outline=INK)                   # his, (9,4): tall-backed
    d.rectangle([148, 59, 157, 74], fill=(176, 86, 158), outline=INK)
    # the setting: a cup and saucer at every place, teapots, a cake, an empty plate turned over
    for cx in range(2, 9):
        x = cx * 16 + 8
        for y in (70, 87):
            d.ellipse([x - 4, y - 2, x + 4, y + 2], fill=(226, 232, 240), outline=(160, 170, 186))
            d.rectangle([x - 2, y - 4, x + 2, y], fill=(250, 250, 250), outline=(120, 122, 140))
    for x in (60, 108):
        d.ellipse([x - 5, 74, x + 5, 83], fill=(84, 130, 112), outline=INK)
        d.line([(x + 5, 77), (x + 9, 74)], fill=INK); d.rectangle([x - 1, 72, x + 1, 74], fill=INK)
    d.ellipse([78, 74, 92, 84], fill=(236, 201, 140), outline=INK); d.line([(85, 74), (85, 84)], fill=(176, 86, 158))
    d.ellipse([124, 75, 134, 82], fill=(200, 186, 150), outline=INK)
    # his own place: a full cup, a hat-block for the felt
    d.ellipse([133, 76, 141, 82], fill=(226, 232, 240), outline=INK); d.point((137, 79), fill=(132, 84, 66))
    # a hat stand by the wall, (10,2), with a hat on it -- and a coil of felt
    d.line([(168, 34), (168, 60)], fill=INK, width=2); d.ellipse([160, 26, 175, 34], fill=(84, 76, 100), outline=INK)
    d.rectangle([163, 18, 172, 29], fill=(84, 76, 100), outline=INK)
    # him at the head, (9,4), facing the table: his side frame, which faces west
    im.paste(stoat_side, (144, 48), stoat_side)
    return im


def label(img, text, scale=1):
    F = ImageFont.load_default()
    out = Image.new("RGB", (img.width, img.height + 14), (24, 24, 28))
    out.paste(img, (0, 14))
    ImageDraw.Draw(out).text((2, 1), text, fill=(230, 230, 230), font=F)
    return out


def main():
    scratch_island = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "island_before.png")
    before = Image.open(scratch_island).convert("RGB")
    before.save(os.path.join(HERE, "island_before.png"))

    h = hat()
    h.save(os.path.join(HERE, "hat_1x.png"))
    h.resize((144, 144), Image.NEAREST).save(os.path.join(HERE, "hat_3x.png"))
    uniq, empty, total = tiles_report(h)

    after = before.copy()
    mask = Image.frombytes("L", h.size, h.tobytes()).point(lambda v: 255 if v else 0)
    after.paste(h.convert("RGB"), (9 * 16, 11 * 16), mask)
    after.save(os.path.join(HERE, "island_after.png"))

    def grid3(im):
        im3 = im.resize((im.width * 3, im.height * 3), Image.NEAREST)
        return im3
    b3, a3 = grid3(before), grid3(after)
    pair = Image.new("RGB", (b3.width * 2 + 24, b3.height + 30), (24, 24, 28))
    pair.paste(b3, (0, 30)); pair.paste(a3, (b3.width + 24, 30))
    dr = ImageDraw.Draw(pair)
    F = ImageFont.load_default()
    dr.text((4, 8), "QUICKSILVER before (vanilla plan, T-447 landmarks), 3x", fill=(230, 230, 230), font=F)
    dr.text((b3.width + 28, 8), "after: OSRIC HATTER's hat at (9..11, 11..13), door (10,13) -- DRAFT", fill=(230, 230, 230), font=F)
    x0, y0 = b3.width + 24 + 9 * 48, 30 + 11 * 48
    dr.rectangle([x0, y0 + 48, x0 + 3 * 48 - 1, y0 + 3 * 48 - 1], outline=(255, 64, 64))
    dr.rectangle([x0, y0, x0 + 2 * 48 - 1, y0 + 47], outline=(255, 200, 64))
    pair.save(os.path.join(HERE, "island_before_after_3x.png"))

    # the hat on the island, close, at 1x and 3x
    crop = after.crop((4 * 16, 8 * 16, 17 * 16, 16 * 16))
    crop.save(os.path.join(HERE, "hat_on_island_1x.png"))
    crop.resize((crop.width * 3, crop.height * 3), Image.NEAREST).save(os.path.join(HERE, "hat_on_island_3x.png"))

    # the cells
    cells = Image.new("RGB", (3 * 16 * 6 + 2 * 6, 3 * 16 * 6 + 2 * 6), (24, 24, 28))
    big = h.convert("RGB").resize((288, 288), Image.NEAREST)
    for cy in range(3):
        for cx in range(3):
            tile = big.crop((cx * 96, cy * 96, cx * 96 + 96, cy * 96 + 96))
            cells.paste(tile, (cx * 102, cy * 102))
    dc = ImageDraw.Draw(cells)
    for cy in range(3):
        for cx in range(3):
            for k in (1,):
                dc.line([(cx * 102 + 48, cy * 102), (cx * 102 + 48, cy * 102 + 95)], fill=(60, 60, 70))
                dc.line([(cx * 102, cy * 102 + 48), (cx * 102 + 95, cy * 102 + 48)], fill=(60, 60, 70))
    dc.text((2 * 102 + 4, 4), "old man\n(11,11)\nnothing\ndrawn", fill=(230, 230, 230), font=F)
    cells.save(os.path.join(HERE, "hat_cells.png"))

    # him
    own, town = own_pal(), town_pal()
    s_own = stoat_sheet(own)
    s_own.save(os.path.join(HERE, "osric_hatter.png"))
    s_town = stoat_sheet(town)
    sheet = Image.new("RGB", (3 * 16 * 6 + 3 * 16 * 6 + 60, 32 * 6 + 40), (24, 24, 28))
    dd = ImageDraw.Draw(sheet)
    for j, (s, name) in enumerate(((s_own, "his own palette (band purple)"), (s_town, "QUICKSILVER's people's palette"))):
        rgb = s.convert("RGB")
        for i, fi in enumerate((0, 2, 1)):
            fr = rgb.crop((fi * 16, 0, fi * 16 + 16, 32)).resize((96, 192), Image.NEAREST)
            sheet.paste(fr, (j * (288 + 60) + i * 96, 30))
        dd.text((j * (288 + 60) + 4, 8), name + ": front, side, back", fill=(230, 230, 230), font=F)
    sheet.save(os.path.join(HERE, "osric_hatter_sheet.png"))
    walk_strip = s_own.convert("RGB").resize((144 * 4, 128), Image.NEAREST)
    walk_strip.save(os.path.join(HERE, "osric_hatter_frames_4x.png"))

    # the room
    side = s_own.convert("RGBA").crop((32, 0, 48, 32))
    px = side.load()
    key = own[0]
    for y in range(32):
        for x in range(16):
            if px[x, y][:3] == key:
                px[x, y] = (0, 0, 0, 0)
    r = room(side)
    r.save(os.path.join(HERE, "room_1x.png"))
    r.resize((528, 432), Image.NEAREST).save(os.path.join(HERE, "room_3x.png"))

    # one contact sheet
    parts = [
        label(pair, "1. the plot"),
        label(Image.open(os.path.join(HERE, "hat_on_island_3x.png")), "2. the exterior on the island, 3x (1x beside it)"),
        label(r.resize((528, 432), Image.NEAREST), "3. the room, 3x: every clock at half past three; the table laid for many; his chair at the head"),
        label(sheet, "4. OSRIC HATTER, a stoat, 6x"),
    ]
    Wd = max(p.width for p in parts) + 20
    Hd = sum(p.height for p in parts) + 20 * (len(parts) + 1)
    cs = Image.new("RGB", (Wd, Hd), (16, 16, 20))
    y = 20
    for i, p in enumerate(parts):
        cs.paste(p, (10, y))
        if i == 1:
            cs.paste(crop, (10 + p.width + 20, y + 14))
            cs.paste(h.convert("RGB").resize((144, 144), Image.NEAREST), (10 + p.width + 20, y + 14 + crop.height + 20))
        y += p.height + 20
    cs.save(os.path.join(HERE, "t485_sheet.png"))
    print("hat: %d unique 8x8 tiles (flips shared), %d of %d empty; 30 slots free in cinnabar_island (346..375)"
          % (uniq, empty, total))


if __name__ == "__main__":
    main()

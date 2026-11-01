#!/usr/bin/env python3
"""T-509 DRAFT: the tarot card frames, drawn for the GBA.

Four faces -- REASON (a green circuit) and INSTINCT (a gold net) for THE SUBTLE
LAYER, ABOVE and BELOW (emerald on the breathing purple) for THE HERMETIC LAYER,
which replaced round one's single SPELLCRAFT face -- each with a shiny palette
(1 in 16), and one shared back that never shows the type. Also the mocks: the
spread, the deck selectors, and the page a turned card's words go on (sheet2.png).
sheet.png is round one's sheet, kept as it was (commit cc85f3c0 reproduces it).

How it is drawn: every card is a 72x104 grid of palette indices (9x13 tiles,
4bpp). Index 0 is transparent; each frame uses at most 15 colours more, so it is
one 16-colour BG palette. The daemon's 64x64 front sprite sits over it in its own
palette (an OBJ, or a second BG palette), so the frame never shares its colours.

  * shiny is a PALETTE SWAP of the same tiles, plus a few sparkle pixels on
    index 15 (a handful of extra tiles);
  * the hermetic pulse is index 14 alone, so the "breathing" is one palette
    write per beat (red #C8405A <-> blue #4F6BD8), no tiles touched;
  * the back has its own palette and is the same bytes for every deck.

The masters are 512x512: the card at exactly 4x, centred. Reducing a master to
the GBA card is an exact integer divide, so nothing is resampled -- nearest
neighbour, integer factors, everywhere (the sheet too).

  ~/.pyenv/versions/3.12.2/bin/python3 gfx/drafts/t509_cards/draw_cards.py

Reads the sample sprites from the companion (read only) and writes into this
folder. DRAFT: nothing here is in the game yet.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ART = Path.home() / "Projects/daemons-companion/server/data/art"

W, H = 72, 104                      # the card: 9 x 13 tiles
SPRITE_XY = (4, 14)                 # the 64x64 window
KW_BAND = (4, 12)                   # keyword band rows (inclusive)
WIN = (14, 77)                      # sprite window rows
PHRASE = (79, 99)                   # phrase area rows
MASTER = 512
SCALE = 4                           # master = card x 4, centred on 512

# palette layout, shared by every frame
T, OUT, BG0, BG1, BG2, MD, MM, ML, FD, FM, FL, PANEL, INK, DIM, PULSE, SPARK = range(16)


def hexrgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def pal(*hexes: str) -> list[tuple[int, int, int]]:
    assert len(hexes) == 16, len(hexes)
    return [hexrgb(h) for h in hexes]


#                 T          OUT        BG0        BG1        BG2        MD         MM         ML         FD         FM         FL         PANEL      INK        DIM        PULSE      SPARK
PALETTES = {
    "reason": pal("#000000", "#140A18", "#2A1830", "#46284C", "#5E3A62", "#1E5A3C", "#2E9A5A", "#8AE6A8", "#12402A", "#2E9A5A", "#8AE6A8", "#1C0F22", "#F2EAF2", "#8A7894", "#2E9A5A", "#8AE6A8"),
    "reason_shiny": pal("#000000", "#2A1830", "#7CC49A", "#A4DDB6", "#CDEFD6", "#8E4A80", "#6A3060", "#C070B0", "#8A6A20", "#E0B840", "#FFF0A0", "#E6F6EA", "#2A1830", "#7A6A80", "#6A3060", "#FFE860"),
    "instinct": pal("#000000", "#140A18", "#3A1E3E", "#5C2E52", "#8A4A5E", "#7A5418", "#C89838", "#F4D878", "#5A3C10", "#C89838", "#F4D878", "#24122A", "#F6EEDC", "#9A8070", "#C89838", "#F4D878"),
    "instinct_shiny": pal("#000000", "#1A2440", "#6CBCA8", "#98D6C2", "#C8EEE0", "#24407A", "#3A64A8", "#7AA4E0", "#8A6A20", "#E0B840", "#FFF0A0", "#E4F6F0", "#1A2440", "#6A7890", "#3A64A8", "#FFE860"),
    "spellcraft": pal("#000000", "#1A0A1A", "#5A2A55", "#84407A", "#B0569E", "#145C3E", "#1F8F5F", "#50C878", "#0F4A30", "#1F8F5F", "#50C878", "#2A1028", "#F2F0E8", "#9A86A0", "#C8405A", "#50C878"),
    "spellcraft_shiny": pal("#000000", "#3A1838", "#7CC49A", "#A4DDB6", "#CDEFD6", "#6A2E66", "#B0569E", "#E08AD0", "#8A6A20", "#E0B840", "#FFF0A0", "#E6F6EA", "#3A1838", "#7A6A80", "#C8405A", "#FFE860"),
}
PULSE_BLUE = hexrgb("#4F6BD8")

# the back: its own palette, no face's colour in it (silver on night)
#                     T          OUT        BG0        BG1        BG2        MD         MM         ML         FD         FM         FL         PANEL      INK        DIM        PULSE      SPARK
BACK_PAL = pal("#000000", "#0C0816", "#1C1530", "#2A2148", "#3A2F62", "#4E4486", "#8A82BC", "#D8D2F0", "#2A2148", "#8A82BC", "#D8D2F0", "#1C1530", "#D8D2F0", "#8A82BC", "#8A82BC", "#D8D2F0")

# ---------------------------------------------------------------- 3x5 font
FONT = {
    "A": "010101111101101", "B": "110101110101110", "C": "011100100100011",
    "D": "110101101101110", "E": "111100110100111", "F": "111100110100100",
    "G": "011100101101011", "H": "101101111101101", "I": "111010010010111",
    "J": "001001001101010", "K": "101101110101101", "L": "100100100100111",
    "M": "101111111101101", "N": "110101101101101", "O": "010101101101010",
    "P": "110101110100100", "Q": "010101101110011", "R": "110101110101101",
    "S": "011100010001110", "T": "111010010010010", "U": "101101101101111",
    "V": "101101101101010", "W": "101101111111101", "X": "101101010101101",
    "Y": "101101010010010", "Z": "111001010100111", " ": "000000000000000",
    "/": "001001010100100", "-": "000000111000000", ".": "000000000000010",
}


def text_w(s: str) -> int:
    return len(s) * 4 - 1


def draw_text(a: np.ndarray, s: str, x: int, y: int, v) -> None:
    for i, ch in enumerate(s):
        g = FONT[ch]
        for r in range(5):
            for c in range(3):
                if g[r * 3 + c] == "1":
                    yy, xx = y + r, x + i * 4 + c
                    if 0 <= yy < a.shape[0] and 0 <= xx < a.shape[1]:
                        a[yy, xx] = v


def draw_text_c(a, s, cx, y, v):
    draw_text(a, s, cx - text_w(s) // 2, y, v)


# ---------------------------------------------------------------- primitives
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def put(a, x, y, v, mask=None):
    x, y = int(x), int(y)
    if 0 <= y < a.shape[0] and 0 <= x < a.shape[1] and (mask is None or mask[y, x]):
        a[y, x] = v


def line(a, x0, y0, x1, y1, v, mask=None):
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        put(a, x0, y0, v, mask)
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def ring(a, cx, cy, r, v, mask=None, width=1.0):
    ys, xs = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    d = np.hypot(xs - cx, ys - cy)
    sel = (d >= r - width / 2) & (d < r + width / 2)
    if mask is not None:
        sel &= mask
    a[sel] = v


def outline_of(m: np.ndarray) -> np.ndarray:
    p = np.pad(m, 1)
    inner = p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return m & ~inner


def card_geometry():
    ys, xs = np.mgrid[0:H, 0:W]
    edge = np.minimum(np.minimum(xs, W - 1 - xs), np.minimum(ys, H - 1 - ys))
    corner = np.minimum(xs, W - 1 - xs) + np.minimum(ys, H - 1 - ys)
    return xs, ys, edge, corner


def base_card(glow_cy: float) -> tuple[np.ndarray, np.ndarray]:
    """Outline, a dithered radial glow and the inner mask; frame rings left to the face."""
    xs, ys, edge, corner = card_geometry()
    a = np.full((H, W), T, np.uint8)
    inside = corner >= 2
    a[inside] = OUT
    inner = (edge >= 4) & inside
    d = np.hypot((xs - 35.5) / 40.0, (ys - glow_cy) / 52.0)
    val = np.clip((1.0 - d) * 2.6, 0, 2.99) + (BAYER[ys % 4, xs % 4] - 0.5) * 0.9
    lvl = np.clip(val.astype(int), 0, 2)
    a[inner] = (BG0 + lvl)[inner]
    return a, inner


def panels(a, inner):
    """Inset keyword and phrase panels, rounded by one pixel, with a frame-colour rule."""
    for (y0, y1) in (KW_BAND, PHRASE):
        for y in range(y0, y1 + 1):
            for x in range(5, 67):
                if (y in (y0, y1)) and x in (5, 66):
                    continue
                a[y, x] = PANEL
    for x in range(4, 68):
        a[WIN[0] - 1, x] = FM
        a[WIN[1] + 1, x] = FM
    a[WIN[0] - 1, 4] = a[WIN[0] - 1, 67] = FD
    a[WIN[1] + 1, 4] = a[WIN[1] + 1, 67] = FD


def window_mask():
    m = np.zeros((H, W), bool)
    m[WIN[0]:WIN[1] + 1, 4:68] = True
    return m


# ---------------------------------------------------------------- REASON
def face_reason() -> np.ndarray:
    a, inner = base_card(glow_cy=46)
    xs, ys, edge, corner = card_geometry()
    rnd = random.Random(509_1)
    wm = window_mask()
    occ = np.zeros((H, W), bool)

    def free(x, y):
        if not (4 <= x < 68 and WIN[0] <= y <= WIN[1]):
            return False
        return not occ[max(0, y - 1):y + 2, max(0, x - 1):x + 2].any()

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    starts = []
    for y in range(WIN[0] + 3, WIN[1] - 2, 7):           # traces enter from both sides
        starts.append((4, y, (1, 0)))
        starts.append((67, y + 3, (-1, 0)))
    for x in range(9, 64, 9):                            # and from the rules
        starts.append((x, WIN[0], (0, 1)))
        starts.append((x + 4, WIN[1], (0, -1)))
    rnd.shuffle(starts)
    for (x, y, d) in starts[:18]:
        path = [(x, y)]
        occ[y, x] = True
        steps = rnd.randint(10, 26)
        run = rnd.randint(3, 9)
        for _ in range(steps):
            if run == 0:                                 # turn, or a 45-degree jog
                if rnd.random() < 0.5:
                    d = rnd.choice([dd for dd in dirs if dd != (-d[0], -d[1])])
                else:
                    jog = (d[0] or rnd.choice((-1, 1)), d[1] or rnd.choice((-1, 1)))
                    for _ in range(rnd.randint(2, 3)):
                        nx, ny = x + jog[0], y + jog[1]
                        if not free(nx, ny):
                            break
                        x, y = nx, ny
                        occ[y, x] = True
                        path.append((x, y))
                run = rnd.randint(3, 9)
            nx, ny = x + d[0], y + d[1]
            occ_backup = occ[y, x]
            occ[y, x] = False
            ok = free(nx, ny)
            occ[y, x] = occ_backup
            if not ok:
                break
            x, y = nx, ny
            occ[y, x] = True
            path.append((x, y))
            run -= 1
        if len(path) < 4:
            continue
        for (px, py) in path:
            a[py, px] = MM
        ex, ey = path[-1]                                # a pad: a ring with a lit dot
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                put(a, ex + dx, ey + dy, MD if (dx or dy) else ML, wm)
        sx, sy = path[0]
        put(a, sx, sy, ML, wm)
    # two chips, legs out (drawn after the traces, so traces run under them)
    for (cx, cy, cw, ch) in ((10, 20, 9, 5), (52, 66, 9, 5)):
        for y in range(cy, cy + ch):
            for x in range(cx, cx + cw):
                a[y, x] = MD
        for x in range(cx + 1, cx + cw - 1, 2):
            a[cy - 1, x] = MM
            a[cy + ch, x] = MM
        a[cy + 1, cx + 1] = ML
    # the frame: outline, a green trace, a dark channel, vias every six
    a[(edge == 1) & (corner >= 2)] = FM
    a[(edge == 2) & (corner >= 2)] = FD
    a[(edge == 3) & (corner >= 2)] = OUT
    via = (edge == 1) & (((xs + ys) % 6) == 0) & (corner >= 3)
    a[via] = FL
    for (cx, cy) in ((1, 1), (W - 5, 1), (1, H - 5), (W - 5, H - 5)):   # corner pads
        a[cy:cy + 4, cx:cx + 4] = FD
        a[cy + 1:cy + 3, cx + 1:cx + 3] = FL
    _round(a, corner)
    panels(a, inner)
    return a


# ---------------------------------------------------------------- INSTINCT
def face_instinct() -> np.ndarray:
    a, inner = base_card(glow_cy=46)
    xs, ys, edge, corner = card_geometry()
    rnd = random.Random(509_2)
    wm = window_mask()
    # a net: knots jittered off a lattice, each tied to its near neighbours
    pts = []
    for j, y in enumerate(range(WIN[0] + 2, WIN[1] + 1, 12)):
        for i, x in enumerate(range(6 + (6 if j % 2 else 0), 68, 12)):
            pts.append((min(66, x + rnd.randint(-3, 3)), min(WIN[1] - 1, y + rnd.randint(-3, 3))))
    for i, p in enumerate(pts):
        near = sorted(pts, key=lambda q: (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)[1:4]
        for q in near:
            line(a, p[0], p[1], q[0], q[1], MD, wm)
    for (x, y) in pts:                                   # knots: big ones lit, small ones gold
        if rnd.random() < 0.35:
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                put(a, x + dx, y + dy, ML, wm)
            for dx, dy in ((-1, 0), (2, 0), (0, -1), (1, -1), (-1, 1), (2, 1), (0, 2), (1, 2)):
                put(a, x + dx, y + dy, MM, wm)
        else:
            put(a, x, y, MM, wm)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if rnd.random() < 0.5:
                    put(a, x + dx, y + dy, MM, wm)
    # the frame: a twisted gold rope, knots at the corners
    rope = (edge >= 1) & (edge <= 2) & (corner >= 2)
    twist = (((xs + ys + edge) // 2) % 2) == 0
    a[rope & twist] = FL
    a[rope & ~twist] = FM
    a[(edge == 3) & (corner >= 2)] = FD
    for (cx, cy) in ((2, 2), (W - 3, 2), (2, H - 3), (W - 3, H - 3)):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                put(a, cx + dx, cy + dy, FD if (dx or dy) else FL)
        put(a, cx, cy, FL)
    _round(a, corner)
    panels(a, inner)
    return a


# ---------------------------------------------------------------- THE HERMETIC LAYER: ABOVE and BELOW
# Round two (the user, 2026-11-01): SPELLCRAFT's single face becomes a pair, "as above, so below".
# Both keep the hermetic family -- emerald ink on the breathing purple, the pulse on index 14 alone -- and
# mirror each other top for bottom: BELOW is weighted at the base (courses laid one at a time, the top one
# unfinished, roots through the joints, strata of time above it), ABOVE at the crown (one star, its rays
# coming down, a pattern that arrives whole). Each carries its elements opposite its weight: BELOW's two
# downward triangles (water, earth) sit at the top of the window, ABOVE's two upward ones (fire, air) at the
# bottom, so each card points at the other.
GLYPHS = {
    "fire":  ["00100", "01010", "01010", "10001", "11111"],
    "air":   ["00100", "01010", "11111", "10001", "11111"],
    "water": ["11111", "10001", "01010", "01010", "00100"],
    "earth": ["11111", "10001", "11111", "01010", "00100"],
}


def _glyph(a, gx, gy, g, wm):
    for r, row in enumerate(GLYPHS[g]):
        for c, bit in enumerate(row):
            if bit == "1":
                put(a, gx + c, gy + r, ML, wm)


def hermetic_frame(a, corner, edge, gem_top: bool):
    a[(edge == 1) & (corner >= 2)] = FM
    a[(edge == 2) & (corner >= 2)] = FD
    a[(edge == 3) & (corner >= 2)] = FL
    gy = 1 if gem_top else H - 4                   # the pulse gem: at the crown above, at the base below
    for dy in range(3):
        for dx in range(4):
            if (dy == 1) or dx in (1, 2):
                put(a, 34 + dx, gy + dy, PULSE)
    put(a, 34, gy + 1, OUT)
    put(a, 37, gy + 1, OUT)
    for (px, py) in ((2, 2), (W - 3, 2), (2, H - 3), (W - 3, H - 3)):
        put(a, px, py, FL)
    _round(a, corner)


def face_below() -> np.ndarray:
    a, inner = base_card(glow_cy=74)               # the glow rises from the ground
    xs, ys, edge, corner = card_geometry()
    wm = window_mask()
    rnd = random.Random(509_4)
    base = WIN[1]
    courses = 7
    for k in range(courses):                       # brick by brick, from the base
        yb = base - 5 * k
        top = yb - 4
        last = k == courses - 1
        offs = 4 if k % 2 else 0
        laid = 4 + 8 * 3 + offs if last else 68    # the top course is still being laid
        for x in range(4, laid):
            put(a, x, top, MD, wm)
        for x0 in range(4 - offs, laid, 8):
            for y in range(top + 1, yb + 1):
                put(a, x0, y, MD, wm)
            if x0 + 1 >= 4 and rnd.random() < 0.55:
                put(a, x0 + 1, top + 1, MM, wm)
                put(a, x0 + 2, top + 1, MM, wm)
        if last:                                   # the next brick, held just above its place
            bx, by = laid + 2, top - 4
            for x in range(bx, bx + 8):
                put(a, x, by, MM, wm)
                put(a, x, by + 4, MM, wm)
            for y in range(by, by + 5):
                put(a, bx, y, MM, wm)
                put(a, bx + 7, y, MM, wm)
            put(a, bx + 1, by + 1, ML, wm)
    for (rx, drift) in ((14, -1), (49, 1), (31, 0)):   # roots, down through the joints
        x, y = rx, base - 5 * (courses - 2) - 4
        for step in range(34):
            put(a, x, y, MM, wm)
            y += 1
            if rnd.random() < 0.35:
                x += drift if drift else rnd.choice((-1, 1))
            if step in (12, 22) and rnd.random() < 0.8:          # a side root
                bx, bdir = x, rnd.choice((-1, 1))
                for by in range(y, min(base, y + 7)):
                    bx += bdir if rnd.random() < 0.6 else 0
                    put(a, bx, by, MD, wm)
    top_of_wall = base - 5 * (courses - 1) - 4
    for i, sy in enumerate(range(top_of_wall - 6, WIN[0] + 2, -7)):  # strata: time, laid down in lines
        v = PULSE if i == 0 else MD
        for x in range(4 + (i % 2), 68, 2 if i else 1):
            put(a, x, sy, v, wm)
    for k in range(courses):                       # a tally up the side: one notch a course
        put(a, 66, base - 5 * k - 2, ML, wm)
    _glyph(a, 6, WIN[0] + 2, "water", wm)
    _glyph(a, 61, WIN[0] + 2, "earth", wm)
    hermetic_frame(a, corner, edge, gem_top=False)
    panels(a, inner)
    return a


def face_above() -> np.ndarray:
    a, inner = base_card(glow_cy=18)               # the glow comes down from the crown
    xs, ys, edge, corner = card_geometry()
    wm = window_mask()
    rnd = random.Random(509_3)
    cx, cy = 35.5, WIN[0] + 5
    for k in range(-5, 6):                         # rays, all at once, from the top
        t = math.radians(90 + k * 14)
        x0, y0 = cx + 10 * math.cos(t), cy + 10 * math.sin(t)
        x1, y1 = cx + 80 * math.cos(t), cy + 80 * math.sin(t)
        line(a, x0, y0, x1, y1, MD, wm)
    ring(a, cx, cy, 7.5, PULSE, wm)                # the halo breathes
    ring(a, cx, cy, 10.5, MM, wm)
    for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1)):
        put(a, cx - 0.5 + dx, cy - 0.5 + dy, ML, wm)
    for r in range(2, 5):                          # an eight-point star
        for (ux, uy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            put(a, cx - 0.5 + (ux * r if ux > 0 else ux * r + 1), cy - 0.5 + (uy * r if uy > 0 else uy * r + 1), ML, wm)
    for r in (2, 3):
        for (ux, uy) in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            put(a, cx + ux * r, cy + uy * r, MM, wm)
    # the pattern that descends whole: a downward triangle of six stars, tied, arriving at once
    tri = [(18, 32), (36, 32), (54, 32), (27, 44), (45, 44), (36, 56)]
    for (i, j) in ((0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5), (4, 5)):
        line(a, *tri[i], *tri[j], MM, wm)
    for (x, y) in tri:
        for (dx, dy) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            put(a, x + dx, y + dy, ML if (dx, dy) == (0, 0) else MM, wm)
    for _ in range(18):                            # and the field of stars around it
        x, y = rnd.randint(5, 66), rnd.randint(WIN[0] + 1, WIN[1] - 14)
        put(a, x, y, ML if rnd.random() < 0.5 else MM, wm)
    _glyph(a, 6, WIN[1] - 6, "fire", wm)
    _glyph(a, 61, WIN[1] - 6, "air", wm)
    hermetic_frame(a, corner, edge, gem_top=True)
    panels(a, inner)
    return a


def _round(a, corner):
    a[corner < 2] = T
    a[corner == 2] = OUT


# ---------------------------------------------------------------- shiny sparkles
def add_sparkles(a: np.ndarray) -> np.ndarray:
    a = a.copy()
    for (x, y, big) in ((9, 19, True), (61, 26, False), (8, 70, False), (62, 72, True), (12, 84, False), (60, 95, False), (36, 8, False)):
        put(a, x, y, SPARK)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            put(a, x + dx, y + dy, SPARK)
        if big:
            for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
                put(a, x + dx, y + dy, SPARK)
    return a


# ---------------------------------------------------------------- the back
def card_back() -> np.ndarray:
    xs, ys, edge, corner = card_geometry()
    a = np.full((H, W), T, np.uint8)
    inside = corner >= 2
    a[inside] = OUT
    inner = (edge >= 4) & inside
    cx, cy = 35.5, 51.5                           # true centre: the back is 4-fold symmetric
    d = np.hypot((xs - cx) / 40.0, (ys - cy) / 56.0)
    val = np.clip((1.0 - d) * 2.4, 0, 2.99) + (BAYER[ys % 4, xs % 4] - 0.5) * 0.9
    # mirror the dither so the whole back stays symmetric
    val = np.maximum(val, val[:, ::-1])
    val = np.maximum(val, val[::-1, :])
    a[inner] = (BG0 + np.clip(val.astype(int), 0, 2))[inner]
    u, v = np.abs(xs - cx), np.abs(ys - cy)
    lattice = inner & ((((u + v) % 10) < 0.6) | ((np.abs(u - v) % 10) < 0.6))
    a[lattice] = MD
    dc = np.hypot(xs - cx, ys - cy)
    disc = dc < 24
    a[disc & inner] = BG0
    ring(a, cx, cy, 24.0, MM)
    ring(a, cx, cy, 21.5, MD)
    for k in range(8):                            # eight rays
        t = math.radians(k * 45 + 22.5)
        for rr in np.arange(10, 19.5, 0.5):
            put(a, cx + rr * math.cos(t), cy + rr * math.sin(t), MM)
    for k in range(16):                           # sixteen beads on the ring
        t = math.radians(k * 22.5)
        put(a, cx + 24 * math.cos(t), cy + 24 * math.sin(t), ML)
    eye = (np.hypot(xs - cx, ys - cy + 6.5) < 10.5) & (np.hypot(xs - cx, ys - cy - 6.5) < 10.5)
    a[eye] = BG1
    a[outline_of(eye)] = ML
    a[np.hypot(xs - cx, ys - cy) < 2.6] = MM
    a[np.hypot(xs - cx, ys - cy) < 1.2] = OUT
    for (sx, sy) in ((9.5, 9.5), (W - 10.5, 9.5), (9.5, H - 10.5), (W - 10.5, H - 10.5)):   # corner stars
        for (dx, dy) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2)):
            put(a, sx + dx, sy + dy, ML if abs(dx) + abs(dy) <= 1 else MM)
    a[(edge == 1) & inside] = FM
    a[(edge == 2) & inside] = FD
    a[(edge == 3) & inside] = MD
    dots = (edge == 3) & inside & ((((xs + ys) % 4)) == 0)
    a[dots] = FM
    # fold: the top-left quarter, mirrored, so rounding in the rays cannot tilt it
    q = a[:H // 2, :W // 2]
    top = np.concatenate([q, q[:, ::-1]], axis=1)
    a = np.concatenate([top, top[::-1, :]], axis=0)
    _round(a, corner)
    assert (a == a[:, ::-1]).all() and (a == a[::-1, :]).all(), "the back must be symmetric"
    return a


# ---------------------------------------------------------------- output
def to_rgba(a: np.ndarray, palette) -> Image.Image:
    lut = np.array([(*c, 255) for c in palette], np.uint8)
    lut[0, 3] = 0
    return Image.fromarray(lut[a], "RGBA")


def to_indexed(a: np.ndarray, palette) -> Image.Image:
    im = Image.fromarray(a, "P")
    im.putpalette([v for c in palette for v in c])
    im.info["transparency"] = 0
    return im


def nn(im: Image.Image, k: int) -> Image.Image:
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def master_of(card: Image.Image) -> Image.Image:
    m = Image.new("RGBA", (MASTER, MASTER), (0, 0, 0, 0))
    big = nn(card, SCALE)
    m.paste(big, ((MASTER - big.width) // 2, (MASTER - big.height) // 2), big)
    return m


def sprite(name: str) -> Image.Image:
    return Image.open(ART / f"{name}.png").convert("RGBA")


def with_daemon(card_rgba: Image.Image, card_idx: np.ndarray, palette, spr: Image.Image, keyword: str) -> Image.Image:
    a = card_idx.copy()
    draw_text_c(a, keyword, 36, KW_BAND[0] + 2, INK)
    for i, y in enumerate((PHRASE[0] + 4, PHRASE[0] + 10)):     # phrase placeholder: the words come from arcana.json
        wdt = (44, 30)[i]
        for x in range(36 - wdt // 2, 36 + wdt // 2):
            if (x // 4 + i) % 5 != 4:
                a[y:y + 1, x] = DIM
    im = to_rgba(a, palette)
    im.paste(spr, SPRITE_XY, spr)
    return im


def font(size: int):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except OSError:
        return ImageFont.load_default(size=size)


SCREEN_PAL = {
    "board0": hexrgb("#120C1C"), "board1": hexrgb("#1A1228"), "line": hexrgb("#8A82BC"),
    "line_dim": hexrgb("#4E4486"), "ink": hexrgb("#D8D2F0"), "lit": hexrgb("#F4D878"),
}


def mock_screen(back: Image.Image, turned: Image.Image | None) -> Image.Image:
    s = np.zeros((160, 240, 3), np.uint8)
    ys, xs = np.mgrid[0:160, 0:240]
    s[:] = SCREEN_PAL["board0"]
    s[((xs // 2 + ys // 2) % 2 == 0) & ((xs + ys) % 4 == 0)] = SCREEN_PAL["board1"]
    labels = ("PAST", "PRESENT", "FUTURE")
    ink = np.zeros((160, 240), np.uint8)
    draw_text_c(ink, "PAST / PRESENT / FUTURE", 120, 3, 1)
    draw_text_c(ink, "A TURN    B BACK", 120, 151, 2)
    places = []
    for i in range(3):
        px, py = 1 + i * 80, 12
        pw, ph = 78, 110
        places.append((px, py))
        for x in range(px, px + pw):
            for y in (py, py + ph - 1):
                ink[y, x] = 3
        for y in range(py, py + ph):
            for x in (px, px + pw - 1):
                ink[y, x] = 3
        for (cx, cy) in ((px, py), (px + pw - 1, py), (px, py + ph - 1), (px + pw - 1, py + ph - 1)):
            ink[cy, cx] = 4
        draw_text_c(ink, labels[i], px + pw // 2, py + ph + 3, 1 if (turned is not None and i == 1) else 2)
    s[ink == 1] = SCREEN_PAL["lit"]
    s[ink == 2] = SCREEN_PAL["ink"]
    s[ink == 3] = SCREEN_PAL["line_dim"]
    s[ink == 4] = SCREEN_PAL["line"]
    im = Image.fromarray(s, "RGB").convert("RGBA")
    for i, (px, py) in enumerate(places):
        c = turned if (turned is not None and i == 1) else back
        im.paste(c, (px + 3, py + 3), c)
    return im


# ---------------------------------------------------------------- the game's own font
# The engine's message font, read from its sheet and measured with its width table (tools/fontwidth.py), so a
# line measured here is a line the game draws. 16x16 cells, byte b at (b % 16, b // 16); index 1 ink, 2 shadow.
# The engine has no bold Latin face, so "bold" here is the glyph struck twice, one pixel apart, and measured as
# one pixel wider per letter -- a real cost the game would pay (or it sets the titles in a colour instead).
import sys as _sys
_sys.path.insert(0, str(HERE.parents[2] / "tools"))
from fontwidth import font as _engine_font  # noqa: E402

GBA_FONT = np.array(Image.open(HERE.parents[2] / "engineGba/graphics/fonts/latin_normal.png"))
GBA_W, GBA_CM = _engine_font()
MSG_W = 208
LINE_H = 16


def gw(s: str, bold=False) -> int:
    return sum(GBA_W[GBA_CM[c]] + (1 if bold else 0) for c in s)


def runs_w(runs) -> int:
    return sum(gw(s, b) for s, b, *_ in runs)


def gba_text(img: np.ndarray, s: str, x: int, y: int, ink, shadow, bold=False) -> int:
    for ch in s:
        b = GBA_CM[ch]
        adv = GBA_W[b]
        cell = GBA_FONT[(b // 16) * 16:(b // 16) * 16 + 16, (b % 16) * 16:(b % 16) * 16 + adv]
        for strike in ((0, 1) if bold else (0,)):
            for (idx, col) in ((2, shadow), (1, ink)):
                if col is None:
                    continue
                yy, xx = np.nonzero(cell == idx)
                yy, xx = yy + y, xx + x + strike
                ok = (yy >= 0) & (yy < img.shape[0]) & (xx >= 0) & (xx < img.shape[1])
                img[yy[ok], xx[ok]] = col
        x += adv + (1 if bold else 0)
    return x


def gba_runs(img, runs, x, y, shadow):
    for (s, bold, ink) in runs:
        x = gba_text(img, s, x, y, ink, shadow, bold)
    return x


def wrap(text: str, width=MSG_W) -> list[str]:
    out, cur = [], ""
    for word in text.split(" "):
        t = (cur + " " + word) if cur else word
        if gw(t) <= width:
            cur = t
        else:
            out.append(cur)
            cur = word
    return out + [cur]


def box(img, x0, y0, x1, y1, fill, border, inner=None):
    img[y0:y1 + 1, x0:x1 + 1] = border
    img[y0 + 2:y1 - 1, x0 + 2:x1 - 1] = inner if inner is not None else fill
    img[y0 + 3:y1 - 2, x0 + 3:x1 - 2] = fill
    for (cx, cy) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        img[cy, cx] = img[min(max(cy, 0), img.shape[0] - 1), cx] * 0  # square the corners off to black
    return img


def board() -> np.ndarray:
    s = np.zeros((160, 240, 3), np.uint8)
    ys, xs = np.mgrid[0:160, 0:240]
    s[:] = SCREEN_PAL["board0"]
    s[((xs // 2 + ys // 2) % 2 == 0) & ((xs + ys) % 4 == 0)] = SCREEN_PAL["board1"]
    return s


def paste(s: np.ndarray, im: Image.Image, x: int, y: int) -> np.ndarray:
    base = Image.fromarray(s, "RGB").convert("RGBA")
    base.alpha_composite(im, (x, y))
    return np.array(base.convert("RGB"))


SUBTLE_UI = dict(fill=hexrgb("#24142A"), border=hexrgb("#8A7894"), inner=hexrgb("#46284C"),
                 ink=hexrgb("#F2EAF2"), plain=hexrgb("#9A86A0"), bold=hexrgb("#F2EAF2"), shadow=hexrgb("#46284C"))
HERMETIC_UI = dict(fill=hexrgb("#2A1028"), border=hexrgb("#1F8F5F"), inner=hexrgb("#C8405A"),
                   ink=hexrgb("#F2F0E8"), plain=hexrgb("#9A86A0"), bold=hexrgb("#50C878"), shadow=hexrgb("#0F4A30"))

# The options, as lines: (text, bold, selectable). Plain words sit between the bold titles, so the menu
# reads down as the sentence it is.
COMBINED = "Both, as One"          # suggested; the alternative is "The One Thing" (the Tablet's own)
SELECTORS = {
    "subtle": ("THE SUBTLE LAYER", SUBTLE_UI, [("The Deck of Reason", True, True), ("The Deck of Instinct", True, True),
                                              ("A Combined Deck", True, True)],
               [[("The Deck of Reason / The Deck of Instinct / A Combined Deck", False, "ink")]]),
    "hermetic": ("THE HERMETIC LAYER", HERMETIC_UI, [("so,", False, False), ("The Deck Above", True, True),
                                                    ("as", False, False), ("The Deck Below", True, True),
                                                    ("or", False, False), (COMBINED, True, True)],
                 [[("so, ", False, "plain"), ("The Deck Above", True, "bold"), (", as ", False, "plain"),
                   ("The Deck Below", True, "bold"), (", or ", False, "plain"), (COMBINED, True, "bold")]]),
    "hermetic_thin": ("THE HERMETIC LAYER", HERMETIC_UI, [("so,", False, False), ("The Deck Within", True, True),
                                                         ("as", False, False), ("The Deck Without", True, True),
                                                         ("or", False, False), (COMBINED, True, True)],
                      [[("so, ", False, "plain"), ("The Deck Within", True, "bold"), (", as ", False, "plain"),
                        ("The Deck Without", True, "bold"), (", or ", False, "plain"), (COMBINED, True, "bold")]]),
}


def selector_screen(key: str, back_rgba: Image.Image, cursor: int, measures: list) -> Image.Image:
    title, ui, menu, sentence = SELECTORS[key]
    s = board()
    for i in (2, 1, 0):                                     # the deck tile: three backs, squared up
        s = paste(s, back_rgba, 4 + 2 * i, 3 + 2 * (2 - i))
    mx0, my0, mx1 = 86, 3, 236
    rows = len(menu)
    gap = LINE_H if rows > 3 else LINE_H + 8
    my1 = my0 + 10 + (rows - 1) * gap + LINE_H
    box(s, mx0, my0, mx1, my1, ui["fill"], ui["border"], ui["inner"])
    sel = [i for i, m in enumerate(menu) if m[2]]
    for i, (text, bold, selectable) in enumerate(menu):
        y = my0 + 5 + i * gap
        x = mx0 + 14 if selectable else mx0 + 8
        gba_text(s, text, x, y, ui["bold"] if bold else ui["plain"], ui["shadow"], bold)
        measures.append((key, "menu", text, gw(text, bold), mx1 - 3 - (mx0 + 14)))
        if i == sel[cursor]:                                # the cursor, a small arrow
            for r in range(7):
                w = 4 - abs(r - 3)
                s[y + 3 + r, mx0 + 6:mx0 + 6 + w] = ui["bold"]
    bx0, by0, bx1, by1 = 8, 120, 231, 151                   # the message box (208px inside) names the book
    box(s, bx0, by0, bx1, by1, ui["fill"], ui["border"], ui["inner"])
    gba_text(s, title, 120 - gw(title, True) // 2, by0 + 8, ui["ink"], ui["shadow"], True)
    measures.append((key, "box", title, gw(title, True), MSG_W))
    for runs in sentence:                                   # the sentence on one line: measured, not drawn
        r = [(t, b, ui[c]) for (t, b, c) in runs]
        measures.append((key, "1-line", "".join(t for t, *_ in runs), runs_w(r), MSG_W))
    return Image.fromarray(s, "RGB")


SAMPLE_WORDS = ("Something in you lies still while the day hurries past it. Do not shake it awake. Behind its "
                "closed eyes a road is being drawn, and when it rises it will already know the way.")


def reading_screen(card_rgba: Image.Image, keyword: str, place: int, measures: list) -> Image.Image:
    """Page two of a turned card: the phrase has 4-6 lines, so it gets the whole screen's width (208px),
    under a header naming the card; the spread's three places run along the foot, this one lit."""
    s = board()
    ui = SUBTLE_UI
    small = card_rgba.crop((4, 32, 68, 58))                 # the daemon's face, from its window
    box(s, 4, 1, 235, 31, ui["fill"], ui["border"], ui["inner"])
    s = paste(s, small, 7, 4)
    gba_text(s, keyword, 80, 3, ui["ink"], ui["shadow"], True)
    gba_text(s, "REASON", 80, 16, ui["plain"], ui["shadow"])
    lines = wrap(SAMPLE_WORDS)
    assert 4 <= len(lines) <= 6, lines
    box(s, 4, 34, 235, 34 + 9 + 6 * LINE_H, ui["fill"], ui["border"], ui["inner"])
    for i, ln in enumerate(lines):
        gba_text(s, ln, 16, 39 + i * LINE_H, ui["ink"], ui["shadow"])
        measures.append(("reading", "phrase", ln, gw(ln), MSG_W))
    for i, lab in enumerate(("Past", "Present", "Future")):
        cx = 40 + i * 80
        lit = i == place
        gba_text(s, lab, cx - gw(lab) // 2, 144 + 1, SCREEN_PAL["lit"] if lit else SCREEN_PAL["line_dim"], None, lit)
    return Image.fromarray(s, "RGB"), len(lines)


def main() -> None:
    faces = {"reason": face_reason(), "instinct": face_instinct(), "above": face_above(), "below": face_below()}
    family = {"reason": "reason", "instinct": "instinct", "above": "spellcraft", "below": "spellcraft"}
    back = card_back()
    counts, cards = {}, {}

    def save(name, a, palette):
        to_indexed(a, palette).save(HERE / f"frame_{name}.png", transparency=0)
        rgba = to_rgba(a, palette)
        master_of(rgba).save(HERE / f"master_{name}.png")
        used = sorted(set(np.unique(a).tolist()) - {T})
        counts[name] = len(set(palette[i] for i in used))
        return rgba

    pals = {}
    for f in list(faces):
        pals[f] = PALETTES[family[f]]
        pals[f + "_shiny"] = PALETTES[family[f] + "_shiny"]
        cards[f] = save(f, faces[f], pals[f])
        faces[f + "_shiny"] = add_sparkles(faces[f])
        cards[f + "_shiny"] = save(f + "_shiny", faces[f + "_shiny"], pals[f + "_shiny"])
    pb = list(PALETTES["spellcraft"])
    pb[PULSE] = PULSE_BLUE
    for f in ("above", "below"):
        to_indexed(faces[f], pb).save(HERE / f"frame_{f}_pulse_blue.png", transparency=0)
    back_rgba = to_rgba(back, BACK_PAL)
    to_indexed(back, BACK_PAL).save(HERE / "back.png", transparency=0)
    master_of(back_rgba).save(HERE / "master_back.png")
    counts["back"] = len(set(BACK_PAL[i] for i in set(np.unique(back).tolist()) - {T}))

    daydream, phoenix = sprite("daydream"), sprite("phoenix")
    sample = {"reason": (daydream, "XVIII DREAMING"), "instinct": (daydream, "XVIII DREAMING"),
              "above": (phoenix, "XX INVOCATION"), "below": (phoenix, "XX INVOCATION")}
    filled = {}
    for k in cards:
        spr, kw = sample[k.replace("_shiny", "")]
        filled[k] = with_daemon(None, faces[k], pals[k], spr, kw)
    for f in ("above", "below"):
        filled[f + "_blue"] = with_daemon(None, faces[f], pb, phoenix, "XX INVOCATION")

    mock_down = mock_screen(back_rgba, None)
    mock_up = mock_screen(back_rgba, filled["reason"])
    mock_down.save(HERE / "mock_spread.png")
    mock_up.save(HERE / "mock_spread_turned.png")
    measures = []
    sel = {k: selector_screen(k, back_rgba, 0, measures) for k in SELECTORS}
    for k, im in sel.items():
        im.save(HERE / f"mock_select_{k}.png")
    reading, nlines = reading_screen(filled["reason"], "XVIII DREAMING", 1, measures)
    reading.save(HERE / "mock_reading.png")
    over = [m for m in measures if m[3] > m[4] and m[1] != "1-line"]
    assert not over, over

    # ---------------- sheet2
    G = 24
    f_big, f_mid, f_small = font(22), font(18), font(14)
    SW = max(G + 4 * (MASTER + G), G + 3 * (720 + G) + 60)
    SH = 3400
    sheet = Image.new("RGBA", (SW, SH), (30, 28, 36, 255))
    dr = ImageDraw.Draw(sheet)
    hi, lo = (236, 230, 240), (160, 150, 170)
    dr.text((G, 12), "T-509  DRAFT  round two  --  THE HERMETIC LAYER's pair: The Deck Above & The Deck Below "
            "(replacing SPELLCRAFT's one face)", fill=hi, font=f_big)
    y = 52
    dr.text((G, y), f"ABOVE  (top-down: one star, rays coming down, a pattern arriving whole; fire and air at the foot)   "
            f"normal {counts['above']} / shiny {counts['above_shiny']} colours + transparent", fill=hi, font=f_mid)
    dr.text((G, y + 24), f"BELOW  (bottom-up: courses laid from the base, the top one unfinished, roots, strata of time; "
            f"water and earth at the crown)   normal {counts['below']} / shiny {counts['below_shiny']} colours + transparent",
            fill=hi, font=f_mid)
    yy = y + 56
    for i, k in enumerate(("above", "below", "above_shiny", "below_shiny")):
        x = G + i * (MASTER + G)
        sheet.alpha_composite(master_of(filled[k]), (x, yy))
        dr.text((x + 6, yy + 4), "master" + (", shiny (1 in 16)" if "shiny" in k else ""), fill=lo, font=f_small)
    yy += MASTER + 10
    dr.text((G, yy), "GBA 1x and 2x  --  the pair side by side, then the pulse (palette index 14 only): red #C8405A, blue #4F6BD8",
            fill=lo, font=f_small)
    yy += 22
    x = G
    for k in ("above", "below", "above_shiny", "below_shiny"):
        sheet.alpha_composite(filled[k], (x, yy))
        x += 72 + 12
    x += 20
    for k in ("above", "below", "above_shiny", "below_shiny", "above_blue", "below_blue"):
        sheet.alpha_composite(nn(filled[k], 2), (x, yy))
        x += 144 + 12
    yy += 208 + 30
    dr.text((G, yy), "The whole set at 2x: REASON, INSTINCT (unchanged), ABOVE, BELOW, and the one back (unchanged)", fill=hi, font=f_mid)
    yy += 28
    x = G
    for k in ("reason", "instinct", "above", "below"):
        sheet.alpha_composite(nn(filled[k], 2), (x, yy))
        x += 144 + 16
    sheet.alpha_composite(nn(back_rgba, 2), (x, yy))
    yy += 208 + 30
    dr.text((G, yy), "Deck selectors, GBA 240x160 at 3x, in the game's own font (bold = struck twice, +1px a letter). "
            "No sentence fits one 208px line, so the menu stacks it and reads down as the sentence.", fill=hi, font=f_mid)
    yy += 28
    for i, k in enumerate(("subtle", "hermetic", "hermetic_thin")):
        x = G + i * (720 + G)
        lab = {"subtle": "THE SUBTLE LAYER", "hermetic": "THE HERMETIC LAYER",
               "hermetic_thin": "THE HERMETIC LAYER, in the thin half-hour"}[k]
        dr.text((x, yy), lab, fill=lo, font=f_small)
        sheet.alpha_composite(nn(sel[k].convert("RGBA"), 3), (x, yy + 20))
    yy += 20 + 480 + 30
    dr.text((G, yy), f"Where the phrase goes: a second page. A turned card's 2-3 sentences ({len(SAMPLE_WORDS)} characters "
            f"here) wrap to {nlines} lines at 208px:\ntoo many for a box under a 104px card, so A on a turned card opens this page "
            "and B returns to the spread.", fill=hi, font=f_mid)
    yy += 48
    sheet.alpha_composite(nn(mock_up, 3), (G, yy + 20))
    dr.text((G, yy), "the spread, PRESENT turned", fill=lo, font=f_small)
    sheet.alpha_composite(nn(reading.convert("RGBA"), 3), (G + 720 + G, yy + 20))
    dr.text((G + 720 + G, yy), "A: its page (sample words, NOT the card's -- those come from arcana.json)", fill=lo, font=f_small)
    tx = G + 2 * (720 + G)
    dr.text((tx, yy), "every line measured (engine widths, px)", fill=lo, font=f_small)
    ty = yy + 22
    for (k, where, text, w, lim) in measures:
        dr.text((tx, ty), f"{w:3d}/{lim}  {where:6s} {text}", fill=hi if w <= lim else (255, 120, 90), font=font(12))
        ty += 16
    yy += 20 + 480 + 20
    dr.text((G, yy), "Sample: RED12345, 2026-11-01 -- subtle XVIII DREAMING (DAYDREAM), hermetic XX INVOCATION (PHOENIX). "
            f"Combined hermetic deck: '{COMBINED}' suggested; 'The One Thing' the alternative. Every word DRAFT.",
            fill=lo, font=f_small)
    sheet = sheet.crop((0, 0, SW, yy + 30))
    sheet.save(HERE / "sheet2.png")
    for k, v in counts.items():
        print(f"{k:16s} {v:2d} colours (+ transparent)")
    for m in measures:
        print(f"{m[3]:3d}/{m[4]}  {m[0]:14s} {m[1]:6s} {m[2]}")
    print("phrase lines:", nlines)


if __name__ == "__main__":
    main()

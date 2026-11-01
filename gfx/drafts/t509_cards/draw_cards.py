#!/usr/bin/env python3
"""T-509 DRAFT: the tarot card frames, drawn for the GBA.

Three faces -- REASON (a green circuit), INSTINCT (a gold net), SPELLCRAFT
(emerald on the breathing purple) -- each with a shiny palette (1 in 16), and
one shared back that never shows the type.

How it is drawn: every card is a 72x104 grid of palette indices (9x13 tiles,
4bpp). Index 0 is transparent; each frame uses at most 15 colours more, so it is
one 16-colour BG palette. The daemon's 64x64 front sprite sits over it in its own
palette (an OBJ, or a second BG palette), so the frame never shares its colours.

  * shiny is a PALETTE SWAP of the same tiles, plus a few sparkle pixels on
    index 15 (a handful of extra tiles);
  * SPELLCRAFT's pulse ring is index 14 alone, so the "breathing" is one palette
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


# ---------------------------------------------------------------- SPELLCRAFT
GLYPHS = {
    "fire":  ["00100", "01010", "01010", "10001", "11111"],
    "water": ["11111", "10001", "01010", "01010", "00100"],
    "sun":   ["01110", "10001", "10101", "10001", "01110"],
    "moon":  ["00110", "01100", "01000", "01100", "00110"],
}


def face_spellcraft() -> np.ndarray:
    a, inner = base_card(glow_cy=46)
    xs, ys, edge, corner = card_geometry()
    wm = window_mask()
    cx, cy = 35.5, (WIN[0] + WIN[1]) / 2           # the circle sits on the daemon
    ring(a, cx, cy, 30.5, MM, wm)
    ring(a, cx, cy, 28.5, PULSE, wm)               # index 14: the breath
    ring(a, cx, cy, 26.0, MD, wm)
    ring(a, cx, cy, 15.0, MD, wm)
    pts = [(cx + 24.5 * math.sin(math.radians(k * 72)), cy - 24.5 * math.cos(math.radians(k * 72))) for k in range(5)]
    for k in range(5):                             # the star, in ink
        p, q = pts[k], pts[(k + 2) % 5]
        line(a, p[0], p[1], q[0], q[1], MM, wm)
    for k in range(12):                            # twelve ticks between the rings
        t = math.radians(k * 30 + 15)
        put(a, cx + 29.5 * math.sin(t), cy - 29.5 * math.cos(t), ML, wm)
    for (gx, gy, g) in ((5, WIN[0] + 1, "fire"), (62, WIN[0] + 1, "water"),
                        (5, WIN[1] - 5, "sun"), (62, WIN[1] - 5, "moon")):
        for r, row in enumerate(GLYPHS[g]):
            for c, bit in enumerate(row):
                if bit == "1":
                    put(a, gx + c, gy + r, ML, wm)
    # the frame: emerald, a lit inner line, and a pulse gem top and bottom
    a[(edge == 1) & (corner >= 2)] = FM
    a[(edge == 2) & (corner >= 2)] = FD
    a[(edge == 3) & (corner >= 2)] = FL
    for (gx, gy) in ((35, 1), (35, H - 4)):
        for dy in range(3):
            for dx in range(4):
                if (dy == 1) or dx in (1, 2):
                    put(a, gx - 1 + dx, gy + dy, PULSE)
        put(a, gx - 1, gy + 1, OUT)
        put(a, gx + 2, gy + 1, OUT)
    for (px, py) in ((2, 2), (W - 3, 2), (2, H - 3), (W - 3, H - 3)):
        put(a, px, py, FL)
    _round(a, corner)
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


def main() -> None:
    faces = {"reason": face_reason(), "instinct": face_instinct(), "spellcraft": face_spellcraft()}
    back = card_back()
    counts = {}

    def save(name, a, palette):
        to_indexed(a, palette).save(HERE / f"frame_{name}.png", transparency=0)
        rgba = to_rgba(a, palette)
        master_of(rgba).save(HERE / f"master_{name}.png")
        used = sorted(set(np.unique(a).tolist()) - {T})
        counts[name] = len(set(palette[i] for i in used))
        return rgba

    cards = {}
    for f, a in list(faces.items()):
        cards[f] = save(f, a, PALETTES[f])
        sh = add_sparkles(a)
        cards[f + "_shiny"] = save(f + "_shiny", sh, PALETTES[f + "_shiny"])
        faces[f + "_shiny"] = sh
    pb = list(PALETTES["spellcraft"])
    pb[PULSE] = PULSE_BLUE
    to_indexed(faces["spellcraft"], pb).save(HERE / "frame_spellcraft_pulse_blue.png", transparency=0)
    back_rgba = to_rgba(back, BACK_PAL)
    to_indexed(back, BACK_PAL).save(HERE / "back.png", transparency=0)
    master_of(back_rgba).save(HERE / "master_back.png")
    counts["back"] = len(set(BACK_PAL[i] for i in set(np.unique(back).tolist()) - {T}))

    daydream, phoenix = sprite("daydream"), sprite("phoenix")
    sample = {"reason": (daydream, "XVIII DREAMING"), "instinct": (daydream, "XVIII DREAMING"),
              "spellcraft": (phoenix, "XX INVOCATION")}
    filled = {}
    for k in cards:
        f = k.replace("_shiny", "")
        spr, kw = sample[f]
        filled[k] = with_daemon(cards[k], faces[k], PALETTES[k], spr, kw)
    filled["spellcraft_blue"] = with_daemon(None, faces["spellcraft"], pb, phoenix, "XX INVOCATION")

    mock_down = mock_screen(back_rgba, None)
    mock_up = mock_screen(back_rgba, filled["reason"])
    mock_down.save(HERE / "mock_spread.png")
    mock_up.save(HERE / "mock_spread_turned.png")

    # ---------------- the sheet
    G = 24
    gx = G + MASTER + G + MASTER + 40
    SW = max(gx + 3 * 144 + 2 * 16 + G, G + 2 * (720 + G) + 240 + G)
    rows_h = [44] + [MASTER + 40] * 4 + [480 + 70]
    SH = sum(rows_h) + 120
    sheet = Image.new("RGBA", (SW, SH), (30, 28, 36, 255))
    dr = ImageDraw.Draw(sheet)
    f_big, f_mid, f_small = font(26), font(18), font(14)
    dr.text((G, 12), "T-509  DRAFT  tarot card frames  --  72x104 (9x13 tiles), 4bpp, one 16-colour palette per frame; master = 4x on 512",
            fill=(236, 230, 240), font=f_mid)
    y = 44 + 16
    names = {"reason": "REASON  -  green circuit", "instinct": "INSTINCT  -  gold net",
             "spellcraft": "SPELLCRAFT  -  emerald on the breathing purple"}
    for f in ("reason", "instinct", "spellcraft"):
        dr.text((G, y), f"{names[f]}     (normal {counts[f]} colours, shiny {counts[f + '_shiny']} colours + transparent)",
                fill=(236, 230, 240), font=f_mid)
        yy = y + 30
        sheet.alpha_composite(master_of(filled[f]), (G, yy))
        sheet.alpha_composite(master_of(filled[f + "_shiny"]), (G + MASTER + G, yy))
        dr.text((G + 6, yy + 4), "master", fill=(160, 150, 170), font=f_small)
        dr.text((G + MASTER + G + 6, yy + 4), "master, shiny (1 in 16)", fill=(160, 150, 170), font=f_small)
        dr.text((gx, yy), "GBA 1x", fill=(160, 150, 170), font=f_small)
        sheet.alpha_composite(filled[f], (gx, yy + 22))
        sheet.alpha_composite(filled[f + "_shiny"], (gx + 72 + 16, yy + 22))
        dr.text((gx, yy + 140), "GBA 2x (preview)", fill=(160, 150, 170), font=f_small)
        sheet.alpha_composite(nn(filled[f], 2), (gx, yy + 162))
        sheet.alpha_composite(nn(filled[f + "_shiny"], 2), (gx + 160, yy + 162))
        if f == "spellcraft":
            sheet.alpha_composite(nn(filled["spellcraft_blue"], 2), (gx + 320, yy + 162))
            dr.text((gx, yy + 380), "pulse = palette index 14 only:\nred #C8405A <-> blue #4F6BD8\n(one palette write per beat)",
                    fill=(160, 150, 170), font=f_small)
        y += MASTER + 40
    dr.text((G, y), f"THE BACK  -  shared by all three decks, its own palette ({counts['back']} colours), 4-fold symmetric, no type in it",
            fill=(236, 230, 240), font=f_mid)
    yy = y + 30
    sheet.alpha_composite(master_of(back_rgba), (G, yy))
    for i, f in enumerate(("REASON", "INSTINCT", "SPELLCRAFT")):
        x = G + MASTER + G + i * (72 * 2 + 24)
        dr.text((x, yy), f"{f} deck", fill=(160, 150, 170), font=f_small)
        sheet.alpha_composite(nn(back_rgba, 2), (x, yy + 22))
    dr.text((G + MASTER + G, yy + 240), "the same bytes for every deck (back.png)", fill=(160, 150, 170), font=f_small)
    sheet.alpha_composite(back_rgba, (gx, yy + 22))
    y += MASTER + 40
    dr.text((G, y), "GBA screen 240x160 (shown 3x)  -  PAST / PRESENT / FUTURE face down, then PRESENT turned",
            fill=(236, 230, 240), font=f_mid)
    yy = y + 30
    sheet.alpha_composite(nn(mock_down, 3), (G, yy))
    sheet.alpha_composite(nn(mock_up, 3), (G + 720 + G, yy))
    sheet.alpha_composite(mock_down, (G + 2 * (720 + G), yy))
    sheet.alpha_composite(mock_up, (G + 2 * (720 + G), yy + 180))
    dr.text((G + 2 * (720 + G), yy + 350), "1x", fill=(160, 150, 170), font=f_small)
    dr.text((G, yy + 490), "sample: RED12345, 2026-11-01  -  subtle XVIII DREAMING (DAYDREAM), spellcraft XX INVOCATION (PHOENIX).  "
            "Phrase lines are placeholders; the words come from arcana.json.", fill=(160, 150, 170), font=f_small)
    sheet = sheet.crop((0, 0, SW, yy + 520))
    sheet.save(HERE / "sheet.png")
    for k, v in counts.items():
        print(f"{k:18s} {v:2d} colours (+ transparent)")


if __name__ == "__main__":
    main()

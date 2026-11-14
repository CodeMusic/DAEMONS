#!/usr/bin/env python3
"""T-523: the text window frames and the "more text" arrow -- every dialogue box, sign and menu border, drawn anew.

    python3 tools/gbaframes.py                          # report: the engine's frame files, the slot contract each
                                                        #   drop-in keeps, and each direction's colours measured
                                                        #   against the type hues (9.4)
    python3 tools/gbaframes.py --draft [DIR]            # draw the three directions, the ten menu frames and the
                                                        #   arrow into DIR (gfx/drafts/t523_frames/), the contact
                                                        #   sheet and a mock screen per direction at real size
    python3 tools/gbaframes.py --write --approved --main A   # write the chosen direction into the engine.
                                                        #   Refuses without --approved, and without --main.
    python3 tools/gbaframes.py --std-draft [DIR]        # T-554: the std frame (std.png, LoadStdWindowGfx's) in its two
                                                        #   versions into DIR (gfx/drafts/t554_menus/std/)
    python3 tools/gbaframes.py --write --approved --std 1|2  # write it; refuses until APPROVED_STD names the pick

DRAFT, 2026-11-06, the user away ("Text boxes first", from the vanilla-art census). Every pixel here is drawn in code,
on the tile grid, from scratch: no AI image, nothing traced. The engine's own files are read only to keep what this does
not own (the tiles the frames do not use, the text colours in slots 1-9) byte for byte.

WHAT THE ENGINE DRAWS (src/new_menu_helpers.c, src/text_window.c, src/text.c)
  THE MESSAGE BOX   graphics/text_window/menu_message.png (48x24, 18 tiles; tiles 0-6 and 8-13 are the frame),
                    palette stdpal_0.pal in BG palette 15. WindowFunc_DrawDialogueFrame lays it round a 26x4 window at
                    (2,15): a top row 0 1 2..2 3 4, side rows 5 6 | 8 9 and 10 11 | 12 13, and the bottom half the same
                    tiles V-flipped -- so the frame is mirrored top to bottom by the hardware, the top edge is tile 2
                    repeated (anything along it repeats every 8px), and the left and right sides are separate tiles (a
                    glyph may sit on one side only). 240x48 on screen: rows 14-19, edge to edge.
  THE SIGN          signpost.png (40x32, the same tile numbers 0-13 in the same places), stdpal_1.pal.
  THE TEN FRAMES    type1..10.png (24x24, 3x3 tiles, palette in the PNG): OPTIONS' FRAME, round every menu.
  THE ARROW         graphics/fonts/down_arrows.png (128x16): four 16px cells read at x 0, 16, 32, 16 (a bounce), a
                    10x12 rect blitted into the text window, so it is drawn in the TEXT palette's slots -- 4 on 2 (the
                    normal arrow) in x 0-63, 2 on 9 (the dark one) in x 64-127. down_arrow_3/4.png are the same arrow as a
                    16x16 cursor sprite (the list menus).

THE SLOT CONTRACT EACH DROP-IN KEEPS (why a frame is not just a picture)
  slot 0 transparent; 1 the paper (PIXEL_FILL(1), and the text's ground); 2-9 the inks and the text colours.
  MESSAGE BOX, palette 15: 10 is T-459's purple at run time (never drawn in); 11 stays stdpal_0's colour (the MAIL
  prints in 10 and 11) and is drawn only as the inner-corner flecks, which take a holiday's month colour (T-481 B);
  14 is the weekday's trim at run time -- here THE CORNER GLYPH, so the glyph wears the day; 12, 13 and 15 are the
  frame, which the hour tints. So daemons_calendar_pane.h's text-box row (14, 11, 0xF800) holds unchanged.
  THE TEN FRAMES: 15 outline, 14 band, 13 band light, 10 band shade, 11 the inner bevel, 12 the eight inner-corner
  pixels -- vanilla style 1's contract, now in all ten, so T-481 B's START day and holiday reach every style: after a
  --write, re-run tools/gbacalendar_ui.py --write --approved (its styleMask is measured, and becomes 0x3FF).
  THE ARROW keeps vanilla's indices (4/2 and 2/9), so it is coloured by whatever text palette it lands in.

THE THREE DIRECTIONS for the message box (and its sign):
  A  TERMINAL   a slate rule, 45-degree corners, a corner bracket in the day's trim and a prompt chevron at the left
  B  MANUSCRIPT iron-gall ink on vellum, a gilt dotted rule, a rubric quatrefoil at each corner
  C  CIRCUIT    a dark substrate with one copper trace round it, a pad every 8px, an LED at each 45-degree bend
"""
import argparse, importlib.util, math, os, shutil, struct, sys, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
TW = os.path.join(GBA, "graphics/text_window")
FONTS = os.path.join(GBA, "graphics/fonts")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t523_frames")
SCRATCH_BG = None                    # --bg PNG: a 240x160 screen to lay the mock box over

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--bg")
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
ap.add_argument("--over-later-work", action="store_true", help="accepted so check_generators --writes really runs the write")
ap.add_argument("--main", choices="ABC")
ap.add_argument("--std-draft", nargs="?", const=os.path.join(ROOT, "gfx", "drafts", "t554_menus", "std"),
                help="T-554: draw the std frame's versions into DIR (std.png, and stdpal_3.pal where one moves)")
ap.add_argument("--std", choices=("1", "2"), help="T-554: with --write --approved, write this std version (APPROVED_STD)")
A = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])

MAIN_RECOMMENDED = "A"
APPROVED = "A"                       # the user's pick, 2026-11-06: A TERMINAL, and the whole family with it
#  T-554: the std frame, graphics/text_window/std.png. The user, 2026-11-14 (multiple choice): version 1, TERMINAL
#  in stdpal_3 -- std.png only, no palette moves. --write --approved --std 1 writes it.
APPROVED_STD = "1"
STD_RECOMMENDED = "1"


def q5(c):
    """A colour as the GBA keeps it (five bits a channel), shown back at 8."""
    return tuple((v >> 3) << 3 for v in c)


# ============================================================================================ the engine's own files
def load_png(p):
    import gbafont
    w, h, bd, plte, px = gbafont.png_load(p)
    pal = [tuple(plte[i:i + 3]) for i in range(0, len(plte), 3)]
    return w, h, bd, pal, px


def save_png(p, px, pal, bd=4):
    import gbafont
    pal = (list(pal) + [(0, 0, 0)] * 16)[:16]
    gbafont.png_save(p, len(px[0]), len(px), bd, b"".join(bytes(q5(c)) for c in pal), px)


def jasc(p):
    w = open(p).read().split()
    n = int(w[2])
    v = list(map(int, w[3:3 + 3 * n]))
    return [tuple(v[3 * i:3 * i + 3]) for i in range(n)]


def write_jasc(cols, p):
    with open(p, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(cols))
        for c in cols:
            f.write("%d %d %d\n" % q5(c))


def tile(px, i, per_row):
    x0, y0 = (i % per_row) * 8, (i // per_row) * 8
    return [row[x0:x0 + 8] for row in px[y0:y0 + 8]]


def put_tile(px, i, per_row, t):
    x0, y0 = (i % per_row) * 8, (i // per_row) * 8
    for y in range(8):
        px[y0 + y][x0:x0 + 8] = t[y]


# ========================================================================================= the message box's shape
# A frame is drawn as its TOP-HALF QUARTER: 40 x 24, the five top tiles (0 1 2 3 4) and the two side rows (5 6 . 8 9,
# 10 11 . 12 13). x 0-15 is the screen's x 0-15, x 16-23 the repeated tile 2 (and the window below it), x 24-39 the
# screen's x 224-239. The hardware mirrors it top to bottom.
QW, QH = 40, 24
DLG_TILES = {0: (0, 0), 1: (8, 0), 2: (16, 0), 3: (24, 0), 4: (32, 0),
             5: (0, 8), 6: (8, 8), 8: (24, 8), 9: (32, 8),
             10: (0, 16), 11: (8, 16), 12: (24, 16), 13: (32, 16)}


def ring_d(x, y, w, cut):
    """How far (x, y) lies inside the frame's outer edge: the nearest of the left, right and top edges, and the
    45-degree cut across each corner (cut 0: square)."""
    xx = min(x, w - 1 - x)
    return min(xx, y, (xx + y - cut) if cut else 99)


def quarter(direction, sign=False):
    g = [[0] * QW for _ in range(QH)]
    st = STYLES[direction]
    rings = st["sign_rings"] if sign else st["rings"]
    paper_at = len(rings)
    for y in range(QH):
        for x in range(QW):
            d = ring_d(x, y, QW, st["cut"])
            if d < 0:
                continue
            if d < paper_at:
                g[y][x] = rings[d]
            else:
                g[y][x] = 1
    st["motif"](g, sign)
    # the inner-corner flecks (slot 11): one pixel just inside each inner corner
    k = paper_at
    for x in (k, QW - 1 - k):
        if g[k][x] == 1:
            g[k][x] = 11
    for y in range(8, QH):                     # the window's column stays paper
        for x in range(16, 24):
            g[y][x] = 1
    return g


def _put(g, x, y, v):
    if 0 <= x < QW and 0 <= y < QH and g[y][x] != 0:
        g[y][x] = v


def _side_both(g, x, y, v):
    """A pixel at x on the left, and its mirror on the right."""
    _put(g, x, y, v)
    _put(g, QW - 1 - x, y, v)


def motif_terminal(g, sign):
    # the corner bracket, in slot 14 (the day's trim): an L three long each way, just inside the outline
    L = [(4, 3), (5, 3), (6, 3), (7, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
    for x, y in L:
        _side_both(g, x, y, 14)
    if not sign:
        # the prompt: a chevron on the left side, its point at the side's foot, mirrored by the hardware into a '>'
        for x, y in ((8, 20), (9, 21), (10, 22), (11, 23), (9, 20), (10, 21), (11, 22), (12, 23)):
            _put(g, x, y, 12 if (x + y) % 2 == 0 else 13)
        # and the cursor block opposite, on the right
        for y in (21, 22, 23):
            for x in (QW - 1 - 9, QW - 1 - 10):
                _put(g, x, y, 13)
    else:
        # a sign is a plate: four rivets, one in each corner's bracket
        _side_both(g, 6, 6, 15)


def motif_manuscript(g, sign):
    # the gilt dotted rule (slot 13) on ring 3, every 4px along the top and down each side
    for y in range(QH):
        for x in range(QW):
            if g[y][x] == 0:
                continue
            d = ring_d(x, y, QW, STYLES["B"]["cut"])
            if d == 3:
                along = x if y == 3 else y
                g[y][x] = 13 if along % 4 == 1 else 12
    # the rubric quatrefoil at each corner (slot 14, the day's trim), outlined in ink
    cx, cy = 4, 4
    foil = {(0, -2): 14, (-2, 0): 14, (2, 0): 14, (0, 2): 14, (0, 0): 13,
            (-1, -1): 15, (1, -1): 15, (-1, 1): 15, (1, 1): 15,
            (0, -1): 14, (-1, 0): 14, (1, 0): 14, (0, 1): 14}
    for (dx, dy), v in foil.items():
        _side_both(g, cx + dx, cy + dy, v)
    if sign:
        # a sign is a bookplate: a second ink rule inside the first
        for y in range(QH):
            for x in range(QW):
                if g[y][x] != 0 and ring_d(x, y, QW, STYLES["B"]["cut"]) == 6 and g[y][x] == 1:
                    g[y][x] = 15 if (x + y) % 2 else 12


def motif_circuit(g, sign):
    cut = STYLES["C"]["cut"]
    # the pads: every 8px along the trace (ring 3), a 3x3 pad, solder (12) in the middle
    for y in range(QH):
        for x in range(QW):
            if g[y][x] == 0:
                continue
            d = ring_d(x, y, QW, cut)
            xx = min(x, QW - 1 - x)
            if d == 3 and y == 3 and x % 8 == 4 and xx > 6:
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        _put(g, x + dx, y + dy, 13)
                _put(g, x, y, 12)
            if d == 3 and xx == 3 and y % 8 == 4 and y > 6:
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        _side_both(g, 3 + dx, y + dy, 13)
                _side_both(g, 3, y, 12)
    # the LED at the 45-degree bend (slot 14, the day's trim)
    for x, y in ((5, 4), (4, 5), (5, 5), (4, 4)):
        _side_both(g, x, y, 14)
    if not sign:
        # a via off the trace into the paper at the left: the line the words come in on
        # (on the side's last row, so the hardware's mirror makes it one 2px line, not two)
        for x in range(7, 12):
            _put(g, x, 23, 13)
        _put(g, 12, 23, 12)
        _put(g, 12, 22, 13)
        _put(g, 13, 23, 13)


# palettes: {slot: colour}; anything not named stays the engine's
STYLES = {
    "A": dict(name="TERMINAL", cut=2,
              rings=[0, 15, 13, 13, 12, 15],
              sign_rings=[0, 15, 13, 13, 13, 12, 15],
              pal={12: (176, 192, 204), 13: (88, 104, 120), 14: (112, 208, 184), 15: (32, 40, 52)},
              sign_pal={11: (224, 228, 232), 12: (200, 196, 184), 13: (136, 128, 116), 14: (232, 200, 120),
                        15: (48, 44, 40)},
              motif=motif_terminal,
              said="a slate rule cut at 45 degrees, a corner bracket in the day's trim, a prompt chevron at the "
                   "left and a cursor block at the right"),
    "B": dict(name="MANUSCRIPT", cut=3,
              rings=[0, 15, 12, 12, 12, 15],
              sign_rings=[0, 15, 12, 12, 12, 15],
              pal={12: (236, 224, 196), 13: (196, 156, 84), 14: (168, 56, 48), 15: (64, 48, 40)},
              sign_pal={11: (232, 224, 208), 12: (216, 184, 136), 13: (160, 112, 64), 14: (120, 72, 136),
                        15: (64, 40, 24)},
              motif=motif_manuscript,
              said="iron-gall ink on a vellum band, a gilt dotted rule, a rubric quatrefoil at each corner"),
    "C": dict(name="CIRCUIT", cut=4,
              rings=[0, 15, 15, 13, 15, 15, 13],
              sign_rings=[0, 15, 15, 13, 15, 15, 13],
              pal={12: (232, 204, 140), 13: (176, 128, 80), 14: (104, 216, 168), 15: (28, 36, 40)},
              sign_pal={11: (224, 232, 224), 12: (232, 220, 160), 13: (192, 168, 96), 14: (232, 112, 88),
                        15: (24, 48, 40)},
              motif=motif_circuit,
              said="a dark substrate with one copper trace round it, a solder pad every 8px, an LED at each "
                   "45-degree bend, a via leading into the words"),
}


# ================================================================================================ the ten frames
FAMILY = [
    # name, motif, {10 shade, 11 bevel, 12 inner corners, 13 light, 14 band, 15 outline}
    ("TERMINAL", "bracket", {10: (64, 76, 92), 11: (176, 192, 204), 12: (112, 208, 184), 13: (128, 144, 160),
                             14: (88, 104, 120), 15: (32, 40, 52)}),
    ("MANUSCRIPT", "dots", {10: (200, 184, 152), 11: (64, 48, 40), 12: (168, 56, 48), 13: (196, 156, 84),
                            14: (236, 224, 196), 15: (64, 48, 40)}),
    ("CIRCUIT", "trace", {10: (232, 204, 140), 11: (176, 128, 80), 12: (104, 216, 168), 13: (176, 128, 80),
                          14: (28, 36, 40), 15: (16, 20, 24)}),
    ("PHOSPHOR", "scan", {10: (24, 56, 52), 11: (136, 216, 196), 12: (224, 248, 240), 13: (72, 152, 136),
                          14: (32, 80, 72), 15: (12, 24, 24)}),
    ("AMBER", "scan", {10: (72, 40, 16), 11: (240, 184, 96), 12: (255, 232, 176), 13: (200, 128, 48),
                       14: (112, 64, 24), 15: (32, 20, 12)}),
    ("VELLUM", "hair", {10: (220, 212, 196), 11: (120, 104, 88), 12: (168, 152, 128), 13: (244, 240, 228),
                        14: (236, 228, 212), 15: (88, 76, 64)}),
    ("BRASS", "dots", {10: (136, 96, 40), 11: (96, 64, 24), 12: (255, 240, 184), 13: (240, 208, 120),
                       14: (208, 168, 80), 15: (64, 40, 16)}),
    ("NIGHT", "stars", {10: (24, 24, 56), 11: (152, 160, 208), 12: (232, 232, 255), 13: (72, 72, 128),
                        14: (40, 40, 88), 15: (12, 12, 32)}),
    ("SALT", "double", {10: (176, 188, 200), 11: (120, 136, 152), 12: (64, 80, 96), 13: (240, 244, 248),
                        14: (216, 224, 232), 15: (96, 108, 124)}),
    ("HERMETIC", "sigil", {10: (96, 80, 104), 11: (184, 168, 192), 12: (232, 216, 160), 13: (168, 152, 176),
                           14: (128, 112, 140), 15: (48, 36, 56)}),
]


def family(main):
    """The ten in OPTIONS order: the first is the default and the main direction's."""
    first = {"A": 0, "B": 1, "C": 2}[main]
    order = [first] + [i for i in range(10) if i != first]
    return [FAMILY[i] for i in order]


def user_frame(motif):
    g = [[0] * 24 for _ in range(24)]
    for y in range(24):
        for x in range(24):
            xx, yy = min(x, 23 - x), min(y, 23 - y)
            d = min(xx, yy, xx + yy - 2)
            if d < 1:
                continue
            if d == 1:
                v = 15
            elif d in (2, 3, 4):
                v = 14
                if d == 2 and (x < 12 and xx <= yy or y < 12 and yy <= xx):
                    v = 13                       # the light falls on the band's top and left
                if d == 4 and (x > 11 and xx <= yy or y > 11 and yy <= xx):
                    v = 10                       # and the shade on its right and foot
            elif d == 5:
                v = 11                           # the inner bevel
            else:
                v = 1
            g[y][x] = v
    along = lambda x, y: x if min(y, 23 - y) <= min(x, 23 - x) else y

    def band(x, y):
        xx, yy = min(x, 23 - x), min(y, 23 - y)
        return min(xx, yy, xx + yy - 2)
    for y in range(24):
        for x in range(24):
            d = band(x, y)
            if d < 2 or d > 4:
                continue
            a = along(x, y)
            if motif == "dots" and d == 3 and a % 4 == 1:
                g[y][x] = 13
            elif motif == "trace" and d == 3:
                g[y][x] = 11 if a % 8 != 4 else 10
            elif motif == "scan" and (y % 2 == 0) and d in (2, 3, 4) and g[y][x] == 14:
                g[y][x] = 10
            elif motif == "stars" and d == 3 and (a * 5 + d) % 8 == 2:
                g[y][x] = 13
            elif motif == "double" and d == 3:
                g[y][x] = 13
            elif motif == "hair" and d in (2, 4):
                g[y][x] = 14
    if motif == "bracket":
        for k in range(3, 7):
            for (x, y) in ((k, 2), (2, k)):
                for X, Y in ((x, y), (23 - x, y), (x, 23 - y), (23 - x, 23 - y)):
                    g[Y][X] = 11
    if motif == "sigil":
        for X, Y in ((3, 3), (20, 3), (3, 20), (20, 20)):
            for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                g[Y + dy][X + dx] = 13
            g[Y][X] = 15
    # the eight inner-corner pixels (slot 12): two at each inner corner, as style 1 always had them
    for X, Y in ((5, 6), (6, 5), (18, 6), (17, 5), (5, 17), (6, 18), (18, 17), (17, 18)):
        g[Y][X] = 12
    return g


# ===================================================================================================== the arrow
CHEVRON = ["X.......X",
           "XX.....XX",
           ".XX...XX.",
           "..XX.XX..",
           "...XXX...",
           "....X...."]


def arrow_cell(dy, body, edge, bar=False):
    c = [[0] * 16 for _ in range(16)]
    for y, row in enumerate(CHEVRON):
        for x, ch in enumerate(row):
            if ch == "X":
                Y = 1 + dy + y
                c[Y][x] = body
                if c[Y + 1][x] == 0:
                    c[Y + 1][x] = edge               # its shadow, one below
    if bar:                                          # a floor under it (tried: it read as a Y, so off)
        for x in range(2, 7):
            c[10][x] = edge
    return c


def arrows():
    """down_arrows.png's 128x16: four cells (dy 0, 1, 2, 3) in 4-on-2, then four in 2-on-9."""
    px = [[0] * 128 for _ in range(16)]
    for half, (body, edge) in enumerate(((4, 2), (2, 9))):
        for f, dy in enumerate((0, 1, 2, 3)):
            c = arrow_cell(dy, body, edge)
            for y in range(16):
                for x in range(16):
                    px[y][half * 64 + f * 16 + x] = c[y][x]
    single = {3: arrow_cell(2, 4, 2), 4: arrow_cell(2, 2, 9)}
    return px, single


# ================================================================================================ composing
def text_pal(n=0):
    return jasc(os.path.join(TW, "stdpal_%d.pal" % n))


def dlg_palette(direction=None, sign=False):
    p = text_pal(1 if sign else 0)
    if direction:
        st = STYLES[direction]
        for k, v in (st["sign_pal"] if sign else st["pal"]).items():
            p[k] = v
    return [q5(c) for c in p]


def vanilla_quarter(sign=False):
    w, h, bd, pal, px = load_png(os.path.join(TW, "signpost.png" if sign else "menu_message.png"))
    per = w // 8
    g = [[0] * QW for _ in range(QH)]
    for t, (x0, y0) in DLG_TILES.items():
        tt = tile(px, t, per)
        for y in range(8):
            for x in range(8):
                g[y0 + y][x0 + x] = tt[y][x]
    for y in range(8, QH):
        for x in range(16, 24):
            g[y][x] = 1
    return g


def strip(g):
    """The 240x48 the hardware draws from a quarter: tile 2 repeated, the bottom half V-flipped."""
    s = [[0] * 240 for _ in range(48)]
    for y in range(24):
        for x in range(240):
            qx = x if x < 16 else (16 + (x - 16) % 8 if x < 224 else x - 200)
            s[y][x] = g[y][qx]
            s[47 - y][x] = g[y][qx]
    return s


def render(idx, pal, bg=None):
    h, w = len(idx), len(idx[0])
    im = Image.new("RGB", (w, h), bg or (0, 0, 0)) if bg is None or isinstance(bg, tuple) else bg.copy()
    px = im.load()
    for y in range(h):
        for x in range(w):
            v = idx[y][x]
            if v:
                px[x, y] = pal[v]
            elif bg is None:
                px[x, y] = (40, 44, 52)
    return im


def menu_box(fr, wt, ht):
    """A standard-frame window wt x ht tiles: the frame one tile round it (DrawStdWindowFrame)."""
    W, H = (wt + 2) * 8, (ht + 2) * 8
    g = [[1] * W for _ in range(H)]
    for ty in range(ht + 2):
        for tx in range(wt + 2):
            sx = 0 if tx == 0 else (2 if tx == wt + 1 else 1)
            sy = 0 if ty == 0 else (2 if ty == ht + 1 else 1)
            for y in range(8):
                for x in range(8):
                    g[ty * 8 + y][tx * 8 + x] = fr[sy * 8 + y][sx * 8 + x]
    return g


_FONT = None


def print_text(im, x, y, s, ink, shadow):
    global _FONT
    import fontwidth
    if _FONT is None:
        _FONT = (Image.open(os.path.join(FONTS, "latin_normal.png")), fontwidth.font(GBA))
    sheet, (w, cm) = _FONT
    fp, px = sheet.load(), im.load()
    for ch in s:
        b = cm.get(ch)
        if b is None:
            continue
        gx, gy = (b % 16) * 16, (b // 16) * 16
        for yy in range(16):
            for xx in range(min(16, w[b])):
                v = fp[gx + xx, gy + yy]
                X, Y = x + xx, y + yy
                if 0 <= X < im.width and 0 <= Y < im.height:
                    if v == 1:
                        px[X, Y] = ink
                    elif v == 2:
                        px[X, Y] = shadow
        x += w[b]
    return x


def text_width(s):
    import fontwidth
    w, cm = fontwidth.font(GBA)
    return sum(w[cm[c]] for c in s if c in cm)


LINES = ["DRAFT: the frame around every line.", "Every sign and menu wears it too."]
MENU = ["INDEX", "DAEMONS", "STOCK", "USER", "SAVE", "OPTIONS"]


def mock(direction, bg, fr_pal, fr, arrow_px, sign=False):
    """A 240x160 screen: the message box (or the sign) as the game draws it, two lines in its font, the arrow, and
    a START menu in the family's first frame at the right."""
    im = bg.copy().convert("RGB")
    if direction:
        g = quarter(direction, sign)
    else:
        g = vanilla_quarter(sign)
    pal = dlg_palette(direction, sign)
    s = strip(g)
    px = im.load()
    for y in range(48):
        for x in range(240):
            if s[y][x]:
                px[x, 112 + y] = pal[s[y][x]]
    for x in range(16, 224):                           # the window: PIXEL_FILL(1)
        for y in range(120, 152):
            px[x, y] = pal[1]
    print_text(im, 16 + 2, 120 + 1, LINES[0], pal[2], pal[3])
    end = print_text(im, 16 + 2, 120 + 17, LINES[1], pal[2], pal[3])
    # the arrow, cell 1, 10x12, where the printer would put it after the last line
    for y in range(12):
        for x in range(10):
            v = arrow_px[y][16 + x]
            if v:
                px[end + 2 + x, 120 + 17 + y] = pal[v]
    if fr is not None and not sign:
        mb = menu_box(fr, 7, len(MENU) * 2)
        X0, Y0 = 240 - (7 + 2) * 8, 0
        for y in range(len(mb)):
            for x in range(len(mb[0])):
                if mb[y][x] and Y0 + y < 112:
                    px[X0 + x, Y0 + y] = fr_pal[mb[y][x]]
        for i, t in enumerate(MENU):
            if Y0 + 8 + i * 16 + 2 < 104:
                print_text(im, X0 + 8 + 8, Y0 + 8 + i * 16, t, fr_pal[2], fr_pal[3])
    return im


# ============================================================================================ the 9.4 measure
def hue_distance(c):
    try:
        spec = importlib.util.spec_from_file_location("gbabattlebg", os.path.join(ROOT, "tools", "gbabattlebg.py"))
        if "gbabattlebg" not in sys.modules:
            argv, sys.argv = sys.argv, sys.argv[:1]
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            sys.argv = argv
            sys.modules["gbabattlebg"] = m
        return sys.modules["gbabattlebg"].type_distance(tuple(v >> 3 for v in c))
    except Exception as e:                           # the measure is advice here, never a reason to fail a draft
        return (float("nan"), "(%s)" % e.__class__.__name__)


# =========================================================================================================== main
def report():
    print("T-523 text window frames -- the engine's files (%s):" % TW)
    for n in ["menu_message", "signpost"] + ["type%d" % i for i in range(1, 11)]:
        w, h, bd, pal, px = load_png(os.path.join(TW, n + ".png"))
        used = sorted({v for r in px for v in r})
        print("  %-13s %3dx%-3d %d tiles, %d-bit, slots drawn %s" % (n + ".png", w, h, w * h // 64, bd, used))
    w, h, bd, pal, px = load_png(os.path.join(FONTS, "down_arrows.png"))
    print("  %-13s %3dx%-3d slots drawn %s" % ("down_arrows", w, h, sorted({v for r in px for v in r})))
    print("\nThe directions' colours (5-bit, as the GBA keeps them), CIE76 from the nearest type hue (9.4):")
    for k, st in STYLES.items():
        for what, pal in (("box", st["pal"]), ("sign", st["sign_pal"])):
            cells = []
            for slot, c in sorted(pal.items()):
                d, t = hue_distance(q5(c))
                cells.append("%d %s %.0f %s" % (slot, "#%02x%02x%02x" % q5(c), d, t))
            print("  %s %-10s %-4s %s" % (k, st["name"], what, " | ".join(cells)))
    print("\nThe ten frames (slot 12 is the day's at run time on START):")
    for i, (name, motif, pal) in enumerate(family(MAIN_RECOMMENDED), 1):
        near = min((hue_distance(q5(c)) for s, c in pal.items() if s in (13, 14)), key=lambda t: t[0])
        print("  %2d %-10s %-7s band nearest a type hue: %.0f (%s)" % (i, name, motif, near[0], near[1]))
    for s in LINES:
        print("  mock line %3dpx (208 allowed): %s" % (text_width(s), s))


def draft(out):
    os.makedirs(out, exist_ok=True)
    bg = Image.open(A.bg).convert("RGB") if A.bg else Image.new("RGB", (240, 160), (96, 120, 104))
    apx, single = arrows()
    w, h, bd, vpal, vapx = load_png(os.path.join(FONTS, "down_arrows.png"))
    text = [q5(c) for c in text_pal(0)]
    save_png(os.path.join(out, "down_arrows.png"), apx, vpal)
    for n, c in single.items():
        save_png(os.path.join(out, "down_arrow_%d.png" % n), c, vpal)
    for k in STYLES:
        d = os.path.join(out, k)
        os.makedirs(d, exist_ok=True)
        for sign in (False, True):
            g = quarter(k, sign)
            name = "signpost" if sign else "menu_message"
            w, h, bd, p, px = load_png(os.path.join(TW, name + ".png"))
            per = w // 8
            for t, (x0, y0) in DLG_TILES.items():
                put_tile(px, t, per, [row[x0:x0 + 8] for row in g[y0:y0 + 8]])
            pal = dlg_palette(k, sign)
            save_png(os.path.join(d, name + ".png"), px, pal)
            write_jasc(pal, os.path.join(d, "stdpal_%d.pal" % (1 if sign else 0)))
        fam = family(k)
        for i, (name, motif, fp) in enumerate(fam, 1):
            w, h, bd, p, vpx = load_png(os.path.join(TW, "type%d.png" % i))
            pal = [q5(c) for c in p]
            for s, c in fp.items():
                pal[s] = q5(c)
            save_png(os.path.join(d, "type%d.png" % i), user_frame(motif), pal)
    sheet(out, bg, apx, vapx, text)


def font_label():
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
    except Exception:
        return ImageFont.load_default()


def sheet(out, bg, apx, vapx, text):
    F = font_label()
    blocks = []                                        # (caption, image)
    vq = vanilla_quarter()
    rows = [("THE ENGINE NOW (FireRed's)", None)] + [("%s  %s" % (k, STYLES[k]["name"]), k) for k in STYLES]
    W = 1500
    parts = []
    hdr = Image.new("RGB", (W, 60), (24, 26, 30))
    d = ImageDraw.Draw(hdr)
    d.text((12, 8), "T-523 DRAFT -- the text window frames and the more-text arrow, drawn by hand in code on the "
                    "tile grid (no AI image). Same tiles, sizes and palette slots as the engine's.", fill=(230, 230, 230),
           font=F)
    d.text((12, 28), "Each row: the message box as the hardware lays it (1x, then 3x), its sign, its tiles at 3x. "
                     "Below: the ten OPTIONS frames, the arrow, and each direction at real size.", fill=(170, 170, 170),
           font=F)
    parts.append(hdr)
    for cap, k in rows:
        g = vq if k is None else quarter(k)
        sg = vanilla_quarter(True) if k is None else quarter(k, True)
        pal, spal = dlg_palette(k), dlg_palette(k, True)
        s1 = render(strip(g), pal, (40, 44, 52))
        sg1 = render(strip(sg), spal, (40, 44, 52))
        q3 = render(g, pal, (40, 44, 52)).resize((QW * 4, QH * 4), Image.NEAREST)
        row = Image.new("RGB", (W, 48 * 3 + 48 + 60), (32, 34, 40))
        d = ImageDraw.Draw(row)
        d.text((12, 6), cap + ("" if k is None else " -- " + STYLES[k]["said"]), fill=(240, 220, 160), font=F)
        row.paste(s1, (12, 26))
        row.paste(sg1, (12 + 250, 26))
        row.paste(s1.resize((720, 144), Image.NEAREST), (12, 82))
        row.paste(q3, (12 + 740, 82))
        d.text((12 + 740, 62), "the top-half tiles 0-13, 4x", fill=(160, 160, 160), font=F)
        d.text((502, 26), "1x: box, sign", fill=(160, 160, 160), font=F)
        parts.append(row)
    # the ten frames
    fr_row = Image.new("RGB", (W, 330), (32, 34, 40))
    d = ImageDraw.Draw(fr_row)
    d.text((12, 6), "THE TEN OPTIONS FRAMES -- the engine's (top) and the family, frame 1 the default (%s); each at "
                    "1x and as a menu at 3x" % STYLES[MAIN_RECOMMENDED]["name"], fill=(240, 220, 160), font=F)
    for i in range(10):
        w, h, bd, p, vpx = load_png(os.path.join(TW, "type%d.png" % (i + 1)))
        vp = [q5(c) for c in p]
        name, motif, fp = family(MAIN_RECOMMENDED)[i]
        np_ = list(vp)
        for s, c in fp.items():
            np_[s] = q5(c)
        x = 12 + i * 148
        for j, (fr, pal, lab) in enumerate(((vpx, vp, "%d" % (i + 1)), (user_frame(motif), np_, name))):
            y = 26 + j * 150
            mb = menu_box(fr, 3, 2)
            im1 = render(mb, pal, (40, 44, 52))
            fr_row.paste(render(fr, pal, (40, 44, 52)), (x, y + 16))
            fr_row.paste(im1.resize((im1.width * 3, im1.height * 3), Image.NEAREST), (x + 30, y + 16))
            d.text((x, y), lab, fill=(200, 200, 200), font=F)
    parts.append(fr_row)
    # the arrow
    ar = Image.new("RGB", (W, 150), (32, 34, 40))
    d = ImageDraw.Draw(ar)
    d.text((12, 6), "THE ARROW -- down_arrows.png, the engine's (left) and ours (right): cells x 0, 16, 32, 16 make the "
                    "bounce; 4-on-2 and 2-on-9 as before. 1x and 4x, on the paper.", fill=(240, 220, 160), font=F)
    for j, src in enumerate((vapx, apx)):
        im = render(src, text, (255, 255, 255))
        ar.paste(im, (12 + j * 700, 30))
        ar.paste(im.resize((512, 64), Image.NEAREST), (12 + j * 700, 60))
    parts.append(ar)
    # the mocks at real size, and at 2x
    mk = Image.new("RGB", (W, 380), (32, 34, 40))
    d = ImageDraw.Draw(mk)
    d.text((12, 6), "AT REAL SIZE (240x160, the game's own font; the corner glyph in slot 14 wears the day's trim at "
                    "run time): the engine now, A, B, C -- and below, each at 2x with its sign", fill=(240, 220, 160),
           font=F)
    mocks = []
    vfr = load_png(os.path.join(TW, "type1.png"))
    mocks.append(mock(None, bg, [q5(c) for c in vfr[3]], vfr[4], vapx))
    for k in STYLES:
        name, motif, fp = family(k)[0]
        w, h, bd, p, vpx = load_png(os.path.join(TW, "type1.png"))
        pal = [q5(c) for c in p]
        for s, c in fp.items():
            pal[s] = q5(c)
        mocks.append(mock(k, bg, pal, user_frame(motif), apx))
    for i, m in enumerate(mocks):
        mk.paste(m, (12 + i * 250, 30))
        m.save(os.path.join(out, "mock_%s.png" % ("engine" if i == 0 else "ABC"[i - 1])))
    for i, k in enumerate([None] + list(STYLES)):
        sm = mock(k, bg, None, None, vapx if k is None else apx, sign=True)
        mk.paste(sm, (12 + i * 250, 200))
        sm.save(os.path.join(out, "mock_sign_%s.png" % ("engine" if k is None else k)))
    parts.append(mk)
    big = Image.new("RGB", (W, 360 * 2 + 30), (32, 34, 40))
    d = ImageDraw.Draw(big)
    d.text((12, 6), "2x: the engine now (left) and the recommendation, A TERMINAL (right); B and C under them",
           fill=(240, 220, 160), font=F)
    order = [0, 1, 2, 3]
    for j, i in enumerate(order):
        big.paste(mocks[i].resize((480, 320), Image.NEAREST), (12 + (j % 2) * 500, 30 + (j // 2) * 340))
    parts.append(big)
    H = sum(p.height for p in parts)
    sh = Image.new("RGB", (W, H), (32, 34, 40))
    y = 0
    for p in parts:
        sh.paste(p, (0, y))
        y += p.height
    path = os.path.join(out, "t523_frames_sheet.png")
    sh.save(path)
    print("  sheet -> %s" % path)


def write(main):
    """Into the engine: menu_message.png and stdpal_0.pal (12-15), signpost.png and stdpal_1.pal (11-15), type1..10.png,
    down_arrows.png and down_arrow_3/4.png. Only the tiles and slots named above move; the rest is read back as it was."""
    d = os.path.join(DRAFT_DEFAULT, main)
    for sign in (False, True):
        name = "signpost" if sign else "menu_message"
        shutil.copyfile(os.path.join(d, name + ".png"), os.path.join(TW, name + ".png"))
        n = 1 if sign else 0
        cur, new = jasc(os.path.join(TW, "stdpal_%d.pal" % n)), jasc(os.path.join(d, "stdpal_%d.pal" % n))
        keep = range(0, 11) if sign else range(0, 12)
        for s in keep:
            new[s] = cur[s]
        write_jasc(new, os.path.join(TW, "stdpal_%d.pal" % n))
    for i in range(1, 11):
        shutil.copyfile(os.path.join(d, "type%d.png" % i), os.path.join(TW, "type%d.png" % i))
    for n in ("down_arrows", "down_arrow_3", "down_arrow_4"):
        shutil.copyfile(os.path.join(DRAFT_DEFAULT, n + ".png"), os.path.join(FONTS, n + ".png"))
    print("  written %s's frames, sign, the ten and the arrow into %s" % (main, GBA))
    print("  now: python3 tools/gbacalendar_ui.py --write --approved  (the START styleMask is measured: all ten)")


# ================================================================================================ T-554: the std frame
#  graphics/text_window/std.png is NOT type1: LoadStdWindowGfx (src/text_window.c) loads it, 9 tiles (0x120 bytes),
#  always with stdpal_3 (GetTextWindowPalette(3)), for the money box (bag, MART, field), the save box, the party's
#  message box, the PC's message box, the item PC's and TOOLKIT's sub-windows, the coin box, the elevator and the map
#  name popup (which loads stdpal_3 too). T-523 redrew type1-10, so the user's TERMINAL is round every window the
#  OPTIONS frame draws, and pret's 9 tiles (a grey rounded ring, recoloured) round these.
#  THE CONTRACT: 24x24, exactly 9 tiles in DrawStdFrameWithCustomTileAndPalette's order (0 1 2 / 3 4 5 / 6 7 8, no
#  flips), tile 4 the paper (1) because the window's own pixels sit over it; drawn in stdpal_3's slots, which are
#  every std window's TEXT colours too (1 paper, 2 ink, 3 shadow) and the popup's -- so a drop-in leaves the .pal be.
#  stdpal_3 holds no near-black and no teal, so TERMINAL cannot be matched colour for colour inside it:
#    1  TERMINAL, IN STDPAL_3   type1's drawing pixel for pixel, its slots mapped to stdpal_3's nearest in lightness
#                               order (outline 13 slate, band 15, light 12, shade 13, bevel 11, the inner corners 14
#                               sky). std.png only; no palette moves. A lighter TERMINAL.
#    2  TERMINAL, EXACT         type1 itself (slots 10-15) and stdpal_3's 10-15 set to type1's colours. Breaks the
#                               rule that stdpal_0..4 do not move: slot 10 is unused magenta, but 11-15 are read by the
#                               map name popup's frame (the same std tiles) and the PC's multi-move palette 13 too.
STD_SLOTS_1 = {15: 13, 14: 15, 13: 12, 10: 13, 11: 11, 12: 14, 1: 1, 0: 0}


def std_versions():
    """{version: (24x24 index grid, stdpal_3 as it would be, said)} -- drawn from user_frame, the code type1 came from."""
    base = user_frame("bracket")
    p3 = text_pal(3)
    one = [[STD_SLOTS_1[v] for v in r] for r in base]
    p2 = list(p3)
    for s, c in FAMILY[0][2].items():
        p2[s] = c
    return {"1": (one, p3, "TERMINAL, IN STDPAL_3: type1's drawing, stdpal_3's colours; std.png only"),
            "2": ([r[:] for r in base], p2, "TERMINAL, EXACT: type1 itself, and stdpal_3's slots 10-15 retinted")}


def std_now():
    w, h, bd, pal, px = load_png(os.path.join(TW, "std.png"))
    return [[v & 15 for v in r] for r in px], text_pal(3)


def std_draft(out):
    for v, (g, p3, said) in std_versions().items():
        d = os.path.join(out, v)
        os.makedirs(d, exist_ok=True)
        save_png(os.path.join(d, "std.png"), g, [q5(c) for c in p3])
        if p3 != text_pal(3):
            write_jasc(p3, os.path.join(d, "stdpal_3.pal"))
        print("  std %s: %s -> %s" % (v, said, os.path.relpath(d, ROOT)))


def std_write(v):
    g, p3, said = std_versions()[v]
    assert len(g) == 24 and len(g[0]) == 24 and all(x == 1 for r in g[8:16] for x in r[8:16]), "std's 9-tile contract"
    w, h, bd, pal, px = load_png(os.path.join(TW, "std.png"))
    save_png(os.path.join(TW, "std.png"), g, pal)        # the PNG's own palette kept: stdpal_3 colours it at run time
    if p3 != text_pal(3):
        write_jasc(p3, os.path.join(TW, "stdpal_3.pal"))
    print("  written std.png (%s)%s" % (said, ", stdpal_3.pal 10-15" if p3 != text_pal(3) else ""))


def main():
    if A.std_draft:
        std_draft(A.std_draft)
        if not (A.write or A.draft):
            return 0
    if A.std and not A.write:                            # report: the engine's std.png against the approved version
        g, p3, said = std_versions()[A.std]
        w, h, bd, pal, px = load_png(os.path.join(TW, "std.png"))
        drift = [[v & 15 for v in r] for r in px] != g or text_pal(3) != p3
        print("  std %s: %s" % (A.std, "DRIFT: engineGba's std.png is not this version" if drift else "the engine's"))
        return 1 if drift and APPROVED_STD == A.std else 0
    if A.write and A.std:
        if not A.approved or APPROVED_STD != A.std:
            print("  --write --std %s refuses: APPROVED_STD is %r (the user has not picked the std frame)."
                  % (A.std, APPROVED_STD))
            return 1
        std_write(A.std)
        return 0
    if A.write and not A.approved:
        print("  --write refuses without --approved: the user picks a direction before it is written.")
        return 1
    if A.write and not A.main:
        print("  --write needs --main A|B|C: the direction the user picked.")
        return 1
    report()
    if A.draft:
        draft(A.draft)
    if A.write:
        if not os.path.isdir(os.path.join(DRAFT_DEFAULT, A.main)):
            print("  no draft for %s: run --draft first" % A.main)
            return 1
        write(A.main)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""CHECKPOINTS, THE REPO and the BENCHMARKS in detail, on each town's own tiles (T-85; vision.md 9.23).

    python3 tools/gbacivictown.py            # report and preview to /tmp/civic_town.png (shared | detailed)
    python3 tools/gbacivictown.py --write    # town tiles, town blocks, town maps, and tools/gbacivictown.json

WHY A SECOND TOOL. gbacivic.py draws every building once, in the General
tileset, and the General tileset has five slots left -- so its drawings are as
detailed as they can ever be there. This tool draws each building again, far
more finely, on the tiles of the town it stands in: every cell of the building
gets a block of the town's own, and the map cell is pointed at it. The shared
drawing stays underneath as the fallback, and is what a building keeps when its
town cannot take the tiles or when it stands where a connection can see it.

WHERE THE ROOM COMES FROM. A town tileset holds 384 tiles and the build packs
only -num_tiles of them, but most towns carry many slots no block draws -- Slate
has 188 -- and vanilla's own animations write only a few by number. So a tile
goes first into a slot nothing references (never an animated one), then onto the
end.

WHAT IS DRAWN, cell by cell over the original blocks:

  * where the original drew the building on its BOTTOM layer, the detail replaces
    it there, opaque;
  * where it drew the building on its TOP layer over ground, the detail goes on
    the top layer with the ground kept below -- which also lets the dome's crown
    rise into the row above, a BENCHMARK's steps fill the half-cell vanilla left
    as grass, and the board stand full height;
  * a BENCHMARK pillar is palette row 7 on the top layer with the porch behind it
    on the bottom, as in gbacivic.py; the gauge and the mark's plate are row 5,
    each on whole tiles; everything else is row 2.

The door cell is never touched: the door animation draws it.

NEVER NEAR A CONNECTION. The engine does not redraw the screen when you cross a
connection (engine.md trap 14), so a building any cell of which is within seven
cells of an edge joined to another tileset keeps the shared drawing. That is
Lurid's BENCHMARK.

RERUNNABLE. tools/gbacivictown.json records each cell's original block and the
blocks this tool made; a rerun draws over the originals, reuses its own block
ids and frees its old tiles. gbacivic.py reads the same file and leaves those
cells alone.
"""
import importlib.util, json, math, os, re, struct, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbacivic", os.path.join(ROOT, "tools", "gbacivic.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
E, Canvas = C.E, C.Canvas

GBA = C.GBA
PD = C.PD
RULES = C.RULES
MANIFEST = os.path.join(ROOT, "tools", "gbacivictown.json")
PREVIEW = "/tmp/civic_town.png"
WRITE = "--write" in sys.argv
BAND = 7
ANIM_SLOTS = {"gTileset_CeladonCity": range(744, 776)}      # TilesetAnim_Celadon writes from 744
ORDER = {"BENCHMARK": 0, "CHECKPOINT": 1, "REPO": 2}
BUILDING_ROWS = C.BUILDING_ROWS
R2, R5, R7 = C.R2, C.R5, C.R7


# ================================================================== the detailed drawings
def art_checkpoint():
    """80x80, dx -2..2 by dy -4..0; the door cell is x 32..47, y 64..79 and stays empty. Row 2."""
    c, r = Canvas(80, 80), 2
    # the terrace, paved in offset slabs
    for y in range(16, 80):
        course = (y - 16) // 8
        off = 4 if course % 2 else 0
        for x in range(80):
            v = 3
            if (y - 16) % 8 == 0 or (x + off) % 8 == 0:
                v = 4
            elif (y - 16) % 8 == 1:
                v = 2
            c.px(x, y, r, v)
    # the dome: lit from the upper left, ribbed, coursed, with a lantern on its crown
    step_dark = {1: 15, 15: 9, 9: 8, 8: 7, 7: 7}
    step_light = {7: 8, 8: 9, 9: 15, 15: 1, 1: 1}
    spans = {}
    for y in range(5, 45):
        t = (44 - y) / 39.0
        h = int(38 * math.sqrt(max(0.0, 1 - t * t)))
        if h <= 0:
            continue
        spans[y] = h
        for x in range(40 - h, 40 + h):
            u = (x - 39.5) / h
            v = (y - 5) / 39.0
            light = 0.42 - 0.72 * v - 0.38 * abs(u)       # lit from above, so both halves share mirrored tiles
            c.px(x, y, r, 15 if light > 0.22 else 9 if light > -0.28 else 8)
        c.px(40 - h - 1, y, r, 7); c.px(40 + h, y, r, 7)
    top = min(spans)
    c.rect(40 - spans[top], top - 1, 39 + spans[top], top - 1, r, 7)
    for y, h in spans.items():
        for k in (-3, -2, -1, 1, 2, 3):
            rx = int(round(39.5 + k * h / 4.0 + (-0.5 if k < 0 else 0.5)))
            if 40 - h < rx < 39 + h and 7 < y < 42:
                c.px(rx, y, r, step_dark[c.p[y][rx][1]])
        if y in (16, 26, 36):
            for x in range(40 - h, 40 + h):
                c.px(x, y, r, step_dark[c.p[y][x][1]])
                if y - 1 in spans:
                    c.px(x, y - 1, r, step_light[c.p[y - 1][x][1]])
    for y in range(9, 16):                              # a glint either side of the crown
        h = spans.get(y, 0)
        x = 40 - int(h * 0.55)
        c.px(x, y, r, 1); c.px(79 - x, y, r, 1)
    c.rect(36, 0, 43, 4, r, 7); c.rect(37, 1, 42, 3, r, 2); c.px(38, 1, r, 1); c.px(38, 2, r, 1)   # lantern
    c.rect(35, 4, 44, 4, r, 8)
    c.stamp(32, 18, E.emblem("CHECKPOINT", {"O": 7, "L": 1, "M": 15, "D": 8}), r)
    # the eave: a cornice with dentils and the shadow it casts on the drum
    c.rect(2, 42, 77, 42, r, 7); c.rect(2, 43, 77, 43, r, 3); c.rect(2, 44, 77, 44, r, 2)
    for x in range(2, 78):
        c.px(x, 45, r, 5 if x % 3 == 0 else 3); c.px(x, 46, r, 5 if x % 3 == 0 else 4)
    c.rect(4, 47, 75, 47, r, 6)
    # the drum, in coursed stone, lit in the middle
    for y in range(48, 72):
        course = (y - 48) // 4                          # courses of four and joints of eight: they sit on the tile grid, so tiles repeat
        off = 4 if course % 2 else 0
        for x in range(4, 76):
            d = abs(x - 39.5)
            face, mortar = (1, 2) if d < 12 else (2, 3) if d < 28 else (3, 4)
            joint = (y - 48) % 4 == 3 or (x + off) % 8 == 0
            c.px(x, y, r, mortar if joint else face)
    c.rect(4, 48, 4, 75, r, 7); c.rect(75, 48, 75, 75, r, 7); c.rect(5, 48, 5, 75, r, 4); c.rect(74, 48, 74, 75, r, 4)
    for x0 in (9, 21, 53, 65):                          # arched windows with sills and a reflection
        c.rect(x0, 51, x0 + 5, 68, r, 7); c.rect(x0 + 1, 52, x0 + 4, 67, r, 2)
        c.px(x0 + 1, 52, r, 7); c.px(x0 + 4, 52, r, 7)
        c.rect(x0 + 1, 60, x0 + 4, 60, r, 3)
        for k in range(4):                              # the reflection mirrors with the window
            c.px(x0 + 1 + (k // 2) if x0 < 40 else x0 + 4 - (k // 2), 54 + k, r, 1)
        c.rect(x0 - 1, 69, x0 + 6, 69, r, 3); c.rect(x0 - 1, 70, x0 + 6, 70, r, 4)
    # the door: pilasters, a teal canopy and its shadow, two warm lamps
    c.rect(29, 56, 31, 71, r, 1); c.rect(31, 56, 31, 71, r, 3); c.rect(48, 56, 50, 71, r, 1); c.rect(50, 56, 50, 71, r, 3)
    c.rect(27, 53, 52, 53, r, 7); c.rect(27, 54, 52, 54, r, 15); c.rect(27, 55, 52, 55, r, 9); c.rect(27, 56, 52, 56, r, 8)
    c.rect(32, 57, 47, 63, r, 6); c.rect(32, 57, 47, 57, r, 7)
    for lx in (30, 49):
        c.px(lx, 58, r, 6); c.px(lx, 59, r, 10); c.px(lx, 60, r, 10); c.px(lx, 61, r, 11)
    # plinth and steps
    c.rect(4, 72, 75, 72, r, 3); c.rect(4, 73, 75, 73, r, 2); c.rect(4, 74, 75, 74, r, 4); c.rect(4, 75, 75, 75, r, 5)
    c.rect(0, 76, 79, 76, r, 1); c.rect(0, 77, 79, 77, r, 2); c.rect(0, 78, 79, 78, r, 3); c.rect(0, 79, 79, 79, r, 7)
    for y in range(64, 80):                              # the door cell belongs to the door
        for x in range(32, 48):
            c.p[y][x] = None
    return c


def art_repo():
    """64x64, dx -2..1 by dy -3..0; the door cell is x 32..47, y 48..63 and stays empty. Row 5."""
    c, r = Canvas(64, 64), 5
    for y in range(64):                                 # the yard: concrete with joints
        for x in range(64):
            c.px(x, y, r, 4 if (x % 16 == 0 or y % 16 == 0) else 3)

    def castings(x0, y0, x1, y1):
        for cx, cy in ((x0, y0), (x1 - 2, y0), (x0, y1 - 2), (x1 - 2, y1 - 2)):
            c.rect(cx, cy, cx + 2, cy + 2, r, 5); c.px(cx + 1, cy + 1, r, 3)

    # the top container: darker, ribbed, the branch on a painted panel, two vents
    for x in range(4, 60):
        v = {0: 12, 1: 9, 2: 9, 3: 4}[(x - 4) % 4]
        c.rect(x, 3, x, 28, r, v)
    c.rect(4, 2, 59, 2, r, 5); c.rect(4, 3, 59, 3, r, 10); c.rect(4, 4, 59, 4, r, 12)
    c.rect(4, 27, 59, 27, r, 4); c.rect(4, 28, 59, 28, r, 9); c.rect(4, 29, 59, 29, r, 5)
    c.rect(4, 2, 4, 29, r, 5); c.rect(59, 2, 59, 29, r, 5); c.rect(5, 5, 6, 26, r, 9); c.rect(57, 5, 58, 26, r, 4)
    castings(4, 2, 60, 30)
    c.rect(21, 7, 42, 25, r, 11); c.rect(21, 7, 42, 7, r, 12); c.rect(21, 7, 21, 25, r, 12)
    c.rect(42, 8, 42, 25, r, 9); c.rect(22, 25, 42, 25, r, 9)
    c.stamp(24, 8, E.emblem("REPO", {"O": 5, "L": 10, "M": 7, "T": 1}), r)
    for vx in (9, 47):
        c.rect(vx, 10, vx + 7, 15, r, 4)
        for vy in (11, 13):
            c.rect(vx + 1, vy, vx + 6, vy, r, 3)
    # the bottom pair: lighter, ribbed, rails, lock rods and handles, REPO on the left
    for x0 in (0, 32):
        for x in range(x0, x0 + 32):
            v = {0: 10, 1: 8, 2: 8, 3: 9}[(x - x0) % 4]
            c.rect(x, 31, x, 61, r, v)
        c.rect(x0, 30, x0 + 31, 30, r, 5); c.rect(x0, 31, x0 + 31, 31, r, 10); c.rect(x0, 62, x0 + 31, 62, r, 9); c.rect(x0, 63, x0 + 31, 63, r, 5)
        c.rect(x0, 30, x0, 63, r, 5); c.rect(x0 + 31, 30, x0 + 31, 63, r, 5); c.rect(x0 + 1, 32, x0 + 1, 61, r, 9)
        castings(x0, 30, x0 + 32, 64)
    c.rect(5, 37, 25, 47, r, 5); c.rect(6, 38, 24, 46, r, 9); c.rect(6, 38, 24, 38, r, 12)
    c.word(8, 40, "REPO", r, 1)
    for rx in (8, 22):
        c.rect(rx, 49, rx, 60, r, 2); c.rect(rx + 1, 49, rx + 1, 60, r, 4)
        c.rect(rx - 1, 54, rx + 2, 55, r, 5)
    for rx in (51, 55, 59):
        c.rect(rx, 35, rx, 60, r, 2); c.rect(rx + 1, 35, rx + 1, 60, r, 4)
        c.rect(rx - 1, 46, rx + 2, 47, r, 5)
    # a hazard-striped lintel over the loading door
    c.rect(30, 42, 49, 42, r, 5)
    for y in range(43, 48):
        for x in range(30, 50):
            c.px(x, y, r, 10 if (x + y) % 4 < 2 else 5)
    for y in range(48, 64):
        for x in range(32, 48):
            c.p[y][x] = None
    return c


def art_benchmark(left, right, mark):
    """(right-left+1)*16 x 80, dy -4..0; the door is column -left, its bottom cell empty."""
    ncell = right - left + 1
    c, r, B = Canvas(ncell * 16, 80), 2, R5
    W = ncell * 16
    X = lambda dx: (dx - left) * 16
    role = lambda dx: C.benchmark_role(dx, left, right)
    # the roof deck, its coping, vents and a skylight over the door
    c.rect(0, 0, W - 1, 0, r, 7); c.rect(0, 1, W - 1, 1, r, 1); c.rect(0, 2, W - 1, 2, r, 2)
    for y in range(3, 12):
        for x in range(W):
            c.px(x, y, r, 5 if (x % 16 == 8 or y == 7) else 4)
    for dx in (left + 1, right - 1):
        x0 = X(dx) + 4
        c.rect(x0, 4, x0 + 7, 9, r, 5); c.rect(x0, 4, x0 + 7, 4, r, 3); c.rect(x0 + 7, 5, x0 + 7, 9, r, 6)
        for gy in (6, 8):
            c.rect(x0 + 1, gy, x0 + 6, gy, r, 6)
    xs = X(0)
    c.rect(xs + 2, 4, xs + 13, 10, r, 7); c.rect(xs + 3, 5, xs + 12, 9, r, 2)
    for k in range(4):
        c.px(xs + 4 + k, 5 + k, r, 1)
    c.rect(0, 12, W - 1, 12, r, 3); c.rect(0, 13, W - 1, 13, r, 2); c.rect(0, 14, W - 1, 14, r, 1); c.rect(0, 15, W - 1, 15, r, 3)
    # the cornice: dentils, then a frieze with a carved relief of bars in every bay
    c.rect(0, 16, W - 1, 16, r, 7); c.rect(0, 17, W - 1, 17, r, 1); c.rect(0, 18, W - 1, 18, r, 3)
    for x in range(W):
        m = x % 4
        for y in (19, 20, 21):
            c.px(x, y, r, {0: 3, 1: 1 if y == 19 else 2, 2: 1 if y == 19 else 2, 3: 4}[m])
    c.rect(0, 22, W - 1, 22, r, 3); c.rect(0, 23, W - 1, 23, r, 2)
    c.rect(0, 24, W - 1, 30, r, 1); c.rect(0, 31, W - 1, 31, r, 4)
    for dx in range(left + 1, right):
        x0 = X(dx)
        for bx, h in ((2, 3), (6, 5), (10, 4)):
            c.rect(x0 + bx, 30 - h, x0 + bx + 2, 30, r, 2)
            c.rect(x0 + bx, 30 - h, x0 + bx, 30, r, 1); c.rect(x0 + bx + 2, 30 - h, x0 + bx + 2, 30, r, 4)
            c.rect(x0 + bx, 30 - h, x0 + bx + 2, 30 - h, r, 3)
    # the architrave; the mark's name on a bronze plate over two whole cells right of the door
    c.rect(0, 32, W - 1, 32, r, 2); c.rect(0, 33, W - 1, 44, r, 1)
    c.rect(0, 36, W - 1, 36, r, 3); c.rect(0, 41, W - 1, 41, r, 3)
    c.rect(0, 45, W - 1, 45, r, 4); c.rect(0, 46, W - 1, 46, r, 6); c.rect(0, 47, W - 1, 47, r, 7)
    # the porch: shadowed soffit, a panelled back wall with sconces
    c.rect(0, 48, W - 1, 48, r, 7); c.rect(0, 49, W - 1, 50, r, 6)
    for y in range(51, 74):
        for x in range(W):
            c.px(x, y, r, 6 if (x % 16 == 0 or y in (51, 62)) else 5)
    for dx in range(left, right + 1):
        if role(dx) in ("W", "M"):
            sx = X(dx) + 1
            c.px(sx, 57, r, 6); c.px(sx, 58, r, 10); c.px(sx, 59, r, 11)
    # floor and steps, full width
    c.rect(0, 74, W - 1, 74, r, 4); c.rect(0, 75, W - 1, 75, r, 3); c.rect(0, 76, W - 1, 76, r, 1)
    c.rect(0, 77, W - 1, 77, r, 2); c.rect(0, 78, W - 1, 78, r, 3); c.rect(0, 79, W - 1, 79, r, 7)
    for dx in range(left, right + 1):
        x0, ro = X(dx), role(dx)
        if ro in ("W", "M"):                            # a fluted stone column
            c.rect(x0 + 4, 48, x0 + 11, 48, r, 1); c.rect(x0 + 5, 49, x0 + 10, 49, r, 2); c.px(x0 + 4, 49, r, 4); c.px(x0 + 11, 49, r, 4)
            c.rect(x0 + 5, 50, x0 + 10, 50, r, 3)
            for k, v in enumerate((3, 1, 2, 1, 2, 4)):
                c.rect(x0 + 5 + k, 51, x0 + 5 + k, 71, r, v)
            c.rect(x0 + 4, 72, x0 + 11, 72, r, 2); c.rect(x0 + 4, 73, x0 + 11, 73, r, 4)
        elif ro in ("P", "P'"):                         # the leader's pillar, row 7
            a = x0 + 9 if ro == "P" else x0
            c.rect(a, 48, a + 6, 48, C.PILLAR_ROW, R7["LIGHT"]); c.rect(a, 49, a + 6, 50, C.PILLAR_ROW, R7["MID"])
            c.rect(a, 50, a + 6, 50, C.PILLAR_ROW, R7["DARK"])
            s = a + 1
            c.rect(s, 51, s + 4, 71, C.PILLAR_ROW, R7["MID"]); c.rect(s, 51, s, 71, C.PILLAR_ROW, R7["LIGHT"])
            c.rect(s + 4, 51, s + 4, 71, C.PILLAR_ROW, R7["DARK"]); c.rect(s + 2, 53, s + 2, 69, C.PILLAR_ROW, R7["DARK"])
            c.rect(a, 72, a + 6, 72, C.PILLAR_ROW, R7["DARK"]); c.rect(a, 73, a + 6, 73, C.PILLAR_ROW, R7["OUT"])
        elif ro in ("L", "R"):                          # a stone pier
            a = x0 if ro == "L" else x0 + 10
            for y in range(16, 80):
                for x in range(a, a + 6):
                    c.px(x, y, r, 3 if (y % 6 == 0) else 1 if x in (a + 1, a + 2) else 2)
            outer = x0 if ro == "L" else x0 + 15
            inner = a + 5 if ro == "L" else a
            c.rect(outer, 0, outer, 79, r, 7); c.rect(inner, 16, inner, 79, r, 4)
        elif ro == "D":                                 # the gauge over the door, row 5, a whole cell
            c.rect(x0, 48, x0 + 15, 63, 5, B["WHITE"]); c.rect(x0, 48, x0 + 15, 48, 5, B["OUT"]); c.rect(x0, 49, x0 + 15, 49, 5, B["DARK"])
            c.rect(x0, 50, x0, 63, 5, B["LIGHT"]); c.rect(x0 + 15, 50, x0 + 15, 63, 5, B["LIGHT"])
            art = E.emblem("BENCHMARK", {"O": B["OUT"], "W": B["WHITE"], "T": B["GREY"], "N": B["OUT"], "G": B["BRIGHT"], "S": B["LIGHT"]})
            for y in range(13):
                for x in range(16):
                    if art[y + 1][x]:
                        c.px(x0 + x, 50 + y, 5, art[y + 1][x])
            for y in range(64, 80):
                for x in range(x0, x0 + 16):
                    c.p[y][x] = None
    px0 = X(1)                                          # the plate last, over any pier under it
    c.rect(px0, 32, px0 + 31, 47, 5, B["OUT"]); c.rect(px0 + 1, 33, px0 + 30, 46, 5, B["AMBERD"])
    c.rect(px0 + 1, 33, px0 + 30, 33, 5, B["BRIGHT"]); c.rect(px0 + 1, 46, px0 + 30, 46, 5, B["DARK"])
    for rx, ry in ((px0 + 3, 35), (px0 + 28, 35), (px0 + 3, 44), (px0 + 28, 44)):
        c.px(rx, ry, 5, B["GOLD3"])
    tw = len(mark) * 4 - 1
    c.word(px0 + (32 - tw) // 2, 38, mark, 5, B["GOLDL"])
    return c


def art_board(tall):
    """the free-standing board, row 5: 16x32 over two cells, or 16x16 where a town has only the bottom one."""
    B = R5
    c = Canvas(16, 32 if tall else 16)
    y0 = 3 if tall else 0
    c.rect(0, y0, 15, y0 + 13, 5, B["OUT"]); c.rect(1, y0 + 1, 14, y0 + 12, 5, B["WHITE"])
    c.rect(1, y0 + 1, 14, y0 + 1, 5, B["BRIGHT"]); c.rect(1, y0 + 12, 14, y0 + 12, 5, B["LIGHT"])
    c.word(1, y0 + 4, "MARK", 5, B["OUT"])
    c.rect(2, y0 + 10, 13, y0 + 10, 5, B["GOLD3"])
    post_top, post_bottom = y0 + 14, (30 if tall else 14)
    for x0 in (3, 11):
        c.rect(x0, post_top, x0 + 1, post_bottom, 5, B["GREY"]); c.rect(x0, post_top, x0, post_bottom, 5, B["LIGHT"])
        c.rect(x0 - 1, post_bottom + 1, x0 + 2, post_bottom + 1, 5, B["DARK"])
    return c


# ================================================================== placing it
def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {"cells": {}, "made": {}}
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    btiles = {k: {t & 0x3FF for m in v for t in struct.unpack_from("<8H", prim, m * 16)
                  if t & 0x3FF and (t >> 12) & 0xF in BUILDING_ROWS} for k, v in C.GROUP.items()}
    btiles["CHECKPOINT"] |= C.CHECKPOINT_ROOF_EDGE
    maps = {}
    for d in sorted(os.listdir(os.path.join(GBA, "data/maps"))):
        p = os.path.join(GBA, "data/maps", d, "map.json")
        if os.path.exists(p):
            j = json.load(open(p)); maps[j["id"]] = (d, j)

    secs = {}
    def sec(symbol):
        if symbol not in secs:
            d = C.tdir(symbol, "secondary")
            rules = open(RULES).read()
            key = "secondary/%s/tiles.4bpp: %%.4bpp: %%.png\n\t$(GFX) $< $@ -num_tiles " % os.path.basename(d)
            n = int(rules[rules.index(key) + len(key):].split()[0])
            img = Image.open(os.path.join(d, "tiles.png"))
            meta = bytearray(open(os.path.join(d, "metatiles.bin"), "rb").read())
            attr = bytearray(open(os.path.join(d, "metatile_attributes.bin"), "rb").read())
            secs[symbol] = {"dir": d, "key": key, "n": n, "img": img, "meta": meta, "attr": attr,
                            "made": list(manifest["made"].get(symbol, [])), "tiles": {}, "blocks": {}, "new_blocks": []}
        return secs[symbol]

    def entries(ts, m):
        buf = prim if m < 640 else sec(ts)["meta"]
        k = m if m < 640 else m - 640
        return list(struct.unpack_from("<8H", buf, k * 16)) if (k + 1) * 16 <= len(buf) else None

    def attr_of(ts, m):
        if m < 640:
            return open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()[m * 4:(m + 1) * 4]
        return bytes(sec(ts)["attr"][(m - 640) * 4:(m - 639) * 4])

    # ---------------------------------------------------------------- every building, by its door, over the ORIGINAL blocks
    instances, bds = [], {}
    for mid, (mp, j) in maps.items():
        l = layouts.get(j["layout"])
        if not l or l["primary_tileset"] != "gTileset_General":
            continue
        path = l["blockdata_filepath"]
        bd = bds.setdefault(path, bytearray(open(os.path.join(GBA, path), "rb").read()))
        Wm, Hm = l["width"], l["height"]
        orig = manifest["cells"].get(mp, {})
        def cell(x, y, bd=bd, Wm=Wm, orig=orig):
            o = orig.get("%d,%d" % (x, y))
            return o if o is not None else struct.unpack_from("<H", bd, (y * Wm + x) * 2)[0] & 0x3FF
        ts = l["secondary_tileset"]
        def bentries(m, kind, ts=ts):
            e = entries(ts, m)
            return [] if e is None else [k for k, t in enumerate(e) if t & 0x3FF and (t >> 12) & 0xF in BUILDING_ROWS and (t & 0x3FF) in btiles[kind]]
        diff = set()
        for cn in j.get("connections") or []:
            if cn["map"] in maps and layouts[maps[cn["map"]][1]["layout"]]["secondary_tileset"] != ts:
                diff.add(cn["direction"])
        for w in j["warp_events"]:
            for suffix, (kind, door) in C.KINDS.items():
                if not (w["dest_map"].endswith(suffix) and 0 <= w["x"] < Wm and 0 <= w["y"] < Hm and cell(w["x"], w["y"]) == door):
                    continue
                x, y = w["x"], w["y"]
                if kind == "CHECKPOINT":
                    cells = {(dx, dy) for dx in range(-2, 3) for dy in range(-4, 1)}
                    canvas, dx0, dy0 = art_checkpoint(), -2, -4
                elif kind == "REPO":
                    cells = {(dx, dy) for dx in range(-2, 2) for dy in range(-3, 1)}
                    canvas, dx0, dy0 = art_repo(), -2, -3
                else:
                    has = lambda X_, Y_: 0 <= X_ < Wm and 0 <= Y_ < Hm and bool(bentries(cell(X_, Y_), kind)) and cell(X_, Y_) not in C.SIGN_BLOCKS
                    left = 0
                    while has(x + left - 1, y - 1) or has(x + left - 1, y - 2):
                        left -= 1
                    right = 0
                    while has(x + right + 1, y - 1) or has(x + right + 1, y - 2):
                        right += 1
                    mark = C.TOWNS[ts][0]
                    cells = {(dx, dy) for dx in range(left, right + 1) for dy in range(-4, 1)}
                    canvas, dx0, dy0 = art_benchmark(left, right, mark), left, -4
                cells.discard((0, 0))
                parts = [(canvas, dx0, dy0, cells)]
                if kind == "BENCHMARK":
                    board = [(dx, dy) for dy in range(-3, 2) for dx in range(left - 2, right + 3)
                             if 0 <= x + dx < Wm and 0 <= y + dy < Hm and cell(x + dx, y + dy) in C.SIGN_BLOCKS]
                    tops = [(dx, dy) for dx, dy in board if cell(x + dx, y + dy) == 352]
                    bots = [(dx, dy) for dx, dy in board if cell(x + dx, y + dy) == 360]
                    for bx, by in bots:
                        tall = (bx, by - 1) in tops
                        parts.append((art_board(tall), bx, by - 1 if tall else by, {(bx, by - 1), (bx, by)} if tall else {(bx, by)}))
                absolute = {(x + dx, y + dy) for _, _, _, cs in parts for dx, dy in cs if 0 <= x + dx < Wm and 0 <= y + dy < Hm}
                near = [d for d in diff if any((d == "up" and Y_ < BAND) or (d == "down" and Y_ >= Hm - BAND) or
                                               (d == "left" and X_ < BAND) or (d == "right" and X_ >= Wm - BAND) for X_, Y_ in absolute)]
                instances.append(dict(kind=kind, mp=mp, l=l, ts=ts, x=x, y=y, parts=parts, cell=cell, near=near, bd=bd, W=Wm))

    # ---------------------------------------------------------------- the blocks each building wants
    def quadrant(canvas, cx, cy, q):
        x0, y0 = cx * 16 + (q % 2) * 8, cy * 16 + (q // 2) * 8
        if not (0 <= x0 < canvas.w and 0 <= y0 < canvas.h):
            return [None] * 64
        return [canvas.p[y0 + i // 8][x0 + i % 8] for i in range(64)]

    def plan(inst):
        """{(X, Y): (orig block, new entries)}, or a reason it cannot be drawn."""
        out = {}
        ts = inst["ts"]
        for canvas, dx0, dy0, cells in inst["parts"]:
            for dx, dy in sorted(cells):
                X_, Y_ = inst["x"] + dx, inst["y"] + dy
                if not (0 <= X_ < inst["W"] and 0 <= Y_ < inst["l"]["height"]):
                    continue
                m = inst["cell"](X_, Y_)
                e = entries(ts, m)
                if e is None:
                    return "block %d missing" % m
                new = list(out[(X_, Y_)][1]) if (X_, Y_) in out else list(e)
                for q in range(4):
                    pix = quadrant(canvas, dx - dx0, dy - dy0, q)
                    if all(v is None for v in pix):
                        continue
                    rows = {v[0] for v in pix if v is not None}
                    bottom_building = bool(e[q] & 0x3FF) and (e[q] >> 12) & 0xF in BUILDING_ROWS
                    top_px = [v if v is not None and v[0] == C.PILLAR_ROW else None for v in pix]
                    base_px = [v if v is not None and v[0] != C.PILLAR_ROW else None for v in pix]
                    brows = {v[0] for v in base_px if v is not None}
                    if len(brows) > 1:
                        return "%s (%d,%d) q%d mixes rows %s" % (inst["mp"], X_, Y_, q, sorted(brows))
                    if C.PILLAR_ROW in rows:
                        fill = max(set(v[1] for v in base_px if v), key=[v[1] for v in base_px if v].count) if brows else 6
                        new[q] = ("tile", tuple(v[1] if v else fill for v in base_px), brows.pop() if brows else 2)
                        new[4 + q] = ("tile", tuple(v[1] if v else 0 for v in top_px), C.PILLAR_ROW)
                    elif bottom_building or all(v is not None for v in pix):
                        row = brows.pop()
                        fill = max(set(v[1] for v in pix if v), key=[v[1] for v in pix if v].count)
                        if bottom_building or all(v is not None for v in pix):
                            new[q] = ("tile", tuple(v[1] if v else fill for v in pix), row)
                            new[4 + q] = 0
                    else:
                        new[4 + q] = ("tile", tuple(v[1] if v else 0 for v in pix), brows.pop())
                out[(X_, Y_)] = (m, new)
        return out

    by_ts = {}
    for inst in instances:
        by_ts.setdefault(inst["ts"], []).append(inst)
    report, active = [], {}
    for ts, insts in sorted(by_ts.items()):
        s = sec(ts)
        img = s["img"]; ip = img.load()
        slot_px = lambda n: tuple(ip[(n % 16) * 8 + k % 8, (n // 16) * 8 + k // 8] for k in range(64)) if (n // 16) * 8 + 8 <= img.height else None
        made = set(s["made"])
        referenced = set()
        for k in range(len(s["meta"]) // 16):
            if 640 + k in made:
                continue
            for t in struct.unpack_from("<8H", s["meta"], k * 16):
                if t & 0x3FF >= 640:
                    referenced.add((t & 0x3FF) - 640)
        anim = {a - 640 for a in ANIM_SLOTS.get(ts, [])}
        free = [n for n in range(s["n"]) if n not in referenced and n not in anim] + list(range(s["n"], 384))
        tiles, pool = {}, list(free)                    # pixels -> (slot, flip)

        def place(px, tiles, pool):
            if not any(px):
                return (0, 0)
            if px in tiles:
                return tiles[px]
            for flip, f in ((0x400, C.hflip), (0x800, C.vflip), (0xC00, lambda p: C.hflip(C.vflip(p)))):
                t = f(px)
                if t in tiles and tiles[t][1] == 0:
                    return (tiles[t][0], flip)
            if not pool:
                return None
            tiles[px] = (pool.pop(0), 0)
            return tiles[px]

        for inst in sorted(insts, key=lambda i: ORDER[i["kind"]]):
            where = "%s %s (%d,%d)" % (inst["kind"], inst["mp"], inst["x"], inst["y"])
            if inst["near"]:
                report.append("  %s keeps the shared drawing: within %d of the %s connection" % (where, BAND, "/".join(inst["near"]))); continue
            p = plan(inst)
            if isinstance(p, str):
                report.append("  %s keeps the shared drawing: %s" % (where, p)); continue
            trial_tiles, trial_pool = dict(tiles), list(pool)
            ok = True
            for (X_, Y_), (m, new) in p.items():
                for v in new:
                    if isinstance(v, tuple) and place(v[1], trial_tiles, trial_pool) is None:
                        ok = False; break
                if not ok:
                    break
            if not ok:
                report.append("  %s keeps the shared drawing: %s is out of tile slots" % (where, ts)); continue
            tiles, pool = trial_tiles, trial_pool
            active.setdefault(ts, []).append((inst, p))
            report.append("  %s drawn in detail" % where)
        s["tiles"] = tiles
        s["tiles_used"] = len({v[0] for v in tiles.values()})
        s["pool_left"] = len(pool)

    for line in report:
        print(line)

    # ---------------------------------------------------------------- write tiles, blocks and map cells (in memory)
    new_cells = {}
    for ts, lst in active.items():
        s = sec(ts)
        top_slot = max([s["n"] - 1] + [v[0] for v in s["tiles"].values()])
        total = max(s["n"], top_slot + 1)
        g = Image.new("P", (128, ((total + 15) // 16) * 8)); g.putpalette(s["img"].getpalette()); g.paste(s["img"], (0, 0)); gp = g.load()
        for px, (n, flip) in s["tiles"].items():
            if flip:
                continue
            for i, v in enumerate(px):
                gp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] = v
        s["grown"], s["total"] = g, total
        reuse = list(s["made"])
        made_now = []
        for inst, p in lst:
            for (X_, Y_), (m, new) in p.items():
                e = []
                for v in new:
                    if isinstance(v, tuple):
                        n, flip = s["tiles"][v[1]] if v[1] in s["tiles"] else next(
                            (s["tiles"][f(v[1])][0], fl) for fl, f in ((0x400, C.hflip), (0x800, C.vflip), (0xC00, lambda q_: C.hflip(C.vflip(q_))))
                            if f(v[1]) in s["tiles"] and s["tiles"][f(v[1])][1] == 0) if any(v[1]) else (0, 0)
                        e.append(((640 + n) | flip | (v[2] << 12)) if any(v[1]) else 0)
                    else:
                        e.append(v)
                a = attr_of(ts, m)
                key = (tuple(e), a)
                if key not in s["blocks"]:
                    nid = reuse.pop(0) if reuse else 640 + len(s["meta"]) // 16
                    k = nid - 640
                    if (k + 1) * 16 > len(s["meta"]):
                        s["meta"] += bytes(16); s["attr"] += bytes(4)
                    struct.pack_into("<8H", s["meta"], k * 16, *e); s["attr"][k * 4:(k + 1) * 4] = a
                    s["blocks"][key] = nid; made_now.append(nid)
                new_cells.setdefault(inst["mp"], {})[(X_, Y_)] = (m, s["blocks"][key], inst)
        for nid in reuse:                                # blocks this tool made before and no longer needs: blank them
            k = nid - 640
            struct.pack_into("<8H", s["meta"], k * 16, *([0] * 8)); made_now.append(nid)
        s["made_now"] = sorted(set(made_now))
        assert len(s["meta"]) // 16 <= 384, "%s: too many blocks" % ts
        assert total <= 384, "%s: too many tiles" % ts
        print("  %s: %d detail tiles, %d slots left; %d blocks" % (ts, s["tiles_used"], s["pool_left"], len(s["blocks"])))

    # map cells: every cell of an active building points at its block; cells of buildings no longer drawn go back
    new_manifest = {"cells": {}, "made": {}}
    for mid, (mp, j) in maps.items():
        l = layouts.get(j["layout"])
        if not l or l["primary_tileset"] != "gTileset_General":
            continue
        bd = bds[l["blockdata_filepath"]]; Wm = l["width"]
        for key, o in manifest["cells"].get(mp, {}).items():
            X_, Y_ = map(int, key.split(","))
            if (X_, Y_) not in new_cells.get(mp, {}):
                raw = struct.unpack_from("<H", bd, (Y_ * Wm + X_) * 2)[0]
                struct.pack_into("<H", bd, (Y_ * Wm + X_) * 2, (raw & ~0x3FF) | o)
        for (X_, Y_), (m, nid, inst) in new_cells.get(mp, {}).items():
            raw = struct.unpack_from("<H", bd, (Y_ * Wm + X_) * 2)[0]
            struct.pack_into("<H", bd, (Y_ * Wm + X_) * 2, (raw & ~0x3FF) | nid)
            new_manifest["cells"].setdefault(mp, {})["%d,%d" % (X_, Y_)] = m
    for ts, s in secs.items():
        if s.get("made_now"):
            new_manifest["made"][ts] = s["made_now"]

    # ---------------------------------------------------------------- preview: each active building, shared | detailed
    ppal = [C.read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)]
    ptiles = Image.open(os.path.join(PD, "tiles.png")); ptp = ptiles.load()
    def render(l, bd, meta, timg, x0, y0, w, h):
        sd = C.tdir(l["secondary_tileset"], "secondary")
        pals = ppal + [C.read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
        tp = timg.load(); Wm = l["width"]
        img = Image.new("RGB", (w * 16, h * 16)); o = img.load()
        for yy in range(y0, y0 + h):
            for xx in range(x0, x0 + w):
                if not (0 <= xx < Wm and 0 <= yy < l["height"]):
                    continue
                m = struct.unpack_from("<H", bd, (yy * Wm + xx) * 2)[0] & 0x3FF
                buf, k = (prim, m) if m < 640 else (meta, m - 640)
                if (k + 1) * 16 > len(buf):
                    continue
                ee = struct.unpack_from("<8H", buf, k * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = ee[layer * 4 + q]; i = t & 0x3FF
                        src, jj, hh = (ptp, i, ptiles.height) if i < 640 else (tp, i - 640, timg.height)
                        for ty in range(8):
                            for tx in range(8):
                                sy = (jj // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                v = src[(jj % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                                if layer and v == 0:
                                    continue
                                o[(xx - x0) * 16 + (q % 2) * 8 + tx, (yy - y0) * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
        return img
    panels = []
    for ts, lst in sorted(active.items()):
        s = sec(ts)
        for inst, p in lst:
            xs = [X_ for X_, _ in p]; ys = [Y_ for _, Y_ in p]
            x0, y0, w, h = min(xs) - 1, min(ys) - 1, max(xs) - min(xs) + 3, max(ys) - min(ys) + 3
            before = bytearray(inst["bd"])
            for key, o in manifest["cells"].get(inst["mp"], {}).items():
                X_, Y_ = map(int, key.split(","))
                raw = struct.unpack_from("<H", before, (Y_ * inst["W"] + X_) * 2)[0]
                struct.pack_into("<H", before, (Y_ * inst["W"] + X_) * 2, (raw & ~0x3FF) | o)
            for (X_, Y_), (m, new) in p.items():
                raw = struct.unpack_from("<H", before, (Y_ * inst["W"] + X_) * 2)[0]
                struct.pack_into("<H", before, (Y_ * inst["W"] + X_) * 2, (raw & ~0x3FF) | m)
            old_meta = open(os.path.join(s["dir"], "metatiles.bin"), "rb").read()
            a = render(inst["l"], before, old_meta, s["img"], x0, y0, w, h)
            b = render(inst["l"], inst["bd"], bytes(s["meta"]), s["grown"], x0, y0, w, h)
            panels.append(("%s %s" % (inst["kind"], inst["mp"]), a, b))
    if panels:
        cols = 3
        cw = max(a.width for _, a, _ in panels) * 2 + 12
        chh = max(a.height for _, a, _ in panels) + 14
        rows_n = (len(panels) + cols - 1) // cols
        sheet = Image.new("RGB", (cw * cols, chh * rows_n), (28, 30, 36)); d = ImageDraw.Draw(sheet)
        for k, (name, a, b) in enumerate(panels):
            X0, Y0 = (k % cols) * cw, (k // cols) * chh
            d.text((X0 + 2, Y0), name, fill=(230, 230, 230))
            sheet.paste(a, (X0, Y0 + 12)); sheet.paste(b, (X0 + a.width + 4, Y0 + 12))
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
        print("  preview %s (%d buildings: shared | detailed)" % (PREVIEW, len(panels)))

    if WRITE:
        rules = open(RULES).read()
        for ts, s in secs.items():
            if "grown" not in s:
                continue
            s["grown"].save(os.path.join(s["dir"], "tiles.png"))
            open(os.path.join(s["dir"], "metatiles.bin"), "wb").write(s["meta"])
            open(os.path.join(s["dir"], "metatile_attributes.bin"), "wb").write(s["attr"])
            at = rules.index(s["key"]) + len(s["key"])
            old = rules[at:].split()[0]
            rules = rules[:at] + str(s["total"]) + rules[at + len(old):]
        open(RULES, "w").write(rules)
        for path, bd in bds.items():
            open(os.path.join(GBA, path), "wb").write(bd)
        json.dump(new_manifest, open(MANIFEST, "w"), indent=1, sort_keys=True)
        print("  written: %d town tilesets, the maps, %s" % (sum(1 for s in secs.values() if "grown" in s), os.path.relpath(MANIFEST, ROOT)))


if __name__ == "__main__":
    main()

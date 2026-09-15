#!/usr/bin/env python3
"""The player's house as a timber cottage, with depth (T-89; vision.md 9.22).

    python3 tools/gbahouse.py            # preview to /tmp/house.png (the concept drawn | the game's own render of it)
    python3 tools/gbahouse.py --write    # a new tileset gTileset_PlayersHouse, both floors' maps pointed at it

WHY ITS OWN TILESET. Both floors are drawn almost entirely from gTileset_Building,
the primary every interior in the game loads (184 layouts), so redrawing those
tiles would redraw shops and houses alike. The house gets a secondary tileset of
its own instead -- the route CRYSTAL CLEAR's lab took (T-54) -- and every cell of
both floors a block of it.

THE LAYOUT is new, and PLAN below is its truth: which cells are open, and the
behaviour of each one that has any. The map sizes, the exit mat, both stair warps,
the PORT at (1,1), the TV at (6,1), the note at (11,1) and the wake-up cell (6,6)
stay where they were; MOM stands in her kitchen at (3,3) and the console sits at
(9,6) -- both moved in the maps' map.json, which this tool does not write.

THE DRAWING follows vanilla's rooms, which read as a box because:
  * the camera looks down from the south, so an object shows a lit top face and a
    darker front face, and tall things rise up over the wall behind them;
  * light comes from the upper left;
  * every object sits on a contact shadow;
  * the floor darkens where it meets the back wall, and the left edge is a side
    wall in shadow.
Furniture stands on the cells whose behaviour it is: the counter and stove on
the two KITCHEN cells, the dresser on the CABINET cells, the set on the
TELEVISION cell, the window on the WINDOW cell; upstairs the PORT on the desk at
(1,1), the chest of drawers on the DRESSER cell, the books on the BOOKSHELF cells.

COLOUR. Six palette rows, one per material -- wood, walls, stone and iron and
glass, fire and copper, fabric, greens and books. The room is drawn in full
colour, then each 8x8 tile is given whichever row reproduces it best, pixel by
nearest pixel. Textures sit on the 8-pixel grid (boards eight tall, joints every
16 or 32, planks every 8) so tiles repeat, and mirrored tiles are shared.
"""
import json, math, os, re, struct, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
BASE = os.path.join(GBA, "data/tilesets/secondary/generic_building_1")
PRIM = os.path.join(GBA, "data/tilesets/primary/building")
OUT_DIR = os.path.join(GBA, "data/tilesets/secondary/players_house")
PREVIEW = "/tmp/house.png"
WRITE = "--write" in sys.argv
LAYOUTS = ("PalletTown_PlayersHouse_1F_Layout", "PalletTown_PlayersHouse_2F_Layout")

C = dict(
    OUT=(38, 26, 22), BEAM=(80, 52, 36), BEAMD=(56, 36, 26), BEAML=(112, 76, 52),
    WALL=(198, 152, 106), WALLL=(220, 178, 128), WALLD=(164, 120, 82), SEAM=(140, 98, 64),
    SIDE=(120, 84, 58), SIDED=(96, 66, 46),
    FLOOR=(186, 132, 82), FLOORL=(208, 156, 102), FLOORD=(154, 106, 66), FLOORS=(126, 86, 54),
    SHADE=(118, 80, 50), SHADE2=(142, 98, 62),
    WOODT=(214, 166, 112), WOODF=(150, 100, 62), WOODD=(110, 72, 44),
    STONET=(196, 192, 184), STONE=(158, 154, 148), STONED=(112, 108, 104), MORTAR=(128, 124, 118),
    SOOT=(44, 36, 34), FIRE=(252, 196, 80), FIRE2=(236, 132, 52), EMBER=(190, 70, 36), GLOW=(214, 150, 96),
    IRONT=(120, 122, 134), IRON=(74, 76, 88), IROND=(48, 50, 58),
    CREAM=(238, 226, 200), CREAMD=(206, 190, 160), WHITE=(248, 246, 240),
    SKY=(168, 210, 236), SKYL=(222, 240, 250), SKYD=(120, 168, 200), CHK=(196, 88, 78),
    RUG1=(178, 90, 74), RUG2=(226, 212, 184), RUG3=(112, 142, 98), RUG4=(214, 180, 98), RUG5=(98, 122, 162), RUGD=(120, 76, 56),
    Q1=(172, 86, 78), Q2=(218, 188, 122), Q3=(106, 134, 170), QD=(128, 70, 64),
    GREEN=(90, 148, 82), GREENL=(146, 196, 112), GREEND=(58, 104, 60),
    POT=(186, 104, 70), POTD=(140, 72, 48), POTT=(210, 136, 96),
    SCREEN=(62, 90, 110), SCREENL=(128, 168, 188), SCREEND=(40, 58, 74),
    BOOK1=(150, 66, 58), BOOK2=(74, 98, 142), BOOK3=(98, 128, 80), BOOK4=(202, 172, 92), BOOK5=(122, 92, 128),
    LED=(236, 96, 72), COPPER=(200, 124, 74), VOID=(16, 12, 10),
)
ROWS = {                                             # palette rows 7..12, fifteen colours each, by material
    7: ["OUT", "BEAMD", "BEAM", "BEAML", "WOODD", "WOODF", "WOODT", "FLOORS", "FLOORD", "FLOOR", "FLOORL", "SHADE", "SHADE2", "CREAM", "CREAMD"],
    8: ["OUT", "SIDED", "SIDE", "SEAM", "WALLD", "WALL", "WALLL", "BEAMD", "BEAM", "BEAML", "WOODD", "WOODF", "WOODT", "VOID", "CREAM"],
    9: ["OUT", "SOOT", "STONED", "MORTAR", "STONE", "STONET", "WHITE", "IROND", "IRON", "IRONT", "SCREEND", "SCREEN", "SCREENL", "SKYD", "SKY"],
    10: ["OUT", "SOOT", "STONED", "MORTAR", "STONE", "STONET", "EMBER", "FIRE2", "FIRE", "GLOW", "IROND", "IRON", "WHITE", "CHK", "SHADE"],   # the hearth row: fire with its stone and iron
    11: ["OUT", "RUGD", "RUG1", "RUG2", "RUG3", "RUG4", "RUG5", "Q1", "Q2", "Q3", "QD", "FLOOR", "FLOORL", "FLOORS", "SHADE2"],
    12: ["OUT", "GREEND", "GREEN", "GREENL", "BOOK1", "BOOK2", "BOOK3", "BOOK4", "BOOK5", "WOODD", "WOODF", "WOODT", "POT", "POTD", "FLOOR"],
}


# ================================================================== drawing
class Room:
    def __init__(self, w, h):
        self.w, self.h = w * 16, h * 16
        self.im = Image.new("RGB", (self.w, self.h), C["VOID"]); self.p = self.im.load()

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[x, y] = C[c] if isinstance(c, str) else c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def shadow(self, x0, y0, x1, y1, k=0.72):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < self.w and 0 <= y < self.h:
                    r, g, b = self.p[x, y]
                    self.p[x, y] = (int(r * k), int(g * k), int(b * k))

    def box(self, x0, y0, x1, y1, top_h, top="WOODT", front="WOODF", dark="WOODD", shadow=True):
        """top face and front face, lit left, dark right, outlined, on a contact shadow"""
        if shadow:
            self.shadow(x0 + 2, y1 + 1, x1 + 3, y1 + 3)
            self.shadow(x1 + 1, y0 + top_h + 2, x1 + 3, y1)
        self.rect(x0, y0, x1, y0 + top_h, top)
        self.rect(x0, y0 + top_h + 1, x1, y1, front)
        self.hline(x0, x1, y0 + top_h + 1, dark); self.vline(x1, y0, y1, dark)
        self.hline(x0, x1, y1, "OUT"); self.vline(x0 - 1, y0, y1, "OUT"); self.vline(x1 + 1, y0, y1, "OUT"); self.hline(x0, x1, y0 - 1, "OUT")

    def ellipse(self, cx, cy, rx, ry, fn):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                if d <= 1:
                    fn(x, y, d)


def shell(r, attic=False, void_bottom=False):
    W, H = r.w, r.h
    for y in range(32, H):
        board = (y - 32) // 8
        for x in range(8, W):
            v = "FLOOR"
            if (y - 32) % 8 == 0:
                v = "FLOORS"
            elif (y - 32) % 8 == 1:
                v = "FLOORL"
            elif (x + (16 if board % 2 else 0)) % 32 == 0:
                v = "FLOORD"
            r.px(x, y, v)
    r.shadow(8, 32, W - 1, 33, 0.7); r.shadow(8, 34, W - 1, 35, 0.85)
    for y in range(0, 32):
        for x in range(8, W):
            r.px(x, y, {0: "SEAM", 1: "WALLL", 7: "WALLD"}.get(x % 8, "WALL"))
    r.rect(8, 0, W - 1, 5, "BEAM"); r.hline(8, W - 1, 5, "BEAML"); r.hline(8, W - 1, 6, "BEAMD")
    r.rect(8, 27, W - 1, 31, "WOODF"); r.hline(8, W - 1, 27, "WOODT"); r.hline(8, W - 1, 31, "OUT")
    if attic:
        for x0 in range(16, W, 32):
            for k in range(20):
                r.px(x0 + k, 7 + k, "BEAMD"); r.px(x0 + k + 1, 7 + k, "BEAM"); r.px(x0 + k + 2, 7 + k, "BEAML")
    for y in range(0, H):
        for x in range(0, 8):
            r.px(x, y, "SIDED" if x < 2 or y % 8 == 0 else "SIDE")
    r.vline(7, 0, H - 1, "OUT"); r.shadow(8, 32, 11, H - 1, 0.8)
    if void_bottom:
        r.rect(0, H - 16, W - 1, H - 1, "VOID")


def window(r, x0, y0, w, h, deep=False):
    if deep:
        r.rect(x0 - 3, y0 - 2, x0 + w + 2, y0 + h + 2, "BEAMD")
    r.rect(x0, y0, x0 + w - 1, y0 + h, "BEAM")
    r.rect(x0 + 2, y0 + 2, x0 + w - 3, y0 + h - 3, "SKY"); r.rect(x0 + 2, y0 + 2, x0 + w // 2 - 2, y0 + 5, "SKYL")
    r.rect(x0 + 2, y0 + h - 5, x0 + w - 3, y0 + h - 3, "SKYD")
    r.vline(x0 + w // 2, y0 + 2, y0 + h - 3, "BEAM"); r.hline(x0 + 2, x0 + w - 3, y0 + h // 2, "BEAM")
    r.rect(x0 - 2, y0 + h + 1, x0 + w + 1, y0 + h + 2, "WOODT"); r.rect(x0 - 2, y0 + h + 3, x0 + w + 1, y0 + h + 3, "WOODD")
    r.shadow(x0 - 1, y0 + h + 4, x0 + w + 2, y0 + h + 5)
    cw = max(3, w // 6)
    for cx in (x0 + 1, x0 + w - 1 - cw):
        for y in range(y0 + 1, y0 + h - 1):
            for x in range(cx, cx + cw):
                r.px(x, y, "CHK" if (x // 2 + y // 2) % 2 else "WHITE")


def rug(r, cx, cy, rx, ry):
    bands = ["RUG1", "RUG2", "RUG3", "RUG4", "RUG5", "RUG2", "RUG1", "RUG4"]
    r.ellipse(cx + 1, cy + 2, rx, ry, lambda x, y, d: r.px(x, y, "SHADE2"))
    def paint(x, y, d):
        c = bands[int((1 - math.sqrt(d)) * 12) % len(bands)]
        if d > 0.9 and y < cy:
            c = "RUG2"
        if d > 0.93 and y >= cy:
            c = "RUGD"
        r.px(x, y, c)
    r.ellipse(cx, cy, rx, ry, paint)


def plant(r, x0, y0):
    r.shadow(x0 + 2, y0 + 21, x0 + 15, y0 + 23)
    r.rect(x0 + 2, y0 + 12, x0 + 12, y0 + 20, "POT"); r.vline(x0 + 12, y0 + 12, y0 + 20, "POTD"); r.vline(x0 + 2, y0 + 12, y0 + 20, "POTT")
    r.hline(x0 + 2, x0 + 12, y0 + 20, "OUT"); r.rect(x0 + 1, y0 + 10, x0 + 13, y0 + 11, "POTT"); r.hline(x0 + 1, x0 + 13, y0 + 12, "POTD")
    for dx, dy, c in ((6, 0, "GREEND"), (2, 3, "GREEN"), (9, 2, "GREEN"), (4, 6, "GREENL"), (10, 6, "GREEN"), (6, 4, "GREENL"), (1, 8, "GREEND"), (12, 8, "GREEND")):
        r.rect(x0 + dx, y0 + dy, x0 + dx + 3, y0 + dy + 3, c)


def chair(r, cx, cy, back):
    if back == "up":
        r.rect(cx - 6, cy - 14, cx + 6, cy - 3, "WOODF"); r.hline(cx - 6, cx + 6, cy - 14, "WOODT"); r.vline(cx + 6, cy - 14, cy - 3, "WOODD")
        r.rect(cx - 4, cy - 11, cx + 4, cy - 9, "WOODD")
    r.shadow(cx - 4, cy + 7, cx + 9, cy + 9)
    r.rect(cx - 7, cy - 2, cx + 7, cy + 2, "WOODT"); r.rect(cx - 7, cy + 3, cx + 7, cy + 5, "WOODF"); r.hline(cx - 7, cx + 7, cy + 6, "OUT")
    r.rect(cx - 7, cy + 6, cx - 6, cy + 9, "WOODD"); r.rect(cx + 6, cy + 6, cx + 7, cy + 9, "WOODD")
    if back == "down":
        r.rect(cx - 7, cy - 12, cx + 7, cy - 1, "WOODF"); r.hline(cx - 7, cx + 7, cy - 12, "WOODT")
        r.rect(cx - 5, cy - 9, cx + 5, cy - 4, "WOODD"); r.vline(cx + 7, cy - 12, cy + 5, "WOODD"); r.hline(cx - 7, cx + 7, cy - 1, "OUT")


def armchair(r, cx, cy, facing):
    """a padded armchair side-on, seen from above and the south: a tall back on the
    outer side, an arm roll either side of the seat, a skirt in shadow along the front"""
    x0, x1, top, bot = cx - 11, cx + 11, cy - 13, cy + 11
    r.shadow(x0 + 3, bot + 1, x1 + 4, bot + 4); r.shadow(x1 + 2, top + 6, x1 + 4, bot)
    bx0, bx1 = (x0, x0 + 6) if facing == "right" else (x1 - 6, x1)
    sx0, sx1 = (bx1 + 1, x1) if facing == "right" else (x0, bx0 - 1)
    r.rect(x0, top + 4, x1, bot, "Q1")
    r.rect(bx0, top, bx1, bot - 7, "Q1"); r.hline(bx0, bx1, top, "RUG2"); r.hline(bx0, bx1, top + 1, "Q2")
    r.vline(bx1 if facing == "right" else bx0, top + 2, bot - 7, "QD")
    r.rect(sx0, top + 4, sx1, top + 8, "Q1"); r.hline(sx0, sx1, top + 4, "RUG2"); r.hline(sx0, sx1, top + 9, "QD")
    r.rect(sx0 + 1, top + 10, sx1 - 1, bot - 11, "Q2"); r.hline(sx0 + 1, sx1 - 1, top + 10, "RUG2")
    r.rect(sx0, bot - 10, sx1, bot - 7, "Q1"); r.hline(sx0, sx1, bot - 10, "RUG2")
    r.rect(x0, bot - 6, x1, bot, "QD"); r.hline(x0, x1, bot - 6, "RUGD")
    r.hline(bx0, bx1, top - 1, "OUT"); r.hline(sx0, sx1, top + 3, "OUT"); r.hline(x0, x1, bot, "OUT")
    r.vline(x0 - 1, top if facing == "right" else top + 4, bot, "OUT"); r.vline(x1 + 1, top + 4 if facing == "right" else top, bot, "OUT")


def bench(r, x0, y0, x1):
    r.shadow(x0 + 2, y0 + 9, x1 + 3, y0 + 11)
    r.rect(x0, y0, x1, y0 + 3, "WOODT"); r.hline(x0, x1, y0, "CREAM"); r.rect(x0, y0 + 4, x1, y0 + 6, "WOODF"); r.hline(x0, x1, y0 + 7, "OUT")
    r.vline(x0 - 1, y0, y0 + 7, "OUT"); r.vline(x1 + 1, y0, y0 + 7, "OUT"); r.hline(x0, x1, y0 - 1, "OUT")
    for x in (x0 + 1, x1 - 2):
        r.rect(x, y0 + 8, x + 1, y0 + 10, "WOODD")


def rect_table(r, x0, y0, x1, y1):
    r.shadow(x0 + 3, y1 + 4, x1 + 4, y1 + 7)
    for x in (x0 + 1, x1 - 2):
        r.rect(x, y1 + 1, x + 1, y1 + 5, "WOODD")
    r.rect(x0, y0, x1, y1 - 4, "WOODT"); r.hline(x0, x1, y0, "CREAM"); r.rect(x0, y1 - 3, x1, y1, "WOODF"); r.hline(x0, x1, y1, "OUT")
    r.vline(x1, y0, y1, "WOODD"); r.vline(x0 - 1, y0, y1, "OUT"); r.vline(x1 + 1, y0, y1, "OUT"); r.hline(x0, x1, y0 - 1, "OUT")


def hearth(r, x0):
    """the stone chimney breast on the back wall, two cells wide, its hearthstone lit"""
    x1 = x0 + 31
    r.rect(x0, 0, x1, 31, "STONE")
    for y in range(1, 31, 5):
        r.hline(x0, x1, y, "MORTAR")
        for x in range(x0 + (4 if (y // 5) % 2 else 0), x1 + 1, 8):
            r.vline(x, y, y + 4, "MORTAR")
    r.vline(x0, 0, 31, "STONET"); r.vline(x1, 0, 31, "STONED")
    r.rect(x0 + 6, 12, x1 - 6, 31, "SOOT")
    for k, x in enumerate(range(x0 + 8, x1 - 7, 3)):
        r.rect(x, 20 + (k % 2) * 3, x + 1, 30, "FIRE" if k % 2 else "FIRE2")
    # the mantel and hearthstone are stone and stop at the breast's own edges: a tile holding stone and the wall
    # or the floor has no palette row to be drawn in
    r.rect(x0, 9, x1, 10, "STONET"); r.hline(x0, x1, 11, "STONED")
    r.rect(x0 + 7, 28, x1 - 7, 31, "EMBER")
    r.rect(x0, 32, x1, 37, "STONET"); r.hline(x0, x1, 32, "WHITE"); r.rect(x0, 38, x1, 39, "STONED"); r.hline(x0, x1, 40, "OUT")
    r.rect(x0 + 6, 33, x1 - 6, 36, "GLOW"); r.shadow(x0 + 1, 41, x1 + 2, 42)


def first_floor():
    r = Room(13, 10); shell(r, void_bottom=True)
    # one stone splashback behind the basin and the stove: stone, water and iron share no palette row with the
    # wall, so every tile holding them is kept clear of it
    r.rect(16, 8, 47, 13, "STONE"); r.hline(16, 47, 8, "STONET"); r.hline(16, 47, 11, "MORTAR")
    for x in (24, 40):
        r.vline(x, 8, 10, "MORTAR")
    # x1: the stone basin, its apron down to the tile edge, a wooden cupboard under (KITCHEN)
    r.box(17, 14, 31, 38, 5, top="STONET", front="WOODF", dark="STONED")
    r.rect(17, 21, 31, 23, "STONE"); r.hline(17, 31, 23, "STONED"); r.vline(31, 24, 37, "WOODD")
    r.rect(19, 15, 28, 18, "STONED"); r.rect(20, 16, 27, 17, "SKY"); r.px(21, 16, "WHITE")
    r.rect(19, 25, 29, 36, "WOODD"); r.rect(20, 26, 28, 35, "WOODF"); r.px(27, 30, "WOODT")
    # x2: the iron stove and its pipe (KITCHEN); the pipe is a dark silhouette across the beam, iron against the stone
    r.rect(37, 0, 40, 7, "OUT"); r.vline(37, 0, 7, "BEAMD")
    r.rect(37, 8, 40, 13, "IROND"); r.vline(37, 8, 13, "IRON")
    r.box(33, 14, 46, 38, 4, top="IRONT", front="IRON", dark="IROND")
    r.rect(36, 24, 43, 33, "IROND"); r.rect(37, 26, 42, 31, "EMBER"); r.rect(38, 27, 41, 30, "FIRE2")
    # x3..4: the counter and its cupboards (CABINET), a shelf of jars above
    r.box(49, 14, 78, 38, 5, top="CREAM", front="WOODF", dark="WOODD")
    for x in (51, 65):
        r.rect(x, 24, x + 11, 36, "WOODD"); r.rect(x + 1, 25, x + 10, 35, "WOODF"); r.px(x + (10 if x == 51 else 1), 30, "COPPER")
    # x5, rows 1..3: the peninsula, a long worktop running into the room, its end the only front
    # (as tall as the back counter, so its top reaches y 39 and its front, doors and all, the floor at row 3)
    r.box(81, 14, 94, 62, 25, top="CREAM", front="WOODF", dark="WOODD")
    r.rect(83, 44, 92, 60, "WOODD"); r.rect(84, 45, 91, 59, "WOODF"); r.px(90, 52, "COPPER")
    r.rect(83, 17, 92, 25, "WOODT"); r.hline(83, 92, 26, "WOODD"); r.vline(92, 17, 26, "WOODD")   # a chopping board
    r.ellipse(88, 33, 5, 3, lambda x, y, d: r.px(x, y, "POTD" if d > 0.55 else "GREENL"))       # a bowl
    # the runner MOM stands on
    for y in range(44, 58):
        for x in range(20, 77):
            r.px(x, y, "RUGD" if y in (44, 57) else ("RUG4" if (y // 3) % 2 else "RUG1"))
    r.shadow(21, 58, 77, 59, 0.8)
    # x6: the TV on its cabinet (TELEVISION) -- the set fills the cell from y 8 to 23 and the cabinet from 24, so
    # no tile holds iron with the wall or the wood
    r.box(97, 24, 110, 38, 3, top="WOODT", front="WOODF", dark="WOODD", shadow=False)
    r.shadow(98, 39, 111, 39); r.shadow(98, 41, 111, 41)      # not the floor seam at y 40: a darker seam is in no row with the armchair
    r.box(97, 9, 110, 22, 2, top="IRONT", front="IROND", dark="IROND", shadow=False); r.hline(97, 110, 23, "OUT")
    r.vline(96, 8, 23, "OUT"); r.vline(111, 8, 23, "OUT")
    r.rect(99, 13, 108, 20, "SCREEN"); r.rect(100, 14, 102, 16, "SCREENL"); r.hline(99, 108, 20, "SCREEND")
    # x7..8: the hearth; x9: the window (WINDOW)
    hearth(r, 112)
    window(r, 146, 5, 12, 14)
    # x10..12: the stairs up, treads and risers, a banister
    x0, bottom, steps = 162, 62, 8
    for k in range(steps):
        y = bottom - k * 7; xs = x0 + k * 4
        r.rect(xs, y - 6, 207, y - 4, "WOODT"); r.hline(xs, 207, y - 6, "CREAM")
        r.rect(xs, y - 3, 207, y, "WOODF"); r.hline(xs, 207, y, "WOODD"); r.vline(xs, y - 6, y, "WOODD")
    for k in range(steps):
        px_, py = x0 + k * 4 + 1, bottom - k * 7
        r.rect(px_, py - 15, px_ + 1, py - 7, "WOODD"); r.px(px_, py - 15, "WOODT")
    for k in range(steps * 7 + 3):
        r.px(x0 + k * 4 // 7, bottom - 15 - k, "BEAML"); r.px(x0 + k * 4 // 7, bottom - 14 - k, "BEAMD")
    r.shadow(160, 63, 207, 65)
    # the fireside: a rug, and an armchair either side on (6,3) and (9,3)
    rug(r, 128, 60, 26, 13)
    armchair(r, 105, 55, "right"); armchair(r, 150, 55, "left")
    plant(r, 192, 56); plant(r, 192, 104)
    # the dining table on (1..2,6), a bench on the rows either side -- clear of the mat
    bench(r, 18, 80, 44)
    rect_table(r, 18, 94, 44, 108)
    bench(r, 18, 115, 44)
    # the doormat over the exit
    for y in range(130, 146):
        for x in range(52, 92):
            r.px(x, y, "RUG4" if (x // 4 + y // 4) % 2 else "WOODF")
    r.hline(52, 91, 130, "CREAM"); r.rect(52, 146, 91, 147, "WOODD")
    return r


def second_floor():
    r = Room(12, 9); shell(r, attic=True)
    # x1..2: the desk, the PORT on it at (1,1), its chair pushed in on (2,2)
    r.box(17, 18, 46, 40, 5, top="WOODT", front="WOODF", dark="WOODD")
    r.rect(35, 27, 45, 38, "WOODD"); r.rect(36, 28, 44, 32, "WOODF"); r.rect(36, 34, 44, 37, "WOODF"); r.px(40, 30, "COPPER"); r.px(40, 35, "COPPER")
    r.box(19, 4, 32, 17, 2, top="IRONT", front="IRON", dark="IROND", shadow=False)
    r.rect(21, 8, 30, 15, "SCREEN"); r.rect(22, 9, 24, 11, "SCREENL"); r.px(29, 15, "LED")
    r.rect(20, 19, 31, 21, "IRONT"); r.hline(20, 31, 22, "IROND")
    chair(r, 40, 47, "down")
    # x3..4: the bookshelf (BOOKSHELF)
    r.box(50, 0, 77, 40, 2, top="WOODT", front="WOODD", dark="OUT")
    for k, y in enumerate((5, 16, 27)):
        for x in range(52, 76, 3):
            h = 8 - ((x // 3 + k) % 3)
            r.rect(x, y + (9 - h), x + 1, y + 9, ["BOOK1", "BOOK2", "BOOK3", "BOOK4", "BOOK5"][(x // 3 + k) % 5])
        r.hline(51, 76, y + 10, "WOODT")
    # x5..6: the dormer window (WINDOW); x7: a narrow chest of drawers (DRESSER)
    window(r, 84, 3, 28, 16, deep=True)
    r.box(116, 10, 124, 40, 3, top="WOODT", front="WOODF", dark="WOODD")
    for y in (18, 25, 32):
        r.hline(116, 124, y, "WOODD"); r.px(120, y + 3, "COPPER")
    # the bed under the dormer on (5..6, 2..3), head to the wall, a chest at its foot on row 4
    r.shadow(86, 67, 118, 69); r.shadow(116, 30, 118, 66)
    r.rect(84, 24, 115, 32, "WOODF"); r.hline(84, 115, 24, "WOODT"); r.vline(115, 24, 32, "WOODD")
    r.rect(86, 33, 113, 40, "WHITE"); r.hline(86, 113, 40, "CREAMD"); r.rect(89, 34, 98, 38, "CREAM"); r.rect(101, 34, 110, 38, "CREAM")
    for y in range(41, 58):
        for x in range(86, 114):
            r.px(x, y, "QD" if x == 113 else ["Q1", "Q2", "Q3", "RUG2"][((x - 86) // 8 + (y - 41) // 8) % 4])
    r.rect(86, 58, 113, 61, "QD")
    r.rect(84, 62, 115, 66, "WOODF"); r.hline(84, 115, 62, "WOODT"); r.hline(84, 115, 66, "OUT"); r.vline(83, 24, 66, "OUT"); r.vline(116, 24, 66, "OUT")
    r.box(88, 69, 111, 79, 3, top="WOODT", front="WOODF", dark="WOODD")
    r.rect(97, 74, 102, 76, "COPPER")
    # x8..10: the stairwell, an opening behind a railing, the treads going down
    r.rect(128, 24, 175, 60, "SOOT")
    for k in range(5):
        r.rect(130 + k * 5, 28 + k * 6, 175, 30 + k * 6, "WOODF"); r.hline(130 + k * 5, 175, 28 + k * 6, "WOODT")
    r.rect(126, 18, 128, 62, "WOODF"); r.vline(126, 18, 62, "WOODT"); r.vline(128, 18, 62, "WOODD")
    for x in range(130, 160, 6):
        r.rect(x, 58, x + 1, 66, "WOODD"); r.px(x, 58, "WOODT")
    r.rect(126, 55, 161, 56, "WOODT"); r.hline(126, 161, 57, "WOODD"); r.shadow(128, 67, 163, 69)
    # x11: the pinned note (signpost)
    r.shadow(181, 13, 189, 26)
    r.rect(178, 10, 188, 23, "CREAM"); r.vline(188, 10, 23, "CREAMD"); r.px(183, 11, "CHK")
    for y in (14, 17, 20):
        r.hline(180, 186, y, "WOODF")
    # the console corner, rows 5..8 on the right: a rug; the set on its low cabinet on
    # (10..11,5); the console on the floor on (9,6), its lead up to the set; a crate of
    # games on (11,6); a floor cushion on (8,6)
    rug(r, 144, 108, 26, 13)                             # downstairs' fireside rug on the same grid phase: its edge tiles are shared
    r.box(163, 84, 188, 95, 3, top="WOODT", front="WOODF", dark="WOODD")
    r.rect(166, 89, 175, 94, "WOODD"); r.rect(177, 89, 186, 94, "WOODD")
    r.box(167, 66, 184, 83, 2, top="IRONT", front="IRON", dark="IROND", shadow=False)
    r.rect(170, 71, 181, 81, "SCREEN"); r.rect(171, 72, 175, 75, "SCREENL"); r.hline(170, 181, 81, "SCREEND")
    r.shadow(147, 108, 160, 110)
    r.rect(146, 99, 157, 102, "IRONT"); r.hline(146, 157, 99, "WHITE"); r.rect(146, 103, 157, 106, "IRON"); r.hline(146, 157, 107, "OUT")
    r.vline(145, 99, 107, "OUT"); r.vline(158, 99, 107, "OUT"); r.px(148, 105, "LED"); r.rect(151, 104, 156, 105, "IROND")
    for k in range(9):
        r.px(158 + k, 101 - k // 2, "IROND")
    r.box(178, 102, 189, 111, 3, top="WOODT", front="WOODF", dark="WOODD")
    for x, c in ((180, "BOOK1"), (183, "BOOK2"), (186, "BOOK4")):
        r.rect(x, 97, x + 1, 102, c)
    r.shadow(127, 113, 141, 115)
    r.rect(125, 102, 139, 112, "Q3"); r.hline(125, 139, 102, "RUG2"); r.rect(125, 109, 139, 112, "QD"); r.hline(125, 139, 113, "OUT")
    r.rect(129, 104, 135, 107, "RUG5")
    return r


# ================================================================== the plan: collision and behaviour
# '.' walkable, '#' blocked; every other cell's behaviour is 0
MB = dict(KITCHEN=0x8A, CABINET=0x89, TELEVISION=0x86, WINDOW=0x9D, BOOKSHELF=0x81, DRESSER=0x8B, SIGNPOST=0x84,
          WARP_UP=0x6C, WARP_DOWN=0x6F, SOUTH_ARROW_WARP=0x65)
PLAN = {
    LAYOUTS[0]: ([
        "#############",
        "#############",
        "#....#.....##",      # (5,2) the peninsula; (10,2) the stairs
        "#....##..#...",      # MOM at (3,3); the armchairs at (6,3) and (9,3)
        "#...........#",      # a plant at (12,4)
        "###..........",      # the dining benches and table, (1..2, 5..7)
        "###..........",
        "###.........#",      # a plant at (12,7)
        "#............",      # the mat (3..5,8)
        "#############",
    ], {(1, 1): "KITCHEN", (2, 1): "KITCHEN", (3, 1): "CABINET", (4, 1): "CABINET", (6, 1): "TELEVISION",
        (9, 1): "WINDOW", (10, 2): "WARP_UP", (4, 8): "SOUTH_ARROW_WARP"}),
    LAYOUTS[1]: ([
        "############",
        "############",
        "#.#..##.##..",       # the desk chair (2,2); the bed (5..6, 2..3); the stairwell (8..9); (10,2) the stairs
        "#....##.##..",
        "#....##.....",       # the chest at the bed's foot (5..6,4)
        "#.........##",       # the set (10..11,5)
        "#........#.#",       # the console (9,6), the crate (11,6), a floor cushion (8,6); the player wakes at (6,6)
        "#...........",
        "#...........",
    ], {(3, 1): "BOOKSHELF", (4, 1): "BOOKSHELF", (5, 1): "WINDOW", (6, 1): "WINDOW", (7, 1): "DRESSER",
        (11, 1): "SIGNPOST", (10, 2): "WARP_DOWN", (10, 5): "TELEVISION", (11, 5): "TELEVISION"}),
}
WALK, BLOCK = 12 << 10, 1 << 10       # the map's collision and elevation bits: elevation 3 open, or collision 1


# ================================================================== tiles, blocks, palettes
def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, cols):
    open(path, "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols))


def hflip(px):
    return tuple(px[(i // 8) * 8 + 7 - i % 8] for i in range(64))


def vflip(px):
    return tuple(px[(7 - i // 8) * 8 + i % 8] for i in range(64))


def main():
    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    rows = {r: [(255, 0, 255)] + [C[n] for n in names] for r, names in ROWS.items()}
    rooms = {LAYOUTS[0]: first_floor(), LAYOUTS[1]: second_floor()}
    tiles, tile_list, blocks, block_list, attrs = {}, [], {}, [], []
    new_maps, total_err, used_rows, uses = {}, 0, {}, {}

    def place(px):
        if px in tiles:
            return tiles[px]
        for flip, f in ((0x400, hflip), (0x800, vflip), (0xC00, lambda p: hflip(vflip(p)))):
            t = f(px)
            if t in tiles and tiles[t][1] == 0:
                return (tiles[t][0], flip)
        tiles[px] = (len(tile_list), 0); tile_list.append(px)
        return tiles[px]

    for name, room in rooms.items():
        lay = layouts[name]; W, H = lay["width"], lay["height"]
        bd = bytearray(W * H * 2)
        grid, behaviours = PLAN[name]
        assert len(grid) == H and all(len(row) == W for row in grid), "the plan for %s is not %dx%d" % (name, W, H)
        for cy in range(H):
            for cx in range(W):
                raw = WALK if grid[cy][cx] == "." else BLOCK
                entries = []
                for q in range(4):
                    x0, y0 = cx * 16 + (q % 2) * 8, cy * 16 + (q // 2) * 8
                    rgb = [room.p[x0 + i % 8, y0 + i // 8] for i in range(64)]
                    best = None
                    for r, pal in rows.items():
                        idx, err = [], 0
                        for c in rgb:
                            k, e = min(((k, sum((c[j] - pal[k][j]) ** 2 for j in range(3))) for k in range(1, 16)), key=lambda t: t[1])
                            idx.append(k); err += e
                        if best is None or err < best[1]:
                            best = (r, err, tuple(idx))
                    r, err, idx = best
                    total_err += err; used_rows[r] = used_rows.get(r, 0) + 1
                    n, flip = place(idx)
                    uses.setdefault(n, []).append((name[:25], cx, cy))
                    entries.append((640 + n) | flip | (r << 12))
                a = struct.pack("<I", MB[behaviours[(cx, cy)]] if (cx, cy) in behaviours else 0)   # bottom layer only: NORMAL
                key = (tuple(entries), a)
                if key not in blocks:
                    blocks[key] = 640 + len(block_list); block_list.append(entries + [0, 0, 0, 0]); attrs.append(a)
                struct.pack_into("<H", bd, (cy * W + cx) * 2, (raw & ~0x3FF) | blocks[key])
        new_maps[name] = bd
    quads = max(1, sum(used_rows.values()))
    print("  %d tiles (of 384), %d blocks (of 384); tiles by row %s; mean squared colour error per pixel %.1f" % (
        len(tile_list), len(block_list), dict(sorted(used_rows.items())), total_err / (quads * 64)))
    over = len(tile_list) > 384 or len(block_list) > 384
    if over:
        print("  OVER BUDGET: the preview is drawn, nothing will be written")
        once = {}
        for n, where in uses.items():
            if len(where) == 1:
                once[where[0]] = once.get(where[0], 0) + 1
        print("  cells holding the most tiles used nowhere else:", sorted(once.items(), key=lambda t: -t[1])[:16])

    # preview: the concept as drawn | the game's render of the tiles and palettes
    def render(name):
        lay = layouts[name]; W, H = lay["width"], lay["height"]; bd = new_maps[name]
        if over:                                   # tile ids past 10 bits: nothing to render yet
            return rooms[name].im.copy()
        out = Image.new("RGB", (W * 16, H * 16)); o = out.load()
        for cy in range(H):
            for cx in range(W):
                m = struct.unpack_from("<H", bd, (cy * W + cx) * 2)[0] & 0x3FF
                for q, t in enumerate(block_list[m - 640][:4]):
                    px = tile_list[(t & 0x3FF) - 640]; pal = rows[(t >> 12) & 0xF]
                    for i in range(64):
                        x, y = i % 8, i // 8
                        if t & 0x400: x = 7 - x
                        if t & 0x800: y = 7 - y
                        o[cx * 16 + (q % 2) * 8 + x, cy * 16 + (q // 2) * 8 + y] = pal[px[i]]
        return out
    def plan(name):
        out = render(name); d = ImageDraw.Draw(out, "RGBA"); grid, behaviours = PLAN[name]
        for cy, row in enumerate(grid):
            for cx, c in enumerate(row):
                if c == "#":
                    d.rectangle((cx * 16, cy * 16, cx * 16 + 15, cy * 16 + 15), fill=(220, 40, 40, 90))
        for (cx, cy) in behaviours:
            d.rectangle((cx * 16, cy * 16, cx * 16 + 15, cy * 16 + 15), outline=(255, 230, 60, 255))
        return out
    panels = [(rooms[n].im, render(n), plan(n)) for n in LAYOUTS]
    wid = sum(p[0].width for p in panels) + 16
    hgt = max(p[0].height for p in panels)
    sheet = Image.new("RGB", (wid, hgt * 3 + 16), (28, 30, 36)); x = 0
    for p in panels:
        for k, im in enumerate(p):
            sheet.paste(im, (x, k * (hgt + 8)))
        x += p[0].width + 16
    sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(PREVIEW)
    print("  preview %s (top: drawn; middle: tiles and palettes as the game will show them; bottom: blocked cells red, behaviours outlined)" % PREVIEW)

    if over:
        raise SystemExit(1)
    if WRITE:
        os.makedirs(os.path.join(OUT_DIR, "palettes"), exist_ok=True)
        img = Image.new("P", (128, ((len(tile_list) + 15) // 16) * 8))
        greys = []
        for k in range(16):
            greys += [k * 17] * 3
        img.putpalette(greys + [0] * (768 - len(greys))); ip = img.load()
        for n, px in enumerate(tile_list):
            for i, v in enumerate(px):
                ip[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] = v
        img.save(os.path.join(OUT_DIR, "tiles.png"))
        with open(os.path.join(OUT_DIR, "metatiles.bin"), "wb") as f:
            for e in block_list:
                f.write(struct.pack("<8H", *e))
        open(os.path.join(OUT_DIR, "metatile_attributes.bin"), "wb").write(b"".join(attrs))
        for k in range(16):
            src = os.path.join(BASE, "palettes/%02d.pal" % k)
            cols = rows[k] if k in rows else read_pal(src)
            write_pal(os.path.join(OUT_DIR, "palettes/%02d.pal" % k), cols)
        for name, bd in new_maps.items():
            open(os.path.join(GBA, layouts[name]["blockdata_filepath"]), "wb").write(bd)
        # register the tileset, once
        lj_path = os.path.join(GBA, "data/layouts/layouts.json"); lj = open(lj_path).read()
        for name in LAYOUTS:
            lj = re.sub(r'("name": "%s",(?:[^{}]*?)"secondary_tileset": )"gTileset_\w+"' % re.escape(name), r'\1"gTileset_PlayersHouse"', lj, flags=re.S)
        open(lj_path, "w").write(lj)
        rules_path = os.path.join(GBA, "tileset_rules.mk"); rules = open(rules_path).read()
        key = "$(TILESETGFXDIR)/secondary/players_house/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles "
        if key in rules:
            at = rules.index(key) + len(key); old = rules[at:].split()[0]
            rules = rules[:at] + str(len(tile_list)) + rules[at + len(old):]
        else:
            rules += "\n%s%d -Wnum_tiles\n" % (key, len(tile_list))
        open(rules_path, "w").write(rules)
        def add_once(path, anchor_text, block):
            s = open(path).read()
            if "PlayersHouse" in s:
                return
            open(path, "w").write(s + ("\n" if not s.endswith("\n") else "") + block)
        add_once(os.path.join(GBA, "src/data/tilesets/graphics.h"), "",
                 "// The player's house, its own tileset so it can be a timber cottage (T-89).\n"
                 "const u32 gTilesetTiles_PlayersHouse[] = INCBIN_U32(\"data/tilesets/secondary/players_house/tiles.4bpp.lz\");\n\n"
                 "const u16 gTilesetPalettes_PlayersHouse[][16] =\n{\n" +
                 "".join("\tINCBIN_U16(\"data/tilesets/secondary/players_house/palettes/%02d.gbapal\"),\n" % k for k in range(16)) + "};\n")
        add_once(os.path.join(GBA, "src/data/tilesets/metatiles.h"), "",
                 "const u16 gMetatiles_PlayersHouse[] = INCBIN_U16(\"data/tilesets/secondary/players_house/metatiles.bin\");\n"
                 "const u32 gMetatileAttributes_PlayersHouse[] = INCBIN_U32(\"data/tilesets/secondary/players_house/metatile_attributes.bin\");\n")
        add_once(os.path.join(GBA, "src/data/tilesets/headers.h"), "",
                 "// T-89: the player's house, a timber cottage inside.\n"
                 "const struct Tileset gTileset_PlayersHouse =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
                 "    .tiles = gTilesetTiles_PlayersHouse,\n    .palettes = gTilesetPalettes_PlayersHouse,\n"
                 "    .metatiles = gMetatiles_PlayersHouse,\n    .metatileAttributes = gMetatileAttributes_PlayersHouse,\n    .callback = NULL,\n};\n")
        print("  written: %s, both floors, layouts.json, tileset_rules.mk and the three tileset headers" % os.path.relpath(OUT_DIR, GBA))


if __name__ == "__main__":
    main()

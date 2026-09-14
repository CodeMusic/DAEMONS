#!/usr/bin/env python3
"""The player's house as a timber cottage, with depth (T-89; vision.md 9.22).

    python3 tools/gbahouse.py            # preview to /tmp/house.png (the concept drawn | the game's own render of it)
    python3 tools/gbahouse.py --write    # a new tileset gTileset_PlayersHouse, both floors' maps pointed at it

WHY ITS OWN TILESET. Both floors are drawn almost entirely from gTileset_Building,
the primary every interior in the game loads (184 layouts), so redrawing those
tiles would redraw shops and houses alike. The house gets a secondary tileset of
its own instead -- the route CRYSTAL CLEAR's lab took (T-54) -- and every cell of
both floors a block of it. The layout, collision and every behaviour stay: each
new block copies the attributes of the block it replaces, so the KITCHEN, the
CABINET, the TELEVISION, the WINDOW, the BOOKSHELF, the DRESSER, the signpost,
both stair warps and the exit mat keep doing what they did.

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
    10: ["OUT", "EMBER", "FIRE2", "FIRE", "GLOW", "COPPER", "POTD", "POT", "POTT", "CHK", "SKYL", "WHITE", "WOODF", "WOODT", "BEAM"],
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


def first_floor():
    r = Room(13, 10); shell(r, void_bottom=True)
    # x1: the counter with its basin (KITCHEN)
    r.box(17, 14, 31, 38, 5, top="CREAM", front="WOODF", dark="WOODD")
    r.rect(19, 15, 28, 18, "STONED"); r.rect(20, 16, 27, 17, "SKY"); r.rect(19, 24, 29, 36, "WOODD"); r.rect(20, 25, 28, 35, "WOODF"); r.px(27, 30, "COPPER")
    # x2: the iron stove and its pipe (KITCHEN)
    r.rect(37, 0, 40, 13, "IROND"); r.vline(37, 0, 13, "IRON")
    r.box(33, 14, 46, 38, 4, top="IRONT", front="IRON", dark="IROND")
    r.rect(36, 24, 43, 33, "IROND"); r.rect(37, 26, 42, 31, "EMBER"); r.rect(38, 27, 41, 30, "FIRE2")
    # x3..4: the dresser with plates (CABINET)
    r.box(50, 2, 77, 38, 3, top="WOODT", front="WOODF", dark="WOODD")
    r.hline(51, 76, 17, "WOODD"); r.hline(51, 76, 24, "WOODD")
    for x in (53, 60, 67):
        r.rect(x, 8, x + 4, 15, "WHITE"); r.vline(x + 4, 8, 15, "CREAMD")
    r.rect(52, 26, 62, 36, "WOODD"); r.rect(65, 26, 75, 36, "WOODD"); r.px(60, 31, "COPPER"); r.px(67, 31, "COPPER")
    # x5: copper pans on hooks
    r.hline(82, 93, 8, "BEAMD")
    for x, h in ((83, 7), (89, 5)):
        r.vline(x + 2, 9, 11, "BEAMD"); r.rect(x, 12, x + 5, 12 + h, "COPPER"); r.vline(x + 5, 12, 12 + h, "POTD")
    # x6: the TV on its cabinet (TELEVISION)
    r.box(97, 22, 110, 38, 3, top="WOODT", front="WOODF", dark="WOODD")
    r.box(98, 6, 109, 21, 2, top="IRONT", front="IROND", dark="IROND", shadow=False)
    r.rect(100, 10, 107, 19, "SCREEN"); r.rect(101, 11, 103, 13, "SCREENL"); r.hline(100, 107, 19, "SCREEND")
    # x7: a framed picture
    r.rect(114, 8, 125, 19, "BEAM"); r.rect(116, 10, 123, 17, "SKY"); r.rect(116, 14, 123, 17, "GREEN"); r.shadow(126, 9, 127, 20)
    # x8: the window (WINDOW)
    window(r, 129, 5, 14, 14)
    # x9: the stone fireplace, its hearthstone on the floor lit by the fire
    r.rect(144, 0, 159, 31, "STONE")
    for y in range(1, 31, 5):
        r.hline(144, 159, y, "MORTAR")
        for x in range(144 + (4 if (y // 5) % 2 else 0), 160, 8):
            r.vline(x, y, y + 4, "MORTAR")
    r.vline(144, 0, 31, "STONET"); r.vline(159, 0, 31, "STONED")
    r.rect(147, 14, 156, 31, "SOOT")
    for k, x in enumerate(range(148, 156, 2)):
        r.rect(x, 21 + (k % 2) * 3, x + 1, 30, "FIRE" if k % 2 else "FIRE2")
    r.rect(147, 29, 156, 31, "EMBER"); r.rect(142, 10, 161, 11, "WOODT"); r.hline(142, 161, 12, "WOODD")
    r.rect(142, 32, 161, 36, "STONET"); r.hline(142, 161, 32, "WHITE"); r.rect(142, 37, 161, 38, "STONED"); r.hline(142, 161, 39, "OUT")
    r.rect(147, 33, 156, 35, "GLOW"); r.shadow(143, 40, 162, 41)
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
    # the rug, the table on cells (6..7, 4..5), four chairs
    rug(r, 112, 80, 50, 28)
    r.ellipse(113, 88, 22, 10, lambda x, y, d: r.shadow(x, y, x, y))
    for lx in (96, 127):
        r.rect(lx, 78, lx + 1, 92, "WOODD")
    r.ellipse(112, 74, 22, 11, lambda x, y, d: r.px(x, y, "WOODF"))
    r.ellipse(112, 72, 22, 10, lambda x, y, d: r.px(x, y, "CREAM" if (d > 0.8 and y < 67) else "WOODT"))
    for cx, cy, back in ((104, 54, "up"), (120, 54, "up"), (104, 100, "down"), (120, 100, "down")):
        chair(r, cx, cy, back)
    plant(r, 17, 104); plant(r, 193, 104)
    # the doormat over the exit, with a thickness
    for y in range(130, 146):
        for x in range(52, 92):
            r.px(x, y, "RUG4" if (x // 4 + y // 4) % 2 else "WOODF")
    r.hline(52, 91, 130, "CREAM"); r.rect(52, 146, 91, 147, "WOODD")
    return r


def second_floor():
    r = Room(12, 9); shell(r, attic=True)
    # x1..2: the desk, the PORT on it at (1,1)
    r.box(17, 18, 46, 40, 5, top="WOODT", front="WOODF", dark="WOODD")
    r.rect(35, 27, 45, 38, "WOODD"); r.rect(36, 28, 44, 32, "WOODF"); r.rect(36, 34, 44, 37, "WOODF"); r.px(40, 30, "COPPER"); r.px(40, 35, "COPPER")
    r.box(19, 4, 32, 17, 2, top="IRONT", front="IRON", dark="IROND", shadow=False)
    r.rect(21, 8, 30, 15, "SCREEN"); r.rect(22, 9, 24, 11, "SCREENL"); r.px(29, 15, "LED")
    r.rect(20, 19, 31, 21, "IRONT"); r.hline(20, 31, 22, "IROND")
    # x3: the chest of drawers (DRESSER)
    r.box(49, 8, 62, 40, 3, top="WOODT", front="WOODF", dark="WOODD")
    for y in (16, 24, 32):
        r.hline(49, 62, y, "WOODD"); r.px(55, y + 4, "COPPER"); r.px(56, y + 4, "COPPER")
    # x4..5: the bookshelf (BOOKSHELF)
    r.box(66, 0, 93, 40, 2, top="WOODT", front="WOODD", dark="OUT")
    for k, y in enumerate((5, 16, 27)):
        for x in range(68, 92, 3):
            h = 8 - ((x // 3 + k) % 3)
            r.rect(x, y + (9 - h), x + 1, y + 9, ["BOOK1", "BOOK2", "BOOK3", "BOOK4", "BOOK5"][(x // 3 + k) % 5])
        r.hline(67, 92, y + 10, "WOODT")
    # x6..7: the dormer window
    window(r, 99, 4, 26, 16, deep=True)
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
    # the bed on x2, rows 4..6: headboard, pillow, quilt, its fall, a footboard
    r.shadow(30, 108, 54, 111); r.shadow(51, 62, 54, 107)
    r.rect(28, 56, 51, 64, "WOODF"); r.hline(28, 51, 56, "WOODT"); r.vline(51, 56, 64, "WOODD")
    r.rect(30, 65, 49, 73, "WHITE"); r.hline(30, 49, 73, "CREAMD"); r.rect(32, 66, 40, 71, "CREAM")
    for y in range(74, 98):
        for x in range(30, 50):
            r.px(x, y, "QD" if x == 49 else ["Q1", "Q2", "Q3", "RUG2"][((x - 30) // 8 + (y - 74) // 8) % 4])
    for y in range(98, 104):
        for x in range(30, 50):
            r.px(x, y, "QD" if y > 100 else ["QD", "Q2", "Q3"][((x - 30) // 8) % 3])
    r.rect(28, 104, 51, 108, "WOODF"); r.hline(28, 51, 104, "WOODT"); r.hline(28, 51, 108, "OUT"); r.vline(51, 56, 108, "OUT"); r.vline(27, 56, 108, "OUT")
    # the rug, the low table with the set on (6,4), the console on (6,5), its pad
    rug(r, 104, 96, 50, 28)                              # the same rug as downstairs, on the same grid: its tiles are shared
    r.shadow(94, 84, 122, 86)
    r.rect(90, 74, 119, 78, "WOODT"); r.hline(90, 119, 74, "CREAM"); r.rect(90, 79, 119, 81, "WOODF"); r.hline(90, 119, 82, "OUT")
    for lx in (91, 117):
        r.rect(lx, 82, lx + 1, 86, "WOODD")
    r.box(95, 54, 112, 73, 3, top="IRONT", front="IRON", dark="IROND", shadow=False)
    r.rect(98, 60, 109, 70, "SCREEN"); r.rect(99, 61, 103, 64, "SCREENL"); r.hline(98, 109, 70, "SCREEND")
    r.shadow(100, 97, 116, 99)
    r.rect(97, 88, 111, 91, "IRONT"); r.hline(97, 111, 88, "WHITE"); r.rect(97, 92, 111, 95, "IRON"); r.hline(97, 111, 96, "OUT")
    r.px(100, 94, "LED"); r.rect(104, 93, 109, 94, "IROND")
    for k in range(8):
        r.px(106 + k // 3, 97 + k, "IROND")
    r.rect(106, 105, 115, 108, "IRONT"); r.rect(106, 109, 115, 110, "IRON")
    return r


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
    battr = open(os.path.join(PRIM, "metatile_attributes.bin"), "rb").read()
    sattr = open(os.path.join(BASE, "metatile_attributes.bin"), "rb").read()
    tiles, tile_list, blocks, block_list, attrs = {}, [], {}, [], []
    new_maps, total_err, used_rows = {}, 0, {}

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
        bd = bytearray(open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read())
        for cy in range(H):
            for cx in range(W):
                raw = struct.unpack_from("<H", bd, (cy * W + cx) * 2)[0]; m = raw & 0x3FF
                a = battr[m * 4:(m + 1) * 4] if m < 640 else sattr[(m - 640) * 4:(m - 639) * 4]
                if m >= 640 and len(a) < 4:
                    raise SystemExit("cell (%d,%d) of %s: block %d has no attributes" % (cx, cy, name, m))
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
                    entries.append((640 + n) | flip | (r << 12))
                a = bytes(a)
                a = struct.pack("<I", struct.unpack("<I", a)[0] & ~(7 << 29))      # bottom layer only: NORMAL
                key = (tuple(entries), a)
                if key not in blocks:
                    blocks[key] = 640 + len(block_list); block_list.append(entries + [0, 0, 0, 0]); attrs.append(a)
                struct.pack_into("<H", bd, (cy * W + cx) * 2, (raw & ~0x3FF) | blocks[key])
        new_maps[name] = bd
    quads = max(1, sum(used_rows.values()))
    print("  %d tiles (of 384), %d blocks (of 384); tiles by row %s; mean squared colour error per pixel %.1f" % (
        len(tile_list), len(block_list), dict(sorted(used_rows.items())), total_err / (quads * 64)))
    assert len(tile_list) <= 384 and len(block_list) <= 384, "over budget"

    # preview: the concept as drawn | the game's render of the tiles and palettes
    def render(name):
        lay = layouts[name]; W, H = lay["width"], lay["height"]; bd = new_maps[name]
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
    panels = [(rooms[n].im, render(n)) for n in LAYOUTS]
    wid = sum(a.width for a, _ in panels) + 16
    sheet = Image.new("RGB", (wid, max(a.height for a, _ in panels) * 2 + 8), (28, 30, 36)); x = 0
    for a, b in panels:
        sheet.paste(a, (x, 0)); sheet.paste(b, (x, a.height + 8)); x += a.width + 16
    sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(PREVIEW)
    print("  preview %s (top: drawn; bottom: tiles and palettes as the game will show them)" % PREVIEW)

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

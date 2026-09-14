#!/usr/bin/env python3
"""CHECKPOINTS, THE REPO and the BENCHMARKS, as buildings (T-62..T-64, T-77..T-79; vision.md 9.23).

    python3 tools/gbacivic.py            # report and preview to /tmp/civic.png (before | after)
    python3 tools/gbacivic.py --write    # tiles, blocks and palettes across the outdoor tilesets, and eight town maps

WHAT EACH BECOMES (9.23, chosen from concepts 2026-09-14 so none of them reads as a house):

    CHECKPOINT   a rotunda: a teal dome carrying the restore arrow, its crown rising
                 into the row above, over a round stone drum on a stone terrace
    THE REPO     stacked shipping containers: the branch stencilled on the top one,
                 the door cut into the bottom pair, REPO on the left container
    BENCHMARK    a colonnade: a flat roof, a frieze with a relief of bars and the
                 mark's name, the gauge over the door, columns across the front --
                 the two at the door in the leader's type colour -- and steps

FOUND BY THEIR DOORS, NOT BY BLOCK NUMBERS. Every warp into a Pokemon Center,
Mart or Gym is a building: 17 CHECKPOINTS, 12 REPOs and 8 BENCHMARKs on the
General tileset. Around each door the building sits on the same cells, but a
town may draw an edge, a roof top or a sign with a block of its own. So each
building is stamped from a drawing placed on its door, and every block under it
-- shared or a town's -- has only its building entries redrawn: an entry in
palette row 2, 3 or 5 that draws a tile the vanilla building draws. Grass, the
town's own rows and the door keep what they had.

A BENCHMARK IS DRAWN BY COLUMN, because they are six, seven and eight cells wide
and the same block stands at a different offset in different towns. Each column
is drawn by its role -- left edge, wall, the pillar either side of the door, the
door, right edge -- so a block always gets the same pixels wherever it stands.
Rows -4..-2 are one block for every middle column, so only rows -1 and 0 can
tell one column from another: the gauge and the pillars live there.

TWO THINGS DIFFER BY TOWN, and each is done the cheapest way it can be:

  THE PILLARS' COLOUR (T-78). The pillar blocks are shared by all eight, so the
  pillar is drawn on the top layer in palette row 7, which every one of the
  eight towns' tilesets leaves unused; the recess behind it moves to the bottom
  layer. Each town's row 7 holds its leader's type colour (gbasprite.py's
  TYPE_COLOR), so one drawing wears eight colours.
  THE MARK'S NAME (T-79). Letters cannot be a palette trick, so the two frieze
  cells right of the door are given blocks of the town's own, with the name
  drawn over the frieze in the 3x5 face.

COLOUR. The General palette rows are full. The CHECKPOINT's teal takes three
colours of row 2 that only one Verdigris door block drew (8, 9) or nothing drew
(15), and that door block moves to row 5, whose browns it recolours onto. THE
REPO is drawn in row 5's golds. The BENCHMARK is row 2's slate greys and whites,
its gauge row 5's gold, its pillars row 7.

TILES. Each drawn tile is de-duplicated -- mirrored and flipped copies included,
which the dome and the colonnade rely on -- and placed in a slot that only these
buildings used, or one nobody used. A block asked for two different drawings by
two buildings is a conflict and is reported, never guessed.
"""
import importlib.util, json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbaemblems", os.path.join(ROOT, "tools", "gbaemblems.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)

GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/civic.png"
WRITE = "--write" in sys.argv

BUILDING_ROWS = {2, 3, 5}
KINDS = {"POKEMON_CENTER_1F": ("CHECKPOINT", 98), "_MART": ("REPO", 98), "_GYM": ("BENCHMARK", 347)}
GROUP = {
    "CHECKPOINT": [72, 73, 74, 75, 80, 81, 82, 83, 88, 89, 90, 91, 96, 97, 390, 391, 399, 407, 415],
    "REPO": [40, 41, 42, 43, 48, 49, 50, 51, 56, 57, 58, 59, 64, 65, 99],
    "BENCHMARK": [313, 314, 315, 321, 322, 323, 329, 330, 331, 336, 337, 338, 339, 340, 341, 342,
                  344, 345, 346, 348, 349, 350, 352, 360],
}
SIGN_BLOCKS = {352: 0, 360: 1}                      # the BENCHMARK's free-standing board: top cell, bottom cell
# vanilla's CHECKPOINT roof reaches one row up: every town draws that top edge
# with a block of its own, whose top layer draws these four roof tiles in row 2
CHECKPOINT_ROOF_EDGE = {192, 193, 194, 195}
TEAL = {8: (58, 138, 140), 9: (96, 184, 176), 15: (156, 220, 210)}
VERDIGRIS_DOOR = (61, [200, 201, 216, 217])          # moves from row 2 to row 5
ROW2_TO_5 = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 9, 9: 8}
PILLAR_ROW = 7

# each BENCHMARK town: its mark (T-79) and its leader's type colour (T-78, gbasprite.py TYPE_COLOR)
TOWNS = {
    "gTileset_PewterCity":     ("SLATE", "LEGACY",  (130, 130, 138)),
    "gTileset_CeruleanCity":   ("SLOPE", "FLOW",    (70, 106, 176)),
    "gTileset_VermilionCity":  ("SENSE", "SIGNAL",  (86, 190, 190)),
    "gTileset_CeladonCity":    ("FIT",   "GROWTH",  (92, 158, 96)),
    "gTileset_FuchsiaCity":    ("SKEW",  "CORRUPT", (84, 92, 52)),
    "gTileset_SaffronCity":    ("FRAME", "CONTEXT", (176, 86, 158)),
    "gTileset_CinnabarIsland": ("HEAT",  "ENTROPY", (222, 158, 46)),
    "gTileset_ViridianCity":   ("TRUE",  "STRATUM", (158, 122, 78)),
}

# palette roles
R2 = dict(WHITE=1, PALE=2, LIGHT=3, MID=4, GREY=5, DARK=6, OUT=7, TEALD=8, TEALM=9, TEALL=15)
R5 = dict(WHITE=1, LIGHT=2, GREY=3, DARK=4, OUT=5, GOLDL=6, GOLDM=7, GOLDD=8, AMBERD=9, BRIGHT=10, GOLD2=11, GOLD3=12)
R7 = dict(LIGHT=1, MID=2, DARK=3, OUT=4)


def type_ramp(rgb):
    """row 7: a light, the colour, a dark and an outline, from one type colour."""
    light = tuple(min(255, int(c + (255 - c) * 0.45)) for c in rgb)
    dark = tuple(int(c * 0.62) for c in rgb)
    out = tuple(int(c * 0.35) for c in rgb)
    return {R7["LIGHT"]: light, R7["MID"]: tuple(rgb), R7["DARK"]: dark, R7["OUT"]: out}


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, colours):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in colours]
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


def tdir(symbol, kind):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    for d in os.listdir(os.path.join(GBA, "data/tilesets", kind)):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(GBA, "data/tilesets", kind, d)


class Canvas:
    """(row, index) pixels; None is transparent."""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = [[None] * w for _ in range(h)]

    def rect(self, x0, y0, x1, y1, row, v):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.p[y][x] = (row, v)

    def px(self, x, y, row, v):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y][x] = (row, v)

    def stamp(self, x0, y0, art, row):
        for y, line in enumerate(art):
            for x, v in enumerate(line):
                if v:
                    self.px(x0 + x, y0 + y, row, v)

    def word(self, x0, y0, text, row, v):
        for y, line in enumerate(E.word(text)):
            for x, b in enumerate(line):
                if b:
                    self.px(x0 + x, y0 + y, row, v)


# ------------------------------------------------------------------ drawings
def draw_checkpoint():
    """80x80: the row above the building (dy -4, only the crown), then dy -3..0. The door is x 32..47, y 64..79. Row 2."""
    c, r, A = Canvas(80, 80), 2, R2
    # the terrace the drum stands on
    c.rect(0, 16, 79, 79, r, A["GREY"])
    for y in range(20, 79, 8):
        c.rect(0, y, 79, y, r, A["MID"])
    # the dome, an ellipse from its crown at y 6 to its eave at y 47
    for y in range(6, 48):
        t = (47 - y) / 41.0
        half = int(38 * max(0.0, 1 - t * t) ** 0.5)
        shade = "TEALL" if y < 17 else "TEALM" if y < 38 else "TEALD"
        c.rect(40 - half, y, 39 + half, y, r, A[shade])
        c.px(40 - half - 1, y, r, A["OUT"]); c.px(40 + half, y, r, A["OUT"])
        if y % 9 == 3 and y > 10:                       # courses of the dome
            c.rect(40 - half, y, 39 + half, y, r, A["TEALD"] if shade != "TEALD" else A["OUT"])
    c.rect(34, 5, 45, 5, r, A["OUT"])
    c.rect(38, 1, 41, 4, r, A["WHITE"]); c.rect(37, 0, 42, 0, r, A["OUT"]); c.px(37, 1, r, A["OUT"]); c.px(42, 1, r, A["OUT"])   # the lantern
    c.rect(2, 44, 77, 46, r, A["TEALD"]); c.rect(2, 47, 77, 47, r, A["OUT"])
    c.stamp(32, 22, E.emblem("CHECKPOINT", {"O": A["OUT"], "L": A["WHITE"], "M": A["TEALL"], "D": A["TEALD"]}), r)
    # the drum: lit in the middle, shaded to its edges
    for y in range(48, 76):
        for x in range(4, 76):
            d = abs(x - 39.5)
            c.px(x, y, r, A["WHITE"] if d < 16 else A["PALE"] if d < 28 else A["LIGHT"])
    c.rect(4, 48, 4, 75, r, A["OUT"]); c.rect(75, 48, 75, 75, r, A["OUT"]); c.rect(4, 48, 75, 49, r, A["MID"])
    for x0 in (9, 21, 53, 65):                          # tall windows, the same tiles either side
        c.rect(x0, 53, x0 + 5, 70, r, A["OUT"]); c.rect(x0 + 1, 54, x0 + 4, 69, r, A["PALE"])
        c.rect(x0 + 1, 54, x0 + 2, 57, r, A["WHITE"]); c.rect(x0 + 1, 62, x0 + 4, 62, r, A["LIGHT"])
    c.rect(30, 60, 49, 63, r, A["OUT"]); c.rect(31, 61, 48, 62, r, A["LIGHT"])      # the lintel over the door
    c.rect(28, 58, 51, 59, r, A["TEALD"]); c.rect(28, 57, 51, 57, r, A["OUT"])   # a teal canopy over the door
    c.rect(4, 72, 75, 72, r, A["MID"]); c.rect(4, 73, 75, 75, r, A["LIGHT"])      # the drum's plinth
    c.rect(0, 76, 79, 78, r, A["LIGHT"]); c.rect(0, 76, 79, 76, r, A["WHITE"]); c.rect(0, 79, 79, 79, r, A["OUT"])
    c.rect(0, 16, 79, 79, r, None) if False else None
    for y in range(16):                                 # the row above keeps only the crown
        for x in range(80):
            if c.p[y][x] is not None and c.p[y][x][1] == A["GREY"]:
                c.p[y][x] = None
    return c


def draw_repo():
    """64x64, cells dx -2..+1 by dy -3..0; the door is x 32..47, y 48..63. Row 5."""
    c, r, A = Canvas(64, 64), 5, R5
    c.rect(0, 0, 63, 63, r, A["GREY"]); c.rect(0, 0, 63, 0, r, A["OUT"])            # the yard deck behind
    for x in (0, 63):
        c.rect(x, 0, x, 63, r, A["OUT"])

    def container(x0, y0, x1, y1, body, rib):
        for x in range(x0, x1 + 1):
            c.rect(x, y0, x, y1, r, body if (x - x0) % 4 else rib)
        c.rect(x0, y0, x1, y0, r, A["OUT"]); c.rect(x0, y1, x1, y1, r, A["OUT"])
        c.rect(x0, y0, x0, y1, r, A["OUT"]); c.rect(x1, y0, x1, y1, r, A["OUT"])
        c.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 1, r, A["BRIGHT"])
        for cx, cy in ((x0 + 1, y0 + 1), (x1 - 2, y0 + 1), (x0 + 1, y1 - 2), (x1 - 2, y1 - 2)):   # corner castings
            c.rect(cx, cy, cx + 1, cy + 1, r, A["DARK"])
        c.rect(x0 + 1, y1 - 1, x1 - 1, y1 - 1, r, rib)
    container(6, 3, 57, 29, A["GOLDD"], A["AMBERD"])
    c.rect(20, 8, 43, 25, r, A["AMBERD"])
    c.stamp(24, 9, E.emblem("REPO", {"O": A["OUT"], "L": A["BRIGHT"], "M": A["GOLDM"], "T": A["WHITE"]}), r)
    container(0, 30, 31, 63, A["GOLD2"], A["GOLDD"])
    container(32, 30, 63, 63, A["GOLD2"], A["GOLDD"])
    c.rect(31, 44, 48, 47, r, A["OUT"]); c.rect(32, 45, 47, 46, r, A["AMBERD"])     # the cut over the door
    for x in (51, 57):                                  # locking bars on the right container
        c.rect(x, 36, x + 1, 58, r, A["LIGHT"]); c.rect(x + 1, 36, x + 1, 58, r, A["DARK"])
    c.rect(4, 38, 22, 46, r, A["AMBERD"]); c.rect(4, 38, 22, 38, r, A["OUT"]); c.rect(4, 46, 22, 46, r, A["OUT"])
    c.word(5, 40, "REPO", r, A["WHITE"])
    return c


def benchmark_column(role, dy):
    """16x16 of (row, index) for one BENCHMARK cell by its role and row (dy -4..0)."""
    c, r, A, B = Canvas(16, 16), 2, R2, R5
    edge = {"L": 0, "R": 15}.get(role)
    if dy == -4:                                        # the flat roof deck and its parapet
        c.rect(0, 0, 15, 15, r, A["MID"]); c.rect(0, 0, 15, 0, r, A["OUT"]); c.rect(0, 1, 15, 1, r, A["LIGHT"])
        c.rect(8, 3, 8, 11, r, A["GREY"])
        c.rect(0, 12, 15, 12, r, A["OUT"]); c.rect(0, 13, 15, 15, r, A["PALE"])
    elif dy == -3:                                      # a cornice with dentils, then the frieze's relief of bars
        c.rect(0, 0, 15, 15, r, A["WHITE"]); c.rect(0, 0, 15, 0, r, A["LIGHT"])
        c.rect(0, 1, 15, 1, r, A["PALE"]); c.rect(0, 2, 15, 2, r, A["MID"])
        for x in range(0, 16, 4):                       # dentils, four to a cell so every cell repeats
            c.rect(x + 1, 3, x + 2, 4, r, A["LIGHT"]); c.px(x + 2, 4, r, A["MID"])
        c.rect(0, 5, 15, 5, r, A["PALE"])
        if role not in ("L", "R"):
            for x0, h in ((2, 4), (6, 7), (10, 5)):
                c.rect(x0, 13 - h, x0 + 2, 13, r, A["PALE"]); c.rect(x0 + 2, 13 - h, x0 + 2, 13, r, A["LIGHT"]); c.px(x0, 13 - h, r, A["LIGHT"])
        c.rect(0, 14, 15, 14, r, A["LIGHT"]); c.rect(0, 15, 15, 15, r, A["PALE"])
    elif dy == -2:                                      # the architrave, where the mark's name goes
        c.rect(0, 0, 15, 9, r, A["WHITE"]); c.rect(0, 10, 15, 10, r, A["LIGHT"])
        c.rect(0, 11, 15, 13, r, A["MID"]); c.rect(0, 14, 15, 15, r, A["OUT"])
    elif dy == -1:                                      # capitals, the porch in shadow, the gauge over the door
        c.rect(0, 0, 15, 15, r, A["DARK"]); c.rect(0, 0, 15, 1, r, A["OUT"])
        if role == "D":
            c = Canvas(16, 16)
            c.rect(0, 0, 15, 15, 5, B["LIGHT"]); c.rect(0, 0, 15, 1, 5, B["OUT"])
            art = E.emblem("BENCHMARK", {"O": B["OUT"], "W": B["WHITE"], "T": B["GREY"], "N": B["OUT"], "G": B["BRIGHT"], "S": B["LIGHT"]})
            for y in range(13):
                for x in range(16):
                    if art[y + 1][x]:
                        c.px(x, y + 2, 5, art[y + 1][x])
            return c
        if role in ("W", "M"):
            c.rect(4, 2, 11, 3, r, A["PALE"]); c.rect(4, 4, 11, 4, r, A["LIGHT"])
            c.rect(5, 5, 10, 15, r, A["WHITE"]); c.rect(6, 5, 6, 15, r, A["PALE"]); c.rect(10, 5, 10, 15, r, A["LIGHT"])
        if role in ("P", "P'"):                         # the leader's pillar, in row 7
            x0 = 10 if role == "P" else 0
            c.rect(x0, 2, x0 + 5, 3, PILLAR_ROW, R7["LIGHT"]); c.rect(x0, 4, x0 + 5, 4, PILLAR_ROW, R7["OUT"])
            c.rect(x0 + (1 if role == "P" else 0), 5, x0 + (5 if role == "P" else 4), 15, PILLAR_ROW, R7["MID"])
            c.rect(x0 + (1 if role == "P" else 0), 5, x0 + (1 if role == "P" else 0), 15, PILLAR_ROW, R7["LIGHT"])
            c.rect(x0 + (5 if role == "P" else 4), 5, x0 + (5 if role == "P" else 4), 15, PILLAR_ROW, R7["DARK"])
    else:                                               # dy 0: only its top half is building -- the shafts' feet, bases and one step
        c.rect(0, 0, 15, 3, r, A["DARK"])
        c.rect(0, 4, 15, 4, r, A["PALE"]); c.rect(0, 5, 15, 5, r, A["WHITE"]); c.rect(0, 6, 15, 6, r, A["LIGHT"]); c.rect(0, 7, 15, 7, r, A["OUT"])
        if role in ("W", "M"):
            c.rect(5, 0, 10, 2, r, A["WHITE"]); c.rect(6, 0, 6, 2, r, A["PALE"]); c.rect(10, 0, 10, 2, r, A["LIGHT"])
            c.rect(4, 3, 11, 4, r, A["LIGHT"]); c.rect(4, 4, 11, 4, r, A["MID"])
        if role in ("P", "P'"):
            x0 = 10 if role == "P" else 0
            a, b = (x0 + 1, x0 + 5) if role == "P" else (x0, x0 + 4)
            c.rect(a, 0, b, 2, PILLAR_ROW, R7["MID"]); c.rect(a, 0, a, 2, PILLAR_ROW, R7["LIGHT"]); c.rect(b, 0, b, 2, PILLAR_ROW, R7["DARK"])
            c.rect(x0, 3, x0 + 5, 4, PILLAR_ROW, R7["DARK"])
    if edge is not None and dy >= -3:                   # the end walls, stone the full height
        x0 = 0 if role == "L" else 12
        c.rect(x0, 0 if dy > -3 else 1, x0 + 3, 15 if dy < 0 else 11, r, A["WHITE"])
        c.rect(edge, 0, edge, 15, r, A["OUT"]); c.rect(x0 + (3 if role == "L" else 0), 0, x0 + (3 if role == "L" else 0), 15 if dy < 0 else 11, r, A["LIGHT"])
    if edge is not None and dy == -4:
        c.rect(edge, 0, edge, 15, r, A["OUT"])
    if edge is not None and dy == -2:
        c.rect(edge, 0, edge, 15, r, A["OUT"])
    return c


def benchmark_role(dx, left, right):
    if dx == left:
        return "L"
    if dx == right:
        return "R"
    return {-2: "W", -1: "P", 0: "D", 1: "P'"}.get(dx, "M")


def draw_board():
    """16x32 BENCHMARK board, row 5, reading MARK. Its face sits low, in the bottom cell, because
    the top cell only draws its lower half and one town's board has no top cell at all."""
    c, r, B = Canvas(16, 32), 5, R5
    c.rect(0, 13, 15, 24, r, B["WHITE"]); c.rect(0, 13, 15, 13, r, B["OUT"]); c.rect(0, 24, 15, 24, r, B["OUT"])
    c.rect(0, 14, 0, 23, r, B["OUT"]); c.rect(0, 14, 15, 14, r, B["LIGHT"])
    c.word(1, 17, "MARK", r, B["OUT"])
    for x0 in (3, 11):
        c.rect(x0, 25, x0 + 1, 30, r, B["GREY"]); c.rect(x0 + 1, 25, x0 + 1, 30, r, B["DARK"])
    c.rect(1, 31, 14, 31, r, B["LIGHT"])
    return c


def plate_over(col, dx_in_plate, text):
    """the mark's name over one architrave cell: dx_in_plate is this cell's x offset within the plate."""
    c = Canvas(16, 16)
    c.p = [list(row) for row in col.p]
    w = len(text) * 4 + 3
    for x in range(16):
        px = x + dx_in_plate
        if 0 <= px < w:
            for y in range(0, 10):
                c.p[y][x] = (2, R2["DARK"])
            c.p[0][x] = (2, R2["OUT"]); c.p[9][x] = (2, R2["OUT"])
            if px == 0 or px == w - 1:
                for y in range(10):
                    c.p[y][x] = (2, R2["OUT"])
    rows = E.word(text)
    for y in range(5):
        for x, b in enumerate(rows[y]):
            X = x + 2 - dx_in_plate
            if b and 0 <= X < 16:
                c.p[y + 2][X] = (2, R2["WHITE"])
    return c


# ------------------------------------------------------------------ tiles, with mirrored copies shared
def hflip(px):
    return tuple(px[(i // 8) * 8 + 7 - i % 8] for i in range(64))


def vflip(px):
    return tuple(px[(7 - i // 8) * 8 + i % 8] for i in range(64))


# ------------------------------------------------------------------ main
def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    prim = bytearray(open(os.path.join(PD, "metatiles.bin"), "rb").read())
    pattr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    ptiles = Image.open(os.path.join(PD, "tiles.png")); ptp = ptiles.load()
    ppal = {n: read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)}
    btiles = {k: {t & 0x3FF for m in v for t in struct.unpack_from("<8H", prim, m * 16)
                  if t & 0x3FF and (t >> 12) & 0xF in BUILDING_ROWS} for k, v in GROUP.items()}
    btiles["CHECKPOINT"] |= CHECKPOINT_ROOF_EDGE

    secs = {}
    def sec(symbol):
        if symbol not in secs:
            d = tdir(symbol, "secondary")
            secs[symbol] = {"dir": d, "meta": bytearray(open(os.path.join(d, "metatiles.bin"), "rb").read()),
                            "attr": bytearray(open(os.path.join(d, "metatile_attributes.bin"), "rb").read())}
        return secs[symbol]

    def entries(tileset, m):
        buf = prim if m < 640 else sec(tileset)["meta"]
        k = m if m < 640 else m - 640
        return list(struct.unpack_from("<8H", buf, k * 16)) if (k + 1) * 16 <= len(buf) else None

    # every building, by its door
    instances = []
    for mp in sorted(os.listdir(os.path.join(GBA, "data/maps"))):
        p = os.path.join(GBA, "data/maps", mp, "map.json")
        if not os.path.exists(p):
            continue
        j = json.load(open(p)); l = layouts.get(j["layout"])
        if not l or l["primary_tileset"] != "gTileset_General":
            continue
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read(); W, H = l["width"], l["height"]
        cell = lambda x, y, bd=bd, W=W: struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
        for w in j["warp_events"]:
            for suffix, (kind, door) in KINDS.items():
                if w["dest_map"].endswith(suffix) and 0 <= w["x"] < W and 0 <= w["y"] < H and cell(w["x"], w["y"]) == door:
                    instances.append((kind, mp, l, w["x"], w["y"], cell, W, H))

    def building_entries(tileset, m, kind):
        e = entries(tileset, m)
        if e is None:
            return []
        return [j for j, t in enumerate(e) if t & 0x3FF and (t >> 12) & 0xF in BUILDING_ROWS and (t & 0x3FF) in btiles[kind]]

    # what each block under a building should draw: {(tileset, block): {entry: (tile pixels, row)}}
    wants, conflicts = {}, []
    def want(tileset, m, j, px, row, where):
        key = (tileset if m >= 640 else "General", m)
        prev = wants.setdefault(key, {}).get(j)
        if prev is not None and prev != (px, row):
            conflicts.append((key, j, where))
            return
        wants[key][j] = (px, row)

    def quadrant_of(canvas, cx, cy, q):
        x0, y0 = cx * 16 + (q % 2) * 8, cy * 16 + (q // 2) * 8
        return [canvas.p[y0 + i // 8][x0 + i % 8] for i in range(64)]

    def emit(tileset, m, j, pix, where):
        e = entries(tileset, m)
        rows = {v[0] for v in pix if v is not None}
        q = j % 4
        if PILLAR_ROW in rows:
            # the pillar goes on the top layer in row 7; everything behind it moves to the bottom layer
            base = [v if v is not None and v[0] != PILLAR_ROW else None for v in pix]
            top = [v if v is not None and v[0] == PILLAR_ROW else None for v in pix]
            brow = {v[0] for v in base if v is not None}
            if len(brow) > 1:
                conflicts.append(((tileset, m), j, where + " mixes rows %s" % sorted(brow)))
                return
            fill = min((v[1] for v in base if v is not None), default=1)
            want(tileset, m, q, tuple(v[1] if v else fill for v in base), brow.pop() if brow else 2, where)
            want(tileset, m, 4 + q, tuple(v[1] if v else 0 for v in top), PILLAR_ROW, where)
            return
        if len(rows) > 1:
            conflicts.append(((tileset, m), j, where + " mixes rows %s" % sorted(rows)))
            return
        row = rows.pop() if rows else (e[j] >> 12) & 0xF
        if j < 4 and any(v is None for v in pix):
            fill = min((v[1] for v in pix if v is not None), default=1)
            pix = [v if v is not None else (row, fill) for v in pix]
        want(tileset, m, j, tuple(v[1] if v else 0 for v in pix), row, where)

    checkpoint = draw_checkpoint()
    CANVAS = {"CHECKPOINT": (checkpoint, -2, -4), "REPO": (draw_repo(), -2, -3)}
    board = draw_board()
    counts, benchmarks = {}, []
    for kind, mp, l, x, y, cell, W, H in instances:
        counts[kind] = counts.get(kind, 0) + 1
        ts = l["secondary_tileset"]
        if kind in CANVAS:
            canvas, dx0, dy0 = CANVAS[kind]
            for cy in range(canvas.h // 16):
                for cx in range(canvas.w // 16):
                    X, Y = x + dx0 + cx, y + dy0 + cy
                    if not (0 <= X < W and 0 <= Y < H):
                        continue
                    m = cell(X, Y)
                    for j in building_entries(ts, m, kind):
                        emit(ts, m, j, quadrant_of(canvas, cx, cy, j % 4), "%s %s (%d,%d)" % (kind, mp, X, Y))
        else:
            has = lambda X, Y: 0 <= X < W and 0 <= Y < H and bool(building_entries(ts, cell(X, Y), kind)) and cell(X, Y) not in SIGN_BLOCKS
            left = 0
            while has(x + left - 1, y - 1) or has(x + left - 1, y - 2):
                left -= 1
            right = 0
            while has(x + right + 1, y - 1) or has(x + right + 1, y - 2):
                right += 1
            benchmarks.append((mp, l, x, y, left, right))
            for dy in range(-4, 1):
                for dx in range(left, right + 1):
                    X, Y = x + dx, y + dy
                    if not (0 <= X < W and 0 <= Y < H) or (dx == 0 and dy == 0):
                        continue
                    m = cell(X, Y)
                    if m in SIGN_BLOCKS:
                        continue
                    col = benchmark_column(benchmark_role(dx, left, right), dy)
                    for j in building_entries(ts, m, kind):
                        emit(ts, m, j, quadrant_of(col, 0, 0, j % 4), "BENCHMARK %s (%d,%d)" % (mp, X, Y))
            for dy in range(-3, 2):                       # the free-standing board, wherever it stands
                for dx in range(left - 2, right + 3):
                    X, Y = x + dx, y + dy
                    if 0 <= X < W and 0 <= Y < H and cell(X, Y) in SIGN_BLOCKS:
                        m = cell(X, Y)
                        for j in building_entries(ts, m, kind):
                            emit(ts, m, j, quadrant_of(board, 0, SIGN_BLOCKS[m], j % 4), "board %s (%d,%d)" % (mp, X, Y))
    print("  buildings found: %s" % counts)
    if conflicts:
        print("  CONFLICTS (%d):" % len(conflicts))
        for c in conflicts[:20]:
            print("   ", c)

    # ---------------------------------------------------------------- tiles
    rewritten = {(ts, m, j) for (ts, m), js in wants.items() for j in js}
    placed = set()
    for l in layouts.values():
        if l["primary_tileset"] != "gTileset_General":
            continue
        for key in ("blockdata_filepath", "border_filepath"):
            data = open(os.path.join(GBA, l[key]), "rb").read()
            placed |= {struct.unpack_from("<H", data, i)[0] & 0x3FF for i in range(0, len(data), 2)}
    named = {int(v, 16) for v in re.findall(r"#define METATILE_General_\w+\s+0x([0-9A-Fa-f]+)",
                                             open(os.path.join(GBA, "include/constants/metatile_labels.h")).read())}
    idle = {m for m in range(len(prim) // 16) if m not in placed and m not in named}
    referenced_elsewhere = set()
    def scan_refs(ts_name, buf, base):
        for k in range(len(buf) // 16):
            for j, t in enumerate(struct.unpack_from("<8H", buf, k * 16)):
                if t & 0x3FF and (t & 0x3FF) < 640 and (ts_name, base + k, j) not in rewritten \
                        and not (ts_name == "General" and k in idle):
                    referenced_elsewhere.add(t & 0x3FF)
    scan_refs("General", prim, 0)
    for symbol in {l["secondary_tileset"] for l in layouts.values() if l["primary_tileset"] == "gTileset_General"}:
        scan_refs(symbol, sec(symbol)["meta"], 640)
    anim = set(range(416, 482)) | set(range(508, 512))
    pool = sorted(n for n in range(2, 640) if n not in referenced_elsewhere and n not in anim)
    available = len(pool)
    slot = {}                                             # pixels -> (tile, flip bits)
    def place(px):
        if not any(px):
            return 0, 0
        if px in slot:
            return slot[px]
        for flip, f in ((0x400, hflip), (0x800, vflip), (0xC00, lambda p: hflip(vflip(p)))):
            t = f(px)
            if t in slot and slot[t][1] == 0:
                return slot[t][0], flip
        if not pool:
            raise SystemExit("  !! out of primary tile slots (%d were available)" % available)
        slot[px] = (pool.pop(0), 0)
        return slot[px]
    for (ts, m), js in sorted(wants.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        for j, (px, row) in js.items():
            place(px)
    used = len({v[0] for v in slot.values()})
    print("  %d blocks redrawn, %d distinct tiles after mirroring; %d slots were available" % (len(wants), used, available))

    new_tiles = ptiles.copy(); ntp = new_tiles.load()
    for px, (n, flip) in slot.items():
        if flip:
            continue
        for i, v in enumerate(px):
            ntp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] = v
    for (ts, m), js in wants.items():
        buf = prim if m < 640 else sec(ts)["meta"]
        k = m if m < 640 else m - 640
        e = list(struct.unpack_from("<8H", buf, k * 16))
        for j, (px, row) in js.items():
            n, flip = place(px)
            e[j] = (n | flip | (row << 12)) if n else 0
        struct.pack_into("<8H", buf, k * 16, *e)

    # ---------------------------------------------------------------- the mark's name, on each town's own blocks
    rules = open(RULES).read()
    town_tiles, map_writes = {}, {}
    for mp, l, x, y, left, right in benchmarks:
        ts = l["secondary_tileset"]; mark = TOWNS[ts][0]
        s = sec(ts)
        bd = map_writes.get(l["blockdata_filepath"]) or bytearray(open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read())
        map_writes[l["blockdata_filepath"]] = bd
        W = l["width"]
        if ts not in town_tiles:
            key = "secondary/%s/tiles.4bpp: %%.4bpp: %%.png\n\t$(GFX) $< $@ -num_tiles " % os.path.basename(s["dir"])
            at = rules.index(key) + len(key)
            img = Image.open(os.path.join(s["dir"], "tiles.png"))
            town_tiles[ts] = {"key": key, "n": int(rules[at:].split()[0]), "img": img, "new": [], "have": {}}
            tp = img.load(); tt = town_tiles[ts]
            for n in range(tt["n"]):
                tt["have"].setdefault(tuple(tp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] for i in range(64)), n)
        tt = town_tiles[ts]
        for dx in (1, 2):
            X, Y = x + dx, y - 2
            raw = struct.unpack_from("<H", bd, (Y * W + X) * 2)[0]; m = raw & 0x3FF
            if m >= 640 and m not in (330, 331):
                e = entries(ts, m)
                if e and all(((t >> 12) & 0xF) == 2 and (t & 0x3FF) >= 640 for t in e[4:]):
                    print("  %s: the name is already on (%d,%d)" % (mp, X, Y)); continue
            col = plate_over(benchmark_column(benchmark_role(dx, left, right), -2), 16 * (dx - 1), mark)
            e = list(entries(ts, m))
            for q in range(4):
                px = tuple(v[1] if v else 0 for v in quadrant_of(col, 0, 0, q))
                if px not in tt["have"]:
                    tt["have"][px] = tt["n"] + len(tt["new"]); tt["new"].append(px)
                e[4 + q] = (640 + tt["have"][px]) | (2 << 12)
            nid = 640 + len(s["meta"]) // 16
            s["meta"] += struct.pack("<8H", *e); s["attr"] += pattr[m * 4:(m + 1) * 4]
            struct.pack_into("<H", bd, (Y * W + X) * 2, (raw & ~0x3FF) | nid)
        print("  %s: %s on the frieze" % (mp, mark))

    # ---------------------------------------------------------------- palettes, and the Verdigris door
    new_ppal = {n: list(c) for n, c in ppal.items()}
    for i, colour in TEAL.items():
        new_ppal[2][i] = colour
    m61, door_tiles = VERDIGRIS_DOOR
    e = list(struct.unpack_from("<8H", prim, m61 * 16))
    door_still_row2 = any(t & 0x3FF in door_tiles and (t >> 12) & 0xF == 2 for t in e)
    for j, t in enumerate(e):
        if t & 0x3FF in door_tiles:
            e[j] = (t & 0x0FFF) | (5 << 12)
    struct.pack_into("<8H", prim, m61 * 16, *e)
    for n in (door_tiles if door_still_row2 else []):     # already moved: do not recolour twice
        for yy in range(8):
            for xx in range(8):
                X, Y = (n % 16) * 8 + xx, (n // 16) * 8 + yy
                ntp[X, Y] = ROW2_TO_5.get(ntp[X, Y], ntp[X, Y])
    row7 = {}
    for ts, (mark, tname, rgb) in TOWNS.items():
        d = tdir(ts, "secondary"); cols = read_pal(os.path.join(d, "palettes/%02d.pal" % PILLAR_ROW))
        for i, colour in type_ramp(rgb).items():
            cols[i] = colour
        row7[ts] = cols

    # ---------------------------------------------------------------- preview
    def render(l, x0, y0, w, h, prim_meta, prim_tiles, pals_primary, sec_meta, sec_tiles, row7_pal, bd):
        sd = tdir(l["secondary_tileset"], "secondary")
        stp = sec_tiles.load()
        pals = [pals_primary[n] for n in range(7)] + [read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
        if row7_pal:
            pals[PILLAR_ROW] = row7_pal
        W = l["width"]
        img = Image.new("RGB", (w * 16, h * 16)); o = img.load(); ptp_ = prim_tiles.load()
        for yy in range(y0, y0 + h):
            for xx in range(x0, x0 + w):
                m = struct.unpack_from("<H", bd, (yy * W + xx) * 2)[0] & 0x3FF
                buf = prim_meta if m < 640 else sec_meta
                k = m if m < 640 else m - 640
                if (k + 1) * 16 > len(buf):
                    continue
                ee = struct.unpack_from("<8H", buf, k * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = ee[layer * 4 + q]; i = t & 0x3FF
                        src, jj, hh = (ptp_, i, prim_tiles.height) if i < 640 else (stp, i - 640, sec_tiles.height)
                        for ty in range(8):
                            for tx in range(8):
                                sy = (jj // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                v = src[(jj % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                                if layer and v == 0:
                                    continue
                                o[(xx - x0) * 16 + (q % 2) * 8 + tx, (yy - y0) * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
        return img

    def grown(ts):
        tt = town_tiles.get(ts)
        img = Image.open(os.path.join(tdir(ts, "secondary"), "tiles.png"))
        if not tt or not tt["new"]:
            return img
        total = tt["n"] + len(tt["new"])
        g = Image.new("P", (128, ((total + 15) // 16) * 8)); g.putpalette(img.getpalette()); g.paste(img, (0, 0)); gp = g.load()
        for k, px in enumerate(tt["new"]):
            s_ = tt["n"] + k
            for i, v in enumerate(px):
                gp[(s_ % 16) * 8 + i % 8, (s_ // 16) * 8 + i // 8] = v
        return g

    views = [("LAYOUT_PEWTER_CITY", 8, 10, 26, 18), ("LAYOUT_VIRIDIAN_CITY", 20, 5, 22, 24), ("LAYOUT_SAFFRON_CITY", 16, 5, 36, 36),
             ("LAYOUT_FUCHSIA_CITY", 0, 24, 24, 14), ("LAYOUT_CINNABAR_ISLAND", 10, 0, 18, 14)]
    panels = []
    for lid, x0, y0, w, h in views:
        l = layouts[lid]; ts = l["secondary_tileset"]; sd = tdir(ts, "secondary")
        h = min(h, l["height"] - y0); w = min(w, l["width"] - x0)
        old_bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        new_bd = bytes(map_writes.get(l["blockdata_filepath"], old_bd))
        panels.append((render(l, x0, y0, w, h, open(os.path.join(PD, "metatiles.bin"), "rb").read(), ptiles, ppal,
                              open(os.path.join(sd, "metatiles.bin"), "rb").read(), Image.open(os.path.join(sd, "tiles.png")), None, old_bd),
                       render(l, x0, y0, w, h, bytes(prim), new_tiles, new_ppal, bytes(sec(ts)["meta"]), grown(ts), row7.get(ts), new_bd)))
    width = max(a.width for a, _ in panels) * 2 + 8
    sheet = Image.new("RGB", (width, sum(a.height for a, _ in panels) + 8 * len(panels)), (30, 30, 30)); yy = 0
    for a, b in panels:
        sheet.paste(a, (0, yy)); sheet.paste(b, (a.width + 8, yy)); yy += a.height + 8
    sheet.save(PREVIEW)
    print("  preview %s (before | after: Slate, Callow, Brazen, Lurid, Quicksilver)" % PREVIEW)

    if WRITE:
        if conflicts:
            raise SystemExit("  refusing to write with conflicts")
        new_tiles.save(os.path.join(PD, "tiles.png"))
        open(os.path.join(PD, "metatiles.bin"), "wb").write(prim)
        for symbol, s in secs.items():
            open(os.path.join(s["dir"], "metatiles.bin"), "wb").write(s["meta"])
            open(os.path.join(s["dir"], "metatile_attributes.bin"), "wb").write(s["attr"])
        write_pal(os.path.join(PD, "palettes/02.pal"), new_ppal[2])
        for ts, cols in row7.items():
            write_pal(os.path.join(tdir(ts, "secondary"), "palettes/%02d.pal" % PILLAR_ROW), cols)
        for ts, tt in town_tiles.items():
            if not tt["new"]:
                continue
            grown(ts).save(os.path.join(tdir(ts, "secondary"), "tiles.png"))
            at = rules.index(tt["key"]) + len(tt["key"])
            rules = rules[:at] + str(tt["n"] + len(tt["new"])) + rules[at + len(str(tt["n"])):]
        open(RULES, "w").write(rules)
        for path, bd in map_writes.items():
            open(os.path.join(GBA, path), "wb").write(bd)
        print("  written: General tiles, metatiles and row 2; %d secondary tilesets; eight towns' row 7; the frieze names" % len(secs))


if __name__ == "__main__":
    main()

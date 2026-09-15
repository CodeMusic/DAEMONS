#!/usr/bin/env python3
"""The CHECKPOINT (both floors) and THE REPO, rethemed and replanned, each on a tileset of its own (T-103; vision.md 9.23).

    python3 tools/gbainterior.py              # both buildings: counts, and a preview to /tmp/interior_<name>.png
    python3 tools/gbainterior.py --write      # write the tilesets, the layouts, and register both tilesets
    python3 tools/gbainterior.py checkpoint   # one building only (checkpoint | repo)

WHAT IT BUILDS. Each building is drawn whole, in full colour, from the concept
approved 2026-09-15 -- the rooms as they should look, not as tile edits -- and
this turns the drawing into a secondary tileset: every cell's 16x16 becomes a
block, blocks and 8x8 tiles are deduplicated (tiles with their flips), and six
palette rows are fitted to the colours the tiles actually share.

WHAT IT KEEPS. The layouts' sizes, every cell's collision and behaviour (the
nurse's counter, the PC, the region map, the stairs, the doors, the clerk's L
counter with the questionnaire hidden in it) except where PLAN says otherwise.
And every block id the engine or a script names keeps its id: the escalator's
frames (special_field_anim.c), the cable club door (field_door.c), the union room
barrier and its shade (cable_club.inc), Viridian's two counter pieces
(ViridianCity_Mart). The escalator, the door and the barrier are drawn as their
originals recoloured into the building's theme, so each animation's frames
still match; the counter pieces take the new counter's own cells.

WHY A TILESET EACH. One tileset cannot hold every CHECKPOINT: Kanto's two floors
(and One Island's identical upstairs) fill `gTileset_Checkpoint` to 381 of 384
tiles. One Island's and Indigo Plateau's downstairs, which are shaped
differently and have no concept of their own, get `gTileset_CheckpointOneIsland`
and `gTileset_CheckpointIndigo`: the theme and the new floor, Kanto's new
drawing wherever the same vanilla block stands (KANTO_STAMP), our plant for
Indigo's, and everything else recoloured. `gTileset_PokemonCenter` now serves
only the unused RS layout; `gTileset_Mart` keeps the unused Lavaridge and RS ones.

    python3 tools/gbainterior.py checkpoint_one_island checkpoint_indigo --write

BENCHMARKS too: `slate` (T-105) is CAIRN's hall, drawn from its concept with every
blocked cell where it was, on `gTileset_SlateBenchmark`; Brazen's dojo keeps the
old tileset it shared.

    python3 tools/gbainterior.py slate --write
    python3 tools/gbainterior.py doldrum --write      # BASIN's becalmed lido (T-106)
    python3 tools/gbainterior.py ardor --write        # GAUGE's signal room (T-107)
    python3 tools/gbainterior.py verdigris --write    # TRELLIS's espalier house (T-108)
    python3 tools/gbainterior.py lurid --write        # TILT's tilted room, its maze redrawn (T-109)
    python3 tools/gbainterior.py brazen --write       # MATTE's gallery of mounts (T-111)
    python3 tools/gbainterior.py quicksilver --write  # ANNEAL's silver lab (T-112)

Statue heads are drawn on the top layer, as vanilla does, so the player walks behind them (T-110).

Everything is flattened onto the bottom layer, as the player's house is (T-89):
nothing in either room draws over a sprite.
"""
import importlib.util, json, math, os, re, struct, sys
from collections import Counter
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
ONLY = [a for a in sys.argv[1:] if not a.startswith("--")]


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


CP, RP, EM = load("gbacheckpoint"), load("gbarepo"), load("gbaemblems")
PRIM = os.path.join(GBA, "data/tilesets/primary/building")
LAYOUTS = {l["id"]: l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if "id" in l}
MAGENTA = (255, 0, 255)                   # transparent: the see-through pixels of a top-layer tile


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, cols):
    open(path, "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols))


# ---------------------------------------------------------------- the old tileset, rendered flat
class Old:
    def __init__(self, sec):
        self.sec = os.path.join(GBA, "data/tilesets/secondary", sec)
        self.pmeta = open(os.path.join(PRIM, "metatiles.bin"), "rb").read()
        self.smeta = open(os.path.join(self.sec, "metatiles.bin"), "rb").read()
        self.pattr = open(os.path.join(PRIM, "metatile_attributes.bin"), "rb").read()
        self.sattr = open(os.path.join(self.sec, "metatile_attributes.bin"), "rb").read()
        self.pt = Image.open(os.path.join(PRIM, "tiles.png")).load()
        self.st = Image.open(os.path.join(self.sec, "tiles.png")).load()
        self.pals = [read_pal(os.path.join(PRIM, "palettes/%02d.pal" % r)) for r in range(7)] + \
                    [read_pal(os.path.join(self.sec, "palettes/%02d.pal" % r)) for r in range(7, 13)]

    def attr(self, m):
        buf, k = (self.pattr, m) if m < 640 else (self.sattr, m - 640)
        return struct.unpack_from("<I", buf, k * 4)[0] if (k + 1) * 4 <= len(buf) else 0

    def block(self, m):
        """16x16 RGB, top over bottom"""
        buf, k = (self.pmeta, m) if m < 640 else (self.smeta, m - 640)
        out = [[(0, 0, 0)] * 16 for _ in range(16)]
        if (k + 1) * 16 > len(buf):
            return out
        e = struct.unpack_from("<8H", buf, k * 16)
        for layer in (0, 1):
            for q in range(4):
                t = e[layer * 4 + q]; i = t & 0x3FF
                src, j = (self.pt, i) if i < 640 else (self.st, i - 640)
                for ty in range(8):
                    for tx in range(8):
                        sx = 7 - tx if t & 0x400 else tx; sy = 7 - ty if t & 0x800 else ty
                        try:
                            v = src[(j % 16) * 8 + sx, (j // 16) * 8 + sy] % 16
                        except IndexError:
                            v = 0
                        if layer and v == 0:
                            continue
                        out[(q // 2) * 8 + ty][(q % 2) * 8 + tx] = self.pals[(t >> 12) & 15][v]
        return out

    def layout(self, lid):
        l = LAYOUTS[lid]; W, H = l["width"], l["height"]
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        raw = [[struct.unpack_from("<H", bd, (y * W + x) * 2)[0] for x in range(W)] for y in range(H)]
        img = Image.new("RGB", (W * 16, H * 16)); p = img.load()
        cache = {}
        for y in range(H):
            for x in range(W):
                m = raw[y][x] & 0x3FF
                b = cache.setdefault(m, self.block(m))
                for yy in range(16):
                    for xx in range(16):
                        p[x * 16 + xx, y * 16 + yy] = b[yy][xx]
        return img, raw


def recolour(pixels, theme):
    return [[theme.get(c, c) for c in row] for row in pixels]


# ---------------------------------------------------------------- drawing
class Room:
    def __init__(self, img):
        self.im = img; self.p = img.load(); self.w, self.h = img.size

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[x, y] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.p[x, y] = c

    def shade(self, x0, y0, x1, y1, k):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                r, g, b = self.p[x, y]; self.p[x, y] = (int(r * k), int(g * k), int(b * k))

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                    self.px(x, y, c)

    def indexed(self, art, pal, x0, y0):
        for y, row in enumerate(art):
            for x, v in enumerate(row):
                if v:
                    self.px(x0 + x, y0 + y, pal[v])

    def corners(self, bottom_rows=1):
        for k in range(12):
            self.rect(0, k, 11 - k, k, (0, 0, 0)); self.rect(self.w - 12 + k, k, self.w - 1, k, (0, 0, 0))
            y = self.h - 16 * bottom_rows - 12 + k
            self.rect(0, y, k, y, (0, 0, 0)); self.rect(self.w - 1 - k, y, self.w - 1, y, (0, 0, 0))


def plant(r, x0, y0, pot, potd, leaves):
    L, M, D = leaves
    r.shade(x0 + 2, y0 + 12, x0 + 15, y0 + 14, 0.75)
    r.rect(x0, y0, x0 + 11, y0 + 11, pot); r.rect(x0 + 9, y0, x0 + 11, y0 + 11, potd); r.rect(x0, y0 + 11, x0 + 11, y0 + 11, (40, 40, 48))
    r.rect(x0, y0, x0 + 11, y0, tuple(min(255, c + 40) for c in pot))
    for dx, h, lean in ((3, 22, -1), (6, 28, 0), (8, 20, 1), (4, 16, -2), (9, 14, 2)):
        for t in range(h):
            x = x0 + dx + (lean * t) // 8; y = y0 - 1 - t
            r.rect(x, y, x + 1, y, M if t % 5 else L)
            if t > 3 and t % 3 == 0:
                r.px(x + (1 if lean >= 0 else -1), y, D)


# the CHECKPOINT's materials
C_FLOOR, C_JOINT, C_DOT = (218, 212, 200), (192, 186, 174), (120, 180, 176)
C_WALL, C_WALLS, C_CORN, C_CORNL, C_WAIN, C_RAIL, C_SKIRT = (204, 226, 218), (186, 212, 204), (46, 96, 100), (84, 140, 142), (104, 164, 160), (238, 234, 222), (58, 88, 92)
C_TEAL, C_TEALD, C_TEALL = (62, 140, 142), (40, 104, 108), (84, 160, 156)
C_INLAY, C_INLAYB = (192, 180, 150), (240, 236, 220)
PLANT_CP = ((170, 168, 160), (132, 130, 124), ((150, 200, 120), (84, 150, 90), (50, 100, 64)))


def cp_floor(x, y):
    if x % 16 in (0, 15) and y % 16 in (0, 15):
        return C_DOT
    return C_JOINT if (x % 16 == 0 or y % 16 == 0) else C_FLOOR


def checkpoint_1f(old_img):
    W, H = 15, 10
    r = Room(Image.new("RGB", (W * 16, H * 16)))
    for y in range(32, 144):
        for x in range(240):
            r.px(x, y, cp_floor(x, y))
    r.shade(0, 32, 239, 35, 0.86)
    r.rect(0, 0, 239, 3, C_CORN); r.rect(0, 4, 239, 4, C_CORNL)
    for y in range(5, 20):
        for x in range(240):
            r.px(x, y, C_WALLS if x % 4 == 0 else C_WALL)
    r.rect(0, 20, 239, 20, C_RAIL); r.rect(0, 21, 239, 27, C_WAIN); r.rect(0, 28, 239, 31, C_SKIRT)
    em = EM.emblem("CHECKPOINT", {"O": 1, "M": 2, "L": 2})
    for y in range(16):
        for x in range(16):
            if em[y][x]:
                r.rect(96 + x * 3, 80 + y * 3, 98 + x * 3, 82 + y * 3, C_INLAY if em[y][x] == 1 else C_INLAYB)
    r.ellipse(196, 104, 42, 22, (150, 196, 190)); r.ellipse(196, 104, 38, 19, (120, 176, 172)); r.ellipse(196, 104, 30, 13, (150, 196, 190))
    TOP, TOPD, EDGE = (244, 240, 228), (214, 208, 192), (30, 56, 60)
    r.shade(66, 59, 178, 62, 0.8)
    for x0, x1 in ((64, 79), (160, 175)):
        r.rect(x0, 24, x1, 46, TOP); r.rect(x0, 24, x0, 58, EDGE); r.rect(x1, 24, x1, 58, EDGE)
    r.rect(64, 36, 175, 46, TOP); r.rect(64, 45, 175, 46, TOPD)
    r.rect(64, 47, 175, 58, C_TEAL); r.rect(64, 57, 175, 58, C_TEALD); r.rect(64, 35, 175, 35, EDGE); r.rect(64, 59, 175, 59, EDGE)
    for x in range(72, 172, 16):
        r.rect(x, 49, x, 55, C_TEALD)
    r.rect(114, 38, 128, 43, (60, 70, 80)); r.rect(115, 39, 127, 41, (140, 210, 200))
    r.rect(67, 26, 76, 33, (230, 226, 210)); r.rect(70, 20, 73, 26, C_CORNL)
    r.ellipse(168, 30, 5, 3, (220, 190, 90)); r.rect(166, 27, 170, 29, (240, 214, 120))
    pc_pal = read_pal(os.path.join(GBA, "data/tilesets/secondary/pokemon_center/palettes/11.pal"))
    r.indexed(CP.rack(), pc_pal, 80, 16)
    r.rect(114, 6, 141, 22, (46, 56, 66)); r.rect(116, 8, 139, 20, (30, 40, 50)); r.rect(118, 10, 124, 12, (70, 120, 130))
    r.shade(180, 42, 194, 44, 0.8)
    r.rect(177, 8, 191, 41, (170, 178, 184)); r.rect(177, 8, 177, 41, (210, 216, 220)); r.rect(191, 8, 191, 41, (110, 118, 124))
    r.rect(179, 11, 189, 22, (40, 60, 70)); r.rect(180, 12, 188, 21, (96, 186, 180)); r.rect(181, 13, 184, 15, (190, 240, 230))
    r.rect(178, 26, 190, 29, (90, 98, 106)); r.rect(179, 27, 189, 28, (140, 150, 158)); r.rect(182, 34, 186, 36, (96, 186, 180))
    r.rect(194, 6, 223, 25, (74, 60, 46)); r.rect(196, 8, 221, 23, (36, 48, 58))
    pts = [(199, 20), (204, 14), (210, 17), (215, 11), (219, 18), (208, 10)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        for t in range(12):
            r.px(ax + (bx - ax) * t // 12, ay + (by - ay) * t // 12, (80, 170, 164))
    for (x, y) in pts:
        r.rect(x - 1, y - 1, x + 1, y + 1, (190, 240, 230))
    r.shade(34, 41, 64, 43, 0.8)
    r.rect(33, 18, 62, 40, (150, 106, 70)); r.rect(33, 18, 62, 20, (184, 138, 96)); r.rect(35, 22, 60, 38, (96, 66, 44))
    for k, x in enumerate(range(37, 59, 4)):
        r.rect(x, 25, x + 2, 30, [(96, 186, 180), (240, 236, 220), (220, 180, 90)][k % 3])
        r.rect(x, 32, x + 2, 37, [(240, 236, 220), (96, 186, 180), (180, 120, 90)][k % 3])
    plant(r, 18, 28, *PLANT_CP)
    r.ellipse(197, 115, 18, 7, (120, 90, 60)); r.ellipse(196, 111, 18, 8, (196, 150, 100)); r.ellipse(196, 110, 15, 6, (214, 170, 120))
    r.rect(198, 104, 205, 112, (240, 236, 220)); r.rect(199, 104, 204, 105, (150, 110, 70))
    r.shade(222, 128, 238, 130, 0.8)
    r.rect(228, 94, 239, 127, C_TEALD); r.rect(222, 98, 233, 126, C_TEALL); r.rect(222, 98, 233, 99, (140, 200, 196))
    r.rect(222, 111, 233, 111, C_TEALD); r.rect(221, 94, 234, 97, C_TEAL); r.rect(221, 124, 234, 127, C_TEAL)
    r.rect(231, 76, 232, 92, (60, 70, 76)); r.ellipse(231.5, 74, 6, 4, (244, 226, 170)); r.rect(227, 92, 236, 93, (60, 70, 76))
    r.rect(96, 130, 143, 150, C_TEAL); r.rect(98, 132, 141, 148, C_TEALL); r.rect(98, 139, 141, 141, C_RAIL)
    r.rect(0, 144, 95, 159, (0, 0, 0)); r.rect(144, 144, 239, 159, (0, 0, 0))
    r.corners()
    return r.im


def link_mark(r, cx, cy):
    """where two players link: two nodes and the line between them, inlaid like the floor arrow downstairs"""
    for x in range(cx - 9, cx + 10):
        r.rect(x, cy - 1, x, cy + 1, C_INLAY)
    for nx in (cx - 12, cx + 12):
        r.ellipse(nx, cy, 6, 6, C_INLAY); r.ellipse(nx, cy, 4, 4, C_INLAYB); r.ellipse(nx, cy, 1.6, 1.6, C_INLAY)


def checkpoint_2f(old_img, theme, raw=None):
    r = Room(old_img.copy())
    floor_cols = set(FLOOR_OLD)
    for y in range(r.h):
        for x in range(r.w):
            c = r.p[x, y]
            r.p[x, y] = cp_floor(x, y) if c in floor_cols else theme.get(c, c)
    for x0, x1 in ((64, 111), (128, 175)):                # the link spots
        for y in range(64, 112):
            for x in range(x0, x1 + 1):
                r.p[x, y] = cp_floor(x, y)
    link_mark(r, 88, 88); link_mark(r, 152, 88)
    for cx in (3, 13):                                    # the plants
        for y in range(112, 144):
            for x in range(cx * 16, cx * 16 + 16):
                r.p[x, y] = cp_floor(x, y)
        plant(r, cx * 16 + 2, 128, *PLANT_CP)
    return r.im


# the CHECKPOINTs without a concept of their own (One Island, Indigo Plateau): the theme, the new floor, and wherever
# they stand the same vanilla furniture as Kanto's downstairs, Kanto's new drawing of it -- found by the vanilla block
# id, whose Kanto cell is recorded here because Kanto's own map now uses the new tileset's ids
KANTO_STAMP = {
    723: (1, 0), 653: (1, 1), 660: (1, 2),                                             # the plant
    713: (2, 0), 714: (3, 0), 715: (2, 1), 716: (3, 1), 717: (2, 2), 718: (3, 2),       # the leaflet shelf
    681: (4, 1), 682: (5, 1), 683: (6, 1), 689: (4, 2), 690: (5, 2), 691: (6, 2),   # the rack (not the plain wall: stamped
                                                                                     # alone it patched the recoloured walls)
    646: (7, 0), 647: (8, 0), 654: (7, 1), 655: (8, 1),                                 # the monitor
    684: (9, 1), 685: (10, 1), 692: (9, 2), 693: (10, 2),                              # the counter's arm and bell
    645: (11, 0), 98: (11, 1), 661: (11, 2),                                            # the terminal
    662: (12, 0), 663: (13, 0), 670: (12, 1), 671: (13, 1),                             # the wall map
    697: (4, 3), 700: (5, 3), 664: (7, 3), 701: (10, 3),                               # the counter's front
    649: (6, 5), 650: (7, 5), 651: (8, 5), 657: (6, 6), 658: (7, 6), 659: (8, 6),
    665: (6, 7), 666: (7, 7), 667: (8, 7),                                              # the floor arrow
    706: (6, 8), 707: (7, 8), 708: (8, 8), 26: (6, 9), 27: (7, 9), 28: (8, 9),          # the mat
}
_KANTO = []


def themed(old_img, theme, raw):
    if not _KANTO:
        _KANTO.append(checkpoint_1f(None).load())
    kp = _KANTO[0]
    r = Room(old_img.copy())
    floor_cols = set(FLOOR_OLD)
    for y in range(r.h):
        for x in range(r.w):
            c = r.p[x, y]
            r.p[x, y] = cp_floor(x, y) if c in floor_cols else theme.get(c, c)
    for y, row in enumerate(raw):
        for x, v in enumerate(row):
            cell = KANTO_STAMP.get(v & 0x3FF)
            if cell:
                for yy in range(16):
                    for xx in range(16):
                        r.p[x * 16 + xx, y * 16 + yy] = kp[cell[0] * 16 + xx, cell[1] * 16 + yy]
    # vanilla's floor plants -- a leafy top (832 or 768) over its pot (769) -- become our snake plant
    for y in range(1, len(raw)):
        for x in range(len(raw[0])):
            if raw[y][x] & 0x3FF == 769 and raw[y - 1][x] & 0x3FF in (832, 768):
                for yy in range((y - 1) * 16, (y + 1) * 16):
                    for xx in range(x * 16, x * 16 + 16):
                        r.p[xx, yy] = cp_floor(xx, yy)
                plant(r, x * 16 + 2, y * 16 + 2, *PLANT_CP)
    return r.im


# SLATE BENCHMARK (CAIRN), from the concept approved 2026-09-15: a slate hall that keeps a record. The same cells
# are blocked and open -- every boulder becomes a cairn where it stood, so the room plays exactly as before
S_SLATE, S_SLATEL, S_SLATED, S_JOINT = (104, 112, 124), (132, 140, 152), (84, 90, 102), (70, 76, 88)
S_WALL, S_WALLD, S_WALLL = (60, 64, 74), (42, 46, 54), (84, 90, 100)
S_CHALK, S_CHALKD = (234, 232, 222), (190, 188, 180)
S_LIME, S_LIMEL, S_LIMED = (196, 192, 180), (218, 214, 202), (160, 156, 146)
S_STONE, S_STONEL, S_STONED = (138, 132, 124), (170, 164, 154), (98, 94, 88)
S_LAMP, S_INK = (244, 204, 120), (30, 32, 38)


def slate(old_img, raw_=None, statues=True):
    ST = load("gbastatues")
    W, H = old_img.width // 16, old_img.height // 16
    lid = "LAYOUT_PEWTER_CITY_GYM"
    l = LAYOUTS[lid]; bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    blocked = {(x, y) for y in range(H) for x in range(W) if (struct.unpack_from("<H", bd, (y * W + x) * 2)[0] >> 10) & 3}
    r = Room(Image.new("RGB", (W * 16, H * 16)))
    for y in range(H * 16):                                                 # slate flagstones, rows offset by half
        for x in range(W * 16):
            off = 8 if (y // 16) % 2 else 0
            c = S_SLATE
            if y % 16 == 0 or (x + off) % 16 == 0:
                c = S_JOINT
            elif y % 16 == 1 or (x + off) % 16 == 1:
                c = S_SLATEL
            elif (x * 7 + y * 3) % 23 == 0:
                c = S_SLATED
            r.px(x, y, c)
    for y in range(7 * 16, 15 * 16):                                        # the limestone path, door to dais
        for x in range(6 * 16 + 1, 7 * 16 - 1):
            r.px(x, y, S_LIMED if y % 8 == 0 else (S_LIMEL if y % 8 == 1 else S_LIME))
    for x in range(4 * 16, 9 * 16):
        for y in range(10 * 16 + 3, 11 * 16 - 3):
            if not (6 * 16 <= x < 7 * 16):
                r.px(x, y, S_LIMED if x % 8 == 0 else S_LIME)
    r.shade(66, 116, 146, 119, 0.8)                                         # CAIRN's dais
    r.rect(64, 60, 143, 115, S_LIMED); r.rect(66, 62, 141, 113, S_LIME); r.rect(66, 62, 141, 64, S_LIMEL)
    r.rect(72, 68, 135, 107, S_LIMEL); r.rect(74, 70, 133, 105, S_LIME)
    for x in range(76, 132, 4):
        r.px(x, 72, S_CHALKD); r.px(x, 103, S_CHALKD)
    r.rect(66, 112, 141, 115, S_LIMED)
    r.rect(0, 0, W * 16 - 1, 47, S_WALL); r.rect(0, 44, W * 16 - 1, 47, S_WALLD); r.rect(0, 0, W * 16 - 1, 3, S_WALLD)
    for gx0 in range(20, 190, 22):                                          # the record: tallies of five
        for row, gy in enumerate((12, 24, 34)):
            if (gx0 // 22 + row) % 5 == 4:
                continue
            for k in range(4):
                r.rect(gx0 + k * 3, gy, gx0 + k * 3, gy + 7, S_CHALK)
            for k in range(12):
                r.px(gx0 - 1 + k, gy + 6 - k // 2, S_CHALKD)
    for lx in (44, 148):
        r.rect(lx, 14, lx + 6, 26, S_WALLL); r.ellipse(lx + 3, 12, 5, 4, S_LAMP); r.ellipse(lx + 3, 12, 3, 2, (255, 236, 180))
    r.rect(80, 6, 127, 40, (96, 70, 48)); r.rect(83, 9, 124, 37, (46, 52, 58))     # the board behind the dais
    for k, yy in enumerate(range(12, 36, 5)):
        r.rect(87, yy, 87 + 12 + (k * 7) % 14, yy + 1, S_CHALK); r.rect(106, yy, 106 + 8 + (k * 5) % 10, yy + 1, S_CHALKD)
    r.rect(0, 0, 15, H * 16 - 1, S_WALL); r.rect(12 * 16, 0, W * 16 - 1, H * 16 - 1, S_WALL)
    r.rect(14, 48, 15, H * 16 - 17, S_WALLD); r.rect(12 * 16, 48, 12 * 16 + 1, H * 16 - 17, S_WALLL)
    r.rect(0, 15 * 16, W * 16 - 1, H * 16 - 1, (0, 0, 0))

    def cairn(cx, cy):
        r.shade(cx * 16 + 3, cy * 16 + 13, cx * 16 + 15, cy * 16 + 15, 0.7)
        for k, (w, h) in enumerate(((13, 5), (10, 4), (7, 4))):
            x0 = cx * 16 + (16 - w) // 2; y1 = cy * 16 + 13 - k * 4; y0 = y1 - h
            r.rect(x0, y0, x0 + w - 1, y1, S_STONE); r.rect(x0, y0, x0 + w - 1, y0, S_STONEL); r.rect(x0 + w - 1, y0, x0 + w - 1, y1, S_STONED)
            r.rect(x0, y1, x0 + w - 1, y1, S_INK)
        r.rect(cx * 16 + 7, cy * 16 + 2, cx * 16 + 8, cy * 16 + 3, S_CHALK)
    for (x, y) in sorted(blocked):
        if 3 <= y <= 10 and 1 <= x <= 11:
            cairn(x, y)
    pal0 = read_pal(os.path.join(GBA, "data/tilesets/primary/building/palettes/00.pal"))
    badges = Image.open(ST.BADGES).load()
    top, base = ST.mark_top([[badges[x, y] for x in range(16)] for y in range(16)]), ST.plinth()
    for sx in ((4, 8) if statues else ()):
        r.indexed(top, pal0, sx * 16, 11 * 16); r.indexed(base, pal0, sx * 16, 12 * 16)
    r.rect(84, 222, 123, 239, S_WALLD); r.rect(86, 224, 121, 237, (76, 82, 94)); r.rect(86, 224, 121, 224, S_CHALKD); r.rect(86, 237, 121, 237, S_CHALKD)
    return r.im


# DOLDRUM BENCHMARK (BASIN), from the concept approved 2026-09-15: the becalmed lido. Every water cell stays
# water (MB_OCEAN_WATER, surfable) and every walkway floor; the drawing reads which is which from the room itself
def doldrum(old_img, raw_=None, statues=True):
    ST = load("gbastatues")
    old = Old("cerulean_gym")
    _, raw = old.layout("LAYOUT_CERULEAN_CITY_GYM")
    H, W = len(raw), len(raw[0])
    blocked = lambda x, y: bool((raw[y][x] >> 10) & 3)
    water = lambda x, y: 0 <= x < W and 0 <= y < H and (old.attr(raw[y][x] & 0x3FF) & 0x1FF) == 0x15 and not blocked(x, y) and y >= 3
    WATER, WATERL, WATERD, WALLBAND, RING = (58, 116, 176), (84, 144, 200), (46, 98, 156), (34, 72, 120), (72, 132, 190)
    DECK, GROUT = (226, 222, 208), (196, 204, 212)
    WALK, WALKL, GUTTER = (236, 232, 218), (248, 246, 238), (120, 170, 210)
    COPE, COPEF = (248, 246, 238), (196, 192, 180)
    TILE, TILEL, TILED, TRIM = (198, 214, 226), (220, 232, 240), (160, 182, 200), (92, 120, 150)
    SKY, SKYL, SEA, SEAD = (206, 230, 244), (232, 244, 250), (98, 150, 196), (70, 120, 170)
    STEEL, STEELL, STEELD = (176, 184, 192), (222, 228, 232), (110, 118, 126)
    r = Room(Image.new("RGB", (W * 16, H * 16)))
    CX, CY = 8 * 16 + 8, 6 * 16 + 8
    for y in range(H):
        for x in range(W):
            X, Y = x * 16, y * 16
            if y <= 2 or x in (0, W - 1) or y == H - 1:
                continue
            if water(x, y):
                for yy in range(16):
                    for xx in range(16):
                        px, py = X + xx, Y + yy
                        d = math.hypot(px - CX, (py - CY) * 1.3)
                        c = WATER
                        if (py % 8) == 3 and (px // 8 + py // 8) % 3 == 0:
                            c = WATERL
                        if int(d) % 18 == 0 and d > 20:
                            c = RING
                        r.px(px, py, c)
                if not water(x, y - 1):
                    r.rect(X, Y, X + 15, Y + 3, WALLBAND); r.rect(X, Y + 4, X + 15, Y + 4, WATERD)
                if not water(x - 1, y):
                    r.rect(X, Y, X + 1, Y + 15, WATERD)
                if not water(x + 1, y):
                    r.rect(X + 14, Y, X + 15, Y + 15, WATERD)
            else:
                if 2 <= x <= W - 3 and 5 <= y <= H - 3:
                    r.rect(X, Y, X + 15, Y + 15, WALK)
                    if x % 2 == 0:
                        r.rect(X, Y, X + 15, Y, WALKL)
                    if water(x, y - 1) or water(x, y + 1):
                        r.rect(X, Y + 7, X + 15, Y + 8, GUTTER)
                    else:
                        r.rect(X + 7, Y, X + 8, Y + 15, GUTTER)
                else:
                    r.rect(X, Y, X + 15, Y + 15, DECK)
                    r.rect(X, Y, X + 15, Y, GROUT); r.rect(X, Y, X, Y + 15, GROUT); r.rect(X + 8, Y + 8, X + 15, Y + 8, GROUT)
                if water(x, y + 1):
                    r.rect(X, Y + 12, X + 15, Y + 13, COPE); r.rect(X, Y + 14, X + 15, Y + 15, COPEF)
    r.ellipse(CX, CY + 3, 14, 7, COPEF); r.ellipse(CX, CY, 14, 7, COPE); r.ellipse(CX, CY, 10, 5, WALK); r.ellipse(CX, CY, 3, 1.5, GUTTER)
    for y in range(0, 48):
        for x in range(0, W * 16):
            c = TILE
            if y % 8 == 0 or x % 8 == 0:
                c = TILED
            elif y % 8 == 1:
                c = TILEL
            r.px(x, y, c)
    r.rect(0, 40, W * 16 - 1, 43, TRIM); r.rect(0, 44, W * 16 - 1, 47, TILED)
    for px_ in (4 * 16 + 8, 6 * 16 + 8, 10 * 16 + 8, 12 * 16 + 8):                 # portholes onto a flat horizon
        r.ellipse(px_, 22, 9, 9, STEELD); r.ellipse(px_, 22, 7, 7, SKY)
        r.rect(px_ - 6, 25, px_ + 6, 29, SEA); r.rect(px_ - 5, 30, px_ + 5, 31, SEAD); r.rect(px_ - 4, 17, px_ - 1, 18, SKYL)
        r.rect(px_ - 7, 24, px_ + 7, 24, SKYL)
    r.ellipse(8 * 16 + 8, 6, 5, 4, STEEL)
    r.rect(0, 0, 15, H * 16 - 1, TRIM); r.rect(W * 16 - 16, 0, W * 16 - 1, H * 16 - 1, TRIM)
    for y in range(0, H * 16, 16):
        r.rect(0, y, 15, y, TILED); r.rect(W * 16 - 16, y, W * 16 - 1, y, TILED)
    r.rect(0, (H - 1) * 16, W * 16 - 1, H * 16 - 1, (0, 0, 0))
    for (lx, ly) in ((3, 5), (13, 5), (3, 18), (13, 18)):                                # steel pool ladders
        X, Y = lx * 16, ly * 16
        r.rect(X + 3, Y - 4, X + 4, Y + 10, STEEL); r.rect(X + 11, Y - 4, X + 12, Y + 10, STEEL)
        r.rect(X + 3, Y - 4, X + 4, Y - 4, STEELL); r.rect(X + 11, Y - 4, X + 12, Y - 4, STEELL)
        for k in (0, 5):
            r.rect(X + 5, Y + k, X + 10, Y + k, STEELD)
    pal0 = read_pal(os.path.join(GBA, "data/tilesets/primary/building/palettes/00.pal"))
    badges = Image.open(ST.BADGES).load()
    top, base = ST.mark_top([[badges[16 + x, y] for x in range(16)] for y in range(16)]), ST.plinth()
    for sx in ((6, 10) if statues else ()):
        r.indexed(top, pal0, sx * 16, 16 * 16); r.indexed(base, pal0, sx * 16, 17 * 16)
    r.rect(7 * 16 + 2, 18 * 16 + 2, 10 * 16 - 3, 18 * 16 + 15, TRIM); r.rect(7 * 16 + 4, 18 * 16 + 4, 10 * 16 - 5, 18 * 16 + 13, TILEL)
    r.rect(7 * 16 + 4, 18 * 16 + 8, 10 * 16 - 5, 18 * 16 + 9, GUTTER)
    return r.im


# ARDOR BENCHMARK (GAUGE), from the concept approved 2026-09-15: the signal room. Vanilla's switch puzzle is whole --
# fifteen identical unlabelled ports where the bins stood, and the beam barrier a signal gate between two emitters,
# drawn on, half on and off so every block id the map script swaps in has art of its own
A_FLOOR, A_FLOORL, A_JOINT, A_TRACE, A_TRACEL = (58, 48, 52), (74, 62, 66), (40, 32, 36), (164, 100, 60), (212, 146, 92)
A_WALL, A_WALLD, A_WALLL, A_TRIM, A_TRAY = (124, 42, 42), (84, 28, 30), (164, 68, 58), (190, 118, 70), (46, 40, 44)
A_STEEL, A_STEELL, A_STEELD, A_HOLE = (150, 154, 160), (200, 204, 208), (96, 100, 108), (28, 26, 30)
A_AMBER, A_AMBERD, A_RED, A_GREEN = (255, 190, 80), (200, 120, 40), (230, 64, 52), (96, 206, 120)
A_BEAM, A_GLOW, A_EDGE, A_HAZ = (255, 240, 200), (255, 176, 84), (206, 96, 44), (236, 184, 48)
A_GATE = [(x, y) for y in (6, 7) for x in range(3, 8)]
A_IDS = {"half": [0x2BB, 0x2BC, 0x2BD, 0x2BE, 0x2BF, 0x2C3, 0x2C4, 0x2C5, 0x2C6, 0x2C7],
         "off":  [0x293, 0x294, 0x281, 0x295, 0x296, 0x29B, 0x29C, 0x281, 0x29D, 0x29E],
         "on":   [0x2A9, 0x2AA, 0x285, 0x2AB, 0x2AC, 0x2B1, 0x2B2, 0x28D, 0x2B3, 0x2B4]}   # on last: where half on draws
                                                                                    # the same, the map starts on on's ids


def ardor_room(gate="on", statues=True):
    ST = load("gbastatues")
    W, H = 11, 21
    r = Room(Image.new("RGB", (W * 16, H * 16)))
    under_gate = lambda x, y: 48 <= x < 128 and 96 <= y < 128           # no copper here: Floor 0x281 serves both rows
    for y in range(32, 20 * 16):                                        # dark floor panels, copper along the joints
        for x in range(W * 16):
            c = A_FLOOR
            if x % 16 == 0 or y % 16 == 0:
                c = A_JOINT
                if ((y % 32 == 0 and x % 16 != 0) or (x % 48 == 0 and y % 16 != 0)) and not under_gate(x, y):
                    c = A_TRACE
            elif x % 16 == 1 or y % 16 == 1:
                c = A_FLOORL
            r.px(x, y, c)
    for x in range(0, W * 16, 48):
        for y in range(32, 20 * 16, 32):
            if not under_gate(x, y) and not under_gate(x - 1, y - 1):
                r.rect(x - 1, y - 1, x + 1, y + 1, A_TRACEL)
    r.rect(0, 0, W * 16 - 1, 31, A_WALL); r.rect(0, 0, W * 16 - 1, 3, A_WALLD)          # the back wall and its scope
    r.rect(0, 24, W * 16 - 1, 27, A_TRAY); r.rect(0, 28, W * 16 - 1, 31, A_WALLD)
    r.rect(52, 4, 123, 22, A_STEELD); r.rect(54, 6, 121, 20, (20, 34, 30))
    for x in range(56, 120):
        r.px(x, 13 + int(5 * math.sin((x - 56) / 5.0) * (1 if (x // 16) % 2 else 0.4)), A_GREEN)
    for x in (16, 144):                                                  # vents
        r.rect(x, 6, x + 16, 20, A_TRAY)
        for k in range(4):
            r.rect(x + 2, 8 + k * 3, x + 14, 8 + k * 3, A_STEELD)
    for (x0, x1) in ((0, 15), (160, 175)):                               # GAUGE's end, its side walls
        r.rect(x0, 32, x1, 6 * 16 - 1, A_WALL); r.rect(x0 if x0 else x1 - 1, 32, x0 + 1 if x0 else x1, 6 * 16 - 1, A_WALLD)
    for (x0, x1) in ((0, 47), (128, 175)):                               # the wall across, either side of the gate
        r.rect(x0, 96, x1, 127, A_WALL); r.rect(x0, 96, x1, 98, A_WALLL); r.rect(x0, 124, x1, 127, A_WALLD)
        r.rect(x0, 106, x1, 109, A_TRAY)
    for rx in (2, 8):                                                    # amplifier racks, their lights blinking
        X = rx * 16
        r.rect(X + 1, 90, X + 14, 125, A_STEELD); r.rect(X + 2, 91, X + 13, 124, A_STEEL); r.rect(X + 2, 91, X + 13, 92, A_STEELL)
        for k in range(5):
            y = 97 + k * 5
            r.rect(X + 4, y, X + 11, y + 2, A_HOLE); r.px(X + 5 + k % 3, y + 1, [A_AMBER, A_RED, A_GREEN][k % 3])
    for cx in (3, 7):                                                    # copper coils where the pillars stood
        X = cx * 16
        r.rect(X + 3, 16, X + 12, 46, A_AMBERD)
        for y in range(18, 44, 3):
            r.rect(X + 2, y, X + 13, y + 1, A_TRIM); r.px(X + 3, y, A_TRACEL)
        r.rect(X + 2, 44, X + 13, 47, A_STEELD); r.rect(X + 4, 12, X + 11, 16, A_STEEL)
    r.shade(66, 64, 114, 66, 0.7)                                        # GAUGE's steel dais, a hazard stripe round it
    r.rect(64, 34, 111, 63, A_STEELD); r.rect(66, 36, 109, 61, A_STEEL); r.rect(66, 36, 109, 37, A_STEELL)
    for x in range(64, 112):
        if (x // 3) % 2:
            r.px(x, 34, A_HAZ); r.px(x, 63, A_HAZ)
    for ex in (3, 7):                                                    # the gate's emitters
        X = ex * 16
        r.rect(X + 4, 92, X + 11, 126, A_STEELD); r.rect(X + 5, 93, X + 10, 125, A_STEEL)
        for y in (104, 118):
            on = gate != "off"
            r.ellipse(X + 8, y, 4, 4, (A_AMBER if gate == "on" else A_AMBERD) if on else A_HOLE)
            r.ellipse(X + 8, y, 2, 2, A_BEAM if gate == "on" else (A_GLOW if on else A_STEELD))
    for k, y in enumerate((104, 118)):                                   # the beam: both on, the lower one off after a switch
        if gate == "off" or (gate == "half" and k == 1):
            continue
        for x in range(60, 117):
            r.px(x, y - 2, A_EDGE); r.px(x, y + 2, A_EDGE); r.px(x, y - 1, A_GLOW); r.px(x, y + 1, A_GLOW); r.px(x, y, A_BEAM)
            if (x * 7) % 11 == 0:
                r.px(x, y - 3, A_GLOW); r.px(x, y + 3, A_GLOW)
    for (bx, by) in [(x, y) for y in (10, 12, 14) for x in (1, 3, 5, 7, 9)]:   # fifteen ports, none of them labelled
        X, Y = bx * 16, by * 16
        r.shade(X + 4, Y + 13, X + 15, Y + 15, 0.6)
        r.rect(X + 2, Y + 1, X + 13, Y + 13, A_STEELD); r.rect(X + 3, Y + 2, X + 12, Y + 12, A_STEEL); r.rect(X + 3, Y + 2, X + 12, Y + 3, A_STEELL)
        for k in range(3):
            r.rect(X + 4 + k * 3, Y + 6, X + 5 + k * 3, Y + 8, A_HOLE)
        r.px(X + 11, Y + 10, A_STEELD)
    pal0 = read_pal(os.path.join(GBA, "data/tilesets/primary/building/palettes/00.pal"))
    badges = Image.open(ST.BADGES).load()
    top, base = ST.mark_top([[badges[32 + x, y] for x in range(16)] for y in range(16)]), ST.plinth()
    for sx in ((3, 7) if statues else ()):
        r.indexed(top, pal0, sx * 16, 16 * 16); r.indexed(base, pal0, sx * 16, 17 * 16)
    r.rect(66, 306, 108, 319, A_AMBERD); r.rect(68, 308, 106, 317, A_TRAY)      # the mat
    r.rect(0, 20 * 16, W * 16 - 1, H * 16 - 1, (0, 0, 0))
    return r.im


def ardor(old_img, statues=True):
    return ardor_room("on", statues)


def ardor_states():
    """Every block id the map script swaps into the gate, with the art of the state it names."""
    out = {}
    for gate, ids in A_IDS.items():
        im = ardor_room(gate).load()
        for (x, y), m in zip(A_GATE, ids):
            out[m] = tuple(im[x * 16 + i % 16, y * 16 + i // 16] for i in range(256))
    return out


# VERDIGRIS BENCHMARK (TRELLIS), from the concept approved 2026-09-15: the espalier house. Every hedge cell stays
# blocked and becomes a plant pruned flat along a verdigris frame; the lawn is mown in stripes, the flowers are
# identical seedlings on canes, the sand is gravel, the wall is a glasshouse
V_VERD, V_VERDL, V_VERDD = (84, 158, 138), (140, 204, 180), (46, 102, 90)
V_LEAF, V_LEAFL, V_LEAFD = (68, 138, 62), (116, 182, 86), (38, 90, 46)
V_GRASS, V_GRASSL, V_GRASSD = (98, 158, 86), (114, 174, 98), (78, 132, 72)
V_PATH, V_PATHL, V_PATHD = (204, 194, 168), (224, 216, 194), (164, 154, 130)
V_GLASS, V_GLASSL = (184, 222, 220), (226, 244, 240)
V_BRONZE, V_BRONZED, V_BLOOM, V_BLOOMD = (168, 124, 70), (116, 82, 46), (232, 214, 120), (190, 160, 70)


def verdigris(old_img, statues=True):
    ST = load("gbastatues")
    old = Old("celadon_gym")
    _, raw = old.layout("LAYOUT_CELADON_CITY_GYM")
    H, W = len(raw), len(raw[0])
    inside = lambda x, y: 1 <= x <= W - 2 and 2 <= y <= H - 2
    blocked = lambda x, y: inside(x, y) and bool((raw[y][x] >> 10) & 3)
    path = lambda x, y: inside(x, y) and ((5 <= x <= 7 and y >= 9) or (2 <= x <= 10 and 10 <= y <= 11) or y >= 15)
    flower = lambda x, y: (raw[y][x] & 0x3FF) in (0x2B6, 0x2B7)
    r = Room(Image.new("RGB", (W * 16, H * 16)))
    for y in range(2, H - 1):                                            # mown lawn, and gravel where the sand ran
        for x in range(1, W - 1):
            X, Y = x * 16, y * 16
            if path(x, y):
                for yy in range(16):
                    for xx in range(16):
                        c = V_PATH
                        if (xx * 5 + yy * 3 + x + y) % 11 == 0:
                            c = V_PATHD
                        elif (xx * 3 + yy * 7 + x) % 13 == 0:
                            c = V_PATHL
                        r.px(X + xx, Y + yy, c)
                if not path(x, y - 1) and inside(x, y - 1):              # bronze edging where the lawn stops
                    r.rect(X, Y, X + 15, Y + 1, V_VERDD)
                if not path(x - 1, y) and inside(x - 1, y):
                    r.rect(X, Y, X + 1, Y + 15, V_VERDD)
                if not path(x + 1, y) and inside(x + 1, y):
                    r.rect(X + 14, Y, X + 15, Y + 15, V_VERDD)
            else:
                r.rect(X, Y, X + 15, Y + 15, V_GRASSL if (x // 2) % 2 else V_GRASS)
                for k in range(0, 16, 4):
                    r.px(X + (k * 5 + y * 3) % 16, Y + k + 1, V_GRASSD)
    r.rect(0, 0, W * 16 - 1, 31, V_GLASS)                                # the glasshouse, its bars gone green
    for x in range(0, W * 16, 12):
        r.rect(x, 0, x + 1, 31, V_VERD)
    for y in (0, 11, 22):
        r.rect(0, y, W * 16 - 1, y + 1, V_VERD)
    for x in range(2, W * 16, 12):
        r.rect(x + 1, 3, x + 3, 9, V_GLASSL)
    r.rect(0, 28, W * 16 - 1, 31, V_VERDD)
    for x0 in (0, (W - 1) * 16):                                         # bronze columns, verdigris down them
        r.rect(x0, 0, x0 + 15, H * 16 - 1, V_VERD)
        r.rect(x0 + 3, 0, x0 + 12, H * 16 - 1, V_VERDL); r.rect(x0 + 7, 0, x0 + 8, H * 16 - 1, V_VERDD)
        for y in range(8, H * 16, 24):
            r.rect(x0 + 2, y, x0 + 13, y + 2, V_BRONZE)
    r.rect(0, (H - 1) * 16, W * 16 - 1, H * 16 - 1, (0, 0, 0))

    def espalier(cx, cy):
        X, Y = cx * 16, cy * 16
        r.shade(X, Y + 14, X + 15, Y + 15, 0.65)
        left, right = blocked(cx - 1, cy), blocked(cx + 1, cy)
        if not left:
            r.rect(X + 1, Y, X + 2, Y + 14, V_VERDD); r.px(X + 1, Y, V_VERDL)
        if not right:
            r.rect(X + 13, Y, X + 14, Y + 14, V_VERDD); r.px(X + 13, Y, V_VERDL)
        for wy in (3, 8, 12):
            r.rect(X + (0 if left else 2), Y + wy, X + (15 if right else 13), Y + wy, V_VERD)
        r.rect(X + 7, Y + 2, X + 8, Y + 14, V_BRONZED)
        for wy in (3, 8, 12):
            x0, x1 = X + (0 if left else 3), X + (15 if right else 12)
            for xx in range(x0, x1 + 1):
                k = (xx + wy * 5) % 5
                r.px(xx, Y + wy - 1, V_LEAF); r.px(xx, Y + wy + 1, V_LEAFD if k < 3 else V_LEAF)
                if k != 4:
                    r.px(xx, Y + wy - 2, V_LEAFL if k == 1 else V_LEAF)
                if k in (0, 2):
                    r.px(xx, Y + wy - 3, V_LEAFL)
                if k == 3 and wy != 12:
                    r.px(xx, Y + wy + 2, V_LEAFD)
            for xx in range(x0, x1 + 1, 4):
                r.px(xx + 1, Y + wy, V_VERDL)
        r.rect(X + 6, Y + 14, X + 9, Y + 15, V_BRONZED)
    for y in range(H):
        for x in range(W):
            if blocked(x, y):
                espalier(x, y)
            elif flower(x, y):                                           # identical seedlings, one bloom each
                X, Y = x * 16, y * 16
                for (sx, sy) in ((4, 5), (11, 5), (4, 12), (11, 12)):
                    r.rect(X + sx, Y + sy - 4, X + sx, Y + sy + 1, V_BRONZE)
                    r.px(X + sx - 1, Y + sy - 1, V_LEAF); r.px(X + sx + 1, Y + sy - 2, V_LEAF)
                    r.px(X + sx - 1, Y + sy - 4, V_BLOOM); r.px(X + sx, Y + sy - 5, V_BLOOM); r.px(X + sx + 1, Y + sy - 4, V_BLOOMD)
                    r.px(X + sx - 1, Y + sy + 2, V_GRASSD); r.px(X + sx + 1, Y + sy + 2, V_GRASSD)
    for x in range(5 * 16, 9 * 16):                                      # TRELLIS's alcove, gravel edged in bronze
        for y in range(4 * 16, 5 * 16):
            r.px(x, y, V_PATHD if (x * 5 + y * 3) % 11 == 0 else (V_PATHL if (x * 3 + y * 7) % 13 == 0 else V_PATH))
    r.rect(5 * 16, 5 * 16 - 2, 9 * 16 - 1, 5 * 16 - 1, V_VERDD)
    pal0 = read_pal(os.path.join(GBA, "data/tilesets/primary/building/palettes/00.pal"))
    badges = Image.open(ST.BADGES).load()
    top, base = ST.mark_top([[badges[48 + x, y] for x in range(16)] for y in range(16)]), ST.plinth()
    for sx in ((4, 8) if statues else ()):
        r.indexed(top, pal0, sx * 16, 15 * 16); r.indexed(base, pal0, sx * 16, 16 * 16)
    r.rect(5 * 16 + 2, 18 * 16 + 2, 8 * 16 - 3, 18 * 16 + 15, V_VERDD); r.rect(5 * 16 + 4, 18 * 16 + 4, 8 * 16 - 5, 18 * 16 + 13, V_VERD)
    for x in range(5 * 16 + 6, 8 * 16 - 6, 4):
        r.rect(x, 18 * 16 + 6, x, 18 * 16 + 11, V_VERDL)
    return r.im


# LURID BENCHMARK (TILT), from the concept approved 2026-09-15 (v3). A new invisible maze in two halves joined by four
# corner pads that turn you one way only, clockwise: the first half ends at the upper-left pad, which puts you upper
# right for the second. The lower-left pad has a pocket of its own, so nobody skips the first half; it is also the
# second half's way back. The floor is a grid that leans, the same over wall and open cell alike. When TILT loses,
# every leaning tile a wall mostly covers swaps its light and dark, and a lit way opens from his dais to the door
L_GRID = [                                # rows 2..21; # an invisible wall (or a statue), P a pad
    "P.....#.....##P",
    ".##.#.#.#.#.#..",
    "#..#..#..##....",
    "......#.##.#...",
    ".#...##....#.#.",
    ".#....##..#.#.#",
    "..##.##.#......",
    ".#....#..#.###.",
    "..#...#...#....",
    "#..####.#...#.#",
    "##...#...#..#..",
    "...#.#....#..#.",
    "###..#....##.#.",
    "....##....#....",
    ".#.#.######....",
    ".#.........#...",
    "..#.#..#..###..",
    "#...####..#.#..",
    ".#.#........#..",
    "P.#..#...#..#.P",
]
L_PADS = [(0, 2), (14, 2), (14, 21), (0, 21)]           # clockwise: each sends you to the next
L_STATUES = [(4, 19), (10, 19)]
L_DOOR = [(6, 21), (7, 21), (8, 21)]
L_EXIT = {(7, 16), (7, 18), (7, 19)}                     # opened when TILT loses: straight down to the door
L_WALLS = {(x, y + 2) for y, row in enumerate(L_GRID) for x, ch in enumerate(row) if ch == "#"}
L_PLAN = {(x, y + 2): (ch == "#", 0x67 if ch == "P" else 0)          # MB_REGULAR_WARP on the pads
          for y, row in enumerate(L_GRID) for x, ch in enumerate(row) if (x, y + 2) not in L_STATUES + L_DOOR}
L_FLOOR, L_FLOORL, L_LINE, L_LINEL = (192, 188, 140), (230, 228, 190), (158, 152, 110), (242, 240, 208)
L_WALL, L_WALLD, L_WALLL = (76, 50, 86), (50, 32, 58), (108, 76, 116)
L_GLOW, L_GLOWL, L_MAG = (196, 238, 118), (236, 255, 200), (222, 96, 172)
L_DAIS, L_DAISL, L_DAISD, L_PADC = (132, 100, 132), (170, 136, 164), (92, 66, 94), (60, 40, 70)


def lurid_check():
    """The halves are sealed from each other, the pocket holds the pad and two cells, and every open cell belongs to
    one of the three; after the win the way out reaches TILT from the door"""
    def reach(start, walls):
        seen, todo = {start}, [start]
        while todo:
            x, y = todo.pop()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= n[0] < 15 and 2 <= n[1] <= 21 and n not in walls and n not in seen:
                    seen.add(n); todo.append(n)
        return seen
    a, b, c = reach((7, 21), L_WALLS), reach((14, 2), L_WALLS), reach((0, 21), L_WALLS)
    opened = {(x, y) for x in range(15) for y in range(2, 22) if (x, y) not in L_WALLS}
    assert (0, 2) in a and (14, 21) in b and (7, 14) in b and not a & b and not c & (a | b) and len(c) == 3, "LURID: the halves leak"
    assert opened == a | b | c, "LURID: a pocket nobody can reach"
    assert (7, 14) in reach((7, 21), L_WALLS - L_EXIT), "LURID: the way out does not reach TILT"


def lurid_room(after=False):
    from collections import Counter
    ST = load("gbastatues")
    W, H = 15, 23
    r = Room(Image.new("RGB", (W * 16, H * 16)))
    flipped = set()
    if after:                                            # a leaning tile flips whole when a wall covers most of it
        hidden = L_WALLS - set(L_STATUES) - {(x, y - 1) for x, y in L_STATUES} - L_EXIT
        inwall, total = Counter(), Counter()
        for y in range(32, 22 * 16):
            for x in range(W * 16):
                t = ((x + y // 2) // 16, y // 16)
                total[t] += 1
                if (x // 16, y // 16) in hidden:
                    inwall[t] += 1
        flipped = {t for t in total if inwall[t] * 2 > total[t]}
    for y in range(32, 22 * 16):                         # the grid leans half a pixel a row
        for x in range(W * 16):
            u = x + y // 2
            light = ((u // 16) + (y // 16)) % 2 == 1
            if (u // 16, y // 16) in flipped:
                light = not light
            c = L_FLOORL if light else L_FLOOR
            if u % 16 == 0 or y % 16 == 0:
                c = L_LINE
            elif u % 16 == 1 or y % 16 == 1:
                c = L_LINEL
            if x < 6:
                c = tuple(int(v * 0.86) for v in c)
            r.px(x, y, c)
    r.rect(0, 0, W * 16 - 1, 31, L_WALL); r.rect(0, 0, W * 16 - 1, 2, L_WALLD); r.rect(0, 27, W * 16 - 1, 31, L_WALLD)
    r.rect(0, 25, W * 16 - 1, 26, L_WALLL)
    r.rect(64, 4, 175, 23, L_WALLD); r.rect(66, 6, 173, 21, (34, 26, 40))          # a distribution with a long tail
    for k, h in enumerate([2, 5, 11, 14, 12, 9, 7, 5, 4, 3, 3, 2, 2, 1, 1, 1, 1, 1]):
        r.rect(70 + k * 6, 20 - h, 74 + k * 6, 20, L_GLOW if k != 3 else L_MAG)
    for lx in (24, 208):
        r.rect(lx, 6, lx + 7, 20, L_WALLL); r.ellipse(lx + 3, 12, 3, 5, L_GLOW); r.ellipse(lx + 3, 12, 1, 3, L_GLOWL)
    for y in range(12 * 16 + 2, 15 * 16 - 2):           # TILT's slab, leaning with the floor
        s = (y - 12 * 16) // 2
        x0, x1 = 6 * 16 + 10 - s, 9 * 16 - 2 - s
        for x in range(x0, x1 + 1):
            r.px(x, y, L_DAISL if (y < 12 * 16 + 4 or x < x0 + 2) else (L_DAISD if (y > 15 * 16 - 5 or x > x1 - 2) else L_DAIS))
    if after:                                            # the way out, lit
        r.rect(7 * 16 + 5, 15 * 16, 7 * 16 + 10, 21 * 16 - 1, L_GLOW); r.rect(7 * 16 + 7, 15 * 16, 7 * 16 + 8, 21 * 16 - 1, L_GLOWL)
    for (px_, py_) in L_PADS:                            # the pads: a spiral winding clockwise
        cx, cy = px_ * 16 + 8, py_ * 16 + 8
        r.ellipse(cx, cy, 7, 7, L_WALLD); r.ellipse(cx, cy, 6, 6, L_PADC)
        for k in range(90):
            rad = 0.6 + k * 0.058
            r.px(int(round(cx + rad * math.cos(k * 0.19))), int(round(cy + rad * math.sin(k * 0.19))), L_MAG if k < 60 else L_GLOW)
    pal0 = read_pal(os.path.join(GBA, "data/tilesets/primary/building/palettes/00.pal"))
    badges = Image.open(ST.BADGES).load()
    top, base = ST.mark_top([[badges[64 + x, y] for x in range(16)] for y in range(16)]), ST.plinth()
    for sx, sy in L_STATUES:                             # SKEW; their heads are solid here, so nobody stands behind
        r.indexed(top, pal0, sx * 16, (sy - 1) * 16); r.indexed(base, pal0, sx * 16, sy * 16)
    r.rect(6 * 16 + 2, 21 * 16 + 2, 9 * 16 - 3, 21 * 16 + 15, L_WALLD); r.rect(6 * 16 + 4, 21 * 16 + 4, 9 * 16 - 5, 21 * 16 + 13, L_WALL)
    for x in range(6 * 16 + 6, 9 * 16 - 6, 3):
        r.px(x, 21 * 16 + 8 + (x // 3) % 2, L_GLOW)
    r.rect(0, 22 * 16, W * 16 - 1, H * 16 - 1, (0, 0, 0))
    return r.im


def lurid(old_img):
    lurid_check()
    return lurid_room()


# BRAZEN BENCHMARK (MATTE), from the concept approved 2026-09-15: the gallery of mounts. Vanilla's pad maze is whole
# and every cell keeps its collision. Each room is a picture seen through its own mat -- gilt frame mouldings between
# rooms, a cream bevelled mat where they meet a room, a halftone print in a different ink on each floor, so a room
# shows only its own part of the picture. The pads are brass viewfinders; MATTE stands on the bare mount, framed
B_GALLERY, B_GALLERYD = (58, 44, 40), (38, 28, 26)
B_GILT, B_GILTL, B_GILTD, B_GILTS = (196, 150, 64), (238, 204, 116), (130, 90, 36), (96, 64, 28)
B_MAT, B_MATL, B_MATD = (232, 224, 204), (248, 244, 232), (196, 186, 164)
B_BRASS, B_BRASSL = (214, 170, 72), (250, 222, 140)
B_CYAN, B_MAGENTA_INK, B_YELLOW, B_KEY = ((214, 230, 232), (110, 170, 190)), ((236, 220, 228), (190, 110, 150)), \
    ((238, 232, 204), (206, 176, 80)), ((226, 226, 228), (120, 122, 136))
B_INKS = {(0, 0): B_CYAN, (1, 0): B_MAGENTA_INK, (2, 0): B_YELLOW, (0, 1): B_KEY, (1, 1): None, (2, 1): B_CYAN,
          (0, 2): B_YELLOW, (1, 2): B_KEY, (2, 2): B_MAGENTA_INK}
B_ROOMS_X, B_ROOMS_Y = [(0, 8), (10, 18), (20, 28)], [(2, 7), (10, 15), (18, 23)]
B_STATUES = [(12, 20), (16, 20)]


def brazen(old_img, statues=True):
    ST = load("gbastatues")
    W, H = 29, 25
    pads = {(w["x"], w["y"]) for w in json.load(open(os.path.join(GBA, "data/maps/SaffronCity_Gym/map.json")))["warp_events"]
            if w["dest_map"] == "MAP_SAFFRON_CITY_GYM"}
    r = Room(Image.new("RGB", (W * 16, H * 16)))
    r.rect(0, 0, W * 16 - 1, H * 16 - 1, B_GALLERY)
    for wy in (0, 8, 16):                                # the gallery wall over each row of rooms, a brass picture rail
        Y = wy * 16
        r.rect(0, Y, W * 16 - 1, Y + 3, B_GALLERYD)
        r.rect(0, Y + 10, W * 16 - 1, Y + 11, B_GILTD); r.rect(0, Y + 12, W * 16 - 1, Y + 12, B_GILT)
    for ry, (y0, y1) in enumerate(B_ROOMS_Y):
        for rx, (x0, x1) in enumerate(B_ROOMS_X):
            ink = B_INKS[(rx, ry)]
            X0, Y0, X1, Y1 = x0 * 16, y0 * 16, (x1 + 1) * 16 - 1, (y1 + 1) * 16 - 1
            for y in range(Y0, Y1 + 1):
                for x in range(X0, X1 + 1):
                    c = B_MATL
                    if ink:                              # halftone: a big dot, then a small one
                        paper, dot = ink
                        dx, dy, big = x % 8, y % 8, (x // 8 + y // 8) % 2 == 0
                        c = paper
                        if big and 2 <= dx <= 5 and 2 <= dy <= 5 and not (dx in (2, 5) and dy in (2, 5)):
                            c = dot
                        elif not big and dx in (3, 4) and dy in (3, 4):
                            c = dot
                    r.px(x, y, c)
            r.rect(X0, Y0, X1, Y0 + 2, B_MATD); r.rect(X0, Y0 + 3, X1, Y0 + 3, B_MAT)      # the mat's bevel
            r.rect(X0, Y0, X0 + 1, Y1, B_MATL); r.rect(X1 - 1, Y0, X1, Y1, B_MATD); r.rect(X0, Y1 - 1, X1, Y1, B_MATD)
    for vx in (9, 19):                                   # the gilt mouldings between rooms
        X = vx * 16
        r.rect(X, 32, X + 15, (H - 1) * 16 - 1, B_GILT)
        r.rect(X + 2, 32, X + 3, (H - 1) * 16 - 1, B_GILTL); r.rect(X + 7, 32, X + 8, (H - 1) * 16 - 1, B_GILTD)
        r.rect(X + 12, 32, X + 13, (H - 1) * 16 - 1, B_GILTS)
        for y in range(32, (H - 1) * 16, 6):
            r.px(X + 5, y, B_GILTL); r.px(X + 10, y + 3, B_GILTD)
    for wy in (7, 15):
        Y = (wy + 1) * 16 + 24
        r.rect(0, Y, W * 16 - 1, Y + 7, B_GILT); r.rect(0, Y + 1, W * 16 - 1, Y + 2, B_GILTL); r.rect(0, Y + 6, W * 16 - 1, Y + 7, B_GILTS)
    r.rect(0, (H - 1) * 16, W * 16 - 1, H * 16 - 1, (0, 0, 0))
    for (px_, py_) in pads:                              # brass viewfinders round a dark window
        X, Y = px_ * 16, py_ * 16
        r.rect(X + 3, Y + 3, X + 12, Y + 12, B_GALLERY); r.rect(X + 5, Y + 5, X + 10, Y + 10, B_GALLERYD)
        for (cx, cy, sx, sy) in ((1, 1, 1, 1), (13, 1, -1, 1), (1, 13, 1, -1), (13, 13, -1, -1)):
            r.rect(min(X + cx, X + cx + sx * 5), min(Y + cy, Y + cy + 1), max(X + cx, X + cx + sx * 5) + (1 if sx < 0 else 0), max(Y + cy, Y + cy + 1), B_BRASS)
            r.rect(min(X + cx, X + cx + 1), min(Y + cy, Y + cy + sy * 5), max(X + cx, X + cx + 1), max(Y + cy, Y + cy + sy * 5) + (1 if sy < 0 else 0), B_BRASS)
            r.px(X + cx + (1 if sx > 0 else 0), Y + cy + (1 if sy > 0 else 0), B_BRASSL)
        r.rect(X + 7, Y + 7, X + 8, Y + 8, B_BRASSL)
    FX0, FY0, FX1, FY1 = 12 * 16 + 4, 10 * 16 + 2, 17 * 16 - 5, 13 * 16 - 3        # MATTE's mount, an empty gilt frame
    r.rect(FX0, FY0, FX1, FY1, B_GILT); r.rect(FX0 + 5, FY0 + 5, FX1 - 5, FY1 - 5, B_MATL)
    r.rect(FX0 + 1, FY0 + 1, FX1 - 1, FY0 + 2, B_GILTL); r.rect(FX0 + 1, FY0 + 1, FX0 + 2, FY1 - 1, B_GILTL)
    r.rect(FX0 + 1, FY1 - 2, FX1 - 1, FY1 - 1, B_GILTS); r.rect(FX1 - 2, FY0 + 1, FX1 - 1, FY1 - 1, B_GILTS)
    r.rect(FX0 + 5, FY0 + 5, FX1 - 5, FY0 + 6, B_MATD)
    pal0 = read_pal(os.path.join(GBA, "data/tilesets/primary/building/palettes/00.pal"))
    badges = Image.open(ST.BADGES).load()
    top, base = ST.mark_top([[badges[80 + x, y] for x in range(16)] for y in range(16)]), ST.plinth()
    for sx, sy in (B_STATUES if statues else ()):        # FRAME
        r.indexed(top, pal0, sx * 16, (sy - 1) * 16); r.indexed(base, pal0, sx * 16, sy * 16)
    r.rect(13 * 16 + 2, 23 * 16 + 2, 16 * 16 - 3, 23 * 16 + 15, B_GILTD); r.rect(13 * 16 + 4, 23 * 16 + 4, 16 * 16 - 5, 23 * 16 + 13, B_MAT)
    return r.im


# QUICKSILVER BENCHMARK (ANNEAL), from the concept approved 2026-09-15: the silver lab where S.T.A.R.R. was built.
# Vanilla's quiz is whole. Everything is mercury and steel, and the one colour in the room is S.T.A.R.R.'s blue: the
# conduit up the middle and its light on the floor, the quiz still running on her machines, the barrier the conduit
# holds shut -- and, never pointed at, a deer: antler-branched electrodes at the conduit's head, the same antlers
# engraved in ANNEAL's annealing plate. The quiz doors open by the script's own blocks, drawn from the room opened
Q_DOORS = {1: (26, 8), 2: (17, 8), 3: (17, 15), 5: (5, 16), 6: (5, 8)}        # top-left of each 2x2 door
Q_DOOR4 = [(11, 22), (11, 23)]
Q_DOOR_CELLS = {(x + dx, y + dy) for (x, y) in Q_DOORS.values() for dx in (0, 1) for dy in (0, 1)}
Q_QUIZ = [(22, 10), (15, 2), (13, 10), (13, 17), (1, 18), (1, 10)]            # left cell of each machine
Q_STATUES = [(23, 20), (27, 20)]
Q_USES = {                                                                     # each script id, every cell it is set at
    0x2C7: [(x, y) for (x, y) in Q_DOORS.values()], 0x2C6: [(x + 1, y) for (x, y) in Q_DOORS.values()],
    0x2CF: [(x, y + 1) for (x, y) in Q_DOORS.values()], 0x2CE: [(x + 1, y + 1) for (x, y) in Q_DOORS.values()],
    0x289: [(x, y + 2) for (x, y) in Q_DOORS.values()] + [(11, 22)], 0x281: [(x + 1, y + 2) for (x, y) in Q_DOORS.values()] + [(11, 23)],
    0x282: [(x + 2, y + 2) for (x, y) in Q_DOORS.values()], 0x2D1: [(11, 21)]}
Q_FLOOR, Q_FLOORL, Q_JOINT, Q_RIVET = (146, 152, 160), (168, 174, 182), (108, 114, 124), (190, 196, 204)
Q_TOP, Q_TOPL, Q_FACE, Q_FACED, Q_FACEL = (196, 200, 208), (226, 230, 236), (118, 124, 134), (84, 90, 100), (150, 156, 166)
Q_BACK, Q_BACKD, Q_BACKL = (72, 78, 90), (50, 54, 64), (96, 102, 116)
Q_GLASS, Q_GLASSL, Q_CASE, Q_CASEL = (26, 34, 52), (60, 76, 104), (170, 176, 186), (206, 212, 220)
Q_BLUE, Q_BLUEL, Q_BLUED, Q_CORE = (72, 164, 255), (164, 214, 255), (36, 92, 196), (232, 246, 255)


def quicksilver_room(doors_open=False, statues=True):
    ST = load("gbastatues")
    _, raw = Old("cinnabar_gym").layout("LAYOUT_CINNABAR_ISLAND_GYM")
    H, W = len(raw), len(raw[0])
    conduit = lambda x, y: 10 <= x <= 12 and y <= 21

    def blocked(x, y):
        if not (0 <= x < W and 0 <= y < H):
            return True
        if doors_open and ((x, y) in Q_DOOR_CELLS or (x, y) in Q_DOOR4):
            return False
        return bool((raw[y][x] >> 10) & 3)

    r = Room(Image.new("RGB", (W * 16, H * 16)))

    def line(x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            r.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

    for y in range(H * 16):                              # steel plate, the same in every cell
        for x in range(W * 16):
            dx, dy = x % 16, y % 16
            c = Q_FLOOR
            if dx == 0 or dy == 0:
                c = Q_JOINT
            elif dx == 1 or dy == 1:
                c = Q_FLOORL
            elif (dx, dy) in ((3, 3), (12, 3), (3, 12), (12, 12)):
                c = Q_RIVET
            r.px(x, y, c)
    r.rect(0, 0, W * 16 - 1, 31, Q_BACK); r.rect(0, 0, W * 16 - 1, 3, Q_BACKD); r.rect(0, 24, W * 16 - 1, 31, Q_FACE)
    r.rect(0, 24, W * 16 - 1, 25, Q_FACEL); r.rect(0, 30, W * 16 - 1, 31, Q_FACED)
    for x in range(8, W * 16, 32):
        r.rect(x, 6, x + 1, 22, Q_BACKL)
    for y in range(2, H - 1):                            # wall cells: a front face over floor, a top face otherwise
        for x in range(W):
            if conduit(x, y) or not blocked(x, y):
                continue
            X, Y = x * 16, y * 16
            if not blocked(x, y + 1):
                r.rect(X, Y, X + 15, Y + 15, Q_FACE); r.rect(X, Y, X + 15, Y + 2, Q_TOPL); r.rect(X, Y + 13, X + 15, Y + 15, Q_FACED)
                r.rect(X, Y + 7, X + 15, Y + 7, Q_FACEL)
                if not conduit(x, y + 1):
                    r.shade(X, Y + 16, X + 15, Y + 18, 0.8)
            else:
                r.rect(X, Y, X + 15, Y + 15, Q_TOP)
                if not blocked(x - 1, y): r.rect(X, Y, X + 1, Y + 15, Q_TOPL)
                if not blocked(x + 1, y): r.rect(X + 14, Y, X + 15, Y + 15, Q_FACED)
    for (x, y) in Q_DOORS.values():
        if doors_open:                                   # a gap in the wall, its two ends shown
            for dy in (0, 1):
                r.rect(x * 16, (y + dy) * 16, x * 16 + 1, (y + dy) * 16 + 15, Q_FACED)
                r.rect((x + 2) * 16 - 2, (y + dy) * 16, (x + 2) * 16 - 1, (y + dy) * 16 + 15, Q_FACED)
        else:                                            # a steel shutter with a blue seam
            X, Y = x * 16, y * 16
            r.rect(X, Y + 4, X + 31, Y + 15, Q_TOP); r.rect(X, Y + 4, X + 31, Y + 5, Q_TOPL)
            r.rect(X, Y + 16, X + 31, Y + 31, Q_FACE); r.rect(X, Y + 16, X + 31, Y + 17, Q_TOPL); r.rect(X, Y + 29, X + 31, Y + 31, Q_FACED)
            for k in range(Y + 19, Y + 29, 3):
                r.rect(X + 2, k, X + 29, k, Q_FACED)
            r.rect(X + 15, Y + 17, X + 16, Y + 28, Q_BLUED); r.px(X + 15, Y + 22, Q_BLUE); r.px(X + 16, Y + 23, Q_BLUE)
    for y in range(2 * 16, 22 * 16):                     # the conduit's light on the floor, columns 9 and 13 only
        for x in list(range(9 * 16, 10 * 16)) + list(range(13 * 16, 14 * 16)):
            if blocked(x // 16, y // 16):
                continue
            d = (10 * 16 + 4 - x) if x < 11 * 16 else (x - (13 * 16 - 5))
            k = max(0.0, 1 - d / 18.0) * 0.28
            p = r.p[x, y]
            r.px(x, y, tuple(int(p[i] * (1 - k) + Q_BLUEL[i] * k) for i in range(3)))
    X0, X1, cx = 10 * 16 + 4, 13 * 16 - 5, 11 * 16 + 8   # the conduit, a glass column of blue light
    r.rect(X0, 0, X1, 22 * 16 - 1, Q_CASE); r.rect(X0 + 3, 0, X1 - 3, 22 * 16 - 1, Q_GLASS); r.rect(X0 + 4, 0, X0 + 4, 22 * 16 - 1, Q_GLASSL)
    for y in range(24, 21 * 16 + 8):
        w = 2 + int(1.5 * (1 + math.sin(y * 2 * math.pi / 16)))
        r.rect(cx - w, y, cx + w, y, Q_BLUED); r.rect(cx - max(0, w - 2), y, cx + max(0, w - 2), y, Q_BLUE)
        r.px(cx, y, Q_CORE if y % 16 < 8 else Q_BLUEL)
    for y in range(32, 21 * 16, 32):
        r.rect(X0, y, X1, y + 2, Q_CASE); r.rect(X0 + 1, y + 1, X1 - 1, y + 1, Q_CASEL)
    r.rect(9 * 16, 4, 14 * 16 - 1, 23, Q_BACKD)          # the electrodes at its head, branched like antlers
    for s in (-1, 1):
        beam = [(cx + s * 2, 24), (cx + s * 12, 18), (cx + s * 24, 13), (cx + s * 34, 6)]
        for (a, b) in zip(beam, beam[1:]):
            line(*a, *b, Q_BLUEL); line(a[0], a[1] - 1, b[0], b[1] - 1, Q_BLUE)
        for (t0, t1) in (((cx + s * 12, 18), (cx + s * 14, 8)), ((cx + s * 24, 13), (cx + s * 27, 4)),
                         ((cx + s * 30, 9), (cx + s * 38, 12)), ((cx + s * 18, 15), (cx + s * 21, 7))):
            line(*t0, *t1, Q_BLUE)
        r.px(cx + s * 34, 6, Q_CORE); r.px(cx + s * 27, 4, Q_CORE); r.px(cx + s * 14, 8, Q_CORE)
    r.rect(cx - 6, 24, cx + 6, 31, Q_CASE); r.rect(cx - 3, 26, cx + 3, 29, Q_BLUEL)
    r.rect(X0, 21 * 16 + 6, X1, 21 * 16 + 15, Q_CASE); r.rect(X0 + 2, 21 * 16 + 8, X1 - 2, 21 * 16 + 9, Q_CASEL)
    if doors_open:                                       # door 4: the barrier retracted, the emitter capped
        r.rect(cx - 3, 21 * 16 + 11, cx + 3, 21 * 16 + 13, Q_BLUED)
    else:                                                # door 4: the barrier the conduit's light holds shut
        for y in range(22 * 16, 24 * 16):
            r.rect(11 * 16 + 1, y, 11 * 16 + 2, y, Q_CASE); r.rect(11 * 16 + 13, y, 11 * 16 + 14, y, Q_CASE)
            for x in range(11 * 16 + 3, 11 * 16 + 13):
                ph = (x * 3 + y) % 8
                r.px(x, y, Q_BLUEL if ph == 0 else (Q_BLUE if ph < 4 else Q_BLUED))
    for (qx, qy) in Q_QUIZ:                              # the quiz, still running on her machines
        X, Y = qx * 16, qy * 16
        r.rect(X + 2, Y - 10, X + 29, Y + 13, Q_CASE); r.rect(X + 2, Y - 10, X + 29, Y - 9, (214, 218, 226))
        r.rect(X + 5, Y - 7, X + 26, Y + 5, Q_GLASS)
        for k, yy in enumerate(range(Y - 5, Y + 4, 3)):
            r.rect(X + 7, yy, X + 7 + (8 + (k * 5 + qx) % 12), yy, Q_BLUE if k else Q_BLUEL)
        r.rect(X + 5, Y + 8, X + 26, Y + 10, Q_FACED)
        for k in range(5):
            r.rect(X + 7 + k * 4, Y + 8, X + 8 + k * 4, Y + 9, Q_TOP)
    pcx, pcy = 5 * 16 + 8, 4 * 16 + 8                    # ANNEAL's annealing plate, the antlers engraved
    r.ellipse(pcx, pcy + 2, 23, 21, Q_FACED); r.ellipse(pcx, pcy, 23, 21, Q_CASE); r.ellipse(pcx, pcy, 20, 18, (132, 138, 148))
    r.ellipse(pcx, pcy, 18, 16, (150, 156, 166))
    for s in (-1, 1):
        beam = [(pcx + s, pcy + 9), (pcx + s * 5, pcy + 3), (pcx + s * 9, pcy - 3), (pcx + s * 12, pcy - 10)]
        for (a, b) in zip(beam, beam[1:]):
            line(*a, *b, Q_BLUED); line(a[0] + s, a[1], b[0] + s, b[1], Q_BLUED)
        line(pcx + s * 5, pcy + 3, pcx + s * 12, pcy + 1, Q_BLUED); line(pcx + s * 9, pcy - 3, pcx + s * 15, pcy - 4, Q_BLUED)
        line(pcx + s * 10, pcy - 6, pcx + s * 7, pcy - 12, Q_BLUED)
        r.px(pcx + s * 12, pcy - 10, Q_BLUE); r.px(pcx + s * 15, pcy - 4, Q_BLUE); r.px(pcx + s * 7, pcy - 12, Q_BLUE)
    r.rect(3 * 16 + 2, 8, 3 * 16 + 13, 22, Q_CASE); r.rect(3 * 16 + 4, 10, 3 * 16 + 11, 20, (186, 180, 164))    # the photograph
    r.rect(3 * 16 + 6, 13, 3 * 16 + 7, 18, Q_FACED); r.rect(3 * 16 + 9, 12, 3 * 16 + 10, 18, Q_FACED)
    pal0 = read_pal(os.path.join(GBA, "data/tilesets/primary/building/palettes/00.pal"))
    badges = Image.open(ST.BADGES).load()
    top, base = ST.mark_top([[badges[96 + x, y] for x in range(16)] for y in range(16)]), ST.plinth()
    for sx, sy in (Q_STATUES if statues else ()):        # HEAT
        r.indexed(top, pal0, sx * 16, (sy - 1) * 16); r.indexed(base, pal0, sx * 16, sy * 16)
    r.rect(24 * 16 + 2, 23 * 16 + 2, 27 * 16 - 3, 23 * 16 + 15, Q_FACED); r.rect(24 * 16 + 4, 23 * 16 + 4, 27 * 16 - 5, 23 * 16 + 13, Q_FACE)
    r.rect(24 * 16 + 4, 23 * 16 + 8, 27 * 16 - 5, 23 * 16 + 8, Q_BLUED)
    r.rect(0, (H - 1) * 16, W * 16 - 1, H * 16 - 1, (0, 0, 0))
    return r.im


def quicksilver(old_img, statues=True):
    return quicksilver_room(False, statues)


def quicksilver_states():
    """Each block id the quiz doors' scripts set, drawn from the room with every door open; an id used at several
    doors must draw the same at all of them, or the room would open wrongly somewhere"""
    im = quicksilver_room(True).load()
    art = lambda x, y: tuple(im[x * 16 + i % 16, y * 16 + i // 16] for i in range(256))
    out = {}
    for m, cells in Q_USES.items():
        arts = {art(*c) for c in cells}
        assert len(arts) == 1, "QUICKSILVER: block 0x%X draws differently at %s" % (m, cells)
        out[m] = arts.pop()
    return out


# the REPO's materials
def repo(old_img):
    W, H = 11, 9
    r = Room(Image.new("RGB", (W * 16, H * 16)))
    WALL, WALLL, BAND, BANDD, SKIRT = (236, 226, 202), (246, 238, 220), (212, 160, 76), (170, 116, 52), (92, 66, 44)
    CON, CONJ, TAPE = (196, 192, 182), (176, 172, 162), (226, 176, 70)
    for y in range(32, 128):
        for x in range(176):
            r.px(x, y, CONJ if (x % 32 == 0 or y % 32 == 0) else CON)
    r.shade(0, 32, 175, 35, 0.86)
    for y in range(80, 128):
        if y % 6 < 4:
            r.rect(64, y, 65, y, TAPE)
    for x in range(66):
        if x % 6 < 4:
            r.rect(x, 82, x, 83, TAPE)
    r.rect(0, 0, 175, 3, (72, 58, 44)); r.rect(0, 4, 175, 17, WALL); r.rect(0, 4, 175, 4, WALLL)
    r.rect(0, 18, 175, 21, BAND); r.rect(0, 21, 175, 21, BANDD); r.rect(0, 22, 175, 27, WALL); r.rect(0, 28, 175, 31, SKIRT)
    r.rect(33, 5, 47, 26, (60, 48, 36)); r.rect(34, 6, 46, 25, (246, 232, 190))
    em = EM.emblem("REPO", {"O": 1, "L": 2, "M": 3, "T": 4})
    epal = {1: (80, 56, 30), 2: (238, 214, 140), 3: (170, 120, 54), 4: (250, 244, 220)}
    for y in range(16):
        for x in range(16):
            if em[y][x] and 1 <= x <= 13 and 1 <= y <= 15:
                r.px(33 + x, 7 + y, epal[em[y][x]])
    r.shade(66, 33, 112, 35, 0.8)
    r.rect(64, 6, 111, 23, (120, 84, 50)); r.rect(64, 6, 111, 7, (160, 116, 70))
    for x in range(66, 110, 11):
        for y in (9, 16):
            r.rect(x, y, x + 9, y + 5, (212, 160, 76)); r.rect(x + 3, y + 2, x + 6, y + 3, (246, 246, 238))
    r.rect(64, 24, 111, 32, (230, 200, 150)); r.rect(64, 30, 111, 32, (190, 150, 96)); r.rect(64, 32, 111, 32, (80, 56, 30))
    r.rect(68, 19, 79, 26, (70, 76, 86)); r.rect(70, 21, 77, 22, (246, 246, 238))
    r.ellipse(88, 25, 3, 2, (170, 116, 52)); r.rect(95, 21, 103, 27, (212, 160, 76)); r.rect(97, 23, 101, 24, (246, 246, 238))
    OAK, OAKD, AMB, AMBD, EDGE = (232, 204, 156), (204, 172, 120), (204, 150, 68), (160, 108, 44), (70, 48, 26)
    r.shade(2, 81, 68, 84, 0.8); r.shade(64, 30, 68, 80, 0.8)
    r.rect(48, 22, 63, 70, OAK); r.rect(48, 22, 48, 79, EDGE); r.rect(63, 22, 63, 79, EDGE); r.rect(48, 21, 63, 21, EDGE)
    r.rect(0, 58, 63, 70, OAK); r.rect(0, 69, 63, 70, OAKD); r.rect(0, 57, 47, 57, EDGE)
    r.rect(0, 71, 63, 79, AMB); r.rect(0, 78, 63, 79, AMBD); r.rect(0, 80, 63, 80, EDGE)
    r.rect(14, 61, 26, 67, (70, 76, 86)); r.rect(16, 62, 24, 64, (140, 210, 200))
    r.rect(30, 62, 40, 66, (246, 246, 238)); r.rect(31, 63, 39, 63, (180, 180, 170))
    r.rect(51, 42, 60, 48, (150, 156, 164)); r.rect(52, 40, 59, 41, (210, 214, 220))
    for (x, y) in ((1, 34), (1, 41), (6, 37)):                                      # parcels on the blocked cell (0,2) only
        r.rect(x, y, x + 9, y + 6, (212, 160, 76)); r.rect(x, y, x + 9, y, (238, 204, 120)); r.rect(x + 4, y, x + 5, y + 6, (170, 116, 52))
    plant(r, 18, 30, (150, 110, 64), (110, 78, 44), ((160, 204, 110), (98, 150, 70), (60, 104, 50)))
    r.indexed(RP.cabinet(), RP.PALETTE, 112, 8)
    g = RP.gondola(); r.indexed(g, RP.PALETTE, 112, 56); r.indexed([row[:16] for row in g], RP.PALETTE, 160, 56)
    r.shade(66, 111, 98, 113, 0.8)
    r.rect(66, 88, 95, 110, (120, 84, 50)); r.rect(66, 88, 95, 94, (230, 200, 150)); r.rect(66, 94, 95, 94, (190, 150, 96))
    for x in (69, 80):
        r.rect(x, 82, x + 8, 90, (212, 160, 76)); r.rect(x + 2, 84, x + 6, 85, (246, 246, 238))
    r.rect(50, 114, 93, 134, (170, 116, 52)); r.rect(52, 116, 91, 132, (212, 160, 76)); r.rect(52, 123, 91, 125, (246, 232, 190))
    r.rect(0, 128, 47, 143, (0, 0, 0)); r.rect(96, 128, 175, 143, (0, 0, 0))
    r.corners()
    return r.im


# vanilla's CHECKPOINT colours and what they become
FLOOR_OLD = [(213, 205, 156), (238, 238, 172), (230, 222, 156), (246, 246, 205), (197, 180, 139)]
THEME_CP = {
    (205, 82, 65): C_TEALD, (255, 131, 115): C_TEALL, (189, 98, 74): C_TEALD, (230, 139, 98): C_TEAL, (255, 98, 49): C_TEAL,
    (230, 189, 115): (214, 226, 220), (255, 205, 90): (186, 212, 204), (246, 238, 164): (226, 220, 208), (255, 238, 197): (236, 232, 220),
    (238, 222, 164): (226, 220, 208), (246, 238, 148): (214, 226, 220), (213, 197, 106): (186, 212, 204), (172, 148, 65): (120, 150, 140),
    (189, 148, 49): (120, 150, 140), (156, 115, 90): (104, 120, 116), (156, 205, 246): (150, 196, 190), (98, 156, 238): C_TEAL,
    (172, 205, 246): (150, 196, 190), (82, 148, 197): C_TEAL, (213, 205, 156): C_JOINT, (238, 238, 172): C_FLOOR, (230, 222, 156): C_FLOOR,
    (246, 246, 205): C_FLOOR, (197, 180, 139): C_JOINT,
    # upstairs: the yellow and blue stools, and the blue link machine at the right wall
    (255, 246, 131): (236, 232, 220), (230, 180, 74): C_JOINT, (156, 213, 255): (150, 196, 190),
    (189, 230, 255): (204, 226, 218), (139, 180, 222): (120, 176, 172), (90, 131, 180): C_TEAL,
}

ESCALATOR = [0x2D0, 0x30A, 0x308, 0x2D8, 0x312, 0x310, 0x2D1, 0x30B, 0x309, 0x2D9, 0x313, 0x311,
             0x2EB, 0x31E, 0x31C, 0x2E3, 0x316, 0x314, 0x2E4, 0x317, 0x315]

BUILDINGS = {
    "checkpoint": dict(
        old="pokemon_center", symbol="gTileset_Checkpoint", dir="checkpoint",
        layouts=[("LAYOUT_POKEMON_CENTER_1F", checkpoint_1f), ("LAYOUT_POKEMON_CENTER_2F", checkpoint_2f),
                 ("LAYOUT_ONE_ISLAND_POKEMON_CENTER_2F", checkpoint_2f)],
        theme=THEME_CP,
        # reserved ids drawn as their originals recoloured; cells holding one keep it and are drawn the same way
        recoloured=ESCALATOR + [0x2DE, 0x2F9, 0x2C5],
        forced=set(ESCALATOR + [0x2DE, 0x2F9]),
        recolour_cells={"LAYOUT_POKEMON_CENTER_1F": [(x, y) for x in (0, 1) for y in (5, 6, 7)],
                        "LAYOUT_POKEMON_CENTER_2F": [(x, y) for x in (0, 1) for y in (5, 6, 7)],
                        "LAYOUT_ONE_ISLAND_POKEMON_CENTER_2F": [(x, y) for x in (0, 1) for y in (5, 6, 7)]},
        from_cells={},
        plan={"LAYOUT_POKEMON_CENTER_1F": {(14, 5): (True, 0)}},
    ),
    "repo": dict(
        old="mart", symbol="gTileset_Repo", dir="repo",
        layouts=[("LAYOUT_MART", repo)],
        theme={}, recoloured=[], forced=set(), recolour_cells={},
        from_cells={0x2BF: ("LAYOUT_MART", 1, 3), 0x2C0: ("LAYOUT_MART", 1, 4)},
        plan={"LAYOUT_MART": {(1, 6): (False, 0), (2, 6): (False, 0), (4, 5): (True, 0), (5, 5): (True, 0), (4, 6): (True, 0), (5, 6): (True, 0)}},
    ),
    # One Island's and Indigo Plateau's downstairs, each on a tileset of its own (gTileset_Checkpoint is full)
    "checkpoint_one_island": dict(
        old="pokemon_center", symbol="gTileset_CheckpointOneIsland", dir="checkpoint_one_island",
        layouts=[("LAYOUT_ONE_ISLAND_POKEMON_CENTER_1F", themed)],
        theme=THEME_CP,
        recoloured=ESCALATOR + [0x2C5, 0x35A, 0x35B, 0x35D, 0x35F],      # the network machine's screens, which the map script switches on
        forced=set(ESCALATOR),
        recolour_cells={"LAYOUT_ONE_ISLAND_POKEMON_CENTER_1F": [(x, y) for x in (0, 1) for y in (4, 5, 6)]},
        from_cells={}, plan={},
    ),
    "checkpoint_indigo": dict(
        old="pokemon_center", symbol="gTileset_CheckpointIndigo", dir="checkpoint_indigo",
        layouts=[("LAYOUT_INDIGO_PLATEAU_POKEMON_CENTER_1F", themed)],
        theme=THEME_CP,
        recoloured=ESCALATOR + [0x2C5],
        forced=set(ESCALATOR),
        recolour_cells={"LAYOUT_INDIGO_PLATEAU_POKEMON_CENTER_1F": [(x, y) for x in (0, 1) for y in (13, 14, 15)]},
        from_cells={}, plan={},
    ),    # SLATE BENCHMARK, on a tileset of its own: Brazen's dojo keeps gTileset_PewterGym
    "slate": dict(
        old="pewter_gym", symbol="gTileset_SlateBenchmark", dir="slate_benchmark",
        layouts=[("LAYOUT_PEWTER_CITY_GYM", slate)],
        theme={}, recoloured=[], forced=set(), recolour_cells={}, from_cells={}, plan={},
        tops={"LAYOUT_PEWTER_CITY_GYM": [(4, 11), (8, 11)]},
    ),    # DOLDRUM BENCHMARK, on a tileset of its own
    "doldrum": dict(
        old="cerulean_gym", symbol="gTileset_DoldrumBenchmark", dir="doldrum_benchmark",
        layouts=[("LAYOUT_CERULEAN_CITY_GYM", doldrum)],
        theme={}, recoloured=[], forced=set(), recolour_cells={}, from_cells={}, plan={},
        tops={"LAYOUT_CERULEAN_CITY_GYM": [(6, 16), (10, 16)]},
    ),    # ARDOR BENCHMARK, on a tileset of its own; the gate's three states keep their ids
    "ardor": dict(
        old="vermilion_gym", symbol="gTileset_ArdorBenchmark", dir="ardor_benchmark",
        layouts=[("LAYOUT_VERMILION_CITY_GYM", ardor)],
        theme={}, recoloured=[], forced=set(), recolour_cells={}, from_cells={}, plan={},
        states=ardor_states, tops={"LAYOUT_VERMILION_CITY_GYM": [(3, 16), (7, 16)]},
    ),    # VERDIGRIS BENCHMARK, on a tileset of its own
    "verdigris": dict(
        old="celadon_gym", symbol="gTileset_VerdigrisBenchmark", dir="verdigris_benchmark",
        layouts=[("LAYOUT_CELADON_CITY_GYM", verdigris)],
        theme={}, recoloured=[], forced=set(), recolour_cells={}, from_cells={}, plan={},
        tops={"LAYOUT_CELADON_CITY_GYM": [(4, 15), (8, 15)]},
    ),    # LURID BENCHMARK: a new maze through the plan, the pads, and the swap its map script runs when TILT loses
    "lurid": dict(
        old="fuchsia_gym", symbol="gTileset_LuridBenchmark", dir="lurid_benchmark",
        layouts=[("LAYOUT_FUCHSIA_CITY_GYM", lurid)],
        theme={}, recoloured=[], forced=set(), recolour_cells={}, from_cells={},
        plan={"LAYOUT_FUCHSIA_CITY_GYM": L_PLAN},
        swap=("LAYOUT_FUCHSIA_CITY_GYM", lambda: lurid_room(after=True), L_EXIT,
              "data/maps/FuchsiaCity_Gym/scripts.inc", "FuchsiaCity_Gym_EventScript_ShowWalls"),
    ),    # BRAZEN BENCHMARK, on a tileset of its own; the pad maze untouched
    "brazen": dict(
        old="saffron_gym", symbol="gTileset_BrazenBenchmark", dir="brazen_benchmark",
        layouts=[("LAYOUT_SAFFRON_CITY_GYM", brazen)],
        theme={}, recoloured=[], forced=set(), recolour_cells={}, from_cells={}, plan={},
        tops={"LAYOUT_SAFFRON_CITY_GYM": [(12, 19), (16, 19)]},
    ),    # QUICKSILVER BENCHMARK, on a tileset of its own; the quiz doors keep the ids their scripts set
    "quicksilver": dict(
        old="cinnabar_gym", symbol="gTileset_QuicksilverBenchmark", dir="quicksilver_benchmark",
        layouts=[("LAYOUT_CINNABAR_ISLAND_GYM", quicksilver)],
        theme={}, recoloured=[], forced=set(), recolour_cells={}, from_cells={}, plan={},
        states=quicksilver_states, tops={"LAYOUT_CINNABAR_ISLAND_GYM": [(23, 19), (27, 19)]},
    ),
}


# ---------------------------------------------------------------- palette rows fitted to the tiles
def fit_rows(tiles, rows=6, per_row=15, rounds=6):
    """Six palette rows of fifteen colours, fitted to the tiles: split the tiles into six groups by colour, give
    each group a median-cut palette of its own pixels, move every tile to the row that draws it with least error,
    and repeat. It always returns rows; the price of a tight fit is colour error, which is reported."""
    def median_cut(pixels):
        distinct = list(dict.fromkeys(pixels))
        if len(distinct) <= per_row:
            return distinct
        strip = Image.new("RGB", (len(pixels), 1)); strip.putdata(pixels)
        q = strip.quantize(colors=per_row, method=Image.Quantize.MEDIANCUT)
        pal = q.getpalette()[:per_row * 3]
        return [tuple(pal[i * 3:i * 3 + 3]) for i in range(per_row)]

    def nearest_map(pal, colours):
        return {c: min((sum((c[j] - p[j]) ** 2 for j in range(3)), n) for n, p in enumerate(pal)) for c in colours}

    colours = list({c for t in tiles for c in t})
    # start: order the tiles by their mean colour's hue and lightness, and cut the order into six groups
    def key(t):
        r, g, b = (sum(c[j] for c in t) / 64 for j in range(3))
        return (round((max(r, g, b) - min(r, g, b)) / 40), r - b, r + g + b)
    order = sorted(range(len(tiles)), key=lambda i: key(tiles[i]))
    groups = [order[i * len(order) // rows:(i + 1) * len(order) // rows] for i in range(rows)]
    pals = [median_cut([c for i in g for c in tiles[i]]) or [(0, 0, 0)] for g in groups]
    for _ in range(rounds):
        maps = [nearest_map(p, colours) for p in pals]
        assign = [[] for _ in range(rows)]
        for i, t in enumerate(tiles):
            errs = [sum(m[c][0] for c in t) for m in maps]
            assign[errs.index(min(errs))].append(i)
        pals = [median_cut([c for i in g for c in tiles[i]]) if g else p for g, p in zip(assign, pals)]
    return [list(p) for p in pals], {}, len(colours)


def hflip(t):
    return tuple(t[(i // 8) * 8 + 7 - i % 8] for i in range(64))


def vflip(t):
    return tuple(t[(7 - i // 8) * 8 + i % 8] for i in range(64))


def build(name, cfg):
    old = Old(cfg["old"])
    theme = cfg["theme"]
    art_of = {}            # (layout, x, y) -> 16x16 RGB
    attr_of, raw_of, top_of = {}, {}, {}
    canvases = {}
    for lid, draw in cfg["layouts"]:
        if LAYOUTS[lid]["secondary_tileset"] == cfg["symbol"]:        # its map.bin already holds the new ids, which
            raise SystemExit("  %s: %s is already built -- restore its map.bin and layouts.json "      # read against
                             "from git before rebuilding" % (name, lid))                                 # the old tileset
        img, raw = old.layout(lid)                                                                       # are nonsense
        canvas = draw(img, theme, raw) if draw in (checkpoint_2f, themed) else draw(img)
        l = LAYOUTS[lid]; W, H = l["width"], l["height"]
        cp = canvas.load()
        tops = set(cfg.get("tops", {}).get(lid, []))
        fp = draw(img, statues=False).load() if tops else None      # the same room with no statues: what is under a head
        for y in range(H):
            for x in range(W):
                m = raw[y][x] & 0x3FF
                if m in cfg["forced"] or (x, y) in cfg["recolour_cells"].get(lid, []):
                    pix = recolour(old.block(m), theme)
                    for yy in range(16):
                        for xx in range(16):
                            cp[x * 16 + xx, y * 16 + yy] = pix[yy][xx]
                art = tuple(cp[x * 16 + i % 16, y * 16 + i // 16] for i in range(256))
                top = None
                if (x, y) in tops:                   # a statue's head on the top layer, over the floor, as vanilla has it
                    floor = tuple(fp[x * 16 + i % 16, y * 16 + i // 16] for i in range(256))
                    top = tuple(a if a != f else MAGENTA for a, f in zip(art, floor)); art = floor
                art_of[(lid, x, y)] = art; top_of[(lid, x, y)] = top
                a = old.attr(m) & ~(7 << 29)
                r = raw[y][x]
                if (x, y) in cfg["plan"].get(lid, {}):
                    blocked, behaviour = cfg["plan"][lid][(x, y)]
                    a = (a & ~0x1FF) | behaviour
                    r = (r & 0x3FF) | ((1 << 10) if blocked else (3 << 12))
                attr_of[(lid, x, y)] = a; raw_of[(lid, x, y)] = r
        canvases[lid] = (canvas, W, H, raw)

    # reserved ids first
    reserved = {}
    for m in cfg["recoloured"]:
        pix = recolour(old.block(m), theme)
        reserved[m] = (tuple(pix[i // 16][i % 16] for i in range(256)), None, old.attr(m) & ~(7 << 29))
    for m, (lid, x, y) in cfg["from_cells"].items():
        reserved[m] = (art_of[(lid, x, y)], top_of[(lid, x, y)], old.attr(m) & ~(7 << 29))
    for m, art in (cfg["states"]() if "states" in cfg else {}).items():
        reserved[m] = (art, None, old.attr(m) & ~(7 << 29))
    ids, next_id = {v: k for k, v in reserved.items()}, 640
    cell_id = {}
    for key in art_of:
        lid, x, y = key
        m = canvases[lid][3][y][x] & 0x3FF
        k2 = (art_of[key], top_of[key], attr_of[key])
        if m in cfg["forced"]:
            cell_id[key] = m; continue
        if k2 not in ids:
            while next_id in reserved:
                next_id += 1
            ids[k2] = next_id; next_id += 1
        cell_id[key] = ids[k2]
    swaps = []
    if "swap" in cfg:                                    # a second state a map script sets, cell by cell
        slid, after, opened = cfg["swap"][:3]
        ap = after().load()
        for y in range(canvases[slid][2]):
            for x in range(canvases[slid][1]):
                key = (slid, x, y)
                was = bool((raw_of[key] >> 10) & 3)
                shut = was and (x, y) not in opened
                art = tuple(ap[x * 16 + i % 16, y * 16 + i // 16] for i in range(256))
                if art == art_of[key] and shut == was:
                    continue
                k2 = (art, top_of[key], attr_of[key])
                if k2 not in ids:
                    while next_id in reserved:
                        next_id += 1
                    ids[k2] = next_id; next_id += 1
                swaps.append((x, y, ids[k2], int(shut)))
        print("  %s: %d cells change when the script runs" % (name, len(swaps)))
    blocks = {v: k for k, v in ids.items()}
    for m, v in reserved.items():
        blocks[m] = v
    nblocks = max(blocks) - 639
    print("  %s: %d blocks (ids to %d, of 384)" % (name, len(blocks), nblocks))

    # tiles
    quads = {}                                           # (block, entry 0..3 bottom, 4..7 top) -> 64 pixels
    for m, (art, top, a) in blocks.items():
        for layer, pix in ((0, art), (1, top)):
            if pix is None:
                continue
            for q in range(4):
                x0, y0 = (q % 2) * 8, (q // 2) * 8
                t = tuple(pix[(y0 + i // 8) * 16 + x0 + i % 8] for i in range(64))
                if layer and all(c == MAGENTA for c in t):
                    continue                             # an empty top tile is entry 0, as in vanilla
                quads[(m, layer * 4 + q)] = t
    uniq = list(set(quads.values()))
    rows, near, k = fit_rows([[c for c in t if c != MAGENTA] or [(0, 0, 0)] for t in uniq])
    row_pals = [[(255, 0, 255)] + r + [(0, 0, 0)] * (15 - len(r)) for r in rows]
    tiles, tile_list, entry = {}, [], {}
    err_total = 0
    for (m, q), px in quads.items():
        best = None
        for ri, pal in enumerate(row_pals):
            idx, err = [], 0
            for c in px:
                if c == MAGENTA:
                    idx.append(0); continue
                c2 = near.get(c, c)
                j, e = min(((j, sum((c2[t] - pal[j][t]) ** 2 for t in range(3))) for j in range(1, len(rows[ri]) + 1)), key=lambda z: z[1])
                idx.append(j); err += e
            if best is None or err < best[1]:
                best = (ri, err, tuple(idx))
        ri, err, idx = best; err_total += err
        ref = None
        for flip, f in ((0, lambda t: t), (0x400, hflip), (0x800, vflip), (0xC00, lambda t: hflip(vflip(t)))):
            t = f(idx)
            if t in tiles:
                ref = (tiles[t], flip); break
        if ref is None:
            tiles[idx] = len(tile_list); tile_list.append(idx); ref = (tiles[idx], 0)
        entry[(m, q)] = (640 + ref[0]) | ref[1] | ((7 + ri) << 12)
    print("  %s: %d tiles (of 384), %d palette rows from %d colours, mean squared error %.1f" %
          (name, len(tile_list), len(rows), k, err_total / (len(quads) * 64)))
    ok = len(tile_list) <= 384 and nblocks <= 384

    # preview: each layout, the game's render of what was built
    shots = []
    for lid, (canvas, W, H, raw) in canvases.items():
        out = Image.new("RGB", (W * 16, H * 16)); o = out.load()
        for y in range(H):
            for x in range(W):
                m = cell_id[(lid, x, y)]
                for q in range(8):
                    if (m, q) not in entry:
                        continue
                    t = entry[(m, q)]; idx = tile_list[(t & 0x3FF) - 640]; pal = row_pals[((t >> 12) & 15) - 7]
                    for i in range(64):
                        if q >= 4 and idx[i] == 0:
                            continue
                        tx, ty = i % 8, i // 8
                        if t & 0x400: tx = 7 - tx
                        if t & 0x800: ty = 7 - ty
                        o[x * 16 + (q % 4 % 2) * 8 + tx, y * 16 + (q % 4 // 2) * 8 + ty] = pal[idx[i]]
        old_img, _ = old.layout(lid)
        pair = Image.new("RGB", (W * 32 + 8, H * 16), (30, 30, 30)); pair.paste(old_img, (0, 0)); pair.paste(out, (W * 16 + 8, 0))
        shots.append(pair)
    sheet = Image.new("RGB", (max(s.width for s in shots), sum(s.height + 8 for s in shots)), (30, 30, 30)); y = 0
    for s in shots:
        sheet.paste(s, (0, y)); y += s.height + 8
    path = "/tmp/interior_%s.png" % name
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(path)
    print("  %s: preview %s" % (name, path))
    if not ok:
        raise SystemExit("  %s does not fit" % name)
    if not WRITE:
        return

    d = os.path.join(GBA, "data/tilesets/secondary", cfg["dir"]); os.makedirs(os.path.join(d, "palettes"), exist_ok=True)
    img = Image.new("P", (128, ((len(tile_list) + 15) // 16) * 8)); img.putpalette(sum(([v * 17] * 3 for v in range(16)), []) + [0] * 720)
    ip = img.load()
    for n, t in enumerate(tile_list):
        for i, v in enumerate(t):
            ip[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] = v
    img.save(os.path.join(d, "tiles.png"))
    meta, attrs = bytearray(nblocks * 16), bytearray(nblocks * 4)
    for m, (art, top, a) in blocks.items():
        struct.pack_into("<8H", meta, (m - 640) * 16, *[entry.get((m, q), 0) for q in range(8)])
        struct.pack_into("<I", attrs, (m - 640) * 4, a)
    open(os.path.join(d, "metatiles.bin"), "wb").write(meta)
    open(os.path.join(d, "metatile_attributes.bin"), "wb").write(attrs)
    olddir = os.path.join(GBA, "data/tilesets/secondary", cfg["old"])
    for r in range(16):
        write_pal(os.path.join(d, "palettes/%02d.pal" % r), row_pals[r - 7] if 7 <= r < 7 + len(row_pals) else read_pal(os.path.join(olddir, "palettes/%02d.pal" % r)))
    for lid, (canvas, W, H, raw) in canvases.items():
        l = LAYOUTS[lid]; bd = bytearray(W * H * 2)
        for y in range(H):
            for x in range(W):
                struct.pack_into("<H", bd, (y * W + x) * 2, (raw_of[(lid, x, y)] & ~0x3FF) | cell_id[(lid, x, y)])
        open(os.path.join(GBA, l["blockdata_filepath"]), "wb").write(bd)
    # register the tileset and point the layouts at it
    lj_path = os.path.join(GBA, "data/layouts/layouts.json"); lj = open(lj_path).read()
    for lid, _ in cfg["layouts"]:
        lj = re.sub(r'("id": "%s",(?:[^{}]*?)"secondary_tileset": )"gTileset_\w+"' % re.escape(lid), r'\1"%s"' % cfg["symbol"], lj, flags=re.S)
    open(lj_path, "w").write(lj)
    stem = cfg["symbol"][len("gTileset_"):]
    rules_path = os.path.join(GBA, "tileset_rules.mk"); rules = open(rules_path).read()
    key = "$(TILESETGFXDIR)/secondary/%s/tiles.4bpp: %%.4bpp: %%.png\n\t$(GFX) $< $@ -num_tiles " % cfg["dir"]
    if key in rules:
        at = rules.index(key) + len(key); oldn = rules[at:].split()[0]
        rules = rules[:at] + str(len(tile_list)) + rules[at + len(oldn):]
    else:
        rules += "\n%s%d -Wnum_tiles\n" % (key, len(tile_list))
    open(rules_path, "w").write(rules)

    def add_once(path, marker, block):
        s = open(path).read()
        if marker not in s:
            open(path, "w").write(s + ("" if s.endswith("\n") else "\n") + block)
    add_once(os.path.join(GBA, "src/data/tilesets/graphics.h"), "gTilesetTiles_%s[]" % stem,
             "// T-103: %s, a tileset of its own (tools/gbainterior.py).\nconst u32 gTilesetTiles_%s[] = INCBIN_U32(\"data/tilesets/secondary/%s/tiles.4bpp.lz\");\n\n"
             "const u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n" % (stem, stem, cfg["dir"], stem,
             "".join("\tINCBIN_U16(\"data/tilesets/secondary/%s/palettes/%02d.gbapal\"),\n" % (cfg["dir"], k) for k in range(16))))
    add_once(os.path.join(GBA, "src/data/tilesets/metatiles.h"), "gMetatiles_%s[]" % stem,
             "const u16 gMetatiles_%s[] = INCBIN_U16(\"data/tilesets/secondary/%s/metatiles.bin\");\n"
             "const u32 gMetatileAttributes_%s[] = INCBIN_U32(\"data/tilesets/secondary/%s/metatile_attributes.bin\");\n" % (stem, cfg["dir"], stem, cfg["dir"]))
    add_once(os.path.join(GBA, "src/data/tilesets/headers.h"), "gTileset_%s =" % stem,
             "// T-103: %s, rethemed and replanned.\nconst struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
             "    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n"
             "    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = NULL,\n};\n" % (stem, stem, stem, stem, stem, stem))
    if swaps:                                            # the script's half: one setmetatile per changed cell
        inc_path, label = os.path.join(GBA, cfg["swap"][3]), cfg["swap"][4]
        begin, end = "@ generated by DAEMONS tools/gbainterior.py %s -- do not edit by hand\n" % name, "@ end of generated %s\n" % name
        body = begin + "%s::\n" % label + "".join("\tsetmetatile %d, %d, 0x%X, %d\n" % sw for sw in swaps) + "\treturn\n" + end
        text = open(inc_path).read()
        if begin in text:
            text = text[:text.index(begin)] + body + text[text.index(end) + len(end):]
        else:
            text = text + ("" if text.endswith("\n") else "\n") + "\n" + body
        open(inc_path, "w").write(text)
    print("  %s: written %s, %d layouts, registered" % (name, os.path.relpath(d, GBA), len(cfg["layouts"])))


def main():
    for name, cfg in BUILDINGS.items():
        if not ONLY or name in ONLY:
            build(name, cfg)


if __name__ == "__main__":
    main()

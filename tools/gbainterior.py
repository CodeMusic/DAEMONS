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

WHY A TILESET EACH. `gTileset_PokemonCenter` also draws One Island's and Indigo
Plateau's CHECKPOINTs, which are shaped differently; those stay on it for now
(T-103), and One Island's upstairs, which is identical to Kanto's, moves over.
`gTileset_Mart` keeps the unused Lavaridge and RS layouts.

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


def checkpoint_2f(old_img, theme):
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
    attr_of, raw_of = {}, {}
    canvases = {}
    for lid, draw in cfg["layouts"]:
        img, raw = old.layout(lid)
        canvas = draw(img, theme) if draw is checkpoint_2f else draw(img)
        l = LAYOUTS[lid]; W, H = l["width"], l["height"]
        cp = canvas.load()
        for y in range(H):
            for x in range(W):
                m = raw[y][x] & 0x3FF
                if m in cfg["forced"] or (x, y) in cfg["recolour_cells"].get(lid, []):
                    pix = recolour(old.block(m), theme)
                    for yy in range(16):
                        for xx in range(16):
                            cp[x * 16 + xx, y * 16 + yy] = pix[yy][xx]
                art_of[(lid, x, y)] = tuple(cp[x * 16 + i % 16, y * 16 + i // 16] for i in range(256))
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
        reserved[m] = (tuple(pix[i // 16][i % 16] for i in range(256)), old.attr(m) & ~(7 << 29))
    for m, (lid, x, y) in cfg["from_cells"].items():
        reserved[m] = (art_of[(lid, x, y)], old.attr(m) & ~(7 << 29))
    ids, next_id = {v: k for k, v in reserved.items()}, 640
    cell_id = {}
    for key in art_of:
        lid, x, y = key
        m = canvases[lid][3][y][x] & 0x3FF
        k2 = (art_of[key], attr_of[key])
        if m in cfg["forced"]:
            cell_id[key] = m; continue
        if k2 not in ids:
            while next_id in reserved:
                next_id += 1
            ids[k2] = next_id; next_id += 1
        cell_id[key] = ids[k2]
    blocks = {v: k for k, v in ids.items()}
    for m, (art, a) in reserved.items():
        blocks[m] = (art, a)
    nblocks = max(blocks) - 639
    print("  %s: %d blocks (ids to %d, of 384)" % (name, len(blocks), nblocks))

    # tiles
    quads = {}
    for m, (art, a) in blocks.items():
        for q in range(4):
            x0, y0 = (q % 2) * 8, (q // 2) * 8
            quads[(m, q)] = tuple(art[(y0 + i // 8) * 16 + x0 + i % 8] for i in range(64))
    uniq = list(set(quads.values()))
    rows, near, k = fit_rows(uniq)
    row_pals = [[(255, 0, 255)] + r + [(0, 0, 0)] * (15 - len(r)) for r in rows]
    tiles, tile_list, entry = {}, [], {}
    err_total = 0
    for (m, q), px in quads.items():
        best = None
        for ri, pal in enumerate(row_pals):
            idx, err = [], 0
            for c in px:
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
                for q in range(4):
                    t = entry[(m, q)]; idx = tile_list[(t & 0x3FF) - 640]; pal = row_pals[((t >> 12) & 15) - 7]
                    for i in range(64):
                        tx, ty = i % 8, i // 8
                        if t & 0x400: tx = 7 - tx
                        if t & 0x800: ty = 7 - ty
                        o[x * 16 + (q % 2) * 8 + tx, y * 16 + (q // 2) * 8 + ty] = pal[idx[i]]
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
    for m, (art, a) in blocks.items():
        struct.pack_into("<8H", meta, (m - 640) * 16, *[entry[(m, q)] for q in range(4)], 0, 0, 0, 0)
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
    print("  %s: written %s, %d layouts, registered" % (name, os.path.relpath(d, GBA), len(cfg["layouts"])))


def main():
    for name, cfg in BUILDINGS.items():
        if not ONLY or name in ONLY:
            build(name, cfg)


if __name__ == "__main__":
    main()

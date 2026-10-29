#!/usr/bin/env python3
"""The TOWN MAP / GOTO map in SCORE: paper and ink, staff-line terrain, beamed routes, noteheads (T-449).

    python3 tools/gbaregionmap.py                     # report: tile and colour budgets, and whether the engine's
                                                      #   files are what this would write
    python3 tools/gbaregionmap.py --draft [DIR]       # the review sheets (today | built), the sea's and the opening's
                                                      #   GIFs, into DIR (default: the preview directory)
    python3 tools/gbaregionmap.py --write --approved  # into the engine (approved by the user 2026-10-24, direction A).
                                                      #   Without --approved it refuses.

WHAT IT READS. Only VANILLA's region map (`git show upstream/master:graphics/region_map/...`) and our cursor grid
(src/data/region_map/region_map_layout_*.h). Never the files it writes, so a second run writes the same bytes.

SAME SHAPE (the user, 2026-10-24: "similar shape so it matches normal navigation from it"). Every page is rebuilt
from vanilla's, pixel class by pixel class: what was sea stays sea, what was land stays land at the same height, and
the routes and towns are re-derived from the cursor grid's own cells, so every town, route and island cell sits
exactly where the cursor expects it. The draft this grew from is DAEMONS f780ddb9 (gfx/drafts/t449, direction A).

THE PAGE (BG0): paper land, its height drawn as staff lines (the higher, the more of the five); an ink coast; routes
beamed, with a barline at each cell (a cell is a measure); towns are noteheads; bridges dotted; the sea lanes only
TRAVERSE crosses in FLOW's blue, the one hue on the map. The sea is a dark slate under the paper, lifted from the
draft's grey so the islands and the coast read at 1x and under T-317's 2x2 mosaic.

THE SEA (palette row 5, new): every 8x8 tile that is wholly open sea moves to row 5 and may carry a glyph -- a 0, a
1, or a note -- drawn as two shapes (A and B) in one of four groups. src/region_map.c's Task_RegionMapSea cycles the
twelve glyph colours, each group on its own period, so the sea shuffles between bits and notes with no tile ever
changing. A tile that mixes coast and water cannot use row 5 (it needs the land's colours), so the shore is calm and
the shuffle starts one tile out. The task writes the unfaded buffer (and the faded one only while it is settled), so
every fade still works. Its colours are graphics/region_map/sea.pal; entry 15 is the glyphs' ink, 1 the water.

THE FRAME, redrawn whole: the side panels as two closed covers of a score (ink, a vertical staff, a barline every
16px, a paper rule on the inner edge), in map_edge.png/.bin (the TOWN MAP's BG1), the six slide-open edge sprites
(cut from the same two columns, so the hand-off from sprites to BG1 does not move a pixel), background.png/.bin (the
GOTO map's BG1), the top strip (top_bar.pal's 15, the backdrop, now ink), the page margins and the switch-map buttons
re-inked. Rows 1, 2 and 4 hold the frame's colours; row 2 is stored a shade light, because TintMapEdgesPalette
darkens it to 95% for BG1 and the sprites use the frame's colours undarkened.

FIXED SLOTS the engine names by number, kept: BG0 tile 0 (blank), 3 (the calm sea src/region_map.c fills over NAVEL
ROCK and BIRTH ISLAND until they are found), 0xF0-0xF2 and 0x100-0x132 (the switch buttons); BG1 map_edge tiles 2, 3,
0x3D, 0x3E, 0x3F (the top strip's rule, drawn by Task_MapOpenAnim). switch_map_menu.png is recoloured by role, since
its cells draw with rows 0 and 3.
"""
import io, os, re, struct, sys, hashlib
from collections import Counter, deque
from PIL import Image, ImageDraw, ImageFont
import daemonslib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
G = os.path.join(GBA, "graphics/region_map")
L = os.path.join(GBA, "src/data/region_map")
ARGS = sys.argv[1:]
WRITE = "--write" in ARGS
DRAFT = "--draft" in ARGS
PAGES = ["kanto", "sevii_123", "sevii_45", "sevii_67"]
HDR = {p: "region_map_layout_%s.h" % p for p in PAGES}

FLOW = (112, 160, 232)     # FLOW's blue, lifted to read on the slate sea; TRAVERSE is FLOW's routine
INK, INK2, STAFF, BAR = (30, 26, 36), (46, 40, 54), (92, 84, 100), (110, 100, 112)
GREY, PAPERD, PAPER2, PAPER, LIGHT = (150, 142, 128), (192, 178, 148), (226, 216, 192), (238, 230, 210), (248, 244, 234)
SEA, SEATEX, GLYPH = (70, 82, 108), (63, 74, 99), (150, 164, 190)

# ---------------------------------------------------------------------------------------------------- vanilla
def vbytes(f):
    return daemonslib.upstream(GBA, "graphics/region_map/" + f, binary=True)


def vjasc(f):
    L_ = vbytes(f).decode().replace("\r", "").split("\n")
    return [tuple(map(int, l.split())) for l in L_[3:3 + int(L_[2])]]


def vtiles(f):
    im = Image.open(io.BytesIO(vbytes(f))); w, h = im.size; px = im.load()
    return [[[px[tx * 8 + x, ty * 8 + y] & 15 for x in range(8)] for y in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]


def vbin(f):
    d = vbytes(f)
    return [struct.unpack_from("<H", d, i * 2)[0] for i in range(len(d) // 2)]


VPAL = vjasc("region_map.pal")
VTILES = vtiles("region_map.png")


def vidx(page):
    """(row, index) per pixel of vanilla's BG0 page, None where transparent."""
    out = [[None] * 240 for _ in range(160)]
    for i, e in enumerate(vbin(page + ".bin")[:600]):
        t, hf, vf, p = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
        for y in range(8):
            for x in range(8):
                c = VTILES[t][7 - y if vf else y][7 - x if hf else x]
                if c:
                    out[(i // 30) * 8 + y][(i % 30) * 8 + x] = (p, c)
    return out


SEA_, SEAROUTE, LAND, ROUTE, PALE, TOWN, UI, WHITE, NONE = range(9)


def classify(pi):
    if pi is None: return NONE, 0
    r, c = pi
    if r == 0:
        if 1 <= c <= 5: return LAND, c
        if 6 <= c <= 9: return ROUTE, 0
        if c in (10, 11): return PALE, 0
        if c in (12, 13): return SEAROUTE, 0
        return SEA_, 0
    if r == 1: return (TOWN if 6 <= c <= 11 else ROUTE), 0
    if r == 2: return WHITE, 0
    if r == 3: return (SEA_ if c >= 14 else UI), 0
    return UI, 0


def layout(page):
    s = open(os.path.join(L, HDR[page])).read()
    body = s[s.index("[LAYER_MAP]"):s.index("[LAYER_DUNGEON]")]
    rows = re.findall(r"\{([^{}]*)\}", body)
    return [[t.strip() for t in r.split(",") if t.strip()] for r in rows][:15]


def analyse(page):
    """as the draft: the ground under every pixel, the cursor cells that are towns or routes, and the links."""
    idx = vidx(page)
    cls = [[classify(idx[y][x]) for x in range(240)] for y in range(160)]
    base = [[None] * 240 for _ in range(160)]

    def fill(seeds, into):
        q = deque(seeds)
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if 0 <= X < 240 and 0 <= Y < 160 and base[Y][X] is None and cls[Y][X][0] in into:
                    base[Y][X] = base[y][x]; q.append((X, Y))
    land = []
    for y in range(160):
        for x in range(240):
            k, lv = cls[y][x]
            if k == LAND: base[y][x] = ("L", lv); land.append((x, y))
            elif k in (SEA_, SEAROUTE): base[y][x] = ("S", 0)
    fill(land, (ROUTE, TOWN))
    for y in range(160):
        for x in range(240):
            if cls[y][x][0] in (ROUTE, TOWN) and base[y][x] is None: base[y][x] = ("L", 2)
    fill([(x, y) for y in range(160) for x in range(240) if base[y][x]], (PALE,))
    lay = layout(page)
    towncells, seen = set(), set()
    for y in range(160):
        for x in range(240):
            if cls[y][x][0] == TOWN and (x, y) not in seen:
                blob = []; q2 = deque([(x, y)]); seen.add((x, y))
                while q2:
                    a, b = q2.popleft(); blob.append((a, b))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        X, Y = a + dx, b + dy
                        if 0 <= X < 240 and 0 <= Y < 160 and (X, Y) not in seen and cls[Y][X][0] == TOWN:
                            seen.add((X, Y)); q2.append((X, Y))
                if len(blob) < 12: continue
                mx = sum(a for a, _ in blob) / len(blob); my = sum(b for _, b in blob) / len(blob)
                cands = []
                for cy in range(15):
                    for cx in range(22):
                        sec = lay[cy][cx]
                        if sec == "MAPSEC_NONE": continue
                        d2 = (8 * (cx + 4) + 3.5 - mx) ** 2 + (8 * (cy + 4) + 3.5 - my) ** 2
                        if d2 <= 100: cands.append((re.match(r"MAPSEC_ROUTE_\d+$", sec) is not None, d2, (cx, cy)))
                if cands: towncells.add(min(cands)[2])
    cells = {}
    for cy in range(15):
        for cx in range(22):
            if lay[cy][cx] == "MAPSEC_NONE": continue
            px_, py_ = 8 * (cx + 4) + 4, 8 * (cy + 4) + 4
            box = [cls[py_ + dy][px_ + dx][0] for dy in range(-3, 4) for dx in range(-3, 4)]
            kinds = Counter(k for k in box if k in (ROUTE, PALE, SEAROUTE))
            if (cx, cy) in towncells or kinds:
                cells[(cx, cy)] = dict(sec=lay[cy][cx], town=(cx, cy) in towncells,
                                       kind=(kinds.most_common(1)[0][0] if kinds else ROUTE))
    links = []
    for (cx, cy), c in cells.items():
        for dx, dy in ((1, 0), (0, 1)):
            n = (cx + dx, cy + dy)
            if n not in cells: continue
            ax, ay = 8 * (cx + 4) + 4, 8 * (cy + 4) + 4
            ks = [cls[ay + dy * i][ax + dx * i][0] for i in range(9)]
            if sum(k in (ROUTE, PALE, SEAROUTE, TOWN) for k in ks) >= 7:
                kc = Counter(k for k in ks if k in (ROUTE, PALE, SEAROUTE))
                links.append(((cx, cy), n, kc.most_common(1)[0][0] if kc else ROUTE))
    return dict(idx=idx, cls=cls, base=base, cells=cells, links=links, bin=vbin(page + ".bin")[:600])


# ---------------------------------------------------------------------------------------------------- palettes
# Row 0, the page: 1..4 paper by height, 5 a staff line, 6 coast, 7 calm sea, 8 its texture, 9 route, 10 barline,
# 11 bridge, 12 TRAVERSE lane, 13 notehead, 14 paper light (the margins, the notehead's shine), 15 unused
I_L1, I_L2, I_L3, I_L4, I_TEX, I_COAST, I_SEA, I_SEATEX, I_RT, I_RTL, I_PALE, I_LANE, I_TOWN, I_LIGHT = range(1, 15)
ROW0 = [(0, 0, 0), PAPER, PAPER2, (210, 198, 170), PAPERD, (176, 164, 136), (44, 38, 52), SEA, SEATEX,
        (44, 38, 52), BAR, (214, 206, 190), FLOW, INK, LIGHT, LIGHT]
# Row 3, the switch buttons (and the switch menu's frames): ink to light, the lane, the sea
R3_INK, R3_MID, R3_PAPERD, R3_PAPER, R3_LIGHT, R3_LANE = range(1, 7)
ROW3 = [(0, 0, 0), INK, BAR, PAPERD, PAPER, LIGHT, FLOW] + [INK] * 7 + [SEA, SEATEX]
# The frame's colours (rows 1, 2 and 4, map_edge.png and the edge sprites)
F_INK, F_INK2, F_STAFF, F_BAR, F_GREY, F_PAPERD, F_PAPER, F_LIGHT = range(1, 9)
FRAME = [(0, 0, 0), INK, INK2, STAFF, BAR, GREY, PAPERD, PAPER, LIGHT] + [INK] * 6 + [LIGHT]
F_WHITE = 15          # row 2's 15 is not darkened by TintMapEdgesPalette: the opening's white page, the margins
# Row 5, the open sea: 1 water, 2 its texture, 3..14 four groups of {A, B, both}, 15 the glyphs' ink
def SEA_A(g): return 3 + 3 * g
def SEA_B(g): return 4 + 3 * g
def SEA_AB(g): return 5 + 3 * g


#  The cycle, as src/region_map.c's Task_RegionMapSea runs it: each group steps through its eight states (0 nothing,
#  1 shape A, 2 shape B) on its own period, so no two groups turn together. KEEP IN STEP with sSeaSteps/sSeaPeriods.
SEA_STEPS = [[1, 1, 0, 2, 2, 0, 1, 2], [2, 0, 1, 1, 0, 2, 2, 1], [0, 1, 2, 0, 1, 1, 2, 0], [1, 2, 2, 0, 0, 1, 0, 2]]
SEA_PERIODS = [18, 26, 22, 30]


def sea_row(frame):
    """row 5 after `frame` frames of the task (0: as sea.pal stores it)"""
    pal = [(0, 0, 0), SEA, SEATEX] + [SEA] * 12 + [GLYPH]
    for g in range(4):
        s = SEA_STEPS[g][(frame // SEA_PERIODS[g]) % 8]
        pal[SEA_A(g)] = GLYPH if s == 1 else SEA
        pal[SEA_B(g)] = GLYPH if s == 2 else SEA
        pal[SEA_AB(g)] = GLYPH if s else SEA
    return pal


def gba5(c):
    return tuple(v >> 3 for v in c)


def darken95(c5):
    return tuple((((v << 8) // 100) * 95) >> 8 for v in c5)


def lighten_for_tint(c):
    """a colour that TintMapEdgesPalette's 95% brings back to c (in the GBA's five bits), so BG1 and the sprites match"""
    want = gba5(c)
    out = []
    for i, w in enumerate(want):
        best = min(range(32), key=lambda s: (abs(darken95((s, s, s))[0] - w), s))
        out.append(best * 8)
    return tuple(out)


ROW2 = [FRAME[0]] + [lighten_for_tint(c) for c in FRAME[1:15]] + [FRAME[15]]


# ---------------------------------------------------------------------------------------------------- the page
def h(*a):
    return int(hashlib.md5(repr(a).encode()).hexdigest()[:8], 16)


def glyph(rows, dx=0, dy=0):
    return frozenset((x + dx, y + dy) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch == "#")


ZERO = ["###", "#.#", "#.#", "#.#", "###"]
ONE = [".#.", "##.", ".#.", ".#.", "###"]
NOTE_LO = ["..#", "..#", "..#", "###", "##."]
NOTE_HI = ["..#", "..##", "..#", "###", "##."]
#  (A, B): the shapes a tile shows in turn -- a bit becomes the other bit or a note, a note steps up or turns to a bit
SEA_GLYPHS = []
for dx, dy in ((1, 1), (4, 2)):
    SEA_GLYPHS += [(glyph(ZERO, dx, dy), glyph(ONE, dx, dy)), (glyph(ONE, dx, dy), glyph(NOTE_LO, dx, dy)),
                   (glyph(NOTE_LO, dx, dy + 1), glyph(NOTE_HI, dx, dy)), (glyph(NOTE_HI, dx, dy), glyph(ZERO, dx, dy))]


def land_px(x, y, lv):
    """elevation as a staff: the higher the ground, the more of the five lines (every other pixel row of a tile)"""
    lines = {1: (), 2: (), 3: (2,), 4: (2, 6), 5: (0, 2, 4, 6)}[lv]
    if lv >= 3 and (y % 8) in lines:
        return I_TEX
    return [I_L1, I_L1, I_L2, I_L3, I_L4][lv - 1]


def calm_px(x, y):
    """the calm sea's texture: two short ripples a tile, the same in every tile (so tile 3 is any calm tile)"""
    return I_SEATEX if (x % 8, y % 8) in ((2, 2), (3, 2), (6, 6), (7, 6)) else I_SEA


def put(img, x, y, i):
    if 24 <= x < 216 and 16 <= y < 160:
        img[y][x] = (0, i)


def draw_route(img, a, b, kind):
    ax, ay = 8 * (a[0] + 4) + 4, 8 * (a[1] + 4) + 4
    horiz = ay == 8 * (b[1] + 4) + 4
    for i in range(9):
        x, y = (ax + i, ay) if horiz else (ax, ay + i)
        if kind == SEAROUTE:
            if i % 3 != 2:
                put(img, x, y, I_LANE); put(img, x + (0 if horiz else 1), y + (1 if horiz else 0), I_LANE)
        elif kind == PALE:
            if i % 2 == 0:
                put(img, x, y, I_PALE)
        else:
            put(img, x, y, I_RT); put(img, x + (0 if horiz else 1), y + (1 if horiz else 0), I_RT)
    if kind == ROUTE:   # a barline at the cell boundary: a cell is a measure
        mx, my = (ax + 4, ay) if horiz else (ax, ay + 4)
        for k in (-2, -1, 2, 3):
            put(img, mx + (0 if horiz else k), my + (k if horiz else 0), I_RTL)


def draw_town(img, cx, cy):
    x0, y0 = 8 * (cx + 4) + 1, 8 * (cy + 4) + 1
    head = ["..###..", ".#####.", "#######", "#######", ".#####.", "..###.."]
    for y, r in enumerate(head):
        for x, ch in enumerate(r):
            if ch == "#": put(img, x0 + x, y0 + y, I_TOWN)
    put(img, x0 + 2, y0 + 1, I_LIGHT); put(img, x0 + 3, y0 + 1, I_LIGHT)


def compose(page, A):
    """the page as 240x160 (row, index); rows 0 and 1 of tiles, the margins and the buttons are placed by cell"""
    cls, base = A["cls"], A["base"]
    img = [[None] * 240 for _ in range(160)]
    for y in range(16, 160):
        for x in range(24, 216):
            k, _ = cls[y][x]
            b = base[y][x]
            if b is None:
                b = ("S", 0)
            img[y][x] = (0, land_px(x, y, max(1, b[1])) if b[0] == "L" else calm_px(x, y))
    for y in range(16, 160):
        for x in range(24, 216):
            b = base[y][x]
            if not b or b[0] != "L": continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if 24 <= X < 216 and 16 <= Y < 160 and base[Y][X] and base[Y][X][0] == "S":
                    img[y][x] = (0, I_COAST); break
    for a, b, kind in A["links"]:
        draw_route(img, a, b, kind)
    for (cx, cy), c in A["cells"].items():
        if c["town"]:
            draw_town(img, cx, cy)
    # the open sea: a tile that is all calm water moves to row 5, and one in three carries a glyph
    for ty in range(2, 20):
        for tx in range(3, 27):
            pts = [img[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8)]
            if not all(p and p[0] == 0 and p[1] in (I_SEA, I_SEATEX) for p in pts):
                continue
            for y in range(8):
                for x in range(8):
                    img[ty * 8 + y][tx * 8 + x] = (5, 2 if img[ty * 8 + y][tx * 8 + x][1] == I_SEATEX else 1)
            v = h(page, tx, ty, "v") % (len(SEA_GLYPHS) * 2)
            g = h(page, tx, ty, "g") % 4
            if v < len(SEA_GLYPHS):
                ga, gb = SEA_GLYPHS[v]
                for (x, y) in ga | gb:
                    img[ty * 8 + y][tx * 8 + x] = (5, SEA_AB(g) if (x, y) in ga and (x, y) in gb
                                                   else SEA_A(g) if (x, y) in ga else SEA_B(g))
    return img


def margin_tile(right):
    """the page's margin (BG0 columns 2 and 27): paper light, a staff-grey rule a pixel in from the frame"""
    t = [[I_LIGHT] * 8 for _ in range(8)]
    for y in range(8):
        t[y][6 if right else 1] = I_RTL
    return t


# ---------------------------------------------------------------------------------------------------- tiles
def flips(t):
    return [(t, 0, 0), ([r[::-1] for r in t], 1, 0), (t[::-1], 0, 1), ([r[::-1] for r in t[::-1]], 1, 1)]


class TileSet:
    def __init__(self, n, fixed):
        self.slots = [None] * n
        self.index = {}
        for i, t in fixed.items():
            self.slots[i] = t
            self.index.setdefault(self.key(t), i)
        self.free = [i for i in range(n) if self.slots[i] is None]

    @staticmethod
    def key(t):
        return tuple(tuple(r) for r in t)

    def add(self, t):
        """(slot, hflip, vflip)"""
        for ft, hf, vf in flips(t):
            k = self.key(ft)
            if k in self.index:
                return self.index[k], hf, vf
        if not self.free:
            raise SystemExit("  !! out of tile slots")
        i = self.free.pop(0)
        self.slots[i] = t
        self.index[self.key(t)] = i
        return i, 0, 0

    def used(self):
        return max(i for i, t in enumerate(self.slots) if t is not None) + 1


BLANK = [[0] * 8 for _ in range(8)]
CALM = [[calm_px(x, y) for x in range(8)] for y in range(8)]
BUTTONS = [0xF0 + i for i in range(3)] + [b + i for b in (0x100, 0x110, 0x120, 0x130) for i in range(3)]


def reink3(c):
    """a vanilla row-3 colour, by its lightness, to the button's ink and paper"""
    lum = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    return R3_INK if lum < 110 else R3_MID if lum < 150 else R3_PAPERD if lum < 185 else R3_PAPER if lum < 230 else R3_LIGHT


def button_tile(n):
    t = VTILES[n]
    out = [[0] * 8 for _ in range(8)]
    for y in range(8):
        for x in range(8):
            v = t[y][x]
            if v in (14, 15):   # vanilla's striped sea behind the buttons -> our calm sea
                out[y][x] = 14 if calm_px(x, y) == I_SEA else 15
            elif v:
                out[y][x] = reink3(VPAL[48 + v])
    return out


def build_bg0(analyses):
    fixed = {0: BLANK, 3: CALM}
    for n in BUTTONS:
        fixed[n] = button_tile(n)
    ts = TileSet(512, fixed)
    bins, imgs = {}, {}
    margins = {False: ts.add(margin_tile(False)), True: ts.add(margin_tile(True))}
    for p in PAGES:
        A = analyses[p]
        img = compose(p, A)
        imgs[p] = img
        out = []
        for i, ve in enumerate(A["bin"]):
            tx, ty = i % 30, i // 30
            if ve >> 12 == 3:          # a switch button: vanilla's own slot, re-inked
                out.append(ve); continue
            if ty < 2 or tx < 2 or tx > 27:
                out.append(0); continue
            if tx in (2, 27):
                s, hf, vf = margins[tx == 27]
                out.append(s | hf << 10 | vf << 11); continue
            pix = [img[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8)]
            rows = {q[0] for q in pix}
            assert len(rows) == 1, (p, tx, ty, rows)
            row = rows.pop()
            t = [[pix[y * 8 + x][1] for x in range(8)] for y in range(8)]
            s, hf, vf = ts.add(t)
            out.append(s | hf << 10 | vf << 11 | row << 12)
        bins[p] = out
    return ts, bins, imgs


# ---------------------------------------------------------------------------------------------------- the frame
def column(right):
    """one side of the closed score, 32x192: the edge sprites' column (screen y 8..199); BG1's side panel is its inner
    half. Its top eight rows are the top strip's own ink and rule, so the sprites hand over to BG1 without a seam."""
    W, H = 32, 192
    c = [[F_INK] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if y < 8:
                c[y][x] = F_PAPER if y == 7 else F_INK
                continue
            if x == 31: c[y][x] = F_PAPER                  # the inner edge (screen x 15 when open)
            elif x == 0: c[y][x] = F_BAR                   # the outer edge, seen only while it is closed
            elif x in (19, 21, 23, 25, 27) or x in (4, 6, 8, 10, 12):
                c[y][x] = F_STAFF
            if y % 16 == 0 and (18 <= x <= 28 or 3 <= x <= 13):
                c[y][x] = F_BAR                            # a barline every 16px (screen y = 8 mod 16)
    # a clef's dot pair and a double bar on the outer half: what the closed score shows on its spine
    for y in (88, 89, 100, 101):
        for x in (7, 8):
            c[y][x] = F_PAPER
    for y in range(80, 112):
        if y in (80, 81, 110, 111):
            for x in range(3, 14):
                c[y][x] = F_GREY
    if right:
        c = [r[::-1] for r in c]
    return c


def frame_layer(opening):
    """BG1 at rest, 240x160 frame indices: the top strip, the two panels; the page between them is the opening's
    white (map_edge, the TOWN MAP) or nothing (background, the GOTO map)"""
    Lc, Rc = column(False), column(True)
    f = [[0] * 240 for _ in range(160)]
    for y in range(160):
        for x in range(240):
            if y < 8:
                f[y][x] = F_INK
            elif y < 16 and 16 <= x < 224:
                f[y][x] = F_PAPER if y == 15 else F_INK
            elif x < 16:
                f[y][x] = Lc[y - 8][x + 16]
            elif x >= 224:
                f[y][x] = Rc[y - 8][x - 224]
            elif opening:
                f[y][x] = F_WHITE
    return f


def tiles_of(f, ts, row):
    out = []
    for i in range(600):
        tx, ty = i % 30, i // 30
        t = [[f[ty * 8 + y][tx * 8 + x] for x in range(8)] for y in range(8)]
        s, hf, vf = ts.add(t)
        out.append(s | hf << 10 | vf << 11 | row << 12)
    return out


def build_frame():
    f = frame_layer(True)
    top = [[f[8 + y][x] for x in range(8)] for y in range(8)]     # row 1's tiles are all alike: ink, then the rule
    fixed = {0: BLANK}
    for n in (2, 3, 0x3D, 0x3E, 0x3F):
        fixed[n] = top
    ts = TileSet(64, fixed)
    edge_bin = tiles_of(f, ts, 2)
    bts = TileSet(64, {0: BLANK})
    bg_bin = tiles_of(frame_layer(False), bts, 2)
    return ts, edge_bin, bts, bg_bin


# ---------------------------------------------------------------------------------------------------- the switch menu
def switch_menu():
    """switch_map_menu.png recoloured by role: its cells draw with row 0 (the small maps) or row 3 (the frames)"""
    im = Image.open(io.BytesIO(vbytes("switch_map_menu.png"))); px = im.load()
    uses = {}
    for f in ("switch_map_kanto_sevii_all.bin", "switch_map_kanto_sevii_123.bin", "switch_map_kanto_sevii_all2.bin"):
        for e in vbin(f):
            uses.setdefault(e & 0x3FF, set()).add(e >> 12)
    # row 0's roles in vanilla -> ours; row 3's colours -> ours
    R0 = {1: I_L4, 2: I_L3, 3: I_L2, 4: I_L1, 5: I_L1, 6: I_RT, 7: I_RT, 8: I_RT, 9: I_RT, 10: I_PALE, 11: I_PALE,
          12: I_LANE, 13: I_LANE, 14: I_SEA, 15: I_SEA}
    R3 = {v: (14 if v in (14, 15) else R3_LANE if v == 9 else R3_INK if v in (7, 10) else reink3(VPAL[48 + v]))
          for v in range(1, 16)}
    out = Image.new("P", im.size); out.putpalette([v for c in ROW0 for v in c]); o = out.load()
    w = im.size[0] // 8
    clash = []
    for t in range(im.size[0] * im.size[1] // 64):
        rows = uses.get(t, {0})
        if len(rows) > 1:
            clash.append(t)
        m = R3 if 3 in rows else R0
        for y in range(8):
            for x in range(8):
                v = px[(t % w) * 8 + x, (t // w) * 8 + y] & 15
                o[(t % w) * 8 + x, (t // w) * 8 + y] = m[v] if v else 0
    return out, clash


# ---------------------------------------------------------------------------------------------------- the sprites
#  T-449's leftover (the user chose it 2026-10-29): the cursor, the GOTO (fly) icon and the dungeon icon were still
#  vanilla's white, yellow and blue. They keep vanilla's sizes, frames and timings (sAnim_MapCursor, sAnim_FlyIcon,
#  sAnims_DungeonIcon are untouched) and their two OBJ palettes (cursor.pal, tag 0; misc_icon.pal, tag 10, shared by
#  the fly and dungeon icons), rewritten in place: no palette is added.
#
#  THE CURSOR is navigation, so legibility comes first: a measure's four brackets in a TWO-TONE stroke -- an ink core
#  with a paper halo, then (its second frame, the brackets breathing a pixel out as vanilla's do) a paper core with an
#  ink halo. Nothing else on the page is drawn in two tones or blinks between them, so it reads on the paper, on the
#  slate sea and on the ink routes alike, where vanilla's white vanished on the paper.
#  THE GOTO ICON marks a town you can GOTO: the town's notehead lit in FLOW's blue inside an ink-rimmed paper ring,
#  then (where vanilla went blank) the ring alone -- so a GOTO-able town reads differently from one you cannot GOTO to
#  in every frame, not only on the blink, and the one you cannot is the page's bare ink notehead.
#  THE DUNGEON ICON: not yet found, a small open notehead (ink ring, paper centre); found, a filled one (FLOW's blue in
#  an ink rim, a paper halo).
C_INK, C_LIGHT = 1, 2
CURSOR_PAL = [vjasc("cursor.pal")[0], INK, LIGHT] + [INK] * 13
M_INK, M_LIGHT, M_FLOW, M_PAPER = 1, 2, 3, 4
MISC_PAL = [vjasc("misc_icon.pal")[0], INK, LIGHT, FLOW, PAPER] + [INK] * 11


def halo(core, w, h, core_i, halo_i):
    """a stroke: the core's pixels, and a one-pixel halo round them (4-neighbour, so its corners stay round)"""
    t = [[0] * w for _ in range(h)]
    for (x, y) in core:
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= x + dx < w and 0 <= y + dy < h:
                t[y + dy][x + dx] = halo_i
    for (x, y) in core:
        t[y][x] = core_i
    return t


def brackets(a, b, arm=4):
    """four corners, two thick, from a to b on both axes. With its halo it spans 1..14, then 0..15 -- a pixel wider
    than vanilla's, so it closes round the GOTO icon's ring instead of sitting on it"""
    pts = set()
    for (x0, sx) in ((a, 1), (b, -1)):
        for (y0, sy) in ((a, 1), (b, -1)):
            for i in range(arm):
                for j in range(2):
                    pts.add((x0 + sx * i, y0 + sy * j))
                    pts.add((x0 + sx * j, y0 + sy * i))
    return pts


def cursor_frames():
    out = []
    for (a, b), core, hal in (((2, 13), C_INK, C_LIGHT), ((1, 14), C_LIGHT, C_INK)):
        t = halo(brackets(a, b), 16, 16, core, hal)
        for y in range(16):           # the halo never bridges the middle, so it reads as four brackets, never a box
            for x in range(16):
                if (x in (7, 8) or y in (7, 8)) and t[y][x] == hal:
                    t[y][x] = 0
        out.append(t)
    return out


def disk(cx, cy, r0, r1, w=16, h=16):
    return {(x, y) for y in range(h) for x in range(w) if r0 <= ((x - cx) ** 2 + (y - cy) ** 2) ** .5 < r1}


NOTEHEAD = ["..###..", ".#####.", "#######", "#######", ".#####.", "..###.."]


def fly_frames():
    c = 7.5
    lit = [[0] * 16 for _ in range(16)]
    for (x, y) in disk(c, c, 5.2, 6.4): lit[y][x] = M_INK
    for (x, y) in disk(c, c, 0, 5.2): lit[y][x] = M_LIGHT
    for y, r in enumerate(NOTEHEAD):       # the page's notehead (cell + 1..7, 1..6) is at sprite 5..11, 5..10
        for x, ch in enumerate(r):
            if ch == "#": lit[5 + y][5 + x] = M_FLOW
    for y, r in enumerate(NOTEHEAD):       # its rim in ink, so the blue sits on the paper
        for x, ch in enumerate(r):
            if ch != "#": continue
            if any(not (0 <= y + dy < 6 and 0 <= x + dx < 7) or NOTEHEAD[y + dy][x + dx] != "#"
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                lit[5 + y][5 + x] = M_INK
    lit[6][7] = lit[6][8] = M_LIGHT          # the shine the page's notehead has
    ring = [[0] * 16 for _ in range(16)]
    for (x, y) in disk(c, c, 5.2, 6.4): ring[y][x] = M_INK
    for (x, y) in disk(c, c, 4.4, 5.2): ring[y][x] = M_LIGHT
    return [lit, ring]


def dungeon_frames():
    found = [[0] * 8 for _ in range(8)]
    for (x, y) in disk(3.5, 3.5, 2.6, 3.7, 8, 8): found[y][x] = M_LIGHT
    for (x, y) in disk(3.5, 3.5, 1.6, 2.6, 8, 8): found[y][x] = M_INK
    for (x, y) in disk(3.5, 3.5, 0, 1.6, 8, 8): found[y][x] = M_FLOW
    unfound = [[0] * 8 for _ in range(8)]
    for (x, y) in disk(3.5, 3.5, 1.0, 2.2, 8, 8): unfound[y][x] = M_INK
    for (x, y) in disk(3.5, 3.5, 0, 1.0, 8, 8): unfound[y][x] = M_LIGHT
    return [unfound, found]                   # frame 0 not visited, frame 1 visited (sAnims_DungeonIcon)


def sprite_png(frames, pal):
    w, hh = len(frames[0][0]), len(frames[0])
    im = Image.new("P", (w, hh * len(frames))); im.putpalette([v for c in pal for v in c]); o = im.load()
    for k, f in enumerate(frames):
        for y in range(hh):
            for x in range(w):
                o[x, k * hh + y] = f[y][x]
    return im


# ---------------------------------------------------------------------------------------------------- files
def png16(tiles, pal, width=16):
    n = len(tiles)
    rows = (n + width - 1) // width
    im = Image.new("P", (width * 8, rows * 8)); im.putpalette([v for c in pal for v in c]); o = im.load()
    for i, t in enumerate(tiles):
        for y in range(8):
            for x in range(8):
                o[(i % width) * 8 + x, (i // width) * 8 + y] = (t or BLANK)[y][x]
    return im


def strip_png(c, x0, y0):
    im = Image.new("P", (32, 64)); im.putpalette([v for col in FRAME for v in col]); o = im.load()
    for y in range(64):
        for x in range(32):
            o[x, y] = c[y0 + y][x0 + x]
    return im


def jasc(colours):
    lines = ["JASC-PAL", "0100", str(len(colours))] + ["%d %d %d" % c for c in colours]
    return ("\r\n".join(lines) + "\r\n").encode()


def png_bytes(im):
    b = io.BytesIO(); im.save(b, "PNG", optimize=False); return b.getvalue()


def bin_bytes(entries):
    return b"".join(struct.pack("<H", e) for e in entries)


def outputs():
    analyses = {p: analyse(p) for p in PAGES}
    ts, bins, imgs = build_bg0(analyses)
    fts, edge_bin, bts, bg_bin = build_frame()
    menu, clash = switch_menu()
    Lc, Rc = column(False), column(True)
    files = {
        "region_map.png": png_bytes(png16(ts.slots[:max(ts.used(), 0x140)], ROW0)),
        "region_map.pal": jasc(ROW0 + FRAME + ROW2 + ROW3 + FRAME),
        "sea.pal": jasc(sea_row(0)),
        "map_edge.png": png_bytes(png16(fts.slots, FRAME)),
        "map_edge.bin": bin_bytes(edge_bin),
        "background.png": png_bytes(png16(bts.slots[:bts.used()], FRAME, width=bts.used())),
        "background.bin": bin_bytes(bg_bin),
        "switch_map_menu.png": png_bytes(menu),
        "cursor.png": png_bytes(sprite_png(cursor_frames(), CURSOR_PAL)),
        "cursor.pal": jasc(CURSOR_PAL),
        "fly_icon.png": png_bytes(sprite_png(fly_frames(), MISC_PAL)),
        "dungeon_icon.png": png_bytes(sprite_png(dungeon_frames(), MISC_PAL)),
        "misc_icon.pal": jasc(MISC_PAL),
    }
    for p in PAGES:
        files[p + ".bin"] = bin_bytes(bins[p])
    for name, c, y0 in (("top_left", Lc, 0), ("mid_left", Lc, 64), ("bottom_left", Lc, 128),
                        ("top_right", Rc, 0), ("mid_right", Rc, 64), ("bottom_right", Rc, 128)):
        files["map_edge_%s.png" % name] = png_bytes(strip_png(c, 0, y0))
    tb = vjasc("top_bar.pal")
    tb[1] = LIGHT        # the white of every name on the map
    tb[15] = INK         # the top strip and, on the GOTO map, the backdrop
    files["top_bar.pal"] = jasc(tb)
    state = dict(analyses=analyses, ts=ts, bins=bins, imgs=imgs, fts=fts, edge_bin=edge_bin, bts=bts,
                 bg_bin=bg_bin, clash=clash, Lc=Lc, Rc=Rc, tb=tb)
    return files, state


# ---------------------------------------------------------------------------------------------------- rendering
def render_page(bins, tiles, pal80, row5, page_bin, bg1_bin, bg1_tiles, bg1_pal, backdrop, switch=False):
    """a screen at rest: backdrop, BG1, BG0 (the GBA's order for these priorities)"""
    im = Image.new("RGB", (240, 160), backdrop); o = im.load()

    def lay(entries, T, pal, rowpal):
        for i, e in enumerate(entries[:600]):
            t, hf, vf, p = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
            if t >= len(T) or T[t] is None: continue
            for y in range(8):
                for x in range(8):
                    c = T[t][7 - y if vf else y][7 - x if hf else x]
                    if c: o[(i % 30) * 8 + x, (i // 30) * 8 + y] = rowpal(p)[c]
    if bg1_bin:
        lay(bg1_bin, bg1_tiles, None, lambda p: bg1_pal[p])
    entries = list(page_bin)
    if switch:
        for r, b in ((14, 0xF0), (15, 0x100), (16, 0x110)):
            for i in range(3):
                entries[r * 30 + 24 + i] = (b + i) | 3 << 12
    lay(entries, tiles, None, lambda p: row5 if p == 5 else pal80[p * 16:p * 16 + 16])
    return im


def today_screen(page, goto=False):
    T = VTILES
    me = vtiles("background.png" if goto else "map_edge.png")
    row2 = [tuple(int(v * 95 / 100) for v in c) for c in VPAL[32:48]]
    pal = {p: VPAL[p * 16:p * 16 + 16] for p in range(5)}
    pal[2] = row2[:15] + [VPAL[47]]
    im = render_page(None, T, VPAL, None, vbin(page + ".bin"), vbin("background.bin" if goto else "map_edge.bin"),
                     me, pal, (16, 115, 230))
    o = im.load()
    for y in range(16):
        for x in range(240):
            o[x, y] = (16, 115, 230)
    return im


def built_screen(state, page, frame=0, switch=False, goto=False):
    T = state["ts"].slots
    pal80 = ROW0 + FRAME + ROW2 + ROW3 + FRAME
    frame_pal = {p: pal80[p * 16:p * 16 + 16] for p in range(5)}
    frame_pal[2] = [tuple(v * 8 for v in darken95(gba5(c))) for c in ROW2[:15]] + [ROW2[15]]
    if goto:
        bg1, bt = state["bg_bin"], state["bts"].slots
    else:
        bg1, bt = state["edge_bin"], state["fts"].slots
    return render_page(None, T, pal80, sea_row(frame), state["bins"][page], bg1, bt, frame_pal, INK, switch)


def font(n=14):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except Exception:
        return ImageFont.load_default()


def label(im, text, xy, fill=(235, 235, 240), n=14):
    ImageDraw.Draw(im).text(xy, text, fill=fill, font=font(n))


def mosaic(im, w=2, hh=2):
    out = im.copy(); s = im.load(); d = out.load()
    for y in range(16, 160):
        for x in range(24, 216):
            d[x, y] = s[x - (x % w), y - (y % hh)]
    return out


def sheets(state, out):
    os.makedirs(out, exist_ok=True)
    written = []
    names = {"kanto": "THE MAINLAND", "sevii_123": "SEVII 1-2-3", "sevii_45": "SEVII 4-5", "sevii_67": "SEVII 6-7"}
    # today | built, every page, at 2x
    for group, pages in (("mainland", ["kanto"]), ("islands", ["sevii_123", "sevii_45", "sevii_67"])):
        S = 2
        W = 2 * (240 * S + 12) + 12
        H = 34 + len(pages) * (160 * S + 30)
        sh = Image.new("RGB", (W, H), (24, 24, 28))
        label(sh, "T-449  the TOWN MAP in SCORE  --  TODAY | BUILT (decoded from what the ROM is built from)", (12, 8))
        for i, p in enumerate(pages):
            y0 = 34 + i * (160 * S + 30)
            for j, im in enumerate((today_screen(p), built_screen(state, p))):
                sh.paste(im.resize((240 * S, 160 * S), Image.NEAREST), (12 + j * (240 * S + 12), y0))
            label(sh, names[p], (12, y0 + 160 * S + 6), (180, 180, 190))
        f = os.path.join(out, "t449b_%s.png" % group); sh.save(f); written.append(f)
    # the mosaic: T-317's 2x2 and 2x1 before the understandings arrive
    sh = Image.new("RGB", (2 * 492 + 12, 3 * 350 + 34), (24, 24, 28))
    label(sh, "T-317's clarity: the page at 2x2, 2x1 and sharp -- TODAY | BUILT", (12, 8))
    for j, im in enumerate((today_screen("kanto"), built_screen(state, "kanto"))):
        for i, (w, hh) in enumerate(((2, 2), (2, 1), (1, 1))):
            sh.paste(mosaic(im, w, hh).resize((480, 320), Image.NEAREST), (12 + j * 492, 34 + i * 350))
            label(sh, "mosaic %dx%d" % (w, hh) if w * hh > 1 else "sharp", (12 + j * 492, 34 + i * 350 + 322),
                  (180, 180, 190))
    f = os.path.join(out, "t449b_mosaic.png"); sh.save(f); written.append(f)
    # the frame: the opening's closed score, half open, and at rest; the GOTO map's frame; the switch buttons
    sh = Image.new("RGB", (4 * 252 + 12, 2 * 190 + 40), (24, 24, 28))
    label(sh, "the frame: the closed score, opening, open (TOWN MAP) | the GOTO map, and the switch button", (12, 8))
    Lc, Rc = state["Lc"], state["Rc"]
    for k, dxo in enumerate((0, 52, 104)):
        im = Image.new("RGB", (240, 160), (0, 0, 0)); o = im.load()
        lx, rx = 104 - dxo - 16, 136 + dxo - 16
        for y in range(160):
            for x in range(240):
                if 16 <= y and lx + 32 <= x < rx: o[x, y] = LIGHT
        for col, x0 in ((Lc, lx), (Rc, rx)):
            for y in range(192):
                for x in range(32):
                    v = col[y][x]
                    if v and 0 <= x0 + x < 240 and 0 <= y + 8 < 160:
                        o[x0 + x, y + 8] = FRAME[v]
        sh.paste(im, (12 + k * 252, 34))
    sh.paste(built_screen(state, "kanto", goto=True), (12 + 3 * 252, 34))
    sh.paste(built_screen(state, "sevii_45", switch=True), (12, 34 + 190))
    sh.paste(built_screen(state, "sevii_45", switch=True).crop((184, 104, 224, 160)).resize((160, 224), Image.NEAREST),
             (264, 34 + 190 - 40 + 40))
    f = os.path.join(out, "t449b_frame.png"); sh.save(f); written.append(f)
    # the sea, animated: the island page, 2x, a frame every 4 of the task's
    frames = [built_screen(state, "sevii_45", n).resize((480, 320), Image.NEAREST) for n in range(0, 480, 4)]
    f = os.path.join(out, "t449b_sea.gif")
    frames[0].save(f, save_all=True, append_images=frames[1:], duration=67, loop=0); written.append(f)
    written += icon_sheets(state, out)
    return written


# ---------------------------------------------------------------------------------------------------- the sprites, shown
def goto_towns():
    """the mapsecs GetMapsecType can call VISITED: the cells CreateFlyIcons puts a GOTO icon on"""
    s = open(os.path.join(GBA, "src/region_map.c")).read()
    body = s[s.index("static u8 GetMapsecType(u8 mapsec)\n{"):]
    body = body[:body.index("\n}\n")]
    return set(re.findall(r"case (MAPSEC_\w+):\s*return[^;]*MAPSECTYPE_VISITED", body))


def dungeon_layer(page):
    s = open(os.path.join(L, HDR[page])).read()
    body = s[s.index("[LAYER_DUNGEON]"):]
    rows = re.findall(r"\{([^{}]*)\}", body)
    return [[t.strip() for t in r.split(",") if t.strip()] for r in rows][:15]


def sprite_frames(png, pal, fw, fh):
    """an icon PNG as frames of (r, g, b) or None, read from bytes"""
    im = Image.open(io.BytesIO(png)); px = im.load()
    return [[[pal[px[x, k * fh + y] & 15] if px[x, k * fh + y] & 15 else None for x in range(fw)] for y in range(fh)]
            for k in range(im.size[1] // fh)]


def blit(im, f, x0, y0):
    o = im.load()
    for y, r in enumerate(f):
        for x, c in enumerate(r):
            if c is not None and 0 <= x0 + x < 240 and 0 <= y0 + y < 160:
                o[x0 + x, y0 + y] = c


def icon_sets(today):
    """(cursor frames, fly frames, dungeon frames), vanilla's or ours, as colours"""
    if today:
        cp, mp = vjasc("cursor.pal"), vjasc("misc_icon.pal")
        c, f, d = vbytes("cursor.png"), vbytes("fly_icon.png"), vbytes("dungeon_icon.png")
    else:
        cp, mp = CURSOR_PAL, MISC_PAL
        c, f, d = (png_bytes(sprite_png(cursor_frames(), CURSOR_PAL)), png_bytes(sprite_png(fly_frames(), MISC_PAL)),
                   png_bytes(sprite_png(dungeon_frames(), MISC_PAL)))
    return sprite_frames(c, cp, 16, 16), sprite_frames(f, mp, 16, 16), sprite_frames(d, mp, 8, 8)


SHEET_UNVISITED = {"MAPSEC_CINNABAR_ISLAND", "MAPSEC_INDIGO_PLATEAU", "MAPSEC_THREE_ISLAND", "MAPSEC_FIVE_ISLAND"}
SHEET_CURSOR = {"kanto": ("MAPSEC_CERULEAN_CITY", "MAPSEC_ROUTE_9"),
                "sevii_123": ("MAPSEC_TWO_ISLAND", "MAPSEC_BOND_BRIDGE")}


def goto_screen(state, page, today, cursor_sec, t=0):
    """the GOTO map at rest after t frames: the page, the dungeon icons, the GOTO icons, the cursor on cursor_sec
    (CreateSprite's centre is 8*x+36, 8*y+36; subpriority puts the cursor over the GOTO icons over the dungeons)"""
    im = today_screen(page, goto=True) if today else built_screen(state, page, frame=t, goto=True)
    cur, fly, dun = icon_sets(today)
    lay, dl, towns = layout(page), dungeon_layer(page), goto_towns()
    for cy in range(15):
        for cx in range(22):
            sec = dl[cy][cx]
            if sec == "MAPSEC_NONE": continue
            off = 2 if lay[cy][cx] in towns and lay[cy][cx] != "MAPSEC_ROUTE_10_POKECENTER" else 0
            found = h(sec, "found") % 2 == 0
            blit(im, dun[1 if found else 0], 8 * cx + 32 + off, 8 * cy + 32 + off)
    fk = 0 if (t % 90) < 30 else 1                           # sAnim_FlyIcon: 30 frames, then 60
    for cy in range(15):
        for cx in range(22):
            if lay[cy][cx] in towns and lay[cy][cx] not in SHEET_UNVISITED:
                blit(im, fly[fk], 8 * cx + 28, 8 * cy + 28)
    cells = [(cx, cy) for cy in range(15) for cx in range(22) if lay[cy][cx] == cursor_sec]
    cx, cy = cells[len(cells) // 2]
    blit(im, cur[(t // 20) % 2], 8 * cx + 28, 8 * cy + 28)  # sAnim_MapCursor: 20 and 20
    return im


def icon_sheets(state, out):
    written = []
    names = {"kanto": "THE MAINLAND", "sevii_123": "SEVII 1-2-3"}
    W = 12 + 720 + 12 + 720 + 12 + 240 + 12
    rows = [(p, k) for p in ("kanto", "sevii_123") for k in (0, 1)]
    H = 34 + len(rows) * (480 + 30) + 300
    sh = Image.new("RGB", (W, H), (24, 24, 28))
    label(sh, "T-449  the GOTO map's cursor and icons  --  TODAY | DRAFT, 3x and 1x (decoded from what the ROM is "
              "built from; %s not visited)" % ", ".join(s[7:] for s in sorted(SHEET_UNVISITED)), (12, 8))
    for i, (p, k) in enumerate(rows):
        sec = SHEET_CURSOR[p][k]
        y0 = 34 + i * 510
        a, b = goto_screen(state, p, True, sec), goto_screen(state, p, False, sec)
        sh.paste(a.resize((720, 480), Image.NEAREST), (12, y0))
        sh.paste(b.resize((720, 480), Image.NEAREST), (744, y0))
        sh.paste(a, (1476, y0)); sh.paste(b, (1476, y0 + 170))
        label(sh, "%s -- the cursor on %s (%s)" % (names[p], sec[7:], "a town" if k == 0 else "a route"),
              (12, y0 + 484), (180, 180, 190))
    # every frame, 8x, on the paper and on the sea: TODAY above, DRAFT below
    y0 = 34 + len(rows) * 510
    label(sh, "every frame at 8x, on the paper and on the sea: cursor A B | GOTO icon A B | dungeon not found, found"
              "  --  TODAY above, DRAFT below", (12, y0))
    for j, today in enumerate((True, False)):
        cur, fly, dun = icon_sets(today)
        x = 12
        for ground in (PAPER, SEA):
            for f in cur + fly + dun:
                n = len(f)
                tile = Image.new("RGB", (16, 16), ground)
                if n == 8:
                    blit(tile, f, 4, 4)
                else:
                    blit(tile, f, 0, 0)
                if n == 16 and f in fly:      # the page's own notehead under the GOTO icon
                    pass
                sh.paste(tile.resize((112, 112), Image.NEAREST), (x, y0 + 22 + j * 130))
                x += 118
            x += 24
    f = os.path.join(out, "t449i_icons.png"); sh.save(f); written.append(f)
    # animated, at the engine's timings: the mainland, 2x, the cursor on a town
    frames = [goto_screen(state, "kanto", False, SHEET_CURSOR["kanto"][0], t).resize((480, 320), Image.NEAREST)
              for t in range(0, 180, 5)]
    f = os.path.join(out, "t449i_goto.gif")
    frames[0].save(f, save_all=True, append_images=frames[1:], duration=83, loop=0); written.append(f)
    return written


# ---------------------------------------------------------------------------------------------------- main
def main():
    files, state = outputs()
    ts = state["ts"]
    print("  BG0: %d tile slots used of 512 (vanilla 320); the four pages' rows: %s" % (
        ts.used(), ", ".join("%s %s" % (p, dict(sorted(Counter(e >> 12 for e in state["bins"][p]).items())))
                             for p in PAGES)))
    print("  BG1: map_edge %d of 64 tiles, background %d" % (state["fts"].used(), state["bts"].used()))
    if state["clash"]:
        print("  !! switch_map_menu tiles drawn with two rows: %s" % state["clash"])
    sea = sum(1 for p in PAGES for e in state["bins"][p] if e >> 12 == 5)
    print("  the open sea: %d tiles in row 5 over the four pages" % sea)
    differ = [f for f, b in files.items() if not os.path.exists(os.path.join(G, f)) or
              open(os.path.join(G, f), "rb").read() != b]
    print("  engine: %s" % ("every file is what this writes" if not differ else
                            "%d files would change: %s" % (len(differ), ", ".join(sorted(differ)))))
    if DRAFT:
        i = ARGS.index("--draft")
        out = ARGS[i + 1] if len(ARGS) > i + 1 and not ARGS[i + 1].startswith("--") else os.path.dirname(
            daemonslib.preview("t449b"))
        for f in sheets(state, out):
            print("  sheet %s" % f)
    elif not WRITE:
        p = daemonslib.preview("t449b_regionmap.png")
        built_screen(state, "kanto").resize((480, 320), Image.NEAREST).save(p)
        print("  preview %s" % p)
    if WRITE:
        if "--approved" not in ARGS:
            print("  --write refused: T-449's region map is written only with --approved (the user approved "
                  "direction A, SCORE, on 2026-10-24)")
            return 0
        for f, b in files.items():
            path = os.path.join(G, f)
            if not os.path.exists(path) or open(path, "rb").read() != b:
                open(path, "wb").write(b)
                print("  written %s" % os.path.relpath(path, GBA))
    return 0


if __name__ == "__main__":
    sys.exit(main())

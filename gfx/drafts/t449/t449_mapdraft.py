#!/usr/bin/env python3
"""T-449 DRAFT: the TOWN MAP (SITEMAP / GOTO) redrawn in the game's music-and-code language.

    ~/.pyenv/versions/3.12.2/bin/python3 gfx/drafts/t449/t449_mapdraft.py [OUTDIR]

Reads only (never writes) engineGba/graphics/region_map/* and src/data/region_map/region_map_layout_*.h.
Writes the drafts beside this file and the review sheets to OUTDIR (default: this folder).

SAME SHAPE. Every page is rebuilt from today's page, pixel class by pixel class: what is sea stays sea, what
is land stays land at the same height, and the routes and towns are re-derived from the cursor grid's own
cells (LAYER_MAP), so every town, route and island cell stays exactly where the cursor expects it.

THREE DIRECTIONS
    A SCORE    paper land, ink coast; routes are beams with a barline at every cell (a cell is a measure);
               towns are noteheads; the sea is a shuffle of notes that step up and down.
    B CIRCUIT  a dark board; routes are copper traces, towns are vias; the sea is bits flipping 0 <-> 1.
    C SIGNAL   dark land drawn as contour lines (a waveform at every height); routes are a two-line staff;
               towns are noteheads in a via ring; the sea shuffles between 0, 1 and a note.

ONE HUE, ONE MEANING. The map is ink and paper (the UI's own language). The only type colour is FLOW's,
on the sea lanes you can only cross with TRAVERSE (a FLOW routine). GOTO (VECTOR) keeps its own icon layer.

PALETTES. Row 0 holds every static colour (land, coast, routes, towns, the calm sea near a shore); a NEW
row 5 holds the open sea, whose glyph colours are cycled to animate it (12 entries, 4 groups x {A, B, both}).
Coastal tiles mix land and sea so they cannot use row 5 -- the shore is calm water, and the shuffle starts
one tile out. Row 3 keeps the switch-map icon, row 2 the white side columns, both copied as they are.
"""
import os, re, struct, sys, hashlib
from collections import Counter, deque
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
GBA = os.path.join(ROOT, "engineGba")
G = os.path.join(GBA, "graphics/region_map/")
L = os.path.join(GBA, "src/data/region_map/")
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE
PAGES = ["kanto", "sevii_123", "sevii_45", "sevii_67"]
HDR = {"kanto": "region_map_layout_kanto.h", "sevii_123": "region_map_layout_sevii_123.h",
       "sevii_45": "region_map_layout_sevii_45.h", "sevii_67": "region_map_layout_sevii_67.h"}
FLOW = (70, 106, 176)      # gbasprite.py TYPE_COLOR["WATER"] -- FLOW; TRAVERSE is FLOW's routine
VECTOR = (206, 70, 70)     # TYPE_COLOR["FLYING"] -- VECTOR; GOTO is VECTOR's routine

# ---------------------------------------------------------------- reading today's page
def jasc(f):
    L_ = open(G + f).read().split("\n")[3:]
    return [tuple(map(int, l.split())) for l in L_ if l.strip()]

def tiles(f):
    im = Image.open(G + f); w, h = im.size; px = im.load()
    return [[[px[tx * 8 + x, ty * 8 + y] & 15 for x in range(8)] for y in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]

TODAY_PAL = jasc("region_map.pal")
TODAY_TILES = tiles("region_map.png")

def today_idx(page):
    """(row, index) per pixel of BG0, None where transparent."""
    d = open(G + page + ".bin", "rb").read()
    out = [[None] * 240 for _ in range(160)]
    for i in range(600):
        e = struct.unpack_from("<H", d, i * 2)[0]
        t, hf, vf, p = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
        for y in range(8):
            for x in range(8):
                c = TODAY_TILES[t][7 - y if vf else y][7 - x if hf else x]
                if c:
                    out[(i // 30) * 8 + y][(i % 30) * 8 + x] = (p, c)
    return out

def today_rgb(page):
    idx = today_idx(page); im = Image.new("RGB", (240, 160)); px = im.load()
    for y in range(160):
        for x in range(240):
            if idx[y][x]:
                px[x, y] = TODAY_PAL[idx[y][x][0] * 16 + idx[y][x][1]]
    return im

SEA, SEAROUTE, LAND, ROUTE, PALE, TOWN, UI, WHITE, NONE = range(9)
def classify(pi):
    if pi is None: return NONE, 0
    r, c = pi
    if r == 0:
        if 1 <= c <= 5: return LAND, c
        if 6 <= c <= 9: return ROUTE, 0
        if c in (10, 11): return PALE, 0
        if c in (12, 13): return SEAROUTE, 0
        return SEA, 0
    if r == 1: return (TOWN if 6 <= c <= 11 else ROUTE), 0
    if r == 2: return WHITE, 0
    if r == 3: return (SEA if c >= 14 else UI), 0
    return UI, 0

def layout(page):
    s = open(L + HDR[page]).read()
    body = s[s.index("[LAYER_MAP]"):s.index("[LAYER_DUNGEON]")]
    rows = re.findall(r"\{([^{}]*)\}", body)
    return [[t.strip() for t in r.split(",") if t.strip()] for r in rows][:15]

def analyse(page):
    idx = today_idx(page)
    cls = [[classify(idx[y][x]) for x in range(240)] for y in range(160)]
    # the ground under a route or a town: a road or a town stands on land (the islands' sand IS their road),
    # found breadth-first from the nearest land; a pale route (a bridge) takes whatever is nearest, sea or land
    base = [[None] * 240 for _ in range(160)]
    def fill(seeds, into):
        q = deque(seeds)
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if 0 <= X < 240 and 0 <= Y < 160 and base[Y][X] is None and cls[Y][X][0] in into:
                    base[Y][X] = base[y][x]; q.append((X, Y))
    land, sea = [], []
    for y in range(160):
        for x in range(240):
            k, lv = cls[y][x]
            if k == LAND: base[y][x] = ("L", lv); land.append((x, y))
            elif k in (SEA, SEAROUTE): base[y][x] = ("S", 0); sea.append((x, y))
    fill(land, (ROUTE, TOWN))
    for y in range(160):
        for x in range(240):
            if cls[y][x][0] in (ROUTE, TOWN) and base[y][x] is None: base[y][x] = ("L", 2)
    fill([(x, y) for y in range(160) for x in range(240) if base[y][x]], (PALE,))
    lay = layout(page)
    # towns: each ball's own centre, snapped to its cursor cell
    towncells = set(); seen = set()
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
                        plain_route = re.match(r"MAPSEC_ROUTE_\d+$", sec) is not None
                        if d2 <= 100: cands.append((plain_route, d2, (cx, cy)))
                if cands: towncells.add(min(cands)[2])
    cells = {}
    for cy in range(15):
        for cx in range(22):
            if lay[cy][cx] == "MAPSEC_NONE": continue
            px_, py_ = 8 * (cx + 4) + 4, 8 * (cy + 4) + 4
            box = [cls[py_ + dy][px_ + dx][0] for dy in range(-3, 4) for dx in range(-3, 4)]
            town = (cx, cy) in towncells
            kinds = Counter(k for k in box if k in (ROUTE, PALE, SEAROUTE))
            if town or kinds:
                cells[(cx, cy)] = dict(sec=lay[cy][cx], town=town,
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
                kind = kc.most_common(1)[0][0] if kc else ROUTE
                links.append(((cx, cy), n, kind))
    return dict(idx=idx, cls=cls, base=base, cells=cells, links=links)

# ---------------------------------------------------------------- the three directions
def h(*a):
    return int(hashlib.md5(repr(a).encode()).hexdigest()[:8], 16)

class Style:
    name = ""
    def __init__(self):
        self.row0 = [(0, 0, 0)] * 16
        self.sea = [(0, 0, 0)] * 16   # row 5
    # sea glyph pairs: list of (A-pixels, B-pixels) inside an 8x8 tile; shared pixels go to 'both'
    glyphs = []
    def phases(self):
        """4 frames x 4 groups -> 'A', 'B', '-' (blank)"""
        return [["A", "B", "-", "A"], ["B", "-", "A", "A"], ["-", "A", "B", "B"], ["A", "A", "-", "B"]]

# Row 0 index map shared by all three: 0 transparent, 1..4 land by height, 5 land texture, 6 coast,
# 7 calm sea, 8 calm sea texture, 9 route, 10 route light, 11 pale route, 12 TRAVERSE lane (FLOW),
# 13 town, 14 town light, 15 spare (switch icon stays in row 3, side columns in row 2)
I_L1, I_L2, I_L3, I_L4, I_TEX, I_COAST, I_SEA, I_SEATEX, I_RT, I_RTL, I_PALE, I_LANE, I_TOWN, I_TOWNL = range(1, 15)
# Row 5: 1 sea, 2 sea texture, then group g: 3+3g = A only, 4+3g = B only, 5+3g = both
def SEA_A(g): return 3 + 3 * g
def SEA_B(g): return 4 + 3 * g
def SEA_AB(g): return 5 + 3 * g

def glyph(rows):
    return {(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch == "#"}

class Score(Style):
    name = "A  SCORE"
    def __init__(self):
        paper = [(238, 230, 210), (226, 216, 192), (210, 198, 170), (192, 178, 148)]
        self.row0 = [(0, 0, 0)] + paper + [(176, 164, 136), (44, 38, 52), (182, 188, 194), (170, 177, 184),
                     (44, 38, 52), (110, 100, 112), (120, 110, 120), FLOW, (30, 26, 36), (250, 246, 236), (255, 0, 255)]
        self.sea = [(0, 0, 0), (182, 188, 194), (170, 177, 184)] + [(182, 188, 194)] * 13
        self.on = (70, 74, 92)
        # a note at two pitches: A low, B high (the head moves, the stem goes with it)
        lo = glyph(["", "", "....#", "....#", "....##", "....#", ".####", ".###"])
        hi = glyph(["....#", "....##", "....#", "....#", ".####", ".###", "", ""])
        lo2 = glyph(["", "", "...#", "...#", "...#", "...#", "####", "###"])
        hi2 = glyph(["...#", "...#", "...#", "####", "###", "", "", ""])
        self.glyphs = [(lo, hi), (hi, lo), (lo2, hi2), (hi2, lo2)]
    def land(self, x, y, lv, ax, ay):
        # elevation as a staff: the higher the ground, the more of the five lines are drawn
        lines = {1: (), 2: (), 3: (2,), 4: (2, 6), 5: (0, 2, 4, 6)}[lv]
        if (y % 8) in lines and lv >= 3:
            return I_TEX
        return [I_L1, I_L1, I_L2, I_L3, I_L4][lv - 1]
    def calm(self, x, y):
        return I_SEATEX if (y % 4 == 0 and (x // 2) % 3 == 0) else I_SEA
    def route(self, img, a, b, kind):
        ax, ay = 8 * (a[0] + 4) + 4, 8 * (a[1] + 4) + 4
        bx, by = 8 * (b[0] + 4) + 4, 8 * (b[1] + 4) + 4
        horiz = ay == by
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
    def town(self, img, cx, cy):
        x0, y0 = 8 * (cx + 4) + 1, 8 * (cy + 4) + 1
        head = ["..###..", ".#####.", "#######", "#######", ".#####.", "..###..", "......."]
        for y, r in enumerate(head):
            for x, ch in enumerate(r):
                if ch == "#": put(img, x0 + x, y0 + y, I_TOWN)
        put(img, x0 + 2, y0 + 1, I_TOWNL); put(img, x0 + 3, y0 + 1, I_TOWNL)

class Circuit(Style):
    name = "B  CIRCUIT"
    def __init__(self):
        board = [(56, 60, 68), (66, 71, 80), (78, 84, 95), (92, 99, 112)]
        self.row0 = [(0, 0, 0)] + board + [(112, 120, 134), (196, 200, 206), (18, 22, 32), (28, 34, 46),
                     (200, 158, 88), (240, 210, 150), (150, 128, 96), FLOW, (200, 158, 88), (18, 22, 32), (255, 0, 255)]
        self.sea = [(0, 0, 0), (18, 22, 32), (24, 30, 42)] + [(18, 22, 32)] * 13
        self.on = (150, 160, 172)
        zero = glyph(["", ".###", ".#.#", ".#.#", ".#.#", ".###"])
        one = glyph(["", "..#", ".##", "..#", "..#", ".###"])
        zero2 = {(x + 3, y + 1) for x, y in zero if x + 3 < 8 and y + 1 < 8}
        one2 = {(x + 3, y + 1) for x, y in one if x + 3 < 8 and y + 1 < 8}
        self.glyphs = [(zero, one), (one, zero), (zero2, one2), (one2, zero2)]
    def land(self, x, y, lv, ax, ay):
        # a ground plane: copper dots, denser with height
        step = {1: 0, 2: 0, 3: 6, 4: 4, 5: 3}[lv]
        if step and x % step == 0 and y % step == (x // step) % 2:
            return I_TEX
        return [I_L1, I_L1, I_L2, I_L3, I_L4][lv - 1]
    def calm(self, x, y):
        return I_SEATEX if (x % 8 == 0 and y % 2 == 0) else I_SEA
    def route(self, img, a, b, kind):
        ax, ay = 8 * (a[0] + 4) + 4, 8 * (a[1] + 4) + 4
        bx, by = 8 * (b[0] + 4) + 4, 8 * (b[1] + 4) + 4
        horiz = ay == by
        for i in range(9):
            x, y = (ax + i, ay) if horiz else (ax, ay + i)
            if kind == SEAROUTE:
                if i % 4 < 2:
                    put(img, x, y, I_LANE); put(img, x + (0 if horiz else -1), y + (-1 if horiz else 0), I_LANE)
            elif kind == PALE:
                put(img, x, y, I_PALE)
            else:
                put(img, x, y, I_RT); put(img, x + (0 if horiz else -1), y + (-1 if horiz else 0), I_RTL)
    def town(self, img, cx, cy):
        x0, y0 = 8 * (cx + 4) + 1, 8 * (cy + 4) + 1
        via = [".#####.", "##...##", "#.....#", "#.....#", "#.....#", "##...##", ".#####."]
        for y, r in enumerate(via):
            for x, ch in enumerate(r):
                if ch == "#": put(img, x0 + x, y0 + y, I_TOWN)
                elif 1 <= x <= 5 and 1 <= y <= 5 and not (x in (1, 5) and y in (1, 5)):
                    put(img, x0 + x, y0 + y, I_TOWNL if (x, y) in ((2, 2), (3, 2), (2, 3)) else I_SEA)
        for x, y in ((3, 3),):
            put(img, x0 + x, y0 + y, I_SEA)

class Signal(Style):
    name = "C  SIGNAL"
    def __init__(self):
        ground = [(40, 38, 46), (48, 46, 56), (58, 55, 66), (70, 66, 78)]
        self.row0 = [(0, 0, 0)] + ground + [(150, 142, 128), (226, 218, 198), (14, 14, 20), (24, 24, 32),
                     (226, 218, 198), (150, 142, 128), (120, 114, 104), FLOW, (238, 230, 210), (14, 14, 20), (255, 0, 255)]
        self.sea = [(0, 0, 0), (14, 14, 20), (22, 22, 30)] + [(14, 14, 20)] * 13
        self.on = (150, 142, 128)
        one = glyph(["", "", "..#", ".##", "..#", "..#", ".###"])
        note = glyph(["", "...#", "...#", "...#", ".###", ".##"])
        zero = glyph(["", "", ".###", ".#.#", ".#.#", ".#.#", ".###"])
        self.glyphs = [(one, note), (zero, note), (note, one), (note, zero)]
        self.levels = None
    def land(self, x, y, lv, ax, ay):
        return [I_L1, I_L1, I_L2, I_L3, I_L4][lv - 1]
    def contour(self, img, base):
        # a contour wherever the height changes: the ground drawn as a waveform at every level
        for y in range(16, 160):
            for x in range(16, 224):
                b = base[y][x]
                if not b or b[0] != "L": continue
                for dx, dy in ((1, 0), (0, 1)):
                    X, Y = x + dx, y + dy
                    if X < 224 and Y < 160 and base[Y][X] and base[Y][X][0] == "L" and base[Y][X][1] > b[1] >= 2:
                        put(img, x, y, I_TEX)
    def calm(self, x, y):
        return I_SEATEX if ((x + y) % 6 == 0 and y % 2 == 0) else I_SEA
    def route(self, img, a, b, kind):
        ax, ay = 8 * (a[0] + 4) + 4, 8 * (a[1] + 4) + 4
        horiz = ay == 8 * (b[1] + 4) + 4
        for i in range(9):
            x, y = (ax + i, ay) if horiz else (ax, ay + i)
            if kind == SEAROUTE:
                if i % 3 != 2:
                    put(img, x, y - 1 if horiz else y, I_LANE); put(img, x if horiz else x - 1, y + 1 if horiz else y, I_LANE)
                    if not horiz: put(img, x + 1, y, I_LANE)
            elif kind == PALE:
                if i % 2 == 0: put(img, x, y, I_PALE)
            else:   # a two-line staff (or a bus): the cell's centre left open. The lines sit on EVEN pixels
                    # (centre +-2) so T-317's 2x2 mosaic, which samples each block's top-left, still shows them
                if horiz:
                    put(img, x, y - 2, I_RT); put(img, x, y + 2, I_RT)
                else:
                    put(img, x - 2, y, I_RT); put(img, x + 2, y, I_RT)
    def town(self, img, cx, cy):
        x0, y0 = 8 * (cx + 4) + 1, 8 * (cy + 4) + 1
        ring = [".#####.", "#.....#", "#..##.#", "#.###.#", "#.##..#", "#.....#", ".#####."]
        for y, r in enumerate(ring):
            for x, ch in enumerate(r):
                if ch == "#": put(img, x0 + x, y0 + y, I_TOWN if (x in (0, 6) or y in (0, 6)) else I_TOWN)
                elif 0 < x < 6 and 0 < y < 6: put(img, x0 + x, y0 + y, I_SEA)

def put(img, x, y, i):
    if 0 <= x < 240 and 0 <= y < 160:
        img[y][x] = (0, i)

# ---------------------------------------------------------------- composing a page
def compose(style, page, A):
    cls, base, idx = A["cls"], A["base"], A["idx"]
    img = [[None] * 240 for _ in range(160)]
    for y in range(160):
        for x in range(240):
            k, lv = cls[y][x]
            if k == NONE: continue
            if k == UI: img[y][x] = ("keep", idx[y][x]); continue
            if k == WHITE: img[y][x] = ("keep", idx[y][x]); continue
            b = base[y][x] or ("S", 0)
            if b[0] == "L":
                img[y][x] = (0, style.land(x, y, max(1, b[1]), x, y))
            else:
                img[y][x] = (0, style.calm(x, y))
    # coast: land touching sea
    for y in range(160):
        for x in range(240):
            b = base[y][x]
            if not b or b[0] != "L" or cls[y][x][0] in (UI, WHITE): continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if 0 <= X < 240 and 0 <= Y < 160 and base[Y][X] and base[Y][X][0] == "S":
                    img[y][x] = (0, I_COAST); break
    if isinstance(style, Signal):
        style.contour(img, base)
    for a, b, kind in A["links"]:
        style.route(img, a, b, kind)
    for (cx, cy), c in A["cells"].items():
        if c["town"]:
            style.town(img, cx, cy)
    # open sea: an 8x8 tile that is all calm sea moves to row 5 and gets a glyph
    sea_tiles = []
    for ty in range(20):
        for tx in range(30):
            pts = [img[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8)]
            if all(p and p[0] == 0 and p[1] in (I_SEA, I_SEATEX) for p in pts):
                sea_tiles.append((tx, ty))
                v = h(page, tx, ty, "v") % (len(style.glyphs) * 3)
                g = h(page, tx, ty, "g") % 4
                for y in range(8):
                    for x in range(8):
                        img[ty * 8 + y][tx * 8 + x] = (5, 2 if img[ty * 8 + y][tx * 8 + x][1] == I_SEATEX else 1)
                if v < len(style.glyphs):
                    ga, gb = style.glyphs[v]
                    for (x, y) in ga | gb:
                        if x < 8 and y < 8:
                            img[ty * 8 + y][tx * 8 + x] = (5, SEA_AB(g) if (x, y) in ga and (x, y) in gb
                                                           else SEA_A(g) if (x, y) in ga else SEA_B(g))
    return img

def sea_row(style, frame):
    pal = list(style.sea)
    ph = style.phases()[frame]
    for g in range(4):
        s = ph[g]
        pal[SEA_A(g)] = style.on if s == "A" else pal[1]
        pal[SEA_B(g)] = style.on if s == "B" else pal[1]
        pal[SEA_AB(g)] = style.on if s in "AB" else pal[1]
    return pal

def to_rgb(style, img, frame=0, frame_rgb=None):
    out = Image.new("RGB", (240, 160), (0, 0, 0)) if frame_rgb is None else frame_rgb.copy()
    px = out.load(); sea = sea_row(style, frame)
    for y in range(160):
        for x in range(240):
            p = img[y][x]
            if p is None: continue
            if p[0] == "keep":
                c = TODAY_PAL[p[1][0] * 16 + p[1][1]]
                if p[1][0] == 3:   # the switch-map icon, re-inked: ink and paper, no yellow
                    lum = sum(c) / 3
                    c = (30, 26, 36) if lum < 110 else (150, 142, 128) if lum < 200 else (238, 230, 210)
                px[x, y] = c
            elif p[0] == 5: px[x, y] = sea[p[1]]
            else: px[x, y] = style.row0[p[1]]
    return out

def tile_count(imgs):
    seen = set()
    for img in imgs:
        for ty in range(20):
            for tx in range(30):
                t = tuple(tuple((img[ty * 8 + y][tx * 8 + x] or (0, 0))[1] if not (img[ty * 8 + y][tx * 8 + x] or ("", 0))[0] == "keep"
                                else img[ty * 8 + y][tx * 8 + x][1][1] for x in range(8)) for y in range(8))
                if all(v == 0 for r in t for v in r): continue
                vs = [t, tuple(r[::-1] for r in t), t[::-1], tuple(r[::-1] for r in t[::-1])]
                if not any(v in seen for v in vs):
                    seen.add(t)
    return len(seen)

# ---------------------------------------------------------------- the frame, ink and paper
def frame_layer(style):
    """BG1's side panels and the top bar strip redrawn: ink with the direction's motif."""
    im = Image.new("RGB", (240, 160), (0, 0, 0)); px = im.load()
    ink, paper = (30, 26, 36), (238, 230, 210)
    mid = style.row0[I_RTL]
    for y in range(160):
        for x in range(240):
            if 16 <= x < 224 and y >= 16: continue
            px[x, y] = ink
    # the inner edge: a paper rule
    for y in range(15, 160):
        px[15, y] = paper; px[224, y] = paper
    for x in range(15, 225):
        px[x, 15] = paper
    if isinstance(style, Score):
        for side in (2, 228):
            for y in range(24, 152):
                for k in range(5):
                    if (y // 32) % 2 == 0 or True:
                        px[side + 2 * k, y] = mid
            for y in range(24, 152, 16):
                for k in range(9): px[side + k, y] = mid
    elif isinstance(style, Circuit):
        for side in (4, 232):
            for y in range(20, 156):
                px[side, y] = mid; px[side + 3, y] = mid if (y // 12) % 2 else ink
            for y in range(28, 152, 24):
                for dx in range(-2, 6):
                    for dy in range(-1, 2):
                        px[side + dx, y + dy] = mid
                px[side + 1, y] = ink; px[side + 2, y] = ink
    else:
        import math
        for side in (7, 232):
            for y in range(20, 156):
                o = int(round(3 * math.sin(y / 5.0) * math.sin(y / 23.0)))
                px[side + o, y] = mid
    return im


# ---------------------------------------------------------------- the overworld follow-on: a mock only
WD = os.path.join(GBA, "data/tilesets/primary/general")
def water_today(frame):
    im = Image.open(os.path.join(WD, f"anim/water_current_landwatersedge/{frame}.png")); px = im.load()
    pal = [tuple(map(int, l.split())) for l in open(os.path.join(WD, "palettes/04.pal")).read().split("\n")[3:] if l.strip()]
    return [[px[x, y] & 15 for x in range(16)] for y in range(16)], pal

DIG = {"0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
       "n": ["..#", "..#", "..#", "###", "##."], "N": ["..#", "..##", "..#", "###", "##."], " ": []}
def water_block(kind, frame):
    """16x16, the overworld water group's indices only: 6 body, 5 a step lighter, 3 lighter, 1 the speck."""
    b = [[6] * 16 for _ in range(16)]
    # four slots, each with its own schedule, so the repeat is not a grid flipping in unison
    slots = [(1, 1), (9, 3), (4, 9), (12, 11)]
    for si, (x0, y0) in enumerate(slots):
        k = (frame + 3 * si) % 8
        if kind == "bits":
            ch = "0  1  1 "[k] if si % 2 else " 1   0  "[k]
        elif kind == "notes":
            ch = "n N     "[k] if si % 2 else "   n  N "[k]
        else:
            ch = "0  n    "[k] if si % 2 else "    1  N"[k]
        for y, r in enumerate(DIG[ch]):
            for x, c in enumerate(r):
                if c == "#":
                    b[(y0 + y) % 16][(x0 + x) % 16] = 5
    b[(frame * 2 + 7) % 16][(frame * 5 + 2) % 16] = 1
    return b

def water_mock(out):
    rows = [("TODAY (gbawater.py: ripple dashes)", None), ("BITS", "bits"), ("NOTES", "notes"), ("BOTH", "blend")]
    S = 3; W = 4 * (64 * S + 10) + 10
    sheet = Image.new("RGB", (W, len(rows) * (64 * S + 30) + 30), (24, 24, 28))
    label(sheet, "overworld water, 4 of its 8 frames, a 4x4 patch of the open-water group (row 4)", (10, 6))
    for ri, (name, kind) in enumerate(rows):
        y0 = 30 + ri * (64 * S + 30)
        label(sheet, name, (10, y0), (180, 180, 190))
        for fi, f in enumerate((0, 2, 4, 6)):
            blk, pal = water_today(f)
            if kind: blk = water_block(kind, f)
            im = Image.new("RGB", (64, 64)); px = im.load()
            for y in range(64):
                for x in range(64):
                    px[x, y] = pal[blk[y % 16][x % 16]]
            sheet.paste(im.resize((64 * S, 64 * S), Image.NEAREST), (10 + fi * (64 * S + 10), y0 + 20))
    sheet.save(out)

# ---------------------------------------------------------------- sheets
def label(im, text, xy, fill=(255, 255, 255)):
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    except Exception:
        f = ImageFont.load_default()
    d.text(xy, text, fill=fill, font=f)

def mosaic(im, w=2, h=2):
    out = im.copy(); s = im.load(); d = out.load()
    for y in range(16, 160):
        for x in range(16, 224):
            d[x, y] = s[x - (x % w), y - (y % h)]
    return out

def today_frame():
    """BG1's frame as it stands (map_edge.bin over map_edge.png; row 2 is region_map's, darkened as the engine does)."""
    me = Image.open(G + "map_edge.png"); mp = me.getpalette()[:48]
    MP = [tuple(mp[i * 3:i * 3 + 3]) for i in range(16)]
    pal = MP + MP + [tuple(int(c * 95 / 100) for c in TODAY_PAL[32 + i]) for i in range(16)]
    T = tiles("map_edge.png"); d = open(G + "map_edge.bin", "rb").read()
    im = Image.new("RGB", (240, 160)); o = im.load()
    for i in range(600):
        e = struct.unpack_from("<H", d, i * 2)[0]; t, hf, vf, p = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
        if t >= len(T): continue
        for y in range(8):
            for x in range(8):
                c = T[t][7 - y if vf else y][7 - x if hf else x]
                if c and p * 16 + c < len(pal): o[(i % 30) * 8 + x, (i // 30) * 8 + y] = pal[p * 16 + c]
    return im

def today_page(page):
    base = today_frame(); bp = base.load(); tp = today_rgb(page).load(); ix = today_idx(page)
    for y in range(160):
        for x in range(240):
            if ix[y][x]: bp[x, y] = tp[x, y]
    return base

def main():
    styles = [Score(), Circuit(), Signal()]
    analyses = {p: analyse(p) for p in PAGES}
    report = []
    pages_rgb = {}
    for st in styles:
        imgs = []
        fr = frame_layer(st)
        for p in PAGES:
            img = compose(st, p, analyses[p]); imgs.append(img)
            frames = [to_rgb(st, img, f, fr) for f in range(4)]
            key = st.name.split()[0]
            pages_rgb[(key, p)] = frames
            frames[0].save(os.path.join(HERE, f"t449_{key}_{p}.png"))
            frames[0].save(os.path.join(OUT, f"t449_{key}_{p}.png")) if OUT != HERE else None
            frames[0].save(os.path.join(OUT, f"t449_{key}_{p}_anim.gif"), save_all=True,
                           append_images=frames[1:], duration=250, loop=0)
        n = tile_count(imgs)
        report.append(f"{st.name}: {n} unique 8x8 tiles over the four pages (flips folded); "
                      f"BG0 has 512 slots before BG1's char block; vanilla uses 282 of 320")
        # palette files for the draft
        with open(os.path.join(HERE, f"t449_{st.name.split()[0]}_rows.pal"), "w") as f:
            f.write("JASC-PAL\n0100\n32\n")
            for c in st.row0: f.write("%d %d %d\n" % c)
            for c in sea_row(st, 0): f.write("%d %d %d\n" % c)
    # today
    from PIL import ImageDraw
    today = {p: today_page(p) for p in PAGES}
    for p in PAGES: today[p].save(os.path.join(OUT, f"t449_today_{p}.png"))
    # sheets: mainland and islands, today | A | B | C, 1x and 2x
    for name, pages in (("mainland", ["kanto"]), ("islands", ["sevii_123", "sevii_45", "sevii_67"])):
        for scale in (1, 2):
            W = 4 * (240 * scale + 8) + 8; Hh = len(pages) * (160 * scale + 24) + 30
            sheet = Image.new("RGB", (W, Hh), (24, 24, 28))
            for j, head in enumerate(["TODAY", "A  SCORE", "B  CIRCUIT", "C  SIGNAL"]):
                label(sheet, head, (8 + j * (240 * scale + 8), 6))
            for i, p in enumerate(pages):
                y0 = 30 + i * (160 * scale + 24)
                ims = [today[p]] + [pages_rgb[(k, p)][0] for k in ("A", "B", "C")]
                for j, im in enumerate(ims):
                    sheet.paste(im.resize((240 * scale, 160 * scale), Image.NEAREST), (8 + j * (240 * scale + 8), y0))
                label(sheet, p.upper().replace("_", " "), (8, y0 + 160 * scale + 4), (180, 180, 190))
            sheet.save(os.path.join(OUT, f"t449_{name}_{scale}x.png"))
    # mosaic (T-317 clarity): the map at 2x2 and 2x1, as it is shown before understandings arrive
    sheet = Image.new("RGB", (4 * 488 + 8, 3 * 344 + 30), (24, 24, 28))
    for j, (head, src) in enumerate([("TODAY", today["kanto"])] + [(k, pages_rgb[(k, "kanto")][0]) for k in "ABC"]):
        label(sheet, head, (8 + j * 488, 6))
        for i, (w, hh) in enumerate(((2, 2), (2, 1), (1, 1))):
            sheet.paste(mosaic(src, w, hh).resize((480, 320), Image.NEAREST), (8 + j * 488, 30 + i * 344))
            label(sheet, f"mosaic {w}x{hh}" if w * hh > 1 else "sharp", (8 + j * 488, 30 + i * 344 + 322), (180, 180, 190))
    sheet.save(os.path.join(OUT, "t449_mosaic.png"))
    # sea animation strips
    sheet = Image.new("RGB", (4 * 200 + 8, 3 * 220 + 30), (24, 24, 28))
    for i, k in enumerate("ABC"):
        for f in range(4):
            crop = pages_rgb[(k, "sevii_45")][f].crop((24, 24, 120, 120)).resize((192, 192), Image.NEAREST)
            sheet.paste(crop, (8 + f * 200, 30 + i * 220))
            label(sheet, f"{k} frame {f}", (8 + f * 200, 30 + i * 220 + 194), (180, 180, 190))
    label(sheet, "the open sea, four frames of the palette cycle (row 5) -- no tiles change", (8, 6))
    sheet.save(os.path.join(OUT, "t449_sea_frames.png"))
    water_mock(os.path.join(OUT, "t449_water_mock.png"))
    print("\n".join(report))

if __name__ == "__main__":
    main()

# ---------------------------------------------------------------- the GOTO view and the overview
GOTO_ICON = ["................", "................", "....#########...", "....#vvvvvvv#...", "....#######v#...",
             "........#vvv#...", ".......#vv#v#...", "......#vv##v#...", ".....#vv#.#v#...", "....#vv#..###...",
             "...#vv#.........", "..#vv#..........", "..###...........", "................", "................",
             "................"]
CURSOR = ["####......####", "#pp#......#pp#", "#p##......##p#", "##..........##", "..............",
          "..............", "..............", "..............", "..............", "..............",
          "##..........##", "#p##......##p#", "#pp#......#pp#", "####......####"]

def goto_view(src, towns, at):
    im = src.copy(); px = im.load()
    for (cx, cy) in towns:
        x0, y0 = 8 * cx + 36 - 8, 8 * cy + 36 - 8
        for y, r in enumerate(GOTO_ICON):
            for x, ch in enumerate(r):
                if ch == "#": px[x0 + x, y0 + y] = (30, 26, 36)
                elif ch == "v": px[x0 + x, y0 + y] = VECTOR
    x0, y0 = 8 * at[0] + 36 - 7, 8 * at[1] + 36 - 7
    for y, r in enumerate(CURSOR):
        for x, ch in enumerate(r):
            if ch == "#": px[x0 + x, y0 + y] = (30, 26, 36)
            elif ch == "p": px[x0 + x, y0 + y] = (238, 230, 210)
    return im

def plan(out):
    A = analyse("kanto")
    towns = [c for c, v in A["cells"].items() if v["town"]]
    W, H = 4 * 248 + 8, 30 + 2 * 186 + 200 + 260
    sheet = Image.new("RGB", (W, H), (24, 24, 28))
    label(sheet, "T-449 DRAFT -- the TOWN MAP rebranded, same cells.  TODAY | A SCORE | B CIRCUIT | C SIGNAL", (8, 6))
    for i, p in enumerate(("kanto", "sevii_67")):
        for j, k in enumerate(("today", "A", "B", "C")):
            im = Image.open(os.path.join(out, f"t449_{k}_{p}.png") if k != "today" else os.path.join(out, f"t449_today_{p}.png"))
            sheet.paste(im, (8 + j * 248, 30 + i * 186))
    y = 30 + 2 * 186
    label(sheet, "GOTO view (B shown): VECTOR's red only on the GOTO marks; the cursor in ink and paper", (8, y))
    gv = goto_view(Image.open(os.path.join(out, "t449_B_kanto.png")).convert("RGB"), towns, (4, 11))
    sheet.paste(gv.crop((16, 16, 224, 160)).resize((312, 216), Image.NEAREST).crop((0, 0, 312, 180)), (8, y + 18))
    sf = Image.open(os.path.join(out, "t449_sea_frames.png"))
    sheet.paste(sf.resize((sf.width * 180 // sf.height, 180)), (330, y + 20))
    y += 210
    wm = Image.open(os.path.join(out, "t449_water_mock.png"))
    sheet.paste(wm.resize((wm.width * 250 // wm.height, 250)), (8, y))
    notes = ["Limits kept: 22x15 cursor grid, every town/route/island cell unchanged;",
             "BG0 <= 512 tiles (drafts ~310-355); row 0 static, NEW row 5 = open sea,",
             "cycled (no tile changes); coast tiles stay calm (they share row 0).",
             "Only hue: FLOW blue on TRAVERSE lanes; VECTOR red on GOTO marks.",
             "T-317's 2x2 mosaic: lines sit on even pixels so routes survive it.",
             "Overworld water: same 4 indices (6,5,3,1), 8 frames, rows 4 and 6."]
    for i, n in enumerate(notes):
        label(sheet, n, (8 + wm.width * 250 // wm.height + 16, y + 10 + i * 20), (200, 200, 210))
    sheet.save(os.path.join(out, "t449_plan.png"))

if __name__ == "__main__" and len(sys.argv) > 1:
    plan(sys.argv[1])

#!/usr/bin/env python3
"""CHECKPOINTS, THE REPO and the BENCHMARKS, as buildings (T-62, T-63, T-64; vision.md 9.23).

    python3 tools/gbacivic.py            # report and preview to /tmp/civic.png (before | after)
    python3 tools/gbacivic.py --write    # tiles, blocks and palettes across the outdoor tilesets

WHAT EACH BECOMES (9.23): a CHECKPOINT with a calm teal roof and a circular
restore arrow; THE REPO with a golden amber roof and a stacked package; a
BENCHMARK with a slate roof and a gauge. Signs carry the emblem and no letters.

FOUND BY THEIR DOORS, NOT BY BLOCK NUMBERS. Every warp into a Pokemon Center,
Mart or Gym is a building: 17 CHECKPOINTS, 12 REPOs and 8 BENCHMARKs on the
General tileset. Around each door the building sits on the same cells, but a
town may draw an edge, a roof top or a sign with a block of its own. So each
building is stamped from a drawing placed on its door, and every block under it
-- shared or a town's -- has only its building entries redrawn: an entry in
palette row 2, 3 or 5 that draws a tile the vanilla building draws. Grass, the
town's own rows and the door keep what they had.

A BENCHMARK IS DRAWN BY COLUMN, because they are not all one width (six cells at
Callow and Quicksilver, seven at Slate, more at Verdigris) and the same block
stands at a different offset in different towns. Each column is drawn by its
role -- left edge, wall, the plaque and pillars beside the door, the door, right
edge -- so a block always gets the same pixels wherever it stands.

COLOUR. The General palette rows are full. The CHECKPOINT's teal takes three
colours of row 2 that only one Verdigris door block drew (8, 9) or nothing drew
(15), and that door block moves to row 5, whose browns it recolours onto. THE
REPO is drawn in row 5, whose golds were the BENCHMARK roof's and are now the
REPO's alone. The BENCHMARK is row 2's slate greys, its gauge row 5's gold.

TILES. Each drawn tile is de-duplicated and placed in a slot that only these
buildings used, or in one nobody used. A block asked for two different drawings
by two buildings is a conflict and is reported, never guessed.
"""
import importlib.util, json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("gbaemblems", os.path.join(ROOT, "tools", "gbaemblems.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)

GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
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
SIGN_BLOCKS = {352: 0, 360: 1}
# vanilla's CHECKPOINT roof reaches one row up: every town draws that top edge
# with a block of its own, whose top layer draws these four roof tiles in row 2
CHECKPOINT_ROOF_EDGE = {192, 193, 194, 195}                        # the BENCHMARK's free-standing board: top cell, bottom cell
TEAL = {8: (58, 138, 140), 9: (96, 184, 176), 15: (156, 220, 210)}
VERDIGRIS_DOOR = (61, [200, 201, 216, 217])          # moves from row 2 to row 5
ROW2_TO_5 = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 9, 9: 8}

# palette roles
R2 = dict(WHITE=1, PALE=2, LIGHT=3, MID=4, GREY=5, DARK=6, OUT=7, TEALD=8, TEALM=9, TEALL=15)
R5 = dict(WHITE=1, LIGHT=2, GREY=3, DARK=4, OUT=5, GOLDL=6, GOLDM=7, GOLDD=8, AMBERD=9, BRIGHT=10, GOLD2=11, GOLD3=12)


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


# ------------------------------------------------------------------ drawings
def draw_checkpoint():
    """80x64, cells dx -2..+2 by dy -3..0; the door is x 32..47, y 48..63. Row 2."""
    c, r = Canvas(80, 64), 2
    A = R2
    # a hipped teal roof: courses every 8 pixels so the middle of it repeats, and
    # the hips only in the outer cell each side
    for y in range(2, 31):
        c.rect(0, y, 79, y, r, A["TEALM"])
        if y % 8 == 7:
            c.rect(0, y, 79, y, r, A["TEALD"])
        elif y % 8 == 0:
            c.rect(0, y, 79, y, r, A["TEALL"])
    for y in range(2, 31):
        inset = max(0, (30 - y) // 2)
        inset = min(inset, 15)
        for x in range(0, inset):
            c.p[y][x] = None; c.p[y][79 - x] = None
        c.px(inset, y, r, A["OUT"]); c.px(79 - inset, y, r, A["OUT"])
        c.px(inset + 1, y, r, A["TEALL"]); c.px(78 - inset, y, r, A["TEALD"])
    c.rect(16, 1, 63, 1, r, A["OUT"])
    c.rect(0, 29, 79, 30, r, A["TEALD"]); c.rect(0, 31, 79, 31, r, A["OUT"])
    # the walls, in the colour numbers every building shares (1 wall, 2 trim, 3 base)
    c.rect(0, 32, 79, 63, r, 1)
    c.rect(0, 32, 79, 33, r, 2)
    c.rect(0, 59, 79, 62, r, 3); c.rect(0, 63, 79, 63, r, A["OUT"])
    for x0 in (0, 64):                                    # a window in each end cell, the same tiles both sides
        c.rect(x0 + 3, 36, x0 + 12, 46, r, A["OUT"]); c.rect(x0 + 4, 37, x0 + 11, 45, r, A["PALE"])
        c.rect(x0 + 4, 37, x0 + 6, 39, r, 1); c.rect(x0 + 8, 37, x0 + 8, 45, r, A["LIGHT"])
    # the restore arrow over the door, on a teal roundel inside the door's own cell
    c.rect(32, 34, 47, 49, r, A["TEALL"])
    c.stamp(32, 34, E.emblem("CHECKPOINT", {"O": A["OUT"], "L": 1, "M": A["TEALD"]}), r)
    # right of the door, a plate with a checkmark (T-66); the emblem is only over the door
    c.rect(48, 49, 63, 60, r, A["OUT"]); c.rect(49, 50, 62, 59, r, 1)
    for y, line in enumerate(E.CHECK):
        for x, ch in enumerate(line):
            if ch == "1":
                c.rect(51 + x * 2, 50 + y, 52 + x * 2, 50 + y, r, A["TEALD"])
    return c


def draw_repo():
    """64x64, cells dx -2..+1 by dy -3..0; the door is x 32..47, y 48..63. Row 5."""
    c, r = Canvas(64, 64), 5
    A = R5
    for y in range(3, 31):                                # a gabled amber roof
        c.rect(0, y, 63, y, r, A["GOLD2"])
        if (y - 3) % 4 == 3:
            c.rect(1, y, 62, y, r, A["GOLDD"])
        elif (y - 3) % 4 == 0:
            c.rect(1, y, 62, y, r, A["BRIGHT"])
    c.rect(0, 2, 63, 2, r, A["OUT"]); c.rect(0, 3, 0, 31, r, A["OUT"]); c.rect(63, 3, 63, 31, r, A["OUT"])
    c.rect(0, 29, 63, 30, r, A["AMBERD"]); c.rect(0, 31, 63, 31, r, A["OUT"])
    c.rect(0, 32, 63, 63, r, 1); c.rect(0, 32, 63, 33, r, 2)
    c.rect(0, 59, 63, 62, r, 3); c.rect(0, 63, 63, 63, r, A["OUT"])
    for x0 in (0, 48):                                    # a window in each end cell, the same tiles both sides
        c.rect(x0 + 3, 36, x0 + 12, 46, r, A["OUT"]); c.rect(x0 + 4, 37, x0 + 11, 45, r, 2)
        c.rect(x0 + 4, 37, x0 + 6, 39, r, 1); c.rect(x0 + 8, 37, x0 + 8, 45, r, 3)
    c.rect(32, 33, 47, 49, r, A["GOLDL"])
    c.stamp(32, 34, E.emblem("REPO", {"O": A["OUT"], "L": A["BRIGHT"], "M": A["AMBERD"], "T": 1}), r)
    # right of the door, a plate reading REPO (T-66)
    c.rect(48, 50, 63, 58, r, A["AMBERD"]); c.rect(48, 50, 63, 50, r, A["OUT"]); c.rect(48, 58, 63, 58, r, A["OUT"])
    for y, line in enumerate(E.word("REPO")):
        for x, v in enumerate(line):
            if v:
                c.px(48 + 1 + x, 52 + y, r, 1)
    return c


def benchmark_column(role, dy):
    """16x16 of (row, index) for one BENCHMARK cell by its role and row (dy -4..0)."""
    c, r = Canvas(16, 16), 2
    A, B = R2, R5
    if dy <= -2:                                          # the slate roof
        c.rect(0, 0, 15, 15, r, A["MID"])
        for y in range(16):                               # courses every 8, so the roof rows repeat
            if y % 8 == 7:
                c.rect(0, y, 15, y, r, A["DARK"])
            elif y % 8 == 0:
                c.rect(0, y, 15, y, r, A["LIGHT"])
        if dy == -4:
            c.rect(0, 0, 15, 2, r, A["OUT"]); c.rect(0, 3, 15, 4, r, A["PALE"])
        if role == "L":
            c.rect(0, 0, 1, 15, r, A["OUT"]); c.rect(2, 0, 2, 15, r, A["LIGHT"])
        if role == "R":
            c.rect(14, 0, 15, 15, r, A["OUT"]); c.rect(13, 0, 13, 15, r, A["DARK"])
        return c
    if dy == -1:                                          # the eave, and the upper wall
        c.rect(0, 0, 15, 3, r, A["DARK"]); c.rect(0, 4, 15, 4, r, A["OUT"])
        c.rect(0, 5, 15, 15, r, 1); c.rect(0, 5, 15, 5, r, 2)
        if role == "D":                                   # the gauge over the door, in row 5
            c = Canvas(16, 16)
            c.rect(0, 0, 15, 3, 5, B["DARK"]); c.rect(0, 4, 15, 4, 5, B["OUT"])
            c.rect(0, 5, 15, 15, 5, B["WHITE"])
            art = E.emblem("BENCHMARK", {"O": B["OUT"], "W": B["WHITE"], "T": B["GREY"], "N": B["OUT"], "G": B["BRIGHT"], "S": B["LIGHT"]})
            for y in range(11):
                for x in range(16):
                    v = art[y + 2][x]
                    if v:
                        c.px(x, y + 5, 5, v)
            return c
        if role in ("W", "M"):                            # a tall window
            c.rect(4, 7, 11, 15, r, A["OUT"]); c.rect(5, 8, 10, 15, r, A["PALE"]); c.rect(5, 8, 6, 10, r, A["WHITE"])
        if role in ("P", "P'"):                           # a pillar
            x0 = 10 if role == "P" else 1
            c.rect(x0, 5, x0 + 4, 15, r, A["LIGHT"]); c.rect(x0, 5, x0, 15, r, A["MID"]); c.rect(x0 + 4, 5, x0 + 4, 15, r, A["MID"])
        if role == "L":
            c.rect(0, 0, 1, 15, r, A["OUT"])
        if role == "R":
            c.rect(14, 0, 15, 15, r, A["OUT"])
        return c
    # dy 0: the lower wall, the plaque and the pillars' feet
    c.rect(0, 0, 15, 15, r, 1); c.rect(0, 11, 15, 14, r, 3); c.rect(0, 15, 15, 15, r, A["OUT"])
    if role in ("P", "P'"):
        x0 = 10 if role == "P" else 1
        c.rect(x0, 0, x0 + 4, 14, r, A["LIGHT"]); c.rect(x0, 0, x0, 14, r, A["MID"]); c.rect(x0 + 4, 0, x0 + 4, 14, r, A["MID"])
        c.rect(x0 - 1, 12, x0 + 5, 14, r, A["GREY"])
    if role == "P'":                                      # right of the door, a plate reading MARK (T-66)
        c.rect(0, 2, 15, 10, r, A["DARK"]); c.rect(0, 2, 15, 2, r, A["OUT"]); c.rect(0, 10, 15, 10, r, A["OUT"])
        for y, line in enumerate(E.word("MARK")):
            for x, v in enumerate(line):
                if v:
                    c.px(x, 4 + y, r, 1)
    if role == "L":
        c.rect(0, 0, 1, 15, r, A["OUT"])
    if role == "R":
        c.rect(14, 0, 15, 15, r, A["OUT"])
    return c


def benchmark_role(dx, left, right):
    if dx == left:
        return "L"
    if dx == right:
        return "R"
    return {-2: "W", -1: "P", 0: "D", 1: "P'"}.get(dx, "M")


def draw_board():
    """16x32 BENCHMARK board, rows 5: a slate frame, the gauge, two posts."""
    c, r = Canvas(16, 32), 5
    B = R5
    c.rect(0, 2, 15, 20, r, B["OUT"]); c.rect(1, 3, 14, 19, r, B["LIGHT"]); c.rect(2, 4, 13, 18, r, B["WHITE"])
    art = E.emblem("BENCHMARK", {"O": B["OUT"], "W": B["WHITE"], "T": B["GREY"], "N": B["OUT"], "G": B["BRIGHT"], "S": B["LIGHT"]})
    for y in range(1, 14):
        for x in range(1, 15):
            v = art[y][x]
            if v:
                c.px(x, y + 4, r, v)
    for x0 in (3, 11):
        c.rect(x0, 21, x0 + 1, 29, r, B["GREY"]); c.rect(x0 + 1, 21, x0 + 1, 29, r, B["DARK"])
    c.rect(1, 30, 14, 31, r, B["LIGHT"])
    return c


# ------------------------------------------------------------------ main
def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    prim = bytearray(open(os.path.join(PD, "metatiles.bin"), "rb").read())
    ptiles = Image.open(os.path.join(PD, "tiles.png")); ptp = ptiles.load()
    ppal = {n: read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)}
    btiles = {k: {t & 0x3FF for m in v for t in struct.unpack_from("<8H", prim, m * 16)
                  if t & 0x3FF and (t >> 12) & 0xF in BUILDING_ROWS} for k, v in GROUP.items()}
    btiles["CHECKPOINT"] |= CHECKPOINT_ROOF_EDGE

    secs = {}
    def sec(symbol):
        if symbol not in secs:
            d = tdir(symbol, "secondary")
            secs[symbol] = {"dir": d, "meta": bytearray(open(os.path.join(d, "metatiles.bin"), "rb").read())}
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
        if len(rows) > 1:
            conflicts.append(((tileset, m), j, where + " mixes rows %s" % sorted(rows)))
            return
        row = rows.pop() if rows else (e[j] >> 12) & 0xF
        if j < 4 and any(v is None for v in pix):
            fill = min((v[1] for v in pix if v is not None), default=1)
            pix = [v if v is not None else (row, fill) for v in pix]
        want(tileset, m, j, tuple(v[1] if v else 0 for v in pix), row, where)

    cp = draw_checkpoint(); tall = Canvas(80, 80)
    tall.p = [[None] * 80 for _ in range(16)] + cp.p         # the row above the roof, left empty
    CANVAS = {"CHECKPOINT": (tall, -2, -4), "REPO": (draw_repo(), -2, -3)}
    board = draw_board()
    counts = {}
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
    free = sorted(n for n in range(2, 640) if n not in referenced_elsewhere and n not in anim)
    pool = [n for n in free]
    tiles = {}
    distinct = {px for js in wants.values() for px, row in js.values() if any(px)}
    by_kind = {}
    for (ts, m), js in wants.items():
        pass
    print("  distinct tiles wanted: %d; slots available: %d" % (len(distinct), len(pool)))
    for (ts, m), js in wants.items():
        for j, (px, row) in js.items():
            if not any(px):
                tiles[px] = 0                             # nothing drawn: no tile
            elif px not in tiles:
                if not pool:
                    raise SystemExit("  !! out of primary tile slots")
                tiles[px] = pool.pop(0)
    print("  %d blocks redrawn, %d distinct tiles; %d slots were available (only these buildings or nobody used them)"
          % (len(wants), len(tiles), len(free)))

    new_tiles = ptiles.copy(); ntp = new_tiles.load()
    for px, n in tiles.items():
        for i, v in enumerate(px):
            ntp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] = v
    for (ts, m), js in wants.items():
        buf = prim if m < 640 else sec(ts)["meta"]
        k = m if m < 640 else m - 640
        e = list(struct.unpack_from("<8H", buf, k * 16))
        for j, (px, row) in js.items():
            e[j] = tiles[px] | (row << 12)
        struct.pack_into("<8H", buf, k * 16, *e)

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

    # ---------------------------------------------------------------- preview
    def render(l, x0, y0, w, h, prim_meta, prim_tiles, pals_primary, sec_meta):
        sd = tdir(l["secondary_tileset"], "secondary")
        st = Image.open(os.path.join(sd, "tiles.png")); stp = st.load()
        pals = [pals_primary[n] for n in range(7)] + [read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read(); W = l["width"]
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
                        src, jj, hh = (ptp_, i, prim_tiles.height) if i < 640 else (stp, i - 640, st.height)
                        for ty in range(8):
                            for tx in range(8):
                                sy = (jj // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                v = src[(jj % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                                if layer and v == 0:
                                    continue
                                o[(xx - x0) * 16 + (q % 2) * 8 + tx, (yy - y0) * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
        return img
    views = [("LAYOUT_PEWTER_CITY", 8, 10, 26, 18), ("LAYOUT_VIRIDIAN_CITY", 20, 5, 22, 24), ("LAYOUT_SAFFRON_CITY", 16, 5, 36, 36)]
    panels = []
    for lid, x0, y0, w, h in views:
        l = layouts[lid]; sd = tdir(l["secondary_tileset"], "secondary")
        old_sec = open(os.path.join(sd, "metatiles.bin"), "rb").read()
        new_sec = bytes(sec(l["secondary_tileset"])["meta"])
        h = min(h, l["height"] - y0); w = min(w, l["width"] - x0)
        panels.append((render(l, x0, y0, w, h, open(os.path.join(PD, "metatiles.bin"), "rb").read(), ptiles, ppal, old_sec),
                       render(l, x0, y0, w, h, bytes(prim), new_tiles, new_ppal, new_sec)))
    width = max(a.width for a, _ in panels) * 2 + 8
    sheet = Image.new("RGB", (width, sum(a.height for a, _ in panels) + 8 * len(panels)), (30, 30, 30)); yy = 0
    for a, b in panels:
        sheet.paste(a, (0, yy)); sheet.paste(b, (a.width + 8, yy)); yy += a.height + 8
    sheet.save(PREVIEW)
    print("  preview %s (before | after: Slate, Callow, Brazen)" % PREVIEW)

    if WRITE:
        if conflicts:
            raise SystemExit("  refusing to write with conflicts")
        new_tiles.save(os.path.join(PD, "tiles.png"))
        open(os.path.join(PD, "metatiles.bin"), "wb").write(prim)
        for symbol, s in secs.items():
            open(os.path.join(s["dir"], "metatiles.bin"), "wb").write(s["meta"])
        write_pal(os.path.join(PD, "palettes/02.pal"), new_ppal[2])
        print("  written: tiles.png, General metatiles, %d secondary metatile files, palette row 2" % len(secs))


if __name__ == "__main__":
    main()

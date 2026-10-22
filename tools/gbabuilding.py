#!/usr/bin/env python3
"""The interiors: primary/building's furniture and fixtures, redrawn in place in our own hand (T-438 batch D).

    python3 tools/gbabuilding.py                    # report: every drawn tile of primary/building, by object, with
                                                    #   its count, the blocks that place it, how many maps show it
                                                    #   and where a player first meets it
    python3 tools/gbabuilding.py --draft [DIR]      # the redrawn tiles.png (today's palettes), the proposed palettes,
                                                    #   groups.json, and the contact sheets, in DIR
                                                    #   (gfx/drafts/t438/building/); --sheets DIR puts the sheets
                                                    #   elsewhere
    python3 tools/gbabuilding.py --write --approved # into the engine -- NOT YET: batch D is a draft until the user has
                                                    #   seen the sheets; without --approved --write refuses

THE ANSWER IT FOLLOWS (the user, 2026-10-22): "redraw primary/building IN PLACE -- every interior changes at once,
collision never moves, one big contact sheet first". So nothing here moves a block, a layer, a flip, a palette row,
a behaviour or a collision bit, and no map is touched: only the pixels inside tiles change, and every tile keeps its
FOOTPRINT -- a pixel that was transparent (index 0) stays transparent, and one that was drawn stays drawn. Tiles
262..266 hold CHECKPOINT 2F's pots since batch A (gbadoors.py moved them there) and are never touched.

WHAT IS OURS ALREADY. The player's house (gbahouse.py, T-89), the CHECKPOINTs (gbainterior.py, T-103), THE REPO, the
school, the BENCHMARKS and the reading room each have a secondary tileset of their own and draw nothing from this
primary but tile 0 -- the flat colour under everything -- and the CHECKPOINT's pots. So the census's "first seen in
the player's house" is the house LOADING this primary; the first room a player meets that is drawn from it is the
rival's house next door, and then every house, gatehouse, lab, office and mansion in Kanto and the islands.

THE PRIMARY IS A KIT. Its blocks 0x00..0x185 are four house kits, each a floor and a wall in a palette row of its own
-- PARQUET (rows 1/2: the rival's house, the small houses), TILE (row 3: the labs and offices), the ORANGE kit
(row 4: SAFFRON's and LAVENDER's houses) and the PLANK kit (row 5, carpets in row 3: VERMILION, FUCHSIA, the islands)
-- with the same furniture placed over each on the top layer, in row 0. Tiles 256..639 are pieces the secondaries
(SILPH, the MANSION, the labs, the gatehouses) place: statues, maps and paintings, big plants, sofas, counters,
glass cases, machines.

HOW IT IS DRAWN. Each object is a rectangle of tiles.png -- vanilla laid its tiles out as the object stands, so the
TV's four rows of tiles are a column of the sheet and the bookshelf's are a block of it -- and is redrawn whole, in
ROLES (WOODT, WOODF, WOODD, OUT, SCREEN, ...) rather than colours. Each palette row maps the roles onto its own
indices (ROLES), so the drawing is right in today's palettes and in the proposed ones alike. The look is
gbahouse.py's: the camera looks down from the south, so an object shows a lit top face over a darker front; light
from the upper left; timber with grain and boards; bold forms that read at 1x rather than speckle (batch C's third-
pass lesson). Where an object carries meaning in DAEMONS it looks like our world's: the PC is the PORT (a dark
terminal on a desk, as the player's own is), the TV is our set, the bookshelves are full of spines, the counters
are CHECKPOINT-style. Generic pieces stay generic.

PALETTES. --draft draws in today's palettes, and --write would write only tiles. The proposed palettes (PROPOSED:
the mustard woods and lime greens of rows 0..2 moved onto gbahouse.py's timber and greens) are shown as a fourth
panel and listed tile by tile in groups.json -- every tile that draws the index, in that row, anywhere -- for the
user to decide; --write --approved --palettes would write them too.
"""
import collections, glob, importlib.util, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import read_pal, write_pal
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
B = "data/tilesets/primary/building"
PD = os.path.join(GBA, B)
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t438", "building")
KEEP = set(range(262, 267))                  # CHECKPOINT 2F's pots (batch A); never touched

ARGS = sys.argv[1:]
WRITE = "--write" in ARGS


def argval(flag):
    if flag in ARGS:
        i = ARGS.index(flag)
        if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--"):
            return ARGS[i + 1]
        return ""
    return None


DRAFT = argval("--draft")
if DRAFT == "":
    DRAFT = DRAFT_DEFAULT
SHEETS = argval("--sheets") or DRAFT

# the order a player meets the world (T-438's census), by region map section
ORDER = """PALLET_TOWN ROUTE_1 VIRIDIAN_CITY ROUTE_22 ROUTE_2 VIRIDIAN_FOREST PEWTER_CITY ROUTE_3 MT_MOON ROUTE_4
CERULEAN_CITY ROUTE_24 ROUTE_25 ROUTE_5 UNDERGROUND_PATH ROUTE_6 VERMILION_CITY S_S_ANNE ROUTE_11 DIGLETTS_CAVE ROUTE_9
ROUTE_10 ROCK_TUNNEL POWER_PLANT LAVENDER_TOWN ROUTE_8 ROUTE_7 UNDERGROUND_PATH_2 CELADON_CITY ROCKET_HIDEOUT
POKEMON_TOWER SAFFRON_CITY SILPH_CO ROUTE_12 ROUTE_13 ROUTE_14 ROUTE_15 ROUTE_16 ROUTE_17 ROUTE_18 FUCHSIA_CITY
KANTO_SAFARI_ZONE ROUTE_19 ROUTE_20 SEAFOAM_ISLANDS CINNABAR_ISLAND POKEMON_MANSION ROUTE_21 ONE_ISLAND TREASURE_BEACH
KINDLE_ROAD MT_EMBER EMBER_SPA CAPE_BRINK TWO_ISLAND THREE_ISLAND BOND_BRIDGE THREE_ISLE_PORT BERRY_FOREST
THREE_ISLE_PATH ROUTE_23 KANTO_VICTORY_ROAD INDIGO_PLATEAU POKEMON_LEAGUE FOUR_ISLAND ICEFALL_CAVE FIVE_ISLAND
FIVE_ISLE_MEADOW ROCKET_WAREHOUSE MEMORIAL_PILLAR WATER_LABYRINTH RESORT_GORGEOUS LOST_CAVE SIX_ISLAND WATER_PATH
RUIN_VALLEY DOTTED_HOLE GREEN_PATH OUTCAST_ISLAND PATTERN_BUSH ALTERING_CAVE SEVEN_ISLAND CANYON_ENTRANCE
SEVAULT_CANYON TANOBY_RUINS""".split()
RANK = {"MAPSEC_" + m: i for i, m in enumerate(ORDER)}


# ================================================================== reading the engine
def tiles_of(im):
    w, h = im.size
    px = im.tobytes()
    return [[px[(ty * 8 + r) * w + tx * 8 + c] & 15 for r in range(8) for c in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]


def jasc_bytes(b):
    t = b.decode("utf-8", "replace").replace("\r", "").split("\n")
    return [tuple(map(int, l.split()[:3])) for l in t[3:19]]


CUR_IM = Image.open(os.path.join(PD, "tiles.png"))
CUR = tiles_of(CUR_IM)
VAN = tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, B + "/tiles.png", binary=True))))
PALS = [read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(16)]
NT = len(CUR)

HDR = open(os.path.join(GBA, "src/data/tilesets/headers.h")).read()
MTS = open(os.path.join(GBA, "src/data/tilesets/metatiles.h")).read()
BMT = open(os.path.join(PD, "metatiles.bin"), "rb").read()
BAT = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
MB = {int(v, 16): k[3:] for k, v in re.findall(r"#define (MB_\w+) (0x[0-9A-Fa-f]+)",
                                               open(os.path.join(GBA, "include/constants/metatile_behaviors.h")).read())}


def metatiles_dir(symbol):
    body = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % re.escape(symbol), HDR, re.S)
    m = body and re.search(r"\.metatiles = (\w+)", body.group(1))
    md = m and re.search(r"%s\[\] = INCBIN_U16\(\"(data/tilesets/[^\"]+)/metatiles\.bin" % re.escape(m.group(1)), MTS)
    return md and md.group(1)


def behaviour(i):
    return MB.get(struct.unpack_from("<I", BAT, i * 4)[0] & 0x1FF, "?")


def scan():
    """every layout on Building: which of its tiles it draws, through which block, in which row, on which maps"""
    layouts = [l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
               if "id" in l and l.get("primary_tileset") == "gTileset_Building"]
    maps_of, rank = collections.defaultdict(list), {}
    for mj in glob.glob(os.path.join(GBA, "data/maps/*/map.json")):
        d = json.load(open(mj))
        n = os.path.basename(os.path.dirname(mj))
        maps_of[d.get("layout")].append(n)
        rank[n] = (RANK.get(d.get("region_map_section"), 999), n)
    use = collections.defaultdict(lambda: {"draws": 0, "maps": set(), "rows": collections.Counter(),
                                           "blocks": collections.Counter()})
    sec_cache = {}
    for l in layouts:
        maps = maps_of.get(l["id"], [])
        bp = os.path.join(GBA, l.get("blockdata_filepath", ""))
        if not maps or not os.path.exists(bp):
            continue
        s = l.get("secondary_tileset")
        if s not in sec_cache:
            md = metatiles_dir(s)
            sec_cache[s] = open(os.path.join(GBA, md, "metatiles.bin"), "rb").read() if md else b""
        sec = sec_cache[s]
        data = open(bp, "rb").read()
        cells = collections.Counter(struct.unpack_from("<H", data, k)[0] & 0x3FF for k in range(0, len(data) - 1, 2))
        for mid, n in cells.items():
            buf, i, ts = (BMT, mid, "building") if mid < 640 else (sec, mid - 640, s.replace("gTileset_", ""))
            if (i + 1) * 16 > len(buf):
                continue
            for e in struct.unpack_from("<8H", buf, i * 16):
                t = e & 0x3FF
                if t >= 640:
                    continue
                u = use[t]
                u["draws"] += n
                u["maps"].update(maps)
                u["rows"][e >> 12] += n
                u["blocks"][(ts, mid)] += n
    for t, u in use.items():
        u["maps"] = sorted(u["maps"], key=lambda m: rank.get(m, (999, m)))
    RANKS.update(rank)
    return use


RANKS = {}


def home_row(use, t):
    u = use.get(t)
    return u["rows"].most_common(1)[0][0] if u else None


# ================================================================== roles: what each palette row's indices are
#  index -> today's colour is PALS[row][index]; the drawing names roles, each row maps them onto its own indices.
#  1..4 are the same in every row (ink, iron, stone, white) and are never recoloured.
ROLES = {
    0: dict(OUT=1, IRON=2, STONE=3, WHITE=4, WOODD=5, WOODF=6, WOODT=7, BLUE=8, BLUEL=9, PALE=10, GREEN=11,
            GREENL=12, RED=13, REDL=14, GREY=15),
    1: dict(OUT=1, IRON=2, STONE=3, WHITE=4, WALLD=5, WALL=6, SKYL=7, SKY=8, W1=9, W2=10, W3=11, W4=12, W5=13,
            LILAC=14, SKIRT=15),
    2: dict(OUT=1, IRON=2, LILAC=3, WHITE=4, GREEN=5, GOLD=6, AMBER=7, CREAM=8, INK=9, PALE=10, SKYL=11, BLUE=12,
            YEL=13, ORANGE=14, RUST=15),
    3: dict(OUT=1, IRON=2, STONE=3, WHITE=4, AMBER=5, YEL=6, NAVY=7, BLUE=8, BLUEL=9, KHAKI=10, G1=11, G2=12, G3=13,
            GREEN=14, GREENL=15),
    4: dict(OUT=1, IRON=2, STONE=3, WHITE=4, PALE=5, SAGED=6, SAGE=7, TEAL=8, YEL=9, TAN=10, TAND=11, BROWN=12,
            DGREY=13, LIGHT=14, ORANGE=15),
    5: dict(OUT=1, IRON=2, STONE=3, WHITE=4, PALE=5, BLUEGREY=6, W1=8, W2=12, W3=11, W4=10, W5=9, LAV=13, RED=14,
            BLACK=15),
}

#  PROPOSED (never written without --palettes): the mustard woods and the lime greens onto gbahouse.py's timber and
#  greens, the reds onto its quilt and pot, the blues softened -- index -> colour, per row. Nothing else moves.
PROPOSED = {
    0: {5: (128, 86, 54), 6: (176, 122, 76), 7: (214, 166, 112), 8: (74, 104, 130), 9: (150, 186, 204),
        10: (232, 224, 206), 11: (90, 148, 82), 12: (150, 198, 120), 13: (172, 86, 78), 14: (214, 136, 108),
        15: (150, 144, 134)},
    1: {5: (206, 190, 160), 6: (230, 216, 190), 9: (96, 64, 42), 10: (132, 90, 58), 11: (164, 116, 74),
        12: (194, 146, 98), 13: (220, 178, 128), 14: (226, 214, 200), 15: (120, 84, 58)},
    2: {5: (112, 142, 98), 6: (214, 180, 98), 7: (226, 150, 84), 8: (238, 226, 200), 9: (84, 72, 70),
        12: (98, 122, 162), 13: (232, 212, 150), 14: (196, 112, 82), 15: (150, 76, 60)},
}


def palettes(proposed=False):
    out = [list(p) for p in PALS]
    if proposed:
        for row, m in PROPOSED.items():
            for i, c in m.items():
                out[row][i] = c
    return out


# ================================================================== the canvas a group is drawn on
class Canvas:
    """a group's tiles laid out as the object stands, in vanilla's indices: LAYOUT is rows of tile ids (None for a
    hole, (id, 'h') for a tile placed mirrored). Drawing goes through px(), which never paints outside the
    footprint; whatever a painter leaves alone keeps today's index."""

    def __init__(self, layout, row):
        self.layout, self.row = layout, row
        self.R = ROLES[row]
        self.th, self.tw = len(layout), max(len(r) for r in layout)
        self.w, self.h = self.tw * 8, self.th * 8
        self.van = [[0] * self.w for _ in range(self.h)]
        self.hole = [[True] * self.w for _ in range(self.h)]
        for ty, r in enumerate(layout):
            for tx, spec in enumerate(r):
                if spec is None:
                    continue
                t, fl = (spec, "") if isinstance(spec, int) else spec
                for k in range(64):
                    x, y = k % 8, k // 8
                    sx = 7 - x if "h" in fl else x
                    sy = 7 - y if "v" in fl else y
                    self.van[ty * 8 + y][tx * 8 + x] = CUR[t][sy * 8 + sx]
                    self.hole[ty * 8 + y][tx * 8 + x] = False
        self.out = [r[:] for r in self.van]

    def foot(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and not self.hole[y][x] and self.van[y][x] != 0

    def i(self, c):
        return self.R[c] if isinstance(c, str) else c

    def px(self, x, y, c):
        if self.foot(x, y):
            self.out[y][x] = self.i(c)

    def get(self, x, y):
        return self.out[y][x] if 0 <= x < self.w and 0 <= y < self.h else 0

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def fill(self, c):
        self.rect(0, 0, self.w - 1, self.h - 1, c)

    def rim(self, c="OUT"):
        """the footprint's edge, where it meets a transparent pixel (not the canvas edge: the object goes on there)"""
        edge = []
        for y in range(self.h):
            for x in range(self.w):
                if self.foot(x, y) and any(0 <= x + dx < self.w and 0 <= y + dy < self.h and not self.hole[y + dy][x + dx]
                                           and self.van[y + dy][x + dx] == 0
                                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    edge.append((x, y))
        for x, y in edge:
            self.px(x, y, c)

    def where(self, idxs):
        """the pixels whose VANILLA index is one of idxs (roles or numbers)"""
        s = {self.i(c) for c in idxs}
        return [(x, y) for y in range(self.h) for x in range(self.w) if self.foot(x, y) and self.van[y][x] in s]

    def remap(self, m, only=None):
        """vanilla index -> new role, everywhere (or only in the pixels given)"""
        mm = {self.i(a): self.i(b) for a, b in m.items()}
        pts = only if only is not None else [(x, y) for y in range(self.h) for x in range(self.w)]
        for x, y in pts:
            if self.foot(x, y) and self.van[y][x] in mm:
                self.out[y][x] = mm[self.van[y][x]]

    def tiles(self):
        """tile id -> its 64 new indices, unmirrored; the first placement of a tile wins"""
        res = {}
        for ty, r in enumerate(self.layout):
            for tx, spec in enumerate(r):
                if spec is None:
                    continue
                t, fl = (spec, "") if isinstance(spec, int) else spec
                if t in res:
                    continue
                px = [0] * 64
                for y in range(8):
                    for x in range(8):
                        sx = 7 - x if "h" in fl else x
                        sy = 7 - y if "v" in fl else y
                        px[sy * 8 + sx] = self.out[ty * 8 + y][tx * 8 + x]
                res[t] = px
        return res


def rect_layout(t0, w, h, stride=16):
    return [[t0 + y * stride + x for x in range(w)] for y in range(h)]


# ================================================================== drawing helpers
def bbox(K):
    xs = [x for y in range(K.h) for x in range(K.w) if K.foot(x, y)]
    ys = [y for y in range(K.h) for x in range(K.w) if K.foot(x, y)]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, -1, -1)


def depth(K, x, y, cap=6):
    """how far (in pixels, 4-way) this footprint pixel is from a transparent one inside the canvas"""
    if not K.foot(x, y):
        return 0
    for d in range(1, cap + 1):
        for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
            X, Y = x + dx, y + dy
            if 0 <= X < K.w and 0 <= Y < K.h and not K.hole[Y][X] and K.van[Y][X] == 0:
                return d
    return cap + 1


def box(K, x0, y0, x1, y1, top_h, top, front, dark, out="OUT"):
    """gbahouse.py's box: a lit top face, a front face, its right edge and the top's lip in shade, an outline"""
    K.rect(x0, y0, x1, y0 + top_h, top)
    K.rect(x0, y0 + top_h + 1, x1, y1, front)
    K.hline(x0, x1, y0 + top_h + 1, dark)
    K.vline(x1, y0 + top_h + 1, y1, dark)
    if out:
        K.hline(x0, x1, y0, out); K.hline(x0, x1, y1, out); K.vline(x0, y0, y1, out); K.vline(x1, y0, y1, out)


def books(K, x0, y0, x1, y1, seed, cols=("RED", "BLUE", "GREEN", "WOODT", "REDL", "PALE", "BLUEL", "GREENL")):
    """a shelf of spines, x0..x1 wide, standing on y1: two pixels a spine, heights and colours varied, a gap now
    and then, a lit top on each (gbahouse.py's shelf at tile scale)"""
    x, k = x0, seed
    while x <= x1:
        k = (k * 1103515245 + 12345) & 0x7FFFFFFF
        if (k >> 7) % 9 == 0 and x + 2 <= x1:           # a gap, or a book leaning
            x += 2
            continue
        w = 2 if (k >> 11) % 4 else 1
        hgt = (y1 - y0) - (k >> 14) % 3
        c = cols[(k >> 17) % len(cols)]
        for xx in range(x, min(x + w, x1 + 1)):
            K.vline(xx, y1 - hgt + 1, y1, c)
        dim = "STONE" if "STONE" in K.R else "LILAC"
        K.hline(x, min(x + w - 1, x1), y1 - hgt + 1, "WHITE" if c in ("BLUE", "RED", "GREEN", "RUST") else dim)
        x += w + (1 if (k >> 20) % 3 == 0 else 0)


# ================================================================== the painters, one an object
def wall(K, beam, plaster, shade, rail, boards, skirt):
    """a wall two cells tall (four tile rows, each repeated every 8 pixels): a cornice beam, plaster with a shadow
    under the beam, a rail, boards (seam, lit, face) every four pixels, a skirting, the ink line at the floor"""
    for y in range(K.h):
        for x in range(K.w):
            xx = x % 4
            if y < 4:
                c = beam[y]
            elif y < 17:
                c = shade if y in (4, 5) else plaster
            elif y < 19:
                c = rail[y - 17]
            elif y < 28:
                c = boards[0] if xx == 0 else (boards[1] if xx == 1 else boards[2])
                if y == 19:
                    c = boards[0]
            elif y < 31:
                c = skirt[y - 28]
            else:
                c = "OUT"
            K.px(x, y, c)


def p_wall_a(K):
    """the house wall (parquet kit): a timber cornice, plaster, a dado rail, wainscot boards, a skirting"""
    wall(K, ("W2", "W4", "W3", "W1"), "WALL", "WALLD", ("W5", "W2"), ("W2", "W4", "W3"), ("W1", "W2", "W2"))


def p_wall_b(K):
    """the lab wall (tile kit): plaster, a white rail, pale painted panels, a blue skirting"""
    wall(K, ("STONE", "WHITE", "LILAC", "IRON"), "WALL", "WALLD", ("WHITE", "STONE"), ("STONE", "WHITE", "LILAC"),
         ("SKIRT", "SKIRT", "IRON"))


def p_wall_c(K):
    """the sage wall (orange kit): a tan cornice, sage plaster, painted sage boards, a teal skirting"""
    wall(K, ("TAND", "YEL", "TAN", "BROWN"), "SAGE", "SAGED", ("YEL", "TAND"), ("SAGED", "LIGHT", "SAGE"),
         ("TEAL", "TEAL", "DGREY"))


def p_wall_d(K):
    """the grey-blue wall (plank kit): a timber cornice, pale plaster, timber wainscot, a dark skirting"""
    wall(K, ("W2", "W5", "W3", "W1"), "PALE", "BLUEGREY", ("W5", "W2"), ("W2", "W4", "W3"), ("W1", "W2", "W2"))


def p_parquet(K):
    """the floor: long boards eight pixels deep, a dark seam and a lit edge at each, one joint a block on every
    other board (so the boards read long, not as brick), a knot -- the player's house's floor in this row's woods
    (W1 dark .. W5 light). The second block (tiles 5,6,21,22) is vanilla's shadowed floor along a wall: the same
    boards one tone down."""
    for y in range(K.h):
        for x in range(K.w):
            shade = x >= 16
            face, lit, seam, grain = ("W2", "W3", "W1", "W1") if shade else ("W3", "W4", "W1", "W2")
            yy, board = y % 8, (y // 8) % 2
            if yy == 0:
                c = seam
            elif yy == 1:
                c = lit
            else:
                c = face
                if board == 0 and x % 16 == 0:
                    c = seam
                elif board == 0 and x % 16 == 1:
                    c = lit
                elif yy in (4,) and (x * 7 + y * 3 + board * 5) % 11 == 0:
                    c = grain
            K.px(x, y, c)
    K.px(5, 12, "W2"); K.px(6, 12, "W2"); K.px(5, 13, "W1")                # one knot a block


def rug(K, fringe, band, line, field, motif, dot):
    """a woven rug, any size, from its corner, edge and field tiles: a fringe, a band with stitches, a line, then
    the field with a diamond in every tile"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            d = depth(K, x, y)
            if d <= 6:
                c = {1: fringe, 2: band, 3: band, 4: line, 5: field, 6: field}[d]
                if d in (2, 3) and (x + y) % 4 == 0:
                    c = fringe
            else:
                xx, yy = x % 8, y % 8
                m = abs(xx - 3.5) + abs(yy - 3.5)
                c = motif if 2 <= m < 3 else (dot if m < 1 else field)
            K.px(x, y, c)


def p_rug(K):
    """the green rug (parquet kit): rust fringe, cream band, gold line, green field, gold diamonds"""
    rug(K, "RUST", "CREAM", "GOLD", "GREEN", "GOLD", "CREAM")


def p_rug_c(K):
    """the orange rug (orange kit): brown fringe, pale band, yellow line, orange field, tan diamonds"""
    rug(K, "BROWN", "PALE", "YEL", "ORANGE", "TAN", "YEL")


def p_rug_d(K):
    """the blue rug (plank kit): navy fringe, khaki band, amber line, blue field, light-blue diamonds"""
    rug(K, "NAVY", "KHAKI", "AMBER", "BLUE", "BLUEL", "YEL")


def p_plank8(K):
    """a floor of one tile repeated both ways (the plank kit): two boards a tile, four pixels deep, a seam and a lit
    edge, grain -- no joints, since a joint would repeat every eight pixels and read as brick; the second tile of
    the pair is the same floor in the wall's shadow"""
    for y in range(K.h):
        for x in range(K.w):
            shade = x >= 8                                         # the second tile: one tone down
            yy, board = y % 4, (y // 4) % 2
            face, lit, seam = ("W2", "W3", "W1") if shade else ("W3", "W4", "W1")
            c = seam if yy == 0 else (lit if yy == 1 else face)
            if yy == 2 and (x * 5 + y) % 7 == 0:
                c = "W2" if not shade else "W1"
            K.px(x, y, c)


def p_tatami(K):
    """the woven floor (orange kit), chequered: each tile a mat, a bound edge and the weave running across, the
    next mat's weave running down; the lower pair the same in the wall's shadow"""
    for y in range(K.h):
        for x in range(K.w):
            tx, ty = x // 8, y // 8
            xx, yy = x % 8, y % 8
            shade = ty == 1
            field, weave, edge = ("TAN", "TAND", "BROWN") if shade else ("YEL", "TAN", "TAND")
            if xx == 0 or yy == 0:
                c = edge
            elif (yy if tx == 0 else xx) % 2 == 0:
                c = weave
            else:
                c = field
            K.px(x, y, c)


def p_slab(K):
    """the lab floor (tile kit): big pale stone slabs, a grout line, a lit edge; the slabs along a wall (the third
    column) keep vanilla's shadow"""
    for y in range(K.h):
        for x in range(K.w):
            xx, yy = x % 8, y % 8
            if xx == 0 or yy == 0:
                c = "G2"
            elif xx == 1 or yy == 1:
                c = "WHITE"
            else:
                c = "G3"
            if x >= 16 and K.van[y][x] in (K.i("G1"), K.i("STONE"), K.i("G2")):
                c = "G1" if c != "G2" else "STONE"                  # vanilla's shadow under the wall, kept
            K.px(x, y, c)


def p_window_a(K):
    """the window in the wall: a timber frame, glass with a lit corner, a cross mullion, a sill"""
    x0, y0, x1, y1 = bbox(K)
    K.rect(x0, y0, x1, y1, "W2")
    K.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 4, "SKY")
    K.rect(x0 + 2, y0 + 2, x0 + 8, y0 + 4, "SKYL")
    K.px(x0 + 2, y0 + 5, "SKYL")
    mid = (x0 + x1 + 1) // 2
    K.vline(mid, y0 + 2, y1 - 4, "W3"); K.hline(x0 + 2, x1 - 2, (y0 + y1) // 2 - 1, "W3")
    for x in range(x0 + 2, x1 - 1):                               # curtains, tied back
        for y in range(y0 + 2, y1 - 3):
            if x - x0 < 4 - (y - y0) // 5 or x1 - x < 4 - (y - y0) // 5:
                K.px(x, y, "WHITE" if (x + y) % 3 else "LILAC")
    K.hline(x0, x1, y1 - 3, "W5"); K.hline(x0, x1, y1 - 2, "W4"); K.hline(x0, x1, y1 - 1, "W2")
    K.rim()


def p_tv(K):
    """our set: a timber case with a dark screen and a lit glint, a dial column, on a low cabinet with doors"""
    x0, y0, x1, y1 = bbox(K)
    sb = y0 + 20                                                   # where the cabinet starts (tile row 3 = 24)
    box(K, x0, y0, x1, sb, 3, "WOODT", "WOODF", "WOODD")
    K.rect(x0 + 2, y0 + 6, x1 - 5, sb - 2, "OUT")
    K.rect(x0 + 3, y0 + 7, x1 - 6, sb - 3, "BLUE")
    K.rect(x0 + 4, y0 + 8, x0 + 6, y0 + 9, "BLUEL"); K.px(x0 + 4, y0 + 10, "BLUEL")
    K.hline(x0 + 3, x1 - 6, sb - 3, "IRON")
    for y in (y0 + 8, y0 + 11):
        K.px(x1 - 3, y, "STONE"); K.px(x1 - 2, y, "IRON")
    K.hline(x1 - 3, x1 - 2, sb - 4, "RED")
    box(K, x0, sb + 1, x1, y1, 1, "WOODT", "WOODD", "OUT")
    mid = (x0 + x1) // 2
    K.vline(mid, sb + 3, y1 - 1, "OUT")
    K.px(mid - 2, sb + 5, "WOODT"); K.px(mid + 2, sb + 5, "WOODT")
    K.rim()


def p_cabinet(K):
    """a timber hutch: lit top, glazed doors with a glint over a row of drawers, on a plinth"""
    x0, y0, x1, y1 = bbox(K)
    box(K, x0, y0, x1, y1, 7, "WOODT", "WOODF", "WOODD")
    K.hline(x0 + 1, x1 - 1, y0 + 1, "WHITE")
    gy0, gy1 = y0 + 11, y0 + 21
    n = 3
    w = (x1 - x0 - 1) // n
    for k in range(n):
        a, b = x0 + 2 + k * w, x0 + (k + 1) * w - 1
        K.rect(a, gy0, b, gy1, "OUT")
        K.rect(a + 1, gy0 + 1, b - 1, gy1 - 1, "BLUEL")
        K.rect(a + 1, gy0 + 1, b - 1, gy0 + 3, "PALE")
        for j in range(3):
            K.px(a + 2 + j, gy1 - 2 - j, "WHITE")
        K.hline(a + 1, b - 1, gy1 - 1, "BLUE")
    K.hline(x0 + 1, x1 - 1, gy1 + 2, "WOODD")
    for k in range(n):
        a, b = x0 + 2 + k * w, x0 + (k + 1) * w - 1
        K.rect(a, gy1 + 3, b, y1 - 3, "WOODF"); K.hline(a, b, gy1 + 3, "WOODT")
        K.px((a + b) // 2, gy1 + 5, "OUT")
    K.hline(x0 + 1, x1 - 1, y1 - 2, "WOODD")
    K.rim()


def p_bin(K):
    """a wicker basket"""
    x0, y0, x1, y1 = bbox(K)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            K.px(x, y, "WOODT" if (x + (y // 2) * 2) % 4 < 2 else "WOODF")
    K.hline(x0, x1, y0 + 1, "WOODD"); K.hline(x0, x1, y0 + 2, "WOODT")
    K.vline(x1 - 1, y0 + 2, y1 - 1, "WOODD")
    K.rim()


def p_bookshelf(K):
    """two shelves edge to edge, each a timber frame on a dark back, three shelves of spines"""
    x0, y0, x1, y1 = bbox(K)
    for k, (a, b) in enumerate(((x0, x0 + 15), (x0 + 16, x1))):
        box(K, a, y0, b, y1, 2, "WOODT", "WOODD", "WOODD")
        K.vline(a + 1, y0 + 3, y1 - 1, "WOODF"); K.vline(b - 1, y0 + 3, y1 - 1, "WOODD")
        shelves = [y0 + 4, y0 + 13, y0 + 22]
        for j, sy in enumerate(shelves):
            K.rect(a + 2, sy, b - 2, sy + 7, "OUT")
            books(K, a + 2, sy + 1, b - 2, sy + 7, 17 * k + 5 * j + 3)
            K.hline(a + 1, b - 1, sy + 8, "WOODT")
        K.rect(a + 1, y1 - 2, b - 1, y1 - 1, "WOODF")
        K.vline(a, y0, y1, "OUT"); K.vline(b, y0, y1, "OUT"); K.hline(a, b, y1, "OUT"); K.hline(a, b, y0, "OUT")
    K.rim()


def p_dresser(K):
    """a chest of drawers: lit top, three drawers with knobs, short legs"""
    x0, y0, x1, y1 = bbox(K)
    box(K, x0, y0, x1, y1 - 2, 4, "WOODT", "WOODF", "WOODD")
    K.hline(x0 + 1, x1 - 1, y0 + 1, "PALE")
    for y in (y0 + 9, y0 + 14, y0 + 19):
        K.hline(x0 + 1, x1 - 1, y, "WOODD")
        K.px((x0 + x1) // 2, y + 2, "WOODT"); K.px((x0 + x1) // 2 + 1, y + 2, "OUT")
    K.rect(x0, y1 - 1, x0 + 1, y1, "WOODD"); K.rect(x1 - 1, y1 - 1, x1, y1, "WOODD")
    K.rim()


def p_kitchen(K):
    """the kitchen run: a stone worktop with the sink and its tap on the left and two rings on the right, timber
    cupboard doors under it"""
    x0, y0, x1, y1 = bbox(K)
    top_end = y0 + 14
    K.rect(x0, y0, x1, top_end, "STONE"); K.hline(x0, x1, y0 + 1, "WHITE")
    K.hline(x0, x1, top_end, "GREY")
    # the sink
    K.rect(x0 + 3, y0 + 5, x0 + 13, y0 + 12, "OUT"); K.rect(x0 + 4, y0 + 6, x0 + 12, y0 + 11, "IRON")
    K.rect(x0 + 4, y0 + 9, x0 + 12, y0 + 11, "BLUE"); K.hline(x0 + 5, x0 + 8, y0 + 9, "BLUEL")
    K.rect(x0 + 7, y0 + 2, x0 + 8, y0 + 5, "GREY"); K.px(x0 + 7, y0 + 2, "WHITE")
    # the rings
    for cx in (x1 - 12, x1 - 5):
        for dx, dy in ((-2, -1), (-2, 0), (-2, 1), (2, -1), (2, 0), (2, 1), (-1, -2), (0, -2), (1, -2), (-1, 2), (0, 2), (1, 2)):
            K.px(cx + dx, y0 + 8 + dy, "OUT")
        K.px(cx, y0 + 8, "RED")
    # the cupboards
    K.rect(x0, top_end + 1, x1, y1, "WOODF")
    K.hline(x0, x1, top_end + 1, "WOODD")
    w = (x1 - x0 + 1) // 4
    for k in range(4):
        a = x0 + k * w
        K.vline(a, top_end + 2, y1 - 1, "WOODD")
        K.vline(a + 1, top_end + 2, y1 - 1, "WOODT")
        K.px(a + w - 3, top_end + 4, "STONE")
    K.rim()


def p_chair(K):
    """a timber chair side-on, its back on the outer side, a red seat cushion"""
    x0, y0, x1, y1 = bbox(K)
    # back: the right-hand column of the footprint (vanilla's chair faces left)
    K.rect(x0, y0, x1, y1, "WOODF")
    K.rect(x1 - 3, y0, x1, y1 - 3, "WOODF"); K.vline(x1 - 3, y0, y1 - 3, "WOODT"); K.vline(x1, y0, y1, "WOODD")
    K.rect(x0, y0 + 6, x1 - 4, y0 + 10, "RED"); K.hline(x0, x1 - 4, y0 + 6, "REDL"); K.hline(x0, x1 - 4, y0 + 10, "WOODD")
    K.rect(x0, y0 + 11, x1 - 4, y0 + 12, "WOODF"); K.hline(x0, x1, y0 + 12, "WOODD")
    for y in range(y0 + 13, y1 + 1):
        for x in range(x0, x1 + 1):
            if K.foot(x, y):
                K.px(x, y, "WOODD" if x in (x0, x0 + 1, x1 - 1, x1) else "WOODF")
    K.rim()


def p_table_gingham(K):
    """the dining table: a red-and-white check cloth over a timber top, its edge and legs"""
    x0, y0, x1, y1 = bbox(K)
    edge = y1 - 7
    for y in range(y0, edge):
        for x in range(x0, x1 + 1):
            K.px(x, y, "RED" if ((x - x0) // 3 + (y - y0) // 3) % 2 else ("WHITE" if ((x - x0) // 3) % 2 else "REDL"))
    K.hline(x0, x1, edge - 1, "RED")
    K.rect(x0, edge, x1, edge + 2, "WOODT"); K.rect(x0, edge + 3, x1, edge + 4, "WOODF"); K.hline(x0, x1, edge + 5, "OUT")
    for x in (x0 + 1, x0 + 2, x1 - 2, x1 - 1):
        K.vline(x, edge + 5, y1, "WOODD")
    K.rim()


def fronds(K, cx, cy, x0, y0, x1, y1):
    """leaves radiating from (cx, cy): the footprint above it filled green, a lit midrib run out to each tip of the
    footprint's outline, the outline inked -- so the leaves are vanilla's silhouette with our light on them"""
    K.rect(x0, y0, x1, y1, "GREEN")
    tips = []
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if K.foot(x, y) and depth(K, x, y) == 1 and y < cy:
                # a tip: a footprint pixel that sticks out (three of its eight neighbours or fewer are drawn)
                n = sum(K.foot(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
                if n <= 3:
                    tips.append((x, y))
    for tx, ty in tips:
        steps = max(abs(tx - cx), abs(ty - cy), 1)
        for k in range(1, steps):
            x = round(cx + (tx - cx) * k / steps)
            y = round(cy + (ty - cy) * k / steps)
            K.px(x, y, "GREENL")
            if k > steps // 2:
                K.px(x + (1 if tx > cx else -1), y + 1, "WOODD" if y > cy - 3 else "GREEN")
    K.rim()


def p_plant_pot(K):
    """a leafy plant in a terracotta pot: vanilla's leaves lit along their ribs, the pot redrawn"""
    x0, y0, x1, y1 = bbox(K)
    py = y1 - 6
    fronds(K, (x0 + x1) // 2, py, x0, y0, x1, py - 1)
    K.rect(x0 + 2, py, x1 - 2, y1, "RED")
    K.vline(x0 + 3, py + 2, y1 - 1, "REDL"); K.vline(x1 - 3, py + 2, y1 - 1, "WOODD")
    K.hline(x0 + 2, x1 - 2, py, "REDL"); K.hline(x0 + 2, x1 - 2, py + 1, "WOODD")
    K.rim()


def p_mat(K):
    """a doormat: an inked edge, a lit binding, a red field with a lighter panel set in it"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            d = depth(K, x, y)
            K.px(x, y, "OUT" if d == 1 else ("REDL" if d == 2 else ("RED" if d <= 4 else "REDL")))


def p_runner(K):
    """the stair runner (row 2): rust with a cream stripe down each side"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            d = depth(K, x, y)
            K.px(x, y, "INK" if d == 1 else ("CREAM" if d == 3 else ("RUST" if d == 2 else ("ORANGE" if (y % 4) else "RUST"))))


def p_port(K):
    """a PORT terminal on its desk, as the player's own: a slate monitor with a lit prompt, a keyboard, a timber
    desk front"""
    x0, y0, x1, y1 = bbox(K)
    my = y0 + 15
    box(K, x0 + 1, y0, x1 - 1, my, 2, "STONE", "IRON", "OUT")
    K.rect(x0 + 3, y0 + 4, x1 - 3, my - 2, "OUT")
    K.rect(x0 + 4, y0 + 5, x1 - 4, my - 3, "BLUE")
    K.hline(x0 + 5, x0 + 9, y0 + 7, "GREENL"); K.hline(x0 + 5, x0 + 7, y0 + 9, "GREENL"); K.px(x0 + 8, y0 + 9, "WHITE")
    K.rect(x0, my + 1, x1, y1, "WOODF"); K.hline(x0, x1, my + 1, "WOODT")
    K.rect(x0 + 3, my + 2, x1 - 6, my + 4, "PALE"); K.hline(x0 + 3, x1 - 6, my + 5, "STONE")
    K.hline(x0, x1, y1, "OUT")
    K.rim()



def frame(K, d1="OUT", lit="WOODT", face="WOODF", dark="WOODD", width=2):
    """a picture frame round whatever vanilla painted inside it: inked edge, then a timber moulding lit on its
    top and left, shaded on its bottom and right; the picture inside is vanilla's"""
    x0, y0, x1, y1 = bbox(K)
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            d = depth(K, x, y)
            if d == 1:
                K.px(x, y, d1)
            elif d <= 1 + width:
                # which side of the frame: compare distances to the bbox edges
                side = min((x - x0, "l"), (x1 - x, "r"), (y - y0, "t"), (y1 - y, "b"))[1]
                K.px(x, y, lit if side in "lt" else dark if d == 2 else face)
            elif d == 2 + width:
                K.px(x, y, "OUT")


def p_picture(K):
    """a picture on the wall: vanilla's picture, in a timber frame"""
    frame(K)


def p_region_map(K):
    """the region map: parchment in a timber frame, the land kept, the sea a pale wash"""
    K.remap({"BLUEL": "PALE", "WHITE": "PALE", "BLUE": "BLUEL"})
    frame(K, width=1)


def p_notice(K):
    """the notice board (row 2): a cork board in a timber frame, two notes pinned to it"""
    x0, y0, x1, y1 = bbox(K)
    K.rect(x0, y0, x1, y1, "GOLD")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x * 3 + y * 5) % 7 == 0:
                K.px(x, y, "AMBER")
    for nx, ny, w, h in ((x0 + 3, y0 + 4, 7, 8), (x0 + 13, y0 + 6, 9, 7)):
        K.rect(nx, ny, nx + w, ny + h, "CREAM"); K.vline(nx + w, ny, ny + h, "LILAC")
        for yy in range(ny + 3, ny + h, 2):
            K.hline(nx + 1, nx + w - 2, yy, "INK" if yy == ny + 3 else "LILAC")
        K.px(nx + w // 2, ny + 1, "RUST")
    frame(K, d1="OUT", lit="ORANGE", face="RUST", dark="INK", width=1)


def p_big_plant(K):
    """the tall plant (SILPH, the offices): long leaves lit along their ribs, a stone planter"""
    x0, y0, x1, y1 = bbox(K)
    py = y1 - 8
    fronds(K, (x0 + x1) // 2, py, x0, y0, x1, py - 1)
    K.rect(x0 + 3, py, x1 - 3, y1, "STONE"); K.vline(x0 + 3, py, y1, "WHITE"); K.vline(x1 - 3, py, y1, "GREY")
    K.rect(x0 + 2, py, x1 - 2, py + 1, "WHITE"); K.hline(x0 + 2, x1 - 2, py + 2, "GREY")
    for y in (py + 5,):
        K.hline(x0 + 3, x1 - 3, y, "GREY")
    K.rim()


def p_armchair_red(K):
    """the armchair (row 2): gbahouse.py's padded armchair -- a tall back on the outer side, arm rolls, a seat in
    rust and orange"""
    x0, y0, x1, y1 = bbox(K)
    K.rect(x0, y0, x1, y1, "RUST")
    K.rect(x1 - 4, y0, x1, y1 - 4, "ORANGE"); K.hline(x1 - 4, x1, y0, "CREAM"); K.vline(x1, y0, y1 - 4, "RUST")
    K.rect(x0, y0 + 5, x1 - 5, y0 + 9, "ORANGE"); K.hline(x0, x1 - 5, y0 + 5, "CREAM"); K.hline(x0, x1 - 5, y0 + 10, "RUST")
    K.rect(x0 + 1, y0 + 11, x1 - 6, y1 - 4, "ORANGE")
    K.rect(x0, y1 - 3, x1, y1, "INK")
    K.rim()


def p_sofa_blue(K):
    """the lobby armchair (row 1, SILPH): seen side-on, its back down the right, a rolled arm at each end, two seat
    cushions, iron feet"""
    x0, y0, x1, y1 = bbox(K)
    K.rect(x0, y0, x1, y1, "SKY")
    K.rect(x1 - 4, y0, x1, y1 - 3, "SKIRT"); K.vline(x1 - 4, y0, y1 - 3, "SKYL")
    for ay in (y0, y1 - 9):                                      # the arms
        K.rect(x0, ay, x1 - 5, ay + 5, "SKIRT"); K.hline(x0, x1 - 5, ay, "SKYL"); K.hline(x0, x1 - 5, ay + 5, "OUT")
    mid = (y0 + y1 - 3) // 2
    K.hline(x0 + 1, x1 - 5, mid, "SKIRT")
    K.vline(x0 + 1, y0 + 7, y1 - 11, "SKYL")
    K.rect(x0, y1 - 3, x1, y1, "IRON"); K.hline(x0, x1, y1 - 3, "OUT")
    K.rim()


def p_stool(K):
    """a padded stool (SILPH's lobby): a lit cushion top, a button, its side in shade"""
    x0, y0, x1, y1 = bbox(K)
    top, front, dark, lit = (("BLUEL", "BLUE", "OUT", "WHITE") if K.row == 0 else ("YEL", "AMBER", "KHAKI", "WHITE"))
    K.rect(x0, y0, x1, y1, front)
    K.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 9, top); K.hline(x0 + 2, x1 - 2, y0 + 1, lit)
    K.px((x0 + x1) // 2, y0 + 5, front)
    K.hline(x0, x1, y0 + 10, dark); K.vline(x1 - 1, y0 + 11, y1 - 1, dark)
    K.rim()


def p_fridge(K):
    """the fridge (row 2): cream enamel, a freezer door over the main one, a chrome handle on each, a rust kick"""
    x0, y0, x1, y1 = bbox(K)
    box(K, x0, y0, x1, y1, 3, "WHITE", "CREAM", "LILAC")
    K.hline(x0 + 1, x1 - 1, y0 + 12, "INK")
    K.rect(x1 - 4, y0 + 6, x1 - 3, y0 + 10, "IRON"); K.rect(x1 - 4, y0 + 15, x1 - 3, y0 + 22, "IRON")
    K.vline(x0 + 1, y0 + 4, y1 - 4, "PALE")
    K.rect(x0 + 1, y1 - 3, x1 - 1, y1 - 1, "RUST")
    K.rim()


def p_window_big(K):
    """the big window (row 2): a timber frame, sky with a cloud and a lit corner, mullions, the grass outside"""
    x0, y0, x1, y1 = bbox(K)
    K.rect(x0, y0, x1, y1, "GOLD")
    K.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 6, "SKYL")
    K.rect(x0 + 2, y1 - 9, x1 - 2, y1 - 6, "GREEN")
    for cx in (x0 + 8, x0 + 21):
        K.rect(cx, y0 + 5, cx + 5, y0 + 6, "WHITE"); K.rect(cx + 1, y0 + 4, cx + 3, y0 + 4, "WHITE")
    for x in range(x0 + 2, x1 - 1, 8):
        K.vline(x, y0 + 2, y1 - 6, "AMBER")
    K.hline(x0 + 2, x1 - 2, y0 + 12, "AMBER")
    K.rect(x0, y1 - 5, x1, y1 - 3, "CREAM"); K.hline(x0, x1, y1 - 2, "AMBER")
    K.rim()


def p_counter(K):
    """an office counter (row 3): a pale top with a lit lip, a blue panel front with a lit line, a dark kick"""
    x0, y0, x1, y1 = bbox(K)
    top = y0 + 8
    K.rect(x0, y0, x1, top, "G3"); K.hline(x0, x1, y0 + 1, "WHITE"); K.hline(x0, x1, top, "G1")
    K.rect(x0, top + 1, x1, y1, "BLUE"); K.hline(x0, x1, top + 2, "BLUEL")
    for x in range(x0 + 7, x1, 8):
        K.vline(x, top + 3, y1 - 3, "NAVY")
    K.rect(x0, y1 - 2, x1, y1, "NAVY")
    K.rim()


def p_lamp(K):
    """a floor lamp (row 2): a cream shade glowing at its rim, on an iron pole and foot"""
    x0, y0, x1, y1 = bbox(K)
    K.rect(x0, y0, x1, y1, "IRON")
    K.rect(x0 + 1, y0, x1 - 1, y0 + 6, "CREAM"); K.hline(x0 + 1, x1 - 1, y0 + 6, "AMBER"); K.hline(x0 + 2, x1 - 2, y0 + 7, "GOLD")
    K.vline(x0 + 2, y0 + 1, y0 + 5, "WHITE")
    K.rim()


def p_bookshelf_one(K):
    """one tall bookshelf: a timber frame, four shelves of spines"""
    x0, y0, x1, y1 = bbox(K)
    box(K, x0, y0, x1, y1, 2, "WOODT", "WOODD", "WOODD")
    K.vline(x0 + 1, y0 + 3, y1 - 1, "WOODF")
    for j, sy in enumerate((y0 + 4, y0 + 12, y0 + 20)):
        K.rect(x0 + 2, sy, x1 - 2, sy + 6, "OUT")
        books(K, x0 + 2, sy + 1, x1 - 2, sy + 6, 7 * j + 11)
        K.hline(x0 + 1, x1 - 1, sy + 7, "WOODT")
    K.rect(x0 + 1, y1 - 3, x1 - 1, y1 - 1, "WOODF")
    K.rim()


def p_lab_shelves(K):
    """the lab's steel shelving (row 2): two units, white uprights, lilac shelves, files and books"""
    x0, y0, x1, y1 = bbox(K)
    for k, (a, b) in enumerate(((x0, x0 + 15), (x0 + 16, x1))):
        K.rect(a, y0, b, y1, "INK")
        K.vline(a + 1, y0, y1, "WHITE"); K.vline(b - 1, y0, y1, "LILAC")
        K.rect(a, y0, b, y0 + 2, "PALE"); K.hline(a, b, y0 + 3, "LILAC")
        for j, sy in enumerate((y0 + 4, y0 + 13)):
            books(K, a + 2, sy, b - 2, sy + 7, 13 * k + 7 * j + 1,
                  cols=("RUST", "BLUE", "GREEN", "GOLD", "ORANGE", "CREAM", "SKYL"))
            K.hline(a + 1, b - 1, sy + 8, "LILAC")
    K.rim()


def p_desk(K):
    """the lab desks: vanilla's desk, its grey steel turned to timber"""
    K.remap({"IRON": "WOODD", "STONE": "WOODF", "GREY": "WOODF", "WHITE": "WOODT"})


def p_box(K):
    """a cardboard box (row 1): a lit flap top with its seam taped, a shaded front, a label"""
    x0, y0, x1, y1 = bbox(K)
    mid = (x0 + x1 + 1) // 2
    K.rect(x0, y0, x1, y0 + 7, "W5"); K.rect(x0, y0 + 8, x1, y1, "W3")
    K.hline(x0, x1, y0 + 8, "W2"); K.vline(x1, y0 + 8, y1, "W2")
    K.vline(mid, y0, y0 + 7, "W4"); K.vline(mid - 1, y0, y0 + 7, "W4"); K.vline(mid, y0 + 8, y0 + 11, "W4")
    K.rect(x0 + 3, y0 + 10, x0 + 8, y0 + 13, "WHITE"); K.hline(x0 + 4, x0 + 7, y0 + 12, "STONE")
    K.rim()


def p_port_tower(K):
    """the PORT's tower: a slate case, a drive slot, a green light"""
    x0, y0, x1, y1 = bbox(K)
    box(K, x0, y0, x1, y1, 2, "STONE", "IRON", "OUT")
    K.hline(x0 + 2, x1 - 2, y0 + 6, "OUT"); K.px(x1 - 2, y0 + 9, "GREENL"); K.px(x1 - 3, y0 + 9, "GREEN")
    K.rim()


def p_port_big(K):
    """the PORT as a console (row 1, the labs and SILPH 11F): a slate cabinet with its screen and prompt"""
    x0, y0, x1, y1 = bbox(K)
    K.rect(x0, y0, x1, y1, "IRON"); K.rect(x0, y0, x1, y0 + 3, "STONE"); K.hline(x0, x1, y0 + 4, "OUT")
    K.rect(x0 + 2, y0 + 7, x1 - 2, y0 + 18, "OUT"); K.rect(x0 + 3, y0 + 8, x1 - 3, y0 + 17, "SKIRT")
    K.hline(x0 + 4, x0 + 9, y0 + 10, "SKYL"); K.hline(x0 + 4, x0 + 7, y0 + 12, "SKYL"); K.px(x0 + 8, y0 + 12, "WHITE")
    K.rect(x0 + 2, y0 + 21, x1 - 2, y0 + 23, "STONE"); K.hline(x0 + 2, x1 - 2, y0 + 24, "OUT")
    K.rim()


def p_table_blue(K):
    """a small table with a blue check cloth"""
    x0, y0, x1, y1 = bbox(K)
    edge = y1 - 6
    for y in range(y0, edge):
        for x in range(x0, x1 + 1):
            K.px(x, y, "BLUE" if ((x - x0) // 3 + (y - y0) // 3) % 2 else ("WHITE" if ((x - x0) // 3) % 2 else "BLUEL"))
    K.rect(x0, edge, x1, edge + 2, "WOODT"); K.rect(x0, edge + 3, x1, y1, "WOODD")
    K.rim()


def p_table_plain(K):
    """a timber table: the top's boards lit, its edge, its legs"""
    x0, y0, x1, y1 = bbox(K)
    edge = y1 - 6
    for y in range(y0, edge):
        for x in range(x0, x1 + 1):
            K.px(x, y, "WOODD" if (y - y0) % 5 == 4 else ("WOODT" if (y - y0) % 5 == 0 else "WOODF"))
    K.rect(x0, edge, x1, edge + 2, "WOODF"); K.hline(x0, x1, edge, "WOODT"); K.rect(x0, edge + 3, x1, y1, "WOODD")
    K.rim()


def p_glass_table(K):
    """SILPH's glass table (row 1): vanilla's glass, its frame timber"""
    K.remap({"STONE": "W2", "IRON": "W1", "LILAC": "SKYL"})


# ================================================================== the objects
def L(*rows):
    return [list(r) for r in rows]


def H(t):
    return (t, "h")


#  key, title, palette row, layout, painter, what it is. In the order a player meets them (the rival's house first).
GROUPS = [
    ("wall_a", "the house wall (parquet kit)", 1, L([1, 1], [17, 17], [2, 2], [18, 18]), p_wall_a,
     "cornice beam, plaster, dado rail, wainscot boards, skirting"),
    ("parquet", "the parquet floor", 1, L([3, 4, 5, 6], [19, 20, 21, 22]), p_parquet,
     "long boards, a joint a block, as the player's house; the shadowed twin"),
    ("rug", "the rug", 2, L([7, 8, H(7)], [23, 24, H(23)], [(7, "v"), (8, "v"), (7, "hv")]), p_rug,
     "woven: fringe, stitched band, gold line, a diamond a tile"),
    ("window_a", "the window", 1, L([13, H(14), H(13)], [29, H(30), H(29)]), p_window_a,
     "timber frame, cross mullion, tied curtains, sill"),
    ("tv", "the TV", 0, rect_layout(71, 2, 4), p_tv, "our set: timber case, dark screen, dials, on its cabinet"),
    ("cabinet", "the glazed cabinet", 0, rect_layout(68, 3, 4), p_cabinet, "a timber hutch"),
    ("bin", "the bin beside it", 0, L([48], [64]), p_bin, "a wicker basket"),
    ("bookshelf", "the bookshelves", 0, rect_layout(73, 4, 4), p_bookshelf, "timber frames, three shelves of spines"),
    ("dresser", "the dresser", 0, rect_layout(77, 2, 3), p_dresser, "a chest of drawers"),
    ("kitchen", "the kitchen run", 0, rect_layout(128, 4, 3), p_kitchen, "stone worktop, sink, rings, timber doors"),
    ("chair", "the chair", 0, rect_layout(132, 2, 2), p_chair, "timber, a red cushion"),
    ("table_cloth", "the dining table", 0, L([9, 10, H(10), H(9)], [25, 26, H(26), H(25)],
                                             [11, 12, H(12), H(11)], [27, 28, H(28), H(27)]), p_table_gingham,
     "a check cloth on a timber table"),
    ("plant", "the potted plant", 0, L([96, 97], [112, 113], [98, 99], [114, 115]), p_plant_pot,
     "long leaves lit along their ribs, a terracotta pot"),
    ("mat", "the exit mat", 0, L([15, 63, H(63), H(15)], [31, 79, H(79), H(31)]), p_mat, "a woven doormat"),
    ("mat_void", "the exit mat on the void", 0, L([47, 95, H(95), H(47)]), p_mat, "its top edge"),
    ("runner", "the stair runners", 2, L([125, 126, 143, 142], [141, H(141), None, None]), p_runner, "rust runner"),
    ("wall_b", "the lab wall (tile kit)", 1, L([178, 178], [194, 194], [179, 179], [195, 195]), p_wall_b,
     "plaster, white rail, pale panels, blue skirting"),
    ("slab", "the lab floor (tile kit)", 3, L([192, 176, 177], [176, 192, 193]), p_slab,
     "big pale slabs, grout, a lit corner; the wall's shadow kept"),
    ("wall_c", "the sage wall (orange kit)", 4, L([566, 566], [582, 582], [598, 598], [614, 614]), p_wall_c,
     "tan cornice, sage plaster, painted boards, teal skirting"),
    ("tatami", "the woven floor (orange kit)", 4, L([599, 600], [615, 616]), p_tatami,
     "tatami mats, chequered weave; the lower pair in shadow"),
    ("rug_c", "the orange rug", 4, L([567, 568, H(567)], [583, 584, H(583)], [(567, "v"), (568, "v"), (567, "hv")]),
     p_rug_c, "woven, as the green rug"),
    ("wall_d", "the grey-blue wall (plank kit)", 5, L([569, 569], [585, 585], [601, 601], [617, 617]), p_wall_d,
     "timber cornice, pale plaster, timber wainscot"),
    ("plank", "the plank floor", 5, L([594, 595]), p_plank8, "two boards a tile, grain, no joints; its shadowed twin"),
    ("rug_d", "the blue rug", 3, L([570, 571, H(570)], [586, 587, H(586)], [(570, "v"), (571, "v"), (570, "hv")]),
     p_rug_d, "woven, as the green rug"),
    ("window_port", "the small window", 1, L([525, 527], [541, 543]), p_window_a, "as the window"),
    ("window_glass", "the glass panes", 0, L([183, 184], [199, 200]), p_picture, "glass in a timber frame"),
    ("bookshelf_one", "the tall bookshelf", 0, L([560, 561], [576, 577], [592, 593], [608, 609]), p_bookshelf_one,
     "timber, spines"),
    ("armchair", "the armchair", 2, rect_layout(562, 2, 2), p_armchair_red, "padded, rust and orange"),
    ("table_blue", "the small table", 0, L([564, 565, H(565), H(564)], [580, 581, H(581), H(580)]), p_table_blue,
     "a blue check cloth"),
    ("table_plain", "the timber table", 0, L([596, 597, H(597), H(596)], [612, 613, H(613), H(612)]), p_table_plain,
     "boards, an edge, legs"),
    ("fridge", "the fridge", 2, L([426, 427], [442, 443], [428, 429], [444, 445]), p_fridge, "cream enamel, chrome"),
    ("notice", "the notice board", 2, L([496, 497], [498, 499]), p_notice, "cork, two pinned notes"),
    ("region_map", "the region map", 0, L([388, 389, 390, 391], [404, 405, 406, 407]), p_region_map,
     "parchment, a timber frame"),
    ("picture", "the painting", 0, rect_layout(396, 2, 2), p_picture, "a timber frame"),
    ("stool_blue", "the blue stool", 0, rect_layout(392, 2, 2), p_stool, "padded, buttoned"),
    ("stool_yellow", "the yellow stool", 3, rect_layout(394, 2, 2), p_stool, "padded, buttoned"),
    ("picture_big", "the landscape", 0, rect_layout(422, 4, 2), p_picture, "a timber frame"),
    ("poster", "the fan club's poster", 0, rect_layout(299, 2, 2), p_picture, "a timber frame"),
    ("big_plant", "the tall plant", 0, L([382, 383], [398, 399], [414, 415], [430, 431]), p_big_plant,
     "long leaves, a stone planter"),
    ("sofa", "the lobby armchair", 1, rect_layout(386, 2, 4), p_sofa_blue, "upholstered, buttoned"),
    ("glass_table", "the glass table", 1, rect_layout(329, 4, 4), p_glass_table, "its frame timber"),
    ("window_big", "the big window", 2, rect_layout(448, 4, 3), p_window_big, "timber frame, sky, the grass"),
    ("counter", "the office counters", 3, rect_layout(454, 6, 2), p_counter, "CHECKPOINT-style: pale top, blue front"),
    ("lamp", "the lamp", 2, L([460], [476]), p_lamp, "a floor lamp"),
    ("lab_shelves", "the lab shelves", 2, L([137, 138, H(138), H(137)], [153, 154, 139, 140], [169, 170, 155, 156]),
     p_lab_shelves, "steel shelving, files and books"),
    ("lab_desk", "the lab desks", 0, L([166, 167, 168], [164, 165, None]), p_desk, "timber tops"),
    ("box", "the cardboard box", 1, rect_layout(221, 2, 2), p_box, "taped, labelled"),
    ("port_tower", "the PORT's tower", 0, L([226], [242]), p_port_tower, "slate, a green light"),
    ("port_big", "the PORT console", 1, rect_layout(317, 2, 4), p_port_big, "the PC is the PORT"),
    ("port_lab", "the PORT (lab bench)", 0, rect_layout(452, 2, 2), p_port, "the PC is the PORT"),
    ("port_desk", "the PORT (desk)", 0, rect_layout(224, 2, 2), p_port, "the PC is the PORT"),
    ("port_desk2", "the PORT (lab desk)", 0, rect_layout(211, 2, 2), p_port, "the PC is the PORT"),
]


def draft_tiles(proposed=False):
    """the redrawn tile list, and which group drew each tile"""
    new = [t[:] for t in CUR]
    owner = {}
    for key, title, row, layout, paint, note in GROUPS:
        K = Canvas(layout, row)
        paint(K)
        for t, px in K.tiles().items():
            if t in KEEP or t in owner:
                continue
            # the footprint, exactly: transparent stays transparent, drawn stays drawn
            fixed = [(p if p else (CUR[t][k] or 1)) if CUR[t][k] else 0 for k, p in enumerate(px)]
            new[t] = fixed
            owner[t] = key
    return new, owner


# ================================================================== pictures
def tile_img(px, pal, flip=""):
    im = Image.new("RGBA", (8, 8))
    p = im.load()
    for k, v in enumerate(px):
        x, y = k % 8, k // 8
        if "h" in flip:
            x = 7 - x
        if "v" in flip:
            y = 7 - y
        p[x, y] = tuple(pal[v]) + (255,) if v else (0, 0, 0, 0)
    return im


def layout_img(layout, row, tiles, pals, bg=(214, 212, 200)):
    th, tw = len(layout), max(len(r) for r in layout)
    im = Image.new("RGBA", (tw * 8, th * 8), bg + (255,))
    for y in range(th * 8):                                          # a faint check where it is see-through
        for x in range(tw * 8):
            if (x // 4 + y // 4) % 2:
                im.putpixel((x, y), (200, 198, 186, 255))
    for ty, r in enumerate(layout):
        for tx, spec in enumerate(r):
            if spec is None:
                continue
            t, fl = (spec, "") if isinstance(spec, int) else spec
            im.alpha_composite(tile_img(tiles[t], pals[row], fl), (tx * 8, ty * 8))
    return im.convert("RGB")


def font(n):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except OSError:
        return ImageFont.load_default()


#  what the draft leaves as vanilla's drawing, and why (each takes the proposed palette if the user wants it)
LEFT = [
    ("flat", {0, 16, 511}, "a single flat colour (the ground under everything, the void, TRAINER TOWER's roof): "
                           "nothing to redraw"),
    ("stairs", set(range(33, 47)) | set(range(49, 63)) | {65, 66, 67, 80, 81, 82, 83},
     "the stairs and banisters: generic, drawn as vanilla, take the timber in the proposed palette"),
    ("multirow", {324, 325, 326, 340, 341, 342, 356, 357, 358, 370, 371, 372, 373, 374},
     "SILPH's reception desk: drawn in rows 0 AND 1, whose indices mean different colours -- a redraw needs both"),
    ("partition", {171, 172, 180, 181, 187, 188, 196, 197, 247, 248, 249, 250},
     "white partition walls and counter tops seen from above: generic"),
    ("doorway", {522, 523, 524, 538, 539, 540, 554, 555, 556},
     "open doorways (the back rooms): a door frame, batch A's kind"),
    ("league", {256, 257, 272, 273, 288, 289, 304, 305}, "the LEAGUE's statue: batch G, the endgame"),
    ("machines", {159, 175, 191, 207, 189, 190, 205, 206, 203, 204, 219, 220, 235, 236, 223, 239, 251, 252, 253, 254,
                  208, 209, 210, 213, 214, 229, 230, 243, 244, 245, 246, 134, 135, 136, 150, 151, 152, 185, 186, 157,
                  158, 173, 174},
     "the POWER PLANT's and the labs' machines, instruments and benches: the secondaries' own, a second pass"),
    ("silph11", set(range(484, 496)) | set(range(500, 509)) | {461, 462, 463, 477, 478, 479, 493, 494, 495},
     "SILPH 11F's gold stair pieces and the MANSION's striped pieces: drawn with their own tilesets (batch F/G)"),
    ("rest", {270, 271, 286, 287, 302, 303, 319, 335, 351, 367, 365, 366, 368, 420, 421, 436, 437, 432, 433,
              512, 513, 514, 515, 528, 529, 530, 531, 544, 545, 546, 547, 602, 603, 618, 619, 610, 611, 638, 639},
     "the bike shop's racks, the lab lounge's blinds, SILPH 8F's bed, the MANSION's lectern, odd pieces seen once"),
]


# ================================================================== the report
def mapsec_names():
    p = os.path.join(GBA, "src/data/region_map/region_map_sections.json")
    try:
        return {s["id"]: s.get("name", s["id"]) for s in json.load(open(p))["map_sections"]}
    except (OSError, KeyError, ValueError):
        return {}


def summary(use, owner):
    groups = []
    for key, title, row, layout, paint, note in GROUPS:
        ts = sorted({t for t, k in owner.items() if k == key})
        draws = sum(use[t]["draws"] for t in ts if t in use)
        maps = sorted({m for t in ts if t in use for m in use[t]["maps"]})
        first = min((use[t]["maps"][0] for t in ts if t in use and use[t]["maps"]),
                    key=lambda m: RANKS.get(m, (999, m)), default=None)
        groups.append(dict(key=key, title=title, row=row, note=note, tiles=ts, draws=draws, nmaps=len(maps),
                           first=first, maps=maps[:12], blocks=sorted({"%s:%#x" % b for t in ts if t in use
                                                                        for b in use[t]["blocks"]})[:16]))
    left = []
    for key, tiles, why in LEFT:
        ts = sorted(t for t in tiles if t in use and t not in owner)
        left.append(dict(key=key, why=why, tiles=ts, draws=sum(use[t]["draws"] for t in ts)))
    known = set(owner) | {t for _, s, _ in LEFT for t in s} | KEEP
    stray = sorted(t for t in use if t not in known)
    return groups, left, stray


def palette_touch(use, owner):
    """every tile that draws a proposed index in a proposed row: index -> tiles (redrawn or not)"""
    out = {}
    new, _ = draft_tiles()
    for row, m in PROPOSED.items():
        for i in sorted(m):
            ts = sorted(t for t in use if home_row(use, t) == row and i in new[t] and t not in KEEP)
            out["row %d index %d" % (row, i)] = dict(today=PALS[row][i], proposed=m[i], tiles=ts,
                                                     redrawn=[t for t in ts if t in owner],
                                                     vanilla=[t for t in ts if t not in owner])
    return out


def report():
    use = scan()
    new, owner = draft_tiles()
    groups, left, stray = summary(use, owner)
    drawn = [t for t in use if any(CUR[t])]
    total = sum(use[t]["draws"] for t in drawn if t not in (0, 16))
    mine = sum(use[t]["draws"] for t in owner if t in use)
    print("  T-438 batch D: primary/building, %d tiles drawn by %d maps' layouts; %d redrawn here (%d of %d draws "
          "outside the two flat tiles, %.0f%%)" % (len(drawn), len({m for t in use for m in use[t]["maps"]}),
                                                   len(owner), mine, total, 100.0 * mine / max(1, total)))
    print("  the player's house, the CHECKPOINTs, THE REPO, the school and the BENCHMARKS draw only tile 0 and the "
          "pots (262..266): they do not change.\n")
    print("  %-14s %-34s %3s %5s %5s %4s  %s" % ("group", "what", "row", "tiles", "draws", "maps", "first seen"))
    for g in groups:
        print("  %-14s %-34s %3d %5d %5d %4d  %s" % (g["key"], g["title"][:34], g["row"], len(g["tiles"]), g["draws"],
                                                   g["nmaps"], g["first"] or "(no map)"))
    print("\n  left as vanilla's drawing:")
    for l in left:
        if l["tiles"]:
            print("  %-10s %3d tiles %5d draws  %s" % (l["key"], len(l["tiles"]), l["draws"], l["why"]))
    if stray:
        print("  !! drawn and in no group: %s" % stray)
    print("\n  palettes: none written; rows %s proposed (--draft lists every tile each index touches)."
          % ", ".join(map(str, sorted(PROPOSED))))
    return use, new, owner, groups, left, stray


# ================================================================== the rooms, through reviewsheet.py's renderer
ROOMS = [
    ("PalletTown_PlayersHouse_1F", "the player's house 1F (its own tileset: unchanged)"),
    ("PalletTown_PlayersHouse_2F", "the player's house 2F (its own tileset: unchanged)"),
    ("PalletTown_RivalsHouse", "the rival's house, BLANCHE -- the parquet kit"),
    ("ViridianCity_House", "a CALLOW house -- the parquet kit"),
    ("ViridianCity_Mart", "THE REPO (its own tileset: unchanged)"),
    ("Route2_ViridianForest_SouthEntrance", "a gatehouse (its own floor; the plants change)"),
    ("FuchsiaCity_WardensHouse", "a big house: the WARDEN's -- the plank kit, the sage wall"),
    ("SaffronCity_CopycatsHouse_1F", "the orange kit"),
    ("VermilionCity_House1", "the plank kit, the blue rug"),
    ("SixIsland_WaterPath_House2", "an island house: fridge, armchair, tall bookshelf"),
    ("CinnabarIsland_PokemonLab_Entrance", "the tile kit: a lab"),
    ("SilphCo_1F", "an office lobby: stools, the glass table, the tall plants"),
]


def _reviewsheet():
    spec = importlib.util.spec_from_file_location("reviewsheet", os.path.join(ROOT, "tools/reviewsheet.py"))
    R = importlib.util.module_from_spec(spec)
    argv = sys.argv[:]
    spec.loader.exec_module(R)
    sys.argv[:] = argv
    return R


def tiles_png(tiles):
    """tiles.png as the engine keeps it (indexed, its own palette), with these tiles' indices"""
    im = CUR_IM.copy()
    w = im.size[0] // 8
    px = im.load()
    for t, p in enumerate(tiles):
        for k, v in enumerate(p):
            px[(t % w) * 8 + k % 8, (t // w) * 8 + k // 8] = v
    return im


def render_room(R, mapname, tiles, pals):
    """reviewsheet.render with primary/building's tiles and palettes swapped for these"""
    img = tiles_png(tiles)
    real_open, real_pal = R.Image.open, R.C.read_pal
    tp = os.path.realpath(os.path.join(PD, "tiles.png"))

    class Shim:
        new = staticmethod(Image.new)

        @staticmethod
        def open(path, *a, **k):
            return img.copy() if os.path.realpath(path) == tp else real_open(path, *a, **k)

    def pal(path):
        m = re.search(r"palettes/(\d\d)\.pal$", path)
        if m and os.path.realpath(os.path.dirname(os.path.dirname(path))) == os.path.realpath(PD):
            return list(pals[int(m.group(1))])
        return real_pal(path)

    R.Image, R.C.read_pal = Shim, pal
    try:
        return R.render(R.layout_of(mapname))
    finally:
        R.Image, R.C.read_pal = sys.modules["PIL.Image"], real_pal


# ================================================================== the sheets
BG = (250, 249, 245)
INK = (30, 30, 30)
SOFT = (110, 110, 110)


def panel_row(ims, labels, gap=10, top=16):
    w = sum(i.size[0] for i in ims) + gap * (len(ims) - 1)
    h = max(i.size[1] for i in ims) + top
    o = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(o)
    x = 0
    for im, lab in zip(ims, labels):
        o.paste(im, (x, top))
        d.text((x, 1), lab, fill=SOFT, font=font(11))
        x += im.size[0] + gap
    return o


def stack(blocks, title, width=None, gap=18):
    width = width or max(b.size[0] for b in blocks) + 40
    h = 44 + sum(b.size[1] + gap for b in blocks)
    o = Image.new("RGB", (width, h), BG)
    d = ImageDraw.Draw(o)
    d.text((20, 12), title, fill=INK, font=font(15))
    y = 44
    for b in blocks:
        o.paste(b, (20, y))
        y += b.size[1] + gap
    return o


def pack(blocks, title, maxw=1900, gap=18):
    """blocks in rows, left to right, wrapped at maxw"""
    rows, cur, w = [], [], 0
    for b in blocks:
        if cur and w + b.size[0] > maxw - 40:
            rows.append(cur)
            cur, w = [], 0
        cur.append(b)
        w += b.size[0] + gap
    if cur:
        rows.append(cur)
    lines = []
    for r in rows:
        h = max(b.size[1] for b in r)
        line = Image.new("RGB", (sum(b.size[0] + gap for b in r), h), BG)
        x = 0
        for b in r:
            line.paste(b, (x, 0))
            x += b.size[0] + gap
        lines.append(line)
    return stack(lines, title, width=maxw)


def group_block(g, new, pals, ppals, scale=4):
    key, title, row, layout, paint, note = g
    van = VAN
    ims = [layout_img(layout, row, t, p).resize((len(layout[0]) * 8 * scale, len(layout) * 8 * scale), Image.NEAREST)
           for t, p in ((van, pals), (CUR, pals), (new, pals), (new, ppals))]
    body = panel_row(ims, ["pristine", "today", "draft", "draft, proposed palette"])
    o = Image.new("RGB", (body.size[0], body.size[1] + 30), BG)
    d = ImageDraw.Draw(o)
    d.text((0, 0), "%s -- %s (row %d)" % (key, title, row), fill=INK, font=font(13))
    d.text((0, 15), note, fill=SOFT, font=font(11))
    o.paste(body, (0, 30))
    return o


def atlas(tiles, pals, use, scale=2, owner=None):
    """all 640 tiles, each in the palette row that draws it most; redrawn ones outlined"""
    im = Image.new("RGB", (16 * (8 * scale + 1), 40 * (8 * scale + 1)), (60, 60, 60))
    for t in range(NT):
        r = home_row(use, t)
        if r is None or r > 6:
            r = 0
        ti = tile_img(tiles[t], pals[r]).convert("RGBA")
        base = Image.new("RGBA", (8, 8), (214, 212, 200, 255) if t in use else (120, 118, 110, 255))
        base.alpha_composite(ti)
        x, y = (t % 16) * (8 * scale + 1), (t // 16) * (8 * scale + 1)
        im.paste(base.convert("RGB").resize((8 * scale, 8 * scale), Image.NEAREST), (x, y))
    return im


def sheets(use, new, owner, groups, left, outdir):
    os.makedirs(outdir, exist_ok=True)
    pals, ppals = palettes(), palettes(True)
    written = []
    # the overview: the whole primary, pristine | today | draft | proposed, and the key
    ims = [atlas(VAN, pals, use), atlas(CUR, pals, use), atlas(new, pals, use), atlas(new, ppals, use)]
    body = panel_row(ims, ["pristine", "today", "draft", "draft, proposed palette"], gap=16)
    o = Image.new("RGB", (body.size[0] + 560, max(body.size[1] + 60, 420 + 13 * len(groups))), BG)
    d = ImageDraw.Draw(o)
    d.text((20, 12), "T-438 batch D: primary/building redrawn in place (DRAFT) -- every tile in the row that draws "
                     "it most; dim = drawn by no map", fill=INK, font=font(15))
    o.paste(body, (20, 44))
    x, y = body.size[0] + 40, 44
    mine = sum(g["draws"] for g in groups)
    d.text((x, y), "%d tiles redrawn in %d objects" % (len(owner), len(groups)), fill=INK, font=font(13)); y += 18
    d.text((x, y), "%d of the primary's tile draws (outside the flat" % mine, fill=SOFT, font=font(11)); y += 14
    d.text((x, y), "colours) are redrawn; left as vanilla:", fill=SOFT, font=font(11)); y += 18
    for l in left:
        if l["tiles"]:
            d.text((x, y), "%-9s %3d tiles %5d draws" % (l["key"], len(l["tiles"]), l["draws"]), fill=SOFT, font=font(11))
            y += 14
    y += 10
    d.text((x, y), "unchanged rooms: the player's house, the", fill=SOFT, font=font(11)); y += 14
    d.text((x, y), "CHECKPOINTs, THE REPO, the school, the", fill=SOFT, font=font(11)); y += 14
    d.text((x, y), "BENCHMARKS (their own tilesets); 262..266", fill=SOFT, font=font(11)); y += 14
    d.text((x, y), "(CHECKPOINT 2F's pots) kept exactly", fill=SOFT, font=font(11)); y += 22
    for g in groups:
        d.text((x, y), "%-14s %3d tiles %5d draws %3d maps" % (g["key"], len(g["tiles"]), g["draws"], g["nmaps"]),
               fill=INK, font=font(11))
        y += 13
    path = os.path.join(outdir, "t438d_overview.png")
    o.save(path); written.append(path)
    # the objects at 4x, in pages
    blocks = [group_block(g, new, pals, ppals) for g in GROUPS]
    page, pages, h = [], [], 0
    for b in blocks:
        if page and h + b.size[1] > 2200:
            pages.append(page)
            page, h = [], 0
        page.append(b)
        h += b.size[1] // 2 + 20
    if page:
        pages.append(page)
    for n, pg in enumerate(pages, 1):
        path = os.path.join(outdir, "t438d_objects_%d.png" % n)
        pack(pg, "T-438 batch D (DRAFT): the objects at 4x -- page %d of %d" % (n, len(pages))).save(path)
        written.append(path)
    # the rooms at 2x: today | draft | proposed
    R = _reviewsheet()
    names = mapsec_names()
    for k, (m, what) in enumerate(ROOMS, 1):
        try:
            a = render_room(R, m, CUR, pals)
        except (OSError, StopIteration, KeyError) as e:
            print("  !! %s: %s" % (m, e))
            continue
        b = render_room(R, m, new, pals)
        c = render_room(R, m, new, ppals)
        same = list(a.getdata()) == list(b.getdata())
        ims = [i.resize((i.size[0] * 2, i.size[1] * 2), Image.NEAREST) for i in (a, b, c)]
        body = panel_row(ims, ["today", "draft" + (" (identical)" if same else ""), "draft, proposed palette"], gap=16)
        sec = json.load(open(os.path.join(GBA, "data/maps/%s/map.json" % m))).get("region_map_section", "")
        title = "%s -- %s  [%s]" % (m, what, names.get(sec, sec))
        path = os.path.join(outdir, "t438d_room_%02d_%s.png" % (k, m))
        stack([body], "T-438 batch D (DRAFT): " + title).save(path)
        written.append(path)
    return written


def write_draft(use, new, owner, groups, left, stray, outdir):
    os.makedirs(outdir, exist_ok=True)
    tiles_png(new).save(os.path.join(outdir, "tiles.png"))
    pd = os.path.join(outdir, "palettes_proposed")
    os.makedirs(pd, exist_ok=True)
    pp = palettes(True)
    for row in sorted(PROPOSED):
        write_pal(os.path.join(pd, "%02d.pal" % row), pp[row])
    touch = palette_touch(use, owner)
    json.dump(dict(ticket="T-438 batch D", status="DRAFT -- not in the engine", keep=sorted(KEEP),
                   groups=groups, left=left, stray=stray, palette_proposal=touch),
              open(os.path.join(outdir, "groups.json"), "w"), indent=1, default=list)
    return touch


def main():
    if WRITE and "--approved" not in ARGS:
        print("  --write refused: T-438 batch D is a draft until the user has approved its sheets.")
        print("  (When they have: --write --approved writes the redrawn tiles into %s/tiles.png -- only tiles a group"
              " owns, never 262..266 -- and --palettes adds the proposed rows %s.)" % (B, sorted(PROPOSED)))
        return 0
    use, new, owner, groups, left, stray = report()
    if WRITE:
        changed = [t for t in owner if new[t] != CUR[t] and t not in KEEP]
        tiles_png(new).save(os.path.join(PD, "tiles.png"))
        print("  wrote %d tiles into %s/tiles.png" % (len(changed), B))
        if "--palettes" in ARGS:
            pp = palettes(True)
            for row in sorted(PROPOSED):
                write_pal(os.path.join(PD, "palettes/%02d.pal" % row), pp[row])
            print("  wrote palettes %s" % sorted(PROPOSED))
        return 0
    if DRAFT is not None:
        touch = write_draft(use, new, owner, groups, left, stray, DRAFT)
        for k, v in touch.items():
            print("  %-17s %-15s -> %-15s %3d tiles (%d not redrawn)" % (k, v["today"], v["proposed"], len(v["tiles"]),
                                                                      len(v["vanilla"])))
        for p in sheets(use, new, owner, groups, left, SHEETS):
            print("  wrote %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())

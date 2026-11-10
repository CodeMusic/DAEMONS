#!/usr/bin/env python3
"""FOUNDRY CO. and the CORPUS rooms under it: gTileset_SilphCo's office, redrawn in place in our own hand (T-536).

    python3 tools/gbaoffice.py                      # report: every object the office tileset draws, its tiles, its
                                                    #   palette row, how often and on which maps, and the block ids
                                                    #   the engine and the scripts name (they keep their ids)
    python3 tools/gbaoffice.py --draft [DIR]        # three directions (A, B, C) drawn in full: per direction the
                                                    #   tiles.png, rows 07..12 as .pal, the fountain's four frames,
                                                    #   and the contact sheets (gfx/drafts/t536/)
    python3 tools/gbaoffice.py --write --approved --pick X
                                                    # into the engine -- refused unless X is in APPROVED
                                                    #   (the user, 2026-11-09: C, THE FOUNDRY)

WHAT IT REDRAWS. gTileset_SilphCo has its own metatiles but draws with gTilesetTiles_Condominiums and its palettes
(headers.h: "Shared by SilphCo"); gTileset_Condominiums itself is placed by no layout, so the 384 tiles and rows
7..12 are the office's alone. Twenty layouts use it: FOUNDRY CO. 1F..11F and its elevator (SilphCo_*), the CORPUS
HIDEOUT B1F..B4F and its elevator (RocketHideout_*), the CORPUS WAREHOUSE on FIVE ISLAND -- and two that are not
CORPUS's at all, the DEPARTMENT STORE's and TRAINER TOWER's elevators (the same lift car). Everything is redrawn IN
PLACE, the gbabuilding.py way (T-438 batch D): no block, layer, flip, palette row, behaviour or collision bit moves
and no map is touched; only the pixels inside tiles change, and every tile keeps its FOOTPRINT (a transparent pixel
stays transparent, a drawn one stays drawn), so every metatile id the engine or a script names keeps its meaning:
the spin arrows (0x2A0/0x2A1/0x2A8/0x2A9, behaviours SPIN_*; 0x2A8 and 0x2A9 are 0x2A0 and 0x2A1 FLIPPED, so the
arrows are drawn as an up and a left that read right mirrored), the card-key gates the scripts set
(silphco_doors.inc: 0x3B0..0x3C5; the hideout's 0x2C6..0x2D7), the elevator doors (0x2E2, 0x2AB: field_door.c
animates them from graphics/door_anims/silph_co_elevator.png and hideout_elevator.png, which are NOT redrawn here --
gbadoors.py follows once a direction is picked), the lift's moving window (0x2E8..0x2FA, field_specials.c swaps
them), the plastic plants' pots (0x355/0x356, gbaplants.py; 0x300/0x308, daemons_house.c's house plants -- the
plants themselves are primary/building's, already ours), and the lobby's fountain, animated by tileset_anims.c from
anim/fountain/0..3.png onto tiles 336..343.

WHERE THE DESIGN COMES FROM. T-447 drew CORPUS's tower from the outside (gbalandmarks.py, built 2026-10-25): riveted
brass, every amber window lit, one thin red band (his red, never named), and at street level a glass lobby through
which the dark plate cast into the floor shows -- no words on it. So the interior's one fixed point is the plate: in
every direction the lobby's twin fountain (1F only; impassable, so a cordon) becomes the plate cast into the floor,
railed off, and its four animation frames a slow glint across it. Nothing is written anywhere: the reading is the
sign's. The directions differ in what the rest of the building is made of:

  A BRASS AND STONE   the tower continued inside: the lobby's pale stone floor seen through the glass, brass rails
                      and rivets, amber light; the HIDEOUT the same brass unpolished, an undercroft; the WAREHOUSE
                      brass-banded crates. (Brazen is "corporate capture made architecture".)
  B THE FORM          CORPUS requisitions, countersigns, files (1.7): floors ruled like a form (SCORN SOLUTIONS'
                      roof is ruled like one), walls of filing drawers, the warp pads a rubber stamp, the spin arrows
                      routing dockets; the HIDEOUT the ledger under the GAME CORNER (T-427), green baize ruled in
                      columns; the WAREHOUSE tagged totes (the daemons are inventory).
  C THE FOUNDRY       FOUNDRY CO. as it was before CORPUS: the company that made BOXes, in cast iron, bronze and a
                      little furnace glow; tread plates, rivets, the HIDEOUT a casting floor of sand, the WAREHOUSE
                      ingots on pallets. CORPUS shows only by its plastic plants and the red.

HOW IT IS DRAWN. Every used tile belongs to one GROUP: a rectangle of the sheet laid out as the object stands. Objects
(desks, terminals, the BOX apparatus, crates, the couch, boards, gates, pads, arrows) are drawn fresh in ROLES inside
their footprint; vanilla's silhouette sets only where pixels may go. Structural tiles (walls, stairs, partitions,
ledges, the lift's frame) keep vanilla's light-and-shade ZONES as geometry -- which pixels are an edge, a riser, a
shadow -- and every surface inside them is repainted in the direction's material with its own pattern. Rows 7..12
use one role layout in every direction (below), so a tile drawn for row 12 still reads right in the one place row 8
borrows it. Tiles vanilla drew in primary/building's rows 0..2 (a terminal, the warp pad, the lockers and lift door,
the boards, a painting, two plaques) stay in those rows and are drawn in their colours, which this tool never
changes. Each direction needs 0 new tiles and 0 new palette rows: the same 6 secondary rows, recoloured.

Every in-game word: none. This is art.
"""
import collections, glob, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import read_pal, write_pal
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SEC = "data/tilesets/secondary/condominiums"      # the tiles and palettes (shared by SilphCo)
MET = "data/tilesets/secondary/silph_co"          # the metatiles, attributes and the fountain's frames
PRI = "data/tilesets/primary/building"
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t536")
ROWS = range(7, 13)                               # the secondary rows the office owns
#  The user's picks go here ("A", "B" or "C"); --write refuses anything not in it.
APPROVED = {"C"}                                  # the user, 2026-11-09: C The foundry

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


# ============================================================================================ reading the engine
def tiles_of(im):
    w, h = im.size
    px = im.tobytes()
    return [[px[(ty * 8 + r) * w + tx * 8 + c] & 15 for r in range(8) for c in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]


def jasc(text):
    t = text.replace("\r", "").split("\n")
    return [tuple(map(int, l.split()[:3])) for l in t[3:19]]


def van_bytes(rel):
    return daemonslib.upstream(GBA, rel, binary=True)


#  What the painters read is VANILLA's sheet and rows, never today's: once a direction is in the engine, today's IS
#  the redraw, and reading it back would draw over our own work (gbabuilding.py's lesson, 2026-10-23).
VAN = tiles_of(Image.open(io.BytesIO(van_bytes(SEC + "/tiles.png"))))
VPAL = {r: jasc(van_bytes(SEC + "/palettes/%02d.pal" % r).decode()) for r in range(16)}
NT = len(VAN)
PPAL = [read_pal(os.path.join(GBA, PRI, "palettes/%02d.pal" % n)) for n in range(7)]   # primary as it stands (ours)
PTILES = tiles_of(Image.open(os.path.join(GBA, PRI, "tiles.png")))
PMT = open(os.path.join(GBA, PRI, "metatiles.bin"), "rb").read()
SMT = open(os.path.join(GBA, MET, "metatiles.bin"), "rb").read()
SAT = open(os.path.join(GBA, MET, "metatile_attributes.bin"), "rb").read()
NB = len(SMT) // 16
VFRAMES = [tiles_of(Image.open(io.BytesIO(van_bytes(MET + "/anim/fountain/%d.png" % n)))) for n in range(4)]
FOUNTAIN_T0 = 336                                 # tileset_anims.c: TILE_OFFSET_4BPP(976) = secondary tile 336
MB = {int(v, 16): k[3:] for k, v in re.findall(r"#define (MB_\w+) (0x[0-9A-Fa-f]+)",
                                               open(os.path.join(GBA, "include/constants/metatile_behaviors.h")).read())}
LABELS = {int(v, 16): k for k, v in re.findall(r"#define (METATILE_SilphCo_\w+)\s+(0x[0-9A-Fa-f]+)",
                                               open(os.path.join(GBA, "include/constants/metatile_labels.h")).read())}


def entries(m):
    buf, k = (PMT, m) if m < 640 else (SMT, m - 640)
    return struct.unpack_from("<8H", buf, k * 16) if (k + 1) * 16 <= len(buf) else (0,) * 8


def behaviour(m):
    return MB.get(struct.unpack_from("<I", SAT, (m - 640) * 4)[0] & 0x1FF, "?") if m >= 640 else "-"


def layouts():
    L = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    return [l for l in L if l.get("secondary_tileset") == "gTileset_SilphCo"]


def maps_by_layout():
    out = collections.defaultdict(list)
    for mj in glob.glob(os.path.join(GBA, "data/maps/*/map.json")):
        d = json.load(open(mj))
        out[d.get("layout")].append(os.path.basename(os.path.dirname(mj)))
    return out


def named_blocks():
    """block id -> where the engine or a script names it (they must keep their ids and read as what they are)"""
    out = collections.defaultdict(set)
    for b, lab in LABELS.items():
        out[b].add(lab.replace("METATILE_SilphCo_", ""))
    for f in glob.glob(os.path.join(GBA, "data/maps/*/scripts.inc")) + glob.glob(os.path.join(GBA, "data/scripts/*.inc")):
        for lab in set(re.findall(r"METATILE_SilphCo_\w+", open(f).read())):
            v = next((b for b, l in LABELS.items() if l == lab), None)
            if v is not None:
                out[v].add("set by " + os.path.basename(f) if "data/scripts/" in f
                           else "set by " + os.path.basename(os.path.dirname(f)))
    for f in ("src/field_door.c", "src/field_specials.c", "src/daemons_house.c"):
        txt = open(os.path.join(GBA, f)).read()
        for lab in set(re.findall(r"METATILE_SilphCo_\w+", txt)):
            v = next((b for b, l in LABELS.items() if l == lab), None)
            if v is not None:
                out[v].add(os.path.basename(f))
    #  daemons_house.c and gbaplants.py name their pots by number
    for b, why in ((0x300, "daemons_house.c (house plant)"), (0x301, "daemons_house.c (house plant)"),
                   (0x308, "daemons_house.c (house plant)"), (0x309, "daemons_house.c (house plant)"),
                   (0x355, "gbaplants.py (pot)"), (0x356, "gbaplants.py (pot)")):
        out[b].add(why)
    return out


def census():
    """per tile: draws, rows, maps, blocks -- from every map's blocks AND every block a script or the engine places"""
    mbl = maps_by_layout()
    use = collections.defaultdict(lambda: {"n": 0, "rows": collections.Counter(), "maps": set(), "blocks": set()})
    bmaps = collections.defaultdict(set)
    for l in layouts():
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        ms = mbl.get(l["id"], []) or [l["name"].replace("_Layout", "")]
        cells = collections.Counter(struct.unpack_from("<H", bd, k)[0] & 0x3FF for k in range(0, len(bd) - 1, 2))
        for m, n in cells.items():
            if m >= 640:
                bmaps[m].update(ms)
            for e in entries(m):
                t = e & 0x3FF
                if t >= 640:
                    u = use[t - 640]
                    u["n"] += n
                    u["rows"][e >> 12] += n
                    u["maps"].update(ms)
                    u["blocks"].add(m)
    named = named_blocks()
    for m in named:
        if m < 640:
            continue
        for e in entries(m):
            t = e & 0x3FF
            if t >= 640:
                u = use[t - 640]
                u["rows"][e >> 12] += 0 if u["rows"] else 1
                u["blocks"].add(m)
    return use, bmaps, named


# ============================================================================================ the groups
def R(t0, w, h):
    return [[t0 + y * 16 + x for x in range(w)] for y in range(h)]


#  name, layout (rows of sheet tile ids as the object stands; None for a hole), palette row, painter, what it is
GROUPS = [
    ("wall",       R(1, 5, 2),                          12, "zones_wall",  "wall faces and the lift's wall"),
    ("vent",       R(6, 2, 2),                          12, "vent",        "a wall vent"),
    ("partition",  R(8, 8, 2),                          12, "zones_part",  "the HIDEOUT's and WAREHOUSE's low partitions, top and ends"),
    ("hidefloor",  R(32, 5, 2),                         12, "hidefloor",   "the HIDEOUT/WAREHOUSE floor, lit and in a wall's shade"),
    ("stop",       R(37, 2, 2),                          7, "stop",        "the WAREHOUSE's stop square (STOP_SPINNING)"),
    ("arrows",     R(39, 4, 2),                          7, "arrows",      "the spin arrows: up, left (down and right are these flipped)"),
    ("terminal",   R(44, 2, 2),                          0, "terminal",    "a terminal on a desk (COMPUTER)"),
    ("phone",      R(46, 2, 2),                          7, "phone",       "a desk phone (TELEPHONE)"),
    ("stairs",     R(64, 16, 2),                        12, "zones_stair", "the lilac stairs and their banisters"),
    ("ledge",      [[96, 97, 98, 99], [112, 113, 114, 115]], 12, "zones_wall", "the stairwell's ledge and rail ends"),
    ("table",      R(100, 3, 2),                        12, "table",       "a long table (the meeting room's)"),
    ("cabinet",    R(104, 2, 3),                         0, "cabinet",     "a white cabinet: the copier"),
    ("cabside",    [[106], [122]],                      12, "zones_wall",  "the copier's side"),
    ("apparatus",  R(107, 5, 3),                         7, "apparatus",   "FOUNDRY's BOX apparatus (POWER_PLANT_MACHINE)"),
    ("console",    R(156, 4, 2),                         7, "console",     "the apparatus's console"),
    ("lockers",    R(128, 4, 3),                         2, "lockers",     "the lift door (0x2E2, 0x2AB) and a locker"),
    ("desk",       [[132, 133, 134]],                   12, "zones_wall",  "a dark desk's edge"),
    ("trim",       R(148, 4, 2),                        10, "zones_trim",  "the lift window's frame and the counters' rail"),
    ("liftfloor",  [[152, 153], [168, 169]],            10, "liftfloor",   "the lift car's floor"),
    ("liftwin",    R(154, 2, 2),                        10, "zones_shaft", "the lift window: the shaft and a passing floor (field_specials.c)"),
    ("liftwin2",   [[317, 318], [333, 334]],            10, "zones_shaft", "the lift window's other frames (field_specials.c)"),
    ("hgate",      [[188, 189], [204, 205], [190, 191], [206, 207]], 10, "gates", "the HIDEOUT's barrier (0x2C6..0x2D7, set by B1F/B4F)"),
    ("crates",     R(176, 6, 2),                        10, "crates",      "the WAREHOUSE's crates, fronts"),
    ("counters",   R(182, 6, 2),                        10, "zones_trim",  "counters and the lift's control panel"),
    ("couch",      [[208, 209, None], [224, 225, 226], [240, 241, None]], 10, "couch", "the couch (11F, SCORN's office)"),
    ("boards",     R(210, 6, 2),                         2, "boards",      "boards on the wall (BLUEPRINTS)"),
    ("floor",      R(216, 4, 2),                         8, "floor",       "FOUNDRY's floor, lit and in a wall's shade"),
    ("band",       R(220, 2, 2),                         8, "zones_band",  "FOUNDRY's wall, its top and its skirting"),
    ("goldstairs", R(242, 14, 2),                       11, "zones_stair", "the lobby stairs, rail and pillars"),
    ("stairfoot",  [[256], [257]],                      11, "zones_stair", "the lobby stairs' foot"),
    ("gates",      [[272, 273], [288, 289], [274, 275], [290, 291]], 11, "gates",       "the card-key gates, across (0x3B0..0x3B9)"),
    ("gatev",      [[299, 300], [301, 302]],                      11, "gatev",       "the card-key gates, along (0x3C0..0x3C5)"),
    ("notice",     [[276, 277], [292, 293]],            12, "notice",      "a notice on a clipboard"),
    ("notice2",    [[278, 279], [294, 295]],             2, "notice",      "a notice with a seal"),
    ("pillar",     [[280], [296]],                       8, "zones_band",  "a glass pillar"),
    ("pad",        [[281, 282], [297, 298]],             0, "pad",         "the warp pad (REGULAR_WARP)"),
    ("plaque",     [[283, 284]],                        12, "plaque",      "a wall plaque"),
    ("plaque0",    [[285, 286]],                         0, "plaque",      "the lift's floor plaque"),
    ("plateedge",  [[303]],                              9, "plate",       "the plate's field"),
    ("counter",    R(304, 4, 2),                         8, "counter",     "the reception counter"),
    ("picture",    R(308, 2, 2),                         1, "picture",     "a picture (PAINTING)"),
    ("rim",        R(310, 7, 2),                         9, "rim",         "the fountain's rim -> the plate's rail"),
    ("spout",      R(336, 8, 1),                         9, "spout",       "the fountain's spouts (animated) -> the plate's glint"),
    ("cratetop",   R(344, 3, 2),                        10, "cratetop",    "a crate's lid"),
    ("cage",       R(347, 3, 2),                        10, "cage",        "a cage of crates"),
]


# ============================================================================================ roles
#  Rows 7..12 share one role layout in every direction, so a tile reads right in any office row.
SROLE = dict(OUT=1, SHD=2, MID=3, HI=4, WHT=5, FD=6, F=7, FL=8, WD=9, W=10, WL=11, BD=12, B=13, BL=14, X=15)
#  primary/building's rows (gbabuilding.py ROLES), as the office's generic roles: these rows are shared with every
#  house in the game and are never recoloured here, so a tile in them is drawn in what they already hold.
PROLE = {
    0: dict(OUT=1, SHD=2, MID=3, HI=15, WHT=4, FD=5, F=6, FL=7, WD=8, W=9, WL=10, BD=5, B=6, BL=7, X=13, G=11),
    1: dict(OUT=1, SHD=2, MID=3, HI=14, WHT=4, FD=9, F=11, FL=13, WD=5, W=6, WL=4, BD=10, B=12, BL=13, X=15, G=8),
    2: dict(OUT=1, SHD=2, MID=3, HI=10, WHT=4, FD=9, F=8, FL=10, WD=12, W=11, WL=4, BD=15, B=6, BL=13, X=14, G=5),
}
SHADE = {"WHT": "HI", "HI": "MID", "MID": "SHD", "SHD": "OUT", "FL": "F", "F": "FD", "FD": "SHD", "WL": "W",
         "W": "WD", "WD": "SHD", "BL": "B", "B": "BD", "BD": "SHD", "X": "BD", "OUT": "OUT"}


def lum(c):
    return 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def H(x, y, s=0):
    """a fixed hash: the same speckle every run"""
    v = (x * 374761393 + y * 668265263 + s * 2246822519) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return (v ^ (v >> 16)) & 0xFF


# ============================================================================================ the canvas
class Canvas:
    """a group's tiles as the object stands, in vanilla's indices; px() never paints outside the footprint (a pixel
    vanilla left transparent stays transparent) and never paints index 0 into it"""

    def __init__(self, layout, row, S):
        self.layout, self.row, self.S = layout, row, S
        self.R = SROLE if row >= 7 else PROLE[row]
        self.vpal = VPAL[row] if row >= 7 else PPAL[row]
        self.th, self.tw = len(layout), max(len(r) for r in layout)
        self.w, self.h = self.tw * 8, self.th * 8
        self.van = [[0] * self.w for _ in range(self.h)]
        self.hole = [[True] * self.w for _ in range(self.h)]
        for ty, r in enumerate(layout):
            for tx, t in enumerate(r):
                if t is None:
                    continue
                for k in range(64):
                    self.van[ty * 8 + k // 8][tx * 8 + k % 8] = VAN[t][k]
                    self.hole[ty * 8 + k // 8][tx * 8 + k % 8] = False
        self.out = [r[:] for r in self.van]
        self.drawn = [[False] * self.w for _ in range(self.h)]

    def foot(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and not self.hole[y][x] and self.van[y][x] != 0

    def i(self, c):
        return self.R[c] if isinstance(c, str) else c

    def px(self, x, y, c):
        if self.foot(x, y):
            self.out[y][x] = self.i(c)
            self.drawn[y][x] = True

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

    def vl(self, x, y):
        """vanilla's luminance at a pixel (None outside the footprint)"""
        return lum(self.vpal[self.van[y][x]]) if self.foot(x, y) else None

    def edge(self, x, y):
        return self.foot(x, y) and any(0 <= x + dx < self.w and 0 <= y + dy < self.h and not self.hole[y + dy][x + dx]
                                       and self.van[y + dy][x + dx] == 0
                                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    def rim(self, c="OUT"):
        pts = [(x, y) for y in range(self.h) for x in range(self.w) if self.edge(x, y)]
        for x, y in pts:
            self.px(x, y, c)

    def parts(self):
        """the footprint's connected pieces, each as a bbox (x0, y0, x1, y1), largest first"""
        seen, out = set(), []
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in seen or not self.foot(x, y):
                    continue
                st, pts = [(x, y)], []
                seen.add((x, y))
                while st:
                    a, b = st.pop()
                    pts.append((a, b))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        q = (a + dx, b + dy)
                        if q not in seen and self.foot(*q):
                            seen.add(q)
                            st.append(q)
                xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                out.append((min(xs), min(ys), max(xs), max(ys), len(pts)))
        return sorted(out, key=lambda b: -b[4])

    def tiles(self):
        res = {}
        for ty, r in enumerate(self.layout):
            for tx, t in enumerate(r):
                if t is None or t in res:
                    continue
                res[t] = [self.out[ty * 8 + k // 8][tx * 8 + k % 8] for k in range(64)]
        return res


def zones(K, ramp):
    """keep vanilla's light-and-shade ZONES as geometry: each footprint pixel goes to the role for its zone (its
    luminance rank among the colours this group's vanilla pixels use); ramp is darkest-first"""
    ls = sorted({round(K.vl(x, y)) for y in range(K.h) for x in range(K.w) if K.foot(x, y)})
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            v = round(K.vl(x, y))
            k = ls.index(v) * len(ramp) // len(ls)
            K.px(x, y, ramp[min(k, len(ramp) - 1)])


def faces(K, roles):
    return [(x, y) for y in range(K.h) for x in range(K.w) if K.foot(x, y) and K.out[y][x] in {K.i(r) for r in roles}]


# ============================================================================================ painters
def texture(K, S, kind, pts=None, shade=None):
    """the direction's surface pattern on face pixels (zone roles W/WL become the pattern's own)"""
    pts = pts if pts is not None else faces(K, ("W", "WL"))
    pat = S[kind]
    for x, y in pts:
        c = pat(x, y)
        if c:
            K.px(x, y, SHADE[c] if shade and shade(x, y) else c)


def p_zones_wall(K, S):
    zones(K, ["OUT", "SHD", "WD", "W", "WL", "WHT"])
    texture(K, S, "wallpat")


def p_zones_part(K, S):
    zones(K, ["OUT", "SHD", "WD", "W", "WL", "BL"])
    texture(K, S, "partpat")


def p_zones_stair(K, S):
    zones(K, ["OUT", "SHD", "BD", "W", "WL", "WHT"])
    for x, y in faces(K, ("WL",)):
        if y % 4 == 3:
            K.px(x, y, "W")                      # every tread its nosing
    for x, y in faces(K, ("BD",)):
        if (x + y) % 6 == 0:
            K.px(x, y, "B")                      # the rail catches the light


def p_zones_trim(K, S):
    zones(K, ["OUT", "SHD", "WD", "W", "WL", "HI"])
    texture(K, S, "trimpat")


def p_zones_shaft(K, S):
    zones(K, ["OUT", "OUT", "SHD", "BD", "X", "BL"])     # the passing floor is lit amber


def p_zones_band(K, S):
    zones(K, ["OUT", "SHD", "WD", "W", "WL", "WHT"])
    texture(K, S, "bandpat")
    #  vanilla's coloured skirting stripe: the direction's band (A brass, B a red margin rule, C the furnace line)
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y) and 90 < K.vl(x, y) < 175 and K.vpal[K.van[y][x]][0] > K.vpal[K.van[y][x]][1] + 25:
                K.px(x, y, S["skirt"])


def p_floor(K, S, pat="floorpat"):
    """the floor block (left 16x16) and its shaded twin (right); every 16x16 the direction's pattern"""
    f = S[pat]
    for y in range(K.h):
        for x in range(K.w):
            c = f(x % 16, y % 16)
            K.px(x, y, SHADE[c] if x >= 16 else c)


def p_hidefloor(K, S):
    f = S["hidepat"]
    ref = {(x, y): K.vl(x, y) for y in range(16) for x in range(16)}
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            c = f(x % 16, y % 16)
            sh = x >= 16 and K.vl(x, y) < ref[(x % 16, y)] - 12
            K.px(x, y, SHADE[c] if sh else c)


def p_stop(K, S):
    S["stop"](K)


def arrow_up(K, ox, oy, fg, ring):
    """two stacked chevrons pointing up, in a 16x16 at (ox, oy)"""
    for k, cy in enumerate((3, 9)):
        for d in range(6):
            for t in range(2):
                for sx in (-1, 1):
                    x = ox + 7 + (sx * d if sx > 0 else -d) + (1 if sx > 0 else 0)
                    y = oy + cy + d + t
                    K.px(x, y, fg)
                    K.px(x, y + 2, ring) if t == 1 and d < 5 else None


def p_arrows(K, S):
    S["arrowground"](K)
    fg, ring = S["arrowfg"], S["arrowring"]
    #  UP in the left 16x16 (39,40/55,56)
    for cy in (2, 8):
        for d in range(6):
            for t in range(3):
                for x in (7 - d, 8 + d):
                    K.px(x, cy + d + t, ring if t == 2 else fg)
    #  LEFT in the right 16x16 (41,42/57,58): the same, turned
    for cx in (18, 24):
        for d in range(6):
            for t in range(3):
                for y in (7 - d, 8 + d):
                    K.px(cx + d + t, y, ring if t == 2 else fg)


def p_terminal(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, "MID")
        K.rect(x0, y1 - 3, x1, y1, "SHD")                  # the desk's front
        K.hline(x0, x1, y1 - 4, "HI")
        sx0, sx1, sy0, sy1 = x0 + 2, x1 - 2, y0 + 2, y1 - 7
        K.rect(sx0, sy0, sx1, sy1, "OUT")                  # the screen
        for yy in range(sy0 + 1, sy1, 2):
            K.hline(sx0 + 1, sx0 + 1 + (H(yy, sx0, 3) % max(1, sx1 - sx0 - 2)), yy, "WD")
        K.px(sx0 + 1, sy0 + 1, "WL")
    K.rim()


def p_phone(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, S["phone"])
        K.rect(x0, y0, x1, y0 + 3, "OUT")                  # the handset
        K.hline(x0 + 1, x1 - 1, y0 + 1, "SHD")
        for yy in range(y0 + 6, y1 - 1, 2):
            for xx in range(x0 + 3, x1 - 2, 2):
                K.px(xx, yy, "WHT")
        K.px(x1 - 2, y0 + 5, "X")                          # a line waiting
    K.rim()


def p_vent(K, S):
    K.fill("W")
    K.rect(2, 2, K.w - 3, K.h - 3, "SHD")
    for y in range(3, K.h - 3, 2):
        K.hline(3, K.w - 4, y, S["ventslat"])
    K.rim("OUT")


def p_table(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, S["tabletop"])
        K.rect(x0, y1 - 2, x1, y1, "SHD")
        K.hline(x0, x1, y0, S["tableedge"])
        K.hline(x0, x1, y1 - 3, S["tableedge"])
        S["tablemotif"](K, x0, y0, x1, y1)
    K.rim()


def p_cabinet(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, "WHT")
        K.rect(x0, y0, x1, y0 + 4, "HI")                   # its lid, seen from above
        K.hline(x0, x1, y0 + 5, "MID")
        for yy in range(y0 + 9, y1 - 1, 5):                # its trays
            K.hline(x0 + 2, x1 - 2, yy, "MID")
            K.px((x0 + x1) // 2, yy + 2, "SHD")
        K.px(x1 - 3, y0 + 2, "G")
        K.hline(x0, x1, y1, "SHD")
    K.rim()


def p_apparatus(K, S):
    """FOUNDRY's BOX apparatus: a press on a plinth, a BOX held closed in its jaws, a lamp -- the ROOTBOX project
    (7F: 'the ultimate BOX which would bind anything'), drawn as a machine and nothing more"""
    for (x0, y0, x1, y1, n) in K.parts()[:2]:
        cx = (x0 + x1) // 2
        K.rect(x0, y0, x1, y1, S["machine"])
        K.rect(x0, y1 - 5, x1, y1, "WD")                   # the plinth
        K.hline(x0, x1, y1 - 6, "WL")
        K.rect(x0 + 2, y0, x0 + 4, y1 - 6, "WD")           # the press's two columns
        K.rect(x1 - 4, y0, x1 - 2, y1 - 6, "WD")
        K.rect(x0 + 2, y0, x1 - 2, y0 + 3, "WD")           # its head
        K.hline(x0 + 2, x1 - 2, y0, "WL")
        by = (y0 + y1) // 2
        K.rect(cx - 4, by - 4, cx + 4, by + 3, S["boxc"])  # the BOX in the jaws
        K.hline(cx - 4, cx + 4, by - 4, "WHT")
        K.rect(cx - 4, by, cx + 4, by, "OUT")              # its seam, shut
        K.px(cx, by + 1, "X")
        K.rect(cx - 1, y0 + 4, cx + 1, by - 5, "SHD")      # the ram
        K.px(x1 - 3, y1 - 3, "X")
        K.px(x0 + 3, y1 - 3, "BL")
    K.rim()


def p_console(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:2]:
        K.rect(x0, y0, x1, y1, S["machine"])
        K.rect(x0, y0, x1, y0 + 3, "WL")
        K.rect(x0 + 2, y0 + 5, x1 - 2, y1 - 4, "OUT")
        for xx in range(x0 + 3, x1 - 2, 3):
            K.px(xx, y0 + 7, "X" if H(xx, y0, 5) % 3 else "BL")
        K.hline(x0 + 3, x1 - 3, y1 - 6, "SHD")
        K.hline(x0, x1, y1, "WD")
    K.rim()


def p_lockers(K, S):
    """rows 128..131 the tops, 144..147/160..163 below: the lift door (144,145/160,161) and a locker"""
    #  the lift door: two leaves meeting in the middle, a frame in the row's gold, a call light
    K.rect(0, 8, 15, 23, "MID")                         # steel leaves, not glass: it is a door
    K.rect(1, 9, 14, 23, "HI")
    K.vline(7, 9, 23, "OUT")
    K.vline(8, 9, 23, "WHT")
    K.hline(1, 14, 9, "WHT")
    for x in (0, 15):
        K.vline(x, 8, 23, "B")
    K.hline(0, 15, 8, "B")
    K.px(3, 15, "BL")
    K.px(12, 15, "BL")
    #  the locker: a column of drawers
    K.rect(16, 8, 31, 23, "MID")
    K.rect(17, 9, 30, 23, "HI")
    for yy in (13, 18, 23):
        K.hline(17, 30, yy, "MID")
    for yy in (11, 16, 21):
        K.hline(22, 25, yy, "SHD")
    #  their tops
    K.rect(0, 0, 31, 7, "HI")
    K.hline(0, 31, 7, "MID")
    K.hline(0, 31, 0, "WHT")
    K.rim()


def p_couch(K, S):
    """the couch: the only red in the room is his"""
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, "X")
        K.rect(x0, y0, x1, y0 + 6, "BD")                   # the back, in shade
        K.hline(x0 + 1, x1 - 1, y0 + 1, "X")
        K.rect(x0, y0 + 7, x0 + 3, y1, "BD")               # the arms
        K.rect(x1 - 3, y0 + 7, x1, y1, "BD")
        mid = (x0 + x1) // 2
        K.vline(mid, y0 + 8, y1 - 3, "BD")                 # two cushions
        K.hline(x0 + 4, x1 - 4, y0 + 8, "WL")
        K.rect(x0, y1 - 2, x1, y1, "SHD")
    K.rim()


def p_boards(K, S):
    """boards on the wall: a BOX drawn as a schematic -- a cube in thin ink, its lid's hinge, a dimension line"""
    for (x0, y0, x1, y1, n) in K.parts():
        if n < 20:
            continue
        K.rect(x0, y0, x1, y1, "WHT")
        K.rect(x0, y0, x1, y0, "MID")
        K.rect(x0, y1, x1, y1, "MID")
        w, h = x1 - x0, y1 - y0
        s = max(3, min(w, h) // 3)
        cx, cy = x0 + w // 3, y0 + h // 2
        ink = "WD"
        for a, b in ((0, 0), (s, 0), (0, s), (s, s)):
            pass
        K.hline(cx - s // 2, cx + s // 2, cy - s // 2, ink)
        K.hline(cx - s // 2, cx + s // 2, cy + s // 2, ink)
        K.vline(cx - s // 2, cy - s // 2, cy + s // 2, ink)
        K.vline(cx + s // 2, cy - s // 2, cy + s // 2, ink)
        for d in range(3):                                 # the cube's depth
            K.px(cx - s // 2 + d + 1, cy - s // 2 - d - 1, ink)
            K.px(cx + s // 2 + d + 1, cy - s // 2 - d - 1, ink)
            K.px(cx + s // 2 + d + 1, cy + s // 2 - d - 1, ink)
        K.hline(cx - s // 2 + 3, cx + s // 2 + 3, cy - s // 2 - 3, ink)
        K.vline(cx + s // 2 + 3, cy - s // 2 - 3, cy + s // 2 - 3, ink)
        for xx in range(cx + s // 2 + 6, x1 - 1, 2):       # its notes: ruled, never letters
            for yy in range(y0 + 3, y1 - 2, 3):
                if H(xx, yy, 7) % 4:
                    K.px(xx, yy, "G" if K.row == 2 and (xx + yy) % 11 == 0 else "B")
        K.hline(cx - s // 2, cx + s // 2, y1 - 2, "X")     # the dimension line
    K.rim()


def p_gates(K, S):
    """the card-key gates, 2x2 blocks: a header with its reader, then bars -- a barrier, plainly"""
    K.fill(S["gateground"])
    for (x0, y0, x1, y1, n) in K.parts():
        K.rect(x0, y0, x1, y0 + 3, "WD")
        K.hline(x0, x1, y0, "WL")
        for xx in range(x0 + 1, x1, 3):
            K.vline(xx, y0 + 4, y1, S["gatebar"])
            K.vline(xx + 1, y0 + 4, y1, "BD" if S["gatebar"] == "B" else "SHD")
        K.px(x0 + 2, y0 + 1, "X")                          # the reader's light: shut
    K.rim()


def p_gatev(K, S):
    for (x0, y0, x1, y1, n) in K.parts():
        K.rect(x0, y0, x1, y1, S["gateground"])
        for yy in range(y0, y1 + 1, 3):
            K.hline(x0, x1, yy, S["gatebar"])
        K.px((x0 + x1) // 2, y0 + 1, "X")
    K.rim()


def p_notice(K, S):
    for (x0, y0, x1, y1, n) in K.parts():
        if n < 12:
            continue
        K.rect(x0, y0, x1, y1, "WHT")
        K.rect(x0, y0, x1, y0 + 2, "WD")                   # the clip
        for yy in range(y0 + 5, y1 - 1, 2):
            K.hline(x0 + 2, x0 + 2 + H(yy, x0, 9) % max(1, x1 - x0 - 4), yy, "MID")
        K.px(x1 - 2, y1 - 2, "X")                          # countersigned
    K.rim()


def p_pad(K, S):
    """the warp pad: rings in the floor, read as a place to stand"""
    S["pad"](K)


def p_plaque(K, S):
    for (x0, y0, x1, y1, n) in K.parts():
        K.rect(x0, y0, x1, y1, "B")
        K.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, "BL")
        for yy in range(y0 + 3, y1 - 1, 2):
            K.hline(x0 + 3, x1 - 3, yy, "B")
    K.rim()


def p_plate(K, S):
    K.fill("F")
    for y in range(K.h):
        for x in range(K.w):
            if H(x, y, 11) % 23 == 0:
                K.px(x, y, "FL")


def p_rim(K, S):
    """the fountain's rim becomes the rail round the plate: vanilla's white rim -> the rail, its blue water -> the
    plate (dark, the darkest thing in the room, as through the tower's glass)"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            c = K.vpal[K.van[y][x]]
            if c[2] > c[0] + 40:                           # water
                K.px(x, y, "F" if H(x, y, 13) % 29 else "FL")
            elif lum(c) > 185:
                K.px(x, y, "BL")
            elif lum(c) > 120:
                K.px(x, y, "B")
            else:
                K.px(x, y, "BD" if lum(c) > 70 else "OUT")


def plate_frame(n):
    """one of the four 16x32 fountain frames (8 tiles in tileset order), as role names: the plate with a glint that
    crosses it slowly"""
    out = []
    for t in range(8):
        tile = []
        for k in range(64):
            x, y = (t % 2) * 8 + k % 8, (t // 2) * 8 + k // 8
            g = (x + y - n * 6) % 24
            c = "FL" if g in (0, 1) else "FD" if g == 2 else "F"
            if H(x, y, 17) % 31 == 0:
                c = "FL"
            tile.append(c)
        out.append(tile)
    return out


def p_spout(K, S):
    roles = plate_frame(0)
    for t in range(8):
        for k in range(64):
            x, y = t * 8 + k % 8, k // 8
            K.px(x, y, roles[t][k])


def p_counter(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, "W")
        K.rect(x0, y0, x1, y0 + 5, S["countertop"])        # its top, seen from above
        K.hline(x0, x1, y0 + 6, "B")                        # the brass/ink/iron lip
        for xx in range(x0 + 3, x1, 6):
            K.vline(xx, y0 + 8, y1 - 2, "WD")
        K.rect(x0, y1 - 1, x1, y1, "SHD")
    K.rim()


def p_picture(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, "BD")
        K.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, "WHT")
        S["picture"](K, x0 + 2, y0 + 2, x1 - 2, y1 - 2)
    K.rim()


def p_crates(K, S):
    S["crate"](K)
    K.rim()


def p_cratetop(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, "F")
        K.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, "FL")
        S["lid"](K, x0, y0, x1, y1)
    K.rim()


def p_cage(K, S):
    for (x0, y0, x1, y1, n) in K.parts()[:1]:
        K.rect(x0, y0, x1, y1, "SHD")
        K.rect(x0, y0, x1, y0 + 3, "F")
        K.rect(x0, y1 - 3, x1, y1, "F")
        for xx in range(x0 + 2, x1, 4):
            K.vline(xx, y0 + 4, y1 - 4, "B")
        for xx in range(x0 + 1, x1, 4):
            K.rect(xx, y0 + 6, xx + 1, y1 - 6, S["cagefill"])
    K.rim()


def p_liftfloor(K, S):
    p_floor(K, S, "liftpat")


PAINT = {k[2:]: v for k, v in globals().items() if k.startswith("p_")}


# ============================================================================================ the directions
def stop_box(K, ground, frame, mark):
    K.fill(ground)
    for y in range(16):
        for x in range(16):
            if x in (1, 14) or y in (1, 14):
                K.px(x, y, frame)
    for x in range(16):
        for y in (0, 15):
            K.px(x, y, "SHD")
    for y in range(16):
        for x in (0, 15):
            K.px(x, y, "SHD")
    mark(K)


def pad_rings(K, rings, centre):
    """concentric rings in a 16x16"""
    for y in range(16):
        for x in range(16):
            d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
            c = None
            for r0, r1, col in rings:
                if r0 <= d < r1:
                    c = col
            if c:
                K.px(x, y, c)
    centre(K)


def crate_bands(K, body, band, edge):
    """crate fronts across the whole group: planks, with the direction's band"""
    for (x0, y0, x1, y1, n) in K.parts():
        K.rect(x0, y0, x1, y1, body)
        for xx in range(x0, x1 + 1):
            if (xx - x0) % 4 == 3:
                K.vline(xx, y0, y1, edge)
        band(K, x0, y0, x1, y1)


# ---- A: BRASS AND STONE -- the tower continued inside
def A_floor(x, y):
    """the lobby's stone, as through the tower's glass: big slabs, a fine seam, a brass rivet at the crossings"""
    if x == 15 or y == 15:
        return "F"
    if (x, y) in ((0, 0),):
        return "B"
    if (x + 2 * y) % 13 == 0 and H(x, y, 1) % 3 == 0:
        return "FL"
    return "WHT" if (x + y) % 31 == 0 else "FL"


def A_hide(x, y):
    """the undercroft: the same brass, unpolished -- dark bronze plates on a 8px pitch, rivets at the corners"""
    if y % 8 == 7 or x % 16 == 15:
        return "FD"
    if (x % 16, y % 8) in ((1, 1), (13, 1)):
        return "B"
    return "F" if H(x // 4, y, 2) % 5 else "FL"


def A_lift(x, y):
    if x % 4 == 3 or y % 4 == 3:
        return "BD"
    return "B" if (x + y) % 7 else "BL"


def A_stop(K):
    def mark(K):
        for y in range(3, 13):
            for x in range(3, 13):
                if ((x - 3) // 2 + (y - 3) // 2) % 2 == 0:
                    K.px(x, y, "B")
    stop_box(K, "BL", "BD", mark)


def A_arrowground(K):
    K.fill("SHD")
    for y in range(K.h):
        for x in range(K.w):
            if x % 16 in (0, 15) or y % 16 in (0, 15):
                K.px(x, y, "BD")
            elif (x % 16, y % 16) in ((1, 1), (14, 1), (1, 14), (14, 14)):
                K.px(x, y, "B")


def A_pad(K):
    pad_rings(K, [(0, 8.2, "FD"), (5.2, 7.4, "B"), (6.4, 7.4, "BL"), (2.6, 4.0, "F")],
              lambda K: [K.px(x, y, "BL") for x in (7, 8) for y in (7, 8)])


def A_table(K, x0, y0, x1, y1):
    for xx in range(x0 + 4, x1 - 3, 8):
        K.rect(xx, y0 + 3, xx + 4, y0 + 7, "WHT")          # papers squared to the edge


def A_picture(K, x0, y0, x1, y1):
    """the tower itself, small: a brass block and its lit windows"""
    K.rect(x0, y0, x1, y1, "W")
    cx = (x0 + x1) // 2
    K.rect(cx - 4, y0 + 2, cx + 4, y1, "BD")
    for yy in range(y0 + 3, y1, 2):
        for xx in range(cx - 3, cx + 4, 2):
            K.px(xx, yy, "BL")
    K.hline(cx - 2, cx + 2, y0 + 1, "X")


def A_crate(K):
    def band(K, x0, y0, x1, y1):
        for yy in (y0 + 2, y1 - 2):
            K.hline(x0, x1, yy, "B")
            K.hline(x0, x1, yy + 1, "BD")
        for xx in range(x0 + 1, x1, 5):
            K.px(xx, y0 + 2, "BL")
    crate_bands(K, "F", band, "FD")


def A_lid(K, x0, y0, x1, y1):
    K.hline(x0 + 1, x1 - 1, (y0 + y1) // 2, "B")
    for xx, yy in ((x0 + 2, y0 + 2), (x1 - 2, y0 + 2), (x0 + 2, y1 - 2), (x1 - 2, y1 - 2)):
        K.px(xx, yy, "BD")


A = dict(
    name="A", title="BRASS AND STONE",
    lines=["The tower continued inside. The lobby's pale stone, as through its glass; brass rails and rivets;",
           "amber light. The fountain is the dark plate cast into the floor, railed off. Below, the HIDEOUT is",
           "the same brass unpolished (an undercroft); the WAREHOUSE brass-banded crates. His red on the couch."],
    #  rows 7..12, roles 1..15: OUT SHD MID HI WHT | FD F FL | WD W WL | BD B BL | X
    pal={
        8:  [(40, 26, 20), (92, 80, 70), (150, 140, 124), (196, 188, 168), (240, 234, 218),
             (160, 150, 130), (194, 186, 164), (214, 206, 184), (150, 132, 108), (206, 194, 168), (228, 220, 198),
             (116, 80, 34), (204, 160, 72), (236, 206, 124), (198, 34, 44)],
        12: [(40, 26, 20), (70, 56, 46), (128, 116, 100), (184, 174, 152), (236, 228, 206),
             (74, 52, 30), (110, 80, 46), (140, 104, 62), (120, 104, 84), (176, 162, 136), (206, 194, 168),
             (116, 80, 34), (204, 160, 72), (236, 206, 124), (198, 34, 44)],
        7:  [(40, 26, 20), (58, 50, 52), (128, 116, 100), (184, 174, 152), (240, 234, 218),
             (110, 80, 46), (150, 116, 70), (190, 150, 90), (96, 90, 92), (164, 158, 150), (210, 204, 192),
             (116, 80, 34), (204, 160, 72), (255, 226, 150), (226, 164, 78)],
        9:  [(40, 26, 20), (70, 56, 46), (128, 116, 100), (184, 174, 152), (240, 234, 218),
             (18, 14, 22), (24, 20, 30), (54, 48, 60), (150, 132, 108), (206, 194, 168), (228, 220, 198),
             (116, 80, 34), (204, 160, 72), (236, 206, 124), (198, 34, 44)],
        10: [(40, 26, 20), (70, 56, 46), (128, 116, 100), (184, 174, 152), (240, 234, 218),
             (110, 80, 46), (156, 112, 64), (196, 150, 92), (120, 104, 84), (176, 162, 136), (214, 204, 180),
             (110, 20, 30), (204, 160, 72), (236, 206, 124), (176, 34, 44)],
        11: [(40, 26, 20), (92, 80, 70), (150, 140, 124), (196, 188, 168), (240, 234, 218),
             (150, 132, 108), (196, 184, 158), (222, 214, 192), (150, 132, 108), (206, 194, 168), (232, 224, 204),
             (116, 80, 34), (204, 160, 72), (236, 206, 124), (226, 164, 78)],
    },
    floorpat=A_floor, hidepat=A_hide, liftpat=A_lift,
    wallpat=lambda x, y: "WD" if y % 8 == 7 else None,
    partpat=lambda x, y: "B" if y % 8 == 0 else ("BL" if (x % 8, y % 8) == (1, 2) else None),
    trimpat=lambda x, y: "B" if y % 8 == 1 else None,
    bandpat=lambda x, y: ("BL" if (x % 8 == 3 and y % 8 == 3) else None),
    skirt="B",
    stop=A_stop, arrowground=A_arrowground, arrowfg="BL", arrowring="BD",
    phone="WD", ventslat="B", tabletop="WL", tableedge="B", tablemotif=A_table,
    machine="W", boxc="B", gateground="SHD", gatebar="B", pad=A_pad, countertop="WL",
    picture=A_picture, crate=A_crate, lid=A_lid, cagefill="X",
)


# ---- B: THE FORM -- CORPUS requisitions, countersigns, files
def B_floor(x, y):
    """carpet tiles ruled like a form: paper, a feint rule every 4px, the tile's own margin"""
    if x == 15 or y == 15:
        return "FD"
    if y % 4 == 3:
        return "F"
    if x == 2:
        return "WL"
    return "FL"


def B_hide(x, y):
    """the ledger under the GAME CORNER: green baize ruled in columns, a double rule at each column's foot"""
    if x % 8 == 0:
        return "FD"
    if x % 8 == 1 and y % 2 == 0:
        return "FD"
    if y == 15:
        return "FD"
    return "F" if H(x, y, 4) % 7 else "FL"


def B_lift(x, y):
    return "FD" if (x % 8 == 7 or y % 8 == 7) else ("F" if (x + y) % 2 else "FL")


def B_stop(K):
    def mark(K):                                           # a box ticked: received
        for k in range(4):
            K.px(4 + k, 8 + k, "X")
            K.px(4 + k, 9 + k, "X")
        for k in range(6):
            K.px(8 + k, 11 - k - 1, "X")
            K.px(8 + k, 12 - k - 1, "X")
    stop_box(K, "WHT", "B", mark)


def B_arrowground(K):
    """a routing docket: paper with its rules, a folded corner"""
    K.fill("FL")
    for y in range(K.h):
        for x in range(K.w):
            if y % 16 % 4 == 3:
                K.px(x, y, "F")
            if x % 16 in (0, 15) or y % 16 in (0, 15):
                K.px(x, y, "MID")
            if x % 16 >= 12 and y % 16 <= 3 - (15 - x % 16) + 3 and (x % 16) - 12 >= (y % 16):
                K.px(x, y, "HI")


def B_pad(K):
    """a rubber stamp's seal, inked into the floor"""
    pad_rings(K, [(0, 8.2, "FL"), (5.6, 7.2, "X"), (3.2, 4.2, "X")],
              lambda K: [K.px(x, y, "X") for x, y in ((7, 6), (8, 6), (6, 7), (9, 7), (7, 9), (8, 9))])


def B_table(K, x0, y0, x1, y1):
    for yy in range(y0 + 3, y1 - 4, 2):
        K.hline(x0 + 3, x1 - 3, yy, "W")                   # a blotter ruled for the minutes


def B_picture(K, x0, y0, x1, y1):
    """a chart: one line, rising, that never comes down"""
    K.rect(x0, y0, x1, y1, "WHT")
    for yy in range(y0, y1 + 1, 2):
        K.hline(x0, x1, yy, "HI")
    n = x1 - x0
    for k in range(n + 1):
        yy = y1 - 1 - (k * (y1 - y0 - 2)) // max(1, n)
        K.px(x0 + k, yy, "X")
        K.px(x0 + k, yy + 1, "X")


def B_crate(K):
    def band(K, x0, y0, x1, y1):                            # a tag on each tote: barcode stripes, no numbers
        tx0 = x0 + 3
        K.rect(tx0, y0 + 3, min(x1 - 3, tx0 + 9), y0 + 8, "WHT")
        for xx in range(tx0 + 1, min(x1 - 3, tx0 + 9)):
            if H(xx, y0, 6) % 3:
                K.vline(xx, y0 + 4, y0 + 7, "OUT")
    crate_bands(K, "W", band, "WD")


def B_lid(K, x0, y0, x1, y1):
    K.rect(x0 + 3, y0 + 3, x0 + 9, y0 + 6, "WHT")
    K.hline(x0 + 4, x0 + 8, y0 + 4, "MID")


B = dict(
    name="B", title="THE FORM",
    lines=["CORPUS requisitions, countersigns, files (1.7). Floors ruled like a form (SCORN SOLUTIONS' roof is",
           "ruled like one), walls of filing drawers, the warp pad a rubber stamp's seal, the spin arrows routing",
           "dockets. The HIDEOUT is the ledger under the GAME CORNER, green baize ruled in columns; the WAREHOUSE",
           "tagged totes. The plate in the lobby is still the darkest thing in the building."],
    pal={
        8:  [(30, 34, 44), (80, 88, 104), (150, 156, 166), (204, 206, 210), (250, 250, 244),
             (196, 196, 184), (206, 214, 222), (244, 240, 226), (120, 132, 128), (176, 190, 184), (210, 220, 214),
             (60, 86, 140), (100, 132, 192), (166, 190, 226), (198, 52, 52)],
        12: [(30, 34, 44), (56, 62, 70), (130, 136, 140), (190, 194, 196), (246, 246, 240),
             (34, 76, 54), (56, 108, 76), (78, 132, 94), (110, 124, 120), (160, 176, 170), (200, 212, 206),
             (60, 86, 140), (100, 132, 192), (166, 190, 226), (198, 52, 52)],
        7:  [(30, 34, 44), (70, 76, 90), (150, 156, 166), (204, 206, 210), (250, 250, 244),
             (196, 196, 184), (214, 220, 226), (244, 240, 226), (110, 124, 120), (170, 184, 178), (214, 224, 218),
             (60, 86, 140), (40, 70, 140), (166, 190, 226), (198, 52, 52)],
        9:  [(30, 34, 44), (56, 62, 70), (130, 136, 140), (190, 194, 196), (246, 246, 240),
             (18, 14, 22), (24, 20, 30), (54, 48, 60), (110, 124, 120), (160, 176, 170), (200, 212, 206),
             (40, 60, 110), (60, 86, 140), (100, 132, 192), (198, 52, 52)],
        10: [(30, 34, 44), (56, 62, 70), (130, 136, 140), (190, 194, 196), (246, 246, 240),
             (150, 140, 120), (184, 174, 150), (214, 206, 184), (120, 132, 128), (176, 190, 184), (214, 224, 218),
             (110, 20, 30), (100, 132, 192), (166, 190, 226), (176, 34, 44)],
        11: [(30, 34, 44), (80, 88, 104), (150, 156, 166), (204, 206, 210), (250, 250, 244),
             (176, 184, 190), (210, 216, 220), (236, 238, 236), (120, 132, 128), (176, 190, 184), (214, 224, 218),
             (60, 86, 140), (100, 132, 192), (166, 190, 226), (198, 52, 52)],
    },
    floorpat=B_floor, hidepat=B_hide, liftpat=B_lift,
    wallpat=lambda x, y: "WD" if x % 8 == 7 else ("SHD" if (x % 8 in (3, 4) and y % 8 == 3) else None),
    partpat=lambda x, y: "WD" if x % 8 == 7 else ("SHD" if (x % 8 in (3, 4) and y % 8 == 4) else None),
    trimpat=lambda x, y: "B" if y % 8 == 1 else None,
    bandpat=lambda x, y: ("WD" if x % 8 == 7 else ("SHD" if (x % 8 in (3, 4) and y % 16 == 6) else None)),
    skirt="X",
    stop=B_stop, arrowground=B_arrowground, arrowfg="B", arrowring="BD",
    phone="MID", ventslat="WD", tabletop="WHT", tableedge="B", tablemotif=B_table,
    machine="WL", boxc="B", gateground="FL", gatebar="X", pad=B_pad, countertop="WHT",
    picture=B_picture, crate=B_crate, lid=B_lid, cagefill="W",
)


# ---- C: THE FOUNDRY -- what was there before CORPUS
def C_floor(x, y):
    """cast-iron tread plate: a raised lozenge on a diagonal, a rivet in each corner"""
    if x == 15 or y == 15:
        return "FD"
    if (x, y) in ((1, 1), (13, 1), (1, 13), (13, 13)):
        return "BL"
    if ((x // 4) + (y // 4)) % 2 == 0 and (x % 4 + y % 4) in (2, 3):
        return "FL"
    return "F"


def C_hide(x, y):
    """the casting floor: sand, speckled, raked"""
    h = H(x, y, 8) % 11
    if y % 6 == 5 and h > 3:
        return "FD"
    return "FL" if h == 0 else ("FD" if h == 1 else "F")


def C_lift(x, y):
    return "FD" if (x % 4 == 0) else "F"


def C_stop(K):
    def mark(K):                                           # a cast square: four ingot pips
        for x0, y0 in ((4, 4), (9, 4), (4, 9), (9, 9)):
            K.rect(x0, y0, x0 + 2, y0 + 2, "F")
            K.hline(x0, x0 + 2, y0, "FL")
    stop_box(K, "MID", "FD", mark)


def C_arrowground(K):
    K.fill("FD")
    for y in range(K.h):
        for x in range(K.w):
            if x % 16 in (0, 15) or y % 16 in (0, 15):
                K.px(x, y, "OUT")
            elif ((x // 4) + (y // 4)) % 2 == 0 and (x % 4 + y % 4) == 3:
                K.px(x, y, "F")


def C_pad(K):
    """a crucible's mouth: iron rings and a glow"""
    pad_rings(K, [(0, 8.2, "FD"), (4.8, 7.4, "WD"), (6.2, 7.4, "W"), (0, 3.6, "X"), (0, 2.0, "BL")],
              lambda K: None)


def C_table(K, x0, y0, x1, y1):
    for xx in range(x0 + 3, x1 - 2, 5):                    # a workbench: clamps along its edge
        K.rect(xx, y0 + 1, xx + 1, y0 + 3, "BD")


def C_picture(K, x0, y0, x1, y1):
    """the founding: an ingot, and the first BOX cast from it"""
    K.rect(x0, y0, x1, y1, "HI")
    my = (y0 + y1) // 2
    K.rect(x0 + 1, my, x0 + 6, my + 3, "BD")
    K.hline(x0 + 2, x0 + 5, my - 1, "B")
    K.rect(x1 - 6, my - 3, x1 - 1, my + 3, "X")
    K.hline(x1 - 6, x1 - 1, my, "OUT")


def C_crate(K):
    def band(K, x0, y0, x1, y1):                            # ingots stacked on a pallet
        K.rect(x0, y1 - 2, x1, y1, "BD")
        for yy in range(y0 + 1, y1 - 3, 3):
            for xx in range(x0 + (yy % 2) * 2, x1 - 1, 5):
                K.rect(xx, yy, xx + 3, yy + 1, "B")
                K.hline(xx, xx + 3, yy, "BL")
    crate_bands(K, "WD", band, "SHD")


def C_lid(K, x0, y0, x1, y1):
    for yy in range(y0 + 2, y1 - 1, 3):
        K.hline(x0 + 2, x1 - 2, yy, "FD")


C = dict(
    name="C", title="THE FOUNDRY",
    lines=["FOUNDRY CO. as it was before CORPUS: the company that made BOXes, in cast iron, bronze and a little",
           "furnace glow. Tread plates and rivets on every floor; the HIDEOUT a casting floor of sand; the",
           "WAREHOUSE ingots on pallets; the warp pad a crucible's mouth. CORPUS shows only by its plastic plants",
           "and the red. The plate in the lobby reads as what it is: a casting."],
    pal={
        8:  [(26, 24, 28), (58, 56, 62), (106, 104, 108), (160, 156, 152), (226, 220, 210),
             (58, 62, 70), (84, 90, 98), (120, 126, 134), (96, 66, 50), (140, 98, 72), (178, 134, 98),
             (110, 70, 34), (170, 112, 52), (220, 166, 96), (198, 34, 44)],
        12: [(26, 24, 28), (52, 48, 50), (106, 104, 108), (160, 156, 152), (226, 220, 210),
             (110, 92, 68), (150, 128, 96), (184, 162, 124), (70, 74, 82), (104, 110, 120), (140, 146, 154),
             (110, 70, 34), (170, 112, 52), (220, 166, 96), (198, 34, 44)],
        7:  [(26, 24, 28), (52, 48, 50), (106, 104, 108), (160, 156, 152), (226, 220, 210),
             (40, 42, 48), (70, 74, 82), (104, 110, 120), (70, 74, 82), (120, 126, 134), (170, 174, 180),
             (110, 70, 34), (240, 140, 40), (255, 210, 120), (230, 90, 30)],
        9:  [(26, 24, 28), (52, 48, 50), (106, 104, 108), (160, 156, 152), (226, 220, 210),
             (18, 14, 22), (24, 20, 30), (70, 40, 34), (70, 74, 82), (120, 126, 134), (170, 174, 180),
             (110, 70, 34), (170, 112, 52), (220, 166, 96), (198, 34, 44)],
        10: [(26, 24, 28), (52, 48, 50), (106, 104, 108), (160, 156, 152), (226, 220, 210),
             (70, 74, 82), (104, 110, 120), (140, 146, 154), (90, 64, 48), (130, 94, 68), (170, 128, 94),
             (110, 20, 30), (170, 112, 52), (220, 166, 96), (176, 34, 44)],
        11: [(26, 24, 28), (58, 56, 62), (106, 104, 108), (160, 156, 152), (226, 220, 210),
             (84, 90, 98), (120, 126, 134), (160, 164, 170), (96, 66, 50), (140, 98, 72), (178, 134, 98),
             (110, 70, 34), (170, 112, 52), (220, 166, 96), (240, 140, 40)],
    },
    floorpat=C_floor, hidepat=C_hide, liftpat=C_lift,
    wallpat=lambda x, y: "BL" if (x % 8, y % 8) == (2, 2) else ("WD" if y % 8 == 7 else None),
    partpat=lambda x, y: "BL" if (x % 8, y % 8) == (2, 3) else None,
    trimpat=lambda x, y: "BD" if y % 8 == 1 else None,
    bandpat=lambda x, y: ("WD" if (x % 8 == 0) else None),
    skirt="X",
    stop=C_stop, arrowground=C_arrowground, arrowfg="B", arrowring="BL",
    phone="SHD", ventslat="WD", tabletop="F", tableedge="FD", tablemotif=C_table,
    machine="W", boxc="X", gateground="SHD", gatebar="W", pad=C_pad, countertop="FL",
    picture=C_picture, crate=C_crate, lid=C_lid, cagefill="WD",
)

STYLES = {"A": A, "B": B, "C": C}


# ============================================================================================ drawing a direction
def draw(S):
    """-> (tiles: 384 x 64 indices, palettes: {row: 16 colours}, fountain frames: 4 x 8 x 64 indices, groups' tiles)"""
    tiles = [t[:] for t in VAN]
    owner = {}
    for name, layout, row, painter, desc in GROUPS:
        K = Canvas(layout, row, S)
        PAINT[painter](K, S)
        for t, px in K.tiles().items():
            tiles[t] = px
            owner[t] = name
    pals = {}
    for r in ROWS:
        pals[r] = [VPAL[r][0]] + list(S["pal"][r])
    frames = []
    for n in range(4):
        roles = plate_frame(n)
        fr = []
        for t in range(8):
            fr.append([SROLE[c] if VFRAMES[n][t][k] else 0 for k, c in enumerate(roles[t])])
        frames.append(fr)
    for t in range(8):                                     # the sheet's own copy is frame 0
        tiles[FOUNTAIN_T0 + t] = frames[0][t][:]
    return tiles, pals, frames, owner


# ============================================================================================ rendering
def render_layout(l, tiles, spals, frame=None):
    pals = [PPAL[n] for n in range(7)] + [spals[r] for r in ROWS]
    W, Hh = l["width"], l["height"]
    bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    img = Image.new("RGB", (W * 16, Hh * 16))
    o = img.load()
    for yy in range(Hh):
        for xx in range(W):
            m = struct.unpack_from("<H", bd, (yy * W + xx) * 2)[0] & 0x3FF
            ee = entries(m)
            for layer in (0, 1):
                for q in range(4):
                    t = ee[layer * 4 + q]
                    i = t & 0x3FF
                    src = PTILES[i] if i < 640 else (tiles[i - 640] if i - 640 < len(tiles) else [0] * 64)
                    pr = (t >> 12) & 0xF
                    pal = pals[pr] if pr < len(pals) else pals[0]
                    for ty in range(8):
                        for tx in range(8):
                            sx = 7 - tx if (t >> 10) & 1 else tx
                            sy = 7 - ty if (t >> 11) & 1 else ty
                            v = src[sy * 8 + sx]
                            if layer and v == 0:
                                continue
                            o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = pal[v]
    return img


def vanilla_state():
    return [t[:] for t in VAN], {r: VPAL[r] for r in ROWS}


def sheet_image(tiles, spals, use):
    sh = Image.new("RGB", (128, 192), (255, 255, 255))
    o = sh.load()
    for t in range(NT):
        if t not in use:
            continue
        rows = use[t]["rows"]
        r = rows.most_common(1)[0][0] if rows else 12
        pal = spals[r] if r >= 7 else PPAL[r]
        for k in range(64):
            v = tiles[t][k]
            o[(t % 16) * 8 + k % 8, (t // 16) * 8 + k // 8] = pal[v] if v else (236, 236, 236)
    return sh


ROOMS = [("SilphCo_1F", "FOUNDRY 1F: the lobby"), ("SilphCo_5F", "FOUNDRY 5F: an office floor"),
         ("SilphCo_11F", "FOUNDRY 11F: the boardroom"), ("RocketHideout_B4F", "HIDEOUT B4F: SCORN's office"),
         ("FiveIsland_RocketWarehouse", "the WAREHOUSE: spin floor")]
DETAILS = [("SilphCo_1F", (6, 2, 22, 12), "the lobby: the plate"), ("SilphCo_11F", (0, 0, 13, 12), "the boardroom"),
           ("FiveIsland_RocketWarehouse", (0, 0, 15, 11), "the spin floor, the gates"),
           ("RocketHideout_B4F", (0, 0, 14, 11), "SCORN's office below")]


def label(d, xy, s, fill=(30, 30, 30)):
    d.text(xy, s, fill=fill)


def contact_sheets(out_dir, states, use):
    L = {l["name"].replace("_Layout", ""): l for l in layouts()}
    #  1x: every state a row of whole rooms
    renders = {k: {m: render_layout(L[m], *v) for m, _ in ROOMS} for k, v in states.items()}
    pad, head = 12, 26
    rw = sum(renders["NOW"][m].width for m, _ in ROOMS) + pad * (len(ROOMS) + 1)
    rh = max(renders["NOW"][m].height for m, _ in ROOMS)
    titles = {"NOW": ("NOW", ["vanilla's office as it stands (Nintendo's tiles)"])}
    for k in "ABC":
        titles[k] = ("%s %s" % (k, STYLES[k]["title"]), STYLES[k]["lines"])
    blocks = []
    for k in states:
        t, lines = titles[k]
        th = head + 13 * len(lines) + 6
        im = Image.new("RGB", (rw, th + rh + pad), (250, 248, 242))
        d = ImageDraw.Draw(im)
        label(d, (pad, 6), t, (120, 20, 30))
        for j, s in enumerate(lines):
            label(d, (pad + 220, 6 + 13 * j), s)
        x = pad
        for m, cap in ROOMS:
            label(d, (x, th - 14), cap, (60, 60, 60))
            im.paste(renders[k][m], (x, th))
            x += renders[k][m].width + pad
        blocks.append(im)
    W = max(b.width for b in blocks)
    sheet = Image.new("RGB", (W, sum(b.height for b in blocks) + 40), (250, 248, 242))
    d = ImageDraw.Draw(sheet)
    label(d, (pad, 10), "T-536 DRAFT -- FOUNDRY CO. and CORPUS interiors, three directions, real rooms at 1x "
                        "(redrawn in place: no block, collision or palette row moves). Nothing here is in the engine.",
          (20, 20, 20))
    y = 40
    for b in blocks:
        sheet.paste(b, (0, y))
        y += b.height
    p1 = os.path.join(out_dir, "t536_rooms_1x.png")
    sheet.save(p1)
    #  3x: the details
    crops = {}
    for k, v in states.items():
        crops[k] = []
        for m, (x0, y0, x1, y1), cap in DETAILS:
            im = renders[k][m] if m in renders[k] else render_layout(L[m], *v)
            c = im.crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
            crops[k].append((c.resize((c.width * 3, c.height * 3), Image.NEAREST), cap))
    cw = sum(c.width for c, _ in crops["NOW"]) + pad * (len(DETAILS) + 1)
    ch = max(c.height for c, _ in crops["NOW"]) + 30
    det = Image.new("RGB", (cw + 150, ch * len(states) + 40), (250, 248, 242))
    d = ImageDraw.Draw(det)
    label(d, (pad, 10), "T-536 DRAFT -- details at 3x: the plate where the fountain was, the boardroom, the spin "
                        "floor and its gates, SCORN's office.", (20, 20, 20))
    y = 40
    for k in states:
        label(d, (pad, y + 8), titles[k][0], (120, 20, 30))
        x = 150
        for c, cap in crops[k]:
            label(d, (x, y + 4), cap, (60, 60, 60))
            det.paste(c, (x, y + 20))
            x += c.width + pad
        y += ch
    p2 = os.path.join(out_dir, "t536_detail_3x.png")
    det.save(p2)
    #  the tilesets, 3x side by side, and the four fountain frames
    sh = Image.new("RGB", (len(states) * (384 + pad) + pad, 576 + 60), (250, 248, 242))
    d = ImageDraw.Draw(sh)
    label(d, (pad, 6), "T-536 DRAFT -- the office's 384 tiles at 3x, each in its own row (light grey: unused, "
                       "left as they are)", (20, 20, 20))
    x = pad
    for k, v in states.items():
        label(d, (x, 26), titles[k][0], (120, 20, 30))
        sh.paste(sheet_image(v[0], v[1], use).resize((384, 576), Image.NEAREST), (x, 44))
        x += 384 + pad
    p3 = os.path.join(out_dir, "t536_tiles_3x.png")
    sh.save(p3)
    return [p1, p2, p3]


# ============================================================================================ writing
def save_indexed(path, tiles, pal, w=16):
    n = len(tiles)
    hgt = (n + w - 1) // w
    im = Image.new("P", (w * 8, hgt * 8))
    flat = []
    for c in list(pal)[:16]:
        flat += list(c)
    im.putpalette(flat + [0] * (48 - len(flat)))      # 16 colours, saved 4-bit as the engine's own sheets are
    px = im.load()
    for t in range(n):
        for k in range(64):
            px[(t % w) * 8 + k % 8, (t // w) * 8 + k // 8] = tiles[t][k]
    im.save(path, bits=4)


def write_direction(base, S):
    tiles, pals, frames, owner = draw(S)
    os.makedirs(os.path.join(base, "palettes"), exist_ok=True)
    os.makedirs(os.path.join(base, "anim", "fountain"), exist_ok=True)
    save_indexed(os.path.join(base, "tiles.png"), tiles, pals[12])
    for r in ROWS:
        write_pal(os.path.join(base, "palettes", "%02d.pal" % r), pals[r])
    for n, fr in enumerate(frames):
        save_indexed(os.path.join(base, "anim", "fountain", "%d.png" % n), fr, pals[9], w=2)
    return tiles, pals, owner


# ============================================================================================ report
def report(use, bmaps, named):
    owner = {}
    for name, layout, row, painter, desc in GROUPS:
        for r in layout:
            for t in r:
                if t is not None:
                    owner.setdefault(t, name)
    L = layouts()
    mbl = maps_by_layout()
    print("T-536 -- gTileset_SilphCo (tiles and rows 7..12 from secondary/condominiums, shared by no other layout)")
    print("  %d layouts:" % len(L))
    for l in L:
        print("    %-44s %2dx%-2d  %s" % (l["name"], l["width"], l["height"], ", ".join(mbl.get(l["id"], [])) or "-"))
    used = sorted(use)
    print("\n  %d of %d tiles drawn (by a map or by a block the engine/scripts place); %d blocks of %d placed by maps"
          % (len(used), NT, len(bmaps), NB))
    rows = collections.Counter()
    for t in used:
        if use[t]["rows"]:
            rows[use[t]["rows"].most_common(1)[0][0]] += 1
    print("  tiles by home row:", ", ".join("%d: %d" % (r, n) for r, n in sorted(rows.items())))
    print("\n  OBJECTS")
    print("  %-11s %4s %3s %7s  %-58s %s" % ("group", "tls", "row", "draws", "what", "maps"))
    by = collections.defaultdict(list)
    for t in used:
        by[owner.get(t, "?")].append(t)
    for name, layout, row, painter, desc in GROUPS:
        ts = by.get(name, [])
        draws = sum(use[t]["n"] for t in ts)
        ms = set()
        for t in ts:
            ms |= use[t]["maps"]
        short = sorted({re.sub(r"(SilphCo|RocketHideout)_.*", r"\1", m) for m in ms})
        print("  %-11s %4d %3d %7d  %-58s %s" % (name, len(ts), row, draws, desc[:58], ", ".join(short)))
    orphans = by.get("?", [])
    print("\n  tiles in no group: %s" % (orphans or "none"))
    print("\n  BLOCKS THE ENGINE OR A SCRIPT NAMES (ids kept; each still reads as what it is)")
    for b in sorted(named):
        print("    0x%03X %-20s %s" % (b, behaviour(b), "; ".join(sorted(named[b]))))
    print("\n  Each direction: %d tiles redrawn (rows 7..12 and the office's tiles in primary rows 0..2), 0 new tiles,"
          " 0 new rows;\n  rows 7..12 recoloured (6 rows, as vanilla); primary rows 0..2 unchanged; 4 fountain frames."
          % len([t for t in used if t in owner]))
    print("  Not here: door_anims silph_co_elevator.png / hideout_elevator.png (gbadoors.py, after a pick).")
    return orphans


def main():
    use, bmaps, named = census()
    orphans = report(use, bmaps, named)
    if DRAFT is not None:
        os.makedirs(DRAFT, exist_ok=True)
        states = collections.OrderedDict()
        states["NOW"] = vanilla_state()
        summary = {}
        for k, S in STYLES.items():
            tiles, pals, owner = write_direction(os.path.join(DRAFT, k), S)
            states[k] = (tiles, pals)
            changed = sum(1 for t in use if tiles[t] != VAN[t])
            summary[k] = dict(title=S["title"], tiles_redrawn=changed, rows=list(ROWS),
                              palettes={r: pals[r] for r in ROWS})
        json.dump(summary, open(os.path.join(DRAFT, "directions.json"), "w"), indent=1)
        paths = contact_sheets(DRAFT, states, use)
        print("\n  drafts: %s/{A,B,C}/ (tiles.png, palettes/07..12.pal, anim/fountain/0..3.png)" % DRAFT)
        for p in paths:
            print("  sheet:", p)
        for k in STYLES:
            print("  %s %-16s %d tiles redrawn" % (k, STYLES[k]["title"], summary[k]["tiles_redrawn"]))
    if not WRITE and len(APPROVED) == 1:
        #  T-446's rule, as gbadoors.py keeps it: report mode compares the engine with the approved write and exits 1
        #  if they differ, so check_generators.py fails the day another pass draws over the office
        pick = next(iter(APPROVED))
        tiles, pals, frames, owner = draw(STYLES[pick])
        want = {SEC + "/tiles.png": (tiles, VPAL[7], 16)}
        for n, fr in enumerate(frames):
            want[MET + "/anim/fountain/%d.png" % n] = (fr, pals[9], 2)
        off = []
        for rel, (ts, pal, w) in want.items():
            path = os.path.join(GBA, rel)
            if not os.path.exists(path) or tiles_of(Image.open(path)) != [list(t) for t in ts]:
                off.append(rel)
        for r in ROWS:
            path = os.path.join(GBA, SEC, "palettes", "%02d.pal" % r)
            if [tuple(c) for c in read_pal(path)] != [tuple(c) for c in pals[r]]:
                off.append(SEC + "/palettes/%02d.pal" % r)
        if off:
            print("\n  !! the engine differs from `--write --approved --pick %s` (%d file%s) -- find which side is right:"
                  % (pick, len(off), "s" if len(off) > 1 else ""))
            for rel in off:
                print("       " + rel)
            return 1
        print("\n  the engine matches `--write --approved --pick %s`: the tiles, rows 7..12 and the fountain's frames" % pick)
    if WRITE:
        pick = argval("--pick")
        if "--approved" not in ARGS or not pick or pick not in APPROVED:
            print("\n  --write refused: T-536 is a draft. APPROVED is %s; the user picks a direction first, it goes "
                  "into APPROVED,\n  then --write --approved --pick X writes the tiles, rows 7..12 and the fountain's "
                  "frames (and gbadoors.py redraws the lift doors' frames)." % (sorted(APPROVED) or "empty"))
            return 1
        S = STYLES[pick]
        tiles, pals, frames, owner = draw(S)
        save_indexed(os.path.join(GBA, SEC, "tiles.png"), tiles, VPAL[7])
        for r in ROWS:
            write_pal(os.path.join(GBA, SEC, "palettes", "%02d.pal" % r), pals[r])
        for n, fr in enumerate(frames):
            save_indexed(os.path.join(GBA, MET, "anim", "fountain", "%d.png" % n), fr, pals[9], w=2)
        print("  written: direction %s" % pick)
    return 1 if orphans else 0


if __name__ == "__main__":
    sys.exit(main())

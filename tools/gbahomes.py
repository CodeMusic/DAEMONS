#!/usr/bin/env python3
"""The rest of the interiors, batch 1: the houses, the road houses between routes, and primary/building's last
vanilla pieces, redrawn in place in our own hand (T-538).

    python3 tools/gbahomes.py                       # report: the census of every interior secondary tileset that is
                                                    #   still vanilla (tiles, maps, rows, named blocks), the batches,
                                                    #   and batch 1's objects tile by tile
    python3 tools/gbahomes.py --draft [DIR]         # batch 1's three directions (A, B, C) drawn in full: per direction
                                                    #   the two secondaries' tiles.png and rows as .pal, the primary
                                                    #   leftovers' tiles, and the contact sheets (gfx/drafts/t538/)
    python3 tools/gbahomes.py --write --approved --pick X
                                                    # into the engine -- refused unless X is in APPROVED ({"A"}:
                                                    #   the user, 2026-11-10). Report mode compares the engine with
                                                    #   that write and exits 1 on a difference (T-446's rule)

THE ANSWER IT FOLLOWS (the user, 2026-11-10, from the vanilla-art census, item 6): "the rest of the interiors". That is
too much for one sheet -- about 800 vanilla tiles in a dozen secondary tilesets -- so it is split (BATCHES below) and
this tool draws batch 1:

  generic_building_2   the road houses: every route's gatehouse, 1F and 2F, the UNDERGROUND PATH's four door houses
                       and ROUTE 2's east building -- 22 maps draw its tiles, 111 of them vanilla. (Its other 29
                       maps, the ordinary houses, draw only primary/building's furniture: batch D's, already ours.)
  generic_building_1   the COPYCAT's room in BRAZEN, the one map that draws its tiles: the PORT on a desk, the set
                       on its stand, and vanilla's games console on its cable. 12 vanilla tiles, all but four in
                       primary row 0. (Its other 14 maps draw only primary/building's.)
  primary/building     what T-537 left: the rest-room beds (FOUNDRY 8F/9F, LORELEI's house), the open doorways, the
                       white partitions, the CINNABAR lab lounge's rug border and side blinds (T-537 listed all five as
                       "blinds") and lab-lobby tile 368. 33 tiles, all in
                       primary rows 0..3, whose colours are fixed. gbabuilding.py's LATER_T538 names them, so batch D
                       never draws them; gbamachines.py (T-537) owns a disjoint set, checked in report mode.

NOT HERE: the MANSION's diary (T-447); the LEAGUE statue (batch G's, already redrawn, not vanilla -- the road house
on ROUTE 22 only places it); the bike shop's racks (they are bike_shop's own tiles: batch 2); the SAFARI ZONE's
buildings (held for the SAFARI redesign, the user 2026-11-10); SLATE's museum (ERRATA, a landmark: drawn from 4.32).

THE RULES ARE BATCH D'S (gbabuilding.py) and T-536's (gbaoffice.py). Redrawn IN PLACE: no block, layer, flip,
palette row, behaviour or collision bit moves and no map is touched; only pixels inside tiles change, and every tile
keeps its FOOTPRINT (a transparent pixel stays transparent, a drawn one stays drawn). Primary rows 0..6 never change
colour: a primary tile, and a secondary tile placed in a primary row, is drawn in the colours that row already holds
(nearest match, summed over every row it is placed in). Only the secondaries' own rows are recoloured -- 7, 8, 9 and
12 in generic_building_2, 8 in generic_building_1 -- and each direction builds those rows from its own materials.
Neither secondary has an animation; no door animation uses either; the only blocks a script or the engine names are
0x338/0x339 (OneIsland_House2's GUIDE shelf, gbaguideshelf.py's two appended tiles: never touched) and
METATILE_GenericBuilding1_PlayersPCOff/On (0x28F/0x28A, field_specials.c -- set only in the player's house, whose
tileset is players_house; in generic_building_1 they keep their ids and still read as the PORT, off and on).

HOW IT IS DRAWN. Each object is a canvas laid out as it stands (mirrored halves and all) and drawn fresh in named
MATERIALS inside its footprint; vanilla's silhouette says only where pixels may go. Structure (counters, stairs,
banisters, wall ends) keeps vanilla's light-and-shade ZONES as geometry and is repainted in the direction's materials
with its grain. The look is batch D's: from above and the south, a lit top over a darker front, light from the upper
left, bold forms that read at 1x.

Every in-game word: none. This is art.
"""
import collections, contextlib, glob, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import read_pal, write_pal
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t538")
#  The user's pick goes here ("A", "B" or "C"); --write refuses anything not in it.
APPROVED = {"A"}                                  # the user, 2026-11-10: A Hearth

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
PICK = argval("--pick")

#  gbabuilding and gbamachines read their own switches off sys.argv at import (engine.md trap 16): a clean argv.
_argv, sys.argv = sys.argv, ["gbabuilding"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import gbabuilding as GB
finally:
    sys.argv = _argv

PRI = "data/tilesets/primary/building"
HDR = open(os.path.join(GBA, "src/data/tilesets/headers.h")).read()
GFX = open(os.path.join(GBA, "src/data/tilesets/graphics.h")).read() + open(os.path.join(GBA, "src/graphics.c")).read()
MTS = open(os.path.join(GBA, "src/data/tilesets/metatiles.h")).read()
LAYOUTS = [l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if "id" in l]
MB = {int(v, 16): k[3:] for k, v in re.findall(r"#define (MB_\w+) (0x[0-9A-Fa-f]+)",
                                               open(os.path.join(GBA, "include/constants/metatile_behaviors.h")).read())}


def tiles_of(im):
    w, h = im.size
    px = im.tobytes()
    return [[px[(ty * 8 + r) * w + tx * 8 + c] & 15 for r in range(8) for c in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]


def jasc(b):
    t = b.decode("utf-8", "replace").replace("\r", "").split("\n")
    return [tuple(map(int, l.split()[:3])) for l in t[3:19]]


def _field(sym, f):
    b = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % re.escape(sym), HDR, re.S)
    m = b and re.search(r"\.%s = (\w+)" % f, b.group(1))
    return m and m.group(1)


def tileset_dirs(sym):
    """(tiles dir, metatiles dir) of a tileset symbol, from the headers (SilphCo draws condominiums' tiles)"""
    t, m = _field(sym, "tiles"), _field(sym, "metatiles")
    td = t and re.search(r"%s\[\] = INCBIN_U32\(\"(data/tilesets/[^\"]+)/tiles" % t, GFX)
    md = m and re.search(r"%s\[\] = INCBIN_U16\(\"(data/tilesets/[^\"]+)/metatiles" % m, MTS)
    return (td.group(1) if td else None), (md.group(1) if md else None)


def maps_by_layout():
    out = collections.defaultdict(list)
    for mj in glob.glob(os.path.join(GBA, "data/maps/*/map.json")):
        d = json.load(open(mj))
        out[d.get("layout")].append(os.path.basename(os.path.dirname(mj)))
    return out


MBL = maps_by_layout()
LAYOUT_OF_MAP = {m: lid for lid, ms in MBL.items() for m in ms}

# ============================================================================================ the census and batches
#  Every interior secondary on primary/building that still draws Nintendo's tiles. Status is the plan, not a fact
#  the tool can measure; the counts are measured.
CENSUS_SETS = [
    ("gTileset_GenericBuilding2", 1, "the road houses (every route's gatehouse), drawn by 22 of its maps"),
    ("gTileset_GenericBuilding1", 1, "the COPYCAT's room: the PORT on a desk, the TV stand, the console"),
    ("gTileset_Lab", 2, "the CINNABAR lab (four rooms) and THREE ISLAND's house"),
    ("gTileset_BikeShop", 2, "CERULEAN's bike shop: the racks and the bikes"),
    ("gTileset_SeaCottage", 2, "the SEA COTTAGE (ROUTE 25)"),
    ("gTileset_FanClubDaycare", 3, "VERMILION's fan club, the two day cares, LAVENDER's volunteer house"),
    ("gTileset_BurgledHouse", 3, "CERULEAN's burgled house"),
    ("gTileset_UndergroundPath", 3, "the UNDERGROUND PATH's two tunnels"),
    ("gTileset_Museum", "L", "SLATE's MUSEUM OF ERRATA (4.32), the WARDEN's house, FUCHSIA's house 2, the RESORT house: "
                            "a landmark, drawn from the story"),
    ("gTileset_SafariZoneBuilding", "S", "the SAFARI ZONE's entrance, office, rest houses and SECRET HOUSE, and "
                                        "LORELEI's house: held for the SAFARI redesign"),
    ("gTileset_CableClub", "-", "the link rooms (colosseum, trade centre, record corner): link only"),
]
BATCHES = {
    1: "batch 1 (this draft): the road houses and the house leftovers -- generic_building_2 + generic_building_1 + "
       "primary's leftovers (beds, doorways, partitions, the lounge's rug border and blinds, 368)",
    2: "batch 2: the workrooms -- the CINNABAR lab (lab), the bike shop with its racks (bike_shop), the SEA COTTAGE",
    3: "batch 3: the rest of the homes -- the fan club and day cares (fan_club_daycare), the burgled house, the "
       "UNDERGROUND PATH's tunnels",
    "L": "landmark (T-447's way, from the story): SLATE's museum of ERRATA; museum's tileset also furnishes the WARDEN's "
         "house, which the same design must serve",
    "S": "held for the SAFARI redesign (the user, 2026-11-10)",
    "-": "later or never: link-only rooms",
}


def census_set(sym):
    """tiles a placed map draws from this secondary, how many are still vanilla's drawing, its rows, its maps"""
    td, md = tileset_dirs(sym)
    if not td:
        td = md
    cur = tiles_of(Image.open(os.path.join(GBA, td, "tiles.png")))
    van = tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, td + "/tiles.png", binary=True))))
    mt = open(os.path.join(GBA, md, "metatiles.bin"), "rb").read()
    used, rows, maps = collections.Counter(), collections.Counter(), []
    for l in LAYOUTS:
        if l.get("secondary_tileset") != sym or not MBL.get(l["id"]):
            continue
        maps += MBL[l["id"]]
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        for k in range(0, len(bd) - 1, 2):
            m = struct.unpack_from("<H", bd, k)[0] & 0x3FF
            if m < 640 or (m - 640 + 1) * 16 > len(mt):
                continue
            for e in struct.unpack_from("<8H", mt, (m - 640) * 16):
                t = (e & 0x3FF) - 640
                if 0 <= t < len(cur) and any(cur[t]):
                    used[t] += 1
                    rows[e >> 12] += 1
    vanl = [t for t in used if t < len(van) and cur[t] == van[t] and len(set(cur[t])) > 1]
    anim = _field(sym, "callback")
    return dict(dir=td, used=len(used), vanilla=len(vanl), rows=sorted(rows), maps=sorted(set(maps)),
                anim=anim if anim and anim != "NULL" else None)


# ============================================================================================ batch 1's sets
class Set:
    """one secondary tileset this batch redraws: vanilla's tiles and rows (what the painters draw over), today's"""

    def __init__(self, key, sym, own_rows):
        self.key, self.sym, self.rows = key, sym, own_rows
        td, md = tileset_dirs(sym)
        self.dir = td or md
        self.mdir = md
        self.van = tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, self.dir + "/tiles.png", binary=True))))
        self.cur_im = Image.open(os.path.join(GBA, self.dir, "tiles.png"))
        self.cur = tiles_of(self.cur_im)
        self.vpal = {r: jasc(daemonslib.upstream(GBA, self.dir + "/palettes/%02d.pal" % r, binary=True))
                     for r in range(16)}
        self.mt = open(os.path.join(GBA, md, "metatiles.bin"), "rb").read()
        self.use = collections.defaultdict(lambda: {"n": 0, "rows": collections.Counter(), "maps": set()})
        for l in LAYOUTS:
            if l.get("secondary_tileset") != sym or not MBL.get(l["id"]):
                continue
            bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
            cells = collections.Counter(struct.unpack_from("<H", bd, k)[0] & 0x3FF for k in range(0, len(bd) - 1, 2))
            for m, n in cells.items():
                if m < 640 or (m - 640 + 1) * 16 > len(self.mt):
                    continue
                for e in struct.unpack_from("<8H", self.mt, (m - 640) * 16):
                    t = (e & 0x3FF) - 640
                    if t >= 0:
                        u = self.use[t]
                        u["n"] += n
                        u["rows"][e >> 12] += n
                        u["maps"].update(MBL[l["id"]])
        #  vanilla's own tile count: anything past it was appended by us (the GUIDE's shelf) and is never touched
        self.nvan = len(self.van)

    def home(self, t):
        u = self.use.get(t)
        return u["rows"].most_common(1)[0][0] if u and u["rows"] else 0


GB2 = Set("gb2", "gTileset_GenericBuilding2", [7, 8, 9, 12])
GB1 = Set("gb1", "gTileset_GenericBuilding1", [8])
SETS = {"gb2": GB2, "gb1": GB1}
PUSE = GB.scan()                     # primary/building: tile -> draws, maps, rows, blocks
PPAL = [read_pal(os.path.join(GBA, PRI, "palettes/%02d.pal" % n)) for n in range(7)]   # as they stand (fixed)

#  primary/building's leftovers this batch owns -- gbabuilding.LATER_T538 must say the same (checked in report)
PRIMARY = {
    "bed": {512, 513, 514, 515, 528, 529, 530, 531, 544, 545, 546, 547},
    "doorway": {522, 523, 524, 538, 539, 540, 554, 555, 556},
    "partition": {171, 180, 181, 187, 196, 197},
    "loungerug": {420, 421, 436},            # T-537 called these "blinds": they are the lounge rug's border
    "blinds": {432, 433},
    "odd": {368},
}
PRIMARY_ALL = set().union(*PRIMARY.values())
#  tiles no map places but a block the engine names does: drawn too (the PORT, on: 0x28A)
NAMED_UNPLACED = {("gb1", 13), ("gb1", 14), ("gb1", 29), ("gb1", 30)}


def ptile(t):
    """the primary tile the painters draw over: vanilla's"""
    return GB.VAN[t]


# ============================================================================================ the canvas
class Cv:
    """an object laid out as it stands: specs are (setkey, tile, flip). Painters write MATERIAL names, never
    indices, and only inside the footprint (a pixel vanilla left transparent stays transparent)"""

    def __init__(self, layout, setkey):
        self.setkey = setkey
        self.layout = [[None if s is None else ((s, "") if isinstance(s, int) else s) for s in r] for r in layout]
        self.th, self.tw = len(self.layout), max(len(r) for r in self.layout)
        self.w, self.h = self.tw * 8, self.th * 8
        self.van = [[0] * self.w for _ in range(self.h)]
        self.hole = [[True] * self.w for _ in range(self.h)]
        for ty, r in enumerate(self.layout):
            for tx, spec in enumerate(r):
                if spec is None:
                    continue
                t, fl = spec
                src = ptile(t) if setkey == "P" else SETS[setkey].van[t]
                for k in range(64):
                    x, y = k % 8, k // 8
                    sx = 7 - x if "h" in fl else x
                    sy = 7 - y if "v" in fl else y
                    self.van[ty * 8 + y][tx * 8 + x] = src[sy * 8 + sx]
                    self.hole[ty * 8 + y][tx * 8 + x] = False
        self.out = [[None] * self.w for _ in range(self.h)]

    def foot(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and not self.hole[y][x] and self.van[y][x] != 0

    def px(self, x, y, m):
        if self.foot(x, y):
            self.out[y][x] = m

    def rect(self, x0, y0, x1, y1, m):
        for y in range(max(0, y0), min(self.h - 1, y1) + 1):
            for x in range(max(0, x0), min(self.w - 1, x1) + 1):
                self.px(x, y, m)

    def hline(self, x0, x1, y, m):
        self.rect(x0, y, x1, y, m)

    def vline(self, x, y0, y1, m):
        self.rect(x, y0, x, y1, m)

    def fill(self, m):
        self.rect(0, 0, self.w - 1, self.h - 1, m)

    def fn(self, f):
        """paint every footprint pixel with f(x, y) (None leaves it)"""
        for y in range(self.h):
            for x in range(self.w):
                if self.foot(x, y):
                    m = f(x, y)
                    if m is not None:
                        self.out[y][x] = m

    def edge(self, x, y):
        return self.foot(x, y) and any(0 <= x + dx < self.w and 0 <= y + dy < self.h and not self.hole[y + dy][x + dx]
                                       and self.van[y + dy][x + dx] == 0
                                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    def rim(self, m="OUT"):
        for x, y in [(x, y) for y in range(self.h) for x in range(self.w) if self.edge(x, y)]:
            self.out[y][x] = m

    def bbox(self):
        pts = [(x, y) for y in range(self.h) for x in range(self.w) if self.foot(x, y)]
        return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

    def vi(self, x, y):
        return self.van[y][x] if self.foot(x, y) else None

    def tiles(self):
        res = {}
        for ty, r in enumerate(self.layout):
            for tx, spec in enumerate(r):
                if spec is None:
                    continue
                t, fl = spec
                if t in res:
                    continue
                px = [None] * 64
                for y in range(8):
                    for x in range(8):
                        sx = 7 - x if "h" in fl else x
                        sy = 7 - y if "v" in fl else y
                        px[sy * 8 + sx] = self.out[ty * 8 + y][tx * 8 + x]
                res[t] = px
        return res


def H(x, y, s=0):
    v = (x * 374761393 + y * 668265263 + s * 2246822519) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return (v ^ (v >> 16)) & 0xFF


# ============================================================================================ painters
#  Materials every direction defines (its D["mat"]): OUT SHD MID HI WHT (the shared greys) and
#    floor:  F0 F1 F2 F3        (dark..light; the shaded floor uses F0..F2, the lit F1..F3)
#    wall:   W1 W2 W3 WT        (the upper wall, dark..light, and its trim);  P1 P2 (the pelmet); S1 S2 (the skirting)
#    timber: CT CTL CF          (a counter's top, its lit edge, its front)
#    glass:  GD GL GH           (a window or a view: dark, light, highlight)
#    rug:    R1 R2 R3 R4        (the road houses' runner)   Q1 Q2 Q3 Q4 (the houses' rug)
#    accent: X  XL              (brass, or the direction's one strong colour)
#    bed:    BS BSD BQ BQD BQL  (sheet, its shade, the quilt and its shade and light)


def p_floor(K, D, shade=False):
    pat = D["floor"]
    K.fn(lambda x, y: pat(x % 16, y % 16, shade))


def p_floor_lit(K, D):
    p_floor(K, D, False)


def p_floor_shade(K, D):
    p_floor(K, D, True)


def p_valance(K, D):
    """the upper wall where vanilla hung a scalloped valance: the direction's wall, its trim and its pelmet"""
    K.fn(lambda x, y: D["wall"](x, y))
    D["pelmet"](K)


def p_plainwall(K, D):
    """the plain upper wall (2) and its foot (18): wall, a dado rail, the skirting"""
    K.fn(lambda x, y: D["wall"](x, y))
    D["skirting"](K)


def zones(K, D, zmap=None):
    """structure: keep vanilla's light-and-shade ZONES as geometry; each vanilla index becomes a material (by the
    tile's home row), floor-coloured pixels take the floor pattern where they stand"""
    zm = zmap or D["zones"][K.setkey, K.row]
    pat = D["floor"]
    for y in range(K.h):
        for x in range(K.w):
            v = K.vi(x, y)
            if v is None:
                continue
            m = zm.get(v, "MID")
            if m == "FLOOR":
                m = pat(x % 16, y % 16, False)
            elif m == "FLOORS":
                m = pat(x % 16, y % 16, True)
            elif m in D.get("grain", {}):
                m = D["grain"][m](x, y)
            K.out[y][x] = m


def p_zones(K, D):
    zones(K, D)


def p_view(K, D):
    """a window onto the outside (the 2F's long windows and the low panes under them): a timber or iron frame
    and the sky beyond, with one glint; the panes divided the direction's way"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not K.foot(x, y):
                continue
            t = (y - y0) / max(1, (y1 - y0))
            K.px(x, y, "GH" if t < 0.25 else ("GL" if t < 0.7 else "GD"))
    D["panes"](K, x0, y0, x1, y1)
    K.rim("OUT")


def p_wallwin(K, D):
    """the small windows set in the wall"""
    p_view(K, D)


def p_lightpatch(K, D):
    """the floor in the light under a window: the floor, a step lighter"""
    pat = D["floor"]
    K.fn(lambda x, y: {"F0": "F1", "F1": "F2", "F2": "F3", "F3": "F3"}.get(pat(x % 16, y % 16, False), "F3"))


def p_spyglass(K, D):
    """vanilla's coin viewer at the 2F window, drawn again as the direction's: two barrels in its metal, the lenses
    catching the sky, a bridge, the post"""
    m, mL, mD = D["metal"], D["metalL"], D["metalD"]
    K.fill("SHD")
    for x0 in (2, 9):
        K.rect(x0, 1, x0 + 4, 9, m)
        K.vline(x0, 1, 9, mL)
        K.vline(x0 + 4, 2, 9, mD)
        K.rect(x0 + 1, 1, x0 + 3, 4, "GD")
        K.px(x0 + 1, 2, "WHT")
        K.hline(x0, x0 + 4, 5, mD)
    K.rect(6, 6, 9, 8, mD)
    K.hline(6, 9, 6, mL)
    K.rect(7, 9, 8, 15, mD)
    K.vline(7, 9, 14, m)
    K.rim("OUT")


def p_stand(K, D):
    """the viewer's post where it meets the floor"""
    K.fill(D["metalD"])
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y) and x in (7, 8) and y < 5:
                K.px(x, y, D["metal"] if x == 7 else D["metalD"])
    K.rim("OUT")


def p_strongbox(K, D):
    """the plinth under the statue on ROUTE 22's road house (row 0): the direction's"""
    D["stove"](K)


def p_runner(K, D):
    D["runner"](K)


def p_rug(K, D):
    D["rug"](K)


def p_doors(K, D):
    """a doorway with its two leaves folded back (the road houses' back rooms)"""
    D["doors"](K)


def p_hatch(K, D):
    """the counter hatch let into a wall (its cap and its sill)"""
    zones(K, D)


# ---- generic_building_1: the towns' house kit
def p_port_screen(K, D, on):
    """the PORT on a desk (batch D's): a case, a small screen set high, feet; dark when off, a soft line when on"""
    x0, y0, x1, y1 = K.bbox()
    K.fn(lambda x, y: "pFrame")
    K.rect(x0 + 3, y0 + 3, x1 - 3, y0 + 9, "pOn" if on else "pFace")
    K.hline(x0 + 3, x1 - 3, y0 + 3, "OUT")
    for yy in (y0 + 5, y0 + 7):
        K.hline(x0 + 5, x1 - 6 - (yy - y0 - 5), yy, "pLine" if not on else "pLit")
    K.hline(x0 + 1, x1 - 1, y0 + 1, "pLight")
    K.vline(x0 + 1, y0 + 1, y1 - 4, "pLight")
    K.vline(x1 - 1, y0 + 2, y1 - 4, "pFace")
    K.rect(x0 + 2, y1 - 3, x1 - 2, y1 - 2, "pFace")
    K.hline(x0 + 3, x1 - 3, y1 - 3, "pLine")
    K.rim("OUT")


def p_port_off(K, D):
    p_port_screen(K, D, False)


def p_port_on(K, D):
    p_port_screen(K, D, True)


def p_tvstand(K, D):
    """the set on its stand: a timber cabinet, a dark screen"""
    x0, y0, x1, y1 = K.bbox()
    K.fn(lambda x, y: "pWood")
    K.hline(x0, x1, y0, "pWoodL")
    K.rect(x0 + 3, y0 + 3, x1 - 4, y0 + 10, "pDark")
    K.hline(x0 + 4, x0 + 7, y0 + 4, "pLine")
    K.px(x1 - 3, y0 + 5, "pWoodL")
    K.px(x1 - 3, y0 + 8, "pWoodL")
    K.rect(x0 + 3, y0 + 12, x1 - 3, y1 - 1, "pFace")
    K.hline(x0 + 3, x1 - 3, y0 + 12, "pWoodL")
    K.rim("OUT")


def p_doll(K, D):
    """vanilla's games console and its cable (the COPYCAT's room) -> a pull-along wooden duck and its string, DRAFT"""
    K.fill("dollD")
    for y in range(2, 10):
        for x in range(3, 13):
            if ((x - 7.5) / 5.0) ** 2 + ((y - 6.5) / 3.6) ** 2 < 1:
                K.px(x, y, "doll")
    K.rect(9, 1, 12, 4, "doll")
    K.px(13, 3, "dollB")
    K.px(10, 2, "OUT")
    K.hline(4, 9, 6, "dollL")
    for cx in (5, 10):
        K.rect(cx - 1, 9, cx, 10, "OUT")
    for y in range(11, 16):
        for x in range(0, 8):
            if K.foot(x, y):
                K.px(x, y, "dollB" if (x + y) % 3 else "dollD")
    K.rim("OUT")


# ---- primary/building's leftovers
def p_bed(K, D):
    """the rest-room bed: head against the wall, a pillow, the quilt the direction's"""
    x0, y0, x1, y1 = K.bbox()
    K.fn(lambda x, y: "BQ")
    K.rect(x0, y0, x1, y0 + 3, D["bedhead"])
    K.hline(x0, x1, y0 + 4, "OUT")
    K.rect(x0 + 2, y0 + 5, x1 - 2, y0 + 9, "BS")
    K.hline(x0 + 2, x1 - 2, y0 + 9, "BSD")
    D["quilt"](K, x0, y0 + 11, x1, y1)
    K.hline(x0, x1, y0 + 10, "BQL")
    K.rim("OUT")


def p_doorway(K, D):
    """an open doorway to a back room: the frame the direction's, the dark beyond"""
    zones(K, D, D["pz"])
    x0, y0, x1, y1 = K.bbox()
    D["frame"](K, x0, y0, x1, y1)


def p_partition(K, D):
    zones(K, D, D["pz"])
    D["screen"](K)


def p_blinds(K, D):
    x0, y0, x1, y1 = K.bbox()
    D["blind"](K, x0, y0, x1, y1)


def p_loungerug(K, D):
    """the lounge rug's border, around a field that stays as it is"""
    x0, y0, x1, y1 = K.bbox()
    D["rugedge"](K, x0, y0, x1, y1)


def p_pzones(K, D):
    zones(K, D, D["pz"])


# ============================================================================================ the groups
def M(*rows):
    return [list(r) for r in rows]


def h(t):
    return (t, "h")


def v(t):
    return (t, "v")


def hv(t):
    return (t, "hv")


#  key, set, layout (as it stands), painter, what it is
GROUPS = [
    ("floor",      "gb2", M([32, 33], [48, 49]),                         p_floor_lit,   "the road houses' floor, lit"),
    ("floorshade", "gb2", M([34, 35], [50, 51]),                         p_floor_shade, "the same floor in a wall's shade"),
    ("valance",    "gb2", M([1, h(1)], [17, h(17)]),                     p_valance,     "the upper wall with vanilla's valance"),
    ("wall",       "gb2", M([2, 2], [18, 18]),                           p_plainwall,   "the plain wall and its foot"),
    ("wallend",    "gb2", M([128, 130, h(130), h(128)], [144, 17, h(17), h(144)]), p_zones, "the wall's ends in an alcove"),
    ("wallside",   "gb2", M([129, 2], [145, 18]),                        p_zones,       "a wall's side edge"),
    ("ledge",      "gb2", M([147, 131, 131, h(147)]),                    p_zones,       "the 2F gallery's ledge"),
    ("winvalance", "gb2", M([11, 12, 13]),                               p_wallwin,     "windows under the valance"),
    ("winwall",    "gb2", M([27, 28, 29]),                               p_wallwin,     "windows in the plain wall"),
    ("view",       "gb2", M([38, 39, 40, 41], [54, 55, 56, 57]),         p_view,        "the 2F's long north windows"),
    ("panes",      "gb2", M([42, 43, 44, 45], [58, 59, 60, 61]),         p_view,        "the low panes at the 2F window"),
    ("spyglass",   "gb2", M([14, 15], [30, 31]),                         p_spyglass,    "the coin binoculars -> a spyglass"),
    ("light",      "gb2", M([36, 37], [52, 53]),                         p_lightpatch,  "the floor in a window's light"),
    ("stand",      "gb2", M([46, 47]),                                   p_stand,       "the spyglass stand's foot"),
    ("counter",    "gb2", M([19, 20, 8, 8, h(20), h(19)], [5, 6, 24, 24, h(6), h(5)]), p_zones, "the counter, its top and front"),
    ("counterv",   "gb2", M([9, 10, 25], [9, 23, 10]),                   p_zones,       "the counter's runs along"),
    ("counterwall", "gb2", M([3, 4]),                                    p_zones,       "the counter against the wall"),
    ("edge",       "gb2", M([21, 7, 7, h(21)]),                          p_zones,       "a step's edge on the floor"),
    ("stairs",     "gb2", M([64, 65, 66, 67, 68, 69, 70, 71], [72, 73, 74, 75, 76, 77, 78, 79],
                            [81, 82, 83, 84, 85, 86, 87, 88], [89, 90, 91, 92, 93, 94, 96, 97],
                            [98, 99, 112, 113, 114, 115, None, None]), p_zones, "the stairs, banisters and counter ends"),
    ("runner",     "gb2", M([107, 108, h(107)], [123, 124, h(123)], [v(107), v(108), hv(107)]), p_runner,
     "the road houses' long runner"),
    ("rug",        "gb2", M([132, 133, h(132)], [148, 149, h(148)], [v(132), v(133), hv(132)]), p_rug, "the houses' rug"),
    ("plinth",     "gb2", M([134, 135], [150, 151]),                     p_strongbox,   "the statue's plinth (row 0; ROUTE 22)"),
    ("hatch",      "gb2", M([109, 110, h(110), h(109)]),                 p_hatch,       "a hatch let into the wall"),
    ("doors",      "gb2", M([125, 126, h(126), h(125)], [141, 142, h(142), h(141)]), p_doors, "a doorway, its leaves open"),
    ("doorfoot",   "gb2", M([143]),                                      p_zones,       "the doorway's sill"),
    ("rugcorner",  "gb2", M([136]),                                      p_zones,       "a rug's corner in the dark (row 9)"),
    ("port_off",   "gb1", M([19, 20], [35, 36]),                         p_port_off,    "the PORT, off (0x288, 0x28F)"),
    ("port_on",    "gb1", M([13, 14], [29, 30]),                         p_port_on,     "the PORT, on (0x28A)"),
    ("tv",         "gb1", M([1, 2], [17, 18]),                           p_tvstand,     "the set on its stand"),
    ("toy",        "gb1", M([45, 46], [61, 62]),                         p_doll,        "the console and cable -> a pull-along duck"),
    ("bed",        "P",   M([512, 513, 514, 515], [528, 529, 530, 531], [544, 545, 546, 547]), p_bed,
     "the rest-room beds (FOUNDRY 8F/9F, LORELEI's house)"),
    ("doorway",    "P",   M([522, 523, 524], [538, 539, 540], [554, 555, 556]), p_doorway, "the open doorways"),
    ("partition",  "P",   M([171, None], [187, None], [180, 181], [196, 197]), p_partition, "the white partitions"),
    ("loungerug",  "P",   M([420, 421, h(420)], [436, 437, h(436)], [v(420), v(421), hv(420)]), p_loungerug,
     "the lab lounge's rug, its border (its field, 437, is one flat colour: kept)"),
    ("blinds",     "P",   M([432, 433]),                                 p_blinds,      "the lab lounge's side blinds"),
    ("odd",        "P",   M([368]),                                      p_pzones,      "lab-lobby tile 368"),
]


# ============================================================================================ resolving materials
def nearest(c, cols):
    return min(range(1, 16), key=lambda i: sum((a - b) ** 2 for a, b in zip(cols[i], c)) if cols[i] else 1e9)


def set_palettes(D, S):
    """{row: 16 colours} for a secondary's own rows: vanilla's index 0, then the direction's 15 materials"""
    out = {}
    for r in range(16):
        if r in S.rows:
            out[r] = [S.vpal[r][0]] + [D["mat"][m] for m in D["rows"][S.key, r]]
        else:
            out[r] = list(S.vpal[r])
    return out


def resolve(mats, base, rows, D, spals):
    """64 materials -> 64 indices for one tile placed in ROWS (weights); FOOTPRINT exact (0 stays 0, drawn 1..15)"""
    px, cache = [], {}
    for k, m in enumerate(mats):
        if base[k] == 0:
            px.append(0)
            continue
        if m is None:
            m = "OUT"
        if m not in cache:
            c = D["mat"][m]
            best, bd = 1, 1e18
            for i in range(1, 16):
                d = 0
                for r, w in rows.items():
                    col = spals[r][i] if r in spals else PPAL[r][i] if r < 7 else (0, 0, 0)
                    d += w * sum((a - b) ** 2 for a, b in zip(col, c))
                if d < bd:
                    best, bd = i, d
            #  an own-row material is placed by index, exactly
            own = [r for r in rows if r in spals]
            if len(rows) == 1 and own and (own[0], m) in D["_index"]:
                best = D["_index"][own[0], m]
            cache[m] = best
        px.append(cache[m])
    return px


def draw(D):
    """-> {setkey: (tiles, palettes)}, primary {tile: px}, owner {(setkey, t): group}"""
    out = {}
    for key, S in SETS.items():
        out[key] = ([t[:] for t in S.cur], set_palettes(D, S))
    prim = {}
    owner = {}
    for key, setkey, layout, painter, what in GROUPS:
        K = Cv(layout, setkey)
        K.row = None
        if setkey != "P":
            S = SETS[setkey]
            t0 = next(s[0] for r in K.layout for s in r if s is not None)
            K.row = S.home(t0) if S.use.get(t0) else S.rows[-1]     # an unplaced tile: zones read the set's last row
        painter(K, D)
        for t, mats in K.tiles().items():
            if (setkey, t) in owner:
                continue
            if setkey == "P":
                if t not in PRIMARY_ALL:
                    continue
                rows = dict(PUSE[t]["rows"]) if t in PUSE else {0: 1}
                D["_index"] = {}
                prim[t] = resolve(mats, ptile(t), rows, D, {})
            else:
                S = SETS[setkey]
                if t >= S.nvan or (t not in S.use and (setkey, t) not in NAMED_UNPLACED):
                    continue
                spals = out[setkey][1]
                rows = dict(S.use[t]["rows"]) if t in S.use and S.use[t]["rows"] else {0: 1}   # 0x28A: row 0
                D["_index"] = {(r, m): i + 1 for r in S.rows for i, m in enumerate(D["rows"][S.key, r])}
                own = {r: spals[r] for r in S.rows}
                out[setkey][0][t] = resolve(mats, S.van[t], rows, D, own)
            owner[setkey, t] = key
    return out, prim, owner


# ============================================================================================ the directions
GREYS = dict(OUT=(58, 46, 40), SHD=(96, 82, 72), MID=(150, 138, 124), HI=(208, 198, 182), WHT=(246, 240, 226),
             #  batch D's PORT and TV, in primary row 0's own colours: the same object in every direction
             pFrame=(150, 144, 134), pFace=(128, 86, 54), pLight=(232, 224, 206), pLine=(150, 186, 204),
             pOn=(150, 186, 204), pLit=(232, 224, 206), pWood=(176, 122, 76), pWoodL=(214, 166, 112),
             pDark=(74, 104, 130))


def zmaps(counter_top, counter_front, glass=("GD", "GL", "GH")):
    """vanilla's indices -> materials, per (set, row): structure keeps its zones"""
    g = glass
    z12 = {1: "OUT", 2: counter_front[0], 3: counter_front[1], 4: "HI", 5: "FLOORS", 6: "FLOOR", 7: "FLOOR",
           8: g[0], 9: g[1], 10: g[2], 13: "X", 14: counter_top[1], 15: counter_top[0]}
    z7 = {1: "OUT", 2: "SHD", 3: "MID", 4: "WT", 5: "W1", 6: "W2", 7: "W3", 8: "WT", 9: "S1", 10: "S2",
          11: g[0], 12: g[1], 13: g[2]}
    z9 = {1: "OUT", 2: "SHD", 3: "MID", 4: "HI", 13: "X", 14: "XL"}
    z9.update({i: "SHD" for i in range(5, 13)})
    z9[15] = "OUT"
    return {("gb2", 12): z12, ("gb2", 7): z7, ("gb2", 9): z9, ("gb2", 8): z12, ("gb1", 8): z12}


def pz_map(D):
    """primary rows' vanilla indices -> materials, for the doorways, partitions and 368 (zones kept)"""
    return {1: "OUT", 2: "SHD", 3: D["pzLight"], 4: "WHT", 5: D["pzA"], 6: D["pzB"], 7: D["pzC"], 8: "GD", 9: "GL",
            10: "GH", 11: "CF", 12: "CT", 13: "CTL", 14: D["pzLight"], 15: "MID"}


# ---- A HEARTH: the road houses kept like front rooms
def A_floor(x, y, shade):
    """terracotta quarry tiles, 8px, a pale grout line, one tile in five a shade worn"""
    if x % 8 == 7 or y % 8 == 7:
        return "F0" if shade else "F1"
    worn = H(x // 8, y // 8, 3) % 5 == 0
    base = ("F1" if shade else "F2") if not worn else ("F0" if shade else "F1")
    if (x % 8, y % 8) in ((0, 0), (1, 0), (0, 1)):
        return "F2" if shade else "F3"
    return base


def A_wall(x, y):
    """limewash over timber-framed plaster: a soft speckle, a post every 32px"""
    if y < 2:
        return "WT" if y == 1 else "OUT"
    return "W3" if H(x, y, 1) % 17 else "W2"


def A_pelmet(K):
    """a gingham pelmet on a timber rail where the valance hung"""
    K.hline(0, K.w - 1, 2, "CF")
    K.hline(0, K.w - 1, 3, "CT")
    for y in range(4, 9):
        for x in range(K.w):
            if y == 8 and (x % 8) in (3, 4):
                continue
            K.px(x, y, "P2" if ((x // 2) + (y // 2)) % 2 else "P1")
    K.hline(0, K.w - 1, 9, "W2")


def A_skirting(K):
    K.hline(0, K.w - 1, 9, "CF")
    K.hline(0, K.w - 1, 8, "CTL")
    for y in range(10, 14):
        for x in range(K.w):
            K.px(x, y, "W2" if H(x, y, 2) % 11 else "W1")
    K.hline(0, K.w - 1, 13, "S2")
    K.rect(0, 14, K.w - 1, 15, "S1")


def A_panes(K, x0, y0, x1, y1):
    """leaded lights: small panes in a timber frame"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x - x0) % 6 == 5 or (y - y0) % 5 == 4:
                K.px(x, y, "CF")
    K.hline(x0, x1, y0, "CT")
    K.hline(x0, x1, y1, "CT")


def rug_border(K, a, b, c, field):
    x0, y0, x1, y1 = K.bbox()
    K.fn(lambda x, y: field(x, y))
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = min(x - x0, x1 - x, y - y0, y1 - y)
            if d == 0:
                K.px(x, y, a)
            elif d == 1:
                K.px(x, y, b)
            elif d == 2:
                K.px(x, y, c if (x + y) % 2 else b)


def A_runner(K):
    """a rag rug: stripes of the household's old cloth"""
    rug_border(K, "R1", "R2", "R3", lambda x, y: ["R2", "R3", "R4", "R3"][(y // 2) % 4]
               if H(x // 3, y // 2, 5) % 9 else "R1")


def A_rug(K):
    """a braided oval's worth of colour: a hooked rug, flowers in its field"""
    def field(x, y):
        if (x % 8, y % 8) in ((3, 3), (4, 4), (3, 4), (4, 3)):
            return "Q4"
        if (x % 8, y % 8) in ((3, 2), (2, 3), (5, 4), (4, 5)):
            return "Q1"
        return "Q3"
    rug_border(K, "Q1", "Q2", "Q4", field)


def A_stove(K):
    """the statue's plinth: a dressed sandstone block, a moulded cap, a timber base"""
    x0, y0, x1, y1 = K.bbox()
    K.fn(lambda x, y: "MID")
    K.rect(x0 + 1, y0 + 3, x1 - 1, y1 - 3, "HI")
    K.vline(x1 - 2, y0 + 3, y1 - 3, "MID")
    K.rect(x0, y0, x1, y0 + 2, "WHT")
    K.hline(x0, x1, y0 + 2, "MID")
    for y in range(y0 + 5, y1 - 3, 3):
        K.hline(x0 + 2, x1 - 3, y, "MID" if H(y, 0, 7) % 2 else "HI")
    K.rect(x0, y1 - 2, x1, y1, "CF")
    K.hline(x0, x1, y1 - 2, "CT")
    K.rim("OUT")


def doors_common(K, leaf, leafD, leafL, dark="SHD"):
    x0, y0, x1, y1 = K.bbox()
    K.fn(lambda x, y: dark)
    K.rect(x0 + 6, y0, x1 - 6, y1, "OUT")
    K.rect(x0 + 7, y0 + 2, x1 - 7, y1, dark)
    for (a, b) in ((x0, x0 + 5), (x1 - 5, x1)):
        K.rect(a, y0, b, y1, leaf)
        K.vline(a, y0, y1, leafL)
        K.vline(b, y0, y1, leafD)
        for y in range(y0 + 3, y1 - 1, 5):
            K.hline(a + 1, b - 1, y, leafD)
    K.hline(x0, x1, y0, "OUT")


def A_doors(K):
    doors_common(K, "CT", "CF", "CTL")


def A_bedhead(K):
    pass


def A_quilt(K, x0, y0, x1, y1):
    """a patchwork quilt: four cloths in a 4px check"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            K.px(x, y, ["BQ", "BQL", "BQD", "BQ"][((x - x0) // 4 + 2 * ((y - y0) // 4)) % 4])


def A_frame(K, x0, y0, x1, y1):
    """a timber door frame with a lintel"""
    K.rect(x0, y0, x1, y0 + 2, "CT")
    K.hline(x0, x1, y0 + 2, "CF")
    for x in (x0, x0 + 1, x1 - 1, x1):
        K.vline(x, y0, y1, "CT" if x in (x0, x1 - 1) else "CF")


def A_screen(K):
    """the white partitions as timber screens: boards with a darker joint"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y) and K.out[y][x] in ("WHT", "HI", "GH", "MID") and x % 4 == 3:
                K.out[y][x] = "CF"


def A_rugedge(K, x0, y0, x1, y1):
    """a braided border: two strands of the household's cloth plaited"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = min(x - x0, x1 - x, y - y0, y1 - y)
            if d == 0:
                K.px(x, y, "CF")
            elif d in (1, 2, 3, 4):
                K.px(x, y, ("BQ", "BQL", "BQD")[(x + y + d) % 3] if d in (2, 3) else "CT")


def A_blind(K, x0, y0, x1, y1):
    """linen roller blinds half down: the cloth, its pull, the sun behind it"""
    K.fn(lambda x, y: "BS")
    for y in range(y0, y1 + 1):
        if (y - y0) % 4 == 3:
            K.hline(x0, x1, y, "BSD")
    K.hline(x0, x1, y0, "CT")
    K.hline(x0, x1, y0 + 1, "CF")
    K.rim("OUT")


A = dict(
    name="A", title="HEARTH",
    lines=["The road houses kept like front rooms by the people who live on the road: terracotta quarry tiles,",
           "limewash over timber, a gingham pelmet where the valance hung, oak counters, leaded lights, a rag rug",
           "down the middle, sandstone plinths, brass coin-viewers at the north window. The beds patchwork."],
    mat=dict(GREYS,
             F0=(150, 84, 58), F1=(178, 104, 70), F2=(200, 126, 86), F3=(224, 164, 120),
             W1=(196, 176, 150), W2=(226, 212, 186), W3=(242, 232, 210), WT=(176, 122, 76),
             P1=(196, 82, 72), P2=(244, 232, 214), S1=(128, 86, 54), S2=(176, 122, 76),
             CT=(176, 122, 76), CTL=(214, 166, 112), CF=(128, 86, 54),
             GD=(110, 150, 170), GL=(170, 206, 214), GH=(226, 240, 236),
             R1=(128, 86, 54), R2=(172, 86, 78), R3=(90, 120, 150), R4=(214, 180, 98),
             Q1=(96, 64, 42), Q2=(90, 120, 78), Q3=(150, 170, 110), Q4=(214, 136, 108),
             X=(196, 150, 80), XL=(240, 180, 90),
             BS=(240, 232, 214), BSD=(204, 192, 172), BQ=(172, 86, 78), BQD=(90, 120, 150), BQL=(214, 180, 98),
             case=(176, 122, 76), caseL=(214, 166, 112), caseD=(128, 86, 54), scr=(60, 56, 64),
             scrOn=(84, 96, 90), scrL=(150, 198, 120), doll=(176, 140, 100), dollL=(232, 212, 170),
             dollD=(128, 86, 54), dollB=(214, 166, 112)),
    floor=A_floor, wall=A_wall, pelmet=A_pelmet, skirting=A_skirting, panes=A_panes, runner=A_runner, rug=A_rug,
    stove=A_stove, doors=A_doors, metal="X", metalL="XL", metalD="CF", bedhead="CT", quilt=A_quilt, frame=A_frame,
    screen=A_screen, blind=A_blind, rugedge=A_rugedge, pzLight="HI", pzA="CF", pzB="CT", pzC="CTL",
    grain=dict(),
)

# ---- B THE WAYMARK: the road houses as the numbered road's own offices
def B_floor(x, y, shade):
    """slate flags, 16 by 8, laid in courses, a cool seam; the lit ones catch a sheen"""
    off = 8 if (y // 8) % 2 else 0
    if y % 8 == 7 or (x + off) % 16 == 15:
        return "F0"
    if shade:
        return "F1" if H((x + off) // 16, y // 8, 4) % 3 else "F0"
    s = H((x + off) // 16, y // 8, 4) % 3
    return ("F2", "F3", "F2")[s] if (x + y) % 9 else "F3"


def B_wall(x, y):
    """painted tongue-and-groove, sage, a groove every 4px"""
    if y < 2:
        return "WT" if y == 1 else "OUT"
    return "W2" if x % 4 == 3 else "W3"


def B_pelmet(K):
    """an enamel band where the valance hung: blue, with a cream rule, blank (the road's number is never written)"""
    K.hline(0, K.w - 1, 2, "OUT")
    K.rect(0, 3, K.w - 1, 7, "P1")
    K.hline(0, K.w - 1, 4, "P2")
    K.hline(0, K.w - 1, 8, "OUT")


def B_skirting(K):
    K.hline(0, K.w - 1, 8, "WT")
    for y in range(9, 14):
        for x in range(K.w):
            K.px(x, y, "W1" if x % 8 == 7 else "W2")
    K.hline(0, K.w - 1, 13, "S2")
    K.rect(0, 14, K.w - 1, 15, "S1")


def B_panes(K, x0, y0, x1, y1):
    """sash windows: two big panes, a meeting rail, painted frames"""
    mx = (x0 + x1) // 2
    for x in range(x0, x1 + 1):
        if (x - x0) % 16 == 15:
            K.vline(x, y0, y1, "WT")
    K.hline(x0, x1, (y0 + y1) // 2, "WT")
    K.hline(x0, x1, y0, "WT")


def B_runner(K):
    """a survey runner: cream, contour lines in blue (a map with no names on it)"""
    def field(x, y):
        d = int(((x - 6) ** 2 * 0.5 + (y - 9) ** 2) ** 0.5)
        return "R3" if d % 4 == 0 else "R4"
    rug_border(K, "R1", "R2", "R2", field)


def B_rug(K):
    """a plain wool rug, a deep border, a quiet grid"""
    rug_border(K, "Q1", "Q2", "Q2", lambda x, y: "Q4" if (x % 6 == 0 or y % 6 == 0) else "Q3")


def B_stove(K):
    """the statue's plinth as a milestone: blank stone, a blue enamel plate with nothing on it"""
    x0, y0, x1, y1 = K.bbox()
    K.fn(lambda x, y: "MID")
    K.rect(x0 + 2, y0 + 1, x1 - 2, y1 - 1, "HI")
    K.vline(x1 - 2, y0 + 2, y1 - 1, "MID")
    K.rect(x0 + 4, y0 + 4, x1 - 4, y0 + 9, "P1")
    K.hline(x0 + 4, x1 - 4, y0 + 5, "P2")
    K.hline(x0 + 2, x1 - 2, y0 + 1, "WHT")
    K.rim("OUT")


def B_doors(K):
    doors_common(K, "W2", "W1", "W3")


def B_quilt(K, x0, y0, x1, y1):
    """a grey wool blanket, a blue stripe across its foot"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            K.px(x, y, "BQD" if (y1 - y) in (2, 3) else ("BQL" if (x + y) % 7 == 0 else "BQ"))


def B_frame(K, x0, y0, x1, y1):
    K.rect(x0, y0, x1, y0 + 1, "W2")
    for x in (x0, x1):
        K.vline(x, y0, y1, "W2")


def B_screen(K):
    pass


def B_rugedge(K, x0, y0, x1, y1):
    """a plain wool border, a single cream rule"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = min(x - x0, x1 - x, y - y0, y1 - y)
            if d <= 4:
                K.px(x, y, "BQD" if d != 2 else "BS")


def B_blind(K, x0, y0, x1, y1):
    """venetian slats, half open"""
    K.fn(lambda x, y: "HI" if (y - y0) % 2 == 0 else "MID")
    K.vline(x0 + 3, y0, y1, "SHD")
    K.hline(x0, x1, y0, "OUT")
    K.rim("OUT")


B = dict(
    name="B", title="THE WAYMARK",
    lines=["The road houses as the numbered road's own offices (3.2: the institution navigates by number, the",
           "residents by name): slate flags, sage tongue-and-groove, a blue enamel band where the valance hung --",
           "blank, the number is never written -- sash windows, a survey runner of contour lines with no names, a",
           "milestone for each statue's plinth. Beds in grey wool, blinds venetian."],
    mat=dict(GREYS,
             F0=(74, 82, 92), F1=(98, 108, 118), F2=(126, 136, 144), F3=(156, 166, 172),
             W1=(120, 146, 118), W2=(150, 176, 140), W3=(186, 206, 170), WT=(240, 234, 214),
             P1=(56, 86, 140), P2=(240, 234, 214), S1=(70, 82, 74), S2=(110, 128, 106),
             CT=(186, 206, 170), CTL=(222, 232, 206), CF=(110, 128, 106),
             GD=(110, 150, 184), GL=(176, 206, 230), GH=(232, 242, 246),
             R1=(56, 86, 140), R2=(98, 122, 162), R3=(98, 122, 162), R4=(238, 228, 200),
             Q1=(70, 82, 74), Q2=(120, 146, 118), Q3=(200, 190, 160), Q4=(176, 164, 132),
             X=(56, 86, 140), XL=(150, 186, 204),
             BS=(240, 236, 226), BSD=(200, 198, 190), BQ=(130, 134, 138), BQD=(56, 86, 140), BQL=(170, 172, 172),
             case=(180, 180, 164), caseL=(232, 230, 226), caseD=(123, 123, 123), scr=(82, 82, 106),
             scrOn=(70, 96, 84), scrL=(150, 198, 120), doll=(200, 190, 160), dollL=(240, 236, 226),
             dollD=(120, 110, 96), dollB=(150, 140, 120)),
    floor=B_floor, wall=B_wall, pelmet=B_pelmet, skirting=B_skirting, panes=B_panes, runner=B_runner, rug=B_rug,
    stove=B_stove, doors=B_doors, metal="MID", metalL="HI", metalD="SHD", bedhead="MID", quilt=B_quilt,
    frame=B_frame, screen=B_screen, blind=B_blind, rugedge=B_rugedge, pzLight="HI", pzA="W1", pzB="W2", pzC="W3",
    grain=dict(),
)


# ---- C FOUNDRY TOWN: the works' iron reaching every house
def C_floor(x, y, shade):
    """brick pavers in herringbone, a dark joint"""
    a = (x + y) % 8
    joint = (a == 7) or ((x // 4 + y // 4) % 2 == 0 and x % 4 == 3) or ((x // 4 + y // 4) % 2 == 1 and y % 4 == 3)
    if joint:
        return "F0"
    if shade:
        return "F1"
    return "F3" if H(x // 4, y // 4, 6) % 7 == 0 else "F2"


def C_wall(x, y):
    """exposed brick, limewashed pale, the courses showing"""
    if y < 2:
        return "WT" if y == 1 else "OUT"
    off = 4 if (y // 4) % 2 else 0
    if y % 4 == 3 or (x + off) % 8 == 7:
        return "W2"
    return "W3"


def C_pelmet(K):
    """an iron picture rail with rivets where the valance hung"""
    K.hline(0, K.w - 1, 2, "OUT")
    K.rect(0, 3, K.w - 1, 5, "P1")
    for x in range(2, K.w, 6):
        K.px(x, 4, "P2")
    K.hline(0, K.w - 1, 6, "OUT")


def C_skirting(K):
    K.hline(0, K.w - 1, 9, "OUT")
    K.rect(0, 10, K.w - 1, 13, "CT")
    K.hline(0, K.w - 1, 10, "CTL")
    for x in range(K.w):
        if x % 8 == 7:
            K.vline(x, 10, 13, "CF")
    K.rect(0, 14, K.w - 1, 15, "S1")


def C_panes(K, x0, y0, x1, y1):
    """factory glazing: an iron grid of small panes"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x - x0) % 4 == 3 or (y - y0) % 4 == 3:
                K.px(x, y, "S1")


def C_runner(K):
    """a jute runner, bound in leather"""
    rug_border(K, "R1", "R2", "R2", lambda x, y: "R4" if (x + 2 * y) % 5 == 0 else "R3")


def C_rug(K):
    """a kilim in the works' colours: bronze border, rust field, a stepped diamond"""
    rug_border(K, "Q2", "Q1", "Q2", lambda x, y: "Q4" if (abs(x % 12 - 6) + abs(y % 12 - 6)) in (3, 4) else "Q3")


def C_stove(K):
    """the statue's plinth cast in iron: panelled sides, a bronze band, rivets"""
    x0, y0, x1, y1 = K.bbox()
    K.fn(lambda x, y: "SHD")
    K.rect(x0, y0, x1, y0 + 2, "MID")
    K.hline(x0, x1, y0 + 2, "OUT")
    K.rect(x0 + 2, y0 + 5, x1 - 2, y1 - 4, "OUT")
    K.rect(x0 + 3, y0 + 6, x1 - 3, y1 - 5, "SHD")
    K.hline(x0, x1, y0 + 4, "X")
    for x, y in ((x0 + 1, y0 + 6), (x1 - 1, y0 + 6), (x0 + 1, y1 - 3), (x1 - 1, y1 - 3)):
        K.px(x, y, "XL")
    K.rect(x0, y1 - 2, x1, y1, "OUT")


def C_doors(K):
    doors_common(K, "S2", "S1", "MID")


def C_quilt(K, x0, y0, x1, y1):
    """a felted blanket, a bronze-stitched hem"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            K.px(x, y, "BQL" if y == y1 - 1 and x % 2 == 0 else ("BQD" if (x + y) % 6 == 0 else "BQ"))


def C_frame(K, x0, y0, x1, y1):
    """an iron frame, riveted"""
    K.rect(x0, y0, x1, y0 + 1, "S2")
    for x in (x0, x1):
        K.vline(x, y0, y1, "S2")
    for y in range(y0 + 2, y1, 4):
        K.px(x0, y, "X")
        K.px(x1, y, "X")


def C_screen(K):
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y) and (x % 8, y % 8) == (2, 2):
                K.out[y][x] = "X"


def C_rugedge(K, x0, y0, x1, y1):
    """a leather-bound border with bronze studs"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = min(x - x0, x1 - x, y - y0, y1 - y)
            if d <= 4:
                K.px(x, y, "X" if d == 2 and (x + y) % 4 == 0 else ("CF" if d in (0, 4) else "CT"))


def C_blind(K, x0, y0, x1, y1):
    """iron shutters, folded: ribbed sheet"""
    K.fn(lambda x, y: "S2" if (x - x0) % 3 else "S1")
    K.hline(x0, x1, y0, "OUT")
    K.rim("OUT")


C = dict(
    name="C", title="FOUNDRY TOWN",
    lines=["FOUNDRY CO.'s works reaching every house (T-536 C, T-537 A): brick pavers in herringbone, limewashed",
           "brick, an iron picture rail riveted where the valance hung, oak counters on iron, factory glazing, a",
           "jute runner, a kilim under each statue on a cast-iron plinth, iron coin-viewers. Felt blankets."],
    mat=dict(GREYS,
             F0=(92, 56, 42), F1=(132, 78, 56), F2=(164, 98, 70), F3=(196, 128, 92),
             W1=(150, 120, 100), W2=(196, 176, 158), W3=(230, 218, 200), WT=(170, 112, 52),
             P1=(70, 74, 82), P2=(220, 166, 96), S1=(52, 48, 50), S2=(84, 90, 98),
             CT=(150, 104, 66), CTL=(196, 146, 98), CF=(96, 66, 50),
             GD=(96, 120, 132), GL=(150, 172, 176), GH=(214, 226, 222),
             R1=(96, 66, 50), R2=(140, 98, 72), R3=(196, 170, 120), R4=(160, 134, 92),
             Q1=(52, 48, 50), Q2=(170, 112, 52), Q3=(120, 60, 50), Q4=(170, 90, 60),
             X=(170, 112, 52), XL=(240, 140, 40),
             BS=(236, 228, 210), BSD=(196, 186, 168), BQ=(110, 92, 80), BQD=(84, 70, 62), BQL=(220, 166, 96),
             case=(110, 104, 104), caseL=(150, 144, 134), caseD=(84, 72, 70), scr=(60, 56, 64),
             scrOn=(84, 72, 70), scrL=(226, 150, 84), doll=(160, 134, 92), dollL=(220, 200, 160),
             dollD=(96, 66, 50), dollB=(170, 112, 52)),
    floor=C_floor, wall=C_wall, pelmet=C_pelmet, skirting=C_skirting, panes=C_panes, runner=C_runner, rug=C_rug,
    stove=C_stove, doors=C_doors, metal="X", metalL="XL", metalD="S1", bedhead="S2", quilt=C_quilt, frame=C_frame,
    screen=C_screen, blind=C_blind, rugedge=C_rugedge, pzLight="HI", pzA="S1", pzB="S2", pzC="MID", grain=dict(),
)

STYLES = {"A": A, "B": B, "C": C}

#  each own row's fifteen materials, in index order 1..15 (the same layout in every direction)
ROWMATS = {
    ("gb2", 12): ["OUT", "SHD", "MID", "HI", "WHT", "F0", "F1", "F2", "F3", "CT", "CTL", "CF", "GL", "X", "XL"],
    ("gb2", 7):  ["OUT", "SHD", "MID", "HI", "WHT", "W1", "W2", "W3", "WT", "P1", "P2", "S1", "S2", "CT", "CF"],
    ("gb2", 8):  ["OUT", "SHD", "MID", "HI", "WHT", "R1", "R2", "R3", "R4", "Q1", "Q2", "Q3", "Q4", "X", "XL"],
    ("gb2", 9):  ["OUT", "SHD", "MID", "HI", "WHT", "F0", "F1", "F2", "F3", "CT", "CTL", "CF", "GL", "X", "XL"],
    ("gb1", 8):  ["OUT", "SHD", "MID", "HI", "WHT", "case", "caseL", "caseD", "scr", "scrOn", "scrL", "doll",
                  "dollL", "dollD", "dollB"],
}
for _D in STYLES.values():
    _D["rows"] = ROWMATS
    _D["zones"] = zmaps(("CT", "CTL"), ("CF", "CT"))
    _D["pz"] = pz_map(_D)
    _D["mat"].setdefault("GD", (110, 150, 170))
#  the glass in row 12 has one slot (GL); its dark and highlight resolve to the nearest -- MID and WHT


# ============================================================================================ rendering any room
_TS = {}


def tileset_data(sym):
    if sym not in _TS:
        td, md = tileset_dirs(sym)
        td = td or md
        _TS[sym] = dict(tiles=tiles_of(Image.open(os.path.join(GBA, td, "tiles.png"))),
                        mt=open(os.path.join(GBA, md, "metatiles.bin"), "rb").read(),
                        pals=[read_pal(os.path.join(GBA, td, "palettes/%02d.pal" % n)) for n in range(16)])
    return _TS[sym]


PTILES_NOW = tiles_of(Image.open(os.path.join(GBA, PRI, "tiles.png")))
PMT = open(os.path.join(GBA, PRI, "metatiles.bin"), "rb").read()


def render_map(mapname, state=None):
    """the room as the engine would draw it; state = (sets drawn, primary drawn) or None for today"""
    lid = LAYOUT_OF_MAP[mapname]
    l = next(x for x in LAYOUTS if x["id"] == lid)
    sym = l["secondary_tileset"]
    ts = tileset_data(sym)
    stiles, spals = ts["tiles"], ts["pals"]
    ptiles = PTILES_NOW
    if state:
        sets, prim = state
        for k, S in SETS.items():
            if S.sym == sym:
                stiles, pal = sets[k]
                spals = [pal[r] for r in range(16)]
        if prim:
            ptiles = list(PTILES_NOW)
            for t, px in prim.items():
                ptiles[t] = px
    pals = PPAL + [spals[r] for r in range(7, 16)]
    W, Hh = l["width"], l["height"]
    bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    img = Image.new("RGB", (W * 16, Hh * 16))
    o = img.load()
    for yy in range(Hh):
        for xx in range(W):
            m = struct.unpack_from("<H", bd, (yy * W + xx) * 2)[0] & 0x3FF
            buf, k = (PMT, m) if m < 640 else (ts["mt"], m - 640)
            ee = struct.unpack_from("<8H", buf, k * 16) if (k + 1) * 16 <= len(buf) else (0,) * 8
            for layer in (0, 1):
                for q in range(4):
                    t = ee[layer * 4 + q]
                    i = t & 0x3FF
                    src = ptiles[i] if i < 640 else (stiles[i - 640] if i - 640 < len(stiles) else [0] * 64)
                    pal = pals[(t >> 12) & 15]
                    for ty in range(8):
                        for tx in range(8):
                            sx = 7 - tx if (t >> 10) & 1 else tx
                            sy = 7 - ty if (t >> 11) & 1 else ty
                            vv = src[sy * 8 + sx]
                            if layer and vv == 0:
                                continue
                            o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = pal[vv]
    return img


# ============================================================================================ sheets
BG, INK, RED, SOFT = (250, 248, 242), (24, 24, 24), (120, 20, 30), (90, 90, 90)
ROOMS = [("Route2_ViridianForest_SouthEntrance", "a road house, 1F"), ("Route11_EastEntrance_2F", "a road house, 2F"),
         ("Route22_NorthEntrance", "ROUTE 22's road house"), ("Route12_NorthEntrance_1F", "ROUTE 12's road house"),
         ("UndergroundPath_NorthEntrance", "the UNDERGROUND PATH's door house"),
         ("SaffronCity_CopycatsHouse_2F", "the COPYCAT's room"), ("SilphCo_9F", "FOUNDRY 9F: the rest room"),
         ("FourIsland_LoreleisHouse", "LORELEI's house: the beds"),
         ("CinnabarIsland_PokemonLab_Lounge", "the lab lounge: rug border, blinds"),
         ("CinnabarIsland_PokemonLab_Entrance", "the lab lobby: doorways, 368")]
CROPS = {"SilphCo_9F": "bed"}
DETAILS = [("Route11_EastEntrance_2F", (0, 0, 13, 6), "2F: the window, the spyglass"),
           ("Route2_ViridianForest_SouthEntrance", (0, 0, 11, 7), "1F: the counter, the runner"),
           ("SaffronCity_CopycatsHouse_2F", (0, 0, 8, 8), "the PORT, the duck"),
           ("SilphCo_9F", None, "a bed")]


def find_bed():
    """where SilphCo_9F's first bed stands, for the detail crop"""
    lid = LAYOUT_OF_MAP["SilphCo_9F"]
    l = next(x for x in LAYOUTS if x["id"] == lid)
    bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    for yy in range(l["height"]):
        for xx in range(l["width"]):
            m = struct.unpack_from("<H", bd, (yy * l["width"] + xx) * 2)[0] & 0x3FF
            buf, k = (PMT, m) if m < 640 else (tileset_data(l["secondary_tileset"])["mt"], m - 640)
            if any((e & 0x3FF) in PRIMARY["bed"] for e in struct.unpack_from("<8H", buf, k * 16)):
                return (max(0, xx - 1), max(0, yy - 1), min(l["width"], xx + 5), min(l["height"], yy + 4))
    return (0, 0, 6, 6)


def text(d, xy, s, fill=INK):
    d.text(xy, s, fill=fill)


def contact_sheets(out_dir, states):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: Nintendo's tiles in these rooms (the furniture around them is already ours)"])}
    for k in STYLES:
        titles[k] = ("%s %s" % (k, STYLES[k]["title"]), STYLES[k]["lines"])
    pad = 10
    paths = []
    #  1x: two rows of rooms per state
    halves = [ROOMS[:5], ROOMS[5:]]
    for hi, rooms in enumerate(halves):
        blocks = []
        for k in names:
            st = states[k]
            ims = []
            for m, _ in rooms:
                im_ = render_map(m, st)
                if CROPS.get(m) == "bed":
                    x0, y0, x1, y1 = find_bed()
                    im_ = im_.crop((max(0, x0 - 3) * 16, max(0, y0 - 4) * 16, (x1 + 3) * 16, (y1 + 1) * 16))
                ims.append(im_)
            t, lines = titles[k]
            th = 8 + 12 * len(lines) + 16
            W = sum(i.width for i in ims) + pad * (len(ims) + 1)
            im = Image.new("RGB", (W, th + max(i.height for i in ims) + pad), BG)
            d = ImageDraw.Draw(im)
            text(d, (pad, 6), t, RED)
            for j, s in enumerate(lines):
                text(d, (pad + 150, 6 + 12 * j), s)
            x = pad
            for i, (m, cap) in zip(ims, rooms):
                text(d, (x, th - 13), cap, SOFT)
                im.paste(i, (x, th))
                x += i.width + pad
            blocks.append(im)
        W = max(b.width for b in blocks)
        sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
        d = ImageDraw.Draw(sh)
        text(d, (pad, 8), "T-538 DRAFT, batch 1 -- the road houses and the houses' leftovers, real rooms at 1x, three directions "
                          "beside today's (redrawn in place: no block, collision or palette row moves). (%d/2)"
             % (hi + 1), INK)
        y = 30
        for b in blocks:
            sh.paste(b, (0, y))
            y += b.height
        p = os.path.join(out_dir, "t538_rooms_1x_%d.png" % (hi + 1))
        sh.save(p)
        paths.append(p)
    #  3x details
    dets = [(m, crop if crop else find_bed(), cap) for m, crop, cap in DETAILS]
    rowsim = []
    for k in names:
        crops = []
        for m, (x0, y0, x1, y1), cap in dets:
            im = render_map(m, states[k]).crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
            crops.append((im.resize((im.width * 3, im.height * 3), Image.NEAREST), cap))
        rowsim.append((k, crops))
    cw = sum(c.width for c, _ in rowsim[0][1]) + pad * (len(dets) + 1) + 130
    ch = max(c.height for c, _ in rowsim[0][1]) + 24
    det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
    d = ImageDraw.Draw(det)
    text(d, (pad, 8), "T-538 DRAFT -- details at 3x: the 2F window and spyglass, the 1F counter and runner, the PORT "
                      "and the COPYCAT's pull-along duck, a rest-room bed.", INK)
    y = 30
    for k, crops in rowsim:
        text(d, (pad, y + 6), titles[k][0], RED)
        x = 130
        for c, cap in crops:
            text(d, (x, y + 2), cap, SOFT)
            det.paste(c, (x, y + 16))
            x += c.width + pad
        y += ch
    p = os.path.join(out_dir, "t538_detail_3x.png")
    det.save(p)
    paths.append(p)
    #  the tiles at 3x: generic_building_2's sheet, generic_building_1's, and the primary leftovers, per state
    cols = []
    for k in names:
        st = states[k]
        sets, prim = st if st else (None, None)
        imgs = []
        for key, S in SETS.items():
            tiles, pals = sets[key] if sets else (S.cur, {r: read_pal(os.path.join(GBA, S.dir, "palettes/%02d.pal" % r))
                                                          for r in range(16)})
            n = (S.nvan + 15) // 16
            im = Image.new("RGB", (128, n * 8), (236, 236, 236))
            o = im.load()
            for t in range(S.nvan):
                if t not in S.use and (key, t) not in NAMED_UNPLACED:
                    continue
                r = S.home(t)
                pal = pals[r] if r >= 7 else PPAL[r]
                for q in range(64):
                    vv = tiles[t][q]
                    o[(t % 16) * 8 + q % 8, (t // 16) * 8 + q // 8] = pal[vv] if vv else (200, 200, 200)
            imgs.append(im)
        pt = sorted(PRIMARY_ALL)
        im = Image.new("RGB", (128, ((len(pt) + 15) // 16) * 8), (236, 236, 236))
        o = im.load()
        for n_, t in enumerate(pt):
            r = PUSE[t]["rows"].most_common(1)[0][0] if t in PUSE else 0
            px = prim[t] if prim and t in prim else PTILES_NOW[t]
            for q in range(64):
                vv = px[q]
                o[(n_ % 16) * 8 + q % 8, (n_ // 16) * 8 + q // 8] = PPAL[r][vv] if vv else (200, 200, 200)
        imgs.append(im)
        hh = sum(i.height * 3 + 16 for i in imgs)
        col = Image.new("RGB", (384, hh), BG)
        y = 0
        dd = ImageDraw.Draw(col)
        for i, lab in zip(imgs, ("generic_building_2", "generic_building_1", "primary leftovers (%d)" % len(pt))):
            dd.text((0, y), lab, fill=SOFT)
            col.paste(i.resize((384, i.height * 3), Image.NEAREST), (0, y + 14))
            y += i.height * 3 + 16
        cols.append((titles[k][0], col))
    W = sum(c.width + pad for _, c in cols) + pad
    sh = Image.new("RGB", (W, max(c.height for _, c in cols) + 50), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 6), "T-538 DRAFT -- batch 1's tiles at 3x, each in its home row (grey: transparent; light grey "
                      "cells: unused, left as they are)", INK)
    x = pad
    for t, c in cols:
        text(d, (x, 26), t, RED)
        sh.paste(c, (x, 42))
        x += c.width + pad
    p = os.path.join(out_dir, "t538_tiles_3x.png")
    sh.save(p)
    paths.append(p)
    return paths


# ============================================================================================ writing
def save_like(path_src, tiles, out_path):
    """tiles.png as the engine keeps it: the same indexed image and palette, these tiles' indices, 4-bit"""
    im = Image.open(path_src).copy()
    w = im.size[0] // 8
    px = im.load()
    for t, p in enumerate(tiles):
        for k, vv in enumerate(p):
            px[(t % w) * 8 + k % 8, (t // w) * 8 + k // 8] = vv
    im.save(out_path, bits=4)


def write_direction(base, D):
    sets, prim, owner = draw(D)
    for key, S in SETS.items():
        dd = os.path.join(base, S.dir.split("/")[-1])
        os.makedirs(os.path.join(dd, "palettes"), exist_ok=True)
        save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[key][0], os.path.join(dd, "tiles.png"))
        for r in S.rows:
            write_pal(os.path.join(dd, "palettes", "%02d.pal" % r), sets[key][1][r])
    pt = list(PTILES_NOW)
    for t, px in prim.items():
        pt[t] = px
    os.makedirs(os.path.join(base, "building"), exist_ok=True)
    save_like(os.path.join(GBA, PRI, "tiles.png"), pt, os.path.join(base, "building", "tiles.png"))
    return sets, prim, owner


# ============================================================================================ report
def named_blocks():
    labels = {int(v, 16): k for k, v in re.findall(r"#define (METATILE_GenericBuilding\d_\w+)\s+(0x[0-9A-Fa-f]+)",
                                                   open(os.path.join(GBA, "include/constants/metatile_labels.h")).read())}
    sets_by = {}
    for f in glob.glob(os.path.join(GBA, "data/maps/*/scripts.inc")):
        m = os.path.basename(os.path.dirname(f))
        lid = LAYOUT_OF_MAP.get(m)
        l = next((x for x in LAYOUTS if x["id"] == lid), None)
        if not l or l["secondary_tileset"] not in (GB2.sym, GB1.sym):
            continue
        for b in re.findall(r"setmetatile\s+\d+,\s*\d+,\s*(0x[0-9A-Fa-f]+|\d+)", open(f).read()):
            sets_by.setdefault(int(b, 0), set()).add("set by " + m)
    return labels, sets_by


def report():
    print("T-538 -- the rest of the interiors (census item 6)\n")
    print("  CENSUS: interior secondaries on primary/building still drawing Nintendo's tiles (maps that are placed)")
    print("  %-26s %-5s %5s %7s %-14s %-4s %s" % ("tileset", "batch", "used", "vanilla", "rows", "anim", "maps"))
    tot = 0
    for sym, batch, what in CENSUS_SETS:
        c = census_set(sym)
        tot += c["vanilla"]
        print("  %-26s %-5s %5d %7d %-14s %-4s %d: %s" % (sym[9:], batch, c["used"], c["vanilla"],
                                                         ",".join(map(str, c["rows"])), "yes" if c["anim"] else "-",
                                                         len(c["maps"]), ", ".join(c["maps"][:6]) +
                                                         (" ..." if len(c["maps"]) > 6 else "")))
    print("  (%d vanilla tiles in these sets; the landmarks' sets -- MANSION, DAEMON TOWER, POWER PLANT, LEAGUE, HALL"
          " OF FAME, USER TOWER, TANOBY -- are T-447's, census item 8)\n" % tot)
    for k, s in BATCHES.items():
        print("  %-3s %s" % (k, s))
    print("\n  BATCH 1, OBJECT BY OBJECT")
    owner = {}
    for key, setkey, layout, painter, what in GROUPS:
        for r in layout:
            for s in r:
                if s is not None:
                    t = s if isinstance(s, int) else s[0]
                    owner.setdefault((setkey, t), key)
    print("  %-11s %-4s %5s %6s %4s  %s" % ("group", "set", "tiles", "draws", "maps", "what"))
    for key, setkey, layout, painter, what in GROUPS:
        ts = sorted(t for (sk, t), k in owner.items() if k == key)
        if setkey == "P":
            ts = [t for t in ts if t in PRIMARY_ALL]
            draws = sum(PUSE[t]["draws"] for t in ts if t in PUSE)
            maps = {m for t in ts if t in PUSE for m in PUSE[t]["maps"]}
        else:
            S = SETS[setkey]
            ts = [t for t in ts if t in S.use and t < S.nvan]
            draws = sum(S.use[t]["n"] for t in ts)
            maps = {m for t in ts for m in S.use[t]["maps"]}
        print("  %-11s %-4s %5d %6d %4d  %s" % (key, setkey, len(ts), draws, len(maps), what))
    bad = 0
    for key, S in SETS.items():
        mine = {t for (sk, t) in owner if sk == key}
        used = {t for t in S.use if t < S.nvan and any(S.cur[t])}
        stray = sorted(t for t in used if t not in mine and len(set(S.van[t])) > 1)
        flat = sorted(t for t in used if t not in mine and len(set(S.van[t])) <= 1)
        print("  %s: %d used tiles, %d in a group; flat (recoloured through their row only): %s; in no group: %s"
              % (S.dir.split("/")[-1], len(used), len(used & mine), flat or "none", stray or "none"))
        bad |= bool(stray)
    print("  primary leftovers: %d tiles (%s)" % (len(PRIMARY_ALL), ", ".join("%s %d" % (k, len(v))
                                                                            for k, v in PRIMARY.items())))
    #  coordination with batch D (gbabuilding) and T-537 (gbamachines)
    later = getattr(GB, "LATER_T538", None)
    if later is None:
        print("  !! gbabuilding.LATER_T538 is missing: batch D does not know these tiles are T-538's")
        bad = 1
    elif set(later) != PRIMARY_ALL:
        print("  !! gbabuilding.LATER_T538 and this tool disagree: only here %s, only there %s"
              % (sorted(PRIMARY_ALL - set(later)), sorted(set(later) - PRIMARY_ALL)))
        bad = 1
    else:
        print("  gbabuilding.LATER_T538 names the same %d tiles (batch D skips them)" % len(PRIMARY_ALL))
    t537 = getattr(GB, "LATER_T537", GB.LATER)
    if PRIMARY_ALL & set(t537):
        print("  !! overlap with T-537's tiles (gbamachines): %s" % sorted(PRIMARY_ALL & set(t537)))
        bad = 1
    else:
        print("  disjoint from T-537's %d tiles (gbamachines.py)" % len(t537))
    held = sorted(t for t in PRIMARY_ALL if GB.CUR[t] != GB.VAN[t])
    if held:
        print("  (already redrawn in the engine: %s)" % held)
    labels, sets_by = named_blocks()
    print("\n  BLOCKS THE ENGINE OR A SCRIPT NAMES (ids kept)")
    for b, lab in sorted(labels.items()):
        print("    0x%03X %s (field_specials.c; applied only in the player's house, players_house)" % (b, lab))
    for b, who in sorted(sets_by.items()):
        print("    0x%03X %s (gbaguideshelf.py's appended tiles: never touched)" % (b, "; ".join(sorted(who))))
    print("  no animation in either secondary; no door animation draws from them")
    return bad


def check_engine():
    """T-446's rule: the engine's two secondaries (tiles and own rows) and primary/building's tiles.png against
    `--write --approved --pick X` for the one approved X"""
    pick = next(iter(APPROVED))
    sets, prim, owner = draw(STYLES[pick])
    off = []
    for key, S in SETS.items():
        off += ["%s tile %d" % (key, t) for t in range(len(S.cur)) if sets[key][0][t] != S.cur[t]]
        for r in S.rows:
            now = read_pal(os.path.join(GBA, S.dir, "palettes", "%02d.pal" % r))
            if [tuple(c) for c in now] != [tuple(c) for c in sets[key][1][r]]:
                off.append("%s row %d" % (key, r))
    off += ["primary tile %d" % t for t, px in prim.items() if px != PTILES_NOW[t]]
    if off:
        print("\n  !! the engine differs from `--write --approved --pick %s` in %d place%s (%s) -- find which side is "
              "right" % (pick, len(off), "s" if len(off) > 1 else "", ", ".join(off[:12])))
        return 1
    print("\n  the engine matches `--write --approved --pick %s`: %d tiles, gb2 rows 7/8/9/12 and gb1 row 8 "
          "(the user, 2026-11-10)" % (pick, len(owner)))
    return 0


def main():
    if WRITE:
        if "--approved" not in ARGS or not PICK or PICK not in APPROVED:
            print("  --write refused: T-538 is a draft. APPROVED is %s; the user picks a direction first, it goes into "
                  "APPROVED,\n  then --write --approved --pick X writes generic_building_2's and generic_building_1's "
                  "tiles and own rows,\n  and the primary leftovers into primary/building/tiles.png (never a primary "
                  "palette)." % (sorted(APPROVED) or "empty"))
            return 1
        D = STYLES[PICK]
        sets, prim, owner = draw(D)
        for key, S in SETS.items():
            save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[key][0], os.path.join(GBA, S.dir, "tiles.png"))
            for r in S.rows:
                write_pal(os.path.join(GBA, S.dir, "palettes", "%02d.pal" % r), sets[key][1][r])
        pt = list(PTILES_NOW)
        for t, px in prim.items():
            pt[t] = px
        save_like(os.path.join(GBA, PRI, "tiles.png"), pt, os.path.join(GBA, PRI, "tiles.png"))
        print("  written: direction %s" % PICK)
        return 0
    bad = report()
    if DRAFT is not None:
        os.makedirs(DRAFT, exist_ok=True)
        states = collections.OrderedDict()
        states["NOW"] = None
        summary = {}
        for k, D in STYLES.items():
            sets, prim, owner = write_direction(os.path.join(DRAFT, k), D)
            states[k] = (sets, prim)
            ch = sum(1 for (sk, t) in owner if (sk == "P" and prim[t] != GB.VAN[t]) or
                     (sk != "P" and sets[sk][0][t] != SETS[sk].van[t]))
            summary[k] = dict(title=D["title"], tiles_redrawn=ch, new_tiles=0,
                              rows={"%s %d" % (S.dir.split("/")[-1], r): sets[key][1][r]
                                    for key, S in SETS.items() for r in S.rows})
            print("  %s %-13s %d tiles redrawn, 0 new tiles; rows recoloured: generic_building_2 7/8/9/12, "
                  "generic_building_1 8; primary rows untouched" % (k, D["title"], ch))
        json.dump(dict(ticket="T-538", status="DRAFT -- not in the engine", approved=sorted(APPROVED),
                       directions=summary), open(os.path.join(DRAFT, "directions.json"), "w"), indent=1)
        for p in contact_sheets(DRAFT, states):
            print("  sheet:", p)
    if len(APPROVED) == 1:
        bad |= check_engine()
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""T-569: the islands and the caves -- the Nintendo tiles they still draw (batch 8, the last, of the 2026-11-14 re-census).

    python3 tools/gbaislands.py                       # report: the census per tileset (ours / pret's where a player
                                                      #   can stand / pret's but unplaced or unreachable), what is
                                                      #   excluded and why, what each piece redraws; exits 1 when the
                                                      #   engine differs from an approved pick
    python3 tools/gbaislands.py --draft [DIR]         # the drafts into DIR (gfx/drafts/t569_islands/): per tileset
                                                      #   tiles_A.png / _B / _C, steam frames per option, draft.json
    python3 tools/gbaislands.py --sheets [DIR]        # --draft, and the proof sheets in DIR/sheets: per piece, every
                                                      #   changed tile at 4x (today | A | B | C) and map crops at 2x
                                                      #   (today | A | B | C), rendered from the tiles the ROM is built from
    python3 tools/gbaislands.py --write --approved    # into the engine: the pieces in APPROVED, each with the option the
                                                      #   user picked, drawn from BASE and laid over the engine's own
                                                      #   tiles.png, then T-570's picks over them (below), so the
                                                      #   result is the engine as the user picked it; a second write
                                                      #   is a no-op. The report also checks gbacaves' T569_ISLANDS
                                                      #   (the tiles its write keeps) is exactly these.

    T-570, the last 134 (ladders, holes, slide ice, the rest), drawn by hand as shapes -- its own section and picks:
    python3 tools/gbaislands.py --t570                # report: per kind (ladders / holes and rims / slide ice /
                                                      #   other) each object, what A/B/C draw, what is left and why;
                                                      #   exits 1 when one of the 134 is unaccounted for or the engine
                                                      #   differs from an approved T-570 pick
    python3 tools/gbaislands.py --t570 --draft [DIR]  # the drafts into DIR (gfx/drafts/t570_islands/): per kind and
                                                      #   option a tiles.png per tileset, draft.json
    python3 tools/gbaislands.py --t570 --sheets [DIR] # --draft, and DIR/sheets: every object at 4x (today | A | B
                                                      #   | C) and map crops at 2x (today from reviewsheet.py map)
    python3 tools/gbaislands.py --t570 --write --approved  # APPROVED_570's picks over the engine's own tiles.png.
                                                      #   EMPTY until picked.

THE CENSUS (step 1). For each tileset of the batch: a tile is OURS when its pixels differ from pret's upstream/master;
PRET'S AND REACHABLE when it is pret's, a metatile that draws it is placed on a map (its blockdata, its border, or a
METATILE_ label a script or the C code sets), and that map is reachable; otherwise pret's but UNUSED (no placed metatile
draws it) or UNREACHABLE (only maps nothing reaches draw it). Reachable is a map graph from PALLET TOWN: map.json warps
and connections, every warp a map's own scripts make, and the SEAGALLOP's eleven ports for any map that calls the
ferry. It ignores flags on purpose (a floor, like check_reach's): NAVEL ROCK's ferry opens with the GLOBAL INDEX
(VermilionCity_EventScript_NavelRockIsOpen) and THE ANNEX's once CRYSTAL has read the payload, so all 26 maps on
navel_rock's set (NAVEL ROCK's 20 and THE DOTS' 6) are reachable here, unlike vanilla.

THE RULES (gbatownslast's, kept): pixels only -- no block, layer, flip, palette row, behaviour, collision, map or
animation frame count moves; index 0 stays 0 and a drawn pixel stays drawn; each row's darkest index (the outline),
its whites and general's reserved indices keep pret's pixel; a pixel touching transparency or another family keeps
pret's pixel, so every join and every seam is where it was. EXCLUDED, and named: door tiles (gbadoors.py), gbatowns'
KEEP_TILES (the canopy hollows), grove tells (gbagrove.py), LANDMARK boxes (USER TOWER and THE ANNEX's triangle are
T-447's), tiles an animation overwrites (MT. SMOULDER's steam, drawn here as its own frames), and a copy of a general
tile T-542 left as pret's. The palette splits (THE SAME BUSH over DENSE WOOD's neighbour, UMBRAL ASCENT over the
stack, STILLFALL over GLAUCOUS ISLES, OTHER CAVE over THE BLACKOUT) hold because no row is touched: a split shares
its base's tiles, so one drawing reads in both lights (the sheets show both).

THE PIECES, the most-seen first: the islands' three outdoor sets, the harbours and DENSE WOOD (drawn by hue family in
the island kit's own T-438 motifs, gbatowns _ISLE_STYLE); then the caves' leftovers, which are almost all the things
gbacaves kept on purpose (OBJECTS: the rock clusters, rubble and pebbles, and the ladders and hole rims), drawn in
each cave's own grain (gbacaves' motifs) so the STACK's stones are slabs and THE BLACKOUT's are basalt.
"""
import collections, io, json, os, re, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv = sys.argv
sys.argv = [sys.argv[0]]
import gbatownslast as L                  # noqa: E402  (imports gbatowns, which reads its flags at import)
import gbacaves as C                      # noqa: E402
sys.argv = _argv
from PIL import Image, ImageDraw          # noqa: E402

T = L.T
ROOT = T.ROOT
GBA = T.GBA
ARGS = sys.argv[1:]
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t569_islands")

#  THE ENGINE AS T-569 FOUND IT (origin/context-content, 2026-11-15): every draft starts from these tiles, so a write is
#  the same pixels every time and no tile another tool draws later is read as a leftover.
BASE = "79922dc95"

#  the user's picks, {piece: option}, 2026-11-15 by multiple choice: A for the islands, the caves and the steam, with
#  one exception -- THE BLACKOUT (rock_tunnel) is left as T-546 drew it: "the blackout's purple with glowing green needs
#  to stay as it links to the story" (the user). TANOBY's chamber fronts stay the landmark's (T-447). DRAFT.
APPROVED = {}   # filled below, once SETS is defined

#  the batch's tilesets: (tileset, its DAEMONS name)
ISLES = [("sevii_islands_67", "SIX and SEVEN ISLAND"), ("sevii_islands_123", "ONE, TWO and THREE ISLAND, MT. SMOULDER's "
                                                                              "outside"),
         ("sevii_islands_45", "FOUR and FIVE ISLAND"), ("island_harbor", "the harbours"), ("berry_forest", "DENSE WOOD")]
CAVES = [("seafoam_islands", "GLAUCOUS ISLES and STILLFALL"), ("cave", "DEADSTACK, UMBRAL ASCENT, THE WRONG WAY"),
         ("mt_ember", "MT. SMOULDER"), ("navel_rock", "NAVEL ROCK and THE DOTS"),
         ("rock_tunnel", "THE BLACKOUT and OTHER CAVE"), ("digletts_cave", "TAPPOINT'S CAVE"),
         ("underground_path", "THE TUNNEL")]
SETS = ISLES + CAVES
NAME = dict(SETS)
#  THE TUNNEL (underground_path) is out too: gbadwellings already redrew its "pret" tiles in THE TUNNEL's colours
#  (vanilla shapes kept on purpose, vision 3.2), so they only looked like leftovers here (found by check_generators).
APPROVED = {ts: "A" for ts, _ in SETS if ts not in ("rock_tunnel", "underground_path")}
APPROVED["steam"] = "A"
#  tiles an animation overwrites (trap 39): MT. SMOULDER's steam, 896..903 -> secondary 256..263, 4 frames
ANIM = {"mt_ember": set(range(256, 264))}
STEAM = "data/tilesets/secondary/mt_ember/anim/steam/%d.png"
#  a map whose own tiles are a landmark's: the seven TANOBY chamber fronts are the outside of T-447 pair 5's chambers
#  (the user's "key buildings get their own art"), so a tile drawn ONLY there is the landmark's, not this batch's
ONLY_LANDMARK_MAPS = {"sevii_islands_67": {"SevenIsland_TanobyRuins"}}
#  the splits that share a base's tiles (their own rows only): the sheets show the draft in both lights
SPLITS = {"cave": ("UMBRAL ASCENT", "palettes_umbral", "VictoryRoad_2F"),
          "seafoam_islands": ("STILLFALL", "palettes_stillfall", "FourIsland_IcefallCave_1F"),
          "rock_tunnel": ("OTHER CAVE", "palettes_other", "SixIsland_AlteringCave")}


# ================================================================== where a player can be
_REACH = None


def reachable():
    """every map directory a player can reach from PALLET TOWN (see the docstring: flags ignored, a floor)"""
    global _REACH
    if _REACH is not None:
        return _REACH
    maps, dirs = {}, {}
    for d in os.listdir(os.path.join(GBA, "data/maps")):
        p = os.path.join(GBA, "data/maps", d, "map.json")
        if os.path.exists(p):
            j = json.load(open(p))
            maps[j["id"]], dirs[j["id"]] = j, d
    ferry = set(re.findall(r"MAP\((MAP_\w+)\)", open(os.path.join(GBA, "src/seagallop.c")).read()))
    edges = collections.defaultdict(set)
    for mid, j in maps.items():
        edges[mid] |= {w["dest_map"] for w in j.get("warp_events") or []}
        edges[mid] |= {c["map"] for c in j.get("connections") or []}
        s = os.path.join(GBA, "data/maps", dirs[mid], "scripts.inc")
        if os.path.exists(s):
            text = open(s).read()
            edges[mid] |= set(re.findall(r"^\s*warp\w*\s+(MAP_\w+)", text, re.M))
            if "SEAGALLOP" in text:
                edges[mid] |= ferry
    seen, q = {"MAP_PALLET_TOWN"}, ["MAP_PALLET_TOWN"]
    while q:
        for n in edges[q.pop()]:
            if n in maps and n not in seen:
                seen.add(n)
                q.append(n)
    _REACH = {dirs[m] for m in seen}
    return _REACH


_LABELS = None


def script_metatiles(ts):
    """the secondary blocks of TS that a script or the C code sets by name (METATILE_<Tileset>_*), the debug menu's aside"""
    global _LABELS
    if _LABELS is None:
        defs = dict(re.findall(r"#define (METATILE_\w+)\s+(0x[0-9A-Fa-f]+)",
                               open(os.path.join(GBA, "include/constants/metatile_labels.h")).read()))
        used = set()
        for sub in ("src", "data/maps", "data/scripts"):
            for dp, _, fs in os.walk(os.path.join(GBA, sub)):
                for f in fs:
                    if f.endswith((".c", ".inc", ".h")) and "daemons_debug" not in f:
                        used |= set(re.findall(r"METATILE_\w+", open(os.path.join(dp, f), errors="ignore").read()))
        _LABELS = {k: int(v, 16) for k, v in defs.items() if k in used}
    pre = "METATILE_" + T.camel(ts) + "_"
    return {v for k, v in _LABELS.items() if k.startswith(pre) and v >= 640}


# ================================================================== the census
_BASE_TILES = {}


def base_town(ts):
    """gbatowns' Town for TS, its tiles read from BASE"""
    town = T.Town(ts)
    if ts not in _BASE_TILES:
        _BASE_TILES[ts] = T.tiles_of(Image.open(io.BytesIO(T.daemonslib.upstream(
            GBA, T.SEC + ts + "/tiles.png", binary=True, ref=BASE))))
    town.now = [list(t) for t in _BASE_TILES[ts]]
    town._leftovers()
    return town


def placement(town):
    """{tile: maps} -- every map whose blockdata, border or scripts place a block drawing the tile"""
    blocks = collections.defaultdict(set)
    lay = T.layouts()
    for m in town.maps:
        l = lay[m]
        users = T.used_layouts()[m]
        for f in ("blockdata_filepath", "border_filepath"):
            d = open(os.path.join(GBA, l[f]), "rb").read()
            for k in range(len(d) // 2):
                blocks[struct.unpack_from("<H", d, k * 2)[0] & 0x3FF] |= set(users)
    every = {u for m in town.maps for u in T.used_layouts()[m]}
    for b in script_metatiles(town.ts):
        blocks[b] |= every
    out = collections.defaultdict(set)
    for b, ms in blocks.items():
        if 640 <= b < 640 + town.nblocks:
            for v in T.entries(town.mt, b - 640):
                if v & 0x3FF >= 640:
                    out[(v & 0x3FF) - 640] |= ms
    return out


def census(ts):
    """(town, {tile: class}, {tile: why excluded}, {map: pret's tiles it draws}); town.targets is what may be drawn"""
    town = base_town(ts)
    where = placement(town)
    reach = reachable()
    cls = {}
    for t in range(len(town.now)):
        if not any(town.now[t]):
            continue
        if t >= len(town.van) or town.now[t] != town.van[t]:
            cls[t] = "ours"
        elif t in ANIM.get(ts, ()):
            cls[t] = "anim"
        elif not where.get(t):
            cls[t] = "unused"
        elif not (where[t] & reach):
            cls[t] = "unreachable"
        else:
            cls[t] = "reach"
    lm = town.kept_by_map()
    gk = L.gen_kept_copies(town)
    why = collections.OrderedDict()
    for t in sorted(t for t, c in cls.items() if c == "reach"):
        if t in town.door_tiles:
            why[t] = "door (gbadoors.py)"
        elif t + 640 in T.KEEP_TILES.get(ts, ()):
            why[t] = "kept (gbatowns KEEP_TILES: the canopy hollows)"
        elif t in T.grove_tell(ts):
            why[t] = "grove tell (gbagrove.py)"
        elif t in lm:
            why[t] = "landmark (T-447)"
        elif where[t] & reach <= ONLY_LANDMARK_MAPS.get(ts, set()):
            why[t] = "TANOBY's chamber fronts (T-447 pair 5: drawn only on SevenIsland_TanobyRuins)"
        elif t in gk and gk[t] in L.T542_KEPT:
            why[t] = "general %d, left pret's by T-542" % gk[t]
    per = collections.Counter()
    for t, c in cls.items():
        if c == "reach":
            for m in where[t] & reach:
                per[m] += 1
    town.targets = {t for t, c in cls.items() if c == "reach"} - set(why)
    town.where = where
    return town, cls, why, per


# ================================================================== the islands: hue families in the island kit
def m_limewash(x, y, w, h, X, Y, b):
    """B, LIMEWASH: a wall as lime render on rubble -- a bleached band under the eave, the body flat, the render worn
    through to a darker course along the foot; a roof keeps its own light, and a window slot or a sill (the family's
    darkest, pret's) is kept, so the hall keeps its windows"""
    if b >= 0.8:
        return b
    if y < 2:
        return 0.0
    if y >= h - 2:
        return 0.85
    return 0.3


def m_shiplap(x, y, w, h, X, Y, b):
    """C, SHIPLAP AND TAR: boards a full eight high, a tarred dark seam under each, butt joints staggered course to
    course -- the harbour kit's boarding carried up the island houses"""
    yy, course = Y % 8, Y // 8
    if yy == 7:
        return 1.0
    if (X + 12 * (course % 2)) % 24 == 0:
        return 1.0
    return 0.0 if yy == 0 else 0.45


def m_dune(x, y, w, h, X, Y, b):
    """sand and grass laid by the wind: long low ridges, lit on the windward side, a step darker in the lee"""
    k = (Y * 3 + (X // 6)) % 9
    return 0.0 if k < 2 else (0.85 if k > 6 else 0.45)


def walls_only(f):
    """B and C are about WALLS: a region narrower than three and a half blocks (a flight of steps, a post, a sill)
    keeps A's drawing, so the steps still read as steps (and a thin cap, the harbour hall's white top, stays white)"""
    def g(x, y, w, h, X, Y, b):
        return f(x, y, w, h, X, Y, b) if w >= 56 and h >= 24 else T.m_clapboard(x, y, w, h, X, Y, b)
    g.__name__ = f.__name__ + "_walls"
    L.KEEP_LIGHT[g] = 0.0
    return g


_family = L.family


def isle_family(c):
    """gbatownslast's hue families, with one change for the islands: a pale, greyed blue (the harbour halls' and the
    NET centre's painted walls) is a wall, not glass -- read as glass it took diagonal glints (draft 1, 2026-11-15)"""
    import colorsys
    f = _family(c)
    s = colorsys.rgb_to_hsv(*(v / 255.0 for v in c))[1]
    return "grey" if f in ("blue", "teal") and s < 0.32 else f


ISLE_A = {"red": T.m_weatherboard, "purple": T.m_weatherboard, "pink": T.m_weatherboard, "blue": T.m_glass,
          "teal": T.m_glass, "yellow": T.m_awning, "orange": T.m_boards, "green": T.m_leaf, "grey": T.m_clapboard,
          "*": T.m_clapboard}
ISLE_OPTIONS = [
    ("A", "THE ISLAND KIT (DRAFT)", "the islands' own T-438 look carried on: walls in clapboard, roofs in sea-weathered "
                                    "board, glass level, awnings striped", {}),
    ("B", "LIMEWASH (DRAFT)", "walls as lime render -- a bleached band under every eave, worn to a darker foot; roofs "
                              "and glass as A", {"grey": walls_only(m_limewash), "*": walls_only(m_limewash),
                               "orange": walls_only(m_limewash)}),
    ("C", "SHIPLAP AND TAR (DRAFT)", "the harbours' boarding carried up the houses: eight-high boards, a tarred seam "
                                     "under each, joints staggered; roofs and glass as A",
     {"grey": walls_only(m_shiplap), "*": walls_only(m_shiplap), "orange": walls_only(m_shiplap)}),
]
HARBOUR_OPTIONS = [
    ("A", "NETS AND BOARDS (DRAFT)", "the harbour hall's walls and quay in the island kit's clapboard, its windows level "
                                     "glass, its red as nets drying", {"red": T.m_net}),
    ("B", "LIMEWASH (DRAFT)", "the hall limewashed as the islands' B, its red as A", {"red": T.m_net, "*": walls_only(m_limewash),
                                                                                      "grey": walls_only(m_limewash)}),
    ("C", "SHIPLAP AND TAR (DRAFT)", "the hall in tarred shiplap as the islands' C", {"red": T.m_net, "*": walls_only(m_shiplap),
                                                                                     "grey": walls_only(m_shiplap)}),
]
WOOD_OPTIONS = [
    ("A", "DENSE CANOPY (DRAFT)", "the wood's last pieces -- the grass edge and the berry patches -- in DENSE WOOD's "
                                  "own packed lobes (gbatowns m_dense)", {"*": T.m_dense, "green": T.m_dense}),
    ("B", "WIND-LAID (DRAFT)", "the same pieces as long wind-laid ridges, lit to windward", {"*": m_dune,
                                                                                            "green": m_dune}),
]


# ================================================================== the caves: each cave's own grain on what it kept
ROLE = {"hi": -0.3, "body": 0.0, "lo": 0.3, "crack": 1.0, "accent0": 0.0, "accent1": 0.0, None: 0.0}
GRAIN = {"cave": C.m_stack, "rock_tunnel": C.m_outage, "digletts_cave": C.m_line, "seafoam_islands": C.m_bloom,
         "mt_ember": C.m_ember, "navel_rock": C.m_dots, "underground_path": C.m_stack}


def grain(ts):
    f = GRAIN[ts]

    def m_grain(x, y, w, h, X, Y, b):
        """A, THE CAVE'S OWN GRAIN: the stone cut in its cave's wall motif (gbacaves), pret's light kept under it --
        the lit top of a stone reads the motif's top, its shaded body the face"""
        r = f(X % 16, Y % 16, "top" if b < 0.35 else "face")
        role, shift = (r if isinstance(r, tuple) else (r, 0))
        if role == "crack":
            return 1.0
        return max(0.0, min(1.0, b + ROLE.get(role, 0.0) + 0.12 * shift))
    m_grain.__name__ = "m_grain_" + ts
    return m_grain


def m_knapped(x, y, w, h, X, Y, b):
    """B, KNAPPED: every stone struck flat -- pret's light on it cut to three planes (lit, body, shade), and a struck
    edge one step darker along the diagonal every eight pixels; no texture at all"""
    lv = 0.0 if b < 0.34 else (0.5 if b < 0.67 else 1.0)
    if (X - Y) % 8 == 0 and lv < 1.0:
        lv += 0.5
    return lv


def m_worn(x, y, w, h, X, Y, b):
    """C, WATER-WORN: every stone rounded smooth -- lit from its upper left across its block, half pret's light and
    half the round, so it keeps its place and loses its chisel marks (an eight-pixel round drew a cross on every
    sixteen-pixel stone, draft 3)"""
    t = ((X % 16) + (Y % 16)) / 30.0
    return 0.5 * b + 0.5 * (0.0 if t < 0.3 else (0.5 if t < 0.7 else 1.0))


def cave_materials(town):
    """{(row, idx): material} for a cave: gbacaves' own index plan (MATERIALS, by role -- rock, floor, wood, rung,
    water, patch, glint...), not hue: a cave's rows are one hue, so hue split its rock into slivers and drew almost
    nothing (draft 1). The hole's black, the dark and the cast shade are single and stay pret's"""
    plan = C.MATERIALS[town.ts]
    rows = collections.defaultdict(set)
    for b in range(town.nblocks):
        for v in T.entries(town.mt, b):
            t = (v & 0x3FF) - 640
            if 0 <= t < len(town.now) and t in town.targets:
                rows[v >> 12] |= set(town.van[t]) - {0}
    out = {}
    for row, idxs in rows.items():
        fam = collections.defaultdict(list)
        for i in idxs:
            m = plan.get(row, {}).get(i)
            if m and m[0] not in ("hole", "dark", "shade"):
                fam[m[0]].append(i)
        for f, ii in fam.items():
            if len(ii) >= 2:
                for i in ii:
                    out[(row, i)] = f
    return out


def cave_ladder(town, row, mat, M):
    plan = C.MATERIALS[town.ts][row]
    return sorted((i for (r, i), f in M.items() if r == row and f == mat), key=lambda i: (plan[i][1], i))


def redraw(town, style):
    """gbatownslast's redraw, reading a cave's materials by role and an island's by isle_family"""
    saved = L.materials, L.ladder, L.family
    try:
        if town.ts in C.MATERIALS:
            L.materials, L.ladder = cave_materials, cave_ladder
        else:
            L.family = isle_family
        return L.redraw(town, style)
    finally:
        L.materials, L.ladder, L.family = saved


def cave_options(ts):
    g = grain(ts)
    opts = [("A", "THE CAVE'S OWN GRAIN (DRAFT)", "the stones, rubble, ladders and rims %s kept cut in its own wall "
                                                  "motif, so its rocks are made of what its walls are" % NAME[ts],
             {"*": g}),
            ("B", "KNAPPED (DRAFT)", "every stone struck flat: its light cut to three planes with a struck edge on "
                                     "the diagonal -- the shape kept, no texture; the ladders, slides and floors as A",
             {"*": g, "rock": m_knapped}),
            ("C", "WATER-WORN (DRAFT)", "every stone rounded smooth, lit from its upper left lump by lump, its chisel "
                                        "marks gone; the ladders, slides and floors as A", {"*": g, "rock": m_worn})]
    #  a built room (THE TUNNEL) has no rock, so B and C would only repeat A: one option, no false choice
    if not any(m[0] == "rock" for plan in C.MATERIALS[ts].values() for m in plan.values()):
        return opts[:1]
    return opts


for _f in (m_limewash, m_shiplap, m_dune, m_knapped, m_worn):
    L.KEEP_LIGHT[_f] = 0.0
L.KEEP_LIGHT.update({T.m_weatherboard: 0.0, T.m_net: 0.0, T.m_dense: 0.0})


# ================================================================== the steam (4 frames of 8 tiles, 16x32)
STEAM_OPTIONS = [
    ("A", "BANKED HEAT (DRAFT)", "the spa's steam as two soft solid wisps, lit on top and shaded under, that rise eight "
                                 "pixels a frame and thin as they go -- no dither"),
    ("B", "THREADS (DRAFT)", "two thin threads of vapour that waver up the column, a quarter wave a frame, thinning "
                             "toward the top"),
    ("C", "THE DITHER RELIT (DRAFT)", "pret's dithered puffs where they were, each re-shaded as one lump lit from "
                                      "above -- the smallest change"),
]


def steam(option, k):
    """(image, pret's indices, the drafted indices) of frame K. The steam floats over the spring (layer 1, open round
    it), so A and B draw new shapes -- no seam can move -- in pret's own colours; the four frames loop as pret's do"""
    import math
    im = Image.open(io.BytesIO(T.daemonslib.upstream(GBA, STEAM % k, binary=True))).convert("P")
    w, h = im.size
    px = im.load()
    src = [[px[x, y] & 15 for x in range(w)] for y in range(h)]
    used = sorted({c for kk in range(4) for c in Image.open(io.BytesIO(T.daemonslib.upstream(
        GBA, STEAM % kk, binary=True))).convert("P").getdata() if c & 15} | {0}) [1:]
    pal = im.getpalette()
    lumc = lambda c: 0.30 * pal[3 * c] + 0.59 * pal[3 * c + 1] + 0.11 * pal[3 * c + 2]
    lad = sorted({c & 15 for c in used}, key=lambda c: -lumc(c))           # light .. dark
    pick = lambda v: lad[max(0, min(len(lad) - 1, int(round(v * (len(lad) - 1)))))]
    out = [[0] * w for _ in range(h)]
    if option == "A":
        for i in range(2):
            cy = (h - 4) - ((k * 8 + i * 16) % h)              # rises 8 px a frame, two wisps half a loop apart
            cx = 6.5 if i == 0 else 9.0
            life = (h - cy) / float(h)                          # 0 at the spring .. 1 at the top
            rx, ry = 5.0 - 2.0 * life, 3.6 - 1.2 * life
            for y in range(h):
                for x in range(w):
                    dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                    if dx * dx + dy * dy < 1.0:
                        out[y][x] = pick(0.0 if dy < -0.25 else (0.4 if dy < 0.45 else 0.8))
    elif option == "B":
        for i, (cx, ph) in enumerate(((4.0, 0.0), (11.5, math.pi / 2))):
            for y in range(h):
                life = (h - 1 - y) / float(h - 1)
                x0 = cx + 1.4 * math.sin(2 * math.pi * (y / 16.0 - k / 4.0) + ph)
                half = 1.3 - 0.7 * life
                for x in range(w):
                    d = abs(x + 0.5 - x0)
                    if d < half:
                        out[y][x] = pick(0.0 if d < half * 0.45 else 0.55)
    else:
        for y in range(h):
            for x in range(w):
                c = src[y][x]
                if not c:
                    continue
                b = lad.index(c) / max(1, len(lad) - 1)
                up = y > 1 and src[y - 1][x] == 0 and src[y - 2][x] != 0
                out[y][x] = pick(max(0.0, b - 0.35) if y % 8 < 4 else min(1.0, b + 0.25)) if not up else pick(0.0)
    o = Image.new("P", (w, h))
    o.putpalette(pal[:48])
    o.putdata([v for r in out for v in r])
    return o, src, out


# ================================================================== the pieces
def options(ts):
    if ts in ("sevii_islands_67", "sevii_islands_123", "sevii_islands_45"):
        return [(o, t, l, dict(ISLE_A, **ov)) for o, t, l, ov in ISLE_OPTIONS]
    if ts == "island_harbor":
        return [(o, t, l, dict(ISLE_A, **ov)) for o, t, l, ov in HARBOUR_OPTIONS]
    if ts == "berry_forest":
        return WOOD_OPTIONS
    return cave_options(ts)


#  the follow-up: what this pass does not draw, and why (filled by run())
LATER = collections.OrderedDict()


def draw_set(ts):
    town, cls, why, per = census(ts)
    news = []
    for o, title, line, st in options(ts):
        new, what = redraw(town, st)
        news.append((o, title, line, new))
    return town, cls, why, per, news


# ================================================================== pictures
def rows_of(town):
    rows = collections.Counter()
    for b in range(town.nblocks):
        for v in T.entries(town.mt, b):
            if v & 0x3FF >= 640:
                rows[((v & 0x3FF) - 640, v >> 12)] += 1 + town.placed.get(640 + b, 0)
    return rows


def tile_sheet(town, news, path, title):
    rows = rows_of(town)
    changed = sorted({t for *_, new in news for t in range(len(new)) if new[t] != town.now[t]})
    f = T.font(11)
    cols = 6
    cell_w = 34 * (1 + len(news)) + 14
    W = cols * cell_w + 16
    H = 46 + ((len(changed) + cols - 1) // cols) * 58
    out = Image.new("RGB", (W, max(H, 80)), T.BG)
    d = ImageDraw.Draw(out)
    d.text((8, 6), title, font=T.font(13), fill=(20, 20, 20))
    d.text((8, 24), "each cell: today | " + " | ".join(n[0] for n in news) + "   (4x, the tile's commonest row)",
           font=f, fill=(60, 60, 60))
    for n, t in enumerate(changed):
        row = max((r for (tt, r) in rows if tt == t), key=lambda r: rows[(t, r)], default=8)
        pal = town.palette(row)
        x, y = 8 + (n % cols) * cell_w, 46 + (n // cols) * 58
        d.text((x, y), "%d r%d" % (t, row), font=f, fill=(30, 30, 30))
        out.paste(L.tile_img(town.now[t], pal), (x, y + 14))
        for j, nw in enumerate(news):
            out.paste(L.tile_img(nw[-1][t], pal), (x + 34 * (j + 1), y + 14))
    out.save(path)
    return path


def crop_for(town, mapname, shown, W=15, H=10):
    """the 15x10 window (a GBA screen) over the most-drawn target object on MAPNAME that shows tiles no crop before it
    showed (every island has the same harbour hall: shown once, not three times)"""
    objs = [o for o in town.objects(town.targets) if o["map"] == mapname]
    l = T.layouts()[mapname]
    if not objs:
        return (0, 0, min(W, l["width"]), min(H, l["height"])), set()

    def tiles_of(o):
        out = set()
        for (x, y) in o["cells"]:
            b = town.grid[mapname][y * l["width"] + x]
            if 640 <= b < 640 + town.nblocks:
                out |= {(v & 0x3FF) - 640 for v in T.entries(town.mt, b - 640)} & town.targets
        return out
    best = max(objs[:40], key=lambda o: (len(tiles_of(o) - shown), o["draws"]))
    x0, y0, w, h = best["box"]
    cx, cy = x0 + w // 2, y0 + h // 2
    box = (max(0, min(l["width"] - W, cx - W // 2)), max(0, min(l["height"] - H, cy - H // 2)), W, H)
    seen = set()
    for o in objs:
        bx, by, bw, bh = o["box"]
        if box[0] <= bx and bx + bw <= box[0] + W and box[1] <= by and by + bh <= box[1] + H:
            seen |= tiles_of(o)
    return box, seen | tiles_of(best)


def crop_maps(town, n=3):
    """the layouts that draw the most of the targets, most first"""
    score = {}
    for m in town.maps:
        g = town.grid[m]
        drawn = set()
        for b in set(g):
            if 640 <= b < 640 + town.nblocks:
                drawn |= {(v & 0x3FF) - 640 for v in T.entries(town.mt, b - 640)}
        score[m] = len(drawn & town.targets)
    return [m for m in sorted(score, key=lambda m: -score[m]) if score[m]][:n]


def with_pals(town, folder):
    """a copy of TOWN reading its rows 7..15 from FOLDER (a split's own palettes)"""
    import copy
    tw = copy.copy(town)
    tw.pals = [C.read_pal(os.path.join(town.dir, folder, "%02d.pal" % r)) if os.path.exists(
        os.path.join(town.dir, folder, "%02d.pal" % r)) else town.pals[r] for r in range(16)]
    return tw


def map_sheet(town, news, maps, path, title):
    """today | A | B | C at 2x, one row per map (the most-seen maps this set's leftovers are drawn on); a split's own
    light gets a row of its own"""
    f = T.font(12)
    rows = []
    shown = set()
    for m, tw, label in maps:
        box, seen = crop_for(town, m, shown if tw is town else set())
        shown |= seen
        ims = [tw_render(tw, m, None, box)] + [tw_render(tw, m, nw[-1], box) for nw in news]
        rows.append(("%s  %s  cells %d,%d %dx%d" % (label, m, *box), ims))
    Z = 2
    cw = 15 * 16 * Z
    W = 16 + (1 + len(news)) * (cw + 10)
    H = 40 + max(1, len(rows)) * (10 * 16 * Z + 40)
    out = Image.new("RGB", (W, H), T.BG)
    d = ImageDraw.Draw(out)
    d.text((8, 6), title, font=T.font(13), fill=(20, 20, 20))
    d.text((8, 22), "today | " + " | ".join("%s %s" % (n[0], n[1]) for n in news) + "   (2x)", font=T.font(11),
           fill=(60, 60, 60))
    y = 40
    for label, ims in rows:
        d.text((8, y), label, font=f, fill=(30, 30, 30))
        for j, im in enumerate(ims):
            out.paste(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (8 + j * (cw + 10), y + 16))
        y += 10 * 16 * Z + 40
    out.save(path)
    return path


def tw_render(tw, m, tiles, box):
    return T.render(tw, m, tiles=tiles, box=box)


def steam_sheet(path):
    town = T.Town("mt_ember")
    rows = rows_of(town)
    row = max((r for (t, r) in rows if t in ANIM["mt_ember"]), key=lambda r: rows.get((256, r), 0), default=8)
    pal = town.palette(row)
    Z = 6
    lines = [("today (pret's)", [steam("A", k)[1] for k in range(4)])]
    for o, title, line in STEAM_OPTIONS:
        lines.append(("%s  %s -- %s" % (o, title, line), [steam(o, k)[2] for k in range(4)]))
    W, H = max(4 * (16 * Z + 12) + 24, 900), len(lines) * (32 * Z + 34) + 30
    out = Image.new("RGB", (W, H), T.BG)
    d = ImageDraw.Draw(out)
    d.text((8, 6), "T-569 MT. SMOULDER's steam (the spa), 4 frames at %dx (row %d; tiles 896-903 by the animation) "
                   "-- DRAFT" % (Z, row), font=T.font(12), fill=(20, 20, 20))
    y = 28
    for name, frames in lines:
        d.text((8, y), name[:150], font=T.font(11), fill=(30, 30, 30))
        for k, fr in enumerate(frames):
            im = Image.new("RGB", (16, 32), (60, 52, 50))
            for yy in range(32):
                for xx in range(16):
                    if fr[yy][xx]:
                        im.putpixel((xx, yy), pal[fr[yy][xx]])
            out.paste(im.resize((16 * Z, 32 * Z), Image.NEAREST), (12 + k * (16 * Z + 12), y + 16))
        y += 32 * Z + 34
    out.save(path)
    return path


# ================================================================== T-570: the last tiles, drawn by hand
#  T-569 drew by re-cutting a tile's colour families, so a tile of one index (a flat red wall, the spa's water), or one
#  whose shape IS the thing (a ladder, a hole, the slide ice), came through as pret's: 134 of them ("later" in
#  t569_islands/draft.json). These are drawn as SHAPES, one object at a time -- the whole ladder, the whole hole, the
#  whole ice block -- on a canvas cut from the blocks that show it, then cut back into its tiles. The rules: no block,
#  layer, flip, palette row, behaviour, collision or animation frame moves; only indices the object already uses are
#  drawn (the ladders keep their gold, gbacaves: "a ladder is a thing the player looks for"); a block's outer edge
#  keeps its seam where a neighbour meets it. A tile in an object is written only when it is one of the 134 or one
#  this tool's T-569 pick drew (an object is redrawn whole, so a ladder is one drawing, not pret's rails under T-569's
#  rungs); anything another tool owns is left and named (LEFT_570). DRAFT until picked: APPROVED_570 is empty.
BASE_570 = "31adf3c19"      # the engine as T-570 found it (origin/context-content, 2026-11-16; T-569's A built)
DRAFT_570 = os.path.join(ROOT, "gfx", "drafts", "t570_islands")
APPROVED_570 = {"ladders": "A", "holes": "A", "ice": "A", "other": "A"}   # the user, 2026-11-16, by multiple choice: A for every kind (DRAFT)

KINDS_570 = collections.OrderedDict([
    ("ladders", dict(name="LADDERS", rec="A", options=[
        ("A", "RUNGS AND RAILS (DRAFT)", "two straight rails and a flat rung every five pixels, outlined, lit rail "
                                         "left, its foot on its own shadow -- reads as a ladder at a glance"),
        ("B", "ROPE AND SLATS (DRAFT)", "a rope ladder: two twisted ropes and wide slats lashed across them, lit on "
                                        "top, shaded under"),
        ("C", "PEG POLE (DRAFT)", "one stout pole with pegs driven in left and right, turn about -- a climber's "
                                  "pole, the same gold")])),
    ("holes", dict(name="HOLES AND RIMS", rec="A", options=[
        ("A", "BROKEN LIP (DRAFT)", "an uneven lip in the place's own rim colour, the far wall seen falling away "
                                    "inside, the near edge lit -- a drop, not a black disc"),
        ("B", "STEPPED SHAFT (DRAFT)", "a round shaft that steps down in rings -- rim, wall, a ledge, wall -- to a "
                                       "smaller black: deep"),
        ("C", "SPLINTERED (DRAFT)", "a jagged break with cracks running out into the floor, as if it gave way "
                                    "under someone")])),
    ("ice", dict(name="SLIDE ICE", rec="A", options=[
        ("A", "GLARE AND GLINT (DRAFT)", "polished ice: deeper cyan, a soft-edged white glare and a thin one across "
                                         "every block, and a four-point glint -- slippery at a glance"),
        ("B", "SKATE-SCORED (DRAFT)", "pale ice scored with long curved blade marks, a rink someone has already "
                                      "slid across"),
        ("C", "FACETS (DRAFT)", "the ice cut into flat facets, each lit its own way with a fine seam between -- "
                                "glassy, less slippery")])),
    ("other", dict(name="OTHER PIECES", rec="A", options=[
        ("A", "IN KEEPING (DRAFT)", "each last piece drawn in its place's approved look: boards on the harbour's "
                                    "red, the spa's ripples, embers in the steps, berries in clusters, a press "
                                    "plate, lit pebbles"),
        ("B", "QUIET (DRAFT)", "the same pieces with one mark each instead of several -- the least drawing that is "
                               "no longer pret's")])),
])

#  every object: (kind, tileset, what it is, the blocks that show it (rows of block ids), the layer, the drawing)
#  -- filled below the drawings


# ---------------------------------------------------------------- the canvas
_B570, _T570 = {}, {}


def base570(ts):
    """TS's tiles as BASE_570 has them"""
    if ts not in _B570:
        _B570[ts] = T.tiles_of(Image.open(io.BytesIO(T.daemonslib.upstream(
            GBA, T.SEC + ts + "/tiles.png", binary=True, ref=BASE_570))))
    return _B570[ts]


def town570(ts):
    if ts not in _T570:
        _T570[ts] = T.Town(ts)
    return _T570[ts]


def canvas(ts, grid, layer):
    """(pixels, owners, rows): the layer of the blocks in GRID as one index picture; owners maps a pixel to the
    (tile, index) a write goes back to, for a secondary tile (a general tile under it is never written)"""
    town, tiles = town570(ts), base570(ts)
    H, W = 16 * len(grid), 16 * len(grid[0])
    pix = [[0] * W for _ in range(H)]
    own, rows = {}, set()
    for by, line in enumerate(grid):
        for bx, b in enumerate(line):
            e = T.entries(town.mt, b - 640)
            for q in range(4):
                v = e[layer * 4 + q]
                t = v & 0x3FF
                src = town.G["tiles"][t] if t < 640 else (tiles[t - 640] if t - 640 < len(tiles) else [0] * 64)
                if t >= 640:
                    rows.add(v >> 12)
                for ty in range(8):
                    for tx in range(8):
                        sx = 7 - tx if v & 0x400 else tx
                        sy = 7 - ty if v & 0x800 else ty
                        Y, X = by * 16 + (q // 2) * 8 + ty, bx * 16 + (q % 2) * 8 + tx
                        pix[Y][X] = src[sy * 8 + sx]
                        if t >= 640:
                            own[(Y, X)] = (t - 640, sy * 8 + sx)
    return pix, own, rows


def blank(h, w):
    return [[0] * w for _ in range(h)]


def put(P, x, y, c):
    if 0 <= y < len(P) and 0 <= x < len(P[0]):
        P[y][x] = c


class R:
    """an object's roles: names for the palette indices it already uses"""
    def __init__(self, **kw):
        self.__dict__.update(kw)


# ---------------------------------------------------------------- LADDERS (16 x 32: the ladder's top block over its foot)
#  the ladders' own indices, per cave: outline (o, and o2 on the shaded side), lit, body, shade, the floor shadow
LAD = {"seafoam_islands": R(o=0xB, o2=0xB, hi=5, mid=7, lo=8, sh=(3, 4)),
       "cave": R(o=0xB, o2=0xB, hi=5, mid=7, lo=8, sh=(3, 4)),
       "mt_ember": R(o=0xB, o2=0xB, hi=5, mid=7, lo=8, sh=(3, 4)),
       "navel_rock": R(o=0xB, o2=0xC, hi=1, mid=5, lo=7, sh=(9, 9)),
       "digletts_cave": R(o=0x8, o2=0xC, hi=5, mid=6, lo=7, sh=(0xB, 0xB))}


def _foot(P, r, xs):
    """the ladder's feet (xs: the outline columns of each foot) and its shadow on the floor"""
    for x in range(1, 15):
        put(P, x, 30, r.sh[0])
    for x in range(2, 14):
        put(P, x, 31, r.sh[1])
    for x0, x1 in xs:
        for x in range(x0, x1 + 1):
            put(P, x, 30, r.o)


def ladder_A(r, h=32):
    P = blank(h, 16)
    for y in range(2, 30):
        for x0, inner in ((3, r.hi), (10, r.mid)):
            P[y][x0], P[y][x0 + 1], P[y][x0 + 2] = r.o, inner if y < 29 else r.lo, r.o2
    for x0 in (3, 10):
        P[2][x0], P[2][x0 + 2], P[2][x0 + 1] = 0, 0, r.o
    for y in range(6, 28, 5):
        for x in range(6, 10):
            P[y - 1][x], P[y][x], P[y + 1][x] = r.o, r.mid, r.o2
        P[y][5], P[y][10] = r.hi, r.mid
    _foot(P, r, [(3, 5), (10, 12)])
    return P


def ladder_B(r, h=32):
    P = blank(h, 16)
    for y in range(1, 30):
        tw = (y // 2) % 2
        for x0 in (2, 11):
            a, b = (r.mid, r.lo) if tw else (r.lo, r.mid)
            if x0 == 2:
                P[y][2], P[y][3], P[y][4] = r.o, a, b
            else:
                P[y][11], P[y][12], P[y][13] = a, b, r.o2
    for y in range(4, 28, 6):
        for x in range(1, 15):
            P[y - 1][x], P[y + 2][x] = r.o, r.o2
        for x in range(2, 14):
            P[y][x], P[y + 1][x] = r.hi, r.lo
        P[y][1] = P[y + 1][1] = r.o
        P[y][14] = P[y + 1][14] = r.o2
    _foot(P, r, [(2, 4), (11, 13)])
    return P


def ladder_C(r, h=32):
    P = blank(h, 16)
    for y in range(2, 30):
        P[y][6], P[y][7], P[y][8], P[y][9] = r.o, r.hi if y < 29 else r.lo, r.mid if y < 29 else r.lo, r.o2
    P[1][7] = P[1][8] = r.o
    for i, y in enumerate(range(4, 28, 4)):
        xs = range(2, 6) if i % 2 == 0 else range(10, 14)
        for x in xs:
            P[y - 1][x], P[y][x], P[y + 1][x] = r.o, r.mid, r.o2
        P[y][2 if i % 2 == 0 else 13] = r.o
        P[y][5 if i % 2 == 0 else 10] = r.hi
    _foot(P, r, [(6, 9)])
    return P


LADDER_DRAW = {"A": ladder_A, "B": ladder_B, "C": ladder_C}


def draw_ladder(ts):
    def f(pix, opt):
        return LADDER_DRAW[opt](LAD[ts], len(pix))
    return f


# ---------------------------------------------------------------- HOLES (16 x 16, the whole bottom layer)
#  bg: the floor round it (a pixel of one of these keeps pret's), lip: the near edge lit, rim, wall (the far side seen
#  falling away), black: the bottom you cannot see
HOLE = {("seafoam_islands", 0x286): R(bg={1, 2, 3, 4}, base=2, lip=4, rim=0xA, wall=0xB, black=0xC),
        ("seafoam_islands", 0x285): R(bg={1, 2, 3, 4}, base=2, lip=4, rim=0xA, wall=0xB, black=0xC),
        ("cave", 0x286): R(bg={1, 2, 3, 4}, base=4, lip=3, rim=0xA, wall=0xB, black=0xC),
        ("seafoam_islands", 0x35B): R(bg={5, 6, 7}, base=5, lip=6, rim=0xA, wall=0xC, black=0xF),
        ("cave", 0x285): R(bg={1, 2, 3, 4}, base=4, lip=3, rim=0xA, wall=0xB, black=0xC),
        ("mt_ember", 0x2AF): R(bg={1, 2, 3, 4}, base=4, lip=3, rim=0xB, wall=0xA, black=0xC),
        ("navel_rock", 0x2AF): R(bg={2, 3, 4}, base=4, lip=3, rim=0xA, wall=0xB, black=0xC),
        ("navel_rock", 0x286): R(bg={2, 3, 4}, base=4, lip=3, rim=0xA, wall=0xB, black=0xC),
        ("digletts_cave", 0x2AF): R(bg={1, 2, 3, 4}, base=3, lip=2, rim=4, wall=0xB, black=0xC)}
#  DEADSTACK's hole: its lower half (22, 23) is drawn by others (T-569 and the cave look), so only its upper half takes
#  the option and meets that lower half where it is
HOLE[("cave", 0x286)].keep_rows = range(8, 16)


def _hole_mask(opt):
    """{(x, y): class} for a 16x16 hole: 'rim', 'in', or absent (floor); class 'crack' for C's rays"""
    import math
    out = {}
    for y in range(1, 15):
        for x in range(1, 15):
            dx, dy = x + 0.5 - 8.0, y + 0.5 - 8.0
            a, d = math.atan2(dy, dx), math.hypot(dx, dy)
            if opt == "A":
                rr = 6.3 + 0.55 * math.sin(3 * a + 1.0) + 0.35 * math.sin(5 * a + 2.0)
            elif opt == "B":
                rr = 6.6
            else:
                rr = 5.4 + 1.3 * abs(math.sin(2.5 * a + 0.4)) ** 3
            if d <= rr - 1.0:
                out[(x, y)] = ("in", d / rr)
            elif d <= rr:
                out[(x, y)] = ("rim", d / rr)
    if opt == "C":
        for a in (0.55, 2.2, 3.7, 5.3):
            for s in range(5, 15):
                x, y = int(8.0 + math.cos(a) * s * 0.5 + 0.0), int(8.0 + math.sin(a) * s * 0.5)
                if 1 <= x <= 14 and 1 <= y <= 14 and (x, y) not in out:
                    out[(x, y)] = ("crack", 1.0)
    return out


def hole(pix, opt, r):
    P = [row[:] for row in pix]
    m = _hole_mask(opt)
    for y in range(16):
        for x in range(16):
            if (x, y) not in m and P[y][x] not in r.bg:
                P[y][x] = r.base
    for (x, y), (c, d) in m.items():
        if c == "crack":
            P[y][x] = r.rim
            continue
        if c == "rim":
            P[y][x] = r.rim
            continue
        up = m.get((x, y - 1), ("out",))[0]
        up2 = m.get((x, y - 2), ("out",))[0]
        if opt == "B":
            P[y][x] = r.wall if d > 0.72 else (r.rim if d > 0.62 else (r.wall if d > 0.45 and y < 8 else r.black))
        elif up != "in" or (up2 != "in" and y < 8):
            P[y][x] = r.wall
        else:
            P[y][x] = r.black
    #  the near edge, lit: the floor just under the rim on the bottom half
    for (x, y), (c, d) in m.items():
        if c == "rim" and y >= 8 and (x, y + 1) not in m and 1 <= y + 1 <= 14:
            P[y + 1][x] = r.lip
    for y in getattr(r, "keep_rows", ()):
        P[y] = pix[y][:]
    return P


def draw_hole(ts, b):
    def f(pix, opt):
        return hole(pix, opt, HOLE[(ts, b)])
    return f


def draw_ladder_hole(ts, b):
    """a ladder going down a hole (GLAUCOUS ISLES' 0x285): the hole as HOLES A draws it, the ladder's top in the
    ladder option, its rails running into the dark"""
    def f(pix, opt):
        P = hole(pix, "A", HOLE[(ts, b)])
        lad = LADDER_DRAW[opt](LAD[ts], 32)
        for y in range(16):
            for x in range(16):
                v = lad[y + 4][x]
                if v and y >= 2:
                    P[y][x] = v if y < 12 or v in (LAD[ts].o, LAD[ts].o2) else HOLE[(ts, b)].wall
        return P
    return f


# ---------------------------------------------------------------- SLIDE ICE (16-pixel periodic; only ice pixels drawn)
ICE = R(ice={5, 6, 7}, shade=5, base=6, light=7, deep=(8, 9, 0xA), crack=0xB)


def ice_at(opt, x, y):
    """the slide ice's index at block pixel (x, y), period 16 both ways, so blocks tile and every edge seams"""
    import math
    x, y = x % 16, y % 16
    if opt == "A":
        d = (x + y) % 16
        if (x, y) == (13, 9) or (abs(x - 13) + abs(y - 9) == 1):
            return ICE.light
        if d == 3 or d == 10:
            return ICE.light
        if d in (2, 4):
            return ICE.base
        return ICE.shade
    if opt == "B":
        for cx, cy, rr in ((-3, 19, 15.0), (19, 21, 12.5), (6, -9, 13.0)):
            for kx in (-16, 0, 16):
                for ky in (-16, 0, 16):
                    if abs(math.hypot(x + 0.5 - cx - kx, y + 0.5 - cy - ky) - rr) < 0.55:
                        return ICE.shade
        if (x, y) in ((4, 4), (12, 11)):
            return ICE.light
        return ICE.base
    seeds = [(3, 4, ICE.light), (11, 2, ICE.base), (6, 11, ICE.base), (13, 12, ICE.shade)]
    ds = []
    for sx, sy, c in seeds:
        for kx in (-16, 0, 16):
            for ky in (-16, 0, 16):
                ds.append((math.hypot(x + 0.5 - sx - kx, y + 0.5 - sy - ky), c))
    ds.sort()
    if ds[1][0] - ds[0][0] < 0.9:
        return ICE.shade if ds[0][1] != ICE.shade else ICE.base
    return ds[0][1]


def draw_ice(pix, opt):
    return [[ice_at(opt, x, y) if pix[y][x] in ICE.ice else pix[y][x] for x in range(len(pix[0]))]
            for y in range(len(pix))]


def _pane(x, y):
    """thin ice's pane: a rounded square inside the block -> 0 outside, 1 its edge, 2 the ring in, 3 the middle"""
    if not (2 <= x <= 13 and 2 <= y <= 13) or min(x - 2, 13 - x) + min(y - 2, 13 - y) < 2:
        return 0
    e = min(x - 2, 13 - x, y - 2, 13 - y)
    corner = min(x - 2, 13 - x) + min(y - 2, 13 - y)
    if e == 0 or corner == 2:
        return 1
    if e == 1 or corner == 3:
        return 2
    return 3


CRACKS = [(7, 8), (6, 7), (5, 6), (4, 6), (3, 5), (8, 7), (9, 6), (9, 5), (10, 4), (11, 3), (8, 9), (9, 10), (10, 10),
          (11, 11), (12, 12), (6, 9), (5, 10), (5, 11), (4, 12), (7, 10), (7, 11), (8, 12), (2, 5), (12, 2), (13, 13),
          (3, 13), (10, 9), (11, 8), (12, 8)]


def thin_ice(opt, cracked=False):
    def f(pix, o):
        P = [[0] * 16 for _ in range(16)]
        for y in range(16):
            for x in range(16):
                k = _pane(x, y)
                if k == 0:
                    P[y][x] = ice_at(o, x, y)
                else:
                    P[y][x] = ICE.deep[k - 1]
                    if k == 3:
                        if o == "A" and (x + y) % 16 in (13, 14):
                            P[y][x] = ICE.deep[0]
                        if o == "B" and abs(((x - 3) ** 2 + (y - 15) ** 2) ** 0.5 - 10.0) < 0.6:
                            P[y][x] = ICE.deep[0]
                        if o == "C" and (x == 7 or y == 8):
                            P[y][x] = ICE.deep[1]
        if cracked:
            for (x, y) in CRACKS:
                P[y][x] = ICE.light
                if x + 1 < 16 and (x + 1, y) not in CRACKS and _pane(x + 1, y):
                    P[y][x + 1] = ICE.crack
        return P
    return f


# ---------------------------------------------------------------- OTHER PIECES
def keep_border(P, pix):
    """a block's outer ring keeps pret's pixels: where a neighbour meets it, the seam stays"""
    h, w = len(P), len(P[0])
    for y in range(h):
        for x in range(w):
            if x in (0, w - 1) or y in (0, h - 1):
                P[y][x] = pix[y][x]
    return P


def draw_trickle(pix, opt):
    """the trickle down a cave wall into its pool (252/253): A, falling water -- light dashes down its lit side, a
    drop every fourth pixel on its far one; B, one lit edge, still. Its own two waters, d and e"""
    P = [row[:] for row in pix]
    for y in range(16):
        for x in range(16):
            if not pix[y][x]:
                continue
            if opt == "B":
                P[y][x] = 0xD if x < 15 else 0xE
            elif x < 15:
                P[y][x] = 0xD if (y // 2) % 2 == 0 else 0xE
            else:
                P[y][x] = 0xD if y % 4 == 1 else 0xE
    return P


def draw_pool(pix, opt):
    """the pool the trickle falls into (254/255): rings spreading from where it lands (A), or one lit near edge (B)"""
    P = [row[:] for row in pix]
    for y in range(16):
        for x in range(16):
            if not pix[y][x]:
                continue
            if opt == "A":
                d = ((x + 0.5 - 15.5) ** 2 + ((y + 0.5) * 1.6) ** 2) ** 0.5
                P[y][x] = 0xD if abs(d - 4.5) < 0.6 or abs(d - 9.5) < 0.6 or abs(d - 14.5) < 0.6 else 0xE
            else:
                P[y][x] = 0xD if y + 1 < 16 and not pix[y + 1][x] else 0xE
    return P


SPA_A = {(1, 1): 2, (2, 2): 2, (3, 2): 2, (4, 1): 2, (6, 7): 2, (7, 7): 2}
SPA_B = {(2, 2): 2, (3, 2): 2}


def draw_spa(pix, opt):
    """MT. SMOULDER's spa water (one index, 247 laid 2 x 2): small ripple marks on an eight-pixel beat, never in a
    tile's rows 5 and 6, so the far edge's reflection band (230/231) is kept as it is"""
    marks = SPA_A if opt == "A" else SPA_B
    P = [row[:] for row in pix]
    for y in range(len(pix)):
        for x in range(len(pix[0])):
            if pix[y][x] == 1:
                P[y][x] = marks.get((x % 8, y % 8), 1)
    return P


def draw_embers(pix, opt):
    """the embers in MT. SMOULDER's steps (264/266/286): pret's yellow dither, gone; two coals a tile (A) or one (B),
    each a lit point over a dull one, set in the stone's own body"""
    P = [row[:] for row in pix]
    for y in range(16):
        for x in range(16):
            if pix[y][x] == 6:
                P[y][x] = 0xD
    coals = [(3, 9), (11, 10)] if opt == "A" else [(4, 9)]
    for cx, cy in coals:
        for (dx, dy, c) in ((0, 0, 6), (1, 0, 6), (0, 1, 0xE), (1, 1, 6) if opt == "A" else (1, 1, 0xE)):
            if pix[cy + dy][cx + dx] in (5, 6, 0xD, 0xE):
                P[cy + dy][cx + dx] = c
    return P


def draw_button(pix, opt):
    """VICTORY ROAD's press plate (the STRENGTH button, primary row 2): its round outline kept; a lit dome, its rim
    under it, and (A) a pressed-in chevron that says push something here"""
    import math
    P = [row[:] for row in pix]
    for y in range(16):
        for x in range(16):
            c = pix[y][x]
            if c in (1, 2, 4):
                d = math.hypot(x + 0.5 - 7.0, y + 0.5 - 6.0)
                P[y][x] = 4 if y >= 11 else (1 if d < 3.2 and (x + y) < 13 else 2)
    if opt == "A":
        for y, xs in ((5, range(5, 11)), (6, range(6, 10)), (7, range(7, 9))):
            for x in xs:
                P[y][x] = 4
    else:
        for x, y in ((7, 6), (8, 6)):
            P[y][x] = 4
    return P


def relight(lit, body, shade, keep, quiet=False):
    """pebbles and boulder caps: every blob lit from its upper left -- the light reaches as far as the blob goes
    up-left of it (two steps lit, then the body, the shade at its foot); pixels of KEEP (outlines) stay"""
    def f(pix, opt):
        P = [row[:] for row in pix]
        h, w = len(pix), len(pix[0])
        for y in range(h):
            for x in range(w):
                c = pix[y][x]
                if not c or c in keep:
                    continue
                k = 0
                while 0 <= y - k - 1 and 0 <= x - k - 1 and pix[y - k - 1][x - k - 1] and \
                        pix[y - k - 1][x - k - 1] not in keep:
                    k += 1
                j = 0
                while y + j + 1 < h and x + j + 1 < w and pix[y + j + 1][x + j + 1] and \
                        pix[y + j + 1][x + j + 1] not in keep:
                    j += 1
                if opt == "B":
                    P[y][x] = lit if (k == 1 and j >= 3) else (shade if j == 0 else body)
                else:
                    P[y][x] = lit if k <= 1 else (shade if j <= 1 else body)
        return P
    return f


def draw_glow(pix, opt):
    """NAVEL ROCK's summit light (94, with 79 beside it): pret's dithered fall-off as bands, brightest at the top --
    four (A), or two with one dithered row each between (B)"""
    P = [row[:] for row in pix]
    bands = {0: 8, 1: 7, 2: 6, 3: 6, 4: 5, 5: 5, 6: 5} if opt == "A" else {0: 8, 1: 7, 2: 7, 3: 6, 4: 6, 5: 5, 6: 5}
    for y in range(7):
        for x in range(len(pix[0])):
            if pix[y][x] in (5, 6, 7, 8):
                P[y][x] = bands[y] if not (opt == "B" and y in (1, 3) and x % 2) else bands[y + 1]
    return P


def draw_berries(pix, opt):
    """DENSE WOOD's berry patch: pret's checker of leaves cleared, the berries in round clusters (three, lit at the
    top left) on leaf sprigs, two small white flowers; B, two clusters and no flowers. The ring keeps its seams"""
    P = blank(16, 16)
    leaf, berry, lit, white = 0xC, 0xE, 0xB, 0xD
    clusters = [(3, 3), (10, 8), (4, 11)] if opt == "A" else [(4, 4), (10, 10)]
    for cx, cy in clusters:
        for dx, dy in ((-2, 1), (-1, 2), (2, -1), (3, 0), (1, 3)):
            put(P, cx + dx, cy + dy, leaf)
        for bx, by in ((0, 0), (2, 1), (0, 2)):
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                put(P, cx + bx + dx, cy + by + dy, berry)
            put(P, cx + bx, cy + by, lit)
    if opt == "A":
        for fx, fy in ((12, 3), (8, 13)):
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                put(P, fx + dx, fy + dy, white)
            put(P, fx, fy, berry)
    return keep_border(P, pix)


def draw_harbour(pix, opt):
    """the harbour halls' red walls and yellow skirt (one index each): A, boards -- a tarred seam every fourth row on
    the red, a batten every eighth pixel on the yellow; B, the red's laps lit instead, the skirt left plain"""
    P = [row[:] for row in pix]
    for y in range(len(pix)):
        for x in range(len(pix[0])):
            c = pix[y][x]
            if c == 0xB and y % 4 == 3:
                P[y][x] = 2 if opt == "A" else 0xD
            elif c == 0xC and opt == "A" and x % 8 == 7:
                P[y][x] = 0xE
    return P


def draw_pylon(pix, opt):
    """the islands' red piling (365, in the sea by the halls): its cap and outline kept; the web between the rails a
    bolted cross-brace (A) or a plain girder with a rivet row (B)"""
    P = [row[:] for row in pix]
    for y in range(2, 6):
        for x in range(0, 14):
            if opt == "A":
                a = 2 + round(x * 3 / 13.0)
                b = 5 - round(x * 3 / 13.0)
                P[y][x] = 0xD if y in (a, b) else (0xE if y - 1 in (a, b) else 0)
            else:
                P[y][x] = 0xD if y < 4 else 0xE
                if y == 3 and x % 4 == 1:
                    P[y][x] = 0xA
    return P


def draw_stall(pix, opt):
    """TWO ISLAND's stall front (118): its red body in slats (A) or lit along its top (B); frame and slot kept"""
    P = [row[:] for row in pix]
    for y in range(8, 16):
        for x in range(16):
            if pix[y][x] == 0xD:
                if opt == "A" and y % 2 == 1:
                    P[y][x] = 0xC
                if opt == "B" and y == 10:
                    P[y][x] = 0xC
    return P


#  NOT objects here: the ladders down a hole in DEADSTACK, MT. SMOULDER, NAVEL ROCK and TAPPOINT'S (0x285/0x2AF) and
#  NAVEL ROCK's fall hole are the cave look's (gbacaves) and still draw pret's slanted ladder -- if a ladder option is
#  picked, they want the same ladder there, drawn by that tool (the T-570 report names it)
#  the objects: (kind, tileset, what, grid of blocks, layer, drawing). A pair of blocks that share tiles (0x2F6/0x2F7, a
#  ladder's 0x296/0x297) is drawn once: the other shows the same tiles, mirrored or not
OBJECTS_570 = []
for _ts in ("seafoam_islands", "cave", "mt_ember", "navel_rock", "digletts_cave"):
    OBJECTS_570.append(("ladders", _ts, "the ladder (top 0x28E over foot 0x296)", [[0x28E], [0x296]], 1,
                        draw_ladder(_ts)))
OBJECTS_570 += [
    ("ladders", "seafoam_islands", "the ladder down a hole (0x285)", [[0x285]], 0,
     draw_ladder_hole("seafoam_islands", 0x285)),
    ("holes", "seafoam_islands", "the fall hole (0x286)", [[0x286]], 0, draw_hole("seafoam_islands", 0x286)),
    ("holes", "cave", "the fall hole (0x286)", [[0x286]], 0, draw_hole("cave", 0x286)),
    ("holes", "seafoam_islands", "the ice hole (0x35B, after cracked ice)", [[0x35B]], 0,
     draw_hole("seafoam_islands", 0x35B)),
    ("ice", "seafoam_islands", "the slide ice (0x34B)", [[0x34B]], 0, lambda p, o: draw_ice(p, o)),
    ("ice", "seafoam_islands", "the slide ice's frosted edge (0x346)", [[0x346]], 0, lambda p, o: draw_ice(p, o)),
    ("ice", "seafoam_islands", "the floor's frosted edge (0x34C)", [[0x34C]], 0, lambda p, o: draw_ice(p, o)),
    ("ice", "seafoam_islands", "thin ice (0x359)", [[0x359]], 0, None),
    ("ice", "seafoam_islands", "cracked ice (0x35A)", [[0x35A]], 0, None),
    ("other", "seafoam_islands", "a boulder's lit cap (0x283)", [[0x283]], 1, relight(9, 8, 0xA, {0xD, 0xE, 0xC})),
    ("other", "seafoam_islands", "a boulder on ice, its lit cap (0x347)", [[0x347]], 1,
     relight(9, 8, 0xA, {0xD, 0xE, 0xC})),
    ("other", "navel_rock", "the rubble (0x283)", [[0x283]], 1, relight(9, 0xC, 0xD, {0xE})),
    ("other", "cave", "the press plate (0x2C0, the STRENGTH button)", [[0x2C0]], 1, draw_button),
    ("other", "mt_ember", "the spa's water (0x331 over 0x339)", [[0x331], [0x339]], 0, draw_spa),
    ("other", "mt_ember", "the spa's corner (0x330)", [[0x330]], 0, draw_spa),
    ("other", "berry_forest", "the berry patch (0x282)", [[0x282]], 1, draw_berries),
    ("other", "island_harbor", "the hall's red wall (0x290 over 0x298)", [[0x290], [0x298]], 0, draw_harbour),
    ("other", "island_harbor", "the hall's corner (0x2C4)", [[0x2C4]], 0, draw_harbour),
    ("other", "island_harbor", "the hall's corner (0x2C6)", [[0x2C6]], 0, draw_harbour),
    ("other", "island_harbor", "the skirt by the steps (0x2CC)", [[0x2CC]], 0, draw_harbour),
    ("other", "island_harbor", "the skirt by the steps (0x2CE)", [[0x2CE]], 0, draw_harbour),
    ("other", "sevii_islands_123", "the stall front (0x2A1)", [[0x2A1]], 1, draw_stall),
]
for _ts in ("seafoam_islands", "cave", "mt_ember"):
    OBJECTS_570 += [("other", _ts, "the trickle down the wall (0x2EE)", [[0x2EE]], 1, draw_trickle),
                    ("other", _ts, "its pool (0x2F6)", [[0x2F6]], 1, draw_pool)]
OBJECTS_570 = [(k, ts, w, g, l, f if f else thin_ice(None, cracked="cracked" in w)) for k, ts, w, g, l, f in OBJECTS_570]

#  what T-570 leaves, and why (every one of the 134 not drawn above is named here, so the report adds up)
LEFT_WHY = {
    "blackout": "THE BLACKOUT (rock_tunnel): left as T-546 drew it -- its purple and glowing green link to the story "
                "(the user); its seven are seam slivers and its pools' rim, in T-546's purple",
    "sliver": "a seam sliver: one to three pixels (a slope's or a sill's last pixel, a rail's end) that only finish "
              "a neighbour's outline -- nothing to draw, and moving one moves the seam",
    "black": "flat black (the void beyond a cave or over the harbour): nothing pret drew",
    "door": "a doorway or cave mouth (a door, gbadoors/gbaprimary's; THE DOTS' opened door is placed by its braille "
            "script)",
    "half": "one quarter or half of a piece whose other part another tool drew (the embers' steps beside 265/287, "
            "the red piling beside gbatowns' 364, NAVEL ROCK's summit light beside 79): a new drawing on this half "
            "alone would split the piece at the seam -- drawn with its other half, if ever (draw_embers, draw_pylon "
            "and draw_glow are kept for that)",
    "rail": "a railing's corner post: two-pixel rails that meet T-569's railing either side; drawn with them, if ever",
}


def left_570():
    """{(ts, tile): why} for the 134 this pass does not draw"""
    out = {}
    for t in (11, 32, 37, 252, 253, 254, 255):
        out[("rock_tunnel", t)] = "blackout"
    for ts, ts_tiles in (("seafoam_islands", [32]), ("cave", [32, 37]), ("mt_ember", [32, 37, 246]),
                         ("navel_rock", [32, 37]), ("sevii_islands_67", [52, 53]), ("sevii_islands_123", [52, 53, 140]),
                         ("sevii_islands_45", [52, 53, 115])):
        for t in ts_tiles:
            out[(ts, t)] = "sliver"
    for ts, t in (("cave", 16), ("island_harbor", 16)):
        out[(ts, t)] = "black"
    for ts, ts_tiles in (("cave", [166, 182]), ("island_harbor", [148]), ("sevii_islands_67", [216, 217, 232, 233])):
        for t in ts_tiles:
            out[(ts, t)] = "door"
    out[("island_harbor", 9)] = "rail"
    for ts, ts_tiles in (("mt_ember", [264, 266, 286]), ("sevii_islands_67", [365]), ("sevii_islands_123", [365]),
                         ("sevii_islands_45", [365]), ("navel_rock", [94])):
        for t in ts_tiles:
            out[(ts, t)] = "half"
    return out


#  never drawn by T-570, whatever an object reaches: the tilesets and tiles other tools own
NEVER_570 = {"rock_tunnel", "underground_path"}


def later_569():
    """{ts: set of tiles} -- T-569's leftovers, from its own census (BASE), the same as draft.json's 'later'"""
    p = os.path.join(DRAFT_DEFAULT, "draft.json")
    return {ts: set(v) for ts, v in json.load(open(p))["later"].items()}


_MINE569 = {}


def mine_569(ts):
    """the tiles T-569's approved pick drew in TS (this tool's own work, so a T-570 object may redraw them)"""
    if ts not in _MINE569:
        _MINE569[ts] = set(picked(ts, APPROVED[ts])[1]) if ts in APPROVED else set()
    return _MINE569[ts]


def draw_570(opt_of):
    """{ts: {tile: pixels}} for the options in OPT_OF {kind: option}, and per object (kind, ts, what, written tiles,
    tiles it reached but left, conflicts)"""
    later = later_569()
    out = collections.defaultdict(dict)
    log = []
    for kind, ts, what, grid, layer, f in OBJECTS_570:
        if kind not in opt_of or ts in NEVER_570:
            continue
        pix, own, rows = canvas(ts, grid, layer)
        new = f(pix, opt_of[kind])
        base = base570(ts)
        allowed = later.get(ts, set()) | mine_569(ts)
        if kind == "other":
            allowed = later.get(ts, set())          # the last pieces only: T-569's drawing round them stays
        wrote, held, first, conflict = {}, set(), {}, 0
        for (Y, X), (t, k) in sorted(own.items()):
            if t not in allowed:
                if new[Y][X] != pix[Y][X]:
                    held.add(t)
                continue
            if (t, k) in first:
                conflict += first[(t, k)] != new[Y][X]
                continue
            first[(t, k)] = new[Y][X]
            wrote.setdefault(t, list(out[ts].get(t, base[t])))[k] = new[Y][X]
        for t, p in wrote.items():
            if p != base[t]:
                out[ts][t] = p
        log.append((kind, ts, what, sorted(t for t, p in wrote.items() if p != base[t]), sorted(held), conflict))
    return out, log


# ---------------------------------------------------------------- pictures
SPLIT_PALS = {"gTileset_Stillfall": "palettes_stillfall", "gTileset_CaveUmbral": "palettes_umbral"}


def tiles_with(ts, out):
    base = [list(t) for t in base570(ts)]
    for t, p in out.get(ts, {}).items():
        base[t] = list(p)
    return base


def town_for(ts, m):
    """TS's town, read in the light of map M (a palette split's own rows: STILLFALL, UMBRAL ASCENT)"""
    town = town570(ts)
    sec = T.layouts()[m]["secondary_tileset"]
    return with_pals(town, SPLIT_PALS[sec]) if sec in SPLIT_PALS else town


def block_img(ts, grid, tiles, town=None, Z=4):
    """the blocks of GRID, both layers, from TILES, at Z x"""
    town = town or town570(ts)
    G = town.G
    allp = [G["pals"][r] for r in range(7)] + [town.pals[r] for r in range(7, 16)]
    H, W = 16 * len(grid), 16 * len(grid[0])
    im = Image.new("RGB", (W, H), allp[0][0])
    o = im.load()
    for by, line in enumerate(grid):
        for bx, b in enumerate(line):
            e = T.entries(town.mt, b - 640)
            for layer in (0, 1):
                for q in range(4):
                    v = e[layer * 4 + q]
                    t, row = v & 0x3FF, v >> 12
                    src = G["tiles"][t] if t < 640 else (tiles[t - 640] if t - 640 < len(tiles) else [0] * 64)
                    for ty in range(8):
                        for tx in range(8):
                            sx = 7 - tx if v & 0x400 else tx
                            sy = 7 - ty if v & 0x800 else ty
                            c = src[sy * 8 + sx]
                            if c:
                                o[bx * 16 + (q % 2) * 8 + tx, by * 16 + (q // 2) * 8 + ty] = allp[row][c]
    return im.resize((W * Z, H * Z), Image.NEAREST)


def object_sheet(kind, results, path):
    """every object of KIND: today | A | B | C at 4x, both layers, in its own light"""
    K = KINDS_570[kind]
    objs = [o for o in OBJECTS_570 if o[0] == kind and o[1] not in NEVER_570]
    Z = 4
    cells = []
    for _, ts, what, grid, layer, _ in objs:
        ims = [block_img(ts, grid, base570(ts), Z=Z)] + \
              [block_img(ts, grid, tiles_with(ts, results[(kind, o)][0]), Z=Z) for o, _, _ in K["options"]]
        cells.append(("%s -- %s" % (NAME.get(ts, ts), what), ims))
    cw = max(im.width for _, ims in cells for im in ims)
    chh = max(im.height for _, ims in cells for im in ims)
    per = len(K["options"]) + 1
    cols = 1
    W = cols * (per * (cw + 8) + 24) + 16
    H = 64 + ((len(cells) + cols - 1) // cols) * (chh + 34)
    out = Image.new("RGB", (max(W, 760), H), T.BG)
    d = ImageDraw.Draw(out)
    d.text((8, 6), "T-570 %s -- today | %s, each object at %dx, both layers -- DRAFT" % (
        K["name"], " | ".join(o for o, _, _ in K["options"]), Z), font=T.font(13), fill=(20, 20, 20))
    for i, (o, title, line) in enumerate(K["options"]):
        d.text((8, 24 + i * 13), "%s %s -- %s%s" % (o, title, line, "   (recommended)" if o == K["rec"] else "")[:170],
               font=T.font(10), fill=(50, 50, 50))
    y0 = 30 + 13 * len(K["options"])
    for n, (label, ims) in enumerate(cells):
        x = 8 + (n % cols) * (per * (cw + 8) + 24)
        y = y0 + (n // cols) * (chh + 34)
        d.text((x, y), label[:max(20, (out.width - 16) // 7)], font=T.font(11), fill=(30, 30, 30))
        for j, im in enumerate(ims):
            out.paste(im, (x + j * (cw + 8), y + 16))
    out.save(path)
    return path


def maps_for(kind):
    """[(ts, map, box)]: for each object of KIND, the reachable map that places its blocks most, a GBA screen round
    the first of them; one crop per (ts, map)"""
    reach = reachable()
    seen, out = set(), []
    for k, ts, what, grid, layer, f in OBJECTS_570:
        if k != kind or ts in NEVER_570:
            continue
        town = town570(ts)
        blocks = {b for line in grid for b in line}
        best = None
        for m in town.maps:
            if m not in reach:
                continue
            g = town.grid[m]
            n = sum(1 for v in g if v in blocks)
            if n and (best is None or n > best[0]):
                best = (n, m)
        if not best or (ts, best[1]) in seen:
            continue
        m = best[1]
        seen.add((ts, m))
        l = T.layouts()[m]
        g = town.grid[m]
        k0 = next(i for i, v in enumerate(g) if v in blocks)
        x, y = k0 % l["width"], k0 // l["width"]
        W, H = min(15, l["width"]), min(10, l["height"])
        box = (max(0, min(l["width"] - W, x - W // 2)), max(0, min(l["height"] - H, y - H // 2)), W, H)
        out.append((ts, m, box, what))
    return out


def map_sheet_570(kind, results, path, tmp):
    """today (tools/reviewsheet.py map, from what the ROM is built from) beside each option (the same window drawn
    from the draft's tiles), at 2x, on the maps that show the kind"""
    import subprocess
    K = KINDS_570[kind]
    rows = []
    for ts, m, box, what in maps_for(kind):
        shot = os.path.join(tmp, "today_%s_%s.png" % (kind, m))
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "reviewsheet.py"), "map", shot, m] +
                       [str(v) for v in box], check=True, capture_output=True)
        tw = town_for(ts, m)
        ims = [Image.open(shot).convert("RGB")] + \
              [T.render(tw, m, tiles=tiles_with(ts, results[(kind, o)][0]), box=box) for o, _, _ in K["options"]]
        rows.append(("%s  %s  cells %d,%d %dx%d  (%s)" % (NAME.get(ts, ts), m, box[0], box[1], box[2], box[3], what),
                     ims))
    Z = 2
    cw, ch = 15 * 16 * Z, 10 * 16 * Z
    per = len(K["options"]) + 1
    W = 16 + per * (cw + 10)
    H = 44 + max(1, len(rows)) * (ch + 34)
    out = Image.new("RGB", (W, H), T.BG)
    d = ImageDraw.Draw(out)
    d.text((8, 6), "T-570 %s on the maps -- today (reviewsheet.py map) | %s, at 2x -- DRAFT" % (
        K["name"], " | ".join("%s %s" % (o, t) for o, t, _ in K["options"])), font=T.font(12), fill=(20, 20, 20))
    y = 28
    for label, ims in rows:
        d.text((8, y), label[:140], font=T.font(11), fill=(30, 30, 30))
        for j, im in enumerate(ims):
            out.paste(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (8 + j * (cw + 10), y + 14))
        y += ch + 34
    out.save(path)
    return path


# ---------------------------------------------------------------- report, drafts, write
def run_570(draft_dir=None, sheets=False):
    later, left = later_569(), left_570()
    results = {}
    for kind, K in KINDS_570.items():
        for o, _, _ in K["options"]:
            results[(kind, o)] = draw_570({kind: o})
    print("  T-570 (BASE %s): the last tiles, drawn by hand -- %d left by T-569 in %d tilesets" % (
        BASE_570, sum(len(v) for v in later.values()), len(later)))
    drawn = set()
    report = collections.OrderedDict()
    for kind, K in KINDS_570.items():
        out, log = results[(kind, "A")]
        n_later = sorted((ts, t) for ts, tt in out.items() for t in tt if t in later.get(ts, ()))
        n_mine = sorted((ts, t) for ts, tt in out.items() for t in tt if t not in later.get(ts, ()))
        drawn |= set(n_later)
        print("\n  %-15s %d objects; option A draws %d of the 134%s" % (
            K["name"], len(log), len(n_later), "" if not n_mine else
            " and redraws %d of T-569's own round them (the object drawn whole)" % len(n_mine)))
        for o, title, line in K["options"]:
            print("      %s %-28s %s%s" % (o, title, line[:90], "  << recommended" if o == K["rec"] else ""))
        for k, ts, what, wrote, held, conflict in log:
            print("      %-18s %-48s writes %-3d%s%s" % (ts, what[:48], len(wrote),
                  "  leaves %s as drawn (%s)" % (held, "the last pieces only" if k == "other" else "another tool's") if held else "", "  CONFLICT %d" % conflict if conflict else ""))
        report[kind] = dict(name=K["name"], recommended=K["rec"],
                            options=[dict(option=o, title=t, line=l) for o, t, l in K["options"]],
                            objects=[dict(tileset=ts, what=w, tiles=wr, held=h) for _, ts, w, wr, h, _ in log],
                            of_134=len(n_later), t569_redrawn=len(n_mine))
    alll = {(ts, t) for ts, tt in later.items() for t in tt}
    unacc = sorted(alll - drawn - set(left))
    print("\n  left, and why (%d):" % len(left))
    for why, text in LEFT_WHY.items():
        tl = sorted((ts, t) for (ts, t), w in left.items() if w == why)
        print("      %-9s %2d  %s\n                    %s" % (why, len(tl), text[:110], ", ".join(
            "%s %d" % (ts, t) for ts, t in tl)))
    print("\n  the 134: drawn %d, left %d, unaccounted %d%s" % (len(drawn), len(set(left) & alll), len(unacc),
                                                              "  " + str(unacc) if unacc else ""))
    if draft_dir:
        os.makedirs(draft_dir, exist_ok=True)
        for (kind, o), (out, _) in results.items():
            for ts in out:
                d = os.path.join(draft_dir, kind)
                os.makedirs(d, exist_ok=True)
                L.save_tiles(town570(ts), tiles_with(ts, out), os.path.join(d, "%s_%s.png" % (ts, o)))
        json.dump(dict(ticket="T-570", status="DRAFT -- nothing approved (APPROVED_570 is empty)", base=BASE_570,
                       kinds=report, drawn=sorted("%s %d" % k for k in drawn),
                       left={"%s %d" % k: LEFT_WHY[w] for k, w in sorted(left.items())}, unaccounted=unacc),
                  open(os.path.join(draft_dir, "draft.json"), "w"), indent=1)
        print("  drafts in %s" % draft_dir)
    if sheets:
        sd = os.path.join(draft_dir, "sheets")
        os.makedirs(sd, exist_ok=True)
        tmp = os.path.join(sd, ".today")
        os.makedirs(tmp, exist_ok=True)
        for kind in KINDS_570:
            print("  wrote %s" % object_sheet(kind, results, os.path.join(sd, "t570_%s_objects.png" % kind)))
            print("  wrote %s" % map_sheet_570(kind, results, os.path.join(sd, "t570_%s_maps.png" % kind), tmp))
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    return results, unacc


_A570 = []


def approved_570_tiles():
    """{ts: {tile: pixels}} of the approved T-570 picks (empty until picked); drawn once a run"""
    if not _A570:
        _A570.append(draw_570(APPROVED_570)[0] if APPROVED_570 else {})
    return _A570[0]


def check_engine_570():
    bad = 0
    for ts, tt in approved_570_tiles().items():
        disk = town570(ts).disk
        miss = [t for t, p in tt.items() if disk[t] != p]
        print("  engine %-18s T-570 %3d tiles%s" % (ts, len(tt), "  DIFFERS" if miss else "  as approved"))
        bad += bool(miss)
    return bad


def main_570():
    if "--write" in ARGS:
        if "--approved" not in ARGS or not APPROVED_570:
            print("  --t570 --write refused: --write needs --approved, and APPROVED_570 names nothing the user has "
                  "picked. Nothing written.")
            return 0
        for ts, tt in approved_570_tiles().items():
            town = town570(ts)
            out = [list(t) for t in town.disk]
            for t, p in tt.items():
                out[t] = list(p)
            if out == town.disk:
                print("  %s: already drawn, nothing to write" % ts)
                continue
            L.save_tiles(town, out, os.path.join(town.dir, "tiles.png"))
            print("  wrote %s: %d tiles (T-570 %s)" % (ts, len(tt), APPROVED_570))
        return 0
    for flag in ("--sheets", "--draft"):
        if flag in ARGS:
            i = ARGS.index(flag)
            d = ARGS[i + 1] if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--") else DRAFT_570
            _, unacc = run_570(d, sheets=flag == "--sheets")
            return 1 if unacc else 0
    _, unacc = run_570(None)
    bad = check_engine_570()
    print("  the engine %s" % ("matches every approved T-570 pick (none yet)" if not bad else
                               "DIFFERS from %d approved T-570 picks" % bad))
    return 1 if bad or unacc else 0


# ================================================================== main
def run(draft_dir=None, sheets=False):
    report = collections.OrderedDict()
    tot = collections.Counter()
    print("  T-569 census (BASE %s): per tileset -- ours / pret's and reachable / pret's unreachable / pret's unused"
          % BASE)
    only = ARGS[ARGS.index("--only") + 1].split(",") if "--only" in ARGS else None
    for ts, name in SETS:
        if only and ts not in only:
            continue
        town, cls, why, per, news = draw_set(ts)
        c = collections.Counter(cls.values())
        ch = {o: sum(1 for t in range(len(new)) if new[t] != town.now[t]) for o, _, _, new in news}
        undrawn = sorted(town.targets - {t for t in range(len(news[0][-1])) if news[0][-1][t] != town.now[t]})
        print("\n  %-44s %-18s ours %3d  pret+reach %3d  unreachable %d  unused %3d%s" % (
            name, ts, c["ours"], c["reach"], c["unreachable"], c["unused"],
            "  anim %d (the steam, drawn as frames)" % c["anim"] if c["anim"] else ""))
        for r, n in collections.Counter(why.values()).items():
            print("        excluded: %-46s %d" % (r, n))
        print("        targets %d; redrawn %s; left as pret's %d (a single-index family, or a tile no map draws in "
              "its blockdata)" % (len(town.targets), " / ".join("%s %d" % kv for kv in ch.items()), len(undrawn)))
        print("        most seen: %s" % ", ".join("%s %d" % kv for kv in per.most_common(6)))
        rep = dict(name=name, ours=c["ours"], reach=c["reach"], unreachable=c["unreachable"], unused=c["unused"],
                   anim=c["anim"], excluded={str(t): w for t, w in why.items()}, targets=len(town.targets),
                   redrawn=ch, undrawn=undrawn, maps=dict(per.most_common()),
                   options=[dict(option=o, title=t, line=l) for o, t, l, _ in news])
        report[ts] = rep
        for k in ("ours", "reach", "unreachable", "unused"):
            tot[k] += c[k]
        tot["targets"] += len(town.targets)
        tot["redrawn"] += ch["A"]
        if undrawn:
            LATER[ts] = undrawn
        if draft_dir:
            d = os.path.join(draft_dir, ts)
            os.makedirs(d, exist_ok=True)
            for o, _, _, new in news:
                L.save_tiles(town, new, os.path.join(d, "tiles_%s.png" % o))
        if sheets:
            sd = os.path.join(draft_dir, "sheets")
            print("        wrote %s" % tile_sheet(town, news, os.path.join(sd, "t569_tiles_%s.png" % ts),
                                                  "T-569 %s (%s): %d tiles drawn -- DRAFT" % (name, ts, max(ch.values()))))
            maps = [(m, town, "today's light") for m in crop_maps(town)]
            if ts in SPLITS:
                sn, folder, sm = SPLITS[ts]
                if sm in town.grid:
                    maps.append((sm, with_pals(town, folder), sn + "'s light (a split: the same tiles)"))
            print("        wrote %s" % map_sheet(town, news, maps, os.path.join(sd, "t569_map_%s.png" % ts),
                                                 "T-569 %s -- today beside each option, on the maps that show the most "
                                                 "of it -- DRAFT" % name))
    print("\n  all twelve: ours %d, pret's and reachable %d (targets %d after exclusions), unreachable %d, unused %d; "
          "option A redraws %d" % (tot["ours"], tot["reach"], tot["targets"], tot["unreachable"], tot["unused"],
                                    tot["redrawn"]))
    if draft_dir:
        for o, _, _ in STEAM_OPTIONS:
            d = os.path.join(draft_dir, "mt_ember", "steam_%s" % o)
            os.makedirs(d, exist_ok=True)
            for k in range(4):
                steam(o, k)[0].save(os.path.join(d, "%d.png" % k), bits=4)
        if sheets:
            print("        wrote %s" % steam_sheet(os.path.join(draft_dir, "sheets", "t569_steam.png")))
        json.dump(dict(ticket="T-569", status="DRAFT -- nothing approved (APPROVED is empty)", base=BASE, sets=report,
                       steam=[dict(option=o, title=t, line=l) for o, t, l in STEAM_OPTIONS],
                       later={k: v for k, v in LATER.items()}),
                  open(os.path.join(draft_dir, "draft.json"), "w"), indent=1)
    return report


_PICKED = {}


def picked(ts, option):
    if (ts, option) not in _PICKED:
        town, _, _, _ = census(ts)
        st = [s for s in options(ts) if s[0] == option][0][3]
        new, _ = redraw(town, st)
        _PICKED[(ts, option)] = town, {t: new[t] for t in range(len(new)) if new[t] != town.now[t]}
    return _PICKED[(ts, option)]


def check_engine():
    bad = 0
    for ts, option in APPROVED.items():
        if ts == "steam":
            continue
        town, mine = picked(ts, option)
        later = set(approved_570_tiles().get(ts, {}))      # a tile T-570's approved pick redraws is T-570's now
        miss = sorted(t for t, p in mine.items() if town.disk[t] != p and t not in later)
        print("  engine %-18s pick %s %3d tiles%s" % (ts, option, len(mine), "  DIFFERS" if miss else "  as approved"))
        bad += bool(miss)
    return bad


def owned_tiles():
    """{ts: {tile: pixels}} -- every tile this tool's two approved picks draw: T-569's, then T-570's over them (T-570
    redrew some of T-569's, its ladders drawn whole), so this is the engine as the user picked it"""
    out = {}
    for ts, option in APPROVED.items():
        if ts != "steam":
            out[ts] = dict(picked(ts, option)[1])
    for ts, tt in approved_570_tiles().items():
        out.setdefault(ts, {}).update(tt)
    return out


def check_keep_sets(owned):
    """gbacaves' write keeps the tiles this tool draws (its T569_ISLANDS); each set must be exactly ours, or its write
    would revert a pick (or freeze a tile that is its own). 1 when one is out of step."""
    bad = 0
    keep = getattr(C, "T569_ISLANDS", {})
    drawn = {k.split("/")[0] for k in C.DRAFTED + C.DRAFTED_E2 if not C.LOOKS[k].get("base")}
    for ts in sorted(drawn & (set(owned) | set(keep))):
        mine, theirs = set(owned.get(ts, ())), set(keep.get(ts, ()))
        if mine != theirs:
            print("  !! gbacaves.T569_ISLANDS[%r] is out of step with this tool's tiles: missing %s, extra %s -- its "
                  "--write would revert T-569/T-570" % (ts, sorted(mine - theirs), sorted(theirs - mine)))
            bad += 1
    print("  gbacaves' keep set (T569_ISLANDS) %s" % ("matches this tool's tiles in every cave it draws" if not bad
                                                     else "is OUT OF STEP in %d tilesets" % bad))
    return bad


def main():
    if "--t570" in ARGS:
        return main_570()
    if "--write" in ARGS:
        if "--approved" not in ARGS or not APPROVED:
            print("  --write refused: --write needs --approved, and APPROVED names nothing the user has picked. "
                  "Nothing written.")
            return 0
        if "steam" in APPROVED:
            for k in range(4):
                steam(APPROVED["steam"], k)[0].save(os.path.join(GBA, STEAM % k), bits=4)
            print("  MT. SMOULDER's steam, option %s: 4 frames" % APPROVED["steam"])
        #  T-569's picks, then T-570's over them (2026-11-16: a T-569 write alone put back the ladders T-570 redrew)
        for ts, mine in owned_tiles().items():
            town = town570(ts)
            out = [list(t) for t in town.disk]
            for t, p in mine.items():
                out[t] = list(p)
            if out == town.disk:
                print("  %s: already drawn, nothing to write" % ts)
                continue
            L.save_tiles(town, out, os.path.join(town.dir, "tiles.png"))
            print("  wrote %s: %d tiles (T-569 %s, T-570 %s)" % (ts, len(mine), APPROVED.get(ts), APPROVED_570))
        return 0
    for flag in ("--sheets", "--draft"):
        if flag in ARGS:
            i = ARGS.index(flag)
            d = ARGS[i + 1] if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--") else DRAFT_DEFAULT
            os.makedirs(os.path.join(d, "sheets"), exist_ok=True)
            run(d, sheets=flag == "--sheets")
            return 0
    run(None)
    bad = check_engine()
    print("  the engine %s" % ("matches every approved pick (none yet)" if not bad else
                               "DIFFERS from %d approved picks" % bad))
    bad += check_keep_sets(owned_tiles())
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

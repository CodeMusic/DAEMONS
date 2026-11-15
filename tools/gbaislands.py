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
                                                      #   tiles.png; a second write is a no-op. EMPTY until picked.

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
APPROVED = {ts: "A" for ts, _ in SETS if ts != "rock_tunnel"}
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


def picked(ts, option):
    town, _, _, _ = census(ts)
    st = [s for s in options(ts) if s[0] == option][0][3]
    new, _ = redraw(town, st)
    return town, {t: new[t] for t in range(len(new)) if new[t] != town.now[t]}


def check_engine():
    bad = 0
    for ts, option in APPROVED.items():
        if ts == "steam":
            continue
        town, mine = picked(ts, option)
        miss = sorted(t for t, p in mine.items() if town.disk[t] != p)
        print("  engine %-18s pick %s %3d tiles%s" % (ts, option, len(mine), "  DIFFERS" if miss else "  as approved"))
        bad += bool(miss)
    return bad


def main():
    if "--write" in ARGS:
        if "--approved" not in ARGS or not APPROVED:
            print("  --write refused: --write needs --approved, and APPROVED names nothing the user has picked. "
                  "Nothing written.")
            return 0
        for ts, option in APPROVED.items():
            if ts == "steam":
                for k in range(4):
                    steam(option, k)[0].save(os.path.join(GBA, STEAM % k), bits=4)
                print("  MT. SMOULDER's steam, option %s: 4 frames" % option)
                continue
            town, mine = picked(ts, option)
            out = [list(t) for t in town.disk]
            for t, p in mine.items():
                out[t] = list(p)
            if out == town.disk:
                print("  %s: already drawn, nothing to write" % ts)
                continue
            L.save_tiles(town, out, os.path.join(town.dir, "tiles.png"))
            print("  wrote %s (option %s): %d tiles" % (ts, option, len(mine)))
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
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

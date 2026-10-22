#!/usr/bin/env python3
"""The general ground: the General tileset's last vanilla tiles, re-surfaced in our own hand (T-438 batch C).

    python3 tools/gbageneral.py                    # report: every General tile still vanilla and still drawn, by
                                                   #   group, with its blocks, how many maps draw it and where first
    python3 tools/gbageneral.py --draft [DIR]      # the drawn tiles as a full tiles.png (and the two water-edge
                                                   #   animation strips) in DIR (gfx/drafts/t438/general/), groups.json
                                                   #   beside them, the seam measure, and the contact sheets
                                                   #   (--sheets DIR puts the sheets elsewhere)
    python3 tools/gbageneral.py --write --approved # into the engine -- NOT YET: batch C is a draft until the user
                                                   #   has seen the sheets; without --approved --write refuses

WHAT IS LEFT. The census (T-438) found 428 of General's 640 tiles still pixel-identical to pret's and drawn by some
map. 56 of them sit in 416..481, which the water animations overwrite in VRAM every few frames (engine.md trap 39),
so what the screen shows there is the animation strip, not tiles.png -- they are drawn here in the strips. Six are a
single flat colour (the grass under everything, the sand under every path, two waters, two walls): there is nothing
in them to redraw, and they are listed and left. The other 366 are the ground a player crosses in every route:
cliffs and mountain rock, ledges, sand and dirt, paving, plants, fences, signs, the house kit and the water's edges.

WHAT CHANGES, AND WHAT CANNOT. Nothing but pixels inside tiles. Every block keeps its tiles, its flips, its palette
rows, its layers and its behaviour (T-125: zero collision change), so no map, no connection and no seam between two
maps' tilesets moves (engine.md trap 14; gbaseams.py reports the same before and after). Every tile keeps its
FOOTPRINT: a pixel that was transparent stays transparent, and a pixel on the line where one material meets another
-- rock against grass, sand against its halo, a post against the lawn -- keeps vanilla's index exactly. So every
outline, every silhouette and every edge a neighbouring tile meets is where it was, and what changes is the SURFACE
inside each material.

HOW A SURFACE IS REDRAWN. Each palette row is read as MATERIALS -- in row 1, the rock browns 9..13, the rock's own
outline 14, the greys, the grass -- and each material as a RAMP, dark to light. A pixel's place on its ramp is its
TONE. Vanilla's tone carries two things at once: the light (a lit top, a shaded face) and vanilla's texture (the
diagonal scales on every Kanto mountain, the scattered specks in its sand). The light is kept by averaging the tone
over the pixel's own material in its 3x3 neighbourhood; the texture goes with the averaging; and OUR texture is laid
on top, then the result is rounded back onto the ramp, never more than one step past the lightest or darkest tone
vanilla used in that tile. Every texture is drawn on an 8x8 torus -- the left column continues the right, the top the
bottom -- so a tile meets its neighbour seamlessly whatever the neighbour is, as long as both are textured the same.

THE TEXTURES (all DRAFT, for the user's eye):

    cliffs, ledges   WEATHERED ROCK in place of vanilla's diagonal scales: irregular slabs parted by wandering
                     cracks, each lit along its lower lip, where the light falls; tall split blocks down the shaded
                     faces. Drawn on a 16x16 torus placed by the tile's quarter of its block (every rock tile sits in
                     one quarter, unflipped), and the light read over the whole block, so a mountain's fill is one
                     surface rather than a grid
    sand             WIND RIPPLES: two short dashes a tile, each with a lit grain above it, for vanilla's dot scatter
    dirt             PEBBLES: three small stones a tile, lit above and shaded below
    paving           COBBLES: four-pixel setts in staggered courses, mortar between, each lit at its top left
    plants           on the light grass, gbagrass.py's sprig, a small V of two blades, twice a tile. The round
                     bush, the hedge and the last conifer pieces are MOTIFS, not surfaces: a leaf texture laid over
                     them read as striped melons, so they wait for a drawing of their own (as gbatrees.py's tree)
    fences, signs    WOOD GRAIN on the brown posts and boards. The metal posts are left: re-surfacing a post two
                     pixels wide changes nothing a player sees, and a new fence is a design, not a texture
    the house kit    SHINGLES on the blue house's roof, where its indices allow it. The blue house is General's
                     own house, and its roof tiles are drawn far more in SAFFRON's and CERULEAN's rows (11, 10) than
                     in General's row 3 -- and in four of them the roof's blues fall in a different order in those
                     rows, so those four are left. The walls, windows, doors and the town pieces General lends to
                     CELADON, SEVII and FUCHSIA keep their drawing: a building is a design (gbacivic.py), not a surface
    water edges      the land side only (stone, sand); the water is gbawater.py's, and stays as it is

THE SEAM MEASURE (--draft). Every pair of blocks some map places side by side, and every 8x8 joint inside a
block: a pixel pair across a joint is a SEAM when its jump in lightness exceeds, by 30, the larger jump one pixel
either side of it -- an edge the surface does not explain. Reported as opened and closed against today's tiles.

A TILE DRAWN IN MORE THAN ONE ROW. 56 of these tiles are drawn mostly by town tilesets in the towns' own rows (10..12) as
well as General's. A texture only moves a pixel along its material's ramp, so it is applied to a material only where
that material's indices fall in the same light-to-dark order in EVERY row that draws the tile; where they do not, the
material is left exactly as it was, and the report lists it.

PALETTES. None change. Every new pixel is an index the tile's material already had in the row that draws it. (The
pink-brown of Kanto's rock is still vanilla's colour, in row 1's 9..14; recolouring it is a palette change every
cliff, ledge, rock rim and wooden post would take together, and is offered to the user as a question, not made here.)
"""
import collections, colorsys, glob, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import read_pal
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
G = "data/tilesets/primary/general"
PD = os.path.join(GBA, G)
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t438", "general")

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

ANIMS = [("water_current_landwatersedge", 416, 48), ("sandwatersedge", 464, 18)]     # src/tileset_anims.c
ANIM_TILES = {s + k for _, s, n in ANIMS for k in range(n)} | set(range(508, 512))   # 508..511: the flower (ours)
FRAMES = 8

# the order a player meets the world (T-438's census): the first map a tile is seen on
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
VAN = tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, G + "/tiles.png", binary=True))))
PALS = [read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(16)]
VPALS = [jasc_bytes(daemonslib.upstream(GBA, G + "/palettes/%02d.pal" % n, binary=True)) for n in range(7)]

HDR = open(os.path.join(GBA, "src/data/tilesets/headers.h")).read()
GFX = open(os.path.join(GBA, "src/data/tilesets/graphics.h")).read()
MTS = open(os.path.join(GBA, "src/data/tilesets/metatiles.h")).read()


def tileset_dirs(symbol):
    """(metatiles dir, graphics dir) of a tileset: SilphCo draws with Condominiums' graphics (reviewsheet.gdir)."""
    body = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % re.escape(symbol), HDR, re.S)
    if not body:
        return None, None
    m = re.search(r"\.metatiles = (\w+)", body.group(1))
    t = re.search(r"\.tiles = (\w+)", body.group(1))
    md = m and re.search(r"%s\[\] = INCBIN_U16\(\"(data/tilesets/[^\"]+)/metatiles\.bin" % re.escape(m.group(1)), MTS)
    td = t and re.search(r"%s\[\] = INCBIN_U32\(\"(data/tilesets/[^\"]+)/tiles\." % re.escape(t.group(1)), GFX)
    return (md and md.group(1)), (td and td.group(1))


_SEC = {}


def secondary(symbol):
    """metatiles, tiles and rows 7..12 of a secondary tileset, by its symbol"""
    if symbol not in _SEC:
        md, td = tileset_dirs(symbol)
        if not md or not os.path.exists(os.path.join(GBA, md, "metatiles.bin")):
            _SEC[symbol] = None
        else:
            gd = os.path.join(GBA, td or md)
            pals = [read_pal(os.path.join(gd, "palettes/%02d.pal" % n)) for n in range(16)]
            _SEC[symbol] = {"name": os.path.basename(md), "mt": open(os.path.join(GBA, md, "metatiles.bin"), "rb").read(),
                            "tiles": Image.open(os.path.join(gd, "tiles.png")), "pals": pals}
    return _SEC[symbol]


GMT = open(os.path.join(PD, "metatiles.bin"), "rb").read()
GAT = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
MB = {int(v, 16): k[3:] for k, v in re.findall(r"#define (MB_\w+) (0x[0-9A-Fa-f]+)",
                                               open(os.path.join(GBA, "include/constants/metatile_behaviors.h")).read())}


def entries(buf, i):
    return struct.unpack_from("<8H", buf, i * 16)


def behaviour(i):
    return MB.get(struct.unpack_from("<I", GAT, i * 4)[0] & 0x1FF, "?")


def scan():
    """every layout on General: which General tiles it draws, through which block, in which row, on which maps"""
    layouts = [l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if "id" in l]
    maps_of, rank = collections.defaultdict(list), {}
    for mj in glob.glob(os.path.join(GBA, "data/maps/*/map.json")):
        d = json.load(open(mj))
        n = os.path.basename(os.path.dirname(mj))
        maps_of[d.get("layout")].append(n)
        outdoor = d.get("map_type") in ("MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE", "MAP_TYPE_OCEAN_ROUTE")
        rank[n] = (RANK.get(d.get("region_map_section"), 999), 0 if outdoor else 1, n)
    use = collections.defaultdict(lambda: {"draws": 0, "maps": set(), "rows": collections.Counter(),
                                           "blocks": collections.Counter(), "beh": collections.Counter(),
                                           "quads": collections.Counter()})
    mt_seen = collections.Counter()
    nlay = 0
    for l in layouts:
        if l.get("primary_tileset") != "gTileset_General":
            continue
        sec = secondary(l.get("secondary_tileset"))
        bp = os.path.join(GBA, l.get("blockdata_filepath", ""))
        if sec is None or not os.path.exists(bp):
            continue
        nlay += 1
        data = open(bp, "rb").read()
        maps = maps_of.get(l["id"], [])
        cells = collections.Counter(struct.unpack_from("<H", data, k)[0] & 0x3FF for k in range(0, len(data) - 1, 2))
        for mid, n in cells.items():
            buf, i, ts = (GMT, mid, "general") if mid < 640 else (sec["mt"], mid - 640, sec["name"])
            if (i + 1) * 16 > len(buf):
                continue
            mt_seen[(ts, mid, l.get("secondary_tileset"))] += n
            for q8, e in enumerate(entries(buf, i)):
                t = e & 0x3FF
                if t >= 640 or not any(CUR[t]):
                    continue
                u = use[t]
                u["quads"][(q8 % 4, (e >> 10) & 3)] += n
                u["draws"] += n
                u["maps"].update(maps)
                row = e >> 12
                u["rows"][("general" if row < 7 else l.get("secondary_tileset"), row)] += n
                u["blocks"][(ts, mid)] += n
                if mid < 640:
                    u["beh"][behaviour(mid)] += n
    for t, u in use.items():
        u["maps"] = sorted(u["maps"], key=lambda m: rank.get(m, (999, 1, m)))
    return use, nlay, mt_seen


# ================================================================== materials
#  each primary row as materials, each a set of indices; a ramp is a material's indices, dark to light
ROW_MATERIALS = {
    0: {"leaf": {1, 2, 3, 4}, "trunk": {5, 6}, "grass": {8, 12, 13, 14, 15}, "bloom": {9, 10, 11}},
    1: {"grey": {1, 2, 3, 4, 6, 8}, "ink": {5}, "green": {7}, "rock": {9, 10, 11, 12, 13}, "rockline": {14},
        "grass": {15}},
    2: {"grey": {1, 2, 3, 4, 5, 6, 7}, "teal": {8, 9, 15}, "red": {10, 11, 12, 13, 14}},
    3: {"grey": {1, 2, 3, 4, 5, 6, 7}, "sand": {8, 9}, "water": {10, 11, 12, 13, 14}, "grass": {15}},
    4: {"water": {1, 2, 3, 4, 5, 6, 7, 12}, "grey": {8, 9, 10, 11}, "sand": {13, 14, 15}},
    5: {"grey": {1, 2, 3, 4, 5}, "dirt": {6, 7, 8, 9}, "sand": {10, 11, 12}, "halo": {13, 14, 15}},
    6: {"water": set(range(1, 16))},
}


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def families_of(pal, row):
    """index -> material name, for one palette row; town rows (7..12) are read by hue"""
    if row in ROW_MATERIALS:
        return {i: m for m, s in ROW_MATERIALS[row].items() for i in s}
    out = {}
    for i in range(1, 16):
        r, g, b = (v / 255.0 for v in pal[i])
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        out[i] = "grey" if s < 0.18 or l > 0.93 else "hue%d" % (int(h * 12 + 0.5) % 12)
    return out


def palette(key):
    ts, row = key
    return PALS[row] if ts == "general" else secondary(ts)["pals"][row]


# ================================================================== the textures (8x8 tori, in tone steps)
def _voronoi(seeds, sy):
    """a 16x16 torus of slabs: '=' a crack where two slabs meet, '+' the lit lip just under it, '-' the shade over it"""
    def near(x, y):
        ds = sorted(min((x - a + dx) ** 2 for dx in (-16, 0, 16)) + sy * min((y - b + dy) ** 2 for dy in (-16, 0, 16))
                    for a, b in seeds)
        return ds[1] ** 0.5 - ds[0] ** 0.5
    crack = [[near(x + 0.5, y + 0.5) < 0.6 for x in range(16)] for y in range(16)]
    out = []
    for y in range(16):
        row = ""
        for x in range(16):
            if crack[y][x]:
                row += "="
            elif crack[(y - 1) % 16][x] or crack[y][(x - 1) % 16]:
                row += "+"
            elif crack[(y + 1) % 16][x]:
                row += "-"
            else:
                row += "."
        out.append(row)
    return out


ROCK_TOP = _voronoi([(2, 3), (10, 1), (6, 9), (14, 8), (1, 13), (11, 14)], 1.0)    # weathered slabs on the tops
ROCK_FACE = _voronoi([(3, 2), (8, 9), (13, 4), (1, 11), (11, 15)], 0.25)          # tall blocks down the faces
GLYPH = {"+": 0.75, ".": 0.0, "-": -0.6, "=": -1.5}


def t_strata(x, y, tile, base=None, top=None):
    """weathered rock: irregular slabs where the light falls, tall split blocks down the shaded faces (16x16 tori,
    placed by the tile's quarter of its block; 8x8 where a tile sits in more than one quarter)"""
    pat = ROCK_TOP if top else ROCK_FACE
    lift = 0.3 if top else 0.0                          # the tops a little brighter, as vanilla's are
    ox, oy = QUARTER.get(tile, (None, None))
    if ox is None:
        return lift + (GLYPH[pat[y][x]] if pat[y][x] != "=" or (x, y) in ((3, 3), (3, 4), (4, 4)) else -0.3)
    return lift + GLYPH[pat[oy + y][ox + x]]


QUARTER = {}       # tile -> (x, y) of its quarter of a 16x16 torus, when every block puts it in the same quarter
BLOCK_OF = {}      # such a tile -> the 16x16 (x, y, index) of the layer it sits in, in the block that draws it most


def block_layer(buf, i, t, cur):
    e = entries(buf, i)
    for layer in (0, 1):
        quad = e[layer * 4:layer * 4 + 4]
        if any(v & 0x3FF == t for v in quad):
            row = next(v >> 12 for v in quad if v & 0x3FF == t)
            out = []
            for q, v in enumerate(quad):
                u = v & 0x3FF
                if u >= 640 or v >> 12 != row or v & 0xC00:
                    continue
                for k, c in enumerate(cur[u]):
                    if c:
                        out.append(((q % 2) * 8 + k % 8, (q // 2) * 8 + k // 8, c))
            return out
    return None


def t_ripple(x, y, tile, base=None, top=None):
    """wind ripples: two short dashes, each with a lit grain over its middle"""
    dash = {(1, 2): -1.2, (2, 2): -1.2, (3, 2): -0.7, (5, 6): -1.2, (6, 6): -1.2, (7, 6): -0.7, (6, 1): -0.9,
            (2, 5): -0.9}
    lit = {(2, 1): 0.6, (6, 5): 0.6}
    return dash.get((x, y), lit.get((x, y), 0.0))


def t_pebble(x, y, tile, base=None, top=None):
    """three small stones, lit above and shaded below"""
    d = 0.0
    for px, py in ((1, 1), (5, 3), (2, 5)):
        dx, dy = (x - px) % 8, (y - py) % 8
        if (dx, dy) == (0, 0):
            d += 0.9
        elif (dx, dy) in ((1, 0), (0, 1)):
            d += 0.0
        elif (dx, dy) == (1, 1):
            d -= 1.1
    return d


def t_cobble(x, y, tile, base=None, top=None):
    """four-pixel setts in staggered courses: mortar between, each lit at its top left"""
    course = (y // 4) % 2
    xs, ys = (x + 2 * course) % 4, y % 4
    if xs == 3 or ys == 3:
        return -1.4
    if xs == 0 and ys == 0:
        return 0.9
    if xs == 0 or ys == 0:
        return 0.35
    return 0.0


def t_leaf(x, y, tile, base=None, top=None):
    """leaf clusters, lit on top, shaded under (gbatrees.py's crown, at tile scale)"""
    best = None
    for cx, cy in ((1, 1), (5, 2), (3, 5), (7, 6)):
        dx = (x - cx + 4) % 8 - 4
        dy = (y - cy + 4) % 8 - 4
        if best is None or dx * dx + dy * dy < best[0]:
            best = (dx * dx + dy * dy, dx, dy)
    _, dx, dy = best
    if dx + dy <= -1:
        return 0.8
    if dx + dy >= 2:
        return -1.0
    return 0.0


def t_sprig(x, y, tile, base=None, top=None):
    """gbagrass.py's sprig, a small V of two blades, one lit -- chosen by the tile's number, a pixel inside it"""
    h = (tile * 2654435761) & 0xFFFFFFFF
    d = {}
    for k in range(2):                               # two a tile here: the light grass had vanilla's dither to lose
        sx, sy = (h >> (9 + 8 * k)) % 4 + 2 - 2 * k % 4, (h >> (13 + 8 * k)) % 4 + 2
        sx = max(1, min(6, sx))
        d.update({(sx - 1, sy - 1): 1.0, (sx + 1, sy - 1): -1.0, (sx, sy): -2.0})
    return d.get((x, y), 0.0)


def t_grain(x, y, tile, base=None, top=None):
    """wood: upright grain every third pixel, a knot"""
    d = -0.7 if x % 3 == 2 else 0.0
    if (x, y) in ((1, 4), (4, 1)):
        d -= 0.8
    return d


def t_shingle(x, y, tile, base=None, top=None):
    """roof shingles: courses three deep, a lit lip, butt joints staggered"""
    course = (y // 4) % 2
    r = y % 4
    if r == 3:
        return -1.2
    if r == 0:
        return 0.6
    if (x + 4 * course) % 8 == 0:
        return -0.9
    return 0.0


def t_smooth(x, y, tile, base=None, top=None):
    return 0.0


LOCAL = {"leaf": 0.85, "grain": 0.6, "shingle": 0.5}
TEX = {"strata": t_strata, "ripple": t_ripple, "pebble": t_pebble, "cobble": t_cobble, "leaf": t_leaf,
       "sprig": t_sprig, "grain": t_grain, "shingle": t_shingle, "smooth": t_smooth}

# ================================================================== the groups
#  tile -> group, from the census and its contact sheets; what is not named here falls to its dominant material
FENCES = {14, 15, 30, 31, 47, 46, 62, 63, 239, 308, 309, 324, 325, 340, 356, 357, 499, 500}
SIGNS = {364, 365, 380, 381, 366, 367, 382, 383}
ROOFS = set(range(296, 300)) | set(range(312, 316)) | set(range(328, 332)) | set(range(344, 348))
HOUSE = ROOFS | {192, 193, 194, 195, 197, 198, 199, 212, 213, 214, 215, 228, 229, 230, 231, 232, 233, 244, 245, 246,
                 247, 248, 249, 260, 261, 263, 269, 276, 277, 278, 279, 285, 287, 292, 293, 334, 335, 341, 350, 351,
                 360, 362, 363, 376, 377, 378, 379, 388, 389, 390, 391, 400, 402, 403, 404, 405, 406, 407, 496, 497,
                 516, 517, 519, 520, 521, 522, 523, 524, 525, 526, 527, 532, 533, 537, 538, 539, 540, 541, 542, 543,
                 548, 549, 552, 553, 554, 555, 556, 557, 558, 564, 565, 566, 568, 569, 570, 571, 573, 574, 580, 581,
                 582, 583, 584, 585, 586, 587, 596, 598, 599, 600, 601, 602, 603, 611, 612, 613, 614, 627, 628, 629,
                 630}
PAVING = {51, 52, 512, 513, 514, 515, 528, 529, 530, 531, 560, 561, 562, 563, 615, 616, 619, 624, 625, 631, 632, 633,
          634, 635, 306, 307, 322, 323, 338, 355, 576, 577, 578, 579, 592, 593, 594, 595, 608, 609, 610, 294, 295}
PLANTS = {2, 3, 16, 18, 48, 49, 11, 12, 13, 28, 29, 27, 43, 90, 91, 44, 45, 92, 93, 53, 60, 59, 75, 393, 394, 409, 410}
STAIRS = {294, 295}
WATER = {78, 95, 173, 174, 189, 190, 191, 310, 311, 326, 342, 358, 359, 505, 506, 617, 618}

GROUPS = [   # key, title, material -> texture
    ("cliffs", "cliffs and mountain rock", {"rock": "strata", "hue1": "strata", "hue0": "strata", "dirt": "strata"}),
    ("ledges", "ledges", {"rock": "strata", "dirt": "strata"}),
    ("sand", "sand, beach and dirt", {"sand": "ripple", "dirt": "pebble"}),
    ("paving", "paving, stairs and paths", {"dirt": "cobble", "grey": "cobble", "sand": "ripple", "hue1": "cobble",
                                           "hue2": "cobble"}),
    ("plants", "grass, bushes, hedges and the last conifer pieces", {"grass": "sprig"}),
    ("fences", "fences and posts", {"rock": "grain"}),
    ("signs", "signs", {"rock": "grain"}),
    ("house", "the house kit (the blue house: every town's house)", {}),
    ("water", "water's edges (the land side)", {"rock": "strata", "sand": "ripple"}),
    ("anim", "water's edges in the animation strips (the land side)", {"rock": "strata", "sand": "ripple"}),
    ("flat", "flat fills: nothing to redraw", {}),
]
GROUP_TEX = {k: v for k, _, v in GROUPS}
TITLE = {k: t for k, t, _ in GROUPS}


def group_of(t, u):
    if t in ANIM_TILES:
        return "anim"
    if len(set(CUR[t])) == 1:
        return "flat"
    for name, s in (("fences", FENCES), ("signs", SIGNS), ("house", HOUSE), ("paving", PAVING),
                    ("plants", PLANTS), ("water", WATER)):
        if t in s:
            return name
    key = u["rows"].most_common(1)[0][0]
    fam = families_of(palette(key), key[1])
    count = collections.Counter(fam.get(v) for v in CUR[t] if v)
    top = count.most_common(1)[0][0]
    if any(b.startswith("JUMP") for b in u["beh"]) and top in ("rock", "rockline"):
        return "ledges"          # the lip itself; the sand and grass a ledge block also draws stay with their own
    return {"rock": "cliffs", "rockline": "cliffs", "sand": "sand", "dirt": "sand", "halo": "sand",
            "leaf": "plants", "grass": "plants", "water": "water"}.get(top, "house")


# ================================================================== drawing one tile
def light_plane(pts):
    """the light across a tile, as a plane through its tones (least squares): vanilla's tile-sized scales average
    out of it, and the plane of one tile runs on into its neighbour's"""
    n = len(pts)
    if n < 6:
        mean = sum(p[2] for p in pts) / max(n, 1)
        return lambda x, y: mean
    sx = sum(p[0] for p in pts) / n
    sy = sum(p[1] for p in pts) / n
    st = sum(p[2] for p in pts) / n
    a11 = sum((p[0] - sx) ** 2 for p in pts)
    a22 = sum((p[1] - sy) ** 2 for p in pts)
    a12 = sum((p[0] - sx) * (p[1] - sy) for p in pts)
    b1 = sum((p[0] - sx) * (p[2] - st) for p in pts)
    b2 = sum((p[1] - sy) * (p[2] - st) for p in pts)
    det = a11 * a22 - a12 * a12
    if abs(det) < 1e-6:
        return lambda x, y: st
    gx = (b1 * a22 - b2 * a12) / det
    gy = (a11 * b2 - a12 * b1) / det
    return lambda x, y: st + gx * (x - sx) + gy * (y - sy)


def redraw(t, px, rows, group, texmap=None):
    """px: 64 indices. rows: Counter of (tileset, row) that draw it. Returns (new 64, notes)."""
    texmap = GROUP_TEX[group] if texmap is None else texmap
    if group == "house":
        texmap = {"*": "shingle"} if t in ROOFS else {}
    if t in STAIRS:
        return list(px), ["stairs: their treads are the drawing, and are kept"]
    if not texmap:
        return list(px), []
    key = rows.most_common(1)[0][0]
    pal = palette(key)
    fam = families_of(pal, key[1])
    notes = []
    out = list(px)
    present = collections.defaultdict(set)
    for v in px:
        if v:
            present[fam.get(v)].add(v)
    for m, idxs in present.items():
        tex = texmap.get(m, None if m in ("grey", "ink", "grass") else texmap.get("*"))
        if tex is None:
            continue
        # the ramp: the material's indices in this row, dark to light; one step past what the tile used, either way
        full = sorted((i for i in range(1, 16) if fam.get(i) == m), key=lambda i: lum(pal[i]))
        used = sorted(idxs, key=lambda i: lum(pal[i]))
        lo, hi = full.index(used[0]), full.index(used[-1])
        ramp = full[max(0, lo - 1):hi + 2]
        # every other row that draws this tile must order these indices the same way, or the material is left
        ok = True
        for k in rows:
            if k == key:
                continue
            p2 = palette(k)
            if sorted(ramp, key=lambda i: lum(p2[i])) != ramp:
                if sorted(used, key=lambda i: lum(p2[i])) == used:
                    ramp = used
                else:
                    ok = False
                    break
        if not ok:
            notes.append("%s left: its indices do not keep their order in every row that draws it" % m)
            continue
        if len(ramp) < 2:
            continue
        tone = {v: k for k, v in enumerate(ramp)}
        lo_t = min(tone[v] for v in idxs if v in tone)
        hi_t = max(tone[v] for v in idxs if v in tone)
        lo_t, hi_t = max(0, lo_t - 1), min(len(ramp) - 1, hi_t + 1)
        f = TEX[tex]
        mid_lum = (lum(pal[full[0]]) + lum(pal[full[-1]])) / 2.0
        pts = [(x, y, tone[px[y * 8 + x]]) for y in range(8) for x in range(8)
               if px[y * 8 + x] in tone and fam.get(px[y * 8 + x]) == m]
        if t in BLOCK_OF:              # the light read over the whole block, so the four quarters share one plane
            ox, oy = QUARTER[t]
            pts = [(x - ox, y - oy, tone[v]) for x, y, v in BLOCK_OF[t] if v in tone and fam.get(v) == m]
        if len(pts) >= 0.9 * 256:      # a block that is all one material tiles with itself: its light is level
            mean = sum(p[2] for p in pts) / len(pts)
            plane = lambda x, y: mean
        else:
            plane = light_plane(pts)
        for y in range(8):
            for x in range(8):
                v = px[y * 8 + x]
                if not v or fam.get(v) != m or v not in tone:
                    continue
                edge = False
                acc = wsum = 0.0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        xx, yy = x + dx, y + dy
                        if not (0 <= xx < 8 and 0 <= yy < 8):
                            continue
                        w = px[yy * 8 + xx]
                        same = w and fam.get(w) == m and w in tone
                        if not same and abs(dx) + abs(dy) == 1:
                            edge = True
                        if same:
                            k = 2.0 if dx == dy == 0 else 1.0
                            acc += k * tone[w]
                            wsum += k
                if edge:
                    continue
                near_edge = any(0 <= x + dx < 8 and 0 <= y + dy < 8 and (not px[(y + dy) * 8 + x + dx] or
                                    fam.get(px[(y + dy) * 8 + x + dx]) != m)
                                    for dy in (-2, -1, 0, 1, 2) for dx in (-2, -1, 0, 1, 2))
                k = 0.6 if near_edge else 0.15                 # the rim keeps vanilla's modelling; the field, its light
                k = max(k, LOCAL.get(tex, 0.0))                # a bush keeps its roundness, a post its bevel
                b = (1 - k) * plane(x, y) + k * acc / wsum
                lit = lum(pal[ramp[max(0, min(len(ramp) - 1, int(round(b))))]]) >= mid_lum   # the same test in every tile
                n = int(round(b + f(x, y, t, b, lit)))
                out[y * 8 + x] = ramp[max(lo_t, min(hi_t, n))]
    return out, notes


# ================================================================== the seam measure
def composite(buf, i, tilesrc, pals_of):
    """16x16 RGB of one block, both layers"""
    e = entries(buf, i)
    o = [[None] * 16 for _ in range(16)]
    for layer in (0, 1):
        for q in range(4):
            v = e[layer * 4 + q]
            t, row = v & 0x3FF, v >> 12
            for yy in range(8):
                for xx in range(8):
                    sx = 7 - xx if v & 0x400 else xx
                    sy = 7 - yy if v & 0x800 else yy
                    c = tilesrc(t, sx, sy)
                    if c == 0 and layer:
                        continue
                    o[(q // 2) * 8 + yy][(q % 2) * 8 + xx] = pals_of(row)[c]
    return o


def seam_measure(new_tiles, mt_seen):
    """for every pair of blocks that sit side by side on some map, and every 8x8 joint inside a block: the pixel pairs
    across a joint that are near in colour today and far apart in the draft -- a seam the draft would open"""
    layouts = [l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if "id" in l]
    cache = {}

    def comp(mid, secsym, draft):
        k = (mid if mid < 640 else (secsym, mid), draft)
        if k not in cache:
            sec = secondary(secsym)
            tl = new_tiles if draft else CUR
            stp = sec["tiles"].load()
            sw, sh = sec["tiles"].size

            def src(t, x, y):
                if t < 640:
                    return tl[t][y * 8 + x]
                j = t - 640
                yy = (j // (sw // 8)) * 8 + y
                return stp[(j % (sw // 8)) * 8 + x, yy] & 15 if yy < sh else 0
            pals_of = lambda r: PALS[r] if r < 7 else sec["pals"][r]
            buf, i = (GMT, mid) if mid < 640 else (sec["mt"], mid - 640)
            cache[k] = composite(buf, i, src, pals_of) if (i + 1) * 16 <= len(buf) else None
        return cache[k]

    changed = {t for t in range(640) if new_tiles[t] != CUR[t]}
    touches = lambda buf, i: any((e & 0x3FF) in changed for e in entries(buf, i))
    pairs = collections.Counter()
    for l in layouts:
        if l.get("primary_tileset") != "gTileset_General":
            continue
        sec = secondary(l.get("secondary_tileset"))
        bp = os.path.join(GBA, l.get("blockdata_filepath", ""))
        if sec is None or not os.path.exists(bp):
            continue
        W, H = l["width"], l["height"]
        d = open(bp, "rb").read()
        grid = [struct.unpack_from("<H", d, k * 2)[0] & 0x3FF for k in range(W * H)]
        hit = {}

        def hits(m):
            if m not in hit:
                buf, i = (GMT, m) if m < 640 else (sec["mt"], m - 640)
                hit[m] = (i + 1) * 16 <= len(buf) and touches(buf, i)
            return hit[m]
        for y in range(H):
            for x in range(W):
                a = grid[y * W + x]
                if x + 1 < W and (hits(a) or hits(grid[y * W + x + 1])):
                    pairs[(a, grid[y * W + x + 1], "h", l["secondary_tileset"])] += 1
                if y + 1 < H and (hits(a) or hits(grid[(y + 1) * W + x])):
                    pairs[(a, grid[(y + 1) * W + x], "v", l["secondary_tileset"])] += 1
                if hits(a):
                    pairs[(a, a, "i", l["secondary_tileset"])] += 1
    opened = closed = examined = 0
    worst = collections.Counter()

    def d(P, a, Q, b):
        return abs(lum(P[a[0]][a[1]]) - lum(Q[b[0]][b[1]]))

    def seam(A, B, a0, a1, b0, b1):
        """a jump across the joint (a0|b0) bigger by 30 than the jumps one pixel either side of it (a1|a0, b0|b1):
        an edge the surface itself does not explain"""
        return d(A, a0, B, b0) - max(d(A, a1, A, a0), d(B, b0, B, b1)) > 30
    for (a, b, how, secsym), n in pairs.items():
        ca, cb = comp(a, secsym, False), comp(b, secsym, False)
        da, db = comp(a, secsym, True), comp(b, secsym, True)
        if None in (ca, cb, da, db):
            continue
        if how == "h":
            js = [(ca, cb, da, db, (r, 15), (r, 14), (r, 0), (r, 1)) for r in range(16)]
        elif how == "v":
            js = [(ca, cb, da, db, (15, c), (14, c), (0, c), (1, c)) for c in range(16)]
        else:
            js = [(ca, ca, da, da, (r, 7), (r, 6), (r, 8), (r, 9)) for r in range(16)] + \
                 [(ca, ca, da, da, (7, c), (6, c), (8, c), (9, c)) for c in range(16)]
        for A, B, DA, DB, a0, a1, b0, b1 in js:
            examined += n
            was, now = seam(A, B, a0, a1, b0, b1), seam(DA, DB, a0, a1, b0, b1)
            if now and not was:
                opened += n
                worst[(a, b, how, secsym)] += n
            elif was and not now:
                closed += n
    return {"pairs": len(pairs), "pixel_pairs": examined, "opened": opened, "closed": closed,
            "worst": [("%s %s %s %s" % k, n) for k, n in worst.most_common(12)]}


# ================================================================== the animation strips
def anim_frames(strip):
    return [Image.open(os.path.join(PD, "anim", strip, "%d.png" % f)) for f in range(FRAMES)]


def strip_tile(im, k):
    p = im.load()
    return [p[(k % 2) * 8 + i % 8, (k // 2) * 8 + i // 8] & 15 for i in range(64)]


def put_tile(im, k, px):
    p = im.load()
    for i, v in enumerate(px):
        p[(k % 2) * 8 + i % 8, (k // 2) * 8 + i // 8] = v


_AV = {}


def anim_vanilla(strip, f, k):
    if (strip, f) not in _AV:
        _AV[(strip, f)] = Image.open(io.BytesIO(daemonslib.upstream(GBA, "%s/anim/%s/%d.png" % (G, strip, f), binary=True)))
    return strip_tile(_AV[(strip, f)], k)


# ================================================================== the contact sheets
def font(n):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except OSError:
        return ImageFont.load_default()


def tile_rgb(px, pal, Z):
    im = Image.new("RGB", (8, 8))
    for i, v in enumerate(px):
        im.putpixel((i % 8, i // 8), (60, 60, 66) if v == 0 else pal[v])
    return im.resize((8 * Z, 8 * Z), Image.NEAREST)


_RS = None


def reviewsheet():
    """tools/reviewsheet.py's map renderer, imported with argv swapped round it (engine.md trap 16)"""
    global _RS
    if _RS is None:
        import importlib.util
        argv = sys.argv
        sys.argv = [argv[0]]
        try:
            spec = importlib.util.spec_from_file_location("reviewsheet", os.path.join(ROOT, "tools", "reviewsheet.py"))
            _RS = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_RS)
        finally:
            sys.argv = argv
    return _RS


def render_map(name, draft_png=None):
    """the map as reviewsheet.py draws it -- from tiles.png, or, given draft_png, with General's tiles swapped for it"""
    rs = reviewsheet()
    if draft_png is None:
        return rs.render(rs.layout_of(name))
    real = rs.Image

    class Shim:
        new = staticmethod(real.new)

        @staticmethod
        def open(path, *a, **k):
            if os.path.abspath(path) == os.path.abspath(os.path.join(PD, "tiles.png")):
                return Image.open(draft_png)
            return real.open(path, *a, **k)
    rs.Image = Shim
    try:
        return rs.render(rs.layout_of(name))
    finally:
        rs.Image = real


MAP_CROPS = [   # (map, x0, y0, w, h in cells, what it shows)
    ("Route1", 0, 16, 24, 14, "ROUTE 1: ledges, sand, the paths"),
    ("Route2", 0, 44, 24, 14, "ROUTE 2: ledges and fences"),
    ("Route3", 44, 0, 40, 20, "ROUTE 3: cliffs and mountain rock"),
    ("Route22", 0, 0, 30, 24, "ROUTE 22: cliffs, ledges, a fence and its sign"),
    ("VermilionCity", 0, 0, 30, 30, "VERMILION: the beach, the house kit, the docks"),
    ("CeruleanCity", 6, 4, 30, 24, "CERULEAN: town fences, a sign, paving, the house kit"),
]


def group_sheet(group, items, Z, path):
    """pristine (vanilla palettes) | today (our palettes) | draft, per tile, 4x"""
    F, f2 = font(15), font(11)
    cols = 6
    cw = 3 * 8 * Z + 26
    ch = 8 * Z + 34
    rows = (len(items) + cols - 1) // cols
    W = cols * cw + 16
    im = Image.new("RGB", (W, 64 + rows * ch), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-438 C  %s  (%d tiles)   DRAFT" % (TITLE[group], len(items)), fill=(250, 214, 120), font=F)
    dr.text((8, 28), "each: PRISTINE (pret's palette) | TODAY (our palette, vanilla's pixels) | DRAFT.  "
                     "label: tile, row it is drawn in, maps", fill=(200, 200, 210), font=f2)
    for k, it in enumerate(items):
        t, key, nmaps, new = it["tile"], it["key"], it["nmaps"], it["new"]
        x = 8 + (k % cols) * cw
        y = 52 + (k // cols) * ch
        pal_now = palette(key)
        pal_van = VPALS[key[1]] if key[0] == "general" and key[1] < 7 else pal_now
        dr.text((x, y), "%d  r%d%s  %dm" % (t, key[1], "" if key[0] == "general" else "*", nmaps),
                fill=(230, 230, 230), font=f2)
        for j, (px, pal) in enumerate(((VAN[t] if it.get("van") is None else it["van"], pal_van),
                                       (CUR[t] if it.get("cur") is None else it["cur"], pal_now),
                                       (new, pal_now))):
            im.paste(tile_rgb(px, pal, Z), (x + j * (8 * Z + 4), y + 16))
    im.save(path)
    return path


def map_sheet(crops, draft_png, path):
    F, f2 = font(15), font(12)
    panels = []
    for name, x0, y0, w, h, why in crops:
        a = render_map(name).crop((x0 * 16, y0 * 16, (x0 + w) * 16, (y0 + h) * 16))
        b = render_map(name, draft_png).crop((x0 * 16, y0 * 16, (x0 + w) * 16, (y0 + h) * 16))
        a = a.resize((a.width * 2, a.height * 2), Image.NEAREST)
        b = b.resize((b.width * 2, b.height * 2), Image.NEAREST)
        panels.append((why, a, b))
    W = max(p[1].width * 2 + 24 for p in panels)
    H = sum(p[1].height + 44 for p in panels) + 10
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    y = 6
    for why, a, b in panels:
        dr.text((8, y), why + "   (TODAY | DRAFT, 2x)", fill=(250, 214, 120), font=F)
        im.paste(a, (8, y + 24))
        im.paste(b, (16 + a.width, y + 24))
        y += a.height + 44
    im.save(path)
    return path


# ================================================================== the run
def main():
    if WRITE and "--approved" not in ARGS:
        print("  --write refused: T-438 batch C is a draft until the user has approved its sheets.")
        print("  (When they have: --write --approved writes the drawn tiles into %s/tiles.png and the two water-edge" % G)
        print("   strips into its anim/, overwriting only tiles that are still vanilla.)")
        return 0

    use, nlay, mt_seen = scan()
    for t, u in use.items():
        qs = set(u["quads"])
        if len(qs) == 1 and next(iter(qs))[1] == 0:
            q = next(iter(qs))[0]
            QUARTER[t] = ((q % 2) * 8, (q // 2) * 8)
            gb = [b for b in u["blocks"].most_common() if b[0][0] == "general"]
            bl = gb and block_layer(GMT, gb[0][0][1], t, CUR)
            if bl:
                BLOCK_OF[t] = bl
    drawn = [t for t in range(640) if t in use and any(CUR[t])]
    vanilla = [t for t in drawn if CUR[t] == VAN[t]]
    print("  scanned %d layouts on General; %d of its tiles are drawn, %d of them still vanilla" %
          (nlay, len(drawn), len(vanilla)))

    by_group = collections.defaultdict(list)
    new_tiles = [list(p) for p in CUR]
    all_notes = []
    for t in vanilla:
        u = use[t]
        g = group_of(t, u)
        key = u["rows"].most_common(1)[0][0]
        if g == "anim":
            new = CUR[t]
        else:
            new, notes = redraw(t, CUR[t], u["rows"], g)
            all_notes += ["%d: %s" % (t, n) for n in notes]
            new_tiles[t] = new
        by_group[g].append({"tile": t, "key": key, "nmaps": len(u["maps"]), "first": u["maps"][0] if u["maps"] else None,
                            "maps": u["maps"], "blocks": sorted("%s:%d" % b for b in u["blocks"]), "new": new,
                            "draws": u["draws"]})

    # the animation strips: every frame of every vanilla-drawn tile in them, its land side
    strips = {}
    for strip, first, n in ANIMS:
        frames = [im.copy() for im in anim_frames(strip)]
        for it in by_group.get("anim", []):
            k = it["tile"] - first
            if not 0 <= k < n:
                continue
            for f in range(FRAMES):
                px = strip_tile(frames[f], k)
                if px != anim_vanilla(strip, f, k):
                    continue                     # gbawater.py's, already ours
                new, notes = redraw(it["tile"], px, use[it["tile"]]["rows"], "anim")
                put_tile(frames[f], k, new)
                if f == 0:
                    it["new"] = new
                    it["van"] = px
                    it["cur"] = px
                    new_tiles[it["tile"]] = new
                    all_notes += ["%d: %s" % (it["tile"], x) for x in notes]
        strips[strip] = frames

    order = [k for k, _, _ in GROUPS]
    print("  %-10s %5s %6s %8s  %-28s %s" % ("group", "tiles", "drawn", "maps", "first seen", "what"))
    for g in order:
        items = by_group.get(g, [])
        if not items:
            continue
        nd = sum(1 for it in items if it["new"] != CUR[it["tile"]] or (g == "anim" and it.get("van") and it["new"] != it["van"]))
        maps = set(m for it in items for m in it["maps"])
        firsts = sorted((it for it in items if it["first"]), key=lambda it: -len(it["maps"]))
        print("  %-10s %5d %6d %8d  %-28s %s" % (g, len(items), nd, len(maps), firsts[0]["first"] if firsts else "-",
                                                 TITLE[g]))
    print("  %d tiles in all; %d notes:" % (sum(len(v) for v in by_group.values()), len(all_notes)))
    for n in all_notes:
        print("    " + n)

    if WRITE:
        cur = Image.open(os.path.join(PD, "tiles.png"))
        now = tiles_of(cur)
        cp = cur.load()
        n = 0
        for t in range(640):
            if new_tiles[t] != CUR[t] and now[t] == VAN[t]:
                for i, v in enumerate(new_tiles[t]):
                    cp[(t % 16) * 8 + i % 8, (t // 16) * 8 + i // 8] = v
                n += 1
        cur.save(os.path.join(PD, "tiles.png"))
        for strip, frames in strips.items():
            for f, im in enumerate(frames):
                im.save(os.path.join(PD, "anim", strip, "%d.png" % f))
        print("  written: %d tiles into tiles.png, and the two strips" % n)

    if not DRAFT:
        return 0

    os.makedirs(DRAFT, exist_ok=True)
    os.makedirs(SHEETS, exist_ok=True)
    out = CUR_IM.copy()
    p = out.load()
    for t in range(640):
        if new_tiles[t] != CUR[t]:
            for i, v in enumerate(new_tiles[t]):
                p[(t % 16) * 8 + i % 8, (t // 16) * 8 + i // 8] = v
    draft_png = os.path.join(DRAFT, "tiles.png")
    out.save(draft_png)
    for strip, frames in strips.items():
        d = os.path.join(DRAFT, "anim", strip)
        os.makedirs(d, exist_ok=True)
        for f, im in enumerate(frames):
            im.save(os.path.join(d, "%d.png" % f))
    print("  measuring seams over every block pair the maps place ...")
    seams = seam_measure(new_tiles, mt_seen)
    print("  seams: %d block pairs and joints, %d pixel pairs across them; %d opened by the draft, %d closed" %
          (seams["pairs"], seams["pixel_pairs"], seams["opened"], seams["closed"]))
    for k, n in seams["worst"]:
        print("    %-40s %d" % (k, n))
    groups = {g: [{k: it[k] for k in ("tile", "nmaps", "first", "blocks", "draws")} | {"row": list(it["key"]),
                   "changed": it["new"] != (it.get("van") or VAN[it["tile"]])} for it in by_group.get(g, [])]
              for g in order}
    json.dump({"groups": groups, "titles": TITLE, "notes": all_notes, "seams": seams}, open(os.path.join(DRAFT, "groups.json"), "w"),
              indent=1, sort_keys=True)
    names = []
    for g in order:
        items = by_group.get(g, [])
        if not items or g == "flat":
            continue
        for part in range(0, len(items), 60):
            names.append(group_sheet(g, items[part:part + 60], 4,
                                     os.path.join(SHEETS, "t438c_ground_%s%s.png" % (g, "" if part == 0 else "_%d" % (part // 60 + 1)))))
    names.append(map_sheet(MAP_CROPS[:3], draft_png, os.path.join(SHEETS, "t438c_ground_maps_1.png")))
    names.append(map_sheet(MAP_CROPS[3:], draft_png, os.path.join(SHEETS, "t438c_ground_maps_2.png")))
    print("  drafts in %s; sheets:\n    %s" % (DRAFT, "\n    ".join(names)))

    return 0


if __name__ == "__main__":
    sys.exit(main())

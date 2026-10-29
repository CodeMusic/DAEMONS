#!/usr/bin/env python3
"""The general ground: the General tileset's last vanilla tiles, re-surfaced in our own hand (T-438 batch C).

    python3 tools/gbageneral.py                    # report: every General tile still vanilla and still drawn, by
                                                   #   group, with its blocks, how many maps draw it and where first
    python3 tools/gbageneral.py --draft [DIR]      # the drawn tiles as a full tiles.png (and the two water-edge
                                                   #   animation strips) in DIR (gfx/drafts/t438/general/), groups.json
                                                   #   beside them, the seam measure, and the contact sheets
                                                   #   (--sheets DIR puts the sheets elsewhere)
    python3 tools/gbageneral.py --write --approved # into the engine: pass 3, approved by the user 2026-10-22 and
                                                   #   BUILT (T-438 batch C); without --approved --write refuses

PASS 2 AND 3 (the user, 2026-10-22: "a bolder second pass -- rock that reads as solid stone with a look of our own, and
motifs for fences, bushes, hedges and the blue house"; on pass 2: the motifs approved with the ribbed roof, the rock
to go "chunkier" -- big irregular blocks and boulders, no long parallel stripes). --draft now writes PASS 3 into DIR
(pass 1 and pass 2 beside it in DIR/pass1/ and DIR/pass2/) and --write --approved would write pass 3: pass 2's motifs,
and the rock as redraw_rock3 draws it -- lumps of four sizes and boulders, lit tops, shaded feet, the planes read from
each tile itself so a tile shared between blocks agrees with its neighbours in all of them. What pass 2 added:

    rock             DRAWN, not re-surfaced (redraw_rock): vanilla's light cut into three planes with hard edges --
                     a lit TOP (terraced: a few long shaded steps with a lit lip, running on over the blocks' edges),
                     a SHOULDER and a FACE (strata: bedding lines and staggered joints) -- and a lit rim where a plane
                     turns down. Layered stone in place of Kanto's scales. Outlines and joins stay vanilla's.
    motifs           drawn inside their own footprints: the metal fence (faceted square posts, a bright cap), the
                     wooden fence (squared timber with grain), the round bush and the hedge (gbatrees.py's crown in
                     little), the blue house's roof (ROOF_STYLE: standing-seam "ribbed" metal, or "shingle"), the
                     signboard (planks in a frame) and SAFFRON GYM's sign (a plaque with a red header)
    a palette        PROPOSED, never written: row 1's rock ramp 9..14 as an ochre sandstone (ROCK_RECOLOUR); the map
                     sheets show it as a fourth panel and groups.json lists every tile it would touch
    sheets           t438c3_maps_N.png (today | pass 2 | pass 3, at 1x and 2x), t438c3_rock_kit.png (the mountain
                     kit's blocks at 5x), t438c3_motifs.png, t438c3_ground_<group>.png

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


def unfilled(c):
    """a palette slot nobody filled: pret leaves them magenta (T-484)"""
    return tuple(c[:3]) == (255, 0, 255)


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
        # an index vanilla did not use here must be a real colour in EVERY row that draws the tile: UMBRA PLATEAU's
        # row 12 leaves 5 and 9..12 unfilled (magenta), and the paving's step to 9 showed there as pink specks
        # (T-484). A pixel that lands on one takes the nearest step that is filled everywhere instead
        holes = {i for i in ramp if i not in idxs and any(unfilled(palette(k)[i]) for k in rows)}
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
                j = max(lo_t, min(hi_t, n))
                if ramp[j] in holes:
                    j = min((q for q in range(lo_t, hi_t + 1) if ramp[q] not in holes),
                            key=lambda q: (abs(q - j), abs(q - b)))
                out[y * 8 + x] = ramp[j]
    return out, notes


# ================================================================== pass 2: solid stone
#  The second pass (the user, 2026-10-22: "a bolder second pass -- rock that reads as solid stone with a look of our
#  own"). Pass 1 kept vanilla's light and laid a small texture over it, and the rock read flatter and noisier than
#  Kanto's. Pass 2 DRAWS the rock: a 16x16 pattern of a few large stones, each stone ONE flat tone with a lit lip
#  along its top and left, a shaded lip along its bottom and right, and a dark crack round it. Two patterns:
#
#      TOPS    faceted slabs (three a block) where vanilla's rock is lit -- the plateaus, the tops of ledges
#      FACES   strata: bands of stone five and six pixels deep, parted by dark bedding lines and staggered joints,
#              where vanilla's rock is in shadow -- every cliff face, every ledge's lip
#
#  Which pattern and which tone is read from vanilla: its tones smoothed over the whole block (5x5), and the mean of
#  that over each STONE of the pattern, so a stone is one tone and a change of light falls on a crack. The ramp is the
#  whole of row 1's rock, 9..14 -- the outline colour 14 now also the deepest crack -- and a pixel whose neighbour in
#  its block is not rock keeps vanilla's index: every outline, every silhouette and every join with the grass, sand
#  or water beside it stays where it was. Every rock tile sits in one quarter of its block, unflipped (the census);
#  the pattern is a 16x16 torus placed by that quarter, so it runs on across every block of a mountain.
ROCK_RAMP = [9, 10, 11, 12, 13, 14]      # light to dark, in row 1 and in every town row that draws a rock tile
ROLE_OFF = {"hi": -1, "body": 0, "lo": 1, "crack": 2}


def _label_roles(lab, cracks=None):
    """a 16x16 torus of stone labels -> (labels, roles). A crack where a stone meets the stone below it or to its
    right; the lit lip is the pixel under or right of a crack, the shaded lip the pixel above or left of one"""
    crack = [[False] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if cracks is not None:
                crack[y][x] = cracks[y][x]
            else:
                crack[y][x] = lab[y][x] != lab[y][(x + 1) % 16] or lab[y][x] != lab[(y + 1) % 16][x]
    role = [[None] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if crack[y][x]:
                role[y][x] = "crack"
            elif crack[(y - 1) % 16][x] or crack[y][(x - 1) % 16]:
                role[y][x] = "hi"
            elif crack[(y + 1) % 16][x] or crack[y][(x + 1) % 16]:
                role[y][x] = "lo"
            else:
                role[y][x] = "body"
    return lab, role


def _cracked(cracks_at):
    """a 16x16 torus of roles from a list of crack pixels"""
    cracks = [[False] * 16 for _ in range(16)]
    for x, y in cracks_at:
        cracks[y % 16][x % 16] = True
    return _label_roles([[0] * 16 for _ in range(16)], cracks)[1]


def _line(pts):
    """the pixels of a polyline, 8-connected"""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for k in range(n + 1):
            out.append((x0 + round((x1 - x0) * k / max(n, 1)), y0 + round((y1 - y0) * k / max(n, 1))))
    return out


#  TOPS: a lit plane, terraced -- the strata of the faces showing through as low steps, each a shaded line with a lit
#  lip under it, of different lengths and running on over the blocks' edges, so the plane does not read as a grid
def _terraces():
    role = [["body"] * 16 for _ in range(16)]
    for y, xs in ((1, range(3, 12)), (5, list(range(12, 16)) + list(range(0, 5))), (9, range(6, 14)),
                  (13, list(range(14, 16)) + list(range(0, 3)) + list(range(8, 11)))):
        xs = list(xs)
        for k, x in enumerate(xs):
            role[y][x] = "lo" if k in (0, len(xs) - 1) else "crack"
        for x in xs[1:-1]:
            role[(y + 1) % 16][x] = "hi"
    return role


TOP_ROLE = _terraces()
#  FACES: strata -- three beds a block, each bedding line stepping once, one joint in two of the beds
STRATA_ROLE = _cracked([(x, 2 if x < 9 else 3) for x in range(16)] + [(x, 7 if x < 4 else 6) for x in range(16)] +
                       [(x, 12 if x < 12 else 13) for x in range(16)] + [(12, 4), (12, 5)] + [(5, 9), (5, 10)])
PLANES = (("top", 2.0), ("shoulder", 3.1), ("face", 99))
PLANE_INDEX = {   # plane -> {role: index}, row 1's rock ramp 9 (light) .. 14 (dark)
    "top":      {"body": 10, "hi": 9, "lo": 11, "crack": 12, "rim": 9},
    "shoulder": {"body": 12, "hi": 11, "lo": 13, "crack": 14, "rim": 11},
    "face":     {"body": 13, "hi": 12, "lo": 14, "crack": 14, "rim": 13},
}


def rock_rows_ok(rows):
    """True when every row that draws the tile orders 9..14 light to dark"""
    for k in rows:
        p = palette(k)
        ls = [lum(p[i]) for i in ROCK_RAMP]
        if any(ls[i] <= ls[i + 1] for i in range(len(ls) - 1)):
            return False
    return True


def rock_grid(t, px):
    """the block this tile is drawn in most, as a 16x16 grid of indices (None where nothing of this layer and row),
    and the tile's (ox, oy) in it. A rock tile drawn in several blocks (129 in 115 and 112) is read in the one that
    draws it most, so the blocks a player sees most are the ones whose quarters agree"""
    ox, oy = QUARTER2.get(t, (0, 0))
    grid = [[None] * 16 for _ in range(16)]
    if t in BLOCK_OF2:
        for x, y, v in BLOCK_OF2[t]:
            grid[y][x] = v
    for y in range(8):
        for x in range(8):
            grid[oy + y][ox + x] = px[y * 8 + x] or None
    return grid, ox, oy


def redraw_rock(t, px, rows):
    """pass 2's stone for one tile; None when its rows do not keep the ramp's order"""
    if not rock_rows_ok(rows):
        return None
    R = ROCK_RAMP
    grid, ox, oy = rock_grid(t, px)
    isrock = lambda v: v is not None and v in R
    # vanilla's light, smoothed over the block (5x5), cut into three planes with hard edges between them
    plane = [[None] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if not isrock(grid[y][x]):
                continue
            acc = n = 0
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < 16 and 0 <= yy < 16 and isrock(grid[yy][xx]):
                        acc += R.index(grid[yy][xx])
                        n += 1
            s = acc / n
            plane[y][x] = next(name for name, top in PLANES if s <= top)
    cells = [(x, y) for y in range(16) for x in range(16) if plane[y][x]]
    qmean = []
    for qx in (0, 8):
        for qy in (0, 8):
            qs = [R.index(grid[y][x]) for x, y in cells if qx <= x < qx + 8 and qy <= y < qy + 8]
            qmean.append(sum(qs) / len(qs) if len(qs) > 48 else None)
    if None not in qmean and max(qmean) - min(qmean) < 0.7:
        # a fill block, rock all over and lit evenly, tiles with itself: one plane, from its mean light
        mean = sum(R.index(grid[y][x]) for x, y in cells) / len(cells)
        level = next(name for name, top in PLANES if mean <= top)
        for x, y in cells:
            plane[y][x] = level
    else:                                # a scrap of one plane inside another, away from the block's edge, joins it
        seen = set()
        for c in cells:
            if c in seen:
                continue
            comp, stack, border, nbr = [], [c], False, collections.Counter()
            while stack:
                x, y = stack.pop()
                if (x, y) in seen:
                    continue
                seen.add((x, y))
                comp.append((x, y))
                border |= x in (0, 15) or y in (0, 15)
                for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= a < 16 and 0 <= b < 16 and plane[b][a]:
                        if plane[b][a] == plane[y][x]:
                            stack.append((a, b))
                        else:
                            nbr[plane[b][a]] += 1
            if len(comp) < 20 and not border and nbr:
                to = nbr.most_common(1)[0][0]
                for x, y in comp:
                    plane[y][x] = to
    order = [p for p, _ in PLANES]
    out = list(px)
    for y in range(8):
        for x in range(8):
            v = px[y * 8 + x]
            if v not in R:
                continue
            bx, by = ox + x, oy + y
            nb = [(bx + dx, by + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= bx + dx < 16 and 0 <= by + dy < 16]
            if any(not isrock(grid[b][a]) for a, b in nb):
                continue                                   # the silhouette and every join: vanilla's
            p = plane[by][bx]
            lower = any(plane[b][a] is not None and order.index(plane[b][a]) > order.index(p) for a, b in nb)
            if lower:
                role = "rim"                               # the lit edge where a plane turns down into the next
            else:
                role = (TOP_ROLE if p == "top" else STRATA_ROLE)[by][bx]
            out[y * 8 + x] = PLANE_INDEX[p][role]
    return out


# ================================================================== pass 3: chunky rock
#  The user on pass 2 (2026-10-22): keep the lit tops, the dark faces and the bright rims, but "break the horizontal
#  layers into big irregular blocks and boulders" -- varied sizes, angled cracks between masses, a few rounded
#  boulders on the tops, no long parallel stripes; rock, not stacked planks or a mesa.
#
#  So: ONE pattern of stones for the whole mountain on the 16x16 torus (below), each stone one flat tone, a lit lip
#  under the crack above it, shaded at its foot; the smallest are boulders.
#
#  The planes (top, shoulder or face) are read from vanilla's smoothed light as in pass 2, a scrap of one inside
#  another joins it, and a lit plane against a darker one gets the bright rim. The light is read
#  from the TILE ITSELF (a rock tile shared between blocks, 129 in 112 and 115, 132 in 114 and 117, is then the same
#  wherever it is, and its edge agrees with its neighbour's because vanilla's light runs on across the joint), and a
#  tile whose main block is an evenly lit fill (113) takes that block's one plane, from the block's mean light.
#  The stones: four masses a block of four sizes, a weighted Voronoi on the torus with its seeds off the 8-pixel grid
#  and off each other's half-period, so the cracks run at every angle and the masses do not fall into a lattice. Each
#  mass is shaded as a LUMP: a lit band along its top, its body, a shaded band along its foot two pixels deep, and a
#  dark crack under it -- so it reads as a block of stone standing up from the rest. The smallest masses are boulders:
#  on a lit top they get a highlight inside their upper left as well.
STONE_SEEDS = [(10.0, 9.5, 3.4), (17.5, 5.5, 1.4), (16.0, 14.5, 2.6), (7.0, 16.5, 1.2)]
BOULDERS = {1, 3}
MASS_TONE = {0: 0, 1: 0, 2: 1, 3: 0}


def _stones():
    lab = [[0] * 16 for _ in range(16)]
    off = [[(0.0, 0.0)] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            best = None
            for k, (a, b, w) in enumerate(STONE_SEEDS):
                dx = (x + 0.5 - a + 8) % 16 - 8
                dy = (y + 0.5 - b + 8) % 16 - 8
                d = (dx * dx + dy * dy) ** 0.5 - w
                if best is None or d < best[0]:
                    best = (d, k, dx, dy)
            lab[y][x] = best[1]
            off[y][x] = best[2:]
    crack = [[any(lab[y][x] < lab[(y + v) % 16][(x + u) % 16] for u, v in ((1, 0), (0, 1), (-1, 0), (0, -1)))
              for x in range(16)] for y in range(16)]
    same = lambda x, y, k: lab[y % 16][x % 16] == k and not crack[y % 16][x % 16]

    def run(x, y, step):
        n = 0
        while n < 6 and same(x, y + step * (n + 1), lab[y][x]):
            n += 1
        return n
    role = [[None] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            k = lab[y][x]
            if crack[y][x]:
                role[y][x] = "crack"
                continue
            up, down = run(x, y, -1), run(x, y, 1)
            left = same(x - 1, y, k)
            dx, dy = off[y][x]
            if down == 0:
                role[y][x] = "lo2"                    # the foot of the lump, in shadow
            elif down == 1:
                role[y][x] = "lo"
            elif up == 0 or not left:
                role[y][x] = "hi"                     # its lit top and left edge
            elif k in BOULDERS and dx + dy < 0:
                role[y][x] = "boulder"
            else:
                role[y][x] = "body"
    return lab, role


STONE_LAB, STONE_ROLE = _stones()
FILL_BLOCKS = {}   # block -> the one plane its tiles take


def find_fills():
    """the general blocks that are rock all over and evenly lit (113): a tile drawn in one most takes one plane"""
    R = ROCK_RAMP
    for mid in range(len(GMT) // 16):
        for L in (0, 1):
            quad = entries(GMT, mid)[L * 4:L * 4 + 4]
            means = []
            for v in quad:
                t = v & 0x3FF
                px = CUR[t] if t < 640 and v >> 12 == 1 else []        # row 1's rock, not row 0's grass
                rk = [R.index(c) for c in px if c in R]
                means.append(sum(rk) / len(rk) if len(rk) > 56 else None)
            if None not in means and max(means) - min(means) < 0.7:
                FILL_BLOCKS[mid] = next(name for name, top in PLANES if sum(means) / 4 <= top)


def redraw_rock3(t, px, rows):
    """pass 3's stone for one tile; None when its rows do not keep the ramp's order"""
    if not rock_rows_ok(rows):
        return None
    R = ROCK_RAMP
    ox, oy = QUARTER2.get(t, (0, 0))
    isrock = lambda x, y: 0 <= x < 8 and 0 <= y < 8 and px[y * 8 + x] in R
    order = [p for p, _ in PLANES]
    level = None
    main = USE.get(t) and [b for b in USE[t]["blocks"].most_common() if b[0][0] == "general"]
    if main and main[0][0][1] in FILL_BLOCKS:
        level = FILL_BLOCKS[main[0][0][1]]
    plane = {}
    for y in range(8):
        for x in range(8):
            if not isrock(x, y):
                continue
            if level:
                plane[(x, y)] = level
                continue
            acc = n = 0
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if isrock(x + dx, y + dy):
                        acc += R.index(px[(y + dy) * 8 + x + dx])
                        n += 1
            plane[(x, y)] = next(name for name, top in PLANES if acc / n <= top)
    # a scrap of one plane inside another, away from the tile's edge, joins it (block 179's light notch)
    seen = set()
    for c in list(plane):
        if c in seen:
            continue
        comp, stack, border, nbr = [], [c], False, collections.Counter()
        while stack:
            x, y = stack.pop()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            comp.append((x, y))
            border |= x in (0, 7) or y in (0, 7)
            for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (a, b) in plane:
                    if plane[(a, b)] == plane[(x, y)]:
                        stack.append((a, b))
                    else:
                        nbr[plane[(a, b)]] += 1
        if len(comp) < 12 and nbr and (not border or len(comp) < 5):
            to = nbr.most_common(1)[0][0]
            for q in comp:
                plane[q] = to
    sp = lambda x, y: plane[(x, y)]
    out = list(px)
    for y in range(8):
        for x in range(8):
            if not isrock(x, y):
                continue
            nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < 8 and 0 <= y + dy < 8]
            if any(not isrock(a, b) for a, b in nb):
                continue                                   # the silhouette and every join: vanilla's
            p = sp(x, y)
            X, Y = (ox + x) % 16, (oy + y) % 16
            role = STONE_ROLE[Y][X]
            shift = MASS_TONE[STONE_LAB[Y][X]]
            if role != "crack" and any(isrock(a, b) and order.index(sp(a, b)) > order.index(p) for a, b in nb):
                role, shift = "rim", 0
            if role == "boulder":
                role = "hi" if p == "top" else "body"
            if role == "lo2":
                role, shift = "lo", shift + 1
            v = PLANE_INDEX[p][role]
            if shift and role in ("body", "hi", "lo"):
                v = R[min(len(R) - 1, R.index(v) + shift)]
            out[y * 8 + x] = v
    return out


QUARTER2 = {}      # pass 2: tile -> (x, y) of the quarter that draws it most (unflipped), when that is 75% of draws
BLOCK_OF2 = {}


def place_quarters(use):
    for t, u in use.items():
        qs = u["quads"]
        tot = sum(qs.values())
        (q, flip), n = qs.most_common(1)[0]
        if flip == 0 and n >= 0.75 * tot:
            QUARTER2[t] = ((q % 2) * 8, (q // 2) * 8)
            gb = [b for b in u["blocks"].most_common() if b[0][0] == "general"]
            for (ts, mid), _ in gb:
                e = entries(GMT, mid)
                if any(e[L * 4 + q] & 0x3FF == t and not e[L * 4 + q] & 0xC00 for L in (0, 1)):
                    bl = block_layer(GMT, mid, t, CUR)
                    if bl:
                        BLOCK_OF2[t] = bl
                    break


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


# ================================================================== pass 2's sheets
_LAYOUTS = None


def layout_named(name):
    global _LAYOUTS
    if _LAYOUTS is None:
        _LAYOUTS = {l["id"]: l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
                    if "id" in l}
    return _LAYOUTS[json.load(open(os.path.join(GBA, "data/maps/%s/map.json" % name)))["layout"]]


_ANIM_NOW = {}


def anim_now(strip):
    if strip not in _ANIM_NOW:
        _ANIM_NOW[strip] = anim_frames(strip)
    return _ANIM_NOW[strip]


def render2(name, tiles, strips=None, pals=None, box=None):
    """a map (or a box of it, in cells) as the screen draws it: General's tiles from `tiles` (640 lists of 64), the
    water strips' frame 0 over 416..481 as VRAM has them (trap 39), and General's rows 0..6 from `pals`"""
    l = layout_named(name)
    sec = secondary(l["secondary_tileset"])
    pals = pals or PALS
    allp = [pals[r] for r in range(7)] + [sec["pals"][r] for r in range(7, 16)]
    tl = [list(p) for p in tiles]
    for strip, first, n in ANIMS:
        fr = (strips or {}).get(strip, [None])[0] or anim_now(strip)[0]
        for k in range(n):
            tl[first + k] = strip_tile(fr, k)
    stp = sec["tiles"].load()
    sw, sh = sec["tiles"].size
    W, H = l["width"], l["height"]
    d = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    x0, y0, w, h = box or (0, 0, W, H)
    w, h = min(w, W - x0), min(h, H - y0)
    img = Image.new("RGB", (w * 16, h * 16))
    o = img.load()
    for yy in range(h):
        for xx in range(w):
            m = struct.unpack_from("<H", d, ((y0 + yy) * W + x0 + xx) * 2)[0] & 0x3FF
            buf, k = (GMT, m) if m < 640 else (sec["mt"], m - 640)
            if (k + 1) * 16 > len(buf):
                continue
            e = entries(buf, k)
            for layer in (0, 1):
                for q in range(4):
                    v = e[layer * 4 + q]
                    t, row = v & 0x3FF, v >> 12
                    for ty in range(8):
                        for tx in range(8):
                            sx = 7 - tx if v & 0x400 else tx
                            sy = 7 - ty if v & 0x800 else ty
                            if t < 640:
                                c = tl[t][sy * 8 + sx]
                            else:
                                j = t - 640
                                py = (j // (sw // 8)) * 8 + sy
                                c = stp[(j % (sw // 8)) * 8 + sx, py] & 15 if py < sh else 0
                            if layer and c == 0:
                                continue
                            o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = allp[row][c]
    return img


MAP_CROPS2 = [   # (map, x0, y0, w, h in cells, what it shows)
    ("Route1", 0, 16, 24, 14, "ROUTE 1: ledges, sand, the paths"),
    ("Route2", 0, 44, 24, 14, "ROUTE 2: ledges and fences"),
    ("Route3", 44, 0, 40, 20, "ROUTE 3: cliffs and mountain rock"),
    ("Route4", 0, 0, 40, 20, "ROUTE 4: MT MOON's flank"),
    ("Route22", 0, 0, 30, 24, "ROUTE 22: cliffs, ledges, a fence and its sign"),
    ("VermilionCity", 4, 10, 30, 30, "VERMILION: the beach, the docks, a hedge"),
    ("CeruleanCity", 6, 4, 30, 24, "CERULEAN: town fences, a sign, paving, the blue house"),
]


MAP_CROPS3 = [   # pass 3's sheets: the rock
    ("Route3", 44, 0, 40, 20, "ROUTE 3: cliffs and mountain rock"),
    ("Route4", 0, 0, 40, 20, "ROUTE 4: MT MOON's flank"),
    ("Route22", 0, 0, 30, 24, "ROUTE 22: cliffs and ledges"),
    ("SevenIsland_SevaultCanyon", 0, 20, 24, 24, "SEVAULT CANYON (Sevii): a mountain in a town row"),
]
KIT_BLOCKS = [104, 105, 106, 112, 113, 114, 115, 117, 120, 121, 122, 124, 179]


def kit_sheet(versions, path, Z=5):
    """the mountain kit's blocks at 5x, one row a version: 112 and 114 beside 115 and 117 (their shared tiles), 179's
    inner corner"""
    F, f2 = font(15), font(12)
    cell = 16 * Z + 6
    im = Image.new("RGB", (130 + len(KIT_BLOCKS) * cell, 40 + len(versions) * (cell + 18)), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-438 C, third pass: the mountain kit, 5x   (DRAFT)", fill=(250, 214, 120), font=F)
    y = 34
    for label, tl in versions:
        dr.text((8, y + 30), label, fill=(220, 220, 230), font=f2)
        for k, b in enumerate(KIT_BLOCKS):
            dr.text((130 + k * cell, y), str(b), fill=(200, 200, 210), font=f2)
            im.paste(block_rgb("general", b, tl, Z), (130 + k * cell, y + 14))
        y += cell + 18
    im.save(path)
    return path


def map_sheet2(crop, versions, path, which="second"):
    """one map crop: every version side by side at 1x, then again at 2x"""
    name, x0, y0, w, h, why = crop
    F, f2 = font(15), font(12)
    shots = [(label, render2(name, tl, st, pals, (x0, y0, w, h))) for label, tl, st, pals in versions]
    a = shots[0][1]
    gap = 12
    W1 = len(shots) * (a.width + gap) + 16
    W2 = len(shots) * (a.width * 2 + gap) + 16
    W = max(W1, W2) if W2 <= 4200 else max(W1, 2 * (a.width * 2 + gap) + 16)
    two_rows = W2 > 4200
    H = 40 + a.height + 30 + (a.height * 2 + 30) * (2 if two_rows else 1) * (1 if not two_rows else 1) + 10
    if two_rows:
        H = 40 + a.height + 30 + ((len(shots) + 1) // 2) * (a.height * 2 + 30) + 10
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-438 C, %s pass   %s   (DRAFT)" % (which, why), fill=(250, 214, 120), font=F)
    y = 30
    for k, (label, s) in enumerate(shots):
        dr.text((8 + k * (a.width + gap), y), label + "  1x", fill=(220, 220, 230), font=f2)
        im.paste(s, (8 + k * (a.width + gap), y + 16))
    y += a.height + 30
    for k, (label, s) in enumerate(shots):
        big = s.resize((s.width * 2, s.height * 2), Image.NEAREST)
        if two_rows:
            cx, cy = 8 + (k % 2) * (big.width + gap), y + (k // 2) * (big.height + 30)
        else:
            cx, cy = 8 + k * (big.width + gap), y
        dr.text((cx, cy), label + "  2x", fill=(220, 220, 230), font=f2)
        im.paste(big, (cx, cy + 16))
    im.save(path)
    return path


# ================================================================== pass 2: drawing a tile
MOTIFS = {}        # tile -> function(t, px, rows) -> 64 indices: the motifs, drawn below
MOTIF_TILES = {}   # motif name -> its tiles, for groups.json and the motif sheet
#  A PROPOSAL, not made: row 1's rock ramp (9..14) from Kanto's pink-brown to a warm ochre sandstone, so the layered
#  stone of pass 2 reads as a stone of our own. Shown as a fourth panel on every map sheet; --write never writes it.
ROCK_RECOLOUR = {9: (240, 224, 184), 10: (224, 200, 148), 11: (196, 158, 108), 12: (156, 114, 80), 13: (120, 82, 62),
                 14: (86, 58, 52)}
RECOLOUR = [list(p) for p in PALS]
for _i, _c in ROCK_RECOLOUR.items():
    RECOLOUR[1][_i] = _c
USE = {}


def RECOLOUR_REPORT():
    """every General tile a map draws in row 1 with any of 9..14 -- what the recolour would touch"""
    hit = collections.defaultdict(list)
    for t, u in sorted(USE.items()):
        if ("general", 1) in u["rows"] and any(v in ROCK_RECOLOUR for v in CUR[t]):
            g = group_of(t, u) if CUR[t] == VAN[t] else "already ours"
            hit[g].append(t)
    return {"row": 1, "from": {str(i): list(PALS[1][i]) for i in ROCK_RECOLOUR},
            "to": {str(i): list(c) for i, c in ROCK_RECOLOUR.items()}, "tiles": dict(hit),
            "count": sum(len(v) for v in hit.values())}


# ================================================================== pass 2: the motifs
#  Each drawn inside its own footprint: a pixel that was transparent stays so, a pixel of grass or sand round a post
#  stays that, and only the motif's own material is redrawn -- so no silhouette, no join and no block moves. Drawn as
#  the world's own things are (gbatrees.py's tree, gbacivic.py's houses): a dark outline all round, a lit top, a lit
#  face and a shaded face, flat tones rather than dither.
def runs(px, mat, x, y):
    """(horizontal run, vertical run, place along each) of the material through (x, y), inside the tile"""
    a = x
    while a > 0 and px[y * 8 + a - 1] in mat:
        a -= 1
    b = x
    while b < 7 and px[y * 8 + b + 1] in mat:
        b += 1
    c = y
    while c > 0 and px[(c - 1) * 8 + x] in mat:
        c -= 1
    d = y
    while d < 7 and px[(d + 1) * 8 + x] in mat:
        d += 1
    return a, b, c, d


def paint_solid(px, mat, keep, ink):
    """a post or a rail, faceted: the material's dark pixels (keep) are its outline and stay as they are, so every
    silhouette and join does; inside them, a bright cap where the outline closes over the top, then three flat faces
    across each run -- lit, mid and shaded -- in place of vanilla's rounded gradient. ink: role -> index"""
    out = list(px)
    inner = lambda a, b: 0 <= a < 8 and 0 <= b < 8 and px[b * 8 + a] in mat and px[b * 8 + a] not in keep
    for y in range(8):
        for x in range(8):
            if not inner(x, y):
                continue
            a = x
            while inner(a - 1, y):
                a -= 1
            b = x
            while inner(b + 1, y):
                b += 1
            w = b - a + 1
            if y > 0 and not inner(x, y - 1):
                role = "cap"
            elif w >= 7:
                role = "mid"                                  # a rail seen end-on across the tile
            elif x - a < max(1, w // 3):
                role = "lit"
            elif b - x < max(1, w // 3):
                role = "shade"
            else:
                role = "mid"
            out[y * 8 + x] = ink[role]
    return out


GREY = set(range(1, 8))
METAL_INK = {"cap": 1, "lit": 1, "mid": 3, "shade": 4}
WOOD = set(range(9, 15))
WOOD_INK = {"cap": 10, "lit": 11, "mid": 12, "shade": 13}


def m_metal(t, px, rows):
    """the metal fence: square iron posts, a bright cap, a lit face and a shaded face; the rails flat bars"""
    return paint_solid(px, GREY, {5, 6, 7}, METAL_INK)


def m_wood(t, px, rows):
    """the wooden fence: squared timber posts in place of the cut log ends, the grain down the shaded face"""
    out = paint_solid(px, WOOD, {14}, WOOD_INK)
    for y in range(8):
        for x in range(8):
            if out[y * 8 + x] == WOOD_INK["mid"] and y % 4 == (x % 2) * 2 and px[y * 8 + x] in WOOD:
                out[y * 8 + x] = 13                       # the grain
    return out


def crown(px, mat, block, ox, oy, lobes, ink):
    """gbatrees.py's crown in little: lobes lit across their tops and dark across their feet (the top of the
    highest lobe over a pixel decides), a little of the tree's texture, a deep outline round the silhouette"""
    grid = [[None] * 16 for _ in range(16)]
    for x, y, v in block:
        grid[y][x] = v
    for y in range(8):
        for x in range(8):
            grid[oy + y][ox + x] = px[y * 8 + x]
    out = list(px)
    for y in range(8):
        for x in range(8):
            if px[y * 8 + x] not in mat:
                continue
            bx, by = ox + x, oy + y
            if any(0 <= a < 16 and 0 <= b < 16 and grid[b][a] is not None and grid[b][a] not in mat
                   for a, b in ((bx + 1, by), (bx - 1, by), (bx, by + 1), (bx, by - 1))):
                out[y * 8 + x] = ink["deep"]
                continue
            cover = [(cx, cy, r) for cx, cy, r in lobes if (bx + 0.5 - cx) ** 2 + (by + 0.5 - cy) ** 2 <= r * r]
            if not cover:
                out[y * 8 + x] = ink["dark"]
                continue
            k = min((by + 0.5 - (cy - r)) / (2 * r) for cx, cy, r in cover)
            shade = 0 if k < 0.3 else 1 if k < 0.62 else 2
            if (bx * 5 + by * 3) % 7 == 0 and shade:
                shade -= 1
            elif (bx * 3 + by * 7) % 11 == 0 and shade < 2:
                shade += 1
            out[y * 8 + x] = (ink["lit"], ink["leaf"], ink["dark"])[shade]
    return out


MOTIF_BLOCK = {}   # tile -> the general block a motif is drawn in


def motif_block(t):
    mid = MOTIF_BLOCK.get(t)
    if mid is None:
        return QUARTER2.get(t, (0, 0)), BLOCK_OF2.get(t, [])
    e = entries(GMT, mid)
    q = next(k % 4 for k in range(8) if e[k] & 0x3FF == t)
    return ((q % 2) * 8, (q // 2) * 8), block_layer(GMT, mid, t, CUR) or []


LEAF = {1, 2, 3, 4}
LEAF_INK = {"lit": 1, "leaf": 2, "dark": 3, "deep": 4}
BUSH_LOBES = [(8.0, 6.0, 4.6), (4.6, 9.0, 4.2), (11.4, 9.0, 4.2), (8.0, 11.5, 4.2)]
HEDGE_LOBES = [(x + 4.0, 5.5, 4.4) for x in (-8, 0, 8, 16)] + [(x, 10.5, 4.2) for x in (0, 8, 16)]


def m_bush(t, px, rows):
    """the round bush: four lobes of gbatrees.py's crown"""
    (ox, oy), bl = motif_block(t)
    return crown(px, LEAF, bl, ox, oy, BUSH_LOBES, LEAF_INK)


def m_hedge(t, px, rows):
    """the hedge: a row of the crown's lobes along its top, a second row staggered under them, 8 pixels apart so a
    hedge of any length runs on"""
    (ox, oy), bl = motif_block(t)
    return crown(px, LEAF, bl, ox, oy, HEDGE_LOBES, LEAF_INK)


ROOF_STYLE = "ribbed"     # the blue house's roof: "ribbed" (standing-seam metal, as our houses') or "shingle"


def t_ribs(x, y, tile, base=None, top=None):
    """standing-seam metal: a lit seam every four pixels with its shadow beside it"""
    return {0: -2.0, 1: 2.0, 2: 0.3, 3: 0.6}[x % 4]


def t_shingle2(x, y, tile, base=None, top=None):
    """shingles: courses three deep, a dark butt line, a lit lip, joints staggered course to course"""
    course = (y // 3) % 2
    r = y % 3
    if r == 2:
        return 2.0
    if r == 0:
        return -1.5
    return 1.8 if (x + 3 * course) % 6 == 0 else 0.0


TEX["ribs"] = t_ribs
TEX["shingle2"] = t_shingle2
LOCAL["ribs"] = 0.0
LOCAL["shingle2"] = 0.0


def m_roof(t, px, rows, style=None):
    new, _ = redraw(t, px, rows, "roof2", {"*": "ribs" if (style or ROOF_STYLE) == "ribbed" else "shingle2"})
    return new


def m_board(t, px, rows):
    """the signboard: a timber board in a dark frame, its planks lit along their tops"""
    out = list(px)
    for y in range(8):
        for x in range(8):
            v = px[y * 8 + x]
            if v in (9, 10, 11, 12):                  # the board inside its frame (13, 14 kept): planks, lit on top
                up = y > 0 and px[(y - 1) * 8 + x] in (13, 14)
                out[y * 8 + x] = 9 if up else 11 if (y + (t in (380, 381)) * 8) % 3 == 0 else 10
    return out


GYM_SIGN = {   # SAFFRON GYM's sign (row 2): a white plaque, a red header, three lines of lettering, a dark frame
    366: ["67777777", "71111111", "7cccccc1", "7dddddd1", "71111111", "71665661", "71111111", "71666561"],
    367: ["77777776", "11111117", "1cccccd7", "1dddddd7", "11111117", "16566517", "11111117", "16511117"],
    382: ["71111111", "71656661", "71111111", "75555555", "77777777", "00555555", "00000000", "00000000"],
    383: ["11111117", "16561117", "11111117", "55555557", "77777777", "55555000", "00000000", "00000000"],
}


def m_gymsign(t, px, rows):
    pic = [int(c, 16) for c in "".join(GYM_SIGN[t])]
    return [pic[i] if px[i] and pic[i] else px[i] for i in range(64)]


for _t in (14, 15, 30, 31, 47, 499, 500, 308, 309, 324, 325):
    MOTIFS[_t] = m_metal
for _t in (46, 62, 63, 340, 356, 357, 239):
    MOTIFS[_t] = m_wood
for _t in (12, 13, 28, 29):
    MOTIFS[_t] = m_bush
    MOTIF_BLOCK[_t] = 5
MOTIF_BLOCK.update({44: 317, 92: 317, 45: 318, 93: 318, 53: 326, 60: 343})
for _t in (44, 45, 92, 93, 53, 60):
    MOTIFS[_t] = m_hedge
for _t in ROOFS:
    MOTIFS[_t] = m_roof
for _t in (364, 365, 380, 381):
    MOTIFS[_t] = m_board
for _t in GYM_SIGN:
    MOTIFS[_t] = m_gymsign
MOTIF_TILES.update({
    "metal fence": [14, 15, 30, 31, 47, 499, 500, 308, 309, 324, 325],
    "wooden fence": [46, 62, 63, 340, 356, 357, 239],
    "round bush": [12, 13, 28, 29],
    "hedge": [44, 45, 92, 93, 53, 60],
    "blue house roof": sorted(ROOFS),
    "signboard": [364, 365, 380, 381],
    "SAFFRON GYM sign": sorted(GYM_SIGN),
})
MOTIF_BLOCKS = [   # (motif, [(tileset, block)]) for the sheet
    ("metal fence", [("general", b) for b in (223, 231, 236, 238, 244, 246, 252, 309, 214)]),
    ("wooden fence", [("general", b) for b in (222, 230, 232, 234, 240, 242, 248)]),
    ("round bush", [("general", 5)]),
    ("hedge", [("general", b) for b in (317, 318, 319, 326, 333, 343)]),
    ("blue house roof", [("general", b) for b in (44, 45, 47, 52, 53, 54, 55)]),
    ("signboard", [("general", 3)]),
    ("SAFFRON GYM sign", [("gTileset_SaffronCity", 780)]),
]


def block_rgb(ts, mid, tiles, Z, pals=None):
    """one block, both layers, at Z, its transparent pixels on a dark ground"""
    pals = pals or PALS
    if ts == "general":
        buf, i, sec = GMT, mid, None
    else:
        sec = secondary(ts)
        buf, i = sec["mt"], mid - 640
    stp = sec and sec["tiles"].load()
    sw = sec and sec["tiles"].size[0]

    def src(t, x, y):
        if t < 640:
            return tiles[t][y * 8 + x]
        j = t - 640
        return stp[(j % (sw // 8)) * 8 + x, (j // (sw // 8)) * 8 + y] & 15
    pal_of = lambda r: pals[r] if r < 7 else sec["pals"][r]
    o = composite(buf, i, src, pal_of)
    im = Image.new("RGB", (16, 16))
    for y in range(16):
        for x in range(16):
            im.putpixel((x, y), o[y][x] or (40, 40, 46))
    return im.resize((16 * Z, 16 * Z), Image.NEAREST)


def motif_sheet(new_tiles, path, Z=4):
    """every motif's blocks at 4x: TODAY above, PASS 2 under it (and the roof's other style beside)"""
    F, f2 = font(15), font(12)
    alt = [list(p) for p in new_tiles]
    other = "shingle" if ROOF_STYLE == "ribbed" else "ribbed"
    use_rows = {t: collections.Counter({("general", 3): 1}) for t in ROOFS}
    for t in ROOFS:
        if new_tiles[t] != CUR[t]:
            alt[t] = m_roof(t, CUR[t], ROOF_ROWS.get(t, use_rows[t]), other)
    rows = []
    for name, blocks in MOTIF_BLOCKS:
        rows.append((name, blocks, [("TODAY", CUR), ("PASS 2" + (", " + ROOF_STYLE if name == "blue house roof" else ""),
                                                      new_tiles)] +
                     ([("PASS 2, " + other, alt)] if name == "blue house roof" else [])))
    cell = 16 * Z + 6
    W = 16 + max(len(b) for _, b, _ in rows) * cell + 150
    H = 40 + sum(len(v) * (cell + 4) + 30 for _, _, v in rows)
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-438 C, second pass: the motifs, 4x   (DRAFT)", fill=(250, 214, 120), font=F)
    y = 36
    for name, blocks, versions in rows:
        dr.text((8, y), name + "   tiles " + " ".join(str(t) for t in MOTIF_TILES[name]), fill=(250, 214, 120), font=f2)
        y += 20
        for label, tl in versions:
            dr.text((8, y + 24), label, fill=(220, 220, 230), font=f2)
            for k, (ts, mid) in enumerate(blocks):
                im.paste(block_rgb(ts, mid, tl, Z), (150 + k * cell, y))
            y += cell + 4
        y += 10
    im.save(path)
    return path


def redraw2(t, px, rows, group, first, third=False):
    """pass 2 (or 3) over pass 1: px is vanilla's tile, first is pass 1's drawing of it. A motif is drawn whole; rock
    is redrawn as stone, and everything else in the tile keeps pass 1"""
    if t in MOTIFS:
        return MOTIFS[t](t, px, rows)
    if group in ("cliffs", "ledges", "water", "anim"):
        r = (redraw_rock3 if third else redraw_rock)(t, px, rows)
        if r is not None:
            return [r[i] if px[i] in ROCK_RAMP else first[i] for i in range(64)]
    return first


ROOF_ROWS = {}


def prepare():
    use, nlay, mt_seen = scan()
    USE.update(use)
    for t in ROOFS:
        if t in use:
            ROOF_ROWS[t] = use[t]["rows"]
    for t, u in use.items():
        qs = set(u["quads"])
        if len(qs) == 1 and next(iter(qs))[1] == 0:
            q = next(iter(qs))[0]
            QUARTER[t] = ((q % 2) * 8, (q // 2) * 8)
            gb = [b for b in u["blocks"].most_common() if b[0][0] == "general"]
            bl = gb and block_layer(GMT, gb[0][0][1], t, CUR)
            if bl:
                BLOCK_OF[t] = bl
    place_quarters(use)
    find_fills()
    return use, nlay, mt_seen


def build(use, vanilla, second, third=False):
    """(by_group, new_tiles, strips, notes) for pass 1, or with second for pass 2 (and third for pass 3)"""
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
            if second:
                new = redraw2(t, CUR[t], u["rows"], g, new, third)
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
                if second:
                    new = redraw2(it["tile"], px, use[it["tile"]]["rows"], "anim", new, third)
                put_tile(frames[f], k, new)
                if f == 0:
                    it["new"] = new
                    it["van"] = px
                    it["cur"] = px
                    new_tiles[it["tile"]] = new
                    all_notes += ["%d: %s" % (it["tile"], x) for x in notes]
        strips[strip] = frames
    return by_group, new_tiles, strips, all_notes


def save_draft(new_tiles, strips, d):
    os.makedirs(d, exist_ok=True)
    out = CUR_IM.copy()
    p = out.load()
    for t in range(640):
        if new_tiles[t] != CUR[t]:
            for i, v in enumerate(new_tiles[t]):
                p[(t % 16) * 8 + i % 8, (t // 16) * 8 + i // 8] = v
    path = os.path.join(d, "tiles.png")
    out.save(path)
    for strip, frames in strips.items():
        sd = os.path.join(d, "anim", strip)
        os.makedirs(sd, exist_ok=True)
        for f, im in enumerate(frames):
            im.save(os.path.join(sd, "%d.png" % f))
    return path


def main():
    if WRITE and "--approved" not in ARGS:
        print("  --write refused: T-438 batch C is a draft until the user has approved its sheets.")
        print("  (When they have: --write --approved writes pass 3's tiles into %s/tiles.png and the two water-edge" % G)
        print("   strips into its anim/, overwriting only tiles that are still vanilla.)")
        return 0

    use, nlay, mt_seen = prepare()
    drawn = [t for t in range(640) if t in use and any(CUR[t])]
    vanilla = [t for t in drawn if CUR[t] == VAN[t]]
    print("  scanned %d layouts on General; %d of its tiles are drawn, %d of them still vanilla" %
          (nlay, len(drawn), len(vanilla)))

    by_group1, new1, strips1, _ = build(use, vanilla, False)
    by_group2, new2, strips2, _ = build(use, vanilla, True)
    by_group, new_tiles, strips, all_notes = build(use, vanilla, True, True)     # pass 3: the candidate

    order = [k for k, _, _ in GROUPS]
    print("  %-10s %5s %6s %6s %6s %8s  %-28s %s" % ("group", "tiles", "pass1", "pass2", "pass3", "maps", "first seen",
                                                    "what"))
    for g in order:
        items = by_group.get(g, [])
        if not items:
            continue
        base = lambda it: it.get("van") or CUR[it["tile"]]
        n1 = sum(1 for it in by_group1[g] if it["new"] != base(it))
        n2 = sum(1 for it in by_group2[g] if it["new"] != base(it))
        n3 = sum(1 for it in items if it["new"] != base(it))
        maps = set(m for it in items for m in it["maps"])
        firsts = sorted((it for it in items if it["first"]), key=lambda it: -len(it["maps"]))
        print("  %-10s %5d %6d %6d %6d %8d  %-28s %s" % (g, len(items), n1, n2, n3, len(maps),
                                                      firsts[0]["first"] if firsts else "-", TITLE[g]))
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

    os.makedirs(SHEETS, exist_ok=True)
    save_draft(new1, strips1, os.path.join(DRAFT, "pass1"))
    save_draft(new2, strips2, os.path.join(DRAFT, "pass2"))
    save_draft(new_tiles, strips, DRAFT)
    print("  measuring seams over every block pair the maps place ...")
    seams1 = seam_measure(new1, mt_seen)
    seams2 = seam_measure(new2, mt_seen)
    seams = seam_measure(new_tiles, mt_seen)
    for name, sm in (("pass 1", seams1), ("pass 2", seams2), ("pass 3", seams)):
        print("  seams, %s: %d block pairs and joints, %d pixel pairs across them; %d opened, %d closed" %
              (name, sm["pairs"], sm["pixel_pairs"], sm["opened"], sm["closed"]))
    for k, n in seams["worst"]:
        print("    %-40s %d" % (k, n))
    groups = {g: [{k: it[k] for k in ("tile", "nmaps", "first", "blocks", "draws")} | {"row": list(it["key"]),
                   "changed": it["new"] != (it.get("van") or VAN[it["tile"]]), "motif": it["tile"] in MOTIFS}
                  for it in by_group.get(g, [])]
              for g in order}
    json.dump({"pass": 3, "groups": groups, "titles": TITLE, "notes": all_notes, "seams": seams, "seams_pass1": seams1,
               "seams_pass2": seams2, "roof": ROOF_STYLE,
               "motifs": MOTIF_TILES, "recolour": RECOLOUR_REPORT()},
              open(os.path.join(DRAFT, "groups.json"), "w"), indent=1, sort_keys=True)
    names = []
    for g in order:
        items = by_group.get(g, [])
        if not items or g == "flat":
            continue
        for part in range(0, len(items), 60):
            names.append(group_sheet(g, items[part:part + 60], 4,
                                     os.path.join(SHEETS, "t438c3_ground_%s%s.png" % (g, "" if part == 0 else "_%d" % (part // 60 + 1)))))
    versions = [("TODAY", CUR, None, None), ("PASS 2", new2, strips2, None), ("PASS 3", new_tiles, strips, None)]
    for k, crop in enumerate(MAP_CROPS3):
        names.append(map_sheet2(crop, versions, os.path.join(SHEETS, "t438c3_maps_%d.png" % (k + 1)), "third"))
    names.append(kit_sheet([("TODAY", CUR), ("PASS 2", new2), ("PASS 3", new_tiles)],
                           os.path.join(SHEETS, "t438c3_rock_kit.png")))
    names.append(motif_sheet(new_tiles, os.path.join(SHEETS, "t438c3_motifs.png")))
    print("  drafts in %s (pass 1 in pass1/, pass 2 in pass2/); sheets:\n    %s" % (DRAFT, "\n    ".join(names)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

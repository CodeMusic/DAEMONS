#!/usr/bin/env python3
"""A look per cave (T-438 batch E): each cave's secondary tileset redrawn in code, matched to its name.

    python3 tools/gbacaves.py                       # report: every cave-like tileset, the maps that use it, their
                                                    #   DAEMONS names, the look proposed for each, what is drafted
    python3 tools/gbacaves.py --draft [DIR]         # the drafted caves' tiles.png and palettes, groups.json, and the
                                                    #   contact sheets, in DIR (gfx/drafts/t438/caves/); --sheets DIR
                                                    #   puts the sheets elsewhere
    python3 tools/gbacaves.py --write --approved    # into the engine: every cave the user approved (batch E's three
                                                    #   and E2's eight, 2026-10-23): tiles.png and the rows each look
                                                    #   changes; the three palette splits' rows 7..12 beside their base
                                                    #   (UMBRAL ASCENT, STILLFALL, and OTHER CAVE's four lights). The
                                                    #   splits' Tileset headers and OTHER CAVE's cycle are engine code
                                                    #   (headers.h, graphics.h, fieldmap.c). Without --approved it refuses.

THE ANSWER IT FOLLOWS (the user, 2026-10-22): "a look per cave, matched to its name and what it is". A cave is a
secondary tileset over primary/general, and several maps can share one (DEADSTACK, UMBRAL ASCENT, THE WRONG WAY and
the THREE ISLE PATH tunnel all draw gTileset_Cave), so a look belongs to a TILESET, and a cave that shares one shares
its look unless it is split. A split can be cheap: a Tileset header is four pointers, so a new header that reuses
gTilesetTiles_Cave and its metatiles with palettes of its own costs 192 bytes and no tiles (a "palette split").

T-125's rule holds here as everywhere: nothing moves a block, a layer, a flip, a palette row, a behaviour or a
collision bit, and no map is touched. Only the pixels inside tiles and the colours of the secondary's rows 8..12
change, and every tile keeps its FOOTPRINT -- a pixel that was transparent (index 0) stays transparent, one that was
drawn stays drawn -- and its SILHOUETTE: a pixel of one material that touches another material (in its block) keeps
vanilla's index, so every join between a wall and the floor, a ledge and its lip, a ladder and the rock it is set in,
is vanilla's and agrees with the tile beside it.

HOW IT IS DRAWN, the lessons of batches C and D: bold forms that read at 1x, never speckle; and draw by ROLE, so the
palettes can follow. Every index of every row is given a MATERIAL (floor, rock, sand, wood, water, hole, dark, the
accents) and a rank within it, light to dark. A tile's rock is re-cut by batch C's method (gbageneral.py
redraw_rock3), read in the block that draws it most so the light runs on across tile edges: each pixel's BASE is
vanilla's own light around it, so a wall keeps its lit top and its shaded face where vanilla had them, and which
side of TOP_AT that light falls (top or face) picks the motif's top or face pattern; the MOTIF, a 16x16 pattern laid
at the tile's place in its block (a block is the motif's period, so it runs on across blocks), gives each pixel a
role -- lit edge, body, underside, crack -- as an offset from its base. The floor is re-cut the same way with a few
bold marks, and vanilla's shadow under a wall is kept. Boulders, breakable rocks, ladders, holes and water keep
their drawing (OBJECTS) and only take the new colours. Each cave's MOTIF is its one idea; its PALETTE is its light.

THE GREY RULE IS NOT OURS TO TOUCH. HALFTONE is grey, and the unread DOLDRUM CAVE is "the second grey place" (vision
8.6a, T-251) -- DaemonsIsHalftone() greys gPlttBufferFaded once a frame, whatever the tileset's palettes are. So no
cave here may be grey (THE BLACKOUT is dark and cold, never grey), and DOLDRUM CAVE's tileset is not drafted at all:
its look waits on the user, and whatever it becomes, the unread state greys it on top.

BATCH E2 (the rest, after the user approved the first three on 2026-10-23): UMBRAL ASCENT and OTHER CAVE as palette
splits over the stack and the outage, STILLFALL as one over GLAUCOUS ISLES' bloom; THE TUNNEL and the KEEPALIVE PLANT
(built rooms over primary/building, drawn by draw_tunnel and draw_plant); GLAUCOUS ISLES, MT. SMOULDER and THE DOTS
(the cave method, each with its own index plan). TANOBY waits for batch G and DOLDRUM CAVE for the user.
"""
import collections, io, json, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import read_pal, write_pal
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t438", "caves")
GEN = "data/tilesets/primary/general"
SEC = "data/tilesets/secondary/"

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


# ================================================================== the proposal
#  tileset -> its places. Names are the mapsecs' (region_map_sections.json); meanings are the bible's (vision.md
#  3.2's table and 3.3, the KEEPALIVE section, 2.10's island table, 8.6a / T-251 for DOLDRUM). `order` is where a
#  player first meets it (the census's rank). `drafted` marks what is drawn; `drafted_e2`, what batch E2 added.
PROPOSAL = [
    dict(ts="cave", order=8, drafted=True,
         places=[("DEADSTACK", "MtMoon_1F/B1F/B2F", "Mt. Moon: a mountain of dead hardware; its fossils are legacy "
                  "silicon (3.2)"),
                 ("THREE ISLE PATH", "ThreeIsland_DunsparceTunnel", "a short tunnel; no name of its own"),
                 ("UMBRAL ASCENT", "VictoryRoad_1F/2F/3F", "Victory Road: the climb into partial shadow toward UMBRA"),
                 ("THE WRONG WAY", "FiveIsland_LostCave x15", "Lost Cave: named by somebody who took it (2.10)")],
         look="THE STACK. The rock is dead hardware piled up: every face reads as thin courses of slab -- boards, "
              "drives, casings -- laid one on another, every other one a shade darker, a joint here and there; one "
              "course a block carries a strip of tarnished gold: an edge connector. A ridge's top is the top board, "
              "seamed once a block. Light: dull sage and solder-mask green; the floor is ash-brown grit with a chip "
              "of board lying in it (ROUTE 3 is ASHFALL); the bright floor patches become pale drifts.",
         split="SPLIT UMBRAL ASCENT (palette split now: a cold violet dusk, the same courses; its own tiles in batch "
               "G). THE WRONG WAY and the tunnel can keep the stack."),
    dict(ts="digletts_cave", order=19, drafted=True,
         places=[("TAPPOINT'S CAVE", "DiglettsCave_B1F + N/S entrances", "TAPPOINT (Diglett) 'sits under the route "
                  "everything takes and reads what goes past' -- a wiretap's burrow"),
                 ("TANOBY KEY", "SevenIsland_SevaultCanyon_TanobyKey", "one small room (LONG DROP's)")],
         look="THE LINE. A long burrow of warm packed earth under the routes, and along the top of every cut runs "
              "the buried cable it was dug to reach: a red sheath over a dark core, two pixels deep, following the "
              "cut wherever it turns. The faces are packed clods; the ground above is calm earth with soft rises; "
              "TAPPOINT's holes are kept. Light: umber and ochre; the cable is the one colour that is not earth.",
         split="No split: TANOBY KEY is one room and an earth room suits it."),
    dict(ts="rock_tunnel", order=22, drafted=True,
         places=[("THE BLACKOUT", "RockTunnel_1F/B1F (FLASH-dark)", "'No light, no color, no context' (3.2); next "
                  "door to the KEEPALIVE PLANT, so ROUTE 10 signposts the blackout and the thing still running"),
                 ("OTHER CAVE", "SixIsland_AlteringCave", "Altering Cave: 'never holds the same thing twice' (2.10)")],
         look="THE OUTAGE. Basalt that grew in the dark: the walls are tall columns, cut vertically (the stack runs "
              "across; this runs down), each column a lit left edge and a dark right one. Light: night indigo and "
              "blue-black, deep but never grey -- HALFTONE and the unread DOLDRUM own grey. VERBOSE (FLASH) shows it; "
              "unlit it is a 24-pixel circle in black.",
         split="SPLIT OTHER CAVE (palette split): the same columns in a palette that is not THE BLACKOUT's -- a "
               "pale mineral teal. A per-entry palette swap would make it never the same twice: described (how, cost, risks) in --draft's "
               "groups.json, not built; that is the user's question."),
    dict(ts="underground_path", drafted=True, order=14, drafted_e2=True,
         places=[("UNDERGROUND PATH", "UndergroundPath_NorthSouth/EastWest", "officially UNDERGROUND PATH, locally "
                  "THE TUNNEL: routing around a blocked path, as a VPN does (3.1)")],
         look="THE TUNNEL. Not a cave but a built bore: a concrete tube with a lit lane down the middle, conduit along "
              "both walls, a dashed centre line like a packet trace. Light: sodium-free white and cool concrete, the "
              "most ordered underground in the game, so the caves read as caves beside it.",
         split="Its own tileset already; it draws primary/building (batch D's palettes sit under it)."),
    dict(ts="power_plant", drafted=True, order=23, drafted_e2=True,
         places=[("KEEPALIVE PLANT", "PowerPlant", "a building still running with nobody connected to it; SENTINEL "
                  "lives there (3.3)")],
         look="STILL RUNNING. A plant left on: floor plates and machine housings, and the one motif is a status light "
              "on every housing, all green. Light: plant-green and machine grey-blue, with the living PLANT's second "
              "meaning in moss along the seams.",
         split="Its own tileset; batch D left its machines for this batch or its town's."),
    dict(ts="seafoam_islands", drafted=True, order=44, drafted_e2=True,
         places=[("GLAUCOUS ISLES", "SeafoamIslands_1F..B4F", "Seafoam: named for its surface, and what matters is "
                  "four floors under it (3.3)"),
                 ("STILLFALL CAVE", "FourIsland_IcefallCave x4", "Icefall: a waterfall that stopped (2.10)"),
                 ("SEVEN ISLAND", "SevenIsland_House_Room1", "one room")],
         look="THE BLOOM. GLAUCOUS (our reading) is the powdery blue-green bloom on a plum or a leaf: ice under a matte "
              "frosted skin, lit tops chalky, faces clear and deep. Its rows 8..12 were already recoloured (census).",
         split="SPLIT STILLFALL (palette split): the ice gone glassy and still, frozen falls -- its own tiles later."),
    dict(ts="mt_ember", drafted=True, order=51, drafted_e2=True,
         places=[("MT. SMOULDER", "MtEmber_RubyPath/SummitPath x11", "burning without flame is what it does and what "
                  "it looks like from the sea (2.10)"),
                 ("KETTLE SPRING", "OneIsland_KindleRoad_EmberSpa", "Ember Spa")],
         look="EMBER UNDER ASH. Black cinder rock whose cracks glow a low orange from inside, never flame; the steam "
              "animation stays. Light: charcoal and banked-coal red.",
         split="KETTLE SPRING shares it; no split."),
    dict(ts="cerulean_cave", order=95, drafted=False,
         places=[("DOLDRUM CAVE", "CeruleanCave_1F/2F/B1F", "S.T.A.R.R. sleeps here; unread it is grey and wrongly "
                  "arranged, read it is itself, in colour (8.6a, T-251)")],
         look="BECALMED (the read state only). Still water and slack rock: horizontal tidelines on every wall, a calm "
              "green-blue. The unread state is not this batch's: DaemonsIsHalftone greys it whatever its palette is, "
              "and the rearrangement is the map's, not the tiles'.",
         split="Never drafted without the user: its grey and its 'itself' are a decided pair."),
    dict(ts="navel_rock", drafted=True, order=76, drafted_e2=True,
         places=[("THE DOTS", "SixIsland_DottedHole x6", "Dotted Hole: 'said by somebody who could see them and could "
                  "not read them' (2.10)"),
                 ("NAVEL ROCK", "NavelRock x20", "unnamed: no player of this game reaches it (2.10)")],
         look="BRAILLE. THE DOTS' walls carry raised dots in cells of six -- writing for the hand, unread by the eye. "
              "Light: sandstone and shadow. NAVEL ROCK is unreachable and can keep whatever THE DOTS gets.",
         split="No split needed: NAVEL ROCK is never reached."),
    dict(ts="tanoby_ruins", order=85, drafted=False,
         places=[("TANOBY CHAMBERS", "SevenIsland_TanobyRuins x7", "the chambers; vanilla's Unown walls")],
         look="An older script: the walls' glyphs redrawn as one of our own, carved, not lit. With batch G.",
         split="Its own tileset."),
]

# the three batch E drew first, first met first -- APPROVED by the user 2026-10-23, and the only ones --write writes.
# Batch E2 (the rest, DRAFTED_E2 below) is a draft until the user has seen its sheets.
DRAFTED = ["cave", "digletts_cave", "rock_tunnel"]


# ================================================================== reading the engine
def tiles_of(im):
    w, h = im.size
    px = im.tobytes()
    return [[px[(ty * 8 + r) * w + tx * 8 + c] & 15 for r in range(8) for c in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]


def entries(buf, i):
    return struct.unpack_from("<8H", buf, i * 16)


_LAYOUTS = None


def layouts():
    global _LAYOUTS
    if _LAYOUTS is None:
        _LAYOUTS = {l["name"][:-len("_Layout")]: l for l in
                    json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if "name" in l}
    return _LAYOUTS


_PRIMARY = {}
PRIMARY_DIR = {"gTileset_General": GEN, "gTileset_Building": "data/tilesets/primary/building"}


def general(name="gTileset_General"):
    """a primary tileset as the engine has it now (general, or building under THE TUNNEL and the KEEPALIVE PLANT):
    its tiles, rows 0..6, its metatiles"""
    if name not in _PRIMARY:
        d = os.path.join(GBA, PRIMARY_DIR[name])
        _PRIMARY[name] = dict(tiles=tiles_of(Image.open(os.path.join(d, "tiles.png"))),
                              pals=[read_pal(os.path.join(d, "palettes/%02d.pal" % r)) for r in range(16)],
                              mt=open(os.path.join(d, "metatiles.bin"), "rb").read())
    return _PRIMARY[name]


class Cave:
    """one secondary tileset: its tiles and palettes as they are now, and where each tile is drawn"""

    def __init__(self, ts):
        self.ts = ts
        self.dir = os.path.join(GBA, SEC + ts)
        self.im = Image.open(os.path.join(self.dir, "tiles.png"))
        self.now = tiles_of(self.im)
        #  every look draws over VANILLA's tile, never today's, so a second --write is a no-op (batch D's lesson)
        self.van = tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, SEC + ts + "/tiles.png", binary=True))))
        self.tiles = self.van
        self.pals = [read_pal(os.path.join(self.dir, "palettes/%02d.pal" % r)) for r in range(16)]
        self.mt = open(os.path.join(self.dir, "metatiles.bin"), "rb").read()
        self.attr = open(os.path.join(self.dir, "metatile_attributes.bin"), "rb").read()
        self.n = len(self.tiles)
        #  a palette split's maps draw these tiles too (UMBRAL ASCENT's draw the stack), so they count here
        own = {"gTileset_" + "".join(w.title() for w in ts.split("_"))} | \
              {SPLIT_SYMBOL[k] for k in SPLIT_SYMBOL if k.split("/")[0] == ts}
        self.maps = sorted(n for n, l in layouts().items()
                           if l["secondary_tileset"] in own
                           or l["secondary_tileset"].lower() == "gtileset_" + ts.replace("_", ""))
        self.use()

    def use(self):
        """tile -> palette rows (Counter), and its quarters in the blocks that draw it, weighted by placements"""
        self.rows = collections.defaultdict(collections.Counter)
        self.quads = collections.defaultdict(collections.Counter)
        place = collections.Counter()
        for m in self.maps:
            l = layouts()[m]
            d = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
            for k in range(len(d) // 2):
                place[struct.unpack_from("<H", d, k * 2)[0] & 0x3FF] += 1
        self.placed = place
        for b in range(len(self.mt) // 16):
            w = place.get(640 + b, 0) + 1                  # a block no map places still counts once
            for j, v in enumerate(entries(self.mt, b)):
                t = v & 0x3FF
                if t < 640:
                    continue
                t -= 640
                self.rows[t][v >> 12] += w
                q = j % 4
                self.quads[t][((q % 2) * 8, (q // 2) * 8, (v >> 10) & 3)] += w

    def home(self, t):
        return self.rows[t].most_common(1)[0][0] if self.rows[t] else None

    def quarter(self, t):
        """(x, y) offset of the tile in its 16x16 block-cell, when its main placement is unflipped; else (0, 0)"""
        if not self.quads[t]:
            return (0, 0), 0
        (x, y, f), _ = self.quads[t].most_common(1)[0]
        return (x, y), f


def render(cave, mapname, tiles=None, pals=None, box=None):
    """a map (or a box of it, in cells) as the screen draws it, the secondary's tiles and rows from `tiles`/`pals`"""
    l = layouts()[mapname]
    G = general(l["primary_tileset"])
    tl = tiles or cave.tiles
    sp = pals or cave.pals
    allp = [G["pals"][r] for r in range(7)] + [sp[r] for r in range(7, 16)]
    W, H = l["width"], l["height"]
    d = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    x0, y0, w, h = box or (0, 0, W, H)
    w, h = min(w, W - x0), min(h, H - y0)
    img = Image.new("RGB", (w * 16, h * 16), allp[0][0])
    o = img.load()
    for yy in range(h):
        for xx in range(w):
            m = struct.unpack_from("<H", d, ((y0 + yy) * W + x0 + xx) * 2)[0] & 0x3FF
            buf, k = (G["mt"], m) if m < 640 else (cave.mt, m - 640)
            if (k + 1) * 16 > len(buf):
                continue
            e = entries(buf, k)
            for layer in (0, 1):
                for q in range(4):
                    v = e[layer * 4 + q]
                    t, row = v & 0x3FF, v >> 12
                    src = G["tiles"][t] if t < 640 else (tl[t - 640] if t - 640 < len(tl) else [0] * 64)
                    for ty in range(8):
                        for tx in range(8):
                            sx = 7 - tx if v & 0x400 else tx
                            sy = 7 - ty if v & 0x800 else ty
                            c = src[sy * 8 + sx]
                            if c == 0:
                                continue
                            o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = allp[row][c]
    return img


# ================================================================== the looks, by role
#  MATERIALS: per palette row, index -> (material, rank light..dark). The three drafted tilesets share vanilla's
#  layout -- the same tile numbers carry the same objects in each (ladders 6..13/22..29, the ladder holes in row 10,
#  the floor patches in row 11) -- and close to the same index plan: row 8 is the floor (1..4) and the rock (9..14);
#  row 9 the ladders (5..10) and water (13..15); row 10 the holes and their rungs; row 11 the floor's patches.
#  Indices not named here (the outlines, the holes' black, 15's cast shade) are never redrawn: they keep vanilla's
#  pixels and take the new palette's colour for their role.
def _plan(floor, rock, extra=None):
    m = {i: ("floor", k) for k, i in enumerate(floor)}
    m.update({i: ("rock", k) for k, i in enumerate(rock)})
    m.update(extra or {})
    return m


ROCK = list(range(9, 15))
MATERIALS = {
    "cave": {8: _plan([1, 2, 3, 4], ROCK, {5: ("dark", 0), 15: ("shade", 0)}),
             9: _plan([1, 2, 3, 4], [], {5: ("wood", 0), 6: ("wood", 1), 7: ("wood", 2), 8: ("wood", 3),
                                         9: ("wood", 4), 10: ("wood", 5), 11: ("dark", 1), 12: ("hole", 0),
                                         13: ("water", 0), 14: ("water", 1), 15: ("water", 2)}),
             10: _plan([], ROCK, {4: ("hole", 0), 5: ("rung", 0), 6: ("rung", 1), 7: ("rung", 2), 8: ("rung", 3),
                                  15: ("shade", 0)}),
             11: _plan([1, 2, 3, 4], [], {12: ("patch", 0), 13: ("patch", 1), 14: ("patch", 2), 15: ("patch", 3)}),
             12: {15: ("hole", 0)}},
}
MATERIALS["digletts_cave"] = {r: dict(v) for r, v in MATERIALS["cave"].items()}
MATERIALS["digletts_cave"][9] = _plan([1, 2, 3, 4], [], {5: ("wood", 0), 6: ("wood", 1), 7: ("wood", 3),
                                                         8: ("wood", 5), 11: ("dark", 1), 12: ("hole", 0),
                                                         13: ("water", 0), 14: ("water", 1), 15: ("water", 2)})
MATERIALS["digletts_cave"][12] = _plan([], ROCK, {5: ("rung", 0), 6: ("rung", 1), 7: ("rung", 2), 8: ("rung", 3),
                                                  15: ("shade", 0)})
MATERIALS["rock_tunnel"] = {r: dict(v) for r, v in MATERIALS["cave"].items()}
MATERIALS["rock_tunnel"][8] = _plan([1, 2, 3, 4], ROCK, {5: ("floor", 4), 15: ("shade", 0)})
MATERIALS["rock_tunnel"][11] = _plan([2, 3], [], {13: ("patch", 0), 14: ("patch", 1), 15: ("patch", 2)})

#  ACCENT: the indices a row leaves free (magenta in vanilla), which a look may use for its motif's one colour.
#  A tile drawn in more than one row takes an accent only if every one of its rows has it free.
ACCENT = {"cave": {8: [6, 7, 8]}, "digletts_cave": {8: [6, 7, 8]}, "rock_tunnel": {}}     # THE BLACKOUT has none

#  OBJECTS: the tiles that are things standing on the floor rather than the cave itself -- boulders, the breakable
#  rocks, the pebble clusters. Vanilla's drawing of each is kept and only recoloured: a STRENGTH boulder has to read
#  as one, and its shape is what a player knows it by. (The same tile numbers in all three drafted tilesets.)
OBJECTS = {3, 4, 19, 20, 108, 109, 124, 125, 110, 111, 126, 127, 140, 141, 142, 143, 158, 159, 174, 175,
           226, 227, 228, 229, 242, 243, 244, 245}

#  A rock pixel's BASE is vanilla's own light around it (the mean rank of the rock within two pixels), so a wall keeps
#  its lit top and its shaded face exactly where vanilla had them; its PLANE (top or face) is which side of TOP_AT
#  that light falls, and chooses the motif's top or face pattern. The motif then gives each pixel a ROLE, an offset
#  from its base: lit edge -1, body 0, shaded underside +1, crack +2 (+1 on a top, where a seam is shallower), plus
#  a SHIFT for a course or a column that is a board darker than the one beside it.
TOP_AT = 2.25                                        # the valley between tops and faces in all three
ROLE_OFF = {"hi": -1, "body": 0, "lo": 1, "crack": 2}


def _torus(fn):
    return [[fn(x, y) for x in range(16)] for y in range(16)]


def _voronoi(seeds):
    lab = [[0] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            best = None
            for k, (a, b, w) in enumerate(seeds):
                dx = (x + 0.5 - a + 8) % 16 - 8
                dy = (y + 0.5 - b + 8) % 16 - 8
                d = (dx * dx + dy * dy) ** 0.5 - w
                if best is None or d < best[0]:
                    best = (d, k)
            lab[y][x] = best[1]
    return lab


def _lumps(lab):
    """each mass of a label field shaded as a lump: lit top and left, body, shaded foot, dark crack under it"""
    crack = [[any(lab[y][x] < lab[(y + v) % 16][(x + u) % 16] for u, v in ((1, 0), (0, 1), (-1, 0), (0, -1)))
              for x in range(16)] for y in range(16)]
    same = lambda x, y, k: lab[y % 16][x % 16] == k and not crack[y % 16][x % 16]
    out = [[None] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            k = lab[y][x]
            if crack[y][x]:
                out[y][x] = "crack"
            elif not same(x, y + 1, k):
                out[y][x] = "lo"
            elif not same(x, y - 1, k) or not same(x - 1, y, k):
                out[y][x] = "hi"
            else:
                out[y][x] = "body"
    return out


# ---------------------------------------------------------------- DEADSTACK: the stack
#  Down a face, thin COURSES of slab -- boards, drives, casings -- 3/4/2/4/3 pixels deep, every other one a shade
#  darker, so the wall reads as things laid one on another rather than as masonry; a joint here and there, never
#  lined up. One course in each block carries a run of PINS in tarnished gold along its middle: dead boards, still
#  with their contacts. Across a top, the top slab seen from above: one plate a block, lit at its back edge, seamed
#  at its front -- so a ridge seen from above is layered too.
COURSES = [(0, 3, (6,), 0), (3, 4, (13,), 1), (7, 2, (), 0), (9, 4, (2, 10), 1), (13, 3, (8,), 0)]
PINS = (10, range(3, 10))                                 # row, x run: an edge connector, one gold strip


def _course(x, y):
    for top, h, joints, shift in COURSES:
        if top <= y < top + h:
            k = y - top
            if k == h - 1 or x in joints:
                return "crack", shift
            if k == 0 or (x - 1) % 16 in joints:
                return "hi", shift
            if k == h - 2 and h >= 4:
                return "lo", shift
            if y == PINS[0] and x in PINS[1]:
                return "accent0", shift
            return "body", shift


def _plate(x, y):
    if y == 15:
        return "crack", 0
    if y == 0:
        return "hi", 0
    if y == 14:
        return "lo", 0
    return "body", 0


STACK_FACE, STACK_TOP = _torus(_course), _torus(_plate)


def m_stack(X, Y, plane):
    return (STACK_TOP if plane == "top" else STACK_FACE)[Y][X]


# ---------------------------------------------------------------- TAPPOINT'S CAVE: the line
#  Packed earth in a few big soft clods; and along the top of every cut, where the burrow's wall meets the ground
#  above it, a buried CABLE laid bare: a lit sheath over a dark core, two pixels deep, following the cut wherever it
#  turns (redraw() finds that rim; the motif only says the cave has one).
CLODS = _lumps(_voronoi([(4.0, 4.5, 3.4), (12.5, 3.5, 2.0), (9.5, 11.5, 3.6), (1.0, 12.5, 1.0)]))


def m_line(X, Y, plane):
    if plane == "top":                                    # the ground above is only earth: two soft rises a block
        return TOP_EARTH[Y][X] or "body", 0
    return CLODS[Y][X], 0


# ---------------------------------------------------------------- THE BLACKOUT: the outage
#  Basalt, which forms where rock cools in the dark. Down a face, COLUMNS 4/5/3/4 wide: a lit left edge, the body, a
#  dark right edge and a crack, each column broken once by a joint at its own height and every other one a shade
#  darker. Across a top, the columns end-on: blocky cells, each lit on its upper left.
COLUMNS = [(0, 4, 3, 0), (4, 5, 10, 1), (9, 3, 6, 0), (12, 4, 13, 1)]     # x0, width, joint row, shift


def _basalt(x, y):
    for x0, w, j, shift in COLUMNS:
        if x0 <= x < x0 + w:
            k = x - x0
            if k == w - 1 or y == j:
                return "crack", shift
            if k == 0 or y == (j + 1) % 16:
                return "hi", shift
            if k == w - 2 and w >= 4:
                return "lo", shift
            return "body", shift


BASALT = _torus(_basalt)
ENDS = _lumps(_voronoi([(3.5, 3.5, 0.5), (11.5, 3.0, 0.5), (7.5, 11.0, 0.5), (15.5, 11.5, 0.5)]))


def m_outage(X, Y, plane):
    if plane == "top":
        r = ENDS[Y][X]
        return {"crack": "lo", "lo": "body"}.get(r, r), 0
    return BASALT[Y][X]


# ---------------------------------------------------------------- the floors
#  A floor is its field rank with a few BOLD marks laid on it -- never a speckle: each mark a lit row, a body, a
#  shaded row, in a 16x16 torus. Offsets from the field rank, per look.
def _marks(rects):
    g = [[None] * 16 for _ in range(16)]
    for x0, y0, w, h in rects:
        for dy in range(h):
            for dx in range(w):
                g[(y0 + dy) % 16][(x0 + dx) % 16] = "hi" if dy == 0 else "lo" if dy == h - 1 else "body"
    return g


TOP_EARTH = _marks([(2, 3, 6, 3), (10, 10, 5, 3)])
FLOOR_GRIT = _marks([(3, 3, 3, 2), (11, 11, 2, 2)])                          # a chip of board lying in the ash
FLOOR_EARTH = _marks([(1, 2, 6, 3), (10, 10, 5, 3)])                         # tamped earth: two clods a block
FLOOR_SLATE = [[None] * 16 for _ in range(16)]                               # slate, two short fractures a block
for _x, _y in ((1, 5), (2, 5), (3, 6), (4, 6), (5, 6), (6, 5), (9, 12), (10, 12), (11, 11), (12, 11), (13, 11)):
    FLOOR_SLATE[_y][_x] = "crack"
MARK_OFF = {None: 0, "hi": -1, "body": -1, "lo": 1, "crack": 1}
CRACK_OFF = {None: 0, "hi": 0, "body": 0, "lo": 0, "crack": 1}


#  PALETTES by role, light to dark. Every look keeps vanilla's VALUE structure -- the floor sits between a wall's lit
#  top and its face, so a cave reads the same way to the eye that learned vanilla's -- and changes the hue, the
#  saturation and the one accent. Nothing here is grey: HALFTONE and the unread DOLDRUM own grey.
LOOKS = {
    "cave": dict(
        name="DEADSTACK", motif="the stack", rock=m_stack, rim=None, floor=FLOOR_GRIT, field=2, off=MARK_OFF,
        patch_field=1,
        pal={"floor": [(178, 170, 140), (152, 144, 118), (126, 120, 98), (98, 94, 78)],
             "rock": [(208, 218, 188), (172, 190, 160), (134, 158, 132), (98, 126, 104), (66, 92, 78), (40, 60, 54)],
             "dark": [(28, 40, 38), (58, 62, 52)], "shade": [(70, 78, 72)], "hole": [(8, 14, 14)],
             "wood": [(232, 234, 216), (206, 210, 190), (176, 182, 164), (146, 152, 138), (112, 118, 108),
                      (80, 86, 80)],
             "rung": [(232, 234, 216), (196, 202, 184), (156, 162, 148), (118, 124, 114)],
             "water": [(104, 150, 168), (78, 122, 146), (58, 98, 124)],
             "patch": [(210, 208, 172), (192, 190, 152), (174, 172, 136), (156, 154, 122)],
             "accent": [(222, 184, 88), (150, 116, 56), (184, 110, 70)]}),
    "digletts_cave": dict(
        name="TAPPOINT'S CAVE", motif="the line", rock=m_line, rim=("accent1", "accent0"), floor=FLOOR_EARTH, field=2,
        off=MARK_OFF,
        patch_field=1,
        pal={"floor": [(200, 154, 104), (174, 128, 82), (146, 102, 64), (114, 76, 46)],
             "rock": [(230, 198, 140), (204, 170, 112), (172, 138, 90), (138, 106, 68), (100, 74, 50), (64, 46, 34)],
             "dark": [(40, 30, 26), (66, 52, 44)], "shade": [(60, 46, 40)], "hole": [(12, 8, 6)],
             "wood": [(214, 168, 108), (188, 140, 84), (164, 118, 70), (140, 98, 58), (112, 78, 46), (84, 58, 36)],
             "rung": [(226, 186, 128), (196, 154, 98), (164, 124, 76), (128, 94, 58)],
             "water": [(98, 132, 150), (76, 108, 128), (58, 86, 108)],
             "patch": [(222, 194, 138), (206, 174, 116), (188, 154, 98), (170, 134, 82)],
             "accent": [(34, 30, 34), (196, 84, 60), (220, 150, 84)]}),
    "rock_tunnel": dict(
        name="THE BLACKOUT", motif="the outage", rock=m_outage, rim=None, floor=FLOOR_SLATE, field=1,
        off=CRACK_OFF,
        patch_field=0,
        pal={"floor": [(96, 102, 134), (80, 86, 118), (66, 70, 102), (52, 56, 86), (40, 42, 70)],
             "rock": [(140, 146, 192), (112, 118, 166), (88, 92, 140), (66, 70, 114), (48, 50, 90), (32, 32, 66)],
             "dark": [(18, 18, 38), (30, 30, 54)], "shade": [(24, 24, 46)], "hole": [(4, 4, 12)],
             "wood": [(176, 182, 206), (150, 156, 186), (126, 132, 164), (104, 108, 142), (82, 86, 120),
                      (60, 62, 96)],
             "rung": [(176, 182, 206), (146, 152, 184), (116, 120, 156), (88, 92, 128)],
             "water": [(58, 86, 140), (44, 68, 118), (32, 52, 96)],
             "patch": [(58, 60, 96), (50, 52, 86), (40, 42, 74)],
             "accent": []}),
}


# ================================================================== batch E2: the rest of the caves
#  The user approved DEADSTACK, TAPPOINT'S CAVE and THE BLACKOUT on 2026-10-23 and asked for the rest of the
#  proposal: UMBRAL ASCENT and OTHER CAVE with palettes of their own, then the KEEPALIVE PLANT, GLAUCOUS ISLES (and
#  STILLFALL), MT. SMOULDER, THE DOTS and THE TUNNEL. TANOBY (batch G) and DOLDRUM CAVE (the user's call) are not here.
#
#  seafoam_islands, mt_ember and navel_rock are cut from the same vanilla layout as cave -- ladders at 6..13/22..29,
#  holes at 14/15, boulders at 3/4/19/20 -- so they take the same method with their own index plans. power_plant and
#  underground_path are built rooms over primary/building, not caves: each is drawn by its own function (BUILT).
#
#  A PALETTE SPLIT is a look with `base`: it draws nothing, reuses the base look's tiles, and only gives the tileset's
#  rows a light of its own (UMBRAL ASCENT over the stack; OTHER CAVE over the outage; STILLFALL over the bloom).

#  GLAUCOUS ISLES (seafoam_islands). Row 8: floor 1..4; the ice 9 8 10 11 12 13 14 light to dark, 15 its outline;
#  5..7 the bright glints of the slides. Row 10 repeats row 8's ice; row 11 carries the slides' water (8..12, kept),
#  the glints and the moss (13, 14). The ladders keep vanilla's gold: a ladder is a thing the player looks for.
_ICE = {9: ("rock", 0), 8: ("rock", 1), 10: ("rock", 2), 11: ("rock", 3), 12: ("rock", 4), 13: ("rock", 5),
        14: ("rock", 6), 15: ("shade", 0)}
_GLINT = {5: ("glint", 0), 6: ("glint", 1), 7: ("glint", 2)}
MATERIALS["seafoam_islands"] = {
    8: {**_plan([1, 2, 3, 4], []), **_ICE, **_GLINT},
    9: _plan([1, 2, 3, 4], []),
    10: dict(_ICE),
    11: {**_plan([1, 2, 3, 4], []), **_GLINT, 13: ("patch", 0), 14: ("patch", 1)},
}
#  MT. SMOULDER (mt_ember): cave's plan in rows 8..10; rows 7 and 12 are the same rock a step and two steps deeper
#  (the lower floors), row 11 the pale ground round KETTLE SPRING (12..15; the steam animation draws 12 and 13, so 12
#  stays the lighter). Row 12's 1 and 2 are the spring's water, kept.
_EMBER_ROCK = _plan([], ROCK, {15: ("shade", 0)})
MATERIALS["mt_ember"] = {
    7: dict(_EMBER_ROCK),
    8: _plan([1, 2, 3, 4], ROCK, {15: ("shade", 0)}),
    9: _plan([1, 2, 3, 4], []),
    10: dict(_EMBER_ROCK),
    11: _plan([1, 2, 3, 4], [], {12: ("patch", 0), 13: ("patch", 1), 14: ("patch", 2), 15: ("patch", 3)}),
    12: dict(_EMBER_ROCK),
}
#  THE DOTS (navel_rock): row 8's floor is 2..4 (5, vanilla's worn spots, takes 4's colour), its rock 9/10 (both
#  white) then 11..15; rows 7 and 12 the same
#  rock in other light (row 12 is NAVEL ROCK's shadowed half); row 11's 12..15 the pale floor bands.
_SAND = {9: ("rock", 0), 10: ("rock", 0), 11: ("rock", 1), 12: ("rock", 2), 13: ("rock", 3), 14: ("rock", 4),
         15: ("rock", 5)}
MATERIALS["navel_rock"] = {
    7: {**_plan([2, 3, 4], []), 5: ("floor", 2), **_SAND},
    8: {**_plan([2, 3, 4], []), 5: ("floor", 2), **_SAND},
    9: _plan([2, 3, 4], []),
    10: {8: ("floor", 0), **_SAND},
    11: _plan([2, 3, 4], [], {12: ("patch", 0), 13: ("patch", 1), 14: ("patch", 2), 15: ("patch", 3)}),
    12: {**_plan([2, 3, 4], []), 5: ("floor", 2), **_SAND},
}
#  THE KEEPALIVE PLANT (power_plant): row 7 is the room -- plates (9, seams 11), corridors (8, seams 10), the housings'
#  body (10) and outlines (12, 13), the girders (4..6), the three conduit stripes (1 red, 2 green, 3 blue); 14 is
#  free and becomes the STATUS LIGHT. Row 8 is the coils and the drums: 1..3 their metal, 5 and 6 the lamp each
#  drum carries in its middle (vanilla's pink), which turns green.
_PLANT_ROOM = {1: ("conduit", 0), 2: ("conduit", 1), 3: ("conduit", 2), 4: ("girder", 2), 5: ("girder", 1),
               6: ("girder", 0), 7: ("trim", 0), 8: ("lane", 0), 9: ("plate", 0), 10: ("housing", 1),
               11: ("plate", 1), 12: ("housing", 3), 13: ("housing", 2), 14: ("status", 0)}
MATERIALS["power_plant"] = {
    7: dict(_PLANT_ROOM),
    8: {1: ("coil", 2), 2: ("coil", 1), 3: ("coil", 0), 5: ("status", 0), 6: ("status", 1), 10: ("housing", 1),
        11: ("plate", 1), 12: ("housing", 3), 13: ("housing", 2)},
}
#  THE TUNNEL (underground_path): row 7 is the whole bore -- the walls (6 lit, 3, 5, 2, 1 the outline), the floor's
#  planks (8 lit edge, 7, 9 the joint), and the two coloured bands vanilla runs down it: teal (11, 10, 12) becomes the
#  LIT LANE, red (14, 13, 15) the lane with the PACKET TRACE on it, whose dashes take 4, which row 7 never draws.
#  Row 8 is the ceiling lamps: 4..8 their glass and glow.
_TUNNEL_BORE = {6: ("wall", 0), 3: ("wall", 1), 5: ("wall", 2), 2: ("wall", 3), 1: ("wall", 4),
                8: ("floor", 0), 7: ("floor", 1), 9: ("floor", 2),
                11: ("lane", 0), 10: ("lane", 1), 12: ("lane", 2),
                14: ("trace", 0), 13: ("trace", 1), 15: ("trace", 2), 4: ("dash", 0)}
MATERIALS["underground_path"] = {
    7: dict(_TUNNEL_BORE),
    8: {1: ("wall", 4), 2: ("wall", 3), 3: ("wall", 1), 4: ("lamp", 0), 5: ("lamp", 1), 6: ("lamp", 2),
        7: ("lamp", 3), 8: ("lamp", 4)},
}

#  The accents: MT. SMOULDER's glow (the low orange and the banked red under it) takes 5 and 6, free in rows 7, 8
#  and 12 alike, so a tile drawn in any of the three rock rows glows the same.
ACCENT.update({"seafoam_islands": {}, "navel_rock": {}, "power_plant": {}, "underground_path": {},
               "mt_ember": {7: [5, 6], 8: [5, 6], 12: [5, 6]}})

#  More things standing on the floor, per tileset, beyond the shared OBJECTS: GLAUCOUS ISLES' cracked-ice floor and
#  its slides (row 11) and the frozen puddles' rings; MT. SMOULDER's steam, which its animation redraws in VRAM
#  (src/tileset_anims.c writes tiles 896.., secondary 256..263, every 16 frames).
EXTRA_OBJECTS = {
    "seafoam_islands": {14, 15, 30, 31, 156, 157, 172, 173, 188, 189} | set(range(230, 236)) | set(range(246, 252)) |
                       set(range(256, 264)) | set(range(272, 280)),
    "mt_ember": set(range(256, 264)),
}


def objects_of(ts):
    return OBJECTS | EXTRA_OBJECTS.get(ts, set())


# ---------------------------------------------------------------- GLAUCOUS ISLES: the bloom
#  Ice under a matte frosted skin. Down a face, tall FACETS of clear ice: each lit along its upper and left edges,
#  deep in the body, and crossed by one diagonal glint, the light inside clear ice; facets meet at a shaded edge,
#  never a black crack. Across a top, the BLOOM: big soft chalky drifts with a shallow seam between them.
_FAC = _voronoi([(4.0, 4.0, 0.0), (12.5, 7.0, 0.0), (6.0, 13.0, 0.0)])
GLINTS = {(3, 6), (4, 5), (5, 4), (11, 10), (12, 9), (13, 8), (5, 15), (6, 14)}     # one short diagonal a facet


def _facet(x, y):
    k = _FAC[y][x]
    if _FAC[y][(x + 1) % 16] != k or _FAC[(y + 1) % 16][x] != k:
        return "lo", 0
    if _FAC[y][(x - 1) % 16] != k or _FAC[(y - 1) % 16][x] != k:
        return "hi", 0
    if (x, y) in GLINTS:
        return "hi", 0
    return "body", (1 if k == 1 else 0)


FACETS = _torus(_facet)
#  a top is matte: flat, with one soft hollow in the powder a block, never a line
BLOOM = _marks([(9, 4, 4, 2)])


def m_bloom(X, Y, plane):
    if plane == "top":
        return ("lo" if BLOOM[Y][X] else "body"), 0
    return FACETS[Y][X]


# ---------------------------------------------------------------- MT. SMOULDER: ember under ash
#  Black cinder, and fire that never shows as flame. Down a face, CINDER clots (round, shaded, cracked between) and one
#  FISSURE a block, a jagged line across the face whose core glows low orange with a banked red under it -- the heat is
#  inside the rock, seen only through a crack. Across a top, ash: soft drifts lying on the cinder, no glow.
CINDER = _lumps(_voronoi([(3.0, 3.0, 0.6), (9.0, 2.0, 0.3), (14.0, 5.5, 0.5), (6.0, 8.5, 0.4), (12.0, 12.0, 0.6),
                          (2.0, 13.0, 0.3), (8.0, 15.0, 0.2)]))
FISSURE = [10, 10, 11, 11, 11, 10, 9, 9, 10, 10, 11, 12, 12, 11, 10, 10]   # its row at each column
GLOW = range(3, 11)                                                         # where it is open enough to glow
GLOW_CORE = range(5, 8)
#  a top is ash lying in DRIFTS (the user, 2026-10-23: "a little less flat"): each heap lit on its crest and body and
#  shaded at its foot, and here and there a cinder showing through where the ash lies thin
ASH = _marks([(1, 2, 7, 3), (9, 7, 6, 4), (3, 12, 5, 3)])       # three drifts a block, wind-laid, none alike
CINDERS_SHOWING = {(11, 3), (12, 3), (13, 13)}


def m_ember(X, Y, plane):
    if plane == "top":
        if (X, Y) in CINDERS_SHOWING:
            return "crack", 1
        #  a drift is heaped ash, lighter than the ash it lies on: its crest and body lit, its foot in shade
        return {"body": "hi", None: "body"}.get(ASH[Y][X], ASH[Y][X]), 0
    f = FISSURE[X]
    if Y == f:
        return ("accent0" if X in GLOW_CORE else "accent1" if X in GLOW else "crack"), 0
    if Y == f + 1:
        return ("accent1" if X in GLOW_CORE else "crack"), 0
    if Y == f - 1:
        return "lo", 0
    return CINDER[Y][X], 0


# ---------------------------------------------------------------- THE DOTS: braille
#  Sandstone, and on it writing meant for the hand. Down a face, one tall course of smooth stone carrying a line of
#  two BRAILLE CELLS a block (six positions each, 2 across and 3 down, a raised dot lit on its upper row and shaded on
#  its lower), and a thin course under it. Across a top, the same cells seen from above -- each dot is its shadow --
#  on a slab seamed once a block. The cells are "h" and "i" (dots 1-2-5 and 2-4): a greeting nobody sighted reads.
BRAILLE = ({1, 2, 5}, {2, 4})                                  # dot numbers: 1-3 down the left, 4-6 down the right
CELL_X, CELL_Y, PITCH = (2, 9), 1, 3


def _dot_at(x, y):
    """(dx, dy) inside a dot if (x, y) falls in a raised dot of one of the block's cells, else None"""
    for cx, cell in zip(CELL_X, BRAILLE):
        for n in cell:
            col, row = (n - 1) // 3, (n - 1) % 3
            x0, y0 = cx + col * PITCH, CELL_Y + row * PITCH
            if x0 <= x < x0 + 2 and y0 <= y < y0 + 2:
                return x - x0, y - y0
    return None


def _sandstone(x, y):
    if y == 15 or y == 10:
        return "crack", 0
    if y == 0 or y == 11:
        return "hi", 0
    if y == 14:
        return "lo", 0
    d = _dot_at(x, y)
    if d:
        return ("hi" if d[1] == 0 else "lo"), 0
    return "body", (1 if y > 10 else 0)


def _slab(x, y):
    if y == 15 or x == 15:
        return "crack", 0
    d = _dot_at(x, y)
    if d:
        #  seen from above a dot is its shadow, and it has to read at 1x (the user, 2026-10-23): a mid corner and
        #  three pixels four ranks down, so each cell's pattern is legible from across the screen
        return {(0, 0): ("body", 2), (1, 0): ("lo", 3), (0, 1): ("lo", 3), (1, 1): ("crack", 3)}[d]
    return "body", 0


BRAILLE_FACE, BRAILLE_TOP = _torus(_sandstone), _torus(_slab)


def m_dots(X, Y, plane):
    return (BRAILLE_TOP if plane == "top" else BRAILLE_FACE)[Y][X]


FLOOR_FROST = _marks([(2, 3, 5, 2), (10, 11, 4, 2)])           # two frost drifts a block
FLOOR_ASH = _marks([(4, 3, 2, 2), (11, 9, 3, 2), (2, 12, 2, 2)])    # cinders lying in the ash
FLOOR_FLAGS = [[None] * 16 for _ in range(16)]                     # sandstone flags laid like brick, two a block
for _k in range(16):
    FLOOR_FLAGS[7][_k] = FLOOR_FLAGS[15][_k] = "crack"
for _y in range(7):
    FLOOR_FLAGS[_y][4] = FLOOR_FLAGS[_y + 8][12] = "crack"


# ---------------------------------------------------------------- the two built rooms
def draw_plant(cave):
    """THE KEEPALIVE PLANT: still running. Every housing's face (tile 21, the panel under the conduits) is cut
    into panels a tile wide, each with a STATUS LIGHT on -- a lit pixel pair in the free index with a dark bezel under
    it; the drums' pink lamps turn green by palette. The floor plates keep vanilla's bevel; moss (the conduit's green:
    the living PLANT) grows in the seam where the walkways meet the plates."""
    new, what = [list(t) for t in cave.tiles], {}
    for t in range(cave.n):
        px = new[t]
        rows = cave.rows[t]
        if not rows or 7 not in rows:
            continue
        g = lambda x, y: px[y * 8 + x]
        # a housing face: a conduit stripe (2, then 3) above a plain body of 10 at least four rows deep
        body = [y for y in range(8) if all(g(x, y) == 10 for x in range(8))]
        if len(body) >= 4 and any(g(x, 0) in (1, 2, 3) for x in range(8)):
            top = body[0]
            for y in body:
                px[y * 8 + 7] = 13                           # the seam between two panels
            px[(top + 1) * 8 + 2] = px[(top + 1) * 8 + 3] = 14      # the status light
            px[(top + 2) * 8 + 2] = px[(top + 2) * 8 + 3] = 12      # its bezel's shadow
            px[(top + 1) * 8 + 1] = 12
            what[t] = "housing"
        # the seam where a walkway meets the plates (a row of 9 over a row of 13): moss growing in it
        elif all(g(x, 6) == 9 for x in range(8)) and all(g(x, 7) == 13 for x in range(8)) and \
                all(g(x, y) == 11 for x in range(8) for y in range(6)):
            for x, y in ((1, 6), (2, 6), (2, 5), (5, 6)):
                px[y * 8 + x] = 2
            what[t] = "seam"
    return new, what


def draw_tunnel(cave):
    """THE TUNNEL: a built bore. Its planks become the ring joints of a concrete tube (same pixels, the palette's
    work); vanilla's red band becomes the lane with the PACKET TRACE on it, a dashed line five on and three off in the
    free index; the long wall faces carry two CONDUITS, each a lit row over a shaded one; the side walls' panels carry
    one upright conduit."""
    new, what = [list(t) for t in cave.tiles], {}
    for t in range(cave.n):
        px = new[t]
        if not cave.rows[t] or 7 not in cave.rows[t]:
            continue
        g = lambda x, y: px[y * 8 + x]
        n13 = sum(1 for v in px if v == 13)
        if n13 >= 16:                                        # the red band: the trace
            for y in (3, 4):
                for x in range(1, 6):
                    if g(x, y) == 13 and g(x - 1, y) in (13, 4) and g(x + 1, y) == 13:
                        px[y * 8 + x] = 4
            what[t] = "trace"
            continue
        rows3 = [y for y in range(8) if all(g(x, y) == 3 for x in range(8))]
        rows2 = [y for y in range(8) if all(g(x, y) == 2 for x in range(8))]
        if len(rows3) >= 4 or len(rows2) >= 5:              # a long wall face: two conduits along it
            band, lit, dk = (rows3, 6, 2) if len(rows3) >= 4 else (rows2, 3, 1)
            a = band[0] + (0 if band is rows3 else 1)
            for y, v in ((a, lit), (a + 1, dk), (a + 3, lit), (a + 4, dk)):
                if y in band:
                    for x in range(8):
                        px[y * 8 + x] = v
            what[t] = "wall"
            continue
        cols = [x for x in range(8) if sum(1 for y in range(8) if g(x, y) == 3) >= 6]
        if len(cols) >= 4 and g(0, 0) == 1:                  # a side wall's panel: one conduit up it
            c = cols[len(cols) // 2 - 1]
            for y in range(8):
                if g(c, y) == 3 and g(c + 1, y) == 3:
                    px[y * 8 + c], px[y * 8 + c + 1] = 6, 2
            what[t] = "wall"
    return new, what


LOOKS.update({
    #  palette splits: tiles from `base`, light of their own
    "cave/umbral": dict(
        base="cave", name="UMBRAL ASCENT", motif="the stack, at dusk",
        pal={"floor": [(150, 140, 164), (128, 118, 146), (108, 98, 128), (86, 78, 106)],
             "rock": [(196, 186, 222), (162, 150, 198), (128, 116, 170), (98, 86, 140), (70, 60, 108), (44, 38, 74)],
             "dark": [(28, 24, 44), (52, 46, 70)], "shade": [(64, 58, 84)], "hole": [(10, 8, 18)],
             "wood": [(226, 220, 236), (200, 192, 218), (172, 164, 196), (144, 136, 170), (112, 104, 140),
                      (82, 76, 108)],
             "rung": [(226, 220, 236), (190, 182, 210), (152, 144, 178), (116, 108, 142)],
             "water": [(92, 104, 168), (70, 82, 146), (52, 62, 122)],
             "patch": [(184, 176, 200), (168, 160, 186), (152, 144, 172), (136, 128, 158)],
             "accent": [(206, 180, 132), (138, 112, 92), (168, 112, 128)]}),
    "rock_tunnel/other": dict(
        base="rock_tunnel", name="OTHER CAVE", motif="the outage, in mineral light",
        pal={"floor": [(184, 160, 164), (166, 142, 148), (148, 124, 132), (128, 106, 116), (108, 88, 100)],
             "rock": [(208, 238, 230), (170, 216, 208), (136, 190, 184), (104, 160, 158), (76, 128, 130), (52, 96, 100)],
             "dark": [(26, 52, 56), (44, 74, 76)], "shade": [(40, 70, 72)], "hole": [(6, 18, 20)],
             "wood": [(238, 232, 206), (214, 206, 178), (186, 178, 150), (160, 150, 124), (130, 120, 98),
                      (100, 92, 76)],
             "rung": [(238, 232, 206), (206, 198, 170), (170, 162, 136), (134, 126, 104)],
             "water": [(80, 150, 176), (60, 126, 156), (44, 102, 134)],
             "patch": [(148, 124, 132), (136, 112, 122), (122, 100, 110)],
             "accent": []},
        #  OTHER CAVE never holds the same light twice running (the user, 2026-10-23): four lights in a cycle a player
        #  can learn, one a visit, and its wild daemons follow the light (light n is VAR_ALTERING_CAVE_WILD_SET's set
        #  n). Light 0 is the mineral teal above; these three are the same mineral idea in other stones -- each the
        #  walls' crystal over a floor of the rock it grows in, the same value steps as the teal, never grey.
        #  The ladders keep one colour in every light: a ladder is a thing the player looks for.
        lights=[
            dict(name="AMBER", stone="amber in slate",
                 floor=[(150, 152, 164), (132, 134, 148), (114, 116, 132), (96, 98, 116), (78, 80, 98)],
                 rock=[(246, 226, 170), (228, 196, 128), (204, 162, 88), (168, 124, 60), (124, 88, 44), (84, 58, 32)],
                 dark=[(52, 36, 20), (74, 54, 32)], shade=[(64, 46, 28)], hole=[(20, 12, 6)],
                 patch=[(114, 116, 132), (104, 106, 122), (92, 94, 110)]),
            dict(name="CHRYSOPRASE", stone="chrysoprase in brown jasper",
                 floor=[(168, 150, 140), (150, 132, 124), (132, 114, 108), (112, 96, 92), (94, 78, 76)],
                 rock=[(226, 238, 190), (196, 218, 150), (160, 190, 114), (122, 156, 84), (88, 120, 62), (58, 86, 46)],
                 dark=[(30, 46, 24), (48, 66, 36)], shade=[(40, 58, 32)], hole=[(10, 18, 8)],
                 patch=[(132, 114, 108), (122, 104, 98), (108, 92, 88)]),
            dict(name="ROSE QUARTZ", stone="rose quartz in green schist",
                 floor=[(140, 166, 164), (122, 148, 148), (104, 130, 132), (88, 112, 116), (72, 94, 100)],
                 rock=[(250, 222, 228), (236, 192, 204), (214, 156, 176), (184, 120, 146), (146, 88, 114), (104, 60, 82)],
                 dark=[(56, 26, 40), (78, 44, 58)], shade=[(68, 36, 50)], hole=[(20, 6, 12)],
                 patch=[(104, 130, 132), (94, 120, 122), (82, 106, 110)]),
        ]),
    "seafoam_islands": dict(
        name="GLAUCOUS ISLES", motif="the bloom", rock=m_bloom, rim=None, floor=FLOOR_FROST, field=1, off=MARK_OFF,
        patch_field=0, top_at=2.6,
        pal={"floor": [(208, 224, 222), (190, 210, 210), (166, 190, 194), (138, 162, 172)],
             "rock": [(234, 242, 236), (214, 230, 226), (176, 214, 214), (130, 188, 198), (94, 156, 176),
                      (68, 124, 150), (48, 94, 122)],
             "shade": [(34, 54, 72)],
             "glint": [(168, 238, 232), (196, 248, 242), (228, 255, 250)],
             "patch": [(200, 222, 180), (180, 206, 164)]}),
    "seafoam_islands/stillfall": dict(
        base="seafoam_islands", name="STILLFALL CAVE", motif="the bloom, gone glassy",
        pal={"floor": [(198, 222, 238), (174, 204, 226), (148, 182, 210), (120, 154, 188)],
             "rock": [(220, 242, 252), (180, 224, 244), (124, 192, 228), (80, 152, 204), (52, 116, 174),
                      (36, 84, 140), (26, 58, 104)],
             "shade": [(22, 40, 72)],
             "glint": [(150, 236, 255), (192, 246, 255), (236, 255, 255)],
             "patch": [(184, 214, 204), (164, 198, 190)]}),
    "mt_ember": dict(
        name="MT. SMOULDER", motif="ember under ash", rock=m_ember, rim=None, floor=FLOOR_ASH, field=1,
        off=MARK_OFF, patch_field=1,
        pal={"floor": [(136, 112, 100), (118, 96, 86), (100, 80, 72), (82, 64, 58)],
             "rock": [(180, 164, 150), (148, 132, 122), (106, 92, 86), (64, 52, 50), (42, 32, 32), (26, 18, 20)],
             "shade": [(34, 26, 28)],
             "patch": [(216, 204, 186), (194, 182, 164), (174, 162, 146), (156, 144, 130)],
             "accent": [(200, 92, 38), (120, 40, 28)]},
        rows={7: {"rock": [(156, 140, 128), (122, 106, 98), (84, 70, 66), (50, 40, 40), (32, 24, 26), (18, 12, 14)],
                  "shade": [(24, 18, 20)]},
              12: {"rock": [(128, 112, 104), (96, 82, 78), (64, 52, 50), (38, 30, 30), (22, 16, 18), (10, 6, 8)],
                   "shade": [(12, 8, 10)]}}),
    "navel_rock": dict(
        name="THE DOTS", motif="braille", rock=m_dots, rim=None, floor=FLOOR_FLAGS, field=1, off=CRACK_OFF,
        patch_field=1,
        pal={"floor": [(214, 190, 150), (194, 168, 130), (172, 146, 110), (142, 118, 88)],
             "rock": [(244, 228, 194), (226, 204, 164), (198, 172, 130), (162, 134, 98), (122, 96, 70), (82, 62, 48)],
             "patch": [(234, 216, 180), (218, 198, 162), (202, 180, 144), (162, 140, 108)]},
        rows={12: {"rock": [(190, 160, 146), (164, 134, 122), (136, 108, 100), (108, 84, 80), (80, 60, 60),
                            (54, 40, 42)],
                   "floor": [(172, 150, 128), (152, 130, 110), (132, 112, 94), (110, 92, 78)]}}),
    "power_plant": dict(
        name="KEEPALIVE PLANT", motif="still running", built=draw_plant, home=7,
        pal={"plate": [(200, 212, 200), (160, 178, 168)], "lane": [(182, 198, 188)],
             "housing": [(150, 168, 178), (122, 140, 154), (90, 104, 122), (50, 58, 76)],
             "girder": [(160, 180, 200), (120, 142, 166), (88, 110, 136)], "trim": [(176, 192, 162)],
             "conduit": [(170, 100, 64), (82, 134, 62), (44, 66, 118)], "status": [(128, 250, 104), (62, 168, 72)],
             "coil": [(214, 232, 196), (170, 196, 150), (118, 148, 108)]}),
    "underground_path": dict(
        name="THE TUNNEL", motif="the bore", built=draw_tunnel, home=7,
        pal={"wall": [(198, 206, 214), (152, 162, 172), (130, 138, 150), (108, 118, 130), (54, 60, 74)],
             "floor": [(196, 204, 202), (176, 186, 186), (138, 150, 154)],
             "lane": [(250, 252, 246), (234, 240, 234), (184, 194, 194)],
             "trace": [(250, 252, 246), (234, 240, 234), (184, 194, 194)], "dash": [(56, 156, 214)],
             "lamp": [(250, 252, 255), (220, 240, 255), (188, 204, 214), (158, 172, 184), (128, 140, 152)]}),
})


def palettes(cave, proposed=True, key=None, light=0):
    """the secondary's sixteen rows: today's, or the look's -- each named index given its role's colour. `key` names a
    look other than the tileset's own (a palette split: "cave/umbral"); `light`, one of OTHER CAVE's other lights."""
    pals = [list(p) for p in cave.pals]
    if not proposed:
        return pals
    look = LOOKS[key or cave.ts]
    if light:
        look = dict(look, pal=dict(look["pal"], **{k: v for k, v in look["lights"][light - 1].items()
                                                   if k not in ("name", "stone")}))
    for r, plan in MATERIALS[cave.ts].items():
        for i, (mat, k) in plan.items():
            ramp = look.get("rows", {}).get(r, {}).get(mat) or look["pal"].get(mat)
            if ramp:
                pals[r][i] = ramp[min(k, len(ramp) - 1)]
        for k, i in enumerate(ACCENT.get(cave.ts, {}).get(r, [])):
            pals[r][i] = look["pal"]["accent"][k]
    return pals


def palette_touch(cave, key=None):
    """row -> [(index, today, proposed, its role)] for every index the look changes"""
    now, new = palettes(cave, False), palettes(cave, True, key)
    out = {}
    for r in range(16):
        ch = []
        for i in range(16):
            if now[r][i] != new[r][i]:
                plan = MATERIALS[cave.ts].get(r, {})
                role = "%s %d" % plan[i] if i in plan else "accent %d" % ACCENT[cave.ts][r].index(i)
                ch.append((i, now[r][i], new[r][i], role))
        if ch:
            out[r] = ch
    return out


def placement(cave, t):
    """the tile's main placement: (block, slot 0..7, flip bits), by how often maps place the block"""
    best = None
    for b in range(len(cave.mt) // 16):
        w = cave.placed.get(640 + b, 0) + 0.001
        for j, v in enumerate(entries(cave.mt, b)):
            if (v & 0x3FF) - 640 == t and (best is None or w > best[0]):
                best = (w, b, j, (v >> 10) & 3)
    return best[1:] if best else None


def layer_grid(cave, b, layer, plans):
    """the 16x16 (material, rank) grid of one layer of a block, as vanilla draws it"""
    g = [[None] * 16 for _ in range(16)]
    for q, v in enumerate(entries(cave.mt, b)[layer * 4:layer * 4 + 4]):
        t, row = v & 0x3FF, v >> 12
        if t < 640 or t - 640 >= cave.n:
            continue
        src = cave.tiles[t - 640]
        for y in range(8):
            for x in range(8):
                c = src[(7 - y if v & 0x800 else y) * 8 + (7 - x if v & 0x400 else x)]
                if c:
                    g[(q // 2) * 8 + y][(q % 2) * 8 + x] = plans.get(row, {}).get(c)
    return g


def _gmean(g, x, y, kind, rad):
    acc = n = 0
    for b in range(max(0, y - rad), min(16, y + rad + 1)):
        for a in range(max(0, x - rad), min(16, x + rad + 1)):
            if g[b][a] and g[b][a][0] == kind:
                acc += g[b][a][1]
                n += 1
    return acc / n if n else 0


def redraw(cave, key=None):
    """every tile of the tileset in the look: (new tiles, {tile: what it is}), footprints and joins kept.

    Each tile is drawn where it is drawn most: in its main block's layer, so the light around a pixel, the joins and
    the rim are read across the tile's edges from the three tiles beside it, and the motif is laid at the tile's own
    place in the block (a block is 16x16, the motif's period, so it runs on across blocks)."""
    look = LOOKS[key or cave.ts]
    look = LOOKS[look.get("base", key or cave.ts)]       # a palette split draws its base's tiles
    if look.get("built"):
        return look["built"](cave)
    plans = MATERIALS[cave.ts]
    objs = objects_of(cave.ts)
    top_at = look.get("top_at", TOP_AT)
    new, what = [], {}
    COMPROMISES.pop(cave.ts, None)
    for t in range(cave.n):
        px = cave.tiles[t]
        rows = [r for r in cave.rows[t] if r >= 7]
        where = placement(cave, t)
        if not rows or not any(px) or t in objs or not where:
            new.append(list(px))
            continue
        b, j, f = where
        home = entries(cave.mt, b)[j] >> 12
        plan = plans.get(home, {})
        # an index may be written only if it means the same in every row this tile is drawn in
        inv = collections.defaultdict(dict)
        for i, mk in plan.items():
            if all(plans.get(r, {}).get(i) == mk for r in rows):
                inv[mk[0]][mk[1]] = i
        # an accent may be written if the rows that lack it draw the tile less than a tenth of the time; those few
        # placements show the accent index in their own row's colour, and COMPROMISES lists them for the sheet
        tot = sum(cave.rows[t][r] for r in rows)
        lack = [r for r in rows if r != home and cave.rows[t][r] * 10 >= tot]
        acc = [i for i in ACCENT.get(cave.ts, {}).get(home, []) if all(i in ACCENT[cave.ts].get(r, []) for r in lack)]
        minor = [r for r in rows if r != home and r not in lack and not set(acc) <= set(ACCENT[cave.ts].get(r, []))]
        g = layer_grid(cave, b, j // 4, plans)
        ox, oy = ((j % 4) % 2) * 8, ((j % 4) // 2) * 8
        base = [[_gmean(g, x, y, "rock", 2) if g[y][x] and g[y][x][0] == "rock" else None for x in range(16)]
                for y in range(16)]
        face = lambda x, y: 0 <= y < 16 and base[y][x] is not None and base[y][x] > top_at
        top = lambda x, y: 0 <= y < 16 and base[y][x] is not None and base[y][x] <= top_at
        out = list(px)
        drawn = 0
        kinds = collections.Counter()

        def run(X, Y):
            """how far a face runs along its row from here, counting a block edge as going on"""
            n = 1
            for step in (1, -1):
                a = X + step
                while 0 <= a < 16 and face(a, Y):
                    n += 1
                    a += step
                if not 0 <= a < 16:
                    n += 3
            return n

        def put(i, kind, k):
            ramp = inv[kind]
            k = max(0, min(max(ramp) if ramp else 0, k))
            while k not in ramp and k > 0:
                k -= 1
            if k in ramp:
                out[i] = ramp[k]
                return 1
            return 0
        for y in range(8):
            for x in range(8):
                i = y * 8 + x
                if not px[i]:
                    continue
                X, Y = ox + (7 - x if f & 1 else x), oy + (7 - y if f & 2 else y)    # in the block
                m = g[Y][X]
                if not m:
                    continue
                kinds[m[0]] += 1
                if m[0] not in ("rock", "floor", "patch"):
                    continue
                kind = m[0]
                if any(not (0 <= a < 16 and 0 <= c < 16) or not g[c][a] or g[c][a][0] != kind
                       for a, c in ((X + 1, Y), (X - 1, Y), (X, Y + 1), (X, Y - 1))
                       if 0 <= a < 16 and 0 <= c < 16):
                    continue                            # a join: vanilla's, so it meets what is beside it
                if kind == "rock":
                    b0 = base[Y][X]
                    plane = "top" if b0 <= top_at else "face"
                    if plane == "top" and m[1] >= b0 + 2.5:
                        continue                        # a hole or pit vanilla drew in a top: kept
                    role, shift = look["rock"](X, Y, plane)
                    # the rim: the first rows of a face under a lit top, where THE LINE runs -- a real cut only,
                    # one that goes on down at least four rows (not the lip of a hole)
                    if look["rim"] and plane == "face" and all(face(X, Y + e) or Y + e >= 16 for e in range(4)) \
                            and run(X, Y) >= 7:
                        for d, r in enumerate(look["rim"]):
                            if top(X, Y - d - 1) and all(face(X, Y - e) for e in range(d + 1)):
                                role, shift = r, 0
                    if role.startswith("accent"):
                        k = int(role[-1])
                        if k < len(acc):
                            out[i] = acc[k]
                            drawn += 1
                            continue
                        role = "lo"
                    off = ROLE_OFF[role] - (1 if plane == "top" and role == "crack" else 0)
                    drawn += put(i, "rock", round(b0) + off + shift)
                else:
                    ramp = inv[kind]
                    hi = max(ramp) if ramp else 0
                    if kind == "floor" and m[1] >= hi and _gmean(g, X, Y, kind, 1) >= hi - 0.5:
                        continue                        # vanilla's shadow under a wall stays
                    field = look["field"] if kind == "floor" else look["patch_field"]
                    k = field + look["off"][look["floor"][Y][X]]
                    drawn += put(i, kind, min(k, hi - 1) if kind == "floor" and hi > field + 1 else k)
        new.append(out)
        if drawn:
            what[t] = max(kinds, key=kinds.get)
        if minor and any(v in acc for v in out):
            COMPROMISES.setdefault(cave.ts, []).append((t, minor))
    return new, what


COMPROMISES = {}   # tileset -> [(tile, rows that show its accent index in their own colour)]


# ================================================================== the draft: files and sheets
SHORT = {"cave": "deadstack", "digletts_cave": "tappoint", "rock_tunnel": "blackout",
         "cave/umbral": "umbral", "rock_tunnel/other": "othercave", "power_plant": "keepalive",
         "seafoam_islands": "glaucous", "seafoam_islands/stillfall": "stillfall", "mt_ember": "smoulder",
         "navel_rock": "dots", "underground_path": "tunnel"}
FLASH = {"RockTunnel_1F", "RockTunnel_B1F"}             # requires_flash: dark until VERBOSE
FLASH_DARK = 24                                         # field_screen_effect.c: sFlashLevelToRadius[4], no VERBOSE
CROPS = {   # (map, x0, y0, w, h in cells, what it shows); a dark view is centred on (x0 + 7, y0 + 5)
    "cave": [("MtMoon_1F", 8, 0, 20, 18, "DEADSTACK 1F: ridges, a ladder hole, a fossil, the pale drifts"),
             ("MtMoon_B2F", 0, 0, 24, 20, "DEADSTACK B2F: ledges, stairs, ladders, water"),
             ("VictoryRoad_1F", 0, 0, 24, 20, "UMBRAL ASCENT 1F: the same tileset -- what sharing gives it")],
    "digletts_cave": [("DiglettsCave_B1F", 0, 0, 24, 24, "TAPPOINT'S CAVE B1F: the burrow, its cuts, the holes"),
                      ("DiglettsCave_B1F", 52, 44, 24, 24, "TAPPOINT'S CAVE B1F: the far end"),
                      ("DiglettsCave_NorthEntrance", 0, 0, 10, 8, "the north entrance")],
    "rock_tunnel": [("RockTunnel_1F", 0, 0, 24, 20, "THE BLACKOUT 1F, lit by VERBOSE"),
                    ("RockTunnel_B1F", 0, 0, 24, 20, "THE BLACKOUT B1F, lit by VERBOSE"),
                    ("SixIsland_AlteringCave", 0, 0, 24, 20, "OTHER CAVE: the same tileset -- what sharing gives it")],
    # batch E2
    "cave/umbral": [("VictoryRoad_1F", 0, 0, 24, 20, "UMBRAL ASCENT 1F: boulders, ladders, the climb"),
                    ("VictoryRoad_2F", 24, 0, 24, 20, "UMBRAL ASCENT 2F: ledges and switches")],
    "rock_tunnel/other": [("SixIsland_AlteringCave", 0, 0, 24, 20, "OTHER CAVE: the entrance half"),
                          ("SixIsland_AlteringCave", 8, 4, 24, 20, "OTHER CAVE: the far half")],
    "power_plant": [("PowerPlant", 0, 0, 24, 20, "KEEPALIVE PLANT: the entrance, the first housings, the coils"),
                    ("PowerPlant", 20, 16, 24, 20, "KEEPALIVE PLANT: the long housing, the drums, the generator")],
    "seafoam_islands": [("SeafoamIslands_1F", 0, 0, 24, 20, "GLAUCOUS ISLES 1F: ice walls, boulders, ladders"),
                        ("SeafoamIslands_B3F", 8, 2, 24, 20, "GLAUCOUS ISLES B3F: the currents, four floors down")],
    "seafoam_islands/stillfall": [("FourIsland_IcefallCave_1F", 0, 0, 20, 20, "STILLFALL 1F: the cracked-ice floor"),
                                  ("FourIsland_IcefallCave_Back", 0, 0, 25, 20, "STILLFALL: the back, the frozen falls")],
    "mt_ember": [("MtEmber_RubyPath_1F", 0, 0, 27, 19, "MT. SMOULDER: the RUBY PATH's first floor"),
                 ("OneIsland_KindleRoad_EmberSpa", 0, 0, 27, 24, "KETTLE SPRING: the spa, its steam, the pools")],
    "navel_rock": [("SixIsland_DottedHole_1F", 0, 0, 16, 11, "THE DOTS 1F: tops, the walls' faces, the floor"),
                   ("NavelRock_Base", 0, 0, 21, 23, "NAVEL ROCK (never reached): what it would inherit")],
    "underground_path": [("UndergroundPath_EastWestTunnel", 0, 0, 30, 7, "THE TUNNEL, east-west: the lane and its trace"),
                         ("UndergroundPath_NorthSouthTunnel", 0, 0, 8, 40, "THE TUNNEL, north-south: the bands, the walls")],
}
DARK_AT = {"RockTunnel_1F": (12, 10), "RockTunnel_B1F": (10, 9)}     # a floor cell to stand on, for the dark view


def font(n):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except OSError:
        return ImageFont.load_default()


def tiles_png(cave, tiles, pal=None):
    """tiles.png as the engine keeps it (indexed, its own palette), with these tiles' indices"""
    im = cave.im.copy()
    if pal:
        flat = [c for rgb in pal for c in rgb]
        im.putpalette(flat + im.getpalette()[len(flat):])
    w = im.size[0] // 8
    px = im.load()
    for t, p in enumerate(tiles):
        for k, v in enumerate(p):
            px[(t % w) * 8 + k % 8, (t // w) * 8 + k // 8] = v
    return im


def dark(img, cx, cy, r=FLASH_DARK):
    """the screen without VERBOSE: only the circle round the player is drawn, the rest is the black backdrop"""
    out = img.copy()
    o = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if (x - cx) ** 2 + (y - cy) ** 2 > r * r:
                o[x, y] = (0, 0, 0)
    return out


def _label(im, text, f, pad=4, colour=(30, 30, 30), bg=(236, 234, 226)):
    lines = text.split("\n")
    h = (f.size + 3) * len(lines) + pad * 2
    out = Image.new("RGB", (im.width, im.height + h), bg)
    d = ImageDraw.Draw(out)
    for k, l in enumerate(lines):
        d.text((pad, pad + k * (f.size + 3)), l, font=f, fill=colour)
    out.paste(im, (0, h))
    return out


def _row(ims, gap=12, bg=(236, 234, 226)):
    w = sum(i.width for i in ims) + gap * (len(ims) - 1)
    h = max(i.height for i in ims)
    out = Image.new("RGB", (w, h), bg)
    x = 0
    for i in ims:
        out.paste(i, (x, 0))
        x += i.width + gap
    return out


def _title(text, f, w, bg=(236, 234, 226)):
    lines = text.split("\n")
    im = Image.new("RGB", (w, (f.size + 5) * len(lines) + 6), bg)
    d = ImageDraw.Draw(im)
    for k, l in enumerate(lines):
        d.text((2, 3 + k * (f.size + 5)), l, font=f, fill=(20, 20, 20))
    return im


def _col(ims, gap=12, bg=(236, 234, 226), pad=12):
    w = max(i.width for i in ims) + pad * 2
    h = sum(i.height for i in ims) + gap * (len(ims) - 1) + pad * 2
    out = Image.new("RGB", (w, h), bg)
    y = pad
    for i in ims:
        out.paste(i, (pad, y))
        y += i.height + gap
    return out


def map_sheet(cave, new, pals, crop, path, key=None):
    name, x0, y0, w, h, what = crop
    look = LOOKS[key or cave.ts]
    a = render(cave, name, box=(x0, y0, w, h))
    b = render(cave, name, tiles=new, pals=pals, box=(x0, y0, w, h))
    f, F = font(13), font(17)
    z2 = lambda im: im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    if look.get("base"):                # a palette split: also what it would be if it kept sharing its base's light
        c = render(cave, name, tiles=new, pals=palettes(cave, True, look["base"]), box=(x0, y0, w, h))
        rows = [_row([_label(a, "today (vanilla) 1x", f), _label(c, "shared: %s's light 1x" % LOOKS[look["base"]][
                    "name"], f), _label(b, "draft: its own light 1x", f)]),
                _row([_label(z2(a), "today 2x", f), _label(z2(b), "draft 2x", f)])]
    else:
        rows = [_label(_row([_label(a, "today (vanilla) 1x", f), _label(b, "draft: %s 1x" % look["motif"], f)]),
                       "", f),
                _row([_label(z2(a), "today 2x", f), _label(z2(b), "draft 2x", f)])]
    if name in FLASH:
        cx, cy = DARK_AT[name]
        box = (cx - 7, cy - 5, 15, 10)
        sa, sb = render(cave, name, box=box), render(cave, name, tiles=new, pals=pals, box=box)
        c = (7 * 16 + 8, 5 * 16 + 8)
        rows.append(_row([_label(z2(sa), "today, one screen, VERBOSE used", f),
                          _label(z2(sb), "draft, VERBOSE used", f),
                          _label(z2(dark(sa, *c)), "today, dark (24px)", f),
                          _label(z2(dark(sb, *c)), "draft, dark (24px)", f)]))
    sheet = _col([_title("T-438 batch E DRAFT -- %s (%s): %s\n%s, cells %d,%d %dx%d -- footprints, blocks, "
                         "collision unchanged" % (look["name"], key or cave.ts, what, name, x0, y0, w, h), F,
                         max(r.width for r in rows))] + rows)
    sheet.save(path)
    return path


def swatch_rows(cave, pals_now, pals_new, f):
    """rows 8..12 (7..12 where the look names row 7), today over proposed, every index boxed and labelled"""
    Z = 26
    ims = []
    plans = MATERIALS[cave.ts]
    for r in range(7 if 7 in plans else 8, 13):
        im = Image.new("RGB", (60 + 16 * (Z + 52), Z * 2 + 22), (236, 234, 226))
        d = ImageDraw.Draw(im)
        d.text((4, Z // 2), "row %d" % r, font=f, fill=(30, 30, 30))
        for i in range(16):
            x = 60 + i * (Z + 52)
            d.rectangle([x, 0, x + Z - 1, Z - 1], fill=pals_now[r][i])
            d.rectangle([x, Z + 2, x + Z - 1, 2 * Z + 1], fill=pals_new[r][i],
                        outline=(200, 30, 30) if pals_now[r][i] != pals_new[r][i] else None)
            role = plans.get(r, {}).get(i)
            lab = ("%s%d" % (role[0][:5], role[1])) if role else (
                "acc%d" % ACCENT[cave.ts][r].index(i) if i in ACCENT.get(cave.ts, {}).get(r, []) else "-")
            d.text((x, 2 * Z + 6), "%d %s" % (i, lab), font=f, fill=(60, 60, 60))
        ims.append(im)
    return ims


def atlas(cave, tiles, pals, Z=3):
    w = 16
    im = Image.new("RGB", (w * 8 * Z, (cave.n // w) * 8 * Z), (255, 0, 255))
    o = im.load()
    for t in range(cave.n):
        r = cave.home(t)
        r = r if r and r >= 7 else 8
        for k, v in enumerate(tiles[t]):
            if not v:
                continue
            x, y = (t % w) * 8 + k % 8, (t // w) * 8 + k // 8
            for a in range(Z):
                for b in range(Z):
                    o[x * Z + a, y * Z + b] = pals[r][v]
    return im


def tiles_sheet(cave, new, what, path, key=None):
    f, F = font(12), font(17)
    look = LOOKS[key or cave.ts]
    now, pp = palettes(cave, False), palettes(cave, True, key)
    counts = collections.Counter(what.values())
    top = _row([_label(atlas(cave, cave.tiles, now), "tiles.png today, each tile in its own row", f),
                _label(atlas(cave, new, pp), ("draft: %d tiles redrawn (%s)\nboulders, rocks, ladders, holes, "
                       "water keep their drawing" % (len(what), ", ".join("%s %d" % kv for kv in sorted(counts.items())))
                       if not look.get("base") else "draft: %s's tiles, in %s's own light\n(a palette split: no "
                       "tile of its own)" % (LOOKS[look["base"]]["name"], look["name"])), f)])
    sw = swatch_rows(cave, now, pp, f)
    sheet = _col([_title("T-438 batch E DRAFT -- %s: the tileset and its palettes\nrows %d..12: today above, "
                         "proposed below, red where changed" % (look["name"], 7 if 7 in MATERIALS[cave.ts] else 8), F,
                         max(top.width, sw[0].width)), top] + sw)
    sheet.save(path)
    return path


def _wrap(text, n):
    out, line = [], ""
    for w in text.split():
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    return out + [line]


def proposal_sheet(path):
    """the proposal as a table: tileset, its places and what each is, the look, the split, drafted or not"""
    f, fb, F = font(13), font(14), font(20)
    cols = [("TILESET (first met)", 22), ("PLACES -- maps -- what the bible says it is", 62),
            ("THE LOOK PROPOSED", 66), ("SHARED? SPLIT?", 36)]
    lh = f.size + 4
    rows = []
    for p in sorted(PROPOSAL, key=lambda p: p["order"]):
        cells = [_wrap("%s%s" % (p["ts"], "  [DRAFTED%s]" % (" E2" if p.get("drafted_e2") else "") if p["drafted"] else ""), cols[0][1]) +
                 ["", "rank %d" % p["order"]],
                 sum((_wrap("%s -- %s -- %s" % pl, cols[1][1]) + [""] for pl in p["places"]), []),
                 _wrap(p["look"], cols[2][1]), _wrap(p["split"], cols[3][1])]
        rows.append((p, cells, max(len(c) for c in cells)))
    cw = [n * 8 + 16 for _, n in cols]
    W = sum(cw) + 24
    H = 70 + sum(n * lh + 14 for _, _, n in rows) + 30 + 60
    im = Image.new("RGB", (W, H), (244, 242, 236))
    d = ImageDraw.Draw(im)
    d.text((12, 10), "T-438 batch E -- a look per cave (PROPOSAL; all but TANOBY and DOLDRUM drafted, nothing in the "
                     "engine)",
           font=F, fill=(20, 20, 20))
    x = 12
    for (h, _), w in zip(cols, cw):
        d.text((x, 44), h, font=fb, fill=(90, 40, 30))
        x += w
    y = 70
    for p, cells, n in rows:
        d.rectangle([8, y - 4, W - 8, y + n * lh + 6], fill=(232, 238, 226) if p["drafted"] else (250, 249, 245),
                    outline=(200, 196, 186))
        x = 12
        for c, w in zip(cells, cw):
            for k, l in enumerate(c):
                d.text((x, y + k * lh), l, font=fb if (c is cells[0] and k == 0) else f, fill=(25, 25, 25))
            x += w
        if p["drafted"]:
            pp = palettes(Cave(p["ts"]), True)
            hr = LOOKS[p["ts"]].get("home", 8)
            for k, rgb in enumerate([pp[hr][i] for i in (1, 2, 3, 4, 9, 10, 11, 12, 13, 14)] +
                                    [pp[hr][i] for i in ACCENT[p["ts"]].get(hr, [])[:2]]):
                d.rectangle([12 + k * 14, y + n * lh - 16, 12 + k * 14 + 12, y + n * lh - 4], fill=rgb)
        y += n * lh + 14
    for k, l in enumerate(["Grey is not a look here: HALFTONE and the unread DOLDRUM CAVE own it (8.6a, T-251), and "
                           "DaemonsIsHalftone() greys DOLDRUM's screen whatever its tileset is.",
                           "A palette split is a new Tileset header reusing the tiles and metatiles with its own "
                           "palettes (192 bytes, no tiles): the cheap way to give a shared cave a light of its own."]):
        d.text((12, y + 8 + k * lh), l, font=f, fill=(90, 40, 30))
    im.save(path)
    return path


def groups(cave, new, what, key=None):
    look = LOOKS[key or cave.ts]
    pal = {r: [dict(index=i, today=a, proposed=b, role=role) for i, a, b, role in v]
           for r, v in palette_touch(cave, key).items()}
    if look.get("base"):
        return dict(tiles="shares %s's drafted tiles (%s/tiles.png): a palette split" % (
                        LOOKS[look["base"]]["name"], look["base"]),
                    maps=split_maps(cave, key), palette_proposal=pal)
    by = collections.defaultdict(list)
    for t, k in sorted(what.items()):
        by[k].append(t)
    kept = sorted(t for t in range(cave.n) if any(cave.tiles[t]) and t not in what and cave.rows[t])
    return dict(redrawn={k: v for k, v in by.items()}, kept_drawing=kept,
                objects=sorted(objects_of(cave.ts)), compromises=COMPROMISES.get(cave.ts, []),
                maps=cave.maps, palette_proposal=pal)


#  the batch E2 drafts, first met first. The first three (DRAFTED) are approved and are the only ones --write writes.
DRAFTED_E2 = ["underground_path", "power_plant", "rock_tunnel/other", "seafoam_islands", "seafoam_islands/stillfall",
              "mt_ember", "navel_rock", "cave/umbral"]
#  a palette split in the engine: its Tileset header (src/data/tilesets/headers.h) and where its rows 7..12 are kept
SPLIT_SYMBOL = {"cave/umbral": "gTileset_CaveUmbral", "rock_tunnel/other": "gTileset_OtherCave",
                "seafoam_islands/stillfall": "gTileset_Stillfall"}
SPLIT_DIR = {"cave/umbral": "cave/palettes_umbral", "rock_tunnel/other": "rock_tunnel/palettes_other",
             "seafoam_islands/stillfall": "seafoam_islands/palettes_stillfall"}
SPLIT_MAPS = {"cave/umbral": "VictoryRoad_", "rock_tunnel/other": "SixIsland_AlteringCave",
              "seafoam_islands/stillfall": "FourIsland_IcefallCave"}


def split_maps(cave, key):
    return [m for m in cave.maps if m.startswith(SPLIT_MAPS[key])]


#  OTHER CAVE, "never holds the same thing twice" (2.10): how the per-entry light works. The user approved it as a
#  cycle of four (2026-10-23) with the wild daemons following the light; BUILT as described, the var VAR_OTHER_CAVE_LIGHT
#  (0x40C5) and the palettes this tool writes, the code in fieldmap.c and the map's ON_TRANSITION.
PER_ENTRY = [
    "HOW: OTHER CAVE gets its own Tileset header (the palette split above) whose palettes are a table of N lights "
    "instead of one -- the mineral teal and, say, three more (amber, rose quartz, lichen). LoadTilesetPalette() in "
    "src/fieldmap.c already special-cases gTileset_General; one more case, `if (tileset == &gTileset_OtherCave)`, "
    "loads rows 7..12 from light number VAR_OTHER_CAVE_LIGHT instead of the header's own.",
    "WHEN IT CHANGES: on ENTRY, never on a reload. LoadSecondaryTilesetPalette() also runs after a battle, after the "
    "bag or the menu closes, on a load from the save and on the DEBUG menu's return -- a light picked there would "
    "flicker mid-visit. So the map's ON_TRANSITION script (which runs once per warp in) steps the var: "
    "`addvar VAR_OTHER_CAVE_LIGHT, 1` mod N, or a `random N`. Stepping in order makes it a cycle a player can learn; "
    "random makes it never knowable (and can repeat the last one unless re-rolled).",
    "COST: N x 192 bytes of palettes (rows 7..12; 768 B for four) plus about 40 bytes of code and one var (a free "
    "VAR_ 0x40xx). No tile, no metatile, no map changes. The watch's dusk/night tint and DaemonsIsHalftone() work on "
    "the loaded rows, so they apply on top unchanged.",
    "RISKS: the field-move banners and the VERBOSE/FLASH fade reload palettes from the header (T-442's lesson): each "
    "such reload must go through the same case, or the cave snaps back to light 0 mid-visit -- check every caller of "
    "LoadSecondaryTilesetPalette and of gMapHeader.mapLayout->secondaryTileset->palettes. The wild encounters could "
    "follow the light (a different table per light, which is what Altering Cave's name promised in vanilla); that is "
    "a design question, not a palette one.",
]


def palette_lines(cave, key=None):
    """every palette entry the look changes, and what draws it: how many tiles, how many placements"""
    out = []
    draws = collections.defaultdict(lambda: [0, 0])
    for t in range(cave.n):
        for r, w in cave.rows[t].items():
            if r >= 7:
                draws[r][0] += 1
                draws[r][1] += w
    for r, ch in sorted(palette_touch(cave, key).items()):
        out.append("row %d (drawn by %d tiles, %d weighted placements):" % (r, draws[r][0], draws[r][1]))
        out.append("    " + "  ".join("%d %s %02x%02x%02x->%02x%02x%02x" % ((i, role.replace(" ", "")) + tuple(a) + tuple(b))
                                     for i, a, b, role in ch))
    return out


def write_draft(outdir):
    os.makedirs(outdir, exist_ok=True)
    made, info = [], {}
    for ts in DRAFTED:
        cave = Cave(ts)
        new, what = redraw(cave)
        pp = palettes(cave, True)
        d = os.path.join(outdir, ts)
        os.makedirs(os.path.join(d, "palettes_proposed"), exist_ok=True)
        tiles_png(cave, new, pp[8]).save(os.path.join(d, "tiles.png"))
        for r in range(8, 13):
            write_pal(os.path.join(d, "palettes_proposed", "%02d.pal" % r), pp[r])
        info[ts] = groups(cave, new, what)
        made.append((cave, new, what, pp, ts))
    caves = {}
    for key in DRAFTED_E2:
        ts = key.split("/")[0]
        cave = caves.setdefault(ts, Cave(ts))
        look = LOOKS[key]
        new, what = redraw(cave, key)
        pp = palettes(cave, True, key)
        d = os.path.join(outdir, key.replace("/", "_"))
        os.makedirs(os.path.join(d, "palettes_proposed"), exist_ok=True)
        if not look.get("base"):
            tiles_png(cave, new, pp[look.get("home", 8)]).save(os.path.join(d, "tiles.png"))
        for r in range(7, 13):
            write_pal(os.path.join(d, "palettes_proposed", "%02d.pal" % r), pp[r])
        info[key] = groups(cave, new, what, key)
        made.append((cave, new, what, pp, key))
    json.dump(dict(ticket="T-438 batch E", status="approved 2026-10-23 -- --write --approved builds it",
                   proposal=[{k: v for k, v in p.items()} for p in PROPOSAL], drafted=info,
                   other_cave_per_entry=PER_ENTRY),
              open(os.path.join(outdir, "groups.json"), "w"), indent=1, default=list)
    return made


def overview_sheet(made, path):
    """batch E2 on one page: each look's first crop, today beside the draft, at 1x"""
    f, F = font(13), font(20)
    tiles = []
    for cave, new, what, pp, key in made:
        if key not in DRAFTED_E2:
            continue
        name, x0, y0, w, h, _ = CROPS[key][0]
        w, h = min(w, 24), min(h, 16)
        a = render(cave, name, box=(x0, y0, w, h))
        b = render(cave, name, tiles=new, pals=pp, box=(x0, y0, w, h))
        look = LOOKS[key]
        tiles.append(_label(_row([_label(a, "today", f), _label(b, "draft", f)]), "%s -- %s\n%s" % (
            look["name"], look["motif"], name), font(14)))
    rows = [_row(tiles[k:k + 2], gap=24) for k in range(0, len(tiles), 2)]
    sheet = _col([_title("T-438 batch E2 DRAFT -- the remaining caves (not in the engine)\nUMBRAL ASCENT, OTHER CAVE and "
                         "STILLFALL are palette splits over their base's tiles; TANOBY (batch G) and DOLDRUM CAVE are "
                         "not here", F, max(r.width for r in rows))] + rows, gap=18)
    sheet.save(path)
    return path


def lights_sheet(cave, new, key, path):
    """OTHER CAVE's four lights in their cycle, each over the wild set it brings"""
    look = LOOKS[key]
    f, F = font(13), font(17)
    name, x0, y0, w, h, _ = CROPS[key][0]
    names = ["TEAL (the approved light)"] + ["%s -- %s" % (l["name"], l["stone"]) for l in look["lights"]]
    ims = [_label(render(cave, name, tiles=new, pals=palettes(cave, True, key, n), box=(x0, y0, 16, 12)).resize(
               (512, 384), Image.NEAREST), "light %d: %s\nentry %d, %d, ...; wild set %d" % (n, names[n], n + 1, n + 5, n),
               f) for n in range(1 + len(look["lights"]))]
    rows = [_row(ims[:2]), _row(ims[2:])]
    _col([_title("T-438 batch E2 -- OTHER CAVE's four lights, in the order they come (one a visit, then round again)",
                 F, max(r.width for r in rows))] + rows).save(path)
    return path


def sheets(made, outdir):
    os.makedirs(outdir, exist_ok=True)
    out = [proposal_sheet(os.path.join(outdir, "t438e_proposal.png"))]
    for cave, new, what, pp, key in made:
        s = SHORT[key]
        pre = "t438e" if key in DRAFTED else "t438e2"
        out.append(tiles_sheet(cave, new, what, os.path.join(outdir, "%s_%s_tiles.png" % (pre, s)), key))
        for k, crop in enumerate(CROPS[key][:3 if key in DRAFTED else 2], 1):
            out.append(map_sheet(cave, new, pp, crop, os.path.join(outdir, "%s_%s_%d.png" % (pre, s, k)), key))
    for cave, new, what, pp, key in made:
        if LOOKS[key].get("lights"):
            out.append(lights_sheet(cave, new, key, os.path.join(outdir, "t438e2_%s_lights.png" % SHORT[key])))
    out.append(overview_sheet(made, os.path.join(outdir, "t438e2_overview.png")))
    return out


# ================================================================== the report
def report():
    print("T-438 batch E -- a look per cave (approved 2026-10-23; --write --approved puts it in the engine)")
    for p in sorted(PROPOSAL, key=lambda p: p["order"]):
        print("\n  %-17s rank %-3d %s" % (p["ts"], p["order"], "DRAFTED" if p["drafted"] else "proposal only"))
        for pl in p["places"]:
            print("      %-16s %-36s %s" % pl)
        print("      look:  " + "\n             ".join(_wrap(p["look"], 100)))
        print("      split: " + "\n             ".join(_wrap(p["split"], 100)))
    caves = {}
    for key in DRAFTED + DRAFTED_E2:
        ts = key.split("/")[0]
        cave = caves.setdefault(ts, Cave(ts))
        look = LOOKS[key]
        new, what = redraw(cave, key)
        changed = sum(1 for t in range(cave.n) if new[t] != cave.tiles[t])
        touch = palette_touch(cave, key)
        print("\n  %s (%s)%s: %s%d palette entries proposed in rows %s; maps: %d" % (
            look["name"], key, " APPROVED 2026-10-23" if key in DRAFTED else " batch E2, APPROVED 2026-10-23",
            "a palette split over %s's tiles; " % LOOKS[look["base"]]["name"] if look.get("base") else
            "%d of %d tiles redrawn; " % (changed, cave.n), sum(len(v) for v in touch.values()), sorted(touch),
            len(split_maps(cave, key)) if look.get("base") else len(cave.maps)))
        if key in DRAFTED_E2:
            for l in palette_lines(cave, key):
                print("      " + l)
        if COMPROMISES.get(ts) and not look.get("base"):
            print("      accent shown in another row's colour on a few placements: %s" % COMPROMISES[ts])
        moved = [t for t in range(cave.n) if any((a == 0) != (b == 0) for a, b in zip(new[t], cave.tiles[t]))]
        print("      footprint: %s" % ("every tile keeps its transparent pixels" if not moved else
                                       "!! tiles %s change their footprint" % moved))
    print("\n  OTHER CAVE, a light per entry (a cycle of four, built):")
    for l in PER_ENTRY:
        print("      " + "\n        ".join(_wrap(l, 108)))


def write_engine():
    """every approved cave into the engine: the drawn ones' tiles.png and the rows their look changes; each palette
    split's rows 7..12 in its own folder beside its base (the Tileset header in headers.h names them), and OTHER CAVE's
    other three lights in palettes_other_1..3. Nothing else: no metatile, attribute or map is touched."""
    caves = {}
    for key in DRAFTED + DRAFTED_E2:
        ts = key.split("/")[0]
        cave = caves.setdefault(ts, Cave(ts))
        look = LOOKS[key]
        pp = palettes(cave, True, key)
        if look.get("base"):
            sets = [(SPLIT_DIR[key], pp)] + [("%s_%d" % (SPLIT_DIR[key], n), palettes(cave, True, key, n))
                                             for n in range(1, len(look.get("lights", [])) + 1)]
            for rel, pals in sets:
                d = os.path.join(GBA, SEC + rel)
                os.makedirs(d, exist_ok=True)
                for r in range(7, 13):
                    write_pal(os.path.join(d, "%02d.pal" % r), pals[r])
            print("  wrote %s: a palette split, rows 7..12 in %s" % (look["name"], ", ".join(r for r, _ in sets)))
            continue
        new, what = redraw(cave, key)
        if any((a == 0) != (b == 0) for t in range(cave.n) for a, b in zip(new[t], cave.van[t])):
            raise SystemExit("  !! %s: a tile's footprint moved -- nothing written" % key)
        tiles_png(cave, new).save(os.path.join(cave.dir, "tiles.png"), bits=4)
        rows = [r for r in range(7, 13) if pp[r] != cave.pals[r]]
        for r in rows:
            write_pal(os.path.join(cave.dir, "palettes/%02d.pal" % r), pp[r])
        print("  wrote %s (%s): %d tiles redrawn, palette rows %s" % (look["name"], ts, len(what), rows or "none"))


def main():
    if WRITE and "--approved" not in ARGS:
        print("  --write refused: T-438 batch E is written only with --approved (the user approved every cave here "
              "on 2026-10-23).")
        return 0
    if WRITE:
        write_engine()
        return 0
    if DRAFT is not None:
        made = write_draft(DRAFT)
        for p in sheets(made, SHEETS):
            print("  wrote %s" % p)
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())

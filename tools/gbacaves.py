#!/usr/bin/env python3
"""A look per cave (T-438 batch E): each cave's secondary tileset redrawn in code, matched to its name.

    python3 tools/gbacaves.py                       # report: every cave-like tileset, the maps that use it, their
                                                    #   DAEMONS names, the look proposed for each, what is drafted
    python3 tools/gbacaves.py --draft [DIR]         # the drafted caves' tiles.png and palettes, groups.json, and the
                                                    #   contact sheets, in DIR (gfx/drafts/t438/caves/); --sheets DIR
                                                    #   puts the sheets elsewhere
    python3 tools/gbacaves.py --write --approved    # into the engine -- NOT YET: batch E is a draft until the user has
                                                    #   seen the sheets; without --approved --write refuses

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
#  player first meets it (the census's rank). `drafted` marks the three this batch draws.
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
               "pale mineral teal. A per-entry palette swap would make it never the same twice; that is a question."),
    dict(ts="underground_path", order=14, drafted=False,
         places=[("UNDERGROUND PATH", "UndergroundPath_NorthSouth/EastWest", "officially UNDERGROUND PATH, locally "
                  "THE TUNNEL: routing around a blocked path, as a VPN does (3.1)")],
         look="THE TUNNEL. Not a cave but a built bore: a concrete tube with a lit lane down the middle, conduit along "
              "both walls, a dashed centre line like a packet trace. Light: sodium-free white and cool concrete, the "
              "most ordered underground in the game, so the caves read as caves beside it.",
         split="Its own tileset already; it draws primary/building (batch D's palettes sit under it)."),
    dict(ts="power_plant", order=23, drafted=False,
         places=[("KEEPALIVE PLANT", "PowerPlant", "a building still running with nobody connected to it; SENTINEL "
                  "lives there (3.3)")],
         look="STILL RUNNING. A plant left on: floor plates and machine housings, and the one motif is a status light "
              "on every housing, all green. Light: plant-green and machine grey-blue, with the living PLANT's second "
              "meaning in moss along the seams.",
         split="Its own tileset; batch D left its machines for this batch or its town's."),
    dict(ts="seafoam_islands", order=44, drafted=False,
         places=[("GLAUCOUS ISLES", "SeafoamIslands_1F..B4F", "Seafoam: named for its surface, and what matters is "
                  "four floors under it (3.3)"),
                 ("STILLFALL CAVE", "FourIsland_IcefallCave x4", "Icefall: a waterfall that stopped (2.10)"),
                 ("SEVEN ISLAND", "SevenIsland_House_Room1", "one room")],
         look="THE BLOOM. GLAUCOUS (our reading) is the powdery blue-green bloom on a plum or a leaf: ice under a matte "
              "frosted skin, lit tops chalky, faces clear and deep. Its rows 8..12 were already recoloured (census).",
         split="SPLIT STILLFALL (palette split): the ice gone glassy and still, frozen falls -- its own tiles later."),
    dict(ts="mt_ember", order=51, drafted=False,
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
    dict(ts="navel_rock", order=76, drafted=False,
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

# the three this batch draws, first met first
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


_GENERAL = None


def general():
    """primary/general as the engine has it now: its tiles, rows 0..6, its metatiles"""
    global _GENERAL
    if _GENERAL is None:
        d = os.path.join(GBA, GEN)
        _GENERAL = dict(tiles=tiles_of(Image.open(os.path.join(d, "tiles.png"))),
                        pals=[read_pal(os.path.join(d, "palettes/%02d.pal" % r)) for r in range(16)],
                        mt=open(os.path.join(d, "metatiles.bin"), "rb").read())
    return _GENERAL


class Cave:
    """one secondary tileset: its tiles and palettes as they are now, and where each tile is drawn"""

    def __init__(self, ts):
        self.ts = ts
        self.dir = os.path.join(GBA, SEC + ts)
        self.im = Image.open(os.path.join(self.dir, "tiles.png"))
        self.tiles = tiles_of(self.im)
        self.van = tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, SEC + ts + "/tiles.png", binary=True))))
        self.pals = [read_pal(os.path.join(self.dir, "palettes/%02d.pal" % r)) for r in range(16)]
        self.mt = open(os.path.join(self.dir, "metatiles.bin"), "rb").read()
        self.attr = open(os.path.join(self.dir, "metatile_attributes.bin"), "rb").read()
        self.n = len(self.tiles)
        self.maps = sorted(n for n, l in layouts().items()
                           if l["secondary_tileset"] == "gTileset_" + "".join(w.title() for w in ts.split("_"))
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
    G = general()
    l = layouts()[mapname]
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


def palettes(cave, proposed=True):
    """the secondary's sixteen rows: today's, or the look's -- each named index given its role's colour"""
    pals = [list(p) for p in cave.pals]
    if not proposed:
        return pals
    look = LOOKS[cave.ts]
    for r, plan in MATERIALS[cave.ts].items():
        for i, (mat, k) in plan.items():
            ramp = look["pal"].get(mat)
            if ramp:
                pals[r][i] = ramp[min(k, len(ramp) - 1)]
        for k, i in enumerate(ACCENT.get(cave.ts, {}).get(r, [])):
            pals[r][i] = look["pal"]["accent"][k]
    return pals


def palette_touch(cave):
    """row -> [(index, today, proposed, its role)] for every index the look changes"""
    now, new = palettes(cave, False), palettes(cave, True)
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


def redraw(cave):
    """every tile of the tileset in the look: (new tiles, {tile: what it is}), footprints and joins kept.

    Each tile is drawn where it is drawn most: in its main block's layer, so the light around a pixel, the joins and
    the rim are read across the tile's edges from the three tiles beside it, and the motif is laid at the tile's own
    place in the block (a block is 16x16, the motif's period, so it runs on across blocks)."""
    look = LOOKS[cave.ts]
    plans = MATERIALS[cave.ts]
    new, what = [], {}
    COMPROMISES.pop(cave.ts, None)
    for t in range(cave.n):
        px = cave.tiles[t]
        rows = [r for r in cave.rows[t] if r >= 7]
        where = placement(cave, t)
        if not rows or not any(px) or t in OBJECTS or not where:
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
        face = lambda x, y: 0 <= y < 16 and base[y][x] is not None and base[y][x] > TOP_AT
        top = lambda x, y: 0 <= y < 16 and base[y][x] is not None and base[y][x] <= TOP_AT
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
                    plane = "top" if b0 <= TOP_AT else "face"
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
SHORT = {"cave": "deadstack", "digletts_cave": "tappoint", "rock_tunnel": "blackout"}
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


def map_sheet(cave, new, pals, crop, path):
    name, x0, y0, w, h, what = crop
    look = LOOKS[cave.ts]
    a = render(cave, name, box=(x0, y0, w, h))
    b = render(cave, name, tiles=new, pals=pals, box=(x0, y0, w, h))
    f, F = font(13), font(17)
    z2 = lambda im: im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    rows = [_label(_row([_label(a, "today (vanilla) 1x", f), _label(b, "draft: %s 1x" % look["motif"], f)]), "", f),
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
                         "collision unchanged" % (look["name"], cave.ts, what, name, x0, y0, w, h), F,
                         max(r.width for r in rows))] + rows)
    sheet.save(path)
    return path


def swatch_rows(cave, pals_now, pals_new, f):
    """rows 8..12, today over proposed, every index boxed and labelled with its role"""
    Z = 26
    ims = []
    plans = MATERIALS[cave.ts]
    for r in range(8, 13):
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
        r = cave.home(t) or 8
        for k, v in enumerate(tiles[t]):
            if not v:
                continue
            x, y = (t % w) * 8 + k % 8, (t // w) * 8 + k // 8
            for a in range(Z):
                for b in range(Z):
                    o[x * Z + a, y * Z + b] = pals[r][v]
    return im


def tiles_sheet(cave, new, what, path):
    f, F = font(12), font(17)
    look = LOOKS[cave.ts]
    now, pp = palettes(cave, False), palettes(cave, True)
    counts = collections.Counter(what.values())
    top = _row([_label(atlas(cave, cave.tiles, now), "tiles.png today, each tile in its own row", f),
                _label(atlas(cave, new, pp), "draft: %d tiles redrawn (%s)\nboulders, rocks, ladders, holes, "
                       "water keep their drawing" % (len(what), ", ".join("%s %d" % kv for kv in sorted(counts.items()))),
                       f)])
    sw = swatch_rows(cave, now, pp, f)
    sheet = _col([_title("T-438 batch E DRAFT -- %s: the tileset and its palettes\nrows 8..12: today above, "
                         "proposed below, red where changed" % look["name"], F, max(top.width, sw[0].width)), top] + sw)
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
        cells = [_wrap("%s%s" % (p["ts"], "  [DRAFTED]" if p["drafted"] else ""), cols[0][1]) +
                 ["", "rank %d" % p["order"]],
                 sum((_wrap("%s -- %s -- %s" % pl, cols[1][1]) + [""] for pl in p["places"]), []),
                 _wrap(p["look"], cols[2][1]), _wrap(p["split"], cols[3][1])]
        rows.append((p, cells, max(len(c) for c in cells)))
    cw = [n * 8 + 16 for _, n in cols]
    W = sum(cw) + 24
    H = 70 + sum(n * lh + 14 for _, _, n in rows) + 30 + 60
    im = Image.new("RGB", (W, H), (244, 242, 236))
    d = ImageDraw.Draw(im)
    d.text((12, 10), "T-438 batch E -- a look per cave (PROPOSAL; the first three drafted, nothing in the engine)",
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
            for k, rgb in enumerate([pp[8][i] for i in (1, 2, 3, 4, 9, 10, 11, 12, 13, 14)] +
                                    [pp[8][i] for i in ACCENT[p["ts"]].get(8, [])[:2]]):
                d.rectangle([12 + k * 14, y + n * lh - 16, 12 + k * 14 + 12, y + n * lh - 4], fill=rgb)
        y += n * lh + 14
    for k, l in enumerate(["Grey is not a look here: HALFTONE and the unread DOLDRUM CAVE own it (8.6a, T-251), and "
                           "DaemonsIsHalftone() greys DOLDRUM's screen whatever its tileset is.",
                           "A palette split is a new Tileset header reusing the tiles and metatiles with its own "
                           "palettes (192 bytes, no tiles): the cheap way to give a shared cave a light of its own."]):
        d.text((12, y + 8 + k * lh), l, font=f, fill=(90, 40, 30))
    im.save(path)
    return path


def groups(cave, new, what):
    by = collections.defaultdict(list)
    for t, k in sorted(what.items()):
        by[k].append(t)
    kept = sorted(t for t in range(cave.n) if any(cave.tiles[t]) and t not in what and cave.rows[t])
    return dict(redrawn={k: v for k, v in by.items()}, kept_drawing=kept,
                objects=sorted(OBJECTS), compromises=COMPROMISES.get(cave.ts, []),
                maps=cave.maps,
                palette_proposal={r: [dict(index=i, today=a, proposed=b, role=role) for i, a, b, role in v]
                                  for r, v in palette_touch(cave).items()})


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
        made.append((cave, new, what, pp))
    json.dump(dict(ticket="T-438 batch E", status="DRAFT -- not in the engine",
                   proposal=[{k: v for k, v in p.items()} for p in PROPOSAL], drafted=info),
              open(os.path.join(outdir, "groups.json"), "w"), indent=1, default=list)
    return made


def sheets(made, outdir):
    os.makedirs(outdir, exist_ok=True)
    out = [proposal_sheet(os.path.join(outdir, "t438e_proposal.png"))]
    for cave, new, what, pp in made:
        s = SHORT[cave.ts]
        out.append(tiles_sheet(cave, new, what, os.path.join(outdir, "t438e_%s_tiles.png" % s)))
        for k, crop in enumerate(CROPS[cave.ts], 1):
            out.append(map_sheet(cave, new, pp, crop, os.path.join(outdir, "t438e_%s_%d.png" % (s, k))))
    return out


# ================================================================== the report
def report():
    print("T-438 batch E -- a look per cave (DRAFT; nothing here is in the engine)")
    for p in sorted(PROPOSAL, key=lambda p: p["order"]):
        print("\n  %-17s rank %-3d %s" % (p["ts"], p["order"], "DRAFTED" if p["drafted"] else "proposal only"))
        for pl in p["places"]:
            print("      %-16s %-36s %s" % pl)
        print("      look:  " + "\n             ".join(_wrap(p["look"], 100)))
        print("      split: " + "\n             ".join(_wrap(p["split"], 100)))
    for ts in DRAFTED:
        cave = Cave(ts)
        new, what = redraw(cave)
        changed = sum(1 for t in range(cave.n) if new[t] != cave.tiles[t])
        touch = palette_touch(cave)
        print("\n  %s (%s): %d of %d tiles redrawn; %d palette entries proposed in rows %s; maps: %d" % (
            LOOKS[ts]["name"], ts, changed, cave.n, sum(len(v) for v in touch.values()), sorted(touch),
            len(cave.maps)))
        if COMPROMISES.get(ts):
            print("      accent shown in another row's colour on a few placements: %s" % COMPROMISES[ts])
        moved = [t for t in range(cave.n) if any((a == 0) != (b == 0) for a, b in zip(new[t], cave.tiles[t]))]
        print("      footprint: %s" % ("every tile keeps its transparent pixels" if not moved else
                                       "!! tiles %s change their footprint" % moved))


def main():
    if WRITE and "--approved" not in ARGS:
        print("  --write refused: T-438 batch E is a draft until the user has approved its sheets.")
        print("  (When they have: --write --approved writes the drafted caves' tiles.png and rows 8..12 of their "
              "palettes into %s{%s}.)" % (SEC, ",".join(DRAFTED)))
        return 0
    if WRITE:
        for ts in DRAFTED:
            cave = Cave(ts)
            new, what = redraw(cave)
            tiles_png(cave, new).save(os.path.join(cave.dir, "tiles.png"))
            pp = palettes(cave, True)
            for r in range(8, 13):
                write_pal(os.path.join(cave.dir, "palettes/%02d.pal" % r), pp[r])
            print("  wrote %s: %d tiles, palettes 8..12" % (ts, len(what)))
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

#!/usr/bin/env python3
"""The primary general tileset's last Nintendo drawings (T-542): the census, the batches, and batch 1 drawn three ways.

    python3 tools/gbaprimary.py                    # report: every General tile still pixel-identical to pret's and
                                                   #   drawn by some layout, by object -- count, blocks, maps, what
                                                   #   engine code or script names its blocks -- and the batch it is
                                                   #   in; batch 1's checks (rows, reserved indices, animations, doors,
                                                   #   setmetatile, every other tool's hold on these tiles)
    python3 tools/gbaprimary.py --draft [DIR]      # batch 1 in each direction as a full tiles.png in DIR/A, DIR/B,
                                                   #   DIR/C (gfx/drafts/t542/), census.json and directions.json, and
                                                   #   the sheets: each direction beside today at 1x on real maps, a
                                                   #   3x detail, and every tile at 3x
    python3 tools/gbaprimary.py --write --approved --pick X
                                                   # into the engine: batch 1 in direction X. Refused unless X is in
                                                   #   APPROVED ({"A"}: the user, 2026-11-10, "A Hearth"); with
                                                   #   one direction approved the report compares the engine with
                                                   #   that write and exits 1 on any difference
    python3 tools/gbaprimary.py --draft --batch 2  # (--batch 1 drafts batch 1 again) batch 2 THE TOWN PIECES into
                                                   #   gfx/drafts/t542_b2/: A, B, C tiles.png, directions.json, and the
                                                   #   sheets -- each town map today beside the draft (the town pieces
                                                   #   are one drawing in every direction), the cave mouth in all
                                                   #   three, and the 75 tiles at 3x
    python3 tools/gbaprimary.py --write --batch 2 --approved --pick X
                                                   # batch 2 into the engine: refused unless X is in APPROVED_B2
                                                   #   ({"A"}: the user, 2026-11-10, "build as drawn; cave mouth A")
    python3 tools/gbaprimary.py --draft            # (batch 3, the default for --draft since batches 1 and 2 are built)
                                                   #   batch 3 THE EDGES AND DOORS into gfx/drafts/t542_b3/: A, B, C
                                                   #   tiles.png, directions.json, and the sheets -- each map today beside
                                                   #   the draft (everything but the doors is one drawing), the doors in
                                                   #   all three and opening as gbadoors draws them, the 24 tiles at 3x
    python3 tools/gbaprimary.py --write --batch 3 --approved --pick X
                                                   # batch 3 into the engine: refused unless X is in APPROVED_B3 (empty:
                                                   #   a draft); then gbadoors.py --write --approved for the door frames

WHAT IS LEFT (census item 7, re-measured on today's engine). T-438 batch C (gbageneral.py) re-surfaced General's
ground -- the rock, the LEDGES, sand and paving -- and drew its motifs: the FENCES, the SIGNPOSTS, the bushes and the
blue house's roof. So no ledge, fence or signboard tile is still Nintendo's drawing, and the boulders are object
sprites (already ours). What is left is the BUILDINGS General lends to every outdoor map, a few water edges, a few
ground strays and three doors. A tile is LEFT when its 64 pixels are pret's and a layout on General draws it.

    left in tiles.png                   210
      under the water animation          44  (416..481: VRAM shows gbawater's strips, never tiles.png -- trap 39)
      one flat colour                     6  (nothing in them to redraw)
      only on layouts no map uses         8
      SEEN by a player                  152  = batch 1 53 + batch 2 75 + batch 3 24

    BATCH 1  THE ROAD GATES (53 tiles, 58 blocks, General's own rows only): the twelve gatehouses' roofs, fronts,
             window strips and doorways, the east-west gates' side doors, the posts behind every gate, the ROUTE 12
             house's last blue pieces, and the stone stairs of the islands and the SAFARI. Drawn here, three ways.
    BATCH 2  THE TOWN PIECES (75): tiles General lends to the towns and drawn in THEIR rows (VERDIGRIS and LURID's
             row 12, DOLDRUM's 10/11/12, BRAZEN's 11, CALLOW's 11, ARDOR's 8, HALFTONE's 12, the islands' 12), the
             pieces a town draws in General's rows, the cave mouth (also SEVII row 12) and one cliff piece. Each in
             its own town's look (gbatowns.py's motifs, at the tile's home); only the cave mouth is a real choice
             (A THE ROCK'S OWN MOUTH, B THE ADIT, C THE PORTAL). Drafted 2026-11-10 (B2 below); gbageneral's
             LATER_T542 claims all 75, so its pass 3 no longer draws 298 and 330.
    BATCH 3  THE EDGES AND DOORS (24): the ground strays (a sand edge on 39 maps, beach sand, grass edges, plants),
             the sea's edge and FOUR ISLAND's puddles (gbawater.py's to agree with), and the sliding doors 0x62/0x15B,
             whose opening frames gbadoors.py derives from the closed block -- so gbadoors re-runs after them.
             Drafted 2026-11-10 (B3 below): all dictated but the doors (A THE CLEAR PANE, B THE READOUT, C THE
             MANIFESTATION); 21 of 24 redrawn, 4, 301 and 503 all edge and already met; gbageneral's LATER_T542
             claims all 24.

THE RULES (as gbamuseum and gbadwellings keep them). Nothing but pixels inside batch 1's 53 tiles moves: no block,
layer, flip, palette row, behaviour, collision or map. No palette changes -- General's rows 0..6 are every outdoor
map's. Every tile keeps its FOOTPRINT (index 0 stays 0, a drawn pixel stays drawn), its OUTLINE (row 5's index 5,
rows 2 and 3's index 7 -- the dark navy every building is outlined in) and every pixel that touches transparency.
Inside, each pixel's MATERIAL (its row's grey, gold, blue, warm, teal, cream...) and its TONE (its place on that
ramp, which carries vanilla's light) go to the direction's painter for the tile's PART, which may move a material to
another ramp of the SAME row. Never used: row 2 index 8 (the CHECKPOINT's day trim, fieldmap.c) and rows 4 and 6
index 1 (the water's crest) -- the runtime writes the day's colour there. A tile some block draws flipped is drawn
mirror-symmetric, so it meets itself.

THE OTHER TOOLS. Every tool that writes General's tiles.png starts from the engine's own file and draws its own
tiles; gbageneral.py writes only tiles still identical to pret's, so once batch 1 is in, nothing of T-438 C can put
these back. The report holds every batch 1 tile to two states only -- pret's drawing (before the write) or the
approved pick's (after) -- and fails, naming it, on anything else: another tool has drawn there, find which side is
right. The write refuses then too. After a build, `check_generators.py --writes` is the full proof.
"""
import collections, glob, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t542")

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
    DRAFT = DRAFT_DEFAULT                # batch 1's folder; batch 2 drafts into DRAFT_B2 (gfx/drafts/t542_b2/)
PICK = argval("--pick")

#  The user's pick goes here ("A", "B" or "C"); --write refuses anything not in it.
APPROVED = {"A"}                     # the user, 2026-11-10: A Hearth

#  gbageneral (T-438 C) reads the engine at import and holds the census, the map renderer and the block tables; it is
#  a writing tool, so it is loaded with an empty argv (engine.md trap 16) and only its functions are used.
_argv, sys.argv = sys.argv, ["gbageneral"]
try:
    import gbageneral as G
finally:
    sys.argv = _argv

# ================================================================== batch 1, by object
OBJECTS = collections.OrderedDict([
    ("roof",    ("the road gate's roof (ridge, slope, eave)", [197, 198, 199, 213, 214, 215, 229, 230, 231])),
    ("wall",    ("the road gate's front wall and its band", [246, 233, 278])),
    ("pillar",  ("the road gate's corner piers", [245, 247, 261, 263, 277, 279])),
    ("window",  ("the road gate's window strip", [611, 612, 613, 614, 627, 628, 629, 630])),
    ("door",    ("the road gate's doorway, lintel and steps", [388, 389, 390, 391, 402, 403, 404, 405, 406, 407])),
    ("wing",    ("the east-west gates' side doors", [212, 228, 244, 260, 276, 400])),
    ("post",    ("the posts behind every gate", [386, 387])),
    ("blue",    ("ROUTE 12's house: its last blue pieces", [345, 346, 378, 557, 558, 573, 574])),
    ("stairs",  ("the stone stairs (islands, SAFARI, DOLDRUM CAVE)", [294, 295])),
])
BATCH1 = sorted(t for _, ts in OBJECTS.values() for t in ts)
PART = {t: k for k, (_, ts) in OBJECTS.items() for t in ts}

#  batch 3, by object (anything seen and not named here or in B2 below is reported as unplaced, and fails the report);
#  B3 below draws them
LATER = collections.OrderedDict([
    ("3 ground strays: sand edge, beach sand, grass edges, plants", (3, [4, 11, 27, 43, 59, 79, 94, 301, 503])),
    ("3 the sea's edge (gbawater's to agree with)", (3, [173, 174, 189, 190, 617, 618])),
    ("3 FOUR ISLAND's puddles", (3, [311, 326, 342, 358, 359])),
    ("3 the sliding doors 0x62 / 0x15B (gbadoors re-runs after)", (3, [269, 285, 292, 293])),
])

DOOR_BLOCKS = {0x03D, 0x062, 0x15B}                  # src/field_door.c's General entries
RESERVED = {(2, 8), (4, 1), (6, 1)}                 # fieldmap.c writes the day's colour into these at runtime
OUTLINE = {5: {5}, 2: {7}, 3: {7}}

# ================================================================== the palette, as materials
MATS = {5: {"grey": [1, 2, 3, 4], "gold": [6, 7, 8, 9], "yellow": [10, 11, 12], "green": [13, 14, 15]},
        2: {"grey": [1, 2, 3, 4, 5, 6], "warm": [10, 11, 12, 13, 14], "teal": [15, 9]},
        3: {"grey": [1, 2, 3, 4, 5, 6], "cream": [8, 9], "blue": [10, 11, 12, 13, 14], "green": [15]}}


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


for _r, _ms in MATS.items():                         # every ramp light to dark, as the palette really is
    for _m in _ms:
        _ms[_m] = sorted(_ms[_m], key=lambda i: -lum(G.PALS[_r][i]))
MAT_OF = {r: {i: m for m, ix in ms.items() for i in ix} for r, ms in MATS.items()}


def ink(row, mat, level):
    """the index at LEVEL (0 light .. 1 dark) of MAT's ramp in ROW"""
    ramp = MATS[row][mat]
    level = min(1.0, max(0.0, level))
    return ramp[int(round(level * (len(ramp) - 1)))]


def tone(row, v):
    ramp = MATS[row][MAT_OF[row][v]]
    return ramp.index(v) / max(1, len(ramp) - 1)


# ================================================================== the three directions
#  Each painter takes (part, material, x, y, tone) -- x, y inside the tile, mirror-folded when the tile is drawn
#  flipped -- and returns (material, level) to paint, or None to keep vanilla's pixel. Patterns repeat every 4 or 8,
#  so a tile meets the one beside it whatever block it is in.
def h(x, y, k=0):
    return ((x * 7 + y * 13 + k * 5) * 2654435761 >> 7) % 97


def paint_A(part, row, mat, x, y, t):
    """A HEARTH -- the toll cottage: T-538's road houses (the user's pick, A HEARTH) carried out to their own front.
    Thatch in row 5's straw, limewash, quarry-tile piers, leaded lights in oak, terracotta steps, oak posts"""
    if part == "roof" and mat == "grey":
        lv = 0.1 + 0.55 * t + (0.3 if (x * 5 + y * 3) % 7 == 0 else 0) - (0.15 if x % 4 == 1 else 0)
        return "gold", lv
    if part == "wall":
        if mat == "grey":
            return "grey", 0.05 + 0.45 * t + (0.25 if h(x, y) % 9 == 0 else 0)
        if mat == "gold":                                  # quarry-stone courses under the sill
            joint = y % 4 == 3 or (x + (y // 4) % 2 * 4) % 8 == 7
            return "gold", 0.95 if joint else (0.05 if y % 4 == 0 else 0.35)
    if part == "pillar" and mat == "grey":                 # terracotta quarry tiles, three to a course
        if y % 3 == 2:
            return "warm", 0.75
        return "warm", 0.0 if y % 3 == 0 else 0.25 + 0.3 * t
    if part == "window":
        if mat == "blue":                                  # leaded lights: a diamond came over the glass
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                return "grey", 0.8
            return "blue", 0.2 + 0.6 * t
        if mat == "cream":                                 # the oak sill
            return "cream", 1.0 if x % 3 == 0 else 0.0
    if part == "door":
        if t > 0.6:
            return None                                    # the doorway's dark stays dark
        if row == 3 and mat == "grey":                     # an oak frame
            return "cream", 0.0 if x <= 2 else 1.0
        if row == 5 and mat == "grey":                     # an oak lintel, grained
            return "gold", 0.2 + 0.4 * t + (0.4 if (x + y * 3) % 5 == 0 else 0)
        if row == 2 and mat == "grey":                     # flagstone steps, a joint in each
            return "grey", 0.6 if x % 8 == 3 else 0.1 + 0.4 * t
    if part == "wing" and mat == "grey":
        return "grey", 0.05 + 0.5 * t + (0.25 if h(x, y, 1) % 11 == 0 else 0)
    if part == "post" and mat == "grey":
        return "gold", 0.1 + 0.6 * t + (0.3 if x % 3 == 2 else 0)
    if part == "blue" and mat == "blue":                   # glazed pantiles
        if y % 4 == 3:
            return "blue", 0.85
        return "blue", 0.1 + 0.4 * t + (0.3 if (x % 4 in (0, 3) and y % 4 == 2) else 0)
    if part == "stairs" and mat == "grey":                 # flags, worn at the nosing
        if t < 0.3:
            return "grey", 0.65 if (x + (y // 4) * 3) % 8 == 7 else (0.0 if y % 4 == 1 else 0.15)
        return "grey", 0.75 + (0.25 if (x * 3 + y) % 6 == 0 else 0)
    return None


def paint_B(part, row, mat, x, y, t):
    """B THE WAYMARK -- the numbered road's office (3.2: the official map keeps the numbers): slate roof, dressed
    ashlar, stone quoins, sash windows over a blank blue enamel band, milestones, slate treads"""
    if part == "roof" and mat == "grey":
        if t > 0.7:
            return "grey", 1.0
        if y % 4 == 3:
            return "grey", 0.67                             # each course's shadow line
        if (x + 4 * ((y // 4) % 2)) % 8 == 7:
            return "grey", 0.67                             # the joint between two slates, staggered
        return "grey", 0.0 if y % 4 == 0 else 0.33          # a slate, lit along its top
    if part == "wall":
        if mat == "grey":
            return "grey", 0.6 if (y % 4 == 3 or (x + (y // 4) % 2 * 4) % 8 == 7) else 0.05 + 0.3 * t
        if mat == "gold":
            if y % 4 == 3 or (x + (y // 4) % 2 * 4) % 8 == 7:
                return "gold", 1.0
            return "gold", 0.0 if y % 4 == 0 else 0.4
    if part == "pillar" and mat == "grey":                 # quoins: long and short blocks in turn
        if y % 4 == 3:
            return "grey", 0.75
        if (y // 4) % 2 and x >= 5:
            return "grey", 0.55
        return "grey", 0.0 if y % 4 == 0 else 0.2 + 0.2 * t
    if part == "window":
        if mat == "blue":
            if x % 4 == 0 or y % 8 == 5:
                return "grey", 0.0                          # white glazing bars
            return "blue", 0.0 if (x - y) % 8 == 0 else 0.35 + 0.5 * t
        if mat == "cream":                                 # the blank enamel band: a white edge, a blue field
            return ("grey", 0.0) if t == 1.0 else ("blue", 0.95)
    if part == "door":
        if t > 0.6:
            return None
        if mat == "grey" and row == 3:                     # a stone architrave
            return "grey", 0.6 if y % 4 == 3 else 0.05 + 0.25 * t
        if mat == "grey" and row == 5:                     # a keystoned lintel
            return "grey", 0.85 if x % 4 == 3 else 0.1 + 0.3 * t
        if mat == "grey" and row == 2:                     # slate treads, each lit at its nosing
            return "grey", 0.0 if y % 3 == 0 else 0.5
    if part == "wing" and mat == "grey":
        return "grey", 0.6 if (y % 4 == 3) else 0.05 + 0.35 * t
    if part == "post" and mat == "grey":                   # a milestone with a blank face
        return "grey", 0.0 if x % 4 in (1, 2) else 0.3 + 0.4 * t
    if part == "blue" and mat == "blue":                   # enamel panels, standing seams
        return "blue", 0.95 if x % 4 == 3 else (0.0 if x % 4 == 0 else 0.35 + 0.3 * t)
    if part == "stairs" and mat == "grey":
        if t < 0.3:
            return "grey", 0.0 if y % 4 == 1 else 0.45     # slate tread, lit lip
        return "grey", 1.0
    return None


def paint_C(part, row, mat, x, y, t):
    """C THE LATCH -- the gate as a latch on the bus, the world as the running machine it is: a finned heat-sink
    roof, a row of gold legs under the eave, a gold edge-connector for the brick band, teal board piers with a copper
    trace, status lamps for windows, a shutter for a door, header pins for posts"""
    if part == "roof" and mat == "grey":
        if t > 0.7:                                        # under the eave: the chip's legs
            return ("gold", 0.3) if x % 4 in (1, 2) else ("grey", 1.0)
        if t < 0.05:
            return "grey", 0.0
        return "grey", [0.0, 0.35, 0.65, 1.0][x % 4]
    if part == "wall":
        if mat == "grey":
            return "grey", 0.55 + 0.4 * t
        if mat == "gold":                                  # an edge connector: gold fingers
            return "gold", 0.0 if x % 4 in (1, 2) and y % 4 != 3 else 1.0
    if part == "pillar" and mat == "grey":
        if x in (3, 4):
            return "warm", 0.25 if y % 4 else 0.0          # a copper trace up the board
        return "teal", 0.0 if t < 0.4 else 1.0
    if part == "window":
        if mat == "blue":                                  # status lamps on dark glass
            if x % 4 == 1 and y % 8 in (4, 5):
                return "blue", 0.0
            if x % 4 in (0, 2) and y % 8 in (4, 5):
                return "blue", 0.25
            return "blue", 1.0
        if mat == "cream":
            return "cream", 0.0 if x % 2 == 0 else 1.0
    if part == "door":
        if t > 0.6:
            return None
        if mat == "grey":                                  # a shutter: slats
            return "grey", 0.1 if y % 2 == 0 else 0.6
    if part == "wing" and mat == "grey":
        if y % 4 == 1:
            return "warm", 0.25
        return "teal", 0.0 if t < 0.4 else 1.0
    if part == "post" and mat == "grey":
        return "gold", 0.0 if x % 3 == 1 else 0.3 + 0.5 * t
    if part == "blue" and mat == "blue":
        return "blue", 0.0 if y % 4 == 0 else 0.5 + 0.3 * t
    if part == "stairs" and mat == "grey":
        if t < 0.3:
            return ("warm", 0.0) if y % 4 == 1 else ("grey", 0.3)
        return "grey", 1.0
    return None


STYLES = collections.OrderedDict([
    ("A", dict(title="HEARTH", paint=paint_A,
               blurb="the toll cottage: the road houses' HEARTH (T-538 A) carried out to their front -- thatch in "
                     "row 5's straw, limewash, terracotta quarry-tile piers, leaded lights in oak, flagstone steps")),
    ("B", dict(title="THE WAYMARK", paint=paint_B,
               blurb="the numbered road's office (3.2): slate roof, dressed ashlar, quoins, sash windows over a "
                     "blank blue enamel band, milestones, slate treads -- every material kept on its own ramp")),
    ("C", dict(title="THE LATCH", paint=paint_C,
               blurb="the gate as a latch on the bus: a finned heat-sink roof on gold legs, a gold edge-connector, "
                     "teal board piers with a copper trace, status lamps, a shutter door, header pins")),
])


# ================================================================== reading what places each tile
def flips_of(tiles):
    """tile -> (drawn h-flipped somewhere, drawn v-flipped somewhere), over every General block"""
    out = {t: [False, False] for t in tiles}
    for b in range(len(G.GMT) // 16):
        for e in G.entries(G.GMT, b):
            t = e & 0x3FF
            if t in out:
                out[t][0] |= bool(e & 0x400)
                out[t][1] |= bool(e & 0x800)
    return out


def draw_tile(t, row, paint, flip):
    van = G.VAN[t]
    out = list(van)
    for y in range(8):
        for x in range(8):
            v = van[y * 8 + x]
            if v == 0 or v in OUTLINE[row] or v not in MAT_OF[row]:
                continue
            if any(0 <= x + dx < 8 and 0 <= y + dy < 8 and van[(y + dy) * 8 + x + dx] == 0
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                continue                                     # the silhouette stays vanilla's
            px = min(x, 7 - x) if flip[0] else x
            py = min(y, 7 - y) if flip[1] else y
            r = paint(PART[t], row, MAT_OF[row][v], px, py, tone(row, v))
            if r is None:
                continue
            n = ink(row, r[0], r[1])
            if (row, n) in RESERVED or n == 0:
                raise SystemExit("  !! tile %d: direction drew reserved index %d in row %d" % (t, n, row))
            out[y * 8 + x] = n
    return out


def draw(style, use):
    flips = flips_of(BATCH1)
    tiles = [list(p) for p in G.CUR]
    for t in BATCH1:
        row = row_of(t, use)
        tiles[t] = draw_tile(t, row, style["paint"], flips[t])
    return tiles


def row_of(t, use):
    rows = set(use[t]["rows"])
    if len(rows) != 1 or next(iter(rows))[0] != "general":
        raise SystemExit("  !! tile %d is drawn in %s -- not batch 1's (General's own rows only)" % (t, sorted(rows)))
    return next(iter(rows))[1]


# ================================================================== the census
def code_names(blocks):
    """what in the engine names these General blocks: the door table, METATILE_ labels, setmetatile in scripts"""
    labels = {int(v, 16): k for k, v in re.findall(r"#define (METATILE_General_\w+)\s+(0x[0-9A-Fa-f]+)",
                                                   open(os.path.join(GBA, "include/constants/metatile_labels.h")).read())}
    sm = collections.defaultdict(list)
    for f in glob.glob(os.path.join(GBA, "data/maps/*/scripts.inc")) + glob.glob(os.path.join(GBA, "data/scripts/*.inc")):
        for m in re.finditer(r"setmetatile\s+[^,]+,\s*[^,]+,\s*(0x[0-9A-Fa-f]+|\d+|METATILE_\w+)", open(f).read()):
            v = m.group(1)
            b = int(v, 0) if not v.startswith("METATILE_") else None
            if b is None and v.startswith("METATILE_General_"):
                b = next((k for k, n in labels.items() if n == v), None)
            if b is not None and b < 640:
                sm[b].append(os.path.basename(os.path.dirname(f)))
    out = {}
    for b in blocks:
        why = []
        if b in DOOR_BLOCKS:
            why.append("field_door.c")
        if b in labels:
            why.append(labels[b])
        if b in sm:
            why.append("setmetatile in %s" % ", ".join(sorted(set(sm[b]))))
        if why:
            out["0x%X" % b] = why
    return out


def census(use):
    left = [t for t in sorted(use) if G.CUR[t] == G.VAN[t]]
    anim = [t for t in left if t in G.ANIM_TILES]
    flat = [t for t in left if t not in G.ANIM_TILES and len(set(G.CUR[t])) == 1]
    rest = [t for t in left if t not in anim and t not in flat]
    unseen = [t for t in rest if not use[t]["maps"]]
    seen = [t for t in rest if use[t]["maps"]]
    return dict(left=left, anim=anim, flat=flat, unseen=unseen, seen=seen)


def summarise(name, ts, use):
    blocks = sorted({m for t in ts for (s, m) in use[t]["blocks"] if s == "general"})
    sec = sorted({s for t in ts for (s, m) in use[t]["blocks"] if s != "general"})
    maps = sorted({m for t in ts for m in use[t]["maps"]})
    beh = collections.Counter(G.behaviour(b) for b in blocks)
    return dict(object=name, tiles=ts, count=len(ts), blocks=["0x%X" % b for b in blocks],
                secondary_blocks_in=sec, maps=len(maps), map_names=maps,
                draws=sum(use[t]["draws"] for t in ts),
                behaviours={k: v for k, v in beh.items() if k != "NORMAL"}, code=code_names(blocks))


def engine_state(pick_tiles):
    """every batch 1 tile is pret's, or the approved pick's; anything else is another tool's drawing"""
    van, ours, other = [], [], []
    for t in BATCH1:
        if pick_tiles is not None and G.CUR[t] == pick_tiles[t]:
            ours.append(t)                                   # (573 and 574 are all outline and edge: the same either way)
        elif G.CUR[t] == G.VAN[t]:
            van.append(t)
        else:
            other.append(t)
    return van, ours, other


def report(use):
    print("T-542 -- the primary general tileset's last Nintendo drawings (%s)\n" % os.path.relpath(PD, GBA))
    c = census(use)
    print("  census: %d General tiles still pret's drawing on some layout -- %d under the water animation (VRAM shows "
          "the strips), %d flat, %d on layouts no map uses, %d SEEN" %
          (len(c["left"]), len(c["anim"]), len(c["flat"]), len(c["unseen"]), len(c["seen"])))
    print("  ledges, fences, signposts: 0 left (T-438 C re-surfaced them); boulders are object sprites (ours)")
    bad = False
    named = set(BATCH1)
    rows = []
    print("\n  BATCH 1 -- THE ROAD GATES (drawn here)")
    for k, (name, ts) in OBJECTS.items():
        s = summarise(name, ts, use)
        rows.append(dict(s, batch=1))
        print("    %-48s %3d tiles  %2d blocks  %3d maps  %5d draws  %s%s" %
              (name, s["count"], len(s["blocks"]), s["maps"], s["draws"],
               ("behaviour " + ", ".join("%s %d" % kv for kv in s["behaviours"].items()) + "  ") if s["behaviours"] else "",
               ("NAMED: " + "; ".join("%s %s" % (b, w) for b, w in s["code"].items())) if s["code"] else "named by no code"))
    for key, o in B2.items():
        s = summarise(o["title"], o["tiles"], use)
        rows.append(dict(s, batch=2))
        named |= set(o["tiles"])
    for title, (batch, ts) in LATER.items():
        s = summarise(title[2:], ts, use)
        rows.append(dict(s, batch=batch))
        named |= set(ts)
    for batch in (2, 3):
        print("\n  BATCH %d -- %s (%s)" % (batch, "THE TOWN PIECES" if batch == 2 else "THE EDGES AND DOORS",
                                         "built" if batch == 2 else ("built" if APPROVED_B3 else "drafted")))
        for r in rows:
            if r["batch"] == batch:
                print("    %-58s %3d tiles  %2d blocks  %3d maps  %s" %
                      (r["object"], r["count"], len(r["blocks"]), r["maps"],
                       ("NAMED: " + "; ".join("%s %s" % (b, w) for b, w in r["code"].items())) if r["code"] else ""))
    stray = sorted(set(c["seen"]) - named)
    gone = sorted(named - set(c["seen"]))
    if stray:
        print("  !! seen and in no batch: %s" % stray)
        bad = True
    if gone:
        print("  (no longer vanilla or no longer seen, so out of the census: %s)" % gone)
    nb = {r["batch"]: 0 for r in rows}
    for r in rows:
        nb[r["batch"]] += len([t for t in r["tiles"] if t in c["seen"]])
    b1maps = sorted({m for t in BATCH1 for m in use[t]["maps"]})
    print("\n  batches: 1 = %d, 2 = %d, 3 = %d (of %d seen); batch 1 is on %d maps" %
          (nb[1], nb.get(2, 0), nb.get(3, 0), len(c["seen"]), len(b1maps)))

    # batch 1's checks
    print("\n  batch 1's checks")
    for t in BATCH1:
        row_of(t, use)
    print("    every tile drawn in exactly one of General's own rows (%s)" %
          dict(collections.Counter(row_of(t, use) for t in BATCH1)))
    anim = [t for t in BATCH1 if t in G.ANIM_TILES]
    print("    under an animation (416..481, 508..511): %s" % (anim or "none"))
    bad |= bool(anim)
    blocks = sorted({m for t in BATCH1 for (s, m) in use[t]["blocks"] if s == "general"})
    doors = [b for b in blocks if b in DOOR_BLOCKS]
    print("    door blocks (field_door.c): %s" % (doors or "none -- no door animation draws these tiles"))
    bad |= bool(doors)
    names = code_names(blocks)
    print("    labels / setmetatile on its %d blocks: %s" % (len(blocks), names or "none"))
    print("    reserved indices (row 2 idx 8, rows 4/6 idx 1) in today's tiles: %s" %
          ([t for t in BATCH1 if any((row_of(t, use), v) in RESERVED for v in G.CUR[t])] or "none"))
    print("    behaviours of its blocks (unchanged by a redraw): %s" %
          dict(collections.Counter(G.behaviour(b) for b in blocks)))
    pick_tiles = draw(STYLES[next(iter(APPROVED))], use) if len(APPROVED) == 1 else None
    van, ours, other = engine_state(pick_tiles)
    print("    in the engine: %d pret's, %d the approved pick's, %d someone else's%s" %
          (len(van), len(ours), len(other), (" -- %s: find which side is right" % other) if other else ""))
    bad |= bool(other)
    if pick_tiles is not None and van:
        print("  !! %d batch 1 tiles are still pret's with %s approved -- run the write" % (len(van), sorted(APPROVED)))
        bad = True
    print("    gbageneral writes only tiles still pret's, so once batch 1 is in it cannot put one back")
    bad |= report_b2(use)
    bad |= report_b3(use)
    return bad, rows, c


# ================================================================== the sheets
MAP_CROPS = [   # (map, x0, y0, w, h in cells, what it shows, detail box inside the crop for the 3x)
    ("Route6", 0, 0, 24, 14, "ROUTE 6: BRAZEN's south gate, its posts, fences and a ledge", (9, 0, 9, 8)),
    ("Route11", 52, 2, 18, 12, "ROUTE 11: an east-west gate, a boulder, fences", (5, 5, 10, 7)),
    ("Route2", 0, 40, 24, 16, "ROUTE 2: two gates, ledges, the forest edge", (1, 5, 9, 9)),
    ("SaffronCity", 24, 0, 22, 14, "BRAZEN CITY: the north gate from inside, the town's fences, signs and paving", (7, 0, 8, 8)),
    ("Route12", 4, 78, 18, 12, "ROUTE 12: the blue house by the water", (6, 5, 8, 5)),
    ("FourIsland", 4, 16, 18, 12, "FOUR ISLAND: the stone stairs", (3, 4, 8, 6)),
]
HEAD = (250, 214, 120)


def map_sheet(crop, versions, path, head="T-542 batch 1 -- %s   (DRAFT; 1x above, 3x below)"):
    name, x0, y0, w, h, why, det = crop
    F, f2 = G.font(15), G.font(12)
    shots = [(lab, G.render2(name, tl, None, None, (x0, y0, w, h))) for lab, tl in versions]
    dets = [(lab, G.render2(name, tl, None, None, (x0 + det[0], y0 + det[1], det[2], det[3]))) for lab, tl in versions]
    a, d = shots[0][1], dets[0][1]
    gap = 12
    W = max(len(shots) * (a.width + gap), len(dets) * (d.width * 3 + gap), int(F.getlength(head % why))) + 16
    H = 30 + 16 + a.height + 24 + 16 + d.height * 3 + 14
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), head % why, fill=HEAD, font=F)
    for k, (lab, s) in enumerate(shots):
        dr.text((8 + k * (a.width + gap), 30), lab, fill=(220, 220, 230), font=f2)
        im.paste(s, (8 + k * (a.width + gap), 46))
    y = 46 + a.height + 24
    for k, (lab, s) in enumerate(dets):
        dr.text((8 + k * (d.width * 3 + gap), y - 2), lab + "  3x", fill=(220, 220, 230), font=f2)
        im.paste(s.resize((s.width * 3, s.height * 3), Image.NEAREST), (8 + k * (d.width * 3 + gap), y + 14))
    im.save(path)
    return path


def tiles_sheet(versions, use, path, Z=3):
    F, f2 = G.font(15), G.font(11)
    cell = 8 * Z + 4
    per = 20
    lines = []
    for k, (name, ts) in OBJECTS.items():
        for i in range(0, len(ts), per):
            lines.append((name if i == 0 else "", ts[i:i + per]))
    W = 16 + 100 + per * cell + 10
    rowh = len(versions) * (cell + 2) + 22
    im = Image.new("RGB", (max(W, 760), 34 + len(lines) * rowh), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-542 batch 1: the 53 tiles at 3x, today and each direction (DRAFT)", fill=HEAD, font=F)
    y = 34
    for name, ts in lines:
        dr.text((8, y), name, fill=(200, 200, 210), font=f2)
        for vi, (lab, tl) in enumerate(versions):
            yy = y + 16 + vi * (cell + 2)
            dr.text((8, yy + 6), lab[:14], fill=(170, 170, 180), font=f2)
            for k, t in enumerate(ts):
                row = row_of(t, use)
                im.paste(G.tile_rgb(tl[t], G.PALS[row], Z), (116 + k * cell, yy))
        y += rowh
    im.save(path)
    return path


def save_tiles(tiles, path):
    cur = Image.open(os.path.join(PD, "tiles.png"))
    out = cur.copy()
    p = out.load()
    for t in range(len(tiles)):
        if tiles[t] != G.CUR[t]:
            for i, v in enumerate(tiles[t]):
                p[(t % 16) * 8 + i % 8, (t // 16) * 8 + i // 8] = v
    out.save(path, bits=4)
    back = G.tiles_of(Image.open(path))
    if back[:len(tiles)] != [list(x) for x in tiles]:
        raise SystemExit("  !! %s does not read back as drawn" % path)


def check_engine(use):
    """T-446's rule: with one direction approved, General's tiles.png must be exactly what `--write --approved --pick X`
    makes -- every tile, not only batch 1's -- and its palettes untouched by it"""
    pick = next(iter(APPROVED))
    tiles = draw(STYLES[pick], use)
    if len(APPROVED_B2) == 1:                            # batch 2's pick on top, once the user has made it
        b2 = draw_b2(next(iter(APPROVED_B2)), use)
        for t in B2_TILES:
            tiles[t] = b2[t]
    if len(APPROVED_B3) == 1:                            # and batch 3's
        b3 = draw_b3(next(iter(APPROVED_B3)), use)
        for t in B3_TILES:
            tiles[t] = b3[t]
    off = [t for t in range(len(G.CUR)) if list(tiles[t]) != list(G.CUR[t])]
    reserved = [t for t in BATCH1 if any((row_of(t, use), v) in RESERVED for v in tiles[t])]
    if off or reserved:
        print("  !! general: the engine differs from `--write --approved --pick %s` in tiles %s%s -- find which side is "
              "right" % (pick, off[:12], ("; reserved indices drawn in %s" % reserved) if reserved else ""))
        return 1
    print("  the engine matches `--write --approved --pick %s` (batch 1, %d tiles%s%s; no reserved index drawn)"
          % (pick, len(BATCH1), (", and batch 2's --pick %s, %d tiles" % (next(iter(APPROVED_B2)), len(B2_TILES)))
             if len(APPROVED_B2) == 1 else "", (", and batch 3's --pick %s, %d tiles" % (next(iter(APPROVED_B3)),
                                                len(B3_TILES))) if len(APPROVED_B3) == 1 else ""))
    return 0


# ================================================================== batch 2: THE TOWN PIECES
#  General's tiles the towns draw in their OWN rows (and a few of General's rows on a town's map): no tool before this
#  one could reach them -- gbatowns redraws a town's secondary tiles, gbageneral General's tiles in General's rows --
#  so each is drawn here in its town's existing look, by gbatowns' own method and motifs: a tile is drawn where it is
#  drawn MOST (its home map, the object it is part of, in that object's coordinates, so a motif runs on across the
#  secondary tiles beside it), each pixel by its MATERIAL's motif on that material's ramp; a pixel touching another
#  material or nothing keeps vanilla's index (outline, silhouette, sill); an index no material names keeps vanilla's.
#  A tile drawn in several towns' rows is ONE drawing: its ramps keep only indices whose light-to-dark order holds in
#  every row it is drawn in, so it reads as the same drawing in each town's colours.
APPROVED_B2 = {"A"}                  # the user, 2026-11-10: build as drawn; cave mouth A (--write --batch 2 refuses others)
DRAFT_B2 = os.path.join(ROOT, "gfx", "drafts", "t542_b2")
BATCH = argval("--batch")            # --draft: 2 unless given (batch 1 is built); --write: 1 unless given

_argv, sys.argv = sys.argv, ["gbatowns"]
try:
    import gbatowns as T                                     # the towns' motifs (a writing tool: read, never run)
finally:
    sys.argv = _argv


def m_hip(x, y, w, h, X, Y, b):
    """the roof's hip, in the standing seam the roof itself is drawn in (gbageneral's ribbed house roof): a seam every
    four pixels down the slope, a lit edge and a dark groove, on the hip's own shade (it stays the shaded plane)"""
    return min(1.0, b + 0.3) if X % 4 == 3 else (max(0.0, b - 0.25) if X % 4 == 0 else b)


def m_callow_roof(x, y, w, h, X, Y, b):
    """CALLOW's green roof in its calmed standing seam (gbatowns m_ribs_calm: a seam every eight, one step of shade):
    the lit ridge band stays lit, the slope below it stays dark, each with its seam"""
    if b < 0.5:
        return 0.5 if X % 8 == 7 else (0.0 if y < 2 else 0.25)
    return 1.0 if X % 8 == 7 else (0.5 if X % 8 == 0 else 0.75)


def m_verdigris_roof(x, y, w, h, X, Y, b):
    """VERDIGRIS's flat roofs as its bronze (gbatowns m_bronze, kept on the roof's own ramp so LURID's grey roofs, which
    draw these tiles, get no other colour): a standing seam every eight on vanilla's own line, lit on its far side,
    and a run of bloom down beside every other seam from a third of the way down"""
    xo = X % 8
    if xo == 3:
        return 1.0
    if xo == 4:
        return 0.0
    if xo == 2 and y >= h // 3 and T._h(X // 8, 3) < 0.6:
        return 0.8
    return 0.5


def m_post(x, y, w, h, X, Y, b):
    """a turned post: lit on its left, dark on its right, a collar every eight rows"""
    if Y % 8 == 0:
        return 0.0
    return 0.0 if x == 0 else (1.0 if x >= w - 1 else 0.45)


def m_timber(x, y, w, h, X, Y, b):
    """a timber post: a lit arris, the grain in long strokes, a check every six rows"""
    if x == 0:
        return 0.0
    if Y % 6 == 3 and x == 1:
        return 1.0
    return 0.0 if (2 * X + Y // 4) % 5 == 0 else 0.85


def m_coping(x, y, w, h, X, Y, b):
    """ARDOR's quay coping in sun-bleached plaster (its walls' stucco): a bleached top, a flat body, a shade along the
    foot, and a joint every sixteen pixels"""
    if X % 16 == 15:
        return 1.0
    return T.m_stucco(x, y, w, h, X, Y, b)


#  B2: object -> its title, its tiles, and its HOMES in order: (map, {row: {index: material}}, {material: motif},
#  {material: keep}[, thin materials]) -- a tile is drawn at the first home that draws it; the town each home belongs
#  to sets the look. KEEP is how much of vanilla's own light a material keeps (gbatowns' KEEP_LIGHT).
_R = lambda a, b, m: {i: m for i in range(a, b + 1)}


def _M(*ds):
    out = {}
    for d in ds:
        out.update(d)
    return out


B2 = collections.OrderedDict([
    ("hip", dict(title="BRAZEN's roof hips (298/330: gbageneral's drift; DOLDRUM and the blue house draw them too)",
                 town="BRAZEN", tiles=[298, 299, 330, 331],
                 homes=[("SaffronCity", {11: _R(10, 14, "hip")}, {"hip": m_hip}, {"hip": 0.0})],
                 look="the standing seam of the roof they end (gbageneral's ribbed house roof), down the hip")),
    ("kiosk", dict(title="BRAZEN's crossing: the kiosks' domes", town="BRAZEN", tiles=[350, 351],
                   homes=[("SaffronCity_Connection", {2: _R(10, 14, "dome")}, {"dome": T.m_rivet}, {"dome": 0.3})],
                   look="BRAZEN's rolled sheet (m_rivet): a lit roll, a lap, a rivet line")),
    ("blue", dict(title="the blue house's walls, posts and eave (every route's house; CALLOW and DOLDRUM lend rows)",
                  town="the routes", tiles=[344, 347, 360, 362, 363, 376, 377, 379, 552, 568],
                  homes=[("Route2", {3: _M(_R(2, 4, "siding"), _R(8, 9, "post"), _R(10, 14, "hip"))},
                          {"siding": T.m_clapboard, "post": m_timber, "hip": m_hip},
                          {"siding": 0.35, "post": 0.0, "hip": 0.0}, {"post"})],
                  look="the house kit's own: level boards (as CALLOW's, DOLDRUM's and the islands' siding), timber "
                       "corner posts, the ribbed roof's hip")),
    ("verdigris", dict(title="VERDIGRIS's buildings (row 12; LURID's row 12 and ARDOR's row 8 draw the same tiles)",
                       town="VERDIGRIS", tiles=[521, 522, 523, 537, 538, 539, 540, 541, 542, 553, 554, 555, 556, 569,
                                                570, 571, 583, 584, 585, 586, 587, 599, 600, 601, 602, 603, 524, 525,
                                                526],
                       homes=[("CeladonCity", {12: _M(_R(2, 4, "bronze"), _R(10, 13, "bloom")),
                                               3: _R(10, 14, "glass")},
                               {"bronze": m_verdigris_roof, "bloom": T.m_patina, "glass": T.m_glass},
                               {"bronze": 0.0, "bloom": 0.35, "glass": 0.2}),
                              ("FuchsiaCity", {12: _M(_R(2, 4, "bronze"), _R(10, 13, "bloom"))},
                               {"bronze": m_verdigris_roof, "bloom": T.m_patina}, {"bronze": 0.0, "bloom": 0.35})],
                       look="VERDIGRIS's own (gbatowns): bronze sheet with a seam every eight, the walls a green "
                            "patina with the rain's runs, the panes dark below with a glint")),
    ("callow", dict(title="CALLOW's green house (THREE ISLAND's red one draws the same tiles in General's row 2)",
                    town="CALLOW", tiles=[516, 517, 532, 533, 548, 549, 564, 565, 566, 519],
                    homes=[("ViridianCity", {11: _M(_R(10, 14, "roof"), _R(2, 3, "siding"), _R(8, 9, "post"))},
                            {"roof": m_callow_roof, "siding": T.m_clapboard, "post": m_timber},
                            {"roof": 0.0, "siding": 0.35, "post": 0.0}, {"post"}),
                           ("ThreeIsland", {2: _R(10, 14, "roof")}, {"roof": m_callow_roof}, {"roof": 0.0})],
                    look="CALLOW's own roof (gbatowns m_ribs_calm, the user's calmed seam): a lit ridge cap, a seam "
                         "every eight; the walls in level boards")),
    ("doldrum", dict(title="DOLDRUM's long houses' walls (SLATE's and ROUTE 5's houses draw them too), a fence post",
                     town="DOLDRUM", tiles=[580, 581, 582, 341, 520, 527, 543, 596, 598],
                     homes=[("CeruleanCity", {12: _R(2, 4, "siding"), 3: _R(1, 4, "post")},
                             {"siding": T.m_clapboard, "post": m_post}, {"siding": 0.35, "post": 0.3}, {"post"}),
                            ("Route5", {11: _R(2, 4, "siding"), 10: _M(_R(10, 13, "hip"), _R(2, 4, "siding"))},
                             {"siding": T.m_clapboard, "hip": m_hip}, {"siding": 0.35, "hip": 0.0}),
                            ("PewterCity", {3: _R(2, 4, "stone")}, {"stone": T.m_ashlar}, {"stone": 0.35}),
                            ("FuchsiaCity", {3: _R(1, 4, "post")}, {"post": m_post}, {"post": 0.3}, {"post"})],
                     look="DOLDRUM's siding (gbatowns m_clapboard, as gbarestyle's houses); SLATE's corners in its "
                          "dressed stone (m_ashlar); the hip in the roof's seam")),
    ("ardor", dict(title="ARDOR's pier: the quay's coping", town="ARDOR", tiles=[496, 497],
                   homes=[("SSAnne_Exterior", {2: _R(1, 4, "coping")}, {"coping": m_coping}, {"coping": 0.3})],
                   look="ARDOR's walls (gbatowns m_stucco): sun on plaster, a bleached top, a shaded foot")),
    ("seven", dict(title="SEVEN ISLAND's house: its red eave", town="the islands", tiles=[192, 193, 194, 195],
                   homes=[("SevenIsland_TrainerTower", {2: _R(10, 14, "net")}, {"net": T.m_net}, {"net": 0.0})],
                   look="the islands' harbour roofs (gbatowns m_net): red under a lit ridge, a net drying")),
    ("cave", dict(title="the cave mouth (CAVE_DOOR; the islands' row 12 too)", town="every cave", tiles=[302, 303, 318,
                                                                                                    319],
                  homes=[], look="the real choice: three directions")),
    ("cliff", dict(title="a cliff piece (one pixel: nothing to redraw)", town="every cliff", tiles=[101], homes=[],
                   look="one drawn pixel, on the silhouette: it stays pret's")),
])
B2_TILES = sorted(t for o in B2.values() for t in o["tiles"])
B2_OBJ = {t: k for k, o in B2.items() for t in o["tiles"]}
TOWN_OF = {"gTileset_CeladonCity": "VERDIGRIS", "gTileset_FuchsiaCity": "LURID", "gTileset_VermilionCity": "ARDOR",
           "gTileset_SaffronCity": "BRAZEN", "gTileset_CeruleanCity": "DOLDRUM", "gTileset_ViridianCity": "CALLOW",
           "gTileset_LavenderTown": "HALFTONE", "gTileset_SeviiIslands123": "ONE..THREE ISLAND", "general": "General"}

#  the cave mouth, three ways: only its rock (row 1's 11..14; the islands' row 12 keeps the same order) is drawn; the
#  opening (5) and the grey sill (4, 8) stay as they are, so the mouth is the same hole in the same place
CAVE_ROCK = [11, 12, 13, 14]


def _lip(px, x, y):
    """how far this pixel is from the opening, along its row (1 = the jamb's face)"""
    d = [abs(x - u) for u in range(8) if px[y * 8 + u] == 5]
    return min(d) if d else 9


def paint_cave(pick, t):
    van = G.VAN[t]
    out = list(van)
    for y in range(8):
        for x in range(8):
            if van[y * 8 + x] not in CAVE_ROCK:
                continue
            d = _lip(van, x, y)
            if pick == "A":          # THE ROCK'S OWN MOUTH: pass 3's chunky stones carried to the lip
                yy = (y + (3 if (x // 3) % 2 else 0)) % 6
                v = 14 if yy == 5 else (13 if d == 1 else (11 if yy == 0 else 12))
            elif pick == "B":        # THE ADIT: a timber post each side of the hole, its lit arris and grain
                v = 14 if d == 1 else (11 if d == 2 else (13 if y % 5 == 2 else 12))
            else:                    # THE PORTAL: dressed jamb stones in courses of four, a shaded reveal
                yy = y % 4
                v = 14 if yy == 3 else (13 if d == 1 else (11 if yy == 0 else (14 if d == 4 and (y // 4) % 2 else 12)))
            out[y * 8 + x] = v
    return out


B2_STYLES = collections.OrderedDict([
    ("A", dict(title="THE ROCK'S OWN MOUTH",
               blurb="every town piece in its town's existing look (the same in B and C); the cave mouth's jambs as "
                     "pass 3's own chunky stones, carried to the lip")),
    ("B", dict(title="THE ADIT", blurb="the town pieces as A; the cave mouth timbered -- a post each side of the hole")),
    ("C", dict(title="THE PORTAL", blurb="the town pieces as A; the cave mouth's jambs dressed stone in courses")),
])


def pal_of(key):
    ts, r = key
    return G.PALS[r] if ts == "general" else G.secondary(ts)["pals"][r]


def b2_ladder(t, homekey, mrow, mat, use):
    """MAT's indices in the home row, light to dark, keeping only those whose order holds in every row t is drawn in
    (an index the tile already draws is never dropped)"""
    pal = pal_of(homekey)
    ix = sorted([i for i, m in mrow.items() if m == mat], key=lambda i: -lum(pal[i]))
    ix = [i for i in ix if (homekey[1], i) not in RESERVED]
    own = set(G.VAN[t])
    rows = [k for k in use[t]["rows"] if k != homekey]

    def ok(seq):
        return all(all(lum(pal_of(k)[a]) >= lum(pal_of(k)[b]) - 1 for a, b in zip(seq, seq[1:])) for k in rows)
    while not ok(ix):
        drop = [i for i in ix if i not in own]
        bad = next((i for i in reversed(drop) if ok([j for j in ix if j != i])), drop[-1] if drop else None)
        if bad is None:
            break
        ix.remove(bad)
    return ix


def _clusters(mapname, tiles):
    l = G.layout_named(mapname)
    sec = G.secondary(l["secondary_tileset"])
    W, H = l["width"], l["height"]
    d = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    cs = set()
    for y in range(H):
        for x in range(W):
            m = struct.unpack_from("<H", d, (y * W + x) * 2)[0] & 0x3FF
            buf, k = (G.GMT, m) if m < 640 else (sec["mt"], m - 640)
            if (k + 1) * 16 <= len(buf) and any((e & 0x3FF) in tiles for e in G.entries(buf, k)):
                cs.add((x, y))
    out = []
    while cs:
        st, grp = [cs.pop()], []
        while st:
            a = st.pop()
            grp.append(a)
            for dx in (-2, -1, 0, 1, 2):
                for dy in (-2, -1, 0, 1, 2):
                    b = (a[0] + dx, a[1] + dy)
                    if b in cs:
                        cs.remove(b)
                        st.append(b)
        xs, ys = [a for a, _ in grp], [b for _, b in grp]
        x0, y0 = max(0, min(xs) - 1), max(0, min(ys) - 1)
        out.append((x0, y0, min(W, max(xs) + 2) - x0, min(H, max(ys) + 2) - y0, len(grp)))
    return sorted(out, key=lambda c: -c[4]), l, sec, W, d


_SECT = {}


def _sec_tiles(sec):
    if sec["name"] not in _SECT:
        _SECT[sec["name"]] = G.tiles_of(sec["tiles"])
    return _SECT[sec["name"]]


def draw_b2(pick, use, how=None):
    """General's tiles with batch 2 drawn in direction PICK: the town pieces by their towns' looks at their homes
    (the same in every direction), the cave mouth by the direction"""
    tiles = [list(p) for p in G.CUR]
    for t in B2_TILES:
        tiles[t] = list(G.VAN[t])
    done = set()
    for key, o in B2.items():
        if key == "cave":
            for t in o["tiles"]:
                tiles[t] = paint_cave(pick, t)
                done.add(t)
            continue
        for home in o["homes"]:
            mapname, mats, style, keep = home[:4]
            thin = home[4] if len(home) > 4 else set()
            todo = {t for t in o["tiles"] if t not in done}
            if not todo:
                break
            boxes, l, sec, W, d = _clusters(mapname, todo)
            secsym = l["secondary_tileset"]
            stiles = _sec_tiles(sec)
            claimed = {}
            for x0, y0, w, h, _ in boxes:
                for layer in (0, 1):
                    PW, PH = w * 16, h * 16
                    px = [[None] * PW for _ in range(PH)]
                    for cy in range(h):
                        for cx in range(w):
                            m = struct.unpack_from("<H", d, ((y0 + cy) * W + x0 + cx) * 2)[0] & 0x3FF
                            buf, k = (G.GMT, m) if m < 640 else (sec["mt"], m - 640)
                            if (k + 1) * 16 > len(buf):
                                continue
                            for q in range(4):
                                v = G.entries(buf, k)[layer * 4 + q]
                                t, row = v & 0x3FF, v >> 12
                                if t < 640:
                                    src = G.VAN[t] if t in B2_OBJ else G.CUR[t]
                                else:
                                    src = stiles[t - 640] if t - 640 < len(stiles) else [0] * 64
                                for ty in range(8):
                                    for tx in range(8):
                                        sx = 7 - tx if v & 0x400 else tx
                                        sy = 7 - ty if v & 0x800 else ty
                                        c = src[sy * 8 + sx]
                                        if c:
                                            px[cy * 16 + (q // 2) * 8 + ty][cx * 16 + (q % 2) * 8 + tx] = \
                                                (row, c, t if t < 640 else None, sy * 8 + sx)
                    mat = lambda p: mats.get(p[0], {}).get(p[1]) if p else None
                    region = {}
                    for Y in range(PH):
                        for X in range(PW):
                            m0 = mat(px[Y][X])
                            if m0 is None or (X, Y) in region:
                                continue
                            st, grp = [(X, Y)], []
                            region[(X, Y)] = None
                            while st:
                                a, c = st.pop()
                                grp.append((a, c))
                                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                                    u, vv = a + dx, c + dy
                                    if 0 <= u < PW and 0 <= vv < PH and (u, vv) not in region and \
                                            mat(px[vv][u]) == m0:
                                        region[(u, vv)] = None
                                        st.append((u, vv))
                            xs, ys = [a for a, _ in grp], [c for _, c in grp]
                            box = (min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)
                            for g in grp:
                                region[g] = box
                    for Y in range(PH):
                        for X in range(PW):
                            p = px[Y][X]
                            if not p or p[2] not in todo:
                                continue
                            row, idx, t, k = p
                            m0 = mat(p)
                            if m0 is None:
                                continue
                            if any(not (0 <= X + dx < PW and 0 <= Y + dy < PH) or not px[Y + dy][X + dx] or
                                   (mat(px[Y + dy][X + dx]) != m0 and
                                    (m0 not in thin or mat(px[Y + dy][X + dx]) is not None))
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                                continue                      # an outline, a sill, a join: vanilla's (a THIN
                                #                               material -- a post two pixels wide -- is drawn up to
                                #                               its outline, never past it)
                            homekey = ("general", row) if row < 7 else (secsym, row)
                            lad = b2_ladder(t, homekey, mats[row], m0, use)
                            if len(lad) < 2 or idx not in lad:
                                continue
                            base = lad.index(idx) / (len(lad) - 1)
                            rx, ry, rw, rh = region[(X, Y)]
                            lv = style[m0](X - rx, Y - ry, rw, rh, X + x0 * 16, Y + y0 * 16, base)
                            if isinstance(lv, tuple):
                                lv = lv[0]                    # never onto another material's ramp
                            kp = keep.get(m0, 0.35)
                            lv = max(0.0, min(1.0, (1 - kp) * lv + kp * base))
                            claimed.setdefault(t, {})[k] = lad[int(round(lv * (len(lad) - 1)))]
            for t, pix in claimed.items():
                for k, v in pix.items():
                    tiles[t][k] = v
                done.add(t)
                if how is not None:
                    how[t] = mapname
    for t in B2_TILES:
        if any((a == 0) != (b == 0) for a, b in zip(G.VAN[t], tiles[t])):
            raise SystemExit("  !! batch 2: tile %d's footprint moved" % t)
        for k in use[t]["rows"]:
            r = k[1]
            if r < 7 and any((r, v) in RESERVED for v in tiles[t] if v not in G.VAN[t]):
                raise SystemExit("  !! batch 2: tile %d draws a reserved index in row %d" % (t, r))
    return tiles


def b2_state(pick_tiles):
    van, ours, other = [], [], []
    for t in B2_TILES:
        if pick_tiles is not None and G.CUR[t] == pick_tiles[t]:
            ours.append(t)
        elif G.CUR[t] == G.VAN[t]:
            van.append(t)
        else:
            other.append(t)
    return van, ours, other


def report_b2(use):
    """batch 2's census by town and object, and its checks"""
    bad = False
    print("\n  BATCH 2 -- THE TOWN PIECES (drafted: gfx/drafts/t542_b2/; APPROVED_B2 %s)" % (sorted(APPROVED_B2) or
                                                                                          "empty"))
    for key, o in B2.items():
        ts = o["tiles"]
        towns = collections.Counter()
        for t in ts:
            for (sym, r), n in use[t]["rows"].items():
                towns["%s r%d" % (TOWN_OF.get(sym, sym), r)] += n
        maps = sorted({m for t in ts for m in use[t]["maps"]})
        print("    %-10s %-14s %3d tiles  %3d maps  %5d draws  rows: %s" %
              (key, o["town"], len(ts), len(maps), sum(use[t]["draws"] for t in ts),
               ", ".join("%s %d" % kv for kv in towns.most_common())))
    fl = [t for t, f in flips_of(B2_TILES).items() if any(f)]
    print("    drawn flipped by some block: %s" % (fl or "none (no mirror needed)"))
    anim = [t for t in B2_TILES if t in G.ANIM_TILES]
    blocks = sorted({m for t in B2_TILES for (s, m) in use[t]["blocks"] if s == "general"})
    doors = [b for b in blocks if b in DOOR_BLOCKS]
    print("    under an animation: %s; door blocks: %s; named by code: %s" %
          (anim or "none", doors or "none", code_names(blocks) or "none"))
    bad |= bool(anim) or bool(doors) or bool(fl)
    claim = set(getattr(G, "LATER_T542", set()))
    ours = set(B2_TILES) | set(B3_TILES)                 # batch 3's are claimed too (report_b3 says so)
    if claim != ours:
        print("  !! gbageneral.LATER_T542 is not batches 2 and 3's tiles: only there %s, only here %s -- its write "
              "would draw over them" % (sorted(claim - ours), sorted(ours - claim)))
        bad = True
    else:
        print("    gbageneral.LATER_T542 claims the same %d tiles, and batch 3's (its pass 3 no longer draws 298 and 330)"
              % len(B2_TILES))
    pick_tiles = draw_b2(next(iter(APPROVED_B2)), use) if len(APPROVED_B2) == 1 else None
    van, ours, other = b2_state(pick_tiles)
    print("    in the engine: %d pret's, %d the approved pick's, %d someone else's%s" %
          (len(van), len(ours), len(other), (" -- %s: find which side is right" % other) if other else ""))
    bad |= bool(other)
    if len(APPROVED_B2) > 1:
        print("  !! APPROVED_B2 holds more than one direction: %s" % sorted(APPROVED_B2))
        bad = True
    return bad


B2_CROPS = [   # (map, x0, y0, w, h in cells, what it shows, detail box inside the crop), first met first
    ("ViridianCity", 20, 5, 13, 8, "CALLOW CITY: the green house", (2, 1, 9, 6)),
    ("Route2", 11, 17, 12, 7, "ROUTE 2: the blue house (every route's house)", (2, 1, 7, 5)),
    ("PewterCity", 29, 8, 11, 6, "SLATE CITY: a house's wall corners (General's row 3)", (2, 1, 7, 4)),
    ("CeruleanCity", 6, 8, 40, 7, "DOLDRUM CITY: the long houses' walls, a fence post", (0, 0, 11, 6)),
    ("Route5", 18, 19, 10, 8, "ROUTE 5: the house in DOLDRUM's rows", (1, 1, 8, 6)),
    ("VermilionCity", 4, 3, 28, 6, "ARDOR CITY: walls in ARDOR's row 8 (VERDIGRIS's tiles)", (2, 0, 9, 5)),
    ("SSAnne_Exterior", 44, 0, 28, 6, "ARDOR's pier: the quay's coping", (0, 1, 12, 3)),
    ("CeladonCity", 2, 2, 46, 12, "VERDIGRIS CITY: the north row", (16, 1, 10, 10)),
    ("CeladonCity", 14, 23, 40, 12, "VERDIGRIS CITY: the south row", (1, 0, 11, 10)),
    ("SaffronCity", 16, 8, 12, 8, "BRAZEN CITY: the houses' roof hips (298/330: gbageneral's drift)", (1, 1, 9, 5)),
    ("SaffronCity_Connection", 28, 3, 16, 6, "BRAZEN's crossing: the kiosks' domes", (3, 2, 6, 3)),
    ("FuchsiaCity", 11, 26, 33, 7, "LURID CITY: VERDIGRIS's tiles in LURID's row 12", (1, 0, 11, 6)),
    ("ThreeIsland", 0, 25, 10, 8, "THREE ISLAND: CALLOW's roof tiles in General's red row", (0, 1, 8, 6)),
    ("SevenIsland_TrainerTower", 54, 35, 14, 5, "SEVEN ISLAND: the house's red eave", (4, 2, 8, 3)),
]
CAVE_CROPS = [
    ("Route4", 14, 1, 12, 8, "ROUTE 4: the cave mouth (General's row 1, every cave on the mainland)", (4, 2, 4, 4)),
    ("FourIsland", 33, 8, 10, 7, "FOUR ISLAND: the cave mouth (the islands' row 12)", (3, 2, 4, 4)),
]


def b2_tiles_sheet(versions, use, path, Z=3):
    F, f2 = G.font(15), G.font(11)
    cell = 8 * Z + 4
    per = 15
    lines = []
    for key, o in B2.items():
        ts = o["tiles"]
        for i in range(0, len(ts), per):
            lines.append(((o["town"] + ": " + key) if i == 0 else "", ts[i:i + per]))
    W = 120 + per * (cell * 2 + 6) + 10
    rowh = len(versions) * (cell + 2) + 22
    im = Image.new("RGB", (W, 34 + len(lines) * rowh), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-542 batch 2: the 75 tiles at 3x, in their two most-drawn rows, today and each direction (DRAFT)",
            fill=HEAD, font=F)
    y = 34
    for name, ts in lines:
        dr.text((8, y), name, fill=(200, 200, 210), font=f2)
        for vi, (lab, tl) in enumerate(versions):
            yy = y + 16 + vi * (cell + 2)
            dr.text((8, yy + 6), lab[:16], fill=(170, 170, 180), font=f2)
            for k, t in enumerate(ts):
                for j, (key, _) in enumerate(use[t]["rows"].most_common(2)):
                    im.paste(G.tile_rgb(tl[t], pal_of(key), Z), (120 + k * (cell * 2 + 6) + j * cell, yy))
        y += rowh
    im.save(path)
    return path


def draft_b2(use):
    os.makedirs(DRAFT_B2, exist_ok=True)
    summary, drawn = {}, {}
    print("\n  batch 2, directions (75 tiles; 0 new tiles, 0 palette changes, 0 blocks moved)")
    for k, D in B2_STYLES.items():
        how = {}
        tiles = draw_b2(k, use, how)
        drawn[k] = tiles
        dd = os.path.join(DRAFT_B2, k)
        os.makedirs(dd, exist_ok=True)
        save_tiles(tiles, os.path.join(dd, "tiles.png"))
        ch = [t for t in B2_TILES if tiles[t] != G.VAN[t]]
        summary[k] = dict(title=D["title"], what=D["blurb"], tiles_redrawn=len(ch), unchanged=sorted(set(B2_TILES) -
                          set(ch)), new_tiles=0, palettes_changed=0, homes={str(t): m for t, m in sorted(how.items())})
        print("    %s %-22s %d of %d tiles redrawn (unchanged: %s)" % (k, D["title"], len(ch), len(B2_TILES),
                                                                      sorted(set(B2_TILES) - set(ch))))
    same = [t for t in B2_TILES if B2_OBJ[t] != "cave" and not (drawn["A"][t] == drawn["B"][t] == drawn["C"][t])]
    if same:
        raise SystemExit("  !! batch 2: a town piece differs between directions: %s" % same)
    json.dump(dict(ticket="T-542", batch=2, status="DRAFT -- not in the engine", approved=sorted(APPROVED_B2),
                   directions=summary,
                   objects={k: dict(title=o["title"], town=o["town"], tiles=o["tiles"], look=o["look"],
                                    homes=[h[0] for h in o["homes"]]) for k, o in B2.items()}),
              open(os.path.join(DRAFT_B2, "directions.json"), "w"), indent=1)
    head = "T-542 batch 2 -- %s   (DRAFT; 1x above, 3x below)"
    town = [("TODAY", G.CUR), ("DRAFT (A = B = C)", drawn["A"])]
    allv = [("TODAY", G.CUR)] + [("%s %s" % (k, D["title"]), drawn[k]) for k, D in B2_STYLES.items()]
    out = []
    for i, crop in enumerate(B2_CROPS):
        out.append(map_sheet(crop, town, os.path.join(DRAFT_B2, "t542b2_maps_%02d.png" % (i + 1)), head))
    for i, crop in enumerate(CAVE_CROPS):
        out.append(map_sheet(crop, allv, os.path.join(DRAFT_B2, "t542b2_cave_%d.png" % (i + 1)), head))
    out.append(b2_tiles_sheet(allv, use, os.path.join(DRAFT_B2, "t542b2_tiles.png")))
    for p in out:
        print("  sheet:", p)


# ================================================================== batch 3: THE EDGES AND DOORS
#  The last 24: ground strays, the sea's edge, FOUR ISLAND's puddles and the two sliding doors. Every piece but the
#  doors is DICTATED by what already surrounds it, so it is drawn once, the same in every direction: the thin tree in
#  the crown every other tree has (gbageneral's m_bush, gbatrees' crown in little), the islet's corners in the lip
#  pass 3 gave the rim between them, the sea rock in the chunky stones its twin in the water strip already has
#  (tiles 420..423, gbageneral pass 3), the quay's edge as one more course of the paving's own bond, the puddles'
#  banks in the language of their one corner already ours (310: a lit lip on the grass side, a dark bank, a wet foot).
#  The sliding doors are the one real choice: they are glass on every CENTRE and REPO in the game, and nothing round
#  them says what the glass should be. A tile some block draws mirrored is drawn so it meets itself (the doors' two
#  halves, the thin tree's two sides, the puddles' banks), and nothing touches the reserved indices (row 2 index 8,
#  rows 4 and 6 index 1): batch 3 draws in rows 0, 1, 2, 3 and 5 (and PALLET's row 10 for the sea rock), never 4 or 6.
#  The water itself is gbawater's and is never drawn here: the sea rock and the quay's foot sit ON its strips (a top
#  layer over 416..419), so their drawing stops at their own silhouette and the animation runs on round them.
APPROVED_B3 = set()                  # the user's pick goes here ("A", "B" or "C"); --write --batch 3 refuses until then
DRAFT_B3 = os.path.join(ROOT, "gfx", "drafts", "t542_b3")

B3_STYLES = collections.OrderedDict([
    ("A", dict(title="THE CLEAR PANE",
               blurb="the doors as plain good glass: a sky-lit top fading down the pane, two upright glints, a steel "
                     "push bar at the waist and a steel kick plate; every edge, rock, tree and bank as dictated")),
    ("B", dict(title="THE READOUT",
               blurb="the doors as dark screens (the world as the running machine it is): night-blue glass with three "
                     "lit scan lines and a cursor block, a lit status line at the foot")),
    ("C", dict(title="THE MANIFESTATION",
               blurb="the doors as glass with the frosted safety band real glass doors carry at eye height (a white "
                     "band of dots, so no one walks into it), a steel kick plate below")),
])


def _touch(px, x, y, pred):
    return any(0 <= x + dx < 8 and 0 <= y + dy < 8 and pred(px[(y + dy) * 8 + x + dx])
               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


# ---------------------------------------------------------------- the thin tree (FOUR ISLAND's garden, SAFFRON's)
#  A column of crown two tiles wide, drawn left half and mirrored right half: the tip (11, a top layer over the tall
#  grass in 0x0A), the body (27 over 43, again and again in 0x1B and 0x12) and the foot over its trunk (59 in 0x23).
#  Lobes in the 16-wide column's own coordinates, symmetric about x = 8 and repeating every eight rows, so the halves
#  meet and the body runs on whatever its height.
TREE_TILES = {11: 8, 27: 0, 43: 8, 59: 0}            # tile -> its row offset in the block it is drawn in


def _tree_lobes(oy):
    out = []
    for k in range(-2, 3):
        y = oy - (oy % 8) + 8 * k
        out += [(8.0, y + 3.0, 4.6), (3.6, y + 7.5, 3.8), (12.4, y + 7.5, 3.8)]
    return out


def paint_tree(t):
    px = list(G.VAN[t])
    oy = TREE_TILES[t]
    lobes = _tree_lobes(oy)
    if t == 11:                                          # the tip: one lobe closing the column
        lobes = [(8.0, 12.5, 3.6), (5.5, 15.5, 3.4), (10.5, 15.5, 3.4)]
    if t == 59:                                          # the foot: the body's lobes, nothing below the trunk's top
        lobes = [l for l in _tree_lobes(0) if l[1] <= 3.5]
    #  the block context gbageneral's crown reads for its outline: the left half and its mirror, as the block draws them
    block = []
    for y in range(8):
        for x in range(8):
            v = px[y * 8 + x]
            block.append((x, oy + y, v))
            block.append((15 - x, oy + y, v))
    return G.crown(px, G.LEAF, block, 0, oy, lobes, G.LEAF_INK)


# ---------------------------------------------------------------- the islet's corners (ROUTE 12, the islands)
#  0x132 and 0x134 end the rock rim of a grassy islet each side of 239, which pass 3 drew as a crenellated lip (D C D C
#  over C). Its corners carry the lip on, in phase (239's x = 0 is D), and keep where it turns down the side.
def paint_lip(t):
    px = list(G.VAN[t])
    if t == 79:                                          # left of 239: x 1..7 on, x 0 the corner turning down
        for x in range(1, 8):
            px[x] = 12 if x % 2 else 13
            if x >= 2:
                px[8 + x] = 12
    elif t == 94:                                        # right of 239: x 0..5 on, x 6..7 the corner into shade
        for x in range(0, 6):
            px[x] = 13 if x % 2 == 0 else 12
            px[8 + x] = 12
    return px


# ---------------------------------------------------------------- the sea rock (ROUTE 20 and every sea route; BREATHVERSE)
#  The other sea rock (tiles 420..423, in the water strip) is pass 3's chunky stones: pale lumps, a lit top to each, a
#  shaded foot, dark cracks between. This one -- 173 174 / 189 190, a top layer across four OCEAN_WATER blocks, in
#  General's row 2 and PALLET's row 10 -- is drawn the same: its silhouette and its foam rim are kept (every pixel
#  touching the water), and inside it four lumps, each lit where vanilla's light falls (top left) and darker toward
#  the right and the foot. Row 2's grey ramp 1..7 and row 10's are both light to dark, so it reads the same in both.
ROCK_GRID = [[173, 174], [189, 190]]
ROCK_SEEDS = [(5.0, 6.0, 1.0), (10.5, 4.5, 1.0), (11.0, 10.0, 1.0), (5.5, 11.5, 1.0), (8.0, 14.5, 1.4)]
ROCK_ROLES = {0: {"lit": 2, "body": 2, "foot": 3, "crack": 5},       # vanilla's light here: lit, mid, dark (the
              1: {"lit": 2, "body": 3, "foot": 4, "crack": 6},       # twin's lumps are pale: its 8 is row 2's 2)
              2: {"lit": 3, "body": 4, "foot": 5, "crack": 6}}


def paint_rock():
    comp = [[0] * 16 for _ in range(16)]
    for r in range(2):
        for c in range(2):
            v = G.VAN[ROCK_GRID[r][c]]
            for y in range(8):
                for x in range(8):
                    comp[r * 8 + y][c * 8 + x] = v[y * 8 + x]
    at = lambda x, y: comp[y][x] if 0 <= x < 16 and 0 <= y < 16 else 0
    out = [row[:] for row in comp]
    for y in range(16):
        for x in range(16):
            v = comp[y][x]
            if v == 0 or any(at(x + dx, y + dy) == 0 for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                continue                                 # the silhouette and the foam rim stay
            nb = [at(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if at(x + dx, y + dy)]
            light = sum(nb) / len(nb)                    # vanilla's light, its texture averaged away
            band = 0 if light < 3.9 else (1 if light < 5.2 else 2)
            ds = sorted((((x + 0.5 - sx) ** 2 + (y + 0.5 - sy) ** 2 * 1.4) ** 0.5 / w, sx, sy)
                        for sx, sy, w in ROCK_SEEDS)
            d1, d2 = ds[0][0], ds[1][0]
            if d2 - d1 < 0.8:
                role = "crack"
            else:
                dy = y + 0.5 - ds[0][2]
                role = "lit" if dy < -1.2 else ("foot" if dy > 1.6 else "body")
            out[y][x] = ROCK_ROLES[band][role]
    tiles = {}
    for r in range(2):
        for c in range(2):
            tiles[ROCK_GRID[r][c]] = [out[r * 8 + y][c * 8 + x] for y in range(8) for x in range(8)]
    return tiles


# ---------------------------------------------------------------- the quay's edge (ARDOR, the S.S. ANNE's pier, THREE ISLAND)
#  617 (and 618, its end) is the quay's lip over the water: the paving's running bond (615/616/631/632, three rows to
#  a course, joints at 3 and 7 then 1 and 5, mortar in 9) stops in two flat rows of 9. Those two rows become one more
#  course, the coping, lit along its arris, its joints in the bond's phase (the course under a mortar row jointed at 3
#  and 7). The dark line under it stays, and the lap below (rows 3 and 4, over gbawater's strip) is drawn as small
#  regular ripples against the stone, mirror-safe (618 is drawn flipped once). 618's last column, the corner, stays.
def paint_quay(t):
    px = list(G.VAN[t])
    for x in range(8):
        if t == 618 and x == 7:
            continue
        px[x] = 9 if x in (3, 7) else 8
        px[8 + x] = 9 if x in (3, 7) else 7
        px[24 + x] = 5 if x in (1, 2, 5, 6) else 3
        px[32 + x] = 5 if x in (0, 3, 4, 7) else 3
    return px


# ---------------------------------------------------------------- FOUR ISLAND's puddles
#  The banks are a line one or two pixels wide between the grass (15) and the water under them (transparent). The one
#  bank tile already ours (310) reads grass -> a lit lip (12) -> a dark bank (14) -> a wet foot (13) -> water; the five
#  left are drawn in that language: where the bank is two pixels or more, lip on the grass side and foot on the water
#  side; where it is one pixel, a bank of small stones, two dark and two wet, symmetric in the tile so a bank and its
#  mirror (every puddle tile is drawn flipped somewhere) meet in step.
BANK = [14, 13, 13, 14, 14, 13, 13, 14]


def paint_puddle(t):
    van = G.VAN[t]
    px = list(van)
    rim = lambda v: v in (12, 13, 14)
    for y in range(8):
        for x in range(8):
            v = van[y * 8 + x]
            if not rim(v):
                continue
            wet = _touch(van, x, y, lambda u: u == 0)
            grass = _touch(van, x, y, lambda u: u == 15)
            hr = sum(1 for u in range(max(0, x - 1), min(8, x + 2)) if rim(van[y * 8 + u])) >= 3 or \
                (x in (0, 7) and sum(1 for u in range(8) if rim(van[y * 8 + u])) >= 6)
            vr = sum(1 for u in range(max(0, y - 1), min(8, y + 2)) if rim(van[u * 8 + x])) >= 3 or \
                (y in (0, 7) and sum(1 for u in range(8) if rim(van[u * 8 + x])) >= 6)
            if grass and not wet:
                px[y * 8 + x] = 12                       # the lit lip
            elif wet and not grass and (hr or vr):
                px[y * 8 + x] = BANK[x] if hr else BANK[y]
            elif wet and not grass:
                px[y * 8 + x] = 13                       # the wet foot, at a turn
            else:
                px[y * 8 + x] = 14                       # the dark bank
    return px


# ---------------------------------------------------------------- the sliding doors (every CENTRE and REPO)
#  0x62 the single door (292 over 293, the right half the left mirrored: one leaf of glass across the doorway) and
#  0x15B the double (269 over 285, mirrored: two leaves with their own frames and a mullion between). In row 3: the
#  navy frame (7) and the threshold stay every pixel; the glass (10..14) and the kick band under it are the door's,
#  in DOOR coordinates -- x 0 the outer frame .. 7 the middle, y 0 the top frame .. 15 the threshold. gbadoors draws
#  their three opening frames FROM this closed block (the leaves slide, their highlights with them), so it re-runs
#  after the write.
DOORS3 = {"single": (292, 293), "double": (269, 285)}


def paint_door(pick, kind):
    top, bot = DOORS3[kind]
    comp = list(G.VAN[top]) + list(G.VAN[bot])           # 8 wide, 16 tall
    out = list(comp)
    glass = lambda v: v in (10, 11, 12, 13, 14)
    for y in range(16):
        for x in range(8):
            v = comp[y * 8 + x]
            if not glass(v):
                continue
            k = x if kind == "single" else min(x, 7 - x)   # 1 = beside the frame .. 7 the middle (single)
            if pick == "A":
                if y >= 11:
                    n = 3 if y == 11 else 4                       # the steel kick plate, lit along its top
                elif y == 8 and k >= 2:
                    n = 2                                         # the push bar
                elif y == 9 and k >= 2:
                    n = 5                                         # its shadow on the glass
                elif k == 2 and 2 <= y <= 5 or k == 3 and y == 2:
                    n = 10                                        # the glints, upright
                else:
                    n = 11 if y <= 2 else (12 if y <= 6 else 13)  # the sky in the top, deepening down the pane
            elif pick == "B":
                if y == 12:
                    n = 11                                        # the status line at the foot
                elif y in (3, 5, 7) and (k + y) % 4 != 0 and not (y == 7 and k >= 5):
                    n = 12                                        # three scan lines, broken
                elif y in (9, 10) and kind == "single" and k in (2, 3):
                    n = 10                                        # the cursor block
                elif y in (9, 10) and kind == "double" and k == 2:
                    n = 10
                else:
                    n = 14                                        # night-blue glass
            else:
                if y >= 11:
                    n = 3 if y == 11 else 4                       # the steel kick plate
                elif y in (6, 7):
                    n = 1 if (k + y) % 2 == 0 else 2              # the frosted band: a field of white dots
                elif y == 5 or y == 8:
                    n = 11                                        # the band's soft edge in the glass
                else:
                    n = 11 if y <= 2 else (12 if y <= 4 else 13)
            out[y * 8 + x] = n
    return out[:64], out[64:]


B3 = collections.OrderedDict([
    ("tree", dict(title="the thin tree's crown (FOUR ISLAND's garden, BRAZEN)", tiles=[11, 27, 43, 59],
                  look="dictated: every tree's crown (gbageneral m_bush, gbatrees' crown in little) -- lobes lit across "
                       "their tops, dark at their feet, a deep edge; symmetric, so its two halves meet")),
    ("lip", dict(title="the islet's rim corners (ROUTE 12, the islands)", tiles=[79, 94],
                 look="dictated: pass 3's crenellated lip on 239 between them, carried on in phase to where the rim "
                      "turns down")),
    ("ground", dict(title="the sand's corner, the forest path's edge, a cliff sliver", tiles=[4, 301, 503],
                    look="dictated, and already met: each is all edge -- the halo band and the sand's lip (4), the "
                         "path's scalloped edge its sides share (301), a cliff's grey rim and rock line beside a "
                         "bridge (503, 6 draws) -- so ours is vanilla's; redrawing them is redrawing every path edge")),
    ("rock", dict(title="the sea rock (every sea route; BREATHVERSE in PALLET's row 10)", tiles=[173, 174, 189, 190],
                  look="dictated: the chunky stones of its twin already in the water strip (420..423) -- four lumps, "
                       "lit tops, shaded feet, dark cracks; the silhouette and its foam rim kept")),
    ("quay", dict(title="the quay's edge (ARDOR, the S.S. ANNE's pier, THREE ISLAND)", tiles=[617, 618],
                  look="dictated: one more course of the paving's running bond, the coping, lit along its arris; the "
                       "lap below it in small even ripples against the stone, over gbawater's strip")),
    ("puddle", dict(title="FOUR ISLAND's puddles: their banks", tiles=[311, 326, 342, 358, 359],
                    look="dictated: the bank already ours at 310 -- a lit lip on the grass, a dark bank, a wet foot; "
                         "one-pixel banks in small stones, symmetric so a bank meets its mirror")),
    ("doors", dict(title="the sliding doors 0x62 (single) and 0x15B (double)", tiles=[292, 293, 269, 285],
                   look="the real choice: the glass (A THE CLEAR PANE, B THE READOUT, C THE MANIFESTATION); the frame "
                        "and threshold stay; gbadoors re-runs after the write")),
])
B3_TILES = sorted(t for o in B3.values() for t in o["tiles"])
B3_UNCHANGED = {4, 301, 503}


def draw_b3(pick, use=None):
    """General's tiles with batch 3 drawn: everything dictated (the same in every direction), the doors by PICK"""
    tiles = [list(p) for p in G.CUR]
    for t in TREE_TILES:
        tiles[t] = paint_tree(t)
    for t in (79, 94):
        tiles[t] = paint_lip(t)
    for t, px in paint_rock().items():
        tiles[t] = px
    for t in (617, 618):
        tiles[t] = paint_quay(t)
    for t in (311, 326, 342, 358, 359):
        tiles[t] = paint_puddle(t)
    for kind, (top, bot) in DOORS3.items():
        tiles[top], tiles[bot] = paint_door(pick, kind)
    for t in B3_TILES:
        if any((a == 0) != (b == 0) for a, b in zip(G.VAN[t], tiles[t])):
            raise SystemExit("  !! batch 3: tile %d's footprint moved" % t)
        if use is not None:
            for k in use[t]["rows"]:
                if k[0] == "general" and any((k[1], v) in RESERVED for v in tiles[t] if v not in G.VAN[t]):
                    raise SystemExit("  !! batch 3: tile %d draws a reserved index in row %d" % (t, k[1]))
    return tiles


def b3_state(pick_tiles):
    van, ours, other = [], [], []
    for t in B3_TILES:
        if pick_tiles is not None and G.CUR[t] == pick_tiles[t]:
            ours.append(t)
        elif G.CUR[t] == G.VAN[t]:
            van.append(t)
        else:
            other.append(t)
    return van, ours, other


def report_b3(use):
    """batch 3's census by object, and its checks"""
    bad = False
    print("\n  BATCH 3 -- THE EDGES AND DOORS (drafted: gfx/drafts/t542_b3/; APPROVED_B3 %s)" %
          (sorted(APPROVED_B3) or "empty"))
    for key, o in B3.items():
        ts = o["tiles"]
        rows = collections.Counter()
        for t in ts:
            for (sym, r), n in use[t]["rows"].items():
                rows["%s r%d" % (TOWN_OF.get(sym, sym.replace("gTileset_", "")), r)] += n
        blocks = sorted({(s, m) for t in ts for (s, m) in use[t]["blocks"]})
        gen = sorted(m for s, m in blocks if s == "general")
        maps = sorted({m for t in ts for m in use[t]["maps"]})
        named = code_names(gen)
        print("    %-7s %2d tiles  %2d blocks (%d General)  %3d maps  %5d draws  rows: %s%s" %
              (key, len(ts), len(blocks), len(gen), len(maps), sum(use[t]["draws"] for t in ts),
               ", ".join("%s %d" % kv for kv in rows.most_common()),
               ("\n            NAMED: " + "; ".join("%s %s" % (b, w) for b, w in named.items())) if named else ""))
    anim = [t for t in B3_TILES if t in G.ANIM_TILES]
    print("    under an animation (416..481, 508..511): %s -- the sea rock and the quay's foot sit on gbawater's "
          "strips as a top layer" % (anim or "none"))
    bad |= bool(anim)
    rsv = [t for t in B3_TILES if any(k[0] == "general" and k[1] in (4, 6) for k in use[t]["rows"])]
    print("    drawn in rows 4 or 6 (the water's own, index 1 reserved): %s" % (rsv or "none"))
    bad |= bool(rsv)
    claim = set(getattr(G, "LATER_T542", set()))
    if not set(B3_TILES) <= claim:
        print("  !! gbageneral.LATER_T542 does not claim batch 3's %s -- its write could draw over them" %
              sorted(set(B3_TILES) - claim))
        bad = True
    else:
        print("    gbageneral.LATER_T542 claims batch 3's %d tiles too (its build keeps them as the engine has them)" %
              len(B3_TILES))
    pick_tiles = draw_b3(next(iter(APPROVED_B3)), use) if len(APPROVED_B3) == 1 else None
    van, ours, other = b3_state(pick_tiles)
    print("    in the engine: %d pret's, %d the approved pick's, %d someone else's%s" %
          (len(van), len(ours), len(other), (" -- %s: find which side is right" % other) if other else ""))
    bad |= bool(other)
    if len(APPROVED_B3) > 1:
        print("  !! APPROVED_B3 holds more than one direction: %s" % sorted(APPROVED_B3))
        bad = True
    return bad


B3_CROPS = [   # (map, x0, y0, w, h in cells, what it shows, detail box inside the crop), first met first
    ("FourIsland", 8, 3, 16, 9, "FOUR ISLAND: the garden -- the thin trees and the puddles", (2, 2, 6, 6)),
    ("FourIsland", 32, 25, 10, 7, "FOUR ISLAND: the south puddles", (1, 2, 8, 5)),
    ("SaffronCity", 47, 6, 8, 5, "BRAZEN CITY: a thin tree by the east road", (2, 1, 5, 4)),
    ("Route12", 14, 32, 10, 7, "ROUTE 12: the islet's rim corners", (3, 2, 6, 3)),
    ("Route20", 36, 0, 16, 7, "ROUTE 20: the sea rocks (and their twin, already ours)", (4, 0, 6, 4)),
    ("VermilionCity", 20, 27, 20, 8, "ARDOR CITY: the quay's edge over the water", (3, 3, 6, 3)),
    ("SSAnne_Exterior", 30, 6, 28, 6, "ARDOR's pier by the S.S. ANNE: the quay's edge", (4, 3, 8, 3)),
    ("Route1", 8, 2, 10, 6, "ROUTE 1: the sand's corner (unchanged: all edge)", (1, 1, 4, 4)),
    ("ViridianForest", 10, 4, 14, 8, "the FOREST: the path's edge (unchanged: the scallop its sides share)", (2, 1, 6, 4)),
]
DOOR_CROPS = [
    ("ViridianCity", 30, 7, 10, 6, "CALLOW CITY: the CENTRE's double door (0x15B)", (4, 1, 5, 4)),
    ("ViridianCity", 30, 16, 10, 6, "CALLOW CITY: the REPO's single door (0x62)", (4, 1, 5, 4)),
    ("CeruleanCity", 18, 15, 16, 8, "DOLDRUM CITY: the CENTRE and the REPO", (2, 2, 5, 4)),
]


def b3_tiles_sheet(versions, use, path, Z=3):
    F, f2 = G.font(15), G.font(11)
    cell = 8 * Z + 4
    lines = [(o["title"][:40], o["tiles"]) for o in B3.values()]
    W = max(330 + 8 * cell + 10, 880)
    rowh = len(versions) * (cell + 2) + 22
    im = Image.new("RGB", (W, 34 + len(lines) * rowh), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-542 batch 3: the 24 tiles at 3x, in their most-drawn row, today and each direction (DRAFT)",
            fill=HEAD, font=F)
    y = 34
    for name, ts in lines:
        dr.text((8, y), name, fill=(200, 200, 210), font=f2)
        for vi, (lab, tl) in enumerate(versions):
            yy = y + 16 + vi * (cell + 2)
            dr.text((8, yy + 6), lab[:24], fill=(170, 170, 180), font=f2)
            for k, t in enumerate(ts):
                key = use[t]["rows"].most_common(1)[0][0]
                im.paste(G.tile_rgb(tl[t], pal_of(key), Z), (330 + k * cell, yy))
        y += rowh
    im.save(path)
    return path


def door_frames_sheet(drawn, path):
    """each direction's two doors as gbadoors would open them: closed, ajar, half, open, in their places -- drawn by
    gbadoors itself from the closed block, with General's tiles.png swapped for the direction's in its read cache"""
    _a, sys.argv = sys.argv, ["gbadoors"]
    try:
        import gbadoors as D
    finally:
        sys.argv = _a
    rel = "data/tilesets/primary/general/tiles.png"
    F, f2 = G.font(15), G.font(12)
    rows = []
    for lab, png in drawn:
        D.CUR._cache.clear()
        if png is not None:
            D.CUR._cache[rel] = open(png, "rb").read()
        table = D.door_table(D.CUR)
        found, _ = D.find_doors(D.CUR, table)
        for d in table:
            if d["name"] in ("sliding_double", "sliding_single") and found.get(d["name"]):
                p = D.plan(d, found[d["name"]], D.CUR.png(d["png"]))
                rows.append(("%s -- %s: closed, ajar, half, open%s" % (lab, d["name"].replace("_", " "),
                             "" if not p["off"] else " (!! a colour outside row 3)"), D.strip(p, p["new"])))
    W = max(s.width for _, s in rows) + 16
    im = Image.new("RGB", (W, 34 + sum(s.height + 22 for _, s in rows)), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-542 batch 3 -- the sliding doors opening, as gbadoors draws them from each closed block (DRAFT)",
            fill=HEAD, font=F)
    y = 34
    for lab, s in rows:
        dr.text((8, y), lab, fill=(220, 220, 230), font=f2)
        im.paste(s, (8, y + 16))
        y += s.height + 22
    im.save(path)
    return path


def draft_b3(use):
    os.makedirs(DRAFT_B3, exist_ok=True)
    summary, drawn = {}, {}
    print("\n  batch 3, directions (24 tiles; 0 new tiles, 0 palette changes, 0 blocks moved)")
    for k, D in B3_STYLES.items():
        tiles = draw_b3(k, use)
        drawn[k] = tiles
        dd = os.path.join(DRAFT_B3, k)
        os.makedirs(dd, exist_ok=True)
        save_tiles(tiles, os.path.join(dd, "tiles.png"))
        ch = [t for t in B3_TILES if tiles[t] != G.VAN[t]]
        summary[k] = dict(title=D["title"], what=D["blurb"], tiles_redrawn=len(ch),
                          unchanged=sorted(set(B3_TILES) - set(ch)), new_tiles=0, palettes_changed=0)
        print("    %s %-18s %d of %d tiles redrawn (unchanged: %s)" % (k, D["title"], len(ch), len(B3_TILES),
                                                                     sorted(set(B3_TILES) - set(ch))))
    diff = [t for t in B3_TILES if B3_OBJ3[t] != "doors" and not (drawn["A"][t] == drawn["B"][t] == drawn["C"][t])]
    if diff:
        raise SystemExit("  !! batch 3: a dictated piece differs between directions: %s" % diff)
    json.dump(dict(ticket="T-542", batch=3, status="DRAFT -- not in the engine", approved=sorted(APPROVED_B3),
                   directions=summary,
                   objects={k: dict(title=o["title"], tiles=o["tiles"], look=o["look"]) for k, o in B3.items()}),
              open(os.path.join(DRAFT_B3, "directions.json"), "w"), indent=1)
    head = "T-542 batch 3 -- %s   (DRAFT; 1x above, 3x below)"
    one = [("TODAY", G.CUR), ("DRAFT (A = B = C)", drawn["A"])]
    allv = [("TODAY", G.CUR)] + [("%s %s" % (k, D["title"]), drawn[k]) for k, D in B3_STYLES.items()]
    out = []
    for i, crop in enumerate(B3_CROPS):
        out.append(map_sheet(crop, one, os.path.join(DRAFT_B3, "t542b3_maps_%02d.png" % (i + 1)), head))
    for i, crop in enumerate(DOOR_CROPS):
        out.append(map_sheet(crop, allv, os.path.join(DRAFT_B3, "t542b3_doors_%d.png" % (i + 1)), head))
    out.append(door_frames_sheet([("TODAY", None)] + [("%s %s" % (k, D["title"]), os.path.join(DRAFT_B3, k, "tiles.png"))
                                                     for k, D in B3_STYLES.items()],
                                 os.path.join(DRAFT_B3, "t542b3_doors_opening.png")))
    out.append(b3_tiles_sheet(allv, use, os.path.join(DRAFT_B3, "t542b3_tiles.png")))
    for p in out:
        print("  sheet:", p)


B3_OBJ3 = {t: k for k, o in B3.items() for t in o["tiles"]}


def main():
    use, nlay, mt_seen = G.scan()
    if WRITE and BATCH == "3":
        if "--approved" not in ARGS or not PICK or PICK not in APPROVED_B3:
            print("  --write --batch 3 refused: batch 3 is a draft. APPROVED_B3 is %s; the user picks a direction "
                  "first, it goes into APPROVED_B3,\n  then --write --batch 3 --approved --pick X writes its 24 tiles "
                  "into General's tiles.png (never a palette, a block or a map),\n  and gbadoors.py --write --approved "
                  "redraws the two sliding doors' opening frames from them." % (sorted(APPROVED_B3) or "empty"))
            return 1
        tiles = draw_b3(PICK, use)
        van, ours, other = b3_state(tiles)
        if other:
            print("  --write refused: batch 3 tiles %s are neither pret's nor direction %s's -- another tool drew "
                  "there; find which side is right first" % (other, PICK))
            return 1
        save_tiles(tiles, os.path.join(PD, "tiles.png"))
        print("  written: batch 3, direction %s -- %d tiles (%d were already so); now gbadoors.py --write --approved"
              % (PICK, len(van), len(ours)))
        return 0
    if WRITE and BATCH == "2":
        if "--approved" not in ARGS or not PICK or PICK not in APPROVED_B2:
            print("  --write --batch 2 refused: batch 2 is a draft. APPROVED_B2 is %s; the user picks a direction "
                  "first, it goes into APPROVED_B2,\n  then --write --batch 2 --approved --pick X writes its 75 tiles "
                  "into General's tiles.png (never a palette, a block or a map)." % (sorted(APPROVED_B2) or "empty"))
            return 1
        tiles = draw_b2(PICK, use)
        van, ours, other = b2_state(tiles)
        if other:
            print("  --write refused: batch 2 tiles %s are neither pret's nor direction %s's -- another tool drew "
                  "there; find which side is right first" % (other, PICK))
            return 1
        save_tiles(tiles, os.path.join(PD, "tiles.png"))
        print("  written: batch 2, direction %s -- %d tiles (%d were already so)" % (PICK, len(van), len(ours)))
        return 0
    if WRITE:
        if "--approved" not in ARGS or not PICK or PICK not in APPROVED:
            print("  --write refused: T-542 is a draft. APPROVED is %s; the user picks a direction first, it goes into "
                  "APPROVED,\n  then --write --approved --pick X writes batch 1's 53 tiles into General's tiles.png "
                  "(never a palette, a block or a map)." % (sorted(APPROVED) or "empty"))
            return 1
        tiles = draw(STYLES[PICK], use)
        van, ours, other = engine_state(tiles)
        if other:
            print("  --write refused: batch 1 tiles %s are neither pret's nor direction %s's -- another tool drew "
                  "there; find which side is right first" % (other, PICK))
            return 1
        save_tiles(tiles, os.path.join(PD, "tiles.png"))
        print("  written: batch 1, direction %s -- %d tiles (%d were already so)" % (PICK, len(van), len(ours)))
        return 0
    bad, rows, c = report(use)
    if DRAFT is not None and BATCH == "2":
        draft_b2(use)
    elif DRAFT is not None and BATCH != "1":
        draft_b3(use)
    elif DRAFT is not None:
        os.makedirs(DRAFT, exist_ok=True)
        versions = [("TODAY", G.CUR)]
        summary = {}
        print("\n  directions (batch 1: 53 tiles each, 0 new tiles, 0 palette changes, 0 blocks moved)")
        for k, D in STYLES.items():
            tiles = draw(D, use)
            dd = os.path.join(DRAFT, k)
            os.makedirs(dd, exist_ok=True)
            save_tiles(tiles, os.path.join(dd, "tiles.png"))
            n = sum(1 for t in BATCH1 if tiles[t] != G.VAN[t])
            moved = sorted({(PART[t]) for t in BATCH1
                            if any(MAT_OF[row_of(t, use)].get(a) != MAT_OF[row_of(t, use)].get(b)
                                   for a, b in zip(G.VAN[t], tiles[t]) if a)})
            footprint = [t for t in BATCH1 if any((a == 0) != (b == 0) for a, b in zip(G.VAN[t], tiles[t]))]
            if footprint:
                raise SystemExit("  !! %s: footprint moved in %s" % (k, footprint))
            summary[k] = dict(title=D["title"], what=D["blurb"], tiles_redrawn=n, new_tiles=0, palettes_changed=0,
                              parts_moved_to_another_ramp=moved)
            versions.append(("%s %s" % (k, D["title"]), tiles))
            print("    %s %-12s %d tiles redrawn; materials moved to another ramp of their row in: %s" %
                  (k, D["title"], n, ", ".join(moved) or "none"))
        json.dump(dict(ticket="T-542", batch=1, status="DRAFT -- not in the engine", approved=sorted(APPROVED),
                       directions=summary), open(os.path.join(DRAFT, "directions.json"), "w"), indent=1)
        json.dump(dict(ticket="T-542", left=len(c["left"]), anim=c["anim"], flat=c["flat"], unseen=c["unseen"],
                       seen=len(c["seen"]), objects=rows), open(os.path.join(DRAFT, "census.json"), "w"), indent=1)
        for i, crop in enumerate(MAP_CROPS):
            print("  sheet:", map_sheet(crop, versions, os.path.join(DRAFT, "t542_maps_%d.png" % (i + 1))))
        print("  sheet:", tiles_sheet(versions, use, os.path.join(DRAFT, "t542_tiles.png")))
    if len(APPROVED) > 1:
        print("  !! APPROVED holds more than one direction: %s" % sorted(APPROVED))
        bad = True
    if len(APPROVED) == 1:
        bad = check_engine(use) or bad
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

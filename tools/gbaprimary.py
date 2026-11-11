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
             row 12, DOLDRUM's 10/11, BRAZEN's 11, CALLOW's 11, ARDOR's 8, HALFTONE's 12, SEVEN ISLAND's 12), the
             secondary-only pieces in General's rows, the cave mouth (also SEVII row 12) and one cliff piece. Each in
             its own town's look (gbatowns.py's), so it waits for this batch's pick. It must also claim 298 and 330,
             which gbageneral's write would still draw (its pass 3 drifted there).
    BATCH 3  THE EDGES AND DOORS (24): the ground strays (a sand edge on 39 maps, beach sand, grass edges, plants),
             the sea's edge and FOUR ISLAND's puddles (gbawater.py's to agree with), and the sliding doors 0x62/0x15B,
             whose opening frames gbadoors.py derives from the closed block -- so gbadoors re-runs after them.

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
    DRAFT = DRAFT_DEFAULT
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

#  batches 2 and 3, by object (anything seen and not named here is reported as unplaced, and fails the report)
LATER = collections.OrderedDict([
    ("2 BRAZEN's roofs lent from General (and 298/330, gbageneral's drift)", (2, [298, 299, 330, 331, 350, 351])),
    ("2 the blue house's pieces in DOLDRUM / CALLOW rows", (2, [344, 347, 360, 362, 363, 376, 377, 379, 552, 568])),
    ("2 VERDIGRIS and LURID's buildings (row 12)", (2, [521, 522, 523, 524, 525, 526, 537, 538, 539, 540, 541, 542,
                                                       553, 554, 555, 556, 569, 570, 571, 583, 584, 585, 586, 587,
                                                       599, 600, 601, 602, 603])),
    ("2 CALLOW and ONE ISLAND pieces (row 11 / 2)", (2, [516, 517, 519, 532, 533, 548, 549, 564, 565, 566])),
    ("2 DOLDRUM and SLATE pieces", (2, [341, 520, 527, 543, 580, 581, 582, 596, 598])),
    ("2 ARDOR's pier", (2, [496, 497])),
    ("2 SEVEN ISLAND's house", (2, [192, 193, 194, 195])),
    ("2 the cave mouth (CAVE_DOOR; SEVII row 12 too)", (2, [302, 303, 318, 319])),
    ("2 a cliff piece (SEVII row 12 too)", (2, [101])),
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
    for title, (batch, ts) in LATER.items():
        s = summarise(title[2:], ts, use)
        rows.append(dict(s, batch=batch))
        named |= set(ts)
    for batch in (2, 3):
        print("\n  BATCH %d -- %s (later)" % (batch, "THE TOWN PIECES" if batch == 2 else "THE EDGES AND DOORS"))
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
    print("    gbageneral writes only tiles still pret's, so once batch 1 is in it cannot put one back; its next write "
          "would still draw 298 and 330 (batch 2 claims them)")
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


def map_sheet(crop, versions, path):
    name, x0, y0, w, h, why, det = crop
    F, f2 = G.font(15), G.font(12)
    shots = [(lab, G.render2(name, tl, None, None, (x0, y0, w, h))) for lab, tl in versions]
    dets = [(lab, G.render2(name, tl, None, None, (x0 + det[0], y0 + det[1], det[2], det[3]))) for lab, tl in versions]
    a, d = shots[0][1], dets[0][1]
    gap = 12
    W = max(len(shots) * (a.width + gap), len(dets) * (d.width * 3 + gap)) + 16
    H = 30 + 16 + a.height + 24 + 16 + d.height * 3 + 14
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "T-542 batch 1 -- %s   (DRAFT; 1x above, 3x below)" % why, fill=HEAD, font=F)
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
    off = [t for t in range(len(G.CUR)) if list(tiles[t]) != list(G.CUR[t])]
    reserved = [t for t in BATCH1 if any((row_of(t, use), v) in RESERVED for v in tiles[t])]
    if off or reserved:
        print("  !! general: the engine differs from `--write --approved --pick %s` in tiles %s%s -- find which side is "
              "right" % (pick, off[:12], ("; reserved indices drawn in %s" % reserved) if reserved else ""))
        return 1
    print("  the engine matches `--write --approved --pick %s` (batch 1, %d tiles; no reserved index drawn)"
          % (pick, len(BATCH1)))
    return 0


def main():
    use, nlay, mt_seen = G.scan()
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
    if DRAFT is not None:
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

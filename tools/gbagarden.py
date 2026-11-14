#!/usr/bin/env python3
"""THE WALLED GARDEN's buildings, inside: the SAFARI tileset redrawn in place in our own hand, from the story (T-540).

    python3 tools/gbagarden.py                      # report: the census (each building, its tileset, the tiles still
                                                    #   Nintendo's, the tool that owns them), the groups tile by tile,
                                                    #   LORELEI's share of the tileset, and every other tool's claim
    python3 tools/gbagarden.py --draft [DIR]        # the three directions (A, B, C) drawn in full: safari_zone_building's
                                                    #   tiles.png and rows 8, 9 as .pal per direction, the GATEKEEPER's
                                                    #   shelf (museum 129..136) per direction, and the contact sheets
                                                    #   (gfx/drafts/t540_interiors/)
    python3 tools/gbagarden.py --write --approved --pick X
                                                    # into the engine -- refused unless X is in APPROVED (empty: the
                                                    #   user has not picked)

THE ANSWER IT FOLLOWS (the user, 2026-11-14, "the last of T-540": the inside of its buildings, as art to pick). T-538
held the SAFARI's buildings out of its three batches until the redesign's words were built; they are (engine
ce345c195, and T-551's GATEKEEPER, dc780f8c5). vision 3.11: THE WALLED GARDEN is a curated, walled platform run as a
sandbox. Unsigned daemons run only inside the wall and nothing leaves unvetted; guests sign in at the gate and are
issued GUESTBOXES that expire; four RINGS of permission count down from RING 3 at the gate to RING 0; the rest houses
are WAITING ROOMS, the review queue; the GATEKEEPER (LATENCY to his staff) has lost his TOKEN; the SECRET HOUSE at
RING 0 gives away DRIVER03 TRAVERSE, the one thing that works outside. Visitors love it; it is safe; nothing in it
surprises anybody. CRAFT RULE 1 HOLDS FOR THE PICTURE: nothing drawn here says what a walled garden is for or costs --
no bars, no locks, no cameras. Only what a visitor would see: a gate that is lovely to pass, a runner to walk in on,
drawers of things waiting, seats to wait on, a lamp that says "not yet" and never anything else.

ONE TILESET, SEVEN ROOMS AND A GUEST (gTileset_SafariZoneBuilding, secondary/safari_zone_building, rows 8, 9, 10):
  FuchsiaCity_SafariZone_Entrance  THE GATE: the gate wall and its doorway into the garden, the sign-in runner with its
                                   emblem (vanilla's ball: here four rings, RING 3 to RING 0), the two lane rails with
                                   their end posts, the drawers, the plants, the waiting stools
  FuchsiaCity_SafariZone_Office    THE OFFICE: walls, floor, plants (its desks are primary/building's: batch D's)
  SafariZone_*_RestHouse (4)       THE WAITING ROOMS: one layout, four maps -- the desk (an L) ending in a ticket post,
                                   the drawers, the stools, the plants
  SafariZone_SecretHouse           THE SECRET HOUSE: the drawers, the stools, the plants, the paved floor
  FourIsland_LoreleisHouse         not the garden's, but it borrows the tileset: tiles 9, 10, 15, 25, 31 (the counter
                                   and the floor) are shared and so change with the garden; her own fifteen tiles
                                   (50..56, 64, 66..72) are NOT redrawn -- the six in row 8 are re-indexed to the
                                   nearest colours of the new row so they keep their look; the nine in row 10 are untouched,
                                   and row 10 is never recoloured (no garden tile is placed in it)
  FuchsiaCity_WardensHouse         the GATEKEEPER's own house is gTileset_Museum, whose every placed tile is already
                                   ours (gbamuseum.py, T-541 A THE SLATE). Only his shelf (129..136, his alone) is
                                   drafted here, a keepsake per direction in the museum's rows as they stand (never
                                   recoloured); gbamuseum's --write redraws those eight tiles, so a pick here means
                                   gbamuseum gives them up first (a GARDEN_SHELF set it skips, as gbacaves' T538_TUNNEL)

WHAT THE RULES LEAVE OUT, AND WHY. The OFFICE's desks (the checked cloths) and the SECRET HOUSE's bookcases and
windows are primary/building's tiles, drawn by batch D and shared with every house in the game: a review desk piled
with requests or a window that looks out would need new tiles and new blocks (a map change) or a primary redraw, and
this tool does neither. So the story is told in what the tileset owns -- the gate, the runner, the rails, the drawers,
the seats, the walls and floors -- and every room carries it.

THE RULES ARE gbahomes.py's (batch D's): redrawn IN PLACE. No block, layer, flip, palette row, behaviour or collision
bit moves and no map is touched; only pixels inside tiles change, and every tile keeps its FOOTPRINT (a transparent
pixel stays transparent, a drawn one stays drawn). Primary rows 0..6 never change colour (no primary tile is placed in
rows 8 or 9 in any of these rooms: checked). Only safari_zone_building's own rows 8 and 9 are recoloured; row 10
(LORELEI's alone) is kept. No animation, no setmetatile, no METATILE_ label names a block of it. 0 new tiles.

Every in-game word: none. This is art. All DRAFT.
"""
import collections, contextlib, io, json, math, os, shutil, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import write_pal, read_pal
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t540_interiors")
#  The user's pick goes here ("A", "B" or "C"); --write refuses anything not in it.
APPROVED = set()

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

#  gbahomes (and gbabuilding under it) read their switches off sys.argv at import (engine.md trap 16)
_argv, sys.argv = sys.argv, ["gbahomes"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import gbahomes as G
finally:
    sys.argv = _argv

Cv, H, M, h, v, hv = G.Cv, G.H, G.M, G.h, G.v, G.hv

SAF = G.Set("saf", "gTileset_SafariZoneBuilding", [8, 9])
SETS = {"saf": SAF}
G.SETS.update(SETS)          # Cv and render_map look sets up there
MUS = G.Set("mus", "gTileset_Museum", [])
MUS_PALS = {r: read_pal(os.path.join(GBA, MUS.dir, "palettes/%02d.pal" % r)) for r in range(16)}
SHELF = list(range(129, 137))                      # the GATEKEEPER's own shelf: his alone (gbamuseum's warden2)
SHELF_BOX = (5, 2, 26, 15)                         # inside its glass, on the 32x16 canvas of 129..132 / 133..136
LORELEI = "FourIsland_LoreleisHouse"
GARDEN = ["FuchsiaCity_SafariZone_Entrance", "FuchsiaCity_SafariZone_Office", "SafariZone_Center_RestHouse",
          "SafariZone_East_RestHouse", "SafariZone_North_RestHouse", "SafariZone_West_RestHouse",
          "SafariZone_SecretHouse"]
#  LORELEI's own tiles (placed by her house alone): never redrawn; row 8's re-indexed to keep their look
LOR_ONLY = sorted(t for t in SAF.use if SAF.use[t]["maps"] == {LORELEI})


# ============================================================================================ drawing helpers
def vlum(K, x, y):
    """vanilla's brightness at a canvas pixel (0..255), in the row its tile is placed in"""
    vv = K.vi(x, y)
    if vv is None:
        return None
    t = K.layout[y // 8][x // 8][0]
    c = SAF.vpal[SAF.home(t)][vv]
    return (c[0] * 3 + c[1] * 6 + c[2]) / 10


def vgreen(K, x, y):
    vv = K.vi(x, y)
    if vv is None:
        return False
    c = SAF.vpal[SAF.home(K.layout[y // 8][x // 8][0])][vv]
    return c[1] > c[0] + 12 and c[1] > c[2] + 12


def lumrank(K, ramp, pred=None):
    """vanilla's light kept as lighting only: each footprint pixel (where pred) -> one of RAMP, ranked"""
    pts = [(x, y) for y in range(K.h) for x in range(K.w) if K.foot(x, y) and (pred is None or pred(x, y))]
    lums = sorted({vlum(K, x, y) for x, y in pts})
    for x, y in pts:
        k = lums.index(vlum(K, x, y))
        K.out[y][x] = ramp[min(len(ramp) - 1, k * len(ramp) // max(1, len(lums)))]


def ell(K, cx, cy, rx, ry, m, ring=None):
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            d = ((x - cx) / max(rx, .5)) ** 2 + ((y - cy) / max(ry, .5)) ** 2
            if d <= 1 and (ring is None or d >= ((rx - ring) / max(rx, .5)) ** 2):
                K.px(x, y, m)


# ============================================================================================ painters
def p_wall(K, D):
    """the rooms' wall, 32px: its head (tile 1, 0..7), the field (17, repeated: 8..15 drawn), its foot (33, 24..31)"""
    K.fn(lambda x, y: D["wall"](x % 8, y))


def p_floor(K, D, shade=False):
    """the main floor (40..43, a 16x16 unit) and the same in a wall's shade (44..47)"""
    K.fn(lambda x, y: D["floor"](x % 16, y % 16, shade))


def p_floor_lit(K, D):
    p_floor(K, D, False)


def p_floor_shade(K, D):
    p_floor(K, D, True)


def p_paving(K, D):
    """the paved floor (15) and its border course (31), each one 8x8 tile repeated"""
    K.fn(lambda x, y: D["paving"](x % 8, y % 8, x >= 16))


def p_gatewall(K, D):
    """the gate's wall (2 head, 18 field, 34 foot), 8px repeated across"""
    K.fn(lambda x, y: D["gatewall"](x % 8, y))


def p_gate(K, D):
    """the gate: its head of wall (2), the piers (3 4 / 19 20 / 35 36, mirrored), the way through (57 / 73 / 89: one
    8px tile twice, so whatever is seen through it repeats at 8px)"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y < 8:
                K.out[y][x] = D["gatewall"](x % 8, y)
            elif 16 <= x < 32:
                K.out[y][x] = D["through"](x % 8, y - 8)
            else:
                xx = x if x < 16 else 47 - x                    # the pier, 0 at the wall .. 15 at the opening
                K.out[y][x] = D["pier"](xx, y - 8, vlum(K, x, y))


def p_runner(K, D):
    """the sign-in runner: its left border (48, flat in vanilla), its head band (49), the field (30), the right border
    (14, placed mirrored), and at its middle the emblem (13 / 29, mirrored): four rings, one inside the next"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if x < 8:
                K.out[y][x] = D["runner"]("edge", 7 - x, y % 8)
            elif x >= 40:
                K.out[y][x] = D["runner"]("edge", x - 40, y % 8)
            elif y < 8:
                K.out[y][x] = D["runner"]("head", x % 8, y)
            else:
                K.out[y][x] = D["runner"]("field", x % 8, y % 8)
    #  the emblem: centred on the 16x16 at (16..31, 16..31)
    for y in range(16, 32):
        for x in range(16, 32):
            r = math.hypot(x - 23.5, y - 23.5)
            m = D["rings"](r)
            if m:
                K.px(x, y, m)


def p_plant(K, D):
    """a plant in its pot, 16x32: the crown (vanilla's greens), the stem, the pot (the rest)"""
    D["plant"](K)


def p_drawers(K, D):
    """the drawers: a stack of units, each 24px (5 or 8 its head, 21, 37), on a plinth (24)"""
    D["drawers"](K)


def p_stool(K, D):
    D["stool"](K)


def p_desk(K, D):
    """the L desk (rest houses) and the gate's lane rails (9 25 12 28, mirrored): vanilla's light as the form -- top,
    front, edge -- and the direction's making on it; 12/28 (the rail's or the desk's end) carries the ticket post"""
    D["desk"](K)


# ============================================================================================ the groups
#  key, set, layout (as it stands), painter, what it is
GROUPS = [
    ("wall",     "saf", M([1, 1], [17, 17], [17, 17], [33, 33]),          p_wall,        "the rooms' wall: head, field, foot"),
    ("floor",    "saf", M([40, 41], [42, 43]),                            p_floor_lit,   "the floor"),
    ("shade",    "saf", M([44, 45], [46, 47]),                            p_floor_shade, "the floor in a wall's shade"),
    ("paving",   "saf", M([15, 15, 31, 31], [15, 15, 31, 31]),            p_paving,      "the paved floor and its border"),
    ("gatewall", "saf", M([2, 2], [18, 18], [18, 18], [34, 34]),          p_gatewall,    "the gate's wall"),
    ("gate",     "saf", M([2, 2, 2, 2, 2, 2], [3, 4, 57, 57, h(4), h(3)], [19, 20, 73, 73, h(20), h(19)],
                          [35, 36, 89, 89, h(36), h(35)]),                p_gate,        "the gate: piers and the way through"),
    ("runner",   "saf", M([48, 49, 49, 49, 49, h(14)], [48, 30, 30, 30, h(30), h(14)], [48, 30, 13, h(13), h(30), h(14)],
                          [48, 30, 29, h(29), h(30), h(14)]),             p_runner,      "the sign-in runner and its emblem"),
    ("plant",    "saf", M([7, h(7)], [23, h(23)], [39, 38], [22, h(22)]),  p_plant,       "a plant in a pot"),
    ("drawers",  "saf", M([5, h(5)], [21, h(21)], [37, h(37)], [8, h(8)], [21, h(21)], [37, h(37)], [24, h(24)]),
     p_drawers, "the drawers (a stack of units on a plinth)"),
    ("stool",    "saf", M([16, h(16)], [32, h(32)]),                      p_stool,       "a stool"),
    ("desk",     "saf", M([9, 10, 10, 10], [25, 26, 11, 11], [25, h(25), 27, 27], [25, h(25), None, None],
                          [h(12), 12, None, None], [h(28), 28, None, None]), p_desk,     "the desk / the lane rails"),
]

#  each own row's fifteen materials, in index order 1..15 (the same layout in every direction)
ROWMATS = {
    ("saf", 8): ["OUT", "SHD", "MID", "HI", "WHT", "G1", "G2", "G3", "C1", "C2", "C3", "R1", "R2", "X", "XL"],
    ("saf", 9): ["OUT", "SHD", "MID", "HI", "WHT", "W1", "W2", "W3", "K1", "K2", "F1", "F2", "F3", "T1", "T2"],
}


# ============================================================================================ resolving
def mats_for(D):
    m = dict(D["mat"])
    return m


def set_palettes(D, S):
    mat = mats_for(D)
    out = {}
    for r in range(16):
        if r in S.rows:
            out[r] = [S.vpal[r][0]] + [mat[m] for m in ROWMATS[S.key, r]]
        else:
            out[r] = list(read_pal(os.path.join(GBA, S.dir, "palettes/%02d.pal" % r)))
    return out


def nearest_index(c, pal):
    return min(range(1, 16), key=lambda i: sum((a - b) ** 2 for a, b in zip(pal[i], c)))


def draw(D):
    """-> {setkey: (tiles, palettes)} (with "mus": the GATEKEEPER's shelf), owner {(setkey, t): group}"""
    out = {k: ([t[:] for t in S.cur], set_palettes(D, S)) for k, S in SETS.items()}
    owner = {}
    mat = mats_for(D)
    for key, setkey, layout, painter, what in GROUPS:
        S = SETS[setkey]
        K = Cv(layout, setkey)
        painter(K, D)
        for t, mats in K.tiles().items():
            if (setkey, t) in owner or t >= S.nvan or t not in S.use:
                continue
            spals = out[setkey][1]
            rows = dict(S.use[t]["rows"])
            own = {r: spals[r] for r in S.rows}
            Dm = {"mat": mat, "_index": {(r, m): i + 1 for r in S.rows for i, m in enumerate(ROWMATS[S.key, r])}}
            out[setkey][0][t] = G.resolve(mats, S.van[t], rows, Dm, own)
            owner[setkey, t] = key
    #  LORELEI's own row-8 tiles: re-indexed to the nearest colour of the new row, so they look as they did
    tiles, pals = out["saf"]
    for t in LOR_ONLY:
        r = SAF.home(t)
        if r not in SAF.rows:
            continue
        cache = {}
        tiles[t] = [0 if vv == 0 else cache.setdefault(vv, nearest_index(SAF.vpal[r][vv], pals[r])) for vv in SAF.van[t]]
        owner["saf", t] = "lorelei"
    #  the GATEKEEPER's shelf, in the museum's rows as they stand
    out["mus"] = (shelf_tiles(D), {r: MUS_PALS[r] for r in range(16)})
    return out, owner


def shelf_tiles(D):
    """museum tiles with 129..136 redrawn: today's case (gbamuseum's frame and glass) kept, and inside the glass the
    direction's keepsake, painted in RGB and taken to the nearest colour of the tile's own museum row"""
    tiles = [t[:] for t in MUS.cur]
    lay = [SHELF[:4], SHELF[4:]]
    im = Image.new("RGB", (32, 16))
    o = im.load()
    for ty, r in enumerate(lay):
        for tx, t in enumerate(r):
            pal = MUS_PALS[MUS.home(t)]
            for q in range(64):
                o[tx * 8 + q % 8, ty * 8 + q // 8] = tuple(pal[MUS.cur[t][q]])
    #  the glass inside the case, cleared to its own pale glass
    x0, y0, x1, y1 = SHELF_BOX
    glass = MUS_PALS[10][6]
    d = ImageDraw.Draw(im)
    d.rectangle((x0, y0, x1, y1), fill=glass)
    for k in range(4):                                       # the glass's one diagonal glint, as gbamuseum draws it
        o[x0 + 1 + k, y0 + 4 - k] = tuple(MUS_PALS[10][7])
    D["keepsake"](d, o)
    for ty, r in enumerate(lay):
        for tx, t in enumerate(r):
            pal = MUS_PALS[MUS.home(t)]
            px = []
            for q in range(64):
                if MUS.cur[t][q] == 0:
                    px.append(0)
                else:
                    px.append(nearest_index(o[tx * 8 + q % 8, ty * 8 + q // 8], pal))
            tiles[t] = px
    return tiles


# ============================================================================================ A THE ARBOUR
#  the garden kept by hand, HEARTH and THE KEEPING carried in through the gate: limewash with a green trellis, a brick
#  path, sandstone flags, the wall's dressed stone, oak, brass, clipped box, a moss runner
def A_wall(x, y):
    if y < 8:                                                    # an oak picture rail under the cornice
        return "OUT" if y == 7 else "K2" if y >= 4 else ("W3" if y == 0 else "W2")
    if y < 24:                                                   # limewash with a green trellis, diamonds 8px
        yy = y % 8
        if (x + yy) % 8 == 0 or (x - yy) % 8 == 4:
            return "K1"
        return "W3" if (x * 3 + yy) % 11 == 0 else "W2"
        # (the lattice is painted on: the wall stays flat)
    return "OUT" if y in (24, 31) else "K2" if y < 29 else "SHD"     # a brick skirting


def A_floor(x, y, shade):
    """brick in basketweave: two bricks across, then two up, 8px squares"""
    bx, by = x // 8, y // 8
    xx, yy = x % 8, y % 8
    horiz = (bx + by) % 2 == 0
    joint = (yy in (3, 7)) if horiz else (xx in (3, 7))
    if joint:
        m = "F1"
    else:
        m = "F3" if (H(x, y, 3) % 9 == 0) else "F2"
    if shade:
        m = {"F3": "F2", "F2": "F1", "F1": "SHD"}[m]
    return m


def A_paving(x, y, band):
    """sandstone flags (15), the border course in brick on edge (31)"""
    if band:
        return "K2" if y % 4 else "F1"
    if x == 7 or y == 7:
        return "MID"
    return "T2" if H(x, y, 7) % 7 else "T1"


def A_gatewall(x, y):
    """the wall itself from inside: dressed sandstone, 8px courses, a lit coping"""
    if y < 3:
        return "WHT" if y == 0 else "HI"
    if y == 3:
        return "MID"
    if y >= 29:
        return "OUT" if y == 31 else "SHD"
    yy = y % 8
    if yy == 3 or x == 0:
        return "MID"
    return "HI" if H(x, y, 9) % 6 == 0 else "C3"


def A_pier(x, y, lum):
    """a sandstone pier with a keystone head, chamfered to the opening"""
    if x >= 13:
        return "OUT" if x == 15 else "SHD"
    if y < 4:
        return "WHT" if y == 0 else "HI"
    if y >= 21:
        return "OUT" if y == 23 else "SHD"
    if x == 0:
        return "MID"
    if y % 6 == 5:
        return "MID"
    return "HI" if x < 3 else "C3"


def A_through(x, y):
    """the way through: the garden beyond, lit -- a gold sky, the round crowns of the trees, the path's light"""
    if y < 6:
        return "XL" if y < 3 else "X"
    if y < 14:
        r = math.hypot(x - 3.5, y - 10)
        return "G3" if r < 2 else "G2" if r < 4 else "G1"
    if y < 22:
        return "XL" if 2 <= x <= 5 else ("G2" if y < 17 else "G1")
    return "C3" if 1 <= x <= 6 else "MID"


def A_runner(part, x, y):
    """a moss-green woven runner with a darker border and a brass rod at its head"""
    if part == "edge":
        return "OUT" if x == 0 else "R1" if x < 4 else ("G1" if (y % 2) else "R1")
    if part == "head":                                           # the head band (two rows of 49): a darker weave
        return "G2" if (x + y) % 4 == 0 else "R1"
    return "R2" if (x + 2 * y) % 4 else "G2"


def A_rings(r):
    if r < 1.2:
        return "X"
    for rr in (7.0, 5.0, 3.0):
        if abs(r - rr) < 0.6:
            return "XL" if rr == 7.0 else "X"
    return None


def A_plant(K):
    """a clipped box ball in an oak planter with brass corners"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y < 18 and vgreen(K, x, y):
                r = math.hypot(x - 7.5, y - 8)
                c = H(x, y, 11) % 5
                K.out[y][x] = "G3" if (x < 7 and y < 7 and c) else "G1" if (r > 6.5 or c == 0) else "G2"
            elif y < 22:
                K.out[y][x] = "C1"
            else:
                yy = y - 22
                if yy in (0, 9):
                    K.out[y][x] = "OUT"
                elif x in (3, 4, 11, 12) and yy in (1, 2):
                    K.out[y][x] = "X"
                else:
                    K.out[y][x] = "C3" if yy == 1 else ("C1" if x % 4 == 0 else "C2")
    K.rim("OUT")


def A_drawers(K):
    """oak seed drawers, a brass label holder on each with a blank card in it"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y >= 48:                                          # the plinth
                K.out[y][x] = "OUT" if y in (48, 55) else "C1"
                continue
            ly = y % 24
            if ly in (0, 23) or x in (x0, x1):
                K.out[y][x] = "OUT"
            elif ly == 1:
                K.out[y][x] = "C3"
            elif x in (x0 + 1, x1 - 1) or ly in (2, 22):
                K.out[y][x] = "C1"
            elif ly == 12:
                K.out[y][x] = "C1"                               # two drawers to a unit
            else:
                K.out[y][x] = "C2"
        for base in (0, 24):
            for ly in (5, 15):
                yy = base + ly
                K.rect(5, yy, 10, yy + 3, "X")
                K.rect(6, yy + 1, 9, yy + 2, "WHT")              # the card: blank


def A_stool(K):
    """a stool cut from a log: the rings on its top, the bark round it"""
    x0, y0, x1, y1 = K.bbox()
    cx = (x0 + x1) / 2
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y <= y0 + 7:
                r = math.hypot((x - cx) / 1.6, (y - y0 - 3.5))
                K.out[y][x] = "C3" if int(r * 1.3) % 2 == 0 else "C2"
            else:
                K.out[y][x] = "C1" if (x + y) % 3 else "SHD"
    K.rim("OUT")


def desk_common(K, top, front, edge, light):
    """vanilla's desk/rail light as the form: brightest = top, mid = front, darkest = edges"""
    lumrank(K, [edge, edge, front, front, top, top])
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y) and K.out[y][x] == top and K.edge(x, y) and y < 8:
                K.out[y][x] = light


def ticket_post(K, body, lamp, base):
    """the end of the desk / rail (12 and 28, canvas 0..15 x 32..47): a ticket post -- a slim post with a lamp"""
    for y in range(32, 48):
        for x in range(0, 16):
            if not K.foot(x, y):
                continue
            if 6 <= x <= 9 and y >= 34:
                K.out[y][x] = body if y < 45 else base
    K.rect(5, 33, 10, 36, "OUT")
    K.rect(6, 34, 9, 35, lamp)


def A_desk(K):
    """oak with a brass edge; the end post a brass ticket post with a warm lamp"""
    desk_common(K, "C3", "C2", "C1", "X")
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y) and K.out[y][x] == "C2" and (x + 2 * y) % 9 == 0:
                K.out[y][x] = "C1"                               # the grain
    ticket_post(K, "X", "XL", "C1")
    K.rim("OUT")


def A_keepsake(d, o):
    """the GATEKEEPER's shelf: old merchandise from when it was the SAFARI ZONE, kept on purpose -- a pennant on a
    stick, a souvenir mug, a little plush with round ears. No word on any of it."""
    d.polygon([(8, 4), (16, 7), (8, 10)], fill=(186, 106, 56))      # the pennant
    d.line((8, 3, 8, 14), fill=(92, 62, 42))
    d.line((9, 6, 11, 7), fill=(232, 172, 110))
    d.rectangle((14, 10, 18, 14), fill=(240, 240, 230))              # the mug
    d.line((19, 11, 19, 13), fill=(240, 240, 230))
    d.line((14, 11, 18, 11), fill=(84, 136, 76))
    d.ellipse((20, 8, 25, 14), fill=(184, 138, 90))                  # the plush
    d.ellipse((20, 6, 22, 8), fill=(138, 96, 60))
    d.ellipse((23, 6, 25, 8), fill=(138, 96, 60))
    o[21, 10] = o[24, 10] = (30, 32, 42)
    d.line((5, 15, 26, 15), fill=(92, 62, 42))                       # the shelf


A = dict(
    name="A", title="THE ARBOUR",
    lines=["The garden kept by hand (HEARTH and THE KEEPING carried in through the gate): limewash with a green trellis,",
           "a brick path in basketweave, sandstone flags, the wall dressed sandstone, a lit way through to the trees. A",
           "moss runner to sign in on, four brass rings at its heart; oak drawers each with a blank card; log stools;",
           "box balls in oak planters; the desks oak with a brass ticket post. The GATEKEEPER's shelf: pennant, mug, plush."],
    mat=dict(OUT=(54, 42, 34), SHD=(98, 82, 66), MID=(152, 138, 120), HI=(216, 206, 188), WHT=(248, 244, 230),
             G1=(46, 86, 46), G2=(82, 138, 60), G3=(150, 196, 92), C1=(112, 74, 44), C2=(164, 116, 70),
             C3=(206, 160, 104), R1=(70, 96, 58), R2=(118, 148, 84), X=(212, 168, 72), XL=(250, 226, 150),
             W1=(206, 190, 156), W2=(232, 220, 192), W3=(246, 240, 222), K1=(110, 140, 84), K2=(150, 96, 64),
             F1=(118, 66, 50), F2=(168, 96, 68), F3=(198, 128, 88), T1=(196, 184, 156), T2=(224, 214, 190)),
    wall=A_wall, floor=A_floor, paving=A_paving, gatewall=A_gatewall, pier=A_pier, through=A_through,
    runner=A_runner, rings=A_rings, plant=A_plant, drawers=A_drawers, stool=A_stool, desk=A_desk, keepsake=A_keepsake,
)


# ============================================================================================ B THE LOBBY
#  the platform as its own brochure: white, soft grey and one mint light; frosted glass at the gate; every drawer's lamp
#  amber -- the colour of waiting -- and none of them green
def B_wall(x, y):
    if y < 8:
        return "WHT" if y < 4 else "K1" if y == 5 else "W3"              # one mint line under the ceiling
    if y < 24:
        return "W2" if (y % 8) else "W1"                                 # wide white panels, a shadow gap
    return "K2" if y < 30 else "SHD"


def B_floor(x, y, shade):
    """large pale grey porcelain tiles, 16px, a fine joint"""
    m = "F1" if (x == 15 or y == 15) else ("F3" if (x + y) < 6 else "F2")
    if shade:
        m = {"F3": "F2", "F2": "F1", "F1": "SHD"}[m]
    return m


def B_paving(x, y, band):
    """mint carpet tiles (15), and a grey border (31)"""
    if band:
        return "F1" if (x + y) % 4 == 0 else "MID"
    return "T1" if (x + 2 * y) % 5 == 0 else "T2"


def B_gatewall(x, y):
    if y < 3:
        return "WHT"
    if y == 3:
        return "K1" if False else "HI"
    if y >= 29:
        return "OUT" if y == 31 else "SHD"
    return "C3" if x % 8 else "C2"


def B_pier(x, y, lum):
    """a white frame, a mint light along its inner edge"""
    if x >= 14:
        return "OUT" if x == 15 else "XL"
    if y >= 21:
        return "OUT" if y == 23 else "MID"
    return "WHT" if x < 6 else "C2" if x == 13 else "C3"


def B_through(x, y):
    """frosted glass doors, two leaves to the 8px, a mint line at hand height: light, not a view"""
    if x in (0, 7):
        return "MID"
    if y == 12:
        return "XL"
    if y >= 22:
        return "SHD" if y == 23 else "MID"
    return "WHT" if (x + y) % 5 == 0 else "HI"


def B_runner(part, x, y):
    if part == "edge":
        return "OUT" if x == 0 else "R1"
    if part == "head":
        return "XL" if y in (3, 4) else "R1"
    return "R2" if (y % 8) not in (0,) else "R1"


def B_rings(r):
    for rr in (7.0, 5.0, 3.0, 1.0):
        if abs(r - rr) < 0.55:
            return "XL" if rr == 1.0 else "WHT"
    return None


def B_plant(K):
    """a clipped sphere, smooth as a render, on a white stem in a white cube"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y < 18 and vgreen(K, x, y):
                r = math.hypot(x - 5.5, y - 5)                       # lit from the upper left, no texture
                K.out[y][x] = "G3" if r < 4 else "G2" if r < 9.5 else "G1"
            elif y < 22:
                K.out[y][x] = "C2"
            else:
                K.out[y][x] = "WHT" if y < 24 else ("C2" if x > 10 else "C3")
    K.rim("OUT")


def B_drawers(K):
    """white file drawers, a recessed pull, and on each an amber lamp: all of them waiting"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y >= 48:
                K.out[y][x] = "OUT" if y == 55 else "MID"
                continue
            ly = y % 24
            if ly in (0, 23) or x in (x0, x1):
                K.out[y][x] = "SHD"
            elif ly in (11, 12):
                K.out[y][x] = "C1"
            else:
                K.out[y][x] = "C3" if ly < 3 or ly in (13, 14) else "C2"
        for base in (0, 24):
            for ly in (6, 17):
                yy = base + ly
                K.hline(5, 10, yy, "MID")
                K.px(12, yy - 1, "X")
                K.px(12, yy, "X")


def B_stool(K):
    """a moulded seat in mint on a white stem"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y <= y0 + 8:
                K.out[y][x] = "R2" if y > y0 + 1 else "XL"
            else:
                K.out[y][x] = "C2" if 5 <= x <= 10 else "MID"
    K.rim("OUT")


def B_desk(K):
    """white, a mint light strip along its edge; the end post a white ticket post, its lamp amber"""
    desk_common(K, "C3", "C2", "C1", "XL")
    ticket_post(K, "WHT", "X", "MID")
    K.rim("SHD")


def B_keepsake(d, o):
    """the GATEKEEPER's shelf: the old merchandise still boxed, three boxes stood in a row, a round sticker on each and
    nothing written"""
    for k, (x, col) in enumerate(((7, (84, 136, 76)), (13, (186, 106, 56)), (19, (84, 124, 146)))):
        d.rectangle((x, 6, x + 5, 14), fill=(240, 240, 230))
        d.rectangle((x, 6, x + 5, 8), fill=col)
        d.rectangle((x + 1, 10, x + 4, 13), fill=(150, 188, 200))   # the window in the box
        o[x + 2, 11] = col
        o[x + 4, 7] = (232, 172, 110)                                 # the sticker
    d.line((5, 15, 26, 15), fill=(92, 62, 42))


B = dict(
    name="B", title="THE LOBBY",
    lines=["The platform as its own brochure: white, soft grey and one mint light. White panels with a shadow gap,",
           "pale porcelain, mint carpet tiles; the gate's wall white, the way through frosted glass doors -- light, not",
           "a view. A mint runner with four white rings; white file drawers each with an amber lamp, all of them",
           "waiting; moulded seats; clipped spheres in white cubes. The GATEKEEPER's shelf: the old merchandise, still boxed."],
    mat=dict(OUT=(44, 48, 56), SHD=(110, 118, 128), MID=(168, 176, 184), HI=(220, 226, 230), WHT=(250, 252, 252),
             G1=(46, 104, 84), G2=(78, 156, 118), G3=(150, 212, 176), C1=(186, 194, 200), C2=(222, 228, 232),
             C3=(242, 246, 248), R1=(92, 150, 138), R2=(150, 204, 190), X=(240, 170, 60), XL=(120, 226, 196),
             W1=(206, 214, 218), W2=(234, 240, 242), W3=(248, 250, 250), K1=(96, 192, 168), K2=(150, 160, 170),
             F1=(170, 176, 182), F2=(202, 208, 212), F3=(226, 230, 232), T1=(140, 190, 180), T2=(184, 222, 212)),
    wall=B_wall, floor=B_floor, paving=B_paving, gatewall=B_gatewall, pier=B_pier, through=B_through,
    runner=B_runner, rings=B_rings, plant=B_plant, drawers=B_drawers, stool=B_stool, desk=B_desk, keepsake=B_keepsake,
)


# ============================================================================================ C THE GLASSHOUSE
#  everything under glass, beautiful and kept: whitewashed panes (light comes in; nothing is seen through them) in
#  white iron, a terracotta dwarf wall, red quarry tiles, an encaustic floor, citrus in tubs, a coir runner
def C_wall(x, y):
    if y < 8:
        return "K1" if y in (0, 1, 6) else ("W1" if y == 7 else "W3")    # the iron cornice
    if y < 24:
        if x == 0 or y % 8 == 0:
            return "K1"                                                   # the glazing bars, 8px
        return "W3" if (x + (y % 8)) % 6 == 0 else "W2" if (y % 8) < 5 else "W1"
    return "OUT" if y in (24, 31) else "K2" if y < 30 else "SHD"          # the dwarf wall


def C_floor(x, y, shade):
    """red quarry tiles, 8px, one in four a shade darker"""
    xx, yy = x % 8, y % 8
    if xx == 7 or yy == 7:
        m = "F1"
    else:
        m = "F3" if (xx + yy) < 3 else ("F1" if (x // 8 == 1 and y // 8 == 0 and (xx + yy) % 5 == 0) else "F2")
    if shade:
        m = {"F3": "F2", "F2": "F1", "F1": "SHD"}[m]
    return m


def C_paving(x, y, band):
    """encaustic tile: a dark lozenge on pale stone (15); a terracotta border (31)"""
    if band:
        return "F2" if (x + y) % 2 else "F1"
    d = abs(x - 3.5) + abs(y - 3.5)
    return "OUT" if d < 1.6 else "F2" if d < 2.6 else "T2" if d < 6 else "T1"


def C_gatewall(x, y):
    """the glasshouse's end wall: whitewashed panes in white iron"""
    if y < 3:
        return "WHT"
    if y >= 28:
        return "OUT" if y in (28, 31) else "C1"
    if x == 0 or y % 8 == 3:
        return "WHT"
    return "HI" if (x + y) % 7 else "MID"


def C_pier(x, y, lum):
    """a white iron door case, a scroll at its head"""
    if x >= 13:
        return "OUT" if x == 15 else "SHD"
    if y < 5:
        return "WHT" if (x + y) % 3 else "HI"
    if y >= 20:
        return "OUT" if y == 23 else "C1"
    return "WHT" if x in (0, 11, 12) else "HI"


def C_through(x, y):
    """the way through: the garden under the open sky, past an iron door held open"""
    if y < 4:
        return "WHT" if y < 2 else "HI"
    if y < 16:
        if x == 0:
            return "WHT"
        r = math.hypot(x - 4, y - 10)
        return "X" if r < 1 else "G3" if r < 2.5 else "G2" if r < 4.2 else "G1"
    if y < 22:
        return "G2" if (x + y) % 3 else "G1"
    return "C2" if y < 23 else "C1"


def C_runner(part, x, y):
    """a coir mat runner, bound in green"""
    if part == "edge":
        return "OUT" if x == 0 else "G1" if x < 3 else "R1"
    if part == "head":
        return "G1" if y in (0, 1) else ("R2" if (x + y) % 2 else "R1")
    return "R2" if (x + y) % 2 else ("R1" if (x - y) % 4 == 0 else "R2")


def C_rings(r):
    for rr, m in ((7.0, "G1"), (5.0, "G2"), (3.0, "G3"), (1.0, "X")):
        if abs(r - rr) < 0.6 or (rr == 1.0 and r < 1.2):
            return m
    return None


def C_plant(K):
    """a standard citrus in a terracotta tub: the crown with fruit in it"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y < 18 and vgreen(K, x, y):
                c = H(x, y, 21) % 13
                K.out[y][x] = "X" if c == 0 and 2 < y < 15 else "G3" if (x < 7 and y < 8 and c % 3) else \
                    "G1" if c % 4 == 0 else "G2"
            elif y < 22:
                K.out[y][x] = "C1"
            else:
                yy = y - 22
                K.out[y][x] = "C3" if yy < 2 else ("C1" if yy in (5, 9) else "C2")
    K.rim("OUT")


def C_drawers(K):
    """potting-bench crates of seedlings in trays, a tag tied on each, blank"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y >= 48:
                K.out[y][x] = "OUT" if y == 55 else "C1"
                continue
            ly = y % 24
            if ly in (0, 23) or x in (x0, x1):
                K.out[y][x] = "OUT"
            elif ly < 6:                                             # the seedlings showing over the rim
                K.out[y][x] = ("G3" if (x + ly) % 3 == 0 else "G2") if ly > 1 else "G1"
            elif ly % 5 == 0:
                K.out[y][x] = "C1"                                   # the slats
            else:
                K.out[y][x] = "C3" if x < 5 else "C2"
        for base in (0, 24):
            K.rect(10, base + 9, 12, base + 12, "WHT")               # the tag
            K.px(11, base + 8, "SHD")


def C_stool(K):
    """a white iron garden stool, a green cushion on it"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y <= y0 + 7:
                K.out[y][x] = "G3" if y == y0 + 1 else "G2"
            else:
                K.out[y][x] = "WHT" if (x % 3 == 0 or y == y0 + 8) else "HI"
    K.rim("OUT")


def C_desk(K):
    """white marble on white iron; the end post an iron ticket post, its lamp a warm glass"""
    desk_common(K, "WHT", "HI", "MID", "WHT")
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y) and K.out[y][x] == "WHT" and H(x, y, 31) % 11 == 0:
                K.out[y][x] = "HI"                                   # the veins
    ticket_post(K, "SHD", "XL", "OUT")
    K.rim("OUT")


def C_keepsake(d, o):
    """the GATEKEEPER's shelf: the old gate's sign, a painted board kept on purpose and stood with its face to the
    wall -- what it says is on the other side, and nobody here reads it"""
    d.rectangle((7, 5, 24, 13), fill=(138, 96, 60))
    d.rectangle((8, 6, 23, 12), fill=(184, 138, 90))
    for x in (10, 15, 20):                                           # the battens on its back
        d.line((x, 6, x, 12), fill=(92, 62, 42))
    d.line((9, 13, 9, 15), fill=(92, 62, 42))
    d.line((22, 13, 22, 15), fill=(92, 62, 42))
    d.line((5, 15, 26, 15), fill=(92, 62, 42))


C = dict(
    name="C", title="THE GLASSHOUSE",
    lines=["Everything under glass, beautiful and kept: whitewashed panes in white iron (the light comes in, nothing",
           "is seen through them), a terracotta dwarf wall, red quarry tiles, encaustic flags; the",
           "way through an iron door held open on the garden. A coir runner with four green rings; crates of seedlings",
           "with blank tags; iron stools; citrus in tubs. The GATEKEEPER's shelf: the old sign, its face to the wall."],
    mat=dict(OUT=(40, 46, 44), SHD=(86, 98, 92), MID=(150, 162, 154), HI=(212, 222, 214), WHT=(246, 250, 244),
             G1=(36, 84, 52), G2=(70, 134, 66), G3=(138, 190, 84), C1=(150, 82, 52), C2=(196, 118, 74),
             C3=(226, 160, 108), R1=(110, 92, 60), R2=(170, 146, 96), X=(236, 140, 40), XL=(252, 206, 96),
             W1=(168, 200, 200), W2=(204, 226, 224), W3=(232, 244, 240), K1=(238, 242, 238), K2=(166, 92, 62),
             F1=(118, 62, 46), F2=(164, 92, 64), F3=(196, 124, 84), T1=(204, 198, 182), T2=(234, 230, 214)),
    wall=C_wall, floor=C_floor, paving=C_paving, gatewall=C_gatewall, pier=C_pier, through=C_through,
    runner=C_runner, rings=C_rings, plant=C_plant, drawers=C_drawers, stool=C_stool, desk=C_desk, keepsake=C_keepsake,
)

STYLES = {"A": A, "B": B, "C": C}


# ============================================================================================ sheets
BG, INK, RED, SOFT = (250, 248, 242), (24, 24, 24), (120, 20, 30), (90, 90, 90)
ROOMS = [("FuchsiaCity_SafariZone_Entrance", "THE GATE (sign-in)"), ("SafariZone_Center_RestHouse", "a WAITING ROOM"),
         ("SafariZone_SecretHouse", "the SECRET HOUSE"), ("FuchsiaCity_SafariZone_Office", "the OFFICE"),
         ("FuchsiaCity_WardensHouse", "the GATEKEEPER's house"), (LORELEI, "LORELEI's house (shares 5 tiles)")]


def render(m, sets):
    """a room as the engine would draw it with SETS (None: today)"""
    if sets is None:
        return G.render_map(m)
    if m == "FuchsiaCity_WardensHouse":
        old = G.SETS.get("mus")
        G.SETS["mus"] = MUS
        try:
            return G.render_map(m, ({"mus": sets["mus"]}, None))
        finally:
            if old is None:
                del G.SETS["mus"]
    return G.render_map(m, ({"saf": sets["saf"]}, None))


def contact_sheets(out_dir, states):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: Nintendo's SAFARI ZONE tiles (the desks, bookcases, windows and the mats are",
                              "primary/building's, batch D's, already ours; the GATEKEEPER's house is gbamuseum's A)"])}
    for k in STYLES:
        titles[k] = ("%s %s" % (k, STYLES[k]["title"]), STYLES[k]["lines"])
    pad = 10
    paths = []
    for part, rooms in enumerate((ROOMS[:3], ROOMS[3:])):
        blocks = []
        for k in names:
            ims = [render(m, states[k]) for m, _ in rooms]
            ims = [i.resize((i.width * 2, i.height * 2), Image.NEAREST) for i in ims]
            t, lines = titles[k]
            th = 8 + 12 * len(lines) + 18
            W = sum(i.width for i in ims) + pad * (len(ims) + 1)
            im = Image.new("RGB", (max(W, 900), th + max(i.height for i in ims) + pad), BG)
            d = ImageDraw.Draw(im)
            d.text((pad, 6), t, fill=RED)
            for j, s in enumerate(lines):
                d.text((pad + 150, 6 + 12 * j), s, fill=INK)
            x = pad
            for i, (m, cap) in zip(ims, rooms):
                d.text((x, th - 14), cap, fill=SOFT)
                im.paste(i, (x, th))
                x += i.width + pad
            blocks.append(im)
        W = max(b.width for b in blocks)
        sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
        d = ImageDraw.Draw(sh)
        d.text((pad, 8), "T-540 DRAFT -- THE WALLED GARDEN inside, rooms at 2x: three directions beside today's (redrawn "
                         "in place: no block, collision or palette row moves; row 10 kept). (%d/2)" % (part + 1), fill=INK)
        y = 30
        for b in blocks:
            sh.paste(b, (0, y))
            y += b.height
        p = os.path.join(out_dir, "t540_rooms_2x_%d.png" % (part + 1))
        sh.save(p)
        paths.append(p)
    #  the details at 4x: the gate and the runner; the waiting room's desk, drawers and stools; the keeper's shelf
    DET = [("FuchsiaCity_SafariZone_Entrance", (2, 0, 7, 5), "the gate, the rails, the runner's emblem"),
           ("SafariZone_Center_RestHouse", (7, 5, 13, 11), "the desk and its ticket post, the drawers"),
           ("FuchsiaCity_WardensHouse", (4, 3, 8, 6), "the GATEKEEPER's shelf (museum 129..136)")]
    rowsim = []
    for k in names:
        crops = []
        for m, (x0, y0, x1, y1), cap in DET:
            im = render(m, states[k]).crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
            crops.append((im.resize((im.width * 4, im.height * 4), Image.NEAREST), cap))
        rowsim.append((k, crops))
    cw = sum(c.width for c, _ in rowsim[0][1]) + pad * 4 + 150
    ch = max(c.height for c, _ in rowsim[0][1]) + 24
    det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
    d = ImageDraw.Draw(det)
    d.text((pad, 8), "T-540 DRAFT -- details at 4x: %s." % "; ".join(c for _, _, c in DET), fill=INK)
    y = 30
    for k, crops in rowsim:
        d.text((pad, y + 6), titles[k][0], fill=RED)
        x = 150
        for c, cap in crops:
            d.text((x, y + 2), cap, fill=SOFT)
            det.paste(c, (x, y + 16))
            x += c.width + pad
        y += ch
    p = os.path.join(out_dir, "t540_detail_4x.png")
    det.save(p)
    paths.append(p)
    return paths


# ============================================================================================ report
def report():
    print("T-540 -- THE WALLED GARDEN's buildings, inside (gTileset_SafariZoneBuilding; the GATEKEEPER's shelf)\n")
    c = G.census_set(SAF.sym)
    print("  safari_zone_building: %d vanilla of %d placed; rows %s; animation %s; maps: %s"
          % (c["vanilla"], c["used"], c["rows"], c["anim"] or "none", ", ".join(c["maps"])))
    print("\n  the census, building by building (secondary tiles placed / still Nintendo's drawing; primary's):")
    for m in GARDEN + ["FuchsiaCity_WardensHouse", LORELEI]:
        lid = G.LAYOUT_OF_MAP[m]
        l = next(x for x in G.LAYOUTS if x["id"] == lid)
        S = SAF if l["secondary_tileset"] == SAF.sym else MUS
        st, pt = set(), set()
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        for k in range(0, len(bd) - 1, 2):
            b = struct.unpack_from("<H", bd, k)[0] & 0x3FF
            buf, bb = (S.mt, b - 640) if b >= 640 else (G.PMT, b)
            if (bb + 1) * 16 > len(buf):
                continue
            for e in struct.unpack_from("<8H", buf, bb * 16):
                t = e & 0x3FF
                if t >= 640:
                    st.add(t - 640)
                elif t:
                    pt.add(t)
        sv = [t for t in st if t < S.nvan and S.cur[t] == S.van[t] and len(set(S.cur[t])) > 1]
        pv = [t for t in pt if G.GB.VAN[t] == G.GB.CUR[t] and len(set(G.GB.VAN[t])) > 1]
        own = "gbagarden (this, DRAFT)" if S is SAF else "gbamuseum (T-541 A, built); shelf 129..136 drafted here"
        print("    %-34s %-30s sec %2d placed, %2d Nintendo's; primary %2d placed, %d Nintendo's -> %s"
              % (m, S.sym, len(st), len(sv), len(pt), len(pv), own))
    owner = {}
    for key, setkey, layout, painter, what in GROUPS:
        for r in layout:
            for s in r:
                if s is not None:
                    owner.setdefault((setkey, s if isinstance(s, int) else s[0]), key)
    print("\n  %-9s %5s %6s %4s  %s" % ("group", "tiles", "draws", "maps", "what"))
    for key, setkey, layout, painter, what in GROUPS:
        ts = sorted(t for (sk, t), k in owner.items() if k == key and t in SAF.use and t < SAF.nvan)
        draws = sum(SAF.use[t]["n"] for t in ts)
        maps = {m for t in ts for m in SAF.use[t]["maps"]}
        print("  %-9s %5d %6d %4d  %s" % (key, len(ts), draws, len(maps), what))
    bad = 0
    used = {t for t in SAF.use if t < SAF.nvan}
    mine = {t for (sk, t) in owner}
    stray = sorted(t for t in used if t not in mine and t not in LOR_ONLY)
    print("  %d placed tiles: %d in a group, %d LORELEI's own (%s), in neither: %s"
          % (len(used), len(used & mine), len(LOR_ONLY), LOR_ONLY, stray or "none"))
    bad |= bool(stray)
    shared = sorted(t for t in used if LORELEI in SAF.use[t]["maps"] and t not in LOR_ONLY)
    print("  shared with LORELEI's house (change there too): %s" % shared)
    rows_garden = sorted({r for t in used if t not in LOR_ONLY for r in SAF.use[t]["rows"]})
    print("  rows the garden's tiles are placed in: %s (own rows %s; row 10 is LORELEI's alone, kept)"
          % (rows_garden, SAF.rows))
    if any(r not in SAF.rows for r in rows_garden):
        print("  !! a garden tile is placed in a row this tool does not own")
        bad = 1
    #  no primary tile may be placed in a row we recolour
    hits = collections.Counter()
    for l in G.LAYOUTS:
        if l.get("secondary_tileset") != SAF.sym or not G.MBL.get(l["id"]):
            continue
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        for k in range(0, len(bd) - 1, 2):
            b = struct.unpack_from("<H", bd, k)[0] & 0x3FF
            buf, bb = (G.PMT, b) if b < 640 else (SAF.mt, b - 640)
            if (bb + 1) * 16 > len(buf):
                continue
            for e in struct.unpack_from("<8H", buf, bb * 16):
                if (e & 0x3FF) < 640 and (e & 0x3FF) and (e >> 12) in SAF.rows:
                    hits[e >> 12] += 1
    if hits:
        print("  !! primary tiles placed in rows %s -- recolouring them would repaint primary art" % dict(hits))
        bad = 1
    else:
        print("  no primary tile is placed in row 8 or 9 in any map of this tileset")
    print("  scripted blocks: none (no setmetatile in these maps; no METATILE_ label names this tileset)")
    print("  the GATEKEEPER's shelf: museum %s, his alone; gbamuseum.py owns them (APPROVED A) -- a pick here needs "
          "gbamuseum to give them up first" % SHELF)
    for k, D in STYLES.items():
        sets, own = draw(D)
        n = sum(1 for (sk, t), g in own.items() if sk == "saf" and g != "lorelei" and sets["saf"][0][t] != SAF.van[t])
        print("  %s %-15s %d tiles redrawn, 0 new; rows 8, 9 recoloured; LORELEI's %d row-8 tiles re-indexed; shelf %d"
              % (k, D["title"], n, sum(1 for t in LOR_ONLY if SAF.home(t) == 8),
                 sum(1 for t in SHELF if sets["mus"][0][t] != MUS.cur[t])))
    return bad


def main():
    if WRITE:
        if "--approved" not in ARGS or not PICK or PICK not in APPROVED:
            print("  --write refused: T-540's interiors are a draft. APPROVED is %s; the user picks a direction first, "
                  "it goes into APPROVED,\n  then --write --approved --pick X writes safari_zone_building's tiles and "
                  "rows 8, 9 (never row 10, never a primary palette)." % (sorted(APPROVED) or "empty"))
            return 1
        sets, owner = draw(STYLES[PICK])
        G.save_like(os.path.join(GBA, SAF.dir, "tiles.png"), sets["saf"][0], os.path.join(GBA, SAF.dir, "tiles.png"))
        for r in SAF.rows:
            write_pal(os.path.join(GBA, SAF.dir, "palettes", "%02d.pal" % r), sets["saf"][1][r])
        print("  written: direction %s (safari_zone_building). The GATEKEEPER's shelf is gbamuseum's: not written "
              "here." % PICK)
        return 0
    bad = report()
    if DRAFT is not None:
        os.makedirs(DRAFT, exist_ok=True)
        states = collections.OrderedDict()
        states["NOW"] = None
        summary = {}
        for k, D in STYLES.items():
            sets, owner = draw(D)
            dd = os.path.join(DRAFT, k, "safari_zone_building")
            os.makedirs(os.path.join(dd, "palettes"), exist_ok=True)
            G.save_like(os.path.join(GBA, SAF.dir, "tiles.png"), sets["saf"][0], os.path.join(dd, "tiles.png"))
            for r in SAF.rows:
                write_pal(os.path.join(dd, "palettes", "%02d.pal" % r), sets["saf"][1][r])
            md = os.path.join(DRAFT, k, "museum")
            os.makedirs(md, exist_ok=True)
            G.save_like(os.path.join(GBA, MUS.dir, "tiles.png"), sets["mus"][0], os.path.join(md, "tiles.png"))
            states[k] = sets
            n = sum(1 for (sk, t), g in owner.items() if g != "lorelei" and sets["saf"][0][t] != SAF.van[t])
            summary[k] = dict(title=D["title"], tiles_redrawn=n, new_tiles=0,
                              lorelei_reindexed=[t for t in LOR_ONLY if SAF.home(t) == 8],
                              shelf=[t for t in SHELF if sets["mus"][0][t] != MUS.cur[t]],
                              rows={"safari_zone_building %d" % r: sets["saf"][1][r] for r in SAF.rows})
        json.dump(dict(ticket="T-540", part="interiors", status="DRAFT -- not in the engine",
                       approved=sorted(APPROVED), directions=summary),
                  open(os.path.join(DRAFT, "directions.json"), "w"), indent=1)
        for p in contact_sheets(DRAFT, states):
            print("  sheet:", p)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

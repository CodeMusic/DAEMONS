#!/usr/bin/env python3
"""SLATE's MUSEUM OF ERRATA, inside: the museum tileset redrawn in place in our own hand, from the story (T-541).

    python3 tools/gbamuseum.py                      # report: the census (maps, rows, the blocks the engine or a
                                                    #   script names, animation), the exhibits and what each is in
                                                    #   our world, the groups tile by tile, and every other tool's
                                                    #   claim on these tiles
    python3 tools/gbamuseum.py --draft [DIR]        # the three directions (A, B, C) drawn in full: per direction
                                                    #   museum's tiles.png and rows 8, 9, 10 as .pal, and the contact
                                                    #   sheets (gfx/drafts/t541/)
    python3 tools/gbamuseum.py --write --approved --pick X
                                                    # into the engine -- refused unless X is in APPROVED ({"A"}: the
                                                    #   user, 2026-11-10, A The slate); the report exits 1 when the
                                                    #   engine is not what that write makes (T-446's rule)

THE ANSWER IT FOLLOWS (the user, 2026-11-10, "SLATE's museum"). T-538 held the museum out of its batches as a
landmark, to be drawn T-447's way: from the story, not retinted. vision 4.32: SLATE MUSEUM OF RECORD became the
MUSEUM OF ERRATA -- an erratum is a published list of what a printed edition got wrong; a legacy mind is one that
still runs the faults it shipped with. The hardware stays, every case gains a card in a fixed form (OBJECT.
provenance. KNOWN FAULT: ...), the fault always the machine's and never the reader's, no distortion ever named,
nobody in the building corrected. Outside (gbalandmarks' ERRATA, built): a writing slate in a timber frame, wiped
clean; one line still written, struck through, a red caret where the correction goes in -- the only red; columns of
dead hardware in strata; the annex one big index card. Its chalk was scrambled so no word reads (T-447): the same
rule holds in here -- no legible word anywhere, at 1x or 3x.

ONE TILESET, FOUR ROOMS (gTileset_Museum, secondary/museum, own rows 8, 9 and 10):
  PewterCity_Museum_1F             ERRATA's hall: the two CORE cases, the ticket desk, the stairs, the wall plaques,
                                   the annex's OLD CORE on its plinth and the reading stools by the PORTs
  PewterCity_Museum_2F             KNOWN FAULTS: the REFLECTION's case, the SHUTTLE MODEL, the stairs down
  FuchsiaCity_WardensHouse         the WARDEN (LATENCY) of THE WALLED GARDEN (T-540): two cases on his rug and his
                                   desk. The left case shares the CORE cases' tiles; the right one -- "old
                                   merchandise", his own shelf -- draws eight tiles nobody else does (129..136)
  FiveIsland_ResortGorgeous_House  SELPHY's house in RESORT SUBLIME: only the hall's wall, pilasters and window
  (FuchsiaCity_House2 uses the tileset's layout but places no tile of it: nothing here reaches it.)

THE CARD AND THE WARDEN. The case card's body is in tiles 73/74, which the WARDEN's two cases draw too; its foot
(89/90) is drawn only in the museum. So the card the WARDEN's shelf shows is blank -- no rule, no stroke, nothing
that reads as writing -- and the erratum's mark (the red caret) lives on the museum-only foot. vision 4.33's rule
is honoured the same way: nothing in the ERRATA is filed under anyone. The WARDEN's merchandise is drawn with no
word on it (the text says "most of it still says SAFARI ZONE"; the picture never does).

THE RULES ARE gbahomes.py's (batch D's): redrawn IN PLACE. No block, layer, flip, palette row, behaviour or collision
bit moves and no map is touched; only pixels inside tiles change, and every tile keeps its FOOTPRINT (a transparent
pixel stays transparent, a drawn one stays drawn). Primary rows 0..6 never change colour (no primary tile is placed
in rows 8..10 in any of the four rooms: checked). Only the museum's own rows 8, 9, 10 are recoloured. No animation,
no setmetatile, no METATILE_ label names a block of it. 0 new tiles.

NOT HERE: everything primary/building places in these rooms (batch D's and gbamachines': the plants, the bookcases,
the PORTs, the mats, the bench rail 185/186, the WARDEN's walls and floor); the OLD CORE itself, which is an object
sprite (OBJ_EVENT_GFX_OLD_AMBER), not a tile; the exterior (gbalandmarks' ERRATA).

Every in-game word: none. This is art. All DRAFT.
"""
import collections, contextlib, glob, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import write_pal, read_pal
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t541")
#  The user's pick goes here ("A", "B" or "C"); --write refuses anything not in it.
APPROVED = {"A"}                     # the user, 2026-11-10: A The slate

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

MUS = G.Set("mus", "gTileset_Museum", [8, 9, 10])
SETS = {"mus": MUS}
G.SETS.update(SETS)          # Cv and render_map look sets up there
ROOMS = [("PewterCity_Museum_1F", "ERRATA 1F (the hall, the annex)"), ("PewterCity_Museum_2F", "ERRATA 2F (KNOWN FAULTS)"),
         ("FuchsiaCity_WardensHouse", "the WARDEN's house"), ("FiveIsland_ResortGorgeous_House", "SELPHY's house")]

#  ============================================================================================ the exhibits
#  vanilla's exhibit -> what it is in our world, from 4.32 and the shipped text (the cards are text, never art)
EXHIBITS = [
    ("the two fossil cases (1F, tiles 8 9 24 25 and the glass)",
     "the CORE cases: HELIX CORE and DRUM CORE, 'recovered from DEADSTACK, contents unread' -- core-memory planes, "
     "rings on a grid threaded by hand ('a CORE is wire and iron'). Both cases draw the same tiles, so both cores "
     "share one drawing; their faults are on the cards (only ever tested what it held; eight units from one drawing)"),
    ("the case cards (73 74 body, 89 90 foot)",
     "the KNOWN FAULT cards. The body is BLANK -- the WARDEN's cases draw it too, and his shelf carries no word and is "
     "filed under nothing; the museum-only foot carries the erratum's red caret, where the correction goes in"),
    ("the old amber's plinth (37 38 53 54; the amber is a sprite)",
     "the OLD CORE's plinth: 'KNOWN FAULT: none recorded' -- its card is drawn blank, which is the joke and the point "
     "(no fault recorded is not the same as none occurring)"),
    ("the moon stone case (2F, 39 40 55..59)",
     "the REFLECTION: 'a stone that fell on DEADSTACK... nobody has taken it apart. KNOWN FAULT: the label is older "
     "than any test of it' -- a dark stone with one mirror facet, and a big old luggage tag tied to it, blank"),
    ("the space shuttle (2F, 96..105 112..121 128)",
     "the SHUTTLE MODEL, scale 1:144, 'it answers every question you can think to ask it. Nobody asked it what it "
     "weighed' -- the model on its plinth with a scale bar along the front (bars, no numerals), the rope kept"),
    ("the wall plaques (1F, 65 66 81 82)",
     "errata slips: the one line still written, scrawled so no word reads, struck through, and the red caret under "
     "it -- the exterior's pediment brought inside"),
    ("the WARDEN's 'old merchandise' case (129..136, his alone)",
     "his own shelf, from THE WALLED GARDEN: a keepsake from when it was the SAFARI ZONE, with no word on it"),
]

#  ============================================================================================ drawing helpers
def ell(K, cx, cy, rx, ry, m, ring=None):
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            d = ((x - cx) / max(rx, .5)) ** 2 + ((y - cy) / max(ry, .5)) ** 2
            if d <= 1 and (ring is None or d >= ((rx - ring) / max(rx, .5)) ** 2):
                K.px(x, y, m)


def poly(K, pts, m):
    """fill a polygon (pixel centres inside)"""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    for y in range(int(min(ys)), int(max(ys)) + 1):
        for x in range(int(min(xs)), int(max(xs)) + 1):
            px, py, inside = x + .5, y + .5, False
            j = len(pts) - 1
            for i in range(len(pts)):
                (xi, yi), (xj, yj) = pts[i], pts[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            if inside:
                K.px(x, y, m)


def line(K, x0, y0, x1, y1, m):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        K.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), m)


def outline(K, inside, m="OUT"):
    """draw M around every pixel whose material is in INSIDE (4-neighbours), inside the footprint"""
    pts = [(x, y) for y in range(K.h) for x in range(K.w) if K.out[y][x] in inside]
    for x, y in pts:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            xx, yy = x + dx, y + dy
            if K.foot(xx, yy) and K.out[yy][xx] not in inside:
                K.out[yy][xx] = m


def role(K, R, default="MID"):
    """repaint by vanilla's palette index: R maps an index to a material or to f(x, y) -> material"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                m = R.get(K.vi(x, y), default)
                K.out[y][x] = m(x, y) if callable(m) else m


SHADE = {"F3": "F2", "F2": "F1", "F1": "SHD", "SHD": "OUT", "CH": "F2", "T3": "T2", "T2": "T1", "T1": "SHD",
         "W3": "W2", "W2": "W1", "W1": "SHD", "K2": "K1", "K1": "SHD", "RED": "T1", "OUT": "OUT"}


# ============================================================================================ painters
def p_floor(K, D, shade=False):
    """the hall's floor: one 16x16 period over tiles 1 2 / 17 18 (and their shaded twins 33 34 / 49 50)"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                m = D["floor"](x % 16, y % 16)
                K.out[y][x] = SHADE.get(m, m) if shade else m


def p_floor_lit(K, D):
    p_floor(K, D, False)


def p_floor_shade(K, D):
    p_floor(K, D, True)


def p_wall(K, D):
    """the wall, 8 wide and 32 tall (16, 32, 32, 48): cornice 0..4, the wall, a rail, the dado, the skirting 29..31"""
    K.fn(lambda x, y: D["wall"](x % 8, y))


def p_window(K, D):
    """the window (4, 20, 36, 52 and their mirrors): wall and cornice above, frame 6..26, sill, the wall's foot"""
    def f(x, y):
        if y < 6 or y > 26:
            return D["wall"](x % 8, y)
        return D["window"](x, y)
    K.fn(f)


def p_pillar(K, D):
    """the pilaster between the windows (83, 35, 51, 51, 67 and mirrors): cap 0..7, shaft 8..31, base 32..36,
    its foot's outline and shadow 37..39"""
    K.fn(lambda x, y: D["pillar"](x, y))


def p_plaque(K, D):
    """the wall plaque (65 66 / 81 82, with the wall around it): an erratum slip, x1..14, y13..22"""
    K.fn(lambda x, y: D["wall"](x % 8, y))
    x0, y0, x1, y1 = 1, 13, 14, 22
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            edge = x in (x0, x1) or y in (y0, y1)
            K.px(x, y, "OUT" if edge else ("T3" if y == y0 + 1 or x == x0 + 1 else
                                           "T1" if y == y1 - 1 or x == x1 - 1 else D["plaque_face"]))
    D["plaque"](K, x0 + 2, y0 + 2)


def erratum(K, x0, y0, ink, strike, caret="RED"):
    """the erratum on a 10 x 6 face at (x0, y0): a scrawl that is not writing (one unbroken wavering pen line, no
    letter shape, no gap that makes a word -- the ERRATA rule, T-447), struck straight through, and the red caret
    below and to the right, where the correction goes in. Drawn off-centre so it never reads as a face."""
    for i, dy in enumerate((2, 1, 1, 2, 3, 3, 2, 1, 2, 3)):
        K.px(x0 + i, y0 + dy, ink)
    K.hline(x0 - 1, x0 + 10, y0 + 2, strike)
    K.px(x0 + 7, y0 + 4, caret)
    K.px(x0 + 6, y0 + 5, caret)
    K.px(x0 + 8, y0 + 5, caret)


# ---- the cases: frame posts, glass, the exhibit, the card, the base
def glass(D, x, y):
    """the case's glass by canvas row: 0 the top rim, 1 its light, 2..12 the glass, 13..15 the tier's floor; 16 the
    shelf's light, 17..23 the lower front"""
    if y == 0:
        return "B1"
    if y == 1:
        return "G3"
    if y < 13:
        return "G3" if 3 <= y <= 11 and (x - y) % 23 in (0, 1) else "G2"
    if y < 16:
        return "G1" if y > 13 else "G2"
    if y == 16:
        return "G3"
    return "G2" if (x - y) % 19 in (0, 1, 2) else "G1"


def case_frame(K, D, x0, x1):
    """posts (vanilla's 1ccc6 columns), glass, base; x0..x1 the case's width on this canvas"""
    base = D["base"]
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            vv = K.vi(x, y)
            if y >= 24:                                  # the base and the card's foot
                K.out[y][x] = base(x, y - 24, vv)
            elif x - x0 <= 4 or x1 - x <= 4:              # a post
                d = x - x0 if x - x0 <= 4 else x1 - x
                K.out[y][x] = "OUT" if d == 0 or vv == 1 else ("B1" if d == 4 else "B3" if d == 1 else "B2")
            else:
                K.out[y][x] = glass(D, x, y)


def card(K, cx, museum):
    """the case card: the body (73 74) blank, the foot (89 90) with the caret only in the museum"""
    x0, x1 = cx - 7, cx + 6
    for y in range(18, 24):
        for x in range(x0, x1 + 1):
            K.px(x, y, "MID" if y == 18 or x in (x0, x1) else "WHT")
    if museum:
        K.hline(x0 + 1, x1 - 2, 24, "WHT")
        K.px(cx, 25, "RED")
        K.px(cx - 1, 25, "RED")
        K.px(cx - 2, 26, "RED")
        K.px(cx + 1, 26, "RED")


def core(K, D, x0, y0):
    """a CORE: a core-memory plane standing in the case -- a frame, a grid of wires, a ferrite ring at every crossing
    (16 x 11 box at x0, y0)"""
    fx0, fx1, fy0, fy1 = x0 + 2, x0 + 13, y0, y0 + 9
    for y in range(fy0, fy1 + 1):
        for x in range(fx0, fx1 + 1):
            if x in (fx0, fx1) or y in (fy0, fy1):
                K.px(x, y, "X1")
            elif (x - fx0) % 2 == 0 and (y - fy0) % 2 == 0:
                K.px(x, y, D["ring"])
            elif (x - fx0) % 2 == 0 or (y - fy0) % 2 == 0:
                K.px(x, y, "X3")
            else:
                K.px(x, y, "X2")
    K.hline(fx0 + 1, fx1 - 1, fy0, "X2")
    K.px(fx0 + 3, fy1 + 1, "OUT")                 # its feet
    K.px(fx1 - 3, fy1 + 1, "OUT")


def stone(K, D, x0, y0):
    """the REFLECTION: a lumpy grey stone with one flat mirror facet catching the light, and a big old tag tied to it
    on a string, lying beside it on the shelf -- blank (16 x 11 box at x0, y0)"""
    pts = [(x0 + 1, y0 + 8), (x0 + 2, y0 + 4), (x0 + 5, y0 + 2), (x0 + 9, y0 + 2), (x0 + 11, y0 + 5),
           (x0 + 11, y0 + 9), (x0 + 8, y0 + 11), (x0 + 3, y0 + 11)]
    poly(K, pts, "MID")
    poly(K, [(x0 + 3, y0 + 9), (x0 + 11, y0 + 8), (x0 + 11, y0 + 9), (x0 + 8, y0 + 11), (x0 + 3, y0 + 11)], "SHD")
    poly(K, [(x0 + 4, y0 + 4), (x0 + 8, y0 + 3), (x0 + 9, y0 + 6), (x0 + 5, y0 + 7)], "WHT")     # the facet
    K.px(x0 + 6, y0 + 4, "G3")
    outline(K, {"MID", "SHD", "WHT", "G3"}, "OUT")
    K.hline(x0 + 12, x0 + 12, y0 + 7, "X2")                     # the string
    for y in range(y0 + 7, y0 + 11):                             # the tag, older than any test of it
        for x in range(x0 + 13, x0 + 16):
            K.px(x, y, "OUT" if y == y0 + 10 else ("MID" if x == x0 + 15 else "WHT"))
    K.px(x0 + 13, y0 + 8, "X2")


def p_case1f(K, D):
    """the CORE cases (1F): [7 8 9 10 10 8 9 7h] [23 24 25 26 41 24 25 42] [71 72 73 74 75 72 91 76] [87 88 89 90 88 88 88 92]"""
    case_frame(K, D, 0, 63)
    core(K, D, 8, 5)
    core(K, D, 40, 5)
    card(K, 24, True)


def p_case2f(K, D):
    """the REFLECTION's case (2F): two tiers of [7 39 40 10 ...] [55 56 57 58 59 56 57 55h], the lower glass, the base"""
    case_frame(K, D, 0, 63)
    stone(K, D, 8, 5)
    stone(K, D, 40, 5)
    card(K, 24, True)


def p_warden1(K, D):
    """the WARDEN's left case: the CORE cases' own tiles (7 8 9 7h / 23 24 25 42 / 71 73 74 76 / 87 88 88 92)"""
    case_frame(K, D, 0, 31)
    core(K, D, 8, 5)
    card(K, 24, False)


def p_warden2(K, D):
    """the WARDEN's own shelf: 129..132 / 133..136 (his alone), the shared lower glass and base"""
    case_frame(K, D, 0, 31)
    D["keepsake"](K, D)
    card(K, 24, False)


def p_shuttle(K, D):
    """the SHUTTLE MODEL on its plinth (96..101 / 112..117 / 102 103 104 105 121 128 / 118 119 120 120h 119h 118h):
    the plinth's top and the model drawn fresh above y18; the plinth's front, the stanchions and the rope by role"""
    R = {1: "OUT", 2: "SHD", 3: "B1", 4: "B2", 5: D["plinth_front"], 6: "G1", 7: "G1", 8: "G2", 11: "MID",
         12: "WHT", 13: "WHT", 14: D["rope"][0], 15: D["rope"][1]}
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            vv = K.vi(x, y)
            post = any(c <= x <= c + 3 for c in (2, 22, 42))      # the three stanchions in front
            if y >= 24 or (y >= 21 and post):
                K.out[y][x] = R.get(vv, "MID")
            elif x == 0 or x == 47 or y <= 2 or y == 18:
                K.out[y][x] = "OUT"                      # the edges; above the plinth, repainted by the model
            elif y == 3:
                K.out[y][x] = "B3"
            elif y > 18:
                K.out[y][x] = D["plinth_front"]
            else:
                K.out[y][x] = D["plinth"](x, y)
    #  the model on its stand, climbing: tail low at the left, nose high at the right; thin, so it reads at 1x
    def thick(xa, ya, xb, yb, r, m):
        for y in range(K.h):
            for x in range(K.w):
                dx, dy = xb - xa, yb - ya
                t = max(0, min(1, ((x - xa) * dx + (y - ya) * dy) / float(dx * dx + dy * dy)))
                if (x - xa - t * dx) ** 2 + (y - ya - t * dy) ** 2 <= r * r:
                    K.px(x, y, m)
    #  its card stands at the back of the plinth, above it (the plinth's back edge, 14..25): blank, and the museum's
    #  caret at its foot
    K.rect(14, 1, 25, 7, "OUT")
    K.rect(25, 9, 26, 16, "B1")                                       # the stand
    poly(K, [(1, 0), (5, 0), (10, 11), (5, 12)], "WHT")               # the fin
    thick(6, 13, 44, 2, 1.6, "WHT")                                   # the fuselage
    K.rect(43, 0, 46, 1, "WHT")                                       # the nose, above the plinth
    poly(K, [(17, 11), (32, 7), (29, 15)], "MID")                     # the wing
    K.px(40, 3, "G1")                                                 # the cockpit
    K.px(41, 3, "G1")
    K.rect(2, 12, 4, 14, "G1")                                        # the engines
    outline(K, {"WHT", "MID", "G1"}, "OUT")
    K.rect(15, 2, 24, 6, "WHT")
    K.px(22, 5, "RED")
    K.px(21, 6, "RED")
    K.px(23, 6, "RED")
    for x in range(4, 44):                                            # the scale bar, 1:144: bars, no numerals
        K.px(x, 17, "OUT" if (x // 4) % 2 == 0 else "WHT")


def p_role(key):
    def f(K, D):
        role(K, D["roles"][key])
    f.__doc__ = "repainted by vanilla's palette index: %s" % key
    return f


# ============================================================================================ the groups
#  key, layout (as it stands), painter, what it is. Order matters: the first group to draw a tile owns it.
CASE1F = M([7, 8, 9, 10, 10, 8, 9, h(7)], [23, 24, 25, 26, 41, 24, 25, 42], [71, 72, 73, 74, 75, 72, 91, 76],
           [87, 88, 89, 90, 88, 88, 88, 92])
CASE2F = M([7, 39, 40, 10, 10, 39, 40, h(7)], [55, 56, 57, 58, 59, 56, 57, h(55)], [71, 72, 73, 74, 75, 72, 91, 76],
           [87, 88, 89, 90, 88, 88, 88, 92])
WARDEN1 = M([7, 8, 9, h(7)], [23, 24, 25, 42], [71, 73, 74, 76], [87, 88, 88, 92])
WARDEN2 = M([129, 130, 131, 132], [133, 134, 135, 136], [71, 73, 74, 76], [87, 88, 88, 92])
SHUTTLE = M([96, 97, 98, 99, 100, 101], [112, 113, 114, 115, 116, 117], [102, 103, 104, 105, 121, 128],
            [118, 119, 120, h(120), h(119), h(118)])
COUNTER = [3, 19, 64, 80, 94, 95, 110, 111, 126, 127]
STAIRS = [13, 14, 15, 29, 30, 45, 46, 47, 61, 62, 63, 68, 69, 70, 77, 78, 79, 84, 85, 86, 93,
          106, 107, 108, 109, 122, 123, 124, 125]
GROUPS = [
    ("floor",    M([1, 2], [17, 18]),                                 p_floor_lit,   "the hall's floor"),
    ("shade",    M([33, 34], [49, 50]),                               p_floor_shade, "the floor in a wall's or a case's shade"),
    ("wall",     M([16], [32], [32], [48]),                           p_wall,        "the wall (museum and SELPHY's)"),
    ("window",   M([4, h(4)], [20, h(20)], [36, h(36)], [52, h(52)]), p_window,      "a window (museum and SELPHY's)"),
    ("pillar",   M([83, h(83)], [35, h(35)], [51, h(51)], [51, h(51)], [67, h(67)]), p_pillar,
     "the pilaster between the windows (museum and SELPHY's)"),
    ("plaque",   M([16, 16], [65, 66], [81, 82], [48, 48]),           p_plaque,      "the wall plaques: errata slips (1F)"),
    ("cores",    CASE1F,                                              p_case1f,      "the CORE cases, their cards and bases"),
    ("reflection", CASE2F,                                            p_case2f,      "the REFLECTION's case (2F)"),
    ("warden1",  WARDEN1,                                             p_warden1,     "the WARDEN's left case (the CORE cases' tiles)"),
    ("warden2",  WARDEN2,                                             p_warden2,     "the WARDEN's own shelf (his alone)"),
    ("shuttle",  SHUTTLE,                                             p_shuttle,     "the SHUTTLE MODEL (2F)"),
    ("plinth",   M([37, 38], [53, 54]),                               p_role("plinth"), "the OLD CORE's plinth and its blank card"),
    ("stools",   M([5, 6], [21, 22]),                                 p_role("stool"), "the reading stools by the PORTs"),
] + [("counter_%d" % t, M([t]), p_role("counter"), "the desk (ticket desk, 2F bar, the WARDEN's desk)") for t in COUNTER] \
  + [("stair_%d" % t, M([t]), p_role("stair"), "the stairs and their rails") for t in STAIRS]

ROWMATS = {
    8:  ["OUT", "SHD", "MID", "HI", "WHT", "S1", "S2", "S3", "R1", "R2", "R3", "T1", "T2", "T3", "FL"],
    9:  ["OUT", "SHD", "F1", "F2", "F3", "W1", "W2", "W3", "T1", "T2", "T3", "K1", "K2", "CH", "RED"],
    10: ["OUT", "SHD", "MID", "WHT", "G1", "G2", "G3", "B1", "B2", "B3", "X1", "X2", "X3", "GRN", "RED"],
}


# ============================================================================================ resolving
def mats_for(D):
    return dict(D["mat"])


def set_palettes(D):
    mat = mats_for(D)
    out = {}
    for r in range(16):
        if r in MUS.rows:
            out[r] = [MUS.vpal[r][0]] + [mat[m] for m in ROWMATS[r]]
        else:
            out[r] = list(read_pal(os.path.join(GBA, MUS.dir, "palettes/%02d.pal" % r)))
    return out


def draw(D):
    """-> {"mus": (tiles, palettes)}, owner {t: group}"""
    tiles = [t[:] for t in MUS.cur]
    pals = set_palettes(D)
    owner = {}
    mat = mats_for(D)
    Dm = {"mat": mat, "_index": {(r, m): i + 1 for r in MUS.rows for i, m in enumerate(ROWMATS[r])}}
    own = {r: pals[r] for r in MUS.rows}
    for key, layout, painter, what in GROUPS:
        K = Cv(layout, "mus")
        painter(K, D)
        for t, mm in K.tiles().items():
            if t in owner or t >= MUS.nvan or t not in MUS.use:
                continue
            tiles[t] = G.resolve(mm, MUS.van[t], dict(MUS.use[t]["rows"]), Dm, own)
            owner[t] = key
    return {"mus": (tiles, pals)}, owner


# ============================================================================================ the directions
def hsh(x, y, s=0):
    return H(x, y, s)


# ---------------------------------------------------------------------------------------- A THE SLATE
def A_floor(x, y):
    """pale SLATE flagstones, 16 x 8 in running bond: the city's own stone underfoot"""
    jx = 0 if y < 8 else 8
    if y % 8 == 0 or x == jx:
        return "F1"
    if y % 8 == 1 or x == (jx + 1) % 16:
        return "F3"
    return "F1" if hsh(x // 2, y // 2, 3) % 13 == 0 else "F2"


def A_wall(x, y):
    """the hall is the slate itself, in its timber frame: an oak cornice, the slate ruled in chalk and wiped clean,
    an oak rail, oak boarding below"""
    if y == 0 or y == 4:
        return "OUT"
    if y < 4:
        return ("T3", "T2", "T1")[y - 1]
    if y < 20:
        if y in (9, 14):
            return "W3"                                   # chalk ruling, faint
        return "W1" if y == 5 else "W2"
    if y == 20:
        return "T3"
    if y == 21:
        return "T1"
    if y < 29:
        return "T1" if x == 0 else ("T3" if x == 1 else "T2")
    return "OUT" if y == 29 else "SHD"


def A_window(x, y):
    """a timber sash: two lights over two, the sky, SLATE's roofs in the lowest pane"""
    xx = x if x < 8 else 15 - x
    if y == 6:
        return "OUT"
    if y == 7:
        return "T3"
    if y == 24:
        return "OUT"
    if y == 25:
        return "T3"
    if y == 26:
        return "T1"
    if xx == 0:
        return "OUT"
    if xx == 1:
        return "T2"
    if xx == 2 or xx == 7 or y in (12, 20):
        return "B1"
    if y > 20:
        return "SHD" if y > 22 or (xx in (3, 4) and y == 22) else "MID"
    if y < 12:
        return "G3"
    return "G3" if (xx + y) % 9 == 0 else "G2"


def A_pillar(x, y):
    """an oak frame member between the slates: a capital, the post with a chamfer, a plinth"""
    if y >= 37:
        return "OUT" if y == 37 else "SHD"
    if x in (0, 15) or y in (0, 7, 32):
        return "OUT"
    if y < 7:
        return "T3" if y < 3 else ("T2" if y < 6 else "T1")
    if y > 32:
        return "T2" if y < 36 else "T1"
    if x in (3, 4):
        return "T1" if x == 4 else "T3"                   # the chamfer
    if x in (11, 12):
        return "T1" if x == 11 else "T3"
    if x in (1, 14):
        return "T3" if x == 1 else "T1"
    return "T1" if (x * 3 + y // 5) % 7 == 0 else "T2"


def A_plaque(K, x0, y0):
    erratum(K, x0, y0, "CH", "CH")


def A_base(x, y, vv):
    """the case's plinth: oak with a grain, its card's foot above it"""
    if vv == 1:
        return "OUT"
    if vv in (12, 11):
        return "WHT" if vv == 12 else "MID"
    if vv == 2:
        return "SHD"
    if vv == 3:
        return "B1"
    if vv == 4:
        return "B2"
    return "B1" if (x + 3 * y) % 11 == 0 else "B3"


def A_keepsake(K, D):
    """the WARDEN's keepsake: a snow globe of the garden from when it was the SAFARI ZONE -- a ring of wall, a lawn,
    one tree, under glass on an oak foot. No word on it."""
    cx, cy = 15.5, 10.5
    ell(K, cx, cy, 5.5, 5.0, "OUT")
    ell(K, cx, cy, 4.5, 4.0, "G3")
    ell(K, cx, cy + 1.6, 3.6, 1.6, "GRN")
    ell(K, cx, cy + 1.6, 3.6, 1.6, "MID", ring=0.9)                  # the wall, all the way round
    K.rect(15, 8, 16, 11, "B1")                                       # the tree
    ell(K, cx, cy - 2.5, 2.0, 1.5, "GRN")
    K.px(12, 8, "WHT")                                                # the glass's light
    K.rect(10, 15, 21, 15, "B2")
    K.rect(11, 14, 20, 14, "B3")


A = dict(
    name="A", title="THE SLATE",
    lines=["The exterior carried in: the hall is a writing slate in its oak frame, ruled in chalk and wiped clean,",
           "on pale SLATE flags. Oak vitrines; the CORES copper planes of wire and rings; the REFLECTION a dark stone with",
           "a mirror facet and a blank tag; the SHUTTLE on an oak plinth with a scale bar. Red only for the errata: the",
           "caret on each card's foot and on the struck slips. The WARDEN's shelf: a snow globe of the walled garden."],
    mat=dict(OUT=(30, 32, 42), SHD=(56, 62, 74), MID=(122, 130, 142), HI=(186, 192, 200), WHT=(240, 240, 230),
             F1=(126, 132, 142), F2=(158, 164, 172), F3=(188, 192, 198),
             W1=(40, 48, 60), W2=(60, 70, 84), W3=(96, 108, 122),
             T1=(92, 62, 42), T2=(138, 96, 60), T3=(184, 138, 90),
             K1=(150, 112, 48), K2=(212, 172, 92), CH=(236, 236, 226), RED=(204, 40, 44),
             G1=(84, 124, 146), G2=(150, 188, 200), G3=(212, 232, 236),
             B1=(92, 62, 42), B2=(138, 96, 60), B3=(184, 138, 90),
             X1=(112, 58, 30), X2=(186, 106, 56), X3=(232, 172, 110), GRN=(84, 136, 76),
             S1=(46, 54, 66), S2=(62, 72, 86), S3=(104, 116, 130), R1=(92, 62, 42), R2=(138, 96, 60),
             R3=(184, 138, 90), FL=(158, 164, 172)),
    floor=A_floor, wall=A_wall, window=A_window, pillar=A_pillar, plaque_face="W2", plaque=A_plaque, base=A_base,
    ring="OUT", keepsake=A_keepsake, plinth=lambda x, y: "B3" if y == 4 else ("B1" if (x + 2 * y) % 13 == 0 else "B2"),
    plinth_front="B2", rope=("X1", "X2"),
    roles=dict(
        counter={1: "OUT", 2: "SHD", 3: "T1", 4: "T3", 12: "SHD", 13: "F1", 10: "CH", 8: "W2", 9: "W3",
                 5: lambda x, y: "T2" if (y + hsh(0, x // 8, 7)) % 4 == 0 else "T3"},
        plinth={1: "OUT", 2: "SHD", 3: "T1", 4: "T3", 5: "W2", 10: "CH", 12: "F1", 13: "F2"},
        stool={1: "OUT", 2: "SHD", 3: "B1", 4: "B2", 5: "B3", 14: "B2", 15: "GRN"},
        stair={1: "OUT", 2: "MID", 3: "S1", 4: "S2", 5: "S2", 6: "S3", 7: "MID", 8: "R2", 9: "R3", 10: "SHD",
               11: "FL"}),
)


# ---------------------------------------------------------------------------------------- B THE INDEX
def B_floor(x, y):
    """graph-paper linoleum in the card's buff: a faint grid every 8, a blue one every 16"""
    if x == 0 or y == 0:
        return "F1"
    if x == 8 or y == 8:
        return "F2"
    return "F3"


def B_wall(x, y):
    """the annex's card turned inside: card stock with faint blue rules and the red header rule round the room, a
    steel cornice, and the card catalogue's drawers for a dado -- each label holder empty"""
    if y == 0 or y == 4:
        return "OUT"
    if y < 4:
        return ("T3", "T2", "T1")[y - 1]
    if y < 20:
        if y == 7:
            return "RED"
        return "W1" if y in (11, 15, 19) else "W3"
    if y == 20 or y == 28:
        return "T1"
    if y < 28:
        if x == 7:
            return "T1"
        if 22 <= y <= 23 and 2 <= x <= 5:
            return "CH"                                   # the label holder, empty
        if y == 25 and x in (3, 4):
            return "K2"                                   # the pull
        return "T3" if y == 21 else "T2"
    return "OUT" if y == 29 else "SHD"


def B_window(x, y):
    """a steel casement: one tall light with a single transom, white sky"""
    xx = x if x < 8 else 15 - x
    if y in (6, 24):
        return "OUT"
    if y == 7 or y == 25:
        return "T3"
    if y == 26:
        return "T1"
    if xx == 0:
        return "OUT"
    if xx == 1:
        return "T2"
    if xx == 2 or y == 16:
        return "MID"
    if xx == 7:
        return "MID" if y > 16 else "G3"
    if y > 20:
        return "G1"
    return "G3" if y < 12 or (xx - y) % 7 == 0 else "G2"


def B_pillar(x, y):
    """a card-catalogue cabinet between the windows: steel, a column of small drawers, each with an empty label
    holder and a brass pull"""
    if y >= 37:
        return "OUT" if y == 37 else "SHD"
    if x in (0, 15) or y in (0, 32):
        return "OUT"
    if y < 7:
        return "T3" if y < 3 else "T2"
    if y == 7:
        return "T1"
    if y > 32:
        return "T1"
    if x == 1:
        return "T3"
    if x == 14:
        return "T1"
    yy = (y - 8) % 6
    if yy == 5:
        return "T1"
    if yy in (1, 2) and 5 <= x <= 10:
        return "CH" if yy == 1 or x in (5, 10) else "W3"
    if yy == 3 and x in (7, 8):
        return "K2"
    return "T3" if yy == 0 else "T2"


def B_plaque(K, x0, y0):
    erratum(K, x0, y0, "T1", "OUT")


def B_base(x, y, vv):
    """the case's plinth: steel, a seam, a kick plate"""
    if vv == 1:
        return "OUT"
    if vv in (12, 11):
        return "WHT" if vv == 12 else "MID"
    if vv == 2:
        return "SHD"
    if vv == 3:
        return "B1"
    if vv == 4:
        return "B2"
    return "B2" if y == 5 else "B3"


def B_keepsake(K, D):
    """the WARDEN's keepsake: a pennant from the old gate on a little stand, and the gate's arch in miniature. Its
    stripe and its arch, no word."""
    K.vline(9, 6, 15, "B1")                                           # the stick
    poly(K, [(10, 6), (19, 8), (10, 11)], "GRN")                      # the pennant
    K.hline(10, 15, 8, "WHT")
    outline(K, {"GRN", "WHT"}, "OUT")
    K.rect(7, 15, 11, 15, "B1")
    for y in range(7, 16):                                            # the gate's arch
        for x in range(20, 27):
            d = ((x - 23) / 3.6) ** 2 + ((y - 11) / 4.6) ** 2
            if y >= 11 and x in (20, 21, 25, 26) or (y < 11 and 0.45 < d <= 1):
                K.px(x, y, "MID")
    K.hline(19, 27, 15, "SHD")


B = dict(
    name="B", title="THE INDEX",
    lines=["The annex's index card turned inside: walls of card stock with faint blue rules and the red header rule",
           "round the room, a dado of card-catalogue drawers with empty label holders, graph-paper linoleum, steel",
           "cabinets for pilasters. Steel vitrines; the CORES and the REFLECTION as in A; the SHUTTLE on a steel plinth",
           "ruled like graph paper. The WARDEN's shelf: a pennant from the old gate and the gate's arch in miniature."],
    mat=dict(OUT=(40, 44, 60), SHD=(98, 102, 118), MID=(152, 158, 172), HI=(206, 210, 218), WHT=(250, 248, 240),
             F1=(146, 168, 200), F2=(208, 200, 176), F3=(230, 224, 204),
             W1=(184, 202, 226), W2=(226, 220, 198), W3=(246, 242, 228),
             T1=(80, 88, 104), T2=(132, 140, 154), T3=(182, 190, 202),
             K1=(150, 120, 60), K2=(206, 170, 96), CH=(252, 252, 246), RED=(200, 40, 48),
             G1=(102, 142, 172), G2=(172, 206, 226), G3=(228, 242, 248),
             B1=(80, 88, 104), B2=(132, 140, 154), B3=(182, 190, 202),
             X1=(112, 62, 34), X2=(186, 110, 60), X3=(232, 172, 112), GRN=(70, 128, 90),
             S1=(56, 60, 72), S2=(86, 92, 106), S3=(126, 132, 146), R1=(80, 88, 104), R2=(132, 140, 154),
             R3=(182, 190, 202), FL=(208, 200, 176)),
    floor=B_floor, wall=B_wall, window=B_window, pillar=B_pillar, plaque_face="CH", plaque=B_plaque, base=B_base,
    ring="OUT", keepsake=B_keepsake, plinth=lambda x, y: "B3" if y == 4 else ("B1" if x % 8 == 0 or y % 8 == 0 else "B2"),
    plinth_front="B3", rope=("B1", "B2"),
    roles=dict(
        counter={1: "OUT", 2: "SHD", 3: "T1", 4: "T3", 12: "SHD", 13: "F1", 10: "CH", 8: "W2", 9: "W3",
                 5: lambda x, y: "T3" if y % 4 == 0 else "T2"},
        plinth={1: "OUT", 2: "SHD", 3: "T1", 4: "T3", 5: "T2", 10: "CH", 12: "F1", 13: "F2"},
        stool={1: "OUT", 2: "SHD", 3: "B1", 4: "B2", 5: "B3", 14: "SHD", 15: "MID"},
        stair={1: "OUT", 2: "MID", 3: "S1", 4: "S2", 5: "S2", 6: "S3", 7: "MID", 8: "R2", 9: "R3", 10: "SHD",
               11: "FL"}),
)


# ---------------------------------------------------------------------------------------- C THE STRATA
def C_floor(x, y):
    """a terrazzo of dead hardware: warm grey, chips of board and gold pin in it, brass strips every 16"""
    if x == 0 or y == 0:
        return "T2"
    k = hsh(x, y, 11) % 53
    if k == 0:
        return "K1"
    if k == 1:
        return "K2"
    if k in (2, 3):
        return "F1"
    if k in (4, 5):
        return "F3"
    return "F2"


def C_wall(x, y):
    """the hall cut through strata, like the exterior's columns: sand, ochre, a band of fossil chips, umber"""
    if y == 0 or y == 4:
        return "OUT"
    if y < 4:
        return ("T3", "T2", "T1")[y - 1]
    if y < 9:
        return "W3"
    if y < 12:
        return "W2"
    if y < 16:                                            # the fossil bed: a chip in every span
        if 1 <= x <= 5 and y in (13, 14):
            return "SHD"
        if x in (1, 3, 5) and y in (12, 15):
            return "K2"
        return "W1"
    if y < 20:
        return "W2"
    if y == 20:
        return "T1"
    if y < 29:
        b = 24 + (1 if x in (2, 3, 4) else 0)
        return "W3" if y < b else ("W1" if y == b else "W2")
    return "OUT" if y == 29 else "SHD"


def C_window(x, y):
    """a stone mullion and transom, the lights small and deep"""
    xx = x if x < 8 else 15 - x
    if y in (6, 24):
        return "OUT"
    if y == 7 or y == 25:
        return "T3"
    if y == 26:
        return "T1"
    if xx == 0:
        return "OUT"
    if xx in (1, 2):
        return "T2" if xx == 1 else "T1"
    if xx == 7 or y in (15, 16):
        return "T2"
    if y > 20:
        return "G1"
    return "G3" if y < 10 else "G2"


def C_pillar(x, y):
    """a column of dead hardware stacked in strata, as outside: a beige case, a cartridge, a drive, a keyboard, a chip,
    on a stone cap and base"""
    if y >= 37:
        return "OUT" if y == 37 else "SHD"
    if x in (0, 15) or y in (0, 7, 32):
        return "OUT"
    if y < 7:
        return "T3" if y < 3 else "T2"
    if y > 32:
        return "T2" if y < 36 else "T1"
    if x in (1, 14):
        return "T1"
    if y < 14:                                            # a beige case with its vents
        return "SHD" if y in (10, 12) and 3 <= x <= 12 else ("T1" if y == 13 else "CH")
    if y < 18:                                            # a cartridge, its label blank
        return "W3" if 5 <= x <= 10 and y in (15, 16) else ("OUT" if y == 17 else "SHD")
    if y < 23:                                            # a drive and its slot
        return "OUT" if y == 20 and 4 <= x <= 11 else ("T1" if y == 22 else "T3")
    if y < 28:                                            # a keyboard, key by key
        return "T1" if (x % 2 == 1 and y in (24, 26)) else ("SHD" if y == 27 else "CH")
    return "K2" if y in (28, 31) and x % 2 == 0 else "K1"     # a chip, its pins


def C_plaque(K, x0, y0):
    erratum(K, x0, y0, "T1", "SHD")


def C_base(x, y, vv):
    """the case's plinth: one block of stone"""
    if vv == 1:
        return "OUT"
    if vv in (12, 11):
        return "WHT" if vv == 12 else "MID"
    if vv == 2:
        return "SHD"
    if vv == 3:
        return "B1"
    if vv == 4:
        return "B2"
    return "B2" if hsh(x, y, 5) % 9 == 0 else "B3"


def C_keepsake(K, D):
    """the WARDEN's own shelf: a velvet cushion with tassels and an empty dent the shape of his TOKEN, the key he keeps
    losing. Nothing on it."""
    K.rect(7, 10, 24, 15, "GRN")
    K.hline(8, 23, 10, "X3")
    for x, y in ((7, 10), (24, 10), (7, 15), (24, 15)):
        K.px(x, y, "B3")                                              # the tassels
    outline(K, {"GRN", "X3", "B3"}, "OUT")
    ell(K, 11.0, 12.5, 1.6, 1.6, "SHD", ring=0.8)                     # the dent: the bow
    K.hline(13, 20, 12, "SHD")                                        # the shaft
    K.px(18, 13, "SHD")                                               # the bit
    K.px(20, 13, "SHD")


C = dict(
    name="C", title="THE STRATA",
    lines=["Dead hardware in strata, as the exterior's columns: walls cut through sand, ochre and umber with a bed of",
           "fossil chips, a terrazzo floor with board and gold pin in it, pilasters of stacked cases, cartridges, drives",
           "and keyboards. Stone plinths; the CORES gone to verdigris; the SHUTTLE on a stone slab. The WARDEN's shelf:",
           "a velvet cushion with an empty dent the shape of his TOKEN, the key he keeps losing."],
    mat=dict(OUT=(40, 34, 30), SHD=(84, 74, 64), MID=(142, 130, 114), HI=(198, 188, 168), WHT=(240, 234, 216),
             F1=(112, 106, 98), F2=(158, 152, 142), F3=(198, 192, 180),
             W1=(124, 96, 68), W2=(172, 138, 94), W3=(212, 184, 136),
             T1=(92, 92, 98), T2=(130, 130, 136), T3=(172, 172, 174),
             K1=(62, 112, 72), K2=(216, 178, 86), CH=(226, 218, 196), RED=(204, 40, 44),
             G1=(90, 128, 128), G2=(150, 186, 180), G3=(210, 228, 220),
             B1=(92, 86, 82), B2=(134, 126, 118), B3=(178, 170, 158),
             X1=(56, 96, 86), X2=(98, 148, 128), X3=(178, 208, 188), GRN=(72, 120, 70),
             S1=(112, 102, 90), S2=(152, 142, 126), S3=(192, 182, 162), R1=(62, 58, 58), R2=(102, 98, 98),
             R3=(152, 148, 142), FL=(158, 152, 142)),
    floor=C_floor, wall=C_wall, window=C_window, pillar=C_pillar, plaque_face="T3", plaque=C_plaque, base=C_base,
    ring="OUT", keepsake=C_keepsake, plinth=lambda x, y: "B3" if y == 4 else ("B2" if hsh(x, y, 9) % 11 == 0 else "MID"),
    plinth_front="B2", rope=("R1", "MID"),
    roles=dict(
        counter={1: "OUT", 2: "SHD", 3: "T1", 4: "T3", 12: "SHD", 13: "F1", 10: "CH", 8: "W2", 9: "W3",
                 5: lambda x, y: "F3" if hsh(x, y, 13) % 9 == 0 else "T3"},
        plinth={1: "OUT", 2: "SHD", 3: "T1", 4: "T2", 5: "T3", 10: "CH", 12: "F1", 13: "F2"},
        stool={1: "OUT", 2: "SHD", 3: "B1", 4: "B2", 5: "B3", 14: "X1", 15: "X2"},
        stair={1: "OUT", 2: "MID", 3: "S1", 4: "S2", 5: "S2", 6: "S3", 7: "MID", 8: "R2", 9: "R3", 10: "SHD",
               11: "FL"}),
)

#  C's CORES have gone to verdigris (its X row is green copper); A and B keep bright copper.
STYLES = {"A": A, "B": B, "C": C}
for _D in STYLES.values():
    for _r, _ms in ROWMATS.items():
        for _m in _ms:
            assert _m in _D["mat"], (_D["name"], _m)


# ============================================================================================ sheets
BG, INK, RED, SOFT = (250, 248, 242), (24, 24, 24), (120, 20, 30), (90, 90, 90)
DETAILS = [("PewterCity_Museum_1F", (2, 0, 8, 6), "a CORE case, its card and caret; a pilaster and window"),
           ("PewterCity_Museum_1F", (10, 0, 18, 4), "the errata slips on the wall, the ticket desk"),
           ("PewterCity_Museum_1F", (20, 1, 28, 6), "the annex: the OLD CORE's plinth (blank card), the stools"),
           ("PewterCity_Museum_2F", (1, 3, 7, 9), "the REFLECTION, its blank tag"),
           ("PewterCity_Museum_2F", (13, 3, 18, 7), "the SHUTTLE MODEL and its scale bar"),
           ("FuchsiaCity_WardensHouse", (3, 2, 13, 7), "the WARDEN's cases (blank cards) and desk")]


def text(d, xy, s, fill=INK):
    d.text(xy, s, fill=fill)


def room(m, sets, crop=None):
    im = G.render_map(m, (sets, None) if sets else None)
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
    return im


def contact_sheets(out_dir, states):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: Nintendo's museum (the plants, bookcases, PORTs, mats and the WARDEN's walls",
                              "and floor are primary/building's -- batch D's and gbamachines', already ours)"])}
    for k in STYLES:
        titles[k] = ("%s %s" % (k, STYLES[k]["title"]), STYLES[k]["lines"])
    pad = 10
    paths = []
    blocks = []
    for k in names:
        ims = [room(m, states[k]) for m, _ in ROOMS]
        t, lines = titles[k]
        th = 8 + 12 * len(lines) + 16
        W = sum(i.width for i in ims) + pad * (len(ims) + 1)
        im = Image.new("RGB", (max(W, 900), th + max(i.height for i in ims) + pad), BG)
        d = ImageDraw.Draw(im)
        text(d, (pad, 6), t, RED)
        for j, s in enumerate(lines):
            text(d, (pad + 120, 6 + 12 * j), s)
        x = pad
        for i, (m, cap) in zip(ims, ROOMS):
            text(d, (x, th - 13), cap, SOFT)
            im.paste(i, (x, th))
            x += i.width + pad
        blocks.append(im)
    W = max(b.width for b in blocks)
    sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 8), "T-541 DRAFT -- SLATE's MUSEUM OF ERRATA inside, real rooms at 1x: three directions beside today's "
                      "(redrawn in place: no block, collision or palette row moves; rows 8, 9, 10 only).", INK)
    y = 30
    for b in blocks:
        sh.paste(b, (0, y))
        y += b.height
    p = os.path.join(out_dir, "t541_rooms_1x.png")
    sh.save(p)
    paths.append(p)
    #  3x details, two pages
    rowsim = []
    for k in names:
        crops = []
        for m, cr, cap in DETAILS:
            im = room(m, states[k], cr)
            crops.append((im.resize((im.width * 3, im.height * 3), Image.NEAREST), cap))
        rowsim.append((k, crops))
    for pi, part in enumerate(((0, 1, 2), (3, 4, 5))):
        cw = sum(rowsim[0][1][i][0].width for i in part) + pad * 4 + 120
        ch = max(rowsim[0][1][i][0].height for i in part) + 24
        det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
        d = ImageDraw.Draw(det)
        text(d, (pad, 8), "T-541 DRAFT -- details at 3x: %s." % "; ".join(DETAILS[i][2] for i in part), INK)
        y = 30
        for k, crops in rowsim:
            text(d, (pad, y + 6), titles[k][0], RED)
            x = 120
            for i in part:
                c, cap = crops[i]
                text(d, (x, y + 2), cap, SOFT)
                det.paste(c, (x, y + 16))
                x += c.width + pad
            y += ch
        p = os.path.join(out_dir, "t541_detail_3x_%d.png" % (pi + 1))
        det.save(p)
        paths.append(p)
    #  the tiles at 3x, each in its home row, per state
    cols = []
    for k in names:
        tiles, pals = states[k]["mus"] if states[k] else (MUS.cur, {r: read_pal(os.path.join(GBA, MUS.dir,
                                                                                            "palettes/%02d.pal" % r))
                                                                    for r in range(16)})
        n = (MUS.nvan + 15) // 16
        im = Image.new("RGB", (128, n * 8), (236, 236, 236))
        o = im.load()
        for t in range(MUS.nvan):
            if t not in MUS.use:
                continue
            r = MUS.home(t)
            pal = pals[r]
            for q in range(64):
                vv = tiles[t][q]
                o[(t % 16) * 8 + q % 8, (t // 16) * 8 + q // 8] = pal[vv] if vv else (200, 200, 200)
        cols.append((titles[k][0], im.resize((384, im.height * 3), Image.NEAREST)))
    W = sum(c.width + pad for _, c in cols) + pad
    sh = Image.new("RGB", (W, max(c.height for _, c in cols) + 50), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 6), "T-541 DRAFT -- museum's tiles at 3x, each in its home row (grey: transparent; light grey cells: "
                      "unplaced, left as they are)", INK)
    x = pad
    for t, c in cols:
        text(d, (x, 26), t, RED)
        sh.paste(c, (x, 42))
        x += c.width + pad
    p = os.path.join(out_dir, "t541_tiles_3x.png")
    sh.save(p)
    paths.append(p)
    return paths


# ============================================================================================ report
def other_claims():
    """every other tool that names the museum's tiles or rows: none may write them"""
    out = []
    me = os.path.basename(__file__)
    for f in sorted(glob.glob(os.path.join(ROOT, "tools", "*.py"))):
        if os.path.basename(f) == me:
            continue
        src = open(f, encoding="utf-8", errors="ignore").read()
        if "secondary/museum" in src or re.search(r"Set\([^)]*gTileset_Museum", src):
            out.append(os.path.basename(f))
    return out


def report():
    print("T-541 -- SLATE's MUSEUM OF ERRATA inside (gTileset_Museum, %s)\n" % MUS.dir)
    c = G.census_set(MUS.sym)
    print("  census: %d placed tiles, %d still Nintendo's drawing; rows %s (all three the museum's own); animation %s"
          % (c["used"], c["vanilla"], c["rows"], c["anim"] or "none"))
    for m in c["maps"]:
        ts = sorted(t for t in MUS.use if m in MUS.use[t]["maps"] and t < MUS.nvan)
        print("    %-34s %3d of its tiles%s" % (m, len(ts), "" if ts else " -- places none: nothing here reaches it"))
    labels = re.findall(r"#define (METATILE_Museum\w*)", open(os.path.join(GBA, "include/constants/metatile_labels.h")).read())
    sm = []
    for m in c["maps"]:
        f = os.path.join(GBA, "data/maps", m, "scripts.inc")
        if os.path.exists(f) and "setmetatile" in open(f).read():
            sm.append(m)
    print("  blocks a script or the engine names: %s; setmetatile in: %s" % (labels or "none", sm or "none"))
    print("\n  the exhibits, and what each is in our world (4.32; the cards are text, never art):")
    for van, ours in EXHIBITS:
        print("    %s\n      -> %s" % (van, ours))
    owner = {}
    for key, layout, painter, what in GROUPS:
        for r in layout:
            for s in r:
                if s is not None:
                    owner.setdefault(s if isinstance(s, int) else s[0], key)
    print("\n  %-12s %5s %6s  %s" % ("group", "tiles", "draws", "what"))
    seen = set()
    for key, layout, painter, what in GROUPS:
        k2 = key.split("_")[0] if key.startswith(("counter_", "stair_")) else key
        if k2 in seen:
            continue
        seen.add(k2)
        ts = sorted(t for t, k in owner.items() if (k == key or k.split("_")[0] == k2 and "_" in k) and t in MUS.use
                    and t < MUS.nvan)
        print("  %-12s %5d %6d  %s" % (k2, len(ts), sum(MUS.use[t]["n"] for t in ts), what))
    bad = 0
    used = {t for t in MUS.use if t < MUS.nvan and any(MUS.cur[t])}
    stray = sorted(t for t in used if t not in owner)
    rows = sorted({r for t in used for r in MUS.use[t]["rows"]})
    foreign = [r for r in rows if r not in MUS.rows]
    print("\n  %d placed tiles, %d in a group; in no group: %s; rows placed %s%s"
          % (len(used), len(used & set(owner)), stray or "none", rows,
             ("; !! placed in a row this tool does not own: %s" % foreign) if foreign else ""))
    bad |= bool(stray) or bool(foreign)
    #  rows a primary tile is placed in, inside these rooms: none may be one we recolour
    hits = collections.Counter()
    for l in G.LAYOUTS:
        if l.get("secondary_tileset") != MUS.sym or not G.MBL.get(l["id"]):
            continue
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        for k in range(0, len(bd) - 1, 2):
            m = struct.unpack_from("<H", bd, k)[0] & 0x3FF
            buf, mm = (G.PMT, m) if m < 640 else (MUS.mt, m - 640)
            if (mm + 1) * 16 > len(buf):
                continue
            for e in struct.unpack_from("<8H", buf, mm * 16):
                if (e & 0x3FF) < 640 and (e & 0x3FF) and (e >> 12) in MUS.rows:
                    hits[e >> 12] += 1
    if hits:
        print("  !! primary tiles placed in the museum's own rows %s -- recolouring them would repaint primary art"
              % dict(hits))
        bad = 1
    else:
        print("  no primary tile is placed in rows 8, 9 or 10 in any of the five maps")
    #  the WARDEN's shelf: his tiles carry no card mark, and the card's body is blank in every direction
    print("  the WARDEN's cases draw tiles %s; of those only 129..136 are his alone; the card body (73 74) is blank"
          % sorted({s if isinstance(s, int) else s[0] for r in WARDEN1 + WARDEN2 for s in r}))
    others = other_claims()
    print("  other tools naming secondary/museum: %s" % (others or "none -- no tool but this one writes these tiles or "
                                                                    "rows (gbahomes lists it as a landmark, 'L', and "
                                                                    "never draws it)"))
    bad |= bool(others)
    if not APPROVED:
        vt = sum(1 for t in range(MUS.nvan) if MUS.cur[t] != MUS.van[t])
        vr = [r for r in MUS.rows
              if [tuple(x) for x in read_pal(os.path.join(GBA, MUS.dir, "palettes/%02d.pal" % r))]
              != [tuple(x) for x in MUS.vpal[r]]]
        print("  the engine's museum today: %d tiles and rows %s differ from vanilla (nothing has written it yet)"
              % (vt, vr or "none"))
    return bad


def check_engine():
    """T-446's rule: with one direction approved, the engine must be exactly what `--write --approved --pick X` makes"""
    pick = next(iter(APPROVED))
    sets, _ = draw(STYLES[pick])
    tiles, pals = sets["mus"]
    off = [t for t in range(len(MUS.cur)) if tiles[t] != MUS.cur[t]]
    rows = [r for r in MUS.rows if [tuple(c) for c in pals[r]]
            != [tuple(c) for c in read_pal(os.path.join(GBA, MUS.dir, "palettes/%02d.pal" % r))]]
    if off or rows:
        print("  !! museum: the engine differs from `--write --approved --pick %s` in tiles %s rows %s -- find which "
              "side is right" % (pick, off[:12], rows))
        return 1
    print("  the engine matches `--write --approved --pick %s`" % pick)
    return 0


def main():
    if WRITE:
        if "--approved" not in ARGS or not PICK or PICK not in APPROVED:
            print("  --write refused: T-541 is a draft. APPROVED is %s; the user picks a direction first, it goes into "
                  "APPROVED,\n  then --write --approved --pick X writes museum's tiles.png and rows 8, 9, 10 (never a "
                  "primary palette)." % (sorted(APPROVED) or "empty"))
            return 1
        sets, owner = draw(STYLES[PICK])
        tiles, pals = sets["mus"]
        G.save_like(os.path.join(GBA, MUS.dir, "tiles.png"), tiles, os.path.join(GBA, MUS.dir, "tiles.png"))
        for r in MUS.rows:
            write_pal(os.path.join(GBA, MUS.dir, "palettes", "%02d.pal" % r), pals[r])
        print("  written: direction %s" % PICK)
        return 0
    bad = report()
    if DRAFT is not None:
        os.makedirs(DRAFT, exist_ok=True)
        states = collections.OrderedDict()
        states["NOW"] = None
        summary = {}
        for k, D in STYLES.items():
            sets, owner = draw(D)
            dd = os.path.join(DRAFT, k, "museum")
            os.makedirs(os.path.join(dd, "palettes"), exist_ok=True)
            G.save_like(os.path.join(GBA, MUS.dir, "tiles.png"), sets["mus"][0], os.path.join(dd, "tiles.png"))
            for r in MUS.rows:
                write_pal(os.path.join(dd, "palettes", "%02d.pal" % r), sets["mus"][1][r])
            states[k] = sets
            n = sum(1 for t in owner if sets["mus"][0][t] != MUS.van[t])
            summary[k] = dict(title=D["title"], tiles_redrawn=n, new_tiles=0,
                              rows={"museum %d" % r: sets["mus"][1][r] for r in MUS.rows})
            print("  %s %-10s %d tiles redrawn, 0 new; rows recoloured: museum 8/9/10 only" % (k, D["title"], n))
        json.dump(dict(ticket="T-541", status="DRAFT -- not in the engine", approved=sorted(APPROVED),
                       directions=summary), open(os.path.join(DRAFT, "directions.json"), "w"), indent=1)
        for p in contact_sheets(DRAFT, states):
            print("  sheet:", p)
    if len(APPROVED) == 1:
        bad = check_engine() or bad
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""The rest of the interiors, batch 2: the workrooms -- the bike shop, HOLT's SEA COTTAGE and the QUICKSILVER lab --
redrawn in place in our own hand (T-538).

    python3 tools/gbaworkrooms.py                   # report: batch 2 object by object, what is left vanilla and why
    python3 tools/gbaworkrooms.py --draft [DIR]     # the three directions (A, B, C) drawn in full: per direction each
                                                    #   secondary's tiles.png and own rows as .pal, and the contact
                                                    #   sheets (gfx/drafts/t538_b2/)
    python3 tools/gbaworkrooms.py --write --approved --pick X
                                                    # into the engine -- refused unless X is in APPROVED (empty: the
                                                    #   user has not picked)

THE ANSWER IT FOLLOWS (the user, 2026-11-10, "Other interiors", census item 6). gbahomes.py split the job into
batches and drew batch 1 (the road houses and primary/building's leftovers). This is batch 2, the workrooms:

  bike_shop     CERULEAN's bike shop (one map): its wall, its floor, the parts racks, the tools on the wall and the
                floor, the bicycles, the tool box. The racks the user named are this set's own tiles, not primary's.
  sea_cottage   HOLT's SEA COTTAGE on ROUTE 25 (one map): the wall and its pillars, the floor, the SEPARATION SYSTEM
                (two pods and the pipe between them, 4.x: "it forces a read that the store deliberately defers"), the
                notes on the floor and the wall, the crates.
  lab           the QUICKSILVER lab (four maps) and THREE ISLAND's house 1: the SALVAGE RIG that reads legacy silicon
                (vanilla's fossil reviver: "Deadstack's fossils are legacy silicon"), the wall of cabinets and tanks,
                the door plates, two instruments on their stands, the founder's frame. Its walls and floor are
                primary/building's (batch D, already ours).

NOT HERE: the founder's PHOTO (gbafounder.py, CRYSTAL -- only the frame round it is redrawn; the 110 pixels of her
picture are copied through untouched); everything primary/building places in these rooms (batch D, T-537, batch 1).

THE RULES ARE gbahomes.py's (batch D's): redrawn IN PLACE. No block, layer, flip, palette row, behaviour or
collision bit moves and no map is touched; only pixels inside tiles change, and every tile keeps its FOOTPRINT (a
transparent pixel stays transparent, a drawn one stays drawn). Primary rows 0..6 never change colour: the lab's
tiles placed in rows 0, 1 and 3 are drawn in the colours those rows hold. Only the secondaries' own rows are
recoloured -- bike_shop 7 and 8, sea_cottage 8 and 9, lab 7, 8 and 12 -- each built from the direction's materials.
None of the three has an animation; no script or engine constant names a block in any of them.

Every in-game word: none. This is art. The door plates and the notes are blank on purpose.
"""
import collections, contextlib, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from daemonslib import write_pal, read_pal
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t538_b2")
#  The user's pick goes here ("A", "B" or "C"); --write refuses anything not in it.
APPROVED = {"A"}                     # the user, 2026-11-10: "A THE WORKBENCH"

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

#  gbahomes (and gbabuilding under it) read their switches off sys.argv at import (engine.md trap 16): a clean argv
_argv, sys.argv = sys.argv, ["gbahomes"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import gbahomes as G
finally:
    sys.argv = _argv

Cv, H, M, h, v, hv = G.Cv, G.H, G.M, G.h, G.v, G.hv

BIKE = G.Set("bike", "gTileset_BikeShop", [7, 8])
SEA = G.Set("sea", "gTileset_SeaCottage", [8, 9])
LAB = G.Set("lab", "gTileset_Lab", [7, 8, 12])
SETS = {"bike": BIKE, "sea": SEA, "lab": LAB}
G.SETS.update(SETS)          # Cv and render_map look sets up there

#  the founder's photo (gbafounder.py): canvas pixels of the frame group that are hers and are copied through
PHOTO_TILES = {10, 11, 26, 27}


def photo_pixel(t, k):
    x, y = k % 8, k // 8
    if t == 10:
        return 4 <= y and x >= 2
    if t == 11:
        return 4 <= y and x <= 4
    if t == 26:
        return y <= 5 and x >= 2
    if t == 27:
        return y <= 5 and x <= 4
    return False


# ============================================================================================ drawing helpers
def ell(K, cx, cy, rx, ry, m, ring=None):
    """a filled ellipse; with ring, only the band rx-ring..rx"""
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            d = ((x - cx) / max(rx, .5)) ** 2 + ((y - cy) / max(ry, .5)) ** 2
            if d <= 1 and (ring is None or d >= ((rx - ring) / max(rx, .5)) ** 2):
                K.px(x, y, m)


def shade_by_light(K, lit, mid, dark, cx=None):
    """a rounded body lit from the upper left: three materials by position in its own footprint"""
    x0, y0, x1, y1 = K.bbox()
    cx = (x0 + x1) / 2 if cx is None else cx
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if K.foot(x, y):
                t = (x - cx) / max(1, (x1 - x0) / 2)
                K.px(x, y, lit if t < -0.35 else (dark if t > 0.45 else mid))


def lines_v(K, x0, x1, y0, y1, step, m, off=0):
    for x in range(x0, x1 + 1):
        if (x - off) % step == 0:
            K.vline(x, y0, y1, m)


def by_vanilla(K, table, default="MID"):
    """vanilla's tone kept as LIGHTING only: each vanilla index -> one of the direction's materials (used where the
    silhouette is thin -- a spanner, a bicycle -- and the light is all there is to redraw)"""
    for y in range(K.h):
        for x in range(K.w):
            vv = K.vi(x, y)
            if vv is not None:
                K.out[y][x] = table.get(vv, default)


def lum_rank(S, row):
    """vanilla row's indices ranked dark..light (1..15)"""
    pal = S.vpal[row]
    return sorted(range(1, 16), key=lambda i: sum(pal[i]))


def by_tone(K, S, row, ramp):
    """map each vanilla index by its brightness in vanilla's row onto RAMP (dark..light materials)"""
    pal = S.vpal[row]
    lum = {i: (pal[i][0] * 3 + pal[i][1] * 6 + pal[i][2]) / 10 for i in range(1, 16)}
    lo, hi = min(lum.values()), max(lum.values())
    for y in range(K.h):
        for x in range(K.w):
            vv = K.vi(x, y)
            if vv is not None:
                t = (lum[vv] - lo) / max(1, hi - lo)
                K.out[y][x] = ramp[min(len(ramp) - 1, int(t * len(ramp)))]


# ============================================================================================ painters: bike shop
def p_bk_wall(K, D):
    """the shop's back wall: the cornice band (rows 0..15), the board the tools hang on (16..39), its foot (34), and
    the side posts (the end columns, mirrored)"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            post = x < 8 or x >= K.w - 8
            if post:
                xx = x if x < 8 else K.w - 1 - x
                K.out[y][x] = D["bk_post"](xx, y)
            elif y < 16:
                K.out[y][x] = D["bk_upper"](x, y)
            elif y < 32 or (32 <= y < 40 and False):
                K.out[y][x] = D["bk_board"](x, y)
            elif y < 40:
                K.out[y][x] = D["bk_foot"](x, y - 32)
            else:
                K.out[y][x] = D["bk_floor"](x, y, True)


def p_bk_floor(K, D, shade):
    #  42 / 40 the "A" squares, 41 / 39 the "B" squares of vanilla's check: our floor reads across both
    K.fn(lambda x, y: D["bk_floor"](x, y, shade))


def p_bk_floor_lit(K, D):
    p_bk_floor(K, D, False)


def p_bk_floor_shade(K, D):
    p_bk_floor(K, D, True)


def p_bk_rack(K, D):
    """the parts rack on the wall (two stand side by side): frame, three shelves, what is on them"""
    x0, y0, x1, y1 = K.bbox()
    D["bk_rack"](K, x0, y0, x1, y1)
    K.rim("OUT")


def p_bk_walltool(K, D):
    """the tools hung on the wall: vanilla's silhouette, our metal and its light"""
    by_tone(K, BIKE, 7, ["OUT", "SHD", D["bk_tool"][0], D["bk_tool"][1], D["bk_tool"][2]])
    K.rim("OUT")


def p_bk_bike(K, D):
    """a bicycle on its stand: tyres dark, rims bright, the frame in the direction's enamel, a leather saddle"""
    x0, y0, x1, y1 = K.bbox()
    by_tone(K, BIKE, 8, ["OUT", "TY", "K1", "K2", "K3", "RM"])
    #  the frame's own colour over vanilla's: anything vanilla coloured (not grey, not dark) becomes the enamel
    pal = BIKE.vpal[8]
    for y in range(K.h):
        for x in range(K.w):
            vv = K.vi(x, y)
            if vv is None:
                continue
            r, g, b = pal[vv]
            sat = max(r, g, b) - min(r, g, b)
            lum = (r * 3 + g * 6 + b) / 10
            if sat > 60:
                K.out[y][x] = "K3" if lum > 170 else ("K2" if lum > 110 else "K1")
            elif lum < 70:
                K.out[y][x] = "OUT"
            elif lum < 120:
                K.out[y][x] = "TY"
            elif lum > 200:
                K.out[y][x] = "RM"
            else:
                K.out[y][x] = "MID"
    #  a saddle where the frame is highest at the back: the top-left drawn run
    for y in range(y0, y0 + 4):
        row = [x for x in range(x0, x0 + (x1 - x0) // 2) if K.foot(x, y)]
        if len(row) >= 3:
            for x in row[:4]:
                K.px(x, y, "SD")
            break
    K.rim("OUT")


def p_bk_box(K, D):
    """the tool box on the floor: its lid, its body, a handle, the clasp"""
    x0, y0, x1, y1 = K.bbox()
    D["bk_box"](K, x0, y0, x1, y1)
    K.rim("OUT")


def p_bk_floortool(K, D):
    by_tone(K, BIKE, 7, ["OUT", "SHD", D["bk_tool"][0], D["bk_tool"][1], D["bk_tool"][2]])
    K.rim("OUT")


# ============================================================================================ painters: sea cottage
def p_sc_wall(K, D):
    """HOLT's wall: the top rail (0..7), the wall (8..15), the lower band (16..23), its foot (24..31); column 0 is the
    pillar (its tile repeats, so the pillar is 8-periodic)"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = D["sc_pillar"](x % 8, y) if x < 8 else D["sc_wall"](x % 8, y)


def p_sc_floor(K, D, shade):
    K.fn(lambda x, y: D["sc_floor"](x % 8, y % 16, shade))


def p_sc_floor_lit(K, D):
    p_sc_floor(K, D, False)


def p_sc_floor_shade(K, D):
    p_sc_floor(K, D, True)


def p_sc_note(K, D):
    """a note, pinned on the wall or dropped on the floor (6 7 / 22 23-or-8), and the pencil beside it (9 24 25)"""
    #  the sheet: the drawn pixels of cells (0..1, 0..1); its lines are blank, wordless
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            sheet = x < 16 and y < 16
            if sheet:
                K.out[y][x] = "PA" if (y % 3 or x < 3 or x > 12) else "MID"
            else:
                K.out[y][x] = D["sc_pencil"](x, y)
    K.rim("OUT")


def p_sc_pod(K, D):
    """one pod of the SEPARATION SYSTEM (48 x 48, mirrored but for its window)"""
    x0, y0, x1, y1 = K.bbox()
    D["sc_pod"](K, x0, y0, x1, y1)


def p_sc_pipe(K, D):
    """the pipe between the pods: what passes along it is the read the store defers"""
    D["sc_pipe"](K)


def p_sc_crate(K, D):
    x0, y0, x1, y1 = K.bbox()
    D["sc_crate"](K, x0, y0, x1, y1)
    K.rim("OUT")


# ============================================================================================ painters: the lab
def p_lab_rig(K, D):
    """vanilla's fossil reviver -> the SALVAGE RIG: a reader that takes a slab of legacy silicon and brings back what
    ran on it. A dome over the slab, a body with a window, feet."""
    x0, y0, x1, y1 = K.bbox()
    D["lab_rig"](K, x0, y0, x1, y1)


def p_lab_wall(K, D):
    """the wall of cabinets (16 | 14 15 | 16) and tanks (45 45h over 61, 77, 69 70): the lab's long storage"""
    D["lab_wall"](K)


def p_lab_stand(K, D):
    """an instrument on its stand (the research room's, 80 81 / 96 97 / 82 83; THREE ISLAND's, 98 99 / 84 85 /
    100 101)"""
    x0, y0, x1, y1 = K.bbox()
    D["lab_stand"](K, x0, y0, x1, y1, K.kind)
    K.rim("OUT")


def p_lab_plate(K, D):
    """the plate over a lab door (primary row 3): blank -- the rooms are known by what is in them"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = D["lab_platewall"](x, y)
    D["lab_plate"](K)


def p_lab_frame(K, D):
    """the founder's frame (primary row 0): ours round her photo, which is copied through untouched"""
    x0, y0, x1, y1 = K.bbox()
    D["lab_frame"](K, x0, y0, x1, y1)


def p_lab_odd(K, D):
    """lab tile 44 (primary row 1), the corner of the reception's glass at the lobby's left: glass and its frame"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = "GLASS_D" if (x + y) % 7 else "GLASS_L"
    K.rim("OUT")


# ============================================================================================ the groups
#  key, set, layout (as it stands), painter, what it is
GROUPS = [
    ("bk_wall",   "bike", M([1, 16, 16, h(1)], [17, 2, 2, h(17)], [4, 18, 18, h(4)], [20, 18, 18, h(20)],
                            [20, 34, 34, h(20)], [36, None, None, h(36)]), p_bk_wall,
     "the back wall: cornice, the board the tools hang on, its foot, the side posts"),
    ("bk_floor",  "bike", M([42, 41], [41, 42]),                 p_bk_floor_lit,   "the shop floor"),
    ("bk_shade",  "bike", M([40, 39], [39, 40]),                 p_bk_floor_shade, "the same floor in the wall's shade"),
    ("bk_rack",   "bike", M([44, 45, 46, 47], [48, 49, 50, 51], [52, 53, 54, 55], [56, 57, 58, 59]), p_bk_rack,
     "the parts racks (the racks the user named)"),
    ("bk_spanner", "bike", M([5, 6], [21, 22]),                  p_bk_walltool,    "a spanner on its hook"),
    ("bk_pump",   "bike", M([37, 38]),                           p_bk_walltool,    "a pump on its hook"),
    ("bk_big",    "bike", M([10, 11, 12], [26, 27, 28]),         p_bk_bike,        "the big bicycle on its stand"),
    ("bk_small",  "bike", M([None, 8, 9], [23, 24, 25]),         p_bk_bike,        "the small bicycles"),
    ("bk_wrench", "bike", M([None, 43], [7, None]),              p_bk_floortool,   "a spanner left on the floor"),
    ("bk_box",    "bike", M([13, 14], [29, 30]),                 p_bk_box,         "the tool box"),
    ("sc_wall",   "sea",  M([4, 2], [20, 18], [5, 3], [21, 19]), p_sc_wall,        "HOLT's wall and its pillars"),
    ("sc_floor",  "sea",  M([1], [17]),                          p_sc_floor_lit,   "the cottage floor"),
    ("sc_shade",  "sea",  M([48], [49]),                         p_sc_floor_shade, "the floor in the wall's shade"),
    ("sc_note",   "sea",  M([6, 7, None], [22, 8, 9], [None, 24, 25]), p_sc_note,  "a note and its pencil, on the floor"),
    ("sc_notewall", "sea", M([6, 7], [22, 23]),                  p_sc_note,        "a note pinned on the wall"),
    ("sc_pod",    "sea",  M([None, 10, 11, h(11), h(10), None], [32, 26, 27, h(27), h(26), h(32)],
                            [33, 12, 13, h(13), h(12), h(33)], [34, 28, 50, 51, h(28), h(34)],
                            [35, 36, 39, 40, h(36), h(35)], [37, 38, 41, 42, h(38), h(37)]), p_sc_pod,
     "a pod of the SEPARATION SYSTEM"),
    ("sc_pipe",   "sea",  M([14, 15, h(15), 15, h(15), h(14)], [30, 31, h(31), 31, h(31), h(30)]), p_sc_pipe,
     "the pipe between the pods"),
    ("sc_crate",  "sea",  M([44, h(44)], [46, h(46)], [47, h(47)], [16, h(16)]), p_sc_crate, "two crates, stacked"),
    ("sc_crate2", "sea",  M([44, h(44)], [45, h(45)]),           p_sc_crate,       "a single crate"),
    ("lab_rig",   "lab",  M([1, 2, 3, 4], [17, 18, 19, 20], [33, 34, 35, 36], [49, 50, 51, 52], [65, 66, 67, 68]),
     p_lab_rig, "the SALVAGE RIG (vanilla's fossil reviver)"),
    ("lab_wall",  "lab",  M([16, 14, 15, 16, 45, h(45), 16], [32, 30, 31, 32, 61, h(61), 32],
                            [48, 46, 47, 48, 77, h(77), 48], [64, 62, 63, 64, 69, 70, 64]), p_lab_wall,
     "the wall of cabinets and tanks"),
    ("lab_scope", "lab",  M([80, 81], [96, 97], [82, 83]),       p_lab_stand,      "the research room's instrument"),
    ("lab_radio", "lab",  M([98, 99], [84, 85], [100, 101]),     p_lab_stand,      "THREE ISLAND's set on its table"),
    ("lab_plate", "lab",  M([12, 13], [28, 29]),                 p_lab_plate,      "the plate over a door (row 3)"),
    ("lab_frame", "lab",  M([10, 11], [26, 27], [42, 43]),       p_lab_frame,      "the founder's frame (row 0)"),
    ("lab_odd",   "lab",  M([44]),                               p_lab_odd,        "the lobby glass's corner (row 1)"),
]
KIND = {"lab_scope": "scope", "lab_radio": "radio"}

#  each own row's fifteen materials, in index order 1..15 (the same layout in every direction)
ROWMATS = {
    ("bike", 7): ["OUT", "SHD", "MID", "HI", "WHT", "F0", "F1", "F2", "W1", "W2", "W3", "WT", "T1", "T2", "X"],
    ("bike", 8): ["OUT", "SHD", "MID", "HI", "WHT", "K1", "K2", "K3", "TY", "RM", "SD", "B1", "B2", "X", "XL"],
    ("sea", 9):  ["OUT", "SHD", "MID", "HI", "WHT", "F0", "F1", "F2", "F3", "W1", "W2", "W3", "C1", "C2", "C3"],
    ("sea", 8):  ["OUT", "SHD", "MID", "HI", "WHT", "M1", "M2", "M3", "G1", "G2", "G3", "X", "XL", "PA", "PI"],
    ("lab", 7):  ["OUT", "SHD", "MID", "HI", "WHT", "C1", "C2", "C3", "G1", "G2", "G3", "X", "XL", "BK", "BK2"],
    ("lab", 8):  ["OUT", "SHD", "MID", "HI", "WHT", "S1", "S2", "S3", "D1", "D2", "D3", "X", "XL", "LM", "N1"],
    ("lab", 12): ["OUT", "SHD", "MID", "HI", "WHT", "R1", "R2", "R3", "G1", "G2", "G3", "X", "XL", "L1", "L2"],
}


# ============================================================================================ resolving
def mats_for(D, setkey):
    m = dict(D["mat"]["*"])
    m.update(D["mat"][setkey])
    return m


def set_palettes(D, S):
    mat = mats_for(D, S.key)
    out = {}
    for r in range(16):
        if r in S.rows:
            out[r] = [S.vpal[r][0]] + [mat[m] for m in ROWMATS[S.key, r]]
        else:
            out[r] = list(read_pal(os.path.join(GBA, S.dir, "palettes/%02d.pal" % r)))
    return out


def draw(D):
    """-> {setkey: (tiles, palettes)}, owner {(setkey, t): group}"""
    out = {k: ([t[:] for t in S.cur], set_palettes(D, S)) for k, S in SETS.items()}
    owner = {}
    for key, setkey, layout, painter, what in GROUPS:
        S = SETS[setkey]
        K = Cv(layout, setkey)
        t0 = next(s[0] for r in K.layout for s in r if s is not None)
        K.row = S.home(t0)
        K.kind = KIND.get(key)
        painter(K, D)
        mat = mats_for(D, setkey)
        for t, mats in K.tiles().items():
            if (setkey, t) in owner or t >= S.nvan or t not in S.use:
                continue
            spals = out[setkey][1]
            rows = dict(S.use[t]["rows"])
            own = {r: spals[r] for r in S.rows}
            Dm = {"mat": mat, "_index": {(r, m): i + 1 for r in S.rows for i, m in enumerate(ROWMATS[S.key, r])}}
            px = G.resolve(mats, S.van[t], rows, Dm, own)
            if setkey == "lab" and t in PHOTO_TILES:
                px = [S.cur[t][k] if photo_pixel(t, k) else px[k] for k in range(64)]
            out[setkey][0][t] = px
            owner[setkey, t] = key
    return out, owner


# ============================================================================================ the directions
#  shared greys per direction; each direction's mat = {"*": shared, setkey: that set's}
def ramp(d, l):
    return d, l


# ---------------------------------------------------------------------------------------- A THE WORKBENCH
def A_bk_post(x, y):
    """an oak post, a darker arris on the inside"""
    if x == 7:
        return "OUT"
    return "T1" if x in (5, 6) else ("T2" if x in (0, 1) else "T2" if (y + x) % 9 else "T1")


def A_bk_upper(x, y):
    """the cornice: an oak rail, then whitewashed boards"""
    if y == 0:
        return "OUT"
    if y < 4:
        return "T2" if y == 1 else "T1"
    if y == 4:
        return "OUT"
    return "W2" if x % 6 == 5 else ("W3" if y > 5 else "WT")


def A_bk_board(x, y):
    """cork board, the tools' own outline painted on it (a maker's shadow board)"""
    if (x * 7 + y * 3) % 11 == 0:
        return "W1"
    return "F2" if H(x, y, 9) % 4 == 0 else "WT"


def A_bk_foot(x, y):
    """the bench rail under the board: oak on a dark rebate"""
    if y < 2:
        return "OUT" if y == 0 else "T2"
    if y < 6:
        return "T1" if x % 16 else "SHD"
    return "SHD" if y == 6 else "OUT"


def A_bk_floor(x, y, shade):
    """oak block parquet in a basket weave: vanilla's check is the weave -- one square's two blocks run across, its
    neighbour's run down -- so the floor reads as laid wood, not as tiles"""
    across = ((x // 8) + (y // 8)) % 2 == 0
    a, b = (y % 8, x % 8) if across else (x % 8, y % 8)
    if a in (3, 7):
        return "F0"
    if b == 7 and a < 3 and across:
        return "F0"
    base = "F1" if shade else "F2"
    if a in (0, 4) and not shade:
        return "F2" if across else "F1"
    return base if H(x // 8, y // 8 * 2 + a // 4, 2) % 3 else ("F0" if shade else "F1")


def A_bk_rack(K, x0, y0, x1, y1):
    """an oak parts rack: two bays, shelves of wheels, tins and a tyre"""
    K.fn(lambda x, y: "T1")
    K.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, "SHD")
    for sy in (y0 + 10, y0 + 20, y1 - 3):
        K.rect(x0 + 1, sy, x1 - 1, sy + 1, "T2")
        K.hline(x0 + 1, x1 - 1, sy + 2, "OUT")
    K.vline((x0 + x1) // 2, y0 + 2, y1 - 2, "T1")
    #  top shelf: wheels on pegs, in profile (ellipses)
    for cx in (x0 + 7, x0 + 24):
        ell(K, cx, y0 + 6, 3.5, 3.5, "SHD")
        ell(K, cx, y0 + 6, 3.5, 3.5, "MID", ring=1.2)
        K.px(cx, y0 + 6, "HI")
    #  middle shelf: tins (brass lids)
    for cx in range(x0 + 4, x1 - 2, 5):
        K.rect(cx, y0 + 15, cx + 3, y0 + 19, "MID")
        K.hline(cx, cx + 3, y0 + 15, "X")
        K.vline(cx, y0 + 16, y0 + 19, "HI")
    #  bottom: a coiled tyre and a box
    ell(K, x0 + 9, y0 + 25, 5, 2.4, "OUT")
    ell(K, x0 + 9, y0 + 25, 5, 2.4, "SHD", ring=1)
    K.rect(x0 + 19, y0 + 23, x1 - 4, y0 + 27, "WT")
    K.hline(x0 + 19, x1 - 4, y0 + 23, "WHT")


def A_bk_box(K, x0, y0, x1, y1):
    """a joiner's tool box: green-painted wood, a timber handle along the top, brass corners"""
    K.fn(lambda x, y: "B1")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if K.foot(x, y) and (x + y) % 5 == 0:
                K.px(x, y, "B2")
    K.hline(x0, x1, y0 + 1, "XL")
    K.hline(x0, x1, y0 + 2, "X")
    for x, y in ((x0 + 1, y1 - 1), (x1 - 1, y1 - 1)):
        K.px(x, y, "XL")


def A_sc_pillar(x, y):
    """a copper-clad pillar (an otter's holt by the sea: everything here is ship's copper and teak)"""
    if x == 7:
        return "OUT"
    if y < 8 and y in (0, 7):
        return "OUT"
    return "W1" if x == 6 else ("W3" if x < 2 else ("W2" if (y // 4) % 2 else "W3"))


def A_sc_wall(x, y):
    if y < 8:          # the top rail: teak, a brass bead
        return "OUT" if y in (0, 7) else ("C3" if y == 2 else "C2")
    if y < 16:         # the wall: pale planking
        return "F3" if x % 8 != 7 else "F2"
    if y < 24:         # the lower band: a teak dado with a groove
        return "C1" if y in (16, 23) else ("C3" if y == 18 else "C2")
    return "SHD" if y < 26 else ("F0" if y < 28 else "F1")


def A_sc_floor(x, y, shade):
    """ship's deck: teak planks with caulked seams"""
    if y % 4 == 3:
        return "OUT" if shade else "F0"
    if (x + (y // 4) * 3) % 8 == 0 and H(x, y // 4, 3) % 2:
        return "F0"
    return ("F1" if shade else "F2") if (y % 4) else ("F2" if shade else "F3")


def A_sc_pencil(x, y):
    return "PI" if (x + y) % 3 else "X"


def A_sc_pod(K, x0, y0, x1, y1):
    """a copper diving bell on a riveted base: a domed top, a round port of green water, a brass band"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "M2")
    shade_by_light(K, "M3", "M2", "M1")
    for y in range(y0, y1 + 1):
        if (y - y0) % 6 == 5:
            for x in range(x0, x1 + 1):
                if K.foot(x, y) and x % 4 == 0:
                    K.px(x, y, "XL")
    #  the port: green water, a bubble
    ell(K, cx, y0 + 25, 9, 8, "G1")
    ell(K, cx, y0 + 25, 7, 6, "G2")
    ell(K, cx - 2, y0 + 23, 3, 2.5, "G3")
    ell(K, cx, y0 + 25, 9, 8, "X", ring=1.3)
    K.px(int(cx) + 3, y0 + 21, "WHT")
    #  the band and the base
    K.rect(x0, y1 - 9, x1, y1 - 8, "X")
    K.hline(x0, x1, y1 - 9, "XL")
    K.rect(x0, y1 - 7, x1, y1, "M1")
    for x in range(x0 + 2, x1, 5):
        K.px(x, y1 - 4, "XL")
    K.rim("OUT")


def A_sc_pipe(K):
    """a copper pipe, banded, a sight-glass of green water in the middle"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        K.hline(x0, x1, y, "XL" if t < .15 else ("M3" if t < .4 else ("M2" if t < .75 else "M1")))
    for x in range(x0 + 3, x1 + 1, 12):
        K.vline(x, y0, y1, "X")
        K.vline(x + 1, y0, y1, "M1")
    K.rect(x0 + 18, y0 + 2, x1 - 18, y1 - 2, "G2")
    K.hline(x0 + 18, x1 - 18, y0 + 3, "G3")
    K.rim("OUT")


def A_sc_crate(K, x0, y0, x1, y1):
    """a sea chest: teak, rope handles, brass corners"""
    K.fn(lambda x, y: "C2")
    for y in range(y0, y1 + 1):
        if (y - y0) % 16 in (0, 1):
            K.hline(x0, x1, y, "C3" if (y - y0) % 16 == 0 else "C1")
        if (y - y0) % 16 == 15:
            K.hline(x0, x1, y, "OUT")
    for y in range(y0 + 6, y1, 16):
        K.rect(x0 + 5, y, x1 - 5, y + 1, "F3")
    for y in range(y0 + 2, y1, 16):
        K.px(x0 + 1, y, "C3")
        K.px(x1 - 1, y, "C3")


def A_lab_rig(K, x0, y0, x1, y1):
    """the SALVAGE RIG as a foundry piece: a cast-iron body, a copper dome with a sight-glass, a slab of old silicon
    on the bed, a furnace-glow lamp, iron feet"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "R2")
    shade_by_light(K, "R3", "R2", "R1")
    #  the dome (top 16 rows): copper
    for y in range(y0, y0 + 15):
        for x in range(x0, x1 + 1):
            if K.foot(x, y):
                t = (x - cx) / max(1, (x1 - x0) / 2)
                K.px(x, y, "XL" if t < -0.3 else ("X" if t < 0.4 else "L2"))
    ell(K, cx, y0 + 7, 6, 4, "G1")
    ell(K, cx - 1, y0 + 6, 4, 2.5, "G2")
    K.px(int(cx) - 3, y0 + 5, "G3")
    #  the bed: a slab of legacy silicon, its gold pins
    K.rect(x0 + 6, y0 + 17, x1 - 6, y0 + 23, "OUT")
    K.rect(x0 + 7, y0 + 18, x1 - 7, y0 + 22, "G1")
    for x in range(x0 + 8, x1 - 7, 2):
        K.px(x, y0 + 17, "L1")
        K.px(x, y0 + 23, "L1")
    K.hline(x0 + 8, x1 - 9, y0 + 19, "G2")
    #  the lamp and the dial
    ell(K, x0 + 9, y0 + 29, 2.5, 2.5, "L1")
    K.px(x0 + 8, y0 + 28, "WHT")
    ell(K, x1 - 9, y0 + 29, 3, 3, "HI")
    K.vline(int(x1 - 9), y0 + 27, y0 + 29, "OUT")
    #  feet
    K.rect(x0, y1 - 3, x1, y1, "R1")
    K.rim("OUT")


def A_lab_wall(K):
    """oak cabinets with glazed doors, and between them tall glass tanks of quicksilver light on iron stands"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            col = x // 8
            if col in (0, 3, 6):             # the posts between bays
                K.out[y][x] = "C1" if x % 8 in (0, 7) else ("C3" if x % 8 == 1 else "C2")
            elif col in (1, 2):              # a cabinet bay
                xx, yy = x - 8, y
                if yy < 2:
                    K.out[y][x] = "C3" if yy == 0 else "C2"
                elif yy >= 26:
                    K.out[y][x] = "C1" if yy in (26, 31) else "C2"
                elif xx in (0, 7, 8, 15) or yy in (2, 13, 14, 25):
                    K.out[y][x] = "C1"
                else:
                    #  glazed doors: books and jars behind the glass
                    sh = (yy - 3) % 11
                    if sh == 0:
                        K.out[y][x] = "C1"
                    elif sh >= 4:
                        K.out[y][x] = ("BK", "BK2", "X", "G1")[(xx + yy // 11) % 4] if xx % 3 else "OUT"
                    else:
                        K.out[y][x] = "G3" if (xx + yy) % 5 == 0 else "G2"
            else:                            # the tank bay (45 45h, 61, 77, 69 70)
                xx, yy = x - 32, y
                if yy < 2:
                    K.out[y][x] = "C2"
                elif yy >= 24:
                    K.out[y][x] = "C1" if yy in (24, 31) else ("XL" if (xx in (3, 12) and yy == 27) else "C2")
                elif xx in (0, 15):
                    K.out[y][x] = "C1"
                else:
                    t = yy / 24
                    K.out[y][x] = "G3" if t < .2 else ("G2" if t < .6 else "G1")
                    if (xx * 5 + yy * 3) % 23 == 0:
                        K.out[y][x] = "WHT"
                    if yy == 6:
                        K.out[y][x] = "G3"
    K.rim("OUT")


def A_lab_stand(K, x0, y0, x1, y1, kind):
    """oak stand; on it a brass microscope (research room) or a valve set in a timber case (THREE ISLAND)"""
    K.fn(lambda x, y: "S2")
    K.rect(x0, y1 - 8, x1, y1, "S1")
    K.hline(x0, x1, y1 - 8, "S3")
    if kind == "scope":
        K.rect(x0 + 6, y0 + 1, x0 + 9, y0 + 12, "X")
        K.vline(x0 + 6, y0 + 1, y0 + 12, "XL")
        K.rect(x0 + 4, y0 + 12, x1 - 4, y0 + 14, "D1")
        K.rect(x0 + 10, y0 + 6, x0 + 12, y0 + 9, "D2")
        K.px(x0 + 7, y0 + 1, "LM")
    else:
        K.rect(x0 + 2, y0 + 1, x1 - 2, y0 + 12, "D2")
        K.hline(x0 + 2, x1 - 2, y0 + 1, "D3")
        ell(K, x0 + 7, y0 + 7, 3.5, 3.5, "N1")
        K.px(x0 + 7, y0 + 7, "OUT")
        K.rect(x1 - 6, y0 + 4, x1 - 4, y0 + 10, "LM")


def A_lab_platewall(x, y):
    return "WALL"


def A_lab_plate(K):
    """a blank brass plate, two screws"""
    x0, y0, x1, y1 = K.bbox()
    K.rect(x0 + 2, y1 - 6, x1 - 2, y1 - 2, "PLATE")
    K.hline(x0 + 2, x1 - 2, y1 - 6, "PLATE_L")
    K.hline(x0 + 2, x1 - 2, y1 - 1, "OUT")
    K.px(x0 + 3, y1 - 4, "OUT")
    K.px(x1 - 3, y1 - 4, "OUT")


def A_lab_frame(K, x0, y0, x1, y1):
    """an oak frame, gilt slip"""
    K.fn(lambda x, y: "FRAME")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = min(x - x0, x1 - x, y - y0, y1 - y)
            if d == 1:
                K.px(x, y, "FRAME_L")
            elif d >= 3:
                K.px(x, y, "FRAME_IN")
    K.rim("OUT")


# ---------------------------------------------------------------------------------------- B THE CLEAN ROOM
def B_bk_post(x, y):
    if x == 7:
        return "OUT"
    return "W2" if x >= 5 else "W3"


def B_bk_upper(x, y):
    """white glazed tiles, a steel cornice"""
    if y == 0:
        return "OUT"
    if y < 3:
        return "HI" if y == 1 else "MID"
    if y == 3:
        return "SHD"
    return "W2" if (x % 8 == 7 or y % 6 == 3) else "W3"


def B_bk_board(x, y):
    """perforated white steel"""
    return "W1" if (x % 3 == 1 and y % 3 == 1) else "W3"


def B_bk_foot(x, y):
    if y == 0:
        return "W2"
    if y < 6:
        return "MID" if y < 2 else ("HI" if y == 2 else "MID")
    return "SHD" if y == 6 else "OUT"


def B_bk_floor(x, y, shade):
    """sealed vinyl squares, pale grey and white, a fine grout"""
    if x % 8 == 7 or y % 8 == 7:
        return "F0"
    a = ((x // 8) + (y // 8)) % 2
    if shade:
        return "F0" if a else "F1"
    return "F1" if a else "F2"


def B_bk_rack(K, x0, y0, x1, y1):
    """white steel shelving behind glass: parts in labelled bins (the labels blank)"""
    K.fn(lambda x, y: "W3")
    K.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, "HI")
    for sy in (y0 + 10, y0 + 20):
        K.hline(x0 + 1, x1 - 1, sy, "MID")
        K.hline(x0 + 1, x1 - 1, sy + 1, "SHD")
    for row, yy in enumerate((y0 + 4, y0 + 14, y0 + 24)):
        for i, cx in enumerate(range(x0 + 3, x1 - 4, 7)):
            K.rect(cx, yy, cx + 5, yy + 5, ("T1", "X", "T2")[(i + row) % 3])
            K.rect(cx + 1, yy + 1, cx + 4, yy + 2, "WHT")
    for y in range(y0 + 2, y1 - 1):
        if (y - y0) % 9 == 3:
            K.px(x0 + 3, y, "WHT")


def B_bk_box(K, x0, y0, x1, y1):
    """a steel case, blue, a white handle"""
    K.fn(lambda x, y: "B1")
    K.hline(x0, x1, y0 + 1, "B2")
    K.rect(x0 + 3, y0 + 2, x1 - 3, y0 + 3, "RM")
    K.hline(x0, x1, y1 - 2, "SHD")


def B_sc_pillar(x, y):
    if x == 7:
        return "OUT"
    return "W2" if x >= 5 else "W3"


def B_sc_wall(x, y):
    if y < 8:
        return "OUT" if y in (0, 7) else ("C3" if y < 3 else "C2")
    if y < 16:
        return "W3" if (x % 8 != 7 and y % 8 != 7) else "W2"
    if y < 24:
        return "C1" if y == 16 else ("W2" if y < 20 else "W1")
    return "SHD" if y < 26 else "F0"


def B_sc_floor(x, y, shade):
    """a sealed resin floor, faintly blue, a seam every 16px"""
    if y % 16 == 15 or x % 8 == 7 and y % 16 == 7:
        return "F0"
    if shade:
        return "F1"
    return "F3" if H(x, y, 4) % 23 == 0 else "F2"


def B_sc_pencil(x, y):
    return "PI" if (x + y) % 2 else "MID"


def B_sc_pod(K, x0, y0, x1, y1):
    """a glass bell jar on a white enamel plinth: the jar empty and lit blue, a steel collar"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "G2")
    for y in range(y0, y1 - 11):
        for x in range(x0, x1 + 1):
            if K.foot(x, y):
                t = (x - cx) / max(1, (x1 - x0) / 2)
                K.px(x, y, "G3" if t < -0.55 else ("G1" if t > 0.6 else "G2"))
    for y in range(y0 + 3, y1 - 13, 3):
        K.px(int(cx - (x1 - x0) * 0.3), y, "WHT")
    #  inside: the beam (one line, top to bottom)
    K.vline(int(cx), y0 + 6, y1 - 13, "XL")
    K.rect(x0, y1 - 11, x1, y1 - 10, "M1")
    K.rect(x0, y1 - 9, x1, y1, "M3")
    K.hline(x0, x1, y1 - 9, "WHT")
    K.rect(int(cx) - 3, y1 - 6, int(cx) + 2, y1 - 4, "X")
    K.rim("OUT")


def B_sc_pipe(K):
    """a glass conduit with a blue light running along it"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        K.hline(x0, x1, y, "G3" if t < .3 else ("G2" if t < .75 else "G1"))
    K.hline(x0, x1, (y0 + y1) // 2, "XL")
    for x in range(x0, x1 + 1, 16):
        K.vline(x, y0, y1, "M1")
    K.rim("OUT")


def B_sc_crate(K, x0, y0, x1, y1):
    """a white specimen case, a blue stripe"""
    K.fn(lambda x, y: "C3")
    for y in range(y0, y1 + 1):
        r = (y - y0) % 16
        if r == 0:
            K.hline(x0, x1, y, "WHT")
        elif r in (7, 8):
            K.hline(x0, x1, y, "W1")
        elif r == 15:
            K.hline(x0, x1, y, "OUT")
        elif r >= 13:
            K.hline(x0, x1, y, "C2")


def B_lab_rig(K, x0, y0, x1, y1):
    """the SALVAGE RIG as clean-room kit: a white enamel body, a glass dome lit blue over the slab, a status strip"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "R2")
    shade_by_light(K, "R3", "R2", "R1")
    for y in range(y0, y0 + 15):
        for x in range(x0, x1 + 1):
            if K.foot(x, y):
                t = (x - cx) / max(1, (x1 - x0) / 2)
                K.px(x, y, "G3" if t < -0.4 else ("G1" if t > 0.5 else "G2"))
    K.px(int(cx) - 6, y0 + 4, "WHT")
    K.px(int(cx) - 5, y0 + 3, "WHT")
    K.hline(x0 + 2, x1 - 2, y0 + 15, "X")
    K.rect(x0 + 6, y0 + 17, x1 - 6, y0 + 23, "OUT")
    K.rect(x0 + 7, y0 + 18, x1 - 7, y0 + 22, "G1")
    K.hline(x0 + 8, x1 - 8, y0 + 20, "XL")
    for i, x in enumerate(range(x0 + 7, x1 - 6, 4)):
        K.rect(x, y0 + 27, x + 1, y0 + 28, "L1" if i % 3 else "L2")
    K.rect(x0, y1 - 3, x1, y1, "R1")
    K.rim("OUT")


def B_lab_wall(K):
    """white steel lockers with a slot of glass, and tall clean tanks lit blue"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            col = x // 8
            if col in (0, 3, 6):
                K.out[y][x] = "C1" if x % 8 in (0, 7) else "C2"
            elif col in (1, 2):
                xx = x - 8
                if y < 2 or y >= 30:
                    K.out[y][x] = "C1"
                elif xx in (0, 7, 8, 15) or y in (15, 16):
                    K.out[y][x] = "C2"
                elif 4 <= y <= 6 and 2 <= xx % 8 <= 5:
                    K.out[y][x] = "G2"
                elif y in (10, 22) and xx % 8 == 5:
                    K.out[y][x] = "X"
                else:
                    K.out[y][x] = "C3"
            else:
                xx = x - 32
                if y < 2:
                    K.out[y][x] = "C2"
                elif y >= 24:
                    K.out[y][x] = "C1" if y in (24, 31) else ("XL" if xx in (4, 5) and y == 27 else "C3")
                elif xx in (0, 15):
                    K.out[y][x] = "C2"
                else:
                    K.out[y][x] = "G3" if (xx < 4) else ("G2" if xx < 12 else "G1")
                    if y % 6 == 2 and xx == 8:
                        K.out[y][x] = "WHT"
    K.rim("OUT")


def B_lab_stand(K, x0, y0, x1, y1, kind):
    """a white steel stand; on it a grey analyser with a small screen, or a white radio set"""
    K.fn(lambda x, y: "S3")
    K.rect(x0, y1 - 8, x1, y1, "S2")
    K.hline(x0, x1, y1 - 8, "WHT")
    K.rect(x0 + 2, y0 + 1, x1 - 2, y0 + 12, "D2")
    K.hline(x0 + 2, x1 - 2, y0 + 1, "D3")
    if kind == "scope":
        K.rect(x0 + 4, y0 + 3, x1 - 6, y0 + 8, "N1")
        K.hline(x0 + 5, x1 - 8, y0 + 5, "LM")
    else:
        for x in range(x0 + 4, x1 - 6, 2):
            K.vline(x, y0 + 4, y0 + 10, "D1")
        K.rect(x1 - 6, y0 + 4, x1 - 4, y0 + 6, "LM")


def B_lab_plate(K):
    x0, y0, x1, y1 = K.bbox()
    K.rect(x0 + 2, y1 - 6, x1 - 2, y1 - 2, "PLATE_W")
    K.hline(x0 + 2, x1 - 2, y1 - 1, "OUT")
    K.hline(x0 + 3, x0 + 5, y1 - 4, "PLATE_B")


def B_lab_frame(K, x0, y0, x1, y1):
    """a thin white enamel frame"""
    K.fn(lambda x, y: "FRAME_W")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = min(x - x0, x1 - x, y - y0, y1 - y)
            if d >= 2:
                K.px(x, y, "FRAME_IN_W")
    K.rim("OUT")


# ---------------------------------------------------------------------------------------- C THE SALVAGE YARD
def C_bk_post(x, y):
    """a scaffold pole, lashed"""
    if x == 7:
        return "OUT"
    if y % 12 in (4, 5):
        return "T2"
    return "MID" if x < 3 else ("SHD" if x > 5 else "HI")


def C_bk_upper(x, y):
    """corrugated sheet, the ribs showing, a little rust"""
    if y == 0:
        return "OUT"
    if y < 3:
        return "X" if y == 1 else "SHD"
    rib = x % 4
    m = ("W3", "W2", "W1", "W2")[rib]
    return "X" if H(x, y, 5) % 29 == 0 else m


def C_bk_board(x, y):
    """planks from crates, laid across, nail heads at the joints"""
    if y % 5 == 4:
        return "OUT"
    if (x + (y // 5) * 7) % 21 == 0:
        return "SHD"
    if (x + (y // 5) * 7) % 21 == 1 and y % 5 == 1:
        return "HI"
    return "T2" if H(x // 4, y // 5, 1) % 3 else "T1"


def C_bk_foot(x, y):
    """a rope along the foot of the boards"""
    if y < 2:
        return "OUT" if y == 0 else "SHD"
    if y < 5:
        return "WT" if (x + y) % 3 else "W1"
    return "SHD" if y < 7 else "OUT"


def C_bk_floor(x, y, shade):
    """poured concrete, cracked, oil-stained"""
    if (x * 2 + y) % 23 == 0 and H(x // 8, y // 8, 8) % 3 == 0:
        return "F0"
    if H(x // 3, y // 3, 4) % 11 == 0:
        return "F0" if shade else "F1"
    return "F1" if shade else "F2"


def C_bk_rack(K, x0, y0, x1, y1):
    """a pallet stood on end: wheels hung on its slats, a chain, a crate of bolts"""
    K.fn(lambda x, y: "T1")
    for y in range(y0, y1 + 1):
        if (y - y0) % 6 in (4, 5):
            K.hline(x0, x1, y, "SHD" if (y - y0) % 6 == 4 else "OUT")
    for x in (x0 + 1, (x0 + x1) // 2, x1 - 1):
        K.vline(x, y0, y1, "T2")
    for cx, cy in ((x0 + 8, y0 + 9), (x0 + 22, y0 + 7)):
        ell(K, cx, cy, 5.5, 5.5, "OUT")
        ell(K, cx, cy, 5.5, 5.5, "SHD", ring=1.6)
        K.px(cx, cy, "HI")
        K.hline(cx - 4, cx + 4, cy, "MID")
        K.vline(cx, cy - 4, cy + 4, "MID")
    for i, y in enumerate(range(y0 + 15, y0 + 24)):
        K.px(x0 + 16 + (i % 2), y, "HI" if i % 2 else "MID")
    K.rect(x0 + 3, y1 - 7, x1 - 3, y1 - 2, "X")
    for x in range(x0 + 4, x1 - 3, 2):
        K.px(x, y1 - 6, "HI")


def C_bk_box(K, x0, y0, x1, y1):
    """an ammunition box turned tool box: olive drab, rusted clasps"""
    K.fn(lambda x, y: "B1")
    K.hline(x0, x1, y0 + 1, "B2")
    K.hline(x0, x1, y0 + 3, "OUT")
    K.px(x0 + 3, y0 + 2, "X")
    K.px(x1 - 3, y0 + 2, "X")
    for y in range(y0 + 5, y1, 3):
        K.hline(x0 + 2, x1 - 2, y, "SHD")


def C_sc_pillar(x, y):
    """a driftwood post, bleached"""
    if x == 7:
        return "OUT"
    return "W3" if x < 2 else ("W1" if (y * 3 + x) % 7 == 0 else "W2")


def C_sc_wall(x, y):
    if y < 8:          # a rope strung along the top
        return "OUT" if y in (0, 7) else (("C3", "C2")[(x + y) % 2] if 2 <= y <= 5 else "SHD")
    if y < 24:         # shiplap, salvaged, two shades of old paint
        if (y - 8) % 4 == 3:
            return "SHD"
        return "W3" if H(x // 8, (y - 8) // 4, 7) % 2 else "W2"
    return "SHD" if y < 27 else "F0"


def C_sc_floor(x, y, shade):
    """boards from wrecks, uneven widths, a nail head here and there"""
    widths = (5, 3, 4, 4)
    yy = y % 16
    acc, k = 0, 0
    while acc + widths[k % 4] <= yy:
        acc += widths[k % 4]
        k += 1
    if yy == acc + widths[k % 4] - 1:
        return "F0"
    if (x + k * 3) % 8 == 0 and yy == acc + 1:
        return "HI"
    tone = ("F1", "F2", "F3", "F2")[k % 4]
    if shade:
        tone = {"F3": "F2", "F2": "F1", "F1": "F0"}[tone]
    return tone


def C_sc_pencil(x, y):
    return "X" if (x + y) % 2 else "PI"


def C_sc_pod(K, x0, y0, x1, y1):
    """a barrel bound with iron hoops, a salvaged porthole in its side, the water inside it dark"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "M2")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if K.foot(x, y):
                stave = int((x - x0) / 4)
                t = (x - cx) / max(1, (x1 - x0) / 2)
                base = "M3" if t < -0.4 else ("M1" if t > 0.5 else "M2")
                K.px(x, y, "SHD" if (x - x0) % 4 == 0 and t > -0.6 else base)
    for yy in (y0 + 6, y0 + 7, y1 - 14, y1 - 13, y1 - 4, y1 - 3):
        for x in range(x0, x1 + 1):
            K.px(x, yy, "OUT" if yy in (y0 + 7, y1 - 13, y1 - 3) else "PI")
    ell(K, cx, y0 + 23, 8, 7, "G1")
    ell(K, cx - 1, y0 + 22, 5, 4, "G2")
    K.px(int(cx) - 3, y0 + 20, "G3")
    ell(K, cx, y0 + 23, 8, 7, "X", ring=1.4)
    for a in ((-7, 0), (7, 0), (0, -6), (0, 6)):
        K.px(int(cx + a[0]), int(y0 + 23 + a[1]), "XL")
    K.rim("OUT")


def C_sc_pipe(K):
    """a ribbed hose, patched with tape"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        K.hline(x0, x1, y, "G3" if t < .3 else ("G2" if t < .7 else "G1"))
    for x in range(x0, x1 + 1, 3):
        K.vline(x, y0, y1, "G1")
    K.rect(x0 + 20, y0, x0 + 25, y1, "PA")
    K.rim("OUT")


def C_sc_crate(K, x0, y0, x1, y1):
    """fish boxes, slatted, stencilled with a fish (no word)"""
    K.fn(lambda x, y: "C2")
    for y in range(y0, y1 + 1):
        r = (y - y0) % 16
        if r % 4 == 3:
            K.hline(x0, x1, y, "C1")
        if r == 15:
            K.hline(x0, x1, y, "OUT")
    for yb in range(y0, y1, 16):
        cx = (x0 + x1) // 2
        K.rect(cx - 3, yb + 5, cx + 2, yb + 7, "W1")
        K.px(cx + 3, yb + 5, "W1")
        K.px(cx + 3, yb + 7, "W1")


def C_lab_rig(K, x0, y0, x1, y1):
    """the SALVAGE RIG as it was found: a ship's binnacle and a radar housing bolted together, a slab clamped under
    a magnifier, a red lamp, a crank"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "R2")
    shade_by_light(K, "R3", "R2", "R1")
    for y in range(y0, y0 + 15):
        for x in range(x0, x1 + 1):
            if K.foot(x, y):
                K.px(x, y, "X" if (x - x0) % 5 else "R1")
    ell(K, cx, y0 + 8, 5, 4, "G2")
    ell(K, cx, y0 + 8, 5, 4, "OUT", ring=1)
    K.px(int(cx) - 2, y0 + 6, "G3")
    K.rect(x0 + 6, y0 + 17, x1 - 6, y0 + 23, "OUT")
    K.rect(x0 + 7, y0 + 18, x1 - 7, y0 + 22, "G1")
    for x in range(x0 + 8, x1 - 7, 3):
        K.px(x, y0 + 20, "L2")
    K.rect(x0 + 5, y0 + 16, x0 + 6, y0 + 24, "XL")
    K.rect(x1 - 6, y0 + 16, x1 - 5, y0 + 24, "XL")
    ell(K, x0 + 9, y0 + 29, 2.5, 2.5, "L1")
    K.px(x0 + 8, y0 + 28, "WHT")
    K.hline(x1 - 12, x1 - 6, y0 + 29, "XL")
    K.vline(x1 - 6, y0 + 27, y0 + 31, "XL")
    for x in range(x0 + 1, x1, 4):
        K.px(x, y1 - 2, "XL")
    K.rect(x0, y1 - 1, x1, y1, "R1")
    K.rim("OUT")


def C_lab_wall(K):
    """shelves of crates and jars from the yard, and tanks made of old aquariums, weed in the water"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            col = x // 8
            if col in (0, 3, 6):
                K.out[y][x] = "OUT" if x % 8 == 7 else ("C2" if x % 8 in (1, 2) else "C1")
            elif col in (1, 2):
                xx = x - 8
                r = y % 8
                if r == 7:
                    K.out[y][x] = "OUT"
                elif r == 6:
                    K.out[y][x] = "C3"
                else:
                    k = (xx // 4 + y // 8) % 4
                    K.out[y][x] = ("BK", "G2", "BK2", "X")[k] if xx % 4 != 3 else "SHD"
                    if k == 1 and r == 1:
                        K.out[y][x] = "G3"
            else:
                xx = x - 32
                if y < 2 or y >= 24:
                    K.out[y][x] = "C1" if y in (0, 24, 31) else "C2"
                elif xx in (0, 15):
                    K.out[y][x] = "OUT"
                else:
                    K.out[y][x] = "G1" if y > 16 else ("G2" if y > 5 else "G3")
                    if (xx in (4, 5) and y > 10 - (y % 3)) or (xx == 11 and y > 14):
                        K.out[y][x] = "BK2"
    K.rim("OUT")


def C_lab_stand(K, x0, y0, x1, y1, kind):
    """a crate for a stand; on it a brass ship's sextant (research) or a crystal set in a cigar box (THREE ISLAND)"""
    K.fn(lambda x, y: "S2")
    for y in range(y1 - 8, y1 + 1):
        K.hline(x0, x1, y, "S1" if (y - y1) % 3 == 0 else "S2")
    if kind == "scope":
        for y in range(y0 + 1, y0 + 13):
            for x in range(x0 + 2, x1 - 1):
                d = ((x - (x0 + x1) / 2) ** 2 + (y - (y0 + 12)) ** 2) ** .5
                if 9 <= d <= 11:
                    K.px(x, y, "X")
        K.vline((x0 + x1) // 2, y0 + 3, y0 + 12, "XL")
        K.px((x0 + x1) // 2, y0 + 3, "LM")
    else:
        K.rect(x0 + 2, y0 + 3, x1 - 2, y0 + 12, "D1")
        K.hline(x0 + 2, x1 - 2, y0 + 3, "D2")
        for x in range(x0 + 4, x1 - 3, 2):
            K.px(x, y0 + 7, "X")
        K.rect(x1 - 5, y0 + 1, x1 - 5, y0 + 6, "N1")


def C_lab_plate(K):
    """a strip of painted board, nailed up, blank"""
    x0, y0, x1, y1 = K.bbox()
    K.rect(x0 + 1, y1 - 6, x1 - 1, y1 - 2, "BOARD")
    K.hline(x0 + 1, x1 - 1, y1 - 6, "BOARD_L")
    K.px(x0 + 2, y1 - 4, "OUT")
    K.px(x1 - 2, y1 - 4, "OUT")


def C_lab_frame(K, x0, y0, x1, y1):
    """a frame of driftwood lashed at the corners"""
    K.fn(lambda x, y: "DRIFT")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = min(x - x0, x1 - x, y - y0, y1 - y)
            if d >= 3:
                K.px(x, y, "DRIFT_IN")
            elif (x - x0 < 3 or x1 - x < 3) and (y - y0 < 3 or y1 - y < 3):
                K.px(x, y, "ROPE")
    K.rim("OUT")


# ============================================================================================ the directions' colours
#  the primary rows' colours are fixed: these are targets, resolved to the nearest of the row(s) a tile sits in
PRIMARY_TARGETS = dict(WALL=(226, 214, 180), PLATE=(206, 160, 70), PLATE_L=(246, 214, 120), PLATE_W=(246, 246, 238),
                       PLATE_B=(80, 120, 200), BOARD=(150, 110, 70), BOARD_L=(200, 160, 110),
                       FRAME=(128, 86, 54), FRAME_L=(214, 166, 112), FRAME_IN=(240, 200, 90),
                       FRAME_W=(246, 246, 238), FRAME_IN_W=(200, 200, 200), DRIFT=(176, 166, 150),
                       DRIFT_IN=(130, 120, 110), ROPE=(214, 190, 140), GLASS_D=(150, 190, 220), GLASS_L=(230, 240, 246))

A = dict(
    name="A", title="THE WORKBENCH",
    lines=["The workrooms as makers keep them (batch 1's HEARTH and T-537's FOUNDRY STOCK carried in): oak and",
           "whitewash, a cork shadow-board for the tools, oak parts racks with wheels and tins, enamelled roadsters;",
           "HOLT's pods are copper diving bells on a ship's teak deck, a copper pipe between them with a green",
           "sight-glass; the lab's SALVAGE RIG is cast iron under a copper dome, a slab of old silicon on its bed."],
    mat={"*": dict(PRIMARY_TARGETS, OUT=(52, 40, 34), SHD=(92, 76, 64), MID=(150, 136, 120), HI=(206, 196, 178),
                   WHT=(246, 240, 226)),
         "bike": dict(F0=(110, 72, 46), F1=(160, 110, 70), F2=(196, 146, 96), W1=(150, 120, 90), W2=(206, 196, 176),
                      W3=(240, 234, 220), WT=(196, 160, 116), T1=(128, 86, 54), T2=(196, 150, 96), X=(200, 156, 70),
                      K1=(40, 74, 58), K2=(56, 112, 82), K3=(110, 170, 120), TY=(64, 56, 52), RM=(220, 220, 210),
                      SD=(140, 82, 48), B1=(70, 110, 76), B2=(96, 140, 96), XL=(240, 196, 100)),
         "sea": dict(F0=(90, 60, 40), F1=(140, 96, 62), F2=(176, 124, 80), F3=(210, 166, 116), W1=(122, 70, 46),
                     W2=(184, 112, 70), W3=(222, 152, 98), C1=(96, 60, 38), C2=(150, 96, 58), C3=(214, 166, 90),
                     M1=(130, 70, 44), M2=(184, 104, 64), M3=(230, 156, 104), G1=(30, 90, 80), G2=(60, 150, 120),
                     G3=(150, 220, 180), X=(196, 150, 70), XL=(244, 210, 120), PA=(240, 232, 210), PI=(90, 70, 54)),
         "lab": dict(C1=(96, 62, 40), C2=(150, 104, 66), C3=(204, 156, 104), G1=(120, 150, 160), G2=(180, 206, 210),
                     G3=(230, 240, 236), X=(196, 150, 70), XL=(244, 200, 110), BK=(150, 60, 50), BK2=(70, 100, 80),
                     S1=(110, 72, 46), S2=(160, 112, 70), S3=(206, 160, 108), D1=(70, 60, 56), D2=(130, 92, 60),
                     D3=(190, 140, 90), LM=(250, 200, 110), N1=(230, 220, 190), R1=(60, 60, 66), R2=(100, 100, 106),
                     R3=(150, 148, 150), L1=(250, 140, 60), L2=(140, 80, 50))},
    bk_post=A_bk_post, bk_upper=A_bk_upper, bk_board=A_bk_board, bk_foot=A_bk_foot, bk_floor=A_bk_floor,
    bk_rack=A_bk_rack, bk_box=A_bk_box, bk_tool=("MID", "X", "HI"),
    sc_pillar=A_sc_pillar, sc_wall=A_sc_wall, sc_floor=A_sc_floor, sc_pencil=A_sc_pencil, sc_pod=A_sc_pod,
    sc_pipe=A_sc_pipe, sc_crate=A_sc_crate,
    lab_rig=A_lab_rig, lab_wall=A_lab_wall, lab_stand=A_lab_stand, lab_platewall=A_lab_platewall,
    lab_plate=A_lab_plate, lab_frame=A_lab_frame,
)

B = dict(
    name="B", title="THE CLEAN ROOM",
    lines=["The workrooms as the institution keeps them (batch 1's WAYMARK, T-537's PORT'S FAMILY): white glazed",
           "tile, perforated steel, sealed floors; parts in bins with blank labels, bicycles in signal blue;",
           "HOLT's pods are glass bell jars on white plinths, one blue line of light running pod to pod; the",
           "lab's SALVAGE RIG is white enamel under a glass dome, a status strip, lockers and clean lit tanks."],
    mat={"*": dict(PRIMARY_TARGETS, OUT=(60, 64, 80), SHD=(110, 116, 132), MID=(164, 170, 182), HI=(214, 220, 228),
                   WHT=(250, 252, 252)),
         "bike": dict(F0=(160, 166, 176), F1=(206, 210, 216), F2=(236, 238, 240), W1=(150, 156, 168),
                      W2=(204, 208, 216), W3=(240, 242, 244), WT=(220, 224, 230), T1=(70, 120, 190),
                      T2=(230, 180, 60), X=(200, 80, 70), K1=(30, 70, 140), K2=(50, 110, 200), K3=(130, 180, 240),
                      TY=(60, 60, 70), RM=(230, 236, 240), SD=(70, 70, 80), B1=(50, 100, 180), B2=(110, 160, 220),
                      XL=(250, 200, 80)),
         "sea": dict(F0=(150, 164, 180), F1=(186, 200, 214), F2=(214, 226, 236), F3=(240, 246, 250),
                     W1=(80, 120, 190), W2=(200, 210, 220), W3=(238, 242, 246), C1=(140, 150, 164), C2=(200, 206, 214),
                     C3=(240, 242, 246), M1=(120, 128, 140), M2=(190, 196, 206), M3=(244, 246, 248),
                     G1=(110, 160, 210), G2=(170, 210, 240), G3=(226, 242, 252), X=(80, 120, 190), XL=(120, 220, 255),
                     PA=(250, 250, 246), PI=(80, 120, 190)),
         "lab": dict(C1=(150, 156, 168), C2=(204, 208, 216), C3=(240, 242, 244), G1=(100, 150, 200),
                     G2=(160, 204, 236), G3=(220, 240, 252), X=(80, 120, 190), XL=(120, 220, 255), BK=(80, 120, 190),
                     BK2=(160, 170, 180), S1=(150, 156, 168), S2=(204, 208, 216), S3=(236, 238, 242),
                     D1=(110, 116, 128), D2=(170, 176, 186), D3=(220, 224, 230), LM=(120, 230, 160),
                     N1=(40, 56, 70), R1=(160, 166, 178), R2=(214, 218, 226), R3=(246, 248, 250), L1=(120, 230, 160),
                     L2=(250, 200, 80))},
    bk_post=B_bk_post, bk_upper=B_bk_upper, bk_board=B_bk_board, bk_foot=B_bk_foot, bk_floor=B_bk_floor,
    bk_rack=B_bk_rack, bk_box=B_bk_box, bk_tool=("SHD", "MID", "WHT"),
    sc_pillar=B_sc_pillar, sc_wall=B_sc_wall, sc_floor=B_sc_floor, sc_pencil=B_sc_pencil, sc_pod=B_sc_pod,
    sc_pipe=B_sc_pipe, sc_crate=B_sc_crate,
    lab_rig=B_lab_rig, lab_wall=B_lab_wall, lab_stand=B_lab_stand, lab_platewall=A_lab_platewall,
    lab_plate=B_lab_plate, lab_frame=B_lab_frame,
)

C = dict(
    name="C", title="THE SALVAGE YARD",
    lines=["The workrooms built from what the sea and the dumps gave up (SALVAGER, 2.x: the ruins are dead hardware):",
           "corrugated sheet and crate planks, a pallet for a rack, concrete, bicycles in rust-red; HOLT's pods are",
           "hooped barrels with a salvaged porthole, a patched hose between them, fish boxes and driftwood; the",
           "lab's SALVAGE RIG is a binnacle and a radar housing bolted together, a slab clamped under its glass."],
    mat={"*": dict(PRIMARY_TARGETS, OUT=(44, 40, 40), SHD=(86, 80, 76), MID=(140, 132, 124), HI=(196, 190, 180),
                   WHT=(236, 232, 222)),
         "bike": dict(F0=(100, 100, 98), F1=(140, 140, 136), F2=(170, 168, 162), W1=(110, 116, 120),
                      W2=(150, 156, 158), W3=(190, 196, 196), WT=(200, 170, 120), T1=(130, 100, 70),
                      T2=(170, 136, 96), X=(170, 90, 50), K1=(110, 40, 30), K2=(170, 70, 50), K3=(220, 130, 100),
                      TY=(56, 52, 50), RM=(200, 196, 186), SD=(100, 70, 50), B1=(90, 100, 60), B2=(130, 140, 90),
                      XL=(220, 150, 80)),
         "sea": dict(F0=(70, 60, 54), F1=(120, 104, 90), F2=(160, 142, 120), F3=(196, 180, 156), W1=(110, 130, 140),
                     W2=(150, 170, 176), W3=(196, 206, 200), C1=(110, 90, 70), C2=(160, 140, 110), C3=(214, 196, 150),
                     M1=(90, 66, 50), M2=(140, 104, 74), M3=(186, 146, 104), G1=(30, 60, 70), G2=(60, 110, 120),
                     G3=(150, 200, 196), X=(180, 140, 70), XL=(230, 200, 120), PA=(220, 200, 150), PI=(70, 64, 60)),
         "lab": dict(C1=(100, 80, 60), C2=(150, 126, 96), C3=(200, 180, 140), G1=(40, 80, 80), G2=(80, 130, 120),
                     G3=(170, 210, 196), X=(180, 140, 70), XL=(230, 200, 120), BK=(150, 70, 50), BK2=(90, 140, 70),
                     S1=(110, 86, 60), S2=(160, 130, 96), S3=(200, 176, 136), D1=(90, 60, 44), D2=(140, 100, 70),
                     D3=(200, 160, 110), LM=(250, 220, 140), N1=(140, 140, 150), R1=(70, 76, 80), R2=(110, 120, 120),
                     R3=(160, 170, 166), L1=(230, 70, 50), L2=(250, 200, 80))},
    bk_post=C_bk_post, bk_upper=C_bk_upper, bk_board=C_bk_board, bk_foot=C_bk_foot, bk_floor=C_bk_floor,
    bk_rack=C_bk_rack, bk_box=C_bk_box, bk_tool=("SHD", "X", "MID"),
    sc_pillar=C_sc_pillar, sc_wall=C_sc_wall, sc_floor=C_sc_floor, sc_pencil=C_sc_pencil, sc_pod=C_sc_pod,
    sc_pipe=C_sc_pipe, sc_crate=C_sc_crate,
    lab_rig=C_lab_rig, lab_wall=C_lab_wall, lab_stand=C_lab_stand, lab_platewall=A_lab_platewall,
    lab_plate=C_lab_plate, lab_frame=C_lab_frame,
)

STYLES = {"A": A, "B": B, "C": C}


# ============================================================================================ sheets
BG, INK, RED, SOFT = (250, 248, 242), (24, 24, 24), (120, 20, 30), (90, 90, 90)
ROOMS = [("CeruleanCity_BikeShop", "the bike shop"), ("Route25_SeaCottage", "HOLT's SEA COTTAGE"),
         ("CinnabarIsland_PokemonLab_ExperimentRoom", "the lab: the SALVAGE RIG"),
         ("CinnabarIsland_PokemonLab_ResearchRoom", "the lab: research"),
         ("CinnabarIsland_PokemonLab_Entrance", "the lab: lobby, plates, the founder"),
         ("ThreeIsland_House1", "THREE ISLAND's house")]
DETAILS = [("CeruleanCity_BikeShop", (0, 1, 7, 7), "the racks, the bicycles"),
           ("Route25_SeaCottage", (2, 0, 13, 4), "the SEPARATION SYSTEM"),
           ("CinnabarIsland_PokemonLab_ExperimentRoom", (3, 0, 15, 5), "the cabinets, the SALVAGE RIG"),
           ("CinnabarIsland_PokemonLab_Entrance", (3, 0, 7, 3), "the founder's frame")]


def text(d, xy, s, fill=INK):
    d.text(xy, s, fill=fill)


def state_of(sets):
    return (sets, None) if sets else None


def contact_sheets(out_dir, states):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: Nintendo's tiles in the workrooms (the walls and floors primary/building",
                              "draws in the lab, and all the furniture batch D and T-537 drew, are already ours)"])}
    for k in STYLES:
        titles[k] = ("%s %s" % (k, STYLES[k]["title"]), STYLES[k]["lines"])
    pad = 10
    paths = []
    for hi, rooms in enumerate([ROOMS[:3], ROOMS[3:]]):
        blocks = []
        for k in names:
            ims = [G.render_map(m, state_of(states[k])) for m, _ in rooms]
            t, lines = titles[k]
            th = 8 + 12 * len(lines) + 16
            W = sum(i.width for i in ims) + pad * (len(ims) + 1)
            im = Image.new("RGB", (max(W, 760), th + max(i.height for i in ims) + pad), BG)
            d = ImageDraw.Draw(im)
            text(d, (pad, 6), t, RED)
            for j, s in enumerate(lines):
                text(d, (pad + 150, 6 + 12 * j), s)
            x = pad
            for i, (m, cap) in zip(ims, rooms):
                text(d, (x, th - 13), cap, SOFT)
                im.paste(i, (x, th))
                x += i.width + pad
            blocks.append(im)
        W = max(b.width for b in blocks)
        sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
        d = ImageDraw.Draw(sh)
        text(d, (pad, 8), "T-538 DRAFT, batch 2 -- the workrooms, real rooms at 1x, three directions beside today's "
                          "(redrawn in place: no block, collision or palette row moves). (%d/2)" % (hi + 1), INK)
        y = 30
        for b in blocks:
            sh.paste(b, (0, y))
            y += b.height
        p = os.path.join(out_dir, "t538b2_rooms_1x_%d.png" % (hi + 1))
        sh.save(p)
        paths.append(p)
    #  3x details
    rowsim = []
    for k in names:
        crops = []
        for m, (x0, y0, x1, y1), cap in DETAILS:
            im = G.render_map(m, state_of(states[k])).crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
            crops.append((im.resize((im.width * 3, im.height * 3), Image.NEAREST), cap))
        rowsim.append((k, crops))
    #  two rows of details per state: the first two, then the last two
    pages = []
    for part in ((0, 1), (2, 3)):
        cw = sum(rowsim[0][1][i][0].width for i in part) + pad * 3 + 130
        ch = max(rowsim[0][1][i][0].height for i in part) + 24
        det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
        d = ImageDraw.Draw(det)
        text(d, (pad, 8), "T-538 DRAFT, batch 2 -- details at 3x: %s." % ", ".join(DETAILS[i][2] for i in part), INK)
        y = 30
        for k, crops in rowsim:
            text(d, (pad, y + 6), titles[k][0], RED)
            x = 130
            for i in part:
                c, cap = crops[i]
                text(d, (x, y + 2), cap, SOFT)
                det.paste(c, (x, y + 16))
                x += c.width + pad
            y += ch
        p = os.path.join(out_dir, "t538b2_detail_3x_%d.png" % (len(pages) + 1))
        det.save(p)
        pages.append(p)
    paths += pages
    #  the tiles at 3x, each set in its home rows, per state
    cols = []
    for k in names:
        sets = states[k]
        imgs = []
        for key, S in SETS.items():
            tiles, pals = sets[key] if sets else (S.cur, {r: read_pal(os.path.join(GBA, S.dir, "palettes/%02d.pal" % r))
                                                          for r in range(16)})
            n = (S.nvan + 15) // 16
            im = Image.new("RGB", (128, n * 8), (236, 236, 236))
            o = im.load()
            for t in range(S.nvan):
                if t not in S.use:
                    continue
                r = S.home(t)
                pal = pals[r] if r >= 7 else G.PPAL[r]
                for q in range(64):
                    vv = tiles[t][q]
                    o[(t % 16) * 8 + q % 8, (t // 16) * 8 + q // 8] = pal[vv] if vv else (200, 200, 200)
            imgs.append((S.dir.split("/")[-1], im))
        hh = sum(i.height * 3 + 16 for _, i in imgs)
        col = Image.new("RGB", (384, hh), BG)
        y = 0
        dd = ImageDraw.Draw(col)
        for lab, i in imgs:
            dd.text((0, y), lab, fill=SOFT)
            col.paste(i.resize((384, i.height * 3), Image.NEAREST), (0, y + 14))
            y += i.height * 3 + 16
        cols.append((titles[k][0], col))
    W = sum(c.width + pad for _, c in cols) + pad
    sh = Image.new("RGB", (W, max(c.height for _, c in cols) + 50), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 6), "T-538 DRAFT, batch 2 -- the tiles at 3x, each in its home row (grey: transparent; light grey "
                      "cells: unused, left as they are)", INK)
    x = pad
    for t, c in cols:
        text(d, (x, 26), t, RED)
        sh.paste(c, (x, 42))
        x += c.width + pad
    p = os.path.join(out_dir, "t538b2_tiles_3x.png")
    sh.save(p)
    paths.append(p)
    return paths


# ============================================================================================ report
def report():
    print("T-538 batch 2 -- the workrooms (bike shop, SEA COTTAGE, the QUICKSILVER lab)\n")
    owner = {}
    for key, setkey, layout, painter, what in GROUPS:
        for r in layout:
            for s in r:
                if s is not None:
                    t = s if isinstance(s, int) else s[0]
                    owner.setdefault((setkey, t), key)
    print("  %-12s %-5s %5s %6s %4s  %s" % ("group", "set", "tiles", "draws", "maps", "what"))
    for key, setkey, layout, painter, what in GROUPS:
        S = SETS[setkey]
        ts = sorted(t for (sk, t), k in owner.items() if k == key and t in S.use and t < S.nvan)
        draws = sum(S.use[t]["n"] for t in ts)
        maps = {m for t in ts for m in S.use[t]["maps"]}
        print("  %-12s %-5s %5d %6d %4d  %s" % (key, setkey, len(ts), draws, len(maps), what))
    bad = 0
    for key, S in SETS.items():
        mine = {t for (sk, t) in owner if sk == key}
        used = {t for t in S.use if t < S.nvan and any(S.cur[t])}
        stray = sorted(t for t in used if t not in mine)
        rows = sorted({r for t in used for r in S.use[t]["rows"]})
        foreign = sorted(r for r in rows if r >= 7 and r not in S.rows)
        print("  %s: %d placed tiles, %d in a group; in no group: %s; rows placed %s, own rows %s%s"
              % (S.dir.split("/")[-1], len(used), len(used & mine), stray or "none", rows, S.rows,
                 ("; !! placed in a row this tool does not own: %s" % foreign) if foreign else ""))
        bad |= bool(stray) or bool(foreign)
    #  rows a primary tile is placed in, inside these rooms: none may be one we recolour
    for key, S in SETS.items():
        hits = collections.Counter()
        for l in G.LAYOUTS:
            if l.get("secondary_tileset") != S.sym or not G.MBL.get(l["id"]):
                continue
            bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
            for k in range(0, len(bd) - 1, 2):
                m = struct.unpack_from("<H", bd, k)[0] & 0x3FF
                buf, mm = (G.PMT, m) if m < 640 else (S.mt, m - 640)
                if (mm + 1) * 16 > len(buf):
                    continue
                for e in struct.unpack_from("<8H", buf, mm * 16):
                    if (e & 0x3FF) < 640 and (e & 0x3FF) and (e >> 12) in S.rows:
                        hits[e >> 12] += 1
        if hits:
            print("  !! %s: primary tiles placed in its own rows %s -- recolouring them would repaint primary art"
                  % (S.dir.split("/")[-1], dict(hits)))
            bad = 1
    print("  no primary tile is placed in a row this batch recolours")
    print("  the founder's photo (lab 10 11 26 27, gbafounder.py): its 110 pixels copied through; the frame is ours")
    for key, S in SETS.items():
        print("  %s: animation %s; scripted blocks: none (setmetatile never names this set)"
              % (S.dir.split("/")[-1], G._field(S.sym, "callback")))
    return bad


def check_engine():
    """T-446's rule: with one direction approved, the engine must be exactly what `--write --approved --pick X` makes
    (every tile of each set this tool writes, its own rows); exit 1 on a difference"""
    pick = next(iter(APPROVED))
    D = STYLES[pick]
    res = draw(D)
    sets = res[0]
    bad = 0
    for key, S in SETS.items():
        off = [t for t in range(len(S.cur)) if sets[key][0][t] != S.cur[t]]
        rows = [r for r in S.rows
                if [tuple(c) for c in sets[key][1][r]] != [tuple(c) for c in read_pal(os.path.join(GBA, S.dir, "palettes/%02d.pal" % r))]]
        if off or rows:
            print("  !! %s: the engine differs from `--write --approved --pick %s` in tiles %s rows %s -- find which side "
                  "is right" % (S.dir.split("/")[-1], pick, off[:12], rows))
            bad = 1
    if not bad:
        print("  the engine matches `--write --approved --pick %s` (the user, 2026-11-10)" % pick)
    return bad


def main():
    if WRITE:
        if "--approved" not in ARGS or not PICK or PICK not in APPROVED:
            print("  --write refused: T-538 batch 2 is a draft. APPROVED is %s; the user picks a direction first, it "
                  "goes into APPROVED,\n  then --write --approved --pick X writes bike_shop's, sea_cottage's and "
                  "lab's tiles and own rows (never a primary palette)." % (sorted(APPROVED) or "empty"))
            return 1
        sets, owner = draw(STYLES[PICK])
        for key, S in SETS.items():
            G.save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[key][0], os.path.join(GBA, S.dir, "tiles.png"))
            for r in S.rows:
                write_pal(os.path.join(GBA, S.dir, "palettes", "%02d.pal" % r), sets[key][1][r])
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
            for key, S in SETS.items():
                dd = os.path.join(DRAFT, k, S.dir.split("/")[-1])
                os.makedirs(os.path.join(dd, "palettes"), exist_ok=True)
                G.save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[key][0], os.path.join(dd, "tiles.png"))
                for r in S.rows:
                    write_pal(os.path.join(dd, "palettes", "%02d.pal" % r), sets[key][1][r])
            states[k] = sets
            ch = sum(1 for (sk, t) in owner if sets[sk][0][t] != SETS[sk].van[t])
            summary[k] = dict(title=D["title"], tiles_redrawn=ch, new_tiles=0,
                              rows={"%s %d" % (S.dir.split("/")[-1], r): sets[key][1][r]
                                    for key, S in SETS.items() for r in S.rows})
            print("  %s %-17s %d tiles redrawn, 0 new tiles; rows recoloured: bike_shop 7/8, sea_cottage 8/9, lab "
                  "7/8/12; primary rows untouched" % (k, D["title"], ch))
        json.dump(dict(ticket="T-538", batch=2, status="DRAFT -- not in the engine", approved=sorted(APPROVED),
                       directions=summary), open(os.path.join(DRAFT, "directions.json"), "w"), indent=1)
        for p in contact_sheets(DRAFT, states):
            print("  sheet:", p)
    if len(APPROVED) == 1:
        bad = check_engine() or bad
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

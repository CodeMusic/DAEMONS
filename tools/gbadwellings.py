#!/usr/bin/env python3
"""The rest of the interiors, batch 3: the fan club and the day cares, the burgled house, and THE TUNNEL's last vanilla
pieces -- redrawn in place in our own hand (T-538).

    python3 tools/gbadwellings.py                   # report: batch 3's census and its objects, what is left vanilla
                                                    #   and why, and the other tools' claims on these tilesets
    python3 tools/gbadwellings.py --draft [DIR]     # the three directions (A, B, C) drawn in full: per direction each
                                                    #   secondary's tiles.png and own rows as .pal, and the contact
                                                    #   sheets (gfx/drafts/t538_b3/)
    python3 tools/gbadwellings.py --write --approved --pick A
                                                    # into the engine -- refused unless X is in APPROVED ({"A"}: the
                                                    #   user, 2026-11-10, A The keeping); the report exits 1 when the
                                                    #   engine is not what that write makes

THE ANSWER IT FOLLOWS (the user, 2026-11-10, "Other interiors", census item 6; "rest of interiors" for batch 3).
gbahomes.py split the job into batches; batch 1 (gbahomes, A HEARTH) and batch 2 (gbaworkrooms.py, A THE WORKBENCH)
are built. This is batch 3:

  fan_club_daycare   one tileset, four rooms: ARDOR's fan club (the ENTHUSIASTS' parlour: "Won't you admire my
                     SPIKE's adorable tail?"), the two DAY-CAREs (ROUTE 5's and FOUR ISLAND's: someone keeps your
                     daemon running while you are away), and INIT's house in HALFTONE ("He looks after DAEMONS nobody
                     came back for" -- the orphan process reparented to init, vision 4.x ORPHAN). Its walls, floors,
                     the lawn and its low wall, the sofa and armchairs, the table, the stools, the rug, the windows and
                     the glass cases. Own rows 8, 9 and 10, recoloured.
  burgled_house      DOLDRUM's burgled house: TEAM CORPUS "did not use the door" -- the hole they dug through the wall,
                     the ransacked kitchen and shelf, the chairs knocked over, the things strewn, the plant tipped, and
                     the LOOTER's tracks across the floor. Every tile sits in a PRIMARY row (0, 2, 4, 5), whose
                     colours are batch D's and fixed: it is redrawn in those colours. The fable (actors are animals):
                     the tracks are PAW prints.
  underground_path   THE TUNNEL (vision 3.2: "The Underground Path is already correct"). gbacaves.py (T-438 batch E,
                     approved 2026-10-23) owns its rows 7 and 8 -- THE TUNNEL's palette -- and nine tiles: the wall
                     faces with their conduits (1 17 33 35) and the lane with the PACKET TRACE (26 39 40 42 43). The
                     rest is vanilla's drawing in THE TUNNEL's colours: the floor's rings, the lit lane, the wall ends
                     and corners, the two stairs, the ceiling lamps. Those are redrawn here, in gbacaves' colours
                     (never its rows), and gbacaves' --write keeps them (its T538_TUNNEL).

NOT HERE: everything primary/building places in these rooms (batch D's: the plants, the bookcases, the PC, the
counters, the frames, the burgled house's table and rug); THE READING ROOM (gbainterior.py: it reads only
fan_club_daycare's LAYOUT, never a pixel, so nothing here moves it); THE TUNNEL's palette and nine tiles (gbacaves).

THE RULES ARE gbahomes.py's (batch D's): redrawn IN PLACE. No block, layer, flip, palette row, behaviour or
collision bit moves and no map is touched; only pixels inside tiles change, and every tile keeps its FOOTPRINT (a
transparent pixel stays transparent, a drawn one stays drawn). Primary rows 0..6 never change colour; gbacaves' rows
never change colour. Only fan_club_daycare's own rows 8, 9 and 10 are recoloured. None of the three has an
animation; no script or engine constant names a block in any of them (setmetatile is never used in these maps;
METATILE_SeviiIslands45_DayCareDoor is an outdoor tileset's).

Every in-game word: none. This is art.
"""
import collections, contextlib, io, json, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import write_pal, read_pal
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t538_b3")
#  The user's pick goes here ("A", "B" or "C"); --write refuses anything not in it.
APPROVED = {"A"}                     # the user, 2026-11-10: A The keeping

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

#  gbahomes (and gbabuilding under it) and gbacaves read their switches off sys.argv at import (engine.md trap 16)
_argv, sys.argv = sys.argv, ["gbahomes"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import gbahomes as G
        import gbacaves as GC
finally:
    sys.argv = _argv

Cv, H, M, h, v, hv = G.Cv, G.H, G.M, G.h, G.v, G.hv

FAN = G.Set("fan", "gTileset_FanClubDaycare", [8, 9, 10])
BURG = G.Set("burg", "gTileset_BurgledHouse", [])
TUN = G.Set("tun", "gTileset_UndergroundPath", [])
SETS = {"fan": FAN, "burg": BURG, "tun": TUN}
G.SETS.update(SETS)          # Cv and render_map look sets up there
#  rows another tool owns, drawn in but never written: THE TUNNEL's (gbacaves.py, T-438 batch E)
FIXED = {"tun": [7, 8]}
#  vanilla's primary/building rows 0..6: what a secondary tile placed in a primary row was drawn against
VPRI = [G.jasc(daemonslib.upstream(GBA, G.PRI + "/palettes/%02d.pal" % r, binary=True)) for r in range(7)]
FIXED_PAL = {(k, r): read_pal(os.path.join(GBA, SETS[k].dir, "palettes/%02d.pal" % r)) for k, rs in FIXED.items()
             for r in rs}


# ============================================================================================ drawing helpers
def ell(K, cx, cy, rx, ry, m, ring=None):
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            d = ((x - cx) / max(rx, .5)) ** 2 + ((y - cy) / max(ry, .5)) ** 2
            if d <= 1 and (ring is None or d >= ((rx - ring) / max(rx, .5)) ** 2):
                K.px(x, y, m)


def vcol(K, x, y):
    """vanilla's colour at a canvas pixel, in the row its tile is placed in; None off the footprint"""
    vv = K.vi(x, y)
    if vv is None:
        return None
    S = SETS[K.setkey]
    r = S.home(K.layout[y // 8][x // 8][0])
    return tuple(S.vpal[r][vv] if r >= 7 else VPRI[r][vv])


def vlum(K, x, y):
    """vanilla's brightness at a canvas pixel (0..255)"""
    c = vcol(K, x, y)
    return None if c is None else (c[0] * 3 + c[1] * 6 + c[2]) / 10


def vrank(K, ramp):
    """vanilla's light kept as LIGHTING only, ranked over this canvas: each pixel -> one of RAMP (dark..light). Used
    for silhouettes thinner than a pattern (a toppled chair's leg, a spilt book), where the light is what is drawn."""
    lums = sorted({vlum(K, x, y) for y in range(K.h) for x in range(K.w) if K.foot(x, y)})
    if not lums:
        return
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                k = lums.index(vlum(K, x, y))
                K.out[y][x] = ramp[min(len(ramp) - 1, k * len(ramp) // len(lums))]


def zone(K, x, y, cuts):
    """which of len(cuts)+1 bands vanilla's brightness puts this pixel in (0 darkest)"""
    l = vlum(K, x, y)
    return sum(1 for c in cuts if l is not None and l > c)


# ============================================================================================ painters: fan club & day cares
def p_fc_wall(K, D):
    """the fan club's back wall: the upper wall (0..15), a rail (16..17), the dado (18..27), the skirting (28..31); the
    end columns are the side wall's return, a pilaster"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            end = x < 3 or x >= K.w - 3
            if end:
                xx = x if x < 3 else K.w - 1 - x
                K.out[y][x] = "OUT" if xx == 2 else ("T2" if xx == 0 else "T1")
            elif y < 16:
                K.out[y][x] = D["fc_upper"](x, y)
            elif y < 18:
                K.out[y][x] = "T2" if y == 16 else "OUT"
            elif y < 28:
                K.out[y][x] = D["fc_dado"](x, y - 18)
            else:
                K.out[y][x] = "SHD" if y < 30 else "OUT"


def p_fc_floor(K, D, shade=False):
    """the fan club's floor: one 8x8 tile mirrored four ways makes the 16x16 square vanilla laid"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = D["fc_floor"](x % 16 if x % 16 < 8 else 15 - x % 16,
                                            y % 16 if y % 16 < 8 else 15 - y % 16, shade)
    if shade:
        #  the wall's shadow on the floor: vanilla's darkest band, kept where it falls
        for y in range(K.h):
            for x in range(K.w):
                if K.foot(x, y) and zone(K, x, y, [150]) == 0:
                    K.out[y][x] = "SHD"


def p_fc_floor_lit(K, D):
    p_fc_floor(K, D, False)


def p_fc_floor_shade(K, D):
    p_fc_floor(K, D, True)


def upholster(K, D):
    """a sofa or an armchair: vanilla's light as the form (back, arms, seat), the direction's cloth and its making"""
    vrank(K, ["OUT", "U1", "U1", "U2", "U2", "U3"])
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y) or K.out[y][x] == "OUT":
                continue
            m = D["fc_cloth"](x, y, K.out[y][x])
            if m:
                K.out[y][x] = m
    #  the feet: the bottom two drawn rows
    for y in (y1 - 1, y1):
        for x in range(x0, x1 + 1):
            if K.foot(x, y) and K.out[y][x] != "OUT":
                K.px(x, y, "T1")
    K.rim("OUT")


def p_fc_table(K, D):
    """the table: its top, the cloth or the finish, the apron and the legs (the bottom five drawn rows)"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y >= y1 - 5:
                leg = x < x0 + 3 or x > x1 - 3
                K.out[y][x] = ("T1" if leg else "OUT") if y > y1 - 3 else ("T1" if y == y1 - 5 else "T2")
            else:
                K.out[y][x] = D["fc_top"](x - x0, y - y0, x1 - x0, y1 - 5 - y0)
    K.rim("OUT")


def p_dc_wall(K, D):
    """the day cares' wall (and INIT's): a frieze (0..5), the wall (6..23), the skirting (24..31, row 9); the end
    columns are the side wall's return"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            end = x < 3 or x >= K.w - 3
            if end:
                xx = x if x < 3 else K.w - 1 - x
                K.out[y][x] = "OUT" if xx == 2 else ("V3" if xx == 0 else "V2")
            elif y < 24:
                K.out[y][x] = D["dc_upper"](x, y)
            else:
                K.out[y][x] = "T2" if y == 24 else ("OUT" if y in (25, 31) else ("SHD" if y == 30 else "T1"))


def p_dc_window(K, D):
    """a window: what hangs at its head, the glass, the sill"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = D["dc_window"](x, y)
    K.rim("OUT")


def p_dc_floor(K, D, shade=False):
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = D["dc_floor"](x % 8, y % 8, shade)
    if shade:
        for y in range(K.h):
            for x in range(K.w):
                if K.foot(x, y) and zone(K, x, y, [170]) == 0:
                    K.out[y][x] = "SHD"


def p_dc_floor_lit(K, D):
    p_dc_floor(K, D, False)


def p_dc_floor_shade(K, D):
    p_dc_floor(K, D, True)


def p_dc_lawn(K, D):
    """the lawn the daemons play on (row 10): vanilla's shaded top rows stay the wall's shadow"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = D["dc_lawn"](x % 8, y % 8, zone(K, x, y, [120]) == 0)


def p_dc_lowwall(K, D):
    """the low wall between the floor and the lawn, its end, its corner, the gate post: vanilla's top-lit / front-
    shaded zones as geometry, the direction's making on them"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                z = zone(K, x, y, [90, 150, 190])
                K.out[y][x] = D["dc_lowwall"](x % 8, y, z)
    K.rim("OUT")


def p_dc_stool(K, D):
    """a stool, seen from above and the south: a seat, its front, its legs"""
    x0, y0, x1, y1 = K.bbox()
    D["dc_stool"](K, x0, y0, x1, y1)
    K.rim("OUT")


def p_rug(K, D):
    """the rug under the table: field, then the border (a 6px band all round the canvas -- the rug grows by repeating
    its edge tiles, so the border is drawn in tile coordinates)"""
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            ex = min(x, K.w - 1 - x)
            ey = min(y, K.h - 1 - y)
            e = min(ex if ex < 8 else 99, ey if ey < 8 else 99)
            K.out[y][x] = D["rug"](x % 8, y % 8, e)


def p_case(K, D):
    """the glass case on its cabinet (cases 72..79): in every one of the four rooms"""
    x0, y0, x1, y1 = K.bbox()
    D["case"](K, x0, y0, x1, y1)
    K.rim("OUT")


# ============================================================================================ painters: the burgled house
def p_bh_hole(K, D):
    """the wall round the hole TEAM CORPUS dug (row 4): the wall's head (0..3), the wall, the hole's rim, the rubble at
    its foot. The arch itself is vanilla's footprint: its inside shows the dark tiles behind."""
    x0, y0, x1, y1 = K.bbox()
    #  the rim: drawn pixels next to the arch's hole (inside the bbox, not the canvas edge)
    def near_hole(x, y, r):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                xx, yy = x + dx, y + dy
                if 0 <= xx < K.w and 0 <= yy < K.h and y0 + 4 <= yy and (K.hole[yy][xx] or K.van[yy][xx] == 0):
                    if x0 < xx < x1:
                        return True
        return False
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            if y < 4:
                K.out[y][x] = "head_l" if y < 2 else ("head" if y == 2 else "OUT")
            elif y >= y1 - 6 and (x < x0 + 6 or x > x1 - 6):
                K.out[y][x] = D["bh_rubble"](x, y)
            elif near_hole(x, y, 1):
                K.out[y][x] = "rim_d"
            elif near_hole(x, y, 3):
                K.out[y][x] = D["bh_rim"](x, y)
            else:
                K.out[y][x] = D["bh_wall"](x, y)


def p_bh_dark(K, D):
    """the dark inside the hole (2 3 in row 5, 18 19 in row 4): what is behind the wall"""
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = D["bh_dark"](x, y)


def p_bh_kitchen(K, D):
    """the kitchen dresser, ransacked: the top, the doors or drawers pulled open (vanilla's glass, now the gap)"""
    x0, y0, x1, y1 = K.bbox()
    D["bh_kitchen"](K, x0, y0, x1, y1)
    K.rim("OUT")


def p_bh_shelf(K, D):
    """the shelf by the wall, emptied: what was left on it, and the posts"""
    x0, y0, x1, y1 = K.bbox()
    D["bh_shelf"](K, x0, y0, x1, y1)
    K.rim("OUT")


def p_bh_furniture(K, D):
    """a chair or a stool knocked over, the tall chair: vanilla's silhouette and light, the direction's timber and
    cloth (thin, so the light is what is drawn)"""
    vrank(K, ["OUT", "wood_d", "wood", "wood", "wood_l", "cloth", "cloth_l"])
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y) and K.out[y][x] in ("wood", "wood_l") and D["grain"](x, y):
                K.out[y][x] = "wood_d"
    K.rim("OUT")


def p_bh_strewn(K, D):
    """what was pulled off the shelf and the desk: books, a paper, a framed picture face down. Each keeps vanilla's
    silhouette; its colour is told by what it is, not by vanilla's hue"""
    for y in range(K.h):
        for x in range(K.w):
            c = vcol(K, x, y)
            if c is None:
                continue
            r, g, b = c
            l = (r * 3 + g * 6 + b) / 10
            sat = max(c) - min(c)
            if l < 80:
                m = "OUT"
            elif l > 215 and sat < 40:
                m = "paper"
            elif sat < 30:
                m = "wood_d" if l < 140 else "paper_d"
            elif r > b + 30:
                m = "book_l" if l > 150 else "book"
            elif g > r + 10:
                m = "cloth"
            else:
                m = "cloth_l" if l > 150 else "wood"
            K.out[y][x] = m
    K.rim("OUT")


def p_bh_plant(K, D):
    """the plant knocked off its stand, its pot on its side, the soil spilt: vanilla's green stays the leaves (in the
    direction's greens), the rest is the pot and the soil"""
    vrank(K, ["OUT", "soil", "pot_d", "pot", "pot_l", "paper"])
    for y in range(K.h):
        for x in range(K.w):
            c = vcol(K, x, y)
            if c is not None and c[1] > c[0] + 20 and c[1] > c[2]:
                K.out[y][x] = "leaf_l" if c[1] > 170 else ("leaf" if c[1] > 120 else "leaf_d")
    K.rim("OUT")


def p_bh_tracks(K, D):
    """the LOOTER's tracks: the floor is batch D's floor tile under them, exactly (594, or 595 in the room's back
    row), and over it each of vanilla's prints becomes a PAW print -- a pad and four toes -- in the direction's mud"""
    t0 = K.layout[0][0][0] if K.layout[0][0] else None
    base = None
    for ty, r in enumerate(K.layout):
        for tx, spec in enumerate(r):
            t, fl = spec
            vt = BURG.van[t]
            pt = max((594, 595), key=lambda p: sum(a == b for a, b in zip(vt, G.GB.VAN[p])))
            van_base, now_base = G.GB.VAN[pt], G.PTILES_NOW[pt]
            for k in range(64):
                x, y = k % 8, k // 8
                sx = 7 - x if "h" in fl else x
                sy = 7 - y if "v" in fl else y
                X, Y = tx * 8 + x, ty * 8 + y
                K.out[Y][X] = "@5:%d" % now_base[sy * 8 + sx]
                K.__dict__.setdefault("print_mask", set())
                c = VPRI[5][vt[sy * 8 + sx]]
                if vt[sy * 8 + sx] != van_base[sy * 8 + sx] and max(c) - min(c) < 24 and sum(c) < 450:
                    K.print_mask.add((X, Y))
    #  vanilla's prints -> blobs -> one paw at each blob's middle
    seen, blobs = set(), []
    for p in sorted(K.print_mask):
        if p in seen:
            continue
        st, blob = [p], []
        seen.add(p)
        while st:
            q = st.pop()
            blob.append(q)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (q[0] + dx, q[1] + dy)
                if n in K.print_mask and n not in seen:
                    seen.add(n)
                    st.append(n)
        if len(blob) >= 6:
            blobs.append(blob)
    for blob in blobs:
        cx = round(sum(p[0] for p in blob) / len(blob))
        cy = round(sum(p[1] for p in blob) / len(blob))
        D["paw"](K, cx, cy)


# ============================================================================================ painters: THE TUNNEL
#  THE TUNNEL's row 7 (gbacaves' roles): 1 outline, 2 3 5 6 the walls (dark..lit), 7 8 9 the floor (body, lit edge,
#  joint), 10 11 12 the lit lane, 13..15 the trace's lane, 4 the trace's blue. Row 8: 1..3 the walls, 4..8 the lamps.
def tun_floor(D, x, y, lane=False):
    """a pixel of the bore's floor: the ring joint and its lit edge stay where vanilla's planks put them (every tile
    of THE TUNNEL joins them, gbacaves' lane among them); the ring's own face is the direction's"""
    if y % 8 == 0:
        return "@7:11" if lane else "@7:8"
    if y % 8 == 7:
        return "@7:2"
    return D["tn_face"](x, y, lane)


def p_tn_floor(K, D):
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                K.out[y][x] = tun_floor(D, x, y, K.lane)


def p_tn_struct(K, D):
    """a wall end, a corner, an edge of the floor: vanilla's geometry kept (it joins gbacaves' walls and lane), every
    floor and lane pixel in it carrying the direction's floor, every wall pixel its own index"""
    row = K.row
    for y in range(K.h):
        for x in range(K.w):
            vv = K.vi(x, y)
            if vv is None:
                continue
            if row == 7 and vv == 7 and 0 < y % 8 < 7:
                K.out[y][x] = D["tn_face"](x, y, False)
            elif row == 7 and vv == 10 and 0 < y % 8 < 7:
                K.out[y][x] = D["tn_face"](x, y, True)
            else:
                K.out[y][x] = "@%d:%d" % (row, vv)


def p_tn_stairs(K, D):
    """the stairs up to the street at each end: a flight running on the diagonal, the balustrade beside it"""
    for y in range(K.h):
        for x in range(K.w):
            vv = K.vi(x, y)
            if vv is None:
                continue
            K.out[y][x] = D["tn_stair"](K, x, y, vv)


def p_tn_lamp(K, D):
    """the ceiling lamp (row 8): the plate on the ceiling, the light the direction hangs on it"""
    x0, y0, x1, y1 = K.bbox()
    for y in range(K.h):
        for x in range(K.w):
            vv = K.vi(x, y)
            if vv is not None:
                K.out[y][x] = "@8:%d" % (vv if vv <= 3 else 2)
    D["tn_lamp"](K, x0, y0, x1, y1)


# ============================================================================================ the groups
#  key, set, layout (as it stands), painter, what it is
TABLE = M([4, 5, h(5), h(4)], [3, 21, h(21), h(3)], [20, 21, h(21), h(20)], [36, 37, h(37), h(36)])
GROUPS = [
    ("fc_wall",   "fan", M([1, 16, 16, h(1)], [17, 32, 32, h(17)], [33, 48, 48, h(33)], [49, 64, 64, h(49)]),
     p_fc_wall, "the fan club's wall"),
    ("fc_floor",  "fan", M([61, h(61)], [v(61), hv(61)]),                  p_fc_floor_lit,   "the fan club's floor"),
    ("fc_shade",  "fan", M([65, h(62), 62, h(65)], [v(62), hv(62), v(62), hv(62)]), p_fc_floor_shade,
     "the same floor in the wall's shade"),
    ("fc_sofa",   "fan", M([6, 7, h(7), h(6)], [22, 23, h(23), h(22)], [38, 39, h(39), h(38)]), upholster,
     "the sofa at the head of the rug"),
    ("fc_chair",  "fan", M([11, 12], [13, 14], [29, 30], [45, 46]),       upholster,        "the armchairs"),
    ("fc_table",  "fan", TABLE,                                            p_fc_table,       "the table"),
    ("fc_table2", "fan", M([84, 5, h(5), h(4)], [3, 21, h(21), h(3)], [20, 21, h(21), h(20)], [36, 37, h(37), h(36)]),
     p_fc_table, "INIT's table (84: the corner his book lies on)"),
    ("dc_wall",   "fan", M([h(2), 19, 19, 2], [h(18), 35, 35, 18], [h(34), 51, 51, 34], [h(50), 67, 67, 50]),
     p_dc_wall, "the day cares' and INIT's wall"),
    ("dc_window", "fan", M([52, 53], [54, 55]),                            p_dc_window,      "a window"),
    ("dc_floor",  "fan", M([57, 57], [57, 57]),                            p_dc_floor_lit,   "the day cares' floor"),
    ("dc_shade",  "fan", M([h(66), 58, 58, 66], [57, 57, 57, 57]),         p_dc_floor_shade, "the floor in the wall's shade"),
    ("dc_lawn",   "fan", M([60, 60], [59, 59]),                            p_dc_lawn,        "the lawn"),
    ("dc_rail",   "fan", M([27, 27], [43, 43]),                            p_dc_lowwall,     "the low wall by the lawn"),
    ("dc_rail_end", "fan", M([28], [44]),                                  p_dc_lowwall,     "its end"),
    ("dc_rail_corner", "fan", M([26], [42]),                               p_dc_lowwall,     "its corner"),
    ("dc_post",   "fan", M([56], [10], [10]),                              p_dc_lowwall,     "the gate post"),
    ("dc_stool",  "fan", M([80, h(80)], [81, h(81)]),                      p_dc_stool,       "a stool"),
    ("rug",       "fan", M([hv(70), v(71), v(71), v(70)], [hv(69), v(68), v(68), v(69)], [h(69), 68, 68, 69],
                           [h(70), 71, 71, 70]), p_rug, "the rug under the table"),
    ("case",      "fan", M([72, 73], [74, 75], [76, 77], [78, 79]),       p_case,           "the glass case"),
    ("bh_hole",   "burg", M([120, 121, 122, 123], [136, 137, 138, 139], [152, 153, 154, 155], [168, 169, 170, 171]),
     p_bh_hole, "the hole TEAM CORPUS dug through the wall"),
    ("bh_dark",   "burg", M([2, 3], [18, 19]),                             p_bh_dark,        "what is behind it"),
    ("bh_kitchen", "burg", M([4, 5, 6], [20, 21, 22], [36, 37, 38]),       p_bh_kitchen,     "the kitchen dresser, ransacked"),
    ("bh_shelf",  "burg", M([7, 8, 9, 10], [23, 24, 25, 26], [39, 40, 41, 42]), p_bh_shelf,  "the shelf, emptied"),
    ("bh_tall",   "burg", M([13, 14], [29, 30], [45, 46], [15, 31]),       p_bh_furniture,   "the tall chair"),
    ("bh_stool",  "burg", M([52, 53, 54], [68, 69, 70]),                   p_bh_furniture,   "a chair on its back"),
    ("bh_chair1", "burg", M([130, 131], [146, 147], [162, 163]),           p_bh_furniture,   "a chair knocked over"),
    ("bh_chair2", "burg", M([124, 125], [140, 141], [156, 157]),           p_bh_furniture,   "a chair knocked over"),
    ("bh_chair3", "burg", M([128, 129], [144, 145], [160, 161]),           p_bh_furniture,   "a chair knocked over"),
    ("bh_strewn", "burg", M([55, 56, 57, 58], [11, 12, 59, 60], [27, 28, 75, 76], [43, 44, 61, 62], [None, None, 77, 78]),
     p_bh_strewn, "what was pulled out and dropped"),
    ("bh_plant",  "burg", M([80, 81, 82, 83], [96, 97, 98, 99], [112, 113, 114, 115]), p_bh_plant, "the plant, tipped"),
    ("bh_track1", "burg", M([84, 85], [100, 101]),                         p_bh_tracks,      "the LOOTER's tracks"),
    ("bh_track2", "burg", M([92, 93], [108, 109]),                         p_bh_tracks,      "the LOOTER's tracks"),
    ("bh_track3", "burg", M([86, 87], [102, 103]),                         p_bh_tracks,      "the LOOTER's tracks"),
    ("bh_track4", "burg", M([90, 91], [106, 107]),                         p_bh_tracks,      "the LOOTER's tracks"),
    ("bh_track5", "burg", M([h(89), h(88)], [h(105), h(104)]),             p_bh_tracks,      "the LOOTER's tracks"),
    ("tn_stairs", "tun", M([None, None, 12, 13], [12, 13, 45, 29], [28, 29, 44, 14], [44, 14, 14, 15], [14, 15, 27, 31],
                           [30, 31, None, None], [46, 47, 47, 22]), p_tn_stairs, "the stairs at each end"),
    ("tn_floor",  "tun", M([8]),                                           p_tn_floor,       "the bore's floor"),
    ("tn_lane",   "tun", M([24]),                                          p_tn_floor,       "the lit lane"),
    ("tn_lamp",   "tun", M([h(16), 16], [h(32), 32]),                      p_tn_lamp,        "a ceiling lamp"),
] + [("tn_%d" % t, "tun", M([t]), p_tn_struct, "a wall end, corner or floor edge")
     for t in (2, 3, 4, 5, 6, 7, 9, 10, 11, 18, 19, 20, 21, 23, 25, 34, 36, 37, 38, 41, 49)]
LANE = {"tn_lane"}

#  each own row's fifteen materials, in index order 1..15 (the same layout in every direction)
ROWMATS = {
    ("fan", 8):  ["OUT", "SHD", "MID", "HI", "WHT", "W1", "W2", "W3", "F1", "F2", "U1", "U2", "U3", "T1", "T2"],
    ("fan", 9):  ["OUT", "SHD", "MID", "HI", "WHT", "D1", "D2", "D3", "G1", "G2", "R1", "R2", "R3", "T1", "T2"],
    ("fan", 10): ["OUT", "SHD", "MID", "HI", "WHT", "V1", "V2", "V3", "L1", "L2", "L3", "C1", "C2", "X", "GL"],
}

#  THE TUNNEL's tiles gbacaves.py redraws itself (its draw_tunnel): never ours. gbacaves.T538_TUNNEL must equal the
#  tunnel tiles this tool owns (checked in report), so its --write keeps them as they stand.
TUNNEL_GBACAVES = {1, 17, 26, 33, 35, 39, 40, 42, 43}


# ============================================================================================ resolving
def mats_for(D, setkey):
    m = dict(D["mat"]["*"])
    m.update(D["mat"][setkey])
    #  exact colours of the fixed rows, by index: "@r:i" (primary rows 0..6 as batch D left them, gbacaves' rows)
    for r in range(7):
        for i in range(1, 16):
            m["@%d:%d" % (r, i)] = tuple(G.PPAL[r][i])
    for (k, r), pal in FIXED_PAL.items():
        if k == setkey:
            for i in range(1, 16):
                m["@%d:%d" % (r, i)] = tuple(pal[i])
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
        K.lane = key in LANE
        painter(K, D)
        mat = mats_for(D, setkey)
        for t, mats in K.tiles().items():
            if (setkey, t) in owner or t >= S.nvan or t not in S.use:
                continue
            if setkey == "tun" and t in TUNNEL_GBACAVES:
                continue
            spals = out[setkey][1]
            rows = dict(S.use[t]["rows"])
            own = {r: spals[r] for r in S.rows + FIXED.get(setkey, [])}
            Dm = {"mat": mat, "_index": {(r, m): i + 1 for r in S.rows for i, m in enumerate(ROWMATS[S.key, r])}}
            px = G.resolve(mats, S.van[t], rows, Dm, own)
            out[setkey][0][t] = px
            owner[setkey, t] = key
    return out, owner


# ============================================================================================ the directions
# ---------------------------------------------------------------------------------------- A THE KEEPING
def A_fc_upper(x, y):
    """limewash in warm ochre, brushed: the HEARTH's walls carried into ARDOR's parlour"""
    if y == 0:
        return "W1"
    return "W3" if H(x // 3, y, 5) % 5 == 0 else "W2"


def A_fc_dado(x, y):
    """oak tongue-and-groove: a board every four pixels, the groove dark, the board's lit edge"""
    if x % 4 == 0:
        return "T1"
    if x % 4 == 1:
        return "W3"
    return "T2"


def A_fc_floor(x, y, shade):
    """terracotta quarry tiles (the HEARTH's floor), a lime grout line"""
    if x == 0 or y == 0:
        return "SHD" if shade else "HI"
    if shade:
        return "F1"
    return "F2" if (x + y) % 9 else "F1"


def A_fc_cloth(x, y, m):
    """oxblood corduroy, button-backed: the wale runs down, a button every six pixels on the back"""
    if m in ("U2", "U3") and x % 2 == 0:
        return "U2" if m == "U3" else "U1"
    if m == "U3" and x % 6 == 3 and y % 6 == 2:
        return "U1"
    return None


def A_fc_top(x, y, w, hh):
    """an oak table under a red gingham cloth"""
    if x < 2 or x > w - 2 or y < 1:
        return "T2"
    a, b = (x // 3) % 2, (y // 3) % 2
    return "U2" if a and b else ("U3" if a or b else "WHT")


def A_dc_upper(x, y):
    """duck-egg limewash, a stencilled frieze of small flowers along the top (a nursery's), no words"""
    if y < 6:
        if y in (0, 5):
            return "V1"
        k = x % 8
        if (k, y) in ((3, 2), (2, 3), (4, 3), (3, 4)):
            return "X"
        if (k, y) == (3, 3):
            return "WHT"
        return "V3"
    return "V3" if H(x // 3, y, 9) % 6 == 0 else "V2"


def A_dc_window(x, y):
    """a leaded light under a gingham pelmet"""
    if y < 4:
        return "R2" if ((x // 2) + (y // 2)) % 2 else "WHT"
    if y >= 13:
        return "T2" if y == 13 else "T1"
    if x in (0, 15) or y == 4:
        return "T1"
    #  diamond leading
    if (x + y) % 6 == 0 or (x - y) % 6 == 0:
        return "OUT"
    return "G2" if (x + y) % 11 < 4 else "G1"


def A_dc_floor(x, y, shade):
    """long oak boards, 4px wide, a grain streak along each"""
    if y % 4 == 3:
        return "OUT" if shade else "D1"
    if y % 4 == 1 and x in (2, 3, 4):
        return "D1" if shade else "D2"
    return "D2" if shade else "D3"


def A_dc_lawn(x, y, dark):
    """a clover lawn, a daisy or two"""
    if dark:
        return "L1"
    if (x, y) == (2, 2):
        return "WHT"
    if (x, y) in ((6, 5), (5, 6), (7, 6), (6, 7)):
        return "L3"
    return "L1" if H(x, y, 4) % 11 == 0 else "L2"


def A_dc_lowwall(x, y, z):
    """an oak planter box along the lawn: a lit capping board, planked front, a nail head"""
    if z == 0:
        return "OUT"
    if z >= 2 and y % 8 < 3:
        return "T2"
    if y % 4 == 3:
        return "SHD"
    return "T1" if x != 6 else ("HI" if y % 8 == 5 else "T1")


def A_dc_stool(K, x0, y0, x1, y1):
    """a milking stool: a round oak seat, three splayed legs"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "OUT")
    ell(K, cx, y0 + 5, (x1 - x0) / 2, 5, "T1")
    ell(K, cx - 1, y0 + 4, (x1 - x0) / 2 - 2, 3, "T2")
    for lx in (x0 + 2, int(cx), x1 - 2):
        K.vline(lx, y0 + 10, y1 - 1, "T1")


def A_rug(x, y, e):
    """a hooked rag rug: a flecked field, a madder band and an olive band"""
    if e < 2:
        return "R1"
    if e < 4:
        return "R3"
    if e < 6:
        return "R1"
    return "R2" if H(x, y, 11) % 4 else ("R3" if H(x, y, 12) % 2 else "D2")


def A_case(K, x0, y0, x1, y1):
    """a Wardian case: an oak frame, glass, three ferns in clay pots; the cabinet under it oak"""
    split = y0 + 22
    K.fn(lambda x, y: "C1")
    K.rect(x0 + 2, y0 + 2, x1 - 2, split - 2, "GL")
    for cy in (y0 + 5, y0 + 11, y0 + 17):
        cx = (x0 + x1) / 2
        ell(K, cx, cy, 4, 2.5, "L2")
        ell(K, cx - 1, cy - 1, 2, 1, "L3")
        K.rect(int(cx) - 1, cy + 2, int(cx) + 1, cy + 3, "X")
    K.hline(x0 + 2, x1 - 2, y0 + 2, "WHT")
    K.rect(x0, split - 1, x1, split, "C2")
    for y in range(split + 1, y1 + 1):
        K.hline(x0, x1, y, "C1" if y % 4 else "OUT")
    K.px(int((x0 + x1) / 2), split + 4, "X")


def A_bh_wall(x, y):
    """DOLDRUM brick under limewash, worn through where the shoulder brushed it"""
    if y % 4 == 3:
        return "mortar"
    if (x + (y // 4) * 4) % 8 == 0:
        return "mortar"
    return "brick" if H(x // 8, y // 4, 2) % 3 else "brick_l"


def A_bh_rim(x, y):
    """the broken edge: bricks snapped short, raw earth behind them"""
    return "brick_d" if H(x, y, 4) % 3 else "earth"


def A_bh_rubble(x, y):
    return "brick_d" if H(x // 2, y // 2, 5) % 3 == 0 else ("earth" if H(x, y, 6) % 2 else "brick")


def A_bh_dark(x, y):
    """the earth behind the wall, a root through it"""
    if y in (5, 6) and 2 < x < 13 or (x == 12 and y > 6):
        return "root"
    return "earth" if H(x // 2, y // 2, 8) % 9 == 0 else "earth_d"


def A_bh_kitchen(K, x0, y0, x1, y1):
    """an oak dresser: its top scrubbed, two drawers pulled out and left (the dark in them)"""
    K.fn(lambda x, y: "wood")
    K.rect(x0, y0, x1, y0 + 4, "wood_l")
    K.hline(x0, x1, y0 + 5, "OUT")
    for xa in (x0 + 2, x0 + 13):
        K.rect(xa, y1 - 9, xa + 8, y1 - 2, "OUT")
        K.rect(xa + 1, y1 - 8, xa + 7, y1 - 6, "wood_d")
        K.hline(xa, xa + 8, y1 - 2, "wood_l")
    for y in range(y0 + 6, y1 - 10):
        if y % 4 == 0:
            K.hline(x0 + 1, x1 - 1, y, "wood_d")


def A_bh_shelf(K, x0, y0, x1, y1):
    """the oak shelf, emptied: two books left lying, the rest of the boards bare"""
    K.fn(lambda x, y: "wood")
    K.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, "wood_d")
    for sy in (y0 + 9, y0 + 17):
        K.rect(x0 + 2, sy, x1 - 2, sy + 1, "wood_l")
    K.rect(x0 + 5, y0 + 15, x0 + 12, y0 + 16, "book")
    K.rect(x1 - 9, y0 + 7, x1 - 7, y0 + 8, "book_l")
    K.vline(x0 + 1, y0, y1, "wood_l")


def A_paw(K, cx, cy):
    """a paw print in DOLDRUM mud: a dark pad, four toes, the mud's lighter edge"""
    ell(K, cx, cy + 1, 2.4, 1.8, "mud")
    ell(K, cx, cy + 1, 1.6, 1.1, "mud_d")
    for dx, dy in ((-2, -2), (-1, -3), (1, -3), (2, -2)):
        K.px(cx + dx, cy + dy, "mud_d")


def A_tn_face(x, y, lane):
    """glazed tile: a vertical grout every eight pixels, the tile's lit corner"""
    if x % 8 == 7:
        return "@7:12" if lane else "@7:9"
    if x % 8 == 0 and y % 8 == 1:
        return "@7:11" if lane else "@7:8"
    return "@7:10" if lane else "@7:7"


def A_tn_stair(K, x, y, vv):
    """tiled treads with a lit nosing; the balustrade's posts kept, each with its lit side"""
    if vv in (8, 9):
        return "@7:6" if (x + 2 * y) % 8 == 0 else "@7:%d" % vv
    if vv == 3 and x % 4 == 1:
        return "@7:5"
    return "@7:%d" % vv


def A_tn_lamp(K, x0, y0, x1, y1):
    """a bulkhead lamp: an oval glass in a cage of two bars"""
    cx, cy = (x0 + x1) / 2, y0 + 5
    ell(K, cx, cy, 5, 3, "@8:3")
    ell(K, cx, cy, 4, 2, "@8:5")
    ell(K, cx - 1, cy - 1, 2, 1, "@8:4")
    K.vline(int(cx) - 2, cy - 3, cy + 3, "@8:1")
    K.vline(int(cx) + 2, cy - 3, cy + 3, "@8:1")


# ---------------------------------------------------------------------------------------- B THE REGISTER
def B_fc_upper(x, y):
    """sage tongue-and-groove, upright: the WAYMARK's walls"""
    if y == 0:
        return "W1"
    return "W1" if x % 5 == 0 else ("W3" if x % 5 == 1 else "W2")


def B_fc_dado(x, y):
    """a blank blue enamel band, then slate panelling"""
    if y < 3:
        return "U3" if y == 1 else "U2"
    return "OUT" if x % 16 == 0 else ("T2" if y == 3 else "T1")


def B_fc_floor(x, y, shade):
    """slate flags, a speckle in the stone"""
    if x == 0 or y == 0:
        return "SHD"
    if H(x, y, 3) % 11 == 0:
        return "F1" if not shade else "F2"
    return "F1" if shade else "F2"


def B_fc_cloth(x, y, m):
    """grey wool, one blue welt along the seams"""
    if m == "U3" and y % 8 == 0:
        return "U1"
    return None


def B_fc_top(x, y, w, hh):
    """white laminate, a blue edge banding"""
    if x < 1 or x > w - 1 or y < 1:
        return "U2"
    return "HI" if y == 2 and 2 < x < w - 2 else "WHT"


def B_dc_upper(x, y):
    """white glazed tile in courses, a blue band at the head"""
    if y < 6:
        return "X" if 1 < y < 5 else "V1"
    if y % 4 == 1 or x % 4 == 0:
        return "V2"
    return "V3"


def B_dc_window(x, y):
    """a venetian blind half down over the glass"""
    if y >= 13:
        return "T2" if y == 13 else "T1"
    if x in (0, 15):
        return "T1"
    if y < 8:
        return "HI" if y % 2 == 0 else "MID"
    return "G2" if (x - y) % 7 < 2 else "G1"


def B_dc_floor(x, y, shade):
    """sheet vinyl in a two-tone check"""
    a = ((x // 4) + (y // 4)) % 2
    if shade:
        return "D1" if a else "D2"
    return "D2" if a else "D3"


def B_dc_lawn(x, y, dark):
    """a mown lawn, stripes the width of the mower"""
    if dark:
        return "L1"
    return "L3" if (x // 4) % 2 else "L2"


def B_dc_lowwall(x, y, z):
    """a white rendered low wall with a blue coping"""
    if z == 0:
        return "OUT"
    if z >= 2 and y % 8 < 2:
        return "X"
    return "WHT" if z >= 2 else "HI"


def B_dc_stool(K, x0, y0, x1, y1):
    """a moulded stool: a blue seat on white legs"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "OUT")
    ell(K, cx, y0 + 5, (x1 - x0) / 2, 5, "T1")
    ell(K, cx, y0 + 4, (x1 - x0) / 2 - 2, 3, "T2")
    K.vline(x0 + 2, y0 + 10, y1 - 1, "WHT")
    K.vline(x1 - 2, y0 + 10, y1 - 1, "WHT")


def B_rug(x, y, e):
    """a felt runner with a fine grid, a single blue rule inside its edge"""
    if e < 1:
        return "R1"
    if e == 3:
        return "R1"
    if e < 6:
        return "R3"
    return "R3" if (x == 0 and y % 2 == 0) or (y == 0 and x % 2 == 0) else "R2"


def B_case(K, x0, y0, x1, y1):
    """an incubator cabinet: white enamel, a glass front, three domed trays under a soft lamp, a blue status light"""
    split = y0 + 22
    K.fn(lambda x, y: "C2")
    K.rect(x0 + 2, y0 + 2, x1 - 2, split - 2, "GL")
    K.hline(x0 + 3, x1 - 3, y0 + 3, "X")
    for cy in (y0 + 7, y0 + 12, y0 + 17):
        K.rect(x0 + 4, cy + 1, x1 - 4, cy + 2, "HI")
        ell(K, (x0 + x1) / 2, cy, 3, 1.6, "L2")
    K.rect(x0, split - 1, x1, split, "C1")
    for y in range(split + 1, y1 + 1):
        K.hline(x0, x1, y, "C2" if y % 5 else "C1")
    K.px(x1 - 3, split + 3, "X")


def B_bh_wall(x, y):
    """smooth plaster, a skim coat"""
    return "plaster_l" if H(x, y, 3) % 9 == 0 else "plaster"


def B_bh_rim(x, y):
    """a clean cut: a cored ring, the plaster's section showing"""
    return "cut"


def B_bh_rubble(x, y):
    return "dust" if H(x, y, 2) % 3 else "plaster_l"


def B_bh_dark(x, y):
    """the dark behind the cut, the core's ring scored on it"""
    if (x - 7.5) ** 2 + (y - 9) ** 2 < 4:
        return "earth"
    return "dark"


def B_bh_kitchen(K, x0, y0, x1, y1):
    """white cabinets, every door left open"""
    K.fn(lambda x, y: "plaster_l")
    K.rect(x0, y0, x1, y0 + 4, "paper")
    K.hline(x0, x1, y0 + 5, "OUT")
    for xa in (x0 + 2, x0 + 13):
        K.rect(xa, y1 - 10, xa + 8, y1 - 1, "dark")
        K.vline(xa - 1, y1 - 10, y1 - 1, "paper")
        K.vline(xa + 9, y1 - 10, y1 - 1, "cut")


def B_bh_shelf(K, x0, y0, x1, y1):
    """white shelving, the box files gone: their outlines in the dust"""
    K.fn(lambda x, y: "plaster_l")
    K.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, "plaster")
    for sy in (y0 + 9, y0 + 17):
        K.rect(x0 + 2, sy, x1 - 2, sy + 1, "paper")
    for bx in range(x0 + 4, x1 - 4, 6):
        K.rect(bx, y0 + 11, bx + 3, y0 + 16, "dust")


def B_paw(K, cx, cy):
    """a paw print in pale plaster dust"""
    ell(K, cx, cy + 1, 1.6, 1.2, "dust")
    for dx, dy in ((-2, -1), (-1, -3), (1, -3), (2, -1)):
        K.px(cx + dx, cy + dy, "dust")


def B_tn_face(x, y, lane):
    """precast rings, smooth, an aggregate speckle"""
    if H(x, y, 21) % 13 == 0:
        return "@7:12" if lane else "@7:9"
    return "@7:10" if lane else "@7:7"


def B_tn_stair(K, x, y, vv):
    """plain treads, each nosing a lit line; the balustrade a glass panel with one blue handrail light"""
    if vv in (8, 9):
        return "@7:8" if (x + 2 * y) % 8 < 2 else "@7:7"
    if vv == 5:
        return "@7:4"
    if vv == 3:
        return "@7:6" if (x - y) % 9 else "@7:5"
    return "@7:%d" % vv


def B_tn_lamp(K, x0, y0, x1, y1):
    """a linear light: one long lit bar"""
    K.rect(x0 + 1, y0 + 3, x1 - 1, y0 + 7, "@8:3")
    K.rect(x0 + 2, y0 + 4, x1 - 2, y0 + 6, "@8:5")
    K.hline(x0 + 2, x1 - 2, y0 + 4, "@8:4")


# ---------------------------------------------------------------------------------------- C MAKE DO
def C_fc_upper(x, y):
    """limewashed brick in courses: the FOUNDRY TOWN and SALVAGE YARD hand, a club in an old net loft"""
    if y % 4 == 3:
        return "W1"
    if (x + (y // 4) * 4) % 8 == 0:
        return "W1"
    return "W2" if H(x // 8, y // 4, 3) % 3 else "W3"


def C_fc_dado(x, y):
    """corrugated sheet, painted"""
    return ("T1", "T2", "T2", "OUT")[x % 4] if y > 0 else "OUT"


def C_fc_floor(x, y, shade):
    """brick pavers in a basket weave"""
    if x == 0 or y == 0 or y == 4:
        return "SHD"
    if shade:
        return "F1"
    return "F2" if H(x, y // 4, 6) % 4 else "F1"


def C_fc_cloth(x, y, m):
    """felt patchwork, a stitch line at each seam"""
    if m == "U1":
        return None
    p = H(x // 5, y // 5, 13) % 3
    if x % 5 == 0 or y % 5 == 0:
        return "U1"
    return ("U2", "U3", "U2")[p] if m == "U3" else ("U2" if p else "U1")


def C_fc_top(x, y, w, hh):
    """a ship's hatch cover laid on trestles: steel, its panels, a rivet at each corner"""
    if x < 1 or x > w - 1 or y < 1:
        return "T1"
    if y % 10 == 0 or x % 16 == 0:
        return "T1"
    if (x % 16 in (2, 14)) and (y % 10 in (2, 8)):
        return "WHT"
    return "T2" if y % 10 != 1 else "HI"


def C_dc_upper(x, y):
    """matchboarding painted from odd tins: each board its own colour"""
    if y < 6:
        return "V1" if y in (0, 5) else "X"
    if x % 4 == 0:
        return "OUT"
    return ("V2", "V3", "V2", "MID")[H(x // 4, 0, 7) % 4]


def C_dc_window(x, y):
    """a salvaged porthole: a brass ring, the glass"""
    d = (x - 7.5) ** 2 + (y - 6.5) ** 2
    if y >= 13:
        return "T2" if y == 13 else "T1"
    if d > 49:
        return "SHD"
    if d > 30:
        return "R3" if (x + y) % 3 else "R2"
    return "G2" if (x - y) % 6 < 2 else "G1"


def C_dc_floor(x, y, shade):
    """plywood sheets screwed down"""
    if (x, y) in ((1, 1), (6, 6)):
        return "OUT"
    if x == 7:
        return "D1"
    return ("D1" if shade else "D2") if H(x, y, 9) % 5 == 0 else ("D2" if shade else "D3")


def C_dc_lawn(x, y, dark):
    """patchy grass over sand"""
    if dark:
        return "L1"
    return "V3" if H(x // 2, y // 2, 4) % 6 == 0 else ("L3" if H(x, y, 5) % 4 == 0 else "L2")


def C_dc_lowwall(x, y, z):
    """fish boxes stacked into a low wall: slats with gaps"""
    if z == 0:
        return "OUT"
    if x % 4 == 3:
        return "SHD"
    return "T2" if z >= 2 else "T1"


def C_dc_stool(K, x0, y0, x1, y1):
    """an upturned drum with a felt pad"""
    cx = (x0 + x1) / 2
    K.fn(lambda x, y: "OUT")
    ell(K, cx, y0 + 5, (x1 - x0) / 2, 5, "R1")
    ell(K, cx, y0 + 4, (x1 - x0) / 2 - 2, 3, "R2")
    for y in range(y0 + 10, y1):
        K.hline(x0 + 1, x1 - 1, y, "MID" if y % 3 else "SHD")


def C_rug(x, y, e):
    """a kilim: diamonds in the field, a zigzag border"""
    if e < 6:
        return "R1" if (x + y) % 4 == 0 else ("R3" if e % 3 == 1 else "R2")
    k = abs(x - 3.5) + abs(y - 3.5)
    return "R1" if k < 1.5 else ("R3" if k < 3 else "R2")


def C_case(K, x0, y0, x1, y1):
    """an old aquarium on a crate: green water, weed, a bubble"""
    split = y0 + 22
    K.fn(lambda x, y: "C1")
    K.rect(x0 + 2, y0 + 3, x1 - 2, split - 2, "L1")
    K.rect(x0 + 2, y0 + 3, x1 - 2, y0 + 5, "GL")
    for wx in (x0 + 4, x1 - 5):
        for y in range(y0 + 9, split - 2):
            K.px(wx + (y // 3) % 2, y, "L3")
    K.px(x0 + 7, y0 + 10, "WHT")
    K.px(x0 + 8, y0 + 13, "WHT")
    K.rect(x0, split - 1, x1, split, "C2")
    for y in range(split + 1, y1 + 1):
        K.hline(x0, x1, y, "C2" if y % 4 else "OUT")


def C_bh_wall(x, y):
    """plaster on lath, the lath showing where it has fallen"""
    if H(x // 6, y // 4, 7) % 5 == 0:
        return "lath" if y % 3 else "OUT"
    return "plaster"


def C_bh_rim(x, y):
    """the hole shored up with planks, nailed across"""
    return "lath" if (y // 3) % 2 else "lath_d"


def C_bh_rubble(x, y):
    return "lath_d" if (x + y) % 5 == 0 else ("earth" if H(x, y, 3) % 2 else "plaster")


def C_bh_dark(x, y):
    """the dug earth, wet, a plank laid in it"""
    if y in (10, 11):
        return "lath"
    return "earth" if H(x // 2, y // 2, 2) % 7 == 0 else "earth_d"


def C_bh_kitchen(K, x0, y0, x1, y1):
    """crate shelving, one crate pulled out and tipped"""
    K.fn(lambda x, y: "lath")
    for y in range(y0, y1 + 1):
        if (y - y0) % 4 == 3:
            K.hline(x0, x1, y, "lath_d")
    K.rect(x0 + 13, y1 - 9, x0 + 21, y1 - 2, "OUT")
    K.rect(x0 + 2, y1 - 9, x0 + 10, y1 - 2, "earth_d")


def C_bh_shelf(K, x0, y0, x1, y1):
    """planks on bricks, emptied: a tin left on its side"""
    K.fn(lambda x, y: "brick")
    K.rect(x0 + 3, y0 + 1, x1 - 3, y1 - 1, "OUT")
    for sy in (y0 + 8, y0 + 16, y1 - 3):
        K.rect(x0 + 1, sy, x1 - 1, sy + 1, "lath")
    K.rect(x0 + 8, y0 + 13, x0 + 12, y0 + 15, "paper_d")


def C_paw(K, cx, cy):
    """a wet paw print, dark, a drip trailing from it"""
    ell(K, cx, cy + 1, 1.8, 1.4, "wet")
    for dx, dy in ((-2, -2), (-1, -3), (1, -3), (2, -2)):
        K.px(cx + dx, cy + dy, "wet")
    K.px(cx, cy + 3, "wet")
    K.px(cx + 1, cy + 5, "wet")


def C_tn_face(x, y, lane):
    """riveted steel plate: a rivet at each plate's corner, a diamond tread"""
    if x % 8 in (1, 6) and y % 8 in (1, 6):
        return "@7:12" if lane else "@7:8"
    if (x + y) % 4 == 0 and (x - y) % 4 == 0:
        return "@7:12" if lane else "@7:9"
    return "@7:10" if lane else "@7:7"


def C_tn_stair(K, x, y, vv):
    """steel grating treads, a mesh balustrade"""
    if vv in (8, 9):
        return "@7:2" if (x % 2 == 0 and y % 2 == 0) else "@7:%d" % vv
    if vv == 3:
        return "@7:1" if (x + y) % 3 == 0 or (x - y) % 3 == 0 else "@7:3"
    return "@7:%d" % vv


def C_tn_lamp(K, x0, y0, x1, y1):
    """a bare bulb on a bracket"""
    cx = int((x0 + x1) / 2)
    K.vline(cx, y0 + 1, y0 + 4, "@8:1")
    ell(K, cx, y0 + 7, 2.5, 2.5, "@8:6")
    ell(K, cx - 0.5, y0 + 6.5, 1.2, 1.2, "@8:4")


# ============================================================================================ the directions' colours
#  burgled_house sits in PRIMARY rows: these are targets, resolved to the nearest colour of the row a tile is placed in
A = dict(
    name="A", title="THE KEEPING",
    lines=["The rooms kept by hand (batch 1's HEARTH and batch 2's WORKBENCH carried on): ARDOR's parlour in ochre",
           "limewash and oak, terracotta tiles, oxblood corduroy, a red gingham cloth; the day cares and INIT's house in",
           "duck-egg with a stencilled frieze, oak boards, a clover lawn, Wardian cases of ferns; DOLDRUM's wall is brick",
           "dug through to the earth and a root, the LOOTER's paws in mud; THE TUNNEL's rings glazed tile, bulkhead lamps."],
    mat={"*": dict(OUT=(52, 40, 34), SHD=(96, 80, 66), MID=(150, 136, 120), HI=(214, 204, 186), WHT=(248, 242, 228)),
         "fan": dict(W1=(176, 136, 76), W2=(224, 188, 122), W3=(240, 214, 160), F1=(150, 78, 52), F2=(190, 104, 68),
                     U1=(92, 30, 34), U2=(140, 46, 46), U3=(184, 72, 64), T1=(128, 86, 54), T2=(196, 150, 96),
                     D1=(110, 74, 46), D2=(170, 120, 76), D3=(204, 156, 104), G1=(120, 160, 170), G2=(196, 224, 220),
                     R1=(120, 40, 40), R2=(176, 76, 60), R3=(120, 130, 70),
                     V1=(110, 150, 150), V2=(176, 210, 204), V3=(206, 230, 222), L1=(56, 100, 56), L2=(90, 146, 76),
                     L3=(136, 186, 104), C1=(128, 86, 54), C2=(196, 150, 96), X=(200, 96, 70), GL=(206, 232, 226)),
         "burg": dict(head=(214, 166, 112), head_l=(232, 224, 206), brick=(176, 122, 76), brick_l=(214, 166, 112),
                      brick_d=(128, 86, 54), mortar=(232, 224, 206), earth=(131, 115, 74), earth_d=(84, 72, 70),
                      root=(205, 189, 131), rim_d=(84, 72, 70), wood=(176, 122, 76), wood_l=(214, 166, 112),
                      wood_d=(128, 86, 54), cloth=(172, 86, 78), cloth_l=(214, 136, 108), book=(150, 76, 60),
                      book_l=(196, 112, 82), paper=(255, 255, 255), paper_d=(232, 212, 150), leaf=(90, 148, 82),
                      leaf_d=(74, 104, 60), leaf_l=(150, 198, 120), pot=(176, 122, 76), pot_l=(214, 136, 108),
                      pot_d=(128, 86, 54), soil=(84, 72, 70), mud=(131, 115, 74), mud_d=(82, 82, 106),
                      plaster=(197, 222, 205), plaster_l=(230, 238, 246), cut=(172, 197, 180), dust=(213, 222, 222),
                      dark=(82, 82, 106), lath=(189, 164, 123), lath_d=(148, 131, 106), wet=(82, 82, 106)),
         "tun": {}},
    fc_upper=A_fc_upper, fc_dado=A_fc_dado, fc_floor=A_fc_floor, fc_cloth=A_fc_cloth, fc_top=A_fc_top,
    dc_upper=A_dc_upper, dc_window=A_dc_window, dc_floor=A_dc_floor, dc_lawn=A_dc_lawn, dc_lowwall=A_dc_lowwall,
    dc_stool=A_dc_stool, rug=A_rug, case=A_case,
    bh_wall=A_bh_wall, bh_rim=A_bh_rim, bh_rubble=A_bh_rubble, bh_dark=A_bh_dark, bh_kitchen=A_bh_kitchen,
    bh_shelf=A_bh_shelf, paw=A_paw, grain=lambda x, y: (x + 2 * y) % 7 == 0,
    tn_face=A_tn_face, tn_stair=A_tn_stair, tn_lamp=A_tn_lamp,
)

B = dict(
    name="B", title="THE REGISTER",
    lines=["The rooms as the institution keeps them (batch 1's WAYMARK and batch 2's CLEAN ROOM): sage panelling and a",
           "blank blue enamel band, slate flags, grey wool, white laminate; the day cares white glazed tile, a venetian",
           "blind, sheet vinyl, a mown lawn, incubator cabinets with a blue status light; DOLDRUM's hole a clean cored",
           "cut, its prints pale dust; THE TUNNEL's rings smooth precast, a glass balustrade, linear lights."],
    mat={"*": dict(OUT=(60, 64, 80), SHD=(110, 116, 132), MID=(164, 170, 182), HI=(214, 220, 228), WHT=(250, 252, 252)),
         "fan": dict(W1=(120, 140, 120), W2=(170, 190, 168), W3=(206, 220, 200), F1=(84, 92, 104), F2=(118, 128, 140),
                     U1=(50, 90, 170), U2=(130, 136, 148), U3=(180, 186, 196), T1=(76, 84, 96), T2=(120, 128, 142),
                     D1=(150, 156, 168), D2=(204, 208, 216), D3=(236, 238, 240), G1=(110, 160, 210),
                     G2=(190, 224, 246), R1=(50, 90, 170), R2=(150, 160, 150), R3=(196, 204, 196),
                     V1=(150, 156, 168), V2=(214, 220, 226), V3=(244, 246, 248), L1=(60, 110, 70), L2=(96, 156, 96),
                     L3=(130, 186, 120), C1=(160, 166, 178), C2=(236, 238, 242), X=(60, 120, 200), GL=(200, 230, 248)),
         "burg": dict(head=(197, 222, 205), head_l=(230, 238, 246), plaster=(197, 222, 205), plaster_l=(230, 238, 246),
                      cut=(172, 197, 180), dust=(213, 222, 222), dark=(82, 82, 106), earth=(106, 106, 106),
                      rim_d=(82, 82, 106), wood=(150, 186, 204), wood_l=(232, 224, 206), wood_d=(74, 104, 130),
                      cloth=(74, 104, 130), cloth_l=(150, 186, 204), book=(74, 104, 130), book_l=(150, 186, 204),
                      paper=(255, 255, 255), paper_d=(230, 238, 246), leaf=(90, 148, 82), leaf_d=(74, 104, 60),
                      leaf_l=(150, 198, 120), pot=(232, 224, 206), pot_l=(255, 255, 255), pot_d=(150, 144, 134),
                      soil=(84, 72, 70), lath=(172, 172, 164), lath_d=(123, 123, 123)),
         "tun": {}},
    fc_upper=B_fc_upper, fc_dado=B_fc_dado, fc_floor=B_fc_floor, fc_cloth=B_fc_cloth, fc_top=B_fc_top,
    dc_upper=B_dc_upper, dc_window=B_dc_window, dc_floor=B_dc_floor, dc_lawn=B_dc_lawn, dc_lowwall=B_dc_lowwall,
    dc_stool=B_dc_stool, rug=B_rug, case=B_case,
    bh_wall=B_bh_wall, bh_rim=B_bh_rim, bh_rubble=B_bh_rubble, bh_dark=B_bh_dark, bh_kitchen=B_bh_kitchen,
    bh_shelf=B_bh_shelf, paw=B_paw, grain=lambda x, y: False,
    tn_face=B_tn_face, tn_stair=B_tn_stair, tn_lamp=B_tn_lamp,
)

C = dict(
    name="C", title="MAKE DO",
    lines=["The rooms made from what was to hand (batch 1's FOUNDRY TOWN and batch 2's SALVAGE YARD): ARDOR's club in",
           "an old net loft -- limewashed brick, corrugated sheet, brick pavers, felt patchwork, a hatch cover on trestles,",
           "a kilim; the day cares matchboarded from odd tins, a porthole, plywood, fish-box walls, an old aquarium; the",
           "hole shored with planks, wet paws; THE TUNNEL's rings riveted plate, grating stairs, bare bulbs."],
    mat={"*": dict(OUT=(44, 40, 40), SHD=(86, 80, 76), MID=(140, 132, 124), HI=(196, 190, 180), WHT=(236, 232, 222)),
         "fan": dict(W1=(150, 130, 116), W2=(214, 204, 188), W3=(232, 224, 210), F1=(120, 60, 44), F2=(166, 88, 62),
                     U1=(80, 56, 44), U2=(130, 120, 80), U3=(180, 120, 76), T1=(110, 116, 120), T2=(150, 156, 158),
                     D1=(120, 100, 70), D2=(180, 150, 104), D3=(206, 180, 132), G1=(40, 80, 80), G2=(120, 170, 160),
                     R1=(110, 40, 30), R2=(176, 120, 60), R3=(214, 180, 90),
                     V1=(70, 90, 100), V2=(120, 150, 150), V3=(196, 170, 120), L1=(70, 90, 50), L2=(110, 130, 70),
                     L3=(150, 170, 100), C1=(130, 100, 70), C2=(170, 136, 96), X=(200, 120, 60), GL=(170, 210, 196)),
         "burg": dict(head=(148, 131, 106), head_l=(205, 189, 131), plaster=(197, 222, 205), lath=(189, 164, 123),
                      lath_d=(148, 131, 106), earth=(131, 115, 74), earth_d=(84, 72, 70), rim_d=(84, 72, 70),
                      brick=(172, 86, 78), wood=(176, 122, 76), wood_l=(214, 166, 112), wood_d=(128, 86, 54),
                      cloth=(90, 148, 82), cloth_l=(150, 198, 120), book=(172, 86, 78), book_l=(214, 136, 108),
                      paper=(232, 224, 206), paper_d=(150, 144, 134), leaf=(90, 148, 82), leaf_d=(74, 104, 60),
                      leaf_l=(150, 198, 120), pot=(150, 144, 134), pot_l=(180, 180, 164), pot_d=(123, 123, 123),
                      soil=(84, 72, 70), wet=(82, 82, 106)),
         "tun": {}},
    fc_upper=C_fc_upper, fc_dado=C_fc_dado, fc_floor=C_fc_floor, fc_cloth=C_fc_cloth, fc_top=C_fc_top,
    dc_upper=C_dc_upper, dc_window=C_dc_window, dc_floor=C_dc_floor, dc_lawn=C_dc_lawn, dc_lowwall=C_dc_lowwall,
    dc_stool=C_dc_stool, rug=C_rug, case=C_case,
    bh_wall=C_bh_wall, bh_rim=C_bh_rim, bh_rubble=C_bh_rubble, bh_dark=C_bh_dark, bh_kitchen=C_bh_kitchen,
    bh_shelf=C_bh_shelf, paw=C_paw, grain=lambda x, y: y % 3 == 0,
    tn_face=C_tn_face, tn_stair=C_tn_stair, tn_lamp=C_tn_lamp,
)

STYLES = {"A": A, "B": B, "C": C}
#  a burgled-house material a direction does not name falls back to these
BURG_FALLBACK = dict(head=(232, 224, 206), head_l=(255, 255, 255), rim_d=(82, 82, 106), wood=(176, 122, 76),
                     wood_l=(214, 166, 112), wood_d=(128, 86, 54), cloth=(172, 86, 78), cloth_l=(214, 136, 108),
                     earth=(131, 115, 74), earth_d=(84, 72, 70))
for _D in STYLES.values():
    for _k, _c in BURG_FALLBACK.items():
        _D["mat"]["burg"].setdefault(_k, _c)


# ============================================================================================ sheets
BG, INK, RED, SOFT = (250, 248, 242), (24, 24, 24), (120, 20, 30), (90, 90, 90)
ROOMS1 = [("VermilionCity_PokemonFanClub", "ARDOR's fan club"), ("Route5_PokemonDayCare", "ROUTE 5's DAY-CARE"),
          ("FourIsland_PokemonDayCare", "FOUR ISLAND's DAY-CARE"),
          ("LavenderTown_VolunteerPokemonHouse", "INIT's house (HALFTONE)")]
ROOMS2 = [("CeruleanCity_House2", "DOLDRUM's burgled house", None),
          ("UndergroundPath_NorthSouthTunnel", "TUNNEL N-S", (0, 0, 8, 12)),
          ("UndergroundPath_EastWestTunnel", "THE TUNNEL, east-west (its west end)", (0, 0, 16, 7))]
DETAILS = [("VermilionCity_PokemonFanClub", (3, 0, 9, 7), "the sofa, the armchairs, the table, the rug"),
           ("Route5_PokemonDayCare", (0, 0, 6, 5), "the window, the lawn, the low wall, the case"),
           ("CeruleanCity_House2", (2, 0, 7, 4), "the hole TEAM CORPUS dug"),
           ("CeruleanCity_House2", (5, 2, 10, 8), "the strewn things, the LOOTER's tracks"),
           ("UndergroundPath_NorthSouthTunnel", (3, 0, 8, 5), "THE TUNNEL's stairs and lamps")]


def text(d, xy, s, fill=INK):
    d.text(xy, s, fill=fill)


def state_of(sets):
    return (sets, None) if sets else None


def room(m, st, crop=None):
    im = G.render_map(m, st)
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
    return im


def contact_sheets(out_dir, states):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: Nintendo's tiles (the plants, bookcases, PC, counters and frames primary/building",
                              "places here are batch D's and already ours; THE TUNNEL's colours and its walls' conduits",
                              "and PACKET TRACE are gbacaves' T-438 look, already ours)"])}
    for k in STYLES:
        titles[k] = ("%s %s" % (k, STYLES[k]["title"]), STYLES[k]["lines"])
    pad = 10
    paths = []
    for hi, rooms in enumerate([[(m, c, None) for m, c in ROOMS1], ROOMS2]):
        blocks = []
        for k in names:
            ims = [room(m, state_of(states[k]), cr) for m, _, cr in rooms]
            t, lines = titles[k]
            th = 8 + 12 * len(lines) + 16
            W = sum(i.width for i in ims) + pad * (len(ims) + 1)
            im = Image.new("RGB", (max(W, 900), th + max(i.height for i in ims) + pad), BG)
            d = ImageDraw.Draw(im)
            text(d, (pad, 6), t, RED)
            for j, s in enumerate(lines):
                text(d, (pad + 130, 6 + 12 * j), s)
            x = pad
            for i, (m, cap, _) in zip(ims, rooms):
                text(d, (x, th - 13), cap, SOFT)
                im.paste(i, (x, th))
                x += i.width + pad
            blocks.append(im)
        W = max(b.width for b in blocks)
        sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
        d = ImageDraw.Draw(sh)
        text(d, (pad, 8), "T-538 DRAFT, batch 3 -- %s, real rooms at 1x, three directions beside today's (redrawn in "
                          "place: no block, collision or palette row moves). (%d/2)"
             % (("the fan club, the day cares, INIT's house" if hi == 0 else "the burgled house, THE TUNNEL"), hi + 1),
             INK)
        y = 30
        for b in blocks:
            sh.paste(b, (0, y))
            y += b.height
        p = os.path.join(out_dir, "t538b3_rooms_1x_%d.png" % (hi + 1))
        sh.save(p)
        paths.append(p)
    #  3x details, one page per two or three
    rowsim = []
    for k in names:
        crops = []
        for m, (x0, y0, x1, y1), cap in DETAILS:
            im = room(m, state_of(states[k]), (x0, y0, x1, y1))
            crops.append((im.resize((im.width * 3, im.height * 3), Image.NEAREST), cap))
        rowsim.append((k, crops))
    for part in ((0, 1), (2, 3), (4,)):
        cw = sum(rowsim[0][1][i][0].width for i in part) + pad * 3 + 130
        ch = max(rowsim[0][1][i][0].height for i in part) + 24
        det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
        d = ImageDraw.Draw(det)
        text(d, (pad, 8), "T-538 DRAFT, batch 3 -- details at 3x: %s." % ", ".join(DETAILS[i][2] for i in part), INK)
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
        p = os.path.join(out_dir, "t538b3_detail_3x_%d.png" % (len(paths) - 1))
        det.save(p)
        paths.append(p)
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
    text(d, (pad, 6), "T-538 DRAFT, batch 3 -- the tiles at 3x, each in its home row (grey: transparent; light grey "
                      "cells: unused, left as they are)", INK)
    x = pad
    for t, c in cols:
        text(d, (x, 26), t, RED)
        sh.paste(c, (x, 42))
        x += c.width + pad
    p = os.path.join(out_dir, "t538b3_tiles_3x.png")
    sh.save(p)
    paths.append(p)
    return paths


# ============================================================================================ report
def report():
    print("T-538 batch 3 -- the fan club and day cares, the burgled house, THE TUNNEL\n")
    print("  census (placed tiles still Nintendo's drawing, gbahomes' measure):")
    for key, S in SETS.items():
        c = G.census_set(S.sym)
        print("    %-18s %3d vanilla of %3d placed; rows %s; animation %s; maps: %s"
              % (S.dir.split("/")[-1], c["vanilla"], c["used"], c["rows"], c["anim"] or "none", ", ".join(c["maps"])))
    owner = {}
    for key, setkey, layout, painter, what in GROUPS:
        for r in layout:
            for s in r:
                if s is not None:
                    t = s if isinstance(s, int) else s[0]
                    owner.setdefault((setkey, t), key)
    print("\n  %-15s %-5s %5s %6s %4s  %s" % ("group", "set", "tiles", "draws", "maps", "what"))
    for key, setkey, layout, painter, what in GROUPS:
        S = SETS[setkey]
        ts = sorted(t for (sk, t), k in owner.items() if k == key and t in S.use and t < S.nvan)
        draws = sum(S.use[t]["n"] for t in ts)
        maps = {m for t in ts for m in S.use[t]["maps"]}
        print("  %-15s %-5s %5d %6d %4d  %s" % (key, setkey, len(ts), draws, len(maps), what))
    bad = 0
    for key, S in SETS.items():
        mine = {t for (sk, t) in owner if sk == key}
        used = {t for t in S.use if t < S.nvan and any(S.cur[t])}
        others = TUNNEL_GBACAVES if key == "tun" else set()
        stray = sorted(t for t in used if t not in mine and t not in others)
        rows = sorted({r for t in used for r in S.use[t]["rows"]})
        foreign = sorted(r for r in rows if r >= 7 and r not in S.rows + FIXED.get(key, []))
        print("  %s: %d placed tiles, %d in a group%s; in no group: %s; rows placed %s, own rows %s%s"
              % (S.dir.split("/")[-1], len(used), len(used & mine),
                 ("; gbacaves' %d" % len(used & others)) if others else "", stray or "none", rows, S.rows or "none",
                 ("; !! placed in a row this tool does not own: %s" % foreign) if foreign else ""))
        bad |= bool(stray) or bool(foreign)
    #  rows a primary tile is placed in, inside these rooms: none may be one we recolour
    for key, S in SETS.items():
        if not S.rows:
            continue
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
    #  THE TUNNEL: gbacaves draws nine tiles and owns rows 7 and 8; its --write must keep ours (T538_TUNNEL)
    mine_tun = {t for (sk, t) in owner if sk == "tun" and t in TUN.use and t < TUN.nvan}
    cave = GC.Cave("underground_path")
    new, _ = GC.draw_tunnel(cave)
    theirs = {t for t in range(cave.n) if new[t] != cave.van[t]}
    if theirs != TUNNEL_GBACAVES:
        print("  !! gbacaves' THE TUNNEL now redraws %s, not %s -- update TUNNEL_GBACAVES" % (sorted(theirs),
                                                                                              sorted(TUNNEL_GBACAVES)))
        bad = 1
    keep = set(getattr(GC, "T538_TUNNEL", set()))
    if keep != mine_tun:
        print("  !! gbacaves.T538_TUNNEL %s is not this tool's tunnel tiles %s: its --write would revert them"
              % (sorted(keep), sorted(mine_tun)))
        bad = 1
    else:
        print("  THE TUNNEL: gbacaves draws %s and rows 7, 8 (never written here); its T538_TUNNEL keeps this tool's %d"
              % (sorted(theirs), len(mine_tun)))
    print("  THE READING ROOM (gbainterior): reads fan_club_daycare's layout, never its pixels -- untouched by a write")
    print("  scripted blocks: none (no setmetatile in these seven maps; no METATILE_ label names these tilesets)")
    return bad


def check_engine():
    """T-446's rule: with one direction approved, the engine must be exactly what `--write --approved --pick X` makes
    (every tile of each set this tool writes, its own rows); exit 1 on a difference"""
    pick = next(iter(APPROVED))
    sets, _ = draw(STYLES[pick])
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
            print("  --write refused: T-538 batch 3 is a draft. APPROVED is %s; the user picks a direction first, it "
                  "goes into APPROVED,\n  then --write --approved --pick X writes fan_club_daycare's tiles and rows 8, "
                  "9, 10, burgled_house's tiles and underground_path's tiles\n  (never a primary palette, never THE "
                  "TUNNEL's rows)." % (sorted(APPROVED) or "empty"))
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
            ch = {sk: sum(1 for (s2, t) in owner if s2 == sk and sets[sk][0][t] != SETS[sk].van[t]) for sk in SETS}
            summary[k] = dict(title=D["title"], tiles_redrawn=sum(ch.values()), by_set=ch, new_tiles=0,
                              rows={"fan_club_daycare %d" % r: sets["fan"][1][r] for r in FAN.rows})
            print("  %s %-13s %d tiles redrawn (fan_club_daycare %d, burgled_house %d, underground_path %d), 0 new; rows "
                  "recoloured: fan_club_daycare 8/9/10 only" % (k, D["title"], sum(ch.values()), ch["fan"], ch["burg"],
                                                               ch["tun"]))
        json.dump(dict(ticket="T-538", batch=3, status="DRAFT -- not in the engine", approved=sorted(APPROVED),
                       directions=summary), open(os.path.join(DRAFT, "directions.json"), "w"), indent=1)
        for p in contact_sheets(DRAFT, states):
            print("  sheet:", p)
    if len(APPROVED) == 1:
        bad = check_engine() or bad
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""The landmarks' rooms, drawn from the story, a pair at a time (T-447, pair 4: the MANSION and DAEMON TOWER).

    python3 tools/gbalandmarkrooms.py                 # report: the re-census of the seven landmarks still mostly
                                                      #   Nintendo's drawing, the proposed pairs, pair 4's groups, and
                                                      #   every other tool's claim on these tiles
    python3 tools/gbalandmarkrooms.py --draft [DIR]   # pair 4's directions drawn in full: per direction each set's
                                                      #   tiles.png and own rows as .pal, the MANSION diary's four
                                                      #   primary tiles, and the contact sheets (gfx/drafts/t447_pair4/)
    python3 tools/gbalandmarkrooms.py --write --approved
                                                      # into the engine -- refused unless APPROVED names a direction
                                                      #   per building (the user, 2026-11-10: A and A); the report
                                                      #   then exits 1 on any difference from that write

THE JOB (the user, 2026-11-10, "The landmarks left"; census item 8). T-447 drew the landmarks' OUTSIDES from the story
(pairs 1-3, tools/gbalandmarks.py). Seven landmarks are still mostly Nintendo's drawing INSIDE: the MANSION (and its
diary), DAEMON TOWER's floors, the LEAGUE, the HALL OF FAME, the S.S. ANNE, the POWER PLANT and TANOBY. USER TOWER is
left for the user (T-447) and DOLDRUM CAVE waits on the user (T-251): neither is drafted here. T-447's rule holds:
two at a time, a sheet and a yes before each pair.

PAIR 4 -- THE TWO CRIME SCENES. Their outsides are already ours (pair 1: the MANSION's burned shell, one stain rising
from the cave-in, racks curved like a rib cage; pair 2: DAEMON TOWER's dots and arched niches), and their insides are
the most Nintendo's of the seven (98% and 90% of their placed tiles). vision 4.5: DAEMON TOWER is Scorn's crime
scene, where CONTEXT and CONTENT stop being an abstraction; 4.24: the MANSION is the campus's burned half, which
"holds the machine's own words" (its four logs, RESPONSE 1001). One is a fire nobody set (heat, ANNEAL, ENTROPY);
the other a process nobody can agree to grieve.

  pokemon_mansion   the MANSION 1F, 2F, 3F, B1F -- and ROUTE 21's station, which borrows its walls and floor (the
                    station's sketch, tiles 350..353 and row 9, is gbastation.py's and is never touched). Own rows
                    7 (the secret switch and the gates it opens), 8 (the window glass), 12 (everything else).
  diary             the MANSION's open diary: primary/building tiles 602, 603, 618, 619 in primary row 5, whose colours
                    are batch D's and fixed. In DAEMONS the "diaries" are the machine's LOGs (RESPONSE 1001), so the
                    book becomes what the log is read from. gbabuilding.LATER_T447 names the four (batch D skips them).
  pokemon_tower     DAEMON TOWER 1F..7F. Own rows 7, 8, 9, 12 -- but in rows 7 and 8 the slots the STONES draw with
                    (1, 2, 8, 10, 11, 12, 15: tools/gbatombstones.py, T-249, the encased screens) keep their colours
                    exactly, and the twelve stone tiles are T-249's: only the floor AROUND the stone in its two
                    floor-layer copies is repainted (gbatombstones writes the face, columns 4..11 rows 3..11, never
                    that floor). The tower is grey until each floor comes back into colour after INIT is rescued
                    (fieldmap.c, FLAG_TOWER_COLOUR_1F..7F; T-430), so every drawing is checked in grey as well: the
                    grey is each colour's luminance, (0.3, 0.59, 0.1133), DaemonsHalftoneLum's weights.

THE RULES ARE THE INTERIOR TOOLS' (gbahomes, gbadwellings, gbamuseum): redrawn IN PLACE. No block, layer, flip,
palette row, behaviour or collision bit moves and no map is touched; only pixels inside tiles change, and every tile
keeps its FOOTPRINT (a transparent pixel stays transparent, a drawn one stays drawn). The engine names blocks in the
MANSION (the switch's two faces 0x314/0x34D and their kin, the gates 0x2F8.. 0x372 the switch swaps, the floors
0x284..0x287): those keep their ids and still read as what they are -- a switch OFF and ON, a gate SHUT and OPEN.
Neither tileset has an animation. 0 new tiles, 0 new palette rows.

Every in-game word: none. This is art.
"""
import collections, contextlib, glob, io, json, math, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import write_pal, read_pal
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t447_pair4")
#  The user's picks, one direction per building. --write refuses while it is empty.
#  the user, 2026-11-10: MANSION A The rack hall, TOWER A The dot screen
APPROVED = {"man": "A", "tow": "A"}

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

#  gbahomes (and gbabuilding under it) read their switches off sys.argv at import (engine.md trap 16): a clean argv.
_argv, sys.argv = sys.argv, ["gbahomes"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import gbahomes as G
finally:
    sys.argv = _argv
GB = G.GB
Cv, H, M, h, v, hv = G.Cv, G.H, G.M, G.h, G.v, G.hv

MAN = G.Set("man", "gTileset_PokemonMansion", [7, 8, 12])
TOW = G.Set("tow", "gTileset_PokemonTower", [7, 8, 9, 12])
SETS = {"man": MAN, "tow": TOW}
G.SETS.update(SETS)                 # Cv and render_map look sets up there
NAMES = {"man": "the MANSION", "tow": "DAEMON TOWER"}

#  others' tiles in these sets, never drawn here
STATION = {350, 351, 352, 353}                     # gbastation.py: the sketch on the station table (row 9)
STONES = [(39, 40, 55, 56), (108, 109, 124, 125), (110, 111, 126, 127)]   # gbatombstones.py (T-249)
STONE_T = {t for s in STONES for t in s}
STONE_FLOOR_COPIES = [(108, 109, 124, 125), (110, 111, 126, 127)]
STONE_FACE = (4, 3, 11, 11)                        # gbatombstones: columns 4..11, rows 3..11 of each 16x16 stone
#  slots the stones draw with, in the tower's rows 7 (purple stones) and 8 (gold stones): kept exactly
FIXED_SLOTS = {("tow", 7): [1, 2, 8, 10, 11, 12, 15], ("tow", 8): [1, 2, 8, 10, 11, 12, 15]}
#  the MANSION's diary: primary/building tiles, primary row 5 (fixed colours) -- gbabuilding.LATER_T447
DIARY = [602, 603, 618, 619]
PROW = 5
VPRI = [G.jasc(daemonslib.upstream(GBA, G.PRI + "/palettes/%02d.pal" % r, binary=True)) for r in range(7)]
TODAY_PAL = {(k, r): read_pal(os.path.join(GBA, S.dir, "palettes/%02d.pal" % r)) for k, S in SETS.items()
             for r in range(16)}


# ============================================================================================ the census (all seven)
LANDMARKS = [
    #  key, tileset symbol, name, what it is in the story, pair
    ("pokemon_mansion", "gTileset_PokemonMansion", "the MANSION", "the campus's burned half; the machine's own words "
     "(4.24)", 4),
    ("pokemon_tower", "gTileset_PokemonTower", "DAEMON TOWER", "Scorn's crime scene; a town that does not know whether "
     "it may grieve (4.5)", 4),
    ("power_plant", "gTileset_PowerPlant", "KEEPALIVE PLANT", "a building still running with nobody connected to it "
     "(4.25)", 5),
    ("tanoby_ruins", "gTileset_TanobyRuins", "TANOBY", "an alphabet nobody reads (4.24)", 5),
    ("pokemon_league", "gTileset_PokemonLeague", "the LEAGUE", "the REVIEW BOARD's four hearing rooms, then AL CLEAR "
     "(6)", 6),
    ("hall_of_fame", "gTileset_HallOfFame", "the HALL OF FAME", "the record that files a person as fields; the UNION "
     "ROOM shares it", 6),
    ("ss_anne", "gTileset_SSAnne", "the S.S. ANNE", "the liner at ARDOR's pier; the SEAGALLOP's sailor (9.17)", 7),
]
PAIRS = [
    (4, "the MANSION + DAEMON TOWER", "the two crime scenes, each the inside of an outside already ours (pairs 1, 2): a "
     "fire nobody set, and a process nobody can agree to grieve. The most Nintendo's of the seven."),
    (5, "KEEPALIVE PLANT + TANOBY", "the two places that outlived their users -- a plant still running with nobody "
     "connected, an alphabet nobody reads; both in gbacaves' colours (batch E), small sets (75 and 68 tiles)."),
    (6, "the LEAGUE + the HALL OF FAME", "the ending walked straight through: the four hearing rooms, AL CLEAR, then the "
     "record; batch G's floors and walls are already ours, the rest is not."),
    (7, "the S.S. ANNE (+ its departure)", "the largest set (227 tiles, 25 rooms) on its own, with its smoke and wake "
     "(census item 10's cutscene) so the liner is ours at the pier and leaving it."),
]


def census_all():
    out = []
    for key, sym, name, story, pair in LANDMARKS:
        c = G.census_set(sym)
        out.append((key, name, c, story, pair))
    return out


# ============================================================================================ roles
#  vanilla's (row, index) -> what that colour was FOR. Structure keeps vanilla's zones as geometry; a direction
#  decides what each zone is made of.
ROLE = {
    "man": {
        12: {1: "wD", 2: "w", 3: "wL", 4: "wDD", 5: "rD", 6: "r", 7: "fDD", 8: "fD", 9: "f", 10: "fL", 11: "face",
             12: "OUT", 13: "gD", 14: "gL", 15: "W"},
        8: {1: "wD", 2: "w", 3: "wL", 4: "wDD", 5: "gl", 6: "glH", 9: "f", 11: "face", 12: "OUT", 13: "gD", 14: "gL",
            15: "W"},
        7: {1: "sD", 2: "s", 3: "sL", 4: "eD", 5: "e", 6: "bD", 7: "b", 12: "OUT", 13: "gD", 14: "gL", 15: "W"},
    },
    "tow": {
        7: {1: "OUT", 2: "gD", 3: "gL", 4: "W", 5: "fD", 6: "f", 7: "fL", 8: "fLL", 9: "pLL", 10: "pD", 11: "p",
            12: "pL", 14: "fDD", 15: "W"},
        8: {1: "OUT", 2: "gD", 3: "gL", 4: "W", 5: "fD", 6: "f", 7: "fL", 8: "fLL", 9: "pLL", 10: "dD", 11: "d",
            12: "dL", 14: "fDD", 15: "W"},
        12: {1: "OUT", 2: "p", 3: "pL", 4: "W", 5: "gD", 6: "f", 11: "pD", 12: "p", 13: "pLL", 14: "pL", 15: "gD"},
        9: {1: "OUT", 2: "gD", 3: "gL", 4: "W", 11: "dD", 12: "d", 13: "c", 14: "cL", 15: "W"},
        0: {i: "x" for i in range(16)},
    },
}

#  each own row's fifteen materials, index 1..15, the same layout in every direction. "@r:i" is a fixed slot, kept as
#  it stands today (the tower's stones).
ROWMATS = {
    ("man", 12): ["OUT", "SHD", "MID", "HI", "WHT", "W1", "W2", "W3", "F1", "F2", "F3", "C1", "C2", "A1", "A2"],
    ("man", 8):  ["OUT", "SHD", "MID", "HI", "WHT", "W1", "W2", "W3", "G1", "G2", "G3", "GH", "F2", "A1", "A2"],
    ("man", 7):  ["OUT", "SHD", "MID", "HI", "WHT", "S1", "S2", "S3", "E1", "E2", "B1", "B2", "B3", "A1", "GL"],
    ("tow", 7):  ["@7:1", "@7:2", "F1", "F2", "F3", "N1", "N2", "@7:8", "N3", "@7:10", "@7:11", "@7:12", "L1", "L2",
                  "@7:15"],
    ("tow", 8):  ["@8:1", "@8:2", "F1", "F2", "F3", "D1", "D2", "@8:8", "D3", "@8:10", "@8:11", "@8:12", "L1", "L2",
                  "@8:15"],
    ("tow", 12): ["OUT", "SHD", "MID", "HI", "WHT", "N1", "N2", "N3", "NT", "S1", "S2", "S3", "L1", "L2", "X"],
    ("tow", 9):  ["OUT", "SHD", "MID", "HI", "WHT", "R1", "R2", "R3", "R4", "L1", "L2", "X", "F1", "F2", "F3"],
}


# ============================================================================================ drawing helpers
def home_row(K, x, y):
    S = SETS.get(K.setkey)
    spec = K.layout[y // 8][x // 8]
    if K.setkey == "P" or spec is None:
        return PROW
    return S.home(spec[0])


def vrole(K, x, y):
    vi = K.vi(x, y)
    if vi is None:
        return None
    return ROLE[K.setkey].get(home_row(K, x, y), {}).get(vi, "x")


def vcol(K, x, y):
    vi = K.vi(x, y)
    if vi is None:
        return None
    r = home_row(K, x, y)
    if K.setkey == "P":
        return VPRI[r][vi]
    return tuple(SETS[K.setkey].vpal[r][vi] if r >= 7 else VPRI[r][vi])


def lum(c):
    return 0.3 * c[0] + 0.59 * c[1] + 0.1133 * c[2]


def disc(K, cx, cy, r, m, ring=None):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            d = math.hypot(x - cx, y - cy)
            if d <= r and (ring is None or d >= r - ring):
                K.px(x, y, m)


def zones(kind):
    """structure: every footprint pixel goes through the direction's zone function for KIND, with vanilla's role"""
    def painter(K, D):
        f = D["zone"]
        K.fn(lambda x, y: f(kind, vrole(K, x, y), x, y, K))
    painter.__name__ = "zones_" + kind
    return painter


# ============================================================================================ the MANSION's groups
def p_floor(K, D):
    """the floor: lit tiles 23/24, shaded 7/8 (vanilla's checker of two 8x8 cells, A and B)"""
    f = D["floor"]
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                t = K.layout[y // 8][x // 8][0]
                shade = t in (7, 8)
                cell = "A" if t in (24, 7) else "B"
                m = f(x % 8, y % 8, cell, shade)
                if vrole(K, x, y) == "OUT" and D.get("floor_keep_out"):
                    m = "OUT"
                K.px(x, y, m)


def p_wood(K, D):
    f = D["wood"]
    K.fn(lambda x, y: f(x % 8, y % 8, K.layout[y // 8][x // 8][0] == 41))


def p_tiled(K, D):
    f = D["tiled"]
    K.fn(lambda x, y: f(x % 8, y % 8, K.layout[y // 8][x // 8][0] == 42, vrole(K, x, y)))


def p_carpet(K, D):
    """1F's long runner (55 its edge, 56 its field): 32 wide as it stands"""
    f = D["carpet"]
    K.fn(lambda x, y: f(x, y % 8, vrole(K, x, y)))


def p_debris(K, D):
    """the burned patches: where vanilla shows bare earth through the floor, its broken tile edges kept as drawn"""
    f = D["debris"]
    K.fn(lambda x, y: f(vrole(K, x, y), x, y, K))


def p_rubble(K, D):
    f = D["rubble"]
    K.fn(lambda x, y: f(vrole(K, x, y), x, y, K))


def p_hole(K, D):
    """the floor's broken edge over the void (FALL_WARP): what is left hanging"""
    f = D["hole"]
    K.fn(lambda x, y: f(vrole(K, x, y), x, y, K))


def p_window(K, D):
    D["window"](K)


def p_rail(K, D):
    D["rail"](K)


def p_switch(on):
    def painter(K, D):
        D["switch"](K, on)
    painter.__name__ = "switch_" + ("on" if on else "off")
    return painter


def p_gate(K, D):
    D["gate"](K)


def p_post(K, D):
    D["post"](K)


def p_diary(K, D):
    D["diary"](K)


MAN_DEBRIS = [3, 4, 5, 6, 19, 20, 21, 22, 35, 36, 37, 38, 43, 51, 52, 53, 54, 59, 70, 71, 72, 73, 86, 88, 89, 102,
              103, 104, 105, 118, 119, 120]
MAN_WALL = [16, 17, 18, 32, 33, 34, 48, 49, 50, 64, 65, 66, 67, 80, 81, 82, 83, 84, 85, 97, 98, 112, 113, 128, 144]
MAN_STAIR = [256, 257, 258, 262, 263, 264, 265, 272, 273, 274, 278, 279, 280, 281, 288, 289, 290, 294, 297, 304, 305,
             306, 309, 311, 312, 313, 320, 321, 322, 325, 327, 328, 329, 336, 337, 338, 339, 341, 342, 345]
GROUPS_MAN = [
    ("floor",   M([24, 23], [23, 24]),                   p_floor,   "the floor, lit (0x284)"),
    ("shade",   M([7, 8], [8, 7]),                       p_floor,   "the floor in a wall's shade (0x285)"),
    ("wood",    M([57, 57], [57, 57]),                   p_wood,    "B1F's boards, lit (0x286)"),
    ("woodsh",  M([41, 41], [41, 41]),                   p_wood,    "B1F's boards in shade (0x287)"),
    ("tiled",   M([58, 58], [58, 58]),                   p_tiled,   "2F's south terrace, lit"),
    ("tiledsh", M([42, 42], [42, 42]),                   p_tiled,   "the terrace in shade"),
    ("carpet",  M([55, 56, 56, h(55)], [55, 56, 56, h(55)]), p_carpet, "1F's long runner"),
    ("rubble1", M([9, 10], [25, 26]),                    p_rubble,  "rubble on the burned floor"),
    ("rubble2", M([11, 12], [27, 28]),                   p_rubble,  "rubble on the burned floor"),
    ("hole1",   M([13, 14]),                             p_hole,    "the floor's broken edge over the drop"),
    ("hole2",   M([29, 30]),                             p_hole,    "the floor's broken edge over the drop"),
    ("hole3",   M([45, 46]),                             p_hole,    "the floor's broken edge over the drop"),
    ("window",  M([74, 75, h(75), h(74)], [90, 91, h(91), h(90)], [106, 107, h(107), h(106)],
                  [122, 123, h(123), h(122)]),           p_window,  "a window, its frame and glass (rows 12 and 8)"),
    ("rail",    M([99, 100, 100, 101], [115, 116, 116, 117]), p_rail, "the gallery's rail (2F's south edge)"),
    ("switch",  M([266, 267], [282, 283], [298, 299], [314, 315]), p_switch(False),
     "the secret switch, OFF (0x314, its foot 0x31C)"),
    ("switchon", M([330, 331], [346, 347], [298, 299], [314, 315]), p_switch(True),
     "the secret switch, ON (0x34D: set by the scripts, placed by no map)"),
    ("gate",    M([268, 269, 269, 270], [284, 285, 285, 286], [300, 301, 301, 302], [316, 317, 317, 318]), p_gate,
     "the gate the switch swaps, shut (0x2F8..0x302)"),
    ("post",    M([332, 333], [348, 349], [348, 349]),   p_post,    "the gate's post, along (0x350..0x372)"),
] + [("debris_%d" % t, M([t]), p_debris, "a burned patch") for t in MAN_DEBRIS] \
  + [("wall_%d" % t, M([t]), zones("wall"), "a wall's top, face or skirting") for t in MAN_WALL] \
  + [("stair_%d" % t, M([t]), zones("stair"), "the stairs and their rails") for t in MAN_STAIR]
#  0x34D's tiles are placed by no map, only set by the scripts: drawn too
NAMED_UNPLACED = {("man", 330), ("man", 331), ("man", 346), ("man", 347)}
GROUPS_P = [("diary", M([602, 603], [618, 619]), p_diary, "the diary on the table -> the LOG (primary row 5)")]


# ============================================================================================ DAEMON TOWER's groups
#  the lit floor, by its place in the 16x16 block (1 2 / 17 18): what a shaded tile is compared against
LITFLOOR = {(0, 0): 1, (1, 0): 2, (0, 1): 17, (1, 1): 18}


def floor_shaded(K, x, y):
    """vanilla's shade, read as geometry: a pixel is in shade where it differs from the lit floor at that place"""
    lit = TOW.van[LITFLOOR[(x // 8) % 2, (y // 8) % 2]]
    return K.vi(x, y) != lit[(y % 8) * 8 + x % 8]


def p_tfloor(K, D):
    f = D["tfloor"]
    K.fn(lambda x, y: f(x % 16, y % 16, floor_shaded(K, x, y)))


def p_tedge(K, D):
    """the floor's shadow pieces that lie on the top layer (58..61): shade over a transparent field"""
    f = D["tfloor"]
    K.fn(lambda x, y: f((x + K.ox) % 16, y % 16, True))


def p_niche(K, D):
    D["niche"](K)


def p_desk(K, D):
    D["desk"](K)


def p_circle(K, D):
    D["circle"](K)


def p_pedestal(K, D):
    D["pedestal"](K)


TOW_WALL = [14, 15, 30, 31, 46, 47, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
            82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]
GROUPS_TOW = [
    ("tfloor",  M([1, 2], [17, 18]),                     p_tfloor,  "the floor (0x282)"),
    ("tshade1", M([33, 34], [49, 50]),                   p_tfloor,  "the floor in the wall's shade"),
    ("tshade2", M([16, 34], [17, 18]),                   p_tfloor,  "the floor at a shadow's corner"),
    ("tshade3", M([1, 105], [17, 18]),                   p_tfloor,  "the floor by the stairs"),
    ("tshade4", M([106, 107], [17, 18]),                 p_tfloor,  "the floor by the stairs"),
    ("tedge58", M([58]),                                 p_tedge,   "a shadow laid on the floor"),
    ("tedge59", M([59]),                                 p_tedge,   "a shadow laid on the floor"),
    ("tedge60", M([60, 61]),                             p_tedge,   "a shadow laid on the floor"),
    ("niche",   M([3, 4], [19, 20]),                     p_niche,   "the back wall's panels (0x298)"),
    ("niche53", M([3, 53], [19, 20]),                    p_niche,   "a panel's right end"),
    ("niche54", M([54, 4], [19, 20]),                    p_niche,   "a panel's left end"),
    ("niche2",  M([35, 36], [51, 52]),                   p_niche,   "the round wall's panels (0x2A0)"),
    ("rim",     M([None, 21], [None, 37]),               zones("rim"), "the round wall's rim"),
    ("rim2",    M([22, None], [38, None]),               zones("rim"), "the round wall's rim"),
    ("desk",    M([96, 97, 114, 115], [112, 113, 114, 115], [118, 118, 100, None], [101, 117, 116, None],
                  [102, h(102), 103, h(103)]),           p_desk,    "1F's desk (0x2C8..0x2D4, COUNTER)"),
    ("desk2",   M([98, 99]),                             p_desk,    "1F's desk, its end"),
    ("circle",  M([11, 12, 13, h(13), h(12), h(11)], [27, 28, 29, h(29), h(28), h(27)],
                  [43, 44, 45, h(45), h(44), h(43)], [v(43), v(44), v(45), hv(45), hv(44), hv(43)],
                  [v(27), v(28), v(29), hv(29), hv(28), hv(27)], [v(11), v(12), v(13), hv(13), hv(12), hv(11)]),
     p_circle, "5F's circle, where the player is made whole (row 9)"),
    ("pedestal", M([9, 10], [25, 26], [41, 42]),         p_pedestal, "7F's two pedestals (primary row 0)"),
] + [("twall_%d" % t, M([t]), zones("twall"), "the walls, stairs and pillars") for t in TOW_WALL]
#  the shadow pieces sit at a known column of their block
TEDGE_OX = {"tedge58": 0, "tedge59": 8, "tedge60": 0}


# ============================================================================================ resolving
def mats_for(D, key):
    m = dict(D["mat"]["*"])
    m.update(D["mat"].get(key, {}))
    for (k, r), slots in FIXED_SLOTS.items():
        if k == key:
            for i in slots:
                m["@%d:%d" % (r, i)] = tuple(TODAY_PAL[k, r][i])
    return m


def set_palettes(D, S):
    mat = mats_for(D, S.key)
    out = {}
    for r in range(16):
        if r in S.rows:
            out[r] = [tuple(TODAY_PAL[S.key, r][0])] + [tuple(mat[n]) for n in ROWMATS[S.key, r]]
        else:
            out[r] = [tuple(c) for c in TODAY_PAL[S.key, r]]
    return out


def resolve_into(mats, base, rows, mat, own, index):
    """G.resolve with this tool's materials; a material a row lacks is matched to the nearest colour"""
    Dm = {"mat": mat, "_index": index}
    return G.resolve(mats, base, rows, Dm, own)


def all_groups():
    for key, layout, painter, what in GROUPS_MAN:
        yield key, "man", layout, painter, what
    for key, layout, painter, what in GROUPS_TOW:
        yield key, "tow", layout, painter, what
    for key, layout, painter, what in GROUPS_P:
        yield key, "P", layout, painter, what


def draw(D, only=None):
    """-> {setkey: (tiles, palettes)}, diary {tile: px}, owner {(setkey, t): group}. ONLY limits it to one building"""
    out = {k: ([t[:] for t in S.cur], set_palettes(D[k] if k in D else D, S)) for k, S in SETS.items()}
    prim, owner = {}, {}
    for key, setkey, layout, painter, what in all_groups():
        bkey = "man" if setkey == "P" else setkey
        if only and bkey != only:
            continue
        DD = D[bkey]
        K = Cv(layout, setkey)
        K.ox = TEDGE_OX.get(key, 0)
        painter(K, DD)
        if setkey == "P":
            mat = mats_for(DD, "P")
            for t, mats in K.tiles().items():
                if t in DIARY and ("P", t) not in owner:
                    prim[t] = resolve_into(mats, G.ptile(t), {PROW: 1}, mat, {}, {})
                    owner["P", t] = key
            continue
        S = SETS[setkey]
        mat = mats_for(DD, setkey)
        spals = out[setkey][1]
        index = {(r, n): i + 1 for r in S.rows for i, n in enumerate(ROWMATS[S.key, r])}
        own = {r: spals[r] for r in S.rows}
        for t, mats in K.tiles().items():
            if (setkey, t) in owner or t >= S.nvan:
                continue
            if t not in S.use and (setkey, t) not in NAMED_UNPLACED:
                continue
            if setkey == "man" and t in STATION or setkey == "tow" and t in STONE_T:
                continue
            rows = dict(S.use[t]["rows"]) if t in S.use and S.use[t]["rows"] else {7: 1}
            out[setkey][0][t] = resolve_into(mats, S.van[t], rows, mat, own, index)
            owner[setkey, t] = key
    if not only or only == "tow":
        stone_floor(D["tow"], out["tow"])
    return out, prim, owner


STONE_FLOOR_AT = {t: q for copy in STONE_FLOOR_COPIES for q, t in enumerate(copy)}


def stone_floor_px(t, k):
    """(floor, shade) of pixel k of stone tile t. The floor is read off VANILLA's pixel there -- the floor's own slots
    5, 6, 7, 14 and 8, outside the screen gbatombstones writes -- never off the engine's, which after a write holds
    this tool's floor (reading the engine made a second write repaint its own floor: 2026-11-10, the build)"""
    q = STONE_FLOOR_AT.get(t)
    if q is None:
        return False, False
    x, y = (q % 2) * 8 + k % 8, (q // 2) * 8 + k // 8
    fx0, fy0, fx1, fy1 = STONE_FACE
    if fx0 <= x <= fx1 and fy0 <= y <= fy1:
        return False, False
    vv = TOW.van[t][k]
    return vv in (5, 6, 7, 8, 14), vv in (5, 14)


def stone_floor(DD, st):
    """the floor AROUND the stones in their floor-layer copies (T-249's tiles): only the floor's pixels (stone_floor_px)
    are repainted, in this direction's floor; the stone is not touched"""
    tiles, pals = st
    mat = mats_for(DD, "tow")
    index = {n: i + 1 for i, n in enumerate(ROWMATS["tow", 7])}
    f = DD["tfloor"]
    for copy in STONE_FLOOR_COPIES:
        for q, t in enumerate(copy):
            px = TOW.cur[t][:]
            for k in range(64):
                floor, shade = stone_floor_px(t, k)
                if floor:
                    x, y = (q % 2) * 8 + k % 8, (q // 2) * 8 + k // 8
                    n = f(x, y, shade)
                    px[k] = index.get(n) or G.nearest(mat[n], pals[7])
            tiles[t] = px


# ============================================================================================ the directions
#  A direction is {"man": {...}, "tow": {...}}: each building's materials and painters, with a title and lines.

# ---------------------------------------------------------------------------------------- shared shapes
def soot(y, h, strength=3):
    """how sooty a wall face is at row y of h (heaviest at its top: the smoke rose)"""
    return max(0, strength - (y * (strength + 1)) // max(1, h))


def crackle(x, y, s=0, cell=6):
    """a glaze's crazing: the borders of a Voronoi network of jittered seeds (True on a crack), period 24 so it
    tiles across 8x8 tiles -- irregular polygons, never a grid that could read as letters"""
    best = []
    for gy in range(-1, 2):
        for gx in range(-1, 2):
            cx, cy = (x // cell + gx) % (24 // cell), (y // cell + gy) % (24 // cell)
            px = (x // cell + gx) * cell + H(cx, cy, s) % cell
            py = (y // cell + gy) * cell + H(cy, cx, s + 1) % cell
            best.append((px - x) ** 2 + (py - y) ** 2)
    best.sort()
    return best[1] - best[0] <= 3


def frame_box(K, x0, y0, x1, y1, m):
    for x in range(x0, x1 + 1):
        K.px(x, y0, m)
        K.px(x, y1, m)
    for y in range(y0, y1 + 1):
        K.px(x0, y, m)
        K.px(x1, y, m)


# ---------------------------------------------------------------------------------------- MANSION A: THE RACK HALL
def A_man_zone(kind, role, x, y, K):
    if role in ("OUT", None):
        return "OUT"
    if role == "gD":
        return "SHD"
    if role == "gL":
        return "HI"
    if role == "W":
        return "WHT"
    if kind == "wall":
        if role in ("w", "wL"):                       # the wall's top seen from above: riveted plate
            if (x % 8 == 1 and y % 8 == 1):
                return "HI"
            return "W2" if role == "w" else "W3"
        if role in ("wD", "wDD"):                     # the skirting: one steel band, riveted
            return "HI" if (x % 6 == 2 and y % 8 == 4) else "W1"
        if role == "face":                            # the face: a rack front -- rails, rows of dead lights
            if x % 4 == 0:
                return "W1"
            if y % 3 == 1 and x % 4 == 2:
                return "A1" if H(x, y, 3) % 11 == 0 else "OUT"
            return "W3" if soot(y % 8, 8, 1) == 0 else "W2"
        if role in ("fDD", "fD", "f", "fL"):
            return {"fDD": "SHD", "fD": "W1", "f": "W2", "fL": "W3"}[role]
        if role in ("rD", "r"):
            return "C1" if role == "rD" else "C2"
    if kind == "stair":                               # steel treads, the rail a cable tray
        if role in ("rD", "r"):
            return "C1" if role == "rD" else "C2"
        if role in ("fDD", "fD"):
            return "F1"
        if role in ("f", "fL", "face"):
            return "F3" if y % 4 == 0 else "F2"
        if role in ("wDD", "wD"):
            return "W1"
        return "W2" if role == "w" else "W3"
    return "MID"


def A_man_floor(x, y, cell, shade):
    """raised-floor plates: one plate per 8x8 cell, a seam on its edge and a pin at its corner; B cells perforated"""
    base = ["F2", "F1"][shade]
    if x == 0 or y == 0:
        return "SHD" if shade else "F1"
    if x == 1 and y == 1:
        return "HI" if not shade else "F2"
    if cell == "B" and x % 2 == 0 and y % 2 == 0 and 2 <= x <= 6 and 2 <= y <= 6:
        return "F1" if not shade else "SHD"
    if not shade and x == 7 - y and H(x, y, 9) % 3 == 0:      # soot dragged across a plate
        return "MID"
    return base


def A_man_wood(x, y, shade):
    """B1F: an open grating over the cable floor"""
    if x % 4 == 0 or y % 4 == 0:
        return "F1" if not shade else "SHD"
    return "C1" if (x // 4 + y // 4) % 2 else ("A2" if shade else "SHD")


def A_man_tiled(x, y, shade, role):
    """the terrace: ash over steel deck, pale where the rain has run"""
    if role == "OUT":
        return "OUT"
    if y % 4 == 3:
        return "F1"
    return ("MID" if H(x, y, 4) % 5 == 0 else "HI") if not shade else "F2"


def A_man_carpet(x, y, role):
    """the runner becomes the cable trench: a channel, three bundles running its length"""
    if role in ("OUT",) or x in (0, 31):
        return "OUT"
    if x in (1, 30):
        return "F3"
    if x in (8, 9, 22, 23) or 14 <= x <= 17:
        return "C2" if (y + x) % 6 else "MID"
    if x in (10, 21, 13, 18):
        return "SHD"
    return "C1"


def A_man_debris(role, x, y, K):
    """bare floor where the plates burned off: ash over the void floor, plates' broken edges kept"""
    if role == "OUT":
        return "OUT"
    if role in ("fL", "face", "W"):
        return "F2"
    if role == "f":
        return "F1"
    n = H(x, y, 7) % 9
    if n == 0:
        return "HI"
    if n < 3:
        return "MID"
    return "A2" if role == "fDD" else "SHD"


def A_man_rubble(role, x, y, K):
    """fallen plates and burnt cards"""
    if role == "OUT":
        return "OUT"
    if role in ("fL", "face", "W", "gL"):
        return "W3" if (x + y) % 5 else "A1"
    if role in ("f",):
        return "W2"
    if role in ("fD",):
        return "W1"
    return "A2"


def A_man_hole(role, x, y, K):
    """the floor's edge over the drop: a plate's frame and a joist hanging"""
    if role == "OUT":
        return "OUT"
    if y < 2:
        return "F2"
    if y < 4:
        return "W1"
    return "SHD" if x % 4 else "W2"


def A_man_window(K):
    """blown out: the frame steel, the glass gone dark with a skin of ash; one bead of quicksilver on the sill"""
    W, Hh = K.w, K.h
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if r in ("gl", "glH", "gD", "gL", "W") and home_row(K, x, y) == 8:
            if (x + y) % 7 == 0:
                return "G3"
            if y > Hh - 10 and H(x, y, 2) % 4 == 0:
                return "G2"
            return "G1" if y < 12 else "G2"
        if r in ("w", "wL"):
            return "W2"
        if r in ("wD", "wDD"):
            return "W1"
        if r == "face":
            return "W3"
        return "SHD"
    K.fn(f)
    K.px(W // 2 - 4, Hh - 9, "A1")
    K.px(W // 2 + 3, Hh - 9, "A1")


def A_man_rail(K):
    """the gallery's edge: a cable tray, its rungs"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if y in (2, 3, 12, 13):
            return "C2" if y in (2, 12) else "C1"
        if x % 4 == 0:
            return "W2"
        return "SHD"
    K.fn(f)


def A_man_switch(K, on):
    """the secret switch: a breaker cabinet, 16x32 -- two lamps at its head (dark: open; red: closed), a lever, a
    plinth. vanilla's ears and paws are not followed: only where pixels may go"""
    def f(x, y):
        if y < 16:
            return "S2" if 2 <= x <= 13 else "S1"
        if y < 26:
            return "S3" if x in (3, 4) else "S2"
        return "B1" if y >= 29 else "S1"
    K.fn(f)
    K.rim("OUT")
    for x in range(3, 13):
        K.px(x, 4, "S3")
    for cx in (5, 10):
        disc(K, cx + 0.5, 9.5, 1.6, "E2" if on else "E1")
        K.px(cx, 9, "WHT" if on else "S1")
    for y in range(17, 26):
        K.px(8, y, "OUT")
    K.px(7, 18 if on else 24, "S3")
    K.px(8, 18 if on else 24, "S3")
    K.px(9, 18 if on else 24, "S3")
    for x in range(2, 14):
        K.px(x, 27, "B3")


def A_man_gate(K):
    """the gate the switch swaps: a rack door of louvred steel"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if y % 4 == 0:
            return "B1"
        if y % 4 == 1:
            return "B3"
        return "B2" if x % 16 else "B1"
    K.fn(f)


def A_man_post(K):
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if y % 6 == 0:
            return "HI"
        return "W2" if (x % 8) in (3, 4) else "W1"
    K.fn(f)


def A_diary(K):
    """the LOG: fanfold printout, sprocket holes down both edges, a column of marks (no letters)"""
    def f(x, y):
        if x in (1, 14):
            return "hole" if y % 3 == 0 else "paper"
        if y % 8 == 7:
            return "fold"
        if 3 <= x <= 12 and y % 2 == 1 and H(x // 2, y, 6) % 4 != 0:
            return "ink"
        return "paper"
    K.fn(f)
    K.rim("edge")


# ---------------------------------------------------------------------------------------- MANSION B: ANNEALED
def B_man_zone(kind, role, x, y, K):
    if role in ("OUT", None):
        return "OUT"
    if role == "gD":
        return "SHD"
    if role == "gL":
        return "HI"
    if role == "W":
        return "WHT"
    if kind == "wall":
        if role in ("w", "wL"):                       # plaster top, burnt umber, grained
            return "W1" if H(x // 2, y, 3) % 6 == 0 else ("W2" if role == "w" else "W3")
        if role in ("wD", "wDD"):                     # the skirting charred through
            return "SHD" if H(x // 2, y // 3, 4) % 4 == 0 else "A2"
        if role == "face":                            # the face fired like a glaze: crazed, browned toward its top
            if crackle(x, y, 1):
                return "A2" if soot(y % 8, 8, 2) else "W2"
            return "W3" if y % 8 > 2 else "F3"
        if role in ("fDD", "fD", "f", "fL"):
            return {"fDD": "SHD", "fD": "A2", "f": "W2", "fL": "W3"}[role]
        if role in ("rD", "r"):
            return "C1" if role == "rD" else "C2"
    if kind == "stair":
        if role in ("rD", "r"):                       # wrought iron, heat-blued
            return "C1" if role == "rD" else "C2"
        if role in ("fDD", "fD"):
            return "A2"
        if role in ("f", "fL", "face"):
            return "F3" if (x + 2 * y) % 9 == 0 else "F2"
        if role in ("wDD", "wD"):
            return "SHD"
        return "W2" if role == "w" else "W3"
    return "MID"


def B_man_floor(x, y, cell, shade):
    """parquet charred into an alligator check: blocks of char split by pale fissures"""
    bx, by = (x + (2 if cell == "B" else 0)) // 4, y // 3
    fiss = (x + (2 if cell == "B" else 0)) % 4 == 0 or y % 3 == 0
    if fiss:
        return "F3" if not shade and H(bx, by, 5) % 2 else "F2"
    if shade:
        return "A2"
    return "F1" if H(bx, by, 1 if cell == "A" else 2) % 3 else "F2"


def B_man_wood(x, y, shade):
    """B1F's boards, checked by the heat along the grain"""
    if y % 4 == 0:
        return "SHD"
    if (x + (y // 4) * 3) % 6 == 0:
        return "A2"
    return "F1" if shade else ("F2" if H(x, y // 4, 8) % 4 else "F3")


def B_man_tiled(x, y, shade, role):
    """the terrace's tiles, their glaze bubbled"""
    if role == "OUT":
        return "OUT"
    if x % 4 == 0 or y % 4 == 0:
        return "W2" if not shade else "SHD"
    if (x + y) % 3 == 0 and H(x, y, 3) % 2:
        return "WHT" if not shade else "W3"
    return "W3" if not shade else "W2"


def B_man_carpet(x, y, role):
    """the runner burnt to a dark ribbon, its edge frayed"""
    if role == "OUT":
        return "OUT"
    if x <= 2 or x >= 29:
        return "C2" if (x + y) % 2 else "F2"
    if x <= 4 or x >= 27:
        return "C2" if H(x, y, 4) % 3 else "C1"
    return "C1" if (x // 3 + y) % 5 else "A2"


def B_man_debris(role, x, y, K):
    """fallen plaster and lath"""
    if role == "OUT":
        return "OUT"
    if role in ("fL", "face", "W"):
        return "F2"
    if role == "f":
        return "F1"
    if (x + y * 3) % 7 == 0:
        return "W2"
    return "W3" if H(x, y, 2) % 5 == 0 else "A2" if role == "fDD" else "SHD"


def B_man_rubble(role, x, y, K):
    if role == "OUT":
        return "OUT"
    if role in ("fL", "face", "W", "gL"):
        return "W3"
    if role == "f":
        return "W2"
    if role == "fD":
        return "F1"
    return "A2"


def B_man_hole(role, x, y, K):
    """charred joists over the drop"""
    if role == "OUT":
        return "OUT"
    if y < 2:
        return "F1"
    return "A2" if x % 5 in (1, 2) else "SHD"


def B_man_window(K):
    """the glass slumped in the heat: warped panes, ochre, a drip at the sill"""
    Hh = K.h
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if home_row(K, x, y) == 8 and r in ("gl", "glH", "gD", "gL", "W"):
            wave = (x + int(2 * math.sin(y / 3.0))) % 6
            if wave == 0:
                return "GH"
            return "G2" if y > Hh // 2 else ("G3" if wave < 3 else "G2")
        if r in ("w", "wL"):
            return "W2"
        if r in ("wD", "wDD"):
            return "A2"
        return "W3" if r == "face" else "SHD"
    K.fn(f)


def B_man_rail(K):
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if y in (2, 12):
            return "C2"
        if y in (3, 13):
            return "C1"
        return "C1" if x % 5 == 0 else ("SHD" if (x + y) % 5 else "C2")
    K.fn(f)


def B_man_switch(K, on):
    """a bust in fired clay on a plinth (no face drawn: a head turned away); its eyes a glaze, black or red"""
    def f(x, y):
        if y < 15:
            d = math.hypot(x - 7.5, y - 8)
            return "S3" if d < 4 else "S2"
        if y < 18:
            return "S1"
        return "B2" if y < 29 else "B1"
    K.fn(f)
    K.rim("OUT")
    for cx in (5, 10):
        K.px(cx, 8, "E2" if on else "OUT")
        K.px(cx, 9, "E1" if on else "SHD")
    for y in range(19, 28, 3):
        for x in range(3, 13):
            K.px(x, y, "B3")


def B_man_gate(K):
    """an iron gate bent by the heat"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        bend = int(1.5 * math.sin((y + 2) / 5.0)) if 4 < (x % 16) < 12 else 0
        if (x + bend) % 4 == 0:
            return "B3"
        if y in (2, 3, 28, 29):
            return "B2"
        return "B1"
    K.fn(f)


def B_man_post(K):
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        return "C2" if (x % 8) == 3 else "C1" if (x % 8) == 4 else "SHD"
    K.fn(f)


def B_diary(K):
    """the notebook, its pages browned and curled at the corners, a column of marks"""
    def f(x, y):
        if (x < 2 or x > 13) and (y < 2 or y > 13):
            return "edge"
        if x in (7, 8):
            return "fold"
        if (x + y) > 24 or (15 - x + y) > 25:
            return "burnt"
        if (2 <= x <= 5 or 10 <= x <= 13) and y % 2 == 0 and H(x // 2, y, 3) % 3:
            return "ink"
        return "paper"
    K.fn(f)
    K.rim("edge")


# ---------------------------------------------------------------------------------------- MANSION C: QUICKSILVER
def C_man_zone(kind, role, x, y, K):
    if role in ("OUT", None):
        return "OUT"
    if role == "gD":
        return "SHD"
    if role == "gL":
        return "HI"
    if role == "W":
        return "WHT"
    if kind == "wall":
        if role in ("w", "wL"):                       # lead flashing
            return "W2" if role == "w" else "W3"
        if role in ("wD", "wDD"):                     # a lead skirting, beads gathered at its foot
            return "A1" if (y % 8 == 6 and H(x, 1, 12) % 7 == 0) else "W1"
        if role == "face":                            # cold silver; quicksilver run down it in beads
            trail = H(x, 0, 11) % 5 == 0
            if trail and y % 4 == 3:
                return "A1"
            if trail and y % 4 == 0:
                return "SHD"
            return "W3" if (x + y) % 7 else "HI"
        if role in ("fDD", "fD", "f", "fL"):
            return {"fDD": "SHD", "fD": "W1", "f": "W2", "fL": "W3"}[role]
        if role in ("rD", "r"):
            return "C1" if role == "rD" else "C2"
    if kind == "stair":
        if role in ("rD", "r"):
            return "C1" if role == "rD" else "C2"
        if role in ("fDD", "fD"):
            return "F1"
        if role in ("f", "fL", "face"):
            return "F3" if y % 4 == 1 else "F2"
        if role in ("wDD", "wD"):
            return "W1"
        return "W2" if role == "w" else "W3"
    return "MID"


def C_man_floor(x, y, cell, shade):
    """dark polished slate, one slab per cell, a reflection's streak across it and a bead at the joint"""
    if x == 0 or y == 0:
        return "SHD"
    if (x, y) == (1, 1) and cell == "A":
        return "A1"
    if not shade and (x + y) in (8, 9) and cell == "A":
        return "F3"
    if not shade and (x - y) in (3,) and cell == "B":
        return "F3"
    return "F1" if shade else "F2"


def C_man_wood(x, y, shade):
    """B1F: lead sheet, its seams rolled"""
    if x % 8 == 0:
        return "W3" if not shade else "W2"
    if x % 8 == 1:
        return "SHD"
    return "W1" if shade else ("W2" if H(x // 8, y, 4) % 6 else "W3")


def C_man_tiled(x, y, shade, role):
    """the terrace a mirror: what it shows is the sky"""
    if role == "OUT":
        return "OUT"
    if x % 8 == 0 or y % 8 == 0:
        return "SHD"
    if (x + y) % 8 == 2:
        return "WHT" if not shade else "HI"
    return "HI" if not shade else "MID"


def C_man_carpet(x, y, role):
    """the runner a channel of quicksilver, slow, a meniscus at each bank"""
    if role == "OUT":
        return "OUT"
    if x <= 1 or x >= 30:
        return "F1"
    if x in (2, 29):
        return "SHD"
    if x in (3, 28):
        return "WHT"
    if (x * 3 + y * 5) % 11 == 0:
        return "WHT"
    return "C2" if (x + y // 2) % 4 else "C1"


def C_man_debris(role, x, y, K):
    """where the floor broke: the slate's edges kept, mirror glass scattered in the dust"""
    if role == "OUT":
        return "OUT"
    if role in ("fL", "face", "W"):
        return "F2"
    if role == "f":
        return "F1"
    n = H(x, y, 5) % 13
    if n == 0:
        return "A1"
    if n == 1:
        return "HI"
    return "MID" if role == "fD" else "SHD"


def C_man_rubble(role, x, y, K):
    if role == "OUT":
        return "OUT"
    if role in ("fL", "face", "W", "gL"):
        return "WHT" if (x * 2 + y) % 4 == 0 else "HI"
    if role == "f":
        return "MID"
    return "SHD"


def C_man_hole(role, x, y, K):
    if role == "OUT":
        return "OUT"
    if y < 2:
        return "F2"
    if y == 2:
        return "A1" if x % 3 == 0 else "SHD"
    return "SHD"


def C_man_window(K):
    """mirror-backed: the window gives the room back to itself"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if home_row(K, x, y) == 8 and r in ("gl", "glH", "gD", "gL", "W"):
            if (x - y) % 9 in (0, 1):
                return "GH"
            return "G3" if (x - y) % 9 < 5 else "G2"
        if r in ("w", "wL"):
            return "W2"
        if r in ("wD", "wDD"):
            return "W1"
        return "W3" if r == "face" else "SHD"
    K.fn(f)


def C_man_rail(K):
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if y in (2, 12):
            return "C2"
        if y in (3, 13):
            return "C1"
        return "W3" if x % 6 == 0 else "SHD"
    K.fn(f)


def C_man_switch(K, on):
    """a mercury tilt switch: a glass bulb on a stand -- the bead lies away from the contacts (dark) or across them,
    and the lamp below it lit red"""
    def f(x, y):
        if y < 16:
            return "S1"
        if y < 26:
            return "S2" if 5 <= x <= 10 else "S1"
        return "B1"
    K.fn(f)
    K.rim("OUT")
    for x in range(2, 14):                        # the bulb, tilted
        for y in range(4, 12):
            if ((x - 7.5) / 6.0) ** 2 + ((y - 7.5 + (x - 7.5) * (0.25 if on else -0.25)) / 3.4) ** 2 <= 1:
                K.px(x, y, "GL" if (x + y) % 5 == 0 else "S3")
    bx = 4 if not on else 11
    disc(K, bx, 8 + (1 if on else 0), 1.6, "A1")
    K.px(bx - 1, 7 + (1 if on else 0), "WHT")
    K.px(12, 8, "OUT")
    K.px(12, 9, "OUT")
    for cx in (5, 10):
        K.px(cx, 20, "E2" if on and cx == 10 else "E1")
        K.px(cx, 21, "E2" if on and cx == 10 else "E1")


def C_man_gate(K):
    """a pane of glass in a silver frame: shut, it shows you yourself"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if y in (0, 1, 30, 31) or x % 16 in (0, 15):
            return "B3"
        if (x - y) % 10 in (0, 1):
            return "GL"
        return "B2" if (x - y) % 10 < 5 else "B1"
    K.fn(f)


def C_man_post(K):
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "OUT"
        if (x % 8) == 3:
            return "WHT"
        return "W3" if (x % 8) == 4 else "W2"
    K.fn(f)


def C_diary(K):
    """a terminal's face, cracked: dark glass, rows of grey marks, a red cursor, a crack across a corner"""
    def f(x, y):
        if x in (0, 15) or y in (0, 15):
            return "edge"
        if x == y + 4 or x == y + 5:
            return "crack"
        if 2 <= x <= 12 and y % 3 == 2 and H(x // 2, y, 9) % 3:
            return "ink"
        if (x, y) in ((4, 12), (5, 12)):
            return "red"
        return "glass"
    K.fn(f)


# ---------------------------------------------------------------------------------------- TOWER A: THE DOT SCREEN
def dotted(x, y, density, s=0, pitch=4):
    """a halftone dot at (x, y) of a screen of this pitch: density 0 (none) .. 3 (solid)"""
    cx, cy = x % pitch, y % pitch
    row = (y // pitch) % 2
    if row:
        cx = (x + pitch // 2) % pitch
    if density <= 0:
        return False
    if density == 1:
        return cx == pitch // 2 and cy == pitch // 2
    if density == 2:
        return abs(cx - pitch // 2) + abs(cy - pitch // 2) <= 1
    return abs(cx - pitch // 2) + abs(cy - pitch // 2) <= 2


def A_tow_zone(kind, role, x, y, K):
    if role in ("OUT", None):
        return "OUT" if K.setkey != "P" else "OUT"
    if kind == "rim":
        if role in ("W", "gL"):
            return "@7:15" if role == "W" else "N3"
        return "N2"
    if kind == "twall":                               # the tower's stone, screened
        if role in ("W", "pLL"):
            return "WHT"
        if role in ("pL",):
            return "N3" if not dotted(x, y, 1) else "N2"
        if role in ("p",):
            return "N2" if not dotted(x, y, 2) else "N1"
        if role in ("pD",):
            return "N1"
        if role == "gD":
            return "SHD"
        if role == "f":
            return "MID"
    return "MID"


def A_tow_floor(x, y, shade):
    """pale flags under a dot screen: sparse in the light, dense in the wall's shade"""
    if dotted(x, y, 2 if shade else 1):
        return "F1"
    if not shade and dotted(x + 2, y, 1):
        return "F2"
    return "F2" if shade else "F3"


def A_tow_niche(K):
    """the panels are rows of arched niches cut into screened stone (the outside's seven bands), each with a light"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "@7:1"
        if r in ("W", "gL", "pLL"):
            return "@7:15" if r == "W" else "N3"
        if y >= K.h - 3:
            return "N1"
        cx, cy = x % 8, y % 10
        inside = 2 <= cx <= 5 and 2 <= cy <= 8 and not (cy == 2 and cx in (2, 5))
        if inside:
            if cx in (3, 4) and cy == 6:
                return "L1"
            if cx in (3, 4) and cy == 5:
                return "L2"
            return "@7:1" if cy > 3 else "N1"
        return "N2" if dotted(x, y, 1, pitch=4) else "N3"
    K.fn(f)


def A_tow_desk(K):
    """1F's desk: the same screened stone, a slab top"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "@8:1"
        if r in ("W", "dL", "gL"):
            return "D3"
        if r in ("d",):
            return "D2" if not dotted(x, y, 1) else "D1"
        return "D1"
    K.fn(f)


def A_tow_circle(K):
    """5F's circle: a ring of dots that thickens to one clean line -- a picture coming into resolution"""
    c = (K.w - 1) / 2.0
    def f(x, y):
        d = math.hypot(x - c, y - c)
        a = math.atan2(y - c, x - c)
        if 19 <= d <= 21:
            return "R4"
        if 15 <= d < 19:
            return "R2" if dotted(int(x), int(y), 2 + int(3 * (a + math.pi) / (2 * math.pi)) % 2, pitch=3) else None
        if d < 4:
            return "L2"
        return None
    for y in range(K.h):
        for x in range(K.w):
            if K.foot(x, y):
                m = f(x, y)
                K.out[y][x] = m if m else ("R1" if vrole(K, x, y) != "OUT" else "OUT")
    K.rim("OUT")


def A_tow_pedestal(K):
    """7F's pedestals, in primary row 0's colours: screened stone"""
    def f(x, y):
        r = vrole(K, x, y)
        if K.edge(x, y) or x in (0, K.w - 1):
            return "p_out"
        return "p_l" if dotted(x, y, 1, pitch=3) else "p_m"
    K.fn(f)


# ---------------------------------------------------------------------------------------- TOWER B: THE NICHES
def B_tow_zone(kind, role, x, y, K):
    if role in ("OUT", None):
        return "OUT"
    if kind == "rim":
        return "@7:15" if role == "W" else "N3" if role == "gL" else "N2"
    if kind == "twall":
        if role in ("W", "pLL"):
            return "WHT"
        if role == "pL":
            return "N3"
        if role == "p":
            if x % 4 == 1 and y % 4 == 1:
                return "L1"
            return "N2"
        if role == "pD":
            return "N1"
        if role == "gD":
            return "SHD"
        if role == "f":
            return "MID"
    return "MID"


def B_tow_floor(x, y, shade):
    """square slabs: a columbarium's floor, or a machine room's -- the same drawing"""
    if x % 8 == 0 or y % 8 == 0:
        return "F1" if shade else "F2"
    if (x % 8, y % 8) == (1, 1):
        return "F3" if not shade else "F2"
    return "F1" if shade and (x + y) % 2 else ("F2" if shade else "F3")


def B_tow_niche(K):
    """a grid of identical small niches, each with one point of light: a candle, or a status light"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "@7:1"
        if r in ("W", "gL", "pLL"):
            return "@7:15" if r == "W" else "N3"
        cx, cy = x % 4, y % 4
        if cx == 0 or cy == 0:
            return "N3"
        if (cx, cy) == (2, 2):
            return "L1" if H(x // 4, y // 4, 3) % 5 else "L2"
        return "@7:1" if cy == 3 else "N1"
    K.fn(f)


def B_tow_desk(K):
    """1F's desk: an intake ledger, ruled"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "@8:1"
        if r in ("W", "dL", "gL"):
            return "D3" if y % 3 else "D2"
        return "D1" if r == "dD" else "D2"
    K.fn(f)


def B_tow_circle(K):
    """5F's circle: a ring of the niches' lights, laid in the floor"""
    c = (K.w - 1) / 2.0
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            d = math.hypot(x - c, y - c)
            a = math.atan2(y - c, x - c)
            m = "R1"
            if 17 <= d <= 21:
                k = int((a + math.pi) / (2 * math.pi) * 24)
                ca = -math.pi + (k + 0.5) * 2 * math.pi / 24
                px_, py_ = c + 19 * math.cos(ca), c + 19 * math.sin(ca)
                dd = math.hypot(x - px_, y - py_)
                m = "L1" if dd < 1.2 else "R3" if dd < 2.4 else "R2"
            if vrole(K, x, y) == "OUT":
                m = "OUT"
            K.out[y][x] = m
    K.rim("OUT")


def B_tow_pedestal(K):
    def f(x, y):
        if K.edge(x, y) or x in (0, K.w - 1):
            return "p_out"
        if x % 4 in (1, 2) and y % 5 in (1, 2, 3):
            return "p_out" if y % 5 == 3 else "p_dk"
        return "p_m"
    K.fn(f)


# ---------------------------------------------------------------------------------------- TOWER C: THE PROOF
def C_tow_zone(kind, role, x, y, K):
    if role in ("OUT", None):
        return "OUT"
    if kind == "rim":
        return "@7:15" if role == "W" else "F1" if role == "gL" else "N2"
    if kind == "twall":
        if role in ("W", "pLL"):
            return "WHT"
        if role == "pL":
            return "HI"
        if role == "p":
            return "N2"
        if role == "pD":
            return "N1"
        if role == "gD":
            return "SHD"
        if role == "f":
            return "MID"
    return "MID"


def C_tow_floor(x, y, shade):
    """a printer's rosette: four screens at four angles -- grey, it is one even tone; in colour, it is made of dots"""
    k = (x + 2 * y) % 5
    j = (2 * x - y) % 5
    if shade:
        if k == 0 or j == 0:
            return "F1"
        return "N1" if (x + y) % 4 == 0 else "F2"
    if k == 0:
        return "L1"        # cyan
    if j == 0:
        return "L2"        # magenta
    if (x * 3 + y) % 7 == 0:
        return "N3"        # yellow
    return "F3"


def C_tow_niche(K):
    """the panels are a press sheet's margin: a registration mark per panel, and a colour bar along its foot"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "@7:1"
        if r in ("W", "gL", "pLL"):
            return "@7:15" if r == "W" else "F1"
        cx, cy = x % 16 - 7.5, y - 7.5
        d = math.hypot(cx, cy)
        if 3 <= d <= 4 or (abs(cx) < 0.6 and abs(cy) < 6) or (abs(cy) < 0.6 and abs(cx) < 6):
            return "@7:1"
        if y >= K.h - 4:
            return ["L1", "L2", "N3", "@7:1"][(x // 4) % 4]
        return "F3"
    K.fn(f)


def C_tow_desk(K):
    """1F's desk: a light table, its top lit"""
    def f(x, y):
        r = vrole(K, x, y)
        if r == "OUT":
            return "@8:1"
        if r in ("W", "dL", "gL"):
            return "D3"
        return "D2" if r == "d" else "D1"
    K.fn(f)


def C_tow_circle(K):
    """5F's circle: a registration mark laid in the floor, its four quarters the four inks"""
    c = (K.w - 1) / 2.0
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            d = math.hypot(x - c, y - c)
            m = "R1"
            if 18 <= d <= 20 or (abs(x - c) < 0.8 and d < 22) or (abs(y - c) < 0.8 and d < 22):
                m = "R4"
            elif 8 <= d <= 14:
                q = (x > c) + 2 * (y > c)
                m = ["L1", "L2", "X", "R4"][q]
            if vrole(K, x, y) == "OUT":
                m = "OUT"
            K.out[y][x] = m
    K.rim("OUT")


def C_tow_pedestal(K):
    def f(x, y):
        if K.edge(x, y) or x in (0, K.w - 1):
            return "p_out"
        return "p_out" if y % 3 == 0 else "p_l"
    K.fn(f)


# ---------------------------------------------------------------------------------------- the directions' tables
#  primary rows' colours, by name, for the diary (row 5) and 7F's pedestals (row 0): resolved to the nearest there
DIARY_MATS = {
    "A": dict(paper=(213, 222, 222), hole=(82, 82, 106), fold=(164, 180, 189), ink=(123, 123, 123),
              edge=(82, 82, 106)),
    "B": dict(paper=(213, 213, 148), fold=(148, 131, 90), ink=(82, 82, 106), burnt=(131, 115, 74),
              edge=(82, 82, 106)),
    "C": dict(glass=(0, 0, 0), ink=(164, 180, 189), crack=(213, 222, 222), red=(205, 82, 65), edge=(82, 82, 106)),
}
PED = dict(p_out=(82, 82, 106), p_m=(150, 144, 134), p_l=(232, 224, 206), p_dk=(123, 123, 123))


def direction(name, title, lines, man_mat, tow_mat, man, tow):
    D = dict(name=name, title=title, lines=lines)
    D["man"] = dict(mat={"*": man_mat, "P": DIARY_MATS[name]}, zone=man["zone"], floor=man["floor"],
                    wood=man["wood"], tiled=man["tiled"], carpet=man["carpet"], debris=man["debris"],
                    rubble=man["rubble"], hole=man["hole"], window=man["window"], rail=man["rail"],
                    switch=man["switch"], gate=man["gate"], post=man["post"], diary=man["diary"])
    tm = dict(tow_mat)
    tm.update(PED)
    D["tow"] = dict(mat={"*": tm}, zone=tow["zone"], tfloor=tow["floor"], niche=tow["niche"], desk=tow["desk"],
                    circle=tow["circle"], pedestal=tow["pedestal"])
    return D


A = direction(
    "A", "THE RACK HALL / THE DOT SCREEN",
    ["MANSION: the machine's housing, burnt -- raised-floor plates, rack fronts with rows of dead lights, the runner a",
     "cable trench, the switch a breaker cabinet with two lamps (dark: open; red: closed), the gates louvred rack doors,",
     "ash and charcoal steel, one bead of quicksilver; the diary a fanfold LOG printout.",
     "TOWER: the outside carried in -- pale flags under a dot screen (sparse in the light, dense in shade), the panels",
     "rows of arched niches each with a warm light, 5F's circle a ring of dots thickening into one clean line."],
    dict(OUT=(30, 28, 34), SHD=(64, 62, 70), MID=(108, 106, 112), HI=(164, 162, 164), WHT=(224, 222, 216),
         W1=(52, 52, 60), W2=(86, 88, 98), W3=(128, 130, 138), F1=(72, 70, 76), F2=(116, 114, 118),
         F3=(152, 150, 148), C1=(38, 42, 50), C2=(92, 106, 124), A1=(214, 220, 228), A2=(58, 50, 46),
         G1=(26, 30, 36), G2=(54, 60, 70), G3=(96, 104, 114), GH=(176, 182, 190),
         S1=(48, 52, 60), S2=(88, 94, 104), S3=(138, 144, 152), E1=(70, 26, 26), E2=(226, 44, 38),
         B1=(56, 58, 66), B2=(96, 100, 108), B3=(146, 150, 156), GL=(232, 236, 240)),
    dict(OUT=(40, 38, 46), SHD=(84, 80, 88), MID=(132, 126, 128), HI=(196, 190, 184), WHT=(240, 236, 228),
         F1=(112, 104, 100), F2=(178, 170, 158), F3=(228, 222, 208), N1=(98, 86, 120), N2=(150, 136, 168),
         N3=(196, 186, 210), NT=(120, 108, 140), S1=(90, 80, 108), S2=(140, 128, 156), S3=(190, 180, 204),
         L1=(244, 196, 110), L2=(255, 236, 180), X=(160, 112, 60),
         R1=(200, 192, 178), R2=(120, 112, 128), R3=(160, 150, 170), R4=(70, 64, 80),
         D1=(140, 130, 124), D2=(186, 176, 164), D3=(230, 222, 208)),
    dict(zone=A_man_zone, floor=A_man_floor, wood=A_man_wood, tiled=A_man_tiled, carpet=A_man_carpet,
         debris=A_man_debris, rubble=A_man_rubble, hole=A_man_hole, window=A_man_window, rail=A_man_rail,
         switch=A_man_switch, gate=A_man_gate, post=A_man_post, diary=A_diary),
    dict(zone=A_tow_zone, floor=A_tow_floor, niche=A_tow_niche, desk=A_tow_desk, circle=A_tow_circle,
         pedestal=A_tow_pedestal))

B = direction(
    "B", "ANNEALED / THE NICHES",
    ["MANSION: the house went through the kiln -- the walls' plaster crazed like a glaze and browned toward the ceiling,",
     "the parquet charred into an alligator check, the runner burnt to a frayed ribbon, the glass slumped, the gates",
     "iron bent by the heat, the switch a fired-clay bust whose eyes are glaze (black, or red); the diary a scorched book.",
     "TOWER: the ambiguity made architecture -- every wall a grid of identical small niches, each with one point of",
     "light (a candle, or a status light), square slabs underfoot, 5F's circle a ring of the same lights."],
    dict(OUT=(40, 30, 26), SHD=(78, 60, 50), MID=(134, 112, 94), HI=(196, 178, 154), WHT=(240, 230, 210),
         W1=(110, 76, 52), W2=(168, 128, 92), W3=(224, 204, 170), F1=(70, 50, 40), F2=(120, 86, 60),
         F3=(176, 138, 98), C1=(60, 30, 30), C2=(120, 60, 48), A1=(200, 196, 188), A2=(54, 40, 34),
         G1=(70, 60, 40), G2=(140, 120, 70), G3=(190, 170, 110), GH=(236, 224, 176),
         S1=(120, 70, 46), S2=(168, 104, 66), S3=(206, 146, 100), E1=(110, 20, 20), E2=(210, 46, 40),
         B1=(48, 44, 52), B2=(88, 84, 96), B3=(132, 128, 146), GL=(236, 228, 212)),
    dict(OUT=(36, 34, 40), SHD=(78, 74, 82), MID=(128, 122, 126), HI=(192, 186, 182), WHT=(238, 234, 226),
         F1=(122, 118, 122), F2=(168, 162, 160), F3=(206, 200, 192), N1=(76, 66, 96), N2=(124, 112, 146),
         N3=(176, 166, 194), NT=(100, 90, 120), S1=(86, 76, 104), S2=(136, 124, 152), S3=(186, 176, 200),
         L1=(250, 214, 140), L2=(160, 224, 160), X=(150, 100, 60),
         R1=(176, 170, 166), R2=(110, 102, 118), R3=(206, 186, 140), R4=(60, 56, 70),
         D1=(110, 96, 86), D2=(160, 146, 130), D3=(214, 204, 186)),
    dict(zone=B_man_zone, floor=B_man_floor, wood=B_man_wood, tiled=B_man_tiled, carpet=B_man_carpet,
         debris=B_man_debris, rubble=B_man_rubble, hole=B_man_hole, window=B_man_window, rail=B_man_rail,
         switch=B_man_switch, gate=B_man_gate, post=B_man_post, diary=B_diary),
    dict(zone=B_tow_zone, floor=B_tow_floor, niche=B_tow_niche, desk=B_tow_desk, circle=B_tow_circle,
         pedestal=B_tow_pedestal))

C = direction(
    "C", "QUICKSILVER / THE PROOF",
    ["MANSION: the island's own metal -- dark polished slate, silver walls with quicksilver run down them in beads,",
     "the runner a slow channel of it, mirror-backed windows, glass gates in silver frames; the switch a mercury tilt",
     "switch (the bead off the contacts, or across them with a red lamp); the diary a terminal's cracked face.",
     "TOWER: HALFTONE is a printer's word -- the floor a four-ink rosette that is one even tone in grey and only dots in",
     "colour, so a floor coming back into colour comes back as dots; registration marks and a colour bar on the walls."],
    dict(OUT=(22, 24, 32), SHD=(52, 56, 68), MID=(104, 110, 122), HI=(170, 176, 186), WHT=(236, 240, 246),
         W1=(64, 70, 82), W2=(110, 116, 128), W3=(150, 156, 166), F1=(36, 40, 50), F2=(58, 64, 76),
         F3=(120, 128, 142), C1=(130, 136, 146), C2=(184, 190, 198), A1=(226, 232, 240), A2=(44, 46, 56),
         G1=(70, 78, 92), G2=(118, 126, 140), G3=(160, 168, 180), GH=(220, 226, 234),
         S1=(40, 44, 56), S2=(80, 86, 100), S3=(150, 170, 186), E1=(80, 30, 34), E2=(232, 52, 48),
         B1=(80, 90, 106), B2=(130, 142, 158), B3=(196, 204, 214), GL=(244, 248, 252)),
    dict(OUT=(34, 34, 40), SHD=(80, 80, 88), MID=(132, 132, 138), HI=(196, 196, 198), WHT=(244, 244, 240),
         F1=(150, 148, 146), F2=(190, 188, 184), F3=(236, 234, 226), N1=(70, 70, 80), N2=(124, 122, 134),
         N3=(232, 210, 60), NT=(98, 96, 108), S1=(84, 84, 96), S2=(132, 132, 144), S3=(184, 184, 192),
         L1=(60, 176, 214), L2=(214, 64, 150), X=(232, 210, 60),
         R1=(220, 218, 212), R2=(120, 120, 128), R3=(170, 168, 172), R4=(40, 40, 48),
         D1=(132, 132, 138), D2=(196, 196, 198), D3=(250, 250, 240)),
    dict(zone=C_man_zone, floor=C_man_floor, wood=C_man_wood, tiled=C_man_tiled, carpet=C_man_carpet,
         debris=C_man_debris, rubble=C_man_rubble, hole=C_man_hole, window=C_man_window, rail=C_man_rail,
         switch=C_man_switch, gate=C_man_gate, post=C_man_post, diary=C_diary),
    dict(zone=C_tow_zone, floor=C_tow_floor, niche=C_tow_niche, desk=C_tow_desk, circle=C_tow_circle,
         pedestal=C_tow_pedestal))
STYLES = {"A": A, "B": B, "C": C}


# ============================================================================================ rendering
BG, INK, RED, SOFT = (250, 248, 242), (24, 24, 24), (120, 20, 30), (90, 90, 90)


def grey(im):
    """the tower as HALFTONE shows it before INIT is rescued: each colour's luminance (DaemonsHalftoneLum)"""
    g = im.convert("RGB").copy()
    px = g.load()
    for y in range(g.height):
        for x in range(g.width):
            r, gg, b = px[x, y]
            l = int(min(255, 0.3 * r + 0.59 * gg + 0.1133 * b))
            px[x, y] = (l, l, l)
    return g


def room(m, st, crop=None, prim=None):
    """a map as the engine draws it -- state (sets, diary) or None for today"""
    state = None
    if st is not None:
        sets, diary = st
        state = (sets, diary or None)
    im = G.render_map(m, state)
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
    return im


def text(d, xy, s, fill=INK):
    d.text(xy, s, fill=fill)


ROOMS_MAN = [("PokemonMansion_1F", "the MANSION 1F", None), ("PokemonMansion_B1F", "the MANSION B1F", None),
             ("Route21_North_Station", "ROUTE 21's station (borrows its walls)", None)]
ROOMS_TOW = [("PokemonTower_2F", "DAEMON TOWER 2F, grey (before INIT)", None, True),
             ("PokemonTower_2F", "2F in colour (after)", None, False),
             ("PokemonTower_5F", "5F, the circle (colour)", None, False),
             ("PokemonTower_7F", "7F, grey", None, True),
             ("PokemonTower_1F", "1F, the desk (colour)", None, False)]
DETAILS = [("man", "PokemonMansion_1F", (0, 2, 8, 9), "1F: the switch, a burned patch, the table", None),
           ("man", "PokemonMansion_2F", (8, 0, 17, 6), "2F: the windows, the diary, a wall's face", None),
           ("man", "PokemonMansion_B1F", (17, 24, 27, 31), "B1F: the diary, the switch, the boards", None),
           ("man", "PokemonMansion_1F", (5, 12, 16, 18), "1F: the runner, the stairs, the floor", None),
           ("tow", "PokemonTower_7F", (7, 0, 17, 6), "7F: the panels, the stones, the pedestals (colour)", False),
           ("tow", "PokemonTower_7F", (7, 0, 17, 6), "7F as HALFTONE shows it (grey)", True),
           ("tow", "PokemonTower_5F", (6, 5, 16, 13), "5F: the circle", False),
           ("tow", "PokemonTower_1F", (12, 8, 22, 17), "1F: the desk, the stairs", False)]
SWITCH_STATES = ["PokemonMansion_1F"]


def gate_open_render(st, m, crop):
    """a map with every switch-swapped block shown in its other state (the switch ON, the gates' partners)"""
    return room(m, st, crop)


def contact_sheets(out_dir, states):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: Nintendo's drawing in Nintendo's colours (the MANSION's statue, gates and diary;",
                              "DAEMON TOWER's floor, panels, desk and circle). The tower's STONES are T-249's encased",
                              "screens (gbatombstones) and stay; the station's sketch is gbastation's and stays."])}
    for k in STYLES:
        titles[k] = ("%s %s" % (k, STYLES[k]["title"]), STYLES[k]["lines"])
    pad = 10
    paths = []
    for which, rooms in (("mansion", ROOMS_MAN), ("tower", ROOMS_TOW)):
        blocks = []
        for k in names:
            st = states[k]
            ims = []
            for spec in rooms:
                m, cap, cr = spec[0], spec[1], spec[2]
                im = room(m, st, cr)
                if len(spec) > 3 and spec[3]:
                    im = grey(im)
                ims.append((im, cap))
            t, lines = titles[k]
            th = 8 + 12 * len(lines) + 16
            W = sum(i.width for i, _ in ims) + pad * (len(ims) + 1)
            im = Image.new("RGB", (max(W, 900), th + max(i.height for i, _ in ims) + pad), BG)
            d = ImageDraw.Draw(im)
            text(d, (pad, 6), t, RED)
            for j, s in enumerate(lines):
                text(d, (pad + 230, 6 + 12 * j), s)
            x = pad
            for i, cap in ims:
                text(d, (x, th - 13), cap, SOFT)
                im.paste(i, (x, th))
                x += i.width + pad
            blocks.append(im)
        W = max(b.width for b in blocks)
        sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
        d = ImageDraw.Draw(sh)
        text(d, (pad, 8), "T-447 DRAFT, pair 4 -- %s, real rooms at 1x, three directions beside today's (redrawn in "
                          "place: no block, collision or palette row moves; 0 new tiles)" %
             ("the MANSION's rooms" if which == "mansion" else "DAEMON TOWER's floors, grey and in colour"), INK)
        y = 30
        for b in blocks:
            sh.paste(b, (0, y))
            y += b.height
        p = os.path.join(out_dir, "t447p4_%s_1x.png" % which)
        sh.save(p)
        paths.append(p)
    #  3x details
    for part, idxs in ((1, (0, 1, 2, 3)), (2, (4, 5, 6, 7))):
        rowsim = []
        for k in names:
            crops = []
            for i in idxs:
                key, m, cr, cap, g = DETAILS[i]
                im = room(m, states[k], cr)
                if g:
                    im = grey(im)
                crops.append((im.resize((im.width * 3, im.height * 3), Image.NEAREST), cap))
            rowsim.append((k, crops))
        cw = sum(c.width for c, _ in rowsim[0][1]) + pad * (len(idxs) + 1) + 130
        ch = max(c.height for c, _ in rowsim[0][1]) + 24
        det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
        d = ImageDraw.Draw(det)
        text(d, (pad, 8), "T-447 DRAFT, pair 4 -- details at 3x (%s)" %
             ("the MANSION" if part == 1 else "DAEMON TOWER"), INK)
        y = 30
        for k, crops in rowsim:
            text(d, (pad, y + 6), titles[k][0][:18], RED)
            x = 130
            for c, cap in crops:
                text(d, (x, y + 2), cap, SOFT)
                det.paste(c, (x, y + 16))
                x += c.width + pad
            y += ch
        p = os.path.join(out_dir, "t447p4_detail_3x_%d.png" % part)
        det.save(p)
        paths.append(p)
    #  the switch and gates in both states, at 3x (the script's other faces: ON, gates open)
    paths.append(switch_sheet(out_dir, states))
    #  the tiles at 3x, each set in its home rows, and the diary
    cols = []
    for k in names:
        st = states[k]
        imgs = []
        for key, S in SETS.items():
            if st:
                tiles, pals = st[0][key]
            else:
                tiles, pals = S.cur, {r: TODAY_PAL[key, r] for r in range(16)}
            n = (S.nvan + 15) // 16
            im = Image.new("RGB", (128, n * 8), (236, 236, 236))
            o = im.load()
            for t in range(S.nvan):
                if t not in S.use and (key, t) not in NAMED_UNPLACED:
                    continue
                r = S.home(t) if t in S.use else 7
                pal = pals[r] if r >= 7 else G.PPAL[r]
                for q in range(64):
                    vv = tiles[t][q]
                    o[(t % 16) * 8 + q % 8, (t // 16) * 8 + q // 8] = tuple(pal[vv]) if vv else (200, 200, 200)
            #  only the rows that hold placed tiles
            used_rows = sorted({t // 16 for t in range(S.nvan) if t in S.use or (key, t) in NAMED_UNPLACED})
            strip = Image.new("RGB", (128, 8 * len(used_rows)), (236, 236, 236))
            for j, r in enumerate(used_rows):
                strip.paste(im.crop((0, r * 8, 128, r * 8 + 8)), (0, j * 8))
            imgs.append((S.dir.split("/")[-1] + " (rows of the sheet that maps place)", strip))
        dim = Image.new("RGB", (16, 16), (236, 236, 236))
        dpx = st[1] if st and st[1] else {}
        o = dim.load()
        for q, t in enumerate(DIARY):
            px = dpx.get(t) or G.PTILES_NOW[t]
            for k2 in range(64):
                vv = px[k2]
                o[(q % 2) * 8 + k2 % 8, (q // 2) * 8 + k2 // 8] = tuple(G.PPAL[PROW][vv]) if vv else (200, 200, 200)
        imgs.append(("the diary (primary 602/603/618/619, row 5)", dim))
        hh = sum(i.height * 3 + 16 for _, i in imgs)
        col = Image.new("RGB", (384, hh), BG)
        y = 0
        dd = ImageDraw.Draw(col)
        for lab, i in imgs:
            dd.text((0, y), lab, fill=SOFT)
            col.paste(i.resize((i.width * 3, i.height * 3), Image.NEAREST), (0, y + 14))
            y += i.height * 3 + 16
        cols.append((titles[k][0], col))
    W = sum(c.width + pad for _, c in cols) + pad
    sh = Image.new("RGB", (W, max(c.height for _, c in cols) + 50), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 6), "T-447 DRAFT, pair 4 -- the tiles at 3x, each in its home row (grey: transparent; only the sheet's "
                      "rows that maps place)", INK)
    x = pad
    for t, c in cols:
        text(d, (x, 26), t[:40], RED)
        sh.paste(c, (x, 42))
        x += c.width + pad
    p = os.path.join(out_dir, "t447p4_tiles_3x.png")
    sh.save(p)
    paths.append(p)
    return paths


def obj_image(st, setkey, layout):
    """an object's tiles as they stand, over the floor's colour"""
    S = SETS[setkey]
    tiles, pals = st[0][setkey] if st else (S.cur, {r: TODAY_PAL[setkey, r] for r in range(16)})
    K = Cv(layout, setkey)
    im = Image.new("RGB", (K.w, K.h), (120, 120, 120))
    o = im.load()
    for ty, r in enumerate(K.layout):
        for tx, spec in enumerate(r):
            if spec is None:
                continue
            t, fl = spec
            row = S.home(t) if t in S.use else 7
            pal = pals[row]
            for k in range(64):
                x, y = k % 8, k // 8
                sx = 7 - x if "h" in fl else x
                sy = 7 - y if "v" in fl else y
                vv = tiles[t][sy * 8 + sx]
                if vv:
                    o[tx * 8 + x, ty * 8 + y] = tuple(pal[vv])
    return im


def switch_sheet(out_dir, states):
    """the MANSION's switch OFF and ON, and the gate it swaps, per direction, at 3x (the scripts set them)"""
    pad = 10
    objs = [("switch OFF (0x314)", M([266, 267], [282, 283], [298, 299], [314, 315])),
            ("switch ON (0x34D)", M([330, 331], [346, 347], [298, 299], [314, 315])),
            ("the gate, shut", M([268, 269, 269, 270], [284, 285, 285, 286], [300, 301, 301, 302],
                                 [316, 317, 317, 318])),
            ("its post", M([332, 333], [348, 349], [348, 349]))]
    rows = []
    for k in states:
        ims = [(obj_image(states[k], "man", lay), cap) for cap, lay in objs]
        rows.append((k, [(i.resize((i.width * 3, i.height * 3), Image.NEAREST), c) for i, c in ims]))
    colw = [max(i.width, 130) for i, _ in rows[0][1]]
    cw = max(900, 130 + sum(w + pad for w in colw))
    ch = max(i.height for i, _ in rows[0][1]) + 24
    sh = Image.new("RGB", (cw, ch * len(rows) + 30), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 8), "T-447 DRAFT, pair 4 -- the MANSION's secret switch OFF and ON and the gate it swaps, 3x (the "
                      "scripts set these blocks; ON is placed by no map)", INK)
    y = 30
    for k, ims in rows:
        text(d, (pad, y + 6), k, RED)
        x = 130
        for (i, cap), w in zip(ims, colw):
            text(d, (x, y + 2), cap, SOFT)
            sh.paste(i, (x, y + 16))
            x += w + pad
        y += ch
    p = os.path.join(out_dir, "t447p4_switch_3x.png")
    sh.save(p)
    return p


# ============================================================================================ report
def claims():
    """every other tool that names these tilesets or the diary's tiles"""
    out = collections.defaultdict(list)
    pats = {"pokemon_mansion": "man", "PokemonMansion": "man", "pokemon_tower": "tow", "PokemonTower": "tow"}
    me = os.path.basename(__file__)
    for f in sorted(glob.glob(os.path.join(ROOT, "tools", "*.py"))):
        if os.path.basename(f) == me:
            continue
        src = open(f, encoding="utf-8", errors="ignore").read()
        for p, k in pats.items():
            if p in src and os.path.basename(f) not in out[k]:
                out[k].append(os.path.basename(f))
        if re.search(r"\b602\b.*\b603\b.*\b618\b.*\b619\b", src):
            out["diary"].append(os.path.basename(f))
    return out


def report():
    bad = 0
    print("T-447 -- the landmarks' rooms. RE-CENSUS against today's engine (placed tiles still Nintendo's drawing, "
          "gbahomes' measure:\n  a tile counts if a map places it and its pixels equal pret's):\n")
    for key, name, c, story, pair in census_all():
        print("    %-16s %-18s %3d of %3d vanilla (%3d%%); rows %s; maps %d; pair %d" %
              (key, name, c["vanilla"], c["used"], round(100 * c["vanilla"] / max(1, c["used"])), c["rows"],
               len(c["maps"]), pair))
    print("    (USER TOWER is left for the user with T-447; DOLDRUM CAVE waits on the user, T-251: neither drafted)")
    print("\n  the pairs, in order:")
    for n, what, why in PAIRS:
        print("    %d  %-34s %s" % (n, what, why))
    owner = {}
    for key, setkey, layout, painter, what in all_groups():
        for r in layout:
            for s in r:
                if s is not None:
                    t = s if isinstance(s, int) else s[0]
                    owner.setdefault((setkey, t), key)
    print("\n  pair 4's groups:")
    print("  %-12s %-4s %5s %6s %4s  %s" % ("group", "set", "tiles", "draws", "maps", "what"))
    seen = set()
    for key, setkey, layout, painter, what in all_groups():
        base = re.sub(r"_\d+$", "", key)
        if (setkey, base) in seen and base != key:
            continue
        seen.add((setkey, base))
        if setkey == "P":
            ts = DIARY
            draws = sum(G.PUSE[t]["draws"] for t in ts if t in G.PUSE)
            maps = {m for t in ts if t in G.PUSE for m in G.PUSE[t]["maps"]}
        else:
            S = SETS[setkey]
            ts = sorted(t for (sk, t), kk in owner.items() if sk == setkey and re.sub(r"_\d+$", "", kk) == base
                        and (t in S.use or (sk, t) in NAMED_UNPLACED) and t < S.nvan)
            draws = sum(S.use[t]["n"] for t in ts if t in S.use)
            maps = {m for t in ts if t in S.use for m in S.use[t]["maps"]}
        print("  %-12s %-4s %5d %6d %4d  %s" % (base, setkey, len(ts), draws, len(maps), what))
    for key, S in SETS.items():
        mine = {t for (sk, t) in owner if sk == key}
        others = STATION if key == "man" else STONE_T
        used = {t for t in S.use if t < S.nvan and any(S.cur[t])}
        stray = sorted(t for t in used if t not in mine and t not in others)
        rows = sorted({r for t in used for r in S.use[t]["rows"]})
        foreign = sorted(r for r in rows if r >= 7 and r not in S.rows + ([9] if key == "man" else [11]))
        print("  %s: %d placed tiles, %d in a group, %d another tool's (%s); in no group: %s; rows placed %s, own %s%s"
              % (S.dir.split("/")[-1], len(used), len(used & mine), len(used & others),
                 "gbastation's sketch" if key == "man" else "gbatombstones' stones", stray or "none", rows, S.rows,
                 ("; !! placed in a row this tool does not own: %s" % foreign) if foreign else ""))
        bad |= bool(stray) or bool(foreign)
    #  the diary: batch D must skip it, and nothing else may draw it
    later = getattr(GB, "LATER_T447", None)
    if later is None:
        print("  !! gbabuilding.LATER_T447 is missing: batch D does not know the diary is T-447's")
        bad = 1
    elif set(later) != set(DIARY):
        print("  !! gbabuilding.LATER_T447 %s is not the diary %s" % (sorted(later), DIARY))
        bad = 1
    elif not set(DIARY) <= set(GB.LATER):
        print("  !! gbabuilding.LATER does not include LATER_T447: its write would draw the diary")
        bad = 1
    else:
        maps = sorted({m for t in DIARY if t in G.PUSE for m in G.PUSE[t]["maps"]})
        print("  the diary: gbabuilding.LATER_T447 names its 4 tiles (batch D skips them); placed on %s" % ", ".join(maps))
    #  other tools on these tilesets: what each owns, and that neither side can undo the other
    cl = claims()
    print("  other tools naming the MANSION's tileset: %s" % ", ".join(cl["man"]))
    print("  other tools naming DAEMON TOWER's tileset: %s" % ", ".join(cl["tow"]))
    print("    gbastation: appends the sketch (tiles 350..353, row 9) only if it is missing; never written here")
    print("    gbatombstones: writes the stones' faces (columns 4..11, rows 3..11) in slots 1 and 8 only; the stones "
          "and those slots are kept here")
    print("    gbapreviews: the map-name cards (pictures, not these tiles); companion_export: names only")
    known = {"gbastation.py", "gbatombstones.py", "gbapreviews.py", "companion_export.py", "check_lexicon.py",
             "port_dialogue.py", "gbadocs.py", "port_hearsay.py", "gbalandmarks.py"}
    new = sorted(set(cl["man"] + cl["tow"]) - known)
    if new:
        print("  !! a tool this one does not know names these tilesets: %s -- read it before a write" % new)
        bad = 1
    #  each direction: the stones untouched, the fixed slots kept, the station untouched
    for k, D in STYLES.items():
        sets, prim, own = draw(D)
        tt, tp = sets["tow"]
        for t in STONE_T:
            for q in range(64):
                a, b2 = tt[t][q], TOW.cur[t][q]
                if a != b2 and not stone_floor_px(t, q)[0]:
                    print("  !! %s: stone tile %d pixel %d changed (not the floor around it)" % (k, t, q))
                    bad = 1
                    break
        for (sk, r), slots in FIXED_SLOTS.items():
            for i in slots:
                if tuple(tp[r][i]) != tuple(TODAY_PAL[sk, r][i]):
                    print("  !! %s: tower row %d slot %d changed: the stones draw with it" % (k, r, i))
                    bad = 1
        mt, mp = sets["man"]
        if any(mt[t] != MAN.cur[t] for t in STATION) or [tuple(c) for c in mp[9]] != [tuple(c) for c in TODAY_PAL["man", 9]]:
            print("  !! %s: the station's sketch (gbastation) changed" % k)
            bad = 1
    print("  every direction keeps the stones (but the floor around them), the stones' slots, and the station's sketch")
    print("  scripted blocks: the switch 0x314/0x315/0x316 <-> 0x34D/0x34E/0x34F and the gates 0x2F8..0x372 keep "
          "their ids; their tiles are drawn as OFF/ON and SHUT (switch sheet)")
    return bad


def check_engine():
    """with a pick approved, the engine must be exactly what `--write --approved` makes"""
    bad = 0
    for bkey, pick in APPROVED.items():
        sets, prim, _ = draw(STYLES[pick], only=bkey)
        S = SETS[bkey]
        off = [t for t in range(len(S.cur)) if sets[bkey][0][t] != S.cur[t]]
        rows = [r for r in S.rows if [tuple(c) for c in sets[bkey][1][r]] != [tuple(c) for c in TODAY_PAL[bkey, r]]]
        dia = [t for t in prim if prim[t] != G.PTILES_NOW[t]] if bkey == "man" else []
        if off or rows or dia:
            print("  !! %s: the engine differs from `--write --approved` (%s) in tiles %s rows %s diary %s"
                  % (NAMES[bkey], pick, off[:12], rows, dia))
            bad = 1
    if APPROVED and not bad:
        print("  the engine matches `--write --approved` (%s)" % APPROVED)
    return bad


def main():
    if WRITE:
        if "--approved" not in ARGS or not APPROVED:
            print("  --write refused: T-447 pair 4 is a draft. APPROVED is %s; the user picks a direction per building "
                  "first, it goes\n  into APPROVED ({\"man\": X, \"tow\": Y}), then --write --approved writes "
                  "pokemon_mansion's tiles and rows 7, 8, 12,\n  the diary's four primary tiles, and pokemon_tower's "
                  "tiles and rows 7, 8, 9, 12 (never the stones' slots)." % (APPROVED or "empty"))
            return 1
        for bkey, pick in APPROVED.items():
            sets, prim, _ = draw(STYLES[pick], only=bkey)
            S = SETS[bkey]
            G.save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[bkey][0], os.path.join(GBA, S.dir, "tiles.png"))
            for r in S.rows:
                write_pal(os.path.join(GBA, S.dir, "palettes", "%02d.pal" % r), sets[bkey][1][r])
            if prim:
                pt = list(G.PTILES_NOW)
                for t, px in prim.items():
                    pt[t] = px
                G.save_like(os.path.join(GBA, G.PRI, "tiles.png"), pt, os.path.join(GBA, G.PRI, "tiles.png"))
            print("  written: %s, direction %s" % (NAMES[bkey], pick))
        return 0
    bad = report()
    if DRAFT is not None:
        os.makedirs(DRAFT, exist_ok=True)
        states = collections.OrderedDict()
        states["NOW"] = None
        summary = {}
        for k, D in STYLES.items():
            sets, prim, owner = draw(D)
            for key, S in SETS.items():
                dd = os.path.join(DRAFT, k, S.dir.split("/")[-1])
                os.makedirs(os.path.join(dd, "palettes"), exist_ok=True)
                G.save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[key][0], os.path.join(dd, "tiles.png"))
                for r in S.rows:
                    write_pal(os.path.join(dd, "palettes", "%02d.pal" % r), sets[key][1][r])
            pt = list(G.PTILES_NOW)
            for t, px in prim.items():
                pt[t] = px
            os.makedirs(os.path.join(DRAFT, k, "building"), exist_ok=True)
            G.save_like(os.path.join(GBA, G.PRI, "tiles.png"), pt, os.path.join(DRAFT, k, "building", "tiles.png"))
            states[k] = (sets, prim)
            ch = {sk: sum(1 for (s2, t) in owner if s2 == sk and sets[sk][0][t] != SETS[sk].van[t]) for sk in SETS}
            ch["diary"] = sum(1 for t in prim if prim[t] != G.ptile(t))
            summary[k] = dict(title=D["title"], tiles_redrawn=ch, new_tiles=0,
                              rows={"pokemon_mansion": MAN.rows, "pokemon_tower": TOW.rows})
            print("  %s %-32s redrawn: pokemon_mansion %d, pokemon_tower %d (+ the floor around 6 stones), diary "
                  "%d; 0 new tiles" % (k, D["title"], ch["man"], ch["tow"], ch["diary"]))
        json.dump(dict(ticket="T-447", pair=4, status="DRAFT -- not in the engine", approved=APPROVED,
                       directions=summary), open(os.path.join(DRAFT, "directions.json"), "w"), indent=1)
        for p in contact_sheets(DRAFT, states):
            print("  sheet:", p)
    if APPROVED:
        bad = check_engine() or bad
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

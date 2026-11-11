#!/usr/bin/env python3
"""The landmarks' rooms, drawn from the story, a pair at a time (T-447, pair 4: the MANSION and DAEMON TOWER; pair 5:
KEEPALIVE PLANT and TANOBY; pair 6: the LEAGUE and the HALL OF FAME; pair 7: the S.S. ANNE and its departure).

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
    python3 tools/gbalandmarkrooms.py --pair 5 --draft [DIR]
                                                      # pair 5's directions (KEEPALIVE PLANT + TANOBY, below), the
                                                      #   same outputs in gfx/drafts/t447_pair5/
    python3 tools/gbalandmarkrooms.py --pair 5 --write --approved
                                                      # into the engine (the user, 2026-11-11: PLANT B, TANOBY A,
                                                      #   B extended over the tiles its draft left bare); the report
                                                      #   then exits 1 on any difference from that write
    python3 tools/gbalandmarkrooms.py --pair 6 --draft [DIR]
                                                      # pair 6's directions (the LEAGUE + the HALL OF FAME, below),
                                                      #   the same outputs in gfx/drafts/t447_pair6/
    python3 tools/gbalandmarkrooms.py --pair 6 --write --approved
                                                      # into the engine (the user, 2026-11-11: LEAGUE A, HALL A);
                                                      #   the report then exits 1 on any difference from that write
    python3 tools/gbalandmarkrooms.py --pair 7 --draft [DIR]
                                                      # pair 7's directions (the S.S. ANNE and its departure's smoke
                                                      #   and wake, below), the same outputs in gfx/drafts/t447_pair7/
    python3 tools/gbalandmarkrooms.py --pair 7 --write --approved
                                                      # into the engine (the user, 2026-11-11: C THE LIVERY,
                                                      #   extended over the tiles its draft only recoloured; the
                                                      #   smoke moved over the funnel in src/ss_anne.c by hand);
                                                      #   the report then exits 1 on any difference from that write

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
#  the user, 2026-11-11: PLANT B Growing untended, TANOBY A Carved, not lit
#  the user, 2026-11-11: LEAGUE A The four vessels, HALL A The index card
APPROVED = {"man": "A", "tow": "A", "pp": "B", "tan": "A", "lg": "A", "hof": "A",
            "ss": "C"}   # the user, 2026-11-11: C The livery; smoke moved over the funnel

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


# ============================================================================================ PAIR 5
#  KEEPALIVE PLANT + TANOBY -- the two places that outlived their users (the user, 2026-11-10: "The landmarks left";
#  pair 4's notes give the order). A plant still running with nobody connected to it (vision "Named 2026-09-04 --
#  KEEPALIVE PLANT", 4.25: SENTINEL, whose MEAN LOOK stops you DETACHing), and an alphabet nobody reads (4.24, T-21:
#  seven chambers, seven accounts of one event, the event never named; reading the seventh sets THE FIRST).
#
#  power_plant    KEEPALIVE PLANT, one map. Its rows 7 and 8 are gbacaves.py's (T-438 batch E2 "STILL RUNNING",
#                 approved 2026-10-23): every index that look names keeps its colour exactly (CAVES_PLANT), so a
#                 direction here is drawing, not colour -- only row 8's six free slots (4, 7, 8, 9, 14, 15: no placed
#                 tile draws them) and row 7's 15 (vanilla's white) may take a colour. Row 11 is the dark outside the
#                 walls (tile 1, one black): never drawn. gbacaves.T447_PLANT names the tiles this pair draws and its
#                 write keeps them as the engine has them (the T538_TUNNEL precedent), so neither tool undoes the
#                 other. Its machines' consoles are primary/building tiles (gbamachines.py): not this tool's.
#  tanoby_ruins   the seven TANOBY chambers. Its palettes are still vanilla's (gbacaves never drafted it: "with batch
#                 G"); gbatowns.py batch G (2026-10-28, a DRAFT the user away) redrew 11 tiles' pixels (flags, wall
#                 foot, brick) in those colours. gbatowns.LANDMARKS now holds the seven chambers, so its write keeps
#                 every tile they draw exactly as it is. Rows 8..12 are one ladder drawn by the back wall's shared
#                 tiles, each chamber picking its row (Weepth/Viapois 8, Scufib/Rixy 9, Liptoo 10, Monean 11,
#                 Dilford 12) for one colour of its own at index 15 (and 14): those two slots are kept in every row,
#                 and indices 1..13 stay equal across rows 8..12. The chamber name card (map_preview, T-445) is
#                 gbapreviews' and is not touched.
#
#  The same rules as pair 4: redrawn IN PLACE, every tile keeps its footprint, no block, layer, flip, palette row,
#  behaviour or collision bit moves, no map is touched. Neither tileset has an animation (both callbacks NULL) and the
#  engine names none of their blocks (no METATILE_ labels, no setmetatile): only the plant's machine behaviour
#  (MB 0x95, the generators) is read by code, and behaviours are not touched. No index of either set is recoloured at
#  run time (no tileset test in fieldmap.c; the watch's tint is global). 0 new tiles.
#
#  TANOBY'S SCRIPT STAYS UNREADABLE. Every glyph is drawn from GLYPHS, generated in code on a 3x5 grid and kept only
#  if it stands at least GLYPH_MIN cells away from every Latin letter and digit (upper and lower case, any of the
#  eight turns and mirrors) in a 3x5 face -- so no glyph reads as a letter and no row of them reads as a word. The
#  report checks every glyph again. The names stay transliterated (vision 6.x): nothing here translates them.

PAIR = argval("--pair") or "4"
DRAFT5_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t447_pair5")

PP = G.Set("pp", "gTileset_PowerPlant", [7, 8])
TAN = G.Set("tan", "gTileset_TanobyRuins", [7, 8, 9, 10, 11, 12])
SETS5 = {"pp": PP, "tan": TAN}
G.SETS.update(SETS5)
NAMES.update({"pp": "KEEPALIVE PLANT", "tan": "TANOBY"})
TODAY5 = {(k, r): [tuple(c) for c in read_pal(os.path.join(GBA, S.dir, "palettes/%02d.pal" % r))]
          for k, S in SETS5.items() for r in range(16)}

#  gbacaves' approved look on the plant: row -> the indices its MATERIALS["power_plant"] names (kept exactly)
CAVES_PLANT = {7: list(range(1, 15)), 8: [1, 2, 3, 5, 6, 10, 11, 12, 13]}
CHAMBER_ROWS = [8, 9, 10, 11, 12]
CHAMBER_SLOTS = [14, 15]
FIXED5 = {("pp", 7): CAVES_PLANT[7], ("pp", 8): CAVES_PLANT[8]}
FIXED5.update({("tan", r): CHAMBER_SLOTS for r in CHAMBER_ROWS})
VOID5 = {("pp", 1)}                                  # the dark outside the plant's walls (row 11): never drawn
CHAMBERS = ["SevenIsland_TanobyRuins_MoneanChamber", "SevenIsland_TanobyRuins_LiptooChamber",
            "SevenIsland_TanobyRuins_WeepthChamber", "SevenIsland_TanobyRuins_DilfordChamber",
            "SevenIsland_TanobyRuins_ScufibChamber", "SevenIsland_TanobyRuins_RixyChamber",
            "SevenIsland_TanobyRuins_ViapoisChamber"]

#  each own row's fifteen materials (index 1..15). The plant's are gbacaves' roles by name: CR CG CB the three
#  conduits (rust, green, blue), G3..G1 the girders dark..light, TRIM, LANE, PLATE, HB the housings' body, SEAM, HO
#  their outline, HM their shade, LED the status light; row 8's K3..K1 the coils, L5 L6 the drums' lamps, Q* free.
ROWMATS5 = {
    ("pp", 7): ["CR", "CG", "CB", "G3", "G2", "G1", "TRIM", "LANE", "PLATE", "HB", "SEAM", "HO", "HM", "LED", "WHT"],
    ("pp", 8): ["K3", "K2", "K1", "Q4", "L5", "L6", "Q7", "Q8", "Q9", "HB", "SEAM", "HO", "HM", "Q14", "Q15"],
    ("tan", 7): ["OUT", "T1", "T2", "T3", "T4", "T5", "N1", "N2", "F1", "F2", "F3", "F4", "F5", "X1", "X2"],
}
for _r in CHAMBER_ROWS:
    ROWMATS5["tan", _r] = ["OUT", "B1", "B2", "B3", "B4", "B5", "B6", "S1", "S2", "S3", "D1", "D2", "D3", "CH14",
                           "CH15"]

#  vanilla's (row, index) -> what it was FOR (the plant's are gbacaves' names for the same indices)
ROLE5 = {
    "pp": {7: dict(enumerate(ROWMATS5["pp", 7], 1)), 8: dict(enumerate(ROWMATS5["pp", 8], 1)), 11: {15: "VOID"}},
    "tan": {7: {1: "OUT", 2: "grey", 3: "face", 4: "topD", 5: "top", 6: "crack", 7: "studR", 8: "stud", 9: "sand",
                10: "sandD", 11: "sandG", 12: "flagL", 13: "flag", 14: "flagD", 15: "x"}},
}
for _r in CHAMBER_ROWS:
    ROLE5["tan"][_r] = {1: "OUT", 2: "speck", 3: "brD", 4: "mortar", 5: "brL", 6: "brM", 7: "br", 8: "cap",
                        9: "capS", 10: "olD", 11: "flagL", 12: "ol", 13: "dk", 14: "CH14", 15: "CH15"}


def home5(S, t):
    return S.home(t) if t in S.use else S.rows[0]


def vrole5(K, x, y):
    vi = K.vi(x, y)
    if vi is None:
        return None
    spec = K.layout[y // 8][x // 8]
    return ROLE5[K.setkey].get(home5(SETS5[K.setkey], spec[0]), {}).get(vi, "x")


def ktile(K, x, y):
    spec = K.layout[y // 8][x // 8]
    return spec[0] if spec else None


# ---------------------------------------------------------------------------------------- the script (TANOBY)
#  a 3x5 face of the Latin letters and digits, upper and lower case and a bar: what no glyph may resemble
LATIN = {
    "A": "010101111101101", "B": "110101110101110", "C": "011100100100011", "D": "110101101101110",
    "E": "111100110100111", "F": "111100110100100", "G": "011100101101011", "H": "101101111101101",
    "I": "111010010010111", "J": "001001001101010", "K": "101101110101101", "L": "100100100100111",
    "M": "101111111101101", "N": "110101101101101", "O": "010101101101010", "P": "110101110100100",
    "Q": "010101101110011", "R": "110101110101101", "S": "011100010001110", "T": "111010010010010",
    "U": "101101101101111", "V": "101101101101010", "W": "101101111111101", "X": "101101010101101",
    "Y": "101101010010010", "Z": "111001010100111", "0": "111101101101111", "1": "010110010010111",
    "2": "110001010100111", "3": "110001010001110", "4": "101101111001001", "5": "111100110001110",
    "6": "011100110101010", "7": "111001010010010", "8": "010101010101010", "9": "010101011001110",
    "a": "000011101101011", "b": "100110101101110", "c": "000011100100011", "d": "001011101101011",
    "e": "000010111100011", "f": "011100110100100", "g": "011101011001110", "h": "100110101101101",
    "i": "010000010010010", "j": "001000001001110", "k": "100101110101101", "l": "100100100100011",
    "m": "000111111101101", "n": "000110101101101", "o": "000010101101010", "p": "000110101110100",
    "q": "000011101011001", "r": "000011100100100", "s": "000011110011110", "t": "010111010010011",
    "u": "000101101101011", "v": "000101101101010", "w": "000101101111111", "x": "000101010101101",
    "y": "101101011001110", "z": "000111001100111", "|": "010010010010010", "-": "000000111000000",
    #  and the marks a reader would take for punctuation
    "!": "010010010000010", "?": "110001010000010", "/": "001001010100100", "\\": "100100010001001",
    ";": "000010000010100", ":": "000010000010000", "+": "000010111010000", "=": "000111000111000",
    "(": "001010010010001", ")": "100010010010100", "<": "001010100010001", ">": "100010001010100",
    "%": "101001010100101", "*": "101010101000000", "^": "010101000000000", "~": "000110011000000",
    "#": "101111101111101", "&": "010101010101011", ".": "000000000000010", ",": "000000000010100",
}
GLYPH_MIN = 4          # cells (of 15) every glyph keeps from every letter, in every turn and mirror


def _turns(bits):
    g = [[int(bits[y * 3 + x]) for x in range(3)] for y in range(5)]
    out = []
    for a in (g, [r[::-1] for r in g]):
        for b in (a, a[::-1]):
            out.append(b)
    #  a quarter turn of a 3x5 face is 5x3: compared on the 5x5 square it sits in (centred)
    sq = []
    for b in list(out):
        t = [[b[y][x] for y in range(5)] for x in range(3)]       # 3 rows of 5
        sq.append(t)
    return out, sq


def glyph_distance(g):
    """the fewest cells between glyph G (5 rows of 3) and any letter, in any of the eight turns and mirrors"""
    best = 99
    gs = [[g[y][x] for x in range(3)] for y in range(5)]
    for name, bits in LATIN.items():
        same, quarter = _turns(bits)
        for L in same:
            best = min(best, sum(gs[y][x] != L[y][x] for y in range(5) for x in range(3)))
        #  the glyph turned a quarter (3 rows of 5) against the letter turned a quarter, on a 5x5 square
        gq = [[gs[y][x] for y in range(5)] for x in range(3)]
        for L in quarter:
            best = min(best, sum(gq[y][x] != L[y][x] for y in range(3) for x in range(5)))
    return best


def make_glyphs(n=16, seed=4471):
    """the script: n glyphs on a 3x5 grid, each one pen stroke from the top that turns at least twice -- a step
    across and a step aslant -- ending in a hook, and a dot set apart from it; kept only far from every letter, digit
    and mark, and no two alike"""
    out, s = [], seed
    while len(out) < n and s < seed + 200000:
        s += 1
        g = [[0] * 3 for _ in range(5)]
        x, y = H(s, 1) % 3, 0
        g[y][x] = 1
        diag = across = False
        for k in range(3 + H(s, 3) % 3):
            dx, dy = (-1, 0, 1)[H(s, 10 + k) % 3], (0, 1, 1)[H(s, 20 + k) % 3]
            if not dx and not dy:
                continue
            nx, ny = max(0, min(2, x + dx)), max(0, min(4, y + dy))
            if (nx, ny) == (x, y):
                continue
            diag |= bool(nx != x and ny != y)
            across |= bool(nx != x and ny == y)
            x, y = nx, ny
            g[y][x] = 1
        dx, dy = H(s, 40) % 3, 2 + H(s, 41) % 3
        if g[dy][dx] == 0 and all(g[yy][xx] == 0 for yy in range(max(0, dy - 1), min(5, dy + 2))
                                  for xx in range(max(0, dx - 1), min(3, dx + 2)) if (yy, xx) != (dy, dx)):
            g[dy][dx] = 1
        else:
            continue
        cells = sum(map(sum, g))
        if not (diag and across) or cells < 5 or cells > 8:
            continue
        if glyph_distance(g) < GLYPH_MIN:
            continue
        if any(sum(g[yy][xx] != o[yy][xx] for yy in range(5) for xx in range(3)) < 3 for o in out):
            continue
        out.append(g)
    return out


GLYPHS = make_glyphs()


def glyph_at(gi, x, y, x0, y0):
    """is (x, y) a cell of glyph gi drawn with its top-left at (x0, y0)?"""
    gx, gy = x - x0, y - y0
    if 0 <= gx < 3 and 0 <= gy < 5:
        return GLYPHS[gi % len(GLYPHS)][gy][gx] == 1
    return False


# ---------------------------------------------------------------------------------------- the groups
#  the objects first (their own coordinates), then every placed block by how often it is placed, each layer a 16x16
#  canvas, so a tile is drawn in the block that shows it most and a motif runs on across its blocks
OBJ_PP = [
    ("housing", M([33, 33], [8, 8], [21, 21], [38, 38]), "the housings: cap, upper body, conduits, kick plate"),
    ("panel",   M([3, 4], [19, 20]),                     "a housing's hatch"),
    ("coil",    M([61, 62], [77, 78]),                   "the coils on the floor (0x2B5, 0x2B6)"),
    ("drums",   M([48, 49], [64, 65], [50, 51], [64, 65], [66, 67]), "the drums, stacked (row 8)"),
    ("gen",     M([52, 53, 54, h(54), h(53), h(52)], [68, 69, 70, h(70), h(69), h(68)],
                  [55, 56, 57, h(57), h(56), h(55)], [71, 72, 73, h(73), h(72), h(71)],
                  [58, 59, 60, h(60), h(59), h(58)], [74, 75, 76, h(76), h(75), h(74)]),
     "the two generators (MB 0x95) and their crowns over the housing"),
    ("floor",   M([10, 11], [26, 27]),                   "the floor plates (0x29F)"),
]
OBJ_TAN = [
    ("frieze",  M([5, 6], [21, 22], [7, 8], [23, 24]),   "the back wall: its cap, the chamber's band, the courses"),
    ("door",    M([9, h(9)], [25, h(25)], [10, h(10)], [26, h(26)], [12, 13]), "the back wall's doors"),
    ("face",    M([39, 39], [43, 43]),                   "the maze walls' face (0x2B9)"),
    ("face2",   M([62, 39], [60, 61]),                   "the face, its second run (0x2D6)"),
    ("floor",   M([1, 2], [17, 18]),                     "the flags (0x288)"),
]
KIND_PP = {}
for _k, _ts in (("floor", [10, 11, 26, 27, 12, 13, 28, 29, 37]), ("grate", [14, 15, 30, 31, 47, 63, 79]),
                ("lane", [2, 16, 17, 18, 32]), ("base", [46]),
                ("house", [33, 34, 8, 21, 38, 5, 6, 7, 22, 23, 24, 39, 40, 9, 25, 41, 35, 36, 3, 4, 19, 20])):
    for _t in _ts:
        KIND_PP[_t] = _k
KIND_TAN = {}
for _k, _ts in (("face", [39, 43, 44, 47, 60, 61, 62, 63]),
                ("top", [28, 29, 32, 34, 35, 36, 38, 41, 42, 45, 46, 56, 57, 58, 59, 64, 65, 66, 67, 68, 69]),
                ("floor", [1, 2, 3, 4, 17, 18, 19, 20, 70, 71, 72])):
    for _t in _ts:
        KIND_TAN[_t] = _k
KIND5 = {"pp": KIND_PP, "tan": KIND_TAN}


def placed_blocks(S):
    """(block, count, its eight entries) for every block a map places, most placed first"""
    cnt = collections.Counter()
    for l in G.LAYOUTS:
        if l.get("secondary_tileset") != S.sym or not G.MBL.get(l["id"]):
            continue
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        for k in range(0, len(bd) - 1, 2):
            cnt[struct.unpack_from("<H", bd, k)[0] & 0x3FF] += 1
    out = []
    for b, n in cnt.most_common():
        if b < 640 or (b - 640 + 1) * 16 > len(S.mt):
            continue
        out.append((b, n, struct.unpack_from("<8H", S.mt, (b - 640) * 16)))
    return out


def block_layout(ee):
    rows = []
    for q0 in (0, 2):
        r = []
        for e in ee[q0:q0 + 2]:
            t = e & 0x3FF
            if t < 640:
                r.append(None)
            else:
                fl = ("h" if (e >> 10) & 1 else "") + ("v" if (e >> 11) & 1 else "")
                r.append((t - 640, fl))
        rows.append(r)
    return rows


def groups5():
    """(key, setkey, layout, kind, what): the objects, then each placed block's two layers"""
    out = []
    for setkey, objs in (("pp", OBJ_PP), ("tan", OBJ_TAN)):
        for key, lay, what in objs:
            out.append((key, setkey, lay, "obj", what))
        for b, n, ee in placed_blocks(SETS5[setkey]):
            for layer in (0, 1):
                lay = block_layout(ee[layer * 4:layer * 4 + 4])
                if any(s is not None for r in lay for s in r):
                    out.append(("b%03X.%d" % (b, layer), setkey, lay, "block", "block 0x%03X layer %d (%d placed)"
                                % (b, layer, n)))
    return out


GROUPS5 = groups5()


def paint5(K, D, key, kind):
    """one group: an object goes to the direction's painter of that name; a block goes through its zones, its
    kinds read per tile, a housing block placed low (it draws the kick plate, 38) a housing's lower half"""
    if kind == "obj":
        D[key](K)
        return
    tiles = {s[0] for r in K.layout for s in r if s}
    K.hy = 16 if K.setkey == "pp" and 38 in tiles else 0
    f = D["zone"]
    kinds = KIND5[K.setkey]
    K.fn(lambda x, y: f(kinds.get(ktile(K, x, y), "wall"), vrole5(K, x, y), x, y, K))


# ---------------------------------------------------------------------------------------- resolving
def mats5(D, setkey):
    m = dict(D["mat"])
    for (k, r), slots in FIXED5.items():
        if k == setkey:
            for i in slots:
                m.setdefault(ROWMATS5[k, r][i - 1], tuple(TODAY5[k, r][i]))
    return m


def set_palettes5(D, S):
    mat = mats5(D, S.key)
    out = {}
    for r in range(16):
        if r in S.rows:
            row = [tuple(TODAY5[S.key, r][0])]
            for i, n in enumerate(ROWMATS5[S.key, r], 1):
                row.append(tuple(TODAY5[S.key, r][i]) if i in FIXED5.get((S.key, r), ()) else tuple(mat[n]))
            out[r] = row
        else:
            out[r] = list(TODAY5[S.key, r])
    return out


def resolve5(mats, base, rows, mat, pals, setkey):
    """64 materials -> 64 indices for a tile placed in ROWS (weights). A material its rows hold at one index takes it
    exactly; CH14/CH15 are the chamber's own slots; anything else the nearest colour, never a chamber slot. None
    keeps vanilla's index there. The footprint is exact: 0 stays 0, a drawn pixel stays drawn."""
    px, cache = [], {}
    for k, m in enumerate(mats):
        if base[k] == 0:
            px.append(0)
            continue
        if m is None:
            px.append(base[k])
            continue
        if m in ("CH14", "CH15"):
            px.append(int(m[2:]))
            continue
        if m not in cache:
            idx = {ROWMATS5[setkey, r].index(m) + 1 for r in rows if (setkey, r) in ROWMATS5
                   and m in ROWMATS5[setkey, r]}
            if len(idx) == 1 and all((setkey, r) in ROWMATS5 and m in ROWMATS5[setkey, r] for r in rows):
                cache[m] = idx.pop()
            else:
                c = mat[m]
                best, bd = 1, 1e18
                for i in range(1, 16):
                    if setkey == "tan" and i in CHAMBER_SLOTS and any(r in CHAMBER_ROWS for r in rows):
                        continue
                    d = 0
                    for r, w in rows.items():
                        col = pals[r][i] if r in pals else (0, 0, 0)
                        d += w * sum((a - b) ** 2 for a, b in zip(col, c))
                    if d < bd:
                        best, bd = i, d
                cache[m] = best
        px.append(cache[m])
    return px


def draw5(D, only=None):
    """-> {setkey: (tiles, palettes)}, owner {(setkey, t): group}. ONLY limits it to one building"""
    out = {k: ([t[:] for t in S.cur], set_palettes5(D[k], S)) for k, S in SETS5.items()}
    owner = {}
    for key, setkey, layout, kind, what in GROUPS5:
        if only and setkey != only:
            continue
        DD = D[setkey]
        K = Cv(layout, setkey)
        K.hy = 0
        paint5(K, DD, key, kind)
        S = SETS5[setkey]
        mat = mats5(DD, setkey)
        pals = out[setkey][1]
        for t, mats in K.tiles().items():
            if (setkey, t) in owner or (setkey, t) in VOID5 or t >= S.nvan or t not in S.use:
                continue
            rows = dict(S.use[t]["rows"])
            out[setkey][0][t] = resolve5(mats, S.van[t], rows, mat, pals, setkey)
            owner[setkey, t] = key
    return out, owner


def owned5(setkey):
    """the tiles this pair draws in a set: every placed tile but the void"""
    S = SETS5[setkey]
    return sorted(t for t in S.use if t < S.nvan and any(S.van[t]) and (setkey, t) not in VOID5)


# ---------------------------------------------------------------------------------------- the PLANT's directions
def pp_keep(role):
    """a role drawn as gbacaves drew it"""
    return role if role not in (None, "x", "VOID") else None


def ring_at(x, y, cx, cy, r, w=1.0):
    return abs(math.hypot(x - cx, y - cy) - r) < w * 0.5 + 0.01


# ------------------------------------------------------------------ PLANT A: THE HEARTBEAT (keepalive)
def A_pp_zone(kind, role, x, y, K):
    if role in (None, "VOID"):
        return None
    if kind == "floor" or kind == "grate":
        return A_pp_floorpx(role, x % 16, y % 16, kind)
    if kind == "lane":                                 # the walkways: a clean raised edge, a pin every plate
        if role in ("SEAM",) and x % 8 == 3 and y % 8 == 3:
            return "PLATE"
        return pp_keep(role)
    if kind == "house":
        return A_pp_housepx(role, x % 8, y + K.hy, K)
    return pp_keep(role)


def A_pp_floorpx(role, x, y, kind):
    """raised-floor plates, a pin at each plate's corner; the seams kept"""
    if kind == "grate":
        return pp_keep(role)
    if role == "PLATE" and (x, y) in ((1, 1), (9, 9)):
        return "SEAM"
    return pp_keep(role)


def A_pp_housepx(role, x, hy, K):
    """a cabinet face: a dark screen band across the body carrying the trace, one status light per cabinet"""
    if role in ("HO",) or hy < 8:
        return pp_keep(role)
    if 13 <= hy <= 19:                                 # the screen band, where the three conduits ran
        trace = {0: 17, 1: 17, 2: 17, 3: 17, 4: 16, 5: 14, 6: 19, 7: 17}[x]
        if hy == trace or (x == 5 and 14 <= hy <= 17) or (x == 6 and 17 <= hy <= 19):
            return "LED"
        if hy in (13, 19) and not (x == 6 and hy == 19):
            return "HM"
        return "HO"
    if hy in (10, 11) and x in (2, 3):                 # the status light (on: green)
        return "LED" if hy == 10 else "HO"
    if role in ("CR", "CG", "CB"):
        return "HB"
    if 24 <= hy and role in ("G1", "G2") and x % 4 == 1 and 26 <= hy <= 29:
        return "G3"                                    # the plinth's vent slots
    return pp_keep(role)


def A_pp_housing(K):
    K.fn(lambda x, y: A_pp_housepx(vrole5(K, x, y), x % 8, y, K))


def A_pp_panel(K):
    """a hatch: a small screen with the trace on it"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r in ("PLATE", "TRIM") and 4 <= x <= 13 and 6 <= y <= 12:
            if y == {4: 10, 5: 10, 6: 10, 7: 9, 8: 7, 9: 11, 10: 10, 11: 10, 12: 10, 13: 10}[x]:
                return "LED"
            return "HO"
        return pp_keep(r)
    K.fn(f)


def A_pp_coil(K):
    """a mast's emitter brought inside: rings sent out to nobody"""
    def f(x, y):
        r = vrole5(K, x, y)
        if K.edge(x, y):
            return "HO"
        d = math.hypot(x - 7.5, y - 8.0)
        if d < 1.6:
            return "LED"
        if abs(d - 3.6) < 0.6:
            return "G1"
        if abs(d - 6.0) < 0.6:
            return "G2"
        return "HM" if d < 7 else "HO"
    K.fn(f)


def A_pp_drums(K):
    """the drums as cells of a battery, every one charged: a window down each with its charge in bars"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r in ("L5", "L6") and y % 3 == 0:
            return "HM"                                # the glow cut into charge bars
        return pp_keep(r)
    K.fn(f)


def A_pp_gen(K):
    """the generator: one great ring and its single light, still on"""
    cx, cy = (K.w - 1) / 2.0, 22.0
    def f(x, y):
        r = vrole5(K, x, y)
        if r in (None, "HO", "VOID"):
            return pp_keep(r)
        d = math.hypot(x - cx, y - cy)
        if d < 2.2:
            return "LED"
        if abs(d - 6) < 0.7:
            return "G1"
        if abs(d - 10) < 0.7 and y < 30:
            return "G2"
        return pp_keep(r)
    K.fn(f)


def A_pp_floor(K):
    K.fn(lambda x, y: A_pp_floorpx(vrole5(K, x, y), x, y, "floor"))


# ------------------------------------------------------------------ PLANT B: GROWING UNTENDED (the second meaning)
def leafy(x, y, s, density):
    """a leaf cluster mask: small lobes, never speckle (period 16)"""
    cx, cy = (x // 4) * 4 + H(x // 4, y // 4, s) % 3, (y // 4) * 4 + H(y // 4, x // 4, s + 1) % 3
    if H(x // 4, y // 4, s + 2) % 10 >= density:
        return 0
    d = abs(x - cx) + abs(y - cy)
    return 2 if d == 0 else 1 if d <= 1 else 0


def B_pp_zone(kind, role, x, y, K):
    return B_grown(K, x, y, B_pp_zone0(kind, role, x, y, K))


def B_pp_zone0(kind, role, x, y, K):
    if role in (None, "VOID"):
        return None
    if kind in ("floor", "grate"):
        return B_pp_floorpx(role, x % 16, y % 16)
    if kind == "lane":                                 # moss creeping along the walkways' edge
        if role == "SEAM" and y % 8 == 5 and H(x // 3, y // 8, 7) % 4 == 0:
            return "CG"
        return pp_keep(role)
    if kind == "house":
        return B_pp_housepx(role, x, y + K.hy, K)
    return pp_keep(role)


def B_pp_floorpx(role, x, y):
    """moss in the plates' lower seams, a sprout where two seams meet"""
    if role == "SEAM" and y >= 14 and x % 3:
        return "CG"
    if role == "PLATE" and (x, y) in ((14, 13), (13, 14), (14, 14)):
        return "CG"
    return pp_keep(role)


def ivy(xx, hy):
    """two vines up an 8-pixel face from the floor (hy 31) -- one to the cap, one half way -- each wandering a pixel
    either side, a leaf every third row on alternate sides"""
    for sx, top in ((1, 9), (5, 19)):
        if hy < top:
            continue
        wx = sx + (1 if (hy // 3) % 2 else 0)
        if xx == wx:
            return "CG"
        side = 1 if ((hy + sx) // 3) % 2 else -1
        if (hy + sx) % 3 == 0 and xx in (wx + side, wx + 2 * side):
            return "LED" if xx == wx + 2 * side and hy % 2 else "CG"
        if (hy + sx) % 3 == 1 and xx == wx + side:
            return "CG"
    return None


def B_pp_housepx(role, x, hy, K):
    """ivy up every housing from the floor, thick at the foot and thinning to the cap; the light still green in it"""
    if role in (None, "HO"):
        return pp_keep(role)
    xx = x % 8
    if hy in (10, 11) and xx in (2, 3):
        return "LED" if hy == 10 else "HO"
    m = ivy(xx, hy)
    if m:
        return m
    if role in ("CR", "CB") and hy >= 13:
        return "HB"                                    # the conduits under the leaves
    return pp_keep(role)


def B_pp_housing(K):
    B_fn(K, lambda x, y: B_pp_housepx(vrole5(K, x, y), x % 8, y, K))


def B_pp_panel(K):
    def f(x, y):
        r = vrole5(K, x, y)
        if r not in (None, "HO"):
            m = ivy(x % 8, y + 8)
            if m:
                return m
        return pp_keep(r)
    B_fn(K, f)


def B_pp_coil(K):
    """a coil wound round with a vine"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        if K.edge(x, y):
            return "HO"
        if (x + y * 2) % 7 in (0, 1) and r not in ("HO",):
            return "CG"
        return pp_keep(r)
    B_fn(K, f)


def B_pp_drums(K):
    """the drums as planters: the lamps' green gone to leaves, a shoot over each rim"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        cy = y % 16
        if r in ("L5", "L6", "K1"):
            return "Q8" if (x + cy) % 4 else "Q9"
        if r in ("HB",) and cy in (0, 1, 2, 3) and H(x, y, 3) % 3 == 0:
            return "Q7"
        return pp_keep(r)
    B_fn(K, f)


def B_pp_gen(K):
    def f(x, y):
        r = vrole5(K, x, y)
        if r in (None, "HO") or y < 8:
            return pp_keep(r)
        m = ivy(x % 8, min(31, y))
        if m and (x // 8) in (0, 5):
            return m
        return pp_keep(r)
    B_fn(K, f)


def B_pp_floor(K):
    B_fn(K, lambda x, y: B_pp_floorpx(vrole5(K, x, y), x, y))


#  THE EXTENSION (the user, 2026-11-11, picking B: "extend it to the girders, grates, ends and generator parts that
#  keep Nintendo's shapes"). The draft left 35 of the plant's 74 tiles as Nintendo drew them; every one of those but
#  the bare floor plate (10, a flat fill under 747 placements) is grown over here in B's own language, in the same
#  slots -- CG and LED in row 7 (gbacaves' green conduit and status light, kept), Q7..Q9 in row 8 (B's three greens)
#  -- and ONLY those tiles, so every tile the user saw drawn stays byte-identical to the draft.
B_BARE = {2, 11, 12, 13, 14, 15, 16, 23, 24, 28, 29, 33, 34, 35, 37, 46, 47, 48, 49, 52, 53, 54, 56, 57, 59, 60, 63,
          69, 70, 72, 73, 75, 76, 79}
B_CAP = {33, 34}                                     # the housings' ribbed cap
B_WALK = {12, 13, 28, 29}                            # the walkway's raised edges
B_ENDS = {2, 16}                                     # the walkways' ends
B_SEAMS = {11, 37}                                   # a plate's seam, a kick plate's slot
B_GRATE = {14: "SEAM", 15: "SEAM", 47: "HM", 63: "HM", 79: "HM"}
B_LID = {48, 49}                                     # the drums' lids (row 8)
B_GEN = {52, 53, 54, 56, 57, 59, 60, 69, 70, 72, 73, 75, 76}


def B_grow(t, r, x, y):
    """what grows on a tile the draft left bare: None keeps the draft's (Nintendo's) pixel"""
    if r in (None, "x", "VOID", "HO"):
        return None
    ly = y % 8
    if t in B_CAP:                                   # moss on the cap's lip, draping a pixel or three down the ribs
        if ly == 0:
            return "LED" if H(x, 1, 448) % 6 == 0 else "CG"
        if ly <= H(x // 2, 3, 447) % 4 and r in ("LANE", "TRIM", "PLATE", "HM"):
            return "CG"
        return None
    if r in ("G1", "G2", "G3"):                      # a creeper wound round the girders, a leaf every third turn
        k = (2 * x + y) % 7
        if k == 0:
            return "CG"
        if k == 1 and y % 3 == 0:
            return "LED"
        return None
    if t == 24 and r == "CB":                        # the brace's conduit band under leaves
        return "CG" if H(x // 2, y, 449) % 2 == 0 else None
    if t in B_ENDS:                                  # tufts at the walkways' ends
        if r == "PLATE":
            return "CG"
        if ly >= 7 - H(x // 2, y // 8, 451) % 3 and H(x // 2, y // 8, 450) % 3 == 0:
            return "CG"
        return None
    if t in B_WALK:                                  # moss along the walkway's raised edge
        return "CG" if r == "HB" and H(x // 2, y // 2, 452) % 2 == 0 else None
    if t in B_SEAMS:                                 # moss in the lower half of the seam
        return "CG" if r == "SEAM" and ly >= 4 else None
    if t in B_GRATE:                                 # grass up through the grate's slots
        if r == B_GRATE[t] and H(x // 2, y, 453) % 4 == 0:
            return "LED" if H(x, y, 454) % 5 == 0 else "CG"
        return None
    if t in B_LID:                                   # the planters' lids: leaves over the rim
        if r == "SEAM":
            return "Q8" if (x + y) % 3 else "Q9"
        if r == "HB":
            return "Q7"
        return None
    if t == 46:                                      # a runner across the coil's base plate
        k = (x + 2 * y) % 9
        if r == "K3" and k == 0:
            return "Q7"
        if r == "K3" and k == 1 and y % 2:
            return "Q8"
        return None
    if t in B_GEN:                                   # ivy up the generator's dome, moss in its vents and at its foot
        if r in ("PLATE", "LANE"):
            if y < 9:                                # moss on the crown, where nothing climbs
                return "CG" if H(x // 2, y // 3, 457) % 4 == 0 else None
            return ivy(x % 8, min(31, y))
        if r == "HM" and y < 8:                      # the crown's rim
            return "CG" if H(x // 2, 0, 458) % 3 == 0 else None
        if r == "SEAM":
            return "CG" if H(x // 2, y, 455) % 3 == 0 else None
        if r == "HB" and y >= 24 and H(x, y, 456) % 4 == 0:
            return "CG"
        return None
    return None


def B_grown(K, x, y, m):
    t = ktile(K, x, y)
    if t in B_BARE:
        g = B_grow(t, vrole5(K, x, y), x, y)
        if g:
            return g
    return m


def B_fn(K, f):
    K.fn(lambda x, y: B_grown(K, x, y, f(x, y)))


# ------------------------------------------------------------------ PLANT C: OPEN SESSIONS (nobody connected)
def C_pp_zone(kind, role, x, y, K):
    if role in (None, "VOID"):
        return None
    if kind in ("floor", "grate"):
        return C_pp_floorpx(role, x % 16, y % 16, kind)
    if kind == "lane":                                 # the walkways are cable trays: two runs along them
        if role == "SEAM":
            return {2: "CR", 4: "CB"}.get(y % 8, "SEAM")
        return pp_keep(role)
    if kind == "house":
        return C_pp_housepx(role, x, y + K.hy, K)
    return pp_keep(role)


def C_pp_floorpx(role, x, y, kind):
    """the plates as they were: the leads are the housings'"""
    return pp_keep(role)


def C_pp_housepx(role, x, hy, K):
    """a patch panel: two rows of ports, each with its light (green: listening), a few cables plugged in and hanging
    down to nothing, the conduits drooping between the panels"""
    if role in (None, "HO") or hy < 8:
        return pp_keep(role)
    xx = x % 8
    for py in (9, 19):                                 # the two rows of ports
        if py <= hy <= py + 2:
            if xx in (1, 2, 5, 6):
                return "LED" if hy == py and xx in (1, 5) else "HO"
            return "HM"
    if hy in (12, 13) and xx in (1, 2):                # a lead plugged into the first port, hanging down
        return "CR"
    if 22 <= hy <= 27 and xx in (5, 6):
        return "CB" if hy < 27 else "HO"
    if role in ("CR", "CG", "CB"):
        return "HB"
    return pp_keep(role)


def C_pp_housing(K):
    K.fn(lambda x, y: C_pp_housepx(vrole5(K, x, y), x % 8, y, K))


def C_pp_panel(K):
    """a hatch: a jack field, all ports open"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r in ("PLATE", "TRIM") and 4 <= x <= 13 and 6 <= y <= 13:
            return "HO" if (x % 3 == 1 and y % 3 == 1) else "HM"
        return pp_keep(r)
    K.fn(f)


def C_pp_coil(K):
    """a cable reel, wound and never unwound"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        if K.edge(x, y):
            return "HO"
        d = math.hypot(x - 7.5, y - 8.0)
        if d < 1.8:
            return "HO"
        if d < 6:
            return "CR" if int(d * 1.5) % 2 else "HM"
        return "G2"
    K.fn(f)


def C_pp_drums(K):
    """the drums as transformers, their leads unplugged and coiled on top"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        cy = y % 16
        if r in ("L5", "L6"):
            return "HM" if cy % 2 else "HB"
        if r in ("K1", "K2") and cy in (1, 2) and x % 3 == 0:
            return "Q4"
        return pp_keep(r)
    K.fn(f)


def C_pp_gen(K):
    """the generator as a switchboard: rows of lit jacks round the crown"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r in (None, "HO"):
            return pp_keep(r)
        if 10 <= y <= 30 and x % 4 == 1 and y % 4 == 2 and r not in ("PLATE",):
            return "LED"
        return pp_keep(r)
    K.fn(f)


def C_pp_floor(K):
    K.fn(lambda x, y: C_pp_floorpx(vrole5(K, x, y), x, y, "floor"))


# ---------------------------------------------------------------------------------------- TANOBY's directions
def tan_base(role, P):
    """a role's material through the direction's role table P"""
    if role in (None, "x"):
        return None
    if role in ("CH14", "CH15"):
        return role
    return P.get(role)


def incised(x, y, gi, x0, y0, groove, lit):
    """a carved glyph: the groove, and its lower lip catching the light"""
    if glyph_at(gi, x, y, x0, y0):
        return groove
    if glyph_at(gi, x, y - 1, x0, y0):
        return lit
    return None


def tan_frieze_glyphs(x, y, y0, seed, groove, lit):
    """a line of the script, four glyphs a 16-pixel course (3 wide, a pixel between)"""
    for k in range(4):
        m = incised(x, y, seed + k, 4 * k, y0, groove, lit)
        if m:
            return m
    return None


# ------------------------------------------------------------------ TANOBY A: CARVED, NOT LIT
PA = {"OUT": "OUT", "grey": "T4", "face": "T3", "topD": "T2", "top": "T1", "crack": "T4", "studR": "T3",
      "stud": "T3", "sand": "F2", "sandD": "F3", "sandG": "F3", "flagL": "F1", "flag": "F2", "flagD": "F3",
      "speck": "B3", "brD": "B4", "mortar": "B5", "brL": "B1", "brM": "B3", "br": "B2", "cap": "S1", "capS": "S2",
      "olD": "D1", "ol": "D2", "dk": "D3"}


def A_tan_zone(kind, role, x, y, K):
    m = tan_base(role, PA)
    if kind == "face" and role in ("face", "studR", "stud", "crack"):
        return A_tan_facepx(x, y % 16, ktile(K, x, y))
    if kind == "floor" and role in ("flagL", "flag", "flagD"):
        return A_tan_flag(x % 16, y % 16)
    return m


FACE_GLYPHS = {39: 0, 62: 2, 60: 4, 61: 6, 43: 8, 47: 10, 63: 12, 44: 14}


def face_glyph(x, y, t, y0, base=0):
    """two glyphs a face tile (3 wide, a pixel apart): which glyph is at (x, y), or None"""
    gi = FACE_GLYPHS.get(t, 0) + base
    xx = x % 8
    for k, x0 in enumerate((0, 4)):
        if glyph_at(gi + k, xx, y, x0, y0):
            return gi + k
    return None


def A_tan_facepx(x, y, t):
    """the maze walls: dressed stone, and along the upper course one line of the script cut into it"""
    if y < 8:
        if face_glyph(x, y, t, 1) is not None:
            return "T5"
        if face_glyph(x, y - 1, t, 1) is not None:
            return "T2"
    if y in (8,):
        return "T4"
    if y >= 14:
        return "T5"
    return "T3"


def A_tan_flag(x, y):
    """flags laid in pairs, a course offset at each row"""
    if y in (0, 8) or (x == 0 and y < 8) or (x == 8 and y >= 8):
        return "F3"
    return "F2" if (x, y) in ((5, 3), (12, 11)) else "F1"


def A_tan_frieze(K):
    """the back wall: a sandstone cap, the chamber's own colour as a band of pigment, a frieze of the script cut
    into the stone, courses below"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        if y < 4:
            return "S1" if y else "S2"
        if y == 4:
            return "B4"
        if 5 <= y <= 8:
            return "CH15" if y >= 6 else "B5"
        if 10 <= y <= 15:
            m = tan_frieze_glyphs(x, y, 10, 2, "B5", "S1")
            return m or "B2"
        if y == 9 or y == 16:
            return "B4"
        cy = (y - 17) % 5
        if cy == 4:
            return "B4"
        off = 0 if ((y - 17) // 5) % 2 == 0 else 4
        return "B4" if (x + off) % 8 == 0 else ("B1" if cy == 0 else "B2")
    K.fn(f)


def A_tan_door(K):
    """a door into the dark, under a stepped lintel"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        if y >= 32:
            return tan_base(r, PA)
        if x in (0, 15):
            return "OUT"
        if y < 4:
            return "S1" if y else "S2"
        if y < 7:
            return "B4" if (x < 3 + (y - 4) or x > 12 - (y - 4)) else "B1"
        if 3 <= x <= 12 and y >= 9:
            return "D3" if y > 10 else "D2"
        if 3 <= x <= 12:
            return "B5"
        return "B2" if y % 5 else "B4"
    K.fn(f)


def A_tan_face(K):
    K.fn(lambda x, y: A_tan_facepx(x, y, ktile(K, x, y)) if vrole5(K, x, y) in ("face", "studR", "stud", "crack")
         else tan_base(vrole5(K, x, y), PA))


def A_tan_floor(K):
    K.fn(lambda x, y: A_tan_flag(x, y) if vrole5(K, x, y) in ("flagL", "flag", "flagD")
         else tan_base(vrole5(K, x, y), PA))


# ------------------------------------------------------------------ TANOBY B: THE READER CHANGED (interlinear)
PB = dict(PA)


def punch(x, gi):
    """the machine's reading of glyph gi: a row of holes, one per column the glyph inks more than twice"""
    g = GLYPHS[gi % len(GLYPHS)]
    col = x % 4
    return col < 3 and sum(g[y][col] for y in range(5)) >= 2


def B_tan_zone(kind, role, x, y, K):
    m = tan_base(role, PB)
    if kind == "face" and role in ("face", "studR", "stud", "crack"):
        return B_tan_facepx(x, y % 16, ktile(K, x, y))
    if kind == "floor" and role in ("flagL", "flag", "flagD"):
        return B_tan_flag(x % 16, y % 16)
    return m


def B_tan_facepx(x, y, t):
    """every wall carries two lines: the script in ink, and under it the machine's reading of it as holes in a tape"""
    xx = x % 8
    if 1 <= y <= 5:
        return "N1" if face_glyph(x, y, t, 1) is not None else "T3"
    if 9 <= y <= 12:
        if y in (9, 12):
            return "N2"
        gi = FACE_GLYPHS.get(t, 0) + (0 if xx < 4 else 1)
        return "OUT" if (y == 10 and punch(xx % 4, gi)) else "X1"
    if y >= 14:
        return "T5"
    return "T3"


def B_tan_flag(x, y):
    """the flags ruled like a page"""
    if x in (0, 15) or y in (0, 15):
        return "F3"
    return "F2" if y % 4 == 3 and 2 <= x <= 13 else "F1"


def B_tan_frieze(K):
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        if y < 4:
            return "S1" if y else "S2"
        if y == 4:
            return "B4"
        if 5 <= y <= 8:
            return "CH15" if y >= 6 else "B5"
        if 10 <= y <= 14:
            for k in range(4):
                if glyph_at(6 + k, x, y, 4 * k, 10):
                    return "D3"
            return "B1"
        if 17 <= y <= 20:                              # the tape: the machine's reading, the same four glyphs
            if y in (17, 20):
                return "D1"
            return "D3" if (y == 18 and punch(x, 6 + x // 4)) else "S2"
        if y in (9, 15, 16, 21):
            return "B4"
        return "B2" if (x + (y // 4) * 4) % 8 else "B4"
    K.fn(f)


def B_tan_door(K):
    """a tablet in the door: one column of holes, read top to bottom"""
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        if y >= 32:
            return tan_base(r, PB)
        if x in (0, 15):
            return "OUT"
        if y < 4:
            return "S1" if y else "S2"
        if 3 <= x <= 12 and 6 <= y <= 30:
            if x in (7, 8) and y % 3 == 0 and H(y, 0, 5) % 3:
                return "D3"
            return "S2" if 4 <= x <= 11 else "D1"
        return "B2" if y % 5 else "B4"
    K.fn(f)


def B_tan_face(K):
    K.fn(lambda x, y: B_tan_facepx(x, y, ktile(K, x, y)) if vrole5(K, x, y) in ("face", "studR", "stud", "crack")
         else tan_base(vrole5(K, x, y), PB))


def B_tan_floor(K):
    K.fn(lambda x, y: B_tan_flag(x, y) if vrole5(K, x, y) in ("flagL", "flag", "flagD")
         else tan_base(vrole5(K, x, y), PB))


# ------------------------------------------------------------------ TANOBY C: STRATUM (laid down, worn away)
PC = dict(PA)
STRATA = [("N1", 2), ("T2", 3), ("X1", 2), ("T4", 3), ("N2", 2), ("T3", 4)]    # top down: (material, rows)


def stratum(y):
    acc = 0
    for m, n in STRATA:
        acc += n
        if y < acc:
            return m
    return "T5"


def C_tan_zone(kind, role, x, y, K):
    m = tan_base(role, PC)
    if kind == "face" and role in ("face", "studR", "stud", "crack"):
        return C_tan_facepx(x, y % 16, ktile(K, x, y))
    if kind == "floor" and role in ("flagL", "flag", "flagD"):
        return C_tan_flag(x % 16, y % 16)
    if kind == "top" and role in ("top",):
        return "N1" if y % 16 == 11 else "T1"
    return m


def C_tan_facepx(x, y, t):
    """the maze walls as strata, the oldest layer at the foot holding what is left of the script: broken glyphs"""
    if y >= 14:
        return "T5"
    if y >= 9:
        gi = face_glyph(x, y, t, 9)
        if gi is not None and H(x, y, gi) % 3:
            return "T5"
        return "T3"
    return stratum(y)


def C_tan_flag(x, y):
    """every flag worn down into a shallow basin: its joint, the shadow under its upper lip, the lit lower lip"""
    if x in (0, 15) or y in (0, 15):
        return "F3"
    if x == 1 or y == 1:
        return "F2"
    if x == 14 or y == 14:
        return "N1"
    return "F1"


def C_tan_frieze(K):
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        if y < 4:
            return "S1" if y else "S2"
        if 5 <= y <= 8:
            return "CH15" if y >= 6 else "B5"
        if y >= 26:                                    # the oldest course: glyphs half gone
            for k in range(4):
                if glyph_at(12 + k, x, y, 4 * k, 26) and H(x, y, k) % 3:
                    return "B5"
            return "B4"
        band = ((y - 9) // 3) % 4
        return ("B1", "B3", "B2", "B6")[band] if not (y == 4) else "B4"
    K.fn(f)


def C_tan_door(K):
    def f(x, y):
        r = vrole5(K, x, y)
        if r is None:
            return None
        if y >= 32:
            return tan_base(r, PC)
        if x in (0, 15):
            return "OUT"
        if y < 4:
            return "S1" if y else "S2"
        if 4 <= x <= 11 and y >= 8:
            return "D3"
        return ("B1", "B3", "B2", "B6")[((y - 4) // 3) % 4]
    K.fn(f)


def C_tan_face(K):
    K.fn(lambda x, y: C_tan_facepx(x, y, ktile(K, x, y)) if vrole5(K, x, y) in ("face", "studR", "stud", "crack")
         else tan_base(vrole5(K, x, y), PC))


def C_tan_floor(K):
    K.fn(lambda x, y: C_tan_flag(x, y) if vrole5(K, x, y) in ("flagL", "flag", "flagD")
         else tan_base(vrole5(K, x, y), PC))


# ---------------------------------------------------------------------------------------- the directions' tables
def direction5(name, title, lines, pp_mat, tan_mat, pp, tan):
    D = dict(name=name, title=title, lines=lines)
    D["pp"] = dict(mat=pp_mat, zone=pp["zone"], housing=pp["housing"], panel=pp["panel"], coil=pp["coil"],
                   drums=pp["drums"], gen=pp["gen"], floor=pp["floor"])
    D["tan"] = dict(mat=tan_mat, zone=tan["zone"], frieze=tan["frieze"], door=tan["door"], face=tan["face"],
                    face2=tan["face"], floor=tan["floor"])
    return D


#  the plant's free slots: row 7's 15 (vanilla's white) and row 8's 4, 7, 8, 9, 14, 15
PP_FREE = dict(WHT=(255, 255, 255), Q4=(156, 65, 65), Q7=(255, 0, 255), Q8=(255, 0, 255), Q9=(255, 0, 255),
               Q14=(246, 238, 222), Q15=(255, 255, 255))

A5 = direction5(
    "A", "THE HEARTBEAT / CARVED, NOT LIT",
    ["PLANT: keepalive drawn literally -- every housing a cabinet whose conduit band is a dark screen carrying one",
     "green trace with a beat in it, a status light on each cabinet; the coils emitters sending rings to nobody; the",
     "drums battery cells, every one charged; the generator one ring and its light. gbacaves' colours, untouched.",
     "TANOBY: an alphabet carved and never lit -- sandstone courses, the chamber's own colour as a band of pigment,",
     "a frieze of the script cut into the back wall and one line of it along every maze wall; doors into the dark."],
    dict(PP_FREE),
    dict(OUT=(58, 44, 40), T1=(232, 212, 168), T2=(206, 180, 134), T3=(176, 146, 104), T4=(140, 112, 80),
         T5=(96, 74, 56), N1=(120, 96, 70), N2=(190, 160, 118), F1=(232, 218, 182), F2=(212, 194, 154),
         F3=(184, 164, 126), F4=(160, 140, 106), F5=(132, 112, 84), X1=(120, 92, 64), X2=(220, 204, 166),
         B1=(236, 214, 164), B2=(204, 176, 124), B3=(180, 150, 104), B4=(130, 102, 72), B5=(84, 62, 46),
         B6=(156, 126, 88), S1=(244, 232, 200), S2=(220, 204, 166), S3=(196, 178, 140), D1=(70, 54, 44),
         D2=(44, 34, 30), D3=(24, 18, 18)),
    dict(zone=A_pp_zone, housing=A_pp_housing, panel=A_pp_panel, coil=A_pp_coil, drums=A_pp_drums, gen=A_pp_gen,
         floor=A_pp_floor),
    dict(zone=A_tan_zone, frieze=A_tan_frieze, door=A_tan_door, face=A_tan_face, floor=A_tan_floor))

B5 = direction5(
    "B", "GROWING UNTENDED / THE READER CHANGED",
    ["PLANT: the PLANT's other meaning -- nobody tends it and it grows: ivy up every housing, thick at the foot and",
     "thin at the cap, the status lights still green in the leaves; moss in the seams; the drums planters; a vine",
     "round each coil. gbacaves' colours, untouched; three greens in row 8's free slots for the planters.",
     "TANOBY: 4.24 -- the same pages, only the reader changed: every inscription has a second line under it, the",
     "machine's reading as holes punched in a tape; the doors tablets with one column of holes; the flags a ruled page."],
    dict(PP_FREE, Q7=(40, 88, 44), Q8=(82, 150, 70), Q9=(150, 210, 110)),
    dict(OUT=(40, 44, 54), T1=(226, 228, 220), T2=(204, 206, 198), T3=(178, 182, 178), T4=(146, 150, 150),
         T5=(98, 104, 112), N1=(52, 58, 76), N2=(70, 128, 140), F1=(232, 230, 218), F2=(206, 204, 192),
         F3=(176, 176, 166), F4=(150, 150, 142), F5=(120, 122, 118), X1=(150, 196, 200), X2=(196, 120, 110),
         B1=(232, 228, 214), B2=(206, 200, 184), B3=(184, 178, 162), B4=(140, 136, 124), B5=(92, 92, 92),
         B6=(164, 158, 142), S1=(244, 242, 234), S2=(218, 222, 216), S3=(190, 196, 192), D1=(70, 128, 140),
         D2=(52, 58, 76), D3=(30, 36, 48)),
    dict(zone=B_pp_zone, housing=B_pp_housing, panel=B_pp_panel, coil=B_pp_coil, drums=B_pp_drums, gen=B_pp_gen,
         floor=B_pp_floor),
    dict(zone=B_tan_zone, frieze=B_tan_frieze, door=B_tan_door, face=B_tan_face, floor=B_tan_floor))

C5 = direction5(
    "C", "OPEN SESSIONS / STRATUM",
    ["PLANT: nobody connected -- every housing a patch panel, two rows of open ports each with its light listening,",
     "a few leads plugged in and hanging to nothing; the walkways cable trays; the coils cable reels never unwound;",
     "the drums transformers; the generator a switchboard of lit jacks (SENTINEL's MEAN LOOK: you may not DETACH).",
     "TANOBY: STRATUM, TANOBY's lobe (the physical layer, memory laid down) -- every wall in bands of sediment, the",
     "script surviving only in the oldest band at the foot and half worn away; the floor worn into shallow basins."],
    dict(PP_FREE, Q4=(206, 120, 70)),
    dict(OUT=(50, 40, 40), T1=(226, 204, 160), T2=(198, 150, 104), T3=(150, 118, 96), T4=(120, 128, 112),
         T5=(76, 64, 60), N1=(232, 214, 176), N2=(176, 96, 70), F1=(214, 196, 160), F2=(190, 170, 134),
         F3=(160, 140, 110), F4=(140, 120, 94), F5=(110, 94, 76), X1=(156, 160, 140), X2=(168, 148, 116),
         B1=(230, 206, 160), B2=(196, 150, 100), B3=(170, 112, 80), B4=(120, 96, 80), B5=(76, 60, 56),
         B6=(138, 140, 120), S1=(240, 224, 190), S2=(214, 196, 160), S3=(186, 170, 136), D1=(80, 64, 56),
         D2=(54, 42, 40), D3=(30, 24, 24)),
    dict(zone=C_pp_zone, housing=C_pp_housing, panel=C_pp_panel, coil=C_pp_coil, drums=C_pp_drums, gen=C_pp_gen,
         floor=C_pp_floor),
    dict(zone=C_tan_zone, frieze=C_tan_frieze, door=C_tan_door, face=C_tan_face, floor=C_tan_floor))
STYLES5 = {"A": A5, "B": B5, "C": C5}


# ---------------------------------------------------------------------------------------- pair 5's sheets
ROOMS_PP = [("PowerPlant", "KEEPALIVE PLANT, the whole floor", None)]
ROOMS_TAN = [(CHAMBERS[0], "MONEAN (row 11's colour)", None), (CHAMBERS[3], "DILFORD (row 12)", None),
             (CHAMBERS[4], "SCUFIB (row 9)", None), (CHAMBERS[2], "WEEPTH (row 8)", None)]
DETAILS5 = [("PowerPlant", (0, 0, 10, 8), "the entrance housings, a hatch, the coils"),
            ("PowerPlant", (35, 2, 49, 8), "the drums and the coils"),
            ("PowerPlant", (24, 33, 35, 40), "a generator, its crown over the housing"),
            (CHAMBERS[0], (0, 0, 10, 6), "the back wall: cap, band, frieze, doors"),
            (CHAMBERS[0], (2, 3, 12, 9), "a maze wall: its top and face"),
            (CHAMBERS[3], (10, 0, 20, 6), "DILFORD's band in its own colour")]


def contact_sheets5(out_dir, states):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: KEEPALIVE PLANT is Nintendo's drawing in gbacaves' STILL RUNNING colours",
                              "(batch E2: only its status lights and the moss in one seam are drawn); TANOBY is",
                              "Nintendo's drawing and colours, with gbatowns' batch G carving 11 tiles (a DRAFT)."])}
    for k in STYLES5:
        titles[k] = ("%s %s" % (k, STYLES5[k]["title"]), STYLES5[k]["lines"])
    pad = 10
    paths = []
    for which, rooms in (("plant", ROOMS_PP), ("tanoby", ROOMS_TAN)):
        blocks = []
        for k in names:
            st = states[k]
            ims = [(room(m, (st, None) if st else None, cr), cap) for m, cap, cr in rooms]
            t, lines = titles[k]
            th = 8 + 12 * len(lines) + 16
            W = sum(i.width for i, _ in ims) + pad * (len(ims) + 1)
            im = Image.new("RGB", (max(W, 1000), th + max(i.height for i, _ in ims) + pad), BG)
            d = ImageDraw.Draw(im)
            text(d, (pad, 6), t.split(" / ")[0], RED)
            if " / " in t:
                text(d, (pad, 18), "/ " + t.split(" / ")[1], RED)
            for j, s in enumerate(lines):
                text(d, (pad + 250, 6 + 12 * j), s)
            x = pad
            for i, cap in ims:
                text(d, (x, th - 13), cap, SOFT)
                im.paste(i, (x, th))
                x += i.width + pad
            blocks.append(im)
        W = max(b.width for b in blocks)
        sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
        d = ImageDraw.Draw(sh)
        text(d, (pad, 8), "T-447 DRAFT, pair 5 -- %s, the real map%s at 1x, three directions beside today's (redrawn in "
                          "place: no block, collision or palette row moves; 0 new tiles)" %
             (("KEEPALIVE PLANT", "") if which == "plant" else ("four of TANOBY's seven chambers", "s")), INK)
        y = 30
        for b in blocks:
            sh.paste(b, (0, y))
            y += b.height
        p = os.path.join(out_dir, "t447p5_%s_1x.png" % which)
        sh.save(p)
        paths.append(p)
    #  3x details
    for part, idxs in ((1, (0, 1, 2)), (2, (3, 4, 5))):
        rowsim = []
        for k in names:
            crops = []
            for i in idxs:
                m, cr, cap = DETAILS5[i]
                im = room(m, (states[k], None) if states[k] else None, cr)
                crops.append((im.resize((im.width * 3, im.height * 3), Image.NEAREST), cap))
            rowsim.append((k, crops))
        cw = sum(c.width for c, _ in rowsim[0][1]) + pad * (len(idxs) + 1) + 130
        ch = max(c.height for c, _ in rowsim[0][1]) + 24
        det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
        d = ImageDraw.Draw(det)
        text(d, (pad, 8), "T-447 DRAFT, pair 5 -- details at 3x (%s)" %
             ("KEEPALIVE PLANT" if part == 1 else "TANOBY"), INK)
        y = 30
        for k, crops in rowsim:
            text(d, (pad, y + 6), titles[k][0][:18], RED)
            x = 130
            for c, cap in crops:
                text(d, (x, y + 2), cap, SOFT)
                det.paste(c, (x, y + 16))
                x += c.width + pad
            y += ch
        p = os.path.join(out_dir, "t447p5_detail_3x_%d.png" % part)
        det.save(p)
        paths.append(p)
    #  the tiles at 3x, each set in its home rows; and the script
    cols = []
    for k in names:
        st = states[k]
        imgs = []
        for key, S in SETS5.items():
            tiles, pals = st[key] if st else (S.cur, {r: TODAY5[key, r] for r in range(16)})
            used_rows = sorted({t // 16 for t in owned5(key)})
            strip = Image.new("RGB", (128, 8 * len(used_rows)), (236, 236, 236))
            o = strip.load()
            for j, rr in enumerate(used_rows):
                for t in range(rr * 16, rr * 16 + 16):
                    if t not in owned5(key):
                        continue
                    hr = home5(S, t)
                    for q in range(64):
                        vv = tiles[t][q]
                        o[(t % 16) * 8 + q % 8, j * 8 + q // 8] = tuple(pals[hr][vv]) if vv else (200, 200, 200)
            imgs.append((S.dir.split("/")[-1] + " (rows of the sheet that maps place)", strip))
        hh = sum(i.height * 3 + 16 for _, i in imgs)
        col = Image.new("RGB", (384, hh), BG)
        y = 0
        dd = ImageDraw.Draw(col)
        for lab, i in imgs:
            dd.text((0, y), lab, fill=SOFT)
            col.paste(i.resize((i.width * 3, i.height * 3), Image.NEAREST), (0, y + 14))
            y += i.height * 3 + 16
        cols.append((titles[k][0], col))
    #  the script itself, at 6x: every glyph, and its distance from the nearest letter
    gs = Image.new("RGB", (len(GLYPHS) * 40 + 8, 56), BG)
    go = gs.load()
    for n, g in enumerate(GLYPHS):
        for yy in range(5):
            for xx in range(3):
                if g[yy][xx]:
                    for a in range(8):
                        for b in range(8):
                            go[8 + n * 40 + xx * 8 + a, 8 + yy * 8 + b] = (60, 44, 36)
    W = max(sum(c.width + pad for _, c in cols) + pad, gs.width + 2 * pad)
    sh = Image.new("RGB", (W, max(c.height for _, c in cols) + 50 + gs.height + 40), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 6), "T-447 DRAFT, pair 5 -- the tiles at 3x, each in its home row (grey: transparent; only the "
                      "sheet's rows that maps place)", INK)
    x = pad
    for t, c in cols:
        text(d, (x, 26), t[:44], RED)
        sh.paste(c, (x, 42))
        x += c.width + pad
    y = 42 + max(c.height for _, c in cols) + 8
    text(d, (pad, y), "TANOBY's script: %d glyphs, each at least %d cells from every letter and digit in any turn or "
                      "mirror (nearest: %d)" % (len(GLYPHS), GLYPH_MIN, min(glyph_distance(g) for g in GLYPHS)), INK)
    sh.paste(gs, (pad, y + 16))
    p = os.path.join(out_dir, "t447p5_tiles_3x.png")
    sh.save(p)
    paths.append(p)
    return paths


# ---------------------------------------------------------------------------------------- pair 5's report
def _literal(path, name):
    """a module-level literal of another tool, read without importing it"""
    import ast
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    return None


def report5():
    bad = 0
    print("\n  pair 5 (KEEPALIVE PLANT + TANOBY) -- DRAFT, %s" %
          ("APPROVED %s" % {k: APPROVED[k] for k in SETS5 if k in APPROVED} if any(k in APPROVED for k in SETS5)
           else "not approved: `--pair 5 --write --approved` refuses"))
    for key, S in SETS5.items():
        own = owned5(key)
        van = [t for t in own if S.cur[t] == S.van[t] and len(set(S.van[t])) > 1]
        rows = sorted({r for t in own for r in S.use[t]["rows"]})
        changed = [r for r in range(16) if [tuple(c) for c in S.vpal[r]] != TODAY5[key, r]]
        print("    %-16s %3d tiles drawn here, %d still Nintendo's drawing; rows placed %s, own %s; rows recoloured "
              "since vanilla %s" % (NAMES[key], len(own), len(van), rows, S.rows, changed or "none"))
    #  the groups
    cnt = collections.Counter()
    for key, setkey, lay, kind, what in GROUPS5:
        if kind == "obj":
            print("      %-4s %-8s %s" % (setkey, key, what))
        else:
            cnt[setkey] += 1
    print("      and %d plant / %d TANOBY block layers, drawn through each direction's zones" % (cnt["pp"], cnt["tan"]))
    #  the script
    dmin = min(glyph_distance(g) for g in GLYPHS)
    print("    TANOBY's script: %d glyphs, nearest to a letter or digit %d cells (needs %d)" % (len(GLYPHS), dmin,
                                                                                         GLYPH_MIN))
    if dmin < GLYPH_MIN or len(GLYPHS) < 16:
        print("  !! the script has a glyph that could be read, or too few glyphs")
        bad = 1
    #  the guards in the other tools
    caves = _literal(os.path.join(ROOT, "tools", "gbacaves.py"), "T447_PLANT")
    if caves is None or set(caves) != set(owned5("pp")):
        print("  !! gbacaves.T447_PLANT is not this pair's plant tiles (%d): its write could redraw them"
              % len(owned5("pp")))
        bad = 1
    else:
        print("    gbacaves.T447_PLANT names the plant's %d tiles: its write keeps them as the engine has them; its rows "
              "7 and 8 are kept here (CAVES_PLANT)" % len(caves))
    towns = _literal(os.path.join(ROOT, "tools", "gbatowns.py"), "LANDMARKS") or {}
    boxed = {b[0] for b in towns.get("tanoby_ruins", [])}
    if boxed != set(CHAMBERS):
        print("  !! gbatowns.LANDMARKS does not hold all seven chambers (%s): its write could redraw TANOBY"
              % sorted(set(CHAMBERS) - boxed))
        bad = 1
    else:
        print("    gbatowns.LANDMARKS holds all seven chambers: its write keeps every TANOBY tile as it is")
    print("    gbapreviews: the chamber's name card (T-445) and the plant's -- pictures, not these tiles; gbamachines: "
          "the plant's consoles (primary/building); gbatowns: the chamber doors on SEVEN ISLAND (sevii_islands_67)")
    known = {"gbacaves.py", "gbatowns.py", "gbamachines.py", "gbapreviews.py", "port_music.py"}
    found = set()
    me = os.path.basename(__file__)
    for f in sorted(glob.glob(os.path.join(ROOT, "tools", "*.py"))):
        if os.path.basename(f) == me:
            continue
        src = open(f, encoding="utf-8", errors="ignore").read()
        if re.search(r"power_plant|PowerPlant|tanoby_ruins|TanobyRuins", src):
            found.add(os.path.basename(f))
    if found - known:
        print("  !! a tool this one does not know names these tilesets: %s -- read it before a write" %
              sorted(found - known))
        bad = 1
    #  each direction: footprints, gbacaves' colours, the chambers' slots, rows 8..12 one ladder
    for k, D in STYLES5.items():
        sets, own = draw5(D)
        for key, S in SETS5.items():
            tiles, pals = sets[key]
            moved = [t for t in range(S.nvan) if any((a == 0) != (b == 0) for a, b in zip(tiles[t], S.cur[t]))]
            if moved:
                print("  !! %s %s: tiles %s change their footprint" % (k, key, moved[:10]))
                bad = 1
            for (sk, r), slots in FIXED5.items():
                if sk == key and any(tuple(pals[r][i]) != TODAY5[sk, r][i] for i in slots):
                    print("  !! %s %s row %d: a kept slot changed" % (k, key, r))
                    bad = 1
            if any(tiles[t] != S.cur[t] for t in range(S.nvan) if (key, t) in VOID5):
                print("  !! %s: the void was drawn" % k)
                bad = 1
        tp = sets["tan"][1]
        if any(tp[r][1:14] != tp[8][1:14] for r in CHAMBER_ROWS):
            print("  !! %s: TANOBY rows 8..12 differ in 1..13 (the back wall's shared tiles)" % k)
            bad = 1
        n = {key: sum(1 for t in owned5(key) if sets[key][0][t] != SETS5[key].van[t]) for key in SETS5}
        print("    %s %-38s redrawn: power_plant %d of %d, tanoby_ruins %d of %d; 0 new tiles; kept slots kept" %
              (k, D["title"], n["pp"], len(owned5("pp")), n["tan"], len(owned5("tan"))))
    return bad


def check_engine5():
    bad = 0
    for bkey, pick in APPROVED.items():
        if bkey not in SETS5:
            continue
        sets, _ = draw5(STYLES5[pick], only=bkey)
        S = SETS5[bkey]
        off = [t for t in range(len(S.cur)) if sets[bkey][0][t] != S.cur[t]]
        rows = [r for r in S.rows if sets[bkey][1][r] != TODAY5[bkey, r]]
        if off or rows:
            print("  !! %s: the engine differs from `--pair 5 --write --approved` (%s) in tiles %s rows %s"
                  % (NAMES[bkey], pick, off[:12], rows))
            bad = 1
    return bad


def main5():
    picks = {k: APPROVED[k] for k in SETS5 if k in APPROVED}
    if WRITE:
        if "--approved" not in ARGS or not picks:
            print("  --write refused: T-447 pair 5 is a draft. APPROVED holds no pick for it (%s); the user picks a "
                  "direction per\n  building first, it goes into APPROVED (\"pp\": X, \"tan\": Y), then "
                  "`--pair 5 --write --approved` writes power_plant's\n  tiles and rows 7, 8 (gbacaves' slots kept) and "
                  "tanoby_ruins' tiles and rows 7..12 (each chamber's slots kept)." % (picks or "empty"))
            return 1
        for bkey, pick in picks.items():
            sets, _ = draw5(STYLES5[pick], only=bkey)
            S = SETS5[bkey]
            G.save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[bkey][0], os.path.join(GBA, S.dir, "tiles.png"))
            for r in S.rows:
                write_pal(os.path.join(GBA, S.dir, "palettes", "%02d.pal" % r), sets[bkey][1][r])
            print("  written: %s, direction %s" % (NAMES[bkey], pick))
        return 0
    bad = report()
    if DRAFT is not None:
        out = DRAFT if DRAFT != DRAFT_DEFAULT else DRAFT5_DEFAULT
        os.makedirs(out, exist_ok=True)
        states = collections.OrderedDict()
        states["NOW"] = None
        summary = {}
        for k, D in STYLES5.items():
            sets, owner = draw5(D)
            for key, S in SETS5.items():
                dd = os.path.join(out, k, S.dir.split("/")[-1])
                os.makedirs(os.path.join(dd, "palettes"), exist_ok=True)
                G.save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[key][0], os.path.join(dd, "tiles.png"))
                for r in S.rows:
                    write_pal(os.path.join(dd, "palettes", "%02d.pal" % r), sets[key][1][r])
            states[k] = sets
            ch = {key: sum(1 for t in owned5(key) if sets[key][0][t] != SETS5[key].van[t]) for key in SETS5}
            summary[k] = dict(title=D["title"], lines=D["lines"], tiles_redrawn=ch, new_tiles=0,
                              rows={"power_plant": PP.rows, "tanoby_ruins": TAN.rows})
        json.dump(dict(ticket="T-447", pair=5, status="DRAFT -- not in the engine",
                       approved={k: APPROVED[k] for k in SETS5 if k in APPROVED}, directions=summary,
                       glyphs=["".join(str(c) for r in g for c in r) for g in GLYPHS]),
                  open(os.path.join(out, "directions.json"), "w"), indent=1)
        for p in contact_sheets5(out, states):
            print("  sheet:", p)
    if APPROVED:
        bad = check_engine() or bad
    return 1 if bad else 0


# ============================================================================================ PAIR 6
#  THE LEAGUE + THE HALL OF FAME -- the ending, walked straight through (pair 4's notes give the order): the REVIEW
#  BOARD's four hearing rooms, met IV, II, III, I (vision 6: PHLEGMATIC, CHOLERIC, MELANCHOLIC, SANGUINE -- the
#  humours, which were "literally colored fluids"), AL CLEAR's room (the incumbent: CONTENT-optimal, "mechanically
#  excellent, philosophically wrong"), then the record (4.1: "she records you into a system that flattens you into
#  stats"; 3386: the HALL OF FAME is where the institution records AL CLEAR's name).
#
#  pokemon_league  the four hearing rooms and AL CLEAR's room. All six of its own rows are this pair's: row 7 the
#                  stone every room shares (walls, doors, AL CLEAR's steps), rows 8..11 the four hearing rooms (IV 8,
#                  II 9, III 10, I 11 -- each room's own row draws the SAME floor, ring and wall-light tiles, so the
#                  fifteen materials stand at the same index in all four and only their colours differ: that is how
#                  each room carries its member's humour), row 12 AL CLEAR's. Tiles placed in primary/building's
#                  rows (the door's round plate in row 3, AL CLEAR's stair and pillars in row 0, his runner in row 1,
#                  the lights beside it in row 5) are redrawn in those rows' fixed colours. The engine names nine
#                  blocks here (metatile_labels.h: the door 0x28E/0x296 OPEN, the entry 0x29D..0x2A7 CLOSED behind
#                  the player, LANCE's floor shade 0x311): each keeps its id and still reads as what it is, and the
#                  two tiles only those blocks draw (49, 51) are drawn with them. The statues in I's corridor are
#                  primary/building's (batch G's LEAGUE statue, gbabuilding): never touched here.
#  hall_of_fame    the HALL OF FAME. Its rows 7, 10, 11 are drawn by the HALL alone; the UNION ROOM (a link room)
#                  shares the tileset but draws rows 8 and 9 and its own tiles, and the three tiles both rooms draw
#                  (45..47, the floor's front edge, in primary row 5) are kept: the UNION ROOM does not change. The
#                  RECORD's machine keeps its six lights where FLDEFF_HALL_OF_FAME_RECORD sets the six balls (field_
#                  effect.c, 117,60); its monitor sprite is gbafieldfx's (hof_monitor), not these tiles.
#
#  The same rules as pairs 4 and 5: redrawn IN PLACE, every tile keeps its footprint, no block, layer, flip, palette
#  row, behaviour or collision bit moves and no map is touched; 0 new tiles. Neither tileset has an animation (both
#  callbacks NULL) and nothing recolours them at run time (no tileset test in fieldmap.c). gbatowns batch G drew 91
#  LEAGUE and 38 HALL tiles by role (a DRAFT, 2026-10-28); gbatowns.LANDMARKS now holds all five LEAGUE rooms and the
#  HALL (T-447 pair 6), so its write keeps every tile they draw as the engine has it, and this pair redraws them.
#  No readable words anywhere: no letters, numerals or marks in any direction (the report checks the four secrets'
#  words are nowhere in this file's art -- there is no text in it at all).

DRAFT6_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t447_pair6")
LG = G.Set("lg", "gTileset_PokemonLeague", [7, 8, 9, 10, 11, 12])
HOF = G.Set("hof", "gTileset_HallOfFame", [7, 10, 11])
SETS6 = {"lg": LG, "hof": HOF}
G.SETS.update(SETS6)
NAMES.update({"lg": "the LEAGUE", "hof": "the HALL OF FAME"})
TODAY6 = {(k, r): [tuple(c) for c in read_pal(os.path.join(GBA, S.dir, "palettes/%02d.pal" % r))]
          for k, S in SETS6.items() for r in range(16)}

HEARING = [("PokemonLeague_LoreleisRoom", 8, "IV", "PHLEGMATIC"), ("PokemonLeague_BrunosRoom", 9, "II", "CHOLERIC"),
           ("PokemonLeague_AgathasRoom", 10, "III", "MELANCHOLIC"), ("PokemonLeague_LancesRoom", 11, "I", "SANGUINE")]
CHAMPION = "PokemonLeague_ChampionsRoom"
HALL = "PokemonLeague_HallOfFame"
UNION = "UnionRoom"
LEAGUE_MAPS = [h[0] for h in HEARING] + [CHAMPION]
#  the blocks the engine names (include/constants/metatile_labels.h), drawn whether or not a map places them
NAMED6 = {0x28E: "Door_Top_Open", 0x296: "Door_Mid_Open", 0x29D: "Entry_TopLeft_Closed", 0x29E: "Entry_TopMid_Closed",
          0x29F: "Entry_TopRight_Closed", 0x2A5: "Entry_BottomLeft_Closed", 0x2A6: "Entry_BottomMid_Closed",
          0x2A7: "Entry_BottomRight_Closed", 0x311: "Floor_ShadeFull_Lance"}
KEEP_HOF = {45, 46, 47}                              # the floor's front edge (primary row 5), the UNION ROOM's too

#  what each tile is, by its vanilla drawing (read off the five rooms' blocks)
def _kinds(spec):
    out = {}
    for kind, ts in spec:
        for t in ts:
            out[t] = kind
    return out


R = lambda a, b: list(range(a, b + 1))
KIND_LG = _kinds([
    ("walltop", [5, 6, 21, 22, 16]), ("wall", [7, 8, 9, 10, 23, 24, 25, 26, 32, 33, 48]),
    ("door", [34, 35, 36, 47, 49, 50, 51, 63] + R(70, 79) + R(86, 95)), ("plate", R(80, 85)),
    ("floor", [1, 2, 17, 18, 96, 154, 155, 170, 171]), ("kerb", [3, 4, 19, 20]),
    ("ring", R(11, 15) + R(27, 31) + R(37, 46) + R(52, 62)),
    ("light", R(156, 159) + R(172, 175)), ("lightwall", [126, 127, 142, 143]),
    ("pillar", R(97, 125) + R(128, 135) + R(144, 149) + [152, 153, 164, 165, 168, 169]),
    ("cfloor", [160, 161, 162, 176, 177, 178, 184, 186, 199]),
    ("cwall", R(180, 183) + [185] + R(196, 198) + [200, 201] + R(212, 217) + R(228, 233) + R(244, 247) +
     R(260, 263) + R(276, 281) + R(292, 295) + [308, 309, 324]),
    ("cstep", R(224, 226) + R(234, 236) + R(248, 251) + R(264, 267)),
    ("cemblem", [188, 202, 203, 204, 218, 219, 220]), ("cpillar", [189, 190, 205, 206, 221, 222]),
    ("cdoor", R(240, 243) + R(256, 259) + R(272, 275) + R(288, 291)),
    ("runner", [304, 307] + R(320, 323) + R(336, 339)), ("clight", [237, 238, 239, 253, 254, 255]),
])
KIND_HOF = _kinds([
    ("wall", R(1, 10) + R(17, 26) + R(33, 40) + R(49, 56) + R(65, 68) + [71, 72] + R(81, 84) + [87, 88]),
    ("machine", [41, 42] + R(57, 62) + R(73, 78) + R(89, 94) + [79] + R(95, 101) + R(110, 117) + R(122, 127)),
    ("side", [64, 69, 70, 85, 86, 48]), ("floor", [16]), ("pillar", [11, 12, 13, 14, 27, 28, 29, 30, 43, 44]),
    ("emblem", [128, 129, 130, 144, 145, 146, 160, 161, 162]),
])
KIND6 = {"lg": KIND_LG, "hof": KIND_HOF}


def map_blocks(m):
    lid = G.LAYOUT_OF_MAP[m]
    l = next(x for x in G.LAYOUTS if x["id"] == lid)
    bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    W = l["width"]
    return [[struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF for x in range(W)] for y in range(l["height"])]


def region6(S, blocks, layer):
    """a grid of block ids -> (layout of (tile, flip), the palette row of each tile) for one layer"""
    lay, rg = [], []
    for brow in blocks:
        for half in (0, 1):
            L, Rr = [], []
            for b in brow:
                if b is None or b < 640 or (b - 640 + 1) * 16 > len(S.mt):
                    L += [None, None]
                    Rr += [None, None]
                    continue
                ee = struct.unpack_from("<8H", S.mt, (b - 640) * 16)
                for q in (half * 2, half * 2 + 1):
                    e = ee[layer * 4 + q]
                    t = e & 0x3FF
                    if t < 640:
                        L.append(None)
                        Rr.append(None)
                    else:
                        L.append((t - 640, ("h" if (e >> 10) & 1 else "") + ("v" if (e >> 11) & 1 else "")))
                        Rr.append(e >> 12)
            lay.append(L)
            rg.append(Rr)
    return lay, rg


def owned6(setkey):
    """the tiles this pair draws: every tile the LEAGUE's five rooms place or its named blocks draw; the HALL's own
    (never a tile the UNION ROOM draws, never the front edge)"""
    S = SETS6[setkey]
    if setkey == "lg":
        ts = {t for t in S.use if t < S.nvan and any(S.van[t])}
        for b in NAMED6:
            for e in struct.unpack_from("<8H", S.mt, (b - 640) * 16):
                if (e & 0x3FF) >= 640 and any(S.van[(e & 0x3FF) - 640]):
                    ts.add((e & 0x3FF) - 640)
        return sorted(ts)
    return sorted(t for t in S.use if t < S.nvan and any(S.van[t]) and S.use[t]["maps"] == {HALL}
                  and t not in KEEP_HOF)


def rows_of6(setkey, t):
    S = SETS6[setkey]
    if t in S.use and S.use[t]["rows"]:
        return dict(S.use[t]["rows"])
    return {7: 1}                                     # 49, 51: only the CLOSED entry draws them, in row 7


# ---------------------------------------------------------------------------------------- the scene
class Scene:
    """a room (or a named block) as one picture: both layers' kinds and vanilla colours, the components the painters
    draw whole (pillars, the ring, the machine, the emblem)"""

    def __init__(self, setkey, name, blocks, maprow=None):
        self.setkey, self.name, self.blocks = setkey, name, blocks
        S = SETS6[setkey]
        self.layers = [region6(S, blocks, layer) for layer in (0, 1)]
        self.th = len(self.layers[0][0])
        self.tw = max(len(r) for r in self.layers[0][0])
        self.w, self.h = self.tw * 8, self.th * 8
        self.row = maprow
        kinds = KIND6[setkey]
        self.kindL = [[[None] * self.w for _ in range(self.h)] for _ in (0, 1)]
        self.colL = [[[None] * self.w for _ in range(self.h)] for _ in (0, 1)]
        self.ukind = [[None] * self.w for _ in range(self.h)]
        self.L = 0
        for layer in (0, 1):
            lay, rg = self.layers[layer]
            for ty, r in enumerate(lay):
                for tx, spec in enumerate(r):
                    if spec is None:
                        continue
                    t, fl = spec
                    row = rg[ty][tx]
                    pal = S.vpal[row] if row >= 7 else VPRI[row]
                    for k in range(64):
                        x, y = k % 8, k // 8
                        sx = 7 - x if "h" in fl else x
                        sy = 7 - y if "v" in fl else y
                        vv = S.van[t][sy * 8 + sx]
                        if vv == 0:
                            continue
                        X, Y = tx * 8 + x, ty * 8 + y
                        self.kindL[layer][Y][X] = self.ukind[Y][X] = kinds.get(t, "misc")
                        self.colL[layer][Y][X] = pal[vv]
        self.comps = {}

    @property
    def kind(self):
        """the kinds in the layer being painted (a layer-1 pillar over a floor tile leaves the floor a floor)"""
        return self.kindL[self.L]

    @property
    def col(self):
        return self.colL[self.L]

    def comp(self, kind):
        """the 8-connected components of one kind, as bounding boxes, largest first"""
        if kind in self.comps:
            return self.comps[kind]
        seen, out = set(), []
        for y in range(self.h):
            for x in range(self.w):
                if self.ukind[y][x] != kind or (x, y) in seen:
                    continue
                st, pts = [(x, y)], []
                seen.add((x, y))
                while st:
                    a, b = st.pop()
                    pts.append((a, b))
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            u, v2 = a + dx, b + dy
                            if 0 <= u < self.w and 0 <= v2 < self.h and (u, v2) not in seen and self.ukind[v2][u] == kind:
                                seen.add((u, v2))
                                st.append((u, v2))
                xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                out.append((min(xs), min(ys), max(xs), max(ys), len(pts)))
        out.sort(key=lambda c: -c[4])
        out = [c for c in out if c[4] >= 24]
        if kind == "pillar":                          # I's horns stand touching: one vessel each
            split = []
            for c in out:
                h = c[3] - c[1] + 1
                n = max(1, int(round(h / 40.0))) if h > 52 else 1
                for i in range(n):
                    split.append((c[0], c[1] + i * h // n, c[2], c[1] + (i + 1) * h // n - 1, c[4] // n))
            out = split
        self.comps[kind] = out
        return self.comps[kind]

    def box_at(self, kind, x, y):
        for c in self.comp(kind):
            if c[0] <= x <= c[2] and c[1] <= y <= c[3]:
                return c
        return None

    def lum(self, x, y):
        c = self.col[y][x]
        return 0.0 if c is None else (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255.0


def scenes6():
    out = []
    for m in LEAGUE_MAPS:
        out.append(Scene("lg", m, map_blocks(m), dict(HEARING_ROW).get(m)))
    out.append(Scene("lg", "the entry, CLOSED", [[0x29D, 0x29E, 0x29F], [0x2A5, 0x2A6, 0x2A7]], 11))
    out.append(Scene("lg", "the door, OPEN", [[0x28E], [0x296]], 8))
    out.append(Scene("lg", "LANCE's floor shade", [[0x311]], 11))
    out.append(Scene("hof", HALL, map_blocks(HALL)))
    return out


HEARING_ROW = [(h[0], h[1]) for h in HEARING]


# ---------------------------------------------------------------------------------------- materials, resolving
#  each own row's fifteen materials (index 1..15). Rows 8..11 carry ONE list (the hearing rooms' shared tiles); the
#  colours of H1..H4 (the humour), A1/A2 (its accent) and F1..F3 (the floor) are each room's own.
ROWS6 = {("lg", 7): ["OUT", "GRY", "SIG", "W1", "W2", "W3", "W4", "LMP", "LMPD", "E1", "E2", "E3", "E4", "E5", "E6"],
         ("lg", 12): ["INK", "SL1", "FL1", "FL0", "WHT", "GRY12", "WA1", "WA2", "FL2", "GD1", "Q1", "WA0", "GD0", "WA3",
                      "BLK"]}
for _r in (8, 9, 10, 11):
    ROWS6["lg", _r] = ["WHT", "LG", "DG", "H1", "H2", "H3", "H4", "S1", "S2", "S3", "A1", "A2", "F1", "F2", "F3"]
ROWS6["hof", 7] = ["OUT", "GRY", "P3", "WHT", "B1", "B2", "B3", "FL1", "FL2", "B0", "Y1", "Y2", "B4", "AMB", "B5"]
ROWS6["hof", 10] = ["P1", "P2", "M1", "M2", "M3", "M4", "M5", "OUT", "GRY", "M0", "WHT", "M6", "M7", "AMB", "AMB2"]
ROWS6["hof", 11] = ["OUT", "GRY", "C1", "WHT", "C2", "C3", "C4", "C5", "C6", "C0", "Y1", "Y2", "Y3", "Y4", "C7"]


def pals6(D, setkey):
    S = SETS6[setkey]
    out = {}
    for r in range(16):
        if r in S.rows:
            row = [TODAY6[setkey, r][0]]
            over = D.get("rowcol", {}).get((setkey, r), {})
            for n in ROWS6[setkey, r]:
                row.append(tuple(over.get(n, D["mat"][n])))
            out[r] = row
        else:
            out[r] = list(TODAY6[setkey, r])
    for r in range(7):                                # primary/building's rows, as the engine has them (fixed)
        out[r] = [tuple(c) for c in G.PPAL[r]]
    return out


def resolve6(mats, base, rows, D, pals, setkey):
    """64 materials -> 64 indices for a tile placed in ROWS. A material its rows hold at one index takes it exactly;
    anything else the nearest colour (weighted over the rows). The footprint is exact: 0 stays 0, a drawn pixel
    stays drawn; None keeps vanilla's index."""
    px, cache = [], {}
    for k, m in enumerate(mats):
        if base[k] == 0:
            px.append(0)
            continue
        if m is None:
            px.append(base[k])
            continue
        if m not in cache:
            idx = {ROWS6[setkey, r].index(m) + 1 for r in rows if (setkey, r) in ROWS6 and m in ROWS6[setkey, r]}
            if len(idx) == 1 and all((setkey, r) in ROWS6 and m in ROWS6[setkey, r] for r in rows):
                cache[m] = idx.pop()
            else:
                cols = {}
                for r in rows:
                    over = D.get("rowcol", {}).get((setkey, r), {})
                    cols[r] = tuple(over.get(m, D["mat"].get(m, (255, 0, 255))))
                best, bd = 1, 1e18
                for i in range(1, 16):
                    d = 0
                    for r, wgt in rows.items():
                        d += wgt * sum((a - b) ** 2 for a, b in zip(pals[r][i], cols[r]))
                    if d < bd:
                        best, bd = i, d
                cache[m] = best
        px.append(cache[m])
    return px


def draw6(D, only=None):
    """-> {setkey: (tiles, palettes)}, owner {(setkey, t): scene}"""
    out = {k: ([t[:] for t in S.cur], pals6(D[k], k)) for k, S in SETS6.items()}
    owner = {}
    own = {k: set(owned6(k)) for k in SETS6}
    for sc in SCENES6:
        if only and sc.setkey != only:
            continue
        S = SETS6[sc.setkey]
        DD = D[sc.setkey]
        for layer in (0, 1):
            lay, rg = sc.layers[layer]
            if not any(s for r in lay for s in r):
                continue
            K = Cv(lay, sc.setkey)
            K.layer, K.sc = layer, sc
            sc.L = layer
            f = DD["paint"]
            K.fn(lambda x, y: f(sc, x, y, K))
            for t, mats in K.tiles().items():
                if (sc.setkey, t) in owner or t not in own[sc.setkey]:
                    continue
                out[sc.setkey][0][t] = resolve6(mats, S.van[t], rows_of6(sc.setkey, t), DD, out[sc.setkey][1],
                                                sc.setkey)
                owner[sc.setkey, t] = sc.name
    return out, owner


# ---------------------------------------------------------------------------------------- shared painting helpers
def ramp(names, l):
    """a luminance 0..1 onto a ramp of materials, light first"""
    n = len(names)
    return names[max(0, min(n - 1, int((1.0 - l) * n)))]


def is_out(sc, x, y):
    """vanilla's outline: its darkest ink"""
    return sc.lum(x, y) < 0.36


def hs(x, y, s=0):
    return H(x, y, s) / 255.0


# ------------------------------------------------------------------ the hearing rooms' geometry, read off vanilla
def ring_geom(sc):
    c = sc.comp("ring")
    if not c:
        return None
    x0, y0, x1, y1, _ = c[0]
    return (x0, y0, x1, y1, (x0 + x1 + 1) / 2.0, (y0 + y1 + 1) / 2.0)


def pillar_box(sc, x, y):
    return sc.box_at("pillar", x, y)


def lg_paint(style):
    """the LEAGUE's painter: each pixel by what vanilla had there (its kind) and where it stands in its room"""
    def paint(sc, x, y, K):
        kind = sc.kind[y][x]
        if kind is None:
            return None
        if kind in ("wall", "walltop"):
            return style["wall"](sc, x, y, kind)
        if kind in ("door", "plate"):
            return style["door"](sc, x, y, kind)
        if kind in ("floor", "kerb"):
            return style["floor"](sc, x, y, kind)
        if kind == "ring":
            return style["ring"](sc, x, y)
        if kind in ("light", "lightwall"):
            return style["light"](sc, x, y, kind)
        if kind == "pillar":
            return style["pillar"](sc, x, y)
        if kind in ("cfloor", "cwall", "cstep", "cemblem", "cpillar", "cdoor", "runner", "clight"):
            return style["champion"](sc, x, y, kind)
        return ramp(["LG", "S2", "F2", "DG"], sc.lum(x, y))
    return paint


def door_parts(sc, x, y):
    """(u, v) inside the door's 48x32 frame (the arch over the wall), or None"""
    c = sc.box_at("door", x, y)
    if not c:
        return None
    return x - c[0], y - c[1], c[2] - c[0] + 1, c[3] - c[1] + 1


def champ_geom(sc):
    """AL CLEAR's room: the floor's octagon, the emblem's centre"""
    e = sc.comp("cemblem")
    cx, cy = ((e[0][0] + e[0][2] + 1) / 2.0, (e[0][1] + e[0][3] + 1) / 2.0) if e else (sc.w / 2.0, sc.h / 2.0)
    return cx, cy


# ================================================================== LEAGUE A: THE FOUR VESSELS / CLEAR
def A_wall(sc, x, y, kind):
    l = sc.lum(x, y)
    if is_out(sc, x, y):
        return "OUT"
    if l > 0.86:                                      # vanilla's round lamps on the wall: kept, dimmed
        return "LMP"
    if kind == "walltop":                             # the bench slab's edge: a lit lip, a shaded face
        return "W1" if (y % 16) in (0, 1) else ("W2" if l > 0.62 else "W3")
    #  near-black ashlar: courses of 8, joints every 16 offset per course, a faint grain
    yy = y % 8
    if yy == 7:
        return "W4"
    off = 8 if (y // 8) % 2 else 0
    if (x + off) % 16 == 0:
        return "W4"
    if yy == 0:
        return "W2"
    return "W3" if hs(x // 2, y // 2, 3) > 0.12 else "W2"


def A_door(sc, x, y, kind):
    """the bench: a dark slab door, one seam, a round plate on it -- a vessel's mark, empty"""
    if kind == "plate":
        c = sc.box_at("plate", x, y)
        if c:
            u, v = x - c[0], y - c[1]
            cx, cy = (c[2] - c[0]) / 2.0, (c[3] - c[1]) / 2.0
            d = math.hypot(u - cx, v - cy)
            if is_out(sc, x, y) and d > 6.5:
                return "OUT"
            if abs(d - 5.0) < 0.8:
                return "LMPD"
            if v > cy + 1 and d < 4.5:
                return "SIG"                          # the level line: a vessel's fill, its colour left out
            return "W2" if d < 4.5 else "W3"
    if is_out(sc, x, y):
        return "OUT"
    l = sc.lum(x, y)
    if l > 0.9:
        return "SIG"
    p = door_parts(sc, x, y)
    if p:
        u, v, w, h = p
        if abs(u - w / 2.0) < 0.6:
            return "W4"
    return ramp(["W1", "W2", "W3", "W4"], l)


def A_floor(sc, x, y, kind):
    """UMBRA's floor: near-black flags, one per block, a lighter joint; vanilla's shade (the kerb, the shadows)
    as the flag's darker face"""
    l = sc.lum(x, y)
    u, v = x % 16, y % 16
    if kind == "kerb" or l < 0.55:
        return "F3" if (u + v) % 4 else "F2"
    if u == 15 or v == 15:
        return "F3"
    if u == 0 or v == 0:
        return "F1"
    return "F2" if hs(x, y, 7) > 0.08 else "F1"


def A_ring(sc, x, y):
    """the basin: vanilla's emblem becomes a round vessel set in the floor, its member's humour in it; the square
    frame an inlaid line (a seat place)"""
    g = ring_geom(sc)
    x0, y0, x1, y1, cx, cy = g
    d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
    dy = y + 0.5 - cy
    if d < RING_R:                                    # inside vanilla's circle (its tiles mirror left to right)
        if d > RING_R - 1:
            return "DG"                               # the rim's outer edge
        if d > RING_R - 3:
            return "S1" if dy < 0 else "S2"           # the stone lip, lit from above
        if d > RING_R - 4.2:
            return "DG" if dy < 0 else "H4"           # the inner wall: dark above, the fluid's deep below
        if dy < -13:
            return "H3"                               # the far side, in the lip's shadow
        if abs(d - 15.5) < 0.6 and dy < -6:
            return "H1"                               # the light on the surface, an arc
        if abs(d - 8) < 0.55:
            return "H1"                               # one ripple, standing
        return "H2"
    #  the frame: a fine inlay where vanilla drew its white line, the floor around it
    if sc.lum(x, y) > 0.9:
        return "A2"
    return A_floor(sc, x, y, "floor")


RING_R = 23.6         # vanilla's circle: 48 across, inside its own tiles


def vessel(sc, x, y, fill="H2", hi="H1", deep="H3", glass="S2", glassl="S1", out="DG", foot=("F1", "F2"), level=0.3,
           neck=0.0):
    """a tall glass vessel in a pillar's footprint, filled to LEVEL (a fraction of its height from the top)"""
    c = pillar_box(sc, x, y)
    if not c:
        return None
    x0, y0, x1, y1, _ = c
    w, h = x1 - x0 + 1, y1 - y0 + 1
    u, v = x - x0, y - y0
    cx = (w - 1) / 2.0
    if is_out(sc, x, y):
        return out
    if v >= h - 6:                                    # the foot: a stone base
        return foot[0] if v == h - 6 else foot[1]
    top = int(h * level)
    if v == top:
        return hi                                     # the meniscus
    if abs(u - cx) > cx - 1.2:
        return glass                                  # the glass wall
    if u < cx - 2 and u > cx - 4:
        return glassl                                 # the highlight down the glass
    if v < top:
        return glassl if v < 3 else "LG" if v < top - 1 else glass
    return deep if u > cx + 1 else fill


def A_pillar(sc, x, y):
    return vessel(sc, x, y)


def A_light(sc, x, y, kind):
    """the little wall niches: each a stoppered phial of the humour"""
    if kind == "lightwall":
        return "OUT" if is_out(sc, x, y) else ramp(["W2", "W3", "W4"], sc.lum(x, y))
    c = sc.box_at("light", x, y)
    if not c:
        return "W3"
    u, v = x - c[0], y - c[1]
    w, h = c[2] - c[0] + 1, c[3] - c[1] + 1
    if is_out(sc, x, y):
        return "DG"
    cx = (w - 1) / 2.0
    if 2 <= v <= h - 3 and abs(u - cx) <= 2.5:
        if v <= 3:
            return "S1"                               # the stopper
        if v == 4:
            return "H1"
        return "H3" if u > cx else "H2"
    return "F3" if v < h - 2 else "F2"


def A_champion(sc, x, y, kind):
    """CLEAR: AL CLEAR's room with the four colours gone -- white stone, glass panes for the purple walls, four
    empty vessels for the pillars, a glass walk over the dark, and in the floor a clear vessel with nothing in it."""
    l = sc.lum(x, y)
    if kind == "cplain":                              # the floor round the emblem: vanilla's arrows painted out
        kind, l = "cfloor", 0.7
    cx, cy = champ_geom(sc)
    if kind == "cemblem":                             # a clear vessel with nothing in it (its tiles mirror four ways)
        d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
        if d > 13.6:
            return A_champion(sc, x, y, "cplain")
        if d > 12.6:
            return "WA3"
        if d > 11.4:
            return "WHT"
        if abs(d - 7) < 0.55:
            return "WA1"
        return "FL0"
    if kind == "cwall":
        if is_out(sc, x, y):
            return "INK"
        if x % 16 in (0, 15):
            return "WA3"                              # the mullions
        return ramp(["WA0", "WA1", "WA2", "WA3"], l)
    if kind == "cstep":                               # the benches: pale glass, no black
        return ramp(["E1", "E2", "E3", "E4"], l)
    if kind == "cfloor":
        if is_out(sc, x, y) and l != 0.7:
            return "SL1"
        u, v = x % 16, y % 16
        if u == 0 or v == 0:
            return "FL2"
        return "FL0" if l > 0.8 else "FL1"
    if kind == "cpillar":
        return ramp(["WHT", "GRY12", "SL1", "INK"], l)
    if kind == "cdoor":
        if is_out(sc, x, y):
            return "INK"
        return ramp(["FL0", "FL1", "FL2", "SL1"], l)
    if kind == "runner":                              # a glass walk over the dark: panes, a frame every block
        if is_out(sc, x, y):
            return "RNO"
        if y % 16 in (0, 15) or x % 16 in (0, 15):
            return "RN2"
        return "RN3" if (x % 16 == 3 and y % 16 < 8) else "RN1"
    if kind == "clight":
        return ramp(["WHT", "GRY12", "SL1", "INK"], l)
    return None


# ================================================================== LEAGUE B: THE HEARING / THE INSTRUMENT
def B_wall(sc, x, y, kind):
    l = sc.lum(x, y)
    if is_out(sc, x, y):
        return "OUT"
    if l > 0.86:
        return "LMP"                                  # the sconces, in brass
    if kind == "walltop":
        return "W1" if (y % 16) < 2 else ("W2" if (y % 16) < 6 else "W3")
    #  oak panelling: raised panels 16 wide, a moulding round each, a dado rail where vanilla's lamp line ran
    u, v = x % 16, y % 16
    if u in (0, 15) or v in (0, 15):
        return "W4"
    if u in (1, 14) or v in (1, 14):
        return "W1" if (u == 1 or v == 1) else "W3"
    return "W2" if (x + 2 * y) % 7 else "W3"


def B_door(sc, x, y, kind):
    """a panelled oak door, a brass seal on it -- blank"""
    if kind == "plate":
        c = sc.box_at("plate", x, y)
        if c:
            u, v = x - c[0], y - c[1]
            cx, cy = (c[2] - c[0]) / 2.0, (c[3] - c[1]) / 2.0
            d = math.hypot(u - cx, v - cy)
            if is_out(sc, x, y) and d > 6.5:
                return "OUT"
            if d < 2.2:
                return "LMPD"
            return "LMP" if d < 5 else "SIG"
    if is_out(sc, x, y):
        return "OUT"
    p = door_parts(sc, x, y)
    l = sc.lum(x, y)
    if l > 0.9:
        return "SIG"
    if p:
        u, v, w, h = p
        if (u % 8) in (0, 7):
            return "W4"
    return ramp(["W1", "W2", "W3", "W4"], l)


def B_floor(sc, x, y, kind):
    """parquet, short boards laid in pairs, turning every 8; the shade kept as the boards' darker grain"""
    l = sc.lum(x, y)
    u, v = x % 8, y % 8
    turn = ((x // 8) + (y // 8)) % 2
    a = v if turn else u
    if kind == "kerb" or l < 0.55:
        return "F3" if a % 4 == 3 else "F2"
    if a % 4 == 3:
        return "F3"
    return "F1" if hs(x // 4, y // 4, 9) > 0.3 else "F2"


def B_ring(sc, x, y):
    """the dock: a round carpet in the member's colour where the challenger stands to be heard, a brass rail round
    it; the square frame the bar of the hearing, a rail line"""
    g = ring_geom(sc)
    x0, y0, x1, y1, cx, cy = g
    d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
    if d < RING_R:
        if d > RING_R - 1:
            return "DG"
        if d > RING_R - 3:
            return "A1" if y + 0.5 < cy else "A2"     # the brass rail
        if d > RING_R - 4:
            return "H4"
        if abs(d - 16) < 0.7:
            return "H1"                               # the carpet's border
        if 16.7 < d < 19.6:
            return "H3"
        return "H2"
    if sc.lum(x, y) > 0.9:
        return "A2"
    return B_floor(sc, x, y, "floor")


def B_pillar(sc, x, y):
    """a stack of case files, bound in the member's colour, tied with tape"""
    c = pillar_box(sc, x, y)
    if not c:
        return None
    x0, y0, x1, y1, _ = c
    w, h = x1 - x0 + 1, y1 - y0 + 1
    u, v = x - x0, y - y0
    if is_out(sc, x, y):
        return "DG"
    if v >= h - 5:
        return "F3" if v > h - 3 else "F2"
    band = v // 5
    vv = v % 5
    if vv == 4:
        return "DG" if (u + band) % 3 else "S3"      # between the files
    if vv == 0:
        return "WHT" if u > 1 and u < w - 2 else "S1"    # the paper edge
    if abs(u - (w - 1) / 2.0 + (band % 2) * 2 - 1) < 0.6:
        return "S1"                                   # the tape
    return "H2" if band % 2 else "H3"


def B_light(sc, x, y, kind):
    """the niches: pigeonholes, a rolled brief in each"""
    if kind == "lightwall":
        return "OUT" if is_out(sc, x, y) else ramp(["W2", "W3", "W4"], sc.lum(x, y))
    c = sc.box_at("light", x, y)
    if not c:
        return "F3"
    u, v = x - c[0], y - c[1]
    w, h = c[2] - c[0] + 1, c[3] - c[1] + 1
    if is_out(sc, x, y):
        return "DG"
    if 3 <= v <= 6 and 1 <= u <= w - 2:
        return "WHT" if v < 5 else ("S1" if u % 3 else "H2")   # a roll of paper, a tie in the humour
    return "F3"


def B_champion(sc, x, y, kind):
    """THE INSTRUMENT: AL CLEAR's room as a calibrated gauge -- steel panels ruled with ticks, a floor like graph
    paper, the emblem a dial with every segment of its scale lit, all the way round: mechanically excellent"""
    l = sc.lum(x, y)
    if kind == "cplain":                              # the floor round the emblem: vanilla's arrows painted out
        kind, l = "cfloor", 0.7
    cx, cy = champ_geom(sc)
    if kind == "cemblem":
        dx, dy = x + 0.5 - cx, y + 0.5 - cy
        d = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        if d > 13.6:
            return B_champion(sc, x, y, "cplain")
        if d > 12.4:
            return "INK"
        if d > 8.5:                                   # the scale: every segment lit, a full reading all round
            k = (ang + math.pi) / math.pi * 8
            return "FL0" if abs(k - round(k)) < 0.12 else "GD0"
        if d > 7.5:
            return "WA3"
        return "GD1" if d < 2 else "FL0"
    if kind == "cwall":
        if is_out(sc, x, y):
            return "INK"
        if x % 4 == 0 and (y % 16) < (6 if x % 16 == 0 else 3):
            return "GD1"                              # calibration ticks along every panel
        return ramp(["WA0", "WA1", "WA2", "WA3"], l)
    if kind == "cstep":
        return "OUT" if is_out(sc, x, y) else ramp(["E1", "E2", "E3", "E4"], l)
    if kind == "cfloor":
        if is_out(sc, x, y) and l != 0.7:
            return "SL1"
        if x % 4 == 0 or y % 4 == 0:
            return "FL2" if (x % 16 == 0 or y % 16 == 0) else "FL1"
        return "FL0"
    if kind == "cpillar":
        return ramp(["WHT", "GRY12", "SL1", "INK"], l)
    if kind == "cdoor":
        return "INK" if is_out(sc, x, y) else ramp(["FL0", "FL1", "FL2", "SL1"], l)
    if kind == "runner":                              # a steel grating
        if is_out(sc, x, y):
            return "RNO"
        return "RN2" if (x % 3 == 0 or y % 3 == 0) else "RN1"
    if kind == "clight":
        return ramp(["WHT", "GRY12", "SL1", "INK"], l)
    return None


# ================================================================== LEAGUE C: THE SEASONS / NO WEATHER
def C_wall(sc, x, y, kind):
    l = sc.lum(x, y)
    if is_out(sc, x, y):
        return "OUT"
    if l > 0.86:
        return "LMP"
    if kind == "walltop":
        return "W1" if (y % 16) < 2 else "W2"
    #  limewashed plaster over a stone dado: smooth above, coursed below where vanilla's lamp line ran
    v = y % 48
    if y % 16 >= 12:
        return "W3" if (x + (y // 4)) % 8 else "W4"
    return "W1" if hs(x // 3, y // 3, 5) > 0.85 else "W2"


def C_door(sc, x, y, kind):
    if kind == "plate":
        c = sc.box_at("plate", x, y)
        if c:
            u, v = x - c[0], y - c[1]
            cx, cy = (c[2] - c[0]) / 2.0, (c[3] - c[1]) / 2.0
            d = math.hypot(u - cx, v - cy)
            if is_out(sc, x, y) and d > 6.5:
                return "OUT"
            #  a wheel of four quarters, none lit (the door is every room's)
            if abs(u - cx) < 0.6 or abs(v - cy) < 0.6:
                return "W4"
            return "W2" if d < 5 else "W3"
    if is_out(sc, x, y):
        return "OUT"
    l = sc.lum(x, y)
    if l > 0.9:
        return "SIG"
    return ramp(["W1", "W2", "W3", "W4"], l)


def C_floor(sc, x, y, kind):
    """pale flags, and over them the season's litter -- the same specks in every room, frost in IV's colours, sun
    in II's, leaves in III's, blossom in I's"""
    l = sc.lum(x, y)
    u, v = x % 16, y % 16
    if kind == "kerb" or l < 0.55:
        base = "F3"
    elif u == 15 or v == 15:
        return "F3"
    else:
        base = "F1" if (u + v) % 11 else "F2"
    r = hs(x, y, 21)
    if r > 0.93:
        return "A1"
    if r > 0.88:
        return "A2"
    return base


def C_ring(sc, x, y):
    """the season's wheel: four spokes round a hub, the upper half (the season risen over the horizon) in the room's
    humour, the lower in the floor's stone -- the wheel's tiles are every room's, so it is the colour that turns it"""
    g = ring_geom(sc)
    x0, y0, x1, y1, cx, cy = g
    dx, dy = x + 0.5 - cx, y + 0.5 - cy
    d = math.hypot(dx, dy)
    if d < RING_R:
        if d > RING_R - 1.2:
            return "DG"
        if d < 4:
            return "S3" if d > 3 else "WHT"
        if abs(dx) < 0.8 or abs(dy) < 0.8:
            return "S3"                               # the spokes, and the horizon
        if dy < 0:                                    # the season, risen over the horizon
            return "H1" if d > RING_R - 4 else "H2"
        return "S1" if d > RING_R - 4 else "S2"
    if sc.lum(x, y) > 0.9:
        return "S3"
    return C_floor(sc, x, y, "floor")


def C_pillar(sc, x, y):
    """an urn of the season: the humour glazed down a pale stone urn, a lip, a foot"""
    c = pillar_box(sc, x, y)
    if not c:
        return None
    x0, y0, x1, y1, _ = c
    w, h = x1 - x0 + 1, y1 - y0 + 1
    u, v = x - x0, y - y0
    if is_out(sc, x, y):
        return "DG"
    cx = (w - 1) / 2.0
    if v < 4:
        return "S1" if v < 2 else "S2"                # the lip
    if v >= h - 6:
        return "S2" if v < h - 3 else "S3"
    t = (v - 4) / max(1.0, h - 10)
    if t > 0.25 + 0.15 * math.sin(u * 1.3):
        return "H3" if u > cx + 1 else "H2" if u > cx - 3 else "H1"   # the glaze, run down from the shoulder
    return "S1" if u < cx - 2 else "S2"


def C_light(sc, x, y, kind):
    if kind == "lightwall":
        return "OUT" if is_out(sc, x, y) else ramp(["W2", "W3", "W4"], sc.lum(x, y))
    c = sc.box_at("light", x, y)
    if not c:
        return "F3"
    u, v = x - c[0], y - c[1]
    w, h = c[2] - c[0] + 1, c[3] - c[1] + 1
    if is_out(sc, x, y):
        return "DG"
    if 2 <= v <= h - 3 and 2 <= u <= w - 3:
        return "A1" if (u + v) % 3 == 0 else "H2"     # a niche with the season in it
    return "S3"


def C_champion(sc, x, y, kind):
    """NO WEATHER: AL CLEAR's room sealed like a glasshouse, and his wheel all white -- every season's colour at once,
    which is white light (7.2: white is every wavelength): a room with no season in it"""
    l = sc.lum(x, y)
    if kind == "cplain":                              # the floor round the emblem: vanilla's arrows painted out
        kind, l = "cfloor", 0.7
    cx, cy = champ_geom(sc)
    if kind == "cemblem":
        dx, dy = x + 0.5 - cx, y + 0.5 - cy
        d = math.hypot(dx, dy)
        if d > 13.6:
            return C_champion(sc, x, y, "cplain")
        if d > 12.4:
            return "SL1"
        if d < 2.5:
            return "GRY12"
        if abs(dx) < 0.7 or abs(dy) < 0.7:
            return "GRY12"
        return "WHT"
    if kind == "cwall":
        if is_out(sc, x, y):
            return "INK"
        if x % 8 == 0 or y % 16 == 0:
            return "WA3"                              # the glazing bars
        return "WA0" if (x + y) % 13 == 0 else ramp(["WA0", "WA1", "WA2"], l)
    if kind == "cstep":
        return "OUT" if is_out(sc, x, y) else ramp(["E1", "E2", "E3", "E4"], l)
    if kind == "cfloor":
        if is_out(sc, x, y) and l != 0.7:
            return "SL1"
        u, v = x % 16, y % 16
        return "FL2" if u == 15 or v == 15 else "FL0" if l > 0.8 else "FL1"
    if kind == "cpillar":
        return ramp(["WHT", "GRY12", "SL1", "INK"], l)
    if kind == "cdoor":
        return "INK" if is_out(sc, x, y) else ramp(["FL0", "FL1", "FL2", "SL1"], l)
    if kind == "runner":                              # pale stone boards
        return "RNO" if is_out(sc, x, y) else ("RN2" if y % 16 in (0, 15) else "RN1")
    if kind == "clight":
        return ramp(["WHT", "GRY12", "SL1", "INK"], l)
    return None


# ================================================================== the HALL OF FAME's painter
def hof_paint(style):
    def paint(sc, x, y, K):
        kind = sc.kind[y][x]
        if kind is None:
            return None
        return style[kind if kind in style else "misc"](sc, x, y)
    return paint


def hof_geom(sc, kind):
    c = sc.comp(kind)
    return c[0] if c else None


def machine_px(sc, x, y, P):
    """the RECORD's machine, drawn in place: the panel high on the wall, the console under it, the column with its
    six lights where the six balls are set. P names the direction's materials."""
    l = sc.lum(x, y)
    if is_out(sc, x, y):
        return P["out"]
    c = sc.col[y][x]
    #  vanilla's six orange lights (the balls' places): kept as six lights, in the direction's colour
    if c and c[0] > 200 and c[1] < 180 and c[2] < 80:
        return P["lamp"]
    return P["ramp"](sc, x, y, l)


def card_ramp(sc, x, y, l):
    return ramp(["WHT", "B1", "B2", "B3"], l)


# ------------------------------------------------------------------ HALL A: THE INDEX CARD (sepia)
def HA_wall(sc, x, y):
    """the wall a card catalogue: rows of drawer fronts, each with a pull and an empty label holder, in sepia"""
    if is_out(sc, x, y):
        return "OUT"
    l = sc.lum(x, y)
    u, v = x % 16, y % 8
    if v == 7 or u == 15:
        return "B3"
    if v == 3 and 6 <= u <= 9:
        return "B0"                                   # the pull
    if v == 1 and 4 <= u <= 11:
        return "WHT"                                  # the label holder, nothing in it
    return "B1" if l > 0.7 else "B2"


def HA_side(sc, x, y):
    if is_out(sc, x, y):
        return "OUT"
    return "B3" if y % 8 == 7 else ("B0" if y % 8 == 3 and x % 2 else "B2")


def HA_floor(sc, x, y):
    """card stock ruled into fields: one field to a tile, the rule a faint ink"""
    l = sc.lum(x, y)
    u, v = x % 8, y % 8
    if v == 7:
        return "FL2"
    if u == 7 and v % 2 == 0:
        return "FL2"
    return "FL1" if l > 0.45 else "FL2"


def HA_pillar(sc, x, y):
    """a narrow card cabinet: drawers stacked, a brass pull on each"""
    c = sc.box_at("pillar", x, y)
    if not c:
        return "C3"
    x0, y0, x1, y1, _ = c
    u, v = x - x0, y - y0
    w = x1 - x0 + 1
    if is_out(sc, x, y):
        return "OUT"
    if v < 3:
        return "C1" if v < 2 else "C2"
    if v % 6 == 5:
        return "C4"
    if v % 6 == 2 and abs(u - (w - 1) / 2.0) < 1.6:
        return "Y2"
    return "C2" if u < w // 2 else "C3"


def HA_emblem(sc, x, y):
    """a round date-stamp, its rings and ticks blank"""
    x0, y0, x1, y1, _ = hof_geom(sc, "emblem")
    cx, cy = (x0 + x1 + 1) / 2.0, (y0 + y1 + 1) / 2.0
    dx, dy = x + 0.5 - cx, y + 0.5 - cy
    d = math.hypot(dx, dy)
    if d > 17:
        return HA_floor(sc, x, y)
    if abs(d - 16) < 0.8 or abs(d - 10.5) < 0.7:
        return "M5"
    if 11.5 < d < 15 and abs((math.atan2(dy, dx) / math.pi * 8) % 1 - 0.5) > 0.42:
        return "M5"                                   # the ticks between the rings
    if d < 4:
        return "M4"
    return "M1" if d < 10 else "M2"


def HA_machine(sc, x, y):
    return machine_px(sc, x, y, dict(out="OUT", lamp="AMB", ramp=lambda sc, x, y, l: (
        ramp(["P1", "M1", "M2", "M4", "M5"], l) if sc.kind[y][x] == "machine" else card_ramp(sc, x, y, l))))


# ------------------------------------------------------------------ HALL B: THE STAT SHEET
def HB_wall(sc, x, y):
    """the wall a sheet of rows and columns: ruled bands, the header row darker"""
    if is_out(sc, x, y):
        return "OUT"
    l = sc.lum(x, y)
    if y % 8 == 0:
        return "B3"
    if x % 24 == 0:
        return "B2"
    return "B0" if l > 0.75 else "B1"


def HB_side(sc, x, y):
    if is_out(sc, x, y):
        return "OUT"
    return "B3" if y % 8 == 0 else "B1"


def HB_floor(sc, x, y):
    """graph paper: a fine line every four, a heavier one every eight"""
    u, v = x % 8, y % 8
    if u == 0 or v == 0:
        return "FL2"
    if u == 4 or v == 4:
        return "B0" if (u == 4 and v == 4) else "FL1"
    return "FL1"


def HB_pillar(sc, x, y):
    """a bar meter: a glass column, filled to a level"""
    c = sc.box_at("pillar", x, y)
    if not c:
        return "C3"
    x0, y0, x1, y1, _ = c
    u, v = x - x0, y - y0
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if is_out(sc, x, y):
        return "OUT"
    if v >= h - 4:
        return "C4"
    if u in (1, w - 2) or v < 2:
        return "C2"
    if v < h * 0.45:
        return "C1" if (v % 4) else "C2"              # the empty part, its scale
    return "Y1" if u < w // 2 else "Y2"


def HB_emblem(sc, x, y):
    """the record's shape: a hexagon of six axes, and inside it an uneven hexagon -- a person as six numbers"""
    x0, y0, x1, y1, _ = hof_geom(sc, "emblem")
    cx, cy = (x0 + x1 + 1) / 2.0, (y0 + y1 + 1) / 2.0
    dx, dy = x + 0.5 - cx, y + 0.5 - cy
    ang = math.atan2(dy, dx)
    k = (ang + math.pi / 2) / (math.pi / 3)
    sector = int(math.floor(k)) % 6
    frac = k - math.floor(k)
    def hexr(rad, a):
        return rad * math.cos(math.pi / 6) / math.cos((a % (math.pi / 3)) - math.pi / 6)
    d = math.hypot(dx, dy)
    outer = hexr(17, ang + math.pi / 2)
    if d > outer + 0.7:
        return HB_floor(sc, x, y)
    if d > outer - 0.8:
        return "M5"
    for i in range(6):
        a = -math.pi / 2 + i * math.pi / 3
        if abs(-dx * math.sin(a) + dy * math.cos(a)) < 0.55 and dx * math.cos(a) + dy * math.sin(a) > 0:
            return "M4"                               # the axes
    vals = [0.9, 0.55, 0.75, 0.4, 0.8, 0.6]
    r = (vals[sector] * (1 - frac) + vals[(sector + 1) % 6] * frac) * outer
    if d < r:
        return "M2" if abs(d - r) > 1.2 else "M3"
    return "M0"


def HB_machine(sc, x, y):
    return machine_px(sc, x, y, dict(out="OUT", lamp="AMB", ramp=lambda sc, x, y, l: (
        ramp(["M0", "M1", "M2", "M4", "M5"], l) if sc.kind[y][x] == "machine" else ramp(["WHT", "B0", "B1", "B3"], l))))


# ------------------------------------------------------------------ HALL C: THE CERTIFICATE
def HC_wall(sc, x, y):
    """the wall a certificate's engraved border: interlaced waves, a guilloche"""
    if is_out(sc, x, y):
        return "OUT"
    w1 = 3.5 + 2.5 * math.sin(x * 0.55)
    w2 = 3.5 + 2.5 * math.sin(x * 0.55 + math.pi)
    v = y % 8
    if abs(v - w1) < 0.6 or abs(v - w2) < 0.6:
        return "B2"
    return "B0" if sc.lum(x, y) > 0.6 else "B1"


def HC_side(sc, x, y):
    if is_out(sc, x, y):
        return "OUT"
    w = 3.5 + 2.5 * math.sin(y * 0.55)
    return "B2" if abs(x % 8 - w) < 0.6 else "B1"


def HC_floor(sc, x, y):
    """parchment under a fine engraved lattice"""
    u, v = x % 8, y % 8
    if (u + v) % 8 == 0 or (u - v) % 8 == 0:
        return "FL2"
    return "FL1"


def HC_pillar(sc, x, y):
    """a rolled diploma stood on end, a ribbon round it"""
    c = sc.box_at("pillar", x, y)
    if not c:
        return "C3"
    x0, y0, x1, y1, _ = c
    u, v = x - x0, y - y0
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if is_out(sc, x, y):
        return "OUT"
    if v < 4:
        return "C2" if (u + v) % 3 else "C3"          # the roll's end, a spiral
    if h * 0.45 < v < h * 0.45 + 4:
        return "Y2" if v % 2 else "Y1"                # the ribbon
    return "C1" if u < w // 2 - 1 else "C2" if u < w - 2 else "C3"


def HC_emblem(sc, x, y):
    """a seal: a scalloped foil medallion, blank"""
    x0, y0, x1, y1, _ = hof_geom(sc, "emblem")
    cx, cy = (x0 + x1 + 1) / 2.0, (y0 + y1 + 1) / 2.0
    dx, dy = x + 0.5 - cx, y + 0.5 - cy
    d = math.hypot(dx, dy)
    edge = 14.5 + 1.2 * math.cos(math.atan2(dy, dx) * 12)
    if d > edge + 0.6:
        return HC_floor(sc, x, y)
    if d > edge - 0.8:
        return "M5"
    if abs(d - 9) < 0.7:
        return "M4"
    if d < 9:
        return "M1" if dx + dy < -2 else "M2"
    return "M2" if (int(math.atan2(dy, dx) * 6) % 2) else "M3"


def HC_machine(sc, x, y):
    return machine_px(sc, x, y, dict(out="OUT", lamp="AMB", ramp=lambda sc, x, y, l: (
        ramp(["M1", "M2", "M3", "M4", "M5"], l) if sc.kind[y][x] == "machine" else ramp(["WHT", "B0", "B1", "B2"], l))))


def hof_misc(sc, x, y):
    return ramp(["WHT", "B1", "B2", "OUT"], sc.lum(x, y))


# ================================================================== the directions
HUMOURS = {   # (H1..H4, A1, A2) per hearing room's row: IV pale phlegm, II yellow bile, III black bile, I red blood
    "A": {8: [(246, 246, 238), (214, 220, 210), (172, 182, 176), (126, 136, 134), (196, 204, 198), (100, 110, 110)],
          9: [(255, 236, 130), (236, 196, 60), (196, 146, 30), (138, 96, 22), (226, 186, 70), (120, 84, 24)],
          10: [(118, 110, 134), (62, 58, 72), (34, 30, 42), (14, 12, 20), (150, 140, 170), (40, 36, 48)],
          11: [(248, 112, 100), (214, 52, 52), (164, 26, 38), (104, 14, 26), (232, 90, 84), (110, 20, 30)]},
    "B": {8: [(228, 232, 226), (196, 204, 200), (156, 166, 166), (110, 120, 122), (236, 206, 120), (168, 128, 60)],
          9: [(250, 222, 110), (224, 184, 56), (180, 136, 30), (124, 88, 20), (236, 206, 120), (168, 128, 60)],
          10: [(98, 94, 106), (64, 60, 72), (42, 38, 48), (24, 22, 28), (236, 206, 120), (168, 128, 60)],
          11: [(232, 96, 88), (196, 52, 52), (150, 30, 38), (98, 18, 26), (236, 206, 120), (168, 128, 60)]},
    "C": {8: [(240, 246, 252), (204, 222, 236), (164, 190, 212), (120, 148, 176), (255, 255, 255), (180, 206, 228)],
          9: [(255, 232, 120), (240, 190, 70), (206, 140, 40), (150, 96, 30), (255, 240, 170), (222, 170, 60)],
          10: [(200, 140, 80), (160, 96, 50), (118, 64, 34), (76, 40, 24), (214, 150, 70), (140, 80, 40)],
          11: [(255, 196, 210), (240, 150, 170), (196, 104, 128), (100, 150, 80), (255, 214, 224), (140, 190, 100)]},
}


def hearing_rowcol(k):
    out = {}
    for r, cols in HUMOURS[k].items():
        out["lg", r] = dict(zip(["H1", "H2", "H3", "H4", "A1", "A2"], cols))
    return out


def direction6(name, title, lines, lg_mat, lg_style, hof_mat, hof_style):
    D = dict(name=name, title=title, lines=lines)
    D["lg"] = dict(mat=lg_mat, rowcol=hearing_rowcol(name), paint=lg_paint(lg_style))
    D["hof"] = dict(mat=hof_mat, paint=hof_paint(hof_style))
    return D


A6 = direction6(
    "A", "THE FOUR VESSELS / THE INDEX CARD",
    ["LEAGUE: UMBRA's near-black stone carried inside, and the only colour in each hearing room its member's humour",
     "as a fluid -- the pillars tall glass vessels filled with it, the ring a basin of it set in the floor, the wall",
     "niches stoppered phials: pale phlegm (IV), yellow bile (II), black bile (III), red blood (I). AL CLEAR's room",
     "CLEAR: white stone and glass, four empty vessels, a glass walk over the dark, a clear vessel with nothing in it.",
     "HALL: the record as the INDEX keeps it, in sepia (8.6) -- a card catalogue for walls, the floor ruled into",
     "fields, the pillars card cabinets, the emblem a blank date-stamp; the machine prints the card."],
    dict(OUT=(18, 16, 24), GRY=(70, 68, 80), SIG=(214, 206, 186), W1=(92, 90, 104), W2=(68, 66, 80), W3=(48, 46, 58),
         W4=(32, 30, 40), LMP=(232, 220, 184), LMPD=(150, 140, 118), E1=(226, 232, 238), E2=(184, 194, 206),
         E3=(132, 142, 156), E4=(96, 104, 118), E5=(210, 180, 96), E6=(150, 120, 60),
         WHT=(240, 240, 236), LG=(170, 170, 176), DG=(24, 22, 30), S1=(210, 220, 226), S2=(140, 150, 160),
         S3=(82, 88, 100), F1=(66, 64, 76), F2=(50, 48, 60), F3=(36, 34, 44),
         H1=(255, 255, 255), H2=(200, 200, 200), H3=(150, 150, 150), H4=(100, 100, 100), A1=(200, 200, 200),
         A2=(100, 100, 100),
         INK=(60, 66, 78), SL1=(140, 150, 164), FL1=(222, 228, 234), FL0=(246, 248, 250), GRY12=(176, 184, 196),
         WA1=(214, 222, 232), WA2=(176, 188, 204), FL2=(196, 204, 214), GD1=(226, 196, 110), Q1=(160, 170, 186),
         WA0=(236, 242, 248), GD0=(250, 230, 160), WA3=(128, 140, 160), BLK=(14, 12, 20),
         RN1=(189, 230, 255), RN2=(139, 180, 222), RN3=(255, 255, 255), RNO=(82, 82, 106)),
    dict(wall=A_wall, door=A_door, floor=A_floor, ring=A_ring, pillar=A_pillar, light=A_light, champion=A_champion),
    dict(OUT=(52, 38, 28), GRY=(140, 120, 96), P3=(200, 180, 146), WHT=(244, 234, 210), B1=(176, 134, 88),
         B2=(140, 100, 62), B3=(96, 66, 42), FL1=(232, 220, 192), FL2=(204, 186, 150), B0=(214, 176, 110),
         Y1=(226, 190, 120), Y2=(184, 140, 72), B4=(120, 88, 58), AMB=(250, 196, 90), B5=(222, 204, 170),
         P1=(236, 226, 200), P2=(212, 196, 162), M1=(220, 206, 176), M2=(188, 166, 128), M3=(160, 136, 100),
         M4=(124, 98, 70), M5=(84, 62, 42), M0=(240, 232, 212), M6=(200, 184, 152), M7=(170, 150, 118),
         AMB2=(200, 140, 60), C1=(214, 186, 140), C2=(170, 128, 84), C3=(130, 94, 60), C4=(90, 64, 42),
         C5=(232, 220, 192), C6=(204, 186, 150), C0=(150, 120, 90), Y3=(150, 112, 60), Y4=(110, 80, 44),
         C7=(196, 170, 130)),
    dict(wall=HA_wall, side=HA_side, floor=HA_floor, pillar=HA_pillar, emblem=HA_emblem, machine=HA_machine,
         misc=hof_misc))

B6 = direction6(
    "B", "THE HEARING / THE STAT SHEET",
    ["LEAGUE: the REVIEW BOARD as a hearing -- oak panelling and brass sconces, a parquet floor, the ring a round",
     "dock (a carpet in the member's colour inside a brass rail, where the challenger stands to be heard), the",
     "pillars stacks of case files bound in that colour, the niches pigeonholes. AL CLEAR's room THE INSTRUMENT:",
     "steel panels ruled with ticks, graph-paper floor, the emblem a dial with every segment lit all the way round.",
     "HALL: the record as numbers -- walls of ruled rows, graph-paper floor, the pillars bar meters, the emblem a",
     "hexagon of six axes with a smaller hexagon plotted in it (a person as six stats); the machine a tabulator."],
    dict(OUT=(34, 22, 18), GRY=(110, 96, 84), SIG=(232, 196, 96), W1=(178, 128, 82), W2=(146, 98, 60),
         W3=(112, 72, 44), W4=(80, 50, 32), LMP=(250, 226, 150), LMPD=(196, 156, 80), E1=(210, 214, 220),
         E2=(160, 166, 176), E3=(110, 116, 128), E4=(70, 76, 88), E5=(250, 250, 246), E6=(60, 64, 72),
         WHT=(250, 246, 232), LG=(214, 206, 186), DG=(40, 30, 26), S1=(232, 222, 196), S2=(196, 184, 156),
         S3=(150, 136, 110), F1=(190, 170, 140), F2=(160, 140, 110), F3=(124, 106, 82),
         H1=(255, 255, 255), H2=(200, 200, 200), H3=(150, 150, 150), H4=(100, 100, 100), A1=(236, 206, 120),
         A2=(168, 128, 60),
         INK=(30, 34, 40), SL1=(90, 98, 110), FL1=(226, 230, 226), FL0=(246, 248, 244), GRY12=(150, 156, 164),
         WA1=(176, 184, 194), WA2=(134, 142, 154), FL2=(196, 202, 200), GD1=(64, 70, 82), Q1=(110, 118, 130),
         WA0=(214, 220, 228), GD0=(24, 26, 30), WA3=(96, 104, 116), BLK=(14, 12, 20),
         RN1=(180, 180, 164), RN2=(123, 123, 123), RN3=(213, 213, 172), RNO=(82, 82, 106)),
    dict(wall=B_wall, door=B_door, floor=B_floor, ring=B_ring, pillar=B_pillar, light=B_light, champion=B_champion),
    dict(OUT=(28, 36, 52), GRY=(120, 132, 150), P3=(176, 188, 204), WHT=(240, 246, 252), B1=(196, 210, 226),
         B2=(150, 170, 196), B3=(96, 116, 146), FL1=(222, 232, 240), FL2=(176, 196, 216), B0=(210, 222, 236),
         Y1=(120, 200, 196), Y2=(70, 150, 150), B4=(70, 88, 116), AMB=(250, 196, 90), B5=(160, 176, 196),
         P1=(230, 238, 246), P2=(196, 208, 222), M1=(170, 188, 210), M2=(110, 190, 186), M3=(60, 140, 140),
         M4=(120, 136, 160), M5=(50, 64, 90), M0=(226, 234, 244), M6=(150, 166, 190), M7=(100, 118, 146),
         AMB2=(200, 140, 60), C1=(226, 236, 246), C2=(160, 178, 200), C3=(110, 128, 156), C4=(64, 80, 108),
         C5=(200, 214, 230), C0=(140, 156, 180), C6=(180, 196, 216), Y3=(50, 120, 120), Y4=(30, 90, 96),
         C7=(190, 204, 222)),
    dict(wall=HB_wall, side=HB_side, floor=HB_floor, pillar=HB_pillar, emblem=HB_emblem, machine=HB_machine,
         misc=hof_misc))

C6 = direction6(
    "C", "THE SEASONS / THE CERTIFICATE",
    ["LEAGUE: each humour's season (8.679) -- limewashed rooms on pale flags, and over every floor the same litter",
     "that is frost in IV's colours, sun in II's, leaves in III's, blossom in I's; the ring a wheel of four spokes",
     "with the room's season risen over its horizon; the pillars urns glazed in the humour. AL CLEAR's room NO",
     "WEATHER: a sealed glasshouse, his wheel all white -- every season's colour at once is white light (7.2).",
     "HALL: the record as an official document (AL CLEAR's name is on it) -- an engraved guilloche border for walls,",
     "parchment under a fine lattice, the pillars rolled diplomas in a ribbon, the emblem a blank foil seal."],
    dict(OUT=(40, 36, 40), GRY=(130, 124, 120), SIG=(240, 236, 220), W1=(226, 218, 200), W2=(204, 194, 174),
         W3=(174, 162, 142), W4=(138, 126, 108), LMP=(255, 246, 214), LMPD=(214, 196, 150), E1=(236, 240, 242),
         E2=(200, 208, 212), E3=(160, 170, 176), E4=(120, 130, 138), E5=(180, 200, 190), E6=(120, 140, 132),
         WHT=(252, 252, 248), LG=(200, 198, 192), DG=(52, 48, 50), S1=(210, 204, 194), S2=(176, 168, 156),
         S3=(136, 128, 118), F1=(200, 194, 182), F2=(176, 170, 158), F3=(148, 142, 130),
         H1=(255, 255, 255), H2=(200, 200, 200), H3=(150, 150, 150), H4=(100, 100, 100), A1=(200, 200, 200),
         A2=(100, 100, 100),
         INK=(50, 56, 60), SL1=(120, 130, 134), FL1=(214, 216, 212), FL0=(236, 238, 234), GRY12=(168, 172, 170),
         WA1=(196, 204, 200), WA2=(160, 172, 168), FL2=(190, 192, 188), GD1=(240, 190, 70), Q1=(204, 222, 236),
         WA0=(226, 234, 230), GD0=(240, 240, 236), WA3=(120, 134, 130), BLK=(14, 12, 20),
         RN1=(226, 214, 200), RN2=(206, 190, 160), RN3=(230, 216, 190), RNO=(82, 82, 106)),
    dict(wall=C_wall, door=C_door, floor=C_floor, ring=C_ring, pillar=C_pillar, light=C_light, champion=C_champion),
    dict(OUT=(46, 40, 36), GRY=(150, 140, 126), P3=(214, 204, 180), WHT=(250, 244, 226), B1=(214, 204, 176),
         B2=(120, 140, 110), B3=(80, 96, 76), FL1=(240, 230, 204), FL2=(218, 206, 174), B0=(236, 228, 204),
         Y1=(70, 110, 150), Y2=(40, 74, 110), B4=(150, 160, 130), AMB=(250, 210, 110), B5=(226, 214, 186),
         P1=(244, 236, 214), P2=(220, 208, 178), M1=(250, 226, 140), M2=(222, 184, 80), M3=(184, 140, 50),
         M4=(140, 100, 36), M5=(100, 70, 30), M0=(244, 236, 214), M6=(200, 186, 150), M7=(170, 156, 122),
         AMB2=(200, 150, 60), C1=(248, 242, 224), C2=(224, 214, 186), C3=(190, 176, 140), C4=(120, 104, 78),
         C5=(236, 226, 200), C0=(160, 146, 116), C6=(210, 198, 168), Y3=(60, 96, 130), Y4=(30, 56, 86),
         C7=(200, 188, 156)),
    dict(wall=HC_wall, side=HC_side, floor=HC_floor, pillar=HC_pillar, emblem=HC_emblem, machine=HC_machine,
         misc=hof_misc))
STYLES6 = {"A": A6, "B": B6, "C": C6}
SCENES6 = scenes6()


# ---------------------------------------------------------------------------------------- pair 6's sheets
ROOMS_LG = [(HEARING[0][0], "IV PHLEGMATIC (met 1st)"), (HEARING[1][0], "II CHOLERIC (2nd)"),
            (HEARING[2][0], "III MELANCHOLIC (3rd)"), (HEARING[3][0], "I SANGUINE (4th)"),
            (CHAMPION, "AL CLEAR's room")]
ROOMS_HOF = [(HALL, "the HALL OF FAME"), (UNION, "the UNION ROOM (shares the set: unchanged)")]
DETAILS6 = [(HEARING[0][0], (1, 1, 12, 10), "IV: the door, the pillars, the ring"),
            (HEARING[1][0], (1, 2, 5, 10), "II's pillars"), (HEARING[2][0], (1, 2, 5, 10), "III's pillars"),
            (HEARING[3][0], (1, 4, 5, 13), "I's pillars"),
            (CHAMPION, (3, 0, 10, 4), "AL CLEAR: the door"), (CHAMPION, (3, 5, 10, 11), "AL CLEAR: the emblem"),
            (HALL, (2, 0, 9, 5), "the RECORD's machine (six lights)"), (HALL, (1, 4, 10, 9), "the emblem, pillars")]


def contact_sheets6(out_dir, states):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: Nintendo's rooms, their floors and walls retinted by gbatowns batch G (a DRAFT);",
                              "the rings, emblems, pillars, doors and the RECORD's machine as Nintendo drew them."])}
    for k in STYLES6:
        titles[k] = ("%s %s" % (k, STYLES6[k]["title"]), STYLES6[k]["lines"])
    pad = 10
    paths = []
    for which, rooms in (("league", ROOMS_LG), ("hall", ROOMS_HOF)):
        blocks = []
        for k in names:
            st = states[k]
            ims = [(room(m, (st, None) if st else None), cap) for m, cap in rooms]
            t, lines = titles[k]
            th = 8 + 12 * len(lines) + 16
            W = sum(i.width for i, _ in ims) + pad * (len(ims) + 1)
            im = Image.new("RGB", (max(W, 1100), th + max(i.height for i, _ in ims) + pad), BG)
            d = ImageDraw.Draw(im)
            text(d, (pad, 6), t.split(" / ")[0], RED)
            if " / " in t:
                text(d, (pad, 18), "/ " + t.split(" / ")[1], RED)
            for j, s in enumerate(lines):
                text(d, (pad + 250, 6 + 12 * j), s)
            x = pad
            for i, cap in ims:
                text(d, (x, th - 13), cap, SOFT)
                im.paste(i, (x, th))
                x += i.width + pad
            blocks.append(im)
        W = max(b.width for b in blocks)
        sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
        d = ImageDraw.Draw(sh)
        text(d, (pad, 8), "T-447 DRAFT, pair 6 -- %s, the real maps at 1x, three directions beside today's (redrawn in "
                          "place: no block, collision or palette row moves; 0 new tiles)" %
             ("the LEAGUE: the four hearing rooms in the order met, then AL CLEAR" if which == "league"
              else "the HALL OF FAME"), INK)
        y = 30
        for b in blocks:
            sh.paste(b, (0, y))
            y += b.height
        p = os.path.join(out_dir, "t447p6_%s_1x.png" % which)
        sh.save(p)
        paths.append(p)
    for part, idxs in ((1, (0, 1, 2, 3)), (2, (4, 5, 6, 7))):
        rowsim = []
        for k in names:
            crops = []
            for i in idxs:
                m, cr, cap = DETAILS6[i]
                im = room(m, (states[k], None) if states[k] else None, cr)
                crops.append((im.resize((im.width * 3, im.height * 3), Image.NEAREST), cap))
            rowsim.append((k, crops))
        cw = sum(c.width for c, _ in rowsim[0][1]) + pad * (len(idxs) + 1) + 130
        ch = max(c.height for c, _ in rowsim[0][1]) + 24
        det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
        d = ImageDraw.Draw(det)
        text(d, (pad, 8), "T-447 DRAFT, pair 6 -- details at 3x (%s)" %
             ("the hearing rooms" if part == 1 else "AL CLEAR's room and the HALL OF FAME"), INK)
        y = 30
        for k, crops in rowsim:
            text(d, (pad, y + 6), titles[k][0][:18], RED)
            x = 130
            for c, cap in crops:
                text(d, (x, y + 2), cap, SOFT)
                det.paste(c, (x, y + 16))
                x += c.width + pad
            y += ch
        p = os.path.join(out_dir, "t447p6_detail_3x_%d.png" % part)
        det.save(p)
        paths.append(p)
    #  the tiles at 3x, each in its home row (the hearing rooms' shared tiles shown in each room's row)
    cols = []
    for k in names:
        st = states[k]
        imgs = []
        for key, S in SETS6.items():
            tiles, pals = st[key] if st else (S.cur, {r: (TODAY6[key, r] if r >= 7 else G.PPAL[r]) for r in range(16)})
            own = set(owned6(key))
            shows = [None] + ([8, 9, 10, 11] if key == "lg" else [])
            for showrow in shows:
                pick = sorted(t for t in own if showrow is None or set(rows_of6(key, t)) & {8, 9, 10, 11})
                if showrow is not None:
                    pick = [t for t in pick if all(r in (8, 9, 10, 11) for r in rows_of6(key, t))]
                used_rows = sorted({t // 16 for t in pick})
                strip = Image.new("RGB", (128, 8 * len(used_rows)), (236, 236, 236))
                o = strip.load()
                for j, rr in enumerate(used_rows):
                    for t in range(rr * 16, rr * 16 + 16):
                        if t not in pick:
                            continue
                        rws = rows_of6(key, t)
                        hr = showrow if showrow is not None else max(rws, key=rws.get)
                        for q in range(64):
                            vv = tiles[t][q]
                            o[(t % 16) * 8 + q % 8, j * 8 + q // 8] = tuple(pals[hr][vv]) if vv else (200, 200, 200)
                lab = S.dir.split("/")[-1] + (" (home rows)" if showrow is None else " (shared, in row %d)" % showrow)
                imgs.append((lab, strip))
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
    text(d, (pad, 6), "T-447 DRAFT, pair 6 -- the tiles at 3x (grey: transparent); the hearing rooms' shared tiles "
                      "once per room's row", INK)
    x = pad
    for t, c in cols:
        text(d, (x, 26), t[:44], RED)
        sh.paste(c, (x, 42))
        x += c.width + pad
    p = os.path.join(out_dir, "t447p6_tiles_3x.png")
    sh.save(p)
    paths.append(p)
    return paths


# ---------------------------------------------------------------------------------------- pair 6's report
def report6():
    bad = 0
    picks = {k: APPROVED[k] for k in SETS6 if k in APPROVED}
    print("\n  pair 6 (the LEAGUE + the HALL OF FAME) -- DRAFT, %s" %
          ("APPROVED %s" % picks if picks else "not approved: `--pair 6 --write --approved` refuses"))
    for key, S in SETS6.items():
        own = owned6(key)
        van = [t for t in own if S.cur[t] == S.van[t] and len(set(S.van[t])) > 1]
        rows = sorted({r for t in own for r in rows_of6(key, t)})
        print("    %-16s %3d tiles drawn here, %d still Nintendo's drawing; rows placed %s, own %s" %
              (NAMES[key], len(own), len(van), rows, S.rows))
    print("    scenes: %s" % ", ".join(sc.name for sc in SCENES6))
    print("    named blocks kept by id: %s" % ", ".join("0x%03X %s" % kv for kv in sorted(NAMED6.items())))
    #  the UNION ROOM shares the HALL's set: none of its tiles and none of its rows may move
    union = {t for t in HOF.use if UNION in HOF.use[t]["maps"]}
    urows = sorted({r for t in union for r in HOF.use[t]["rows"]})
    if union & set(owned6("hof")) or set(urows) & set(HOF.rows):
        print("  !! the UNION ROOM draws a tile or row this pair redraws")
        bad = 1
    else:
        print("    the UNION ROOM: its %d tiles and rows %s are not this pair's (the front edge 45..47 kept)" %
              (len(union), urows))
    #  gbatowns must keep every tile these rooms draw
    towns = _literal(os.path.join(ROOT, "tools", "gbatowns.py"), "LANDMARKS") or {}
    boxed = {b[0] for b in towns.get("pokemon_league", [])} | {b[0] for b in towns.get("hall_of_fame", [])}
    if boxed != set(LEAGUE_MAPS) | {HALL}:
        print("  !! gbatowns.LANDMARKS does not hold the five LEAGUE rooms and the HALL (%s): its write could redraw them"
              % sorted(set(LEAGUE_MAPS) | {HALL} - boxed))
        bad = 1
    else:
        print("    gbatowns.LANDMARKS holds the five LEAGUE rooms and the HALL: its write keeps every tile they draw")
    print("    gbafieldfx: the RECORD's monitor sprite (hof_monitor) -- a sprite, not these tiles; the six lights are "
          "kept where FLDEFF_HALL_OF_FAME_RECORD sets the balls; the statues in I's corridor are primary/building's")
    known = {"gbatowns.py", "gbafieldfx.py", "port_dialogue.py", "port_hearsay.py", "check_generators.py"}
    found = set()
    me = os.path.basename(__file__)
    for f in sorted(glob.glob(os.path.join(ROOT, "tools", "*.py"))):
        if os.path.basename(f) == me:
            continue
        if re.search(r"pokemon_league|PokemonLeague|hall_of_fame|HallOfFame",
                     open(f, encoding="utf-8", errors="ignore").read()):
            found.add(os.path.basename(f))
    if found - known:
        print("  !! a tool this one does not know names these tilesets: %s -- read it before a write" %
              sorted(found - known))
        bad = 1
    for k, D in STYLES6.items():
        sets, owner = draw6(D)
        for key, S in SETS6.items():
            tiles, pals = sets[key]
            moved = [t for t in range(S.nvan) if any((a == 0) != (b == 0) for a, b in zip(tiles[t], S.cur[t]))]
            if moved:
                print("  !! %s %s: tiles %s change their footprint" % (k, key, moved[:10]))
                bad = 1
            stray = [t for t in range(S.nvan) if tiles[t] != S.cur[t] and t not in set(owned6(key))]
            if stray:
                print("  !! %s %s: tiles %s that are not this pair's changed" % (k, key, stray[:10]))
                bad = 1
            missed = sorted(set(owned6(key)) - {t for (sk, t) in owner if sk == key})
            if missed:
                print("  !! %s %s: tiles %s in no scene" % (k, key, missed[:10]))
                bad = 1
            if any(pals[r] != TODAY6[key, r] for r in range(7, 16) if r not in S.rows):
                print("  !! %s %s: a row this pair does not own changed" % (k, key))
                bad = 1
        n = {key: sum(1 for t in owned6(key) if sets[key][0][t] != SETS6[key].van[t]) for key in SETS6}
        print("    %s %-38s redrawn: pokemon_league %d of %d, hall_of_fame %d of %d; 0 new tiles" %
              (k, D["title"], n["lg"], len(owned6("lg")), n["hof"], len(owned6("hof"))))
    return bad


def check_engine6():
    bad = 0
    for bkey, pick in APPROVED.items():
        if bkey not in SETS6:
            continue
        sets, _ = draw6(STYLES6[pick], only=bkey)
        S = SETS6[bkey]
        off = [t for t in range(len(S.cur)) if sets[bkey][0][t] != S.cur[t]]
        rows = [r for r in S.rows if sets[bkey][1][r] != TODAY6[bkey, r]]
        if off or rows:
            print("  !! %s: the engine differs from `--pair 6 --write --approved` (%s) in tiles %s rows %s"
                  % (NAMES[bkey], pick, off[:12], rows))
            bad = 1
    return bad


def main6():
    picks = {k: APPROVED[k] for k in SETS6 if k in APPROVED}
    if WRITE:
        if "--approved" not in ARGS or not picks:
            print("  --write refused: T-447 pair 6 is a draft. APPROVED holds no pick for it (%s); the user picks a "
                  "direction per\n  building first, it goes into APPROVED (\"lg\": X, \"hof\": Y), then "
                  "`--pair 6 --write --approved` writes pokemon_league's\n  tiles and rows 7..12 and hall_of_fame's "
                  "tiles and rows 7, 10, 11 (never a tile or row the UNION ROOM draws)." % (picks or "empty"))
            return 1
        for bkey, pick in picks.items():
            sets, _ = draw6(STYLES6[pick], only=bkey)
            S = SETS6[bkey]
            G.save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[bkey][0], os.path.join(GBA, S.dir, "tiles.png"))
            for r in S.rows:
                write_pal(os.path.join(GBA, S.dir, "palettes", "%02d.pal" % r), sets[bkey][1][r])
            print("  written: %s, direction %s" % (NAMES[bkey], pick))
        return 0
    bad = report()
    if DRAFT is not None:
        out = DRAFT if DRAFT != DRAFT_DEFAULT else DRAFT6_DEFAULT
        os.makedirs(out, exist_ok=True)
        states = collections.OrderedDict()
        states["NOW"] = None
        summary = {}
        for k, D in STYLES6.items():
            sets, owner = draw6(D)
            for key, S in SETS6.items():
                dd = os.path.join(out, k, S.dir.split("/")[-1])
                os.makedirs(os.path.join(dd, "palettes"), exist_ok=True)
                G.save_like(os.path.join(GBA, S.dir, "tiles.png"), sets[key][0], os.path.join(dd, "tiles.png"))
                for r in S.rows:
                    write_pal(os.path.join(dd, "palettes", "%02d.pal" % r), sets[key][1][r])
            states[k] = sets
            ch = {key: sum(1 for t in owned6(key) if sets[key][0][t] != SETS6[key].van[t]) for key in SETS6}
            summary[k] = dict(title=D["title"], lines=D["lines"], tiles_redrawn=ch, new_tiles=0,
                              rows={"pokemon_league": LG.rows, "hall_of_fame": HOF.rows})
        json.dump(dict(ticket="T-447", pair=6, status="DRAFT -- not in the engine", approved=picks,
                       directions=summary), open(os.path.join(out, "directions.json"), "w"), indent=1)
        for p in contact_sheets6(out, states):
            print("  sheet:", p)
    if APPROVED:
        bad = check_engine() or bad
    return 1 if bad else 0


# ============================================================================================ PAIR 7
#  THE S.S. ANNE, alone (the largest set) -- and its departure's smoke and wake, so the liner is ours at the pier and
#  leaving it. In the story she is the liner at ARDOR's pier: the player's brother is her captain (fond of boats, still
#  seasick; DRIVER01 is his), the band leaves its sheet on the piano every voyage ("a key and no tune"), the lioness
#  checks everything that comes aboard and asks the player to post a letter in the ship's post, a painting in the
#  corridor holds words that will not hold still, and once she sails MOM gets a card with a ship's stamp on it and
#  "Come back." ends (vision 9.17, T-493..T-496, T-504). The same sailor becomes the SEAGALLOP's.
#
#  ss_anne      25 rooms on nine layouts: the deck, four corridors (1F, 2F, 3F, B1F -- the hold's), the captain's
#               office, the galley, and the two cabin layouts (7 and 11 rooms). Its primary is gTileset_General (not
#               building). Own rows 7 (everything shared: walls, floors, rails, the hull, the stairs, the galley), 8
#               (the cabins' wallpaper and carpets, the painting, the cabin portholes) and 9 (the deck's barrels);
#               rows 10 and 12 are empty and stay so, row 11 keeps its one black (tile 1, the void). Every direction
#               keeps each row's slot ROLES (1 the outline, 2..6 the neutrals, 7..9 and 10..12 two accents, 13..15
#               the boards -- rows 7, 8 and 9 share the outline, the white and the boards), so a pixel vanilla drew
#               in a role keeps it unless a motif redraws it; the motifs are drawn inside each tile's footprint.
#               Tiles drawn in general's fixed rows 1, 2, 5 (the shelf, the potted palm, the rug, tiles 35/104) are
#               kept as the engine has them; the tablecloth's checker (row 5) is re-laid in its own row's indices.
#               The door (0x281, METATILE_SSAnne_Door: tiles 28, 29, 44, 45) is gbadoors' hinged door, whose frames
#               are copied from the closed block: kept exactly. No animation (callback NULL), no run-time recolour.
#  departure    graphics/ss_anne/smoke.png (16x72, four 16x16 frames) and wake.png (16x64, two 16x32 frames), still
#               pret's drawing. src/ss_anne.c draws both in OBJ palette 10, PALSLOT_NPC_SPECIAL -- the S.S. ANNE's
#               own palette, which genships.py (T-167) made ours. They were drawn in vanilla's indices 10 and 14 (a
#               pale lavender and white in Nintendo's ship palette), which in genships' ANNE_PAL are the planking's
#               dark brown and the porthole light: TODAY THE SMOKE IS BROWN AND BLUE. The drafts draw in ANNE_PAL's
#               own indices (5 white, 6 white in shade, 7 grey, 13 the water's shadow, 14 the porthole light), so
#               nothing in genships changes. THE SMOKE'S PLACE (built 2026-11-11, the user: "the smoke moves over
#               the new funnel"): the draft read ss_anne.c's +49 as 30 px aft of genships' funnel, measuring from
#               the picture's centre -- but the 128x64 ship is drawn from subsprites at x -32/+32 (y -16/+16), so
#               her column c is at sprite x + c - 32, and vanilla's +49 is column 81, its FORE funnel's mouth.
#               genships' funnel mouth is columns 72..84, row 1 (vanilla's row 9), so the built smoke is +46 and
#               y 78 -> 66 (8 rows higher, and C's first puff sits 4 rows lower in its frame than vanilla's).
#               The draft's +8..+20 would have put it over the bow. The report checks it (smoke_at, FUNNEL_MOUTH).
#
#  The same rules as pairs 4-6: redrawn IN PLACE, every tile keeps its footprint, no block, layer, flip, palette row,
#  behaviour or collision bit moves and no map is touched; 0 new tiles. gbatowns batch G drew the deck's teak, the
#  bulkheads and the cabins' carpet by role (a DRAFT, 2026-10-28); gbatowns.LANDMARKS now holds all 25 rooms (the
#  pair-5/6 precedent), so its write keeps every tile they draw as the engine has it, and this pair redraws them.
#  No readable words anywhere: no letters, numerals or marks (the postmarks are rings and waves, the stamps pictures,
#  the band's sheet five lines and nothing on them).

DRAFT7_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t447_pair7")
SS = G.Set("ss", "gTileset_SSAnne", [7, 8, 9])
SETS7 = {"ss": SS}
G.SETS.update(SETS7)
NAMES.update({"ss": "the S.S. ANNE"})
TODAY7 = {r: [tuple(c) for c in read_pal(os.path.join(GBA, SS.dir, "palettes/%02d.pal" % r))] for r in range(16)}
GEN_SYM = "gTileset_General"
GEN_NOW = G.tileset_data(GEN_SYM)
SS_DOOR = {0x281: "METATILE_SSAnne_Door"}
KEEP7 = {28, 29, 44, 45, 1}                         # the door (gbadoors' hinged door copies it), the void's black
FIXED7_ROWS = (1, 2, 5)                             # general's rows: kept, but the tablecloth is re-laid in them
CLOTH = {115, 116, 117, 131, 132, 133, 145, 146, 147, 148}
SS_ROOMS = ["SSAnne_Deck", "SSAnne_CaptainsOffice", "SSAnne_Kitchen", "SSAnne_1F_Room1", "SSAnne_2F_Room1",
            "SSAnne_B1F_Corridor", "SSAnne_1F_Corridor", "SSAnne_2F_Corridor", "SSAnne_3F_Corridor"]
SS_MAPS = sorted(m for t in SS.use for m in SS.use[t]["maps"])
SS_MAPS = sorted(set(SS_MAPS))
ANNE_PAL = [(57, 115, 180), (16, 16, 40), (40, 56, 104), (72, 96, 152), (176, 48, 40), (248, 248, 240),
            (208, 212, 224), (152, 160, 184), (32, 40, 64), (200, 160, 104), (152, 112, 72), (232, 168, 48),
            (176, 112, 32), (40, 88, 152), (136, 200, 232), (8, 8, 16)]     # genships.ANNE_PAL (checked in report)

#  each own row's slot roles (index 1..15); 1 = darkest in every ramp
ROWS7 = {7: ["OUT", "N1", "N2", "N3", "N4", "WHT", "Y1", "Y2", "Y3", "B1", "B2", "B3", "W1", "W2", "W3"],
         8: ["OUT", "M1", "M3", "WHT", "G1", "G2", "G3", "G4", "G5", "O1", "O2", "O3", "W1", "W2", "W3"],
         9: ["OUT", "M1", "M3", "WHT", "F1", "C4", "C3", "C2", "C1", "F2", "F3", "F4", "W1", "W2", "W3"]}

R7 = lambda a, b: list(range(a, b + 1))
KIND7 = _kinds([
    ("floor", [22, 23, 24, 25]), ("floork", [6, 7, 8, 9]),
    ("deck", [160, 161, 169, 170, 185, 186, 197]), ("hull", [155, 156, 167, 171, 187, 202]),
    ("roof", [206, 226]),
    ("swall", [157, 158, 159, 172, 173, 174, 188, 189, 190, 204, 205, 207, 208, 209, 211, 212, 224, 225, 227, 228,
               240, 241, 242, 243, 244]),
    ("sport", [175, 176, 191]),
    ("wall", [2, 18, 19, 36]), ("edge", [3, 4, 5, 12, 15, 20, 21, 31, 37, 47, 70]),
    ("paper1", [16, 32]), ("paper2", [17, 33]), ("port", [10, 26, 92, 93, 108, 109]),
    ("carpet1", [40, 41]), ("carpet2", [42, 43]), ("painting", R7(84, 87) + R7(100, 103)),
    ("bed", R7(80, 83) + R7(96, 99)), ("book", [124, 125, 140, 141]),
    ("barrel", [213, 214, 215, 216, 218, 219, 229, 230, 231, 232]),
    ("counter", [118, 119, 120, 121, 134, 135, 136, 137, 150, 151]), ("plate", [152, 153, 154]), ("stove", [149]),
    ("pillar", [14, 30, 46]), ("cloth", sorted(CLOTH)),
])


def owned7():
    return sorted(t for t in SS.use if t < SS.nvan and any(SS.van[t]) and t not in KEEP7
                  and all(r >= 7 for r in SS.use[t]["rows"]) or (t in CLOTH and t in SS.use))


def rows_of7(t):
    return dict(SS.use[t]["rows"]) if t in SS.use and SS.use[t]["rows"] else {7: 1}


GEN_VPAL = [G.jasc(daemonslib.upstream(GBA, "data/tilesets/primary/general/palettes/%02d.pal" % r, binary=True))
            for r in range(7)]


class Scene7:
    """a room as one picture: per layer, each pixel's tile kind and vanilla (row, index)"""

    def __init__(self, name, blocks):
        self.name, self.blocks = name, blocks
        self.setkey = "ss"
        self.layers = [region6(SS, blocks, layer) for layer in (0, 1)]
        self.th = len(self.layers[0][0])
        self.tw = max(len(r) for r in self.layers[0][0])
        self.w, self.h = self.tw * 8, self.th * 8
        mk = lambda: [[None] * self.w for _ in range(self.h)]
        self.kindL, self.roleL, self.idxL, self.tileL = [mk(), mk()], [mk(), mk()], [mk(), mk()], [mk(), mk()]
        self.ukind = mk()
        self.L = 0
        for layer in (0, 1):
            lay, rg = self.layers[layer]
            for ty, r in enumerate(lay):
                for tx, spec in enumerate(r):
                    if spec is None:
                        continue
                    t, fl = spec
                    row = rg[ty][tx]
                    for k in range(64):
                        x, y = k % 8, k // 8
                        sx = 7 - x if "h" in fl else x
                        sy = 7 - y if "v" in fl else y
                        vv = SS.van[t][sy * 8 + sx]
                        if vv == 0:
                            continue
                        X, Y = tx * 8 + x, ty * 8 + y
                        self.kindL[layer][Y][X] = self.ukind[Y][X] = KIND7.get(t, "misc")
                        self.roleL[layer][Y][X] = ROWS7[row][vv - 1] if row in ROWS7 else None
                        self.idxL[layer][Y][X] = vv
                        self.tileL[layer][Y][X] = t
        self.comps = {}

    @property
    def kind(self):
        return self.kindL[self.L]

    @property
    def role(self):
        return self.roleL[self.L]

    def comp(self, kind, minsize=12):
        if kind in self.comps:
            return self.comps[kind]
        seen, out = set(), []
        for y in range(self.h):
            for x in range(self.w):
                if self.ukind[y][x] != kind or (x, y) in seen:
                    continue
                st, pts = [(x, y)], []
                seen.add((x, y))
                while st:
                    a, b = st.pop()
                    pts.append((a, b))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        u, w2 = a + dx, b + dy
                        if 0 <= u < self.w and 0 <= w2 < self.h and (u, w2) not in seen and self.ukind[w2][u] == kind:
                            seen.add((u, w2))
                            st.append((u, w2))
                xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                out.append((min(xs), min(ys), max(xs), max(ys), len(pts)))
        self.comps[kind] = [c for c in out if c[4] >= minsize]
        return self.comps[kind]

    def box(self, kind, x, y):
        for c in self.comp(kind):
            if c[0] <= x <= c[2] and c[1] <= y <= c[3]:
                return c
        return None

    def shade(self, x, y):
        """vanilla laid this board in shadow: its 3x3 is mostly the darkest board"""
        n = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                u, w2 = x + dx, y + dy
                if 0 <= u < self.w and 0 <= w2 < self.h and self.role[w2][u] == "W1":
                    n += 1
        return n >= 6


def scenes7():
    return [Scene7(m, map_blocks(m)) for m in SS_ROOMS]


SCENES7 = scenes7()


def pals7(D):
    out = {}
    for r in range(16):
        if r in SS.rows:
            out[r] = [TODAY7[r][0]] + [tuple(D["mat"][n]) for n in ROWS7[r]]
        else:
            out[r] = list(TODAY7[r])
    for r in range(7):
        out[r] = [tuple(c) for c in GEN_NOW["pals"][r]]
    return out


def resolve7(mats, base, rows, D, pals):
    """materials -> indices: a name its rows hold at one index takes it, anything else the nearest colour; ("i", n)
    is an index in a fixed row; None keeps the engine's pixel"""
    px, cache = [], {}
    for k, m in enumerate(mats):
        if base[k] == 0:
            px.append(0)
            continue
        if m is None:
            px.append(None)
            continue
        if isinstance(m, tuple):
            px.append(m[1])
            continue
        if m not in cache:
            idx = {ROWS7[r].index(m) + 1 for r in rows if r in ROWS7 and m in ROWS7[r]}
            if len(idx) == 1 and all(r in ROWS7 and m in ROWS7[r] for r in rows):
                cache[m] = idx.pop()
            else:
                col = tuple(D["mat"][m])
                best, bd = 1, 1e18
                for i in range(1, 16):
                    d = sum(wgt * sum((a - b) ** 2 for a, b in zip(pals[r][i], col)) for r, wgt in rows.items())
                    if d < bd:
                        best, bd = i, d
                cache[m] = best
        px.append(cache[m])
    return px


def draw7(D):
    """-> (tiles, palettes), owner {t: scene}"""
    pals = pals7(D)
    tiles = [t[:] for t in SS.cur]
    owner = {}
    own = set(owned7())
    for sc in SCENES7:
        for layer in (0, 1):
            lay, rg = sc.layers[layer]
            if not any(s for r in lay for s in r):
                continue
            K = Cv(lay, "ss")
            sc.L = layer
            f = D["paint"]
            K.fn(lambda x, y: f(sc, x, y))
            for t, mats in K.tiles().items():
                if t in owner or t not in own:
                    continue
                if t in CLOTH:
                    new = [m[1] if isinstance(m, tuple) else c for m, c in zip(mats, SS.cur[t])]
                else:
                    new = resolve7(mats, SS.van[t], rows_of7(t), D, pals)
                    new = [c if n is None else n for n, c in zip(new, SS.cur[t])]
                tiles[t] = new
                owner[t] = sc.name
    return (tiles, pals), owner


# ---------------------------------------------------------------------------------------- shared painting
def p7(style):
    """the painter: a motif per kind, else the pixel keeps its vanilla role (that role's new colour)"""
    def paint(sc, x, y):
        kind = sc.kind[y][x]
        if kind is None:
            return None
        role = sc.role[y][x]
        if kind == "cloth":
            return style["cloth"](sc, x, y, sc.idxL[sc.L][y][x])
        if role is None:
            return None
        f = style.get(kind)
        m = f(sc, x, y, role) if f else None
        if m == "WALL":                                     # a porthole's corner: the wall it is set in
            m = None
            for dx in (8, -8, 16, -16):
                if 0 <= x + dx < sc.w:
                    k2 = sc.kind[y][x + dx]
                    if k2 in ("wall", "paper1", "paper2", "swall"):
                        m = style[k2](sc, x, y, role)
                        break
        return role if m is None else m
    return paint


def wave(x, y, period=8, amp=1.0, ph=0.0):
    return math.sin((x + ph) * 2 * math.pi / period) * amp


def ring_d(sc, kind, x, y):
    """(distance from the component's centre / its radius, dx, dy) or None"""
    c = sc.box(kind, x, y)
    if not c:
        return None
    cx, cy = (c[0] + c[2] + 1) / 2.0, (c[1] + c[3] + 1) / 2.0
    r = max(2.0, min(c[2] - c[0] + 1, c[3] - c[1] + 1) / 2.0 - 1.5)
    return math.hypot(x + 0.5 - cx, y + 0.5 - cy) / r, x + 0.5 - cx, y + 0.5 - cy


def rel(sc, kind, x, y):
    """(u, v, w, h) inside the component's box"""
    c = sc.box(kind, x, y)
    if not c:
        return None
    return x - c[0], y - c[1], c[2] - c[0] + 1, c[3] - c[1] + 1


def is_stripe(role):
    return role in ("Y1", "Y2", "Y3", "B1", "B2", "B3")


def board(sc, x, y, role, along, plank=4, run=24, seam="OUT", s=0, dotted=False):
    """planks running ALONG ("x" or "y"), PLANK px wide, butt joints every RUN px staggered by plank"""
    if role == "OUT":
        return "OUT"
    a, b = (x, y) if along == "x" else (y, x)
    lane = b // plank
    off = (lane * run // 2) % run                           # tiles repeat: every pattern divides the tile grid
    lit = sc.shade(x, y)
    if b % plank == plank - 1:
        if dotted and a % 2:
            return "W1" if lit else "W2"
        return "W1"
    if (a + off) % run == 0:
        return "W1"
    g = H(a % run // 3, lane % 4, s) % 7
    if lit:
        return "W1" if g == 0 else "W2"
    return "W3" if g < 4 else "W2"


# ================================================================== A: THE PACKET (the ship's post)
#  The lioness posts a letter in the ship's post; MOM gets a card with a ship's stamp. A packet boat is the mail ship,
#  and a packet is what a network carries: header, payload, a route. The liner as the mail packet: envelope-paper
#  bulkheads with the airmail border where the rail stripe was, kraft boards with perforated seams, cabins carpeted in
#  stamps and in envelope backs, portholes as postmarks, mail sacks on the deck, the galley's tables sorting frames.
def A7_floor(sc, x, y, role):
    return board(sc, x, y, role, "x", plank=4, run=16, dotted=True)


def A7_floork(sc, x, y, role):
    return board(sc, x, y, role, "y", plank=4, run=8, s=1, dotted=True)


def A7_deck(sc, x, y, role):
    if role in ("OUT", "N1", "N2", "N3", "N4", "WHT", "B1", "B2", "B3"):
        return None
    return board(sc, x, y, role, "x", plank=4, run=8, s=2, dotted=True)


def airmail(x, y, light=False):
    """the airmail border: red and blue bars on the slant with paper between"""
    k = (x + y) % 8
    if k < 3:
        return "Y2"
    if k in (3, 7):
        return "WHT"
    return "B2"


def A7_wall(sc, x, y, role):
    if is_stripe(role):
        return airmail(x, y)
    if role == "WHT" and x % 8 == 0:
        return "N4"                                          # laid paper: its chain lines
    if role in ("N2", "N3") and y % 8 == 4 and x % 2 == 0:
        return "N1"                                          # a perforated rule along the deckhead
    return None


def A7_hull(sc, x, y, role):
    if role in ("N1", "N2", "N3", "N4"):
        return "N2" if y % 8 == 7 else "N3"                  # white plating in strakes
    return None


def A7_swall(sc, x, y, role):
    return A7_wall(sc, x, y, role)


def A7_roof(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return "B1" if (x + y) % 8 == 0 else "B2"
    return None


def postmark(sc, kind, x, y, role):
    r = ring_d(sc, kind, x, y)
    if r is None:
        return None
    d, dx, dy = r
    if role == "OUT" and d > 0.8:
        return "OUT"
    if 0.62 < d < 0.86:
        return "N1"
    if d <= 0.62:
        if abs(dy - wave(dx, 0, 6, 1.2)) < 0.6 or abs(dy - 3 - wave(dx, 0, 6, 1.2)) < 0.6:
            return "N1"                                   # the cancellation's waves
        return "B3" if dy < 0 else "N4"
    return "N4" if d < 1.0 else "WALL"


def A7_port(sc, x, y, role):
    return postmark(sc, "port", x, y, role)


def A7_sport(sc, x, y, role):
    return postmark(sc, "sport", x, y, role)


def stamps(x, y, fill, ink, edge, paper):
    """a field of stamps, one to a tile: a perforated paper edge, a picture of one wave under a sun"""
    u, v = x % 8, y % 8
    if u == 7 or v == 7:
        return edge if (u + v) % 2 else paper               # the perforation
    if u == 0 or v == 0:
        return paper
    if (u, v) == (4, 2):
        return paper                                        # the sun
    if v >= 5 - (u % 2 == 0 and v == 4):
        return ink                                          # the sea, one wave
    return fill


def A7_carpet1(sc, x, y, role):
    return stamps(x, y, "G4", "G2", "G3", "G5")


def envelopes(x, y):
    """envelope backs, one to a tile: the flap's V, lit above it"""
    u, v = x % 8, y % 8
    if v == 7:
        return "O1"
    f = abs(u - 3.5)
    if abs(f - (3.5 - v)) < 0.6:
        return "O1"
    return "O3" if f > 3.5 - v else "O2"


def A7_carpet2(sc, x, y, role):
    return envelopes(x, y)


def A7_paper1(sc, x, y, role):
    if role == "OUT":
        return None
    return "N4" if (y % 4 == 3) else "WHT"                  # ruled writing paper


def A7_paper2(sc, x, y, role):
    if role == "OUT":
        return None
    return "G4" if abs((x % 8) - 3.5) + abs((y % 8) - 3.5) in (3.0, 4.0) else "G5"   # an envelope's lining


def A7_painting(sc, x, y, role):
    rr = rel(sc, "painting", x, y)
    if rr is None:
        return None
    u, v, w, h = rr
    if u < 2 or v < 2 or u >= w - 2 or v >= h - 2:
        return None                                         # the frame
    #  a postcard: a sea, a horizon, a liner's smoke; a stamp in the corner
    if u >= w - 9 and v <= 7:
        if u in (w - 9, w - 3) or v in (2, 7):
            return "WHT" if (u + v) % 2 else "M3"
        return "G2" if v > 4 else "O2"
    if v < h * 0.45:
        return "WHT" if (u * 3 + v * 7) % 23 == 0 else "M3"
    if v < h * 0.45 + 1:
        return "M1"
    return "G2" if (u + 2 * v) % 6 else "G3"


def A7_book(sc, x, y, role):
    if role in ("WHT", "N4"):
        return "N3" if y % 3 == 0 and x % 8 not in (0, 7) else "WHT"    # a log's ruled lines, nothing on them
    return None


def A7_barrel(sc, x, y, role):
    u, v = x % 16, y % 16
    if role == "OUT":
        return None
    if v < 4:
        return "C3" if u % 3 else "C1"                      # the neck, gathered
    if v == 4:
        return "F2"                                         # the drawstring
    if 7 <= v <= 9 and 3 <= u <= 6:
        return "F1"                                         # a red tag
    g = (u * 2 + H(u, v) % 3) % 8
    return "C4" if g < 2 else "C3" if g < 6 else "C2"


def A7_counter(sc, x, y, role):
    if role in ("N3", "N4", "WHT", "N2"):
        u, v = x % 8, y % 8
        if u in (0, 7) or v == 7:
            return "N1"
        return "N2" if v < 3 else "N4"                      # pigeonholes: dark at the back, a letter's edge
    return None


def A7_plate(sc, x, y, role):
    if role == "OUT":
        return None
    u, v = x % 16, y % 8
    if v in (1, 6) or u % 16 in (2, 13):
        return "N3"
    if v == 3 or u == 8:
        return "Y2"                                         # a bundle tied with red string
    return "WHT"


CLOTH_LIGHT, CLOTH_DARK = 6, 8                       # the checker's two indices in general's row 5


def cloth(i, dark):
    if i not in (CLOTH_LIGHT, CLOTH_DARK):
        return None
    return ("i", CLOTH_DARK if dark else CLOTH_LIGHT)


def A7_cloth(sc, x, y, i):
    return cloth(i, abs(x % 8 - 3.5) + abs(y % 8 - 3.5) in (3.0, 4.0))     # a lattice of envelopes' diamonds


def A7_pillar(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return airmail(x, y)
    return None


def A7_edge(sc, x, y, role):
    return airmail(x, y) if is_stripe(role) else None


def B7_edge(sc, x, y, role):
    return staff(sc, x, y, role) if is_stripe(role) else None


def C7_edge(sc, x, y, role):
    return livery(x, y, role) if is_stripe(role) else None


def A7_misc(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return airmail(x, y) if role != "B1" else "B1"       # rails, stair rails, bins: the airmail bars
    if role in ("W1", "W2", "W3"):
        return {"W1": "W1", "W2": "W3", "W3": "W2"}[role] if (x + y) % 2 else role   # kraft, grained
    return None


def bed_cover(sc, x, y, role, f):
    rr = rel(sc, "bed", x, y)
    if rr is None or role not in ("WHT", "N4", "N3"):
        return None
    u, v, w, h = rr
    if v < h * 0.38:
        return None                                          # the pillow
    return f(u, v - int(h * 0.38), role)


def A7_bed(sc, x, y, role):
    return bed_cover(sc, x, y, role, lambda u, v, r: airmail(u, v) if v < 2 else
                     "N4" if abs(abs(u % 8 - 3.5) - (v % 8 - 2)) < 0.6 else "WHT")   # an envelope for a coverlet


def B7_misc(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return "Y2" if (x + y) % 6 == 0 else "B2" if role != "B1" else "B1"   # ebony, a brass glint
    if role in ("Y1", "Y2", "Y3"):
        return {"Y1": "B1", "Y2": "B2", "Y3": "B3"}[role]    # the seats lacquered black
    return None


def B7_bed(sc, x, y, role):
    return bed_cover(sc, x, y, role, lambda u, v, r: "N3" if u % 4 == 3 else "WHT")   # a coverlet ruled like keys


def C7_misc(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return {"B1": "W1", "B2": "W2", "B3": "W3"}[role]    # teak rails and caps
    if role in ("Y1", "Y2", "Y3"):
        return {"Y1": "B1", "Y2": "B2", "Y3": "B2"}[role]    # navy upholstery
    return None


def C7_bed(sc, x, y, role):
    return bed_cover(sc, x, y, role, lambda u, v, r: "B2" if v in (2, 3) else "N4" if v % 4 == 0 else "WHT")


STYLE7_A = dict(misc=A7_misc, edge=A7_edge, floor=A7_floor, floork=A7_floork, deck=A7_deck, wall=A7_wall, hull=A7_hull, swall=A7_swall,
                roof=A7_roof, port=A7_port, sport=A7_sport, carpet1=A7_carpet1, carpet2=A7_carpet2,
                paper1=A7_paper1, paper2=A7_paper2, painting=A7_painting, bed=A7_bed, book=A7_book,
                barrel=A7_barrel, counter=A7_counter, plate=A7_plate, cloth=A7_cloth, pillar=A7_pillar)


# ================================================================== B: THE KEY, NO TUNE (the band)
#  The band leaves its sheet on the piano every voyage: a key and no tune, and the tune is somewhere in ARDOR (the
#  singing fir, THE NEXUS). A ship's band keeps time the way a clock does with no program loaded. The liner as the
#  band's room: ivory panels with a five-line staff where the stripe was (nothing written on it, a brass bar line now
#  and then), ebony rails, a herringbone floor, one cabin carpeted in keyboards and one in sound's rings on red
#  velvet, portholes as brass cymbals, the deck's barrels drums, the galley's plates brass bowls.
def B7_floor(sc, x, y, role):
    """a basketweave parquet: each tile's three slats turned across its neighbour's"""
    if role == "OUT":
        return "OUT"
    across = (x // 8 + y // 8) % 2
    a = (y if across else x) % 8
    lit = sc.shade(x, y)
    if a in (2, 5) or (across and x % 8 == 7) or (not across and y % 8 == 7):
        return "W1"
    if lit:
        return "W2" if a == 0 else "W1"
    return "W3" if a in (0, 3, 6) else "W2"


def B7_floork(sc, x, y, role):
    return B7_floor(sc, y, x, role)


def B7_deck(sc, x, y, role):
    if role in ("OUT", "N1", "N2", "N3", "N4", "WHT", "B1", "B2", "B3"):
        return None
    if y % 4 == 3:
        return "W1"
    if x % 8 == (0 if (y // 4) % 2 else 4) and y % 4 == 1:
        return "B2"                                         # an ebony peg at each butt, like a black key
    return "W3" if (y // 4) % 2 else "W2"


def staff(sc, x, y, role):
    """five lines, no notes"""
    return "B1" if y % 2 == 0 else "WHT"


def B7_wall(sc, x, y, role):
    if is_stripe(role):
        return staff(sc, x, y, role)
    if role in ("WHT", "N4"):
        return "N3" if x % 8 == 0 else "N4" if x % 8 in (5, 6) else "WHT"     # fluted ivory
    if role in ("N2", "N3") and y % 8 == 4:
        return "Y2"                                          # a brass picture rail
    return None


def B7_swall(sc, x, y, role):
    return B7_wall(sc, x, y, role)


def B7_hull(sc, x, y, role):
    if role in ("N1", "N2", "N3", "N4"):
        return "N2" if y % 8 == 7 else "N3"
    return None


def B7_roof(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return "B3" if (x + y) % 8 == 0 else "B2"           # lacquer, a glint on the slant
    return None


def cymbal(sc, kind, x, y, role):
    r = ring_d(sc, kind, x, y)
    if r is None:
        return None
    d, dx, dy = r
    if role == "OUT" and d > 0.8:
        return "OUT"
    if d < 0.2:
        return "Y1"
    if d < 1.0:
        k = int(d * 6)
        return ["Y3", "Y2", "Y3", "Y2", "Y1", "Y2"][min(5, k)] if not (dx < -1 and dy < -1 and d < 0.7) else "WHT"
    return "WALL"


def B7_port(sc, x, y, role):
    return cymbal(sc, "port", x, y, role)


def B7_sport(sc, x, y, role):
    return cymbal(sc, "sport", x, y, role)


def keys(x, y, white, black, line, gap):
    """a keyboard to every tile row: two white keys a tile, a black key over the gap between them"""
    u, v = x % 8, y % 8
    if v == 7:
        return gap
    if 2 <= u <= 4 and v < 4:
        return black
    if u in (3, 7):
        return line
    return white


def B7_carpet1(sc, x, y, role):
    return keys(x, y, "G5", "G1", "G3", "G2")


def rings(x, y, a, b, c):
    u, v = x % 8 - 3.5, y % 8 - 3.5
    d = math.hypot(u, v)
    return c if 2.2 < d < 3.2 else b if d < 1.0 else a


def B7_carpet2(sc, x, y, role):
    return rings(x, y, "O2", "O1", "O3")


def B7_paper1(sc, x, y, role):
    if role == "OUT":
        return None
    return "N3" if x % 8 == 0 else "WHT" if x % 8 < 5 else "N4"     # fluted ivory panels


def B7_paper2(sc, x, y, role):
    if role == "OUT":
        return None
    return "G3" if y % 4 == 0 else "G4"                     # the staff again, faint, in the cabin's paper


def B7_painting(sc, x, y, role):
    rr = rel(sc, "painting", x, y)
    if rr is None:
        return None
    u, v, w, h = rr
    if u < 2 or v < 2 or u >= w - 2 or v >= h - 2:
        return None
    #  the sea drawn as a staff: five long swells and nothing on them, a pale sky
    if v < h * 0.45:
        return "WHT" if v < h * 0.25 else "M3"
    return "G1" if int(v - h * 0.45) % 2 == 0 else "G4"     # the swells ruled like a staff, nothing on it


def B7_book(sc, x, y, role):
    if role in ("WHT", "N4"):
        return "B1" if y % 2 == 0 and 1 <= x % 8 <= 6 and (y // 2) % 4 < 3 else "WHT"   # staves, empty
    return None


def B7_barrel(sc, x, y, role):
    u, v = x % 16, y % 16
    if role == "OUT":
        return None
    if v < 4:
        return "C4" if v < 3 else "C3"                       # the head
    if v in (4, 14):
        return "F2"                                          # the hoops, brass
    if abs(((u + v * 0) % 6) - (v - 5) % 6) < 1:
        return "C3"                                          # the rope's zigzag
    return "C2" if u > 2 else "C1"


def B7_counter(sc, x, y, role):
    if role in ("N3", "N4", "WHT", "N2"):
        return "B3" if y % 8 else "B2"                       # black lacquer, like a piano lid
    return None


def B7_plate(sc, x, y, role):
    if role == "OUT":
        return None
    u, v = x % 16 - 7.5, (y % 8 - 3.5) * 2
    d = math.hypot(u, v)
    return "Y3" if d < 2 else "Y2" if int(d) % 3 else "Y1"


def B7_cloth(sc, x, y, i):
    return cloth(i, x % 4 == 3)                              # pinstripes, like the keys' edges


def B7_pillar(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return "B2" if x % 4 else "Y2"                       # ebony with brass flutes
    return None


STYLE7_B = dict(misc=B7_misc, edge=B7_edge, floor=B7_floor, floork=B7_floork, deck=B7_deck, wall=B7_wall, hull=B7_hull, swall=B7_swall,
                roof=B7_roof, port=B7_port, sport=B7_sport, carpet1=B7_carpet1, carpet2=B7_carpet2,
                paper1=B7_paper1, paper2=B7_paper2, painting=B7_painting, bed=B7_bed, book=B7_book,
                barrel=B7_barrel, counter=B7_counter, plate=B7_plate, cloth=B7_cloth, pillar=B7_pillar)


# ================================================================== C: THE LIVERY (the outside carried in)
#  The captain has loved boats since before the player could walk, and keeps her the way a man who loves boats does.
#  The liner at the pier is already ours (genships, T-167): navy hull, white superstructure, one amber funnel, a red
#  boot-top, light in the portholes. Inside she is the same ship: white enamel bulkheads, riveted, a navy band with an
#  amber pinstripe where the stripe was; teak paid with black caulking; brass portholes with four dogs and light in
#  the glass; one cabin navy with amber compass roses, one red with a rope weave; teak casks with brass hoops; a
#  stainless galley; and on the captain's wall a painting of the ship herself.
def C7_floor(sc, x, y, role):
    return board(sc, x, y, role, "x", plank=4, run=16, seam="OUT")


def C7_floork(sc, x, y, role):
    return board(sc, x, y, role, "y", plank=4, run=8, s=1)


def C7_deck(sc, x, y, role):
    if role in ("OUT", "N1", "N2", "N3", "N4", "WHT", "B1", "B2", "B3"):
        return None
    if y % 4 == 3:
        return "OUT" if x % 4 else "W1"                      # black caulking, paid
    return board(sc, x, y, role, "x", plank=4, run=8, s=2)


def livery(x, y, role):
    """a navy band with an amber pinstripe"""
    if role in ("Y1", "Y2", "Y3"):
        return "Y2"
    return "B2" if role != "B3" else "B3"


def C7_wall(sc, x, y, role):
    if is_stripe(role):
        return livery(x, y, role)
    if role in ("N3", "N4", "WHT") and x % 8 == 3 and y % 8 == 3:
        return "N2"                                          # a rivet
    if role in ("N3", "N4", "WHT") and x % 8 == 3 and y % 8 == 4:
        return "WHT"                                         # its glint
    if role in ("N2", "N3") and y % 8 == 6:
        return "B2"                                          # a navy rule under the deckhead
    return None


def C7_swall(sc, x, y, role):
    return C7_wall(sc, x, y, role)


def C7_hull(sc, x, y, role):
    if role in ("N1", "N2", "N3", "N4"):
        return "B1" if y % 8 == 7 else "B2"                  # the navy hull, in strakes
    return None


def C7_roof(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return "N3" if x % 8 == 7 or y % 8 == 7 else "N4"    # white deckhead in panels
    return None


def brass_port(sc, kind, x, y, role):
    r = ring_d(sc, kind, x, y)
    if r is None:
        return None
    d, dx, dy = r
    if d > 1.0:
        return "WALL"
    if role == "OUT" and d > 0.8:
        return "OUT"
    if d >= 0.62:
        a = math.atan2(dy, dx)
        dog = min(abs(((a - math.pi / 4) % (math.pi / 2)) - math.pi / 4), 9) < 0.25 and d > 0.85
        return "Y1" if dog else "Y2" if dy < 0 else "Y1"
    if dx < 0 and dy < 0 and abs(dx + dy + 2) < 0.8:
        return "WHT"
    return "B3"


def C7_port(sc, x, y, role):
    return brass_port(sc, "port", x, y, role)


def C7_sport(sc, x, y, role):
    return brass_port(sc, "sport", x, y, role)


def C7_carpet1(sc, x, y, role):
    u, v = x % 8, y % 8
    if (u == 3 and 1 <= v <= 5) or (v == 3 and 1 <= u <= 5):
        return "G5"                                          # a small compass star in every tile
    return "G2" if v == 7 or u == 7 else "G3"


def C7_carpet2(sc, x, y, role):
    k = (x + y) % 4 if (y // 4) % 2 else (x - y) % 4
    return "O3" if k == 0 else "O1" if k == 2 else "O2"      # a rope weave


def C7_paper1(sc, x, y, role):
    if role == "OUT":
        return None
    return "N3" if x % 8 == 7 else "WHT"                     # enamel panels


def C7_paper2(sc, x, y, role):
    if role == "OUT":
        return None
    return "G3" if y % 4 < 2 else "G2"                       # navy and a lighter navy, ticking


def C7_painting(sc, x, y, role):
    rr = rel(sc, "painting", x, y)
    if rr is None:
        return None
    u, v, w, h = rr
    if u < 2 or v < 2 or u >= w - 2 or v >= h - 2:
        return None
    #  the ship herself: sky, sea, a navy hull, a white house, one amber funnel
    cx = w // 2
    if h * 0.55 <= v <= h * 0.7 and w * 0.2 <= u <= w * 0.82 + (v - h * 0.55):
        return "G1"
    if h * 0.42 <= v < h * 0.55 and w * 0.32 <= u <= w * 0.72:
        return "WHT"
    if h * 0.25 <= v < h * 0.42 and cx - 1 <= u <= cx + 2:
        return "O2"
    if v > h * 0.62:
        return "G3" if (u + v) % 5 else "G4"
    return "M3"


def C7_book(sc, x, y, role):
    if role in ("WHT", "N4"):
        return "N3" if y % 3 == 0 and x % 8 not in (0, 7) else "WHT"
    return None


def C7_barrel(sc, x, y, role):
    u, v = x % 16, y % 16
    if role == "OUT":
        return None
    if v in (4, 12):
        return "F2"
    if v < 4:
        return "C4" if (u + v) % 4 else "C3"
    return "C3" if u % 4 else "C2"


def C7_counter(sc, x, y, role):
    if role in ("N3", "N4", "WHT", "N2"):
        return "N4" if (x + y) % 7 else "WHT"                # stainless, brushed
    return None


def C7_plate(sc, x, y, role):
    if role == "OUT":
        return None
    u, v = x % 16 - 7.5, (y % 8 - 3.5) * 2
    d = math.hypot(u, v)
    return "B2" if 4.5 < d < 6 else "WHT"                    # white with a navy rim


def C7_cloth(sc, x, y, i):
    return cloth(i, x % 4 == 0 or y % 4 == 0)                # a sailcloth check


def C7_pillar(sc, x, y, role):
    if role in ("B1", "B2", "B3"):
        return {"B1": "B1", "B2": "B2", "B3": "B3"}[role]
    return None


STYLE7_C = dict(misc=C7_misc, edge=C7_edge, floor=C7_floor, floork=C7_floork, deck=C7_deck, wall=C7_wall, hull=C7_hull, swall=C7_swall,
                roof=C7_roof, port=C7_port, sport=C7_sport, carpet1=C7_carpet1, carpet2=C7_carpet2,
                paper1=C7_paper1, paper2=C7_paper2, painting=C7_painting, bed=C7_bed, book=C7_book,
                barrel=C7_barrel, counter=C7_counter, plate=C7_plate, cloth=C7_cloth, pillar=C7_pillar)


#  C_GROW (the user, 2026-11-11: "C The livery", extended to the tiles its draft only recoloured -- the pair-5 B_GROW
#  precedent). The draft left 69 of its 206 tiles in Nintendo's drawing, recoloured: the rooms' white edges, the
#  galley's posts, the stairs, the deck's iron rail, the vents and deck chairs, the captain's chair, the bins, the
#  stools, the bunks and the stove. Each is carried into the livery in the same slots and only in row 7's ramps
#  (enamel N, brass Y, navy B, teak W): riveted enamel with a navy rule, stainless posts with brass collars, teak
#  treads with brass nosing, white stanchions with a brass cap on every baluster, brass ventilator cowls, navy-and-
#  white striped canvas, navy leather, navy bins with a brass rim, brass-footed stools, teak bunks, a stainless stove.
#  Left as they are: the tablecloth (145..148, general's fixed row 5) and the painting's frame corner (87), which
#  already match the rest of their pieces.
C_EDGE = {3, 4, 5, 12, 15, 20, 21, 31, 37, 47, 70, 208, 210, 242}
C_POST = {14, 30, 46}
C_STAIR = {49, 53, 54, 66, 57, 58, 59, 60, 61, 73, 74, 76, 77}
C_RAIL = {52, 179, 180, 193, 194, 195, 196, 198, 199, 200, 201, 217, 222, 224}
C_VENT = {91, 107}
C_DCHAIR = {126, 127, 142, 143}
C_CHAIR = {112, 128, 144}
C_BIN = {62, 78}
C_STOOL = {233, 234}
C_BED = {80, 81, 82, 96, 98}
C_GALLEY = {137, 149}
C_BARE = C_EDGE | C_POST | C_STAIR | C_RAIL | C_VENT | C_DCHAIR | C_CHAIR | C_BIN | C_STOOL | C_BED | C_GALLEY


def C_grow(sc, x, y, role, t):
    rr = lambda u, v: sc.role[v][u] if 0 <= u < sc.w and 0 <= v < sc.h else None
    if t in C_EDGE:
        if role in ("N1", "N2"):
            return "B2"                                      # a navy rule round the room
        if role in ("N3", "N4", "WHT") and x % 8 == 3 and y % 8 == 3:
            return "N2"                                      # a rivet
        return None
    if t in C_POST:
        if y % 16 in (2, 3, 12):
            return {"B1": "Y1", "B2": "Y1", "B3": "Y2"}.get(role)   # a brass collar
        return {"B1": "N2", "B2": "N3", "B3": "N4"}.get(role)       # stainless
    if t in C_STAIR:
        return {"N1": "W1", "N2": "W2", "N3": "W3", "N4": "Y2", "WHT": "Y3"}.get(role)   # teak, brass nosing
    if t in C_RAIL:
        if role == "OUT" and rr(x, y - 1) not in ("OUT", None) and rr(x, y + 1) == "OUT":
            return "Y2"                                      # a brass cap on the baluster
        if role == "WHT" and y % 8 == 1 and "OUT" in (rr(x - 1, y), rr(x + 1, y)):
            return "Y2"                                      # a brass ring round a white stanchion
        return {"N1": "N2", "N2": "N3", "N3": "WHT", "N4": "WHT"}.get(role)   # the stanchions white enamel
    if t in C_VENT:
        return {"WHT": "Y3", "N4": "Y3", "N3": "Y2", "N2": "Y1", "N1": "Y1"}.get(role)   # a brass ventilator cowl
    if t in C_DCHAIR:
        if role in ("WHT", "N3", "N4"):
            return "B2" if (x // 2) % 2 else "WHT"           # striped canvas
        return {"N1": "B1", "N2": "B1"}.get(role)
    if t in C_CHAIR:
        return {"N1": "B1", "N2": "B2", "N3": "B2"}.get(role)   # navy leather
    if t in C_BIN:
        return {"N1": "B1", "N2": "B2", "N3": "B2", "N4": "Y2"}.get(role)   # navy, a brass rim
    if t in C_STOOL:
        return {"N1": "Y1"}.get(role)                        # brass feet under teak seats
    if t in C_BED:
        return {"N1": "W1", "N2": "W2"}.get(role)            # a teak bunk
    if t in C_GALLEY:
        if role in ("N2", "N3", "N4", "WHT"):
            return "N4" if (x + y) % 7 else "WHT"            # stainless, brushed (the counter's)
        return {"N1": "N2"}.get(role)
    return None


def p7_grown(style, grow, bare):
    base = p7(style)

    def paint(sc, x, y):
        m = base(sc, x, y)
        t = sc.tileL[sc.L][y][x]
        role = sc.role[y][x]
        if t in bare and role is not None and (m is None or m == role):
            g = grow(sc, x, y, role, t)
            if g is not None:
                return g
        return m
    return paint


# ---------------------------------------------------------------------------------------- the departure
#  smoke.png: 16x72, frames 0..3 at rows 0, 16, 32, 48 (ANIMCMD_FRAME 0/4/8/12 for 10/20/20/30 ticks; it drifts
#  right a pixel every 4 ticks), rows 64..71 a spare tile left blank. wake.png: 16x64, two 16x32 frames alternating
#  every 12 ticks, set 80 px aft of the ship's centre and trailing to the right. Drawn in ANNE_PAL's indices.
def smoke7(style):
    im = Image.new("P", (16, 72), 0)
    px = im.load()
    for f in range(4):
        y0 = f * 16
        for y in range(16):
            for x in range(16):
                c = style(f, x, y)
                if c:
                    px[x, y0 + y] = c
    return im


def wake7(style):
    im = Image.new("P", (16, 64), 0)
    px = im.load()
    for f in range(2):
        for y in range(32):
            for x in range(16):
                c = style(f, x, y)
                if c:
                    px[x, f * 32 + y] = c
    return im


def puff(cx, cy, r, x, y):
    return math.hypot(x + 0.5 - cx, (y + 0.5 - cy) * 1.15) <= r


def SA_smoke(f, x, y):
    """A: puffs with a postmark's waves through them, thinning to waves alone"""
    r = [3.2, 4.6, 5.6, 6.2][f]
    cy = [11, 9, 7, 6][f]
    inside = puff(8, cy, r, x, y) or (f >= 1 and puff(5, cy + 2, r * 0.7, x, y)) or (f >= 2 and puff(11, cy - 2, r * 0.6, x, y))
    if f == 3 and inside and H(x, y, 7) % 3 == 0:
        inside = False
    if not inside:
        return 0
    if abs((y - cy) - wave(x, 0, 6, 1.0)) < 0.6 or abs((y - cy - 3) - wave(x, 0, 6, 1.0)) < 0.6:
        return 7
    return 6 if y > cy + 1 else 5


def SA_wake(f, x, y):
    """A: the airmail's chevrons, opening aft"""
    cy = 15.5
    d = abs(y + 0.5 - cy)
    if d > 4 + x * 0.7:
        return 0
    k = (x + int(d * 0.8) + f * 2) % 6
    if x < 3:
        return 5
    return 5 if k < 2 else 14 if k < 4 else 13 if d < 3 else 0


def SB_smoke(f, x, y):
    """B: a ring, in time -- each frame the ring a beat wider and fainter"""
    r = [2.5, 4.0, 5.5, 7.0][f]
    d = math.hypot(x + 0.5 - 8, (y + 0.5 - [11, 9, 8, 7][f]) * 1.1)
    if abs(d - r) < [1.6, 1.3, 1.0, 0.7][f]:
        if f == 3 and (x + y) % 2:
            return 0
        return 7 if y > [11, 9, 8, 7][f] else 5
    if f == 0 and d < r:
        return 6
    return 0


def SB_wake(f, x, y):
    """B: standing waves -- three sine lines that swap their crests each frame"""
    for k, cy in enumerate((11.5, 15.5, 19.5)):
        a = (1.5 + x * 0.12) * (1 if (k + f) % 2 else -1)
        if abs(y + 0.5 - cy - math.sin(x * 2 * math.pi / 8) * a) < 0.75:
            return 5 if k == 1 else 14
    if x < 2 and 10 <= y <= 21:
        return 5
    return 0


def SC_smoke(f, x, y):
    """C: coal smoke off one funnel -- a billow that breaks up and greys as it goes"""
    cy = [11, 9, 8, 7][f]
    blobs = [(8, cy, [3.4, 4.2, 4.6, 4.4][f])]
    if f >= 1:
        blobs.append((5, cy + 1.5, 3.0))
    if f >= 2:
        blobs.append((11.5, cy - 1.5, 3.2))
    inside = any(puff(a, b, r, x, y) for a, b, r in blobs)
    if not inside or (f == 3 and H(x, y, 11) % 4 == 0):
        return 0
    edge = not any(puff(a, b, r - 1.1, x, y) for a, b, r in blobs)
    if f >= 2:
        return 7 if edge or y > cy else 6
    return 6 if edge else 5 if y < cy + 1 else 6


def SC_wake(f, x, y):
    """C: white foam off the counter stern, light between, breaking up aft"""
    cy = 15.5
    d = abs(y + 0.5 - cy)
    half = 3 + x * 0.6
    if d > half:
        return 0
    if x < 4:
        return 5 if d < half - 0.8 else 14
    k = H(x // 2, int(d), f) % 5
    if d > half - 1.2:
        return 5 if k < 3 else 0
    return 14 if k < 2 else 5 if k < 3 else 13 if x > 9 else 14


SMOKE7 = {"A": (SA_smoke, SA_wake), "B": (SB_smoke, SB_wake), "C": (SC_smoke, SC_wake)}


def mask(im):
    m = Image.new("L", im.size, 0)
    o, p = m.load(), im.load()
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y]:
                o[x, y] = 255
    return m


def sprite_rgb(im, pal=ANNE_PAL, bg=None):
    out = Image.new("RGB", im.size, bg or pal[0])
    o, p = out.load(), im.load()
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y]:
                o[x, y] = pal[p[x, y]]
    return out


def save_sprite(im, path):
    im = im.copy()
    flat = []
    for c in ANNE_PAL:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(path, bits=4)


# ---------------------------------------------------------------------------------------- the directions
def direction7(name, title, lines, mat, style, smoke):
    return dict(name=name, title=title, lines=lines, mat=mat, paint=p7(style), smoke=smoke)


A7 = direction7(
    "A", "THE PACKET",
    ["the ship's post (T-494: the lioness posts a letter; MOM gets a card with a ship's stamp). A packet boat is the",
     "mail ship, and a packet is what a network carries. Laid-paper bulkheads, the airmail border where the",
     "stripe was, kraft boards with perforated seams; one cabin carpeted in stamps, one in envelope backs;",
     "portholes as postmarks; mail sacks on the deck; the galley's tables sorting frames; a postcard on the wall.",
     "Departure: puffs crossed by a postmark's waves; the wake as airmail chevrons."],
    dict(OUT=(40, 36, 52), N1=(120, 112, 104), N2=(158, 150, 136), N3=(204, 196, 178), N4=(232, 226, 210),
         WHT=(252, 250, 242), Y1=(150, 30, 36), Y2=(204, 52, 52), Y3=(236, 110, 96), B1=(30, 50, 110),
         B2=(52, 84, 160), B3=(120, 170, 220), W1=(150, 112, 72), W2=(192, 154, 106), W3=(220, 190, 142),
         M1=(120, 112, 104), M3=(214, 206, 190), G1=(40, 90, 80), G2=(70, 130, 110), G3=(120, 170, 140),
         G4=(190, 214, 180), G5=(240, 240, 224), O1=(176, 140, 96), O2=(214, 184, 140), O3=(240, 222, 186),
         C1=(110, 90, 60), C2=(150, 126, 88), C3=(190, 168, 124), C4=(226, 210, 170), F1=(204, 52, 52),
         F2=(52, 84, 160), F3=(40, 36, 52), F4=(250, 246, 236)),
    STYLE7_A, SMOKE7["A"])

B7 = direction7(
    "B", "THE KEY, NO TUNE",
    ["the band's sheet (the captain: \"a key and no tune\"; the tune is somewhere in ARDOR -- the singing fir, THE",
     "NEXUS). A band keeps time as a clock does with no program loaded. Fluted ivory panels with a staff where the",
     "stripe was, nothing written on it, a brass picture rail; ebony rails; basketweave parquet; one",
     "cabin carpeted in keyboards, one in sound's rings on red velvet; brass cymbals for portholes; drums on deck;",
     "the sea in the painting five long swells. Departure: smoke rings in time; the wake standing waves."],
    dict(OUT=(24, 20, 28), N1=(88, 80, 84), N2=(140, 130, 124), N3=(196, 186, 170), N4=(230, 222, 204),
         WHT=(250, 246, 232), Y1=(150, 104, 40), Y2=(204, 156, 64), Y3=(240, 206, 120), B1=(20, 18, 24),
         B2=(44, 40, 48), B3=(84, 78, 92), W1=(140, 88, 52), W2=(184, 130, 82), W3=(214, 170, 118),
         M1=(110, 100, 100), M3=(220, 212, 196), G1=(20, 18, 24), G2=(60, 56, 62), G3=(180, 172, 160),
         G4=(226, 220, 206), G5=(248, 244, 232), O1=(120, 40, 48), O2=(170, 64, 64), O3=(214, 120, 104),
         C1=(120, 30, 36), C2=(170, 52, 52), C3=(220, 200, 160), C4=(248, 240, 220), F1=(204, 156, 64),
         F2=(150, 104, 40), F3=(24, 20, 28), F4=(250, 246, 232)),
    STYLE7_B, SMOKE7["B"])

C7 = direction7(
    "C", "THE LIVERY",
    ["the outside carried in: the captain has loved boats since before you could walk, and the liner at the pier is",
     "already ours (genships: navy hull, white house, one amber funnel, red boot-top, light in the portholes).",
     "White enamel bulkheads, riveted, a navy band with an amber pinstripe; teak paid with black caulking; brass",
     "portholes with four dogs; one cabin navy with amber compass roses, one red in a rope weave; teak casks with",
     "brass hoops; a stainless galley; the ship herself in the painting. Departure: coal smoke; white foam."],
    dict(OUT=(16, 16, 40), N1=(120, 126, 150), N2=(152, 160, 184), N3=(208, 212, 224), N4=(232, 234, 240),
         WHT=(248, 248, 240), Y1=(176, 112, 32), Y2=(232, 168, 48), Y3=(250, 214, 120), B1=(24, 32, 64),
         B2=(40, 56, 104), B3=(136, 200, 232), W1=(140, 98, 60), W2=(184, 140, 90), W3=(214, 178, 124),
         M1=(120, 126, 150), M3=(208, 212, 224), G1=(16, 20, 48), G2=(32, 44, 88), G3=(52, 72, 130),
         G4=(136, 200, 232), G5=(232, 168, 48), O1=(120, 30, 30), O2=(176, 48, 40), O3=(220, 110, 90),
         C1=(110, 74, 44), C2=(152, 112, 72), C3=(200, 160, 104), C4=(230, 200, 150), F1=(176, 112, 32),
         F2=(232, 168, 48), F3=(16, 16, 40), F4=(248, 248, 240)),
    STYLE7_C, SMOKE7["C"])
C7["paint"] = p7_grown(STYLE7_C, C_grow, C_BARE)          # the user's pick, extended (C_GROW above)
STYLES7 = {"A": A7, "B": B7, "C": C7}


# ---------------------------------------------------------------------------------------- pair 7's sheets
def render7(m, state=None, crop=None):
    """a room as the engine draws it (general's primary), today or with STATE = (tiles, palettes)"""
    lid = G.LAYOUT_OF_MAP[m]
    l = next(x for x in G.LAYOUTS if x["id"] == lid)
    p, s = G.tileset_data(l["primary_tileset"]), G.tileset_data(l["secondary_tileset"])
    stiles, spals = s["tiles"], s["pals"]
    if state is not None:
        stiles, pl = state
        spals = [pl[r] for r in range(16)]
    pals = p["pals"][:7] + [spals[r] for r in range(7, 16)]
    W, Hh = l["width"], l["height"]
    bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    img = Image.new("RGB", (W * 16, Hh * 16))
    o = img.load()
    for yy in range(Hh):
        for xx in range(W):
            mm = struct.unpack_from("<H", bd, (yy * W + xx) * 2)[0] & 0x3FF
            buf, k = (p["mt"], mm) if mm < 640 else (s["mt"], mm - 640)
            ee = struct.unpack_from("<8H", buf, k * 16) if (k + 1) * 16 <= len(buf) else (0,) * 8
            for layer in (0, 1):
                for q in range(4):
                    t = ee[layer * 4 + q]
                    i = t & 0x3FF
                    src = p["tiles"][i] if i < 640 else (stiles[i - 640] if i - 640 < len(stiles) else [0] * 64)
                    pal = pals[(t >> 12) & 15]
                    for ty in range(8):
                        for tx in range(8):
                            sx = 7 - tx if (t >> 10) & 1 else tx
                            sy = 7 - ty if (t >> 11) & 1 else ty
                            vv = src[sy * 8 + sx]
                            if layer and vv == 0:
                                continue
                            o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = tuple(pal[vv])
    if crop:
        x0, y0, x1, y1 = crop
        img = img.crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
    return img


ROOMS_SS = [
    [("SSAnne_Deck", "the deck", None), ("SSAnne_CaptainsOffice", "the captain's office", None),
     ("SSAnne_Kitchen", "the galley", None)],
    [("SSAnne_1F_Room1", "a cabin (7 rooms)", None), ("SSAnne_2F_Room1", "a cabin (11 rooms)", None),
     ("SSAnne_B1F_Corridor", "B1F, the hold's corridor", None), ("SSAnne_1F_Corridor", "1F corridor (part)",
                                                                  (0, 4, 16, 12))],
]
DETAILS7 = [("SSAnne_CaptainsOffice", (0, 1, 9, 6), "the captain's office: painting, desk, book"),
            ("SSAnne_1F_Room1", (0, 0, 6, 4), "a cabin: door, porthole, carpet"),
            ("SSAnne_2F_Room1", (3, 0, 6, 5), "the other cabin: porthole, bed"),
            ("SSAnne_Kitchen", (0, 1, 8, 8), "the galley: porthole, a table"),
            ("SSAnne_Deck", (13, 3, 24, 15), "the deck: barrels, the house, portholes"),
            ("SSAnne_Deck", (0, 13, 10, 19), "the bow: rail, hull")]


def smoke_at():
    """(x offset from the ship's sprite x, screen y) where src/ss_anne.c sets the smoke"""
    src = open(os.path.join(GBA, "src/ss_anne.c")).read()
    m = re.search(r"CreateSmokeSprite\(void\)\s*\{.*?x2 \+ (\d+);.*?sSmokeSpriteTemplate, x, (\d+),", src, re.S)
    return (int(m.group(1)), int(m.group(2))) if m else (49, 78)


FUNNEL_MOUTH = (72, 84, 1)       # genships' funnel: its mouth's columns and top row in the 128x64 picture


def departure_scene(ship, smoke, wake, frame=1, scale=1):
    """the ship as the cutscene sets her up: her sprite at (88, 80) -- the 128x64 object is drawn from subsprites at
    x -32/+32 and y -16/+16, so her picture spans (56..183, 64..127) -- the smoke where src/ss_anne.c sets it
    (smoke_at(), each frame drifted right a pixel per 4 ticks), the wake at +80 (y 109)"""
    sea = Image.new("RGB", (240, 160), ANNE_PAL[0])
    sx, sy = 88, 80
    sea.paste(sprite_rgb(ship), (sx - 32, sy - 16), mask(ship))
    kx, ky = smoke_at()
    for i, (f, dx) in enumerate(((0, 0), (1, 2), (2, 7), (3, 12))):
        fr = smoke.crop((0, f * 16, 16, f * 16 + 16))
        sea.paste(sprite_rgb(fr), (sx + kx - 8 + dx, ky - 8), mask(fr))
    wf = wake.crop((0, frame * 32, 16, frame * 32 + 32))
    sea.paste(sprite_rgb(wf), (sx + 80 - 8 + 2, 109 - 16), mask(wf))
    return sea.resize((240 * scale, 160 * scale), Image.NEAREST)


def contact_sheets7(out_dir, states, sprites):
    names = list(states)
    titles = {"NOW": ("NOW", ["today: Nintendo's ship inside; gbatowns batch G laid the deck's teak, riveted the bulkheads",
                              "and wove the cabins' carpet (a DRAFT, 2026-10-28); the portholes, painting, beds, barrels,",
                              "galley and stripes as Nintendo drew them. The smoke and wake are pret's, drawn in",
                              "indices that genships' palette makes brown and porthole-blue."])}
    for k in STYLES7:
        titles[k] = ("%s %s" % (k, STYLES7[k]["title"]), STYLES7[k]["lines"])
    pad = 10
    paths = []
    for part, rooms in enumerate(ROOMS_SS, 1):
        blocks = []
        for k in names:
            st = states[k]
            ims = [(render7(m, st, cr), cap) for m, cap, cr in rooms]
            t, lines = titles[k]
            th = 8 + 12 * len(lines) + 16
            W = sum(i.width for i, _ in ims) + pad * (len(ims) + 1)
            im = Image.new("RGB", (max(W, 1100), th + max(i.height for i, _ in ims) + pad), BG)
            d = ImageDraw.Draw(im)
            text(d, (pad, 6), t, RED)
            for j, s in enumerate(lines):
                text(d, (pad + 200, 6 + 12 * j), s)
            x = pad
            for i, cap in ims:
                text(d, (x, th - 13), cap, SOFT)
                im.paste(i, (x, th))
                x += i.width + pad
            blocks.append(im)
        W = max(b.width for b in blocks)
        sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 30), BG)
        d = ImageDraw.Draw(sh)
        text(d, (pad, 8), "T-447 DRAFT, pair 7 -- the S.S. ANNE (%d of 2), real rooms at 1x, three directions beside "
                          "today's (redrawn in place: no block, collision or palette row moves; 0 new tiles)" %
             part, INK)
        y = 30
        for b in blocks:
            sh.paste(b, (0, y))
            y += b.height
        p = os.path.join(out_dir, "t447p7_rooms_1x_%d.png" % part)
        sh.save(p)
        paths.append(p)
    for part, idxs in ((1, (0, 1, 2)), (2, (3, 4, 5))):
        rowsim = []
        for k in names:
            crops = []
            for i in idxs:
                m, cr, cap = DETAILS7[i]
                im = render7(m, states[k], cr)
                crops.append((im.resize((im.width * 3, im.height * 3), Image.NEAREST), cap))
            rowsim.append((k, crops))
        cw = sum(c.width for c, _ in rowsim[0][1]) + pad * (len(idxs) + 1) + 130
        ch = max(c.height for c, _ in rowsim[0][1]) + 24
        det = Image.new("RGB", (cw, ch * len(names) + 30), BG)
        d = ImageDraw.Draw(det)
        text(d, (pad, 8), "T-447 DRAFT, pair 7 -- details at 3x (%d of 2)" % part, INK)
        y = 30
        for k, crops in rowsim:
            text(d, (pad, y + 6), titles[k][0][:18], RED)
            x = 130
            for c, cap in crops:
                text(d, (x, y + 2), cap, SOFT)
                det.paste(c, (x, y + 16))
                x += c.width + pad
            y += ch
        p = os.path.join(out_dir, "t447p7_detail_3x_%d.png" % part)
        det.save(p)
        paths.append(p)
    #  the tiles at 3x, each in its home row
    cols = []
    own = set(owned7())
    for k in names:
        st = states[k]
        tiles, pals = st if st else (SS.cur, TODAY7_ALL)
        used_rows = sorted({t // 16 for t in own})
        strip = Image.new("RGB", (128, 8 * len(used_rows)), (236, 236, 236))
        o = strip.load()
        for j, rr in enumerate(used_rows):
            for t in range(rr * 16, rr * 16 + 16):
                if t not in own:
                    continue
                rws = rows_of7(t)
                hr = max(rws, key=rws.get)
                for q in range(64):
                    vv = tiles[t][q]
                    o[(t % 16) * 8 + q % 8, j * 8 + q // 8] = tuple(pals[hr][vv]) if vv else (200, 200, 200)
        cols.append((titles[k][0], strip.resize((384, strip.height * 3), Image.NEAREST)))
    W = sum(c.width + pad for _, c in cols) + pad
    sh = Image.new("RGB", (W, max(c.height for _, c in cols) + 50), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 6), "T-447 DRAFT, pair 7 -- the S.S. ANNE's tiles at 3x, each in its home row (grey: transparent; "
                      "the door, the void and general's rows not shown)", INK)
    x = pad
    for t, c in cols:
        text(d, (x, 26), t[:44], RED)
        sh.paste(c, (x, 42))
        x += c.width + pad
    p = os.path.join(out_dir, "t447p7_tiles_3x.png")
    sh.save(p)
    paths.append(p)
    #  the departure: the scene at 1x, and the frames at 6x
    ship = Image.open(os.path.join(GBA, "graphics/object_events/pics/misc/ss_anne.png"))
    blocks = []
    for k in names:
        sm, wk = sprites[k]
        scene = departure_scene(ship, sm, wk)
        frames = Image.new("RGB", (16 * 6 * 4 + 30 + 16 * 6 * 2 + 10, 32 * 6), BG)
        for f in range(4):
            fr = sprite_rgb(sm.crop((0, f * 16, 16, f * 16 + 16)))
            frames.paste(fr.resize((96, 96), Image.NEAREST), (f * 96 + f * 2, 0))
        for f in range(2):
            fr = sprite_rgb(wk.crop((0, f * 32, 16, f * 32 + 32)))
            frames.paste(fr.resize((96, 192), Image.NEAREST), (4 * 98 + 20 + f * 100, 0))
        t, lines = titles[k]
        im = Image.new("RGB", (240 + frames.width + 3 * pad, 160 + 2 * pad + 30), BG)
        d = ImageDraw.Draw(im)
        text(d, (pad, 4), t, RED)
        text(d, (pad + 240 + pad, 4), "smoke, frames 1-4 (6x)                                      wake, frames 1-2 (6x)", SOFT)
        im.paste(scene, (pad, 22))
        im.paste(frames, (2 * pad + 240, 22))
        blocks.append(im)
    W = max(b.width for b in blocks)
    sh = Image.new("RGB", (W, sum(b.height for b in blocks) + 44), BG)
    d = ImageDraw.Draw(sh)
    text(d, (pad, 6), "T-447 DRAFT, pair 7 -- the departure (src/ss_anne.c): smoke and wake in the S.S. ANNE's own "
                      "palette (genships, unchanged), the ship as she stands", INK)
    text(d, (pad, 20), "the smoke at the ship's x %+d, y %d (src/ss_anne.c): the 128x64 ship is drawn from x-32, so "
                       "that is column %d -- the funnel's mouth (%d..%d)" % (smoke_at() + (smoke_at()[0] + 32,
                                                                              FUNNEL_MOUTH[0], FUNNEL_MOUTH[1])), SOFT)
    y = 40
    for b in blocks:
        sh.paste(b, (0, y))
        y += b.height
    p = os.path.join(out_dir, "t447p7_departure.png")
    sh.save(p)
    paths.append(p)
    return paths


TODAY7_ALL = {r: (TODAY7[r] if r >= 7 else [tuple(c) for c in GEN_NOW["pals"][r]]) for r in range(16)}


# ---------------------------------------------------------------------------------------- pair 7's report
def report7():
    bad = 0
    picks = {k: APPROVED[k] for k in SETS7 if k in APPROVED}
    print("\n  pair 7 (the S.S. ANNE + its departure) -- DRAFT, %s" %
          ("APPROVED %s" % picks if picks else "not approved: `--pair 7 --write --approved` refuses"))
    own = owned7()
    placed = sorted(t for t in SS.use if t < SS.nvan and any(SS.cur[t]))
    van = [t for t in placed if SS.cur[t] == SS.van[t] and len(set(SS.van[t])) > 1]
    rows = sorted({r for t in placed for r in SS.use[t]["rows"]})
    fixed = sorted(t for t in placed if any(r < 7 for r in SS.use[t]["rows"]) and t not in CLOTH)
    print("    ss_anne: %d placed tiles on %d maps, %d still Nintendo's drawing; rows placed %s, own %s" %
          (len(placed), len(SS_MAPS), len(van), rows, SS.rows))
    print("    drawn here %d; kept: the door 0x281 (28, 29, 44, 45: gbadoors' hinged door), the void (1), and %d in "
          "general's fixed rows %s" % (len(own), len(fixed), fixed))
    print("    scenes: %s" % ", ".join(sc.name for sc in SCENES7))
    #  gbatowns must keep every tile these rooms draw
    towns = _literal(os.path.join(ROOT, "tools", "gbatowns.py"), "LANDMARKS") or {}
    boxed = {b[0] for b in towns.get("ss_anne", [])}
    want = {l["name"][:-len("_Layout")] for l in G.LAYOUTS if l.get("secondary_tileset") == SS.sym and G.MBL.get(l["id"])}
    if boxed != want:
        print("  !! gbatowns.LANDMARKS does not hold the S.S. ANNE's nine layouts (%s missing): its write could redraw "
              "them" % sorted(want - boxed))
        bad = 1
    else:
        print("    gbatowns.LANDMARKS holds the S.S. ANNE's %d layouts (all %d rooms): its write keeps every tile they "
              "draw" % (len(want), len(SS_MAPS)))
    #  the ship's palette the departure draws in is genships'
    try:
        gpal = [tuple(int(v) for v in l.split()) for l in
                open(os.path.join(GBA, "graphics/object_events/palettes/ss_anne.pal")).read().split("\n")[3:19]]
    except (OSError, ValueError):
        gpal = None
    if gpal != ANNE_PAL:
        print("  !! graphics/object_events/palettes/ss_anne.pal is not the ANNE_PAL the smoke and wake are drawn in")
        bad = 1
    else:
        print("    departure: smoke and wake drawn in genships' ANNE_PAL (PALSLOT_NPC_SPECIAL = OBJ palette 10); "
              "today's vanilla frames show index 10 (planking, dark) and 14 (porthole light)")
    kx, ky = smoke_at()
    if not FUNNEL_MOUTH[0] <= kx + 32 <= FUNNEL_MOUTH[1]:
        print("  !! src/ss_anne.c sets the smoke at x %+d, column %d of the ship's picture: not over the funnel's mouth "
              "(%d..%d)" % (kx, kx + 32, FUNNEL_MOUTH[0], FUNNEL_MOUTH[1]))
        bad = 1
    else:
        print("    the smoke at x %+d, y %d (src/ss_anne.c): column %d of the ship, in the funnel's mouth (%d..%d)" %
              (kx, ky, kx + 32, FUNNEL_MOUTH[0], FUNNEL_MOUTH[1]))
    known = {"gbatowns.py", "gbadoors.py", "genships.py", "companion_export.py", "check_reach.py", "gbagrove.py",
             "gbanexusmap.py", "gbaprimary.py", "gbawater.py", "port_dialogue.py", "check_generators.py"}
    found = set()
    me = os.path.basename(__file__)
    for f in sorted(glob.glob(os.path.join(ROOT, "tools", "*.py"))):
        if os.path.basename(f) == me:
            continue
        if re.search(r"ss_anne|gTileset_SSAnne", open(f, encoding="utf-8", errors="ignore").read()):
            found.add(os.path.basename(f))
    if found - known:
        print("  !! a tool this one does not know names the S.S. ANNE's tileset: %s -- read it before a write" %
              sorted(found - known))
        bad = 1
    for k, D in STYLES7.items():
        (tiles, pals), owner = draw7(D)
        moved = [t for t in range(SS.nvan) if any((a == 0) != (b == 0) for a, b in zip(tiles[t], SS.cur[t]))]
        stray = [t for t in range(SS.nvan) if tiles[t] != SS.cur[t] and t not in set(own)]
        missed = sorted(set(own) - set(owner))
        if moved or stray or missed:
            print("  !! %s: footprint %s, not this pair's %s, in no scene %s" % (k, moved[:8], stray[:8], missed[:8]))
            bad = 1
        if any(pals[r] != TODAY7[r] for r in range(7, 16) if r not in SS.rows):
            print("  !! %s: a row this pair does not own changed" % k)
            bad = 1
        n = sum(1 for t in own if tiles[t] != SS.van[t])
        print("    %s %-20s redrawn %d of %d, the other %d recoloured in its rows (Nintendo's shapes: chairs, stairs, "
              "rails, bins); + smoke 4 frames, wake 2; 0 new tiles, rows 7, 8, 9" % (k, D["title"], n, len(own),
                                                                                    len(own) - n))
    return bad


def check_engine7():
    bad = 0
    pick = APPROVED.get("ss")
    if pick:
        (tiles, pals), _ = draw7(STYLES7[pick])
        off = [t for t in range(len(SS.cur)) if tiles[t] != SS.cur[t]]
        rows = [r for r in SS.rows if pals[r] != TODAY7[r]]
        if off or rows:
            print("  !! the S.S. ANNE: the engine differs from `--pair 7 --write --approved` (%s) in tiles %s rows %s"
                  % (pick, off[:12], rows))
            bad = 1
    return bad


def main7():
    pick = APPROVED.get("ss")
    if WRITE:
        if "--approved" not in ARGS or not pick:
            print("  --write refused: T-447 pair 7 is a draft. APPROVED holds no pick for the S.S. ANNE (\"ss\"); the "
                  "user picks a\n  direction first, it goes into APPROVED (\"ss\": X), then `--pair 7 --write "
                  "--approved` writes ss_anne's tiles and rows\n  7, 8, 9 and graphics/ss_anne/smoke.png and wake.png "
                  "(never the door, the void, or general's rows).")
            return 1
        (tiles, pals), _ = draw7(STYLES7[pick])
        G.save_like(os.path.join(GBA, SS.dir, "tiles.png"), tiles, os.path.join(GBA, SS.dir, "tiles.png"))
        for r in SS.rows:
            write_pal(os.path.join(GBA, SS.dir, "palettes", "%02d.pal" % r), pals[r])
        sm, wk = STYLES7[pick]["smoke"]
        save_sprite(smoke7(sm), os.path.join(GBA, "graphics/ss_anne/smoke.png"))
        save_sprite(wake7(wk), os.path.join(GBA, "graphics/ss_anne/wake.png"))
        print("  written: the S.S. ANNE, direction %s (tiles, rows 7, 8, 9, smoke, wake)" % pick)
        return 0
    bad = report()
    if DRAFT is not None:
        out = DRAFT if DRAFT != DRAFT_DEFAULT else DRAFT7_DEFAULT
        os.makedirs(out, exist_ok=True)
        states = collections.OrderedDict()
        states["NOW"] = None
        sprites = {"NOW": (Image.open(os.path.join(GBA, "graphics/ss_anne/smoke.png")),
                           Image.open(os.path.join(GBA, "graphics/ss_anne/wake.png")))}
        summary = {}
        for k, D in STYLES7.items():
            (tiles, pals), owner = draw7(D)
            dd = os.path.join(out, k, "ss_anne")
            os.makedirs(os.path.join(dd, "palettes"), exist_ok=True)
            G.save_like(os.path.join(GBA, SS.dir, "tiles.png"), tiles, os.path.join(dd, "tiles.png"))
            for r in SS.rows:
                write_pal(os.path.join(dd, "palettes", "%02d.pal" % r), pals[r])
            sm, wk = D["smoke"]
            smi, wki = smoke7(sm), wake7(wk)
            save_sprite(smi, os.path.join(out, k, "smoke.png"))
            save_sprite(wki, os.path.join(out, k, "wake.png"))
            states[k] = (tiles, pals)
            sprites[k] = (smi, wki)
            summary[k] = dict(title=D["title"], lines=D["lines"], new_tiles=0, rows=SS.rows,
                              tiles_redrawn=sum(1 for t in owned7() if tiles[t] != SS.van[t]), of=len(owned7()))
        json.dump(dict(ticket="T-447", pair=7, status="DRAFT -- not in the engine", approved={"ss": pick} if pick else {},
                       directions=summary), open(os.path.join(out, "directions.json"), "w"), indent=1)
        for p in contact_sheets7(out, states, sprites):
            print("  sheet:", p)
    return 1 if bad else 0


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
    bad |= report5()
    bad |= report6()
    bad |= report7()
    return bad


def check_engine():
    """with a pick approved, the engine must be exactly what `--write --approved` makes"""
    bad = 0
    for bkey, pick in APPROVED.items():
        if bkey not in SETS:
            continue                                   # pair 5's picks: check_engine5
        sets, prim, _ = draw(STYLES[pick], only=bkey)
        S = SETS[bkey]
        off = [t for t in range(len(S.cur)) if sets[bkey][0][t] != S.cur[t]]
        rows = [r for r in S.rows if [tuple(c) for c in sets[bkey][1][r]] != [tuple(c) for c in TODAY_PAL[bkey, r]]]
        dia = [t for t in prim if prim[t] != G.PTILES_NOW[t]] if bkey == "man" else []
        if off or rows or dia:
            print("  !! %s: the engine differs from `--write --approved` (%s) in tiles %s rows %s diary %s"
                  % (NAMES[bkey], pick, off[:12], rows, dia))
            bad = 1
    bad |= check_engine5()
    bad |= check_engine6()
    bad |= check_engine7()
    if APPROVED and not bad:
        print("  the engine matches `--write --approved` (%s)" % APPROVED)
    return bad


def main():
    if PAIR == "5":
        return main5()
    if PAIR == "6":
        return main6()
    if PAIR == "7":
        return main7()
    if WRITE:
        if "--approved" not in ARGS or not APPROVED:
            print("  --write refused: T-447 pair 4 is a draft. APPROVED is %s; the user picks a direction per building "
                  "first, it goes\n  into APPROVED ({\"man\": X, \"tow\": Y}), then --write --approved writes "
                  "pokemon_mansion's tiles and rows 7, 8, 12,\n  the diary's four primary tiles, and pokemon_tower's "
                  "tiles and rows 7, 8, 9, 12 (never the stones' slots)." % (APPROVED or "empty"))
            return 1
        for bkey, pick in APPROVED.items():
            if bkey not in SETS:
                continue                               # pairs 5, 6 and 7 write only with --pair 5 / 6 / 7
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

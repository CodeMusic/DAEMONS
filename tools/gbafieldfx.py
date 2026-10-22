#!/usr/bin/env python3
"""The field effects and the weather, drawn to sit on our ground (T-438 batch B).

    python3 tools/gbafieldfx.py                    # report: every field-effect and weather sheet -- size, frames,
                                                   #   palette, whether the game can show it, where it is first seen
    python3 tools/gbafieldfx.py --draft [DIR]      # the new sheets as PNGs in DIR (gfx/drafts/t438/fieldfx/), the
                                                   #   proposed general_0.pal beside them, and the contact sheets
                                                   #   (or --sheets DIR to put those elsewhere)
    python3 tools/gbafieldfx.py --write --approved # into the engine -- NOT YET: batch B is a draft until the user
                                                   #   has seen the sheets; without --approved --write refuses

WHAT A FIELD EFFECT IS. A small sprite the overworld spawns where something happens on the ground: the grass parting
round your feet, the dust when you land from a ledge, the prints you leave in sand, a ring on a pond. Each is a
sheet in graphics/field_effects/pics (or graphics/weather), cut into frames by src/data/field_effects/
field_effect_objects.h (or field_weather_effects.c). Every sheet drawn here keeps its vanilla SIZE, FRAME COUNT,
FRAME LAYOUT (reading order, which -mwidth/-mheight in spritesheet_rules.mk preserves) and PALETTE TAG, so no code
changes -- only the art, and for general_0 its palette (below).

THE PALETTES. Field effects do not have fixed slots (that is object events, engine.md trap 17): each effect script
loads its palette BY TAG into a free slot (`loadfadedpal`), so a tag is shared by every effect that names it and a
new colour in a shared palette changes every effect that uses that index. So:

  general_0 (FLDEFF_PAL_TAG_GENERAL_0, still vanilla): dust 1-3, water 4-8, sand 11-14. Every sheet that names it is
      redrawn here, so its palette can change with them. PROPOSED: the dust and sand rows move onto our ground --
      vanilla's sand yellows (238,230,164)... are not the colours our path and beach tiles draw with
      ((238,230,139), (222,197,139), (213,189,106)), so a print in vanilla's palette sits on our sand as a decal.
      The water row stays. This is the one palette change batch B asks for.
  general_1 (FLDEFF_PAL_TAG_GENERAL_1, ours since T-61) and its BLANCHE copy (blanche_grass.pal): unchanged. The
      grass greens are already ours; the water blues 6-9 are shared with blanche_grass.pal and stay.
  player.pal (no tag: sprite palette 0, the PLAYER's): the shadows draw here, as vanilla's do. Indices 12 and 13 are
      the shoes (T-256, patched at runtime), so nothing here uses them.
  Own palettes (fldeff_cut, small_sparkle, the field-move streaks, the HALL OF FAME monitor): each sheet carries its
      own, so its colours are free.
  meteorite.pal (OBJ_EVENT_PAL_TAG_METEORITE, ours): the ANNEX stone's fragments draw in the stone's own palette.
  The weather (PALTAG_WEATHER, default.pal, vanilla): unchanged -- rain, snow and fog are redrawn in its colours.

WHAT THE GAME CAN SHOW, measured rather than assumed (engine.md trap 15). FireRed stubs half of Ruby's ground
behaviours (metatile_behavior.c: IsLongGrass, IsDeepSand, IsShortGrass, IsAshGrass, IsFootprints return FALSE), no
map places a disguised trainer, T-387 made GOTO a ribbon of notes instead of a bird, and nothing sets cloudy, ash
or bubble weather. A sheet the game never draws is listed as DEAD and is drawn only if it is a cheap derivative
of a live one (deep prints, short and long grass, the sand pile); the rest are left vanilla, and say so.

STYLE. Our ground is soft and outlined in its own darker colours, not black: a print is a press in the sand's own
shades, a ripple a lit upper arc and a shaded lower one, dust a pale puff of the path. Effects that sit on a tile
take that tile's colours (sampled from the map they are first seen on, by the contact sheet).
"""
import io, json, math, os, random, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t438", "fieldfx")
FX = "graphics/field_effects"
WX = "graphics/weather"

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


# ================================================================== reading the engine
def jasc(path):
    t = open(path, "rb").read().decode("utf-8", "replace").replace("\r", "").split("\n")
    return [tuple(map(int, l.split()[:3])) for l in t[3:19]]


def png(rel):
    p = os.path.join(GBA, rel)
    return Image.open(p) if os.path.exists(p) else None


def png_pal(im):
    p = im.getpalette() or []
    p = p + [0] * (48 - len(p))
    return [tuple(p[i * 3:i * 3 + 3]) for i in range(16)]


def frames_of(im, fw, fh, n):
    """the sheet's frames in reading order, each fh rows of fw indices (0..15)"""
    px = im.load()
    cols = im.width // fw
    out = []
    for k in range(n):
        x0, y0 = (k % cols) * fw, (k // cols) * fh
        out.append([[px[x0 + x, y0 + y] & 15 for x in range(fw)] for y in range(fh)])
    return out


def sheet_of(frames, fw, fh, size, pal):
    """frames laid back into a sheet of vanilla's own size and layout, as an indexed PNG in PAL"""
    W, H = size
    im = Image.new("P", (W, H), 0)
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    px = im.load()
    cols = W // fw
    for k, f in enumerate(frames):
        x0, y0 = (k % cols) * fw, (k // cols) * fh
        for y in range(fh):
            for x in range(fw):
                px[x0 + x, y0 + y] = f[y][x]
    return im


def vanilla_bytes(rel):
    return daemonslib.upstream(GBA, rel, missing=None, binary=True)


# ================================================================== the palettes
G0_CUR = jasc(os.path.join(GBA, FX, "palettes/general_0.pal"))
G1 = jasc(os.path.join(GBA, FX, "palettes/general_1.pal"))
PLAYER = jasc(os.path.join(GBA, "graphics/object_events/palettes/player.pal"))
METEORITE = jasc(os.path.join(GBA, "graphics/object_events/palettes/meteorite.pal"))
WEATHER = jasc(os.path.join(GBA, WX, "default.pal"))

# general_0, proposed: dust and sand onto our ground; water unchanged
G0_NEW = list(G0_CUR)
G0_NEW[1] = (248, 244, 214)       # dust, lit
G0_NEW[2] = (232, 222, 170)       # dust
G0_NEW[3] = (204, 188, 128)       # dust, shade
G0_NEW[11] = (238, 230, 139)      # sand: our path and beach, exactly
G0_NEW[12] = (222, 197, 139)      # sand, shade (the tiles' own speck)
G0_NEW[13] = (213, 189, 106)      # a press (the tiles' darker speck)
G0_NEW[14] = (182, 158, 82)       # a deep press: one step past the tiles, the only new colour
DUST_L, DUST, DUST_D = 1, 2, 3
W_WHITE, W_PALE, W_LIGHT, W_MID, W_DEEP = 4, 5, 6, 7, 8
SAND, SAND_SH, PRESS, DEEP = 11, 12, 13, 14

# general_1 index jobs (gbagrass.py)
LIT, LEAF, DARK, DEEPLEAF = 1, 2, 3, 4
R_DEEP, R_TEAL, R_LIGHT, R_LIT = 6, 7, 8, 9          # the water blues
BASE, GLIGHT, TUFT, TDARK = 13, 12, 14, 15

SHADOW = 6                                           # player.pal (34,34,40): near-black, never the shoes' 12/13

CUT_PAL = [(0, 0, 0), (240, 250, 200), (204, 236, 132), (42, 82, 44)] + [(0, 0, 0)] * 12   # our greens, both ends
#   (a clipping in the grass's own greens vanished into the grass it was cut from, at any shade: it needs the leaf's
#   deepest green, general_1's 4, as an outline, and a near-white lit tip, so it reads as thrown and still belongs)
STREAK_OUT_PAL = [(0, 0, 0), (0, 0, 0), (248, 248, 248), (196, 210, 232)] + [(0, 0, 0)] * 12


# ================================================================== drawing helpers
def blank(w, h):
    return [[0] * w for _ in range(h)]


def put(f, x, y, v):
    if 0 <= y < len(f) and 0 <= x < len(f[0]):
        f[y][x] = v


def inside(x, y, cx, cy, rx, ry):
    return ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0


def ring(f, cx, cy, rx, ry, colour_of, step=None):
    """an ellipse's outline, one pixel wide; colour_of(angle) picks each pixel's index (None leaves a gap)"""
    seen = set()
    for i in range(360):
        a = math.radians(i)
        x, y = int(math.floor(cx + rx * math.cos(a))), int(math.floor(cy + ry * math.sin(a)))
        if (x, y) in seen:
            continue
        seen.add((x, y))
        v = colour_of(a, x, y)
        if v is not None:
            put(f, x, y, v)


def puff(f, cx, cy, r):
    """a round puff of dust: lit above, shaded below"""
    for y in range(len(f)):
        for x in range(len(f[0])):
            if inside(x, y, cx, cy, r, r * 0.85):
                dy = (y + 0.5 - cy) / r
                f[y][x] = DUST_L if dy < -0.35 else DUST_D if dy > 0.4 else DUST


def from_rows(rows, key):
    return [[key.get(ch, 0) for ch in r] for r in rows]


def stamp(f, pat, x0, y0):
    for y, row in enumerate(pat):
        for x, v in enumerate(row):
            if v:
                put(f, x0 + x, y0 + y, v)


def rot_ccw(pat):
    h, w = len(pat), len(pat[0])
    return [[pat[y][w - 1 - x] for y in range(h)] for x in range(w)]


def bbox(frame):
    pts = [(x, y) for y, r in enumerate(frame) for x, v in enumerate(r) if v]
    if not pts:
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


# ================================================================== the effects, drawn
def draw_shadow(van):
    """vanilla's ellipse, which is already the right shape for a five-row shadow (a drawn ellipse came out a box), in
    the palette's near-black (34,34,40) instead of pure black -- shade on the ground, not a hole in it"""
    return [[[SHADOW if v else 0 for v in row] for row in van[0]]]


def draw_dust(van):
    a, b, c = blank(16, 8), blank(16, 8), blank(16, 8)
    puff(a, 5.0, 5.2, 2.1); puff(a, 11.0, 5.2, 2.1)
    puff(b, 3.0, 4.4, 1.8); puff(b, 13.0, 4.4, 1.8); puff(b, 8.0, 5.6, 1.1)
    for x, y, v in ((1, 3, DUST), (2, 2, DUST_L), (14, 3, DUST), (13, 2, DUST_L), (0, 5, DUST_D), (15, 5, DUST_D),
                    (5, 6, DUST_D), (10, 6, DUST_D)):
        put(c, x, y, v)
    return [a, b, c]


def drop(f, x, y, big=False):
    put(f, x, y, W_WHITE)
    put(f, x, y + 1, W_LIGHT)
    if big:
        put(f, x + 1, y, W_PALE)


def draw_splash(van):
    """walking through shallow water: a low ring at the feet and a few drops"""
    a, b = blank(16, 8), blank(16, 8)
    ring(a, 8.0, 6.4, 4.2, 1.3, lambda t, x, y: W_PALE if math.sin(t) < 0 else W_MID)
    for x, y in ((5, 3), (8, 2), (11, 3)):
        drop(a, x, y)
    ring(b, 8.0, 6.4, 6.4, 1.5, lambda t, x, y: (W_LIGHT if math.sin(t) < 0 else W_MID) if (x + y) % 3 else None)
    for x, y in ((3, 4), (13, 4), (6, 3), (10, 3)):
        drop(b, x, y)
    return [a, b]


def crown(f, base, heights, xs, rx):
    """a splash's crown: a ring at the waterline and spikes standing on it"""
    ring(f, 8.0, base, rx, 1.4, lambda t, x, y: W_PALE if math.sin(t) < 0 else W_MID)
    for x, hgt in zip(xs, heights):
        for k in range(hgt):
            put(f, x, int(base) - 1 - k, W_WHITE if k == hgt - 1 else W_PALE if k > hgt // 2 else W_LIGHT)


def draw_jump_small(van):
    a, b, c = blank(16, 8), blank(16, 8), blank(16, 8)
    crown(a, 6.6, (2, 4, 2), (5, 8, 11), 3.6)
    ring(b, 8.0, 6.4, 5.6, 1.4, lambda t, x, y: W_LIGHT if math.sin(t) < 0 else W_MID)
    for x, y in ((3, 2), (13, 2), (6, 1), (10, 1), (8, 3)):
        drop(b, x, y)
    ring(c, 8.0, 6.4, 7.0, 1.5, lambda t, x, y: W_MID if (x + y) % 3 == 0 else None)
    for x, y in ((1, 3), (14, 3), (4, 5), (12, 5)):
        put(c, x, y, W_LIGHT)
    return [a, b, c]


def draw_jump_big(van):
    fr = [blank(16, 16) for _ in range(4)]
    crown(fr[0], 13.6, (3, 5, 6, 5, 3), (4, 6, 8, 10, 12), 5.0)
    crown(fr[1], 13.6, (5, 8, 10, 8, 5), (3, 5, 8, 11, 13), 5.6)
    for x, y in ((2, 4), (13, 4), (8, 1)):
        drop(fr[1], x, y, True)
    ring(fr[2], 8.0, 13.6, 6.2, 1.5, lambda t, x, y: W_LIGHT if math.sin(t) < 0 else W_MID)
    for k in range(5):
        put(fr[2], 8, 12 - k, W_PALE if k < 4 else W_WHITE)
    for x, y in ((3, 6), (12, 6), (5, 3), (10, 3), (1, 9), (14, 9)):
        drop(fr[2], x, y)
    ring(fr[3], 8.0, 13.6, 7.2, 1.6, lambda t, x, y: W_MID if (x + y) % 3 else None)
    for x, y in ((2, 10), (13, 10), (5, 8), (11, 8)):
        put(fr[3], x, y, W_LIGHT)
    return fr


def draw_ripple(van):
    """a ring that widens and fades: its upper arc lit, its lower in the water's shade"""
    fr = []
    spec = [(3.4, 1.9, 1.0), (5.2, 2.7, 1.0), (6.2, 3.3, 0.9), (7.0, 3.9, 0.6), (7.4, 4.2, 0.35)]
    for k, (rx, ry, keep) in enumerate(spec):
        f = blank(16, 16)

        def col(t, x, y, keep=keep, k=k):
            if keep < 1.0 and ((x * 7 + y * 3) % 10) / 10.0 >= keep:
                return None
            up = math.sin(t) < -0.2
            if k <= 1:
                return R_LIT if up else R_LIGHT
            if k == 2:
                return R_LIGHT if up else R_DEEP
            return R_LIGHT if up else R_TEAL
        ring(f, 8.0, 8.5, rx, ry, col)
        if k == 3:                                    # the second, smaller ring that follows the first
            ring(f, 8.0, 8.5, 3.0, 1.5, lambda t, x, y: R_LIT if math.sin(t) < 0 else R_LIGHT)
        fr.append(f)
    return fr


def print_north():
    """a monkey's footprint, toes up: two toes, the ball, the sole, the heel -- pressed in the sand's own shades"""
    return from_rows(["p.p",
                      "...",
                      "pdp",
                      "ddd",
                      ".d."], {"p": PRESS, "d": DEEP})


def draw_footprints(van):
    n = print_north()
    w = rot_ccw(n)                                     # toes to the west
    a, b = blank(16, 16), blank(16, 16)
    stamp(a, n, 9, 2); stamp(a, n, 4, 10)
    stamp(b, w, 10, 10); stamp(b, w, 2, 12)
    return [a, b]


def draw_deep_footprints(van):
    n = from_rows([".p.p",
                   "....",
                   "sddp",
                   "sdDd",
                   "sdDd",
                   ".dd."], {"p": PRESS, "d": DEEP, "D": DEEP, "s": SAND_SH})
    w = rot_ccw(n)
    a, b = blank(16, 16), blank(16, 16)
    stamp(a, n, 9, 1); stamp(a, n, 3, 9)
    stamp(b, w, 10, 9); stamp(b, w, 1, 11)
    return [a, b]


def draw_tracks(van):
    """vanilla's track geometry kept to the pixel (each frame must meet the next cell's), restyled: a soft lip
    either side and a tread down the middle"""
    out = []
    for f0 in van:
        f = blank(16, 16)
        for y in range(16):
            for x in range(16):
                v = f0[y][x]
                if v == 13:
                    f[y][x] = SAND_SH
                elif v == 14:
                    f[y][x] = PRESS if (x + y) % 3 == 0 else DEEP
        out.append(f)
    return out


def draw_sand_pile(van):
    fr = []
    for k, (rx, ry) in enumerate(((6.5, 2.2), (5.5, 2.6), (4.5, 1.6))):
        f = blank(16, 8)
        for y in range(8):
            for x in range(16):
                if inside(x, y, 8.0, 8.0, rx, ry * 1.6):
                    dy = (y + 0.5 - (8.0 - ry * 1.6))
                    f[y][x] = SAND_SH if dy < 1.0 else SAND if dy < 2.4 else PRESS
        if k < 2:
            for x, y in ((2, 3 - k), (13, 3 - k), (5, 2 - k), (11, 2 - k)):
                put(f, x, y, SAND_SH)
        fr.append(f)
    return fr


def draw_hot_springs(van):
    """the spa's water over the bather's waist: vanilla's shape (it is the tile's water), a lit crest round the body"""
    f0 = van[0]
    f = [row[:] for row in f0]
    top = {}
    for x in range(16):
        for y in range(16):
            if f0[y][x]:
                top[x] = y
                break
    for x, y in top.items():
        f[y][x] = R_LIT
    for x, y in ((3, 8), (2, 9), (12, 8), (13, 9)):
        put(f, x, y, R_LIT)
    for x, y in ((4, 9), (11, 9)):
        put(f, x, y, R_TEAL)
    for x, y in ((1, 12), (2, 12), (13, 11), (14, 11), (6, 14), (7, 14)):
        put(f, x, y, R_LIT if y < 13 else R_TEAL)
    return [f]


def clump_from_engine():
    """our tall-grass clump: tall_grass.png's second frame, which gbagrass.py drew as the whole clump"""
    fr = frames_of(png(FX + "/pics/tall_grass.png"), 16, 16, 5)
    return fr[1]


def draw_long_grass(van):
    """the player sunk in long grass: our clump, swaying -- the higher a blade, the further it leans"""
    cl = clump_from_engine()
    out = []
    for sway in (0, 1, 0, -1):
        f = blank(16, 16)
        for y in range(16):
            dx = int(round(sway * (15 - y) / 10.0))
            for x in range(16):
                v = cl[y][x]
                if v and v != BASE:
                    put(f, x + dx, y, v)
                elif y >= 9:
                    put(f, x + dx, y, TUFT)
        out.append(f)
    return out


def draw_jump_long_grass(van):
    cl = clump_from_engine()
    lower = [[(v if y >= 9 and v != BASE else 0) for v in row] for y, row in enumerate(cl)]
    bits = [[(3, 3), (12, 3), (6, 1), (9, 1)], [(2, 2), (13, 2), (5, 0), (10, 0)], [(1, 4), (14, 4), (4, 2), (11, 2)],
            [(1, 6), (14, 6), (4, 5), (11, 5)], [(2, 8), (13, 8)], []]
    out = []
    for k, bb in enumerate(bits):
        f = [row[:] for row in lower]
        for x, y in bb:
            put(f, x, y, LIT if k < 3 else GLIGHT)
            put(f, x + 1, y, LEAF if k < 3 else TUFT)
        out.append(f)
    return out


def draw_short_grass(van):
    """our sprig (gbagrass.grass_tile's V of two blades), round the feet, flattened on the second frame"""
    a, b = blank(16, 16), blank(16, 16)
    for x0 in (3, 8, 12):
        put(a, x0 - 1, 13, GLIGHT); put(a, x0 + 1, 13, TUFT); put(a, x0, 14, TDARK)
        put(b, x0 - 1, 14, GLIGHT); put(b, x0 + 1, 14, TUFT); put(b, x0, 15, TDARK)
    return [a, b]


def draw_cut(van):
    """PRUNE on grass: a clipped sprig of our leaf -- two blades and their cut stem -- that the code spins"""
    return [from_rows([".3....3.",
                       "313..313",
                       "31233213",
                       ".322223.",
                       "..3223..",
                       "...33...",
                       "........",
                       "........"], {"1": 1, "2": 2, "3": 3})]


def draw_sparkle(van):
    """REVEAL's shimmer: a glint, then a four-pointed star with short diagonals and a soft heart"""
    b0 = bbox(van[0]) or (6, 6, 9, 9)
    cx, cy = (b0[0] + b0[2]) // 2, (b0[1] + b0[3]) // 2
    a, b = blank(16, 16), blank(16, 16)
    put(a, cx, cy, 1)
    for d, v in ((1, 2), (2, 3)):
        for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
            put(a, cx + dx, cy + dy, v)
    for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        put(a, cx + dx, cy + dy, 4)
    b1 = bbox(van[1]) or (0, 0, 15, 15)
    cx, cy = (b1[0] + b1[2]) // 2, (b1[1] + b1[3]) // 2
    for d in range(0, 8):
        v = 1 if d <= 2 else 2 if d <= 4 else 3 if d <= 6 else 4
        for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
            put(b, cx + dx, cy + dy, v)
    for d, v in ((1, 2), (2, 3), (3, 4)):
        for dx, dy in ((d, d), (-d, d), (d, -d), (-d, -d)):
            put(b, cx + dx, cy + dy, v)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        put(b, cx + dx, cy + dy, 1)
    return [a, b]


def draw_hof_monitor(van):
    """the RECORD's screen: CHECKPOINT's BOX cartridge (gbacheckpoint.py's glyph) instead of a Poke Ball, dark,
    then lighting up in three steps"""
    out = [[[11] * 16 for _ in range(16)]]
    for lit, line in ((14, 15), (13, 14), (12, 13)):
        f = [[11] * 16 for _ in range(16)]
        for y in range(2, 14):
            for x in range(3, 13):
                edge = y in (2, 13) or x in (3, 12)
                if (x, y) in ((3, 2), (12, 2), (3, 13), (12, 13), (11, 2), (12, 3)):
                    continue                           # rounded corners, the top-right one clipped like a cartridge
                if edge:
                    f[y][x] = lit
        for x in range(5, 11):                         # the label window
            f[4][x] = line; f[8][x] = line
        for y in range(4, 9):
            f[y][5] = line; f[y][10] = line
        for x in range(6, 10):
            f[6][x] = lit
        f[10][6] = lit; f[10][7] = lit                 # its light
        for x in (5, 7, 9, 11):                        # its pins
            f[12][x] = line
        out.append(f)
    return out


SHARDS = {
    "top_left": ["........",
                 ".1......",
                 ".121....",
                 ".1221...",
                 "..12231.",
                 "..12331.",
                 "...1111.",
                 "........"],
    "top_right": ["........",
                  "......1.",
                  "....1131",
                  "...12331",
                  "..12233.",
                  ".1122331",
                  "..111111",
                  "........"],
    "bottom_left": ["........",
                    ".111....",
                    ".1221...",
                    ".12231..",
                    ".122331.",
                    "..11111.",
                    "........",
                    "........"],
    "bottom_right": ["........",
                     "..1111..",
                     ".122331.",
                     ".1223331",
                     "..12331.",
                     "...111..",
                     "........",
                     "........"],
}


def draw_shard(which):
    def fn(van):
        return [from_rows(SHARDS[which], {"1": 1, "2": 2, "3": 3})]
    return fn


def draw_streaks_outdoors(van):
    """the field-move banner's streaks: a rounded head, a white core with a pale edge, a tail that breaks up.
    Tiles as vanilla's tilemap uses them: 1 the ground, 2 head, 3 body, 4 tail; 0 and 5..15 unused."""
    t = [blank(8, 8) for _ in range(16)]
    for k in range(16):
        if k == 0:
            continue
        for y in range(8):
            for x in range(8):
                t[k][y][x] = 1
    for y in (2, 5):
        for x in range(2, 8):
            t[2][y][x] = 3
    for y in (3, 4):
        t[2][y][1] = 3
        for x in range(2, 8):
            t[2][y][x] = 2
    for x in range(8):
        t[3][2][x] = 3; t[3][5][x] = 3; t[3][3][x] = 2; t[3][4][x] = 2
    for x in range(8):
        if x < 3:
            t[4][2][x] = 3; t[4][5][x] = 3
        if x < 4:
            t[4][3][x] = 2; t[4][4][x] = 2
        elif x < 7:
            t[4][3][x] = 3; t[4][4][x] = 3 if x < 6 else 1
    frame = blank(32, 32)
    for k in range(16):
        for y in range(8):
            for x in range(8):
                frame[(k // 4) * 8 + y][(k % 4) * 8 + x] = t[k][y][x]
    return [frame]


def draw_streaks_indoors(van):
    """indoors: the band's border keeps its steps but softens (a dark line, a light one, a shadow into the blue), and
    the streaks are a white line over a pale one"""
    f = [row[:] for row in van[0]]
    for x in range(8):
        f[16][x] = 2; f[17][x] = 4; f[18][x] = 3; f[19][x] = 5; f[20][x] = 5
        for y in (21, 22, 23):
            f[y][x] = 5
        for y in range(24, 32):
            f[y][x] = 5
        f[27][x] = 4; f[28][x] = 3
    return [f]


# ---------------------------------------------------------------- weather
def rain_line(van0):
    """the streak's slope and its bottom-left end, from vanilla's falling frame (the motion code moves along it)"""
    pts = [(x, y) for y, r in enumerate(van0) for x, v in enumerate(r) if v]
    lo = max(pts, key=lambda p: p[1])
    hi = min(pts, key=lambda p: p[1])
    return lo, (hi[0] - lo[0]) / float(lo[1] - hi[1])


def draw_rain(van):
    (bx, by), slope = rain_line(van[0])
    out = []

    def streak(f, length, gap_every=0):
        for k in range(length):
            y = by - k
            x = int(round(bx + slope * k))
            if gap_every and k % gap_every == gap_every - 1:
                continue
            v = 15 if k < 2 else 1 if k < 6 else 2 if k < 11 else 3
            put(f, x, y, v)
    f = blank(16, 32); streak(f, 16); out.append(f)                     # 0: falling
    f = blank(16, 32); streak(f, 8)                                      # 1: hits
    out.append(f)
    for k, (rx, ry, drops) in enumerate(((2.4, 0.9, ((2, 26), (7, 26))), (3.4, 1.1, ((1, 24), (8, 24), (4, 23))),
                                         (4.2, 1.3, ((0, 22), (9, 23))))):
        f = blank(16, 32)                                                # 2..4: the heavy splash
        ring(f, 4.5, 29.6, rx, ry, lambda t, x, y, k=k: (15 if math.sin(t) < 0 else 2) if k < 2 or (x + y) % 2 else None)
        for x, y in drops:
            put(f, x, y, 15 if k == 0 else 1)
        out.append(f)
    f = blank(16, 32)                                                    # 5: the light splash's last
    ring(f, 4.5, 29.6, 3.4, 1.1, lambda t, x, y: 2 if (x + y) % 2 else None)
    out.append(f)
    return out


def flake(size):
    f = blank(8, 8)
    if size:
        pat = ["...f....",
               ".e.f.e..",
               "..eDe...",
               "ffDFDff.",
               "..eDe...",
               ".e.f.e..",
               "...f....",
               "........"]
        return from_rows(pat, {"f": 15, "F": 15, "D": 14, "e": 13})
    return from_rows(["........",
                      "........",
                      "...e....",
                      "..eFe...",
                      "...e....",
                      "........",
                      "........",
                      "........"], {"F": 15, "e": 13})


def draw_snow0(van):
    return [flake(1)]


def draw_snow1(van):
    return [flake(0)]


FOG_LEVELS = [4, 8, 12, 5, 6, 7, 13, 14, 15]        # default.pal's greys, dark to light


def fog(diagonal):
    """a 64x64 tile of mist that wraps both ways (the code tiles it): long soft bands -- stretched four times wider
    than they are tall, as the fog drifts sideways -- dithered between neighbouring greys rather than speckled"""
    rnd = random.Random(438 + diagonal)
    grids = {}

    def noise(u, v, nx, ny):
        g = grids.setdefault((nx, ny), [[rnd.random() for _ in range(nx)] for _ in range(ny)])
        u, v = u * nx, v * ny
        i, j = int(math.floor(u)), int(math.floor(v))
        fu, fv = u - i, v - j
        fu, fv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)
        at = lambda a, b: g[b % ny][a % nx]
        return (at(i, j) * (1 - fu) + at(i + 1, j) * fu) * (1 - fv) + (at(i, j + 1) * (1 - fu) + at(i + 1, j + 1) * fu) * fv
    bayer = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    f = blank(64, 64)
    for y in range(64):
        for x in range(64):
            u, v = x / 64.0, y / 64.0
            if diagonal:
                u = ((x + y) % 64) / 64.0
            val = 0.5 * noise(u, v, 2, 6) + 0.32 * noise(u, v, 4, 12) + 0.18 * noise(u, v, 8, 16)
            val = max(0.0, min(0.999, (val - 0.5) * 1.9 + 0.5))
            lvl = val * (len(FOG_LEVELS) - 1)
            base = int(lvl)
            if (lvl - base) * 16 > bayer[y % 4][x % 4] and base + 1 < len(FOG_LEVELS):
                base += 1
            f[y][x] = FOG_LEVELS[base]
    return f


def draw_fog_h(van):
    return [fog(0)]


def draw_fog_d(van):
    return [fog(1)]


# ================================================================== the census of sheets
# key, sheet, frame w, h, frames, palette (name), tag, live, why, first seen (map, x, y) or None, drawer
P_G0, P_G1, P_PLAYER, P_OWN, P_MET, P_WX, P_ASH, P_SPARKLE = "general_0", "general_1", "player (slot 0)", "own", "meteorite", "weather", "ash", "small_sparkle"
EFFECTS = [
    ("shadow_medium", FX + "/pics/shadow_medium.png", 16, 8, 1, P_PLAYER, "TAG_NONE -> slot 0", True,
     "every ledge jump (215 graphics infos are SHADOW_SIZE_M)", ("Route1", 4, 6), draw_shadow),
    ("shadow_small", FX + "/pics/shadow_small.png", 8, 8, 1, P_PLAYER, "TAG_NONE -> slot 0", True,
     "18 small graphics infos", ("Route1", 4, 6), draw_shadow),
    ("shadow_large", FX + "/pics/shadow_large.png", 32, 8, 1, P_PLAYER, "TAG_NONE -> slot 0", False,
     "no graphics info is SHADOW_SIZE_L", None, draw_shadow),
    ("shadow_extra_large", FX + "/pics/shadow_extra_large.png", 64, 32, 1, P_PLAYER, "TAG_NONE -> slot 0", False,
     "no graphics info is SHADOW_SIZE_XL", None, draw_shadow),
    ("ground_impact_dust", FX + "/pics/ground_impact_dust.png", 16, 8, 3, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", True,
     "landing from a ledge", ("Route1", 4, 6), draw_dust),
    ("tall_grass", FX + "/pics/tall_grass.png", 16, 16, 5, P_G1, "FLDEFF_PAL_TAG_GENERAL_1 / BLANCHE_GRASS", True,
     "ALREADY OURS (gbagrass.py, T-61): shown for reference, not redrawn", ("Route1", 10, 6), None),
    ("jump_tall_grass", FX + "/pics/jump_tall_grass.png", 16, 8, 4, P_G1, "FLDEFF_PAL_TAG_GENERAL_1 / BLANCHE_GRASS", True,
     "ALREADY OURS (gbagrass.py, T-61): shown for reference, not redrawn", ("Route1", 10, 6), None),
    ("fldeff_cut", FX + "/fldeff_cut.png", 8, 8, 1, P_OWN, "0x1000 (its own fldeff_cut.gbapal)", True,
     "PRUNE on grass", ("Route1", 10, 6), draw_cut),
    ("ripple", FX + "/pics/ripple.png", 16, 16, 5, P_G1, "FLDEFF_PAL_TAG_GENERAL_1", True,
     "anything on pond water or a puddle (TRAVERSE on a pond)", ("ViridianCity", 12, 27), draw_ripple),
    ("sand_footprints", FX + "/pics/sand_footprints.png", 16, 16, 2, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", True,
     "walking on MB_SAND (frame 0 north, flipped south; frame 1 west, flipped east)", ("VermilionCity", 14, 10),
     draw_footprints),
    ("bike_tire_tracks", FX + "/pics/bike_tire_tracks.png", 16, 16, 4, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", True,
     "cycling on MB_SAND (the BIKE comes after ARDOR)", ("VermilionCity", 14, 10), draw_tracks),
    ("splash", FX + "/pics/splash.png", 16, 8, 2, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", True,
     "feet in shallow water or a puddle", ("Breathverse", 12, 14), draw_splash),
    ("jump_small_splash", FX + "/pics/jump_small_splash.png", 16, 8, 3, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", True,
     "jumping onto shallow water", ("Breathverse", 12, 14), draw_jump_small),
    ("jump_big_splash", FX + "/pics/jump_big_splash.png", 16, 16, 4, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", True,
     "jumping onto water", ("Breathverse", 12, 14), draw_jump_big),
    ("small_sparkle", FX + "/pics/small_sparkle.png", 16, 16, 2, P_SPARKLE, "FLDEFF_PAL_TAG_SMALL_SPARKLE (its own)", True,
     "REVEAL's shimmer over a hidden item or a grove's tree (reveal.c)", ("Route10", None, None), draw_sparkle),
    ("hot_springs_water", FX + "/pics/hot_springs_water.png", 16, 16, 1, P_G1, "FLDEFF_PAL_TAG_GENERAL_1", True,
     "standing in the spring", ("OneIsland_KindleRoad_EmberSpa", 11, 12), draw_hot_springs),
    ("field_move_streaks_outdoors", FX + "/pics/field_move_streaks_outdoors.png", 32, 32, 1, P_OWN,
     "BG palette 15 (its own .gbapal)", True, "a field routine's banner, outdoors", None, draw_streaks_outdoors),
    ("field_move_streaks_indoors", FX + "/pics/field_move_streaks_indoors.png", 8, 32, 1, P_OWN,
     "BG palette 15 (its own .gbapal)", True, "a field routine's banner, indoors", None, draw_streaks_indoors),
    ("hof_monitor", FX + "/pics/hof_monitor.png", 16, 16, 4, P_OWN, "4112 (its own .gbapal)", True,
     "the RECORD's machine (FLDEFF_HALL_OF_FAME_RECORD)", ("PokemonLeague_HallOfFame", None, None), draw_hof_monitor),
    ("deoxys_rock_fragment_top_left", FX + "/pics/deoxys_rock_fragment_top_left.png", 8, 8, 1, P_MET,
     "OBJ_EVENT_PAL_TAG_METEORITE", True, "THE ANNEX's stone breaking", ("BirthIsland_Exterior", None, None), draw_shard("top_left")),
    ("deoxys_rock_fragment_top_right", FX + "/pics/deoxys_rock_fragment_top_right.png", 8, 8, 1, P_MET,
     "OBJ_EVENT_PAL_TAG_METEORITE", True, "THE ANNEX's stone breaking", ("BirthIsland_Exterior", None, None), draw_shard("top_right")),
    ("deoxys_rock_fragment_bottom_left", FX + "/pics/deoxys_rock_fragment_bottom_left.png", 8, 8, 1, P_MET,
     "OBJ_EVENT_PAL_TAG_METEORITE", True, "THE ANNEX's stone breaking", ("BirthIsland_Exterior", None, None), draw_shard("bottom_left")),
    ("deoxys_rock_fragment_bottom_right", FX + "/pics/deoxys_rock_fragment_bottom_right.png", 8, 8, 1, P_MET,
     "OBJ_EVENT_PAL_TAG_METEORITE", True, "THE ANNEX's stone breaking", ("BirthIsland_Exterior", None, None), draw_shard("bottom_right")),
    # ---- never shown by this game; drawn only where it is a cheap derivative of a live one
    ("deep_sand_footprints", FX + "/pics/deep_sand_footprints.png", 16, 16, 2, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", False,
     "IsDeepSand returns FALSE", None, draw_deep_footprints),
    ("sand_pile", FX + "/pics/sand_pile.png", 16, 8, 3, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", False,
     "deep sand only; IsDeepSand returns FALSE", None, draw_sand_pile),
    ("long_grass", FX + "/pics/long_grass.png", 16, 16, 4, P_G1, "FLDEFF_PAL_TAG_GENERAL_1", False,
     "IsLongGrass returns FALSE", None, draw_long_grass),
    ("jump_long_grass", FX + "/pics/jump_long_grass.png", 16, 16, 6, P_G1, "FLDEFF_PAL_TAG_GENERAL_1", False,
     "IsLongGrass returns FALSE", None, draw_jump_long_grass),
    ("short_grass", FX + "/pics/short_grass.png", 16, 16, 2, P_G1, "FLDEFF_PAL_TAG_GENERAL_1", False,
     "IsShortGrass returns FALSE", None, draw_short_grass),
    ("ash", FX + "/pics/ash.png", 16, 16, 5, P_G1, "FLDEFF_PAL_TAG_GENERAL_1", False,
     "IsAshGrass returns FALSE (Ruby's ash grass)", None, None),
    ("unused_grass", FX + "/pics/unused_grass.png", 16, 16, 9, P_G1, "FLDEFF_PAL_TAG_GENERAL_1", False,
     "FLDEFF_UNUSED_GRASS: nothing starts it", None, None),
    ("unused_grass_2", FX + "/pics/unused_grass_2.png", 16, 16, 4, P_G1, "FLDEFF_PAL_TAG_GENERAL_1", False,
     "FLDEFF_UNUSED_GRASS_2: nothing starts it", None, None),
    ("unused_grass_3", FX + "/pics/unused_grass_3.png", 16, 8, 3, P_G1, "-", False,
     "no template draws it", None, None),
    ("unused_grass_4", FX + "/pics/unused_grass_4.png", 16, 16, 4, P_G1, "-", False,
     "no template draws it", None, None),
    ("unused_sand", FX + "/pics/unused_sand.png", 16, 16, 4, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", False,
     "FLDEFF_UNUSED_SAND: nothing starts it", None, None),
    ("water_surfacing", FX + "/pics/water_surfacing.png", 16, 16, 4, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", False,
     "FLDEFF_UNUSED_WATER_SURFACING (DIVE): nothing starts it", None, None),
    ("underwater_bubbles", FX + "/pics/underwater_bubbles.png", 16, 32, 8, P_G0, "FLDEFF_PAL_TAG_GENERAL_0", False,
     "MB_SEAWEED only, and no map places it", None, None),
    ("pop_out_of_ash", FX + "/pics/pop_out_of_ash.png", 16, 16, 5, P_ASH, "FLDEFF_PAL_TAG_ASH", False,
     "no map places a buried trainer", None, None),
    ("lavaridge_warp", FX + "/pics/lavaridge_warp.png", 16, 16, 5, P_ASH, "FLDEFF_PAL_TAG_ASH", False,
     "Lavaridge's warp: nothing starts it", None, None),
    ("tree_disguise", FX + "/pics/tree_disguise.png", 16, 32, 7, P_PLAYER, "TAG_NONE", False,
     "no map places a disguised trainer", None, None),
    ("mountain_disguise", FX + "/pics/mountain_disguise.png", 16, 32, 7, P_PLAYER, "TAG_NONE", False,
     "no map places a disguised trainer", None, None),
    ("sand_disguise", FX + "/pics/sand_disguise.png", 16, 32, 7, P_PLAYER, "TAG_NONE", False,
     "a placeholder; nothing places it", None, None),
    ("bird", FX + "/pics/bird.png", 64, 64, 5, P_PLAYER, "TAG_NONE -> slot 0", False,
     "T-387: GOTO is not a bird; only FLDEFF_NPCFLY_OUT draws it and no script starts that", None, None),
    ("new_game_oak", FX + "/pics/new_game_oak.png", 64, 64, 1, P_OWN, "0x1006", False,
     "AddNewGameBirchObject is never called", None, None),
]

WEATHERS = [
    ("rain", WX + "/rain.png", 16, 32, 6, "RAIN and STORM (spring, summer; T-415), and DOWNPOUR", True, draw_rain),
    ("snow0", WX + "/snow0.png", 8, 8, 1, "SNOW (winter; T-415): the larger flake", True, draw_snow0),
    ("snow1", WX + "/snow1.png", 8, 8, 1, "SNOW: the smaller flake", True, draw_snow1),
    ("fog_horizontal", WX + "/fog_horizontal.png", 64, 64, 1, "FOG (autumn; T-415) and DAEMON TOWER's 19 floors", True, draw_fog_h),
    ("fog_diagonal", WX + "/fog_diagonal.png", 64, 64, 1, "FOG_DIAGONAL: no map or sky event sets it", False, draw_fog_d),
    ("sandstorm", WX + "/sandstorm.png", 64, 80, 1, "WIND (autumn): ALREADY OURS -- leaves, own sandstorm.gbapal (genwindleaves.py, T-415)", True, None),
    ("cloud", WX + "/cloud.png", 64, 64, 1, "CLOUDS: nothing sets it", False, None),
    ("ash", WX + "/ash.png", 64, 64, 2, "VOLCANIC_ASH: nothing sets it", False, None),
    ("bubble", WX + "/bubble.png", 8, 8, 2, "UNDERWATER_BUBBLES: nothing sets it", False, None),
]


def palette_for(kind, im):
    return {P_G0: G0_CUR, P_G1: G1, P_PLAYER: PLAYER, P_MET: METEORITE, P_WX: WEATHER}.get(kind) or \
        (jasc(os.path.join(GBA, FX, "palettes/ash.pal")) if kind == P_ASH else
         jasc(os.path.join(GBA, FX, "palettes/small_sparkle.pal")) if kind == P_SPARKLE else png_pal(im))


def new_palette_for(key, kind, im):
    if kind == P_G0:
        return G0_NEW
    if key == "fldeff_cut":
        return CUT_PAL
    if key == "field_move_streaks_outdoors":
        return STREAK_OUT_PAL
    return palette_for(kind, im)


def used_indices(frames):
    return sorted({v for f in frames for r in f for v in r})


# ================================================================== where each is first seen
_ORDER = """PALLET_TOWN ROUTE_1 VIRIDIAN_CITY ROUTE_22 ROUTE_2 VIRIDIAN_FOREST PEWTER_CITY ROUTE_3 MT_MOON ROUTE_4
CERULEAN_CITY ROUTE_24 ROUTE_25 ROUTE_5 UNDERGROUND_PATH ROUTE_6 VERMILION_CITY S_S_ANNE ROUTE_11 DIGLETTS_CAVE ROUTE_9
ROUTE_10 ROCK_TUNNEL POWER_PLANT LAVENDER_TOWN ROUTE_8 ROUTE_7 UNDERGROUND_PATH_2 CELADON_CITY ROCKET_HIDEOUT
POKEMON_TOWER SAFFRON_CITY SILPH_CO ROUTE_12 ROUTE_13 ROUTE_14 ROUTE_15 ROUTE_16 ROUTE_17 ROUTE_18 FUCHSIA_CITY
KANTO_SAFARI_ZONE ROUTE_19 ROUTE_20 SEAFOAM_ISLANDS CINNABAR_ISLAND POKEMON_MANSION ROUTE_21 ONE_ISLAND TREASURE_BEACH
KINDLE_ROAD MT_EMBER EMBER_SPA CAPE_BRINK TWO_ISLAND THREE_ISLAND BOND_BRIDGE THREE_ISLE_PORT BERRY_FOREST
THREE_ISLE_PATH ROUTE_23 KANTO_VICTORY_ROAD INDIGO_PLATEAU POKEMON_LEAGUE FOUR_ISLAND ICEFALL_CAVE FIVE_ISLAND""".split()
RANK = {"MAPSEC_" + m: i for i, m in enumerate(_ORDER)}


def place_name(mapname):
    try:
        sec = json.load(open(os.path.join(GBA, "data/maps/%s/map.json" % mapname))).get("region_map_section", "")
        names = {s["id"]: s.get("name", s["id"]) for s in
                 json.load(open(os.path.join(GBA, "src/data/region_map/region_map_sections.json")))["map_sections"]}
        return names.get(sec, sec).replace("é", "E")
    except (OSError, ValueError):
        return mapname


def first_hidden_item():
    """the first map, in story order, with a hidden item -- where REVEAL first shimmers"""
    best = None
    for d in sorted(os.listdir(os.path.join(GBA, "data/maps"))):
        p = os.path.join(GBA, "data/maps", d, "map.json")
        if not os.path.exists(p):
            continue
        m = json.load(open(p))
        hid = [b for b in m.get("bg_events", []) or [] if b.get("type") == "hidden_item"]
        if not hid:
            continue
        r = RANK.get(m.get("region_map_section"), 999)
        outdoor = m.get("map_type") in ("MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE", "MAP_TYPE_OCEAN_ROUTE")
        key = (r, 0 if outdoor else 1, d)
        if best is None or key < best[0]:
            best = (key, d, hid[0]["x"], hid[0]["y"])
    return best[1:] if best else None


def map_object(mapname, gfx_hint):
    m = json.load(open(os.path.join(GBA, "data/maps/%s/map.json" % mapname)))
    for o in m.get("object_events", []) or []:
        if gfx_hint in o.get("graphics_id", ""):
            return o["x"], o["y"]
    return m.get("width", 16) // 2 if "width" in m else 8, 6


# ================================================================== the contact sheets
def font(n):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except OSError:
        return ImageFont.load_default()


_RS = None


def reviewsheet():
    """tools/reviewsheet.py's map renderer, imported with argv swapped round it (engine.md trap 16)"""
    global _RS
    if _RS is None:
        import importlib.util
        argv = sys.argv
        sys.argv = [argv[0]]
        try:
            spec = importlib.util.spec_from_file_location("reviewsheet", os.path.join(ROOT, "tools", "reviewsheet.py"))
            _RS = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_RS)
        finally:
            sys.argv = argv
    return _RS


_MAPS = {}


def map_image(name):
    if name not in _MAPS:
        rs = reviewsheet()
        _MAPS[name] = rs.render(rs.layout_of(name))
    return _MAPS[name]


def player_frame():
    im = png("graphics/object_events/pics/people/red_normal.png")
    f = frames_of(im, 16, 32, 1)[0]
    return rgba(f, PLAYER)


def rgba(frame, pal):
    h, w = len(frame), len(frame[0])
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = im.load()
    for y in range(h):
        for x in range(w):
            v = frame[y][x]
            if v:
                px[x, y] = pal[v] + (255,)
    return im


def opaque(frame, pal):
    h, w = len(frame), len(frame[0])
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = pal[frame[y][x]]
    return im


def ground_colour(e):
    first = e[9]
    if not first:                                      # never shown: under it, the ground it was meant for
        if e[5] == P_G0 and "sand" in e[0]:
            return G0_NEW[SAND]
        if e[5] == P_G1 and "grass" in e[0]:
            return G1[BASE]
    if first and first[1] is not None:
        img = map_image(first[0])
        x, y = first[1] * 16 + 8, first[2] * 16 + 12
        if x < img.width and y < img.height:
            return img.getpixel((x, y))
    return (96, 100, 112)


def strip(frames, pal, ground, Z, is_bg=False):
    if not frames:
        return None
    fh, fw = len(frames[0]), len(frames[0][0])
    im = Image.new("RGB", (len(frames) * (fw * Z + 6) - 6, fh * Z), (16, 16, 20))
    for k, f in enumerate(frames):
        cell = Image.new("RGB", (fw, fh), ground)
        if is_bg:
            cell = opaque(f, pal)
        else:
            cell.paste(rgba(f, pal), (0, 0), rgba(f, pal))
        im.paste(cell.resize((fw * Z, fh * Z), Image.NEAREST), (k * (fw * Z + 6), 0))
    return im


def streak_banner(frames, pal, tilemap_rel, tile_w):
    """the banner as the BG draws it: the 32x10 tilemap over the sheet's tiles"""
    d = open(os.path.join(GBA, tilemap_rel), "rb").read()
    tm = struct.unpack("<%dH" % (len(d) // 2), d)
    sheet = frames[0]
    cols = tile_w // 8
    im = Image.new("RGB", (240, 80))
    px = im.load()
    for r in range(10):
        for c in range(30):
            e = tm[r * 32 + c]
            t = e & 0x3FF
            hf, vf = e & 0x400, e & 0x800
            tx, ty = (t % cols) * 8, (t // cols) * 8
            for y in range(8):
                for x in range(8):
                    sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                    if ty + sy < len(sheet) and tx + sx < len(sheet[0]):
                        px[c * 8 + x, r * 8 + y] = pal[sheet[ty + sy][tx + sx]]
    return im


def context(e, frames, pal, w=10, h=6):
    """the map where it is first seen, its frames laid on successive cells along the row, as the game spawns them"""
    key, first = e[0], e[9]
    if not first:
        return None
    name, cx, cy = first
    if cx is None:
        if key == "small_sparkle":
            hit = first_hidden_item()
            if not hit:
                return None
            name, cx, cy = hit
        elif key == "hof_monitor":
            cx, cy = map_object(name, "")
    img = map_image(name)
    W, H = img.width // 16, img.height // 16
    x0 = max(0, min(W - w, cx - 2))
    y0 = max(0, min(H - h, cy - h // 2))
    crop = img.crop((x0 * 16, y0 * 16, (x0 + w) * 16, (y0 + h) * 16)).convert("RGBA")
    fh, fw = len(frames[0]), len(frames[0][0])
    n = len(frames)
    for k, f in enumerate(frames):
        tx, ty = cx - x0 + (k if n > 1 else 0), cy - y0
        px_ = tx * 16 + (16 - fw) // 2
        py_ = ty * 16 + 16 - fh
        if key == "hof_monitor":
            py_ = ty * 16
        if key.startswith("shadow"):
            py_ = ty * 16 + 16 - fh
        if key == "sand_footprints" and k == 1:
            px_, py_ = (cx - x0 + 2) * 16, ty * 16
        if key == "hot_springs_water":                 # the bather the water covers
            crop.alpha_composite(player_frame(), (tx * 16, ty * 16 - 16))
        sp = rgba(f, pal)
        crop.alpha_composite(sp, (px_, py_))
        if key in ("shadow_medium", "ground_impact_dust") and k == 0:
            pl = player_frame()
            crop.alpha_composite(pl, (tx * 16, ty * 16 - 32 + (2 if key == "ground_impact_dust" else -6)))
    return crop.convert("RGB"), place_name(name), name


def panel(e, van, new, pal_old, pal_new):
    key, rel, fw, fh, n, kind, tag, live, why, first, drawer = e
    F, f2 = font(15), font(12)
    Z = 4 if fw <= 16 else 2 if fw <= 32 else 1
    is_bg = key.startswith("field_move_streaks") or key == "hof_monitor"
    ground = ground_colour(e)
    s_old = strip(van, pal_old, ground, Z, is_bg)
    s_new = strip(new, pal_new, ground, Z, is_bg) if new else None
    ctx_old = ctx_new = None
    label = ""
    if key.startswith("field_move_streaks"):
        tmrel = rel.replace(".png", ".bin")
        ctx_old = (streak_banner(van, pal_old, tmrel, fw), "the banner as drawn", "")
        if new:
            ctx_new = (streak_banner(new, pal_new, tmrel, fw), "the banner as drawn", "")
    elif first and live:
        ctx_old = context(e, van, pal_old)
        if new:
            ctx_new = context(e, new, pal_new)
    if ctx_old:
        label = "first seen: %s (%s)" % (ctx_old[1], ctx_old[2]) if ctx_old[2] else ""
    parts = [s for s in (s_old, s_new) if s]
    CZ = 2
    cw = (ctx_old[0].width * CZ + 10) * (2 if ctx_new else 1) if ctx_old else 0
    ch = ctx_old[0].height * CZ if ctx_old else 0
    sw = max(p.width for p in parts)
    W = max(16 + sw + 24 + cw, 900)
    H = 70 + sum(p.height + 22 for p in parts)
    H = max(H, 70 + ch + 20)
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    status = ("LIVE" if live else "NEVER SHOWN") + ("" if drawer or not live else "")
    dr.text((8, 6), "%s   %dx%d x%d   %s   [%s]" % (key, fw, fh, n, tag, status),
            fill=(250, 214, 120) if live else (170, 170, 180), font=F)
    dr.text((8, 26), why + ("   " + label if label else ""), fill=(200, 200, 210), font=f2)
    note = notes_for(e, new, pal_new)
    dr.text((8, 42), note, fill=(240, 140, 120) if "PALETTE" in note else (140, 210, 150), font=f2)
    y = 62
    for lab, p in (("TODAY", s_old), ("NEW (DRAFT)", s_new)):
        if p is None:
            continue
        dr.text((8, y), lab, fill=(200, 200, 210) if lab == "TODAY" else (140, 210, 150), font=f2)
        im.paste(p, (8, y + 16))
        y += p.height + 22
    if ctx_old:
        x = 16 + sw + 24
        dr.text((x, 62), "TODAY in place", fill=(200, 200, 210), font=f2)
        a = ctx_old[0].resize((ctx_old[0].width * CZ, ctx_old[0].height * CZ), Image.NEAREST)
        im.paste(a, (x, 78))
        if ctx_new:
            x2 = x + a.width + 10
            dr.text((x2, 62), "NEW in place", fill=(140, 210, 150), font=f2)
            b = ctx_new[0].resize((ctx_new[0].width * CZ, ctx_new[0].height * CZ), Image.NEAREST)
            im.paste(b, (x2, 78))
        need = 78 + a.height + 8
        if need > H:
            im2 = Image.new("RGB", (W, need), (16, 16, 20)); im2.paste(im, (0, 0)); im = im2
    return im


def shards_panel(items):
    """THE ANNEX's stone breaking: the four fragments together, and over the stone where it stands"""
    F, f2 = font(15), font(12)
    pal = METEORITE
    name, cx, cy = "BirthIsland_Exterior", 15, 12
    m = json.load(open(os.path.join(GBA, "data/maps/%s/map.json" % name)))
    for o in m.get("object_events", []) or []:
        if o.get("graphics_id") == "OBJ_EVENT_GFX_METEORITE":
            cx, cy = o["x"], o["y"]
    img = map_image(name)
    x0, y0 = max(0, cx - 4), max(0, cy - 3)
    crop = img.crop((x0 * 16, y0 * 16, (x0 + 9) * 16, (y0 + 5) * 16)).convert("RGBA")
    stone = rgba(frames_of(png("graphics/object_events/pics/misc/birth_island_stone.png"), 32, 32, 1)[0], pal)
    sx, sy = (cx - x0) * 16 - 8, (cy - y0) * 16 + 16 - 32
    off = {"top_left": (-6, -8), "top_right": (14, -8), "bottom_left": (-6, 14), "bottom_right": (14, 14)}
    scenes = []
    for which in (0, 1):
        c = crop.copy()
        c.alpha_composite(stone, (sx, sy))
        for e, van, new in items:
            q = e[0][len("deoxys_rock_fragment_"):]
            fr = (van, new)[which][0]
            c.alpha_composite(rgba(fr, pal), (sx + 12 + off[q][0], sy + 12 + off[q][1]))
        scenes.append(c.convert("RGB").resize((c.width * 2, c.height * 2), Image.NEAREST))
    s_old = strip([v[0] for _, v, _ in items], pal, (96, 100, 112), 6)
    s_new = strip([n[0] for _, _, n in items], pal, (96, 100, 112), 6)
    W = max(16 + s_old.width + 24 + 2 * (scenes[0].width + 10), 900)
    H = max(70 + 2 * (s_old.height + 22), 78 + scenes[0].height + 8)
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "deoxys_rock_fragment_*   8x8 x1 each (four sheets)   [OBJ_EVENT_PAL_TAG_METEORITE]   [LIVE]",
            fill=(250, 214, 120), font=F)
    dr.text((8, 26), "THE ANNEX's stone breaking (FLDEFF_DESTROY_DEOXYS_ROCK); first seen: THE ANNEX (%s)" % name,
            fill=(200, 200, 210), font=f2)
    dr.text((8, 42), "indices 1,2,3; meteorite.pal unchanged -- shards of OUR obelisk (dark edge, shade, lit face), "
            "not the red triangle's", fill=(140, 210, 150), font=f2)
    y = 62
    for lab, p in (("TODAY  TL TR BL BR", s_old), ("NEW (DRAFT)", s_new)):
        dr.text((8, y), lab, fill=(200, 200, 210), font=f2)
        im.paste(p, (8, y + 16))
        y += p.height + 22
    x = 16 + s_old.width + 24
    for lab, sc in (("TODAY over the stone", scenes[0]), ("NEW over the stone", scenes[1])):
        dr.text((x, 62), lab, fill=(200, 200, 210), font=f2)
        im.paste(sc, (x, 78))
        x += sc.width + 10
    return im


def notes_for(e, new, pal_new):
    key, rel, fw, fh, n, kind, tag, live, why, first, drawer = e
    if not drawer:
        return "left as it is" + ("" if not live else "")
    used = used_indices(new)
    bits = ["indices %s" % ",".join(map(str, [u for u in used if u]))]
    if kind == P_G0:
        bits.append("PALETTE: general_0's dust (1-3) and sand (11-14) rows move onto our ground -- proposed general_0.pal")
    elif kind == P_PLAYER:
        bits.append("player.pal slot 0; never 12/13 (the shoes)")
    elif key == "fldeff_cut":
        bits.append("its own palette: our greens -- the deepest as outline, a near-white tip (was vanilla's lime)")
    elif key == "field_move_streaks_outdoors":
        bits.append("its own palette: index 3 becomes a pale edge (was unused)")
    elif kind == P_G1:
        bits.append("general_1 unchanged; BLANCHE's copy shares the water blues")
    else:
        bits.append("palette unchanged")
    return "; ".join(bits)


def stack(panels, path):
    W = max(p.width for p in panels)
    H = sum(p.height for p in panels) + 10 * len(panels)
    im = Image.new("RGB", (W, H), (8, 8, 10))
    y = 0
    for p in panels:
        im.paste(p, (0, y))
        y += p.height + 10
    im.save(path)


# ---------------------------------------------------------------- weather in place
def weather_scene(key, frames, pal, crop, t):
    """a few frames of weather over a field: the sprites scattered as the effect scatters them (seeded)"""
    base = crop.convert("RGBA")
    rnd = random.Random(1000 + t)
    if key == "rain":
        for i in range(14):
            x, y = rnd.randrange(-8, base.width), rnd.randrange(-24, base.height - 8)
            k = 0 if i % 4 else rnd.choice((1, 2, 3, 4, 5))
            base.alpha_composite(rgba(frames[(k + t) % len(frames) if k else 0], pal), (max(0, x), max(0, y)))
    elif key.startswith("snow"):
        for i in range(26):
            x, y = rnd.randrange(0, base.width - 8), rnd.randrange(0, base.height - 8)
            base.alpha_composite(rgba(frames[0], pal), (x, (y + t * 6) % (base.height - 8)))
    elif key.startswith("fog"):
        fogim = opaque(frames[0], pal).convert("RGBA")
        layer = Image.new("RGBA", base.size)
        for yy in range(0, base.height, 64):
            for xx in range(-64, base.width, 64):
                layer.paste(fogim, (xx + (t * 10) % 64, yy))
        a = 12 / 16.0
        b = Image.blend(base.convert("RGB"), layer.convert("RGB"), 1 - 8 / 20.0)
        return b
    return base.convert("RGB")


def weather_panel(w, van, new, crop):
    key, rel, fw, fh, n, why, live, drawer = w
    F, f2 = font(15), font(12)
    Z = 4 if fw <= 16 else 2
    parts = [("TODAY", strip(van, WEATHER, (60, 90, 70), Z))]
    if new:
        parts.append(("NEW (DRAFT)", strip(new, WEATHER, (60, 90, 70), Z)))
    scenes = []
    if live and new and key != "snow1":
        for t in range(2):
            scenes.append(("TODAY", weather_scene(key, van, WEATHER, crop, t)))
        for t in range(2):
            scenes.append(("NEW", weather_scene(key, new, WEATHER, crop, t)))
    sw = max(p.width for _, p in parts)
    W = max(sw + 16, 4 * (crop.width + 8) + 16, 900)
    H = 62 + sum(p.height + 22 for _, p in parts) + (crop.height + 26 if scenes else 0)
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "weather/%s   %dx%d x%d   [PALTAG_WEATHER, default.pal]   [%s]" % (key, fw, fh, n, "LIVE" if live else "NEVER SHOWN"),
            fill=(250, 214, 120) if live else (170, 170, 180), font=F)
    dr.text((8, 26), why, fill=(200, 200, 210), font=f2)
    dr.text((8, 42), ("indices %s; default.pal unchanged" % ",".join(map(str, [u for u in used_indices(new) if u]))) if new
            else "left as it is", fill=(140, 210, 150), font=f2)
    y = 62
    for lab, p in parts:
        dr.text((8, y), lab, fill=(200, 200, 210), font=f2)
        im.paste(p, (8, y + 16))
        y += p.height + 22
    if scenes:
        x = 8
        for lab, s in scenes:
            dr.text((x, y), lab + " (two moments)" if x == 8 or lab == "NEW" and x > 8 and scenes[2][1] is s else lab,
                    fill=(140, 210, 150) if lab == "NEW" else (200, 200, 210), font=f2)
            im.paste(s, (x, y + 16))
            x += s.width + 8
    return im


# ================================================================== the run
def status_of(rel):
    cur = open(os.path.join(GBA, rel), "rb").read() if os.path.exists(os.path.join(GBA, rel)) else None
    van = vanilla_bytes(rel)
    if cur is None:
        return "MISSING"
    if van is None:
        return "ADDED"
    return "VANILLA" if cur == van else "OURS"


def main():
    if WRITE and "--approved" not in ARGS:
        print("  --write refused: T-438 batch B is a draft until the user has approved its sheets.")
        print("  (When they have: --write --approved copies the drawn sheets into graphics/field_effects and graphics/weather,")
        print("   and general_0.pal with them; only sheets that are still vanilla are overwritten.)")
        return 0

    drawn, rows = [], []
    for e in EFFECTS:
        key, rel, fw, fh, n, kind, tag, live, why, first, drawer = e
        im = png(rel)
        if im is None:
            print("  !! %s: %s is missing" % (key, rel))
            continue
        van = frames_of(im, fw, fh, n)
        st = status_of(rel)
        new = drawer(van) if drawer else None
        if new:
            assert len(new) == n and all(len(f) == fh and len(f[0]) == fw for f in new), key
            if kind == P_PLAYER:
                assert not ({12, 13} & set(used_indices(new))), key + " uses the shoes' indices"
        rows.append((key, "%dx%d x%d" % (fw, fh, n), kind, "live" if live else "DEAD", st,
                     "drawn" if new else "ours" if st == "OURS" else "left", why))
        if new:
            drawn.append((e, van, new, im))
    print("  %-34s %-12s %-16s %-5s %-8s %-6s %s" % ("field effect", "frames", "palette", "", "today", "batch", "why / where"))
    for r in rows:
        print("  %-34s %-12s %-16s %-5s %-8s %-6s %s" % r)

    wdrawn = []
    for w in WEATHERS:
        key, rel, fw, fh, n, why, live, drawer = w
        im = png(rel)
        van = frames_of(im, fw, fh, n)
        st = status_of(rel)
        new = drawer(van) if drawer else None
        print("  %-34s %-12s %-16s %-5s %-8s %-6s %s" % ("weather/" + key, "%dx%d x%d" % (fw, fh, n), "default.pal",
                                                         "live" if live else "DEAD", st,
                                                         "drawn" if new else "ours" if st == "OURS" else "left", why))
        if new:
            wdrawn.append((w, van, new, im))
    g0_moves = [(i, a, b) for i, (a, b) in enumerate(zip(G0_CUR, G0_NEW)) if a != b]
    print("  general_0.pal: %d entries proposed to move (%s)" % (len(g0_moves), ", ".join("%d" % i for i, _, _ in g0_moves)))
    print("  examined %d field-effect sheets and %d weather sheets; %d + %d drawn" % (len(EFFECTS), len(WEATHERS), len(drawn), len(wdrawn)))

    if DRAFT:
        os.makedirs(DRAFT, exist_ok=True)
        os.makedirs(SHEETS, exist_ok=True)
        for e, van, new, im in drawn:
            key, rel, fw, fh, n, kind = e[:6]
            sheet_of(new, fw, fh, im.size, new_palette_for(key, kind, im)).save(os.path.join(DRAFT, os.path.basename(rel)))
        wdir = os.path.join(DRAFT, "weather")
        os.makedirs(wdir, exist_ok=True)
        for w, van, new, im in wdrawn:
            key, rel, fw, fh, n = w[:5]
            sheet_of(new, fw, fh, im.size, WEATHER).save(os.path.join(wdir, os.path.basename(rel)))
        lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in G0_NEW]
        open(os.path.join(DRAFT, "general_0.pal"), "wb").write(("\r\n".join(lines) + "\r\n").encode())

        names = []
        order = [e for e in EFFECTS if e[7]] + [e for e in EFFECTS if not e[7]]
        by_key = {d[0][0]: d for d in drawn}
        panels = []
        shards = [(d[0], d[1], d[2]) for d in drawn if d[0][0].startswith("deoxys")]
        for e in order:
            if e[0].startswith("deoxys"):
                if e[0] == shards[0][0][0]:
                    panels.append(shards_panel(shards))
                continue
            if e[0] in by_key:
                _, van, new, im = by_key[e[0]]
            else:
                im = png(e[1])
                if e[0] not in ("tall_grass", "jump_tall_grass"):
                    continue
                van, new = frames_of(im, e[2], e[3], e[4]), None
            panels.append(panel(e, van, new, palette_for(e[5], im), new_palette_for(e[0], e[5], im)))
        for i in range(0, len(panels), 4):
            path = os.path.join(SHEETS, "t438b_fx_%d.png" % (i // 4 + 1))
            stack(panels[i:i + 4], path)
            names.append(path)
        crop = map_image("Route1").crop((0, 2 * 16, 15 * 16, 12 * 16))
        wp = [weather_panel(w, van, new, crop) for (w, van, new, im) in wdrawn]
        for i in range(0, len(wp), 3):
            path = os.path.join(SHEETS, "t438b_weather_%d.png" % (i // 3 + 1))
            stack(wp[i:i + 3], path)
            names.append(path)
        print("  drafts in %s; sheets:\n    %s" % (DRAFT, "\n    ".join(names)))

    if WRITE:
        n = 0
        for e, van, new, im in drawn:
            key, rel, fw, fh, nf, kind = e[:6]
            if status_of(rel) != "VANILLA":
                print("  !! %s is no longer vanilla; not overwritten" % rel)
                continue
            sheet_of(new, fw, fh, im.size, new_palette_for(key, kind, im)).save(os.path.join(GBA, rel))
            n += 1
        for w, van, new, im in wdrawn:
            key, rel, fw, fh = w[:4]
            if status_of(rel) != "VANILLA":
                print("  !! %s is no longer vanilla; not overwritten" % rel)
                continue
            sheet_of(new, fw, fh, im.size, WEATHER).save(os.path.join(GBA, rel))
            n += 1
        lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in G0_NEW]
        open(os.path.join(GBA, FX, "palettes/general_0.pal"), "wb").write(("\r\n".join(lines) + "\r\n").encode())
        print("  written: %d sheets and general_0.pal into the engine" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())

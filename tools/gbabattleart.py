#!/usr/bin/env python3
"""T-527: THE BATTLE BACKGROUNDS, DRAWN AGAIN -- the nine terrains and their entry strips, in our own hand.

    python3 tools/gbabattleart.py                      # report: every terrain, what it is made of, its budgets, the
                                                       #   run-time contract, and whether each draft keeps it
    python3 tools/gbabattleart.py --draft [DIR]        # draw both directions into DIR (gfx/drafts/t527_battle_bg/):
                                                       #   terrain.png/.bin/.pal and anim.png/.bin per terrain per
                                                       #   direction, the contact sheet and the calendar sheet
    python3 tools/gbabattleart.py --write --approved --pick grass=A cave=B ...
                                                       # write the picked drafts into the engine. Refuses without
                                                       #   --approved, and refuses a terrain APPROVED does not name.
    python3 tools/gbabattleart.py --write --approved --all   # every pick APPROVED holds (check_generators runs this)
    python3 tools/gbabattleart.py --approved           # report, and exit 1 if the engine is not what that write makes

DRAFT, 2026-11-07 (the user picked "Battle backgrounds" from the vanilla-art census, gap 2). Every pixel is drawn in
code or taken from OUR map tilesets (the T-438 ground, the cave, the beach, the sea's bits, the house) as the maps
render them -- no AI image, nothing of Nintendo's. Nothing is written into the engine until the user picks.

THE TWO DIRECTIONS
  A  OUR PLACE    the scene from our own tiles: Route 1's trees on the horizon and its tall grass on the platforms, the
                  beach and the sea's bits, MT. EMBER's rock, MT. MOON's wall, the house's floor and its rug.
  B  QUIET FIELD  a calm sky, a low hint of the place on the horizon, plain ground with faint scan lines (the
                  Readout's), flat platforms with a few marks of the place. Low chroma, so the daemons carry the colour.

WHAT THE ENGINE DOES WITH A TERRAIN, AND WHAT EVERY DRAFT KEEPS (battle_bg.c, daemons_battle_bg.c,
daemons_weather.c, daemons_pulse.c, battle_anim.c, evolution_scene.c)
  SHAPE     one tileset (BG char 2), one 32x64 map (screen 26), three BG palette rows 2-4, loaded whole. Visible rows
            0-13 (y 0-111); rows 14-29 sit under the message box (tile 0, palette 0); rows 30-31 the field; rows 32-63
            a second screen, the backdrop without platforms (move animations and the evolution scene scroll to it).
            The entry strip: its own tiles (BG char 1) and a 32x14 map in palette 4, scrolled sideways at the intro,
            so it is drawn 256 wide and wraps.
  PLATFORMS the foe's at x 112-239, y 48-79 (row 2); the player's at x 0-127 from y 101, cut by the box (row 3). The
            battlers' positions are fixed in code, so the ellipses stay exactly there.
  T-481 A   (the calendar, after the palette loads) measures the ART, so every draft must still give it:
            - a FIELD: a pixel row of row 2's colour 15 from edge to edge (the first one is the field's top);
            - a HORIZON: one tile row above the field drawn by ONE unflipped tile in row 2, with a whole pixel row of
              colour 1, the tile drawn nowhere else (both screens) -- the weekday's line is patched into it (1 -> 12)
              and its row moved to palette row 3, so every other colour it draws must read the same in row 3;
            - row 3's 10-14 drawn by NO row-3 tile (12 is the weekday's trim; the rest are copied from row 2);
            - SKY: the row-2 colours drawn only above the field, at most six -- the hour steps them toward rose,
              amber or navy, so on an outdoor terrain nothing but sky may use them (a far sea or haze may);
            - each platform's GLINT, its brightest colour drawn on at most a fifth of it: a holiday paints it the
              month's colour and spring's bloom takes it -- so the glint is a sparse highlight on the platforms only.
            Its season tables, horizon and glints are generated from the art (gbabattlebg.py --write --approved), so
            a new drawing needs that run straight after; this tool's --write runs it.
  T-415     the weather's wash blends rows 2-4 toward the sky's colour: no slot constraint.
  T-482     the witching hour breathes rows 2-4 red to blue: no slot constraint.
  HALFTONE  greys rows 2-4: every draft keeps its platforms apart from the field in value, not hue alone.
  ROOMS     BUILDING's drawing is shared by PLAIN (outdoor trainer battles off the grass, and the evolution scene),
            LINK, the gyms, the leaders and the eight BENCHMARK arenas, and indoor/'s copy by INDOOR_1/2 and the Elite
            rooms -- 20 palettes this does not own. So the building drafts keep vanilla's ROLES: 2 the platform's
            fill, 3 its rim, 5 its inner ring, 4 its top and bottom, 6-9 small marks; 10-14 the wall in horizontal
            bands only (they are PLAIN's sky); 15 the floor, 1 its seams (PLAIN's field and scan lines).
  CAMOUFLAGE (battle_anim_utility_funcs.c) tints a battler by terrain with fixed colours; the art does not touch it.

THE COST: EWRAM 0, IWRAM 0, SAVE 0. ROM: each draft holds its terrain's vanilla tile budget (the PNG's size).
"""
import argparse, importlib.util, math, os, random, shutil, struct, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
GBA = os.path.join(ROOT, "engineGba")
TERR = os.path.join(GBA, "graphics/battle_terrain")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t527_battle_bg")
SETS = ("grass", "longgrass", "sand", "underwater", "water", "pond", "mountain", "cave", "building")
DIRS = ("A", "B")
# after the drafts were looked at: A wherever the place is ours to show; B for the building drawing, which PLAIN
# (most trainer battles off the grass, and the evolution scene) wears outdoors, where A's rug reads as a target
RECOMMENDED = {"grass": "A", "longgrass": "A", "sand": "A", "underwater": "B", "water": "A", "pond": "A",
               "mountain": "A", "cave": "A", "building": "B"}
# the user, 2026-11-07: "A outdoors, B indoors" -- the recommendation, every terrain
APPROVED = {"grass": "A", "longgrass": "A", "sand": "A", "water": "A", "pond": "A", "mountain": "A", "cave": "A",
            "building": "B", "underwater": "B"}

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
ap.add_argument("--pick", nargs="*", default=[])
ap.add_argument("--all", action="store_true", help="--pick every terrain APPROVED names")
ap.add_argument("--over-later-work", action="store_true", help="accepted so check_generators --writes really runs the write")
A = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(TOOLS, name + ".py"))
    argv, sys.argv = sys.argv, sys.argv[:1]
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, TOOLS)
    spec.loader.exec_module(mod)
    sys.argv = argv
    return mod


BG = _load("gbabattlebg")        # T-481's measure of a terrain, and its calendar, as the cartridge does them
W, H = 256, 112                  # the drawn width (the map is 32 tiles; 240 are seen) and the seen height
FOE = (176, 64, 64, 16)          # cx, cy, rx, ry -- measured off vanilla (x 112-239, y 48-79)
ME = (64, 117, 64, 16)           # the player's: x 0-127 from y 101, its lower half under the box
HORIZON_ROW = 3                  # tile row 3 (y 24-31): line 5 the scan line the weekday takes, 6-7 the field
FIELD_TOP = 30


# ============================================================================================ our tiles, as the maps draw them
_MAPS = {}


def map_render(name):
    if name not in _MAPS:
        R = _load("reviewsheet")
        _MAPS[name] = R.render(R.layout_of(name))
    return _MAPS[name]


MATERIAL = {   # (map, box): every crop is 16px-aligned -- our metatiles, as the overworld shows them
    "tree":       ("Route1", (64, 112, 96, 144)),
    "forest":     ("Route1", (0, 96, 32, 128)),
    "tall":       ("Route1", (160, 96, 176, 112)),
    "plain":      ("Route1", (48, 144, 64, 160)),
    "pond":       ("Route1", (64, 192, 128, 240)),
    "sand":       ("OneIsland_TreasureBeach", (128, 304, 160, 336)),
    "sea":        ("OneIsland_TreasureBeach", (0, 240, 32, 272)),
    "searock":    ("OneIsland_TreasureBeach", (32, 256, 64, 288)),
    "beachgrass": ("OneIsland_TreasureBeach", (96, 368, 128, 400)),
    "wall":       ("MtMoon_1F", (160, 0, 224, 32)),
    "floor":      ("MtMoon_1F", (160, 64, 192, 96)),
    "lfloor":     ("MtMoon_1F", (304, 48, 336, 80)),
    "boulders":   ("MtMoon_1F", (192, 32, 224, 64)),
    "cliff":      ("MtEmber_Exterior", (240, 316, 304, 348)),
    "dirt":       ("MtEmber_Exterior", (208, 444, 224, 460)),
    "hfloor":     ("PalletTown_PlayersHouse_1F", (48, 96, 96, 128)),
    "hwall":      ("PalletTown_PlayersHouse_1F", (0, 0, 64, 32)),
    "rug":        ("PalletTown_PlayersHouse_1F", (96, 40, 176, 80)),
}


def material(key):
    m, box = MATERIAL[key]
    im = map_render(m).crop(box).convert("RGB")
    return [[tuple(v >> 3 for v in im.getpixel((x, y))) for x in range(im.width)] for y in range(im.height)]


def lum(c):
    return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def quant(keys, n):
    """n colours of our materials, dark to light (median cut on the five-bit colours the GBA shows)."""
    px = [c for k in keys for row in material(k) for c in row]
    im = Image.new("RGB", (len(px), 1))
    im.putdata([tuple(v << 3 for v in c) for c in px])
    q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:3 * n]
    cols = sorted({tuple(pal[3 * i + k] >> 3 for k in range(3)) for i in range(n)}, key=lum)
    return cols


def nearest(c, choices):
    """the slot whose colour is nearest c, weighted toward value so a shape keeps its light and shade"""
    return min(choices, key=lambda sc: 3 * (lum(c) - lum(sc[1])) ** 2 + sum((a - b) ** 2 for a, b in zip(c, sc[1])))[0]


def slotted(key, choices, key_out=None, tol=0):
    """a material as slots, -1 where it matches key_out (another material's colours: the ground round a tree)"""
    out = []
    keyset = set()
    if key_out:
        keyset = {c for row in material(key_out) for c in row}
    for row in material(key):
        r = []
        for c in row:
            if c in keyset or (tol and any(sum(abs(a - b) for a, b in zip(c, k)) <= tol for k in keyset)):
                r.append(-1)
            else:
                r.append(nearest(c, choices))
        out.append(r)
    return out


# ================================================================================================ colour
def hsv_adj(c, s=1.0, v=1.0, v_to=None, k=0.0, hue=0.0):
    import colorsys
    h, ss, vv = colorsys.rgb_to_hsv(*(x / 31 for x in c))
    ss *= s
    vv *= v
    if v_to is not None:
        vv += (v_to - vv) * k
    r = colorsys.hsv_to_rgb((h + hue / 360) % 1, max(0, min(1, ss)), max(0, min(1, vv)))
    return tuple(min(31, max(0, round(x * 31))) for x in r)


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


MAGENTA = (31, 0, 31)


# ================================================================================================ the canvas
class Canvas:
    def __init__(self, fill=15):
        self.px = [[fill] * W for _ in range(H)]

    def put(self, x, y, v):
        if 0 <= x < W and 0 <= y < H and v is not None and v >= 0:
            self.px[y][x] = v

    def stamp(self, art, x0, y0, wrap=True):
        for y, row in enumerate(art):
            for x, v in enumerate(row):
                if v >= 0:
                    self.put((x0 + x) % W if wrap else x0 + x, y0 + y, v)

    def copy(self):
        c = Canvas()
        c.px = [r[:] for r in self.px]
        return c


def sky(cv, bands, top=0, bottom=24, dither=True):
    """horizontal bands, top to bottom, each change a two-row checker -- every tile row stays one tile across"""
    n = len(bands)
    span = bottom - top
    for y in range(top, bottom):
        f = (y - top) / span * n
        i = min(n - 1, int(f))
        nxt = min(n - 1, i + 1)
        frac = f - i
        for x in range(W):
            v = bands[i]
            if dither and frac > 0.75 and (x + y) % 2 == 0:
                v = bands[nxt]
            cv.px[y][x] = v


def horizon(cv, fill, line=1, field=15):
    """tile row 3: the backdrop's last band (fill), the line the weekday takes (y 29), then the field"""
    for y in range(24, 32):
        ly = y - 24
        for x in range(W):
            cv.px[y][x] = fill if ly < 5 else (line if ly == 5 else field)


def field(cv, scan=1, every=4, phase=0, top=32, fill=15, rows=None):
    for y in range(top, H):
        for x in range(W):
            cv.px[y][x] = scan if scan is not None and (y - top) % every == phase else fill
    if rows:
        for y, v in rows.items():
            for x in range(W):
                cv.px[y][x] = v


def ell(E, x, y):
    cx, cy, rx, ry = E
    dx, dy = (x + 0.5 - cx), (y + 0.5 - cy)
    r = (dx / rx) ** 2 + (dy / ry) ** 2
    g = math.hypot(2 * dx / rx ** 2, 2 * dy / ry ** 2) or 1e-6
    return r, (1 - r) / g, dy          # inside if r <= 1; d = distance in from the edge (px); dy < 0 the top half


def mirror_x(E, x):
    cx = E[0]
    return x if x >= cx else 2 * cx - 1 - x


def platform(cv, E, tex, rim, lip=None, light=None, marks=None, tips=None, lip_w=2.5, mirror=True):
    """an ellipse at E: tex(x, y) inside, a 1px rim, a darker lip on its lower half, a 1px light on its upper edge;
    marks(x, y) -> slot or None scattered over it; tips(xm) -> how far a blade rises above the top edge at xm."""
    cx, cy, rx, ry = E
    for y in range(max(0, cy - ry - 8), min(H, cy + ry + 1)):
        for x in range(max(0, cx - rx - 1), min(W, cx + rx + 1)):
            xm = mirror_x(E, x) if mirror else x
            r, d, dy = ell(E, xm, y)
            if r > 1:
                continue
            v = tex(xm, y)
            if light is not None and dy < 0 and 1.0 <= d < 2.0:
                v = light
            if lip is not None and dy > 0 and d < lip_w:
                v = lip
            if d < 1.0:
                v = rim
            if marks:
                mk = marks(xm, y, d)
                if mk is not None:
                    v = mk
            cv.put(x, y, v)
    if tips:
        for x in range(max(0, cx - rx), min(W, cx + rx)):
            xm = mirror_x(E, x) if mirror else x
            # the top edge at this column
            t = (xm + 0.5 - cx) / rx
            if abs(t) >= 1:
                continue
            ytop = cy - ry * math.sqrt(1 - t * t)
            got = tips(xm, ytop)
            if not got:
                continue
            hgt, slot = got
            for k in range(1, hgt + 1):
                cv.put(x, int(ytop) - k + 1, slot)


def hashr(*a):
    h = 2166136261
    for v in a:
        h = (h ^ (v & 0xFFFFFFFF)) * 16777619 & 0xFFFFFFFF
    return h


# ================================================================================================ the nine, both ways
def P(row2, row4=None):
    """48 colours: row 2 as given (16), row 3 the same (its 10-14 the copies vanilla keeps), row 4 the strip's"""
    r2 = [c if c is not None else MAGENTA for c in row2]
    r4 = [c if c is not None else (0, 0, 0) for c in (row4 or [None] * 16)]
    r4[0] = (0, 0, 0)
    return r2 + list(r2) + r4


def ground_slots(cols):
    """slots 2-8 for seven ground colours, dark to light"""
    return [(2 + i, c) for i, c in enumerate(cols)]


def outdoor_sky_A():
    # our sky: the sea's blue lifted (TREASURE BEACH's water, from the top down to the haze at the horizon)
    sea = quant(["sea"], 4)[2]
    top = hsv_adj(sea, s=0.55, v=1.0, v_to=0.98, k=0.75)
    low = (30, 31, 30)
    return [mix(top, low, t) for t in (0.0, 0.3, 0.55, 0.8, 1.0)]


def quiet(c, s=0.42, v_to=0.86, k=0.45):
    return hsv_adj(c, s=s, v_to=v_to, k=k)


def strip_canvas():
    return Canvas(fill=0)


def settle(cv, bd, pal, outdoor):
    """T-481 steps every row-2 colour drawn only above the field as SKY. Outdoors a ground colour (2-9) the scenery
    draws but no platform does would go navy at night with the sky: give it the nearest colour the ground also has."""
    if not outdoor:
        return
    below = {v for y in range(FIELD_TOP, H) for v in cv.px[y][:240]}
    above = {v for y in range(FIELD_TOP) for v in cv.px[y][:240]}
    for v in sorted(above - below):
        if not 2 <= v <= 9:
            continue
        to = min((u for u in below if 2 <= u <= 9), key=lambda u: sum((a - b) ** 2 for a, b in zip(pal[u], pal[v])))
        for c in (cv, bd):
            for y in range(FIELD_TOP):
                c.px[y] = [to if q == v else q for q in c.px[y]]


def treeline(cv, GS, period=64):
    """Route 1's tree, its crown keyed off the grass it stands on: a back rank, darker, and a front rank between,
    every 32px with a gap in each 64 -- sky above, the hedge's shade at the foot (y 21-23)"""
    greens = [(v, c) for v, c in GS if c[1] >= c[0] and c[1] >= c[2]] or GS
    tree = slotted("tree", greens, key_out="plain", tol=2)
    # the crown is round: keep what lies inside it, so the sky shows between the trees
    tree = [[(v if ((x - 15.5) / 16.5) ** 2 + ((y - 11.5) / 12) ** 2 <= 1 else -1) for x, v in enumerate(row)]
            for y, row in enumerate(tree)]
    order = [v for v, c in sorted(greens, key=lambda vc: lum(vc[1]))]
    darker = {v: order[max(0, order.index(v) - 2)] for v in order}
    back = [[(darker.get(v, v) if v >= 0 else -1) for v in row] for row in tree]
    for x0 in range(0, W, period):
        cv.stamp([r for r in back[:24]], x0 + 4, 3)
        cv.stamp([r for r in back[:24]], x0 + 38, 6)
        cv.stamp([r for r in tree[:16]], x0 + 20, 9)
        cv.stamp([r for r in tree[:13]], x0 + 52, 12)
    for x in range(W):
        for y in range(21, 24):
            if cv.px[y][x] >= 10 or y == 23:
                cv.px[y][x] = order[0]


def dash(x, y, base, mark, cell=16):
    """B's ground: the fill, and in each 16x8 cell one short level mark (a ripple, a tuft, a seam) -- a hint, no more"""
    h = hashr(x // cell, y // 8, 527)
    yy, x0, ln = 2 + h % 4, h % (cell - 5), 3 + (h >> 4) % 3
    return mark if (y % 8 == yy and x0 <= x % cell < x0 + ln and (h >> 8) % 3) else base


def slot_near(GS, c):
    return min(GS, key=lambda vc: sum((a - b) ** 2 for a, b in zip(vc[1], c)))[0]


def scene(name, d):
    """(canvas with platforms, backdrop canvas, 48 colours, strip canvas) for one terrain and direction"""
    cv, bd, pal, st = globals()["scene_" + name](d)
    settle(cv, bd, pal, name not in ("cave", "building"))
    return cv, bd, pal, st


# ---- GRASS: Route 1 -------------------------------------------------------------------------------------------------
def grass_cols(d, deep=False):
    g = quant(["tall", "tree", "forest"], 7)
    if deep:
        g = [hsv_adj(c, s=1.05, v=0.9) for c in g]
    if d == "B":
        g = [quiet(c) for c in g]
    return g


def scene_grass(d, deep=False):
    g = grass_cols(d, deep)
    GS = ground_slots(g)
    plain = quant(["plain"], 2)
    fieldc = plain[-1] if d == "A" else quiet(plain[-1], s=0.35, v_to=0.88, k=0.5)
    scanc = mix(fieldc, g[3], 0.25 if d == "A" else 0.12)
    skyc = outdoor_sky_A() if d == "A" else [quiet(c, s=0.5, v_to=0.95, k=0.6) for c in outdoor_sky_A()]
    glint = hsv_adj(g[-1], s=0.5, v_to=1.0, k=0.6)
    row2 = [None, scanc] + g + [glint] + skyc + [fieldc]
    cv = Canvas()
    if d == "A":
        sky(cv, [10, 11, 12, 13], 0, 24)
        # the treeline: Route 1's tree, its crown keyed off the grass it stands on, every 32px, a second rank behind
        treeline(cv, GS)
        horizon(cv, 2)
        field(cv)
    else:
        sky(cv, [10, 11, 12, 13], 0, 24)
        # a hint: a low, soft treeline in the haze (slot 14, a sky colour -- it goes with the hour)
        for x in range(W):
            hh = 3 + int(2 * math.sin(x / 9.0) + 1.5 * math.sin(x / 4.1 + 1))
            for y in range(24 - max(1, hh), 24):
                cv.px[y][x] = 14
        horizon(cv, 14)
        field(cv, every=8)
    bd = cv.copy()
    tall = slotted("tall", GS)

    def tex(x, y):
        if d == "A":
            return tall[y % 16][x % 16]
        return dash(x, y, 6, 5)

    def marks(x, y, dd):
        if dd < 2:
            return None
        if d == "A":
            h = hashr(x // 12, y // 6)
            if h % 11 == 0 and (x % 12, y % 6) == (h % 9 + 1, 2):
                return 9
            return None
        h = hashr(x // 10, y // 5)
        if h % 5 == 0 and x % 10 == h % 7 and y % 5 == 2:
            return 9 if h % 3 == 0 else 4
        return None

    def tips(xm, ytop):
        if d == "A":
            k = (xm // 3) % 5
            return ((3, 4, 2, 5, 3)[k] + (2 if deep else 0), 3 if k % 2 else 2) if xm % 3 != 2 else None
        return (1, 4) if xm % 9 == 0 else None

    for E in (FOE, ME):
        platform(cv, E, tex, rim=2, lip=3, light=7 if d == "A" else 7, marks=marks, tips=tips)
    # the strip: Route 1's tall grass, as blades
    st = strip_canvas()
    g4 = [None, g[2], g[4], g[5], g[6], g[3]] + [None] * 10
    if d == "A":
        # Route 1's tall grass itself, stacked into a wall of it, its tips cut ragged (a 32px repeat)
        S4 = [(1, g[2]), (2, g[4]), (3, g[5]), (4, g[6]), (5, g[3])]
        tall4 = slotted("tall", S4)
        hmax = 44 if deep else 34
        for x in range(W):
            k = x % 32
            top = 112 - hmax + (hashr(k // 2, 5) % 12) + (0 if k % 2 else 2)
            for y in range(top, 112):
                st.put(x, y, tall4[y % 16][x % 16] if y > top + 1 else 4)
    else:
        for x in range(W):
            hh = 14 + int(6 * math.sin(x / 7.0) + 4 * math.sin(x / 3.3))
            for y in range(112 - hh, 112):
                st.put(x, y, 2 if y > 112 - hh + 2 else 3)
    return cv, bd, P(row2, g4), st


def scene_longgrass(d):
    return scene_grass(d, deep=True)


# ---- SAND: TREASURE BEACH -------------------------------------------------------------------------------------------
def scene_sand(d):
    sq = quant(["sand"], 5)[1:]
    bgq = quant(["beachgrass"], 5)
    s = sorted([hsv_adj(sq[0], v=0.66), hsv_adj(sq[0], v=0.8), bgq[1]] + sq, key=lum)
    if d == "B":
        s = [quiet(c, s=0.45) for c in s]
    GS = ground_slots(s)
    sandc = [hsv_adj(sq[0], v=0.66), hsv_adj(sq[0], v=0.8), sq[3]]
    fieldc = mix(sq[1], sq[0], 0.5) if d == "A" else quiet(mix(sq[0], s[1], 0.35), s=0.4, v_to=0.78, k=0.4)
    scanc = mix(fieldc, sandc[0], 0.35 if d == "A" else 0.15)
    sk = outdoor_sky_A()
    sea = quant(["sea"], 4)
    if d == "A":
        skyc = sk[:3] + [hsv_adj(sea[2], s=0.85, v=1.05), hsv_adj(sea[3], s=0.6, v_to=1, k=0.3)]
    else:
        skyc = [quiet(c, s=0.5, v_to=0.95, k=0.6) for c in sk[:3]] + [quiet(sea[2], s=0.4, v_to=0.8, k=0.4),
                                                                       quiet(sea[3], s=0.3, v_to=0.9, k=0.5)]
    glint = (31, 31, 28)
    row2 = [None, scanc] + s + [glint] + skyc + [fieldc]
    cv = Canvas()
    sky(cv, [10, 11, 12], 0, 16)
    # the sea at the horizon: TREASURE BEACH's water, its bits (0 and 1) kept as the lighter slot
    seat = material("sea")
    for y in range(16, 24):
        for x in range(W):
            c = seat[(y - 16) % 32][x % 32]
            cv.px[y][x] = 14 if (d == "A" and lum(c) > lum(sea[2]) + 2) or (y == 16) else 13
    horizon(cv, 13 if d == "A" else 13)
    for y in range(24, 29):
        for x in range(W):
            if y >= 27:
                cv.px[y][x] = 8 if d == "A" else 13     # the wet sand's edge
    field(cv, every=4 if d == "A" else 8)
    bd = cv.copy()
    sand = slotted("sand", GS)

    def tex(x, y):
        if d == "A":
            return min(8, sand[y % 32][x % 32] + 1)
        return dash(x, y, 7, 6)

    def marks(x, y, dd):
        if dd < 2:
            return None
        h = hashr(x // 14, y // 7)
        if h % 6 == 0 and x % 14 == h % 11 and y % 7 == 3:
            return 9
        if d == "A" and h % 6 == 1 and x % 14 in (h % 11, h % 11 + 1) and y % 7 == 4:
            return 3
        return None

    for E in (FOE, ME):
        platform(cv, E, tex, rim=slot_near(GS, sandc[0]), lip=slot_near(GS, mix(sandc[0], sandc[1], .5)), light=8,
                 marks=marks, lip_w=3.5)
    # the strip: a dune's crest, and its blown sand
    st = strip_canvas()
    s4 = [None, sq[1], hsv_adj(sq[0], v=0.8), sq[2], sq[3]] + [None] * 11
    if d == "B":
        s4 = [None] + [quiet(c, s=0.45) for c in s4[1:5]] + [None] * 11
    for x in range(W):
        k = x % 64
        hh = 18 + int(8 * math.sin(k * 2 * math.pi / 64) + 4 * math.sin(k * 2 * math.pi / 32 + 1))
        for y in range(112 - hh, 112):
            j = y - (112 - hh)
            st.put(x, y, 4 if j < 2 else (3 if j < 6 else (2 if j < 14 or (k // 4 + y // 3) % 7 else 1)))
        if d == "A" and hashr(k, 9) % 7 == 0:
            st.put(x, 112 - hh - 4 - hashr(k) % 10, 4)
    return cv, bd, P(row2, s4), st


# ---- WATER: the sea, and its bits -------------------------------------------------------------------------------------
def water_cols(d):
    w = quant(["sea", "searock"], 7)
    if d == "B":
        w = [quiet(c, s=0.45, v_to=0.8, k=0.35) for c in w]
    return w


def bits_tex(GS, key="sea"):
    return slotted(key, GS)


def scene_water(d):
    w = water_cols(d)
    GS = ground_slots(w)
    sea = quant(["sea"], 4)
    fieldc = hsv_adj(sea[2], s=0.55, v_to=0.95, k=0.55) if d == "A" else quiet(sea[2], s=0.3, v_to=0.9, k=0.6)
    scanc = mix(fieldc, (31, 31, 31), 0.45 if d == "A" else 0.25)
    sk = outdoor_sky_A() if d == "A" else [quiet(c, s=0.5, v_to=0.95, k=0.6) for c in outdoor_sky_A()]
    skyc = sk[:4] + [hsv_adj(sea[1], s=0.7, v_to=0.8, k=0.4) if d == "A" else quiet(sea[1], s=0.35, v_to=0.75, k=0.5)]
    glint = (31, 31, 31)
    row2 = [None, scanc] + w + [glint] + skyc + [fieldc]
    cv = Canvas()
    sky(cv, [10, 11, 12, 13], 0, 20)
    for y in range(20, 24):
        for x in range(W):
            cv.px[y][x] = 14
    horizon(cv, 14)
    field(cv, every=4)
    if d == "A":
        for y in range(34, H, 8):               # the swell: a broken light line every eight rows, our bits between
            for x in range(W):
                if (x // 6 + y // 8) % 3 == 0:
                    cv.px[y][x] = 1
    bd = cv.copy()
    bits = bits_tex(GS)

    def tex(x, y):
        if d == "A":
            return bits[y % 32][x % 32]
        return dash(x, y, 5, 6)

    def marks(x, y, dd):
        if dd < 2:
            return None
        h = hashr(x // 9, y // 5)
        if h % 7 == 0 and x % 9 in (h % 6, h % 6 + 1) and y % 5 == 2:
            return 9
        return None

    def tips(xm, ytop):                           # the wave's crest on the rim
        return (2, 8) if (xm // 4) % 3 == 0 and d == "A" else None

    for E in (FOE, ME):
        platform(cv, E, tex, rim=3, lip=2, light=8, marks=marks, tips=tips)
    st = strip_canvas()
    w4 = [None, w[1], w[3], w[5], w[6], (31, 31, 31)] + [None] * 10
    for x in range(W):
        k = x % 64
        ph = k * 2 * math.pi / 64
        hh = 22 + int(10 * math.sin(ph) + 4 * math.sin(2 * ph + 1))
        for y in range(112 - hh, 112):
            j = y - (112 - hh)
            st.put(x, y, 5 if j < 2 else (4 if j < 5 else (3 if j < 14 else 2 if (y // 4 + k // 8) % 4 else 1)))
        if d == "A" and math.sin(ph) > 0.8 and hashr(k) % 3 == 0:
            st.put(x, 112 - hh - 2 - hashr(k, 1) % 5, 5)
    return cv, bd, P(row2, w4), st


# ---- POND: Route 1's pond, in the grass ------------------------------------------------------------------------------
def scene_pond(d):
    p = quant(["pond"], 4)
    gcol = quant(["plain", "tall"], 2)
    cols = sorted(p + quant(["tree"], 3), key=lum)
    if d == "B":
        cols = [quiet(c, s=0.45, v_to=0.82, k=0.35) for c in cols]
    GS = ground_slots(cols)
    plain = quant(["plain"], 2)
    fieldc = plain[-1] if d == "A" else quiet(plain[-1], s=0.35, v_to=0.88, k=0.5)
    scanc = mix(fieldc, gcol[0], 0.25 if d == "A" else 0.12)
    skyc = outdoor_sky_A() if d == "A" else [quiet(c, s=0.5, v_to=0.95, k=0.6) for c in outdoor_sky_A()]
    row2 = [None, scanc] + cols + [(31, 31, 31)] + skyc + [fieldc]
    cv = Canvas()
    sky(cv, [10, 11, 12, 13], 0, 24)
    if d == "A":
        # the far bank: Route 1's trees, as round its pond
        treeline(cv, GS)
        horizon(cv, 2)
    else:
        for x in range(W):
            hh = 2 + int(1.5 * math.sin(x / 11.0) + math.sin(x / 5.0))
            for y in range(24 - max(1, hh), 24):
                cv.px[y][x] = 14
        horizon(cv, 14)
    field(cv, every=4 if d == "A" else 8)
    bd = cv.copy()
    pond = slotted("pond", GS)

    def tex(x, y):
        if d == "A":
            return pond[16 + (y % 16)][16 + (x % 32)]
        return dash(x, y, 5, 6)

    def marks(x, y, dd):
        if dd < 3.0 and d == "A":
            return pond[2 + int(dd)][24 + x % 16] if dd >= 1 else None
        h = hashr(x // 8, y // 5)
        if dd >= 2 and h % 6 == 0 and x % 8 == h % 5 and y % 5 == 2:
            return 9
        return None

    earth = slot_near(GS, (14, 8, 8))
    gdark = slot_near(GS, quant(["tree"], 3)[0])
    gmid = slot_near(GS, quant(["tree"], 3)[1])
    glight = slot_near(GS, quant(["tree"], 3)[2])

    def tips(xm, ytop):                          # the grass at the pond's far edge
        tone = (gdark, gmid, glight)[(xm // 3) % 3]
        return ((2 + (xm // 3) % 3, tone) if xm % 3 == 0 else None) if d == "A" else None

    for E in (FOE, ME):
        platform(cv, E, tex, rim=earth, lip=earth, light=None, marks=marks, tips=tips)
    st = strip_canvas()
    p4 = [None, cols[1], cols[3], cols[4], cols[6], (31, 31, 31)] + [None] * 10
    for x in range(W):                            # ripples, rising: rings of the pond's light
        for k in range(4):
            q = x % 32
            y = 104 - k * 9 - int(2 * math.sin(q * 2 * math.pi / 32 + k))
            if (q // 8 + k) % 3 != 0:
                st.put(x, y, 4 if k % 2 else 3)
                if d == "A":
                    st.put(x, y + 1, 2)
    for x in range(W):
        for y in range(108, 112):
            st.put(x, y, 1)
    return cv, bd, P(row2, p4), st


# ---- UNDERWATER: below the sea -----------------------------------------------------------------------------------------
def scene_underwater(d):
    top = quant(["sea"], 4)
    rockc = quant(["searock"], 4)
    sand = quant(["sand"], 3)
    # the floor's ramp: the sea rock's darks, then the sand as it looks under water (toward the sea's blue)
    cols = [hsv_adj(rockc[0], v=0.8), rockc[0], rockc[1]] + [mix(c, top[1], 0.45) for c in sand] + [mix(sand[2], top[3], 0.3)]
    if d == "B":
        cols = [quiet(c, s=0.4, v_to=0.6, k=0.35) for c in cols]
    GS = ground_slots(cols)
    fieldc = mix(cols[3], top[0], 0.35)
    scanc = mix(fieldc, cols[1], 0.3)
    skyc = [hsv_adj(top[3], s=0.8), top[2], mix(top[2], top[1], 0.5), top[1], mix(top[1], top[0], 0.5)]
    if d == "B":
        skyc = [quiet(c, s=0.45, v_to=0.6, k=0.4) for c in skyc]
        fieldc, scanc = quiet(fieldc, s=0.4, v_to=0.42, k=0.4), quiet(scanc, s=0.4, v_to=0.38, k=0.4)
    row2 = [None, scanc] + cols + [(31, 31, 31)] + skyc + [fieldc]
    cv = Canvas()
    sky(cv, [10, 11, 12, 13], 0, 24)
    if d == "A":
        # light from above, through our water: its bits (0 and 1), faint, in the upper bands
        seat = material("sea")
        for y in range(0, 14):
            for x in range(W):
                if lum(seat[y % 32][x % 32]) > lum(top[3]) + 1:
                    cv.px[y][x] = 10 if y > 2 else 11
    for x in range(W):
        k = x % 64
        hh = 3 + int(2 * math.sin(k * 2 * math.pi / 64) + 1.5 * math.sin(k * 2 * math.pi / 16))
        for y in range(24 - max(1, hh), 24):
            cv.px[y][x] = 14
    horizon(cv, 14)
    field(cv, every=4 if d == "A" else 8)
    bd = cv.copy()
    rock = slotted("searock", GS)
    sandt = slotted("sand", GS)

    def tex(x, y):
        if d == "A":
            return min(8, max(5, sandt[y % 32][x % 32] + 3))
        return dash(x, y, 6, 5)

    def marks(x, y, dd):
        if d == "A" and dd < 4 and (x // 16) % 3 == 1 and y > (FOE[1] if y < 90 else ME[1]) - 2:
            v = rock[16 + (y % 16)][16 + (x % 16)]      # TREASURE BEACH's sea rock, at the platform's foot
            return v if v <= 4 else None
        if dd < 2:
            return None
        h = hashr(x // 10, y // 6)
        if h % 7 == 0 and x % 10 == h % 9 and y % 6 == 2:
            return 9
        return None

    for E in (FOE, ME):
        platform(cv, E, tex, rim=2, lip=3, light=8, marks=marks)
    st = strip_canvas()
    u4 = [None, cols[4], top[3], (31, 31, 31), (24, 30, 31)] + [None] * 11
    rng = random.Random(527)
    pattern = [(rng.randrange(64), rng.randrange(10, 104), rng.choice((2, 3, 3, 4, 5))) for _ in range(7 if d == "A" else 5)]
    for x0 in range(0, W, 64):                    # bubbles, rising (a 64px pattern, so the strip holds its budget)
        for bx, by, r in pattern:
            for yy in range(-r, r + 1):
                for xx in range(-r, r + 1):
                    q = xx * xx + yy * yy
                    if q <= r * r:
                        v = 2 if q >= (r - 1) * (r - 1) and r > 1 else 1
                        if xx == -(r // 2) and yy == -(r // 2) and r > 1:
                            v = 3
                        st.put((x0 + bx + xx) % W, by + yy, v)
    return cv, bd, P(row2, u4), st


# ---- MOUNTAIN: MT. EMBER ------------------------------------------------------------------------------------------------
def scene_mountain(d):
    r = quant(["cliff", "dirt"], 7)
    if d == "B":
        r = [quiet(c, s=0.45, v_to=0.75, k=0.3) for c in r]
    GS = ground_slots(r)
    dirt = quant(["dirt"], 3)
    fieldc = dirt[-1] if d == "A" else quiet(dirt[-1], s=0.4, v_to=0.88, k=0.4)
    scanc = mix(fieldc, dirt[0], 0.3 if d == "A" else 0.12)
    skyc = outdoor_sky_A() if d == "A" else [quiet(c, s=0.5, v_to=0.95, k=0.6) for c in outdoor_sky_A()]
    row2 = [None, scanc] + r + [(31, 31, 29)] + skyc + [fieldc]
    cv = Canvas()
    sky(cv, [10, 11, 12, 13], 0, 24)
    cliff = slotted("cliff", GS)
    if d == "A":
        # the ridge: MT. EMBER's cliff face, cut along a skyline that rises and falls every 64px
        for x in range(W):
            top = 6 + int(5 * math.sin(x * 2 * math.pi / 64) + 3 * math.sin(x * 2 * math.pi / 32 + 2))
            for y in range(top, 24):
                cv.px[y][x] = cliff[(y - top) % 32][x % 64] if y > top else 2
        horizon(cv, 3)
    else:
        for x in range(W):
            top = 15 + int(3 * math.sin(x * 2 * math.pi / 64) + 2 * math.sin(x * 2 * math.pi / 32 + 2))
            for y in range(top, 24):
                cv.px[y][x] = 14
        horizon(cv, 14)
    field(cv, every=4 if d == "A" else 8)
    bd = cv.copy()

    def tex(x, y):
        if d == "A":
            return cliff[16 + (y % 16)][x % 64]
        return dash(x, y, 6, 5)

    def marks(x, y, dd):
        if dd < 2:
            return None
        h = hashr(x // 12, y // 6)
        if h % 6 == 0 and x % 12 == h % 10 and y % 6 == 2:
            return 9
        return None

    def tips(xm, ytop):                         # a few stones on the rim
        k = (xm // 4) % 7
        return ((2, 3) if k in (1, 4) else None) if d == "A" else None

    for E in (FOE, ME):
        platform(cv, E, tex, rim=2, lip=3, light=7, marks=marks, tips=tips)
    st = strip_canvas()
    m4 = [None, r[1], r[2], r[4], r[5], r[6]] + [None] * 10
    for x in range(W):                            # spires: MT. EMBER's rock, stood on end
        k = x % 64
        hh = int(max(0, 34 - abs(k - 20) * 2.2)) + int(max(0, 22 - abs(k - 48) * 3))
        hh = max(hh, 6)
        for y in range(112 - hh, 112):
            v = 3 if (x % 64) < 20 or (40 < k < 48) else 2
            if y < 112 - hh + 2:
                v = 4
            if d == "A" and (y // 4 + k // 4) % 5 == 0 and y > 112 - hh + 3:
                v = 1
            st.put(x, y, v)
    return cv, bd, P(row2, m4), st


# ---- CAVE: MT. MOON ---------------------------------------------------------------------------------------------------
def scene_cave(d):
    fl = quant(["floor", "lfloor", "boulders"], 7)
    wl = quant(["wall"], 5)
    if d == "B":
        fl = [quiet(c, s=0.45, v_to=0.55, k=0.3) for c in fl]
        wl = [quiet(c, s=0.4, v_to=0.35, k=0.3) for c in wl]
    GS = ground_slots(fl)
    floor = quant(["floor"], 3)
    fieldc = floor[1] if d == "A" else quiet(floor[1], s=0.4, v_to=0.55, k=0.3)
    scanc = mix(fieldc, floor[0], 0.4 if d == "A" else 0.2)
    row2 = [None, scanc] + fl + [(31, 31, 26)] + wl + [fieldc]
    cv = Canvas()
    WS = [(10 + i, c) for i, c in enumerate(wl)]
    if d == "A":
        # MT. MOON's wall, its stones and their yellow seams, from the top to the cave floor
        wall = slotted("wall", WS)
        for y in range(24):
            for x in range(W):
                cv.px[y][x] = wall[y % 32][x % 64]
        horizon(cv, 10)
    else:
        sky(cv, [10, 11, 12, 13], 0, 24)
        for y in range(0, 24, 6):               # the wall's courses, only their seams
            for x in range(W):
                cv.px[y][x] = 10
        horizon(cv, 14)
    field(cv, every=4 if d == "A" else 8)
    bd = cv.copy()
    lfl = slotted("lfloor", GS)
    bou = slotted("boulders", GS, key_out="floor", tol=4)

    def tex(x, y):
        if d == "A":
            return lfl[y % 32][x % 32]
        return dash(x, y, 6, 5)

    def marks(x, y, dd):
        if dd < 2:
            return None
        h = hashr(x // 10, y // 6)
        if h % 8 == 0 and x % 10 == h % 9 and y % 6 == 3:
            return 9
        return None

    for E in (FOE, ME):
        platform(cv, E, tex, rim=2, lip=3, light=7, marks=marks)
    if d == "A":
        # MT. MOON's boulders at the platform's back corners, a pair each side
        for (bx, by) in ((114, 44), (222, 44), (2, 97), (110, 97)):
            for y, row in enumerate(bou[2:14]):
                for x, v in enumerate(row[:16]):
                    if v >= 0:
                        cv.put(bx + x if bx < 176 or bx > 200 else bx + x, by + y, v)
    st = strip_canvas()
    c4 = [None, fl[0], fl[2], fl[3], fl[5], fl[6]] + [None] * 10
    for x in range(W):                            # stalagmites: the cave's stone, rising
        k = x % 48
        hh = int(max(0, 44 - abs(k - 14) * 4)) + int(max(0, 26 - abs(k - 34) * 3.5))
        hh = max(hh, 4)
        for y in range(112 - hh, 112):
            v = 2 if (k < 14 or 30 < k < 34) else 3
            if y < 112 - hh + 2:
                v = 4
            if d == "A" and (y // 5 + x // 2) % 6 == 0:
                v = 1
            st.put(x, y, v)
    return cv, bd, P(row2, c4), st


# ---- BUILDING: the house, and every room that wears its drawing --------------------------------------------------------
def scene_building(d):
    """Vanilla's ROLES kept (the 20 room palettes recolour this drawing): 2 the rug's fill, 3 its rim, 5 its inner
    ring, 4 its top and bottom, 6-9 marks; 10-14 the wall, horizontal bands only (PLAIN's sky); 15 the floor, 1 its
    seams (PLAIN's field and scan lines)."""
    wood = quant(["hfloor"], 4)
    wallc = quant(["hwall"], 6)
    rug = quant(["rug"], 8)
    if d == "A":
        # our house: the floor's warm planks, the wall's panels, the rug's weave
        roles = {2: rug[6], 3: rug[1], 4: rug[3], 5: rug[5], 6: rug[2], 7: rug[4], 8: rug[0], 9: (31, 30, 26)}
        skyc = [wallc[1], wallc[2], wallc[3], mix(wallc[3], wood[2], 0.5), wood[1]]
        fieldc, scanc = wood[2], wood[1]
    else:
        roles = {2: (28, 27, 24), 3: (16, 15, 14), 4: (22, 20, 18), 5: (25, 24, 21), 6: (20, 19, 17),
                 7: (23, 21, 19), 8: (19, 18, 16), 9: (31, 30, 28)}
        skyc = [(19, 19, 20), (21, 21, 22), (23, 23, 23), (24, 24, 24), (20, 19, 18)]
        fieldc, scanc = (23, 22, 20), (21, 20, 18)
    row2 = [None, scanc] + [roles[i] for i in range(2, 10)] + skyc + [fieldc]
    cv = Canvas()
    if d == "A":
        # the wall: a panel's courses (horizontal only), a rail, the skirting at the floor
        for y in range(24):
            v = 10 if y < 3 else (11 if y < 10 else (12 if y < 18 else 13))
            if y in (9, 17):
                v = 10
            if y >= 21:
                v = 14
            for x in range(W):
                cv.px[y][x] = v
        horizon(cv, 14)
        field(cv, every=4)
        # the planks' joints, staggered, in the seam's colour (1): PLAIN reads them as its scan lines' gaps
        for y in range(32, H):
            band = (y - 32) // 4
            if (y - 32) % 4 == 0:
                continue
            for x in range(W):
                if (x + band * 40) % 80 == 0:
                    cv.px[y][x] = 1
    else:
        sky(cv, [10, 11, 12, 13], 0, 24)
        horizon(cv, 14)
        field(cv, every=8)
    bd = cv.copy()

    def tex(x, y):
        cx = FOE[0] if x >= 128 else ME[0]
        cy = FOE[1] if y < 90 else ME[1]
        r = ((x + .5 - cx) / 64) ** 2 + ((y + .5 - cy) / 16) ** 2
        if d == "A":
            # the rug's weave: concentric rings, the diamond at its heart
            ring = int(math.sqrt(r) * 8)
            if abs(x + .5 - cx) / 3.2 + abs(y + .5 - cy) < 5:
                return 4 if abs(x + .5 - cx) / 3.2 + abs(y + .5 - cy) > 3 else 9
            return (2, 5, 2, 7, 2, 5, 6, 2)[ring % 8]
        ring = int(math.sqrt(r) * 6)
        return 5 if ring == 4 else 2

    def marks(x, y, dd):
        return None

    for E in (FOE, ME):
        platform(cv, E, tex, rim=3, lip=4, light=None, marks=marks)
    st = strip_canvas()
    b4 = [None, (20, 26, 31), (29, 31, 31), (22, 28, 31), (25, 29, 31), (27, 30, 31)] + [None] * 10
    if d == "A":
        b4 = [None, wood[1], (31, 30, 26), wood[2], wood[3], (29, 27, 22)] + [None] * 10
    for k, (y, x0, ln) in enumerate(((70, 10, 40), (78, 120, 64), (86, 40, 24), (94, 180, 50), (102, 70, 36))):
        for x in range(x0, x0 + ln):
            st.put(x % W, y, 2 if k % 2 else 3)
            if d == "A":
                st.put(x % W, y + 1, 1)
    return cv, bd, P(row2, b4), st


# ================================================================================================ tiles, map, files
def tile_of(px, tx, ty):
    return tuple(px[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8))


def flips(t):
    rows = [t[i * 8:(i + 1) * 8] for i in range(8)]
    h = tuple(v for r in rows for v in reversed(r))
    v = tuple(v for r in reversed(rows) for v in r)
    hv = tuple(v for r in reversed(rows) for v in reversed(r))
    return [(t, 0, 0), (h, 1, 0), (v, 0, 1), (hv, 1, 1)]


class Tiles:
    def __init__(self):
        self.list = [tuple([0] * 64)]
        self.index = {self.list[0]: (0, 0, 0)}

    def add(self, t, allow_flip=True):
        if t in self.index:
            return self.index[t]
        if allow_flip:
            for ft, hf, vf in flips(t)[1:]:
                if ft in self.index and self.index[ft][1:] == (0, 0):
                    i = self.index[ft][0]
                    return (i, hf, vf)
        i = len(self.list)
        self.list.append(t)
        self.index[t] = (i, 0, 0)
        return (i, 0, 0)


def build_terrain(cv, bd):
    """the 32x64 map and its tiles, as vanilla lays them: rows 0-13 the scene, 14-29 under the box, 30-31 the field,
    32-45 the backdrop without platforms, 46-61 under the box, 62-63 the field"""
    T = Tiles()
    m = [0] * 2048
    for ty in range(14):
        for tx in range(32):
            t = tile_of(cv.px, tx, ty)
            row3 = any(ell(ME, x, y)[0] <= 1.0 for y in range(ty * 8, ty * 8 + 8) for x in range(tx * 8, tx * 8 + 8)) \
                and ty >= 11 and tx < 17
            i, hf, vf = T.add(t, allow_flip=(ty != HORIZON_ROW))
            m[ty * 32 + tx] = i | hf << 10 | vf << 11 | (3 if row3 else 2) << 12
    fieldtile = tile_of(bd.px, 0, 13)
    fi = T.add(fieldtile)[0]
    for ty in (30, 31, 62, 63):
        for tx in range(32):
            m[ty * 32 + tx] = fi | 2 << 12
    for ty in range(14):
        for tx in range(32):
            i, hf, vf = T.add(tile_of(bd.px, tx, ty), allow_flip=(ty != HORIZON_ROW))
            m[(32 + ty) * 32 + tx] = i | hf << 10 | vf << 11 | 2 << 12
    return T.list, m


def build_strip(st):
    T = Tiles()
    m = [0] * (32 * 14)
    for ty in range(14):
        for tx in range(32):
            i, hf, vf = T.add(tile_of(st.px, tx, ty))
            m[ty * 32 + tx] = i | hf << 10 | vf << 11 | 4 << 12
    return T.list, m


def to8(c):
    return tuple(v * 255 // 31 for v in c)


def save_sheet(path, tiles, pal16, rows_min):
    n = len(tiles)
    rows = max(rows_min, (n + 7) // 8)
    im = Image.new("P", (64, rows * 8), 0)
    flat = []
    for c in pal16:
        flat += list(to8(c))
    im.putpalette(flat + [0] * (768 - len(flat)))
    p = im.load()
    for i, t in enumerate(tiles):
        for y in range(8):
            for x in range(8):
                p[(i % 8) * 8 + x, (i // 8) * 8 + y] = t[y * 8 + x]
    im.save(path, bits=4)


def save_pal(path, cols):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(cols))
        for c in cols:
            f.write("%d %d %d\n" % tuple(v << 3 for v in c))


def vanilla_budget(name, kind="terrain"):
    im = Image.open(os.path.join(TERR, name, kind + ".png"))
    return im.width * im.height // 64


def make(name, d, out):
    cv, bd, pal, st = scene(name, d)
    tiles, m = build_terrain(cv, bd)
    stiles, sm = build_strip(st)
    dd = os.path.join(out, d, name)
    os.makedirs(dd, exist_ok=True)
    save_sheet(os.path.join(dd, "terrain.png"), tiles, pal[:16], vanilla_budget(name) // 8)
    open(os.path.join(dd, "terrain.bin"), "wb").write(struct.pack("<2048H", *m))
    save_pal(os.path.join(dd, "terrain.pal"), pal)
    save_sheet(os.path.join(dd, "anim.png"), stiles, pal[32:48], vanilla_budget(name, "anim") // 8)
    open(os.path.join(dd, "anim.bin"), "wb").write(struct.pack("<448H", *sm))
    return dd, len(tiles), len(stiles)


# ================================================================================================ the contract, checked
def check(name, dd, ntiles, nstrip):
    """what T-481 needs of the art, measured as gbabattlebg.py measures it; [] when it holds"""
    bad = []
    T = BG.Terrain(name, os.path.join(dd, "terrain.png"), os.path.join(dd, "terrain.bin"), os.path.join(dd, "terrain.pal"))
    if ntiles > vanilla_budget(name):
        bad.append("tiles %d > vanilla's %d" % (ntiles, vanilla_budget(name)))
    if nstrip > vanilla_budget(name, "anim"):
        bad.append("strip tiles %d > vanilla's %d" % (nstrip, vanilla_budget(name, "anim")))
    if not T.horizon or T.horizon_shared:
        bad.append("horizon %s shared %s" % (T.horizon, T.horizon_shared))
    if BG.ACCENT not in T.row3_free:
        bad.append("row 3's 12 is drawn")
    if any(v not in T.row3_free for v in (10, 11, 13, 14)):
        bad.append("row 3 draws a sky colour: free %s" % T.row3_free)
    if len(T.sky) > 6:
        bad.append("%d sky colours" % len(T.sky))
    if name != "cave" and name != "building" and any(not 10 <= v <= 14 for v in T.sky):
        bad.append("ground colour %s drawn only in the sky (the hour would step it)" % [v for v in T.sky if v < 10])
    if T.horizon_mismatch():
        bad.append("the horizon draws %s, which row 3 reads otherwise" % T.horizon_mismatch())
    for pb in (2, 3):
        if T.glint[pb] is None:
            bad.append("row %d has no glint" % pb)
    vis = [T.px(x, y) for y in range(112) for x in range(240)]
    if any(v == 0 for _, v in vis):
        bad.append("a transparent pixel on screen")
    if grey_gap(T) < 1.0:
        bad.append("HALFTONE: the foe's platform and the field are %.1f apart in grey" % grey_gap(T))
    return T, bad


def grey_gap(T):
    """HALFTONE keeps value, not hue: how far the foe's platform sits from the field, in five-bit grey"""
    plat = [T.pal[v] for y in range(48, 80) for x in range(112, 240) for pb, v in [T.px(x, y)] if pb == 2 and 2 <= v <= 9]
    fld = T.pal[15]
    return abs(sum(lum(c) for c in plat) / max(1, len(plat)) - lum(fld))


# ================================================================================================ pictures
def ground_img(T, pal):
    return T.render(pal, accent=True)


def cal(T, watch="day", season="as drawn", weekday=None, reach=BG.FULL, holiday=None):
    return BG.calendar_palette(T, watch, season, weekday=weekday, holiday_colour=holiday, reach=reach)


def reach_of(name):
    return {"cave": BG.KEPT, "building": BG.INDOOR}.get(name, BG.FULL)


SAT = None


def saturday():
    global SAT
    if SAT is None:
        SAT = BG.day_trims()[6]           # 2026-11-07 is a SATURDAY
    return SAT


def strip_img(dd, pal):
    tiles = BG.png_tiles(os.path.join(dd, "anim.png"))
    m = struct.unpack("<448H", open(os.path.join(dd, "anim.bin"), "rb").read())
    im = Image.new("RGB", (256, 112), (36, 38, 44))
    for k, e in enumerate(m):
        t, hf, vf = e & 0x3FF, e >> 10 & 1, e >> 11 & 1
        for y in range(8):
            for x in range(8):
                sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                b = tiles[t * 32 + sy * 4 + sx // 2]
                v = (b >> 4) if sx & 1 else b & 15
                if v:
                    im.putpixel(((k % 32) * 8 + x, (k // 32) * 8 + y), to8(pal[32 + v]))
    return im


_U = None


def ui():
    global _U
    if _U is None:
        _U = _load("gbabattleui")
    return _U


def mock(ground, message=True):
    U = ui()
    return U.mock_message(None, ground) if message else U.mock(None, ground)


def font(n):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except OSError:
        return ImageFont.load_default()


TITLE = {"grass": "GRASS (Route 1)", "longgrass": "LONG GRASS", "sand": "SAND (TREASURE BEACH)",
         "underwater": "UNDERWATER", "water": "WATER (the sea's bits)", "pond": "POND (Route 1's)",
         "mountain": "MOUNTAIN (MT. EMBER)", "cave": "CAVE (MT. MOON)", "building": "BUILDING (+ PLAIN, rooms, gyms)"}
SAYS = {
    "grass": ("Route 1's trees on the horizon, its tall grass on the platforms, specks of its flowers",
              "a hazy treeline in the sky's own colour; flat green platforms, a few ticks"),
    "longgrass": ("as GRASS, deeper green, the blades rising off the rim", "as GRASS, deeper"),
    "sand": ("TREASURE BEACH's sand on the platforms, its sea (and its bits) at the horizon",
             "a pale sea line; sand platforms, a few shells"),
    "underwater": ("our sea's bits as light from above; sand under the water", "dim blue bands, a low ridge"),
    "water": ("our sea and its 0/1 bits as the platforms; a broken swell line",
              "flat blue, a few glints; the scan lines are the swell"),
    "pond": ("Route 1's pond, its earth rim and bits, grass at its edge, trees beyond", "a low bank; a flat pond"),
    "mountain": ("MT. EMBER's cliff as the ridge and the platforms' stone", "a soft ridge in haze; plain stone"),
    "cave": ("MT. MOON's wall and seams, its floor, its boulders at the platforms",
             "the wall's courses only; plain floor"),
    "building": ("the house: wall panels, skirting, plank floor, the rug's weave as the platforms",
                 "a grey wall and floor; plain rugs"),
}


def label(d, xy, s, n=12, fill=(30, 30, 36)):
    d.text(xy, s, fill=fill, font=font(n))


def contact_sheet(out, made):
    """per terrain: the engine's now, A and B, each a 240x160 battle at real size, and A's and B's entry strips"""
    cw, chh = 240, 160
    pad, lab = 12, 34
    rowh = chh + lab + 70
    Wd = pad + 3 * (cw + pad) + 256 + pad
    Hd = 70 + len(SETS) * rowh + 20
    sheet = Image.new("RGB", (Wd, Hd), (236, 234, 228))
    dr = ImageDraw.Draw(sheet)
    label(dr, (pad, 10), "T-527 DRAFT -- battle backgrounds in our own hand (map tiles + code, no AI): "
                         "now | A OUR PLACE | B QUIET FIELD", 14)
    label(dr, (pad, 32), "Each a mock battle at real size: our daemons, the built Readout (T-524). Day, as drawn; the "
                         "horizon line in SATURDAY's trim (T-481). Nothing is in the engine.", 12, (70, 70, 76))
    y = 70
    for name in SETS:
        label(dr, (pad, y), TITLE[name], 14)
        x = pad
        cur = made[name]["now"]
        for col, (k, T, pal) in enumerate((("now", cur[0], cur[1]),) + tuple(
                (dd_, made[name][dd_][0], made[name][dd_][1]) for dd_ in DIRS)):
            g = ground_img(T, pal)
            sheet.paste(mock(g), (x, y + lab - 14))
            label(dr, (x, y + lab - 14 + chh + 2), {"now": "now (Nintendo's drawing)", "A": "A  our place",
                                                    "B": "B  quiet field"}[k], 11)
            if k != "now":
                label(dr, (x, y + lab - 14 + chh + 16), SAYS[name][0 if k == "A" else 1][:40], 10, (80, 80, 86))
                label(dr, (x, y + lab - 14 + chh + 28), SAYS[name][0 if k == "A" else 1][40:80], 10, (80, 80, 86))
                label(dr, (x, y + lab - 14 + chh + 40), "%d/%d tiles, strip %d/%d" % (
                    made[name][k][2], vanilla_budget(name), made[name][k][3], vanilla_budget(name, "anim")), 10,
                      (80, 80, 86))
            x += cw + pad
        for j, k in enumerate(DIRS):
            s = strip_img(made[name][k][4], made[name][k][1]).crop((0, 56, 256, 112))
            sheet.paste(s, (x, y + lab - 14 + j * 80 + 14))
            label(dr, (x, y + lab - 14 + j * 80), "entry strip %s (the intro, wraps)" % k, 10)
        label(dr, (x, y + lab - 14 + 160), "recommended: %s" % RECOMMENDED[name], 11)
        y += rowh
    sheet.save(out)


def calendar_sheet(out, made):
    """T-481's run time on the drafts, as the cartridge does it: GRASS and WATER at dawn, day, dusk and night in
    autumn (today's season); the building drawing under PLAIN, a gym, LORELEI's room and SLATE's arena"""
    pad = 10
    cw, chh = 240, 112
    rows = []
    for name in ("grass", "water"):
        for k in ("now",) + DIRS:
            T = made[name][k][0] if k != "now" else made[name]["now"][0]
            rows.append(("%s %s" % (name.upper(), k), [(w, cal(T, w, "autumn", saturday())) for w in
                                                       ("dawn", "day", "dusk", "night")], T))
    Wd = pad + 4 * (cw + pad) + 120
    rooms = ["PLAIN", "GYM", "LORELEI", "BENCHMARK_SLATE"]
    Hd = 60 + len(rows) * (chh + 22) + 3 * (chh + 22) + 40
    sheet = Image.new("RGB", (Wd, Hd), (236, 234, 228))
    dr = ImageDraw.Draw(sheet)
    label(dr, (pad, 10), "T-527 DRAFT -- the calendar (T-481) on the drafts: autumn, SATURDAY's line, each hour", 15)
    label(dr, (pad, 30), "Rendered with gbabattlebg.py's calendar_palette, the sum daemons_battle_bg.c does.", 11,
          (70, 70, 76))
    y = 56
    for title, pals, T in rows:
        label(dr, (pad, y + 40), title, 11)
        x = pad + 120
        for w, pal in pals:
            sheet.paste(T.render(pal, accent=True), (x, y))
            label(dr, (x, y + chh + 2), w, 10)
            x += cw + pad
        y += chh + 22
    # the rooms that wear the building drawing, through their own palettes (which this does not change)
    terr = {n: (png, binp, pal) for _, n, png, binp, pal in BG.engine_terrains()}
    for k in ("now",) + DIRS:
        label(dr, (pad, y + 40), "BUILDING " + k, 11)
        x = pad + 120
        for room in rooms:
            png, binp, pal = terr[room]
            if k != "now":
                dd = made["building"][k][4]
                png, binp = os.path.join(dd, "terrain.png"), os.path.join(dd, "terrain.bin")
            T = BG.Terrain("building", png, binp, pal)
            reach = BG.REACH.get(room, BG.KEPT)
            sheet.paste(T.render(cal(T, "day", "autumn", saturday(), reach=reach), accent=True), (x, y))
            label(dr, (x, y + chh + 2), room, 10)
            x += cw + pad
        y += chh + 22
    sheet.save(out)


# ================================================================================================ report, draft, write
def draft(out):
    os.makedirs(out, exist_ok=True)
    made = {}
    allbad = 0
    terr = {n: (png, binp, pal) for _, n, png, binp, pal in BG.engine_terrains()}
    vanilla_name = {"grass": "GRASS", "longgrass": "LONG_GRASS", "sand": "SAND", "underwater": "UNDERWATER",
                    "water": "WATER", "pond": "POND", "mountain": "MOUNTAIN", "cave": "CAVE", "building": "BUILDING"}
    for name in SETS:
        made[name] = {}
        T0 = BG.Terrain(name, *terr[vanilla_name[name]])
        made[name]["now"] = (T0, cal(T0, weekday=saturday(), reach=reach_of(name)))
        for d in DIRS:
            dd, nt, ns = make(name, d, out)
            T, bad = check(name, dd, nt, ns)
            pal = cal(T, weekday=saturday(), reach=reach_of(name))
            made[name][d] = (T, pal, nt, ns, dd)
            print("  %-10s %s  tiles %3d/%-3d strip %3d/%-3d  field %d horizon %s sky %s glints %s grey gap %.1f  %s"
                  % (name, d, nt, vanilla_budget(name), ns, vanilla_budget(name, "anim"), T.field_top, T.horizon,
                     T.sky, T.glint, grey_gap(T), "ok" if not bad else "! " + "; ".join(bad)))
            allbad += len(bad)
    contact_sheet(os.path.join(out, "t527_battle_bg_sheet.png"), made)
    calendar_sheet(os.path.join(out, "t527_battle_bg_calendar.png"), made)
    print("  sheets: %s, %s" % (os.path.join(out, "t527_battle_bg_sheet.png"),
                                os.path.join(out, "t527_battle_bg_calendar.png")))
    return 1 if allbad else 0


def report():
    print("T-527 battle backgrounds -- the engine's terrains (%s):" % TERR)
    for name in SETS:
        T = BG.Terrain(name)
        print("  %-10s %dx%d tiles=%d (budget %d), strip budget %d; field %d, horizon %s, sky %s, row-3 free %s"
              % (name, 64, vanilla_budget(name) // 8 * 8, T.used_tiles, vanilla_budget(name),
                 vanilla_budget(name, "anim"), T.field_top, T.horizon, T.sky, T.row3_free))
    print("\n  indoor/terrain.png and .bin are pixel-for-pixel building's: a write puts the building pick in both.")
    import tempfile
    print("\n  the drafts, made in a scratch folder and measured as T-481 measures the engine's:")
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name in SETS:
            for d in DIRS:
                dd, nt, ns = make(name, d, tmp)
                T, b = check(name, dd, nt, ns)
                bad += len(b)
                print("  %-10s %s  tiles %3d/%-3d strip %3d/%-3d grey gap %4.1f  %s" % (
                    name, d, nt, vanilla_budget(name), ns, vanilla_budget(name, "anim"), grey_gap(T),
                    "keeps the contract" if not b else "! " + "; ".join(b)))
        print("  APPROVED: %s" % (APPROVED or "nothing yet -- the drafts wait on the user (--draft makes them)"))
        if A.approved and APPROVED:
            off = differs(tmp)
            for f in off:
                print("  ! the engine's %s is not what the approved write makes" % f)
            if off:
                print("  the engine drifts from the picks (%d files): --write --approved --all puts them back" % len(off))
                bad += len(off)
            else:
                print("  the engine holds every approved pick")
    return 1 if bad else 0


def targets_of(name):
    """(engine folder, files) the write puts a terrain's pick into: building's drawing goes into indoor/ as well."""
    out = [(name, ("terrain.png", "terrain.bin", "terrain.pal", "anim.png", "anim.bin"))]
    if name == "building":
        out.append(("indoor", ("terrain.png", "terrain.bin")))
    return out


def differs(tmp):
    """Every engine file that is not byte for byte what the approved write makes (the drafts already made in tmp)."""
    off = []
    for name, d in sorted(APPROVED.items()):
        dd = os.path.join(tmp, d, name)
        for tgt, files in targets_of(name):
            for f in files:
                src, dst = os.path.join(dd, f), os.path.join(TERR, tgt, f)
                if not os.path.exists(dst) or open(src, "rb").read() != open(dst, "rb").read():
                    off.append(os.path.join(tgt, f))
    return off


def write(picks):
    if not A.approved:
        print("  --write refuses without --approved: the user picks from the sheet first.")
        return 1
    if not picks:
        print("  --write needs --pick terrain=A|B ...")
        return 1
    for name, d in picks.items():
        if APPROVED.get(name) != d:
            print("  %s=%s is not what APPROVED holds (%s): nothing written." % (name, d, APPROVED.get(name)))
            return 1
    out = DRAFT_DEFAULT
    for name, d in picks.items():
        dd, nt, ns = make(name, d, out)
        T, bad = check(name, dd, nt, ns)
        if bad:
            print("  %s %s breaks the contract: %s" % (name, d, bad))
            return 1
        for tgt, files in targets_of(name):
            for f in files:
                shutil.copyfile(os.path.join(dd, f), os.path.join(TERR, tgt, f))
        print("  wrote %s (%s)" % (name, d))
    # the calendar's tables are measured off the art: regenerate them now
    return subprocess.call([sys.executable, os.path.join(TOOLS, "gbabattlebg.py"), "--write", "--approved"])


def main():
    if A.write:
        picks = dict(APPROVED) if A.all else {}
        picks.update(p.split("=", 1) for p in A.pick)
        return write(picks)
    if A.draft:
        return draft(A.draft)
    return report()


if __name__ == "__main__":
    sys.exit(main())

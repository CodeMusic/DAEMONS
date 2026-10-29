#!/usr/bin/env python3
"""T-481 part A: THE BATTLE BACKGROUNDS THAT KEEP THE CALENDAR.

    python3 tools/gbabattlebg.py                       # report: every terrain, what it draws with, the cost, and
                                                       #   whether the engine holds what --write would write (exit 1 if not)
    python3 tools/gbabattlebg.py --write --approved    # src/data/battle_calendar.h into the engine (approved 2026-10-29)
    python3 tools/gbabattlebg.py --sheet OUTDIR        # the sheets: grass, cave, building, the week, a holiday, the reach

Drafted 2026-10-29 on sheets (DAEMONS 7e16bf3f; qa private 29Oct2026 T481 25-28) and answered by the user the same
day, by multiple choice: OUTDOORS gets the hour (sWatchTint and the sky step: rose at dawn, amber at dusk, navy at
night) and the season in full, summer a light sun-bleach; a BUILDING gets the hour at a quarter ("through the
windows") and no season; a CAVE keeps its own light; the WEEKDAY is ONE 1px horizon line in the day's trim; a
HOLIDAY's month colour goes on the platform glints, and nothing changes on a quiet day; the BENCHMARK arenas and the
Elite rooms get the line and the glints only. The engine's half is src/daemons_battle_bg.c, which does at run time
what calendar_palette() below does for the sheets -- the tables it needs are this tool's --write.

WHAT IS THERE (measured, every terrain). A battle terrain is one tileset, one 32x64 tilemap and three BG palette rows,
BG 2-4 (battle_bg.c: LoadCompressedPalette(..., BG_PLTT_ID(2), 3 * PLTT_SIZE_4BPP)). The layout is the same in every
outdoor terrain and in the building one (whose tiles every indoor terrain shares, each with its own palette):
    row 2  1 the scan line every fourth pixel row, sky and field alike; 10-14 the backdrop's bands (the sky);
           15 the field; 2-9 the foe's platform
    row 3  the player's platform, 2-9; its 1 and 15 copy row 2's, and its 10-14 are copies NO TILE DRAWS -- in every
           terrain. Five free colours, already loaded, already in the palette RAM.
    row 4  the entry animation's tufts (BG 1, the intro only)

THE MECHANISM, in order, after the terrain's palette loads and before the weather's wash:
  1. THE SEASON -- the field, both platforms and row 4's tufts from a table, one per outdoor terrain per season
     (spring's platform glints in bloom). The sky is left to the hour.
  2. THE HOLIDAY -- each platform's GLINT (its brightest sparse colour) takes the month colour the holiday wears.
  3. THE WEEKDAY -- the backdrop's last scan line above the field is repainted in VRAM from colour 1 to colour 12, and
     that tile row's map entries move to row 3, whose other free colours copy row 2's -- so the line, and only the
     line, takes the day's CHECKPOINT trim (day_trims.h). Four bytes of one tile and its row's map entries, after the
     tiles decompress (battle_bg.c LoadBattleTerrainGfx and LoadChosenBattleElement; the move animations that swap
     the backdrop restore it through DrawMainBattleBackground, so through the same patch).
  4. THE HOUR -- the field's own sum (daemons_time.c sWatchTint) on all 48 colours, at a quarter in a building; and
     outdoors, on the sky bands only, a step toward the watch's sky. Day is as drawn.
  then T-415's weather wash, as before; then T-482's pulse, at the copy to PLTT; then HALFTONE's grey.

THE COST: EWRAM 0, IWRAM 0, SAVE 0. ROM: the report's line. CPU: once per terrain load.
"""
import colorsys, os, re, struct, sys
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
TERR = os.path.join(GBA, "graphics/battle_terrain")
OUT_REL = "src/data/battle_calendar.h"
VIS_W, VIS_H = 240, 112          # the screen above the text box

OUTDOOR = ("grass", "longgrass", "sand", "mountain", "water", "pond", "underwater")
ALL = OUTDOOR + ("cave", "building")
WATCHES = ("dawn", "day", "dusk", "night")
C_WATCHES = ("day", "dusk", "night", "dawn")      # daemons_time.h's WATCH_* order
SEASONS = ("winter", "spring", "summer", "autumn")   # daemons_time.h's SEASON_* order
DAYS = ("SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY")
ACCENT = 12                      # row 3's free colour that carries the day
MIN_TYPE_DISTANCE = 22           # 9.4 asks 20; the trims were made 22+, and every colour this adds is held to it

# THE REACH, as the user answered (2026-10-29). Every terrain the engine has must be named here: a new one is a decision.
FULL, INDOOR, KEPT = "full", "indoor", "kept"
REACH = {
    "GRASS": FULL, "LONG_GRASS": FULL, "SAND": FULL, "UNDERWATER": FULL, "WATER": FULL, "POND": FULL,
    "MOUNTAIN": FULL, "PLAIN": FULL,                                    # outdoors: the hour and the season
    "BUILDING": INDOOR, "LINK": INDOOR, "INDOOR_1": INDOOR, "INDOOR_2": INDOOR,   # the hour at a quarter
    "CAVE": KEPT,                                                        # its own light
    # the arenas -- the gyms, the leaders, the BENCHMARK rooms -- and the Elite rooms: the line and the glints only
    "GYM": KEPT, "LEADER": KEPT, "LORELEI": KEPT, "BRUNO": KEPT, "AGATHA": KEPT, "LANCE": KEPT, "CHAMPION": KEPT,
}
C_REACH = {FULL: "BATTLE_CAL_FULL", INDOOR: "BATTLE_CAL_INDOOR", KEPT: "BATTLE_CAL_KEPT"}

try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    SMALL = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
except OSError:
    FONT = SMALL = ImageFont.load_default()


# --- what the engine is built from (the SOURCES -- .png, .pal, .bin -- so a fresh clone reads the same) ----------------

def read(rel):
    return open(os.path.join(GBA, rel)).read()


def rgb_table(text):
    return [tuple(map(int, m)) for m in re.findall(r"RGB\(\s*(\d+),\s*(\d+),\s*(\d+)\)", text)]


def day_trims():
    return rgb_table(read("src/data/day_trims.h"))


def month_colours():
    body = read("src/data/daemons_holidays.h").split("sMonthColours[12] = {", 1)[1].split("};", 1)[0]
    return rgb_table(body)


def watch_tint():
    """daemons_time.c's sWatchTint, as {watch: ((mul, add) r, g, b)} -- read, so the draft lights as the field does."""
    body = read("src/daemons_time.c").split("sWatchTint[WATCH_COUNT][3][2] = {", 1)[1].split("};", 1)[0]
    out = {}
    for name, rest in re.findall(r"\[WATCH_(\w+)\]\s*=\s*\{(.*?)\},\s*\n", body):
        nums = list(map(int, re.findall(r"\d+", rest)))
        out[name.lower()] = tuple((nums[2 * k], nums[2 * k + 1]) for k in range(3))
    return out


def holiday_months():
    """{HOLIDAY NAME: (month 1-12, quiet)} for CONTENT's table (the first in the file), from the generated header."""
    text = read("src/data/daemons_holidays.h")
    names = dict(re.findall(r'(sHolidayName_\w+)\[\] = _\("([^"]*)"\)', text))
    table = text.split("static const struct HolidayRow sHolidays[HOLIDAY_COUNT] = {", 1)[1].split("};", 1)[0]
    out = {}
    for sym, flags, month in re.findall(r"\{ (sHolidayName_\w+), ([^,]+), HOLIDAY_RULE_\w+, (\d+),", table):
        out[names.get(sym, sym)] = (int(month), "HF_QUIET" in flags)
    return out


def jasc(path):
    """A JASC .pal as five-bit colours, as gbagfx makes the .gbapal (each channel >> 3)."""
    words = open(path).read().split()
    n = int(words[2])
    v = list(map(int, words[3:3 + 3 * n]))
    return [(v[3 * i] >> 3, v[3 * i + 1] >> 3, v[3 * i + 2] >> 3) for i in range(n)]


def png_tiles(path):
    """An indexed PNG as 4bpp tiles in reading order, as gbagfx makes the .4bpp (trailing blank tiles kept)."""
    im = Image.open(path)
    w, h = im.size
    px = im.load()
    out = bytearray()
    for ty in range(h // 8):
        for tx in range(w // 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    out.append((px[tx * 8 + x, ty * 8 + y] & 15) | (px[tx * 8 + x + 1, ty * 8 + y] & 15) << 4)
    return out


def engine_terrains():
    """[(number, NAME, tiles .png, map .bin, palette .pal)] -- battle_bg.c's sBattleTerrainTable, every row."""
    src = read("src/battle_bg.c")
    inc = dict(re.findall(r'static const u32 (\w+)\[\] = INCBIN_U32\("([^"]+)"\);', src))
    nums = {n: int(v) for n, v in re.findall(r"#define BATTLE_TERRAIN_(\w+)\s+(\d+)", read("include/constants/battle.h"))}
    body = src.split("sBattleTerrainTable[] = {", 1)[1].split("\n};", 1)[0]
    out = []
    for name, entry in re.findall(r"\[BATTLE_TERRAIN_(\w+)\]\s*=\s*\{(.*?)\}", body, re.S):
        f = dict(re.findall(r"\.(\w+)\s*=\s*(\w+)", entry))
        def src_of(sym, ext):
            return os.path.join(GBA, re.sub(r"\.(4bpp|bin|gbapal)\.lz$", "", inc[sym]) + ext)
        out.append((nums[name], name, src_of(f["tileset"], ".png"), src_of(f["tilemap"], ".bin"),
                    src_of(f["palette"], ".pal")))
    out.sort()
    assert [n for n, *_ in out] == list(range(len(out))), "sBattleTerrainTable has a gap"
    return out


class Terrain:
    def __init__(self, name, png=None, binp=None, pal=None):
        d = os.path.join(TERR, name)
        self.name = name
        self.tiles = png_tiles(png or os.path.join(d, "terrain.png"))
        self.map = list(struct.unpack("<2048H", open(binp or os.path.join(d, "terrain.bin"), "rb").read()))
        self.pal = jasc(pal or os.path.join(d, "terrain.pal"))[:48]
        self.measure()

    def px(self, x, y, tiles=None, tmap=None):
        tiles, tmap = tiles or self.tiles, tmap or self.map
        e = tmap[(y // 8) * 32 + x // 8]
        t, hf, vf, pb = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
        sx, sy = (7 - x % 8) if hf else x % 8, (7 - y % 8) if vf else y % 8
        b = tiles[t * 32 + sy * 4 + sx // 2]
        return pb, (b >> 4) if sx & 1 else b & 15

    def tile_colours(self, t):
        return {v for b in self.tiles[t * 32: t * 32 + 32] for v in (b & 15, b >> 4)}

    def measure(self):
        self.count = {2: Counter(), 3: Counter()}
        ys = {}
        for y in range(VIS_H):
            for x in range(VIS_W):
                pb, v = self.px(x, y)
                if pb in self.count:
                    self.count[pb][v] += 1
                    ys.setdefault((pb, v), set()).add(y)
        self.used_tiles = max(e & 0x3FF for e in self.map) + 1
        # the field: the first pixel row drawn in row 2's 15 from edge to edge
        self.field_top = next(y for y in range(VIS_H) if all(self.px(x, y) == (2, 15) for x in range(VIS_W)))
        # the sky: row 2's colours drawn only above the field (the scan line 1 runs through both, so it is not one)
        self.sky = sorted((v for (pb, v), s in ys.items() if pb == 2 and v not in (0, 1) and max(s) < self.field_top),
                          key=lambda v: sum(ys[(2, v)]) / len(ys[(2, v)]))
        # each platform's glint: its brightest colour that draws at most a fifth of the platform
        self.glint = {}
        for pb in (2, 3):
            plat = {v: n for v, n in self.count[pb].items() if 2 <= v <= 9}
            total = sum(plat.values()) or 1
            sparse = [v for v, n in plat.items() if n <= total / 5]
            self.glint[pb] = max(sparse, key=lambda v: sum(self.pal[(pb - 2) * 16 + v])) if sparse else None
        # the horizon: the lowest backdrop tile row above the field drawn by ONE tile, row 2, with a whole pixel row
        # of the scan line (1) -- the line the weekday takes
        self.horizon = None
        for ty in range(self.field_top // 8, -1, -1):
            ents = self.map[ty * 32: ty * 32 + 30]
            if len(set(ents)) != 1 or ents[0] >> 12 != 2 or ents[0] >> 10 & 3:
                continue
            t = ents[0] & 0x3FF
            for ly in range(7, -1, -1):
                if all(b == 0x11 for b in self.tiles[t * 32 + ly * 4: t * 32 + ly * 4 + 4]) and ty * 8 + ly < self.field_top:
                    self.horizon = (ty, ly, t)
                    break
            if self.horizon:
                break
        # the tile may be drawn nowhere but its own row, in either screen, or the patch would move another row too
        self.horizon_shared = bool(self.horizon) and any(
            (e & 0x3FF) == self.horizon[2] and k // 32 not in (self.horizon[0], self.horizon[0] + 32)
            for k, e in enumerate(self.map))
        # row 3's FREE colours: drawn by no row-3 map entry ANYWHERE in the map (both screens, under the text box too)
        drawn3 = set()
        for e in self.map:
            if e >> 12 == 3:
                drawn3 |= self.tile_colours(e & 0x3FF)
        self.row3_free = [i for i in range(1, 16) if i not in drawn3]
        r2, r3 = self.pal[0:16], self.pal[16:32]
        self.row3_copies = all(r3[i] == r2[i] for i in (1, 15)) and all(r3[i] == r2[i] for i in range(10, 15))

    def free_mask(self):
        """row 3's free colours, the accent left out: copied from row 2's, so the moved horizon row reads the same"""
        return sum(1 << i for i in self.row3_free if i != ACCENT)

    def horizon_mismatch(self):
        """the horizon tile's colours that row 3 does not hold as row 2 does after the copy (LONG GRASS's 15, a step)"""
        if not self.horizon:
            return []
        return sorted(c for c in self.tile_colours(self.horizon[2])
                      if c not in (0, ACCENT) and c not in self.row3_free and self.pal[c] != self.pal[16 + c])

    def with_accent(self):
        """The tiles and map with the horizon line moved to row 3's ACCENT -- what DaemonsBattleBgHorizon leaves."""
        tiles, tmap = bytearray(self.tiles), list(self.map)
        if self.horizon:
            ty, ly, t = self.horizon
            for k in range(4):
                tiles[t * 32 + ly * 4 + k] = ACCENT << 4 | ACCENT
            for row in (ty, ty + 32):
                for tx in range(32):
                    e = tmap[row * 32 + tx]
                    if (e & 0x3FF) == t:
                        tmap[row * 32 + tx] = (e & 0x0FFF) | 3 << 12
        return tiles, tmap

    def render(self, pal, accent=True):
        tiles, tmap = self.with_accent() if accent else (self.tiles, self.map)
        im = Image.new("RGB", (VIS_W, VIS_H))
        for y in range(VIS_H):
            for x in range(VIS_W):
                pb, v = self.px(x, y, tiles, tmap)
                c = pal[(pb - 2) * 16 + v] if 2 <= pb <= 4 else (0, 0, 0)
                im.putpixel((x, y), to8(c))
        return im


def terrain_of(name, png, binp, pal):
    T = Terrain(os.path.basename(os.path.dirname(png)), png, binp, pal)
    T.name = name.lower()
    return T


# --- the sums, in five-bit colour, as the cartridge does them ---------------------------------------------------------

def to8(c):
    return tuple(v * 255 // 31 for v in c)


def hsv5(c):
    return colorsys.rgb_to_hsv(*(v / 31 for v in c))


def rgb5(h, s, v):
    return tuple(min(31, max(0, round(k * 31))) for k in colorsys.hsv_to_rgb(h % 1, max(0, min(1, s)), max(0, min(1, v))))


def lerp(a, b, k16):
    """a step from a toward b, by sixteenths, floored (daemons_battle_bg.c's Step, an arithmetic shift)."""
    return tuple(x + (y - x) * k16 // 16 for x, y in zip(a, b))


def season(c, name, field=False):
    """The ground in a season. Greens turn (the field's T-359 rules, carried to the platforms); everything else is
    dusted, warmed or freshened a little, so sand and rock keep the calendar too."""
    if name == "summer":                     # as drawn, with a little sun: bleached a touch toward straw
        h, s, v = hsv5(c)
        return rgb5(h + (6 / 360 if 0.15 < h < 0.5 else 0), s * 0.86, v + (1 - v) * 0.06)
    h, s, v = hsv5(c)
    green = 0.17 < h < 0.48 and s > 0.08
    if name == "winter":
        if green:                            # silver frost, as the field's grass; the platforms keep their darks
            if field:
                return rgb5(165 / 360, s * 0.22, v + (1 - v) * 0.70)
            return rgb5(170 / 360, s * 0.40, v + (1 - v) * 0.40 * v)
        return rgb5(h, s * 0.45, v + (1 - v) * (0.55 if field else 0.35))   # a dusting of snow
    if name == "autumn":
        if green:                            # the platforms' grass to gold and amber; the field to straw
            return rgb5((h * 360 - (48 if not field else 24)) / 360, s * (1.20 if not field else 0.95), v * (0.92 if not field else 0.97))
        return rgb5(h - 4 / 360, s * 1.08, v * 0.97)
    if name == "spring":
        if green:
            return rgb5((h * 360 - 8) / 360, s * 1.15, v + (1 - v) * 0.08)
        return rgb5(h, s * 1.04, v + (1 - v) * 0.05)
    return c


# the watch's sky, top band to horizon (five-bit), and how far the bands step toward it (sixteenths)
SKY = {
    "dawn":  (((20, 20, 28), (31, 24, 22)), 7),     # a pale lilac overhead, rose at the horizon
    "dusk":  (((16, 14, 22), (31, 19, 9)), 8),      # a dim slate overhead, amber at the horizon
    "night": (((3, 4, 11), (8, 10, 18)), 8),          # navy, a little lighter low down
}
SPRING_BLOOM = (31, 20, 24)                          # spring's glint, when no holiday has it


def tint(c, t):
    return tuple(min(31, (v * t[k][0] >> 8) + t[k][1]) for k, v in enumerate(c))


def quarter(t, q):
    """sWatchTint at q quarters of its strength -- daemons_time.c's DaemonsTintBattleForWatch"""
    return tuple((256 - (256 - m) * q // 4, a * q // 4) for m, a in t)


def seasoned(T, season_name):
    """Step 1 alone: the terrain's 48 colours in a season (the table --write emits)."""
    pal = list(T.pal)
    for pb in (2, 3, 4):
        for v in range(1, 16):
            i = (pb - 2) * 16 + v
            if pb in (2, 3) and v in T.sky:
                continue
            pal[i] = season(pal[i], season_name, field=(v in (1, 15)))
    if season_name == "spring":
        for pb in (2, 3):
            if T.glint[pb]:
                pal[(pb - 2) * 16 + T.glint[pb]] = SPRING_BLOOM
    return pal


def sky_targets(T, watch):
    """The watch's sky for each of the terrain's bands, top first: a straight run from its top to its horizon."""
    if watch not in SKY:
        return [(0, 0, 0)] * len(T.sky)
    (top, low), _ = SKY[watch]
    n = max(1, len(T.sky) - 1)
    return [tuple(a + (b - a) * rank // n for a, b in zip(top, low)) for rank in range(len(T.sky))]


def calendar_palette(T, watch="day", season_name="summer", weekday=None, holiday_colour=None, reach=FULL):
    """The terrain's 48 colours for one moment, as daemons_battle_bg.c makes them. reach: FULL (outdoors), INDOOR
    (the hour at a quarter, no season) or KEPT (no hour, no season: the cave, the arenas, the Elite rooms)."""
    W = watch_tint()
    # 1. the season, on the ground
    pal = seasoned(T, season_name) if reach == FULL else list(T.pal)
    # 2. the holiday's touch, on the glints
    if holiday_colour is not None:
        for pb in (2, 3):
            if T.glint[pb]:
                pal[(pb - 2) * 16 + T.glint[pb]] = holiday_colour
    # 3. row 3's free colours copy row 2's, so the horizon row reads the same in row 3; the accent takes the day
    for v in T.row3_free:
        if v != ACCENT:
            pal[16 + v] = pal[v]
    pal[16 + ACCENT] = weekday if weekday is not None else pal[1]
    # 4. the hour
    if reach != KEPT and watch != "day":
        t = quarter(W[watch], 4 if reach == FULL else 1)
        for i in range(48):
            pal[i] = tint(pal[i], t)
        if reach == FULL and watch in SKY:
            (top, low), k = SKY[watch]
            for v, target in zip(T.sky, sky_targets(T, watch)):
                for pb in (2, 3):
                    pal[(pb - 2) * 16 + v] = lerp(pal[(pb - 2) * 16 + v], target, k)
            # the scan line (1) runs through the field too, so it keeps the field's light; the day's line a quarter
            # step toward the horizon, so it sits in the sky it is drawn across
            pal[16 + ACCENT] = lerp(pal[16 + ACCENT], low, k // 4)
    return pal


# --- the measure the bible holds colour to (9.4): CIE76 from every type's hue, as genguide.py and gbadaytrim.py take it --

_G = None


def type_distance(c5):
    """(distance, type) from the nearest of the 18 type hues, on the GBA's colour as the screen shows it."""
    global _G
    if _G is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("genguide", os.path.join(ROOT, "tools", "genguide.py"))
        _G = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_G)
    hues = _G.type_hues()
    c = tuple(v << 3 for v in c5)
    return min((sum((a - b) ** 2 for a, b in zip(_G.lab(c), _G.lab(v))) ** .5, k) for k, v in hues.items())


def added_colours():
    """Every colour the calendar ADDS to a terrain, named: the seven trims, the twelve month colours, spring's bloom."""
    out = [(d, c) for d, c in zip(DAYS, day_trims())]
    out += [(m, c) for m, c in zip("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(), month_colours())]
    out.append(("BLOOM", SPRING_BLOOM))
    return out


# --- the write: src/data/battle_calendar.h ----------------------------------------------------------------------------

def rgb(c):
    return "RGB(%d, %d, %d)" % c


def plan():
    """Every terrain's row of the table, and the outdoor ones' seasons and skies."""
    rows, full = [], []
    for num, name, png, binp, pal in engine_terrains():
        reach = REACH.get(name, KEPT if name.startswith("BENCHMARK_") else None)
        if reach is None:
            raise SystemExit("  BATTLE_TERRAIN_%s has no reach: a new terrain is a decision (REACH, above)." % name)
        T = terrain_of(name, png, binp, pal)
        if not T.horizon or T.horizon_shared or ACCENT not in T.row3_free:
            raise SystemExit("  %s: no horizon line the patch can move alone (horizon %s, shared %s, row 3 free %s)"
                             % (name, T.horizon, T.horizon_shared, T.row3_free))
        if len(T.sky) > 6:
            raise SystemExit("  %s: %d sky bands; the table holds 6" % (name, len(T.sky)))
        index = None
        if reach == FULL:
            index = len(full)
            full.append(T)
        rows.append((num, name, reach, index, T))
    return rows, full


def header():
    rows, full = plan()
    bad = [(n, c) + type_distance(c) for n, c in added_colours()]
    bad = [b for b in bad if b[2] < MIN_TYPE_DISTANCE]
    if bad:
        raise SystemExit("  refused: %s" % "; ".join("%s %s is %.1f from %s" % b for b in bad))
    L = ["// Generated by DAEMONS tools/gbabattlebg.py --write --approved -- do not edit. T-481 A: the battle",
         "// backgrounds that keep the calendar (approved by the user 2026-10-29, by multiple choice). Read by",
         "// src/daemons_battle_bg.c only. Every terrain of sBattleTerrainTable, measured from its .png, .bin and .pal:",
         "// the horizon tile and line the weekday takes, each platform's glint, row 3's free colours, the sky bands",
         "// (top first); and for the outdoor ones the four seasons' palettes and the three watches' skies.",
         "",
         "#define BATTLE_CAL_FULL       0   // outdoors: the season, the holiday, the weekday, the hour",
         "#define BATTLE_CAL_INDOOR     1   // a building: the hour at a quarter, no season",
         "#define BATTLE_CAL_KEPT       2   // a cave, an arena, an Elite room: the weekday's line and the glints only",
         "#define BATTLE_CAL_ACCENT     %d  // row 3's colour that carries the day" % ACCENT,
         "#define BATTLE_CAL_NO_SEASON  0xFF",
         "",
         "struct BattleCalendarTerrain",
         "{",
         "    u8 reach;           // BATTLE_CAL_*",
         "    u8 index;           // into sBattleSeasonPals and sBattleSkyTargets, or BATTLE_CAL_NO_SEASON",
         "    u16 horizonTile;    // the horizon tile, in BG 3's tiles (BG_CHAR_ADDR(2))",
         "    u8 horizonRow;      // its tile row in the map (and + 32, the second screen)",
         "    u8 horizonLine;     // the pixel row inside it that is the line",
         "    u8 glint[2];        // the foe's platform's (row 2) and the player's (row 3); 0 for none",
         "    u16 freeMask;       // row 3's colours no tile draws, the accent left out: copied from row 2",
         "    u8 sky[6];          // row 2's sky bands, top first, 0-terminated",
         "};",
         "",
         "static const struct BattleCalendarTerrain sBattleCalendar[] = {"]
    for num, name, reach, index, T in rows:
        ty, ly, t = T.horizon
        sky = list(T.sky) + [0] * (6 - len(T.sky))
        L.append("    [BATTLE_TERRAIN_%s] = { %s, %s, %d, %d, %d, { %d, %d }, 0x%04X, { %s } },"
                 % (name, C_REACH[reach], "BATTLE_CAL_NO_SEASON" if index is None else index, t, ty, ly,
                    T.glint[2] or 0, T.glint[3] or 0, T.free_mask(), ", ".join(map(str, sky))))
    L += ["};", "",
          "// The outdoor terrains' 48 colours in each season (SEASON_* order), the sky as drawn -- the hour moves it.",
          "static const u16 sBattleSeasonPals[%d][SEASON_COUNT][48] = {" % len(full)]
    for i, T in enumerate(full):
        L.append("    [%d] = { // %s" % (i, T.name.upper()))
        for s in SEASONS:
            pal = seasoned(T, s)
            L.append("        [SEASON_%s] = {" % s.upper())
            for r in range(3):
                L.append("            %s," % ", ".join(rgb(c) for c in pal[r * 16:(r + 1) * 16]))
            L.append("        },")
        L.append("    },")
    L += ["};", "",
          "// Each outdoor terrain's sky bands' targets at each watch (WATCH_* order), top first: the watch's sky from",
          "// overhead to the horizon, stepped toward by sBattleSkyStep sixteenths. Day is as drawn.",
          "static const u16 sBattleSkyTargets[%d][WATCH_COUNT][6] = {" % len(full)]
    for i, T in enumerate(full):
        L.append("    [%d] = { // %s" % (i, T.name.upper()))
        for w in C_WATCHES:
            tg = sky_targets(T, w) if w in SKY else []
            tg = tg + [(0, 0, 0)] * (6 - len(tg))
            L.append("        [WATCH_%s] = { %s }," % (w.upper(), ", ".join(rgb(c) for c in tg)))
        L.append("    },")
    L += ["};", "",
          "static const u8 sBattleSkyStep[WATCH_COUNT] = { %s };"
          % ", ".join("[WATCH_%s] = %d" % (w.upper(), SKY[w][1] if w in SKY else 0) for w in C_WATCHES),
          "// the horizon's colour at each watch, which the day's line steps a quarter of the way toward",
          "static const u16 sBattleSkyLow[WATCH_COUNT] = { %s };"
          % ", ".join("[WATCH_%s] = %s" % (w.upper(), rgb(SKY[w][0][1]) if w in SKY else "0") for w in C_WATCHES),
          ""]
    return "\n".join(L)


# --- the report ----------------------------------------------------------------------------------------------------

def report():
    print("T-481 A -- the battle terrains as built (engineGba/graphics/battle_terrain), above the text box\n")
    print("%-22s %-6s %5s %-20s %-6s %-15s %-6s %s" % ("terrain", "reach", "tiles", "sky bands (row 2)", "field",
                                                     "horizon line", "glints", "row 3 free"))
    rows, full = plan()
    for num, name, reach, index, T in rows:
        hz = "y %d (tile %d)" % (T.horizon[0] * 8 + T.horizon[1], T.horizon[2])
        mis = T.horizon_mismatch()
        print("%-22s %-6s %5d %-20s y %-4d %-15s %-6s %s%s" % (
            name, reach, T.used_tiles, ",".join(map(str, T.sky)), T.field_top, hz,
            "%s/%s" % (T.glint[2], T.glint[3]), ",".join(map(str, T.row3_free)),
            "  (the horizon row's %s in row 3 is a step from row 2's)" % ",".join(map(str, mis)) if mis else ""))
    print("\n  Every terrain loads THREE rows (BG 2-4, 48 colours); row 4 is the intro's tufts, BG 1. The horizon tile of")
    print("  every one is drawn in its own row only, and row 3's colour %d is free in every one." % ACCENT)
    print("\nThe colours the calendar adds, CIE76 from the nearest type hue (9.4 asks 20; held here to %d):" % MIN_TYPE_DISTANCE)
    for n, c in added_colours():
        print("  %-9s RGB%-13s %4.1f from %s" % ((n, c) + type_distance(c)))
    for w in ("dawn", "dusk", "night"):
        (top, low), k = SKY[w]
        print("  %-9s sky %s -> %s, %d/16 a step (%4.1f / %4.1f from the nearest hue; a step toward, never the colour)"
              % (w.upper(), top, low, k, type_distance(top)[0], type_distance(low)[0]))
    drawn = min(type_distance(T.pal[v])[0] for T in full for v in T.sky)
    print("  (the sky as DRAWN is already %.1f from a hue -- a blue sky beside WATER's and FLYING's -- so 9.4's line holds"
          " the colours the calendar adds, as the draft took it; the hour moves the terrain's own colours, the field's"
          " way)" % drawn)
    season_b = len(full) * 4 * 48 * 2
    sky_b = len(full) * 4 * 6 * 2
    table_b = len(rows) * 16
    print("\nCOST: EWRAM 0, IWRAM 0, SAVE 0. ROM: seasons %d outdoor terrains x 4 x 48 x 2 B = %d B, skies %d B, the "
          "terrain table %d B, ~600 B of code. CPU: once per terrain load, 48 colours through a multiply and a step, and "
          "one 32-bit tile write and 64 map halfwords in VRAM." % (len(full), season_b, sky_b, table_b))
    want = header()
    path = os.path.join(GBA, OUT_REL)
    have = open(path).read() if os.path.exists(path) else None
    if have == want:
        print("  the engine matches `--write --approved` exactly (%s)" % OUT_REL)
        return 0
    print("  !! %s %s what `--write --approved` would write -- run it, or find which side is right"
          % (OUT_REL, "is missing:" if have is None else "differs from"))
    return 1


def write():
    want = header()
    path = os.path.join(GBA, OUT_REL)
    have = open(path).read() if os.path.exists(path) else None
    if have == want:
        print("  %s already holds this; nothing written" % OUT_REL)
        return 0
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(want)
    os.replace(tmp, path)
    print("  wrote %s (%d lines)" % (OUT_REL, want.count("\n")))
    return 0


# --- the sheets ----------------------------------------------------------------------------------------------------

def label(d, xy, text, font=None, fill=(30, 30, 36)):
    d.text(xy, text, font=font or SMALL, fill=fill)


def scale(im, k=2):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def grid_sheet(T, out, reach, title, weekday, note):
    cw, ch = VIS_W * 2, VIS_H * 2
    pad, lw, th = 12, 78, 64
    sheet = Image.new("RGB", (lw + 5 * (cw + pad) + pad, th + 4 * (ch + pad + 16) + pad), (244, 244, 246))
    d = ImageDraw.Draw(sheet)
    label(d, (pad, 10), title, FONT)
    label(d, (pad, 30), note)
    label(d, (pad, 44), "Every cell has the weekday's horizon line (%s) -- the 1px line above the field." % weekday[0])
    cols = ("TODAY (as built)",) + tuple(w.upper() for w in WATCHES)
    for c, name in enumerate(cols):
        label(d, (lw + pad + c * (cw + pad), th - 14), name, FONT)
    for r, s in enumerate(SEASONS):
        y = th + r * (ch + pad + 16)
        label(d, (pad, y + ch // 2), s.upper(), FONT)
        sheet.paste(scale(T.render(T.pal, accent=False)), (lw + pad, y))
        for c, w in enumerate(WATCHES):
            pal = calendar_palette(T, w, s, weekday=weekday[1], reach=reach)
            sheet.paste(scale(T.render(pal)), (lw + pad + (c + 1) * (cw + pad), y))
    sheet.save(out)
    return out


def week_sheet(T, out):
    trims = day_trims()
    cw, ch = VIS_W * 2, VIS_H * 2
    pad = 12
    zoom = 4
    zh = 16 * zoom
    sheet = Image.new("RGB", (pad + 4 * (cw + pad), 60 + 2 * (ch + zh + 40)), (244, 244, 246))
    d = ImageDraw.Draw(sheet)
    label(d, (pad, 10), "T-481 A -- the week on the horizon (%s, summer day; the line is row 3's colour %d)"
          % (T.name.upper(), ACCENT), FONT)
    label(d, (pad, 30), "One 1px line in the day's CHECKPOINT trim (day_trims.h). Under each: the line at 4x.")
    hz = T.horizon[0] * 8 + T.horizon[1]
    for k, (day, c) in enumerate(zip(DAYS, trims)):
        x = pad + (k % 4) * (cw + pad)
        y = 52 + (k // 4) * (ch + zh + 40)
        pal = calendar_palette(T, "day", "summer", weekday=c)
        im = T.render(pal)
        sheet.paste(scale(im), (x, y + 16))
        crop = im.crop((0, hz - 8, VIS_W // 2, hz + 8)).resize((VIS_W // 2 * zoom, zh), Image.NEAREST)
        sheet.paste(crop.crop((0, 0, cw, zh)), (x, y + 16 + ch + 4))
        label(d, (x, y), "%s  RGB%s" % (day, c), FONT)
    x, y = pad + 3 * (cw + pad), 52 + (ch + zh + 40)
    pal = calendar_palette(T, "night", "summer", weekday=trims[6])
    im = T.render(pal)
    sheet.paste(scale(im), (x, y + 16))
    crop = im.crop((0, hz - 8, VIS_W // 2, hz + 8)).resize((VIS_W // 2 * zoom, zh), Image.NEAREST)
    sheet.paste(crop.crop((0, 0, cw, zh)), (x, y + 16 + ch + 4))
    label(d, (x, y), "SATURDAY at NIGHT", FONT)
    sheet.save(out)
    return out


def holiday_sheet(T, out):
    months = month_colours()
    hm = holiday_months()
    name = "MASK NIGHT"
    month, quiet = hm.get(name, (10, False))
    colour = months[month - 1]
    trims = day_trims()
    sat = trims[6]                           # 2026-10-31 is a Saturday
    cw, ch = VIS_W * 2, VIS_H * 2
    pad = 12
    sheet = Image.new("RGB", (pad + 3 * (cw + pad), 64 + 2 * (ch + 40)), (244, 244, 246))
    d = ImageDraw.Draw(sheet)
    label(d, (pad, 10), "T-481 A -- a holiday's one touch: %s (CONTENT, autumn, a Saturday)" % name, FONT)
    label(d, (pad, 30), "Above: the day before, ordinary. Below: %s -- each platform's glint in the month colour it "
                        "wears (OCT, RGB%s). Not on a QUIET holiday." % (name, colour))
    for r, hol in enumerate((None, colour)):
        for c, w in enumerate(("day", "dusk", "night")):
            x, y = pad + c * (cw + pad), 56 + r * (ch + 40)
            pal = calendar_palette(T, w, "autumn", weekday=trims[5] if hol is None else sat, holiday_colour=hol)
            sheet.paste(scale(T.render(pal)), (x, y + 16))
            label(d, (x, y), ("FRIDAY 30 OCT, " if hol is None else "%s, SATURDAY 31 OCT, " % name) + w.upper(), FONT)
    sheet.save(out)
    return out


def reach_sheet(out):
    """What the cave and the building get: the cave keeps its own light; the building has the hour at a quarter."""
    trims = day_trims()
    cw, ch = VIS_W * 2, VIS_H * 2
    pad = 12
    sheet = Image.new("RGB", (pad + 5 * (cw + pad), 60 + 2 * (ch + 40)), (244, 244, 246))
    d = ImageDraw.Draw(sheet)
    label(d, (pad, 10), "T-481 A -- the REACH: the cave keeps its own light; the building has the hour at a quarter, "
                        "through the windows; neither has the season", FONT)
    label(d, (pad, 30), "Both keep the weekday's line (WEDNESDAY here) and a holiday's glints.")
    for r, (name, reach) in enumerate((("cave", KEPT), ("building", INDOOR))):
        T = Terrain(name)
        x, y = pad, 52 + r * (ch + 40)
        sheet.paste(scale(T.render(T.pal, accent=False)), (x, y + 16))
        label(d, (x, y), "%s TODAY" % name.upper(), FONT)
        for c, w in enumerate(WATCHES):
            x = pad + (c + 1) * (cw + pad)
            pal = calendar_palette(T, w, "winter", weekday=trims[3], reach=reach)
            sheet.paste(scale(T.render(pal)), (x, y + 16))
            label(d, (x, y), "%s, %s" % (name.upper(), w.upper()), FONT)
    sheet.save(out)
    return out


def sheets(outdir):
    os.makedirs(outdir, exist_ok=True)
    trims = day_trims()
    wed = ("WEDNESDAY", trims[3])
    made = [
        grid_sheet(Terrain("grass"), os.path.join(outdir, "t481a_grass.png"), FULL,
                   "T-481 A -- GRASS: today beside each hour, in each season", wed,
                   "The hour: the field's own light (sWatchTint) on all, and the sky bands a step toward the watch's "
                   "sky. The season: the ground and both platforms."),
        week_sheet(Terrain("grass"), os.path.join(outdir, "t481a_week.png")),
        holiday_sheet(Terrain("grass"), os.path.join(outdir, "t481a_holiday.png")),
        reach_sheet(os.path.join(outdir, "t481a_reach.png")),
    ]
    for m in made:
        print(m)


def main():
    if "--sheet" in sys.argv:
        sheets(sys.argv[sys.argv.index("--sheet") + 1])
        return 0
    if "--write" in sys.argv:
        if "--approved" not in sys.argv:
            print("  --write refused without --approved: the look is the one the user answered on 2026-10-29 "
                  "(T-481 A); --write --approved writes it.")
            return 1
        return write()
    return report()


if __name__ == "__main__":
    sys.exit(main())

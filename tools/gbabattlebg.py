#!/usr/bin/env python3
"""T-481 part A: THE BATTLE BACKGROUNDS THAT KEEP THE CALENDAR -- a draft, on sheets, before anything is built.

    python3 tools/gbabattlebg.py                 # report: every terrain's palette, what it draws with, and the cost
    python3 tools/gbabattlebg.py --sheet OUTDIR  # the sheets: grass, cave, building, the week, a holiday

It has no --write. Nothing in the engine changes until the user picks a look (T-481: "draft each surface on a sheet
first ... then build A, B, C in that order").

WHAT IS THERE (measured, every terrain). A battle terrain is one tileset, one 32x64 tilemap and three BG palette rows,
BG 2-4 (battle_bg.c: LoadCompressedPalette(..., BG_PLTT_ID(2), 3 * PLTT_SIZE_4BPP)). The layout is the same in every
outdoor terrain and in both building ones:
    row 2  1 the scan line every fourth pixel row, sky and field alike; 10-14 the backdrop's bands (the sky);
           15 the field; 2-9 the foe's platform
    row 3  the player's platform, 2-9; its 1 and 15 copy row 2's, and its 10-14 are copies NO TILE DRAWS -- in every
           terrain. Five free colours, already loaded, already in the palette RAM.
    row 4  the entry animation's tufts (BG 1, the intro only)
The bottom 48 pixels are under the battle's text box (palette 0) and are not drawn here.

THE MECHANISM (the cheapest that is faithful). One function, after the terrain's palette loads and before the
weather's wash (daemons_weather.c DaemonsTintBattleTerrain), at the two places battle_bg.c loads it:
  1. THE SEASON -- what the ground IS goes first, as in the field (T-359): the field and both platforms (2-9, 15,
     and row 4's tufts) from a table the tool writes, one per outdoor terrain per season; summer is as drawn,
     with a little sun.
  2. THE HOLIDAY -- one touch: each platform's GLINT (its brightest sparse colour, found below) takes the month
     colour the holiday wears (DaemonsHolidayMonth -> DaemonsMonthColour). Not on a QUIET holiday. An ordinary day
     keeps the glints as drawn.
  3. THE WEEKDAY -- one line, the horizon: the backdrop's last scan line above the field (grass: y 29) is repainted,
     in VRAM, from colour 1 to colour 12, and that tile row's 30 map entries move to row 3, whose 12 is free -- so
     the line, and only the line, takes the day's CHECKPOINT trim (day_trims.h). Four bytes of one tile and 32 map
     halfwords, done after the tiles decompress; no art is redrawn and no ROM tile changes.
  4. THE HOUR -- the watch's light, the field's own sum (daemons_time.c sWatchTint) on everything, so the battle is
     lit as the route outside it was; and on the sky bands only, a step toward the watch's sky (dawn's pale rose,
     dusk's amber, night's navy). Day is as drawn.
  then the weather's wash, as now; then HALFTONE's grey and the four tones, which run over every palette anyway.

THE COST, against docs/engine.md's budgets (EWRAM 696 B free, IWRAM 2.7 KB, ROM 5.9 MB):
  EWRAM  none -- every input is asked of the clock when the battle starts, and the result goes into the palette
         buffers that already exist. IWRAM none. SAVE none.
  ROM    the season tables: 3 seasons x the outdoor terrains x 2 rows x 16 colours x 2 bytes (see the report's line),
         the four skies (4 x 5 x 2 bytes), the horizon and glint per terrain (a few bytes each), ~400 bytes of code.
  CPU    once per terrain load: 48 colours through a multiply and a blend, 4 + 32 halfwords into VRAM -- a few
         thousand cycles, under 2% of one frame.
"""
import colorsys, os, re, struct, sys
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
TERR = os.path.join(GBA, "graphics/battle_terrain")
VIS_W, VIS_H = 240, 112          # the screen above the text box

OUTDOOR = ("grass", "longgrass", "sand", "mountain", "water", "pond", "underwater")
ALL = OUTDOOR + ("cave", "building")
WATCHES = ("dawn", "day", "dusk", "night")
SEASONS = ("winter", "spring", "summer", "autumn")
DAYS = ("SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY")
ACCENT = 12                      # row 3's free colour that carries the day

try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    SMALL = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
except OSError:
    FONT = SMALL = ImageFont.load_default()


# --- what the engine is built from ----------------------------------------------------------------------------------

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


def gbapal(path):
    d = open(path, "rb").read()
    return [((c & 31), (c >> 5) & 31, (c >> 10) & 31) for c in struct.unpack("<%dH" % (len(d) // 2), d)]


class Terrain:
    def __init__(self, name, palette=None):
        d = os.path.join(TERR, name)
        self.name = name
        self.tiles = bytearray(open(os.path.join(d, "terrain.4bpp"), "rb").read())
        self.map = list(struct.unpack("<2048H", open(os.path.join(d, "terrain.bin"), "rb").read()))
        self.pal = gbapal(palette or os.path.join(d, "terrain.gbapal"))
        self.measure()

    def px(self, x, y, tiles=None, tmap=None):
        tiles, tmap = tiles or self.tiles, tmap or self.map
        e = tmap[(y // 8) * 32 + x // 8]
        t, hf, vf, pb = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
        sx, sy = (7 - x % 8) if hf else x % 8, (7 - y % 8) if vf else y % 8
        b = tiles[t * 32 + sy * 4 + sx // 2]
        return pb, (b >> 4) if sx & 1 else b & 15

    def measure(self):
        self.count = {2: Counter(), 3: Counter()}
        ys = {}
        for y in range(VIS_H):
            for x in range(VIS_W):
                pb, v = self.px(x, y)
                if pb in self.count:
                    self.count[pb][v] += 1
                    ys.setdefault((pb, v), set()).add(y)
        # the field: the first pixel row drawn in row 2's 15 from edge to edge
        self.field_top = next(y for y in range(VIS_H) if all(self.px(x, y) == (2, 15) for x in range(VIS_W)))
        # the sky: row 2's colours drawn only above the field (the scan line 1 runs through both, so it is not one)
        self.sky = sorted((v for (pb, v), s in ys.items() if pb == 2 and v not in (0, 1) and max(s) < self.field_top),
                          key=lambda v: sum(ys[(2, v)]) / len(ys[(2, v)]))
        self.ground = {pb: sorted(v for v in self.count[pb] if v and v not in self.sky) for pb in (2, 3)}
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
        used_elsewhere = [k for k, e in enumerate(self.map) if self.horizon and (e & 0x3FF) == self.horizon[2]
                          and k // 32 not in (self.horizon[0], self.horizon[0] + 32)]
        self.horizon_shared = bool(used_elsewhere)
        r2, r3 = self.pal[0:16], self.pal[16:32]
        self.row3_copies = all(r3[i] == r2[i] for i in (1, 15)) and all(r3[i] == r2[i] for i in range(10, 15))
        self.row3_free = [i for i in range(1, 16) if not self.count[3][i]]

    def with_accent(self):
        """The tiles and map with the horizon line moved to row 3's ACCENT -- what the VRAM patch would leave."""
        tiles, tmap = bytearray(self.tiles), list(self.map)
        if self.horizon:
            ty, ly, t = self.horizon
            for k in range(4):
                tiles[t * 32 + ly * 4 + k] = ACCENT << 4 | ACCENT
            for row in (ty, ty + 32):
                for tx in range(32):
                    e = tmap[row * 32 + tx]
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


# --- the draft's sums, in five-bit colour, as the cartridge would do them --------------------------------------------

def to8(c):
    return tuple(v * 255 // 31 for v in c)


def hsv5(c):
    return colorsys.rgb_to_hsv(*(v / 31 for v in c))


def rgb5(h, s, v):
    return tuple(min(31, max(0, round(k * 31))) for k in colorsys.hsv_to_rgb(h % 1, max(0, min(1, s)), max(0, min(1, v))))


def lerp(a, b, k16):
    """a step from a toward b, by sixteenths -- the engine's own BlendPalette arithmetic."""
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


def calendar_palette(T, watch="day", season_name="summer", weekday=None, holiday_colour=None, reach="full"):
    """The terrain's 48 colours for one moment. reach: 'full' (outdoors), 'indoor' (the hour at a quarter, through the
    windows; no season) or 'kept' (no hour, no season -- the cave)."""
    W = watch_tint()
    pal = list(T.pal)
    rows = (2, 3, 4)
    # 1. the season, on the ground
    if reach == "full":
        for pb in rows:
            for v in range(1, 16):
                i = (pb - 2) * 16 + v
                if pb in (2, 3) and v in T.sky:
                    continue
                pal[i] = season(pal[i], season_name, field=(v in (1, 15)))
        if season_name == "spring" and holiday_colour is None:
            for pb in (2, 3):
                if T.glint[pb]:
                    pal[(pb - 2) * 16 + T.glint[pb]] = SPRING_BLOOM
    # 2. the holiday's touch, on the glints
    if holiday_colour is not None:
        for pb in (2, 3):
            if T.glint[pb]:
                pal[(pb - 2) * 16 + T.glint[pb]] = holiday_colour
    # row 3's free bands copy row 2's, so the horizon row reads the same when it moves to row 3 (its 1 and 15 are
    # the player's platform's and stay; they match row 2's but for one step of green in LONG GRASS)
    for v in (10, 11, 13, 14):
        pal[16 + v] = pal[v]
    # 3. the weekday, on the horizon line
    pal[16 + ACCENT] = weekday if weekday is not None else pal[1]
    # 4. the hour
    if reach != "kept" and watch != "day":
        t = W[watch]
        if reach == "indoor":                # a quarter of the way to the watch's light
            t = tuple((256 - (256 - m) // 4, a // 4) for m, a in t)
        sky = set(T.sky)
        for i in range(48):
            pal[i] = tint(pal[i], t)
        if reach == "full" and watch in SKY:
            (top, low), k = SKY[watch]
            n = max(1, len(T.sky) - 1)
            for rank, v in enumerate(T.sky):
                target = tuple(a + (b - a) * rank // n for a, b in zip(top, low))
                for pb in (2, 3):
                    pal[(pb - 2) * 16 + v] = lerp(pal[(pb - 2) * 16 + v], target, k)
            # the scan line (1) runs through the field too, so it keeps the field's light; the day's line a quarter
            # step toward the horizon, so it sits in the sky it is drawn across
            pal[16 + ACCENT] = lerp(pal[16 + ACCENT], low, k // 4)
    return pal


# --- the measure the bible holds colour to (9.4): CIE76 from every type's hue, as genguide.py and gbadaytrim.py take it --

def type_distance(c5):
    """(distance, type) from the nearest of the 18 type hues, on the GBA's colour as the screen shows it."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("genguide", os.path.join(ROOT, "tools", "genguide.py"))
    G = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(G)
    hues = G.type_hues()
    c = tuple(v << 3 for v in c5)
    return min((sum((a - b) ** 2 for a, b in zip(G.lab(c), G.lab(v))) ** .5, k) for k, v in hues.items())


# --- the report ----------------------------------------------------------------------------------------------------

def report():
    print("T-481 A -- the battle terrains as built (engineGba/graphics/battle_terrain), above the text box\n")
    print("%-11s %5s %4s %-22s %-10s %-14s %-9s %s" % ("terrain", "tiles", "used", "sky bands (row 2)", "field top",
                                                     "horizon line", "glints", "row 3 free"))
    seasonal = 0
    for name in ALL:
        T = Terrain(name)
        used = sum(1 for pb in (2, 3) for v in T.count[pb] if v)
        hz = "y %d (tile %d)" % (T.horizon[0] * 8 + T.horizon[1], T.horizon[2]) if T.horizon else "none"
        if T.horizon_shared:
            hz += " SHARED"
        print("%-11s %5d %4d %-22s y %-8d %-14s %-9s %s%s" % (
            name, len(T.tiles) // 32, used, ",".join(map(str, T.sky)), T.field_top, hz,
            "%s/%s" % (T.glint[2], T.glint[3]), ",".join(map(str, T.row3_free)),
            "" if T.row3_copies else "  (row 3 differs from row 2 by a step: %s)" % ",".join(
                str(i) for i in [1] + list(range(10, 16)) if T.pal[i] != T.pal[16 + i])))
        if name in OUTDOOR:
            seasonal += 1
    indoor_pals = [f for f in os.listdir(os.path.join(TERR, "indoor")) if f.endswith(".gbapal")]
    print("\n  + %d palettes over the building/indoor tiles (gym, leader, link, plain, the Elite rooms, the eight "
          "BENCHMARK arenas)." % len(indoor_pals))
    print("  Every terrain loads THREE rows (BG 2-4, 48 colours); row 4 is the intro's tufts, BG 1.")
    trims, months = day_trims(), month_colours()
    print("\nThe colours the draft adds, CIE76 from the nearest type hue (9.4 asks 20; the trims were made 22+):")
    for d, c in zip(DAYS, trims):
        print("  %-9s RGB%-13s %4.1f from %s" % ((d, c) + type_distance(c)))
    for m, c in zip(("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC").split(), months):
        print("  %-9s RGB%-13s %4.1f from %s   (a holiday's glint)" % ((m, c) + type_distance(c)))
    print("  %-9s RGB%-13s %4.1f from %s   (spring's bloom)" % (("BLOOM", SPRING_BLOOM) + type_distance(SPRING_BLOOM)))
    rom = 3 * seasonal * 2 * 16 * 2 + 3 * 16 * 2 * seasonal // 2
    print("\nCOST: EWRAM 0, IWRAM 0, SAVE 0. ROM: season tables 3 x %d outdoor terrains x 2 rows x 16 x 2 B = %d B "
          "(+ row 4's tufts, %d B), skies 40 B, horizon/glint 4 B a terrain, ~400 B code. CPU: once per terrain load, "
          "48 colours + 36 halfwords of VRAM, a few thousand cycles." % (seasonal, 3 * seasonal * 2 * 16 * 2,
                                                                          3 * seasonal * 16 * 2))
    print("Nothing is written: the draft is the sheets (--sheet OUTDIR).")


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
    label(d, (pad, 10), "T-481 A DRAFT -- the week on the horizon (%s, summer day; the line is row 3's colour %d)"
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
    # the eighth cell: the same day at night, to show the line holds under the light
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
    label(d, (pad, 10), "T-481 A DRAFT -- a holiday's one touch: %s (CONTENT, autumn, a Saturday)" % name, FONT)
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
    """What the cave and the building get if the hour and season do NOT reach them (the recommended reach)."""
    trims = day_trims()
    cw, ch = VIS_W * 2, VIS_H * 2
    pad = 12
    sheet = Image.new("RGB", (pad + 5 * (cw + pad), 60 + 2 * (ch + 40)), (244, 244, 246))
    d = ImageDraw.Draw(sheet)
    label(d, (pad, 10), "T-481 A DRAFT -- the recommended REACH: the cave keeps its own light; the building has the "
                        "hour at a quarter, through the windows; neither has the season", FONT)
    label(d, (pad, 30), "Both keep the weekday's line (WEDNESDAY here) and a holiday's glints. Compare the full-reach "
                        "grids, t481a_cave.png and t481a_building.png.")
    for r, (name, reach) in enumerate((("cave", "kept"), ("building", "indoor"))):
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
        grid_sheet(Terrain("grass"), os.path.join(outdir, "t481a_grass.png"), "full",
                   "T-481 A DRAFT -- GRASS: today beside each hour, in each season", wed,
                   "The hour: the field's own light (sWatchTint) on all, and the sky bands a step toward the watch's "
                   "sky. The season: the ground and both platforms."),
        grid_sheet(Terrain("cave"), os.path.join(outdir, "t481a_cave.png"), "full",
                   "T-481 A DRAFT -- CAVE, if everything reached it (not recommended: see t481a_reach.png)", wed,
                   "The same sums as the grass. A cave has no sky, so its bands are its ceiling: the hour tints them "
                   "as if they were."),
        grid_sheet(Terrain("building"), os.path.join(outdir, "t481a_building.png"), "full",
                   "T-481 A DRAFT -- BUILDING, if everything reached it (not recommended: see t481a_reach.png)", wed,
                   "The building's tiles are also the gym's, the leaders', the Elite rooms' and the eight BENCHMARK "
                   "arenas' (their own palettes)."),
        week_sheet(Terrain("grass"), os.path.join(outdir, "t481a_week.png")),
        holiday_sheet(Terrain("grass"), os.path.join(outdir, "t481a_holiday.png")),
        reach_sheet(os.path.join(outdir, "t481a_reach.png")),
    ]
    for m in made:
        print(m)


def main():
    if "--write" in sys.argv:
        sys.exit("gbabattlebg.py has no --write: T-481 A is a draft until the user picks a look.")
    if "--sheet" in sys.argv:
        sheets(sys.argv[sys.argv.index("--sheet") + 1])
    else:
        report()


if __name__ == "__main__":
    main()

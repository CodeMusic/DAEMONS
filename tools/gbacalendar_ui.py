#!/usr/bin/env python3
"""T-481 parts B and C: THE MENUS AND THE FIELD THAT KEEP THE CALENDAR.

    python3 tools/gbacalendar_ui.py                     # report: what exists, each surface's slots, the cost, the 9.4
                                                        #   check, and whether the engine holds what --write would write
    python3 tools/gbacalendar_ui.py --write --approved  # src/data/calendar_panes.h into the engine (approved 2026-10-29)
    python3 tools/gbacalendar_ui.py --sheet OUTDIR      # the sheets: B (START, text box, SUMMARY, INDEX), C (a town)

THE USER'S ANSWERS (2026-10-29, by multiple choice, on the draft's sheets -- qa private 29Oct2026 T481 52-58), which
--write builds and the engine's src/daemons_calendar_pane.c and fieldmap.c follow:
  START    T-318's wash RETIRED: the frame keeps its style's own colours, and the day goes on the eight inner-corner
           pixels only (index 12; styles 1, 3, 4 and 5, the one drawing that has them -- the others are other
           drawings and take the hour alone); the hour and the holiday (the inner bevel, 11) as drafted.
  HOUR     in menus and panes at HALF strength (sWatchTint at two quarters), on frames and backdrops only -- never the
           paper or any ink, so the text's contrast is the day's.
  WEEKDAY  the text box: the outer-corner flecks (15.14); SUMMARY: the 1px line under the title bar (0.6); INDEX: the
           box's corners (0.8). The draft's slots. NO SEASON IN THE MENUS.
  HOLIDAY  the text box's inner corner flecks (15.11), START's inner bevel (14.11) and SUMMARY's title pip (0.14) take
           the month colour as drafted; the INDEX's corners take the month for that day (the day yields); in the field,
           on a non-quiet holiday with no field look of its own, petal 11 takes the month colour.
  FIELD    beside T-275's rotunda, the water's crest (option W: General rows 4 and 6, index 1) takes the day's trim, at
           the palette load and before the faded print and the watch, so T-483's pulse, the weather and the fades stay
           on top and nothing compounds. (Option F and the season's paper whisper were declined.)

The rules are part A's, as the user set them by multiple choice (2026-10-29, TODO T-481): the hour, the season and
the holidays; and THE WEEKDAY AS A FINE ACCENT, ONE DETAIL, NEVER A WASH -- "noticed on the seventh day, not the
first". Every colour this adds is held to 22 (CIE76) from every type hue, as gbabattlebg.py holds A's. No new words:
the sheets draw ink as grey bars, never text. The sums are A's own (gbabattlebg.py: sWatchTint by quarters, the
five-bit lerp), so what a sheet shows is what the cartridge would draw.

WHAT EXISTS ALREADY (measured in the engine; nothing here is duplicated):
  T-275  the CHECKPOINT rotunda's trim, General row 2 index 8, takes the day's colour as the field's palette loads
         (fieldmap.c LoadTilesetPalette) -- THE FIELD'S WEEKDAY DETAIL, BUILT, in every town with a rotunda (9 of 12
         Kanto towns measured; no route has one).
  T-318  the START menu's frame (styles 1, 3, 4, 5: indices 10 dark, 14 body, 13 light) is WHOLLY the day's colour
         (start_menu.c DaemonsThemeMenuFrame) -- a wash of the frame, by the user's earlier decision.
  T-268  the field's hour: sWatchTint as tileset and object palettes load, outdoors only. Menus, the text box, the
         SUMMARY and the INDEX are untouched by it.
  T-359  the field's season: General palette 0's trees, grass and petals (and the greens other rows copy), outdoors
         on General maps (fieldmap.c DaemonsSeasonColour; tools/gbaseasons.py).
  T-416  the field's holiday looks, six flags: LANTERN, FROST, SNOW LIGHT, BRIGHT DAY (sHolidayLift, a step after the
         watch), FIR GLOW (the found fir), VIOLET BLOOM (petals 9-11 in NOV's purple); and the holiday skies
         (weather rows) and FIREWORKS. 19 of CONTENT's 24 holidays have NO palette look in the field.
  T-481 A  the battle backgrounds, all four (tools/gbabattlebg.py, src/daemons_battle_bg.c).
  T-483  the pulse at the copy to PLTT (daemons_pulse.c), T-415's weather on the faded buffer, T-442's restores (OBJ
         palettes only): all run after a palette loads, so anything done AT the load is tinted, faded, weathered and
         pulsed once, exactly as T-275's trim is.

B, THE MENUS AND PANES (proposed). One function, DaemonsCalendarPane(pal, surface), after each surface's palette
loads -- four call sites, each one line -- on a table this tool would write:
  THE WEEKDAY  one sparse slot per surface, the day's trim (day_trims.h), nothing else:
               TEXT BOX  palette 15 index 14, the frame's twelve corner flecks (3 px at each corner)
               START     index 12, the frame's eight inner-corner pixels -- if T-318's wash is thinned (a question)
               SUMMARY   BG row 0 index 6, the 1px line under the title bar (112 px; A's horizon line, again)
               INDEX     BG row 0 index 8, the box's corners (4 px each)
  THE HOUR     sWatchTint at HALF strength on the frame or backdrop colours only -- never the paper, never an ink,
               so text contrast is the day's. Day is as drawn.
  THE SEASON   drawn as the paper a whisper (3/16) toward the season's tone -- and it FAILS 9.4's line: a
               near-white is boxed in, cooler is ICE's and warmer NORMAL's (the report). A question, not a proposal.
  THE HOLIDAY  one sparse slot per surface in the month colour ITSELF, as A's glints (never on a QUIET holiday;
               nothing on an ordinary day): the text box's inner corner flecks (11), START's inner bevel (11), the
               SUMMARY title bar's white pip (14); the INDEX has no free colour, so its corners take the month
               instead of the day. Every blend of a trim or a month colour tried failed 22 (the report).

C, THE FIELD (proposed). Hour (T-268) and season (T-359) are built and stay as they are. Two additions, both in
LoadTilesetPalette beside T-275's line, before the faded print and the watch:
  THE WEEKDAY, beyond the towns (two options):  W  the water's crest -- General rows 4 and 6 index 1, the brightest
               glint on sea and pond, in the day's trim;  F  the flower's heart -- General row 0 index 9, the
               lightest petal, in the day's trim (not in winter: the season's frost keeps it).
  THE HOLIDAY  every non-quiet holiday with no field look of its own: the petal's own colour (index 11) in its
               month's colour, the light parts kept -- VIOLET BLOOM's idea given the holiday's month.

THE COST: EWRAM 0, IWRAM 0, SAVE 0. ROM: the report's lines. CPU: once per palette load. The field's palette
signature already carries the weekday (bits 3-5) and a bloom (look = HOLIDAY_LIFT_COUNT).
"""
import importlib.util, os, struct, sys
from collections import Counter
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
GBA = os.path.join(ROOT, "engineGba")
GFX = os.path.join(GBA, "graphics")


def _load(name):
    argv, sys.argv = sys.argv, sys.argv[:1]
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.argv = argv
    return mod


A = _load("gbabattlebg")          # part A: the trims, the month colours, sWatchTint, the sums, the 9.4 measure
DAYS, WATCHES, SEASONS = A.DAYS, A.WATCHES, A.SEASONS
MIN = A.MIN_TYPE_DISTANCE
HOUR_Q = 2                        # the menus' hour: sWatchTint at two quarters
PAPER_STEP = 3                    # sixteenths toward the season's paper tone
PAPER = {"winter": (26, 29, 31), "spring": (27, 31, 26), "autumn": (31, 27, 21)}   # summer: as drawn
SUBTLE_PURPLE = (22, 10, 19)      # new_menu_helpers.c sSubtlePurple, in the dialogue palette's slot 10 (T-459)

TRIMS = A.day_trims()
MONTHS = A.month_colours()
HOLS = A.holiday_months()


def pal5_png(path, rows=None):
    """A picture's own palette in five bits, as gbagfx makes its .gbapal (c >> 3) -- read from the .png, which git
    holds, rather than the .gbapal the build makes and ignores (a fresh clone, or check_generators' sandbox, has none)."""
    im = Image.open(path)
    p = im.getpalette()
    out = [(p[3 * i] >> 3, p[3 * i + 1] >> 3, p[3 * i + 2] >> 3) for i in range(len(p) // 3)]
    return out if rows is None else out[:rows * 16]


def hour(c, watch):
    if watch == "day":
        return c
    return A.tint(c, A.quarter(A.watch_tint()[watch], HOUR_Q))


# --- the B surfaces: each one an image of (row, index) cells, its palette rows, and the slots each part takes --------

class Surface:
    """name; cells[y][x] = (row, index) or None; rows {row: 16 colours}; the roles."""

    def __init__(self, name, cells, rows, accent, hour_slots, paper, holiday, note):
        self.name, self.cells, self.rows = name, cells, rows
        self.accent, self.hour_slots, self.paper, self.holiday, self.note = accent, hour_slots, paper, holiday, note
        self.h, self.w = len(cells), len(cells[0])

    def count(self):
        return Counter(c for row in self.cells for c in row if c)

    def palette(self, day=None, watch="day", season="summer", month=None, wash=None):
        """{(row, idx): colour}, as DaemonsCalendarPane would leave it. wash: T-318's frame (START as built)."""
        p = {(r, i): c for r, cs in self.rows.items() for i, c in enumerate(cs)}
        if wash is not None:
            p.update(wash)
        if season in PAPER:
            for s in self.paper:
                p[s] = A.lerp(p[s], PAPER[season], PAPER_STEP)
        if day is not None and self.accent:
            p[self.accent] = TRIMS[day]
        if month is not None and self.holiday:          # the month colour itself, as A's glints: never a blend
            p[self.holiday] = MONTHS[month - 1]
        for s in self.hour_slots + ([self.accent] if self.accent else []) + ([self.holiday] if self.holiday else []):
            p[s] = hour(p[s], watch)
        return p

    def render(self, pal, bg=(96, 104, 112)):
        im = Image.new("RGB", (self.w, self.h), bg)
        px = im.load()
        for y, row in enumerate(self.cells):
            for x, c in enumerate(row):
                if c:
                    px[x, y] = A.to8(pal[c])
        return im


def tiles_of(png):
    im = Image.open(png)
    px = im.load()
    tw = im.width // 8
    return lambda t, x, y: px[(t % tw) * 8 + x, (t // tw) * 8 + y] & 15 if (t // tw) * 8 + y < im.height else 0


def blit(cells, tile, t, tx, ty, row, hf=False, vf=False, opaque=False):
    for y in range(8):
        for x in range(8):
            v = tile(t, 7 - x if hf else x, 7 - y if vf else y)
            if v or opaque:
                cells[ty * 8 + y][tx * 8 + x] = (row, v) if v else None


def ink_bars(cells, x0, y0, w, rows, step, row, ink, gap=4):
    """Grey bars where text would be -- the sheets add no words."""
    for k in range(rows):
        for y in range(y0 + k * step, y0 + k * step + 7, 3):
            for yy in (y, y + 1):
                for x in range(x0, x0 + w - (k * 9) % 23):
                    if (x - x0) % 24 < 24 - gap:
                        cells[yy][x] = (row, ink)


def textbox():
    """The field's dialogue box: menu_message.png in palette 15 (stdpal_0 + T-459's purple), drawn as
    WindowFunc_DrawDialogueFrame draws it -- a 26 x 4 window at (2, 15), the paper PIXEL_FILL(1)."""
    tile = tiles_of(os.path.join(GFX, "text_window/menu_message.png"))
    row = A.jasc(os.path.join(GFX, "text_window/stdpal_0.pal"))[:16]
    row[10] = SUBTLE_PURPLE
    W, L, T = 26, 2, 1                    # the strip drawn is screen rows 14-19, so the window's top is 1 here
    cells = [[None] * 240 for _ in range(48)]
    put = lambda t, x, y, vf=False: blit(cells, tile, t, x, y, 15, vf=vf)
    for x in range(L, L + W):
        put(2, x, T - 1)
        put(2, x, T + 4, True)
        for y in range(T, T + 4):
            for yy in range(8):
                for xx in range(8):
                    cells[y * 8 + yy][x * 8 + xx] = (15, 1)
    for k, (t, dx) in enumerate(((0, -2), (1, -1), (3, W), (4, W + 1))):
        put(t, L + dx, T - 1)
        put(t, L + dx, T + 4, True)
    for t, dx in ((5, -2), (6, -1), (8, W), (9, W + 1)):
        put(t, L + dx, T)
        put(t, L + dx, T + 3, True)
    for t, dx in ((10, -2), (11, -1), (12, W), (13, W + 1)):
        put(t, L + dx, T + 1)
        put(t, L + dx, T + 2, True)
    ink_bars(cells, L * 8 + 2, T * 8 + 3, 190, 2, 16, 15, 2)
    return Surface("TEXT BOX", cells, {15: row}, accent=(15, 14), hour_slots=[(15, 12), (15, 13), (15, 15)],
                   paper=[(15, 1)], holiday=(15, 11),
                   note="palette 15: paper 1, ink 2/3 kept; the weekday on 14 (the outer corner flecks); the hour on "
                        "the frame 12, 13, 15; a holiday on 11 (the inner corner flecks)")


def startmenu(frame=1):
    """The START menu's window in user frame style `frame` (type1.png .. type10.png), as WindowFunc_DrawStandardFrame
    draws it: 7 tiles wide, 14 tall, the paper PIXEL_FILL(1), seven rows of ink."""
    tile = tiles_of(os.path.join(GFX, "text_window/type%d.png" % frame))
    row = pal5_png(os.path.join(GFX, "text_window/type%d.png" % frame), 1)
    W, H, L, T = 7, 14, 1, 1
    cells = [[None] * ((W + 2) * 8) for _ in range((H + 2) * 8)]
    put = lambda t, x, y: blit(cells, tile, t, x, y, 14)
    put(0, L - 1, T - 1), put(2, L + W, T - 1), put(6, L - 1, T + H), put(8, L + W, T + H)
    for x in range(L, L + W):
        put(1, x, T - 1), put(7, x, T + H)
    for y in range(T, T + H):
        put(3, L - 1, y), put(5, L + W, y)
        for x in range(L, L + W):
            for yy in range(8):
                for xx in range(8):
                    cells[y * 8 + yy][x * 8 + xx] = (14, 1)
    ink_bars(cells, L * 8 + 10, T * 8 + 4, 40, 7, 16, 14, 2)
    return Surface("START (frame style %d)" % frame, cells, {14: row}, accent=(14, 12),
                   hour_slots=[(14, 10), (14, 11), (14, 13), (14, 14), (14, 15)], paper=[(14, 1)], holiday=(14, 11),
                   note="palette 14: paper 1, ink 2/3 kept; thinned, the weekday on 12 (the eight inner-corner "
                        "pixels); the hour on the frame 10, 11, 13, 14, 15; a holiday on 11 (the inner bevel)")


def t318_wash(day):
    """start_menu.c DaemonsThemeMenuFrame, as built: the frame's dark, body and light from the day's trim."""
    def scale(c, top):
        m = max(c)
        return c if m == 0 else tuple(v * top // m for v in c)
    trim = TRIMS[day]
    body, dark = scale(trim, 24), scale(trim, 13)
    light = tuple(v + (31 - v) // 2 for v in body)
    return {(14, 10): dark, (14, 14): body, (14, 13): light}


def summary():
    """The SUMMARY's INFO page behind its text: BG3 moves_page.bin under BG2 page_info.bin, bg.png, bg.gbapal rows
    0-4 (PokeSum_HandleLoadBgGfx). Row 0 is BG-only (every palette-0 window is a 0x0 dummy); the text is in 6-8."""
    tile = tiles_of(os.path.join(GFX, "summary_screen/bg.png"))
    pal = pal5_png(os.path.join(GFX, "summary_screen/bg.png"))
    cells = [[None] * 240 for _ in range(160)]
    for f in ("moves_page", "page_info"):
        d = open(os.path.join(GFX, "summary_screen/%s.bin" % f), "rb").read()
        m = struct.unpack("<%dH" % (len(d) // 2), d)
        for y in range(160):
            for x in range(240):
                e = m[(y // 8) * 32 + x // 8]
                t, hf, vf, pb = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
                v = tile(t, 7 - x % 8 if hf else x % 8, 7 - y % 8 if vf else y % 8)
                if v:
                    cells[y][x] = (pb, v)
    rows = {r: pal[r * 16:(r + 1) * 16] for r in range(5)}
    return Surface("SUMMARY (INFO)", cells, rows, accent=(0, 6), hour_slots=[(0, 3), (0, 8), (0, 10), (0, 2)],
                   paper=[(2, 5), (2, 6), (3, 5), (3, 6), (4, 5), (4, 6)], holiday=(0, 14),
                   note="BG row 0: the weekday on 6 (the 1px line under the title bar); the hour on the lavender "
                        "backdrop 3, 8, 10 and the title bar 2; a holiday on 14 (the title bar's white pip); the "
                        "panes' paper (rows 2-4, 5/6) kept")


def index_page():
    """The INDEX's entry page behind its text: BG3 filled with tile 0x00C, the box (DexScreen_DrawMonDexPage, 28 x 14
    at (0, 2), tiles 4, 5, 6 and 1), kanto_dex_bgtiles.png, kanto_dex_bgpals row 0. Row 0 is also the windows' text
    palette: ink 1, 2, 3, 5, 11, 14, 15 and the type slots 12, 13 -- none of them is touched."""
    tile = tiles_of(os.path.join(GFX, "pokedex/kanto_dex_bgtiles.png"))
    row = A.jasc(os.path.join(GFX, "pokedex/kanto_dex_bgpals.pal"))[:16]
    cells = [[None] * 240 for _ in range(160)]
    for ty in range(20):
        for tx in range(30):
            blit(cells, tile, 0x00C, tx, ty, 0, opaque=True)
    W, H, L, T = 28, 14, 0, 2
    put = lambda t, x, y, hf=False, vf=False: blit(cells, tile, t, x, y, 0, hf, vf, opaque=True)
    put(4, L, T), put(4, L + 1 + W, T, hf=True), put(4, L, T + 1 + H, vf=True), put(4, L + 1 + W, T + 1 + H, True, True)
    for x in range(L + 1, L + 1 + W):
        put(5, x, T), put(5, x, T + 1 + H, vf=True)
        for y in range(T + 1, T + 1 + H):
            put(1, x, y)
    for y in range(T + 1, T + 1 + H):
        put(6, L, y), put(6, L + 1 + W, y, hf=True)
    ink_bars(cells, 96, 30, 120, 5, 16, 0, 1)
    return Surface("INDEX (entry page)", cells, {0: row}, accent=(0, 8), hour_slots=[(0, 7)], paper=[],
                   holiday=(0, 8),
                   note="BG row 0: the weekday on 8 (the box's corners); the hour on the backdrop 7; on a holiday "
                        "the corners take the month instead (the page has no other free colour); no season (the "
                        "box paper 5 is also an ink)")


def surfaces():
    return [startmenu(1), textbox(), summary(), index_page()]


# --- C, the field -----------------------------------------------------------------------------------------------------

SM = None
TOWN, CROP = "CeruleanCity", (3, 5, 22, 15)     # CERULEAN's pond, flowers and rotunda, in metatiles x0 y0 w h
WATER_GLINT = ((4, 1), (6, 1))
FLOWER_HEART = (0, 9)
PETALS = (9, 10, 11)


def field_setup():
    global SM
    if SM is None:
        SM = _load("seasonmock")
    m, l = SM.layout_of(TOWN)
    SM.PAL0 = SM.C.read_pal(os.path.join(SM.C.tdir(l["primary_tileset"], "primary"), "palettes/00.pal"))
    bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    return l, bd


def glint(trim):
    """The crest takes the trim itself: lifted toward white it falls under 22 from ROCK, NORMAL, GRASS or FIGHTING on
    six days of seven, and brightened (T-318's scale) SUNDAY's red reaches FIRE and THURSDAY's teal WATER."""
    return trim


def field_palettes(l, season, watch, day, option=None, month=None):
    """Rows 0-12 as LoadTilesetPalette leaves them: the season (T-359), the CHECKPOINT's trim (T-275), the draft's
    weekday detail (option W or F) and holiday bloom, then the watch (T-268). In 8-bit, for render()."""
    pd, sd = SM.C.tdir(l["primary_tileset"], "primary"), SM.C.tdir(l["secondary_tileset"], "secondary")
    raw = [[SM.to5(c) for c in SM.C.read_pal(os.path.join(pd, "palettes/%02d.pal" % n))] for n in range(7)] + \
          [[SM.to5(c) for c in SM.C.read_pal(os.path.join(sd, "palettes/%02d.pal" % n))] for n in range(7, 13)]
    table = SM.season_table(season)
    follow = {SM.to5(SM.PAL0[i]): table[i] for i in SM.TREES + SM.GRASS + SM.PETALS}
    rows = []
    for n, pal in enumerate(raw):
        rows.append(list(table) if n == 0 else [c if i == 0 else follow.get(c, c) for i, c in enumerate(pal)])
    rows[2][8] = TRIMS[day]
    if option == "W":
        for r, i in WATER_GLINT:
            rows[r][i] = glint(TRIMS[day])
    if month is not None:                       # the petal's own colour (11) in the month's; its light parts kept
        rows[0][PETALS[2]] = MONTHS[month - 1]
    if option == "F" and season != "winter" and month is None:
        rows[FLOWER_HEART[0]][FLOWER_HEART[1]] = TRIMS[day]
    return [[SM.to8(SM.watch(c, watch)) for c in row] for row in rows]


def field_image(l, bd, *args, **kw):
    x, y, w, h = CROP
    return SM.render(l, bd, field_palettes(l, *args, **kw)).crop((x * 16, y * 16, (x + w) * 16, (y + h) * 16))


# --- the measure ------------------------------------------------------------------------------------------------------

def added_colours():
    """Every colour B and C put on screen that the build does not. Every accent is a trim or a month colour ITSELF --
    the seven and the twelve A holds to 22 -- because every blend of them tried failed (the report's last lines)."""
    out = [("trim " + d, c) for d, c in zip(DAYS, TRIMS)]
    out += [("month %d" % (m + 1), c) for m, c in enumerate(MONTHS)]
    return out


def moved_colours():
    """The colours B MOVES -- the season's paper whisper -- as A's hour and season move a terrain's own: each held to
    'no nearer a type hue than the colour it moves, or 22 clear'."""
    out = []
    for s in surfaces():
        base = s.palette()
        for season in PAPER:
            for slot in s.paper[:1]:
                out.append(("%s paper %s" % (s.name.split()[0], season), base[slot],
                            A.lerp(base[slot], PAPER[season], PAPER_STEP)))
    return out


def tried_and_failed():
    """What the draft tried first, kept so nobody tries it again: blends of the trims and months."""
    rows = []
    for label, cs in (("trims lifted 8/16 to white (a water glint)", [A.lerp(t, (31, 31, 31), 8) for t in TRIMS]),
                      ("trims brightened to 28 (T-318's scale)", [tuple(v * 28 // max(t) for v in t) for t in TRIMS]),
                      ("month colours 9/16 to white (VIOLET BLOOM's light petal)",
                       [A.lerp(m, (31, 31, 31), 9) for m in MONTHS]),
                      ("month colours 8/16 into a frame's colour", [A.lerp(m, (16, 16, 16), 8) for m in MONTHS])):
        n = sum(A.type_distance(c)[0] < MIN for c in cs)
        rows.append((label, n, len(cs)))
    return rows


def report():
    print("T-481 B and C -- APPROVED 2026-10-29. What exists is in the docstring; the slots, measured:\n")
    for s in surfaces():
        n = s.count()
        print("  %-22s %s" % (s.name, s.note))
        for role, slots in (("weekday", [s.accent]), ("hour", s.hour_slots), ("season", s.paper),
                            ("holiday", [s.holiday])):
            slots = [x for x in slots if x]
            print("      %-8s %s" % (role, ", ".join("r%d.%d %dpx" % (r, i, n.get((r, i), 0)) for r, i in slots) or "-"))
    l, bd = field_setup()
    print("\n  FIELD (%s): the CHECKPOINT's trim r2.8, the water's crest r4.1 + r6.1 (option W), the flower's heart "
          "r0.9 (option F), petals r0.9-11 (the holiday)" % TOWN)
    bad = []
    print("\nThe colours B and C add -- the trims and the month colours themselves, CIE76 from the nearest type hue:")
    for name, c in added_colours():
        d, t = A.type_distance(c)
        if d < MIN:
            bad.append(name)
        print("  %-10s RGB%-13s %5.1f from %s%s" % (name, c, d, t, "" if d >= MIN else "   << UNDER %d" % MIN))
    print("\nThe colours B MOVES (the season's paper whisper), held to: no nearer a hue than before, or %d clear:" % MIN)
    near = []
    for name, c0, c in moved_colours():
        d0, t0 = A.type_distance(c0)
        d, t = A.type_distance(c)
        ok = d >= MIN or d >= d0
        if not ok:
            near.append(name)
        print("  %-18s RGB%-13s %5.1f (%s) -> RGB%-13s %5.1f (%s)%s" % (name, c0, d0, t0, c, d, t,
                                                                      "" if ok else "   << nearer, under %d" % MIN))
    print("  (a near-white is boxed in: cooler is ICE's, warmer NORMAL's -- the paper as drawn is 19.8-23.1 already)")
    print("\nTried and dropped (blends fail 9.4's line, so every accent is a colour A already holds):")
    for label, n, k in tried_and_failed():
        print("  %-58s %2d of %2d under %d" % (label, n, k, MIN))
    print("\nCOST: EWRAM 0, IWRAM 0, SAVE 0.")
    print("  B  (measured 2026-10-29, CONTENT, against the build before) src/daemons_calendar_pane.c 232 B of code and "
          "this table 32 B; the call sites +100 B (text box and its relight with the field, START, SUMMARY twice, the "
          "INDEX and its flip's fade colour); T-318's wash retired from start_menu.c, -303 B.")
    print("  C  fieldmap.c +76 B: the water's crest beside T-275's line in LoadTilesetPalette, and DaemonsBloomHere's "
          "month petal. No table. NET ROM about +140 B.")
    if bad:
        print("\n  !! %d added colours under %d: %s" % (len(bad), MIN, ", ".join(bad)))
        return 1
    print("\n  every added colour clears %d. (The season's paper whisper, %d of %d nearer a hue, was declined: no season "
          "in the menus.)" % (MIN, len(near), len(moved_colours())))
    print("\nTHE TABLE (--write --approved, %s): START's day and holiday on frame styles %s (1-based), the drawing "
          "they share" % (OUT_REL, ", ".join(str(k + 1) for k in start_styles())))
    for name, day, hol, mask, styles, note in table():
        print("  %-24s day %2d  holiday %2d  hour 0x%04X  styles 0x%04X" % (name, day, hol, mask, styles))
    want, path, have = engine_state()
    if have == want:
        print("  the engine matches `--write --approved` exactly (%s)" % OUT_REL)
        return 0
    print("  !! %s %s what `--write --approved` would write -- run it, or find which side is right"
          % (OUT_REL, "is missing:" if have is None else "differs from"))
    return 1


# --- the write: the panes' table (T-481 B, approved 2026-10-29) ------------------------------------------------------

OUT_REL = "src/data/calendar_panes.h"
PANES = (("CALENDAR_PANE_TEXT_BOX", textbox), ("CALENDAR_PANE_START", startmenu), ("CALENDAR_PANE_SUMMARY", summary),
         ("CALENDAR_PANE_INDEX", index_page))
FRAME_STYLES = 10


def frame_drawing(n):
    im = Image.open(os.path.join(GFX, "text_window/type%d.png" % n))
    px = im.load()
    return [px[x, y] & 15 for y in range(im.height) for x in range(im.width)]


def start_styles():
    """The frame styles (0-based, as optionsWindowFrameType counts) that are style 1's drawing pixel for pixel -- the
    ones whose index 12 is the eight inner-corner pixels and 11 the inner bevel. Measured, not listed."""
    one = frame_drawing(1)
    return [n - 1 for n in range(1, FRAME_STYLES + 1) if frame_drawing(n) == one]


def table():
    """{pane: (day slot, holiday slot, hour mask, style mask)} -- the hour mask holds the frame or backdrop slots and
    the day's and the holiday's, which take the hour as A's horizon line does; the paper and the ink are never in it."""
    out = []
    for name, make in PANES:
        s = make()
        n = s.count()
        for slot in [s.accent, s.holiday] + s.hour_slots:
            if slot and n.get(slot, 0) == 0:
                raise SystemExit("  refused: %s draws nothing in %s -- the drawing moved" % (name, slot))
        for slot in s.hour_slots + [s.accent, s.holiday]:
            if slot in s.paper:
                raise SystemExit("  refused: %s would tint its paper %s" % (name, slot))
        mask = 0
        for slot in s.hour_slots + [s.accent, s.holiday]:
            mask |= 1 << slot[1]
        if name == "CALENDAR_PANE_START":
            styles = sum(1 << k for k in start_styles())
            mask |= sum(1 << k for k in range(10, 16))     # every style's frame is 10-15 (styles 6-10 included)
        else:
            styles = 0xFFFF
        out.append((name, s.accent[1], s.holiday[1], mask, styles, s.note))
    return out


def header():
    bad = [(n, c) + A.type_distance(c) for n, c in added_colours()]
    bad = [b for b in bad if b[2] < MIN]
    if bad:
        raise SystemExit("  refused: %s" % "; ".join("%s %s is %.1f from %s" % b for b in bad))
    L = ["// Generated by DAEMONS tools/gbacalendar_ui.py --write --approved -- do not edit. T-481 B: the menus and panes",
         "// that keep the calendar (approved by the user 2026-10-29, by multiple choice). Read by",
         "// src/daemons_calendar_pane.c only. Each pane's slots, measured from its drawing: the day's trim on one",
         "// sparse slot, the month colour on one on a holiday that is not QUIET, and sWatchTint at a half on the frame",
         "// or backdrop slots (the mask) -- never the paper, never an ink. No season in the menus.",
         "",
         "struct CalendarPane",
         "{",
         "    u8 day;           // the slot that takes the day's trim (day_trims.h)",
         "    u8 holiday;       // the slot that takes the holiday's month colour (the day's, when they are one slot)",
         "    u16 hourMask;     // the slots the hour falls on, bit n for colour n",
         "    u16 styleMask;    // START: the frame styles (bit n, optionsWindowFrameType n) that have the day's slots",
         "};",
         "",
         "static const struct CalendarPane sCalendarPanes[CALENDAR_PANE_COUNT] =",
         "{"]
    for name, day, hol, mask, styles, note in table():
        L.append("    // " + note)
        L.append("    [%s] = { %d, %d, 0x%04X, 0x%04X }," % (name, day, hol, mask, styles))
    L.append("};")
    return "\n".join(L) + "\n"


def engine_state():
    want = header()
    path = os.path.join(GBA, OUT_REL)
    have = open(path).read() if os.path.exists(path) else None
    return want, path, have


def write():
    want, path, have = engine_state()
    if have == want:
        print("  %s already holds this; nothing written" % OUT_REL)
        return 0
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(want)
    os.replace(tmp, path)
    print("  wrote %s (%d lines)" % (OUT_REL, want.count("\n")))
    return 0


# --- the sheets -------------------------------------------------------------------------------------------------------

BG = (244, 244, 246)


def cell(sheet, d, im, x, y, cap, k=2):
    sheet.paste(A.scale(im, k), (x, y + 16))
    A.label(d, (x, y), cap, A.FONT)


def surface_sheet(s, out, wash_start=False):
    """Seven days, four hours, four seasons and a holiday, each at 2x, today first."""
    k = 2
    cw, ch = s.w * k, s.h * k
    pad = 14
    cols = 8
    rows_n = 5 if wash_start else 4
    sheet = Image.new("RGB", (pad + cols * (cw + pad), 70 + rows_n * (ch + 36) + 120), BG)
    d = ImageDraw.Draw(sheet)
    A.label(d, (pad, 10), "T-481 B DRAFT -- %s: today beside the draft, at 2x" % s.name, A.FONT)
    A.label(d, (pad, 30), s.note + ". Ink as grey bars: no words.")
    A.label(d, (pad, 44), "Hour: sWatchTint at a half on the frame/backdrop only. Season: the paper 3/16 toward its "
                          "tone (under 9.4's line -- a question). Holiday: one slot in the month colour itself.")
    y = 64
    wash = (lambda day: t318_wash(day)) if wash_start else (lambda day: None)
    # row 1: the week
    cell(sheet, d, s.render(s.palette(wash=wash(3) if wash_start else None)), pad, y,
         "TODAY (as built)" + (", WED" if wash_start else ""))
    for i, day in enumerate(DAYS):
        cell(sheet, d, s.render(s.palette(day=i)), pad + (i + 1) * (cw + pad), y, "%s, day" % day)
    y += ch + 36
    if wash_start:
        A.label(d, (pad, y - 14), "T-318 AS BUILT, for comparison: the whole frame in the day's colour (a wash)")
        for i, day in enumerate(DAYS):
            p = s.palette(wash=t318_wash(i))
            cell(sheet, d, s.render(p), pad + (i + 1) * (cw + pad), y, "%s, T-318" % day)
        y += ch + 36
    # row: the hours (Wednesday, summer)
    cell(sheet, d, s.render(s.palette()), pad, y, "TODAY (any hour)")
    for i, w in enumerate(WATCHES):
        cell(sheet, d, s.render(s.palette(day=3, watch=w)), pad + (i + 1) * (cw + pad), y, "WED, %s" % w.upper())
    y += ch + 36
    # row: the seasons (Wednesday, day)
    cell(sheet, d, s.render(s.palette()), pad, y, "TODAY (any season)")
    for i, se in enumerate(SEASONS):
        cell(sheet, d, s.render(s.palette(day=3, season=se)), pad + (i + 1) * (cw + pad), y, "WED, %s" % se.upper())
    for i, (se, w) in enumerate((("winter", "night"), ("autumn", "dusk"), ("spring", "dawn"))):
        cell(sheet, d, s.render(s.palette(day=3, season=se, watch=w)), pad + (i + 5) * (cw + pad), y,
             "%s %s" % (se.upper(), w.upper()))
    y += ch + 36
    # row: a holiday -- MASK NIGHT (CONTENT, 31 Oct 2026, a Saturday, autumn)
    month = HOLS.get("MASK NIGHT", (10, False))[0]
    cell(sheet, d, s.render(s.palette(day=5, season="autumn")), pad, y, "FRI 30 OCT, day")
    for i, w in enumerate(("day", "dusk", "night")):
        cell(sheet, d, s.render(s.palette(day=6, season="autumn", watch=w, month=month)),
             pad + (i + 1) * (cw + pad), y, "MASK NIGHT, %s" % w.upper())
    # the accent and the holiday slot, zoomed
    zx = pad + 4 * (cw + pad)
    p = s.palette(day=6, season="autumn", month=month)
    zoom = s.render(p)
    pos = [(x, yy) for yy, row in enumerate(s.cells) for x, c in enumerate(row) if c == s.accent]
    if pos:
        x0, y0 = pos[0]
        box = (max(0, x0 - 12), max(0, y0 - 8), min(s.w, x0 + 36), min(s.h, y0 + 16))
        z = zoom.crop(box)
        sheet.paste(z.resize((z.width * 6, z.height * 6), Image.NEAREST), (zx, y + 16))
        A.label(d, (zx, y), "the weekday's slot at 6x (SATURDAY)", A.FONT)
    y += ch + 36
    A.label(d, (pad, y), "MASK NIGHT is not QUIET, so it shows; its month colour is OCT RGB%s. The weekday stays on "
                         "its slot on a holiday. HALFTONE's grey and T-483's pulse are not drawn." % (MONTHS[month - 1],))
    sheet.save(out)
    return out


def field_hours_sheet(out):
    l, bd = field_setup()
    x, y, w, h = CROP
    cw, ch = w * 16 * 2, h * 16 * 2
    pad = 14
    sheet = Image.new("RGB", (pad + 4 * (cw + pad), 70 + 4 * (ch + 36)), BG)
    d = ImageDraw.Draw(sheet)
    A.label(d, (pad, 10), "T-481 C DRAFT -- %s, the hour x two seasons, today beside the draft (option W), at 2x"
            % "CERULEAN (CeruleanCity)", A.FONT)
    A.label(d, (pad, 30), "TODAY: T-268's hour, T-359's season and T-275's trim on the rotunda -- all built. DRAFT: "
                          "and the water's crest in the day's trim (WEDNESDAY).")
    A.label(d, (pad, 44), "Nothing else changes in the field: the hour and the season are as built.")
    yy = 64
    for se in ("summer", "winter"):
        for tag, opt in (("TODAY", None), ("DRAFT W", "W")):
            for i, wa in enumerate(WATCHES):
                cell(sheet, d, field_image(l, bd, se, wa, 3, option=opt), pad + i * (cw + pad), yy,
                     "%s -- %s, %s, WED" % (tag, se.upper(), wa.upper()))
            yy += ch + 36
    sheet.save(out)
    return out


def locate(l, bd, slots):
    """Where in the crop the given (row, index) slots are drawn: render with them in a sentinel colour."""
    pals = field_palettes(l, "summer", "day", 3)
    for r, i in slots:
        pals[r][i] = (255, 0, 255)
    x, y, w, h = CROP
    im = SM.render(l, bd, pals).crop((x * 16, y * 16, (x + w) * 16, (y + h) * 16))
    px = im.load()
    return [(xx, yy) for yy in range(im.height) for xx in range(im.width) if px[xx, yy] == (255, 0, 255)]


def field_week_sheet(out):
    l, bd = field_setup()
    x, y, w, h = CROP
    cw, ch = w * 16, h * 16
    pad, z, zw, zh = 12, 6, 48, 24
    sheet = Image.new("RGB", (pad + 7 * (cw + pad), 70 + 2 * (ch + 40 + zh * z)), BG)
    d = ImageDraw.Draw(sheet)
    A.label(d, (pad, 10), "T-481 C DRAFT -- the weekday beyond the rotunda: two options, the seven days (summer day, "
                          "1x; under each the detail at 6x)", A.FONT)
    A.label(d, (pad, 30), "W: the water's crest (General rows 4, 6 index 1) in the day's trim.  F: the flower's heart "
                          "(row 0 index 9) in the trim, not in winter.  Both keep T-275's rotunda trim.")
    yy = 56
    for opt, cap, slots in (("W", "W, THE WATER'S CREST", WATER_GLINT), ("F", "F, THE FLOWER'S HEART", [FLOWER_HEART])):
        pos = locate(l, bd, slots)
        px0, py0 = pos[len(pos) // 2] if pos else (0, 0)
        box = (max(0, px0 - zw // 2), max(0, py0 - zh // 2))
        box = box + (box[0] + zw, box[1] + zh)
        for i, day in enumerate(DAYS):
            im = field_image(l, bd, "summer", "day", i, option=opt)
            xx = pad + i * (cw + pad)
            cell(sheet, d, im, xx, yy, "%s -- %s" % ("%s (%d px here)" % (cap, len(pos)) if i == 0 else opt, day), k=1)
            zz = im.crop(box)
            sheet.paste(zz.resize((zw * z, zh * z), Image.NEAREST), (xx, yy + 16 + ch + 4))
        yy += ch + 40 + zh * z
    sheet.save(out)
    return out


def field_holiday_sheet(out):
    l, bd = field_setup()
    x, y, w, h = CROP
    cw, ch = w * 16 * 2, h * 16 * 2
    pad = 14
    month = HOLS.get("MASK NIGHT", (10, False))[0]
    sheet = Image.new("RGB", (pad + 3 * (cw + pad), 70 + 2 * (ch + 36)), BG)
    d = ImageDraw.Draw(sheet)
    A.label(d, (pad, 10), "T-481 C DRAFT -- a holiday's one touch in the field: MASK NIGHT (CONTENT, autumn, a "
                          "Saturday), at 2x", A.FONT)
    A.label(d, (pad, 30), "Above: the day before, as built. Below: the petal's own colour (index 11) in OCT's, its light "
                          "parts kept -- VIOLET BLOOM's idea with the holiday's own month. Not on a QUIET holiday.")
    for r, (hol, day, tag) in enumerate(((None, 5, "FRI 30 OCT (ordinary)"), (month, 6, "MASK NIGHT, SAT 31 OCT"))):
        for c, wa in enumerate(("day", "dusk", "night")):
            cell(sheet, d, field_image(l, bd, "autumn", wa, day, month=hol), pad + c * (cw + pad),
                 64 + r * (ch + 36), "%s, %s" % (tag, wa.upper()))
    sheet.save(out)
    return out


def sheets(outdir):
    os.makedirs(outdir, exist_ok=True)
    s = surfaces()
    made = [surface_sheet(s[0], os.path.join(outdir, "t481b_start.png"), wash_start=True),
            surface_sheet(s[1], os.path.join(outdir, "t481b_textbox.png")),
            surface_sheet(s[2], os.path.join(outdir, "t481b_summary.png")),
            surface_sheet(s[3], os.path.join(outdir, "t481b_index.png")),
            field_hours_sheet(os.path.join(outdir, "t481c_hours.png")),
            field_week_sheet(os.path.join(outdir, "t481c_week.png")),
            field_holiday_sheet(os.path.join(outdir, "t481c_holiday.png"))]
    for m in made:
        print(m)


def main():
    if "--sheet" in sys.argv:
        sheets(sys.argv[sys.argv.index("--sheet") + 1])
        return 0
    if "--write" in sys.argv:
        if "--approved" not in sys.argv:
            print("  --write refused without --approved: the look is the one the user answered on 2026-10-29 "
                  "(T-481 B and C); --write --approved writes it.")
            return 1
        return write()
    return report()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""HOLIDAYS on the real calendar, and a colour and a note for each month (T-416; decided by the user 2026-10-17/18).

    python3 tools/genholidays.py               # report: every check, and what --write would change
    python3 tools/genholidays.py --write       # write the engine's files (below)
    python3 tools/genholidays.py --companion   # print companion/server/data/holidays.json as the game's table makes it

docs/holidays.json is the single source: each holiday's real name (the companion's) and in-world name (the game's,
DRAFT), edition, date rule, length, quiet, banner, overlays, sky, daemons, routines' look, gift and THE YEAR's line;
the twelve months' notes and colours. The approved table it was made from is docs/private/draft-holidays-2026-10-17.md.

--write writes (all generated; the hand-written engine code that reads them is the build plan's,
docs/private/plan-holidays-build-2026-10-18.md):
    engineGba/src/data/daemons_holidays.h     the const ROM table for src/daemons_holidays.c: 24 rows per edition
                                              (#if'd), the gifts, the presents, the daemons' slots, the skies, the
                                              Easter and Mid-Autumn tables 2024-2040, the month colours and notes,
                                              the lead's GAIN by type, the givers' lines and THE YEAR's lines
    engineGba/src/data/holiday_lines.h        THE YEAR's NOTEBOOK entries (NB_YEAR_ENTRIES), for src/notebook.c
    engineGba/include/constants/holidays.h    HOLIDAY_* ids (COMMON 1-12, the edition's 13-24), HF_*, GIVER_*, ...
    engineGba/include/constants/flags.h       a BEGIN/END genholidays block: 24 gift flags, 12 line flags and
                                              MARIGOLD DAYS' visitor's hide flag (0x300-0x324)
    engineGba/include/constants/vars.h        VAR_HOLIDAY_YEAR in place of an unreferenced VAR_0x40xx

THE RULES THIS KEEPS, and fails on (exit 1, so check_generators fails with it):
  - three a month: one COMMON, one CONTENT, one CONTEXT; every rule resolves for 2024-2040
  - a banner ("Bb · LANTERN NIGHTS", or on the 1st "Db · WEDNESDAY · NIGHT") fits the day banner's 152px and its
    28-byte buffer; a giver's line fits the 208px box with the widest name in STR_VAR_1; THE YEAR's quoted lines
    wrap to at most three lines of 208px
  - every month colour is 22+ (CIE76) from every type's hue (9.4); months 12+ apart is reported, not failed
  - every daemon resolves, is ready (tools/gbashifts.py's own readiness check), is met in the wild somewhere already
    (never a gate), and its map has that area and slot in both editions
  - every item, routine, map and mapsec resolves; every gift line names a line of THE YEAR
  - the chosen flags and VAR are free (read from the constants headers, read-only) or already this tool's
"""
import datetime, importlib.util, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SRC = os.path.join(ROOT, "docs", "holidays.json")
OUT_TABLE = os.path.join(GBA, "src", "data", "daemons_holidays.h")
OUT_LINES = os.path.join(GBA, "src", "data", "holiday_lines.h")
OUT_CONST = os.path.join(GBA, "include", "constants", "holidays.h")
FLAGS_H = os.path.join(GBA, "include", "constants", "flags.h")
VARS_H = os.path.join(GBA, "include", "constants", "vars.h")
COMPANION = os.path.join(ROOT, "companion", "server", "data", "holidays.json")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genguide import width, lab, type_hues  # noqa: E402  (the game's font and 9.4's colour check)


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SHIFTS = _load("gbashifts")     # the season/hour slots per road, and the readiness check

FIRST_YEAR, LAST_YEAR = 2024, 2040
YEARS = range(FIRST_YEAR, LAST_YEAR + 1)
BANNER_W, BANNER_BUF = 152, 28   # src/map_name_popup.c: the day banner's width and sDayBanner[28]
BOX_W = 208
TYPE_MARGIN, MONTH_MARGIN = 22, 12

#  The flags and the VAR (engine.md 1: 947 of our 1024 flags free; vanilla's spare VAR_0x40xx). 0x272-0x2FF is left
#  for PLAY (T-417, still building); 0x300 up is ours. VAR_0x40BF is the next spare in line, so PLAY's session is the
#  likeliest to claim it -- this takes the one after.
FLAG_GIFT_BASE = 0x300          # + 0..11 COMMON by month, + 12..23 the edition's by month
FLAG_LINE_BASE = 0x318          # + 0..10 THE YEAR's lines
VAR_NUM = 0x40C0
VAR_NAME = "VAR_HOLIDAY_YEAR"

WATCHES = ["DAY", "DUSK", "NIGHT", "DAWN"]               # include/daemons_time.h WATCH_*; play time's order too
SKIES = ["CLEAR", "RAIN", "STORM", "SNOW", "FOG", "WIND"]  # include/daemons_weather.h DAEMONS_SKY_*
WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
DAY_NAMES = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
NORTH_STARTS = {"winter": (12, 21), "spring": (3, 21), "summer": (6, 21), "autumn": (9, 22)}   # tools/seasons.py
SEASON_ORDER = ["winter", "spring", "summer", "autumn"]
EDITIONS = (("CONTENT", "FIRERED"), ("CONTEXT", "LEAFGREEN"))
OVERLAYS = ["fireworks", "lantern", "frost", "snow_light", "long_day", "long_night", "bright_day", "fir_glow",
            "violet_bloom"]
GIVERS = ["CHECKPOINT", "MOM", "BEACH", "HALFTONE", "TOWER", "DAWN_OUTDOORS"]
NATURALS = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}   # SE_NOTE_C + n (field_specials.c)
LAND_SLOTS, FISH_SLOTS = 12, 10
WRITE = "--write" in sys.argv


def read(path):
    return open(path, encoding="utf-8").read()


def gba(rel):
    return read(os.path.join(GBA, rel))


# ---- dates ------------------------------------------------------------------------------------------------------

def easter(y):
    """Easter Sunday by the Gregorian computus (the anonymous algorithm, as companion/server/src/holidays.ts)."""
    a, b, c = y % 19, y // 100, y % 100
    d, e, f = b // 4, b % 4, (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    return datetime.date(y, (h + l - 7 * m + 114) // 31, (h + l - 7 * m + 114) % 31 + 1)


def season_start(season, edition):
    """The day the edition's own season starts: the southern year is the northern one two seasons on."""
    if edition == "CONTEXT":
        season = SEASON_ORDER[(SEASON_ORDER.index(season) + 2) % 4]
    return NORTH_STARTS[season]


def start(rule, y, edition):
    k = rule["kind"]
    if k == "fixed":
        return datetime.date(y, rule["month"], rule["day"])
    if k == "nth_weekday":
        first = datetime.date(y, rule["month"], 1)
        wd = (first.weekday() + 1) % 7          # Python's Monday 0 -> Sunday 0
        return first + datetime.timedelta(days=(rule["weekday"] - wd) % 7 + 7 * (rule["n"] - 1))
    if k == "easter":
        return easter(y) + datetime.timedelta(days=rule["offset"])
    if k == "table":
        md = rule["dates"].get(str(y))
        return datetime.date(y, int(md[:2]), int(md[3:])) if md else None
    if k == "season_start":
        m, d = season_start(rule["season"], edition)
        return datetime.date(y, m, d)
    raise ValueError(k)


def days_on(rows, y, edition):
    """{date: [holidays on it]} for year y, with steps_off kept: a holiday is not on a day the one it steps off holds."""
    on = {}
    for h in rows:
        s = start(h["rule"], y, edition)
        for i in range(h["days"]):
            on.setdefault(s + datetime.timedelta(days=i), []).append(h)
    for day, hs in on.items():
        ids = {h["id"] for h in hs}
        on[day] = [h for h in hs if h.get("steps_off") not in ids]
    return on


def editions_of(h):
    return [e for e, _ in EDITIONS] if h["edition"] == "COMMON" else [h["edition"]]


def mean_date(h, edition):
    """A moving holiday's anchor where there is no clock: its mean day of the year, 2024-2040."""
    days = [start(h["rule"], y, edition).timetuple().tm_yday for y in YEARS if y % 4]   # common years only
    doy = round(sum(days) / len(days))
    return datetime.date(2026, 1, 1) + datetime.timedelta(days=doy - 1)


def play_watches(doc, edition):
    """{id: (watch, anchor date, moved by)} for a ROM's 24: COMMON placed first, and an edition's holiday that would
    share a watch with one already placed moves on to the next free watch of its kind -- so with no clock every
    holiday is seen on its own (with a clock, two on one day follow the user's rule: the edition's shows)."""
    taken, out = set(), {}
    for h in edition_rows(doc, edition):
        w, d = play_watch(h, edition, doc["play_time"])
        step = 4 if h.get("play_watch") else 1
        w0 = w
        while w in taken:
            w = (w + step) % 112
        taken.add(w)
        out[h["id"]] = (w, d, w - w0)
    return out


def play_watch(h, edition, play):
    """The watch of the 28-hour play-time year (0-111) a holiday holds when there is no clock, before clashes."""
    year_watches = play["year_minutes"] // play["watch_minutes"]
    origin = datetime.date(2026, play["starts"]["month"], play["starts"]["day"])
    d = mean_date(h, edition) if h["rule"]["kind"] != "fixed" else datetime.date(2026, h["rule"]["month"], h["rule"]["day"])
    offset = (d - origin).days % 365
    w = offset * year_watches // 365
    want = h.get("play_watch")
    if want:
        kind = WATCHES.index(want)
        w = min((x for x in range(w - 3, w + 4) if x % 4 == kind), key=lambda x: (abs(x - w), x))
    return w % year_watches, d


def midautumn_check(dates):
    """The published Mid-Autumn dates against the mean lunation: each must be 14 days (+-1) after a new moon, in
    China's time. A sanity check on the typing, not a calendar -- the month it falls in is the table's."""
    errs = []
    ref = datetime.datetime(2000, 1, 6, 18, 14) + datetime.timedelta(hours=8)   # a new moon, UTC+8
    syn = 29.530588853
    for y, md in dates.items():
        d = datetime.datetime(int(y), int(md[:2]), int(md[3:]), 12)
        nm = d - datetime.timedelta(days=14)
        k = round((nm - ref).total_seconds() / 86400 / syn)
        mean = ref + datetime.timedelta(days=k * syn)
        if abs((nm - mean).total_seconds()) / 86400 > 1.6:
            errs.append("Mid-Autumn %s-%s is %.1f days off a full moon" % (y, md, (nm - mean).total_seconds() / 86400))
    return errs


# ---- what the engine names ----------------------------------------------------------------------------------------

def name_tables():
    species = {}
    for sp, n in re.findall(r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]*)"\)', gba("src/data/text/species_names.h")):
        species.setdefault(n, []).append(sp)
    items, gains = {}, {}
    for it in json.loads(gba("src/data/items.json"))["items"]:
        items.setdefault(it["english"], it["itemId"])
        if it["holdEffect"].endswith("_POWER") and it["english"].endswith(" GAIN"):   # not the incenses
            gains[it["holdEffect"]] = it["itemId"]
    moves = {n: m for m, n in re.findall(r'\[(MOVE_\w+)\]\s*=\s*_\("([^"]*)"\)', gba("src/data/text/move_names.h"))}
    hold_to_type = dict(re.findall(r'\{(HOLD_EFFECT_\w+_POWER),\s*(TYPE_\w+)\}', gba("src/pokemon.c")))
    types = re.findall(r'#define (TYPE_\w+)\s+(\d+)', gba("include/constants/pokemon.h"))
    types = [t for t, n in sorted(((t, int(n)) for t, n in types if t != "TYPE_NONE"), key=lambda x: x[1])]
    type_gain = {}
    for he, item in gains.items():
        if he in hold_to_type:
            type_gain[hold_to_type[he]] = item
    maps = set(re.findall(r'#define (MAP_\w+)\s', gba("include/constants/map_groups.h")))
    mapsecs = set(re.findall(r'^\s*(MAPSEC_\w+)', gba("include/constants/region_map_sections.h"), re.M))
    return species, items, moves, types, type_gain, maps, mapsecs


def wild_tables():
    wild = json.loads(gba("src/data/wild_encounters.json"))["wild_encounter_groups"][0]["encounters"]
    met = set()
    for e in wild:
        for k, v in e.items():
            if k.endswith("_mons"):
                met.update(m["species"] for m in v["mons"])
    return wild, met


# ---- the checks ---------------------------------------------------------------------------------------------------

def c_quote(s):
    return s.replace('"', '\\"')


def wrap(text, w=BOX_W):
    lines, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if width(cand) <= w or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def box(paragraphs):
    """Paragraphs -> one message: \\n then \\l within a paragraph, \\p between (as tools/gbawisdom.py)."""
    out = []
    for para in paragraphs:
        ls = wrap(para)
        out.append(ls[0] + "".join(("\\n" if i == 1 else "\\l") + l for i, l in enumerate(ls[1:], 1)))
    return "\\p".join(out)


def check(doc, names, wild, met, errors, notes):
    species, items, moves, types, type_gain, maps, mapsecs = names
    hols, months = doc["holidays"], doc["months"]

    # three a month
    for m in range(1, 13):
        eds = sorted(h["edition"] for h in hols if h["month"] == m)
        if eds != ["COMMON", "CONTENT", "CONTEXT"]:
            errors.append("month %d holds %s, not one COMMON, one CONTENT, one CONTEXT" % (m, eds))
    ids = [h["id"] for h in hols]
    if len(set(ids)) != len(ids):
        errors.append("holiday ids repeat")

    # every rule resolves, every year; the month a rule lands in is the row's
    for h in hols:
        for ed in editions_of(h):
            for y in YEARS:
                s = start(h["rule"], y, ed)
                if s is None:
                    errors.append("%s names no day in %d" % (h["id"], y))
                elif h["rule"]["kind"] in ("fixed", "nth_weekday", "season_start") and s.month != h["month"]:
                    errors.append("%s starts in month %d, its row says %d" % (h["id"], s.month, h["month"]))
    errors += midautumn_check(next(h for h in hols if h["rule"]["kind"] == "table")["rule"]["dates"])

    # the banner
    widest_name = max(hols, key=lambda h: width(h["name"]))["name"]
    for h in hols:
        note = months[h["month"] - 1]["note"]
        text = "%s · %s" % (note, h["name"])
        if width(text) > BANNER_W:
            errors.append("banner %r is %dpx (%d)" % (text, width(text), BANNER_W))
        if len(note) + 3 + len(h["name"]) + 1 > BANNER_BUF:
            errors.append("banner %r overflows sDayBanner[%d]" % (text, BANNER_BUF))
        if not re.fullmatch(r"[A-Z' ]+", h["name"]):
            errors.append("%s's name %r: capitals, spaces and ' only" % (h["id"], h["name"]))
    first = max(("%s · %s · %s" % (m["note"], d, w) for m in months for d in DAY_NAMES for w in WATCHES), key=width)
    if width(first) > BANNER_W:
        errors.append("the 1st's banner %r is %dpx (%d)" % (first, width(first), BANNER_W))
    notes.append("banners: widest holiday %r %dpx, widest 1st-of-month %r %dpx, of %dpx"
                 % ("%s · %s" % ("Bb", widest_name), width("Bb · " + widest_name), first, width(first), BANNER_W))

    # the givers' lines, with the widest name in STR_VAR_1
    for g, v in doc["givers"].items():
        if g not in GIVERS:
            errors.append("giver %s is not one of %s" % (g, GIVERS))
        if v.get("say"):
            lines = v["say"].replace("{STR_VAR_1}", widest_name).split("\n")
            if len(lines) > 2 or any(width(l) > BOX_W for l in lines):
                errors.append("%s's line %r: %s px in %d lines" % (g, v["say"], [width(l) for l in lines], len(lines)))

    # THE YEAR
    line_ids = [l["id"] for l in doc["lines"]]
    for l in doc["lines"]:
        quoted = wrap("“%s”" % l["text"])
        if len(quoted) > l.get("max_lines", 3) or any(width(x) > BOX_W for x in quoted):
            errors.append("THE YEAR's %s wraps to %d lines (%s px)" % (l["id"], len(quoted), [width(x) for x in quoted]))
    used_lines = set()

    # month colours (9.4)
    hues = type_hues()
    rgb8 = [tuple(v << 3 for v in m["rgb5"]) for m in months]

    def dist(a, b):
        return sum((x - y) ** 2 for x, y in zip(lab(a), lab(b))) ** .5
    for i, (m, c) in enumerate(zip(months, rgb8)):
        d, t = min((dist(c, v), k) for k, v in hues.items())
        mm, j = min((dist(c, o), months[k]["month"]) for k, o in enumerate(rgb8) if k != i)
        if d < TYPE_MARGIN:
            errors.append("%s's colour %s is %.1f from %s (9.4 wants %d+)" % (m["month"], m["rgb5"], d, t, TYPE_MARGIN))
        flag = "" if mm >= MONTH_MARGIN else "   << under %d from %s" % (MONTH_MARGIN, j)
        notes.append("  %s %-2s rgb%-13s %4.1f from %-8s %4.1f from %s%s"
                     % (m["month"], m["note"], tuple(m["rgb5"]), d, t, mm, j, flag))
        if m["pc"] != i or m["key_colour_index"] != i + 1:
            errors.append("%s: pc and key colour must be its place in the scale" % m["month"])

    # daemons
    shift_slots = {mp: (ss, hs) for mp, (ss, _), _, (hs, _), _ in SHIFTS.TABLES}
    need_ready = set()
    for h in hols:
        for dm in h["daemons"]:
            for ed_i, (ed, label) in enumerate(EDITIONS):
                if ed not in editions_of(h):
                    continue
                nm = dm.get("species") or dm["name"]
                nm = nm.split("|")[ed_i] if "|" in nm else nm
                sp = species.get(nm, [])
                if len(sp) != 1:
                    errors.append("%s: daemon %r names %s" % (h["id"], nm, sp))
                    continue
                sp = sp[0]
                need_ready.add(sp)
                shifted = any(nm in c.rstrip("*").split("|") for row in SHIFTS.TABLES for c in row[2] + row[4])
                if sp not in met and not shifted:
                    errors.append("%s: %s (%s) is met nowhere in the wild -- a holiday may not be its only home"
                                  % (h["id"], nm, sp))
                for mp in dm["maps"]:
                    if mp not in maps:
                        errors.append("%s: no map %s" % (h["id"], mp))
                        continue
                    area = "land_mons" if dm["area"] == "land" else "fishing_mons"
                    here = [e for e in wild if e["map"] == mp and e["base_label"].endswith(
                        "_FireRed" if ed == "CONTENT" else "_LeafGreen")]
                    if not here or area not in here[0]:
                        errors.append("%s: %s has no %s in %s" % (h["id"], mp, area, ed))
                    slot = dm["slot"]
                    if slot in ("season", "hour"):
                        if mp not in shift_slots:
                            errors.append("%s: %s has no %s slot in gbashifts' TABLES -- name a number" % (h["id"], mp, slot))
                    elif not 0 <= slot < (LAND_SLOTS if dm["area"] == "land" else FISH_SLOTS):
                        errors.append("%s: slot %s out of range" % (h["id"], slot))
            for w in dm["watches"]:
                if w not in WATCHES:
                    errors.append("%s: watch %s" % (h["id"], w))
    ready = SHIFTS.readiness(need_ready)
    for sp, why in sorted(ready.items()):
        if why:
            errors.append("%s is not ready: %s" % (sp, "; ".join(why)))

    # gifts, routines, sky
    for h in hols:
        if h["giver"] not in GIVERS:
            errors.append("%s: giver %s" % (h["id"], h["giver"]))
        for g in h["gift"]:
            give = g["give"]
            for it in ([give] if isinstance(give, str) else give.get("year_draw", [])):
                if it not in items:
                    errors.append("%s: no item %r" % (h["id"], it))
            if isinstance(give, dict) and "line" in give:
                if give["line"] not in line_ids:
                    errors.append("%s: no line %s" % (h["id"], give["line"]))
                used_lines.add(give["line"])
            w = g.get("when", {})
            for k in w:
                if k not in ("watches", "sky", "weekdays", "storm_on_islands_today"):
                    errors.append("%s: gift condition %s" % (h["id"], k))
            if not set(w.get("watches", [])) <= set(WATCHES) or not set(w.get("sky", [])) <= set(SKIES) \
                    or not set(w.get("weekdays", [])) <= set(WEEKDAYS):
                errors.append("%s: a gift condition names an unknown watch, sky or weekday" % h["id"])
        if h.get("quiet") and any(isinstance(g["give"], str) or "year_draw" in g["give"] for g in h["gift"]):
            errors.append("%s is QUIET and gives an item" % h["id"])
        for r in h.get("routines", []):
            if r["routine"] not in moves:
                errors.append("%s: no routine %r" % (h["id"], r["routine"]))
        for o in h.get("overlay", []):
            if o not in OVERLAYS:
                errors.append("%s: overlay %s" % (h["id"], o))
        if h.get("steps_off"):
            other = next((x for x in hols if x["id"] == h["steps_off"]), None)
            if not other or other["edition"] != "COMMON" or h["edition"] == "COMMON":
                errors.append("%s steps off %s: only an edition's holiday steps off a COMMON one" % (h["id"], h["steps_off"]))
            elif other["days"] != 1 or other.get("eve_from_hour"):
                errors.append("%s steps off %s, which is not one plain day" % (h["id"], h["steps_off"]))
            else:
                for y in YEARS:
                    s, o = start(h["rule"], y, h["edition"]), start(other["rule"], y, h["edition"])
                    if o == s + datetime.timedelta(days=h["days"] - 1):
                        errors.append("%s's last day is %s's in %d: stepping off leaves it outside its span" % (h["id"], other["id"], y))
        if h.get("sky") and h["sky"]["mapsec"] not in mapsecs:
            errors.append("%s: no %s" % (h["id"], h["sky"]["mapsec"]))
    for l in line_ids:
        if l not in used_lines:
            errors.append("THE YEAR's %s is given by no holiday" % l)
    missing = [t for t in types if t not in type_gain]
    if missing:
        den = next(h for h in hols if h["id"] == "DEN_DAY")["gift"]
        if not any(isinstance(g["give"], dict) and "line" in g["give"] for g in den[1:]):
            errors.append("DEN DAY: no GAIN item for %s and no line after it (the user, 2026-10-18: a line)" % ", ".join(missing))
        notes.append("DEN DAY: no GAIN item for %s -- that lead brings THE YEAR's line instead" % ", ".join(missing))


# ---- the flags and the VAR ----------------------------------------------------------------------------------------

def gift_flag_names(doc):
    mon = [m["month"] for m in doc["months"]]
    common = ["FLAG_HOLIDAY_GIFT_COMMON_%s" % mon[i] for i in range(12)]
    edition = ["FLAG_HOLIDAY_GIFT_EDITION_%s" % mon[i] for i in range(12)]
    return common, edition


def flags_block(doc):
    common, edition = gift_flag_names(doc)
    lines = ["//  BEGIN genholidays -- T-416 (the user, 2026-10-17): HOLIDAYS. An ITEM gift once per holiday per year: one",
             "//  flag per holiday, cleared when VAR_HOLIDAY_YEAR no longer holds this year (src/daemons_holidays.c). COMMON",
             "//  by month, then the edition's own by month -- a save is one edition, so CONTENT's and CONTEXT's share them.",
             "//  THE YEAR's lines, once ever, one flag each. Written by DAEMONS tools/genholidays.py from docs/holidays.json."]
    for i, n in enumerate(common + edition):
        lines.append("#define %-36s (DAEMONS_FLAGS_START + 0x%03X)" % (n, FLAG_GIFT_BASE + i))
    for i, l in enumerate(doc["lines"]):
        lines.append("#define %-36s (DAEMONS_FLAGS_START + 0x%03X)" % ("FLAG_YEAR_LINE_" + l["id"], FLAG_LINE_BASE + i))
    lines.append("//  MARIGOLD DAYS' visitor at the stones in DAEMON TOWER: hidden but on those days (set and cleared on the floor's transition).")
    lines.append("#define %-36s (DAEMONS_FLAGS_START + 0x%03X)" % ("FLAG_HIDE_HOLIDAY_VISITOR", FLAG_LINE_BASE + len(doc["lines"])))
    lines.append("#define %-36s %d   // from FLAG_HOLIDAY_GIFT_COMMON_JAN" % ("HOLIDAY_GIFT_FLAG_COUNT", 24))
    lines.append("//  END genholidays")
    return "\n".join(lines) + "\n"


def flags_after(doc, errors):
    """flags.h with the block in place (before DAEMONS_FLAGS_COUNT), or None if it cannot be placed."""
    t = read(FLAGS_H)
    block = flags_block(doc)
    m = re.search(r"//  BEGIN genholidays.*?//  END genholidays\n", t, re.S)
    if m:
        theirs = t[:m.start()] + t[m.end():]
    else:
        theirs = t
    used = {int(x, 16) for x in re.findall(r"\(DAEMONS_FLAGS_START \+ 0x([0-9A-Fa-f]+)\)", theirs)}
    for n in range(FLAG_GIFT_BASE, FLAG_LINE_BASE + len(doc["lines"]) + 1):
        if n in used:
            errors.append("flag DAEMONS_FLAGS_START + 0x%03X is already someone else's" % n)
    for lo, hi in re.findall(r"\+ 0x([0-9A-Fa-f]+)\)\s*//\s*\.\. \+ 0x([0-9A-Fa-f]+)", theirs):   # ranges in comments
        if int(lo, 16) <= FLAG_LINE_BASE + len(doc["lines"]) and FLAG_GIFT_BASE <= int(hi, 16):
            errors.append("flags 0x%s..0x%s (a range in flags.h) overlap ours" % (lo, hi))
    count = int(re.search(r"#define DAEMONS_FLAGS_COUNT\s+(0x[0-9A-Fa-f]+)", t).group(1), 16)
    if FLAG_LINE_BASE + len(doc["lines"]) + 1 > count:
        errors.append("our flags run past DAEMONS_FLAGS_COUNT")
    if m:
        return t[:m.start()] + block + t[m.end():]
    anchor = re.search(r"\n#define DAEMONS_FLAGS_COUNT", t)
    return t[:anchor.start()] + "\n" + block + t[anchor.start():]


def vars_after(errors):
    t = read(VARS_H)
    ours = "#define %-26s 0x%04X // T-416: the year the holiday gifts were last given in (real year - 2000; play-time years have bit 15)" % (VAR_NAME, VAR_NUM)
    if re.search(r"^#define %s\s" % VAR_NAME, t, re.M):
        return re.sub(r"^#define %s\s.*$" % VAR_NAME, ours, t, flags=re.M)
    placeholder = "VAR_0x%04X" % VAR_NUM
    m = re.search(r"^#define %s\s+0x%04X\s*$" % (placeholder, VAR_NUM), t, re.M)
    if not m:
        errors.append("%s is not the spare placeholder any more -- pick another" % placeholder)
        return t
    hits = subprocess.run(["git", "-C", GBA, "grep", "-lw", placeholder, "--", "src", "data", "include", "asm"],
                          capture_output=True, text=True).stdout.split()
    if [x for x in hits if not x.endswith("constants/vars.h")]:
        errors.append("%s is referenced in %s" % (placeholder, hits))
    return t[:m.start()] + ours + t[m.end():]


# ---- the generated files ------------------------------------------------------------------------------------------

def edition_rows(doc, ed):
    """The 24 rows a ROM carries, in id order: COMMON by month (1-12), then the edition's by month (13-24)."""
    hols = doc["holidays"]
    common = sorted((h for h in hols if h["edition"] == "COMMON"), key=lambda h: h["month"])
    own = sorted((h for h in hols if h["edition"] == ed), key=lambda h: h["month"])
    return common + own


def const_id(h):
    return "HOLIDAY_" + h["id"]


def const_header(doc):
    o = ["// Generated by DAEMONS tools/genholidays.py from docs/holidays.json -- edit the json, not this file.",
         "// T-416 HOLIDAYS (the user, 2026-10-17/18). Shared by C and the event scripts.",
         "#ifndef GUARD_CONSTANTS_HOLIDAYS_H", "#define GUARD_CONSTANTS_HOLIDAYS_H", "",
         "#define HOLIDAY_NONE  0", "#define HOLIDAY_COUNT 24   // a ROM's: the twelve COMMON (1-12) and its edition's twelve (13-24)", ""]
    for i, h in enumerate(edition_rows(doc, "CONTENT")[:12]):
        o.append("#define %-28s %2d   // %s, %s" % (const_id(h), i + 1, h["name"], h["real"]))
    for k, (ed, define) in enumerate(EDITIONS):
        o.append("#%s defined(%s)   // %s" % ("if" if k == 0 else "elif", define, ed))
        for i, h in enumerate(edition_rows(doc, ed)[12:]):
            o.append("#define %-28s %2d   // %s, %s" % (const_id(h), i + 13, h["name"], h["real"]))
    o += ["#endif", ""]
    o += ["#define HOLIDAY_RULE_FIXED        0", "#define HOLIDAY_RULE_NTH_WEEKDAY  1", "#define HOLIDAY_RULE_EASTER       2",
          "#define HOLIDAY_RULE_MIDAUTUMN    3", ""]
    o.append("// HF_*: what a holiday changes besides the banner (src/daemons_holidays.c reads them; the build plan says where)")
    for i, f in enumerate(["QUIET", "EVE_FROM_DUSK", "OTHER_EDITION", "STEPS_OFF"] + [x.upper() for x in OVERLAYS]):
        o.append("#define HF_%-16s (1 << %d)" % (f, i))
    o.append("")
    for i, g in enumerate(GIVERS):
        o.append("#define GIVER_%-16s %d" % (g, i))
    o += ["", "#define HOLIDAY_AREA_LAND  0", "#define HOLIDAY_AREA_FISH  1", "",
          "#define HOLIDAY_FIRST_YEAR %d   // the Easter and Mid-Autumn tables; outside them a moving holiday keeps its mean date" % FIRST_YEAR,
          "#define HOLIDAY_LAST_YEAR  %d" % LAST_YEAR,
          "#define HOLIDAY_PLAY_YEAR_WATCHES %d   // the play-time year: 28 hours of play, 15 minutes a watch"
          % (doc["play_time"]["year_minutes"] // doc["play_time"]["watch_minutes"]),
          "#define HOLIDAY_YEAR_LINE_COUNT %d" % len(doc["lines"]), "", "#endif // GUARD_CONSTANTS_HOLIDAYS_H", ""]
    return "\n".join(o)


def mask(names, order):
    return sum(1 << order.index(n) for n in names)


def item_c(items, name):
    return items[name]


def table_header(doc, names):
    species, items, moves, types, type_gain, maps, mapsecs = names
    months, play = doc["months"], doc["play_time"]
    shift_slots = {mp: (ss, hs) for mp, (ss, _), _, (hs, _), _ in SHIFTS.TABLES}
    line_index = {l["id"]: i for i, l in enumerate(doc["lines"])}
    o = ["// Generated by DAEMONS tools/genholidays.py from docs/holidays.json -- edit the json, not this file.",
         "// T-416 HOLIDAYS (the user, 2026-10-17/18). Included once, by src/daemons_holidays.c. EVERY WORD DRAFT.",
         "// The real names live only in the companion; here a holiday is its in-world name.", "",
         "struct HolidayRow", "{",
         "    const u8 *name;",
         "    u16 flags;        // HF_*",
         "    u8 rule;          // HOLIDAY_RULE_*",
         "    u8 month;         // 1-12: the month whose note and colour it wears",
         "    s8 arg;           // FIXED: the day; NTH_WEEKDAY: n; EASTER: days from Easter Sunday; MIDAUTUMN: 0",
         "    u8 weekday;       // NTH_WEEKDAY: 0 Sunday",
         "    u8 days;          // how long, from the clock",
         "    u8 anchorMonth;   // outside the tables' years: the mean date a moving holiday keeps",
         "    u8 anchorDay;",
         "    u8 playWatch;     // 0-111: the one watch of the play-time year it holds when there is no clock",
         "    u8 bannerWatches; // bit per WATCH_*: when the banner names it",
         "    u8 giver;         // GIVER_*",
         "    u8 giftFirst;     // into sHolidayGifts",
         "    u8 giftCount;",
         "};", "",
         "#define HG_GO_ON           (1 << 0)   // gives and reads on",
         "#define HG_LINE            (1 << 1)   // a line for THE YEAR (arg: its index), not an item",
         "#define HG_LEAD_TYPE_GAIN  (1 << 2)   // the lead's first type's GAIN (sHolidayTypeGain); ORACLE as either type reads on",
         "#define HG_YEAR_DRAW       (1 << 3)   // sHolidayPresents[(year + edition) % 4]",
         "#define HG_STORM_ISLANDS   (1 << 4)   // only if a thunderstorm touched the islands today", "",
         "struct HolidayGift", "{",
         "    u16 item;",
         "    u8 count;",
         "    u8 watches;       // bit per WATCH_*; 0 = any",
         "    u8 skies;         // bit per DAEMONS_SKY_*; 0 = any",
         "    u8 weekdays;      // bit per weekday, Sunday 0; 0 = any",
         "    u8 flags;         // HG_*",
         "    u8 arg;",
         "};", "",
         "struct HolidayShift", "{",
         "    u16 species;",
         "    u8 holiday;",
         "    u8 mapGroup;",
         "    u8 mapNum;",
         "    u8 area;          // HOLIDAY_AREA_*",
         "    u8 slot;",
         "    u8 watches;       // bit per WATCH_*",
         "};", "",
         "struct HolidaySky", "{",
         "    u8 holiday;",
         "    u8 sky;           // DAEMONS_SKY_*",
         "    u8 mapsec;        // the centre",
         "    u8 radius;        // region-map cells, or 254 the whole region (as daemons_weather.c)",
         "    u8 watches;",
         "    u8 onlyIfClear;   // TRUE: only where the day's draw left the sky clear; FALSE: held over any weather",
         "};", ""]

    # months
    o.append("// The months: a note of the chromatic scale each, C (JAN) to B (DEC); 9.4-checked UI colours (A is INDIGO).")
    o.append("static const u16 sMonthColours[12] = {")
    for m in months:
        o.append("    RGB(%d, %d, %d),   // %s, %s" % (*m["rgb5"], m["month"], m["note"]))
    o.append("};")
    for m in months:
        o.append('static const u8 sMonthNote_%s[] = _("%s");' % (m["month"].title(), m["note"]))
    o.append("static const u8 *const sMonthNotes[12] = {%s};" % ", ".join("sMonthNote_%s" % m["month"].title() for m in months))
    o.append("// The toy piano's natural (SE_NOTE_C + n) and the bend to the flat, in semitones (m4aMPlayPitchControl x 256)")
    o.append("static const s8 sMonthNoteSound[12][2] = {%s};" % ", ".join(
        "{%d, %d}" % (NATURALS[m["note"][0]], -1 if m["note"].endswith("b") else 0) for m in months))
    o.append("")

    # the tables of moving dates
    o.append("// Easter Sunday, %d-%d, as days after March 21 (the Gregorian computus)." % (FIRST_YEAR, LAST_YEAR))
    o.append("static const u8 sEasterAfterMar21[] = {%s};" % ", ".join(
        str((easter(y) - datetime.date(y, 3, 21)).days) for y in YEARS))
    ma = next(h for h in doc["holidays"] if h["rule"]["kind"] == "table")["rule"]["dates"]
    o.append("// The Mid-Autumn Festival, %d-%d, as days after September 1 (the 15th of the 8th lunar month, as published)." % (FIRST_YEAR, LAST_YEAR))
    o.append("static const u8 sMidAutumnAfterSep1[] = {%s};" % ", ".join(
        str((datetime.date(y, int(ma[str(y)][:2]), int(ma[str(y)][3:])) - datetime.date(y, 9, 1)).days) for y in YEARS))
    o.append("")

    # the lead's GAIN
    o.append("// DEN DAY: the GAIN item of the party lead's first type. A lead that is ORACLE as EITHER type gets none -- its gift reads on to\n// THE YEAR's line (the user, 2026-10-18).")
    o.append("static const u16 sHolidayTypeGain[NUMBER_OF_MON_TYPES] = {")
    for t in types:
        o.append("    [%s] = %s," % (t, type_gain.get(t, "ITEM_NONE")))
    o.append("};")
    o.append("")

    # givers
    for g, v in doc["givers"].items():
        if v.get("say"):
            o.append('static const u8 sHolidaySay_%s[] = _("%s");' % (g.title().replace("_", ""), c_quote(v["say"]).replace("\n", "\\n")))
    o.append("static const u8 *const sHolidaySay[] = {")
    for g in GIVERS:
        v = doc["givers"].get(g, {})
        o.append("    [GIVER_%s] = %s," % (g, "sHolidaySay_" + g.title().replace("_", "") if v.get("say") else "NULL"))
    o.append("};")
    o.append("")

    # THE YEAR
    ty = doc["the_year"]
    o.append("// THE YEAR (a NOTEBOOK section): each line arrives the way an INSIGHT does, once ever.")
    o.append('const u8 gText_YearSection[] = _("%s");' % ty["section"])
    for l in doc["lines"]:
        cid = l["id"].title().replace("_", "")
        o.append('const u8 gYearTitle_%s[] = _("%s");' % (cid, c_quote(l["title"])))
        o.append('const u8 gYearText_%s[] = _("%s");' % (cid, c_quote(l["text"])))
        o.append('static const u8 sYearArrival_%s[] = _("%s");' % (cid, box([ty["arrival"], "“%s”" % l["text"], ty["filed"]])))
    o.append("static const u8 *const sYearArrivals[HOLIDAY_YEAR_LINE_COUNT] = {%s};"
             % ", ".join("sYearArrival_" + l["id"].title().replace("_", "") for l in doc["lines"]))
    o.append("static const u16 sYearLineFlags[HOLIDAY_YEAR_LINE_COUNT] = {%s};"
             % ", ".join("FLAG_YEAR_LINE_" + l["id"] for l in doc["lines"]))
    o.append("")

    # per edition
    for k, (ed, define) in enumerate(EDITIONS):
        rows = edition_rows(doc, ed)
        placed = play_watches(doc, ed)
        o.append("#%s defined(%s)   // %s" % ("if" if k == 0 else "elif", define, ed))
        o.append("#define HOLIDAY_EDITION %d" % k)
        for h in rows:
            o.append('static const u8 sHolidayName_%s[] = _("%s");' % (h["id"].title().replace("_", ""), c_quote(h["name"])))
        gifts, presents = [], None
        rowtext, shifts, skies = [], [], []
        for idx, h in enumerate(rows):
            hid = idx + 1
            first = len(gifts)
            for g in h["gift"]:
                give, w = g["give"], g.get("when", {})
                fl = ["HG_GO_ON"] if g.get("go_on") else []
                item, arg = "ITEM_NONE", 0
                if isinstance(give, str):
                    item = item_c(items, give)
                elif "line" in give:
                    fl.append("HG_LINE")
                    arg = line_index[give["line"]]
                elif give.get("lead_type_gain"):
                    fl.append("HG_LEAD_TYPE_GAIN")
                elif "year_draw" in give:
                    fl.append("HG_YEAR_DRAW")
                    presents = give["year_draw"]
                if w.get("storm_on_islands_today"):
                    fl.append("HG_STORM_ISLANDS")
                gifts.append("    { %s, %d, 0x%02X, 0x%02X, 0x%02X, %s, %d },   // %s"
                             % (item, g.get("count", 1), mask(w.get("watches", []), WATCHES), mask(w.get("sky", []), SKIES),
                                mask(w.get("weekdays", []), WEEKDAYS), " | ".join(fl) or "0", arg, h["name"]))
            r = h["rule"]
            kind = {"fixed": "FIXED", "season_start": "FIXED", "nth_weekday": "NTH_WEEKDAY", "easter": "EASTER",
                    "table": "MIDAUTUMN"}[r["kind"]]
            if r["kind"] == "fixed":
                arg, wd = r["day"], 0
            elif r["kind"] == "season_start":
                arg, wd = season_start(r["season"], ed)[1], 0
            elif r["kind"] == "nth_weekday":
                arg, wd = r["n"], r["weekday"]
            elif r["kind"] == "easter":
                arg, wd = r["offset"], 0
            else:
                arg, wd = 0, 0
            pw, anchor, _moved = placed[h["id"]]
            fl = (["HF_QUIET"] if h.get("quiet") else []) + (["HF_EVE_FROM_DUSK"] if h.get("eve_from_hour") == 18 else []) \
                + (["HF_OTHER_EDITION"] if h.get("other_edition") else []) + (["HF_STEPS_OFF"] if h.get("steps_off") else []) \
                + ["HF_" + x.upper() for x in h.get("overlay", [])]
            if h.get("eve_from_hour") not in (None, 18):
                raise SystemExit("genholidays: only an eve from dusk (18) is built")
            rowtext.append("    [%s - 1] = { sHolidayName_%s, %s, HOLIDAY_RULE_%s, %d, %d, %d, %d, %d, %d, %d, 0x%X, GIVER_%s, %d, %d },"
                           % (const_id(h), h["id"].title().replace("_", ""), " | ".join(fl) or "0", kind, h["month"], arg, wd,
                              h["days"], anchor.month, anchor.day, pw, mask(h.get("banner_watches", WATCHES), WATCHES),
                              h["giver"], first, len(gifts) - first))
            for dm in h["daemons"]:
                nm = dm.get("species") or dm["name"]
                nm = nm.split("|")[k] if "|" in nm else nm
                for mp in dm["maps"]:
                    slot = dm["slot"]
                    if slot == "season":
                        slot = shift_slots[mp][0]
                    elif slot == "hour":
                        slot = shift_slots[mp][1]
                    shifts.append("    { %s, %s, MAP_GROUP(%s), MAP_NUM(%s), HOLIDAY_AREA_%s, %2d, 0x%X },   // %s, %s"
                                  % (species[nm][0], const_id(h), mp, mp, dm["area"].upper(), slot,
                                     mask(dm["watches"], WATCHES), h["name"], nm))
            if h.get("sky"):
                s = h["sky"]
                skies.append("    { %s, DAEMONS_SKY_%s, %s, %s, 0x%X, %s },   // %s"
                             % (const_id(h), s["kind"], s["mapsec"], "254" if s["radius"] == "region" else s["radius"],
                                mask(s["watches"], WATCHES), "TRUE" if s.get("only_if_clear") else "FALSE", h["name"]))
        o.append("static const struct HolidayGift sHolidayGifts[] = {")
        o += gifts
        o.append("};")
        o.append("static const u16 sHolidayPresents[] = {%s};" % ", ".join(items[x] for x in presents))
        o.append("static const struct HolidayRow sHolidays[HOLIDAY_COUNT] = {")
        o += rowtext
        o.append("};")
        o.append("static const struct HolidayShift sHolidayShifts[] = {")
        o += shifts
        o.append("};")
        o.append("static const struct HolidaySky sHolidaySkies[] = {")
        o += skies
        o.append("};")
    o += ["#endif", ""]
    return "\n".join(o)


def lines_header(doc):
    o = ["// Generated by DAEMONS tools/genholidays.py from docs/holidays.json -- edit the json, not this file.",
         "// T-416: THE YEAR's NOTEBOOK entries, in the order of the year. Included once, by src/notebook.c, which adds",
         "// NB_THE_YEAR to its sections (named gText_YearSection). The words live in src/daemons_holidays.c. DRAFT.",
         "#ifndef GUARD_DATA_HOLIDAY_LINES_H", "#define GUARD_DATA_HOLIDAY_LINES_H", ""]
    o.append("extern const u8 gText_YearSection[];")
    for l in doc["lines"]:
        cid = l["id"].title().replace("_", "")
        o.append("extern const u8 gYearTitle_%s[];" % cid)
        o.append("extern const u8 gYearText_%s[];" % cid)
    o += ["", "#define NB_YEAR_ENTRIES \\"]
    for l in doc["lines"]:
        cid = l["id"].title().replace("_", "")
        o.append("    { NB_THE_YEAR, NB_KIND_TEXT, 0, FLAG_YEAR_LINE_%s, 0, gYearTitle_%s, gYearText_%s }, \\" % (l["id"], cid, cid))
    o += ["", "#endif // GUARD_DATA_HOLIDAY_LINES_H", ""]
    return "\n".join(o)


# ---- the companion ------------------------------------------------------------------------------------------------

def companion_doc(doc):
    """companion/server/data/holidays.json in server/src/holidays.ts's Row shape, from the game's table."""
    rows = []
    for h in doc["holidays"]:
        r = h["rule"]
        rule = dict(r)
        row = {"name": h["real"], "edition": "both" if h["edition"] == "COMMON" else h["edition"], "rule": rule,
               "days": h["days"]}
        if h.get("steps_off"):          # the companion has no ids: the real name of the holiday it steps off
            row["steps_off"] = next(o["real"] for o in doc["holidays"] if o["id"] == h["steps_off"])
        if h.get("quiet"):
            row["quiet"] = True
        else:
            row.update(h.get("companion", {}))
        rows.append(row)
    for extra in doc.get("companion_only", []):
        rows.append({k: v for k, v in extra.items() if k != "about"})
    return {
        "_about": ("C-149: the holidays on the real calendar, by their real names (DAEMONS T-416, decided by the user "
                   "2026-10-17: in-world names in the game, the real names in the companion). Three a month: one COMMON "
                   "to both editions, one NORTHERN for CONTENT, one SOUTHERN for CONTEXT, and New Year's Eve beside "
                   "Christmas. Written by DAEMONS tools/companion_export.py from the game's table (docs/holidays.json, "
                   "through tools/genholidays.py). 'look', 'colours' and 'hat' are how a board dresses for the day (the "
                   "CASINO's reels first); a QUIET day is left as it is. Every look DRAFT."),
        "rules": ("fixed: month, day. nth_weekday: month, n (1st..4th), weekday (0 Sunday). easter: days after Easter "
                  "Sunday. table: one date a year, 'MM-DD' by year. season_start: the day the edition's own season "
                  "begins (seasons.json). 'days' long from there."),
        "steps_off": ("the real name of a COMMON holiday this one is not on the day of: that day is the other's, and "
                      "this one goes on inside its own span (T-416: SCIENCE FAIR off FLEDGLING DAY, the user, 2026-10-18)."),
        "holidays": rows,
    }


def companion_text(doc):
    d = companion_doc(doc)
    head = json.dumps({"_about": d["_about"], "steps_off": d["steps_off"], "rules": d["rules"]},
                      ensure_ascii=False, indent=1)[:-2]
    body = ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in d["holidays"])
    return head + ',\n "holidays": [\n' + body + "\n ]\n}\n"


# ---- main ---------------------------------------------------------------------------------------------------------

def main():
    doc = json.load(open(SRC, encoding="utf-8"))
    if "--companion" in sys.argv:
        sys.stdout.write(companion_text(doc))
        return 0
    names = name_tables()
    wild, met = wild_tables()
    errors, notes = [], []
    check(doc, names, wild, met, errors, notes)
    new_flags = flags_after(doc, errors)
    new_vars = vars_after(errors)

    print("  %d holidays (%d per ROM), %d lines for THE YEAR, %d gifts"
          % (len(doc["holidays"]), 24, len(doc["lines"]), sum(len(h["gift"]) for h in doc["holidays"])))
    for n in notes:
        print("  " + n)

    # the play-time year, and the days with two
    for ed, _ in EDITIONS:
        rows = edition_rows(doc, ed)
        placed = play_watches(doc, ed)
        taken = {w for w, _d, _m in placed.values()}
        moved = ["%s +%d" % (h["name"], placed[h["id"]][2]) for h in rows if placed[h["id"]][2]]
        both = {}
        for y in YEARS:
            on = {}
            for day, hs in days_on(rows, y, ed).items():
                on[day] = [h["name"] for h in hs]
            for day, n in on.items():
                if len(n) > 1:
                    both.setdefault(" + ".join(sorted(n)), []).append(day.isoformat())
        print("  %s: no clock, %d of 112 watches hold a holiday (%.0f%% of play)%s"
              % (ed, len(taken), 100 * len(taken) / 112,
                 "" if not moved else "; moved on a watch to stand alone: " + ", ".join(moved)))
        for k, v in sorted(both.items()):
            print("    two on one day, %d of %d-%d: %s (%s%s)" % (len(v), FIRST_YEAR, LAST_YEAR, k, v[0], ", ..." if len(v) > 1 else ""))

    if errors:
        for e in errors:
            print("  !! " + e)
        return 1

    outs = [(OUT_TABLE, table_header(doc, names)), (OUT_LINES, lines_header(doc)), (OUT_CONST, const_header(doc)),
            (FLAGS_H, new_flags), (VARS_H, new_vars)]
    stale = []
    for path, text in outs:
        old = read(path) if os.path.exists(path) else None
        if old != text:
            stale.append(path)
            print("  %s %s" % (os.path.relpath(path, ROOT), "to write" if old is None else "differs"))
        else:
            print("  %s already written" % os.path.relpath(path, ROOT))
    if os.path.exists(COMPANION):
        same = json.load(open(COMPANION, encoding="utf-8"))["holidays"] == companion_doc(doc)["holidays"]
        print("  companion's holidays.json %s (companion_export.py writes it; --companion prints it)"
              % ("matches the game's table" if same else "differs from the game's table"))
    if WRITE and stale:
        for path, text in outs:
            if path in stale:
                open(path, "w", encoding="utf-8").write(text)
                print("  written %s" % os.path.relpath(path, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())

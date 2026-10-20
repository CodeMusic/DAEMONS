#!/usr/bin/env python3
"""T-422: the GAME CORNER plays as the companion's CASINO -- its table, its luck, its pieces and its tunes, carried in.

    python3 tools/gencasino.py            # report: what would change, and whether the game still agrees
    python3 tools/gencasino.py --write    # engineGba/src/data/daemons_casino.h and graphics/slot_machine/daemons/*.png

The user, 2026-10-18 (confirmed by phone): the GAME CORNER's reels become the companion's, on the companion's engine
-- "same numbers, so the game and the devices agree". So nothing here is typed: every number is READ from the
companion (READ ONLY -- this tool never writes there):

  server/src/slots.ts, firmware/common/slots.h   the table (WEIGHTS, PAYS), the return for a luck (90..100 back), the
                                                 cat and the string (REACH_SPAN, LEARN, NOISE, TARGET), near misses
  server/src/context.ts                          the luck a holiday, a sky, a watch and a season each add
  firmware/common/tunes.h                        TUNE_SLOTS_*, in semitones over the day's note
  server/data/casino_art.json, art/casino/*.png  the coin, the season's pieces and the hats (56x56 -> 28x28, outlined)
  docs/holidays.json (ours)                      each holiday's look, colours and hat ("companion" block)

and the game plays them in whole numbers (ten-thousandths of a return, hundredths of luck) -- no floats on the GBA.
The report also HOLDS the game to the companion, the way the companion's own tests hold slots.h to slots.ts:
  * slots.ts and slots.h agree (the companion's two copies)
  * the game's whole-number table for every return from 86 to 104 (each ten-thousandth) is slots.ts's weightsFor,
    rounded as Math.round rounds the exact value, and pays that return to within a hundredth
  * the game's return for every luck (each hundredth) is RETURN_AT's
and fails (exit 1) on any disagreement. A stale generated file is "would write", as every generator here reports it.
"""
import json, os, re, sys
from collections import Counter
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT_H = os.path.join(GBA, "src", "data", "daemons_casino.h")
OUT_DIR = os.path.join(GBA, "graphics", "slot_machine", "daemons")
HOLIDAYS = os.path.join(ROOT, "docs", "holidays.json")
HOLIDAYS_H = os.path.join(GBA, "include", "constants", "holidays.h")


def companion_root():
    for p in (os.path.join(ROOT, "companion"), os.path.expanduser("~/Projects/daemons-companion")):
        if os.path.isdir(os.path.join(p, "server", "src")):
            return os.path.realpath(p)
    return None


# ---------------------------------------------------------------------------------------------------- reading them

def nums(text, name):
    m = re.search(r"\b%s\s*=\s*\[([^\]]*)\]" % name, text) or re.search(r"\b%s\[\]\s*=\s*\{([^}]*)\}" % name, text)
    if not m:
        raise SystemExit("gencasino: %s not found" % name)
    return [int(x) for x in m.group(1).split(",") if x.strip()]


def num(text, name):
    m = re.search(r"\b%s\s*=\s*(-?[0-9.]+)f?\b" % name, text)
    if not m:
        raise SystemExit("gencasino: %s not found" % name)
    return float(m.group(1))


def engine(comp):
    ts = open(os.path.join(comp, "server", "src", "slots.ts")).read()
    h = open(os.path.join(comp, "firmware", "common", "slots.h")).read()
    e = {"WEIGHTS": nums(ts, "WEIGHTS"), "PAYS": nums(ts, "PAYS"), "BETS": nums(ts, "BETS"),
         "STRIP": int(num(ts, "STRIP")), "REACH_SPAN": num(ts, "REACH_SPAN"), "LEARN": num(ts, "LEARN"),
         "NOISE": num(ts, "NOISE"), "FINE": int(num(ts, "FINE"))}
    problems = []
    for k in ("WEIGHTS", "PAYS", "BETS"):
        if nums(h, k) != e[k]:
            problems.append("slots.h's %s is not slots.ts's" % k)
    for k in ("REACH_SPAN", "LEARN", "NOISE", "FINE"):
        if num(h, k) != e[k]:
            problems.append("slots.h's %s is not slots.ts's" % k)
    if int(num(h, "STRIP_N")) != e["STRIP"]:
        problems.append("slots.h's STRIP_N is not slots.ts's STRIP")
    # the formulas, as the companion's own test reads them
    m = re.search(r"RETURN_AT = \(luck: number\) => Math\.min\(([0-9.]+), Math\.max\(([0-9.]+), ([0-9.]+) \+ ([0-9.]+) \* "
                  r"Math\.max\(-1, Math\.min\(1, luck\)\)\)\)", ts)
    pr = re.search(r"Math\.min\(([0-9.]+), Math\.max\(([0-9.]+), RETURN_AT\(luck\) \+ REACH_SPAN \* cat\.reach\)\)", ts)
    nc = re.search(r"nearChance = \(cat: Cat\) => Math\.min\(([0-9.]+), ([0-9.]+) \+ ([0-9.]+) \* Math\.max\(0, cat\.reach\)\)", ts)
    if not (m and pr and nc):
        raise SystemExit("gencasino: slots.ts's RETURN_AT, pullReturn or nearChance has a new shape -- port it here")
    e["RET_HIGH"], e["RET_LOW"], e["RET_MID"], e["RET_PER"] = (float(x) for x in m.groups())
    e["PULL_HIGH"], e["PULL_LOW"] = (float(x) for x in pr.groups())
    e["NEAR_MAX"], e["NEAR_BASE"], e["NEAR_PER"] = (float(x) for x in nc.groups())
    if "0.95f + 0.05f * clampf(luck, -1, 1)" not in h or "0.25f + 0.35f *" not in h:
        problems.append("slots.h's returnAt or nearChance is not slots.ts's")
    w, p = e["WEIGHTS"], e["PAYS"]
    e["RETURN"] = Fraction(sum(a * b for a, b in zip(w, p)), 1000)                     # 0.944
    e["TARGET"] = Fraction(sum(w[2:]), 1000)                                             # 0.126
    if abs(num(h, "BASE_RETURN") - float(e["RETURN"])) > 1e-9 or abs(num(h, "TARGET") - float(e["TARGET"])) > 1e-9:
        problems.append("slots.h's BASE_RETURN or TARGET is not the table's")
    # the pieces, and what makes each result: the game ports outcomeOf/piecesFor by hand -- hold the shape
    if 'PIECES = ["JACK", "F1", "F2", "F3", "COIN", "SEASON"]' not in ts or \
       'OUTCOMES = ["LOSE", "SEASON1", "JACK2", "SEASON3", "COIN3", "FRIEND3", "JACK3"]' not in ts:
        problems.append("slots.ts's PIECES or OUTCOMES moved -- the game's piecesFor needs porting again")
    oc = re.search(r"export function outcomeOf\(a: number, b: number, c: number\): number \{(.*?)\n\}", ts, re.S)
    want = ("if (a === b && b === c) return a === JACK ? 6 : a === COIN ? 4 : a === SEASON ? 3 : 5;"
            "if (a === JACK && b === JACK) return 2;if (a === SEASON) return 1;return 0;")
    if not oc or re.sub(r"\s*\n\s*", "", oc.group(1)).strip() != want:
        problems.append("slots.ts's outcomeOf changed -- the game's CasinoOutcomeOf needs porting again")
    return e, problems


def luck_numbers(comp):
    t = open(os.path.join(comp, "server", "src", "context.ts")).read()
    m = re.search(r"if \(/([^/]+)/i\.test\(holiday\.name\)\) reasons\.push\(\{ source: \"holiday\", effect: ([0-9.]+)", t)
    f = re.search(r"else reasons\.push\(\{ source: \"holiday\", effect: ([0-9.]+), why: `\$\{holiday\.name\}: ([^`]*)`", t)
    q = re.search(r"holiday\?\.quiet\) reasons\.push\(\{ source: \"holiday\", effect: ([0-9.]+), why: `\$\{holiday\.name\}: ([^`]*)`", t)
    lucky_why = re.search(r"effect: [0-9.]+, why: `\$\{holiday\.name\}: ([^`]*)` \}\);\s*\n\s*else", t)

    def table(keys):
        out = {}
        for k in keys:
            mm = re.search(r"\b%s: \[(-?[0-9.]+), \"([^\"]*)\"\]" % k, t)
            if not mm:
                raise SystemExit("gencasino: context.ts has no %s -- port it here" % k)
            out[k] = (round(float(mm.group(1)) * 100), mm.group(2))
        return out
    if not (m and f and q and lucky_why):
        raise SystemExit("gencasino: context.ts's holiday luck has a new shape -- port it here")
    return {"lucky_re": m.group(1), "lucky": round(float(m.group(2)) * 100), "lucky_why": lucky_why.group(1),
            "festive": round(float(f.group(1)) * 100), "festive_why": f.group(2),
            "quiet": round(float(q.group(1)) * 100), "quiet_why": q.group(2),
            "sky": table(["clear", "cloudy", "fog", "rain", "snow", "storm"]),
            "watch": table(["DAWN", "DAY", "DUSK", "NIGHT"]),
            "season": table(["spring", "summer", "autumn", "winter"])}


def tunes(comp):
    t = open(os.path.join(comp, "firmware", "common", "tunes.h")).read()
    out = []
    for m in re.finditer(r"static const Note (TUNE_SLOTS_\w+)\[\]\s*=\s*\{(.*?)\};", t, re.S):
        notes = [(int(a), int(b)) for a, b in re.findall(r"\{\s*(-?\d+)\s*,\s*(\d+)\s*\}", m.group(2))]
        out.append((m.group(1), notes))
    if not out:
        raise SystemExit("gencasino: no TUNE_SLOTS_* in tunes.h")
    return out


# ------------------------------------------------------------------------------------------- the game's whole numbers

def game_weights(e, ret):
    """The game's table for a return in ten-thousandths: each win's weight * 10 * ret / RETURN, rounded half up."""
    base = int(e["RETURN"] * 10000)                                       # 9440
    wins = [(2 * w * 10 * ret + base) // (2 * base) for w in e["WEIGHTS"][1:]]
    return [e["FINE"] - sum(wins)] + wins


def ts_weights(e, ret):
    """slots.ts's weightsFor, Math.round on the exact value (a float may land either side of an exact half)."""
    k = Fraction(ret, 10000) / e["RETURN"]
    wins = [int(w * 10 * k + Fraction(1, 2)) for w in e["WEIGHTS"][1:]]   # Math.round: half up
    return [e["FINE"] - sum(wins)] + wins


def check(e):
    bad = []
    lo, hi = round(e["PULL_LOW"] * 10000), round(e["PULL_HIGH"] * 10000)
    for ret in range(lo, hi + 1):
        g, t = game_weights(e, ret), ts_weights(e, ret)
        if g != t:
            bad.append("return %d: game %s, slots.ts %s" % (ret, g, t))
            continue
        paid = sum(a * b for a, b in zip(g, e["PAYS"])) / e["FINE"]
        if abs(paid - ret / 10000) > 0.005:                                 # the companion's toBeCloseTo(r, 2)
            bad.append("return %d: the table pays %.4f" % (ret, paid))
        # the float JS would compute, away from an exact half, must round the same
        kf = (ret / 10000) / (sum(a * b for a, b in zip(e["WEIGHTS"], e["PAYS"])) / 1000)
        for i, w in enumerate(e["WEIGHTS"][1:]):
            x = Fraction(w * 10 * ret, 10000) / e["RETURN"]
            if x.denominator != 2 and int(w * 10 * kf + 0.5) != g[i + 1]:
                bad.append("return %d, outcome %d: JS's float rounds differently" % (ret, i + 1))
    # the whole engine as the game plays it, in whole numbers (src/daemons_casino.c): over many pulls the money that
    # comes back is the day's return, the string's shaping washing out (slots.test.ts's own check, 0.012)
    import random
    rng = random.Random(11)
    base = round(e["RET_MID"] * 10000)
    won_step = round(e["LEARN"] * (1 - e["TARGET"]) * 10000)
    lost_step = round(e["LEARN"] * e["TARGET"] * 10000)
    noise = round(e["NOISE"] * 10000)
    span = round(e["REACH_SPAN"] * 10000)
    tables = {}
    reach, bet, back = 0, 0, 0
    for _ in range(300000):
        ret = max(round(e["PULL_LOW"] * 10000), min(round(e["PULL_HIGH"] * 10000), base + int(span * reach / 10000)))
        w = tables.get(ret) or tables.setdefault(ret, game_weights(e, ret))
        r = rng.randrange(e["FINE"])
        o = 0
        while r >= w[o]:
            r -= w[o]
            o += 1
        bet += 1
        back += e["PAYS"][o]
        won = e["PAYS"][o] >= 2
        reach = max(-10000, min(10000, reach + (-won_step if won else lost_step) + rng.randint(-noise, noise)))
    e["SIM"] = back / bet
    if abs(back / bet - base / 10000) > 0.012:
        bad.append("300000 pulls at luck 0 came back %.4f, not %.4f" % (back / bet, base / 10000))
    for luck in range(-150, 151):
        g = max(round(e["RET_LOW"] * 10000), min(round(e["RET_HIGH"] * 10000),
                round(e["RET_MID"] * 10000) + round(e["RET_PER"] * 100) * max(-100, min(100, luck))))
        t = min(e["RET_HIGH"], max(e["RET_LOW"], e["RET_MID"] + e["RET_PER"] * max(-1, min(1, luck / 100))))
        if abs(g - t * 10000) > 1e-6:
            bad.append("luck %d: game %d, RETURN_AT %.6f" % (luck, g, t))
    return bad


# ---------------------------------------------------------------------------------------------------------- the art

CASINO_INK = 0x181C21


def art_palette(comp):
    src = open(os.path.join(comp, "firmware", "common", "casino_art.h")).read()
    m = re.search(r"CASINO_PALETTE\[\d+\]\s*=\s*\{([^}]*)\}", src)
    cols = [int(x, 16) for x in m.group(1).split(",") if x.strip()]
    return {4 + i: c for i, c in enumerate(cols)}


def shrink(path, fixed):
    """A picture half size: each 2x2 block takes its commonest colour if two or more of its pixels are drawn; then a
    true-black outline round it (T-184), so a white snowflake reads on the GBA's white reel. Returns ({(x,y): slot}, w, h)
    where a slot is 1 colourA, 2 colourB, 3 the day's, or ('rgb', 0xRRGGBB)."""
    from PIL import Image
    im = Image.open(path)
    W, H = im.size
    px = im.load()
    out = {}
    for y in range(H // 2):
        for x in range(W // 2):
            c = Counter(px[2 * x + dx, 2 * y + dy] for dx in (0, 1) for dy in (0, 1))
            drawn = [(v, n) for v, n in c.items() if v]
            if sum(n for _, n in drawn) >= 2:
                v = max(drawn, key=lambda t: (t[1], -t[0]))[0]
                out[(x, y)] = v if v <= 3 else ("rgb", fixed[v])
    w, h = W // 2, H // 2
    edge = {}
    for y in range(h):
        for x in range(w):
            if (x, y) not in out and any((x + dx, y + dy) in out for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                edge[(x, y)] = ("rgb", CASINO_INK)
    out.update(edge)
    return out, w, h


def rgb15(c):
    return ((c >> 19) & 31) | (((c >> 11) & 31) << 5) | (((c >> 3) & 31) << 10)


def pieces(comp, art):
    """Every piece a 32x32 frame of 4bpp, each with its own palette: 1 A, 2 B, 3 the day's (filled at run time), then
    the piece's own colours from 4."""
    fixed = art_palette(comp)
    frames, pals = [], []
    for name in art["pieces"]:
        pix, w, h = shrink(os.path.join(comp, "server", "data", "art", "casino", name + ".png"), fixed)
        own = sorted({v[1] for v in pix.values() if isinstance(v, tuple)})
        if len(own) > 12:
            raise SystemExit("gencasino: %s has %d colours" % (name, len(own)))
        index = {c: 4 + i for i, c in enumerate(own)}
        ox, oy = (32 - w) // 2, (32 - h) // 2
        frame = [[0] * 32 for _ in range(32)]
        for (x, y), v in pix.items():
            frame[oy + y][ox + x] = v if isinstance(v, int) else index[v[1]]
        frames.append(frame)
        pals.append([0, 0, 0, 0] + [rgb15(c) for c in own] + [0] * (12 - len(own)))
    return frames, pals


def hats(comp, art):
    fixed = art_palette(comp)
    out = []
    for name in art["hats"]:
        pix, w, h = shrink(os.path.join(comp, "server", "data", "art", "casino", "hat_%s.png" % name), fixed)
        a = art["hats"][name]
        out.append((name, pix, w, h, a["x"] // 2, a["y"] // 2))
    return out


# the falling season: one 8x8 tile per shape and colour. Palette: 1 A, 2 B, then fixed colours
BITS_PAL = [0, 0, 0, 0xFFFFFF, 0x60A8FF, 0x20B040, 0xFF7A1A, 0x2E7D32, 0x8A8E96, 0xFFFBF7,
            0xFF4060, 0xFFD040, 0x40C0FF, 0x60E060, 0xC060FF, 0x181C21]


def bit_tiles():
    def blank():
        return [[0] * 8 for _ in range(8)]

    def disc(r, c):
        t = blank()
        for y in range(8):
            for x in range(8):
                if (x - 3.5) ** 2 + (y - 3.5) ** 2 <= (r + 0.5) ** 2:
                    t[y][x] = c
        return t

    def rows(lines, cmap):
        t = blank()
        for y, row in enumerate(lines):
            for x, ch in enumerate(row):
                if ch != ".":
                    t[y][x] = cmap[ch]
        return t
    tiles = {}
    for c, tag in ((1, "A"), (2, "B")):
        tiles["DOT1_" + tag] = rows(["........", "........", "........", "...##...", "...##...", "........", "........", "........"], {"#": c})
        tiles["DOT2_" + tag] = disc(1.5, c)
    # snow is white, ringed in grey: the GBA's reels are white where the companion's boards are dark
    tiles["DOT1_WHITE"] = rows(["........", "........", "...gg...", "..g##g..", "..g##g..", "...gg...", "........", "........"], {"#": 3, "g": 8})
    tiles["DOT2_WHITE"] = rows(["........", "..ggg...", ".g###g..", ".g###g..", ".g###g..", "..ggg...", "........", "........"], {"#": 3, "g": 8})
    for c, tag in ((1, "A"), (2, "B")):
        tiles["PETAL_" + tag] = rows(["........", "........", "..####..", ".######.", ".######.", "..####..", "........", "........"], {"#": c})
        tiles["LEAF_" + tag] = rows(["...#....", "..###...", ".#####..", "#######.", ".#####..", "..###...", "...#....", "........"], {"#": c})
        tiles["HEART_" + tag] = rows(["........", ".##.##..", "#######.", "#######.", ".#####..", "..###...", "...#....", "........"], {"#": c})
        tiles["EGG_" + tag] = rows(["...##...", "..####..", ".######.", ".######.", ".######.", ".######.", "..####..", "...##..."], {"#": c})
        tiles["PRESENT_" + tag] = rows(["........", "..#o#...", "..#o#...", "..#o#...", "..#o#...", "..#o#...", "........", "........"], {"#": c, "o": 9})
        for k, r in enumerate((0, 1, 2, 3)):
            tiles["TWINKLE%d_%s" % (k, tag)] = rows([("...#...." if abs(y - 3) <= r else "........") if y != 3 else
                                                     "." * (3 - r) + "#" * (2 * r + 1) + "." * (8 - (3 - r) - (2 * r + 1))
                                                     for y in range(8)], {"#": c})
    tiles["CLOVER"] = rows(["........", ".##.##..", "#######.", "#######.", ".#####..", "..###...", "...#....", "........"], {"#": 5})
    tiles["PUMPKIN"] = rows(["...g....", "...g....", "..ooo...", ".ooooo..", ".ooooo..", "..ooo...", "........", "........"], {"o": 6, "g": 7})
    tiles["RAIN"] = rows(["....#...", "....#...", "...#....", "...#....", "..#.....", "..#.....", "........", "........"], {"#": 4})
    tiles["FOG"] = rows(["........", "........", "........", "########", "........", "........", "........", "........"], {"#": 8})
    for i in range(5):
        w = 3 + i % 3
        tiles["CONFETTI%d" % i] = rows(["........", "........", "........", "#" * w + "." * (8 - w), "#" * w + "." * (8 - w), "........", "........", "........"], {"#": 10 + i})
    return tiles


# each look: the piece's art, and what falls (BITS: the kind; its colours chosen A/B as casino.cpp does)
FALL = {"snow": "SNOW", "frost": "DOT", "petals": "PETAL", "leaves": "LEAF", "hearts": "HEART", "confetti": "CONFETTI",
        "streamers": "CONFETTI", "clover": "CLOVER", "eggs": "EGG", "pumpkins": "PUMPKIN", "presents": "PRESENT",
        "fireworks": "SPARK", "rain": "RAIN", "storm": "RAIN", "fog": "FOG"}            # the rest twinkle
RISES = {"hearts", "fireworks"}


def looks(art):
    names = list(art["pieces"]) + ["stars", "confetti", "streamers"]
    return [(n, art["pieces"].index(n) if n in art["pieces"] else art["pieces"].index("star")) for n in names]


# ----------------------------------------------------------------------------------------------------- the holidays

def holiday_rows(luck):
    data = json.load(open(HOLIDAYS))["holidays"]
    by_id = {h["id"]: h for h in data}
    text = open(HOLIDAYS_H).read()
    out = {}
    for ed, guard in (("CONTENT", "FIRERED"), ("CONTEXT", "LEAFGREEN")):
        ids = {}
        common = text.split("#if defined(FIRERED)")[0]
        mine = re.search(r"#%s defined\(%s\)(.*?)(#elif|#endif)" % ("if" if guard == "FIRERED" else "elif", guard), text, re.S).group(1)
        for m in re.finditer(r"#define HOLIDAY_(\w+)\s+(\d+)\s+//", common + mine):
            if m.group(1) in by_id:
                ids[int(m.group(2))] = by_id[m.group(1)]
        out[guard] = ids
    return out


def colour(s):
    return int(s.lstrip("#"), 16) if s else None


# ---------------------------------------------------------------------------------------------------------- writing

def c_string(s):
    return s.replace('"', '\\"')


def header(e, luck, tune_list, art, look_list, hat_list, holidays, piece_pals, tiles):
    L = []
    w = L.append
    w("// Generated by DAEMONS tools/gencasino.py from the companion (server/src/slots.ts, firmware/common/slots.h,")
    w("// server/src/context.ts, firmware/common/tunes.h, server/data/casino_art.json) and docs/holidays.json -- edit those,")
    w("// not this. T-422 (the user, 2026-10-18): the GAME CORNER plays by the companion's CASINO, in whole numbers.")
    w("// Every word below is DRAFT.")
    w("#ifndef GUARD_DATA_DAEMONS_CASINO_H")
    w("#define GUARD_DATA_DAEMONS_CASINO_H")
    w("")
    w("// ---- the table (slots.ts WEIGHTS, PAYS): the chance of each result in a thousand, and its pay for each coin bet")
    w("// (the results and the pieces, CASINO_LOSE.. and CASINO_JACK.., are include/daemons_casino.h's, slots.ts's order)")
    w("static const u16 sCasinoWeights[CASINO_OUTCOME_COUNT] = {%s};" % ", ".join(map(str, e["WEIGHTS"])))
    w("static const u8 sCasinoPays[CASINO_OUTCOME_COUNT] = {%s};" % ", ".join(map(str, e["PAYS"])))
    w("#define CASINO_STRIP        %d      // each piece twice round a reel" % e["STRIP"])
    w("STATIC_ASSERT(CASINO_STRIP == CASINO_STRIP_LENGTH, CasinoStripIsTheCompanions);")
    w("#define CASINO_FINE         %d   // a table for any return is kept in ten thousand" % e["FINE"])
    w("#define CASINO_BASE_RETURN  %d    // the table's own return, in ten-thousandths" % int(e["RETURN"] * 10000))
    w("// RETURN_AT: the day's return from its luck (hundredths, -100..100), in ten-thousandths")
    w("#define CASINO_RETURN_MID   %d" % round(e["RET_MID"] * 10000))
    w("#define CASINO_RETURN_PER   %d       // for each hundredth of luck" % round(e["RET_PER"] * 100))
    w("#define CASINO_RETURN_LOW   %d" % round(e["RET_LOW"] * 10000))
    w("#define CASINO_RETURN_HIGH  %d" % round(e["RET_HIGH"] * 10000))
    w("// pullReturn: the string's reach (ten-thousandths, -10000..10000) moves a pull's return by up to REACH_SPAN")
    w("#define CASINO_REACH_SPAN   %d     // ten-thousandths of return, at the string's nearest" % round(e["REACH_SPAN"] * 10000))
    w("#define CASINO_PULL_LOW     %d" % round(e["PULL_LOW"] * 10000))
    w("#define CASINO_PULL_HIGH    %d" % round(e["PULL_HIGH"] * 10000))
    w("// learn: a step against the error -- a real win (2x and up) takes the string away, a loss brings it nearer -- and noise")
    w("#define CASINO_LEARN_WON    %d    // LEARN * (1 - TARGET)" % round(e["LEARN"] * (1 - e["TARGET"]) * 10000))
    w("#define CASINO_LEARN_LOST   %d     // LEARN * TARGET" % round(e["LEARN"] * e["TARGET"] * 10000))
    w("#define CASINO_NOISE        %d     // either way, at most" % round(e["NOISE"] * 10000))
    w("// nearChance: a loss falls near this often (ten-thousandths), oftener the nearer the string")
    w("#define CASINO_NEAR_BASE    %d" % round(e["NEAR_BASE"] * 10000))
    w("#define CASINO_NEAR_PER     %d       // hundredths of a chance for each hundredth of reach" % round(e["NEAR_PER"] * 100))
    w("#define CASINO_NEAR_MAX     %d" % round(e["NEAR_MAX"] * 10000))
    w("")
    w("// ---- the luck (context.ts casinoContext), in hundredths, and why -- the GAME's world: its holiday, sky, watch, season")
    w("#define CASINO_LUCK_LUCKY_DAY   %d   // a holiday matching /%s/ (the companion's name for it)" % (luck["lucky"], luck["lucky_re"]))
    w("#define CASINO_LUCK_FESTIVE     %d" % luck["festive"])
    w("#define CASINO_LUCK_QUIET       %d" % luck["quiet"])
    sky = {"DAEMONS_SKY_CLEAR": "clear", "DAEMONS_SKY_RAIN": "rain", "DAEMONS_SKY_STORM": "storm",
           "DAEMONS_SKY_SNOW": "snow", "DAEMONS_SKY_FOG": "fog", "DAEMONS_SKY_WIND": "cloudy"}
    w("// the game's WIND has no row of the companion's: it is its cloudy (a sky with nothing to say)")
    w("static const s8 sCasinoLuckSky[DAEMONS_SKY_COUNT] = {%s};" % ", ".join(
        "[%s] = %d" % (k, luck["sky"][v][0]) for k, v in sky.items()))
    watch = {"WATCH_DAY": "DAY", "WATCH_DUSK": "DUSK", "WATCH_NIGHT": "NIGHT", "WATCH_DAWN": "DAWN"}
    w("static const s8 sCasinoLuckWatch[WATCH_COUNT] = {%s};" % ", ".join(
        "[%s] = %d" % (k, luck["watch"][v][0]) for k, v in watch.items()))
    season = {"SEASON_WINTER": "winter", "SEASON_SPRING": "spring", "SEASON_SUMMER": "summer", "SEASON_AUTUMN": "autumn"}
    w("static const s8 sCasinoLuckSeason[SEASON_COUNT] = {%s};" % ", ".join(
        "[%s] = %d" % (k, luck["season"][v][0]) for k, v in season.items()))
    w("static const u8 sCasinoWhyLucky[] = _(\"%s\");" % c_string(luck["lucky_why"]))
    w("static const u8 sCasinoWhyFestive[] = _(\"%s\");" % c_string(luck["festive_why"]))
    for table, keys in (("Sky", sky), ("Watch", watch), ("Season", season)):
        src = {"Sky": luck["sky"], "Watch": luck["watch"], "Season": luck["season"]}[table]
        for k, v in keys.items():
            w("static const u8 sCasinoWhy%s_%s[] = _(\"%s\");" % (table, k, c_string(src[v][1])))
        size = {"Sky": "DAEMONS_SKY_COUNT", "Watch": "WATCH_COUNT", "Season": "SEASON_COUNT"}[table]
        w("static const u8 *const sCasinoWhy%s[%s] = {%s};" % (table, size, ", ".join(
            "[%s] = sCasinoWhy%s_%s" % (k, table, k) for k in keys)))
    w("")
    w("// ---- how it is dressed: the looks (casino.cpp lookNow), each with its piece's art and what falls over the reels")
    w("enum {")
    for i, (n, _) in enumerate(look_list):
        w("    CASINO_LOOK_%s,%s" % (n.upper(), "" if i else "   // the art's order (casino_art.json), then the looks drawn as a star"))
    w("    CASINO_LOOK_COUNT,")
    w("    CASINO_LOOK_NONE = 0xFF")
    w("};")
    w("static const u8 sCasinoLookArt[CASINO_LOOK_COUNT] = {%s};" % ", ".join(str(a) for _, a in look_list))
    falls = sorted(set(FALL.values()) | {"TWINKLE"})
    w("enum { %s };" % ", ".join("CASINO_FALL_%s" % f for f in falls))
    w("static const u8 sCasinoLookFall[CASINO_LOOK_COUNT] = {%s};" % ", ".join(
        "CASINO_FALL_" + FALL.get(n, "TWINKLE") for n, _ in look_list))
    w("static const bool8 sCasinoLookRises[CASINO_LOOK_COUNT] = {%s};" % ", ".join(
        "TRUE" if n in RISES else "FALSE" for n, _ in look_list))
    w("#define CASINO_ART_COUNT %d" % len(art["pieces"]))
    w("#define CASINO_ART_COIN  %d" % art["pieces"].index("coin"))
    w("#define CASINO_ART_MARK  %d" % art["pieces"].index("mark"))
    w("// each piece's palette: 1 colourA, 2 colourB, 3 the day's -- filled in as the machine opens -- then its own")
    w("static const u16 sCasinoArtPals[CASINO_ART_COUNT][16] = {")
    for p in piece_pals:
        w("    {%s}," % ", ".join("0x%04X" % c for c in p))
    w("};")
    w("// the season's own colours (casino.cpp colourA / colourB), SEASON_* order")
    sc = art["season"]
    w("static const u32 sCasinoSeasonColours[SEASON_COUNT][2] = {%s};" % ", ".join(
        "[%s] = {0x%s, 0x%s}" % (k, sc[v][0][1:].upper(), sc[v][1][1:].upper()) for k, v in season.items()))
    w("static const u8 sCasinoSeasonLook[SEASON_COUNT] = {[SEASON_WINTER] = CASINO_LOOK_SNOW, [SEASON_SPRING] = CASINO_LOOK_PETALS, "
      "[SEASON_SUMMER] = CASINO_LOOK_SUN, [SEASON_AUTUMN] = CASINO_LOOK_LEAVES};")
    w("")
    w("// ---- the falling season: 8x8 tiles (graphics/slot_machine/daemons/bits.png) and their palette (1 A, 2 B)")
    names = list(tiles)
    w("enum { %s, CASINO_BIT_TILE_COUNT };" % ", ".join("CASINO_BIT_%s" % n for n in names))
    w("static const u16 sCasinoBitsPal[16] = {%s};" % ", ".join("0x%04X" % rgb15(c) for c in BITS_PAL))
    w("")
    w("// ---- the hats (casino.cpp hat()), half size: 0 clear, else a slot of sCasinoHatColours (0xFF000001 colourA,")
    w("// 0xFF000002 colourB, else 0xRRGGBB); (x, y) the point that sits on the head's top middle")
    w("enum { CASINO_HAT_NONE, %s, CASINO_HAT_COUNT };" % ", ".join("CASINO_HAT_%s" % n.upper() for n, *_ in hat_list))
    maxw = max(hw for _, _, hw, _, _, _ in hat_list)
    maxh = max(hh for _, _, _, hh, _, _ in hat_list)
    w("#define CASINO_HAT_W %d" % maxw)
    w("#define CASINO_HAT_H %d" % maxh)
    w("struct CasinoHat { u8 x, y; u32 colours[4]; u8 pix[CASINO_HAT_H][CASINO_HAT_W]; };")
    w("static const struct CasinoHat sCasinoHats[CASINO_HAT_COUNT] = {")
    for name, pix, hw, hh, ax, ay in hat_list:
        slots = []
        for v in pix.values():
            key = v if isinstance(v, int) else v[1]
            if key not in slots:
                slots.append(key)
        slots.sort(key=lambda k: (not isinstance(k, int) or k > 3, k))
        if len(slots) > 3:
            raise SystemExit("gencasino: hat %s has %d colours" % (name, len(slots)))
        cols = ["0xFF0000%02X" % k if (isinstance(k, int) and k <= 3 and k < 0x10) else "0x%06X" % k for k in slots]
        cols = ["0"] + cols + ["0"] * (3 - len(slots))
        grid = [[0] * maxw for _ in range(maxh)]
        for (x, y), v in pix.items():
            key = v if isinstance(v, int) else v[1]
            grid[y][x] = 1 + slots.index(key)
        w("    [CASINO_HAT_%s] = {%d, %d, {%s}, {" % (name.upper(), ax, ay, ", ".join(cols)))
        for row in grid:
            w("        {%s}," % ",".join(str(v) for v in row))
        w("    }},")
    w("};")
    w("")
    w("// ---- each holiday's dress (docs/holidays.json's \"companion\"): its look, its two colours (0: the season's), its hat,")
    w("// whether it is the lucky one, and whether it stands the daemons on their heads (casino.cpp drawPicture's flip,")
    w("// FOOLS' DAY); a QUIET day is left undressed (HF_QUIET), a flipped one has no hat")
    w("struct CasinoHoliday { u8 look, hat; bool8 lucky, flip; u32 a, b; };")
    for guard, ids in holidays.items():
        w("#%s defined(%s)" % ("if" if guard == "FIRERED" else "elif", guard))
        w("static const struct CasinoHoliday sCasinoHolidays[HOLIDAY_COUNT + 1] = {")
        for n in sorted(ids):
            h = ids[n]
            c = h.get("companion") or {}
            look = c.get("look")
            look_c = "CASINO_LOOK_%s" % look.upper() if look and look != "none" else "CASINO_LOOK_NONE"
            hat = c.get("hat")
            hat_c = "CASINO_HAT_%s" % hat.upper() if hat and hat != "none" and not c.get("flip") else "CASINO_HAT_NONE"
            cols = c.get("colours") or [None, None]
            lucky = "TRUE" if re.search(luck["lucky_re"], h["real"], re.I) else "FALSE"
            flip = "TRUE" if c.get("flip") else "FALSE"
            w("    [%2d] = {%s, %s, %s, %s, 0x%06X, 0x%06X},   // %s (%s)" % (
                n, look_c, hat_c, lucky, flip, colour(cols[0]) or 0, colour(cols[1]) or 0, h["name"], h["real"]))
        w("};")
    w("#endif")
    w("")
    w("// ---- the tunes (tunes.h TUNE_SLOTS_*): semitones over the day's note (127 a rest), and the frame each starts on")
    w("// (its ms at 60 a second, counted from the tune's start so the rounding never adds up); the last entry its end")
    w("struct CasinoNote { s8 semis; u8 frame; };")
    for name, notes in tune_list:
        t, rows = 0, []
        for s, ms in notes:
            rows.append("{%d, %d}" % (s, round(t * 60 / 1000)))
            t += ms
        rows.append("{127, %d}" % round(t * 60 / 1000))
        w("static const struct CasinoNote s%s[] = {%s};" % (
            "".join(p.capitalize() for p in name.split("_")), ", ".join(rows)))
    w("")
    w("#endif // GUARD_DATA_DAEMONS_CASINO_H")
    return "\n".join(L) + "\n"


def png_bytes(frames, pal, w, h):
    from PIL import Image
    import io
    im = Image.new("P", (w, h * len(frames)), 0)
    flat = []
    for c in pal:
        flat += [(c >> 16) & 255, (c >> 8) & 255, c & 255]
    flat += [0] * (768 - len(flat))
    im.putpalette(flat)
    px = im.load()
    for k, f in enumerate(frames):
        for y in range(h):
            for x in range(w):
                px[x, k * h + y] = f[y][x]
    b = io.BytesIO()
    im.save(b, "PNG", bits=4)
    return b.getvalue()


def main():
    write = "--write" in sys.argv
    comp = companion_root()
    if not comp:
        print("  no companion beside DAEMONS: the CASINO's tables are kept as they are")
        return 0
    e, problems = engine(comp)
    luck = luck_numbers(comp)
    tune_list = tunes(comp)
    art = json.load(open(os.path.join(comp, "server", "data", "casino_art.json")))
    look_list = looks(art)
    frames, pals = pieces(comp, art)
    hat_list = hats(comp, art)
    holidays = holiday_rows(luck)
    tiles = bit_tiles()
    problems += check(e)

    files = {OUT_H: header(e, luck, tune_list, art, look_list, hat_list, holidays, pals, tiles).encode(),
             os.path.join(OUT_DIR, "pieces.png"): png_bytes(frames, [0xFF00FF] + [0x808080] * 15, 32, 32),
             os.path.join(OUT_DIR, "bits.png"): png_bytes(list(tiles.values()), [0xFF00FF] + BITS_PAL[1:], 8, 8)}
    changes = []
    for p, data in files.items():
        old = open(p, "rb").read() if os.path.exists(p) else None
        if p.endswith(".png") and old is not None:
            from PIL import Image
            import io
            a, b = Image.open(io.BytesIO(old)), Image.open(io.BytesIO(data))
            if a.size == b.size and list(a.getdata()) == list(b.getdata()):
                continue
        if old != data:
            changes.append(os.path.relpath(p, ROOT))
            if write:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "wb").write(data)
    print("  the CASINO: %d results, %d pieces of art, %d looks, %d hats, %d tunes; return %.3f..%.3f by luck: %s" % (
        len(e["WEIGHTS"]), len(frames), len(look_list), len(hat_list), len(tune_list), e["RET_LOW"], e["RET_HIGH"],
        "unchanged" if not changes else ("written" if write else "would write")))
    for c in changes:
        print("    " + c)
    if problems:
        print("  THE GAME DOES NOT AGREE WITH THE COMPANION:")
        for p in problems[:20]:
            print("    " + p)
        return 1
    print("  held to the companion: the table for every return %d..%d, RETURN_AT for every luck, slots.h = slots.ts;"
          " 300000 pulls at luck 0 paid %.4f" % (
        round(e["PULL_LOW"] * 10000), round(e["PULL_HIGH"] * 10000), e["SIM"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

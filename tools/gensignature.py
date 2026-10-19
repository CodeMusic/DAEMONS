#!/usr/bin/env python3
"""Every routine signed: its own codeword, shown as code and played as music (T-392 P1; the user, 2026-10-18).

    python3 tools/gensignature.py                  # report: the checks, the pilot, and whether the table is current
    python3 tools/gensignature.py --write          # write engineGba/src/data/daemons_signatures.h
    python3 tools/gensignature.py --check          # the uniqueness rule only (exit 1 on a failure)
    python3 tools/gensignature.py --list [NAME..]  # one line per routine: word, figure, key, path, tempo, side
    python3 tools/gensignature.py --sheet OUT.png [NAME..]   # a review sheet: the word in its ink, path, figure
    python3 tools/gensignature.py --audio OUT.mp3 [NAME..]   # the figures, from the BUILT ROM's own harp and flute,
                                                             # each after its spoken name (needs `say` and ffmpeg)

WHAT A SIGNATURE IS (docs/private/plan-routine-animations-2026-10-18.md, section 2, as the user decided it):

  WORD    9 glyphs of 0 and 1: a fixed bijection of the routine's id, (id * 0x13B) mod 512 XOR 0x0A5, so it is
          unique by construction and neighbours (RAPPORT 216, PRESENT 217) do not differ by one bit.
  FIGURE  3 notes: the WORD's three octal digits as degrees 1-8 of a major scale. Its RHYTHM is the WORD: a 1
          plucks the next note of the figure, a 0 rests (a word with fewer than three 1s plucks its last 0s too).
  KEY     the TYPE's colour folded into a pitch by vision 7.2 (light's frequency into an octave, red 700nm = C);
          a purple, which has no wavelength, is B (7.3); the three achromatic types take REGISTER instead (7.4):
          CONTENT middle C, LEGACY an octave down, OPAQUE two. On a holiday the engine plays it in the month's note.
  INK     the type's colour (9.24 clause 3); LEGACY bleached as genanims draws it; the union routines the splash's own.
  PATH    from the family's verb (the plan's table); WAVE and the lane order from the WORD; TEMPO = 12 + 2 x the
          WORD's 1s (14-30 frames a glyph flies; the figure's step is a quarter of it).
  SIDE    BOTH kinds for every routine, its side's kind leading: bits on the CONTENT side (CONTENT LOGIC STRATUM
          LEGACY, 9.24 as amended 2026-10-08) and CORRUPT SWARM HARDENED; notes on the CONTEXT side (CONTEXT LATENT
          VECTOR ENTROPY) and FLOW SIGNAL GROWTH FROZEN EMERGENT OPAQUE (the plan's Q4 a, for the nine 10-08 left
          unsided -- DRAFT, listed for the user).

THE RULE IT FAILS ON (exit 1, so check_generators fails with it):
  - no two routines share both WORD and FIGURE;
  - two routines of the same TYPE differ by at least 3, counting each differing word bit, each differing figure
    note, a different path and a different tempo.

THE TABLE (src/data/daemons_signatures.h, generated, read by src/daemons_signature.c): one 12-byte row per move id
and the type inks.

THE GLYPHS (T-392 P2; the user, 2026-10-18: "outline every signature glyph with a dark edge so any colour reads on
any picture" -- MISREAD's magenta was lost on its own pink). --write also draws the battle's own glyph sheet,
graphics/battle_anims/sprites/daemons_glyphs.png: the splash's 0, 1 and note (tools/gbanotes.py draws the splash's
own, which stays as it is), each redrawn one pixel in from the tile's edge and ringed in index 1, the OUTLINE, on all
eight sides. Index 1 is TRUE BLACK in both palettes it is drawn in (vision 9.4a's outline, every picture of ours):
daemons_ink.pal (grey, shaded into the type's colour at the start of a routine -- black times any colour stays black)
and daemons_glyphs.pal (the splash's colours, for the seven union routines). The ink's greys are lifted so a 1 is the
type's own colour and a 0 a step under it, not the darker shades the 2026-10-08 sheet borrowed (DRAFT). APPROVED rows play in the release ROMs; the debug ROMs play every row. Approving routines is
adding them to APPROVED here and re-running --write -- the scripts are never touched (engine.md trap 32).
"""
import ast, colorsys, importlib.util, math, os, re, struct, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")
OUT = os.path.join(E, "src", "data", "daemons_signatures.h")

#  T-392 P1's pilot (the plan, section 3): the 7 union routines, the 20 whose release scripts are byte-identical in
#  pairs (the hardest case), and the 4 already filmed. Vanilla's constant names; the routine's own name beside it.
PILOT = {
    "FLUENCY": "FLUENCY", "STILLPOINT": "STILLPOINT", "RECONNECT": "RECONNECT", "PRAXIS": "PRAXIS",
    "MEDIAN": "MEDIAN", "PANORAMA": "PANORAMA", "HINDSIGHT": "HINDSIGHT",
    "HEADBUTT": "COLLIDE", "HORN_ATTACK": "INSERT", "PIN_MISSILE": "FANOUT", "CONSENSUS": "CONSENSUS",
    "LOW_KICK": "WEIGH", "ROCK_SMASH": "CRACK", "SEISMIC_TOSS": "EQUATE", "SKY_UPPERCUT": "ABSTRACT",
    "SLEEP_POWDER": "SATURATE", "SPORE": "PARK", "LIGHT_SCREEN": "STEELMAN", "REFLECT": "PARAPHRASE",
    "DIZZY_PUNCH": "RACE", "SECRET_POWER": "AMBIENT", "SHARPEN": "INLINE", "HOWL": "RALLY",
    "DESTINY_BOND": "ATOMIC", "GRUDGE": "ZOMBIE", "RETURN": "RAPPORT", "PRESENT": "PRESENT",
    "TACKLE": "WRITE", "EMBER": "JITTER", "WATER_GUN": "TRICKLE", "CONFUSION": "MISREAD",
}
#  Released by the user's word: the pilot (2026-10-18, T-392 "Build P1 ... a pilot of 31"), then P2 (the user,
#  2026-10-18: "roll out to ALL 363"), family by family as the plan's section 3 releases them -- each family named
#  here sets SIG_APPROVED on every routine of it. The order is the one P2 released them in: the chart's eight sided
#  families first (they carried the 2026-10-08 draft), then the other ten types, then the six status families.
APPROVED = set(PILOT)
APPROVED_FAMILIES = [
    "CONTENT", "LOGIC", "STRATUM", "LEGACY", "CONTEXT", "LATENT", "VECTOR", "ENTROPY",
    "FLOW", "SIGNAL", "GROWTH", "CORRUPT", "SWARM", "HARDENED", "FROZEN", "EMERGENT", "OPAQUE", "COPY",
    "RAISE", "LOWER", "HEAL", "AFFLICT", "PROTECT", "FIELD",
]

UNION = {"FLUENCY", "STILLPOINT", "RECONNECT", "PRAXIS", "MEDIAN", "PANORAMA", "HINDSIGHT"}

TYPE_NAME = {"NORMAL": "CONTENT", "FIGHTING": "LOGIC", "FLYING": "VECTOR", "POISON": "CORRUPT", "GROUND": "STRATUM",
             "ROCK": "LEGACY", "BUG": "SWARM", "GHOST": "LATENT", "STEEL": "HARDENED", "MYSTERY": "MYSTERY",
             "FIRE": "ENTROPY", "WATER": "FLOW", "GRASS": "GROWTH", "ELECTRIC": "SIGNAL", "PSYCHIC": "CONTEXT",
             "ICE": "FROZEN", "DRAGON": "EMERGENT", "DARK": "OPAQUE"}
TYPE_ORDER = ["NORMAL", "FIGHTING", "FLYING", "POISON", "GROUND", "ROCK", "BUG", "GHOST", "STEEL", "MYSTERY",
              "FIRE", "WATER", "GRASS", "ELECTRIC", "PSYCHIC", "ICE", "DRAGON", "DARK"]

BITS_SIDE = {"CONTENT", "LOGIC", "STRATUM", "LEGACY", "CORRUPT", "SWARM", "HARDENED", "MYSTERY"}
ACHROMATIC = {"CONTENT": 0, "LEGACY": -12, "OPAQUE": -24, "MYSTERY": 0}     # register, in semitones from middle C

#  The paths (include/constants/battle_anim.h DAEMONS_GLYPH_*) and the modifiers (SIG_MOD_*, daemons_signature.c).
PATHS = ["STREAM", "RISE", "FALL", "RING", "CONVERGE", "SWEEP", "RETURN", "HOLD", "STEP", "SCATTER"]
MODS = ["ARC", "FADE", "BACK", "FLIP", "SLOW", "FAST", "SELF", "ORBIT"]
#  The family's verb picks the path (the plan's MOTION table).
VERB = {
    "CONTENT": ("STREAM", []), "LOGIC": ("STEP", []), "FROZEN": ("HOLD", []), "OPAQUE": ("STREAM", ["FADE"]),
    "LATENT": ("RISE", []), "HARDENED": ("FALL", []), "EMERGENT": ("RING", []), "COPY": ("STREAM", ["BACK"]),
    "FLOW": ("STREAM", []), "ENTROPY": ("SCATTER", []), "SIGNAL": ("SWEEP", ["FAST"]), "GROWTH": ("RISE", ["SLOW"]),
    "VECTOR": ("STREAM", ["ARC"]), "STRATUM": ("FALL", []), "SWARM": ("CONVERGE", []),
    "CORRUPT": ("STREAM", ["FLIP"]), "CONTEXT": ("RING", ["ORBIT"]), "LEGACY": ("STREAM", ["SLOW"]),
    "RAISE": ("RISE", ["SELF"]), "HEAL": ("RISE", ["SELF"]), "LOWER": ("FALL", []), "AFFLICT": ("CONVERGE", []),
    "PROTECT": ("RING", ["SELF"]), "FIELD": ("SWEEP", []), "MYSTERY": ("STREAM", []),
}
FLAG_APPROVED, FLAG_OWN_SCRIPT, FLAG_UNION, FLAG_NOTES_LEAD = 1, 2, 4, 8
MAJOR8 = [0, 2, 4, 5, 7, 9, 11, 12]
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


# ---- the glyph sheet and its two palettes (P2: the outline) ----
GLYPH_ROWS = {
    "ZERO": ["........",
             "..###...",
             ".#...#..",
             ".#...#..",
             ".#...#..",
             "..###...",
             "........",
             "........"],
    "ONE":  ["........",
             "...##...",
             "..###...",
             "...##...",
             "...##...",
             "..####..",
             "........",
             "........"],
    "NOTE": ["........",
             "....##..",
             "....#.#.",
             "....#...",
             "..###...",
             "..###...",
             "........",
             "........"],
}
OUTLINE = 1
#  The four frames, in the splash sheet's order and on its indices (3 the 0, 4 the 1, 7 and 8 the note and the lit note).
GLYPH_FRAMES = [("ZERO", 3), ("ONE", 4), ("NOTE", 7), ("NOTE", 8)]
SPRITES = os.path.join(E, "graphics", "battle_anims", "sprites")
GLYPH_PNG = os.path.join(SPRITES, "daemons_glyphs.png")
GLYPH_PAL = os.path.join(SPRITES, "daemons_glyphs.pal")
INK_PAL = os.path.join(SPRITES, "daemons_ink.pal")
#  The ink: grey, each index shaded by its grey / 31 into the type's colour (daemons_signature.c). 1 the outline.
INK_GREYS = {1: 0, 3: 208, 4: 248, 7: 208, 8: 248}


def outlined(rows, ink):
    g = [[ink if c == "#" else 0 for c in r] for r in rows]
    out = [row[:] for row in g]
    for y in range(8):
        for x in range(8):
            if g[y][x]:
                continue
            if any(0 <= y + dy < 8 and 0 <= x + dx < 8 and g[y + dy][x + dx]
                   for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                out[y][x] = OUTLINE
    for y in range(8):
        for x in range(8):
            if g[y][x] and (x in (0, 7) or y in (0, 7)):
                raise SystemExit("a glyph touches its tile's edge: no room for the outline")
    return out


def splash_palette():
    tree = ast.parse(open(os.path.join(ROOT, "tools/gbanotes.py")).read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "PALETTE" for t in n.targets):
            pal = list(ast.literal_eval(n.value))
            pal[OUTLINE] = (0, 0, 0)          # the splash's own navy outline, made the true black every picture wears
            return pal
    raise SystemExit("gbanotes.py no longer defines PALETTE")


def ink_palette():
    pal = [(0, 0, 0)] + [(104, 104, 104)] * 15
    for i, g in INK_GREYS.items():
        pal[i] = (g, g, g)
    return pal


def jasc(pal):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal)


def glyph_image():
    from PIL import Image
    im = Image.new("P", (16, 16), 0)
    flat = []
    for c in splash_palette():
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for k, (shape, ink) in enumerate(GLYPH_FRAMES):
        g = outlined(GLYPH_ROWS[shape], ink)
        ox, oy = (k % 2) * 8, (k // 2) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = g[y][x]
    return im


def glyph_files():
    """{path: bytes} of the three files --write keeps current."""
    import io
    buf = io.BytesIO()
    glyph_image().save(buf, "PNG")
    return {GLYPH_PNG: buf.getvalue(), GLYPH_PAL: jasc(splash_palette()).encode(),
            INK_PAL: jasc(ink_palette()).encode()}


def png_pixels(data):
    from PIL import Image
    import io
    im = Image.open(io.BytesIO(data))
    return im.mode, im.size, list(im.getdata()), im.getpalette()[:48] if im.getpalette() else None


def glyph_stale():
    stale = []
    for path, data in glyph_files().items():
        if not os.path.exists(path):
            stale.append(path)
            continue
        cur = open(path, "rb").read()
        if path.endswith(".png"):
            if png_pixels(cur) != png_pixels(data):
                stale.append(path)
        elif cur.replace(b"\r\n", b"\n") != data.replace(b"\r\n", b"\n"):
            stale.append(path)
    return stale


# ---- how long a signature runs (daemons_signature.c's DaemonsSignature_Start, SIG_MODE_FULL) ----
def length_of(r):
    flight = r["tempo"] * 3 // 2 if "SLOW" in r["mods"] else r["tempo"] * 2 // 3 if "FAST" in r["mods"] else r["tempo"]
    notes_lead = r["flags"] & FLAG_NOTES_LEAD
    note_start, bit_start = (0, LAG) if notes_lead else (LAG, 0)
    last = max(k for k, b in enumerate(bits(r["rhythm"])) if b)
    last_pluck = note_start + last * note_step(r)
    end = max(last_pluck + flight, bit_start + 8 * 2 + flight, last_pluck + 10 + 5)
    return end + 2           # tEnd = end + 1, and the task is destroyed on the frame after it



def read(p):
    return open(os.path.join(E, p)).read()


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def type_colours():
    tree = ast.parse(open(os.path.join(ROOT, "tools/gbasprite.py")).read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "TYPE_COLOR" for t in n.targets):
            return ast.literal_eval(n.value)
    raise SystemExit("gbasprite.py no longer defines TYPE_COLOR")


def word_of(mid):
    return ((mid * 0x13B) % 512) ^ 0x0A5


def bits(w):
    return [(w >> (8 - i)) & 1 for i in range(9)]


def figure_of(w):
    return [(w >> 6) & 7, (w >> 3) & 7, w & 7]


def rhythm_of(w):
    r = bits(w)
    i = 8
    while sum(r) < 3:              # a word with fewer than three 1s plucks its last 0s, so the whole figure sounds
        if not r[i]:
            r[i] = 1
        i -= 1
    return sum(b << (8 - i) for i, b in enumerate(r))


#  7.2's fold: the hue's wavelength (piecewise between the spectral anchors), then 12 * log2(700 / nm) above C.
HUE_NM = [(0, 700), (30, 620), (60, 580), (90, 550), (120, 530), (180, 500), (225, 470), (270, 420)]


def key_of(rgb, tname):
    if tname in ACHROMATIC:
        return 0, ACHROMATIC[tname]
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb))
    h *= 360
    if h > 270:
        return 11, 0               # a purple has no wavelength: the invented colour, B (7.3)
    for (h0, n0), (h1, n1) in zip(HUE_NM, HUE_NM[1:]):
        if h0 <= h <= h1:
            nm = n0 + (n1 - n0) * (h - h0) / (h1 - h0)
            return int(round(12 * math.log2(700 / nm))) % 12, 0
    raise SystemExit("no wavelength for hue %.0f" % h)


def rgb555(rgb):
    return tuple(c >> 3 for c in rgb)


def bleach(c):
    return tuple(min(31, int(v + (31 - v) * 0.70)) for v in c)       # genanims.bleach, LEGACY worn pale


def routines():
    ids = {m: int(v) for m, v in re.findall(r"#define MOVE_(\w+)\s+(\d+)\b", read("include/constants/moves.h"))}
    names = dict(re.findall(r'\[MOVE_(\w+)\]\s*= _\("(.*?)"\)', read("src/data/text/move_names.h")))
    info = {}
    for mv, body in re.findall(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \}", read("src/data/battle_moves.h"), re.S):
        info[mv] = dict(effect=re.search(r"\.effect = (\w+)", body).group(1),
                        power=int(re.search(r"\.power = (\d+)", body).group(1)),
                        type=re.search(r"\.type = TYPE_(\w+)", body).group(1))
    census = _load("animcensus")
    colours = type_colours()
    rows = []
    for mv, mid in sorted(ids.items(), key=lambda x: x[1]):
        if mid == 0 or mv not in info or mv not in names:
            continue
        d = info[mv]
        tname = TYPE_NAME[d["type"]]
        fam = census.family(d["effect"], d["power"])
        if fam in (None, "OTHER"):
            fam = tname
        w = word_of(mid)
        path, mods = VERB[fam]
        rgb = colours.get(d["type"], (104, 104, 104))
        tonic, register = key_of(rgb, tname)
        ink = rgb555(rgb)
        if tname == "LEGACY":
            ink = bleach(ink)
        wave = (w >> 2) % 7
        if fam == "FLOW":
            wave += 6                                # FLOW: a big wave
        if path in ("FALL",) and fam == "HARDENED":
            wave = 0                                 # HARDENED: no give
        flags = 0
        if mv in APPROVED or fam in APPROVED_FAMILIES:
            flags |= FLAG_APPROVED
        if mv in UNION:
            flags |= FLAG_UNION | FLAG_OWN_SCRIPT
        if tname not in BITS_SIDE:
            flags |= FLAG_NOTES_LEAD
        rows.append(dict(id=mid, mv=mv, name=names[mv], type=d["type"], tname=tname, family=fam, word=w,
                         figure=figure_of(w), rhythm=rhythm_of(w), tonic=tonic, register=register, ink=ink,
                         path=path, mods=mods, wave=wave, tempo=12 + 2 * bin(w).count("1"), flags=flags))
    return rows


def distance(a, b):
    return (bin(a["word"] ^ b["word"]).count("1") + sum(x != y for x, y in zip(a["figure"], b["figure"]))
            + (a["path"] != b["path"]) + (a["tempo"] != b["tempo"]))


def check(rows):
    bad = []
    seen = {}
    for r in rows:
        k = (r["word"], tuple(r["figure"]))
        if k in seen:
            bad.append("%s and %s share a word and figure" % (seen[k]["name"], r["name"]))
        seen[k] = r
    worst = {}
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            if a["type"] != b["type"]:
                continue
            d = distance(a, b)
            if d < 3:
                bad.append("%s and %s (both %s) differ by only %d" % (a["name"], b["name"], a["tname"], d))
            worst[a["tname"]] = min(worst.get(a["tname"], 99), d)
    return bad, worst


def semis(r, k):
    return r["tonic"] + r["register"] + MAJOR8[r["figure"][k % 3]]


def describe(r):
    word = "".join(map(str, bits(r["word"])))
    rh = "".join("x" if b else "." for b in bits(r["rhythm"]))
    notes = " ".join(NOTE_NAMES[semis(r, k) % 12] for k in range(3))
    key = NOTE_NAMES[r["tonic"]] + ("" if not r["register"] else " %+d" % (r["register"] // 12))
    return "%3d %-11s %-8s %-8s %s %s  %-8s key %-5s %-9s%-12s wave %2d tempo %2d %s%s" % (
        r["id"], r["name"], r["tname"], r["family"], word, rh, notes, key, r["path"], "+".join(r["mods"]), r["wave"],
        r["tempo"], "notes first" if r["flags"] & FLAG_NOTES_LEAD else "bits first",
        "  APPROVED" if r["flags"] & FLAG_APPROVED else "")


def header(rows, colours):
    out = ["// GENERATED by tools/gensignature.py -- do not edit. T-392: every routine signed (its own codeword).",
           "// One row per routine: {word, rhythm, figure, tonic, path, mods, wave, tempo, flags}. The word's first glyph",
           "// is bit 8; the figure's three degrees (0-7 of a major scale and its octave) are bits 6-8, 3-5 and 0-2.",
           "// The release ROMs play a row only if it is SIG_APPROVED; the debug ROMs play every row.", "",
           "static const struct DaemonsSignature sDaemonsSignatures[MOVES_COUNT] =", "{"]
    for r in rows:
        fig = (r["figure"][0] << 6) | (r["figure"][1] << 3) | r["figure"][2]
        flags = [n for n, f in (("SIG_APPROVED", FLAG_APPROVED), ("SIG_OWN_SCRIPT", FLAG_OWN_SCRIPT),
                                ("SIG_UNION", FLAG_UNION), ("SIG_NOTES_LEAD", FLAG_NOTES_LEAD)) if r["flags"] & f]
        mods = " | ".join("SIG_MOD_" + m for m in r["mods"]) or "0"
        out.append("    [MOVE_%s] = {0x%03X, 0x%03X, 0%03o, %d, DAEMONS_GLYPH_%s, %s, %d, %d, %s},   // %s" % (
            r["mv"], r["word"], r["rhythm"], fig, r["tonic"] + r["register"], r["path"], mods, r["wave"], r["tempo"],
            " | ".join(flags) or "0", r["name"]))
    out += ["};", "", "// Each type's ink (vision 9.24 clause 3: gbasprite.py's TYPE_COLOR; LEGACY bleached as genanims draws it).",
            "static const u16 sDaemonsSignatureInk[NUMBER_OF_MON_TYPES] =", "{"]
    for t in TYPE_ORDER:
        rgb = rgb555(colours.get(t, (104, 104, 104)))
        if TYPE_NAME[t] == "LEGACY":
            rgb = bleach(rgb)
        out.append("    [TYPE_%s] = RGB(%d, %d, %d),   // %s" % (t, rgb[0], rgb[1], rgb[2], TYPE_NAME[t]))
    out += ["};", ""]
    return "\n".join(out)


def pick(rows, names):
    if not names:
        return [r for r in rows if r["mv"] in PILOT]
    if [n.upper() for n in names] == ["ALL"]:
        return rows
    want = {n.upper() for n in names}
    return [r for r in rows if r["name"] in want or r["mv"] in want]


# ---- --sheet: each routine's word in its ink, its path, its figure on a staff ----
def sheet(rows, path):
    from PIL import Image, ImageDraw
    W, H = 760, 34
    per = 92                                    # a long sheet (ALL) wraps into columns of 92
    cols = (len(rows) + per - 1) // per
    img = Image.new("RGB", (W * cols, 24 + H * min(per, len(rows))), (24, 24, 28))
    d = ImageDraw.Draw(img)
    d.text((8, 6), "T-392 signatures (DRAFT): word in the type's ink, rhythm, path, figure on a staff", fill=(220, 220, 220))
    for i, r in enumerate(rows):
        y = 24 + (i % per) * H
        ox = (i // per) * W
        ink = tuple(min(255, c * 8 + 4) for c in r["ink"]) if not r["flags"] & FLAG_UNION else (255, 214, 90)
        d.text((ox + 8, y + 10), "%3d %s" % (r["id"], r["name"]), fill=(230, 230, 230))
        for k, b in enumerate(bits(r["word"])):
            d.text((ox + 128 + k * 12, y + 4), str(b), fill=ink)
        for k, b in enumerate(bits(r["rhythm"])):
            d.text((ox + 128 + k * 12, y + 18), "x" if b else ".", fill=(150, 150, 160))
        d.text((ox + 250, y + 10), "%s %s" % (r["path"], "+".join(r["mods"])), fill=(200, 200, 210))
        # a staff: five lines, the three notes as dots on it (C4 on the first ledger below)
        x0 = ox + 400
        for ln in range(5):
            d.line((x0, y + 6 + ln * 5, x0 + 120, y + 6 + ln * 5), fill=(110, 110, 120))
        steps = [0, 1, 2, 3, 4, 5, 6, 7]
        for k in range(3):
            s = semis(r, k)
            octave, pc = divmod(s, 12)
            dia = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6][pc] + 7 * octave
            ny = y + 6 + 4 * 5 + 5 - dia * 2.5
            nx = x0 + 20 + k * 35
            d.ellipse((nx - 4, ny - 3, nx + 4, ny + 3), fill=ink)
        d.text((ox + 540, y + 10), "key %s%s  tempo %d  %s%s" % (
            NOTE_NAMES[r["tonic"]], "" if not r["register"] else " %+d oct" % (r["register"] // 12), r["tempo"],
            "notes first" if r["flags"] & FLAG_NOTES_LEAD else "bits first",
            "  APPROVED" if r["flags"] & FLAG_APPROVED else ""), fill=(200, 200, 210))
    img.save(path)
    print("  wrote", path)


# ---- --audio: the figures out of the BUILT ROM's own samples, timed as daemons_signature.c times them ----
RATE, SPF = 13379, 224
NAT_OF = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6]
NAT = [0, 2, 4, 5, 7, 9, 11]
SE_HARP_C, SE_FLUTE_C = 351, 359
LAG = 12                    # frames the follower kind waits (daemons_signature.c SIG_LAG)


def note_step(r):
    return max(3, r["tempo"] // 4)


def pluck_frames(r):
    """The frames a note is plucked on, as Task_DaemonsSignature schedules them."""
    start = 0 if r["flags"] & FLAG_NOTES_LEAD else LAG
    return [start + i * note_step(r) for i, b in enumerate(bits(r["rhythm"])) if b]


def audio(rows, out, edition):
    import numpy as np, wave
    rom_name = "daemonsContent.gba" if edition == "CONTENT" else "daemonsContext.gba"
    rom = open(os.path.join(E, rom_name), "rb").read()
    mp = read(rom_name.replace(".gba", ".map"))

    def sym(n):
        return int(re.search(r"0x([0-9a-f]+)\s+%s\n" % re.escape(n), mp).group(1), 16)

    def rd(a, n):
        return rom[a - 0x08000000: a - 0x08000000 + n]

    def u32(a):
        return struct.unpack("<I", rd(a, 4))[0]

    songs = sym("gSongTable")

    def voice(song):
        hdr = u32(songs + 8 * song)
        vg, track = u32(hdr + 4), u32(hdr + 8)
        t = rd(track, 64)
        v = t[t.index(0xBD) + 1]
        k = next(i for i in range(len(t)) if t[i] >= 0xCF)
        vb = rd(vg + 12 * v, 12)
        wav = struct.unpack("<I", vb[4:8])[0]
        flags, freq, ls, size = struct.unpack("<IIII", rd(wav, 16))
        return dict(key=t[k + 1], vel=t[k + 2], adsr=tuple(vb[8:12]), loop=bool(flags & 0x40000000), freq=freq / 1024,
                    ls=ls, size=size, pcm=np.frombuffer(rd(wav + 16, size + 1), np.int8).astype(np.float64))

    class Chan:
        def __init__(s, v, bend, vol):
            s.v, s.pos, s.env, s.phase, s.vol, s.on = v, 0.0, 0, "attack", vol, True
            s.step = v["freq"] * 2 ** ((v["key"] - 60 + bend) / 12) / RATE

        def tick(s):
            a, dd, su, rr = s.v["adsr"]
            if s.phase == "release":
                s.env = s.env * rr >> 8
                s.on = s.env > 0
            elif s.phase == "attack":
                s.env += a
                if s.env >= 255:
                    s.env, s.phase = 255, "decay"
            elif s.phase == "decay":
                s.env = s.env * dd >> 8
                if s.env <= su:
                    s.env, s.phase = su, "sustain"
                    s.on = su != 0

        def mix(s, n):
            o = np.zeros(n)
            if not s.on:
                return o
            v = s.v
            idx = s.pos + s.step * np.arange(n)
            if v["loop"]:
                L = v["size"] - v["ls"]
                idx = np.where(idx >= v["size"], v["ls"] + (idx - v["ls"]) % L, idx)
            else:
                alive = idx < v["size"]
                s.on = bool(alive.all())
                idx = idx[alive]
            i = idx.astype(int)
            f = idx - i
            smp = v["pcm"][i] + (v["pcm"][np.minimum(i + 1, len(v["pcm"]) - 1)] - v["pcm"][i]) * f
            o[:len(i)] = np.floor(smp * (s.env * s.vol >> 8) / 256)
            s.pos += s.step * n
            if v["loop"] and s.pos >= v["size"]:
                s.pos = v["ls"] + (s.pos - v["ls"]) % (v["size"] - v["ls"])
            return o

    def render(r):
        inst = "flute" if edition == "CONTEXT" else "harp"
        events = {}
        plucks = pluck_frames(r)
        for k, fr in enumerate(plucks):
            i = inst if not r["flags"] & FLAG_UNION else ("harp", "flute")[k & 1]
            events.setdefault(fr, []).append(("note", semis(r, k), i))
        last = plucks[-1]
        events.setdefault(last + 10, []).append(("stop",))
        cur, dying, out = None, [], []
        for fr in range(last + 70):
            for ev in events.get(fr, []):
                if cur:
                    if ev[0] == "note" and cur.inst == "harp":
                        cur.phase = "release"
                    elif ev[0] == "stop" and cur.inst == "harp":
                        continue                     # the harp rings out (only the flute is stopped)
                    else:
                        cur.phase = "release"
                    dying.append(cur)
                    cur = None
                if ev[0] == "note":
                    s = ev[1]
                    octave = s // 12
                    nat = NAT_OF[s - octave * 12]
                    v = voice((SE_FLUTE_C if ev[2] == "flute" else SE_HARP_C) + nat)
                    cur = Chan(v, s - NAT[nat], 0)
                    cur.inst = ev[2]
                    cur.vol = min(255, v["vel"] * (100 if ev[2] == "flute" else 110) // 127 * 2)
            buf = np.zeros(SPF)
            for c in ([cur] if cur else []) + dying:
                c.tick()
                buf += c.mix(SPF)
            dying = [c for c in dying if c.on]
            out.append(np.clip(buf, -128, 127))
        return np.concatenate(out) / 128.0

    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), "sig_audio_tmp")
    os.makedirs(tmp, exist_ok=True)
    parts = []
    gap = np.zeros(int(RATE * 0.5))
    for i, r in enumerate(rows):
        sp = os.path.join(tmp, "label%d" % i)
        notes = ", ".join(NOTE_NAMES[semis(r, k) % 12].replace("#", " sharp") for k in range(3))
        subprocess.run(["say", "-o", sp + ".aiff", "%s. %s, in %s. %s." % (r["name"].title(), r["tname"].title(),
                        NOTE_NAMES[r["tonic"]].replace("#", " sharp"), notes)], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", sp + ".aiff", "-ar", "44100", "-ac", "1", sp + ".wav"], check=True)
        x = np.concatenate([gap, render(r) * 0.9, gap])
        raw = os.path.join(tmp, "fig%d_13379.wav" % i)
        with wave.open(raw, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
            w.writeframes(np.int16(np.clip(x, -1, 1) * 30000).tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-ar", "44100", "-ac", "1",
                        os.path.join(tmp, "fig%d.wav" % i)], check=True)
        parts += [sp + ".wav", os.path.join(tmp, "fig%d.wav" % i)]
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join("file '%s'\n" % p for p in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-codec:a", "libmp3lame", "-q:a", "2", out], check=True)
    print("  wrote", out)


def main():
    args = sys.argv[1:]
    rows = routines()
    bad, worst = check(rows)
    colours = type_colours()
    if "--check" in args:
        for b in bad:
            print("  FAIL", b)
        print("  %d routines; %s" % (len(rows), "every one unique" if not bad else "%d failures" % len(bad)))
        return 1 if bad else 0
    if "--list" in args:
        names = [a for a in args if not a.startswith("--")]
        for r in (pick(rows, names) if names else rows):
            print(describe(r))
        return 0
    for flag in ("--sheet", "--audio"):
        if flag in args:
            i = args.index(flag)
            out = args[i + 1]
            names = [a for a in args[i + 2:] if not a.startswith("--")]
            chosen = pick(rows, names)
            if flag == "--sheet":
                sheet(chosen, out)
            else:
                audio(chosen, out, "CONTEXT" if "--context" in args else "CONTENT")
            return 0
    text = header(rows, colours)
    cur = open(OUT).read() if os.path.exists(OUT) else ""
    print("  %d routines signed; %d APPROVED for the release ROMs (the pilot and %d families)" % (
        len(rows), sum(r["flags"] & FLAG_APPROVED > 0 for r in rows), len(APPROVED_FAMILIES)))
    print("  the closest two routines of one type: " + ", ".join("%s %d" % (t, d) for t, d in sorted(worst.items())))
    for b in bad:
        print("  FAIL", b)
    longest = max(rows, key=length_of)
    print("  the longest signature: %s, %d frames (it may run 12 past its picture, no more)" % (longest["name"], length_of(longest)))
    stale = glyph_stale()
    if "--write" in args:
        if bad:
            raise SystemExit("  refused: the uniqueness rule fails")
        if text != cur:
            open(OUT, "w").write(text)
            print("  wrote", os.path.relpath(OUT, ROOT))
        else:
            print("  %s is current" % os.path.relpath(OUT, ROOT))
        for path, data in glyph_files().items():
            if path in stale:
                open(path, "wb").write(data)
                print("  wrote", os.path.relpath(path, ROOT))
        if not stale:
            print("  the glyph sheet and its palettes are current")
    else:
        print("  %s %s" % (os.path.relpath(OUT, ROOT), "is current" if text == cur else "would change (--write)"))
        for path in stale:
            print("  %s would change (--write)" % os.path.relpath(path, ROOT))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

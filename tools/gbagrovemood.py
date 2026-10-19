#!/usr/bin/env python3
"""T-408: each grove's universe in its own light -- the same trees and ground, recoloured to the universe's mood.

    python3 tools/gbagrovemood.py              # report: each universe's key colours, and how near each sits to a type
    python3 tools/gbagrovemood.py --write      # engineGba/src/data/grove_moods.h
    python3 tools/gbagrovemood.py --swatch OUT.png   # the key colours before and after, one row a universe

"The same trees and ground recoloured to each universe's mood" (the user, 2026-10-19). ALL DRAFT, for the user's eye.

WHAT CHANGES. Only the grove map's BACKGROUND palettes, as they load (fieldmap.c's DaemonsClarityEntries, the pass the
season and the faded print already take): rows 0..12, General's and the grove's secondary, and only while the player
stands on that grove's map -- never the parent route, which loads its own palettes on the way out. People, daemons and
the fir are sprites, so they keep their own colours and stand out of the mood; the dialogue frame (rows 13..15) is
never touched. The season goes first, the mood on it, then the faded print and the watch's light over both, so dusk
still falls in every universe. HALFTONE's grey outranks it and BREATHVERSE is not a grove (it stays timeless).

THE SHIFT, per channel in the GBA's 5-bit colour, the colour's own grey Y = (77r + 150g + 29b) / 256:
    v = Y + (v - Y) * sat            saturation (1 keeps it)
    v = v + (T*Y/Ty - v) * amount    toward the mood's colour T AT THIS COLOUR'S OWN LIGHTNESS, so a dark outline stays
                                     dark and a light path light -- the paths and the lone tree keep their contrast
    v = 16 + (v - 16) * contrast + lift
The C does exactly this in integers; this file does it the same way (truncating division) to report what the screen
shows.

THE TYPE RULE (vision.md 9.4). A mood is the PLACE's, never a type's, so a grove must not read as one type's colour
block. Measured as gbadaytrim/genguide measure it (CIE76 on the 5-bit colour): every key colour's nearest type, and a
FLAG where a mood brings a key colour inside 22 of a type its unshifted colour was not already that near (a near-grey,
max - min under 24, is nobody's type, as genguide.check_palette rules). Vanilla's
grass already sits 17 from GRASS's hue and its bark 12 from GROUND's; that is the route's, and is not counted against a
mood. Most muted colours sit within 22 of NORMAL, ROCK, STEEL or GROUND, so those are LISTED for the user's eye; what
the tool REFUSES is a grove that reads as one type's block -- its leaf and its grass, the two colours that fill the
clearing, both within BLOCK of the same type.
"""
import importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(GBA, "src/data/grove_moods.h")
WRITE = "--write" in sys.argv
MARGIN = 22
BLOCK = 14


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    m = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, sys.argv[:1]
    try:
        spec.loader.exec_module(m)
    finally:
        sys.argv = argv
    return m


#  universe -> (the mood in words, T as 8-bit RGB, amount, sat, contrast, lift in 5-bit steps). DRAFT, 2026-10-19,
#  each read from its universe's name and its NEXUS sign (tools/gbanexusmap.py UNIVERSES).
MOODS = {
    "BACKDROP": ("a painted set: flat, low contrast, a warm cream wash",  (232, 214, 172), 0.40, 0.75, 0.70, 1),
    "PULSE":    ("vivid: saturated, hard contrast, pushed toward lime",    (230, 240, 60),  0.25, 1.70, 1.20, 0),
    "INWARD":   ("candle-warm: amber-orange light in a dim room",         (255, 136, 96),  0.72, 0.70, 1.10, -4),
    "EMPATH":   ("rose",                                                  (232, 130, 160), 0.62, 0.90, 1.00, 0),
    "DRIFT":    ("dusky lavender",                                        (176, 136, 220), 0.75, 0.95, 0.95, 0),
    "HAZE":     ("soft fog: pale, grey, low contrast",                    (214, 216, 224), 0.45, 0.50, 0.70, 2),
    "HUSH":     ("muted blue-grey, soft",                                 (124, 144, 176), 0.60, 0.45, 0.84, 1),
    "SEED":     ("fresh spring green: pale, light and new",               (170, 236, 150), 0.40, 0.90, 0.88, 2),
    "WEATHER":  ("storm-slate: dark, cool, heavy",                        (90, 110, 140),  0.62, 0.60, 1.14, -4),
    "HUNGER":   ("warm red-amber, saturated",                             (232, 96, 60),   0.66, 1.10, 1.04, 0),
    "HUSK":     ("dry straw",                                             (220, 192, 118), 0.62, 0.60, 0.95, 0),
    "MECHA":    ("cool steel: hard-edged, blue-white",                    (140, 160, 200), 0.66, 0.30, 1.18, 0),
    "COMPASS":  ("north-blue",                                            (86, 138, 220),  0.60, 0.90, 1.00, 0),
    "CLAY":     ("terracotta: earthy, a little dull",                     (220, 96, 80),   0.70, 0.80, 1.00, 0),
}

#  The colours that make a grove read: (General palette row, index, what it draws).
KEYS = [(0, 2, "leaf"), (0, 4, "leaf shade"), (0, 13, "grass"), (0, 5, "bark"), (3, 8, "path")]


def five(c):
    return tuple(v >> 3 for v in c)


def tdiv(a, b):
    """C's integer division (toward zero)."""
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def grey5(r, g, b):
    return (r * 77 + g * 150 + b * 29) >> 8


def params(u):
    _, t, amount, sat, contrast, lift = MOODS[u]
    t5 = five(t)
    return dict(t=t5, ty=max(1, grey5(*t5)), amount=round(amount * 256), sat=round(sat * 256),
                contrast=round(contrast * 256), lift=lift)


def shift5(c, p):
    """One 5-bit colour through the mood, as fieldmap.c's DaemonsGroveColour does it."""
    y = grey5(*c)
    out = []
    for v, t in zip(c, p["t"]):
        v = y + tdiv((v - y) * p["sat"], 256)
        tt = min(31, tdiv(t * y, p["ty"]))
        v = v + tdiv((tt - v) * p["amount"], 256)
        v = 16 + tdiv((v - 16) * p["contrast"], 256) + p["lift"]
        out.append(max(0, min(31, v)))
    return tuple(out)


def eight(c5):
    return tuple(v << 3 for v in c5)


def general_palette(row):
    lines = open(os.path.join(GBA, "data/tilesets/primary/general/palettes/%02d.pal" % row)).read().split("\n")[3:19]
    return [tuple(int(x) for x in l.split()) for l in lines]


def groves():
    """universe -> (grove map name, its MAP_ constant), in gbanexusmap's UNIVERSES order."""
    nexus, grove = _load("gbanexusmap"), _load("gbagrove")
    rows = {g["name"]: g for g in grove.GROVES}
    out = {}
    for name, (title, _) in nexus.UNIVERSES.items():
        u = title.replace("THE ", "").replace("VERSE", "")
        out[u] = (name, grove.map_const(rows[name]))
    return out


def nearest(c, hues, G):
    return min((sum((a - b) ** 2 for a, b in zip(G.lab(c), G.lab(v))) ** .5, k) for k, v in hues.items())


def report():
    G = _load("genguide")
    hues = G.type_hues()
    pals = {r: general_palette(r) for r in {k[0] for k in KEYS}}
    flags, rows, blocks = [], [], []
    for u, (name, mapc) in groves().items():
        p = params(u)
        cells = []
        for row, idx, what in KEYS:
            base = five(pals[row][idx])
            new = eight(shift5(base, p))
            d0, t0 = nearest(eight(base), hues, G)
            d1, t1 = nearest(new, hues, G)
            cells.append((what, new, d1, t1))
            neutral = max(new) - min(new) < 24          # genguide's rule: a grey is nobody's type
            if d1 < MARGIN and not neutral and not (t1 == t0 and d0 < MARGIN):
                flags.append("%s's %s rgb%s is %.1f from %s" % (u, what, new, d1, t1))
        near = {c[0]: c for c in cells}
        if near["leaf"][3] == near["grass"][3] and max(near["leaf"][2], near["grass"][2]) < BLOCK:
            blocks.append("%s reads as %s: leaf %.1f, grass %.1f" % (u, near["leaf"][3], near["leaf"][2],
                                                                      near["grass"][2]))
        rows.append((u, name, mapc, cells))
        print("  %-9s %-30s %s" % (u, name, MOODS[u][0]))
        print("            " + "  ".join("%s %s %.0f/%s" % (w, "#%02X%02X%02X" % c, d, t) for w, c, d, t in cells))
    print("  type check (%d+ from a type a key colour was not already near): %s"
          % (MARGIN, "clear" if not flags else "%d too close" % len(flags)))
    for f in flags:
        print("    " + f)
    print("  type blocks (leaf and grass both within %d of one type): %s" % (BLOCK, "none" if not blocks else len(blocks)))
    for b in blocks:
        print("    " + b)
    if blocks:
        raise SystemExit("  refused: a grove reads as a type's colour block")
    return rows


def header():
    lines = ["//  Generated by tools/gbagrovemood.py -- edit the tool, not this file. T-408 (the user, 2026-10-19): each",
             "//  grove's universe in its own light, its map's BG palettes shifted as they load (fieldmap.c). DRAFT.",
             "//  Per channel, 5-bit: v = Y + (v-Y)*sat; v += (T*Y/Ty - v)*amount; v = 16 + (v-16)*contrast + lift.",
             "",
             "struct DaemonsGroveMood",
             "{",
             "    u16 map;            // MAP_ constant: num | group << 8",
             "    u8 target[3];       // T, 5-bit",
             "    u8 targetGrey;      // Ty, never 0",
             "    u16 amount, sat, contrast;   // of 256",
             "    s8 lift;",
             "};",
             "",
             "static const struct DaemonsGroveMood sGroveMoods[] =",
             "{"]
    for u, (name, mapc) in groves().items():
        p = params(u)
        lines.append("    { %-36s { %2d, %2d, %2d }, %2d, %3d, %3d, %3d, %2d },   // %s: %s"
                     % (mapc + ",", p["t"][0], p["t"][1], p["t"][2], p["ty"], p["amount"], p["sat"], p["contrast"],
                        p["lift"], u, MOODS[u][0]))
    return "\n".join(lines + ["};", ""])


def swatch(path, rows):
    from PIL import Image, ImageDraw
    G = _load("genguide")
    pals = {r: general_palette(r) for r in {k[0] for k in KEYS}}
    cw, ch, lw = 36, 24, 90
    img = Image.new("RGB", (lw + cw * len(KEYS) * 2 + 12, ch * (len(rows) + 1)), (24, 24, 28))
    d = ImageDraw.Draw(img)
    d.text((4, 6), "before / after", fill=(220, 220, 220))
    for i, (u, _, _, cells) in enumerate(rows):
        y = ch * (i + 1)
        d.text((4, y + 6), u, fill=(220, 220, 220))
        for k, ((row, idx, _), (_, new, _, _)) in enumerate(zip(KEYS, cells)):
            x = lw + k * (cw * 2 + 2)
            d.rectangle([x, y + 2, x + cw - 1, y + ch - 3], fill=eight(five(pals[row][idx])))
            d.rectangle([x + cw, y + 2, x + 2 * cw - 1, y + ch - 3], fill=new)
    img.save(path)
    print("  swatch: %s" % path)


def main():
    rows = report()
    if "--swatch" in sys.argv:
        swatch(sys.argv[sys.argv.index("--swatch") + 1], rows)
    text = header()
    old = open(OUT).read() if os.path.exists(OUT) else None
    if old == text:
        print("  grove_moods.h already written")
    elif WRITE:
        open(OUT, "w").write(text)
        print("  written")
    else:
        print("  grove_moods.h to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())

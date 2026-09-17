#!/usr/bin/env python3
"""The streaks' data: each type's streak colour, and which species can wear streaks (T-132; 9.4).

    python3 tools/genstreaks.py            # report
    python3 tools/genstreaks.py --write    # src/data/pokemon/streaks.h

9.4 (amended 2026-09-17, v11.209): a daemon's palette indices 11-14 are its four STREAKS, one per move
slot, each the type of the move it knows. The engine writes them at runtime (src/daemon_streaks.c); this
writes the two tables it reads.

  gStreakColours[BODY][MOVE]           the streak a MOVE type draws on a BODY type. Its LIGHT step -- unless
                                       that sits within 9.4's separability floor (CIE76 20) of ANY of the body's
                                       three light tones (highlight, light, mid), and then whichever of its
                                       light and DARK steps stands furthest from the nearest of them. The
                                       choice is made here, in real CIE76, so no colour maths runs in the ROM.

    MEASURED AGAINST THREE TONES, NOT ONE, AND THE FIRST VERSION IS WHY. It compared a streak with the body's
    MID tone only, and a body is mostly its light tones -- NIBBLE's cleaned draft sits almost entirely on
    highlight and light. Worse, a streak in the body's OWN type at the light step IS the body's light tone,
    distance 0.0, which a mid-only test cannot see: FLYING on FLYING passed at 26 against mid and was invisible
    on the body. The mid-only rule darkened 22 pairs; measured against the three tones, 104 need it.
                                       NOT typed here either: the colour and the ramp
                                       both live in gbasprite.py, and a second copy is how a streak and a
                                       body of the same type would come to disagree. The TYPE_COLOR table
                                       and the ramp5() function are lifted out of that file's syntax tree
                                       and run in isolation -- gbasprite.py has no main guard, so importing
                                       it would run the whole sprite build (engine.md trap 16).
  gSpeciesHasStreaks[NUM_SPECIES]      TRUE only for a species whose streaks the BUILD put there. This is the
                                       safety rail, not a convenience: a vanilla palette uses all sixteen
                                       colours, so writing 11-14 into a species still on vanilla art would
                                       repaint it.

THE FIRST VERSION OF THE RAIL WAS THE HAZARD IT WAS BUILT AGAINST. It flagged any species whose front sprite
drew with indices 11-14 -- and reported 346, because vanilla sprites use 11-14 as ordinary colours. Written,
it would have repainted every vanilla daemon in battle. It ran in report mode first and the number was
absurd, which is the only reason that is a paragraph and not a bug.

So the flag needs a mark only this project's build leaves: `gbasprite.py` writes the BLANK grey into ALL
FOUR of 11-14, and only for art that carries streak markers. A species has streaks when its built
normal.pal holds BLANK at 11, 12, 13 and 14 AND its front sprite draws with at least one of them. A
vanilla palette does not hold one exact grey four times over, and the check asserts that none does.

TYPE_MYSTERY has no colour and takes the blank grey, as an empty move slot would not -- an empty slot
disappears into the body, and that is the engine's job, not a table's.
"""
import ast, glob, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
OUT = os.path.join(GBA, "src/data/pokemon/streaks.h")
STREAKS = range(11, 15)
FLOOR = 20.0                       # 9.4: under ~20 in CIE76 two colours are not separable at sprite size


def from_gbasprite():
    """TYPE_COLOR and ramp5, executed on their own"""
    tree = ast.parse(open(os.path.join(ROOT, "tools/gbasprite.py")).read())
    want = {"TYPE_COLOR", "STREAK_BLANK", "STREAK_FIRST"}
    keep = [n for n in tree.body if (isinstance(n, ast.Assign) and any(getattr(t, "id", "") in want for t in n.targets))
            or (isinstance(n, ast.FunctionDef) and n.name == "ramp5")]
    assert len(keep) == 4, "gbasprite.py no longer defines TYPE_COLOR, STREAK_BLANK, STREAK_FIRST and ramp5 at top level"
    ns = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), "gbasprite.py", "exec"), ns)
    assert ns["STREAK_FIRST"] == STREAKS.start, "gbasprite.py puts the streaks at %d, this file at %d" % (ns["STREAK_FIRST"], STREAKS.start)
    return ns["TYPE_COLOR"], ns["ramp5"], ns["STREAK_BLANK"]


def types():
    src = open(os.path.join(GBA, "include/constants/pokemon.h")).read()
    return {n: int(v) for n, v in re.findall(r"#define TYPE_(\w+)\s+(\d+)\s*$", src, re.M) if n != "NONE"}


def lab(c):
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(v) for v in c)
    x, y, z = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047, r * 0.2126 + g * 0.7152 + b * 0.0722, (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def cie76(a, b):
    return sum((p - q) ** 2 for p, q in zip(lab(a), lab(b))) ** 0.5


def rgb555(c):
    return "RGB(%d, %d, %d)" % tuple(v >> 3 for v in c)


def species_dirs():
    """SPECIES_X -> graphics/pokemon/<dir>, through the engine's own front-pic tables"""
    table = dict(re.findall(r"SPECIES_SPRITE\((\w+),\s*(gMonFrontPic_\w+)\)",
                            open(os.path.join(GBA, "src/data/pokemon_graphics/front_pic_table.h")).read()))
    inc = dict(re.findall(r"const u32 (gMonFrontPic_\w+)\[\] = INCBIN_U32\(\"graphics/pokemon/([\w/]+)/front\.4bpp\.lz\"\)",
                          open(os.path.join(GBA, "src/data/graphics/pokemon.h")).read()))
    return {"SPECIES_" + sp: inc[sym] for sp, sym in table.items() if sym in inc}


def read_pal(path):
    L = open(path).read().replace("\r", "").split("\n")
    return [tuple(map(int, l.split())) for l in L[3:3 + int(L[2])]]


def streaked(d):
    base = os.path.join(GBA, "graphics/pokemon", d)
    png, pal = os.path.join(base, "front.png"), os.path.join(base, "normal.pal")
    if not (os.path.exists(png) and os.path.exists(pal)):
        return False
    colours = read_pal(pal)
    if len(colours) < 15 or any(colours[i] != BLANK for i in STREAKS):
        return False                       # the build's mark is missing: this is not our streak palette
    im = Image.open(png)
    return im.mode == "P" and any(v in STREAKS for v in set(im.getdata()))


def main():
    global BLANK
    colours, ramp5, BLANK = from_gbasprite()
    tys = types()
    ramps = {name: (ramp5(*colours[name]) if name in colours else None) for name in tys}
    missing = [n for n in tys if n not in colours and n != "MYSTERY"]
    assert not missing, "types with no colour in gbasprite.py: %s" % missing
    order = sorted(tys.items(), key=lambda kv: kv[1])
    table, darkened, tight = {}, [], []
    for body, _ in order:
        tones = ramps[body][0:3] if ramps[body] else [BLANK]
        near = lambda c: min(cie76(c, t) for t in tones)          # distance to the body tone it is closest to
        for move, _ in order:
            if not ramps[move]:
                table[body, move] = BLANK
                continue
            light, dark = ramps[move][1], ramps[move][3]
            pick = light
            if near(light) < FLOOR:
                pick = max((light, dark), key=near)
                darkened.append((body, move, near(light), near(pick)))
            if near(pick) < FLOOR:
                tight.append((body, move, near(pick)))
            table[body, move] = pick
    dirs = species_dirs()
    have = sorted(sp for sp, d in dirs.items() if streaked(d))
    print("  %d types (%d coloured, MYSTERY blank); scanned %d species' built sprites, %d carry the build's streak mark"
          % (len(order), len(order) - 1, len(dirs), len(have)))
    print("  %d of %d body/move pairs take the DARK step: at the light step they are under CIE76 %.0f from one of the body's light tones"
          % (len(darkened), len(order) * len(order), FLOOR))
    if tight:
        print("  still under the floor with either step (%d):" % len(tight))
        for body, move, d in tight:
            print("     %-9s on %-9s %4.1f" % (move, body, d))
    for sp in have:
        print("     streaks: %s" % sp)
    text = ("// GENERATED by tools/genstreaks.py -- edit gbasprite.py's TYPE_COLOR or the art, then re-run. (9.4, T-132)\n"
            "// [body type][move type]: the move type's LIGHT step, or its DARK step where the light one would vanish\n"
            "// into a body of that type (CIE76 under %.0f from any of its highlight, light and mid tones).\n\n" % FLOOR +
            "const u16 gStreakColours[NUMBER_OF_MON_TYPES][NUMBER_OF_MON_TYPES] =\n{\n" +
            "".join("    [TYPE_%s] = {%s},\n" % (body, ", ".join("[TYPE_%s] = %s" % (move, rgb555(table[body, move])) for move, _ in order))
                    for body, _ in order) +
            "};\n\nconst u16 gStreakBlank = %s;\n\n" % rgb555(BLANK) +
            "// A species wears streaks only if the BUILD marked its palette: the one blank grey in all four of 11-14,\n"
            "// on a sprite that draws with them. A vanilla palette uses all sixteen colours, so writing 11-14 into any\n"
            "// other species would repaint it. SPECIES_NONE is listed so the initializer is never empty (C89).\n"
            "const bool8 gSpeciesHasStreaks[NUM_SPECIES] =\n{\n    [SPECIES_NONE] = FALSE,\n" +
            "".join("    [%s] = TRUE,\n" % sp for sp in have) + "};\n")
    if WRITE:
        old = open(OUT).read() if os.path.exists(OUT) else None
        if old != text:
            open(OUT, "w").write(text)
        print("  %s %s" % ("wrote" if old != text else "unchanged:", os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The PLUGIN discs, coloured by OUR chart (T-211; vision.md 9.4).

    python3 tools/genplugincolours.py            # report every type's ramp, old against new
    python3 tools/genplugincolours.py --write     # rewrite the sixteen icon palettes

WHAT WAS WRONG. Every PLUGIN and DRIVER shares one disc drawing (`gItemIcon_TMHM`) and is told apart by a
PER-TYPE PALETTE -- so the TOOLKIT is, quietly, the one screen in the game that teaches colour-to-type by
showing eighteen of them in a list. It was teaching VANILLA'S chart: our VECTOR is red and its disc was pale
blue, our LOGIC is steel blue and its disc was orange, our OPAQUE is near-black and its disc was pale cyan.

A player building the intuition 9.4 claims they can build would have built the wrong one, from our own
screen, using our own names. That is worse than not teaching it.

WHERE THE COLOURS COME FROM. tools/gbasprite.py's TYPE_COLOR, read at run time rather than copied -- the
same table that ramps every daemon's body, so a disc and the daemons it teaches cannot disagree.

THE STRUCTURE IS VANILLA'S AND IS KEPT. Entries 3-9 are the type's own seven-step ramp, lightest first;
0-2 and 10-15 are the disc's shared shading and are not touched. Vanilla's lightest step is about three
parts white to one of the hue and its darkest is the hue at full saturation, so that is the shape rebuilt.
"""
import ast, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PALDIR = os.path.join(ROOT, "engineGba/graphics/items/icon_palettes")
WRITE = "--write" in sys.argv
FIRST, LAST = 3, 9            # the type's own entries; the rest of the palette is the disc

FILES = {"dark": "DARK", "dragon": "DRAGON", "electric": "ELECTRIC", "fighting": "FIGHTING",
         "fire": "FIRE", "flying": "FLYING", "ghost": "GHOST", "grass": "GRASS", "ground": "GROUND",
         "ice": "ICE", "normal": "NORMAL", "poison": "POISON", "psychic": "PSYCHIC", "rock": "ROCK",
         "steel": "STEEL", "water": "WATER"}


def type_colours():
    src = open(os.path.join(ROOT, "tools/gbasprite.py"), encoding="utf-8").read()
    body = re.search(r'TYPE_COLOR = \{(.*?)\n\}', src, re.S).group(1)
    return {m.group(1): tuple(int(x) for x in m.groups()[1:])
            for m in re.finditer(r'"(\w+)":\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\)', body)}


def ramp(rgb):
    """seven steps, lightest first: a pale tint down through the hue to a shade of it"""
    out = []
    for i in range(LAST - FIRST + 1):
        t = 0.74 - i * (0.74 + 0.16) / (LAST - FIRST)      # +0.74 white .. -0.16 black
        if t >= 0:
            out.append(tuple(min(255, int(c + (255 - c) * t)) for c in rgb))
        else:
            out.append(tuple(max(0, int(c * (1 + t))) for c in rgb))
    return out


def main():
    colours = type_colours()
    n = 0
    for stem, t in sorted(FILES.items()):
        p = os.path.join(PALDIR, "%s_tm_hm.pal" % stem)
        if not os.path.exists(p) or t not in colours:
            print("  %-9s SKIPPED (no palette or no colour)" % t)
            continue
        raw = open(p, encoding="utf-8", newline="").read()
        eol = "\r\n" if "\r\n" in raw else "\n"       # the repo checks these out CRLF; keep whatever is there
        lines = raw.splitlines()
        head, rows = lines[:3], [l for l in lines[3:] if l.strip()]
        was = rows[FIRST]
        new = ramp(colours[t])
        for i, c in enumerate(new):
            rows[FIRST + i] = "%d %d %d" % c
        print("  %-9s %-14s  %s -> %s" % (t, str(colours[t]), was, rows[FIRST]))
        n += 1
        if WRITE:
            open(p, "w", encoding="utf-8", newline="").write(eol.join(head + rows) + eol)
    print("\n  %d palettes%s" % (n, " rewritten" if WRITE else " (report only; pass --write)"))


if __name__ == "__main__":
    main()

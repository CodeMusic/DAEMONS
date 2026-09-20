#!/usr/bin/env python3
"""The mark in every Index entry, one per TYPE (T-175; vision.md 4.2, 2.2).

    python3 tools/genfootprints.py            # preview the eighteen marks to /tmp/footprints.png
    python3 tools/genfootprints.py --write    # write every species' footprint.png from its primary type

WHAT THIS REPLACES. Gen 3 prints a 16x16 one-bit FOOTPRINT between HT and WT on every Index entry, and all 386 of
ours were still vanilla's paw prints -- spotted in play as "some symbol or ink smudge". A paw is a BODY, on the one
screen in the game whose every other line is a process, and it is the only place the fable's own rule was broken.

WHY A TYPE MARK RATHER THAN A SILHOUETTE. The entry page shows species, category, height and weight and never says
the daemon's TYPE, so this slot can carry the one thing the page lacks -- and the chart is the argument (invariant
3). A silhouette would be the alternative; at sixteen pixels in ONE BIT it is mush, and it would say nothing the
picture beside it does not already say.

EACH MARK IS THE TYPE'S OWN CLAUSE from 2.2, drawn flat:

    CONTENT  a filled token          LOGIC    a turnstile, which is what proves
    VECTOR   an arrow                CORRUPT  a blot, spreading
    STRATUM  layers                  LEGACY   a cairn
    SWARM    many, apart             LATENT   a dashed box: present, unseen
    HARDENED a plate                 ORACLE   a closed box that answers
    ENTROPY  a rising jag            FLOW     a gradient, descending
    GROWTH   a sprout                SIGNAL   a carrier
    CONTEXT  two brackets, framing   FROZEN   a crystal
    EMERGENT a spiral                OPAQUE   filled solid: nothing gets out

ONE BIT: 0 is ink and 255 is paper, and the file is mode "1" at 16x16 -- the build turns it into .1bpp.
"""
import os, re, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")
PREVIEW = "/tmp/footprints.png"
WRITE = "--write" in sys.argv
INK, PAPER = 0, 255


def mark(kind):
    im = Image.new("1", (16, 16), PAPER)
    d = ImageDraw.Draw(im)
    if kind == "NORMAL":                                   # a token: one thing, whole
        d.rectangle([5, 5, 10, 10], fill=INK)
    elif kind == "FIGHTING":                               # a turnstile: what proves
        d.line([(4, 3), (4, 12)], fill=INK); d.line([(4, 7), (12, 7)], fill=INK)
        d.line([(4, 5), (9, 5)], fill=INK)
    elif kind == "FLYING":                                 # a direction
        d.line([(3, 8), (12, 8)], fill=INK); d.line([(8, 4), (12, 8)], fill=INK); d.line([(8, 12), (12, 8)], fill=INK)
    elif kind == "POISON":                                 # a blot, spreading
        d.ellipse([5, 5, 10, 10], fill=INK)
        for p in ((3, 4), (12, 5), (4, 12), (11, 11), (8, 2), (2, 9)):
            d.point(p, fill=INK)
    elif kind == "GROUND":                                 # layers, laid down
        for y in (5, 8, 11):
            d.line([(3, y), (12, y)], fill=INK)
    elif kind == "ROCK":                                   # a cairn
        d.rectangle([4, 10, 11, 12], fill=INK); d.rectangle([5, 7, 10, 9], fill=INK); d.rectangle([6, 4, 9, 6], fill=INK)
    elif kind == "BUG":                                    # many, apart
        for p in ((4, 4), (11, 4), (7, 8), (4, 12), (11, 12)):
            d.rectangle([p[0] - 1, p[1] - 1, p[0] + 1, p[1] + 1], fill=INK)
    elif kind == "GHOST":                                  # present, unseen: a box drawn dashed
        for x in range(3, 13, 3):
            d.line([(x, 3), (x + 1, 3)], fill=INK); d.line([(x, 12), (x + 1, 12)], fill=INK)
        for y in range(3, 13, 3):
            d.line([(3, y), (3, y + 1)], fill=INK); d.line([(12, y), (12, y + 1)], fill=INK)
    elif kind == "STEEL":                                  # a plate
        d.rectangle([3, 5, 12, 10], fill=INK)
        d.rectangle([5, 7, 10, 8], fill=PAPER)
    elif kind == "MYSTERY":                                # a closed box that answers
        d.rectangle([3, 4, 12, 11], outline=INK)
        d.line([(6, 8), (9, 8)], fill=INK)
    elif kind == "FIRE":                                   # a rising jag
        d.line([(4, 12), (7, 6)], fill=INK); d.line([(7, 6), (9, 9)], fill=INK); d.line([(9, 9), (12, 3)], fill=INK)
    elif kind == "WATER":                                  # a gradient, descending
        d.line([(3, 5), (12, 5)], fill=INK); d.line([(4, 8), (11, 8)], fill=INK); d.line([(6, 11), (9, 11)], fill=INK)
    elif kind == "GRASS":                                  # a sprout
        d.line([(8, 12), (8, 5)], fill=INK)
        d.line([(8, 7), (4, 4)], fill=INK); d.line([(8, 8), (12, 5)], fill=INK)
    elif kind == "ELECTRIC":                               # a carrier
        d.line([(3, 8), (5, 8)], fill=INK); d.line([(5, 8), (7, 4)], fill=INK)
        d.line([(7, 4), (9, 12)], fill=INK); d.line([(9, 12), (11, 8)], fill=INK); d.line([(11, 8), (13, 8)], fill=INK)
    elif kind == "PSYCHIC":                                # two brackets: the frame is the thing
        d.line([(5, 3), (3, 3)], fill=INK); d.line([(3, 3), (3, 12)], fill=INK); d.line([(3, 12), (5, 12)], fill=INK)
        d.line([(10, 3), (12, 3)], fill=INK); d.line([(12, 3), (12, 12)], fill=INK); d.line([(12, 12), (10, 12)], fill=INK)
    elif kind == "ICE":                                    # a crystal
        d.line([(8, 2), (8, 13)], fill=INK); d.line([(3, 5), (12, 10)], fill=INK); d.line([(3, 10), (12, 5)], fill=INK)
    elif kind == "DRAGON":                                 # a spiral, unaccounted for
        d.arc([3, 3, 12, 12], 0, 300, fill=INK); d.arc([6, 6, 10, 10], 90, 360, fill=INK)
    elif kind == "DARK":                                   # solid: nothing gets out
        d.rectangle([3, 4, 12, 11], fill=INK)
    return im


TYPES = ["NORMAL", "FIGHTING", "FLYING", "POISON", "GROUND", "ROCK", "BUG", "GHOST", "STEEL",
         "MYSTERY", "FIRE", "WATER", "GRASS", "ELECTRIC", "PSYCHIC", "ICE", "DRAGON", "DARK"]


def primary_types():
    src = open(os.path.join(E, "src/data/pokemon/species_info.h")).read()
    out = {}
    #  split on the label rather than matching a braced block: SPECIES_NONE is written `= {0},` on one line, so a
    #  non-greedy block match runs straight through it and swallows BULBASAUR's entry with it.
    parts = re.split(r"\[SPECIES_(\w+)\]\s*=", src)
    for name, body in zip(parts[1::2], parts[2::2]):
        t = re.search(r"\.types = \{TYPE_(\w+), TYPE_(\w+)\}", body)
        if t:
            out[name.lower()] = t.group(1)
    return out


def main():
    marks = {t: mark(t) for t in TYPES}
    names = dict(re.findall(r'\[TYPE_(\w+)\] = _\("([^"]*)"\)', open(os.path.join(E, "src/battle_main.c")).read()))
    types = primary_types()
    count = {t: sum(1 for v in types.values() if v == t) for t in TYPES}
    S, CW = 6, 112
    out = Image.new("RGB", (9 * CW, 2 * (16 * S + 34) + 6), (40, 44, 52))
    d = ImageDraw.Draw(out)
    for i, t in enumerate(TYPES):
        cx, cy = (i % 9) * CW + 6, (i // 9) * (16 * S + 34) + 6
        d.rectangle([cx, cy, cx + CW - 12, cy + 16 * S + 26], fill=(250, 250, 248))
        out.paste(marks[t].convert("RGB").resize((16 * S, 16 * S), Image.NEAREST), (cx + (CW - 12 - 16 * S) // 2, cy + 4))
        d.text((cx + 6, cy + 16 * S + 8), "%-10s %3d" % (names.get(t, t), count[t]), fill=(30, 30, 34))
    out.save(PREVIEW)
    print("  eighteen marks, and how many daemons carry each -> %s" % PREVIEW)
    if WRITE:
        n = 0
        for species, t in sorted(types.items()):
            p = os.path.join(E, "graphics/pokemon/%s/footprint.png" % species)
            if os.path.exists(p) and t in marks:
                marks[t].save(p)
                n += 1
        print("  written %d footprints, one per species from its primary type" % n)


if __name__ == "__main__":
    main()

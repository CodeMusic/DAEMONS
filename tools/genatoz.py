#!/usr/bin/env python3
"""The INDEX's A TO Z MODE, sorted by OUR names (T-477).

    python3 tools/genatoz.py            # report: how far the table is from our names' order
    python3 tools/genatoz.py --write    # rewrite gPokedexOrder_Alphabetical in src/data/pokemon/pokedex_orders.h

gPokedexOrder_Alphabetical was pret's: vanilla's English names in order, ABRA, ABSOL, AERODACTYL. Every species has
been renamed since, so A TO Z MODE read in no order at all (found fixing T-470). The order is DERIVED here, never
typed, so it stays right as names change: run it after any rename (port_names.py, gbanexus.py, gbacarried.py ...).

  WHICH ENTRIES. Every NATIONAL_DEX_ constant the engine's enum declares, NONE excepted -- which is the 422 the table
  held when T-470 bounded the loop by ARRAY_COUNT, and the tool asserts the table keeps exactly that set. The old
  UNOWN letters past NATIONAL_DEX_COUNT stay at the front in enum order, as pret kept them: the screen skips any
  number past the dex it shows, so where they sit does not matter, only that they are there.

  WHOSE NAME. A dex number is shown with gSpeciesNames[NationalPokedexNumToSpecies(n)], so this reads the same
  path: src/pokemon.c's sSpeciesToNationalPokedexNum (species i+1 -> its number, SPECIES_TO_NATIONAL(X) or a literal
  NATIONAL_DEX_X, as gbanexus writes for the NEXUS residents), then src/data/text/species_names.h.

  WHAT ORDER. The charmap's: a space before every letter (LEMMA MIND), letters A to Z, and two equal names by
  national number. Our names are capitals and spaces; a name with anything else stops the tool rather than guess.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(GBA, "src/data/pokemon/pokedex_orders.h")
WRITE = "--write" in sys.argv
TABLE = "gPokedexOrder_Alphabetical"


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8").read()


def dex_enum():
    """NATIONAL_DEX_ constants in enum order, and the one NATIONAL_DEX_COUNT names"""
    src = read("include/constants/pokedex.h")
    body = src[src.index("NATIONAL_DEX_NONE"):]
    body = body[:body.index("};")]
    names = re.findall(r"^\s*(NATIONAL_DEX_\w+)\s*,", body, re.M)
    count = re.search(r"#define NATIONAL_DEX_COUNT\s+(NATIONAL_DEX_\w+)", src).group(1)
    assert count in names, "NATIONAL_DEX_COUNT names %s, which the enum does not declare" % count
    return names, count


def dex_names():
    """NATIONAL_DEX_X -> the name the INDEX prints for it"""
    ids = {n: int(v) for n, v in re.findall(r"#define (SPECIES_\w+) (\d+)\s*$", read("include/constants/species.h"), re.M)}
    by_id = {v: n for n, v in ids.items()}
    src = read("src/pokemon.c")
    start = src.index("sSpeciesToNationalPokedexNum[NUM_SPECIES - 1] =")
    body = src[src.index("{", start) + 1:src.index("};", start)]
    entries = re.findall(r"SPECIES_TO_NATIONAL\((\w+)\)|(NATIONAL_DEX_\w+)", body)
    names = dict(re.findall(r"\[(SPECIES_\w+)\]\s*=\s*_\(\"([^\"]*)\"\)", read("src/data/text/species_names.h")))
    out = {}
    for i, (via, literal) in enumerate(entries):
        dex = literal or "NATIONAL_DEX_" + via
        species = by_id[i + 1]
        #  the first species wins, as NationalPokedexNumToSpecies searches from species 1 up
        out.setdefault(dex, names[species])
    return out


def current():
    src = open(OUT, encoding="utf-8").read()
    start = src.index("const u16 %s[] =" % TABLE)
    end = src.index("};", start) + 2
    return src, start, end, re.findall(r"^\s*(NATIONAL_DEX_\w+),", src[start:end], re.M)   # entries, not comments


def order():
    enum, count = dex_enum()
    shown = enum[1:enum.index(count) + 1]            # NONE is not a daemon
    past = enum[enum.index(count) + 1:]              # the old UNOWN letters: never shown, kept at the front
    names = dex_names()
    missing = [d for d in shown if d not in names]
    assert not missing, "no species for %s" % missing
    odd = sorted({names[d] for d in shown if not re.fullmatch(r"[A-Z][A-Z ]*", names[d])})
    assert not odd, "names this tool does not know how to sort: %s" % odd
    rank = {d: i for i, d in enumerate(enum)}
    return past, sorted(shown, key=lambda d: (names[d], rank[d])), names


def render(past, ordered):
    lines = ["const u16 %s[] =" % TABLE, "{",
             "    // T-477: written by DAEMONS tools/genatoz.py from our names -- run it after a rename, never edit by hand.",
             "    // The old UNOWN letters past NATIONAL_DEX_COUNT: the INDEX skips them."]
    lines += ["    %s," % d for d in past]
    lines += ["    // Actual daemons start here."]
    lines += ["    %s," % d for d in ordered]
    return "\n".join(lines) + "\n};"


def main():
    past, ordered, names = order()
    src, start, end, have = current()
    want = past + ordered
    if sorted(have) != sorted(want):
        gone, new = sorted(set(have) - set(want)), sorted(set(want) - set(have))
        raise SystemExit("  the table's set of entries would change (T-470 bounded it at %d): lose %s, gain %s"
                         % (len(have), gone[:5], new[:5]))
    shown = [names[d] for d in ordered]
    print("  %d entries (%d shown, %d old UNOWN letters skipped): %s, %s, %s ... %s, %s, %s"
          % (len(want), len(ordered), len(past), *shown[:3], *shown[-3:]))
    moved = sum(1 for a, b in zip(have, want) if a != b)
    text = render(past, ordered)
    if src[start:end] == text:
        print("  %s already reads A to Z by our names" % TABLE)
        return 0
    print("  %d of %d entries %s" % (moved, len(want), "out of place" if moved else "in place; the comments differ"))
    if not WRITE:
        print("  (report only; pass --write)")
        return 0
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(src[:start] + text + src[end:])
    os.replace(tmp, OUT)
    print("  wrote %s" % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())

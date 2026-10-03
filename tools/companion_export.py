#!/usr/bin/env python3
"""C-03 (daemons-companion): one export of what the goal companion needs to know about DAEMONS, so nothing is typed
twice.

    python3 tools/companion_export.py            # report: what would change in companion/server/data/
    python3 tools/companion_export.py --write    # write it

Writes three files into the companion repo (symlinked here as companion/, setup.sh step 5):

  species.json  every species the save can hold, keyed by the game's INTERNAL species id (what a save stores), with
                its national INDEX number, our name, our types, the INDEX category, both editions' entries (CONTENT is
                FireRed's pokedex_text_fr.h, CONTEXT LeafGreen's pokedex_text_lg.h), and its art in gfx/daemons/
  charmap.json  the game's text encoding, byte -> character, for reading nicknames and names out of a save
  week.json     the week as the game keeps it: Sunday first, each day's colour (day_trims.h, the CHECKPOINT's trim)
                and its note, C to B (vision 9.21)
  seasons.json  the seasons by edition (C-14), from tools/seasons.py -- the one definition the game shares

Everything is read from the engine's sources and the art folder; nothing of Nintendo's is copied -- our names, our
entries and our art only.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(ROOT, "companion", "server", "data")
WRITE = "--write" in sys.argv


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8").read()


def gba_string(body):
    """the text of a _("...") or a run of "..." lines, with the line breaks as \\n"""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', body)
    return "".join(parts).replace("\\n", "\n").replace("\\p", "\n\n")


def species_table():
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define SPECIES_(\w+)\s+(\d+)\b", read("include/constants/species.h"))}
    dex = re.findall(r"NATIONAL_DEX_(\w+)\s*,", read("include/constants/pokedex.h"))
    national = {name: i for i, name in enumerate(dex)}                       # NATIONAL_DEX_NONE is 0
    to_nat = set(re.findall(r"SPECIES_TO_NATIONAL\((\w+)\)", read("src/pokemon.c")))   # every species the INDEX numbers
    names = dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/data/text/species_names.h")))
    typename = dict(re.findall(r'\[TYPE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/battle_main.c")))
    info = read("src/data/pokemon/species_info.h")
    types = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{((?:(?!\[SPECIES_).)*)", info, re.S):   # a body ends at the next species ([SPECIES_NONE] = {0}, is one line)
        t = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+)\s*,\s*TYPE_(\w+)\s*\}", m.group(2))
        if t:
            pair = [typename.get(t.group(1), t.group(1))]
            if t.group(2) != t.group(1):
                pair.append(typename.get(t.group(2), t.group(2)))
            types[m.group(1)] = pair
    entries = read("src/data/pokemon/pokedex_entries.h")
    cat, desc = {}, {}
    for m in re.finditer(r"\[NATIONAL_DEX_(\w+)\]\s*=\s*\{((?:(?!\[NATIONAL_DEX_).)*)", entries, re.S):
        c = re.search(r'\.categoryName\s*=\s*_\("([^"]*)"\)', m.group(2))
        d = re.search(r"\.description\s*=\s*(\w+)", m.group(2))
        if c:
            cat[m.group(1)] = c.group(1)
        if d:
            desc[m.group(1)] = d.group(1)
    texts = {}
    for edition, rel in (("CONTENT", "src/data/pokemon/pokedex_text_fr.h"), ("CONTEXT", "src/data/pokemon/pokedex_text_lg.h")):
        texts[edition] = {m.group(1): gba_string(m.group(2))
                          for m in re.finditer(r"const u8 (\w+)\[\]\s*=\s*_\((.*?)\);", read(rel), re.S)}
    art = set(os.listdir(os.path.join(ROOT, "gfx", "daemons")))

    out = {}
    for sp, sid in sorted(ids.items(), key=lambda kv: kv[1]):
        if sp not in to_nat or sp not in names:
            continue
        nat = national.get(sp)
        stem = re.sub(r"[^a-z0-9_]", "", names[sp].lower().replace(" ", "_"))   # LEMMA MIND -> lemma_mind
        sym = desc.get(sp)
        row = {
            "constant": sp,
            "national": nat,
            "name": names[sp],
            "types": types.get(sp, []),
            "category": cat.get(sp),
            "entry": {ed: texts[ed].get(sym) for ed in ("CONTENT", "CONTEXT")},
            "art": {view: ("gfx/daemons/%s_%s.png" % (stem, view)) if ("%s_%s.png" % (stem, view)) in art else None
                    for view in ("front", "back")},
        }
        out[str(sid)] = row
    return out


def charmap_table():
    table = {}
    for line in read("charmap.txt").splitlines():
        m = re.match(r"^'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if m and m.group(2).upper() not in table:
            table[m.group(2).upper()] = m.group(1)
    return {"_about": "byte (hex) -> character; 0xFF ends a string", "bytes": table}


def week_table():
    trims = re.findall(r"RGB\((\d+),\s*(\d+),\s*(\d+)\),\s*//\s*(\w+),\s*([A-G])", read("src/data/day_trims.h"))
    days = []
    for r, g, b, day, note in trims:
        hexc = "#%02X%02X%02X" % tuple(int(v) * 255 // 31 for v in (r, g, b))
        days.append({"day": day.capitalize(), "colour": hexc, "note": note})
    return {"_about": "Sunday first; each day's colour is the CHECKPOINT's trim (day_trims.h) and its note C to B "
                      "(vision 9.21). The virtue for each day comes from RoverRadio (companion C-01) when known.",
            "days": days}


def seasons_table():
    """C-14: the seasons from tools/seasons.py, the one definition the game's T-359 will share."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import seasons
    return {"_about": "vision 9.21: CONTENT keeps the northern year, CONTEXT the southern. A season begins on its date "
                      "and runs to the day before the next; the southern year is the northern one two seasons on. "
                      "Defined once in DAEMONS tools/seasons.py.",
            "order": list(seasons.SEASONS),
            "north_starts": {k: {"month": m, "day": d} for k, (m, d) in seasons.NORTH_STARTS.items()},
            "edition_hemisphere": seasons.EDITION_HEMISPHERE,
            "play_hours_per_season": seasons.PLAY_HOURS_PER_SEASON}


def main():
    files = {"species.json": species_table(), "charmap.json": charmap_table(), "week.json": week_table(),
             "seasons.json": seasons_table()}
    changed = []
    for name, data in files.items():
        text = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
        path = os.path.join(OUT, name)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old != text:
            changed.append(name)
            if WRITE:
                os.makedirs(OUT, exist_ok=True)
                open(path, "w", encoding="utf-8").write(text)
    sp = files["species.json"]
    with_art = sum(1 for r in sp.values() if r["art"]["front"])
    with_entry = sum(1 for r in sp.values() if r["entry"]["CONTENT"] and r["entry"]["CONTEXT"])
    print("  %d species (%d with both editions' entries, %d with art), %d characters, %d days, 4 seasons"
          % (len(sp), with_entry, with_art, len(files["charmap.json"]["bytes"]), len(files["week.json"]["days"])))
    if not changed:
        print("  companion/server/data/ agrees")
    elif WRITE:
        print("  written: " + ", ".join(changed))
    else:
        print("  would change: " + ", ".join(changed) + " (report only; pass --write)")


if __name__ == "__main__":
    main()

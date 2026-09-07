#!/usr/bin/env python3
"""Rewrite the AI harness's name tables from OUR build.

    python3 tools/port_gamedata.py [--write]

WHY. engineAi/game_data_firered/mappings.json carries the names the agent is
shown for species, moves, items and maps -- and they are retail Kanto's. So the
agent reads BULBASAUR where the screen says our name, PALLET_TOWN where the
game says BLANCHE, and it reasons about a game that does not exist. Same class
of error as the prompts, and less visible: nothing errors, the words are simply
wrong.

The tables are keyed by ID and the names are VALUES, so rewriting them is safe:
game_data.py builds a group/number lookup out of MAP_NAME_TABLE and never
matches on the string.

WHAT COMES FROM WHERE. Species, moves and items are read out of our own source
rather than transcribed, so they cannot drift from the ROM:
    SPECIES_NAME  src/data/text/species_names.h
    MOVE_NAME     src/data/text/move_names.h
    ITEM_NAME     src/data/items.json
Map names have no such table -- 3.3 renames what the PLAYER reads, while these
are internal identifiers -- so they go through a word substitution instead, and
only the towns 3.3 actually renamed.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
MAPS = os.path.join(ROOT, "engineAi", "game_data_firered", "mappings.json")
WRITE = "--write" in sys.argv

#  3.3's town renames, and the places 3.1 renamed outright. Applied to internal
#  identifiers, so they are the SCREAMING_SNAKE forms.
PLACES = [
    ("PALLET", "BLANCHE"), ("VERMILION", "ARDOR"), ("CINNABAR", "QUICKSILVER"),
    ("CELADON", "VERDIGRIS"), ("VIRIDIAN_FOREST", "THE_UNDERTONE"),
    ("ROCK_TUNNEL", "THE_BLACKOUT"), ("VICTORY_ROAD", "UMBRAL_ASCENT"),
    ("POKEMON_TOWER", "HALFTONE_TOWER"), ("POKEMON_MANSION", "DAEMON_MANSION"),
    ("POKEMON_LEAGUE", "REVIEW_BOARD"), ("MT_MOON", "DEADSTACK"),
    ("POKEMON", "DAEMON"),          # last: anything else that still says it
]


def upstream_header(path):
    """Vanilla's copy of the same file, from the fork's upstream remote."""
    import subprocess
    r = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + path],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def names_from_text(src, macro):
    """[MOVE_X] = _("NAME") -> [NAME, ...] in declaration order."""
    found = re.findall(r"\[%s_(\w+)\]\s*=\s*_\(\"([^\"]*)\"\)" % macro, src)
    #  The harness's tables are SCREAMING_SNAKE identifiers -- KARATE_CHOP, not
    #  "KARATE CHOP". Writing our spaced display strings in would have "renamed"
    #  200 moves we never touched, changing only the separator, and anything
    #  matching on those identifiers would have quietly stopped matching.
    return [n.replace(" ", "_") for _, n in found]


def names_from_header(path, macro):
    return names_from_text(open(os.path.join(GBA, path), encoding="utf-8").read(), macro)


def main():
    raw = json.load(open(MAPS, encoding="utf-8"))
    report = []

    #  species and moves: our source lists them in ID order
    for key, path, macro in (("SPECIES_NAME", "src/data/text/species_names.h", "SPECIES"),
                             ("MOVE_NAME", "src/data/text/move_names.h", "MOVE")):
        try:
            ours = names_from_header(path, macro)
        except FileNotFoundError:
            report.append((key, 0, "source missing")); continue
        #  DIFF AGAINST UPSTREAM, DO NOT ZIP. CLAUDE.md records why for
        #  port_names.py and it is the same trap here: writing every name whose
        #  string differs would have "renamed" 23 moves we never touched --
        #  DOUBLESLAP to DOUBLE_SLAP and the like, which is the harness's own
        #  normalisation and better than our raw display strings -- plus index
        #  0, whose value in our source is the padding "-$$$$$$".
        #
        #  Only where OUR source differs from VANILLA's is a rename ours.
        van = names_from_text(upstream_header(path), macro)
        table = raw[key]
        changed = 0
        for i, name in enumerate(ours):
            k = str(i)
            if i >= len(van) or van[i] == name:
                continue                      # unchanged from vanilla
            if k in table and table[k] != name:
                table[k] = name; changed += 1
        report.append((key, changed, "%d ours of %d" % (changed, len(ours))))

    #  items come from the json the build generates its header from
    try:
        doc = json.load(open(os.path.join(GBA, "src/data/items.json"), encoding="utf-8"))
        items = doc if isinstance(doc, list) else next(v for v in doc.values() if isinstance(v, list))
        table, changed = raw["ITEM_NAME"], 0
        import subprocess
        vr = subprocess.run(["git", "-C", GBA, "show", "upstream/master:src/data/items.json"],
                            capture_output=True, text=True)
        vdoc = json.loads(vr.stdout) if vr.returncode == 0 else []
        vitems = vdoc if isinstance(vdoc, list) else next(
            (v for v in (vdoc.values() if isinstance(vdoc, dict) else []) if isinstance(v, list)), [])
        for i, it in enumerate(items):
            k, name = str(i), str(it.get("english", "")).replace(" ", "_")
            van = str(vitems[i].get("english", "")).replace(" ", "_") if i < len(vitems) else None
            if van is not None and van == name:
                continue                      # unchanged from vanilla
            if name and k in table and table[k] != name:
                table[k] = name; changed += 1
        report.append(("ITEM_NAME", changed, "%d in items.json" % len(items)))
    except Exception as e:
        report.append(("ITEM_NAME", 0, "skipped: %s" % str(e)[:40]))

    #  map names: substitution, longest first so VIRIDIAN_FOREST beats VIRIDIAN
    changed = 0
    for grp, maps in raw["MAP_NAME_TABLE"].items():
        for num, name in maps.items():
            new = name
            for old, rep in sorted(PLACES, key=lambda p: -len(p[0])):
                new = new.replace(old, rep)
            if new != name:
                maps[num] = new; changed += 1
    report.append(("MAP_NAME_TABLE", changed, "%d maps" % sum(len(m) for m in raw["MAP_NAME_TABLE"].values())))

    for k, n, note in report:
        print("  %-18s %4d renamed   (%s)" % (k, n, note))

    left = [n for m in raw["MAP_NAME_TABLE"].values() for n in m.values()
            if re.search(r"POKEMON|PALLET|CINNABAR|CELADON|VERMILION", n)]
    print("  vanilla place names left: %s" % (", ".join(sorted(set(left))[:4]) if left else "none"))

    if not WRITE:
        print("\n  (report only; pass --write)")
        return
    json.dump(raw, open(MAPS, "w", encoding="utf-8"), indent=1)
    print("\n  written %s" % MAPS)


if __name__ == "__main__":
    main()

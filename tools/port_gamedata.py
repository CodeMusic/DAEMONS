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
#  ALL SIXTEEN, not the four that happened to get typed. This list had
#  PALLET, VERMILION, CINNABAR and CELADON and stopped -- so the agent read
#  BLANCHE for its home town and VIRIDIAN_CITY for the next one along, and
#  wrote "head toward Viridian City" into its own objectives. Kept in step with
#  port_vocab.py's table, which is the one that has always been complete.
PLACES = [
    ("PALLET", "BLANCHE"), ("VERMILION", "ARDOR"), ("CINNABAR", "QUICKSILVER"),
    ("CELADON", "VERDIGRIS"), ("VIRIDIAN_FOREST", "THE_UNDERTONE"),
    ("VIRIDIAN", "CALLOW"), ("PEWTER", "SLATE"), ("CERULEAN", "DOLDRUM"),
    ("LAVENDER", "HALFTONE"), ("FUCHSIA", "LURID"), ("SAFFRON", "BRAZEN"),
    ("INDIGO", "UMBRA"), ("SEAFOAM", "GLAUCOUS"),
    ("ROCK_TUNNEL", "THE_BLACKOUT"), ("VICTORY_ROAD", "UMBRAL_ASCENT"),
    ("POKEMON_TOWER", "HALFTONE_TOWER"), ("POKEMON_MANSION", "DAEMON_MANSION"),
    ("POKEMON_LEAGUE", "REVIEW_BOARD"), ("MT_MOON", "DEADSTACK"),
    #  The two buildings the lexicon renamed and the port kept calling
    #  DAEMON MART / DAEMON CENTER. These are the AGENT's copy of the map
    #  names, so leaving them vanilla means the agent reasons about a Mart
    #  while the game shows it a REPO -- and it then writes "Pokemon Mart"
    #  into its own markers, which persist and teach it again next turn.
    #
    #  Safe as bare words here: checked against all 427 map names, MART and
    #  CENTER never appear inside a longer word, and the substitution runs
    #  longest-first so POKEMON_CENTER is consumed before CENTER is reached.
    ("POKEMON_CENTER", "CHECKPOINT"), ("DAEMON_CENTER", "CHECKPOINT"),
    ("CENTER", "CHECKPOINT"), ("MART", "REPO"),
    #  Her lab. port_oak.py renames every OAK the PLAYER reads and this table
    #  was never given the same treatment, so the agent read
    #  BLANCHE_TOWN_PROFESSOR_OAKS_LAB as the lab door's destination on every
    #  single turn -- and then wrote "I hope this NPC is Professor Oak" into
    #  its own inner voice. It was not recalling vanilla; it was reading ours.
    #
    #  NO TITLE, per the lexicon: she is CRYSTAL CLEAR, never PROF. So
    #  PROFESSOR_OAKS_LAB becomes CRYSTALS_LAB rather than PROFESSOR_CRYSTALS.
    ("PROFESSOR_OAKS_LAB", "CRYSTALS_LAB"), ("PROFESSOR_OAK", "CRYSTAL_CLEAR"),
    ("OAKS_LAB", "CRYSTALS_LAB"), ("PROF_OAK", "CRYSTAL_CLEAR"),
    ("OAK", "CRYSTAL_CLEAR"),
    #  Lexicon words that reach these tables too. TRAINER -> USER and
    #  POKEDEX -> INDEX are settled everywhere else in the game and were
    #  simply never applied to the agent's copies.
    ("COOLTRAINER", "COOLUSER"), ("TRAINER_TOWER", "USER_TOWER"),
    ("TRAINER_TIPS", "USER_TIPS"), ("TRAINER", "USER"),
    ("POKEDEX", "INDEX"),
    ("POKEMON", "DAEMON"),          # last: anything else that still says it
]


#  The dashboard's PROGRESS panel. Labels only -- id and trigger are matched
#  against game flags and must not move.
PROGRESS_LABELS = {
    "Starter Pokémon": "Starter DAEMON",   "Get Pokédex": "Get the INDEX",
    "Boulder Badge": "SLATE MARK",         "Cascade Badge": "SLOPE MARK",
    "Thunder Badge": "SENSE MARK",         "Rainbow Badge": "FIT MARK",
    "Soul Badge": "SKEW MARK",             "Marsh Badge": "FRAME MARK",
    "Volcano Badge": "HEAT MARK",          "Earth Badge": "TRUE MARK",
    "Mt. Moon": "DEADSTACK",               "Rock Tunnel": "THE BLACKOUT",
    "Victory Road": "UMBRAL ASCENT",       "Elite Four": "THE REVIEW BOARD",
    "Pokémon Tower": "HALFTONE TOWER",     "Pokémon Mansion": "DAEMON MANSION",
    "Rocket Hideout": "CORPUS HIDEOUT",
}


# Gen 3's badge order, which is fixed and is the only thing here that never
# changes. The bridge's BADGES table is read for what WE call each one, so the
# rename lives in exactly one place.
VANILLA_BADGES = ["BOULDER", "CASCADE", "THUNDER", "RAINBOW",
                  "SOUL", "MARSH", "VOLCANO", "EARTH"]


def our_badge_ids():
    """The eight MARK ids, read out of the bridge rather than typed here."""
    f = os.path.join(ROOT, "engineAi/firered_bridge/constants/addresses.py")
    if not os.path.isfile(f):
        return {}
    m = re.search(r"BADGES = \[(.*?)\n\]", open(f, encoding="utf-8").read(), re.S)
    if not m:
        return {}
    ids = [x[0] for x in re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]*)"', m.group(1))]
    return dict(zip(VANILLA_BADGES, ids))


def port_progress():
    """Rewrite the milestone labels AND the badge triggers. Both copies --
    server/progress_steps.json and the gpt_data mirror -- or the dashboard and
    the agent disagree.

    The trigger is a CONTRACT with the bridge: gameLoop matches a step's
    trigger against the badge id the bridge reports. Renaming BADGES to the
    eight MARKS broke it silently -- the card showed the SLATE MARK and the
    step stayed unticked, because the step was still waiting for BOULDER.
    Nothing errored, which is why it took a screenshot to find."""
    badges = our_badge_ids()
    total = 0
    for rel in ("engineAi/server/progress_steps.json",
                "engineAi/server/gpt_data/progress_steps.json"):
        f = os.path.join(ROOT, rel)
        if not os.path.isfile(f):
            continue
        doc = json.load(open(f, encoding="utf-8"))
        steps = doc if isinstance(doc, list) else doc.get("steps", [])
        n = 0
        t = 0
        for e in steps:
            lab = e.get("label")
            if lab in PROGRESS_LABELS:
                e["label"] = PROGRESS_LABELS[lab]; n += 1
            if e.get("type") == "badge" and e.get("trigger") in badges:
                e["trigger"] = badges[e["trigger"]]; t += 1
        print("  %-40s %2d of %d labels, %d badge trigger(s)"
              % (os.path.basename(rel), n, len(steps), t))
        total += n
        if WRITE:
            json.dump(doc, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return total


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

    #  EVENT_OBJECT_NAME is how the agent is told WHO IT IS LOOKING AT -- the
    #  NPC entries in the prompt come from here. It still held PROF_OAK, so the
    #  sprite standing in her lab announced itself as Oak on every turn the
    #  agent could see her, and the inner voice duly read "I hope this NPC is
    #  Professor Oak". No tool had ever touched this table.
    if isinstance(raw.get("EVENT_OBJECT_NAME"), dict):
        objs = raw["EVENT_OBJECT_NAME"]
        nchanged = 0
        for k, name in list(objs.items()):
            if not isinstance(name, str):
                continue
            new_name = name
            for old_w, rep in sorted(PLACES, key=lambda p: -len(p[0])):
                new_name = new_name.replace(old_w, rep)
            if new_name != name:
                objs[k] = new_name; nchanged += 1
        report.append(("EVENT_OBJECT_NAME", nchanged, "%d objects" % len(objs)))

    port_progress()

    for k, n, note in report:
        print("  %-18s %4d renamed   (%s)" % (k, n, note))

    #  The leftover check used to look for POKEMON|PALLET|CINNABAR|CELADON|
    #  VERMILION -- which is to say, only the names the list already handled.
    #  It printed "vanilla place names left: none" while VIRIDIAN_CITY,
    #  PEWTER_CITY and six others sat untouched in the table it had just
    #  written. A check that can only find what you already fixed is not a
    #  check. Derived from the full vanilla set now, so adding a town to
    #  PLACES and forgetting the guard is no longer possible.
    VANILLA = ["POKEMON", "PALLET", "VIRIDIAN", "PEWTER", "CERULEAN",
               "VERMILION", "LAVENDER", "CELADON", "FUCHSIA", "SAFFRON",
               "CINNABAR", "INDIGO", "SEAFOAM", "MART", "CENTER", "OAK"]
    left = [n for m in raw["MAP_NAME_TABLE"].values() for n in m.values()
            if re.search("|".join(VANILLA), n)]
    print("  vanilla place names left: %s" % (", ".join(sorted(set(left))[:4]) if left else "none"))

    if not WRITE:
        print("\n  (report only; pass --write)")
        return
    json.dump(raw, open(MAPS, "w", encoding="utf-8"), indent=1)
    print("\n  written %s" % MAPS)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""NIGHT on a few routes (T-268; vision.md 9.21, decided by the user 2026-09-25).

    python3 tools/gbanight.py            # report
    python3 tools/gbanight.py --write     # engineGba/src/data/wild_encounters.json

9.21: "The daemons change by watch on a few routes and islands, not everywhere. LATENT and OPAQUE come out at night,
and a handful of daemons are met only then" -- and nobody says so. The user chose three or four routes, as 9.21 did.

THE RULE, which a player can learn by walking: the day's bird sleeps. PACKET is the daylight flier, and at night its
slots go to what runs in the dark -- the LATENT line (DANGLING, and on Route 12 RESPAWN), each at the slot's own level
and odds, so a route's difficulty is where it was. OPAQUE has no daemon in the first 151, and a daemon beyond them
would arrive before the national INDEX can hold it, so the night is LATENT's for now.

THE ROUTES. Route 1, because the first route is where a player can first notice anything; and 8, 10 and 12, the three
roads into HALFTONE -- 10 is "Gloaming" in 4.x's table, dusk approaching the tower -- where the tower's LATENT would be
seen out after dark. Both editions change the same way, so the edition split (Tier 2) is untouched.

HOW. wild_encounter.c takes the header right after a map's own when it is night and that header is for the same map.
So each night table is written immediately after its day table, per edition, labelled <day label>_Night (the label
still contains FireRed or LeafGreen, which is what the template's #ifdef reads), and carries ALL of the day's tables:
the one it chose is the only header the engine reads, for the grass, the water, the rods and Rock Smash alike. The day tables are never edited:
this tool rebuilds every _Night header from its day one and the rule below, so re-running it changes nothing.
"""
import copy, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = os.path.join(ROOT, "engineGba/src/data/wild_encounters.json")
WRITE = "--write" in sys.argv

# map -> {land slot: species at night}. Slots keep their level and odds (20,20,10,10,10,10,5,5,4,4,1,1).
NIGHT = {
    "MAP_ROUTE1":  {0: "SPECIES_RATTATA", 2: "SPECIES_RATTATA", 4: "SPECIES_RATTATA",
                    6: "SPECIES_GASTLY", 8: "SPECIES_GASTLY", 10: "SPECIES_GASTLY"},
    "MAP_ROUTE8":  {0: "SPECIES_GASTLY", 3: "SPECIES_GASTLY"},
    "MAP_ROUTE10": {2: "SPECIES_GASTLY", 3: "SPECIES_GASTLY"},
    "MAP_ROUTE12": {3: "SPECIES_GASTLY", 4: "SPECIES_GASTLY", 7: "SPECIES_HAUNTER", 8: "SPECIES_GASTLY",
                    10: "SPECIES_GASTLY"},
}
DAY_BIRD = "SPECIES_PIDGEY"   # PACKET: where a slot is replaced because the bird sleeps, it must be the bird's


def night_of(day):
    n = copy.deepcopy(day)
    n["base_label"] = day["base_label"] + "_Night"
    # Night changes the grass; the water, the rods and the rocks are as by day -- and they must be COPIED, not left
    # out: the engine reads every table from the one header it chose, so a night header without water_mons meant no
    # surfing encounters and "not even a nibble" on Routes 10 and 12 all night (found 2026-09-25).
    mons = n["land_mons"]["mons"]
    for slot, species in NIGHT[day["map"]].items():
        if day["map"] in ("MAP_ROUTE1", "MAP_ROUTE8", "MAP_ROUTE12"):
            assert mons[slot]["species"] == DAY_BIRD, (day["base_label"], slot, mons[slot]["species"])
        mons[slot]["species"] = species
    return n


def main():
    raw = open(JSON).read()
    data = json.loads(raw)
    group = data["wild_encounter_groups"][0]
    days = [e for e in group["encounters"] if not e["base_label"].endswith("_Night")]
    out = []
    for e in days:
        out.append(e)
        if e["map"] in NIGHT and "land_mons" in e:
            out.append(night_of(e))
    group["encounters"] = out
    new = json.dumps(data, indent=2) + "\n"
    nights = [e["base_label"] for e in out if e["base_label"].endswith("_Night")]
    if new == raw:
        print("  %d night tables, already written" % len(nights))
        return 0
    print("  %d night tables to write: %s" % (len(nights), ", ".join(nights)))
    if WRITE:
        open(JSON, "w").write(new)
        print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())

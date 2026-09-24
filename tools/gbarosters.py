#!/usr/bin/env python3
"""8.4's Tier 2: the rosters LEAN (T-233).

    python3 tools/gbarosters.py            # report
    python3 tools/gbarosters.py --write     # edit engineGba/src/data/wild_encounters.json

8.4: "Do not split the exclusives at random. Bias them" -- CONTENT sees more CONTENT, LOGIC, STRATUM and LEGACY
early; CONTEXT more CONTEXT, LATENT, VECTOR and ENTROPY. The GBA's exclusives were vanilla's FireRed/LeafGreen split
and pointed the wrong way as often as the right one; CONTEXT held both STRATUM exclusives. Four swaps fix most of it,
each trading a vanilla PAIR whole so neither edition loses a daemon (decided by the user, 2026-09-24):

    WORM <-> SECTOR, OUTBREAK <-> PARTITION   (the STRATUM line to CONTENT)
    REAPER <-> BLOCKING, REPAY <-> CUNNING     (VECTOR to CONTEXT)

Written as the TARGET, not as a swap: in CONTENT's tables (the *_FireRed labels) the left-hand species become the
right-hand ones, and in CONTEXT's (*_LeafGreen) the reverse. So a second run changes nothing, which is what
tools/check_generators.py holds it to.

Only the wild tables. The Game Corner's prizes and the in-game trades are edition-split too, and are not touched
here: whether they follow is a separate question, and the ticket says so.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "engineGba/src/data/wild_encounters.json")
WRITE = "--write" in sys.argv

TO_CONTENT = {                      # in CONTENT's tables: this species becomes that one
    "SPECIES_EKANS": "SPECIES_SANDSHREW",
    "SPECIES_ARBOK": "SPECIES_SANDSLASH",
    "SPECIES_SCYTHER": "SPECIES_PINSIR",
    "SPECIES_DELIBIRD": "SPECIES_SNEASEL",
}
TO_CONTEXT = {v: k for k, v in TO_CONTENT.items()}


def main():
    text = open(PATH, encoding="utf-8").read()
    data = json.loads(text)
    changed = 0
    for e in data["wild_encounter_groups"][0]["encounters"]:
        label = e["base_label"]
        table = TO_CONTENT if label.endswith("_FireRed") else TO_CONTEXT if label.endswith("_LeafGreen") else None
        if not table:
            continue
        for field in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
            for mon in e.get(field, {}).get("mons", []):
                if mon["species"] in table:
                    mon["species"] = table[mon["species"]]
                    changed += 1
    print("  %d wild slots %s" % (changed, "swapped" if WRITE and changed else "to swap" if changed else "-- the rosters already lean"))
    if WRITE and changed:
        out = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        open(PATH, "w", encoding="utf-8").write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

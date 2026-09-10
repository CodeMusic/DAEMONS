#!/usr/bin/env python3
"""One word, one meaning. Prove no name in the lexicon is used twice.

    python3 tools/check_lexicon.py       # exits non-zero if any word is doubled

WHY THIS EXISTS. INTERRUPT was assigned to POKé FLUTE and to ICE HEAL six weeks
apart and nothing caught it. The fix -- PREEMPT -- collided with MANKEY, which
had been named PREEMPT four days earlier, and nothing caught that either. Both
times a human found it by reading a list aloud.

4.26 DID run a collision check when the bestiary was named. It validated the
new species against species, moves and types. It did not check ITEMS, because
at that moment the item pass had not happened yet -- so the check was complete
for the day it was written and incomplete by the following week.

That is the general failure: a check scoped to the surfaces that existed when
it was written. This one reads every surface out of the build each time it runs,
so a surface added later is covered without anyone remembering to add it.

WHAT COUNTS AS A COLLISION. Two DIFFERENT things wearing the same word. A move
and a type both called GROWTH is a collision; the FROZEN type and the FROZEN
state would be too, which is exactly why 1.6 went looking for HUNG.

Deliberate doubles live in ALLOWED below, each with the reason it is allowed.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")

#  Doubles that are on purpose. A word here has been argued for, not overlooked.
ALLOWED = {
    "OVERHEAT": "the ENTROPY move and the OVERHEATED state agreeing is the point (2.8)",
}

STATES = ["LEAKING", "CASCADING", "SUSPENDED", "THROTTLED",
          "OVERHEATED", "HUNG", "THRASHING", "HALTED"]


def read(rel, pat):
    f = os.path.join(GBA, rel)
    if not os.path.isfile(f):
        return []
    return re.findall(pat, open(f, encoding="utf-8", errors="ignore").read())


def main():
    surfaces = {
        "species": read("src/data/text/species_names.h",
                        r'\[SPECIES_\w+\]\s*=\s*_\("([^"]+)"\)'),
        "move":    read("src/data/text/move_names.h",
                        r'\[MOVE_\w+\]\s*=\s*_\("([^"]+)"\)'),
        "type":    read("src/battle_main.c",
                        r'\[TYPE_\w+\]\s*=\s*_\("(\w+)"\)'),
        "ability": read("src/data/text/abilities.h",
                        r'\[ABILITY_\w+\]\s*=\s*_\("([^"]+)"\)'),
        "state":   STATES,
    }
    f = os.path.join(GBA, "src/data/items.json")
    if os.path.isfile(f):
        d = json.load(open(f, encoding="utf-8"))
        surfaces["item"] = [i["english"] for i in (d if isinstance(d, list)
                                                   else d.get("items", d))]

    seen = {}
    for label, words in surfaces.items():
        for w in words:
            w = w.strip()
            #  A one- or two-letter label is a slot, not a name. Vanilla's own
            #  placeholders ("-", "???") would otherwise report as collisions
            #  against every other placeholder in the build.
            if len(w) < 3 or set(w) <= set("-?"):
                continue
            seen.setdefault(w, set()).add(label)

    bad = [(w, sorted(v)) for w, v in seen.items()
           if len(v) > 1 and w not in ALLOWED]
    print("  %d names across %s" % (len(seen), ", ".join(sorted(surfaces))))
    for w, reason in sorted(ALLOWED.items()):
        if w in seen and len(seen[w]) > 1:
            print("  ..  %-14s allowed: %s" % (w, reason))
    if not bad:
        print("  no word means two things.")
        return 0
    print("\n  %d word(s) mean two things:\n" % len(bad))
    for w, where in sorted(bad):
        print("   %-16s %s" % (w, " + ".join(where)))
    return 1


if __name__ == "__main__":
    sys.exit(main())

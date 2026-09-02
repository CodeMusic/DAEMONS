#!/usr/bin/env python3
"""Write the item descriptions Gen 1 had nowhere to put.

    python3 tools/port_item_text.py [--write]

This is not a port. The Game Boy build has no descriptions to carry over --
Gen 1 stores none at all -- so these are new writing, and vision.md 9.3 named
them as the concrete thing the GBA buys. Three lines, about 35 characters each.

Two rules held throughout. Craft rule 1: none of these explains the thesis;
they describe an object and stop. Craft rule 6: the joke is allowed to sit
underneath and is never pointed at -- the boxes are a privilege ladder and no
description says so.

The MARKS are absent on purpose. Badges are not items in Gen 3, so the eight
of them have no slot here; see tools/port_names.py.
"""
import json, os, re, sys

GBA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engineGba")
PATH = os.path.join(GBA, "src/data/items.json")
WIDTH = 36

TEXT = {
    # The ladder. 1.1: acquisition as privilege escalation, and 1.x makes the
    # catch rate literal -- "an unbound daemon will not run on a box where it
    # only has user rights." Each rung says what rights it has and lets the
    # player draw the conclusion.
    "ITEM_POKE_BALL":   ["A host offered at user level.",
                         "A steady daemon will run on it.",
                         "A stubborn one will not."],
    "ITEM_GREAT_BALL":  ["A host with wider rights than a",
                         "USERBOX. More daemons will agree",
                         "to run on it."],
    "ITEM_ULTRA_BALL":  ["A host with elevated rights.",
                         "Most daemons will run on it,",
                         "including reluctant ones."],
    "ITEM_MASTER_BALL": ["A host with unrestricted rights.",
                         "No daemon can decline to run on",
                         "it. Nothing is refused root."],
    # 1.x: the Safari Zone is restricted, temporary, expiring access.
    "ITEM_SAFARI_BALL": ["A temporary host, issued at the",
                         "gate and expiring at the gate.",
                         "Its rights are minimal."],

    # 8.x: the stones are not stones, they are what you expose a mind to, and
    # the set closes as reason from / search with / feel with / learn from.
    "ITEM_FIRE_STONE":   ["Something for a mind to reason",
                          "from. Some daemons take a new",
                          "form when given one."],
    "ITEM_THUNDER_STONE":["A representation a mind can",
                          "search through. Some daemons",
                          "take a new form when given one."],
    "ITEM_WATER_STONE":  ["Something for a mind to feel",
                          "with. Some daemons take a new",
                          "form when given one."],
    "ITEM_LEAF_STONE":   ["A signal a mind can learn from.",
                          "Some daemons take a new form",
                          "when given one."],

    # 7.x: what wakes a blocked process. SUSPEND and HIBERNATE induce it,
    # DEADLOCK is stuck in it, INTERRUPT ends it.
    "ITEM_POKE_FLUTE":   ["Sends an interrupt. A daemon",
                          "that has stopped responding",
                          "will wake."],
    # 1.x: a linker resolves a symbol to a name.
    "ITEM_SILPH_SCOPE":  ["Resolves a name that will not",
                          "resolve on its own. Some things",
                          "cannot be identified without it."],
    # 4.18: the requisition board at Quicksilver asks for one of these.
    "ITEM_OAKS_PARCEL":  ["A CLARIFIER MODULE, requisitioned",
                          "and sealed. It is addressed to",
                          "CRYSTAL, not to you."],
}

raw = open(PATH).read()
rc = 0
for item_id, lines in TEXT.items():
    for ln in lines:
        if len(ln) > WIDTH:
            print("  !! %s: %d chars > %d -- %s" % (item_id, len(ln), WIDTH, ln)); rc = 1
    body = json.dumps("\\n".join(lines))[1:-1]
    # Rewrite the description that follows this itemId, and only that one.
    pat = re.compile(r'("itemId": "%s".*?"description_english": ")(.*?)(")' % re.escape(item_id), re.S)
    raw, n = pat.subn(lambda m: m.group(1) + body + m.group(3), raw, count=1)
    if not n:
        print("  !! %s not found" % item_id); rc = 1
print("  %d descriptions" % len(TEXT))
if "--write" in sys.argv and rc == 0:
    open(PATH, "w").write(raw); print("  written")
sys.exit(rc)

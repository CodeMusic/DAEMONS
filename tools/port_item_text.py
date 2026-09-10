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
    #  8.6 moved the part number into the item NAME, so the description had
    #  to stop repeating it as a noun. This tool still held the earlier
    #  wording and would have reverted the shipped text on the next run.
    "ITEM_OAKS_PARCEL":  ["A sealed module. Part no. CC-7.",
                          "Addressed to CRYSTAL CLEAR.",
                          "Not to you."],

    #  Ruled 2026-09-10. PREEMPT collided with MANKEY -- a species named four
    #  days before the item -- and the third review found the deeper fault
    #  underneath the collision: preempting a hung task hands the processor to
    #  somebody else and the hung one stays hung. A WATCHDOG is the timer whose
    #  whole job is to notice something has stopped answering and reset it. The
    #  actual cure, and it still works twice.
    #
    #  This description lived directly in items.json and the tool did not own
    #  it, which is the same drift that nearly reverted CC-7. It owns it now.
    "ITEM_ICE_HEAL":     ["A watchdog notices a process",
                          "that stopped answering, and",
                          "resets it. Ends HUNG."],

    # ---------------------------------------------------------------- states
    #  1.6 renamed the seven states and 9.15 gave them tiles, and twenty-one
    #  descriptions went on saying paralysis, poison, burn and confusion --
    #  the two flutes, the six berries that end a state, the five that cause
    #  one, and nine TMs. A player reads a description at the moment they are
    #  deciding whether the item is the answer, so this is the surface where
    #  the vocabulary has to agree with the tile.
    "ITEM_BLUE_FLUTE":   ["A blue glass flute that resumes",
                          "a SUSPENDED daemon."],
    "ITEM_YELLOW_FLUTE": ["A yellow glass flute that ends",
                          "THRASHING in one daemon."],
    "ITEM_CHERI_BERRY":  ["When held by a DAEMON, it will be",
                          "used in battle to end THROTTLED."],
    "ITEM_PECHA_BERRY":  ["When held by a DAEMON, it will be",
                          "used in battle to end LEAKING."],
    "ITEM_RAWST_BERRY":  ["When held by a DAEMON, it will be",
                          "used in battle to cool OVERHEATED."],
    "ITEM_PERSIM_BERRY": ["When held by a DAEMON, it will be",
                          "used in battle to end THRASHING."],
    #  The five that trade health for THRASHING all share vanilla's wording,
    #  and there is no reason to give five identical items five voices.
    "ITEM_FIGY_BERRY":   ["A hold item that restores HP but",
                          "may cause THRASHING when used."],
    "ITEM_WIKI_BERRY":   ["A hold item that restores HP but",
                          "may cause THRASHING when used."],
    "ITEM_MAGO_BERRY":   ["A hold item that restores HP but",
                          "may cause THRASHING when used."],
    "ITEM_AGUAV_BERRY":  ["A hold item that restores HP but",
                          "may cause THRASHING when used."],
    "ITEM_IAPAPA_BERRY": ["A hold item that restores HP but",
                          "may cause THRASHING when used."],

    #  The TMs. "move" is deliberately left alone -- 1.6 records that
    #  move -> routine inside prose is the ROUTINES pass, not this one.
    "ITEM_TM06":         ["A move that leaves the foe",
                          "CASCADING. Its damage",
                          "worsens every turn."],
    "ITEM_TM13":         ["An icy-cold beam is shot at the",
                          "foe. It may leave the",
                          "target HUNG."],
    "ITEM_TM14":         ["A vicious snow-and-wind attack that",
                          "strikes all foe in battle. It",
                          "may cause a HANG."],
    "ITEM_TM24":         ["A massive jolt of electricity is",
                          "launched at the foe. It may",
                          "cause THROTTLING."],
    "ITEM_TM25":         ["Strikes the foe with a",
                          "huge thunderbolt. It may",
                          "cause THROTTLING."],
    "ITEM_TM35":         ["The foe is roasted with a",
                          "heavy blast of fire. It may",
                          "leave the target OVERHEATED."],
    "ITEM_TM36":         ["Toxic sludge is hurled at the",
                          "foe with great force. It may",
                          "leave the target LEAKING."],
    "ITEM_TM38":         ["The foe is incinerated with",
                          "an intense flame. It may leave",
                          "the target OVERHEATED."],
    "ITEM_TM42":         ["An attack move that becomes very",
                          "powerful if the user is LEAKING,",
                          "OVERHEATED or THROTTLED."],

    #  Three of OUR OWN descriptions had no line break at all and ran to 290,
    #  288 and 245 pixels in a box whose ceiling is 198 -- found by measuring
    #  the whole table rather than the diff, which is the only way an old line
    #  ever gets caught.
    "ITEM_FULL_RESTORE": ["Restores a DAEMON whole:",
                          "health and state together."],
    "ITEM_MAX_REVIVE":   ["Brings back a HALTED daemon",
                          "at full health."],
    "ITEM_HEAL_POWDER":  ["Bitter, cheap, and it works now.",
                          "Clears every state."],
}

#  WIDTH was a character count, which is a proxy for the thing that actually
#  matters. The face is variable width, so the real ceiling is PIXELS -- and
#  vanilla's own widest description line, measured across all 375 of them, is
#  exactly 198. That is the budget, and port_vocab already owns the measurer.
def _pixels():
    import importlib.util, io, contextlib
    argv, sys.argv = sys.argv, ["port_vocab"]
    try:
        spec = importlib.util.spec_from_file_location("pv", os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "port_vocab.py"))
        pv = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):   # it reports on load
            try:
                spec.loader.exec_module(pv)
            except SystemExit:
                pass
        return pv.textwidth
    except Exception:
        return None
    finally:
        sys.argv = argv

BUDGET = 198
textwidth = _pixels()

raw = open(PATH).read()
rc = 0
widest = 0
for item_id, lines in TEXT.items():
    for ln in lines:
        w = textwidth(ln) if textwidth else None
        if w is not None:
            widest = max(widest, w)
            if w > BUDGET:
                print("  !! %s: %dpx > %d -- %s" % (item_id, w, BUDGET, ln)); rc = 1
        elif len(ln) > WIDTH:
            print("  !! %s: %d chars > %d -- %s" % (item_id, len(ln), WIDTH, ln)); rc = 1
    body = json.dumps("\\n".join(lines))[1:-1]
    # Rewrite the description that follows this itemId, and only that one.
    pat = re.compile(r'("itemId": "%s".*?"description_english": ")(.*?)(")' % re.escape(item_id), re.S)
    raw, n = pat.subn(lambda m: m.group(1) + body + m.group(3), raw, count=1)
    if not n:
        print("  !! %s not found" % item_id); rc = 1
print("  %d descriptions, widest %dpx of %d" % (len(TEXT), widest, BUDGET))
if "--write" in sys.argv and rc == 0:
    open(PATH, "w").write(raw); print("  written")
sys.exit(rc)

#!/usr/bin/env python3
"""Write the item descriptions Gen 1 had nowhere to put.

    python3 tools/port_item_text.py [--write]       # report exits 1 when the engine is not what --write makes
    python3 tools/port_item_text.py --sheet OUT.png              # T-526: the drafts against the engine, in its font
    python3 tools/port_item_text.py --trap-sheet OUT.png         # T-526: the TRAP TABLE's rows in its two-line window
    python3 tools/port_item_text.py --write --approved ITEM ...  # T-526: write only those DRAFT descriptions

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

    #  BLACK BELT collided with the trainer class the moment that class became
    #  FORMALIST -- and its description still said FIGHTING-type, which has
    #  been LOGIC since 2.2. Rigour is what you hold to argue harder from.
    "ITEM_BLACK_BELT":   ["Held to argue harder from.",
                          "Raises the power of LOGIC",
                          "routines."],

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

    #  The TMs. "move" is NO LONGER left alone: the ROUTINES pass (T-37)
    #  swept prose to ROUTINE, and this table is authored, so a re-run was
    #  reverting it. Anything port_vocab sweeps has to be current HERE too.
    "ITEM_TM06":         ["Leaves them CASCADING,",
                          "and the loss grows with",
                          "every turn."],
    "ITEM_TM13":         ["Stops the weights",
                          "updating. They may",
                          "end up HUNG."],
    "ITEM_TM14":         ["Everything stops",
                          "updating at once. May",
                          "leave them HUNG."],
    "ITEM_TM24":         ["Lets the whole stored charge go at",
                          "once. It may leave them throttled."],
    "ITEM_TM25":         ["A spike too sudden to plan for.",
                          "Often misses. May leave them",
                          "throttled."],
    "ITEM_TM35":         ["Gives off heat in every direction.",
                          "It may leave them overheating."],
    "ITEM_TM36":         ["Everything unwanted,",
                          "all at once. May",
                          "cause LEAKING."],
    "ITEM_TM38":         ["Everything in reach ignites at once.",
                          "It may leave them overheating."],
    "ITEM_TM42":         ["Running degraded, it hits twice as",
                          "hard: overheating, leaking,",
                          "throttled."],

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


#  ---------------------------------------------------------------------------
#  THE HELD ITEMS -- 1.6c. Names AND descriptions, because unlike the ten
#  medicines these have no Game Boy source to port: Gen 1 has no held items at
#  all. 1.6 ruled that an item is an OPERATION; a held item is not one. It is a
#  CONFIGURATION -- a setting attached to a process from outside, in force
#  while it runs, and removable, which is exactly what 2.11 says an ability is
#  NOT.
#
#  The seventeen type boosters are a rack. Vanilla's are seventeen unrelated
#  trinkets -- a spoon, a magnet, a lump of charcoal -- and ours are seventeen
#  labelled controls on one desk: GAIN on a channel, TRIM for the small one,
#  HEADROOM for the margin, DITHER for the noise, MUTE for the channel you do
#  not want to hear. Five words from one instrument, and the Bag becomes a
#  glossary of the type chart, which is 8.7's second teaching surface spent.
#
#  Each gain's first clause is 2.6's own one-line test for that type, verbatim
#  where it fits. The player who reads all seventeen has read the chart.
NAMED = {
    # The rack.
    "ITEM_SILK_SCARF":     ("CONTENT GAIN",  ["The thing itself, with nothing",
                                              "read into it. Gain lifts one",
                                              "channel: this one is CONTENT."]),
    "ITEM_BLACK_BELT":     ("LOGIC GAIN",    ["Rules applied step by step, not",
                                              "intuition. Gain lifts one",
                                              "channel: this one is LOGIC."]),
    "ITEM_SHARP_BEAK":     ("VECTOR GAIN",   ["A direction that never touches",
                                              "the ground. Gain lifts one",
                                              "channel: this one is VECTOR."]),
    "ITEM_POISON_BARB":    ("CORRUPT GAIN",  ["Data that has been tampered",
                                              "with. Gain lifts one channel:",
                                              "this one is CORRUPT."]),
    "ITEM_SOFT_SAND":      ("STRATUM GAIN",  ["The layer everything else runs",
                                              "on. Gain lifts one channel:",
                                              "this one is STRATUM."]),
    "ITEM_HARD_STONE":     ("LEGACY GAIN",   ["Old material everything else has",
                                              "had time to work on. Gain lifts",
                                              "one channel: this one is LEGACY."]),
    "ITEM_SILVER_POWDER":  ("SWARM GAIN",    ["Many small agents; no single one",
                                              "matters. Gain lifts one channel:",
                                              "this one is SWARM."]),
    "ITEM_SPELL_TAG":      ("LATENT GAIN",   ["Running below the surface,",
                                              "unobserved. Gain lifts one",
                                              "channel: this one is LATENT."]),
    "ITEM_CHARCOAL":       ("ENTROPY GAIN",  ["Noise and heat; disorder that",
                                              "spreads. Gain lifts one channel:",
                                              "this one is ENTROPY."]),
    "ITEM_MYSTIC_WATER":   ("FLOW GAIN",     ["Everything running downhill to",
                                              "the lowest point. Gain lifts one",
                                              "channel: this one is FLOW."]),
    "ITEM_MIRACLE_SEED":   ("GROWTH GAIN",   ["Training: fitting to whatever it",
                                              "is fed. Gain lifts one channel:",
                                              "this one is GROWTH."]),
    "ITEM_MAGNET":         ("SIGNAL GAIN",   ["Raw current, before anything",
                                              "interprets it. Gain lifts one",
                                              "channel: this one is SIGNAL."]),
    "ITEM_TWISTED_SPOON":  ("CONTEXT GAIN",  ["The frame you read a thing in.",
                                              "Gain lifts one channel: this one",
                                              "is CONTEXT."]),
    "ITEM_NEVER_MELT_ICE": ("FROZEN GAIN",   ["Locked to what it already saw.",
                                              "Gain lifts one channel: this one",
                                              "is FROZEN."]),
    "ITEM_DRAGON_FANG":    ("EMERGENT GAIN", ["Behaviour nobody designed and",
                                              "nobody can account for. Gain",
                                              "lifts the EMERGENT channel."]),
    "ITEM_METAL_COAT":     ("HARDENED GAIN", ["Hardened against whatever anyone",
                                              "tries. Gain lifts one channel:",
                                              "this one is HARDENED."]),
    "ITEM_BLACK_GLASSES":  ("OPAQUE GAIN",   ["The black box, from outside.",
                                              "Gain lifts one channel: this one",
                                              "is OPAQUE."]),
    "ITEM_SEA_INCENSE":    ("FLOW TRIM",     ["A trim is a small gain. This one",
                                              "lifts the FLOW channel a little."]),

    # T-488 (the user, 2026-10-29): the other shelf of the rack. A SINK takes one
    # hit and is spent -- Gen 4's resist berries, as items: the first
    # super-effective hit of its type on the holder is halved and the item used
    # up. Sixteen, not eighteen: ORACLE has none, and CONTENT is super-effective
    # against nothing, so a CONTENT SINK could never fire. The GAIN's last line,
    # turned round. DRAFT, every name and line.
    "ITEM_LOGIC_SINK":     ("LOGIC SINK",   ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is LOGIC."]),
    "ITEM_VECTOR_SINK":    ("VECTOR SINK",  ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is VECTOR."]),
    "ITEM_CORRUPT_SINK":   ("CORRUPT SINK", ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is CORRUPT."]),
    "ITEM_STRATUM_SINK":   ("STRATUM SINK", ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is STRATUM."]),
    "ITEM_LEGACY_SINK":    ("LEGACY SINK",  ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is LEGACY."]),
    "ITEM_SWARM_SINK":     ("SWARM SINK",   ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is SWARM."]),
    "ITEM_LATENT_SINK":    ("LATENT SINK",  ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is LATENT."]),
    "ITEM_HARDENED_SINK":  ("HARDENED SINK",["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is HARDENED."]),
    "ITEM_ENTROPY_SINK":   ("ENTROPY SINK", ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is ENTROPY."]),
    "ITEM_FLOW_SINK":      ("FLOW SINK",    ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is FLOW."]),
    "ITEM_GROWTH_SINK":    ("GROWTH SINK",  ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is GROWTH."]),
    "ITEM_SIGNAL_SINK":    ("SIGNAL SINK",  ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is SIGNAL."]),
    "ITEM_CONTEXT_SINK":   ("CONTEXT SINK", ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is CONTEXT."]),
    "ITEM_FROZEN_SINK":    ("FROZEN SINK",  ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is FROZEN."]),
    "ITEM_EMERGENT_SINK":  ("EMERGENT SINK",["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is EMERGENT."]),
    "ITEM_OPAQUE_SINK":    ("OPAQUE SINK",  ["Halves the first super-effective",
                                          "hit on one channel, then is",
                                          "spent. This one is OPAQUE."]),

    # The rest of the desk.
    "ITEM_BRIGHT_POWDER":  ("DITHER",        ["Noise added on purpose, so that",
                                              "nothing can be pinned exactly.",
                                              "Their aim slips."]),
    "ITEM_LAX_INCENSE":    ("DITHER TRIM",   ["Dither, at a lower setting.",
                                              "Their aim slips a little."]),
    "ITEM_LEFTOVERS":      ("HEADROOM",      ["The margin left before anything",
                                              "clips. The holder recovers a",
                                              "little each turn."]),
    "ITEM_CLEANSE_TAG":    ("MUTE",          ["Mutes the channel wild daemons",
                                              "listen on. Carried in front,",
                                              "fewer of them approach."]),

    # Configurations.
    "ITEM_WHITE_HERB":     ("REVERT",        ["Puts a value back the way it",
                                              "was. Restores a lowered stat,",
                                              "once."]),
    "ITEM_MENTAL_HERB":    ("UNPAIR",        ["Drops a binding that was formed",
                                              "without being asked for. Works",
                                              "once."]),
    "ITEM_MACHO_BRACE":    ("DEBUG BUILD",   ["Every step is instrumented, so",
                                              "it learns faster and runs",
                                              "slower. SPEED falls."]),
    "ITEM_EXP_SHARE":      ("WEIGHT SHARE",  ["Two things trained as one: what",
                                              "teaches the first teaches the",
                                              "second. Shares EXP. POINTS."]),
    "ITEM_QUICK_CLAW":     ("QUEUE JUMP",    ["Sometimes the scheduler takes",
                                              "you out of turn. The holder may",
                                              "move first."]),
    "ITEM_SOOTHE_BELL":    ("AFFINITY",      ["Affinity binds a process to one",
                                              "host. The holder grows attached",
                                              "faster."]),
    "ITEM_SMOKE_BALL":     ("ESCAPE HATCH",  ["A way out that is always open.",
                                              "The holder can DETACH from any",
                                              "wild daemon."]),
    "ITEM_EVERSTONE":      ("VERSION LOCK",  ["Pins a thing to the version it",
                                              "is at. The holder will not",
                                              "evolve."]),
    "ITEM_FOCUS_BAND":     ("FAILSAFE",      ["What stops the fall when",
                                              "everything else already has.",
                                              "The holder may survive on 1 HP."]),
    "ITEM_LUCKY_EGG":      ("LEARNING RATE", ["How large a step each lesson",
                                              "takes. Turned up: the holder",
                                              "earns more EXP. POINTS."]),
    "ITEM_SCOPE_LENS":     ("LONG TAIL",     ["The far end of a distribution,",
                                              "where the rare large values are.",
                                              "Raises the critical-hit ratio."]),
    "ITEM_SHELL_BELL":     ("RECLAIM",       ["Takes back what is no longer in",
                                              "use. The holder recovers HP on",
                                              "striking."]),
    "ITEM_KINGS_ROCK":     ("BUBBLE",        ["A gap pushed into a pipeline",
                                              "where nothing issues. They",
                                              "may flinch."]),
    "ITEM_CHOICE_BAND":    ("HARD CODED",    ["One value, written in, with no",
                                              "way to pass another. Powers up",
                                              "one routine and allows no other."]),
    "ITEM_AMULET_COIN":    ("SURCHARGE",     ["Charged on top of the agreed",
                                              "rate. Doubles prize money if",
                                              "the holder took part."]),
    "ITEM_UP_GRADE":       ("SERVICE PACK",  ["Everything that was fixed",
                                              "since the release, in one",
                                              "bundle. Made by FOUNDRY CO."]),
    "ITEM_DRAGON_SCALE":   ("SCALING LAW",   ["What happens to a thing when",
                                              "you only make it bigger.",
                                              "A BACKPRESS may be holding it."]),

    # The ones that only work on one host. A device that fits nothing else is
    # still a configuration -- it just has a very short compatibility list.
    "ITEM_DEEP_SEA_TOOTH": ("DEEP FEATURE",  ["A representation learned far",
                                              "from the surface. It raises the",
                                              "SP. ATK stat."]),
    "ITEM_DEEP_SEA_SCALE": ("DEEP LAYER",    ["The layers nothing outside gets",
                                              "at directly. It raises the",
                                              "SP. DEF stat."]),
    "ITEM_SOUL_DEW":       ("INNER STATE",   ["An orb for CASTOR or POLYDEUCES.",
                                              "What it holds, nothing outside",
                                              "can read. Raises both SP. stats."]),
    "ITEM_LIGHT_BALL":     ("SUPPLY RAIL",   ["The line every other part draws",
                                              "from. Held by a SPIKE, it raises",
                                              "the SP. ATK stat."]),
    "ITEM_LUCKY_PUNCH":    ("FLUKE",         ["A result nothing predicted and",
                                              "nothing repeats. It raises",
                                              "UPTIME's critical-hit ratio."]),
    "ITEM_METAL_POWDER":   ("STRICT MODE",   ["Refuses anything it was not",
                                              "promised. It raises MOCK's",
                                              "DEFENSE stat."]),
    "ITEM_THICK_CLUB":     ("BARE METAL",    ["Nothing at all between you and",
                                              "the hardware. It raises",
                                              "ARTEFACT's and COREFILE's ATTACK."]),
    "ITEM_STICK":          ("OFF BY ONE",    ["The error at the edge that",
                                              "everything else survives. Raises",
                                              "EDGECASE's critical-hit ratio."]),
}


#  ---------------------------------------------------------------------------
#  THE USABLE ITEMS -- T-14. 1.6 named the ten that undo a STATE and stopped
#  there, which left the rest of the bag reading as Gen 3 wrote it. Same rule
#  as 1.6's: AN ITEM IS AN OPERATION, not medicine -- the thing you would
#  actually do to a process in that condition.
#
#  What is DELIBERATELY not here is the finding. 2.8's rule -- the pass that
#  renames what already lands makes the game worse -- takes out more than half
#  the bag: FRESH WATER, SODA POP and LEMONADE are drinks that ordinary people
#  buy from a machine; NUGGET, PEARL, STARDUST and the mushrooms are things you
#  sell; the MAIL, the BICYCLE, the TEA, the tickets and the keys are objects.
#  A world where every item is a computing pun is 5.3a's world with nobody in
#  it. The ones below are the ones you USE ON A DAEMON, and those are machine
#  operations in any reading.
USABLE = {
    # The repair ladder. HP is how much of the process is still running.
    "ITEM_POTION":       ("RECOVER",      ["Puts back a little of what was",
                                           "lost. Restores 20 HP."]),
    "ITEM_SUPER_POTION": ("DEEP RECOVER", ["Goes further in than the first",
                                           "one does. Restores 50 HP."]),
    "ITEM_HYPER_POTION": ("FULL RECOVER", ["Everything reachable, put back.",
                                           "Restores 200 HP."]),
    "ITEM_MAX_POTION":   ("REBUILD",      ["From nothing, rather than from",
                                           "where it got to. Restores all HP."]),

    # MP is a budget for running a routine, so putting it back is a charge.
    "ITEM_ETHER":        ("CHARGE",       ["Puts the budget back for one",
                                           "routine. Restores 10 MP."]),
    "ITEM_MAX_ETHER":    ("FULL CHARGE",  ["One routine, all of its budget.",
                                           "Restores that routine's MP."]),
    "ITEM_ELIXIR":       ("CHARGE ALL",   ["Every routine at once, a little",
                                           "each. Restores 10 MP to all."]),
    "ITEM_MAX_ELIXIR":   ("FULL RECHARGE",["Every routine, all of it.",
                                           "Restores the MP of every one."]),

    # The vitamins are six parts of a machine's spec, one per stat -- which is
    # the same joke vanilla tells with six nutrients, in the other domain.
    "ITEM_HP_UP":        ("MEMORY",       ["How much a daemon can hold before",
                                           "it stops. Raises base HP."]),
    "ITEM_PROTEIN":      ("WATTAGE",      ["How hard it can drive something.",
                                           "Raises base ATTACK."]),
    "ITEM_IRON":         ("SHIELDING",    ["What sits between it and what is",
                                           "arriving. Raises base DEFENSE."]),
    "ITEM_CARBOS":       ("CLOCK RATE",   ["How many times a second it gets",
                                           "to act. Raises base SPEED."]),
    "ITEM_CALCIUM":      ("BANDWIDTH",    ["How much it can push down one",
                                           "channel. Raises base SP. ATK."]),
    "ITEM_ZINC":         ("INSULATION",   ["What keeps the outside out.",
                                           "Raises base SP. DEF."]),
    "ITEM_RARE_CANDY":   ("INCREMENT",    ["Adds exactly one, which is what",
                                           "the word means. Raises the level."]),

    # Tuning is what you do to a parameter for one run and then undo.
    "ITEM_X_ATTACK":     ("TUNE ATTACK",  ["Turned up for this engagement",
                                           "only. Raises ATTACK in battle."]),
    "ITEM_X_DEFEND":     ("TUNE DEFENSE", ["Turned up for this engagement",
                                           "only. Raises DEFENSE in battle."]),
    "ITEM_X_SPEED":      ("TUNE SPEED",   ["Turned up for this engagement",
                                           "only. Raises SPEED in battle."]),
    "ITEM_X_ACCURACY":   ("TUNE AIM",     ["Turned up for this engagement",
                                           "only. Raises accuracy in battle."]),
    "ITEM_X_SPECIAL":    ("TUNE SP. ATK", ["Turned up for this engagement",
                                           "only. Raises SP. ATK in battle."]),
    "ITEM_DIRE_HIT":     ("TUNE CRIT",    ["Reaches further into the tail of",
                                           "the distribution. Raises the",
                                           "critical-hit ratio in battle."]),
    "ITEM_GUARD_SPEC":   ("LOCK STATS",   ["Nothing outside gets to change",
                                           "them. Blocks stat reduction for",
                                           "five turns."]),

    # Suppressing a signal is exactly what a REPEL does, and MUTE is already
    # the held item that does it permanently -- 1.6c.
    "ITEM_REPEL":        ("SUPPRESS",     ["Holds the channel quiet. Weak",
                                           "wild daemons stay away for 100",
                                           "steps."]),
    "ITEM_SUPER_REPEL":  ("LONG SUPPRESS",["The same, held longer. 200",
                                           "steps."]),
    "ITEM_MAX_REPEL":    ("MAX SUPPRESS", ["The same, held longest. 250",
                                           "steps."]),
    "ITEM_ESCAPE_ROPE":  ("EJECT",        ["Out, now, from wherever you are.",
                                           "Returns you to the last",
                                           "CHECKPOINT you used."]),
    "ITEM_POKE_DOLL":    ("DECOY",        ["Something else to attend to.",
                                           "Lets you DETACH from any wild",
                                           "daemon."]),

    # The four inputs were named in 1.x -- something to reason from, to search
    # through, to feel with, to learn from. These are the fifth and sixth.
    "ITEM_SUN_STONE":    ("EXPOSURE",     ["Simply being left in front of",
                                           "something, for long enough. Some",
                                           "daemons take a new form."]),
    "ITEM_MOON_STONE":   ("REFLECTION",   ["Light that came back, and the",
                                           "other meaning. Some daemons take",
                                           "a new form when given one."]),

    # A rod pulls something out of a store you cannot see into.
    "ITEM_OLD_ROD":      ("QUERY",        ["Asks a body of water what is in",
                                           "it. The answers are shallow."]),
    "ITEM_GOOD_ROD":     ("DEEP QUERY",   ["Asks the same question further",
                                           "down."]),
    "ITEM_SUPER_ROD":    ("FULL SCAN",    ["Reads the whole of it rather than",
                                           "asking. Slow, and it finds",
                                           "everything."]),

    # The three that were waiting for the obvious word.
    "ITEM_ITEMFINDER":   ("GREP",         ["Finds the thing that is there and",
                                           "not shown. Reports a hidden item",
                                           "nearby."]),
    "ITEM_TOWN_MAP":     ("SITEMAP",      ["Everywhere there is, and how they",
                                           "join. Viewable at any time."]),
    "ITEM_VS_SEEKER":    ("ROLL CALL",    ["Asks who is listening. USERS who",
                                           "want to engage answer. The",
                                           "battery charges as you walk."]),
    "ITEM_COIN_CASE":    ("TOKEN CASE",   ["Holds the tokens the GAME CORNER",
                                           "deals in. It holds up to 9,999."]),

    #  1.6 named the ten items that undo a STATE and stopped, and 1.6d named
    #  what is used ON A DAEMON. These four fell between the two passes: they
    #  are medicine in vanilla's reading and operations in ours, and the line
    #  1.6 already drew is the one that decides them. HEAL POWDER is HOTFIX --
    #  "bitter, cheap, works now, nobody is proud of it" -- so the bitter
    #  powder and the bitter root are the same joke at a different size, and
    #  the two that restart a HALTED daemon belong beside RESTART and REBOOT.
    #
    #  The drinks stay drinks. Nobody buys a bitter medicinal root for
    #  pleasure and everybody buys a LEMONADE, which is the whole difference.
    "ITEM_REVIVAL_HERB": ("COLD START",   ["Brought up from nothing rather",
                                           "than resumed. Restarts a HALTED",
                                           "daemon at full health."]),
    "ITEM_SACRED_ASH":   ("RESTART ALL",  ["Every halted daemon at once, and",
                                           "all of them whole."]),
    "ITEM_ENERGY_POWDER":("FIELD PATCH",  ["Applied where it broke, by",
                                           "whoever was standing there.",
                                           "Restores 50 HP."]),
    "ITEM_ENERGY_ROOT":  ("WORKAROUND",   ["Not the fix. The thing you do",
                                           "instead of the fix, and it works.",
                                           "Restores 200 HP."]),

    #  T-19. The package Ty hands you in the Warehouse, and 8.2a is exact that
    #  what is in it "is not written here and may never need to be" -- so the
    #  name must not describe the contents. A PAYLOAD is what a message
    #  actually carries as opposed to what routes it, which says the shape and
    #  nothing else. Repurposed from ITEM_LETTER: a Hoenn key item, referenced
    #  by nothing in this game, and already a letter.
    #
    #  PAYLOAD was the first answer and check_lexicon refused it: PARAS is
    #  already PAYLOAD, which is a better home for the word -- a thing that
    #  carries something else and did not choose to. An ENVELOPE wraps a
    #  message without being it, which is the same statement about shape.
    "ITEM_LETTER":       ("ENVELOPE",     ["Sealed. It is addressed, and it",
                                           "is not addressed to you."]),

    #  T-51. What the Owl signs (4.34, ruling 1 reversed on playtest). He said
    #  "I will put that in writing, and I will sign that too" and handed over
    #  nothing, so the scene promised a consequence and never showed one. Its
    #  contents are never shown, which is the part of the ruling that mattered.
    #  A PEER REVIEW is exactly what a scholar signs, and it answers the Review
    #  Board without saying so. Repurposed from ITEM_DEVON_GOODS: a Hoenn key
    #  item nothing in this game referenced, and already a sealed package.
    "ITEM_DEVON_GOODS":  ("PEER REVIEW",  ["Signed and sealed. Addressed to",
                                           "everyone who signed the first one."]),

    # T-20. 8.2a calls these the two halves of a bridge between systems built
    # apart, and a KEY PAIR is that, exactly and as a term of art: two halves
    # made together, useless singly, and one of them is the half you are
    # allowed to hand out. CELIO's machine wants both before it will talk to
    # anywhere else, which is what a handshake is.
    #
    # Which is which was decided by the plot rather than by taste. CORPUS
    # steals the SAPPHIRE -- so the SAPPHIRE is the private one, because
    # stealing a private key is a crime and stealing a public one is not.
    "ITEM_RUBY":         ("PUBLIC KEY",   ["One half of a pair made together.",
                                           "This is the half you are allowed",
                                           "to hand out."]),
    "ITEM_SAPPHIRE":     ("PRIVATE KEY",  ["The other half, and the one that",
                                           "matters. Nothing works any more",
                                           "once somebody else has it."]),

    # POKe FLUTE is INTERRUPT (1.6). These are the same idea, carried.
    "ITEM_BLUE_FLUTE":   ("WAKE TONE",    ["A tone that reaches something",
                                           "not scheduled. Ends SUSPENDED."]),
    "ITEM_YELLOW_FLUTE": ("CALM TONE",    ["A tone steady enough to work",
                                           "against. Ends THRASHING."]),
    "ITEM_RED_FLUTE":    ("CLEAR TONE",   ["A tone that cuts through a",
                                           "binding made without asking."]),
    "ITEM_BLACK_FLUTE":  ("LOW TONE",     ["Pitched under what wild daemons",
                                           "answer to. Fewer appear."]),
    "ITEM_WHITE_FLUTE":  ("HIGH TONE",    ["Pitched where wild daemons",
                                           "answer. More appear."]),
}
NAMED.update(USABLE)


#  ---------------------------------------------------------------------------
#  THE BERRIES -- T-13, and 1.6c derived the register without spending it: a
#  berry sits there doing nothing, fires ONCE when a condition is met, and is
#  gone. That is a HANDLER, and the word for the kind installed against a
#  machine condition is a TRAP -- which is also a physical thing that catches
#  something, so it does the double duty CHERI and PECHA never did.
#
#  Which makes the pouch a TRAP TABLE, and that is the term for the array of
#  handlers a system installs, so the container names itself.
#
#  T-14's rule decides the scope here too. A berry is USED ON A DAEMON, so
#  unlike the drinks it is not a thing a person owns -- it is an operation
#  waiting to happen. The twenty-two that only "can be ground up into a powder
#  as an ingredient for medicine" have no effect, no use in this game and no
#  way to obtain one; they are left alone, which is 2.10's reachability rule.
BERRIES = {
    # The six states, each with the handler that catches it. 1.6 named the
    # items that undo one on purpose; these are the same undo, armed.
    "ITEM_CHERI_BERRY":  ("THROTTLE TRAP",["Armed against one condition and",
                                           "spent on it. Ends THROTTLED,",
                                           "once."]),
    "ITEM_CHESTO_BERRY": ("SUSPEND TRAP", ["Fires the moment the daemon stops",
                                           "being scheduled. Ends SUSPENDED,",
                                           "once."]),
    "ITEM_PECHA_BERRY":  ("LEAK TRAP",    ["Catches a slow loss before it",
                                           "compounds. Ends LEAKING, once."]),
    "ITEM_RAWST_BERRY":  ("HEAT TRAP",    ["Fires on heat the daemon made",
                                           "itself. Ends OVERHEATED, once."]),
    "ITEM_ASPEAR_BERRY": ("HANG TRAP",    ["Fires when nothing else will.",
                                           "Ends HUNG, once."]),
    "ITEM_PERSIM_BERRY": ("THRASH TRAP",  ["Catches a daemon making no",
                                           "progress against itself. Ends",
                                           "THRASHING, once."]),
    "ITEM_LUM_BERRY":    ("CATCH ALL",    ["The handler that takes whatever",
                                           "arrives. Ends any state, once."]),
    "ITEM_LEPPA_BERRY":  ("EXHAUST TRAP", ["Fires when a routine runs out of",
                                           "budget. Restores 10 MP, once."]),

    # A watermark is the level at which a handler fires, which is exactly what
    # these do -- and the two of them are the two marks.
    "ITEM_ORAN_BERRY":   ("LOW MARK",     ["The level at which something is",
                                           "done about it. Restores 10 HP",
                                           "when health falls, once."]),
    "ITEM_SITRUS_BERRY": ("HIGH MARK",    ["The same idea, set higher and",
                                           "worth more. Restores 30 HP when",
                                           "health falls, once."]),
    "ITEM_BERRY_JUICE":  ("RESERVE",      ["Held back for the moment it is",
                                           "needed. Restores 20 HP."]),

    # The five that fix it and may make something else worse. Flavour is the
    # mechanic -- each upsets a different nature -- so the flavour stays.
    "ITEM_FIGY_BERRY":   ("SPICY TRAP",   ["Restores health, and may leave a",
                                           "daemon THRASHING. Which is which",
                                           "depends on the daemon."]),
    "ITEM_WIKI_BERRY":   ("DRY TRAP",     ["Restores health, and may leave a",
                                           "daemon THRASHING. Which is which",
                                           "depends on the daemon."]),
    "ITEM_MAGO_BERRY":   ("SWEET TRAP",   ["Restores health, and may leave a",
                                           "daemon THRASHING. Which is which",
                                           "depends on the daemon."]),
    "ITEM_AGUAV_BERRY":  ("BITTER TRAP",  ["Restores health, and may leave a",
                                           "daemon THRASHING. Which is which",
                                           "depends on the daemon."]),
    "ITEM_IAPAPA_BERRY": ("SOUR TRAP",    ["Restores health, and may leave a",
                                           "daemon THRASHING. Which is which",
                                           "depends on the daemon."]),

    # AUTO is TUNE that fires without you, which is the whole of the
    # difference between an item you use and an item you hold.
    "ITEM_LIECHI_BERRY": ("AUTO ATTACK",  ["Turns itself up when there is",
                                           "little left. Raises ATTACK in a",
                                           "pinch."]),
    "ITEM_GANLON_BERRY": ("AUTO DEFENSE", ["Turns itself up when there is",
                                           "little left. Raises DEFENSE in a",
                                           "pinch."]),
    "ITEM_SALAC_BERRY":  ("AUTO SPEED",   ["Turns itself up when there is",
                                           "little left. Raises SPEED in a",
                                           "pinch."]),
    "ITEM_PETAYA_BERRY": ("AUTO SP. ATK", ["Turns itself up when there is",
                                           "little left. Raises SP. ATK in a",
                                           "pinch."]),
    "ITEM_APICOT_BERRY": ("AUTO SP. DEF", ["Turns itself up when there is",
                                           "little left. Raises SP. DEF in a",
                                           "pinch."]),
    "ITEM_LANSAT_BERRY": ("AUTO CRIT",    ["Reaches further into the tail",
                                           "when there is little left. Raises",
                                           "the critical-hit ratio."]),
    "ITEM_STARF_BERRY":  ("AUTO ANY",     ["Turns one of them sharply up, and",
                                           "does not say which. Raises a",
                                           "random stat in a pinch."]),

    "ITEM_BERRY_POUCH":  ("TRAP TABLE",   ["Where the handlers are installed.",
                                           "It attaches to the POOL's pocket",
                                           "for important items."]),
}
NAMED.update(BERRIES)


#  ---------------------------------------------------------------------------
#  T-526 (2026-11-07) -- DRAFT, every line, and NOTHING here reaches the engine until the user approves it.
#  A sweep of all 376 rows of items.json for what still reads as FireRed's: a Hoenn place, a POKeMON plural the
#  vocabulary pass took as singular, a type or verb it missed, or vanilla's object where the item is ours. 2.10's
#  reachability rule decided the scope: a row is drafted when the player can hold the item (a map, a mart, a
#  gift, a holiday in daemons_holidays.h, a wild daemon's held item); the Hoenn items nothing hands out are left
#  as they are. docs/t526-item-descriptions-draft.md is the table; `--sheet OUT.png` draws it in the BAG's font.
#
#      python3 tools/port_item_text.py --write --approved ITEM [ITEM ...]   # write ONLY those drafts' descriptions
#      python3 tools/port_item_text.py --write --approved                   # every row in T526_APPROVED
#
#  An approved row goes into T526_APPROVED as well, so the whole-table --write below writes it too rather than
#  putting the old words back. Names are untouched: only description_english moves.
#  2026-11-07, building it: the whole-table --write had fallen behind the engine on 16 rows written after it last ran
#  (TM06/13/14/24/25/35/36/38/42 rewritten, the 'they' pass on DITHER, DITHER TRIM and BUBBLE, the species renames
#  in INNER STATE, SCALING LAW and BARE METAL, POOL in TRAP TABLE). Those rows were brought into the tables above
#  as the engine has them, so a plain --write now changes nothing -- and main() reports any row it would move.
T526 = {
    "ITEM_COIN_CASE":    (["A token spends only where it was",
                           "issued. Holds the GAME CORNER's",
                           "COINS, up to 9,999."],
                          "it said 'tokens', and the GAME CORNER deals in COINS"),
    "ITEM_SS_TICKET":    (["Passage on the S.S. ANNE, at",
                           "ARDOR CITY. Made out to HOLT,",
                           "who gave it to you instead."],
                          "vanilla's ferry ticket; HOLT gives it, and it was his invitation"),
    "ITEM_BIKE_VOUCHER": (["One BICYCLE, owed to whoever",
                           "holds this. The BIKE SHOP in",
                           "DOLDRUM CITY pays it out."],
                          "vanilla's instruction, town renamed and nothing else"),
    "ITEM_LAVA_COOKIE":  (["A cookie baked on hot stone, sold",
                           "on TWO ISLAND. Ends every state",
                           "of one DAEMON."],
                          "LAVARIDGE TOWN is Hoenn's; TWO ISLAND sells it, and 'status problems' are states"),
    "ITEM_RED_SCARF":    (["A red scarf, handed out on",
                           "PARADE DAYS. It changes nothing",
                           "in battle. It is worn for the day."],
                          "CONTESTS are Hoenn's; PARADE DAYS hands it out (the user: name the day), and it does nothing"),
    "ITEM_BLUE_SCARF":   (["A blue scarf, handed out on",
                           "PARADE DAYS. It changes nothing",
                           "in battle. It is worn for the day."],
                          "CONTESTS are Hoenn's; PARADE DAYS hands it out (the user: name the day), and it does nothing"),
    "ITEM_PINK_SCARF":   (["A pink scarf, like the ones handed",
                           "out on PARADE DAYS. It changes",
                           "nothing in battle."],
                          "CONTESTS are Hoenn's; nothing hands this one out, so it names the day its set comes from"),
    "ITEM_GREEN_SCARF":  (["A green scarf, handed out on",
                           "CLOVER DAY and PARADE DAYS. It",
                           "changes nothing in battle."],
                          "CONTESTS are Hoenn's; CLOVER DAY and PARADE DAYS hand it out (the user: name the day), and it does nothing"),
    "ITEM_YELLOW_SCARF": (["A yellow scarf, handed out on",
                           "PARADE DAYS. It changes nothing",
                           "in battle. It is worn for the day."],
                          "CONTESTS are Hoenn's; PARADE DAYS hands it out (the user: name the day), and it does nothing"),
    "ITEM_NET_BALL":     (["A somewhat different BOX that",
                           "works especially well on",
                           "FLOW- and SWARM-type DAEMONS."],
                          "WATER is FLOW; the plural was read as one"),
    "ITEM_NEST_BALL":    (["A somewhat different BOX that",
                           "works especially well on weaker",
                           "DAEMONS."],
                          "the plural was read as one"),
    "ITEM_REPEAT_BALL":  (["A somewhat different BOX that",
                           "works especially well on DAEMONS",
                           "bound before."],
                          "the plural was read as one"),
    "ITEM_DIVE_BALL":    (["A somewhat different BOX that",
                           "works especially well on DAEMONS",
                           "deep in the sea."],
                          "the plural was read as one (nothing hands it out; drafted with its set)"),
    "ITEM_LUXURY_BALL":  (["A comfortable BOX that makes a",
                           "bound wild DAEMON quickly grow",
                           "friendly."],
                          "'captured' is the one capture verb the vocabulary pass never had"),
    "ITEM_RETRO_MAIL":   (["A piece of MAIL featuring a print",
                           "of three cute DAEMONS. It is to",
                           "be held by a DAEMON."],
                          "the plural was read as one"),
    "ITEM_SUBTLE_LAYER": (["THE SUBTLE LAYER. A USER's",
                           "handbook of the craft: read,",
                           "write and link."],
                          "TRAINER is USER everywhere else; the book's cover says 'a trainer's handbook' too"),
    #  The TRAP TABLE's description window is two lines (src/berry_pouch.c, window 1: 200x32, FONT_NORMAL at y=2), so
    #  a third line was never seen (T-525 batch 3, qa 7Nov2026 T525 22). The user, 2026-11-07: "Rewrite to 2 lines".
    "ITEM_CHERI_BERRY":  (["Armed against one condition, spent",
                           "on it. Ends THROTTLED, once."],
                          "THROTTLE TRAP: 'once.' fell to a third line the TRAP TABLE never shows"),
    "ITEM_CHESTO_BERRY": (["Fires when the daemon stops being",
                           "scheduled. Ends SUSPENDED, once."],
                          "SUSPEND TRAP: 'once.' fell to a third line"),
    "ITEM_PERSIM_BERRY": (["Catches a daemon working against",
                           "itself. Ends THRASHING, once."],
                          "THRASH TRAP: 'THRASHING, once.' fell to a third line"),
    "ITEM_ORAN_BERRY":   (["A mark set low. When health falls,",
                           "it restores 10 HP, once."],
                          "LOW MARK: 'when health falls, once.' fell to a third line"),
    "ITEM_SITRUS_BERRY": (["The same, set higher. When health",
                           "falls, it restores 30 HP, once."],
                          "HIGH MARK: 'health falls, once.' fell to a third line"),
    "ITEM_FIGY_BERRY":   (["Restores health. Whether it causes",
                           "THRASHING depends on the daemon."],
                          "SPICY TRAP: 'depends on the daemon.' fell to a third line"),
    "ITEM_WIKI_BERRY":   (["Restores health. Whether it causes",
                           "THRASHING depends on the daemon."],
                          "DRY TRAP: the same"),
    "ITEM_MAGO_BERRY":   (["Restores health. Whether it causes",
                           "THRASHING depends on the daemon."],
                          "SWEET TRAP: the same"),
    "ITEM_AGUAV_BERRY":  (["Restores health. Whether it causes",
                           "THRASHING depends on the daemon."],
                          "BITTER TRAP: the same"),
    "ITEM_IAPAPA_BERRY": (["Restores health. Whether it causes",
                           "THRASHING depends on the daemon."],
                          "SOUR TRAP: the same"),
}
#  The rows the TRAP TABLE shows, in its two-line window: each checked at two lines, and drawn so by --trap-sheet.
T526_TWO_LINES = ["ITEM_CHERI_BERRY", "ITEM_CHESTO_BERRY", "ITEM_PERSIM_BERRY", "ITEM_ORAN_BERRY", "ITEM_SITRUS_BERRY",
                  "ITEM_FIGY_BERRY", "ITEM_WIKI_BERRY", "ITEM_MAGO_BERRY", "ITEM_AGUAV_BERRY", "ITEM_IAPAPA_BERRY"]
#  Their three-line words as they stood before, kept for the sheet's NOW column (NAMED is overwritten just below).
T526_BEFORE = {k: list(NAMED[k][1]) for k in T526_TWO_LINES}
#  The user approves rows by name. The user, 2026-11-07: "Build all 16" -- every row above, with SUBTLE LAYER's
#  USER (the book's cover follows: gensubtle.py, bookpdf.py), HOLT's ticket and the cookie's hot stone kept, and the
#  scarves naming the day. The ten TRAP TABLE rows: the user, "Rewrite to 2 lines", 2026-11-07. Still DRAFT words,
#  every one.
T526_APPROVED = list(T526)
for _k in T526_APPROVED:
    TEXT[_k] = T526[_k][0]
    if _k in NAMED:
        NAMED[_k] = (NAMED[_k][0], T526[_k][0])


def _t526_sheet(out, engine_items, measure, trap=False):
    """Current against draft, in the engine's latin_normal sheet at its own pixels, one row per draft: the BAG's
    description window is 200x48 (src/bag.c, window 1) and the text starts at y=3, so that is what is drawn. With
    trap, the TRAP TABLE's rows in ITS window -- 200x32 (src/berry_pouch.c, window 1), text at y=2, two lines, so a
    third line is cut as the game cuts it -- at real size (1x) and at 3x."""
    from PIL import Image, ImageDraw, ImageFont
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import fontwidth
    font = Image.open(os.path.join(GBA, "graphics/fonts/latin_normal.png"))
    w, cm = fontwidth.font(GBA)
    fp = font.load()
    PAPER, INK, SHADOW, EDGE = (255, 255, 255), (98, 98, 98), (213, 213, 205), (232, 120, 120)
    H, TOP = (32, 2) if trap else (48, 3)

    def pane(lines):
        im = Image.new("RGB", (200, H), PAPER)
        px = im.load()
        for row, s in enumerate(lines[:3]):
            x, y = 0, TOP + row * 14
            for ch in s:
                b = cm.get(ch)
                if b is None:
                    continue
                gx, gy = (b % 16) * 16, (b // 16) * 16
                for yy in range(16):
                    for xx in range(min(16, w[b])):
                        v = fp[gx + xx, gy + yy]
                        if 0 <= x + xx < 200 and 0 <= y + yy < H and v in (1, 2):
                            px[x + xx, y + yy] = INK if v == 1 else SHADOW
                x += w[b]
        for yy in range(0, H, 2):                       # the 198px budget, dotted
            px[198, yy] = EDGE
        return im

    try:
        label = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
    except Exception:
        label = ImageFont.load_default()
    LEFT = 150
    scales = (1, 3) if trap else (2,)
    keys = list(T526_TWO_LINES) if trap else [k for k in T526 if k not in T526_TWO_LINES]
    ROW = max(H * max(scales), 40) + 18
    cols = [(sc, which) for sc in scales for which in ("NOW", "DRAFT")]
    xs, x = [], LEFT
    for sc, _ in cols:
        xs.append(x)
        x += 200 * sc + 16
    sheet = Image.new("RGB", (x + 8, 44 + len(keys) * ROW), (28, 30, 36))
    d = ImageDraw.Draw(sheet)
    d.text((8, 6), ("T-526 TRAP TABLE descriptions, DRAFT -- its own font and 200x32 window (two lines), at 1x (real "
                    "size) and 3x. NOW is cut where the game cuts it." if trap else
                    "T-526 item descriptions, DRAFT -- the BAG's own font and 200x48 window, at 2x. Left: the engine "
                    "now. Right: the draft.") + " Dotted: the 198px budget.", fill=(220, 220, 224), font=label)
    for (sc, which), cx in zip(cols, xs):
        d.text((cx, 24), "%s %dx" % (which, sc), fill=(240, 200, 120) if which == "DRAFT" else (160, 160, 170),
               font=label)
    for i, k in enumerate(keys):
        y = 40 + i * ROW
        it = engine_items[k]
        d.text((8, y + 4), it["english"], fill=(230, 230, 234), font=label)
        d.text((8, y + 20), k.replace("ITEM_", ""), fill=(140, 140, 150), font=label)
        new = T526[k][0]
        #  the engine's words before T-526 wrote them: once written, NOW would show the draft twice
        now = T526_BEFORE.get(k, it["description_english"].split("\\n"))
        d.text((8, y + 36), "%dpx max" % max(measure(l) for l in new), fill=(140, 140, 150), font=label)
        for (sc, which), cx in zip(cols, xs):
            sheet.paste(pane(now if which == "NOW" else new).resize((200 * sc, H * sc), Image.NEAREST), (cx, y))
    sheet.save(out)
    print("  sheet: %s (%d rows)" % (out, len(keys)))


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
textwidth = None

def main():
    global textwidth
    textwidth = _pixels()
    rc = 0
    TEXT.update({k: v[1] for k, v in NAMED.items()})

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
    #  Names are thirteen characters -- ITEM_NAME_LENGTH is 14 and the terminator
    #  takes one. check_lexicon.py owns the collision half; this owns the budget.
    NAME_MAX = 13
    for item_id, (name, _lines) in NAMED.items():
        if len(name) > NAME_MAX:
            print("  !! %s: name %d chars > %d -- %s" % (item_id, len(name), NAME_MAX, name)); rc = 1
            continue
        pat = re.compile(r'("english": ")([^"]*)("(?:[^{}]*?)"itemId": "%s")' % re.escape(item_id))
        raw, n = pat.subn(lambda m: m.group(1) + name + m.group(3), raw, count=1)
        if not n:
            print("  !! %s name anchor not found" % item_id); rc = 1

    print("  %d descriptions, widest %dpx of %d" % (len(TEXT), widest, BUDGET))
    print("  %d held items named" % len(NAMED))

    #  T-526: the drafts are measured on every run, and written only as --write --approved names them.
    engine_items = {it["itemId"]: it for it in json.loads(open(PATH).read())["items"]}
    def _measure(ln):
        return textwidth(ln) if textwidth else len(ln) * 6
    for item_id, (lines, _why) in T526.items():
        if item_id not in engine_items:
            print("  !! T-526 %s not in items.json" % item_id); rc = 1
        if len(lines) > 3:
            print("  !! T-526 %s: %d lines > 3" % (item_id, len(lines))); rc = 1
        if item_id in T526_TWO_LINES and len(lines) > 2:
            print("  !! T-526 %s: %d lines > 2, and the TRAP TABLE shows two" % (item_id, len(lines))); rc = 1
        for ln in lines:
            if _measure(ln) > BUDGET:
                print("  !! T-526 %s: %dpx > %d -- %s" % (item_id, _measure(ln), BUDGET, ln)); rc = 1
    held = [k for k in T526 if engine_items.get(k, {}).get("description_english") == "\\n".join(T526[k][0])]
    print("  T-526: %d DRAFT descriptions, %d approved, %d in the engine" % (len(T526), len(T526_APPROVED), len(held)))
    if "--sheet" in sys.argv:
        _t526_sheet(sys.argv[sys.argv.index("--sheet") + 1], engine_items, _measure)
    if "--trap-sheet" in sys.argv:
        _t526_sheet(sys.argv[sys.argv.index("--trap-sheet") + 1], engine_items, _measure, trap=True)

    if "--approved" in sys.argv:
        named = []
        for a in sys.argv[sys.argv.index("--approved") + 1:]:
            if a.startswith("--"):
                break
            named.append(a if a.startswith("ITEM_") else "ITEM_" + a)
        named = named or list(T526_APPROVED)
        unknown = [k for k in named if k not in T526]
        if unknown:
            print("  !! --approved names rows T-526 does not hold: %s" % " ".join(unknown)); sys.exit(1)
        if not named:
            print("  --approved names no rows, and none is approved yet: nothing written.")
            sys.exit(rc)
        if "--write" not in sys.argv or rc:
            print("  would write %d T-526 rows: %s" % (len(named), " ".join(named)))
            sys.exit(rc)
        #  ONLY those rows' descriptions, read fresh from the engine, so nothing else in the file moves.
        raw = open(PATH).read()
        for item_id in named:
            body = json.dumps("\\n".join(T526[item_id][0]))[1:-1]
            pat = re.compile(r'("itemId": "%s".*?"description_english": ")(.*?)(")' % re.escape(item_id), re.S)
            raw, n = pat.subn(lambda m: m.group(1) + body + m.group(3), raw, count=1)
            if not n:
                print("  !! %s not found" % item_id); sys.exit(1)
        tmp = PATH + ".tmp"
        open(tmp, "w").write(raw)
        os.replace(tmp, PATH)
        print("  written: %d T-526 rows -- add them to T526_APPROVED so a whole-table --write keeps them" % len(named))
        sys.exit(0)

    #  T-526: the whole-table write is level with the engine (the TM lines, the 'they' pass, the species renames and
    #  POOL were brought back into the tables above, 2026-11-07), so it changes nothing when the engine is right -- and
    #  a report says so, exiting 1 when it would not, which is how check_generators sees this tool drift again.
    current = open(PATH).read()
    if "--write" in sys.argv and rc == 0:
        if raw != current:
            tmp = PATH + ".tmp"
            open(tmp, "w").write(raw)
            os.replace(tmp, PATH)
            print("  written")
        else:
            print("  nothing to write: the engine is what this table makes")
    elif raw != current and rc == 0:
        now = {it["itemId"]: it for it in json.loads(current)["items"]}
        made = {it["itemId"]: it for it in json.loads(raw)["items"]}
        moved = sorted(k for k in made if made[k] != now.get(k))
        print("  !! the engine is not what this table makes: %d row%s would change (%s) -- bring the table level, or --write"
              % (len(moved), "" if len(moved) == 1 else "s", " ".join(moved[:8]) + (" ..." if len(moved) > 8 else "")))
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())

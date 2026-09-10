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
    "ITEM_SHARP_BEAK":     ("VECTOR GAIN",   ["A direction in a space of",
                                              "meanings. Gain lifts one",
                                              "channel: this one is VECTOR."]),
    "ITEM_POISON_BARB":    ("CORRUPT GAIN",  ["Data that has been tampered",
                                              "with. Gain lifts one channel:",
                                              "this one is CORRUPT."]),
    "ITEM_SOFT_SAND":      ("STRATUM GAIN",  ["The layer everything else runs",
                                              "on. Gain lifts one channel:",
                                              "this one is STRATUM."]),
    "ITEM_HARD_STONE":     ("LEGACY GAIN",   ["Deprecated hardware, still",
                                              "running. Gain lifts one channel:",
                                              "this one is LEGACY."]),
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

    # The rest of the desk.
    "ITEM_BRIGHT_POWDER":  ("DITHER",        ["Noise added on purpose, so that",
                                              "nothing can be pinned exactly.",
                                              "The foe's aim slips."]),
    "ITEM_LAX_INCENSE":    ("DITHER TRIM",   ["Dither, at a lower setting.",
                                              "The foe's aim slips a little."]),
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
                                              "where nothing issues. The foe",
                                              "may flinch."]),
    "ITEM_CHOICE_BAND":    ("HARD CODED",    ["One value, written in, with no",
                                              "way to pass another. Powers up",
                                              "one routine and allows no other."]),
    "ITEM_AMULET_COIN":    ("SURCHARGE",     ["Charged on top of the agreed",
                                              "rate. Doubles prize money if",
                                              "the holder took part."]),
    "ITEM_UP_GRADE":       ("SERVICE PACK",  ["Everything that was fixed since",
                                              "the release, in one bundle.",
                                              "Made by SILPH CO."]),
    "ITEM_DRAGON_SCALE":   ("SCALING LAW",   ["What happens to a thing when",
                                              "you only make it bigger.",
                                              "A JETSTREAM may be holding it."]),

    # The ones that only work on one host. A device that fits nothing else is
    # still a configuration -- it just has a very short compatibility list.
    "ITEM_DEEP_SEA_TOOTH": ("DEEP FEATURE",  ["A representation learned far",
                                              "from the surface. It raises the",
                                              "SP. ATK stat."]),
    "ITEM_DEEP_SEA_SCALE": ("DEEP LAYER",    ["The layers nothing outside gets",
                                              "at directly. It raises the",
                                              "SP. DEF stat."]),
    "ITEM_SOUL_DEW":       ("INNER STATE",   ["An orb for a LATIOS or LATIAS.",
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
                                              "the hardware. It raises RELIC's",
                                              "and CAIRNLING's ATTACK stat."]),
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

    #  T-19. The package Ty hands you in the Warehouse, and 8.2a is exact that
    #  what is in it "is not written here and may never need to be" -- so the
    #  name must not describe the contents. A PAYLOAD is what a message
    #  actually carries as opposed to what routes it, which says the shape and
    #  nothing else. Repurposed from ITEM_LETTER: a Hoenn key item, referenced
    #  by nothing in this game, and already a letter.
    "ITEM_LETTER":       ("PAYLOAD",      ["Sealed. It is addressed, and it",
                                           "is not addressed to you."]),

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
                                           "It attaches to the BAG's pocket",
                                           "for important items."]),
}
NAMED.update(BERRIES)

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
if "--write" in sys.argv and rc == 0:
    open(PATH, "w").write(raw); print("  written")
sys.exit(rc)

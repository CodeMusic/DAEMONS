#!/usr/bin/env python3
"""Rename the six process states, the items that undo them, and two menu words.

    python3 tools/port_states.py [--write]

WHY THESE ARE NOT MEDICAL WORDS. Vanilla leaves a creature poisoned, asleep,
paralysed, burned, frozen or confused, and every one of those is a BODILY
metaphor. This game has no bodies -- it has processes, and 1.4 already shipped
HALTED for fainting, which sets the register: a state is something a process is
IN, and something it can be got out of. Each name below is the ordinary
computing word for what the mechanic actually does, so it explains itself the
first time it is read.

    poison      LEAKING     a memory leak is the only thing in computing that
                            costs you a fixed slice per tick
    bad poison  CASCADING   a cascading failure is precisely a fault whose rate
                            rises because of the damage it already did
    sleep       SUSPENDED   not gone, not scheduled, and it RESUMES
    paralysis   THROTTLED   a speed cap that intermittently stalls work --
                            both halves of paralysis in one word
    burn        OVERHEATED  chip damage plus reduced output, dealt by ENTROPY,
                            whose clause is "noise and heat"
    freeze      HUNG        FROZEN could not be reused: it is a type name, and
                            2.6 just spent effort making those carry meaning
    confusion   THRASHING   a system so busy managing itself it makes no
                            progress and damages its own throughput

THE ITEMS ARE OPERATIONS, NOT MEDICINE. PATCH passes 1's does-it-work-twice
test without a beat of confusion -- you patch a leak and you patch software --
which is the standard CACHE was held to. RESTART and REBOOT come with their
ladder already built: the bigger item is the bigger operation.

TWO MENU WORDS, AND THE PORT UNLOCKED ONE. 1.4 wanted INVOKE for FIGHT --
"you bind() a daimon and you invoke it, both idioms true twice over" -- and
refused it on width: six characters where the Game Boy's left column fits five.
The GBA menu is pixel-addressed at CLEAR_TO 56 and already ships DAEMON in that
column. INVOKE measures 36px, exactly DAEMON's width. The objection is gone.

MOVES BECOME ROUTINES, and the rename is one string. Eleven player-visible
strings contain "MOVE" and most are the VERB -- MOVE ITEMS, MOVE TO BAG,
{DPAD_ANY}MOVE all mean relocate and must stay. Same trap as "catchy tune".
"""
import json, os, re, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA   = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

MSG   = os.path.join(GBA, "src/battle_message.c")
STR   = os.path.join(GBA, "src/strings.c")
ITEMS = os.path.join(GBA, "src/data/items.json")

#  Battle messages. Whole strings, because the grammar moves with the noun --
#  "was poisoned" and "started leaking" are not the same sentence shape.
LINES = [
 ("But {B_DEF_NAME_WITH_PREFIX} can't\\nsleep in an UPROAR!",
  "But {B_DEF_NAME_WITH_PREFIX} can't\\nsuspend in an UPROAR!"),
 ("It hurt itself in its\\nconfusion!",            "It hurt itself\\nthrashing!"),
 ("The DAEMON hearing the FLUTE\\nawoke!",         "The DAEMON hearing the FLUTE\\nresumed!"),
 ("a POISON move",                                 "a CORRUPT move"),
 ("{B_ATK_NAME_WITH_PREFIX} became\\nconfused due to fatigue!",
  "{B_ATK_NAME_WITH_PREFIX} began\\nthrashing from fatigue!"),
 ("{B_ATK_NAME_WITH_PREFIX} ignored\\norders while asleep!",
  "{B_ATK_NAME_WITH_PREFIX} ignored\\norders while suspended!"),
 ("{B_ATK_NAME_WITH_PREFIX} is fast\\nasleep.",    "{B_ATK_NAME_WITH_PREFIX} is\\nsuspended."),
 ("{B_ATK_NAME_WITH_PREFIX} is hurt\\nby its burn!",
  "{B_ATK_NAME_WITH_PREFIX} is hurt\\nby the heat!"),
 ("{B_ATK_NAME_WITH_PREFIX} is hurt\\nby poison!",
  "{B_ATK_NAME_WITH_PREFIX} is hurt\\nby the leak!"),
 ("{B_ATK_NAME_WITH_PREFIX} is paralyzed!\\nIt can't move!",
  "{B_ATK_NAME_WITH_PREFIX} is throttled!\\nIt can't act!"),
 ("{B_ATK_NAME_WITH_PREFIX} is\\nalready asleep!",
  "{B_ATK_NAME_WITH_PREFIX} is\\nalready suspended!"),
 ("{B_ATK_NAME_WITH_PREFIX} is\\nconfused!",       "{B_ATK_NAME_WITH_PREFIX} is\\nthrashing!"),
 ("{B_ATK_NAME_WITH_PREFIX} is\\nfrozen solid!",   "{B_ATK_NAME_WITH_PREFIX} is\\nhung!"),
 ("{B_ATK_NAME_WITH_PREFIX} snapped\\nout of confusion!",
  "{B_ATK_NAME_WITH_PREFIX} stopped\\nthrashing!"),
 ("{B_ATK_NAME_WITH_PREFIX} went\\nto sleep!",     "{B_ATK_NAME_WITH_PREFIX} was\\nsuspended!"),
 ("{B_ATK_NAME_WITH_PREFIX} woke up!",             "{B_ATK_NAME_WITH_PREFIX} resumed!"),
 ("{B_ATK_NAME_WITH_PREFIX} woke up\\nin the UPROAR!",
  "{B_ATK_NAME_WITH_PREFIX} resumed\\nin the UPROAR!"),
 ("{B_DEF_NAME_WITH_PREFIX} already\\nhas a burn.",
  "{B_DEF_NAME_WITH_PREFIX} is already\\noverheated."),
 ("{B_DEF_NAME_WITH_PREFIX} is already\\npoisoned.",
  "{B_DEF_NAME_WITH_PREFIX} is already\\nleaking."),
 ("{B_DEF_NAME_WITH_PREFIX} is\\nalready asleep!",
  "{B_DEF_NAME_WITH_PREFIX} is\\nalready suspended!"),
 ("{B_DEF_NAME_WITH_PREFIX} is\\nalready confused!",
  "{B_DEF_NAME_WITH_PREFIX} is\\nalready thrashing!"),
 ("{B_DEF_NAME_WITH_PREFIX} is\\nalready paralyzed!",
  "{B_DEF_NAME_WITH_PREFIX} is\\nalready throttled!"),
 ("{B_DEF_NAME_WITH_PREFIX} was\\nhealed of paralysis!",
  "{B_DEF_NAME_WITH_PREFIX} is no\\nlonger throttled!"),
 ("{B_DEF_NAME_WITH_PREFIX}'s {B_DEF_ABILITY}\\nprevents confusion!",
  "{B_DEF_NAME_WITH_PREFIX}'s {B_DEF_ABILITY}\\nprevents thrashing!"),
 ("{B_EFF_NAME_WITH_PREFIX} became\\nconfused!",   "{B_EFF_NAME_WITH_PREFIX} started\\nthrashing!"),
 ("{B_EFF_NAME_WITH_PREFIX} is badly\\npoisoned!", "{B_EFF_NAME_WITH_PREFIX} is\\ncascading!"),
 ("{B_EFF_NAME_WITH_PREFIX} is paralyzed!\\nIt may be unable to move!",
  "{B_EFF_NAME_WITH_PREFIX} is throttled!\\nIt may stall!"),
 ("{B_EFF_NAME_WITH_PREFIX} was burned!",          "{B_EFF_NAME_WITH_PREFIX} overheated!"),
 ("{B_EFF_NAME_WITH_PREFIX} was\\nfrozen solid!",  "{B_EFF_NAME_WITH_PREFIX}\\nhung!"),
 ("{B_EFF_NAME_WITH_PREFIX}'s {B_DEF_ABILITY}\\nprevents paralysis!",
  "{B_EFF_NAME_WITH_PREFIX}'s {B_DEF_ABILITY}\\nprevents throttling!"),
 ("{B_EFF_NAME_WITH_PREFIX}'s {B_DEF_ABILITY}\\nprevents poisoning!",
  "{B_EFF_NAME_WITH_PREFIX}'s {B_DEF_ABILITY}\\nprevents leaks!"),
 ("{B_EFF_NAME_WITH_PREFIX}'s {B_EFF_ABILITY}\\nprevents burns!",
  "{B_EFF_NAME_WITH_PREFIX}'s {B_EFF_ABILITY}\\nprevents overheating!"),
 ("{B_EFF_NAME_WITH_PREFIX}\\nfell asleep!",       "{B_EFF_NAME_WITH_PREFIX}\\nwas suspended!"),
 ("{B_EFF_NAME_WITH_PREFIX}\\nwas poisoned!",      "{B_EFF_NAME_WITH_PREFIX}\\nstarted leaking!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\ncured paralysis!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\nlifted the throttle!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\ncured poison!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\npatched the leak!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\nhealed its burn!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\ncooled it down!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\nsnapped it out of confusion!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\nstopped the thrashing!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\nwoke it from its sleep!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_LAST_ITEM}\\nresumed it!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\nburned {B_EFF_NAME_WITH_PREFIX}!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\noverheated {B_EFF_NAME_WITH_PREFIX}!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\nfroze {B_EFF_NAME_WITH_PREFIX} solid!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\nhung {B_EFF_NAME_WITH_PREFIX}!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\nmade {B_EFF_NAME_WITH_PREFIX} sleep!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\nsuspended {B_EFF_NAME_WITH_PREFIX}!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\nparalyzed {B_EFF_NAME_WITH_PREFIX}!\\lIt may be unable to move!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\nthrottled {B_EFF_NAME_WITH_PREFIX}!\\lIt may stall!"),
 ("{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\npoisoned {B_EFF_NAME_WITH_PREFIX}!",
  "{B_SCR_ACTIVE_NAME_WITH_PREFIX}'s {B_SCR_ACTIVE_ABILITY}\\nleft {B_EFF_NAME_WITH_PREFIX} leaking!"),
 #  the bare status nouns, which the summary screen prints
 ('_("sleep")',     '_("suspended")'),
 ('_("poison")',    '_("leaking")'),
 ('_("burn")',      '_("overheated")'),
 ('_("paralysis")', '_("throttled")'),
 ('_("ice")',       '_("hung")'),
 ('_("confusion")', '_("thrashing")'),
 #  two menu words
 ("{PALETTE 5}{COLOR_HIGHLIGHT_SHADOW 13 14 15}FIGHT{CLEAR_TO 56}BAG\\nDAEMON{CLEAR_TO 56}DETACH",
  "{PALETTE 5}{COLOR_HIGHLIGHT_SHADOW 13 14 15}INVOKE{CLEAR_TO 56}BAG\\nDAEMON{CLEAR_TO 56}DETACH"),
]

#  strings.c, because the summary page name lives there rather than with the
#  battle text. POKESUM_WIN_PAGE_NAME is 13 tiles -- 104px -- with the printer
#  starting at x=4, so the budget is 100. KNOWN ROUTINES measures 84 and keeps
#  the parallel with DAEMON INFO and DAEMON SKILLS; ROUTINES alone would have
#  been safer and needlessly so.
STRINGS = [("KNOWN MOVES", "KNOWN ROUTINES")]

#  english -> ours. Descriptions are rewritten separately, because the vanilla
#  ones say "a spray-type medicine" and none of these is medicine.
ITEM_NAMES = {
    "ANTIDOTE":     ("PATCH",     "Seals a LEAK. The same word for a hole and for the fix."),
    "AWAKENING":    ("RESUME",    "Puts a SUSPENDED DAEMON back on the schedule."),
    "PARLYZ HEAL":  ("PRIORITY",  "Lifts a THROTTLE by scheduling the DAEMON ahead."),
    "BURN HEAL":    ("COOLANT",   "Cools an OVERHEATED DAEMON back to full output."),
    "ICE HEAL":     ("INTERRUPT", "Reaches a HUNG DAEMON, which nothing else does."),
    "FULL HEAL":    ("ROLLBACK",  "Returns a DAEMON to a known-good state. Clears everything."),
    "FULL RESTORE": ("SNAPSHOT",  "Restores a DAEMON whole: health and state together."),
    "REVIVE":       ("RESTART",   "Brings back a HALTED DAEMON at half its health."),
    "MAX REVIVE":   ("REBOOT",    "Brings back a HALTED DAEMON at full health."),
    "HEAL POWDER":  ("HOTFIX",    "Bitter, cheap, and it works now. Clears every state."),
}

LEFTOVERS = re.compile(
    r'_\("[^"]*\b(poison|poisoned|poisoning|asleep|sleep|sleeping|paraly\w*|'
    r'burn|burned|burns|frozen|froze|thaw\w*|confus\w*|woke|awoke)\b', re.I)



#  ---- pass 2: everywhere else the states and the items are named ----
#
#  ORDER MATTERS AND IT IS THE WHOLE TRICK. "POISON" is a TYPE (-> CORRUPT) and
#  "poisoned" is a STATE (-> leaking), so the multi-word item names go first,
#  then the type words, then the bare states. Reversing that turns POISON HEAL
#  into LEAKING HEAL and the CORRUPT type into the LEAKING type.
#
#  AND AN ESCAPE IS TWO CHARACTERS WHOSE FIRST IS A LETTER. In "\nPoisoned" the
#  n sits against the P, so \b finds no word boundary and every word at the
#  start of a line is invisible to a pattern looking for it. That has hidden
#  substitutions in three tools in this project already, so these patterns are
#  matched against a FLATTENED copy and applied by offset.
PASS2_FILES = [
    "src/move_descriptions.c",
    "src/data/text/teachy_tv.h",
    "data/text/help_system.inc",
]

ITEM_WORDS = [
    ("FULL RESTORE", "SNAPSHOT"), ("FULL HEAL", "ROLLBACK"),
    ("PARLYZ HEAL", "PRIORITY"),  ("BURN HEAL", "COOLANT"),
    ("ICE HEAL", "INTERRUPT"),    ("HEAL POWDER", "HOTFIX"),
    ("MAX REVIVE", "REBOOT"),     ("ANTIDOTES", "PATCHES"),
    ("ANTIDOTE", "PATCH"),        ("AWAKENINGS", "RESUMES"),
    ("AWAKENING", "RESUME"),      ("REVIVES", "RESTARTS"),
    ("REVIVE", "RESTART"),        ("KNOWN MOVES", "KNOWN ROUTINES"),
]

#  Only where the word is unmistakably the TYPE. Bare "POISON" is left alone
#  because it is as often the state; 1.2 already holds nineteen type lines for 5.
TYPE_WORDS = [
    ("POISON-type", "CORRUPT-type"), ("POISON type", "CORRUPT type"),
    ("POISON move", "CORRUPT move"), ("POISON moves", "CORRUPT moves"),
]

STATE_WORDS = [
    ("badly poisoned", "cascading"), ("Badly poisoned", "Cascading"),
    ("poisoning", "leaking"),  ("Poisoning", "Leaking"),
    ("poisoned", "leaking"),   ("Poisoned", "Leaking"),
    ("paralyzed", "throttled"),("Paralyzed", "Throttled"),
    ("paralysis", "throttling"),("Paralysis", "Throttling"),
    ("paralyze", "throttle"),  ("Paralyze", "Throttle"),
    ("asleep", "suspended"),   ("Asleep", "Suspended"),
    ("confused", "thrashing"), ("Confused", "Thrashing"),
    ("confusion", "thrashing"),("Confusion", "Thrashing"),
    ("frozen", "hung"),        ("Frozen", "Hung"),
    ("freeze", "hang"),        ("Freeze", "Hang"),
    ("burned", "overheated"),  ("Burned", "Overheated"),
    #  the bare nouns, longest phrase first. "burn" is only ever a noun in
    #  these files -- inflict/suffer/cause/with a burn -- and never the verb.
    ("inflict a burn", "cause overheating"), ("suffer a burn", "overheat"),
    ("cause a burn", "cause overheating"),   ("with a burn", "with overheating"),
    ("a burn", "overheating"),   ("deep sleep", "deep suspension"),
    ("induces sleep", "induces suspension"),
    ("prevents sleep", "prevents suspension"),
    ("to sleep", "into suspension"),
    ("sleep", "suspension"),     ("Sleep", "Suspension"),
    ("burn", "overheating"),     ("Burn", "Overheating"),
]

#  Two lines the word pass makes too wide for the box, rewritten rather than
#  truncated. Measured against sFontNormalLatinGlyphWidths: 210px and 220px
#  against a 196px box, versus 141 and 190 for these.
OVERRIDES = [
    ("weaken it with throttling or suspension", "throttle it or suspend it"),
    ("Overheating: HP loss and lowers ATTACK.", "Overheating: HP loss, less ATTACK."),
]


def flatten(t):
    """Escapes become two spaces so \\b works and every offset is preserved."""
    return re.sub(r"\\[a-zA-Z]", "  ", t)

def pass2(report):
    total = 0
    for rel in PASS2_FILES:
        f = os.path.join(GBA, rel)
        if not os.path.isfile(f):
            print("  %-30s missing" % rel); continue
        t = load(f); n = 0
        for old, new in ITEM_WORDS + TYPE_WORDS + STATE_WORDS:
            pat = re.compile(r"\b%s\b" % re.escape(old))
            flat = flatten(t)
            spans = [m.span() for m in pat.finditer(flat)]
            for a, b in reversed(spans):
                t = t[:a] + new + t[b:]
                n += 1
        for old, new in OVERRIDES:
            if old in t:
                t = t.replace(old, new); n += 1
        if n:
            print("  %-30s %3d" % (rel, n))
            report.append((f, t))
        total += n
    return total


def load(p):
    return open(p, encoding="utf-8").read()


def main():
    msg, n = load(MSG), 0
    for old, new in LINES:
        if old in msg:
            msg = msg.replace(old, new); n += 1
        elif new not in msg:
            print("  !! not found and not already done: %.60s" % old)
    print("  battle_message.c   %d of %d strings" % (n, len(LINES)))

    st, sn = load(STR), 0
    for old, new in STRINGS:
        if old in st:
            st = st.replace(old, new); sn += 1
    print("  strings.c          %d of %d strings" % (sn, len(STRINGS)))

    raw = load(ITEMS)
    items = json.loads(raw)
    items = items if isinstance(items, list) else next(v for v in items.values() if isinstance(v, list))
    hits = 0
    for it in items:
        e = it.get("english", "")
        if e in ITEM_NAMES:
            name, desc = ITEM_NAMES[e]
            it["english"] = name
            it["description_english"] = desc
            hits += 1
    print("  items.json         %d of %d renamed" % (hits, len(ITEM_NAMES)))

    pending = []
    print("  --- pass 2, the rest of the game ---")
    pass2(pending)

    left = sorted(set(m.group(0) for m in LEFTOVERS.finditer(msg)))
    if left:
        print("  still naming a bodily state (%d):" % len(left))
        for s in left[:12]:
            print("     %s" % s[:70])
    else:
        print("  no bodily-state words left in battle_message.c")

    if not WRITE:
        print("\n  (report only; pass --write)")
        return
    open(MSG, "w", encoding="utf-8").write(msg)
    open(STR, "w", encoding="utf-8").write(st)
    for f, t in pending:
        open(f, "w", encoding="utf-8").write(t)
    doc = json.loads(raw)
    if isinstance(doc, list):
        doc = items
    else:
        for k, v in doc.items():
            if isinstance(v, list):
                doc[k] = items
    json.dump(doc, open(ITEMS, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("\n  written")


if __name__ == "__main__":
    main()

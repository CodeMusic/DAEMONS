#!/usr/bin/env python3
"""T-36: does a daemon's routine list read as things THAT daemon would do?

    python3 tools/gbacoherence.py                 # the faults, worst first
    python3 tools/gbacoherence.py --all           # every daemon, as a card
    python3 tools/gbacoherence.py ECHO HEAP       # just these, as cards

2.7a did three lines out of seventy-two by hand and found the seam: the
thirteen retyped daemons were 78% off-type against a 45% baseline. This is the
other sixty-nine, and the question has moved on. OFF-TYPE PERCENTAGE IS NOT THE
FAULT -- 45% is what coverage IS, and a daemon reaching outside itself and
being worse at it is a thing the engine already says through same-type attack
bonus.

WHAT A TOOL CAN AND CANNOT DO. Whether ECHO invoking REFLECT reads right is a
judgement; nothing here can make it. So this does not score coherence. It finds
the three faults that ARE computable and are exactly what 2.7a found by hand,
and then it gets out of the way and prints the list for a human to read.

    SILENT TYPE   a daemon has a type and knows NOT ONE routine of it. This is
                  the fault 2.7a found on ROVERBYTE: GROWTH/SIGNAL, and the
                  SIGNAL half never appeared in a single routine. A type the
                  creature never uses is a label, not a design.

    NO STAB       every damaging routine it knows is off-type, so the same-type
                  bonus never fires. Mechanically it is a daemon that is worse
                  at everything it does than the chart says it should be.

    MIXED SIGNAL  before level 10 the daemon does something TYPED, it is the
                  wrong type, and it never does its own. A player meets a
                  creature there and the first thing it does teaches them what
                  it is -- so being taught a type it does not have is worse
                  than being taught nothing.

    LATE TYPE     it does have a damaging routine of its own type, and the
                  routine does not arrive until after level 25. The label is
                  right and the player waits most of the game to see it.

THIN OPENING WAS THE FIRST TRY AT THIS AND IT CRIED WOLF. It read "everything
before level 10 is off-type" and flagged 41 daemons, and 22 of them were
flagged for opening with WRITE, FLIP or PUSH. Those are TACKLE, SCRATCH and
POUND, and 2.8 SETTLED THEM ON PURPOSE: "WRITE is the plainest operation there
is and every daemon can do it -- damage in this world is putting your data
where theirs was." A check that fires on a thing the design decided is not
measuring the design, it is arguing with it.

So CONTENT is excluded from MIXED SIGNAL by ruling rather than by exception.
2.8 makes CONTENT the type that hands you no verb, the neutral instruction set
every daemon performs; opening with it says nothing false about the creature.
Opening with SOMEBODY ELSE'S type does.

Two more things the first version got wrong, both found by reading its output:

  * it counted DAMAGING routines only, so a daemon opening with an on-type
    STATUS routine looked silent. DAMPEN at level 1 on a FLOW daemon is the
    creature saying what it is. MIXED SIGNAL still counts damage, because the
    fault is about what a player is TAUGHT by watching it attack -- but
    LATE TYPE's threshold was set knowing this, not in ignorance of it.

  * it fired even when an on-type routine sat in the same window. A daemon
    that opens with one of each is being taught correctly and the off-type
    one is coverage, which is what 2.7b said off-type is FOR.

The percentage is still printed, because it is the cheapest way to spot a line
that drifted -- but it is reported, never ranked on.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
ALL  = "--all" in sys.argv
EARLY = 10          # "before level 10" -- the window a player meets it in
LATE  = 25          # past here, the label has been waiting most of the game
#  2.8: the type that hands you no verb. Opening with it says nothing false.
NEUTRAL = "CONTENT"

#  Flags that are CORRECT and should stop reporting. Same device as
#  check_lexicon's ALLOWED and for the same reason: a report carrying permanent
#  known-noise stops being read, and the day it stops being read is the day a
#  real flag hides in it. A name here is a ruling, not a dismissal, so each one
#  carries why -- and the entry names the FLAG, so a daemon exempted for one
#  fault still reports the other two.
EXEMPT = {
    ("STUB", "SILENT TYPE"):
        "4.26 -- a placeholder that does nothing, until it does. A stub knowing "
        "no routine of its own type IS the joke",
    ("STUB", "NO STAB"):
        "same joke, stated in the numbers",
    ("CRAWLER", "NO STAB"):
        "a larva with one attack is the genre's oldest shape, and it evolves at "
        "7. It knows BACKLOG, so SWARM is not silent -- only its one DAMAGING "
        "routine is off-type",
    ("PENDING", "SILENT TYPE"):
        "a cocoon. Knows PIN twice and nothing else; there is no routine to "
        "make on-type",
    ("BUFFER", "SILENT TYPE"):
        "the other cocoon, same reason",
    ("SLURP", "MIXED SIGNAL"):
        "LICK is the daemon's NAME as a verb, and vanilla types that routine "
        "LATENT on a creature that is not. Swapping it for a CONTENT primitive "
        "would fix the report and delete the creature. 2.8's own counter-test "
        "cuts this way: the routine IS the thing itself here",

    #  T-46. Three daemons know exactly ONE routine between them, and in all
    #  three cases the single routine is the creature. An on-type second
    #  routine would clear the flag and cost more than the flag is worth.
    ("SYMBOL", "SILENT TYPE"):
        "it knows one routine, PRIOR, and PRIOR's type is decided by the "
        "individual carrying it. The tool reads the table's base type and sees "
        "CONTEXT unused; in play it is whatever this one turned out to be. A "
        "daemon called SYMBOL whose only routine means something different in "
        "every copy is the joke, and it is vanilla's joke sharpened rather "
        "than ours invented",
    ("SYMBOL", "NO STAB"):
        "same single routine, stated in the numbers",
    ("REPAY", "SILENT TYPE"):
        "it knows one routine, PRESENT, which helps or harms at random -- "
        "vanilla's own one-move creature, and 8.2b's name is built on it: "
        "'the amounts have never matched and it keeps coming.' Giving it a "
        "FROZEN routine would make it a competent ice type and delete a gift "
        "nobody can predict",
    ("REPAY", "NO STAB"):
        "same single routine, stated in the numbers",
    ("PREMISE", "SILENT TYPE"):
        "it knows one routine, WRITE, and becomes three different daemons "
        "depending on how it grew -- which is what a premise does. 2.7f named "
        "it for the argument triad on exactly that reading, so an on-type "
        "second routine would be arguing with the name",
    ("PREMISE", "NO STAB"):
        "same single routine, stated in the numbers",
}


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8", errors="ignore").read()


def upstream(rel):
    """Vanilla's copy, so 'ours' is DERIVED rather than listed here."""
    out = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel],
                         capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else ""


def load():
    tn = dict(re.findall(r'\[TYPE_(\w+)\]\s*=\s*_\("(\w+)"\)', read("src/battle_main.c")))

    names = dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]+)"\)',
                            read("src/data/text/species_names.h")))
    van = dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]+)"\)',
                          upstream("src/data/text/species_names.h")))
    ours = {k for k in names if van.get(k) != names[k]}

    info = read("src/data/pokemon/species_info.h")
    types = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{(?:[^{}]|\{[^{}]*\})*?"
                         r"\.types\s*=\s*\{\s*TYPE_(\w+),\s*TYPE_(\w+)", info, re.S):
        # a single-type daemon lists the same type twice; dict.fromkeys keeps order
        types[m.group(1)] = list(dict.fromkeys(
            [tn.get(m.group(2), m.group(2)), tn.get(m.group(3), m.group(3))]))

    mn = dict(re.findall(r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]+)"\)',
                         read("src/data/text/move_names.h")))
    mv = read("src/data/battle_moves.h")
    mt, mp = {}, {}
    for b in re.finditer(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \}", mv, re.S):
        d = dict(re.findall(r"\.(\w+)\s*=\s*([A-Za-z0-9_]+)", b.group(2)))
        mt[b.group(1)] = tn.get(d.get("type", "").replace("TYPE_", ""), "?")
        mp[b.group(1)] = int(d.get("power", "0"))

    ls = read("src/data/pokemon/level_up_learnsets.h")
    learn = {}
    for b in re.finditer(r"s(\w+)LevelUpLearnset\[\]\s*=\s*\{(.*?)\};", ls, re.S):
        learn[b.group(1).upper()] = [
            (int(lv), mid) for lv, mid in
            re.findall(r"LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)", b.group(2))]

    return names, ours, types, mn, mt, mp, learn


def main():
    names, ours, types, mn, mt, mp, learn = load()
    key = {k.replace("_", ""): k for k in names}

    rows = []
    for upper, moves in learn.items():
        k = key.get(upper)
        if not k or k not in ours or k not in types:
            continue
        mine = types[k]
        dmg = [(lv, m) for lv, m in moves if mp.get(m, 0) > 0]
        off = [(lv, m) for lv, m in dmg if mt.get(m) not in mine]
        early = [(lv, m) for lv, m in dmg if lv <= EARLY]
        silent = [t for t in mine if not any(mt.get(m) == t for _, m in moves)]
        #  wrong: early, damaging, and typed as something it is NOT -- with
        #  CONTENT excluded by 2.8's ruling rather than by exception.
        wrong = [(lv, m) for lv, m in early
                 if mt.get(m) not in mine and mt.get(m) != NEUTRAL]
        right = [(lv, m) for lv, m in early if mt.get(m) in mine]
        on = [lv for lv, m in dmg if mt.get(m) in mine]
        rows.append({
            "name": names[k], "types": mine, "moves": moves, "dmg": dmg, "off": off,
            "silent": silent, "wrong": wrong,
            "nostab": bool(dmg) and len(off) == len(dmg),
            #  an on-type routine in the same window means the player IS being
            #  taught correctly, and the off-type one is coverage (2.7b)
            "mixed": bool(wrong) and not right,
            "late": min(on) if on and min(on) > LATE else None,
            #  None, not 0. A daemon with no damaging routine at all -- PENDING
            #  knows PIN twice and nothing else -- reported as "0% off-type",
            #  which reads as a clean sheet and is the opposite of the truth.
            "pct": round(100 * len(off) / len(dmg)) if dmg else None,
        })

    def card(r):
        print("\n  %-12s %s" % (r["name"], "/".join(r["types"])))
        for lv, m in r["moves"]:
            t = mt.get(m, "?")
            mark = "  " if t in r["types"] else " ·"
            pw = ("%3d" % mp[m]) if mp.get(m, 0) else "  —"
            print("   %s %3d  %-14s %-9s %s" % (mark, lv, mn.get(m, m), t, pw))
        flags = []
        if r["silent"]:  flags.append("SILENT TYPE: " + ", ".join(r["silent"]))
        if r["nostab"]:  flags.append("NO STAB")
        if r["mixed"]:
            flags.append("MIXED SIGNAL: " + ", ".join(
                "%s@%d is %s" % (mn.get(m, m), lv, mt.get(m)) for lv, m in r["wrong"]))
        if r["late"]:    flags.append("LATE TYPE: first on-type at %d" % r["late"])
        if flags:
            print("      !! " + " · ".join(flags))

    if ARGS:
        want = {a.upper() for a in ARGS}
        for r in sorted(rows, key=lambda r: r["name"]):
            if r["name"].upper() in want:
                card(r)
        return 0

    if ALL:
        for r in sorted(rows, key=lambda r: r["name"]):
            card(r)
        return 0

    print("  %d of our daemons have a learnset and a type\n" % len(rows))
    excused = 0
    for label, fault, pick in (
        ("SILENT TYPE  — has the type, knows not one routine of it",
         "SILENT TYPE", lambda r: r["silent"]),
        ("NO STAB      — every damaging routine is off-type",
         "NO STAB", lambda r: r["nostab"]),
        ("MIXED SIGNAL — before level %d it does something typed, it is the wrong\n"
         "                 type, and it never does its own" % EARLY,
         "MIXED SIGNAL", lambda r: r["mixed"] and not r["nostab"]),
        ("LATE TYPE    — its first on-type damaging routine arrives after level %d" % LATE,
         "LATE TYPE", lambda r: r["late"] and not r["silent"]),
    ):
        flagged = [r for r in rows if pick(r)]
        excused += sum(1 for r in flagged if (r["name"], fault) in EXEMPT)
        hit = sorted([r for r in flagged if (r["name"], fault) not in EXEMPT],
                     key=lambda r: (r["pct"] is not None, r["pct"] or 0), reverse=True)
        print("  %s" % label)
        if not hit:
            print("     none\n")
            continue
        for r in hit:
            if fault == "MIXED SIGNAL":
                extra = " — " + ", ".join("%s@%d is %s" % (mn.get(m, m), lv, mt.get(m))
                                          for lv, m in r["wrong"])
            elif fault == "LATE TYPE":
                extra = " — first on-type at %d" % r["late"]
            else:
                extra = (" — " + ", ".join(r["silent"])) if r["silent"] else ""
            pct = "  no damaging routine" if r["pct"] is None else "%3d%% off-type" % r["pct"]
            print("     %-12s %-18s %s%s" % (r["name"], "/".join(r["types"]), pct, extra))
        print()

    if excused:
        print("  %d flag(s) excused, each with a ruling:" % excused)
        for (who, fault), why in sorted(EXEMPT.items()):
            print("     %-10s %-13s %s" % (who, fault, why))
        print()

    tot_off = sum(len(r["off"]) for r in rows)
    tot_dmg = sum(len(r["dmg"]) for r in rows)
    print("  off-type overall: %d of %d damaging routines (%d%%) — 2.7a's baseline is 45%%"
          % (tot_off, tot_dmg, round(100 * tot_off / max(tot_dmg, 1))))
    print("  read a daemon with:  python3 tools/gbacoherence.py ECHO HEAP MUTEX")
    return 0


sys.exit(main())

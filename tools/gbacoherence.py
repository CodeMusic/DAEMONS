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

    THIN OPENING  the routines it has BEFORE level 10 are all off-type. A
                  player meets the daemon there, and the first three things it
                  does are what teaches them what it is.

The percentage is still printed, because it is the cheapest way to spot a line
that drifted -- but it is reported, never ranked on.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
ALL  = "--all" in sys.argv
EARLY = 10          # "before level 10" -- the window a player meets it in


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
        rows.append({
            "name": names[k], "types": mine, "moves": moves, "dmg": dmg, "off": off,
            "silent": silent,
            "nostab": bool(dmg) and len(off) == len(dmg),
            "thin": bool(early) and all(mt.get(m) not in mine for _, m in early),
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
        if r["thin"]:    flags.append("THIN OPENING")
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
    for label, pick in (
        ("SILENT TYPE  — has the type, knows not one routine of it",
         lambda r: r["silent"]),
        ("NO STAB      — every damaging routine is off-type",
         lambda r: r["nostab"]),
        ("THIN OPENING — everything before level %d is off-type" % EARLY,
         lambda r: r["thin"] and not r["nostab"]),
    ):
        hit = sorted([r for r in rows if pick(r)],
                     key=lambda r: (r["pct"] is not None, r["pct"] or 0), reverse=True)
        print("  %s" % label)
        if not hit:
            print("     none\n")
            continue
        for r in hit:
            extra = (" — " + ", ".join(r["silent"])) if r["silent"] else ""
            pct = "  no damaging routine" if r["pct"] is None else "%3d%% off-type" % r["pct"]
            print("     %-12s %-18s %s%s" % (r["name"], "/".join(r["types"]), pct, extra))
        print()

    tot_off = sum(len(r["off"]) for r in rows)
    tot_dmg = sum(len(r["dmg"]) for r in rows)
    print("  off-type overall: %d of %d damaging routines (%d%%) — 2.7a's baseline is 45%%"
          % (tot_off, tot_dmg, round(100 * tot_off / max(tot_dmg, 1))))
    print("  read a daemon with:  python3 tools/gbacoherence.py ECHO HEAP MUTEX")
    return 0


sys.exit(main())

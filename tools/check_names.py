#!/usr/bin/env python3
"""T-49: does a name assert something its OWN TABLE contradicts?

    python3 tools/check_names.py            # the contradictions, or nothing
    python3 tools/check_names.py --rulings  # and the exemptions, with reasons

EVERY OTHER CHECK IN THIS REPO COMPARES NAMES TO OTHER NAMES. check_lexicon
finds collisions, vowel-drops and stale prose; gbacoherence reads a daemon's
ROUTINE LIST against its type. Nothing has ever read a NAME against the row it
sits on, which is the axis "some of these feel like generic renames" is about.

IT FIRES ON CONTRADICTION ONLY, and that bound is 2.6's, word for word:

    A contradicting clause is worse than a silent one. Silence costs a
    lookup. A contradiction costs trust in the chart -- and the chart is
    the argument.

So a move called PRUNE that deals flat damage is SILENT and is fine. A move
called REINFORCE that lowers the target's DEFENSE is a contradiction. The
first costs a player one lookup; the second teaches them the wrong thing and
then makes them distrust the next name too.

AND THE OTHER BOUND IS 2.8'S. WRITE, FLIP and PUSH are TACKLE, SCRATCH and
POUND, and 2.8 settled them on purpose -- "damage in this world is putting
your data where theirs was." gbacoherence's first version flagged 41 daemons
and 22 of them were flagged for exactly that. A check that fires on a thing
the design decided is not measuring the design, it is arguing with it. So
PLAINNESS IS NEVER A FAULT HERE. Only a name that says the wrong thing is.

Three faults, each computable:

  DIRECTION   the name states a direction and the effect goes the other way.
              REINFORCE lowering the target's DEFENSE was the worst of them:
              its DESCRIPTION had doubled down, reading "adds more of what was
              already holding" in front of an effect that takes armour away.

  TYPE WORD   a daemon's name is a TYPE's own word -- the type name, or a
              noun from that type's 2.6 clause -- and the daemon is not that
              type. NOISE is ENTROPY's clause ("noise and heat") and was on a
              CONTENT daemon.

  DISPLACED   a name we chose is a VANILLA name for a DIFFERENT entity, so a
              player who knows the source game reads it as that thing. CHARM
              was on SWEET KISS while vanilla's CHARM was our DOWNCLOCK --
              two moves, and the wrong one answered to the name.

Every exemption is a RULING with its reason in the table below, never a
silent skip -- the same shape gbacoherence uses, for the same reason: an
exemption nobody can read is indistinguishable from a bug.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GBA  = os.path.join(os.path.dirname(HERE), "engineGba")
SHOW_RULINGS = "--rulings" in sys.argv

#  A type's own words: the type name, plus the nouns from its 2.6 one-clause
#  test. These are the words that make a reader predict a type.
TYPE_WORDS = {
    "ENTROPY":  ["NOISE", "HEAT", "DISORDER"],
    #  FAULT is deliberately NOT here. STRATUM owns the COMPOUNDS -- HARD FAULT,
    #  PAGE FAULT, SEGFAULT -- and not the bare noun, so the FLOW daemon called
    #  FAULT is not wearing STRATUM's word. 4.26 reads FAULT and HANDLER as "the
    #  thing it needs is not loaded; and the thing that catches that", which
    #  AGREES with the memory reading and disagrees only about the type. That is
    #  the chart's business, not the name's -- and a ruling that can never fire
    #  is worse than no entry, so this is a comment and not an exemption.
    "STRATUM":  ["SUBSTRATE", "LAYER"],
    "FLOW":     ["DOWNHILL"],
    "LOGIC":    ["PROOF"],
    "LATENT":   ["UNOBSERVED"],
    "FROZEN":   ["LOCKED"],
    "GROWTH":   ["TRAINING"],
    "CORRUPT":  ["TAMPERED"],
    "SIGNAL":   ["CURRENT"],
    "SWARM":    ["AGENTS"],
    "CONTEXT":  ["FRAME", "SUSPEND", "SUSPENDED"],
    "VECTOR":   ["DIRECTION"],
    "LEGACY":   ["DEPRECATED"],
    "HARDENED": ["RESIST"],
    "OPAQUE":   [],
    "EMERGENT": [],
    "CONTENT":  [],
    "ORACLE":   [],
}

RAISES = {"REINFORCE", "FORTIFY", "TEMPER", "RALLY", "INLINE", "BRACKET", "ELECT",
          "ATTEST", "PROMOTE", "SPINUP", "BUILDUP", "ESCALATE", "AMPLIFY", "BOOST",
          "HARDEN", "SHIELD", "STRENGTHEN", "UPCLOCK"}
LOWERS = {"DEMOTE", "DOWNCLOCK", "DEPRECATE", "REDUCE", "SCATTER", "CLOG", "DISSOLVE",
          "PRUNE", "REDACT", "AUDIT", "EXPOSE", "DEGRADE", "THROTTLE", "SHRINK",
          "DILUTE", "CORRODE", "WEAKEN"}

#  RULINGS. Each is a place the check WOULD fire and a reason it should not.
#  The reason is the point: a reader has to be able to disagree with it.
RULINGS = {
    ("SUBSTRATE", "TYPE WORD"):
        "4.25, on purpose. SUBSTRATE was the original name for the STRATUM TYPE and was "
        "cut at nine characters; the species then took the word. Its ability is INHERITS "
        "-- the substrate takes on whatever runs on it -- which is the Index entry as a "
        "mechanic, and 1.6c's TRACE note depends on it.",
    ("SUSPEND", "TYPE WORD"):
        "The name is a VERB IT PERFORMS, not a type claim. It is the sleep ladder's middle "
        "rung under STANDBY, and what it does to other daemons is suspend them. 2.7's "
        "question is who owns the STATE; a daemon that inflicts one is not claiming to be "
        "the type that owns it.",
}


def _named(path, key):
    return dict(re.findall(rf'\[{key}_(\w+)\]\s*=\s*_\("([^"]+)"\)',
                           open(os.path.join(GBA, path)).read()))


def main():
    moves   = _named("src/data/text/move_names.h", "MOVE")
    species = _named("src/data/text/species_names.h", "SPECIES")
    types   = dict(re.findall(r'\[TYPE_(\w+)\] = _\("(\w+)"\)',
                              open(os.path.join(GBA, "src/battle_main.c")).read()))
    battle  = dict(re.findall(r'\[MOVE_(\w+)\] =\s*\{(.*?)\n\s*\},',
                              open(os.path.join(GBA, "src/data/battle_moves.h")).read(), re.S))
    info    = dict(re.findall(r'\[SPECIES_(\w+)\] =\s*\n\s*\{(.*?)\n\s*\},',
                              open(os.path.join(GBA, "src/data/pokemon/species_info.h")).read(), re.S))

    def upstream(path, key):
        out = subprocess.run(["git", "-C", GBA, "show", f"upstream/master:{path}"],
                             capture_output=True, text=True).stdout
        return dict(re.findall(rf'\[{key}_(\w+)\]\s*=\s*_\("([^"]+)"\)', out))

    van_moves   = upstream("src/data/text/move_names.h", "MOVE")
    van_species = upstream("src/data/text/species_names.h", "SPECIES")

    faults, excused = [], []

    def record(kind, name, detail):
        (excused if (name, kind) in RULINGS else faults).append((kind, name, detail))

    #  DIRECTION -- the name states one way and the effect goes the other.
    for mv, nm in moves.items():
        body = battle.get(mv)
        if not body:
            continue
        ef = (re.search(r'\.effect\s*=\s*(\w+)', body) or [None, ''])[1]
        words = set(re.split(r'[^A-Z]+', nm))
        if "_UP" in ef and (words & LOWERS):
            record("DIRECTION", nm, f"{ef[7:]} raises, and the name says it lowers")
        if "_DOWN" in ef and (words & RAISES):
            record("DIRECTION", nm, f"{ef[7:]} lowers, and the name says it raises")

    #  TYPE WORD -- a daemon wearing another type's vocabulary.
    for sp, body in info.items():
        nm = species.get(sp)
        if not nm or nm == van_species.get(sp):
            continue
        m = re.search(r'\.types\s*=\s*\{TYPE_(\w+),\s*TYPE_(\w+)\}', body)
        if not m:
            continue
        mine = {types.get(m.group(1)), types.get(m.group(2))}
        words = set(re.split(r'[^A-Z]+', nm))
        for ty, extra in TYPE_WORDS.items():
            if ty in mine:
                continue
            for word in [ty] + extra:
                if word in words:
                    record("TYPE WORD", nm, f"is {'/'.join(sorted(x for x in mine if x))}, "
                                            f"and {word} is {ty}'s own word")
                    break

    #  DISPLACED -- our name is vanilla's name for something else.
    for ours, vans, label in ((moves, van_moves, "move"), (species, van_species, "daemon")):
        pool = {v.replace("é", "e").upper() for v in vans.values()}
        for key, nm in ours.items():
            if nm == vans.get(key) or nm.startswith("?") or "$" in nm:
                continue
            if nm.replace("é", "e").upper() in pool:
                owner = [k for k, v in vans.items() if v.replace("é", "e").upper() == nm.upper()]
                if owner and owner[0] != key:
                    record("DISPLACED", nm,
                           f"vanilla's {nm} is {label} {owner[0]}, and we put the name on {key}")

    order = {"DIRECTION": 0, "TYPE WORD": 1, "DISPLACED": 2}
    faults.sort(key=lambda f: (order[f[0]], f[1]))
    if faults:
        print(f"  {len(faults)} name(s) contradict their own table:\n")
        for kind, nm, detail in faults:
            print(f"     {nm:14} {kind:10} {detail}")
    else:
        print("  no name contradicts its own table.")

    if excused or SHOW_RULINGS:
        print(f"\n  {len(excused)} ruling(s)" + ("" if SHOW_RULINGS else " -- see --rulings"))
        if SHOW_RULINGS:
            for kind, nm, detail in sorted(excused, key=lambda f: f[1]):
                print(f"\n     {nm} -- {kind}")
                print(f"       would fire: {detail}")
                for line in RULINGS[(nm, kind)].split(". "):
                    print(f"       {line.strip().rstrip('.')}.")
    return 1 if faults else 0


if __name__ == "__main__":
    raise SystemExit(main())

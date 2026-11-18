#!/usr/bin/env python3
"""T-490 step 3: CONTACT IS PHYSICAL, applied to the routines step 2 left as candidates. DRAFT.

    python3 tools/gbasplit.py                       # report: every routine the rule would move, and the judgement calls
    python3 tools/gbasplit.py --write --approved    # write APPROVED into engineGba's battle_moves.h (none yet)

THE RULE (the user, 2026-10-30; recorded at struct BattleMove's .split in include/pokemon.h): a routine that touches
the foe is PHYSICAL; beams, sound, signals, data and anything thrown or spread without touching are SPECIAL. The engine
already says which routines touch -- FLAG_MAKES_CONTACT -- so the rule's candidates are the damaging routines whose
.split disagrees with that flag: contact and SPECIAL (the rule says PHYSICAL), or no contact and PHYSICAL (the rule says
SPECIAL). Step 2 (engine c93a5ce48) left 77 of them, 25 and 52, "for when each is touched"; the user's pick on
2026-11-18 (by multiple choice) was to apply the rule to all of them now, on a sheet first, then re-check the five
5.3b leaders.

Step 2's ten (TAMPER, the CORRUPT row, CONSENSUS, PRIOR, WEATHER BALL) and SLANT already agree with the rule, and STATUS
routines have no side to move, so neither appears here. SPAGHETTI stays as built (the user, 2026-10-30).

JUDGEMENT CALLS. Where the contact flag is vanilla's and our routine no longer depicts what it did (a punch renamed into
weights, a whip into an error signal), or where the side moves a mechanic that lives on one side only, the rule is not
the whole answer. JUDGEMENT holds those, each with both readings and a recommendation; the user rules them.

APPROVED is None until the user rules. Then it is {"date": ..., "keep": {MOVE: why}}: every candidate is written to the
rule's side EXCEPT the ones in keep, which stay where they are (and drop out of the report as "kept by ruling"). A
routine in keep is a ruling, not an oversight -- this tool reports it every time so it stays visible.

WHAT --write CHANGES: only `.split = SPLIT_...,` lines, inside the blocks of the routines it names, in
engineGba/src/data/battle_moves.h. Nothing else in that file (it is hand-edited; no other tool writes .split, so
generator_drift.json has no entry for it). Read whole, written to a temp file, renamed into place.

AFTER A WRITE, by hand in the same commit: the comment at .split in include/pokemon.h ("Judged so far"); CalculateBaseDamage
if PANIC / CORE DUMP go SPECIAL (EFFECT_EXPLOSION halves only DEFENSE, so a SPECIAL blast would lose it) and Thick Fat
(it halves only SP. ATK, so a PHYSICAL ENTROPY or FROZEN routine would get past it); then companion_export.py --write
(the companion carries each routine's split) and gbamovemenu.py's report (it counts the routines off their type's side).
"""
import os, re, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GBA = os.path.join(ROOT, "engineGba")
MOVES = os.path.join(GBA, "src/data/battle_moves.h")
NAMES = os.path.join(GBA, "src/data/text/move_names.h")
TYPES = os.path.join(GBA, "src/battle_main.c")
DESCS = os.path.join(GBA, "src/move_descriptions.c")

#  The user's ruling. None while T-490 step 3 is a DRAFT: --write writes nothing.
APPROVED = None

#  The judgement calls: MOVE -> (the group it is ruled with, why the rule is not the whole answer, reading A (the
#  rule's side), reading B (stays), the recommendation: "rule" or "keep"). A group is ruled as one.
JUDGEMENT = {
    #  contact and SPECIAL, renamed out of the body: the contact flag is vanilla's, the routine is now data or a signal
    "ICE_PUNCH":    ("LOCK", "vanilla's ice punch; ours 'holds the weights where they are' -- model weights, data",
                     "PHYSICAL, beside BURN IN and SHORT OUT (the three punches move together)",
                     "SPECIAL: freezing weights is data, and the flag is the punch's", "keep"),
    "VINE_WHIP":    ("BACKPROP", "vanilla's whip; ours is 'the error travels back the way it came in' -- a signal",
                     "PHYSICAL (ROVERCUB's first hit: CAIRN's line, held at 1 by DURABLE today, keeps a quarter)",
                     "SPECIAL: backpropagation is a signal; the flag is the whip's", "keep"),
    "BITE":         ("OCCLUDE", "vanilla's bite; ours 'shuts the light out'",
                     "PHYSICAL (CLUSTER's line and ANNEAL's SENTRY and GUARDIAN strike with ATTACK)",
                     "SPECIAL: blocking light touches nothing", "keep"),
    "PETAL_DANCE":  ("OVERTRAIN", "vanilla's thrashing dance; ours 'trains on one thing for two or three turns'",
                     "PHYSICAL (a rampage, like RUNAWAY)", "SPECIAL: training is data", "keep"),
    "CLAMP":        ("SLUICE", "vanilla's clamp; ours 'shuts the channel'",
                     "PHYSICAL (a gate is a thing)", "SPECIAL: a channel is BANDWIDTH's own word (1.6d)", "keep"),
    "DRAGON_CLAW":  ("EMERGE", "vanilla's claw; ours 'something nobody specified, arriving anyway'",
                     "PHYSICAL", "SPECIAL: an emergence touches nothing", "keep"),
    "OVERHEAT":     ("BURNOUT", "its cost is SP. ATK -2: a PHYSICAL BURNOUT strikes from ATTACK and pays with a stat it "
                     "no longer uses, so it can be fired again at full strength",
                     "PHYSICAL (GUARDIAN's BURNOUT then OHKOs ROVERBYTE every time, not on a high roll)",
                     "SPECIAL: the drawback has to land on the side it strikes from", "keep"),
    #  no contact and PHYSICAL
    "EARTHQUAKE":   ("UPHEAVAL + TREMOR", "the ground moving under a body: spread without touching by the rule's "
                     "letter, but nothing in it is a signal or data. STRATUM goes from 11 physical hits to 1",
                     "SPECIAL (SCORN's only hit and every STRATUM daemon's main one strike from SP. ATK; see the "
                     "leaders)", "PHYSICAL: mass on a body, Gen 4's reading too", "keep"),
    "MAGNITUDE":    ("UPHEAVAL + TREMOR", "as UPHEAVAL", "SPECIAL", "PHYSICAL", "keep"),
    "SELF_DESTRUCT": ("PANIC + CORE DUMP", "EFFECT_EXPLOSION halves the target's DEFENSE only; a SPECIAL blast loses "
                      "the halving unless CalculateBaseDamage halves SP. DEF too (one line)",
                      "SPECIAL, with the halving moved to whichever defence it strikes (an engine line, same commit)",
                      "PHYSICAL: no engine change", "rule"),
    "EXPLOSION":    ("PANIC + CORE DUMP", "as PANIC; CORE DUMP 'writes out all it has at once' is plainly data",
                     "SPECIAL, with the halving moved", "PHYSICAL", "rule"),
    "SKY_ATTACK":   ("BALLISTIC", "'rises on the first turn and comes down on the second' -- the user is what comes "
                     "down; Gen 3 left the dive without a contact flag",
                     "SPECIAL (a ballistic arc as a projectile)", "PHYSICAL: the body falls on them, as REBOUND does",
                     "keep"),
    "BONE_RUSH":    ("PAGE FAULT", "its description is still vanilla's ('strikes them with a bone in hand'), but the "
                     "name is data and its sibling HARD FAULT (no contact) goes SPECIAL",
                     "SPECIAL, following the name and HARD FAULT; the description wants writing",
                     "PHYSICAL, following the description", "rule"),
    "FAKE_OUT":     ("STALL", "Gen 3 omitted Fake Out's contact flag (Gen 4 added it); ours 'goes first and holds "
                     "them up' -- a delay", "SPECIAL", "PHYSICAL: the flag was an omission", "rule"),
    "COVET":        ("CLAIM", "Gen 3 omitted Covet's contact flag; its sibling LIFT (contact) goes PHYSICAL; ours "
                     "'asks nicely, and takes what they were holding'",
                     "SPECIAL: the asking is the routine, and the contrast with LIFT is the point",
                     "PHYSICAL, beside LIFT", "rule"),
}
#  THE HOURS: the eight 90-power routines one per physical type, "Gone by four". BITROT MOON, the CORRUPT one, went
#  SPECIAL in step 2, and the special types' hours already are; the rule makes all seventeen one side.
for _m in ("BLANK_PAGE", "LAST_PROOF", "NIGHT_COURSE", "UNDERLAYER", "OLD_GHOSTS", "QUIET_HIVE", "WHAT_SLEEPS",
           "NIGHT_WATCH"):
    JUDGEMENT[_m] = ("THE HOURS", "a set of eighteen, one per type, built on each type's old side; BITROT MOON already "
                     "went SPECIAL (step 2)",
                     "SPECIAL: all seventeen damaging hours one side, as BITROT MOON", "PHYSICAL: each hour strikes "
                     "as its type's daemons do", "rule")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def blocks(src):
    """[(MOVE, start, end)] -- each routine's block in battle_moves.h, as gbamovemenu.py reads it."""
    return [(m.group(1), m.start(), m.end()) for m in re.finditer(r"\[MOVE_(\w+)\] =\s*\{(.*?)\n    \},", src, re.S)]


def routines():
    src = read(MOVES)
    names = dict(re.findall(r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read(NAMES)))
    tnames = dict(re.findall(r'\[TYPE_(\w+)\] = _\("([^"]*)"\)', read(TYPES)))
    out = []
    for mv, a, b in blocks(src):
        body = src[a:b]
        g = lambda k: (re.search(r"\.%s = ([^,\n]+)," % k, body) or [None, ""])[1]
        split = g("split").replace("SPLIT_", "")
        contact = "FLAG_MAKES_CONTACT" in g("flags")
        out.append(dict(move=mv, name=names.get(mv, mv), type=tnames.get(g("type")[5:], g("type")), power=int(g("power") or 0),
                        acc=int(g("accuracy") or 0), contact=contact, split=split))
    return src, out


def candidates(rs):
    """Damaging routines whose side disagrees with their contact flag: (routine, the rule's side)."""
    keep = (APPROVED or {}).get("keep", {})
    out = []
    for r in rs:
        if r["split"] not in ("PHYSICAL", "SPECIAL") or r["move"] in keep:
            continue
        rule = "PHYSICAL" if r["contact"] else "SPECIAL"
        if rule != r["split"]:
            out.append((r, rule))
    return out


def report():
    _, rs = routines()
    cs = candidates(rs)
    print("gbasplit (T-490 step 3): contact is physical. APPROVED: %s"
          % ("none -- a DRAFT, nothing is written" if APPROVED is None else APPROVED.get("date")))
    for r, rule in cs:
        j = JUDGEMENT.get(r["move"])
        mark = "  [judgement: %s -- recommend %s]" % (j[0], rule if j[4] == "rule" else "keep " + r["split"]) if j else ""
        print("  %-13s %-9s %3d/%-3s %-10s %-8s -> %-8s MOVE_%s%s"
              % (r["name"], r["type"], r["power"], r["acc"] or "--", "contact" if r["contact"] else "no contact",
                 r["split"], rule, r["move"], mark))
    to_p = sum(1 for _, s in cs if s == "PHYSICAL")
    js = [r for r, _ in cs if r["move"] in JUDGEMENT]
    groups = sorted({JUDGEMENT[r["move"]][0] for r in js})
    keep_rec = sum(1 for r in js if JUDGEMENT[r["move"]][4] == "keep")
    print("  %d routines move: %d to PHYSICAL, %d to SPECIAL; %d of them in %d judgement calls (%s)"
          % (len(cs), to_p, len(cs) - to_p, len(js), len(groups), ", ".join(groups)))
    print("  following every recommendation, %d move and %d stay" % (len(cs) - keep_rec, keep_rec))
    named = {r["move"]: r for r in rs}
    for mv, why in sorted((APPROVED or {}).get("keep", {}).items()):
        r = named.get(mv, {"name": mv, "split": "?"})
        print("  kept by ruling: %s stays %s (MOVE_%s) -- %s" % (r["name"], r["split"], mv, why))
    return 0


def write():
    if APPROVED is None:
        print("gbasplit: nothing approved yet (T-490 step 3 is a DRAFT); nothing written")
        return 0
    src, rs = routines()
    cs = {r["move"]: rule for r, rule in candidates(rs)}
    out, pos, n = [], 0, 0
    for mv, a, b in blocks(src):
        if mv not in cs:
            continue
        body = src[a:b]
        new, k = re.subn(r"\.split = SPLIT_\w+,", ".split = SPLIT_%s," % cs[mv], body, count=1)
        if k != 1:
            sys.exit("gbasplit: %s has no .split line; nothing written" % mv)
        out += [src[pos:a], new]
        pos, n = b, n + 1
    out.append(src[pos:])
    text = "".join(out)
    if read(MOVES) != src:
        sys.exit("gbasplit: battle_moves.h changed while this ran; nothing written")
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.realpath(MOVES)), prefix=".gbasplit.")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.chmod(tmp, os.stat(MOVES).st_mode & 0o7777)
    os.replace(tmp, os.path.realpath(MOVES))
    print("  wrote %d routines' .split into engineGba/src/data/battle_moves.h" % n)
    print("  by hand, same commit: pokemon.h's .split comment; CalculateBaseDamage (EFFECT_EXPLOSION, Thick Fat) if "
          "they moved; then companion_export.py --write")
    return 0


def main():
    a = sys.argv
    if "--write" in a:
        if "--approved" not in a:
            sys.exit("gbasplit: --write needs --approved (it writes APPROVED, the user's ruling)")
        return write()
    return report()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Curate the MUSAI branch to the argument it is named for.

    python3 tools/port_musai.py [--write]

T-02. 2.7 measured a seam: thirteen daemons were RETYPED to carry an argument,
and 78% of their damaging routines are off-type against a 45% baseline. 2.7a
closed it for the three starters; this closes it for the branch 8.2 calls
"the central argument delivered as an evolution branch, with no dialogue at
all" -- CODEMUSAI is LOGIC, CAREMUSAI is CONTEXT, and 2's chart makes LOGIC
fail against CONTEXT.

Every rule is 2.7a's, unchanged.

  NO TYPE MOVES. The chart is untouched (8.4) and no matchup moves (2.5).
  Only which routines a daemon reaches for.

  THE CURVE IS PRESERVED. Every level that had a move still has one, of
  comparable power. Where a replacement is weaker on paper it is stronger in
  play, because it is on-type and takes same-type attack bonus.

  THE RESIDUAL IS DELIBERATE. The target was never zero -- 45% is what
  coverage IS. Each line keeps two routines it is visibly worse at, chosen
  because being worse at THAT is true of what it is.
"""
import os, re, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA   = os.path.join(ROOT, "engineGba")
PATH  = os.path.join(GBA, "src/data/pokemon/level_up_learnsets.h")
WRITE = "--write" in sys.argv

# ---------------------------------------------------------------------------
# CODEMUSAI -- LOGIC. The left hemisphere pulled out into a creature: rules
# applied step by step, proof rather than intuition (2.6). It was fighting
# entirely by heat and one bite -- SEVEN of seven damaging routines off-type,
# the worst in the game -- and it is one half of the game's central argument.
#
#   LEMMA     a small thing proved first so the next step can stand on it,
#             and it has priority, which is what a lemma is FOR
#   REDUCE    reduction: the problem made smaller until it is the one you know
#   INDUCT    two steps, and induction is the method that proves by stepping
#   CRACK     you crack a rock and you crack a problem
#   FALSIFY   ***the best-placed routine in this pass.*** It breaks STEELMAN
#             and PARAPHRASE -- and CODEMUSAI's whole existence is LOGIC
#             against CONTEXT, so the thesis relation arrives as a routine
#             the player uses on the sibling
CODEMUSAI = [
    ( 1, "TACKLE"), ( 1, "TAIL_WHIP"), ( 1, "HELPING_HAND"),
    ( 8, "SAND_ATTACK"),       # SILT, kept. It is MUSAI's own and it is not
                               # a damaging routine, so replacing it would be
                               # a balance change wearing a naming change's
                               # clothes -- 2.7a's first rule
    (16, "MACH_PUNCH"),        # LEMMA -- a small thing proved first so the
                               # next step can stand on it. It has PRIORITY,
                               # which is what a lemma is for
    (23, "DOUBLE_KICK"),       # INDUCT -- two steps, and induction is the
                               # method that proves by stepping
    (30, "BITE"),              # RESIDUAL -- OCCLUDE. The reasoner reaching
                               # into a black box and being worse at it:
                               # OPAQUE is the one thing step-by-step proof
                               # cannot open
    (36, "ROCK_SMASH"),        # CRACK -- you crack a rock and a problem
    (42, "BRICK_BREAK"),       # FALSIFY -- ***the best-placed routine in this
                               # pass.*** It breaks STEELMAN and PARAPHRASE,
                               # and CODEMUSAI exists to be LOGIC against
                               # CONTEXT, so 2.2's thesis relation arrives as
                               # a routine the player uses on the sibling
    (47, "LEER"),              # INSPECT
    (52, "FLAMETHROWER"),      # RESIDUAL -- RADIATE. 6 makes the choleric
                               # LOGIC: "hot, driven, and reasons by force"
]

# ---------------------------------------------------------------------------
# CAREMUSAI -- CONTEXT. The other half. The frame you read a thing in, and
# what makes the same thing mean differently (2.6's strongest clause, 8/8).
# It was fighting by water, which says nothing about any of that.
#
#   MISREAD    reading it in the wrong frame, which is the base case
#   SLANT      the frame tilted, on purpose
#   INTERPRET  and it only works on something SUSPENDED, which is the one
#              state where there is nothing but frame left to read
#   CONSTRUE   the whole of it, said as a verb
CAREMUSAI = [
    ( 1, "TACKLE"), ( 1, "TAIL_WHIP"), ( 1, "HELPING_HAND"),
    ( 8, "SAND_ATTACK"),       # SILT, kept
    (16, "CONFUSION"),         # MISREAD -- reading it in the wrong frame,
                               # which is the base case of the whole type
    (23, "PSYBEAM"),           # SLANT -- the frame tilted, on purpose
    (30, "DREAM_EATER"),       # INTERPRET -- and it works only on something
                               # SUSPENDED, which is the one state where
                               # there is nothing left to read but frame
    (36, "PSYCHIC"),           # CONSTRUE -- the whole of it, said as a verb
    (42, "HAZE"),              # RESET
    (47, "ACID_ARMOR"),        # DISSOLVE
    (52, "HYDRO_PUMP"),        # RESIDUAL -- FLUSH. 0.5 makes CONTEXT the
                               # parallel, flowing, many-at-once side, so the
                               # water it arrived with is on-argument
]

# ---------------------------------------------------------------------------
# SEEKMUSAI -- VECTOR. A direction in a space of meanings (2.6), and 8.2 says
# its pair is the clearest of the three because it is about EMBEDDING.
#
#   PROBE     what a seeker does first
#   DRIFT     movement without a heading yet
#   SHEAR     a separating surface cut through the space
#   DISPATCH  sent somewhere, with a heading
SEEKMUSAI = [
    ( 1, "TACKLE"), ( 1, "TAIL_WHIP"), ( 1, "HELPING_HAND"),
    ( 8, "SAND_ATTACK"),       # SILT, kept
    (16, "GUST"),              # DRIFT -- movement without a heading yet
    (23, "AIR_CUTTER"),        # SHEAR -- a separating surface cut through
                               # the space
    (30, "WING_ATTACK"),       # DISPATCH -- sent somewhere, with a heading
    (36, "PECK"),              # PROBE -- one direction, tried
    (42, "THUNDER_WAVE"),      # BROWNOUT
    (47, "AGILITY"),           # REFRAME
    (52, "THUNDER"),           # RESIDUAL -- TRANSIENT. SIGNAL is "raw current
                               # before anything interprets it", which is what
                               # a search returns before anybody reads it
]

#  S.T.A.R.R. is NOT here, and the ticket said it would be. Measured on
#  2026-09-10 it is 1 of 4 damaging routines off-type -- 25%, well under 2.7's
#  45% baseline -- because the CONTEXT routines it already had are the ones it
#  should have. The 78% in T-02 was the thirteen's average carried onto a name
#  that does not deserve it. UNERRING stays as its residual.
LINES = [("CODEMUSAI", "sFlareonLevelUpLearnset",  CODEMUSAI, {"LOGIC"}),
         ("CAREMUSAI", "sVaporeonLevelUpLearnset", CAREMUSAI, {"CONTEXT"}),
         ("SEEKMUSAI", "sJolteonLevelUpLearnset",  SEEKMUSAI, {"VECTOR"})]


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8", errors="ignore").read()


def main():
    tn = dict(re.findall(r'\[TYPE_(\w+)\] = _\("([^"]+)"\)', read("src/battle_main.c")))
    blocks = dict(re.findall(r'\[MOVE_(\w+)\] =\s*\{(.*?)\n    \},', read("src/data/battle_moves.h"), re.S))
    names = dict(re.findall(r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]+)"\)', read("src/data/text/move_names.h")))

    def kind(mid):
        b = blocks.get(mid, "")
        t = re.search(r'\.type = TYPE_(\w+)', b)
        p = re.search(r'\.power = (\d+)', b)
        return tn.get(t.group(1), "?") if t else "?", int(p.group(1)) if p else 0

    def count(entries, mine):
        off = dmg = 0
        for _, mid in entries:
            ty, pw = kind(mid)
            if pw > 0:
                dmg += 1
                off += ty not in mine
        return off, dmg

    raw = open(PATH, encoding="utf-8").read()
    rc, bo, bd, ao, ad = 0, 0, 0, 0, 0
    for nm, sym, entries, mine in LINES:
        m = re.search(r'(%s\[\] = \{\n)(.*?)(\n?\};)' % sym, raw, re.S)
        if not m:
            print("  !! %s not found" % sym); rc = 1; continue
        old = [(int(a), b) for a, b in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)\)', m.group(2))]
        #  2.7a's first rule, checked rather than trusted: every level that had
        #  a move still has one. Silently dropping a level is a balance change
        #  wearing a naming change's clothes.
        if [lv for lv, _ in old] != [lv for lv, _ in entries]:
            print("  !! %s: the level curve moved -- %s vs %s"
                  % (nm, [lv for lv, _ in old], [lv for lv, _ in entries])); rc = 1; continue
        for _, mid in entries:
            if mid not in blocks:
                print("  !! %s: no such routine MOVE_%s" % (nm, mid)); rc = 1
        o1, d1 = count(old, mine); o2, d2 = count(entries, mine)
        bo += o1; bd += d1; ao += o2; ad += d2
        print("  %-10s %-8s  off-type %d/%d -> %d/%d" % (nm, "/".join(mine), o1, d1, o2, d2))
        for (lv, a), (_, b) in zip(old, entries):
            if a != b:
                print("      %3d  %-13s -> %-13s %s" % (lv, names.get(a, a), names.get(b, b), kind(b)[0]))
        body = "".join("    LEVEL_UP_MOVE(%2d, MOVE_%s),\n" % (lv, mid) for lv, mid in entries)
        raw = raw[:m.start(2)] + body.rstrip("\n") + raw[m.end(2):]

    print("\n  the branch together: %d of %d off-type (%d%%)  ->  %d of %d (%d%%)"
          % (bo, bd, round(100 * bo / max(bd, 1)), ao, ad, round(100 * ao / max(ad, 1))))
    print("  2.7's baseline, the fifty-nine left on vanilla's typing, is 45%")
    if rc:
        return rc
    if WRITE:
        open(PATH, "w", encoding="utf-8").write(raw)
        print("  written")
    else:
        print("  (report only; pass --write)")
    return 0


sys.exit(main())

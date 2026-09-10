#!/usr/bin/env python3
"""Curate the three starter learnsets to the paradigms they are named for.

    python3 tools/port_starters.py [--write]

2.7 measured the seam and named this as the one place the design's argument
stops at the surface: THE THREE STARTERS ARE THE THREE LEARNING PARADIGMS AND
THEIR MOVESETS SAY NOTHING ABOUT ANY OF THEM. The names carry it, the types
carry it, and then the creature fights with vanilla's fire, water and grass.

Of the three levers 2.7 lists -- retype the daemon, retype the move, curate the
learnset -- this is the third and cheapest. It touches no type, so the chart is
untouched (8.4) and no matchup moves (2.5). It only changes which routines a
daemon reaches for.

TWO RULES HELD THROUGHOUT.

  The curve is preserved. Every level that had a move still has one, of
  comparable power, so the early game is balanced the way it was. Where a
  replacement is weaker on paper it is stronger in play, because it is ON-TYPE
  and takes same-type attack bonus -- TRI ATTACK at 80 with STAB beats
  FLAMETHROWER at 95 without it.

  The residual is deliberate. 2.7's finding was that 45% off-type is what
  coverage IS and 78% is a mismatch; the target was never zero. Each line keeps
  one or two routines it is visibly worse at, chosen because being worse at
  THAT is true of the paradigm. Those are marked RESIDUAL below.
"""
import os, re, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA   = os.path.join(ROOT, "engineGba")
PATH  = os.path.join(GBA, "src/data/pokemon/level_up_learnsets.h")
WRITE = "--write" in sys.argv

# ---------------------------------------------------------------------------
# SUPERVISED -- LABL -> RUBRIC -> CANON, CONTENT then CONTENT/LOGIC
#
# You hold the answer key. You compare, you score, you correct. A supervised
# learner is the LEAST entropic thing in the set -- it has ground truth -- so
# a line that fought entirely by heat was the sharpest of the three seams.
#
#   FORESIGHT   identify the target, which is what a label IS
#   MIMIC       copy the answer you were shown
#   SWIFT       an answer that cannot miss (ALWAYS_HIT), and on-type
#   TRI ATTACK  classification into three outcomes, and 80 with STAB
#   SLASH       precision, kept from vanilla
#   LOCK-ON     the next one cannot miss, because you have the ground truth
#   COUNTER     return exactly the error you were given -- CANON, on LOGIC
#   SEISMIC TOSS  damage equal to your level: a known quantity, not a roll
#
#   RESIDUAL: DRAGON RAGE stays. EMERGENT is "behaviour nobody designed and
#   nobody can account for", and a labelled learner producing exactly one of
#   those is the entire modern story. It is fixed damage and it is off-type,
#   so the daemon is measurably worse at the one thing it cannot account for.
SUPERVISED = {
    "Charmander": [
        (1,  "SCRATCH"), (1, "GROWL"),
        (7,  "FORESIGHT"),          # was EMBER
        (13, "MIMIC"),              # was METAL_CLAW
        (19, "SMOKESCREEN"),
        (25, "SWIFT"),              # was SCARY_FACE
        (31, "TRI_ATTACK"),         # was FLAMETHROWER
        (37, "SLASH"),
        (43, "DRAGON_RAGE"),        # RESIDUAL
        (49, "LOCK_ON"),            # was FIRE_SPIN
    ],
    "Charmeleon": [
        (1,  "SCRATCH"), (1, "GROWL"), (1, "FORESIGHT"),
        (7,  "FORESIGHT"),
        (13, "MIMIC"),
        (20, "SMOKESCREEN"),
        (27, "SWIFT"),
        (34, "TRI_ATTACK"),
        (41, "SLASH"),
        (48, "DRAGON_RAGE"),        # RESIDUAL
        (55, "LOCK_ON"),
    ],
    "Charizard": [
        # The second type arrives at the third stage, so LOGIC does too:
        # COUNTER returns the error, SEISMIC TOSS is a known quantity.
        (1,  "COUNTER"),            # was HEAT_WAVE
        (1,  "SCRATCH"), (1, "GROWL"), (1, "FORESIGHT"), (1, "MIMIC"),
        (7,  "FORESIGHT"),
        (13, "MIMIC"),
        (20, "SMOKESCREEN"),
        (27, "SWIFT"),
        (34, "TRI_ATTACK"),
        (36, "KARATE_CHOP"),        # was WING_ATTACK -- CANON is not VECTOR
        (44, "SLASH"),
        (54, "DRAGON_RAGE"),        # RESIDUAL
        (64, "BRICK_BREAK"),        # was FIRE_SPIN
    ],
}

# ---------------------------------------------------------------------------
# UNSUPERVISED -- CLUSTR -> LOCUS -> MANIFOLD, VECTOR then VECTOR/LATENT
#
# THE FLOW SPINE STAYS, and that is a finding rather than a compromise.
# k-means descends a distance objective, and FLOW's clause is "everything
# running downhill to the lowest point" -- so an unsupervised learner that
# operates BY FLOW is not off-model, it is the algorithm. It is also load
# bearing: FLOW x2 against LEGACY is the one LEGACY relation that reads (2.6),
# and Slate is the first Benchmark. Stripping the water would have broken the
# first gym to make a point the chart was already making.
#
# What was actually missing is that a VECTOR line knew no VECTOR routines.
#
#   AIR CUTTER  cutting the space -- a separating surface, and high-crit
#   DRILL PECK  the STAB finisher the line never had
#   SHADOW BALL MANIFOLD gains LATENT, and the manifold IS the latent space
#
#   RESIDUAL: BITE stays. OPAQUE is the black box, and unsupervised methods
#   are the least interpretable thing in machine learning. The line is worse
#   at being a black box, which is the joke and also the truth.
UNSUPERVISED = {
    "Squirtle": [
        (1,  "TACKLE"), (4, "TAIL_WHIP"),
        (7,  "GUST"),               # was BUBBLE -- the line's first STAB
        (10, "WITHDRAW"),
        (13, "WATER_GUN"),          # and FLOW by 13, which is what Slate needs
        (18, "BITE"),               # RESIDUAL
        (23, "AIR_CUTTER"),         # was RAPID_SPIN
        (28, "PROTECT"),
        (33, "RAIN_DANCE"),         # reshape the field, not the point
        (40, "DRILL_PECK"),         # was SKULL_BASH
        (47, "HYDRO_PUMP"),
    ],
    "Wartortle": [
        (1,  "TACKLE"), (1, "TAIL_WHIP"), (1, "GUST"),
        (4,  "TAIL_WHIP"), (7, "GUST"), (10, "WITHDRAW"), (13, "WATER_GUN"),
        (19, "BITE"),               # RESIDUAL
        (25, "AIR_CUTTER"),
        (31, "PROTECT"),
        (37, "RAIN_DANCE"),
        (45, "DRILL_PECK"),
        (53, "HYDRO_PUMP"),
    ],
    "Blastoise": [
        (1,  "SHADOW_BALL"),        # the second type, on the stage that gains it
        (1,  "TACKLE"), (1, "TAIL_WHIP"), (1, "GUST"), (1, "WITHDRAW"),
        (4,  "TAIL_WHIP"), (7, "GUST"), (10, "WITHDRAW"), (13, "WATER_GUN"),
        (19, "BITE"),               # RESIDUAL
        (25, "AIR_CUTTER"),
        (31, "PROTECT"),
        (42, "RAIN_DANCE"),
        (55, "DRILL_PECK"),
        (68, "HYDRO_PUMP"),
    ],
}

# ---------------------------------------------------------------------------
# REINFORCEMENT -- ROVERCUB -> ROVERSEER -> ROVERBYTE, GROWTH then GROWTH/SIGNAL
#
# This line was already nearly right and needed the least. LEECH SEED is the
# best-fitting routine in the whole set without anyone having arranged it: a
# return that accrues every turn from a thing you did once. SYNTHESIS recovers
# from what you gathered, GROWTH gets stronger by doing, and SOLARBEAM charges
# a turn before it pays -- which is delayed reward, in the engine, since 1996.
#
#   MEGA DRAIN  taking return from the environment, and on-type -- replaces
#               POISONPOWDER, the only CORRUPT routine in the line
#   SHOCK WAVE  ROVERBYTE gains SIGNAL and learned no SIGNAL routine at all.
#               The reward signal arrives on evolution, and it never misses.
#
#   RESIDUAL: SLEEP POWDER stays, and it is the one routine in these three
#   lines whose TYPE is an open question -- 2.7 gives SUSPENDED to CONTEXT and
#   leaves the retype as a balance decision. It is marked here so the two
#   places agree.
REINFORCEMENT = {
    "Bulbasaur": [
        (1,  "TACKLE"), (4, "GROWL"), (7, "LEECH_SEED"), (10, "VINE_WHIP"),
        (15, "MEGA_DRAIN"),         # was POISONPOWDER
        (15, "SLEEP_POWDER"),       # RESIDUAL -- see 2.7's open item
        (20, "RAZOR_LEAF"), (25, "SWEET_SCENT"), (32, "GROWTH"),
        (39, "SYNTHESIS"), (46, "SOLAR_BEAM"),
    ],
    "Ivysaur": [
        (1,  "TACKLE"), (1, "GROWL"), (1, "LEECH_SEED"),
        (4,  "GROWL"), (7, "LEECH_SEED"), (10, "VINE_WHIP"),
        (15, "MEGA_DRAIN"),
        (15, "SLEEP_POWDER"),
        (22, "RAZOR_LEAF"), (29, "SWEET_SCENT"), (38, "GROWTH"),
        (47, "SYNTHESIS"), (56, "SOLAR_BEAM"),
    ],
    "Venusaur": [
        (1,  "SHOCK_WAVE"),         # the second type, on the stage that gains it
        (1,  "TACKLE"), (1, "GROWL"), (1, "LEECH_SEED"), (1, "VINE_WHIP"),
        (4,  "GROWL"), (7, "LEECH_SEED"), (10, "VINE_WHIP"),
        (15, "MEGA_DRAIN"),
        (15, "SLEEP_POWDER"),
        (22, "RAZOR_LEAF"), (29, "SWEET_SCENT"), (41, "GROWTH"),
        (53, "SYNTHESIS"), (65, "SOLAR_BEAM"),
    ],
}

SETS = {}
for d in (SUPERVISED, UNSUPERVISED, REINFORCEMENT):
    SETS.update(d)

MAX_LEVEL_UP_MOVES = 20


def types_and_powers():
    """Everything measured is read out of the build, never typed here."""
    tn = dict(re.findall(r'\[TYPE_(\w+)\]\s*=\s*_\("(\w+)"\)',
                         open(os.path.join(GBA, "src/battle_main.c")).read()))
    mv = open(os.path.join(GBA, "src/data/battle_moves.h"),
              encoding="utf-8", errors="ignore").read()
    mt, mp = {}, {}
    for b in re.finditer(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \}", mv, re.S):
        d = dict(re.findall(r"\.(\w+)\s*=\s*([A-Za-z0-9_]+)", b.group(2)))
        mt[b.group(1)] = tn.get(d.get("type", "").replace("TYPE_", ""), "?")
        mp[b.group(1)] = int(d.get("power", "0"))
    info = open(os.path.join(GBA, "src/data/pokemon/species_info.h"),
                encoding="utf-8", errors="ignore").read()
    st = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{(?:[^{}]|\{[^{}]*\})*?"
                         r"\.types\s*=\s*\{\s*TYPE_(\w+),\s*TYPE_(\w+)", info, re.S):
        st[m.group(1)] = {tn.get(m.group(2), "?"), tn.get(m.group(3), "?")}
    names = dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]+)"\)',
                 open(os.path.join(GBA, "src/data/text/species_names.h"),
                      encoding="utf-8", errors="ignore").read()))
    return mt, mp, st, names


def offtype(entries, mine, mt, mp):
    dmg = [m for _, m in entries if mp.get(m, 0) > 0]
    off = [m for m in dmg if mt.get(m) not in mine]
    return len(off), len(dmg)


def main():
    mt, mp, st, names = types_and_powers()
    raw = open(PATH, encoding="utf-8").read()
    rc, before_o, before_d, after_o, after_d = 0, 0, 0, 0, 0

    for who, entries in SETS.items():
        key = who.upper()
        mine = st.get(key, set())
        nm = names.get(key, who)
        if len(entries) > MAX_LEVEL_UP_MOVES:
            print("  !! %s: %d entries > %d" % (nm, len(entries), MAX_LEVEL_UP_MOVES))
            rc = 1
        for _, mid in entries:
            if mid not in mt:
                print("  !! %s: MOVE_%s does not exist" % (nm, mid)); rc = 1

        pat = re.compile(r"(static const u16 s%sLevelUpLearnset\[\] = \{\n)(.*?)(    LEVEL_UP_END\n\};)"
                         % who, re.S)
        m = pat.search(raw)
        if not m:
            print("  !! %s: learnset not found" % nm); rc = 1; continue
        old = [(int(a), b) for a, b in
               re.findall(r"LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)", m.group(2))]
        bo, bd = offtype(old, mine, mt, mp)
        ao, ad = offtype(entries, mine, mt, mp)
        before_o += bo; before_d += bd; after_o += ao; after_d += ad
        kept = sum(1 for e in entries if e in old)
        print("  %-11s %-16s  off-type %2d/%-2d -> %2d/%-2d   %d of %d entries unchanged"
              % (nm, "/".join(sorted(mine)), bo, bd, ao, ad, kept, len(entries)))
        body = "".join("    LEVEL_UP_MOVE(%d, MOVE_%s),\n" % (lv, mid) for lv, mid in entries)
        raw = raw[:m.start(2)] + body + raw[m.end(2):]

    print("\n  the three lines together: %d of %d damaging routines off-type (%d%%)"
          "  ->  %d of %d (%d%%)"
          % (before_o, before_d, round(100 * before_o / max(before_d, 1)),
             after_o, after_d, round(100 * after_o / max(after_d, 1))))
    print("  2.7's baseline, the fifty-nine daemons left on vanilla's typing, is 45%")

    if rc:
        return rc
    if WRITE:
        open(PATH, "w", encoding="utf-8").write(raw)
        print("  written")
    else:
        print("  (report only; pass --write)")
    return 0


sys.exit(main())

#!/usr/bin/env python3
"""The STATE animations -- what plays each turn a daemon is in a state (T-168, wave 1; vision.md 9.24, 1.6).

    python3 tools/genstates.py --wave 2            # report what would be written
    python3 tools/genstates.py --wave 2 --write    # write that wave's drafts (debug ROMs only)
    python3 tools/genstates.py --wave 2 --release  # approved: drop each .if DAEMONS_DEBUG and vanilla's .else

A WAVE IS NAMED EVERY TIME, because a released script has no guard left to find: run over a released wave, the
tool would wrap OUR script as if it were vanilla's. Waves 1 and 2 are released (engine 0e786a157, 79b94a3e0).

WHY. 1.6 renamed every state for a PROCESS -- LEAKING, THRASHING, OVERHEATED, SUSPENDED, THROTTLED, HUNG -- and
T-137's close showed each still playing the BODY it replaced: a Z, circling ducks, embers, sparks, an ice cube.
9.24 is the rule, unchanged: the animation shows the process; the daemon's own palette is the medium and grey is
the ground; the only colour added is a type's, from gbasprite.py's TYPE_COLOR; the streaks go with the palette.

THE VOCABULARY IS TIME, because a state is a process that keeps happening. No sprite is loaded and nothing moves
except where the word IS motion (THRASHING); each state is told apart by its rhythm:

    LEAKING     CORRUPT   two slow ticks, and after each a slice of colour drains to grey and seeps back --
                          a fixed loss per tick (1.6). CASCADING plays the same script (the engine has one for both)
    THRASHING   (grey)    fast, many, shallow: flicker toward grey and a one-pixel jitter -- busy, no progress
    OVERHEATED  ENTROPY   heat flushes up slowly, shimmers, and cools
    SUSPENDED   (grey)    dims, holds, and resumes -- silent, because nothing is scheduled
    THROTTLED   SIGNAL    pulse, pulse, a long stall, one more pulse -- a speed cap that stalls work
    HUNG        FROZEN    snaps to FROZEN at once and holds there, still, until it is let go

WAVE 4 -- what happens TO a daemon outside a move: a hit landing, fear, an item acting or being taken, a return,
gathering, being revealed, a set routine arriving. No sprite is loaded: a loss drains toward grey, a gain deepens
toward the daemon's own type, a return comes back in ticked steps (9.24's RESTORE exemplar).

KEPT ON PURPOSE, each because the MECHANIC is the picture (T-144's rule, and T-156's doll): the ball throws and
their four helpers, the level-up, both switch-outs, SUBSTITUTE's four, the Safari's bait, rock and three
reactions, and CASTFORM's change -- no player of this game can meet a Castform. SNATCH is kept for a mechanical
reason instead: its script runs past its own `end` into SnatchMoveContinue, which two other scripts jump to, so a
guard around it does not link. region() now refuses a region with a second label in it rather than writing that.

WAVE 3 -- weather and field, and it is ONE animation: sun, sandstorm, hail and the leech drain turned out to be
one-line scripts that jump straight into OUR redrawn move animations (rain already did), so they read as vanilla
only because the jump is byte-identical. What is left is the STAT CHANGE, which plays constantly:

    a stat change        vanilla scrolls an arrow mask over the daemon; 9.24 makes the daemon's palette the medium --
                         UP deepens it toward its own type, DOWN drains it toward grey, and two stages go further
                         and HOLD there before coming back

WAVE 2 -- the other conditions, named for what our routines do (move_names.h, 2.x):

    PAIR        CONTENT   its attention is on its pair: it AND the other daemon pulse together, slowly, twice
                          (AnimTask_BlendBattleAnimPalExclude 2: every battler but itself)
    CONSULT     (grey)    ORACLE's routine, and ORACLE has no colour: the box goes dark at once, answers, and
                          the answer costs a slice
    STARVATION  LATENT    a SUSPENDED daemon given nothing at all: it sinks, two ticks deeper, and surfaces
    the traps             HELD, in the trapping routine's type: the colour closes, holds with a one-pixel tick
                          of damage, and lets go -- each told apart by how it holds:
      LATCH/ENCLOSE CONTENT  plain; THERMAL ENTROPY  shimmers while held; WHIRLPOOL FLOW  circulates;
      SLUICE        FLOW     a gate: snaps shut and snaps open; BURY STRATUM  settles slowly, lifts slowly

THE REGION a draft replaces is the `Status_X:` label through its own first `end`. The subroutines vanilla's
versions call (ConfusionEffect, BurnFlame, ElectricityEffect) stay where they are, because the `.else` still
calls them and so may other scripts. Running it again replaces its own drafts.
"""
import ast, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")
SCRIPTS = os.path.join(E, "data/battle_anim_scripts.s")
MARK = "@ genstates:"
GREY = "RGB(13, 13, 13)"


def type_rgb555(name):
    tree = ast.parse(open(os.path.join(ROOT, "tools/gbasprite.py")).read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "TYPE_COLOR" for t in n.targets):
            r, g, b = ast.literal_eval(n.value)[name]
            return "RGB(%d, %d, %d)" % (r >> 3, g >> 3, b >> 3)
    raise SystemExit("gbasprite.py no longer defines TYPE_COLOR")


def blend(delay, a, b, col):
    return ["\tcreatevisualtask AnimTask_BlendBattleAnimPal, 10, F_PAL_ATTACKER, %d, %d, %d, %s" % (delay, a, b, col)]


def cycle(delay, times, a, b, col):
    return ["\tcreatevisualtask AnimTask_BlendColorCycle, 2, F_PAL_ATTACKER, %d, %d, %d, %d, %s" % (delay, times, a, b, col)]


def shake(px, times, delay):
    return ["\tcreatevisualtask AnimTask_ShakeMon2, 2, ANIM_ATTACKER, %d, 0, %d, %d" % (px, times, delay)]


W = ["\twaitforvisualfinish"]


def pause(n):
    return ["\tdelay %d" % n]


def leaking():
    c = type_rgb555("POISON")
    tick = (["\tplaysewithpan SE_M_TOXIC, SOUND_PAN_ATTACKER"] + cycle(2, 1, 0, 9, c) + W
            + blend(1, 0, 7, GREY) + W + blend(3, 7, 0, GREY) + W)
    return tick + pause(6) + tick


def thrashing():
    return (["\tloopsewithpan SE_M_DIZZY_PUNCH, SOUND_PAN_ATTACKER, 13, 3"]
            + shake(1, 28, 1) + cycle(0, 7, 0, 7, GREY) + W)


def overheated():
    c = type_rgb555("FIRE")
    return (["\tplaysewithpan SE_M_FLAME_WHEEL, SOUND_PAN_ATTACKER"] + blend(3, 0, 10, c) + W
            + cycle(1, 3, 10, 6, c) + W + blend(2, 10, 0, c) + W)


def suspended():
    return blend(3, 0, 10, GREY) + W + pause(36) + blend(3, 10, 0, GREY) + W


def throttled():
    c = type_rgb555("ELECTRIC")
    pulse = ["\tplaysewithpan SE_M_THUNDERBOLT2, SOUND_PAN_ATTACKER"] + shake(1, 2, 1) + blend(0, 0, 9, c) + W + blend(0, 9, 0, c) + W
    return pulse + pause(6) + pulse + pause(30) + pulse


def hung():
    c = type_rgb555("ICE")
    return (["\tplaysewithpan SE_M_ICY_WIND, SOUND_PAN_ATTACKER"] + blend(0, 0, 12, c) + W
            + pause(44) + blend(0, 12, 0, c) + W)


def pair():
    c = type_rgb555("NORMAL")
    both = ["\tcreatevisualtask AnimTask_BlendBattleAnimPalExclude, 10, 2, %d, %d, %d, %s" % (d, a, b, c) for d, a, b in ((3, 0, 8),)]
    back = ["\tcreatevisualtask AnimTask_BlendBattleAnimPalExclude, 10, 2, 3, 8, 0, %s" % c]
    beat = (["\tplaysewithpan SE_M_CHARM, SOUND_PAN_ATTACKER"] + blend(3, 0, 8, c) + both + W
            + blend(3, 8, 0, c) + back + W)
    return beat + pause(10) + beat


def consult():
    return (["\tplaysewithpan SE_M_CONFUSE_RAY, SOUND_PAN_ATTACKER"] + blend(0, 0, 14, GREY) + W + pause(16)
            + blend(0, 14, 0, GREY) + W + pause(4) + blend(1, 0, 6, GREY) + W + blend(2, 6, 0, GREY) + W)


def starvation():
    c = type_rgb555("GHOST")
    return (blend(3, 0, 11, c) + W + ["\tplaysewithpan SE_M_NIGHTMARE, SOUND_PAN_ATTACKER"]
            + cycle(3, 2, 11, 15, c) + W + blend(2, 11, 0, c) + W)


def held(tname, se, close=1, hold=16, open_=2, depth=9, during=()):
    c = type_rgb555(tname)
    return (["\tplaysewithpan %s, SOUND_PAN_ATTACKER" % se] + blend(close, 0, depth, c) + W
            + list(during(c) if during else []) + shake(1, 2, 2) + pause(hold) + W
            + blend(open_, depth, 0, c) + W)


def latch():
    return held("NORMAL", "SE_M_BIND")


def thermal():
    return held("FIRE", "SE_M_FLAME_WHEEL", during=lambda c: cycle(1, 3, 9, 5, c) + W)


def whirlpool():
    #  Deeper than the others: at 9 -> 4 the first film showed the circulation only faintly.
    return held("WATER", "SE_M_WHIRLPOOL", depth=11, during=lambda c: cycle(0, 5, 11, 5, c) + W)


def sluice():
    return held("WATER", "SE_M_VICEGRIP", close=0, hold=20, open_=0, depth=11)


def bury():
    return held("GROUND", "SE_M_SAND_TOMB", close=4, hold=12, open_=4, depth=10)


def statchange():
    """9.24 on a stat change: UP deepens the daemon toward its own type, DOWN drains it toward grey, and a two-stage
    change goes further and holds. AnimTask_DaemonsStatKind reads animationData->animArg and says which it is."""
    up = (["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 1, 0, 9"] + W
          + ["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 2, 9, 0"] + W + ["\tend"])
    up_sharp = (["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 0, 0, 14"] + W + pause(10)
                + ["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 2, 14, 0"] + W + ["\tend"])
    down = blend(1, 0, 8, GREY) + W + blend(2, 8, 0, GREY) + W + ["\tend"]
    down_sharp = blend(0, 0, 13, GREY) + W + pause(10) + blend(2, 13, 0, GREY) + W + ["\tend"]
    return (["\tcreatevisualtask AnimTask_DaemonsStatKind, 5", "\tdelay 0",
             "\tjumpargeq 0, 1, DaemonsStatDown",
             "\tjumpargeq 1, 1, DaemonsStatUpSharply"]
            + ["\tplaysewithpan SE_M_SWAGGER, SOUND_PAN_ATTACKER"] + up
            + ["DaemonsStatUpSharply:", "\tplaysewithpan SE_M_SWAGGER2, SOUND_PAN_ATTACKER"] + up_sharp
            + ["DaemonsStatDown:", "\tjumpargeq 1, 1, DaemonsStatDownSharply",
               "\tplaysewithpan SE_M_STAT_DECREASE, SOUND_PAN_ATTACKER"] + down
            + ["DaemonsStatDownSharply:", "\tplaysewithpan SE_M_STAT_DECREASE, SOUND_PAN_ATTACKER"] + down_sharp)


# ---- wave 4: what happens TO a daemon outside a move. Each is the palette again, in the vocabulary already set:
# a loss drains toward grey, a gain deepens toward the daemon's own type, a return comes back in ticked steps.
def hit(depth=7, shakes=3):
    return (["\tplaysewithpan SE_M_DOUBLE_SLAP, SOUND_PAN_TARGET"] + shake(2, shakes, 1)
            + ["\tcreatevisualtask AnimTask_BlendBattleAnimPal, 10, F_PAL_TARGET, 0, 0, %d, %s" % (depth, GREY)] + W
            + ["\tcreatevisualtask AnimTask_BlendBattleAnimPal, 10, F_PAL_TARGET, 2, %d, 0, %s" % (depth, GREY)] + W)


def scared():
    """it is about to be gone: the colour thins and jitters, and vanilla's sweat beads go"""
    return (["\tcreatevisualtask AnimTask_SafariOrGhost_DecideAnimSides, 2, 1"] + W
            + shake(1, 10, 1) + ["\tcreatevisualtask AnimTask_BlendBattleAnimPal, 10, F_PAL_TARGET, 1, 0, 11, %s" % GREY] + W
            + ["\tcreatevisualtask AnimTask_BlendBattleAnimPal, 10, F_PAL_TARGET, 3, 11, 0, %s" % GREY] + W)


def focus_band():
    """held at one HP: it drains nearly out, then catches and holds one step back"""
    return (["\tplaysewithpan SE_M_DRAGON_RAGE, SOUND_PAN_ATTACKER"] + blend(0, 0, 15, GREY) + W
            + blend(0, 15, 11, GREY) + W + pause(24) + blend(2, 11, 0, GREY) + W)


def held_item():
    """something it carries acts on it: two quick deepenings toward its own type"""
    beat = (["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 0, 0, 10"] + W
            + ["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 1, 10, 0"] + W)
    return ["\tplaysewithpan SE_M_TAKE_DOWN, SOUND_PAN_ATTACKER"] + beat + pause(4) + beat


def transfer(se="SE_M_TAIL_WHIP"):
    """an item moves from one to the other: the one that loses drains, then the one that gains deepens"""
    return (["\tplaysewithpan %s, SOUND_PAN_TARGET" % se]
            + ["\tcreatevisualtask AnimTask_BlendBattleAnimPal, 10, F_PAL_TARGET, 1, 0, 10, %s" % GREY] + W
            + ["\tcreatevisualtask AnimTask_BlendBattleAnimPal, 10, F_PAL_TARGET, 2, 10, 0, %s" % GREY]
            + ["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 1, 0, 10"] + W
            + ["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 2, 10, 0"] + W)


def restore_ticks():
    """9.24's exemplar, as RESTORE was built: what was lost comes back in ticked steps"""
    out = ["\tplaysewithpan SE_M_ABSORB_2, SOUND_PAN_ATTACKER"] + blend(0, 0, 12, GREY) + W
    for a, b in ((12, 8), (8, 4), (4, 0)):
        out += blend(1, a, b, GREY) + W + pause(6)
    return out


def gathering():
    """it holds still and deepens toward its own type, and keeps it"""
    return (["\tplaysewithpan SE_M_DRAGON_RAGE, SOUND_PAN_ATTACKER"]
            + ["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 2, 0, 12"] + W + pause(20)
            + ["\tcreatevisualtask AnimTask_DaemonsBlendToUserType, 10, 3, 12, 0"] + W)


def revealed():
    """the SILPH SCOPE: what was grey resolves into its own colour"""
    return (["\tplaysewithpan SE_M_TELEPORT, SOUND_PAN_ATTACKER"] + blend(0, 0, 15, GREY) + W + pause(10)
            + blend(3, 15, 0, GREY) + W)


def delayed_hit():
    """a routine that was set turns up later: the same landing, deeper, with nothing thrown"""
    return (["\tcreatevisualtask AnimTask_SetAnimTargetToBattlerTarget, 2"] + W + hit(depth=11, shakes=5))


STATES = [   # wave, label, our word, the process
    (1, "Status_Poison", "LEAKING", leaking),
    (1, "Status_Confusion", "THRASHING", thrashing),
    (1, "Status_Burn", "OVERHEATED", overheated),
    (1, "Status_Sleep", "SUSPENDED", suspended),
    (1, "Status_Paralysis", "THROTTLED", throttled),
    (1, "Status_Freeze", "HUNG", hung),
    (2, "Status_Infatuation", "PAIR", pair),
    (2, "Status_Curse", "CONSULT", consult),
    (2, "Status_Nightmare", "STARVATION", starvation),
    (2, "Status_BindWrap", "LATCH / ENCLOSE", latch),
    (2, "Status_FireSpin", "THERMAL", thermal),
    (2, "Status_Whirlpool", "WHIRLPOOL", whirlpool),
    (2, "Status_Clamp", "SLUICE", sluice),
    (2, "Status_SandTomb", "BURY", bury),
    (3, "General_StatsChange", "a stat change", statchange),
    (4, "General_MonHit", "a hit lands", hit),
    (4, "General_MonScared", "it is about to go", scared),
    (4, "General_FocusBand", "held at one HP", focus_band),
    (4, "General_HeldItemEffect", "what it carries acts", held_item),
    (4, "General_ItemKnockoff", "an item knocked out of it", transfer),
    (4, "General_ItemSteal", "an item taken", transfer),
    (4, "General_IngrainHeal", "a return, ticked", restore_ticks),
    (4, "General_WishHeal", "a return, ticked", restore_ticks),
    (4, "General_FocusPunchSetUp", "gathering, and holding it", gathering),
    (4, "General_SilphScoped", "revealed", revealed),
    (4, "General_FutureSightHit", "a set routine lands", delayed_hit),
    (4, "General_DoomDesireHit", "a set routine lands", delayed_hit),
]


def region(text, label):
    """(start, end) of `label:` through its first `end` line -- or of an earlier draft's whole guard"""
    m = re.search(r"^%s:\n" % label, text, re.M)
    if not m:
        raise SystemExit("no %s in battle_anim_scripts.s" % label)
    body_start = m.end()
    if text.startswith("%s %s" % (MARK, label), body_start):
        e = text.index("\n.endif\n", body_start) + len("\n.endif\n")
        return m.start(), e, text[text.index(".else\n", body_start) + 6:text.index("\n.endif\n", body_start) + 1]
    e = re.compile(r"^\tend\n", re.M).search(text, body_start).end()
    van = text[body_start:e]
    #  A REGION MAY NOT SWALLOW ANOTHER LABEL. General_SnatchMove runs past its own `end` into SnatchMoveContinue,
    #  which two other scripts jump to -- guarding the region put that label inside `.else`, and the debug build
    #  failed to link (genanims.py met the same trap on SWALLOW). A script shaped like this keeps vanilla's.
    inner = [l for l in re.findall(r"^([A-Za-z_]\w*):$", van, re.M)]
    if inner:
        raise SystemExit("%s runs into %s, which other scripts call: leave it vanilla's" % (label, ", ".join(inner)))
    return m.start(), e, van


def main():
    text = open(SCRIPTS).read()
    release = "--release" in sys.argv
    if "--wave" not in sys.argv:
        raise SystemExit("name a wave: --wave N (a released wave has no guard, and would be wrapped as vanilla)")
    wave = int(sys.argv[sys.argv.index("--wave") + 1])
    for w, label, word, make in STATES:
        if w != wave:
            continue
        s, e, vanilla = region(text, label)
        lines = make()
        ours = "\n".join(lines + ([] if lines[-1].strip() == "end" else ["\tend"])) + "\n"
        if release:
            block = "%s:\n%s" % (label, ours)
        else:
            block = "%s:\n%s %s -- %s (T-168)\n.if DAEMONS_DEBUG\n%s.else\n%s.endif\n" % (label, MARK, label, word, ours, vanilla)
        text = text[:s] + block + text[e:]
        print("  %-18s %-11s %2d lines%s" % (label, word, len(ours.splitlines()), "  (released)" if release else ""))
    if "--write" in sys.argv or release:
        open(SCRIPTS, "w").write(text)
        print("  written: %s" % os.path.relpath(SCRIPTS, ROOT))


if __name__ == "__main__":
    main()

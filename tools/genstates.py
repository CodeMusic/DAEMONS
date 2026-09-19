#!/usr/bin/env python3
"""The STATE animations -- what plays each turn a daemon is in a state (T-168, wave 1; vision.md 9.24, 1.6).

    python3 tools/genstates.py            # report what would be written
    python3 tools/genstates.py --write    # write the drafts into data/battle_anim_scripts.s (debug ROMs only)
    python3 tools/genstates.py --release  # approved: drop each .if DAEMONS_DEBUG and vanilla's .else

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


STATES = [   # label, our word, the process
    ("Status_Poison", "LEAKING", leaking),
    ("Status_Confusion", "THRASHING", thrashing),
    ("Status_Burn", "OVERHEATED", overheated),
    ("Status_Sleep", "SUSPENDED", suspended),
    ("Status_Paralysis", "THROTTLED", throttled),
    ("Status_Freeze", "HUNG", hung),
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
    return m.start(), e, text[body_start:e]


def main():
    text = open(SCRIPTS).read()
    release = "--release" in sys.argv
    for label, word, make in STATES:
        s, e, vanilla = region(text, label)
        ours = "\n".join(make() + ["\tend"]) + "\n"
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

#!/usr/bin/env python3
"""Battle animations for a family of routines, generated from one visual vocabulary (T-134; vision.md 9.24).

    python3 tools/genanims.py CONTENT            # report what would be written
    python3 tools/genanims.py CONTENT --write     # write the drafts into data/battle_anim_scripts.s
    python3 tools/genanims.py CONTENT --release  # approved: drop each .if DAEMONS_DEBUG and vanilla's .else

WHY A GENERATOR. A family is dozens of routines, and a hand-written animation per routine drifts: two
strikes of the same strength end up drawn two ways, and a later rule change means editing sixty scripts. So
each family has a vocabulary -- a handful of STEPS, each a few lines of animation script -- and a TABLE that
says which steps each routine takes. Changing a step redraws every routine that uses it, identically.

THE CONTENT VOCABULARY (T-140), which is 9.24's answer to "WRITE is a lunge":
  * THE ATTACKER DOES NOT MOVE (9.24.1). What travels is the write: the attacker's colour pulses toward its
    routine's type -- the routine running -- and then
  * THE TARGET TAKES THE TYPE'S COLOUR AND SHAKES -- the write landing. Strength is read off the routine's
    POWER, so a stronger write lands deeper into the colour and shakes harder, with no hand-tuning.
  * Loss is GREY (9.24.2): recoil greys the attacker a little, a one-hit KO drains the target to black and
    back, halving drains it half-way. A self-destruct greys the attacker out completely under a full-field flash.
  * The only colour added is the routine's type (9.24.3), taken from gbasprite.py's TYPE_COLOR, never typed here.

HOW IT WRITES. Each routine's script is replaced from its `Move_X:` label up to the next `Move_` label, and
the whole of vanilla's region -- its private subroutines included -- goes into the `.else`, so the release
ROMs keep playing vanilla's until the family is approved. A subroutine that OTHER routines still call is
left outside the guard; if it jumps back into the region the tool stops and says so, since a debug build
would not link (SWALLOW's SwallowGood did exactly that in T-139). Running it again replaces its own drafts.
"""
import ast, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")
SCRIPTS = os.path.join(E, "data/battle_anim_scripts.s")
MARK = "@ genanims:"


def type_rgb555(name):
    tree = ast.parse(open(os.path.join(ROOT, "tools/gbasprite.py")).read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "TYPE_COLOR" for t in n.targets):
            r, g, b = ast.literal_eval(n.value)[name]
            return "RGB(%d, %d, %d)" % (r >> 3, g >> 3, b >> 3)
    raise SystemExit("gbasprite.py no longer defines TYPE_COLOR")


def powers():
    out = {}
    for mv, body in re.findall(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \}", open(os.path.join(E, "src/data/battle_moves.h")).read(), re.S):
        out[mv] = int(re.search(r"\.power = (\d+)", body).group(1))
    return out


# ---- the steps. Each returns script lines. `c` is the type colour, `se` the routine's own vanilla sound. ----
GREY = "RGB(13, 13, 13)"


def blend(sel, delay, a, b, col):
    return ["\tcreatevisualtask AnimTask_BlendBattleAnimPal, 10, %s, %d, %d, %d, %s" % (sel, delay, a, b, col)]


def wait():
    return ["\twaitforvisualfinish"]


def sound(se, side="SOUND_PAN_TARGET"):
    return ["\tplaysewithpan %s, %s" % (se, side)] if se else []


def send(c, k=6):
    """The routine runs: the attacker's colour pulses toward its type and back. It does not move."""
    return blend("F_PAL_ATTACKER", 0, 0, k, c) + wait() + blend("F_PAL_ATTACKER", 0, k, 0, c) + wait()


def strength(power):
    #  Blend depth, shake amplitude (px) and shake count. The first table (6+p/20, 1+p/40, 2+p/40) gave WRITE a
    #  one-pixel shake twice over -- invisible at 1:1 -- so the floor is two pixels, three shakes, depth nine.
    p = max(power, 20)
    return min(14, 7 + p // 15), min(5, 2 + p // 40), min(7, 3 + p // 30)


def land(c, power, se, times=1):
    """The write lands: the target takes the type's colour, as deep as the power, and shakes as hard."""
    k, amp, n = strength(power)
    out = []
    for _ in range(times):
        out += sound(se) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (amp, n)]
        out += blend("F_PAL_TARGET", 0, 0, k, c) + wait() + blend("F_PAL_TARGET", 0, k, 0, c) + wait()
    return out


def cut(c, power, se):
    """An edge, not a weight: two thin, fast flashes and no shake."""
    k, _, _ = strength(power)
    out = []
    for _ in range(2):
        out += sound(se) + blend("F_PAL_TARGET", 0, 0, k, c) + wait() + blend("F_PAL_TARGET", 0, k, 0, c) + wait()
    return out


def recoil():
    """Recoil costs the attacker: a short dip toward grey."""
    return ["\tdelay 4"] + blend("F_PAL_ATTACKER", 0, 0, 8, GREY) + wait() + blend("F_PAL_ATTACKER", 1, 8, 0, GREY) + wait()


def hold(c, power, se, beats=3):
    """Binding: the target is held in the type's colour and shaken in short beats while held."""
    k, amp, _ = strength(power)
    out = sound(se) + blend("F_PAL_TARGET", 1, 0, k, c) + wait()
    for _ in range(beats):
        out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 0, %d, 2, 2" % max(1, amp - 1), "\tdelay 8"] + sound(se)
    return out + wait() + blend("F_PAL_TARGET", 1, k, 0, c) + wait()


def field(c, se, pulses=2):
    """A write to everything in range at once -- sound, noise: the field pulses in the type's colour."""
    out = []
    for _ in range(pulses):
        out += sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_BG | F_PAL_DEF_SIDE", 0, 0, 8, c) + wait()
        out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 2, 0, 3, 1"] + blend("F_PAL_BG | F_PAL_DEF_SIDE", 0, 8, 0, c) + wait()
    return out


def terminate(c, se):
    """A one-hit KO: the target's process ends -- drained to black -- and the frame then shows whether it did."""
    return send(c, 10) + sound(se) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 4, 0, 6, 1"] + \
        blend("F_PAL_TARGET", 0, 0, 16, "RGB_BLACK") + wait() + ["\tdelay 10"] + blend("F_PAL_TARGET", 2, 16, 0, "RGB_BLACK") + wait()


def halve(c, se):
    """Halving: the target drains exactly half-way to grey, holds, and returns."""
    return send(c) + sound(se) + blend("F_PAL_TARGET", 0, 0, 8, GREY) + wait() + ["\tdelay 12"] + blend("F_PAL_TARGET", 1, 8, 0, GREY) + wait()


def equalise(c, se):
    """Both sides brought to the same level: attacker and target grey to one depth together, then return."""
    both = "F_PAL_ATTACKER | F_PAL_TARGET"
    return send(c) + sound(se) + blend(both, 1, 0, 8, GREY) + wait() + ["\tdelay 12"] + blend(both, 1, 8, 0, GREY) + wait()


def explode(c, se):
    """Self-destruct: the attacker spends itself -- greyed out entirely -- under a full-field flash of its type."""
    return blend("F_PAL_ATTACKER", 1, 0, 16, GREY) + wait() + sound(se, "SOUND_PAN_ATTACKER") + \
        ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 4, 0, 8, 1"] + blend("F_PAL_BG | F_PAL_DEF_SIDE", 0, 0, 16, c) + wait() + \
        blend("F_PAL_BG | F_PAL_DEF_SIDE", 2, 16, 0, c) + wait() + blend("F_PAL_ATTACKER", 0, 16, 0, GREY) + wait()


def beam(c, power, se):
    """The heaviest write: the attacker's colour loads slowly, the field flashes, the target is held long."""
    k, amp, _ = strength(power)
    return blend("F_PAL_ATTACKER", 2, 0, 12, c) + wait() + sound(se, "SOUND_PAN_ATTACKER") + \
        blend("F_PAL_BG", 0, 0, 6, c) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, 10, 1" % amp] + \
        blend("F_PAL_TARGET", 0, 0, 14, c) + wait() + ["\tdelay 16"] + blend("F_PAL_TARGET", 1, 14, 0, c) + \
        blend("F_PAL_BG", 1, 6, 0, c) + blend("F_PAL_ATTACKER", 1, 12, 0, c) + wait()


def charge(c, power, se, name):
    """Two turns: on the first the routine loads (the attacker held in its colour); on the second it lands."""
    return ["\tchoosetwoturnanim %sLoad, %sRun" % (name, name), "%sDone:" % name, "\tend", "%sLoad:" % name] + \
        blend("F_PAL_ATTACKER", 2, 0, 10, c) + wait() + ["\tdelay 12"] + blend("F_PAL_ATTACKER", 2, 10, 0, c) + wait() + \
        ["\tgoto %sDone" % name, "%sRun:" % name] + send(c, 10) + land(c, power, se) + ["\tgoto %sDone" % name]


def spin(c):
    """Spinning free: three quick pulses of the attacker's own colour."""
    out = []
    for _ in range(3):
        out += blend("F_PAL_ATTACKER", 0, 0, 7, c) + wait() + blend("F_PAL_ATTACKER", 0, 7, 0, c) + wait()
    return out


def take(c):
    """Something taken back to the attacker: after the landing, the attacker's own pulse answers it."""
    return ["\tdelay 4"] + send(c, 8)


# ---- the CONTENT table. Every routine of the family, vanilla id -> its steps. power is read from the game. ----
def content_table():
    std = lambda send_first=True, times=1: (lambda c, p, se, n: (send(c) if send_first else []) + land(c, p, se, times))
    t = {}
    for mv in ["POUND", "SCRATCH", "VICE_GRIP", "HEADBUTT", "HORN_ATTACK", "STOMP", "TACKLE", "SLAM", "BODY_SLAM",
               "MEGA_PUNCH", "MEGA_KICK", "DIZZY_PUNCH", "SMELLING_SALT", "CRUSH_CLAW", "FACADE", "FRUSTRATION", "RETURN",
               "SECRET_POWER", "HIDDEN_POWER", "WEATHER_BALL", "PRESENT", "FLAIL", "SWIFT", "EGG_BOMB", "SONIC_BOOM"]:
        t[mv] = std()
    for mv in ["DOUBLE_SLAP", "COMET_PUNCH", "FURY_ATTACK", "FURY_SWIPES", "BARRAGE", "SPIKE_CANNON"]:
        t[mv] = std(send_first=False)                     # multi-hit: each hit plays the animation, so each is lean
    for mv in ["QUICK_ATTACK", "FAKE_OUT"]:
        t[mv] = std(send_first=False)                     # priority: no windup at all
    t["EXTREME_SPEED"] = std(send_first=False, times=2)
    t["FALSE_SWIPE"] = lambda c, p, se, n: send(c) + land(c, 20, se)   # it never finishes: drawn as the lightest write
    for mv in ["CUT", "SLASH", "HYPER_FANG"]:
        t[mv] = lambda c, p, se, n: send(c) + cut(c, p, se)
    for mv in ["TAKE_DOWN", "DOUBLE_EDGE", "STRUGGLE"]:
        t[mv] = lambda c, p, se, n: send(c) + land(c, p, se) + recoil()
    for mv in ["WRAP", "BIND", "CONSTRICT"]:
        t[mv] = lambda c, p, se, n: send(c) + hold(c, p, se)
    for mv in ["THRASH", "RAGE"]:
        t[mv] = std(times=2)
    t["STRENGTH"] = lambda c, p, se, n: send(c) + land(c, 120, se)     # displacement: shoves harder than its number
    for mv in ["UPROAR", "HYPER_VOICE", "SNORE"]:
        t[mv] = lambda c, p, se, n: field(c, se)
    t["TRI_ATTACK"] = std(send_first=False, times=3)
    t["RAPID_SPIN"] = lambda c, p, se, n: spin(c) + land(c, p, se)
    t["PAY_DAY"] = lambda c, p, se, n: send(c) + land(c, p, se) + take(c)
    t["COVET"] = lambda c, p, se, n: send(c) + land(c, p, se) + take(c)
    t["SPIT_UP"] = lambda c, p, se, n: blend("F_PAL_ATTACKER", 0, 0, 10, GREY) + wait() + blend("F_PAL_ATTACKER", 1, 10, 0, GREY) + wait() + land(c, 100, se)
    t["GUILLOTINE"] = lambda c, p, se, n: terminate(c, se)
    t["HORN_DRILL"] = lambda c, p, se, n: terminate(c, se)
    t["SUPER_FANG"] = lambda c, p, se, n: halve(c, se)
    t["ENDEAVOR"] = lambda c, p, se, n: equalise(c, se)
    for mv in ["SELF_DESTRUCT", "EXPLOSION"]:
        t[mv] = lambda c, p, se, n: explode(c, se)
    t["HYPER_BEAM"] = lambda c, p, se, n: beam(c, p, se)
    for mv in ["SKULL_BASH", "RAZOR_WIND", "BIDE"]:
        t[mv] = (lambda mv: lambda c, p, se, n: charge(c, p if p else 80, se, "Daemons" + "".join(w.capitalize() for w in mv.split("_"))))(mv)
    return t


FAMILIES = {"CONTENT": ("NORMAL", content_table)}


def first_sound(text):
    m = re.search(r"\b(SE_M_\w+|SE_\w+)\b", text)
    return m.group(1) if m else "SE_M_COMET_PUNCH"


def region(s, mv):
    """[start, end) of Move_X's region: its label up to the next Move_ label."""
    m = re.search(r"^Move_%s:\n" % mv, s, re.M)
    if not m:
        raise SystemExit("no Move_%s in the scripts" % mv)
    nxt = re.search(r"^Move_\w+:\n", s[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(s) - m.end())
    # a genanims header comment written above the NEXT label belongs to the next region
    while True:
        k = s.rfind("\n", m.start(), end - 1)
        line = s[k + 1:end]
        if line.startswith("@") and k > m.start():
            end = k + 1
        else:
            break
    return m.start(), end


def main():
    args = sys.argv[1:]
    if not args or args[0] not in FAMILIES:
        raise SystemExit(__doc__)
    fam = args[0]
    tname, make = FAMILIES[fam]
    colour = type_rgb555(tname)
    table = make()
    pw = powers()
    #  The table must be the whole family and nothing else, as animcensus.py files it: every routine of this
    #  type with power, and no other. A routine left out stays vanilla silently; one added redraws a stranger.
    moves_h = open(os.path.join(E, "src/data/battle_moves.h")).read()
    family = {mv for mv, body in re.findall(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \}", moves_h, re.S)
              if "TYPE_%s," % tname in body and int(re.search(r"\.power = (\d+)", body).group(1)) > 0}
    if family != set(table):
        raise SystemExit("table and family differ -- missing %s, extra %s" % (sorted(family - set(table)), sorted(set(table) - family)))
    s = open(SCRIPTS).read()
    release = "--release" in args
    written = 0
    if release:
        #  A draft block is found by its header and walked LINE BY LINE with a depth count. Two earlier versions
        #  failed on EXPLOSION, whose vanilla carries its own `.if REVISION >= 0xA ... .endif`: a region walk cut
        #  it in the wrong place, and a non-greedy pattern took vanilla's inner .endif for the guard's.
        head = "@ genanims: %s (T-134, vision.md 9.24)" % fam
        lines = s.split("\n")
        out, k = [], 0
        while k < len(lines):
            if lines[k] == head + " DRAFT, debug ROMs only until approved." and k + 2 < len(lines) and lines[k + 2] == ".if DAEMONS_DEBUG":
                out += [head + " approved.", lines[k + 1]]
                k += 3
                depth, keep = 1, True
                while depth:
                    l = lines[k]
                    if l.startswith(".if"):
                        depth += 1
                    elif l == ".endif":
                        depth -= 1
                    elif l == ".else" and depth == 1:
                        keep = False
                        k += 1
                        continue
                    if depth and keep:
                        out.append(l)
                    k += 1
                written += 1
                continue
            out.append(lines[k])
            k += 1
        s = "\n".join(out)
        if head + " DRAFT" in s:
            raise SystemExit("a %s draft was not released" % fam)
        print("  %s: %d routines released, type colour %s" % (fam, written, colour))
        open(SCRIPTS, "w").write(s)
        return
    for mv in sorted(table):
        a, b = region(s, "Move_" + mv[5:] if mv.startswith("Move_") else mv)
        text = s[a:b]
        head = "@ genanims: %s (T-134, vision.md 9.24)" % fam
        if release:
            if ".if DAEMONS_DEBUG" not in text:
                continue
            i, e, z = text.index(".if DAEMONS_DEBUG\n"), text.index(".else\n"), text.index(".endif\n")
            draft = text[i + len(".if DAEMONS_DEBUG\n"):e]
            outside = text[z + len(".endif\n"):]
            new = text[:i] + draft + outside
        else:
            if ".if DAEMONS_DEBUG" in text:           # our own earlier draft: recover vanilla from its .else
                e, z = text.index(".else\n"), text.index(".endif\n")
                vanilla = text[e + len(".else\n"):z]
                keep = text[z + len(".endif\n"):]
            else:
                vanilla, keep = text[text.index("\n") + 1:], ""
            # subroutines defined in vanilla's region and called from anywhere else stay outside the guard
            rest = s[:a] + s[b:]
            shared = [l for l in re.findall(r"^(\w+):\n", vanilla, re.M) if re.search(r"\b%s\b" % l, rest)]
            if shared:
                cutat = min(vanilla.index(l + ":\n") for l in shared)
                keep = vanilla[cutat:] + keep
                vanilla = vanilla[:cutat]
                for l in re.findall(r"^(\w+):\n", vanilla, re.M):
                    if re.search(r"\b%s\b" % l, keep):
                        raise SystemExit("Move_%s: shared code after %s jumps back into %s; split it by hand" % (mv, cutat, l))
            se = first_sound(vanilla + keep)           # a shared subroutine may carry the sound (SELF_DESTRUCT's does)
            body = table[mv](colour, pw.get(mv, 0), se, mv)
            new = ("%s DRAFT, debug ROMs only until approved.\nMove_%s:\n.if DAEMONS_DEBUG\n" % (head, mv) +
                   "\n".join(body) + ("\n" if body[-1] == "\tend" else "\n\tend\n") + ".else\n" + vanilla + ".endif\n" + keep)
            # the label line and any previous genanims header are replaced; other comments above are kept
        pre = s[:a]
        if pre.endswith("DRAFT, debug ROMs only until approved.\n"):
            pre = pre[:pre.rfind(MARK)]
            if release:
                pre += "%s approved.\n" % head
        s = pre + new + s[b:]
        written += 1
    print("  %s: %d routines %s, type colour %s" % (fam, written, "released" if release else "drafted", colour))
    if "--write" in args or release:
        open(SCRIPTS, "w").write(s)
    else:
        print("  (report only; --write to write)")


if __name__ == "__main__":
    main()

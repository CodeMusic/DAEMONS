#!/usr/bin/env python3
"""Battle animations for a family of routines, generated from one visual vocabulary (T-134; vision.md 9.24).

    python3 tools/genanims.py CONTENT            # report what would be written (families: CONTENT LOWER AFFLICT RAISE FIELD LOGIC VECTOR GROWTH FLOW ENTROPY STRATUM SIGNAL CORRUPT CONTEXT SWARM FROZEN PROTECT OPAQUE)
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



# ---- the STATE vocabulary (T-141 LOWER, T-142 AFFLICT, T-143 RAISE): a daemon's numbers and state changed. ----
#  Colour here is each routine's OWN type (9.24.3), so a SIGNAL paralysis flickers teal and a CORRUPT poison creeps
#  in mould. Up is toward that colour, down is toward grey (9.24.2), and a stage is a step: +2 is drawn as two.

def tick_se():
    return ["\tplaysewithpan SE_M_MINIMIZE, SOUND_PAN_ATTACKER"]


def rise(c, stages, se, fast=False, stats=1):
    """A parameter of its own turned up: the user's colour climbs toward the routine's type, one step a stage."""
    out = sound(se, "SOUND_PAN_ATTACKER")
    for _ in range(stats):
        level = 0
        for _ in range(stages):
            out += tick_se() + blend("F_PAL_ATTACKER", 0 if fast else 1, level, level + 6, c) + wait()
            level += 6
        out += ["\tdelay %d" % (4 if fast else 10)] + blend("F_PAL_ATTACKER", 0 if fast else 2, level, 0, c) + wait()
        if fast:                                           # speed: the same climb, three times as quick
            out += blend("F_PAL_ATTACKER", 0, 0, 6, c) + wait() + blend("F_PAL_ATTACKER", 0, 6, 0, c) + wait()
    return out


def flicker_self(c, se):
    """Evasion up: harder to pin down -- the user flickers between its colour and the routine's."""
    out = sound(se, "SOUND_PAN_ATTACKER")
    for _ in range(4):
        out += blend("F_PAL_ATTACKER", 0, 0, 10, c) + wait() + blend("F_PAL_ATTACKER", 0, 10, 0, c) + wait()
    return out


def sink(c, stages, se, sound_wave=False, accuracy=False, slow=False):
    """A parameter of the target turned down: the routine's colour touches it, then it sinks toward grey a step a stage."""
    out = send(c)
    if sound_wave:
        out += sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_BG", 0, 0, 6, c) + wait() + blend("F_PAL_BG", 0, 6, 0, c) + wait()
    else:
        out += sound(se)
    out += blend("F_PAL_TARGET", 0, 0, 8, c) + wait() + blend("F_PAL_TARGET", 0, 8, 0, c) + wait()
    sel = "F_PAL_TARGET | F_PAL_BG" if accuracy else "F_PAL_TARGET"   # it cannot see: the field it reads dims too
    level = 0
    for _ in range(stages):
        out += tick_se() + blend(sel, 1, level, level + 5, GREY) + wait()
        level += 5
    return out + ["\tdelay 10"] + blend(sel, 3 if slow else 1, level, 0, GREY) + wait()


def afflict(kind, c, se):
    """A fault put into the target, each with its own pattern, in the routine's own colour."""
    out = send(c) + sound(se)
    T = "F_PAL_TARGET"
    if kind in ("sleep", "yawn"):                        # suspended: a slow fade to grey that holds
        depth, d = (12, 3) if kind == "sleep" else (7, 4)
        out += blend(T, 0, 0, 6, c) + wait() + blend(T, 0, 6, 0, c) + wait() + blend(T, d, 0, depth, GREY) + wait()
        out += ["\tdelay 16"] + blend(T, 2, depth, 0, GREY) + wait()
    elif kind in ("poison", "toxic"):                    # it creeps: the colour seeps in by steps
        n = 4 if kind == "toxic" else 3
        for i in range(n):
            out += tick_se() + blend(T, 2, i * 4, (i + 1) * 4, c) + wait()
        out += ["\tdelay 8"] + blend(T, 1, n * 4, 0, c) + wait()
    elif kind == "paralyze":                             # a voltage sag: it flickers
        out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 1, 0, 8, 1"]
        for _ in range(4):
            out += blend(T, 0, 0, 10, c) + wait() + blend(T, 0, 10, 0, c) + wait()
    elif kind == "burn":                                 # heat that stays: two slow pulses
        for _ in range(2):
            out += blend(T, 2, 0, 12, c) + wait() + blend(T, 2, 12, 0, c) + wait()
    elif kind in ("confuse", "swagger", "teeter"):       # two states at once: colour and grey, alternating
        if kind == "swagger":                            # it is also turned UP first -- the flattery is real
            out += blend(T, 1, 0, 10, c) + wait() + blend(T, 1, 10, 0, c) + wait()
        sel = "F_PAL_DEF_SIDE" if kind == "teeter" else T
        out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 3, 0, 6, 2"]
        for _ in range(3):
            out += blend(sel, 0, 0, 9, c) + wait() + blend(sel, 0, 9, 0, c) + wait()
            out += blend(sel, 0, 0, 9, GREY) + wait() + blend(sel, 0, 9, 0, GREY) + wait()
    elif kind == "attract":                              # paired: both pulse in step
        for _ in range(2):
            out += blend("F_PAL_ATTACKER | F_PAL_TARGET", 1, 0, 10, c) + wait() + blend("F_PAL_ATTACKER | F_PAL_TARGET", 1, 10, 0, c) + wait()
    else:
        raise SystemExit("no affliction pattern for %s" % kind)
    return out


def effect_of(mv):
    body = re.search(r"\[MOVE_%s\]\s*=\s*\{(.*?)\n    \}" % mv, open(os.path.join(E, "src/data/battle_moves.h")).read(), re.S).group(1)
    return re.search(r"\.effect = EFFECT_(\w+)", body).group(1)


def census_family(name):
    import importlib.util
    spec = importlib.util.spec_from_file_location("animcensus", os.path.join(ROOT, "tools/animcensus.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return [r["move"][5:] for r in mod.census() if r["family"] == name]


SOUND_WAVE = {"GROWL", "SCREECH", "METAL_SOUND"}


def lower_table():
    t = {}
    for mv in census_family("LOWER"):
        e = effect_of(mv)
        stages = 2 if e.endswith("_2") else 1
        t[mv] = (lambda stages, e, mv: lambda c, p, se, n: sink(c, stages, se, sound_wave=mv in SOUND_WAVE,
                 accuracy=e.startswith("ACCURACY"), slow=e.startswith("SPEED")))(stages, e, mv)
    return t


AFFLICTION = {"SLEEP": "sleep", "YAWN": "yawn", "POISON": "poison", "TOXIC": "toxic", "PARALYZE": "paralyze",
              "WILL_O_WISP": "burn", "CONFUSE": "confuse", "SWAGGER": "swagger", "FLATTER": "swagger",
              "TEETER_DANCE": "teeter", "ATTRACT": "attract"}


def afflict_table():
    return {mv: (lambda k: lambda c, p, se, n: afflict(k, c, se))(AFFLICTION[effect_of(mv)]) for mv in census_family("AFFLICT")}


MULTI_STAT = {"CALM_MIND": 2, "BULK_UP": 2, "DRAGON_DANCE": 2, "COSMIC_POWER": 2}


def raise_table():
    t = {}
    for mv in census_family("RAISE"):
        e = effect_of(mv)
        if e in ("EVASION_UP", "MINIMIZE"):
            t[mv] = lambda c, p, se, n: flicker_self(c, se)
            continue
        stages = 2 if e.endswith("_2") else 1
        t[mv] = (lambda stages, e: lambda c, p, se, n: rise(c, stages, se, fast=e.startswith("SPEED"), stats=MULTI_STAT.get(e, 1)))(stages, e)
    return t


# ---- the FIELD vocabulary (T-144): routines that change the ground, a side, or what a daemon may do next. ----
#  The four weathers are REPLAYED every turn they last (General_Sun/Sandstorm/Hail jump into them; General_Rain is
#  pointed at RAIN DANCE to match), so they are kept short. Four routines carry MECHANICS inside their animation --
#  ROAR and WHIRLWIND slide the target off (the switch depends on it), TELEPORT hides the user, BATON PASS runs the
#  sprite that recalls it, CAMOUFLAGE fades the user out and back -- and those tasks are kept; only the picture goes.

WHOLE = "F_PAL_BG | F_PAL_BATTLERS"


def weather(c, se):
    """The ground both sides run on changes: the field takes the routine's colour, briefly, every turn it holds."""
    return sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_BG", 1, 0, 9, c) + wait() + ["\tdelay 12"] + blend("F_PAL_BG", 1, 9, 0, c) + wait()


def screen(c, se):
    """A side protected: the user's side holds a pale layer of the routine's colour, twice."""
    out = sound(se, "SOUND_PAN_ATTACKER")
    for _ in range(2):
        out += blend("F_PAL_ATK_SIDE", 1, 0, 8, c) + wait() + ["\tdelay 6"] + blend("F_PAL_ATK_SIDE", 1, 8, 0, c) + wait()
    return out


def lay(c, se, times=3):
    """Something placed on the other side that will act later: laid down in ticks of the routine's colour."""
    out = send(c)
    for _ in range(times):
        out += sound(se) + blend("F_PAL_TARGET", 0, 0, 7, c) + wait() + blend("F_PAL_TARGET", 0, 7, 0, c) + wait() + ["\tdelay 4"]
    return out


def clamp(c, se, times=1):
    """A restriction: the routine's colour, then a hard snap toward grey held a moment -- something is now locked."""
    out = send(c)
    for _ in range(times):
        out += sound(se) + blend("F_PAL_TARGET", 0, 0, 10, c) + wait() + blend("F_PAL_TARGET", 0, 10, 0, c) + wait()
        out += tick_se() + blend("F_PAL_TARGET", 0, 0, 12, GREY) + wait() + ["\tdelay 8"] + blend("F_PAL_TARGET", 1, 12, 0, GREY) + wait()
    return out


def deplete(c, se):
    """SPITE: what the target has left is drawn down, three ticks toward grey."""
    out = send(c) + sound(se)
    for i in range(3):
        out += tick_se() + blend("F_PAL_TARGET", 1, i * 4, (i + 1) * 4, GREY) + wait()
    return out + ["\tdelay 6"] + blend("F_PAL_TARGET", 1, 12, 0, GREY) + wait()


def reveal(c, se, hold=10):
    """Seen clearly / aimed at: the target is lit (white is neutral, not colour) and held while it is read."""
    return send(c) + sound(se) + blend("F_PAL_TARGET", 1, 0, 9, "RGB_WHITE") + wait() + ["\tdelay %d" % hold] + blend("F_PAL_TARGET", 1, 9, 0, "RGB_WHITE") + wait()


def reset_all(se, steps=1):
    """Everything returned to a common state: the whole field greys and comes back (HAZE); PERISH SONG counts it down."""
    out = sound(se, "SOUND_PAN_ATTACKER")
    for i in range(steps):
        out += tick_se() + blend(WHOLE, 1, i * (12 // steps), (i + 1) * (12 // steps), GREY) + wait() + ["\tdelay 8"]
    return out + blend(WHOLE, 1, 12, 0, GREY) + wait()


def bond(c, se):
    """Two processes tied together (DESTINY BOND, GRUDGE): both pulse in step, once in the colour and once in grey."""
    both = "F_PAL_ATTACKER | F_PAL_TARGET"
    return sound(se) + blend(both, 1, 0, 10, c) + wait() + blend(both, 1, 10, 0, c) + wait() + blend(both, 1, 0, 10, GREY) + wait() + blend(both, 1, 10, 0, GREY) + wait()


def memento(c, se):
    """The user spends itself to weaken the target: it greys out entirely while the target dips."""
    return sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_ATTACKER", 1, 0, 16, GREY) + wait() + blend("F_PAL_TARGET", 0, 0, 8, GREY) + wait() + \
        blend("F_PAL_TARGET", 1, 8, 0, GREY) + wait() + blend("F_PAL_ATTACKER", 0, 16, 0, GREY) + wait()


def evict(c, se, speed):
    """Forced out: the routine's colour, the target greyed, and vanilla's own slide off the screen, which the switch needs."""
    return send(c) + sound(se) + blend("F_PAL_TARGET", 0, 0, 10, GREY) + wait() + \
        ["\tcreatevisualtask AnimTask_SlideOffScreen, 5, ANIM_TARGET, %d" % speed] + wait() + blend("F_PAL_TARGET", 0, 10, 0, GREY) + wait()


def teleport(c, se):
    """Gone: the user greys and vanilla's own task removes it."""
    return blend("F_PAL_ATTACKER", 0, 0, 12, GREY) + wait() + ["\tcreatevisualtask AnimTask_Teleport, 2"] + sound(se, "SOUND_PAN_ATTACKER") + \
        ["\tdelay 15"] + wait() + blend("F_PAL_ATTACKER", 0, 12, 0, GREY) + wait()


def baton_pass(c, se):
    """State handed on: the user pulses its routine's colour, then vanilla's recall sprite runs as it must."""
    return ["\tloadspritegfx ANIM_TAG_POKEBALL"] + sound(se, "SOUND_PAN_ATTACKER") + send(c, 10) + ["\tcreatesprite gBatonPassPokeballSpriteTemplate, ANIM_ATTACKER, 2"]


def camouflage(c, se):
    """Blending into the ground: the user greys toward the field and fades out and back, by vanilla's own fade tasks."""
    return ["\tmonbg ANIM_ATK_PARTNER", "\tsplitbgprio ANIM_ATTACKER", "\tsetalpha 16, 0"] + blend("F_PAL_ATTACKER", 1, 0, 12, GREY) + wait() + \
        ["\tcreatevisualtask AnimTask_AttackerFadeToInvisible, 2, 4"] + sound(se, "SOUND_PAN_ATTACKER") + wait() + ["\tdelay 8"] + \
        blend("F_PAL_ATTACKER", 0, 12, 0, GREY) + wait() + ["\tcreatevisualtask AnimTask_AttackerFadeFromInvisible, 2, 1"] + wait() + ["\tblendoff", "\tclearmonbg ANIM_ATK_PARTNER"]


def noop(c, se):
    """NO-OP: nothing happens, exactly on time."""
    return sound(se, "SOUND_PAN_ATTACKER") + ["\tdelay 20"]


def nightmare(c, se):
    """A sleeping target's fault fed: slow flickers of the routine's colour over grey."""
    out = sound(se) + blend("F_PAL_TARGET", 1, 0, 8, GREY) + wait()
    for _ in range(3):
        out += blend("F_PAL_TARGET", 0, 8, 12, c) + wait() + blend("F_PAL_TARGET", 0, 12, 8, GREY) + wait()
    return out + blend("F_PAL_TARGET", 1, 8, 0, GREY) + wait()


def curse(se):
    """CURSE branches as vanilla's does: a LATENT user pays in grey and marks the target; any other climbs twice and slows."""
    lat = type_rgb555("GHOST")
    return ["\tchoosetwoturnanim DaemonsCurseLatent, DaemonsCurseStats", "DaemonsCurseDone:", "\tend", "DaemonsCurseLatent:"] + \
        blend("F_PAL_ATTACKER", 1, 0, 12, GREY) + wait() + bond(lat, se) + ["\tgoto DaemonsCurseDone", "DaemonsCurseStats:"] + \
        rise(lat, 1, se, stats=2) + blend("F_PAL_ATTACKER", 1, 0, 6, GREY) + wait() + blend("F_PAL_ATTACKER", 2, 6, 0, GREY) + wait() + ["\tgoto DaemonsCurseDone"]


def field_table():
    f = lambda fn, *a: (lambda c, p, se, n: fn(c, se, *a))
    t = {}
    for mv in ["SANDSTORM", "RAIN_DANCE", "HAIL", "SUNNY_DAY"]:
        t[mv] = f(weather)
    for mv in ["REFLECT", "LIGHT_SCREEN", "SAFEGUARD", "MIST", "WATER_SPORT", "MUD_SPORT"]:
        t[mv] = f(screen)
    t["SPIKES"] = f(lay)
    t["LEECH_SEED"] = f(lay)
    for mv in ["DISABLE", "TAUNT", "TORMENT", "IMPRISON", "MEAN_LOOK", "SPIDER_WEB", "BLOCK"]:
        t[mv] = f(clamp)
    t["ENCORE"] = f(clamp, 2)
    t["SPITE"] = f(deplete)
    for mv in ["FORESIGHT", "ODOR_SLEUTH"]:
        t[mv] = f(reveal)
    for mv in ["LOCK_ON", "MIND_READER"]:
        t[mv] = f(reveal, 20)
    t["HAZE"] = lambda c, p, se, n: reset_all(se)
    t["PERISH_SONG"] = lambda c, p, se, n: reset_all(se, 3)
    for mv in ["DESTINY_BOND", "GRUDGE"]:
        t[mv] = f(bond)
    t["MEMENTO"] = f(memento)
    t["ROAR"] = f(evict, 2)
    t["WHIRLWIND"] = f(evict, 8)
    t["TELEPORT"] = f(teleport)
    t["BATON_PASS"] = f(baton_pass)
    t["CAMOUFLAGE"] = f(camouflage)
    t["SPLASH"] = f(noop)
    t["NIGHTMARE"] = f(nightmare)
    t["TICKLE"] = lambda c, p, se, n: sink(c, 1, se) + sink(c, 1, se)
    for mv in ["CHARGE", "FOCUS_ENERGY"]:
        t[mv] = lambda c, p, se, n: rise(c, 1, se)
    t["CURSE"] = lambda c, p, se, n: curse(se)
    return t


# ---- the LOGIC vocabulary (T-145): "formal rules applied step by step; proof, not intuition" (vision.md 2.8). ----
#  Where a CONTENT write lands in one pulse, a LOGIC write lands as a DERIVATION: the target takes the colour in
#  ordered steps, each with its tick -- each licensed by the last -- and then, concluded, the whole thing lets go at
#  once. How many steps is read off the power, so a stronger proof has more lines.

def derive(c, power, se, lean=False, shake=True, steps=None):
    """A stepped landing: premise (the attacker's pulse), then the target in ordered ticked steps, then Q.E.D."""
    k, amp, n = strength(power)
    if steps is None:
        steps = min(4, 2 + power // 45)
    each = max(3, k // steps)
    out = [] if lean else send(c)
    level = 0
    for i in range(steps):
        out += tick_se() + blend("F_PAL_TARGET", 0, level, level + each, c) + wait()
        level += each
        if not lean:
            out += ["\tdelay 2"]
    out += sound(se)
    if shake:
        out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (amp, n)]
    return out + ["\tdelay 4"] + blend("F_PAL_TARGET", 0, level, 0, c) + wait()


def returned(c, power, se):
    """A rebuttal (COUNTER, REVENGE, REVERSAL): the argument received is derived back -- the user steps up first,
    then hands the same steps to the target."""
    out = []
    level = 0
    for _ in range(2):
        out += tick_se() + blend("F_PAL_ATTACKER", 0, level, level + 5, c) + wait()
        level += 5
    out += blend("F_PAL_ATTACKER", 0, level, 0, c) + wait()
    return out + derive(c, power, se, lean=True)


def non_sequitur(c, power, se):
    """NON SEQUITUR: the steps do not follow -- a small step, a jump past where the next should be, a step BACK --
    and the target is left alternating, as confused by it as the move leaves it."""
    k, amp, n = strength(power)
    out = send(c) + tick_se() + blend("F_PAL_TARGET", 0, 0, 3, c) + wait() + tick_se() + blend("F_PAL_TARGET", 0, 3, 12, c) + wait()
    out += tick_se() + blend("F_PAL_TARGET", 0, 12, 6, c) + wait() + sound(se) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (amp, n)]
    out += blend("F_PAL_TARGET", 0, 6, 0, c) + wait() + blend("F_PAL_TARGET", 0, 0, 8, GREY) + wait() + blend("F_PAL_TARGET", 0, 8, 0, GREY) + wait()
    return out


def loop_back(c, power, se):
    """LOOP BACK: the derivation climbs and returns to its start, twice, before it lands."""
    out = send(c)
    for _ in range(2):
        out += tick_se() + blend("F_PAL_TARGET", 0, 0, 6, c) + wait() + blend("F_PAL_TARGET", 0, 6, 0, c) + wait()
    return out + derive(c, power, se, lean=True)


def falsify(c, power, se):
    """FALSIFY breaks screens: on the turn it does (turn 1), the defending side's layer greys and is gone first."""
    return ["\tchoosetwoturnanim DaemonsFalsifyPlain, DaemonsFalsifyScreen", "DaemonsFalsifyDone:", "\tend", "DaemonsFalsifyPlain:"] + \
        derive(c, power, se) + ["\tgoto DaemonsFalsifyDone", "DaemonsFalsifyScreen:"] + \
        blend("F_PAL_DEF_SIDE", 0, 0, 10, c) + wait() + tick_se() + blend("F_PAL_DEF_SIDE", 0, 0, 12, GREY) + wait() + blend("F_PAL_DEF_SIDE", 1, 12, 0, GREY) + wait() + \
        derive(c, power, se) + ["\tgoto DaemonsFalsifyDone"]


def logic_table():
    t = {}
    for mv in ["ROCK_SMASH", "KARATE_CHOP", "JUMP_KICK", "HI_JUMP_KICK", "CROSS_CHOP", "VITAL_THROW", "SKY_UPPERCUT", "LOW_KICK", "DYNAMIC_PUNCH"]:
        t[mv] = lambda c, p, se, n: derive(c, p, se)
    t["DYNAMIC_PUNCH"] = lambda c, p, se, n: non_sequitur(c, p, se)
    for mv in ["DOUBLE_KICK", "TRIPLE_KICK", "ARM_THRUST"]:        # each hit plays the animation: one short derivation each
        t[mv] = lambda c, p, se, n: derive(c, p, se, lean=True, steps=2)
    t["MACH_PUNCH"] = lambda c, p, se, n: derive(c, p, se, lean=True)           # priority: no premise, straight to the steps
    t["SEISMIC_TOSS"] = lambda c, p, se, n: derive(c, 80, se, steps=3)          # EQUATE: a fixed result, the same three lines every time
    t["FOCUS_PUNCH"] = lambda c, p, se, n: derive(c, p, se, steps=3)            # SYLLOGISM: two premises and a conclusion
    for mv in ["COUNTER", "REVENGE", "REVERSAL"]:
        t[mv] = lambda c, p, se, n: returned(c, p if p else 60, se)
    t["SUBMISSION"] = lambda c, p, se, n: derive(c, p, se) + recoil()
    t["SUPERPOWER"] = lambda c, p, se, n: derive(c, p, se) + recoil() + recoil()   # BRUTE FORCE costs two of its own stats
    t["ROLLING_KICK"] = lambda c, p, se, n: loop_back(c, p, se)
    t["BRICK_BREAK"] = lambda c, p, se, n: falsify(c, p, se)
    return t


# ---- the VECTOR vocabulary (T-146): "direction in a space of meanings" -- delivery with a heading (2.8). ----
#  A CONTENT write lands in place and a LOGIC write lands in steps; a VECTOR write TRAVELS. It leaves the user (its
#  colour pulses and lets go), crosses the field (the ground flickers in the routine's red while it is in flight),
#  and arrives with a HEADING: the target is shaken along the line it came in on, never up and down.
#  FLY (GOTO) and BOUNCE (REBOUND) hide the user on their first turn -- a mechanic: the battle reads it back as the
#  user being elsewhere -- and that is done with the script's own `invisible` and `visible`, not vanilla's sprites.

def carry(c, power, se, lean=False, sel="F_PAL_TARGET", drift=False, drill=False):
    k, amp, n = strength(power)
    out = [] if lean else blend("F_PAL_ATTACKER", 0, 0, 8, c) + wait()
    out += ([] if lean else blend("F_PAL_ATTACKER", 0, 8, 0, c)) + blend("F_PAL_BG", 1 if drift else 0, 0, 5, c) + wait()
    out += blend("F_PAL_BG", 0, 5, 0, c) + sound(se)
    out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, %d" % (amp + (1 if drift else 0), n + (2 if drift else 0), 2 if drift else 1)]
    if drill:                                             # TUNNEL: the same point struck again and again
        for _ in range(3):
            out += blend(sel, 0, 0, k, c) + wait() + blend(sel, 0, k, k // 2, c) + wait()
        return out + blend(sel, 0, k // 2, 0, c) + wait()
    return out + blend(sel, 0, 0, k, c) + wait() + blend(sel, 1 if drift else 0, k, 0, c) + wait()


def away_and_back(c, power, se, name, bounce=False):
    """Two turns. The first: the user's colour drains and it is gone -- somewhere else on the map of meanings.
    The second: it is back, and arrives on its heading (REBOUND lands with a vertical jolt: it comes DOWN)."""
    run = ["\tvisible ANIM_ATTACKER"] + carry(c, power, se)
    if bounce:
        run += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 0, 4, 4, 1"] + wait()
    return ["\tchoosetwoturnanim %sAway, %sBack" % (name, name), "%sDone:" % name, "\tend", "%sAway:" % name] + \
        sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_ATTACKER", 0, 0, 12, GREY) + wait() + ["\tinvisible ANIM_ATTACKER"] + \
        blend("F_PAL_ATTACKER", 0, 12, 0, GREY) + wait() + ["\tgoto %sDone" % name, "%sBack:" % name] + run + ["\tgoto %sDone" % name]


def aim_then_carry(c, power, se, name):
    """BALLISTIC: the first turn is the aim -- the user held in its colour while the heading is set; the second, the flight."""
    return ["\tchoosetwoturnanim %sAim, %sFire" % (name, name), "%sDone:" % name, "\tend", "%sAim:" % name] + \
        blend("F_PAL_ATTACKER", 2, 0, 12, c) + wait() + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_ATTACKER, 1, 0, 6, 2", "\tdelay 16"] + \
        blend("F_PAL_ATTACKER", 1, 12, 0, c) + wait() + ["\tgoto %sDone" % name, "%sFire:" % name] + carry(c, power, se) + ["\tgoto %sDone" % name]


def vector_table():
    t = {}
    for mv in ["WING_ATTACK", "AERIAL_ACE", "AEROBLAST"]:
        t[mv] = lambda c, p, se, n: carry(c, p, se)
    t["PECK"] = lambda c, p, se, n: carry(c, p, se, lean=True)
    t["GUST"] = lambda c, p, se, n: carry(c, p, se, drift=True)
    t["AIR_CUTTER"] = lambda c, p, se, n: carry(c, p, se, sel="F_PAL_DEF_SIDE")
    t["DRILL_PECK"] = lambda c, p, se, n: carry(c, p, se, drill=True)
    t["FLY"] = lambda c, p, se, n: away_and_back(c, p, se, "DaemonsGoto")
    t["BOUNCE"] = lambda c, p, se, n: away_and_back(c, p, se, "DaemonsRebound", bounce=True)
    t["SKY_ATTACK"] = lambda c, p, se, n: aim_then_carry(c, p, se, "DaemonsBallistic")
    return t


# ---- the GROWTH vocabulary (T-147): "training: fitting to whatever it is fed" (2.8). ----
#  A GROWTH write lands the way a fit converges: the target's colour overshoots, undershoots and settles in
#  narrowing swings. What it FEEDS on shows too: the drains take colour from the target and step it into the user.
#  INGEST's animation is also played every turn a SEED drains (General_LeechSeedDrain jumps to it), which suits it.

def fit(c, power, se, lean=False, sel="F_PAL_TARGET", swings=None, diverge=False):
    k, amp, n = strength(power)
    out = [] if lean else send(c)
    out += sound(se) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (amp, max(2, n - 1))]
    if diverge:                                           # OVERTRAIN: the swings grow instead of settling
        path = [0, k // 3, k // 6, k * 2 // 3, k // 3, k]
    elif lean:
        path = [0, k, k // 3, k // 2]
    else:
        path = [0, k, k // 3, k * 2 // 3, k // 2]
    for a, b in zip(path, path[1:]):
        out += blend(sel, 0, a, b, c) + wait()
    return out + blend(sel, 1, path[-1], 0, c) + wait()


def feed(c, power, se):
    """A drain: the target gives up colour and the user takes it in, a step for each 20 power."""
    k, amp, n = strength(power)
    steps = max(1, min(3, power // 20))
    out = send(c) + sound(se) + blend("F_PAL_TARGET", 0, 0, k, c) + wait() + blend("F_PAL_TARGET", 1, k, 0, c) + wait()
    level = 0
    for _ in range(steps):
        out += tick_se() + blend("F_PAL_ATTACKER", 0, level, level + 4, c) + wait()
        level += 4
    return out + ["\tdelay 6"] + blend("F_PAL_ATTACKER", 1, level, 0, c) + wait()


def backprop(c, power, se):
    """BACKPROP: the error runs backward first -- target, then user -- and only then does the update land."""
    return blend("F_PAL_TARGET", 0, 0, 6, c) + wait() + blend("F_PAL_TARGET", 0, 6, 0, c) + wait() + \
        blend("F_PAL_ATTACKER", 0, 0, 6, c) + wait() + blend("F_PAL_ATTACKER", 0, 6, 0, c) + wait() + fit(c, power, se, lean=True)


def batch(c, power, se, name):
    """BATCH: turn 1 gathers the batch -- the user fills in three slow steps; turn 2 fits it, field and all."""
    gather = []
    for i in range(3):
        gather += tick_se() + blend("F_PAL_ATTACKER", 2, i * 4, (i + 1) * 4, c) + wait()
    return ["\tchoosetwoturnanim %sGather, %sFit" % (name, name), "%sDone:" % name, "\tend", "%sGather:" % name] + gather + \
        ["\tdelay 8"] + blend("F_PAL_ATTACKER", 1, 12, 0, c) + wait() + ["\tgoto %sDone" % name, "%sFit:" % name] + \
        blend("F_PAL_BG", 0, 0, 6, c) + wait() + fit(c, power, se) + blend("F_PAL_BG", 1, 6, 0, c) + wait() + ["\tgoto %sDone" % name]


def growth_table():
    t = {}
    t["ABSORB"] = lambda c, p, se, n: feed(c, p, se)
    t["MEGA_DRAIN"] = lambda c, p, se, n: feed(c, p, se)
    t["GIGA_DRAIN"] = lambda c, p, se, n: feed(c, p, se)
    t["SOLAR_BEAM"] = lambda c, p, se, n: batch(c, p, se, "DaemonsBatch")
    t["BULLET_SEED"] = lambda c, p, se, n: fit(c, p, se, lean=True)         # MINIBATCH: small, and again
    t["RAZOR_LEAF"] = lambda c, p, se, n: fit(c, p, se, sel="F_PAL_DEF_SIDE")
    t["VINE_WHIP"] = lambda c, p, se, n: backprop(c, p, se)
    t["MAGICAL_LEAF"] = lambda c, p, se, n: fit(c, p, se, lean=True)        # CONVERGE: never misses, settles fast
    t["PETAL_DANCE"] = lambda c, p, se, n: fit(c, p, se, diverge=True) + recoil()
    t["FRENZY_PLANT"] = lambda c, p, se, n: fit(c, p, se) + recoil() + recoil()
    t["LEAF_BLADE"] = lambda c, p, se, n: fit(c, p, se) 
    t["NEEDLE_ARM"] = lambda c, p, se, n: fit(c, p, se, lean=True)
    return t


# ---- the FLOW vocabulary (T-148): "everything running downhill to the lowest point" -- gradient and current (2.8). ----
#  A FLOW write POURS. A current rises across the field, the target fills, and then everything runs downhill: the
#  target drains slowly while the field runs off. Its shake is vertical -- flow goes down. ASCEND climbs against the
#  gradient and falls at once; DESCEND sinks out of sight (the script's own invisible, as GOTO) and surfaces.

def pour(c, power, se, lean=False, sel="F_PAL_TARGET", slow=1, abrupt=False):
    k, amp, n = strength(power)
    out = [] if lean else send(c)
    out += blend("F_PAL_BG", 0 if lean else 1, 0, 6, c) + wait() + sound(se)
    out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 0, %d, %d, %d" % (amp, n, 1 if abrupt else 2)]
    out += blend(sel, 0, 0, k, c) + wait()
    if abrupt:
        return out + blend(sel, 0, k, 0, c) + blend("F_PAL_BG", 0, 6, 0, c) + wait()
    return out + blend(sel, 1 + slow, k, 0, c) + blend("F_PAL_BG", 1 + slow, 6, 0, c) + wait()


def silt():
    """What the water leaves behind (FIREHOSE, MUDDY WATER lower accuracy): the target settles grey a moment."""
    return blend("F_PAL_TARGET", 0, 0, 7, GREY) + wait() + ["\tdelay 6"] + blend("F_PAL_TARGET", 1, 7, 0, GREY) + wait()


def ascend(c, power, se):
    """ASCEND: up the gradient in three ticked steps, then down all at once."""
    k, amp, n = strength(power)
    out = send(c)
    for i in range(3):
        out += tick_se() + blend("F_PAL_TARGET", 0, i * k // 3, (i + 1) * k // 3, c) + wait()
    return out + sound(se) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 0, %d, %d, 1" % (amp, n)] + blend("F_PAL_TARGET", 0, (3 * k) // 3, 0, c) + wait()


def ripples(c, power, se, pops=3, lean=False):
    """Rings spreading: pulses that shrink (RIPPLE), or small pops (SEEP, CAVITATE)."""
    k, amp, n = strength(power)
    out = [] if lean else send(c)
    for i in range(pops):
        d = max(3, k - i * (k // pops)) if not lean else max(3, k // 2)
        out += sound(se) + blend("F_PAL_TARGET", 0, 0, d, c) + wait() + blend("F_PAL_TARGET", 0, d, 0, c) + wait()
    return out


def descend(c, power, se, name):
    """DESCEND: turn 1 sinks -- the user darkens toward the deep and is gone; turn 2 it surfaces under the target."""
    return ["\tchoosetwoturnanim %sSink, %sSurface" % (name, name), "%sDone:" % name, "\tend", "%sSink:" % name] + \
        sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_ATTACKER", 1, 0, 12, c) + wait() + ["\tinvisible ANIM_ATTACKER"] + \
        blend("F_PAL_ATTACKER", 0, 12, 0, c) + wait() + ["\tgoto %sDone" % name, "%sSurface:" % name, "\tvisible ANIM_ATTACKER"] + \
        ascend(c, power, se) + ["\tgoto %sDone" % name]


def flow_table():
    t = {}
    t["WATER_GUN"] = lambda c, p, se, n: pour(c, p, se, lean=True)
    t["HYDRO_PUMP"] = lambda c, p, se, n: pour(c, p, se, slow=2)
    t["HYDRO_CANNON"] = lambda c, p, se, n: pour(c, p, se, slow=2) + recoil() + recoil()
    t["SURF"] = lambda c, p, se, n: pour(c, p, se, sel="F_PAL_DEF_SIDE")
    t["MUDDY_WATER"] = lambda c, p, se, n: pour(c, p, se, sel="F_PAL_DEF_SIDE") + silt()
    t["WATER_SPOUT"] = lambda c, p, se, n: pour(c, p, se, sel="F_PAL_DEF_SIDE", slow=2)
    t["OCTAZOOKA"] = lambda c, p, se, n: pour(c, p, se) + silt()
    t["CRABHAMMER"] = lambda c, p, se, n: pour(c, p, se, abrupt=True)
    t["WATERFALL"] = lambda c, p, se, n: ascend(c, p, se)
    t["WATER_PULSE"] = lambda c, p, se, n: ripples(c, p, se)
    t["BUBBLE"] = lambda c, p, se, n: ripples(c, p, se, pops=3, lean=True)
    t["BUBBLE_BEAM"] = lambda c, p, se, n: ripples(c, p, se, pops=3)
    for mv in ["CLAMP", "WHIRLPOOL"]:
        t[mv] = lambda c, p, se, n: send(c) + hold(c, p, se)
    t["DIVE"] = lambda c, p, se, n: descend(c, p, se, "DaemonsDescend")
    return t


# ---- the ENTROPY vocabulary (T-149): "noise and heat; disorder that spreads" (2.8). ----
#  An ENTROPY write is NOISE. The target's colour jumps between uneven levels in a fixed pattern that reads as
#  random (never Random(): an animation must not touch a battle's rolls), it jitters sideways, and the disorder
#  SPREADS -- outward into the field, or across everything at once for FLASHOVER. What it leaves decays slowly.

NOISE = [1.0, 0.3, 0.8, 0.15, 0.6, 0.35, 0.9, 0.2, 0.5]


def noise(c, power, se, lean=False, sel="F_PAL_TARGET", spread=None, burn_in=False):
    k, amp, n = strength(power)
    out = [] if lean else send(c)
    out += sound(se) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (max(1, amp - 1), n + 3)]
    levels = [0] + [max(1, int(k * f)) for f in (NOISE[:5] if lean else NOISE)]
    for a, b in zip(levels, levels[1:]):
        out += blend(sel, 0, a, b, c) + wait()
    last = levels[-1]
    if spread:                                            # the disorder leaves the target and takes the field
        seq = [0, 6, 2, 5, 1, 4, 0]
        for a, b in zip(seq, seq[1:]):
            out += blend(spread, 0, a, b, c) + wait()
    return out + blend(sel, 3 if burn_in else 1, last, 0, c) + wait()


def flashover(c, power, se):
    """FLASHOVER: the noise, and then everything on the field ignites at once."""
    whole = "F_PAL_BG | F_PAL_BATTLERS"
    return noise(c, power, se) + sound(se, "SOUND_PAN_ATTACKER") + blend(whole, 0, 0, 12, c) + wait() + blend(whole, 2, 12, 0, c) + wait()


def entropy_table():
    t = {}
    t["EMBER"] = lambda c, p, se, n: noise(c, p, se, lean=True)
    t["FLAMETHROWER"] = lambda c, p, se, n: noise(c, p, se, spread="F_PAL_BG")
    t["FIRE_BLAST"] = lambda c, p, se, n: flashover(c, p, se)
    t["BLAST_BURN"] = lambda c, p, se, n: flashover(c, p, se) + recoil() + recoil()
    t["OVERHEAT"] = lambda c, p, se, n: noise(c, p, se, spread="F_PAL_BG") + recoil() + recoil()
    t["FIRE_PUNCH"] = lambda c, p, se, n: noise(c, p, se, lean=True, burn_in=True)
    t["SACRED_FIRE"] = lambda c, p, se, n: noise(c, p, se, burn_in=True)
    t["BLAZE_KICK"] = lambda c, p, se, n: noise(c, p, se)
    t["FIRE_SPIN"] = lambda c, p, se, n: send(c) + hold(c, p, se)
    t["FLAME_WHEEL"] = lambda c, p, se, n: spin(c) + noise(c, p, se, lean=True)
    t["HEAT_WAVE"] = lambda c, p, se, n: noise(c, p, se, sel="F_PAL_DEF_SIDE", spread="F_PAL_BG")
    t["ERUPTION"] = lambda c, p, se, n: noise(c, p, se, sel="F_PAL_DEF_SIDE", spread="F_PAL_BG | F_PAL_ATK_SIDE")
    return t


# ---- the STRATUM vocabulary (T-150): "the physical layer everything else runs on" -- substrate and ground (2.8). ----
#  A STRATUM write comes FROM BELOW. The layer under both daemons -- the field -- takes STRATUM's brown first, the
#  terrain shakes (vanilla's own AnimTask_HorizontalShake, which restores itself), and only then does the target take
#  the colour, jolted vertically. UPHEAVAL moves everything; SEGFAULT opens the layer to black and the target with
#  it; EXCAVATE goes under on turn 1 (the script's own invisible) and comes up on turn 2.

def ground(c, power, se, lean=False, sel="F_PAL_TARGET", quake=False, fault=False):
    k, amp, n = strength(power)
    out = [] if lean else send(c)
    out += blend("F_PAL_BG", 0, 0, 8 if not lean else 5, c) + wait() + sound(se)
    #  The shake settles for about (intensity + 2) * 8 frames after its main phase (AnimTask_ShakeTerrain), so it is
    #  kept small: at 4 + 2*amp for 30, UPHEAVAL outlasted a 160-frame capture still brown.
    out += ["\tcreatevisualtask AnimTask_HorizontalShake, 5, (MAX_BATTLERS_COUNT + 1), %d, %d" % (3 + amp if quake else 1 + amp // 2, 20 if quake else 8)]
    if quake:
        out += ["\tcreatevisualtask AnimTask_HorizontalShake, 5, MAX_BATTLERS_COUNT, %d, 20" % (3 + amp)]
    else:
        out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 0, %d, %d, %d" % (amp + (2 if fault else 0), n, 1)]
    out += blend(sel, 0, 0, k, c) + wait() + ["\tdelay 6" if quake else "\tdelay 2"]
    return out + blend(sel, 1, k, 0, c) + blend("F_PAL_BG", 1, 8 if not lean else 5, 0, c) + wait()


def segfault(c, se):
    """SEGFAULT: the layer opens -- the field to black -- and the target falls into it, drained to black, then back."""
    #  The layer and the target go dark TOGETHER: waiting on the shake first (it settles for ~190 frames at intensity 12)
    #  meant the target's drain never reached the capture.
    return send(c, 10) + sound(se) + ["\tcreatevisualtask AnimTask_HorizontalShake, 5, (MAX_BATTLERS_COUNT + 1), 5, 16"] + \
        blend("F_PAL_BG", 1, 0, 14, "RGB_BLACK") + blend("F_PAL_TARGET", 1, 0, 16, "RGB_BLACK") + wait() + ["\tdelay 12"] + \
        blend("F_PAL_TARGET", 2, 16, 0, "RGB_BLACK") + blend("F_PAL_BG", 2, 14, 0, "RGB_BLACK") + wait()


def excavate(c, power, se, name):
    """EXCAVATE: turn 1 the user sinks into the layer -- browned and gone; turn 2 it comes up under the target."""
    return ["\tchoosetwoturnanim %sUnder, %sUp" % (name, name), "%sDone:" % name, "\tend", "%sUnder:" % name] + \
        sound(se, "SOUND_PAN_ATTACKER") + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_ATTACKER, 0, 2, 6, 1"] + blend("F_PAL_ATTACKER", 1, 0, 12, c) + wait() + \
        ["\tinvisible ANIM_ATTACKER"] + blend("F_PAL_ATTACKER", 0, 12, 0, c) + wait() + ["\tgoto %sDone" % name, "%sUp:" % name, "\tvisible ANIM_ATTACKER"] + \
        ground(c, power, se, lean=True, fault=True) + ["\tgoto %sDone" % name]


def stratum_table():
    t = {}
    t["EARTHQUAKE"] = lambda c, p, se, n: ground(c, p, se, sel="F_PAL_BATTLERS", quake=True)
    t["MAGNITUDE"] = lambda c, p, se, n: ground(c, 70, se, sel="F_PAL_BATTLERS", quake=True)
    t["FISSURE"] = lambda c, p, se, n: segfault(c, se)
    t["DIG"] = lambda c, p, se, n: excavate(c, p, se, "DaemonsExcavate")
    t["BONE_CLUB"] = lambda c, p, se, n: ground(c, p, se, fault=True)
    t["BONEMERANG"] = lambda c, p, se, n: ground(c, p, se, lean=True, fault=True)
    t["BONE_RUSH"] = lambda c, p, se, n: ground(c, p, se, lean=True, fault=True)
    t["MUD_SLAP"] = lambda c, p, se, n: ground(c, p, se, lean=True) + silt()
    t["MUD_SHOT"] = lambda c, p, se, n: ground(c, p, se) + silt()
    t["SAND_TOMB"] = lambda c, p, se, n: blend("F_PAL_BG", 0, 0, 6, c) + wait() + hold(c, p, se) + blend("F_PAL_BG", 1, 6, 0, c) + wait()
    return t


# ---- the SIGNAL vocabulary (T-151): "raw current, before anything interprets it" -- the raw edge (2.8). ----
#  ENTROPY is uneven noise; SIGNAL is EXACT. Square pulses, full on and full off with no ramp and no decay, on a
#  regular beat -- a carrier, not a flame. What varies between routines is the train: how many edges, how tall, and
#  whether the current jumps (ARC), spikes across the field (TRANSIENT), overshoots and cuts out (OVERVOLT), or dies
#  (SHORT OUT).

def edges(c, power, se, count=3, sel="F_PAL_TARGET", gap=4, climb=False, shake=True):
    k, amp, n = strength(power)
    out = sound(se)
    if shake:
        out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (amp, n)]
    for i in range(count):
        level = k if not climb else max(4, (k * (i + 1)) // count)
        out += blend(sel, 0, 0, level, c) + wait() + blend(sel, 0, level, 0, c) + wait() + ["\tdelay %d" % gap]
    return out


def arc(c, power, se):
    """ARC: the current jumps -- user edge, target edge, user edge, target edge, on the same beat."""
    out = sound(se)
    for _ in range(3):
        out += edges(c, power, se, count=1, sel="F_PAL_ATTACKER", gap=2, shake=False)
        out += edges(c, power, se, count=1, gap=2, shake=False)
    return out


def transient(c, power, se):
    """TRANSIENT: one spike, the whole field with it, and nothing after it."""
    k, amp, n = strength(power)
    whole = "F_PAL_BG | F_PAL_BATTLERS"
    return sound(se, "SOUND_PAN_ATTACKER") + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (amp, n)] + \
        blend(whole, 0, 0, 14, c) + wait() + blend(whole, 0, 14, 0, c) + wait() + ["\tdelay 6"] + \
        blend("F_PAL_TARGET", 0, 0, k, c) + wait() + blend("F_PAL_TARGET", 0, k, 0, c) + wait()


def overvolt(c, power, se):
    """OVERVOLT: the train climbs past full, then the current cuts out and the target is left flickering."""
    out = edges(c, power, se, count=3, climb=True) + blend("F_PAL_TARGET", 0, 0, 16, c) + wait() + blend("F_PAL_TARGET", 0, 16, 0, c) + wait()
    for _ in range(3):
        out += blend("F_PAL_TARGET", 0, 0, 6, GREY) + wait() + blend("F_PAL_TARGET", 0, 6, 0, GREY) + wait()
    return out


def short_out(c, power, se):
    """SHORT OUT: two edges and then nothing -- the target sits dead grey a moment."""
    return edges(c, power, se, count=2) + blend("F_PAL_TARGET", 0, 0, 10, GREY) + wait() + ["\tdelay 10"] + \
        blend("F_PAL_TARGET", 1, 10, 0, GREY) + wait()


def signal_table():
    t = {}
    t["THUNDER_SHOCK"] = lambda c, p, se, n: edges(c, p, se, count=2)
    t["THUNDERBOLT"] = lambda c, p, se, n: edges(c, p, se, count=4, climb=True)
    t["SHOCK_WAVE"] = lambda c, p, se, n: edges(c, p, se, count=6, gap=2)
    t["THUNDER"] = lambda c, p, se, n: transient(c, p, se)
    t["ZAP_CANNON"] = lambda c, p, se, n: overvolt(c, p, se)
    t["THUNDER_PUNCH"] = lambda c, p, se, n: short_out(c, p, se)
    t["SPARK"] = lambda c, p, se, n: arc(c, p, se)
    t["VOLT_TACKLE"] = lambda c, p, se, n: edges(c, p, se, count=4) + recoil()
    return t


# ---- the CORRUPT vocabulary (T-152): "data that has been tampered with" (2.8). ----
#  A CORRUPT write goes in clean and comes back WRONG. The target fills smoothly -- and then the return does not
#  unwind: it steps through out-of-order values, as a record read back from a tampered store does, and a residue
#  fades last. (ENTROPY is disordered going IN; CORRUPT is disordered coming OUT. SIGNAL is disordered never.)

def taint(c, power, se, lean=False, sel="F_PAL_TARGET", spread=False):
    k, amp, n = strength(power)
    out = [] if lean else send(c)
    if spread:
        out += blend("F_PAL_BG", 1, 0, 6, c) + wait()
    out += sound(se) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (amp, n)]
    out += blend(sel, 1, 0, k, c) + wait()                     # the write goes in, clean
    back = [k, k // 4, (k * 3) // 4, k // 8, k // 2, k // 6, 0]  # and comes back through the wrong values
    for a, b in zip(back, back[1:]):
        out += blend(sel, 0, a, b, c) + wait()
    out += blend(sel, 3, 0, 3, c) + wait() + blend(sel, 3, 3, 0, c) + wait()   # the residue, fading last
    if spread:
        out += blend("F_PAL_BG", 2, 6, 0, c) + wait()
    return out


def corrupt_table():
    t = {}
    t["POISON_STING"] = lambda c, p, se, n: taint(c, p, se, lean=True)
    t["POISON_FANG"] = lambda c, p, se, n: taint(c, p, se)
    t["POISON_TAIL"] = lambda c, p, se, n: taint(c, p, se)
    t["ACID"] = lambda c, p, se, n: taint(c, p, se, sel="F_PAL_DEF_SIDE") + silt()
    t["SMOG"] = lambda c, p, se, n: taint(c, p, se, spread=True)
    t["SLUDGE"] = lambda c, p, se, n: taint(c, p, se)
    t["SLUDGE_BOMB"] = lambda c, p, se, n: taint(c, p, se, spread=True)
    return t


# ---- the CONTEXT vocabulary (T-153): "the frame you read a thing in -- what makes the same thing mean
#  differently" (2.8). A CONTEXT write changes the FRAME first: the field takes CONTEXT's magenta and HOLDS it, the
#  target's colour shifts while the frame is up, and it comes back as the frame lifts. Nothing is thrown; the
#  reading changes. (PERSPECTIVE, the frame move that is not an attack, already drains to grey before the swap.)

def reframe(c, power, se, lean=False, sel="F_PAL_TARGET", body=None, after=None):
    k, amp, n = strength(power)
    out = [] if lean else send(c)
    out += blend("F_PAL_BG", 1, 0, 9, c) + wait() + sound(se)                  # the frame goes up, and stays up
    out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 2" % (max(1, amp - 1), n)]
    out += (body if body is not None else blend(sel, 1, 0, k, c) + wait() + ["\tdelay 8"] + blend(sel, 1, k, 0, c) + wait())
    out += blend("F_PAL_BG", 1, 9, 0, c) + wait()                              # and the frame lifts
    return out + (after or [])


def misread(c, power, se):
    """MISREAD: under the frame the target reads two ways at once -- its colour and the ground, alternating."""
    k, _, _ = strength(power)
    body = []
    for _ in range(3):
        body += blend("F_PAL_TARGET", 0, 0, k, c) + wait() + blend("F_PAL_TARGET", 0, k, 0, c) + wait()
        body += blend("F_PAL_TARGET", 0, 0, k // 2, GREY) + wait() + blend("F_PAL_TARGET", 0, k // 2, 0, GREY) + wait()
    return reframe(c, power, se, body=body)


def variance(c, power, se):
    """VARIANCE: the same routine reads differently every time -- three shifts, none the same size."""
    body = []
    for lvl in (5, 13, 8):
        body += blend("F_PAL_TARGET", 1, 0, lvl, c) + wait() + blend("F_PAL_TARGET", 1, lvl, 0, c) + wait()
    return reframe(c, power, se, body=body)


def amplify(c, power, se):
    """AMPLIFY: what came in goes back doubled -- the user takes the frame's colour first, the target twice as deep."""
    k, _, _ = strength(power)
    body = blend("F_PAL_ATTACKER", 1, 0, k // 2, c) + wait() + blend("F_PAL_ATTACKER", 1, k // 2, 0, c) + wait()
    body += blend("F_PAL_TARGET", 0, 0, min(16, k * 2), c) + wait() + ["\tdelay 8"] + blend("F_PAL_TARGET", 1, min(16, k * 2), 0, c) + wait()
    return reframe(c, power, se, body=body)


def schedule(c, power, se):
    """SCHEDULE: the frame is set now and nothing lands -- the reading is due later."""
    body = blend("F_PAL_TARGET", 1, 0, 5, c) + wait() + ["\tdelay 16"] + blend("F_PAL_TARGET", 2, 5, 0, c) + wait()
    return reframe(c, power, se, body=body)


def context_table():
    t = {}
    for mv in ["PSYCHIC", "EXTRASENSORY", "LUSTER_PURGE", "MIST_BALL"]:
        t[mv] = lambda c, p, se, n: reframe(c, p, se)
    t["PSYBEAM"] = lambda c, p, se, n: reframe(c, p, se, lean=True)
    t["CONFUSION"] = lambda c, p, se, n: misread(c, p, se)
    t["PSYWAVE"] = lambda c, p, se, n: variance(c, 60, se)
    t["MIRROR_COAT"] = lambda c, p, se, n: amplify(c, p if p else 60, se)
    t["FUTURE_SIGHT"] = lambda c, p, se, n: schedule(c, p, se)
    t["DREAM_EATER"] = lambda c, p, se, n: reframe(c, p, se, body=feed(c, p, se)[len(send(c)):])
    t["PSYCHO_BOOST"] = lambda c, p, se, n: reframe(c, p, se, after=recoil())
    return t


# ---- the SWARM vocabulary (T-154): "many small agents; no single one matters" (2.8). ----
#  A SWARM write is a QUORUM: many small EQUAL marks land one after another and accumulate on the target, hold a
#  moment once they are all in, and release together. No mark is the blow; the count is. (LOGIC's steps are ordered
#  and each licensed by the last; SWARM's are interchangeable, which is the difference between a proof and a vote.)

def quorum(c, power, se, marks=None, sel="F_PAL_TARGET", growing=False, after=None):
    k, amp, n = strength(power)
    if marks is None:
        marks = max(3, min(6, 2 + power // 25))
    out = send(c)
    level = 0
    for i in range(marks):
        step = max(2, k // marks) if not growing else max(2, ((i + 1) * 2 * k) // (marks * (marks + 1) // 2) // 1)
        out += sound(se) + ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, 1, 0, 2, 1"]
        out += blend(sel, 0, level, min(16, level + step), c) + wait()
        level = min(16, level + step)
    out += ["\tdelay 8"] + blend(sel, 0, level, 0, c) + wait()     # the decision, all at once
    return out + (after or [])


def swarm_table():
    t = {}
    t["PIN_MISSILE"] = lambda c, p, se, n: quorum(c, p, se, marks=2)     # FANOUT, and CONSENSUS plays this script too
    t["TWINEEDLE"] = lambda c, p, se, n: quorum(c, p, se, marks=2)
    t["MEGAHORN"] = lambda c, p, se, n: quorum(c, p, se, marks=6)
    t["LEECH_LIFE"] = lambda c, p, se, n: quorum(c, p, se, marks=3, after=feed(c, p, se)[len(send(c)):])
    t["SIGNAL_BEAM"] = lambda c, p, se, n: quorum(c, p, se, after=blend("F_PAL_TARGET", 0, 0, 7, GREY) + wait() + blend("F_PAL_TARGET", 0, 7, 0, GREY) + wait())
    t["SILVER_WIND"] = lambda c, p, se, n: quorum(c, p, se, after=rise(c, 1, se))
    t["FURY_CUTTER"] = lambda c, p, se, n: quorum(c, p, se, marks=4, growing=True)
    t["CONSENSUS"] = None            # §2.5's added routine plays FANOUT's script; redrawing that redraws this
    return t


# ---- the FROZEN vocabulary (T-155): "locked to what it already saw, unable to move" (2.8). ----
#  The one family with NO MOTION. Every other write shakes its target; a FROZEN write snaps it to the pale blue and
#  holds it dead still -- a long flat hold, no shake, the frame that will not update -- and releases late and all at
#  once. What varies is how much is locked (one daemon, a side, the field) and for how long.

def lock(c, power, se, lean=False, sel="F_PAL_TARGET", field=False, hold_frames=None, slow_release=False, depth=None):
    k, _, _ = strength(power)
    k = depth or k
    out = [] if lean else send(c)
    out += sound(se)
    if field:
        out += blend("F_PAL_BG", 0, 0, 7, c)
    out += blend(sel, 0, 0, k, c) + wait()
    out += ["\tdelay %d" % (hold_frames if hold_frames is not None else (14 if lean else 24))]
    out += blend(sel, 2 if slow_release else 0, k, 0, c)
    if field:
        out += blend("F_PAL_BG", 0, 7, 0, c)
    return out + wait()


def frozen_table():
    t = {}
    t["POWDER_SNOW"] = lambda c, p, se, n: lock(c, p, se, lean=True)
    t["ICE_PUNCH"] = lambda c, p, se, n: lock(c, p, se, lean=True)
    t["ICE_BEAM"] = lambda c, p, se, n: lock(c, p, se)
    t["BLIZZARD"] = lambda c, p, se, n: lock(c, p, se, sel="F_PAL_DEF_SIDE", field=True)
    t["ICY_WIND"] = lambda c, p, se, n: lock(c, p, se, sel="F_PAL_DEF_SIDE", slow_release=True)
    t["AURORA_BEAM"] = lambda c, p, se, n: lock(c, p, se) + blend("F_PAL_TARGET", 0, 0, 6, GREY) + wait() + blend("F_PAL_TARGET", 1, 6, 0, GREY) + wait()
    t["SHEER_COLD"] = lambda c, p, se, n: lock(c, p, se, field=True, hold_frames=40, depth=16)
    t["ICE_BALL"] = lambda c, p, se, n: lock(c, p, se, lean=True)
    t["ICICLE_SPEAR"] = lambda c, p, se, n: lock(c, p, se, lean=True, hold_frames=6)
    return t


# ---- the PROTECT vocabulary (T-156): refusing, deferring, or taking the hit for another. ----
#  These act on the USER'S OWN boundary. A seal: the user snaps to its routine's colour and HOLDS it -- nothing
#  gets in while it is up -- then lets it go. SURVIVE holds at almost-grey (it will stay at 1 HP); SUBSTITUTE greys
#  what it leaves and then runs vanilla's own AnimTask_MonToSubstitute, which is the mechanic (the stand-in sprite
#  is vanilla's doll, one of T-137's graphics); MAGIC COAT seals and bounces; INTERCEPT takes; REDIRECT draws the
#  eye by dimming everything else.

def seal(c, se, hold_frames=16, tick=False):
    out = sound(se, "SOUND_PAN_ATTACKER") + (tick_se() if tick else [])
    return out + blend("F_PAL_ATTACKER", 0, 0, 11, c) + wait() + ["\tdelay %d" % hold_frames] + blend("F_PAL_ATTACKER", 1, 11, 0, c) + wait()


def survive(c, se):
    return sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_ATTACKER", 1, 0, 13, GREY) + wait() + ["\tdelay 18"] + \
        tick_se() + blend("F_PAL_ATTACKER", 1, 13, 0, GREY) + wait()


def substitute(c, se):
    return sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_ATTACKER", 1, 0, 12, GREY) + wait() + \
        blend("F_PAL_ATTACKER", 0, 12, 0, GREY) + wait() + ["\tcreatevisualtask AnimTask_MonToSubstitute, 2"] + wait()


def magic_coat(c, se):
    return seal(c, se, hold_frames=8) + blend("F_PAL_TARGET", 0, 0, 10, c) + wait() + blend("F_PAL_TARGET", 0, 10, 0, c) + wait()


def intercept(c, se):
    return sound(se) + blend("F_PAL_TARGET", 0, 0, 8, GREY) + wait() + blend("F_PAL_TARGET", 0, 8, 0, GREY) + \
        blend("F_PAL_ATTACKER", 0, 0, 10, c) + wait() + blend("F_PAL_ATTACKER", 1, 10, 0, c) + wait()


def redirect(c, se):
    out = sound(se, "SOUND_PAN_ATTACKER") + blend("F_PAL_BG | F_PAL_DEF_SIDE", 1, 0, 8, GREY) + wait()
    for _ in range(2):
        out += blend("F_PAL_ATTACKER", 0, 0, 10, c) + wait() + blend("F_PAL_ATTACKER", 0, 10, 0, c) + wait()
    return out + blend("F_PAL_BG | F_PAL_DEF_SIDE", 1, 8, 0, GREY) + wait()


def delegate(c, se):
    both = "F_PAL_ATK_SIDE"
    return sound(se, "SOUND_PAN_ATTACKER") + blend(both, 0, 0, 9, c) + wait() + blend(both, 1, 9, 0, c) + wait()


def protect_table():
    t = {}
    t["PROTECT"] = lambda c, p, se, n: seal(c, se)
    t["DETECT"] = lambda c, p, se, n: seal(c, se, tick=True)
    t["ENDURE"] = lambda c, p, se, n: survive(c, se)
    t["SUBSTITUTE"] = lambda c, p, se, n: substitute(c, se)
    t["MAGIC_COAT"] = lambda c, p, se, n: magic_coat(c, se)
    t["SNATCH"] = lambda c, p, se, n: intercept(c, se)
    t["FOLLOW_ME"] = lambda c, p, se, n: redirect(c, se)
    t["HELPING_HAND"] = lambda c, p, se, n: delegate(c, se)
    return t


# ---- the OPAQUE vocabulary (T-157): "a box you cannot see inside" (2.8). ----
#  An OPAQUE write OCCLUDES. The target blacks out to OPAQUE's near-black -- its inside is no longer visible -- the
#  hit happens there, a shake in the dark nobody can read, and then it is revealed. The event is never shown; only
#  before and after are. (FROZEN holds still in the light; OPAQUE moves where you cannot see it.)

def occlude(c, power, se, lean=False, after=None, hidden_user=False, times=1):
    k, amp, n = strength(power)
    dark = max(12, min(15, k + 4))
    out = []
    if hidden_user:                                         # BLINDSIDE: the user is not seen coming either
        out += blend("F_PAL_ATTACKER", 0, 0, 14, c) + wait()
    elif not lean:
        out += send(c)
    for _ in range(times):
        out += blend("F_PAL_TARGET", 0, 0, dark, c) + wait() + sound(se)
        out += ["\tcreatevisualtask AnimTask_ShakeMon, 2, ANIM_TARGET, %d, 0, %d, 1" % (amp, n)] + wait() + ["\tdelay 4"]
        out += blend("F_PAL_TARGET", 0 if times > 1 else 1, dark, 0, c) + wait()
    if hidden_user:
        out += blend("F_PAL_ATTACKER", 1, 14, 0, c) + wait()
    return out + (after or [])


def opaque_table():
    t = {}
    t["BITE"] = lambda c, p, se, n: occlude(c, p, se)
    t["PURSUIT"] = lambda c, p, se, n: occlude(c, p, se, lean=True)
    t["FAINT_ATTACK"] = lambda c, p, se, n: occlude(c, p, se, hidden_user=True)
    t["CRUNCH"] = lambda c, p, se, n: occlude(c, p, se, after=blend("F_PAL_TARGET", 0, 0, 7, GREY) + wait() + ["\tdelay 6"] + blend("F_PAL_TARGET", 1, 7, 0, GREY) + wait())
    t["THIEF"] = lambda c, p, se, n: occlude(c, p, se, after=take(c))
    t["KNOCK_OFF"] = lambda c, p, se, n: occlude(c, p, se, after=blend("F_PAL_TARGET", 0, 0, 8, GREY) + wait() + blend("F_PAL_TARGET", 0, 8, 0, GREY) + wait())
    t["BEAT_UP"] = lambda c, p, se, n: occlude(c, 40, se, lean=True, times=3)
    return t

FAMILIES = {"CONTENT": content_table, "LOWER": lower_table, "AFFLICT": afflict_table, "RAISE": raise_table, "FIELD": field_table, "LOGIC": logic_table, "VECTOR": vector_table, "GROWTH": growth_table, "FLOW": flow_table, "ENTROPY": entropy_table, "STRATUM": stratum_table, "SIGNAL": signal_table, "CORRUPT": corrupt_table, "CONTEXT": context_table, "SWARM": swarm_table, "FROZEN": frozen_table, "PROTECT": protect_table, "OPAQUE": opaque_table}


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
    table = FAMILIES[fam]()
    pw = powers()
    #  Each routine is drawn in ITS OWN type's colour (9.24.3): CONTENT's attacks are all bone, and a status family
    #  mixes types -- THUNDER WAVE is SIGNAL, POISON POWDER is CORRUPT.
    moves_h = open(os.path.join(E, "src/data/battle_moves.h")).read()
    mtype = {mv: re.search(r"\.type = TYPE_(\w+)", body).group(1) for mv, body in re.findall(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \}", moves_h, re.S)}
    colour_of = lambda mv: GREY if mtype[mv] == "MYSTERY" else type_rgb555(mtype[mv])
    colour = "per routine"
    #  The table must be the whole family and nothing else, as animcensus.py files it. A routine left out stays
    #  vanilla silently; one added redraws a stranger.
    family = set(census_family(fam))
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
        if table[mv] is None:
            #  A routine with no script of its OWN: the animation table points it at another's (CONSENSUS plays
            #  FANOUT's PIN MISSILE). Redrawing that one redraws this one; there is nothing here to write.
            continue
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
            body = table[mv](colour_of(mv), pw.get(mv, 0), se, mv)
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

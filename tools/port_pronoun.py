#!/usr/bin/env python3
"""THE FOE IS A THING. THEM IS A SOMEONE. (T-183; vision.md 4.2, 1.6)

    python3 tools/port_pronoun.py            # report every changed description, measured
    python3 tools/port_pronoun.py --write     # write src/move_descriptions.c

Everywhere else "the foe" is a neutral word for the other side. Here it is the one the game spends forty
hours arguing against: a foe is a thing you are hitting, and this game's whole claim is that the thing in
front of you has an inside. The Index already says "them" (T-194's neighbours and the fourteen of T-181);
the routines still said "the foe" 153 times, which is the argument disagreeing with itself in the one place
a player reads most.

THE CATCH IS THE PRIZE. 37 of them are vanilla's PASSIVE -- "The foe is hit with an intense flame" -- and a
blind swap writes "Them is hit with". Each of those is turned ACTIVE by hand below, which is why this is a
table and not a regular expression, and why it reads better afterwards: an active sentence is shorter, and
these have 113 pixels and four lines to live in (T-181).

The rest is mechanical and safe: the possessive becomes THEIR, and the object becomes THEM.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(ROOT, "engineGba/src/move_descriptions.c")
PANE, MAXLINES = 113, 4
WRITE = "--write" in sys.argv

_src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
_ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
exec(compile(_src.split("# ------------------------------------------------------- names, derived")[0],
             "port_vocab.py", "exec"), _ns)
textwidth = _ns["textwidth"]

#  The 37 passives, turned active. Each says the same thing the vanilla line said; what changes is who is
#  doing it and what the other one is called.
ACTIVE = {
    "CometPunch":   "Hits them with a flurry of punches, two to five times.",
    "ThunderPunch": "Punches them with an electrified fist. It may leave them throttled.",
    "Guillotine":   "A vicious tearing attack with pincers. They HALT if it hits.",
    "Whirlwind":    "Forces them out and an ally in. In the wild, the battle ends.",
    "Stomp":        "Stomps them with a big foot. They may flinch.",
    "FuryAttack":   "Jabs them with a horn or beak, two to five times.",
    "Bite":         "Shuts the light out. They may flinch.",
    "Roar":         "Forces them out and an ally in. In the wild, the battle ends.",
    "Ember":        "Attacks them with small flames. They may overheat.",
    "Flamethrower": "Scorches them with intense flames. They may overheat.",
    "IceBeam":      "Stops the weights updating. They may end up HUNG.",
    "Peck":         "Jabs them with a sharply pointed beak or horn.",
    "StringShot":   "Their work piles up behind them. Lowers SPEED.",
    "Fissure":      "Drops them into a fissure. They HALT if it hits.",
    "ConfuseRay":   "A sinister ray that leaves them THRASHING.",
    "Lick":         "Licks them with a long tongue. It may also throttle.",
    "DizzyPunch":   "A rhythmic punch that may leave them THRASHING.",
    "FurySwipes":   "Rakes them with claws or scythes, two to five times.",
    "HyperFang":    "Attacks them with sharp fangs. They may flinch.",
    "MeanLook":     "Holds the connection open. They cannot leave.",
    "Present":      "Gives them a booby-trapped gift. It restores HP sometimes.",
    "DynamicPunch": "The user's full power in one punch. Leaves them THRASHING if it hits.",
    "DragonBreath": "An incredible blast of breath. It may also throttle them.",
    "Encore":       "Holds them to the routine they last ran, for two to six turns.",
    "Twister":      "Pulls everything in toward one point. They may flinch.",
    "Crunch":       "Crunches them with sharp fangs. It may lower their SP. DEF.",
    "Whirlpool":    "Traps them in a fast, vicious whirlpool for two to five turns.",
    "Torment":      "They cannot run the same routine twice in a row.",
    "Taunt":        "They can only attack for two turns. Nothing else.",
    "CrushClaw":    "Attacks them with sharp claws. It may lower their DEFENSE.",
    "BlastBurn":    "Hits them with a huge explosion. The user can't move next turn.",
    "HydroCannon":  "Hits them with a watery cannon. The user can't move next turn.",
    "AirCutter":    "Hits them with razor-like wind. High critical-hit ratio.",
    "Tickle":       "Makes them laugh, lowering their ATTACK and DEFENSE.",
    "SignalBeam":   "A flashing beam that may leave them THRASHING.",
    "FrenzyPlant":  "Hits them with an enormous branch. The user can't move next turn.",
    "LeafBlade":    "Slashes them with a sharp leaf. High critical-hit ratio.",

    #  And nineteen the mechanical rules broke, which is the whole argument for reading the output. A rule
    #  that turns "the foe" into "them" writes "takes what them was holding", and one that leaves "it" alone
    #  writes "holds it there" about a someone it has just called them. Singular they needs the verb to agree
    #  and the other pronouns in the sentence to follow it; neither is something a substitution can know.
    "Wrap":         "Closes around them and holds them there for two to five turns.",
    "Growl":        "Runs them below their rated capacity. Lowers ATTACK.",
    "AuroraBeam":   "Narrows what they are allowed to do. Lowers ATTACK.",
    "PoisonPowder": "Mixes something bad into what they are running. It may leave them LEAKING.",
    "Smokescreen":  "Blurs what they are aiming at. Reduces accuracy.",
    "MirrorMove":   "Sends their own heading back at them.",
    "Kinesis":      "Puts something else in front of them. It may lower their accuracy.",
    "Glare":        "Intimidates them with the design on its belly. It may throttle.",
    "CottonSpore":  "Fills their path with what they cannot clear. Sharply lowers SPEED.",
    "ScaryFace":    "Lowers their priority, so they are scheduled later.",
    "FaintAttack":  "Arrives from where they were not looking. It does not miss.",
    "MudSlap":      "Covers what they read from. Damages them, and lowers their accuracy.",
    "Octazooka":    "More at once than they can take in. Lowers accuracy.",
    "Swagger":      "Leaves them THRASHING, but sharply raises their ATTACK.",
    "Trick":        "Swaps what the two are holding, before they can refuse.",
    "SandTomb":     "Covers them over and holds them there for two to five turns.",
    "Covet":        "Asks nicely, and takes what they were holding.",
    "Psychic":      "Reads them in its own way. It may lower their SP. DEF.",
    "MuddyWater":   "The user attacks with muddy water. It may lower their accuracy.",

    #  And seven more found by reading the output a second time. Every one is an "it" that meant the foe and
    #  now sits beside a "them" -- which the first scan missed because "them last ran" has no verb in it that
    #  a pattern would think to look for. The ones left alone are the "it"s that mean the MOVE or the USER,
    #  and those are correct: "Nothing about them changes what it costs" is the move's cost.
    "TailWhip":     "Leaves them open where they were not. Lowers DEFENSE.",
    "Disable":      "For a few turns, it stops them using the routine they last ran.",
    "Screech":      "Strips them of what was guarding them. Sharply cuts DEFENSE.",
    "Constrict":    "Holds them tight enough to slow them. It may lower SPEED.",
    "SuperFang":    "Cuts them down to half of what they had.",
    "Sketch":       "Copies the routine they last ran, and is spent doing it.",
    "SpiderWeb":    "Ensnares them in sticky string, so they cannot DETACH or switch out.",

    #  And six that say "foe" with no article at all -- "all foe", "a SUSPENDED foe", "Prevents foe from" --
    #  which is vanilla's own clipped plural and matches none of the rules. They are the last of it.
    "Swift":        "Star-shaped rays that never miss are fired at all of them.",
    "DreamEater":   "Reads them while SUSPENDED, and keeps half of what it takes.",
    "Nightmare":    "Suspended, they get nothing at all. They lose HP each turn.",
    "SmellingSalt": "Doubly effective if they are throttled, but it cures the throttling.",
    "FollowMe":     "The user draws attention to itself, so they attack only the user.",
    "Imprison":     "Stops them using any routine the user also knows.",
}

RULES = [
    (re.compile(r"\bThe foe's\b"), "Their"),
    (re.compile(r"\bthe foe's\b"), "their"),
    (re.compile(r"\bthe foe\b"),   "them"),
    (re.compile(r"\bThe foe\b"),   "They"),   # anything the table missed, so nothing is left saying it
    (re.compile(r"\ba foe\b"),     "them"),
    #  the bare noun, last, so nothing can survive this pass still calling a daemon a foe
    (re.compile(r"\bfoe's\b"),    "their"),
    (re.compile(r"\bfoes?\b"),     "them"),
]


def wrap(s):
    out, cur = [], ""
    for w in s.split():
        trial = (cur + " " + w).strip()
        if cur and textwidth(trial) > PANE:
            out.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out


def main():
    src = open(C, encoding="utf-8").read()
    changed = over = 0
    for m in list(re.finditer(r'const u8 gMoveDescription_(\w+)\[\] = _\((.*?)\);', src, re.S)):
        name = m.group(1)
        body = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2))).replace("\\n", " ")
        new = ACTIVE.get(name, body)
        if name not in ACTIVE:
            for pat, rep in RULES:
                new = pat.sub(rep, new)
        if new == body:
            continue
        lines = wrap(new)
        widest = max(textwidth(l) for l in lines)
        bad = widest > PANE or len(lines) > MAXLINES
        over += bad
        changed += 1
        print("  %-16s %3dpx %d%s  %s" % (name, widest, len(lines), " !!" if bad else "  ", " / ".join(lines)))
        pat = re.compile(r'(const u8 gMoveDescription_%s\[\] = _\()(.*?)(\);)' % name, re.S)
        src = pat.sub(lambda mm: mm.group(1) + '"' + "\\n".join(lines) + '"' + mm.group(3), src, count=1)
    print("\n  %d descriptions rewritten, %d over the %dpx pane" % (changed, over, PANE))
    if WRITE:
        open(C, "w", encoding="utf-8").write(src)
        print("  written src/move_descriptions.c")


if __name__ == "__main__":
    main()

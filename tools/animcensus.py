#!/usr/bin/env python3
"""Every move's battle animation, and whether it is still vanilla's (T-134).

    python3 tools/animcensus.py                 # one line per family: how many moves, how many still vanilla
    python3 tools/animcensus.py --family HEAL   # every move in a family, earliest-seen first
    python3 tools/animcensus.py --gfx           # the effect graphics, by how many vanilla animations still use them
    python3 tools/animcensus.py --descriptions  # renamed routines whose description is still vanilla's (T-138)
    python3 tools/animcensus.py --descriptions --kept  # ...and the ones kept on purpose, each with its reason
    python3 tools/animcensus.py --general       # the animations that are not moves: states, weather, items, balls (T-168)

THE QUESTION IT ANSWERS is T-134's: 309 of 355 move names are ours and the animations are all vanilla's, so a
player watches RESTORE draw a creature gathering energy. A move is VANILLA here while its `Move_` script in
data/battle_anim_scripts.s is byte-identical to upstream's -- which means the tickets close themselves: a family
is done when this reports 0 still vanilla for it, and the checklist stops naming what is finished.

FAMILIES. An attack (power > 0) is filed by its TYPE, under our type names, because a type's attacks share a
visual language and should be redrawn together. A routine with no power is filed by what it DOES (its effect):
healing, raising, lowering, afflicting, shaping the field, copying, protecting -- and OTHER for the rest. The
family table is below and every effect the engine has lands in exactly one of them.

EARLIEST SEEN is the lowest level at which any daemon THIS GAME RENAMED learns it by level-up (0 for a TM, HM
or tutor, which a player can teach at once). It is a proxy for "the order a player meets it", good enough to
order the work; trainers' custom moves are counted separately. Species still carrying vanilla names are not
in the game's reachable set and do not count.

Traps respected: nothing here imports a gba* tool (docs/engine.md trap 16); everything is read as text.
"""
import os, re, subprocess, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")

TYPE_NAME = {"NORMAL": "CONTENT", "FIGHTING": "LOGIC", "FLYING": "VECTOR", "POISON": "CORRUPT", "GROUND": "STRATUM",
             "ROCK": "LEGACY", "BUG": "SWARM", "GHOST": "LATENT", "STEEL": "HARDENED", "MYSTERY": "MYSTERY",
             "FIRE": "ENTROPY", "WATER": "FLOW", "GRASS": "GROWTH", "ELECTRIC": "SIGNAL", "PSYCHIC": "CONTEXT",
             "ICE": "FROZEN", "DRAGON": "EMERGENT", "DARK": "OPAQUE"}

#  Routines with no power, by effect. Matched in order; the first pattern that fits wins.
STATUS_FAMILIES = [
    ("HEAL",     r"RESTORE_HP|SOFTBOILED|MORNING_SUN|SYNTHESIS|MOONLIGHT|^REST$|WISH|INGRAIN|HEAL_BELL|REFRESH|SWALLOW|STOCKPILE"),
    ("PROTECT",  r"PROTECT|ENDURE|SUBSTITUTE|DETECT|MAGIC_COAT|SNATCH|FOLLOW_ME|HELPING_HAND"),
    ("FIELD",    r"REFLECT|LIGHT_SCREEN|MIST|SAFEGUARD|RAIN_DANCE|SUNNY_DAY|SANDSTORM|HAIL|SPIKES|MUD_SPORT|WATER_SPORT|HAZE|PERISH_SONG|MEAN_LOOK|ROAR|TELEPORT|BATON_PASS|FUTURE_SIGHT|NIGHTMARE|CURSE|SPITE|GRUDGE|IMPRISON|TORMENT|TAUNT|DISABLE|ENCORE|LOCK_ON|FORESIGHT|CAMOUFLAGE|FOCUS_ENERGY|CHARGE|LEECH_SEED|DESTINY_BOND|SPLASH|MEMENTO|TICKLE"),
    ("COPY",     r"TRANSFORM|MIMIC|SKETCH|CONVERSION|ROLE_PLAY|SKILL_SWAP|MIRROR_MOVE|METRONOME|ASSIST|SLEEP_TALK|NATURE_POWER|RECYCLE|TRICK|PSYCH_UP|BELLY_DRUM|PAIN_SPLIT"),
    ("AFFLICT",  r"TEETER|SLEEP|TOXIC|POISON|PARALYZE|WILL_O_WISP|CONFUSE|ATTRACT|YAWN|SWAGGER|FLATTER"),
    ("RAISE",    r"_UP|MINIMIZE|DEFENSE_CURL|DRAGON_DANCE|CALM_MIND|BULK_UP|COSMIC_POWER"),
    ("LOWER",    r"_DOWN"),
]


def read(p):
    return open(os.path.join(E, p)).read()


def upstream(p):
    return subprocess.run(["git", "-C", E, "show", "upstream/master:" + p], capture_output=True, text=True).stdout


def blocks(src):
    """label -> its script text, up to the next label."""
    out = {}
    for b in re.split(r"\n(?=[A-Za-z_]\w*:\n)", src):
        m = re.match(r"([A-Za-z_]\w*):\n", b)
        if m:
            #  Comments are not animation: a note written above the NEXT label lands in this block's text, and it
            #  made DISABLE look redrawn when RESTORE's draft was annotated.
            out[m.group(1)] = "\n".join(l for l in b.split("\n") if not l.lstrip().startswith("@"))
    return out


def family(effect, power):
    if power > 0:
        return None
    e = effect[len("EFFECT_"):]
    for name, pat in STATUS_FAMILIES:
        if re.search(pat, e):
            return name
    return "OTHER"


def census():
    moves_h = read("src/data/battle_moves.h")
    info = {}
    for mv, body in re.findall(r"\[(MOVE_\w+)\]\s*=\s*\{(.*?)\n    \}", moves_h, re.S):
        eff = re.search(r"\.effect = (\w+)", body).group(1)
        pw = int(re.search(r"\.power = (\d+)", body).group(1))
        ty = re.search(r"\.type = TYPE_(\w+)", body).group(1)
        info[mv] = dict(effect=eff, power=pw, type=ty)
    names = dict(re.findall(r'\[(MOVE_\w+)\]\s*= _\("(.*?)"\)', read("src/data/text/move_names.h")))

    #  gBattleAnims_Moves is indexed by move id, in the order include/constants/moves.h numbers them.
    order = [m for m, _ in sorted(((m, int(v)) for m, v in re.findall(r"#define (MOVE_\w+)\s+(\d+)", read("include/constants/moves.h"))),
                                  key=lambda x: x[1]) if m in info]
    s_ours, s_up = read("data/battle_anim_scripts.s"), upstream("data/battle_anim_scripts.s")
    table = re.search(r"gBattleAnims_Moves::\n(.*?)\n\n", s_ours, re.S).group(1)
    labels = re.findall(r"\.4byte (\w+)", table)
    b_ours, b_up = blocks(s_ours), blocks(s_up)

    sp_ours = dict(re.findall(r'\[SPECIES_(\w+)\]\s*= _\("(.*?)"\)', read("src/data/text/species_names.h")))
    sp_up = dict(re.findall(r'\[SPECIES_(\w+)\]\s*= _\("(.*?)"\)', upstream("src/data/text/species_names.h")))
    ours = {s for s in sp_ours if sp_ours[s] != sp_up.get(s)}

    earliest = defaultdict(lambda: None)
    learners = defaultdict(set)
    ptr = dict((a, s) for s, a in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*(s\w+LevelUpLearnset)", read("src/data/pokemon/level_up_learnset_pointers.h")))
    for arr, body in re.findall(r"static const u16 (s\w+LevelUpLearnset)\[\] = \{(.*?)\};", read("src/data/pokemon/level_up_learnsets.h"), re.S):
        sp = ptr.get(arr)
        if sp not in ours:
            continue
        for lvl, mv in re.findall(r"LEVEL_UP_MOVE\(\s*(\d+), (MOVE_\w+)\)", body):
            learners[mv].add(sp_ours[sp])
            if earliest[mv] is None or int(lvl) < earliest[mv]:
                earliest[mv] = int(lvl)
    for sp, body in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*TMHM_LEARNSET\((.*?)\),\n", read("src/data/pokemon/tmhm_learnsets.h"), re.S):
        if sp in ours:
            for mv in re.findall(r"TMHM\((?:TM|HM)\d+_(\w+)\)", body):
                learners["MOVE_" + mv].add(sp_ours[sp]); earliest["MOVE_" + mv] = 0
    trainer_uses = defaultdict(int)
    for mv in re.findall(r"MOVE_\w+", read("src/data/trainer_parties.h")):
        trainer_uses[mv] += 1

    rows = []
    for i, mv in enumerate(order):
        if mv == "MOVE_NONE" or i >= len(labels):
            continue
        lab = labels[i]
        d = info[mv]
        fam = family(d["effect"], d["power"]) or TYPE_NAME.get(d["type"], d["type"])
        text = b_ours.get(lab, "")
        vanilla = text == b_up.get(lab)
        #  A redraw behind `.if DAEMONS_DEBUG` is a DRAFT: the debug ROMs play it for approval, release keeps vanilla's.
        draft = ".if DAEMONS_DEBUG" in text
        tags = sorted(set(re.findall(r"ANIM_TAG_\w+", text)))
        subs = sorted(set(re.findall(r"\b(?:call|goto|jumpif\w*)\s+(\w+)", text)))
        rows.append(dict(move=mv, name=names.get(mv, "?"), family=fam, label=lab, vanilla=vanilla or draft, draft=draft, tags=tags, subs=subs,
                         earliest=earliest[mv], learners=len(learners[mv]), trainers=trainer_uses[mv], **d))
    return rows


#  T-168. The scripts that are not moves: they play for a STATE (1.6's LEAKING, SUSPENDED, THROTTLED...), the
#  weather, an item, a ball, a level-up. T-137 closed when no MOVE animation still loaded a vanilla picture, and
#  that is when this layer showed -- 1.6 renamed every state and SUSPENDED still draws a Z.
GENERAL = ("Status_", "General_", "Special_", "SafariReaction_", "BallThrow")
STATE_WORD = {"Status_Poison": "LEAKING", "Status_Confusion": "THRASHING", "Status_Burn": "OVERHEATED",
              "Status_Sleep": "SUSPENDED", "Status_Paralysis": "THROTTLED", "Status_Freeze": "HUNG"}


def general():
    s_ours, s_up = read("data/battle_anim_scripts.s"), upstream("data/battle_anim_scripts.s")
    b_ours, b_up = blocks(s_ours), blocks(s_up)
    labs = [l for l in b_ours if l.startswith(GENERAL)]
    left = 0
    for pre in GENERAL:
        for l in (l for l in labs if l.startswith(pre)):
            van = b_ours[l] == b_up.get(l)
            #  A DISPATCH IS NOT VANILLA'S PICTURE. General_Sun is one line, `goto Move_SUNNY_DAY`, and that line is
            #  byte-identical to upstream -- but the animation it reaches is one we redrew, so the player sees ours.
            #  Sun, sandstorm, hail, the leech drain and the trap dispatcher all read as vanilla until this ran.
            body = [x.strip() for x in b_ours[l].splitlines() if x.strip()]
            body = [x for x in body if not x.endswith(":")]      # the block carries its own label line
            goto = [x[5:].strip() for x in body if x.startswith("goto ")]
            dispatch = van and goto and all(x.startswith(("goto ", "jumpargeq ", "createvisualtask ", "delay ", "end")) for x in body)
            if dispatch:
                van = False
            tags = sorted(set(re.findall(r"ANIM_TAG_(\w+)", b_ours[l])))
            left += van
            how = "vanilla" if van else ("-> %s" % goto[-1] if dispatch else "ours")
            print("  %-30s %-11s %-18s %s" % (l, STATE_WORD.get(l, ""), how, " ".join(tags)))
    print("  %d of %d animations that are not moves are still vanilla's" % (left, len(labs)))


def main():
    args = sys.argv[1:]
    if "--general" in args:
        general()
        return
    rows = census()
    if "--family" in args:
        want = args[args.index("--family") + 1].upper()
        sel = [r for r in rows if r["family"] == want]
        sel.sort(key=lambda r: (r["earliest"] is None, r["earliest"] if r["earliest"] is not None else 999, r["name"]))
        for r in sel:
            seen = "never" if r["earliest"] is None else ("TM/HM" if r["earliest"] == 0 else "Lv%d" % r["earliest"])
            print("  %-14s %-18s %-6s %3d daemons %3d trainer uses  %s" % (r["name"], r["move"][5:], seen, r["learners"], r["trainers"],
                                                                      ("draft" if r["draft"] else "vanilla") if r["vanilla"] else "ours"))
        return
    #  T-138. A description KEPT ON PURPOSE is not an outstanding one, and the ticket says keeping one needs a
    #  record rather than silence -- so the reason lives here, beside the count, and the census subtracts them.
    #  Byte-identity with upstream cannot tell a keep from an oversight; this table is what tells them apart.
    KEPT = {
        "MOVE_WHIRLWIND": "the foe is made to switch out, which is what EVICT means",
        "MOVE_ROAR": "the same text, and unloading is what forcing a switch is",
        "MOVE_ABSORB": "absorbing half the damage IS what INGEST says",
        "MOVE_MEGA_DRAIN": "draining half the damage IS what EXTRACT says",
        "MOVE_LEECH_LIFE": "the same, for SIPHON",
        "MOVE_GIGA_DRAIN": "the same, for DISTILL",
        "MOVE_RAGE": "stronger each time the user is hit: ACCUMULATE, exactly",
        "MOVE_BIDE": "endures two turns then pays back double, which is ACCRUE",
        "MOVE_SKULL_BASH": "DEFENSE first turn, attack second: PRELOAD",
        "MOVE_AMNESIA": "already ours -- 'Forgets about something'",
        "MOVE_THIEF": "taking the foe's held item is LIFT",
        "MOVE_CONVERSION_2": "changing type against the last attack is RECAST",
        "MOVE_BELLY_DRUM": "maximum ATTACK for half the HP is OVERCOMMIT",
        "MOVE_FALSE_SWIPE": "always leaves 1 HP: NONFATAL",
        "MOVE_FURY_CUTTER": "grows on each successive hit: RAMP UP",
        "MOVE_PAIN_SPLIT": "adds both HP and shares the total, which is LOAD BALANCE",
        "MOVE_VITAL_THROW": "acts after the foe and cannot miss: DEDUCE",
        "MOVE_STOCKPILE": "charges for later, three times: ENQUEUE",
        "MOVE_SUPERPOWER": "power at the cost of ATTACK and DEFENSE is BRUTE FORCE",
        "MOVE_ENDEAVOR": "gains as the user's HP falls toward the foe's: EQUALISE",
        "MOVE_SECRET_POWER": "an effect that varies with the terrain is AMBIENT",
        "MOVE_CAMOUFLAGE": "type follows the terrain, which is BLEND",
        "MOVE_AERIAL_ACE": "fast, single target, cannot be evaded: HOMING",
    }
    if "--descriptions" in args:
        #  T-138: a routine we renamed whose description is still byte-identical to upstream's. Not every one is
        #  wrong (2.8) -- this is the reading list, and it shrinks as each is kept on purpose or rewritten.
        src, up = read("src/move_descriptions.c"), upstream("src/move_descriptions.c")
        d, d_up = (dict(re.findall(r"(gMoveDescription_\w+)\[\] = _\((.*?)\);", t, re.S)) for t in (src, up))
        n_up = dict(re.findall(r'\[(MOVE_\w+)\]\s*= _\("(.*?)"\)', upstream("src/data/text/move_names.h")))
        named = {r["move"]: r for r in rows}
        hits = [(m, g) for m, g in re.findall(r"\[(MOVE_\w+)\s*-\s*1\]\s*=\s*(gMoveDescription_\w+)", src)
                if d.get(g) == d_up.get(g) and m in named and named[m]["name"] != n_up.get(m)]
        left = [(m, g) for m, g in hits if m not in KEPT]
        for m, g in left:
            print("  %-14s (was %-13s) %s" % (named[m]["name"], n_up.get(m), " ".join(re.findall(r'"(.*?)"', d[g])).replace("\\n", " ")))
        print("  %d still to read; %d kept on purpose, with the reason" % (len(left), len(hits) - len(left)))
        if "--kept" in args:
            for m, g in hits:
                if m in KEPT:
                    print("  KEPT %-14s %s" % (named[m]["name"], KEPT[m]))
        return
    if "--gfx" in args:
        use = defaultdict(set)
        for r in rows:
            if r["vanilla"]:
                for t in r["tags"]:
                    use[t].add(r["name"])
        for t, ms in sorted(use.items(), key=lambda kv: -len(kv[1])):
            print("  %-32s %3d  %s" % (t, len(ms), ", ".join(sorted(ms)[:6]) + (" ..." if len(ms) > 6 else "")))
        print("  %d effect graphics used by a still-vanilla animation" % len(use))
        return
    fams = defaultdict(list)
    for r in rows:
        fams[r["family"]].append(r)
    total = sum(r["vanilla"] for r in rows)
    print("  %-10s %5s %8s %8s %9s" % ("family", "moves", "vanilla", "in game", "seen <20"))
    for f, rs in sorted(fams.items(), key=lambda kv: min((r["earliest"] for r in kv[1] if r["earliest"] is not None), default=999)):
        ingame = [r for r in rs if r["earliest"] is not None or r["trainers"]]
        early = [r for r in rs if r["earliest"] is not None and r["earliest"] < 20]
        print("  %-10s %5d %8d %8d %9d" % (f, len(rs), sum(r["vanilla"] for r in rs), len(ingame), len(early)))
    print("  %d of %d move animations are still vanilla's" % (total, len(rows)))


if __name__ == "__main__":
    main()

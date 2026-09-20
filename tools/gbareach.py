#!/usr/bin/env python3
"""Which daemons a player can actually REACH, and how many of those are still vanilla's art (T-131, T-176).

    python3 tools/gbareach.py              # the report
    python3 tools/gbareach.py --list       # and name every species in each bucket

WHY THIS IS A TOOL AND NOT A COUNT IN A TICKET. T-131 scoped itself at "about 190-200 species a player can meet or
evolve into" and drew ten batches against that estimate; T-176 then found FORTY-THREE meetable daemons the estimate
had missed, because the list it worked from came from wild tables and scripts and these arrive by EVOLUTION, gift or
legendary. An estimate cannot be re-checked. This reads the game.

REACHABLE means one of:

    wild        src/data/wild_encounters.json -- every grass, water, rock-smash and fishing table
    trainer     src/data/trainer_parties.h -- every party of every trainer
    script      data/**/*.inc -- givemon, setwildbattle, the gift and static and legendary encounters
    trade       src/data/ingame_trades.h -- what is offered AND what is asked for
    starter     the starter table
    evolution   the transitive closure of src/data/pokemon/evolution.h over all of the above

and the art is VANILLA when graphics/pokemon/<species>/front.png is byte-identical to pret's own, which is the
census's own test (tools/gbaspritecensus.py) rather than a second opinion about it.
"""
import io, json, os, re, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
UPSTREAM = "upstream/master"
LIST = "--list" in sys.argv


def git(*args, binary=False):
    r = subprocess.run(["git", "-C", GBA] + list(args), capture_output=True)
    return r.stdout if binary else r.stdout.decode()


def species_in(text):
    return set(re.findall(r"SPECIES_([A-Z0-9_]+)", text))


def read(*parts):
    p = os.path.join(GBA, *parts)
    return open(p).read() if os.path.exists(p) else ""


def sources():
    out = {}
    j = json.loads(read("src/data/wild_encounters.json") or "{}")
    out["wild"] = {e["species"].replace("SPECIES_", "") for grp in j.get("wild_encounter_groups", [])
                   for f in grp.get("encounters", []) for k, v in f.items()
                   if isinstance(v, dict) for e in v.get("mons", [])}
    out["trainer"] = species_in(read("src/data/trainer_parties.h"))
    inc = []
    for base, _, files in os.walk(os.path.join(GBA, "data")):
        for f in files:
            if f.endswith(".inc"):
                inc.append(open(os.path.join(base, f), errors="ignore").read())
    out["script"] = species_in("\n".join(inc))
    out["trade"] = species_in(read("src/data/ingame_trades.h"))
    out["starter"] = species_in(read("src/data/starter_choose.h") + read("src/starter_choose.c")
                                + read("src/data/starters.h") + read("src/field_specials.c"))
    return out


def evolutions():
    """{from: {into, ...}} -- every evolution any of the methods reaches"""
    src = read("src/data/pokemon/evolution.h")
    out = {}
    for m in re.finditer(r"\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \}", src, re.S):
        out[m.group(1)] = species_in(m.group(2))
    return out


def close(seed, evo):
    seen, stack = set(seed), list(seed)
    while stack:
        s = stack.pop()
        for nxt in evo.get(s, ()):
            if nxt not in seen:
                seen.add(nxt); stack.append(nxt)
    return seen


def vanilla_fronts():
    have = set(git("ls-tree", "-r", "--name-only", UPSTREAM, "graphics/pokemon").split("\n"))
    out = set()
    for d in sorted(os.listdir(os.path.join(GBA, "graphics/pokemon"))):
        p = "graphics/pokemon/%s/front.png" % d
        if p not in have or not os.path.exists(os.path.join(GBA, p)):
            continue
        ours = Image.open(os.path.join(GBA, p))
        theirs = Image.open(io.BytesIO(git("show", "%s:%s" % (UPSTREAM, p), binary=True)))
        if ours.size == theirs.size and ours.tobytes() == theirs.tobytes():
            out.add(d.upper())
    return out


def main():
    src = sources()
    direct = set().union(*src.values())
    evo = evolutions()
    reach = close(direct, evo)
    reach.discard("NONE")
    print("  REACHABLE, by how a player gets there")
    for k in ("wild", "trainer", "script", "trade", "starter"):
        print("    %-9s %4d" % (k, len(src[k])))
    print("    %-9s %4d   (direct %d, +%d by evolution)" % ("all", len(reach), len(direct), len(reach) - len(direct)))

    van = vanilla_fronts()
    stuck = sorted(reach & van)
    spare = sorted(van - reach)
    print("\n  STILL ON VANILLA'S FRONT")
    print("    reachable   %4d   <- this is the number that matters" % len(stuck))
    print("    unreachable %4d   (evolutions of nothing, and species no map places)" % len(spare))
    if stuck:
        print("    " + ", ".join(s.title() for s in stuck))
    if LIST and spare:
        print("\n  UNREACHABLE AND VANILLA:\n    " + ", ".join(s.title() for s in spare))


if __name__ == "__main__":
    main()

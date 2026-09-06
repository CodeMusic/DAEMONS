#!/usr/bin/env python3
"""Audit the vertical slice -- Blanche to Slate -- against upstream.

    python3 tools/gbaslice.py            # summary
    python3 tools/gbaslice.py --vanilla  # every block still in vanilla's words

8 is unambiguous that the slice comes before the bestiary, and 9.3 records the
cost of the port in one line: *a port resets implementation to zero while the
design keeps galloping.* This measures how far from zero the slice actually is.

WHAT "OURS" MEANS HERE. A block is compared against upstream's by similarity,
the same test gbaindex.py uses and for the same reason: the vocabulary pass
rewrites POKeMON and TRAINER everywhere, so "did it change?" says yes to almost
everything and means nothing. Below 0.5 the sentence was rewritten; above it,
vanilla is still doing the talking with our nouns in its mouth.

That distinction is the whole point. A slice where every string differs from
upstream and none of it is ours is a slice that has been TRANSLATED, not
written -- and it will read as Kanto with the labels changed.
"""
import difflib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")

SLICE = [
    ("Blanche",        ["PalletTown", "PalletTown_PlayersHouse_1F", "PalletTown_PlayersHouse_2F",
                        "PalletTown_RivalsHouse", "PalletTown_ProfessorOaksLab"]),
    ("The Bleed",      ["Route1", "Route2", "Route22"]),
    ("Callow",         ["ViridianCity", "ViridianCity_House1", "ViridianCity_Mart",
                        "ViridianCity_PokemonCenter_1F", "ViridianCity_Gym", "ViridianCity_School"]),
    ("The Undertone",  ["ViridianForest"]),
    ("Slate",          ["PewterCity", "PewterCity_Gym", "PewterCity_Mart", "PewterCity_Museum_1F",
                        "PewterCity_Museum_2F", "PewterCity_House1", "PewterCity_House2",
                        "PewterCity_PokemonCenter_1F"]),
]
STR = re.compile(r'^\s*\.string "(.*)"\s*$')

def upstream(rel):
    return subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel],
                          capture_output=True, text=True).stdout

# ---------------------------------------------------------------- exemptions
#
# THE 0.5 TEST IS STRUCTURAL, NOT AUTHORIAL, AND FOR SOME BLOCKS THAT IS WRONG.
# "A sleeping daemon does not act" shares almost no wording with "A POKéMON
# can't attack if it's asleep" and still scores above 0.5 -- because a status
# explainer has to say what the condition does, that it persists and what cures
# it, IN THAT ORDER. Any correct rewrite scores high. So do receipts, capacity
# refusals, route signs and cries: their shape is fixed by the job they do, and
# forcing them under the threshold means writing them WORSE to satisfy a number.
#
# Those are counted separately as FUNCTIONAL rather than as vanilla, and the
# percentage is taken over the prose that is left. Judged on UPSTREAM's text,
# which does not move.
FUNCTIONAL = [
    r'\{(PLAYER|RIVAL)\} (received|got|put|switched|obtained)',
    r"(don't|do not) have (enough money|room|space)",
    r'^ROUTE \d',
    r'GYM.{0,4}LEADER:|WINNING TRAINERS',
    r'^[A-Z][A-Za-z]*: [A-Za-z]+ ?[a-z]*[!.]',      # a cry, not a line
]
FUNC_RE = [re.compile(x) for x in FUNCTIONAL]
SHORT = 45      # below this a block cannot diverge enough for the test to mean
                # anything -- "Come again!" against "Come again." scores 0.95

def functional(up):
    return len(up) < SHORT or any(r.search(up) for r in FUNC_RE)

def blocks(text):
    """Consecutive .string lines are one block, which is how a message is stored."""
    out, cur = [], []
    for line in text.split("\n"):
        m = STR.match(line)
        if m:
            cur.append(m.group(1))
        elif cur:
            out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out

def main():
    show = "--vanilla" in sys.argv
    tot_ours = tot_van = tot_same = tot_fn = 0
    print("  %-16s %-28s %5s %5s %5s %5s"
          % ("", "map", "ours", "van", "same", "fn"))
    for town, maps in SLICE:
        first = True
        for m in maps:
            rel = "data/maps/%s/text.inc" % m
            path = os.path.join(GBA, rel)
            if not os.path.isfile(path):
                continue
            mine, up = blocks(open(path, encoding="utf-8").read()), blocks(upstream(rel))
            if len(mine) != len(up):
                print("  %-16s %-28s  block count moved (%d vs %d)"
                      % (town if first else "", m, len(mine), len(up))); first = False
                continue
            ours = van = same = fn = 0
            for a, b in zip(mine, up):
                if functional(b):
                    fn += 1
                elif a == b:
                    same += 1
                elif difflib.SequenceMatcher(None, a, b).ratio() < 0.5:
                    ours += 1
                else:
                    van += 1
                    if show:
                        print("      %-24s %s" % (m, b[:88]))
            tot_ours += ours; tot_van += van; tot_same += same; tot_fn += fn
            print("  %-16s %-28s %5d %5d %5d %5d"
                  % (town if first else "", m, ours, van, same, fn))
            first = False
    n = tot_ours + tot_van + tot_same
    print("\n  %d prose blocks: %d ours (%d%%), %d vanilla reworded, %d untouched"
          % (n, tot_ours, 100 * tot_ours // max(1, n), tot_van, tot_same))
    print("  %d functional blocks exempt -- receipts, refusals, signs, cries, and"
          % tot_fn)
    print("  anything under %d characters, where the shape is the job." % SHORT)

main()

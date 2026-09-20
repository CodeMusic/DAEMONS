#!/usr/bin/env python3
"""The twelve reachable species that were never converted at all (T-131, after tools/gbareach.py measured them).

    python3 gfx/drafts/t131_twelve.py            # report every edit it would make
    python3 gfx/drafts/t131_twelve.py --write

WHAT THESE TWELVE ARE. gbareach.py reads which species a player can actually reach -- wild tables, every trainer
party, every script, the trades, the starters, and the closure of evolution.h over all of it -- and found thirteen
still wearing vanilla's front. Twelve of them had never been touched at ALL: vanilla ART and vanilla NAMES, absent
from the 229-name register. Ten are the Johto strays that vanilla FRLG sprinkles into Sevii trainer parties, and two
are LUGIA and HO-OH at Navel Rock, whom a player meets once and remembers.

The name, the category and the entry go in together, because a name without an entry is the thing this project keeps
finding later. The ART is drafted from the entry (gfx/drafts/t131/), which is the order T-176 settled: an entry that
names a SHAPE drafts well.

BOTH EDITIONS get the same entry text. The edition split is a per-entry decision (4.2) and none of these twelve is
one of the places it has anything to say.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

TWELVE = [
    # species const, our name, Index category, the entry, and the C text symbol
    ("HOOTHOOT",  "POLL",     "ASKING",     ["It asks the same question at a fixed", "interval and writes down the answer.", "It does not wait to be asked to."],                 "Hoothoot"),
    ("NOCTOWL",   "SUPERVISOR", "WATCHING",   ["It watches one thing that should keep", "moving. If the movement stops, it", "starts that thing again."],                          "Noctowl"),
    ("CHINCHOU",  "PILOT",    "STANDBY",    ["A light kept lit for no purpose but to", "show the line is live. It is taken", "into the dark for that reason."],                   "Chinchou"),
    ("LANTURN",   "SOUNDING", "MEASURING",  ["It measures the dark by sending and", "waiting. What comes back is how far", "down the bottom is."],                                "Lanturn"),
    ("SUNKERN",   "STARVED",  "WAITING",    ["It is owed a turn and has not had one.", "Everything it needs is here. Nothing", "has given it the time."],                         "Sunkern"),
    ("SUNFLORA",  "QUOTA",    "GRANTED",    ["It was finally given the share it was", "owed, and opened at once. It can do", "nothing it could not do before."],                  "Sunflora"),
    ("SUDOWOODO", "FAKEROOT", "PRETENDING", ["It reports itself as something older", "and better rooted than it is. Nothing", "has ever checked."],                               "Sudowoodo"),
    ("GIRAFARIG", "DUPLEX",   "TWO-WAY",    ["It sends and receives at once, from", "opposite ends. Neither end is told", "what the other has agreed to."],                       "Girafarig"),
    ("SNUBBULL",  "WARNING",  "HARMLESS",   ["It announces a fault in the loudest", "voice it has. Nothing has failed. It", "will say so again tomorrow."],                       "Snubbull"),
    ("MILTANK",   "CACHE",    "KEEPING",    ["It holds what everything nearby will", "want next and gives it up at once.", "Asking it costs less than working."],                 "Miltank"),
    ("LUGIA",     "TRITON",   "ACCORD",     ["Three of them quarrelled until it", "arrived. It took no side and said", "nothing. They have not quarrelled since."],               "Lugia"),
    ("HO_OH",     "PHOENIX",  "RETURN",     ["It is the only one that can start", "itself. What it leaves behind is what", "it starts from."],                                    "HoOh"),
]

#  NOCTOWL was written in as WATCHDOG and check_lexicon caught it: WATCHDOG is already an ITEM (our Ice
#  Heal, "a watchdog notices a process that stopped answering, and resets it"), and item names live in
#  items.json whose generated header is gitignored -- so a grep over src/data/text/ says the word is free.
#  SUPERVISOR is what OTP calls the thing that restarts a crashed child, which is the entry unchanged.
#  vanilla's own name, as the tables spell it -- HO_OH's constant and its string disagree, which is vanilla's doing
VANILLA = {"HO_OH": "HO-OH"}


def edit(path, fn):
    p = os.path.join(E, path)
    before = open(p).read()
    after, n = fn(before)
    print("  %-46s %d change(s)" % (path, n))
    if WRITE and after != before:
        open(p, "w").write(after)
    return n


def main():
    total = 0

    def names(s):
        n = 0
        for const, new, _, _, _ in TWELVE:
            old = VANILLA.get(const, const)
            pat = r'(\[SPECIES_%s\] = _\(")%s("\))' % (const, re.escape(old))
            s, k = re.subn(pat, r"\g<1>%s\g<2>" % new, s)
            if not k:
                print("     ! SPECIES_%s does not read %r" % (const, old))
            n += k
        return s, n
    total += edit("src/data/text/species_names.h", names)

    def cats(s):
        n = 0
        for const, _, cat, _, _ in TWELVE:
            pat = r'(\[NATIONAL_DEX_%s\] =\s*\{\s*\.categoryName = _\(")[^"]*("\))' % const
            s, k = re.subn(pat, r"\g<1>%s\g<2>" % cat, s)
            if not k:
                print("     ! NATIONAL_DEX_%s has no categoryName here" % const)
            n += k
        return s, n
    total += edit("src/data/pokemon/pokedex_entries.h", cats)

    def entries(s):
        n = 0
        for _, _, _, lines, sym in TWELVE:
            body = "".join('    "%s\\n"\n' % l for l in lines[:-1]) + '    "%s");' % lines[-1]
            pat = r'(const u8 g%sPokedexText\[\] = _\(\n)(?:\s*"[^"]*"\n)*\s*"[^"]*"\);' % sym
            s, k = re.subn(pat, lambda m: m.group(1) + body, s)
            if not k:
                print("     ! g%sPokedexText not found" % sym)
            n += k
        return s, n
    for f in ("src/data/pokemon/pokedex_text_fr.h", "src/data/pokemon/pokedex_text_lg.h"):
        total += edit(f, entries)

    def tower(s):
        #  trainer_tower_sets.c holds species names as LITERALS, which is how MAINFRAME and PUNCHCARD were caught
        n = 0
        for const, new, _, _, _ in TWELVE:
            old = VANILLA.get(const, const)
            s, k = re.subn(r'"%s"' % re.escape(old), '"%s"' % new, s)
            n += k
        return s, n
    total += edit("src/trainer_tower_sets.c", tower)

    print("  %d edit(s)%s" % (total, "" if WRITE else "  (report only; pass --write)"))


if __name__ == "__main__":
    main()

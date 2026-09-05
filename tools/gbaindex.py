#!/usr/bin/env python3
"""What to read in which cartridge -- the Index, per edition.

    python3 tools/gbaindex.py            # ours
    python3 tools/gbaindex.py --all      # every entry that differs

0.4 rules that the two Indexes disagree ON PURPOSE: Gen 3 keeps a separate
description file per edition, CONTENT reports what a daemon does and CONTEXT
what follows from it.

TWO TESTS THAT DO NOT WORK, both tried. "Does it differ between editions?" is
useless because VANILLA ALREADY VARIES nearly all of its own entries. And "did
vanilla have them identical?" fails for the same reason -- every entry this
project has paired was one vanilla had already varied.

So the test is SIMILARITY TO UPSTREAM, which is what port_dialogue.py uses for
the same reason: a vocabulary substitution leaves most of a sentence standing,
and an entry we wrote does not. Below 0.5 it is ours.

THE PLAY-TEST ANSWER IS THE PAIR LIST. Those are the entries where reading the
other cartridge tells you something, and there is no way to see both at once.
"""
import difflib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
ENTRIES = "src/data/pokemon/pokedex_entries.h"
FR = "src/data/pokemon/pokedex_text_fr.h"
LG = "src/data/pokemon/pokedex_text_lg.h"
LIT = re.compile(r'const u8 (\w+PokedexText)\[\] = _\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)')
PIECE = re.compile(r'"((?:[^"\\]|\\.)*)"')

def upstream(rel):
    return subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel],
                          capture_output=True, text=True).stdout

def texts(rel, raw=None):
    src = raw if raw is not None else open(os.path.join(GBA, rel), encoding="utf-8").read()
    return {m.group(1): ''.join(PIECE.findall(m.group(2))) for m in LIT.finditer(src)}

def named():
    """{species constant: our name} for every species we renamed."""
    rel = "src/data/text/species_names.h"
    pat = re.compile(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)')
    ours = dict(pat.findall(open(os.path.join(GBA, rel), encoding="utf-8").read()))
    van = dict(pat.findall(upstream(rel)))
    return {k: v for k, v in ours.items() if van.get(k) != v}

def dex_symbol():
    """species -> its description symbol, read from the entry table itself
    rather than guessed from the name. MR_MIME and NIDORAN would not survive
    a guess, and a wrong symbol would silently report 'no entry'."""
    src = open(os.path.join(GBA, ENTRIES), encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"\[NATIONAL_DEX_(\w+)\][^}]*?\.description = (\w+),", src, re.S):
        out[m.group(1)] = m.group(2)
    return out

def main():
    fr, lg = texts(FR), texts(LG)
    ufr, ulg = texts(FR, upstream(FR)), texts(LG, upstream(LG))
    sym = dex_symbol()
    ours = named()

    differ = sum(1 for k in fr if k in lg and fr[k] != lg[k])
    print("  %d entries differ between the editions in all (vanilla varies most of its own)\n"
          % differ)

    pairs, single, inherited = [], [], []
    for spc, name in sorted(ours.items(), key=lambda kv: kv[1]):
        s = sym.get(spc)
        if not s or s not in fr or s not in lg:
            continue
        ratio = lambda a, b: difflib.SequenceMatcher(None, a, b or "").ratio()
        mine = (ratio(fr[s], ufr.get(s)) < 0.5) and (ratio(lg[s], ulg.get(s)) < 0.5)
        if not mine:
            inherited.append((name, s))
        elif fr[s] != lg[s]:
            pairs.append((name, s))
        else:
            single.append((name, s))

    print("  WRITTEN AS A PAIR -- read these in BOTH cartridges (%d)" % len(pairs))
    for name, s in pairs:
        print("     %-11s CONTENT  %s" % (name, fr[s].replace("\\n", " ")[:58]))
        print("     %-11s CONTEXT  %s" % ("", lg[s].replace("\\n", " ")[:58]))
    print("\n  ours, one entry copied into both -- either cartridge will do (%d)" % len(single))
    print("     " + ", ".join(n for n, _ in single))
    if inherited:
        print("\n  renamed, but the ENTRY is still vanilla's -- only the vocabulary moved (%d)"
              % len(inherited))
        print("     " + ", ".join(n for n, _ in inherited))

main()

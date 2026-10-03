#!/usr/bin/env python3
"""T-210: check a batch's words before they go into the build. Report only; it writes nothing.

    python3 tools/t210check.py docs/drafts/t210_batch5.json     # one batch
    python3 tools/t210check.py                                  # every docs/drafts/t210_batch*.json

It fails on a name over 10 characters or a category over 11; any word of a name that is a word of a name in use
(species other than the batch's own, routines, abilities, items, map sections, trainer classes) -- PLATEAU was
UMBRA PLATEAU's, ATTRACTOR and UPTIME were taken; a name used twice; a category that repeats its own name (SAVESTATE's
SAVED STATE: a category word of five letters or more inside the name, or the name inside the category); and an INDEX
line wider than the widest line the existing entries use, measured in the game's font (check_lexicon's width).
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = sys.argv[:1]                 # check_lexicon reads argv when imported
sys.path.insert(0, os.path.join(ROOT, "tools"))
import check_lexicon
WIDTH = check_lexicon._load_textwidth()
WORD = r"[A-Z0-9É']+"


def read(path):
    return open(os.path.join(GBA, path), encoding="utf-8").read()


def names_in_use(skip):
    found = {}
    for sp, n in re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/data/text/species_names.h")):
        if sp not in skip:
            found[n] = "species " + sp
    for m, n in re.findall(r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/data/text/move_names.h")):
        found[n] = "routine " + m
    for n in re.findall(r'_\("([^"]*)"\)', read("src/data/text/abilities.h")):
        if len(n) <= 13:                # the names; the descriptions are longer
            found[n] = "ability"
    for n in re.findall(r'"english":\s*"([^"]*)"', read("src/data/items.json")):
        found[n] = "item"
    for n in re.findall(r'"name":\s*"([^"]*)"', read("src/data/region_map/region_map_sections.json")):
        found[n] = "map section"
    for n in re.findall(r'_\("([^"]*)"\)', read("src/data/text/trainer_class_names.h")):
        found[n] = "trainer class"
    words = {}
    for n, kind in found.items():
        for w in re.findall(WORD, n.upper()):
            if len(w) > 2:
                words.setdefault(w, []).append("%s (%s)" % (n, kind))
    return words


def widest_entry_line():
    widest = 0
    for f in ("src/data/pokemon/pokedex_text_fr.h", "src/data/pokemon/pokedex_text_lg.h"):
        for line in re.findall(r'^\s*"([^"]*)"', read(f), re.M):
            widest = max(widest, WIDTH(line.replace("\\n", "")))
    return widest


def check(path, widest):
    batch = json.load(open(path))["daemons"]
    words = names_in_use({x["species"] for x in batch})
    problems, seen = [], set()
    for x in batch:
        name, cat = x["name"], x["category"]
        if len(name) > 10:
            problems.append("%s: name is %d characters (10 at most)" % (name, len(name)))
        if len(cat) > 11:
            problems.append("%s: category %s is %d characters (11 at most)" % (name, cat, len(cat)))
        for w in re.findall(WORD, name):
            if w in words:
                problems.append("%s: %s is already in %s" % (name, w, ", ".join(words[w][:3])))
        if name in seen:
            problems.append("%s: named twice in the batch" % name)
        seen.add(name)
        flat = cat.replace(" ", "")
        if name in flat or any(len(w) >= 5 and w in name for w in cat.split()):
            problems.append("%s: its category %s repeats its name" % (name, cat))
        for key in ("content", "context"):
            for line in x[key]:
                if WIDTH(line) > widest:
                    problems.append("%s: a %s line is %dpx (%d at most): %s" % (name, key.upper(), WIDTH(line), widest, line))
    return len(batch), problems


def main():
    paths = args or sorted(glob.glob(os.path.join(ROOT, "docs/drafts/t210_batch*.json")))
    widest = widest_entry_line()
    bad = 0
    for p in paths:
        n, problems = check(p, widest)
        print("  %-22s %d daemons, %s" % (os.path.basename(p), n, "clear" if not problems else "%d problem(s)" % len(problems)))
        for line in problems:
            print("    " + line)
        bad += len(problems)
    print("  widest existing INDEX line %dpx; %s" % (widest, "every batch clear" if not bad else "%d problem(s)" % bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

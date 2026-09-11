#!/usr/bin/env python3
"""One word, one meaning. Prove no name in the lexicon is used twice.

    python3 tools/check_lexicon.py       # exits non-zero if any word is doubled

WHY THIS EXISTS. INTERRUPT was assigned to POKé FLUTE and to ICE HEAL six weeks
apart and nothing caught it. The fix -- PREEMPT -- collided with MANKEY, which
had been named PREEMPT four days earlier, and nothing caught that either. Both
times a human found it by reading a list aloud.

4.26 DID run a collision check when the bestiary was named. It validated the
new species against species, moves and types. It did not check ITEMS, because
at that moment the item pass had not happened yet -- so the check was complete
for the day it was written and incomplete by the following week.

That is the general failure: a check scoped to the surfaces that existed when
it was written. This one reads every surface out of the build each time it runs,
so a surface added later is covered without anyone remembering to add it.

WHAT COUNTS AS A COLLISION. Two DIFFERENT things wearing the same word. A move
and a type both called GROWTH is a collision; the FROZEN type and the FROZEN
state would be too, which is exactly why 1.6 went looking for HUNG.

Deliberate doubles live in ALLOWED below, each with the reason it is allowed.

IT ALSO CHECKS THE VERSION, which is the same failure one level up. Two
sessions wrote a 2.7 on the same day and both took v11.112; the same two then
both took v11.115. A version is a name like any other -- it means one release
-- and it lived in one line of one file with nothing reading it back. So the
CHANGELOG headings, vision.md's version line, the README row and the PDF on
disk are compared against each other here, for the same reason the lexicon is:
a contract between places with no compiler in between needs something to be
the compiler.

Gaps are NOT a fault. The project has jumped 1.0 -> 11.8 -> 11.108 on purpose.
Duplicates, disagreement between the four places, and a newest entry that is
not at the top are.

AND IT CHECKS TODO.md's TICKET IDS, which is the same rule again one level up.
Two sessions issued T-13 through T-17 within the hour in a file whose own first
line is that ids are permanent. Here a GAP IS a fault, unlike the version: that
file says a finished ticket is struck through and never deleted, so a missing
number means one was.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
DOCS = os.path.join(ROOT, "docs")

#  Doubles that are on purpose. A word here has been argued for, not overlooked.
ALLOWED = {
    "OVERHEAT": "the ENTROPY move and the OVERHEATED state agreeing is the point (2.8)",
}

#  Same idea as ALLOWED, for the version. A number here is a fault that has
#  been RECORDED rather than one that has been forgiven -- and the reason it
#  is not simply renumbered is that the sequence around it is dense, so
#  fixing one entry means shifting a week of history to erase a mistake that
#  is now evidence. The check exists to stop the NEXT one.
ALLOWED_VERSIONS = {
    "11.25": "two releases on 2026-09-02 -- setup.sh and the 66 sprites. "
             "Found by this check a week later; 11.24 and 11.26 are both taken, "
             "so renumbering would shift everything below it",
}

STATES = ["LEAKING", "CASCADING", "SUSPENDED", "THROTTLED",
          "OVERHEATED", "HUNG", "THRASHING", "HALTED"]


def vkey(v):
    """11.9 sorts BELOW 11.108, so compare the parts as numbers."""
    return tuple(int(x) for x in v.split("."))


def check_version():
    """The CHANGELOG, the bible, the README row and the PDF must agree."""
    bad = []
    cl = os.path.join(DOCS, "CHANGELOG.md")
    vm = os.path.join(DOCS, "vision.md")
    if not (os.path.isfile(cl) and os.path.isfile(vm)):
        return bad, {}

    heads = re.findall(r"(?m)^## v(\d+(?:\.\d+)*)\s+—\s+(\d{4}-\d{2}-\d{2})\s*$",
                       open(cl, encoding="utf-8").read())
    if not heads:
        return [("CHANGELOG.md", "no version headings matched -- the format moved")], {}

    seen = {}
    for v, d in heads:
        seen.setdefault(v, []).append(d)
    for v, dates in seen.items():
        if len(dates) > 1 and v not in ALLOWED_VERSIONS:
            bad.append(("v%s" % v,
                        "%d CHANGELOG entries share it (%s)" % (len(dates), ", ".join(dates))))

    #  Newest first is the file's whole convention, and it is what breaks when
    #  two sessions insert at the top on the same day.
    top_v, top_d = heads[0]
    for v, d in heads[1:]:
        if vkey(v) > vkey(top_v) or d > top_d:
            bad.append(("v%s" % v, "dated %s but filed below v%s (%s)" % (d, top_v, top_d)))
            break

    #  ...and the other three places that carry the same number.
    m = re.search(r"the living design bible, v(\d+(?:\.\d+)*)", open(vm, encoding="utf-8").read())
    if not m:
        bad.append(("vision.md", "no version line found"))
    elif m.group(1) != top_v:
        bad.append(("vision.md", "says v%s, CHANGELOG's newest is v%s" % (m.group(1), top_v)))

    #  The README deliberately keeps rows for frozen historical snapshots, so
    #  only two rows carry the CURRENT number: the living one and the newest
    #  cut. Reading every "v11.x" in the file reported v1.0 as a disagreement,
    #  which is a row doing its job.
    rd = os.path.join(DOCS, "README.md")
    if os.path.isfile(rd):
        rv = set()
        for line in open(rd, encoding="utf-8"):
            if "working" in line or "snapshot** at v" in line:
                rv |= set(re.findall(r"v(\d+(?:\.\d+)+)", line))
        #  AN ABSENT ROW IS A FAULT, NOT AGREEMENT. docs/README.md was left at
        #  zero bytes twice in two days, and both times this reported that the
        #  version agreed in all four places -- because a file with no rows
        #  disagrees with nothing. A check that cannot fail on a missing input
        #  is not checking that input, and it goes quiet exactly when the
        #  surface it watches has been destroyed.
        if not rv:
            bad.append(("README.md", "carries no version row at all -- the "
                        "living row and the snapshot row are two of the four "
                        "places, and an empty file agrees with everything"))
        off = {v for v in rv if v != top_v}
        if off:
            bad.append(("README.md", "row says v%s, CHANGELOG's newest is v%s"
                        % ("/".join(sorted(off, key=vkey)), top_v)))

    #  Older snapshots are KEPT on purpose -- v1.0 and v11.8 are both rows in
    #  the README -- so the only fault here is the newest one missing.
    cut = sorted({f.split("-v")[-1][:-4] for f in os.listdir(DOCS)
                  if f.startswith("CONTEXT-CONTENT-design-bible-v") and f.endswith(".pdf")},
                 key=vkey)
    if cut and cut[-1] != top_v:
        bad.append(("docs/*.pdf", "newest cut is v%s, CHANGELOG's newest is v%s"
                    % (cut[-1], top_v)))
    return bad, seen


def check_tickets():
    """One id, one job -- the same rule as the lexicon, one level up again.

    Two sessions issued T-13 through T-17 within the hour in a file whose own
    first rule is that IDS ARE PERMANENT. Nothing read it back.

    A GAP IS A FAULT HERE, and this is where tickets differ from versions.
    Versions jump on purpose -- 1.0 to 11.8 to 11.108 -- so a gap there means
    nothing. TODO.md says a finished ticket is struck through and never
    deleted, so a missing number means one WAS deleted, which is the thing
    that rule exists to prevent.
    """
    bad = []
    f = os.path.join(DOCS, "TODO.md")
    if not os.path.isfile(f):
        return bad
    ids = re.findall(r"\|\s*\*\*(T-(\d+))\*\*", open(f, encoding="utf-8").read())
    if not ids:
        return [("TODO.md", "no ticket rows matched -- the format moved, or the file is empty")]
    nums = [int(n) for _, n in ids]
    for n in sorted(set(nums)):
        if nums.count(n) > 1:
            bad.append(("T-%02d" % n, "%d rows share it -- ids are permanent" % nums.count(n)))
    missing = [n for n in range(1, max(nums) + 1) if n not in nums]
    if missing:
        bad.append(("TODO.md", "no row for %s -- a finished ticket is struck through, "
                    "never deleted" % ", ".join("T-%02d" % n for n in missing)))
    return bad


def read(rel, pat):
    f = os.path.join(GBA, rel)
    if not os.path.isfile(f):
        return []
    return re.findall(pat, open(f, encoding="utf-8", errors="ignore").read())


def check_stale_names():
    """No line of dialogue may name a place, a move or a daemon by a name we replaced.

    Found 2026-09-10, in three widening passes. First six lines still sending
    the player to ROCK TUNNEL after the map had said THE BLACKOUT for weeks.
    Then, once moves were included, THIRTY-ONE more: the game teaching CUT,
    FLY, DIG and DOUBLE-EDGE, none of which are the names of those moves any
    more. A player is told to use a move that does not exist.

    Two things this has to get right, and the first version got neither:

      * READ WHOLE BLOCKS. A name splits across two `.string` lines, and
        `ROCK SMASH` hid in exactly that seam for weeks.
      * NEVER FLAG AN OLD NAME THAT IS SOMEBODY'S CURRENT NAME. GRASS became
        GROWTH and GROWTH is also a move we renamed, so a naive map reports
        every line that says GROWTH. The rename map is filtered against the
        live lexicon before anything is matched.

    Derived, not listed: every map is ours-vs-upstream, so a rename made
    tomorrow is covered tonight with nobody remembering to add it.
    """
    import json, subprocess

    def upstream(rel):
        r = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel],
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None

    renamed = {}

    rel = "src/data/region_map/region_map_sections.json"
    up = upstream(rel)
    if up and os.path.isfile(os.path.join(GBA, rel)):
        van = {m["id"]: m.get("name") for m in json.loads(up)["map_sections"]}
        ours = {m["id"]: m.get("name")
                for m in json.load(open(os.path.join(GBA, rel)))["map_sections"]}
        renamed.update({van[k]: ours[k] for k in ours
                        if van.get(k) and ours.get(k) and van[k] != ours[k]})

    for rel, pat in (("src/data/text/move_names.h", r'\[MOVE_\w+\]\s*=\s*_\("([^"]+)"\)'),
                     ("src/data/text/species_names.h", r'\[SPECIES_\w+\]\s*=\s*_\("([^"]+)"\)')):
        up = upstream(rel)
        f = os.path.join(GBA, rel)
        if not up or not os.path.isfile(f):
            continue
        ours = re.findall(pat, open(f, encoding="utf-8", errors="ignore").read())
        van = re.findall(pat, up)
        renamed.update({van[i]: ours[i] for i in range(min(len(ours), len(van)))
                        if van[i] != ours[i]})

    #  the live lexicon, so an old name that is now somebody else's name is
    #  never reported -- this is the GROWTH case and it is not hypothetical
    live = set()
    for rel, pat in (("src/data/text/move_names.h", r'_\("([^"]+)"\)'),
                     ("src/data/text/species_names.h", r'_\("([^"]+)"\)'),
                     ("src/battle_main.c", r'\[TYPE_\w+\]\s*=\s*_\("(\w+)"\)'),
                     ("src/data/region_map/region_map_entry_strings.h", r'_\("([^"]+)"\)')):
        f = os.path.join(GBA, rel)
        if os.path.isfile(f):
            live |= set(re.findall(pat, open(f, encoding="utf-8", errors="ignore").read()))
    renamed = {o: n for o, n in renamed.items()
               if o not in live and o.isupper() and len(o) > 2}

    out = []
    for root, dirs, files in os.walk(os.path.join(GBA, "data")):
        for fn in files:
            if fn != "text.inc":
                continue
            p = os.path.join(root, fn)
            lines = open(p, encoding="utf-8", errors="ignore").read().split("\n")
            i = 0
            while i < len(lines):
                m = re.match(r'\s*\.string "(.*)"', lines[i])
                if not m:
                    i += 1
                    continue
                start, parts = i, []
                while i < len(lines):
                    mm = re.match(r'\s*\.string "(.*)"', lines[i])
                    if not mm:
                        break
                    parts.append(mm.group(1))
                    i += 1
                #  the whole block, escapes flattened, so a name split over a
                #  line break is still one name
                s = re.sub(r"\\[nlp]", " ", "".join(parts))
                for old, new in renamed.items():
                    if re.search(r"(?<![A-Z])%s(?![A-Z])" % re.escape(old), s):
                        out.append(("%s:%d" % (os.path.relpath(p, GBA), start + 1),
                                    "says %s; the game calls it %s" % (old, new)))
    return out


def main():
    surfaces = {
        "species": read("src/data/text/species_names.h",
                        r'\[SPECIES_\w+\]\s*=\s*_\("([^"]+)"\)'),
        "move":    read("src/data/text/move_names.h",
                        r'\[MOVE_\w+\]\s*=\s*_\("([^"]+)"\)'),
        "type":    read("src/battle_main.c",
                        r'\[TYPE_\w+\]\s*=\s*_\("(\w+)"\)'),
        "ability": read("src/data/text/abilities.h",
                        r'\[ABILITY_\w+\]\s*=\s*_\("([^"]+)"\)'),
        #  Added after PSYCHIC -> CONSTRUE was chosen twice: once for the
        #  trainer class and once, weeks later, for the CONTEXT routine.
        #  Neither pass could see the other because this table was not read.
        "class":   read("src/data/text/trainer_class_names.h",
                        r'\[TRAINER_CLASS_\w+\]\s*=\s*_\("([^"]+)"\)'),
        "state":   STATES,
    }
    f = os.path.join(GBA, "src/data/items.json")
    if os.path.isfile(f):
        d = json.load(open(f, encoding="utf-8"))
        surfaces["item"] = [i["english"] for i in (d if isinstance(d, list)
                                                   else d.get("items", d))]

    seen = {}
    for label, words in surfaces.items():
        for w in words:
            w = w.strip()
            #  A one- or two-letter label is a slot, not a name. Vanilla's own
            #  placeholders ("-", "???") would otherwise report as collisions
            #  against every other placeholder in the build.
            if len(w) < 3 or set(w) <= set("-?"):
                continue
            seen.setdefault(w, set()).add(label)

    bad = [(w, sorted(v)) for w, v in seen.items()
           if len(v) > 1 and w not in ALLOWED]
    vbad, seen_versions = check_version()
    tbad = check_tickets()
    print("  %d names across %s" % (len(seen), ", ".join(sorted(surfaces))))
    for w, reason in sorted(ALLOWED.items()):
        if w in seen and len(seen[w]) > 1:
            print("  ..  %-14s allowed: %s" % (w, reason))
    if not bad:
        print("  no word means two things.")
    else:
        print("\n  %d word(s) mean two things:\n" % len(bad))
        for w, where in sorted(bad):
            print("   %-16s %s" % (w, " + ".join(where)))

    for v, reason in sorted(ALLOWED_VERSIONS.items()):
        if len(seen_versions.get(v, [])) > 1:
            print("  ..  v%-13s allowed: %s" % (v, reason))
    if not vbad:
        print("  the version agrees in all four places.")
    else:
        print("\n  %d version disagreement(s):\n" % len(vbad))
        for what, why in vbad:
            print("   %-16s %s" % (what, why))

    pbad = check_stale_names()
    if not pbad:
        print("  no dialogue names a place, move or daemon we renamed.")
    else:
        print("\n  %d stale name(s) in dialogue:\n" % len(pbad))
        for what, why in pbad:
            print("   %-44s %s" % (what, why))

    if not tbad:
        print("  every ticket id is used once.")
    else:
        print("\n  %d ticket id problem(s):\n" % len(tbad))
        for what, why in tbad:
            print("   %-16s %s" % (what, why))
    return 1 if (bad or vbad or tbad or pbad) else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""T-23, the naming half: the Sevii Islands' place names.

    python3 tools/port_sevii.py [--write]

8.2a's tone rule is that KANTO TELLS YOU WHAT THINGS ARE AND THE ISLANDS TELL
YOU HOW THEY LOOK FROM WHERE THE SPEAKER IS STANDING, and its grace note is
that the mainland has names and the islands have numbers -- places ON them are
"labels applied by whoever arrived first, on an island nobody named."

Reading what is actually out there splits the 35 places three ways, and the
split is most of the work:

  NUMBERED       THREE ISLE PORT, FIVE ISLE MEADOW, SEVII ISLE 6..24. A place
                 that carries its island's number is a place NOBODY NAMED.
                 That is the grace note itself, so they keep the number.
  TRANSLITERATED TANOBY, and the seven chambers. 4.24 makes these an alphabet
                 nobody reads -- so their names are transliterations, not
                 translations, and renaming them would be translating the one
                 thing whose point is that you cannot. They keep their sounds.
  NAMED          the twenty-one below. Somebody arrived and called it
                 something, and what they called it says where they stood.

NAVEL ROCK and BIRTH ISLAND are left by 2.10: no player of this game can reach
either without an event ticket that was never distributed here.

Two caps, both derived and neither declared anywhere:

  * 18 CHARACTERS, from `u8 mapName[19]` in src/region_map.c.
  * 112 PIXELS, from map_name_popup.c, which centres with
        xpos = (maxWidth - GetStringWidth(...)) / 2
    on UNSIGNED values. A name wider than 112px underflows u32 and the popup
    draws it somewhere off the window rather than clipping it.

Vanilla's own widest mapsec name is measured on every run and reported as the
demonstrated-safe width -- a floor, not a ceiling, exactly as engine.md says.

And the trap this tool exists to not repeat: RENAMING A MAPSEC RENAMES A C
SYMBOL THAT src/region_map.c REFERS TO BY HAND. The generator builds those
symbols out of the name's BYTES, so the rename has to be carried into the .c
by the same rule. That is done here rather than remembered.
"""
import json, os, re, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GBA  = os.path.join(ROOT, "engineGba")
JSON = os.path.join(GBA, "src", "data", "region_map", "region_map_sections.json")
RMC  = os.path.join(GBA, "src", "region_map.c")

CHAR_CAP  = 18     # u8 mapName[19] in region_map.c
PIXEL_CAP = 112    # the unsigned centring in map_name_popup.c

#  The twenty-one. Left column is what vanilla shipped; it is matched against
#  UPSTREAM rather than trusted, so a typo here is an error and not a silent
#  no-op. Right column is ours, and the note is why that label, from where.
NAMED = {
    #  ONE ISLAND
    "KINDLE ROAD":     ("SMOKE ROAD",     "you walk it looking at the mountain, which is smoking"),
    "TREASURE BEACH":  ("FINDERS BEACH",  "somebody found something here once and the name kept the promise"),
    "MT. EMBER":       ("MT. SMOULDER",   "burning without flame is what it does and what it looks like from the sea"),
    "EMBER SPA":       ("KETTLE SPRING",  "named for the only hot thing the namer had a word for"),
    #  TWO ISLAND
    "CAPE BRINK":      ("THE OVERLOOK",   "a cape is a place you look FROM -- and the other meaning sits underneath, unpointed at"),
    #  THREE ISLAND
    "BOND BRIDGE":     ("LONGCROSS",      "it is long and you cross it; nobody was feeling poetic"),
    "BERRY FOREST":    ("DENSE WOOD",     "what it is like to be in, said by someone who had been in it"),
    #  FOUR ISLAND
    "WATER LABYRINTH": ("TANGLEWATER",    "the water is the maze, which is not obvious until you are in it"),
    "ICEFALL CAVE":    ("STILLFALL CAVE", "a waterfall that stopped -- and PHLEGMATIC is in it, slow, which nobody says"),
    #  FIVE ISLAND
    "RESORT GORGEOUS": ("RESORT SUBLIME", "somebody named their own resort, and slightly overdid it"),
    "MEMORIAL PILLAR": ("SOMEONE'S STONE","a stone someone put up. Not knowing whose is the point of it"),
    "OUTCAST ISLAND":  ("NOBODY'S ISLE",  "the grace note said an island nobody named, so one of them says so"),
    "LOST CAVE":       ("THE WRONG WAY",  "named by somebody who took it"),
    #  SIX ISLAND
    "GREEN PATH":      ("SLOW WALK",      "and the doctrine's man takes eight visits to get through it"),
    "WATER PATH":      ("LONG WADE",      "what it takes, rather than what it is"),
    "RUIN VALLEY":     ("WHAT REMAINS",   "the islands offer a second reading; this one offers it in the name"),
    "PATTERN BUSH":    ("THE SAME BUSH",  "a maze where every corner looks like the last one, described honestly"),
    "DOTTED HOLE":     ("THE DOTS",       "said by somebody who could see them and could not read them"),
    "ALTERING CAVE":   ("OTHER CAVE",     "it never holds the same thing twice, so the label never settled either"),
    #  SEVEN ISLAND
    "CANYON ENTRANCE": ("THE WAY IN",     "the plainest label on the islands, and nobody improved on it"),
    "SEVAULT CANYON":  ("LONG DROP",      "a canyon said from the top of it"),
}

#  Kept, on purpose, each with the rule that keeps it. Reported every run so a
#  reader can see these were decided rather than missed.
KEPT = [
    ("ONE..SEVEN ISLAND",                "8.2a's grace note: the islands have numbers"),
    ("THREE ISLE PORT / PATH",           "carries its island's number, so nobody named it"),
    ("FIVE ISLE MEADOW",                 "carries its island's number, so nobody named it"),
    ("SEVII ISLE 6, 7, 8, 9, 22, 23, 24","carries its island's number, so nobody named it"),
    ("TANOBY RUINS / KEY / CHAMBERS",    "4.24: an alphabet nobody reads. The name is a transliteration"),
    ("MONEAN .. VIAPOIS CHAMBER",        "the same seven sounds, untranslated for the same reason"),
    ("NAVEL ROCK, BIRTH ISLAND",         "2.10: no player of this game can reach either"),
    ("CORPUS WAREHOUSE, USER TOWER",     "already ours, tier 1 and tier 0"),
]


def clean(name):
    """jsonproc's cleanString: the symbol is built out of the name's BYTES."""
    return re.sub(r"[^A-Za-z0-9]", "_", name)


def textwidth():
    import io, contextlib
    argv, sys.argv = sys.argv, ["port_vocab"]
    try:
        spec = importlib.util.spec_from_file_location("pv", os.path.join(HERE, "port_vocab.py"))
        pv = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                spec.loader.exec_module(pv)
            except SystemExit:
                pass
        return pv.textwidth
    finally:
        sys.argv = argv


def main():
    write = "--write" in sys.argv
    width = textwidth()
    doc = json.load(open(JSON))
    sections = doc["map_sections"]
    have = {m["name"]: m for m in sections if "name" in m}

    #  Vanilla's widest, measured. engine.md's rule: a demonstrated safe width.
    import subprocess
    r = subprocess.run(["git", "-C", GBA, "show",
                        "upstream/master:src/data/region_map/region_map_sections.json"],
                       capture_output=True, text=True)
    van = [m["name"] for m in json.loads(r.stdout)["map_sections"] if "name" in m] if r.returncode == 0 else []
    vanmax = max((width(n), n) for n in van) if van else (0, "?")

    print("  caps: %d characters (u8 mapName[19]), %dpx (unsigned centring in the popup)"
          % (CHAR_CAP, PIXEL_CAP))
    if van:
        print("  vanilla's widest of %d: %s at %dpx -- demonstrated safe, a floor not a ceiling"
              % (len(van), vanmax[1], vanmax[0]))

    changed, bad, already = [], [], 0
    for old, (new, why) in sorted(NAMED.items()):
        if new in have:
            already += 1
            continue
        if old not in have:
            bad.append("  !! %-16s is not in the table under that name -- vanilla moved, or a typo here" % old)
            continue
        px, ch = width(new), len(new)
        flag = ""
        if ch > CHAR_CAP:  flag = " !! %d characters, cap is %d" % (ch, CHAR_CAP)
        elif px > PIXEL_CAP: flag = " !! %dpx, cap is %d -- the popup would underflow" % (px, PIXEL_CAP)
        elif px > vanmax[0]: flag = " .. %dpx, past vanilla's widest -- look at it" % px
        if flag.startswith(" !!"):
            bad.append("  !! %-16s -> %-16s%s" % (old, new, flag))
            continue
        changed.append((old, new, why, px, ch, flag))

    for line in bad:
        print(line)
    print("  %d named, %d already ours, %d to write" % (len(NAMED), already, len(changed)))
    for old, new, why, px, ch, flag in changed:
        print("  %-16s -> %-16s %3dpx %2dch%s" % (old, new, px, ch, flag))
        print("  %-16s    %s" % ("", why))
    print("  kept, by rule:")
    for what, why in KEPT:
        print("    %-36s %s" % (what, why))
    if bad:
        print("  REFUSED: fix the lines above first; nothing was written.")
        return 1
    if not changed:
        print("  nothing to do.")
        return 0
    if not write:
        print("  (--write to apply)")
        return 0

    #  The JSON is the source; the seven headers under it are generated and
    #  gitignored, so writing anything else would exist in one build only.
    for old, new, why, px, ch, flag in changed:
        have[old]["name"] = new
    open(JSON, "w").write(json.dumps(doc, indent=2) + "\n")

    #  ...and the hand-written symbols. This is the trap: region_map.c names
    #  sMapsecName_* by hand and the generator derives them from the name.
    c = open(RMC).read()
    hits = 0
    for old, new, why, px, ch, flag in changed:
        a, b = "sMapsecName_" + clean(old), "sMapsecName_" + clean(new)
        n = c.count(a)
        if n:
            c = c.replace(a, b)
            hits += n
            print("  region_map.c: %s -> %s (%d)" % (a, b, n))
    open(RMC, "w").write(c)
    print("  written: %d names, %d hand-written symbols" % (len(changed), hits))

    #  And the prose that names these places. NAME TABLES ARE AUTHORED AND
    #  PROSE IS SWEPT, so the JSON above is written from the table and every
    #  other file is swept FROM it -- never the other way round, which is the
    #  bug that has cost this project five name tables.
    #
    #  A swept line can get WIDER than the box, and three of these names do
    #  grow, so every line that changes is re-measured. 196px is engine.md's,
    #  read off vanilla's own widest message-box line.
    swept, files, wide = 0, 0, []
    for dirpath, dirnames, filenames in os.walk(GBA):
        if any(s in dirpath for s in (os.sep + "build", os.sep + ".git",
                                      os.sep + "agbcc", os.sep + "tools")):
            continue
        for fn in filenames:
            if not fn.endswith((".inc", ".c", ".h", ".s")):
                continue
            p = os.path.join(dirpath, fn)
            if os.path.abspath(p) == os.path.abspath(RMC):
                continue
            src = open(p, encoding="utf-8", errors="ignore").read()
            out = src
            for old_n, new_n, why, px, ch, flag in changed:
                out = out.replace(old_n, new_n)
            if out == src:
                continue
            for line in out.split("\n"):
                m = re.match(r'\s*\.string "(.*)"', line)
                if not m or not any(n in line for _, n, _, _, _, _ in changed):
                    continue
                seg = re.sub(r'\\[nlp]|\$', "", m.group(1))
                if width(seg) > 196:
                    wide.append("  !! %dpx in %s: %s" % (width(seg), os.path.relpath(p, GBA), seg))
            swept += sum(src.count(o) for o, n, w, px, ch, f in changed)
            files += 1
            open(p, "w").write(out)
    print("  swept: %d references in %d files" % (swept, files))
    for line in wide:
        print(line)
    if wide:
        print("  ^ the sweep pushed a line past the 196px box. Re-break it by hand.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

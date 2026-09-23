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
import subprocess

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
    #  ~~ ALLOWED BEFORE THE ID. A closed ticket is struck through -- which is
    #  what this file's own rule requires and what this check exists to enforce
    #  -- and the first pattern could not see one. It missed T-41 silently the
    #  day it was closed, and only spoke up once T-43 existed to make the gap
    #  visible, because a gap at the TOP of the range is invisible to a check
    #  that derives its range from max(). The check that enforces "never
    #  deleted" was blind to the approved way of keeping it.
    #  ...and only BELOW the tables start. The preamble discusses tickets by id
    #  -- the section on why old tickets drift cites four of them in a table --
    #  and counting those as rows reported three duplicates that are prose.
    #  The ledger is everything from the first "## Ready" onward.
    doc = open(f, encoding="utf-8").read()
    cut = doc.find("## Ready")
    ids = re.findall(r"\|\s*~{0,2}\s*\*\*(T-(\d+))\*\*",
                     doc[cut:] if cut > 0 else doc)
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


#  Words the design WITHDREW, and which must never come back in anything a
#  player can read. This list exists because TAINT was withdrawn as a MARK
#  name in 5.2 -- "a second meaning the design did not choose is not a second
#  meaning; it is a leak" -- and was still the name of MOVE_POISON_STING four
#  months later, AND the punchline of a Viridian City line: "Mind the TAINT."
#
#  The ruling was made for one surface and never swept to the others, which is
#  the failure this whole tool exists to catch. A veto that is not enforced is
#  a preference.
#
#  Each entry carries what replaced it, so the message tells you what to write
#  instead of only what not to.
VETOED = {
    "TAINT":  ("TAMPER (routines) / SKEW (marks)",
               "withdrawn 5.2 for a well-known vulgar reading, in a game "
               "where you RECEIVE one"),
    "MANIAC": ("ARCHIVIST",
               "craft rule 3 -- name the process, not the pathology"),
}


def check_vetoed():
    """No player-visible string may contain a word the design withdrew.

    Scans the whole lexicon AND every line of map dialogue, because TAINT was
    living in both and the mark ruling had swept neither.

    Matched on word boundaries against the flattened text: an escape is two
    characters and the first is a letter, so `\nTAINT` puts `n` against `T`
    and a naive \b finds no boundary -- the trap that has now hidden
    substitutions in four separate tools.
    """
    out = []
    files = []
    for rel in ("src/data/text/move_names.h", "src/data/text/species_names.h",
                "src/data/text/abilities.h", "src/data/text/item_names.h",
                "src/data/text/trainer_class_names.h", "src/battle_main.c",
                "src/strings.c", "src/battle_message.c"):
        f = os.path.join(GBA, rel)
        if os.path.isfile(f):
            files.append((rel, f))
    maps = os.path.join(GBA, "data/maps")
    for root, _, fnames in os.walk(maps):
        for fn in fnames:
            if fn.endswith((".inc", ".pory")):
                f = os.path.join(root, fn)
                files.append((os.path.relpath(f, GBA), f))

    #  PLAYER-VISIBLE LITERALS ONLY. The first version matched whole files and
    #  reported nine hits, and every one was a CODE SYMBOL --
    #  OBJ_EVENT_GFX_POKE_MANIAC and TRAINER_CLASS_POKEMANIAC, whose displayed
    #  strings already read ARCHIVIST. Renaming a constant changes nothing a
    #  player sees and breaks the build; only the text matters. This is the
    #  same error port_states.py made the same week, which is twice.
    LITERAL = re.compile(r'_\("((?:[^"\\]|\\.)*)"\)|\.string\s+"((?:[^"\\]|\\.)*)"')

    for rel, f in files:
        try:
            raw = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for m in LITERAL.finditer(raw):
            #  flatten the escapes inside the literal -- an escape is two
            #  characters and the first is a letter, so \nTAINT puts n against
            #  T and a naive boundary match finds nothing
            text = re.sub(r"\\[nlpN]", " ", m.group(1) or m.group(2) or "")
            for word, (instead, why) in VETOED.items():
                #  case-INSENSITIVE: "I'm also a mushroom maniac" sat one line
                #  below "DAEMON MOVE MANIAC" and the first version read only
                #  the shouted one. A veto is on the word, not on its casing.
                if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % word, text, re.I):
                    line = raw.count("\n", 0, m.start()) + 1
                    out.append(("%s:%d" % (rel, line),
                                "%s -- use %s (%s)" % (word, instead, why)))
    return out


def read(rel, pat):
    f = os.path.join(GBA, rel)
    if not os.path.isfile(f):
        return []
    return re.findall(pat, open(f, encoding="utf-8", errors="ignore").read())


def check_story_freshness():
    """How far behind the bible each story document says it is.

    T-38: these two are prose with no build behind them, so no diff can tell
    you they have drifted -- story-readthrough.md was a whole act behind and
    nothing said so. The stale-NAME check above catches the objective half.
    This is the other half, and it is REPORTED RATHER THAN FAILED on purpose.

    A story document legitimately trails the bible by a few versions; failing
    a build for that is the crying-wolf failure this project has already had
    twice today. What is not legitimate is nobody knowing, so the number is
    printed every run whether it is zero or forty.
    """
    cl = os.path.join(DOCS, "CHANGELOG.md")
    if not os.path.isfile(cl):
        return []
    heads = re.findall(r"(?m)^## v(\d+(?:\.\d+)*)\s+—", open(cl, encoding="utf-8").read())
    if not heads:
        return []
    top_v = heads[0]
    out = []
    for rel in ("docs/story.md", "docs/story-readthrough.md"):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        m = re.search(r"Reconciled against the bible at v(\d+(?:\.\d+)+)",
                      open(p, encoding="utf-8", errors="ignore").read())
        if not m:
            out.append((rel, "carries no reconciled-against line"))
        elif m.group(1) != top_v:
            try:
                gap = vkey(top_v)[-1] - vkey(m.group(1))[-1]
                out.append((rel, "reconciled at v%s, bible is v%s -- %d behind"
                            % (m.group(1), top_v, gap)))
            except Exception:
                out.append((rel, "reconciled at v%s, bible is v%s"
                            % (m.group(1), top_v)))
    return out


def check_vanilla_index():
    """A renamed daemon whose Index entry is still Kanto's, word for word.

    T-40: PULSAR was found describing "a geometric body the locals suspect is
    an alien creature". port_index.py wrote the entries we HAD, and the ones we
    never wrote kept vanilla's -- so the game named 166 daemons and went on
    describing thirty of them as the creatures they replaced.

    THE COMPARISON HAS TO APPLY OUR VOCABULARY FIRST. The sweep turned POKeMON
    into DAEMON inside every entry, so a byte-for-byte diff against upstream
    says almost nothing is vanilla -- which is exactly what the first
    measurement of this ticket reported, and it was wrong by twenty.
    """
    import subprocess, importlib.util, io, contextlib
    bad = []
    names = os.path.join(GBA, "src/data/text/species_names.h")
    if not os.path.isfile(names):
        return bad
    argv, sys.argv = sys.argv, ["port_vocab"]
    try:
        s = importlib.util.spec_from_file_location(
            "pv", os.path.join(os.path.dirname(os.path.abspath(__file__)), "port_vocab.py"))
        pv = importlib.util.module_from_spec(s)
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                s.loader.exec_module(pv)
            except SystemExit:
                pass
    except Exception:
        return bad
    finally:
        sys.argv = argv
    if not hasattr(pv, "convert"):
        return bad
    pat = r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]+)"\)'
    def up(rel):
        r = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel],
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else ""
    ours = dict(re.findall(pat, open(names, encoding="utf-8").read()))
    van = dict(re.findall(pat, up("src/data/text/species_names.h")))
    renamed = {k for k in ours
               if van.get(k) and ours[k] != van[k] and ours[k] != "??????????"}
    if not renamed:
        return bad
    rx = r'const u8 g(\w+?)PokedexText\[\]\s*=\s*_\(\s*((?:"[^"]*"\s*)+)\)'
    flat = lambda b: re.sub(r"\s+", " ",
                            re.sub(r"\\[nlp]", " ",
                                   "".join(re.findall(r'"([^"]*)"', b)))).strip()
    norm = lambda s: re.sub(r"\W", "", s).upper()
    for rel in ("src/data/pokemon/pokedex_text_fr.h", "src/data/pokemon/pokedex_text_lg.h"):
        f = os.path.join(GBA, rel)
        vsrc = up(rel)
        if not os.path.isfile(f) or not vsrc:
            continue
        o = {norm(k): flat(b) for k, b in re.findall(rx, open(f, encoding="utf-8").read())}
        v = {norm(k): b for k, b in re.findall(rx, vsrc)}
        for k in sorted(renamed):
            key = norm(k)
            if key in o and key in v and o[key] == flat(pv.convert(v[key])):
                bad.append(("%s (%s)" % (ours[k], os.path.basename(rel)),
                            "Index entry is still %s's" % van[k]))
    return bad


def check_near_collisions(surfaces):
    """Two names where one is the other with a single character INSERTED.

    Found 2026-09-11. The SQUIRTLE line was CLUSTR from 2026-08-31; ten days
    later the Kanto sweep gave EXEGGCUTE the name CLUSTER. Two different
    strings, so "no word means two things" passed every run -- and on a party
    screen they are one word with a letter knocked out.

    INSERTION ONLY, and that is the whole design of this check. Edit distance
    1 in general reports twenty-three pairs here and every one is fine:
    LOCK/LICK, FLIP/FLAP, LATIAS/LATIOS, SWALLOW/SWELLOW -- substitutions make
    two words that look different. Stripping vowels is worse still and equates
    SCAN with SUICUNE.

    A name that is another name plus one letter is the case a reader cannot
    tell apart, and it is the only one worth failing a build over.
    """
    flat = []
    for kind, names in sorted(surfaces.items()):
        for n in names:
            if len(n) >= 4 and n != "??????????":
                flat.append((n.upper(), n, kind))
    by_len = {}
    for up, n, kind in flat:
        by_len.setdefault(len(up), []).append((up, n, kind))
    out = []
    for ln, rows in sorted(by_len.items()):
        for up, n, kind in rows:
            for up2, n2, kind2 in by_len.get(ln + 1, []):
                #  ...and the inserted letter must be a VOWEL. That is what
                #  separates a misspelling from two words: CLUSTR+E is CLUSTER
                #  and LABL+E is LABEL, while LOCK+B is BLOCK and MUTE+D is
                #  MUTED, which nobody has ever confused. Insertion alone still
                #  reported thirteen pairs and every one was fine.
                if any(up2[:i] + up2[i + 1:] == up and up2[i] in "AEIOU"
                       for i in range(len(up2))):
                    out.append(("%s / %s" % (n, n2),
                                "%s and %s -- one is the other with a vowel dropped"
                                % (kind, kind2)))
    return out


def check_phantom_places():
    """A place-shaped phrase in dialogue that NO map bears, built out of one of
    our own names.

    Found 2026-09-11 on ONE ISLAND. The map said MT. SMOULDER and every line of
    dialogue said MT. JITTER -- a name the game has never had anywhere. It got
    in because the move rename EMBER -> JITTER reached a PLACE months ago, and
    then T-23 named that mapsec something else entirely.

    THE EXISTING STALE-NAME CHECK CANNOT SEE THIS. It asks "does dialogue still
    say the VANILLA name", and MT. JITTER is neither vanilla nor ours. It is a
    third state, and it survived every check this project has because every
    check compares two columns and this is in neither.

    Narrow on purpose. Asking "is every place-shaped phrase a real mapsec"
    reports seventy things, nearly all of them fine -- CYCLING ROAD, PROOF HALL,
    eight kinds of DAEMON GYM. Requiring that the phrase contain one of OUR OWN
    renamed move or species names is the actual failure mode and reports only
    it: that is how both JITTER and TAPPOINT got into a place name.
    """
    import json, subprocess
    rel = "src/data/region_map/region_map_sections.json"
    f = os.path.join(GBA, rel)
    if not os.path.isfile(f):
        return []
    names = {m["name"] for m in json.load(open(f))["map_sections"] if m.get("name")}
    ours = set()
    for r, pat in (("src/data/text/move_names.h", r'\[MOVE_\w+\]\s*=\s*_\("([^"]+)"\)'),
                   ("src/data/text/species_names.h", r'\[SPECIES_\w+\]\s*=\s*_\("([^"]+)"\)')):
        p = os.path.join(GBA, r)
        if not os.path.isfile(p):
            continue
        v = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + r],
                           capture_output=True, text=True)
        if v.returncode != 0:
            continue
        o = re.findall(pat, open(p, encoding="utf-8", errors="ignore").read())
        van = re.findall(pat, v.stdout)
        ours |= {o[i] for i in range(min(len(o), len(van)))
                 if o[i] != van[i] and len(o[i]) > 3}
    if not ours:
        return []
    suf = ("SPA|CAVE|TOWER|ROAD|PATH|ISLE|ISLAND|TUNNEL|VALLEY|BRIDGE|BEACH"
           "|CANYON|RUINS|MANSION|FOREST|SPRING")
    pat = re.compile(r"\b(MT\. [A-Z][A-Z']+|(?:[A-Z][A-Z'.]+ ){1,2}(?:%s))\b" % suf)
    out = []
    #  T-243: every .inc with dialogue in it, not only the ones named text.inc -- the same blind spot as the stale-name
    #  pass below, which is where it did its damage.
    for root, dirs, files in os.walk(os.path.join(GBA, "data")):
        for fn in files:
            if not fn.endswith(".inc"):
                continue
            p = os.path.join(root, fn)
            txt = re.sub(r"\\[nlp]", " ",
                         open(p, encoding="utf-8", errors="ignore").read())
            for m in pat.finditer(txt):
                ph = re.sub(r"\s+", " ", m.group(1)).strip()
                if ph in names:
                    continue
                if set(re.split(r"[ .']+", ph)) & ours:
                    out.append((os.path.relpath(p, GBA),
                                "%s -- no map bears that name" % ph))
    return out


def check_conflict_markers():
    """No tracked file may contain a merge conflict marker.

    This is not hypothetical. docs/CHANGELOG.md carried `<<<<<<< HEAD`,
    `=======` and `>>>>>>> main` IN THE TREE, committed, for several releases
    -- and nobody noticed, because both sides of that merge were pure appends
    and the file still read correctly to a human. A diff showed nothing wrong
    because each side's text was fine; it took reading the whole file to find
    the three lines that belonged to neither.

    Cheap, and the only check here that would have caught it.
    """
    out = []
    r = subprocess.run(["git", "-C", ROOT, "ls-files"], capture_output=True, text=True)
    if r.returncode != 0:
        return out
    for rel in r.stdout.split("\n"):
        if not rel or rel.endswith((".pdf", ".png", ".gba", ".gbc", ".mid", ".wav")):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            lines = open(p, encoding="utf-8", errors="ignore").read().split("\n")
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if line.startswith(("<<<<<<< ", ">>>>>>> ")) or line.rstrip() == "=======":
                #  a bare ======= is a legitimate markdown rule, so it only
                #  counts when one of the real markers is in the same file
                if line.rstrip() == "=======" and not any(
                        l.startswith(("<<<<<<< ", ">>>>>>> ")) for l in lines):
                    continue
                out.append(("%s:%d" % (rel, i), line.strip()[:40]))
    return out


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

    THREE THINGS ADDED 2026-09-20, all found by one line of battle text.
    `sText_PkmnWrappedBy` still read "was WRAPPED by" months after WRAP became
    ENCLOSE, and this check could not see it for three separate reasons:

      * IT ONLY READ text.inc. battle_message.c, strings.c and the routine
        descriptions are C string literals, so every battle message in the game
        was outside the check. That is where the states and the routines are
        actually named, which makes it the surface that mattered most.
      * AN INFLECTED NAME IS STILL THE NAME. WRAPPED, CLAMPED, SKETCHED,
        STOCKPILED, ENDURED, SNATCHED, TRACED -- seven live ones, none visible
        to a pattern looking for WRAP. The suffix set is S/ES/D/ED/ING plus a
        DOUBLED FINAL CONSONANT, because WRAP -> WRAPPED is not WRAP + ED.
      * THE PAIRINGS WERE ZIPPED, NOT KEYED. `port_names.py` learned this the
        hard way and this function had the bug it was written to avoid: with
        types included, a positional zip read FIRE -> FLOW and STEEL ->
        ENTROPY, because vanilla's type array has holes ours does not. Keyed on
        the designator, an addition can no longer masquerade as a rename.

    ONE KNOWN BLIND SPOT, reported rather than hidden. When the inflected form
    is ITSELF a live name the hit is still printed, with a note -- because
    "{ATK} CLAMPED {DEF}!" is a problem either way: CLAMPED is the name of an
    ABILITY here, so the line reads as a name where a verb was meant. Silently
    skipping it is how it survived in the first place.

    NAME TABLES ARE NOT SWEPT, which is engine.md's trap 6. Only the PROSE
    surfaces in PROSE_C below are read. Pointing this at all of src/ reports 87
    lines, and the bulk are trainer_tower_sets.c nicknames and items.h data --
    name tables, where a vanilla word is an authored value and not a mistake.
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

    #  ITEMS too. They were missing until 2026-09-11 and four lines still
    #  offered the player a POKé DOLL, which is the DECOY. Items live in JSON
    #  rather than a header, so they need their own reader -- which is exactly
    #  why they were left out, and exactly why nothing noticed.
    import json as _json
    vj = upstream("src/data/items.json")
    f = os.path.join(GBA, "src/data/items.json")
    if vj and os.path.isfile(f):
        try:
            vo = {i["itemId"]: i.get("english") for i in _json.loads(vj)["items"]}
            oo = {i["itemId"]: i.get("english") for i in _json.load(open(f))["items"]}
            renamed.update({vo[k]: oo[k] for k in oo
                            if vo.get(k) and oo.get(k) and vo[k] != oo[k]})
        except Exception:
            pass

    #  KEYED ON THE DESIGNATOR, never zipped by position. A zip cannot tell an
    #  ADDITION from a RENAME -- the exact mistake port_names.py exists to
    #  avoid -- and it mispaired the type table outright: vanilla's array has
    #  holes ours does not, so position n is not the same type on both sides.
    for rel, pat in (("src/data/text/move_names.h",
                      r'\[(MOVE_\w+)\]\s*=\s*_\("([^"]+)"\)'),
                     ("src/data/text/species_names.h",
                      r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]+)"\)'),
                     ("src/data/text/abilities.h",
                      r'\[(ABILITY_\w+)\]\s*=\s*_\("([^"]+)"\)')):
        up = upstream(rel)
        f = os.path.join(GBA, rel)
        if not up or not os.path.isfile(f):
            continue
        ours = dict(re.findall(pat, open(f, encoding="utf-8", errors="ignore").read()))
        van = dict(re.findall(pat, up))
        renamed.update({v: ours[k] for k, v in van.items()
                        if k in ours and ours[k] != v})

    #  the live lexicon, so an old name that is now somebody else's name is
    #  never reported -- this is the GROWTH case and it is not hypothetical
    #  THE STATES BELONG IN HERE. 1.6 renamed CONFUSION to THRASHING, so a
    #  routine description reading "ends THRASHING" is correct -- and without
    #  the states in the live set the inflection pass reports every one of them
    #  as a leftover THRASH, which is four false alarms in one file. Abilities
    #  and trainer classes are here for the same reason.
    type_names = set()
    f = os.path.join(GBA, "src/battle_main.c")
    if os.path.isfile(f):
        type_names = set(re.findall(r'\[TYPE_\w+\]\s*=\s*_\("(\w+)"\)',
                                    open(f, encoding="utf-8", errors="ignore").read()))

    live = set(STATES)
    for rel, pat in (("src/data/text/move_names.h", r'_\("([^"]+)"\)'),
                     ("src/data/text/species_names.h", r'_\("([^"]+)"\)'),
                     ("src/data/text/abilities.h", r'_\("([^"]+)"\)'),
                     ("src/data/text/trainer_class_names.h", r'_\("([^"]+)"\)'),
                     ("src/battle_main.c", r'\[TYPE_\w+\]\s*=\s*_\("(\w+)"\)'),
                     ("src/data/region_map/region_map_entry_strings.h", r'_\("([^"]+)"\)')):
        f = os.path.join(GBA, rel)
        if os.path.isfile(f):
            live |= set(re.findall(pat, open(f, encoding="utf-8", errors="ignore").read()))
    renamed = {o: n for o, n in renamed.items()
               #  NOT o.isupper(). "POKé DOLL".isupper() is False, because é
               #  is not an uppercase character -- so the one item name in the
               #  game with an accent in it was invisible to this check on the
               #  very run that added items to it. The test is "contains no
               #  lowercase ASCII", which is what was meant all along.
               if o not in live and not re.search(r"[a-z]", o) and len(o) > 2
               #  and a renamed move whose old name is the interface's own verb (port_vocab's ORDINARY_WORDS):
               #  the storage system WITHDRAWs, and it is not the move EDDY (found 2026-09-23).
               and o not in ("WITHDRAW",)}

    #  AN INFLECTED NAME IS STILL THE NAME. Plain suffixes, plus a doubled
    #  final consonant, which is the one that hid WRAPPED: it is not WRAP + ED.
    #  A trailing vowel pair rules the doubling out (SEED -> SEEDDED is not a
    #  word), and the whole pattern is case-sensitive against an uppercase
    #  name, so lowercase prose -- "cut its own HP" -- never matches CUT.
    def inflected(old):
        alts = ["(?:S|ES|D|ED|ING)?"]
        if (re.search(r"[BCDFGKLMNPRSTVZ]$", old)
                and not re.search(r"[AEIOU][AEIOU][BCDFGKLMNPRSTVZ]$", old)):
            alts.insert(0, re.escape(old[-1]) + "(?:ED|ING)")
        return re.compile(r"(?<![A-Z])%s(%s)(?![A-Z])"
                          % (re.escape(old), "|".join(alts)))

    pats = {o: inflected(o) for o in renamed}

    #  WHICH LIVE WORDS MAY LEGITIMATELY BE WORN AS AN INFLECTION, and it is a
    #  short list: a STATE and a TYPE are adjectives the prose is SUPPOSED to
    #  use. "ends THRASHING" is a routine description doing its job, and 1.6
    #  renamed CONFUSION to THRASHING precisely so it could.
    #
    #  A SPECIES, ABILITY, ITEM or ROUTINE name is NOT in that class, and this
    #  is the distinction the first cut of this got wrong in both directions.
    #  Suppressing every live inflection hid "{ATK} CLAMPED {DEF}!" -- CLAMPED
    #  is the ABILITY BATTLE_ARMOR wears here, so that line reads as a name
    #  where a verb was meant, which is worse than the stale name alone.
    #  Suppressing none of them reported four correct THRASHINGs every run.
    adjectival = set(STATES) | set(type_names)

    def hit(s, old):
        """None, or how to describe the match -- "" plain, or a collision note."""
        m = pats[old].search(s)
        if not m:
            return None
        if m.group(1) and m.group(0) in adjectival:
            return None
        if m.group(1) and m.group(0) in live:
            return "; %s is itself a name here" % m.group(0)
        return " (as %s)" % m.group(0) if m.group(1) else ""

    out = []
    #  THE STORY DOCUMENTS TOO. They are prose with no build behind them, so
    #  nothing has ever checked them -- and story-readthrough.md was naming
    #  KINDLE ROAD, BOND BRIDGE and TREASURE BEACH a day after the islands were
    #  renamed. A markdown paragraph WRAPS, so the text is flattened before
    #  matching: "BOND\nBRIDGE" is one name, and the first scan of this missed
    #  exactly that one for exactly that reason.
    for rel in ("docs/story.md", "docs/story-readthrough.md"):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        prose = re.sub(r"\s+", " ", open(p, encoding="utf-8", errors="ignore").read())
        for old, new in renamed.items():
            note = hit(prose, old)
            if note is not None:
                out.append((rel, "says %s; the game calls it %s%s" % (old, new, note)))

    #  T-243: EVERY .inc WITH DIALOGUE IN IT, not only the ones named text.inc. data/text/ holds trainers.inc, the Fame
    #  Checker, the signs and a dozen more, and data/scripts/ the shared ones; this loop skipped all of them, which is
    #  how a Route 9 rematch still said ROCK TUNNEL two weeks after this docstring promised it could not.
    for root, dirs, files in os.walk(os.path.join(GBA, "data")):
        for fn in files:
            if not fn.endswith(".inc"):
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
                #  a control code is not prose. {PLAY_SE SE_BALL_BOUNCE_1}
                #  carries the word BOUNCE and means nothing by it, and so do
                #  {PLUS} and {EMOJI_MINUS} -- three false alarms, all of them
                #  a constant the player never reads.
                s = re.sub(r"\{[^}]*\}", " ",
                           re.sub(r"\\[nlp]", " ", "".join(parts)))
                for old, new in renamed.items():
                    note = hit(s, old)
                    if note is not None:
                        out.append(("%s:%d" % (os.path.relpath(p, GBA), start + 1),
                                    "says %s; the game calls it %s%s" % (old, new, note)))

    #  THE PROSE C SOURCES, which nothing read until 2026-09-20. Every battle
    #  message and every routine description is a C string literal, so the
    #  whole battle log was invisible here. This list is deliberately NOT all
    #  of src/: name tables hold vanilla words on purpose (engine.md trap 6),
    #  and sweeping them reports 87 lines of authored data.
    #  pokedex_text*.h, NOT pokedex_entries.h. The entries file is a name
    #  table wearing a prose file's extension: its strings are `.categoryName`,
    #  and sweeping it reported WRAPPING, ABSORBING, BITE, GUTS and WISH --
    #  every one an AUTHORED category, and eight more that were the word IRON
    #  in "IRON SNAKE". Trap 6 again, and it took reading the hits to see it.
    #  The _fr and _lg files are CONTENT's and CONTEXT's own dex text.
    PROSE_C = ("src/battle_message.c",
               "src/strings.c",
               "src/move_descriptions.c",
               "src/data/text/quest_log.h",
               "src/data/pokemon/pokedex_text.h",
               "src/data/pokemon/pokedex_text_fr.h",
               "src/data/pokemon/pokedex_text_lg.h")
    for rel in PROSE_C:
        p = os.path.join(GBA, rel)
        if not os.path.isfile(p):
            continue
        for i, line in enumerate(
                open(p, encoding="utf-8", errors="ignore").read().split("\n"), 1):
            #  gExpandedPlaceholder_Sapphire is the literal word SAPPHIRE,
            #  standing for the RSE cartridge in link text -- not ITEM_SAPPHIRE,
            #  which is the PRIVATE KEY. Eight of these, all version and team
            #  names, none of them a reference to anything we renamed.
            if "gExpandedPlaceholder_" in line:
                continue
            m = re.search(r'_\("(.*)"\)', line)
            if not m:
                continue
            s = re.sub(r"\{[^}]*\}", " ", re.sub(r"\\[nlp]", " ", m.group(1)))
            for old, new in renamed.items():
                note = hit(s, old)
                if note is not None:
                    out.append(("%s:%d" % (rel, i),
                                "says %s; the game calls it %s%s" % (old, new, note)))

    #  T-244: two more prose surfaces that live beside name tables. ABILITY DESCRIPTIONS share abilities.h with the
    #  ability names, so only the s*Description lines are read -- PLUS's said "Powers up with MINUS." months after
    #  MINUS became SINK. And ITEM DESCRIPTIONS live in items.json, which this pass read for its NAMES and never for
    #  what the items say: the AURORATICKET was still bound for BIRTH ISLAND. The TOOLKIT's are skipped -- nothing
    #  prints them (engine.md trap 27).
    rel = "src/data/text/abilities.h"
    p = os.path.join(GBA, rel)
    if os.path.isfile(p):
        for i, line in enumerate(open(p, encoding="utf-8", errors="ignore").read().split("\n"), 1):
            m = re.search(r'static const u8 s\w+Description\[\] = _\("(.*)"\)', line)
            if not m:
                continue
            for old, new in renamed.items():
                note = hit(m.group(1), old)
                if note is not None:
                    out.append(("%s:%d" % (rel, i), "says %s; the game calls it %s%s" % (old, new, note)))
    p = os.path.join(GBA, "src/data/items.json")
    if os.path.isfile(p):
        for it in json.load(open(p, encoding="utf-8"))["items"]:
            if it.get("pocket") == "POCKET_TM_CASE":
                continue
            d = re.sub(r"\{[^}]*\}", " ", re.sub(r"\\[nlp]", " ", it.get("description_english", "")))
            for old, new in renamed.items():
                note = hit(d, old)
                if note is not None:
                    out.append(("items.json %s" % it["itemId"], "says %s; the game calls it %s%s" % (old, new, note)))
    return out


def check_type_copy():
    """T-173. `battle_message.c` keeps a SECOND copy of the type names -- eighteen strings of the form
    "a VECTOR routine", read whenever a routine's type is said aloud -- and nothing compared the two. Sixteen sat
    at vanilla's words for months and one said CONSTRUE, which is the trainer class and the CONTEXT routine, not
    the type. A copy nobody checks is how the battle log came to name a type that exists nowhere else in the game.
    """
    names = dict(read("src/battle_main.c", r'\[TYPE_(\w+)\] = _\("([^"]*)"\)'))
    msg = open(os.path.join(GBA, "src/battle_message.c"), encoding="utf-8", errors="ignore").read()
    tab = dict(re.findall(r"\[TYPE_(\w+)\]\s*=\s*(gText_\w+),?", msg))
    strs = dict(re.findall(r'const u8 (gText_\w+Move)\[\] = _\("([^"]*)"\)', msg))
    out = []
    for t, sym in sorted(tab.items()):
        want = names.get(t)
        if not want:
            continue
        article = "an" if want[0] in "AEIOU" else "a"
        if strs.get(sym) != "%s %s routine" % (article, want):
            out.append(("TYPE_" + t, "%r, and gTypeNames says %s" % (strs.get(sym), want)))
    return out


#  T-181 and T-197 were both "a pane was measured once and then nothing watched it". The move descriptions
#  sat 53 lines past vanilla's widest for weeks because the only thing that could tell was a screen, and the
#  margins are wrapped by a tool that could be edited by hand tomorrow. Two panes, both DEMONSTRATED rather
#  than declared -- the entry pane is what the 386 entries already use -- so this cannot drift out of step
#  with the game the way a typed-in number would.
def check_panes():
    import re as _re

    gba = os.path.join(ROOT, "engineGba")
    src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
    ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
    exec(compile(src.split("# ------------------------------------------------------- names, derived")[0],
                 "port_vocab.py", "exec"), ns)
    width = ns["textwidth"]
    bad = []

    #  the summary screen's move pane: POKESUM_WIN_TRAINER_MEMO is fifteen tiles with the text inset seven.
    txt = open(os.path.join(gba, "src/move_descriptions.c"), encoding="utf-8").read()
    for m in _re.finditer(r'const u8 gMoveDescription_(\w+)\[\] = _\((.*?)\);', txt, _re.S):
        body = "".join(_re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
        lines = body.split("\\n")
        if len(lines) > 4:
            bad.append((m.group(1), "%d lines in the routine pane's four" % len(lines)))
        for line in lines:
            if width(line) > 113:
                bad.append(("%s (%dpx)" % (m.group(1), width(line)), "past the 113px routine pane"))

    #  the summary's ability line: StringCopy'd into abilityDescStrBuf[52], so a description past 51 bytes writes
    #  over whatever follows it and says nothing, and then printed at x=2 in a 29-tile window (230px). Ours reach
    #  33 bytes and 175px (measured T-239); vanilla stopped at 28 and 154.
    abil = open(os.path.join(gba, "src/data/text/abilities.h"), encoding="utf-8").read()
    for m in _re.finditer(r'static const u8 (s\w+Description)\[\] = _\("([^"]*)"\);', abil):
        size = len(_re.findall(r'\\.|\{[^}]*\}|.', m.group(2))) + 1
        if size > 52:
            bad.append((m.group(1), "%d bytes, and the summary copies it into 52" % size))
        if width(m.group(2)) > 230:
            bad.append(("%s (%dpx)" % (m.group(1), width(m.group(2))), "past the 230px ability pane"))

    #  and OPUS's margins, against the pane the 386 Index entries demonstrate
    entries = open(os.path.join(gba, "src/data/pokemon/pokedex_text_fr.h"), encoding="utf-8").read()
    widest = 0
    for m in _re.finditer(r'const u8 g\w+PokedexText\[\] = _\((.*?)\);', entries, _re.S):
        body = "".join(_re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1)))
        for line in body.split("\\n"):
            widest = max(widest, width(line))
    margins = os.path.join(gba, "src/data/opus_margins.h")
    if os.path.exists(margins) and widest:
        txt = open(margins, encoding="utf-8").read()
        for m in _re.finditer(r'static const u8 (sOpusMargin_\w+)\[\] = _\("([^"]*)"\);', txt):
            for line in m.group(2).split("\\n"):
                if width(line) > widest:
                    bad.append(("%s (%dpx)" % (m.group(1), width(line)),
                                "past the %dpx the entries themselves use" % widest))

    #  The TOOLKIT does NOT print this text (T-239, engine.md trap 27): vanilla's items.json.txt points every
    #  TOOLKIT item at its routine's description, which the routine check above already holds -- to 113px and
    #  four lines, tighter than the TOOLKIT's own 18-tile pane. A PLUGIN's description_english is port_plugin_text's
    #  mirror of that, and is measured below only so the json stays a truthful copy.
    import json as _json
    items = _json.load(open(os.path.join(gba, "src/data/items.json"), encoding="utf-8"))
    #  T-238: and every OTHER item, in the bag's pane, which is the same 198px. This check looked only at the
    #  discs, so the TOOLKIT's own first line ran 221px from T-198 on and the bag cut it at "DRIVE".
    for it in (items["items"] if isinstance(items, dict) else items):
        name = it.get("english", "")
        lines = _re.split(r"\\[npl]", it.get("description_english", ""))
        if len(lines) > 3:
            bad.append((name, "%d lines in the pane's three" % len(lines)))
        for line in lines:
            if width(line.rstrip()) > 198:
                bad.append(("%s (%dpx)" % (name, width(line.rstrip())), "past the 198px vanilla puts in that pane"))
    return bad



#  T-208 pointed 29 ground pickups at the disc by walking every map.json, which is the right way to do it
#  once and no way at all to keep it true. A pickup added later, or an item changed from a potion to a
#  PLUGIN, goes back to looking like a potion and nothing says so.
def check_disc():
    import glob as _glob, json as _json, re as _re

    bad = []
    for f in sorted(_glob.glob(os.path.join(ROOT, "engineGba/data/maps/*/map.json"))):
        try:
            d = _json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        name = os.path.basename(os.path.dirname(f))
        for o in d.get("object_events", []):
            script = str(o.get("script", ""))
            gfx = o.get("graphics_id")
            plugin = bool(_re.search(r"Item(TM|HM)\d", script))
            if plugin and gfx == "OBJ_EVENT_GFX_ITEM_BALL":
                bad.append(("%s" % script, "holds a PLUGIN or DRIVER and shows a ball"))
            elif not plugin and gfx == "OBJ_EVENT_GFX_PLUGIN_DISC":
                bad.append(("%s" % script, "shows a disc and holds neither"))
    return bad


def check_plugin_colours():
    """Two things about the PLUGIN disc, which is the one screen that teaches colour-to-type.

    Every PLUGIN and DRIVER shares one drawing and is told apart only by its palette, so the TOOLKIT shows
    the player eighteen hues beside eighteen type names -- vision.md 9.4's claim, made legible, whether or
    not we meant it. It teaches whatever it is coloured with, so both halves have to hold: the HUE has to be
    ours (it was vanilla's until T-211), and each disc has to carry the type of the routine ACTUALLY on it.
    """
    import glob as _glob, importlib.util as _il, re as _re

    spec = _il.spec_from_file_location("genplugincolours", os.path.join(ROOT, "tools/genplugincolours.py"))
    gp = _il.module_from_spec(spec)
    spec.loader.exec_module(gp)
    colours = gp.type_colours()

    bad = []
    for stem, t in sorted(gp.FILES.items()):
        f = os.path.join(gp.PALDIR, "%s_tm_hm.pal" % stem)
        if not os.path.exists(f) or t not in colours:
            continue
        rows = [l for l in open(f, encoding="utf-8").read().splitlines()[3:] if l.strip()]
        want = ["%d %d %d" % c for c in gp.ramp(colours[t])]
        got = rows[gp.FIRST:gp.LAST + 1]
        if got != want:
            bad.append(("%s_tm_hm.pal" % stem, "is not %s's colour; re-run tools/genplugincolours.py --write" % t))

    pm = open(os.path.join(ROOT, "engineGba/src/data/party_menu.h"), encoding="utf-8").read()
    blk = _re.search(r"static const u16 sTMHMMoves\[\] =\s*\{(.*?)\n\};", pm, _re.S)
    bm = open(os.path.join(ROOT, "engineGba/src/data/battle_moves.h"), encoding="utf-8").read()
    it = open(os.path.join(ROOT, "engineGba/src/data/item_icon_table.h"), encoding="utf-8").read()
    if blk:
        moves = _re.findall(r"\b(MOVE_\w+)", blk.group(1))
        types = dict(_re.findall(r"\[(MOVE_\w+)\]\s*=\s*\{.*?\.type\s*=\s*TYPE_(\w+)", bm, _re.S))
        pal = dict(_re.findall(r"\[(ITEM_(?:TM|HM)\d+)\]\s*=\s*\{gItemIcon_TMHM,\s*gItemIconPalette_(\w+)TMHM\}", it))
        for i, m in enumerate(moves):
            item = "ITEM_TM%02d" % (i + 1) if i < 50 else "ITEM_HM%02d" % (i - 49)
            want, got = types.get(m, "?"), pal.get(item, "?").upper()
            if want != got:
                bad.append((item, "holds a %s routine and is coloured %s" % (want, got)))
    return bad


def check_numbered():
    """Two traps found on 2026-09-22, kept shut.

    1. The PATCH -> PLUGIN re-sweep ran on words, and `PATCH39` is one token with no word boundary inside it,
       so all 25 numbered ones survived in dialogue -- every gym leader handing over a "PATCH". Nothing a
       player reads may carry a numbered PATCH, TM or HM.
    2. A NOTEBOOK entry is copied into gStringVar4 to be shown, and gStringVar4 is 1000 bytes. An entry that
       outgrows it overwrites whatever follows it in EWRAM, silently.
    """
    import re as _re
    bad = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "engineGba/data")):
        for f in fn:
            if not f.endswith(".inc"):
                continue
            for line in open(os.path.join(dp, f), encoding="utf-8", errors="ignore"):
                if ".string" in line:
                    m = _re.search(r"\b(PATCH\d+|TM\d\d|HM\d\d)", line)
                    if m:
                        bad.append(("%s" % os.path.basename(dp), "says %s" % m.group(1)))
    #  T-223: the books are full screen and REFLOW their text (book_reader.c), so what must fit is a number of
    #  LINES, not bytes. A topic prints across one spread -- 7 lines on the left page, 9 on the right, 94px
    #  wide -- and a line past that is simply not drawn. A NOTEBOOK entry pages, but holds at most 47 lines at
    #  196px. Both are measured by the same wrap the game does, from the tables the game reads.
    src_pv = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
    ns_pv = {"__name__": "pv", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
    exec(compile(src_pv.split("# ------------------------------------------------------- names, derived")[0], "port_vocab.py", "exec"), ns_pv)
    tw = ns_pv["textwidth"]

    def reflow(body, width):
        lines, cur = 0, 0
        for para in _re.split(r"\\p", body):
            words = [w for w in _re.split(r"\\[nl]| ", para) if w]
            if not words:
                continue
            cur = 0
            lines += 1
            for w in words:
                ww = tw(w)
                if cur and cur + tw(" ") + ww > width:
                    lines += 1
                    cur = ww
                else:
                    cur = cur + (tw(" ") if cur else 0) + ww
        return lines

    texts = {}
    for dp, dn, fn in os.walk(os.path.join(ROOT, "engineGba/data/maps")):
        for f in fn:
            if f == "text.inc":
                t = open(os.path.join(dp, f), encoding="utf-8").read()
                for m in _re.finditer(r"^(\w+)::\n((?:\s+\.string \".*\"\n)+)", t, _re.M):
                    texts[m.group(1)] = "".join(_re.findall(r'\.string "(.*)"', m.group(2))).replace("$", "")
    br = os.path.join(ROOT, "engineGba/src/book_reader.c")
    brsrc = open(br, encoding="utf-8").read() if os.path.exists(br) else ""
    blk = _re.search(r"sTopics\[TB_CHAPTERS \+ 1\]\[TB_TOPICS\] =\s*\{(.*?)\n\};", brsrc, _re.S)
    if blk:
        for row in _re.finditer(r"\[(\d)\] = \{(.*?)\}", blk.group(1)):
            for lab in [x.strip() for x in row.group(2).split(",")]:
                head, _, body = texts.get(lab, "").partition("\\p")
                n = reflow(body, 94)
                if n > 16:
                    bad.append((lab, "%d lines, and a TEXTBOOK spread holds 16" % n))
                if tw(head) > 94:
                    bad.append((lab, "heading %dpx, and a page is 94" % tw(head)))
    nbsrc = open(os.path.join(ROOT, "engineGba/src/notebook.c"), encoding="utf-8").read()
    #  T-224: and the documents tools/gbadocs.py has placed, whose words are generated into their own header.
    docs_h = os.path.join(ROOT, "engineGba/src/data/notebook_documents.h")
    if os.path.exists(docs_h):
        nbsrc += open(docs_h, encoding="utf-8").read()
    for m in _re.finditer(r"static const u8 (s(?:Doc)?Text_\w+)\[\] = _\((.*?)\);", nbsrc, _re.S):
        body = "".join(_re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
        if reflow(body, 196) > 47:
            bad.append((m.group(1), "%d lines, and the NOTEBOOK holds 47" % reflow(body, 196)))
    #  T-224: and the entries that are a MAP's own text -- the syllabi, the Mansion's logs, the lab's signs. They are
    #  filed by name from sEntries, so every name there that is not a local sText_ is read from the maps' text.inc.
    blkE = _re.search(r"static const struct NotebookEntry sEntries\[\] =\s*\{(.*?)\n\};", nbsrc, _re.S)
    if blkE:
        for row in _re.finditer(r"\{ NB_\w+,\s*NB_KIND_TEXT,\s*\d+,[^}]*?,\s*(\w+)\s*\}", blkE.group(1)):
            lab = row.group(1)
            if lab.startswith("sText_"):
                continue
            if lab not in texts:
                bad.append((lab, "is filed in the NOTEBOOK and no map's text.inc defines it"))
            elif reflow(texts[lab], 196) > 47:
                bad.append((lab, "%d lines, and the NOTEBOOK holds 47" % reflow(texts[lab], 196)))
    #  T-219: and the exam paper's own panes -- a title beside its answer letter, a question, an option.
    ex = os.path.join(ROOT, "engineGba/src/school_exam.c")
    if os.path.exists(ex):
        src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
        ns = {"__name__": "pv", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
        exec(compile(src.split("# ------------------------------------------------------- names, derived")[0], "port_vocab.py", "exec"), ns)
        width = ns["textwidth"]
        limit = {"T": 170, "Q": 222, "O": 196}
        for m in _re.finditer(r'static const u8 s(\w+?)_(T|Q|O)(\d+)(?:_\d)?\[\] = _\("(.*?)"\);', open(ex, encoding="utf-8").read()):
            for line in m.group(4).split("\\n"):
                if width(line) > limit[m.group(2)]:
                    bad.append(("%s %s%s" % (m.group(1), m.group(2), m.group(3)), "%dpx on the paper, past %d" % (width(line), limit[m.group(2)])))
    nb = os.path.join(ROOT, "engineGba/src/notebook.c")
    if os.path.exists(nb):
        src = open(nb, encoding="utf-8").read()
        dh = os.path.join(ROOT, "engineGba/src/data/notebook_documents.h")
        if os.path.exists(dh):
            src += open(dh, encoding="utf-8").read()
        for m in _re.finditer(r"static const u8 (s(?:Doc)?Text_\w+)\[\] = _\((.*?)\);", src, _re.S):
            body = "".join(_re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
            size = len(_re.sub(r"\\[pnl]", "x", body)) + 1
            if size >= 1000:
                bad.append((m.group(1), "%d bytes, and gStringVar4 holds 1000" % size))
    return bad


#  T-240: a .string that ends without \n, \l, \p or $ runs straight into the next one. VERA's "It was only" met
#  "tired." after an #endif and the player read "onlytired" -- since 9f9544aa8, and not one width check or name
#  check could see it, because each line alone was fine. Vanilla has none, so the rule is: none. Each side of an
#  #ifdef is read as its own path, because that is where this one hid.
def check_joins():
    import glob as _glob
    bad = []
    files = sorted(_glob.glob(os.path.join(GBA, "data/maps/*/text.inc")) + _glob.glob(os.path.join(GBA, "data/text/*.inc"))
                   + _glob.glob(os.path.join(GBA, "data/scripts/*.inc")))
    for f in files:
        lines = open(f, encoding="utf-8", errors="ignore").read().split("\n")
        for which in (0, 1):
            label, seq, branch = None, [], None
            for line in lines + ["END::"]:
                s = line.strip()
                m = re.match(r"^(\w+)::?$", s)
                if m:
                    for a, b in zip(seq, seq[1:]):
                        if a is None or b is None or re.search(r"(\\[nlp]|\$)$", a) or a.endswith(" ") or b.startswith(" "):
                            continue
                        if re.search(r"[A-Za-z0-9.,!?\u2026'\"\u201d]$", a) and re.match(r"[A-Za-z0-9\u201c\"]", b):
                            bad.append(("%s %s" % (os.path.relpath(f, GBA), label), "...%s|%s..." % (a[-24:], b[:16])))
                    label, seq = m.group(1), []
                    continue
                if s.startswith("#if"):
                    branch = 0
                elif s.startswith("#else"):
                    branch = 1
                elif s.startswith("#endif"):
                    branch = None
                elif branch is None or branch == which:
                    mm = re.match(r'\.string\s+"(.*)"$', s)
                    if mm and label:
                        seq.append(mm.group(1))
                    elif label and s and not s.startswith("@"):
                        seq.append(None)
    return sorted(set(bad))


#  T-240, the other half: nothing measured a line of dialogue against the box it is read in. The field message box
#  is 26 tiles (new_menu_helpers.c), 208px. Music and colour codes draw nothing; {PLAYER} and {RIVAL} are counted
#  at seven wide letters; a {STR_VAR} at textwidth's own guess. A line vanilla ships word for word is its problem,
#  not ours -- two of those are over by that guess, and both hold a number. The panes with their own widths
#  (help, the intro, the Fame Checker, the STREAM, the Index, the quest log) are measured elsewhere or not here.
def check_message_box():
    import glob as _glob
    tw = _load_textwidth()
    def clean(l):
        l = re.sub(r"\{(PLAYER|RIVAL)\}", "WWWWWWW", l)
        l = re.sub(r"\{(PLAY_BGM|PLAY_SE|PAUSE|PAUSE_MUSIC|RESUME_MUSIC|COLOR|SHADOW|FONT_\w+|HIGHLIGHT|CLEAR_TO|PAUSE_UNTIL_PRESS)[^}]*\}", "", l)
        return re.sub(r"\{(MUS|SE)_\w+\}", "", l)
    skip = ("help_system", "new_game_intro", "fame_checker", "teachy", "pokedex", "quest_log")
    bad = []
    for f in sorted(_glob.glob(os.path.join(GBA, "data/maps/*/text.inc")) + _glob.glob(os.path.join(GBA, "data/text/*.inc"))
                    + _glob.glob(os.path.join(GBA, "data/scripts/*.inc"))):
        if any(x in f for x in skip):
            continue
        rel = os.path.relpath(f, GBA)
        up = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel], capture_output=True, text=True).stdout
        label = None
        for line in open(f, encoding="utf-8", errors="ignore").read().split("\n"):
            m = re.match(r"^(\w+)::", line)
            if m:
                label = m.group(1)
                continue
            st = re.match(r'\s*\.string\s+"(.*)"', line)
            if not st:
                continue
            for piece in re.split(r"\\[nlp]", st.group(1).replace("$", "")):
                if piece and tw(clean(piece)) > 208 and piece not in up:
                    bad.append(("%s %s" % (rel, label), "%dpx in the 208px box: %s" % (tw(clean(piece)), piece)))
    return bad


def _load_textwidth():
    src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
    ns = {"__name__": "pv", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
    exec(compile(src.split("# ------------------------------------------------------- names, derived")[0], "port_vocab.py", "exec"), ns)
    return ns["textwidth"]


#  T-241: a word said twice, with a line break between -- "by way of the\l THE BLACKOUT." ROCK TUNNEL took the name
#  THE BLACKOUT and vanilla's "the" in front of it survived, on its own line where no one-line check looks. Read with
#  every break flattened to a space. Deliberate ones are named here; a doubling vanilla already had is vanilla's.
DOUBLED_ON_PURPOSE = {
    "PokemonMansion_B1F_Text_MewtwoIsFarTooPowerful",   # the glitch counting in binary
    "ViridianCity_School_Text_Spelling_Board",          # a board's title, then its first word
}


def check_doubled():
    import glob as _glob
    def blocks(text):
        out, label, buf = {}, None, []
        for line in text.split("\n") + ["END::"]:
            m = re.match(r"^(\w+)::?\s*$", line.strip())
            if m:
                if label:
                    out[label] = " ".join(buf)
                label, buf = m.group(1), []
                continue
            st = re.match(r'\s*\.string\s+"(.*)"', line)
            if st and label:
                buf.append(st.group(1))
        return out
    def doubles(body):
        flat = re.sub(r"\{[^}]*\}", "", re.sub(r"\\[nlp]", " ", body)).replace("$", "")
        return {" ".join(m.group(0).lower().split()) for m in re.finditer(r"\b([A-Za-z]+)\s+\1\b", flat, re.I)}
    bad = []
    files = sorted(_glob.glob(os.path.join(GBA, "data/maps/*/text.inc")) + _glob.glob(os.path.join(GBA, "data/text/*.inc"))
                   + _glob.glob(os.path.join(GBA, "data/scripts/*.inc")))
    for f in files:
        rel = os.path.relpath(f, GBA)
        up = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel], capture_output=True, text=True).stdout
        seen = set().union(*[doubles(b) for b in blocks(up).values()]) if up else set()
        for label, body in blocks(open(f, encoding="utf-8", errors="ignore").read()).items():
            if label in DOUBLED_ON_PURPOSE:
                continue
            for d in sorted(doubles(body) - seen):
                bad.append(("%s %s" % (rel, label), '"%s"' % d))
    return bad


#  Invariant 3 (CLAUDE.md, 8.4): the type chart is byte-identical across both editions -- it is the argument,
#  and an argument that changes by cartridge is not one. Nothing watched it on the GBA (2026-09-23). It holds
#  today because both editions compile ONE table; the way it would break is an edition #if inside that table,
#  so the source half looks for exactly that, and the ROM half compares the two built charts when both exist.
def check_one_chart():
    out = []
    src = open(os.path.join(GBA, "src/battle_main.c"), encoding="utf-8", errors="ignore").read()
    for name in ("gTypeEffectiveness", "gTypeNames"):
        m = re.search(r"const u8 %s\[[^\]]*\](?:\[[^\]]*\])? =\s*\{(.*?)\n\};" % name, src, re.S)
        if not m:
            out.append((name, "not found in src/battle_main.c -- the check cannot see the chart"))
        elif re.search(r"^\s*#\s*if|FIRERED|LEAFGREEN|GAME_VERSION", m.group(1), re.M):
            out.append((name, "has an edition conditional inside it"))
    roms = [(os.path.join(GBA, "%s.elf" % n), os.path.join(GBA, "%s.gba" % n)) for n in ("daemonsContent", "daemonsContext")]
    if all(os.path.exists(e) and os.path.exists(g) for e, g in roms):
        tables = []
        for elf, gba in roms:
            try:
                nm = subprocess.run(["arm-none-eabi-nm", "-S", elf], capture_output=True, text=True).stdout
            except OSError:
                return out
            rom, got = open(gba, "rb").read(), {}
            for line in nm.splitlines():
                f = line.split()
                if len(f) == 4 and f[3] in ("gTypeEffectiveness", "gTypeNames"):
                    a, n = int(f[0], 16) - 0x08000000, int(f[1], 16)
                    got[f[3]] = rom[a:a + n]
            tables.append(got)
        for name in ("gTypeEffectiveness", "gTypeNames"):
            if tables[0].get(name) != tables[1].get(name):
                out.append((name, "differs between daemonsContent.gba and daemonsContext.gba"))
    return out


#  Flags and vars are plain numbers, and two names on one number fail SILENTLY: the second setflag answers the
#  first's goto_if_set. This project has added forty-one flags and thirty vars by hand (eleven for T-224's
#  documents alone, and twenty-four documents still to come), so every name we added is checked against every
#  other name for its number, and every hidden item for its own flag (2026-09-23; clean when written).
def check_ids():
    out = []
    for hdr, prefix in (("include/constants/flags.h", "FLAG_"), ("include/constants/vars.h", "VAR_")):
        ours = open(os.path.join(GBA, hdr)).read()
        up = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + hdr], capture_output=True, text=True).stdout
        if not up:
            continue
        defs = dict(re.findall(r"^#define\s+(%s\w+|\w+_START)\s+\(?([^/\n]+?)\)?\s*(?://.*)?$" % prefix, ours, re.M))
        def val(n, depth=0):
            v = defs.get(n)
            if v is None or depth > 8:
                return None
            v = v.strip()
            try:
                return int(v, 0)
            except ValueError:
                pass
            m = re.match(r"(\w+)\s*\+\s*(\w+)$", v)
            if m:
                a, b = (int(x, 0) if re.match(r"(0x[0-9a-fA-F]+|\d+)$", x) else val(x, depth + 1) for x in m.groups())
                return None if a is None or b is None else a + b
            return val(v, depth + 1)
        theirs = set(re.findall(r"^#define\s+(%s\w+)" % prefix, up, re.M))
        seen = {}
        for n in defs:
            if not n.startswith(prefix):
                continue
            v = val(n)
            if v is not None:
                seen.setdefault(v, []).append(n)
        for v, names in seen.items():
            if len(names) > 1 and any(n not in theirs for n in names):
                out.append((hex(v), " and ".join(names)))
    flags = {}
    for f in sorted(os.listdir(os.path.join(GBA, "data/maps"))):
        path = os.path.join(GBA, "data/maps", f, "map.json")
        if not os.path.exists(path):
            continue
        for b in json.load(open(path)).get("bg_events") or []:
            if b.get("type") == "hidden_item":
                flags.setdefault(b["flag"], []).append("%s (%d,%d)" % (f, b["x"], b["y"]))
    for flag, where in flags.items():
        if len(where) > 1:
            out.append((flag, "hidden in %s" % ", ".join(where)))
    return out


#  A rename changes the word after "a" or "an" and nothing changes the article. ENCORE became REPLAY and the
#  battle said "got an REPLAY!"; the POKe FLUTE became INTERRUPT and Lavender said "received a INTERRUPT" --
#  both for two weeks (found 2026-09-23). Escapes are flattened first: in "got\\nan" the n of the escape sits
#  against the article and no word boundary exists, which is CLAUDE.md's escape trap and what hid the first one.
#  Initialisms are read letter by letter (an HP, an S.S. TICKET), and a U that says "you" takes "a" (a USER).
ARTICLE_LETTERS = {"HP", "MP", "RPG", "NPC", "HM", "SOS", "FM", "X", "L", "R", "S.S.", "S.S", "MRI", "LCD"}
def check_articles():
    import glob
    out = []
    pats = ["src/*.c", "data/text/*.inc", "data/maps/*/text.inc", "data/scripts/*.inc", "src/data/text/*.h", "src/data/*.h"]
    for pat in pats:
        for f in sorted(glob.glob(os.path.join(GBA, pat))):
            src = open(f, encoding="utf-8", errors="ignore").read()
            #  T-242: and across a break. A line that ends "a" and a line that begins with the name are one phrase to the
            #  player, so a break and the quote-newline-.string that follows it read as one space. Each join is marked
            #  \x01 in place of the newline it swallows, so a line number still counts both.
            joined = re.sub(r'\\[nlp]"[ \t]*\n[ \t]*(?:\.string[ \t]+)?"', " \x01", src)
            for line_start, line in _lines_with_offsets(joined):
                if '"' not in line:
                    continue
                flat = re.sub(r"\\[nlp]", " ", line).replace("\x01", "")
                for m in re.finditer(r"\b([Aa]n?) (?:\{[A-Z_0-9 ]+\})?([A-Z][A-Z.]+)\b", flat):
                    art, word = m.group(1).lower(), m.group(2)
                    if word in ARTICLE_LETTERS or len(word) < 2:
                        continue
                    #  U is a vowel unless it is said "you": a USER, a UNION -- but an UPTIME (T-242: "a UPTIME" shipped,
                    #  because this line used to call every U a consonant).
                    you = word.startswith(("USE", "USU", "UNI", "UTI", "URA", "URI", "UBI", "UFO", "UKU"))
                    vowel = word[0] in "AEIO" or (word[0] == "U" and not you) or word.startswith("HONEST") or word.startswith("HOUR")
                    if (art == "an") != vowel:
                        n = joined[:line_start].count("\n") + joined[:line_start].count("\x01") + 1
                        out.append(("%s:%d" % (os.path.relpath(f, GBA), n), "%s %s" % (m.group(1), word)))
    return out


def _lines_with_offsets(text):
    pos = 0
    for line in text.split("\n"):
        yield pos, line
        pos += len(line) + 1


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
            seen.setdefault(w, []).append(label)

    #  A LIST, not a set: two entries in the SAME table wearing one word is a
    #  collision too. With a set, species+species collapsed to one label, and
    #  T-165 named CAMERUPT `FORGE` while MAGMAR had been FORGE since the Kanto
    #  seventy-nine -- this check passed it, and gbasprite.py then built the new
    #  drawing over MAGMAR's, because it finds a daemon's art by its name.
    #  Trainer classes are exempt WITHIN their own table: vanilla ships the
    #  same class twice on purpose (a Ruby/Sapphire copy beside FireRed's, a
    #  rival's per stage), and those are one thing listed twice.
    def doubled(labels):
        rest = [l for l in labels if l != "class"] + sorted(set(l for l in labels if l == "class"))
        return len(rest) > 1

    bad = [(w, sorted(v)) for w, v in seen.items()
           if doubled(v) and w not in ALLOWED]
    vbad, seen_versions = check_version()
    tbad = check_tickets()
    print("  %d names across %s" % (len(seen), ", ".join(sorted(surfaces))))
    for w, reason in sorted(ALLOWED.items()):
        if w in seen and doubled(seen[w]):
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

    tcopy = check_type_copy()
    if not tcopy:
        print("  the battle log's type names agree with the chart's.")
    else:
        print("\n  %d type name(s) in the battle log disagree with the chart:\n" % len(tcopy))
        for what, why in tcopy:
            print("   %-16s %s" % (what, why))

    sfresh = check_story_freshness()
    if sfresh:
        for what, why in sfresh:
            print("  ..  %-28s %s" % (os.path.basename(what), why))
    else:
        print("  both story documents are reconciled to the current bible.")

    ibad = check_vanilla_index()
    if not ibad:
        print("  no renamed daemon has a vanilla Index entry.")
    else:
        print("\n  %d vanilla Index entry(s) under our names:\n" % len(ibad))
        for what, why in ibad:
            print("   %-32s %s" % (what, why))

    nbad = check_near_collisions(surfaces)
    if not nbad:
        print("  no name is another with a vowel dropped.")
    else:
        print("\n  %d near-collision(s):\n" % len(nbad))
        for what, why in nbad:
            print("   %-30s %s" % (what, why))

    fbad = check_phantom_places()
    if not fbad:
        print("  no dialogue names a place the map does not have.")
    else:
        print("\n  %d phantom place name(s):\n" % len(fbad))
        for what, why in fbad:
            print("   %-44s %s" % (what, why))

    cbad = check_conflict_markers()
    if not cbad:
        print("  no file carries a merge conflict marker.")
    else:
        print("\n  %d conflict marker(s) COMMITTED:\n" % len(cbad))
        for what, why in cbad:
            print("   %-44s %s" % (what, why))

    pbad = check_stale_names()
    if not pbad:
        print("  no dialogue names a place, move, daemon or item we renamed.")
    else:
        print("\n  %d stale name(s) in dialogue:\n" % len(pbad))
        for what, why in pbad:
            print("   %-44s %s" % (what, why))

    nbad = check_vetoed()
    if not nbad:
        print("  no withdrawn word appears in anything a player can read.")
    else:
        print("\n  %d use(s) of a WITHDRAWN word:\n" % len(nbad))
        for what, why in nbad:
            print("   %-44s %s" % (what, why))

    wbad = check_panes()
    if not wbad:
        print("  every routine, ability, margin and item description fits the pane it prints into.")
    else:
        print("\n  %d line(s) past their pane:\n" % len(wbad))
        for what, why in wbad:
            print("   %-28s %s" % (what, why))

    dbad = check_disc()
    if not dbad:
        print("  every ground pickup that holds a PLUGIN or DRIVER shows the disc, and only those do.")
    else:
        print("\n  %d pickup(s) showing the wrong thing:\n" % len(dbad))
        for what, why in dbad:
            print("   %-44s %s" % (what, why))

    gbad = check_plugin_colours()
    if not gbad:
        print("  every PLUGIN disc carries our colour for the type of the routine on it.")
    else:
        print("\n  %d disc(s) teaching the wrong chart:\n" % len(gbad))
        for what, why in gbad:
            print("   %-24s %s" % (what, why))

    obad = check_one_chart()
    if not obad:
        print("  the type chart is one table, and both editions' ROMs carry it byte for byte.")
    else:
        print("\n  %d break(s) in invariant 3:\n" % len(obad))
        for what, why in obad:
            print("   %-24s %s" % (what, why))

    ibad = check_ids()
    if not ibad:
        print("  every flag and var we added has a number of its own, and every hidden item its own flag.")
    else:
        print("\n  %d number(s) answering to two names:\n" % len(ibad))
        for what, why in ibad:
            print("   %-24s %s" % (what, why))

    mbad = check_message_box()
    if not mbad:
        print("  every line of field dialogue fits the 208px message box.")
    else:
        print("\n  %d line(s) wider than the message box:\n" % len(mbad))
        for what, why in mbad:
            print("   %-52s %s" % (what, why))

    dbad2 = check_doubled()
    if not dbad2:
        print("  no line says a word twice across a break.")
    else:
        print("\n  %d word(s) said twice:\n" % len(dbad2))
        for what, why in dbad2:
            print("   %-60s %s" % (what, why))

    jbad = check_joins()
    if not jbad:
        print("  no line of dialogue runs into the next without a break.")
    else:
        print("\n  %d line(s) that run into the next with no space or break:\n" % len(jbad))
        for what, why in jbad:
            print("   %-52s %s" % (what, why))

    abad = check_articles()
    if not abad:
        print("  every a and an agrees with the name after it.")
    else:
        print("\n  %d article(s) that disagree with the name after them:\n" % len(abad))
        for what, why in abad:
            print("   %-52s %s" % (what, why))

    xbad = check_numbered()
    if not xbad:
        print("  no dialogue says a numbered PATCH, TM or HM; every NOTEBOOK entry and TEXTBOOK topic fits its page; the paper fits.")
    else:
        print("\n  %d numbered or oversized string(s):\n" % len(xbad))
        for what, why in xbad:
            print("   %-32s %s" % (what, why))

    if not tbad:
        print("  every ticket id is used once.")
    else:
        print("\n  %d ticket id problem(s):\n" % len(tbad))
        for what, why in tbad:
            print("   %-16s %s" % (what, why))
    return 1 if (bad or vbad or tbad or pbad or cbad or nbad or wbad or dbad or gbad or xbad or obad or ibad or abad or jbad or mbad or dbad2) else 0


if __name__ == "__main__":
    sys.exit(main())

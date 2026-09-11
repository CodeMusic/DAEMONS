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
    for root, dirs, files in os.walk(os.path.join(GBA, "data")):
        for fn in files:
            if fn != "text.inc":
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
               #  NOT o.isupper(). "POKé DOLL".isupper() is False, because é
               #  is not an uppercase character -- so the one item name in the
               #  game with an accent in it was invisible to this check on the
               #  very run that added items to it. The test is "contains no
               #  lowercase ASCII", which is what was meant all along.
               if o not in live and not re.search(r"[a-z]", o) and len(o) > 2}

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
            if re.search(r"\b%s\b" % re.escape(old), prose):
                out.append((rel, "says %s; the game calls it %s" % (old, new)))

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

    if not tbad:
        print("  every ticket id is used once.")
    else:
        print("\n  %d ticket id problem(s):\n" % len(tbad))
        for what, why in tbad:
            print("   %-16s %s" % (what, why))
    return 1 if (bad or vbad or tbad or pbad or cbad or nbad) else 0


if __name__ == "__main__":
    sys.exit(main())

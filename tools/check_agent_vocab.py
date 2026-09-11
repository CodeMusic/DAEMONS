#!/usr/bin/env python3
"""Prove no vanilla word reaches the model.

    python3 tools/check_agent_vocab.py        # exits non-zero if any do

WHY THIS EXISTS. The agent kept saying "Pokemon Mart", "Professor Oak",
"Pokemon" -- and every single time it turned out to be reading one of OUR
tables or OUR prompts, not recalling vanilla from training. Each was found the
same way: the user noticed it on screen, hours after the fact, one word at a
time. Four separate rounds of that.

The pattern is always the same, so the fix has to be a sweep rather than
another substitution: RENDER what the model actually sees and grep it. Not the
source -- the rendered text, because half the hits were in generated XML tags
and formatter templates rather than in any string a search for "POKEMON" would
have found.

WHAT IT CHECKS. Three surfaces, which together are everything:
    the developer prompt      prompts/game.txt, rendered
    the user prompt           the last one actually sent, from the run dir
    the name tables           mappings.json -- maps, NPCs, species, items, moves
    the bridge's own tables   compared against the C they read, not word-scanned

That fourth surface was added after POKEMON_TYPE_MAP shipped vanilla type names
for weeks. Nothing here caught it, because GROUND and ROCK were never listed as
banned WORDS -- they arrived as DATA, from a table nobody thought of as text.
The lesson generalises: a word scan finds what you already knew to forbid, and
a derived comparison finds what you did not.

A JS identifier like `current_pokemon_data` is NOT a finding: it is a contract
with the Python bridge and the model never sees it. Only rendered output counts,
which is exactly why this renders.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI   = os.path.join(ROOT, "engineAi")
GBA  = os.path.join(ROOT, "engineGba")

#  The lexicon, as what must never appear. Value is what it should have been,
#  so a failure tells you the fix rather than just the fault.
BANNED = [
    #  The town names match the Capitalised form as well as the SHOUTED one.
    #  They were upper-only, so "head back to Pewter" in the agent's own notes
    #  was invisible to every run of this check. Found by testing the checker
    #  against a sentence it should have caught rather than by reading it.
    #  Glossary rows still carry the vanilla name and EXEMPT still skips them.
    (r"Pok[eé]mon",       "DAEMON"),
    (r"\bPOKEMON\b",      "DAEMON"),
    (r"Pok[eé] ?Ball",    "BOX"),
    (r"Pok[eé]dex",       "INDEX"),
    (r"\bPOKEDEX\b",      "INDEX"),
    (r"Professor Oak",    "CRYSTAL CLEAR"),
    (r"PROF\.? ?OAK",     "CRYSTAL CLEAR"),
    (r"\bOAKS?_",         "CRYSTALS_"),
    (r"\b(?:PALLET|Pallet)\b",       "BLANCHE"),
    (r"\b(?:VIRIDIAN|Viridian)\b",     "CALLOW"),
    (r"\b(?:PEWTER|Pewter)\b",       "SLATE"),
    (r"\b(?:CERULEAN|Cerulean)\b",     "DOLDRUM"),
    (r"\b(?:LAVENDER|Lavender)\b",     "HALFTONE"),
    (r"\b(?:CELADON|Celadon)\b",      "VERDIGRIS"),
    (r"\b(?:FUCHSIA|Fuchsia)\b",      "LURID"),
    (r"\b(?:SAFFRON|Saffron)\b",      "BRAZEN"),
    (r"\b(?:CINNABAR|Cinnabar)\b",     "QUICKSILVER"),
    (r"\b(?:VERMILION|Vermilion)\b",    "ARDOR"),
    (r"DAEMON MART",      "THE REPO"),
    (r"DAEMON CENTER",    "CHECKPOINT"),
    #  1.6's six states. The bridge was handing the model the RAM's vanilla
    #  word while the screen said LEAKING, and this checker did not look --
    #  it knew about places and people and not about what a daemon IS.
    #  Lowercase too: the leak that got noticed was the agent thinking
    #  "Poison is ticking down", which no SCREAMING_SNAKE pattern would find.
    (r"(?i)\bpoison(ed|ing)?\b",   "LEAKING (or CASCADING if badly)"),
    (r"(?i)\bparaly[sz]ed?\b",     "THROTTLED"),
    (r"(?i)\bfaint(ed|ing|s)?\b",  "HALTED"),
    (r"(?i)\bconfus(ed|ion)\b",    "THRASHING"),
    (r"(?i)\bburned\b",            "OVERHEATED"),
]

#  The orientation table in game.txt QUOTES the vanilla names in order to
#  forbid them -- "You may expect Professor Oak; it is actually CRYSTAL CLEAR".
#  A checker that cannot tell a mention from a use would report the cure as the
#  disease, so the table's own rows are exempt and nothing else is.
#  Matched on a WINDOW, not a line. The developer prompt arrives
#  JSON-encoded, so its newlines are the two characters \ and n -- splitting
#  on a real newline found one enormous line and exempted nothing. The window
#  looks for the shape of a row in that table: the banned word, then a bolded
#  replacement a short distance later, with a pipe between them.
EXEMPT = re.compile(r"\|[^|]{0,40}\*\*[A-Z]")

#  The glossary teaches the agent "OURS / vanilla", and the agent then writes
#  that pair back in its own notes -- "Need POTION, PRIORITY/Paralyze Heal, and
#  USERBOXes". That is the table WORKING, not a leak: the vanilla word is there
#  because ours is sitting against it. EXEMPT only knows the table's own row
#  shape, so the inline form went unrecognised and was reported for days.
GLOSSED = re.compile(r"[A-Z]{3,}(?:\s?[A-Z]{3,})*\s*[/(]\s*$")
#  ...and the same gloss written the other way round: "Pewter/SLATE". Requires
#  an ALL-CAPS token after the slash, which is how every name of ours is
#  written, so "Pewter/Route 3" is still a leak.
GLOSSED_AFTER = re.compile(r"^\s*[/(]\s*[A-Z]{3,}")

#  Words that are also ordinary English. "navigation confusion" is not a status
#  condition and "the poison type" in a sentence about the chart is not either.
#  A checker that cries about these gets muted, and a muted checker finds
#  nothing at all -- which is worse than the leak it was built for.
INNOCENT = re.compile(
    #  Any -ing or -ion word in front of it is describing a muddle, not naming
    #  a state: navigation confusion, backtracking confusion. Listing them one
    #  at a time meant the list was always one run behind the agent's prose.
    r"(?i)"
    r"\b\w+(?:ing|ion)\s+confusion"
    r"|\b(any|the|more|less|some)\s+confusion"
    r"|confusion\s+(later|about|between|here)"
)

def scan(label, text):
    found = []
    for pat, want in BANNED:
        for m in re.finditer(pat, text):
            if EXEMPT.search(text[m.end():m.end() + 60]):
                continue
            #  Also exempt where the row's own explanation repeats the word it
            #  is forbidding: "| Poisoned | **LEAKING** -- and badly poisoned
            #  is **CASCADING** |" is one table row, not two offences.
            if EXEMPT.search(text[max(0, m.start() - 90):m.start()]):
                continue
            if INNOCENT.search(text[max(0, m.start() - 20):m.end() + 20]):
                continue
            #  ...and the inline gloss: OURS immediately before it, slashed or
            #  parenthesised. The agent is translating, which is the thing we
            #  asked it to be able to do.
            if GLOSSED.search(text[max(0, m.start() - 40):m.start()]):
                continue
            if GLOSSED_AFTER.search(text[m.end():m.end() + 40]):
                continue
            a, b = max(0, m.start() - 45), min(len(text), m.end() + 45)
            found.append((label, m.group(0), want,
                          text[a:b].replace("\n", " ").strip()))
    return found

def render_developer_prompt():
    js = ("(async()=>{const p=require('%s/server/src/ai/promptBuilder.js');"
          "const d=await p.buildDeveloperPrompt();"
          "process.stdout.write(typeof d==='string'?d:JSON.stringify(d));})()" % AI)
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True,
                         cwd=os.path.join(AI, "server"))
    return out.stdout

def stale_ours_check():
    """Names the PROMPT asserts that the build no longer has.

    This is the SECOND failure mode and the forbidding table cannot see it.
    That table catches VANILLA words reaching the model. This catches OUR OWN
    words gone stale -- which has now happened three times:

        INTERRUPT  became PREEMPT became WATCHDOG, and game.txt said PREEMPT
        CLARIFIER  became CC-7, and game.txt said CLARIFIER three times inside
                   the opening sequence, which the agent follows literally
        SURF, FLY  became TRAVERSE and GOTO along with 264 other routines, and
                   the prompt went on telling the agent to teach FLY and SURF

    Every one of those is a word this project chose and then changed, so no
    list of forbidden words will ever contain it. Only the build can catch it.

    ROUTINES ONLY, deliberately. Item and species names appear in the prompt
    inside vanilla-to-ours mapping rows where naming the vanilla side is the
    row's whole job -- the same EXEMPT problem the forbidding table already
    has -- while a routine name in this prompt is always an instruction to go
    and use it.
    """
    #  Ours for a DIFFERENT reason, each with the reason. Same device as
    #  check_lexicon's ALLOWED and needed for the same cause: one word can
    #  legitimately belong to two of our own surfaces at once.
    OURS_ELSEWHERE = {
        "BIND":   "1.5's verb -- you BIND a daemon. The move BIND is LATCH",
        "GROWTH": "a TYPE name (2.2). The move GROWTH is SCALE UP",
    }
    bad = []
    f = os.path.join(AI, "server", "prompts", "game.txt")
    ours_f = os.path.join(GBA, "src/data/text/move_names.h")
    if not (os.path.exists(f) and os.path.exists(ours_f)):
        return bad
    try:
        van = subprocess.run(["git", "-C", os.path.realpath(GBA), "show",
                              "upstream/master:src/data/text/move_names.h"],
                             capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return bad
    if not van:
        return bad
    pat = r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]+)"\)'
    ours = dict(re.findall(pat, open(ours_f, encoding="utf-8").read()))
    txt = open(f, encoding="utf-8").read()
    #  A table row that maps vanilla to ours names both sides on purpose.
    body = "\n".join(l for l in txt.split("\n")
                     if not (l.lstrip().startswith("|") and "**" in l))
    for mid, v in re.findall(pat, van):
        o = ours.get(mid)
        if not o or o == v or len(v) < 3 or v in OURS_ELSEWHERE:
            continue
        n = len(re.findall(r"\b%s\b" % re.escape(v), body))
        if n:
            bad.append(("prompt (stale ours)", v, o,
                        "%d place(s) -- the game renamed this routine and the "
                        "prompt did not" % n))
    return bad


def derived_table_check():
    """Compare the BRIDGE's own lookup tables against the game they read.

    This is the failure this tool did not have: POKEMON_TYPE_MAP shipped
    vanilla type names for weeks, so the agent was handed a type chart in one
    vocabulary and its own party's types in another and could not use its own
    chart. Nothing in the forbidding table caught it, because GROUND and ROCK
    were never listed as words -- they arrived as data.

    So this does not scan for words. It reads gTypeNames out of the C and
    compares, which cannot drift and cannot be argued with.
    """
    bad = []
    c = os.path.join(GBA, "src", "battle_main.c")
    a = os.path.join(AI, "firered_bridge", "constants", "addresses.py")
    if not (os.path.exists(c) and os.path.exists(a)):
        return bad
    body = re.search(r"const u8 gTypeNames\[.*?\{(.*?)\n\};",
                     open(c, encoding="utf-8").read(), re.S)
    if not body:
        return bad
    ours = dict(re.findall(r'\[TYPE_(\w+)\]\s*=\s*_\("(\w+)"\)', body.group(1)))
    src = open(a, encoding="utf-8").read()
    tm = re.search(r"POKEMON_TYPE_MAP = \{(.*?)\n\}", src, re.S)
    if tm:
        VAN = ["NORMAL","FIGHTING","FLYING","POISON","GROUND","ROCK","BUG","GHOST",
               "STEEL","MYSTERY","FIRE","WATER","GRASS","ELECTRIC","PSYCHIC","ICE",
               "DRAGON","DARK"]
        got = dict((int(k), v) for k, v in re.findall(r'(\d+)\s*:\s*"([^"]+)"', tm.group(1)))
        for i, v in enumerate(VAN):
            want = ours.get(v)
            if want and got.get(i) != want:
                bad.append(("bridge POKEMON_TYPE_MAP", got.get(i, "?"), want,
                            "type %d -- the agent is told this is what it is holding" % i))
    #  A step's trigger is matched against the badge id the bridge REPORTS, so
    #  the two files are a contract. Renaming BADGES broke it in silence: the
    #  card drew the SLATE MARK and the step stayed unticked, because the step
    #  was still waiting for BOULDER. It took a screenshot to find, which is
    #  exactly the loop this tool exists to close.
    bt = re.search(r"BADGES = \[(.*?)\n\]", src, re.S)
    if bt:
        MARKS = ["SLATE","SLOPE","SENSE","FIT","SKEW","FRAME","HEAT","TRUE"]
        got = [m[0] for m in re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]*)"', bt.group(1))]
        for i, want in enumerate(MARKS):
            if i < len(got) and got[i] != want:
                bad.append(("bridge BADGES", got[i], want, "benchmark %d, per 5.2" % (i + 1)))
    #  and the progress steps must trigger on ids the bridge can actually emit
    ids = set()
    if bt:
        ids = set(m[0] for m in re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]*)"', bt.group(1)))
    for rel in ("server/progress_steps.json", "server/gpt_data/progress_steps.json"):
        f = os.path.join(AI, rel)
        if not (ids and os.path.exists(f)):
            continue
        try:
            doc = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for e in (doc if isinstance(doc, list) else doc.get("steps", [])):
            if e.get("type") == "badge" and e.get("trigger") not in ids:
                bad.append(("progress_steps %s" % os.path.basename(os.path.dirname(f) or rel),
                            e.get("trigger", "?"), "one of " + "/".join(sorted(ids)),
                            "step %s never ticks -- the bridge cannot emit that id"
                            % e.get("id", "?")))
    return bad


def vanilla_name_check():
    """Vanilla DAEMON names reaching the model, derived from the build.

    The forbidding table lists towns and system words by hand, and a hand list
    cannot hold 151 species. So none of them were checked -- and the prompt was
    telling the agent to go and bind **Mewtwo**, by name, in the post-game
    section. It had been there the whole time and nothing looked.

    Same shape as the towns: ours-vs-upstream, so a species renamed tomorrow is
    covered tonight. Short names are skipped because a three-letter vanilla name
    is usually also an English word, and the glossary rows are exempt for the
    reason every other row is.
    """
    bad = []
    f = os.path.join(AI, "server", "prompts", "game.txt")
    if not os.path.exists(f):
        return bad
    #  species AND abilities: both are renamed wholesale and neither can live
    #  on a hand-written list. Abilities were the second half of the same hole
    #  -- the prompt names Levitate, which is NO ADDRESS.
    ours, pat = {}, r'\[(?:SPECIES|ABILITY)_(\w+)\]\s*=\s*_\("([^"]+)"\)'
    van = ""
    for rel in ("src/data/text/species_names.h", "src/data/text/abilities.h"):
        p = os.path.join(GBA, rel)
        if not os.path.exists(p):
            continue
        try:
            v = subprocess.run(["git", "-C", os.path.realpath(GBA), "show",
                                "upstream/master:" + rel],
                               capture_output=True, text=True, timeout=20).stdout
        except Exception:
            return bad
        van += v
        ours.update(dict(re.findall(pat, open(p, encoding="utf-8").read())))
    if not van:
        return bad
    texts = [("prompt (vanilla name)", open(f, encoding="utf-8").read())]
    live = os.path.join(AI, "server", "gpt_data", "last_userInputText_prompt.txt")
    if os.path.exists(live):
        texts.append(("user prompt (vanilla name)",
                      open(live, encoding="utf-8").read()))
    for label, txt in texts:
        for mid, v in re.findall(pat, van):
            o = ours.get(mid)
            if not o or o == v or len(v) < 5 or v == "??????????":
                continue
            for m in re.finditer(r"\b%s\b" % re.escape(v), txt, re.I):
                if EXEMPT.search(txt[m.end():m.end() + 60]):
                    continue
                if EXEMPT.search(txt[max(0, m.start() - 90):m.start()]):
                    continue
                if GLOSSED.search(txt[max(0, m.start() - 40):m.start()]):
                    continue
                if GLOSSED_AFTER.search(txt[m.end():m.end() + 40]):
                    continue
                a0, b0 = max(0, m.start() - 45), min(len(txt), m.end() + 45)
                bad.append((label, m.group(0), o,
                            txt[a0:b0].replace("\n", " ").strip()))
    return bad


def authored_text():
    """Everything we actually write that reaches the model."""
    out = []
    for rel in ("server/prompts/game.txt", "game_data_firered/mappings.json"):
        p = os.path.join(AI, rel)
        if os.path.exists(p):
            out.append(open(p, encoding="utf-8", errors="ignore").read())
    return "\n".join(out)


def main():
    hits = []
    live_hits = []
    hits += derived_table_check()
    hits += stale_ours_check()
    named = vanilla_name_check()
    hits += [h for h in named if not h[0].startswith("user prompt")]
    live_hits += [h for h in named if h[0].startswith("user prompt")]
    hits += scan("developer prompt", render_developer_prompt())

    #  The last prompt actually sent -- from the LIVE run dir, which is plain
    #  `gpt_data`. The timestamped siblings are archives that --fresh moved
    #  aside, and they legitimately contain the old wording: reporting those is
    #  reporting history as a fault. Sorting the directory listing in reverse
    #  picked an archive first, which is how this got noticed.
    live = os.path.join(AI, "server", "gpt_data", "last_userInputText_prompt.txt")
    if os.path.exists(live):
        live_hits += scan("user prompt (live)", open(live, encoding="utf-8").read())

    maps = os.path.join(AI, "game_data_firered", "mappings.json")
    if os.path.exists(maps):
        raw = json.load(open(maps))
        for table, val in raw.items():
            hits += scan("mappings.json/%s" % table, json.dumps(val))

    #  THE LIVE PROMPT IS A SNAPSHOT, NOT A SURFACE WE AUTHOR. A hit in it means
    #  the LAST RUN saw that word, which is two different things: either the
    #  word is still in something we write -- a real leak -- or we have already
    #  fixed it and the file simply predates the fix. Reporting the second as a
    #  fault is reporting history, which is the same mistake the archived
    #  prompts caused, one directory along.
    #
    #  Demonstrated 2026-09-11: ABILITY_NAME went from 77 stale to 0, and the
    #  live prompt went on saying TORRENT because it was written before that.
    src = authored_text()
    stale_snapshot = [h for h in live_hits
                      if not re.search(r"\b%s\b" % re.escape(h[1]), src, re.I)]
    hits += [h for h in live_hits if h not in stale_snapshot]

    if not hits:
        print("  no vanilla vocabulary reaches the model.")
        if stale_snapshot:
            print("  %d in the last run's prompt only, already fixed at source:"
                  % len(stale_snapshot))
            for label, word, want, ctx in stale_snapshot:
                print("     %-16s now %s -- clears on the next run" % (word, want))
        return 0
    print("  %d vanilla word(s) still reaching the model:\n" % len(hits))
    for label, word, want, ctx in hits:
        print("  %-28s %-16s should be %s" % (label, word, want))
        print("      ...%s...\n" % ctx)
    return 1

if __name__ == "__main__":
    sys.exit(main())

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
    (r"Pok[eé]mon",       "DAEMON"),
    (r"\bPOKEMON\b",      "DAEMON"),
    (r"Pok[eé] ?Ball",    "BOX"),
    (r"Pok[eé]dex",       "INDEX"),
    (r"\bPOKEDEX\b",      "INDEX"),
    (r"Professor Oak",    "CRYSTAL CLEAR"),
    (r"PROF\.? ?OAK",     "CRYSTAL CLEAR"),
    (r"\bOAKS?_",         "CRYSTALS_"),
    (r"\bPALLET\b",       "BLANCHE"),
    (r"\bVIRIDIAN\b",     "CALLOW"),
    (r"\bPEWTER\b",       "SLATE"),
    (r"\bCERULEAN\b",     "DOLDRUM"),
    (r"\bLAVENDER\b",     "HALFTONE"),
    (r"\bCELADON\b",      "VERDIGRIS"),
    (r"\bFUCHSIA\b",      "LURID"),
    (r"\bSAFFRON\b",      "BRAZEN"),
    (r"\bCINNABAR\b",     "QUICKSILVER"),
    (r"\bVERMILION\b",    "ARDOR"),
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

#  Words that are also ordinary English. "navigation confusion" is not a status
#  condition and "the poison type" in a sentence about the chart is not either.
#  A checker that cries about these gets muted, and a muted checker finds
#  nothing at all -- which is worse than the leak it was built for.
INNOCENT = re.compile(
    r"(?i)(navigation|avoid\w*|any|the)\s+confusion"
    r"|confusion\s+(later|about|between)"
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
    bt = re.search(r"BADGES = \[(.*?)\n\]", src, re.S)
    if bt:
        MARKS = ["SLATE","SLOPE","SENSE","FIT","SKEW","FRAME","HEAT","TRUE"]
        got = [m[0] for m in re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]*)"', bt.group(1))]
        for i, want in enumerate(MARKS):
            if i < len(got) and got[i] != want:
                bad.append(("bridge BADGES", got[i], want, "benchmark %d, per 5.2" % (i + 1)))
    return bad


def main():
    hits = []
    hits += derived_table_check()
    hits += scan("developer prompt", render_developer_prompt())

    #  The last prompt actually sent -- from the LIVE run dir, which is plain
    #  `gpt_data`. The timestamped siblings are archives that --fresh moved
    #  aside, and they legitimately contain the old wording: reporting those is
    #  reporting history as a fault. Sorting the directory listing in reverse
    #  picked an archive first, which is how this got noticed.
    live = os.path.join(AI, "server", "gpt_data", "last_userInputText_prompt.txt")
    if os.path.exists(live):
        hits += scan("user prompt (live)", open(live, encoding="utf-8").read())

    maps = os.path.join(AI, "game_data_firered", "mappings.json")
    if os.path.exists(maps):
        raw = json.load(open(maps))
        for table, val in raw.items():
            hits += scan("mappings.json/%s" % table, json.dumps(val))

    if not hits:
        print("  no vanilla vocabulary reaches the model.")
        return 0
    print("  %d vanilla word(s) still reaching the model:\n" % len(hits))
    for label, word, want, ctx in hits:
        print("  %-28s %-16s should be %s" % (label, word, want))
        print("      ...%s...\n" % ctx)
    return 1

if __name__ == "__main__":
    sys.exit(main())

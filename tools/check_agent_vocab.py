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

A JS identifier like `current_pokemon_data` is NOT a finding: it is a contract
with the Python bridge and the model never sees it. Only rendered output counts,
which is exactly why this renders.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI   = os.path.join(ROOT, "engineAi")

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

def scan(label, text):
    found = []
    for pat, want in BANNED:
        for m in re.finditer(pat, text):
            if EXEMPT.search(text[m.end():m.end() + 60]):
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

def main():
    hits = []
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

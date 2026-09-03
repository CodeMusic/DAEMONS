#!/usr/bin/env python3
"""Spend the room Gen 3 gives the Index.

    python3 tools/index_expand.py [--write]

Run AFTER tools/port_index.py, which carries the Game Boy text across. This
replaces it with a longer version, and only in the GBA build.

Gen 1 gives an entry six lines of about eighteen characters -- roughly 108.
Gen 3 gives three of about forty-two -- roughly 126. That is one more short
sentence, not a new canvas, and it is spent as one more BEAT rather than on
adjectives: the entries have a shape (a fact, a consequence, an unmarked
absence) and the extra room extends the shape rather than decorating it.

The Game Boy build keeps the short versions. It has to -- 126 characters do not
fit in 108 -- so this is the one place the two engines deliberately differ, and
it differs by length rather than by meaning. Nothing here says anything the
short version did not already imply.

Craft rule 1 throughout: not one of these explains what it is about.
"""
import os, re, sys

GBA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engineGba")
WRITE = "--write" in sys.argv
WIDTH, LINES = 42, 3

# daemon -> (vanilla species label used by the GBA text symbol, text)
TEXT = {
    "INJECTOR":  ("Beedrill",   "Puts its own instructions where data was expected. The reader cannot tell the difference. It was never asked to."),
    "MANIFOLD":  ("Blastoise",  "The scattered points were on a surface all along. It can show you the shape, not a name. Naming was another job."),
    "ROVERCUB":  ("Bulbasaur",  "Small enough to carry. Learns from what it is carried past. It has no way to choose the route. It remembers it."),
    "INDEXER":   ("Butterfree", "Turns what was gathered into something that can be found again. What it cannot file, it drops. No record is kept."),
    "CRAWLER":   ("Caterpie",   "Follows every link it finds, then the links it finds there. It has no opinion about any of them. It never finishes."),
    "CANON":     ("Charizard",  "Every case it meets is decided by cases it has already met. New things are filed as errors. The file is not read."),
    "LABL":      ("Charmander", "Holds one example and the answer that came with it. Someone else decided what it means. It has never met them."),
    "RUBRIC":    ("Charmeleon", "It no longer needs answers. It has the rule that made them. Nothing checks the rule. It is applied to everything."),
    "FLOOD":     ("Fearow",     "Many of them ask at once, and each one is owed a reply. Nothing is left to answer with. Each of them waits."),
    "CODEMUSAI": ("Flareon",    "Given a rule, it will not stop until the rule is met. It does not ask where the rule came from. It could not."),
    "ROVERSEER": ("Ivysaur",    "Too large to carry now. It answers before it is asked. It has never once been outside. The answers are very good."),
    "SEEKMUSAI": ("Jolteon",    "Finds the nearest match to anything it is shown. Nearest is not the same as right. Nobody told it. Nobody will."),
    "BUFFER":    ("Kakuna",     "Holds what was taken until there is somewhere to put it. It does not know where that is. It keeps holding."),
    "PENDING":   ("Metapod",    "Waiting to be processed. It has been waiting a while. Nothing has told it how long. It has stopped counting."),
    "ARTSAI":    ("Mew",        "Observed once, at a facility, by five people. No two accounts agree. The record is filed complete and unread."),
    "STARR":     ("Mewtwo",     "Assembled from a study of a single prior event. Not derived from a sample. Built to specification. Signed off."),
    "BROADCAST": ("Pidgeot",    "Sends to everyone at once, because it cannot tell who needs it. Most of what it says lands nowhere. It sends again."),
    "RELAY":     ("Pidgeotto",  "Takes what it is handed and hands it on. It does not open it. That is the whole of the job. It is good at it."),
    "PACKET":    ("Pidgey",     "Carries something it cannot read to somewhere it has never been. It does not ask what is inside. It arrives."),
    "SPIKE":     ("Pikachu",    "A single burst, then nothing. It means something only if something was counting. Usually nothing is. It fires."),
    "SURGE":     ("Raichu",     "It no longer stops between bursts. What was a signal is now a condition. Nothing reads it. Nothing needs to."),
    "OVERFLOW":  ("Raticate",   "It kept counting past the space it was given. Nothing stopped it. Nothing was watching. It is counting still."),
    "NIBBLE":    ("Rattata",    "Four bits. The smallest piece the Index will file on its own. There are a great many. No two are filed together."),
    "PING":      ("Spearow",    "Asks one question and requires an answer. The question is: are you there. It asks again. It has always asked."),
    "CLUSTR":    ("Squirtle",   "Puts near things with near things. Nobody told it which things matter. It has guessed. Nobody checked the guess."),
    "CAREMUSAI": ("Vaporeon",   "Reads the room before it reads the problem. Often correct. Cannot show its working. It was never written down."),
    "ROVERBYTE": ("Venusaur",   "It has a body now, and senses that come with one. Everything it predicted, it can finally check. Some was wrong."),
    "LOCUS":     ("Wartortle",  "It found a rule the points obey. It cannot say what the rule is for, only that it holds. So far it has held."),
    "SCRAPER":   ("Weedle",     "Takes the same things a CRAWLER takes, by the same method. Nobody gave it permission. Nobody asked for it back."),
}

import textwrap
rc = 0
for fname in ("pokedex_text_fr.h", "pokedex_text_lg.h"):
    path = os.path.join(GBA, "src/data/pokemon", fname)
    text = open(path).read()
    placed = 0
    for daemon, (label, body) in sorted(TEXT.items()):
        wrapped = textwrap.wrap(body, WIDTH)
        if len(wrapped) > LINES:
            print("  !! %-10s %d chars, will not fit %d lines of %d"
                  % (daemon, len(body), LINES, WIDTH)); rc = 1; continue
        block = "\n".join('    "%s%s"' % (l, "\\n" if i < len(wrapped) - 1 else "")
                          for i, l in enumerate(wrapped))
        sym = "g%sPokedexText" % label
        pat = re.compile(r'(const u8 %s\[\] = _\(\n).*?(\);)' % re.escape(sym), re.S)
        text, n = pat.subn(lambda m: m.group(1) + block + ");", text)
        if n: placed += 1
        else:
            print("  !! no %s in %s" % (sym, fname)); rc = 1
    print("  %s: %d/%d" % (fname, placed, len(TEXT)))
    if WRITE and rc == 0:
        open(path, "w").write(text)
if WRITE:
    print("  written" if rc == 0 else "  NOT written")
sys.exit(rc)

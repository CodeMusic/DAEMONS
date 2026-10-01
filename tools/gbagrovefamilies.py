#!/usr/bin/env python3
"""The grove daemons: names, categories and both editions' INDEX entries (T-221).

    python3 tools/gbagrovefamilies.py            # report every line, measured to the entry pane
    python3 tools/gbagrovefamilies.py --write    # species_names.h, pokedex_entries.h, pokedex_text_fr.h and _lg.h

Thirty-two daemons in fourteen families, one family to a GROVE (tools/gbagrove.py places them). The user approved
the names and the table on 2026-10-01; every word below is DRAFT until they read it in play.

THE SWAP. Each world hides the other half: the mainland's groves hold daemons of PSYCHOLOGY's lineage, named in its
register; the islands' hold COMPUTING's, named in its. Each entry has two jobs -- describe the creature, and teach the
word it is named for without saying it is teaching (T-322). CONTENT says what it does; CONTEXT what follows (8.2c).

Vanilla's slots keep their stats, types and learnsets; they already sit where the design wants them (LATENT for
the ghosts, SWARM for the bugs, CONTEXT for the psychics). Their sprites go through gfx/daemons and gbasprite.py.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
PANE_W, PANE_LINES = 234, 4

_src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
_ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
exec(compile(_src.split("# ------------------------------------------------------- names, derived")[0], "port_vocab.py", "exec"), _ns)
width = _ns["textwidth"]

#  T-221: the thirty-two grove daemons (the user approved the names and the grove table, 2026-10-01). DRAFT words.
#  (slot, name, category, CONTENT entry, CONTEXT entry, what it looks like -- for the sprite server, greyscale)
FAMILIES = [
    # ---- the mainland's groves: psychology's lineage, named in psychology's register
    ("UNDERTONE", "SPECIES_KECLEON", [
        ("KECLEON", "UNNOTICED", "UNSEEN",
         "It stands in plain view. Most who pass it are looking for something else, and so do not see it.",
         "Everyone who walked past it is sure nothing was there. They are right about what they saw.",
         "a chameleon-like lizard standing upright with a curled tail and big rolling eyes, its body striped with a zigzag band, half blended into its surroundings"),
    ]),
    ("ROUTE 25", "SPECIES_RALTS", [
        ("RALTS", "GUESSWORK", "GUESSER",
         "It cannot see what others feel. It guesses from their faces, and is wrong less often each time.",
         "Whoever it is near feels understood. It is only guessing. It guesses well.",
         "a small slim child-like creature in a long gown-like body with a big helmet of hair covering its eyes and two little red horns, peeking shyly"),
        ("KIRLIA", "ATTUNE", "ATTUNER",
         "It moves when others move. It is never told how they feel. It matches it anyway, a little behind.",
         "Near it, a crowd starts to move as one. Nobody can say who started.",
         "a slender dancer-like creature with a tutu-like skirt, arms raised as it spins on one toe, a red horn on its head"),
        ("GARDEVOIR", "MENTALIZE", "MINDREADER",
         "It holds a model of every mind nearby, and acts on the model. When the model is wrong, it changes it.",
         "It knows what you will do before you do. It waits for you to do it anyway.",
         "a tall graceful figure in a flowing gown-like body, a red fin on its chest, one arm extended, calm"),
    ]),
    ("ROUTE 1", "SPECIES_SPOINK", [
        ("SPOINK", "BREATHING", "RHYTHM",
         "It bounces to keep its heart beating. If it stops, so does the beat. It has never once stopped.",
         "Those near it start to breathe in time with it. None of them notice.",
         "a small pig-like creature balanced on a coiled spring tail, a round pearl on its head, short arms"),
        ("GRUMPIG", "GUTFEEL", "INSIDE",
         "It answers before it thinks, from somewhere in its body. It is right more often than thinking would be.",
         "It cannot explain a single answer it gives. It has stopped trying to.",
         "an upright pig-like creature with two dark pearls on its head and one on its belly, hands raised, frilled ears"),
    ]),
    ("ROUTE 24", "SPECIES_MEDITITE", [
        ("MEDITITE", "WITNESS", "OBSERVER",
         "It sits very still and watches its own thoughts go past. It does not stop them. It notes each one.",
         "It has seen every thought it has had. It is still surprised by some.",
         "a small meditating creature sitting cross-legged, a round head with ear-like tufts, eyes closed, baggy trousers"),
        ("MEDICHAM", "MINDSIGHT", "INSIGHT",
         "It sees its own mind as clearly as a room, and moves through it on purpose.",
         "It knows why it is angry before it is angry. It is angry less often.",
         "a lean balanced figure standing on one leg in a yoga pose, arms out, a tall crest on its head, baggy trousers"),
    ]),
    ("ROUTE 8", "SPECIES_DUSKULL", [
        ("DUSKULL", "FADING", "DECAY",
         "Whatever it passes grows faint. Not gone. Fainter each time it is not looked at.",
         "Things it drifted past are still there. Nobody can quite remember where.",
         "a small floating hooded spirit with a skull-like mask and one glowing eye, a wispy tail instead of legs"),
        ("DUSCLOPS", "FORGETTING", "ERASURE",
         "It takes in what is no longer used and keeps nothing. The room it frees is why anything new fits.",
         "Those who meet it feel lighter after, and cannot say what they put down.",
         "a stout wrapped mummy-like figure with one big eye, wide open hands and a hollow body"),
    ]),
    ("ROUTE 11", "SPECIES_SLAKOTH", [
        ("SLAKOTH", "DAYDREAM", "DRIFTER",
         "It lies still for hours. Behind its eyes it is busier than it ever is awake.",
         "Ask it what it was thinking. It will not know. It was thinking all of it.",
         "a small sloth lying on its belly with half-lidded sleepy eyes and a contented smile, long claws"),
        ("VIGOROTH", "RESTLESS", "FIDGETER",
         "It cannot keep still. Its attention leaves every task half done and goes looking for the next.",
         "Everything near it is started. Little near it is finished. It is not unhappy.",
         "a wiry ape-like creature with a tuft of hair on its head, mid-leap with arms flailing, long claws"),
        ("SLAKING", "MINDWANDER", "WANDERER",
         "It lies in one place and goes everywhere. What it finds while lying there it brings back as ideas.",
         "It looks idle. It is the one in the grove that has the new thoughts.",
         "a huge reclining gorilla-like creature propped on one elbow, eyes shut, a calm face, a big belly"),
    ]),
    ("ROUTE 13", "SPECIES_SHUPPET", [
        ("SHUPPET", "UNSPOKEN", "UNSAID",
         "It feeds on what people do not say. It grows where things go unsaid, and hangs back from the talking.",
         "Every room has one. It is quietest in the rooms that seem fine.",
         "a small floating cloth-puppet ghost with a single bent horn and big eyes, a ragged hem"),
        ("BANETTE", "SUBTEXT", "UNDERNEATH",
         "What it says and what it means are different things. The meaning is in the stitching. Its mouth is zipped shut.",
         "Everything it says is polite. Everyone who hears it knows what it meant.",
         "a ragged stitched doll creature with a zipper for a mouth, long thin arms and a pointed head"),
    ]),
    # ---- the islands' groves: computing's lineage, named in computer science's register
    ("FIVE ISLE MEADOW", "SPECIES_BELDUM", [
        ("BELDUM", "SINGLETON", "INSTANCE",
         "Only one of it exists at a time. Every part of the system that asks for one gets this one.",
         "It answers to everyone. Nobody else answers to it.",
         "a floating metal body with a single round eye and a magnet-like claw underneath"),
        ("METANG", "PAIRWISE", "COUPLED",
         "Two of them joined, and they compare every result across the pair before they act. Slower, and seldom wrong.",
         "It argues with itself before every move. Both sides usually win.",
         "a floating metal body with two arms joined to it, two eyes and a cross shape on its face"),
        ("METAGROSS", "FEDERATED", "COLLECTIVE",
         "Four minds, kept apart, learn in four places. Only what they learned is shared, never what they saw.",
         "None of the four has seen what the others saw. Together they know it anyway.",
         "a heavy armoured creature on four clawed metal legs, a big X shape across its face"),
    ]),
    ("LONG WADE", "SPECIES_NOSEPASS", [
        ("NOSEPASS", "GRADIENT", "SLOPE",
         "It always faces the way down. Moved, it turns back by itself, a little at a time, toward the lowest point.",
         "It is certain which way is better. It has never seen the bottom.",
         "a stone figure with a big pointed nose like a compass needle, small stubby arms and a heavy body"),
    ]),
    ("DENSE WOOD", "SPECIES_GULPIN", [
        ("GULPIN", "GREEDY", "SWALLOWER",
         "It takes the nearest best thing, every time, without looking further. It is quick, and often wrong.",
         "It is always full. It is never satisfied.",
         "a small round blob creature with a little tuft on top, a tiny mouth and no arms"),
        ("SWALOT", "BLOATWARE", "BLOAT",
         "It swallowed everything it was ever shown, whole, and learned none of it. It is very large.",
         "It can repeat anything it has eaten. It cannot tell you what it meant.",
         "a huge round blob creature with a wide gaping mouth, small whiskers and diamond markings"),
    ]),
    ("ONE ISLAND", "SPECIES_WURMPLE", [
        ("WURMPLE", "HASHSEED", "SEED",
         "A number nobody chose decides what it will grow into. Even it does not know which.",
         "Two that look the same will not end the same. Nobody can tell which from outside.",
         "a small caterpillar with spikes on its back and a pointed stinger tail"),
        ("SILCOON", "IFTRUE", "CHECK",
         "Sealed in pale silk. Inside, the condition held. It will come out as what follows.",
         "It is sure it is on the right path. It has only seen the one.",
         "a pale silk cocoon with a pair of sleepy eyes peering out of a slit"),
        ("BEAUTIFLY", "THENCASE", "THEN",
         "What follows a condition that held. It is bright, and flies the path that was expected.",
         "Everyone was hoping for this one. It never learned why.",
         "a bright butterfly with big patterned wings and a curled proboscis"),
        ("CASCOON", "IFFALSE", "ELSE",
         "Sealed in dark silk. Inside, the condition failed. It goes on anyway, the other way.",
         "It does not know it is the other case. To it, this is the case.",
         "a dark silk cocoon with one narrow eye peering out"),
        ("DUSTOX", "OTHERWISE", "FALLBACK",
         "What follows a condition that failed. It flies at night, by a path nobody wrote down.",
         "Nobody planned for it. It got there anyway, and lights its own way.",
         "a dusty moth with broad spotted wings and feathery antennae"),
    ]),
    ("TWO ISLAND", "SPECIES_CASTFORM", [
        ("CASTFORM", "OVERLOADED", "OVERLOAD",
         "One name, many bodies. Which body answers depends on the weather it is called in.",
         "Everyone who has met it describes a different one. All of them are right.",
         "a small round cloud-like creature with a little face and a wispy curl on its head"),
    ]),
    ("FOUR ISLAND", "SPECIES_NINCADA", [
        ("NINCADA", "PREFORK", "PRECOPY",
         "It makes copies of itself before they are needed, and waits underground with them.",
         "It is ready for a crowd that has not come. It does not mind waiting.",
         "a small burrowing insect with big digging claws and stubby wings"),
        ("NINJASK", "BURSTMODE", "BURST",
         "It does everything at once, as fast as it can, and then it is spent. Gone before you see it.",
         "Everything near it happens too fast to watch. Then nothing happens.",
         "a sleek fast flying insect with blurred wings and a slim body"),
        ("SHEDINJA", "DEFUNCT", "HUSK",
         "The shell left behind when the copy moved on. It still runs. Nothing is inside it.",
         "It keeps its place in the list. Nobody has cleared it. Most things pass right through it.",
         "a hollow cicada shell floating with a halo above it and a crack down its back"),
    ]),
    ("SEVEN ISLAND", "SPECIES_BALTOY", [
        ("BALTOY", "LIKELIHOOD", "PRIOR",
         "It spins on one point and leans toward what it has seen most. It has seen very little.",
         "It is sure. It has nothing yet to be sure about.",
         "a small clay figurine spinning on one point, two little arms and a row of eyes"),
        ("CLAYDOL", "POSTERIOR", "UPDATED",
         "Each thing it sees shifts what it believes, by exactly as much as it should. It is never quite certain.",
         "It changes its mind often, a little at a time, and always for a reason.",
         "a tall clay idol with many eyes around its head and two floating arms"),
    ]),
]


def wrap(s):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if cur and width(t) > PANE_W:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def ident(slot):
    """KECLEON -> Kecleon, the way the dex text symbols are spelled."""
    return slot.capitalize()


def entry_text(lines):
    return "".join('    "%s%s"\n' % (l, "\\n" if i < len(lines) - 1 else "") for i, l in enumerate(lines)).rstrip("\n")


def main():
    names_p = os.path.join(GBA, "src/data/text/species_names.h")
    entries_p = os.path.join(GBA, "src/data/pokemon/pokedex_entries.h")
    fr_p = os.path.join(GBA, "src/data/pokemon/pokedex_text_fr.h")
    lg_p = os.path.join(GBA, "src/data/pokemon/pokedex_text_lg.h")
    names, entries, fr, lg = (open(p).read() for p in (names_p, entries_p, fr_p, lg_p))
    bad, n = 0, 0
    for grove, _, fam in FAMILIES:
        for slot, name, cat, content, context, _look in fam:
            n += 1
            assert len(name) <= 10 and len(cat) <= 11, name
            for ed, text in (("CONTENT", content), ("CONTEXT", context)):
                lines = wrap(text)
                if len(lines) > PANE_LINES or any(c in text for c in "[]"):
                    print("  !! %s %s: %d lines" % (name, ed, len(lines)))
                    bad += 1
            print("  %-10s %-10s %-11s %s" % (grove[:10], name, cat, slot))
            names = re.sub(r'(\[SPECIES_%s\]\s*=\s*_\(")[^"]*("\))' % slot, r"\g<1>%s\g<2>" % name, names)
            entries = re.sub(r'(\[NATIONAL_DEX_%s\]\s*=\s*\{\s*\.categoryName = _\(")[^"]*("\))' % slot,
                             r"\g<1>%s\g<2>" % cat, entries)
            for text, which in ((content, "fr"), (context, "lg")):
                pat = r'(const u8 g%sPokedexText\[\] = _\(\n)(?:.*\n)*?(.*"\);)' % ident(slot)
                body = entry_text(wrap(text)) + ");"
                if which == "fr":
                    fr = re.sub(pat, lambda m: m.group(1) + body, fr, count=1)
                else:
                    lg = re.sub(pat, lambda m: m.group(1) + body, lg, count=1)
    old = [open(p).read() for p in (names_p, entries_p, fr_p, lg_p)]
    changed = [p for p, o, s in zip((names_p, entries_p, fr_p, lg_p), old, (names, entries, fr, lg)) if o != s]
    print("\n  %d daemons, %d over the pane; %s" % (n, bad, ", ".join(os.path.basename(p) for p in changed) or "nothing to change"))
    if bad:
        return 1
    if WRITE:
        for p, s in zip((names_p, entries_p, fr_p, lg_p), (names, entries, fr, lg)):
            open(p, "w").write(s)
        print("  written" if changed else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())

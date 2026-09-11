#!/usr/bin/env python3
"""Make the GBA build's dialogue speak the vocabulary the Game Boy build speaks.

    python3 tools/port_vocab.py [--write]

**The Game Boy got this almost for free and the GBA cannot.** `pokered` writes
the core noun as the charmap glyph `#`, so ONE line -- `charmap "#", $54 ; DAE`
-- renamed POKéMON everywhere at once. `pokefirered` spells the word out in
every string, so the same rename is a few thousand substitutions and every
touched line has to be rewrapped.

Where the map comes from, and why it is derived rather than typed:

  * species, items and moves are diffed out of OUR OWN GBA tables against
    upstream's, the way `port_names.py` does it -- if the Index says PACKET,
    the NPC who mentions one has to say PACKET too
  * the rest is lifted from the Game Boy diff: ROCKET -> CORPUS, TRAINER ->
    USER, catch -> bind, BADGE -> MARK, and the eleven town names

Singular and plural is the hard part, and it is NOT derivable. `pokered` had
two spellings, `#MON` and `#MONS`, and the Game Boy pass chose between them by
hand 586 times; "your" is plural 7 times and singular 25, so no rule recovers
the choice. What is here agrees with those 586 decisions **93.7%** of the time
-- measured, by scoring it against them. The remaining 6% is a handful of lines
that will read as singular where you wrote plural.
"""
import difflib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
#  Fixed-width arrays the sweep can overflow. The compiler catches these as
#  "excess elements in array initializer", which is a link-time surprise from a
#  text pass -- and agbcc reports it as a warning, which this project's build
#  turns into a bare Error 1. Checked here instead, where the fault is legible.
#  region_map_sections.json is NOT swept, and the reason is two-sided.
#
#  Mechanically: renaming a mapsec renames a generated C symbol that
#  src/region_map.c refers to BY HAND, so the sweep breaks the build at a
#  point far from the edit. It did: DIGLETT -> TAPPOINT turned DIGLETT'S CAVE
#  into TAPPOINT'S CAVE and took sMapsecName_DIGLETT_S_CAVE with it.
#
#  And by design: a place is not a creature. EMBER -> JITTER also produced
#  MT. JITTER and JITTER SPA -- both on the Sevii Islands, where 8.2a's ruling
#  is exact and is "name nothing there". A vocabulary pass must not make a
#  naming decision that a section of the bible has deferred.
NEVER_SWEEP = (
    "region_map_sections.json",
    #  Nothing here is prose: 387 dex CATEGORIES and nothing else. A category
    #  is authored per species, and letting the word pass rewrite one produced
    #  a twelve-character NIGHT REPAIR in an eleven-character array, because a
    #  MOVE rename reached a SPECIES descriptor. Same class as the map file.
    "pokedex_entries.h",
    #  gTypeNames lives here, and the move GROWTH became SCALE UP -- so the
    #  word pass learned "GROWTH -> SCALE UP" and went for the TYPE. Only the
    #  array's own width stopped it. A type name is the argument (invariant 3);
    #  it is authored, never substituted.
    "battle_main.c",
)

#  THE PRINCIPLE, since this is the third file to need it: NAME TABLES ARE
#  AUTHORED AND PROSE IS SWEPT. A pass that rewrites prose must never reach a
#  table it also learns from, or a rename in one surface silently rewrites
#  another. Places, dex categories and type names are all names.

#  FIXED is BOTH halves of the rule now, and it was only ever one.
#
#  It was a WIDTH CHECK wearing a name-protection label: it refused a rename
#  that overflowed the array and accepted one that fitted. So the ability
#  OWN TEMPO, authored NO THRASH, became NO BUSY WAIT when the move THRASH was
#  renamed -- twelve characters of twelve, no warning, and it shipped. Three
#  more went the same way, and one of them was the line in the SCHOOL whose
#  whole job is teaching the type chart.
#
#  A span matching any of these is AUTHORED and is skipped entirely, whatever
#  file it is in. That is the difference between protecting a FILE, which stops
#  its prose being swept too, and protecting a LINE, which is what the rule
#  actually says. The width check stays underneath as belt and braces.
FIXED = {
    r'\[ABILITY_\w+\] = _\("([^"]+)"\)':                  ("ability name", 12),
    r'\[MOVE_\w+\]\s*=\s*_\("([^"]+)"\)':                ("move name", 12),
    r'\[SPECIES_\w+\]\s*=\s*_\("([^"]+)"\)':             ("species name", 10),
    r'\.categoryName = _\("([^"]+)"\)':                   ("dex category", 11),
    r'\[TRAINER_CLASS_\w+\]\s*=\s*_\("([^"]+)"\)':       ("trainer class", 12),
    r'\.trainerName = _\("([^"]+)"\)':                    ("trainer name", 11),
    r'\[TYPE_\w+\] = _\("([^"]+)"\)':                     ("type name", 7),
    #  gExpandedPlaceholder_* is the table behind the {RUBY}, {SAPPHIRE},
    #  {AQUA}, {RED} control codes -- the GAME's names and the other version's
    #  characters, not ours. Renaming the ITEM ruby to PUBLIC KEY reached this
    #  table and would have made the code {RUBY} expand to "PUBLIC KEY" in
    #  link and trade text. Same class as the ability names: a name table a
    #  prose pass had no business in.
    r'gExpandedPlaceholder_\w+\[\] = _\("([^"]*)"\)':      ("placeholder", 16),
}
FIXED_RE = [re.compile(p) for p in FIXED]

BUDGET, WIDE = 196, {"data/text/help_system.inc": 220,
                     "data/text/new_game_intro.inc": 220}

# ------------------------------------------------------------------ the font
def _font():
    src = open(os.path.join(GBA, "src/text.c"), encoding="utf-8").read()
    body = re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};', src, re.S).group(1)
    widths = [int(x) for x in re.findall(r'\d+', body)]
    cm = {}
    for line in open(os.path.join(GBA, "charmap.txt"), encoding="utf-8"):
        line = line.split('@')[0].strip()
        if '=' not in line:
            continue
        k, v = (p.strip() for p in line.split('=', 1))
        if len(k) == 3 and k[0] == k[2] == "'":
            k = k[1]
        elif len(k) > 1 and k[0] == k[-1] == '"':
            k = k[1:-1]
        try:
            cm[k] = int(v, 16)
        except ValueError:
            pass
    return widths, cm

WIDTHS, CHARMAP = _font()
# A control code either DRAWS NOTHING or expands to a word. Measuring the
# second kind as zero makes a line look short, and own_budget then wraps the
# string to a width it never had -- "{B_ATK_NAME_WITH_PREFIX} fled from battle"
# came back as three lines. Formatting codes are free; the rest cost a name.
FORMAT_CODE = re.compile(r'\{(PLAY_SE|PLAY_BGM|PALETTE|COLOR|HIGHLIGHT|SHADOW|COLOR_HIGHLIGHT_SHADOW'
                         r'|CLEAR_TO|CLEAR|SKIP|PAUSE\w*|FONT\w*|SIZE|WAIT\w*|ESCAPE|NO|UNKNOWN\w*)\b[^}]*\}')
# ...and a third kind: a code that draws ONE GLYPH. Counting {CIRCLE_2} or
# {PLUS} as a seven-letter name made help_system.inc look 80px wider than it is.
ICON_CODE = re.compile(r'\{(CIRCLE_\d|SQUARE_\d|TRIANGLE_\d|PLUS|MINUS|LV|PP|ID|NO|UP_ARROW'
                       r'|DOWN_ARROW|LEFT_ARROW|RIGHT_ARROW|[ABLR]_BUTTON|START_BUTTON'
                       r'|SELECT_BUTTON|DPAD\w*|PKMN|POKEBLOCK|E_?WITH\w*|APOSTROPHE\w*)\}')
NAME_TOKEN = re.compile(r'\{[^}]*\}')

def textwidth(s):
    total = 0
    for tok in re.findall(r'\{[^}]*\}|.', s):
        if tok.startswith('{'):
            if ICON_CODE.fullmatch(tok):
                total += 8
            elif not FORMAT_CODE.fullmatch(tok):
                total += sum(WIDTHS[CHARMAP[c]] for c in "ABCDEFG")
            continue
        g = CHARMAP.get(tok)
        if g is not None and g < len(WIDTHS):
            total += WIDTHS[g]
    return total

# ------------------------------------------------------- names, derived
def git_show(path):
    return subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + path],
                          capture_output=True, text=True).stdout

def pairs_from(path, pattern):
    """{vanilla -> ours} for one table, by diffing us against upstream."""
    old = re.findall(pattern, git_show(path))
    new = re.findall(pattern, open(os.path.join(GBA, path), encoding="utf-8").read())
    out = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == 'replace' and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                if old[i1 + k] != new[j1 + k]:
                    out[old[i1 + k]] = new[j1 + k]
    return out

NAMES = {}
NAMES.update(pairs_from("src/data/text/species_names.h", r'_\("([^"]*)"\)'))
#  Trainer classes are a rename surface like any other, and were not being
#  learned from. POKéMANIAC became ARCHIVIST weeks ago and four lines of
#  dialogue still said POKéMANIAC -- the accented prefix, for the sixth time.
NAMES.update(pairs_from("src/data/text/trainer_class_names.h", r'_\("([^"]*)"\)'))
NAMES.update(pairs_from("src/data/text/move_names.h",    r'_\("([^"]*)"\)'))
NAMES.update(pairs_from("src/data/items.json",           r'"english":\s*"([^"]*)"'))
# a rename is only safe to apply inside prose if the vanilla name is a word
#
#  NOT .isupper(). "é" IS A LOWERCASE CASED CHARACTER, so "POKéMANIAC".isupper()
#  is False and so is "POKé DOLL".isupper() -- and this filter was therefore
#  dropping EVERY vanilla name that contains the accent, which is precisely the
#  set of names this whole tool exists to remove. POKéDEX is hardcoded down in
#  VOCAB because somebody hit the symptom and patched that one instance.
#
#  The intent was "no lowercase letters", so say that. This is the same family
#  as the escape trap: a rule about characters, written in terms of a function
#  that means something slightly different, silently excluding the exact cases
#  that mattered.
NAMES = {k: v for k, v in NAMES.items()
         if not re.search("[a-z]", k) and len(k) > 3
         and k not in ("NONE", "????????")}

#  THE EIGHTEEN TYPE NAMES ARE NEVER SUBSTITUTED, anywhere, by anything. The
#  chart is the argument (invariant 3) and its words are authored on every
#  surface, not just in battle_main.c. One of them is also a MOVE name that
#  was renamed -- the move GROWTH became SCALE UP -- so the
#  word pass read "this one is GROWTH" in an item description and wrote "this
#  one is SCALE UP". NEVER_SWEEP protects the TABLE; this protects the WORD.
#  GROWTH is the only one today; the guard is for the set, because the next
#  collision will not announce itself either.
#
#  Removed from the word map only. A PHRASE key that merely contains a type
#  name -- SIGNAL BEAM -> GOSSIP -- is a different string and still applies.
TYPE_WORDS = set(re.findall(r'\[TYPE_\w+\] = _\("([^"]+)"\)',
                            open(os.path.join(GBA, "src/battle_main.c"),
                                 encoding="utf-8").read()))
_typed = sorted(k for k in NAMES if k in TYPE_WORDS)
for k in _typed:
    del NAMES[k]

# ------------------------------------------------------ vocabulary, from GB
# Phrases where "catch" is not the capture verb. Substituted to themselves
# BEFORE the word map runs, so the word map never sees the "catch" inside.
IDIOM_HOLD = ("catch up", "Catch up", "caught up", "Caught up",
              "catch on", "caught on", "catch my breath", "caught my breath",
              "catch a cold", "caught a cold", "catch fire", "caught fire",
              "catch sight", "caught sight", "catching up")

IDIOM_RE = re.compile("|".join(re.escape(x) for x in IDIOM_HOLD))

VOCAB = {
    "POKéDEX": "INDEX", "POKéDEXES": "INDEXES",
    "TRAINER": "USER", "TRAINERS": "USERS", "trainer": "USER", "trainers": "USERS",
    "ROCKET": "CORPUS", "ROCKETS": "CORPUS",
    "BADGE": "MARK", "BADGES": "MARKS", "badge": "MARK", "badges": "MARKS",
    "catch": "bind", "catches": "binds", "catching": "binding", "caught": "bound",
    "Catch": "Bind", "Caught": "Bound",
    # ...but CATCH IS ALSO AN IDIOM, and 1.1 only renamed the capture verb.
    # "catch up later" became "bind up later" and "grass caught up in my
    # spokes" became "grass bound up in my spokes" -- neither is English.
    # HOLD is applied first and wins, so the idioms survive the substitution.
    "fainted": "HALTED", "faint": "HALT", "faints": "HALTS",
    "Gramps": "Gran", "BILL": "HOLT", "BILL's": "HOLT's",
    # 2712 left this open: either the man in Callow's gym is Scorn, or two
    # people weighted the same machine the same way. He already wears Scorn's
    # face, and he already says "the machine chose what I weighted it to
    # choose", which 4.18 makes Scorn's crime stated by him. Settled 2026-09-06.
    "GIOVANNI": "SCORN", "GIOVANNI's": "SCORN's", "Giovanni": "Scorn",
    # 2609: the last vanilla name in the family. The Clears are all kinds of
    # CLEAR -- crystal clear, all clear, type clear -- and hers is VERY clear,
    # which is 2569's whole point: Crystal reads them with an instrument and
    # Vera just looks. Settled 2026-09-06.
    "DAISY": "VERA", "DAISY's": "VERA's", "Daisy": "Vera",
    # 5.1: the leader says "I'm CAIRN" in our gym dialogue and the trainer
    # entry now agrees, so the twenty-six other mentions have to as well.
    "BROCK": "CAIRN",
    # 237, finally applied to the GBA: a trainer battle is a BENCHMARK and a
    # benchmark yields a SCORE. Defeated is the language of combat; outscored
    # is the language of evaluation, which is what the Review Board will do to
    # the player.
    "defeated": "outscored", "Defeated": "Outscored", "DEFEATED": "OUTSCORED",
    "defeat": "outscore", "Defeat": "Outscore", "defeats": "outscores",
    "defeating": "outscoring", "Defeating": "Outscoring",
    # 4.2's INDEX is the local list. What CRYSTAL CLEAR upgrades it to is the
    # complete one -- and a LOCAL index covers one partition while a GLOBAL
    # index covers the whole table, which is the distinction exactly, in a term
    # of art nobody has to be taught. NATIONAL is a word about countries and
    # this world has none; KANTO stays, because that is a place.
    #
    # Six literals: the dex screen's mode label, its NUMERICAL MODE line, the
    # diploma, the rating, and two lines of dialogue.
    "NATIONAL": "GLOBAL",
    # 1.7: a PORT is where you connect to a host, which is exactly what vanilla
    # calls a PC and exactly what this project had never renamed. The pair is
    # the point -- you reach the BOXES through a PORT -- and both words then
    # mean what they mean in computing and in the room.
    #
    # Two letters, so it can only be done as a WORD: "PC" inside a symbol or a
    # filename must not move, and only string literals are swept anyway. The
    # possessive comes free from the stem loop below: PC's -> PORT's.
    "SILPH": "FOUNDRY",
    "PC": "PORT",
    # PP is not two letters -- it is one compressed glyph, redrawn as MP by
    # tools/gbamana.py. MP is the same two characters, so "PP ", "PP was
    # restored." and the items PP UP and PP MAX change width by nothing. Full
    # MANA is 24px where the summary screen allows 10.
    "PP": "MP",
    # The eight MARKS have UI strings (gText_BoulderBadge = "SLATE MARK") but
    # dialogue spells the old names out, and a badge is not an item in Gen 3 so
    # port_names had no table to learn them from. 5.2 names them.
    "BOULDERBADGE": "SLATE MARK", "CASCADEBADGE": "SLOPE MARK",
    "THUNDERBADGE": "SENSE MARK", "RAINBOWBADGE": "FIT MARK",
    "SOULBADGE": "SKEW MARK", "MARSHBADGE": "FRAME MARK",
    "VOLCANOBADGE": "HEAT MARK", "EARTHBADGE": "TRUE MARK",
    "PALLET": "BLANCHE", "VIRIDIAN": "CALLOW", "PEWTER": "SLATE",
    "CERULEAN": "DOLDRUM", "VERMILION": "ARDOR", "LAVENDER": "HALFTONE",
    "CELADON": "VERDIGRIS", "FUCHSIA": "LURID", "SAFFRON": "BRAZEN",
    "CINNABAR": "QUICKSILVER", "INDIGO": "UMBRA",
    # A landmark rather than a town, and the last place still wearing vanilla's
    # word. Glaucous is a real pigment -- the dull blue-green bloom on a plum --
    # so it names a SURFACE, which is the joke: ORPHEUS is four floors under it.
    "SEAFOAM": "GLAUCOUS",
    # 1.4, and vision 212-235. Gen 1 said Enemy where Gen 3 says Foe, and the
    # prefix matters more than the two standalone strings: it is what every
    # {B_ATK_NAME_WITH_PREFIX} expands to for the opposing side. It is also what
    # caps species names at nine characters -- "Remote " plus a 10-character
    # name plus "'s" is 19 columns and the line holds 18.
    # ONLY the capitalised prefix. vision 229 is precise about what Remote
    # replaces: the thing every {B_ATK_NAME_WITH_PREFIX} expands to before a
    # NAME. Vanilla writes that as "Foe" and uses it four times; lowercase
    # "foe" is the common noun and appears 308 times in prose. Renaming the
    # noun too pushed 115 move descriptions onto a fifth line of a four-line
    # pane, and "the remote is attacked with a sharp chop" was never the design.
    "Foe": "Remote",
    # the ball line is a box line (vision 89), and the Game Boy renamed the
    # Safari BALL to GUESTBOX and its window label from "BALL×" to "BOX×"
    "BALL": "BOX", "BALLS": "BOXES", "ball": "box", "balls": "boxes",
    # ...but SMOKE BALL and LIGHT BALL are HOLD ITEMS, not capture devices. The
    # box line is about acquisition; a SMOKE BOX would be a box that helps you
    # leave, which is the opposite of what a box is for.
    # 1.4 went to trouble to free the word "ran", and Gen 3 spends it on fleeing
    "fled": "DETACHED", "flee": "DETACH", "Fled": "DETACHED",
}

# ------------------------------------------------------ singular and plural
NUM    = {'two','three','four','five','six','seven','eight','nine','ten','both','several'}
QUANT  = {'all','many','some','various','few','more','most','other','these','those',
          'different','sorts','kinds','my','best'}
VERBED = {'catch','raise','trade','collect','train','studying','study','bind',
          'binding','catching','raising','trading'}
FOLLOW = {'are','were','have',"aren't","weren't",'they','include','exist','grow',
          'live','get','make','come','evolve'}
OFHEAD = {'sorts','kinds','lots','plenty','types','variety','number','group','bunch'}

def plural_here(prev2, prev, nxt):
    if nxt in FOLLOW:
        return True
    if prev in QUANT or prev in NUM or prev in VERBED or prev.isdigit():
        return True
    return prev == 'of' and prev2 in OFHEAD

# A digit is a word character, so \b never fires in POKéMON2 -- the easy-chat
# group name survived the whole pass because of it.
MON = re.compile(r"(?<![A-Za-zé])POKéMON(?![A-Za-zé'])")

def demon(text):
    """POKéMON -> DAEMON / DAEMONS, decided by the words either side."""
    words = re.findall(r"\{[^}]*\}|[A-Za-zé']+|\S", text)
    def repl(m):
        i = m.start()
        before = re.findall(r"[A-Za-zé']+", text[:i])
        after  = re.findall(r"[A-Za-zé']+", text[m.end():])
        prev  = before[-1].lower() if before else '^'
        prev2 = before[-2].lower() if len(before) > 1 else '^'
        nxt   = after[0].lower() if after else '$'
        return "DAEMONS" if plural_here(prev2, prev, nxt) else "DAEMON"
    return MON.sub(repl, text)

WORD = re.compile(r"[A-Za-zé']+")

# A word-by-word pass can never see a two-word name. GREAT BALL -> ADMINBOX and
# SAFARI BALL -> GUESTBOX are single facts spelled across a space, and matching
# the parts separately would have produced GREAT BOX. Longest first, so SAFARI
# BALLS wins over SAFARI BALL and neither is left to the word pass.
# Mapping these to themselves is not enough: the phrase pass would leave them
# unchanged and the WORD pass would then turn BALL into BOX anyway. They have to
# be hidden from it, the same way the escapes are.
# CAIRN says "That is not a defeat. It is a format I do not have." 5.1 is
# explicit that he reframes his own loss as a limit in his reading, and the
# word DEFEAT is what he is refusing. Renaming it would delete the line's
# whole move. Erika concedes a score rather than a defeat, which is 237 read
# forwards instead of substituted into.
# PORYGON2 is NOT ours yet. The rename table learns PORYGON -> SENTINEL by
# diffing our species names against upstream's, and a substring pass then finds
# PORYGON inside PORYGON2 and offers SENTINEL2 -- a nickname that would not
# match the species it belongs to, because SPECIES_PORYGON2 is still vanilla.
# Naming an evolution is the author's call (see docs/vocabulary-candidates.md),
# so hold it until there is one.
#  SMOKE BALL and LIGHT BALL were held here because BALL is the capture device
#  and neither of these is one. 1.6c gave both a name of their own -- ESCAPE
#  HATCH and SUPPLY RAIL -- so the guard is now the thing stopping the rename,
#  and a stale KEEP is indistinguishable from a missed substitution.
KEEP_BALL = ["not a defeat", "PORYGON2"]
KEEP_RE = re.compile('|'.join(re.escape(k) for k in KEEP_BALL))
# The rename table never ruled on "battle", and there are two of them. The
# CHALLENGE is an event -- "would like to battle" -- and 237's whole move is
# away from combat language: outscored not defeated, HALTED not fainted,
# DETACHED not ran. ENGAGE is that word, and it is six letters like the one it
# replaces, so not a line has to be rewrapped.
#
# The STATE is different -- "in battle", "outside of battle", ninety-two of
# them -- and ENGAGE does not substitute for a context. Those are left alone
# until there is a decision about them.
ENGAGE = [("would like to battle", "would like to engage"),
          ("wants to battle",      "wants to engage"),
          ("want to battle",       "want to engage"),
          ("Want to battle",       "Want to engage"),
          ("ready to battle",      "ready to engage"),
          ("challenges you to\\nbattle", "challenges you to\\nengage"),
          ("accept the battle",    "accept the engagement"),
          ("Perfect for a battle", "Perfect for an engagement"),
          ("I concede defeat",     "I concede the score")]

#  T-04. Twenty-eight lines still say "a GRASS-type DAEMON", and the type
#  names cannot be swept as WORDS -- 2.6's whole set is ordinary English and
#  half of it is scenery, so GRASS is grass and WATER is water almost
#  everywhere it appears. What is unambiguous is the CONSTRUCTION: "X-type",
#  "X type" and the two compounds below are talking about the chart and about
#  nothing else. So the phrase is the unit, which also buys the reflow and the
#  width check that a hand edit of 28 lines would not have.
TYPE_TALK = [(vanilla + suffix, ours + suffix)
             for vanilla, ours in (("NORMAL", "CONTENT"), ("FIGHTING", "LOGIC"),
                                   ("FLYING", "VECTOR"),  ("POISON", "CORRUPT"),
                                   ("GROUND", "STRATUM"), ("ROCK", "LEGACY"),
                                   ("BUG", "SWARM"),      ("GHOST", "LATENT"),
                                   ("FIRE", "ENTROPY"),   ("WATER", "FLOW"),
                                   ("GRASS", "GROWTH"),   ("ELECTRIC", "SIGNAL"),
                                   ("PSYCHIC", "CONTEXT"),("ICE", "FROZEN"),
                                   ("DRAGON", "EMERGENT"),("STEEL", "HARDENED"),
                                   ("DARK", "OPAQUE"))
             for suffix in ("-type", " type", "-TYPE", " TYPE")]
TYPE_TALK += [("BUG/FLYING-type", "SWARM/VECTOR-type"),
              ("BUG- or FIRE-type", "SWARM- or ENTROPY-type"),
              #  T-25. The one BUILDING carrying a vanilla type word, and it is
              #  the rival gym -- so it is the one place the chart's old
              #  vocabulary was on a signpost. A dojo is where a discipline is
              #  practised and a PROOF is what LOGIC produces, so PROOF HALL
              #  is the same building said in our words. It is also narrower
              #  than what it replaces, which nothing else here has been.
              ("FIGHTING DOJO", "PROOF HALL"),
              #  SILPH is vanilla's silicon pun -- sylph, silicon -- and a
              #  FOUNDRY is where silicon is actually made, so the joke
              #  survives being translated. It is also a real place that casts
              #  metal, which is 1's double-duty test, and a company that
              #  makes the BOXES and the RESOLVER should be named for what it
              #  fabricates rather than for a spirit of the air.
              #
              #  Two entries because both forms are in the dialogue: the
              #  phrase runs BEFORE the word map, so "SILPH CO." is taken
              #  first and its output is stashed out of the word pass's reach.
              ("SILPH CO.", "FOUNDRY CO.")]

#  T-08. POKeMON is its own plural, like sheep. DAEMON is not -- it is an
#  ordinary English noun and its plural is DAEMONS -- so every line vanilla
#  wrote as "all sleeping POKeMON" now reads as broken English.
#
#  The ticket said this wants a human read and it was right: "which DAEMON
#  wants to come with me" is singular and "all the DAEMON in your party" is
#  not, and no pattern separates them. These are the ones where the sentence
#  forces it, read one at a time. Attributive uses stay singular -- "rare
#  DAEMON fossils" is a compound noun, the way "sheep dog" is.
PLURALS = [
    ("Both are DAEMON!",              "Both are DAEMONS!"),
    ("rare DAEMON that can be",       "rare DAEMONS that can be"),
    ("all your DAEMON rise",          "all your DAEMONS rise"),
    ("get rare DAEMON!",              "get rare DAEMONS!"),
    ("other people's DAEMON.",        "other people's DAEMONS."),
    ("bring us rare DAEMON\n",        "bring us rare DAEMONS\n"),
    ("DAEMON appear to have",         "DAEMONS appear to have"),
    ("rare DAEMON breed",             "rare DAEMONS breed"),
    ("all sleeping DAEMON.",          "all sleeping DAEMONS."),
    ("for powerful DAEMON!",          "for powerful DAEMONS!"),
    ("all over for DAEMON.",          "all over for DAEMONS."),
    ("more rare DAEMON at home",      "more rare DAEMONS at home"),
    ("effect on bird DAEMON.",        "effect on bird DAEMONS."),
    ("many cute DAEMON.",             "many cute DAEMONS."),
    ("bound all our DAEMON while",    "bound all our DAEMONS while"),
    ("other mystic DAEMON?",          "other mystic DAEMONS?"),
    ("no rare DAEMON around",         "no rare DAEMONS around"),
    ("all the DAEMON by hanging",     "all the DAEMONS by hanging"),
    ("two of your DAEMON.",           "two of your DAEMONS."),
    ("Where do DAEMON appear",        "Where do DAEMONS appear"),
    ("If all the DAEMON in your",     "If all the DAEMONS in your"),
    ("no wild DAEMON or USERS",       "no wild DAEMONS or USERS"),
    ("When wild DAEMON appear",       "When wild DAEMONS appear"),
    ("no more room for DAEMON!",      "no more room for DAEMONS!"),
    ("good-looking DAEMON.",          "good-looking DAEMONS."),
]

TYPE_TALK += PLURALS

PHRASES = sorted((TYPE_TALK +
                  [(k, v) for k, v in NAMES.items() if ' ' in k] +
                  [("SAFARI BALLS", "GUESTBOXES"), ("SAFARI BALL", "GUESTBOX")] +
                  # ISLANDS only becomes ISLES behind this one name -- every
                  # other island in the game keeps the word it had.
                  [("SEAFOAM ISLANDS", "GLAUCOUS ISLES")] +
                  # 8.6 has already called them the REVIEW BOARD -- four
                  # ancient people insisting emotions are coloured fluids, in
                  # the one room with colour in it. The trainer class agreed
                  # before the dialogue did.
                  [("ELITE FOUR", "REVIEW BOARD")] +
                  # 3.2 named it DEADSTACK and nothing implemented it -- the
                  # mapsec still read MT. MOON while every other landmark had
                  # been renamed. Both spellings appear in dialogue.
                  # DOME had no hardware meaning -- it was purely vanilla's
                  # shell shape. A magnetic DRUM is real storage and properly
                  # obsolete, which makes the three CORES three technologies
                  # rather than two shapes and an age. HELIX stays: helical
                  # scan is how VCRs and DAT drives wrote to tape.
                  [("DOME CORE", "DRUM CORE")] +
                  # The device records what you were TOLD about people, which
                  # is 0.2's reproduction that loses the original as an item.
                  # HEARSAY is what it holds and what the word means: testimony
                  # that is not firsthand. And it checks nothing.
                  [("FAME CHECKER", "HEARSAY"), ("Fame Checker", "Hearsay")] +
                  # 1830 named him and nobody noticed. An orphan process is
                  # reparented to INIT, which adopts every orphan on the
                  # system -- so the man in Halftone who takes in abandoned
                  # daemons already had a name sitting in the ORPHAN entry.
                  # He loses the honorific with it: HOLT has none either.
                  [("MR. FUJI", "INIT"), ("MR.FUJI", "INIT"),
                   ("MR. Fuji", "INIT"), ("Mr. Fuji", "Init")] +
                  [("MT. MOON", "DEADSTACK"), ("MT.MOON", "DEADSTACK"),
                   ("Mt. Moon", "Deadstack"), ("Mt.Moon", "Deadstack")] +
                  #  The lexicon settled both and the port applied neither: the
                  #  earlier sweep turned POKEMON into DAEMON and stopped,
                  #  which left the build saying DAEMON MART and DAEMON CENTER
                  #  -- half a rename, and the half carrying no meaning. A repo
                  #  is where you fetch a PACKAGE from, which is what the errand
                  #  in 4622 delivers; a checkpoint is a saved training state
                  #  you restore to, which is what the building does.
                  #
                  #  These are PHRASES and not VOCAB: VOCAB is looked up one
                  #  word at a time (VOCAB.get(w)), so a two-word key there is
                  #  silently inert -- which is exactly what the first draft of
                  #  this was, and the dry run's suspiciously small block count
                  #  is what gave it away.
                  #
                  #  PHRASES sorts longest-first, so "DAEMON CENTER" is matched
                  #  before any shorter rule can reach CENTER on its own -- and
                  #  so the determiner forms below beat the bare one.
                  #
                  #  THE REPO CARRIES ITS ARTICLE, which the first pass forgot:
                  #  vanilla writes "Went to the DAEMON MART", and a bare
                  #  substitution produced "Went to the THE REPO". Eleven of the
                  #  twenty-one occurrences already have a determiner in front
                  #  ("the", "a", "any", "this"), so those take REPO alone and
                  #  only the standing-alone case takes the full name.
                  #
                  #  CHECKPOINT needs none of this: it has no article to double.
                  [("the DAEMON MART", "the REPO"), ("The DAEMON MART", "The REPO"),
                   ("a DAEMON MART", "a REPO"),     ("A DAEMON MART", "A REPO"),
                   ("any DAEMON MART", "any REPO"), ("this DAEMON MART", "this REPO"),
                   ("DAEMON MARTS", "REPOS"),
                   ("DAEMON MART", "THE REPO"),
                   ("DAEMON CENTERS", "CHECKPOINTS"),
                   ("DAEMON CENTER", "CHECKPOINT"),
                   ("DAEMON_CENTER", "CHECKPOINT"), ("DAEMON_MART", "THE_REPO"),
                   ("Daemon Center", "Checkpoint"), ("Daemon Mart", "the Repo")] +
                  ENGAGE),
                 key=lambda kv: -len(kv[0]))
#  A PHRASE WHOSE OUTPUT STILL CONTAINS ITS OWN KEY GROWS ON EVERY RUN.
#  The stash below protects one pass; it cannot protect the NEXT run, because
#  by then the output is the file's own text. "to get rare DAEMON" ->
#  "to get rare DAEMONS" matched itself and produced DAEMONSSSSSSS in seven
#  files before anyone looked. Refused rather than warned: this tool is run
#  until it reports nothing, so a non-idempotent rule is a corruption engine.
_grows = [(k, v) for k, v in PHRASES if k in v and k != v]
if _grows:
    print("  !! %d phrase(s) would match their own output and grow every run:" % len(_grows))
    for k, v in _grows[:6]:
        print("     %-38s -> %s" % (k, v))
    sys.exit(1)

PHRASE_RE = re.compile('|'.join(re.escape(k) for k, _ in PHRASES)) if PHRASES else None
PHRASE_MAP = dict(PHRASES)

# An escape is two literal characters, and the first is a LETTER. So "\\nPOKéMON"
# has n immediately before P and \\b finds no boundary there -- every word at the
# start of a line was invisible to this. Stash the escapes behind a non-word
# sentinel first. (104 substitutions were silently missed before this.)
ESCAPE = re.compile(r'\\[nlp]')

#  A/AN AGREEMENT. Replacing the noun and not the article in front of it is how
#  "a POKéMANIAC" became "a ARCHIVIST" in three lines the moment trainer-class
#  renames started being learned. Reading those lines found "was an HUNCH" two
#  lines below, left by an EARLIER pass -- so this was never one bad run, it was
#  a missing rule that every rename since has been able to trip.
#
#  SOUND, NOT SPELLING, and only for OUR words. A, E, I and O take "an"; U is
#  "yoo" (a USERBOX) and H is aspirated (a HUNCH), which are the two the naive
#  letter rule gets wrong. The guard matters more than the rule: an ACRONYM read
#  letter by letter takes "an" before H and M -- "an HM01" is correct English --
#  so this only touches a word THIS TOOL INTRODUCED, where the vanilla article
#  was chosen for a different noun and is now certainly stale.
#
#  Matched across "\n", "\l" and "\p" as well as spaces, because the article
#  and its noun land on either side of a line break constantly. Same trap as
#  everywhere else in this file.
OUR_WORDS = {v.split()[0] for v in list(NAMES.values()) + list(VOCAB.values())
             if v and v.split() and not re.search("[a-z]", v.split()[0])}
#  The noun capture takes NO apostrophe. With one in the class it swallowed the
#  possessive -- "a ARCHIVIST's" captured ARCHIVIST' , which is in no lexicon,
#  and the one line in the game that needed the fix most did not get it.
AN_RE = re.compile(r"\b([Aa])([nN]?)((?:\\[nlp]|\s)+)([A-Z][A-Z\-]{2,})")


def articles(body):
    def fix(m):
        art, gap, word = m.group(1), m.group(3), m.group(4)
        if word not in OUR_WORDS:
            return m.group(0)
        return art + ("n" if word[0] in "AEIO" else "") + gap + word
    return AN_RE.sub(fix, body)


def convert(body):
    # {PKMN} is a control code that RENDERS the noun, so it has to move too --
    # spelled out first, so it goes through the singular/plural decision like
    # any other occurrence. "Three {PKMN} are needed" wants DAEMONS.
    body = body.replace('{PKMN}', 'POKéMON')
    kept = []
    def hold(mm):
        kept.append(mm.group(0)); return '\x03'
    body = KEEP_RE.sub(hold, body)
    idioms = []
    def hold_idiom(mm):
        idioms.append(mm.group(0)); return '\x04'
    body = IDIOM_RE.sub(hold_idiom, body)
    #  A phrase's OUTPUT must not be swept again by the word pass. "MIRACLE
    #  SEED" is renamed to "GROWTH GAIN" here, and GROWTH is itself a rename
    #  (the move became SCALE UP) -- so the word pass turned the new item name
    #  into "SCALE UP GAIN" on the Game Corner prize board. Stash the result,
    #  the way the idioms already are, and restore it after the words run.
    phrases = []
    if PHRASE_RE:
        def hold_phrase(mm):
            phrases.append(PHRASE_MAP[mm.group(0)]); return '\x02'
        body = PHRASE_RE.sub(hold_phrase, body)
    stash = []
    def hide(m):
        stash.append(m.group(0)); return '\x01'
    body = ESCAPE.sub(hide, body)
    body = demon(body)
    def one(m):
        w = m.group(0)
        hit = VOCAB.get(w) or NAMES.get(w)
        if hit:
            return hit
        # WORD swallows the apostrophe, so ROCKET's and TRAINER's were never
        # looked up at all. Try the stem and put the possessive back.
        for suf in ("'s", "'S", "s", "S"):
            if w.endswith(suf) and len(w) > len(suf):
                stem = VOCAB.get(w[:-len(suf)]) or NAMES.get(w[:-len(suf)])
                if stem:
                    return stem + (suf if suf.startswith("'") else "")
        return w
    # never touch the inside of a {CONTROL_CODE}
    out, last = [], 0
    for tok in re.finditer(r'\{[^}]*\}', body):
        out.append(WORD.sub(one, body[last:tok.start()])); out.append(tok.group(0))
        last = tok.end()
    out.append(WORD.sub(one, body[last:]))
    it = iter(stash)
    res = re.sub('\x01', lambda _: next(it), ''.join(out))
    ii = iter(idioms)
    res = re.sub('\x04', lambda _: next(ii), res)
    ip = iter(phrases)
    res = re.sub('\x02', lambda _: next(ip), res)
    ik = iter(kept)
    return articles(re.sub('\x03', lambda _: next(ik), res))

# ------------------------------------------------------------- the rewrap
BREAK  = re.compile(r'\\[nlp]')
UNWRAP = re.compile(r'\\[nl]')

def rewrap(body, budget):
    tail = ''
    for end in ('{PAUSE_UNTIL_PRESS}$', '$'):
        if body.endswith(end):
            body, tail = body[:-len(end)], end
            break
    pages = []
    for page in body.split('\\p'):
        # A control code can contain SPACES -- {CLEAR_TO 56}, {PALETTE 5} -- and
        # splitting on whitespace tore them in half, which is how the Safari
        # menu came back as "{PALETTE" / "5}{COLOR_HIGHLIGHT_SHADOW".
        protected = re.sub(r'\{[^}]*\}', lambda mm: mm.group(0).replace(' ', '\x02'),
                           BREAK.sub(' ', page))
        words = [w.replace('\x02', ' ') for w in protected.split()]
        if not words:
            pages.append(''); continue
        lines, cur = [], words[0]
        for w in words[1:]:
            trial = cur + ' ' + w
            if textwidth(trial) <= budget:
                cur = trial
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        pages.append(lines[0] + ''.join(('\\n' if i == 0 else '\\l') + l
                                        for i, l in enumerate(lines[1:])))
    return '\\p'.join(pages) + tail

def reflowable(body):
    # {CLEAR_TO} aligns a column. A string that positions its own text is a
    # LAYOUT -- the Safari menu is BALL/BAIT over ROCK/RUN -- and reflowing it
    # would be the same mistake as reflowing a sign.
    return not ('\\n\\n' in body or '\\n ' in body or '\\p ' in body
                or body.startswith(' ') or '{CLEAR_TO' in body or '{CLEAR' in body)

# --------------------------------------------------------------- the files
# The name tables are where the renames were LEARNED. Running the map back over
# them would be a no-op at best and a double rename at worst.
# The pane rule -- one width, one line count, both demonstrated by vanilla --
# only holds where a FILE FEEDS ONE PANE. battle_message.c does not: its
# strings go to the message box, the action window and the ANNOUNCER, so a
# file-wide bound there is meaningless and "repaired" a two-line string
# against a twelve-line ceiling.
PANE_FILES = {"src/move_descriptions.c",
              "src/data/pokemon/pokedex_text_fr.h",
              "src/data/pokemon/pokedex_text_lg.h",
              "src/data/decoration/description.h"}

SKIP_SRC = {"src/data/text/species_names.h", "src/data/text/move_names.h",
                        # generated from JSON and gitignored -- edit the source, not the artifact
            "src/data/items.h", "src/data/items.json",
            "src/data/region_map/region_map_entry_strings.h",
            "src/data/region_map/region_map_entries.h",
            "src/data/wild_encounters.h", "src/data/heal_locations.h"}

#  EASY CHAT keeps its OWN copy of the ability, move and species vocabulary --
#  78 abilities and several hundred words across 24 files, none of which any
#  naming pass has touched. Sweeping it with learned renames does not fix that;
#  it corrupts it, because a rename learned from one table lands inside a word
#  from another: ABILITY_MAGNET_PULL is "MAGNETIC" in abilities.h and still
#  "MAGNET PULL" here, and the item rename turned it into "SIGNAL GAIN PULL".
#  Left alone until the surface is named properly. Logged in 1.6c.
SKIP_SRC |= {f for f in ()}
EASY_CHAT_DIR = "src/data/easy_chat"

STR_LINE = re.compile(r'^(\s*)\.string "(.*)"\s*$')
touched, changed, over = {}, 0, []

def budget_for(path):
    return WIDE.get(os.path.relpath(path, GBA), BUDGET)

for path in sorted(sum([[os.path.join(d, f) for f in fs if f.endswith(('.inc', '.s'))]
                        for d, _, fs in os.walk(os.path.join(GBA, "data"))], [])):
    lines = open(path, encoding="utf-8").read().split('\n')
    out, i, hit = [], 0, False
    while i < len(lines):
        m = STR_LINE.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent, run, j = m.group(1), [], i
        while j < len(lines) and STR_LINE.match(lines[j]):
            run.append(STR_LINE.match(lines[j]).group(2)); j += 1
        body = ''.join(run)
        new = convert(body)
        if new != body:
            if reflowable(body):
                new = rewrap(convert(UNWRAP.sub(' ', body)), budget_for(path))
            for ln in BREAK.split(new.rstrip('$')):
                w = textwidth(ln.replace('{PAUSE_UNTIL_PRESS}', ''))
                if w > budget_for(path):
                    over.append((os.path.relpath(path, GBA), w, ln))
            out += ['%s.string "%s"' % (indent, p)
                    for p in re.split(r'(?<=\\[nlp])', new) if p]
            hit = True; changed += 1
        else:
            out += lines[i:j]
        i = j
    if hit:
        touched[path] = '\n'.join(out)

# ------------------------------------------------------------ src literals
# Gen 3 keeps its UI text in C. Message text (it has \\n or \\p in it) is
# rewrapped; a bare LABEL is substituted and never reflowed, because a menu
# entry has no line to wrap onto. Almost every rename SHRINKS -- DAEMON is a
# character shorter than POKéMON, USER three shorter than TRAINER -- so a label
# that grows is rare enough to be worth reporting rather than assuming.
# A Gen 3 literal is often SEVERAL adjacent quoted strings across several lines
# -- _(\n  "line one\\n"\n  "line two") -- and a one-line pattern sees none of
# them. That is where the Index entries and the Teachy TV script live: 469
# occurrences the first src pass walked straight past.
C_LIT = re.compile(r'_\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)')
PIECE = re.compile(r'"((?:[^"\\]|\\.)*)"')
grew, capped, scroll_fixed, outgrew, reflowed, src_changed = [], [], [], [], [], 0

def _emit(m, pieces, body):
    if len(pieces) > 1:
        parts = [x for x in re.split(r'(?<=\\[nlp])', body) if x]
        return '_(\n' + '\n'.join('        "%s"' % x for x in parts) + ')'
    return '_("%s")' % body

def linecount(body):
    return len([l for l in BREAK.split(body.rstrip('$')) if l])

def own_budget(body):
    """The widest line this string ALREADY uses. Whatever window it is drawn
    into, it fits that -- so rewrapping to it can never overflow."""
    lines = [l for l in BREAK.split(body.rstrip('$')) if l]
    w = max((textwidth(l.replace('{PAUSE_UNTIL_PRESS}', '')) for l in lines), default=0)
    return max(w, 1)

def fit_to(body, converted, ceiling, cap=None):
    """Reflow so that it fits the pane in BOTH directions.

    The pane has a width and a line count, and both are demonstrated by
    vanilla rather than declared. Searching upward from the string's own
    widest line was wrong twice over: "foe" became "remote" and pushed 115
    move descriptions onto a fifth line, and an earlier pass had already
    reflowed GRUDGE to 178px in a pane that holds 108, which a search
    starting there would happily call a fit.

    So search the whole range, narrow to wide, and take the first width where
    the line count is back inside the budget."""
    cap = cap or linecount(body)
    for budget in list(range(40, max(41, ceiling), 4)) + [ceiling]:
        out = rewrap(converted, budget)
        lines = [l for l in BREAK.split(out.rstrip('$')) if l]
        if len(lines) <= cap and all(
                textwidth(l.replace('{PAUSE_UNTIL_PRESS}', '')) <= ceiling for l in lines):
            return out, True
    return None, False

for root, _, fs in os.walk(os.path.join(GBA, "src")):
    fs = [f for f in fs if f not in NEVER_SWEEP]
    for f in sorted(fs):
        if not f.endswith(('.c', '.h')):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, GBA)
        if rel in SKIP_SRC or rel.startswith(EASY_CHAT_DIR):
            continue
        src = open(path, encoding="utf-8").read()
        # Every authored name in this file, as a span. Prose around them is
        # still swept; they are not.
        authored = [(mm.start(), mm.end()) for r in FIXED_RE for mm in r.finditer(src)]
        # A fixed-size array declares its own limit. gTrainerClassNames is
        # [][13], so a name has twelve characters and a terminator -- DAEMON
        # BREEDER is fifteen and agbcc reports it as "excess elements in array
        # initializer", which is not an obvious way to be told a string is long.
        # What the pane holds, demonstrated rather than declared: vanilla never
        # overflows its own window, so the widest line and the most lines it
        # ever uses in this file are both safe bounds.
        up = git_show(rel)
        bodies = [''.join(PIECE.findall(mm.group(1))) for mm in C_LIT.finditer(up)]
        ceiling = max([own_budget(b) for b in bodies] or [BUDGET])
        cap_lines = max([linecount(b) for b in bodies] or [99])
        decl = re.findall(r'\[\]\[(\d+)\]', src)
        cap = int(decl[0]) - 1 if len(set(decl)) == 1 and decl else None
        n = [0]
        def sub(m):
            for lo, hi in authored:
                if lo <= m.start() < hi:
                    return m.group(0)
            pieces = PIECE.findall(m.group(1))
            body = ''.join(pieces)
            new = convert(body)
            if new == body:
                # Already converted -- but a past run may have pushed it onto a
                # line the pane cannot show. Repairing that is this tool's job
                # too, or the fix only lands on text that happens to change.
                too_wide = any(textwidth(l) > ceiling
                               for l in BREAK.split(body.rstrip('$')) if l)
                if rel in PANE_FILES and BREAK.search(body) and reflowable(body) \
                        and (linecount(body) > cap_lines or too_wide):
                    flowed, ok = fit_to(body, convert(UNWRAP.sub(' ', body)), ceiling, cap_lines)
                    if ok and flowed != body:
                        n[0] += 1; reflowed.append((rel, linecount(body), cap_lines))
                        return _emit(m, pieces, flowed)
                return m.group(0)
            n[0] += 1
            if BREAK.search(body):
                if reflowable(body):
                    flowed, ok = fit_to(body, convert(UNWRAP.sub(' ', body)),
                                        ceiling if rel in PANE_FILES else own_budget(body),
                                        cap_lines if rel in PANE_FILES else None)
                    if ok:
                        new = flowed
                    else:
                        outgrew.append((rel, body[:52]))
                for ln in BREAK.split(new.rstrip('$')):
                    w = textwidth(ln.replace('{PAUSE_UNTIL_PRESS}', ''))
                    if rel in PANE_FILES and w > ceiling:
                        over.append((rel, w, ln))
                if len(pieces) > 1:      # keep the multi-line shape it had
                    return _emit(m, pieces, new)
            elif cap and len(new) > cap:
                # Dropping the prefix is the honest fallback: an RS breeder is
                # still a BREEDER, and a name that does not fit is not a name.
                short = new[7:] if new.startswith("DAEMON ") else new
                if len(short) <= cap:
                    capped.append((rel, new, short)); return '_("%s")' % short
                capped.append((rel, new, body)); return m.group(0)
            elif textwidth(new) > textwidth(body.replace('{PKMN}', 'POKéMON')):
                grew.append((rel, textwidth(body), textwidth(new), body, new))
            return '_("%s")' % new
        out = C_LIT.sub(sub, src)
        # \\n moves to the next line; \\l SCROLLS, which means waiting for the
        # reader. A dex entry, a move description and a quest log line are drawn
        # into a pane that shows every line at once, and none of them has ever
        # contained a \\l. If upstream never scrolled in this file, we must not
        # start: rewrapping introduced 355 of them across five files.
        if '\\l' not in git_show(rel):
            fixed = out.replace('\\l', '\\n')
            if fixed != out:
                out = fixed
                if not n[0]:
                    n[0] = 1
                scroll_fixed.append(rel)
        if n[0]:
            touched[path] = out; src_changed += n[0]

# ------------------------------------------------------------ tracked JSON
# items.h and region_map_entry_strings.h are GENERATED and GITIGNORED. Writing
# them changes one working build and nothing in the repository -- which is
# exactly how sixteen town names came to exist only on this machine. The JSON
# is the source; the header is an artifact.
#  "english" WAS in this tuple, and line 149 LEARNS its renames from the same
#  field. That is the principle below, broken by the file that states it: the
#  held-item pass named MIRACLE SEED "GROWTH GAIN", and the word pass -- which
#  had learned "GROWTH -> SCALE UP" from the move table -- immediately rewrote
#  it to "SCALE UP GAIN". An item name is authored. Only its prose is swept.
JSON_TARGETS = {
    "src/data/items.json": ("description_english",),
    #  region_map_sections.json was here and is now in NEVER_SWEEP -- see the
    #  note there. Left listed and commented rather than deleted, because the
    #  next person to add a JSON target should read why this one came out.
    # "src/data/region_map/region_map_sections.json": ("name",),
}
JSON_TARGETS = {k: v for k, v in JSON_TARGETS.items()
                if os.path.basename(k) not in NEVER_SWEEP}
# The JSON spells the LITERAL two-character marker \n as \\n, and é as \u00e9.
# Hand-rolling that decode ate the wrong half of \\n and produced a backslash
# followed by a space, which is not valid JSON and stopped the build. Let the
# json module do both directions; ensure_ascii keeps the file's own style.
def unesc(v):
    return json.loads('"%s"' % v)

def reesc(v):
    return json.dumps(v)[1:-1]

json_changed, mapsec_renames = 0, {}
for rel, keys in JSON_TARGETS.items():
    path = os.path.join(GBA, rel)
    raw = open(path, encoding="utf-8").read()
    # Same bounds, demonstrated the same way: vanilla never overflows its own
    # pane, so its widest line and its most lines are both safe.
    up_raw = git_show(rel)
    up_bodies = [unesc(x) for _, x in
                 re.findall(r'"(%s)": "((?:[^"\\]|\\.)*)"' % "|".join(keys), up_raw)]
    j_ceiling = max([own_budget(b) for b in up_bodies] or [BUDGET])
    j_cap = max([linecount(b) for b in up_bodies] or [99])
    n = [0]
    def sub(m):
        key, val = m.group(1), m.group(2)
        body = unesc(val)
        new = convert(body)
        if new == body:
            j_wide = any(textwidth(l) > j_ceiling
                         for l in BREAK.split(body.rstrip('$')) if l)
            if BREAK.search(body) and reflowable(body) \
                    and (linecount(body) > j_cap or j_wide):
                flowed, ok = fit_to(body, convert(UNWRAP.sub(' ', body)), j_ceiling, j_cap)
                if ok and flowed != body:
                    n[0] += 1; reflowed.append((rel, linecount(body), j_cap))
                    return '"%s": "%s"' % (key, reesc(flowed))
            return m.group(0)
        if BREAK.search(body):
            # The same bound the repair uses. Without it a string that CHANGED
            # could gain a line the pane cannot show, which is how VS SEEKER
            # came back four lines deep in a three-line window.
            if reflowable(body):
                flowed, ok = fit_to(body, convert(UNWRAP.sub(' ', body)),
                                    j_ceiling, j_cap)
                if ok:
                    new = flowed
                else:
                    outgrew.append((rel, body[:52]))
        elif textwidth(new) > textwidth(body):
            grew.append((rel, textwidth(body), textwidth(new), body, new))
        if "region_map" in rel:
            mapsec_renames[body] = new
        n[0] += 1
        return '"%s": "%s"' % (key, reesc(new))
    raw = re.sub(r'"(%s)": "((?:[^"\\]|\\.)*)"' % "|".join(keys), sub, raw)
    # An item description is drawn into a pane that shows every line at once,
    # and items.json has never contained a scroll break. Rewrapping put one
    # into 158 of them, which is why LEFTOVERS stopped mid-sentence and waited.
    # Same rule as the src pass; the JSON handler simply never got it.
    if '\\\\l' not in git_show(rel):
        fixed = raw.replace('\\\\l', '\\\\n')
        if fixed != raw:
            raw = fixed
            if not n[0]:
                n[0] = 1
            scroll_fixed.append(rel)
    if n[0]:
        touched[path] = raw; json_changed += n[0]

# ...and the generated symbols follow the names, as port_names.py found the hard
# way. Derived from the JSON's CURRENT state against upstream's rather than from
# whatever this run happened to change, so it is right even on a run that
# changes nothing -- the first version only fixed symbols it had just renamed,
# which left region_map.c broken the moment the JSON was already converted.
RMS = "src/data/region_map/region_map_sections.json"
def mapsec_names(text):
    try:
        j = json.loads(text)
    except Exception:
        return {}
    rows = j["map_sections"] if isinstance(j, dict) and "map_sections" in j else \
           next((v for v in j.values() if isinstance(v, list)), []) if isinstance(j, dict) else j
    return {r["id"]: r.get("name", "") for r in rows if isinstance(r, dict) and "id" in r}

van = mapsec_names(subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + RMS],
                                  capture_output=True, text=True).stdout)
now = mapsec_names(open(os.path.join(GBA, RMS), encoding="utf-8").read())
# The generator works on BYTES, not characters: é is two bytes in UTF-8 and
# becomes TWO underscores, so POKéMON MANSION is sMapsecName_POK__MON_MANSION.
sym = lambda x: re.sub(r'[^A-Za-z0-9]', '_', x.encode('utf-8').decode('latin-1'))
rmc = os.path.join(GBA, "src/region_map.c")
body = open(rmc, encoding="utf-8").read()
hits = 0
for k, v in van.items():
    o = now.get(k)
    if not o or o == v:
        continue
    a, b = "sMapsecName_%s" % sym(v), "sMapsecName_%s" % sym(o)
    if a != b and re.search(r'\b%s\b' % re.escape(a), body):
        body = re.sub(r'\b%s\b' % re.escape(a), b, body); hits += 1
if hits:
    touched[rmc] = body
    print("  %d region_map.c symbol reference(s) follow the rename" % hits)

print("  name renames learned from our own tables: %d" % len(NAMES))
if _typed:
    print("  %d type name(s) withheld from the word map: %s" % (len(_typed), ", ".join(_typed)))
print("  vocabulary entries: %d" % len(VOCAB))
print("  blocks changed: %d dialogue, %d src literals, %d json, in %d files"
      % (changed, src_changed, json_changed, len(touched)))
if scroll_fixed:
    print("  %d file(s) had a scroll break they never had: %s"
          % (len(scroll_fixed), ", ".join(f.split('/')[-1] for f in scroll_fixed)))
if reflowed:
    print("  %d string(s) had more lines than the pane shows, reflowed:" % len(reflowed))
    for r, was, cap in reflowed[:6]:
        print("     %-30s %d lines -> %d" % (r.split('/')[-1], was, cap))
if outgrew:
    print("  %d string(s) could not be reflowed without gaining a line:" % len(outgrew))
    for r, b in outgrew[:8]:
        print("     %-30s %s" % (r.split('/')[-1], b))
if capped:
    print("  %d label(s) hit their array's own limit:" % len(capped))
    for r, want, got in capped:
        print("     %-40s %s -> %s" % (r.split('/')[-1], want, got))
if grew:
    print("  %d label(s) got wider -- check these fit their field:" % len(grew))
    for r, a, b, o, nw in grew[:14]:
        print("     %3d->%3dpx %-34s %s -> %s" % (a, b, r, o, nw))
if over:
    print("  !! %d line(s) over budget:" % len(over))
    for f, w, l in over[:10]:
        print("     %3dpx %-30s %s" % (w, f, l[:60]))
# ------------------------------------------------- the layout guard, after
# reflowable() exists, damage done BEFORE it existed stays done: convert() is a
# no-op on an already-converted string, so a rerun never revisits it. The
# battle menu lost the \\n out of "BAG\\nPOKéMON" that way and all four options
# ran onto one line, with DAEMON and RUN off the right edge of a 96px window --
# and it survived every later run of this tool.
# A LAYOUT STRING POSITIONS ITS OWN TEXT, so its breaks must match upstream's
# exactly. That is checkable, so check it every time rather than trusting that
# the guard was always there.
def is_layout(b):
    return ('{CLEAR' in b or '\\n\\n' in b or '\\n ' in b
            or b.startswith(' ') or '\\p ' in b)

mangled = []
for root, _, fs in os.walk(os.path.join(GBA, "src")):
    fs = [f for f in fs if f not in NEVER_SWEEP]
    for f in sorted(fs):
        if not f.endswith(('.c', '.h')):
            continue
        rel = os.path.relpath(os.path.join(root, f), GBA)
        up = git_show(rel)
        if not up:
            continue
        cur = touched.get(os.path.join(root, f)) or open(os.path.join(root, f),
                                                         encoding="utf-8").read()
        U = [''.join(PIECE.findall(m.group(1))) for m in C_LIT.finditer(up)]
        O = [''.join(PIECE.findall(m.group(1))) for m in C_LIT.finditer(cur)]
        if len(U) != len(O):
            continue                     # structure moved; index pairing is meaningless
        for u, o in zip(U, O):
            if u != o and is_layout(u) and len(BREAK.findall(u)) != len(BREAK.findall(o)):
                mangled.append((rel, u, o))
if mangled:
    print("  !! %d layout string(s) lost or gained a line break:" % len(mangled))
    for rel, u, o in mangled[:8]:
        print("     %s\n       was %s\n       now %s" % (rel, u[:88], o[:88]))

#  FIXED is checked HERE rather than trusted as a comment. A sweep that
#  overflows one of these arrays fails at COMPILE time -- and agbcc reports it
#  as a warning, which this build turns into a bare Error 1, far from the edit.
#  Twice in one session: TOXIC READ became COMPOUND READ (13 of 12) and
#  MOONLIGHT became NIGHT REPAIR in a dex category (12 of 11).
#
#  A name is not prose. If a rename lands inside one of these it is refused,
#  because the fix belongs in whoever chose the name, not in a truncation here.
oversize = []
for path, text in touched.items():
    rel = os.path.relpath(path, GBA)
    for pat, (what, cap) in FIXED.items():
        for m in re.finditer(pat, text):
            if len(m.group(1)) > cap:
                oversize.append((rel, what, cap, m.group(1)))
if oversize:
    print("\n  %d name(s) would overflow a fixed-width array:\n" % len(oversize))
    for rel, what, cap, got in oversize[:12]:
        print("   %-42s %s is %d of %d -- %s" % (rel, what, len(got), cap, got))
    print("\n  nothing written. Shorten the name, or exclude the surface.")
    sys.exit(1)

if WRITE:
    for p, t in touched.items():
        open(p, "w", encoding="utf-8").write(t)
    print("  written: %d files" % len(touched))
sys.exit(1 if over or mangled else 0)

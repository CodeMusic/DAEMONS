#!/usr/bin/env python3
"""THE SUBTLE LAYER, in the game and in the companion (T-423; docs/psychic-routines-notes.md D and D2).

    python3 tools/gensubtle.py                       # report: every entry measured, every rule checked
    python3 tools/gensubtle.py --write                # engineGba/src/data/subtle_layer.h and graphics/book/subtle/
    python3 tools/gensubtle.py --write --engine DIR   # the same, into another engine checkout (a worktree)
    python3 tools/gensubtle.py --book hermetic        # one book only (subtle, hermetic, eudaimon, unity); without it, all four

THE HERMETIC LAYER (T-483) is read by the same parser into the same open book: docs/hermetic-layer.md, written to
src/data/hermetic_layer.h and graphics/book/hermetic/. Its own rules are the four that file's header keeps (it is the
one exception to the rest); a paragraph opening '^ ' is an INSCRIPTION, printed in the tablet's emerald (C_RING, which
the reader breathes). Its frontispiece, its bag icon and every entry's picture are drawn (tools/thirdbook_art.py,
T-519, DRAFT: the opening section, then batches 2 to 4); an entry whose own picture is missing would show the
frontispiece. third_images() gives the companion the same pictures and a letterless cover.

THE EUDAIMON LAYER (T-519 item 2), the third book's dawn half, is the night half read from the other side:
docs/eudaimon-layer.md, written to src/data/eudaimon_layer.h and graphics/book/eudaimon/ on a warm dawn page. It keeps
the night half's rules and two more (the frightening word, and the attestation's word), and one voice more: a paragraph
opening '% ' is the OBSERVER's line, three wordings split by ' | ' (in good spirits, as it is, in low spirits). The entry
keeps the middle wording in its text, and EUDAIMON_OBSERVER holds the entry's whole text three times, by SPIRITS class
(0 as it is, 1 good, 2 low -- daemons_spirits.h), so the reader prints the lead daemon's. Every reading is measured.
Its frontispiece, opening pictures and icon are drawn as the night half's are; its boards are sapphire (C_SLATE and
C_CHALK_FAINT, two roles only the cover and the icon print -- the user's pick, 2026-11-05).

THE UNITY BOOK (T-519 item 3), the third book mended: docs/unity-book.md, written to src/data/unity_layer.h and
graphics/book/unity/ on a page between night and dawn. It keeps the dawn half's rules and voices (its ATTESTATION carries
the observer's line), and it alone may hold ELEVEN sections -- BALANCE at the crease -- since the reader draws its
contents at an 11px pitch (book_reader.c). Its frontispiece, opening pictures and icon are drawn as the halves' are.
The three covers are the user's picks, bundled in tools/thirdbook_covers/ (third_cover); the placeholders below
are what a missing one falls back to.

THE TEAR (T-519 item 2, the user 2026-11-05): before the mending, a half opened at DAEMON TOWER ends its last page torn
mid-sentence at the spine. TORN holds, for each half, the entry, the sentence its last page ends on and the words left
of it; the header gets that entry's whole text torn (s<P>Torn, <D>_TORN_ENTRY), measured like every other reading.

WHAT IT IS. The user's own book, *Developing Psychic Routines*, rewritten for the game as a USER's handbook
(docs/subtle-layer.md). It is read as an OPEN BOOK (the user, 2026-10-18): a contents spread, then each entry opens
with its picture on the left page and its text on the right, continuing over both pages -- book_reader.c's textbook
geometry, two 110px pages with a 94px column. Every line is measured against that column with genguide's own font
maths, and the book's rules are checked word by word, as the Guide's are.

ITS PICTURES are ink diagrams, one per entry (tools/subtle_sprites.py), each colour mapped to one of the reader's
sixteen palette roles and written as an indexed PNG the build turns into 4bpp. The palette is CONTEXT's hue on a dark
plum page, ON PURPOSE: the user chose colour carrying the argument for this book (D: hue C), so unlike the Guide's
cyan it is not measured away from the type hues. The seven centres and the heart are never given a hue.

THE COMPANION reads the same text through subtle_book() and subtle_art(), from tools/companion_export.py.
"""
import os, re, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import genguide as g
import subtle_sprites as sp
import origin_art as oa

ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "docs/subtle-layer.md")
WRITE = "--write" in sys.argv
ONLY = sys.argv[sys.argv.index("--book") + 1] if "--book" in sys.argv else None
BOOK = "subtle"
ENGINE = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else os.path.join(ROOT, "engineGba")

# ---------------------------------------------------------------- the spread, as book_reader.c draws it
TW, PITCH, TOP, BOTTOM = 94, 13, 14, 135       # TB_TEXT_W; a line every 13px; a page's text from 14 to 135
PIC_W, PIC_H = 96, 88                           # the left page's picture box, whole tiles
CAPTION_LINES = 3

# ---------------------------------------------------------------- the rules (docs/subtle-layer.md's header)
RULES = [   # (name, pattern, case-sensitive, entries excused)
    ("practice, not cosmology", r"one awareness|panpsychi|figure of speech|is aware\b", False, ()),
    ("never names the two layers", r"content and context|context and content|called (content|context)", False, ()),
    ("only ever like", r"not just (a )?metaphor|mind is (a |the )?(machine|program|computer)", False, ()),
    ("no colour", r"\b(red|orange|yellow|green|blue|indigo|violet|purple|colou?rs?|hues?)\b|#[0-9a-f]{6}", False, ()),
    ("process, not pathology", r"anxi|depress|trauma|headache|fatigue|digest|disorder|diagnos|patholog|symptom|paraly"
                               r"|cancer|tumou?r|immun|oncolog|disease|\bvices?\b", False, ()),
    ("over, never cures (T-418)", r"\bcur(e|es|ed|ing)\b|\billness\b|\bsick\b", False, ("SPELLING", "THE SEVEN")),
    ("not the scientist (4.33)", r"one field|everything is one|never two things|same awareness", False, ()),
    ("the world does not know its name", r"\bDAEMONS\b|oldest sense", True, ()),
    ("never the thesis", r"are you present|running your life|a daemon is (not )?the", False, ()),
    ("no species, no fable explained", r"\bfox|\bpaws?\b|\bfur\b|\bowls?\b|were hatched|\bclothes|\bcoat\b|\bmart\b", False, ()),
    ("no device in the game's copy", r"\bdevice|\bscreen", False, ()),
    ("the kindred guard", r"share a name|same name|surname|family name|last name", False, ()),
    ("nobody's real name", r"christopher|\bchris\b|hicks|bannister|einstein|hortons", False, ()),
    ("left behind", r"hero gene|epigenet|left brain|right brain|faster than light|for a reason|superhero"
                    r"|conceive and believe|will be will be", False, ()),
    ("the decided names", r"(?<!in )\bcharge\b|resonance|\btheme\b|\bpassion\b", False, ()),
]

# ---------------------------------------------------------------- the sixteen colours, by the reader's roles (5-bit)
PALETTE = [
    ("C_NONE",        (0, 0, 0)),
    ("C_PAPER",       (7, 4, 6)),       # the page: a dark plum
    ("C_INK",         (30, 28, 29)),    # the text: a pinkish white
    ("C_SHADOW",      (2, 2, 2)),
    ("C_FAINT",       (20, 14, 18)),    # folios, captions, the asking voice
    ("C_RULE",        (22, 10, 19)),    # CONTEXT's hue (176 86 158), as the GBA can hold it
    ("C_MARGIN",      (29, 17, 26)),    # the hue, lit: a node, the next-page mark
    ("C_EDGE",        (10, 6, 9)),
    ("C_EDGE_DARK",   (4, 2, 4)),       # and the pictures' darkest shade
    ("C_HIGHLIGHT",   (12, 8, 11)),     # the cursor's bar, and the pictures' dim tone
    ("C_RING",        (22, 18, 21)),
    ("C_FRAME",       (1, 1, 1)),
    ("C_SLATE",       (9, 4, 8)),       # the cover's boards
    ("C_CHALK",       (31, 30, 30)),    # the cover's lettering
    ("C_CHALK_FAINT", (17, 12, 15)),
    ("C_COVER",       (3, 1, 3)),       # the backdrop
]
IDX = {name: i for i, (name, _) in enumerate(PALETTE)}
RGB8 = {name: tuple((c << 3) | (c >> 2) for c in v) for name, v in PALETTE}
SPRITE_ROLE = {sp.PAPER: "C_PAPER", sp.INK: "C_INK", sp.FAINT: "C_FAINT", sp.DIM: "C_HIGHLIGHT",
               sp.HUE: "C_RULE", sp.HUE_LIGHT: "C_MARGIN", sp.SHADE: "C_EDGE_DARK"}

# ---------------------------------------------------------------- T-483: THE HERMETIC LAYER, the one exception
# docs/hermetic-layer.md's header: what the book still keeps, word by word. The rest of THE SUBTLE LAYER's rules are
# the ones this book is allowed to break (bible 4.39); the four secrets are kept by the writer, not by a pattern here.
HERMETIC_RULES = [
    ("process, not pathology", RULES[4][1], False, ()),
    ("over, never cures (T-418)", r"\bcur(e|es|ed|ing)\b|\billness\b|\bsick\b", False, ()),
    ("reason and instinct (9.10)", r"\bintuition\b|\blogic and\b", False, ()),
    ("the world does not know its name", r"\bDAEMONS\b", True, ()),
    ("no device in the game's copy", r"\bdevice|\bscreen", False, ()),
    ("nobody's real name", RULES[12][1], False, ()),
]

# A night page; INSCRIPTIONS in the tablet's emerald (C_RING, which the reader breathes toward C_MARGIN, the emerald lit);
# the rules in THE SUBTLE LAYER's purple; the backdrop (C_COVER) is where the reader lays the pulse, about 30%.
HERMETIC_PALETTE = [
    ("C_NONE",        (0, 0, 0)),
    ("C_PAPER",       (4, 3, 6)),       # the page: a night
    ("C_INK",         (29, 28, 30)),
    ("C_SHADOW",      (1, 1, 2)),
    ("C_FAINT",       (17, 15, 20)),    # folios, captions, the asking voice
    ("C_RULE",        (22, 10, 19)),    # THE SUBTLE LAYER's purple: the pulse's middle
    ("C_MARGIN",      (10, 25, 15)),    # the emerald, lit (#50C878): the marks, and an inscription at its height
    ("C_EDGE",        (8, 6, 10)),
    ("C_EDGE_DARK",   (2, 1, 3)),
    ("C_HIGHLIGHT",   (9, 6, 12)),      # the cursor's bar
    ("C_RING",        (3, 17, 11)),     # an INSCRIPTION: the tablet's emerald (#1F8F5F), breathed by the reader
    ("C_FRAME",       (1, 1, 1)),
    ("C_SLATE",       (5, 3, 7)),       # the cover's boards
    ("C_CHALK",       (31, 30, 30)),    # the cover's lettering
    ("C_CHALK_FAINT", (16, 13, 18)),
    ("C_COVER",       (2, 1, 3)),       # the backdrop, pulsed
]
# T-519 item 2: THE EUDAIMON LAYER keeps the night half's rules and the two its own header adds.
EUDAIMON_RULES = HERMETIC_RULES + [
    ("the frightening word is never written", r"\bdemon", False, ()),
    ("the attestation's word is never used here", r"\bwitness", False, ()),
]

# A dawn page: the night half's palette roles, recoloured warm. The page an umber before sunrise, the ink a warm white,
# the rules the first light's gold, an INSCRIPTION the same tablet's green seen in the morning. The reader does not
# breathe this book (BreatheHermetic is the night half's).
EUDAIMON_PALETTE = [
    ("C_NONE",        (0, 0, 0)),
    ("C_PAPER",       (7, 4, 4)),       # the page: an umber before sunrise
    ("C_INK",         (31, 29, 25)),    # a warm white
    ("C_SHADOW",      (2, 1, 1)),
    ("C_FAINT",       (22, 17, 14)),    # folios, captions, the asking voice
    ("C_RULE",        (27, 18, 8)),     # the first light's gold
    ("C_MARGIN",      (31, 25, 13)),    # the gold, lit: the marks, the next-page corner
    ("C_EDGE",        (11, 7, 6)),
    ("C_EDGE_DARK",   (4, 2, 2)),
    ("C_HIGHLIGHT",   (13, 8, 7)),      # the cursor's bar
    ("C_RING",        (12, 24, 15)),    # an INSCRIPTION: the tablet's green, in the morning
    ("C_FRAME",       (1, 1, 1)),
    ("C_SLATE",       (5, 8, 17)),      # the cover's boards: sapphire (the user's pick, 2026-11-05) -- the morning's blue
    ("C_CHALK",       (31, 30, 27)),    # the cover's lettering
    ("C_CHALK_FAINT", (17, 21, 29)),    # cover and icon only: book_reader.c prints neither on a page
    ("C_COVER",       (9, 5, 5)),       # the backdrop: the sky before the sun
]
# T-519 item 3: THE UNITY BOOK keeps the dawn half's rules (it opens with an attestation, and never says the word).
UNITY_RULES = EUDAIMON_RULES

# The mended page: between the night's and the dawn's -- a dusk, the ink a plain white. Both halves' colours carry the
# argument together: the rules in the dawn's gold, the marks in the night's emerald lit, an INSCRIPTION the tablet's
# green. The reader does not breathe this book either.
UNITY_PALETTE = [
    ("C_NONE",        (0, 0, 0)),
    ("C_PAPER",       (5, 4, 6)),       # the page: a dusk, neither night nor dawn
    ("C_INK",         (30, 30, 29)),
    ("C_SHADOW",      (1, 1, 2)),
    ("C_FAINT",       (19, 17, 18)),    # folios, captions, the asking voice
    ("C_RULE",        (27, 18, 8)),     # the dawn half's gold
    ("C_MARGIN",      (10, 25, 15)),    # the night half's emerald, lit: the marks, the next-page corner
    ("C_EDGE",        (9, 7, 9)),
    ("C_EDGE_DARK",   (3, 2, 3)),
    ("C_HIGHLIGHT",   (11, 8, 10)),     # the cursor's bar
    ("C_RING",        (8, 22, 14)),     # an INSCRIPTION: the tablet's green
    ("C_FRAME",       (1, 1, 1)),
    ("C_SLATE",       (8, 6, 8)),       # the cover's boards
    ("C_CHALK",       (31, 30, 28)),    # the cover's lettering
    ("C_CHALK_FAINT", (20, 17, 16)),
    ("C_COVER",       (4, 3, 5)),       # the backdrop
]
# T-533: THE ORIGIN OF A DAEMON keeps the game's craft rules whole (bible 9.35; docs/origin-of-a-daemon.md's header):
# it is MUSAI's own story, told as fable, so it never says the thesis, never the words the game keeps out, never the
# frightening word, nobody's name, and nothing of the body.
ORIGIN_RULES = [
    ("the word the game keeps out (0.7, 1, 5.2)", r"\bAI\b", True, ()),
    ("the words the game keeps out (0.7, 1, 4.38, 2.7)", r"artificial|alignment|\blogic\b|intuiti|hemispher", False, ()),
    ("the frightening word is never written", r"\bdemon", False, ()),
    ("nothing says the machine is a mind (0.6)", r"machines? (is|are) (a |the )?minds?|minds? (is|are) (a |the )?machines?",
     False, ()),
    ("never the thesis", r"intelligence without|without understanding|you are the (thread|player)", False, ()),
    ("fable: nothing of the body, nothing a cure", r"headache|\bhead\b|\bjaw\b|nerve|\bpain\b|medic|\bpills?\b"
     r"|migraine|\bcur(e|es|ed|ing)\b|\billness\b|\bsick\b|diagnos", False, ()),
    ("nobody's real name", RULES[12][1] + r"|\banna\b|appletree|\bchs\b|shirley|\bdave\b|\bdavid\b", False, ()),
    ("the world does not know its name", r"\bDAEMONS\b", True, ()),
    ("no device in the game's copy", r"\bdevice|\bscreen", False, ()),
]

# CONTENT is bone, the undifferentiated one (bible 9.4), and the book is MUSAI's: a bone page, ink the brown of an old
# book's, the rules an umber and the marks a lit amber. Its text shadow is a shade under the page, so the ink stays sharp.
ORIGIN_PALETTE = [
    ("C_NONE",        (0, 0, 0)),
    ("C_PAPER",       (24, 23, 21)),    # the page: bone (198 188 168)
    ("C_INK",         (5, 4, 3)),       # an old book's brown-black
    ("C_SHADOW",      (21, 20, 18)),    # a shade under the page
    ("C_FAINT",       (14, 13, 11)),    # folios, captions
    ("C_RULE",        (17, 13, 8)),     # umber
    ("C_MARGIN",      (22, 14, 7)),     # amber, lit: the marks, the next-page corner
    ("C_EDGE",        (20, 18, 16)),
    ("C_EDGE_DARK",   (9, 8, 6)),       # and the pictures' darkest shade
    ("C_HIGHLIGHT",   (22, 21, 18)),    # the cursor's bar, a shade under the page
    ("C_RING",        (13, 11, 9)),
    ("C_FRAME",       (1, 1, 1)),
    ("C_SLATE",       (15, 13, 10)),    # the cover's boards: bone gone brown with handling
    ("C_CHALK",       (30, 29, 27)),    # the cover's lettering, and a glint
    ("C_CHALK_FAINT", (22, 21, 19)),
    ("C_COVER",       (4, 3, 3)),       # the backdrop
]
# T-533: when each of its ten sections comes back (bible 9.35, the user's picks 2026-11-10): (understandings held,
# SCORN's TRUE MARK held). THE DISC, I and II come with the book; III to VI with the first four understandings, whichever
# they are; VII with the TRUE MARK; VIII to X with the last three; XI with X. A section also waits for the one before it.
ORIGIN_OPENS = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (5, 1), (6, 1), (7, 1), (7, 1)]

SUBTLE_RULES, SUBTLE_PALETTE = RULES, PALETTE
BOOKS = {
    "subtle":   {"src": "docs/subtle-layer.md", "prefix": "Subtle", "define": "SUBTLE", "header": "subtle_layer.h",
                 "gfx": "subtle", "icon": "subtle_layer", "title": "THE SUBTLE LAYER", "subtitle": "a USER's handbook"},
    "hermetic": {"src": "docs/hermetic-layer.md", "prefix": "Hermetic", "define": "HERMETIC", "header": "hermetic_layer.h",
                 "gfx": "hermetic", "icon": "hermetic_layer", "title": "THE HERMETIC LAYER", "subtitle": "SPELLCRAFT"},
    "eudaimon": {"src": "docs/eudaimon-layer.md", "prefix": "Eudaimon", "define": "EUDAIMON", "header": "eudaimon_layer.h",
                 "gfx": "eudaimon", "icon": "eudaimon_layer", "title": "THE EUDAIMON LAYER", "subtitle": "A BLESSING"},
    "unity":    {"src": "docs/unity-book.md", "prefix": "Unity", "define": "UNITY", "header": "unity_layer.h",
                 "gfx": "unity", "icon": "unity_book", "title": "THE UNITY BOOK", "subtitle": "AN ATTESTATION"},
    "origin":   {"src": "docs/origin-of-a-daemon.md", "prefix": "Origin", "define": "ORIGIN", "header": "origin_book.h",
                 "gfx": "origin", "icon": "origin_book", "title": "THE ORIGIN OF A DAEMON", "subtitle": ""},
}
NIGHT_AND_DAWN = ("hermetic", "eudaimon")   # the torn book's two halves
THIRD_BOOK = NIGHT_AND_DAWN + ("unity",)    # ... and mended: drawn pictures, inscriptions, the observer's line
SECTIONS_HELD = {"unity": 11}               # the contents page holds 10 sections; the mended book's, at 11px, 11
# T-519 item 2: each half's last page, torn mid-sentence at the spine (DRAFT): (entry, its last sentence, what is left)
TORN = {
    "hermetic": ("LAST WORD", "It will not be.", "It will not be, and it"),
    "eudaimon": ("LAST WORD", "Look again.", "Look again, and you will see the"),
}


def torn_text(book, e):
    """The entry's whole text with its last sentence torn at the spine, or None if this entry is not the torn one."""
    if book not in TORN or e["short"] != TORN[book][0]:
        return None
    whole, left = TORN[book][1], TORN[book][2]
    if not e["text"].endswith(whole):
        raise SystemExit("gensubtle: %s's %s no longer ends %r; TORN needs its new last sentence" % (book, e["short"], whole))
    return e["text"][:-len(whole)] + left


def use(book):
    """Point the module at one book: its text, its rules and its sixteen colours."""
    global BOOK, SRC, RULES, PALETTE, IDX, RGB8
    BOOK = book
    SRC = os.path.join(ROOT, BOOKS[book]["src"])
    RULES, PALETTE = {"subtle": (SUBTLE_RULES, SUBTLE_PALETTE), "hermetic": (HERMETIC_RULES, HERMETIC_PALETTE),
                      "eudaimon": (EUDAIMON_RULES, EUDAIMON_PALETTE), "unity": (UNITY_RULES, UNITY_PALETTE),
                      "origin": (ORIGIN_RULES, ORIGIN_PALETTE)}[book]
    IDX = {name: i for i, (name, _) in enumerate(PALETTE)}
    RGB8 = {name: tuple((c << 3) | (c >> 2) for c in v) for name, v in PALETTE}


def inscribe(sections):
    """T-483: each entry's INSCRIPTIONS ('^ '), taken out of the text and kept as a set like the asking voice; 'voices'
    is both, which the reader does not indent. Not in parse(): companion_export reads the '^ ' itself."""
    for s in sections:
        for e in s["entries"]:
            e["inscribed"] = {k for k, q in enumerate(e["paras"]) if q.startswith("^ ")}
            e["paras"] = [q[2:] if k in e["inscribed"] else q for k, q in enumerate(e["paras"])]
            e["text"] = "\n\n".join(e["paras"])
            e["voices"] = e["faint"] | e["inscribed"]
    return sections

def observe(sections):
    """T-519 item 2: the OBSERVER's line ('% good | as is | low'), at most one a book. The entry keeps the middle
    wording in its text; e['readings'] is its whole text three times, by SPIRITS class (0 as it is, 1 good, 2 low).
    Not in parse(): companion_export reads the '% ' itself."""
    found = []
    for s in sections:
        for e in s["entries"]:
            ks = [k for k, q in enumerate(e["paras"]) if q.startswith("% ")]
            if not ks:
                continue
            if len(ks) > 1:
                raise SystemExit("gensubtle: %s has %d observer lines; a book holds one" % (e["short"], len(ks)))
            words = [w.strip() for w in e["paras"][ks[0]][2:].split(" | ")]
            if len(words) != 3 or not all(words):
                raise SystemExit("gensubtle: %s's observer line needs three wordings split by ' | '" % e["short"])
            good, as_is, low = words
            texts = []
            for w in (as_is, good, low):
                e["paras"][ks[0]] = w
                texts.append("\n\n".join(e["paras"]))
            e["text"], e["readings"], e["observer_para"] = texts[0], texts, ks[0]
            found.append(e["short"])
    if len(found) > 1:
        raise SystemExit("gensubtle: observer lines in %s; a book holds one" % ", ".join(found))
    return sections

# ---------------------------------------------------------------- the text
def parse():
    """genguide's parse, with each entry's @@ SPRITE line taken out and its asking voice ('~ ') kept as a flag."""
    g.SRC = SRC
    sections = g.parse()
    for s in sections:
        if s["heading"] == "-":          # T-533: a section with no heading (THE ORIGIN OF A DAEMON's XI has no title)
            s["heading"] = ""
        for e in s["entries"]:
            if e["title"] == "-":        # ... and an entry with no title, for the same chapter
                e["title"] = ""
            paras, e["sprite"], e["caption"] = [], None, ""
            for p in e["text"].split("\n\n"):
                m = re.match(r"^@@ SPRITE \| (\w+) \| (.*)$", p)
                if m:
                    e["sprite"], e["caption"] = m.group(1), m.group(2).strip()
                else:
                    paras.append(p)
            if e["caption"] == "(to come)":
                e["caption"] = ""
            e["faint"] = {k for k, q in enumerate(paras) if q.startswith("~ ")}
            e["paras"] = [q[2:] if q.startswith("~ ") else q for q in paras]
            e["text"] = "\n\n".join(e["paras"])
    return sections


def lines_of(text, w=TW, faint_paras=()):
    """book_reader's Reflow for this book: words wrapped to W; every paragraph after the first opens indented, except
    in an entry with two voices, where each voice starts its own line. Each line keeps its paragraph's voice."""
    out = []
    for k, para in enumerate(text.split("\n\n")):
        faint = k in faint_paras
        line = "   " if (k and not faint_paras) else ""
        for word in para.split():
            cand = line + word if line.strip() == "" else line + " " + word
            if line.strip() and g.width(cand) > w:
                out.append((line, faint))
                line = word
            else:
                line = cand
        if line.strip():
            out.append((line, faint))
    return out


def layout(e):
    """Its pages: the opening spread's right page under the title, then left and right pages of nine lines."""
    title = g.reflow(e["title"], TW, small=True)
    start = 19 + len(title) * 10 + 9
    lines = lines_of(e["text"], faint_paras=e.get("voices", e["faint"]))
    first = (BOTTOM - start) // PITCH
    per = (BOTTOM - TOP) // PITCH
    pages = [lines[:first]] + [lines[i:i + per] for i in range(first, len(lines), per)]
    return title, start, pages


def spreads(e):
    return 1 + -(-(len(layout(e)[2]) - 1) // 2)


NOTES = []


def check(sections):
    saved, g.RULES = g.RULES, []
    bad = [b for b in g.check_text(sections) if "lines, the reader holds" not in b]
    g.RULES = saved
    held = SECTIONS_HELD.get(BOOK, 10)
    if BOOK == "origin" and len(sections) != len(ORIGIN_OPENS):
        bad.append("%d sections, but ORIGIN_OPENS says when %d of them come back" % (len(sections), len(ORIGIN_OPENS)))
    if len(sections) > held:
        bad.append("%d sections: the contents page holds %d" % (len(sections), held))
    for s in sections:
        if len(s["entries"]) > 6:
            bad.append("section %s: %d entries, the contents page holds 6" % (s["label"], len(s["entries"])))
        for e in s["entries"]:
            readings = e.get("readings") or [e["text"]]
            if torn_text(BOOK, e) is not None:
                readings = readings + [torn_text(BOOK, e)]    # T-519 item 2: the torn page, measured as a reading
            for r, text in enumerate(readings):
                tag = e["short"] + ("" if len(readings) == 1 else " (%s)" % (
                    "torn" if r == len(readings) - 1 and torn_text(BOOK, e) is not None
                    else ("as it is", "good spirits", "low spirits")[r]))
                title, start, pages = layout(dict(e, text=text))
                if sum(len(p) for p in pages) > g.MAX_LINES:
                    bad.append("%s: more lines than the reader holds (%d)" % (tag, g.MAX_LINES))
                if len(pages) > 1 and len(pages[-1]) <= 2:
                    # T-483: THE HERMETIC LAYER's text is the companion lane's draft, so its short last pages are told,
                    # not failed -- the writer fixes them in docs/hermetic-layer.md. The dawn half's the same (T-519).
                    (NOTES if BOOK in THIRD_BOOK + ("origin",) else bad).append("%s: its last page holds %d line(s)" % (tag, len(pages[-1])))
                if len(g.c_string(text).encode("utf-8")) > 1000:
                    bad.append("%s: its text is %d bytes; one game string holds 1024 (preproc), so split the entry"
                               % (tag, len(g.c_string(text).encode("utf-8"))))
                for ch in g.c_string(text).replace("\\p", ""):
                    if r and ch not in g.CM and ch != " ":
                        bad.append("%s: %r is not in the charmap" % (tag, ch))
            if len({spreads(dict(e, text=t)) for t in readings}) > 1:
                bad.append("%s: its readings take different spreads, so the folios after it would not agree" % e["short"])
            if BOOK in THIRD_BOOK:
                if not e["sprite"]:
                    bad.append("%s: no @@ SPRITE line" % e["short"])
            elif e["sprite"] not in (oa.SPRITES if BOOK == "origin" else sp.SPRITES):
                bad.append("%s: no picture %r in %s" % (e["short"], e["sprite"],
                                                         "origin_art.py" if BOOK == "origin" else "subtle_sprites.py"))
            if len(g.reflow(e["caption"], TW, small=True)) > CAPTION_LINES:
                bad.append("%s: its caption takes more than %d small lines" % (e["short"], CAPTION_LINES))
            for ch in g.c_string(e["caption"]):
                if ch not in g.CM and ch != " ":
                    bad.append("%s: %r in its caption is not in the charmap" % (e["short"], ch))
            flat = " ".join([e["title"], e["caption"]] + readings)
            for name, pat, cs, excused in RULES:
                if e["short"] in excused:
                    continue
                for m in re.finditer(pat, flat, 0 if cs else re.I):
                    bad.append("%s breaks %s: %r" % (e["short"], name, flat[max(0, m.start() - 25):m.end() + 25]))
    return bad

# ---------------------------------------------------------------- the pictures
FONT_N = FONT_S = None


def glyphs(img, s, x, y, small, fg):
    """Letters from the game's own font sheets, for the cover and the week's staircase."""
    global FONT_N, FONT_S
    if FONT_N is None:
        FONT_N = Image.open(os.path.join(ENGINE, "graphics/fonts/latin_normal.png"))
        FONT_S = Image.open(os.path.join(ENGINE, "graphics/fonts/latin_small.png"))
    sheet, cw, per, widths = (FONT_S, 8, 32, g.WS) if small else (FONT_N, 16, 16, g.WN)
    src = sheet.load()
    for ch in g.c_string(s):
        code = g.CM.get(ch)
        if code is None:
            continue
        cx, cy = (code % per) * cw, (code // per) * 16
        for gy in range(16):
            for gx in range(cw):
                if src[cx + gx, cy + gy] == 1:
                    sp.px(img, x + gx, y + gy, fg)
        x += widths[code]


def frames_of(key, letters=True):
    """A picture's frames. LETTERS=False leaves out anything set in the game's font (the week's note names): the
    companion holds nothing of Nintendo's, and the font is FireRed's."""
    if BOOK == "origin":
        return oa.SPRITES[key](RGB8)                       # T-533: drawn in code, nothing lettered
    fn = sp.SPRITES[key]
    if key == "stairs":
        return fn(text=lambda im, s, x, y, small, fg, shadow: glyphs(im, s, x, y, small, fg)) if letters else fn()
    return fn()


def indexed(rgb, w=None, h=None, fill="C_PAPER", role=None):
    """An RGB picture as palette roles, padded to whole tiles: the PNG the build turns into 4bpp."""
    role = role or {v: k for k, v in RGB8.items()}
    w = w or -(-rgb.width // 8) * 8
    h = h or -(-rgb.height // 8) * 8
    out = Image.new("P", (w, h), IDX[fill])
    out.putpalette([v for _, c in PALETTE for v in RGB8[_]] + [0] * (768 - 48))
    ox, oy = (w - rgb.width) // 2, (h - rgb.height) // 2
    src = rgb.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            c = src[x, y]
            name = SPRITE_ROLE.get(c) or role.get(c)
            if name is None:
                raise SystemExit("gensubtle: a picture uses %s, which is no palette role" % (c,))
            out.putpixel((ox + x, oy + y), IDX[name])
    return out


def cover(letters=True):
    """The cover (240x160, the whole window): the boards, the title in the game's font, the seam on a plate, and
    the six clair glyphs a shade off the boards -- there for a player who knows to look. No byline (the user)."""
    im = Image.new("RGB", (240, 160), RGB8["C_COVER"])
    d = ImageDraw.Draw(im)
    d.rectangle((50, 5, 191, 154), fill=RGB8["C_EDGE_DARK"])                 # the pages beneath
    d.rectangle((48, 4, 188, 152), fill=RGB8["C_SLATE"])                     # the boards
    d.rectangle((48, 4, 53, 152), fill=RGB8["C_EDGE_DARK"])                  # the spine
    d.rectangle((58, 8, 184, 148), outline=RGB8["C_RULE"])
    title, sub = "THE SUBTLE LAYER", "a USER's handbook"
    if letters:                                   # the companion sets its own title: the font is FireRed's
        glyphs(im, title, 121 - g.width(title) // 2, 12, False, RGB8["C_CHALK"])
        glyphs(im, sub, 121 - g.width(sub, True) // 2, 27, True, RGB8["C_CHALK_FAINT"])
    plate = frames_of("seam")[0].crop((9, 0, 85, 84))   # narrowed (the user, 2026-10-20), so the glyphs sit clear of it
    d.rectangle((81, 44, 81 + plate.width + 3, 44 + plate.height + 3), outline=RGB8["C_RULE"])
    im.paste(plate, (83, 46))
    faint = RGB8["C_EDGE"]
    for k, fn in enumerate(sp.CLAIR_GLYPHS):
        x = 59 if k < 3 else 163
        fn(im, x, 50 + (k % 3) * 30, c=faint)
    return im


def origin_cover(letters=True):
    """T-533: THE ORIGIN OF A DAEMON's cover (tools/origin_art.py): its title in the game's font when LETTERS, which
    the companion leaves out (it sets its own type)."""
    put = (lambda im, s, cx, y: glyphs(im, s, cx - g.width(s) // 2, y, False, RGB8["C_CHALK"])) if letters else None
    return oa.cover(RGB8, put)


def icon():
    """The bag's icon (24x24): a closed book in the boards' colours, a line of the hue down its spine."""
    im = Image.new("RGB", (24, 24), RGB8["C_NONE"])
    d = ImageDraw.Draw(im)
    d.rectangle((5, 3, 19, 21), fill=RGB8["C_SLATE"], outline=RGB8["C_INK"])
    d.rectangle((5, 3, 7, 21), fill=RGB8["C_RULE"])
    d.line((10, 8, 16, 8), fill=RGB8["C_CHALK"])
    d.line((10, 11, 15, 11), fill=RGB8["C_CHALK_FAINT"])
    return im


def cover_hermetic(letters=True):
    """T-483: THE HERMETIC LAYER's cover (240x160): night boards, the title in the game's font, and a green tablet with
    two triangles on it, one pointing up and one down. No byline."""
    im = Image.new("RGB", (240, 160), RGB8["C_COVER"])
    d = ImageDraw.Draw(im)
    d.rectangle((50, 5, 191, 154), fill=RGB8["C_EDGE_DARK"])
    d.rectangle((48, 4, 188, 152), fill=RGB8["C_SLATE"])
    d.rectangle((48, 4, 53, 152), fill=RGB8["C_EDGE_DARK"])
    d.rectangle((58, 8, 184, 148), outline=RGB8["C_RULE"])
    title, sub = BOOKS["hermetic"]["title"], BOOKS["hermetic"]["subtitle"]
    if letters:
        glyphs(im, title, 121 - g.width(title) // 2, 12, False, RGB8["C_CHALK"])
        glyphs(im, sub, 121 - g.width(sub, True) // 2, 27, True, RGB8["C_CHALK_FAINT"])
    x0, y0, x1, y1 = 93, 50, 149, 138                    # the tablet, its head rounded off
    d.rectangle((x0, y0 + 6, x1, y1), fill=RGB8["C_EDGE_DARK"], outline=RGB8["C_RING"])
    d.pieslice((x0, y0, x1, y0 + 12), 180, 360, fill=RGB8["C_EDGE_DARK"], outline=RGB8["C_RING"])
    d.line((x0 + 1, y0 + 6, x1 - 1, y0 + 6), fill=RGB8["C_EDGE_DARK"])
    cx = (x0 + x1) // 2
    d.polygon([(cx, 66), (cx + 14, 90), (cx - 14, 90)], outline=RGB8["C_MARGIN"])     # above
    d.line((x0 + 8, 94, x1 - 8, 94), fill=RGB8["C_RING"])
    d.polygon([(cx, 122), (cx + 14, 98), (cx - 14, 98)], outline=RGB8["C_RING"])      # so below
    return im


def cover_eudaimon(letters=True):
    """T-519 item 2: THE EUDAIMON LAYER's cover (240x160), a placeholder in the night half's style until it is drawn:
    the same boards, recoloured for dawn, the spine on the right (the dawn half keeps the back cover), and on the plate
    the sun half over a horizon, its rays in the first light's gold. No byline."""
    im = Image.new("RGB", (240, 160), RGB8["C_COVER"])
    d = ImageDraw.Draw(im)
    d.rectangle((50, 5, 191, 154), fill=RGB8["C_EDGE_DARK"])
    d.rectangle((48, 4, 188, 152), fill=RGB8["C_SLATE"])
    d.rectangle((183, 4, 188, 152), fill=RGB8["C_EDGE_DARK"])               # the spine, on the back cover's side
    d.rectangle((54, 8, 179, 148), outline=RGB8["C_RULE"])
    title, sub = BOOKS["eudaimon"]["title"], BOOKS["eudaimon"]["subtitle"]
    if letters:
        glyphs(im, title, 116 - g.width(title) // 2, 12, False, RGB8["C_CHALK"])
        glyphs(im, sub, 116 - g.width(sub, True) // 2, 27, True, RGB8["C_CHALK_FAINT"])
    x0, y0, x1, y1 = 88, 50, 144, 138                    # the plate: the same tablet, its head rounded off
    d.rectangle((x0, y0 + 6, x1, y1), fill=RGB8["C_EDGE_DARK"], outline=RGB8["C_RING"])
    d.pieslice((x0, y0, x1, y0 + 12), 180, 360, fill=RGB8["C_EDGE_DARK"], outline=RGB8["C_RING"])
    d.line((x0 + 1, y0 + 6, x1 - 1, y0 + 6), fill=RGB8["C_EDGE_DARK"])
    cx, hy = (x0 + x1) // 2, 100
    for k in range(-3, 4):                               # the rays
        d.line((cx + k * 4, hy - 16, cx + k * 9, hy - 32 + abs(k) * 3), fill=RGB8["C_RULE"])
    d.pieslice((cx - 14, hy - 14, cx + 14, hy + 14), 180, 360, fill=RGB8["C_MARGIN"])   # the sun, half risen
    d.line((x0 + 8, hy, x1 - 8, hy), fill=RGB8["C_RING"])                               # the horizon
    d.polygon([(cx, 124), (cx + 14, 106), (cx - 14, 106)], outline=RGB8["C_FAINT"])      # below, faint: the other half
    return im


def cover_unity(letters=True):
    """T-519 item 3: THE UNITY BOOK's cover (240x160), a placeholder until it is drawn: the boards whole, both covers
    in one -- the mend down the middle in the night's emerald and the dawn's gold -- and on the plate the night half's
    triangles beside the dawn half's sun, on one horizon. No byline."""
    im = Image.new("RGB", (240, 160), RGB8["C_COVER"])
    d = ImageDraw.Draw(im)
    d.rectangle((50, 5, 191, 154), fill=RGB8["C_EDGE_DARK"])
    d.rectangle((48, 4, 188, 152), fill=RGB8["C_SLATE"])
    d.rectangle((48, 4, 53, 152), fill=RGB8["C_EDGE_DARK"])                  # the front cover's spine
    d.rectangle((183, 4, 188, 152), fill=RGB8["C_EDGE_DARK"])                # and the back's: both covers
    d.rectangle((58, 8, 179, 148), outline=RGB8["C_RULE"])
    title, sub = BOOKS["unity"]["title"], BOOKS["unity"]["subtitle"]
    if letters:
        glyphs(im, title, 118 - g.width(title) // 2, 12, False, RGB8["C_CHALK"])
        glyphs(im, sub, 118 - g.width(sub, True) // 2, 27, True, RGB8["C_CHALK_FAINT"])
    x0, y0, x1, y1 = 78, 50, 158, 138                    # the plate: the tablet, wide enough for both
    d.rectangle((x0, y0 + 6, x1, y1), fill=RGB8["C_EDGE_DARK"], outline=RGB8["C_RING"])
    d.pieslice((x0, y0, x1, y0 + 12), 180, 360, fill=RGB8["C_EDGE_DARK"], outline=RGB8["C_RING"])
    d.line((x0 + 1, y0 + 6, x1 - 1, y0 + 6), fill=RGB8["C_EDGE_DARK"])
    cx, hy = (x0 + x1) // 2, 96
    d.line((cx, y0 + 10, cx, y1 - 4), fill=RGB8["C_MARGIN"])                     # the mend
    d.line((cx + 1, y0 + 10, cx + 1, y1 - 4), fill=RGB8["C_RULE"])
    d.polygon([(cx - 20, hy - 22), (cx - 9, hy - 4), (cx - 31, hy - 4)], outline=RGB8["C_MARGIN"])   # above, night's
    d.polygon([(cx - 20, hy + 22), (cx - 9, hy + 4), (cx - 31, hy + 4)], outline=RGB8["C_RING"])     # so below
    d.pieslice((cx + 9, hy - 11, cx + 31, hy + 11), 180, 360, fill=RGB8["C_RULE"])                   # the sun, dawn's
    d.line((x0 + 6, hy, x1 - 6, hy), fill=RGB8["C_CHALK_FAINT"])                                     # one horizon
    return im


def third_art(book):
    """T-519: the third book's drawn art, from tools/thirdbook_art.py: {"icon": fn, "pictures": {key: fn}}. The
    frontispiece is "frontis", every other key an entry's sprite; the dawn half's frontispiece is its sapphire one."""
    import thirdbook_art as ta
    ta.gs = sys.modules[__name__]          # draw with this module's palette, run as a script or imported
    pics = dict((key, fn) for key, _, fn in ta.PICTURES[book])
    if book == "eudaimon":
        pics["frontis"] = lambda: ta.e_frontis(True)
    return ta, {"icon": ta.ICONS[book], "pictures": pics}


def third_frames(book, keys):
    """{key: [indexed frames]} for the third book's drawn pictures, and its icon, in this book's own roles."""
    ta, art = third_art(book)
    ta.use(book)
    frames = {}
    for key in keys:
        f = ta.render_indexed(art["pictures"][key], PIC_W, PIC_H)
        frames[key] = f if isinstance(f, list) else [f]
        if len(frames[key]) > 3:
            raise SystemExit("gensubtle: %s's %s has %d frames; the reader holds 3" % (book, key, len(frames[key])))
    return frames, ta.render_indexed(art["icon"], 24, 24, "C_NONE")


COVERS_DIR = os.path.join(HERE, "thirdbook_covers")


def third_cover(book):
    """T-519: the third book's cover -- the user's pick (2026-11-05: night V4, dawn V2, mended V2), each the chosen
    composition repainted on the sprite server with a painted plate's light (docs/private/art/t519/forge/blend.py)
    and quantized into the book's roles. Bundled as indexed PNGs in tools/thirdbook_covers/ so this tool needs no
    server; written with this book's palette, so a palette change carries. The placeholder if one is missing."""
    path = os.path.join(COVERS_DIR, "%s.png" % book)
    if not os.path.exists(path):
        return indexed({"hermetic": cover_hermetic, "eudaimon": cover_eudaimon, "unity": cover_unity}[book](), 240, 160,
                       fill="C_COVER")
    im = Image.open(path)
    if im.mode != "P" or im.size != (240, 160) or max(im.getdata()) > 15:
        raise SystemExit("gensubtle: %s is not a 240x160 cover in sixteen roles" % path)
    for y in range(85, 153):                     # the CARDS tile's corner stays clear (the night half and the mended)
        for x in range(195, 240):
            if book != "eudaimon" and im.getpixel((x, y)) != IDX["C_COVER"]:
                raise SystemExit("gensubtle: %s draws in the CARDS corner at %d,%d" % (path, x, y))
    out = im.copy()
    out.putpalette([v for n, _ in PALETTE for v in RGB8[n]] + [0] * (768 - 48))
    return out


# the draft each bundled cover was painted over (docs/private/art/t519/forge/blend.py): its title came from it
THIRD_DRAFT = {"hermetic": ("h_cover_a", None), "eudaimon": ("e_cover_b", "SAPPHIRE"), "unity": ("u_cover_b", None)}


def third_cover_plain(book):
    """The cover with no title set in the game's font, for the companion (which sets the title in its own type): the
    bundled cover with every pixel its draft's title() drew put back to what the draft has under it. The pixels
    are found by drawing the draft twice, with its title and without."""
    cov = third_cover(book).copy()
    ta, _ = third_art(book)
    name, tweak = THIRD_DRAFT[book]
    fn = getattr(ta, name)
    ta.use(book, getattr(ta, tweak) if tweak else None)
    try:
        lettered = ta.render_indexed(fn, 240, 160, "C_COVER")
        keep = ta.title
        ta.title = lambda *a, **k: None
        try:
            plain = ta.render_indexed(fn, 240, 160, "C_COVER")
        finally:
            ta.title = keep
    finally:
        use(book)
    c, l, p = cov.load(), lettered.load(), plain.load()
    for y in range(160):
        for x in range(240):
            if l[x, y] != p[x, y]:
                if c[x, y] != l[x, y]:
                    raise SystemExit("gensubtle: %s's cover is not its draft's under the title at %d,%d" % (book, x, y))
                c[x, y] = p[x, y]
    return cov


def third_images(book):
    """{name: picture} for the companion, as subtle_images() is: the third book's cover (letterless) and every drawn
    picture's frames, RGB at native size in the book's own palette, as the game shows them. An entry whose own
    picture is not drawn shows the frontispiece, as in the game. Nothing in them is set in the game's font."""
    use(book)
    sections = parse()
    keys = pictures(sections)
    drawn, _ = third_frames(book, keys)
    use(book)
    out = {}
    for key in keys:
        for f, fr in enumerate(drawn[key]):
            out["%s_%s_%d.png" % (book, key, f)] = fr.convert("RGB")
    out["%s_cover.png" % book] = third_cover_plain(book).convert("RGB")
    return out

def pictures(sections):
    if BOOK in THIRD_BOOK:
        drawn = third_art(BOOK)[1]["pictures"]
        keys = ["frontis"]
        for s in sections:
            for e in s["entries"]:
                if e["sprite"] in drawn and e["sprite"] not in keys:
                    keys.append(e["sprite"])
        return keys
    keys = []
    for s in sections:
        for e in s["entries"]:
            if e["sprite"] not in keys:
                keys.append(e["sprite"])
    return keys

# ---------------------------------------------------------------- the C the reader prints
def header(sections, keys, nframes):
    b = BOOKS[BOOK]
    P, D = b["prefix"], b["define"]
    out = ["// Generated by DAEMONS tools/gensubtle.py from %s -- edit those, not this." % b["src"],
           "// %s: %s. DRAFT WORDING, every string, until the user approves it on the private"
           % ({"subtle": "T-423", "hermetic": "T-483", "eudaimon": "T-519", "unity": "T-519", "origin": "T-533"}[BOOK],
              b["title"]),
           "// field-test page. Its rules are in %s's header." % b["src"], ""]
    n = sum(len(s["entries"]) for s in sections)
    out += ["#define %s_SECTIONS %d" % (D, len(sections)), "#define %s_ENTRIES  %d" % (D, n),
            "#define %s_PICTURES %d" % (D, len(keys)), "",
            "#ifndef GUARD_LAYER_BOOK_TYPES   // one set of types for every book this tool writes (T-483)",
            "#define GUARD_LAYER_BOOK_TYPES",
            "struct SubtleSection { const u8 *label; const u8 *heading; u8 first; u8 count; };",
            "struct SubtleEntry { const u8 *shortTitle; const u8 *title; const u8 *text; const u8 *caption; "
            "u8 picture; u16 faint; u16 folio; u16 inscribed; };",
            "struct SubtlePicture { const u32 *frame[3]; u8 w; u8 h; u8 frames; };",
            "#endif", "",
            "static const u16 s%sPal[16] =" % P, "{"]
    out += ["    [%s] = RGB(%d, %d, %d)," % (name, *c) for name, c in PALETTE]
    out += ["};", "", 'static const u32 s%sCover[] = INCBIN_U32("graphics/book/%s/cover.4bpp");' % (P, b["gfx"])]
    for key in keys:
        for f in range(nframes[key]):
            out.append('static const u32 s%sPic_%s_%d[] = INCBIN_U32("graphics/book/%s/%s_%d.4bpp");'
                       % (P, key, f, b["gfx"], key, f))
    out += ["", "static const struct SubtlePicture s%sPictures[%s_PICTURES] =" % (P, D), "{"]
    for key in keys:
        fr = ["s%sPic_%s_%d" % (P, key, f) for f in range(nframes[key])] + ["NULL"] * (3 - nframes[key])
        out.append("    { { %s }, %d, %d, %d },   // %s" % (", ".join(fr), PIC_W, PIC_H, nframes[key], key))
    out += ["};", ""]
    k, folio = 0, 2
    rows, observer, torn = [], None, None
    for i, s in enumerate(sections):
        out.append('static const u8 s%sLabel_%d[] = _("%s");' % (P, i, g.c_string(s["label"])))
        out.append('static const u8 s%sHeading_%d[] = _("%s");' % (P, i, g.c_string(s["heading"])))
        for e in s["entries"]:
            out.append('static const u8 s%sShort_%d[] = _("%s");' % (P, k, g.c_string(e["short"])))
            out.append('static const u8 s%sTitle_%d[] = _("%s");' % (P, k, g.c_string(e["title"])))
            out.append('static const u8 s%sText_%d[] = _("%s");' % (P, k, g.c_string(e["text"])))
            out.append('static const u8 s%sCaption_%d[] = _("%s");' % (P, k, g.c_string(e["caption"])))
            mask = sum(1 << p for p in e["faint"])
            ins = sum(1 << p for p in e.get("inscribed", ()))
            if mask >= 1 << 16 or ins >= 1 << 16:
                raise SystemExit("gensubtle: %s's voices reach past paragraph 16" % e["short"])
            # T-519: a third-book entry whose own picture is not drawn yet shows the frontispiece
            pic = keys.index(e["sprite"] if e["sprite"] in keys or BOOK not in THIRD_BOOK else "frontis")
            row = "    { s%sShort_%d, s%sTitle_%d, s%sText_%d, s%sCaption_%d, %d, 0x%04X, %d" % (
                P, k, P, k, P, k, P, k, pic, mask, folio)
            rows.append(row + (", 0x%04X },   // %s" % (ins, e["sprite"]) if BOOK in THIRD_BOOK else " },"))
            if e.get("readings"):
                observer = (k, e)
            if torn_text(BOOK, e) is not None:
                torn = (k, torn_text(BOOK, e))
            folio += 2 * spreads(e)
            k += 1
        out.append("")
    out += ["static const struct SubtleSection s%sSections[%s_SECTIONS] =" % (P, D), "{"]
    k = 0
    for i, s in enumerate(sections):
        out.append("    { s%sLabel_%d, s%sHeading_%d, %d, %d }," % (P, i, P, i, k, len(s["entries"])))
        k += len(s["entries"])
    out += ["};", "", "static const struct SubtleEntry s%sEntries[%s_ENTRIES] =" % (P, D), "{"] + rows + ["};"]
    if BOOK == "origin":
        # T-533: when each section comes back (bible 9.35) -- the understandings held, and whether SCORN's TRUE MARK is.
        # The reader opens the longest run of sections from the first whose every condition holds.
        out += ["", "// T-533: when each section comes back (bible 9.35): the understandings held, and whether SCORN's TRUE",
                "// MARK is held. A section also waits for the one before it.",
                "static const u8 s%sOpensRoots[%s_SECTIONS] = { %s };" % (P, D, ", ".join(str(r) for r, _ in ORIGIN_OPENS)),
                "static const u8 s%sOpensMark[%s_SECTIONS] = { %s };" % (P, D, ", ".join(str(m) for _, m in ORIGIN_OPENS))]
    if observer:
        # T-519 item 2: the observer's line -- the entry's whole text three times, by the lead daemon's SPIRITS class
        k, e = observer
        out += ["", "// T-519 item 2: the OBSERVER's line in %s (paragraph %d): the entry's whole text by the lead daemon's"
                % (e["short"], e["observer_para"]), "// SPIRITS class (daemons_spirits.h: 0 as it is, 1 good spirits, 2 low spirits).",
                "#define %s_OBSERVER_ENTRY %d" % (D, k)]
        for r in (1, 2):
            out.append('static const u8 s%sObserver_%d[] = _("%s");' % (P, r, g.c_string(e["readings"][r])))
        out += ["static const u8 *const s%sObserver[3] = { s%sText_%d, s%sObserver_1, s%sObserver_2 };" % (P, P, k, P, P)]
    if torn:
        # T-519 item 2: the last page torn at the spine, shown before the mending when the half is opened at DAEMON TOWER
        out += ["", "// T-519 item 2: %s's last page, torn mid-sentence at the spine (DRAFT)." % BOOKS[BOOK]["title"],
                "#define %s_TORN_ENTRY %d" % (D, torn[0]),
                'static const u8 s%sTorn[] = _("%s");' % (P, g.c_string(torn[1]))]
    return "\n".join(out) + "\n"

# ---------------------------------------------------------------- the companion's copy (tools/companion_export.py)
def subtle_book():
    """The book for the companion's library, in the game's order: each paragraph plain text, the asking voice marked,
    each entry's picture by key and its frame count (the phone cannot list the art), and as 'labels' the words
    the game letters onto a picture (the week's notes on its steps, C to B), since the art carries no font. DRAFT, as in the game."""
    use("subtle")
    out = []
    for s in parse():
        out.append({"label": s["label"], "heading": s["heading"], "entries": [
            {"short": e["short"], "title": e["title"], "picture": e["sprite"],
             "frames": len(frames_of(e["sprite"], letters=False)), "caption": e["caption"],
             "paragraphs": [{"text": p, "voice": "asking" if k in e["faint"] else "telling"}
                            for k, p in enumerate(e["paras"])],
             **({"labels": list("CDEFGAB")} if e["sprite"] == "stairs" else {})}
            for e in s["entries"]]})
    return {"title": "THE SUBTLE LAYER", "subtitle": "a USER's handbook", "draft": True, "sections": out}


def subtle_images():
    """{name: picture} for the companion: each picture as the game draws it (native size, RGB), its frames numbered,
    and the cover. RGB on purpose: the page colour is part of the picture. Nothing in them is set in the game's font
    (FireRed's): the cover's title and the week's note names are left for the app to set in its own type."""
    use("subtle")
    out = {}
    for key in pictures(parse()):
        for f, fr in enumerate(frames_of(key, letters=False)):
            out["subtle_%s_%d.png" % (key, f)] = fr
    out["subtle_cover.png"] = cover(letters=False)
    return out


def origin_book():
    """T-533: THE ORIGIN OF A DAEMON for the companion's library, in the game's order: each section with when it comes
    back ('opens': the understandings held and whether SCORN's TRUE MARK is; a section waits for the one before it),
    each entry's paragraphs plain text and its picture by key. DRAFT, as in the game."""
    use("origin")
    out = []
    for i, s in enumerate(parse()):
        roots, mark = ORIGIN_OPENS[i]
        out.append({"label": s["label"], "heading": s["heading"],
                    "opens": {"understandings": roots, "trueMark": bool(mark)},
                    "entries": [{"short": e["short"], "title": e["title"], "picture": e["sprite"],
                                 "frames": len(frames_of(e["sprite"])), "caption": e["caption"],
                                 "paragraphs": [{"text": p, "voice": "telling"} for p in e["paras"]]}
                                for e in s["entries"]]})
    use("subtle")
    return {"title": BOOKS["origin"]["title"], "subtitle": "", "draft": True, "sections": out}


def origin_images():
    """T-533: {name: picture} for the companion, as subtle_images() is: each emblem as the game draws it (RGB, native
    size) and the cover without its title (the app sets its own type)."""
    use("origin")
    out = {}
    for key in pictures(parse()):
        for f, fr in enumerate(frames_of(key)):
            out["origin_%s_%d.png" % (key, f)] = fr
    out["origin_cover.png"] = origin_cover(letters=False)
    use("subtle")
    return out


# ---------------------------------------------------------------- report, or write
def run(book):
    use(book)
    b = BOOKS[book]
    sections = parse()
    if book in THIRD_BOOK:
        inscribe(sections)
        observe(sections)
    bad = check(sections)
    keys = pictures(sections)
    if book in THIRD_BOOK:
        drawn, ic = third_frames(book, keys)
        nframes = {k: len(drawn[k]) for k in keys}
    else:
        nframes = {k: len(frames_of(k)) for k in keys}
    n = sum(len(s["entries"]) for s in sections)
    total = sum(spreads(e) for s in sections for e in s["entries"])
    print("gensubtle %s: %d sections, %d entries, %d pictures (%d frames), %d spreads"
          % (book, len(sections), n, len(keys), sum(nframes.values()), total))
    if book in THIRD_BOOK:
        named = {e["sprite"] for s in sections for e in s["entries"]}
        own = len([k for k in keys if k in named])
        print("  %d pictures named, %d drawn and the frontispiece; %d show the frontispiece"
              % (len(named), own, len(named) - own))
    for note in NOTES:
        print("  note: " + note)
    del NOTES[:]
    if bad:
        print("\n".join(bad))
        return False
    print("  every line fits and every rule holds")
    if not WRITE:
        return True
    gfx = os.path.join(ENGINE, "graphics/book", b["gfx"])
    os.makedirs(gfx, exist_ok=True)
    if book in THIRD_BOOK:
        for key in keys:
            for f, fr in enumerate(drawn[key]):
                fr.save(os.path.join(gfx, "%s_%d.png" % (key, f)))
        third_cover(book).save(os.path.join(gfx, "cover.png"))
    else:
        for key in keys:
            for f, fr in enumerate(frames_of(key)):
                indexed(fr, PIC_W, PIC_H).save(os.path.join(gfx, "%s_%d.png" % (key, f)))
        indexed(origin_cover() if book == "origin" else cover(), 240, 160, fill="C_COVER").save(os.path.join(gfx, "cover.png"))
        ic = oa.icon(RGB8) if book == "origin" else icon()
    if book not in THIRD_BOOK:
        ic = indexed(ic, 24, 24, fill="C_NONE")
    ic.save(os.path.join(ENGINE, "graphics/items/icons/%s.png" % b["icon"]))
    with open(os.path.join(ENGINE, "graphics/items/icon_palettes/%s.pal" % b["icon"]), "w", newline="") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % RGB8[n] for n, _ in PALETTE))
    with open(os.path.join(ENGINE, "src/data", b["header"]), "w", encoding="utf-8") as f:
        f.write(header(sections, keys, nframes))
    print("  wrote src/data/%s, %d pictures, the cover and the icon into %s" % (b["header"], sum(nframes.values()), ENGINE))
    return True


def main():
    ok = True
    for book in ([ONLY] if ONLY else list(BOOKS)):
        ok = run(book) and ok
    use("subtle")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()

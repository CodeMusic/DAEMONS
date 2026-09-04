#!/usr/bin/env python3
"""Retire OAK from the GBA build's dialogue.

    python3 tools/port_oak.py [--write]

vision.md settled the names once, on the Game Boy side, and this applies the
same table to `engineGba`:

    OAK:            -> CRYSTAL:          the dialogue prefix. People know her
    PROF. OAK       -> CRYSTAL CLEAR     third person, and NO TITLE
    OAK (bare)      -> CRYSTAL CLEAR
    OAK'S PARCEL    -> the PACKAGE       the item is already renamed

*The surname is not decoration.* 4.3 turns on Crystal's full name being as
visible as Ty's, so every formal reference reads CRYSTAL CLEAR in full and only
the spoken prefix is shortened.

**Both replacements are longer** -- `OAK:` -> `CRYSTAL:` is +4 characters and
`PROF. OAK` -> `CRYSTAL CLEAR` is +5 -- and Gen 3 text is hand-wrapped, so every
touched block has to be rewrapped or it runs out of the box.

The rewrap is measured, not counted. `src/text.c` carries FONT_NORMAL's own
advance widths and `charmap.txt` maps a character to its glyph, so a line's
width is arithmetic. The budget is 196px: that is the widest line vanilla ships
in any map text.inc, and 26 tiles is what every standard message window is.

Identifiers are not text. PalletTown_ProfessorOaksLab is a directory, gOakSpeech_
is a label and B_WIN_OAK_OLD_MAN is an enum -- only `.string "..."` bodies and
_("...") literals are touched. ROAK stays: it is a rival name you can pick.
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
BUDGET = 196
# The intro and the help system draw into wider windows than the message box;
# 220px is the widest line vanilla ships in either.
WIDE = {"data/text/help_system.inc": 220, "data/text/new_game_intro.inc": 220}

# ---------------------------------------------------------------- the font
def font():
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

WIDTHS, CHARMAP = font()

# A placeholder is as wide as whatever it expands to. Names cap at seven
# characters, so seven capitals is the honest worst case; the rest draw nothing.
NAME_TOKEN = re.compile(r'\{(PLAYER|RIVAL|B_PLAYER_NAME|B_OPPONENT_NAME|B_BUFF\d|STR_VAR_\d)\}')

def textwidth(s):
    """Pixel width of one rendered line."""
    total = 0
    for tok in re.findall(r'\{[^}]*\}|.', s):
        if tok.startswith('{'):
            if NAME_TOKEN.fullmatch(tok):
                total += sum(WIDTHS[CHARMAP[c]] for c in "ABCDEFG")
            continue
        g = CHARMAP.get(tok)
        if g is not None and g < len(WIDTHS):
            total += WIDTHS[g]
    return total

# ---------------------------------------------------------------- the names
SUBS = [
    (re.compile(r"PROF\.\s?OAK'S"),  "CRYSTAL CLEAR'S"),
    (re.compile(r"PROF\.\s?OAK's"),  "CRYSTAL CLEAR's"),
    (re.compile(r"PROF\.\s?OAK"),    "CRYSTAL CLEAR"),
    (re.compile(r"OAK'S PARCEL"),    "the PACKAGE"),
    (re.compile(r"\bOAK:"),          "CRYSTAL:"),
    (re.compile(r"\bOAK'S"),         "CRYSTAL CLEAR'S"),
    (re.compile(r"\bOAK's"),         "CRYSTAL CLEAR's"),
    (re.compile(r"\bOAK\b"),         "CRYSTAL CLEAR"),
]

# She is not a he, and the design has been caught by this once already -- a
# gender sweep, not a title sweep, is what found PROF. CRYSTAL in ViridianMart.
# Applied only inside blocks that name her, which is why VermilionCity survives:
# its "he" is the OTHER AIDE, and none of these fragments appear in it.
PRONOUN = [
    ("is going to have his own",        "is going to have her own"),
    ("but he's the authority on",       "but she's the authority on"),
    ("TRAINERS hold him in",            "TRAINERS hold her in"),
    ("reportedly lives with his",       "reportedly lives with her"),
    ("He's a shadow of his former self","She's a shadow of her former self"),
    ("Now he just wants to fiddle with","Now she just wants to fiddle with"),
    ("his POKéDEX",                     "her POKéDEX"),
    ("He's wrong",                      "She's wrong"),
    ("under his wing",                  "under her wing"),
    ("He entrusted me with this",       "She entrusted me with this"),
    ("His order came in",               "Her order came in"),
    ("take it to him?",                 "take it to her?"),
    ("He said that POKéMON's energy",   "She said that POKéMON's energy"),
    ("His evaluations should give you", "Her evaluations should give you"),
    # Agatha is reminiscing about a woman
    ("once tough and\\nhandsome",         "once tough and striking"),
]

# Fields with a hard cap, where CRYSTAL CLEAR does not fit and something has to
# give. Same call the design already made for OAK'S PARCEL -> PACKAGE.
OVERRIDES = {
    # quest log location: CRYSTAL CLEAR RESEARCH LAB is 156px and the widest
    # vanilla location, PEWTER MUSEUM OF SCIENCE, is 144.
    "OAK RESEARCH LAB": "CRYSTAL CLEAR'S LAB",
    # struct Trainer's name field is twelve bytes. CRYSTAL CLEAR is thirteen
    # characters, so the battle nameplate gets the short form.
    "PROF. OAK": "CRYSTAL",
    # this one carries a hanging indent, so it is rewrapped by hand
    '{CIRCLE_1} Select \u201cPROF. OAK\'S PC\u201d on the PC.\\n'
    '{CIRCLE_2} PROF. OAK will evaluate your\\n   POKéDEX.\\n'
    'His evaluations should give you hints\\nfor catching more POKéMON!$':
    '{CIRCLE_1} Select \u201cCRYSTAL CLEAR\'S PC\u201d\\n   on the PC.\\n'
    '{CIRCLE_2} CRYSTAL CLEAR will evaluate\\n   your POKéDEX.\\n'
    'Her evaluations should give you hints\\nfor catching more POKéMON!$',
}

def rename(s):
    if s in OVERRIDES:
        return OVERRIDES[s]
    for a, b in PRONOUN:
        s = s.replace(a, b)
    for pat, rep in SUBS:
        s = pat.sub(rep, s)
    return s

# ---------------------------------------------------------------- the rewrap
# A name can be split across a line break -- vanilla wraps "PROF.\\nOAK's
# POKeMON SEMINAR" mid-name -- so a reflowable block is FLATTENED BEFORE it is
# renamed. Matching the wrapped form misses it, and did: two blocks survived the
# first pass and only the second run of this tool found them.
UNWRAP = re.compile(r'\\[nl]')

BREAK = re.compile(r'\\[nlp]')

def rewrap(body, budget=BUDGET):
    """Reflow one string body. \\p starts a page; inside a page the first break
    is \\n and every later one is \\l, which is the scroll."""
    tail = ''
    for end in ('{PAUSE_UNTIL_PRESS}$', '$'):
        if body.endswith(end):
            body, tail = body[:-len(end)], end
            break
    out = []
    for page in body.split('\\p'):
        words = BREAK.sub(' ', page).replace('CRYSTAL CLEAR', 'CRYSTAL\x00CLEAR').split()
        words = [w.replace('\x00', ' ') for w in words]
        if not words:
            out.append('')
            continue
        lines, cur = [], words[0]
        for w in words[1:]:
            trial = cur + ' ' + w
            if textwidth(trial) <= budget:
                cur = trial
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        out.append(lines[0] + ''.join(('\\n' if i == 0 else '\\l') + l
                                      for i, l in enumerate(lines[1:])))
    return '\\p'.join(out) + tail

# A block that carries its own layout -- a blank line, a hanging indent -- is
# formatting, not prose, and rewrapping it would destroy the thing it is doing.
def reflowable(body):
    return not ('\\n\\n' in body or '\\n ' in body or '\\p ' in body
                or body.startswith(' '))

# ---------------------------------------------------------------- the files
STR_LINE = re.compile(r'^(\s*)\.string "(.*)"\s*$')
C_LIT    = re.compile(r'_\("((?:[^"\\]|\\.)*)"\)')
HAS_OAK  = re.compile(r'\bOAK\b|OAK\'|PROF\.\s?OAK')

report, touched, overflow = [], {}, []

def budget_for(path):
    return WIDE.get(os.path.relpath(path, GBA), BUDGET)

def note(path, before, after):
    report.append((path, before, after))
    for line in BREAK.split(after.rstrip('$')):
        line = line.replace('{PAUSE_UNTIL_PRESS}', '')
        w = textwidth(line)
        if w > budget_for(path):
            overflow.append((path, w, line))

def do_asm(path):
    lines = open(path, encoding="utf-8").read().split('\n')
    out, i, hit = [], 0, False
    while i < len(lines):
        m = STR_LINE.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent, run, j = m.group(1), [], i
        while j < len(lines):
            mm = STR_LINE.match(lines[j])
            if not mm:
                break
            run.append(mm.group(2)); j += 1
        body = ''.join(run)
        # Test the FLATTENED body: "PROF.\\nOAK" puts an n against the O and
        # \\b finds no boundary, so the wrapped form hides the name from its
        # own detector. Two fame checker blocks survived every pass this way.
        if HAS_OAK.search(UNWRAP.sub(' ', body)):
            if body not in OVERRIDES and reflowable(body):
                new = rewrap(rename(UNWRAP.sub(' ', body)), budget_for(path))
            else:
                new = rename(body)
            note(path, body, new)
            parts = re.split(r'(?<=\\[nlp])', new)
            out += ['%s.string "%s"' % (indent, p) for p in parts if p]
            hit = True
        else:
            out += lines[i:j]
        i = j
    if hit:
        touched[path] = '\n'.join(out)

def do_c(path):
    src = open(path, encoding="utf-8").read()
    hit = [False]
    def sub(m):
        body = m.group(1)
        if not HAS_OAK.search(UNWRAP.sub(' ', body)):
            return m.group(0)
        if body not in OVERRIDES and reflowable(body):
            new = rewrap(rename(UNWRAP.sub(' ', body)), budget_for(path))
        else:
            new = rename(body)
        note(path, body, new); hit[0] = True
        return '_("%s")' % new
    new_src = C_LIT.sub(sub, src)
    if hit[0]:
        touched[path] = new_src

for p in glob.glob(os.path.join(GBA, "data/**/*.inc"), recursive=True) + \
         glob.glob(os.path.join(GBA, "data/**/*.s"), recursive=True):
    do_asm(p)
for p in glob.glob(os.path.join(GBA, "src/**/*.c"), recursive=True) + \
         glob.glob(os.path.join(GBA, "src/**/*.h"), recursive=True):
    do_c(p)

rel = lambda p: os.path.relpath(p, GBA)
by_file = {}
for path, b, a in report:
    by_file.setdefault(rel(path), []).append((b, a))
for f in sorted(by_file):
    print("  %-52s %2d block%s" % (f, len(by_file[f]), '' if len(by_file[f]) == 1 else 's'))
print("\n  %d blocks in %d files" % (len(report), len(by_file)))

if overflow:
    print("\n  !! %d line(s) still over %dpx:" % (len(overflow), BUDGET))
    for path, w, line in overflow:
        print("     %3dpx  %-34s %s" % (w, rel(path), line))

if WRITE:
    for path, text in touched.items():
        open(path, "w", encoding="utf-8").write(text)
    print("\n  written: %d files" % len(touched))
sys.exit(1 if overflow else 0)

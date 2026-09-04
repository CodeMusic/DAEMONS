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
NAME_TOKEN = re.compile(r'\{(PLAYER|RIVAL|B_PLAYER_NAME|B_OPPONENT_NAME|B_BUFF\d|STR_VAR_\d)\}')

def textwidth(s):
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
NAMES.update(pairs_from("src/data/text/move_names.h",    r'_\("([^"]*)"\)'))
NAMES.update(pairs_from("src/data/items.json",           r'"english":\s*"([^"]*)"'))
# a rename is only safe to apply inside prose if the vanilla name is a word
NAMES = {k: v for k, v in NAMES.items()
         if k.isupper() and len(k) > 3 and k not in ("NONE", "????????")}

# ------------------------------------------------------ vocabulary, from GB
VOCAB = {
    "POKéDEX": "INDEX", "POKéDEXES": "INDEXES",
    "TRAINER": "USER", "TRAINERS": "USERS", "trainer": "USER", "trainers": "USERS",
    "ROCKET": "CORPUS", "ROCKETS": "CORPUS",
    "BADGE": "MARK", "BADGES": "MARKS", "badge": "MARK", "badges": "MARKS",
    "catch": "bind", "catches": "binds", "catching": "binding", "caught": "bound",
    "Catch": "Bind", "Caught": "Bound",
    "fainted": "HALTED", "faint": "HALT", "faints": "HALTS",
    "Gramps": "Gran", "BILL": "HOLT", "BILL's": "HOLT's",
    "PALLET": "BLANCHE", "VIRIDIAN": "CALLOW", "PEWTER": "SLATE",
    "CERULEAN": "DOLDRUM", "VERMILION": "ARDOR", "LAVENDER": "HALFTONE",
    "CELADON": "VERDIGRIS", "FUCHSIA": "LURID", "SAFFRON": "BRAZEN",
    "CINNABAR": "QUICKSILVER", "INDIGO": "UMBRA",
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

MON = re.compile(r'\bPOKéMON\b')

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

# An escape is two literal characters, and the first is a LETTER. So "\\nPOKéMON"
# has n immediately before P and \\b finds no boundary there -- every word at the
# start of a line was invisible to this. Stash the escapes behind a non-word
# sentinel first. (104 substitutions were silently missed before this.)
ESCAPE = re.compile(r'\\[nlp]')

def convert(body):
    stash = []
    def hide(m):
        stash.append(m.group(0)); return '\x01'
    body = ESCAPE.sub(hide, body)
    body = demon(body)
    def one(m):
        w = m.group(0)
        return VOCAB.get(w) or NAMES.get(w) or w
    # never touch the inside of a {CONTROL_CODE}
    out, last = [], 0
    for tok in re.finditer(r'\{[^}]*\}', body):
        out.append(WORD.sub(one, body[last:tok.start()])); out.append(tok.group(0))
        last = tok.end()
    out.append(WORD.sub(one, body[last:]))
    it = iter(stash)
    return re.sub('\x01', lambda _: next(it), ''.join(out))

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
        words = BREAK.sub(' ', page).split()
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
    return not ('\\n\\n' in body or '\\n ' in body or '\\p ' in body
                or body.startswith(' '))

# --------------------------------------------------------------- the files
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

print("  name renames learned from our own tables: %d" % len(NAMES))
print("  vocabulary entries: %d" % len(VOCAB))
print("  blocks changed: %d in %d files" % (changed, len(touched)))
if over:
    print("  !! %d line(s) over budget:" % len(over))
    for f, w, l in over[:10]:
        print("     %3dpx %-30s %s" % (w, f, l[:60]))
if WRITE:
    for p, t in touched.items():
        open(p, "w", encoding="utf-8").write(t)
    print("  written: %d files" % len(touched))
sys.exit(1 if over else 0)

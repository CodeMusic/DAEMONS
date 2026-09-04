#!/usr/bin/env python3
"""Carry the Game Boy build's WRITING into the GBA build.

    python3 tools/port_dialogue.py [--write] [--min 0.55] [MapName ...]

`port_vocab.py` made the GBA say DAEMON instead of POKéMON. It did not carry a
single sentence we wrote. That lives in `engine/text/` -- 165 files, and the
Quicksilver signs, SCORN SOLUTIONS over CLEAR LABORATORY, Holt's house, the
gyms are all in there.

**Nothing is matched on our own text, because our own text is the thing that
differs.** The pairing is done on VANILLA: Gen 1's original line against Gen 3's
original line, both taken from each fork's own `upstream/master`. Where those
two agree well enough, the Gen 3 block is the same NPC saying the same thing,
and our replacement belongs there. Labels are no help -- pokered calls it
`_CinnabarIslandSignText` and pokefirered calls it `CinnabarIsland_Text_IslandSign`
-- but the words survived the generation.

Two things this deliberately does not do. It does not touch a Gen 3 block whose
vanilla text has drifted too far to be sure of (FireRed rewrote a great deal),
and it does not invent a home for a Gen 1 block that has none. Both are
reported, because an unported line we know about is worth more than a line
dropped into the wrong mouth.
"""
import difflib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
MIN = 0.48
if "--min" in sys.argv:
    MIN = float(sys.argv[sys.argv.index("--min") + 1])
ONLY = [a for a in sys.argv[1:] if not a.startswith("-") and not re.match(r'^[\d.]+$', a)]
BUDGET = 196
MARGIN = 0.04   # the winner must beat the runner-up by this much
SURE   = 0.85   # ...unless it is this good, when a tie is between twins

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

# A SIGN IS NOT PROSE. pokered breaks "QUICKSILVER / The Metal That / Will Not
# Set" across three lines on purpose, and reflowing it to fill a wider Gen 3 box
# destroys the thing it is doing -- vanilla keeps its own signs broken the same
# way. pokered names these blocks ...SignText, so the intent is in the label.
def keep_shape(pages, budget):
    out = []
    for page in pages:
        lines = [l for l in page if l.strip()]
        fixed = []
        for l in lines:
            while textwidth(l) > budget:            # only split what cannot fit
                cut = l.rfind(' ', 0, len(l) - 1)
                if cut <= 0:
                    break
                head, l = l[:cut], l[cut + 1:]
                fixed.append(head)
            fixed.append(l)
        out.append(fixed[0] + ''.join(('\\n' if i == 0 else '\\l') + x
                                      for i, x in enumerate(fixed[1:])))
    return '\\p'.join(out) + '$'

def rewrap(pages, budget=BUDGET):
    out = []
    for page in pages:
        words = ' '.join(page).split()
        if not words:
            out.append(''); continue
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
    return '\\p'.join(out) + '$'

# --------------------------------------------------- Gen 1 text -> Gen 3 text
# pokered's tokens are few, and every one has an exact Gen 3 spelling.
TOKENS = [("#MONS", "DAEMONS"), ("#MON", "DAEMON"), ("#", "DAE"),
          ("<PLAYER>", "{PLAYER}"), ("<RIVAL>", "{RIVAL}"),
          ("<TARGET>", "{STR_VAR_1}"), ("<USER>", "{STR_VAR_2}"),
          ("<COLON>", ":"), ("<DOT>", "."), ("¥", "¥")]

def detok(s):
    for a, b in TOKENS:
        s = s.replace(a, b)
    return s.replace("@", "")

GB_LINE = re.compile(r'^\s*(text|line|cont|para|next|done|prompt|text_end|para_line|db)\b(.*)$')
GB_LABEL = re.compile(r'^_?(\w+)::')

def gb_blocks(source):
    """{label: [page, page, ...]} -- pages are flat prose."""
    blocks, label, pages, cur = {}, None, [], []
    def flush():
        if label:
            if cur:
                pages.append(list(cur))
            blocks[label] = [p for p in pages if any(x.strip() for x in p)]
    for raw in source.split('\n'):
        m = GB_LABEL.match(raw)
        if m:
            flush(); label, pages, cur = m.group(1), [], []
            continue
        m = GB_LINE.match(raw)
        if not m or label is None:
            continue
        kind, rest = m.group(1), m.group(2)
        q = re.findall(r'"([^"]*)"', rest)
        if kind in ('para', 'next') and cur:
            pages.append(list(cur)); cur = []
        if q:
            cur.append(detok(q[0]).strip())
    flush()
    return blocks

GBA_STR = re.compile(r'^\s*\.string "(.*)"\s*$')
GBA_LABEL = re.compile(r'^(\w+)::')
BREAK = re.compile(r'\\[nlp]')

def gba_blocks(source):
    blocks, label, run = {}, None, []
    for raw in source.split('\n'):
        m = GBA_LABEL.match(raw)
        if m:
            if label and run:
                blocks[label] = ''.join(run)
            label, run = m.group(1), []
            continue
        m = GBA_STR.match(raw)
        if m and label:
            run.append(m.group(1))
    if label and run:
        blocks[label] = ''.join(run)
    return blocks

def flat(s):
    """Comparable prose: no control codes, no case, no punctuation."""
    s = re.sub(r'\{[^}]*\}', ' ', s)
    s = BREAK.sub(' ', s).replace('$', ' ')
    return ' '.join(re.sub(r"[^a-z0-9' ]", ' ', s.lower()).split())

def show(repo, path):
    return subprocess.run(["git", "-C", repo, "show", "upstream/master:" + path],
                          capture_output=True, text=True).stdout

# ------------------------------------------------------- map name -> map dirs
GBA_MAPS = sorted(d for d in os.listdir(os.path.join(GBA, "data/maps"))
                  if os.path.isfile(os.path.join(GBA, "data/maps", d, "text.inc")))
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
GBA_NORM = {d: norm(d) for d in GBA_MAPS}

# pokered names a few places nothing in pokefirered is called.
ALIAS = {
    "OaksLab": "PalletTown_ProfessorOaksLab",
    "RedsHouse1F": "PalletTown_PlayersHouse_1F",
    "BluesHouse": "PalletTown_RivalsHouse",
    "BillsHouse": "Route25_SeaCottage",
    "CinnabarLab": "CinnabarIsland_PokemonLab_Entrance",
    "CinnabarLabTradeRoom": "CinnabarIsland_PokemonLab_Lounge",
    "CinnabarLabFossilRoom": "CinnabarIsland_PokemonLab_ExperimentRoom",
    "CinnabarLabMetronomeRoom": "CinnabarIsland_PokemonLab_ResearchRoom",
    "Museum1F": "PewterCity_Museum_1F", "Museum2F": "PewterCity_Museum_2F",
    "IndigoPlateauLobby": "IndigoPlateau_PokemonCenter_1F",
    "PewterNidoranHouse": "PewterCity_House1",
    "MrFujisHouse": "LavenderTown_VolunteerPokemonHouse",
    "MtMoonPokecenter": "Route4_PokemonCenter_1F",
    "RockTunnelPokecenter": "Route10_PokemonCenter_1F",
    "CeladonDiner": "CeladonCity_Restaurant",
    "CeladonMansionRoofHouse": "CeladonCity_Condominiums_RoofRoom",
    "CeladonMart1F": "CeladonCity_DepartmentStore_1F",
    "CeladonMart2F": "CeladonCity_DepartmentStore_2F",
    "CeladonMart3F": "CeladonCity_DepartmentStore_3F",
    "CeladonMart4F": "CeladonCity_DepartmentStore_4F",
    "CeladonMartRoof": "CeladonCity_DepartmentStore_Roof",
    "Route11Gate1F": "Route11_EastEntrance_1F",
    "Route11Gate2F": "Route11_EastEntrance_2F",
    "Route12Gate2F": "Route12_NorthEntrance_2F",
    "Route12SuperRodHouse": "Route12_FishingHouse",
    "Route15Gate1F": "Route15_WestEntrance_1F",
    "Route16Gate2F": "Route16_NorthEntrance_2F",
    "Route18Gate2F": "Route18_EastEntrance_2F",
    "SSAnneBow": "SSAnne_Deck",
    "SaffronGates": "SaffronCity_Connection",
    "ViridianForestSouthGate": "Route2_ViridianForest_SouthEntrance",
    "ViridianForestNorthGate": "Route2_ViridianForest_NorthEntrance",
    "Route2Gate": "Route2_EastBuilding",
    "Route5Gate": "Route5_SouthEntrance",
    "Route6Gate": "Route6_NorthEntrance",
    "Route7Gate": "Route7_EastEntrance",
    "Route8Gate": "Route8_WestEntrance",
    "UndergroundPathEntranceRoute5": "UndergroundPath_NorthEntrance",
    "UndergroundPathEntranceRoute6": "UndergroundPath_SouthEntrance",
    "UndergroundPathEntranceRoute7": "UndergroundPath_WestEntrance",
    "UndergroundPathEntranceRoute8": "UndergroundPath_EastEntrance",
}
# Not every pokered text file is a map. These live in data/text/ on both sides.
NONMAP = {"pokedex_ratings": "data/text/pokedex_rating.inc",
          "oakspeech":       "data/text/new_game_intro.inc"}

# a few Gen 1 rooms have several plausible Gen 3 homes; let the scoring choose
MULTI = {"FuchsiaBillsGrandpasHouse": ["FuchsiaCity_House1", "FuchsiaCity_House2",
                                       "FuchsiaCity_House3"]}

def candidates(gbname):
    if gbname in NONMAP:
        return [NONMAP[gbname]]
    if gbname in MULTI:
        return MULTI[gbname]
    if gbname in ALIAS:
        return [ALIAS[gbname]]
    n = norm(gbname)
    exact = [d for d, v in GBA_NORM.items() if v == n]
    if exact:
        return exact
    part = [d for d, v in GBA_NORM.items() if v.endswith(n) or n in v]
    if part:
        return sorted(part, key=len)[:4]
    close = difflib.get_close_matches(n, list(GBA_NORM.values()), n=3, cutoff=0.72)
    return [d for d, v in GBA_NORM.items() if v in close]

# ----------------------------------------------------------------- the port
gb_files = subprocess.run(["git", "-C", GB, "diff", "--name-only", "upstream/master", "--", "text/"],
                          capture_output=True, text=True).stdout.split()
matched, unmatched, nomap, edits = [], [], [], {}

for rel in gb_files:
    name = os.path.basename(rel)[:-4]
    if ONLY and name not in ONLY:
        continue
    ours = gb_blocks(open(os.path.join(GB, rel), encoding="utf-8", errors="replace").read())
    base = gb_blocks(show(GB, rel))
    changed = {k: v for k, v in ours.items() if base.get(k) != v and v}
    if not changed:
        continue
    maps = candidates(name)
    if not maps:
        nomap += [(name, k) for k in changed]
        continue
    pool = []   # (path, label, vanilla_flat)
    for d in maps:
        p = d if d.endswith(".inc") else "data/maps/%s/text.inc" % d
        for lbl, body in gba_blocks(show(GBA, p)).items():
            pool.append((p, lbl, flat(body)))
    for lbl, pages in changed.items():
        want = flat(' '.join(' '.join(pg) for pg in base.get(lbl, [])))
        if not want:
            unmatched.append((name, lbl, 0.0)); continue
        ranked = sorted(((difflib.SequenceMatcher(None, want, van, autojunk=False).ratio(),
                          d, glbl) for d, glbl, van in pool), reverse=True)
        score, best = (ranked[0][0], ranked[0][1:]) if ranked else (0.0, None)
        second = ranked[1][0] if len(ranked) > 1 else 0.0
        # A near-tie means two Gen 3 lines fit the Gen 1 line equally well, and
        # putting our writing in the wrong NPC's mouth is worse than not
        # porting it. MARGIN is what stops that; the threshold alone does not.
        # The margin guards against a COIN FLIP, not against a strong match.
        # Bill's two lines scored 0.94 and 0.98 and were thrown out for being
        # near-ties -- but at that similarity the vanilla sentences are the same
        # sentence, and the worst case is porting to one of two twins rather
        # than putting our writing in a stranger's mouth.
        if best and score >= MIN and (score - second >= MARGIN or score >= SURE):
            matched.append((name, lbl, best[0], best[1], score))
            shaped = keep_shape if "Sign" in lbl else rewrap
            edits.setdefault(best[0], {})[best[1]] = shaped(pages, BUDGET)
        else:
            unmatched.append((name, lbl, score))

print("  matched   %d" % len(matched))
print("  unmatched %d   (no Gen 3 counterpart above %.2f)" % (len(unmatched), MIN))
print("  no map    %d" % len(nomap))
if nomap:
    print("    ", ", ".join(sorted({n for n, _ in nomap})[:12]))

if WRITE:
    files = 0
    for d, subs in edits.items():
        p = os.path.join(GBA, d if d.endswith(".inc") else "data/maps/%s/text.inc" % d)
        lines = open(p, encoding="utf-8").read().split('\n')
        out, i, hit = [], 0, False
        while i < len(lines):
            m = GBA_LABEL.match(lines[i])
            if not m or m.group(1) not in subs:
                out.append(lines[i]); i += 1; continue
            out.append(lines[i]); i += 1
            while i < len(lines) and GBA_STR.match(lines[i]):
                i += 1
            body = subs[m.group(1)]
            out += ['    .string "%s"' % s for s in re.split(r'(?<=\\[nlp])', body) if s]
            hit = True
        if hit:
            open(p, "w", encoding="utf-8").write('\n'.join(out)); files += 1
    print("  written: %d files" % files)

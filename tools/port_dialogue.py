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
def panel(lbl, pages):
    """A PANEL keeps its shape; PROSE ON A SIGN does not.

    QUICKSILVER / The Metal That / Will Not Set is one panel and its three
    lines are the design. The Quicksilver requisitions board is five pages of
    sentences that merely happen to be mounted on a wall, and keeping Gen 1's
    eighteen-character wrap there just wastes a box twice as wide."""
    return "Sign" in lbl and len(pages) <= 2

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

def join(lines):
    """Gen 1 hyphenates across its narrow lines -- "Counter-" / "signed." --
    and joining those with a space gives "Counter- signed".

    But a route sign reads "BLANCHE TOWN -" / "CALLOW CITY", where the dash is
    punctuation and the space belongs. The two are told apart by what sits
    BEFORE the hyphen: attached to a letter it is a broken word, after a space
    it is a dash."""
    text = ""
    for l in lines:
        if text.endswith('-') and len(text) > 1 and text[-2] != ' ':
            text = text[:-1] + l.lstrip()
        else:
            text = (text + ' ' + l).strip() if text else l
    return text

def rewrap(pages, budget=BUDGET):
    out = []
    for page in pages:
        words = join(page).split()
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
# #DEX must come first, and it becomes POKéDEX rather than DAEDEX: pokered's #
# is the glyph the Game Boy build repointed at DAE, but for MATCHING we want
# Gen 1's vanilla line to read like Gen 3's vanilla line. port_vocab.py turns
# POKéDEX into INDEX afterwards, everywhere, which is where that rename lives.
TOKENS = [("#DEX", "POKéDEX"),
          ("#MONS", "DAEMONS"), ("#MON", "DAEMON"), ("#", "DAE"),
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
    "CeruleanBadgeHouse": "CeruleanCity_House1",     # "MARKS have amazing secrets"
    "CeruleanTrashedHouse": "CeruleanCity_House2",   # the one CORPUS broke into
    "SafariZoneGate": "FuchsiaCity_SafariZone_Entrance",
    "SafariZoneEntranceMatt": "FuchsiaCity_SafariZone_Entrance",
    "PewterGym_2": "PewterCity_Gym",
    "ViridianGym_2": "ViridianCity_Gym",
    "SaffronPokecenter": "SaffronCity_PokemonCenter_1F",
    # pokered's Celadon MANSION is the apartment block in Celadon, where the
    # game designer lives. It is NOT the Pokemon Mansion on Cinnabar, which is
    # what a fuzzy name match reaches for -- and did.
    "CeladonMansion1F": "CeladonCity_Condominiums_1F",
    "CeladonMansion2F": "CeladonCity_Condominiums_2F",
    "CeladonMansion3F": "CeladonCity_Condominiums_3F",
    "CeladonMansionRoof": "CeladonCity_Condominiums_Roof",
    "Route22Gate": "Route22_NorthEntrance",
    "UndergroundPathRoute6": "UndergroundPath_SouthEntrance",
    "UndergroundPathRoute7": "UndergroundPath_WestEntrance",
    "UndergroundPathRoute8": "UndergroundPath_EastEntrance",
}

# pokered calls it <Town>Pokecenter; pokefirered calls it <Town>City_PokemonCenter_1F.
# Nineteen maps follow that rule, so state the rule rather than nineteen aliases.
POKECENTER = re.compile(r'^(\w+?)Pokecenter$')
# Not every pokered text file is a map. These live in data/text/ on both sides.
NONMAP = {"pokedex_ratings": "data/text/pokedex_rating.inc",
          "oakspeech":       "data/text/new_game_intro.inc"}

# a few Gen 1 rooms have several plausible Gen 3 homes; let the scoring choose
MULTI = {"FuchsiaBillsGrandpasHouse": ["FuchsiaCity_House1", "FuchsiaCity_House2",
                                       "FuchsiaCity_House3"]}

def candidates(gbname):
    pc = POKECENTER.match(gbname)
    if pc and gbname not in ALIAS:
        town = norm(pc.group(1))
        hit = [d for d in GBA_MAPS
               if GBA_NORM[d].startswith(town) and GBA_NORM[d].endswith("pokemoncenter1f")]
        if hit:
            return hit
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


# Where the scoring could not decide and a person could. Gen 1 and Gen 3 say
# these things in different words, so vanilla-against-vanilla finds nothing --
# but the NPC is the same NPC and the line is doing the same job.
MANUAL = {
    "BrunosRoom": {
        # Gen 3 has an intro AND a rematch intro, near-identical; ours is the
        # first meeting. This is the tie the margin correctly refused to break.
        "BrunoBeforeBattleText": ("PokemonLeague_BrunosRoom", "PokemonLeague_BrunosRoom_Text_Intro"),
    },
    "OaksLab": {
        "OaksLabOak1WhichPokemonDoYouWantText":
            ("PalletTown_ProfessorOaksLab", "PalletTown_ProfessorOaksLab_Text_OakWhichOneWillYouChoose"),
        "OaksLabYouWantBulbasaurText":
            ("PalletTown_ProfessorOaksLab", "PalletTown_ProfessorOaksLab_Text_OakChoosingBulbasaur"),
        "OaksLabYouWantCharmanderText":
            ("PalletTown_ProfessorOaksLab", "PalletTown_ProfessorOaksLab_Text_OakChoosingCharmander"),
        "OaksLabYouWantSquirtleText":
            ("PalletTown_ProfessorOaksLab", "PalletTown_ProfessorOaksLab_Text_OakChoosingSquirtle"),
    },
    "RocketHideoutB4F": {
        "RocketHideoutB4FGiovanniImpressedYouGotHereText":
            ("RocketHideout_B4F", "RocketHideout_B4F_Text_GiovanniIntro"),
    },
    "ViridianCity": {
        "ViridianCityOldManYouNeedToWeakenTheTargetText":
            ("ViridianCity", "ViridianCity_Text_WeakenMonsFirstToCatch"),
    },
    "ViridianForest": {
        # the type chart, cut into a stone older than the path
        "ViridianForestTrainerTips3Text":
            ("ViridianForest", "ViridianForest_Text_CantCatchOwnedMons"),
        "ViridianForestYoungster5Text":
            ("ViridianForest", "ViridianForest_Text_RanOutOfPokeBalls"),
    },
}

# Gen 1 splits the award and the explanation across two blocks; Gen 3 says both
# in one, wrapped around the fanfare. Two into one cannot be done by pairing, and
# the control codes are the badge jingle, so this block is written out.
MANUAL_TEXT = {
    ("PewterCity_Gym", "PewterCity_Gym_Text_BrockDefeat"):
        r"I took you for granted, and so I\nlost.\p"
        r"Proof, then. Something you can\nhold.\p"
        r"{FONT_NORMAL}{PLAYER} received the SLATE MARK\nfrom CAIRN!"
        r"{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\p"
        r"{FONT_MALE}An official mark from BENCHMARK 1.\p"
        r"Its bearer's daemons become more\npowerful.\p"
        r"FLASH can now be used any time.\p"
        r"Of course, a daemon must know the\nmove FLASH to use it.$",
}

# In the game, but not by pairing. Two are ours outright and were placed as new
# bg_events -- they replace no vanilla line, so there is nothing to match them
# against. Two more were MERGED: Gen 1 splits the award and the explanation and
# Gen 3 says both in one block, so they live in MANUAL_TEXT above. Listing them
# keeps them out of the "still needs a home" report without pretending they
# were paired.
HANDLED = {("PokemonMansion1F", "PokemonMansion1FIterLogText"),
           ("SilphCo1F", "SilphCo1FEngravingText"),
           ("PewterGym_2", "PewterGymBrockBoulderBadgeInfoText"),
           ("PewterGym_2", "PewterGymBrockReceivedBoulderBadgeText")}

# ----------------------------------------------------------------- the port
# A block whose only edit was VOCABULARY has nothing to port: port_vocab.py
# already made that change on the Gen 3 side, independently and everywhere.
# Without this, "TRAINER TIPS" -> "USER TIPS" reads as unported writing and the
# remaining list is twice as long as the actual work.
def _tool(name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(ROOT, "tools/%s.py" % name))
    mod = importlib.util.module_from_spec(spec)
    out, sys.stdout = sys.stdout, open(os.devnull, "w")
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    finally:
        sys.stdout.close(); sys.stdout = out
    return mod

VOCAB = _tool("port_vocab")
# port_oak owns OAK -> CRYSTAL CLEAR and her pronouns; without it every line
# whose only edit was the professor's name reads as unported writing.
OAK = _tool("port_oak")

def vocabulary_only(vanilla_pages, our_pages):
    """Is our edit nothing but the rename the GBA already has?"""
    j = lambda ps: ' '.join(' '.join(p) for p in ps)
    van, our = j(vanilla_pages), j(our_pages)
    if not van:
        return False
    a, b = flat(VOCAB.convert(OAK.rename(van))), flat(our)
    return a == b or difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() > 0.97

gb_files = subprocess.run(["git", "-C", GB, "diff", "--name-only", "upstream/master", "--", "text/"],
                          capture_output=True, text=True).stdout.split()
matched, unmatched, nomap, vocab_only, handled, edits = [], [], [], [], [], {}

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
        if (name, lbl) in HANDLED:
            handled.append((name, lbl)); continue
        hand = MANUAL.get(name, {}).get(lbl)
        if hand:
            matched.append((name, lbl, hand[0], hand[1], 1.0))
            shaped = keep_shape if panel(lbl, pages) else rewrap
            edits.setdefault(hand[0], {})[hand[1]] = shaped(pages, BUDGET)
            continue
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
            shaped = keep_shape if panel(lbl, pages) else rewrap
            edits.setdefault(best[0], {})[best[1]] = shaped(pages, BUDGET)
        elif vocabulary_only(base.get(lbl, []), pages):
            vocab_only.append((name, lbl))
        else:
            unmatched.append((name, lbl, score))

print("  matched   %d" % len(matched))
print("  handled elsewhere %d   (new signs, and two merged into one Gen 3 block)" % len(handled))
print("  vocabulary only %d   (already done by port_vocab; nothing to carry)" % len(vocab_only))
print("  unmatched %d   (real writing, no Gen 3 counterpart above %.2f)" % (len(unmatched), MIN))
print("  no map    %d" % len(nomap))
if nomap:
    print("    ", ", ".join(sorted({n for n, _ in nomap})[:12]))

for (d, glbl), body in MANUAL_TEXT.items():
    edits.setdefault(d, {})[glbl] = body

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

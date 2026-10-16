#!/usr/bin/env python3
"""C-03 (daemons-companion): one export of what the goal companion needs to know about DAEMONS, so nothing is typed
twice.

    python3 tools/companion_export.py            # report: what would change in companion/server/data/
    python3 tools/companion_export.py --write    # write it
    python3 tools/companion_export.py --check    # exit 1 if the companion's data is stale (the push routine, T-373)

Writes three files into the companion repo (symlinked here as companion/, setup.sh step 5):

  species.json  every species the save can hold, keyed by the game's INTERNAL species id (what a save stores), with
                its national INDEX number, our name, our types, the INDEX category, both editions' entries (CONTENT is
                FireRed's pokedex_text_fr.h, CONTEXT LeafGreen's pokedex_text_lg.h), and its art in gfx/daemons/
  charmap.json  the game's text encoding, byte -> character, for reading nicknames and names out of a save
  week.json     the week as the game keeps it: Sunday first, each day's colour (day_trims.h, the CHECKPOINT's trim)
                and its note, C to B (vision 9.21)
  seasons.json  the seasons by edition (C-14), from tools/seasons.py -- the one definition the game shares
  save_layout.json  the save's sectors, sizes and offsets, read from the built game (C-02)
  profile_layout.json  where the PROFILE's facts live in the save, from global.h and flags.h (C-23)
  maps.json     every map by the numbers a save stores, with its place's name (C-23)
  margins.json  OPUS's margins, and the game's rule for which line shows (C-24, T-373)
  items.json    every item by id, our name and description, for what an AWAY daemon holds (C-31)
  events.json   the GAME EVENTS, in story order, and the flags that say each is held (C-128)
  school.json   CALLOW SCHOOL: each floor's subject, syllabus and board, the paper, the DIPLOMA (C-129)

Everything is read from the engine's sources and the art folder; nothing of Nintendo's is copied -- our names, our
entries and our art only.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(ROOT, "companion", "server", "data")
WRITE = "--write" in sys.argv


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8").read()


def gba_string(body):
    """the text of a _("...") or a run of "..." lines, with the line breaks as \\n"""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', body)
    return "".join(parts).replace("\\n", "\n").replace("\\p", "\n\n")


def native_values():
    """{SPECIES_X: the packed u16 tools/gbanative.py writes into the ROM} -- one source for the game and the companion."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gbanative
    return {sp: gbanative.pack(h) for sp, h in gbanative.homes().items()}


def native_of(v):
    """T-407: what the INDEX's NATIVE box says, as data. None: not met in the wild. A list is null when it is every
    one (any season, any hour, both editions). grove is the universe's name (THE NEXUS for the NEXUS) -- the game
    shows A GROVE until the daemon has been seen, and so should the companion."""
    if not v:
        return None
    import gbagrove, gbanexusmap, gbanative
    seasons = [x for i, x in enumerate(gbanative.SEASONS) if v >> (4 + i) & 1]
    hours = [x for i, x in enumerate(gbanative.WATCHES) if v >> (8 + i) & 1]
    editions = [x for i, x in enumerate(("CONTENT", "CONTEXT")) if v >> (2 + i) & 1]
    g = v >> 12
    grove = None if not g else "THE NEXUS" if g == gbanative.NEXUS else \
        gbanexusmap.UNIVERSES[gbagrove.GROVES[g - 1]["name"]][0]
    return {"regions": [x for i, x in enumerate(("GAMUT", "THE MARGINS")) if v >> i & 1],
            "editions": editions if len(editions) < 2 else None,
            "seasons": seasons if len(seasons) < 4 else None,
            "hours": hours if len(hours) < 4 else None,
            "grove": grove}


def species_table():
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define SPECIES_(\w+)\s+(\d+)\b", read("include/constants/species.h"))}
    dex = re.findall(r"NATIONAL_DEX_(\w+)\s*,", read("include/constants/pokedex.h"))
    national = {name: i for i, name in enumerate(dex)}                       # NATIONAL_DEX_NONE is 0
    to_nat = set(re.findall(r"SPECIES_TO_NATIONAL\((\w+)\)", read("src/pokemon.c")))   # every species the INDEX numbers
    # T-395: a NEXUS resident is a slot under another name (SPECIES_REFLECTION is SPECIES_OLD_UNOWN_C), and the
    # INDEX numbers it by that name: its national entry, category and text are keyed REFLECTION, not OLD_UNOWN_C
    alias = {a: b for a, b in re.findall(r"#define SPECIES_(\w+)\s+SPECIES_(\w+)\b", read("include/constants/species.h"))}
    by_slot = {b: a for a, b in alias.items()}
    to_nat |= {alias[n] for n in re.findall(r"^\s*NATIONAL_DEX_(\w+),\s*$", read("src/pokemon.c"), re.M) if n in alias}
    names = dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/data/text/species_names.h")))
    typename = dict(re.findall(r'\[TYPE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/battle_main.c")))
    info = read("src/data/pokemon/species_info.h")
    types = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{((?:(?!\[SPECIES_).)*)", info, re.S):   # a body ends at the next species ([SPECIES_NONE] = {0}, is one line)
        t = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+)\s*,\s*TYPE_(\w+)\s*\}", m.group(2))
        if t:
            pair = [typename.get(t.group(1), t.group(1))]
            if t.group(2) != t.group(1):
                pair.append(typename.get(t.group(2), t.group(2)))
            types[m.group(1)] = pair
    entries = read("src/data/pokemon/pokedex_entries.h")
    cat, desc = {}, {}
    for m in re.finditer(r"\[NATIONAL_DEX_(\w+)\]\s*=\s*\{((?:(?!\[NATIONAL_DEX_).)*)", entries, re.S):
        c = re.search(r'\.categoryName\s*=\s*_\("([^"]*)"\)', m.group(2))
        d = re.search(r"\.description\s*=\s*(\w+)", m.group(2))
        if c:
            cat[m.group(1)] = c.group(1)
        if d:
            desc[m.group(1)] = d.group(1)
    texts = {}
    for edition, rel in (("CONTENT", "src/data/pokemon/pokedex_text_fr.h"), ("CONTEXT", "src/data/pokemon/pokedex_text_lg.h")):
        texts[edition] = {m.group(1): gba_string(m.group(2))
                          for m in re.finditer(r"const u8 (\w+)\[\]\s*=\s*_\((.*?)\);", read(rel), re.S)}
    art = set(os.listdir(os.path.join(ROOT, "gfx", "daemons")))
    body = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{((?:(?!\[SPECIES_).)*)", info, re.S):
        t = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+)", m.group(2))
        if t:
            body[m.group(1)] = TYPE_ORDER.index(t.group(1)) if t.group(1) in TYPE_ORDER else None
    streaky = set(re.findall(r"\[SPECIES_(\w+)\]\s*=\s*TRUE", read("src/data/pokemon/streaks.h")))
    # C-24: its growth rate, so a boxed daemon's level can be read from its experience (OPUS's margins need it)
    growth_names = ["MEDIUM_FAST", "ERRATIC", "FLUCTUATING", "MEDIUM_SLOW", "FAST", "SLOW"]   # constants/pokemon.h
    growth = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{((?:(?!\[SPECIES_).)*)", info, re.S):
        g = re.search(r"\.growthRate\s*=\s*GROWTH_(\w+)", m.group(2))
        if g and g.group(1) in growth_names:
            growth[m.group(1)] = growth_names.index(g.group(1))
    # C-45: its base stats, so a daemon that grew on the device comes home with the stats the game would give it
    base = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{((?:(?!\[SPECIES_).)*)", info, re.S):
        got = [re.search(r"\.%s\s*=\s*(\d+)" % f, m.group(2)) for f in
               ("baseHP", "baseAttack", "baseDefense", "baseSpeed", "baseSpAttack", "baseSpDefense")]
        if all(got):
            base[m.group(1)] = [int(x.group(1)) for x in got]

    native = native_values()
    out = {}
    for sp, sid in sorted(ids.items(), key=lambda kv: kv[1]):
        if sp not in to_nat or sp not in names:
            continue
        nat = national.get(by_slot.get(sp), national.get(sp))
        stem = re.sub(r"[^a-z0-9_]", "", names[sp].lower().replace(" ", "_"))   # LEMMA MIND -> lemma_mind
        sym = desc.get(sp, desc.get(by_slot.get(sp)))
        row = {
            "constant": sp,
            "national": nat,
            "name": names[sp],
            "types": types.get(sp, []),
            "category": cat.get(sp, cat.get(by_slot.get(sp))),
            "entry": {ed: texts[ed].get(sym) for ed in ("CONTENT", "CONTEXT")},
            "art": {view: ("gfx/daemons/%s_%s.png" % (stem, view)) if ("%s_%s.png" % (stem, view)) in art else None
                    for view in ("front", "back")},
            "bodyType": body.get(sp),                  # C-18: the type its palette ramp was built from
            "streaks": sp in streaky,                  # C-18: palette 11..14 carry its four routines' streaks
            "growth": growth.get(sp, 0),               # C-24: GROWTH_*, MEDIUM_FAST where a macro hides it
            "base": base.get(sp),                      # C-45: HP, Attack, Defense, Speed, Sp.Atk, Sp.Def
            "native": native_of(native.get("SPECIES_" + sp, 0)),   # T-407: the INDEX's NATIVE box, as data
        }
        out[str(sid)] = row
    # T-395: the save keeps an INDEX bit per national number up to NUM_SPECIES rounded to a byte (DEX_FLAGS_NO, 416);
    # the eight NEXUS residents pushed the unused slots past it, and a number the save cannot hold reads the next array
    flag_bits = 8 * ((ids["EGG"] + 7) // 8)
    for row in out.values():
        if row["national"] and row["national"] > flag_bits:
            row["national"] = None
    return out


TYPE_ORDER = ["NORMAL", "FIGHTING", "FLYING", "POISON", "GROUND", "ROCK", "BUG", "GHOST", "STEEL", "MYSTERY",
              "FIRE", "WATER", "GRASS", "ELECTRIC", "PSYCHIC", "ICE", "DRAGON", "DARK"]      # include/constants/pokemon.h


def rgb8(r, g, b):
    return [(c << 3) | (c >> 2) for c in (r, g, b)]


def streaks_table():
    """C-18: the game's streak colours (src/data/pokemon/streaks.h, tools/genstreaks.py), [body type][move type]."""
    src = read("src/data/pokemon/streaks.h")
    colours = []
    for body in TYPE_ORDER:
        row = re.search(r"\[TYPE_%s\] = \{(.*?)\},\n" % body, src).group(1)
        cells = dict(re.findall(r"\[TYPE_(\w+)\] = RGB\((\d+), (\d+), (\d+)\)", row) and
                     [(t, rgb8(int(r), int(g), int(b))) for t, r, g, b in
                      re.findall(r"\[TYPE_(\w+)\] = RGB\((\d+), (\d+), (\d+)\)", row)])
        colours.append([cells.get(t) for t in TYPE_ORDER])
    blank = rgb8(*map(int, re.search(r"gStreakBlank = RGB\((\d+), (\d+), (\d+)\)", src).groups()))
    return {"_about": "the game's streak colours: colours[body type][move type], 8-bit RGB; a move slot with no move takes "
                      "the body palette's index 3; palette indices 11..14 are the four slots, in order",
            "types": TYPE_ORDER, "colours": colours, "blank": blank, "first_index": 11, "body_mid_index": 3}


def moves_table():
    """C-18: each move's type, by the game's move id."""
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define MOVE_(\w+)\s+(\d+)\b", read("include/constants/moves.h"))}
    out = {}
    for m in re.finditer(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \}", read("src/data/battle_moves.h"), re.S):
        t = re.search(r"\.type\s*=\s*TYPE_(\w+)", m.group(2))
        if t and m.group(1) in ids and t.group(1) in TYPE_ORDER:
            out[str(ids[m.group(1)])] = TYPE_ORDER.index(t.group(1))
    return out


def routines_table():
    """C-68: the names the game prints for each move (a routine) and each type, for GAME ROUTINES on the handhelds."""
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define MOVE_(\w+)\s+(\d+)\b", read("include/constants/moves.h"))}
    names = {}
    for m in re.finditer(r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/data/text/move_names.h")):
        if m.group(1) in ids and ids[m.group(1)]:
            names[str(ids[m.group(1)])] = m.group(2)
    types = dict(re.findall(r'\[TYPE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/battle_main.c")))
    return {"_about": "the game's move (routine) names by move id, and its type names in moves.json's type order",
            "types": [types.get(t, t) for t in TYPE_ORDER], "moves": names}


def party_art(species):
    """C-18: each daemon as the game draws it -- its built front sprite (graphics/pokemon/<slot>/front.4bpp) in its
    normal palette, an indexed PNG whose palette the server rewrites per daemon (11..14, its routines). Only species
    with our own drawing in gfx/daemons/ are exported, so nothing of Nintendo's is ever copied."""
    from PIL import Image
    out = {}
    for sid, row in species.items():
        if not row["art"]["front"]:
            continue
        d = os.path.join(GBA, "graphics/pokemon", row["constant"].lower())
        if not os.path.isdir(d):        # T-395: a NEXUS resident's folder is named for it (nexus_reflection)
            d = os.path.join(GBA, "graphics/pokemon", "nexus_" + row["name"].lower())
        tiles, pal = os.path.join(d, "front.4bpp"), os.path.join(d, "normal.gbapal")
        if not (os.path.exists(tiles) and os.path.exists(pal)):
            continue
        raw, praw = open(tiles, "rb").read(), open(pal, "rb").read()
        colours = []
        for i in range(16):
            c = int.from_bytes(praw[2 * i:2 * i + 2], "little")
            colours += rgb8(c & 31, (c >> 5) & 31, (c >> 10) & 31)
        im = Image.new("P", (64, 64), 0)
        px = im.load()
        for t in range(64):
            for y in range(8):
                for x in range(8):
                    b = raw[t * 32 + y * 4 + x // 2]
                    px[(t % 8) * 8 + x, (t // 8) * 8 + y] = (b >> 4) if x & 1 else b & 15
        im.putpalette(colours + [0] * (768 - len(colours)))
        name = os.path.basename(row["art"]["front"]).replace("_front.png", "") + ".png"
        out[name] = im
    return out


def charmap_table():
    table = {}
    for line in read("charmap.txt").splitlines():
        m = re.match(r"^'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if m and m.group(2).upper() not in table:
            table[m.group(2).upper()] = m.group(1)
    return {"_about": "byte (hex) -> character; 0xFF ends a string", "bytes": table}


#  The Xenith week (the user's own framework and the Programmer's Guide, as the user gave it 2026-10-07): each day's
#  centre, its virtue and the vice it cures, and the theme word. The colour and the note are the game's own week
#  (day_trims.h, vision 9.21).
XENITH_DAYS = [
    ("red",    "Root",         "Chastity",    "Lust",     "Passion"),
    ("orange", "Sacral",       "Temperance",  "Gluttony", "Development"),
    ("yellow", "Solar Plexus", "Charity",     "Greed",    "Connection"),
    ("green",  "Heart",        "Diligence",   "Sloth",    "Growth"),
    ("blue",   "Throat",       "Forgiveness", "Wrath",    "Calm"),
    ("indigo", "Third Eye",    "Kindness",    "Envy",     "Intuition"),
    ("violet", "Crown",        "Humility",    "Pride",    "Flow"),
]


def week_table():
    trims = re.findall(r"RGB\((\d+),\s*(\d+),\s*(\d+)\),\s*//\s*(\w+),\s*([A-G])", read("src/data/day_trims.h"))
    days = []
    for r, g, b, day, note in trims:
        hexc = "#%02X%02X%02X" % tuple(int(v) * 255 // 31 for v in (r, g, b))
        hue, chakra, virtue, shadow, theme = XENITH_DAYS[len(days)]
        days.append({"day": day.capitalize(), "colour": hexc, "hue": hue, "note": note, "chakra": chakra,
                     "virtue": virtue, "shadow": shadow, "cue": "%s cures %s" % (virtue, shadow), "theme": theme})
    return {"_about": "Sunday first; each day's colour is the CHECKPOINT's trim (day_trims.h) and its note C to B "
                      "(vision 9.21); its hue, chakra, the virtue and the vice it cures, and the theme are the "
                      "user's Xenith week (companion C-73).",
            "days": days}


#  C-02 / T-358: the two bits of a daemon's flags byte (struct BoxPokemon, byte 19: isBadEgg, hasSpecies, isEgg,
#  blockBoxRS, then unused:4) that carry the companion's link. T-358 defines them in the engine; until then they are
#  named here, and both must agree.
AWAY_BIT, ASKED_BIT = 4, 5


def save_layout():
    """C-02: what a save reader needs, read from the BUILT game (the ELF's symbol sizes, global.h's offsets), so a
    change to the save blocks reaches the companion. Both editions must agree; without a build, nothing is written."""
    import subprocess
    sizes = {}
    for elf in ("daemonsContent.elf", "daemonsContext.elf"):
        path = os.path.join(GBA, elf)
        if not os.path.exists(path):
            return None
        out = subprocess.run(["arm-none-eabi-nm", "-S", path], capture_output=True, text=True).stdout
        got = {m.group(2): int(m.group(1), 16) for m in re.finditer(r"^[0-9a-f]+ ([0-9a-f]+) [BbDd] (gSaveBlock1|gSaveBlock2|gPokemonStorage)$", out, re.M)}
        if sizes and got != sizes:
            raise SystemExit("  refused: the two editions' save blocks differ: %s" % elf)
        sizes = got
    g = read("include/global.h")
    def off(field):
        m = re.search(r"/\*0x([0-9A-Fa-f]+)\*/\s*(?:u8|struct Pokemon)\s+%s\b" % re.escape(field), g)
        return int(m.group(1), 16)
    return {"_about": "the Gen 3 save as this game writes it: two slots of 14 sectors (0x1000 each: 3968 bytes of data, "
                      "then id u16 at 0xFF4, checksum u16 at 0xFF6, signature u32 0x08012025 at 0xFF8, counter u32 at "
                      "0xFFC); a section's checksum is the u32 sum of its data, folded (high half + low half). "
                      "Sizes from the built ELF.",
            "sector_size": 0x1000, "sector_data_size": 3968, "sectors_per_slot": 14, "signature": 0x08012025,
            "saveblock2_size": sizes["gSaveBlock2"], "saveblock1_size": sizes["gSaveBlock1"],
            "storage_size": sizes["gPokemonStorage"],
            "party_count_offset": off("playerPartyCount"), "party_offset": off("playerParty"),
            "pokemon_size": 100, "box_pokemon_size": 80, "level_offset": 84,
            "flags_byte": 19, "away_bit": AWAY_BIT, "asked_bit": ASKED_BIT,
            # C-45: sNatureStatTable (pokemon.c), by nature: Attack, Defense, Speed, Sp.Atk, Sp.Def, each +1, -1 or 0
            "natures": natures_table()}


def natures_table():
    body = re.search(r"sNatureStatTable\[NUM_NATURES\]\[NUM_NATURE_STATS\]\s*=\s*\{(.*?)\};", read("src/pokemon.c"), re.S).group(1)
    rows = re.findall(r"\[NATURE_\w+\]\s*=\s*\{([^}]*)\}", body)
    return [[int(v) for v in r.replace("+", "").split(",")] for r in rows]


def struct_offsets(text, struct):
    """{field: offset} for one struct in a header, from its /*0xNN*/ comments -- so a field is found in ITS struct (a
    name like flags appears in two save blocks)."""
    m = re.search(r"^struct %s\s*\{(.*?)^\};" % re.escape(struct), text, re.M | re.S)
    if not m:
        raise SystemExit("  refused: struct %s not found" % struct)
    return {f: int(o, 16) for o, f in re.findall(r"/\*0x([0-9A-Fa-f]+)\*/\s*[\w ]+?\s+\**(\w+)\s*(?:\[|;|:)", m.group(1))}


def flag_values(names, header="constants/flags.h"):
    """the numbers of constants, as the compiler sees them: the C preprocessor expands each through every header it
    leans on (SYS_FLAGS, TRAINER_FLAGS_END, MAX_TRAINERS_COUNT...), and the arithmetic left is evaluated here."""
    import subprocess, tempfile
    src = '#include "%s"\n' % header + "".join("@%d@ %s\n" % (i, n) for i, n in enumerate(names))
    with tempfile.NamedTemporaryFile("w", suffix=".c", delete=False) as f:
        f.write(src)
    out = subprocess.run(["arm-none-eabi-cpp", "-P", "-I", os.path.join(GBA, "include"), f.name],
                         capture_output=True, text=True)
    os.unlink(f.name)
    got = {names[int(i)]: v for i, v in re.findall(r"^@(\d+)@ (.+)$", out.stdout, re.M)}
    missing = [n for n in names if n not in got]
    if missing:
        raise SystemExit("  refused: the preprocessor did not resolve %s\n%s" % (missing, out.stderr[-800:]))
    return {n: eval(got[n], {"__builtins__": {}}) for n in names}


UNDERSTANDINGS = ["FLAG_UNDERSTANDING_FIRST", "FLAG_UNDERSTANDING_SCHOOL", "FLAG_UNDERSTANDING_READING",
                  "FLAG_UNDERSTANDING_NOTES", "FLAG_UNDERSTANDING_SCORN", "FLAG_UNDERSTANDING_RETURN",
                  "FLAG_UNDERSTANDING_GUIDE"]
INSIGHTS = ["FLAG_INSIGHT_" + v for v in ("DILIGENCE", "CHASTITY", "CHARITY", "KINDNESS", "TEMPERANCE", "PATIENCE",
                                           "HUMILITY")]


def notebook_table():
    """C-125: the NOTEBOOK, as src/notebook.c's own table holds it -- every page in its authored order, its section, the
    flag (and second flag) that files it, its one line from notebook_notes.h, and its words, from wherever the game keeps
    them: notebook.c, the placed documents (notebook_documents.h), the insights (wisdom.h) or a map's text.inc. The
    companion shows a page only once the save holds its flags. A page written from the save at the moment it is opened
    (the paper's record, WHAT YOU CHOSE) is listed with no words: the game writes it, and the phone says so."""
    nb, docs, wis = read("src/notebook.c"), read("src/data/notebook_documents.h"), read("src/data/wisdom.h")
    notes = read("src/data/notebook_notes.h")
    strings = {}
    for src in (nb, docs, wis):
        for name, body in re.findall(r"static const u8 (\w+)\[\]\s*=\s*_\((.*?)\);", src, re.S):
            strings[name] = gba_string(body)
    import glob
    labels = {}
    for f in glob.glob(os.path.join(GBA, "data/maps/*/text.inc")) + glob.glob(os.path.join(GBA, "data/text/*.inc")):
        for name, body in re.findall(r"^(\w+)::\s*\n((?:\s*\.string\s+\"(?:[^\"\\]|\\.)*\"\s*\n?)+)",
                                     open(f, encoding="utf-8").read(), re.M):
            labels[name] = gba_string(body).replace("\\l", "\n").replace("$", "")
    order = re.search(r"enum\s*\{\s*(NB_SCHOOL_NOTES.*?)NB_SECTION_COUNT", nb, re.S).group(1)
    sections = re.findall(r"(NB_\w+)", order)
    names = dict(re.findall(r"\[(NB_\w+)\]\s*=\s*(\w+)", nb))
    body = re.search(r"static const struct NotebookEntry sEntries\[\] =\s*\{(.*?)^\};", nb, re.M | re.S).group(1)
    macros = dict(re.findall(r"#define (NB_DOC_\w+) (\{.*?\}),", docs))
    body = re.sub(r"\bNB_DOC_\w+\b", lambda m: macros.get(m.group(0), "") + ",", body)
    insight = re.search(r"#define NB_INSIGHT_ENTRIES \\\n(.*?)(?:\n\n|\Z)", wis, re.S).group(1)
    body = body.replace("NB_INSIGHT_ENTRIES", insight.replace("\\", ""))
    body = re.sub(r"//[^\n]*", "", body)
    rows = re.findall(r"\{\s*(NB_\w+),\s*(NB_KIND_\w+),\s*(\d+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\s*\}", body)
    flagnames = sorted({r[3] for r in rows} | {r[4] for r in rows if r[4] != "0"})
    fv = flag_values(flagnames)
    abouts = {n: gba_string(b) for n, b in re.findall(r"static const u8 sNoteAbout_(\w+)\[\]\s*=\s*_\((.*?)\);", notes, re.S)}
    # T-403: each page's SEEN number (unread until FLAG_NOTEBOOK_SEEN_0 + seen is set) and the map it was found on
    seen0 = flag_values(["FLAG_NOTEBOOK_SEEN_0"])["FLAG_NOTEBOOK_SEEN_0"]
    groups = {m: (int(n), int(g)) for m, n, g in
              re.findall(r"#define (MAP_\w+)\s+\((\d+) \| \((\d+) << 8\)\)", read("include/constants/map_groups.h"))}
    places = json.load(open(os.path.join(OUT, "maps.json"), encoding="utf-8")) if os.path.exists(os.path.join(OUT, "maps.json")) else {}
    places = places or maps_table()
    found = {}
    for flag, seen, mp in re.findall(r"\{\s*(FLAG_\w+),\s*(\d+),\s*(MAP_\w+),", notes):
        g = groups.get(mp)
        found[flag] = (seen0 + int(seen), places.get("%d.%d" % (g[1], g[0]), {}).get("place") if g else None)
    # T-402: the song or post a page ends on, as its QR code says (sPageQr -> sQrCodes -> the URL above each code)
    qrc = read("src/data/qr_codes.h")
    urls = dict((n, u) for u, n in re.findall(r"//\s*(https?://\S+)\s*\nstatic const u8 (sQr_\w+)\[\]", qrc))
    table = re.search(r"sQrCodes\[\]\s*=\s*\{(.*?)\}", qrc, re.S).group(1).replace(" ", "").split(",")
    consts = {n: int(v) for n, v in re.findall(r"#define (BOOK_QR_\w+)\s+(\d+)", read("include/constants/book_qr.h"))}
    pageqr = re.search(r"sPageQr\[\]\s*=\s*\{(.*?)^\};", nb, re.S | re.M).group(1)
    links = {}
    for flag, qr in re.findall(r"\{\s*(FLAG_\w+),\s*(BOOK_QR_\w+)\s*\}", pageqr):
        i = consts.get(qr)
        if i is not None and i < len(table) and table[i] in urls:
            links[flag] = urls[table[i]]
    pages = []
    for sec, kind, arg, flag, flag2, title, text in rows:
        words = None
        if kind == "NB_KIND_TEXT":
            words = strings.get(text) if text in strings else labels.get(text)
            if words is None:
                raise SystemExit("  refused: the NOTEBOOK's %s has no words the export can find (%s)" % (title, text))
            if arg == "1":
                words = words.split("\n\n", 1)[-1]           # the heading the title already carries
            words = re.sub(r"\{(?!RIVAL\}|PLAYER\})[^}]*\}", "", words).strip()
        pages.append({"section": sections.index(sec), "title": strings[title], "kind": kind[8:].lower(),
                      "flag": fv[flag], "flag2": fv[flag2] if flag2 != "0" else 0,
                      "about": abouts.get(flag[5:]), "text": words,
                      "seen": found.get(flag, (None, None))[0], "place": found.get(flag, (None, None))[1],
                      "link": links.get(flag)})
    return {"_about": "C-125: the NOTEBOOK's pages in the game's own order, read from src/notebook.c and the headers it "
                      "includes. A page is held when the save has flag and (if not 0) flag2 -- notebook.c's own rule. "
                      "{RIVAL} and {PLAYER} are the names from the save. kind exam/choices: written by the game from "
                      "the save when opened; no words here. seen: the flag set once the page is opened in the game (unread until "
                      "then, T-403); place: where it was found; link: the song or post its QR code opens (T-402).",
            "sections": [strings[names[s]] for s in sections], "pages": pages}


def player_art():
    """C-125: the player as the game draws them -- REASON (red) and INSTINCT (leaf): the trainer card's front picture in
    its own palette, and the first walking frame (facing you) in the player's overworld palette. Ours, the monkey."""
    from PIL import Image
    def jasc(rel):
        lines = read(rel).split()
        return [int(v) for v in lines[3:3 + 48]]
    out = {}
    for who, pic, walk in (("reason", "red", "red_normal"), ("instinct", "leaf", "green_normal")):
        im = Image.open(os.path.join(GBA, "graphics/trainers/front_pics/%s_front_pic.png" % pic)).convert("P")
        im.putpalette(jasc("graphics/trainers/palettes/%s.pal" % pic) + [0] * 720)
        out["player_%s.png" % who] = im
        sheet = Image.open(os.path.join(GBA, "graphics/object_events/pics/people/%s.png" % walk)).convert("P")
        frame = sheet.crop((0, 0, 16, 32))
        frame.putpalette(jasc("graphics/object_events/palettes/player.pal") + [0] * 720)
        out["player_%s_walk.png" % who] = frame
    return out


def profile_layout():
    """C-23: where the PROFILE's facts live in a save -- the trainer, the play time, the INDEX's seen and bound, the
    MARKS, how far the game has gone and where it was saved -- every offset from the built game's own headers."""
    g = read("include/global.h")
    sb2, sb1, dex = struct_offsets(g, "SaveBlock2"), struct_offsets(g, "SaveBlock1"), struct_offsets(g, "Pokedex")
    flags = flag_values(["FLAG_BADGE01_GET", "FLAG_BADGE08_GET", "FLAG_SYS_POKEDEX_GET", "FLAG_SYS_GAME_CLEAR",
                         "FLAG_GOT_DIPLOMA", "DAEMONS_FLAGS_START", "FLAG_COMPANION_LINKED", "FLAG_COMPANION_RECALLED",
                         "FLAG_SYS_B_DASH", "FLAG_SHOES_FROM_DAD", "FLAG_GOT_NOTEBOOK"] + UNDERSTANDINGS + INSIGHTS)
    items = dict(re.findall(r"^#define\s+(ITEM_OPUS)\s+(\d+)", read("include/constants/items.h"), re.M))
    kcount = re.search(r"#define\s+BAG_KEYITEMS_COUNT\s+(\d+)", read("include/constants/global.h")).group(1)
    return {"_about": "C-23: offsets into SaveBlock2 (section 0) and SaveBlock1 (sections 1-4, end to end), read from "
                      "global.h's own struct comments; flag numbers resolved from flags.h. A flag below "
                      "daemons_flags_start is a bit in SaveBlock1's flags, one at or above it a bit in SaveBlock2's "
                      "daemonsFlags. INDEX flags are by national number minus one. Money is stored XOR the "
                      "encryption key. A daemon is SEEN only when sb2 index_seen and sb1 seen1 and seen2 all have its bit "
                      "(pokedex_screen.c's anticheat), so a writer sets all three.",
            "sb2": {"player_name": sb2["playerName"], "player_gender": sb2["playerGender"],
                    "trainer_id": sb2["playerTrainerId"], "play_time_hours": sb2["playTimeHours"],
                    "play_time_minutes": sb2["playTimeMinutes"], "play_time_seconds": sb2["playTimeSeconds"],
                    "index_bound": sb2["pokedex"] + dex["owned"], "index_seen": sb2["pokedex"] + dex["seen"],
                    "index_bytes": dex["seen"] - dex["owned"],
                    "daemons_flags": sb2["daemonsFlags"], "encryption_key": sb2["encryptionKey"]},
            "sb1": {"location": sb1["location"], "flags": sb1["flags"], "money": sb1["money"],
                    "rival_name": sb1["rivalName"],                                    # C-125: the name the player gave
                    "key_items": sb1["bagPocket_KeyItems"], "key_items_count": int(kcount),
                    #  C-128: the PLUGIN pocket holds the eight DRIVERS (and every PLUGIN), the items pocket TEA
                    "tmhm": sb1["bagPocket_TMHM"], "tmhm_count": int(re.search(r"#define\s+BAG_TMHM_COUNT\s+(\d+)", read("include/constants/global.h")).group(1)),
                    "items_pocket": sb1["bagPocket_Items"], "items_count": int(re.search(r"#define\s+BAG_ITEMS_COUNT\s+(\d+)", read("include/constants/global.h")).group(1)),
                    # C-15: the INDEX's seen flags are kept three times; the game believes them only when all agree
                    "seen1": sb1["seen1"], "seen2": sb1["seen2"]},
            "flags": {"marks_first": flags["FLAG_BADGE01_GET"], "marks_last": flags["FLAG_BADGE08_GET"],
                      "index": flags["FLAG_SYS_POKEDEX_GET"], "game_clear": flags["FLAG_SYS_GAME_CLEAR"],
                      "diploma": flags["FLAG_GOT_DIPLOMA"], "daemons_flags_start": flags["DAEMONS_FLAGS_START"],
                      "companion_linked": flags["FLAG_COMPANION_LINKED"],
                      "companion_recalled": flags["FLAG_COMPANION_RECALLED"],
                      # C-125: the PROFILE's more -- whose shoes, the understandings and insights held, the NOTEBOOK
                      "shoes": flags["FLAG_SYS_B_DASH"], "shoes_from_dad": flags["FLAG_SHOES_FROM_DAD"],
                      "notebook": flags["FLAG_GOT_NOTEBOOK"],
                      "understandings": [flags[f] for f in UNDERSTANDINGS],
                      "insights": [flags[f] for f in INSIGHTS]},
            "items": {"opus": int(items["ITEM_OPUS"])}}


def maps_table():
    """C-23: every map by the numbers a save stores (group, number), with its place's name as the game shows it."""
    groups = json.loads(read("data/maps/map_groups.json"))
    names = {}
    for sec in json.loads(read("src/data/region_map/region_map_sections.json"))["map_sections"]:
        if sec.get("name"):
            names[sec["id"]] = sec["name"]
    out = {"_about": "C-23: map group.number -> the map and its place's name (region_map_sections.json, our names)."}
    for g, group in enumerate(groups["group_order"]):
        for n, m in enumerate(groups[group]):
            sec = json.loads(read("data/maps/%s/map.json" % m)).get("region_map_section", "")
            out["%d.%d" % (g, n)] = {"map": m, "place": names.get(sec, "")}
    return out


def margins_table():
    """C-24 / T-373: OPUS's margins as the game holds them (src/data/opus_margins.h, written by genmargins.py), keyed by
    the internal species id a save stores -- with the game's own rule for which line shows, so the app reads exactly
    what the INDEX would: none without OPUS in the bag; CARRIED once any daemon of the species, in the party or a box,
    has gained levels_carried levels since it was met; NEGLECTED if it is only boxed without; and INSTINCT's voice
    (where it has lines) for a player who chose INSTINCT, which the save keeps as playerGender 1."""
    src = read("src/data/opus_margins.h")
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define SPECIES_(\w+)\s+(\d+)\b", read("include/constants/species.h"))}
    text = {name: gba_string(body) for name, body in re.findall(r"static const u8 (sOpusMargin_\w+)\[\]\s*=\s*_\((.*?)\);", src, re.S)}
    levels = int(re.search(r"#define\s+OPUS_LEVELS_CARRIED\s+(\d+)", read("src/pokedex_screen.c")).group(1))
    out = {"_about": margins_table.__doc__.split("\n")[0].strip() + " Rule: see tools/companion_export.py margins_table.",
           "levels_carried": levels, "instinct_gender": 1, "margins": {}}
    for sp, *lines in re.findall(r"\{\s*SPECIES_(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\s*\}", src):
        get = lambda n: None if n == "NULL" else text[n]
        out["margins"][str(ids[sp])] = {"carried": get(lines[0]), "neglected": get(lines[1]),
                                        "instinctCarried": get(lines[2]), "instinctNeglected": get(lines[3])}
    return out


def items_table():
    """C-31: every item by the id a save stores, with our name and description (src/data/items.json, which the game's
    items.h is generated from) -- so the app and the device name what an AWAY daemon is holding as the game does."""
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define (ITEM_\w+)\s+(\d+)\b", read("include/constants/items.h"))}
    out = {"_about": "C-31: item id -> our name and description, from src/data/items.json."}
    for it in json.loads(read("src/data/items.json"))["items"]:
        if it.get("itemId") in ids and ids[it["itemId"]]:
            out[str(ids[it["itemId"]])] = {"name": it.get("english", ""),
                                           "description": it.get("description_english", "").replace("\\n", " ")}
    return out


def seasons_table():
    """C-14: the seasons from tools/seasons.py, the one definition the game's T-359 will share."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import seasons
    return {"_about": "vision 9.21: CONTENT keeps the northern year, CONTEXT the southern. A season begins on its date "
                      "and runs to the day before the next; the southern year is the northern one two seasons on. "
                      "Defined once in DAEMONS tools/seasons.py.",
            "order": list(seasons.SEASONS),
            "north_starts": {k: {"month": m, "day": d} for k, (m, d) in seasons.NORTH_STARTS.items()},
            "edition_hemisphere": seasons.EDITION_HEMISPHERE,
            "play_hours_per_season": seasons.PLAY_HOURS_PER_SEASON}



#  C-126/C-127 (the companion session, for the user's PROFILE, 2026-10-16): the MARKS as the trainer card draws them
#  and with their STREAM lessons; the UNDERSTANDINGS' colours and lobes; the two regions as the region map lays them out.
MARK_TOWNS = ["MAPSEC_PEWTER_CITY", "MAPSEC_CERULEAN_CITY", "MAPSEC_VERMILION_CITY", "MAPSEC_CELADON_CITY",
              "MAPSEC_FUCHSIA_CITY", "MAPSEC_SAFFRON_CITY", "MAPSEC_CINNABAR_ISLAND", "MAPSEC_VIRIDIAN_CITY"]


def _section_names():
    return {sec["id"]: sec.get("name", "") for sec in json.loads(read("src/data/region_map/region_map_sections.json"))["map_sections"]}


def marks_table():
    """C-126: each MARK -- its flag, its STREAM lesson (title and both scripts, teachy_tv.h), and the town whose
    BENCHMARK gives it; its badge is art/mark_N.png. And each UNDERSTANDING -- its flag, its lobe and colour on the
    USER card's brain (trainer_card.c's sBrainLobes, T-331), where it is arrived at, and its name. The understandings
    have only WORKING names (the debug menu's) until the user names them (T-252); their lessons are T-405."""
    tv = read("src/data/text/teachy_tv.h")
    def text(sym):
        m = re.search(r"const u8 %s\[\] = _\(\s*(.*?)\);" % sym, tv, re.S)
        #  the game's scroll break (\\l) is a line break on a phone, and the terminating $ is not a word
        return gba_string(m.group(1)).replace("\\l", "\n").rstrip("$") if m else ""
    names = _section_names()
    flags = flag_values(["FLAG_BADGE0%d_GET" % i for i in range(1, 9)] + UNDERSTANDINGS)
    marks = []
    for i in range(1, 9):
        marks.append({"n": i, "flag": flags["FLAG_BADGE0%d_GET" % i], "art": "mark_%d.png" % i,
                      "title": text("gTeachyTvString_Mark%d" % i),
                      "lesson": [t for t in (text("gTeachyTvText_Mark%dScript1" % i), text("gTeachyTvText_Mark%dScript2" % i)) if t],
                      "found": names.get(MARK_TOWNS[i - 1], "")})
    #  T-389/T-390's words (docs/wisdom.json, DRAFT): the leader after the win without the paired understanding and with
    #  it, the union PLUGIN handed over and what it does, and the insight that arrives when both are held. The eighth
    #  MARK has no pair. T-410's balance paragraphs will join these as "balance".
    wis = json.load(open(os.path.join(ROOT, "docs", "wisdom.json"), encoding="utf-8"))
    wf = flag_values([f for pr in wis["pairs"] for f in (pr["root"], pr["given"], pr["insight_flag"])])
    for pr in wis["pairs"]:
        n = int(pr["badge"][-6:-4])
        marks[n - 1]["wisdom"] = {"leader": pr["leader"], "virtue": pr["virtue"], "root_flag_name": pr["root"],
                                  "without": pr["without"], "with": pr["with"], "explain": pr["explain"],
                                  "union_plugin": pr["plugin_name"], "union_routine": pr["routine"],
                                  "given_flag_name": pr["given"], "insight": pr["insight"],
                                  "insight_flag_name": pr["insight_flag"],
                                  #  numbers, as the save reader works from them (the companion session, 2026-10-16)
                                  "root_flag": wf[pr["root"]], "given_flag": wf[pr["given"]],
                                  "insight_flag": wf[pr["insight_flag"]]}
    tc = read("src/trainer_card.c")
    lobes = re.findall(r"\{ (FLAG_UNDERSTANDING_\w+),\s*\w+,\s*RGB\((\d+), (\d+), (\d+)\)\s*\},\s*//\s*(\w+)\s+(\w+)", tc)
    debug = read("src/daemons_debug_events.c")
    working = re.findall(r"sName_Root(\d)\[\] = _\(\"([^\"]*)\"\)", debug)
    working = {int(n): t for n, t in working}
    found = ["TANOBY CHAMBERS, its last inscription", "CALLOW SCHOOL: the TEXTBOOK and the DIPLOMA",
             "BRAZEN's READING ROOM, with REVEAL", "QUICKSILVER's notes: the run logs and THE FILE",
             "SCORN beaten, the eighth MARK", "TY met, and CRYSTAL found", "THE GUIDE, read to its end"]
    unders = []
    for k, (flag, r, g, b, lobe, ty) in enumerate(lobes):
        unders.append({"n": k + 1, "flag": flags[flag], "flag_name": flag, "lobe": lobe, "type": ty,
                       "rgb": rgb8(int(r), int(g), int(b)), "name": working.get(k + 1, ""), "name_is_working": True,
                       "found": found[k], "lesson": None})
    return {"_about": "C-126: the MARKS (badge art, STREAM lesson, town) and the UNDERSTANDINGS (brain lobe, colour, "
                      "where arrived at). Understanding names are working names until the user names them (T-252); "
                      "their lessons are null until T-405. Order matches profile_layout's flags.understandings.",
            "marks": marks, "understandings": unders}


def regions_table():
    """C-127: GAMUT and THE MARGINS as the region map lays them out -- each map grid's cells as map sections (22 x 15,
    the map layer of region_map_layout_*.h), and for every section its name and the flag the game sets when it is
    first visited (FLAG_WORLD_MAP_*, which the game keeps for towns and a few places only -- a route has none). THE
    MARGINS' name is hidden until game_clear (the REVIEW BOARD beaten, profile_layout's flags.game_clear)."""
    names = _section_names()
    fl = read("include/constants/flags.h")
    visited = {}
    world = re.findall(r"#define (FLAG_WORLD_MAP_(\w+))\s", fl)
    want = flag_values([f for f, _ in world])
    for f, suffix in world:
        mapname = None
        for d in os.listdir(os.path.join(GBA, "data/maps")):
            mj = os.path.join(GBA, "data/maps", d, "map.json")
            if os.path.exists(mj):
                m = json.load(open(mj))
                if m.get("id") == "MAP_" + suffix:
                    mapname = m.get("region_map_section"); break
        if mapname:
            visited.setdefault(mapname, want[f])
    def grid(fname):
        body = read("src/data/region_map/%s" % fname)
        layer = body.split("[LAYER_MAP] =")[1].split("[LAYER_DUNGEON]")[0]
        return [re.findall(r"MAPSEC_\w+", row) for row in re.findall(r"\{([^{}]*)\}", layer)]
    regions = []
    for key, title, files in (("mainland", "gText_Kanto", ["region_map_layout_kanto.h"]),
                              ("islands", "gText_SeviiIslands", ["region_map_layout_sevii_123.h", "region_map_layout_sevii_45.h", "region_map_layout_sevii_67.h"])):
        name = gba_string(re.search(r"const u8 %s\[\] = _\((\".*?\")\);" % title, read("src/strings.c")).group(1))
        maps = [{"file": f, "grid": grid(f)} for f in files]
        secs = sorted({c for m in maps for row in m["grid"] for c in row} - {"MAPSEC_NONE"})
        regions.append({"key": key, "name": name, "hidden_until": "game_clear" if key == "islands" else None, "maps": maps,
                        "sections": {sc: {"name": names.get(sc, ""), "visited_flag": visited.get(sc)} for sc in secs}})
    return {"_about": "C-127: the two regions as the game's region map lays them out. A cell is a map section; a section "
                      "with a visited_flag lights when that flag is set (bits as profile_layout explains); one without "
                      "(routes, water) has no record in the save -- light it however the PROFILE likes, e.g. when a "
                      "neighbouring town is lit. MARGINS is three maps, as the game's own region map is.",
            "regions": regions}


def _grove_flag(g):
    return "FLAG_" + re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", g.replace("_Grove", "")).upper() + "_GROVE_FOUND"


def groves_table():
    """T-408: the fourteen groves as universes -- each one's name and the sign beside its door in THE NEXUS (both
    approved by the user, 2026-10-16), the map its door tree stands on, the flag set the first time it is arrived in,
    and the family that lives there (our names). Read from tools/gbanexusmap.py and tools/gbagrove.py as text."""
    nx = open(os.path.join(ROOT, "tools", "gbanexusmap.py"), encoding="utf-8").read()
    gv = open(os.path.join(ROOT, "tools", "gbagrove.py"), encoding="utf-8").read()
    uni = {g: (t, h.replace("\\n", "\n")) for g, t, h in re.findall(r'"(\w+_Grove)": \("([^"]+)", "([^"]+)"\)', nx)}
    rows = re.findall(r'dict\(name="(\w+_Grove)", parent="(\w+)".*?family="(\w+)"', gv, re.S)
    fam = dict(re.findall(r'"(\w+)":\s*\[(\(.*?\))\],', gv))
    byconst = {v["constant"]: v["name"] for v in species_table().values() if isinstance(v, dict) and v.get("constant")}
    flags = flag_values([_grove_flag(g) for g, _, _ in rows])
    out = []
    for g, parent, family in rows:
        t, h = uni.get(g, ("", ""))
        out.append({"grove": g, "universe": t, "sign": h, "door_map": parent, "found_flag": flags.get(_grove_flag(g)),
                    "found_flag_name": _grove_flag(g),
                    "family": [byconst.get(c, c) for c in re.findall(r"SPECIES_(\w+)", fam.get(family, ""))]})
    return {"_about": "T-408: the groves as universes, with THE NEXUS's signs; found_flag is set the first time the "
                      "grove is arrived in (bits as profile_layout explains). THE NEXUS itself is the PAINTEDVERSE.",
            "nexus": "THE PAINTEDVERSE", "groves": out}


def mark_art():
    """C-126: the eight MARK badges as the trainer card draws them -- badges.png (128x16, a 16x16 badge each) in the
    card's badge palette."""
    from PIL import Image
    sheet = Image.open(os.path.join(GBA, "graphics/trainer_card/badges.png"))
    pal = None
    gp = os.path.join(GBA, "graphics/trainer_card/badges.pal")
    if os.path.exists(gp):
        v = [int(x) for x in read("graphics/trainer_card/badges.pal").split()[3:3 + 48]]
        pal = v + [0] * 720
    out = {}
    for i in range(8):
        im = sheet.crop((i * 16, 0, i * 16 + 16, 16)).convert("P") if sheet.mode == "P" else sheet.crop((i * 16, 0, i * 16 + 16, 16))
        if pal and im.mode == "P":
            im.putpalette(pal)
        out["mark_%d.png" % (i + 1)] = im
    return out

def _c_strings(src):
    """{symbol: text} for every _("...") constant in a C file, the scroll break (\\l) a line break, no $"""
    return {s: gba_string(b).replace("\\l", "\n").rstrip("$")
            for s, b in re.findall(r"\b(\w+)\[\]\s*=\s*_\(\s*((?:\"(?:[^\"\\]|\\.)*\"\s*)+)\)", src)}


def _inc_text(rel, label):
    """one label's words from a map's text.inc: its .string lines up to the $, \\l and \\p as line breaks"""
    m = re.search(r"^%s::\s*\n((?:\s*\.string\s+\".*\"\s*\n?)+)" % re.escape(label), read(rel), re.M)
    return gba_string(m.group(1)).replace("\\l", "\n").rstrip("$") if m else None


#  C-128 (the companion session, for the PROFILE, 2026-10-16): the GAME EVENTS page's rows, less the debug's own kit.
EVENTS_LEFT_OUT = {"EV_EVERYTHING", "EV_ROSTER", "EV_EVERY_DAEMON", "EV_STOCK", "EV_NOTEBOOK_FULL", "EV_INSIGHTS_AGAIN",
                   "EV_MARKS_ALL", "EV_DRIVERS_ALL", "EV_ROOTS_ALL"}


def events_table():
    """C-128: the PROFILE's GAME EVENTS -- every row of the debug menu's GAME EVENTS page (src/daemons_debug_events.c) in
    story order, a sub-page's rows (MARKS, NOTEBOOK, DRIVERS, UNDERSTANDINGS) where its row stands, each with the test
    the page's IsHeld makes for its + or ·, as flags and a var. The debug's own kit (EVERYTHING, THE ROSTER, EVERY
    DAEMON, THE STOCK, EVERY PAGE), each sub-page's ALL and LET INSIGHTS ARRIVE AGAIN are left out. A row held by a
    bag item has held null and its items, since the bag is not a flag."""
    src = read("src/daemons_debug_events.c")
    strings = _c_strings(src)
    def rows(arr):
        body = re.search(r"%s\[\]\s*=\s*\{(.*?)\n\};" % arr, src, re.S).group(1)
        return [(n, k, ev, int(off or 0)) for n, k, ev, off in
                re.findall(r"\{\s*(sName_\w+),\s*(R_\w+),\s*(\w+)(?:\s*\+\s*(\d+))?\s*\}", body)]
    titles = {pg: re.split(r"[,:]", strings[t])[0] for pg, t in
              zip(["PG_EVENTS", "PG_MARKS", "PG_NOTEBOOK", "PG_DRIVERS", "PG_ROOTS"],
                  re.search(r"sTitles\[PG_COUNT\]\s*=\s*\{(.*?)\};", src, re.S).group(1).replace(",", " ").split())}
    pages = {"PG_MARKS": "sRows_Marks", "PG_NOTEBOOK": "sRows_Notebook", "PG_DRIVERS": "sRows_Drivers",
             "PG_ROOTS": "sRows_Roots"}
    held_src = re.search(r"static bool8 IsHeld\(u8 ev\)\s*\{(.*?)\n\}", src, re.S).group(1)
    by_flag = dict(re.findall(r"case (EV_\w+):\s*return FlagGet\((FLAG_\w+)\);", held_src))
    by_item = dict(re.findall(r"case (EV_\w+):\s*return CheckBagHasItem\((ITEM_\w+), 1\);", held_src))
    by_var = {e: (v, op, int(n, 0)) for e, v, op, n in
              re.findall(r"case (EV_\w+):\s*return VarGet\((VAR_\w+)\) (!=|==|>=) (\w+);", held_src)}
    groves = re.findall(r"FLAG_\w+", re.search(r"sGroveFound\[\]\s*=\s*\{(.*?)\};", src, re.S).group(1))
    roots = [r.split(",")[0].strip() for r in
             re.findall(r"\{\s*(FLAG_UNDERSTANDING_\w+[^}]*)\}", re.search(r"sRoots\[7\]\[3\]\s*=\s*\{(.*?)\n\};", src, re.S).group(1))]
    marks = ["FLAG_BADGE0%d_GET" % i for i in range(1, 9)]
    #  THE OPENING has no mark on the page (it only gives); held here is the last of what DaemonsDebug_FinishOpening
    #  sets -- the lab's scene once the starter, the rival, the parcel and the INDEX are all handed over
    opening = re.search(r"VarSet\((VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB), (\d+)\)", read("src/new_game.c"))
    plan = []                                   # (section, name, flags, var, items, note)
    for name, kind, ev, off in rows("sRows_Events"):
        if kind == "R_PAGE":
            for sname, skind, sev, soff in rows(pages[ev]):
                if sev in EVENTS_LEFT_OUT:
                    continue
                if sev == "EV_MARK1":
                    plan.append((titles[ev], sname, [marks[soff]], None, None, None))
                elif sev == "EV_ROOT1":
                    plan.append((titles[ev], sname, [roots[soff]], None, None, None))
                elif sev == "EV_DRIVER1":
                    plan.append((titles[ev], sname, None, None, [("ITEM_HM01", soff)], "held: the DRIVER in the bag"))
                elif sev in by_flag:
                    plan.append((titles[ev], sname, [by_flag[sev]], None, None, None))
                else:
                    raise SystemExit("  refused: no held test read for %s" % sev)
            continue
        if ev in EVENTS_LEFT_OUT:
            continue
        sec = titles["PG_EVENTS"]
        if ev in by_flag:
            plan.append((sec, name, [by_flag[ev]], None, None, None))
        elif ev in by_item:
            plan.append((sec, name, None, None, [(by_item[ev], 0)], "held: the item in the bag"))
        elif ev in by_var:
            plan.append((sec, name, [], by_var[ev], None, None))
        elif ev == "EV_GROVES":
            plan.append((sec, name, groves, None, None, None))
        elif ev == "EV_GLOBAL_INDEX":
            plan.append((sec, name, ["FLAG_SYS_NATIONAL_DEX"], ("VAR_NATIONAL_DEX", "==", 0x6258), None,
                         "IsNationalPokedexEnabled: also sb2 pokedex.nationalMagic == 0xB9 (sb2_byte)"))
        elif ev == "EV_OPENING":
            plan.append((sec, name, [], (opening.group(1), ">=", int(opening.group(2))), None,
                         "the page only gives this row; held is the lab's scene DaemonsDebug_FinishOpening sets"))
        elif ev == "EV_STREAM":
            plan.append((sec, name, None, None, [("ITEM_TEACHY_TV", 0), ("ITEM_FAME_CHECKER", 0)],
                         "the page only gives this row (the STREAM and HEARSAY in the bag, every show told)"))
        else:
            raise SystemExit("  refused: no held test read for %s" % ev)
    fnames = sorted({f for p in plan for f in (p[2] or [])})
    vnames = sorted({p[3][0] for p in plan if p[3]})
    inames = sorted({i for p in plan for i, _ in (p[4] or [])})
    fl = flag_values(fnames)
    vr = flag_values(vnames, "constants/vars.h")
    it = flag_values(inames, "constants/items.h")
    g = read("include/global.h")
    sb1, sb2, dex = struct_offsets(g, "SaveBlock1"), struct_offsets(g, "SaveBlock2"), struct_offsets(g, "Pokedex")
    events = []
    for k, (sec, name, flags, var, items, note) in enumerate(plan):
        row = {"n": k + 1, "name": strings[name], "section": sec}
        if flags is None:
            row["held"] = None
            row["items"] = [{"name": i if not o else "%s + %d" % (i, o), "id": it[i] + o} for i, o in items]
        else:
            row["held"] = {"all_flags": [fl[f] for f in flags], "flag_names": flags}
            if var:
                row["held"]["var"] = {"name": var[0], "number": vr[var[0]], "op": var[1], "value": var[2]}
            if name == "sName_GlobalIndex":
                row["held"]["sb2_byte"] = {"field": "pokedex.nationalMagic", "offset": sb2["pokedex"] + dex["nationalMagic"],
                                           "value": 0xB9}
        if note:
            row["note"] = note
        events.append(row)
    return {"_about": "C-128: the GAME EVENTS page of the debug menu, in story order, its sub-pages' rows where each "
                      "stands (section is the page's heading). held: every flag in all_flags set (bits as "
                      "profile_layout explains) and, if given, var compared by op to value; a var is a u16 at "
                      "sb1_vars + 2 * (number - vars_start). held null means the page tests the bag: items lists the "
                      "item ids (key items, or a DRIVER in the TM case). The debug's own kit, each sub-page's ALL and "
                      "its LET INSIGHTS ARRIVE AGAIN are left out.",
            "sb1_vars": sb1["vars"], "vars_start": 0x4000, "events": events}


def school_table():
    """C-129: CALLOW SCHOOL, what is taught -- each floor's subject (the TEXTBOOK's chapter names, book_reader.c), its
    placard and syllabus, its board's five topics (the TEXTBOOK prints the board itself, sTopics, so the book and the
    building are one text), the flag that marks it stood on (the TEXTBOOK greys a chapter without it); the paper
    (school_exam.c: seven sections, each question's choices and its right answer, the pass mark, the grade letters);
    and the DIPLOMA, with the vars the mark is kept in."""
    br = read("src/book_reader.c")
    bs = _c_strings(br)
    chapters = re.findall(r"\bsChapter\d\b", re.search(r"sChapterNames\[[^]]*\]\s*=\s*\{(.*?)\};", br, re.S).group(1))
    vflags = re.findall(r"FLAG_\w+", re.search(r"sChapterFlags\[[^]]*\]\s*=\s*\{(.*?)\};", br, re.S).group(1))
    topics = {int(n): re.findall(r"\w+", t) for n, t in
              re.findall(r"\[(\d)\]\s*=\s*\{([^}]*)\}", re.search(r"sTopics\[[^]]*\]\[[^]]*\]\s*=\s*\{(.*?)\n\};", br, re.S).group(1))}
    ex = read("src/school_exam.c")
    es = _c_strings(ex)
    sections = re.findall(r"\{\s*(sSection_\w+),\s*(sQuestions_\w+),", re.search(r"sSections\[\]\s*=\s*\{(.*?)\};", ex, re.S).group(1))
    pass_mark = int(re.search(r"#define EXAM_PASS_MARK\s+(\d+)", ex).group(1))
    per_var = int(re.search(r"#define QS_PER_VAR\s+(\d+)", ex).group(1))
    grades = [{"from": int(n), "letter": es[s]} for n, s in
              re.findall(r"if \(percent >= (\d+)\) return (\w+);", re.search(r"GradeLetter\(u16 percent\)(.*?)\n\}", ex, re.S).group(1))]
    grades.append({"from": 0, "letter": es["sF"]})
    fl = flag_values(vflags + ["FLAG_GOT_DIPLOMA", "FLAG_SCHOOL_GOT_TEXTBOOK", "FLAG_SCHOOL_PAPER_MARKED"])
    vnames = ["VAR_SCHOOL_EXAM_BEST", "VAR_SCHOOL_EXAM_LAST", "VAR_SCHOOL_EXAM_ATTEMPTS", "VAR_SCHOOL_EXAM_ANSWERS"]
    vr = flag_values(vnames, "constants/vars.h")
    sb1 = struct_offsets(read("include/global.h"), "SaveBlock1")
    floors = []
    for k, ch in enumerate(chapters):
        f = k + 1
        mapdir = "data/maps/ViridianCity_School" + ("" if f == 1 else "_%dF" % f)
        prefix = "ViridianCity_School" + ("" if f == 1 else "_%dF" % f)
        board = []
        for sym in topics[f]:
            words = _inc_text(mapdir + "/text.inc", sym)
            name, _, rest = words.partition("\n\n")
            board.append({"topic": name, "text": rest})
        floors.append({"floor": "%dF" % f, "subject": bs[ch], "visited_flag": fl[vflags[k]], "visited_flag_name": vflags[k],
                       "placard": _inc_text(mapdir + "/text.inc", prefix + "_Text_Placard"),
                       "syllabus": _inc_text(mapdir + "/text.inc", prefix + "_Text_Syllabus"),
                       "board_intro": _inc_text(mapdir + "/text.inc", prefix + "_Text_BoardIntro"),
                       "board": board})
    paper, q = [], 0
    for sec, qs in sections:
        body = re.search(r"%s\[\]\s*=\s*\{(.*?)\n\};" % qs, ex, re.S).group(1)
        questions = []
        for t, txt, opts, ans in re.findall(r"\{\s*(\w+),\s*(\w+),\s*\{([^}]*)\},\s*(\d)\s*\}", body):
            questions.append({"q": q, "title": es[t], "text": es[txt],
                              "choices": [es[o.strip()] for o in opts.split(",")], "answer": int(ans) - 1})
            q += 1
        paper.append({"section": es[sec], "questions": questions})
    return {"_about": "C-129: CALLOW SCHOOL. floors: 1F-7F, each a TEXTBOOK chapter (subject) whose five topics are "
                      "the floor's board, word for word; a chapter is greyed until its visited_flag is set. paper: "
                      "the exam's seven sections in order; answer is an index into choices (the save stores 1-4 for "
                      "A-D, 0 unanswered). The mark is round(correct * 100 / total); pass_mark or better passes, and "
                      "passing gives the DIPLOMA (flags.diploma). The save keeps no letter: grades turns a mark into "
                      "it (GradeLetter). vars: u16s at sb1_vars + 2 * (number - vars_start); answers is the first of "
                      "the vars holding each question's answer, per_var to a var, three bits each, question q in var "
                      "answers + q // per_var at bit 3 * (q % per_var).",
            "floors": floors, "paper": paper, "pass_mark": pass_mark, "grades": grades,
            "flags": {"diploma": fl["FLAG_GOT_DIPLOMA"], "textbook": fl["FLAG_SCHOOL_GOT_TEXTBOOK"],
                      "paper_marked": fl["FLAG_SCHOOL_PAPER_MARKED"]},
            "vars": {"best": vr["VAR_SCHOOL_EXAM_BEST"], "last": vr["VAR_SCHOOL_EXAM_LAST"],
                     "attempts": vr["VAR_SCHOOL_EXAM_ATTEMPTS"], "answers": vr["VAR_SCHOOL_EXAM_ANSWERS"],
                     "per_var": per_var},
            "sb1_vars": sb1["vars"], "vars_start": 0x4000}


def main():
    files = {"species.json": species_table(), "charmap.json": charmap_table(), "week.json": week_table(),
             "seasons.json": seasons_table(), "streaks.json": streaks_table(), "moves.json": moves_table(),
             "profile_layout.json": profile_layout(), "maps.json": maps_table(), "margins.json": margins_table(),
             "items.json": items_table(), "routines.json": routines_table(), "notebook.json": notebook_table(),
             "marks.json": marks_table(), "regions.json": regions_table(),     # C-126, C-127
             "events.json": events_table(), "school.json": school_table(),
             "groves.json": groves_table()}                                     # T-408       # C-128, C-129
    layout = save_layout()
    if layout:
        files["save_layout.json"] = layout
    else:
        print("  no build to read the save layout from (make firered leafgreen first); save_layout.json left as it is")
    changed = []
    for name, data in files.items():
        text = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
        path = os.path.join(OUT, name)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old != text:
            changed.append(name)
            if WRITE:
                os.makedirs(OUT, exist_ok=True)
                open(path, "w", encoding="utf-8").write(text)
    import io
    art = party_art(files["species.json"])
    art.update(player_art())                                           # C-125
    art.update(mark_art())                                             # C-126
    art_dir = os.path.join(OUT, "art")
    art_changed = 0
    for name, im in art.items():
        buf = io.BytesIO()
        im.save(buf, "PNG", transparency=0, optimize=True)
        path = os.path.join(art_dir, name)
        if not os.path.exists(path) or open(path, "rb").read() != buf.getvalue():
            art_changed += 1
            if WRITE:
                os.makedirs(art_dir, exist_ok=True)
                open(path, "wb").write(buf.getvalue())
    if art_changed:
        changed.append("art/ (%d of %d)" % (art_changed, len(art)))
    sp = files["species.json"]
    with_art = sum(1 for r in sp.values() if r["art"]["front"])
    with_entry = sum(1 for r in sp.values() if r["entry"]["CONTENT"] and r["entry"]["CONTEXT"])
    print("  %d species (%d with both editions' entries, %d with art), %d characters, %d days, 4 seasons"
          % (len(sp), with_entry, with_art, len(files["charmap.json"]["bytes"]), len(files["week.json"]["days"])))
    if not changed:
        print("  companion/server/data/ agrees")
    elif WRITE:
        print("  written: " + ", ".join(changed))
    else:
        print("  would change: " + ", ".join(changed) + " (report only; pass --write)")
    #  T-373: --check is the push routine's: the companion must hold the words the game is built from -- the INDEX
    #  entries, OPUS's margins, the save's layout -- or a release ships words the companion does not have.
    if "--check" in sys.argv and changed and not WRITE:
        print("  !! the companion's data is stale: python3 tools/companion_export.py --write, then commit it in companion/")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
  index_cards.json  the INDEX card whole, per species: number, name, types and their colours, category, HT and WT,
                both entries, NATIVE, the workings, OPUS's margins; the seven understandings (flag, colour, the GUIDE
                margin each writes in); and the rules a save decides (T-453, C-186)
  patches.json  every published release from v11.309.1: its four BPS patches described (source ROM and its
                SHA-1/CRC32/MD5, target SHA-1, the patch's size and hashes, its GitHub URL) -- never a patch (T-453)
  planner_story.json, planner_maps.json, planner_wild.json, planner_trainers.json, planner_curve.json
                the PLANNER (T-453): the story's steps and where each happens, how the maps join, what is wild and
                who fights on each, and the level curve -- every record with the step it is reachable after

(and marks, regions, groves, guide, subtle, holidays, play, notebook, routines, streaks, moves, art/ -- see main())

Everything is read from the engine's sources and the art folder; nothing of Nintendo's is copied -- our names, our
entries and our art only.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.environ.get("COMPANION_DATA") or os.path.join(ROOT, "companion", "server", "data")   # C-203: a worktree's data/ instead
WRITE = "--write" in sys.argv


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8").read()


def gba_string(body):
    """the text of a _("...") or a run of "..." lines, with the line breaks as \\n"""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', body)
    return "".join(parts).replace("\\n", "\n").replace("\\p", "\n\n")


def native_values():
    """{SPECIES_X: the packed u32 tools/gbanative.py writes into the ROM} -- one source for the game and the companion."""
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
    g = v >> 12 & 15
    weathers = [x for i, x in enumerate(gbanative.SKIES[1:]) if v >> (16 + i) & 1]   # T-415 phase 2: "IN RAIN"
    grove = None if not g else "THE NEXUS" if g == gbanative.NEXUS else \
        gbanexusmap.UNIVERSES[gbagrove.GROVES[g - 1]["name"]][0]
    out = {"regions": [x for i, x in enumerate(("GAMUT", "THE MARGINS")) if v >> i & 1],
            "editions": editions if len(editions) < 2 else None,
            "seasons": seasons if len(seasons) < 4 else None,
            "hours": hours if len(hours) < 4 else None,
            "grove": grove}
    if weathers:   # only the few met only in weather carry it, so every other row stays as it was
        out["weathers"] = weathers
    return out


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

    # T-448 (C-184): how each species evolves, so a daemon carried on the companion can evolve there. The companion
    # judges only what it can see (level, friendship, the hour, and the personality split Wurmple's line uses); items,
    # trades, BEAUTY and SHEDINJA's empty-slot copy stay the game's, marked "judged": false
    judged = {"LEVEL", "FRIENDSHIP", "FRIENDSHIP_DAY", "FRIENDSHIP_NIGHT", "LEVEL_ATK_GT_DEF", "LEVEL_ATK_EQ_DEF",
              "LEVEL_ATK_LT_DEF", "LEVEL_SILCOON", "LEVEL_CASCOON", "LEVEL_NINJASK",
              "CARRIED"}   # T-450: the carried line grows only on the companion -- its param is the bond, not a level
    evos = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\}\}", read("src/data/pokemon/evolution.h"), re.S):
        for method, param, target in re.findall(r"\{\s*EVO_(\w+)\s*,\s*(\w+)\s*,\s*SPECIES_(\w+)\s*\}?", m.group(2) + "}"):
            if target in ids:
                evo = {"method": method, "param": int(param) if param.isdigit() else param,
                       "target": ids[target], "judged": method in judged}
                if method == "TRADE_PARTNER":   # T-474: param is the species it must be traded FOR, as its id
                    evo["param"] = evo["partner"] = ids[param[len("SPECIES_"):]]
                evos.setdefault(m.group(1), []).append(evo)
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
            "art": {view: ("gfx/daemons/%s_%s.png" % (stem, view)) if ("%s_%s.png" % (stem, view)) in art
                    #  SYMBOL's 28 forms live in gfx/daemons/symbol/<form>_*.png (T-452); its A form stands for it
                    else ("gfx/daemons/symbol/a_%s.png" % view) if stem == "symbol" and
                    os.path.exists(os.path.join(ROOT, "gfx/daemons/symbol/a_%s.png" % view)) else None
                    for view in ("front", "back")},
            "bodyType": body.get(sp),                  # C-18: the type its palette ramp was built from
            "streaks": sp in streaky,                  # C-18: palette 11..14 carry its four routines' streaks
            "growth": growth.get(sp, 0),               # C-24: GROWTH_*, MEDIUM_FAST where a macro hides it
            "base": base.get(sp),                      # C-45: HP, Attack, Defense, Speed, Sp.Atk, Sp.Def
            "native": native_of(native.get("SPECIES_" + sp, 0)),   # T-407: the INDEX's NATIVE box, as data
            "evolutions": evos.get(sp, []),            # T-448: method, param, target species id, judged by the companion?
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
        if not os.path.exists(tiles) and os.path.exists(os.path.join(d, "a", "front.4bpp")):
            tiles = os.path.join(d, "a", "front.4bpp")      # SYMBOL (UNOWN): its A form, one palette for all 28
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
        if "/symbol/" in row["art"]["front"]:
            name = "symbol.png"
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
#  centre, its virtue and the shadow it is said over (T-418: OVER, never CURES), and the theme word. The colour and the note are the game's own week
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
                     "virtue": virtue, "shadow": shadow, "cue": "%s over %s" % (virtue, shadow), "theme": theme})
    return {"_about": "Sunday first; each day's colour is the CHECKPOINT's trim (day_trims.h) and its note C to B "
                      "(vision 9.21); its hue, chakra, the virtue and the shadow it is over, and the theme are the "
                      "user's Xenith week (companion C-73).",
            "days": days}


#  C-02 / T-358: the two bits of a daemon's flags byte (struct BoxPokemon, byte 19: isBadEgg, hasSpecies, isEgg,
#  blockBoxRS, then unused:4) that carry the companion's link. T-358 defines them in the engine; until then they are
#  named here, and both must agree.
AWAY_BIT, ASKED_BIT = 4, 5
#  C-195 / T-458 (SOUNDINGS): bits 6-7 of the same byte, `signal:2` in include/pokemon.h -- 0 no signal yet, 1 quiet,
#  2 fine, 3 well. The companion writes it at each SYNC; the game only reads it.
SOUNDING_SHIFT = 6


#  T-473 (C-219): a trade's bits, read from struct BoxPokemon in include/pokemon.h, never typed -- each field's bit
#  offset counted from the top (the arrays by their length constants, the bitfields in order): TRADING in the flags
#  byte beside AWAY, LOAN and TRADED_IN in the u16 at 0x1E. T-474: bits 2-10 of that u16 are the species it was traded
#  FOR (the companion writes it with TRADED_IN; the game judges EVO_TRADE_PARTNER by it); bits 11-15 reserved.
def trade_bits():
    h = read("include/pokemon.h")
    body = re.search(r"struct BoxPokemon\s*\{(.*?)\n\s*union", h, re.S).group(1)
    lengths = {"POKEMON_NAME_LENGTH": 10, "PLAYER_NAME_LENGTH": 7}
    size = {"u8": 8, "u16": 16, "u32": 32}
    bit, at = 0, {}
    for m in re.finditer(r"^\s*(u8|u16|u32)\s+(\w+)(?:\[(\w+)\])?(?::(\d+))?;", body, re.M):
        kind, name, length, width = m.groups()
        unit = size[kind]
        if width:                                   # a bitfield: packed into its unit, a new unit when it will not fit
            if bit % unit + int(width) > unit:
                bit += unit - bit % unit
            at[name] = (bit // unit * (unit // 8), bit % unit, int(width), unit)
            bit += int(width)
        else:
            bit += -bit % unit
            at[name] = (bit // 8, 0, unit, unit)
            bit += unit * ((lengths[length] if length in lengths else int(length)) if length else 1)
    trading, loan, traded_in = at["trading"], at["daemonsLoan"], at["daemonsTradedIn"]
    partner = at["daemonsTradePartner"]                                                     # T-474
    if trading[0] != 19 or at["away"][:2] != (19, AWAY_BIT) or not loan[0] == traded_in[0] == partner[0]:
        raise SystemExit("  refused: struct BoxPokemon's trade bits are not where the companion reads them")
    return {"trading_bit": trading[1], "trade_flags_offset": loan[0],
            "loan_mask": 1 << loan[1], "traded_in_mask": 1 << traded_in[1],
            "trade_partner_shift": partner[1], "trade_partner_mask": ((1 << partner[2]) - 1) << partner[1]}


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
            "sounding_shift": SOUNDING_SHIFT,   # two bits, values 0-3 (T-458)
            **trade_bits(),                     # T-473: TRADING beside AWAY; LOAN and TRADED_IN at 0x1E; T-474 the partner
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
    import genplaynotes
    nb, docs, wis = read("src/notebook.c"), read("src/data/notebook_documents.h"), read("src/data/wisdom.h")
    dreams = read("src/data/dream_log.h")                                                   # T-412: the DREAM LOG
    hers = read("src/data/attendant_dreams.h")                                              # T-412: HER DREAMS
    its = read("src/data/its_dreams.h")                                                     # T-462: ITS DREAMS
    hol, holl = read("src/data/daemons_holidays.h"), read("src/data/holiday_lines.h")    # T-416: THE YEAR
    notes = read("src/data/notebook_notes.h")
    strings = {}
    for src in (nb, docs, wis, hol, dreams, hers, its):
        for name, body in re.findall(r"(?:static )?const u8 (\w+)\[\]\s*=\s*_\((.*?)\);", src, re.S):
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
    year = re.search(r"#define NB_YEAR_ENTRIES \\\n(.*?)(?:\n\n|\Z)", holl, re.S).group(1)   # T-416
    body = body.replace("NB_YEAR_ENTRIES", year.replace("\\", ""))
    dream = re.search(r"#define NB_DREAM_ENTRIES \\\n(.*?)(?:\n\n|\Z)", dreams, re.S).group(1)   # T-412
    body = body.replace("NB_DREAM_ENTRIES", dream.replace("\\", ""))
    her = re.search(r"#define NB_HER_DREAM_ENTRIES \\\n(.*?)(?:\n\n|\Z)", hers, re.S).group(1)   # T-412: HER DREAMS
    body = body.replace("NB_HER_DREAM_ENTRIES", her.replace("\\", ""))
    itsr = re.search(r"#define NB_ITS_DREAM_ENTRIES \\\n(.*?)(?:\n\n|\Z)", its, re.S).group(1)   # T-462: ITS DREAMS
    body = body.replace("NB_ITS_DREAM_ENTRIES", itsr.replace("\\", ""))
    #  each image's three endings, broken, quiet, vivid (quality 1, 2, 3)
    endings = [list(e) for e in re.findall(r"\{\s*(\w+),\s*(\w+),\s*(\w+)\s*\},\s*//",
                                           re.search(r"sItsDreamEndings\[.*?\{(.*?)\n\};", its, re.S).group(1))]
    #  each of her steps: the flag that says it is done, and where it led (shown once that flag is held)
    led = {told: (done, ledname) for done, told, first, second, ledname in
           re.findall(r"\{\s*(FLAG_\w+),\s*(FLAG_\w+),\s*(\w+),\s*(\w+),\s*(\w+)\s*\}", hers)}
    body = re.sub(r"//[^\n]*", "", body)
    body = re.sub(r"#if DAEMONS_DEBUG\n.*?#endif", "", body, flags=re.S)     # the release build's pages only
    rows = re.findall(r"\{\s*(NB_\w+),\s*(NB_KIND_\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\s*\}", body)
    flagnames = sorted({r[3] for r in rows} | {r[4] for r in rows if r[4] != "0"} | {d for d, n in led.values()})
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
    #  T-417: each SONGBOOK page's key and notes, from the songs' own data (docs/play_songs.json, tools/genplaysongs.py)
    songs = {t["id"]: t for t in json.load(open(os.path.join(ROOT, "docs/play_songs.json"), encoding="utf-8"))["songs"]}
    fv.update(flag_values(sorted({t["heard"] for t in songs.values() if t.get("heard")})))
    pages = []
    for sec, kind, arg, flag, flag2, title, text in rows:
        words = None
        if kind in ("NB_KIND_TEXT", "NB_KIND_HER_DREAM", "NB_KIND_ITS_DREAM"):
            words = strings.get(text) if text in strings else labels.get(text)
            if words is None:
                raise SystemExit("  refused: the NOTEBOOK's %s has no words the export can find (%s)" % (title, text))
            if arg == "1":
                words = words.split("\n\n", 1)[-1]           # the heading the title already carries
            words = re.sub(r"\{(?!RIVAL\}|PLAYER\})[^}]*\}", "", words).strip()
        page = {"section": sections.index(sec), "title": strings[title], "kind": kind[8:].lower(),
                      "flag": fv[flag], "flag2": fv[flag2] if flag2 != "0" else 0,
                      "about": abouts.get(flag[5:]), "text": words,
                      "seen": found.get(flag, (None, None))[0], "place": found.get(flag, (None, None))[1],
                      "link": links.get(flag)}
        if kind == "NB_KIND_ITS_DREAM":                     # T-462: the ending is the night last received for it
            page.update(image=int(arg), endings=[strings[e] for e in endings[int(arg)]])
        if kind == "NB_KIND_HER_DREAM":                     # T-412: where it led, once its step is done
            done, ledname = led[flag]
            page.update(led=strings[ledname], led_flag=fv[done])
        if kind == "NB_KIND_SONG":                          # T-417: play.c writes the page, its key and notes
            page["song"] = arg
            tune = songs.get(arg[len("PLAY_SONG_"):])
            if tune is None:
                raise SystemExit("  refused: docs/play_songs.json has no song %s" % arg)
            notes = tune["notes"].split()
            frames = tune.get("frames") or [tune["beat"]] * (len(notes) - 1) + [tune["last"]]
            if len(frames) != len(notes):
                raise SystemExit("  refused: %s has %d notes and %d frames" % (arg, len(notes), len(frames)))
            page.update(key=tune["key"], notes=notes, frames=frames,    # 60 fps, as the game plays it when heard
                        heard=fv.get(tune.get("heard")) if tune.get("heard") else None)
        pages.append(page)
    return {"_about": "C-125: the NOTEBOOK's pages in the game's own order, read from src/notebook.c and the headers it "
                      "includes. A page is held when the save has flag and (if not 0) flag2 -- notebook.c's own rule. "
                      "{RIVAL} and {PLAYER} are the names from the save. kind exam/choices: written by the game from "
                      "the save when opened; no words here. kind song (T-417, the SONGBOOK): drawn by the game as coloured note heads on a staff; song names the tune, key the major key it counts in, notes the motif as heard (C4 middle C, sharps or flats), frames each note's length at 60 fps as the game plays it when heard, heard the flag set once it is heard at its place (learned is flag). seen: the flag set once the page is opened in the game (unread until "
                      "then, T-403); key_colours: the twelve note colours C..B and outline the notes' outline, as the GBA shows them (T-417); place: where it was found; link: the song or post its QR code opens (T-402). kind her_dream (T-412): one of the CHECKPOINT attendant's dreams, under HER DREAMS after YOUR DREAMS in the DREAM LOG; led is where it led, shown under it once the save holds led_flag (its step done). kind its_dream (T-462): one of the carried daemon's dreams, under ITS DREAMS after HER DREAMS; text is its opening, and its page ends with endings[quality - 1] -- broken, quiet, vivid -- for the quality last filed for its image (profile_layout's its_dreams.kinds; quiet when none).",
            "sections": [strings[names[s]] for s in sections], "pages": pages,
            #  T-417: the twelve key colours, C..B, and the note outline, as the GBA shows them (tools/genplaynotes.py)
            "key_colours": [hex5(c) for c in genplaynotes.KEYS], "outline": hex5(genplaynotes.PALETTE[genplaynotes.OUTLINE])}


def hex5(c):
    """a GBA 5-bit colour as #rrggbb, each channel v*255//31"""
    return "#" + "".join("%02x" % (v * 255 // 31) for v in c)


def play_table():
    """T-426 (the user, 2026-10-18): PLAY for the companion -- the instrument, the key, the buttons and the songs as the
    game has them (src/play.c, docs/play_songs.json), so a device or the phone can be played the way the game is. The
    note sprites are the game's own (tools/genplaynotes.py draws them; ours): art/play_notes.png, art/play_small.png."""
    import genplaynotes
    songs = json.load(open(os.path.join(ROOT, "docs/play_songs.json"), encoding="utf-8"))["songs"]
    fl = flag_values(["FLAG_GOT_INSTRUMENT"] + sorted({t[k] for t in songs for k in ("learned", "heard") if t.get(k)}))
    it = flag_values(["ITEM_HARP", "ITEM_FLUTE"], "constants/items.h")
    out = []
    for t in songs:
        notes = t["notes"].split()
        out.append({"id": t["id"], "title": t["title"], "key": t["key"], "notes": notes,
                    "frames": t.get("frames") or [t["beat"]] * (len(notes) - 1) + [t["last"]],
                    "learned_flag": fl.get(t.get("learned")), "heard_flag": fl.get(t.get("heard"))})
    return {"_about": "T-426 (the user, 2026-10-18): PLAY as the game plays it. The instrument is the save's edition's "
                      "(CONTENT the HARP, CONTEXT the FLUTE; sounds/instruments.json) and is LOCKED until the save holds "
                      "got_instrument_flag (or the item). Choose a key (major keys only), then play the scale's seven "
                      "degrees; buttons are the game's (D-pad clockwise from Down 1, Left 2, Up 3, Right 4, then B 5, "
                      "A 6, SELECT 7; L an octave down, R an octave up). A song is heard from the last sixteen notes: "
                      "its key and its order count, octave and tempo do not; the right shape in another key is ALMOST. "
                      "A learned song (learned_flag held; O CHRISTMAS TREE always) joins its notes and echoes. Each note "
                      "drifts up in its key colour (key_colours, C..B; A is INDIGO). art/play_notes.png: 12 16x16 notes "
                      "C..B; art/play_small.png: 12 wheel dots, 12 staff heads, 12 hollow heads, then the rest, 8x8.",
            "got_instrument_flag": fl["FLAG_GOT_INSTRUMENT"], "items": {"HARP": it["ITEM_HARP"], "FLUTE": it["ITEM_FLUTE"]},
            "editions": {"CONTENT": "harp", "CONTEXT": "flute"},
            "keys": ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"],
            "buttons": {"DOWN": 1, "LEFT": 2, "UP": 3, "RIGHT": 4, "B": 5, "A": 6, "SELECT": 7,
                        "L": "octave down", "R": "octave up", "START": "put it away"},
            "listen": {"last_notes": 16, "counts": ["key", "order"], "ignores": ["octave", "tempo"],
                       "almost": "the right shape in another key"},
            "key_colours": [hex5(c) for c in genplaynotes.KEYS], "outline": hex5(genplaynotes.PALETTE[genplaynotes.OUTLINE]),
            "songs": out}


def play_art():
    """the game's own PLAY sprites, as genplaynotes drew them (indexed, index 0 clear)"""
    from PIL import Image
    d = os.path.join(GBA, "graphics", "play")
    return {"play_notes.png": Image.open(os.path.join(d, "notes.png")), "play_small.png": Image.open(os.path.join(d, "small.png"))}


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
                         "FLAG_SYS_B_DASH", "FLAG_SHOES_FROM_DAD", "FLAG_GOT_NOTEBOOK", "FLAG_GOT_HERMETIC_LAYER"]
                        + UNDERSTANDINGS + INSIGHTS)
    items = dict(re.findall(r"^#define\s+(ITEM_OPUS)\s+(\d+)", read("include/constants/items.h"), re.M))
    kcount = re.search(r"#define\s+BAG_KEYITEMS_COUNT\s+(\d+)", read("include/constants/global.h")).group(1)
    first_met_count = int(re.search(r"#define\s+DAEMONS_FIRST_SEEN_COUNT\s+(\d+)", read("include/constants/global.h")).group(1))
    magic = re.search(r"#define\s+FIRST_SEEN_MAGIC\s+(0x[0-9A-Fa-f]+)", read("src/daemons_first_seen.c"))
    if not magic:
        raise SystemExit("  refused: FIRST_SEEN_MAGIC not found in src/daemons_first_seen.c")
    FIRST_MET_MAGIC = int(magic.group(1), 16)
    #  a map section's number is its place in region_map_sections.json (the enum is generated in that order)
    first_met_places = {str(n): sec["name"] for n, sec in
                        enumerate(json.loads(read("src/data/region_map/region_map_sections.json"))["map_sections"])
                        if sec.get("name")}
    return {"_about": "C-23: offsets into SaveBlock2 (section 0) and SaveBlock1 (sections 1-4, end to end), read from "
                      "global.h's own struct comments; flag numbers resolved from flags.h. A flag below "
                      "daemons_flags_start is a bit in SaveBlock1's flags, one at or above it a bit in SaveBlock2's "
                      "daemonsFlags. INDEX flags are by national number minus one. Money is stored XOR the "
                      "encryption key. A daemon is SEEN only when sb2 index_seen and sb1 seen1 and seen2 all have its bit "
                      "(pokedex_screen.c's anticheat), so a writer sets all three. T-427: house_take is the house's take "
                      "(what the GAME CORNER and the CASINO kept, in money), house_take_bytes wide, signed little-endian "
                      "(negative while the player is ahead), stored plain -- NOT XORed as money is. Only ever added to. "
                      "house_take_at_fall is the take as it stood when CORPUS fell (the game freezes it there, once; "
                      "VERDIGRIS names it), same width and sign -- the game's to write, never a writer's. "
                      "T-406: sb1 first_met is where each daemon was first SEEN, first_met_bytes bytes, one per national "
                      "number (number - 1), each a map section first_met_places names (0: not recorded); trust them only "
                      "when the u32 at first_met_magic is first_met_magic_value (an older save holds a recap scene there). "
                      "A SEEN daemon with 0 was seen before the game kept them: the INDEX says BEFORE RECORDS.",
            "sb2": {"player_name": sb2["playerName"], "player_gender": sb2["playerGender"],
                    "trainer_id": sb2["playerTrainerId"], "play_time_hours": sb2["playTimeHours"],
                    "play_time_minutes": sb2["playTimeMinutes"], "play_time_seconds": sb2["playTimeSeconds"],
                    "index_bound": sb2["pokedex"] + dex["owned"], "index_seen": sb2["pokedex"] + dex["seen"],
                    "index_bytes": dex["seen"] - dex["owned"],
                    "daemons_flags": sb2["daemonsFlags"], "encryption_key": sb2["encryptionKey"],
                    #  T-427: the house's take, beside the money it is counted in (C-167 adds the CASINO's at SYNC)
                    "house_take": sb2["houseTake"], "house_take_bytes": 4, "house_take_signed": True,
                    "house_take_at_fall": sb2["houseTakeAtFall"]},
            "sb1": {"location": sb1["location"], "flags": sb1["flags"], "money": sb1["money"],
                    "rival_name": sb1["rivalName"],                                    # C-125: the name the player gave
                    "key_items": sb1["bagPocket_KeyItems"], "key_items_count": int(kcount),
                    #  C-128: the PLUGIN pocket holds the eight DRIVERS (and every PLUGIN), the items pocket TEA
                    "tmhm": sb1["bagPocket_TMHM"], "tmhm_count": int(re.search(r"#define\s+BAG_TMHM_COUNT\s+(\d+)", read("include/constants/global.h")).group(1)),
                    "items_pocket": sb1["bagPocket_Items"], "items_count": int(re.search(r"#define\s+BAG_ITEMS_COUNT\s+(\d+)", read("include/constants/global.h")).group(1)),
                    # C-15: the INDEX's seen flags are kept three times; the game believes them only when all agree
                    "seen1": sb1["seen1"], "seen2": sb1["seen2"],
                    # T-406: where each daemon was first met -- a byte per national number (index = number - 1), its
                    # map section (first_met_places names it; 0 = not recorded). Believe the bytes only when the magic
                    # at first_met_magic (u32, little-endian) is first_met_magic_value: an older save holds a recap scene
                    # there. A daemon SEEN with 0 was seen before the game kept these (the INDEX: BEFORE RECORDS).
                    "first_met": sb1["daemonsFirstSeen"], "first_met_bytes": first_met_count,
                    "first_met_magic": sb1["daemonsFirstSeenMagic"], "first_met_magic_value": FIRST_MET_MAGIC,
                    "first_met_places": first_met_places},
            "flags": {"marks_first": flags["FLAG_BADGE01_GET"], "marks_last": flags["FLAG_BADGE08_GET"],
                      "index": flags["FLAG_SYS_POKEDEX_GET"], "game_clear": flags["FLAG_SYS_GAME_CLEAR"],
                      "diploma": flags["FLAG_GOT_DIPLOMA"], "daemons_flags_start": flags["DAEMONS_FLAGS_START"],
                      "companion_linked": flags["FLAG_COMPANION_LINKED"],
                      "companion_recalled": flags["FLAG_COMPANION_RECALLED"],
                      # C-125: the PROFILE's more -- whose shoes, the understandings and insights held, the NOTEBOOK
                      "shoes": flags["FLAG_SYS_B_DASH"], "shoes_from_dad": flags["FLAG_SHOES_FROM_DAD"],
                      "notebook": flags["FLAG_GOT_NOTEBOOK"],
                      "hermetic_layer": flags["FLAG_GOT_HERMETIC_LAYER"],     # T-483 / C-238: SPELLCRAFT, written at a sync
                      "understandings": [flags[f] for f in UNDERSTANDINGS],
                      "insights": [flags[f] for f in INSIGHTS]},
            "items": {"opus": int(items["ITEM_OPUS"])},
            "reads": reads_layout(sb1),
            "its_dreams": its_dreams_layout(sb1, sb2, flags["DAEMONS_FLAGS_START"])}


def its_dreams_layout(sb1, sb2, daemons_start):
    """T-462 / C-200: ITS DREAMS -- the vars a SYNC writes for a new dream, the game's own record of what it has filed,
    and the sixteen images' titles (docs/its_dreams.json, as the ROM holds them in src/data/its_dreams.h)."""
    names = ["VARS_START", "VAR_ITS_DREAM", "VAR_ITS_DREAM_HOURS", "VAR_ITS_DREAM_NIGHTS", "VAR_ITS_DREAM_DAY",
             "VAR_ITS_DREAM_FILED", "VAR_ITS_DREAM_STAMP", "VAR_ITS_DREAM_KINDS", "VAR_ITS_DREAM_KINDS_2"]
    v = flag_values(names, header="constants/vars.h")
    first = flag_values(["FLAG_ITS_DREAM_GRASS"])["FLAG_ITS_DREAM_GRASS"]
    at = lambda n: sb1["vars"] + (v[n] - v["VARS_START"]) * 2
    its = read("src/data/its_dreams.h")
    titles = [gba_string(b) for b in re.findall(r"static const u8 sItsDreamTitle_\w+\[\]\s*=\s*_\((.*?)\);", its, re.S)]
    count = int(re.search(r"#define ITS_DREAM_COUNT\s+(\d+)", its).group(1))
    if len(titles) != count:
        raise SystemExit("  refused: its_dreams.h has %d titles for %d images" % (len(titles), count))
    return {"_about": "T-462 / C-200: ITS DREAMS. Each var is a u16 (little-endian) in SaveBlock1 at the sb1 offset "
                      "given (vars + (var - vars_start) * 2). The COMPANION writes the four under 'write' at a SYNC "
                      "that brings a new dream and leaves them as they are when there is none: dream = quality "
                      "(1 broken, 2 quiet, 3 vivid) | 4 if tucked in | image << 8; hours in tenths; nights = nights "
                      "since the last SYNC | rested nights << 8 (each capped 255); day = days since 2026-01-01. The "
                      "GAME treats a day it has not filed as a new dream and files it at the first dawn after it sees "
                      "it (or on the first load on a later day). The rest is the game's and never written by a "
                      "writer: filed = the day + 1 of the last dream filed (0 none); kinds / kinds_2 = the quality "
                      "last filed for images 0-7 / 8-15, two bits each, image 0 lowest (0 never filed); and "
                      "image n is filed when DAEMONS flag filed_flag_first + n is set (a bit in sb2 daemons_flags, as "
                      "profile_layout explains). titles: each image's title in the NOTEBOOK, in image order. DRAFT.",
            "vars_start": v["VARS_START"], "vars": sb1["vars"],
            "write": {n: {"var": v[k], "sb1": at(k)} for n, k in
                      (("dream", "VAR_ITS_DREAM"), ("hours", "VAR_ITS_DREAM_HOURS"),
                       ("nights", "VAR_ITS_DREAM_NIGHTS"), ("day", "VAR_ITS_DREAM_DAY"))},
            "game": {n: {"var": v[k], "sb1": at(k)} for n, k in
                     (("filed", "VAR_ITS_DREAM_FILED"), ("stamp", "VAR_ITS_DREAM_STAMP"),
                      ("kinds", "VAR_ITS_DREAM_KINDS"), ("kinds_2", "VAR_ITS_DREAM_KINDS_2"))},
            "filed_flag_first": first, "filed_flag_sb2_bit": first - daemons_start,
            "daemons_flags_sb2": sb2["daemonsFlags"],
            "titles": titles}


def reads_layout(sb1):
    """C-203: THE LOG (DAEMONS T-459 B and C), the NOTEBOOK's READS page, as the game composes it from the save's vars
    (daemons_reads.c Daemons_WriteReadsLog) -- so the companion can write it the same way, words and all."""
    v = flag_values(["VARS_START", "VAR_READS_GIVEN", "VAR_READS_LANDED", "VAR_LEANS_TOLD", "VAR_LEANS_LANDED",
                     "VAR_READ_LOG_WHERE", "VAR_READ_LOG_THING"], header="constants/vars.h")
    rc = read("src/daemons_reads.c")
    rh = read("include/daemons_reads.h")
    num = lambda pat, text: int(re.search(pat, text).group(1), 0)
    order = re.findall(r"(PHRASE_\w+)", re.search(r"enum\s*\{(.*?)PHRASE_COUNT", rc, re.S).group(1))
    table = dict(re.findall(r"\[(PHRASE_\w+)\]\s*=\s*(sPhrase_\w+)", rc))
    words = dict(re.findall(r'static const u8 (s(?:Phrase|Log)_\w+)\[\]\s*=\s*_\("(.*?)"\);', rc))
    plain = lambda w: w.replace("{STR_VAR_1}", "{1}").replace("{STR_VAR_2}", "{2}").replace("\\p", "")
    if len(order) != len(table) or any(o not in table for o in order):
        raise SystemExit("  refused: daemons_reads.c's phrases and their table disagree")
    return {"_about": "C-203: THE LOG's vars, each u16 at sb1 vars + (var - vars_start) * 2. where: newest first, "
                      "log of them -- the map section in the low byte (first_met_places names it; 0: an empty row, "
                      "the log ends), the phrase at phrase_shift (phrase_mask wide), landed at landed_bit. thing: the "
                      "flag that says that read's thing was found, 0 for a read about nothing; a read whose flag is "
                      "set has landed even before the game marks it (the game marks it, and counts it, on the next "
                      "arrival or when the page is opened). Lines: reads and leans with {1} {2}, then each read "
                      "'<place><colon><phrase>' and landed after it when it has.",
            "vars": sb1["vars"], "vars_start": v["VARS_START"],
            "given": v["VAR_READS_GIVEN"], "landed": v["VAR_READS_LANDED"],
            "leans_told": v["VAR_LEANS_TOLD"], "leans_landed": v["VAR_LEANS_LANDED"],
            "where": v["VAR_READ_LOG_WHERE"], "thing": v["VAR_READ_LOG_THING"],
            "log": num(r"#define\s+READ_LOG\s+(\d+)", rh),
            "landed_bit": num(r"#define\s+READ_LANDED\s+\(1\s*<<\s*(\d+)\)", rc),
            "phrase_shift": num(r"#define\s+READ_PHRASE\(w\)\s+\(\(\(w\)\s*>>\s*(\d+)\)", rc),
            "phrase_mask": num(r"#define\s+READ_PHRASE\(w\).*?&\s*(0x[0-9A-Fa-f]+)\)", rc),
            "phrases": [words[table[o]] for o in order],
            "words": {"reads": plain(words["sLog_Reads"]), "leans": plain(words["sLog_Leans"]),
                      "colon": words["sLog_Colon"], "landed": words["sLog_Landed"]}}


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
        marks[n - 1]["wisdom"] = {"leader": pr["leader"], "virtue": pr["virtue"], 
                                  "without": pr["without"], "with": pr["with"], "explain": pr["explain"],
                                  "union_plugin": pr["plugin_name"], "union_routine": pr["routine"],
                                  "insight": pr["insight"],
                                  #  numbers, as the save reader works from them (the companion session, 2026-10-16)
                                  "root_flag": wf[pr["root"]], "given_flag": wf[pr["given"]],
                                  "insight_flag": wf[pr["insight_flag"]]}
    tc = read("src/trainer_card.c")
    lobes = re.findall(r"\{ (FLAG_UNDERSTANDING_\w+),\s*\w+,\s*RGB\((\d+), (\d+), (\d+)\)\s*\},\s*//\s*(\w+)\s+(\w+)", tc)
    debug = read("src/daemons_debug_events.c")
    #  T-252: the user named them 2026-10-16; the debug labels carry the name and its place, "STILL (TANOBY)"
    named = {int(n): t.split(" (")[0] for n, t in re.findall(r"sName_Root(\d)\[\] = _\(\"([^\"]*)\"\)", debug)}
    #  where each understanding is found stays out: the companion is public, and the game asks the player to find
    #  them (the user, 2026-10-24)
    unders = []
    for k, (flag, r, g, b, lobe, ty) in enumerate(lobes):
        unders.append({"n": k + 1, "flag": flags[flag], "_flag_name": flag, "lobe": lobe, "type": ty,
                       "rgb": rgb8(int(r), int(g), int(b)), "name": named.get(k + 1, ""), "name_is_working": False,
                       # T-405 (approved 2026-10-16): its STREAM lecture, as the MARKS' -- its two scripts
                       "lesson": [t for t in (text("gTeachyTvText_Root%dScript1" % (k + 1)),
                                              text("gTeachyTvText_Root%dScript2" % (k + 1))) if t] or None})
    return {"_about": "C-126: the MARKS (badge art, STREAM lesson, town) and the UNDERSTANDINGS (brain lobe, colour)"
                      ". Understanding names are the user's (T-252, 2026-10-16); "
                      "their lessons are T-405's STREAM lectures, as the MARKS' are. Order matches profile_layout's flags.understandings.",
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

def guide_table():
    """THE PROGRAMMER'S GUIDE TO THE HUMAN MIND for the companion's reading tab (the user via the companion session,
    2026-10-16): docs/guide.md in its order, read by genguide.py's own parse, each paragraph plain text. Held once
    FLAG_GOT_GUIDE is set. The words are the game's DRAFT (T-315) and already public in docs/guide.md."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import genguide
    sections = []
    for sec in genguide.parse():
        sections.append({"key": sec["key"], "label": sec["label"], "heading": sec["heading"],
                         "entries": [{"short": e["short"], "title": e["title"],
                                      "paragraphs": [" ".join(p) for p in e["paras"] if p]} for e in sec["entries"]]})
    #  Its last page is a QR code (book_reader.c, BOOK_QR_GUIDE): on the companion it is a link, on that last entry
    import gbaqr
    sections[-1]["entries"][-1]["link"] = dict(gbaqr.CODES)["Guide"]
    return {"flag": flag_values(["FLAG_GOT_GUIDE"])["FLAG_GOT_GUIDE"], "draft": True,
            "title": "THE PROGRAMMER'S GUIDE TO THE HUMAN MIND", "author": "CHRISTOPHER ART HICKS",   # the cover sets them (no lettering in art/guide_cover.png)
            "sections": sections}


def guide_cover():
    """The GUIDE's 8-bit cover (240x160) WITHOUT its lettering (the user, 2026-10-18): the game letters it in its own
    font, which is Nintendo's, and the companion is public -- so the app sets the title and the author's name in its
    own type (guide.json's title and author). The art is ours: the boards, the rules, the brain from the user's book."""
    import genguide
    return genguide.build_cover(lettered=False).convert("RGB")


def subtle_table():
    """T-423: THE SUBTLE LAYER for the companion's LIBRARY (the user, 2026-10-18: "both, in parallel"): docs/subtle-layer.md
    read by tools/gensubtle.py, each paragraph plain text, the asking voice marked, each entry's picture and its frame
    count (the phone cannot list the art). Held once FLAG_GOT_SUBTLE_LAYER is set, as the GUIDE is. The words are the
    game's DRAFT and already public in docs/subtle-layer.md; the pictures carry nothing set in the game's font."""
    import gensubtle
    book = gensubtle.subtle_book()
    book["flag"] = flag_values(["FLAG_GOT_SUBTLE_LAYER"])["FLAG_GOT_SUBTLE_LAYER"]
    book["cover"] = "art/subtle_cover.png"
    return book


def hermetic_table():
    """T-483 / C-238: THE HERMETIC LAYER for the companion's LIBRARY -- docs/hermetic-layer.md, in docs/subtle-layer.md's
    format, read by gensubtle's own parser: each paragraph plain text, the asking voice ('~ ') and the INSCRIPTION ('^ ',
    the tablet's emerald, read aloud on its own) marked. Each entry names its picture; the game has not drawn them yet, so
    there are no frames. Held once FLAG_GOT_HERMETIC_LAYER is set (written by the companion at a sync, or in the game).
    DRAFT, every word."""
    import gensubtle
    keep = gensubtle.SRC
    gensubtle.SRC = os.path.join(ROOT, "docs/hermetic-layer.md")
    try:
        sections = gensubtle.parse()
    finally:
        gensubtle.SRC = keep
    out = []
    for s in sections:
        entries = []
        for e in s["entries"]:
            paras = []
            for k, q in enumerate(e["paras"]):
                voice = "asking" if k in e["faint"] else "inscription" if q.startswith("^ ") else "telling"
                paras.append({"text": q[2:] if voice == "inscription" else q, "voice": voice})
            entries.append({"short": e["short"], "title": e["title"], "picture": e["sprite"], "frames": 0,
                            "caption": e["caption"], "paragraphs": paras})
        out.append({"label": s["label"], "heading": s["heading"], "entries": entries})
    flag = flag_values(["FLAG_GOT_HERMETIC_LAYER"])["FLAG_GOT_HERMETIC_LAYER"]
    return {"title": "THE HERMETIC LAYER", "subtitle": "SPELLCRAFT", "draft": True, "flag": flag, "sections": out}


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
                   "EV_MARKS_ALL", "EV_DRIVERS_ALL", "EV_ROOTS_ALL", "EV_SONGS_ALL",
                   "EV_YEAR_ALL", "EV_GIFTS_AGAIN",                                        # T-416
                   "EV_CRYSTAL_AGAIN",                                                     # T-457: a reset, not an event
                   "EV_SOUNDING",                                                          # T-458: the companion's signal, faked
                   "EV_ITS_DREAM",                                                         # T-462: the companion's dream, faked
                   "EV_TRADE_IN", "EV_LOAN_IN",                                            # T-473: the companion's trade, faked
                   "EV_PAIR_PENGUIN", "EV_PAIR_DOLPHIN", "EV_PAIR_OTHER", "EV_PAIR_LOAN"}  # T-474: its pair trade, faked
#  T-18: a page that is a debug SETTING, not the story -- the follower on or off, the lead's friendship set.
PAGES_LEFT_OUT = {"PG_FOLLOWER", "PG_FEELINGS", "PG_THREE"}        # T-431: the feelings' debug view and its clock; T-454: THE THREE's


def events_table():
    """C-128: the PROFILE's GAME EVENTS -- every row of the debug menu's GAME EVENTS page (src/daemons_debug_events.c) in
    story order, a sub-page's rows (MARKS, NOTEBOOK, DRIVERS, UNDERSTANDINGS, SONGBOOK) where its row stands, each with the test
    the page's IsHeld makes for its + or ·, as flags and a var. The debug's own kit (EVERYTHING, THE ROSTER, EVERY
    DAEMON, THE STOCK, EVERY PAGE), each sub-page's ALL and LET INSIGHTS ARRIVE AGAIN are left out. A row held by a
    bag item has held null and its items, since the bag is not a flag."""
    src = read("src/daemons_debug_events.c")
    strings = _c_strings(src)
    strings.update(_c_strings(read("src/data/daemons_holidays.h")))     # T-416: THE YEAR's rows are its lines' titles
    year_lines = [l["id"] for l in json.load(open(os.path.join(ROOT, "docs", "holidays.json"), encoding="utf-8"))["lines"]]
    def rows(arr):
        body = re.search(r"%s\[\]\s*=\s*\{(.*?)\n\};" % arr, src, re.S).group(1)
        return [(n, k, ev, int(off or 0)) for n, k, ev, off in
                re.findall(r"\{\s*((?:sName|gYearTitle)_\w+),\s*(R_\w+),\s*(\w+)(?:\s*\+\s*(\d+))?\s*\}", body)]
    titles = {pg: re.split(r"[,:]", strings[t])[0] for pg, t in
              zip(["PG_EVENTS", "PG_MARKS", "PG_NOTEBOOK", "PG_DRIVERS", "PG_ROOTS", "PG_SONGS", "PG_YEAR"],
                  re.search(r"sTitles\[PG_COUNT\]\s*=\s*\{(.*?)\};", src, re.S).group(1).replace(",", " ").split())}
    pages = {"PG_MARKS": "sRows_Marks", "PG_NOTEBOOK": "sRows_Notebook", "PG_DRIVERS": "sRows_Drivers",
             "PG_ROOTS": "sRows_Roots", "PG_SONGS": "sRows_Songs", "PG_YEAR": "sRows_Year"}
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
            if ev in PAGES_LEFT_OUT:
                continue
            for sname, skind, sev, soff in rows(pages[ev]):
                if sev in EVENTS_LEFT_OUT:
                    continue
                if sev == "EV_MARK1":
                    plan.append((titles[ev], sname, [marks[soff]], None, None, None))
                elif sev == "EV_ROOT1":
                    plan.append((titles[ev], sname, [roots[soff]], None, None, None))
                elif sev == "EV_SONG1":         # T-417: the fir's song, then the seven (FLAG_SONG_FIR, FLAG_SONG_1..)
                    plan.append((titles[ev], sname, ["FLAG_SONG_%s" % (soff or "FIR")], None, None, None))
                elif sev == "EV_YEAR1":         # T-416: THE YEAR's lines, in the year's order
                    plan.append((titles[ev], sname, ["FLAG_YEAR_LINE_%s" % year_lines[soff]], None, None, None))
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
        #  a debug label carries its place, "STILL (TANOBY)": the companion is public, so only the name goes (review 2026-10-28)
        row = {"n": k + 1, "name": strings[name].split(" (")[0], "section": sec}
        if flags is None:
            row["held"] = None
            row["items"] = [{"name": i if not o else "%s + %d" % (i, o), "id": it[i] + o} for i, o in items]
        else:
            row["held"] = {"all_flags": [fl[f] for f in flags]}     # numbers only: a flag's name says where
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


def holidays_table():
    """C-149 / T-416: the holidays by their real names, from the game's own table (docs/holidays.json, through
    tools/genholidays.py's companion_doc), so the companion and the game cannot disagree."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    argv, sys.argv[:] = list(sys.argv), [sys.argv[0]]
    try:
        import genholidays
    finally:
        sys.argv[:] = argv
    #  written in genholidays' own layout (one holiday a line), as the companion's file already is
    return genholidays.companion_text(json.load(open(os.path.join(ROOT, "docs", "holidays.json"), encoding="utf-8")))


def _height_text(dm):
    """the INDEX's HT, as DexScreen_PrintMonHeight prints it: decimetres to feet and inches, rounded to the inch"""
    tenths = 10000 * dm // 254
    if tenths % 10 >= 5:
        tenths += 10
    feet = tenths // 120
    return "%d'%02d\"" % (feet, (tenths - feet * 120) // 10)


def _weight_text(hg):
    """the INDEX's WT, as DexScreen_PrintMonWeight prints it: hectograms to pounds, to a tenth"""
    lbs = hg * 100000 // 4536
    if lbs % 10 >= 5:
        lbs += 10
    return "%d.%d lbs." % (lbs // 100, (lbs % 100) // 10)


def index_cards_table(species, margins, marks, guide):
    """T-453 (C-186): the INDEX card, whole, for the iPad app to draw from a save -- everything pokedex_screen.c shows
    that is static (number, name, types and their colours, category, HT and WT, both editions' entries, NATIVE, the
    workings' line and routines, OPUS's margins) and the rules for what a save decides (seen or bound, FIRST MET,
    BOUND, which margin). With the seven UNDERSTANDINGS: their flags, names and colours, and the margin each writes
    in -- which is the GUIDE's, not OPUS's: the game ties no OPUS margin to an understanding."""
    entries = read("src/data/pokemon/pokedex_entries.h")
    hw = {}
    for m in re.finditer(r"\[NATIONAL_DEX_(\w+)\]\s*=\s*\{((?:(?!\[NATIONAL_DEX_).)*)", entries, re.S):
        h, w = re.search(r"\.height\s*=\s*(\d+)", m.group(2)), re.search(r"\.weight\s*=\s*(\d+)", m.group(2))
        if h and w:
            hw[m.group(1)] = (int(h.group(1)), int(w.group(1)))
    alias = {a: b for a, b in re.findall(r"#define SPECIES_(\w+)\s+SPECIES_(\w+)\b", read("include/constants/species.h"))}
    by_slot = {b: a for a, b in alias.items()}
    #  the workings (L on a bound daemon): the routines it learns, level by level
    ls = read("src/data/pokemon/level_up_learnsets.h")
    sets = {name: [(int(l), mv) for l, mv in re.findall(r"LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)\)", body)]
            for name, body in re.findall(r"static const u16 (s\w+LevelUpLearnset)\[\]\s*=\s*\{(.*?)\};", ls, re.S)}
    ptr = dict(re.findall(r"\[SPECIES_(\w+)\]\s*=\s*(s\w+LevelUpLearnset)", read("src/data/pokemon/level_up_learnset_pointers.h")))
    move_ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define MOVE_(\w+)\s+(\d+)\b", read("include/constants/moves.h"))}
    move_names = dict(re.findall(r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/data/text/move_names.h")))
    #  the type words' colours (type_colours.h: the INDEX names both types in these, as the move menu does)
    typename = dict(re.findall(r'\[TYPE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/battle_main.c")))
    type_colours = {typename.get(t, t): hex5((int(r), int(g), int(b))) for t, r, g, b in
                    re.findall(r"\[TYPE_(\w+)\s*\]\s*=\s*RGB\(\s*(\d+),\s*(\d+),\s*(\d+)\)", read("src/data/type_colours.h"))}
    #  the party art companion_export writes (party_art's own test, without drawing it)
    def party(row):
        if not row["art"]["front"]:
            return None
        d = os.path.join(GBA, "graphics/pokemon", row["constant"].lower())
        if not os.path.isdir(d):
            d = os.path.join(GBA, "graphics/pokemon", "nexus_" + row["name"].lower())
        if not (os.path.exists(os.path.join(d, "front.4bpp")) and os.path.exists(os.path.join(d, "normal.gbapal"))):
            return None
        if "/symbol/" in row["art"]["front"]:
            return "art/symbol.png"
        return "art/" + os.path.basename(row["art"]["front"]).replace("_front.png", "") + ".png"
    #  the understandings: marks.json's, with the GUIDE margin each writes in (book_reader.c sGuideMarginNotes), how it
    #  is arrived at (sUnderstandingConditions) and the balance written under it once its MARK is held (T-410)
    br = read("src/book_reader.c")
    bs = _c_strings(br)
    entry_no = {"GUIDE_ENTRY_DREAMS": int(re.search(r"#define GUIDE_ENTRY_DREAMS\s+(\d+)", br).group(1))}
    notes = {f: (int(entry_no.get(e, e)), bs[t]) for f, e, t in
             re.findall(r"\{\s*(FLAG_UNDERSTANDING_\w+),\s*(\w+),\s*(sText_Margin\w+)\s*\}", br)}
    conds = {f: sorted(set(re.findall(r"FLAG_\w+", n))) for f, n in
             re.findall(r"\{\s*(FLAG_UNDERSTANDING_\w+),\s*\{([^}]*)\}\s*\}", br)}
    chapters = [(sec["key"], e["short"], e["title"]) for sec in guide["sections"] for e in sec["entries"]]
    wis = {p["root"]: p for p in json.load(open(os.path.join(ROOT, "docs", "wisdom.json"), encoding="utf-8"))["pairs"]}
    need = sorted({f for fs in conds.values() for f in fs} | {p["badge"] for p in wis.values()})
    fv = flag_values(need)
    unders = []
    for u in marks["understandings"]:
        e, note = notes[u["_flag_name"]]
        pair = wis.get(u["_flag_name"])
        unders.append({
            "n": u["n"], "name": u["name"], "flag": u["flag"],    # no flag NAME: FLAG_UNDERSTANDING_<place> says where
            "rgb": u["rgb"], "hex": "#%02x%02x%02x" % tuple(u["rgb"]), "lobe": u["lobe"], "lobe_type": u["type"],
            # where it is found and what makes it arrive stay out: the companion is public and the game asks the
            # player to find them (the iOS lane's catch, 2026-10-24); the app only needs to know whether it is held
            "guide_margin": {"entry": e, "section": chapters[e][0], "chapter": chapters[e][1], "title": chapters[e][2],
                             "note": note},
            "balance": {"text": pair["root_balance"], "mark_flag": fv[pair["badge"]], "mark_flag_name": pair["badge"]}
                       if pair and pair.get("root_balance") else None})
    by_type = {}
    for u in unders:
        by_type.setdefault(u["lobe_type"], []).append(u["n"])
    #  the save's side: where a met location is a place, and the substruct bit a gift carries
    rmh = read("include/constants/region_map_sections.h")
    enum = re.findall(r"\b(MAPSEC_\w+),", re.search(r"enum\s*\{(.*?)\};", rmh, re.S).group(1))   # from 0, in order
    rs = {k: int(v, 0) for k, v in re.findall(r"#define (METLOC_\w+)\s+(0x[0-9A-Fa-f]+|\d+)", rmh)}
    rs["KANTO_MAPSEC_START"] = enum.index(re.search(r"#define KANTO_MAPSEC_START\s+(MAPSEC_\w+)", rmh).group(1))
    rs["MAPSEC_NONE"] = enum.index("MAPSEC_NONE")
    cards = {}
    for sid, row in species.items():
        if row["name"] == "?":                  # an unused slot: the INDEX never shows one
            continue
        sp = row["constant"]
        nat_name = by_slot.get(sp, sp)
        h, w = hw.get(nat_name, hw.get(sp, (None, None)))
        learn = [{"level": l, "move": move_ids.get(mv), "name": move_names.get(mv, mv)}
                 for l, mv in sets.get(ptr.get(sp), [])]
        mg = margins["margins"].get(sid)
        cards[sid] = {
            "constant": sp, "national": row["national"], "number": "%03d" % row["national"] if row["national"] else None,
            "name": row["name"], "types": row["types"],
            "type_colours": [type_colours.get(t) for t in row["types"]],
            "category": row["category"],
            "height_dm": h, "weight_hg": w,
            "height": _height_text(h) if h is not None else None, "weight": _weight_text(w) if w is not None else None,
            "entry": row["entry"],
            "art": {"front": row["art"]["front"], "back": row["art"]["back"], "party": party(row)},
            "native": row["native"],
            "evolutions": row["evolutions"],
            "learnset": learn,
            "margins": mg,
            "shares_type_with_understandings": sorted({n for t in row["types"] for n in by_type.get(t, [])}),
        }
    return {
        "_about": "T-453 (C-186): the INDEX card, one per species, keyed by the internal species id a save stores (as "
                  "species.json). Everything static that pokedex_screen.c draws; the save decides the rest (rules). "
                  "number is the No. as printed (three digits). type_colours are the type words' colours (type_colours.h), "
                  "one per type. height/weight are as the card prints them (HT, WT), height_dm/weight_hg the raw values. "
                  "entry: CONTENT for a FireRed-built save, CONTEXT for LeafGreen. art.front/back are DAEMONS-repo paths "
                  "(gfx/daemons, ours), art.party the companion's own art/ file. native is the NATIVE box (species.json). "
                  "evolutions and learnset are the WORKINGS page (L on a bound daemon): the line, and the routines by "
                  "level (move ids as moves.json). margins: OPUS's four lines, or null where OPUS has none (margin_rule "
                  "says which shows). understandings: the seven, each with its save flag, its colour (the USER card's "
                  "brain lobe, trainer_card.c) and the margin it writes in -- a note in a GUIDE chapter "
                  "(book_reader.c), never an OPUS margin: the game links no species or OPUS margin to an "
                  "understanding. shares_type_with_understandings is only a join -- the understandings whose lobe is "
                  "coloured as one of this species' types (each lobe IS a type's colour) -- not a rule the game has.",
        "rules": {
            "seen": "name, number and picture once SEEN (profile_layout: all three seen bitfields agree); types, "
                    "HT, WT, the type mark and the entry only once BOUND (index_bound) -- before that the card prints "
                    "?? for HT and WT and no types.",
            "first_met": "on the area page once SEEN: FIRST MET over the place (profile_layout sb1.first_met, a map "
                         "section by national number - 1; first_met_places names it); 0 prints BEFORE RECORDS.",
            "bound": "the WORKINGS' first line, from the first held daemon of the species (the party in order, then "
                     "the boxes in order, eggs skipped): BY TRADE if met_location is in_game_trade or its OT is not "
                     "the player; FROM AN EGG if met level is 0 or met_location is special_egg; A GIFT if substruct 0's "
                     "u16 at byte 10 has bit 0 set (gift_bit) or met_location is fateful_encounter; else the place "
                     "named by met_location when kanto_mapsec_start <= it < mapsec_none. None held: no line.",
            "met_locations": {"kanto_mapsec_start": rs["KANTO_MAPSEC_START"], "mapsec_none": rs["MAPSEC_NONE"],
                              "special_egg": rs["METLOC_SPECIAL_EGG"], "in_game_trade": rs["METLOC_IN_GAME_TRADE"],
                              "fateful_encounter": rs["METLOC_FATEFUL_ENCOUNTER"]},
            "gift_bit": {"substruct": 0, "byte": 10, "bit": 0},
            "margin_rule": "as margins.json: no margin without OPUS (item opus in the bag); CARRIED once any of the "
                           "species in the party or a box has gained levels_carried levels since met; NEGLECTED if "
                           "only boxed without; else none. INSTINCT's lines when player_gender is instinct_gender and "
                           "the species has them. SELECT turns the entry to the margin on the card.",
            "levels_carried": margins["levels_carried"], "instinct_gender": margins["instinct_gender"],
            "guide_margin_rule": "an understanding's note shows under its GUIDE chapter once its flag is held; its "
                                 "balance under the note once mark_flag is held too.",
        },
        "type_colours": type_colours,
        "understandings": unders,
        "cards": cards,
    }


#  T-453: the patches the app applies on the device. GitHub turns the spaces in an asset's name into dots.
GH_REPO = "CodeMusic/DAEMONS"
PATCHES_FROM = (11, 309, 1)
PATCH_SOURCES = [   # (edition, game, revision, the patch's file, the retail ROM's pret .sha1 file)
    ("CONTENT", "FireRed", "1.0", "DAEMONS CONTENT for FireRed 1.0.bps", "firered.sha1"),
    ("CONTENT", "FireRed", "Rev 1", "DAEMONS CONTENT for FireRed Rev 1.bps", "firered_rev1.sha1"),
    ("CONTEXT", "LeafGreen", "1.0", "DAEMONS CONTEXT for LeafGreen 1.0.bps", "leafgreen.sha1"),
    ("CONTEXT", "LeafGreen", "Rev 1", "DAEMONS CONTEXT for LeafGreen Rev 1.bps", "leafgreen_rev1.sha1"),
]


def patches_table():
    """T-453 (C-186): every release from v11.309.1 that is on GitHub, its four BPS patches described -- never the
    patches themselves. Read from ROM RELEASE/ (the notes for the target ROMs' SHA-1, the local PATCHES/ for each
    patch's size, hashes and the CRC32s in its footer) and checked against HOW_TO_PATCH.md's retail table. A sealed
    group keeps only its last release's patches, so a release whose files are gone keeps the row the last export
    wrote. Which releases are published is asked of gh once; without gh, the last export's list stands."""
    import glob, hashlib, struct, subprocess, zlib
    rel = os.path.join(ROOT, "ROM RELEASE")
    old_path = os.path.join(OUT, "patches.json")
    old = json.load(open(old_path, encoding="utf-8")) if os.path.exists(old_path) else {"releases": []}
    kept = {r["version"]: r for r in old.get("releases", [])}
    vt = lambda v: tuple(int(x) for x in v.split("."))
    r = subprocess.run(["gh", "release", "list", "-R", GH_REPO, "--json", "tagName", "-L", "1000"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        published = {t["tagName"][1:] for t in json.loads(r.stdout) if re.fullmatch(r"v\d+\.\d+\.\d+", t["tagName"])}
    else:
        print("  !! gh could not list the releases; patches.json keeps the releases it had")
        published = set(kept)
    #  the retail ROMs, as the player's guide gives them (CRC32, SHA-1, MD5), checked against pret's .sha1 files
    guide = open(os.path.join(rel, "HOW_TO_PATCH.md"), encoding="utf-8").read()
    rows = re.findall(r"^\| Pok.mon (FireRed|LeafGreen) \(([^)]*)\) \*\*([^*]+)\*\* \| `([0-9A-F]{8})` \| `([0-9a-f]{40})` \|", guide, re.M)
    md5 = {(g, rv): h for g, rv, h in re.findall(r"(FireRed|LeafGreen) (1\.0|Rev 1)\s+`([0-9a-f]{32})`", guide)}
    retail = {}
    for game, region, rev, crc, sha in rows:
        retail[(game, rev)] = {"region": region, "crc32": crc, "sha1": sha, "md5": md5.get((game, rev))}
    for ed, game, rev, _, sha_file in PATCH_SOURCES:
        want = open(os.path.join(GBA, sha_file)).read().split()[0]
        if retail.get((game, rev), {}).get("sha1") != want:
            raise SystemExit("  refused: HOW_TO_PATCH.md's %s %s does not match pret's %s" % (game, rev, sha_file))
    folders = {}
    for meta in glob.glob(os.path.join(rel, "v*.x", "v*", ".release.json")) + glob.glob(os.path.join(rel, "v*.x", ".release.json")):
        folders[json.load(open(meta))["version"]] = os.path.dirname(meta)
    out, missing = [], []
    for v in sorted(set(folders) | set(kept), key=vt):
        if vt(v) < PATCHES_FROM or v not in published:
            continue
        folder = folders.get(v)
        files = [os.path.join(folder, "PATCHES", p[3]) for p in PATCH_SOURCES] if folder else []
        if not files or not all(os.path.exists(f) for f in files):
            if v in kept:
                out.append(kept[v])
            else:
                missing.append(v)
            continue
        notes_path = os.path.join(folder, "RELEASE_NOTES.md")
        if not os.path.exists(notes_path):          # a sealed group: its notes are one PDF now, its row already written
            if v in kept:
                out.append(kept[v])
            else:
                missing.append(v)
            continue
        targets = dict(re.findall(r"^\| `(daemonsCon\w+\.gba)` \| \w+ \| `([0-9a-f]{40})` \|", open(notes_path, encoding="utf-8").read(), re.M))
        meta = json.load(open(os.path.join(folder, ".release.json")))
        patches = []
        for (ed, game, rev, name, sha_file), f in zip(PATCH_SOURCES, files):
            data = open(f, "rb").read()
            crc_src, crc_tgt, crc_patch = struct.unpack("<III", data[-12:])
            if zlib.crc32(data[:-4]) != crc_patch:
                raise SystemExit("  refused: %s's own CRC is wrong" % f)
            src = retail[(game, rev)]
            if "%08X" % crc_src != src["crc32"]:
                raise SystemExit("  refused: %s is made for CRC32 %08X, not %s %s's %s" % (f, crc_src, game, rev, src["crc32"]))
            target = targets["daemonsContent.gba" if ed == "CONTENT" else "daemonsContext.gba"]
            #  where pret's byte-identical retail builds are cached (romrelease.py), apply the patch and prove the
            #  notes' SHA-1 is what it makes -- a ROM left in the folder can have been replaced by hand
            cached = os.path.join(os.path.expanduser("~"), ".cache/daemons/pokefirered-upstream",
                                  open(os.path.join(GBA, sha_file)).read().split()[1])
            if os.path.exists(cached):
                import bps
                if hashlib.sha1(bps.apply(open(cached, "rb").read(), data)).hexdigest() != target:
                    raise SystemExit("  refused: %s does not make the ROM %s's notes name" % (name, v))
            asset = name.replace(" ", ".")
            patches.append({
                "edition": ed, "file": asset,
                "source": {"game": game, "region": src["region"], "revision": rev,
                           "name": "Pokemon %s (%s) %s" % (game, src["region"], rev),
                           "sha1": src["sha1"], "crc32": src["crc32"], "md5": src["md5"]},
                "target": {"sha1": target, "crc32": "%08X" % crc_tgt},
                "patch": {"size": len(data), "sha1": hashlib.sha1(data).hexdigest(),
                          "sha256": hashlib.sha256(data).hexdigest()},
                "url": "https://github.com/%s/releases/download/v%s/%s" % (GH_REPO, v, asset)})
        out.append({"version": v, "tag": "v" + v, "bible": meta["bible"], "engine": meta["engine"],
                    "made": meta["made"], "page": "https://github.com/%s/releases/tag/v%s" % (GH_REPO, v),
                    "patches": patches})
    if missing:
        print("  !! published but no patches on this machine to describe: " + ", ".join(missing))
    out.sort(key=lambda r: vt(r["version"]), reverse=True)
    return {"_about": "T-453 (C-186): DAEMONS' BPS patches, newest first, as published on GitHub (the assets of each "
                      "release on %s). Nothing of Nintendo's is here: the app fetches url, checks patch.sha1 (or "
                      "sha256, which GitHub also reports), checks the player's own ROM against source (sha1, or crc32 "
                      "as a BPS patcher does; md5 for tools that show only that), applies the patch, and checks the "
                      "result against target.sha1. A patch fits only its own source revision; 1.0 and Rev 1 are both "
                      "common. CONTENT is FireRed's edition, CONTEXT LeafGreen's. latest is the newest version." % GH_REPO,
            "repo": GH_REPO, "latest": out[0]["version"] if out else None, "releases": out}


#  ---------------------------------------------------------------------------------------------------------------------
#  T-453: THE PLANNER's data, in the iOS lane's order -- (1) the story's steps, where each happens and in what order;
#  (2) how the maps join; (3) what is wild on each; (4) who fights on each; (5) the level curve along the story. Every
#  record carries `step`: how many of the story's steps are DONE before it is reachable, so the app shows a record once
#  the save has done that many and hides the rest. Five files, so the app loads a tab's data and not the whole planner.
#
#  THE STEPS are the CHECKPOINT attendant's (T-347): docs/attendant_dreams.json, in the AI harness's own order
#  (engineAi/server/progress_steps.json, less its `_skip`), each done by the flag tools/gbadreams.py reads it by -- so the
#  planner, the attendant and the playtester agree on what comes next. The GUIDE and the first UNDERSTANDING are not
#  steps there, and are not here: a hidden find and an arrived-at understanding are never pointed at.
#
#  WHERE: the script that sets a step's flag, followed up through whatever calls it to the person, trigger or sign in
#  map.json that runs it; a flag that hides a person or an item (FLAG_HIDE_*) is that object's own spot; a flag set on
#  arriving (FLAG_WORLD_MAP_*) is the map. Where two maps set it, the one the step's SECOND dream names wins.
#
#  REACHABLE: map.json's connections and warps, every `warp` a map's own script makes, and the ferry, joined both ways;
#  a walk from the player's room where a map or a join behind a gate (PLANNER_GATES) opens once its step is done. The
#  walk is a map's, not a tile's: it knows no ledge, and where a map is cut in two (ROUTE 12's sleeper) the gate is on
#  the join. The tool refuses if a step's own place would open after the step.

PLANNER_START = "MAP_PALLET_TOWN_PLAYERS_HOUSE_2F"      # new_game.c, WarpToPlayersRoom
#  Never in the planner: a grove, THE NEXUS, BREATHVERSE (found blind, T-297/T-337/T-408), ARTSAI's station, and the two
#  far islands the SCHOLAR's house and the ticket reach (when in doubt). Their maps, the ways into them and everything
#  in them are left out.
PLANNER_HIDDEN = re.compile(r"_Grove$|^Nexus$|^Breathverse$|^Route21_North_Station$|^BirthIsland_|^NavelRock_")
#  DOLDRUM CAVE: its place on the map after the REVIEW BOARD, nothing of what is in it (T-251: its second gate is seen).
PLANNER_QUIET = re.compile(r"^CeruleanCave_")
#  (a map id, a prefix ending in *, or "A|B" the join between two maps; the step that must be DONE; what stands there)
PLANNER_GATES = [
    ("MAP_ROUTE2", "get_pokedex", "the old man across CALLOW's north road until the parcel is home"),
    ("MAP_ROUTE2|MAP_DIGLETTS_CAVE_NORTH_ENTRANCE", "ss_anne", "a tree only PRUNE clears (DRIVER01)"),
    ("MAP_ROUTE3", "boulder_badge", "SLATE's east road is held until CAIRN's MARK"),
    ("MAP_ROUTE9", "ss_anne", "a tree only PRUNE clears (DRIVER01)"),
    ("MAP_VERMILION_CITY_GYM", "ss_anne", "a tree only PRUNE clears (DRIVER01)"),
    ("MAP_ROUTE11|MAP_ROUTE12", "pokemon_tower", "the sleeper across ROUTE 12, woken by the INTERRUPT"),
    ("MAP_ROUTE12|MAP_ROUTE13", "pokemon_tower", "the sleeper across ROUTE 12, woken by the INTERRUPT"),
    ("MAP_ROUTE16", "pokemon_tower", "the sleeper across ROUTE 16, woken by the INTERRUPT"),
    ("MAP_POKEMON_TOWER_7F", "rocket_hideout", "the RESOLVER, to see what haunts the stair"),
    ("MAP_SAFFRON_CITY*", "rainbow_badge", "BRAZEN's gate guards, until they have TEA"),
    ("MAP_SAFFRON_CITY_GYM", "silph_co", "CORPUS at the BENCHMARK's door until FOUNDRY CO. is free"),
    ("MAP_ROUTE19", "safari_zone", "water (DRIVER03)"), ("MAP_ROUTE20", "safari_zone", "water (DRIVER03)"),
    ("MAP_ROUTE21_*", "safari_zone", "water (DRIVER03)"), ("MAP_SEAFOAM_ISLANDS_*", "safari_zone", "water (DRIVER03)"),
    ("MAP_CINNABAR_ISLAND*", "safari_zone", "water (DRIVER03)"), ("MAP_POKEMON_MANSION_*", "safari_zone", "water (DRIVER03)"),
    ("MAP_POWER_PLANT", "safari_zone", "water (DRIVER03)"),
    ("MAP_CINNABAR_ISLAND_GYM", "pokemon_mansion", "the SECRET KEY from the MANSION's cellar"),
    ("MAP_VIRIDIAN_CITY_GYM", "volcano_badge", "CALLOW's BENCHMARK opens to seven MARKS"),
    ("MAP_ROUTE23", "earth_badge", "a gate for every MARK"), ("MAP_VICTORY_ROAD_*", "earth_badge", "a gate for every MARK"),
    ("MAP_INDIGO_PLATEAU_*", "earth_badge", "a gate for every MARK"),
    ("MAP_CERULEAN_CAVE_*", "champion", "the guard lets only the champion in"),
    ("MAP_ONE_ISLAND*", "volcano_badge", "the ferry, once QUICKSILVER's MARK is held"),
    ("MAP_TWO_ISLAND*", "volcano_badge", "the ferry"), ("MAP_THREE_ISLAND*", "volcano_badge", "the ferry"),
    ("MAP_FOUR_ISLAND*", "champion", "the ferry's later pass"), ("MAP_FIVE_ISLAND*", "champion", "the ferry's later pass"),
    ("MAP_SIX_ISLAND*", "champion", "the ferry's later pass"), ("MAP_SEVEN_ISLAND*", "champion", "the ferry's later pass"),
]
#  The ferry (data/scripts/seagallop.inc) is a menu, not a warp a map names: it joins VERMILION and QUICKSILVER to each
#  island's harbor. The ticket islands (NAVEL ROCK, BIRTH ISLAND) are not on it here.
PLANNER_FERRY_FROM = ["MAP_VERMILION_CITY", "MAP_CINNABAR_ISLAND"]
PLANNER_FERRY_TO = ["MAP_%s_ISLAND_HARBOR" % n for n in ("ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN")]
#  Where a step is worked for, when its flag is set somewhere else: the S.S. ANNE is left once its captain has given
#  DRIVER01, and the planner points at the captain, not the pier.
PLANNER_SPOT_FLAG = {"ss_anne": "FLAG_GOT_HM01"}
#  The harness's labels, less the four that are still vanilla's words
PLANNER_LABELS = {"ss_anne": "S.S. ANNE", "safari_zone": "SAFARI ZONE", "silph_co": "FOUNDRY CO.", "champion": "CHAMPION"}
#  T-407's season, hour and weather homes (wild_shifts.h): left out until the user says they are not found by playing
PLANNER_SHIFTS = False
PLANNER_AREAS = [["north-west", "north", "north-east"], ["west", "centre", "east"], ["south-west", "south", "south-east"]]


def _planner_steps():
    """[(id, label, flag)] in the harness's order, the attendant's `_skip` left out (tools/gbadreams.py's flags)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gbadreams
    words = json.load(open(os.path.join(ROOT, "docs", "attendant_dreams.json"), encoding="utf-8"))
    harness = json.load(open(gbadreams.STEPS, encoding="utf-8"))
    out = []
    for s in harness:
        if s["id"] in words["_skip"]:
            continue
        if s["id"] not in words["steps"]:
            raise SystemExit("  refused: the harness's step %s has no dream (tools/gbadreams.py)" % s["id"])
        flag = gbadreams.flag_for(s)
        if not flag:
            raise SystemExit("  refused: no flag for the step %s" % s["id"])
        second = " ".join(" ".join(box) for box in words["steps"][s["id"]]["second"])
        out.append((s["id"], PLANNER_LABELS.get(s["id"], s["label"]), flag, second))
    return out


class _PlannerWorld:
    """every map's map.json, scripts and layout size, by its MAP_ id"""
    def __init__(self):
        lay = {l["id"]: l for l in json.loads(read("data/layouts/layouts.json"))["layouts"] if "id" in l}
        self.maps, self.dir = {}, {}
        for d in sorted(os.listdir(os.path.join(GBA, "data/maps"))):
            p = os.path.join(GBA, "data/maps", d, "map.json")
            if not os.path.exists(p):
                continue
            m = json.load(open(p, encoding="utf-8"))
            l = lay.get(m.get("layout"), {})
            m["_w"], m["_h"] = l.get("width", 0), l.get("height", 0)
            sp = os.path.join(GBA, "data/maps", d, "scripts.inc")
            m["_scripts"] = open(sp, encoding="utf-8").read() if os.path.exists(sp) else ""
            self.maps[m["id"]], self.dir[m["id"]] = m, d
        #  the link rooms (trading, battling, the UNION ROOM) sit upstairs in every CHECKPOINT: not a way across the world
        self.link = set(json.loads(read("data/maps/map_groups.json"))["gMapGroup_Link"])

    def hidden(self, mid):
        return mid not in self.maps or self.dir[mid] in self.link or bool(PLANNER_HIDDEN.search(self.dir[mid]))

    def quiet(self, mid):
        return bool(PLANNER_QUIET.search(self.dir[mid]))

    @staticmethod
    def blocks(text):
        """{label: its lines up to the next label}"""
        out, cur = {}, None
        for line in text.split("\n"):
            m = re.match(r"^(\w+)::?\s*$", line)
            if m:
                cur = m.group(1); out[cur] = ""
            elif cur:
                out[cur] += line + "\n"
        return out

    def spot(self, mid, needle):
        """(kind, x, y) of the person, trigger or sign whose script reaches a line matching NEEDLE, followed up through
        every label that names the one below it; ("arrival", None, None) for a map script; None if nothing does."""
        m = self.maps[mid]
        blocks = self.blocks(m["_scripts"])
        events, self.event = {}, None
        for kind, key in (("person", "object_events"), ("trigger", "coord_events"), ("sign", "bg_events")):
            for e in m.get(key) or []:
                if e.get("script") and e["script"] not in events:
                    events[e["script"]] = (kind, e["x"], e["y"], e)
        frontier = [l for l, b in blocks.items() if re.search(needle, b)]
        seen = set(frontier)
        for _ in range(8):
            for l in frontier:
                if l in events:
                    self.event = events[l][3]          # the event itself, for a trigger's var
                    return events[l][:3]
            nxt = []
            for l in frontier:
                for k, b in blocks.items():
                    if k not in seen and re.search(r"\b%s\b" % re.escape(l), b):
                        seen.add(k); nxt.append(k)
                if re.search(r"map_script\w*\s+MAP_SCRIPT_\w+,\s*%s\b|map_script_2\s+\w+,\s*\w+,\s*%s\b" % (l, l), m["_scripts"]):
                    return ("arrival", None, None)
            frontier = nxt
            if not frontier:
                break
        return None

    def area(self, mid, x, y):
        m = self.maps[mid]
        if x is None or not m["_w"] or not m["_h"]:
            return None
        return PLANNER_AREAS[min(2, y * 3 // m["_h"])][min(2, x * 3 // m["_w"])]

    def joins(self):
        """{(a, b)} both ways, hidden maps left out: connections, warps, scripts' own warps and the ferry"""
        out = set()
        for mid, m in self.maps.items():
            to = [c["map"] for c in m.get("connections") or []]
            to += [w["dest_map"] for w in m.get("warp_events") or []]
            to += re.findall(r"^\s*warp\w*\s+(MAP_\w+)", m["_scripts"], re.M)
            for t in to:
                if t != mid and not self.hidden(mid) and not self.hidden(t):
                    out |= {(mid, t), (t, mid)}
        for a in PLANNER_FERRY_FROM:
            for b in PLANNER_FERRY_TO:
                out |= {(a, b), (b, a)}
        return out


def _planner_reach(W, order):
    """{map: the fewest steps done before the walk from PLANNER_START reaches it}, through PLANNER_GATES"""
    import heapq
    idx = {sid: k for k, sid in enumerate(order)}
    map_gate, join_gate = {}, {}
    for what, sid, _ in PLANNER_GATES:
        if sid not in idx:
            raise SystemExit("  refused: PLANNER_GATES names a step the harness has not: %s" % sid)
        need = idx[sid] + 1
        if "|" in what:
            a, b = what.split("|")
            for k in ((a, b), (b, a)):
                join_gate[k] = max(join_gate.get(k, 0), need)
            continue
        hits = [m for m in W.maps if (m.startswith(what[:-1]) if what.endswith("*") else m == what)]
        if not hits:
            raise SystemExit("  refused: PLANNER_GATES names no map: %s" % what)
        for m in hits:
            map_gate[m] = max(map_gate.get(m, 0), need)
    adj = {}
    for a, b in W.joins():
        adj.setdefault(a, set()).add(b)
    best, heap = {PLANNER_START: 0}, [(0, PLANNER_START)]
    while heap:
        k, m = heapq.heappop(heap)
        if k > best.get(m, 99):
            continue
        for n in adj.get(m, ()):
            s = max(k, join_gate.get((m, n), 0), map_gate.get(n, 0))
            if s < best.get(n, 99):
                best[n] = s
                heapq.heappush(heap, (s, n))
    return best


def _planner_place(W, names, mid):
    return names.get(W.maps[mid].get("region_map_section", ""), "")


def planner_tables(species):
    """T-453: the planner's five files -- {name: table}"""
    W = _PlannerWorld()
    names = _section_names()
    steps = _planner_steps()
    order = [s[0] for s in steps]
    reach = _planner_reach(W, order)
    byconst = {v["constant"]: (int(k), v["name"]) for k, v in species.items() if isinstance(v, dict) and v.get("constant")}
    def mon(const):
        c = const.replace("SPECIES_", "")
        if c not in byconst:
            raise SystemExit("  refused: %s is in no species.json row" % const)
        return {"species": byconst[c][0], "name": byconst[c][1]}
    def where(mid, spot):
        kind, x, y = spot or (None, None, None)
        return {"map": W.dir[mid], "place": _planner_place(W, names, mid), "spot": kind,
                "x": x, "y": y, "area": W.area(mid, x, y)}
    flags = flag_values([s[2] for s in steps])
    shown = {m for m in reach if not W.hidden(m)}

    #  (1) the story's steps
    story = []
    for k, (sid, label, flag, second) in enumerate(steps):
        want = PLANNER_SPOT_FLAG.get(sid, flag)
        cands = []
        wm = re.match(r"FLAG_WORLD_MAP_(\w+)$", want)
        if wm and "MAP_" + wm.group(1) in W.maps:
            cands = [("MAP_" + wm.group(1), ("arrival", None, None))]
        if not cands:
            for mid in W.maps:
                if mid in shown and re.search(r"^\s*setflag\s+%s\b" % want, W.maps[mid]["_scripts"], re.M):
                    cands.append((mid, W.spot(mid, r"setflag\s+%s\b" % want)))
        if not cands:
            for mid, m in W.maps.items():
                for o in m.get("object_events") or []:
                    if mid in shown and o.get("flag") == want and want.startswith("FLAG_HIDE_"):
                        cands.append((mid, ("person", o["x"], o["y"])))
        if not cands:       # set in a shared script (data/scripts/, the DEBUG's left out): the maps that call it
            shared = W.blocks("".join(open(os.path.join(GBA, "data/scripts", f), encoding="utf-8").read()
                                      for f in sorted(os.listdir(os.path.join(GBA, "data/scripts")))
                                      if f.endswith(".inc") and "debug" not in f))
            chain = {l for l, b in shared.items() if re.search(r"^\s*setflag\s+%s\b" % want, b, re.M)}
            for _ in range(6):
                chain |= {l for l, b in shared.items() if any(re.search(r"\b%s\b" % c, b) for c in chain)}
            needle = r"\b(%s)\b" % "|".join(sorted(chain)) if chain else None
            for mid in W.maps:
                if needle and mid in shown and re.search(needle, W.maps[mid]["_scripts"]):
                    cands.append((mid, W.spot(mid, needle)))
        if not cands:
            raise SystemExit("  refused: nothing on any map sets %s (the step %s)" % (want, sid))
        cands.sort(key=lambda c: (_planner_place(W, names, c[0]).split(" ")[0] not in second, c[1] is None))
        mid, spot = cands[0]
        if reach.get(mid, 99) > k:
            raise SystemExit("  refused: the step %s (%d) happens in %s, which the walk opens only after %s steps -- "
                             "PLANNER_GATES disagrees with the story's order" % (sid, k, W.dir[mid], reach.get(mid)))
        row = {"step": k, "id": sid, "label": label, "done_flag": flags[flag], "done_flag_name": flag}
        if sid in PLANNER_LABELS:
            row["draft"] = True                         # the planner's own word for it, not the harness's
        row.update(where(mid, spot))
        story.append(row)

    #  (2) the maps and how they join
    maps, joins = {}, {}
    for a, b in sorted(W.joins()):
        if a in shown and b in shown:
            joins.setdefault(a, set()).add(b)
    gates = {}
    for what, sid, why in PLANNER_GATES:
        gates.setdefault(what, (order.index(sid) + 1, why))
    for mid in sorted(shown, key=lambda m: (reach[m], W.dir[m])):
        m = W.maps[mid]
        gate = max(((v[0], what, v) for what, v in gates.items() if "|" not in what and
                    (mid.startswith(what[:-1]) if what.endswith("*") else mid == what)), default=None)
        gate = gate and gate[1:]                    # the gate that holds it longest
        maps[W.dir[mid]] = {"id": mid, "place": _planner_place(W, names, mid), "section": m.get("region_map_section"),
                            "type": m.get("map_type", "").replace("MAP_TYPE_", "").lower(), "width": m["_w"],
                            "height": m["_h"], "step": reach[mid],
                            "edges": {c["direction"]: W.dir[c["map"]] for c in m.get("connections") or []
                                      if c["map"] in shown},
                            "joins": sorted(W.dir[n] for n in joins.get(mid, ()))}
        if gate:
            maps[W.dir[mid]]["gate"] = gate[1][1]
            maps[W.dir[mid]]["draft"] = True            # the gate's reason is the planner's wording
    join_gates = [{"between": [W.dir[a] for a in what.split("|")], "step": order.index(sid) + 1, "why": why, "draft": True}
                  for what, sid, why in PLANNER_GATES if "|" in what]

    #  (3) what is wild
    enc = json.loads(read("src/data/wild_encounters.json"))["wild_encounter_groups"][0]
    rates = {f["type"]: f["encounter_rates"] for f in enc["fields"]}
    rods = next(f for f in enc["fields"] if f["type"] == "fishing_mons")["groups"]
    def table(field, mons, idx):
        got = {}
        for i in idx:
            r, sm = rates[field][i], mons[i]
            k = sm["species"]
            g = got.setdefault(k, dict(mon(k), min=sm["min_level"], max=sm["max_level"], rate=0))
            g["min"], g["max"], g["rate"] = min(g["min"], sm["min_level"]), max(g["max"], sm["max_level"]), g["rate"] + r
        return sorted(got.values(), key=lambda g: -g["rate"])
    def header(h):
        out = {}
        for field, key in (("land_mons", "land"), ("water_mons", "water"), ("rock_smash_mons", "rock_smash")):
            if field in h:
                out[key] = {"rate": h[field]["encounter_rate"],
                            "mons": table(field, h[field]["mons"], range(len(h[field]["mons"])))}
        if "fishing_mons" in h:
            out["fishing"] = {"rate": h["fishing_mons"]["encounter_rate"],
                              **{rod: table("fishing_mons", h["fishing_mons"]["mons"], ix) for rod, ix in rods.items()}}
        return out
    wild = {}
    for h in enc["encounters"]:
        mid = h["map"]
        if mid not in shown or W.quiet(mid):
            continue
        ed = "CONTENT" if "_FireRed" in h["base_label"] else "CONTEXT" if "_LeafGreen" in h["base_label"] else None
        if not ed:
            raise SystemExit("  refused: %s is neither edition's" % h["base_label"])
        rec = wild.setdefault(W.dir[mid], {"place": _planner_place(W, names, mid), "step": reach[mid]})
        slot = rec.setdefault(ed, {})
        when = "night" if h["base_label"].endswith("_Night") else "day" if "day" not in slot else None
        if when:
            slot[when] = header(h)
        else:
            slot.setdefault("other", []).append(header(h))      # SIX ISLAND's ALTERING CAVE: its other tables
    if PLANNER_SHIFTS:
        raise SystemExit("  refused: PLANNER_SHIFTS is not built yet")

    #  (4) who fights
    tsrc, psrc = read("src/data/trainers.h"), read("src/data/trainer_parties.h")
    tnum = {n: int(v) for n, v in re.findall(r"#define (TRAINER_\w+)\s+(\d+)\b", read("include/constants/opponents.h"))}
    classes = dict(re.findall(r"\[(TRAINER_CLASS_\w+)\]\s*=\s*_\(\"([^\"]*)\"\)", read("src/data/text/trainer_class_names.h")))
    tinfo = {t: b for t, b in re.findall(r"\[(TRAINER_\w+)\]\s*=\s*\{(.*?)\n    \},", tsrc, re.S)}
    parties = {m.group(1): m.group(2) for m in (re.match(r"\w+ (sParty_\w+)\[\]\s*=\s*\{(.*)", c, re.S)
                                                for c in psrc.split("static const struct TrainerMon")[1:]) if m}
    start = flag_values(["TRAINER_FLAGS_START"])["TRAINER_FLAGS_START"]
    trainers, seen = [], set()
    for mid in sorted(shown, key=lambda m: (reach[m], W.dir[m])):
        if W.quiet(mid):
            continue
        for t in dict.fromkeys(re.findall(r"^\s*trainerbattle\w*\s+(TRAINER_\w+)", W.maps[mid]["_scripts"], re.M)):
            if (mid, t) in seen or t not in tinfo:
                continue
            seen.add((mid, t))
            b = tinfo[t]
            cls = re.search(r"\.trainerClass\s*=\s*(\w+)", b).group(1)
            party = parties[re.search(r"\.party\s*=\s*\w+\((sParty_\w+)\)", b).group(1)]
            row = {"trainer": t, "number": tnum[t], "flag": start + tnum[t], "class": classes.get(cls, ""),
                   "name": gba_string(re.search(r"\.trainerName\s*=\s*_\((.*?)\)", b).group(1)),
                   "double": "TRUE" in (re.search(r"\.doubleBattle\s*=\s*(\w+)", b) or ["", ""])[1],
                   "party": [dict(mon(sp), level=int(lv)) for lv, sp in
                             re.findall(r"\.lvl\s*=\s*(\d+),.*?\.species\s*=\s*(SPECIES_\w+)", party, re.S)],
                   "boss": cls in ("TRAINER_CLASS_LEADER", "TRAINER_CLASS_BOSS", "TRAINER_CLASS_ELITE_FOUR",
                                   "TRAINER_CLASS_CHAMPION", "TRAINER_CLASS_RIVAL_EARLY", "TRAINER_CLASS_RIVAL_LATE")}
            rv = re.search(r"_(SQUIRTLE|BULBASAUR|CHARMANDER)$", t)
            if cls.startswith("TRAINER_CLASS_RIVAL") or cls == "TRAINER_CLASS_CHAMPION":
                row["rival"], row["name"] = True, None          # the save's own name for the rival
                if rv:
                    row["rival_starter"] = mon("SPECIES_" + rv.group(1))["name"]
            spot = W.spot(mid, r"trainerbattle\w*\s+%s\b" % t)
            row.update(where(mid, spot))
            row["step"] = reach[mid]
            #  a trigger that waits on a scene var fires once some map's script sets it: no sooner than that map opens
            #  (ROUTE 22's second rival waits on CALLOW's BENCHMARK)
            if spot and spot[0] == "trigger":
                for e in [W.event]:
                    if e.get("var", "0") != "0" and not e["var"].startswith("VAR_TEMP"):
                        setters = [reach[o] for o in shown if re.search(r"^\s*setvar\s+%s,\s*%s\b" % (e["var"], e["var_value"]),
                                                                        W.maps[o]["_scripts"], re.M)]
                        if setters:
                            row["step"] = max(row["step"], min(setters))
            if re.search(r"_REMATCH_|^TRAINER_ELITE_FOUR_\w+_2$", t):      # a second round: after the story
                row["step"], row["rematch"] = len(steps), True
            trainers.append(row)

    #  (5) the level curve: for each count of steps done, what that count newly opens, and the fights in it
    curve = []
    for k in range(len(steps) + 1):
        lv_wild = [(g["min"], g["max"]) for w in wild.values() if w["step"] == k for ed in ("CONTENT", "CONTEXT")
                   for h in (w.get(ed, {}).get("day"), w.get(ed, {}).get("night")) if h and "land" in h
                   for g in h["land"]["mons"]]
        lv_tr = [p["level"] for t in trainers if t["step"] == k for p in t["party"]]
        bosses = [{"name": t["name"], "class": t["class"], "map": t["map"], "max": max(p["level"] for p in t["party"]),
                   **({"rival_starter": t["rival_starter"]} if "rival_starter" in t else {})}
                  for t in trainers if t["step"] == k and t["boss"] and t["party"]]
        curve.append({"step": k, "next": steps[k][1] if k < len(steps) else None,
                      **({"draft": True} if k < len(steps) and steps[k][0] in PLANNER_LABELS else {}),
                      "opens": sorted(m for m, v in maps.items() if v["step"] == k),
                      "wild": [min(a for a, _ in lv_wild), max(b for _, b in lv_wild)] if lv_wild else None,
                      "trainers": [min(lv_tr), max(lv_tr)] if lv_tr else None, "bosses": bosses})

    about = ("T-453: the planner. step on every record = how many of the story's steps are done before it is "
             "reachable; show a record when the save has done at least that many (count the done_flag of each step "
             "in planner_story.json, bits as profile_layout explains). ")
    #  (said without naming them: the companion is public, and a list of what is hidden is a map to it)
    #  T-453 (the user, 2026-10-27): the planner's own words -- a gate's reason, a step label it renamed -- are DRAFT
    draft = ("DRAFT: a record with draft: true carries the planner's own wording (a gate's reason, a renamed step "
             "label), which awaits the user's approval.")
    left_out = ("Left out on purpose: every place the game means to be found by playing, the islands only a ticket "
                "reaches, what lives in DOLDRUM CAVE, hidden items, fixed encounters, the GUIDE and the "
                "UNDERSTANDINGS, the NOTEBOOK and its books, and any line of the game's text.")
    return {
        "planner_story.json": {"_draft": draft, "_about": about + "Steps are the CHECKPOINT attendant's (T-347), the AI harness's own "
                               "order; spot is the person, trigger or sign that does it (arrival: on arriving), area "
                               "a ninth of the map. " + left_out, "steps": story},
        "planner_maps.json": {"_draft": draft, "_about": about + "Each map (by its folder, as maps.json names it) with its place, its "
                              "type, its size in tiles, its edges (the maps beside it) and joins (every map a warp, "
                              "edge, script or the ferry leads to, both ways); gate says what holds it until step. "
                              "join_gates hold the way between two maps instead. " + left_out,
                              "start": W.dir[PLANNER_START], "join_gates": join_gates, "maps": maps},
        "planner_wild.json": {"_about": about + "Each map's wild tables by edition (CONTENT, CONTEXT): day, and night "
                              "where the map has one (T-268); land, water, rock_smash and fishing (old_rod, good_rod, "
                              "super_rod), each daemon's slots summed into one rate (percent of that table) with its "
                              "level range. The season, hour and weather homes (T-407, T-415) are not here. " + left_out,
                              "maps": wild},
        "planner_trainers.json": {"_about": about + "Every trainer a map's scripts battle, with our class and name, "
                                  "party (species and level), and flag (set once beaten; bits as profile_layout "
                                  "explains). A rival battle is three rows, one per starter the rival may hold "
                                  "(rival_starter); its name is the save's. boss marks leaders, rivals, the REVIEW "
                                  "BOARD, the champion and CORPUS's boss; rematch, a second round after the story. " + left_out, "trainers": trainers},
        "planner_curve.json": {"_draft": draft, "_about": about + "One row per count of steps done: next (the step ahead), the maps "
                               "that count opens, the level ranges on them -- wild is the land tables (grass and "
                               "caves; water and rods are in planner_wild.json), trainers every party -- and the boss "
                               "fights that count opens (each one's highest level). A rematch is after the story.",
                               "curve": curve},
    }


def main():
    files = {"species.json": species_table(), "charmap.json": charmap_table(), "week.json": week_table(),
             "seasons.json": seasons_table(), "streaks.json": streaks_table(), "moves.json": moves_table(),
             "profile_layout.json": profile_layout(), "maps.json": maps_table(), "margins.json": margins_table(),
             "items.json": items_table(), "routines.json": routines_table(), "notebook.json": notebook_table(),
             "marks.json": marks_table(), "regions.json": regions_table(),     # C-126, C-127
             "events.json": events_table(), "school.json": school_table(),
             "groves.json": groves_table(),                                     # T-408       # C-128, C-129
             "guide.json": guide_table(),                                       # the reading tab
             "subtle.json": subtle_table(),                                     # T-423: the LIBRARY's second book
             "hermetic.json": hermetic_table(),                                 # T-483 / C-238: the LIBRARY's third book
             "holidays.json": holidays_table(),                                 # T-416 / C-149
             "play.json": play_table()}                                         # T-426
    #  T-453; the GUIDE's chapters as guide.json has them (gensubtle, imported since, reuses genguide's parser)
    files["index_cards.json"] = index_cards_table(files["species.json"], files["margins.json"],
                                                  files["marks.json"], files["guide.json"])
    for u in files["marks.json"]["understandings"]:
        u.pop("_flag_name")     # used above to join the tables; its name says where, and the companion is public
    files["patches.json"] = patches_table()                                     # T-453
    files.update(planner_tables(files["species.json"]))                         # T-453: the planner
    layout = save_layout()
    if layout:
        files["save_layout.json"] = layout
    else:
        print("  no build to read the save layout from (make firered leafgreen first); save_layout.json left as it is")
    changed = []
    for name, data in files.items():
        text = data if isinstance(data, str) else json.dumps(data, indent=1, ensure_ascii=False) + "\n"
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
    art.update(play_art())                                             # T-426
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
    #  The cover is RGB, not a palette with a clear index 0: written on its own, nothing made transparent.
    buf = io.BytesIO()
    guide_cover().save(buf, "PNG", optimize=True)
    path = os.path.join(art_dir, "guide_cover.png")
    if not os.path.exists(path) or open(path, "rb").read() != buf.getvalue():
        art_changed += 1
        if WRITE:
            os.makedirs(art_dir, exist_ok=True)
            open(path, "wb").write(buf.getvalue())
    #  T-423: THE SUBTLE LAYER's pictures and cover, RGB like the GUIDE's cover (the page colour is part of the picture).
    import gensubtle
    subtle = gensubtle.subtle_images()
    for name, im in subtle.items():
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        path = os.path.join(art_dir, name)
        if not os.path.exists(path) or open(path, "rb").read() != buf.getvalue():
            art_changed += 1
            if WRITE:
                os.makedirs(art_dir, exist_ok=True)
                open(path, "wb").write(buf.getvalue())
    if art_changed:
        changed.append("art/ (%d of %d)" % (art_changed, len(art) + 1 + len(subtle)))
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

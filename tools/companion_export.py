#!/usr/bin/env python3
"""C-03 (daemons-companion): one export of what the goal companion needs to know about DAEMONS, so nothing is typed
twice.

    python3 tools/companion_export.py            # report: what would change in companion/server/data/
    python3 tools/companion_export.py --write    # write it

Writes three files into the companion repo (symlinked here as companion/, setup.sh step 5):

  species.json  every species the save can hold, keyed by the game's INTERNAL species id (what a save stores), with
                its national INDEX number, our name, our types, the INDEX category, both editions' entries (CONTENT is
                FireRed's pokedex_text_fr.h, CONTEXT LeafGreen's pokedex_text_lg.h), and its art in gfx/daemons/
  charmap.json  the game's text encoding, byte -> character, for reading nicknames and names out of a save
  week.json     the week as the game keeps it: Sunday first, each day's colour (day_trims.h, the CHECKPOINT's trim)
                and its note, C to B (vision 9.21)
  seasons.json  the seasons by edition (C-14), from tools/seasons.py -- the one definition the game shares
  save_layout.json  the save's sectors, sizes and offsets, read from the built game (C-02)

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


def species_table():
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define SPECIES_(\w+)\s+(\d+)\b", read("include/constants/species.h"))}
    dex = re.findall(r"NATIONAL_DEX_(\w+)\s*,", read("include/constants/pokedex.h"))
    national = {name: i for i, name in enumerate(dex)}                       # NATIONAL_DEX_NONE is 0
    to_nat = set(re.findall(r"SPECIES_TO_NATIONAL\((\w+)\)", read("src/pokemon.c")))   # every species the INDEX numbers
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

    out = {}
    for sp, sid in sorted(ids.items(), key=lambda kv: kv[1]):
        if sp not in to_nat or sp not in names:
            continue
        nat = national.get(sp)
        stem = re.sub(r"[^a-z0-9_]", "", names[sp].lower().replace(" ", "_"))   # LEMMA MIND -> lemma_mind
        sym = desc.get(sp)
        row = {
            "constant": sp,
            "national": nat,
            "name": names[sp],
            "types": types.get(sp, []),
            "category": cat.get(sp),
            "entry": {ed: texts[ed].get(sym) for ed in ("CONTENT", "CONTEXT")},
            "art": {view: ("gfx/daemons/%s_%s.png" % (stem, view)) if ("%s_%s.png" % (stem, view)) in art else None
                    for view in ("front", "back")},
            "bodyType": body.get(sp),                  # C-18: the type its palette ramp was built from
            "streaks": sp in streaky,                  # C-18: palette 11..14 carry its four routines' streaks
        }
        out[str(sid)] = row
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


#  RoverRadio's day table (the user's own design, CodeMusic/RoverByte RoverCodeBase: PrefrontalCortex/ProtoPerceptions.cpp
#  DAY_COLORS, AuditoryCortex/PitchPerception.cpp, VisualCortex/RoverViewManager.cpp CHAKRA_DATA and VIRTUE_DATA --
#  four arrays, Sunday first, read across; companion docs/INHERITANCE.md). The game's own week agrees on the rainbow
#  and the notes; the chakra and the virtue are RoverRadio's, and the game does not pair days with virtues.
ROVERRADIO_DAYS = [
    ("red", "Root", "Chastity cures Lust"),
    ("orange", "Sacral", "Temperance cures Gluttony"),
    ("yellow", "Solar Plexus", "Charity cures Greed"),
    ("green", "Heart", "Diligence cures Sloth"),
    ("blue", "Throat", "Forgiveness cures Wrath"),
    ("indigo", "Third Eye", "Kindness cures Envy"),
    ("violet", "Crown", "Humility cures Pride"),
]


def week_table():
    trims = re.findall(r"RGB\((\d+),\s*(\d+),\s*(\d+)\),\s*//\s*(\w+),\s*([A-G])", read("src/data/day_trims.h"))
    days = []
    for r, g, b, day, note in trims:
        hexc = "#%02X%02X%02X" % tuple(int(v) * 255 // 31 for v in (r, g, b))
        hue, chakra, virtue = ROVERRADIO_DAYS[len(days)]
        days.append({"day": day.capitalize(), "colour": hexc, "hue": hue, "note": note, "chakra": chakra, "virtue": virtue})
    return {"_about": "Sunday first; each day's colour is the CHECKPOINT's trim (day_trims.h) and its note C to B "
                      "(vision 9.21); its hue, chakra and virtue are RoverRadio's day table (companion docs/INHERITANCE.md).",
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
            "flags_byte": 19, "away_bit": AWAY_BIT, "asked_bit": ASKED_BIT}


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


def main():
    files = {"species.json": species_table(), "charmap.json": charmap_table(), "week.json": week_table(),
             "seasons.json": seasons_table(), "streaks.json": streaks_table(), "moves.json": moves_table()}
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


if __name__ == "__main__":
    main()

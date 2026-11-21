#!/usr/bin/env python3
"""MUSAI's sixth and seventh forms: SONGMUSAI (SIGNAL) and LANGMUSAI (EMERGENT) (T-605).

    python3 tools/gbamusaiforms.py            # report what it would change
    python3 tools/gbamusaiforms.py --write    # the picked art into gfx/daemons/, then every engine table

THE USER'S DECISIONS (2026-11-21, by multiple choice): MUSAI grows into seven forms, not five. SONGMUSAI is SIGNAL
(TYPE_ELECTRIC) -- the bible's near-miss MusaiStudio, the music module, and the song is now how every daemon grows
(T-594..T-598). LANGMUSAI is EMERGENT (TYPE_DRAGON) -- a language is a code and also is not one, "lang" is how code
names a language, and language is the classic emergent thing. Each grows from a NEW INPUT, as CODE, SEEK and CARE do
from AXIOM, EMBEDDING and AFFECT: ITEM_SONG_INPUT and ITEM_LANG_INPUT (were ITEM_063 and ITEM_064, unused, and inside
gItemEffectTable's range, which an evolution stone needs), named DRAFT, sold beside the other inputs on CELADON's
department store 4F (DRAFT). The items' rows are hand-written (items.json, item_effects.h, EEVEE's evolution row);
their icons are tools/gbaitemicons.py's ICONS5.

THE SLOTS. Gen 3's unused OLD_UNOWN_N and OLD_UNOWN_O (264, 265), after THE NEXUS's eight (C-J, tools/gbanexus.py)
and the carried line (K-M, tools/gbacarried.py) -- the path both took, so no species constant is added: NUM_SPECIES,
the save's INDEX bit arrays (DEX_FLAGS_NO is NUM_SPECIES's) and every species-sized table stay as they are. EEVEE's
evolutions grow from five to seven, so EVOS_PER_MON is 7 (ROM data; nothing in a save is sized by it).

THE INDEX. They are INDEX 398-399, after the carried line; MISSINGNO (OLD_UNOWN_B) moves from 398 to 400, still one
past the end (8.9), and src/daemons_carried.c carries a save's MISSINGNO bits across once more (FLAG_MUSAI_DEX_MOVED).
NATIONAL_DEX_COUNT becomes LANGMUSAI. src/daemons_hermetic.c's costume bound moves to OLD_UNOWN_P..Z with them.

THE ART goes through T-552/T-553's pipeline (gfx/drafts/t605/scripts/): a natural creature body under MUSAI's round
helmet head, drawn on the sprite server at 512x512 (klein4b, the pixel-art LoRA), keyed, cleaned (armc.clean, the
streaks placed) and reduced on the TYPE's ramp. This copies the picked clean drawings into gfx/daemons/<name>_front|
back.png (and the reduced icon to _icon.png), and tools/gbasprite.py builds them into graphics/pokemon/old_unown_n|o/
like any other redrawn daemon. So after a --write here: `gbasprite.py --write`, `genstreaks.py --write`,
`gbafollower.py --write`, `gbafollowerpal.py --write`, `gencries.py --write --approved`, then this again. NOT YET IN THE
SEASONAL BRANCH (T-532): the two wear one coat all year until their winter, spring and autumn are drawn and their
seasonal INDEX lines written -- then they join tools/genmusaiseasons.py's BRANCH (appended, so no form's id moves).

STATS, ROUTINES, ABILITIES, the INDEX's words and the items' are proposals for the user: every word is DRAFT.
"""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
BEGIN, END = "BEGIN gbamusaiforms", "END gbamusaiforms"
SLOT0 = 264                                             # SPECIES_OLD_UNOWN_N

#  slot, name, ident, the daemon its INDEX scale, footprint and menu placing are borrowed from (and its cry's cap:
#  tools/gencries.py caps a slot's own cry at that cry's length)
LINE = [
    ("N", "SONGMUSAI", "Songmusai", "JOLTEON"),
    ("O", "LANGMUSAI", "Langmusai", "ESPEON"),
]

#  the art: the picked drawings (gfx/drafts/t605/picks.json says which seed each is), clean RGBA as armc.clean made them
ART_DIR = "gfx/drafts/t605/picked"
ART_KINDS = ("front", "back", "icon")

#  stats: HP, Atk, Def, Speed, SpAtk, SpDef -- PROPOSED, 525 each like the other five forms (one stat at 130, one at
#  110, one at 95 or so). SONGMUSAI holds a long note (SP. DEF); LANGMUSAI holds its structure (DEFENSE, the one 130 no
#  other form has).
INFO = {
    "SONGMUSAI": dict(stats=(95, 65, 65, 60, 110, 130), types=("ELECTRIC", "ELECTRIC"), exp=197, ev="SpDefense", evn=2,
                      height=9, weight=245, color="YELLOW"),
    "LANGMUSAI": dict(stats=(65, 110, 130, 95, 60, 65), types=("DRAGON", "DRAGON"), exp=197, ev="Defense", evn=2,
                      height=9, weight=265, color="GREEN"),
}
#  LIGHTNING ROD ("Draws electrical moves": a song draws the room's signal to it); TRACE ("Copies special ability":
#  a language is picked up from whoever is speaking). One ability each, as the other forms have.
ABILITIES = {"SONGMUSAI": ("LIGHTNING_ROD", "NONE"), "LANGMUSAI": ("TRACE", "NONE")}

#  PROPOSED routines: the branch's shared opening (TACKLE, TAIL WHIP, HELPING HAND, SAND-ATTACK) and then its own, at
#  the levels every form learns at (our names in the comments). SONGMUSAI: PULSE, LULLABY, ARC, CLEARFLAGS, CARRIER,
#  EMIT, DISCHARGE -- LULLABY and EMIT are sound and off-type, the residual 2.7a keeps on purpose. LANGMUSAI:
#  ATTRACTOR, CLONE, UNPLANNED, REPLAY, EMERGE, BLOOM, RUNAWAY -- CLONE and REPLAY off-type: a language is learned by
#  repeating what was heard.
_OPEN = [(1, "TACKLE"), (1, "TAIL_WHIP"), (1, "HELPING_HAND"), (8, "SAND_ATTACK")]
LEARNSETS = {
    "SONGMUSAI": _OPEN + [(16, "THUNDER_SHOCK"), (23, "SING"), (30, "SPARK"), (36, "HEAL_BELL"), (42, "SHOCK_WAVE"),
                          (47, "HYPER_VOICE"), (52, "THUNDERBOLT")],
    "LANGMUSAI": _OPEN + [(16, "TWISTER"), (23, "MIMIC"), (30, "DRAGON_BREATH"), (36, "ENCORE"), (42, "DRAGON_CLAW"),
                          (47, "DRAGON_DANCE"), (52, "OUTRAGE")],
}
#  PLUGINs: the borrowed daemon's, and LANGMUSAI's own type's claw
TM_EXTRA = {"LANGMUSAI": ["TM02_DRAGON_CLAW"]}

#  THE INDEX (T-605, ALL DRAFT): category, CONTENT, CONTEXT
ENTRIES = {
    "SONGMUSAI": ("MELODY",
        ["It sings back what it hears, a little", "truer each time. Taught one song, it", "finds that tune in everything."],
        ["Every song it knows, it learned from", "someone singing. It cannot say who.", "It still keeps their time."]),
    "LANGMUSAI": ("GRAMMAR",
        ["Nobody taught it the rules it speaks", "by. It heard enough, and the rules were", "there. It cannot list them."],
        ["It says things nobody said to it. Each", "word came from someone. The sentence", "did not."]),
}

_src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
_ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
exec(compile(_src.split("# ------------------------------------------------------- names, derived")[0], "port_vocab.py", "exec"), _ns)
width = _ns["textwidth"]
PANE_W = 234


def gpath(*p):
    return os.path.join(GBA, *p)


def sub1(pat, repl, s, what, count=0):
    out, n = re.subn(pat, repl, s, count=count)
    assert n == 1, "%s: %d matches, want 1 -- %s" % (what, n, pat)
    return out


def block(lines):
    return ["// %s -- T-605, MUSAI's sixth and seventh forms (tools/gbamusaiforms.py writes this)" % BEGIN] + lines + \
           ["// %s" % END]


def cry_id(ident):
    """T-584: the daemon's own cry's index in gCryTable (sound/cry_tables.inc, which tools/gencries.py writes), or
    None before gencries has given it one."""
    labels = re.findall(r"^\s*cry (Cry_\w+)", open(os.path.join(GBA, "sound/cry_tables.inc")).read(), re.M)
    return labels.index("Cry_" + ident) if "Cry_" + ident in labels else None


def put_block(text, anchor, lines, after=True):
    """Replace this tool's block if present, else insert it after (or before) the anchor line."""
    blk = "\n".join(block(lines)) + "\n"
    m = re.search(r"// %s.*?// %s\n" % (re.escape(BEGIN), re.escape(END)), text, re.S)
    if m:
        return text[:m.start()] + blk + text[m.end():]
    i = text.index(anchor)
    if after:
        j = text.index("\n", i) + 1
        return text[:j] + blk + text[j:]
    return text[:i] + blk + text[i:]


def species_entry(text, key, body):
    pat = re.compile(r"(\[%s\]\s*=\s*)(\{(?:[^{}]|\{[^{}]*\})*\}|[^\n]*?)(,)" % re.escape(key))
    return pat.subn(lambda m: m.group(1) + body + m.group(3), text, count=1)


def braced(text, key):
    m = re.search(r"\[%s\]\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\})" % re.escape(key), text)
    return m.group(1) if m else None


# ---- the art --------------------------------------------------------------------------------------------------------
def copy_art(report):
    """The picked clean drawings into gfx/daemons/ -- where gbasprite.py, the companion and the review sheets look."""
    for _, name, *_ in LINE:
        for kind in ART_KINDS:
            src = os.path.join(ROOT, ART_DIR, "%s_%s.png" % (name.lower(), kind))
            out = os.path.join(ROOT, "gfx/daemons", "%s_%s.png" % (name.lower(), kind))
            if not os.path.exists(src):
                report.append("  %s %s: no drawing picked yet (%s)" % (name, kind, os.path.relpath(src, ROOT)))
                continue
            if os.path.exists(out) and open(src, "rb").read() == open(out, "rb").read():
                continue
            if WRITE:
                shutil.copyfile(src, out)
            report.append("  %s %s" % ("copied" if WRITE else "would copy", os.path.relpath(out, ROOT)))


def built(letter):
    """What gbasprite.py built for the slot: (front coords, back coords, icon palette), or None before it has."""
    from PIL import Image
    d = gpath("graphics/pokemon/old_unown_%s" % letter.lower())
    try:
        f, b, i = (Image.open(os.path.join(d, n + ".png")) for n in ("front", "back", "icon"))
    except OSError:
        return None
    def coords(img):
        box = img.point(lambda v: 255 if v else 0).getbbox()
        w = min(64, (box[2] - box[0] + 7) // 8 * 8)
        h = min(64, (box[3] - box[1] + 7) // 8 * 8)
        return w, h, 64 - box[3]
    pal = [tuple(i.getpalette()[k:k + 3]) for k in range(3, 48, 3)]
    best = 0
    for n in range(3):
        lines = open(gpath("graphics/pokemon/icon_palettes/icon_palette_%d.pal" % n)).read().split()
        p = [tuple(int(v) for v in lines[3 + k * 3:6 + k * 3]) for k in range(1, 16)]
        if p == pal:
            best = n
    return coords(f), coords(b), best


def slot_dir(letter):
    return gpath("graphics/pokemon/old_unown_%s" % letter.lower())


# ---- the engine's tables ------------------------------------------------------------------------------------------
def engine():
    changed = {}
    def edit(path, fn):
        p = gpath(path)
        old = changed.get(p) or open(p).read()
        new = fn(old)
        if new != open(p).read():
            changed[p] = new
        elif p in changed:
            del changed[p]

    edit("include/constants/species.h", lambda t: put_block(t, "// END gbacarried",
         ["#define SPECIES_%s SPECIES_OLD_UNOWN_%s" % (name, letter) for letter, name, *_ in LINE]))

    def dex(t):
        t = put_block(t, "// END gbacarried", ["    NATIONAL_DEX_%s," % name for _, name, *_ in LINE])
        return re.sub(r"#define NATIONAL_DEX_COUNT\s+NATIONAL_DEX_\w+",
                      "#define NATIONAL_DEX_COUNT  NATIONAL_DEX_%s" % LINE[-1][1], t)
    edit("include/constants/pokedex.h", dex)

    def to_nat(t):
        for letter, name, *_ in LINE:
            t = t.replace("SPECIES_TO_NATIONAL(OLD_UNOWN_%s)" % letter, "NATIONAL_DEX_%s" % name, 1)
            t = t.replace("HOENN_TO_NATIONAL(OLD_UNOWN_%s)" % letter,
                          "[HOENN_DEX_OLD_UNOWN_%s - 1] = NATIONAL_DEX_%s" % (letter, name), 1)
        return t
    edit("src/pokemon.c", to_nat)

    #  T-584's way: each its own cry, after the carried line's (tools/gencries.py); the table holds the cry's id. Until
    #  gencries has made them, the slots keep playing UNOWN's, as every empty slot does.
    ids = [cry_id(ident) for _, _, ident, _ in LINE]
    if all(i is not None for i in ids):
        def cries(t):
            lines = ["static const u16 sMusaiFormCries[] = {   // T-605: cry ids, each its own (tools/gencries.py)"] + \
                    ["    [SPECIES_%s - SPECIES_OLD_UNOWN_N] = %d,   // Cry_%s" % (name, i, ident)
                     for (_, name, ident, _), i in zip(LINE, ids)] + ["};"]
            t = put_block(t, "u16 SpeciesToCryId(u16 species)", lines, after=False)
            if "sMusaiFormCries[species" not in t:
                t = sub1(r"(    if \(species <= SPECIES_OLD_UNOWN_Z - 1\)\n        return SPECIES_UNOWN - 1;)",
                         "    if (species >= SPECIES_OLD_UNOWN_N - 1 && species <= SPECIES_OLD_UNOWN_O - 1)   // T-605\n"
                         "        return sMusaiFormCries[species - (SPECIES_OLD_UNOWN_N - 1)];\n\\1", t, "cries")
            return t
        edit("src/pokemon.c", cries)

    def pos(t):
        lines = ["static const u16 sMusaiFormPosModel[] = {"] + \
                ["    [SPECIES_%s - SPECIES_OLD_UNOWN_N] = SPECIES_%s," % (name, model) for _, name, _, model in LINE] + ["};", ""]
        t = put_block(t, "u8 Menu2_GetMonPosAttribute(u16 species, u32 personality, u8 attributeId)", lines, after=False)
        if "sMusaiFormPosModel[species" not in t:
            t = sub1(r"(        species = sCarriedPosModel\[species - SPECIES_OLD_UNOWN_K\];\n)",
                     "\\1    else if (species >= SPECIES_OLD_UNOWN_N && species <= SPECIES_OLD_UNOWN_O)   // T-605\n"
                     "        species = sMusaiFormPosModel[species - SPECIES_OLD_UNOWN_N];\n", t, "pos")
        return t
    edit("src/menu2.c", pos)

    def names(t):
        for letter, name, *_ in LINE:
            t = sub1(r'(\[SPECIES_OLD_UNOWN_%s\]\s*=\s*_\(")[^"]*("\))' % letter, r"\g<1>%s\g<2>" % name, t,
                     "species_names.h OLD_UNOWN_" + letter)
        return t
    edit("src/data/text/species_names.h", names)

    def info(t):
        for letter, name, *_ in LINE:
            i = INFO[name]
            hp, at, df, sp, sa, sd = i["stats"]
            evs = {k: 0 for k in ("HP", "Attack", "Defense", "Speed", "SpAttack", "SpDefense")}
            evs[i["ev"]] = i["evn"]
            body = "\n".join([
                "    {   // T-605 (DRAFT, proposed): MUSAI's %s form" % ("sixth" if letter == "N" else "seventh"),
                "        .baseHP = %d," % hp, "        .baseAttack = %d," % at, "        .baseDefense = %d," % df,
                "        .baseSpeed = %d," % sp, "        .baseSpAttack = %d," % sa, "        .baseSpDefense = %d," % sd,
                "        .types = {TYPE_%s, TYPE_%s}," % i["types"], "        .catchRate = 45,", "        .expYield = %d," % i["exp"]] +
                ["        .evYield_%s = %d," % (k, v) for k, v in evs.items()] + [
                "        .itemCommon = ITEM_NONE,", "        .itemRare = ITEM_NONE,", "        .genderRatio = PERCENT_FEMALE(12.5),",
                "        .eggCycles = 35,", "        .friendship = 70,", "        .growthRate = GROWTH_MEDIUM_FAST,",
                "        .eggGroups = {EGG_GROUP_FIELD, EGG_GROUP_FIELD},",
                "        .abilities = {ABILITY_%s, ABILITY_%s}," % ABILITIES[name], "        .safariZoneFleeRate = 0,",
                "        .bodyColor = BODY_COLOR_%s," % i["color"], "        .noFlip = FALSE,", "    }"])
            t, n = species_entry(t, "SPECIES_OLD_UNOWN_" + letter, "\n" + body)
            assert n == 1, letter
            t = re.sub(r"(\[SPECIES_OLD_UNOWN_%s\] =)\s*\{" % letter, r"\1\n    {", t, count=1)
        return t
    edit("src/data/pokemon/species_info.h", info)

    def lvl(t):
        for letter, name, *_ in LINE:
            sym = "sSpecies%dLevelUpLearnset" % (SLOT0 + "NO".index(letter))
            body = "static const u16 %s[] = {   // T-605 (DRAFT, proposed): %s\n" % (sym, name) + \
                   "".join("    LEVEL_UP_MOVE(%d, MOVE_%s),\n" % (l, m) for l, m in LEARNSETS[name]) + "    LEVEL_UP_END\n};"
            t = sub1(r"static const u16 %s\[\] = \{[^}]*\};" % sym, lambda _: body, t, sym)
        return t
    edit("src/data/pokemon/level_up_learnsets.h", lvl)

    def tmhm(t):
        for letter, name, ident, model in LINE:
            m = re.search(r"\[SPECIES_%s\]\s*=\s*TMHM_LEARNSET\(((?:[^()]|\([^()]*\))*)\)," % model, t)
            parts = [p.strip() for p in m.group(1).split("|")]
            parts += ["TMHM(%s)" % x for x in TM_EXTRA.get(name, []) if "TMHM(%s)" % x not in parts]
            body = "TMHM_LEARNSET(" + "\n                                        | ".join(parts) + ")"
            t = sub1(r"\[SPECIES_OLD_UNOWN_%s\]\s*=\s*TMHM_LEARNSET\((?:[^()]|\([^()]*\))*\)," % letter,
                     lambda _: "[SPECIES_OLD_UNOWN_%s] = %s," % (letter, body), t, "tmhm " + letter)
        return t
    edit("src/data/pokemon/tmhm_learnsets.h", tmhm)

    #  the evolutions are EEVEE's own row (seven now, EVOS_PER_MON): checked here, never written
    evo = open(gpath("src/data/pokemon/evolution.h")).read()
    for item, letter in (("ITEM_SONG_INPUT", "N"), ("ITEM_LANG_INPUT", "O")):
        assert "{EVO_ITEM, %s, SPECIES_OLD_UNOWN_%s}" % (item, letter) in evo, "EEVEE's row lacks " + item

    #  the sprites, once gbasprite.py has built them into the slots' own folders
    have = {letter: built(letter) for letter, *_ in LINE}
    if all(have.values()):
        def gfxdata(t):
            lines = []
            for letter, name, ident, _ in LINE:
                d = "graphics/pokemon/old_unown_%s" % letter.lower()
                lines += ['const u32 gMonFrontPic_%s[] = INCBIN_U32("%s/front.4bpp.lz");' % (ident, d),
                          'const u32 gMonBackPic_%s[] = INCBIN_U32("%s/back.4bpp.lz");' % (ident, d),
                          'const u32 gMonPalette_%s[] = INCBIN_U32("%s/normal.gbapal.lz");' % (ident, d),
                          'const u32 gMonShinyPalette_%s[] = INCBIN_U32("%s/shiny.gbapal.lz");' % (ident, d),
                          'const u8 gMonIcon_%s[] = INCBIN_U8("%s/icon.4bpp");' % (ident, d),
                          'const u8 gMonFootprint_%s[] = INCBIN_U8("%s/footprint.1bpp");' % (ident, d)]
            return put_block(t, "const u32 gMonFrontPic_Absol[]", lines, after=False)
        edit("src/data/graphics/pokemon.h", gfxdata)

        def externs(t):
            lines = []
            for letter, name, ident, _ in LINE:
                lines += ["extern const u32 gMonFrontPic_%s[];" % ident, "extern const u32 gMonBackPic_%s[];" % ident,
                          "extern const u32 gMonPalette_%s[];" % ident, "extern const u32 gMonShinyPalette_%s[];" % ident,
                          "extern const u8 gMonIcon_%s[];" % ident, "extern const u8 gMonFootprint_%s[];" % ident]
            return put_block(t, "extern const u32 gMonFrontPic_Absol[];", lines, after=False)
        edit("include/graphics.h", externs)

        def macro_table(path, macro, symbol):
            def fn(t):
                for letter, name, ident, _ in LINE:
                    t = sub1(r"%s\(OLD_UNOWN_%s,\s*\w+\)" % (macro, letter), "%s(OLD_UNOWN_%s, %s_%s)" % (macro, letter, symbol, ident),
                             t, path + letter)
                return t
            edit(path, fn)
        macro_table("src/data/pokemon_graphics/front_pic_table.h", "SPECIES_SPRITE", "gMonFrontPic")
        macro_table("src/data/pokemon_graphics/back_pic_table.h", "SPECIES_SPRITE", "gMonBackPic")
        macro_table("src/data/pokemon_graphics/palette_table.h", "SPECIES_PAL", "gMonPalette")
        macro_table("src/data/pokemon_graphics/shiny_palette_table.h", "SPECIES_SHINY_PAL", "gMonShinyPalette")

        def keyed(path, valuefn):
            def fn(t):
                for letter, name, ident, _ in LINE:
                    t, n = species_entry(t, "SPECIES_OLD_UNOWN_" + letter, valuefn(letter, ident))
                    assert n == 1, (path, letter)
                return t
            edit(path, fn)
        keyed("src/data/pokemon_graphics/footprint_table.h", lambda l, i: "gMonFootprint_" + i)
        keyed("src/data/pokemon_graphics/front_pic_coordinates.h",
              lambda l, i: "{\n        .size = MON_COORDS_SIZE(%d, %d),\n        .y_offset = %d,\n    }" % have[l][0])
        keyed("src/data/pokemon_graphics/back_pic_coordinates.h",
              lambda l, i: "{\n        .size = MON_COORDS_SIZE(%d, %d),\n        .y_offset = %d,\n    }" % have[l][1])

        def icons(t):
            for letter, name, ident, _ in LINE:
                t = sub1(r"(\[SPECIES_OLD_UNOWN_%s\]\s*=\s*)gMonIcon_\w+," % letter, r"\g<1>gMonIcon_%s," % ident, t, "icon " + letter, count=1)
                t = sub1(r"(\[SPECIES_OLD_UNOWN_%s\]\s*=\s*)\d," % letter, r"\g<1>%d," % have[letter][2], t, "iconpal " + letter, count=1)
            return t
        edit("src/pokemon_icon.c", icons)

    def entries(t):
        lines = []
        for letter, name, ident, model in LINE:
            mb = braced(t, "NATIONAL_DEX_" + model)
            g = lambda f: re.search(r"\.%s\s*=\s*(-?\d+)" % f, mb).group(1)
            lines += ["    [NATIONAL_DEX_%s] =" % name, "    {",
                      '        .categoryName = _("%s"),   // T-605, DRAFT' % ENTRIES[name][0],
                      "        .height = %d," % INFO[name]["height"], "        .weight = %d," % INFO[name]["weight"],
                      "        .description = g%sPokedexText," % ident,
                      "        .unusedDescription = g%sPokedexText," % ident,
                      "        .pokemonScale = %s," % g("pokemonScale"), "        .pokemonOffset = %s," % g("pokemonOffset"),
                      "        .trainerScale = %s," % g("trainerScale"), "        .trainerOffset = %s," % g("trainerOffset"),
                      "    },"]
        return put_block(t, "    //  8.9 -- the entry the register does not hold.", lines, after=False)
    edit("src/data/pokemon/pokedex_entries.h", entries)

    def dextext(which):
        def fn(t):
            lines = []
            for letter, name, ident, _ in LINE:
                ls = ENTRIES[name][1 if which == "fr" else 2]
                lines += ["// T-605, DRAFT", "const u8 g%sPokedexText[] = _(" % ident] + \
                         ['    "%s%s"%s' % (l, "\\n" if i < len(ls) - 1 else "", ");" if i == len(ls) - 1 else "")
                          for i, l in enumerate(ls)] + [""]
            return put_block(t, "const u8 gAbsolPokedexText[]", lines, after=False)
        return fn
    edit("src/data/pokemon/pokedex_text_fr.h", dextext("fr"))
    edit("src/data/pokemon/pokedex_text_lg.h", dextext("lg"))

    def orders(t):
        for letter, name, ident, model in LINE:
            if "NATIONAL_DEX_%s," % name in t:
                continue
            t = re.sub(r"(\n(\s*)NATIONAL_DEX_%s,)" % model,
                       lambda m: m.group(1) + "\n" + m.group(2) + "NATIONAL_DEX_%s," % name, t)
        return t
    edit("src/data/pokemon/pokedex_orders.h", orders)
    return changed, have


def footprints(report):
    for letter, name, ident, model in LINE:
        d = slot_dir(letter)
        fp = os.path.join(d, "footprint.png")
        if not os.path.exists(fp):
            if WRITE:
                os.makedirs(d, exist_ok=True)
                shutil.copyfile(gpath("graphics/pokemon/%s/footprint.png" % model.lower()), fp)
            report.append("  %s %s (%s's footprint)" % ("made" if WRITE else "would make", os.path.relpath(d, GBA), model))


def main():
    report = []
    for name, (cat, fr, lg) in ENTRIES.items():
        assert len(name) <= 10 and len(cat) <= 11, name
        for ls in (fr, lg):
            assert len(ls) <= 4, name
            for l in ls:
                assert width(l) <= PANE_W, (name, l, width(l))
    copy_art(report)
    footprints(report)
    changed, have = engine()
    for letter, name, ident, _ in LINE:
        h = have[letter]
        report.append("  %-10s %s" % (name, "front %dx%d y%d, back %dx%d y%d, icon palette %d" % (h[0] + h[1] + (h[2],))
                                       if h else "not built yet: run gbasprite.py --write, then this again"))
        if cry_id(ident) is None:
            report.append("  %-10s no cry of its own yet: run gencries.py --write --approved, then this again" % name)
    for p in sorted(changed):
        report.append("  %s %s" % ("wrote" if WRITE else "would write", os.path.relpath(p, GBA)))
    if WRITE:
        for p, s in changed.items():
            open(p, "w").write(s)
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())

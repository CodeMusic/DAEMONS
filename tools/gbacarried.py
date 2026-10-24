#!/usr/bin/env python3
"""THE CARRIED LINE: HANDSHAKE -> TETHERING -> COROUTINE, a daemon that grows only while carried (T-450, C-185).

    python3 tools/gbacarried.py            # report what it would change
    python3 tools/gbacarried.py --write    # the cleaned art (gfx/daemons/), then every engine table

THE USER'S DECISION (2026-10-24; docs/private/plan-carried-line-2026-10-24.md, line A): a sugar glider in Gen 3's
unused slots OLD_UNOWN_K/L/M (261/262/263), SIGNAL, SIGNAL, SIGNAL/STRATUM, growing by a new method EVO_CARRIED that
nothing on the cart meets -- the companion judges it (bond 60 and 160) and SYNC brings the grown one home (T-448). No
eggs (UNDISCOVERED); the INDEX's workings show a bare arrow. Nothing in the game gives one: the first comes from the
companion.

THE INDEX. They are INDEX 395-397, after the NEXUS's eight; MISSINGNO (OLD_UNOWN_B) moves from 395 to 398, still one
past the end (8.9), and src/daemons_carried.c carries a save's MISSINGNO seen/caught bits (and its FIRST MET byte)
across once. NATIONAL_DEX_COUNT becomes COROUTINE.

THE ART goes through the house pipeline, not its own: the three concepts picked for the sheet (gfx/drafts/t450/) and
the rear views drawn for this build (gfx/drafts/t450/scripts/genback.py) are cleaned here with tools/cleandraft.py
(--streaks, the strokes placed on the body by box) into gfx/daemons/<name>_front|back.png, and tools/gbasprite.py
builds them in the TYPE's ramp (9.4, invariant 5) into graphics/pokemon/old_unown_k|l|m/ like any other daemon. This
tool then reads what gbasprite built for the frame sizes and the icon's palette. So after a --write here:
`gbasprite.py --write`, `genstreaks.py --write`, `gbafollowerpal.py --write`, then this again. FIRST DRAFTS: the
chibi style is still T-452's pilot.

STATS, ROUTINES, ABILITIES are proposals for the user (the plan gave none): a small early line, the last stage
mid-tier. Every in-game word is DRAFT until played.
"""
import os, re, shutil, subprocess, sys
from PIL import Image, ImageOps
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
BEGIN, END = "BEGIN gbacarried", "END gbacarried"
PY = sys.executable

#  slot, name, ident, the daemon its INDEX scale, footprint, cry and menu placing are borrowed from
LINE = [
    ("K", "HANDSHAKE", "Handshake", "PICHU"),
    ("L", "TETHERING", "Tethering", "PIKACHU"),
    ("M", "COROUTINE", "Coroutine", "RAICHU"),
]
EVOLUTIONS = {"K": ("EVO_CARRIED", "60", "L"), "L": ("EVO_CARRIED", "160", "M")}

#  the art: (draft, streak box in the draft's 64 art px) for front and back. The model would not draw these three from
#  behind (gfx/drafts/t450/*_back_*: nine seeds, eight of them facing the viewer), so two backs are their front turned
#  round (":mirror") and TETHERING's is the one seed that looks back over its shoulder -- first drafts, for the user.
ART = {
    "HANDSHAKE": (("handshake_4505", "29,37,43,48"), ("handshake_4505:mirror", "20,37,34,48")),
    "TETHERING": (("tethering_4501", "17,36,32,50"), ("tethering_back_4551", None)),
    "COROUTINE": (("coroutine_4508", "20,37,32,47"), ("coroutine_4508:mirror", "31,37,43,47")),
}

#  stats: HP, Atk, Def, Speed, SpAtk, SpDef -- PROPOSED (250 / 360 / 485)
INFO = {
    "HANDSHAKE": dict(stats=(40, 35, 30, 60, 45, 40), types=("ELECTRIC", "ELECTRIC"), exp=55, ev="Speed", evn=1,
                      height=2, weight=10),
    "TETHERING": dict(stats=(60, 50, 45, 85, 65, 55), types=("ELECTRIC", "ELECTRIC"), exp=120, ev="Speed", evn=2,
                      height=3, weight=25),
    "COROUTINE": dict(stats=(75, 70, 75, 100, 85, 80), types=("ELECTRIC", "GROUND"), exp=190, ev="Speed", evn=3,
                      height=6, weight=60),
}
#  CHARGED (STATIC) and MUTUAL (SYNCHRONIZE); COROUTINE picks up where it left off, FAST RESUME (EARLY BIRD)
ABILITIES = {"HANDSHAKE": ("STATIC", "SYNCHRONIZE"), "TETHERING": ("STATIC", "SYNCHRONIZE"),
             "COROUTINE": ("SYNCHRONIZE", "EARLY_BIRD")}

#  PROPOSED routines (our names in the comments): PULSE, DERATE, DELEGATE, FAST PATH, BROWNOUT, ARC, REDIRECT, CARRIER,
#  TAIL, HANDOFF, SEDIMENT, RAPPORT, REFRAME, DISCHARGE, UPHEAVAL. A delivered HANDSHAKE (level 5) knows the first three.
LEARNSETS = {
    "HANDSHAKE": [(1, "THUNDER_SHOCK"), (1, "GROWL"), (4, "HELPING_HAND"), (8, "QUICK_ATTACK"), (12, "THUNDER_WAVE"),
                  (17, "SPARK"), (22, "FOLLOW_ME"), (28, "SHOCK_WAVE"), (34, "RETURN")],
    "TETHERING": [(1, "THUNDER_SHOCK"), (1, "GROWL"), (1, "HELPING_HAND"), (1, "QUICK_ATTACK"), (12, "THUNDER_WAVE"),
                  (17, "SPARK"), (22, "FOLLOW_ME"), (28, "SHOCK_WAVE"), (34, "PURSUIT"), (40, "RETURN"),
                  (46, "AGILITY"), (52, "THUNDERBOLT")],
    "COROUTINE": [(1, "THUNDER_SHOCK"), (1, "HELPING_HAND"), (1, "QUICK_ATTACK"), (1, "THUNDER_WAVE"), (17, "SPARK"),
                  (22, "FOLLOW_ME"), (28, "SHOCK_WAVE"), (30, "BATON_PASS"), (34, "MUD_SHOT"), (40, "RETURN"),
                  (46, "AGILITY"), (52, "THUNDERBOLT"), (58, "EARTHQUAKE")],
}
#  PLUGINs: the borrowed daemon's, and COROUTINE also digs (STRATUM)
TM_EXTRA = {"COROUTINE": ["TM26_EARTHQUAKE", "TM28_DIG"]}

#  THE INDEX (the user chose line A, 2026-10-24; word for word from the plan, ALL DRAFT): category, CONTENT, CONTEXT
ENTRIES = {
    "HANDSHAKE": ("GREETING",
        ["It holds one paw out to whoever lifts", "it, and keeps it out until it is taken.", "Nobody has found one already grown."],
        ["It asks once, and waits to be asked", "back. An answer that comes back is all", "it needs to ask again tomorrow."]),
    "TETHERING": ("CARRIED",
        ["It rides along and counts the steps it", "is carried. Left in a box it stays as it", "was. Walked a long way, it changes."],
        ["Ask it where it has been and it does not", "name the places. It names the walks, and", "who was walking."]),
    "COROUTINE": ("TURNTAKER",
        ["It glides off the shoulder it rides and", "lands on it again a few steps on. It", "picks up exactly where it left off."],
        ["One rests while the other goes on, then", "they change. Neither one started it, and", "neither could finish it alone."]),
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
    return ["// %s -- T-450, the carried line (tools/gbacarried.py writes this)" % BEGIN] + lines + ["// %s" % END]


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
def clean_art(report):
    """The drafts, cleaned into gfx/daemons/ -- where gbasprite.py, the companion and the review sheets look."""
    for name, views in ART.items():
        for view, (draft, box) in zip(("front", "back"), views):
            src = os.path.join(ROOT, "gfx/drafts/t450", draft.split(":")[0] + ".png")
            if draft.endswith(":mirror"):
                tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
                ImageOps.mirror(Image.open(src)).save(tmp)
                src = tmp
            out = os.path.join(ROOT, "gfx/daemons", "%s_%s.png" % (name.lower(), view))
            cmd = [PY, os.path.join(ROOT, "tools/cleandraft.py"), src, out, "--streaks"]
            if box:
                cmd.append("--streak-box=" + box)
            if WRITE:
                r = subprocess.run(cmd, capture_output=True, text=True)
                assert r.returncode == 0, r.stdout + r.stderr
            report.append("  %s %s <- %s%s" % ("cleaned" if WRITE else "would clean", os.path.relpath(out, ROOT),
                                              draft, " (streaks in %s)" % box if box else ""))


def built(letter):
    """What gbasprite.py built for the slot: (front coords, back coords, icon palette), or None before it has."""
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
    d = gpath("graphics/pokemon/old_unown_%s" % letter.lower())
    return d


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

    edit("include/constants/species.h", lambda t: put_block(t, "#define SPECIES_OLD_UNOWN_Z",
         ["#define SPECIES_%s SPECIES_OLD_UNOWN_%s" % (name, letter) for letter, name, *_ in LINE]))

    def evo_const(t):
        if "EVO_CARRIED" in t:
            return t
        return sub1(r"(#define EVO_BEAUTY\s+15[^\n]*\n)",
                    r"\g<1>#define EVO_CARRIED          16 // T-450: grows on the companion (the bond, as param); never met on the cart\n",
                    t, "EVO_CARRIED")
    edit("include/constants/pokemon.h", evo_const)

    def dex(t):
        t = put_block(t, "// END gbanexus", ["    NATIONAL_DEX_%s," % name for _, name, *_ in LINE])
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

    def cries(t):
        lines = ["static const u16 sCarriedCries[] = {"] + \
                ["    [SPECIES_%s - SPECIES_OLD_UNOWN_K] = SPECIES_%s," % (name, model) for _, name, _, model in LINE] + ["};"]
        t = put_block(t, "u16 SpeciesToCryId(u16 species)", lines, after=False)
        if "sCarriedCries[species" not in t:
            t = sub1(r"(    if \(species <= SPECIES_OLD_UNOWN_Z - 1\)\n        return SPECIES_UNOWN - 1;)",
                     "    if (species >= SPECIES_OLD_UNOWN_K - 1 && species <= SPECIES_OLD_UNOWN_M - 1)   // T-450\n"
                     "        return SpeciesToCryId(sCarriedCries[species - (SPECIES_OLD_UNOWN_K - 1)] - 1);\n\\1", t, "cries")
        return t
    edit("src/pokemon.c", cries)

    #  GetEvolutionTargetSpecies has no case for it, on purpose: say so where someone would "fix" it
    def evo_note(t):
        if "EVO_CARRIED" in t:
            return t
        return sub1(r"(        for \(i = 0; i < EVOS_PER_MON; i\+\+\)\n        \{\n            switch \(gEvolutionTable\[species\]\[i\]\.method\)\n            \{\n            case EVO_FRIENDSHIP:)",
                    "        //  T-450: EVO_CARRIED has no case here, deliberately -- the companion judges it, and SYNC brings the\n"
                    "        //  grown daemon home already grown (src/daemons_carried.c). Nothing on the cart may meet it.\n\\1", t, "evo note", count=1)
    edit("src/pokemon.c", evo_note)

    def pos(t):
        lines = ["static const u16 sCarriedPosModel[] = {"] + \
                ["    [SPECIES_%s - SPECIES_OLD_UNOWN_K] = SPECIES_%s," % (name, model) for _, name, _, model in LINE] + ["};", ""]
        t = put_block(t, "u8 Menu2_GetMonPosAttribute(u16 species, u32 personality, u8 attributeId)", lines, after=False)
        if "sCarriedPosModel[species" not in t:
            t = sub1(r"(        species = sNexusPosModel\[species - SPECIES_OLD_UNOWN_C\];\n)",
                     "\\1    else if (species >= SPECIES_OLD_UNOWN_K && species <= SPECIES_OLD_UNOWN_M)   // T-450\n"
                     "        species = sCarriedPosModel[species - SPECIES_OLD_UNOWN_K];\n", t, "pos")
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
                "    {   // T-450 (DRAFT, proposed): the carried line",
                "        .baseHP = %d," % hp, "        .baseAttack = %d," % at, "        .baseDefense = %d," % df,
                "        .baseSpeed = %d," % sp, "        .baseSpAttack = %d," % sa, "        .baseSpDefense = %d," % sd,
                "        .types = {TYPE_%s, TYPE_%s}," % i["types"], "        .catchRate = 45,", "        .expYield = %d," % i["exp"]] +
                ["        .evYield_%s = %d," % (k, v) for k, v in evs.items()] + [
                "        .itemCommon = ITEM_NONE,", "        .itemRare = ITEM_NONE,", "        .genderRatio = PERCENT_FEMALE(50),",
                "        .eggCycles = 20,", "        .friendship = 70,", "        .growthRate = GROWTH_MEDIUM_FAST,",
                "        .eggGroups = {EGG_GROUP_UNDISCOVERED, EGG_GROUP_UNDISCOVERED},",
                "        .abilities = {ABILITY_%s, ABILITY_%s}," % ABILITIES[name], "        .safariZoneFleeRate = 0,",
                "        .bodyColor = BODY_COLOR_GRAY,", "        .noFlip = FALSE,", "    }"])
            t, n = species_entry(t, "SPECIES_OLD_UNOWN_" + letter, "\n" + body)
            assert n == 1, letter
            t = re.sub(r"(\[SPECIES_OLD_UNOWN_%s\] =)\s*\{" % letter, r"\1\n    {", t, count=1)
        return t
    edit("src/data/pokemon/species_info.h", info)

    def lvl(t):
        for letter, name, *_ in LINE:
            sym = "sSpecies%dLevelUpLearnset" % (261 + "KLM".index(letter))
            body = "static const u16 %s[] = {   // T-450 (DRAFT, proposed): %s\n" % (sym, name) + \
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

    def evo(t):
        lines = ["    [SPECIES_OLD_UNOWN_%s] = {{%s, %s, SPECIES_OLD_UNOWN_%s}}," % (a, how, arg, b)
                 for a, (how, arg, b) in EVOLUTIONS.items()]
        return put_block(t, "    [SPECIES_SKITTY]", lines, after=False)
    edit("src/data/pokemon/evolution.h", evo)

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
                      '        .categoryName = _("%s"),   // T-450, DRAFT' % ENTRIES[name][0],
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
                lines += ["// T-450, DRAFT", "const u8 g%sPokedexText[] = _(" % ident] + \
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
    clean_art(report)
    footprints(report)
    changed, have = engine()
    for letter, name, *_ in LINE:
        h = have[letter]
        report.append("  %-10s %s" % (name, "front %dx%d y%d, back %dx%d y%d, icon palette %d" % (h[0] + h[1] + (h[2],))
                                       if h else "not built yet: run gbasprite.py --write, then this again"))
    for p in sorted(changed):
        report.append("  %s %s" % ("wrote" if WRITE else "would write", os.path.relpath(p, GBA)))
    if WRITE:
        for p, s in changed.items():
            open(p, "w").write(s)
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""THE NEXUS's residents: eight new daemons in the engine's unused species slots (T-395; docs/nexus.md).

    python3 tools/gbanexus.py            # report what it would change
    python3 tools/gbanexus.py --write    # the art (gfx/nexus/), then every engine table

WHY NEW, NOT RENAMED. The slots first proposed (ABSOL, JIRACHI ...) were already named daemons -- docs/still-vanilla.md
was stale. The user chose eight NEW daemons (2026-10-09). Gen 3 keeps 25 unused species, SPECIES_OLD_UNOWN_B..Z; B is
MISSINGNO (8.9), C..J become these eight. Each takes its type, stats, abilities and routines from the daemon it was
modelled on (MODEL below), so the type still says something true.

THE INDEX. They are INDEX 387-394, inserted before MISSINGNO, which moves from 387 to 395 -- still one past the end, so
8.9 holds: the register never lists it. NATIONAL_DEX_COUNT becomes the last of them. The save does not change shape:
its INDEX flags are sized by NUM_SPECIES (412), not the count.

THE ART is the exception to invariant 5 the user chose for the NEXUS: full natural colour, as paint, with the type's
colour emphasised. Front and back share one palette (Gen 3 has one per species): both cuts are quantised together to 15
colours, index 0 transparent. The shiny palette turns the hue a little; the icon takes whichever of the three icon
palettes fits it best. Source art: gfx/drafts/nexus/final64/ (approved 2026-10-09); this writes gfx/nexus/<name>/, the
art the build carries, then copies it into engineGba/graphics/pokemon/nexus_<name>/.

THE WORDS: the INDEX entries (approved 2026-10-09) and categories come from ENTRIES; OPUS's margins live in
tools/genmargins.py with the rest. Every in-game word is DRAFT until played.
"""
import colorsys, os, re, shutil, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SRC = os.path.join(ROOT, "gfx/drafts/nexus/final64")
ART = os.path.join(ROOT, "gfx/nexus")
WRITE = "--write" in sys.argv
BEGIN, END = "BEGIN gbanexus", "END gbanexus"

#  slot letter, name, ident, the daemon it is modelled on (stats, types, routines, height, weight), its cry
RESIDENTS = [
    ("C", "REFLECTION", "Reflection", "ABSOL",    "MIGHTYENA"),
    ("D", "LODESTAR",   "Lodestar",   "JIRACHI",  "STANTLER"),
    ("E", "PERIHELION", "Perihelion", "RAIKOU",   "RAIKOU"),
    ("F", "LYUBOV",     "Lyubov",     "ENTEI",    "ENTEI"),
    ("G", "MULTIMAL",   "Multimal",   "FEEBAS",   "MISDREAVUS"),
    ("H", "ILLUMINED",  "Illumined",  "MILOTIC",  "MILOTIC"),
    ("I", "LYNX",       "Lynx",       "SKITTY",   "SKITTY"),
    ("J", "BASTET",     "Bastet",     "DELCATTY", "PERSIAN"),
]
#  (evolves, how, into): MULTIMAL by friendship (Feebas's beauty cannot be raised in this game), LYNX by the MOON STONE
EVOLUTIONS = {"G": ("EVO_FRIENDSHIP", "0", "H"), "I": ("EVO_ITEM", "ITEM_MOON_STONE", "J")}
#  the INDEX entries (APPROVED by the user, 2026-10-09): category, CONTENT (FireRed's text), CONTEXT (LeafGreen's)
ENTRIES = {
    "REFLECTION": ("CANVAS",
        "It brings a painted mirror in its mouth to anyone lost in the night. Blank canvases come in many forms, it seems to say.",
        "The mirror reflects what its holder needs to learn. Held long enough, it is also a window into other worlds."),
    "LODESTAR": ("GUIDESTAR",
        "A familiar glow in the dark. In its light, fears calm, and the shapes that frightened you are seen to be friends.",
        "Those who once saw its light walk their own path after, sure of their footing even at night."),
    "PERIHELION": ("COMET",
        "It passes close only once in a long while. In that pass it teaches the lesson that stays: being different is good.",
        "Its pupils hardly saw it go. Long after, they still hear what it taught them, now in their own voices."),
    "LYUBOV": ("DEVOTION",
        "It sees others before they are willing to see themselves. It crosses great distances to visit, and asks nothing for the fare.",
        "Those it saw rarely see it in time. After, they mean more to it than they can ever express, and cannot say so."),
    "MULTIMAL": ("SHADOWS",
        "A shadow in the shapes of many animals: those someone tried to heal, but could not reach. A small light stays lit within.",
        "Those who walked away for their own well-being meet it again in the dark. Once they accept it, its shadow fades."),
    "ILLUMINED": ("RADIANT",
        "The light within it grew until it was all there was. It was always a friend. It was only that the night was dark.",
        "Near it, the ones who were afraid feel the strength of reconnection, and are no longer afraid."),
    "LYNX": ("FAMILIAR",
        "A small cat that seems somehow familiar. Its tufted ears hear what most cannot, and it never forgets a visitor.",
        "When a guest leaves, it waits by the door. It knows before they do who will be missed."),
    "BASTET": ("BOUNDLESS",
        "It sits as still as a temple statue. Those it watches begin to reach for more, and make things beyond their day's work.",
        "Its keepers learn that their only limits were ever the ones they imagined."),
}

_src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
_ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
exec(compile(_src.split("# ------------------------------------------------------- names, derived")[0], "port_vocab.py", "exec"), _ns)
width = _ns["textwidth"]
PANE_W, PANE_LINES = 234, 4


def wrap(text):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if cur and width(t) > PANE_W:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    return lines


def gpath(*p):
    return os.path.join(GBA, *p)


# ---- the art ------------------------------------------------------------------------------------------------------
def fit(cut, bottom_gap):
    """The cut-out, scaled to fit 62 px and set `bottom_gap` px above the 64 px frame's floor (alpha kept)."""
    a = cut.getchannel("A").point(lambda v: 255 if v > 40 else 0)
    sub = cut.crop(a.getbbox())
    s = 62 / max(sub.size)
    sub = sub.resize((max(1, round(sub.size[0] * s)), max(1, round(sub.size[1] * s))), Image.LANCZOS)
    c = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    c.alpha_composite(sub, ((64 - sub.size[0]) // 2, 64 - sub.size[1] - bottom_gap))
    return c


def shared_palette(front, back):
    """One 16-colour palette for both (index 0 transparent), and each image indexed against it."""
    both = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    both.alpha_composite(front, (0, 0)); both.alpha_composite(back, (64, 0))
    rgb = Image.new("RGB", both.size, (255, 255, 255)); rgb.paste(both, mask=both.getchannel("A"))
    q = rgb.quantize(colors=15, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:45]
    out = []
    for im, x0 in ((front, 0), (back, 64)):
        idx = Image.new("P", (64, 64), 0)
        src = q.crop((x0, 0, x0 + 64, 64)); al = im.getchannel("A")
        px, sp, ap = idx.load(), src.load(), al.load()
        for y in range(64):
            for x in range(64):
                px[x, y] = sp[x, y] + 1 if ap[x, y] > 110 else 0
        out.append(idx)
    colours = [(0, 0, 0)] + [tuple(pal[i:i + 3]) for i in range(0, 45, 3)]
    flat = [v for c in colours for v in c]
    for im in out:
        im.putpalette(flat + [0] * (768 - len(flat)))
    return out, colours


def shiny(colours):
    """The shiny palette: each colour's hue turned a little (index 0 kept)."""
    out = [colours[0]]
    for r, g, b in colours[1:]:
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        r2, g2, b2 = colorsys.hls_to_rgb((h + 0.11) % 1.0, l, s)
        out.append((round(r2 * 255), round(g2 * 255), round(b2 * 255)))
    return out


def jasc(colours):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in colours)


def read_jasc(path):
    lines = open(path).read().split()
    return [tuple(int(v) for v in lines[3 + i * 3:6 + i * 3]) for i in range(16)]


def icon(front):
    """The party icon: 32x32 twice (the second a pixel higher), in whichever icon palette fits best."""
    small = front.resize((32, 32), Image.LANCZOS)
    pals = [read_jasc(gpath("graphics/pokemon/icon_palettes/icon_palette_%d.pal" % i)) for i in range(3)]
    def err(p):
        e = 0
        for (r, g, b, a) in small.getdata():
            if a > 110:
                e += min((r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2 for c in p[1:])
        return e
    best = min(range(3), key=lambda i: err(pals[i]))
    p = pals[best]
    img = Image.new("P", (32, 64), 0)
    px = img.load()
    for y in range(32):
        for x in range(32):
            r, g, b, a = small.getpixel((x, y))
            if a > 110:
                k = 1 + min(range(15), key=lambda i: (r - p[i + 1][0]) ** 2 + (g - p[i + 1][1]) ** 2 + (b - p[i + 1][2]) ** 2)
                px[x, y] = k
                if y > 0:
                    px[x, 32 + y - 1] = k
    flat = [v for c in p for v in c]
    img.putpalette(flat + [0] * (768 - len(flat)))
    return img, best


def coords(img):
    """MON_COORDS: the opaque box rounded up to 8, and the empty rows below it."""
    box = img.point(lambda v: 255 if v else 0).getbbox()
    w = min(64, (box[2] - box[0] + 7) // 8 * 8)
    h = min(64, (box[3] - box[1] + 7) // 8 * 8)
    return w, h, 64 - box[3]


def make_art():
    made = {}
    for letter, name, ident, model, cry in RESIDENTS:
        n = name.lower()
        front = fit(Image.open(os.path.join(SRC, n + "_cut.png")).convert("RGBA"), 2)
        back = fit(Image.open(os.path.join(SRC, n + "_back_cut.png")).convert("RGBA"), 0)
        (fimg, bimg), colours = shared_palette(front, back)
        ico, ipal = icon(front)
        made[letter] = dict(front=fimg, back=bimg, normal=colours, shiny=shiny(colours), icon=ico, iconpal=ipal,
                            fcoords=coords(fimg), bcoords=coords(bimg))
    return made


def write_art(made, report):
    for letter, name, ident, model, cry in RESIDENTS:
        m, n = made[letter], name.lower()
        d = os.path.join(ART, n)
        os.makedirs(d, exist_ok=True)
        m["front"].save(os.path.join(d, "front.png")); m["back"].save(os.path.join(d, "back.png"))
        m["icon"].save(os.path.join(d, "icon.png"))
        #  and beside every other daemon's drawing, where the companion and the review sheets look
        for view in ("front", "back"):
            m[view].convert("RGBA").save(os.path.join(ROOT, "gfx/daemons", "%s_%s.png" % (n, view)))
        open(os.path.join(d, "normal.pal"), "w", newline="").write(jasc(m["normal"]))
        open(os.path.join(d, "shiny.pal"), "w", newline="").write(jasc(m["shiny"]))
        e = gpath("graphics/pokemon/nexus_" + n)
        os.makedirs(e, exist_ok=True)
        for f in ("front.png", "back.png", "icon.png", "normal.pal", "shiny.pal"):
            shutil.copyfile(os.path.join(d, f), os.path.join(e, f))
        model_fp = gpath("graphics/pokemon/%s/footprint.png" % model.lower())
        shutil.copyfile(model_fp, os.path.join(e, "footprint.png"))
    report.append("art: gfx/nexus/<name>/, gfx/daemons/<name>_front|back.png and engineGba/graphics/pokemon/nexus_<name>/ (8)")


# ---- the engine's tables -------------------------------------------------------------------------------------------
def block(lines):
    return ["// %s -- T-395, the NEXUS residents (tools/gbanexus.py writes this)" % BEGIN] + lines + ["// %s" % END]


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
    """Replace `[SPECIES_OLD_UNOWN_X] = ...,` (one line, or a braced block) with `[SPECIES_OLD_UNOWN_X] = body,`."""
    pat = re.compile(r"(\[%s\]\s*=\s*)(\{(?:[^{}]|\{[^{}]*\})*\}|[^\n]*?)(,)" % re.escape(key))
    new, n = pat.subn(lambda m: m.group(1) + body + m.group(3), text, count=1)
    return new, n


def braced(text, key):
    """The `{...}` body of `[key] = {...}` in text."""
    m = re.search(r"\[%s\]\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\})" % re.escape(key), text)
    return m.group(1) if m else None


def engine(made):
    changed = {}
    def edit(path, fn):
        p = gpath(path)
        old = open(p).read()
        new = fn(old)
        if new != old:
            changed[p] = new

    # the species' own names for the slots
    edit("include/constants/species.h", lambda t: put_block(t, "#define SPECIES_OLD_UNOWN_Z",
         ["#define SPECIES_%s SPECIES_OLD_UNOWN_%s" % (name, letter) for letter, name, *_ in RESIDENTS]))

    # the INDEX numbers: the eight after DEOXYS, MISSINGNO (OLD_UNOWN_B) after them; the count is the last of them
    def dex(t):
        names = ["    NATIONAL_DEX_%s," % name for _, name, *_ in RESIDENTS]
        t = put_block(t, "    NATIONAL_DEX_DEOXYS,", names)
        return re.sub(r"#define NATIONAL_DEX_COUNT\s+NATIONAL_DEX_\w+",
                      "#define NATIONAL_DEX_COUNT  NATIONAL_DEX_%s" % RESIDENTS[-1][1], t)
    edit("include/constants/pokedex.h", dex)

    # species -> INDEX number
    def to_nat(t):
        for letter, name, *_ in RESIDENTS:     # SPECIES_TO_NATIONAL(OLD_UNOWN_C) -> NATIONAL_DEX_REFLECTION (once)
            t = t.replace("SPECIES_TO_NATIONAL(OLD_UNOWN_%s)" % letter, "NATIONAL_DEX_%s" % name, 1)
        return t
    edit("src/pokemon.c", to_nat)

    # the cries: the slots borrow Unown's; these eight borrow a creature's that suits them
    def cries(t):
        lines = ["static const u16 sNexusCries[] = {"] + \
                ["    [SPECIES_%s - SPECIES_OLD_UNOWN_C] = SPECIES_%s," % (name, cry) for _, name, _, _, cry in RESIDENTS] + \
                ["};"]
        t = put_block(t, "u16 SpeciesToCryId(u16 species)", lines, after=False)
        if "sNexusCries[species" not in t:
            t = t.replace("    if (species <= SPECIES_OLD_UNOWN_Z - 1)\n        return SPECIES_UNOWN - 1;",
                          "    if (species >= SPECIES_OLD_UNOWN_C - 1 && species <= SPECIES_OLD_UNOWN_J - 1)   // T-395\n"
                          "        return SpeciesToCryId(sNexusCries[species - (SPECIES_OLD_UNOWN_C - 1)] - 1);\n"
                          "    if (species <= SPECIES_OLD_UNOWN_Z - 1)\n        return SPECIES_UNOWN - 1;", 1)
        return t
    edit("src/pokemon.c", lambda t: cries(changed.get(gpath("src/pokemon.c"), t)))

    # the item and TM animation's placing (menu2.c): the slots' rows belong to SYMBOL's letters C..J, which still
    # use them, so the eight read their model's row instead
    def pos(t):
        lines = ["static const u16 sNexusPosModel[] = {"] + \
                ["    [SPECIES_%s - SPECIES_OLD_UNOWN_C] = SPECIES_%s," % (name, model) for _, name, _, model, _ in RESIDENTS] + \
                ["};", ""]
        t = put_block(t, "u8 Menu2_GetMonPosAttribute(u16 species, u32 personality, u8 attributeId)", lines, after=False)
        if "sNexusPosModel[species" not in t:
            t = t.replace("    }\n    if (species != SPECIES_NONE && attributeId < PSA_MON_ATTR_COUNT)",
                          "    }\n    else if (species >= SPECIES_OLD_UNOWN_C && species <= SPECIES_OLD_UNOWN_J)   // T-395\n"
                          "        species = sNexusPosModel[species - SPECIES_OLD_UNOWN_C];\n"
                          "    if (species != SPECIES_NONE && attributeId < PSA_MON_ATTR_COUNT)", 1)
        return t
    edit("src/menu2.c", pos)

    # names
    def names(t):
        for letter, name, *_ in RESIDENTS:
            t = re.sub(r'(\[SPECIES_OLD_UNOWN_%s\]\s*=\s*_\(")[^"]*("\))' % letter, r"\g<1>%s\g<2>" % name, t)
        return t
    edit("src/data/text/species_names.h", names)

    # stats, types, abilities: the model's, under the slot
    def info(t):
        for letter, name, ident, model, cry in RESIDENTS:
            body = braced(t, "SPECIES_" + model)
            t, n = species_entry(t, "SPECIES_OLD_UNOWN_" + letter, body)
            assert n == 1, letter
        return t
    edit("src/data/pokemon/species_info.h", info)

    # routines: the model's level-up list and PLUGINs
    def lvl(t):
        for letter, name, ident, model, cry in RESIDENTS:
            src = re.search(r"\[SPECIES_%s\]\s*=\s*(\w+)," % model, t).group(1)
            t, n = species_entry(t, "SPECIES_OLD_UNOWN_" + letter, src)
            assert n == 1, letter
        return t
    edit("src/data/pokemon/level_up_learnset_pointers.h", lvl)

    def tmhm(t):
        for letter, name, ident, model, cry in RESIDENTS:
            m = re.search(r"\[SPECIES_%s\]\s*=\s*(TMHM_LEARNSET\((?:[^()]|\([^()]*\))*\))," % model, t)
            t = re.sub(r"\[SPECIES_OLD_UNOWN_%s\]\s*=\s*TMHM_LEARNSET\((?:[^()]|\([^()]*\))*\)," % letter,
                       lambda _: "[SPECIES_OLD_UNOWN_%s] = %s," % (letter, m.group(1)), t, count=1)
        return t
    edit("src/data/pokemon/tmhm_learnsets.h", tmhm)

    # evolutions
    def evo(t):
        lines = ["    [SPECIES_OLD_UNOWN_%s] = {{%s, %s, SPECIES_OLD_UNOWN_%s}}," % (a, how, arg, b)
                 for a, (how, arg, b) in EVOLUTIONS.items()]
        return put_block(t, "    [SPECIES_SKITTY]", lines, after=False)
    edit("src/data/pokemon/evolution.h", evo)

    # the sprites: data, then every table that points at it
    def gfxdata(t):
        lines = []
        for letter, name, ident, *_ in RESIDENTS:
            d = "graphics/pokemon/nexus_" + name.lower()
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
        for letter, name, ident, *_ in RESIDENTS:
            lines += ["extern const u32 gMonFrontPic_%s[];" % ident, "extern const u32 gMonBackPic_%s[];" % ident,
                      "extern const u32 gMonPalette_%s[];" % ident, "extern const u32 gMonShinyPalette_%s[];" % ident,
                      "extern const u8 gMonIcon_%s[];" % ident, "extern const u8 gMonFootprint_%s[];" % ident]
        return put_block(t, "extern const u32 gMonFrontPic_Absol[];", lines, after=False)
    edit("include/graphics.h", externs)

    def macro_table(path, macro, symbol):
        def fn(t):
            for letter, name, ident, *_ in RESIDENTS:
                t = re.sub(r"%s\(OLD_UNOWN_%s,\s*\w+\)" % (macro, letter), "%s(OLD_UNOWN_%s, %s_%s)" % (macro, letter, symbol, ident), t)
            return t
        edit(path, fn)
    macro_table("src/data/pokemon_graphics/front_pic_table.h", "SPECIES_SPRITE", "gMonFrontPic")
    macro_table("src/data/pokemon_graphics/back_pic_table.h", "SPECIES_SPRITE", "gMonBackPic")
    macro_table("src/data/pokemon_graphics/palette_table.h", "SPECIES_PAL", "gMonPalette")
    macro_table("src/data/pokemon_graphics/shiny_palette_table.h", "SPECIES_SHINY_PAL", "gMonShinyPalette")

    def keyed(path, valuefn):
        def fn(t):
            for letter, name, ident, *_ in RESIDENTS:
                t, n = species_entry(t, "SPECIES_OLD_UNOWN_" + letter, valuefn(letter, ident))
                assert n == 1, (path, letter)
            return t
        edit(path, fn)
    keyed("src/data/pokemon_graphics/footprint_table.h", lambda l, i: "gMonFootprint_" + i)
    keyed("src/data/pokemon_graphics/front_pic_coordinates.h",
          lambda l, i: "{\n        .size = MON_COORDS_SIZE(%d, %d),\n        .y_offset = %d,\n    }" % made[l]["fcoords"])
    keyed("src/data/pokemon_graphics/back_pic_coordinates.h",
          lambda l, i: "{\n        .size = MON_COORDS_SIZE(%d, %d),\n        .y_offset = %d,\n    }" % made[l]["bcoords"])

    def icons(t):
        for letter, name, ident, *_ in RESIDENTS:
            t = re.sub(r"(\[SPECIES_OLD_UNOWN_%s\]\s*=\s*)gMonIcon_\w+," % letter, r"\g<1>gMonIcon_%s," % ident, t, count=1)
            t = re.sub(r"(\[SPECIES_OLD_UNOWN_%s\]\s*=\s*)\d," % letter, r"\g<1>%d," % made[letter]["iconpal"], t, count=1)
        return t
    edit("src/pokemon_icon.c", icons)

    # the INDEX: entries (the model's height, weight and scale), both editions' words, and the four orders
    def entries(t):
        lines = []
        for letter, name, ident, model, cry in RESIDENTS:
            mb = braced(t, "NATIONAL_DEX_" + model)
            g = lambda f: re.search(r"\.%s\s*=\s*(-?\d+)" % f, mb).group(1)
            lines += ["    [NATIONAL_DEX_%s] =" % name, "    {",
                      '        .categoryName = _("%s"),' % ENTRIES[name][0],
                      "        .height = %s," % g("height"), "        .weight = %s," % g("weight"),
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
            for letter, name, ident, *_ in RESIDENTS:
                text = ENTRIES[name][1 if which == "fr" else 2]
                ls = wrap(text)
                assert len(ls) <= PANE_LINES, name
                lines += ["const u8 g%sPokedexText[] = _(" % ident] + \
                         ['    "%s%s"%s' % (l, "\\n" if i < len(ls) - 1 else "", ");" if i == len(ls) - 1 else "")
                          for i, l in enumerate(ls)] + [""]
            return put_block(t, "const u8 gAbsolPokedexText[]", lines, after=False)
        return fn
    edit("src/data/pokemon/pokedex_text_fr.h", dextext("fr"))
    edit("src/data/pokemon/pokedex_text_lg.h", dextext("lg"))

    def orders(t):
        for letter, name, ident, model, cry in RESIDENTS:
            if "NATIONAL_DEX_%s," % name in t:
                continue
            t = re.sub(r"(\n(\s*)NATIONAL_DEX_%s,)" % model,
                       lambda m: m.group(1) + "\n" + m.group(2) + "NATIONAL_DEX_%s," % name, t)
        return t
    edit("src/data/pokemon/pokedex_orders.h", orders)
    return changed


def main():
    report = []
    for letter, name, *_ in RESIDENTS:
        assert len(name) <= 10 and len(ENTRIES[name][0]) <= 11, name
        for t in ENTRIES[name][1:]:
            assert len(wrap(t)) <= PANE_LINES, name
    made = make_art()
    for letter, name, *_ in RESIDENTS:
        m = made[letter]
        report.append("  %-10s front %dx%d y%d, back %dx%d y%d, icon palette %d" % ((name,) + m["fcoords"] + m["bcoords"] + (m["iconpal"],)))
    changed = engine(made)
    for p in sorted(changed):
        report.append("  %s %s" % ("wrote" if WRITE else "would write", os.path.relpath(p, GBA)))
    if WRITE:
        write_art(made, report)
        for p, s in changed.items():
            open(p, "w").write(s)
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())

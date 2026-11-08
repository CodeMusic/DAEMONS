#!/usr/bin/env python3
"""T-532: the MUSAI branch keeps the seasons -- 18 picture-only forms, and the tables that point at them.

    python3 tools/genmusaiseasons.py              # report: each form's files and table blocks, final or placeholder
    python3 tools/genmusaiseasons.py --write      # write the form folders and the generated blocks into engineGba/
    python3 tools/genmusaiseasons.py --list       # one line per form: its species id, folder and where its art is from

WHAT IT IS (vision 9.34; the user's decisions 2026-11-08). The six MUSAI -- MUSAI, CODEMUSAI, SEEKMUSAI, CAREMUSAI,
LENSMUSAI, MASKMUSAI (the EEVEE, FLAREON, JOLTEON, VAPOREON, ESPEON and UMBREON slots) -- each wear the season
DaemonsSeason() gives them, Unown's way: one species, its PICTURE chosen when it is drawn. The SUMMER form is each
species' own art (9.21: summer is "the world as drawn"), so 18 picture-only ids are added after SPECIES_UNOWN_QMARK,
winter, spring and autumn for each. src/daemons_seasons.c's DaemonsSeasonalSpecies() turns a species into its form for
the pic loaders, the two sprite-palette look-ups and GetIconSpecies; the species never changes, so the save, the INDEX's
counts, trades, evolution, stats and the companion's ids are untouched. Look only: no stat moves with the season.

WHAT IT WRITES

  graphics/pokemon/<slot>/<season>/  front.png, back.png, icon.png, normal.pal, shiny.pal  (follower.png is
                                     tools/gbafollower.py's, from these; the follower's colours gbafollowerpal.py's)
  include/constants/species.h        SPECIES_<SLOT>_<SEASON> (NUM_SPECIES + 28 ...)
  include/graphics.h                 the externs
  src/data/graphics/pokemon.h        the INCBINs
  src/data/pokemon_graphics/{front_pic,back_pic,palette,shiny_palette}_table.h
                                     one row per form. NOT through SPECIES_SPRITE / SPECIES_PAL: the palette rows keep the
                                     BASE species' tag, so a form loads under the tag every caller already asks for,
                                     and the tools that read those macros (genstreaks) never take a form for a species
  src/pokemon_icon.c                 gMonIconTable and gMonIconPaletteIndices (each form in its base's shared palette:
                                     CreateMonIcon picks the palette by the REAL species)
  src/data/pokemon/musai_seasons.h   the branch and its forms, by season, for daemons_seasons.c
  src/data/pokemon_graphics/{front,back}_pic_coordinates.h
                                     each form's own MON_COORDS row, measured off its picture (T-452's grounding rule:
                                     the box rounded up to 8, y_offset 63 - the lowest row), and each of the six
                                     species' own row re-measured off the built front/back (its summer); the engine reads
                                     every coordinates row through DaemonsSeasonalSpecies(), so a form taller or lower
                                     for its vehicle still stands on the battle platform. None floats: no elevation.
  gfx/daemons/<name>_{front,back,icon}.png   an APPROVED summer's drawings, copied from finals/ (gbasprite's sources)

  Each block sits between "BEGIN genmusaiseasons" and "END genmusaiseasons" lines; a re-run replaces only that.

WHERE EACH FORM'S ART COMES FROM -- and APPROVED_FINAL (below) decides which finals are used at all: a drawing in
finals/ that is not on that list stays a placeholder (the user, 2026-11-08: "Build, redraw the weak").

  FINAL       gfx/drafts/t532_musai_seasons/finals/<name>_<season>_front.png -- an RGBA drawing as every redrawn
              daemon's gfx/daemons/<name>_front.png is (gbasprite's place_rich input), drawn in the base's TYPE ramp
              (invariant 5: the season is only what it wears). Beside it, optionally, _back.png (else the species' own
              back drawing, through the form's palette) and _icon.png (a drawn 32x64 icon in a shared icon palette, as
              gbasprite.drawn_icon reads; else derived from the front). The icon is mapped into the BASE's shared icon
              palette whichever it was drawn in. shiny.pal is genshiny.make_shiny's, inside the type (T-432). Palette
              entries 11-14 stay the streak grey, so the streaks, saturation and SPIRITS paint on a form exactly as on
              its species: they work on the loaded palette, keyed by the real species (T-475 cannot recur -- there is
              no second palette path).
  PLACEHOLDER no final: a byte-for-byte copy of the species' own front, back, icon and palettes (today's art), so the
              swap is wired, filmable and costs its real ROM before the art arrives.

  SUMMER      is the species' own art, gbasprite.py's, from gfx/daemons/<name>_{front,back,icon}.png. An APPROVED
              summer final is copied there by --write ("Yes, all five", 2026-11-08: CODEMUSAI, SEEKMUSAI, CAREMUSAI,
              LENSMUSAI; MASKMUSAI's waits for its redraw; MUSAI's ROM art stands), and then reaches the ROM the way
              every redrawn daemon does. A placeholder form is a copy of whatever the species' art is now.

SWAPPING IN A REDRAW: put finals/<name>_<season>_{front,back,icon}.png in place, add (NAME, season) to APPROVED_FINAL,
then, from the repo root:  genmusaiseasons.py --write;  gbasprite.py --write (only if a summer was copied: it says
so);  genmusaiseasons.py --write again;  gbafollower.py --write;  gbafollowerpal.py --write;  build;
companion_export.py --write. Every report must then be quiet.
"""
import contextlib, io, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
FINALS = os.path.join(ROOT, "gfx", "drafts", "t532_musai_seasons", "finals")
DAEMONS = os.path.join(ROOT, "gfx", "daemons")
ARGS = sys.argv[1:]
WRITE = "--write" in ARGS
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#  (the name the player reads, the slot's folder, the slot's constant stem, its symbol stem, its type)
BRANCH = [("MUSAI", "eevee", "EEVEE", "Eevee", "NORMAL"),
          ("CODEMUSAI", "flareon", "FLAREON", "Flareon", "FIGHTING"),
          ("SEEKMUSAI", "jolteon", "JOLTEON", "Jolteon", "FLYING"),
          ("CAREMUSAI", "vaporeon", "VAPOREON", "Vaporeon", "PSYCHIC"),
          ("LENSMUSAI", "espeon", "ESPEON", "Espeon", "PSYCHIC"),
          ("MASKMUSAI", "umbreon", "UMBREON", "Umbreon", "DARK")]
SEASONS = ["winter", "spring", "summer", "autumn"]      # SEASON_WINTER .. SEASON_AUTUMN (daemons_time.h)
FORM_SEASONS = ["winter", "spring", "autumn"]           # summer is the species' own picture
FIRST = 28                                              # SPECIES_UNOWN_QMARK is NUM_SPECIES + 27
FILES = ("front.png", "back.png", "icon.png", "normal.pal", "shiny.pal")
TAG = "genmusaiseasons"


def forms():
    """[(name, slot dir, const stem, symbol stem, type, season, SPECIES_X_SEASON, id offset)] in id order."""
    out, n = [], FIRST
    for name, d, c, s, t in BRANCH:
        for season in FORM_SEASONS:
            out.append((name, d, c, s, t, season, "SPECIES_%s_%s" % (c, season.upper()), n))
            n += 1
    return out


def form_species():
    """{SPECIES_X_SEASON: (SPECIES_X, season)} -- for the tools that meet a form in gMonIconTable (gbafollower)."""
    return {f[6]: ("SPECIES_" + f[2], f[5]) for f in forms()}


#  THE FINALS THE USER APPROVED (the user, 2026-11-08: "Build, redraw the weak"; and "Yes, all five" summers). A form
#  is built from its drawing in finals/ ONLY if it is named here; anything else stays a placeholder (today's art) even
#  when its files exist, so a redraw is swapped in by dropping it into finals/ and adding it here -- nothing else.
#  Waiting on the redraw, 2026-11-08: MASKMUSAI's four (summer too), SEEKMUSAI autumn, LENSMUSAI autumn, CODEMUSAI
#  winter and autumn. A SUMMER here is copied over the species' own drawings in gfx/daemons/ (gbasprite's sources):
#  summer IS the species' art, so it reaches the ROM through gbasprite.py like every redrawn daemon (MUSAI's summer is
#  its ROM art, which stands).
APPROVED_FINAL = {
    ("MUSAI", "winter"), ("MUSAI", "spring"), ("MUSAI", "autumn"),
    ("CODEMUSAI", "spring"), ("CODEMUSAI", "summer"),
    ("SEEKMUSAI", "winter"), ("SEEKMUSAI", "spring"), ("SEEKMUSAI", "summer"),
    ("CAREMUSAI", "winter"), ("CAREMUSAI", "spring"), ("CAREMUSAI", "summer"), ("CAREMUSAI", "autumn"),
    ("LENSMUSAI", "winter"), ("LENSMUSAI", "spring"), ("LENSMUSAI", "summer"),
}
SUMMER_KINDS = ("front", "back", "icon")                # finals/<name>_summer_<kind>.png -> gfx/daemons/<name>_<kind>.png


def final_front(name, season):
    """The approved final front drawing for NAME in SEASON, or None (not approved, or not drawn yet)."""
    if (name, season) not in APPROVED_FINAL:
        return None
    p = os.path.join(FINALS, "%s_%s_front.png" % (name.lower(), season))
    return p if os.path.exists(p) else None


def summer_copies():
    """[(finals source, gfx/daemons target)] for every approved summer, each kind that was drawn."""
    out = []
    for name, *_ in BRANCH:
        if not final_front(name, "summer"):
            continue
        for kind in SUMMER_KINDS:
            src = os.path.join(FINALS, "%s_summer_%s.png" % (name.lower(), kind))
            if os.path.exists(src):
                out.append((src, os.path.join(DAEMONS, "%s_%s.png" % (name.lower(), kind))))
    return out


def final_of(species_form):
    """The final front drawing for SPECIES_X_SEASON, or None while it is a placeholder (gbafollower reduces it)."""
    for f in forms():
        if f[6] == species_form:
            return final_front(f[0], f[5])
    return None


# ------------------------------------------------------------------------------------------------ the pictures

def _G():
    argv, sys.argv = sys.argv, [sys.argv[0]]     # gbasprite runs its report on import, and reads --write (engine.md 16)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import gbasprite as G
    finally:
        sys.argv = argv
    return G


def icon_palette_index(stem):
    src = open(os.path.join(GBA, "src", "pokemon_icon.c"), encoding="utf-8").read()
    idx = src.split("const u8 gMonIconPaletteIndices[] = {", 1)[1].split("};", 1)[0]
    return int(dict(re.findall(r"\[(SPECIES_\w+)\]\s*=\s*(\d+)", idx))["SPECIES_" + stem])


def to_icon_palette(grid, have, want, pals):
    """An icon drawn (or derived) in shared palette HAVE, re-indexed into WANT by nearest colour (index 0 stays 0)."""
    if have == want:
        return grid
    src, dst = pals[have], pals[want]
    m = {0: 0}
    for i in range(1, 16):
        m[i] = 1 + min(range(15), key=lambda k: sum((a - b) ** 2 for a, b in zip(src[i], dst[k + 1])))
    return [[m[v] for v in row] for row in grid]


def final_files(f):
    """{file name: bytes-to-compare-or-writer} for a FINAL form: (kind, payload)."""
    import genshiny
    G = _G()
    name, d, c, s, t, season = f[:6]
    rgb = G.TYPE_COLOR[t]
    front, pal = G.place_rich(final_front(name, season), rgb)
    back_src = os.path.join(FINALS, "%s_%s_back.png" % (name.lower(), season))
    if not os.path.exists(back_src):
        back_src = G.rich_src(name, "back")
    back, _ = G.place_rich(back_src, rgb, shared=pal)
    pal = list(pal) + [(0, 0, 0)] * (16 - len(pal))
    _t, shiny = genshiny.make_shiny(pal)
    want = icon_palette_index(c)
    pals = G.icon_palettes()
    drawn = os.path.join(FINALS, "%s_%s_icon.png" % (name.lower(), season))
    if os.path.exists(drawn):
        icon, (pi, _e) = G.drawn_icon(drawn)
    else:
        icon, (pi, _e) = G.derive_icon(front, pal)
    icon = to_icon_palette(icon, pi, want, pals)
    return {"front.png": ("png", (front, pal, 64, 64)), "back.png": ("png", (back, pal, 64, 64)),
            "icon.png": ("png", (icon, pals[want], 32, 64)), "normal.pal": ("pal", pal),
            "shiny.pal": ("pal", shiny if shiny is not None else pal)}


def png_bytes(grid, pal, w, h):
    G = _G()
    tmp = os.path.join(_scratch(), "g.png")
    G.write_png4(tmp, grid, pal, w, h)
    return open(tmp, "rb").read()


def pal_bytes(pal):
    import daemonslib
    tmp = os.path.join(_scratch(), "g.pal")
    daemonslib.write_pal(tmp, pal, pad=True)
    return open(tmp, "rb").read()


def _scratch():
    import tempfile
    global _TMP
    try:
        return _TMP
    except NameError:
        _TMP = tempfile.mkdtemp(prefix="genmusaiseasons")
        return _TMP


def wanted_files(f):
    """{file name: bytes} for one form folder, and how it was made."""
    name, d, season = f[0], f[1], f[5]
    if final_front(name, season):
        out = {}
        for k, (kind, v) in final_files(f).items():
            out[k] = png_bytes(*v) if kind == "png" else pal_bytes(v)
        return out, "final"
    base = os.path.join(GBA, "graphics", "pokemon", d)
    return {k: open(os.path.join(base, k), "rb").read() for k in FILES}, "placeholder"


def feet(path):
    """(lowest opaque row, height) of a 64x64 indexed front, for the feet-line check."""
    from PIL import Image
    im = Image.open(path)
    px = im.load()
    rows = [y for y in range(im.size[1]) if any(px[x, y] for x in range(im.size[0]))]
    return (rows[-1], rows[-1] - rows[0] + 1) if rows else (0, 0)


def coords(png):
    """MON_COORDS of a 64x64 indexed picture (a path or PNG bytes), T-452's grounding rule (gfx/drafts/t452/scripts/
    ground.py, as every redrawn daemon's row was made): .size the opaque box rounded up to 8 each way, .y_offset 63 -
    the lowest opaque row -- so the feet sit on the frame's bottom row, on the battle platform, however tall the
    vehicle makes the form. None of the branch floats (tools/daemon_float.json lifts none of them), so no elevation."""
    from PIL import Image
    im = Image.open(io.BytesIO(png) if isinstance(png, bytes) else png)
    px = im.load()
    w = im.size[0]
    pts = [(x, y) for y in range(min(64, im.size[1])) for x in range(w) if px[x, y]]
    if not pts:
        return (64, 64, 0)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    up = lambda v: min(64, (v + 7) // 8 * 8)
    return (up(max(xs) - min(xs) + 1), up(max(ys) - min(ys) + 1), 63 - max(ys))


COORD_TABLES = (("front", "src/data/pokemon_graphics/front_pic_coordinates.h"),
                ("back", "src/data/pokemon_graphics/back_pic_coordinates.h"))


def coord_row(sp, c, indent="    "):
    return ["%s[%s] =" % (indent, sp), "%s{" % indent, "%s    .size = MON_COORDS_SIZE(%d, %d)," % (indent, c[0], c[1]),
            "%s    .y_offset = %d," % (indent, c[2]), "%s}," % indent]


def set_base_row(text, sp, c):
    """Rewrite SP's own row in a coordinates table (outside the block: it is the species' row, summer's picture)."""
    pat = re.compile(r"(\[%s\] =\s*\{\s*\.size = MON_COORDS_SIZE\()\d+, \d+(\),\s*\.y_offset = )\d+" % sp)
    if not pat.search(text):
        raise SystemExit("genmusaiseasons: no coordinates row for %s" % sp)
    return pat.sub(lambda m: "%s%d, %d%s%d" % (m.group(1), c[0], c[1], m.group(2), c[2]), text, count=1)


# ------------------------------------------------------------------------------------------------ the tables

def block(lines, indent=""):
    return ["%s// BEGIN %s (T-532) -- generated by DAEMONS tools/genmusaiseasons.py; do not edit by hand" % (indent, TAG)] \
        + lines + ["%s// END %s" % (indent, TAG)]


def put(text, anchor, lines, before=False):
    """Replace the generated block, or put it after (before=False) or before the line holding ANCHOR."""
    pat = re.compile(r"[ \t]*// BEGIN %s .*?\n.*?// END %s[^\n]*\n" % (TAG, TAG), re.S)
    body = "\n".join(lines) + "\n"
    if pat.search(text):
        return pat.sub(lambda _: body, text, count=1)
    i = text.index(anchor)
    if before:
        j = text.rfind("\n", 0, i) + 1
        return text[:j] + body + text[j:]
    j = text.index("\n", i) + 1
    return text[:j] + body + text[j:]


def tables(pictures=None):
    """{engine-relative path: new text} for every generated block. PICTURES is {SPECIES_X_SEASON: {"front": bytes,
    "back": bytes}}, the form pictures as they will be written (their coordinates rows are measured off them)."""
    fs = forms()
    out = {}
    if pictures is None:
        pictures = {f[6]: wanted_files(f)[0] for f in fs}

    def edit(rel, fn):
        p = os.path.join(GBA, rel)
        out[rel] = fn(open(p, encoding="utf-8").read())

    edit("include/constants/species.h", lambda t: put(t, "#define SPECIES_UNOWN_QMARK", block(
        ["// T-532: the MUSAI branch's seasonal pictures, Unown's way -- picture-only ids, never a species a daemon is.",
         "// Summer is each species' own picture; DaemonsSeasonalSpecies() (src/daemons_seasons.c) picks the rest."]
        + ["#define %-30s (NUM_SPECIES + %d)" % (f[6], f[7]) for f in fs]
        + ["#define SPECIES_MUSAI_SEASONS_FIRST %s" % fs[0][6], "#define SPECIES_MUSAI_SEASONS_LAST  %s" % fs[-1][6]])))

    def sym(f):
        return f[3] + f[5].capitalize()

    edit("include/graphics.h", lambda t: put(t, "extern const u8 gMonIcon_UnownQuestionMark[];", block(
        sum([["extern const u32 gMonFrontPic_%s[];" % sym(f), "extern const u32 gMonBackPic_%s[];" % sym(f),
              "extern const u32 gMonPalette_%s[];" % sym(f), "extern const u32 gMonShinyPalette_%s[];" % sym(f),
              "extern const u8 gMonIcon_%s[];" % sym(f)] for f in fs], []))))

    edit("src/data/graphics/pokemon.h", lambda t: put(t, "const u8 gMonIcon_UnownQuestionMark[]", block(
        sum([['const u32 gMonFrontPic_%s[] = INCBIN_U32("graphics/pokemon/%s/%s/front.4bpp.lz");' % (sym(f), f[1], f[5]),
              'const u32 gMonBackPic_%s[] = INCBIN_U32("graphics/pokemon/%s/%s/back.4bpp.lz");' % (sym(f), f[1], f[5]),
              'const u32 gMonPalette_%s[] = INCBIN_U32("graphics/pokemon/%s/%s/normal.gbapal.lz");' % (sym(f), f[1], f[5]),
              'const u32 gMonShinyPalette_%s[] = INCBIN_U32("graphics/pokemon/%s/%s/shiny.gbapal.lz");' % (sym(f), f[1], f[5]),
              'const u8 gMonIcon_%s[] = INCBIN_U8("graphics/pokemon/%s/%s/icon.4bpp");' % (sym(f), f[1], f[5])]
             for f in fs], []))))

    def row_table(rel, anchor, fmt):
        edit(rel, lambda t: put(t, anchor, block(["    " + fmt(f) for f in fs], "    ")))

    row_table("src/data/pokemon_graphics/front_pic_table.h", "SPECIES_SPRITE(UNOWN_QMARK,",
              lambda f: "[%s] = {gMonFrontPic_%s, 0x800, SPECIES_%s}," % (f[6], sym(f), f[2]))
    row_table("src/data/pokemon_graphics/back_pic_table.h", "SPECIES_SPRITE(UNOWN_QMARK,",
              lambda f: "[%s] = {gMonBackPic_%s, 0x800, SPECIES_%s}," % (f[6], sym(f), f[2]))
    row_table("src/data/pokemon_graphics/palette_table.h", "SPECIES_PAL(UNOWN_QMARK,",
              lambda f: "[%s] = {gMonPalette_%s, SPECIES_%s},   // the base's tag" % (f[6], sym(f), f[2]))
    row_table("src/data/pokemon_graphics/shiny_palette_table.h", "SPECIES_SHINY_PAL(UNOWN_QMARK,",
              lambda f: "[%s] = {gMonShinyPalette_%s, SPECIES_%s + SPECIES_SHINY_TAG}," % (f[6], sym(f), f[2]))

    #  T-532 coords (the user, 2026-11-08): each form its own front and back row, measured off its own picture -- the
    #  battle reads them through DaemonsSeasonalSpecies() (battle_anim_mons.c, battle_main.c ...), as it reads the
    #  pictures; and each species' own row (its summer picture) measured off the built front/back gbasprite wrote.
    for kind, rel in COORD_TABLES:
        def coord_edit(t, kind=kind):
            for name, d, c, s, ty in BRANCH:
                t = set_base_row(t, "SPECIES_" + c, coords(os.path.join(GBA, "graphics", "pokemon", d, kind + ".png")))
            rows = sum([coord_row(f[6], coords(pictures[f[6]][kind + ".png"])) for f in fs], [])
            return put(t, "};", block(rows, "    "), before=True)
        edit(rel, coord_edit)

    def icons(t):
        t = re.sub(r"(\[SPECIES_UNOWN_QMARK\]\s*=\s*gMonIcon_UnownQuestionMark)\n", r"\1,\n", t, count=1)
        t = re.sub(r"(\[SPECIES_UNOWN_QMARK\]\s*=\s*1)\n", r"\1,\n", t, count=1)
        head, rest = t.split("const u8 gMonIconPaletteIndices[] = {", 1)
        head = put(head, "[SPECIES_UNOWN_QMARK] = gMonIcon_UnownQuestionMark",
                   block(["    [%s] = gMonIcon_%s," % (f[6], sym(f)) for f in fs], "    "))
        idx, tail = rest.split("};", 1)
        idx = put(idx, "[SPECIES_UNOWN_QMARK] = 1",
                  block(["    [%s] = %d," % (f[6], icon_palette_index(f[2])) for f in fs], "    "))
        return head + "const u8 gMonIconPaletteIndices[] = {" + idx + "};" + tail
    edit("src/pokemon_icon.c", icons)

    lines = ["//  GENERATED by DAEMONS tools/genmusaiseasons.py (T-532) -- do not edit; run the tool.",
             "//  The MUSAI branch and each one's picture for SEASON_WINTER .. SEASON_AUTUMN (summer is its own).", "",
             "static const u16 sMusaiBranch[] = {"]
    lines += ["    SPECIES_%s,   // %s" % (c, name) for name, d, c, s, t in BRANCH]
    lines += ["};", "", "static const u16 sMusaiSeasonForms[][SEASON_COUNT] = {"]
    for name, d, c, s, t in BRANCH:
        cells = ["SPECIES_%s" % c if se == "summer" else "SPECIES_%s_%s" % (c, se.upper()) for se in SEASONS]
        lines.append("    {%s},   // %s" % (", ".join(cells), name))
    lines += ["};", ""]
    out["src/data/pokemon/musai_seasons.h"] = "\n".join(lines)
    return out


# ------------------------------------------------------------------------------------------------ main

def main():
    fs = forms()
    if "--list" in ARGS:
        for f in fs:
            print("  %-26s NUM_SPECIES+%d  graphics/pokemon/%s/%s  %s" % (f[6], f[7], f[1], f[5],
                  "final " + final_front(f[0], f[5]) if final_front(f[0], f[5]) else "placeholder (today's art)"))
        return 0
    changed = 0
    finals = 0
    summer = [n for n, *_ in BRANCH if final_front(n, "summer")]
    plan = []
    for f in fs:
        files, how = wanted_files(f)
        finals += how == "final"
        d = os.path.join(GBA, "graphics", "pokemon", f[1], f[5])
        diff = [k for k, v in files.items() if not os.path.exists(os.path.join(d, k))
                or open(os.path.join(d, k), "rb").read() != v]
        changed += len(diff)
        plan.append((f, d, files, diff, how))
        print("  %-24s %-11s %s" % (f[6], how, ("WOULD CHANGE: " + " ".join(diff)) if diff else "same"))
        if how == "final":
            base_feet = feet(os.path.join(GBA, "graphics", "pokemon", f[1], "front.png"))
            tmp = os.path.join(_scratch(), "f.png")
            open(tmp, "wb").write(files["front.png"])
            ff = feet(tmp)
            if ff[0] != base_feet[0] or ff[1] > base_feet[1] + 4:
                print("      feet row %d (base %d), height %d (base %d): stood by its own coords rows"
                      % (ff[0], base_feet[0], ff[1], base_feet[1]))
    copies = summer_copies()
    stale_summer = [(s, d) for s, d in copies if not os.path.exists(d) or open(s, "rb").read() != open(d, "rb").read()]
    for s, d in copies:
        print("  summer %-40s -> gfx/daemons/%-22s %s" % (os.path.basename(s), os.path.basename(d),
              "WOULD CHANGE" if (s, d) in stale_summer else "same"))
    waiting = sorted("%s %s" % (n, se) for n, *_ in BRANCH for se in SEASONS
                     if (n, se) not in APPROVED_FINAL and not (n == "MUSAI" and se == "summer"))
    print("  not approved, placeholder until redrawn: %s" % ", ".join(waiting))
    tabs = tables({f[6]: files for f, d, files, diff, how in plan})
    tchanged = []
    for rel, text in tabs.items():
        p = os.path.join(GBA, rel)
        old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        if old != text:
            tchanged.append(rel)
    print("  %d forms: %d final, %d placeholder; %d form file(s), %d table file(s) and %d summer drawing(s) %s"
          % (len(fs), finals, len(fs) - finals, changed, len(tchanged), len(stale_summer),
             "to write" if WRITE else "would change" if (changed or tchanged or stale_summer) else "-- all current"))
    for rel in tchanged:
        print("      %s" % rel)
    if WRITE:
        for s, d in stale_summer:
            tmp = d + ".tmp"
            shutil.copyfile(s, tmp)
            os.replace(tmp, d)
        if stale_summer:
            print("  !! %d summer drawing(s) copied into gfx/daemons/: now run gbasprite.py --write (then genstreaks,"
                  " gbafollowerpal) and THIS AGAIN, so the placeholders and the species' coords follow" % len(stale_summer))
        for f, d, files, diff, how in plan:
            os.makedirs(d, exist_ok=True)
            for k in diff:
                tmp = os.path.join(d, k + ".tmp")
                open(tmp, "wb").write(files[k])
                os.replace(tmp, os.path.join(d, k))
        for rel in tchanged:
            p = os.path.join(GBA, rel)
            tmp = p + ".tmp"
            open(tmp, "w", encoding="utf-8").write(tabs[rel])
            os.replace(tmp, p)
        print("  written; then run tools/gbafollower.py --write and tools/gbafollowerpal.py --write (the followers)")
    shutil.rmtree(_scratch(), ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

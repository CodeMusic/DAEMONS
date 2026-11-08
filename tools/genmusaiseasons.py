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

  Each block sits between "BEGIN genmusaiseasons" and "END genmusaiseasons" lines; a re-run replaces only that.

WHERE EACH FORM'S ART COMES FROM

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

  A summer final is never read: summer IS the species' art, gbasprite.py's, from gfx/daemons/<name>_front.png.
  The form is drawn on its base's feet line and inside its base's y_offset: the coordinate and elevation tables are
  read by the real species everywhere, so a final that stands taller needs a coords entry (the report checks the
  bottom row and height against the base's front).
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


def final_front(name, season):
    p = os.path.join(FINALS, "%s_%s_front.png" % (name.lower(), season))
    return p if os.path.exists(p) else None


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


def tables():
    """{engine-relative path: new text} for every generated block."""
    fs = forms()
    out = {}

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
                print("      !! feet row %d (base %d), height %d (base %d): it needs its own coords entry"
                      % (ff[0], base_feet[0], ff[1], base_feet[1]))
    if summer:
        print("  ignored (summer is the species' own art, gbasprite's): %s" % " ".join(
            "%s_summer_front.png" % n.lower() for n in summer))
    tabs = tables()
    tchanged = []
    for rel, text in tabs.items():
        p = os.path.join(GBA, rel)
        old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        if old != text:
            tchanged.append(rel)
    print("  %d forms: %d final, %d placeholder; %d form file(s) and %d table file(s) %s"
          % (len(fs), finals, len(fs) - finals, changed, len(tchanged),
             "to write" if WRITE else "would change" if (changed or tchanged) else "-- all current"))
    for rel in tchanged:
        print("      %s" % rel)
    if WRITE:
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

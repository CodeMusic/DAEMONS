#!/usr/bin/env python3
"""T-452: OVERLOADED's four bodies -- the CASTFORM slot's normal, sunny, rainy and snowy forms -- from their drawings.

    python3 tools/gencastform.py               # report: what each form's files would become, and a sheet (a preview)
    python3 tools/gencastform.py --sheet OUT   # the contact sheet only, to OUT
    python3 tools/gencastform.py --write       # into engineGba/graphics/pokemon/castform/{normal,sunny,rainy,snowy}/
    python3 tools/gencastform.py --out DIR     # write the four form folders under DIR instead (a dry run you can open)

WHY A TOOL. The build makes castform/front.4bpp, back.4bpp, normal.gbapal and shiny.gbapal by JOINING the four form
folders (graphics_file_rules.mk: normal/, sunny/, rainy/, snowy/, in CASTFORM_NORMAL, _FIRE, _WATER, _ICE order).
gbasprite.py writes only castform/front.png, back.png and the palettes at the top of the folder, which the build never
reads -- so OVERLOADED drew as vanilla's normal form until batch 18 copied its art into normal/ by hand (engine
be3388f75), and its weather forms had no path from a drawing at all. This is that path, so no form folder holds a
hand-copied file.

WHAT IT READS (gfx/daemons/, 64x64 RGBA grids as every redrawn daemon's are):

  overloaded_front.png / _back.png               NORMAL -- the same files gbasprite.py reads for the species
  overloaded_sunny_front.png / _back.png         the sun's body  (CASTFORM_FIRE)
  overloaded_rainy_front.png / _back.png         the rain's body (CASTFORM_WATER)
  overloaded_snowy_front.png / _back.png         the hail's body (CASTFORM_ICE)

WHAT IT WRITES, per form folder: front.png, back.png, normal.pal, shiny.pal.

EACH FORM IS COLOURED BY ITS OWN TYPE (invariant 5). Forecast makes the battler FIRE, WATER or ICE in sun, rain or hail
(CastformDataTypeChange, src/battle_util.c) and the battle loads that form's whole palette (castformPalette[form]), so
each body is drawn in its type's ramp exactly as gbasprite.place_rich draws a daemon: sunny ENTROPY, rainy FLOW, snowy
FROZEN, and NORMAL in CONTENT's bone -- the species' own type, so normal/ comes out byte-for-byte what gbasprite writes
at the top of the folder. The back draws through its front's palette. shiny.pal is genshiny.make_shiny's of that
palette, inside its type (T-432). Each palette keeps 11-14 as the streak grey; the engine paints them per form (T-4xx:
the castform reload used to wipe them).

The party icon is one for every form, castform/icon.png, and stays gbasprite's (from gfx/daemons/overloaded_icon.png).
"""
import contextlib, io, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(GBA, "graphics/pokemon/castform")
DAEMONS = os.path.join(ROOT, "gfx/daemons")
ARGS = sys.argv[1:]
WRITE = "--write" in ARGS
SHEET = ARGS[ARGS.index("--sheet") + 1] if "--sheet" in ARGS else None
DEST = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else None

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
argv, sys.argv = sys.argv, [sys.argv[0]]      # gbasprite runs its report on import, and reads --write (engine.md 16)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import gbasprite as G
finally:
    sys.argv = argv
import daemonslib, genshiny

#  form folder -> (drawing stem in gfx/daemons, the type Forecast gives it); the build joins them in this order
FORMS = [("normal", "overloaded", "NORMAL"), ("sunny", "overloaded_sunny", "FIRE"),
         ("rainy", "overloaded_rainy", "WATER"), ("snowy", "overloaded_snowy", "ICE")]


def form(stem, typ):
    t = G.TYPE_COLOR[typ]
    front, pal = G.place_rich(os.path.join(DAEMONS, stem + "_front.png"), t)
    back, _ = G.place_rich(os.path.join(DAEMONS, stem + "_back.png"), t, shared=pal)
    pal = list(pal) + [(0, 0, 0)] * (16 - len(pal))
    _t, shiny = genshiny.make_shiny(pal)
    return front, back, pal, (shiny if shiny is not None else pal)


def files():
    out = {}
    for d, stem, typ in FORMS:
        front, back, pal, shiny = form(stem, typ)
        out[d] = {"front.png": (front, pal), "back.png": (back, pal), "normal.pal": pal, "shiny.pal": shiny}
    return out


def png_same(path, grid, pal):
    if not os.path.exists(path):
        return False
    im = Image.open(path)
    if im.mode != "P" or im.size != (64, 64):
        return False
    p = im.getpalette()[:48]
    return (list(im.getdata()) == [v for row in grid for v in row]
            and [tuple(p[i:i + 3]) for i in range(0, 48, 3)] == [tuple(c) for c in pal[:16]])


def pal_same(path, pal):
    return os.path.exists(path) and daemonslib.read_pal(path) == [tuple(c) for c in pal[:16]]


def render(grid, pal, z):
    im = Image.new("RGB", (64, 64), (205, 205, 172)); px = im.load()
    for y in range(64):
        for x in range(64):
            if grid[y][x]:
                px[x, y] = tuple(pal[grid[y][x]])
    return im.resize((64 * z, 64 * z), Image.NEAREST)


def sheet(path, fs):
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    except OSError:
        font = ImageFont.load_default()
    z = 3; W = 24 + 4 * (64 * z + 24); H = 40 + 3 * (64 * z + 30)
    out = Image.new("RGB", (W, H), (40, 40, 46)); d = ImageDraw.Draw(out)
    d.text((12, 8), "gencastform: OVERLOADED's four bodies -- front, back, shiny; each in its own form palette",
           fill=(230, 230, 230), font=font)
    for j, (dname, _, typ) in enumerate(FORMS):
        f = fs[dname]; x = 24 + j * (64 * z + 24)
        d.text((x, 24), "%s (%s)" % (dname, typ), fill=(240, 220, 120), font=font)
        for i, (grid, pal) in enumerate((f["front.png"], f["back.png"], (f["front.png"][0], f["shiny.pal"]))):
            out.paste(render(grid, pal, z), (x, 44 + i * (64 * z + 30)))
    out.save(path)
    return path


def main():
    fs = files()
    base = DEST or OUT
    changed = 0
    for d, _, typ in FORMS:
        for name in ("front.png", "back.png", "normal.pal", "shiny.pal"):
            p = os.path.join(OUT, d, name)
            v = fs[d][name]
            same = png_same(p, *v) if name.endswith(".png") else pal_same(p, v)
            changed += not same
            print("  %-7s %-11s %s" % (d, name, "same" if same else "WOULD CHANGE"))
    print("  sheet -> %s" % sheet(SHEET or daemonslib.preview("gencastform.png"), fs))
    if WRITE or DEST:
        for d, _, _ in FORMS:
            os.makedirs(os.path.join(base, d), exist_ok=True)
            for name in ("front.png", "back.png"):
                grid, pal = fs[d][name]
                G.write_png4(os.path.join(base, d, name), grid, pal)
            G.write_pal(os.path.join(base, d, "normal.pal"), fs[d]["normal.pal"])
            G.write_pal(os.path.join(base, d, "shiny.pal"), fs[d]["shiny.pal"])
        print("  written under %s (%d file(s) differed from the engine's)" % (base, changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""T-440: PROTEUS's two shapes in battle and in the party menu, drawn from our hooded PROTEUS (T-176) and T-439's
two overworld shapes -- CONTENT's all edges, CONTEXT's a shell.

    python3 tools/genproteus.py              # report: what each file would become, and a sheet in the scratch dir
    python3 tools/genproteus.py --sheet OUT  # the contact sheet only, to OUT
    python3 tools/genproteus.py --write      # into engineGba/graphics/pokemon/deoxys/

WHAT THE ENGINE READS (src/data/graphics/pokemon.h, src/decompress.c, src/pokemon_icon.c):

  front.png / back.png        CONTENT's PROTEUS. Vanilla's are 64x128 -- the NORMAL form on top, the edition's form
  front_def.png / back_def.png  below -- and LoadSpecialPokePic's DuplicateDeoxysTiles copies the BOTTOM half over the
                              top whenever the sprite is drawn (battle, summary); only the Index-style _DontHandleDeoxys
                              paths show the top. T-176 wrote CONTENT's front and back as 64x64, so the copy read the
                              64x64 past the end of the picture -- whatever the buffer last held.
  icon_attack.png / icon_defense.png   appended to icon.png (gMonIcon_Deoxys); GetMonIconTiles(.., extra=TRUE) -- the
                              party menu, the naming screen, a summary -- shows them. Vanilla DEOXYS until now, both.

WHAT THIS WRITES

  front.png                   64x128: our hooded PROTEUS on top (the Index's), and CONTENT's shape below, ALL EDGES
                              (gfx/daemons/proteus_front_attack.png) -- the half a foe PROTEUS battles in since the
                              user's follow-up (2026-10-23: each edition's own shape, matching the overworld) and the
                              half an owned one shows. gbasprite.py writes the same file the same way.
  back.png                    64x128: the hooded back on top, and ALL EDGES from behind below (gfx/daemons/
                              proteus_back_attack.png, drawn at 512 on the sprite server, gfx/drafts/t440/make4.sh) --
                              what an owned CONTENT PROTEUS shows in battle. gbasprite.py writes it the same way.
  front_def.png, back_def.png 64x128: the hooded PROTEUS on top, and CONTEXT's SHELL below -- the hood drawn shut and
                              curled like a cocoon, redrawn at 512 from T-439's own deoxys_d frame (gfx/drafts/t440/
                              make2.sh; the picks are gfx/daemons/proteus_front_defense.png and _back_defense.png).
  icon_attack.png             two 32x32 frames, the idle bob: ALL EDGES -- DRAWN since T-452 (gfx/daemons/
                              proteus_icon_attack.png, icon3's, copied index for index as gbasprite.drawn_icon copies
                              proteus_icon.png into icon.png); derived from proteus_front_attack.png only if it is missing.
  icon_defense.png            the same, the SHELL (gfx/daemons/proteus_icon_defense.png).

Every view draws through PROTEUS's one species palette (normal.pal, which gbasprite.py writes from the front), so
the shell's pixels are mapped onto it exactly as gbasprite maps a back onto its front (place_rich's `shared`).

THE ICONS (T-452 forms, the user 2026-10-28: PROTEUS's three forms redrawn). icon.png is gbasprite's, from the drawn
gfx/daemons/proteus_icon.png; the two form icons are drawn the same way (icon3, from each form's front) and copied
here. All three must sit on ONE shared icon palette, the one gMonIconPaletteIndices gives SPECIES_DEOXYS (ICON_PALETTE,
1 since T-452: icon3's best fit for PSYCHIC) -- the species has one index, and a form icon on another palette would draw
in the wrong colours. A drawn icon on any other palette is refused. Without a drawn icon the old reduction stands in:
gbasprite's derive_icon held to ICON_PALETTE.
"""
import contextlib, io, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(GBA, "graphics/pokemon/deoxys")
DAEMONS = os.path.join(ROOT, "gfx/daemons")
ARGS = sys.argv[1:]
WRITE = "--write" in ARGS
SHEET = ARGS[ARGS.index("--sheet") + 1] if "--sheet" in ARGS else None

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
argv, sys.argv = sys.argv, [sys.argv[0]]      # gbasprite runs its report on import, and reads --write (engine.md 16)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import gbasprite as G
finally:
    sys.argv = argv
import daemonslib

ICON_PALETTE = 1          # gMonIconPaletteIndices[SPECIES_DEOXYS] (src/pokemon_icon.c); 0 until T-452's drawn icons


def views():
    t = G.TYPE_COLOR["PSYCHIC"]
    front, pal = G.place_rich(os.path.join(DAEMONS, "proteus_front.png"), t)
    back, _ = G.place_rich(os.path.join(DAEMONS, "proteus_back.png"), t, shared=pal)
    shell_f, _ = G.place_rich(os.path.join(DAEMONS, "proteus_front_defense.png"), t, shared=pal)
    shell_b, _ = G.place_rich(os.path.join(DAEMONS, "proteus_back_defense.png"), t, shared=pal)
    edges_f, _ = G.place_rich(os.path.join(DAEMONS, "proteus_front_attack.png"), t, shared=pal)
    edges_b, _ = G.place_rich(os.path.join(DAEMONS, "proteus_back_attack.png"), t, shared=pal)
    return pal, dict(front=front, back=back, shell_f=shell_f, shell_b=shell_b, edges_f=edges_f, edges_b=edges_b)


def icon(grid, pal):
    """gbasprite's derive_icon, held to the species' own icon palette rather than the best-fitting one"""
    im = G._subject(grid, pal)
    ICON_W, ICON_X, ICON_BOTTOM = 20, 6, 30
    small = im.resize((ICON_W, ICON_W), Image.NEAREST)
    bg = tuple(pal[0])
    body = G.icon_palettes()[ICON_PALETTE][1:]
    m = {}
    for _, c in small.getcolors(4096):
        m[c] = 0 if c == bg else 1 + min(range(len(body)), key=lambda k: sum((a - b) ** 2 for a, b in zip(c, body[k])))
    out = [[0] * 32 for _ in range(64)]
    oy = ICON_BOTTOM - ICON_W
    for y in range(ICON_W):
        for x in range(ICON_W):
            v = m[small.getpixel((x, y))]
            out[oy + y][ICON_X + x] = v
            out[32 + oy + y][ICON_X + x] = v            # frame 2, the bob (identical, as gbasprite draws them)
    return out


def drawn_or_icon(stem, grid, pal):
    """the drawn form icon gfx/daemons/STEM.png when there is one (T-452), else the reduction"""
    p = os.path.join(DAEMONS, stem + ".png")
    if not os.path.exists(p):
        return icon(grid, pal)
    out, (pi, _) = G.drawn_icon(p)
    if pi != ICON_PALETTE:
        raise SystemExit("%s: drawn on icon palette %d; SPECIES_DEOXYS's is %d (ICON_PALETTE)" % (p, pi, ICON_PALETTE))
    return out


def stack(a, b):
    return [row[:] for row in a] + [row[:] for row in b]


def files():
    pal, v = views()
    ipal = G.icon_palettes()[ICON_PALETTE]
    return pal, ipal, {
        "front.png": (stack(v["front"], v["edges_f"]), pal, 64, 128),
        "back.png": (stack(v["back"], v["edges_b"]), pal, 64, 128),
        "front_def.png": (stack(v["front"], v["shell_f"]), pal, 64, 128),
        "back_def.png": (stack(v["back"], v["shell_b"]), pal, 64, 128),
        "icon_attack.png": (drawn_or_icon("proteus_icon_attack", v["edges_f"], pal), ipal, 32, 64),
        "icon_defense.png": (drawn_or_icon("proteus_icon_defense", v["shell_f"], pal), ipal, 32, 64),
    }


def render(grid, pal, w, h, z):
    im = Image.new("RGB", (w, h), (150, 150, 150))
    px = im.load()
    for y in range(h):
        for x in range(w):
            if grid[y][x]:
                px[x, y] = tuple(pal[grid[y][x]])
    return im.resize((w * z, h * z), Image.NEAREST)


def sheet(path):
    pal, ipal, fs = files()
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    except OSError:
        font = ImageFont.load_default()
    cells = []
    for name, (grid, p, w, h) in fs.items():
        old = Image.open(os.path.join(OUT, name)).convert("RGB")
        z = 3 if w == 64 else 4
        cells.append((name, old.resize((old.width * z, old.height * z), Image.NEAREST), render(grid, p, w, h, z)))
    W = sum(max(o.width, n.width) + 24 for _, o, n in cells) + 24
    H = 40 + max(o.height for _, o, _ in cells) + 30 + max(n.height for _, _, n in cells) + 20
    out = Image.new("RGB", (W, H), (40, 40, 46))
    d = ImageDraw.Draw(out)
    d.text((12, 8), "T-440 PROTEUS -- top row: what the engine has now; bottom: what --write puts there (the game's "
                    "own palettes). 64x128 = the top half shown by the Index, the BOTTOM in battle (foe and owned).", fill=(230, 230, 230), font=font)
    x = 24
    for name, o, n in cells:
        d.text((x, 26), name, fill=(240, 220, 120), font=font)
        out.paste(o, (x, 44))
        out.paste(n, (x, 44 + max(c[1].height for c in cells) + 24))
        x += max(o.width, n.width) + 24
    out.save(path)
    return path


def main():
    pal, ipal, fs = files()
    for name, (grid, p, w, h) in fs.items():
        old = Image.open(os.path.join(OUT, name))
        print("  %-17s %dx%d -> %dx%d  %d colours" % (name, old.width, old.height, w, h, len({c for r in grid for c in r})))
    path = SHEET or daemonslib.preview("t440_proteus.png")
    print("  sheet -> %s" % sheet(path))
    if WRITE:
        for name, (grid, p, w, h) in fs.items():
            G.write_png4(os.path.join(OUT, name), grid, p, w, h)
            print("  written %s" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

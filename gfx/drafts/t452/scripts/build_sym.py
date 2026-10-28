"""T-452 SYMBOL's 28 forms (the user, 2026-10-28: as drawn), into the engine -- not the one-species path.

    build_sym.py            report what would change
    build_sym.py --write    write it

WHY ITS OWN SCRIPT. SYMBOL is vanilla's UNOWN (201): its art is 28 forms, graphics/pokemon/unown/<form>/ (a-z,
exclamation_mark, question_mark), all drawn through ONE palette, unown/normal.pal (gMonPalette_Unown, which
palette_table.h gives SPECIES_UNOWN and SPECIES_UNOWN_B..QMARK alike). tools/gbasprite.py writes one front, one back,
one icon and one palette per species folder, so the forms live in gfx/daemons/symbol/ -- a SUBFOLDER, which
gbasprite's rich_src (a glob of the top folder) never sees, and SYMBOL stays one of the species it skips.

WHAT IT WRITES (every file to a temp name, then renamed -- never truncated in place):
  * unown/<form>/front.png -- gfx/daemons/symbol/<form>_front.png (the clean 64 RGBA) through gbasprite.place_rich
    in CONTEXT's ramp (TYPE_PSYCHIC). Every accent was greyed in the drafts (gfx/drafts/t452/y), so all 28 come out
    in the same palette; this ASSERTS it -- one form with its own accent would draw the other 27 wrong.
  * unown/<form>/back.png -- gfx/daemons/symbol/<form>_back.png, already 4bpp (the front mirrored on the index grid,
    the eye painted out: sym_process.py), its indices kept and written in the shared palette.
  * unown/normal.pal, and unown/shiny.pal by genshiny.make_shiny (the new normal.pal is a type ramp, so genshiny now
    owns SYMBOL's shiny like any other daemon's).
  * unown/<form>/icon.png -- gfx/daemons/symbol/<form>_icon.png copied index for index (gbasprite.drawn_icon's check:
    a 32x64 indexed PNG in one of the three shared icon palettes).
  * src/pokemon_icon.c gMonIconPaletteIndices -- SPECIES_UNOWN and SPECIES_UNOWN_B..QMARK set to each icon's palette.
  * src/data/pokemon_graphics/{front,back}_pic_coordinates.h -- the 28 grounding rows by ground.py's rule: .size the
    opaque box rounded up to 8, .y_offset = 63 - the lowest opaque row.
Then: tools/gbafollower.py --write (it makes the letters' followers too, T-452 SYMBOL) and tools/gbafollowerpal.py --write."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))      # this checkout (or worktree), never a fixed path
TOOLS = os.path.join(ROOT, "tools"); GBA = os.path.join(ROOT, "engineGba"); MON = os.path.join(GBA, "graphics/pokemon/unown")
SRC = os.path.join(ROOT, "gfx/daemons/symbol")
sys.path.insert(0, TOOLS)
import numpy as np
from PIL import Image
import daemonslib, genshiny
WRITE = "--write" in sys.argv

#  gbasprite.py's functions without its whole-tree loop (gbs.py's trick, read from THIS checkout's tools/)
_src = open(os.path.join(TOOLS, "gbasprite.py")).read(); _src = _src[:_src.index("pairs = renamed()")]
_argv = sys.argv; sys.argv = [sys.argv[0]]; G = {"__file__": os.path.join(TOOLS, "gbasprite.py"), "__name__": "gbs"}
exec(compile(_src, "gbasprite.py", "exec"), G); sys.argv = _argv

FORMS = [chr(c) for c in range(ord("a"), ord("z") + 1)] + ["exclamation_mark", "question_mark"]
CONST = {f: "UNOWN_" + f.upper() for f in FORMS}
CONST.update({"a": "UNOWN", "exclamation_mark": "UNOWN_EMARK", "question_mark": "UNOWN_QMARK"})
TYPE = "PSYCHIC"   # CONTEXT; species_info.h's SPECIES_UNOWN .types
changed = []

def put_bytes(path, data):
    old = open(path, "rb").read() if os.path.exists(path) else None
    if old == data: return
    changed.append(os.path.relpath(path, ROOT))
    if WRITE:
        tmp = path + ".tmp"; open(tmp, "wb").write(data); os.replace(tmp, path)

def png4(grid, pal, w=64, h=64):
    tmp = os.path.join(MON, ".sym_tmp.png"); G["write_png4"](tmp, grid, pal, w, h)
    data = open(tmp, "rb").read(); os.remove(tmp); return data

def pal_bytes(colours):
    colours = list(colours) + [(0, 0, 0)] * (16 - len(colours))
    return ("\r\n".join(["JASC-PAL", "0100", "16"] + ["%d %d %d" % tuple(c) for c in colours]) + "\r\n").encode()

def art():
    pals, grids = {}, {}
    for f in FORMS:
        grids[f], pals[f] = G["place_rich"](os.path.join(SRC, f + "_front.png"), G["TYPE_COLOR"][TYPE])
    one = pals["a"]
    odd = [f for f in FORMS if pals[f] != one]
    if odd: raise SystemExit("not one palette: %s differ from A's -- SYMBOL's 28 forms share gMonPalette_Unown" % " ".join(odd))
    icons = {}
    for f in FORMS:
        d = os.path.join(MON, f)
        put_bytes(os.path.join(d, "front.png"), png4(grids[f], one))
        b = Image.open(os.path.join(SRC, f + "_back.png"))
        if b.mode != "P" or b.size != (64, 64): raise SystemExit(f + "_back.png: not a 64x64 indexed PNG")
        g = np.array(b)
        if g.max() >= len(one): raise SystemExit(f + "_back.png: an index past the shared palette")
        put_bytes(os.path.join(d, "back.png"), png4(g.tolist(), one))
        ig, (pi, _) = G["drawn_icon"](os.path.join(SRC, f + "_icon.png"))
        icons[f] = pi
        put_bytes(os.path.join(d, "icon.png"), png4(ig, G["icon_palettes"]()[pi], 32, 64))
    put_bytes(os.path.join(MON, "normal.pal"), pal_bytes(one))
    t, shiny = genshiny.make_shiny(one)
    if shiny is None: raise SystemExit("genshiny found no type ramp in the new palette")
    put_bytes(os.path.join(MON, "shiny.pal"), pal_bytes(shiny))
    return icons

def iconpal(icons):
    f = os.path.join(GBA, "src/pokemon_icon.c"); t = open(f, newline="").read()
    body = t.split("const u8 gMonIconPaletteIndices[] = {", 1)
    head, rest = body[0] + "const u8 gMonIconPaletteIndices[] = {", body[1]
    for form, pi in icons.items():
        pat = re.compile(r"(\[SPECIES_%s\]\s*= )(\d)(,?)" % CONST[form])
        m = pat.search(rest)
        if not m: raise SystemExit("no gMonIconPaletteIndices row for SPECIES_" + CONST[form])
        rest = rest[:m.start(2)] + str(pi) + rest[m.end(2):]
    new = head + rest
    assert len(new) == len(t), "length changed"   # one digit for one digit
    put_bytes(f, new.encode())

def ground():
    up = lambda v: min(64, (v + 7) // 8 * 8)
    for k in ("front", "back"):
        f = os.path.join(GBA, "src/data/pokemon_graphics/%s_pic_coordinates.h" % k); t = open(f, newline="").read()
        for form in FORMS:
            if WRITE:       # art() has just written them
                a = np.array(Image.open(os.path.join(MON, form, k + ".png")))[:64]
            else:           # report: measure what would be written (the source), not what is on disk
                a = np.array(Image.open(os.path.join(SRC, form + "_back.png"))) if k == "back" else \
                    np.array(G["place_rich"](os.path.join(SRC, form + "_front.png"), G["TYPE_COLOR"][TYPE])[0])
            ys, xs = np.where(a > 0); w, h, y = up(xs.max() - xs.min() + 1), up(ys.max() - ys.min() + 1), 63 - ys.max()
            pat = re.compile(r"(\[SPECIES_%s\] =\s*\{\s*\.size = MON_COORDS_SIZE\()(\d+), (\d+)(\),\s*\.y_offset = )(\d+)" % CONST[form])
            if not pat.search(t): raise SystemExit("no %s row for SPECIES_%s" % (k, CONST[form]))
            t = pat.sub(lambda m: f"{m[1]}{w}, {h}{m[4]}{y}", t, count=1)
        put_bytes(f, t.encode())

if __name__ == "__main__":
    icons = art(); iconpal(icons); ground()
    print("%d file(s) %s" % (len(changed), "written" if WRITE else "would change -- --write to write them"))
    for c in changed: print("  " + c)
    print("icon palettes:", sorted(set(icons.values())))

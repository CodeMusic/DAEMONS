"""T-452 forms: the engine-ready files, written ONLY under z/engine/ (never the engine), the way the install would leave
them, so the sheets show what the build would draw and install.md can name exact files.

PROTEUS (deoxys/), genproteus.py's layout with the new drawings:
  front.png, back.png          64x128: hooded on top (the Index), ALL EDGES below (CONTENT's battle form)
  front_def.png, back_def.png  64x128: hooded on top, the SHELL below (CONTEXT's)
  normal.pal, shiny.pal        the hooded front's palette (every view mapped onto it); shiny by genshiny.make_shiny
  icon.png, icon_attack.png, icon_defense.png   icon3 from each form's hand front, all on ONE icon palette (the species
                               has one gMonIconPaletteIndices entry; icon3 picks it by type, so all three agree)
OVERLOADED (castform/<form>/), each a 64x64 front and back and its OWN 16-colour palette in its weather's type ramp:
  sunny FIRE, rainy WATER, snowy ICE -- Forecast sets those types (CastformDataTypeChange) and the battle loads
  castformPalette[form], so a form coloured by its type is invariant 5 kept; normal.pal and shiny.pal per form.
Also prints the battle coordinate rows each new picture needs (63 - its lowest opaque row; size the opaque box
rounded up to 8), as the batches' ground.py measures them."""
import os, sys, json
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gbs, icon3
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/tools"); import genshiny
D = os.path.dirname(HERE) + "/z"; E = D + "/engine"
def pick(n, k):
    h = f"{D}/hand/{n}_{k}.png"; return h if os.path.exists(h) else f"{D}/clean/{n}_{k}.png"
def wpal(path, pal):
    with open(path, "w", newline="") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in (list(pal) + [(0, 0, 0)] * 16)[:16]))
def pad(pal):
    pal = [tuple(c) for c in pal]; return pal + [(0, 0, 0)] * (16 - len(pal))
def coords(grid):
    g = np.array(grid)[:64]; ys, xs = np.where(g > 0); up = lambda v: min(64, (v + 7) // 8 * 8)
    return int(up(xs.max() - xs.min() + 1)), int(up(ys.max() - ys.min() + 1)), int(63 - ys.max())
rows = {}

#  PROTEUS
os.makedirs(E + "/deoxys", exist_ok=True)
t = gbs.TYPE_COLOR["PSYCHIC"]
v = {}
v["front"], pal = gbs.place_rich(pick("proteus", "front"), t)
for key, (n, k) in {"back": ("proteus", "back"), "edges_f": ("proteus_edges", "front"), "edges_b": ("proteus_edges", "back"),
                    "shell_f": ("proteus_shell", "front"), "shell_b": ("proteus_shell", "back")}.items():
    v[key], _ = gbs.place_rich(pick(n, k), t, shared=pal)
pal = pad(pal)
st = lambda a, b: [r[:] for r in a] + [r[:] for r in b]
for name, (a, b) in {"front": ("front", "edges_f"), "back": ("back", "edges_b"), "front_def": ("front", "shell_f"),
                     "back_def": ("back", "shell_b")}.items():
    gbs.write_png4(f"{E}/deoxys/{name}.png", st(v[a], v[b]), pal, 64, 128)
wpal(f"{E}/deoxys/normal.pal", pal); _, sh = genshiny.make_shiny(pal); wpal(f"{E}/deoxys/shiny.pal", sh or pal)
ic = {}
for out, n in (("icon", "proteus"), ("icon_attack", "proteus_edges"), ("icon_defense", "proteus_shell")):
    ic[out] = icon3.make(n, "PSYCHIC", pick(n, "front"), f"{E}/deoxys/{out}.png")
print("PROTEUS icon palettes", {k: r["icon_palette"] for k, r in ic.items()})
rows["DEOXYS"] = {k: coords(v[k]) for k in ("front", "edges_f", "shell_f", "back", "edges_b", "shell_b")}

#  OVERLOADED's weathers
for form, typ in (("sunny", "FIRE"), ("rainy", "WATER"), ("snowy", "ICE")):
    n = "overloaded_" + form; os.makedirs(f"{E}/castform/{form}", exist_ok=True)
    gf, p = gbs.place_rich(pick(n, "front"), gbs.TYPE_COLOR[typ]); gb, _ = gbs.place_rich(pick(n, "back"), gbs.TYPE_COLOR[typ], shared=p)
    p = pad(p)
    gbs.write_png4(f"{E}/castform/{form}/front.png", gf, p); gbs.write_png4(f"{E}/castform/{form}/back.png", gb, p)
    wpal(f"{E}/castform/{form}/normal.pal", p); _, sh = genshiny.make_shiny(p); wpal(f"{E}/castform/{form}/shiny.pal", sh or p)
    rows["CASTFORM_" + form] = {"front": coords(gf), "back": coords(gb)}
#  the normal form, as installed (engine be3388f75), measured too: its per-form battle rows are still vanilla's
G = "/Users/christopherhicks/Projects/pokefirered-daemons/graphics/pokemon/castform/normal/"
for k in ("front", "back"):
    rows.setdefault("CASTFORM_normal", {})[k] = coords(np.array(Image.open(G + k + ".png")).tolist())
json.dump(rows, open(E + "/coords.json", "w"), indent=1)
for k, r in rows.items(): print(k, r)

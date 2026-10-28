"""the hand grids through gbasprite.place_rich into z/reduced, as the build will colour them: each OVERLOADED weather in
its own type's ramp (its own palette, the back through its front's); every PROTEUS view through the hooded front's
palette (genproteus.py's rule: the species has one). Writes z/reduced/<n>_{front,back}.png, <n>_normal.pal, <n>_shiny.pal.
    render.py NAME:TYPE[:PALFROM] ..."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gbs
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/tools"); import genshiny
D = os.path.dirname(HERE) + "/z"
def pick(n, k):
    h = f"{D}/hand/{n}_{k}.png"; return h if os.path.exists(h) else f"{D}/clean/{n}_{k}.png"
def pct(g):
    g = np.array(g); return round(((g >= 6) & (g <= 10)).sum() / (g > 0).sum() * 100, 1)
def wpal(path, pal):
    with open(path, "w", newline="") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in (list(pal) + [(0, 0, 0)] * 16)[:16]))
out = {}
for spec in sys.argv[1:]:
    n, t, *pf = spec.split(":")
    shared = None
    if pf: shared = [tuple(c) for c in json.load(open(f"{D}/reduced/{pf[0]}_pal.json"))]
    gf, pal = gbs.place_rich(pick(n, "front"), gbs.TYPE_COLOR[t], shared=shared)
    pal = [tuple(c) for c in pal]
    gbs.write_png4(f"{D}/reduced/{n}_front.png", gf, pal)
    res = {"front_accent_pct": pct(gf)}
    if os.path.exists(pick(n, "back")):
        gb, _ = gbs.place_rich(pick(n, "back"), gbs.TYPE_COLOR[t], shared=pal)
        gbs.write_png4(f"{D}/reduced/{n}_back.png", gb, pal); res["back_accent_pct"] = pct(gb)
    json.dump([list(c) for c in pal], open(f"{D}/reduced/{n}_pal.json", "w"))
    wpal(f"{D}/reduced/{n}_normal.pal", pal)
    _, sh = genshiny.make_shiny(pal); wpal(f"{D}/reduced/{n}_shiny.pal", sh if sh else pal)
    print(n, t, res, "shiny" if sh else "NO SHINY (not a type ramp)")

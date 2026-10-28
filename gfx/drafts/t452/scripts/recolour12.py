"""batch 12: the hand grids (l/hand) put back through gbasprite.place_rich into l/reduced, as reduce2 writes them, so the
sheets show what the build would: the front's palette first, the back through it. Writes only l/reduced and l/picks.json."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gbs
T = os.environ["T452_ROOT"]; D = T + "/p"
P = json.load(open(D + "/picks.json"))
def pick(n, k):
    h = f"{D}/hand/{n}_{k}.png"; return h if os.path.exists(h) else f"{D}/clean/{n}_{k}.png"
def measure(grid):
    g = np.array(grid); return round(((g >= 6) & (g <= 10)).sum() / (g > 0).sum() * 100, 1)
for n in sys.argv[1:]:
    typ = P[n]["type"]
    gf, pf = gbs.place_rich(pick(n, "front"), gbs.TYPE_COLOR[typ]); gb, _ = gbs.place_rich(pick(n, "back"), gbs.TYPE_COLOR[typ], shared=pf)
    gbs.write_png4(f"{D}/reduced/{n}_front.png", gf, pf); gbs.write_png4(f"{D}/reduced/{n}_back.png", gb, pf)
    with open(f"{D}/reduced/{n}_normal.pal", "w", newline="") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in (pf + [(0, 0, 0)] * 16)[:16]))
    P[n]["measured"]["front_accent_pct"] = measure(gf); P[n]["measured"]["back_accent_pct"] = measure(gb)
    P[n]["hand"] = [k for k in ("front", "back") if os.path.exists(f"{D}/hand/{n}_{k}.png")]
    print(n, typ, "front %.1f%% back %.1f%%" % (measure(gf), measure(gb)), P[n]["hand"])
json.dump(P, open(D + "/picks.json", "w"), indent=1)

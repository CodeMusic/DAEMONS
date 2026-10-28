"""phase 1: a hand/ front or back put through gbasprite.place_rich in the type's ramp (as reduce2 does), the back
sharing the front's palette, so the sheets show the hand edit"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gbs
D = os.environ["T452_ROOT"] + "/j"; P = json.load(open(D + "/picks.json"))
for n in sys.argv[1:]:
    typ = P[n]["type"]; pal = None
    for k in ("front", "back"):
        h = f"{D}/hand/{n}_{k}.png"; src = h if os.path.exists(h) else f"{D}/clean/{n}_{k}.png"
        grid, p = gbs.place_rich(src, gbs.TYPE_COLOR[typ], shared=pal if k == "back" else None)
        if k == "front": pal = p
        gbs.write_png4(f"{D}/reduced/{n}_{k}.png", grid, p)
    print(n, "reduced from hand/")

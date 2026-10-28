"""batch 18: party icons by icon3 from the hand front (else the clean); GOLDSET's from its flower head only (rows 0-30:
the whole plant at 26px is a stick). Writes n/hand/<name>_icon.png and the palette into n/picks.json."""
import os, sys, json
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import icon3
T = os.environ["T452_ROOT"]; D = T + "/w"; P = json.load(open(D + "/picks.json"))
CROP = {}
for n in sys.argv[1:]:
    h = f"{D}/hand/{n}_front.png"; src = h if os.path.exists(h) else f"{D}/clean/{n}_front.png"
    if n in CROP:
        a = np.array(Image.open(src).convert("RGBA")); x0, y0, x1, y1 = CROP[n]; b = np.zeros_like(a); b[y0:y1, x0:x1] = a[y0:y1, x0:x1]
        src = f"{D}/src/{n}_iconcrop.png"; Image.fromarray(b).save(src)
    r = icon3.make(n, P[n]["type"], src, f"{D}/hand/{n}_icon.png")
    P[n]["measured"]["icon3"] = r; print(n, r["icon_palette"], r.get("size"))
json.dump(P, open(D + "/picks.json", "w"), indent=1)

"""T-552/T-553: turn each reduced (indexed) front and back back into the RGBA drawing gbasprite's place_rich reads, and
prove the round trip: place_rich must give back the same picture and palette, so the build ships exactly what the user
saw on the sheets (the hand-drawn ski feet and MUSAI's autumn leaves included). Body index i (1 light .. 5 dark) becomes
grey 40+40*(5-i); an accent keeps its colour; a streak index its marker. Writes finals/<key>_{front,back}.png."""
import json, os, sys, contextlib, io
import numpy as np
from PIL import Image
R = "/Users/christopherhicks/Projects/DAEMONS"; D = R + "/gfx/drafts/t552_t553/"
sys.path.insert(0, R + "/tools")
argv, sys.argv = sys.argv, [sys.argv[0]]
with contextlib.redirect_stdout(io.StringIO()):
    import gbasprite as G
sys.argv = argv
P = json.load(open(D + "reduced/picks.json"))
SKI = ("maskmusai_winter", "codemusai_winter")

import colorsys
def leafred(c, t):
    """an accent place_rich would rotate off the type's hue (MUSAI autumn's orange leaves on warm NORMAL) becomes a red
    leaf of the same saturation and value, at 356 degrees: far enough from NORMAL's 40 to be kept as drawn"""
    if c == (0, 0, 0) or G.shift_off(c, t) == c: return c
    h, s, v = colorsys.rgb_to_hsv(*[x / 255 for x in c])
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(356 / 360, max(s, 0.8), v))

def to_rgba(path, t=None):
    im = Image.open(path); g = np.array(im); pal = [tuple(im.getpalette()[k*3:k*3+3]) for k in range(16)]
    if t is not None: pal = pal[:6] + [leafred(c, t) for c in pal[6:11]] + pal[11:]
    a = np.zeros(g.shape + (4,), np.uint8)
    for i in range(1, 16):
        m = g == i
        if not m.any(): continue
        if 1 <= i <= 5: c = (40 + 40 * (5 - i),) * 3
        elif i >= G.STREAK_FIRST: c = G.STREAK_MARKERS[i - G.STREAK_FIRST]
        else: c = pal[i]
        a[m] = c + (255,)
    return Image.fromarray(a, "RGBA"), g, pal

def same(grid, g, pal_a, pal_b):
    G2 = np.array([[pal_a[v] if v else (-1, -1, -1) for v in row] for row in grid])
    g = np.array([[pal_b[v] if v else (-1, -1, -1) for v in row] for row in g])
    #  compare as pictures: the bounding boxes may sit differently in the frame (re-centred)
    def crop(x):
        ys, xs = np.nonzero((x >= 0).any(2)); return x[ys.min():ys.max()+1, xs.min():xs.max()+1]
    a, b = crop(G2), crop(g)
    if a.shape != b.shape: return "shape %s vs %s" % (a.shape, b.shape)
    d = (a != b).any(2)
    return "%d pixels differ in colour" % d.sum() if d.any() else None

os.makedirs(D + "finals", exist_ok=True); fails = []
for key, r in P.items():
    t = G.TYPE_COLOR[r["type"]]
    fsrc = D + "reduced/%s%s.png" % (key, "_skifeet" if key in SKI else "")
    rgba, g, pal = to_rgba(fsrc, t); fo = D + "finals/%s_front.png" % key; rgba.save(fo)
    grid, p = G.place_rich(fo, t)
    e = same(grid, g, p, pal); print(key, "front", e or "same", flush=True)
    if e: fails.append((key, "front", e))
    rgba, g, _ = to_rgba(D + "reduced/%s_back.png" % key, t); bo = D + "finals/%s_back.png" % key; rgba.save(bo)
    grid, _ = G.place_rich(bo, t, shared=p)
    e = same(grid, g, p, pal); print(key, "back", e or "same", flush=True)
    if e: fails.append((key, "back", e))
print("FAILS", fails)


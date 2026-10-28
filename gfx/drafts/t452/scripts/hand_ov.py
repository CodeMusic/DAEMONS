"""T-452 forms, OVERLOADED's three weathers by hand, on the RECOMMENDED fixes (as batches 10-18). From z/clean, into
z/hand (started fresh every run).

    OUTLINE   the drafts' dark-blue line (and the eyes' navy) to the one INK: in each weather's own palette a dark blue
              is in the hue trap (rainy WATER 220, snowy ICE 197) and rotates to purple, and on sunny it is a blue rim
              where every other daemon has a black one.
    TRAP      what is left within 40 degrees of the form's type hue greyed into its ramp (the rainy drops, the snowy
              frost flecks): each form's palette is its own type's ramp, as the engine swaps the whole palette per
              form (castformPalette[form]) and Forecast makes the form that type (FIRE, WATER, ICE).
    SNOWY     the orange beak a small pink mouth, as the normal form's; a row of short icicles hung from its lower edge
              (the key the draft lost).
    BACKS     the front mirrored, the face blurred out (batch 18's soft_face, as OVERLOADED's normal back was made).
    CAP       accents trimmed under 15%; near-marker colours fixed; stray specks off."""
import os, sys, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ["T452_ROOT"] = os.path.dirname(HERE)
import hand4 as h4, hand_b5 as hb, hand_b10lib as hx
F = os.environ["T452_ROOT"] + "/z"; H = F + "/hand"
for m in (h4, hb, hx): m.F, m.H = F, H
from hand4 import load_any, save, sanitize, stamp, op, lum, is_mark, INK
import colorsys
TYPES = {"overloaded_sunny": "FIRE", "overloaded_rainy": "WATER", "overloaded_snowy": "ICE"}
hx.P = {n: {"type": t} for n, t in TYPES.items()}
FACE = (12, 24, 52, 44)
GAMMA = float(os.environ.get("OV_GAMMA", "1.8"))

def soft_face(a, box):
    from scipy.ndimage import gaussian_filter
    x0, y0, x1, y1 = box; o = op(a); mk = is_mark(a); L = lum(a).astype(float)
    Lw = np.where(o, L, np.nan); body = np.nanmedian(Lw[y0:y1, x0:x1])
    B = gaussian_filter(np.where(o, L, body), 3); n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not o[y, x] or mk[y, x]: continue
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): continue
            v = int(round(B[y, x] / 22) * 22); v = max(40, min(236, v)); a[y, x] = (v, v, min(255, v + 4), 255); n += 1
    return n

def flat_face(a, box, fill=None):
    """the face off for a back: inside BOX, every interior cell that is not the body's own light (an eye, its shine, a
    cheek, the mouth: off the box's median body value by more than 34, or saturated) to that median grey, then each
    filled cell given its neighbours' light by a 3x3 mean, so the back of the head is plain and keeps its shading"""
    x0, y0, x1, y1 = box; o = op(a); mk = is_mark(a); L = lum(a)
    reg = a[y0:y1, x0:x1].reshape(-1, 4); rl = lum(reg[None])[0]; rs = reg[:, :3].max(-1) - reg[:, :3].min(-1)
    med = np.median(reg[(reg[:, 3] > 127) & (rs < 40) & (rl > 120)], 0).astype(int); med[3] = 255
    if fill is not None: med = np.array(fill)
    ml = int(lum(med[None, None])[0, 0]); fill = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not o[y, x] or mk[y, x]: continue
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): continue
            sat = a[y, x, :3].max() - a[y, x, :3].min()
            if abs(int(L[y, x]) - ml) > 34 or sat >= 60: a[y, x] = med; fill.append((y, x))
    return len(fill)

def ink_blue(n):
    """dark blue / navy cells (hue 190-260, value under 0.62, saturation over 0.3) to INK"""
    a = load_any(n, "front"); m = 0
    for y, x in zip(*np.where(op(a) & ~is_mark(a))):
        h, s, v = colorsys.rgb_to_hsv(*(a[y, x, :3] / 255))
        if 190 / 360 <= h <= 260 / 360 and s > 0.3 and v < 0.62: a[y, x] = INK; m += 1
    save(a, n, "front"); return m

def mouth(n, box, col=(226, 92, 120, 255)):
    a = load_any(n, "front"); x0, y0, x1, y1 = box; m = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if op(a)[y, x] and not is_mark(a)[y, x] and (a[y, x, :3].max() - a[y, x, :3].min()) >= 60: a[y, x] = col; m += 1
    save(a, n, "front"); return m

ICICLE = ["#W#", "#W#", "#W#", "#L#", " # "]
ICEK = {"#": INK, "W": (236, 240, 244, 255), "L": (200, 206, 214, 255)}
def icicles(n, xs):
    a = load_any(n, "front"); o = op(a)
    for x in xs:
        ys = np.where(o[:, x + 1])[0]
        if len(ys): stamp(a, x, int(ys.max()), ICICLE, ICEK, behind=True)
    save(a, n, "front")

if __name__ == "__main__":
    os.makedirs(H, exist_ok=True)       # only this script's own files are started fresh (the other forms share z/hand)
    for f in os.listdir(H):
        if any(f.startswith(n + "_") and f.count("_") == n.count("_") + 1 for n in TYPES): os.remove(os.path.join(H, f))
    for n in TYPES:
        print(n, "blue line to ink", ink_blue(n))
        g = hx.specks(n, "front")
        if g: print(n, "stray cells off", g)
    a = load_any("overloaded_sunny", "front"); m = 0
    for y, x in zip(*np.where(op(a) & ~is_mark(a))):
        h, sv, v = colorsys.rgb_to_hsv(*(a[y, x, :3] / 255))
        if 190 / 360 <= h <= 290 / 360 and sv > 0.2: hx.grey_at(a, y, x); m += 1
    save(a, "overloaded_sunny", "front"); print("sunny: the draft's blue rim flecks in its rays greyed", m)
    print("snowy mouth pink", mouth("overloaded_snowy", (27, 35, 38, 40)))
    icicles("overloaded_snowy", [10, 15, 28, 33, 45, 50])
    #  DEEPEN: the drafts are near-white clouds, and place_rich spreads the body's values over the ramp from the ink up,
    #  so a pale body lands on the highlight and light steps and the weather's colour barely shows (sunny read as pale
    #  peach). The body's values (ink, accents and markers untouched) are spread half by a straight stretch (10th..97th percentile onto 120..245) and half by rank (onto 110..250), so each ramp
    #  step from dark to highlight takes a share and the type's mid tone carries the body: the sun reads ENTROPY's amber,
    #  the rain FLOW's blue, the snow FROZEN's ice. Order is kept, so the shading is the draft's; the stretch half keeps it smooth.
    for n in TYPES:
        a = load_any(n, "front"); o = op(a) & ~is_mark(a); sat = a[..., :3].max(-1) - a[..., :3].min(-1); L = lum(a)
        m = o & (sat < 60) & (L >= 60); lo, hi = np.percentile(L[m], [10, 97])
        lin = np.clip(120 + (L[m] - lo) * (245 - 120) / max(1, hi - lo), 100, 250)
        order = np.argsort(L[m], kind="stable"); rank = np.empty(len(order)); rank[order] = 110 + np.arange(len(order)) / max(1, len(order) - 1) * 140
        new = (0.5 * lin + 0.5 * rank).astype(int)
        for (y, x), v in zip(zip(*np.where(m)), new): a[y, x, :3] = (v, v, min(255, v + 4))
        save(a, n, "front"); print(n, "deepened cells", int(m.sum()))
    for n in TYPES:
        a = load_any(n, "front"); print(n, "back, face cells", flat_face(a, FACE)); save(a[:, ::-1].copy(), n, "back")
        for k in ("front", "back"):
            g = hx.trim(n, k)
            if g: print(n, k, "accent cells greyed for the cap", g)
            left = hx.trap(n, k, "grey", s_min=0.25, acc_only=True)
            if left: print(n, k, "in the type's hue reach, greyed:", left)
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", sorted(os.listdir(H)))

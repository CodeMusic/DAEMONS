"""T-452 round two: a party icon that reads at 1x in the shared icon palettes (the user's batch 1 notes: ROVERSEER,
INDEXER, INJECTOR and CRAWLER muddy).

    icon3.py NAME TYPE CLEAN_ICON.png OUT.png [--size=26]

WHY reduce2's icons went muddy. reduce2 put the drawn bust in the type's ramp first and then sent each ramp step to
its nearest colour in a shared icon palette. A type ramp is five steps of one hue close in value, and the shared
palettes hold only two or three colours near any one hue -- so neighbouring steps landed on olive (123,156,74), the
dark grey-brown (98,98,90) and the outline (65,65,65), three colours within 40 of each other in value. At 1x that is
one dark smear.

WHAT THIS DOES INSTEAD. The cleaned bust is reduced by footprint vote as before (outline wins a cell at 30%), but
each cell keeps its LUMINANCE, not a ramp index. The creature's own values are split in three by 1-D k-means
(dark / mid / light), isolated single cells are voted back into their neighbours' band, and the three bands are
given three colours of ONE shared palette chosen so that:
  * the three sit at least 45 apart in value, and at least 30 above the outline (65): the shape reads first;
  * the mid band is the palette's nearest colour to the type's hue (invariant 5: the type carries the colour),
    the dark band the nearest darker one, the light band white or the palette's palest tint;
  * nothing within 45 of the party screen's teal (palette index 0) -- a body that colour is a hole;
  * small saturated patches of the draft (eyes, a light, a stinger; at most 6 cells each) keep a saturated
    palette colour of their own -- an accent, not the body.
The whole is drawn at SIZE+2 (26 + its outline = 28, against reduce2's 24: vanilla's own icons use most of the
cell) on the bottom of the 32px frame, frame 2 one pixel lower (the bob)."""
import sys, os, json
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gbs

def lum(c): return 0.299 * c[..., 0] + 0.587 * c[..., 1] + 0.114 * c[..., 2]

def kmeans3(v):
    c = np.percentile(v, [15, 50, 85]).astype(float)
    for _ in range(30):
        lab = np.argmin(np.abs(v[:, None] - c[None]), 1)
        for k in range(3):
            if (lab == k).any(): c[k] = v[lab == k].mean()
    return np.sort(c)

def ramp(pal, type_rgb):
    """best (dark, mid, light) palette indices for this type: value gaps first, hue second"""
    P = np.array(pal, float); L = lum(P); t = np.array(type_rgb, float)
    def hue_err(j):
        a = P[j] / max(1, P[j].sum()); b = t / t.sum(); return np.abs(a - b).sum() * 300
    best = None
    #  never the party screen's own teal (index 0, 98,156,131) or a colour within 45 of it: a body that is the
    #  ground's colour is a hole in the icon
    idx = [j for j in range(1, 15) if np.abs(P[j] - P[0]).sum() > 45 * 3 ** 0.5 and np.sqrt(((P[j] - P[0]) ** 2).sum()) > 45]
    for m in idx:
        if not (130 <= L[m] <= 215): continue
        for d in idx:
            if not (95 <= L[d] <= L[m] - 45): continue
            for l in idx:
                if L[l] < L[m] + 40: continue
                sat_l = P[l].max() - P[l].min()
                e = hue_err(m) * 2 + hue_err(d) * 0.6 + (0 if sat_l < 20 else 25 + hue_err(l) * 0.3)
                if best is None or e < best[0]: best = (e, (d, m, l))
    return best

def make(name, typ, src, out, size=26):
    a = np.asarray(Image.open(src).convert("RGBA")).astype(float)
    subj = a[..., 3] > 127
    ys, xs = np.where(subj); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; subj = a[..., 3] > 127
    rgb = a[..., :3]; L = lum(rgb); sat = rgb.max(2) - rgb.min(2)
    sc = size / max(subj.shape); h, w = max(1, round(subj.shape[0] * sc)), max(1, round(subj.shape[1] * sc))
    cell_l = np.full((h, w), -1.0); ink = np.zeros((h, w), bool); acc = np.zeros((h, w, 3)); is_acc = np.zeros((h, w), bool)
    for y in range(h):
        for x in range(w):
            sl = (slice(int(y / sc), max(int(y / sc) + 1, int((y + 1) / sc))), slice(int(x / sc), max(int(x / sc) + 1, int((x + 1) / sc))))
            s = subj[sl]
            if s.mean() <= 0.5: continue
            l = L[sl][s]; st = sat[sl][s]; c = rgb[sl][s]
            if (l < 60).mean() >= 0.30: ink[y, x] = True; cell_l[y, x] = 0; continue
            nl = l >= 60
            cell_l[y, x] = l[nl].mean()
            if (st[nl] >= 70).mean() > 0.5: is_acc[y, x] = True; acc[y, x] = c[nl][st[nl] >= 70].mean(0)
    body = (cell_l >= 0) & ~ink
    #  accents: connected patches of at most 6 cells stay accents; larger saturated areas are body
    lab = np.zeros((h, w), int); k = 0
    for y, x in zip(*np.where(is_acc)):
        if lab[y, x]: continue
        k += 1; st = [(y, x)]; lab[y, x] = k; mem = []
        while st:
            p = st.pop(); mem.append(p)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (p[0] + dy, p[1] + dx)
                if 0 <= q[0] < h and 0 <= q[1] < w and is_acc[q] and not lab[q]: lab[q] = k; st.append(q)
        if len(mem) > 6:
            for p in mem: is_acc[p] = False
    v = cell_l[body & ~is_acc]
    c = kmeans3(v) if len(v) > 3 else np.array([90, 150, 220.])
    band = np.full((h, w), -1); bb = body & ~is_acc
    band[bb] = np.argmin(np.abs(cell_l[bb][:, None] - c[None]), 1)
    #  isolated cells take their neighbours' band
    b2 = band.copy()
    for y, x in zip(*np.where(bb)):
        nb = [band[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= y + dy < h and 0 <= x + dx < w and band[y + dy, x + dx] >= 0]
        if len(nb) >= 3 and band[y, x] not in nb: b2[y, x] = max(set(nb), key=nb.count)
    band = b2
    best = None
    for pi, pal in enumerate(gbs.icon_palettes()):
        r = ramp(pal, gbs.TYPE_COLOR[typ])
        if r and (best is None or r[0] < best[0]): best = (r[0], pi, r[1])
    _, pi, (dk, md, lt) = best; pal = gbs.icon_palettes()[pi]; P = np.array(pal, float)
    g = np.zeros((h, w), int)
    g[ink] = 15; g[band == 0] = dk; g[band == 1] = md; g[band == 2] = lt
    for y, x in zip(*np.where(is_acc)):
        cands = [j for j in range(1, 15) if P[j].max() - P[j].min() >= 60]
        g[y, x] = min(cands, key=lambda j: ((P[j] - acc[y, x]) ** 2).sum())
    big = np.zeros((h + 2, w + 2), int); big[1:-1, 1:-1] = g
    op = big > 0
    ring = ~op & (np.roll(op, 1, 0) | np.roll(op, -1, 0) | np.roll(op, 1, 1) | np.roll(op, -1, 1))
    big[ring] = 15
    out_g = [[0] * 32 for _ in range(64)]
    oy, ox = 31 - big.shape[0], (32 - big.shape[1]) // 2
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            if 0 <= oy + y < 32: out_g[oy + y][ox + x] = int(big[y, x])
            if 32 + oy + y + 1 < 64 and oy + y + 1 >= 0: out_g[32 + oy + y + 1][ox + x] = int(big[y, x])
    gbs.write_png4(out, out_g, pal, 32, 64)
    return {"icon_palette": pi, "ramp": [dk, md, lt], "ramp_rgb": [pal[dk], pal[md], pal[lt]], "bands": [round(x) for x in c],
            "accent_cells": int(is_acc.sum()), "size": [big.shape[1], big.shape[0]]}

if __name__ == "__main__":
    opt = {a.split("=", 1)[0][2:]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    print(json.dumps(make(*args[:4], size=int(opt.get("size", 26)))))

"""T-452 SYMBOL: chosen draft -> clean 64 grid -> every accent greyed (the 28 share ONE palette: gMonPalette_Unown) ->
back = the front mirrored with its eye painted out -> place_rich in CONTEXT's ramp (PSYCHIC) -> 4bpp; icon by icon3.
    process.py [FORM ...]      reads y/choose.json {"form": {"front": FILE, "note": ...}} (default: the 0.6 draft, 6821)
Writes y/clean, y/hand, y/reduced, y/picks.json. Never the engine."""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symlib import *
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import gbs, icon3
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3"); TYP = "PSYCHIC"   # SYMBOL is CONTEXT (species_info: TYPE_PSYCHIC)
for k in ("clean", "hand", "reduced"): os.makedirs(f"{D}/{k}", exist_ok=True)
CH = json.load(open(D + "/choose.json")) if os.path.exists(D + "/choose.json") else {}
P = json.load(open(D + "/picks.json")) if os.path.exists(D + "/picks.json") else {}
def lum(a): return (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000
def grey_accents(a):
    """every saturated cell to grey at its own value: no accent survives, so all 28 palettes are BG + the ramp"""
    s = a[..., 3] > 127; rgb = a[..., :3].astype(int); sat = rgb.max(2) - rgb.min(2)
    m = s & (sat >= 20); L = lum(rgb); n = int(m.sum())
    for c in range(3): a[..., c] = np.where(m, L, a[..., c])
    return a, n
EYES = json.load(open(D + "/src/eyes.json"))
def back_grid(gf, f, grow=0.0):
    """THE BACK, on the index grid: the front's cells mirrored (seen from behind, the glyph reads reversed), the eye
    painted out first -- a disc where the guide put it, each cell taking its nearest body cell outside the disc (index
    2-4, so the shading runs on), cells where the eye bulged past the letter dropped, a new outline (5) round the cut.
    Working on indices keeps the back's shades exactly the front's (place_rich spreads a view's own values afresh)."""
    g = np.array(gf); e = EYES[f]; s = g > 0
    yy, xx = np.mgrid[:64, :64]
    #  place_rich centres the cropped subject: find the offset by matching the clean front's box to the grid's
    cy, cx = e["y"] / 8 + OFF[f][0], e["x"] / 8 + OFF[f][1]
    disc = np.hypot(yy - cy, xx - cx) <= e["r"] / 8 + grow
    src = s & ~disc & (g >= 2) & (g <= 4)
    dist, (iy, ix) = ndi.distance_transform_edt(~src, return_indices=True)
    eye = disc & s; out = g.copy()
    #  inside: the body's mid (3), lit upper left (2), shaded lower right (4) -- the light every draft uses; within
    #  1.5 cells of real body, that body's own cell, so the patch joins what is round it
    ring = src & (np.hypot(yy - cy, xx - cx) <= e["r"] / 8 + 3)
    tone = 3   # the body's mid: the commonest tone round the eye was often the shadow, and a dark blot read as a hole
    fill = np.full(g.shape, tone)
    near = dist <= 1.5
    out[eye] = np.where(near[eye], g[iy[eye], ix[eye]], fill[eye])
    letter = np.roll(np.roll(np.array(Image.open(f"{D}/src/{f}_mask.png")) > 110, OFF[f][0], 0), OFF[f][1], 1)
    out[eye & ~ndi.binary_dilation(letter, iterations=1)] = 0
    s2 = out > 0
    rim = disc & s2 & ndi.binary_dilation(~s2, iterations=1)
    out[rim] = 5
    return out[:, ::-1].tolist(), int(eye.sum())
OFF = {}
def a_counter(a):
    """A: the model drew a tiny 'A' where the counter is; cut a real triangular counter (apex row 26, base row 34)
    over it, every cell of the little letter painted body first, then outlined"""
    out = a.copy(); L = lum(out[..., :3].astype(int))
    box = (slice(24, 36), slice(27, 40)); sub = out[box]; m = (sub[..., 3] > 127) & (lum(sub[..., :3].astype(int)) < 70)
    sub[m, :3] = (128, 128, 128); out[box] = sub
    cx = 33
    for y in range(27, 34):
        hw = (y - 26) * 0.6
        for x in range(64):
            if abs(x + 0.5 - cx) <= hw: out[y, x, 3] = 0
    s = out[..., 3] > 127; rim = s & ndi.binary_dilation(~s, iterations=1); rim[:, :] &= False
    cut = np.zeros((64, 64), bool); cut[26:35, 27:40] = True
    rim = s & ndi.binary_dilation(~s & cut, iterations=1) & cut
    out[rim, :3] = (20, 20, 20)
    return out
HAND = {"a": a_counter}
def counters_out(a, f):
    """THE LETTER'S HOLES ARE HOLES: the model painted A's, B's, D's, O's, P's, Q's and R's counters pale (paper) or drew in
    them (a tiny 'A'); every cell inside a counter of the guide's letter, a cell in from its rim and not under the eye,
    is cut, and the cut is outlined. Same grid as the draft (512/8), so the guide's mask lines up as it is."""
    letter = np.array(Image.open(f"{D}/src/{f}_mask.png")) > 110
    holes = ndi.binary_fill_holes(letter) & ~letter
    e = EYES[f]; yy, xx = np.mgrid[:64, :64]; disc = np.hypot(yy - e["y"] / 8, xx - e["x"] / 8) <= e["r"] / 8
    cut = ndi.binary_erosion(holes, iterations=1) & ~disc
    out = a.copy(); out[cut, 3] = 0
    s = out[..., 3] > 127; rim = s & ndi.binary_dilation(cut, iterations=1) & ~disc
    out[rim, :3] = (20, 20, 20)
    return out, int((cut & (a[..., 3] > 127)).sum())
for f in [a for a in sys.argv[1:]] or FORMS:
    c = CH.get(f, {}); fr = c.get("front", f"{f}_front_i2i_6821.png")
    cl = f"{D}/clean/{f}_front.png"
    r = subprocess.run([PY, R + "/tools/cleandraft.py", f"{D}/{fr}", cl], capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stdout + r.stderr)
    a = np.array(Image.open(cl).convert("RGBA"))
    a, ng = grey_accents(a)
    a, nh = counters_out(a, f)
    if f in HAND: a = HAND[f](a)
    Image.fromarray(a).save(f"{D}/hand/{f}_front.png")
    gf, pf = gbs.place_rich(f"{D}/hand/{f}_front.png", gbs.TYPE_COLOR[TYP])
    #  where place_rich put the clean front: the subject's box centred in 64 (a clean front is never scaled: 64 already)
    ys, xs = np.where(a[..., 3] > 127); h, w = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    OFF[f] = ((64 - h) // 2 - ys.min(), (64 - w) // 2 - xs.min())
    gb, ne = back_grid(gf, f, c.get("grow", 1.0))
    gbs.write_png4(f"{D}/reduced/{f}_front.png", gf, pf); gbs.write_png4(f"{D}/reduced/{f}_back.png", gb, pf)
    ic = icon3.make(key(f), TYP, f"{D}/hand/{f}_front.png", f"{D}/reduced/{f}_icon.png")
    g = np.array(gf); ys, xs = np.where(g > 0)
    P[f] = {"glyph": GLYPH[f], "const": CONST[f], "front": fr, "note": c.get("note", ""), "palette": [list(x) for x in pf],
            "greyed": ng, "eye_cells": ne, "box": [int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)], "icon3": ic}
    print(f, fr, "greyed", ng, "holes cut", nh, "eye", ne, "box", P[f]["box"], "icon pal", ic["icon_palette"], "colours", len(pf), flush=True)
json.dump(P, open(D + "/picks.json", "w"), indent=1)
pals = {json.dumps(v["palette"]) for v in P.values()}
print("ONE PALETTE across", len(P), "forms" if len(pals) == 1 else "-- %d DIFFERENT palettes" % len(pals))

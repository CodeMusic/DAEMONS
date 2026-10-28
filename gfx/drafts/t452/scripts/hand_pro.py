"""T-452 forms, PROTEUS's three forms by hand, on the RECOMMENDED fixes. From z/clean into z/hand (fresh every run).

    ONE CREATURE  the same two glowing eyes in all three: orange (hue ~28, far outside PSYCHIC's 312 +- 40), drawn on the
                  hooded face (the clean wore its draft's eyes away), the edged form's red eyes turned that orange and its
                  cyan visor darkened to the face's shadow, the shell's own orange eyes kept. Every view draws through
                  the hooded front's one palette (genproteus.py), so they must share their accents.
    OUTLINE       the drafts' navy line to the one INK (hooded: hood rim and ears); the hood's pale blue shading greyed.
    GROUND        the hooded draft's shadow off.
    BACKS         the front mirrored with the face flattened to the hood's own grey (the recipe since batch 11):
                  hooded from behind, ALL EDGES from behind (blades still raised), the shell closed.
    CAP           accents trimmed under 15%; what is left within 40 degrees of PSYCHIC greyed; near-marker colours fixed."""
import os, sys, shutil, colorsys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ["T452_ROOT"] = os.path.dirname(HERE)
import hand4 as h4, hand_b5 as hb, hand_b10lib as hx
F = os.environ["T452_ROOT"] + "/z"; H = F + "/hand"
for m in (h4, hb, hx): m.F, m.H = F, H
from hand4 import load_any, save, sanitize, stamp, op, lum, is_mark, INK
from hand_ov import flat_face
NAMES = ["proteus", "proteus_edges", "proteus_shell"]
hx.P = {n: {"type": "PSYCHIC"} for n in NAMES}
EYE = ["LO", "OD"]; EYEK = {"L": (255, 214, 130, 255), "O": (246, 140, 44, 255), "D": (196, 92, 28, 255)}
FACE = {"proteus": (23, 15, 36, 27), "proteus_edges": (22, 18, 42, 30), "proteus_shell": (18, 26, 46, 42)}

def hsv(c): return colorsys.rgb_to_hsv(*(np.array(c[:3]) / 255))

def navy_ink(n, box=(0, 0, 64, 64)):
    a = load_any(n, "front"); m = 0; x0, y0, x1, y1 = box
    for y, x in zip(*np.where(op(a) & ~is_mark(a))):
        if not (x0 <= x < x1 and y0 <= y < y1): continue
        h, s, v = hsv(a[y, x])
        if 190 / 360 <= h <= 265 / 360 and s > 0.25:
            edge = any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not op(a)[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if v < 0.3 or (edge and v < 0.62): a[y, x] = INK
            else: hx.grey_at(a, y, x)
            m += 1
    save(a, n, "front"); return m

def ground(n, row, minL=90):
    a = load_any(n, "front"); m = 0
    for y in range(row, 64):
        for x in range(64):
            if op(a)[y, x] and lum(a[y:y + 1, x:x + 1])[0, 0] >= minL: a[y, x] = 0; m += 1
    save(a, n, "front"); return m

def recolour(n, box, test, col):
    a = load_any(n, "front"); x0, y0, x1, y1 = box; m = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if op(a)[y, x] and not is_mark(a)[y, x] and test(a[y, x]): a[y, x] = col; m += 1
    save(a, n, "front"); return m

if __name__ == "__main__":
    os.makedirs(H, exist_ok=True)       # only this script's own files are started fresh (the other forms share z/hand)
    for f in os.listdir(H):
        if any(f.startswith(n + "_") and f.count("_") == n.count("_") + 1 for n in NAMES): os.remove(os.path.join(H, f))
    print("hooded navy to ink / pale blue greyed", navy_ink("proteus"))
    print("hooded ground off", ground("proteus", 53))
    a = load_any("proteus", "front"); a[56:] = 0; save(a, "proteus", "front")      # the shadow's own dark rim, below the feet
    a = load_any("proteus", "front"); m = 0
    for y, x in zip(*np.where(op(a)[:16])):
        if a[y, x, :3].max() - a[y, x, :3].min() >= 30: hx.grey_at(a, y, x); m += 1
    save(a, "proteus", "front"); print("hooded: the draft's pale blue flecks on the hood greyed", m)
    a = load_any("proteus", "front")
    stamp(a, 25, 19, EYE, EYEK); stamp(a, 31, 19, EYE, EYEK); save(a, "proteus", "front")
    #  the edged form: red eyes to the orange, the cyan visor to the face's dark
    red = lambda c: (hsv(c)[0] < 20 / 360 or hsv(c)[0] > 340 / 360) and hsv(c)[1] > 0.4 and hsv(c)[2] > 0.4
    cyan = lambda c: 150 / 360 <= hsv(c)[0] <= 215 / 360 and hsv(c)[1] > 0.2
    print("edges eyes orange", recolour("proteus_edges", (22, 16, 44, 32), red, EYEK["O"]))
    print("edges visor dark", recolour("proteus_edges", (20, 16, 46, 32), cyan, (58, 56, 66, 255)))
    print("edges navy to ink", navy_ink("proteus_edges"))
    print("shell navy to ink", navy_ink("proteus_shell"))
    #  dark limbs: the darkest body step is the INK (gbasprite's ramp5), so a limb drawn near-black becomes a solid black
    #  shape -- the hooded form's ears and the edged form's raised blades; their interiors lifted to a dark grey, so they
    #  take the ramp's dark step and keep their ink rim
    for n, boxes in (("proteus", [(8, 14, 25, 23), (39, 14, 58, 23)]), ("proteus_edges", [(4, 6, 24, 34), (41, 6, 62, 34)])):
        a = load_any(n, "front"); m = 0
        for x0, y0, x1, y1 in boxes:
            for y in range(y0, y1):
                for x in range(x0, x1):
                    if not op(a)[y, x] or is_mark(a)[y, x] or lum(a[y:y + 1, x:x + 1])[0, 0] >= 70: continue
                    if all(0 <= y + dy < 64 and 0 <= x + dx < 64 and op(a)[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        a[y, x] = (104, 100, 112, 255); m += 1
        save(a, n, "front"); print(n, "dark limb cells lifted", m)
    for n in NAMES:
        g = hx.specks(n, "front")
        if g: print(n, "stray cells off", g)
    for n in NAMES:
        a = load_any(n, "front")
        hood = None
        if n != "proteus_shell":     # the back of a hood is the hood: its own light, from the cells above the face
            x0, y0, x1, y1 = FACE[n]; r = a[max(0, y0 - 8):y0, x0:x1].reshape(-1, 4); r = r[(r[:, 3] > 127) & (lum(r[None])[0] > 150)]
            hood = list(np.median(r, 0).astype(int)) if len(r) else None
        print(n, "back, face cells", flat_face(a, FACE[n], hood), "fill", hood); save(a[:, ::-1].copy(), n, "back")
        for k in ("front", "back"):
            g = hx.trim(n, k, keep=FACE[n] if k == "front" else None)
            if g: print(n, k, "accent cells greyed for the cap", g)
            left = hx.trap(n, k, "grey", s_min=0.25, acc_only=True)
            if left: print(n, k, "in PSYCHIC's hue reach, greyed:", left)
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", sorted(os.listdir(H)))

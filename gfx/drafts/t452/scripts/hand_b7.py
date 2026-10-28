"""T-452 batch 7, by hand (phase 1 drafts; hand4.py's, hand_b5.py's and hand_b6.py's helpers).

    hand_b7.py      writes T/j/hand/<name>_{front,back}.png (from j/clean); handreduce_b7.py reduces them

DYNAMO     two curly antennae drawn back on its head (the key prop; the i2i draft kept only a knob, taken off)
STUB       its back: the front mirrored, the face's features painted out (the drafted backs were side views with a face)
MASKMUSAI  the dot eyes and mouth painted off its face plate, so the mask is blank (its key)
SEEKMUSAI  two wide flat fins out from the helmet, front and back (lost by all eight drafts)
CODEMUSAI  its back scaled to 40 rows, a dark spot painted out
ESCALATE   its back: the front mirrored, the face painted out (choose.json hand-back)
MOCK       its back's dot eye painted out
GROUNDS    baked grounds off the clean grids (hand4.ug)
SANITIZE   hand3's: a drawn colour within reach of a streak marker darkened or greyed"""
import os, sys, json
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hand4 as h4
import hand_b5 as hb
R = "/Users/christopherhicks/Projects/DAEMONS"; F = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452") + "/j"; H = F + "/hand"
hb.F, hb.H = F, H; h4.F, h4.H = F, H
from hand4 import load_any, sanitize, save, ug, outline, stamp, body_grey, op, lum, is_mark, INK
import hand_b6 as h6
from hand_b6 import disc, limb, clear
from batch7 import NAMES
hb.F, hb.H = F, H; h4.F, h4.H = F, H; h6.F, h6.H = F, H
LIGHT = (214, 218, 228, 255); MID = (140, 146, 160, 255)

def dynamo():
    a = load_any("dynamo", "front"); print("dynamo ground", ug(a, 0.85, minL=110))
    clear(a, (27, 3, 32, 10))                       # the knob
    for (bx, tx, cx) in ((27, 24, 21.5), (37, 40, 42.5)):
        limb(a, (bx, 12), (tx, 5), 0.6, 1.4, MID)
        disc(a, cx, 3.5, 2.6, INK, skip_marks=True); disc(a, cx, 3.5, 1.4, LIGHT)
        disc(a, cx + (0.8 if cx < 32 else -0.8), 4.2, 0.6, INK)   # the curl's eye
    outline(a, (11, 14)); save(a, "dynamo", "front")

def fins(k="front", roots=(21, 47), tips=(10, 58), y0=20, y1=28):
    """SEEKMUSAI: two wide flat fins out sideways from the helmet, like wings (its key, lost by every draft)"""
    a = load_any("seekmusai", k)
    if k == "front": print("seekmusai ground", ug(a, 0.85, minL=110))
    W_ = (232, 236, 242, 255); S_ = (176, 184, 198, 255)
    for root, tip in zip(roots, tips):
        for x in range(min(root, tip), max(root, tip) + 1):
            t = abs(x - root) / abs(tip - root)          # 0 at the helmet, 1 at the tip
            if abs(x - root) < 2 and a[y0 + 3, x, 3] > 127: continue
            top = round(y0 + 4 * t); bot = round(y1 - 2 * t)
            for y in range(top, bot + 1):
                if a[y, x, 3] > 127 and abs(x - root) < 2: continue
                a[y, x] = INK if (y in (top, bot) or x == tip) else (S_ if y >= bot - 2 else W_)
    save(a, "seekmusai", k)

def scaled_back(n, rows, foot=62):
    """a back too small beside its front, scaled (nearest) to ROWS tall, centred, standing on FOOT"""
    b = load_any(n, "back"); ys, xs = np.where(op(b)); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    s = rows / (y1 - y0); im = Image.fromarray(b[y0:y1, x0:x1].astype(np.uint8), "RGBA")
    im = im.resize((min(64, round((x1 - x0) * s)), rows), Image.NEAREST)
    out = np.zeros((64, 64, 4), int); sx = 32 - im.width // 2
    out[foot - rows + 1:foot + 1, sx:sx + im.width] = np.array(im).astype(int); save(out, n, "back")

# ---- PHASE 2 (the user's answers to batch 7, 2026-10-27) ----
DARKG = (40, 42, 52, 255); GLASS = (34, 34, 44, 255); RING = (96, 98, 116, 255); SHINE = (236, 238, 244, 255)

def scaled_front(n, sx, sy, foot):
    """the front scaled by SX across and SY down (nearest), centred, standing on FOOT"""
    b = load_any(n, "front"); ys, xs = np.where(op(b)); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    im = Image.fromarray(b[y0:y1, x0:x1].astype(np.uint8), "RGBA")
    w, h = round((x1 - x0) * sx), round((y1 - y0) * sy); im = im.resize((w, h), Image.NEAREST)
    out = np.zeros((64, 64, 4), int); sx0 = 32 - w // 2 - 2
    out[foot - h + 1:foot + 1, sx0:sx0 + w] = np.array(im).astype(int); return out

def crank():
    """CRANK: smaller and rounder (squat), a hand crank on its side; back = the front mirrored, face out"""
    a = scaled_front("crank", 0.86, 0.74, 58)
    ys, xs = np.where(op(a)); y0, y1 = ys.min(), ys.max(); ym = y0 + int((y1 - y0) * 0.66)
    xr = max(x for x in range(64) if a[ym, x, 3] > 127)
    G = (150, 154, 166, 255)
    limb(a, (xr - 1, ym), (xr + 4, ym), 1.0, 2.0, G)           # the shaft out of its side
    limb(a, (xr + 4, ym), (xr + 4, ym - 9), 1.0, 2.0, G)       # the arm, up
    limb(a, (xr + 4, ym - 9), (xr + 8, ym - 9), 1.2, 2.2, (110, 114, 126, 255))   # the handle
    disc(a, xr + 4, ym, 1.6, INK); disc(a, xr + 4, ym, 0.8, (210, 214, 224, 255))  # the pivot
    save(a, "crank", "front")
    ys, xs = np.where(op(a)); fx0 = xs.min(); face = (fx0 + 6, y0 + 8, fx0 + 34, y0 + 22)
    hb.mirrored_features("crank", face)
    return face

def forge_back():
    a = load_any("forge", "front"); print("forge porthole", h4.paint_out(a, (22, 19, 34, 30), body_grey(a, (14, 14, 40, 32))))
    save(a[:, ::-1].copy(), "forge", "back")

def lens():
    """LENSMUSAI: the lens bigger (the face one big round lens); back = the front mirrored, the lens painted out"""
    a = load_any("lensmusai", "front"); cx, cy = 29, 29
    disc(a, cx, cy, 11.4, INK); disc(a, cx, cy, 10.4, RING); disc(a, cx, cy, 8.6, INK); disc(a, cx, cy, 7.8, GLASS)
    disc(a, cx - 3, cy - 3, 2.0, SHINE); disc(a, cx + 3, cy + 3, 0.9, (120, 122, 140, 255))
    save(a, "lensmusai", "front")
    b = a.copy(); disc(b, cx, cy, 10.4, (228, 230, 236, 255)); disc(b, cx, cy - 2, 6, (240, 242, 246, 255))
    save(b[:, ::-1].copy(), "lensmusai", "back")

def visor():
    """CODEMUSAI: the visor band wider and deeper across the helmet, two red eye-lights in it"""
    a = load_any("codemusai", "front"); mk = is_mark(a)
    for y in range(24, 37):
        for x in range(17, 47):
            if a[y, x, 3] <= 127 or mk[y, x]: continue
            a[y, x] = INK if y in (24, 36) else DARKG
    R1, R2 = (210, 40, 40, 255), (250, 150, 130, 255)
    for ex in (21, 36):
        for y in range(28, 32):
            for x in range(ex, ex + 6): a[y, x] = R2 if y == 28 else R1
    save(a, "codemusai", "front")

def phones(k="front", cx0=32, cy0=27, rx=18, ry=15.5, cups=(13, 51), yt=20, yb=36):
    """CAREMUSAI: bigger headphones -- a cup each side of the helmet and a band over the top"""
    a = load_any("caremusai", k); C, Ch = (84, 86, 98, 255), (150, 152, 166, 255)
    for t in np.linspace(np.pi, 2 * np.pi, 80):           # the band, behind the helmet
        x, y = cx0 + rx * np.cos(t), cy0 + ry * np.sin(t)
        for r, c in ((1.9, INK), (1.0, C)):
            for yy in range(int(y - 2), int(y + 3)):
                for xx in range(int(x - 2), int(x + 3)):
                    if 0 <= yy < 64 and 0 <= xx < 64 and (xx - x) ** 2 + (yy - y) ** 2 <= r * r and (a[yy, xx, 3] <= 127 or tuple(a[yy, xx]) in (INK, C)):
                        a[yy, xx] = c
    for cx in cups:
        for y in range(yt, yb + 1):
            for x in range(cx - 4, cx + 5):
                edge = y in (yt, yb) or x in (cx - 4, cx + 4)
                corner = (y in (yt, yb)) and (x in (cx - 4, cx + 4))
                if corner: continue
                a[y, x] = INK if edge else (Ch if x == cx - 2 + (0 if cx < 32 else 3) and yt + 2 < y < yb - 2 else C)
    save(a, "caremusai", k)

def phones_back():
    scaled_back("caremusai", 38, 58)
    a = load_any("caremusai", "back"); o = op(a); ys, xs = np.where(o); y0, y1 = ys.min(), ys.max()
    hy1 = y0 + int((y1 - y0) * 0.66); hx = np.where(o[y0:hy1].any(0))[0]; x0, x1 = hx.min(), hx.max()
    cx, cy = (x0 + x1) / 2, (y0 + hy1) / 2
    phones("back", cx, cy, (x1 - x0) / 2 + 1, (hy1 - y0) / 2 + 1, (round(x0 - 3), round(x1 + 3)), round(cy - 8), round(cy + 8))

def mask():
    """MASKMUSAI: the blank mask bigger -- one smooth pale plate over the whole face"""
    hb.mirrored_features("maskmusai", (0, 0, 1, 1))     # the back first: no mask seen from behind
    a = load_any("maskmusai", "front"); cx, cy, rx, ry = 32, 24, 12.5, 10.5; mk = is_mark(a)
    for y in range(64):
        for x in range(64):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d > 1.0 or mk[y, x]: continue
            a[y, x] = INK if d > 0.80 else ((196, 200, 210, 255) if y > cy + 6 else (236, 238, 244, 255))
    save(a, "maskmusai", "front")

def musai2():
    """MUSAI: a second antenna, the first one mirrored onto the left of the helmet"""
    a = load_any("musai", "front")
    for y in range(9, 19):
        for x in range(38, 48):
            if a[y, x, 3] > 127 and (y < 17 or a[y, 63 - x - 1, 3] <= 127): a[y, 63 - x - 1] = a[y, x]
    save(a, "musai", "front")

def escalate_head():
    """ESCALATE: the head simplified -- three greys by value, one green for the crest, the red eye and the outline kept,
    then a 3x3 majority pass to take the speckle out"""
    a = load_any("escalate", "front"); x0, y0, x1, y1 = 13, 5, 44, 31
    L = lum(a); mk = is_mark(a); lab = np.full((64, 64), -1)
    BANDS = [(84, 88, 98, 255), (148, 152, 160, 255), (212, 216, 222, 255), (60, 140, 90, 255)]
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = a[y, x]
            if p[3] <= 127 or mk[y, x] or L[y, x] < 50: continue
            if p[0] - p[1] > 60: continue                     # the red eye
            lab[y, x] = 3 if p[1] - p[0] > 30 else (0 if L[y, x] < 115 else 1 if L[y, x] < 180 else 2)
    for _ in range(2):
        new = lab.copy()
        for y in range(y0, y1):
            for x in range(x0, x1):
                if lab[y, x] < 0: continue
                nb = [lab[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if lab[y + dy, x + dx] >= 0]
                new[y, x] = max(set(nb), key=nb.count)
        lab = new
    for y in range(y0, y1):
        for x in range(x0, x1):
            if lab[y, x] >= 0: a[y, x] = BANDS[lab[y, x]]
    save(a, "escalate", "front")

def magtape_eyes():
    """MAGTAPE: two small eyes looking out of the shell's opening"""
    a = load_any("magtape", "front")
    for ex in (20, 25):
        for y in range(31, 35):
            for x in (ex, ex + 1): a[y, x] = INK
        a[31, ex] = SHINE
    save(a, "magtape", "front")

def phase2():
    crank(); forge_back(); lens(); visor(); phones(); phones_back(); mask(); musai2(); escalate_head(); magtape_eyes()
    hb.mirrored_features("escalate", (10, 12, 32, 30))      # its back from the simplified head

GROUNDS = (("musai", "front", 0.85, dict(minL=110)),
           ("caremusai", "front", 0.85, dict(minL=110)),
           ("codemusai", "front", 0.85, dict(minL=110)), ("codemusai", "back", 0.85, dict(minL=110)),
           ("ferry", "back", 0.85, dict(minL=110)),
           ("lensmusai", "front", 0.85, dict(minL=110)), ("lensmusai", "back", 0.85, dict(minL=110)),
           ("overlay", "front", 0.85, dict(minL=110)), ("cinder", "back", 0.85, dict(minL=110)),
           ("maskmusai", "front", 0.88, dict(minL=110)))
BACKS = {}   # name -> face box, the front mirrored with the features off; filled below

if __name__ == "__main__":
    os.makedirs(H, exist_ok=True)
    for f in os.listdir(H): os.remove(f"{H}/{f}")
    for n, k, lo, kw in GROUNDS:
        a = load_any(n, k); print(n, k, "ground", ug(a, lo, **kw)); save(a, n, k)
    dynamo(); fins()
    a = load_any("maskmusai", "front"); print("maskmusai mask features", hb.features_off(a, (20, 19, 44, 31))); save(a, "maskmusai", "front")
    scaled_back("codemusai", 40, 58)
    a = load_any("codemusai", "back"); print("codemusai back spot", h4.paint_out(a, (28, 29, 36, 37), (150, 150, 152, 255))); save(a, "codemusai", "back")
    fins("back", (13, 34), (6, 41), 24, 31); scaled_back("seekmusai", 44, 60)
    hb.mirrored_features("stub", (8, 25, 37, 41))
    a = load_any("mock", "back"); print("mock eye", h4.paint_out(a, (34, 12, 48, 26), body_grey(a, (30, 26, 50, 36)))); save(a, "mock", "back")
    ch = json.load(open(F + "/choose.json"))
    for n, v in ch.items():
        if v.get("hand-back") and n not in ("maskmusai", "escalate"): hb.mirrored_features(n, tuple(v["hand-back"]))
    phase2()
    for n in NAMES:
        for k in ("front", "back"):
            if not os.path.exists(f"{F}/clean/{n}_{k}.png"): continue
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", sorted(os.listdir(H)))

"""T-452 batch 8, by hand (the user's answers via the coordinator, 2026-10-27). hand4.py's and hand_b5.py's helpers.

    hand_b8.py      writes T/k/hand/<name>_{front,back,icon}.png (from k/clean, kp/clean and k/reduced)

PROMETHEUS  the flame crest painted back (its mask from kp/, the same draft reduced with the cap at 25%, which kept it):
            CRIMSON, not red or yellow -- gbasprite.shift_off turns any accent within 40 degrees of the type's hue
            (FIRE, 38 degrees) to the far side of the wheel, which is what made the crest blue in kp/. Crimson (350)
            sits 48 away and stays; the crest's light core is left light grey, which the ramp makes its pale
            highlight. The beak and talons greyed so the accents stay under 15%. The back: the crest the same way,
            its orange ground off.
DEADLOCK    TWO smaller sitters (its entry: "Two of them are each waiting for the other"), each 0.7 of the drawn
            one, face to face -- the left one mirrored -- each with its own lock; the streak markers (four strokes)
            redrawn once on the right one's belly. The back: the pair mirrored, faces and locks off. The icon from the
            pair, darker and cleaner (icon_dark below).
STARR       a small gold star between the antlers.
PUNCHCARD   the big eye painted out to card and a small one drawn high; rows of small dark square holes punched below
            it; the top right corner clipped. Icon by icon3 from the hand front.
BACKS       CANARY, SINGULAR, MOMENTUM, TEPID: the front MIRRORED with the face's features painted out (hand_b5).
GROUNDS     CURRICULUM's front (and the white tablet between its legs: the streak markers on it moved up to the flank)
            and back; STEEPEST's line and puddle; PROMETHEUS's back; CANARY's and MOMENTUM's front shadows (before
            they are mirrored).
ICONS       DEADLOCK and ASCLEPIUS darker and cleaner: icon3 from the front smoothed by a 3x3 median, with the three
            value bands cut at the 40th and 92nd percentiles (not k-means): more dark, a little light."""
import os, sys, shutil, colorsys
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hand4 as h4
import hand_b5 as hb
R = "/Users/christopherhicks/Projects/DAEMONS"; T = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452"); F = T + "/k"; H = F + "/hand"
hb.F, hb.H = F, H; h4.F, h4.H = F, H
from hand4 import load_any, sanitize, save, ug, outline, op, lum, is_mark, INK, MARK
NAMES = ["drum", "punchcard", "fossilnet", "deadlock", "orpheus", "asclepius", "prometheus", "canary", "emergence", "singular",
         "starr", "primer", "syllabus", "curriculum", "tepid", "seethe", "heatdeath", "learnrate", "momentum", "steepest"]

def grey_at(a, y, x):
    l = int(lum(a[y:y + 1, x:x + 1])[0, 0]); a[y, x, :3] = (l, l, min(255, l + 4))

# ---- PROMETHEUS
CRIMSON = ((120, 12, 40), (196, 22, 58), (236, 70, 96))
def flame(a, src, rows):
    """cells of SRC (the uncapped clean grid) in ROWS that are red-orange and saturated -> crimson by value on A"""
    L = lum(src); n = 0
    for y in range(*rows):
        for x in range(64):
            R_, G_, B_, A_ = src[y, x]
            if A_ <= 127 or a[y, x, 3] <= 127 or is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
            h, s, v = colorsys.rgb_to_hsv(R_ / 255, G_ / 255, B_ / 255)
            if s > 0.45 and (h < 0.12 or h > 0.95) and v > 0.4:
                l = L[y, x]; a[y, x, :3] = CRIMSON[0] if l < 100 else (CRIMSON[1] if l < 165 else CRIMSON[2]); n += 1
    return n

def prometheus():
    a = load_any("prometheus", "front"); src = np.array(Image.open(T + "/kp/clean/prometheus_front.png").convert("RGBA")).astype(int)
    print("prometheus crest cells", flame(a, src, (0, 18)))
    #  every other saturated cell (beak, talons, the eye ring) to grey at its own value
    sat = a[..., :3].max(-1) - a[..., :3].min(-1); mk = is_mark(a); k = 0
    for y, x in zip(*np.where(op(a) & (sat >= 60) & ~mk)):
        if tuple(a[y, x, :3]) in CRIMSON: continue
        grey_at(a, y, x); k += 1
    print("prometheus greyed", k); save(a, "prometheus", "front")
    b = load_any("prometheus", "back"); print("prometheus back ground", ug(b, 0.90, minL=110))
    #  the back's crest (rows 2-17, left of x 32) is grey in the clean: crimson by value, the light core left
    L = lum(b); n = 0
    for y in range(2, 18):
        for x in range(6, 32):
            if b[y, x, 3] <= 127 or L[y, x] < 60 or is_mark(b[y:y + 1, x:x + 1])[0, 0]: continue
            l = L[y, x]; b[y, x, :3] = CRIMSON[0] if l < 110 else (CRIMSON[1] if l < 170 else CRIMSON[2]); n += 1
    sat = b[..., :3].max(-1) - b[..., :3].min(-1); mk = is_mark(b)
    for y, x in zip(*np.where(op(b) & (sat >= 60) & ~mk)):
        if tuple(b[y, x, :3]) not in CRIMSON: grey_at(b, y, x)
    print("prometheus back crest cells", n); save(b, "prometheus", "back")

# ---- DEADLOCK: the pair
def strip_marks(a):
    """streak markers off: each takes the median of its non-marker opaque neighbours"""
    mk = is_mark(a)
    for y, x in zip(*np.where(mk)):
        nb = [a[y + dy, x + dx] for dy in (-2, -1, 0, 1, 2) for dx in (-2, -1, 0, 1, 2)
              if 0 <= y + dy < 64 and 0 <= x + dx < 64 and a[y + dy, x + dx, 3] > 127 and not mk[y + dy, x + dx]]
        a[y, x] = np.median(np.array(nb), 0).astype(int) if nb else a[y, x]

def pair(single, sc=0.6):
    s = single.copy(); ys, xs = np.where(op(s)); s = s[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = Image.fromarray(s.astype(np.uint8), "RGBA"); w, h = round(im.width * sc), round(im.height * sc)
    c = np.array(im.resize((w, h), Image.NEAREST)).astype(int); L = c[:, ::-1].copy()
    out = np.zeros((64, 64, 4), int); y0 = 63 - h
    def put(img, x0, yy):
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                if img[y, x, 3] > 127 and 0 <= yy + y < 64 and 0 <= x0 + x < 64: out[yy + y, x0 + x] = img[y, x]
    put(L, 0, y0 - 1)                 # the left one, a step behind, facing right
    put(c, 64 - w - 1, y0)            # the right one in front, facing left
    return out, (64 - w - 1, y0, w, h)

def deadlock():
    a = load_any("deadlock", "front"); marks = [(y, x, a[y, x].copy()) for y, x in zip(*np.where(is_mark(a)))]
    s = a.copy(); strip_marks(s)
    p, (rx, ry, w, h) = pair(s)
    #  the four strokes once, on the right one's belly: the original pattern, its box's centre moved to the belly
    my = np.mean([m[0] for m in marks]); mx = np.mean([m[1] for m in marks])
    cy = ry + h * 0.62; cx = rx + w * 0.5   # the middle of the right one's belly
    for y, x, c in marks:
        yy, xx = int(round(cy + (y - my))), int(round(cx + (x - mx)))
        if 0 <= yy < 64 and 0 <= xx < 64 and p[yy, xx, 3] > 127: p[yy, xx] = c
    save(p, "deadlock", "front")
    #  the back: faces and locks off the single one, then the pair, mirrored
    b = s.copy(); print("deadlock face cells", hb.features_off(b, (10, 8, 42, 28)), "lock cells", hb.features_off(b, (14, 36, 26, 63)))
    sat = b[..., :3].max(-1) - b[..., :3].min(-1)
    for y, x in zip(*np.where(op(b) & (sat >= 60))): grey_at(b, y, x)
    bp, _ = pair(b)
    #  the strokes at the same place as on the front, mirrored with it
    q = bp[:, ::-1].copy()
    for y, x, c in marks:
        yy, xx = int(round(cy + (y - my))), int(round(cx + (x - mx)))
        xx = 63 - xx
        if 0 <= yy < 64 and 0 <= xx < 64 and q[yy, xx, 3] > 127: q[yy, xx] = c
    save(q, "deadlock", "back")

# ---- STARR: a small gold star between the antlers
GOLD = {"#": (110, 70, 16, 255), "Y": (240, 190, 40, 255), "W": (252, 236, 150, 255)}
STAR = ["   #   ", "  #Y#  ", "##YWY##", " #YYY# ", "  #Y#  "]
def starr():
    a = load_any("starr", "front"); ys, xs = np.where(op(a)); top = ys.min(); m = ys < top + 10
    cx = (xs[m].min() + xs[m].max()) // 2
    h4.stamp(a, cx - 3, top + 3, STAR, GOLD); save(a, "starr", "front")

# ---- PUNCHCARD
CARD_INK = (34, 30, 40, 255)
def punchcard():
    a = load_any("punchcard", "front")
    #  the card's own paper: the median of its light cells (body_grey's 100-200 band took the grey arms)
    reg = a[14:50, 22:44].reshape(-1, 4); rl = lum(reg[None])[0]
    card = tuple(int(v) for v in np.median(reg[(reg[:, 3] > 127) & (rl >= 170) & (rl < 245)], 0))
    #  the big eye (and the two dark marks under it) to card
    for y in range(20, 45):
        for x in range(22, 44):
            if a[y, x, 3] > 127 and not is_mark(a[y:y + 1, x:x + 1])[0, 0] and all(
                    a[y + dy, x + dx, 3] > 127 for dy in (-1, 0, 1) for dx in (-1, 0, 1)) and not (y < 17):
                a[y, x] = card
    #  a small eye, high
    h4.stamp(a, 30, 18, [" ### ", "#WWW#", "#W#W#", "#WWW#", " ### "], {"#": INK, "W": (236, 236, 240, 255)})
    #  four rows of five 2x2 holes
    for ry in (26, 30, 34, 38):
        for rx in (23, 27, 31, 35, 39):
            for y in (ry, ry + 1):
                for x in (rx, rx + 1):
                    if a[y, x, 3] > 127 and not is_mark(a[y:y + 1, x:x + 1])[0, 0]: a[y, x] = CARD_INK
    #  the clipped corner, top right
    ys, xs = np.where(op(a[:20, 18:48])); top = ys.min(); right = 18 + xs.max()
    for d in range(6):
        for x in range(right - 5 + d, right + 1):
            a[top + d, x] = 0
        a[top + d, right - 5 + d] = INK
    save(a, "punchcard", "front")

# ---- grounds
def curriculum():
    a = load_any("curriculum", "front"); print("curriculum front ground", ug(a, 0.85, minL=100))
    #  the tablet: the pale block between the legs (x 30-37, y 40-56) off; its four markers moved up 10 rows
    marks = [(y, x, a[y, x].copy()) for y, x in zip(*np.where(is_mark(a)))]
    L = lum(a)
    for y in range(40, 58):
        for x in range(30, 38):
            if a[y, x, 3] > 127 and (L[y, x] > 170 or is_mark(a[y:y + 1, x:x + 1])[0, 0]): a[y, x] = 0
    for y, x, c in marks:
        for dy in (12, 11, 13, 10):
            if a[y - dy, x, 3] > 127 and not is_mark(a[y - dy:y - dy + 1, x:x + 1])[0, 0]: a[y - dy, x] = c; break
    outline(a, (38, 60)); save(a, "curriculum", "front")
    b = load_any("curriculum", "back"); print("curriculum back ground", ug(b, 0.85, minL=110)); save(b, "curriculum", "back")

def steepest():
    a = load_any("steepest", "front"); print("steepest front ground", ug(a, 0.90, minL=110)); save(a, "steepest", "front")
    b = load_any("steepest", "back"); print("steepest back ground", ug(b, 0.80, minL=110)); save(b, "steepest", "back")

# ---- icons
def icon_dark(n, typ, src):
    import icon3
    a = Image.open(src).convert("RGBA"); al = a.getchannel("A")
    rgb = a.convert("RGB").filter(ImageFilter.MedianFilter(3)); sm = rgb.convert("RGBA"); sm.putalpha(al)
    tmp = f"{H}/_{n}_smooth.png"; sm.save(tmp)
    def bands(v):
        #  thresholds, not centres: the darkest 40% dark, the lightest 8% light (k-means split a pale body down the middle)
        t1, t2 = np.percentile(v, [40, 92]); c1 = (t1 + t2) / 2; return np.array([2 * t1 - c1, c1, 2 * t2 - c1])
    k0 = icon3.kmeans3; icon3.kmeans3 = bands
    try: r = icon3.make(n, typ, tmp, f"{H}/{n}_icon.png")
    finally: icon3.kmeans3 = k0; os.remove(tmp)
    print(n, "icon (dark)", r["icon_palette"], r["ramp"])

def despeckle(n, k, maxn=8):
    """opaque islands of at most MAXN cells, off (what a ground flood leaves of a tail tip or a shadow's rim)"""
    a = load_any(n, k); o = op(a); seen = np.zeros_like(o); gone = 0
    for y, x in zip(*np.where(o)):
        if seen[y, x]: continue
        st, mem = [(y, x)], []; seen[y, x] = True
        while st:
            p = st.pop(); mem.append(p)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    q = (p[0] + dy, p[1] + dx)
                    if 0 <= q[0] < 64 and 0 <= q[1] < 64 and o[q] and not seen[q]: seen[q] = True; st.append(q)
        if len(mem) <= maxn and not any(is_mark(a[None, None, q[0], q[1]])[0, 0] for q in mem):
            for q in mem: a[q] = 0
            gone += len(mem)
    if gone: save(a, n, k); print(n, k, "islands off", gone)

def trim_accents(n, k, cap=0.149):
    """over the cap after a ground came off (fewer body cells): the largest accent patch's cells nearest its edge
    greyed, one at a time, until the share is under CAP"""
    a = load_any(n, k); o = op(a); mk = is_mark(a); sat = a[..., :3].max(-1) - a[..., :3].min(-1)
    acc = o & ~mk & (sat >= 60); need = int(acc.sum() - cap * o.sum()) + 1
    if need <= 0: return
    ys, xs = np.where(acc); cy, cx = ys.mean(), xs.mean()
    order = sorted(zip(ys, xs), key=lambda p: -((p[0] - cy) ** 2 + (p[1] - cx) ** 2))
    for y, x in order[:need]: grey_at(a, y, x)
    save(a, n, k); print(n, k, "accent cells greyed", need)

def icon_plain(n, typ, src):
    import icon3; r = icon3.make(n, typ, src, f"{H}/{n}_icon.png"); print(n, "icon", r["icon_palette"], r["ramp"])

if __name__ == "__main__":
    os.makedirs(H, exist_ok=True)
    for f in os.listdir(H): os.remove(f"{H}/{f}")
    import json
    P = json.load(open(F + "/picks.json")); TY = {n: P[n]["type"] for n in NAMES}
    prometheus(); deadlock(); starr(); punchcard(); curriculum(); steepest()
    for n, lo in (("canary", 0.85), ("momentum", 0.80)):
        a = load_any(n, "front"); print(n, "front ground", ug(a, lo, minL=110)); save(a, n, "front")
    c = load_any("canary", "front"); print("canary features", hb.features_off(c, (14, 10, 34, 32)), "belly", hb.features_off(c, (16, 32, 34, 50)))
    save(c[:, ::-1].copy(), "canary", "back")
    hb.mirrored_features("singular", (22, 22, 42, 40))
    hb.mirrored_features("momentum", (6, 15, 26, 34))
    hb.mirrored_features("tepid", (9, 14, 36, 33))
    for n, k in (("steepest", "back"), ("steepest", "front"), ("curriculum", "front"), ("curriculum", "back"), ("prometheus", "back"),
                 ("canary", "front"), ("momentum", "front"), ("canary", "back"), ("momentum", "back")):
        despeckle(n, k, maxn={("steepest", "back"): 24, ("curriculum", "front"): 12}.get((n, k), 8))
    for n in NAMES:
        for k in ("front", "back"):
            trim_accents(n, k)
    for n in NAMES:
        for k in ("front", "back"):
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    os.chdir(R)
    icon_dark("deadlock", TY["deadlock"], f"{H}/deadlock_front.png")
    icon_dark("asclepius", TY["asclepius"], f"{F}/clean/asclepius_front.png")
    icon_plain("punchcard", TY["punchcard"], f"{H}/punchcard_front.png")
    icon_plain("prometheus", TY["prometheus"], f"{H}/prometheus_front.png")
    print("written", sorted(os.listdir(H)))

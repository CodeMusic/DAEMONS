"""T-452 batch 4's follow-ups by hand (the user, 2026-10-27), on top of hand4.py's files in g/hand/.

LEMMA MIND  the second pair of arms IN FRONT: two thick forearms crossed over the belly, from the hips up to a fist
            under each opposite pec (drawn from the clean front, so hand4's arms-behind are gone); from behind, the
            crossed arms show as an elbow out at each side of the waist; the icon gets a small X of arms under the chin.
HONEYPOT    a honey pot, not a teacup: the cup's handle taken off, two dark bands round the pot (above and below the
            face), and a leaf lid tipped open on the rim, front; on the back the handles off and the lid on the rim.
STACK       a boulder (fix4.py's i2i 5264, back turned 5272): its ground shadow off, two round boulder fists at its sides.
QUORUM      three pods (its entry: "Three of them"), drawn: no draft in eight drew three. Front with a lens each,
            back plain; the streak markers on the lower right pod.
Run after hand4.py (which empties g/hand/); writes STACK's and QUORUM's icons by icon3 last."""
import os, sys, json
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from hand4 import load, load_any, save, lum, op, is_mark, outline, body_grey, sanitize, F, H, INK

def seg_d(x, y, a, b):
    (x0, y0), (x1, y1) = a, b; dx, dy = x1 - x0, y1 - y0
    t = max(0, min(1, ((x - x0) * dx + (y - y0) * dy) / float(dx * dx + dy * dy)))
    return ((x - x0 - t * dx) ** 2 + (y - y0 - t * dy) ** 2) ** 0.5

def shade(base, k): return tuple(int(max(0, min(255, v * k))) for v in base[:3]) + (255,)

def limb(a, p0, p1, w, base, fist=None):
    """a thick band P0->P1 (half-width W), lit on its upper edge, with an ink rim; FIST a round end at P1"""
    lt, md, dk = shade(base, 1.25), shade(base, 1.0), shade(base, 0.72)
    cells = {}
    for y in range(64):
        for x in range(64):
            d = seg_d(x + .5, y + .5, p0, p1)
            if fist: d = min(d, ((x + .5 - p1[0]) ** 2 + (y + .5 - p1[1]) ** 2) ** 0.5 - (fist - w))
            if d <= w + 1.0: cells[(y, x)] = d
    for (y, x), d in cells.items():
        if d > w: a[y, x] = INK; continue
        up = cells.get((y - 1, x), 99) > w            # the top edge of the band catches the light
        dn = cells.get((y + 1, x), 99) > w
        a[y, x] = lt if up else (dk if dn else md)
    if fist:                                           # two knuckle creases
        fx, fy = p1
        for k in (-1, 1): a[int(fy) + k, int(fx) - 1:int(fx) + 2] = INK

def lemma():
    a = load("lemma mind", "front"); base = body_grey(a, (22, 18, 42, 38))
    limb(a, (47, 46), (25, 33), 2.6, base, fist=3.6)    # the under arm first
    limb(a, (17, 46), (39, 33), 2.6, base, fist=3.6)    # then the one crossing over it
    save(a, "lemma mind", "front")
    b = load("lemma mind", "back"); base = body_grey(b, (22, 26, 42, 40))
    for p0, p1 in (((17, 46), (10, 49)), ((47, 46), (54, 49))):   # an elbow out below each upper arm
        e = b.copy(); limb(e, p0, p1, 2.2, base, fist=3.2)
        m = (np.abs(e - b).sum(2) > 0) & ((~op(b)) | (np.arange(64)[None, :] < 18) | (np.arange(64)[None, :] > 46))
        b[m] = e[m]
    save(b, "lemma mind", "back")
    #  the icon: a small X under the chin in icon3's ramp, frame 2 one row lower
    src = f"{F}/reduced/lemma mind_icon.png"; im = Image.open(src); g = np.array(im)
    dk, md, lt = json.load(open(F + "/picks.json"))["lemma mind"]["measured"]["icon3"]["ramp"]
    #  a fist each side of the chin and the forearm crossing under it
    X = ["####...............####",
         "#LL#...............#LL#",
         "#LLL#.............#LLL#",
         "#LLLL#############LLLL#",
         ".#LLLLLLLLLLLLLLLLLLL#.",
         "..###################.."]
    oy, ox = 24, 4
    for dy, row in enumerate(X):
        for dx, ch in enumerate(row):
            y, x = oy + dy, ox + dx
            if ch == "#": g[y, x] = 15
            elif ch == "L": g[y, x] = lt
    g[32:] = 0; g[33:64] = g[0:31]
    out = Image.fromarray(g.astype(np.uint8), "P"); out.putpalette(im.getpalette()); out.save(f"{H}/lemma mind_icon.png")

LEAF = (176, 214, 140, 255); LEAFD = (112, 160, 92, 255); BAND = (70, 66, 74, 255)

def lid(a, cx, cy, rx, ry, tilt):
    """a leaf lid: a flat oval leaf tipped up by TILT rows across its width, a dark midrib, an ink rim"""
    cells = {}
    for y in range(64):
        for x in range(64):
            yy = y - cy + tilt * (x - cx) / rx
            d = ((x - cx) / rx) ** 2 + (yy / ry) ** 2
            if d <= 1.45: cells[(y, x)] = d
    for (y, x), d in cells.items():
        a[y, x] = INK if d > 1.0 else LEAF
    for x in range(cx - rx + 2, cx + rx - 1):
        y = int(round(cy - tilt * (x - cx) / rx))
        if (y, x) in cells and cells[(y, x)] <= 1.0: a[y, x] = LEAFD
    a[cy - int(tilt) - ry - 1:cy - int(tilt) - ry + 1, cx + rx - 2] = INK   # a little stalk at the tip

def honeypot():
    a = load_any("honeypot", "front")
    a[35:46, 40:46] = 0; outline(a, (34, 47))                          # the teacup's handle off
    o = op(a); L = lum(a); mk = is_mark(a)
    for y in (33, 34, 42, 43):                                         # two bands round the pot
        for x in range(24, 39):
            if o[y, x] and not mk[y, x] and L[y, x] >= 60 and all(o[y, x + d] for d in (-1, 1)): a[y, x] = BAND
    lid(a, 30, 29, 10, 2, 2.5)
    save(a, "honeypot", "front")
    b = load_any("honeypot", "back")
    b[33:43, 12:21] = 0; b[36:44, 40:46] = 0; outline(b, (32, 44))
    lid(b, 31, 31, 11, 2, -2.0)
    save(b, "honeypot", "back")

MARKS = [(255, 0, 255, 255), (0, 255, 255, 255), (255, 255, 0, 255), (0, 255, 0, 255)]

def pod(a, cx, cy, r, eye=True):
    """one round metal pod, lit from the upper left, an ink rim; EYE a lens: dark ring, grey iris, a pinpoint pupil,
    one highlight"""
    GREY = [(236, 236, 240, 255), (200, 202, 208, 255), (160, 162, 170, 255), (118, 120, 130, 255), (84, 86, 96, 255)]
    for y in range(64):
        for x in range(64):
            dx, dy = x + .5 - cx, y + .5 - cy; d = (dx * dx + dy * dy) ** 0.5
            if d > r + 1.0: continue
            if d > r: a[y, x] = INK; continue
            lit = (-dx * 0.6 - dy * 0.8) / r                 # -1 .. 1, the light from the upper left
            k = 0 if lit > 0.55 else 1 if lit > 0.15 else 2 if lit > -0.3 else 3 if lit > -0.7 else 4
            a[y, x] = GREY[k]
    if eye:
        ex, ey, er = cx + 0.5, cy + 1.5, r * 0.5
        for y in range(64):
            for x in range(64):
                d = ((x + .5 - ex) ** 2 + (y + .5 - ey) ** 2) ** 0.5
                if d <= er + 0.9 and d > er - 0.2: a[y, x] = INK
                elif d <= er - 0.2: a[y, x] = (96, 110, 128, 255) if d > er * 0.45 else (30, 32, 40, 255)
        a[int(ey - er * 0.45), int(ex - er * 0.35)] = (250, 250, 252, 255)

def quorum():
    """three pods in a pyramid (its entry: 'Three of them'), the top one behind the two below; the streak markers on
    the lower left pod, where the other daemons carry theirs"""
    for k, eye in (("front", True), ("back", False)):
        a = np.zeros((64, 64, 4), int)
        pod(a, 32, 22, 11, eye); pod(a, 21, 41, 11, eye); pod(a, 43, 41, 11, eye)
        for i, m in enumerate(MARKS):
            for j in range(3): a[44 + j - i // 2, 46 + 2 * i + (2 - j) // 2 + (i % 2)] = m
        save(a, "quorum", k)

def fist(a, cx, cy, r, base):
    """a round boulder fist: rock greys lit from the upper left, an ink rim, two knuckle cracks"""
    sh = [shade(base, k) for k in (1.3, 1.1, 0.9, 0.7)]
    for y in range(64):
        for x in range(64):
            dx, dy = x + .5 - cx, y + .5 - cy; d = (dx * dx + dy * dy) ** 0.5
            if d > r + 1.0: continue
            if d > r: a[y, x] = INK; continue
            lit = (-dx * 0.6 - dy * 0.8) / r
            a[y, x] = sh[0 if lit > 0.45 else 1 if lit > 0 else 2 if lit > -0.5 else 3]
    for k in (-2, 1): a[int(cy) + k, int(cx) - 2:int(cx) + 2] = INK

def stack():
    """STACK as a boulder (the user, 2026-10-27): the ground shadow off; its key, the two boulder fists, at its sides"""
    from hand4 import ug
    for k in ("front", "back"):
        a = load("stack", k); print("stack", k, "ground", ug(a, 0.80, minL=100))
        base = body_grey(a, (14, 14, 50, 46))
        fist(a, 12, 45, 6.5, base); fist(a, 52, 45, 6.5, base)
        save(a, "stack", k)

if __name__ == "__main__":
    lemma(); honeypot(); quorum(); stack()
    for n in ("lemma mind", "honeypot", "quorum", "stack"):
        for k in ("front", "back"):
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    #  STACK's and QUORUM's icons: icon3 from the hand fronts (picks.json's icon3 rows rewritten for build4 iconpal)
    import icon3
    os.chdir("/Users/christopherhicks/Projects/DAEMONS"); P = json.load(open(F + "/picks.json"))
    for n in ("stack", "quorum"):
        P[n]["measured"]["icon3"] = icon3.make(n, P[n]["type"], f"{H}/{n}_front.png", f"{H}/{n}_icon.png")
    json.dump(P, open(F + "/picks.json", "w"), indent=1)
    print("ok")

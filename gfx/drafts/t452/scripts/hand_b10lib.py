"""hand_b10.py's helpers without its side effects (batch 11 imports this; P is set by the importer)"""

import os, sys, json, colorsys, shutil
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hand4 as h4
import hand_b5 as hb
import gbs
T = os.environ["T452_ROOT"]; F = T + "/o"; H = F + "/hand"
hb.F, hb.H = F, H; h4.F, h4.H = F, H
from hand4 import load_any, save, ug, sanitize, stamp, op, lum, is_mark, INK
P = {}   # set by the importer
NAMES = ["goldset", "valence", "mood", "elation", "fakeroot", "semaphore", "whim", "caprice", "abandon", "grasp", "starved",
         "quota", "periphery", "apathy", "torpor", "omen", "kernel", "dread", "rankle", "resentment"]
def thue(n): return colorsys.rgb_to_hsv(*[c / 255 for c in gbs.TYPE_COLOR[P[n]["type"]]])[0]
def hsv(a, y, x): return colorsys.rgb_to_hsv(*(a[y, x, :3] / 255))
def grey_at(a, y, x):
    l = int(lum(a[y:y + 1, x:x + 1])[0, 0]); a[y, x, :3] = (l, l, min(255, l + 4))
def in_reach(n, h):
    d = abs(h - thue(n)); return min(d, 1 - d) < 40 / 360
def acc_mask(a): return op(a) & ~is_mark(a) & ((a[..., :3].max(-1) - a[..., :3].min(-1)) >= 60)

def trap(n, k, mode, box=(0, 0, 64, 64), to=None, s_min=0.25, acc_only=False):
    """cells in BOX whose hue sits within 40 of the type's: 'grey' (into the ramp), 'hue' (to TO degrees), 'dark'"""
    a = load_any(n, k); x0, y0, x1, y1 = box; m = 0
    for y, x in zip(*np.where(op(a) & ~is_mark(a))):
        if not (x0 <= x < x1 and y0 <= y < y1): continue
        h, s, v = hsv(a, y, x)
        if s < s_min or v < 0.2 or not in_reach(n, h): continue
        if acc_only and a[y, x, :3].max() - a[y, x, :3].min() < 60: continue   # only what gbasprite keeps as an accent
        if mode == "grey": grey_at(a, y, x)
        elif mode == "dark": l = int(min(90, lum(a[y:y + 1, x:x + 1])[0, 0] * 0.6)); a[y, x, :3] = (l, l, l + 6)
        else: a[y, x, :3] = [int(c * 255) for c in colorsys.hsv_to_rgb(to / 360, max(s, 0.45), v)]
        m += 1
    save(a, n, k); return m

def halo(n, k):
    """a white sticker border: flood from the transparency through near-white, unsaturated cells, and take them off"""
    a = load_any(n, k); o = op(a); L = lum(a); sat = a[..., :3].max(-1) - a[..., :3].min(-1)
    pale = o & (L >= 222) & (sat < 24) & ~is_mark(a); seen = np.zeros_like(pale); st = []
    for y, x in zip(*np.where(pale)):
        if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not o[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            seen[y, x] = True; st.append((y, x))
    while st:
        y, x = st.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, q = y + dy, x + dx
            if 0 <= p < 64 and 0 <= q < 64 and pale[p, q] and not seen[p, q]: seen[p, q] = True; st.append((p, q))
    a[seen] = 0; save(a, n, k); return int(seen.sum())

GOLD = ((176, 112, 16, 255), (222, 160, 34, 255), (246, 204, 74, 255))
def gold(n, region, face):
    """the grey petals in REGION, outside FACE, to gold by value (outline and markers kept), from the petal TIPS
    inward (farthest from the face's centre first) for as many cells as the 15% cap leaves room for"""
    a = load_any(n, "front"); X0, Y0, X1, Y1 = region; fx0, fy0, fx1, fy1 = face; L = lum(a)
    sat = a[..., :3].max(-1) - a[..., :3].min(-1); cy, cx = (fy0 + fy1) / 2, (fx0 + fx1) / 2; cand = []
    for y in range(Y0, Y1):
        for x in range(X0, X1):
            if not op(a)[y, x] or is_mark(a[y:y + 1, x:x + 1])[0, 0] or (fx0 <= x < fx1 and fy0 <= y < fy1): continue
            if L[y, x] < 95 or L[y, x] > 238 or sat[y, x] >= 60: continue
            cand.append((y, x))
    room = int(0.145 * op(a).sum()) - int(acc_mask(a).sum())
    cand.sort(key=lambda p: -((p[0] - cy) ** 2 + (p[1] - cx) ** 2))
    for y, x in cand[:max(0, room)]: a[y, x] = GOLD[0] if L[y, x] < 140 else (GOLD[1] if L[y, x] < 190 else GOLD[2])
    save(a, n, "front"); return "%d of %d" % (min(max(0, room), len(cand)), len(cand))

BALL = ["   #####   ", "  #LLLLL#  ", " #LWWLLLM# ", "#LWWLLLLMM#", "#LWLLLLLMM#", "#LLLLLLLMM#", "#LLLLLLMMM#",
        "#MLLLLMMMD#", " #MMMMMMD# ", "  #DDDDD#  ", "   #####   "]
GREYS = {"#": INK, "L": (200, 204, 210, 255), "W": (246, 248, 252, 255), "M": (160, 164, 172, 255), "D": (118, 122, 130, 255)}
def valence():
    a = load_any("valence", "front")
    stamp(a, 50, 24, BALL, GREYS)
    for y in (34, 35, 36): stamp(a, 54, y, ["#"], GREYS, behind=True)   # the tail's last cells up into the ball
    save(a, "valence", "front")

HAND = [" ## ## ## ", "#LL#LL#LL#", "#LL#LL#LL#", "#LL#LL#LL#", "#LLLLLLLL#", "#LLLLLLLM#", "#LLLLLLMM#", " #LLLLMM# ",
        "  #MMMM#  ", "   #LL#   ", "   #LL#   "]
def grasp():
    a = load_any("grasp", "front"); stamp(a, 49, 36, HAND, GREYS); save(a, "grasp", "front")

PUFF = ["   ## ##   ", "  #WW#WW#  ", " #WWWWWWW# ", "#WWWWWWWLW#", "#WWWWWWWWL#", "#LWWWWWWLL#", " #LLWWLLL# ",
        "  #LL#LL#  ", "   ## ##   "]
def abandon():
    a = load_any("abandon", "front")
    stamp(a, 0, 19, PUFF, GREYS, behind=True); stamp(a, 53, 19, PUFF, GREYS, behind=True); save(a, "abandon", "front")

FLAG = ["#############", "#RRRRRRRRRRR#", "#RRRWWWWRRRR#", "#RRRWWWWRRRR#", "#RRRWWWWRRRR#", "#RRRRRRRRRRR#",
        "#RRRRRRRRRRR#", "#############"]
def semaphore():
    a = load_any("semaphore", "front")
    for y in range(3, 44): stamp(a, 17, y, ["#"], GREYS, behind=True)
    stamp(a, 16, 2, ["##", "##"], GREYS)
    stamp(a, 18, 4, FLAG, {"#": INK, "R": (196, 40, 44, 255), "W": (244, 244, 246, 255)}, behind=True)
    save(a, "semaphore", "front")

GROUND = {"mood": 0.85, "elation": 0.88, "fakeroot": 0.88, "semaphore": 0.88, "whim": 0.85, "abandon": 0.85, "starved": 0.85,
          "apathy": 0.85, "torpor": 0.85, "omen": 0.85, "kernel": 0.85}
FACE = {"valence": (17, 22, 38, 34), "mood": (19, 22, 46, 36), "elation": (26, 22, 52, 36), "fakeroot": (20, 16, 46, 34),
        "semaphore": (20, 25, 48, 38), "whim": (20, 28, 46, 42), "caprice": (12, 36, 48, 50), "abandon": (16, 32, 48, 46),
        "grasp": (6, 16, 38, 34), "starved": (12, 34, 52, 52), "quota": (24, 22, 42, 36), "periphery": (32, 24, 52, 40),
        "apathy": (14, 24, 44, 40), "torpor": (16, 14, 46, 30), "omen": (22, 28, 44, 42), "dread": (20, 22, 40, 34),
        "rankle": (14, 28, 54, 42), "resentment": (12, 28, 56, 40),
        "goldset": (23, 13, 39, 25), "kernel": (18, 24, 46, 42)}

def omen_back():
    """a black crow: hand_b5's fill is the box's LIGHT median, which on dark feathers read as a pale patch -- here the
    face box's interior cells take the feathers' own dark grey"""
    a = load_any("omen", "front"); x0, y0, x1, y1 = FACE["omen"]; o = op(a); L = lum(a); mk = is_mark(a)
    body = a[28:52, 14:50].reshape(-1, 4); bl = lum(body[None])[0]; pool = body[(body[:, 3] > 127) & (bl >= 40) & (bl < 110)]
    fill = np.median(pool, 0).astype(int); fill[3] = 255; m = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if o[y, x] and not mk[y, x] and all(o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): a[y, x] = fill; m += 1
    save(a[:, ::-1].copy(), "omen", "back"); print("omen face cells (dark fill)", m)

def specks(n, k, maxn=4):
    a = load_any(n, k); o = op(a); seen = np.zeros_like(o); gone = 0
    for y, x in zip(*np.where(o)):
        if seen[y, x]: continue
        st, mem = [(y, x)], []; seen[y, x] = True
        while st:
            p = st.pop(); mem.append(p)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                q = (p[0] + dy, p[1] + dx)
                if 0 <= q[0] < 64 and 0 <= q[1] < 64 and o[q] and not seen[q]: seen[q] = True; st.append(q)
        if len(mem) <= maxn and not any(is_mark(a[None, None, q[0], q[1]])[0, 0] for q in mem):
            for q in mem: a[q] = 0
            gone += len(mem)
    if gone: save(a, n, k)
    return gone

def trim(n, k, cap=0.149, keep=None):
    a = load_any(n, k); o = op(a); acc = acc_mask(a)
    if keep: x0, y0, x1, y1 = keep; acc[y0:y1, x0:x1] = False
    need = int(acc_mask(a).sum() - cap * o.sum()) + 1
    if need <= 0: return 0
    ys, xs = np.where(acc); cy, cx = ys.mean(), xs.mean()
    for y, x in sorted(zip(ys, xs), key=lambda p: -((p[0] - cy) ** 2 + (p[1] - cx) ** 2))[:need]: grey_at(a, y, x)
    save(a, n, k); return need

if __name__ == "__main__":
    for n, lo in GROUND.items():
        a = load_any(n, "front"); print(n, "front ground cells", ug(a, lo, minL=110)); save(a, n, "front")
    print("quota halo", halo("quota", "front"), "omen halo", halo("omen", "front"))
    valence(); grasp(); abandon(); semaphore()
    #  the hue trap, fronts first (the backs are mirrored from them)
    for n in ("whim", "caprice", "starved", "quota", "goldset"):
        box = (0, 0, 64, 64) if n != "starved" else (0, 0, 64, 32)   # STARVED's eyes are re-hued, not greyed
        print(n, "greens greyed", trap(n, "front", "grey", box))
    print("starved eyes blue", trap("starved", "front", "hue", (0, 32, 64, 64), to=215))
    print("valence ears rose", trap("valence", "front", "hue", (0, 10, 64, 30), to=335, s_min=0.15))
    print("valence eyes ink", trap("valence", "front", "dark", (18, 26, 38, 34)))
    print("torpor eyes grey", trap("torpor", "front", "grey", (0, 0, 64, 32), s_min=0.15))
    print("rankle blush red", trap("rankle", "front", "hue", to=0, s_min=0.12))
    print("goldset petals gold", gold("goldset", (16, 6, 46, 30), (23, 13, 39, 25)))
    #  QUOTA: its drawn orange (a stray petal, the collar) gives way to the petal ring; the eyes keep theirs
    a = load_any("quota", "front"); m = 0
    for y, x in zip(*np.where(acc_mask(a))):
        if not (25 <= x < 41 and 27 <= y < 34): grey_at(a, y, x); m += 1
    save(a, "quota", "front"); print("quota other accents greyed", m)
    print("quota petals gold", gold("quota", (12, 2, 54, 40), (24, 18, 41, 37)))
    for n in NAMES:
        g = specks(n, "front")
        if g: print(n, "stray cells off", g)
    for n, box in FACE.items():
        if n == "omen": omen_back()
        else: hb.mirrored_features(n, box)
    for n in NAMES:
        for k in ("front", "back"):
            g = trim(n, k, keep=(10, 0, 56, 40) if n in ("quota", "goldset") and k == "front" else None)
            if g: print(n, k, "accent cells greyed for the cap", g)
            left = trap(n, k, "grey", s_min=0.25, acc_only=True)
            if left: print(n, k, "still in the type's hue reach, greyed:", left)
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", len(os.listdir(H)))

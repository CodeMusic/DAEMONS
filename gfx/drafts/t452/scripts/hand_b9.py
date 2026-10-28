"""T-452 batch 9 by hand: phase 1's default rules, then the user's answers (2026-10-28, multiple choice). hand4.py's,
hand_b5.py's and hand_b8.py's helpers.

    hand_b9.py      writes T/l/hand/<name>_{front,back}.png from l/clean (rm -r l/hand first: it starts from clean)

GROUNDS     baked ground bars/shadows off POLL's, STANDBY's, TRUST's, BUILDUP's, ALARM's and ENTRAPMENT's fronts and
            LOOKOUT's, RESIDUAL's and ALARM's backs (hand4.ug); PRESCIENCE's brown perch painted off (the user).
RELEASE     a lamp on its tail tip, joined to the tail, in DARKER AMBER (the user): pale yellow sat within 48 of the streak
            marker's yellow and the near-marker fix greyed it; amber is 140 degrees from SIGNAL's teal, so it stays an
            accent. Its yellow head the same amber, as far as the 15% cap allows (from the crown down), the rest greyed into the ramp.
MULTICAST   a second pair of wings: each drawn wing flipped upward behind the head (its entry: four places at once).
BUILDUP     the wool off below the collar (bare grey skin), a ball on its tail tip (the user).
ENTRAPMENT  t2i 5701 (the user's swap): a web drawn behind it, eight spokes and two rings in pale grey.
HUE TRAP    CONTENT's hue is 40 degrees and gbasprite.shift_off turns accents within 40 of it blue: ALARM's and LOOKOUT's
            ears rose (335), POLL's and SUPERVISOR's eyes and beaks (and feet) chartreuse (85); LOOKOUT's brown legs and
            tail tip greyed (the user).
BACKS       the front MIRRORED with the face's features painted out (hand_b5.mirrored_features; batch 7's default rule):
            POLL, SUPERVISOR, PILOT, SOUNDING, STANDBY, TRUST, HOPE, VIGILANCE, PRESCIENCE, BUILDUP, RELEASE, ENTRAPMENT,
            MULTICAST (so the back has four wings too).
            STATIC (now the plain mouse, today's shape) keeps today's back.
CAP         accents trimmed under 15% (hand_b8.trim_accents), RELEASE's lamp protected."""
import os, sys, colorsys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hand4 as h4
import hand_b5 as hb
T = os.environ["T452_ROOT"]; F = T + "/l"; H = F + "/hand"; os.makedirs(H, exist_ok=True)
hb.F, hb.H = F, H; h4.F, h4.H = F, H
from hand4 import load_any, save, ug, sanitize, stamp, outline, op, lum, is_mark, INK

GROUND = {("poll", "front"): 0.88, ("standby", "front"): 0.85, ("trust", "front"): 0.88, ("buildup", "front"): 0.85,
          ("alarm", "front"): 0.88, ("lookout", "back"): 0.88, ("residual", "back"): 0.88, ("alarm", "back"): 0.85,
          ("entrapment", "front"): 0.80}
FACE = {"poll": (10, 18, 48, 36), "supervisor": (21, 14, 43, 30), "pilot": (18, 26, 46, 37), "sounding": (24, 22, 42, 38),
        "standby": (18, 30, 46, 38), "trust": (20, 22, 46, 36), "hope": (13, 20, 30, 30), "vigilance": (14, 22, 48, 38),
        "prescience": (18, 10, 34, 20), "buildup": (18, 18, 36, 30), "release": (28, 22, 52, 36), "entrapment": (18, 24, 44, 37),
        "multicast": (20, 26, 42, 38)}   # its four wings on the back too
AMBER = ((120, 66, 10, 255), (176, 104, 22, 255), (214, 146, 46, 255))   # dark, mid, light: hue ~32-36, far from the marker yellow
def grey_at(a, y, x):
    l = int(lum(a[y:y + 1, x:x + 1])[0, 0]); a[y, x, :3] = (l, l, min(255, l + 4))
def hsv(a, y, x): return colorsys.rgb_to_hsv(*(a[y, x, :3] / 255))
def acc_mask(a): return op(a) & ~is_mark(a) & ((a[..., :3].max(-1) - a[..., :3].min(-1)) >= 60)

LAMP = ["  #####  ", " #MMMMM# ", "#MLLLLLM#", "#MLLLLLM#", "#MLLLLLM#", "#MLLLLLM#", "#MDLLLDM#", " #DDDDD# ", "  #####  "]
def release():
    a = load_any("release", "front")
    #  the yellow head -> amber by value, centre first, as far as the cap leaves room (the lamp's 49 cells counted first)
    o = op(a); yel = []
    for y, x in zip(*np.where(o & ~is_mark(a))):
        h, s, v = hsv(a, y, x)
        if 0.10 <= h <= 0.20 and s > 0.35: yel.append((y, x))
    other = acc_mask(a).sum() - len(yel); room = int(0.145 * o.sum()) - other - 49
    cy, cx = np.mean([p[0] for p in yel]), np.mean([p[1] for p in yel])
    yel.sort(key=lambda p: (p[0], abs(p[1] - cx)))   # from the crown down: an amber cap, not a patch over the face
    L = lum(a)
    for i, (y, x) in enumerate(yel):
        if i < room: a[y, x] = AMBER[0] if L[y, x] < 120 else (AMBER[1] if L[y, x] < 190 else AMBER[2])
        else: grey_at(a, y, x)
    print("release head amber", min(room, len(yel)), "of", len(yel), "(rest greyed)")
    #  the lamp: its lower rim sits on the tail's top (the curl's top at x 9-15, rows 30-31), so it reads as the tail's tip
    stamp(a, 7, 23, LAMP, {"#": INK, "D": AMBER[0], "M": AMBER[1], "L": AMBER[2]})
    save(a, "release", "front")

def multicast():
    a = load_any("multicast", "front"); src = a.copy(); k = 0
    for (x0, y0, x1, y1), (tx, ty) in (((8, 28, 23, 48), (1, 6)), ((42, 28, 58, 48), (49, 6))):
        w = src[y0:y1, x0:x1][::-1]
        for y in range(w.shape[0]):
            for x in range(w.shape[1]):
                p, q = ty + y, tx + x
                if w[y, x, 3] > 127 and not is_mark(w[y:y + 1, x:x + 1])[0, 0] and 0 <= p < 64 and 0 <= q < 64 and a[p, q, 3] <= 127:
                    a[p, q] = w[y, x]; k += 1
    print("multicast second wings", k); save(a, "multicast", "front")

BALL = [" ##### ", "#LLLLL#", "#LWWLL#", "#LWLLL#", "#LLLLM#", "#LLMMM#", " ##### "]
def buildup():
    a = load_any("buildup", "front"); L = lum(a); k = 0
    for y in range(33, 50):
        for x in range(8, 45):
            if a[y, x, 3] > 127 and not is_mark(a[y:y + 1, x:x + 1])[0, 0] and L[y, x] >= 175:
                v = int(L[y, x] * 0.62); a[y, x, :3] = (v, v + 4, v + 10); k += 1
    stamp(a, 52, 27, BALL, {"#": INK, "L": (226, 230, 236, 255), "W": (252, 252, 255, 255), "M": (170, 176, 186, 255)})
    print("buildup wool off", k); save(a, "buildup", "front")

def prescience():
    a = load_any("prescience", "front"); k = 0
    for y in range(52, 64):
        for x in range(64):
            if a[y, x, 3] <= 127: continue
            h, s, v = hsv(a, y, x); brown = (h < 0.12 or h > 0.95) and s > 0.2
            feet = 21 <= x <= 33 and y <= 55
            if (brown or lum(a[y:y + 1, x:x + 1])[0, 0] < 60) and not feet: a[y, x] = (0, 0, 0, 0); k += 1
    #  stray outline cells left hanging under the feet
    o = op(a)
    for y in range(52, 64):
        for x in range(64):
            if o[y, x] and sum(o[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= y + dy < 64 and 0 <= x + dx < 64) <= 1:
                a[y, x] = (0, 0, 0, 0); k += 1
    print("prescience perch cells", k); save(a, "prescience", "front")

WEB = (214, 216, 222, 255)
def web(a, cx=32, cy=30, rings=(16, 25)):
    k = 0
    def put(y, x):
        nonlocal k
        if 0 <= y < 64 and 0 <= x < 64 and a[y, x, 3] <= 127: a[y, x] = WEB; k += 1
    for t in range(8):
        ang = t * np.pi / 4 + np.pi / 8
        for r in range(4, 31): put(int(round(cy + r * np.sin(ang))), int(round(cx + r * np.cos(ang))))
    for R_ in rings:
        for t in range(0, 360, 2):
            put(int(round(cy + R_ * np.sin(np.radians(t)))), int(round(cx + R_ * np.cos(np.radians(t)))))
    return k

def rehue(n, k, to, hi=0.23, low_hi=0.93, rows=(0, 64)):
    a = load_any(n, k); m = 0
    for y, x in zip(*np.where(op(a))):
        if not (rows[0] <= y < rows[1]) or is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
        h, s, v = hsv(a, y, x)
        if s > 0.25 and v > 0.25 and (h <= hi or h >= low_hi):
            a[y, x, :3] = [int(c * 255) for c in colorsys.hsv_to_rgb(to / 360, max(s, 0.45), v)]; m += 1
    save(a, n, k); return m

def grey_warm(n, k, rows):
    a = load_any(n, k); m = 0
    for y, x in zip(*np.where(op(a))):
        if not (rows[0] <= y < rows[1]) or is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
        h, s, v = hsv(a, y, x)
        if s > 0.2 and (h <= 0.14 or h >= 0.93): grey_at(a, y, x); m += 1
    save(a, n, k); return m

def trim(n, k, cap=0.149, keep=None):
    a = load_any(n, k); o = op(a); acc = acc_mask(a)
    if keep: x0, y0, x1, y1 = keep; acc[y0:y1, x0:x1] = False
    need = int(acc_mask(a).sum() - cap * o.sum()) + 1
    if need <= 0: return
    ys, xs = np.where(acc); cy, cx = ys.mean(), xs.mean()
    for y, x in sorted(zip(ys, xs), key=lambda p: -((p[0] - cy) ** 2 + (p[1] - cx) ** 2))[:need]: grey_at(a, y, x)
    save(a, n, k); print(n, k, "accent cells greyed", need)

if __name__ == "__main__":
    for (n, k), lo in GROUND.items():
        a = load_any(n, k); print(n, k, "ground cells", ug(a, lo, minL=110)); save(a, n, k)
    release(); multicast(); buildup(); prescience()
    #  the hue trap, fronts (before the backs are mirrored from them)
    print("alarm ears rose", rehue("alarm", "front", 335, rows=(0, 24)))
    print("lookout ears rose", rehue("lookout", "front", 335, rows=(0, 16)))
    print("lookout legs/tail greyed", grey_warm("lookout", "front", (16, 64)))
    print("poll eyes/beak/feet chartreuse", rehue("poll", "front", 85, low_hi=2))
    print("supervisor eyes/beak/feet chartreuse", rehue("supervisor", "front", 85, low_hi=2))
    for n, box in FACE.items():
        hb.mirrored_features(n, box)
    #  backs not mirrored: ALARM's (today's) and LOOKOUT's (turned) ears; LOOKOUT's legs
    print("alarm back ears rose", rehue("alarm", "back", 335, rows=(0, 24)))
    print("lookout back ears rose", rehue("lookout", "back", 335, rows=(0, 16)), "warm greyed", grey_warm("lookout", "back", (16, 64)))
    for k in ("front", "back"):
        a = load_any("entrapment", k); print("entrapment", k, "web cells", web(a)); save(a, "entrapment", k)
    for n in sorted({f[:-4].rsplit("_", 1)[0] for f in os.listdir(H)} | {"pilot", "huddle", "static", "sounding"}):
        for k in ("front", "back"):
            trim(n, k, keep=(5, 20, 18, 34) if n == "release" and k == "front" else ((46, 20, 60, 34) if n == "release" else None))
    for f in sorted(os.listdir(H)):
        n, k = f[:-4].rsplit("_", 1); a = load_any(n, k); s = sanitize(a)
        if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", sorted(os.listdir(H)))

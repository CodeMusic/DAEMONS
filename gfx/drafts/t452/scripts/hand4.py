"""T-452 batch 4, by hand (the user via the coordinator, 2026-10-27: build batch 4 on the recommended answers): the keys
no draft kept, the grounds, the backs. hand3.py's helpers, unchanged.

    hand4.py      writes T/g/hand/<name>_{front,back,icon}.png (from g/clean and g/reduced)

LEMMA MIND  four arms: every draft drew two. Each upper forearm-and-fist is copied 12 rows down and 2 out, BEHIND
            the body (only into empty cells), front and back -- a second pair of arms below the first.
EDGECASE    the stilt legs: the draft had them (thin dark red), the clean wore them away. Two legs drawn from the body
            to the ground line, a knee each, three-toed feet, front; the back is the front mirrored, eye painted out.
BACKS       LATENCY, HOTPATH, HEAP, EDGECASE: the turned drafts kept a face or did not match the front, so each back is
            its front MIRRORED (a back faces right) with the face painted out in the body's own grey.
QUORUM      its turned back kept eyes on the lower pods: small dark interior blobs (the eyes) filled from their ring.
GROUNDS     baked grounds off the CLEAN grids by hand3's flood (ug), listed in grounds() with their arguments.
SANITIZE    hand3's: a drawn colour within reach of a streak marker darkened (small patch) or greyed (large)."""

import os, json, shutil
import numpy as np
from PIL import Image
R = "/Users/christopherhicks/Projects/DAEMONS"; F = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452") + "/g"; H = F + "/hand"
os.makedirs(H, exist_ok=True)
INK = (16, 16, 20, 255)
MARK = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0)]
NAMES = ["proof", "theorem", "lemma mind", "snare", "honeypot", "tarpit", "driftnet", "dragnet", "heap", "stack", "monolith", "hotpath", "overdrive", "latency", "shell", "sentinel", "quorum", "edgecase", "dualcore", "triplecore"]

def load(n, k): return np.array(Image.open(f"{F}/clean/{n}_{k}.png").convert("RGBA")).astype(int)
def save(a, n, k): Image.fromarray(a.astype(np.uint8), "RGBA").save(f"{H}/{n}_{k}.png")
def lum(a): return (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000
def op(a): return a[..., 3] > 127
def is_mark(a): return np.any([np.all(a[..., :3] == m, -1) for m in MARK], 0)

def sanitize(a):
    near = np.zeros(a.shape[:2], bool)
    for m in MARK: near |= (np.abs(a[..., :3] - m).max(-1) <= 48)
    bad = near & ~is_mark(a) & op(a)
    #  a small patch (an eye) is an accent: the same hue, darker, out of the marker's reach; a big one (SKEW's petals)
    #  is body the model drew in a marker's colour: grey at its own value, so the type's ramp takes it
    L = lum(a); seen = np.zeros_like(bad)
    for y, x in zip(*np.where(bad)):
        if seen[y, x]: continue
        st, mem = [(y, x)], []; seen[y, x] = True
        while st:
            p = st.pop(); mem.append(p)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (p[0] + dy, p[1] + dx)
                if 0 <= q[0] < 64 and 0 <= q[1] < 64 and bad[q] and not seen[q]: seen[q] = True; st.append(q)
        for p in mem:
            if len(mem) > 6: a[p][:3] = max(40, min(235, int(L[p])))
            else: a[p][:3] = (a[p][:3] * 0.7).astype(int)
    return int(bad.sum())

def ug(a, lo, minL=None, dark=False):
    """ground cells off: below LO of the figure, flood from transparency through pale (or, DARK, any non-outline) cells"""
    o = op(a); L = lum(a); ink = L < 60
    ys = np.where(o.any(1))[0]; y0, y1 = ys.min(), ys.max(); cut = y0 + int((y1 - y0) * lo)
    cand = o & (~ink if dark else (L >= minL)) & ~is_mark(a); cand[:cut] = False
    seen = np.zeros(o.shape, bool); st = []
    for y, x in zip(*np.where(cand)):
        if y == 63 or any(0 <= y + dy < 64 and 0 <= x + dx < 64 and not o[y + dy, x + dx] for dy, dx in ((1, 0), (0, 1), (0, -1))):
            seen[y, x] = True; st.append((y, x))
    while st:
        y, x = st.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, q = y + dy, x + dx
            if 0 <= p < 64 and 0 <= q < 64 and cand[p, q] and not seen[p, q]: seen[p, q] = True; st.append((p, q))
    sole = seen & np.roll(o & ~seen & ~ink, 1, 0)
    a[seen] = 0; a[sole] = INK
    return int(seen.sum())

def outline(a, rows=None):
    """an outline cell on every opaque, non-outline cell that touches transparency (in ROWS, if given)"""
    o = op(a); L = lum(a); add = []
    for y, x in zip(*np.where(o & (L >= 60))):
        if rows and not (rows[0] <= y < rows[1]): continue
        if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not o[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            add.append((y, x))
    for y, x in add: a[y, x] = INK

def stamp(a, x0, y0, rows, K, behind=False, onto=False):
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch == " ": continue
            y, x = y0 + dy, x0 + dx
            if not (0 <= y < 64 and 0 <= x < 64): continue
            if behind and a[y, x, 3] > 127: continue
            if onto and a[y, x, 3] <= 127: continue
            a[y, x] = (0, 0, 0, 0) if ch == "." else K[ch]

def paint_out(a, box, fill, keep_ink_edge=True):
    """the face off: every INTERIOR cell of BOX (all eight neighbours opaque) that is not a streak marker -> FILL"""
    x0, y0, x1, y1 = box; o = op(a); mk = is_mark(a); n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not o[y, x] or mk[y, x]: continue
            if all(o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                a[y, x] = fill; n += 1
    return n

def body_grey(a, box):
    x0, y0, x1, y1 = box; c = a[y0:y1, x0:x1].reshape(-1, 4)
    c = c[(c[:, 3] > 127) & (lum(c[None])[0] >= 100) & (lum(c[None])[0] <= 200)]
    v = np.median(c[:, :3], 0).astype(int) if len(c) else np.array([150, 150, 156])
    return (int(v[0]), int(v[1]), int(v[2]), 255)

def mirrored(n, face, chest=None):
    a = load(n, "front")
    fill = body_grey(a, face)
    print(n, "face cells", paint_out(a, face, fill))
    if chest:
        x0, y0, x1, y1 = chest; L = lum(a); mk = is_mark(a)
        for y in range(y0, y1):
            for x in range(x0, x1):
                if a[y, x, 3] > 127 and L[y, x] > 200 and not mk[y, x]: a[y, x] = fill
    save(a[:, ::-1].copy(), n, "back")


def load_any(n, k):
    p = f"{H}/{n}_{k}.png"
    return np.array(Image.open(p if os.path.exists(p) else f"{F}/clean/{n}_{k}.png").convert("RGBA")).astype(int)

def arms_below(a, boxes, dy=12):
    """a second pair of arms: each box (x0, y0, x1, y1, dx) copied DY rows down and DX across, behind the body"""
    src = a.copy()
    for x0, y0, x1, y1, dx in boxes:
        for y in range(y0, y1):
            for x in range(x0, x1):
                if src[y, x, 3] <= 127: continue
                p, q = y + dy, x + dx
                if 0 <= p < 64 and 0 <= q < 64 and a[p, q, 3] <= 127 and not is_mark(src[y:y + 1, x:x + 1])[0, 0]:
                    a[p, q] = src[y, x]
    #  where the copied arm meets the body it has no outline of its own: close it
    outline(a, (y0 + dy, 64))

def lemma():
    a = load("lemma mind", "front"); arms_below(a, ((2, 28, 20, 43, -1), (44, 28, 62, 43, 1))); save(a, "lemma mind", "front")
    b = load("lemma mind", "back"); arms_below(b, ((6, 26, 21, 44, -1), (43, 26, 58, 44, 1))); save(b, "lemma mind", "back")

LEG = (110, 36, 48, 255)
def edgecase():
    a = load("edgecase", "front")
    K = {"#": INK, "L": LEG}
    for x in (29, 35):                                   # two thin legs, a knee each, from the belly to the ground
        for y in range(36, 61):
            kx = x + (1 if 46 <= y < 50 else 0)
            if a[y, kx, 3] > 127 and y < 40: continue
            a[y, kx] = LEG; a[y, kx - 1] = INK; a[y, kx + 1] = INK
        stamp(a, x - 3, 60, ["#######", "#LLLLL#", "###.###"], K)   # three-toed foot
    save(a, "edgecase", "front")
    m = a.copy(); paint_out(m, (24, 6, 32, 13), body_grey(m, (26, 12, 34, 30))); save(m[:, ::-1].copy(), "edgecase", "back")

def deface(a, box, maxsize=14):
    """eyes off: small dark blobs inside BOX that never touch transparency, filled with their ring's median colour"""
    x0, y0, x1, y1 = box; o = op(a); L = lum(a); dark = o & (L < 70); seen = np.zeros_like(dark); n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not dark[y, x] or seen[y, x]: continue
            st, mem, edge = [(y, x)], [], False; seen[y, x] = True
            while st:
                p = st.pop(); mem.append(p)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (p[0] + dy, p[1] + dx)
                    if not (0 <= q[0] < 64 and 0 <= q[1] < 64) or not o[q]: edge = True; continue
                    if dark[q] and not seen[q]: seen[q] = True; st.append(q)
            if edge or len(mem) > maxsize: continue
            ring = [a[p[0] + dy, p[1] + dx] for p in mem for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                    if o[p[0] + dy, p[1] + dx] and not dark[p[0] + dy, p[1] + dx] and not is_mark(a[None, None, p[0] + dy, p[1] + dx])[0, 0]]
            if not ring: continue
            fill = np.median(np.array(ring), 0).astype(int)
            for p in mem: a[p] = fill
            n += len(mem)
    return n

QEYES = ((9, 29, 16, 37), (19, 29, 26, 36), (37, 29, 45, 36), (47, 29, 55, 37), (24, 42, 31, 49), (33, 42, 40, 49))
def eyes_off(a, boxes):
    """QUORUM's back: the eye spots the turn kept, by box -- every dark or highlight cell in it that does not touch
    transparency goes to the median mid-tone of the box grown by two"""
    o = op(a); L = lum(a); n = 0
    for x0, y0, x1, y1 in boxes:
        reg = a[max(0, y0 - 2):y1 + 2, max(0, x0 - 2):x1 + 2].reshape(-1, 4); rl = lum(reg[None])[0]
        mid = reg[(reg[:, 3] > 127) & (rl >= 110) & (rl <= 215)]
        fill = np.median(mid, 0).astype(int) if len(mid) else np.array([150, 150, 156, 255])
        for y in range(y0, y1):
            for x in range(x0, x1):
                if not o[y, x] or is_mark(a[None, None, y, x])[0, 0]: continue
                if any(not o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): continue
                if L[y, x] < 90 or L[y, x] > 235: a[y, x] = fill; n += 1
    return n

GROUNDS = (("proof", "front", 0.85, dict(minL=110)), ("proof", "back", 0.90, dict(minL=110)),
           ("theorem", "back", 0.88, dict(minL=110)), ("honeypot", "front", 0.88, dict(dark=True)),
           ("honeypot", "back", 0.90, dict(dark=True)), ("shell", "front", 0.85, dict(minL=110)),
           ("shell", "back", 0.85, dict(minL=110)), ("sentinel", "front", 0.90, dict(dark=True)),
           ("triplecore", "front", 0.92, dict(dark=True)), ("triplecore", "back", 0.90, dict(minL=110)))

def grounds():
    for n, k, lo, kw in GROUNDS:
        a = load_any(n, k); print(n, k, "ground", ug(a, lo, **kw)); save(a, n, k)

if __name__ == "__main__":
    import sys
    os.makedirs(H, exist_ok=True)
    for f in os.listdir(H): os.remove(f"{H}/{f}")
    grounds(); lemma(); edgecase()
    mirrored("latency", (39, 23, 56, 35))
    mirrored("hotpath", (14, 17, 24, 29))
    mirrored("heap", (26, 12, 48, 33))
    q = load("quorum", "back"); print("quorum back eye cells", eyes_off(q, QEYES)); save(q, "quorum", "back")
    t = load_any("theorem", "front"); print("theorem front ground", ug(t, 0.90, minL=110)); save(t, "theorem", "front")
    for n in NAMES:
        for k in ("front", "back"):
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", sorted(os.listdir(H)))

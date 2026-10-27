"""T-452 batch 3, by hand (the user, 2026-10-27, approving batch 3): the keys no draft drew, the grounds, the backs.

    hand3.py      writes gfx/drafts/t452/f/hand/<name>_{front,back,icon}.png (from f/clean and f/reduced)

GROUNDS   ten baked grounds came off the REDUCED sprites for the sheets (unground3.py, f/unground.json); gbasprite
          builds from the CLEAN grids, so they come off those too, by the same flood (ug() below): from the
          transparency through ground cells below LO of the figure's height, stopped by the outline.
SANITIZE  a drawn colour within gbasprite's STREAK_TOLERANCE of a streak marker that is not the marker itself (SKEW's
          cyan petals) would be read as a fifth streak; a small patch (an eye) is darkened to 70%,
          the same hue out of the marker's reach; a big one (SKEW's petals) goes to grey at its own value.
RESIDENT  two antennae ending in round rings (the loops), on front, back and icon.
SPYWARE   one dark eye spot on each wing, front and back.
SPINLOCK  a spiral on the pale belly, front and icon (it is what tells it from MUTEX's frog); the back is today's
          repainted (i2i 5131), its two dangling stick legs cut to stubs.
TAPPOINT  a dark hole under it, rim outlined, drawn behind the body (only where the frame is empty), front and back.
WIRETAP   front zoomed to 52 cells (src/wiretap_front_zoom.png, cleaned by reduce2), its dark base off; back is
          today's back (gfx/daemons/wiretap_back.png) with the dirt mound taken off and the soles outlined.
BACKS     SKEW, HANDLER and LOOP: the turned drafts did not match their fronts, so each back is its front MIRRORED
          (a back faces right) with the face painted out in the body's own grey (and HANDLER's pale chest).
Every edit is in the clean drafts' own colours (gbasprite.place_rich turns value into the type's ramp); icons in the
indices icon3 chose (picks.json's icon3 ramp) and 15 for the outline, frame 2 redrawn from frame 1 one row lower."""
import os, json, shutil
import numpy as np
from PIL import Image
R = "/Users/christopherhicks/Projects/DAEMONS"; F = R + "/gfx/drafts/t452/f"; H = F + "/hand"
os.makedirs(H, exist_ok=True)
INK = (16, 16, 20, 255)
MARK = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0)]
NAMES = ("skew badseed payload rootkit resident spyware tappoint wiretap cookie tracker fault handler preempt livelock "
         "sentry guardian loop spinlock mutex hunch inference conjecture").split()

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

RING = ["  ###  ",
        " #MMM# ",
        "#M###M#",
        "#M#.#M#",
        "#M###M#",
        " #MMM# ",
        "  ###  "]
SPOT = [" ### ", "#DDD#", "#DLD#", "#DDD#", " ### "]
SPIRAL = ["  #####  ",
          " #     # ",
          "#  ###  #",
          "# #   # #",
          "# # # # #",
          "# #  #  #",
          "#  ##  # ",
          " #    #  ",
          "  ####   "]

def icon_edit(n, cells):
    src = f"{H}/{n}_icon.png" if os.path.exists(f"{H}/{n}_icon.png") else f"{F}/reduced/{n}_icon.png"
    im = Image.open(src); g = np.array(im)
    for (x, y), (v, behind) in cells.items():
        if behind and g[y, x] != 0: continue
        g[y, x] = v
    g[32:] = 0; g[33:64] = g[0:31]
    out = Image.fromarray(g.astype(np.uint8), "P"); out.putpalette(im.getpalette()); out.save(f"{H}/{n}_icon.png")

def ramp(n): return json.load(open(F + "/picks.json"))[n]["measured"]["icon3"]["ramp"]

def resident():
    for k, top in (("front", 20), ("back", 20)):
        a = load(k and "resident", k)
        if k == "front":
            a[48:] = 0; outline(a, (44, 48))
        M = body_grey(a, (26, 22, 40, 34)); K = {"#": INK, "M": M}
        for i in range(5):                         # the stalks, out and up from the head
            stamp(a, 28 - i, top - 1 - i, ["#M"], K, behind=True)
            stamp(a, 38 + i, top - 1 - i, ["M#"], K, behind=True)
        stamp(a, 19, top - 12, RING, K); stamp(a, 41, top - 12, RING, K)
        save(a, "resident", k)
    dk, md, lt = ramp("resident"); c = {}
    for (x, y) in ((10, 7), (9, 6), (8, 5), (21, 7), (22, 6), (23, 5)): c[(x, y)] = (15, True)
    for x0 in (5, 22):
        for dy, row in enumerate(["###", "#.#", "###"]):
            for dx, ch in enumerate(row): c[(x0 + dx, 2 + dy)] = (15 if ch == "#" else 0, False)
    icon_edit("resident", c)

def spyware():
    for k, spots in (("front", ((6, 9), (49, 11))), ("back", ((8, 28), (52, 30)))):
        a = load("spyware", k)
        print("spyware", k, "ground", ug(a, 0.75, minL=110))
        K = {"#": INK, "D": (64, 64, 72, 255), "L": (232, 232, 236, 255)}
        for x0, y0 in spots: stamp(a, x0, y0, SPOT, K, onto=True)
        save(a, "spyware", k)

def spinlock():
    a = load("spinlock", "front"); stamp(a, 25, 33, SPIRAL, {"#": INK}, onto=True); save(a, "spinlock", "front")
    b = load("spinlock", "back"); b[50:] = 0; outline(b, (46, 50)); save(b, "spinlock", "back")
    c = {}
    for dy, row in enumerate([" ### ", "#   #", "# # #", "#  ##", " #   "]):
        for dx, ch in enumerate(row):
            if ch == "#": c[(13 + dx, 17 + dy)] = (15, False)
    icon_edit("spinlock", c)

def hole(a, cx, cy, rx, ry):
    for y in range(cy - ry - 1, cy + ry + 2):
        for x in range(cx - rx - 1, cx + rx + 2):
            if not (0 <= y < 64 and 0 <= x < 64) or a[y, x, 3] > 127: continue
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1.0:
                inner = ((x - cx) / (rx - 1.5)) ** 2 + ((y - cy) / (ry - 1.0)) ** 2
                a[y, x] = (40, 40, 46, 255) if inner <= 1.0 else INK

def tappoint():
    a = load("tappoint", "front"); hole(a, 31, 59, 28, 4); save(a, "tappoint", "front")
    b = load("tappoint", "back"); hole(b, 31, 56, 27, 4); save(b, "tappoint", "back")

def wiretap():
    a = load("wiretap", "front"); print("wiretap front base", ug(a, 0.85, dark=True)); save(a, "wiretap", "front")
    b = np.array(Image.open(R + "/gfx/daemons/wiretap_back.png").convert("RGBA")).astype(int)
    shutil.copyfile(R + "/gfx/daemons/wiretap_back.png", F + "/src/wiretap_back_today.png")
    r, g, bl = b[..., 0], b[..., 1], b[..., 2]
    dirt = op(b) & (r - bl > 28) & (r >= g) & ~is_mark(b)
    dirt[:38] = False
    b[dirt] = 0
    b[47:] = 0
    #  the dirt was under and between the two moles: what remains below row 40 that hangs off nothing goes too
    outline(b, (36, 47))
    save(b, "wiretap", "back")

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

def grounds():
    #  the clean grids' own grounds (the reduced ones are in f/unground.json); a hand file already written is edited
    for n, k, lo, kw in (("livelock", "front", 0.80, dict(minL=110)), ("livelock", "back", 0.90, dict(minL=110)),
                         ("badseed", "front", 0.80, dict(minL=110)), ("mutex", "front", 0.80, dict(minL=110)),
                         ("mutex", "back", 0.90, dict(dark=True)), ("conjecture", "back", 0.93, dict(minL=110)),
                         ("sentry", "back", 0.92, dict(dark=True))):
        a = load(n, k); print(n, k, "ground", ug(a, lo, **kw))
        if (n, k) == ("mutex", "back"): a[55:] = 0; outline(a, (51, 55))     # the strip's stray cells under the feet
        save(a, n, k)

if __name__ == "__main__":
    grounds(); resident(); spyware(); spinlock(); tappoint(); wiretap()
    mirrored("skew", (22, 28, 48, 44))
    mirrored("handler", (16, 3, 27, 13), chest=(22, 20, 36, 42))
    mirrored("loop", (26, 9, 47, 29))
    #  sanitize every file that goes in (hand or clean), into hand/ only where it changes something
    for n in NAMES:
        for k in ("front", "back"):
            p = f"{H}/{n}_{k}.png"; a = np.array(Image.open(p if os.path.exists(p) else f"{F}/clean/{n}_{k}.png").convert("RGBA")).astype(int)
            s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", sorted(os.listdir(H)))

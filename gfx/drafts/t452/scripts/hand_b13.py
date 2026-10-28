"""T-452 batch 13 by hand, PHASE 1 on the RECOMMENDED answers (the user away; the coordinator, 2026-10-28: apply the
recommended fix for every issue, as batches 10-12 did). hand_b12.py's helpers, copied, with batch 13's edits below.

    hand_b13.py      writes T/q/hand/<name>_{front,back}.png from q/clean (starts from clean every run)

LOST KEYS, drawn by hand: REFLECTION's black mirror at its mouth, LODESTAR's star between its antlers, LYUBOV's flower
garland, MULTIMAL's chest light, ILLUMINED's halo ring, BASTET's collar, COINFLIP's two-tone coin, MONTECARLO's dice
string, LASVEGAS's die, RUNOFF's drops, SMUDGE's smear, ECLIPSE's black disc and bright ring, DETOUR's zigzag,
UNBRANCHED's back stripe and bundle.
NEXUS      the eight have no streaks (species.json): reduce2's markers taken off their fronts.
TYPE-HUE TRAP: COINFLIP's, MONTECARLO's and LASVEGAS's orange beaks and feet crimson (FIRE 38); MULTIMAL's cyan fins
teal (WATER 220); anything else in reach greyed and reported.
BACKS       the front mirrored, face out, for all 21.
CAP         accents trimmed under 15%; near-marker colours fixed (hand4.sanitize)."""
import os, sys, json, shutil
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("T452_ROOT", "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b13_work")
import hand4 as h4
import hand_b5 as hb
import hand_b10lib as hx   # hand_b10's helpers, without its writes
T = os.environ["T452_ROOT"]; F = T + "/q"; H = F + "/hand"
if os.path.isdir(H): shutil.rmtree(H)
os.makedirs(H)
hb.F, hb.H = F, H; h4.F, h4.H = F, H; hx.F, hx.H = F, H
from hand4 import load_any, save, ug, sanitize, stamp, op, lum, is_mark, INK
P = json.load(open(F + "/picks.json")); hx.P = P
NAMES = ['reflection', 'lodestar', 'perihelion', 'lyubov', 'multimal', 'illumined', 'lynx', 'bastet', 'stump', 'boosting', 'canopy', 'coinflip', 'montecarlo', 'lasvegas', 'runoff', 'alluvium', 'delta', 'smudge', 'eclipse', 'detour', 'unbranched']
GREYS = hx.GREYS

def ring(n, cx, cy, r, col=(84, 86, 92, 255)):
    """a ring of cells at radius R round (CX, CY), markers left alone"""
    a = load_any(n, "front"); m = 0
    for y in range(64):
        for x in range(64):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if r - 0.6 <= d <= r + 0.6 and op(a)[y, x] and not is_mark(a[y:y + 1, x:x + 1])[0, 0]: a[y, x] = col; m += 1
    save(a, n, "front"); return m

SUCKER = [" ##### ", "#MLLLM#", "#L###L#", "#L#D#L#", "#L###L#", "#MLLLM#", " ##### "]
def attachment():
    a = load_any("attachment", "front")
    stamp(a, 11, 34, SUCKER, {"#": INK, "L": (206, 210, 216, 255), "M": (150, 154, 162, 255), "D": (60, 40, 50, 255)})
    save(a, "attachment", "front")

def poly_fill(a, pts, fill, behind=True):
    """a polygon of cells (ray-cast), filled and outlined in ink, behind what is there"""
    from matplotlib.path import Path
    p = Path(pts); o = op(a).copy(); mk = np.zeros((64, 64), bool)
    for y in range(64):
        for x in range(64):
            if p.contains_point((x + 0.5, y + 0.5)): mk[y, x] = True
    edge = mk & ~(np.roll(mk, 1, 0) & np.roll(mk, -1, 0) & np.roll(mk, 1, 1) & np.roll(mk, -1, 1))
    for y, x in zip(*np.where(mk)):
        if behind and o[y, x]: continue
        a[y, x] = INK if edge[y, x] else fill
    return int(mk.sum())

def glidepath():
    """a membrane each side, wrist (about y 40) to foot (y 50), scalloped trailing edge, a finger line through it"""
    a = load_any("glidepath", "front"); M = (150, 154, 162, 255)
    L = [(23, 37), (9, 39), (5, 45), (9, 46), (12, 49), (17, 49), (20, 52), (24, 51)]
    R = [(62 - x, y) for x, y in L]   # the body's centre is about x 31
    n = poly_fill(a, L, M) + poly_fill(a, R, M)
    for x, y in ((9, 41), (12, 42), (15, 43), (18, 44)): a[y, x] = (110, 114, 122, 255)
    for x, y in ((54, 41), (51, 42), (48, 43), (45, 44)): a[y, x] = (110, 114, 122, 255)
    save(a, "glidepath", "front"); return n

def impulse():
    """the eyes under the fringe: each eye box's cells to hair strands (light / mid grey, alternate columns), ink kept
    only where the fringe meets the cheek (the box's bottom row)"""
    a = load_any("impulse", "front"); m = 0
    for x0, y0, x1, y1 in ((35, 26, 43, 33), (49, 26, 55, 32)):
        for y in range(y0, y1):
            for x in range(x0, x1):
                if not op(a)[y, x] or is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
                if y == y1 - 1: a[y, x] = (70, 72, 80, 255) if x % 2 else (150, 154, 160, 255)
                else: a[y, x] = (214, 218, 222, 255) if (x + (y // 3)) % 3 else (150, 154, 160, 255)
                m += 1
    save(a, "impulse", "front"); return m

def grey_box(n, k, box, hues=None):
    """accent cells in BOX (optionally only hues in the HUES range, degrees) greyed into the ramp"""
    import colorsys
    a = load_any(n, k); x0, y0, x1, y1 = box; m = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not op(a)[y, x] or is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
            c = a[y, x, :3]
            if c.max() - c.min() < 40: continue
            h = colorsys.rgb_to_hsv(*(c / 255))[0] * 360
            if hues and not (hues[0] <= h <= hues[1]): continue
            hx.grey_at(a, y, x); m += 1
    save(a, n, k); return m

def features_off2(a, box, dark=False, flat=False):
    """hand_b5.features_off, and then the saturated cells it skips at the box's outline edge (an eye against the
    silhouette, HARDLINE's and CUNNING's) to the same fill; DARK: the fill is the box's own mid-dark grey (a dark
    dog's face painted out light read as a pale patch -- CRYWOLF, as OMEN's in batch 10)"""
    x0, y0, x1, y1 = box; o = op(a); L = lum(a); mk = is_mark(a); sat = a[..., :3].max(-1) - a[..., :3].min(-1)
    reg = a[y0:y1, x0:x1].reshape(-1, 4); rl = lum(reg[None])[0]; rs = reg[:, :3].max(-1) - reg[:, :3].min(-1)
    pool = reg[(reg[:, 3] > 127) & ((rl >= 60) & (rl < 140) if dark else (rl >= 150)) & (rs < 40)]
    fill = np.median(pool, 0).astype(int) if len(pool) else np.array([200, 200, 206, 255]); fill[3] = 255; n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not o[y, x] or mk[y, x]: continue
            edge = any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1))
            if edge and sat[y, x] < 60: continue
            if (L[y, x] < 90 and not edge) or sat[y, x] >= 60 or (flat and not edge):   # FLAT: every interior cell (a face drawn in light lines too)
                a[y, x] = fill; n += 1
    return n

def soft_face(a, box):
    """the back of a head where the face was drawn in strong lines (CRYWOLF, CUNNING): the box's interior cells to a
    blurred, banded version of their own values (sigma 3, steps of 22), so the head keeps its light and shade and
    loses its features; edge cells and markers kept"""
    from scipy.ndimage import gaussian_filter
    x0, y0, x1, y1 = box; o = op(a); mk = is_mark(a); L = lum(a).astype(float)
    Lw = np.where(o, L, np.nan); body = np.nanmedian(Lw[y0:y1, x0:x1])
    Lf = np.where(o, L, body); B = gaussian_filter(Lf, 3); n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not o[y, x] or mk[y, x]: continue
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): continue
            v = int(round(B[y, x] / 22) * 22); v = max(40, min(236, v)); a[y, x] = (v, v, min(255, v + 4), 255); n += 1
    return n

def low_ground(n, k, box, test):
    """a dark ground the pale flood (ug) cannot take: cells in BOX passing TEST(rgb, lum) off, then the cut edge
    outlined (COMFORT's shadow, OLDBRANCH's dark red puddle)"""
    a = load_any(n, k); x0, y0, x1, y1 = box; L = lum(a); m = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if op(a)[y, x] and not is_mark(a[y:y + 1, x:x + 1])[0, 0] and test(a[y, x, :3], L[y, x]): a[y, x] = 0; m += 1
    h4.outline(a, rows=(y0 - 4, y1)); save(a, n, k); return m

def today_back(n, lo):
    """today's back (the art's 64x64) on the clean grid's footing: the clean back is reduce2's from today's i2i draft;
    here the TODAY art itself, ground off"""
    R = "/Users/christopherhicks/Projects/DAEMONS"
    spec = json.load(open(R + "/companion/server/data/species.json")); v = {s["name"].lower(): s for s in spec.values()}[n]
    im = Image.open(R + "/" + v["art"]["back"]).convert("RGBA")
    if im.width != 64: im = im.resize((64, 64), Image.NEAREST)
    a = np.array(im).astype(int); a[a[..., 3] <= 127] = 0
    g = ug(a, lo, minL=110); save(a, n, "back"); return g

# ---------------------------------------------------------------- batch 13's edits
NEXUS = ["reflection", "lodestar", "perihelion", "lyubov", "multimal", "illumined", "lynx", "bastet"]

def unmark(n, k="front"):
    """streak markers off (THE NEXUS's eight carry none): each marker cell to the median of its non-marker neighbours"""
    a = load_any(n, k); mk = is_mark(a); o = op(a); m = 0
    for _ in range(4):
        for y, x in zip(*np.where(mk)):
            nb = [a[y + dy, x + dx] for dy in (-2, -1, 0, 1, 2) for dx in (-2, -1, 0, 1, 2)
                  if 0 <= y + dy < 64 and 0 <= x + dx < 64 and o[y + dy, x + dx] and not mk[y + dy, x + dx]]
            if nb: a[y, x] = np.median(np.array(nb), 0).astype(int); a[y, x, 3] = 255; mk[y, x] = False; m += 1
    save(a, n, k); return m

def stamp_on(n, x, y, rows, K, behind=False, onto=False):
    a = load_any(n, "front"); stamp(a, x, y, rows, K, behind=behind, onto=onto); save(a, n, "front")

def disc(n, cx, cy, r, fill, rim=None, behind=True):
    """a filled disc of cells (behind what is there), an outline, and optionally a RIM ring just outside it"""
    a = load_any(n, "front"); o = op(a).copy(); m = 0
    for y in range(64):
        for x in range(64):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if behind and o[y, x]: continue
            if d <= r - 1: a[y, x] = fill; m += 1
            elif d <= r: a[y, x] = INK
            elif rim and d <= r + 1.2: a[y, x] = rim
            elif rim and d <= r + 2.2: a[y, x] = INK
    save(a, n, "front"); return m

def ringline(n, cx, cy, r, col, behind=True):
    a = load_any(n, "front"); o = op(a).copy(); m = 0
    for y in range(64):
        for x in range(64):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if behind and o[y, x]: continue
            if r - 0.7 <= d <= r + 0.7: a[y, x] = col; m += 1
            elif r + 0.7 < d <= r + 1.7: a[y, x] = INK
    save(a, n, "front"); return m

def paint_line(n, pts, col, width=1, skip_dark=True):
    """cells along the polyline PTS (on opaque cells only; markers and, with SKIP_DARK, outline/eye cells kept)"""
    a = load_any(n, "front"); o = op(a); mk = is_mark(a); L = lum(a); m = 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        steps = max(abs(x1 - x0), abs(y1 - y0)) * 2 + 1
        for t in range(steps + 1):
            x = round(x0 + (x1 - x0) * t / steps); y = round(y0 + (y1 - y0) * t / steps)
            for w in range(width):
                yy = y + w
                if 0 <= yy < 64 and o[yy, x] and not mk[yy, x] and not (skip_dark and L[yy, x] < 60): a[yy, x] = col; m += 1
    save(a, n, "front"); return m

MIRROR = ["  #####  ", " #LKKKL# ", "#LKWKKKL#", "#LKKKKKL#", "#LKKKKKL#", " #LKKKL# ", "  #####  "]
MIRK = {"#": INK, "L": (200, 204, 212, 255), "K": (20, 20, 26, 255), "W": (250, 250, 252, 255)}   # a pale frame round black glass, one glint
STAR = ["  #  ", " #W# ", "#WWW#", " #W# ", "#W#W#"]
STARK = {"#": INK, "W": (250, 250, 240, 255)}
COIN = ["  ###  ", " #LLDD# ", "#LLLDDD#", "#LWLDDD#", "#LLLDDD#", " #LLDD# ", "  ####  "]
COINK = {"#": INK, "L": (226, 228, 232, 255), "W": (252, 252, 252, 255), "D": (70, 72, 80, 255)}
DIE = ["######", "#WWWW#", "#WKWW#", "#WWWW#", "#WWKW#", "######"]
DIEK = {"#": INK, "W": (244, 244, 246, 255), "K": (24, 24, 30, 255)}
DICE = ["#####", "#WWW#", "#WKW#", "#WWW#", "#####"]
DROP = [" # ", "#W#", "#W#", "#L#", " # "]
DROPK = {"#": (90, 96, 108, 255), "W": (248, 250, 252, 255), "L": (200, 206, 214, 255)}
GLOW = [" #W# ", "#WYW#", "WYYYW", "#WYW#", " #W# "]
GLOWK = {"#": (60, 60, 70, 255), "W": (255, 246, 214, 255), "Y": (255, 214, 120, 255)}   # a small warm light (amber, 40 off nothing: WATER is 220)
BUNDLE = [" ###### ", "#LLMLLL#", "#LLMLLL#", "#DDKDDD#", " ###### "]
BUNDK = {"#": INK, "L": (200, 204, 210, 255), "M": (90, 92, 100, 255), "D": (150, 154, 162, 255), "K": (60, 62, 70, 255)}

def garland(n="lyubov"):
    """small flowers along the neck: rose and white alternating dots with a dark leaf between"""
    a = load_any(n, "front"); o = op(a); m = 0
    pts = [(36, 30), (38, 31), (40, 32), (42, 32), (44, 32), (46, 31), (48, 30), (50, 29)]
    for i, (x, y) in enumerate(pts):
        if not o[y, x]: continue
        a[y, x] = (226, 96, 132, 255) if i % 2 == 0 else (250, 246, 240, 255); m += 1
        if o[y + 1, x]: a[y + 1, x] = (70, 96, 70, 255) if i % 2 else (160, 50, 80, 255)
    save(a, n, "front"); return m

def collar(n="bastet"):
    a = load_any(n, "front"); o = op(a); L = lum(a); m = 0
    for y in (23, 24):
        for x in range(14, 32):
            if o[y, x] and L[y, x] >= 60 and not is_mark(a[y:y + 1, x:x + 1])[0, 0]: a[y, x] = (52, 54, 62, 255); m += 1
    save(a, n, "front"); return m

GROUND = [("boosting", "front", 0.88, dict(minL=110)), ("canopy", "front", 0.88, dict(minL=100)), ("coinflip", "front", 0.85, dict(minL=110)),
          ("montecarlo", "front", 0.85, dict(minL=110)), ("detour", "front", 0.9, dict(minL=110)), ("unbranched", "front", 0.88, dict(minL=110)),
          ("stump", "front", 0.9, dict(minL=110))]
FACE = {"reflection": [(28, 8, 56, 26)], "lodestar": [(16, 14, 36, 25)], "perihelion": [(12, 14, 40, 34)], "lyubov": [(32, 10, 54, 29)],
        "multimal": [(28, 22, 48, 36)], "illumined": [(18, 18, 56, 38)], "lynx": [(12, 22, 52, 46)], "bastet": [(8, 6, 26, 22)],
        "stump": [(18, 22, 44, 37)], "boosting": [(21, 21, 29, 31), (33, 21, 41, 31)], "canopy": [(22, 25, 28, 31), (36, 25, 42, 31), (30, 16, 37, 23)], "coinflip": [(20, 22, 46, 34)],
        "montecarlo": [(28, 16, 46, 34)], "lasvegas": [(16, 14, 36, 28)], "runoff": [(18, 14, 48, 32)], "alluvium": [(16, 12, 50, 30)],
        "delta": [(14, 10, 40, 28)], "smudge": [(16, 12, 38, 30)], "eclipse": [(14, 8, 32, 24)], "detour": [(12, 10, 44, 30)],
        "unbranched": [(10, 14, 34, 30)]}
DARKFACE = {"smudge", "multimal", "canopy"}
SOFT = {"perihelion", "delta", "alluvium", "eclipse"}   # a blurred head: a flat fill read as a pale (or grey) plate

if __name__ == "__main__":
    for n in NEXUS: print(n, "streak markers off", unmark(n))
    for n, k, lo, kw in GROUND:
        a = load_any(n, k); print(n, k, "ground cells", ug(a, lo, **kw)); save(a, n, k)
    print("multimal cyan glow ground off", low_ground("multimal", "front", (0, 53, 64, 64), lambda c, l: int(c[2]) > int(c[0]) + 60 and l > 100))
    #  the hue trap, by hand where a colour is the point
    for n in ("coinflip", "montecarlo", "lasvegas"): print(n, "orange beak and feet crimson", hx.trap(n, "front", "hue", to=350, s_min=0.3))
    print("multimal fins teal", hx.trap("multimal", "front", "hue", to=165, s_min=0.3))
    #  lost keys
    stamp_on("reflection", 45, 23, MIRROR, MIRK)
    stamp_on("lodestar", 21, 1, STAR, STARK)
    print("lyubov garland cells", garland())
    stamp_on("multimal", 34, 36, GLOW, GLOWK)
    print("illumined halo cells", ringline("illumined", 37, 22, 22, (250, 250, 246, 255)))
    print("bastet collar cells", collar())
    stamp_on("coinflip", 51, 8, COIN, COINK)
    for x in (25, 30, 35): stamp_on("montecarlo", x, 34, DICE, DIEK)
    stamp_on("lasvegas", 44, 33, DIE, DIEK)
    for x, y in ((12, 6), (52, 6), (10, 18), (54, 18)): stamp_on("runoff", x, y, DROP, DROPK, behind=True)
    print("smudge smear cells", paint_line("smudge", [(16, 27), (37, 17)], (66, 68, 76, 255), width=3))
    print("eclipse disc cells", disc("eclipse", 22, 14, 11, (22, 22, 28, 255), rim=(246, 246, 240, 255)))
    print("detour zigzag cells", paint_line("detour", [(18, 34), (21, 37), (24, 34), (27, 37), (30, 34), (33, 37)], (40, 42, 50, 255), width=2))
    print("unbranched stripe cells", paint_line("unbranched", [(30, 33), (46, 33)], (52, 54, 62, 255), width=1, skip_dark=False))
    stamp_on("unbranched", 32, 30, BUNDLE, BUNDK)
    for n in NAMES:
        g = hx.specks(n, "front")
        if g: print(n, "stray cells off", g)
    for n, boxes in FACE.items():
        a = load_any(n, "front"); m = sum(soft_face(a, b) if n in SOFT else features_off2(a, b, dark=n in DARKFACE) for b in boxes)
        save(a[:, ::-1].copy(), n, "back"); print(n, "back mirrored, feature cells", m)
    for n in NAMES:
        for k in ("front", "back"):
            g = hx.trim(n, k)
            if g: print(n, k, "accent cells greyed for the cap", g)
            left = hx.trap(n, k, "grey", s_min=0.25, acc_only=True)
            if left: print(n, k, "still in the type's hue reach, greyed:", left)
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", len(os.listdir(H)))

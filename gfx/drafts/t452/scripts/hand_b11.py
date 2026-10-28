"""T-452 batch 11 by hand, PHASE 1 on the RECOMMENDED answers (the user away overnight; the coordinator, 2026-10-28:
apply the recommended fix for every issue, as batch 10 did). hand4.py's, hand_b5.py's and hand_b10.py's helpers.

    hand_b11.py      writes T/o/hand/<name>_{front,back}.png from o/clean (starts from clean every run)

LOST KEYS, drawn by hand:
  CRAVING     a ring on its belly (Ursaring's; no draft drew it) -- in dark grey, not gold: gold (~45) sits within 40
              degrees of CONTENT/NORMAL's 40, so gbasprite would turn it blue.
  ATTACHMENT  a round sucker mouth (its HITCHHIKER key; the draft drew a small smile).
  GLIDEPATH   a glider's membrane from each wrist to its feet (no draft of ten spread one; the big ears were all
              the wing it had).
  IMPULSE     its eyes hidden under its fringe (its entry: "It cannot see past its own hair").
TYPE-HUE TRAP (gbasprite.shift_off rotates an accent within 40 degrees of the type's hue):
  CRYWOLF (NORMAL 40)  the salmon slab under its jaw greyed into the body (it would have turned blue).
  SIMMER (FIRE 38)     the green sprout and the teal speckles greyed into the fire ramp (the body is orange in the
                        ramp; teal flecks read as mould).
  Anything else still in reach is greyed and reported (hand_b10.trap, accents only).
GROUNDS     baked ground bars and shadows off the fronts (hand4.ug); today's backs too where they are kept.
BACKS       the front MIRRORED with the face's features painted out (hand_b5.features_off) where today's back does not
            match the new front; TODAY'S back kept where it does (a shell, a dome, a rear view of the same body).
CAP         accents trimmed under 15%; near-marker colours fixed (hand4.sanitize)."""
import os, sys, json, shutil
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("T452_ROOT", "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b11_work")
import hand4 as h4
import hand_b5 as hb
import hand_b10lib as hx   # hand_b10's helpers, without its writes
T = os.environ["T452_ROOT"]; F = T + "/o"; H = F + "/hand"
if os.path.isdir(H): shutil.rmtree(H)
os.makedirs(H)
hb.F, hb.H = F, H; h4.F, h4.H = F, H; hx.F, hx.H = F, H
from hand4 import load_any, save, ug, sanitize, stamp, op, lum, is_mark, INK
P = json.load(open(F + "/picks.json")); hx.P = P
NAMES = ["duplex", "startle", "withdrawal", "blindspot", "glidepath", "hardline", "warning", "crywolf", "bristle", "hoarding",
         "drive", "cunning", "comfort", "craving", "simmer", "callous", "instinct", "impulse", "oldbranch", "attachment", "clinging"]
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

#  grounds: (name, kind, lo, kwargs)
GROUND = [("startle", "front", 0.85, dict(minL=100)), ("hoarding", "front", 0.85, dict(minL=110)),
          ("simmer", "front", 0.88, dict(minL=110)), ("oldbranch", "front", 0.85, dict(dark=True)),
          ("comfort", "front", 0.85, dict(dark=True))]
#  backs kept from today's (they match the new front): their grounds off as well
TODAY = {"withdrawal": 0.85, "startle": 0.85, "hoarding": 0.85, "callous": 0.85, "impulse": 0.85, 
         "attachment": 0.9, "clinging": 0.85}
FACE = {"duplex": [(8, 8, 19, 19), (45, 8, 56, 19)], "bristle": [(6, 22, 44, 40)], "blindspot": [(43, 34, 54, 44)], "hardline": [(26, 24, 58, 38)],
        "warning": [(18, 18, 46, 40)], "crywolf": [(20, 12, 56, 40)], "cunning": [(14, 16, 42, 36)],
        "craving": [(20, 16, 44, 28)], "simmer": [(24, 20, 52, 40)], "instinct": [(6, 26, 32, 42)],
        "drive": [(8, 34, 26, 46)], "comfort": [(18, 16, 46, 40)], "glidepath": [(18, 26, 40, 36)],
        "oldbranch": [(20, 26, 46, 42)]}

def today_back(n, lo):
    """today's back (the art's 64x64) on the clean grid's footing: the clean back is reduce2's from today's i2i draft;
    here the TODAY art itself, ground off"""
    R = "/Users/christopherhicks/Projects/DAEMONS"
    spec = json.load(open(R + "/companion/server/data/species.json")); v = {s["name"].lower(): s for s in spec.values()}[n]
    im = Image.open(R + "/" + v["art"]["back"]).convert("RGBA")
    if im.width != 64: im = im.resize((64, 64), Image.NEAREST)
    a = np.array(im).astype(int); a[a[..., 3] <= 127] = 0
    g = ug(a, lo, minL=110); save(a, n, "back"); return g

if __name__ == "__main__":
    for n, k, lo, kw in GROUND:
        a = load_any(n, k); print(n, k, "ground cells", ug(a, lo, **kw)); save(a, n, k)
    print("craving ring", ring("craving", 32.5, 34.5, 4.2))
    attachment(); print("glidepath membrane cells", glidepath()); print("impulse eye cells under the fringe", impulse())
    print("crywolf salmon slab greyed", grey_box("crywolf", "front", (12, 38, 40, 54)))
    print("simmer sprout and teal greyed", grey_box("simmer", "front", (0, 0, 64, 64), hues=(80, 200)))
    print("comfort shadow off", low_ground("comfort", "front", (0, 52, 24, 60), lambda c, l: l < 110))
    print("oldbranch puddle off", low_ground("oldbranch", "front", (0, 52, 64, 64), lambda c, l: int(c[0]) > int(c[1]) + 20 or l < 40))
    for n in NAMES:
        g = hx.specks(n, "front")
        if g: print(n, "stray cells off", g)
    for n, boxes in FACE.items():
        a = load_any(n, "front"); m = sum(soft_face(a, b) if n in ("crywolf", "cunning") else features_off2(a, b) for b in boxes)
        save(a[:, ::-1].copy(), n, "back"); print(n, "back mirrored, feature cells", m)
    for n, lo in TODAY.items(): print(n, "today's back, ground cells", today_back(n, lo))
    for n in NAMES:
        for k in ("front", "back"):
            g = hx.trim(n, k)
            if g: print(n, k, "accent cells greyed for the cap", g)
            left = hx.trap(n, k, "grey", s_min=0.25, acc_only=True)
            if left: print(n, k, "still in the type's hue reach, greyed:", left)
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", len(os.listdir(H)))

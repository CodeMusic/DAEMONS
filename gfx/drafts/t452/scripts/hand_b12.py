"""T-452 batch 12 by hand, PHASE 1 on the RECOMMENDED answers (the user away; the coordinator, 2026-10-28: apply the
recommended fix for every issue, as batches 10 and 11 did). hand_b11.py's helpers, copied (importing it would wipe its
own hand/), with batch 12's edits below.

    hand_b12.py      writes T/p/hand/<name>_{front,back}.png from p/clean (starts from clean every run)

LOST KEYS, drawn by hand: RECALL's pebble at its trunk tip, RUMINATE's rock at its mouth, BROODING's eyes narrowed to
slits, GRIEVANCE's diamond hole in its chest plate, ILLUSION's two spiral orbs in its antlers, BRONTES's storm cloud on
its back, KAIROS's wing-blur arcs. Left as drawn (asked in questions.md): ARMOURING's blades, BOREAS's ribbon tails.
TYPE-HUE TRAP (gbasprite rotates an accent within 40 degrees of the type's hue): REPAY's cyan gift rose (ICE 197);
PHOENIX's flames crimson (FIRE 38); BOREAS's gem and eyes teal (WATER 220); FIXATION's blue eye amber (DARK 240);
ARMOURING's orange beak and legs crimson (STEEL 44); RECALL's salmon ear linings rose (GROUND 33); anything else in
reach greyed and reported.
BACKS       the front mirrored, face out, for all but BROODING (today's sealed shell, which matches; its halo off).
CAP         accents trimmed under 15%; near-marker colours fixed (hand4.sanitize)."""
import os, sys, json, shutil
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("T452_ROOT", "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b12_work")
import hand4 as h4
import hand_b5 as hb
import hand_b10lib as hx   # hand_b10's helpers, without its writes
T = os.environ["T452_ROOT"]; F = T + "/p"; H = F + "/hand"
if os.path.isdir(H): shutil.rmtree(H)
os.makedirs(H)
hb.F, hb.H = F, H; h4.F, h4.H = F, H; hx.F, hx.H = F, H
from hand4 import load_any, save, ug, sanitize, stamp, op, lum, is_mark, INK
P = json.load(open(F + "/picks.json")); hx.P = P
NAMES = ['repay', 'buoyancy', 'armouring', 'fixation', 'obsession', 'recall', 'engram', 'illusion', 'imitation', 'cache', 'brontes', 'typhon', 'boreas', 'ruminate', 'brooding', 'grievance', 'triton', 'phoenix', 'kairos']
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

# ---------------------------------------------------------------- batch 12's edits
G = GREYS
ROCK = [" ###### ", "#LMMDDD#", "#MDDDDK#", "#DDDDKK#", " ###### "]
ROCKK = dict(GREYS, K=(70, 72, 80, 255))
PEBBLE = [" #### ", "#WWLL#", "#LLLM#", " #### "]   # pale stone against its dark legs
ORB = [" ### ", "#TWT#", "#WTD#", "#TDT#", " ### "]   # a spiral read at 5px: light core turning into dark
TEAL = {"#": INK, "T": (70, 170, 152, 255), "W": (196, 250, 238, 255), "D": (40, 110, 100, 255)}
CLOUD = ["   ####     ", "  #CCCC# ## ", " #CCLLCC#CC#", "#CCLLCCCCCC#", "#CCCCCCCCCD#", " #DDCDDCDD# ", "  ## ## ##  "]
CLOUDK = {"#": INK, "C": (92, 96, 108, 255), "L": (140, 146, 158, 255), "D": (64, 66, 76, 255)}
DIAMOND = ["   #   ", "  #D#  ", " #DKD# ", "#DKKKD#", " #DKD# ", "  #D#  ", "   #   "]
DIAK = {"#": INK, "D": (58, 60, 68, 255), "K": (24, 24, 30, 255)}

def stamp_on(n, x, y, rows, K, behind=False):
    a = load_any(n, "front"); stamp(a, x, y, rows, K, behind=behind); save(a, n, "front")

def slits():
    """BROODING: each round eye painted out to the shell, then a narrow dark slit, angled down to the middle"""
    a = load_any("brooding", "front"); m = 0
    for b in ((14, 24, 26, 36), (33, 24, 45, 36)): m += features_off2(a, b, flat=True)
    for x in range(16, 25): a[30 + (x >= 21), x] = INK
    for x in range(34, 43): a[30 + (x <= 37), x] = INK
    for x in range(20, 25): a[29 + (x >= 23), x] = INK   # a heavier inner end: a frown, not a sleeping eye
    for x in range(34, 39): a[29 + (x <= 35), x] = INK
    save(a, "brooding", "front"); return m

def blur():
    """KAIROS: pale arcs above and behind its raised wings, a hummingbird's blur"""
    a = load_any("kairos", "front"); c = (214, 220, 230, 255)
    for x, y in ((38, 14), (40, 13), (42, 12), (44, 12), (46, 12), (48, 13), (40, 10), (42, 9), (44, 9), (46, 10)):
        if not op(a)[y, x]: a[y, x] = c
    save(a, "kairos", "front")

GROUND = [("repay", "front", 0.85, dict(dark=True)), ("typhon", "front", 0.88, dict(minL=100)), ("ruminate", "front", 0.88, dict(dark=True)),
          ("phoenix", "front", 0.9, dict(minL=110))]
FACE = {"repay": [(22, 18, 42, 30)], "buoyancy": [(6, 22, 26, 38)], "armouring": [(6, 8, 22, 20)], "fixation": [(20, 16, 42, 32)],
        "obsession": [(24, 10, 46, 30)], "recall": [(16, 14, 34, 28)], "engram": [(16, 20, 38, 27)], "illusion": [(14, 18, 34, 30)],
        "imitation": [(10, 22, 30, 34)], "cache": [(10, 16, 26, 35)], "brontes": [(6, 12, 22, 26)], "typhon": [(11, 16, 26, 30)],
        "boreas": [(22, 24, 44, 36)], "ruminate": [(12, 22, 42, 42)], "grievance": [(16, 14, 40, 26)], "triton": [(16, 30, 32, 42)],
        "phoenix": [(18, 24, 36, 36)], "kairos": [(16, 17, 26, 24)]}
TODAY = {"brooding": 0.95}

if __name__ == "__main__":
    for n, k, lo, kw in GROUND:
        a = load_any(n, k); print(n, k, "ground cells", ug(a, lo, **kw)); save(a, n, k)
    print("triton ground bar off", low_ground("triton", "front", (0, 54, 64, 64), lambda c, l: 40 <= l < 140 and int(c[2]) > int(c[0]) + 8))
    #  the hue trap, by hand where a colour is the point
    print("repay gift rose", hx.trap("repay", "front", "hue", (14, 30, 40, 46), to=340, s_min=0.2))
    print("phoenix flames crimson", hx.trap("phoenix", "front", "hue", to=350, s_min=0.25))
    print("boreas eyes and gem teal", hx.trap("boreas", "front", "hue", (26, 26, 38, 34), to=165, s_min=0.3), hx.trap("boreas", "front", "hue", (32, 37, 43, 48), to=165, s_min=0.3))
    print("fixation eye amber", hx.trap("fixation", "front", "hue", (20, 16, 34, 30), to=35, s_min=0.2))
    print("armouring beak and legs crimson", hx.trap("armouring", "front", "hue", to=352, s_min=0.3))
    print("typhon crown gem greyed", grey_box("typhon", "front", (22, 2, 36, 16), hues=(170, 280)))
    print("illusion antlers greyed", grey_box("illusion", "front", (0, 0, 64, 22), hues=(280, 360)))
    #  lost keys
    stamp_on("recall", 28, 41, PEBBLE, G); stamp_on("ruminate", 27, 35, ROCK, ROCKK)
    stamp_on("grievance", 29, 36, DIAMOND, DIAK)
    stamp_on("illusion", 6, 9, ORB, TEAL); stamp_on("illusion", 44, 9, ORB, TEAL)
    stamp_on("brontes", 30, 7, CLOUD, CLOUDK)
    print("brooding eye cells to slits", slits())
    for n in NAMES:
        g = hx.specks(n, "front")
        if g: print(n, "stray cells off", g)
    blur()   # after the specks pass, which would take the arcs
    for n, boxes in FACE.items():
        a = load_any(n, "front"); m = sum(soft_face(a, b) if n == "obsession" else features_off2(a, b, flat=n in ("engram", "ruminate")) for b in boxes)
        save(a[:, ::-1].copy(), n, "back"); print(n, "back mirrored, feature cells", m)
    for n, lo in TODAY.items():
        print(n, "today's back, ground cells", today_back(n, lo), "halo", hx.halo(n, "back"))
    for n in NAMES:
        for k in ("front", "back"):
            g = hx.trim(n, k)
            if g: print(n, k, "accent cells greyed for the cap", g)
            left = hx.trap(n, k, "grey", s_min=0.25, acc_only=True)
            if left: print(n, k, "still in the type's hue reach, greyed:", left)
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", len(os.listdir(H)))

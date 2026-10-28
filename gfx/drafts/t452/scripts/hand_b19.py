"""T-452 batch 19 by hand, PHASE 1 on the RECOMMENDED answers (apply the recommended fix for every issue, as batches
10-17 did). hand_b17.py's helpers, copied, with batch 19's edits in the main block.

    hand_b19.py      writes T/x/hand/<name>_{front,back}.png from x/clean (starts from clean every run)

LOST KEYS, drawn by hand: FEDERATED's four cores (its one big core split, the three recoloured), DEUCALION's stone
cracks, KHIONE's snowflakes, TALOS's chest bolt, GAIA's mountain and tree, POLYDEUCES's star, CASTOR's dark neck,
OVERTONE's rings of sound; OURANOS's cloud. SINGLETON's and PAIRWISE's one-eyed orbs are composed in orbs19.py.
BACKS       the front mirrored, face out, for all 13.
CAP         accents trimmed under 15%; anything left in the type's hue reach greyed; near-marker colours fixed."""
import os, sys, json, shutil
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("T452_ROOT", "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b19_work")
import hand4 as h4
import hand_b5 as hb
import hand_b10lib as hx   # hand_b10's helpers, without its writes
T = os.environ["T452_ROOT"]; F = T + "/x"; H = F + "/hand"
if os.path.isdir(H): shutil.rmtree(H)
os.makedirs(H)
hb.F, hb.H = F, H; h4.F, h4.H = F, H; hx.F, hx.H = F, H
from hand4 import load_any, save, ug, sanitize, stamp, op, lum, is_mark, INK
P = json.load(open(F + "/picks.json")); hx.P = P
NAMES = ['singleton', 'pairwise', 'federated', 'deucalion', 'khione', 'talos', 'pontus', 'gaia', 'ouranos', 'polydeuces', 'castor', 'elpis', 'overtone']
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


def stamp_safe(n, x, y, rows, K, behind=False, onto=False):
    """stamp, leaving streak-marker cells as they are"""
    a = load_any(n, "front"); mk = is_mark(a).copy(); keep = a[mk].copy()
    stamp(a, x, y, rows, K, behind=behind, onto=onto); a[mk] = keep; save(a, n, "front")

def shift_marks(n, dx, dy):
    """the streak markers moved by (DX, DY): each copied to its new cell, the old cells filled from their neighbours"""
    a = load_any(n, "front"); mk = is_mark(a); cells = [(y, x, a[y, x].copy()) for y, x in zip(*np.where(mk))]
    save(a, n, "front"); unmark(n); a = load_any(n, "front"); m = 0
    for y, x, c in cells:
        if 0 <= y + dy < 64 and 0 <= x + dx < 64 and op(a)[y + dy, x + dx]: a[y + dy, x + dx] = c; m += 1
    save(a, n, "front"); return m

# ---------------------------------------------------------------- batch 16's edits
LG = {"#": INK, "L": (184, 188, 196, 255), "D": (120, 124, 132, 255)}
JAW_UP = ["##       ", "#L#      ", "#LL#     ", " #LL###  ", "  #LLLL##", "   ######"]   # a sickle jaw, tip up and out
JAW_DN = JAW_UP[::-1]
SPARK = ["  #  ", " #Y# ", "#YWY#", " #Y# ", "  #  "]
SPARKK = {"#": INK, "Y": (250, 214, 64, 255), "W": (255, 252, 230, 255)}
LOCK = ["  #####  ", " #LLLLL# ", " #L# #L# ", " #L# #L# ", "#########", "#GGGGGGG#", "#GGG#GGG#", "#GGG#GGG#", "#GGGGGGG#", "#########"]
LOCKK = {"#": INK, "L": (190, 194, 202, 255), "G": (226, 176, 48, 255)}   # gold (43): ICE is 197
ICICLE = ["#WW#", "#WL#", " #L#", " #L#", "  # "]
ICEK = {"#": (70, 80, 92, 255), "W": (246, 250, 252, 255), "L": (200, 214, 222, 255)}
DROP = ["  #  ", " #W# ", " #W# ", "#WCC#", "#CCC#", "#CCC#", " ### "]
BLUEK = {"#": INK, "W": (236, 246, 255, 255), "C": (90, 150, 230, 255)}   # blue (215): GRASS is 124
PEARL = [" ### ", "#WWL#", "#WLL#", "#LLM#", " ### "]
PEARLK = {"#": (70, 70, 80, 255), "W": (252, 250, 252, 255), "L": (222, 216, 228, 255), "M": (180, 174, 190, 255)}
BPEARL = [" #### ", "#KKKW#", "#KKKK#", "#KKKK#", " #### "]
BPEARLK = {"#": INK, "K": (40, 40, 48, 255), "W": (236, 236, 244, 255)}
PLUS = ["  ###  ", "  #W#  ", "###W###", "#WWWWW#", "###W###", "  #W#  ", "  ###  "]
MINUS = ["#######", "#WWWWW#", "#######"]
SIGNK = {"#": INK, "W": (252, 252, 252, 255)}

def bolt(n, pts):
    """a lightning arc behind the figure: a white core along PTS, pale yellow below it, an ink edge round both"""
    a = load_any(n, "front"); o = op(a).copy(); new = np.zeros((64, 64), bool)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        st = max(abs(x1 - x0), abs(y1 - y0))
        for t in range(st + 1):
            x = round(x0 + (x1 - x0) * t / st); y = round(y0 + (y1 - y0) * t / st)
            for yy, c in ((y, (255, 255, 250, 255)), (y + 1, (250, 226, 110, 255))):
                if 0 <= yy < 64 and not o[yy, x] and not new[yy, x]: a[yy, x] = c; new[yy, x] = True
    for y, x in zip(*np.where(new)):
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, q = y + dy, x + dx
            if 0 <= p < 64 and 0 <= q < 64 and not o[p, q] and not new[p, q] and a[p, q, 3] <= 127: a[p, q] = INK
    save(a, n, "front"); return int(new.sum())

def funnel(n, bands, col=(214, 214, 206, 255), dark=(130, 128, 120, 255)):
    """a dust whirlwind: the front half of a flattened ellipse per band (CY, CX, RX), pale over a darker line, behind"""
    a = load_any(n, "front"); o = op(a).copy(); m = 0
    for cy, cx, rx in bands:
        for x in range(cx - rx, cx + rx + 1):
            t = (x - cx) / rx; y = cy + round(1.6 * (1 - t * t) ** 0.5)
            for yy, c in ((y, col), (y + 1, dark)):
                if 0 <= yy < 64 and 0 <= x < 64 and not o[yy, x]: a[yy, x] = c; m += 1
    save(a, n, "front"); return m

def pixels(n, cells):
    """square pixels (2x2) breaking away: CELLS are (x, y, rgb)"""
    a = load_any(n, "front"); m = 0
    for x, y, c in cells:
        for dy in (0, 1):
            for dx in (0, 1):
                if 0 <= y + dy < 64 and 0 <= x + dx < 64 and a[y + dy, x + dx, 3] <= 127: a[y + dy, x + dx] = c + (255,); m += 1
    save(a, n, "front"); return m

def ear_tint(n, cx, cy, r, rgb):
    """the cells of an ear disc (not outline, not markers) to RGB by their own value"""
    import colorsys
    a = load_any(n, "front"); L = lum(a); mk = is_mark(a); m = 0
    h, s, _ = colorsys.rgb_to_hsv(*[c / 255 for c in rgb])
    for y in range(64):
        for x in range(64):
            if ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 <= r and op(a)[y, x] and not mk[y, x] and L[y, x] >= 60:
                v = min(1, 0.35 + L[y, x] / 255 * 0.6)
                a[y, x, :3] = [int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)]; m += 1
    save(a, n, "front"); return m

def keep_main(n, keep=None):
    """only the figure: every 8-connected piece but the largest off, except pieces reaching into KEEP (x0, y0, x1, y1)"""
    from scipy.ndimage import label
    a = load_any(n, "front"); lab, k = label(op(a), np.ones((3, 3))); sizes = [(lab == i).sum() for i in range(1, k + 1)]
    big = 1 + int(np.argmax(sizes)); m = 0
    for i in range(1, k + 1):
        if i == big: continue
        ys, xs = np.where(lab == i)
        if keep and ((xs >= keep[0]) & (xs < keep[2]) & (ys >= keep[1]) & (ys < keep[3])).any(): continue
        a[lab == i] = 0; m += len(ys)
    save(a, n, "front"); return m

# ---------------------------------------------------------------- batch 17's edits
def ribbon(n, pts, core=(232, 232, 226, 255), shade=(170, 170, 164, 255)):
    """a loose wrap trailing behind the figure: a pale core along PTS, a shade cell beside it, an ink edge round both"""
    a = load_any(n, "front"); o = op(a).copy(); new = np.zeros((64, 64), bool)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        st = max(abs(x1 - x0), abs(y1 - y0))
        for t in range(st + 1):
            x = round(x0 + (x1 - x0) * t / st); y = round(y0 + (y1 - y0) * t / st)
            for xx, c in ((x, core), (x + 1, shade)):
                if 0 <= xx < 64 and 0 <= y < 64 and not o[y, xx] and not new[y, xx]: a[y, xx] = c; new[y, xx] = True
    for y, x in zip(*np.where(new)):
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, q = y + dy, x + dx
            if 0 <= p < 64 and 0 <= q < 64 and not o[p, q] and not new[p, q] and a[p, q, 3] <= 127: a[p, q] = INK
    save(a, n, "front"); return int(new.sum())

def fade(n, y0, y1):
    """the hem fades: from row Y0 the cells pale toward white, and from halfway down every other cell is gone (a
    checker that thins row by row); markers kept; the last rows (to Y1) mostly gone"""
    a = load_any(n, "front"); mk = is_mark(a); o = op(a); m = 0
    for y in range(y0, 64):
        t = min(1.0, (y - y0) / max(1, y1 - y0))
        for x in range(64):
            if not o[y, x] or mk[y, x]: continue
            if t > 0.4 and ((x + y) % 2 == 0 or (t > 0.8 and (x + 2 * y) % 3)): a[y, x] = 0; m += 1; continue
            l = int(lum(a[y:y + 1, x:x + 1])[0, 0]); v = int(l + (236 - l) * (0.3 + 0.5 * t)); a[y, x, :3] = (v, v, min(255, v + 4))
    save(a, n, "front"); return m

def cut_below(n, y, outline_from=None):
    a = load_any(n, "front"); a[y:] = 0; h4.outline(a, rows=(y - 3, y)); save(a, n, "front")

HONEY = [" #R# ", "#RRW#", "#RRR#", " ### "]
HONEYK = {"#": INK, "R": (214, 56, 84, 255), "W": (255, 220, 228, 255)}   # rose-red (348): STEEL is 44, honey's amber sits in its trap
POISON = ["  #  ", " #K# ", "#KKW#", "#KKK#", " ### "]
POISONK = {"#": INK, "K": (96, 40, 132, 255), "W": (210, 180, 236, 255)}   # dark violet (276): GRASS is 124
BIGPEARL = ["  ###  ", " #WWL# ", "#WWWLL#", "#WWLLM#", "#LLLMM#", " #LMM# ", "  ###  "]
WISP = ["  ## ", " #WW#", "#W# #", "#W#  ", " #   "]
WISPK = {"#": (120, 120, 128, 255), "W": (240, 240, 244, 255)}
CLOUD = (244, 244, 248, 255)
FRUIT = (206, 52, 64, 255)

# ---------------------------------------------------------------- batch 19's edits
def hue_to(n, box, hues, rgb, k="front"):
    """accent cells in BOX whose hue is within HUES (degrees) to RGB's hue and saturation, keeping their own value"""
    import colorsys
    a = load_any(n, k); mk = is_mark(a); x0, y0, x1, y1 = box; m = 0
    h, s, _ = colorsys.rgb_to_hsv(*[c / 255 for c in rgb])
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not op(a)[y, x] or mk[y, x]: continue
            c = a[y, x, :3]
            if c.max() - c.min() < 40: continue
            hh, _, v = colorsys.rgb_to_hsv(*(c / 255))
            if hues[0] <= hh * 360 <= hues[1]:
                a[y, x, :3] = [int(q * 255) for q in colorsys.hsv_to_rgb(h, s, max(0.3, v))]; m += 1
    save(a, n, k); return m

def darken(n, box, lo=50, gain=0.32):
    """the light, unsaturated cells in BOX (not ink, not markers) to a dark grey by their own value: a black neck"""
    a = load_any(n, "front"); mk = is_mark(a); L = lum(a); x0, y0, x1, y1 = box; m = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = a[y, x, :3]
            if not op(a)[y, x] or mk[y, x] or L[y, x] < 70 or c.max() - c.min() >= 40: continue
            v = int(lo + L[y, x] * gain); a[y, x, :3] = (v, v, v + 4); m += 1
    save(a, n, "front"); return m

def arc(n, cx, cy, r, a0, a1, col):
    """cells on a circle arc (degrees A0 to A1, 0 = right, 90 = down), only where the cell is empty"""
    import math
    a = load_any(n, "front"); m = 0
    for t in np.linspace(math.radians(a0), math.radians(a1), 60):
        x = round(cx + r * math.cos(t)); y = round(cy + r * math.sin(t))
        if 0 <= x < 64 and 0 <= y < 64 and a[y, x, 3] <= 127: a[y, x] = col; m += 1
    save(a, n, "front"); return m

CRIMSON = (200, 40, 70)    # 348: STEEL is 44 -- the orange irises sat in its trap
TEAL = (70, 196, 180)      # 172: the cores, out of STEEL's reach (their draft yellow sat in it)
CRACK = (54, 56, 64, 255)
BOLT = ["  ###  ", " #LLL# ", "#LLDLL#", "#LDDDL#", "#LLDLL#", " #LLL# ", "  ###  "]
BOLTK = {"#": INK, "L": (206, 210, 216, 255), "D": (96, 98, 106, 255)}
FLAKE = ["#W#", "WWW", "#W#"]
FLAKEK = {"#": (150, 160, 172, 255), "W": (252, 252, 255, 255)}
STARG = ["  #  ", " #Y# ", "#YYY#", " #Y# ", "  #  "]
STARGK = {"#": INK, "Y": (250, 214, 90, 255)}   # gold (45): DRAGON is 168; CASTOR's drawn star is gold too -- the twins' one star
TREE = [" G ", "GGG", " T "]
TREEK = {"G": (70, 140, 70, 255), "T": (90, 70, 50, 255)}
ROCK = (138, 136, 132, 255)
SOUND = (78, 80, 92, 255)

GROUND = [("federated", 0.85, 110), ("gaia", 0.85, 110), ("overtone", 0.85, 110)]
FACE = {"singleton": (16, 14, 46, 38), "pairwise": (8, 16, 52, 38), "deucalion": (14, 14, 46, 34), "khione": (16, 28, 44, 40),
        "talos": (14, 12, 44, 30), "pontus": (8, 18, 30, 34), "gaia": (46, 22, 62, 38), "ouranos": (8, 26, 30, 40),
        "polydeuces": (10, 3, 26, 14), "castor": (18, 2, 30, 14), "elpis": (16, 18, 40, 34), "overtone": (14, 6, 34, 22)}
DARKFACE = {"castor"}
SOFT = {"deucalion", "talos", "pontus", "elpis", "gaia"}
FLAT = {"singleton", "pairwise", "khione", "ouranos", "polydeuces", "overtone"}
KEEP = {}

if __name__ == "__main__":
    for n, lo, mL in GROUND:
        a = load_any(n, "front"); print(n, "front ground cells", ug(a, lo, minL=mL)); save(a, n, "front")
    for n in NAMES:
        g = hx.specks(n, "front")
        if g: print(n, "stray cells off", g)
    #  SINGLETON / PAIRWISE: irises crimson, the orange spots below greyed
    print("singleton iris", hue_to("singleton", (14, 10, 48, 38), (5, 60), CRIMSON), "spots", grey_box("singleton", "front", (0, 37, 64, 64), hues=(5, 60)))
    print("pairwise irises", hue_to("pairwise", (6, 12, 56, 38), (5, 60), CRIMSON), "spots", grey_box("pairwise", "front", (0, 37, 64, 64), hues=(5, 60)))
    #  FEDERATED: every core teal, the big centre one split by a dark bar -- four cores, kept apart
    print("federated cores", hue_to("federated", (0, 0, 64, 64), (30, 75), TEAL))
    a = load_any("federated", "front")
    for y in range(13, 35):
        for x in (28, 29, 30, 31, 32):
            if op(a)[y, x] and not is_mark(a[y:y + 1, x:x + 1])[0, 0]: a[y, x] = INK if x in (28, 32) else (96, 100, 110, 255)
    save(a, "federated", "front")
    #  DEUCALION: cracks across brow, chest and haunch
    for pts in ([(25, 9), (27, 13), (25, 16), (26, 19)], [(19, 37), (22, 40), (20, 43), (22, 46)], [(37, 40), (39, 43), (37, 46)]):
        paint_line("deucalion", pts, CRACK)
    #  KHIONE: snowflakes held in its antlers
    for x, y in ((3, 7), (58, 8), (19, 5), (40, 4)): stamp_on("khione", x, y, FLAKE, FLAKEK, behind=True)
    #  TALOS: a bolt on its chest
    stamp_safe("talos", 21, 38, BOLT, BOLTK)
    #  GAIA: a two-peaked rock mountain on its shell, a tiny tree on the right peak
    a = load_any("gaia", "front"); print("gaia mountain", poly_fill(a, [(14, 13), (24, 1), (29, 6), (36, 3), (46, 13)], ROCK)); save(a, "gaia", "front")
    paint_line("gaia", [(24, 3), (22, 8)], (176, 174, 170, 255)); paint_line("gaia", [(36, 5), (34, 9)], (176, 174, 170, 255))
    stamp_on("gaia", 35, 0, TREE, TREEK, behind=False)
    #  OURANOS: a small cloud under its lower tip
    for cx, cy, r in ((45, 45, 2.6), (49, 43, 3.2), (53, 46, 2.4)): disc("ouranos", cx, cy, r, CLOUD)
    #  POLYDEUCES: the twins' star
    stamp_on("polydeuces", 27, 1, STARG, STARGK, behind=True)
    #  CASTOR: neck and head dark
    print("castor neck", darken("castor", (19, 4, 30, 33)))
    #  OVERTONE: two rings of sound from its open beak
    print("overtone rings", arc("overtone", 13, 12, 4, 120, 240, SOUND) + arc("overtone", 13, 12, 7, 125, 235, SOUND))
    for n, box in FACE.items():
        a = load_any(n, "front"); m = soft_face(a, box) if n in SOFT else features_off2(a, box, dark=n in DARKFACE, flat=n in FLAT)
        if n in FLAT: soft_face(a, (max(0, box[0] - 4), max(0, box[1] - 4), min(64, box[2] + 4), min(64, box[3] + 4)))
        save(a[:, ::-1].copy(), n, "back"); print(n, "back mirrored, feature cells", m)
    a = load_any("federated", "front"); save(a[:, ::-1].copy(), "federated", "back"); print("federated back mirrored (no face; its cores are on its back)")
    for n in NAMES:
        for k in ("front", "back"):
            kp = KEEP.get(n)
            g = hx.trim(n, k, keep=kp)
            if g: print(n, k, "accent cells greyed for the cap", g)
            left = hx.trap(n, k, "grey", s_min=0.25, acc_only=True)
            if left: print(n, k, "still in the type's hue reach, greyed:", left)
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", len(os.listdir(H)))

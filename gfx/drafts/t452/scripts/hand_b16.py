"""T-452 batch 16 by hand, PHASE 1 on the RECOMMENDED answers (apply the recommended fix for every issue, as batches
10-15 did). hand_b15.py's helpers, copied, with batch 16's edits in the main block.

    hand_b16.py      writes T/u/hand/<name>_{front,back}.png from u/clean (starts from clean every run)

LOST KEYS, drawn by hand: SINKHOLE's pincer jaws, DUSTDEVIL's dust swirl, CRACKLE's sparks, ARCFLASH's arc,
PIXELBYTE's pixels, STOPGRAD's and STALEMATE's icicles, FEWSHOT's water drop, LOCKFILE's padlock, BREATHING's pearl,
GUTFEEL's black pearl, ANODE's plus and CATHODE's minus (each on an ear).
BACKS       the front mirrored, face out, for all 21.
CAP         accents trimmed under 15%; anything left in the type's hue reach greyed; near-marker colours fixed."""
import os, sys, json, shutil
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("T452_ROOT", "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b16_work")
import hand4 as h4
import hand_b5 as hb
import hand_b10lib as hx   # hand_b10's helpers, without its writes
T = os.environ["T452_ROOT"]; F = T + "/u"; H = F + "/hand"
if os.path.isdir(H): shutil.rmtree(H)
os.makedirs(H)
hb.F, hb.H = F, H; h4.F, h4.H = F, H; hx.F, hx.H = F, H
from hand4 import load_any, save, ug, sanitize, stamp, op, lum, is_mark, INK
P = json.load(open(F + "/picks.json")); hx.P = P
NAMES = ['sinkhole', 'shimmer', 'dustdevil', 'postulate', 'deduction', 'crackle', 'arcflash', 'pixelbyte', 'reforge', 'stopgrad', 'permafrost', 'fewshot', 'zeroshot', 'lockfile', 'stalemate', 'lilendian', 'bigendian', 'breathing', 'gutfeel', 'anode', 'cathode']
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

GROUND = [("sinkhole", 0.5, 150), ("deduction", 0.88, 110), ("stopgrad", 0.9, 110), ("permafrost", 0.88, 110), ("lockfile", 0.9, 150)]
LOWGROUND = [("lilendian", (20, 56, 40, 64), lambda c, L: L > 140), ("breathing", (8, 53, 52, 64), lambda c, L: L > 100),
             ("anode", (12, 50, 50, 56), lambda c, L: L > 120), ("cathode", (12, 50, 52, 56), lambda c, L: L > 120)]
FACE = {"sinkhole": (8, 12, 30, 30), "shimmer": (17, 24, 33, 36), "dustdevil": (22, 22, 40, 38), "postulate": (16, 12, 48, 32),
        "deduction": (12, 10, 48, 32), "crackle": (8, 8, 36, 32), "arcflash": (8, 4, 30, 24), "pixelbyte": (12, 8, 48, 34),
        "reforge": (10, 12, 34, 32), "stopgrad": (16, 10, 44, 32), "permafrost": (20, 4, 46, 30), "fewshot": (10, 10, 36, 32),
        "zeroshot": (4, 16, 32, 40), "lockfile": (12, 8, 52, 28), "stalemate": (12, 8, 36, 24), "lilendian": (16, 8, 46, 30),
        "bigendian": (20, 8, 46, 30), "breathing": (12, 8, 52, 38), "gutfeel": (14, 8, 46, 34), "anode": (20, 14, 46, 36),
        "cathode": (20, 12, 46, 34)}
DARKFACE = {"bigendian", "reforge"}
SOFT = {"lockfile", "stalemate", "breathing", "deduction", "pixelbyte"}
KEEP = {"lockfile": (28, 34, 37, 44), "anode": (12, 8, 24, 20), "cathode": (18, 10, 30, 24), "fewshot": (18, 34, 24, 42)}

if __name__ == "__main__":
    for n, lo, mL in GROUND:
        a = load_any(n, "front"); print(n, "front ground cells", ug(a, lo, minL=mL)); save(a, n, "front")
    for n, box, test in LOWGROUND: print(n, "low ground cells", low_ground(n, "front", box, test))
    for n in NAMES:
        g = hx.specks(n, "front")
        if g: print(n, "stray cells off", g)
    print("dustdevil marks moved", shift_marks("dustdevil", 0, 6))
    a = load_any("sinkhole", "front"); a[54:] = 0; a[45:, 56:] = 0; save(a, "sinkhole", "front")
    print("sinkhole pit rim off", keep_main("sinkhole"))
    stamp_on("sinkhole", 1, 14, JAW_UP, LG, behind=True); stamp_on("sinkhole", 1, 26, JAW_DN, LG, behind=True)
    print("dustdevil swirl", funnel("dustdevil", [(44, 36, 13), (48, 37, 10), (52, 38, 7), (56, 39, 4)]))
    for x, y in ((0, 26), (36, 22), (55, 12)): stamp_on("crackle", x, y, SPARK, SPARKK, behind=True)
    print("arcflash arc", bolt("arcflash", [(37, 6), (41, 2), (44, 8), (48, 3), (51, 10), (54, 7)]))
    print("pixelbyte pixels", pixels("pixelbyte", [(59, 48, (226, 226, 230)), (61, 45, (70, 72, 80)), (57, 44, (226, 226, 230)),
                                                    (62, 50, (150, 152, 160)), (60, 41, (90, 200, 200)), (55, 47, (150, 152, 160))]))
    for x, y in ((7, 36), (11, 36), (51, 47)): stamp_on("stopgrad", x, y, ICICLE, ICEK, behind=True)
    for x, y in ((43, 49), (48, 50), (53, 51)): stamp_on("stalemate", x, y, ICICLE, ICEK, behind=True)
    stamp_safe("fewshot", 18, 34, DROP, BLUEK)
    stamp_safe("lockfile", 28, 34, LOCK, LOCKK)
    stamp_on("breathing", 25, 1, PEARL, PEARLK, behind=True)
    print("gutfeel marks moved", shift_marks("gutfeel", 0, 4)); stamp_safe("gutfeel", 29, 39, BPEARL, BPEARLK)
    stamp_safe("anode", 14, 10, PLUS, SIGNK)
    print("cathode ear indigo", ear_tint("cathode", 24, 17, 5, (70, 60, 190)))
    stamp_safe("cathode", 21, 16, MINUS, SIGNK)
    for n, box in FACE.items():
        a = load_any(n, "front"); m = soft_face(a, box) if n in SOFT else features_off2(a, box, dark=n in DARKFACE)
        save(a[:, ::-1].copy(), n, "back"); print(n, "back mirrored, feature cells", m)
    for n in NAMES:
        for k in ("front", "back"):
            kp = KEEP.get(n)
            if kp and k == "back": kp = (64 - kp[2], kp[1], 64 - kp[0], kp[3])
            g = hx.trim(n, k, keep=kp)
            if g: print(n, k, "accent cells greyed for the cap", g)
            left = hx.trap(n, k, "grey", s_min=0.25, acc_only=True)
            if left: print(n, k, "still in the type's hue reach, greyed:", left)
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", len(os.listdir(H)))

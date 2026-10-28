"""T-452 batch 14 by hand, PHASE 1 on the RECOMMENDED answers (the coordinator, 2026-10-28: apply the recommended fix
for every issue, as batches 10-13 did). hand_b13.py's helpers, copied, with batch 14's edits in the main block.

    hand_b14.py      writes T/s/hand/<name>_{front,back}.png from s/clean (starts from clean every run)

LOST KEYS, drawn by hand: HASHSEED's criss-cross seed, IFTRUE's tick mark, THENCASE's arrow marks, OTHERWISE's antenna
lights, POLICY's leaf fan, BURSTMODE's speed lines, DEFUNCT's split (and blank eyes), LONGJUMP's house locket,
CHECKMATE's checkerboard, TANGENT's arrow crest, JACOBIAN's arrows; SPARRING's second glove (the clean wore it away).
TYPE-HUE TRAP: SHORTJUMP's and LONGJUMP's orange beaks and feet crimson (NORMAL 40); anything else in reach greyed.
BACKS       the front mirrored, face out, for all 21.
CAP         accents trimmed under 15%; near-marker colours fixed (hand4.sanitize)."""
import os, sys, json, shutil
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("T452_ROOT", "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b14_work")
import hand4 as h4
import hand_b5 as hb
import hand_b10lib as hx   # hand_b10's helpers, without its writes
T = os.environ["T452_ROOT"]; F = T + "/s"; H = F + "/hand"
if os.path.isdir(H): shutil.rmtree(H)
os.makedirs(H)
hb.F, hb.H = F, H; h4.F, h4.H = F, H; hx.F, hx.H = F, H
from hand4 import load_any, save, ug, sanitize, stamp, op, lum, is_mark, INK
P = json.load(open(F + "/picks.json")); hx.P = P
NAMES = ['hashseed', 'iftrue', 'thencase', 'iffalse', 'otherwise', 'tempo', 'cadence', 'cyclical', 'warmup', 'shaping', 'policy', 'prefork', 'burstmode', 'defunct', 'shortjump', 'longjump', 'sparring', 'checkmate', 'hashcode', 'tangent', 'jacobian']
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


# ---------------------------------------------------------------- batch 14's edits
SEED = ["  ####  ", " #LLML# ", "#LMLLML#", "#MLMLMD#", "#LLMLLD#", "#MLLMDD#", " #DMDD# ", "  ####  "]   # a round seed, criss-cross lines (M) across it
SEEDK = {"#": INK, "L": (206, 210, 216, 255), "M": (96, 100, 108, 255), "D": (150, 154, 162, 255)}
TICK = ["      ##", "     ##W", "##  ##W ", "W## ##  ", " W###   ", "  W#    "]   # a dark tick with a pale edge
TICKK = {"#": (40, 42, 50, 255), "W": (250, 250, 252, 255)}
LIGHT = [" #C# ", "#CWC#", "CWWWC", "#CWC#", " #C# "]   # a pale aqua light: BUG is 76 degrees, so amber (40) would sit in its trap; aqua 175 does not
LIGHTK = {"#": (60, 64, 72, 255), "C": (140, 222, 206, 255), "W": (226, 255, 248, 255)}
FAN = ["   ###   ", "  #LML#  ", " #LLMLL# ", "#LLLMLLL#", "#LLLMLLL#", "#MLLMLLM#", " #MLMLM# ", "  #MMM#  ", "   #D#   ", "   #D#   ", "   #D#   "]
FANK = {"#": INK, "L": (190, 196, 200, 255), "M": (110, 116, 122, 255), "D": (70, 72, 80, 255)}   # a leaf fan, veins dark, a stalk
HOUSE = ["  #  ", " #W# ", "#WWW#", "#W#W#", "#####"]
HOUSEK = {"#": INK, "W": (244, 244, 246, 255)}
GLOVE = [" #### ", "#RRRR#", "#RRRRR#", "#RRRRR#", "#DRRRD#", " #DDD# ", "  ###  "]
GLOVEK = {"#": INK, "R": (150, 40, 50, 255), "D": (100, 26, 36, 255)}   # the drawn glove's own dark red
ARROW = ["   #  ", "####W#", "WWWWWW#", "####W#", "   #  "]   # pointing right, its heading
ARROWK = {"#": INK, "W": (250, 250, 252, 255)}
CHEV = ["##     ##", " ##   ## ", "  ## ##  ", "   ###   ", "    #    "]   # a bold chevron (two cells thick) pointing down; flipped for up
def chev_up(n, x, y, col):
    a = load_any(n, "front")
    for dy, row in enumerate(CHEV[::-1]):
        for dx, ch in enumerate(row):
            if ch == "#" and op(a)[y + dy, x + dx] and not is_mark(a[y + dy:y + dy + 1, x + dx:x + dx + 1])[0, 0]: a[y + dy, x + dx] = col
    save(a, n, "front")

def checker(n, box, dark=(60, 62, 70, 255), light=(236, 238, 240, 255), cell=2):
    a = load_any(n, "front"); x0, y0, x1, y1 = box; m = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not op(a)[y, x] or is_mark(a[y:y + 1, x:x + 1])[0, 0] or lum(a[y:y + 1, x:x + 1])[0, 0] < 50: continue
            a[y, x] = dark if ((x - x0) // cell + (y - y0) // cell) % 2 else light; m += 1
    save(a, n, "front"); return m

def blank_eyes(n, boxes, fill=(214, 218, 224, 255)):
    """eyes to blank pale discs: every non-outline cell in each eye box (lum >= 30 or saturated) to FILL, outline kept"""
    a = load_any(n, "front"); m = 0
    for x0, y0, x1, y1 in boxes:
        for y in range(y0, y1):
            for x in range(x0, x1):
                if op(a)[y, x] and not is_mark(a[y:y + 1, x:x + 1])[0, 0] and lum(a[y:y + 1, x:x + 1])[0, 0] >= 24:
                    a[y, x] = fill; m += 1
    save(a, n, "front"); return m

def speed_lines(n, rows, x0, x1, col=(200, 204, 212, 255)):
    a = load_any(n, "front"); o = op(a).copy(); m = 0
    for y, (s, e) in rows:
        for x in range(s, e):
            if not o[y, x]: a[y, x] = col; m += 1
    save(a, n, "front"); return m

GROUND = [("checkmate", "front", 0.9, dict(minL=110)), ("prefork", "front", 0.9, dict(minL=110))]
FACE = {"hashseed": [(8, 26, 40, 40)], "iftrue": [(16, 16, 46, 40)], "thencase": [(20, 22, 46, 38)], "iffalse": [(24, 10, 42, 28)],
        "otherwise": [(22, 24, 44, 36)], "tempo": [(12, 26, 52, 42)], "cadence": [(20, 16, 46, 28)], "cyclical": [(22, 16, 48, 28)],
        "warmup": [(14, 12, 40, 26)], "shaping": [(12, 16, 46, 32)], "policy": [(8, 18, 30, 32)], "prefork": [(26, 24, 46, 32)],
        "burstmode": [(24, 24, 40, 36)], "defunct": [(20, 16, 44, 30)], "shortjump": [(8, 16, 46, 38)], "longjump": [(16, 22, 40, 34)],
        "sparring": [(18, 20, 40, 32)], "checkmate": [(20, 6, 36, 20)], "hashcode": [(12, 24, 52, 40)], "tangent": [(42, 12, 60, 30)],
        "jacobian": [(26, 8, 40, 20)]}
DARKFACE = {"iffalse", "burstmode", "prefork"}
SOFT = {"shortjump", "hashcode", "iftrue", "tempo"}   # a big light head: a flat fill reads as a plate

if __name__ == "__main__":
    for n, k, lo, kw in GROUND:
        a = load_any(n, k); print(n, k, "ground cells", ug(a, lo, **kw)); save(a, n, k)
    print("checkmate bluish shadow off", low_ground("checkmate", "front", (14, 56, 50, 64), lambda c, l: int(c[2]) > int(c[0]) + 14 and l > 100))
    print("jacobian white halo off", hx.halo("jacobian", "front"))
    #  the hue trap, by hand where a colour is the point: NORMAL's orange beaks and feet crimson
    print("shortjump beak crimson", hx.trap("shortjump", "front", "hue", (16, 26, 38, 38), to=350, s_min=0.3),
          "feet", hx.trap("shortjump", "front", "hue", (12, 52, 46, 64), to=350, s_min=0.3))
    print("longjump beak crimson", hx.trap("longjump", "front", "hue", (26, 26, 42, 36), to=350, s_min=0.3),
          "feet", hx.trap("longjump", "front", "hue", (36, 42, 50, 50), to=350, s_min=0.3))
    #  lost keys
    stamp_on("hashseed", 47, 40, SEED, SEEDK)
    stamp_on("iftrue", 20, 48, TICK, TICKK)
    for x, y in ((6, 16), (8, 22), (46, 16), (48, 22)): chev_up("thencase", x, y, (60, 64, 74, 255))
    stamp_on("otherwise", 6, 8, LIGHT, LIGHTK); stamp_on("otherwise", 44, 8, LIGHT, LIGHTK)
    stamp_on("policy", 0, 18, FAN, FANK, behind=True)
    print("burstmode speed lines", speed_lines("burstmode", [(30, (2, 22)), (34, (4, 24)), (38, (2, 22)), (30, (42, 62)), (34, (40, 60)), (38, (42, 62))], 0, 64))
    print("defunct split", paint_line("defunct", [(32, 14), (31, 18), (33, 22), (31, 26), (33, 30), (32, 33)], (24, 24, 30, 255), width=2, skip_dark=False))
    print("defunct eyes blank", blank_eyes("defunct", [(22, 22, 29, 30), (35, 22, 42, 30)]))
    stamp_on("longjump", 21, 33, HOUSE, HOUSEK)
    print("longjump string", paint_line("longjump", [(23, 32), (28, 31)], (40, 42, 50, 255), skip_dark=False))
    stamp_on("sparring", 15, 31, GLOVE, GLOVEK, behind=True)
    print("checkmate checkerboard", checker("checkmate", (26, 49, 36, 57)))
    stamp_on("tangent", 37, 3, ARROW, ARROWK)
    for x, y in ((12, 24), (17, 21), (22, 18)): stamp_on("jacobian", x, y, ["W#", "#W"] if x % 2 else ["#W", "W#"], {"W": (250, 250, 252, 255), "#": (40, 42, 50, 255)}, onto=True)
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

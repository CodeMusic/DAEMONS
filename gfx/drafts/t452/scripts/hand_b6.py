"""T-452 batch 6, by hand (the user's answers via the coordinator, 2026-10-27). hand4.py's and hand_b5.py's helpers.

    hand_b6.py      writes T/i/hand/<name>_{front,back,icon}.png (from i/clean and i/reduced)

KEEPER      a little one peeking out of a pouch on its belly (front and icon): the entry, "carries the next one"
CRON        the face painted out, one big round gem in the centre (as today's and BEACON's)
MIME        both gloves raised to shoulder height, palms out, as if on glass; its back scaled up to 58 rows
BOTTLENECK  the neck pinched thin by hand
HARDCODE    the saddle painted out (warm cells to the body's grey, the hump above the back cut away)
SIGKILL     the crab-like pincer tips cut off: short blunt beetle forelegs (front), then the back
BACKS       MIGRATE, SIGKILL, SLURP, SPAGHETTI, SPAWN: the front MIRRORED with the face's features painted out
GROUNDS     baked grounds off the clean grids (hand4.ug)
SANITIZE    hand3's: a drawn colour within reach of a streak marker darkened or greyed"""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hand4 as h4
import hand_b5 as hb
R = "/Users/christopherhicks/Projects/DAEMONS"; F = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452") + "/i"; H = F + "/hand"
hb.F, hb.H = F, H; h4.F, h4.H = F, H
from hand4 import load_any, sanitize, save, ug, outline, stamp, body_grey, op, lum, is_mark, INK
NAMES = ["slurp", "exhaust", "smogstack", "hardcode", "migrate", "uptime", "heartbeat", "spaghetti", "keeper", "bottleneck",
         "backpress", "turbulence", "spawn", "upstream", "beacon", "cron", "mime", "reaper", "sigkill", "coldread", "tell"]

def disc(a, cx, cy, r, c, skip_marks=True, only_opaque=False):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if not (0 <= y < 64 and 0 <= x < 64) or (x - cx) ** 2 + (y - cy) ** 2 > r * r: continue
            if skip_marks and is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
            if only_opaque and a[y, x, 3] <= 127: continue
            a[y, x] = c

def limb(a, p0, p1, r_in, r_out, fill):
    """hand_b5.thick_line, but never over a streak marker"""
    (x0, y0), (x1, y1) = p0, p1; n = int(max(abs(x1 - x0), abs(y1 - y0))) * 2 + 1
    pts = [(x0 + (x1 - x0) * i / (n - 1), y0 + (y1 - y0) * i / (n - 1)) for i in range(n)]
    for r, c in ((r_out, INK), (r_in, fill)):
        for cx, cy in pts: disc(a, cx, cy, r, c)

def clear(a, box, keep_marks=True):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            if keep_marks and is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
            a[y, x] = 0

# ---- KEEPER: the little one in the pouch
LIGHT = (226, 226, 232, 255); MID = (160, 160, 170, 255); DARK = (96, 96, 108, 255)
KID = ["   #####   ",
       "  #LLLLL#  ",
       " #LLLLLLL# ",
       " #L#LLL#L# ",
       " #L#LLL#L# ",
       " #LLLMLLL# ",
       "###########",
       "#MMMMMMMMM#",
       "#MDMMMMMDM#",
       " #MMMMMMM# ",
       "  #######  "]
def keeper():
    a = load_any("keeper", "front"); print("keeper ground", ug(a, 0.85, minL=110))
    stamp(a, 27, 43, KID, {"#": INK, "L": LIGHT, "M": MID, "D": DARK})
    save(a, "keeper", "front")
    ic = Image.open(f"{F}/reduced/keeper_icon.png"); x = np.array(ic)
    pat = ["  FFFF  ", " F3333F ", "F3F33F3F", "F333333F", "FFFFFFFF"]
    for f in (0, 1):
        for dy, row in enumerate(pat):
            for dx, ch in enumerate(row):
                if ch != " ": x[f * 32 + 25 + f + dy, 12 + dx] = int(ch, 16)
    o = Image.fromarray(x, "P"); o.putpalette(ic.getpalette()); o.save(f"{H}/keeper_icon.png")

# ---- CRON: the face off, one big gem
GEM = ((24, 60, 110, 255), (60, 130, 196, 255), (128, 190, 236, 255), (230, 246, 255, 255))
def cron():
    a = load_any("cron", "front"); fill = body_grey(a, (14, 16, 50, 46))
    hb.features_off(a, (20, 18, 46, 44))
    disc(a, 33, 32, 10.5, INK); disc(a, 33, 32, 9.5, GEM[0]); disc(a, 33, 32, 8.5, GEM[1])
    disc(a, 31, 30, 5.5, GEM[2]); disc(a, 29, 28, 2.2, GEM[3])
    save(a, "cron", "front")

# ---- MIME: the gloves raised, palms out
GLOVE = ["  # # # #  ",
         " #W#W#W#W# ",
         " #W#W#W#W# ",
         " #W#W#W#W##",
         " #WWWWWWW#W#",
         " #WWWWWWWWW#",
         " #WSWWWWWW# ",
         " #WWWWWWWW# ",
         "  #WWWWWW#  ",
         "   ######   "]
def mime():
    a = load_any("mime", "front"); sleeve = body_grey(a, (20, 28, 44, 40))
    clear(a, (3, 28, 18, 44)); clear(a, (46, 28, 62, 44))
    limb(a, (19, 34), (12, 36), 2.3, 3.3, sleeve); limb(a, (12, 36), (11, 22), 2.3, 3.3, sleeve)
    limb(a, (44, 34), (51, 36), 2.3, 3.3, sleeve); limb(a, (51, 36), (52, 22), 2.3, 3.3, sleeve)
    K = {"#": INK, "W": (244, 246, 252, 255), "S": (200, 206, 222, 255)}
    stamp(a, 5, 10, GLOVE, K)
    stamp(a, 47, 10, [r[::-1] for r in GLOVE], K)
    save(a, "mime", "front")
    #  the back: scaled up to 58 rows, centred, standing on row 62
    b = load_any("mime", "back"); ys, xs = np.where(op(b)); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    s = 58 / (y1 - y0); im = Image.fromarray(b[y0:y1, x0:x1].astype(np.uint8), "RGBA")
    im = im.resize((round((x1 - x0) * s), 58), Image.NEAREST)
    out = np.zeros((64, 64, 4), int); sx = 32 - im.width // 2; c = np.array(im).astype(int)
    out[62 - 58 + 1:63, sx:sx + im.width] = c
    save(out, "mime", "back")

# ---- BOTTLENECK: the neck pinched thin
def bottleneck():
    a = load_any("bottleneck", "front")
    for y in range(27, 32):
        for x in range(64):
            if a[y, x, 3] > 127 and not (31 <= x <= 36) and not is_mark(a[y:y + 1, x:x + 1])[0, 0]: a[y, x] = 0
    for y in range(27, 32):
        a[y, 30] = INK; a[y, 37] = INK
    outline(a, (25, 34)); save(a, "bottleneck", "front")

# ---- HARDCODE: the saddle off
def hardcode():
    a = load_any("hardcode", "front"); print("hardcode ground", ug(a, 0.80, minL=110))
    ramp = [(70, 74, 86), (120, 126, 140), (168, 174, 188), (214, 218, 228)]
    for y in range(8, 30):
        for x in range(16, 48):
            p = a[y, x]
            if p[3] <= 127 or is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
            if p[0] - p[2] > 25:
                if y < 17 and x < 36: a[y, x] = 0; continue
                L = lum(a[y:y + 1, x:x + 1])[0, 0]; a[y, x, :3] = ramp[min(3, int(L) // 64)]
    #  the hump the saddle stood on cut back to the body's line (row 18), and its straps (dark bands) to the hide's grey
    clear(a, (10, 0, 35, 18))
    L = lum(a); o = op(a); mk = is_mark(a)
    for y in range(18, 30):
        for x in range(13, 36):
            if o[y, x] and not mk[y, x] and L[y, x] < 80 and all(o[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                a[y, x, :3] = (150, 156, 170) if y % 5 else (120, 126, 140)
    outline(a, (14, 30)); save(a, "hardcode", "front")

# ---- SIGKILL: blunt beetle forelegs, not crab pincers
def sigkill():
    a = load_any("sigkill", "front"); print("sigkill ground", ug(a, 0.85, minL=110))
    clear(a, (0, 0, 22, 23)); clear(a, (43, 0, 64, 23))
    fill = body_grey(a, (6, 22, 20, 34))
    disc(a, 12, 24, 5.0, INK); disc(a, 12, 24, 4.0, fill); disc(a, 11, 23, 1.5, (210, 214, 224, 255))
    disc(a, 52, 24, 5.0, INK); disc(a, 52, 24, 4.0, fill); disc(a, 51, 23, 1.5, (210, 214, 224, 255))
    outline(a, (0, 40)); save(a, "sigkill", "front")

def mirrored_soft(n, box, thr):
    """hand_b5.features_off with a higher threshold (the eye RINGS go too, not only the pupils), then mirrored"""
    a = load_any(n, "front"); x0, y0, x1, y1 = box; o = op(a); L = lum(a); mk = is_mark(a)
    sat = a[..., :3].max(-1) - a[..., :3].min(-1)
    reg = a[y0:y1, x0:x1].reshape(-1, 4); rl = lum(reg[None])[0]; rs = reg[:, :3].max(-1) - reg[:, :3].min(-1)
    pool = reg[(reg[:, 3] > 127) & (rl >= 150) & (rs < 40)]; fill = np.median(pool, 0).astype(int); k = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not o[y, x] or mk[y, x]: continue
            if any(not o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): continue
            if L[y, x] < thr or sat[y, x] >= 60:
                a[y, x] = fill.copy(); a[y, x, :3] = np.clip(fill[:3] + (int(L[y, x]) - thr) // 6, 0, 255); k += 1
    print(n, "soft face cells", k); save(a[:, ::-1].copy(), n, "back")

GROUNDS = (("reaper", "back", 0.80, dict(minL=110)), ("coldread", "back", 0.88, dict(minL=110)),
           ("tell", "back", 0.88, dict(minL=110)), ("turbulence", "back", 0.85, dict(minL=110)),
           ("uptime", "back", 0.88, dict(minL=110)), ("slurp", "front", 0.80, dict(minL=110)))

if __name__ == "__main__":
    os.makedirs(H, exist_ok=True)
    for f in os.listdir(H): os.remove(f"{H}/{f}")
    for n, k, lo, kw in GROUNDS:
        a = load_any(n, k); print(n, k, "ground", ug(a, lo, **kw)); save(a, n, k)
    keeper(); cron(); mime(); bottleneck(); hardcode(); sigkill()
    hb.mirrored_features("migrate", (22, 30, 44, 44))
    hb.mirrored_features("sigkill", (18, 30, 48, 47))
    mirrored_soft("slurp", (10, 18, 40, 35), 150)
    mirrored_soft("spaghetti", (18, 14, 50, 32), 110)
    hb.mirrored_features("spawn", (10, 22, 26, 36))
    for n in NAMES:
        for k in ("front", "back"):
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", sorted(os.listdir(H)))

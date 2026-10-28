"""T-452 batch 5 FOLLOW-UPS (the user, 2026-10-27, multiple choice -- all six), by hand over the built art.

    fu_b5.py            writes T/h/fu/<name>_{front,back}.png
    fu_b5.py install    copies h/fu/ into gfx/daemons/ (and h/fu/<name>_icon.png where icon3 drew one)
    fu_b5.py icons      icon3 from the new fronts of ICONS, into h/fu/ and h/picks.json's icon3 rows

ACQUIRE    the one big claw a solid curved crab pincer (it read as a bone or a wrench): a fat palm, two curved
           tapering fingers closing round a gap, a thick arm down to the shell; from the clean grid (the small
           claw on the right taken off first). The back gets the same pincer, on its left (a back faces the other way).
AXIOMKICK  the kicking leg thicker, a knee and a foot (it read as a held stick): thigh up and out from behind the body,
           a bent knee with a cap, a shin back in, a cuffed ankle and a foot kicked out at the top. From the clean grid,
           which also gives back the fourth streak marker the stick had painted over. The leg crosses in front of the
           right arm, behind the body.
ARCHIVER   icier: a frost cap over the crown, frost speckles down the back and tail, icicles under the tail and the
           chin, frost sparkles in the air. All in WHITE and pale grey -- a pale cyan accent would sit within 40 degrees
           of WATER's blue and gbasprite would turn it orange (shift_off); the type ramp's highlight is the ice. The
           back is the new front mirrored with the face painted out (hand_b5's rule).
BREAKER    bigger (the ball and its feet widened by repeating interior rows and columns, never an outline row: about
           56 wide against FUSE's 44), cracked (dark zigzag cracks with a lit edge across the shell) and sparking
           (amber bolts round it -- ELECTRIC is teal, so amber is an accent and stays). Front and back.
CIRCULAR   a clear headstand, face at the ground: the long legs kept straight up; the torso and head below them turned
           upside down as one, so the face is upside down with its crown on the ground line; the arms turned down, hands
           planted either side of the head; the small legs it stood on taken off. The back is the new front mirrored,
           face features off.
BOOTSTRAP  the back shows six eggs as the front does: the front mirrored, every face (eyes, beak bands) painted out."""
import os, sys, json, shutil
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hand4 as h4
R = "/Users/christopherhicks/Projects/DAEMONS"; F = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452") + "/h"; H = F + "/fu"
GD = R + "/gfx/daemons"
h4.F, h4.H = F, H
from hand4 import sanitize, outline, paint_out, body_grey, op, lum, is_mark, INK
import hand_b5 as hb
NAMES = ["acquire", "axiomkick", "archiver", "breaker", "circular", "bootstrap"]
ICONS = ["acquire", "axiomkick", "breaker", "circular"]   # ARCHIVER keeps its drawn icon: from the front it went to a blob

def rgba(p): return np.array(Image.open(p).convert("RGBA")).astype(int)
BASE = os.environ.get("T452_FU_BASE", "5de571ba")       # the DAEMONS commit batch 5 was released from: redraws never stack
def built(n, k):
    import io, subprocess
    raw = subprocess.run(["git", "-C", R, "show", f"{BASE}:gfx/daemons/{n}_{k}.png"], capture_output=True, check=True).stdout
    return np.array(Image.open(io.BytesIO(raw)).convert("RGBA")).astype(int)
def clean(n, k): return rgba(f"{F}/clean/{n}_{k}.png")
def save(a, n, k): Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA").save(f"{H}/{n}_{k}.png")

# ---------------------------------------------------------------------------------------------------- drawing
S = 8
def mask_of(draw):
    """DRAW(d, s) paints white shapes on a 64*S canvas in 64-cell coordinates times s; back to 64x64 by majority"""
    im = Image.new("L", (64 * S, 64 * S), 0); draw(ImageDraw.Draw(im), S)
    v = np.array(im).reshape(64, S, 64, S).mean((1, 3))
    return v > 127

def disc(d, s, x, y, r): d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=255)
def taper(d, s, pts, r0, r1, steps=40):
    """a limb or a finger along the polyline PTS, its radius going R0 -> R1"""
    seg = [np.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    tot = sum(seg)
    for i in range(len(pts) - 1):
        for j in range(steps + 1):
            t = j / steps; x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t; y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t
            f = (sum(seg[:i]) + seg[i] * t) / tot; disc(d, s, x, y, r0 + (r1 - r0) * f)

def nb(m, dy, dx):
    """m shifted so out[y,x] = m[y+dy, x+dx] (False off the edge)"""
    o = np.zeros_like(m); H_, W_ = m.shape
    ys, ye = max(0, -dy), min(H_, H_ - dy); xs, xe = max(0, -dx), min(W_, W_ - dx)
    o[ys:ye, xs:xe] = m[ys + dy:ye + dy, xs + dx:xe + dx]; return o

def paint(a, m, ramp, where=None):
    """M shaded from the top left -- ramp = (highlight, light, mid, dark) -- and outlined in ink; only into WHERE"""
    hi, li, md, dk = ramp
    ring = (nb(m, 1, 0) | nb(m, -1, 0) | nb(m, 0, 1) | nb(m, 0, -1)) & ~m
    out_ul = ~nb(m, -1, 0) | ~nb(m, 0, -1); out_ul2 = ~nb(m, -2, 0) | ~nb(m, 0, -2)
    out_dr = ~nb(m, 1, 0) | ~nb(m, 0, 1)
    ok = np.ones_like(m) if where is None else where
    for y, x in zip(*np.where(ring & ok)): a[y, x] = INK
    for y, x in zip(*np.where(m & ok)):
        a[y, x] = li if out_ul[y, x] else dk if out_dr[y, x] else md
    return int((m & ok).sum())

def layers(a, parts, ramp, free):
    """PARTS painted in order, each over the last (its ink ring parts it from what it lies on); FREE says where the
    first may go, and each later one may also go over the parts before it"""
    drawn = np.zeros((64, 64), bool); n = 0
    for m in parts:
        n += paint(a, m, ramp, free | drawn); drawn |= m
    return n

GREY = ((240, 240, 244, 255), (214, 214, 222, 255), (158, 158, 168, 255), (104, 104, 116, 255))

# ---------------------------------------------------------------------------------------------------- ACQUIRE
def pincer(d, s, X, dy=0, arm=True):
    """the big claw in front coordinates; X maps an x (identity on the front, a mirror on the back)"""
    P = lambda pts: [(X(x), y + dy) for x, y in pts]
    if arm == "arm": taper(d, s, P([(45, 23), (47.5, 18), (49.5, 14.5)]), 2.2, 2.2)
    if arm == "palm":
        cx, cy = X(50.5), 10 + dy; d.ellipse([(cx - 6.6) * s, (cy - 5.2) * s, (cx + 6.6) * s, (cy + 5.2) * s], fill=255)
        taper(d, s, P([(46, 12.2), (42, 12.4), (39, 11.2), (36.8, 9.4)]), 2.5, 0.7)      # the fixed finger, curving up
    if arm == "dactyl":
        taper(d, s, P([(47, 6.5), (43, 3.6), (39, 3.4), (36.4, 5.0), (35.0, 6.8)]), 2.6, 0.7)  # the moving finger, curving down

def acquire():
    a = clean("acquire", "front")
    a[0:19, 40:51] = 0                                                   # the small right claw off
    for y in range(19, 22):
        for x in range(44, 51):
            if lum(a[y:y + 1, x:x + 1])[0, 0] >= 60 and x >= 47: a[y, x] = 0
    parts = [mask_of(lambda d, s, k=k: pincer(d, s, lambda x: x, arm=k)) for k in ("arm", "palm", "dactyl")]
    print("acquire front claw cells", layers(a, parts, GREY, a[..., 3] <= 127))
    for y, x in ((7, 50), (7, 51), (8, 49), (6, 52)): a[y, x] = GREY[0]          # a gloss on the palm
    outline(a); save(a, "acquire", "front")
    b = built("acquire", "back")
    b[0:16, 16:26] = 0                                                   # the left stub off (the back faces right)
    parts = [mask_of(lambda d, s, k=k: pincer(d, s, lambda x: 66 - x, dy=-2, arm=k)) for k in ("arm", "palm", "dactyl")]
    print("acquire back claw cells", layers(b, parts, GREY, b[..., 3] <= 127))
    outline(b); save(b, "acquire", "back")

# ---------------------------------------------------------------------------------------------------- AXIOMKICK
def axiomkick():
    a = clean("axiomkick", "front")
    for y in range(42, 52):
        for x in range(36, 48):
            if not is_mark(a[y:y + 1, x:x + 1])[0, 0]: a[y, x] = (0, 0, 0, 0)
    outline(a, (36, 52))
    base = body_grey(a, (24, 6, 40, 14)); L = np.array(base[:3])
    ramp = (tuple(np.minimum(255, L + 50)) + (255,), tuple(np.minimum(255, L + 22)) + (255,), base,
            tuple((L * 0.68).astype(int)) + (255,))
    thigh = mask_of(lambda d, s: taper(d, s, [(45, 37), (55, 22.5)], 4.0, 3.6))
    shin = mask_of(lambda d, s: (disc(d, s, 55, 22.5, 3.6), taper(d, s, [(55, 22.5), (49.5, 9.5)], 3.3, 2.6)))
    foot = mask_of(lambda d, s: (disc(d, s, 48.5, 9.0, 2.8), taper(d, s, [(49, 8), (54, 5), (58.5, 3.0)], 2.9, 2.2)))
    arm = np.zeros((64, 64), bool); arm[25:39, 47:62] = True
    free = (a[..., 3] <= 127) | arm                                       # behind the body, in front of the right arm
    print("axiomkick leg cells", layers(a, [thigh, shin, foot], ramp, free))
    for y, x in ((20, 56), (20, 57), (21, 57), (19, 56)): a[y, x] = ramp[0]   # the kneecap's light
    for y, x in zip(*np.where(foot & ~nb(foot, 1, 0) & (a[..., 3] > 127))): a[y, x] = ramp[3]   # the sole
    save(a, "axiomkick", "front")

# ---------------------------------------------------------------------------------------------------- ARCHIVER
WHITE = (246, 248, 252, 255); FROST = (226, 232, 240, 255)
def archiver():
    a = built("archiver", "front"); o = op(a); L = lum(a); mk = is_mark(a)
    #  a frost cap: the crown's interior from its top down to a ragged line
    edge = [17, 18, 20, 18, 17, 18, 21, 19, 17, 18, 19, 21, 19, 17, 18, 20, 18, 17, 18, 20, 18, 17, 18, 17]
    for i, x in enumerate(range(13, 37)):
        ys = [y for y in range(8, 30) if o[y, x]]
        if not ys: continue
        for y in range(ys[0] + 1, min(edge[i], 30)):
            if o[y, x] and L[y, x] >= 60 and not mk[y, x]: a[y, x] = WHITE if (y + x) % 3 else FROST
    #  frost speckles down the back and along the tail
    for y, x in ((34, 40), (36, 44), (35, 49), (38, 52), (37, 41), (33, 38), (40, 47), (36, 55)):
        if o[y, x] and L[y, x] >= 60 and not mk[y, x]: a[y, x] = WHITE
    #  icicles under the tail and the chin: an ink-edged white drip, longest in the middle
    def icicle(x, y, n):
        #  a tapering drip: three wide at the root, one at the tip, ink round it
        for k in range(n):
            w = 1 if k < n // 2 else 0
            for dx in range(-w, w + 1): a[y + k, x + dx] = WHITE if dx <= 0 else FROST
            for dx in (-w - 1, w + 1):
                if a[y + k, x + dx, 3] <= 127: a[y + k, x + dx] = INK
        a[y + n, x] = INK
    for x, n in ((43, 4), (47, 5), (51, 3), (24, 3), (29, 4)):
        y = max(yy for yy in range(64) if op(a)[yy, x] and yy < (49 if x > 40 else 52))
        icicle(x, y + 1, n)
    #  frost sparkles in the air
    def sparkle(x, y):
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): a[y + dy, x + dx] = WHITE
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            if a[y + dy, x + dx, 3] <= 127: a[y + dy, x + dx] = INK
    for x, y in ((8, 14), (44, 9), (56, 28), (4, 33)): sparkle(x, y)
    save(a, "archiver", "front")
    #  the face's fill: the head's own lighter body tone (body_grey's median sat a ramp step darker once the frost
    #  raised the top of the value range, and the painted-out face read as a dark block)
    b = a.copy(); hl = lum(b); sat = b[..., :3].max(-1) - b[..., :3].min(-1)
    sel = op(b) & (hl >= 150) & (hl <= 205) & (sat < 60); sel[:12] = False; sel[34:] = False; sel[:, :12] = False; sel[:, 38:] = False
    fill = tuple(int(v) for v in np.percentile(b[sel][:, :3], 80, 0)) + (255,)
    print("archiver face fill", fill, "cells", paint_out(b, (12, 18, 38, 34), fill))
    save(b[:, ::-1].copy(), "archiver", "back")

# ---------------------------------------------------------------------------------------------------- BREAKER
def widen(a, extra_x, extra_y):
    """repeat EXTRA interior rows and columns (fewest ink cells running along them, never two side by side)"""
    def pick(a2, n, axis):
        o = op(a2); ink = o & (lum(a2) < 60)
        idx = np.where(o.any(1 - axis))[0]; lo, hi = idx.min() + 4, idx.max() - 4
        if axis == 0: run = (ink & nb(ink, 0, 1)).sum(1)          # horizontal ink along a row
        else: run = (ink & nb(ink, 1, 0)).sum(0)                  # vertical ink along a column
        mkc = is_mark(a2).sum(1 if axis == 0 else 0)
        order = sorted(range(lo, hi), key=lambda i: (run[i] + 3 * mkc[i], abs(i - (lo + hi) / 2)))
        got = []
        for i in order:
            if len(got) == n: break
            if all(abs(i - g) > 2 for g in got): got.append(i)
        return sorted(got)
    rows = pick(a, extra_y, 0); cols = pick(a, extra_x, 1)
    ri = sorted(list(range(64)) + rows); ci = sorted(list(range(64)) + cols)
    big = a[ri][:, ci]
    o = op(big); ys, xs = np.where(o)
    out = np.zeros((64, 64, 4), int); h, w = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    oy, ox = 63 - 2 - h + 1 if h <= 62 else 0, (64 - w) // 2
    out[oy:oy + h, ox:ox + w] = big[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return out

AMBER = (255, 184, 40, 255); SPARKW = (255, 246, 214, 255)
def crack(a, pts):
    """a zigzag crack: ink along PTS, the lit edge one cell above-left of it, only over the shell"""
    o = op(a); L = lum(a); mk = is_mark(a)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for k in range(n + 1):
            x = round(x0 + (x1 - x0) * k / n); y = round(y0 + (y1 - y0) * k / n)
            if o[y, x] and not mk[y, x]:
                a[y, x] = INK
                if o[y, x + 1] and not mk[y, x + 1] and L[y, x + 1] >= 60: a[y, x + 1] = (70, 72, 84, 255)
                if o[y - 1, x - 1] and L[y - 1, x - 1] >= 60 and not mk[y - 1, x - 1] and (y - 1, x - 1) not in pts:
                    a[y - 1, x - 1] = (236, 238, 244, 255)

BOLT = [" #   ", "#A#  ", " #A# ", "#AWA#", " #A# ", "  #A#", "   # "]
def spark(a, x0, y0, flip=False):
    rows = [r[::-1] for r in BOLT] if flip else BOLT
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            y, x = y0 + dy, x0 + dx
            if ch == " " or not (0 <= y < 64 and 0 <= x < 64): continue
            if ch == "#" and a[y, x, 3] > 127: continue
            a[y, x] = {"#": INK, "A": AMBER, "W": SPARKW}[ch]

def breaker():
    a = widen(built("breaker", "front"), 10, 8)
    ys, xs = np.where(op(a)); print("breaker front box", xs.min(), xs.max(), ys.min(), ys.max())
    t, l, r = ys.min(), xs.min(), xs.max()
    crack(a, [(l + 12, t + 3), (l + 15, t + 7), (l + 13, t + 10), (l + 17, t + 14), (l + 15, t + 17)])
    crack(a, [(r - 10, t + 2), (r - 13, t + 6), (r - 11, t + 9), (r - 14, t + 12)])
    crack(a, [(l + 4, t + 24), (l + 7, t + 26), (l + 6, t + 29)])
    spark(a, l - 1, t - 1); spark(a, r - 4, t - 1, flip=True); spark(a, l - 3, t + 30); spark(a, r - 1, t + 26, flip=True)
    save(a, "breaker", "front")
    b = widen(built("breaker", "back"), 10, 8)
    ys, xs = np.where(op(b)); t, l, r = ys.min(), xs.min(), xs.max()
    crack(b, [(l + 14, t + 2), (l + 17, t + 6), (l + 15, t + 9), (l + 19, t + 13), (l + 17, t + 17)])
    crack(b, [(r - 9, t + 3), (r - 12, t + 7), (r - 10, t + 11)])
    spark(b, l - 1, t + 2); spark(b, r - 4, t, flip=True)
    save(b, "breaker", "back")

# ---------------------------------------------------------------------------------------------------- CIRCULAR
def circular():
    a = built("circular", "front"); out = np.zeros_like(a)
    #  the long legs, kept (orig rows 4..28) and set down 4 rows
    D = 4
    out[4 + D:29 + D, 25:41] = a[4:29, 25:41]
    #  the head and the torso (orig rows 29..50, the small legs below left off), turned upside down beneath them
    blk = a[29:51, 25:41][::-1]
    for y in range(blk.shape[0]):
        for x in range(blk.shape[1]):
            if blk[y, x, 3] > 127: out[29 + D + y, 25 + x] = blk[y, x]
    #  the arms turned down, hands on the ground either side of the head
    ground = 29 + D + blk.shape[0] - 1
    for xs, sh in ((slice(0, 25), 0), (slice(41, 64), -2)):          # the right arm two in, to meet the shoulder
        arm = a[:, xs][::-1]; ys = np.where(op(arm).any(1))[0]
        dy = ground - ys.max(); x0 = xs.start + sh
        for y in ys:
            for x in range(arm.shape[1]):
                if arm[y, x, 3] > 127 and out[y + dy, x0 + x, 3] <= 127: out[y + dy, x0 + x] = arm[y, x]
    #  feet on the top of the legs, turned out, so the legs read as legs
    ys = np.where(op(out).any(1))[0]; top = ys.min()
    feet = [mask_of(lambda d, s: (d.ellipse([22.5 * s, (top - 1.0) * s, 29.5 * s, (top + 3.0) * s], fill=255))),
            mask_of(lambda d, s: (d.ellipse([35.5 * s, (top - 1.0) * s, 42.5 * s, (top + 3.0) * s], fill=255)))]
    base = body_grey(out, (25, top + 4, 41, top + 20)); L = np.array(base[:3])
    ramp = (base, tuple(np.minimum(255, L + 22)) + (255,), base, tuple((L * 0.68).astype(int)) + (255,))
    for f in feet: paint(out, f, ramp, (out[..., 3] <= 127) | f)
    outline(out); save(out, "circular", "front")
    b = out.copy(); print("circular face cells", hb.features_off(b, (26, ground - 12, 40, ground)))
    save(b[:, ::-1].copy(), "circular", "back")
    return ground

# ---------------------------------------------------------------------------------------------------- BOOTSTRAP
def bootstrap():
    a = built("bootstrap", "front")[:, ::-1].copy(); o = op(a); L = lum(a); mk = is_mark(a)   # mirrored first: boxes are the back's
    sat = a[..., :3].max(-1) - a[..., :3].min(-1)
    #  the beak bands and eye colours: every saturated cell that is not a streak marker
    pool = a[o & (L >= 200) & (sat < 30)]; fill = tuple(np.median(pool, 0).astype(int)); k = 0
    for y, x in zip(*np.where(o & (sat >= 50) & ~mk)): a[y, x] = fill; k += 1
    #  the eyes: every dark cell inside each egg's face box (front coordinates), clear of the eggs' outlines
    L = lum(a)
    for x0, y0, x1, y1 in ((27, 17, 40, 24), (42, 27, 55, 34), (12, 27, 24, 34), (27, 37, 40, 43)):
        for y in range(y0, y1):
            for x in range(x0, x1):
                if mk[y, x] or not all(o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): continue
                if L[y, x] < 120: a[y, x] = fill; k += 1
    print("bootstrap face cells", k)
    save(a, "bootstrap", "back")

def icons():
    import icon3
    P = json.load(open(F + "/picks.json"))
    for n in ICONS:
        #  from the front's largest piece only: ARCHIVER's sparkles and BREAKER's sparks would shrink the bust
        a = rgba(f"{H}/{n}_front.png"); o = op(a); lab = np.zeros((64, 64), int); k = 0; sizes = {}
        for y, x in zip(*np.where(o)):
            if lab[y, x]: continue
            k += 1; st = [(y, x)]; lab[y, x] = k; c = 0
            while st:
                p = st.pop(); c += 1
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        q = (p[0] + dy, p[1] + dx)
                        if 0 <= q[0] < 64 and 0 <= q[1] < 64 and o[q] and not lab[q]: lab[q] = k; st.append(q)
            sizes[k] = c
        a[lab != max(sizes, key=sizes.get)] = 0
        src = f"{H}/{n}_front_iconsrc.png"; Image.fromarray(a.astype(np.uint8), "RGBA").save(src)
        P[n]["measured"]["icon3"] = icon3.make(n, P[n]["type"], src, f"{H}/{n}_icon.png"); os.remove(src)
        print(n, P[n]["measured"]["icon3"]["icon_palette"], P[n]["measured"]["icon3"]["size"])
    tmp = F + "/picks.json.tmp"; json.dump(P, open(tmp, "w"), indent=1); os.replace(tmp, F + "/picks.json")

def install():
    for f in sorted(os.listdir(H)):
        shutil.copyfile(f"{H}/{f}", f"{GD}/{f}"); print("h/fu/%s -> gfx/daemons/%s" % (f, f))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "draw"
    if cmd == "draw":
        os.makedirs(H, exist_ok=True)
        acquire(); axiomkick(); archiver(); breaker(); circular(); bootstrap()
        for n in NAMES:
            for k in ("front", "back"):
                p = f"{H}/{n}_{k}.png"
                if not os.path.exists(p): continue
                a = rgba(p); s = sanitize(a)
                if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    else:
        {"icons": icons, "install": install}[cmd]()

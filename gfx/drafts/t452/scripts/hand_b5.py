"""T-452 batch 5, by hand (the user via the coordinator, 2026-10-27: build batch 5; BOOTSTRAP six eggs, ENSEMBLE several
heads, ACQUIRE one oversized claw, AXIOMKICK a high kick -- all four as their INDEX entries say). hand4.py's helpers.

    hand_b5.py      writes T/h/hand/<name>_{front,back,icon}.png (from h/clean and h/reduced)

FUSE, BREAKER  the band round the middle: every draft wore it away. A four-row band (outline, light, mid, outline) across
               the body's interior, below the streaks, ending at the outline.
BOOTSTRAP      six eggs: the draft drew four. The left and right eggs copied down and out, BEHIND the others -- six.
BUSYWAIT       the pendulum: the clean took the string and bob off the hand. A string down from the paw, a round bob.
BACKS          ARCHIVER, COLDVAULT, BUSYWAIT: the drafts from today's back kept a face; each back is its front MIRRORED
               with the face painted out in the body's own grey (hand4's rule).
GROUNDS        baked grounds off the CLEAN grids by hand3's flood (ug), listed in GROUNDS.
SANITIZE       hand3's: a drawn colour within reach of a streak marker darkened (small patch) or greyed (large)."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hand4 as h4
R = "/Users/christopherhicks/Projects/DAEMONS"; F = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452") + "/h"; H = F + "/hand"
h4.F, h4.H = F, H
from hand4 import load, save, load_any, ug, sanitize, outline, stamp, paint_out, body_grey, op, lum, is_mark, INK
NAMES = ["heatsink", "archiver", "deadletter", "landfill", "capsule", "coldvault", "respawn", "hauntproc", "lull", "busywait",
         "acquire", "lockup", "fuse", "breaker", "bootstrap", "ensemble", "artefact", "corefile", "axiomkick", "rebuttal",
         "premise", "circular"]
LIGHT = (222, 222, 228, 255); MID = (150, 150, 160, 255)

def band(n, rows):
    """outline / light / mid / outline across every interior cell of ROWS (not the outline, not a marker)"""
    a = load_any(n, "front"); o = op(a); L = lum(a); mk = is_mark(a); k = 0
    for i, y in enumerate(range(*rows)):
        c = (INK, LIGHT, MID, INK)[min(i, 3)]
        for x in range(64):
            if o[y, x] and L[y, x] >= 60 and not mk[y, x]: a[y, x] = c; k += 1
    save(a, n, "front"); print(n, "band cells", k)

def copy_behind(a, box, dy, dx):
    x0, y0, x1, y1 = box; src = a.copy(); k = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if src[y, x, 3] <= 127 or is_mark(src[y:y + 1, x:x + 1])[0, 0]: continue
            p, q = y + dy, x + dx
            if 0 <= p < 64 and 0 <= q < 64 and a[p, q, 3] <= 127: a[p, q] = src[y, x]; k += 1
    return k

def bootstrap():
    a = load_any("bootstrap", "front")
    k = copy_behind(a, (9, 22, 24, 43), 13, -3) + copy_behind(a, (40, 22, 55, 43), 13, 3)
    outline(a, (30, 64)); save(a, "bootstrap", "front"); print("bootstrap egg cells", k)

BOB = (150, 30, 44, 255)
def busywait():
    a = load_any("busywait", "front")
    for y in range(37, 47): a[y, 51] = INK                          # the string, down from the paw
    stamp(a, 48, 46, [" ### ", "#BBB#", "#BBB#", "#BBB#", " ### "], {"#": INK, "B": BOB})
    save(a, "busywait", "front")

def mirrored(n, face, src=None):
    a = load_any(n, "front") if src is None else src
    fill = body_grey(a, face); print(n, "face cells", paint_out(a, face, fill))
    save(a[:, ::-1].copy(), n, "back")

def features_off(a, box):
    """the face's FEATURES off, the rest of the drawing kept (a flat fill over a textured shell read as a patch): every
    dark or saturated interior cell of BOX that is not a marker -> the median of the box's light, unsaturated cells"""
    x0, y0, x1, y1 = box; o = op(a); L = lum(a); mk = is_mark(a)
    sat = a[..., :3].max(-1) - a[..., :3].min(-1)
    reg = a[y0:y1, x0:x1].reshape(-1, 4); rl = lum(reg[None])[0]; rs = reg[:, :3].max(-1) - reg[:, :3].min(-1)
    pool = reg[(reg[:, 3] > 127) & (rl >= 150) & (rs < 40)]
    fill = np.median(pool, 0).astype(int) if len(pool) else np.array([200, 200, 206, 255]); n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not o[y, x] or mk[y, x]: continue
            if any(not o[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)): continue
            if L[y, x] < 90 or sat[y, x] >= 60: a[y, x] = fill; n += 1
    return n

def mirrored_features(n, face):
    a = load_any(n, "front"); print(n, "feature cells", features_off(a, face)); save(a[:, ::-1].copy(), n, "back")

PAPER = (236, 232, 220, 255)
def deadletter():
    """the envelope, stuck in the top of its goo (every draft lost it; the user: hand-draw it)"""
    a = load_any("deadletter", "front")
    stamp(a, 40, 8, ["#########", "#PPPPPPP#", "#P#PPP#P#", "#PP#P#PP#", "#PPP#PPP#", "#########"], {"#": INK, "P": PAPER})
    save(a, "deadletter", "front")

def cut(a, cols, rows):
    """two columns cleared through an arm, and the cut ends outlined: a hand that floats free"""
    for y in range(*rows):
        for x in cols: a[y, x] = (0, 0, 0, 0)
    o = op(a)
    for y in range(*rows):
        for x in (cols[0] - 1, cols[-1] + 1):
            if o[y, x] and lum(a[y:y + 1, x:x + 1])[0, 0] >= 60 and not is_mark(a[y:y + 1, x:x + 1])[0, 0]: a[y, x] = INK

def respawn():
    a = load_any("respawn", "front"); cut(a, (16, 17), (22, 46)); cut(a, (44, 45), (22, 46)); save(a, "respawn", "front")
    b = load_any("respawn", "back"); cut(b, (14, 15), (24, 44)); cut(b, (49, 50), (24, 44)); save(b, "respawn", "back")

def paste_scaled(a, box, scale, at, front=True):
    """BOX of A scaled by SCALE (nearest) and laid with its top-left at AT, over (FRONT) or behind what is there"""
    x0, y0, x1, y1 = box
    im = Image.fromarray(a[y0:y1, x0:x1].astype(np.uint8), "RGBA")
    im = im.resize((max(1, round((x1 - x0) * scale)), max(1, round((y1 - y0) * scale))), Image.NEAREST)
    s = np.array(im).astype(int); k = 0
    for y in range(s.shape[0]):
        for x in range(s.shape[1]):
            p, q = at[1] + y, at[0] + x
            if not (0 <= p < 64 and 0 <= q < 64) or s[y, x, 3] <= 127 or is_mark(s[y:y + 1, x:x + 1])[0, 0]: continue
            if front or a[p, q, 3] <= 127: a[p, q] = s[y, x]; k += 1
    return k

CLAW = ["   #####       ",
        "  #LLLLL#  ##  ",
        " #LLLLLLL##LL# ",
        "#LLLMMMLL#LLL# ",
        "#LLMMMMML#LLM# ",
        "#LLMMMMMLLLLM# ",
        "#LLMMMMMMMMMM# ",
        "#LLMMMMMMMMMM# ",
        " #LMMMMMMMMML# ",
        " #LLMMMMMMMML# ",
        "  #LLMMMMMML#  ",
        "   ##LMMMM##   ",
        "     #LMML#    ",
        "     #LMML#    ",
        "     #LMML#    ",
        "     #LMML#    ",
        "     #LMML#    "]
def acquire():
    """one claw twice the size of the other, raised (the entry: it leads with the big claw, lopsided): the small right
    claw's tip cleared, a big open pincer drawn in its place on a stalk down to the shell"""
    a = load_any("acquire", "front")
    for y in range(10, 19):
        for x in range(38, 52): a[y, x] = (0, 0, 0, 0)
    stamp(a, 36, 2, CLAW, {"#": INK, "L": LIGHT, "M": MID}); save(a, "acquire", "front")

def ensemble():
    """two small heads in the leaf crown beside the big one (the entry: several heads, one body)"""
    a = load_any("ensemble", "front"); src = a.copy()
    k = paste_scaled(a, (19, 19, 46, 45), 0.42, (13, 4)) + paste_scaled(a, (19, 19, 46, 45), 0.42, (40, 4))
    outline(a, (0, 30)); save(a, "ensemble", "front"); print("ensemble head cells", k)

def thick_line(a, p0, p1, r_in, r_out, fill, behind=True):
    """a limb: discs of R_OUT in ink, then R_IN in FILL, stepped from P0 to P1 (only into empty cells if BEHIND)"""
    (x0, y0), (x1, y1) = p0, p1; n = int(max(abs(x1 - x0), abs(y1 - y0))) * 2 + 1
    pts = [(x0 + (x1 - x0) * i / (n - 1), y0 + (y1 - y0) * i / (n - 1)) for i in range(n)]
    empty = a[..., 3] <= 127
    for r, c in ((r_out, INK), (r_in, fill)):
        for cx, cy in pts:
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if 0 <= y < 64 and 0 <= x < 64 and (x - cx) ** 2 + (y - cy) ** 2 <= r * r and (empty[y, x] or not behind):
                        a[y, x] = c

def axiomkick():
    """the high kick (the user): the right leg off the ground, a long leg kicked up past its head, behind the arm"""
    a = load_any("axiomkick", "front"); fill = body_grey(a, (24, 6, 40, 14))
    for y in range(42, 52):
        for x in range(36, 48):
            if not is_mark(a[y:y + 1, x:x + 1])[0, 0]: a[y, x] = (0, 0, 0, 0)
    outline(a, (36, 52))
    thick_line(a, (40, 42), (54, 8), 2.2, 3.3, fill, behind=False)
    thick_line(a, (53, 8), (57, 3), 2.8, 3.9, fill, behind=False)       # the foot
    save(a, "axiomkick", "front")

GROUNDS = (("corefile", "front", 0.88, dict(dark=True)), ("corefile", "back", 0.88, dict(minL=110)),
           ("landfill", "front", 0.90, dict(minL=110)), ("lull", "back", 0.85, dict(minL=110)),
           ("lockup", "front", 0.85, dict(minL=110)), ("rebuttal", "front", 0.92, dict(minL=110)),
           ("premise", "front", 0.88, dict(minL=110)), ("ensemble", "front", 0.92, dict(minL=110)), ("ensemble", "back", 0.93, dict(dark=True)))

def grounds():
    for n, k, lo, kw in GROUNDS:
        a = load_any(n, k); print(n, k, "ground", ug(a, lo, **kw)); save(a, n, k)

if __name__ == "__main__":
    os.makedirs(H, exist_ok=True)
    for f in os.listdir(H): os.remove(f"{H}/{f}")
    grounds()
    band("fuse", (42, 46)); band("breaker", (42, 46))
    bootstrap(); busywait(); deadletter(); respawn(); acquire(); ensemble(); axiomkick()
    mirrored("archiver", (12, 18, 38, 34))
    mirrored_features("coldvault", (16, 26, 48, 44))
    mirrored_features("busywait", (22, 17, 52, 37))
    mirrored_features("artefact", (18, 14, 46, 40))
    for n in NAMES:
        for k in ("front", "back"):
            if not os.path.exists(f"{F}/clean/{n}_{k}.png"): continue
            a = load_any(n, k); s = sanitize(a)
            if s: save(a, n, k); print(n, k, "near-marker cells fixed:", s)
    print("written", sorted(os.listdir(H)))

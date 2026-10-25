"""T-452 round two: a draft -> cleaned 64-grid -> accents capped -> the type's ramp -> 4bpp 64x64.

    reduce2.py NAME TYPE FRONT_DRAFT [--back=BACK_DRAFT] [--icon=ICON_DRAFT] [--cap=0.15]
               [--box-front=x0,y0,x1,y1] [--box-back=...] [--dir=b]

Writes only under gfx/drafts/t452/b/ (clean/, reduced/) and prints one JSON line of measurements.

THE ACCENT CAP (the user, 2026-10-24: "about 15% of the creature's pixels"). An accent is what gbasprite.place_rich
keeps in its own colour: a pixel of the creature, not a streak marker, saturated >= SAT_ACCENT. Measured on the
cleaned grid before reduction, and again on the reduced grid (palette 6..10 over every drawn pixel). Over the cap,
the accent pixels are split into connected patches and the SMALLEST patches are kept first -- an eye, a nose, a wax
seal -- until the next would pass the cap; every larger patch is sent back to grey at its own brightness, so
place_rich draws it in the type's ramp. A big saturated area is a colour the model chose for the body, and the
body's colour is the type's (invariant 5).

STREAKS ON THE BODY (point 5). cleandraft.py's automatic place starts at half the figure's height, which on a chibi
is the chin. Unless a box is given, the box here is the lower body: from 55% to 92% of the subject's height, and
across the median widest run of body in those rows -- below the head however big it is.

THE ICON (point 3) is drawn on its own as a bust, cleaned, put in the type's ramp, then reduced to 24px by
footprint vote (outline wins a pixel at 30% of it, so the line survives), given an outer outline, and mapped onto
whichever of the three shared icon palettes fits best with value weighted twice hue."""
import sys, os, json, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gbs
R = "/Users/christopherhicks/Projects/DAEMONS"; PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
opt = {a.split("=", 1)[0][2:]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
#  --dir=c: batch.py's roll-out batches (round two's own drafts stay in b/, the default)
B = os.path.join(os.environ.get("T452_ROOT", os.path.join(R, "gfx/drafts/t452")), opt.get("dir", "b"))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
name, typ, front = args[:3]
CAP = float(opt.get("cap", 0.15))
os.makedirs(B + "/clean", exist_ok=True); os.makedirs(B + "/reduced", exist_ok=True)
rep = {"name": name, "type": typ, "front": front}

def lum(a): return (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000

def clean(src, out, box=None, streaks=True):
    cmd = [PY, os.path.join(R, "tools/cleandraft.py"), os.path.join(B, src), out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stdout + r.stderr)
    if not streaks: return None
    if box is None:
        a = np.asarray(Image.open(out)).astype(int)
        subj = a[..., 3] > 127
        body = subj & (lum(a[..., :3]) >= 48)
        ys = np.where(subj.any(1))[0]; y0, y1 = ys.min(), ys.max(); h = y1 - y0 + 1
        ty0, ty1 = y0 + int(h * 0.55), y0 + int(h * 0.92)
        st, en = [], []
        for y in range(ty0, ty1 + 1):
            xs = np.where(body[y])[0]
            if len(xs) < 5: continue
            runs, s = [], xs[0]
            for p, q in zip(xs, xs[1:]):
                if q != p + 1: runs.append((s, p)); s = q
            runs.append((s, xs[-1]))
            r0, r1 = max(runs, key=lambda r: r[1] - r[0]); st.append(r0); en.append(r1)
        box = (int(np.median(st)) + 1, ty0, int(np.median(en)) - 1, ty1)
    b = ",".join(str(v) for v in box)
    r = subprocess.run(cmd + ["--streaks", "--streak-box=" + b], capture_output=True, text=True)
    if r.returncode:
        #  A torso too broken up for that box (ROVERCUB's: legs and a chest panel, dark seams between): search the
        #  lower body -- every box starting at or below half the figure's height -- for the one whose four
        #  strokes each find the most body.
        sys.path.insert(0, os.path.join(R, "tools")); argv = sys.argv; sys.argv = ["x"]
        import cleandraft as cd; sys.argv = argv
        g = cd.sample(os.path.join(B, src)); s, _, _ = cd.clear_background(g)
        ys = np.where(s.any(1))[0]; xs = np.where(s.any(0))[0]; y0, y1 = ys.min(), ys.max(); h = y1 - y0 + 1
        best = None
        for by0 in range(y0 + h // 2, y0 + int(h * 0.75), 2):
            for by1 in range(by0 + 8, y1 + 1, 2):
                for bx0 in range(xs.min(), xs.max() - 10, 2):
                    for bx1 in range(bx0 + 10, xs.max() + 1, 2):
                        try: p = cd.paint_streaks(g.copy(), s.copy(), (bx0, by0, bx1, by1))
                        except ValueError: continue
                        if all(p) and (best is None or min(p) > best[0]): best = (min(p), (bx0, by0, bx1, by1))
        if best:
            b = ",".join(str(v) for v in best[1])
            r = subprocess.run(cmd + ["--streaks", "--streak-box=" + b], capture_output=True, text=True)
    if r.returncode:
        subprocess.run(cmd, capture_output=True, text=True)
        return {"box": b, "painted": "FAILED, no streaks"}
    return {"box": b, "painted": [l for l in r.stdout.splitlines() if "streak pixels" in l][0].split(":")[1].strip()}

def accent_mask(a, subj):
    rgb = a[..., :3]
    sat = rgb.max(2) - rgb.min(2)
    st = np.zeros(subj.shape, bool)
    for mk in gbs.STREAK_MARKERS:
        st |= subj & (np.abs(rgb - np.array(mk)).max(2) <= gbs.STREAK_TOLERANCE)
    return subj & (sat >= gbs.SAT_ACCENT) & ~st, st

def cap(path):
    a = np.asarray(Image.open(path)).astype(int).copy()
    subj = a[..., 3] > 127
    acc, st = accent_mask(a, subj)
    n = int(subj.sum()); before = acc.sum() / n
    kept = acc.copy(); greyed = 0
    if before > CAP:
        lab = np.zeros(acc.shape, int); k = 0; sizes = []
        for y, x in zip(*np.where(acc)):
            if lab[y, x]: continue
            k += 1; stack = [(y, x)]; lab[y, x] = k; c = 0
            while stack:
                yy, xx = stack.pop(); c += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    p, q = yy + dy, xx + dx
                    if 0 <= p < acc.shape[0] and 0 <= q < acc.shape[1] and acc[p, q] and not lab[p, q]:
                        lab[p, q] = k; stack.append((p, q))
            sizes.append((c, k))
        budget = CAP * n; used = 0; keep = set()
        for c, k in sorted(sizes):
            if used + c <= budget: keep.add(k); used += c
        kept = acc & np.isin(lab, list(keep))
        drop = acc & ~kept
        L = lum(a[..., :3])
        for ch in range(3): a[..., ch][drop] = L[drop]
        greyed = int(drop.sum())
        Image.fromarray(a.astype(np.uint8), "RGBA").save(path)
    return {"accent_clean_before": round(before * 100, 1), "accent_clean_after": round(kept.sum() / n * 100, 1),
            "greyed_px": greyed, "streak_px": int(st.sum()), "creature_px": n}

def measure(grid):
    g = np.array(grid); drawn = g > 0
    return round(((g >= 6) & (g <= 10)).sum() / drawn.sum() * 100, 1)

pal = None; grid_f = None
for kind, src in (("front", front), ("back", opt.get("back"))):
    if not src: continue
    out = f"{B}/clean/{name}_{kind}.png"
    bx = opt.get("box-" + kind); bx = tuple(int(v) for v in bx.split(",")) if bx else None
    rep[kind + "_streaks"] = clean(src, out, bx)
    rep[kind + "_cap"] = cap(out)
    grid, p = gbs.place_rich(out, gbs.TYPE_COLOR[typ], shared=pal if kind == "back" else None)
    if kind == "front": pal = p; grid_f = grid
    gbs.write_png4(f"{B}/reduced/{name}_{kind}.png", grid, p)
    rep[kind + "_accent_pct"] = measure(grid); rep[kind + "_colours"] = len(set(c for r in grid for c in r))
with open(f"{B}/reduced/{name}_normal.pal", "w", newline="") as f:
    f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in (pal + [(0, 0, 0)] * 16)[:16]))

#  The derived icon, the way gbasprite.py makes it today -- kept for the comparison sheet.
ic, info = gbs.derive_icon(grid_f, pal)
gbs.write_png4(f"{B}/reduced/{name}_icon_derived.png", ic, gbs.icon_palettes()[info[0]], 32, 64)

if opt.get("icon"):
    out = f"{B}/clean/{name}_icon.png"
    clean(opt["icon"], out, streaks=False)
    rep["icon_cap"] = cap(out)
    g, p = gbs.place_rich(out, gbs.TYPE_COLOR[typ])
    g = np.array(g); ys, xs = np.where(g > 0)
    g = g[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    T = 22                                   # inner size; +1px outline each side = 24
    sc = T / max(g.shape); h, w = max(1, round(g.shape[0] * sc)), max(1, round(g.shape[1] * sc))
    small = np.zeros((h, w), int); INK = 5
    for y in range(h):
        for x in range(w):
            fp = g[int(y / sc):max(int(y / sc) + 1, int((y + 1) / sc)), int(x / sc):max(int(x / sc) + 1, int((x + 1) / sc))].ravel()
            if (fp == 0).mean() > 0.5: continue
            o = fp[fp > 0]
            if (o == INK).mean() >= 0.30: small[y, x] = INK; continue
            o = o[o != INK]
            small[y, x] = np.bincount(o).argmax() if len(o) else INK
    big = np.zeros((h + 2, w + 2), int); big[1:-1, 1:-1] = small
    op = big > 0
    ring = ~op & (np.roll(op, 1, 0) | np.roll(op, -1, 0) | np.roll(op, 1, 1) | np.roll(op, -1, 1))
    big[ring] = INK
    #  map the type palette onto each icon palette; value counts twice
    def L(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    used = sorted(set(big.ravel()) - {0}); best = None
    for pi, ipal in enumerate(gbs.icon_palettes()):
        m, err = {}, 0
        for u in used:
            c = p[u]
            if u == INK: m[u] = 15; continue      # 65,65,65: the icons' own outline
            d = [(sum((c[k] - e[k]) ** 2 for k in range(3)) + 2 * (L(c) - L(e)) ** 2, j) for j, e in enumerate(ipal) if j]
            dd, j = min(d); m[u] = j; err += dd ** 0.5 * (big == u).sum()
        if best is None or err < best[0]: best = (err, pi, m)
    err, pi, m = best
    out_g = [[0] * 32 for _ in range(64)]
    oy, ox = 30 - big.shape[0], (32 - big.shape[1]) // 2
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            v = m.get(big[y, x], 0) if big[y, x] else 0
            out_g[oy + y][ox + x] = v
            if 32 + oy + y + 1 < 64: out_g[32 + oy + y + 1][ox + x] = v      # frame 2: the bob, one px down
    gbs.write_png4(f"{B}/reduced/{name}_icon.png", out_g, gbs.icon_palettes()[pi], 32, 64)
    rep["icon_palette"] = pi; rep["icon_size"] = list(big.shape[::-1])
print(json.dumps(rep))

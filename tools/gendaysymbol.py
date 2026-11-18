#!/usr/bin/env python3
"""Draw the seven day symbols (T-531, bible 9.21) for the companion's DREAMS.

    ~/.pyenv/shims/python3 tools/gendaysymbol.py [--write] [--sheet OUT.png]

Each day of the week has one wordless symbol, ring and horizon: the day's centre as a ring in ink, its petal count as
ticks (Root 4, Sacral 6, Solar plexus 10, Heart 12, Throat 16, Third eye 2, Crown a full second ring); a level line
through it; the virtue's mark above the line in the day's colour; and the same mark reflected below, faint and dashed,
its shadow -- a part of the same shape waiting to be lit, never an enemy. The geometry is the drawing the user approved
on 2026-11-08 ("Keep all seven"), copied path for path; the colours are the companion's week.json, which is the
CHECKPOINT's trim. No words in the symbol.

Writes companion/server/data/art/daysymbol/<sun..sat>_<light|dark>.png -- the ring's ink dark for a light page and
light for a dark one; the day's colour the same on both. Without --write it reports what it would write.
"""
import argparse, json, math, os, re, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = os.path.join(ROOT, "companion")
OUT = os.path.join(COMP, "server", "data", "art", "daysymbol")
WEEK = os.path.join(COMP, "server", "data", "week.json")

# The approved drawing (2026-11-08), Sunday first: the day, its petals (0 = Crown, a full second ring), the virtue's mark.
MARKS = [
    ("sun", 4,  "M-12 -3 V-10 A12 12 0 0 1 12 -10 V-3 Z"),                                   # CHASTITY: a closed dome
    ("mon", 6,  "M-15 -17 H15 M-5 -3 L0 -15 L5 -3 Z"),                                        # TEMPERANCE: a beam on its point
    ("tue", 10, "M-13 -21 Q0 4 13 -21"),                                                      # CHARITY: a bowl held open
    ("wed", 12, "M-13 -3 H-6 V-9 H1 V-15 H8 V-21 H13"),                                       # DILIGENCE: a climb
    ("thu", 16, "M0 -3 C-3 -10 -12 -12 -12 -21 M0 -3 C3 -10 12 -12 12 -21"),                  # FORGIVENESS: a knot opening up
    ("fri", 2,  "M-14 -9 A14 14 0 0 1 14 -9 M-2.5 -7 a2.5 2.5 0 1 0 5 0 a2.5 2.5 0 1 0 -5 0"),  # KINDNESS: an arc over a point
    ("sat", 0,  "M0 -3 V-15 Q0 -22 -8 -19"),                                                  # HUMILITY: a stem bowing
]
R = 30                       # the ring
HALF = 42                    # the drawing's half-width in its own units (the Crown's ring at 36, Third eye's ticks at 40)
SCALE = 3                    # output pixels per unit: 252 px square, shown at 56
SS = 4                       # supersampling
INK = {"light": (28, 27, 26), "dark": (237, 231, 218)}


def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def arc_points(x1, y1, rx, ry, phi, fa, fs, x2, y2, n=40):
    """SVG's endpoint arc to points (circular arcs only, as these are)."""
    r = rx
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    d2 = dx * dx + dy * dy
    if d2 > r * r: r = math.sqrt(d2)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    q = math.sqrt(max(0.0, r * r - d2) / d2) if d2 else 0
    sign = -1 if fa == fs else 1
    cx, cy = mx + sign * q * (-dy) * -1, my + sign * q * dx * -1
    # pick the centre that gives the sweep asked for
    for c in ((mx + q * dy, my - q * dx), (mx - q * dy, my + q * dx)):
        a1 = math.atan2(y1 - c[1], x1 - c[0]); a2 = math.atan2(y2 - c[1], x2 - c[0])
        da = a2 - a1
        if fs and da < 0: da += 2 * math.pi
        if not fs and da > 0: da -= 2 * math.pi
        if (abs(da) > math.pi) == bool(fa) or abs(abs(da) - math.pi) < 1e-6:
            return [(c[0] + r * math.cos(a1 + da * t / n), c[1] + r * math.sin(a1 + da * t / n)) for t in range(1, n + 1)]
    return [(x2, y2)]


def subpaths(d):
    """A path's subpaths as point lists, each with whether it closed."""
    toks = re.findall(r"[MmHhVvLlZzQqCcAa]|-?\d*\.?\d+", d)
    out, cur, x, y, i, cmd = [], None, 0.0, 0.0, 0, None
    num = lambda: float(toks[i])
    while i < len(toks):
        t = toks[i]
        if re.match(r"[A-Za-z]", t): cmd = t; i += 1
        if cmd in "Zz":
            if cur: out.append((cur, True)); x, y = cur[0]; cur = None
            continue
        rel = cmd.islower(); C = cmd.upper()
        if C == "M":
            nx, ny = float(toks[i]), float(toks[i + 1]); i += 2
            if rel: nx, ny = x + nx, y + ny
            if cur: out.append((cur, False))
            x, y = nx, ny; cur = [(x, y)]; cmd = "l" if rel else "L"
        elif C in "HV":
            v = float(toks[i]); i += 1
            if C == "H": x = x + v if rel else v
            else: y = y + v if rel else v
            cur.append((x, y))
        elif C == "L":
            nx, ny = float(toks[i]), float(toks[i + 1]); i += 2
            x, y = (x + nx, y + ny) if rel else (nx, ny); cur.append((x, y))
        elif C == "Q":
            v = [float(toks[i + k]) for k in range(4)]; i += 4
            if rel: v = [v[0] + x, v[1] + y, v[2] + x, v[3] + y]
            for k in range(1, 31):
                t = k / 30
                cur.append(((1 - t) ** 2 * x + 2 * (1 - t) * t * v[0] + t * t * v[2],
                            (1 - t) ** 2 * y + 2 * (1 - t) * t * v[1] + t * t * v[3]))
            x, y = v[2], v[3]
        elif C == "C":
            v = [float(toks[i + k]) for k in range(6)]; i += 6
            if rel: v = [v[0] + x, v[1] + y, v[2] + x, v[3] + y, v[4] + x, v[5] + y]
            for k in range(1, 41):
                t = k / 40; u = 1 - t
                cur.append((u ** 3 * x + 3 * u * u * t * v[0] + 3 * u * t * t * v[2] + t ** 3 * v[4],
                            u ** 3 * y + 3 * u * u * t * v[1] + 3 * u * t * t * v[3] + t ** 3 * v[5]))
            x, y = v[4], v[5]
        elif C == "A":
            v = [float(toks[i + k]) for k in range(7)]; i += 7
            ex, ey = (x + v[5], y + v[6]) if rel else (v[5], v[6])
            cur += arc_points(x, y, v[0], v[1], v[2], int(v[3]), int(v[4]), ex, ey)
            x, y = ex, ey
    if cur: out.append((cur, False))
    return out


def dashed(pts, on, off):
    """A polyline cut into dashes, `on` drawn and `off` skipped, in the drawing's units."""
    segs, seg, left, drawing = [], [pts[0]], on, True
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay); pos = 0.0
        while L - pos > left:
            pos += left; t = pos / L; p = (ax + (bx - ax) * t, ay + (by - ay) * t)
            if drawing: seg.append(p); segs.append(seg)
            seg = [p]; drawing = not drawing; left = on if drawing else off
        left -= L - pos
        if drawing: seg.append((bx, by))
    if drawing and len(seg) > 1: segs.append(seg)
    return segs


def draw(day_i, colour, ink):
    name, petals, d = MARKS[day_i]
    k = SCALE * SS; size = 2 * HALF * k
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    P = lambda x, y: ((x + HALF) * k, (y + HALF) * k)
    W = lambda w: max(1, round(w * k))

    def layer(alpha):
        return Image.new("RGBA", (size, size), (0, 0, 0, 0)), alpha

    def put(lay, a):
        if a < 1:
            r, g, b, al = lay.split(); al = al.point(lambda v: int(v * a)); lay = Image.merge("RGBA", (r, g, b, al))
        im.alpha_composite(lay)

    def poly(dr, pts, fill, w):
        q = [P(*p) for p in pts]
        dr.line(q, fill=fill, width=W(w), joint="curve")
        for p in (q[0], q[-1]):   # round caps
            rr = W(w) / 2; dr.ellipse((p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr), fill=fill)

    # the ring, its petals, in ink
    lay, _ = layer(1); dr = ImageDraw.Draw(lay)
    for rad in ([R, R + 6] if petals == 0 else [R]):
        c = P(0, 0); rr = rad * k
        dr.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), outline=ink, width=W(1.2))
    for j in range(petals):
        a = j * math.pi if petals == 2 else 2 * math.pi * j / petals - math.pi / 2
        out = R + (10 if petals == 2 else 6)
        poly(dr, [(math.cos(a) * R, math.sin(a) * R), (math.cos(a) * out, math.sin(a) * out)], ink, 2.4 if petals == 2 else 1.6)
    put(lay, 1)
    # the horizon, the day's colour, faint
    lay, _ = layer(1); dr = ImageDraw.Draw(lay); poly(dr, [(-R + 6, 0), (R - 6, 0)], colour, 1); put(lay, 0.6)
    # the shadow: the mark reflected below the line, dashed and faint
    lay, _ = layer(1); dr = ImageDraw.Draw(lay)
    for pts, closed in subpaths(d):
        pts = [(x, -y) for x, y in pts] + ([(pts[0][0], -pts[0][1])] if closed else [])
        for seg in dashed(pts, 3, 3):
            if len(seg) > 1: poly(dr, seg, colour, 2)
    put(lay, 0.45)
    # the virtue's mark above the line, in the day's colour (filled where the approved path closes)
    lay, _ = layer(1); dr = ImageDraw.Draw(lay)
    for pts, closed in subpaths(d):
        if closed: dr.polygon([P(*p) for p in pts], fill=colour)
        poly(dr, pts + ([pts[0]] if closed else []), colour, 2.6)
    put(lay, 1)
    return im.resize((size // SS, size // SS), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--sheet", help="also write a review sheet of all fourteen here")
    a = ap.parse_args()
    days = json.load(open(WEEK))["days"]
    assert [x["day"][:3].lower() for x in days] == [m[0] for m in MARKS], "week.json is not Sunday first"
    imgs = {}
    for i, day in enumerate(days):
        for theme, ink in INK.items():
            imgs[(MARKS[i][0], theme)] = draw(i, hexrgb(day["colour"]) + (255,), ink + (255,))
    changed = []
    for (name, theme), im in imgs.items():
        p = os.path.join(OUT, f"{name}_{theme}.png")
        old = Image.open(p).convert("RGBA").tobytes() if os.path.exists(p) else None
        if old != im.tobytes(): changed.append(p)
    if a.write:
        os.makedirs(OUT, exist_ok=True)
        for (name, theme), im in imgs.items(): im.save(os.path.join(OUT, f"{name}_{theme}.png"), optimize=True)
    for p in changed: print(("wrote " if a.write else "would write ") + os.path.relpath(p, ROOT))
    if a.sheet:
        cell = 2 * HALF * SCALE; sheet = Image.new("RGBA", (cell * 7, cell * 2), (0, 0, 0, 255))
        for i, (name, *_ ) in enumerate(MARKS):
            for r, (theme, bg) in enumerate((("light", (245, 240, 230)), ("dark", (24, 24, 26)))):
                tile = Image.new("RGBA", (cell, cell), bg + (255,)); tile.alpha_composite(imgs[(name, theme)])
                sheet.paste(tile, (i * cell, r * cell))
        sheet.convert("RGB").save(a.sheet); print("sheet", a.sheet)
    if not changed: print("gendaysymbol: nothing to change")
    return 0


if __name__ == "__main__":
    sys.exit(main())

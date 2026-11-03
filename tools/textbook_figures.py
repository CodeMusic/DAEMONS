"""Draw PRINCIPLES OF MIND's six figures as SVG (T-520): python3 tools/textbook_figures.py docs/manual-textbook/diagrams"""
import math, os, sys
OUT = sys.argv[1]
FONT = 'font-family="Gill Sans, Gill Sans MT, Avenir Next, Helvetica Neue, sans-serif"'
INK, SOFT, RULE = "#1b1c20", "#5b5d66", "#cfccc2"

def svg(name, w, h, body, note):
    x0 = -100 if name.endswith("_") else 0
    name = name.rstrip("_")
    open(os.path.join(OUT, name + ".svg"), "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%d 0 %d %d" %s>\n  <!-- PRINCIPLES OF MIND: %s -->\n%s\n</svg>\n'
        % (x0, w - x0, h, FONT, note, body))

def t(x, y, s, size=12, fill=INK, anchor="start", weight="400", extra=""):
    return '<text x="%g" y="%g" font-size="%g" fill="%s" text-anchor="%s" font-weight="%s"%s>%s</text>' % (
        x, y, size, fill, anchor, weight, extra, s)

# 2.1 the spatial cueing paradigm
C = "#b8662a"
def screen(x, y, cue=None, target=None):
    out = ['<rect x="%g" y="%g" width="96" height="56" rx="4" fill="#f3f1ea" stroke="%s" stroke-width="1.4"/>' % (x, y, INK)]
    for bx in (x + 10, x + 62):
        out.append('<rect x="%g" y="%g" width="24" height="24" fill="none" stroke="%s" stroke-width="1.2"/>' % (bx, y + 16, SOFT))
    out.append(t(x + 48, y + 33, "+", 14, INK, "middle"))
    if cue == "L": out.append('<path d="M%g %gh-12m0 0l5 -4m-5 4l5 4" stroke="%s" stroke-width="2" fill="none"/>' % (x + 54, y + 44, C))
    if cue == "R": out.append('<path d="M%g %gh12m0 0l-5 -4m5 4l-5 4" stroke="%s" stroke-width="2" fill="none"/>' % (x + 42, y + 44, C))
    if cue == "N": out.append('<path d="M%g %gh-10m0 0l4 -3m-4 3l4 3M%g %gh10m0 0l-4 -3m4 3l-4 3" stroke="%s" stroke-width="1.6" fill="none"/>' % (x + 46, y + 44, x + 50, y + 44, SOFT))
    if target: out.append('<circle cx="%g" cy="%g" r="6" fill="%s"/>' % ((x + 22) if target == "L" else (x + 74), y + 28, INK))
    return "\n".join(out)
rows = [("valid", "L", "L", 250, "benefit"), ("neutral", "N", "L", 285, ""), ("invalid", "R", "L", 330, "cost")]
b = [t(20, 22, "the cue", 11, SOFT, "start", "600"), t(140, 22, "then the target", 11, SOFT, "start", "600"),
     t(300, 22, "time to respond (illustrative)", 11, SOFT, "start", "600")]
for i, (name, cue, tgt, ms, tag) in enumerate(rows):
    y = 34 + i * 74
    b += [screen(20, y, cue), '<path d="M122 %g h12" stroke="%s" stroke-width="1.4"/>' % (y + 28, SOFT), screen(140, y, None, tgt)]
    w = (ms - 200) * 1.2
    b += ['<rect x="300" y="%g" width="%g" height="22" rx="2" fill="%s" opacity="%s"/>' % (y + 17, w, C, "1" if name != "neutral" else ".45"),
          t(300 + w + 8, y + 33, "%d ms" % ms, 12, INK, "start", "600"),
          t(250, y + 33, name, 12, INK, "end", "600") if False else t(300, y + 12, name + (" cue" ), 11.5, INK, "start", "600")]
    if tag: b.append(t(300 + w + 64, y + 33, tag, 12, C, "start", "700", ' font-style="italic"'))
svg("cueing", 520, 256, "\n".join(b), "Posner's spatial cueing paradigm: valid, neutral and invalid cues")

# 2.3 feature and conjunction search
import random
random.seed(7)
def field(x0, y0, items):
    out = []
    for (cx, cy, ch, col) in items:
        out.append(t(x0 + cx, y0 + cy, ch, 22, col, "middle", "700"))
    return "\n".join(out)
G, R = "#3f7a3a", "#b0352b"
pos = [(30 + (k % 6) * 36 + random.randint(-6, 6), 30 + (k // 6) * 36 + random.randint(-5, 5)) for k in range(24)]
tk = 15
left = [(px, py, "X", R if k == tk else G) for k, (px, py) in enumerate(pos)]
right = [(px, py, "X" if k == tk else ("O" if k % 2 else "X"), R if k == tk else (R if k % 2 else G)) for k, (px, py) in enumerate(pos)]
b = ['<rect x="10" y="10" width="236" height="170" rx="6" fill="#f3f1ea" stroke="%s"/>' % RULE,
     '<rect x="274" y="10" width="236" height="170" rx="6" fill="#f3f1ea" stroke="%s"/>' % RULE,
     field(10, 18, left), field(274, 18, right),
     t(128, 204, "feature search", 13, INK, "middle", "700"), t(128, 221, "the red X differs in colour alone", 11.5, SOFT, "middle"),
     t(392, 204, "conjunction search", 13, INK, "middle", "700"), t(392, 221, "red, and an X: no single feature finds it", 11.5, SOFT, "middle")]
# the two set-size curves
for x0, slope, lab in ((40, 2, "flat: it pops out"), (304, 22, "rising: item by item")):
    b += ['<path d="M%g 312 V244 M%g 312 H%g" stroke="%s" stroke-width="1.2" fill="none"/>' % (x0, x0, x0 + 180, INK),
          '<path d="M%g %g L%g %g" stroke="%s" stroke-width="2.6"/>' % (x0 + 10, 300, x0 + 170, 300 - slope * 2.6, G if slope < 5 else R),
          t(x0 + 90, 328, "number of items", 10.5, SOFT, "middle"), t(x0 - 6, 278, "time", 10.5, SOFT, "end"),
          t(x0 + 176, 300 - slope * 2.6 - 8, lab, 11, INK, "end", "600")]
svg("search", 520, 336, "\n".join(b), "Treisman and Gelade's feature and conjunction search")

# 3.2 Ebbinghaus's forgetting curve (savings, Ebbinghaus 1885)
pts = [(20 / 60, 58.2, "20 min"), (1, 44.2, "1 hour"), (8.8, 35.8, "9 hours"), (24, 33.7, "1 day"), (48, 27.8, "2 days"),
       (144, 25.4, "6 days"), (744, 21.1, "31 days")]
X0, X1, Y0, Y1 = 60, 500, 230, 30
lx = lambda h: X0 + (math.log10(h) - math.log10(0.25)) / (math.log10(1000) - math.log10(0.25)) * (X1 - X0)
ly = lambda v: Y0 - v / 70 * (Y0 - Y1)
b = ['<path d="M%g %g V%g H%g" stroke="%s" stroke-width="1.2" fill="none"/>' % (X0, Y1 - 6, Y0, X1, INK)]
for v in (0, 20, 40, 60):
    b += ['<path d="M%g %g H%g" stroke="%s" stroke-width=".8"/>' % (X0, ly(v), X1, RULE), t(X0 - 8, ly(v) + 4, "%d%%" % v, 10.5, SOFT, "end")]
path = " ".join(("M" if i == 0 else "L") + "%.1f %.1f" % (lx(h), ly(v)) for i, (h, v, _) in enumerate(pts))
b.append('<path d="%s" stroke="#9a7b1c" stroke-width="2.6" fill="none" stroke-linejoin="round"/>' % path)
for h, v, lab in pts:
    b += ['<circle cx="%.1f" cy="%.1f" r="4.2" fill="#9a7b1c" stroke="#fff" stroke-width="1.2"/>' % (lx(h), ly(v)),
          t(lx(h), ly(v) - 10, "%g" % v, 10.5, INK, "middle", "600"), t(lx(h), Y0 + 18, lab, 10.5, SOFT, "middle")]
b += [t(X0 - 44, Y1 - 12, "savings in relearning", 11, SOFT, "start", "600"),
      t((X0 + X1) / 2, Y0 + 38, "time since learning (drawn on a stretching scale)", 11, SOFT, "middle")]
svg("forgetting", 520, 276, "\n".join(b), "Ebbinghaus's savings after delays, from his 1885 tables")

# 4.4 three levels
LV = "#3f7a3a"
def box(x, y, w, s, strong=False):
    return ('<rect x="%g" y="%g" width="%g" height="30" rx="4" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x, y, w, LV if strong else "#f3f1ea", LV)
            + t(x + w / 2, y + 20, s, 12.5, "#fff" if strong else INK, "middle", "700" if strong else "500"))
b = [t(10, 46, "superordinate", 11, SOFT, "start", "600"), t(10, 116, "basic", 11, LV, "start", "700"),
     t(10, 186, "subordinate", 11, SOFT, "start", "600")]
for cx, top, mid, subs in ((215, "furniture", "chair", ("kitchen chair", "armchair")),
                           (415, "animal", "dog", ("beagle", "sheepdog"))):
    b += [box(cx - 60, 26, 120, top), box(cx - 50, 96, 100, mid, True),
          '<path d="M%g 56 V96" stroke="%s" stroke-width="1.4"/>' % (cx, LV)]
    for k, s in enumerate(subs):
        sx = cx - 100 + k * 104
        b += [box(sx, 166, 96, s), '<path d="M%g 126 L%g 166" stroke="%s" stroke-width="1.4"/>' % (cx, sx + 48, LV)]
b.append(t(315, 226, "named first, learned first, recognised fastest: the middle row", 11.5, SOFT, "middle", "400", ' font-style="italic"'))
svg("levels", 520, 236, "\n".join(b), "Rosch's three levels of a taxonomy, with the basic level marked")

# 5.3 summation and the threshold
LC = "#2e6f86"
def trace(x0, bumps, spike_at=None):
    rest, thr = 170, 110
    pts = []
    for i in range(0, 201):
        x = i
        v = 0
        for b0 in bumps:
            if x >= b0:
                d = x - b0
                v += 26 * (d / 6) * math.exp(1 - d / 6)
        y = rest - v
        pts.append((x0 + x, y))
    if spike_at is not None:
        cut = next(i for i, (x, y) in enumerate(pts) if y <= thr)
        sx = pts[cut][0]
        pts = pts[:cut + 1] + [(sx + 4, 30), (sx + 9, 182), (sx + 20, 176), (sx + 40, 171)] + [(px, 170) for px, _ in pts if px > sx + 40]
    d = " ".join(("M" if i == 0 else "L") + "%.1f %.1f" % p for i, p in enumerate(pts))
    return ('<path d="M%g 170 H%g" stroke="%s" stroke-width=".9" stroke-dasharray="1 0"/>' % (x0, x0 + 200, RULE)
            + '<path d="M%g 110 H%g" stroke="#9c3b2f" stroke-width="1.3" stroke-dasharray="5 4"/>' % (x0, x0 + 200)
            + '<path d="%s" stroke="%s" stroke-width="2.4" fill="none" stroke-linejoin="round"/>' % (d, LC)
            + "".join('<path d="M%g 196 v-10" stroke="%s" stroke-width="2"/>' % (x0 + b0, INK) for b0 in bumps))
b = [trace(60, (20, 85, 150)), trace(300, (34, 40, 46, 52), True),
     t(52, 114, "threshold, about -55 mV", 10.5, "#9c3b2f", "end"), t(52, 174, "rest, about -70 mV", 10.5, SOFT, "end"),
     t(160, 222, "pushes far apart: each fades first", 11.5, INK, "middle", "600"),
     t(400, 222, "pushes close together: they add up, and it fires", 11.5, INK, "middle", "600"),
     t(160, 238, "(each tick marks one excitatory push)", 10.5, SOFT, "middle"), t(392, 26, "action potential", 11, LC, "start", "700")]
svg("threshold_", 520, 248, "\n".join(b), "temporal summation reaching the firing threshold, and falling short")

# 7.2 error-driven learning (Rescorla-Wagner, step 0.3, outcome 1)
EC = "#6e4590"
V, rows = 0.0, []
for n in range(12):
    err = 1 - V
    rows.append((V, err)); V += 0.3 * err
X0, Y0, W, H = 70, 210, 420, 170
b = ['<path d="M%g %g V%g H%g" stroke="%s" stroke-width="1.2" fill="none"/>' % (X0, Y0 - H - 6, Y0, X0 + W, INK),
     '<path d="M%g %g H%g" stroke="%s" stroke-width="1.2" stroke-dasharray="5 4"/>' % (X0, Y0 - H, X0 + W, SOFT),
     t(X0 + W, Y0 - H - 6, "the outcome, fully predicted", 10.5, SOFT, "end")]
step = W / 12
for n, (v, e) in enumerate(rows):
    x = X0 + step * n + step / 2
    b += ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity=".22"/>' % (x - 11, Y0 - H, 22, e * H, EC),
          t(x, Y0 + 16, str(n + 1), 10.5, SOFT, "middle")]
b.append('<path d="%s" stroke="%s" stroke-width="2.6" fill="none"/>' % (
    " ".join(("M" if n == 0 else "L") + "%.1f %.1f" % (X0 + step * n + step / 2, Y0 - (v + 0.3 * e) * H) for n, (v, e) in enumerate(rows)), EC))
b += [t(X0 + W / 2, Y0 + 34, "trial", 11, SOFT, "middle"), t(X0 - 10, Y0 - H / 2, "strength", 11, SOFT, "end"),
      '<rect x="%g" y="236" width="14" height="10" fill="%s" opacity=".22"/>' % (X0, EC), t(X0 + 20, 245, "the error still to learn, before each trial", 11, INK),
      '<path d="M%g 260 h14" stroke="%s" stroke-width="2.6"/>' % (X0, EC), t(X0 + 20, 264, "what has been learned, after it", 11, INK)]
svg("prediction", 520, 274, "\n".join(b), "an association growing by a fixed share of each trial's prediction error")
print("six figures written")

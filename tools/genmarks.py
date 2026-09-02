#!/usr/bin/env python3
"""Draw the eight MARKS for the player status screen.

    python3 tools/genmarks.py

gfx/trainer_card/badges.png is sixteen 16x16 blocks alternating FACE, BADGE:
DrawBadges shows the face until the mark is earned, then the badge. Vanilla put
a gym leader's portrait in the face slot. We put the mark itself, drawn as an
unfilled ghost -- so the whole toolkit is visible from hour one and fills in as
the player is certified. The eight concepts exist whether or not you hold the
certificate for them.

Section 5 assigns each benchmark exactly one concept, so nothing here is
invented; the icons are those eight, and each is an INSTRUMENT or a PLOT:

    SLATE  representation    a slab with the record cut into it
    SLOPE  gradient descent  a valley, and something resting at the bottom
    SENSE  perception        wavefronts arriving, weakening as they come
    FIT    training          scatter, and the line drawn through it
    SKEW   bias             a distribution whose peak misses the centre
    FRAME  attention         brackets holding some of the field and not the rest
    HEAT   temperature       a thermometer
    TRUE   alignment         a plumb bob, hanging exactly on centre

Read as a set they are a bench of measuring tools, which is what a benchmark
issues marks against. Three of them (slate, thermometer, plumb bob) are also
ordinary workshop instruments -- this world's technical vocabulary sits on
physical objects, and 5.1's CAIRN would approve of every one.

No glyphs, no letters: craft rule 1 holds on the status screen too.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import write_png

ENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
N, PAPER = 16, 3


class Ico:
    def __init__(self): self.g = [[PAPER] * N for _ in range(N)]
    def px(self, x, y, v=0):
        if 0 <= x < N and 0 <= y < N: self.g[y][x] = v
    def line(self, x0, y0, x1, y1, v=0):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        e = dx + dy
        while True:
            self.px(x0, y0, v)
            if x0 == x1 and y0 == y1: return
            e2 = 2 * e                      # both tests read the SAME e2
            if e2 >= dy: e += dy; x0 += sx
            if e2 <= dx: e += dx; y0 += sy
    def rect(self, x0, y0, x1, y1, v=0, fill=None):
        if fill is not None:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1): self.px(x, y, fill)
        self.line(x0, y0, x1, y0, v); self.line(x0, y1, x1, y1, v)
        self.line(x0, y0, x0, y1, v); self.line(x1, y0, x1, y1, v)
    def disc(self, cx, cy, r, v=0, fill=None):
        for y in range(N):
            for x in range(N):
                d = math.hypot(x - cx, y - cy)
                if d <= r - 0.7 and fill is not None: self.px(x, y, fill)
                elif d <= r + 0.2 and d > r - 0.9: self.px(x, y, v)
    def arc(self, cx, cy, r, a0, a1, v=0):
        steps = int(r * 8) + 8
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            self.px(round(cx + r * math.cos(a)), round(cy + r * math.sin(a)), v)
    def curve(self, f, x0, x1, v=0):
        pts = [(x, round(f(x))) for x in range(x0, x1 + 1)]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]): self.line(ax, ay, bx, by, v)
        return pts
    def ghost(self):
        """Not yet earned: the structure survives at the lightest ink, the fill does not.

        Dropping level 1 rather than greying it is what keeps the ghost an
        outline instead of a solid block -- and it means HEAT's unearned state
        is a thermometer reading nothing, which is the right picture.
        """
        out = Ico()
        out.g = [[2 if v == 0 else PAPER for v in row] for row in self.g]
        return out


def slate():
    """A slab with the record cut into it. If it is not written down, it did not happen."""
    i = Ico()
    i.rect(2, 2, 13, 13, 0, fill=1)
    i.rect(3, 3, 12, 12, 0, fill=1)
    for x in (5, 8, 11):                      # a tally, scored deep
        i.line(x, 5, x, 8, 0)
    i.line(5, 10, 11, 10, 0)                  # and a rule under it
    return i


def slope():
    """A hillside, and something already partway down it. The doldrums ARE the minimum."""
    i = Ico()
    f = lambda x: 3.0 + 0.62 * x
    for x in range(0, 16):                    # the ground, solid beneath the surface
        for y in range(round(f(x)), 15): i.px(x, y, 1)
    i.curve(f, 0, 15, 0)
    i.line(0, 15, 15, 15, 0)
    i.disc(10, 6, 2.6, 0, fill=0)             # rolling, and not finished
    return i


def sense():
    """Wavefronts arriving at a receptor. Raw input, fast and shallow."""
    i = Ico()
    i.disc(2, 8, 2.4, 0, fill=0)
    for r in (5, 6, 9, 10):                   # two fronts, each two pixels thick
        i.arc(2, 8, r, -46, 46, 0)
    return i


def fit():
    """Scatter, and the line drawn through it. Tuned to these points and no others."""
    i = Ico()
    i.line(1, 1, 1, 14, 1); i.line(1, 14, 15, 14, 1)
    i.line(3, 12, 14, 3, 0)                   # the fit
    for x, y in ((4, 8), (6, 12), (9, 4), (11, 8)):
        i.rect(x, y, x + 1, y + 1, 0, fill=0)
    return i


def skew():
    """A distribution whose peak does not sit over the centre. That gap is the lesson."""
    i = Ico()
    f = lambda x: 12 - 9.5 * math.exp(-((x - 3.8) ** 2) / (2 * (1.15 if x < 3.8 else 5.2) ** 2))
    for x in range(1, 15):                    # solid under the curve
        for y in range(round(f(x)), 13): i.px(x, y, 1)
    i.curve(f, 1, 14, 0)
    i.line(1, 13, 14, 13, 0)
    i.line(8, 14, 8, 15, 0)                    # where the centre actually is
    return i


def frame():
    """Brackets holding some of the field. What falls outside them is still there."""
    i = Ico()
    for cx, cy, dx, dy in ((1, 1, 1, 1), (14, 1, -1, 1), (1, 14, 1, -1), (14, 14, -1, -1)):
        for k in range(2):
            i.line(cx + k * dx, cy + k * dy, cx + 4 * dx, cy + k * dy, 0)
            i.line(cx + k * dx, cy + k * dy, cx + k * dx, cy + 4 * dy, 0)
    i.rect(6, 6, 9, 9, 0, fill=0)             # attended to
    for x, y in ((0, 7), (15, 8), (7, 0), (8, 15)):
        i.px(x, y, 2)                          # not attended to
    return i


def heat():
    """A thermometer. Temperature is the dial that decides how surprising the next step is."""
    i = Ico()
    i.rect(5, 1, 9, 10, 0, fill=PAPER)
    i.disc(7, 12, 3.2, 0, fill=1)
    for y in range(5, 12):                    # the column, risen
        i.line(6, y, 8, y, 1)
    for y in (3, 5, 7): i.line(10, y, 12, y, 1)   # graduations
    return i


def true():
    """A plumb bob, hanging exactly on centre. Alignment, in the sense a carpenter uses."""
    i = Ico()
    i.line(2, 1, 13, 1, 0); i.line(2, 2, 13, 2, 0)     # the beam
    i.line(7, 3, 7, 7, 0)                              # the line
    i.line(4, 8, 10, 8, 0)
    for y in range(8, 15):                             # a solid bob, tapering to a point
        w = max(0, 3 - (y - 8) // 2 * 1)
        for x in range(7 - w, 8 + w): i.px(x, y, 1)
        i.px(7 - w - 1, y, 0); i.px(8 + w, y, 0)
    for x in range(0, 16, 3): i.px(x, 15, 2)           # the ground it is true to
    return i


MARKS = [("SLATE", slate), ("SLOPE", slope), ("SENSE", sense), ("FIT", fit),
         ("SKEW", skew), ("FRAME", frame), ("HEAT", heat), ("TRUE", true)]

rows = []
for name, fn in MARKS:
    mark = fn()
    rows += mark.ghost().g + mark.g          # face slot first, then the badge
    print("  %-6s %s" % (name, fn.__doc__.split('.')[0]))
write_png(os.path.join(ENG, "gfx/trainer_card/badges.png"), rows, 2)
print("  gfx/trainer_card/badges.png 16x%d" % len(rows))

if "--show" in sys.argv:
    for n, (name, fn) in enumerate(MARKS):
        g = fn().g
        print("\n" + name)
        for y in range(N): print("   " + "".join("#:. "[v] for v in g[y]))

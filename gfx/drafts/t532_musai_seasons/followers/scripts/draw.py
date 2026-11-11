#!/usr/bin/env python3
"""T-534: the MUSAI branch's followers, drawn from the finals -- 6 forms x 4 seasons, 24 looks (DRAFT).

    python3 gfx/drafts/t532_musai_seasons/followers/scripts/draw.py          # write ../<name>_<season>_follower.png
    python3 gfx/drafts/t532_musai_seasons/followers/scripts/draw.py --sheet OUT.png   # and a 6x4 contact sheet

The user, 2026-11-11 ("Yes, draw them"): every MUSAI form follows in its season's look. Each follower is drawn here
from the form's BUILT front (engineGba/graphics/pokemon/<slot>[/<season>]/front.png, the final as the ROM has it, in
its own normal.pal) and written as an RGBA 32x32 frame in exactly those colours: the creature at most 20 tall and 22
wide, its lowest row on row 28 (T-464's follower size; tools/gbafollower.py's MAX_H, MAX_W, GROUND). tools/gbafollower.py
reads these and writes follower.png in the form's OWN palette (normal.pal), and tools/gbafollowerpal.py gives such a
follower its normal.pal and shiny.pal as they stand -- every colour of the final, where the shared-icon remap reached
four to nine of them and the vehicles went to mud.

HOW. 1. The front is reduced by footprint vote, the outline (index 5) winning a cell at 30% and a small accent (a
light, an eye, a leaf: an index under 3% of the body) winning at 20%, so eyes and seasonal marks survive the
reduction. Streak entries 11-14 (grey until the battle paints them; the follower is never painted) vote as the
colour under them most often round them. 2. Each form's VEHICLE is then redrawn pixel by pixel at follower size
(VEHICLE below), so it reads at 1x: winter's runners, autumn's rugged wheels, summer's pontoon floats, spring's
model-plane wings -- whichever of them the final carries. MUSAI itself carries no vehicle in any season (the finals:
the base form wears the season on its antennae -- frost, buds and a sprout, a leaf), so its accents are what is kept.
3. Every body pixel that meets the ground gets the outline, so the silhouette holds against grass.
"""
import os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
GBA = os.path.join(ROOT, "engineGba")
MAX_H, MAX_W, GROUND = 20, 22, 28
OUTLINE = 5
STREAK = (11, 12, 13, 14)

BRANCH = [("musai", "eevee"), ("codemusai", "flareon"), ("seekmusai", "jolteon"),
          ("caremusai", "vaporeon"), ("lensmusai", "espeon"), ("maskmusai", "umbreon")]
SEASONS = ["winter", "spring", "summer", "autumn"]


def front(slot, season):
    d = os.path.join(GBA, "graphics", "pokemon", slot) if season == "summer" else \
        os.path.join(GBA, "graphics", "pokemon", slot, season)
    im = Image.open(os.path.join(d, "front.png"))
    pal = [tuple(im.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    px = im.load()
    g = [[px[x, y] for x in range(64)] for y in range(64)]
    return g, pal


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def unstreak(g):
    """Streak pixels (grey until a battle paints them) take the commonest colour round them."""
    h, w = len(g), len(g[0])
    out = [row[:] for row in g]
    for _ in range(4):
        changed = False
        for y in range(h):
            for x in range(w):
                if out[y][x] in STREAK:
                    n = [out[yy][xx] for yy in range(max(0, y - 2), min(h, y + 3)) for xx in range(max(0, x - 2), min(w, x + 3))
                         if out[yy][xx] and out[yy][xx] not in STREAK and out[yy][xx] != OUTLINE]
                    if n:
                        out[y][x] = max(sorted(set(n)), key=n.count)
                        changed = True
        if not changed:
            break
    for y in range(h):
        for x in range(w):
            if out[y][x] in STREAK:
                out[y][x] = 3
    return out


def bbox(g, skip=()):
    pts = [(x, y) for y, row in enumerate(g) for x, v in enumerate(row) if v and (x, y) not in skip]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def reduce(g, pal, crop=None, fit=(MAX_H, MAX_W), outline_share=0.4):
    """The front's box (or CROP: x0, y0, x1, y1 inclusive) reduced to fit FIT. Each cell: ground if under half of it
    is ink; the outline if OUTLINE_SHARE of its ink is outline; a small accent's colour if the accent is a fifth of
    it; else the palette colour nearest the MEAN of its other ink (a vote speckles at this scale; a mean holds the
    shading's steps)."""
    x0, y0, x1, y1 = crop or bbox(g)
    src = [row[x0:x1 + 1] for row in g[y0:y1 + 1]]
    h, w = len(src), len(src[0])
    sc = min(fit[0] / h, fit[1] / w)
    th, tw = min(fit[0], max(1, round(h * sc))), min(fit[1], max(1, round(w * sc)))
    total = {}
    for row in src:
        for v in row:
            if v:
                total[v] = total.get(v, 0) + 1
    body = sum(total.values())
    accent = {k for k, n in total.items() if n < 0.03 * body and k != OUTLINE}
    usable = [k for k in total if k != OUTLINE and k not in accent]
    cells = [[0] * tw for _ in range(th)]
    for y in range(th):
        for x in range(tw):
            ya, yb = int(y * h / th), max(int(y * h / th) + 1, int((y + 1) * h / th))
            xa, xb = int(x * w / tw), max(int(x * w / tw) + 1, int((x + 1) * w / tw))
            vals = [src[yy][xx] for yy in range(ya, min(yb, h)) for xx in range(xa, min(xb, w))]
            ink = [v for v in vals if v]
            if not vals or len(ink) * 2 < len(vals):
                continue
            acc = [v for v in ink if v in accent]
            rest = [v for v in ink if v != OUTLINE and v not in accent]
            if acc and len(acc) >= 0.2 * len(ink):
                cells[y][x] = max(sorted(set(acc)), key=acc.count)
            elif ink.count(OUTLINE) >= outline_share * len(ink) or not rest:
                cells[y][x] = OUTLINE
            else:
                m = [sum(pal[v][i] for v in rest) / len(rest) for i in range(3)]
                cells[y][x] = min(usable, key=lambda k: sum((pal[k][i] - m[i]) ** 2 for i in range(3)))
    return despeckle8(despeckle(cells, accent), accent)


def despeckle8(cells, keep):
    """Then a body pixel none of whose eight neighbours shares its colour, and five or more share one other body
    colour, takes that colour (the pink ramps speckle where a mean falls between two steps)."""
    h, w = len(cells), len(cells[0])
    out = [row[:] for row in cells]
    for y in range(h):
        for x in range(w):
            v = cells[y][x]
            if not v or v == OUTLINE or v in keep:
                continue
            n = [cells[y + dy][x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                 if (dy or dx) and 0 <= y + dy < h and 0 <= x + dx < w]
            if v in n:
                continue
            body = [k for k in n if k and k != OUTLINE and k not in keep]
            for k in sorted(set(body)):
                if body.count(k) >= 5:
                    out[y][x] = k
    return out


def despeckle(cells, keep):
    """A lone body pixel whose four neighbours are three or four of one other body colour takes that colour."""
    h, w = len(cells), len(cells[0])
    out = [row[:] for row in cells]
    for y in range(h):
        for x in range(w):
            v = cells[y][x]
            if not v or v == OUTLINE or v in keep:
                continue
            n = [cells[y + dy][x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))
                 if 0 <= y + dy < h and 0 <= x + dx < w]
            if v in n:
                continue
            body = [k for k in n if k and k != OUTLINE and k not in keep]
            for k in set(body):
                if body.count(k) >= 3:
                    out[y][x] = k
    return out


def place(cells, dx=0):
    h, w = len(cells), len(cells[0])
    out = [[0] * 32 for _ in range(32)]
    oy, ox = GROUND + 1 - h, (32 - w) // 2 + dx
    for y in range(h):
        for x in range(w):
            if cells[y][x]:
                out[oy + y][ox + x] = cells[y][x]
    return out


def outline(g):
    """A body pixel beside the ground (4-neighbour) that is light becomes the outline -- only where the reduction
    left a light edge, so a dark rim stays the drawing's own."""
    out = [row[:] for row in g]
    for y in range(32):
        for x in range(32):
            v = g[y][x]
            if not v or v == OUTLINE:
                continue
            edge = any(not (0 <= y + dy < 32 and 0 <= x + dx < 32) or not g[y + dy][x + dx]
                       for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            if edge and v in LIGHT:
                out[y][x] = OUTLINE
    return out


LIGHT = set()


# --------------------------------------------------------------------------------------------- the vehicles
#  Drawn pixel by pixel over the reduced body, on the 32x32 frame (the creature centred, its lowest row 28). Indices
#  are the form's own: across the branch 1 is the lightest body step, 2 and 3 the middle, 4 the darkest, 5 the outline.

def put(g, x, y, v):
    if 0 <= x < 32 and 0 <= y < 32:
        g[y][x] = v


def hline(g, x0, x1, y, v):
    for x in range(x0, x1 + 1):
        put(g, x, y, v)


def clear(g, y0, y1=GROUND, x0=0, x1=31):
    for y in range(y0, y1 + 1):
        hline(g, x0, x1, y, 0)


def runner(g, x0, x1, face, rim=OUTLINE, y=GROUND):
    """A ski runner on the ground line: a light blade over a dark edge, its front tip (left: icons face left)
    turned up in a hook."""
    hline(g, x0 + 1, x1, y, rim)
    hline(g, x0 + 1, x1 - 1, y - 1, face)
    put(g, x1, y - 1, rim)
    put(g, x0, y - 1, rim)
    put(g, x0 - 1, y - 2, rim)
    put(g, x0, y - 2, face)


def wheel(g, cx, cy, tread, hub, rim=OUTLINE):
    """A rugged wheel, 7 across: an octagon of tyre (dark rim, darker tread) round a light hub, with a lug standing
    out at the top and each side and at the upper diagonals -- the ground takes the bottom."""
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            if abs(dx) + abs(dy) > 4:
                continue
            edge = abs(dx) == 3 or abs(dy) == 3 or abs(dx) + abs(dy) == 4
            put(g, cx + dx, cy + dy, rim if edge else tread)
    for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
        put(g, cx + dx, cy + dy, hub)
    put(g, cx, cy, OUTLINE)
    for dx, dy in ((-4, 0), (4, 0), (0, -4), (-3, -2), (3, -2), (-2, -3), (2, -3)):
        put(g, cx + dx, cy + dy, rim)


def pontoon(g, x0, x1, face, shade, rim=OUTLINE, y=GROUND):
    """A pontoon float, 3 tall on the ground line: rounded ends, a light top, a shaded underside, a dark keel."""
    put(g, x0, y - 2, 0)
    hline(g, x0 + 1, x1 - 1, y - 2, face)
    put(g, x0, y - 1, rim)
    hline(g, x0 + 1, x1 - 1, y - 1, shade)
    put(g, x1, y - 1, rim)
    put(g, x0, y - 2, rim)
    put(g, x1, y - 2, rim)
    hline(g, x0 + 1, x1 - 1, y, rim)
    put(g, x0 + 1, y - 2, face)


def wing(g, x0, x1, y, face, rim=OUTLINE):
    """A model plane's wing, 3 rows: a dark leading and trailing edge round a light face; the tip at the end away
    from the body is rounded off."""
    tip = x0 if x0 < 16 else x1
    for x in range(x0, x1 + 1):
        put(g, x, y - 1, rim if x != tip else 0)
        put(g, x, y, face)
        put(g, x, y + 1, rim if x != tip else 0)
    put(g, tip, y, rim)


def line_down(g, x, y, v=OUTLINE):
    """LENSMUSAI spring's control line (T-534): from the wingtip to the ground line, a pixel left every third row."""
    n = 0
    while y <= GROUND:
        put(g, x, y, v)
        y += 1
        n += 1
        if n % 3 == 0:
            x -= 1


def leftmost(g, y0, y1):
    return min((x, y) for y in range(y0, y1 + 1) for x in range(32) if g[y][x])


def codemusai_winter(g, pal):
    clear(g, 26)
    for x in (14, 15, 19, 20):
        put(g, x, 26, 4)
    runner(g, 9, 25, face=1)


def codemusai_spring(g, pal):
    wing(g, 5, 11, 24, face=1)
    wing(g, 20, 26, 24, face=1)


def codemusai_summer(g, pal):
    clear(g, 24)
    for x in (10, 21):
        put(g, x, 24, 4)
        put(g, x, 25, 4)
    pontoon(g, 5, 14, face=1, shade=2, y=27)
    hline(g, 6, 13, 28, OUTLINE)
    pontoon(g, 17, 26, face=1, shade=2, y=27)
    hline(g, 18, 25, 28, OUTLINE)
    put(g, 5, 27, OUTLINE); put(g, 14, 27, OUTLINE); put(g, 17, 27, OUTLINE); put(g, 26, 27, OUTLINE)
    hline(g, 6, 13, 27, 3)
    hline(g, 18, 25, 27, 3)


def chassis_wheels(g, xa, xb, y0, cxs, tread, hub):
    clear(g, y0)
    hline(g, xa, xb, y0, 4)
    hline(g, xa + 2, xb - 2, y0 + 1, OUTLINE)
    for cx in cxs:
        wheel(g, cx, GROUND - 3, tread, hub)


def codemusai_autumn(g, pal):
    chassis_wheels(g, 9, 22, 22, (9, 22), tread=4, hub=2)


def seekmusai_autumn(g, pal):
    chassis_wheels(g, 8, 21, 22, (9, 21), tread=4, hub=2)


def caremusai_summer(g, pal):
    clear(g, 24)
    hline(g, 6, 24, 24, OUTLINE)
    hline(g, 7, 23, 25, 1)
    put(g, 6, 25, OUTLINE); put(g, 24, 25, OUTLINE)
    for x0, x1 in ((7, 12), (18, 23)):
        put(g, x0, 26, OUTLINE); hline(g, x0 + 1, x1 - 1, 26, 1); put(g, x1, 26, OUTLINE)
        put(g, x0, 27, OUTLINE); hline(g, x0 + 1, x1 - 1, 27, 3); put(g, x1, 27, OUTLINE)
        hline(g, x0 + 1, x1 - 1, 28, OUTLINE)
    hline(g, 7, 23, 25, 2)
    hline(g, 8, 22, 25, 1)


def lensmusai_spring(g, pal):
    x, y = leftmost(g, 18, 24)
    line_down(g, x - 1, y + 1)


def maskmusai_runner(g, pal):
    clear(g, 27)
    xs = [x for x in range(32) if g[26][x]]
    runner(g, min(xs) + 1, max(xs) - 1, face=2)


def nothing(g, pal):
    pass


#  VEHICLE[(name, season)]: the forms whose final carries one of the four (the user's T-532 brief: winter runners,
#  autumn rugged wheels, summer pontoons, spring model-plane wings) -- drawn again here so each reads at 1x.
VEHICLE = {
    ("codemusai", "winter"): codemusai_winter,
    ("codemusai", "spring"): codemusai_spring,
    ("codemusai", "summer"): codemusai_summer,
    ("codemusai", "autumn"): codemusai_autumn,
    ("seekmusai", "autumn"): seekmusai_autumn,
    ("caremusai", "summer"): caremusai_summer,
    ("lensmusai", "spring"): lensmusai_spring,
    ("maskmusai", "winter"): maskmusai_runner,
    ("maskmusai", "spring"): maskmusai_runner,
    ("maskmusai", "summer"): maskmusai_runner,
    ("maskmusai", "autumn"): maskmusai_runner,
}

#  SPEC[(name, season)]: crop (the front's box, inclusive, in its 64x64) and fit, where the plain box would shrink
#  the body for something the vehicle pass draws itself.
SPEC = {
    ("lensmusai", "spring"): {"crop": (7, 10, 62, 52), "fit": (MAX_H, 20)},
}


def roles(pal):
    """The form's body indices, lightest first (the outline and the unused black entries left out)."""
    body = [i for i in range(1, 10) if i != OUTLINE and pal[i] != (0, 0, 0)]
    return sorted(body, key=lambda i: -lum(pal[i]))


def make(name, slot, season):
    g, pal = front(slot, season)
    g = unstreak(g)
    global LIGHT
    order = roles(pal)
    LIGHT = set(order[:1])
    spec = SPEC.get((name, season), {})
    cells = reduce(g, pal, spec.get("crop"), spec.get("fit", (MAX_H, MAX_W)), spec.get("oshare", 0.4))
    out = place(cells, spec.get("dx", 0))
    if spec.get("outline"):
        out = outline(out)
    VEHICLE.get((name, season), nothing)(out, pal)
    return out, pal



def to_rgba(g, pal):
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = im.load()
    for y in range(32):
        for x in range(32):
            if g[y][x]:
                px[x, y] = pal[g[y][x]] + (255,)
    return im


def bounds(g):
    pts = [(x, y) for y in range(32) for x in range(32) if g[y][x]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, max(ys)


def main():
    sheet = "--sheet" in sys.argv and sys.argv[sys.argv.index("--sheet") + 1]
    S = 6
    CW, CH = 128 + 32 * S + 48, 32 * S + 8
    big = Image.new("RGBA", (4 * CW, 6 * CH), (112, 168, 104, 255))
    bad = []
    for r, (name, slot) in enumerate(BRANCH):
        for c, season in enumerate(SEASONS):
            g, pal = make(name, slot, season)
            w, h, low = bounds(g)
            if w > MAX_W or h > MAX_H or low != GROUND:
                bad.append("%s %s %dx%d low %d" % (name, season, w, h, low))
            im = to_rgba(g, pal)
            im.save(os.path.join(OUTDIR, "%s_%s_follower.png" % (name, season)))
            if sheet:
                fg, fpal = front(slot, season)
                fim = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
                fp = fim.load()
                for y in range(64):
                    for x in range(64):
                        if fg[y][x]:
                            fp[x, y] = fpal[fg[y][x]] + (255,)
                x0, y0 = c * CW, r * CH
                big.alpha_composite(fim.resize((128, 128), Image.NEAREST), (x0, y0 + 32 * S - 128))
                big.alpha_composite(im.resize((32 * S, 32 * S), Image.NEAREST), (x0 + 128, y0))
                big.alpha_composite(im, (x0 + 128 + 32 * S, y0 + 32 * S - 32))
    if sheet:
        big.save(sheet)
    for b in bad:
        print("  OVER:", b)
    print("  24 followers written to %s" % os.path.relpath(OUTDIR, ROOT))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

"""T-534 (DRAFT): the user's three sprite notes, drawn pixel by pixel in code on the existing finals -- no AI.

    python3 edits.py BEFORE_DIR OUT_DIR

BEFORE_DIR holds the finals as they stood before T-534 (git show d5dd894c:gfx/drafts/t532_musai_seasons/finals/<file>);
OUT_DIR gets the edited ones, which went into ../finals/. Each form keeps its palette: the edits use the drawing's own
greys and one green, and gbasprite's place_rich maps them into the type ramp as before. Streak markers are never
painted over (they are the streaks' patches, T-475)."""
import os, sys
from PIL import Image
BEFORE = sys.argv[1].rstrip("/") + "/"
OUT = sys.argv[2]
MARKERS = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0)]
def marker(c): return c[3] > 127 and any(max(abs(c[k] - m[k]) for k in range(3)) <= 48 for m in MARKERS)
def load(n): return Image.open(BEFORE + n + ".png").convert("RGBA")
def save(im, n): im.save(os.path.join(OUT, n + ".png"))
def put(im, x, y, rgb):
    if 0 <= x < 64 and 0 <= y < 64 and not marker(im.getpixel((x, y))):
        im.putpixel((x, y), tuple(rgb) + (255,))
def line(im, x0, y0, x1, y1, rgb):
    dx, dy = abs(x1 - x0), -abs(y1 - y0); sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1; e = dx + dy
    while True:
        put(im, x0, y0, rgb)
        if (x0, y0) == (x1, y1): break
        e2 = 2 * e
        if e2 >= dy: e += dy; x0 += sx
        if e2 <= dx: e += dx; y0 += sy

# 1. LENSMUSAI spring: the control line, from the wingtip down to the ground line at the frame's edge (the lowest
#    row the form already has, so its battle coordinates do not move: it stays grounded, T-452's rule)
WIRE = (28, 28, 32)
im = load("lensmusai_spring_front"); line(im, 6, 31, 0, 51, WIRE); save(im, "lensmusai_spring_front")
im = load("lensmusai_spring_back");  line(im, 59, 33, 63, 50, WIRE); save(im, "lensmusai_spring_back")   # the same wing, seen from behind

# 2. CAREMUSAI summer: two hulls that never touch, one deck across them. Seen bow-on, as the body is: a deck of
#    planks, and under each end a U of a hull, the water's gap between them. The two streak bars that lay on the old
#    floats (rows 48 and 50) move onto the right hull, same colours and lengths, so the streaks still have their patch.
OL, TOP, PL, SEAM = (26, 26, 30), (226, 226, 232), (178, 178, 186), (118, 118, 126)
SHADE = [(238, 238, 244), (206, 206, 214), (176, 176, 184), (146, 146, 156), (116, 116, 126), (92, 92, 102)]
INSET = [0, 0, 0, 0, 1, 1, 2, 3, 5]                     # the hull's U, rows 0..8
def hull(im, x0, x1, y0):
    for r, inset in enumerate(INSET):
        a, b = x0 + inset, x1 - inset
        for x in range(a, b + 1):
            if x in (a, b) or r == len(INSET) - 1:
                put(im, x, y0 + r, OL); continue
            f = (x - a) / max(1, b - a)                   # lit from the left, as the body is
            k = min(len(SHADE) - 1, int(f * 4) + (1 if r >= 6 else 0) + (1 if r == 0 else 0))
            put(im, x, y0 + r, SHADE[k])
def catamaran(im, top, left, right, hw):
    moved = []
    for y in range(top, 64):
        for x in range(64):
            c = im.getpixel((x, y))
            if marker(c): moved.append((x, y, c))
            im.putpixel((x, y), (0, 0, 0, 0))
    hull(im, left, left + hw - 1, top + 4)
    hull(im, right - hw + 1, right, top + 4)
    for x in range(left - 1, right + 2):                  # the deck: outline, its top, the planks' edge, outline
        end = x in (left - 1, right + 1)
        im.putpixel((x, top), OL + (255,)); im.putpixel((x, top + 3), OL + (255,))
        im.putpixel((x, top + 1), (OL if end else TOP) + (255,))
        im.putpixel((x, top + 2), (OL if end else (SEAM if (x - left) % 6 == 5 else PL)) + (255,))
    xs = [m[0] for m in moved]
    for x, y, c in moved:                                 # onto the right hull, two rows lower
        im.putpixel((x - min(xs) + right - hw + 3, y + 2), c)
im = load("caremusai_summer_front"); catamaran(im, 44, 9, 55, 14); save(im, "caremusai_summer_front")
im = load("caremusai_summer_back");  catamaran(im, 44, 9, 55, 14); save(im, "caremusai_summer_back")

# 3. CODEMUSAI: four chest lights, on on off on -- 1101, thirteen. A dark housing, 2x2 lamps, one colour lit.
HOUSE, OFF, ON = (24, 26, 30), (44, 66, 52), (90, 230, 110)
def lights(im, y):                                       # lamps on rows y, y+1; housing rows y-1 .. y+2, x 22..34
    for yy in range(y - 1, y + 3):
        for x in range(22, 35): put(im, x, yy, HOUSE)
    for i, bit in enumerate((1, 1, 0, 1)):
        for dx in (0, 1):
            for dy in (0, 1): put(im, 23 + 3 * i + dx, y + dy, ON if bit else OFF)
ROW = {"winter": 40, "spring": 40, "summer": 38, "autumn": 40}
for s, y in ROW.items():
    im = load("codemusai_%s_front" % s); lights(im, y); save(im, "codemusai_%s_front" % s)
for s, y in (("summer", 38), ("autumn", 40)):            # the backs that show the lights; winter's and spring's do not
    im = load("codemusai_%s_back" % s); lights(im, y); save(im, "codemusai_%s_back" % s)

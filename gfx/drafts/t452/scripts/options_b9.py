"""T-452 batch 9: the open questions, each option side by side, every sprite coloured as gbasprite will (place_rich on the
grid, the type's ramp and accents, shift_off included). Mocks drawn here into l/opt/ (never l/hand: nothing is chosen).

    options_b9.py      writes l/opt/*.png and sheets/t452b9_questions.png"""
import os, sys, json, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T = os.environ["T452_ROOT"]; D = T + "/l"; X = T + "/lx"; O = D + "/opt"; os.makedirs(O, exist_ok=True)
import hand4 as h4; h4.F, h4.H = D, D + "/hand"
from hand4 import load_any, stamp, op, lum, is_mark, INK
import gbs
SPEC = json.load(open("/Users/christopherhicks/Projects/DAEMONS/companion/server/data/species.json")); BY = {v["name"].lower(): v for v in SPEC.values()}
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12); FB = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 15)
GROUND = (205, 205, 172); PAPER = (236, 234, 226); INKC = (30, 30, 34); RED = (150, 30, 30)
def sv(a, name): p = f"{O}/{name}.png"; Image.fromarray(a.astype(np.uint8), "RGBA").save(p); return p
def typ(n): return gbs.primary_type(BY[n]["constant"].lower())

def colour(path, n, palfrom=None):
    g, p = gbs.place_rich(path, gbs.TYPE_COLOR[typ(n)])
    a = np.zeros((64, 64, 4), np.uint8)
    for y in range(64):
        for x in range(64):
            i = g[y][x]
            if i: a[y, x, :3] = p[i]; a[y, x, 3] = 255
    return Image.fromarray(a)
def tile(im, s=3):
    b = Image.new("RGBA", im.size, GROUND + (255,)); b.alpha_composite(im); return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)
def raw(path, s=3): return tile(Image.open(path).convert("RGBA"), s)

# ---- RELEASE A: a glowing lamp on the tail tip (pale yellow, 125 degrees from SIGNAL's teal: it stays an accent)
LAMP = ["  #####  ", " #YYYYY# ", "#YYWWWYY#", "#YWWWWWY#", "#YWWWWWY#", "#YWWWWWY#", "#YYWWWYY#", " #YYYYY# ", "  #####  "]
a = load_any("release", "front"); stamp(a, 5, 23, LAMP, {"#": INK, "Y": (238, 214, 70, 255), "W": (255, 246, 190, 255)})
rel_lamp = sv(a, "release_front_lamp")

# ---- MULTICAST A: the second pair of wings -- each drawn wing flipped upward behind the head (its entry: four places at once)
a = load_any("multicast", "front"); src = a.copy()
for (x0, y0, x1, y1), (tx, ty) in (((8, 28, 23, 48), (1, 6)), ((42, 28, 58, 48), (49, 6))):
    w = src[y0:y1, x0:x1][::-1]
    for y in range(w.shape[0]):
        for x in range(w.shape[1]):
            p, q = ty + y, tx + x
            if w[y, x, 3] > 127 and not is_mark(w[y:y + 1, x:x + 1])[0, 0] and 0 <= p < 64 and 0 <= q < 64 and a[p, q, 3] <= 127: a[p, q] = w[y, x]
mc_four = sv(a, "multicast_front_four")

# ---- the CONTENT hue trap: CONTENT's hue is 40 degrees, so every orange, salmon or yellow accent within 40 of it
#      (hue 0-80) is rotated to blue by gbasprite.shift_off. A: re-hue them out of reach -- salmon ears to rose (335),
#      an owl's amber eyes and beak to chartreuse-gold (85) -- B: as gbasprite turns them.
def rehue(n, k, to, lo=0.0, hi=0.23, also_high=0.93, rows=64):
    a = load_any(n, k); m = 0
    for y, x in zip(*np.where(op(a))):
        if y >= rows: continue
        if is_mark(a[y:y + 1, x:x + 1])[0, 0]: continue
        r, g, b = a[y, x, :3] / 255; h, s, v = colorsys.rgb_to_hsv(r, g, b)
        if s > 0.25 and v > 0.25 and (lo <= h <= hi or h >= also_high):
            a[y, x, :3] = [int(c * 255) for c in colorsys.hsv_to_rgb(to / 360, max(s, 0.45), v)]; m += 1
    print(n, k, "re-hued", m); return sv(a, f"{n}_{k}_rehue")
alarm_rose = rehue("alarm", "front", 335); lookout_rose = rehue("lookout", "front", 335, rows=16)   # the ears only: its brown legs sit in the same hues
poll_gold = rehue("poll", "front", 85, also_high=2); sup_gold = rehue("supervisor", "front", 85, also_high=2)

def red(n, d=D, kind="front"):
    h = f"{d}/hand/{n}_{kind}.png"; return h if os.path.exists(h) else f"{d}/clean/{n}_{kind}.png"
def dr(f): return Image.open(f).convert("RGB").resize((192, 192))
rows = [
 ("RELEASE: the lamp\n(entry: the brightest\nthing on the coast)", "release", [
   ("A 5701 + lamp on tail (hand)", colour(rel_lamp, "release")),
   ("B 5724: lamp on a stalk", colour(red("release", X), "release")),
   ("C 5701 as drawn, no lamp", colour(red("release"), "release")),
   ("today's (a placeholder)", None)]),
 ("MULTICAST: four wings\n(entry: four places\nat once)", "multicast", [
   ("A second pair drawn in (hand)", colour(mc_four, "multicast")),
   ("B two wings, as drawn", colour(red("multicast"), "multicast")),
   ("today's", None)]),
 ("PILOT: its light", "pilot", [
   ("A 5704: lights on its crown", colour(red("pilot"), "pilot")),
   ("B 5721: today's dome, no light", colour(red("pilot", X), "pilot")),
   ("today's", None)]),
 ("ENTRAPMENT: drawn\nsmall; no draft drew\nthe web", "entrapment", [
   ("A 5721 zoomed: legs thin", colour(red("entrapment"), "entrapment")),
   ("B 5701: big-eyed, legs kept", colour(red("entrapment", X), "entrapment")),
   ("today's", None)]),
 ("STATIC: fur on end", "static", [
   ("A 5704: a spiky crest", colour(red("static"), "static")),
   ("B 5721: plain mouse", colour(red("static", X), "static")),
   ("today's", None)]),
 ("CONTENT hue trap:\nears and owl eyes\nturned blue", "alarm", [
   ("A ALARM ears rose", colour(alarm_rose, "alarm")), ("B as built: pale blue", colour(red("alarm"), "alarm")),
   ("A POLL eyes chartreuse", colour(poll_gold, "poll")), ("B as built: blue", colour(red("poll"), "poll"))]),
 ("(the trap, continued)", "lookout", [
   ("A LOOKOUT ears rose", colour(lookout_rose, "lookout")), ("B as built", colour(red("lookout"), "lookout")),
   ("A SUPERVISOR chartreuse", colour(sup_gold, "supervisor")), ("B as built: blue", colour(red("supervisor"), "supervisor"))]),
]
s = Image.new("RGB", (4 * 260 + 210, len(rows) * 230 + 50), PAPER); d = ImageDraw.Draw(s)
d.text((10, 10), "T-452 batch 9 -- DRAFT, not in the ROM: the open questions, each option coloured as gbasprite will, 3x; recommended first",
       fill=INKC, font=FB)
for i, (t, n, cs) in enumerate(rows):
    y = 44 + i * 230; d.text((10, y + 70), t, fill=INKC, font=F)
    for j, (lab, im) in enumerate(cs):
        x = 210 + j * 260
        if im is None:
            im = Image.open("/Users/christopherhicks/Projects/DAEMONS/" + BY[n]["art"]["front"]).convert("RGBA")
            if im.width != 64: im = im.resize((64, 64))
        s.paste(tile(im), (x, y + 20)); d.text((x, y + 2), lab, fill=RED if j == 0 else INKC, font=F)
out = T + "/sheets/t452b9_questions.png"; s.save(out); print(out)

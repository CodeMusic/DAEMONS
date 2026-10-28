"""batch 10 phase 1 (copied from ba_b9.py): today | BEFORE (phase-1 picks) | AFTER (the user's answers), front / back / icon, 1x and 2x.

Fronts and backs are coloured the way the build will colour them: gbasprite.place_rich on the clean (or hand) grid,
the type's ramp and its accents (shift_off included), the back through the front's palette. Only gbasprite's
definitions are run (its top 449 lines), never its main loop. Writes only OUT."""
import os, sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
T = os.environ["T452_ROOT"]; D = T + "/n"; B = D; R = "/Users/christopherhicks/Projects/DAEMONS"   # BEFORE = the phase-1 picks as reduce2 cleaned them (n/clean), before hand_b10
sys.path.insert(0, R + "/tools"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
argv = sys.argv; sys.argv = ["gbasprite"]
G = {"__file__": R + "/tools/gbasprite.py", "__name__": "gbasprite_defs"}
exec(compile("".join(open(R + "/tools/gbasprite.py").readlines()[:449]), "gbasprite", "exec"), G)
sys.argv = argv
import gbs
SPEC = json.load(open(R + "/companion/server/data/species.json")); BY = {v["name"].lower(): v for v in SPEC.values()}
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13); FB = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
GROUND = (205, 205, 172); PARTY = (98, 156, 131); PAPER = (236, 234, 226); INK = (30, 30, 34)

def colour(front, back, typ):
    trgb = G["TYPE_COLOR"][typ]
    gf, pf = G["place_rich"](front, trgb); gb, _ = G["place_rich"](back, trgb, shared=pf)
    def im(g, pal):
        a = np.zeros((64, 64, 4), np.uint8)
        for y in range(64):
            for x in range(64):
                i = g[y][x]
                if i: a[y, x, :3] = pal[i] if i < len(pal) else (255, 0, 0); a[y, x, 3] = 255
        return Image.fromarray(a)
    #  the streak slots draw as their blank grey here, as in battle before a streak is earned
    return im(gf, pf), im(gb, pf)

def rgba(p):
    im = Image.open(p)
    if im.mode == "P":
        a = np.array(im.convert("RGBA")); a[np.array(im) == 0, 3] = 0; return Image.fromarray(a)
    return im.convert("RGBA")
def today(n, k):
    im = Image.open(f"{R}/{BY[n]['art'][k]}").convert("RGBA")
    return im if im.width == 64 else im.resize((64, 64), Image.LANCZOS)
def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im); return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)

out, items = sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]]
CW = 2 * (64 + 4 + 128 + 10) + (32 + 4 + 64 + 10); RH = 160
s = Image.new("RGB", (30 + 2 * 132 + 40 + 2 * (CW + 30) + 20, 60 + len(items) * RH), PAPER); d = ImageDraw.Draw(s)
d.text((20, 14), "T-452 batch 10 -- DRAFT, not in the ROM: today (front, back) | BEFORE (the drafts as cleaned) | AFTER (each recommended fix applied); "
       "front / back / icon, 1x and 2x, coloured as gbasprite will", fill=INK, font=FB)
for i, (n, what) in enumerate(items):
    y = 50 + i * RH; v = BY[n]; typ = gbs.primary_type(v["constant"].lower())
    d.text((20, y), "%d %s (%s) -- %s" % (v["national"], v["name"], typ, what), fill=INK, font=F)
    x = 20
    for k in ("front", "back"):
        s.paste(on(today(n, k), GROUND, 2), (x, y + 20)); x += 132
    x += 20; d.line((x - 10, y + 20, x - 10, y + RH - 10), fill=INK, width=2)
    for side in ("before", "after"):
        base = B if side == "before" else D
        def pick(k):
            h = f"{D}/hand/{n}_{k}.png"
            return h if side == "after" and os.path.exists(h) else f"{base}/clean/{n}_{k}.png"
        fr, bk = colour(pick("front"), pick("back"), typ)
        ip = f"{D}/hand/{n}_icon.png" if side == "after" and os.path.exists(f"{D}/hand/{n}_icon.png") else f"{base}/reduced/{n}_icon_before.png"
        ic = rgba(ip).crop((0, 0, 32, 32))
        for im, bg in ((fr, GROUND), (bk, GROUND), (ic, PARTY)):
            s.paste(on(im, bg, 1), (x, y + 20)); s.paste(on(im, bg, 2), (x + im.width + 4, y + 20)); x += im.width * 3 + 14
        x += 30
        if side == "before": d.line((x - 22, y + 20, x - 22, y + RH - 10), fill=INK, width=2)
s.save(out); print(out, s.size)

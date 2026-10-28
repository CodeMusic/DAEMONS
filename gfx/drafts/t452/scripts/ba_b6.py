"""batch 6 phase 2: before (phase 1 picks) | after (the user's answers), front / back / icon, 1x and 2x, with today's in ROM"""
import os, sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
T = os.environ["T452_ROOT"]; D = T + "/i"; B = T + "/before"; R = "/Users/christopherhicks/Projects/DAEMONS"
SPEC = json.load(open(R + "/companion/server/data/species.json")); BY = {v["name"].lower(): v for v in SPEC.values()}
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13); FB = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
GROUND = (205, 205, 172); PARTY = (98, 156, 131); PAPER = (236, 234, 226); INK = (30, 30, 34)
def rgba(p):
    im = Image.open(p)
    if im.mode == "P":
        a = np.array(im.convert("RGBA")); a[np.array(im) == 0, 3] = 0; return Image.fromarray(a)
    return im.convert("RGBA")
def today(n, k):
    im = Image.open(f"{R}/{BY[n]['art'][k]}").convert("RGBA")
    return im if im.width == 64 else im.resize((64, 64), Image.LANCZOS)
def icon(p): return rgba(p).crop((0, 0, 32, 32))
def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im); return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)
out, items = sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]]
CW = 3 * (64 + 4 + 128 + 10); RH = 160
s = Image.new("RGB", (30 + 2 * 128 + 40 + 2 * CW + 60, 60 + len(items) * RH), PAPER); d = ImageDraw.Draw(s)
d.text((20, 14), "T-452 batch 6 -- DRAFT, not in the ROM: today (front, back) | BEFORE (phase-1 picks) | AFTER (the user's answers); front / back / icon, 1x and 2x", fill=INK, font=FB)
for i, (n, what) in enumerate(items):
    y = 50 + i * RH; v = BY[n]
    d.text((20, y), "%d %s -- %s" % (v["national"], v["name"], what), fill=INK, font=F)
    x = 20
    for k in ("front", "back"):
        s.paste(on(today(n, k), GROUND, 2), (x, y + 20)); x += 132
    x += 20; d.line((x - 10, y + 20, x - 10, y + RH - 10), fill=INK, width=2)
    for side in ("before", "after"):
        for k in ("front", "back", "icon"):
            if side == "before":
                p = f"{B}/clean/{n}_{k}.png" if k != "icon" else f"{B}/reduced/{n}_icon.png"
                if n == "migrate" and k == "back": p = f"{B}/reduced/migrate_back.png"
            else:
                h = f"{D}/hand/{n}_{k}.png"
                p = h if os.path.exists(h) else (f"{D}/clean/{n}_{k}.png" if k != "icon" else f"{D}/reduced/{n}_icon.png")
            im = icon(p) if k == "icon" else rgba(p)
            bg = PARTY if k == "icon" else GROUND
            s.paste(on(im, bg, 1), (x, y + 20)); s.paste(on(im, bg, 2), (x + im.width + 4, y + 20)); x += im.width * 3 + 14
        x += 20
        if side == "before": d.line((x - 18, y + 20, x - 18, y + RH - 10), fill=INK, width=2)
s.save(out); print(out, s.size)

"""T-452 SYMBOL sheet: all 28 forms -- today's front | new front, back, icon, each 1x and 2x; the new shiny front"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/tools")
from symlib import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import genshiny
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 15); FS = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
def ld(p, pal=None):
    im = Image.open(p)
    if pal: im.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    a = np.array(im.convert("RGBA")); a[np.array(im) == 0, 3] = 0; return Image.fromarray(a)
def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im); return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)
GB, PT = (205, 205, 172), (98, 156, 131)
P = json.load(open(D + "/picks.json")); pal = [tuple(c) for c in P["a"]["palette"]]
_, shiny = genshiny.make_shiny(pal + [(0, 0, 0)] * (16 - len(pal)))
CW, RH, per = 64 * 3 + 6 + 3 * (64 * 3 + 6) + 32 * 3 + 40, 240, 4
CW = 560
rows = (len(FORMS) + per - 1) // per
s = Image.new("RGB", (20 + per * (CW + 16), 70 + rows * RH), (236, 234, 226)); d = ImageDraw.Draw(s)
d.text((20, 12), "T-452 SYMBOL's 28 forms -- DRAFT, not in the ROM: today's front | new front, back (the front mirrored, eye out), icon (icon3) -- 1x and 2x; and the new shiny front (genshiny)", fill=(30, 30, 34), font=F)
d.text((20, 34), "one palette for all 28 (gMonPalette_Unown): CONTEXT's ramp, no accents; icons all in shared icon palette %d" % P["a"]["icon3"]["icon_palette"], fill=(30, 30, 34), font=FS)
for i, f in enumerate(FORMS):
    x = 20 + (i % per) * (CW + 16); y = 62 + (i // per) * RH
    d.text((x, y), "%s  (SPECIES_%s)" % (GLYPH[f], CONST[f]), fill=(30, 30, 34), font=F)
    ims = [(ld(f"{G}/{f}/front.png"), GB), (ld(f"{D}/reduced/{f}_front.png"), GB), (ld(f"{D}/reduced/{f}_back.png", pal), GB),
           (ld(f"{D}/reduced/{f}_icon.png").crop((0, 0, 32, 32)), PT), (ld(f"{D}/reduced/{f}_front.png", shiny), GB)]
    xx = x
    for j, (im, bg) in enumerate(ims):
        if j == 4:
            s.paste(on(im, bg, 1), (xx, y + 22)); d.text((xx, y + 90), "shiny", fill=(30, 30, 34), font=FS); break
        s.paste(on(im, bg, 1), (xx, y + 22)); s.paste(on(im, bg, 2), (xx, y + 22 + im.height + 4))
        xx += im.width * 2 + (6 if j else 0) + 8
        if j == 0: d.line((xx - 4, y + 22, xx - 4, y + RH - 8), fill=(30, 30, 34), width=2); xx += 6
s.save(W + "/sheets/t452sym_sheet.png"); print(W + "/sheets/t452sym_sheet.png", s.size, "shiny", shiny[:7])

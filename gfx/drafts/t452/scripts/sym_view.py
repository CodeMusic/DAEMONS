"""quick look: hand front, hand back, reduced front/back (3x), icon (4x), on the battle ground"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symlib import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
def ld(p, pal=None):
    im = Image.open(p)
    if im.mode == "P":
        if pal: im.putpalette(pal)
        a = np.array(im.convert("RGBA")); a[np.array(im) == 0, 3] = 0; return Image.fromarray(a)
    return im.convert("RGBA")
def on(im, s, bg=(205, 205, 172)):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im); return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)
out, forms = sys.argv[1], sys.argv[2:]
s = Image.new("RGB", (4 * 200 + 150, len(forms) * 215 + 10), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, f in enumerate(forms):
    y = 10 + i * 215; d.text((10, y), GLYPH[f], fill=(0, 0, 0), font=F)
    pal = Image.open(f"{D}/reduced/{f}_front.png").getpalette()
    ims = [(ld(f"{D}/hand/{f}_front.png"), 3), (ld(f"{D}/reduced/{f}_front.png"), 3), (ld(f"{D}/reduced/{f}_back.png", pal), 3)]
    for j, (im, sc) in enumerate(ims): s.paste(on(im, sc), (30 + j * 200, y + 18))
    s.paste(on(ld(f"{D}/reduced/{f}_icon.png").crop((0, 0, 32, 32)), 4, (98, 156, 131)), (30 + 3 * 200, y + 18))
s.save(out); print(out)

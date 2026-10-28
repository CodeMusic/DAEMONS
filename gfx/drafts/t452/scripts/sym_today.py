import sys; sys.path.insert(0, __import__("os").path.dirname(__file__))
from symlib import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
def ld(p, pal=None):
    im = Image.open(p)
    if pal: im.putpalette(pal)
    a = np.array(im.convert("RGBA")); a[np.array(im) == 0, 3] = 0; return Image.fromarray(a)
def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im); return b.convert("RGB").resize((im.width*s, im.height*s), Image.NEAREST)
s = Image.new("RGB", (7 * 300 + 20, 4 * 190 + 40), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, f in enumerate(FORMS):
    x = 10 + (i % 7) * 300; y = 30 + (i // 7) * 190
    d.text((x, y), GLYPH[f] + "  " + f, fill=(0,0,0), font=F)
    s.paste(on(ld(f"{G}/{f}/front.png"), (205,205,172), 2), (x, y+20))
    s.paste(on(ld(f"{G}/{f}/back.png"), (205,205,172), 2), (x+132, y+20))
    s.paste(on(ld(f"{G}/{f}/icon.png").crop((0,0,32,32)), (98,156,131), 1), (x+264, y+20))
s.save(sys.argv[1]); print(sys.argv[1])

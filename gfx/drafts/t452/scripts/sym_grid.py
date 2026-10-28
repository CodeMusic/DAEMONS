import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symlib import *
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 10)
out, f = sys.argv[1], sys.argv[2]; S = 8
im = Image.open(f"{D}/hand/{f}_front.png").convert("RGBA"); b = Image.new("RGBA", im.size, (205, 205, 172, 255)); b.alpha_composite(im)
s = Image.new("RGB", (64 * S + 40, 64 * S + 40), (236, 234, 226)); s.paste(b.convert("RGB").resize((64 * S, 64 * S), Image.NEAREST), (30, 30)); d = ImageDraw.Draw(s)
for v in range(0, 65, 4):
    c = (255, 0, 0) if v % 8 == 0 else (150, 150, 150)
    d.line((30 + v * S, 30, 30 + v * S, 30 + 64 * S), fill=c); d.line((30, 30 + v * S, 30 + 64 * S, 30 + v * S), fill=c)
    if v % 8 == 0 and v < 64: d.text((30 + v * S, 16), str(v), fill=(200, 0, 0), font=F); d.text((8, 30 + v * S), str(v), fill=(200, 0, 0), font=F)
s.save(out)

"""candidates: guide, then every draft, 160px, for the forms given"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symlib import *
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
out, forms = sys.argv[1], sys.argv[2:]
rows = [(f, ["src/%s_guide.png" % f] + sorted(x for x in os.listdir(D) if x.startswith(f + "_front") and x.endswith(".png"))) for f in forms]
n = max(len(r) for _, r in rows); s = Image.new("RGB", (10 + n * 170, len(rows) * 185 + 10), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, (f, fs) in enumerate(rows):
    for j, x in enumerate(fs):
        s.paste(Image.open(f"{D}/{x}").convert("RGB").resize((160, 160)), (10 + j * 170, 22 + i * 185))
        d.text((10 + j * 170, 8 + i * 185), GLYPH[f] + " " + os.path.basename(x)[:-4].replace(f + "_", ""), fill=(0, 0, 0), font=F)
s.save(out); print(out)

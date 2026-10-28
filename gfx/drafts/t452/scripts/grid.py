"""a 64-grid (clean / hand / reduced) at 5x with a coordinate grid, beside its coloured reduction.  grid.py OUT FILE..."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 10)
out, items = sys.argv[1], sys.argv[2:]
S = 5; s = Image.new("RGB", (len(items) * (64 * S + 30) + 10, 64 * S + 40), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, p in enumerate(items):
    im = Image.open(p)
    if im.mode == "P":
        a = np.array(im.convert("RGBA")); a[np.array(im) == 0, 3] = 0; im = Image.fromarray(a)
    im = im.convert("RGBA").crop((0, 0, 64, 64)) if im.height > 64 and "--bottom" not in p else im.convert("RGBA")
    b = Image.new("RGBA", im.size, (205, 205, 172, 255)); b.alpha_composite(im)
    x0 = 25 + i * (64 * S + 30); s.paste(b.convert("RGB").resize((64 * S, 64 * S), Image.NEAREST), (x0, 25))
    d.text((x0, 2), os.path.basename(p), fill=(0, 0, 0), font=F)
    for v in range(0, 65, 4):
        c = (255, 0, 0) if v % 8 == 0 else (170, 170, 170)
        d.line((x0 + v * S, 25, x0 + v * S, 25 + 64 * S), fill=c); d.line((x0, 25 + v * S, x0 + 64 * S, 25 + v * S), fill=c)
        if v % 8 == 0 and v < 64: d.text((x0 + v * S + 1, 14), str(v), fill=(200, 0, 0), font=F); d.text((x0 - 18, 25 + v * S), str(v), fill=(200, 0, 0), font=F)
s.save(out); print(out)

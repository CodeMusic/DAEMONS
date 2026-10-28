"""batch 6: a clean grid at 8x with a coordinate grid every 4 cells (labels every 8), to place hand edits"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
T = os.environ["T452_ROOT"] + "/i"; F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 10)
out, items = sys.argv[1], sys.argv[2:]
S = 8; s = Image.new("RGB", (len(items) * (64 * S + 30) + 10, 64 * S + 40), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, it in enumerate(items):
    n, k = it.split(":"); h = f"{T}/hand/{n}_{k}.png"; p = h if os.path.exists(h) else f"{T}/clean/{n}_{k}.png"
    im = Image.open(p).convert("RGBA"); b = Image.new("RGBA", im.size, (205, 205, 172, 255)); b.alpha_composite(im)
    x0 = 25 + i * (64 * S + 30); s.paste(b.convert("RGB").resize((64 * S, 64 * S), Image.NEAREST), (x0, 25))
    d.text((x0, 2), it, fill=(0, 0, 0), font=F)
    for v in range(0, 65, 4):
        c = (255, 0, 0) if v % 8 == 0 else (150, 150, 150)
        d.line((x0 + v * S, 25, x0 + v * S, 25 + 64 * S), fill=c, width=1); d.line((x0, 25 + v * S, x0 + 64 * S, 25 + v * S), fill=c, width=1)
        if v % 8 == 0 and v < 64: d.text((x0 + v * S + 1, 14), str(v), fill=(200, 0, 0), font=F); d.text((x0 - 18, 25 + v * S), str(v), fill=(200, 0, 0), font=F)
s.save(out); print(out)

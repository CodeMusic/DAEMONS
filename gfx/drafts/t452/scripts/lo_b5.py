"""batch 5: the redrafts (charmlo, charmback) for NAMES side by side, to choose from"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
D = os.environ["T452_ROOT"] + "/h"; F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
out, names = sys.argv[1], sys.argv[2:]
rows = [[f for f in sorted(os.listdir(D)) if f.startswith(n + "_") and f.endswith(".png") and any(s in f for s in ("_5323", "_5324", "_5303", "_5304", "fromfront"))] for n in names]
s = Image.new("RGB", (max(len(r) for r in rows) * 170 + 10, len(rows) * 190), (236, 234, 226)); d = ImageDraw.Draw(s)
for j, r in enumerate(rows):
    for i, f in enumerate(r):
        s.paste(Image.open(f"{D}/{f}").convert("RGB").resize((160, 160)), (5 + i * 170, 5 + j * 190)); d.text((5 + i * 170, 168 + j * 190), f[:28], fill=0, font=F)
s.save(out); print(out)

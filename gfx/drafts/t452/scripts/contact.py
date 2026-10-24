"""contact.py OUT.png PATTERN... -- every draft matching, at 192px with its file name, to choose from."""
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
fs = sorted(f for p in sys.argv[2:] for f in glob.glob(p))
try: F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
except Exception: F = ImageFont.load_default()
C = 6; S = 192
s = Image.new("RGB", (C * (S + 8) + 8, ((len(fs) + C - 1) // C) * (S + 24) + 8), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, f in enumerate(fs):
    x, y = 8 + (i % C) * (S + 8), 8 + (i // C) * (S + 24)
    s.paste(Image.open(f).convert("RGB").resize((S, S), Image.LANCZOS), (x, y))
    d.text((x, y + S + 4), os.path.basename(f)[:30], fill=(30, 30, 34), font=F)
s.save(sys.argv[1]); print(len(fs), "->", sys.argv[1])

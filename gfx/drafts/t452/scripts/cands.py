"""candidates by prefix: every draft at 192px, labelled.   cands.py OUT PREFIX..."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
D = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452forms_work/z"
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
out, pre = sys.argv[1], sys.argv[2:]
rows = [(p, sorted(f for f in os.listdir(D) if f.startswith(p) and f.endswith(".png"))) for p in pre]
W = 10 + max(len(f) for _, f in rows) * 202
s = Image.new("RGB", (W, len(rows) * 220 + 10), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, (p, fs) in enumerate(rows):
    for j, f in enumerate(fs):
        x, y = 10 + j * 202, 10 + i * 220
        s.paste(Image.open(f"{D}/{f}").convert("RGB").resize((192, 192)), (x, y + 16)); d.text((x, y), f[:-4], fill=(0, 0, 0), font=F)
s.save(out); print(out)

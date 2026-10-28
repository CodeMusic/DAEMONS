"""batch 15: candidates for several daemons on one sheet (today front/back, then every draft at 128px), to choose by eye.
    grp14.py OUT NAME..."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
T = os.environ["T452_ROOT"] + "/t"; R = "/Users/christopherhicks/Projects/DAEMONS"; F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
out, names = sys.argv[1], sys.argv[2:]
rows = []
for n in names:
    fs = sorted(f for f in os.listdir(T) if f.startswith(n + "_") and f.endswith(".png"))
    rows.append((n, fs))
W = 10 + (2 + max(len(f) for _, f in rows)) * 138
s = Image.new("RGB", (W, len(rows) * 160 + 10), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, (n, fs) in enumerate(rows):
    y = 10 + i * 160
    for j, k in enumerate(("front", "back")):
        im = Image.open(f"{R}/gfx/daemons/{n}_{k}.png").convert("RGBA"); b = Image.new("RGBA", im.size, (205, 205, 172, 255)); b.alpha_composite(im)
        s.paste(b.convert("RGB").resize((128, 128), Image.NEAREST), (10 + j * 138, y + 14)); d.text((10 + j * 138, y), n + " today " + k, fill=(0, 0, 0), font=F)
    for j, f in enumerate(fs):
        x = 10 + (j + 2) * 138
        s.paste(Image.open(f"{T}/{f}").convert("RGB").resize((128, 128)), (x, y + 14)); d.text((x, y), f.replace(n + "_", "")[:-4], fill=(0, 0, 0), font=F)
s.save(out); print(out)

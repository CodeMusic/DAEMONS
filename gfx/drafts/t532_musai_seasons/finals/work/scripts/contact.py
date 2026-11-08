"""contact.py KIND OUT [NAME...]: raw drafts of KIND (front/back/icon), both seeds, 192px each, a row per form."""
import sys, os, glob
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kind, out, names = sys.argv[1], sys.argv[2], sys.argv[3:]
fs = sorted(glob.glob("%s/raw/*_%s_*.png" % (HERE, kind)))
fs = [f for f in fs if not names or os.path.basename(f).split("_")[0] in names]
rows = {}
for f in fs:
    b = os.path.basename(f)[:-4].split("_"); rows.setdefault("_".join(b[:2]), []).append(f)
S = 192; W = 4 * S
keys = list(rows)
sh = Image.new("RGB", (W, ((len(keys) + 1) // 2) * (S + 14)), (236, 234, 226)); d = ImageDraw.Draw(sh)
for i, k in enumerate(keys):
    x = (i % 2) * 2 * S; y = (i // 2) * (S + 14)
    d.text((x + 2, y), k, fill=(170, 40, 40))
    for j, f in enumerate(rows[k][:2]):
        sh.paste(Image.open(f).convert("RGB").resize((S, S)), (x + j * S, y + 12))
sh.save(out); print(out, sh.size)

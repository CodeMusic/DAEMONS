"""peek.py KIND OUT [KEY...]: per form a row of raw drafts (160px) with each one's cleandraft result at 2x and 1x beneath."""
import glob, os, subprocess, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keyed import keyed
from PIL import Image, ImageDraw
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3"); R = "/Users/christopherhicks/Projects/DAEMONS"
kind, out, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
rows = {}
for f in sorted(glob.glob("%s/raw/*_%s_*.png" % (W, kind))):
    b = os.path.basename(f)[:-4].split("_"); k = "_".join(b[:2])
    if not keys or k in keys: rows.setdefault(k, []).append(f)
os.makedirs(W + "/peek", exist_ok=True)
S = 160; C = 200; n = max(len(v) for v in rows.values())
sh = Image.new("RGB", (n * C + 8, len(rows) * (S + 150)), (236, 234, 226)); d = ImageDraw.Draw(sh)
for i, (k, fs) in enumerate(rows.items()):
    y = i * (S + 150)
    for j, f in enumerate(fs):
        x = 4 + j * C; seed = f[-8:-4]
        sh.paste(Image.open(f).convert("RGB").resize((S, S)), (x, y + 14))
        cl = "%s/peek/%s" % (W, os.path.basename(f))
        kf = keyed(f, cl[:-4] + "_key.png", (200, 0, 200) if k in ("seekmusai_autumn", "lensmusai_autumn", "maskmusai_autumn") else (0, 200, 0))
        r = subprocess.run([PY, R + "/tools/cleandraft.py", kf, cl], capture_output=True, text=True)
        m = re.search(r"(\d+) shadow", r.stdout); worn = m.group(1) if m else "?"
        d.text((x, y), "%s %s worn %s" % (k, seed, worn), fill=(170, 40, 40))
        if os.path.exists(cl):
            im = Image.open(cl).convert("RGBA"); bg = Image.new("RGBA", im.size, (205, 205, 172, 255)); bg.alpha_composite(im)
            bg = bg.convert("RGB"); sh.paste(bg.resize((128, 128), Image.NEAREST), (x, y + 18 + S)); sh.paste(bg, (x + 130, y + 18 + S))
sh.save(out); print(out, sh.size)

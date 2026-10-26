"""T-452 round two's one-page overview: every daemon drafted this round, in ROM today | the draft, front / back / icon,
at 1x and 2x. Part A's eight (r/), MANIFOLD A (e/) and B (m/), batch 2's twenty (e/).

    combined_r2.py OUT.png"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheet_r2 import show, on, readpal, BY, G, T, F, FS, PAPER, INK, GROUND, PARTY
from PIL import Image, ImageDraw
items = [(n, "r", "A: " + w) for n, w in (("rovercub", "ground off"), ("locus", "new back"), ("relay", "bigger back"),
         ("buffer", "bigger back"), ("roverseer", "icon"), ("indexer", "icon"), ("injector", "icon"), ("crawler", "icon"))]
items += [("manifold", "e", "MANIFOLD A"), ("manifold", "m", "MANIFOLD B")]
C = json.load(open(T + "/e/choose.json"))
for n in "worm outbreak surge sector partition fork thread scheduler branch predictor pipeline anomaly outlier flicker overrun suspend hibernate echo tracer sprawl".split():
    items.append((n, "e", (("LOST KEY " if C[n]["failed"].startswith("front") else "FLAGGED ") if C[n].get("failed") else "") + "batch 2"))
CW, RH, per = 3 * (64 * 2 + 70) + 32 * 2 + 40 + 40, 232, 3
rows = (len(items) + per - 1) // per
s = Image.new("RGB", (20 + per * (CW + 20), 50 + rows * RH), PAPER); d = ImageDraw.Draw(s)
d.text((20, 14), "T-452 round two -- DRAFT, not in the ROM: in ROM front | draft front, back, icon (1x and 2x)", fill=INK, font=F)
for i, (n, dd, lab) in enumerate(items):
    v = BY[n]; rom = G + v["constant"].lower(); npal = readpal(rom + "/normal.pal")
    x = 20 + (i % per) * (CW + 20); y = 46 + (i // per) * RH
    d.text((x, y), "%d %s  (%s)" % (v["national"], v["name"], lab), fill=INK, font=FS)
    nd = f"{T}/{dd}/reduced/{n}_"
    def pick(k):
        return nd + k + ".png" if os.path.exists(nd + k + ".png") else None
    fp = pick("front"); fpal = None
    if fp:
        p = Image.open(fp).getpalette()[:48]; fpal = [tuple(p[j:j + 3]) for j in range(0, 48, 3)]
    ims = [(show(rom + "/front.png", npal), GROUND),
           (show(fp, None) if fp else show(rom + "/front.png", npal), GROUND),
           (show(pick("back"), fpal) if pick("back") else show(rom + "/back.png", npal), GROUND),
           (show(pick("icon"), None, 32) if pick("icon") else show(rom + "/icon.png", None, 32), PARTY)]
    xx = x
    for j, (im, bg) in enumerate(ims):
        s.paste(on(im, bg, 1), (xx, y + 20)); s.paste(on(im, bg, 2), (xx, y + 20 + im.height + 4))
        xx += im.width * 2 + (30 if j == 0 else 8)
        if j == 0: d.line((xx - 16, y + 20, xx - 16, y + RH - 10), fill=INK, width=2)
s.save(sys.argv[1]); print(sys.argv[1], s.size)

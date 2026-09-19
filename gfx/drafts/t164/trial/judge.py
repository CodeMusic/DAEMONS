#!/usr/bin/env python3
"""T-164's trial, judged at the GBA's own scale: each draft sampled back to art pixels (the 8px grid's block centres),
reduced to one 15-colour palette (a tileset palette is 16 with a transparent), and -- for ground -- the 16x16 crop that
tiles best, repeated 3x3 so a seam shows. Writes sheet.png and prints the numbers."""
import numpy as np
from PIL import Image, ImageDraw
T = "gfx/drafts/t164/trial"
def native(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(int); h, w = a.shape[0] // 8, a.shape[1] // 8
    return np.array([[np.median(a[y*8+2:y*8+6, x*8+2:x*8+6].reshape(-1, 3), axis=0) for x in range(w)] for y in range(h)]).astype(np.uint8)
def q15(a):
    im = Image.fromarray(a).quantize(15, method=Image.MEDIANCUT); return np.asarray(im.convert("RGB"))
def seam(t):  # mean colour jump across the wrap edges of a tile, against the mean jump inside it
    wrapx = np.abs(t[:, 0].astype(int) - t[:, -1].astype(int)).mean(); wrapy = np.abs(t[0].astype(int) - t[-1].astype(int)).mean()
    inside = (np.abs(np.diff(t.astype(int), axis=0)).mean() + np.abs(np.diff(t.astype(int), axis=1)).mean()) / 2
    return (wrapx + wrapy) / 2 / max(inside, 1)
rows = []
for name in ["ground_1917", "ground_42", "ground_88", "ground_i2i_35", "ground_i2i_50", "ground_i2i_65", "ground_i2i_80", "ref_ground",
             "house_1917", "house_42", "house_88", "house_i2i_35", "house_i2i_50", "house_i2i_65", "house_i2i_80", "ref_house"]:
    a = np.asarray(Image.open("%s/%s.png" % (T, name)).convert("RGB")) if name.startswith("ref") else native("%s/%s.png" % (T, name))
    cols = len({tuple(c) for c in a.reshape(-1, 3)}); qa = q15(a)
    extra = None
    if name.startswith("ground") or name == "ref_ground":
        best = min(((seam(qa[y:y+16, x:x+16]), y, x) for y in range(0, qa.shape[0] - 15) for x in range(0, qa.shape[1] - 15)), default=None)
        if best:
            s, y, x = best; extra = np.tile(qa[y:y+16, x:x+16], (3, 3, 1)); rows.append((name, a, qa, extra, "%d colours, best 16x16 seam ratio %.2f" % (cols, s))); continue
    rows.append((name, a, qa, extra, "%d colours" % cols))
S = 3; W = 64 * S
sh = Image.new("RGB", (4 * (W + 10), len(rows) * (W + 16)), (40, 40, 44)); d = ImageDraw.Draw(sh)
for i, (n, a, qa, ex, note) in enumerate(rows):
    y = i * (W + 16); d.text((4, y + 2), "%s -- %s" % (n, note), fill=(230, 230, 230))
    for j, img in enumerate([a, qa, ex]):
        if img is None: continue
        im = Image.fromarray(img); f = min(W / im.width, W / im.height)
        sh.paste(im.resize((int(im.width * f), int(im.height * f)), Image.NEAREST), (j * (W + 10), y + 14))
    print("%-16s %s" % (n, note))
sh.save("%s/sheet.png" % T)

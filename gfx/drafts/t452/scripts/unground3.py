"""T-452 batch 3: a baked ground (an ellipse, strip or mound under the feet) off a REDUCED 4bpp sprite, in place.

    unground3.py PNG [--lo=0.70] [--minL=95] [--pal=FRONT.png] [--out=OUT.png] [--dark]

round2.unground's rule on the reduced grid: flood from the transparent ground through cells in the lowest part of
the figure (below LO of its height) that are pale (value >= minL), starting only from cells that touch
transparency; the figure is sealed by its outline, so the flood stops at the feet. --dark floods every non-outline
colour instead of only pale ones (a dark mound, WIRETAP). A foot whose sole was the ground gets an outline cell.
A back is indexed against its front's palette (--pal)."""
import sys
import numpy as np
from PIL import Image
opt = {a.split("=", 1)[0][2:]: (a.split("=", 1)[1] if "=" in a else True) for a in sys.argv[1:] if a.startswith("--")}
src = [a for a in sys.argv[1:] if not a.startswith("--")][0]
im = Image.open(src); g = np.array(im)
pal = np.array((Image.open(opt["pal"]) if "pal" in opt else im).getpalette()[:48]).reshape(16, 3).astype(int)
H = 64; a = g[:H]; op = a > 0
L = (pal[:, 0] * 299 + pal[:, 1] * 587 + pal[:, 2] * 114) // 1000
Lc = L[a]
ys = np.where(op.any(1))[0]; y0, y1 = ys.min(), ys.max()
lo = y0 + int((y1 - y0) * float(opt.get("lo", 0.70)))
ink = Lc < 60
cand = op & ((~ink) if opt.get("dark") else (Lc >= int(opt.get("minL", 95))))
cand[:lo] = False
seen = np.zeros(op.shape, bool); st = []
for y, x in zip(*np.where(cand)):
    if any(0 <= y + dy < H and 0 <= x + dx < 64 and not op[y + dy, x + dx] for dy, dx in ((1, 0), (0, 1), (0, -1))) or y == H - 1:
        seen[y, x] = True; st.append((y, x))
while st:
    y, x = st.pop()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        p, q = y + dy, x + dx
        if 0 <= p < H and 0 <= q < 64 and cand[p, q] and not seen[p, q]: seen[p, q] = True; st.append((p, q))
#  outline cells now standing alone below the figure (the ground's own rim) go too
rim = op & ink & ~seen
for _ in range(0 if opt.get("norim") else 2):
    lone = np.zeros_like(rim)
    for y, x in zip(*np.where(rim)):
        if y < lo: continue
        nb = [(y + dy, x + dx) for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        body = sum(1 for p, q in nb if 0 <= p < H and 0 <= q < 64 and op[p, q] and not seen[p, q] and not (ink[p, q]))
        if body == 0 and not any(0 <= p < H and 0 <= q < 64 and op[p, q] and not seen[p, q] and ink[p, q] and p < y for p, q in nb):
            lone[y, x] = True
    seen |= lone; rim &= ~lone
darkest = int(np.argmin(np.where(np.arange(16) > 0, L, 999)))
sole = seen & np.roll(op & ~seen & ~ink, 1, 0)
a[seen] = 0; a[sole] = darkest
g[:H] = a
out = Image.fromarray(g.astype(np.uint8), "P"); out.putpalette(im.getpalette()); out.info.update(im.info)
if "transparency" in im.info: out.save(opt.get("out", src), transparency=im.info["transparency"])
else: out.save(opt.get("out", src))
print(src.split("/")[-1], "ground cells removed:", int(seen.sum()))

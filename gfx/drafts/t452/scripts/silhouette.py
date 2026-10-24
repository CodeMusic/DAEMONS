"""silhouette.py CLEAN_FRONT.png OUT_512.png -- point 4's image-to-image source for a back.

The chosen front, cleaned to its 64 grid, MIRRORED, and flattened: every drawn pixel mid grey, its edge ink, no
face, no eye, nothing that says which way it looks. The model is then given only a shape the size and stance of
the front, and the prompt says it is the back."""
import sys
import numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert("RGBA"))[:, ::-1]
op = a[..., 3] > 127
edge = op & ~(np.roll(op, 1, 0) & np.roll(op, -1, 0) & np.roll(op, 1, 1) & np.roll(op, -1, 1))
g = np.full(op.shape + (3,), 255, np.uint8)
g[op] = (128, 128, 132)
#  a lighter crown and a darker underside, so the shape reads as a round body and not a flat cut-out
ys = np.where(op.any(1))[0]; h = ys.max() - ys.min() + 1
for y in ys:
    t = (y - ys.min()) / h
    row = op[y] & ~edge[y]
    g[y][row] = (int(150 - 50 * t),) * 3
g[edge] = (24, 24, 28)
Image.fromarray(g).resize((512, 512), Image.NEAREST).save(sys.argv[2])
print("silhouette", int(op.sum()), "px ->", sys.argv[2])

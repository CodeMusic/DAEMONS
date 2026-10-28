"""batch 10: a t2i draft the model framed (seed 5802 drew a box round every one): everything within M px of the edge
painted white, so the white ground floods from the edges again. Writes n/src/<file>_unframed.png."""
import os, sys
import numpy as np
from PIL import Image
D = os.environ["T452_ROOT"] + "/n"
for f in sys.argv[1:]:
    a = np.array(Image.open(f"{D}/{f}").convert("RGB")).astype(int); h, w = a.shape[:2]
    # the frame: walk in from each edge while the row/column is not near-white-dominated
    def depth(lines):
        for i, l in enumerate(lines):
            if (l.min(-1) > 225).mean() > 0.6: return i
        return 24
    t = depth([a[i] for i in range(40)]); b = depth([a[h - 1 - i] for i in range(40)])
    l = depth([a[:, i] for i in range(40)]); r = depth([a[:, w - 1 - i] for i in range(40)])
    M = max(t, b, l, r) + 4
    a[:M] = 255; a[-M:] = 255; a[:, :M] = 255; a[:, -M:] = 255
    #  then the ground itself, where it is an off-white the key flood (> 225) would stop at: flooded from the edges
    #  through near-grey cells brighter than 205, painted white
    from collections import deque
    g = (a.min(-1) > 205) & (a.max(-1) - a.min(-1) < 16); seen = np.zeros(g.shape, bool); q = deque()
    for y in range(h):
        for x in range(w):
            if (y in (0, h - 1) or x in (0, w - 1)) and g[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p_, r_ = y + dy, x + dx
            if 0 <= p_ < h and 0 <= r_ < w and g[p_, r_] and not seen[p_, r_]: seen[p_, r_] = True; q.append((p_, r_))
    a[seen] = 255
    out = f"src/{f[:-4]}_unframed.png"; Image.fromarray(a.astype(np.uint8)).save(f"{D}/{out}"); print(f, "frame", (t, b, l, r), "->", out)

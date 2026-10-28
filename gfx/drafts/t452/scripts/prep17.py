"""batch 12 (batch 17 copy, dir s): a t2i draft the model framed (seed 5802 drew a box round every one): everything within M px of the edge
painted white, so the white ground floods from the edges again. Writes n/src/<file>_unframed.png."""
import os, sys
import numpy as np
from PIL import Image
D = os.environ["T452_ROOT"] + "/v"
FLAT = "--flat" in sys.argv; FF = "--frameflat" in sys.argv   # FF: a frame round a flat coloured ground (OLDBRANCH 5904)
for f in [x for x in sys.argv[1:] if not x.startswith("--")]:
    a = np.array(Image.open(f"{D}/{f}").convert("RGB")).astype(int); h, w = a.shape[:2]
    # the frame: walk in from each edge while the row/column is not near-white-dominated
    def depth(lines):
        for i, l in enumerate(lines):
            if (l.min(-1) > 225).mean() > 0.6: return i
        return 24
    t = depth([a[i] for i in range(40)]); b = depth([a[h - 1 - i] for i in range(40)])
    l = depth([a[:, i] for i in range(40)]); r = depth([a[:, w - 1 - i] for i in range(40)])
    M = max(t, b, l, r) + 4
    if FLAT: M = 0; bgc = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), 0)
    else:
        if FF: M = 12; k = M + 2; bgc = np.median(np.concatenate([a[k, k:-k], a[-k - 1, k:-k], a[k:-k, k], a[k:-k, -k - 1]]), 0)
        a[:M] = 255; a[-M:] = 255; a[:, :M] = 255; a[:, -M:] = 255
    #  then the ground itself, where it is an off-white the key flood (> 225) would stop at: flooded from the edges
    #  through near-grey cells brighter than 205, painted white
    from collections import deque
    g = (a.min(-1) > 205) & (a.max(-1) - a.min(-1) < 16)
    if FLAT: g = np.abs(a - bgc).max(-1) < 16
    if FF: g = (np.abs(a - bgc).max(-1) < 24) | (a.min(-1) > 250)
    seen = np.zeros(g.shape, bool); q = deque()
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

#  batch 12 (batch 17 copy, dir s): a flat coloured (not white) ground, as COMFORT's 5901 drew (grey ~175): `prep11.py --flat FILE...` floods
#  from the edges through cells within 16 of the corner's colour and paints them white

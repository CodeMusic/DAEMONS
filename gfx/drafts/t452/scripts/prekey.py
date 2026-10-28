"""a draft whose ground is an off-white near its own white body: the ground flooded from the edges through cells within
TOL (per channel) of the corners' median colour, painted chroma green, so cleandraft keys it and keeps the white body.
    prekey.py FILE [--tol=10]   -> z/src/<file>_key.png"""
import sys, numpy as np
from collections import deque
from PIL import Image
D = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452forms_work/z"
tol = int(([a.split("=")[1] for a in sys.argv if a.startswith("--tol=")] or [10])[0])
for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
    a = np.array(Image.open(f"{D}/{f}").convert("RGB")).astype(int); h, w = a.shape[:2]
    bg = np.median(np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)]), 0)
    g = np.abs(a - bg).max(-1) <= tol
    seen = np.zeros((h, w), bool); q = deque()
    for y in range(h):
        for x in range(w):
            if (y in (0, h - 1) or x in (0, w - 1)) and g[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, r = y + dy, x + dx
            if 0 <= p < h and 0 <= r < w and g[p, r] and not seen[p, r]: seen[p, r] = True; q.append((p, r))
    a[seen] = (0, 200, 0)
    out = f"src/{f[:-4]}_key.png"; Image.fromarray(a.astype(np.uint8)).save(f"{D}/{out}"); print(f, "bg", bg, "->", out, seen.mean())

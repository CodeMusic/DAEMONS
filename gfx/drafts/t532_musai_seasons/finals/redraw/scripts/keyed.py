"""keyed(src, dst): t452's batch.keyed -- the white ground flooded from the edges is painted chroma green (0,200,0), so
cleandraft takes it as a KEY ground and skips the black-shadow wear that ate the tyres, skis and track."""
from collections import deque
import numpy as np
from PIL import Image


def keyed(src, dst, key=(0, 200, 0)):
    a = np.array(Image.open(src).convert("RGB")).astype(int); h, w = a.shape[:2]
    white = (a.min(2) > 225) & (a.max(2) - a.min(2) < 20)
    seen = np.zeros((h, w), bool); q = deque()
    for y in range(h):
        for x in range(w):
            if (y in (0, h - 1) or x in (0, w - 1)) and white[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, r = y + dy, x + dx
            if 0 <= p < h and 0 <= r < w and white[p, r] and not seen[p, r]: seen[p, r] = True; q.append((p, r))
    a[seen] = key
    Image.fromarray(a.astype(np.uint8)).save(dst)
    return dst

#!/usr/bin/env python3
"""Sample generated art on the grid it was drawn on, instead of its pixels.

Shared by gbasprite.py (daemons) and gbachar.py (characters), because both
take the same input: a Gemini drawing exported as JPEG, since there is no PNG
export. See vision 9.4.
"""
import numpy as np

def deringe(a):
    """Undo JPEG on generated pixel art by sampling the grid it was drawn on.

    Gemini renders at about 100 logical pixels and upscales to 1024, so every
    logical pixel is a ~10px block -- and JPEG ringing lives at BLOCK EDGES.
    Taking the median of each block's centre never reads the ringing at all,
    which matters because there is no PNG export: the tolerance band between
    body grey and marking colour was a workaround for damage we can simply
    decline to sample.

    Falls through unchanged if no regular grid is found -- hand-drawn or
    already-clean art is not on one."""
    d = np.abs(np.diff(a, axis=1)).sum(axis=(0, 2)).astype(float)
    d -= d.mean()
    lags = [(float((d[:-l] * d[l:]).sum()), l) for l in range(4, 40)]
    score, pitch = max(lags)
    if score <= 0:
        return a
    h, w = a.shape[:2]
    ny, nx = h // pitch, w // pitch
    if ny < 24 or nx < 24:                       # not a grid we can trust
        return a
    out = np.zeros((ny, nx, 3), dtype=int)
    k = max(1, pitch // 4)                       # the inner half of each block
    for j in range(ny):
        for i in range(nx):
            cy, cx = j * pitch + pitch // 2, i * pitch + pitch // 2
            blk = a[max(0, cy-k):cy+k+1, max(0, cx-k):cx+k+1].reshape(-1, 3)
            out[j, i] = np.median(blk, axis=0)
    return out


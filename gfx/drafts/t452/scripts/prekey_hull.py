"""prekey for a white body whose outline is broken (OVERLOADED rainy 6922): the figure is everything not near the ground
colour (> 18 off), closed with a disc of R px and its holes filled; outside it is painted chroma green.
    prekey_hull.py FILE [--r=20]  -> z/src/<file>_key.png"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
D = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452forms_work/z"
r = int(([a.split("=")[1] for a in sys.argv if a.startswith("--r=")] or [20])[0])
for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
    a = np.array(Image.open(f"{D}/{f}").convert("RGB")).astype(int)
    bg = np.median(np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3)]), 0)
    fig = np.abs(a - bg).max(-1) > 18
    fig = nd.binary_opening(fig, np.ones((5, 5)))          # specks off
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; disc = yy ** 2 + xx ** 2 <= r * r
    m = nd.binary_fill_holes(nd.binary_closing(np.pad(fig, r), disc)[r:-r, r:-r])
    lab, n = nd.label(m); sizes = nd.sum(m, lab, range(1, n + 1)); m = lab == (1 + int(np.argmax(sizes)))
    a[~m] = (0, 200, 0)
    out = f"src/{f[:-4]}_key.png"; Image.fromarray(a.astype(np.uint8)).save(f"{D}/{out}"); print(f, "->", out, (~m).mean())

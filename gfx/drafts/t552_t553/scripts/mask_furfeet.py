"""T-553: MASKMUSAI winter -- the model will draw skis or ordinary feet, never ski-shaped feet; so take a skis draft and
turn the skis into fur in code: each ski pixel (the cool metal below the body) becomes the body's own fur ramp by its
lightness, keeping the black outline. Writes <seed>_furfeet.png beside the source."""
import sys
import numpy as np
from PIL import Image
D = "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t552_t553/round3/"
for seed in sys.argv[1:]:
    a = np.array(Image.open(D + "maskmusai_winter_%s.png" % seed).convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    L = (r + g + b) / 3
    H = a.shape[0]
    yy = np.arange(H)[:, None].repeat(a.shape[1], 1)
    metal = (yy > H * 0.62) & (b - r > 6) & (L > 60) & (L < 250)
    # the body's fur ramp, from the furry body above
    fur = a[(yy > H * 0.45) & (yy < H * 0.62) & (abs(r - b) < 6) & (L > 70) & (L < 245)]
    ramp = sorted(map(tuple, fur), key=sum)
    if not ramp: continue
    out = a.copy()
    for y, x in zip(*np.nonzero(metal)):
        t = (L[y, x] - 60) / 190.0
        out[y, x] = ramp[min(len(ramp) - 1, int(t * (len(ramp) - 1)))]
    Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(D + "maskmusai_winter_%s_furfeet.png" % seed)
    print(seed, int(metal.sum()), "pixels turned to fur")

"""T-553: MUSAI is NORMAL (hue 40), and gbasprite's shift_off turns any accent within 40 degrees of that to blue, so orange
leaves cannot reach the ROM. Its autumn leaves become red maple (356 degrees, kept as drawn), two-toned: each leaf pixel
with no leaf above it takes the bright red, so the front carries both reds and the back's bright leaves keep theirs
(the back draws through the front's palette). Rewrites reduced/musai_autumn.png and .pal in place."""
import colorsys
import numpy as np
from PIL import Image
D = "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t552_t553/reduced/"
im = Image.open(D + "musai_autumn.png"); g = np.array(im); p = im.getpalette()
def red(c):
    h, s, v = colorsys.rgb_to_hsv(*[x / 255 for x in c]); return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(356 / 360, max(s, 0.8), v))
for i in (6, 7): p[3*i:3*i+3] = red(tuple(p[3*i:3*i+3]))
leaf = g == 7; top = leaf & ~np.vstack([np.zeros((1, 64), bool), leaf[:-1]])
g[top] = 6
out = Image.fromarray(g.astype(np.uint8), "P"); out.putpalette(p); out.info["transparency"] = 0; out.save(D + "musai_autumn.png", transparency=0)
open(D + "musai_autumn.pal", "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(p[3*i:3*i+3]) for i in range(16)))
print("bright", int(top.sum()), "dark", int((leaf & ~top).sum()), p[18:24])

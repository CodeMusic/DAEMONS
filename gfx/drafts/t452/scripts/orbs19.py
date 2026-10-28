"""batch 19: SINGLETON's and PAIRWISE's fronts composed at 512 from the one draft that drew ONE eye (singleton_icon_6741,
its grey ground flooded off by prep19 --flat). The orb is cut to its fitted circle and given an ink ring (its pale top
rim would otherwise flood away with the white ground); SINGLETON is the orb at 78%; PAIRWISE is two of it at 56%, side by
side and overlapping, the right one in front with a seam (its ring) -- two of the line's one, fused.
Writes x/src/singleton_orb.png and x/src/pairwise_orbs.png."""
import os, numpy as np
from PIL import Image, ImageDraw
D = os.environ["T452_ROOT"] + "/x"
a = np.array(Image.open(D + "/src/singleton_icon_6741_unframed.png").convert("RGB")).astype(int)
nw = a.min(-1) < 235; ys, xs = np.where(nw)
cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2; r = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2
yy, xx = np.mgrid[:512, :512]; inside = (xx - cx) ** 2 + (yy - cy) ** 2 <= (r - 2) ** 2
rgba = np.zeros((512, 512, 4), np.uint8); rgba[..., :3] = a; rgba[..., 3] = inside * 255
orb = Image.fromarray(rgba).crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r)))
d = ImageDraw.Draw(orb); d.ellipse((2, 2, orb.width - 3, orb.height - 3), outline=(28, 28, 34, 255), width=12)
def place(scale, centres):
    out = Image.new("RGBA", (512, 512), (255, 255, 255, 255)); s = int(512 * scale); o = orb.resize((s, s), Image.LANCZOS)
    for x, y in centres: out.alpha_composite(o, (int(x - s / 2), int(y - s / 2)))
    return out.convert("RGB")
place(0.78, [(256, 262)]).save(D + "/src/singleton_orb.png")
place(0.56, [(170, 270), (342, 270)]).save(D + "/src/pairwise_orbs.png")
print("orb centre", cx, cy, "r", r)

"""T-452 SYMBOL: a guide image per form for image-to-image -- the glyph as a chunky grey body (Arial Rounded Bold,
thickened), one big eye where the stroke is widest (the family's one eye, as today's), two stubby feet under it.
The model repaints this as a creature; the guide keeps the letter, which text alone never would."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symlib import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 400)
os.makedirs(D + "/src", exist_ok=True)
def make(f, out):
    g = GLYPH[f]; m = Image.new("L", (512, 512), 0); d = ImageDraw.Draw(m)
    bb = d.textbbox((0, 0), g, font=FONT); w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((512 - w) // 2 - bb[0], (470 - h) // 2 - bb[1] - 10), g, font=FONT, fill=255)
    a = np.array(m) > 127
    a = ndi.binary_dilation(a, iterations=12)
    ys, xs = np.where(a); y1 = ys.max()
    # feet: two stubby ovals under the lowest strokes
    bot = xs[ys >= y1 - 6]; cx = int(np.median(bot)); span = bot.max() - bot.min()
    feet = []
    for fx in ((cx - 26, cx + 26) if span < 140 else (bot.min() + 24, bot.max() - 24)):
        feet.append((fx - 26, y1 - 14, fx + 26, y1 + 22))
    im = Image.new("RGB", (512, 512), (255, 255, 255)); dd = ImageDraw.Draw(im)
    for e in feet: dd.ellipse((e[0] - 7, e[1] - 7, e[2] + 7, e[3] + 7), fill=(20, 20, 20)); dd.ellipse(e, fill=(110, 110, 110))
    dist = ndi.distance_transform_edt(a)
    # shade: light upper-left, dark lower-right, by a shifted mask
    sh = ndi.shift(a.astype(float), (-14, -14), order=0) > 0.5
    body = np.array(im)
    out_line = ndi.binary_dilation(a, iterations=8) & ~a
    body[out_line] = (20, 20, 20)
    body[a] = (128, 128, 128)
    body[a & ~sh] = (86, 86, 86)
    hi = a & (dist > 6) & ~ndi.shift(a.astype(float), (22, 22), order=0).astype(bool)
    body[hi] = (190, 190, 190)
    im = Image.fromarray(body); dd = ImageDraw.Draw(im)
    for e in feet: dd.ellipse(e, fill=(110, 110, 110))
    # the eye: where the stroke is widest, a little bigger than the stroke (it bulges, as today's)
    #  near the glyph's middle, a little high (a face), where the stroke is thick: the same place on every form
    ty, tx = ys.min() + 0.42 * (y1 - ys.min()), (xs.min() + xs.max()) / 2
    yy, xx = np.mgrid[:512, :512]; sc = np.where(a, dist - 0.22 * np.hypot(yy - ty, xx - tx), -1e9)
    y, x = np.unravel_index(np.argmax(sc), sc.shape); r = 50
    dd.ellipse((x - r - 8, y - r - 8, x + r + 8, y + r + 8), fill=(20, 20, 20))
    dd.ellipse((x - r, y - r, x + r, y + r), fill=(250, 250, 250))
    p = int(r * 0.52); dd.ellipse((x - p, y - p + 4, x + p, y + p + 4), fill=(24, 24, 28))
    q = max(6, p // 3); dd.ellipse((x - p // 2 - q, y - p // 2 - q, x - p // 2 + q, y - p // 2 + q), fill=(255, 255, 255))
    im.save(out)
    Image.fromarray((a * 255).astype(np.uint8)).resize((64, 64), Image.BOX).save(out.replace('_guide', '_mask'))
    return {"x": int(x), "y": int(y), "r": r + 8}
if __name__ == "__main__":
    import json; E = {f: make(f, f"{D}/src/{f}_guide.png") for f in FORMS}; json.dump(E, open(D + "/src/eyes.json", "w"))
    from PIL import Image as I
    s = I.new("RGB", (7 * 160, 4 * 160), "white")
    for i, f in enumerate(FORMS): s.paste(I.open(f"{D}/src/{f}_guide.png").resize((156, 156)), ((i % 7) * 160, (i // 7) * 160))
    s.save(W + "/sheets/guides.png"); print("ok")

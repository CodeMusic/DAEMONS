"""batch 6: quick look -- clean front, clean back (hand/ where drawn), reduced front/back/icon, 3x on the ground"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
T = os.environ["T452_ROOT"] + "/p"; F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
out, names = sys.argv[1], sys.argv[2:]
def ld(p):
    im = Image.open(p)
    if im.mode == "P":
        import numpy as np
        a = np.array(im.convert("RGBA")); a[np.array(im) == 0, 3] = 0; im = Image.fromarray(a)
    return im.convert("RGBA")
def on(im, s=3):
    b = Image.new("RGBA", im.size, (205, 205, 172, 255)); b.alpha_composite(im); return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)
s = Image.new("RGB", (5 * 200 + 20, len(names) * 220 + 10), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, n in enumerate(names):
    y = 10 + i * 220; d.text((10, y), n, fill=(0, 0, 0), font=F)
    def pick(k, base): h = f"{T}/hand/{n}_{k}.png"; return h if os.path.exists(h) else f"{T}/{base}/{n}_{k}.png"
    fs = [pick("front", "clean"), pick("back", "clean"), f"{T}/reduced/{n}_front.png", f"{T}/reduced/{n}_back.png", pick("icon", "reduced")]
    for j, f in enumerate(fs):
        if not os.path.exists(f): continue
        im = ld(f)
        if j == 3:
            r = Image.open(f); r.putpalette(Image.open(f"{T}/reduced/{n}_front.png").getpalette()); im = ld_p = r
            import numpy as np
            a = np.array(r.convert("RGBA")); a[np.array(r) == 0, 3] = 0; im = Image.fromarray(a)
        if j == 4: im = im.crop((0, 0, 32, 32))
        s.paste(on(im, 3 if j < 4 else 5), (10 + j * 200, y + 20))
s.save(out); print(out)

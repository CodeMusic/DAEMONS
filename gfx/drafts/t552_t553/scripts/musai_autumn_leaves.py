"""T-553: MUSAI's type (NORMAL) is warm, so place_rich rotated autumn's orange leaves to the far side of the wheel (blue).
Set those accent entries back to leaf orange, by luminance, in the png and the .pal."""
from PIL import Image
D = "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t552_t553/reduced/"
im = Image.open(D + "musai_autumn.png"); p = im.getpalette()
ORANGE = [(122, 52, 12), (196, 92, 28), (238, 142, 48)]
blues = [i for i in range(1, 16) if p[3*i+2] > p[3*i] + 50]
blues.sort(key=lambda i: sum(p[3*i:3*i+3]))
for k, i in enumerate(blues):
    p[3*i:3*i+3] = ORANGE[min(len(ORANGE) - 1, round(k * (len(ORANGE) - 1) / max(1, len(blues) - 1)))]
im.putpalette(p); im.save(D + "musai_autumn.png")
open(D + "musai_autumn.pal", "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(p[3*i:3*i+3]) for i in range(16)))
print("entries", blues)

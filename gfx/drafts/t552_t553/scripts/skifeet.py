"""T-553: the winter ski feet drawn by hand, pixel by pixel, on the reduced fronts (the model would draw skis or ordinary
feet, never a ski-shaped foot): the hind foot becomes one long flat furry runner along the ground with a turned-up tip,
in the sprite's own fur ramp and outline. Writes reduced/<name>_skifeet.png; the original stays beside it."""
import numpy as np
from PIL import Image
D = "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t552_t553/reduced/"
def foot(a, top, x0, x1, light, mid, out):
    # rows: top = upper outline (only where empty), top+1 light fur, top+2 mid fur, top+3 lower outline
    for x in range(x0, x1 + 1):
        if a[top, x] == 0: a[top, x] = out
        a[top + 1, x] = light; a[top + 2, x] = mid; a[top + 3, x] = out
    a[top + 1, x0 - 1] = a[top + 2, x0 - 1] = out if a[top + 1, x0 - 1] == 0 else a[top + 1, x0 - 1]
    # the turned-up tip
    a[top + 3, x1 + 1] = out; a[top + 2, x1 + 1] = mid; a[top + 1, x1 + 1] = light; a[top, x1 + 1] = out
    a[top + 2, x1 + 2] = out; a[top + 1, x1 + 2] = out; a[top, x1 + 2] = out; a[top - 1, x1 + 2] = out
    a[top - 1, x1 + 1] = 0 if a[top - 1, x1 + 1] == 0 else a[top - 1, x1 + 1]
for n, args in (("maskmusai_winter", (46, 34, 59, 2, 3, 5)), ("codemusai_winter", (46, 47, 59, 3, 4, 5))):
    im = Image.open(D + n + ".png"); a = np.array(im)
    foot(a, *args)
    o = Image.fromarray(a, "P"); o.putpalette(im.getpalette()); o.save(D + n + "_skifeet.png")
    big = Image.new("RGB", (64 * 8 + 10, 64 * 4), "white")
    for i, f in enumerate((n, n + "_skifeet")):
        x = Image.open(D + f + ".png").crop((0, 0, 64, 64)).convert("RGB").resize((256, 256), Image.NEAREST); big.paste(x, (i * 266, 0))
    big.save("/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/399ec87a-6ccd-49c8-a8ea-33d73f9db2f3/scratchpad/%s_skifeet_cmp.png" % n)
print("ok")

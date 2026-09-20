#!/usr/bin/env python3
"""A character drawing -> the high-resolution source spriteforge.py restyles from (T-174).

    python3 tools/prephires.py gfx/characters/holt.jpeg gfx/drafts/t174/src/holt_hi.png --aspect 1.0

WHY THIS EXISTS, AND IT IS THE WHOLE OF WHAT T-174'S FIRST ATTEMPT GOT WRONG. The first restyle of CRYSTAL fed the
model the 64x96 ROM PICTURE upscaled -- a blocky input -- so it invented detail, and the user called the result
distorted in play. `gbachar.py` already downsamples with LANCZOS: the resolution had been thrown away before it ever
got there. The fix is to restyle from the drawing at ITS OWN size and let the cut do the reduction, once.

THREE THINGS THIS DOES, and each one was a failure before it was a step:

  KEYS THE BACKDROP THE WAY THE CUT DOES. A flood fill could not clear it -- the jpeg's green is not flat, and the
  framing collapsed. So the key here is `gbachar.silhouette` itself, the same function that already knows Holt's
  olive backdrop is two points under the hue threshold and that Al's dark sage is inside 45 of his own trousers.
  One keying rule for the source and the cut means a restyle cannot frame differently from the art it replaces.

  PADS TO THE ASPECT THE ROM PICTURE HAS. A portrait cut to 64x64 from a square source frames as the game frames it;
  from a 1408x768 draft it does not. The subject is cropped to its own box, given a margin, then padded to `--aspect`
  (width/height of the destination: 1.0 for a 64x64 portrait, 0.667 for a 64x96 speech pic).

  DRAWS IT AT 904. SDXL's budget, and a multiple of 8.

WHAT IT DOES NOT DO: it does not change the drawing. Every pixel that is figure comes through untouched, so what the
model is handed is the art the game already shows, at the size it was drawn.
"""
import argparse, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gridsample import deringe
import gbachar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--aspect", type=float, default=1.0, help="width/height of the sprite this becomes")
    ap.add_argument("--long", type=int, default=904, help="longest side of the source handed to the model")
    ap.add_argument("--margin", type=float, default=0.06, help="clear space around the figure, as a share of its box")
    ap.add_argument("--no-hue", action="store_true", help="key on the flat corners alone, as gbachar's hue=False does")
    a = ap.parse_args()

    img = deringe(np.asarray(Image.open(os.path.join(ROOT, a.src)).convert("RGB")).astype(int))
    ink = gbachar.silhouette(img, hue=not a.no_hue)
    ys, xs = np.where(ink)
    if not len(ys):
        raise SystemExit("%s: nothing keyed as figure" % a.src)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1

    #  the figure on white, its backdrop gone: what the model sees is the drawing and nothing else
    flat = np.where(ink[..., None], img, 255).astype(np.uint8)[y0:y1, x0:x1]
    fh, fw = flat.shape[:2]
    m = int(round(max(fw, fh) * a.margin))
    W, H = fw + 2 * m, fh + 2 * m
    if W / H < a.aspect:                       # pad to the destination's shape, never crop to it
        W = int(round(H * a.aspect))
    else:
        H = int(round(W / a.aspect))
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    canvas.paste(Image.fromarray(flat), ((W - fw) // 2, (H - fh) // 2))

    s = a.long / max(W, H)
    size = (max(8, int(round(W * s)) // 8 * 8), max(8, int(round(H * s)) // 8 * 8))
    out = canvas.resize(size, Image.LANCZOS)
    os.makedirs(os.path.dirname(os.path.join(ROOT, a.out)), exist_ok=True)
    out.save(os.path.join(ROOT, a.out))
    print("  %-34s figure %dx%d -> %dx%d (aspect %.3f) -> %s" % (os.path.basename(a.src), fw, fh, *size, W / H, a.out))


if __name__ == "__main__":
    main()

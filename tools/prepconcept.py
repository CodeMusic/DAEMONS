#!/usr/bin/env python3
"""Old concept art -> a 512 image-to-image source for spriteforge.py (T-131).

    python3 tools/prepconcept.py gfx/front/crawler.jpeg SRC.png [R,G,B]

The subject is cropped, fitted (360px, or 440 wide for a long creature), and set on a KEY colour -- batch 1 uses
0,200,0. Redrawing the approved concept at denoise 0.55 keeps the design; at 0.75 ROVERCUB became a cat. A key
ground, not white, because the white NIBBLE, LABEL and CRAWLER's face could not be told from white paper.

Old concept art: subject cropped, fitted, and set on a KEY colour. Only paper REACHABLE
from the edge becomes key -- a white head inside an outline stays white."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
src, out = sys.argv[1], sys.argv[2]
KEY = tuple(int(v) for v in sys.argv[3].split(",")) if len(sys.argv) > 3 else (255, 255, 255)
a = np.asarray(Image.open(src).convert("RGB")).astype(int)
paper = (a.min(2) > 225) & (np.ptp(a, 2) < 24)
lab, _ = ndimage.label(paper)
edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1]); edge.discard(0)
outside = np.isin(lab, list(edge))
ys, xs = np.where(~outside)
box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
im = Image.open(src).convert("RGB").crop(box)
m = Image.fromarray((~outside[box[1]:box[3], box[0]:box[2]] * 255).astype(np.uint8))
size = (440, 360) if im.width > 1.6 * im.height else (360, 360)
sc = min(size[0] / im.width, size[1] / im.height)
im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
m = m.resize(im.size, Image.LANCZOS).point(lambda v: 255 if v > 127 else 0)
c = Image.new("RGB", (512, 512), KEY); c.paste(im, ((512 - im.width) // 2, (512 - im.height) // 2), m); c.save(out)

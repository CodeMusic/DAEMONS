#!/usr/bin/env python3
"""Reduce a 64px drawing to one 16x32 overworld frame, and put it beside the frame we have (T-170, the trial).

    python3 tools/gbareduce.py            # the three trial figures -> /tmp/reduce.png

THE QUESTION T-170 ASKS. T-164 measured spriteforge ON the overworld and found it adds little: a whole 16x32 sheet
restyled comes back as speckle. This asks a different question -- draw at 64px, the size the model is good at, and
REDUCE -- and the trial has to answer the first part of it before any sheet is redrawn:

    can a 64px drawing survive the reduction to sixteen pixels wide at all?

WHAT THE REDUCTION MUST OBEY, or it is not a candidate at all (engine.md trap 17, T-120):

  * THE FRAME IS 16x32 and a sheet's frame COUNT never changes.
  * THE PALETTE IS THE SHEET'S OWN, fixed: the reduced frame is quantized to the sixteen colours the sheet already
    has, with index 0 left transparent. No colour is added, so a figure is drawn from what its NPC slot holds.
  * ONLY the standing frame is reduced here. A walk cycle cannot be reduced from one drawing -- that is the SECOND
    question, and it only matters if the answer to the first is yes.

HOW. The subject is cut from the drawing by its own border colour, scaled to fit 16x32 (area-averaged, because
nearest at this ratio drops whole limbs), and each pixel is mapped to the nearest colour in the sheet's palette in
CIE-ish weighted RGB, with a transparency cut so the ground does not become a colour.
"""
import os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")
OUT = "/tmp/reduce.png"

TRIAL = [   # label, the 64px drawing, the sheet it would go into, which frame is standing-down
    ("YOUNGSTER (a person)", "engineGba/graphics/trainers/front_pics/youngster_front_pic.png",
     "engineGba/graphics/object_events/pics/people/youngster.png", 0),
    ("CRYSTAL (a Clear)", "engineGba/graphics/oak_speech/oak/pic.png",
     "engineGba/graphics/object_events/pics/people/prof_oak.png", 0),
    ("TILT (a leader)", "engineGba/graphics/trainers/front_pics/leader_koga_front_pic.png",
     "engineGba/graphics/object_events/pics/people/koga.png", 0),
]


def opaque(im):
    """the drawing without its ground: index 0 where the file is indexed, else the border colour"""
    if im.mode == "P":
        idx = np.array(im)
        rgb = np.array(im.convert("RGB"))
        return rgb, idx != 0
    rgb = np.array(im.convert("RGB"))
    key = rgb[1, 1].astype(int)
    return rgb, (np.abs(rgb.astype(int) - key).sum(axis=2) > 60)


def reduce_to(src, w, h):
    rgb, mask = opaque(Image.open(src))
    ys, xs = np.where(mask)
    rgb, mask = rgb[ys.min():ys.max() + 1, xs.min():xs.max() + 1], mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    #  fit inside the frame, keeping the figure's own proportions: a person is taller than wide and the frame is too
    sh, sw = mask.shape
    scale = min(w / sw, h / sh)
    tw, th = max(1, int(round(sw * scale))), max(1, int(round(sh * scale)))
    a = Image.fromarray(rgb).resize((tw, th), Image.BOX)
    m = Image.fromarray((mask * 255).astype(np.uint8)).resize((tw, th), Image.BOX)
    #  standing on the bottom of the frame, centred
    out = np.zeros((h, w, 3), dtype=np.uint8)
    cover = np.zeros((h, w), dtype=np.uint8)
    x0, y0 = (w - tw) // 2, h - th
    out[y0:y0 + th, x0:x0 + tw] = np.array(a)
    cover[y0:y0 + th, x0:x0 + tw] = np.array(m)
    return out, cover > 110          # a pixel more than about half covered is the figure


def quantize(rgb, mask, palette):
    """nearest of the sheet's own sixteen, weighted the way an eye weighs them; index 0 stays transparent"""
    pal = np.array(palette[1:], dtype=int)
    w = np.array([0.3, 0.59, 0.11])
    flat = rgb.reshape(-1, 3).astype(int)
    d = (((flat[:, None, :] - pal[None, :, :]) ** 2) * w).sum(axis=2)
    idx = (d.argmin(axis=1) + 1).reshape(rgb.shape[:2])
    return np.where(mask, idx, 0).astype(np.uint8)


def main():
    cells = []
    for label, src, sheet, frame in TRIAL:
        sh = Image.open(os.path.join(ROOT, sheet))
        pal = [tuple(sh.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
        w, h = 16, sh.height
        cur = sh.crop((frame * w, 0, frame * w + w, h))
        rgb, mask = reduce_to(os.path.join(ROOT, src), w, h)
        new = Image.fromarray(quantize(rgb, mask, pal), mode="P")
        new.putpalette(sh.getpalette())
        big = Image.open(os.path.join(ROOT, src))
        print("  %-22s %-42s -> %dx%d in %d colours" % (label, os.path.basename(src), w, h, len(set(np.array(new).flatten())) - 1))
        cells.append((label, big, cur, new))
    S = 8
    W = 120 + len(cells) * (16 * S * 2 + 60)
    out = Image.new("RGB", (W, 32 * S + 40), (40, 44, 52))
    from PIL import ImageDraw
    d = ImageDraw.Draw(out)
    x = 10
    for label, big, cur, new in cells:
        b = big.convert("RGB").resize((32 * S // 2, 32 * S // 2), Image.NEAREST)
        out.paste(b, (x, 20))
        d.text((x, 6), label, fill=(235, 235, 235))
        x += 32 * S // 2 + 12
        for im in (cur, new):
            bg = Image.new("RGB", (16 * S, 32 * S), (150, 190, 210))
            a = im.convert("RGBA")
            a.putdata([(0, 0, 0, 0) if i == 0 else c for i, c in zip(im.getdata(), a.getdata())])
            a = a.resize((16 * S, 32 * S), Image.NEAREST)
            bg.paste(a, (0, 0), a)
            out.paste(bg, (x, 20)); x += 16 * S + 8
        x += 30
    out.save(OUT)
    print("  ours now, then reduced -> %s" % OUT)


if __name__ == "__main__":
    main()

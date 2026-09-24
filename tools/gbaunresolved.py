#!/usr/bin/env python3
"""The unresolved display: what is there before the RESOLVER decodes it (T-250, 2026-09-24).

    python3 tools/gbaunresolved.py            # report
    python3 tools/gbaunresolved.py --write     # engineGba/graphics/pokemon/ghost/front.png

WHAT IT IS. Vanilla's ghost -- a purple mist with two eyes -- is what a player sees in HALFTONE TOWER without the
SILPH SCOPE, and now in the unread DOLDRUM CAVE too. The user's decision: the LATENT daemons keep their
non-corporeal look, and the thing seen WITHOUT the RESOLVER becomes structured noise, a latent before it is
decoded -- the RESOLVER is the decoder. Nothing in the game says so.

SO IT IS ONE, LITERALLY. Two drafts from the same seed on this project's own diffusion pipeline (tools/spriteforge.py):
the finished image, and the same sampling STOPPED eleven steps in of twenty-four and decoded with its noise still in
it. The finished one gives only the OUTLINE; everything inside the outline is the unfinished one. The eyes are just
coming through, which is as far as a thing gets toward being seen before it is read.

THE EDGE DISSOLVES rather than being cut, on an ordered dither over the outline's own soft alpha -- vanilla's mist
does the same, and a hard edge would claim a shape the thing has not settled on yet.

THE PALETTE IS NOT FINAL AND DOES NOT NEED TO BE. In the tower the screen is grey; in the cave
DaemonsScrambleLatentPalette (battle_gfx_sfx_util.c) re-weights every colour's LUMINANCE by random channels each
time. So what has to be right here is the order of light and dark, and the quantiser keeps that.
"""
import os, sys
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFTS = os.path.join(ROOT, "gfx/drafts/unresolved")
FULL, EARLY = os.path.join(DRAFTS, "s1101_full.png"), os.path.join(DRAFTS, "s1101_stop11.png")
OUT = os.path.join(ROOT, "engineGba/graphics/pokemon/ghost/front.png")
WRITE = "--write" in sys.argv
SIZE, BODY = 64, 58                       # the frame, and the tallest the body is drawn (vanilla's mist is ~56)
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
CLEAR = (152, 208, 160)                   # index 0, never drawn; vanilla's own transparent green


def outline(full):
    """Soft alpha: how far each pixel is from the grey the model painted behind the creature."""
    rgb = full.convert("RGB")
    w, h = rgb.size
    corners = [rgb.getpixel((x, y)) for x in (4, w - 5) for y in (4, h - 5)]
    bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))
    px = rgb.load()
    a = Image.new("L", rgb.size)
    ap = a.load()
    for y in range(h):
        for x in range(w):
            d = sum(abs(px[x, y][i] - bg[i]) for i in range(3))
            ap[x, y] = max(0, min(255, (d - 24) * 4))
    return a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6))


def build():
    full, early = Image.open(FULL), Image.open(EARLY).convert("RGB")
    alpha = outline(full)
    box = alpha.point(lambda v: 255 if v > 40 else 0).getbbox()
    side = max(box[2] - box[0], box[3] - box[1])
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
    crop = (cx - side // 2, cy - side // 2, cx - side // 2 + side, cy - side // 2 + side)
    body = early.crop(crop).resize((BODY, BODY), Image.BOX)
    soft = alpha.crop(crop).resize((BODY, BODY), Image.BOX)

    q = body.quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:45]
    order = sorted(range(15), key=lambda i: 77 * pal[3 * i] + 150 * pal[3 * i + 1] + 29 * pal[3 * i + 2])
    remap = {old: new + 1 for new, old in enumerate(order)}

    img = Image.new("P", (SIZE, SIZE), 0)
    flat = list(CLEAR)
    for i in order:
        flat += pal[3 * i:3 * i + 3]
    img.putpalette(flat + [0] * (768 - len(flat)))
    ox, oy = (SIZE - BODY) // 2, SIZE - BODY - 2
    qp, sp, ip = q.load(), soft.load(), img.load()
    for y in range(BODY):
        for x in range(BODY):
            if sp[x, y] > (BAYER[y % 4][x % 4] + 0.5) * 16:
                ip[ox + x, oy + y] = remap[qp[x, y]]
    return img


def main():
    img = build()
    drawn = sum(1 for v in img.getdata() if v)
    same = os.path.exists(OUT) and list(Image.open(OUT).getdata()) == list(img.getdata()) \
        and Image.open(OUT).getpalette()[:48] == img.getpalette()[:48]
    print("  the unresolved display: %d of %d pixels drawn, 15 colours in luminance order%s"
          % (drawn, SIZE * SIZE, " -- already written" if same else ""))
    if WRITE and not same:
        img.save(OUT)
        print("  written %s" % os.path.relpath(OUT, ROOT))
    if os.environ.get("SCRATCH"):
        img.convert("RGB").resize((256, 256), Image.NEAREST).save(os.path.join(os.environ["SCRATCH"], "unresolved.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

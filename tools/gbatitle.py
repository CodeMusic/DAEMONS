#!/usr/bin/env python3
"""Convert Gemini's front-door art into the formats the build wants.

    python3 tools/gbatitle.py art.png codemusai      # 64x64 face-off sprite
    python3 tools/gbatitle.py art.png caremusai
    python3 tools/gbatitle.py art.png wordmark       # 144x16 CODEMUSIC
    python3 tools/gbatitle.py art.png logo-content   # 256x64 title logo
    python3 tools/gbatitle.py art.png logo-context

Four assets, three formats, and none of them is "a PNG". 9.14 designs the
scenes; this is the part that gets the pixels into them.

  * the two FIGURES are 64x64 4bpp sprites -- index 0 transparent, index 1 the
    outline, thirteen left for the body. The outline is protected before the
    median cut runs, because generated art puts hundreds of nearly-black pixels
    on an edge and a cut will happily merge them into the darkest body colour
    and leave the creature with no outline at all. Same guard gbacolour.py uses.
  * the WORDMARK is 144x16 in L mode, and its values are not greys -- Gen 3
    stores a 4bpp index times seventeen, so 0 is index 0 and 255 is index 15.
    Vanilla draws the letters at 0 on a ground of 255.
  * the LOGO is 8bpp, so colour is not the constraint there; only size is.

IT REFUSES RATHER THAN GUESSES. A background that is not white, art with no
black outline, or a wordmark that is mostly anti-aliasing are all reported and
nothing is written. 3118 is the reason: rgbgfx rejects anti-aliasing outright,
and finding that out at build time is worse than finding it out here.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
BG_CUT, OUTLINE = 232, 60          # luminance: above is ground, below is outline

ASSETS = {
    "codemusai":    ("figure", (64, 64),  "graphics/title_screen/faceoff/codemusai.png"),
    "caremusai":    ("figure", (64, 64),  "graphics/title_screen/faceoff/caremusai.png"),
    "wordmark":     ("shades", (144, 16), "graphics/intro/game_freak/game_freak.png"),
    "logo-content": ("indexed", (256, 64), "graphics/title_screen/firered/game_title_logo.png"),
    "logo-context": ("indexed", (256, 64), "graphics/title_screen/leafgreen/game_title_logo.png"),
}

def lum(c):
    if isinstance(c, int):      # L mode hands back one value, RGB hands back three
        return c
    return (c[0] * 299 + c[1] * 587 + c[2] * 114) // 1000

def load(src):
    """Flatten to RGB on WHITE. Gemini hands back RGBA as often as not, and
    PIL's default composite for a dropped alpha channel is black -- which would
    make the whole surround read as subject."""
    im = Image.open(src)
    if im.mode in ("RGBA", "LA") or "transparency" in im.info:
        im = im.convert("RGBA")
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.split()[-1])
        return flat
    return im.convert("RGB")

def lossy(src):
    return os.path.splitext(src)[1].lower() in (".jpg", ".jpeg")

def warn_edges(im, what):
    """Ink on the border means the art was cropped through a letter."""
    px = im.load(); w, h = im.size
    sides = {"left":  sum(1 for y in range(h) if lum(px[0, y]) < 128),
             "right": sum(1 for y in range(h) if lum(px[w-1, y]) < 128),
             "top":   sum(1 for x in range(w) if lum(px[x, 0]) < 128),
             "bottom":sum(1 for x in range(w) if lum(px[x, h-1]) < 128)}
    hit = [k for k, v in sides.items() if v > h // 40]
    if hit:
        print("  ** %s: ink runs off the %s edge -- something is cropped through"
              % (what, " and ".join(hit)))

def crop_to_subject(im):
    """Trim the white surround. Everything downstream assumes the art fills
    the frame, and Gemini leaves a different margin every time."""
    px = im.load()
    w, h = im.size
    box = [(x, y) for y in range(h) for x in range(w) if lum(px[x, y]) < BG_CUT]
    if not box:
        sys.exit("  !! nothing but background -- is the surround pure white?")
    xs = [p[0] for p in box]; ys = [p[1] for p in box]
    return im.crop((min(xs), min(ys), max(xs) + 1, max(ys) + 1))

def fit(im, size, pad=0.02):
    """Scale into the target box, keeping the aspect and centring what is left.
    LANCZOS on the way DOWN is right -- this is a downsample of high-res art,
    not the upscale 9.4 refused."""
    tw, th = size
    inner = (max(1, int(tw * (1 - pad))), max(1, int(th * (1 - pad))))
    scale = min(inner[0] / im.width, inner[1] / im.height)
    nw, nh = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    out = Image.new("RGB", size, (255, 255, 255))
    out.paste(im.resize((nw, nh), Image.LANCZOS), ((tw - nw) // 2, (th - nh) // 2))
    return out

def figure(src, size, dst):
    art = load(src)
    warn_edges(art, "figure")
    im = fit(crop_to_subject(art), size)
    px = im.load()
    w, h = im.size
    ground = [(x, y) for y in range(h) for x in range(w) if lum(px[x, y]) >= BG_CUT]
    edge   = [(x, y) for y in range(h) for x in range(w) if lum(px[x, y]) < OUTLINE]
    if len(edge) < (w * h) // 100:
        sys.exit("  !! only %d outline pixels -- the art has no black outline" % len(edge))
    # quantise the BODY only; spending a slot on the surround would waste one
    body = im.copy()
    for x, y in ground + edge:
        body.putpixel((x, y), (255, 255, 255))
    q = body.convert("RGB").quantize(colors=13, method=Image.MEDIANCUT, dither=Image.NONE)
    qpal = q.getpalette()[:13 * 3]
    out = Image.new("P", size, 0)
    # EXACTLY sixteen entries. Padding to 256 makes gbagfx emit a 256-colour
    # .gbapal, which is a 4bpp sprite carrying an 8bpp palette.
    pal = [255, 0, 255,  0, 0, 0] + qpal          # 0 transparent, 1 outline
    pal += [0, 0, 0] * (16 - len(pal) // 3)
    out.putpalette(pal[:48])
    op, qp = out.load(), q.load()
    for y in range(h):
        for x in range(w):
            if (x, y) in set(ground):
                op[x, y] = 0
    gset, eset = set(ground), set(edge)
    for y in range(h):
        for x in range(w):
            op[x, y] = 0 if (x, y) in gset else 1 if (x, y) in eset else qp[x, y] + 2
    used = len({op[x, y] for y in range(h) for x in range(w)})
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    out.save(dst)
    print("  %s  %dx%d, %d of 16 colours used" % (os.path.relpath(dst, ROOT), w, h, used))

def shades(src, size, dst):
    """L mode, and the values are 4bpp indices times seventeen -- vanilla draws
    the letters at 0 on a ground of 255 (index 15)."""
    # Test the SOURCE, not the resample. Downsampling with LANCZOS creates
    # intermediate values by definition, so checking afterwards would reject
    # even vanilla's own art fed back through. Anti-aliasing is a property of
    # what Gemini drew.
    warn_edges(load(src), "wordmark")
    art = crop_to_subject(load(src).convert("L"))
    ap = art.load()
    aw, ah = art.size
    mid = sum(1 for y in range(ah) for x in range(aw) if 64 < ap[x, y] < 192)
    if mid > (aw * ah) // 20:
        if lossy(src):
            # JPEG puts a ramp on every hard edge by construction, so the
            # measurement cannot tell the artist's anti-aliasing from the
            # codec's. Say so and carry on rather than refuse a good drawing.
            print("  ** %d of %d source pixels are mid-grey, but this is a "
                  "JPEG and ringing accounts for that. Thresholding anyway."
                  % (mid, aw * ah))
        else:
            sys.exit("  !! %d of %d source pixels are mid-grey -- that is "
                     "anti-aliasing, and the converter rejects it. Ask again "
                     "for hard edges." % (mid, aw * ah))
    im = fit(art, size).convert("L")
    px = im.load()
    w, h = im.size
    out = Image.new("L", size, 255)
    op = out.load()
    for y in range(h):
        for x in range(w):
            v = px[x, y]
            op[x, y] = 0 if v < 96 else (17 if v < 160 else (34 if v < 208 else 255))
    out.save(dst)
    print("  %s  %dx%d, source had %d mid-grey pixels of %d"
          % (os.path.relpath(dst, ROOT), w, h, mid, aw * ah))

def split_stacked(im):
    """Vanilla's 256x64 logo is SIDE BY SIDE -- the big word left, the edition
    stacked right -- and ours came back stacked, at 1.87:1 into a 4:1 slot.
    Letterboxing it would waste half the strip, so find the blank band between
    the two words and recompose."""
    px = im.load(); w, h = im.size
    rows = [any(lum(px[x, y]) < 200 for x in range(w)) for y in range(h)]
    bands, run = [], None
    for y, on in enumerate(rows + [False]):
        if on and run is None:
            run = y
        elif not on and run is not None:
            bands.append((run, y)); run = None
    if len(bands) != 2:
        return None
    return [im.crop((0, a, w, b)) for a, b in bands]

def indexed(src, size, dst):
    art = load(src)
    warn_edges(art, "logo")
    blocks = split_stacked(crop_to_subject(art))
    if blocks:
        big, small = sorted(blocks, key=lambda b: -b.height)
        tw, th = size
        gap, m = 8, 2
        bh = th - 2 * m
        bw = min(int(big.width * bh / big.height), int(tw * 0.68))
        bh2 = int(big.height * bw / big.width)
        sw = tw - bw - gap - 2 * m
        sh = min(int(small.height * sw / small.width), bh)
        sw = int(small.width * sh / small.height)
        out = Image.new("RGB", size, (255, 255, 255))
        out.paste(big.resize((bw, bh2), Image.LANCZOS), (m, (th - bh2) // 2))
        out.paste(small.resize((sw, sh), Image.LANCZOS), (tw - m - sw, (th - sh) // 2))
        im = out
        print("  recomposed side by side: %dx%d and %dx%d" % (bw, bh2, sw, sh))
    else:
        im = fit(crop_to_subject(art), size)
    q = im.quantize(colors=200, method=Image.MEDIANCUT, dither=Image.NONE)
    q.save(dst)
    used = len(set(q.getdata()))
    print("  %s  %dx%d, %d colours (8bpp allows 256)"
          % (os.path.relpath(dst, ROOT), size[0], size[1], used))

def main():
    if len(sys.argv) < 3 or sys.argv[2] not in ASSETS:
        sys.exit(__doc__ + "\nassets: " + ", ".join(sorted(ASSETS)))
    src, name = sys.argv[1], sys.argv[2]
    kind, size, rel = ASSETS[name]
    dst = os.path.join(GBA, rel)
    if kind != "figure" and not os.path.isfile(dst):
        sys.exit("  !! %s is not there -- wrong checkout?" % rel)
    {"figure": figure, "shades": shades, "indexed": indexed}[kind](src, size, dst)

if __name__ == "__main__":
    main()

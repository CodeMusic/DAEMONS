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
    """The logo is not an image, it is THREE files.

    game_title_logo is a 32x12 tile area of the screen -- 256x96, not the
    256x64 the atlas PNG happens to be -- drawn from a DEDUPLICATED atlas
    through a tilemap, at 8bpp, with its palette loaded across thirteen banks
    (`13 * PLTT_SIZE_4BPP`, so 208 colours and banks 13 and 14 belong to the
    box art and the background). Replacing only the atlas leaves the map
    pointing at tiles that have moved and the palette coming from the old
    .pal -- which is exactly what garbled the whole background.

    So: compose, quantise, deduplicate, and write the atlas, the map and the
    palette together."""
    art = load(src)
    warn_edges(art, "logo")
    SCREEN_W, SCREEN_H, ROWS = 256, 96, 12
    blocks = split_stacked(crop_to_subject(art))
    canvas = Image.new("RGB", (SCREEN_W, SCREEN_H), (255, 255, 255))
    if blocks:
        big, small = sorted(blocks, key=lambda b: -b.height)
        bw = int(SCREEN_W * 0.80)
        bh = int(big.height * bw / big.width)
        sw = int(SCREEN_W * 0.34)
        sh = int(small.height * sw / small.width)
        top = (SCREEN_H - bh - sh - 6) // 2
        canvas.paste(big.resize((bw, bh), Image.LANCZOS), ((SCREEN_W - bw) // 2, top))
        canvas.paste(small.resize((sw, sh), Image.LANCZOS),
                     ((SCREEN_W - sw) // 2, top + bh + 6))
        print("  composed 256x96: word %dx%d over edition %dx%d" % (bw, bh, sw, sh))
    else:
        canvas.paste(fit(crop_to_subject(art), (SCREEN_W, SCREEN_H)), (0, 0))

    # Fewer colours means more tiles repeat. Vanilla spends 208 because its
    # logo is a gradient; ours is flat black on white with a drop shadow, and
    # at 200 colours the resample's soft edges made every tile unique. Step
    # down until the atlas fits, and say what it cost.
    for ncolours in (200, 64, 32, 16, 8, 4):
        q = canvas.quantize(colors=ncolours, method=Image.MEDIANCUT, dither=Image.NONE)
        px = q.load()
        seen = set()
        for ty in range(ROWS):
            for tx in range(32):
                seen.add(tuple(px[tx * 8 + x, ty * 8 + y]
                               for y in range(8) for x in range(8)))
        if len(seen) < 256:
            break
    else:
        sys.exit("  !! more than 256 unique tiles even at 4 colours")
    # Index 0 is TRANSPARENT on a Gen 3 background, and the surround has to be
    # it -- otherwise the logo arrives as a white rectangle over the title's
    # own backdrop. Quantise puts the colours wherever it likes, so find the
    # one in the corner and swap it to 0.
    qp = q.load()
    corner = qp[0, 0]
    if corner != 0:
        data = list(q.getdata())
        data = [0 if v == corner else (corner if v == 0 else v) for v in data]
        q.putdata(data)
        pal = q.getpalette()
        pal[0:3], pal[corner*3:corner*3+3] = pal[corner*3:corner*3+3], pal[0:3]
        q.putpalette(pal)
    px = q.load()
    # tile 0 must be blank: every screen position the map does not name is 0
    blank = tuple([0] * 64)
    atlas, index = [blank], {blank: 0}
    tmap = [0] * (32 * 20)
    for ty in range(ROWS):
        for tx in range(32):
            tile = tuple(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))
            if tile not in index:
                if len(atlas) >= 256:
                    sys.exit("  !! more than 256 unique tiles after dedup -- "
                             "the art has too much detail for one BG")
                index[tile] = len(atlas); atlas.append(tile)
            tmap[ty * 32 + tx] = index[tile]

    out = Image.new("P", (256, 64), 0)
    op = out.load()
    for i, tile in enumerate(atlas):
        bx, by = (i % 32) * 8, (i // 32) * 8
        for k, v in enumerate(tile):
            op[bx + k % 8, by + k // 8] = v
    pal = q.getpalette()[:256 * 3]
    pal += [0] * (768 - len(pal))
    out.putpalette(pal)
    out.save(dst)

    base = os.path.splitext(dst)[0]
    with open(base + ".bin", "wb") as f:
        for v in tmap:
            f.write(bytes((v & 0xFF, (v >> 8) & 0xFF)))
    # the .gbapal rule prefers .pal over .png, so the palette has to be written
    # HERE or the tiles and their colours come from different centuries
    with open(base + ".pal", "w") as f:
        f.write("JASC-PAL\n0100\n256\n")
        for i in range(256):
            f.write("%d %d %d\n" % tuple(pal[i * 3:i * 3 + 3]))
    print("  %s  %d unique tiles at %d colours (208 available)"
          % (os.path.relpath(dst, ROOT), len(atlas), ncolours))

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

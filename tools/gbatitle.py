#!/usr/bin/env python3
"""Convert Gemini's front-door art into the formats the build wants.

    python3 tools/gbatitle.py art.png codemusai      # 64x64 face-off sprite
    python3 tools/gbatitle.py art.png caremusai
    python3 tools/gbatitle.py art.png wordmark       # 144x16 CODEMUSIC
    python3 tools/gbatitle.py art.png logo-content   # 256x64 title logo
    python3 tools/gbatitle.py art.png logo-context
    python3 tools/gbatitle.py --t564 [--draft [DIR]] [--sheets DIR]   # T-564: the boot's last pret pieces (DRAFT)

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

    # WHICH WHITE. A global "swap the corner colour to index 0" made every white
    # transparent, including the ones INSIDE the letters -- 39 pixels of teal
    # showing through the middle of DAEMONS. The counters of D, A and O must go
    # transparent and the speckle must not, and the difference between them is
    # SIZE: a counter is a large enclosed region, an artefact is two pixels.
    cpx = canvas.load()
    lum = [[(cpx[x, y][0] * 299 + cpx[x, y][1] * 587 + cpx[x, y][2] * 114) // 1000
            for x in range(SCREEN_W)] for y in range(SCREEN_H)]
    white = [[lum[y][x] > 200 for x in range(SCREEN_W)] for y in range(SCREEN_H)]
    seen = [[False] * SCREEN_W for _ in range(SCREEN_H)]
    clear = [[False] * SCREEN_W for _ in range(SCREEN_H)]
    for sy in range(SCREEN_H):
        for sx in range(SCREEN_W):
            if not white[sy][sx] or seen[sy][sx]:
                continue
            blob, edge, border = [], [(sx, sy)], False
            seen[sy][sx] = True
            while edge:
                x, y = edge.pop()
                blob.append((x, y))
                if x in (0, SCREEN_W - 1) or y in (0, SCREEN_H - 1):
                    border = True
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    inside = 0 <= nx < SCREEN_W and 0 <= ny < SCREEN_H
                    if inside and white[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        edge.append((nx, ny))
            if border or len(blob) > 6:
                for x, y in blob:
                    clear[y][x] = True

    # 9.14 sanctioned the colour and this is where it is spent. CONTENT is cold
    # and ordered; CONTEXT is the whole spectrum. The editions differ by what
    # they think the world is made of, and the logo can say that without a word.
    warm = "leafgreen" in dst

    def ramp(t):
        if warm:
            # The whole spectrum EXCEPT the band the title's own background
            # sits in. A teal letter on a teal ground is a hole, not a colour,
            # so the ramp runs red to green and then jumps to blue and violet.
            import colorsys
            h = t * 0.33 if t < 0.5 else 0.60 + (t - 0.5) * 0.46
            r, g, b = colorsys.hsv_to_rgb(h, 0.92, 1.0)
            return (int(r * 248), int(g * 248), int(b * 248))
        a, b_ = (40, 88, 152), (168, 232, 248)
        return tuple(int(a[i] + (b_[i] - a[i]) * t) for i in range(3))

    TRANS = (255, 0, 255)
    shaded = Image.new("RGB", (SCREEN_W, SCREEN_H), TRANS)
    spx = shaded.load()
    for y in range(SCREEN_H):
        for x in range(SCREEN_W):
            if clear[y][x]:
                continue
            c = ramp(x / (SCREEN_W - 1))
            spx[x, y] = c if lum[y][x] < 100 else tuple(v // 4 for v in c)

    for ncolours in (64, 48, 32, 16, 8):
        q = shaded.quantize(colors=ncolours, method=Image.MEDIANCUT, dither=Image.NONE)
        px = q.load()
        uniq = set()
        for ty in range(ROWS):
            for tx in range(32):
                uniq.add(tuple(px[tx * 8 + x, ty * 8 + y]
                               for y in range(8) for x in range(8)))
        if len(uniq) < 256:
            break
    else:
        sys.exit("  !! more than 256 unique tiles even at 8 colours")

    pal = q.getpalette()
    ti = min(range(ncolours), key=lambda i: sum(
        (pal[i * 3 + k] - TRANS[k]) ** 2 for k in range(3)))
    if ti != 0:
        q.putdata([0 if v == ti else (ti if v == 0 else v) for v in q.getdata()])
        pal[0:3], pal[ti * 3:ti * 3 + 3] = pal[ti * 3:ti * 3 + 3], pal[0:3]
        q.putpalette(pal)
    px = q.load()

    blank = tuple([0] * 64)
    atlas, index = [blank], {blank: 0}
    tmap = [0] * (32 * 20)
    for ty in range(ROWS):
        for tx in range(32):
            tile = tuple(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))
            if tile not in index:
                index[tile] = len(atlas)
                atlas.append(tile)
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
    if "--t564" in sys.argv:
        return t564_main()
    if len(sys.argv) < 3 or sys.argv[2] not in ASSETS:
        sys.exit(__doc__ + "\nassets: " + ", ".join(sorted(ASSETS)))
    src, name = sys.argv[1], sys.argv[2]
    kind, size, rel = ASSETS[name]
    dst = os.path.join(GBA, rel)
    if kind != "figure" and not os.path.isfile(dst):
        sys.exit("  !! %s is not there -- wrong checkout?" % rel)
    {"figure": figure, "shades": shades, "indexed": indexed}[kind](src, size, dst)

# ======================================================================================================== T-564
#  THE BOOT'S LAST PRET PIECES (the user, 2026-11-15, batch 5 of the 2026-11-14 re-census). DRAFT: nothing is written
#  to the engine until the user picks (APPROVED_564 is empty).
#
#     python3 tools/gbatitle.py --t564                     # report: each piece, its contract, APPROVED_564
#     python3 tools/gbatitle.py --t564 --draft [DIR]       # every piece's A/B/C into DIR (gfx/drafts/t564_boot/)
#     python3 tools/gbatitle.py --t564 --sheets DIR [--frames DIR]   # today beside A/B/C at 2x, in context
#     python3 tools/gbatitle.py --t564 --write --approved  # write APPROVED_564's picks into engineGba (none yet)
#
#  THE CENSUS (2026-11-15, engine 5bcba60bb against pret upstream/master, by blob and by the code path). The boot is
#  the copyright screen (ours, gbacopyright.py), the CodeMusic splash, the thank-you card (T-320, text on the
#  splash's band), then the title. Of batch 5's eight files FOUR are still pret's AND on screen:
#
#    band    graphics/intro/game_freak/bg.png + bg.pal   the splash's navy band (BG3, three flat tiles, palette 0):
#            under the star, the CODEMUSIC wordmark and the thank-you card -- every boot
#    star    graphics/intro/game_freak/star.png           the yellow star that flies right to left trailing our 0s,
#            1s and notes (its own OBJ palette, PALTAG_STAR) -- every boot
#    slash   graphics/title_screen/slash.png              the glint across DAEMONS: an OBJ-WINDOW sprite, so only its
#            SHAPE is seen (BG0 lightened, BLDY 13, inside it); every 540 frames of the title
#    border  graphics/title_screen/border_bg.png          the title's bands and stage (BG3): four tiles, flat but for
#            one band-to-stage edge, painted through OUR palette (gbatitlepal.py) -- always
#
#  and four are not seen: presents.png (PRESENTS is created only under REVISION >= 1 and every DAEMONS build is
#  REVISION 0), blank_flames.png (all index 0, and CreateFlameSprite is never called since the face-off), streak.png
#  (CreateStreakSprites is never called), blank_sprite.png (all index 0: a 32x64 palette holder at (24,144), priority
#  0 -- drawing anything in it would put a block over the title's corner). Intro scenes 1-3 are cut (IntroCB_Thanks
#  follows the logo), and box_art_mon is ours and blank. slash.pal is pret's and never seen (the slash is a window and
#  the blank sprite has no pixels).
#
#  THE RULES each draft keeps. The same size and tile count as pret's; the same palette row. border: tile 0 untouched,
#  TILE 1 FLAT INDEX 6 -- it is the band under PRESS START, and Task_TitleScreen_BlinkPressStart hides the text by
#  writing index 6's colour into 1-5, so any other index under the letters shows them as holes (gbatitlepal.py) -- and
#  only the indices the palette already gives a role (6 band, 10 copyright ink, 11 stage, 12/15 strips), so both
#  editions' palettes paint it unchanged. slash: indices 0 and 1 only (a window has no colour). band: tiles 0 and 2 as
#  they are, palette entries 0-2 as they are (0 is the backdrop), one new shade in 3. star: index 0 transparent.
T564_PIECES = ["star", "slash", "border", "band"]
APPROVED_564 = {}                    # piece -> "A" | "B" | "C": empty, nothing written (T-564 is a DRAFT)
T564_DRAFT = os.path.join(ROOT, "gfx", "drafts", "t564_boot")
T564_FRAMES = os.path.join(ROOT, ".theatre", "routes", "film_t564_boot", "02")   # tools/routes/film_t564_boot.json
T564_FILES = {
    "star":   ["graphics/intro/game_freak/star.png"],
    "slash":  ["graphics/title_screen/slash.png"],
    "border": ["graphics/title_screen/border_bg.png"],
    "band":   ["graphics/intro/game_freak/bg.png", "graphics/intro/game_freak/bg.pal"],
}
T564_NAMES = {
    "star":   {"A": "THE MARK", "B": "THE CURSOR", "C": "THE QUAVER"},
    "slash":  {"A": "SCANLINE", "B": "BLOCK CURSOR", "C": "BIT RAIN"},
    "border": {"A": "THE RULE", "B": "GRAPH PAPER", "C": "SCANLINES"},
    "band":   {"A": "GRAPH PAPER", "B": "RULED", "C": "SCANLINES"},
}
T564_LINES = {
    "star":   {"A": "the CodeMusic ring itself, small, pink over teal with its white knot, throws the bits that become notes",
               "B": "a terminal block cursor, white on a teal edge, with a short speed trail: the code being typed across",
               "C": "a white quaver whose flag streams back like a comet's tail: the music arriving at the head of the code"},
    "slash":  {"A": "a band of horizontal scanlines sweeps the word, as a CRT redraws it",
               "B": "a solid upright block passes over DAEMONS, a cursor selecting it",
               "C": "three staggered columns of 0s and 1s: the word lit through binary as it passes"},
    "border": {"A": "a one-pixel rule in the copyright's ink where the band meets the stage",
               "B": "one band-coloured dot per tile on the stage: the INDEX's graph paper (T-563) behind the face-off",
               "C": "every fourth row of the stage in the band's shade: a quiet CRT behind the face-off"},
    "band":   {"A": "one lighter dot per tile: graph paper under the star, the wordmark and the thank-you",
               "B": "one lighter rule per tile row: ruled paper, or a long stave",
               "C": "every other row a shade darker: scanlines"},
}
T564_RECOMMENDED = {"star": "A", "slash": "C", "border": "A", "band": "A"}

#  The star's palette: the logo's own colours (logo.pal), so the small mark and the big one are the same object.
T564_STAR_PAL = [(0, 0, 0), (16, 16, 40), (0, 72, 96), (0, 144, 176), (96, 216, 240), (128, 32, 72), (216, 56, 120),
                 (248, 144, 176), (248, 232, 120), (248, 248, 248)] + [(0, 0, 0)] * 6
#  The band's palette: pret's three entries kept (0 the backdrop, 1 the navy, 2 the black outside), 3 and 4 ours.
T564_BAND_PAL = [(0, 0, 0), (24, 41, 74), (0, 0, 0), (34, 56, 98), (18, 31, 58)] + [(0, 0, 0)] * 8 + \
                [(82, 82, 82), (180, 180, 180), (255, 255, 255)]


def _grid(w, h, v=0):
    return [[v] * w for _ in range(h)]


def _stamp(g, rows, x0, y0, legend):
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c in legend and 0 <= y0 + y < len(g) and 0 <= x0 + x < len(g[0]):
                g[y0 + y][x0 + x] = legend[c]


def t564_star(d):
    """16x16, flying right to left: whatever leads, leads on the LEFT, and its trail is on the right."""
    g = _grid(16, 16)
    if d == "A":        # the mark: two rings stacked, pink over teal, a white knot where they cross
        _stamp(g, ["....oooooo....",
                   "..oo777666oo..",
                   ".o77oooooo66o.",
                   ".o7o......o6o.",
                   ".o7o......o5o.",
                   ".o76o....o55o.",
                   "..o66988955o..",
                   "...oo9889oo...",
                   "..o44988933o..",
                   ".o44o....o33o.",
                   ".o4o......o3o.",
                   ".o4o......o2o.",
                   ".o43oooooo22o.",
                   "..oo433322oo..",
                   "....oooooo...."], 1, 0,
               {"o": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9})
    elif d == "B":      # the cursor: a block, its edge teal, and three steps of trail behind it
        _stamp(g, ["................",
                   "..oooooo........",
                   "..o9999o........",
                   "..o9999o........",
                   "..o9999o..44....",
                   "..o9999o.33..2..",
                   "..o9999o44..3...",
                   "..o9999o........",
                   "..o9999o44..3...",
                   "..o9999o.33..2..",
                   "..o9999o..44....",
                   "..o9999o........",
                   "..o4444o........",
                   "..oooooo........",
                   "................",
                   "................"], 0, 1, {"o": 1, "9": 9, "4": 4, "3": 3, "2": 2})
    else:               # the quaver: head leading, flag streaming back to the right
        _stamp(g, [".......o........",
                   "......o9oooo....",
                   "......o99444o...",
                   "......o9o.3344o.",
                   "......o9o...33o.",
                   "......o9o....2o.",
                   "......o9o.....o.",
                   "......o9o.......",
                   "......o9o.......",
                   "..oooo99o.......",
                   ".o99999o........",
                   "o999999o........",
                   "o99999o.........",
                   ".oooo..........."], 0, 1, {"o": 1, "9": 9, "4": 4, "3": 3, "2": 2})
    im = Image.new("P", (16, 16), 0)
    im.putpalette([v for c in T564_STAR_PAL for v in c])
    im.putdata([v for row in g for v in row])
    return {"graphics/intro/game_freak/star.png": im}


_ZERO = [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."]
_ONE = ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."]


def t564_slash(d):
    """64x64, an OBJ-window shape: 1 is inside (BG0 lightened), 0 outside. It travels right at 9 px a frame."""
    g = _grid(64, 64)
    if d == "A":        # scanlines: a 14-wide band, two rows on and one off, top to bottom of the word
        for y in range(4, 60):
            if y % 3 != 2:
                for x in range(25, 39):
                    g[y][x] = 1
    elif d == "B":      # a block cursor, and a hairline ahead of it
        for y in range(4, 60):
            for x in range(24, 36):
                g[y][x] = 1
            for x in range(39, 41):
                g[y][x] = 1
    else:               # three columns of digits, staggered by half a glyph
        seq = "1011001110100101"
        for col, (x0, y0) in enumerate(((20, 2), (28, 6), (36, 0))):
            for k in range(8):
                ch = seq[(k + col * 5) % len(seq)]
                y = y0 + k * 8
                if y + 7 <= 64:
                    _stamp(g, _ONE if ch == "1" else _ZERO, x0, y, {"#": 1})
    im = Image.new("P", (64, 64), 0)
    im.putpalette([255, 255, 255, 238, 238, 238] + [0] * 42)    # pret's two entries: never seen (a window)
    im.putdata([v for row in g for v in row])
    return {"graphics/title_screen/slash.png": im}


def t564_border(d):
    """8x32, L mode: four tiles, value = 255 - 17 * index (gbagfx reads a grey PNG inverted, as the built .4bpp shows).
    Tile 0 untouched, tile 1 the flat band (PRESS START's blink), tile 2 the band-to-stage edge, tile 3 the stage."""
    t = [[[15] * 8 for _ in range(8)], [[6] * 8 for _ in range(8)],
         [[6] * 8 for _ in range(6)] + [[11] * 8 for _ in range(2)], [[11] * 8 for _ in range(8)]]
    if d == "A":
        t[2] = [[6] * 8 for _ in range(4)] + [[10] * 8] + [[6] * 8] + [[11] * 8 for _ in range(2)]
    elif d == "B":
        t[3][0][0] = 6
        t[2][6][0] = 6
    else:
        t[3][3] = [6] * 8
        t[3][7] = [6] * 8
        t[2][7] = [6] * 8
    im = Image.new("L", (8, 32))
    im.putdata([255 - 17 * v for tile in t for row in tile for v in row])
    return {"graphics/title_screen/border_bg.png": im}


def t564_band(d):
    """8x24, palette row 0: tile 0 (index 0) and tile 2 (the black outside, index 2) as pret's; tile 1 the band."""
    t1 = [[1] * 8 for _ in range(8)]
    if d == "A":
        t1[0][0] = 3
    elif d == "B":
        t1[7] = [3] * 8
    else:
        for y in (1, 3, 5, 7):
            t1[y] = [4] * 8
    rows = [[0] * 8 for _ in range(8)] + t1 + [[2] * 8 for _ in range(8)]
    im = Image.new("P", (8, 24), 0)
    im.putpalette([v for c in T564_BAND_PAL for v in c])
    im.putdata([v for row in rows for v in row])
    pal = "JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in T564_BAND_PAL)
    return {"graphics/intro/game_freak/bg.png": im, "graphics/intro/game_freak/bg.pal": pal}


T564_DRAW = {"star": t564_star, "slash": t564_slash, "border": t564_border, "band": t564_band}


def t564_check(piece, files):
    """The contract, against pret's own file at the same path: what a draft must keep to be dropped in."""
    errs = []
    for rel, v in files.items():
        if rel.endswith(".pal"):
            n = int(v.split()[2])
            if n != 16:
                errs.append("%s has %d colours, not 16" % (rel, n))
            continue
        old = Image.open(os.path.join(GBA, rel))
        if v.size != old.size:
            errs.append("%s is %s, pret's %s" % (rel, v.size, old.size))
        if v.mode != old.mode:
            errs.append("%s is mode %s, pret's %s" % (rel, v.mode, old.mode))
        px = list(v.getdata())
        if piece == "slash" and set(px) - {0, 1}:
            errs.append("slash uses %s: a window is 0 and 1" % sorted(set(px) - {0, 1}))
        if piece == "border":
            idx = [15 - p // 17 for p in px]
            tiles = [idx[i * 64:(i + 1) * 64] for i in range(4)]
            if set(tiles[0]) != {15}:
                errs.append("border tile 0 changed")
            if set(tiles[1]) != {6}:
                errs.append("border tile 1 is not flat 6: PRESS START's blink would show holes")
            if set(idx) - {6, 10, 11, 12, 15}:
                errs.append("border uses indices with no role: %s" % sorted(set(idx) - {6, 10, 11, 12, 15}))
        if piece == "band":
            if set(px[:64]) != {0} or set(px[128:]) != {2}:
                errs.append("band tiles 0 and 2 must stay as pret's")
        if piece == "star" and len(set(px)) > 16:
            errs.append("star uses more than 16 colours")
    return errs


def t564_save(files, root):
    for rel, v in files.items():
        dst = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if isinstance(v, str):
            open(dst, "w").write(v)
        else:
            v.save(dst)


def t564_draft(out):
    for piece in T564_PIECES:
        for d in "ABC":
            files = T564_DRAW[piece](d)
            errs = t564_check(piece, files)
            if errs:
                sys.exit("gbatitle --t564: %s %s breaks its contract: %s" % (piece, d, "; ".join(errs)))
            t564_save(files, os.path.join(out, d))
            print("  %-6s %s %-13s %s" % (piece, d, T564_NAMES[piece][d], ", ".join(sorted(files))))
    print("  DRAFT -- nothing in the engine; recommended: %s"
          % ", ".join("%s %s (%s)" % (p, T564_RECOMMENDED[p], T564_NAMES[p][T564_RECOMMENDED[p]]) for p in T564_PIECES))


# ------------------------------------------------------------------------------------------- the sheets, in context
def _gba(c):
    """What mGBA puts on screen for an 8-bit colour: 5 bits a channel, expanded (c5 << 3) | (c5 >> 2)."""
    return tuple(((v >> 3) << 3) | ((v >> 3) >> 2) for v in c[:3])


def _near(a, b, tol=6):
    return all(abs(a[i] - b[i]) <= tol for i in range(3))


def _bg_render(tiles_img, binmap, pal16, bank_pals):
    """One 4bpp background, full screen: (RGB, mask). tiles_img is a P or L PNG; L is read inverted (gbagfx)."""
    w, h = tiles_img.size
    raw = list(tiles_img.getdata())
    if tiles_img.mode == "L":
        raw = [15 - p // 17 for p in raw]
    ts = []
    for ty in range(h // 8):
        for tx in range(w // 8):
            ts.append([raw[(ty * 8 + y) * w + tx * 8 + x] for y in range(8) for x in range(8)])
    d = open(binmap, "rb").read()
    import struct as _st
    ents = _st.unpack("<%dH" % (len(d) // 2), d)
    img = Image.new("RGB", (240, 160)); m = Image.new("L", (240, 160), 0)
    ip, mp = img.load(), m.load()
    for i, e in enumerate(ents):
        r, c = divmod(i, 32)
        if c * 8 >= 240 or r * 8 >= 160:
            continue
        idx, hf, vf, pn = e & 0x3FF, e & 0x400, e & 0x800, e >> 12
        if idx >= len(ts):
            continue
        for y in range(8):
            for x in range(8):
                v = ts[idx][(7 - y if vf else y) * 8 + (7 - x if hf else x)]
                if v == 0:
                    continue
                ip[c * 8 + x, r * 8 + y] = _gba(bank_pals.get(pn, pal16)[v])
                mp[c * 8 + x, r * 8 + y] = 255
    return img, m


def _jasc(path):
    v = open(path).read().split()
    return [tuple(int(x) for x in v[3 + i * 3:6 + i * 3]) for i in range(int(v[2]))]


def _swap_layer(frame, today, draft):
    """Where the filmed frame shows today's layer, show the draft's: a pixel changes only if it is today's colour
    there (so sprites, text and windows over the layer stay as filmed)."""
    out = frame.copy()
    fp, tp, dp, op = frame.load(), today[0].load(), draft[0].load(), out.load()
    tm = today[1].load()
    for y in range(160):
        for x in range(240):
            if tm[x, y] and tp[x, y] != dp[x, y] and _near(fp[x, y], tp[x, y]):
                op[x, y] = dp[x, y]
    return out


def _band_layers(d):
    gf = os.path.join(GBA, "graphics/intro/game_freak")
    if d == "today":
        im, pal = Image.open(os.path.join(gf, "bg.png")), _jasc(os.path.join(gf, "bg.pal"))
    else:
        f = t564_band(d)
        im = f["graphics/intro/game_freak/bg.png"]; pal = T564_BAND_PAL
    return _bg_render(im, os.path.join(gf, "bg.bin"), pal, {})


def _border_layers(d, sub):
    ts = os.path.join(GBA, "graphics/title_screen")
    im = Image.open(os.path.join(ts, "border_bg.png")) if d == "today" else t564_border(d)["graphics/title_screen/border_bg.png"]
    pal = _jasc(os.path.join(ts, sub, "background.pal"))
    return _bg_render(im, os.path.join(ts, sub, "border_bg.bin"), pal, {14: pal, 15: pal})


def _star_box(frame):
    px = frame.load()
    pts = [(x, y) for y in range(160) for x in range(240)
           if px[x, y][0] > 48 and abs(px[x, y][0] - px[x, y][1]) < 12 and px[x, y][2] < 40]
    if not pts:
        return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def _paste_sprite(frame, sprite, pal, x0, y0):
    out = frame.copy(); op = out.load(); sp = sprite.load()
    for y in range(sprite.height):
        for x in range(sprite.width):
            v = sp[x, y]
            if v and 0 <= x0 + x < 240 and 0 <= y0 + y < 160:
                op[x0 + x, y0 + y] = _gba(pal[v])
    return out


def _star_in(frame, d, band_d):
    box = _star_box(frame)
    base = _swap_layer(frame, _band_layers("today"), _band_layers(band_d))
    if d == "today" or box is None:
        return base
    x0, y0 = box[2] - 15, box[3] - 15          # the star's art fills its 16x16 to the right and bottom edges
    clean = base.copy(); cp = clean.load(); bl = _band_layers(band_d)[0].load()
    for y in range(box[1], box[3] + 1):
        for x in range(box[0], box[2] + 1):
            p = cp[x, y]
            if p[0] > 48 and abs(p[0] - p[1]) < 12 and p[2] < 40:
                cp[x, y] = bl[x, y]
    return _paste_sprite(clean, t564_star(d)["graphics/intro/game_freak/star.png"], T564_STAR_PAL, x0, y0)


def _lighten(c, bldy=13):
    return tuple(min(255, v + ((255 - v) * bldy) // 16) for v in c)


def _slash_mask(d):
    im = Image.open(os.path.join(GBA, "graphics/title_screen/slash.png")) if d == "today" \
        else t564_slash(d)["graphics/title_screen/slash.png"]
    return im


def _logo_mask(sub):
    """BG0's ink: the logo, from gbatitleview's own layer reader."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gbatitleview", os.path.join(ROOT, "tools", "gbatitleview.py"))
    tv = importlib.util.module_from_spec(spec); spec.loader.exec_module(tv)
    E = os.path.join(GBA, "graphics/title_screen", sub)
    return tv.layer(os.path.join(E, "game_title_logo.8bpp"), os.path.join(E, "game_title_logo.bin"), 8,
                    tv.pal(os.path.join(E, "game_title_logo.pal")))


def _slash_at(frame_lit, logo_mask):
    """Where pret's slash was when this frame was filmed: the offset whose window best covers the lightened pixels."""
    m = _slash_mask("today").load()
    lm = logo_mask.load(); fp = frame_lit.load()
    lit = {(x, y) for y in range(64) for x in range(240) if lm[x, y] and sum(fp[x, y]) > 600}
    best = (-1, 0, 0)
    for oy in range(-8, 24):
        for ox in range(-64, 240, 1):
            hit = sum(1 for (x, y) in lit if 0 <= x - ox < 64 and 0 <= y - oy < 64 and m[x - ox, y - oy])
            if hit > best[0]:
                best = (hit, ox, oy)
    return best[1], best[2]


def _slash_in(frame_lit, frame_unlit, d, sub, at):
    """The unlit frame, lightened inside the draft's window at the filmed position (BG0 only, as the hardware)."""
    if d == "today":
        return frame_lit
    logo, lm = _logo_mask(sub)
    out = frame_unlit.copy(); op = out.load(); fp = frame_unlit.load(); lmp = lm.load()
    m = _slash_mask(d).load(); ox, oy = at
    for y in range(64):
        for x in range(64):
            X, Y = ox + x, oy + y
            if m[x, y] and 0 <= X < 240 and 0 <= Y < 160 and lmp[X, Y]:
                op[X, Y] = _lighten(fp[X, Y])
    return out


def _offline_title(sub, border_d="today", slash_d=None, slash_at=None):
    """CONTEXT's title, composited offline (gbatitleview's reader) -- the theatre route films CONTENT's debug ROM."""
    import importlib.util, io, contextlib
    spec = importlib.util.spec_from_file_location("gbatitleview", os.path.join(ROOT, "tools", "gbatitleview.py"))
    tv = importlib.util.module_from_spec(spec); spec.loader.exec_module(tv)
    tmp = daemonslib_preview("t564_offline_%s.png" % sub)
    argv = sys.argv
    sys.argv = ["gbatitleview", "content" if sub == "firered" else "context", "--out", tmp]
    with contextlib.redirect_stdout(io.StringIO()):
        tv.main()
    sys.argv = argv
    im = Image.open(tmp).convert("RGB").resize((240, 160), Image.NEAREST)
    im = Image.eval(im, lambda v: v)
    if border_d != "today":
        im = _swap_layer(im, _border_layers("today", sub), _border_layers(border_d, sub))
    if slash_d:
        logo, lm = _logo_mask(sub)
        op = im.load(); lmp = lm.load(); m = _slash_mask(slash_d).load(); ox, oy = slash_at
        for y in range(64):
            for x in range(64):
                X, Y = ox + x, oy + y
                if m[x, y] and 0 <= X < 240 and 0 <= Y < 160 and lmp[X, Y]:
                    op[X, Y] = _lighten(op[X, Y])
    return im


def daemonslib_preview(name):
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import daemonslib
    return daemonslib.preview(name)


def _frames(fdir):
    import re
    fs = [f for f in os.listdir(fdir) if re.match(r"s02_\d+_b_\d+\.png$", f)]
    key = lambda f: tuple(int(v) for v in re.findall(r"\d+", f)[1:])
    return [os.path.join(fdir, f) for f in sorted(fs, key=key)]


def _asset_view(piece, d, scale=8):
    """The asset itself, on the colour it is seen against."""
    if piece == "star":
        im = t564_star(d)["graphics/intro/game_freak/star.png"] if d != "today" else \
            Image.open(os.path.join(GBA, "graphics/intro/game_freak/star.png"))
        pal = T564_STAR_PAL if d != "today" else [tuple(im.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
        bg = Image.new("RGB", im.size, (24, 41, 74)); bp = bg.load(); sp = im.load()
        for y in range(im.height):
            for x in range(im.width):
                if sp[x, y]:
                    bp[x, y] = _gba(pal[sp[x, y]])
        return bg.resize((im.width * scale, im.height * scale), Image.NEAREST)
    if piece == "slash":
        im = _slash_mask(d); out = Image.new("RGB", (64, 64), (8, 16, 33)); op = out.load(); sp = im.load()
        for y in range(64):
            for x in range(64):
                if sp[x, y]:
                    op[x, y] = (230, 236, 246)
        return out.resize((64 * 3, 64 * 3), Image.NEAREST)
    if piece == "border":
        im = Image.open(os.path.join(GBA, "graphics/title_screen/border_bg.png")) if d == "today" else \
            t564_border(d)["graphics/title_screen/border_bg.png"]
        out = Image.new("RGB", (36, 32), (22, 22, 28))
        for k, sub in enumerate(("firered", "leafgreen")):
            pal = _jasc(os.path.join(GBA, "graphics/title_screen", sub, "background.pal"))
            for y in range(32):
                for x in range(8):
                    for rep in range(2):
                        out.putpixel((k * 20 + rep * 8 + x, y), _gba(pal[15 - im.getpixel((x, y)) // 17]))
        return out.resize((36 * 6, 32 * 6), Image.NEAREST)
    im = Image.open(os.path.join(GBA, "graphics/intro/game_freak/bg.png")) if d == "today" else \
        t564_band(d)["graphics/intro/game_freak/bg.png"]
    pal = _jasc(os.path.join(GBA, "graphics/intro/game_freak/bg.pal")) if d == "today" else T564_BAND_PAL
    out = Image.new("RGB", (32, 24))
    for y in range(24):
        for x in range(32):
            out.putpixel((x, y), _gba(pal[im.getpixel((x % 8, y))]))
    return out.resize((32 * 8, 24 * 8), Image.NEAREST)


def t564_sheets(out_dir, fdir):
    from PIL import ImageDraw, ImageFont
    fs = _frames(fdir)
    if len(fs) < 340:
        sys.exit("gbatitle --t564: film the boot first (tools/theatre_route.py tools/routes/film_t564_boot.json)")
    F = lambda k: Image.open(fs[k]).convert("RGB")
    star_frames = [F(26), F(28)]
    thanks = F(124)
    title = F(300)
    lit = [k for k in range(280, len(fs)) if _star_box(F(k)) is None and
           sum(1 for p in F(k).crop((0, 0, 240, 60)).getdata() if p[0] > 240) > 50]
    lit_k = lit[0] if lit else 334
    lit_f = F(lit_k)
    calm = list(F(300).crop((0, 0, 240, 56)).getdata())      # the logo with no glint on it

    def glinted(k):
        return sum(1 for a, b in zip(F(k).crop((0, 0, 240, 56)).getdata(), calm) if abs(sum(a) - sum(b)) > 60)
    unlit_k = next(k for k in range(lit_k - 1, 279, -1) if glinted(k) < 20)
    unlit_f = F(unlit_k)
    logo, lmask = _logo_mask("firered")
    at = _slash_at(lit_f, lmask)
    try:
        font = ImageFont.load_default(size=15); big = ImageFont.load_default(size=22)
    except TypeError:
        font = big = ImageFont.load_default()
    os.makedirs(out_dir, exist_ok=True)
    made = []
    X2 = lambda im: im.resize((480, 320), Image.NEAREST)
    for piece in T564_PIECES:
        cols = ["today", "A", "B", "C"]
        rows = []
        for d in cols:
            r = [_asset_view(piece, d)]
            if piece == "star":
                r += [X2(_star_in(f, d, "today")) for f in star_frames]
            elif piece == "band":
                r += [X2(_star_in(star_frames[1], "today", d if d != "today" else "today")),
                      X2(_swap_layer(thanks, _band_layers("today"), _band_layers(d)) if d != "today" else thanks)]
            elif piece == "slash":
                r += [X2(_slash_in(lit_f, unlit_f, d, "firered", at)),
                      X2(_offline_title("leafgreen", slash_d=None if d == "today" else d, slash_at=at)
                         if d != "today" else _offline_title("leafgreen", slash_d="today", slash_at=at))]
            else:
                r += [X2(_swap_layer(title, _border_layers("today", "firered"), _border_layers(d, "firered"))
                         if d != "today" else title),
                      X2(_offline_title("leafgreen", border_d=d))]
            rows.append(r)
        cw, pad, head = 490, 10, 70
        hs = [max(r[i].height for r in rows) for i in range(3)]
        W = pad + len(cols) * (cw + pad); H = head + sum(h + 34 for h in hs) + pad
        sheet = Image.new("RGB", (W, H), (22, 22, 28)); dr = ImageDraw.Draw(sheet)
        dr.text((pad, 8), "T-564 DRAFT -- %s: %s" % (piece.upper(), ", ".join(T564_FILES[piece])), fill=(240, 240, 240), font=big)
        dr.text((pad, 38), "today (pret's) beside A/B/C, 2x; nothing in the engine until picked. Recommended: %s %s"
                % (T564_RECOMMENDED[piece], T564_NAMES[piece][T564_RECOMMENDED[piece]]), fill=(200, 200, 210), font=font)
        captions = {"star": ["the asset, 8x, on the band", "in flight (filmed, CONTENT debug, capture 26)",
                             "in flight, two frames on (filmed)"],
                    "band": ["three tiles' band, 8x", "under the star and its trail (filmed)",
                             "under the thank-you card (filmed)"],
                    "slash": ["the window's shape, 3x (white = lit)", "crossing DAEMONS (CONTENT, filmed position)",
                              "CONTEXT, same position (offline render)"],
                    "border": ["tiles 0-3, 6x: CONTENT | CONTEXT", "CONTENT title (filmed)",
                               "CONTEXT title (offline render, gbatitleview)"]}[piece]
        for ci, d in enumerate(cols):
            x = pad + ci * (cw + pad); y = head
            label = "TODAY (pret's)" if d == "today" else "%s  %s" % (d, T564_NAMES[piece][d])
            for ri, im in enumerate(rows[ci]):
                dr.text((x, y), label + ("" if ri else "") if ri == 0 else captions[ri], fill=(235, 220, 140) if ri == 0 else (170, 170, 180), font=font)
                if ri == 0 and d != "today":
                    pass
                sheet.paste(im, (x, y + 22))
                if ri == 0:
                    dr.text((x + im.width + 8, y + 26), captions[0], fill=(150, 150, 160), font=font)
                y += hs[ri] + 34
        path = os.path.join(out_dir, "t564_%s.png" % piece)
        sheet.save(path)
        made.append(path)
        print("  sheet %s" % path)
    #  today's boot as filmed, in order, each frame labelled with what is still pret's in it
    strip = [(0, "copyright: ours (gbacopyright)"), (26, "splash: pret's BAND and STAR; our 0/1 and notes"),
             (44, "the trail becomes notes (ours)"), (60, "CODEMUSIC wordmark (ours) on pret's band"),
             (75, "the ring mark (ours); no PRESENTS (REVISION 0)"), (124, "thank-you card (ours) on pret's band"),
             (140, "title reveal: the face-off (ours)"), (300, "title: pret's BORDER tiles, our palette"),
             (lit_k, "title: pret's SLASH glint across DAEMONS")]
    sw, sh = 240, 160
    ov = Image.new("RGB", (10 + 3 * (sw * 2 + 10), 70 + 3 * (sh * 2 + 30)), (22, 22, 28))
    od = ImageDraw.Draw(ov)
    od.text((10, 8), "T-564 -- today's boot, filmed from reset (CONTENT debug ROM, tools/routes/film_t564_boot.json), 2x",
            fill=(240, 240, 240), font=big)
    od.text((10, 38), "captures every 8 frames (4 for the last burst); what is still pret's is named over each", fill=(200, 200, 210), font=font)
    for i, (k, cap) in enumerate(strip):
        x, y = 10 + (i % 3) * (sw * 2 + 10), 70 + (i // 3) * (sh * 2 + 30)
        od.text((x, y), "capture %d: %s" % (k, cap), fill=(235, 220, 140), font=font)
        ov.paste(F(k).resize((sw * 2, sh * 2), Image.NEAREST), (x, y + 22))
    path = os.path.join(out_dir, "t564_boot_today.png"); ov.save(path); made.append(path)
    print("  sheet %s" % path)
    print("  slash filmed at frame %d (drafts lit over frame %d), window at %s" % (lit_k, unlit_k, at))
    return made


def t564_report():
    print("gbatitle --t564 (T-564): the boot's last pret pieces. APPROVED_564: %s"
          % (APPROVED_564 or "none -- nothing is written"))
    for piece in T564_PIECES:
        for d in "ABC":
            errs = t564_check(piece, T564_DRAW[piece](d))
            print("  %-6s %s %-13s %s" % (piece, d, T564_NAMES[piece][d], "ok" if not errs else "; ".join(errs)))
    drift = []
    for piece, d in APPROVED_564.items():
        for rel, v in T564_DRAW[piece](d).items():
            dst = os.path.join(GBA, rel)
            if isinstance(v, str):
                same = os.path.exists(dst) and open(dst).read() == v
            else:
                same = os.path.exists(dst) and list(Image.open(dst).getdata()) == list(v.getdata())
            if not same:
                drift.append(rel)
    for rel in drift:
        print("  DRIFT: engineGba/%s is not what --t564 --write --approved makes" % rel)
    return 1 if drift else 0


def t564_main():
    a = sys.argv
    if "--write" in a:
        if "--approved" not in a:
            sys.exit("gbatitle --t564: --write needs --approved (it writes APPROVED_564, the user's picks)")
        if not APPROVED_564:
            print("gbatitle --t564: nothing approved yet (T-564 is a DRAFT); nothing written")
            return 0
        for piece, d in APPROVED_564.items():
            t564_save(T564_DRAW[piece](d), GBA)
            print("  wrote %s %s (%s)" % (piece, d, T564_NAMES[piece][d]))
        return 0
    if "--draft" in a:
        i = a.index("--draft")
        out = a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else T564_DRAFT
        t564_draft(out)
    if "--sheets" in a:
        fdir = a[a.index("--frames") + 1] if "--frames" in a else T564_FRAMES
        t564_sheets(a[a.index("--sheets") + 1], fdir)
    if "--draft" not in a and "--sheets" not in a:
        return t564_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())

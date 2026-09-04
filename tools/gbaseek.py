#!/usr/bin/env python3
"""Cut SEEKMUSAI's intro rig out of the generated art.

    python3 tools/gbaseek.py            # report + /tmp/seek.png
    python3 tools/gbaseek.py --write

THE RIG IS THREE SPRITES, NOT ONE PICTURE. oak_speech.c draws the intro
creature as a body (32x32), an "ears" overlay (32x16) and an "eyes" overlay
(16x8), two frames each -- a slow breath, a periodic twitch, a blink. For a
MUSAI that is body, ANTENNAE and VISOR, so SEEKMUSAI blinks by its scanner
cycling: the right verb for the one whose item is EMBEDDING.

ONLY THE BODY IS DRAWN ART. Gemini produced all three layers and the two
overlays do not seam -- the antennae sat on a plain dome while the body has a
swept crest, and the visor was a different faceplate shape. Overlaid, the
helmet would change shape every time it twitched or blinked.

So THE OVERLAYS ARE BUILT FROM THE BODY: the antennae layer is the body's own
top sixteen rows with stalks drawn onto them, and the visor layer its own
faceplate with a scan-line drawn across it. The seam is exact by construction,
because the surrounding pixels are the same pixels.

TWO THINGS ABOUT THE GEOMETRY.

Vanilla's body is an EARLESS Pikachu sitting low in its 32x32, with the ears
rising into the space above it. Ours leaves the same headroom for the antennae,
which is why the creature is 26 rows dropped to y=6 rather than filling it.

And THE VISOR SPRITE MOVES DOWN FOUR PIXELS. Vanilla puts it at (24,13),
which is where Pikachu's eyes are; SEEKMUSAI's faceplate sits lower, and
solving the placement against the vanilla box forced the creature down to
sixteen pixels wide. Moving one coordinate in oak_speech.c was cheaper than
shrinking the character. The overlay only has to cover the SCAN-LINE, not the
whole faceplate -- the body's faceplate is already dark and static underneath.
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "gfx/intro/seekmusai_body.jpeg")
DST = os.path.join(ROOT, "engineGba/graphics/oak_speech/pikachu_intro")
KEY = (255, 0, 255)
SCAN = (198, 240, 232)      # the scanner line -- the ear-cups' ice-mint

BODY_H, BODY_Y, BODY_X = 26, 6, 9   # the creature inside its 32x32 cell
EARS_AT = (0, 0, 32, 16)            # body-local, matches CreateSprite(...,16,9)
EYES_AT = (16, 12, 16, 8)           # body-local, needs CreateSprite(...,24,17)
COLOURS = 15                        # index 0 is the sprite's transparent slot

def source_frames():
    """Both creature frames on ONE crop box, so they cannot drift apart."""
    im = Image.open(SRC).convert("RGB")
    a = np.asarray(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ink = ~((r > 170) & (b > 170) & (g < 110))
    H = ink.shape[0]; half = H // 2
    boxes = []
    for sl in (slice(0, half), slice(half, H)):
        lab, n = ndimage.label(ink[sl])
        sz = ndimage.sum(ink[sl], lab, range(1, n + 1))
        # Largest blob is the creature; the rest is the "A"/"B" Gemini burns
        # into the corner, which a plain bounding box would swallow.
        ys, xs = np.where(lab == int(np.argmax(sz)) + 1)
        boxes.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))
    x0 = min(q[0] for q in boxes); x1 = max(q[2] for q in boxes)
    y0 = min(q[1] for q in boxes); y1 = max(q[3] for q in boxes)
    return [im.crop((x0, y0 + off, x1 + 1, y1 + 1 + off)) for off in (0, half)]

def cell(frame):
    w = max(1, round(frame.width * BODY_H / frame.height))
    out = Image.new("RGB", (32, 32), KEY)
    out.paste(frame.resize((w, BODY_H), Image.LANCZOS), (BODY_X, BODY_Y))
    return out

def top_edge(c):
    """For each column, the first solid row -- the silhouette's upper outline.
    The stalks grow from this, so they meet the helmet instead of floating."""
    a = np.asarray(c).astype(int)
    solid = ~((a[..., 0] > 170) & (a[..., 2] > 170) & (a[..., 1] < 110))
    out = {}
    for x in range(solid.shape[1]):
        ys = np.where(solid[:, x])[0]
        if len(ys):
            out[x] = int(ys.min())
    return out

def dome(c):
    """The head's left and right edge, taken from the rows the helmet owns."""
    a = np.asarray(c).astype(int)
    solid = ~((a[..., 0] > 170) & (a[..., 2] > 170) & (a[..., 1] < 110))
    xs = np.where(solid[BODY_Y:BODY_Y + 7].any(axis=0))[0]
    return int(xs.min()), int(xs.max())

def line(put, x0, y0, x1, y1, col):
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        put(x0, y0, col)
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 >= dy: err += dy; x0 += sx
        if e2 <= dx: err += dx; y0 += sy

def stalk(draw, x, y, tipx, tipy, ramp):
    """A thin antenna with a small bright tip. Drawn as a CONTINUOUS line --
    the first version alternated colours per step and came out as dashes."""
    H, W = len(draw), len(draw[0])
    def put(px, py, col):
        if 0 <= px < W and 0 <= py < H:
            draw[py][px] = col
    dark, mid, light = ramp
    line(put, x, y, tipx, tipy, dark)
    for ox, oy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        put(tipx + ox - 1, tipy + oy - 1, light)
    put(tipx - 1, tipy - 2, dark); put(tipx, tipy - 2, dark)

def to_grid(img):
    return [[tuple(p) for p in row] for row in np.asarray(img.convert("RGB"))]

def from_grid(g):
    return Image.fromarray(np.array(g, dtype=np.uint8), "RGB")

def breath(a):
    """Frame B is frame A DROPPED ONE PIXEL, with the shadow left where it is.

    Not Gemini's second frame, which is a full crouch. SpriteCB_Pikachu sets
    each overlay's y2 to the body's animCmdIndex -- 0 or 1 -- so the antennae
    and the visor follow the body by exactly ONE pixel. A body that moves by
    more than that tears away from its own overlays, and the helmet doubles."""
    arr = np.asarray(a).astype(int)
    mag = (arr[..., 0] > 170) & (arr[..., 2] > 170) & (arr[..., 1] < 110)
    grey = (arr.max(axis=2) - arr.min(axis=2) < 46) & ~mag
    rows = [y for y in range(20, 32) if grey[y].sum() > 3]
    floor = min(rows) if rows else 30
    out = np.array(arr, dtype=np.uint8)
    out[1:floor] = arr[0:floor - 1]
    return Image.fromarray(out, "RGB"), floor

def build():
    a = cell(source_frames()[0])
    b, floor = breath(a)
    body = Image.new("RGB", (32, 64), KEY)
    body.paste(a, (0, 0)); body.paste(b, (0, 32))

    # the ramp the antennae are drawn in, taken from the body's own reds
    arr = np.asarray(a).astype(int)
    solid = ~((arr[..., 0] > 170) & (arr[..., 2] > 170) & (arr[..., 1] < 110))
    reds = arr[solid & (arr[..., 0] > arr[..., 2] + 20)]
    lum = reds.sum(axis=1)
    ramp = (tuple(reds[lum.argmin()]), tuple(reds[np.argsort(lum)[len(lum) // 2]]),
            tuple(reds[lum.argmax()]))

    left, right = dome(a)
    edge = top_edge(a)
    # A quarter in from each side of the helmet, on its own upper outline.
    ax = left + max(1, (right - left) // 4)
    bx = right - max(1, (right - left) // 4)
    ay, by = edge.get(ax, BODY_Y), edge.get(bx, BODY_Y)
    ears = []
    for (ldx, ldy), (rdx, rdy) in (((-3, -6), (3, -6)), ((-5, -3), (5, -3))):
        g = to_grid(a.crop((0, 0, 32, 16)))
        stalk(g, ax, ay, ax + ldx, max(1, ay + ldy), ramp)
        stalk(g, bx, by, bx + rdx, max(1, by + rdy), ramp)
        ears.append(from_grid(g))
    ears_sheet = Image.new("RGB", (32, 32), KEY)
    ears_sheet.paste(ears[0], (0, 0)); ears_sheet.paste(ears[1], (0, 16))

    ex, ey, ew, eh = EYES_AT
    face = a.crop((ex, ey, ex + ew, ey + eh))
    lit = to_grid(face)
    # The faceplate by LUMINANCE, not by an exact colour match -- the source is
    # a JPEG, so no two faceplate pixels are the same tuple and comparing
    # tuples found nothing at all.
    row = eh // 2
    dark_cols = [x for x in range(ew) if sum(int(v) for v in lit[row][x]) < 210]
    if dark_cols:
        lo, hi = min(dark_cols), max(dark_cols)
        for x in range(lo, hi + 1):
            lit[row][x] = SCAN
        lit[row - 1][hi] = SCAN            # the reticle point, offset high-right
    eyes_sheet = Image.new("RGB", (32, 8), KEY)
    eyes_sheet.paste(from_grid(lit), (0, 0))
    eyes_sheet.paste(face, (16, 0))        # frame 2: unlit, the body's own pixels
    return body, ears_sheet, eyes_sheet, (left, right, ax, bx, floor), ramp

def quantise(layers):
    """One palette for all three sheets -- they share PAL_TAG_PIKACHU."""
    W = sum(l.width for l in layers); H = max(l.height for l in layers)
    master = Image.new("RGB", (W, H), KEY); x = 0
    for l in layers:
        master.paste(l, (x, 0)); x += l.width
    q = master.convert("P", palette=Image.ADAPTIVE, colors=COLOURS, dither=Image.NONE)
    pal = q.getpalette()[:COLOURS * 3]
    table = [KEY] + [tuple(pal[i * 3:i * 3 + 3]) for i in range(COLOURS)]
    def index(img):
        a = np.asarray(img.convert("RGB")).astype(int)
        out = Image.new("P", img.size)
        flat = np.zeros(img.size[::-1], dtype=np.uint8)
        mag = (a[..., 0] > 170) & (a[..., 2] > 170) & (a[..., 1] < 110)
        cand = np.array(table[1:])
        d = ((a[:, :, None, :] - cand[None, None, :, :]) ** 2).sum(axis=3)
        flat = (d.argmin(axis=2) + 1).astype(np.uint8)
        flat[mag] = 0
        out.putdata(flat.flatten().tolist())
        p = []
        for c in table: p += list(c)
        out.putpalette(p + [0] * (768 - len(p)))
        return out
    return [index(l) for l in layers], table

def main():
    body, ears, eyes, (left, right, ax, bx, floor), ramp = build()
    print("  creature   %d rows at y=%d, x=%d in a 32x32 cell" % (BODY_H, BODY_Y, BODY_X))
    print("  helmet     x %d..%d; stalks at x=%d and x=%d, on its own outline"
          % (left, right, ax, bx))
    print("  breath     frame A dropped 1px above row %d; the shadow stays" % floor)
    print("  ramp       dark #%02X%02X%02X  mid #%02X%02X%02X  light #%02X%02X%02X"
          % (ramp[0] + ramp[1] + ramp[2]))
    (pb, pe, py), table = quantise([body, ears, eyes])
    print("  palette    %d colours, index 0 transparent" % COLOURS)

    # THE PREVIEW COMPOSITES, because sheets do not show seams. Body, then the
    # antennae overlay over its top sixteen rows, then the visor patch -- the
    # same order and the same offsets the hardware uses.
    def compose(bodyf, earsf, eyesf):
        out = pb.convert("RGB").crop((0, 32 * bodyf, 32, 32 * bodyf + 32))
        # SpriteCB_Pikachu: y2 = the body's animCmdIndex, so the overlays drop
        # with the breath. Without this the preview lies about the seam.
        dy = bodyf
        for img, (ox, oy), fr, fh in ((pe, (0, dy), earsf, 16),
                                      (py, (EYES_AT[0], EYES_AT[1] + dy), eyesf, 8)):
            src = img.convert("RGB")
            w = 32 if fh == 16 else 16
            cell_ = src.crop((0, fh * fr, w, fh * fr + fh)) if fh == 16 else \
                    src.crop((w * fr, 0, w * fr + w, fh))
            idx = img.crop((0, fh * fr, w, fh * fr + fh)) if fh == 16 else \
                  img.crop((w * fr, 0, w * fr + w, fh))
            data = list(idx.getdata())
            cp = cell_.load()
            for j in range(fh):
                for i in range(w):
                    if data[j * w + i]:
                        out.putpixel((ox + i, oy + j), cp[i, j])
        return out

    S = 12
    states = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    labels = ["rest", "breath", "twitch", "blink"]
    prev = Image.new("RGB", ((32 * S + 12) * 4, 32 * S + 4), (18, 18, 24))
    for n, st in enumerate(states):
        prev.paste(compose(*st).resize((32 * S, 32 * S), Image.NEAREST),
                   (n * (32 * S + 12), 2))
    prev.save("/tmp/seek.png")
    print("  preview    /tmp/seek.png  -- %s" % ", ".join(labels))

    if "--write" in sys.argv:
        pb.save(os.path.join(DST, "body.png"))
        pe.save(os.path.join(DST, "ears.png"))
        py.save(os.path.join(DST, "eyes.png"))
        with open(os.path.join(DST, "pikachu.pal"), "w") as f:
            f.write("JASC-PAL\n0100\n16\n")
            for c in table: f.write("%d %d %d\n" % c)
        print("  written    body.png, ears.png, eyes.png, pikachu.pal")

main()

#!/usr/bin/env python3
"""WIND's overworld sprites, recoloured from Ruby's sand to autumn leaves (T-415; DRAFT art).

    python3 tools/genwindleaves.py            # report, and a preview in the scratch dir
    python3 tools/genwindleaves.py --write    # graphics/weather/sandstorm.png (the build makes its .gbapal from it)

T-415 (the user, 2026-10-17): autumn's weather is "wind-and-leaves (a recoloured sandstorm)". Phase 1 put WIND on
Ruby's sandstorm as it was -- orange specks -- and left the leaves. This draws them: the same sheet and the same
motion (`field_weather_effects.c` tiles a 64x64 frame five across and sends five 32x32 swirls up the screen), so no
code changes, only the art and its palette.

THE SHEET is 64x80 cut 8x8 row by row: tiles 0..63 are the 64x64 frame (one row of eight tiles per eight pixels, the
1D mapping), tiles 64..79 the 32x32 swirl, which the sprite reads as a 4x4 block -- so the swirl is drawn whole and
its sixteen tiles laid two rows of eight into the sheet. The frame wraps at its edges (a leaf leaving the right edge
re-enters at the left), because the five copies sit edge to edge.

PALETTE-SAFE: the weather's own slot, index 0 clear and seven autumn colours -- sand's eight entries, no more -- so it
spends nothing new and the watch's tint and the season's palettes treat it as they treated the sand. Fewer marks than
the sand's 330 specks (a leaf is three to six pixels, so a frame holds about twenty), each a small leaf in one of four
shapes, a body colour and a darker stem end. Deterministic: a fixed seed.
"""
import os, random, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PNG = os.path.join(GBA, "graphics/weather/sandstorm.png")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

#  0 clear, then the leaves: three bodies, a highlight, two stems, and an early-autumn green
PALETTE = [(0, 0, 0), (232, 192, 64), (216, 120, 40), (176, 56, 32), (248, 224, 120), (120, 72, 32),
           (80, 40, 24), (136, 152, 48)]
BODIES = (1, 1, 2, 2, 3, 7)                                     # yellow and orange most, red and green fewer
LIGHT, STEM, DARK = 4, 5, 6

#  a leaf: rows of '.', 'b' body, 'h' highlight, 's' stem -- four shapes, each also mirrored
SHAPES = [
    [".bb",
     "bs."],
    [".hb",
     "bbs",
     "b.."],
    ["hb.",
     "bbb",
     ".bs"],
    [".hbb",
     "bbb.",
     "s..."],
]


def jasc_free(rgb):
    return tuple(v >> 3 << 3 for v in rgb)                    # what the GBA's 15 bits keep


def leaf(g, w, h, x0, y0, rng, wrap):
    shape = rng.choice(SHAPES)
    if rng.random() < 0.5:
        shape = [r[::-1] for r in shape]
    if rng.random() < 0.5:
        shape = shape[::-1]
    body = rng.choice(BODIES)
    stem = DARK if body == 3 else STEM
    for dy, row in enumerate(shape):
        for dx, ch in enumerate(row):
            if ch == ".":
                continue
            x, y = x0 + dx, y0 + dy
            if wrap:
                x, y = x % w, y % h
            elif not (0 <= x < w and 0 <= y < h):
                continue
            g[y][x] = {"b": body, "h": LIGHT if body != 3 else 2, "s": stem}[ch]


def scatter(w, h, n, rng, wrap, gap=2):
    """n leaves, none touching another (a gap of `gap` pixels), placed by rejection."""
    g = [[0] * w for _ in range(h)]
    boxes = []
    tries = 0
    while len(boxes) < n and tries < 5000:
        tries += 1
        x, y = rng.randrange(w), rng.randrange(h)
        if not wrap and (x > w - 4 or y > h - 3):
            continue
        clash = False
        for bx, by in boxes:
            dx = min(abs(x - bx), w - abs(x - bx)) if wrap else abs(x - bx)
            dy = min(abs(y - by), h - abs(y - by)) if wrap else abs(y - by)
            if dx < 4 + gap and dy < 3 + gap:
                clash = True
                break
        if clash:
            continue
        boxes.append((x, y))
        leaf(g, w, h, x, y, rng, wrap)
    return g


def swirl(rng):
    """the 32x32 gust: leaves round a loose ring, as the sand swirled."""
    import math
    g = [[0] * 32 for _ in range(32)]
    for i in range(7):
        a = i * (2 * math.pi / 7) + rng.random() * 0.4
        r = 9 + rng.random() * 4
        x = int(round(15 + r * math.cos(a))) - 1
        y = int(round(15 + r * math.sin(a))) - 1
        leaf(g, 32, 32, x, y, rng, False)
    return g


def draw():
    rng = random.Random(415)
    frame = scatter(64, 64, 20, rng, True)
    sw = swirl(rng)
    sheet = [[0] * 64 for _ in range(80)]
    for y in range(64):
        sheet[y] = frame[y][:]
    for k in range(16):                                         # swirl tile k (4x4, 1D) -> sheet tile 64 + k
        sx, sy = (k % 4) * 8, (k // 4) * 8
        t = 64 + k
        tx, ty = (t % 8) * 8, (t // 8) * 8
        for y in range(8):
            for x in range(8):
                sheet[ty + y][tx + x] = sw[sy + y][sx + x]
    im = Image.new("P", (64, 80), 0)
    pal = [jasc_free(c) for c in PALETTE] + [(0, 0, 0)] * (16 - len(PALETTE))
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    im.putdata([v for row in sheet for v in row])
    return im, frame, sw, pal


def preview(frame, sw, pal):
    os.makedirs(SCRATCH, exist_ok=True)
    bg = Image.new("RGB", (64 * 3 + 32, 64), (96, 136, 72))      # a grass green, to see them on
    px = bg.load()
    for ox in (0, 64, 128):
        for y in range(64):
            for x in range(64):
                if frame[y][x]:
                    px[ox + x, y] = pal[frame[y][x]]
    for y in range(32):
        for x in range(32):
            if sw[y][x]:
                px[192 + x, y] = pal[sw[y][x]]
    out = os.path.join(SCRATCH, "windleaves_preview.png")
    bg.resize((bg.width * 4, bg.height * 4), Image.NEAREST).save(out)
    return out


def main():
    im, frame, sw, pal = draw()
    marks = sum(1 for row in frame for v in row if v)
    print("  WIND's leaves: a 64x64 frame of %d leaf pixels, a 32x32 swirl, %d colours in the weather's slot"
          % (marks, len(PALETTE) - 1))
    out = preview(frame, sw, pal)
    cur_png = Image.open(PNG) if os.path.exists(PNG) else None
    same_png = cur_png is not None and list(cur_png.getdata()) == list(im.getdata()) \
        and cur_png.getpalette()[:48] == im.getpalette()[:48]
    if same_png:
        print("  sandstorm.png is current")
        return
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % out)
        return
    im.save(PNG, bits=4)
    print("  written")


if __name__ == "__main__":
    main()

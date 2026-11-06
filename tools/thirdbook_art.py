#!/usr/bin/env python3
"""T-519: DRAFT art for the third book's three forms -- THE HERMETIC LAYER (the night half), THE EUDAIMON LAYER (the
dawn half) and THE UNITY BOOK (mended) -- to replace the placeholders tools/gensubtle.py writes for them.

    python3 tools/thirdbook_art.py                     # report the limits of every draft, write nothing
    python3 tools/thirdbook_art.py --out DIR           # every draft as the indexed PNG the build would convert, and
                                                       # a contact sheet (each draft at 2x beside its placeholder)
    python3 tools/thirdbook_art.py --out DIR --forge F # also quantize the ComfyUI plates in F (spriteforge drafts)

NOTHING HERE WRITES INTO THE GAME: tools/gensubtle.py draws PICTURES into it. Batches 2 and 3 (approved 2026-11-05
and 06, with EVERY FOLD, the dawn's UPPER FOLDS and LET GO redrawn first) follow the opening ones. The drafts are drawn
in each book's own sixteen palette roles (gensubtle.use), so an approved one drops into gensubtle's
cover_*/icon_*/pictures() unchanged. The one exception is offered, never
taken: option B of the dawn half recolours two COVER-ONLY roles (C_SLATE, C_CHALK_FAINT) to sapphire, since the
dawn's palette has no blue; book_reader.c prints neither on a layer book's pages.

The limits, read from gensubtle.py and book_reader.c: a cover is the whole window, 240x160, 600 tiles copied raw
(no tile dedup; 19200 bytes 4bpp); a picture is 96x88, 132 tiles, blitted onto the left page; the bag icon 24x24,
9 tiles, index 0 transparent. Every image: one 16-colour palette, the book's, index 0 C_NONE. In the night half the
reader breathes C_RING (the emerald) and C_COVER (the backdrop): emerald drawn in C_RING pulses, and no picture uses
C_COVER. The CARDS tile sits right of the cover at x 195-239, y 85-152 in the night half and the mended book, so
nothing is drawn there.
"""
import glob, json, math, os, random, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gensubtle as gs
import genguide as g

ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engineGba")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
FORGE = sys.argv[sys.argv.index("--forge") + 1] if "--forge" in sys.argv else None
PW, PH = gs.PIC_W, gs.PIC_H

# Option B of the dawn half: the two cover-only roles in sapphire (5-bit), so the morning has its blue.
SAPPHIRE = {"C_SLATE": (5, 8, 17), "C_CHALK_FAINT": (17, 21, 29)}

C = {}          # role -> RGB8, for the book in use


def use(book, tweak=None):
    gs.use(book)
    if tweak:
        gs.PALETTE = [(n, tweak.get(n, v)) for n, v in gs.PALETTE]
        gs.RGB8 = {n: tuple((c << 3) | (c >> 2) for c in v) for n, v in gs.PALETTE}
    C.clear()
    C.update(gs.RGB8)


def render_indexed(fn, w, h, fill="C_PAPER"):
    """FN's drawing as the indexed PNG(s) the build converts -- a list when it has frames. Drawn in one unique
    sentinel colour per role, then mapped back, so two roles that share a colour keep their own index: in the night
    half C_EDGE_DARK and C_COVER are both (2,1,3), and a picture mapped by colour alone would breathe with the
    backdrop (gs.indexed keeps the last role of a colour). Call after use()."""
    real = dict(C)
    names = [n for n, _ in gs.PALETTE]
    sentinel = {n: (251, 3 + 9 * i, 7 + 11 * i) for i, n in enumerate(names)}
    back = {v: gs.IDX[n] for n, v in sentinel.items()}
    C.clear(); C.update(sentinel)
    try:
        drawn = fn()
    finally:
        C.clear(); C.update(real)
    out = []
    for im in (drawn if isinstance(drawn, list) else [drawn]):
        ind = Image.new("P", (w, h), gs.IDX[fill])
        ind.putpalette([v for n, _ in gs.PALETTE for v in gs.RGB8[n]] + [0] * (768 - 48))
        ox, oy = (w - im.width) // 2, (h - im.height) // 2
        src = im.load()
        for y in range(im.height):
            for x in range(im.width):
                if src[x, y] not in back:
                    raise SystemExit("thirdbook_art: %s draws %s, which is no palette role" % (fn.__name__, src[x, y]))
                ind.putpixel((ox + x, oy + y), back[src[x, y]])
        out.append(ind)
    return out if isinstance(drawn, list) else out[0]


def px(im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height:
        im.putpixel((int(x), int(y)), C[c] if isinstance(c, str) else c)


def stars(im, box, seed, n, roles=("C_FAINT", "C_EDGE", "C_INK")):
    r = random.Random(seed)
    x0, y0, x1, y1 = box
    for k in range(n):
        x, y = r.randrange(x0, x1), r.randrange(y0, y1)
        c = roles[0] if k % 7 else roles[2]
        if k % 3 == 0:
            c = roles[1]
        px(im, x, y, c)
        if k % 17 == 0:                                   # a few bright ones, a cross of four
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                px(im, x + dx, y + dy, roles[0])


def bands(im, box, roles, phase=0):
    """A sky in horizontal bands, each ordered-dithered into the next (top role first)."""
    x0, y0, x1, y1 = box
    n = len(roles) - 1
    bayer = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0 - 1)) * n
        k, f = min(int(t), n - 1), t - min(int(t), n - 1)
        for x in range(x0, x1):
            px(im, x, y, roles[k + 1] if f * 16 > bayer[y % 4][(x + phase) % 4] else roles[k])


def tri(d, cx, cy, r, up, c, fill=None):
    pts = [(cx, cy - r), (cx + r, cy + r * 2 // 3), (cx - r, cy + r * 2 // 3)] if up else \
          [(cx, cy + r), (cx + r, cy - r * 2 // 3), (cx - r, cy - r * 2 // 3)]
    d.polygon(pts, outline=C[c], fill=C[fill] if fill else None)


def tablet(im, x0, y0, x1, y1, face="C_EDGE_DARK", edge="C_RING", lit="C_MARGIN", lines=True, glyphs=True, seed=3):
    """The Emerald Tablet: a stone with a rounded head, an emerald edge lit on its left, lines of inscription."""
    d = ImageDraw.Draw(im)
    w = x1 - x0
    d.rectangle((x0, y0 + w // 4, x1, y1), fill=C[face], outline=C[edge])
    d.pieslice((x0, y0, x1, y0 + w // 2), 180, 360, fill=C[face], outline=C[edge])
    d.line((x0 + 1, y0 + w // 4, x1 - 1, y0 + w // 4), fill=C[face])
    d.arc((x0, y0, x1, y0 + w // 2), 190, 250, fill=C[lit])
    d.line((x0, y0 + w // 4, x0, y1 - 6), fill=C[lit])
    cx = (x0 + x1) // 2
    if glyphs:
        r = max(4, w // 5)
        tri(d, cx, y0 + w // 4 + r + 2, r, True, lit)
        d.line((x0 + 5, y0 + w // 4 + 2 * r + 5, x1 - 5, y0 + w // 4 + 2 * r + 5), fill=C[edge])
        tri(d, cx, y0 + w // 4 + 3 * r + 8, r, False, edge)
        top = y0 + w // 4 + 4 * r + 12
    else:
        top = y0 + w // 4 + 6
    if lines:
        rr = random.Random(seed)
        for y in range(top, y1 - 4, 4):
            x = x0 + 5
            while x < x1 - 6:
                n = rr.randrange(2, 7)
                d.line((x, y, min(x + n, x1 - 6), y), fill=C[edge])
                x += n + 2


def stoat(im, x, y, c="C_INK", hat="C_EDGE_DARK", band="C_RING", eye="C_MARGIN", facing=1):
    """OSRIC HATTER: a stoat in a tall hat, standing, 15 x 30. Long body, short ears, a black-tipped tail."""
    d = ImageDraw.Draw(im)
    f = (lambda v: x + v) if facing > 0 else (lambda v: x + 14 - v)
    d.ellipse((f(3) if facing > 0 else f(11), y + 9, f(11) if facing > 0 else f(3), y + 16), fill=C[c])      # head
    d.polygon([(f(5), y + 15), (f(10), y + 15), (f(11), y + 27), (f(3), y + 27)], fill=C[c])              # body
    d.polygon([(f(10), y + 12), (f(14), y + 13), (f(10), y + 15)], fill=C[c])                             # snout
    px(im, f(9), y + 11, eye)
    px(im, f(14), y + 13, "C_EDGE_DARK")
    d.rectangle((min(f(4), f(10)), y + 1, max(f(4), f(10)), y + 8), fill=C[hat])                        # the hat
    d.rectangle((min(f(2), f(12)), y + 8, max(f(2), f(12)), y + 9), fill=C[hat])
    d.line((min(f(4), f(10)), y + 6, max(f(4), f(10)), y + 6), fill=C[band])
    d.line((f(3), y + 27, f(0), y + 29), fill=C[c])                                                       # the tail
    d.line((f(0), y + 29, f(-2), y + 29), fill=C["C_EDGE_DARK"])
    d.line((f(5), y + 28, f(5), y + 29), fill=C[c])
    d.line((f(9), y + 28, f(9), y + 29), fill=C[c])


def fir(im, cx, base, h, c="C_EDGE_DARK", edge=None):
    """The singing fir: tiers narrowing to a point."""
    d = ImageDraw.Draw(im)
    d.rectangle((cx - 1, base - 4, cx + 1, base), fill=C[c])
    tiers = max(3, h // 8)
    for k in range(tiers):
        yb = base - 3 - k * (h - 6) // tiers
        yt = yb - (h - 6) // tiers - 4
        hw = (tiers - k) * h // (tiers * 3) + 1
        d.polygon([(cx, yt), (cx + hw, yb), (cx - hw, yb)], fill=C[c])
        if edge:
            d.line((cx, yt, cx - hw, yb), fill=C[edge])
    return base - h                                          # the tip


def lark(im, x, y, c="C_INK", eye="C_EDGE_DARK", singing=True):
    """A LARK, 9 x 7, perched, beak up: crest, body, tail."""
    d = ImageDraw.Draw(im)
    d.ellipse((x + 1, y + 2, x + 7, y + 6), fill=C[c])
    d.ellipse((x + 4, y, x + 8, y + 4), fill=C[c])
    px(im, x + 5, y - 1, c)                                  # the crest
    px(im, x + 6, y + 1, eye)
    d.line((x + 8, y + 1, x + 9, y), fill=C[c])             # the beak, up
    d.line((x, y + 5, x - 2, y + 7), fill=C[c])              # the tail
    px(im, x + 4, y + 7, "C_EDGE_DARK")
    if singing:
        for k, (dx, dy) in enumerate(((11, -2), (14, -5), (12, -8))):
            px(im, x + dx, y + dy, "C_MARGIN" if k % 2 == 0 else "C_CHALK")
            px(im, x + dx, y + dy + 1, "C_MARGIN" if k % 2 == 0 else "C_CHALK")


def sun(im, cx, hy, r, fill="C_MARGIN", rays="C_RULE", n=7):
    d = ImageDraw.Draw(im)
    for k in range(n):
        a = math.pi * (k + 0.5) / n
        d.line((cx - (r + 3) * math.cos(a), hy - (r + 3) * math.sin(a),
                cx - (r + 9) * math.cos(a), hy - (r + 9) * math.sin(a)), fill=C[rays])
    d.pieslice((cx - r, hy - r, cx + r, hy + r), 180, 360, fill=C[fill])


def moon(im, cx, cy, r, c="C_CHALK", sky="C_SLATE"):
    d = ImageDraw.Draw(im)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=C[c])
    d.ellipse((cx - r + r // 2 + 1, cy - r - 1, cx + r + r // 2 + 1, cy + r - 1), fill=C[sky])


def hand(im, x, y, c="C_INK", line="C_EDGE_DARK", s=1, closed=False, flip=False):
    """An open hand, palm on, fingers up (about 30 x 42 at s=1); closed is a loose fist."""
    d = ImageDraw.Draw(im)
    X = (lambda v: x + v * s) if not flip else (lambda v: x + (30 - v) * s)
    Y = lambda v: y + v * s

    def box(a, b, cc, e, r):
        d.rounded_rectangle((min(X(a), X(cc)), Y(b), max(X(a), X(cc)), Y(e)), radius=r * s, fill=C[c])
    box(5, 20, 25, 40, 5)                                    # the palm
    if closed:
        for k, fx in enumerate((6, 11, 16, 21)):
            box(fx, 14, fx + 4, 24, 2)
            d.line((min(X(fx), X(fx + 4)), Y(23), max(X(fx), X(fx + 4)), Y(23)), fill=C[line])
        d.polygon([(X(5), Y(28)), (X(0), Y(22)), (X(2), Y(18)), (X(9), Y(26))], fill=C[c])
    else:
        for fx, top in ((6, 6), (11, 1), (16, 0), (21, 5)):
            box(fx, top, fx + 4, 24, 2)
            d.line((X(fx + 4), Y(top + 6), X(fx + 4), Y(22)), fill=C[line])
        d.polygon([(X(5), Y(30)), (X(-2), Y(18)), (X(1), Y(15)), (X(8), Y(24))], fill=C[c])
    d.arc((min(X(9), X(22)), Y(26), max(X(9), X(22)), Y(38)), 200, 340, fill=C[line])
    d.line((X(8), Y(32), X(14), Y(35)), fill=C[line])


def frame_plate(d, box, c):
    d.rectangle(box, outline=C[c])


def torn_edge(im, x, y0, y1, side, seed, board="C_SLATE", spine="C_EDGE_DARK", thread="C_CHALK_FAINT", depth=5):
    """The spine torn off: the board's edge ragged, the spine's last strip behind it, thread ends hanging out."""
    d = ImageDraw.Draw(im)
    r = random.Random(seed)
    off = 0
    for y in range(y0, y1 + 1):
        off = max(0, min(depth, off + r.choice((-1, 0, 0, 1))))
        if side < 0:      # torn on the left
            d.line((x, y, x + off, y), fill=C["C_COVER"])
            px(im, x + off + 1, y, spine)
        else:
            d.line((x - off, y, x, y), fill=C["C_COVER"])
            px(im, x - off - 1, y, spine)
    for y in range(y0 + 8, y1 - 4, 14):                  # the stitches the spine was sewn with
        n = r.randrange(3, 7)
        for k in range(n):
            px(im, x + (-k - 1 if side < 0 else k + 1) + depth // 2 * (1 if side < 0 else -1), y + (k // 3), thread)


def stitched_spine(im, x, y0, y1, a="C_MARGIN", b="C_RULE", spine="C_EDGE_DARK", w=6):
    """A spine sewn back on: two threads, the night's emerald and the dawn's gold, laced across it."""
    d = ImageDraw.Draw(im)
    d.rectangle((x, y0, x + w - 1, y1), fill=C[spine])
    for k, y in enumerate(range(y0 + 4, y1 - 3, 7)):
        d.line((x - 1, y, x + w, y + 3), fill=C[a])
        d.line((x - 1, y + 3, x + w, y), fill=C[b])


def title(im, book, cx, y=12, sub=True):
    t, s = gs.BOOKS[book]["title"], gs.BOOKS[book]["subtitle"]
    gs.glyphs(im, t, cx - g.width(t) // 2, y, False, C["C_CHALK"])
    if sub:
        gs.glyphs(im, s, cx - g.width(s, True) // 2, y + 15, True, C["C_CHALK_FAINT"])


def boards(im, x0, x1, y0=4, y1=152):
    d = ImageDraw.Draw(im)
    d.rectangle((x0 + 2, y0 + 1, x1 + 3, y1 + 2), fill=C["C_EDGE_DARK"])   # the pages beneath
    d.rectangle((x0, y0, x1, y1), fill=C["C_SLATE"])
    return d


def blank(w, h, fill):
    return Image.new("RGB", (w, h), C[fill])


# ==================================================================== THE HERMETIC LAYER, the night half
def h_cover_a():
    """A: the tablet at night. The front cover, its spine torn away on the left; on the plate the Emerald Tablet on its
    hill under a crescent, OSRIC HATTER beside it reading, the emerald (C_RING) breathing with the reader's pulse."""
    im = blank(240, 160, "C_COVER")
    d = boards(im, 46, 188)
    stars(im, (60, 40, 182, 120), 11, 70, ("C_EDGE", "C_HIGHLIGHT", "C_FAINT"))
    title(im, "hermetic", 119)
    d.rectangle((56, 8, 184, 148), outline=C["C_RULE"])
    d.rectangle((70, 44, 170, 141), outline=C["C_EDGE"])
    moon(im, 151, 56, 7)
    d.pieslice((60, 118, 180, 170), 180, 360, fill=C["C_EDGE_DARK"])         # the hill
    d.arc((60, 118, 180, 170), 200, 300, fill=C["C_RING"])
    tablet(im, 101, 58, 139, 130)
    stoat(im, 80, 104)
    torn_edge(im, 46, 4, 152, -1, 7)
    return im


def h_cover_b():
    """B: the hatter's sky. No plate: the whole board is the night, the tablet small and high like a lit window, and
    OSRIC HATTER large in the foreground, his hat's band the emerald, looking up at it. More story, less emblem."""
    im = blank(240, 160, "C_COVER")
    d = boards(im, 46, 188)
    bands(im, (47, 5, 188, 152), ["C_SLATE", "C_SLATE", "C_HIGHLIGHT", "C_EDGE"])
    stars(im, (50, 40, 186, 110), 19, 110, ("C_FAINT", "C_EDGE", "C_INK"))
    title(im, "hermetic", 119)
    d.rectangle((56, 8, 184, 148), outline=C["C_RULE"])
    tablet(im, 126, 50, 152, 92, lines=False)
    for k in range(5):                                                       # its light, falling
        d.line((128 + k * 5, 94, 112 + k * 9, 128), fill=C["C_RING"] if k % 2 else C["C_HIGHLIGHT"])
    d.rectangle((57, 128, 183, 147), fill=C["C_EDGE_DARK"])
    d.line((57, 128, 183, 128), fill=C["C_RING"])
    big = Image.new("RGB", (16, 31), C["C_SLATE"])
    stoat(big, 0, 0, c="C_FAINT", hat="C_EDGE_DARK", band="C_RING", eye="C_MARGIN")
    big = big.resize((32, 62), Image.NEAREST)
    mask = Image.eval(big.convert("L"), lambda v: 0)
    bp = big.load()
    for yy in range(big.height):
        for xx in range(big.width):
            if bp[xx, yy] != C["C_SLATE"]:
                im.putpixel((76 + xx, 86 + yy), bp[xx, yy])
    torn_edge(im, 46, 4, 152, -1, 7)
    return im


def h_icon():
    im = blank(24, 24, "C_NONE")
    d = ImageDraw.Draw(im)
    d.rectangle((6, 3, 19, 21), fill=C["C_SLATE"], outline=C["C_INK"])
    for y, o in zip(range(3, 22), (0, 1, 1, 0, 1, 2, 1, 0, 0, 1, 2, 1, 1, 0, 1, 0, 1, 1, 0)):
        d.line((4, y, 5 + o, y), fill=C["C_NONE"])
        px(im, 6 + o, y, "C_RING")
    px(im, 4, 8, "C_CHALK_FAINT"); px(im, 4, 15, "C_CHALK_FAINT")            # a thread end, two
    d.polygon([(13, 7), (17, 13), (9, 13)], outline=C["C_MARGIN"])
    d.polygon([(13, 19), (17, 14), (9, 14)], outline=C["C_RING"])
    return im


def h_frontis():
    """The one picture the engine shows on every entry today: the tablet on its hill, under the crescent, read."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    stars(im, (4, 3, 92, 60), 5, 40, ("C_FAINT", "C_EDGE", "C_INK"))
    moon(im, 74, 14, 6, sky="C_PAPER")
    d.pieslice((-10, 64, 106, 120), 180, 360, fill=C["C_EDGE_DARK"])
    d.arc((-10, 64, 106, 120), 205, 300, fill=C["C_RING"])
    tablet(im, 40, 16, 70, 76)
    stoat(im, 20, 50)
    return im


def h_warning():
    """warning -- This book was not printed here: a closed book on a stone, torn at its spine, threads loose, a candle."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    stars(im, (4, 3, 92, 40), 8, 22, ("C_FAINT", "C_EDGE", "C_INK"))
    d.rectangle((14, 66, 82, 80), fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])      # the stone
    d.polygon([(28, 34), (72, 30), (76, 62), (30, 66)], fill=C["C_EDGE_DARK"], outline=C["C_FAINT"])  # the book, lying
    d.polygon([(31, 36), (70, 32), (73, 60), (32, 63)], fill=C["C_HIGHLIGHT"])
    tri(d, 52, 44, 6, True, "C_RING")
    tri(d, 52, 54, 6, False, "C_RING")
    r = random.Random(4)
    for y in range(34, 67, 2):                                                       # its torn spine
        px(im, 27 - r.randrange(0, 3), y, "C_FAINT")
    for y in (40, 48, 56):
        d.line((27, y, 22 - r.randrange(0, 3), y + 3), fill=C["C_FAINT"])
    d.rectangle((80, 48, 84, 65), fill=C["C_INK"])                                    # the candle
    d.ellipse((80, 41, 84, 47), fill=C["C_MARGIN"])
    px(im, 82, 40, "C_INK")
    return im


def chalkboard(im, d, box, c="C_HIGHLIGHT", edge="C_FAINT"):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=C["C_EDGE_DARK"], outline=C[edge])
    d.rectangle((x0 + 2, y0 + 2, x1 - 2, y1 - 2), outline=C["C_EDGE"])
    d.line((x0 - 2, y1 + 2, x1 + 2, y1 + 2), fill=C[edge])                            # the ledge
    r = random.Random(x0 + y0)
    for y in range(y0 + 8, y0 + 30, 6):                                                # the board's own lines
        x = x0 + 6
        while x < x1 - 30:
            n = r.randrange(3, 9)
            d.line((x, y, x + n, y), fill=C[c])
            x += n + 3


def h_chalk():
    """chalk -- UNDER A SPELL, underlined twice: in the board's corner, small, bright, two strokes beneath."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    chalkboard(im, d, (6, 8, 89, 70))
    x, y = 58, 50
    for k in range(4):                                                                 # three short words, scrawled
        d.line((x + k * 7, y, x + k * 7 + 4, y - 1), fill=C["C_INK"])
    d.line((x - 1, y + 4, x + 26, y + 3), fill=C["C_MARGIN"])
    d.line((x, y + 7, x + 27, y + 6), fill=C["C_MARGIN"])
    d.rectangle((70, 72, 76, 74), fill=C["C_INK"])                                    # the chalk, put down
    return im


def h_emerald():
    """emerald -- The green tablet: large, read in full, its five inscriptions as five breathing lines."""
    im = blank(PW, PH, "C_PAPER")
    stars(im, (4, 3, 92, 84), 21, 18, ("C_EDGE", "C_HIGHLIGHT", "C_FAINT"))
    tablet(im, 26, 6, 70, 84, seed=9)
    return im


def h_hands():
    """hands -- One hand, folded into many: the great hand below, and from each fingertip, on an emerald thread, a small
    hand of its own."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    hand(im, 33, 44, c="C_FAINT", line="C_EDGE_DARK", s=1)
    for k, (fx, top) in enumerate(((6, 6), (11, 1), (16, 0), (21, 5))):
        sx, sy = 6 + k * 22, 6 + abs(k - 1.5) * 4
        d.line((33 + fx + 2, 44 + top, sx + 8, sy + 22), fill=C["C_RING"])
        hand(im, sx, sy, c="C_INK", line="C_EDGE_DARK", s=0.55)
    return im


def h_palm():
    """palm -- The palm every finger rises from: the palm lit in emerald, the fingers ink rising out of it."""
    im = blank(PW, PH, "C_PAPER")
    hand(im, 20, 8, c="C_INK", line="C_EDGE_DARK", s=1.8)
    d = ImageDraw.Draw(im)
    d.ellipse((34, 50, 62, 72), outline=C["C_RING"])
    d.ellipse((38, 54, 58, 68), outline=C["C_MARGIN"])
    return im


# ==================================================================== THE EUDAIMON LAYER, the dawn half
def e_dawn(im, box, hy, firx, seed=2, sun_x=None, sapphire=False):
    """The morning on a plate: the sky's bands to the horizon, the sun half risen, the fir and the lark at its top."""
    x0, y0, x1, y1 = box
    sky = ["C_SLATE", "C_CHALK_FAINT", "C_FAINT", "C_RULE"] if sapphire else \
          ["C_EDGE", "C_HIGHLIGHT", "C_SLATE", "C_FAINT", "C_RULE"]
    bands(im, (x0, y0, x1, hy), sky)
    d = ImageDraw.Draw(im)
    sun(im, sun_x if sun_x is not None else (x0 + x1) // 2 - 8, hy, 12)
    d.rectangle((x0, hy, x1 - 1, y1 - 1), fill=C["C_EDGE_DARK"])
    d.line((x0, hy, x1 - 1, hy), fill=C["C_RING"])
    rr = random.Random(seed)
    for k in range(6):                                                              # the light on the ground
        y = hy + 3 + k * 3
        if y < y1 - 1:
            xa = (x0 + x1) // 2 - 8 - (14 - k * 2)
            d.line((xa, y, xa + (28 - k * 4), y), fill=C["C_EDGE"] if k % 2 else C["C_HIGHLIGHT"])
    tip = fir(im, firx, hy + 1, min(48, hy - y0 - 6))
    lark(im, firx - 4, tip - 7)
    return tip


def e_cover(sapphire=False):
    """The back cover, its spine torn away on the right; on an arched plate the morning: the sun half risen, the
    singing fir, the LARK at its top singing, the tablet's green as the horizon."""
    im = blank(240, 160, "C_COVER")
    d = boards(im, 50, 190)
    if sapphire:
        stars(im, (54, 40, 186, 64), 4, 18, ("C_CHALK_FAINT", "C_HIGHLIGHT", "C_CHALK"))
    title(im, "eudaimon", 118)
    d.rectangle((54, 8, 182, 148), outline=C["C_RULE"])
    plate = Image.new("RGB", (80, 92), C["C_SLATE"])
    e_dawn(plate, (0, 0, 80, 92), 64, 58, sapphire=sapphire, sun_x=30)
    m = Image.new("L", plate.size, 0)
    md = ImageDraw.Draw(m)
    md.rectangle((0, 20, 79, 91), fill=255)
    md.pieslice((0, 0, 79, 40), 180, 360, fill=255)
    im.paste(plate, (78, 46), m)
    d.rectangle((78, 66, 157, 137), outline=C["C_RULE"])
    d.arc((78, 46, 157, 86), 180, 360, fill=C["C_RULE"])
    tri(d, 117, 128, 5, False, "C_FAINT")                                           # below, faint: the other half
    torn_edge(im, 190, 4, 152, 1, 13)
    return im


def e_cover_a():
    return e_cover(False)


def e_cover_b():
    return e_cover(True)


def e_icon():
    im = blank(24, 24, "C_NONE")
    d = ImageDraw.Draw(im)
    d.rectangle((4, 3, 17, 21), fill=C["C_SLATE"], outline=C["C_INK"])
    for y, o in zip(range(3, 22), (0, 1, 0, 0, 1, 2, 1, 1, 0, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0)):
        d.line((18 - o, y, 19, y), fill=C["C_NONE"])
        px(im, 17 - o, y, "C_RULE")
    px(im, 19, 9, "C_CHALK_FAINT"); px(im, 19, 16, "C_CHALK_FAINT")
    sun(im, 10, 14, 4, n=0)
    d.line((5, 14, 15, 14), fill=C["C_RING"])
    return im


def e_frontis(sapphire=False):
    im = blank(PW, PH, "C_PAPER")
    e_dawn(im, (0, 0, PW, PH), 64, 66, sapphire=sapphire)
    return im


def e_blessing():
    """blessing -- This book was read at first light: the book lying open at the fir's foot, the lark above it."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    bands(im, (0, 0, PW, 60), ["C_PAPER", "C_HIGHLIGHT", "C_FAINT", "C_RULE"])
    sun(im, 34, 60, 10)
    d.rectangle((0, 60, PW - 1, PH - 1), fill=C["C_EDGE_DARK"])
    d.line((0, 60, PW - 1, 60), fill=C["C_RING"])
    tip = fir(im, 72, 61, 46)
    lark(im, 68, tip - 7)
    d.polygon([(22, 70), (40, 66), (58, 70), (58, 80), (40, 77), (22, 80)], fill=C["C_INK"])   # the book, open
    d.line((40, 66, 40, 77), fill=C["C_FAINT"])
    for y in (71, 74):
        d.line((26, y, 37, y - 2), fill=C["C_FAINT"]); d.line((43, y - 2, 54, y), fill=C["C_FAINT"])
    return im


def e_chalkfaint():
    """chalkfaint -- IN GOOD SPIRITS, in the other corner: the same board, the faint words in its far corner."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    chalkboard(im, d, (6, 8, 89, 70))
    x, y = 11, 60
    for k in range(4):
        d.line((x + k * 7, y, x + k * 7 + 4, y - 1), fill=C["C_EDGE"])
    px(im, x + 30, y - 2, "C_RULE")                                                   # one mote of gold, a smile
    return im


def e_emeraldback():
    """emeraldback -- The green tablet, from underneath: its plain back, roots under it, the light coming up."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 66, PW - 1, PH - 1), fill=C["C_EDGE_DARK"])
    for k, x in enumerate(range(28, 70, 7)):                                          # its roots
        d.line((x, 66, x + (k - 3) * 3, 84), fill=C["C_EDGE"])
    tablet(im, 28, 8, 68, 70, face="C_HIGHLIGHT", edge="C_RING", lit="C_RULE", lines=False, glyphs=False)
    for y in range(26, 66, 5):
        d.line((34, y, 62, y), fill=C["C_EDGE"])
    d.line((0, 66, PW - 1, 66), fill=C["C_RING"])
    return im


def e_palmup():
    """palmup -- The palm, open: held up, the warmth in it gold."""
    im = blank(PW, PH, "C_PAPER")
    hand(im, 20, 8, c="C_INK", line="C_EDGE", s=1.8)
    d = ImageDraw.Draw(im)
    d.ellipse((36, 52, 60, 70), fill=C["C_MARGIN"])
    d.ellipse((40, 55, 56, 67), fill=C["C_RULE"])
    return im


def e_fingers():
    """fingers -- Every finger, rising from the palm: the hand drawn from below, five lines of gold rising out of it."""
    im = blank(PW, PH, "C_PAPER")
    hand(im, 31, 38, c="C_FAINT", line="C_EDGE", s=1.2)
    d = ImageDraw.Draw(im)
    for fx, top in ((6, 6), (11, 1), (16, 0), (21, 5)):
        x = 31 + int((fx + 2) * 1.2)
        d.line((x, 38 + int(top * 1.2) - 4, x, 4 + top), fill=C["C_RULE"])
        px(im, x, 3 + top, "C_MARGIN")
    return im


# ==================================================================== THE UNITY BOOK, mended
def u_horizon(im, box, hy):
    """One horizon, night on the left and dawn on the right: stars and the emerald triangles; the gold sun."""
    x0, y0, x1, y1 = box
    mid = (x0 + x1) // 2
    d = ImageDraw.Draw(im)
    bands(im, (x0, y0, mid, hy), ["C_EDGE_DARK", "C_EDGE", "C_HIGHLIGHT"])
    bands(im, (mid, y0, x1, hy), ["C_HIGHLIGHT", "C_FAINT", "C_RULE"])
    stars(im, (x0 + 2, y0 + 2, mid - 2, hy - 16), 31, (mid - x0) * (hy - y0) // 60, ("C_FAINT", "C_EDGE", "C_INK"))
    tri(d, (x0 + mid) // 2, hy - 14, 7, True, "C_MARGIN")
    sun(im, (mid + x1) // 2, hy, 10, fill="C_RULE", rays="C_CHALK_FAINT")
    d.rectangle((x0, hy, x1 - 1, y1 - 1), fill=C["C_EDGE_DARK"])
    tri(d, (x0 + mid) // 2, hy + 12, 7, False, "C_RING")
    d.line((x0, hy, x1 - 1, hy), fill=C["C_CHALK"])
    d.line((mid, y0, mid, y1 - 1), fill=C["C_RING"])
    d.line((mid + 1, y0, mid + 1, y1 - 1), fill=C["C_RULE"])


def u_cover_a():
    """A: the closed book, front cover, its spine sewn back on with both threads; on a round plate one horizon, night
    left and dawn right. Closest to the placeholder, made real."""
    im = blank(240, 160, "C_COVER")
    d = boards(im, 48, 188)
    title(im, "unity", 121)
    d.rectangle((60, 8, 184, 148), outline=C["C_RULE"])
    d.rectangle((61, 9, 183, 147), outline=C["C_EDGE"])
    plate = Image.new("RGB", (88, 88), C["C_SLATE"])
    u_horizon(plate, (0, 0, 88, 88), 50)
    m = Image.new("L", plate.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, 87, 87), fill=255)
    im.paste(plate, (78, 50), m)
    d.ellipse((77, 49, 166, 138), outline=C["C_CHALK_FAINT"])
    stitched_spine(im, 48, 4, 152)
    return im


def u_cover_b():
    """B: both covers, the book opened flat: the night's front board and the dawn's back board side by side, the spine
    between them sewn with both threads, one title across both, each board its own emblem."""
    im = blank(240, 160, "C_COVER")
    d = ImageDraw.Draw(im)
    d.rectangle((8, 5, 191, 154), fill=C["C_EDGE_DARK"])
    d.rectangle((6, 4, 96, 152), fill=C["C_SLATE"])
    d.rectangle((103, 4, 188, 152), fill=C["C_SLATE"])
    bands(im, (6, 40, 97, 150), ["C_SLATE", "C_EDGE"])
    bands(im, (103, 40, 189, 150), ["C_SLATE", "C_HIGHLIGHT"])
    stars(im, (10, 44, 92, 100), 3, 30, ("C_EDGE", "C_HIGHLIGHT", "C_FAINT"))
    d.rectangle((12, 42, 90, 146), outline=C["C_RING"])
    d.rectangle((109, 42, 183, 146), outline=C["C_RULE"])
    tablet(im, 35, 58, 67, 128, lines=True)
    sun(im, 146, 104, 14, fill="C_RULE", rays="C_CHALK_FAINT")
    d.line((115, 104, 177, 104), fill=C["C_RING"])
    tip = fir(im, 164, 105, 36)
    lark(im, 160, tip - 7)
    stitched_spine(im, 97, 4, 152)
    d.rectangle((30, 9, 166, 37), fill=C["C_EDGE_DARK"], outline=C["C_CHALK_FAINT"])   # a label, pasted across the mend
    title(im, "unity", 98, y=11)
    return im


def u_cover_c():
    """C: the balance. The closed book, spine sewn back on; on the plate a beam held level on the crease, the night's
    tablet in one pan and the dawn's sun in the other, neither heavier."""
    im = blank(240, 160, "C_COVER")
    d = boards(im, 48, 188)
    title(im, "unity", 121)
    d.rectangle((60, 8, 184, 148), outline=C["C_RULE"])
    cx = 122
    d.rectangle((cx - 1, 50, cx + 1, 134), fill=C["C_CHALK_FAINT"])                 # the post
    d.polygon([(cx - 14, 140), (cx + 14, 140), (cx + 6, 132), (cx - 6, 132)], fill=C["C_CHALK_FAINT"])
    d.line((cx - 44, 58, cx + 44, 58), fill=C["C_CHALK"])                           # the beam, level
    d.ellipse((cx - 3, 54, cx + 3, 60), fill=C["C_CHALK"])
    for side, pan in ((-1, "C_RING"), (1, "C_RULE")):
        px0 = cx + side * 40
        d.line((px0, 58, px0 - 12, 104), fill=C["C_FAINT"]); d.line((px0, 58, px0 + 12, 104), fill=C["C_FAINT"])
        d.chord((px0 - 16, 98, px0 + 16, 114), 0, 180, fill=C["C_EDGE_DARK"], outline=C[pan])
    tablet(im, cx - 49, 74, cx - 31, 103, lines=False)
    sun(im, cx + 40, 103, 8, fill="C_RULE", rays="C_CHALK_FAINT", n=5)
    stars(im, (66, 20, cx - 8, 52), 8, 14, ("C_FAINT", "C_EDGE", "C_INK"))
    stitched_spine(im, 48, 4, 152)
    return im


def u_icon():
    im = blank(24, 24, "C_NONE")
    d = ImageDraw.Draw(im)
    d.rectangle((5, 3, 19, 21), fill=C["C_SLATE"], outline=C["C_INK"])
    d.rectangle((5, 3, 8, 21), fill=C["C_EDGE_DARK"])
    for y in range(4, 21, 4):
        d.line((4, y, 9, y + 2), fill=C["C_MARGIN"]); d.line((4, y + 2, 9, y), fill=C["C_RULE"])
    d.ellipse((10, 7, 18, 15), outline=C["C_CHALK_FAINT"])
    d.line((10, 11, 18, 11), fill=C["C_CHALK"])
    d.line((14, 7, 14, 15), fill=C["C_RING"])
    px(im, 12, 9, "C_MARGIN"); px(im, 16, 10, "C_RULE")
    return im


def u_frontis():
    im = blank(PW, PH, "C_PAPER")
    u_horizon(im, (0, 0, PW, PH), 58)
    return im


def u_attestation():
    """attestation -- One book, both covers: a book standing, the front cover's emerald and the back's gold both
    showing, its spine sewn."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    d.polygon([(26, 14), (50, 20), (50, 80), (26, 74)], fill=C["C_EDGE"], outline=C["C_RING"])     # front, turned
    d.polygon([(50, 20), (74, 14), (74, 74), (50, 80)], fill=C["C_HIGHLIGHT"], outline=C["C_RULE"])  # back, turned
    tri(d, 38, 40, 5, True, "C_MARGIN")
    sun(im, 62, 50, 6, fill="C_RULE", rays="C_CHALK_FAINT", n=5)
    for y in range(24, 78, 6):
        d.line((48, y, 52, y + 2), fill=C["C_MARGIN"]); d.line((48, y + 2, 52, y), fill=C["C_RULE"])
    d.line((10, 84, 86, 84), fill=C["C_FAINT"])
    return im


def u_chalkboth():
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    chalkboard(im, d, (6, 8, 89, 70))
    for k in range(4):
        d.line((11 + k * 7, 60, 15 + k * 7, 59), fill=C["C_EDGE"])
        d.line((58 + k * 7, 50, 62 + k * 7, 49), fill=C["C_INK"])
    d.line((57, 54, 84, 53), fill=C["C_MARGIN"]); d.line((58, 57, 85, 56), fill=C["C_MARGIN"])
    px(im, 41, 58, "C_RULE")
    return im


def u_emeraldwhole():
    """emeraldwhole -- The green tablet, both faces: the inscribed face and the plain back, side by side on one ground."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 74, PW - 1, PH - 1), fill=C["C_EDGE_DARK"])
    tablet(im, 10, 10, 44, 76, seed=5)
    tablet(im, 52, 10, 86, 76, face="C_HIGHLIGHT", edge="C_RING", lit="C_RULE", lines=False, glyphs=False)
    for y in range(26, 72, 5):
        d.line((57, y, 81, y), fill=C["C_EDGE"])
    d.line((0, 74, PW - 1, 74), fill=C["C_RING"])
    d.line((47, 14, 49, 14), fill=C["C_FAINT"]); d.line((47, 16, 49, 16), fill=C["C_FAINT"])
    return im


def u_wholehand():
    im = blank(PW, PH, "C_PAPER")
    hand(im, 20, 8, c="C_INK", line="C_EDGE_DARK", s=1.8)
    d = ImageDraw.Draw(im)
    d.ellipse((36, 52, 60, 70), outline=C["C_RING"])
    d.ellipse((40, 55, 56, 67), fill=C["C_RULE"])
    for fx, top in ((6, 6), (11, 1), (16, 0), (21, 5)):
        px(im, 20 + int((fx + 2) * 1.8), 8 + int(top * 1.8) + 2, "C_MARGIN")
    return im


def u_handturning():
    """handturning -- A hand, closing and opening: two frames (the reader cycles up to three), fist and open hand."""
    out = []
    for closed in (True, False):
        im = blank(PW, PH, "C_PAPER")
        hand(im, 20, 8, c="C_INK", line="C_EDGE_DARK", s=1.8, closed=closed)
        d = ImageDraw.Draw(im)
        d.arc((8, 4, 88, 84), 200, 340, fill=C["C_RING" if closed else "C_RULE"])
        out.append(im)
    return out


# ==================================================================== batch 2 (T-519): its shared shapes
def flask(im, cx, base, r, glass="C_FAINT", fill=None, level=1.0, shine="C_INK"):
    """A round-bottomed flask, the Work's vessel: a bulb of radius R on BASE, a neck, filled to LEVEL with FILL."""
    d = ImageDraw.Draw(im)
    top = base - 2 * r
    if fill:
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).ellipse((cx - r + 1, top + 1, cx + r - 1, base - 1), fill=255)
        cut = int(base - (2 * r - 2) * level)
        ImageDraw.Draw(m).rectangle((0, 0, im.width, cut), fill=0)
        im.paste(Image.new("RGB", im.size, C[fill]), (0, 0), m)
    d.ellipse((cx - r, top, cx + r, base), outline=C[glass])
    d.rectangle((cx - r // 3, top - r, cx + r // 3, top + 1), fill=C["C_PAPER"])
    d.line((cx - r // 3, top - r, cx - r // 3, top + 1), fill=C[glass])
    d.line((cx + r // 3, top - r, cx + r // 3, top + 1), fill=C[glass])
    d.line((cx - r // 3 - 2, top - r, cx + r // 3 + 2, top - r), fill=C[glass])
    d.arc((cx - r + 3, top + 3, cx + r - 3, base - 3), 200, 245, fill=C[shine])
    return top


def standing_stone(im, x0, y0, x1, y1, face, edge, lit):
    """A plain stone, rounded at the head, nothing on it."""
    d = ImageDraw.Draw(im)
    w = x1 - x0
    d.rounded_rectangle((x0, y0, x1, y1), radius=w // 3, fill=C[face], outline=C[edge])
    d.arc((x0 + 1, y0 + 1, x0 + w // 1.5, y0 + w // 1.5), 185, 260, fill=C[lit])
    d.line((x0 + 1, y0 + w // 3, x0 + 1, y1 - 4), fill=C[lit])


def grass2(im, y, seed, c="C_EDGE", n=26):
    r = random.Random(seed)
    for _ in range(n):
        x = r.randrange(2, PW - 2)
        h = r.randrange(2, 5)
        ImageDraw.Draw(im).line((x, y, x + r.choice((-1, 0, 1)), y - h), fill=C[c])


# ================================================================================ THE HERMETIC LAYER, the night half
def h_mirrors():
    """mirrors -- One light, many glasses: a single light on the ground, an arc of six mirrors round it, each showing a
    light of its own from its own angle, sure it is the only one."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    stars(im, (4, 2, 92, 20), 41, 14, ("C_FAINT", "C_EDGE", "C_INK"))
    cx, cy = 48, 70
    for k in range(6):
        a = math.pi * (0.12 + 0.76 * k / 5)
        mx, my = cx - 36 * math.cos(a), cy - 44 * math.sin(a) + 6
        d.line((cx, cy, mx, my + 8), fill=C["C_EDGE"])
        d.rounded_rectangle((mx - 5, my - 2, mx + 5, my + 16), radius=3, fill=C["C_EDGE_DARK"], outline=C["C_FAINT"])
        off = int(3 * math.cos(a))                                   # each glass sees the light from its own side
        px(im, mx + off, my + 8, "C_MARGIN"); px(im, mx + off, my + 7, "C_RING"); px(im, mx + off, my + 9, "C_RING")
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=C["C_RING"])
    d.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=C["C_MARGIN"])
    px(im, cx, cy, "C_INK")
    d.line((10, 80, 86, 80), fill=C["C_EDGE"])
    return im


def h_nigredo():
    """nigredo -- First, black. Then, washed white: two flasks on the stone, the first full of black with ash in it,
    the second rinsed, a white shine left where nothing would burn."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    stars(im, (4, 2, 92, 30), 12, 16, ("C_FAINT", "C_EDGE", "C_INK"))
    d.rectangle((6, 70, 89, 76), fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])
    flask(im, 28, 69, 15, fill="C_SHADOW", level=0.85)
    r = random.Random(5)
    for _ in range(9):
        px(im, 28 + r.randrange(-9, 10), 69 - r.randrange(2, 12), "C_EDGE")
    flask(im, 68, 69, 15, fill="C_HIGHLIGHT", level=0.45)
    d.ellipse((63, 52, 73, 62), fill=C["C_INK"])                    # what would not burn
    d.ellipse((65, 54, 70, 58), fill=C["C_CHALK"])
    for dx in (-8, 8):
        px(im, 68 + dx, 50, "C_FAINT")
    tri(d, 48, 60, 4, False, "C_RING")                               # so below: the Work moves on
    return im


def h_rubedo():
    """rubedo -- Dawn in the glass. Then red, and whole: the night half has no gold and no red, so dawn is the emerald
    lit, rising in the first flask, and red its warmest role, the purple, filling the second round the stone."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    stars(im, (4, 2, 92, 30), 13, 14, ("C_FAINT", "C_EDGE", "C_INK"))
    d.rectangle((6, 70, 89, 76), fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])
    flask(im, 28, 69, 15, fill="C_EDGE_DARK", level=0.9)
    m = Image.new("RGB", (40, 40), C["C_EDGE_DARK"])                 # dawn inside the glass
    sun(m, 20, 26, 6, fill="C_MARGIN", rays="C_RING", n=5)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse((15, 41, 41, 67), fill=255)
    big = Image.new("RGB", im.size, C["C_PAPER"]); big.paste(m, (8, 33))
    im.paste(big, (0, 0), mask)
    flask(im, 68, 69, 15, fill="C_RULE", level=0.92)
    d.ellipse((62, 50, 74, 62), fill=C["C_SHADOW"], outline=C["C_INK"])          # the stone, carrying all of it
    px(im, 66, 54, "C_INK"); px(im, 70, 57, "C_MARGIN"); px(im, 68, 59, "C_RING")
    for k in range(5):                                                         # it turns what it touches
        a = math.pi * (0.15 + 0.7 * k / 4)
        px(im, 68 - 22 * math.cos(a), 56 - 20 * math.sin(a), "C_RULE")
    return im


def h_folds():
    """folds -- One sheet, folded: a single sheet stood up in pleats on the stone at night, its first panel a shimmer,
    every crease in emerald, no fold making it less a sheet."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    stars(im, (4, 2, 92, 22), 17, 14, ("C_FAINT", "C_EDGE", "C_INK"))
    moon(im, 80, 12, 5, sky="C_PAPER")
    x1 = sheet_pleat(im, 12, 30, 6, 11, 38, lean=7)
    r = random.Random(2)                                                       # the first fold: a shimmer, undivided
    for _ in range(26):
        px(im, 12 + r.randrange(1, 11), 30 + r.randrange(0, 38), "C_HIGHLIGHT" if r.random() < .5 else "C_FAINT")
    d.line((8, 76, 88, 76), fill=C["C_EDGE"])
    d.line((12, 68, x1, 75), fill=C["C_EDGE_DARK"])
    return im


def h_blank():
    """blank -- A stone with nothing on it: a plain standing stone in the night grass, under the crescent, read by
    nobody."""
    im = blank(PW, PH, "C_PAPER")
    stars(im, (4, 2, 92, 40), 23, 22, ("C_FAINT", "C_EDGE", "C_INK"))
    moon(im, 20, 14, 6, sky="C_PAPER")
    ground(im, 72, line="C_EDGE")
    grass2(im, 72, 4)
    standing_stone(im, 34, 18, 62, 74, "C_EDGE", "C_FAINT", "C_HIGHLIGHT")
    px(im, 48, 40, "C_RING")                                                   # once, in the thinnest hour
    return im


# ================================================================================ THE EUDAIMON LAYER, the dawn half
def e_windows():
    """windows -- One light, many windows: a house at first light, one lamp inside showing through every window, each
    window sure the light shines in for it; its light falls out on the ground. The mirror's house turned outward."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    bands(im, (0, 0, PW, 64), ["C_SLATE", "C_CHALK_FAINT", "C_FAINT", "C_RULE"])
    ground(im, 64, line="C_RING")
    d.polygon([(18, 34), (48, 12), (78, 34)], fill=C["C_EDGE_DARK"])
    d.rectangle((22, 34, 74, 66), fill=C["C_EDGE_DARK"])
    for row, y in enumerate((38, 52)):
        for col, x in enumerate((27, 43, 59)):
            d.rectangle((x, y, x + 9, y + 9), fill=C["C_RULE"])
            d.line((x + 5, y, x + 5, y + 9), fill=C["C_EDGE_DARK"]); d.line((x, y + 5, x + 9, y + 5), fill=C["C_EDGE_DARK"])
            ox = (1 - col) * 2                                                  # the one lamp, from each window's side
            d.ellipse((x + 3 + ox, y + 2, x + 6 + ox, y + 5), fill=C["C_MARGIN"])
    d.ellipse((45, 22, 50, 27), fill=C["C_RULE"])                              # the attic: the lamp itself
    px(im, 47, 24, "C_INK")
    for k, x in enumerate((27, 43, 59)):                                       # its light out on the ground
        d.polygon([(x, 66), (x + 9, 66), (x + 12 + (k - 1) * 4, 86), (x - 3 + (k - 1) * 4, 86)], fill=C["C_HIGHLIGHT"])
    return im


def e_rubedo():
    """rubedo -- Red, and whole. Then dawn, back in the glass: read from this side the Work starts at the end. The first
    flask full and warm round the stone; the second with the dawn going back down into the glass."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    bands(im, (0, 0, PW, 30), ["C_SLATE", "C_PAPER"])
    d.rectangle((6, 70, 89, 76), fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])
    flask(im, 28, 69, 15, fill="C_RULE", level=0.92)
    d.ellipse((22, 50, 34, 62), fill=C["C_MARGIN"], outline=C["C_INK"])
    px(im, 26, 54, "C_INK"); px(im, 30, 57, "C_RING")
    flask(im, 68, 69, 15, fill="C_EDGE_DARK", level=0.9)
    m = Image.new("RGB", im.size, C["C_EDGE_DARK"])
    sun(m, 68, 62, 6, fill="C_MARGIN", rays="C_RULE", n=5)
    ImageDraw.Draw(m).line((58, 62, 78, 62), fill=C["C_RING"])
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse((55, 41, 81, 67), fill=255)
    im.paste(m, (0, 0), mask)
    tri(d, 48, 58, 4, True, "C_RING")                                          # as below, so above
    return im


def e_nigredo():
    """nigredo -- Washed white. Then a kind dark: the first flask's white shine given back to its ash; the second a
    soft dark at rest, one star in it, the night before a morning."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    bands(im, (0, 0, PW, 30), ["C_SLATE", "C_PAPER"])
    d.rectangle((6, 70, 89, 76), fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])
    flask(im, 28, 69, 15, fill="C_HIGHLIGHT", level=0.5)
    d.ellipse((23, 52, 33, 62), fill=C["C_INK"])
    r = random.Random(8)
    for _ in range(7):                                                         # the shine settling into its ash
        px(im, 28 + r.randrange(-8, 9), 66 - r.randrange(0, 5), "C_FAINT")
    flask(im, 68, 69, 15, fill="C_SLATE", level=0.88)
    d.ellipse((60, 46, 76, 62), fill=C["C_SLATE"])
    px(im, 70, 52, "C_CHALK"); px(im, 69, 52, "C_CHALK_FAINT"); px(im, 71, 52, "C_CHALK_FAINT")
    d.arc((60, 54, 76, 66), 200, 340, fill=C["C_CHALK_FAINT"])                 # a kind dark: it smiles
    return im


def e_opening():
    """opening -- One sheet, opening: the same pleated sheet at first light, its pleats easing flat, each face the
    sheet all along; the sun at its left edge, the creases green."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    bands(im, (0, 0, PW, 76), ["C_SLATE", "C_CHALK_FAINT", "C_FAINT", "C_RULE"])
    sun(im, 16, 76, 9)
    ground(im, 76, line="C_RING")
    x1 = sheet_pleat(im, 26, 32, 6, 10, 38, a="C_INK", b="C_MARGIN", crease_c="C_RING", lean=6, opening=0.6)
    d.line((26, 70, x1, 74), fill=C["C_EDGE"])
    for k in range(4):                                                         # the light on its first face
        px(im, 28 + k * 2, 38 + k * 6, "C_RULE")
    return im


def e_blankback():
    """blankback -- The back of the stone: the same stone from behind, the sun coming up past it, and on its back, just
    begun, a few green lines nobody has turned it over to read."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    bands(im, (0, 0, PW, 72), ["C_SLATE", "C_CHALK_FAINT", "C_FAINT", "C_RULE"])
    sun(im, 72, 72, 11)
    ground(im, 72, line="C_RING")
    grass2(im, 72, 6, c="C_HIGHLIGHT")
    standing_stone(im, 34, 18, 62, 74, "C_EDGE", "C_RULE", "C_MARGIN")
    for k, y in enumerate((36, 41, 46)):                                       # being written, by you
        d.line((40, y, 40 + (14, 10, 5)[k], y), fill=C["C_RING"])
    return im


# ================================================================================ THE UNITY BOOK, mended
def u_glass():
    """glass -- One light, a house of glass: one lamp at the centre; the panes on the night side show it back as
    mirrors, the panes on the dawn side let it through as windows. One house, every pane both."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    bands(im, (0, 0, 48, 64), ["C_EDGE_DARK", "C_EDGE"])
    bands(im, (48, 0, PW, 64), ["C_EDGE", "C_FAINT"])
    stars(im, (2, 2, 44, 20), 51, 9, ("C_FAINT", "C_EDGE", "C_INK"))
    ground(im, 66, line="C_CHALK")
    d.polygon([(16, 30), (48, 10), (80, 30)], outline=C["C_CHALK_FAINT"], fill=C["C_EDGE_DARK"])
    d.rectangle((20, 30, 76, 66), outline=C["C_CHALK_FAINT"], fill=C["C_EDGE_DARK"])
    for y in (34, 50):
        for x in (24, 36, 54, 66):
            night = x < 48
            d.rectangle((x, y, x + 8, y + 12), fill=C["C_SHADOW" if night else "C_RULE"],
                        outline=C["C_RING" if night else "C_MARGIN"])
            if night:                                                          # a glass: the light shown back
                px(im, x + 4 + (48 - x) // 12, y + 6, "C_MARGIN")
            else:                                                              # a window: the light let through
                d.line((x + 2, y + 2, x + 6, y + 10), fill=C["C_INK"])
    d.ellipse((45, 18, 51, 24), fill=C["C_INK"])                               # the one light
    px(im, 48, 21, "C_RULE")
    d.line((48, 30, 48, 66), fill=C["C_RING"]); d.line((49, 30, 49, 66), fill=C["C_RULE"])
    return im


def u_stone():
    """stone -- Black, white, dawn, red: one circle. The Work as a wheel of four flasks round the stone, black, white,
    dawn and the warm one, read either way round (an arrow each way)."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    cx, cy = 48, 44
    d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), outline=C["C_EDGE"])
    d.arc((cx - 38, cy - 38, cx + 38, cy + 38), 200, 250, fill=C["C_RING"])           # the night half's way round
    d.arc((cx - 38, cy - 38, cx + 38, cy + 38), 20, 70, fill=C["C_RULE"])             # the dawn half's
    px(im, cx - 37, cy - 6, "C_MARGIN"); px(im, cx + 37, cy + 6, "C_RULE")
    for k, (fill, lvl) in enumerate((("C_SHADOW", .85), ("C_INK", .5), ("C_EDGE_DARK", .9), ("C_RULE", .92))):
        a = -math.pi / 2 + k * math.pi / 2
        fx, fy = cx + int(30 * math.cos(a)), cy + int(30 * math.sin(a))
        flask(im, fx, fy + 8, 7, fill=fill, level=lvl, glass="C_FAINT")
        if k == 2:
            d.pieslice((fx - 4, fy + 2, fx + 4, fy + 10), 180, 360, fill=C["C_RULE"])
    d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=C["C_SHADOW"], outline=C["C_CHALK"])
    px(im, cx - 3, cy - 3, "C_INK"); px(im, cx + 3, cy, "C_RULE"); px(im, cx, cy + 3, "C_MARGIN")
    return im


def u_sheet():
    """sheet -- One sheet, folded and open: the night's pleats on the left, the dawn's flat open face on the right, one
    sheet, the crease between them sewn with both threads."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    stars(im, (2, 2, 46, 24), 61, 9, ("C_FAINT", "C_EDGE", "C_INK"))
    bands(im, (50, 0, PW, 26), ["C_PAPER", "C_HIGHLIGHT", "C_FAINT"])
    x1 = sheet_pleat(im, 8, 30, 4, 9, 38, a="C_INK", b="C_FAINT", crease_c="C_RING", lean=6)
    d.polygon([(x1, 30), (88, 26), (88, 64), (x1, 68)], fill=C["C_INK"])               # opened flat
    for k in range(4):
        d.line((x1 + 4, 38 + k * 7, 84, 35 + k * 7), fill=C["C_FAINT"])
    for y in range(32, 66, 6):                                                          # the crease, sewn
        d.line((x1 - 1, y, x1 + 1, y + 3), fill=C["C_MARGIN"]); d.line((x1 - 1, y + 3, x1 + 1, y), fill=C["C_RULE"])
    d.line((6, 76, 90, 76), fill=C["C_EDGE"])
    return im


def u_horizon_pic():
    """horizon -- Night on one side, dawn on the other: the world's curve, stars and the emerald on the left, the sun on
    the right, and one small walker standing on the crest where the two meet."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    bands(im, (0, 0, 48, 70), ["C_EDGE_DARK", "C_EDGE", "C_HIGHLIGHT"])
    bands(im, (48, 0, PW, 70), ["C_HIGHLIGHT", "C_FAINT", "C_RULE"])
    stars(im, (2, 2, 44, 44), 71, 26, ("C_FAINT", "C_EDGE", "C_INK"))
    tri(d, 18, 22, 5, True, "C_MARGIN")
    sun(im, 80, 62, 9, fill="C_RULE", rays="C_CHALK_FAINT", n=6)
    d.pieslice((-40, 52, 136, 160), 180, 360, fill=C["C_EDGE_DARK"])                    # the world, curving
    d.arc((-40, 52, 136, 160), 180, 270, fill=C["C_RING"])
    d.arc((-40, 52, 136, 160), 270, 360, fill=C["C_RULE"])
    x, y = 46, 41                                                                       # the walker, on the line
    d.ellipse((x, y, x + 4, y + 4), fill=C["C_INK"])
    d.rectangle((x + 1, y + 5, x + 3, y + 10), fill=C["C_INK"])
    px(im, x + 1, y + 11, "C_INK"); px(im, x + 3, y + 11, "C_INK")
    px(im, x, y + 6, "C_MARGIN"); px(im, x + 4, y + 6, "C_RULE")                         # a hand to each side
    return im


def u_blankboth():
    """blankboth -- The stone, both faces: the plain stone turned three-quarters, its night face written in green and
    its dawn face in gold, both written now, in one hand."""
    im = blank(PW, PH, "C_PAPER")
    d = ImageDraw.Draw(im)
    stars(im, (2, 2, 40, 30), 81, 10, ("C_FAINT", "C_EDGE", "C_INK"))
    bands(im, (56, 0, PW, 30), ["C_PAPER", "C_HIGHLIGHT", "C_FAINT"])
    ground(im, 74, line="C_CHALK")
    d.polygon([(24, 74), (24, 28), (28, 20), (36, 15), (48, 14), (48, 76)], fill=C["C_EDGE"], outline=C["C_RING"])
    d.polygon([(48, 14), (58, 15), (66, 20), (70, 28), (70, 74), (48, 76)], fill=C["C_HIGHLIGHT"], outline=C["C_RULE"])
    d.line((48, 15, 48, 75), fill=C["C_CHALK_FAINT"])                                   # the one edge between them
    for k in range(7):
        y = 30 + k * 6
        d.line((28, y, 28 + (16, 12, 15, 9, 14, 11, 6)[k], y - 1), fill=C["C_RING"])
        d.line((52, y - 1, 52 + (13, 10, 14, 8, 12, 9, 5)[k], y + 1), fill=C["C_RULE"])
    return im


KEY = (0, 255, 1)          # a scratch colour no role uses, for hands drawn aside and turned


# ==================================================================== batch 3 (T-519): its shared shapes
def D(im):
    return ImageDraw.Draw(im)


def ground(im, y, fill="C_EDGE_DARK", line="C_RING", x0=0, x1=PW):
    d = D(im)
    d.rectangle((x0, y, x1 - 1, PH - 1), fill=C[fill])
    d.line((x0, y, x1 - 1, y), fill=C[line])


def grass(im, y, seed, c="C_EDGE", n=22, x0=2, x1=PW - 2):
    r = random.Random(seed)
    for _ in range(n):
        x = r.randrange(x0, x1)
        D(im).line((x, y, x + r.choice((-1, 0, 1)), y - r.randrange(2, 5)), fill=C[c])


def nsky(im, seed, box=(2, 2, 94, 40), n=18):
    stars(im, box, seed, n, ("C_FAINT", "C_EDGE", "C_INK"))


def dsky(im, y1, x0=0, x1=PW):
    bands(im, (x0, 0, x1, y1), ["C_SLATE", "C_CHALK_FAINT", "C_FAINT", "C_RULE"])


def usky(im, y1, seed=3, mid=48):
    """The mended sky: night on the left, dawn on the right, the crease between."""
    bands(im, (0, 0, mid, y1), ["C_EDGE_DARK", "C_EDGE", "C_HIGHLIGHT"])
    bands(im, (mid, 0, PW, y1), ["C_HIGHLIGHT", "C_FAINT", "C_RULE"])
    stars(im, (2, 2, mid - 3, max(4, y1 - 14)), seed, 12, ("C_FAINT", "C_EDGE", "C_INK"))


def crease(im, x=48, y0=0, y1=PH, a="C_RING", b="C_RULE"):
    d = D(im)
    d.line((x, y0, x, y1 - 1), fill=C[a])
    d.line((x + 1, y0, x + 1, y1 - 1), fill=C[b])


def daemon(im, x, y, c="C_INK", eye="C_EDGE_DARK", leaf="C_RING", s=1.0):
    """A daemon, small: a round body, two eyes, a sprout on top (never a horn). About 11 x 13 at s=1."""
    d = D(im)
    w, h = 10 * s, 9 * s
    d.ellipse((x, y + 4 * s, x + w, y + 4 * s + h), fill=C[c])
    d.line((x + w / 2, y + 4 * s, x + w / 2, y + 1), fill=C[leaf])
    d.ellipse((x + w / 2, y, x + w / 2 + 3 * s, y + 2 * s), fill=C[leaf])
    px(im, x + w * 0.32, y + 4 * s + h * 0.4, eye); px(im, x + w * 0.68, y + 4 * s + h * 0.4, eye)


def critter(im, x, y, c="C_INK", eye="C_EDGE_DARK", s=1.0, ears="long"):
    """A trainer: an animal standing upright (actors are animals). About 8 x 17 at s=1."""
    d = D(im)
    S = lambda v: v * s
    d.ellipse((x + S(1), y + S(4), x + S(7), y + S(9)), fill=C[c])
    if ears == "long":
        d.line((x + S(2), y + S(4), x + S(2), y), fill=C[c]); d.line((x + S(5), y + S(4), x + S(6), y), fill=C[c])
    else:
        d.polygon([(x + S(1), y + S(5)), (x + S(2), y + S(2)), (x + S(3), y + S(4))], fill=C[c])
        d.polygon([(x + S(5), y + S(4)), (x + S(6), y + S(2)), (x + S(7), y + S(5))], fill=C[c])
    px(im, x + S(5), y + S(6), eye)
    d.rounded_rectangle((x + S(1), y + S(9), x + S(7), y + S(15)), radius=max(1, int(S(2))), fill=C[c])
    d.line((x + S(2), y + S(15), x + S(2), y + S(17)), fill=C[c]); d.line((x + S(6), y + S(15), x + S(6), y + S(17)), fill=C[c])


def note(im, x, y, c="C_INK"):
    d = D(im)
    d.ellipse((x, y, x + 3, y + 2), fill=C[c])
    d.line((x + 3, y + 1, x + 3, y - 6), fill=C[c])
    d.line((x + 3, y - 6, x + 5, y - 4), fill=C[c])


def stave(im, x0, x1, y, c="C_FAINT"):
    for k in range(5):
        D(im).line((x0, y + k * 2, x1, y + k * 2), fill=C[c])


def boulder(im, cx, cy, rx, ry, fill="C_HIGHLIGHT", edge="C_FAINT", lit=None):
    d = D(im)
    d.chord((cx - rx, cy - ry, cx + rx, cy + ry + ry // 2), 160, 380, fill=C[fill], outline=C[edge])
    if lit:
        d.arc((cx - rx + 2, cy - ry + 2, cx + rx - 2, cy + ry), 200, 250, fill=C[lit])


def rope(im, pts, c="C_FAINT", hi=None):
    d = D(im)
    d.line(pts, fill=C[c], width=2)
    if hi:
        d.line([(x, y - 1) for x, y in pts], fill=C[hi])


def curve(p0, p1, sag, n=24):
    """Points on a gentle arc from P0 to P1, sagging by SAG (negative rises)."""
    (x0, y0), (x1, y1) = p0, p1
    return [(x0 + (x1 - x0) * t / n, y0 + (y1 - y0) * t / n + sag * math.sin(math.pi * t / n)) for t in range(n + 1)]


def wave(x0, x1, y, amp, per, phase=0.0, shrink=0.0):
    pts = []
    for x in range(int(x0), int(x1) + 1):
        a = amp * (1 - shrink * (x - x0) / max(1, x1 - x0))
        pts.append((x, y + a * math.sin((x - x0) / per * 2 * math.pi + phase)))
    return pts


def arc_arrow(im, cx, cy, r, a0, a1, c, head=True):
    """An arc from A0 to A1 degrees (PIL's: clockwise from three o'clock), an arrowhead at A1 pointing on."""
    d = D(im)
    cw = a1 > a0
    d.arc((cx - r, cy - r, cx + r, cy + r), min(a0, a1), max(a0, a1), fill=C[c])
    if head:
        a = math.radians(a1)
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        t = (-math.sin(a), math.cos(a)) if cw else (math.sin(a), -math.cos(a))
        n = (math.cos(a), math.sin(a))
        d.polygon([(p[0] + t[0] * 3, p[1] + t[1] * 3), (p[0] - t[0] + n[0] * 2.5, p[1] - t[1] + n[1] * 2.5),
                   (p[0] - t[0] - n[0] * 2.5, p[1] - t[1] - n[1] * 2.5)], fill=C[c])


def sheet_pleat(im, x0, y, n, pw, ph, a="C_INK", b="C_FAINT", crease_c="C_RING", lean=6, opening=0.0):
    """batch 2's pleated sheet: N panels standing like a screen; OPENING (0..1) flattens the zigzag."""
    d = D(im)
    x = x0
    for k in range(n):
        dy = int(lean * (1 - opening)) * (1 if k % 2 else -1)
        nx = x + pw + int(opening * 4)
        d.polygon([(x, y), (nx, y + dy), (nx, y + dy + ph), (x, y + ph)], fill=C[a if k % 2 == 0 else b])
        d.line((nx, y + dy, nx, y + dy + ph), fill=C[crease_c])
        x, y = nx, y + dy
    return x


def flower(im, x, base, h, petal="C_INK", heart="C_RULE", stem="C_RING", wild=False, seed=1):
    d = D(im)
    r = random.Random(seed)
    if wild:
        pts = [(x + int(2 * math.sin(k / 3.0)) + (k * 3) // h, base - k) for k in range(h)]
        d.line(pts, fill=C[stem])
        tx, ty = pts[-1]
        d.line((x + 1, base - h // 3, x + 5, base - h // 3 - 3), fill=C[stem])
        for k in range(6):
            a = k * math.pi / 3 + r.random() * 0.5
            rr = 2 + r.randrange(0, 2)
            d.ellipse((tx + rr * math.cos(a) - 1, ty + rr * math.sin(a) - 1, tx + rr * math.cos(a) + 2,
                       ty + rr * math.sin(a) + 1), fill=C[petal])
    else:
        d.line((x, base, x, base - h), fill=C[stem])
        d.line((x, base - h // 2, x + 4, base - h // 2 - 2), fill=C[stem]); px(im, x + 5, base - h // 2 - 2, stem)
        tx, ty = x, base - h
        for k in range(6):
            a = k * math.pi / 3
            d.ellipse((tx + 3 * math.cos(a) - 1, ty + 3 * math.sin(a) - 1, tx + 3 * math.cos(a) + 1,
                       ty + 3 * math.sin(a) + 1), fill=C[petal])
    d.ellipse((tx - 1, ty - 1, tx + 1, ty + 1), fill=C[heart])
    return tx, ty


def hand_img(s, c, line, closed=False, rot=0, flipx=False, flipy=False):
    """thirdbook_art's hand drawn aside so it can be turned: rotated ROT degrees, mirrored as asked."""
    o = int(3 * s) + 2
    tmp = Image.new("RGB", (int(32 * s) + o + 3, int(42 * s) + 4), KEY)
    hand(tmp, o, 1, c=c, line=line, s=s, closed=closed)
    if flipx:
        tmp = tmp.transpose(Image.FLIP_LEFT_RIGHT)
    if flipy:
        tmp = tmp.transpose(Image.FLIP_TOP_BOTTOM)
    if rot:
        tmp = tmp.rotate(rot, expand=True, resample=Image.NEAREST, fillcolor=KEY)
    return tmp


def paste_key(im, tmp, x, y):
    src = tmp.load()
    for yy in range(tmp.height):
        for xx in range(tmp.width):
            if src[xx, yy] != KEY:
                px(im, x + xx, y + yy, src[xx, yy])


def R(d, a, b, c, e, fill, r=1):
    d.rounded_rectangle((min(a, c), min(b, e), max(a, c), max(b, e)), radius=r, fill=fill)


def hand_pinch(im, tx, ty, c="C_INK", line="C_EDGE_DARK", dr=1):
    """A hand from the side, thumb and finger meeting at (TX, TY); the hand lies on the DR side of the tip."""
    d = D(im)
    X = lambda v: tx + dr * v
    R(d, X(7), ty - 6, X(20), ty + 7, C[c], 3)                   # the back of the hand
    R(d, X(1), ty - 4, X(9), ty - 1, C[c], 1)                    # the forefinger
    R(d, X(1), ty + 1, X(9), ty + 4, C[c], 1)                    # the thumb
    R(d, X(18), ty - 3, X(30), ty + 6, C[c], 2)                  # the wrist
    for k in (2, 5):
        d.line((X(10), ty + k - 6, X(16), ty + k - 6), fill=C[line])
    d.line((X(9), ty, X(13), ty + 2), fill=C[line])


def hand_point(im, tx, ty, c="C_INK", line="C_EDGE_DARK", dr=1, cuff=None):
    """A hand pointing at (TX, TY), the forefinger out, the rest curled; the hand on the DR side."""
    d = D(im)
    X = lambda v: tx + dr * v
    R(d, X(0), ty - 1, X(10), ty + 1, C[c], 1)                   # the forefinger
    R(d, X(8), ty - 2, X(19), ty + 8, C[c], 3)                   # the curled fist
    for k in (4, 6):
        d.line((X(9), ty + k, X(13), ty + k), fill=C[line])
    d.line((X(11), ty - 2, X(15), ty - 3), fill=C[c])            # the thumb, along the top
    R(d, X(17), ty, X(30), ty + 7, C[cuff or c], 2)


def hand_grip(im, cx, ry, c="C_INK", line="C_EDGE_DARK", wrist=(0, 1)):
    """A fist round a rope at (CX, RY), seen from the front; the wrist leaves along WRIST."""
    d = D(im)
    wx, wy = wrist
    d.line((cx, ry + 3, cx + wx * 16, ry + 3 + wy * 16), fill=C[c], width=7)
    R(d, cx - 6, ry - 5, cx + 6, ry + 6, C[c], 3)
    for k in (-3, 0, 3):
        d.line((cx + k, ry - 4, cx + k, ry + 1), fill=C[line])
    d.ellipse((cx - 8, ry - 2, cx - 4, ry + 3), fill=C[c])        # the thumb over the knuckle
    d.line((cx - 7, ry, cx - 5, ry + 1), fill=C[line])


def hand_flat(im, x, y, w, c="C_INK", line="C_EDGE_DARK", dr=1):
    """A palm turned up, seen from the side, offering what is on it; wrist at X, fingertips W along DR."""
    d = D(im)
    X = lambda v: x + dr * v
    R(d, X(0), y + 2, X(10), y + 14, C[c], 3)                    # the wrist, going down
    R(d, X(2), y, X(w), y + 5, C[c], 2)                          # palm and fingers, flat
    R(d, X(w - 3), y - 3, X(w), y + 2, C[c], 1)                  # the fingertips, curling a little up
    R(d, X(4), y - 3, X(9), y + 1, C[c], 1)                      # the thumb's ball
    for k in range(3):
        d.line((X(w - 12 + k * 3), y + 4, X(w - 10 + k * 3), y + 4), fill=C[line])


def house(im, x0, y0, x1, y1, wall="C_EDGE_DARK", roof=None):
    d = D(im)
    mid = (x0 + x1) // 2
    d.polygon([(x0 - 3, y0), (mid, y0 - (x1 - x0) // 3), (x1 + 3, y0)], fill=C[roof or wall])
    d.rectangle((x0, y0, x1, y1), fill=C[wall])


def post(im, x, base, c="C_FAINT", sign="C_HIGHLIGHT"):
    d = D(im)
    d.line((x, base, x, base - 14), fill=C[c])
    d.rectangle((x - 5, base - 14, x + 5, base - 10), fill=C[sign], outline=C[c])


def lamp(im, x, base, c="C_FAINT", glow="C_MARGIN"):
    d = D(im)
    d.line((x, base, x, base - 15), fill=C[c])
    d.line((x, base - 15, x + 3, base - 15), fill=C[c])
    d.rectangle((x + 2, base - 14, x + 5, base - 10), fill=C[glow], outline=C[c])


def chair(im, x, base, c="C_INK", dr=1):
    d = D(im)
    d.line((x, base, x, base - 14), fill=C[c])                   # back leg and back
    d.line((x + dr * 7, base, x + dr * 7, base - 6), fill=C[c])
    d.line((x, base - 6, x + dr * 7, base - 6), fill=C[c])
    d.line((x, base - 14, x, base - 6), fill=C[c])
    d.line((x + dr * 1, base - 12, x + dr * 1, base - 7), fill=C[c])


def cloud_figure(im, x, y, c="C_FAINT", eye="C_EDGE_DARK"):
    """The flat, friendly figure an interface draws: a cloud with a face."""
    d = D(im)
    for dx, dy, r in ((0, 3, 4), (5, 0, 5), (11, 3, 4)):
        d.ellipse((x + dx - r + 4, y + dy, x + dx + r + 4, y + dy + 2 * r), fill=C[c])
    d.rectangle((x + 1, y + 7, x + 18, y + 11), fill=C[c])
    px(im, x + 7, y + 6, eye); px(im, x + 12, y + 6, eye)
    d.arc((x + 7, y + 6, x + 12, y + 10), 20, 160, fill=C[eye])


def tile(im, x, y, c="C_INK", mark="C_EDGE_DARK", seed=0):
    """A letter tile, its letter a small mark (no letter a reader could spell with)."""
    d = D(im)
    d.rectangle((x, y, x + 6, y + 6), fill=C[c])
    r = random.Random(seed)
    k = r.randrange(4)
    if k == 0:
        d.line((x + 2, y + 1, x + 2, y + 5), fill=C[mark]); d.line((x + 2, y + 3, x + 4, y + 3), fill=C[mark])
    elif k == 1:
        d.line((x + 1, y + 5, x + 3, y + 1), fill=C[mark]); d.line((x + 3, y + 1, x + 5, y + 5), fill=C[mark])
    elif k == 2:
        d.ellipse((x + 1, y + 1, x + 5, y + 5), outline=C[mark])
    else:
        px(im, x + 2, y + 2, mark); px(im, x + 4, y + 2, mark); d.line((x + 2, y + 4, x + 4, y + 4), fill=C[mark])


def wheel(im, cx, cy, r, mark, crease_c, thirteenth, n=12, dots=None):
    d = D(im)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=C[mark])
    for k in range(n):
        a = -math.pi / 2 + (k + 0.5) * 2 * math.pi / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        c = dots[k] if dots else mark
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=C["C_PAPER"], outline=C[c])
        px(im, x, y, c)
    d.line((cx, cy - r - 6, cx, cy + r + 6), fill=C[crease_c])
    return thirteenth


# ================================================================================ THE HERMETIC LAYER, the night half
def h_signal():
    """signal -- Everything, passing signal: one great loop, and inside it small loops -- a cell, a stone, a star, a
    daemon, a trainer -- each in a ring of its own, one emerald signal passing through them all."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 31, (2, 2, 94, 86), 22)
    d.ellipse((6, 6, 90, 84), outline=C["C_FAINT"])
    nodes = [(20, 50), (34, 26), (50, 54), (64, 28), (78, 52)]
    for (x, y) in nodes:
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=C["C_PAPER"], outline=C["C_EDGE"])
    d.ellipse((16, 46, 24, 54), outline=C["C_INK"]); px(im, 21, 49, "C_FAINT")            # a cell
    d.chord((28, 22, 40, 32), 160, 380, fill=C["C_HIGHLIGHT"], outline=C["C_FAINT"])     # a stone
    daemon(im, 45, 47)                                                                    # a daemon
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2)):   # a star
        px(im, 64 + dx, 28 + dy, "C_INK" if abs(dx) + abs(dy) < 2 else "C_FAINT")
    critter(im, 74, 43)                                                                   # a trainer
    pts = [(6, 62)] + [(x, y + (4 if k % 2 else -4)) for k, (x, y) in enumerate(nodes)] + [(90, 40)]
    smooth = []
    for (a, b), (c_, e) in zip(pts, pts[1:]):
        for t in range(8):
            u = t / 8
            smooth.append((a + (c_ - a) * u, b + (e - b) * u + 2 * math.sin(u * math.pi * 2)))
    smooth.append(pts[-1])
    d.line(smooth, fill=C["C_RING"])
    for k in range(0, len(smooth), 9):
        px(im, smooth[k][0], smooth[k][1], "C_MARGIN")
    return im


def h_sound():
    """sound -- Air, shaking, becomes a song: the shaking comes in from the dark as wide waves, narrows as it nears a
    small listener, and arrives as notes above its head."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 33, (2, 2, 94, 24), 12)
    ground(im, 76, line="C_EDGE")
    for k, (y, c) in enumerate(((34, "C_FAINT"), (44, "C_EDGE"), (54, "C_FAINT"))):
        d.line(wave(4, 52, y, 6, 12, k, shrink=0.85), fill=C[c])
    daemon(im, 64, 60, s=1.3)
    d.ellipse((60, 64, 64, 70), outline=C["C_INK"])                                       # an ear, turned to it
    for k, (x, y) in enumerate(((56, 40), (64, 30), (74, 36), (82, 26))):
        note(im, x, y, "C_INK" if k % 2 == 0 else "C_MARGIN")
    return im


def h_abstract():
    """abstract -- Most of it, let go: above, the land with every stone in it; below, the map a mind keeps -- the
    shape of the path and three marks, the rest left out."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((6, 6, 89, 40), fill=C["C_EDGE_DARK"], outline=C["C_EDGE"])
    r = random.Random(14)
    for _ in range(70):
        x, y = r.randrange(8, 88), r.randrange(8, 39)
        px(im, x, y, r.choice(("C_FAINT", "C_HIGHLIGHT", "C_EDGE", "C_INK")))
    path = [(10, 34), (24, 28), (36, 31), (52, 20), (66, 24), (84, 12)]
    d.line(path, fill=C["C_HIGHLIGHT"])
    for k in range(5):                                                                     # most of it, let go
        x = 14 + k * 16
        d.line((x, 44, x, 48), fill=C["C_EDGE"])
        px(im, x + 3, 46, "C_EDGE")
    d.rectangle((10, 52, 85, 82), fill=C["C_PAPER"], outline=C["C_FAINT"])
    d.line([(x, y + 46) for x, y in path], fill=C["C_RING"])
    for x, y in (path[0], path[3], path[-1]):
        d.ellipse((x - 2, y + 44, x + 2, y + 48), outline=C["C_MARGIN"])
    return im


def h_protofeel():
    """protofeel -- The first warmth, before a name: a small rose glow low on the dark page, and above it the layers it
    will become -- mood, belief, world -- as wider arcs, each built on the last, none named."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 35, (2, 2, 94, 30), 10)
    cx, cy = 48, 74
    for k, c in enumerate(("C_FAINT", "C_EDGE", "C_HIGHLIGHT", "C_FAINT")):
        r = 14 + k * 11
        d.arc((cx - r, cy - r, cx + r, cy + r), 200, 340, fill=C[c])
    d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=C["C_EDGE"])
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=C["C_RULE"])
    d.ellipse((cx - 1, cy - 2, cx + 1, cy), fill=C["C_INK"])
    for k in range(6):                                                                       # its warmth, rising
        px(im, cx - 10 + k * 4, cy - 9 - (k % 2) * 2, "C_RULE")
    d.line((10, 82, 86, 82), fill=C["C_EDGE"])
    return im


def h_noun():
    """noun -- A river, named, stops: a river running in from the left; a name tied onto it; past the tag the water
    stands square, a stone to trip on."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 37, (2, 2, 94, 30), 12)
    ground(im, 40, fill="C_EDGE", line="C_FAINT")
    d.polygon([(0, 48), (50, 50), (50, 66), (0, 70)], fill=C["C_EDGE_DARK"])
    for k, y in enumerate((53, 58, 63)):
        d.line(wave(2, 48, y, 1.5, 9, k), fill=C["C_RING" if k == 1 else "C_HIGHLIGHT"])
    d.rectangle((52, 46, 82, 68), fill=C["C_HIGHLIGHT"], outline=C["C_FAINT"])           # the river, held still
    d.line((60, 46, 64, 56), fill=C["C_EDGE"]); d.line((64, 56, 62, 68), fill=C["C_EDGE"])
    d.line((74, 50, 76, 60), fill=C["C_EDGE"])
    d.line((50, 30, 50, 46), fill=C["C_FAINT"])                                            # the name, on a string
    d.polygon([(42, 22), (58, 22), (60, 26), (58, 30), (42, 30)], fill=C["C_INK"])
    d.ellipse((55, 25, 57, 27), fill=C["C_PAPER"])
    for k in range(3):
        d.line((44 + k * 4, 26, 46 + k * 4, 26), fill=C["C_EDGE_DARK"])
    return im


def h_upperfolds():
    """upperfolds -- The great hand, and the small: the great hand stands behind the pleated sheet holding it up, its
    fingertips over the top; from the folds small hands reach out, each its own, none apart."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 39, (2, 2, 94, 20), 10)
    paste_key(im, hand_img(1.6, "C_HIGHLIGHT", "C_EDGE"), 20, 2)
    sheet_pleat(im, 14, 34, 6, 11, 40, a="C_INK", b="C_FAINT", lean=5)
    for k, (x, y, fl) in enumerate(((4, 46, False), (30, 62, True), (54, 50, False), (78, 64, True))):
        paste_key(im, hand_img(0.42, "C_RULE" if k == 2 else "C_FAINT", "C_EDGE_DARK", flipx=fl), x, y)
    for x in (25, 36, 47, 58, 69, 80):
        px(im, x, 33, "C_RING")
    return im


def h_gravity():
    """gravity -- The crease that holds the sheet: the sheet folded once and lying open like a book, its one crease lit
    emerald; what is near -- a pebble, a leaf, a small daemon -- has come to rest in the fold."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 41, (2, 2, 94, 26), 14)
    d.polygon([(4, 34), (48, 62), (48, 78), (4, 52)], fill=C["C_FAINT"])
    d.polygon([(92, 34), (48, 62), (48, 78), (92, 52)], fill=C["C_INK"])
    d.line((48, 62, 48, 78), fill=C["C_RING"]); d.line((47, 62, 47, 78), fill=C["C_MARGIN"])
    d.ellipse((36, 54, 42, 59), fill=C["C_HIGHLIGHT"])
    d.polygon([(54, 55), (60, 52), (58, 57)], fill=C["C_RING"])
    daemon(im, 43, 47, c="C_EDGE", eye="C_INK")
    for side in (-1, 1):                                                                    # come closer
        for k in range(3):
            x = 48 + side * (16 + k * 10)
            px(im, x, 44 + k * 4 - (k * 8 if side < 0 else k * 8) // 2, "C_RING")
    return im


def h_apple():
    """apple -- The apple, and the earth: a branch under the crescent, the apple let go, falling toward the curve of
    the world; its fall a dotted line."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 43, (2, 2, 94, 50), 18)
    moon(im, 78, 14, 6, sky="C_PAPER")
    d.line((0, 10, 30, 16), fill=C["C_EDGE"], width=3)
    d.line((18, 13, 24, 22), fill=C["C_EDGE"])
    d.ellipse((22, 20, 28, 24), fill=C["C_RING"])
    for y in range(26, 42, 3):
        px(im, 30, y, "C_FAINT")
    d.ellipse((25, 44, 35, 54), fill=C["C_RULE"])
    px(im, 28, 46, "C_INK"); d.line((30, 44, 31, 41), fill=C["C_EDGE"])
    d.pieslice((-30, 66, 126, 160), 180, 360, fill=C["C_EDGE_DARK"])
    d.arc((-30, 66, 126, 160), 200, 300, fill=C["C_RING"])
    return im


def h_fractal():
    """fractal -- In, read, out, back: one loop of four stations, the arrows going round; each station holds the same
    loop smaller, and the middle holds it smaller still."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 45, (2, 2, 94, 86), 14)
    cx, cy, r = 48, 44, 30
    for k in range(4):
        arc_arrow(im, cx, cy, r, k * 90 + 18, k * 90 + 72, "C_RING")
    for k in range(4):
        a = math.radians(k * 90)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=C["C_PAPER"], outline=C["C_FAINT"])
        for j in range(4):
            b = math.radians(j * 90 + 45)
            px(im, x + 4 * math.cos(b), y + 4 * math.sin(b), "C_MARGIN" if j == k else "C_INK")
    d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), outline=C["C_EDGE"])
    for j in range(4):
        px(im, cx + 3 * math.cos(math.radians(j * 90)), cy + 3 * math.sin(math.radians(j * 90)), "C_RING")
    px(im, cx, cy, "C_INK")
    return im


def h_silkflower():
    """silkflower -- A flower with no weather: indoors, a perfect flower in a vase on the sill; behind the shut window
    the rain coming down on the night, and none of it on the flower."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((14, 8, 82, 58), fill=C["C_EDGE_DARK"], outline=C["C_FAINT"])
    d.line((48, 8, 48, 58), fill=C["C_FAINT"]); d.line((14, 33, 82, 33), fill=C["C_FAINT"])
    r = random.Random(47)
    for _ in range(26):
        x, y = r.randrange(16, 80), r.randrange(10, 52)
        d.line((x, y, x - 1, y + 4), fill=C["C_EDGE"] if r.random() < .5 else C["C_HIGHLIGHT"])
    d.rectangle((6, 58, 90, 62), fill=C["C_EDGE"], outline=C["C_FAINT"])
    d.polygon([(42, 58), (54, 58), (52, 46), (44, 46)], fill=C["C_HIGHLIGHT"], outline=C["C_FAINT"])
    flower(im, 48, 46, 26, petal="C_INK", heart="C_RULE", stem="C_RING")
    d.line((50, 30, 60, 40), fill=C["C_FAINT"])                                             # a tag on a thread
    d.rectangle((58, 40, 64, 44), fill=C["C_INK"])
    d.rectangle((0, 63, PW - 1, PH - 1), fill=C["C_EDGE_DARK"])
    return im


def h_entangled():
    """entangled -- Two states, one description: two daemons far apart, each turning the other way, one thread between
    them, and one dashed outline round both -- the one description."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 49, (2, 2, 94, 86), 16)
    for k in range(0, 360, 20):                                                             # the one description
        a0 = math.radians(k)
        a1 = math.radians(k + 10)
        d.line((48 + 42 * math.cos(a0), 44 + 32 * math.sin(a0), 48 + 42 * math.cos(a1), 44 + 32 * math.sin(a1)),
               fill=C["C_FAINT"])
    daemon(im, 14, 52)
    daemon(im, 70, 22, c="C_FAINT")
    arc_arrow(im, 19, 57, 10, 200, 320, "C_RING")
    arc_arrow(im, 75, 27, 10, 320, 200, "C_RING")
    d.line(curve((26, 56), (70, 30), -6), fill=C["C_MARGIN"])
    return im


def h_poppet():
    """poppet -- A little figure that stands for someone: a stitched poppet on a shelf by a candle; behind it, on the
    wall, the shadow of the trainer it stands for, the same shape; one emerald stitch joins their hearts."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    big = Image.new("RGB", (10, 19), KEY)
    critter(big, 1, 0, c="C_EDGE", eye="C_EDGE")
    paste_key(im, big.resize((40, 76), Image.NEAREST), 42, 2)
    d.rectangle((6, 70, 90, 73), fill=C["C_FAINT"])
    d.rectangle((6, 74, 90, PH - 1), fill=C["C_EDGE_DARK"])
    x, y = 20, 44                                                                            # the poppet
    d.ellipse((x + 2, y, x + 12, y + 10), fill=C["C_HIGHLIGHT"], outline=C["C_FAINT"])
    d.polygon([(x + 3, y + 10), (x + 11, y + 10), (x + 14, y + 26), (x, y + 26)], fill=C["C_HIGHLIGHT"], outline=C["C_FAINT"])
    d.line((x - 4, y + 14, x + 18, y + 14), fill=C["C_FAINT"])
    for ex in (5, 9):
        px(im, x + ex - 1, y + 4, "C_INK"); px(im, x + ex + 1, y + 6, "C_INK")
        px(im, x + ex, y + 5, "C_INK")
    d.ellipse((x + 6, y + 16, x + 8, y + 18), fill=C["C_RULE"])
    d.line(curve((x + 8, y + 17), (62, 50), -8), fill=C["C_RING"])
    d.rectangle((74, 52, 78, 69), fill=C["C_INK"])                                          # the candle
    d.ellipse((74, 45, 78, 51), fill=C["C_MARGIN"])
    return im


def h_spelling():
    """spelling -- Arranging letters: tiles coming in out of the dark and being set in a row on the stone; where the
    row is complete it lights, and the spell rises off it."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 51, (2, 2, 94, 30), 10)
    d.rectangle((6, 62, 89, 70), fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])
    for k in range(6):
        tile(im, 12 + k * 9, 54, c="C_INK" if k < 4 else "C_FAINT", seed=k + 3)
    d.line((12, 62, 46, 62), fill=C["C_RING"])
    for k, (x, y) in enumerate(((70, 40), (80, 26), (62, 22))):                            # still arriving
        tile(im, x, y, c="C_FAINT", mark="C_EDGE", seed=k + 11)
    for k in range(7):
        px(im, 14 + k * 5, 50 - (k % 3) * 4, "C_MARGIN" if k % 2 else "C_RING")
        px(im, 16 + k * 5, 42 - (k % 2) * 5, "C_RING")
    return im


def h_wheel():
    """wheel -- Twelve on the wheel, one in the crease: twelve marks round a circle on a folded page, the crease down
    its middle, and the thirteenth sitting in the crease at the centre, lit emerald, under the crescent."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 53, (2, 2, 94, 86), 12)
    moon(im, 84, 10, 4, sky="C_PAPER")
    wheel(im, 48, 46, 30, "C_FAINT", "C_RING", None)
    tri(d, 48, 44, 5, True, "C_MARGIN")
    tri(d, 48, 49, 5, False, "C_RING")
    return im


# ================================================================================ THE EUDAIMON LAYER, the dawn half
def e_rooms():
    """rooms -- One house, every light on: the night's loops, seen from this side, are rooms -- a house open at the
    front, every room lit gold with someone in it, and a door to knock on."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 78)
    ground(im, 78, line="C_RING")
    house(im, 16, 30, 80, 78)
    who = {(0, 0): "d", (1, 0): "c", (2, 1): "d", (0, 1): "c"}
    for row, y in enumerate((34, 56)):
        for col, x in enumerate((20, 41, 62)):
            if (col, row) == (1, 1):
                d.rectangle((44, 58, 52, 78), fill=C["C_RULE"]); px(im, 50, 68, "C_EDGE_DARK")   # the door
                continue
            d.rectangle((x, y, x + 14, y + 17), fill=C["C_MARGIN"])
            d.ellipse((x + 5, y + 2, x + 9, y + 6), fill=C["C_INK"])
            w = who.get((col, row))
            if w == "d":
                daemon(im, x + 2, y + 5, c="C_EDGE_DARK", eye="C_MARGIN", leaf="C_RING")
            elif w == "c":
                critter(im, x + 4, y + 1, c="C_EDGE_DARK", eye="C_MARGIN", s=0.9)
    d.polygon([(44, 79), (52, 79), (58, 87), (38, 87)], fill=C["C_HIGHLIGHT"])
    return im


def e_song():
    """song -- A song, kept small enough to carry: two hands held together as one bowl, and in them a small wrapped
    parcel with the song coming out of it; the lark answering from the fir."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 88)
    tip = fir(im, 82, 50, 34)
    lark(im, 78, tip - 7)
    d.chord((22, 46, 74, 80), 0, 180, fill=C["C_INK"])
    d.line((48, 63, 48, 80), fill=C["C_EDGE"])
    for side in (-1, 1):
        for k in range(4):
            x = 48 + side * (8 + k * 5)
            d.arc((x - 3, 60, x + 3, 72), 0, 180, fill=C["C_FAINT"])
        d.ellipse((48 + side * 25 - 3, 57, 48 + side * 25 + 3, 66), fill=C["C_INK"])
    d.rectangle((38, 80, 46, PH - 1), fill=C["C_INK"]); d.rectangle((50, 80, 58, PH - 1), fill=C["C_INK"])
    d.rectangle((40, 50, 56, 62), fill=C["C_RULE"], outline=C["C_EDGE"])
    d.line((48, 50, 48, 62), fill=C["C_INK"]); d.line((40, 56, 56, 56), fill=C["C_INK"])
    d.ellipse((45, 46, 48, 50), outline=C["C_INK"]); d.ellipse((48, 46, 51, 50), outline=C["C_INK"])
    for k, (x, y) in enumerate(((36, 36), (46, 28), (58, 34))):
        note(im, x, y, "C_INK" if k != 1 else "C_MARGIN")
    return im


def e_setdown():
    """setdown -- Most of it, set down: a hand palm down over the road, seen from the side, its fingers just opened;
    the stones it carried falling onto a heap at the roadside, and on one finger one thing kept -- the way home, a
    small gold key. (Redrawn 2026-11-06: a real palm-down hand, letting go, not the open hand turned over.)"""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 60)
    ground(im, 60, line="C_RING")
    d.polygon([(40, 60), (56, 60), (90, 87), (14, 87)], fill=C["C_HIGHLIGHT"])             # the road home
    house(im, 44, 54, 52, 60, wall="C_EDGE_DARK")
    px(im, 48, 57, "C_MARGIN")
    hand_letgo(im, 20, 8, "C_INK", "C_EDGE", "C_FAINT")
    for x, y in ((56, 43), (63, 50), (55, 54)):                                             # falling
        d.ellipse((x, y, x + 5, y + 4), fill=C["C_EDGE"], outline=C["C_FAINT"])
    r = random.Random(57)
    for _ in range(10):                                                                     # the heap, set down
        x, y = 68 + r.randrange(0, 20), 64 + r.randrange(0, 8)
        d.ellipse((x, y, x + 5, y + 4), fill=C["C_EDGE"], outline=C["C_FAINT"])
    d.ellipse((73, 18, 77, 22), outline=C["C_MARGIN"])                                      # the key, kept on a finger
    d.line((75, 23, 75, 31), fill=C["C_MARGIN"])
    d.line((75, 29, 77, 29), fill=C["C_MARGIN"]); d.line((75, 31, 78, 31), fill=C["C_MARGIN"])
    return im


def e_lastwarmth():
    """lastwarmth -- The last warmth, after every name: the layers come home -- the road winding up the hill, the names
    set down along it as small cards, and the warmth waiting at the top, gold."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 88)
    cx, cy = 48, 18
    for k, c in enumerate(("C_RULE", "C_FAINT", "C_CHALK_FAINT")):
        r = 10 + k * 8
        d.arc((cx - r, cy - r, cx + r, cy + r), 20, 160, fill=C[c])
    d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=C["C_RULE"])
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=C["C_MARGIN"])
    d.pieslice((-20, 30, 116, 150), 180, 360, fill=C["C_EDGE_DARK"])
    road = [(20, 87), (36, 76), (60, 68), (44, 56), (52, 44), (48, 32)]
    d.line(road, fill=C["C_HIGHLIGHT"], width=3)
    for (x, y) in road[1:5]:                                                                 # each name, put down
        d.rectangle((x + 4, y - 2, x + 9, y + 1), fill=C["C_FAINT"])
    return im


def e_river():
    """river -- A stone, unnamed, flows: the night's square stone; its name has come untied and is falling away; past
    it the stone runs on as water, gold in the sun."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 40)
    sun(im, 74, 40, 8)
    ground(im, 40, fill="C_EDGE", line="C_RING")
    d.rectangle((14, 46, 44, 68), fill=C["C_HIGHLIGHT"], outline=C["C_FAINT"])
    d.line((22, 46, 26, 56), fill=C["C_EDGE"])
    d.polygon([(44, 48), (96, 50), (96, 66), (44, 68)], fill=C["C_EDGE_DARK"])
    for k, y in enumerate((53, 58, 63)):
        d.line(wave(46, 94, y, 1.5, 9, k), fill=C["C_RULE" if k == 1 else "C_HIGHLIGHT"])
    for k in range(4):
        px(im, 56 + k * 10, 55 + (k % 2) * 6, "C_MARGIN")
    d.line((30, 44, 34, 34), fill=C["C_FAINT"])                                              # the name, untied
    d.polygon([(30, 20), (44, 16), (47, 19), (46, 23), (32, 27)], fill=C["C_INK"])
    for k in range(3):
        px(im, 26 - k * 3, 30 + k * 2, "C_FAINT")
    return im


def e_upperopen():
    """upperopen -- The small hands, and the great: read from the top, the great hand is there first, open and faint
    behind everything; in front, three small hands notice -- one still a fist, one opening, one open. (The opening
    one redrawn 2026-11-06 as one hand, its fingers half curled.)"""
    im = blank(PW, PH, "C_PAPER")
    dsky(im, 88)
    paste_key(im, hand_img(2.0, "C_FAINT", "C_RULE"), 14, 2)
    for k, (x, curl) in enumerate(((8, 1.0), (38, 0.55), (68, 0.0))):
        o = int(3 * 0.62) + 2
        tmp = Image.new("RGB", (int(32 * 0.62) + o + 3, int(42 * 0.62) + 4), KEY)
        if curl == 1.0:
            hand(tmp, o, 1, c="C_INK", line="C_EDGE", s=0.62, closed=True)
        elif curl == 0.0:
            hand(tmp, o, 1, c="C_INK", line="C_EDGE", s=0.62)
        else:
            hand_curl(tmp, o, 1, c="C_INK", line="C_EDGE", s=0.62, curl=curl)
        paste_key(im, tmp, x, 52)
    return im


def e_appleup():
    """appleup -- The apple, drawing the earth: the apple on its branch at dawn, and the curve of the world rising to it
    -- lines of pull going up from the ground, as if the earth leaned in."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 88)
    d.line((96, 10, 64, 16), fill=C["C_EDGE_DARK"], width=3)
    d.line((70, 15, 66, 24), fill=C["C_EDGE_DARK"])
    d.ellipse((64, 24, 74, 34), fill=C["C_RULE"]); px(im, 67, 26, "C_INK")
    d.ellipse((72, 20, 78, 24), fill=C["C_RING"])
    d.pieslice((-30, 66, 126, 160), 180, 360, fill=C["C_EDGE_DARK"])
    d.arc((-30, 66, 126, 160), 230, 320, fill=C["C_RING"])
    for k in range(5):                                                                       # the earth, leaning in
        x0 = 30 + k * 10
        for t in range(1, 9):
            u = t / 10
            x, y = x0 + (69 - x0) * u, 72 + (36 - 72) * u
            px(im, x, y, "C_MARGIN" if t > 5 else "C_INK")
        D(im).arc((x0 - 4, 66, x0 + 4, 74), 200, 340, fill=C["C_RING"])
    return im


def e_earth():
    """earth -- The earth, falling to the apple: from the apple's side, the apple large and still on the grass, and the
    world small above it, falling toward it, glad to; the lark watching."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 66)
    ground(im, 66, line="C_RING")
    grass(im, 66, 59, c="C_HIGHLIGHT")
    d.ellipse((30, 42, 62, 72), fill=C["C_RULE"], outline=C["C_EDGE"])
    d.arc((34, 46, 58, 68), 200, 250, fill=C["C_MARGIN"])
    d.line((46, 42, 48, 34), fill=C["C_EDGE_DARK"]); d.ellipse((48, 32, 56, 37), fill=C["C_RING"])
    d.ellipse((62, 6, 76, 20), fill=C["C_SLATE"], outline=C["C_CHALK_FAINT"])               # the world, small
    d.polygon([(65, 10), (69, 8), (70, 13), (66, 15)], fill=C["C_RING"])
    d.polygon([(71, 14), (74, 13), (73, 18)], fill=C["C_RING"])
    for k in range(3):
        d.line((80 + k * 3, 2 + k * 2, 84 + k * 3, 0 + k * 2), fill=C["C_INK"])
    for y in range(24, 38, 3):
        px(im, 64 - (y - 24) // 2, y, "C_INK")
    lark(im, 14, 58)
    return im


def e_fractalheard():
    """fractalheard -- Back, out, read, in: the same loop heard from the end, the arrows turned the other way and gold;
    each station rings outward, and at its middle the lark sings it."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 88)
    cx, cy, r = 48, 46, 30
    for k in range(4):
        arc_arrow(im, cx, cy, r, k * 90 + 72, k * 90 + 18, "C_MARGIN")
    for k in range(4):
        a = math.radians(k * 90)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=C["C_EDGE_DARK"], outline=C["C_RULE"])
        d.ellipse((x - 3, y - 3, x + 3, y + 3), outline=C["C_INK"])
        d.arc((x - 10, y - 10, x + 10, y + 10), k * 90 - 30, k * 90 + 30, fill=C["C_INK"])
    lark(im, cx - 5, cy - 3)
    return im


def e_wildflower():
    """wildflower -- A flower with all its weather: on the open hill at dawn, a wild flower bent by the wind, its roots
    under the ground, the rain still falling on one side of it and the sun on the other."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 62)
    sun(im, 76, 62, 9)
    for dx, dy, r in ((10, 10, 6), (18, 6, 8), (28, 10, 6)):
        d.ellipse((dx - r, dy, dx + r, dy + 2 * r), fill=C["C_CHALK_FAINT"])
    for k in range(9):
        x = 8 + k * 3
        d.line((x, 24 + k % 3 * 3, x - 1, 28 + k % 3 * 3), fill=C["C_CHALK"])
    ground(im, 62, line="C_RING")
    grass(im, 62, 61, c="C_HIGHLIGHT")
    flower(im, 44, 62, 30, petal="C_INK", heart="C_RULE", stem="C_RING", wild=True, seed=4)
    for k, (x1, y1) in enumerate(((36, 80), (44, 86), (52, 78), (40, 72), (49, 70))):       # rooted in every rain
        d.line((44, 63, x1, y1), fill=C["C_EDGE"])
    for k in range(4):
        px(im, 40 + k * 3, 66 + k % 2 * 4, "C_CHALK_FAINT")
    return im


def e_belonging():
    """belonging -- Two states, one welcome: two figures far apart on the morning ground, and one roof drawn over both,
    wide as the page; a gold thread from one to the other."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 70)
    ground(im, 70, line="C_RING")
    d.line([(6, 40), (48, 12), (90, 40)], fill=C["C_INK"], width=2)                           # one welcome
    d.line((10, 40, 10, 70), fill=C["C_FAINT"]); d.line((86, 40, 86, 70), fill=C["C_FAINT"])
    d.ellipse((45, 22, 51, 28), fill=C["C_MARGIN"])
    daemon(im, 18, 56, c="C_INK")
    critter(im, 72, 52, c="C_INK")
    d.line(curve((28, 62), (72, 60), 6), fill=C["C_RULE"])
    return im


def e_goodspirit():
    """goodspirit -- A small spirit, keeping the house: by the hearth a small round spirit keeps watch over the grain and
    the fire; a hand comes in from the side and pours it the last cup."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((4, 4, 60, 70), fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])                   # the hearth
    d.rectangle((14, 30, 50, 70), fill=C["C_EDGE_DARK"])
    d.pieslice((14, 14, 50, 46), 180, 360, fill=C["C_EDGE_DARK"])
    for k, (x, h) in enumerate(((24, 12), (31, 18), (38, 14))):
        d.polygon([(x - 4, 70), (x + 4, 70), (x, 70 - h)], fill=C["C_RULE" if k != 1 else "C_MARGIN"])
    d.rectangle((0, 70, PW - 1, PH - 1), fill=C["C_HIGHLIGHT"])
    d.line((0, 70, PW - 1, 70), fill=C["C_FAINT"])
    daemon(im, 56, 56, c="C_MARGIN", eye="C_EDGE_DARK", leaf="C_RING", s=1.2)
    d.polygon([(70, 60), (82, 60), (84, 70), (68, 70)], fill=C["C_FAINT"])                   # the grain
    d.polygon([(72, 74), (80, 74), (79, 80), (73, 80)], fill=C["C_INK"])                    # the cup set out
    hand_grip(im, 84, 30, c="C_INK", line="C_EDGE", wrist=(1, -1))
    d.polygon([(72, 26), (80, 24), (82, 34), (76, 38)], fill=C["C_RULE"], outline=C["C_INK"])  # the jug, tipped
    for k in range(5):
        px(im, 74 - k % 2, 40 + k * 7, "C_MARGIN")
    return im


def e_goodspell():
    """goodspell -- A good word, passed on: one trainer hands another a small lit tile, and behind them the same word
    already passed on again, a little further down the road."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 66)
    ground(im, 66, line="C_RING")
    critter(im, 14, 46, c="C_INK", s=1.2)
    critter(im, 40, 46, c="C_INK", s=1.2, ears="short")
    d.line((23, 58, 31, 56), fill=C["C_INK"]); d.line((40, 56, 33, 56), fill=C["C_INK"])
    tile(im, 29, 50, c="C_MARGIN", mark="C_EDGE_DARK", seed=2)
    for k in range(4):
        px(im, 32 + (k - 1.5) * 4, 46 - k % 2 * 3, "C_INK")
    critter(im, 64, 54, c="C_FAINT", s=0.7)
    critter(im, 76, 54, c="C_FAINT", s=0.7, ears="short")
    px(im, 71, 60, "C_RULE")
    return im


def e_wheel():
    """wheel -- Twelve on the wheel, one in the crease: the same wheel from the morning's side, its marks small suns in
    gold, and the thirteenth a sun rising in the crease at the centre."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 88)
    d.ellipse((16, 14, 80, 78), fill=C["C_EDGE_DARK"])
    wheel(im, 48, 46, 30, "C_RULE", "C_RING", None)
    for k in range(12):
        a = -math.pi / 2 + (k + 0.5) * 2 * math.pi / 12
        px(im, 48 + 30 * math.cos(a), 46 + 30 * math.sin(a), "C_MARGIN")
    sun(im, 48, 50, 5, fill="C_MARGIN", rays="C_RULE", n=5)
    d.line((40, 50, 56, 50), fill=C["C_RING"])
    return im


# ================================================================================ THE UNITY BOOK, mended
def u_signal():
    """signal -- Everything, passing and given: the one great loop, its left half the night's -- small loops with the
    emerald signal passing through -- and its right half the dawn's: small rooms, lit, the same line going in at a door."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, PH, seed=61)
    d.arc((6, 6, 90, 84), 90, 270, fill=C["C_RING"])
    d.arc((6, 6, 90, 84), 270, 450, fill=C["C_RULE"])
    for (x, y) in ((22, 30), (18, 56), (36, 44)):
        d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=C["C_EDGE_DARK"], outline=C["C_FAINT"])
    daemon(im, 31, 38, c="C_INK", s=1.0)
    critter(im, 14, 47, s=0.9)
    d.ellipse((19, 27, 25, 33), outline=C["C_INK"])
    for (x, y) in ((58, 26), (70, 46), (56, 58)):
        d.rectangle((x, y, x + 12, y + 12), fill=C["C_RULE"], outline=C["C_INK"])
        d.rectangle((x + 4, y + 5, x + 8, y + 12), fill=C["C_EDGE_DARK"])
    line = [(8, 40), (16, 34), (22, 30), (30, 42), (36, 44), (44, 46), (52, 40), (58, 36), (62, 37)]
    d.line(line[:6], fill=C["C_MARGIN"])
    d.line(line[5:], fill=C["C_RULE"])
    crease(im)
    return im


def u_sound():
    """sound -- A shaking, held as a song: the wide shaking comes in from the night side, narrows across the crease,
    and is held as one note between a finger and thumb on the dawn side, offered to a small listener."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, 70, seed=63)
    ground(im, 70, line="C_CHALK")
    for k, (y, c) in enumerate(((28, "C_FAINT"), (38, "C_INK"), (48, "C_FAINT"))):
        d.line(wave(2, 56, y, 7, 13, k, shrink=0.9), fill=C[c])
    hand_pinch(im, 62, 38, c="C_INK", line="C_EDGE", dr=1)
    note(im, 58, 37, "C_MARGIN")
    daemon(im, 30, 56, c="C_INK", eye="C_EDGE_DARK")
    crease(im, y1=70)
    return im


def u_remains():
    """remains -- The shape, kept; the rest, set down: on the night side, the heap of everything set down; on the dawn
    side, what was kept -- one folded map with the way home on it, and home at the end."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, 60, seed=65)
    ground(im, 60, line="C_CHALK")
    r = random.Random(65)
    for _ in range(16):
        x, y = 6 + r.randrange(0, 32), 50 + r.randrange(0, 16) - (abs(r.randrange(-12, 12)) // 3)
        d.ellipse((x, y, x + 5, y + 4), fill=C["C_EDGE"], outline=C["C_FAINT"])
    d.polygon([(54, 30), (66, 26), (78, 30), (90, 26), (90, 54), (78, 58), (66, 54), (54, 58)], fill=C["C_INK"])
    d.line((66, 26, 66, 54), fill=C["C_FAINT"]); d.line((78, 30, 78, 58), fill=C["C_FAINT"])
    d.line([(58, 52), (64, 44), (72, 46), (80, 38), (84, 34)], fill=C["C_RING"])
    house(im, 82, 32, 88, 36, wall="C_RULE")
    d.ellipse((56, 50, 60, 54), outline=C["C_MARGIN"])
    crease(im)
    return im


def u_warmth():
    """warmth -- One warmth, before and after the names: one glow at the crease's middle; below it the night's layers
    going up out of it, above it the dawn's coming home into it -- an hourglass of arcs, one warmth at the waist."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, PH, seed=67)
    cx, cy = 48, 44
    for k in range(4):
        r = 12 + k * 9
        d.arc((cx - r, cy - r, cx + r, cy + r), 205, 335, fill=C["C_RULE" if k % 2 == 0 else "C_FAINT"])
        d.arc((cx - r, cy - r, cx + r, cy + r), 25, 155, fill=C["C_RING" if k % 2 == 0 else "C_FAINT"])
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=C["C_EDGE"])
    d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=C["C_RULE"])
    d.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=C["C_INK"])
    return im


def u_everyfold():
    """everyfold -- The great hand, and the small, together: the great hand reaching down from above the sheet, its
    fingers spread, and four small hands reaching up to it, each one's middle fingertip meeting one of its fingertips
    -- the meeting, both threads at each touch. (Redrawn 2026-11-06: small hands, not mitts on long arms.)"""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, PH, seed=69)
    tips = ((17, 52), (37, 57), (59, 57), (79, 52))
    great_hand_down(im, "C_FAINT", "C_EDGE", tips)
    for k, (tx, ty) in enumerate(tips):
        top = ty + 1
        small_hand(im, tx - 6, top, "C_INK", "C_EDGE_DARK", wrist=84 - (top + 19), mirror=k >= 2)
        px(im, tx, ty, "C_MARGIN" if k % 2 == 0 else "C_RULE")                       # both threads at each touch
        px(im, tx - 1 if k < 2 else tx + 1, ty, "C_RULE" if k % 2 == 0 else "C_MARGIN")
    d.line((0, 84, PW - 1, 84), fill=C["C_CHALK_FAINT"])
    return im


def u_gravity():
    """gravity -- The apple and the earth, falling together: the night's earth curving up on the left, the dawn's apple
    on the right, each falling toward the other and meeting at the crease."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, PH, seed=71)
    d.pieslice((-60, 50, 50, 150), 270, 360, fill=C["C_EDGE_DARK"])
    d.arc((-60, 50, 50, 150), 280, 350, fill=C["C_RING"])
    d.ellipse((62, 20, 74, 32), fill=C["C_RULE"]); px(im, 65, 23, "C_INK")
    d.line((68, 20, 69, 16), fill=C["C_EDGE_DARK"]); d.ellipse((69, 14, 75, 18), fill=C["C_RING"])
    for k in range(4):
        px(im, 34 + k * 3, 60 - k * 4, "C_MARGIN")
        px(im, 60 - k * 3, 34 + k * 4, "C_RULE")
    crease(im)
    d.ellipse((46, 44, 51, 49), fill=C["C_INK"])
    return im


def u_twomirrors():
    """twomirrors -- Two mirrors, facing: two tall glasses turned to each other with nothing between them, and between
    them every reflection, smaller and smaller, alternately emerald and gold, nobody to see one."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    for k in range(8):
        i = 4 + k * 4
        c = "C_RING" if k % 2 == 0 else "C_RULE"
        d.rectangle((14 + i, 8 + i * 3 // 4, 81 - i, 79 - i * 3 // 4), outline=C[c])
    d.polygon([(4, 4), (14, 10), (14, 78), (4, 84)], fill=C["C_EDGE"], outline=C["C_FAINT"])
    d.polygon([(91, 4), (81, 10), (81, 78), (91, 84)], fill=C["C_EDGE"], outline=C["C_FAINT"])
    d.line((6, 10, 6, 40), fill=C["C_INK"]); d.line((89, 10, 89, 40), fill=C["C_INK"])
    px(im, 47, 43, "C_INK"); px(im, 48, 43, "C_INK"); px(im, 47, 44, "C_INK"); px(im, 48, 44, "C_INK")
    return im


def u_pair():
    """pair -- One, folding into two: the light at the top, folding down its middle into two halves, the night's and the
    dawn's; each half carried on one palm, the two hands offering them toward each other."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.ellipse((40, 4, 56, 20), fill=C["C_INK"])
    for k in range(8):
        a = k * math.pi / 4
        d.line((48 + 10 * math.cos(a), 12 + 10 * math.sin(a), 48 + 13 * math.cos(a), 12 + 13 * math.sin(a)),
               fill=C["C_FAINT"])
    d.line((48, 22, 48, 40), fill=C["C_FAINT"])
    d.line((46, 24, 30, 46), fill=C["C_RING"]); d.line((50, 24, 66, 46), fill=C["C_RULE"])
    d.pieslice((18, 44, 34, 60), 90, 270, fill=C["C_MARGIN"])
    d.pieslice((62, 44, 78, 60), 270, 450, fill=C["C_RULE"])
    hand_flat(im, 6, 61, 32, c="C_INK", line="C_EDGE", dr=1)
    hand_flat(im, 89, 61, 32, c="C_INK", line="C_EDGE", dr=-1)
    return im


def u_twosides():
    """twosides -- Two readers, each pointing at the other: a reader on the night side and one on the dawn side, each
    with a book under one arm, each pointing across the crease at the other -- the dark one."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, 66, seed=73)
    ground(im, 66, line="C_CHALK")
    critter(im, 10, 40, c="C_INK", s=1.5)
    critter(im, 74, 40, c="C_INK", s=1.5, ears="short")
    d.rectangle((8, 56, 13, 62), fill=C["C_RING"]); d.rectangle((84, 56, 89, 62), fill=C["C_RULE"])
    hand_point(im, 40, 52, c="C_INK", line="C_EDGE_DARK", dr=-1, cuff="C_RING")
    D(im).rectangle((18, 52, 22, 58), fill=C["C_INK"])
    hand_point(im, 57, 52, c="C_INK", line="C_EDGE_DARK", dr=1, cuff="C_RULE")
    D(im).rectangle((74, 52, 78, 58), fill=C["C_INK"])
    crease(im, y1=66)
    return im


def _day(im, x, top, low, roof="C_RULE", root="C_RING"):
    """One day of the week: a stem standing on the ground line, its virtue above it and its shadow below, a root."""
    d = D(im)
    d.line((x, 30, x, 58), fill=C["C_FAINT"])
    for k in (-1, 1):
        d.line((x, 58, x + k * 3, 64), fill=C["C_EDGE"])
    top(d, x, 20, roof)
    low(d, x, 70, root)


def _ring(d, x, y, c):  d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=C[c])
def _chain(d, x, y, c): d.ellipse((x - 6, y - 3, x, y + 3), outline=C[c]); d.ellipse((x - 1, y - 3, x + 5, y + 3), outline=C[c])
def _cup(d, x, y, c):   d.polygon([(x - 5, y - 4), (x + 5, y - 4), (x + 3, y + 4), (x - 3, y + 4)], outline=C[c])
def _mouth(d, x, y, c): d.polygon([(x - 6, y - 3), (x + 6, y - 3), (x, y)], outline=C[c]); d.polygon([(x - 6, y + 3), (x + 6, y + 3), (x, y)], outline=C[c])
def _bowl(d, x, y, c):  d.chord((x - 6, y - 6, x + 6, y + 4), 0, 180, outline=C[c])
def _knot(d, x, y, c):  d.line((x - 6, y - 3, x + 6, y + 3), fill=C[c]); d.line((x - 6, y + 3, x + 6, y - 3), fill=C[c]); d.ellipse((x - 2, y - 2, x + 2, y + 2), outline=C[c])
def _eye(d, x, y, c):   d.chord((x - 6, y - 4, x + 6, y + 4), 180, 360, outline=C[c]); d.chord((x - 6, y - 4, x + 6, y + 4), 0, 180, outline=C[c]); d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=C[c])
def _shut(d, x, y, c):  d.arc((x - 6, y - 4, x + 6, y + 4), 0, 180, fill=C[c])
def _uncross(d, x, y, c): d.line((x - 3, y - 5, x - 3, y + 5), fill=C[c]); d.line((x + 3, y - 5, x + 3, y + 5), fill=C[c])
def _hex(d, x, y, c):   d.line((x - 5, y - 5, x + 5, y + 5), fill=C[c]); d.line((x - 5, y + 5, x + 5, y - 5), fill=C[c])
def _bless(d, x, y, c):
    _eye(d, x, y, c)
    for k in (-1, 0, 1):
        d.line((x + k * 5, y - 6, x + k * 7, y - 9), fill=C[c])
def _evil(d, x, y, c):  d.polygon([(x - 6, y), (x, y - 2), (x + 6, y), (x, y + 2)], outline=C[c])
def _ground(d, x, y, c): d.line((x - 6, y + 3, x + 6, y + 3), fill=C[c]); d.polygon([(x - 3, y + 2), (x + 3, y + 2), (x, y - 4)], fill=C[c])
def _glamour(d, x, y, c):
    for a, b in (((0, -5), (0, 5)), ((-5, 0), (5, 0)), ((-3, -3), (3, 3)), ((-3, 3), (3, -3))):
        d.line((x + a[0], y + a[1], x + b[0], y + b[1]), fill=C[c])


def u_weekone():
    """weekone -- Four days, each holding two words: four stems on one ground, each with its virtue in gold above and
    its shadow in green below like a root -- CIRCLE over THRALL, MEASURE over DEVOURING, OFFERING over BINDING, VIGIL
    over SLUMBER, drawn as their signs."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((0, 58, PW - 1, PH - 1), fill=C["C_EDGE_DARK"])
    d.line((0, 58, PW - 1, 58), fill=C["C_CHALK_FAINT"])
    for k, (top, low) in enumerate(((_ring, _chain), (_cup, _mouth), (_bowl, _knot), (_eye, _shut))):
        _day(im, 15 + k * 22, top, low)
    return im


def u_weektwo():
    """weektwo -- Three days, each holding two words: UNCROSSING over HEX, BLESSING over EVIL EYE, GROUNDING over
    GLAMOUR -- and a fourth place on the ground left open, where the week turns over."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((0, 58, PW - 1, PH - 1), fill=C["C_EDGE_DARK"])
    d.line((0, 58, PW - 1, 58), fill=C["C_CHALK_FAINT"])
    for k, (top, low) in enumerate(((_uncross, _hex), (_bless, _evil), (_ground, _glamour))):
        _day(im, 18 + k * 30, top, low)
    return im


def u_twobooks():
    """twobooks -- Two careful books, side by side: two books standing on one shelf, never torn, and above them two open
    eyes whose sight lines meet beyond the page -- depth, with both."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((6, 72, 90, 76), fill=C["C_FAINT"])
    d.rectangle((22, 34, 44, 72), fill=C["C_EDGE"], outline=C["C_INK"])
    d.rectangle((52, 34, 74, 72), fill=C["C_HIGHLIGHT"], outline=C["C_INK"])
    d.line((24, 36, 24, 70), fill=C["C_RING"]); d.line((54, 36, 54, 70), fill=C["C_RULE"])
    tri(d, 33, 50, 4, True, "C_MARGIN")
    d.ellipse((60, 46, 68, 54), outline=C["C_RULE"])
    for x, c in ((33, "C_RING"), (63, "C_RULE")):
        d.chord((x - 7, 8, x + 7, 18), 180, 360, fill=C["C_INK"]); d.chord((x - 7, 8, x + 7, 18), 0, 180, fill=C["C_INK"])
        d.ellipse((x - 2, 11, x + 2, 15), fill=C[c])
        d.line((x, 18, 48, 30), fill=C[c])
    px(im, 48, 31, "C_INK")
    return im


def u_fractal():
    """fractal -- In, read, out, back; back, out, read, in: two loops on the same four stations -- the night's going
    one way in emerald, the dawn's the other way in gold, inside it."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, PH, seed=75)
    cx, cy = 48, 44
    for k in range(4):
        arc_arrow(im, cx, cy, 32, k * 90 + 18, k * 90 + 72, "C_RING")
        arc_arrow(im, cx, cy, 22, k * 90 + 72, k * 90 + 18, "C_RULE")
    for k in range(4):
        a = math.radians(k * 90)
        x, y = cx + 27 * math.cos(a), cy + 27 * math.sin(a)
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=C["C_EDGE_DARK"], outline=C["C_INK"])
        px(im, x, y, "C_MARGIN" if k % 2 else "C_RULE")
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), outline=C["C_CHALK_FAINT"])
    return im


def u_twoflowers():
    """twoflowers -- A silk flower and a wild one: the night's window and its vase on the left, the flower dry inside;
    on the right the open hill and the wild flower in its rain and sun -- the crease between."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((2, 6, 44, 54), fill=C["C_EDGE_DARK"], outline=C["C_FAINT"])
    r = random.Random(77)
    for _ in range(14):
        x, y = r.randrange(4, 42), r.randrange(8, 48)
        d.line((x, y, x - 1, y + 4), fill=C["C_EDGE"])
    d.rectangle((0, 56, 47, PH - 1), fill=C["C_EDGE"])
    d.polygon([(18, 56), (28, 56), (26, 46), (20, 46)], fill=C["C_HIGHLIGHT"], outline=C["C_FAINT"])
    flower(im, 23, 46, 22, petal="C_INK", heart="C_RULE", stem="C_RING")
    bands(im, (49, 0, PW, 60), ["C_HIGHLIGHT", "C_FAINT", "C_RULE"])
    sun(im, 84, 60, 6, fill="C_RULE", rays="C_CHALK_FAINT", n=5)
    for k in range(5):
        d.line((56 + k * 3, 10 + k % 2 * 3, 55 + k * 3, 14 + k % 2 * 3), fill=C["C_CHALK"])
    d.rectangle((49, 60, PW - 1, PH - 1), fill=C["C_EDGE_DARK"])
    d.line((49, 60, PW - 1, 60), fill=C["C_RING"])
    flower(im, 70, 60, 28, petal="C_INK", heart="C_RULE", stem="C_RING", wild=True, seed=9)
    for x1, y1 in ((64, 74), (70, 80), (76, 72)):
        d.line((70, 61, x1, y1), fill=C["C_EDGE"])
    crease(im)
    return im


def u_entangled():
    """entangled -- Two states, one description: one daemon inside the map's edge and one outside it, a thread between
    them half emerald and half gold, running straight through the border."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    stars(im, (2, 2, 94, 86), 79, 14, ("C_FAINT", "C_EDGE", "C_INK"))
    d.rectangle((6, 10, 58, 80), fill=C["C_EDGE_DARK"], outline=C["C_CHALK_FAINT"])
    for k in range(5):
        d.line((10, 20 + k * 12, 54, 18 + k * 12), fill=C["C_EDGE"])
    d.line((30, 12, 34, 78), fill=C["C_EDGE"])
    daemon(im, 18, 46, c="C_INK")
    daemon(im, 74, 28, c="C_INK")
    pts = curve((28, 52), (74, 34), 8)
    d.line(pts[:13], fill=C["C_MARGIN"])
    d.line(pts[12:], fill=C["C_RULE"])
    return im


def u_keeper():
    """keeper -- A little figure, keeping the house: the poppet sits by the hearth with the last cup beside it; the
    window over it half night, half morning."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((52, 8, 86, 38), fill=C["C_EDGE_DARK"], outline=C["C_FAINT"])
    stars(im, (54, 10, 68, 36), 81, 6, ("C_FAINT", "C_EDGE", "C_INK"))
    bands(im, (70, 9, 86, 38), ["C_HIGHLIGHT", "C_FAINT", "C_RULE"])
    d.line((69, 8, 69, 38), fill=C["C_RING"]); d.line((70, 8, 70, 38), fill=C["C_RULE"])
    d.rectangle((4, 20, 40, 70), fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])
    d.rectangle((10, 40, 34, 70), fill=C["C_EDGE_DARK"])
    for x, h, c in ((17, 10, "C_RULE"), (22, 14, "C_MARGIN"), (27, 9, "C_RULE")):
        d.polygon([(x - 3, 70), (x + 3, 70), (x, 70 - h)], fill=C[c])
    d.rectangle((0, 70, PW - 1, PH - 1), fill=C["C_HIGHLIGHT"])
    d.line((0, 70, PW - 1, 70), fill=C["C_FAINT"])
    x, y = 50, 50
    d.ellipse((x + 2, y, x + 12, y + 10), fill=C["C_INK"])
    d.polygon([(x + 3, y + 10), (x + 11, y + 10), (x + 14, y + 22), (x, y + 22)], fill=C["C_INK"])
    d.line((x - 3, y + 14, x + 17, y + 14), fill=C["C_INK"])
    for ex in (5, 9):
        px(im, x + ex, y + 5, "C_EDGE_DARK")
    d.ellipse((x + 6, y + 15, x + 8, y + 17), fill=C["C_RULE"])
    px(im, x + 7, y + 13, "C_MARGIN")
    d.polygon([(70, 64), (78, 64), (77, 72), (71, 72)], fill=C["C_FAINT"])
    d.line((71, 65, 77, 65), fill=C["C_RULE"])
    return im


def u_spelling():
    """spelling -- Arranging letters: two rows of tiles on one board, the upper row cast in emerald, the lower given in
    gold, and one tile between them still in the air, about to be set in both."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((6, 20, 89, 76), fill=C["C_EDGE_DARK"], outline=C["C_FAINT"])
    for k in range(7):
        if k != 3:
            tile(im, 12 + k * 11, 28, c="C_INK", mark="C_EDGE_DARK", seed=k + 21)
            tile(im, 12 + k * 11, 62, c="C_INK", mark="C_EDGE_DARK", seed=k + 31)
    d.line((12, 36, 86, 36), fill=C["C_RING"]); d.line((12, 70, 86, 70), fill=C["C_RULE"])
    d.rectangle((44, 28, 50, 34), outline=C["C_FAINT"]); d.rectangle((44, 62, 50, 68), outline=C["C_FAINT"])
    tile(im, 44, 45, c="C_MARGIN", mark="C_EDGE_DARK", seed=1)
    for k in range(3):
        px(im, 47, 40 + k * 1, "C_RING"); px(im, 47, 54 + k * 2, "C_RULE")
    return im


def u_wheel():
    """wheel -- Twelve on the wheel, one in the crease: the wheel across the mended crease, its night six in emerald and
    its dawn six in gold, the crease sewn, and the thirteenth at the centre half triangle, half sun."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, PH, seed=83)
    dots = ["C_RULE"] * 6 + ["C_MARGIN"] * 6
    wheel(im, 48, 44, 30, "C_FAINT", "C_RING", None, dots=dots)
    for y in range(12, 78, 6):
        d.line((47, y, 49, y + 3), fill=C["C_MARGIN"]); d.line((47, y + 3, 49, y), fill=C["C_RULE"])
    d.polygon([(47, 38), (47, 49), (40, 49)], outline=C["C_MARGIN"])
    d.pieslice((44, 40, 56, 52), 270, 450, fill=C["C_RULE"])
    return im


# ================================================================================ (to come): the first fifteen proposals
def _row_shapes(im, y, c, leaf, night=True):
    """The row the one thread runs through: a daemon, OSRIC HATTER (or the LARK), a route post, a lamp."""
    daemon(im, 8, y - 13, c=c, leaf=leaf)
    if night:
        stoat(im, 28, y - 30, c=c, hat="C_EDGE", band="C_RING")
    else:
        lark(im, 31, y - 8, c=c, singing=False)
    post(im, 62, y, c=c)
    lamp(im, 80, y, c=c, glow="C_MARGIN")


def h_onething():
    """onething (to come) -- One emerald thread through a row of night shapes, each a loop of the same line; a dotted
    box drawn round one of them, the box a game draws round a sprite."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 91, (2, 2, 94, 30), 12)
    d.line((0, 66, PW - 1, 66), fill=C["C_EDGE"])
    _row_shapes(im, 64, "C_FAINT", "C_RING")
    pts = []
    for x in range(0, PW):
        loops = [(13, 56), (35, 48), (62, 54), (83, 52)]
        y = 74
        for lx, ly in loops:
            if abs(x - lx) < 9:
                y = 74 - (74 - ly) * math.cos((x - lx) / 9 * math.pi / 2)
        pts.append((x, y))
    d.line(pts, fill=C["C_RING"])
    for x in range(26, 46, 2):                                                                  # a sprite's box
        px(im, x, 30, "C_INK"); px(im, x, 68, "C_INK")
    for y in range(30, 69, 2):
        px(im, 26, y, "C_INK"); px(im, 45, y, "C_INK")
    return im


def h_prima():
    """prima (to come) -- A boulder on the night hill with faint emerald ripple lines running through it as through
    water: a very slow river, first matter as a process."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 93, (2, 2, 94, 40), 18)
    moon(im, 16, 12, 5, sky="C_PAPER")
    d.pieslice((-20, 62, 116, 140), 180, 360, fill=C["C_EDGE_DARK"])
    d.arc((-20, 62, 116, 140), 210, 300, fill=C["C_RING"])
    boulder(im, 50, 50, 26, 18, fill="C_HIGHLIGHT", edge="C_FAINT", lit="C_INK")
    for k, y in enumerate((44, 50, 56, 62)):
        d.line(wave(28 + k, 72 - k, y, 1.2, 14, k * 1.3), fill=C["C_RING" if k % 2 == 0 else "C_EDGE"])
    return im


def _rope_scene(im, left, right, rope_c, sag, lead=True):
    d = D(im)
    pts = curve((4, 40), (92, 44), sag)
    rope(im, pts, c=rope_c, hi="C_INK")
    return pts


def h_transmute():
    """transmute (to come) -- Two hands on one rope, the rope bending into one curve as they turn it together, no gap
    between them; at the rope's end a dull lump of lead with one green glint."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 95, (2, 2, 94, 20), 8)
    pts = curve((2, 50), (76, 56), -22)
    rope(im, pts, c="C_FAINT", hi="C_INK")
    for i, c, w in ((10, "C_INK", (-0.3, 1)), (13, "C_FAINT", (0.3, 1))):
        hand_grip(im, int(pts[i][0]), int(pts[i][1]), c=c, line="C_EDGE_DARK", wrist=w)
    d.line((0, 82, PW - 1, 82), fill=C["C_EDGE"])
    d.chord((72, 52, 92, 70), 160, 380, fill=C["C_EDGE"], outline=C["C_HIGHLIGHT"])
    px(im, 85, 57, "C_MARGIN"); px(im, 84, 57, "C_RING")
    return im


def h_surface():
    """surface (to come) -- A still pool at night: the crescent and a star on its skin, a flat friendly cloud-figure
    drawn on the surface, and under it, faint, the tablet's shape."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 97, (2, 2, 94, 28), 12)
    moon(im, 70, 12, 5, sky="C_PAPER")
    d.ellipse((4, 34, 92, 86), fill=C["C_EDGE_DARK"], outline=C["C_FAINT"])
    tablet(im, 38, 50, 58, 84, face="C_EDGE", edge="C_HIGHLIGHT", lit="C_HIGHLIGHT", lines=False, glyphs=False)
    moon(im, 70, 56, 4, c="C_FAINT", sky="C_EDGE_DARK")
    px(im, 24, 50, "C_INK")
    cloud_figure(im, 18, 58, c="C_INK", eye="C_EDGE_DARK")
    d.arc((4, 34, 92, 86), 200, 250, fill=C["C_RING"])
    return im


def h_space():
    """space (to come) -- The sheet stood in three pleats, a here-mark at one end and a there-mark at the other, nobody
    between them; above it an empty stave, a song with no one to hum it."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    nsky(im, 99, (2, 2, 94, 14), 8)
    stave(im, 14, 82, 16)
    sheet_pleat(im, 18, 40, 3, 20, 34, a="C_INK", b="C_FAINT", lean=8)
    d.line((8, 82, 88, 82), fill=C["C_EDGE"])
    d.ellipse((6, 74, 14, 80), outline=C["C_RING"]); px(im, 10, 77, "C_MARGIN")             # here
    tri(d, 86, 76, 4, True, "C_RING")                                                       # there
    return im


def e_portions():
    """portions (to come) -- The same thread read from the other side: one sunrise cut into shares, each shape -- a
    daemon, the lark, a route post, a lamp -- holding a slice of the same light; nobody left out."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 66)
    cx, cy = 48, 66
    for k in range(4):
        a0, a1 = 180 + k * 45, 180 + (k + 1) * 45
        d.pieslice((cx - 56, cy - 56, cx + 56, cy + 56), a0 + 2, a1 - 2, fill=C["C_RULE" if k % 2 else "C_MARGIN"])
    d.pieslice((cx - 12, cy - 12, cx + 12, cy + 12), 180, 360, fill=C["C_INK"])
    ground(im, 66, line="C_RING")
    _row_shapes(im, 82, "C_INK", "C_RING", night=False)
    return im


def e_firstlight():
    """firstlight (to come) -- The night half's boulder at dawn, gold seams of sunrise glowing from inside it: a very
    patient sunrise."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 66)
    d.pieslice((-20, 62, 116, 140), 180, 360, fill=C["C_EDGE_DARK"])
    d.arc((-20, 62, 116, 140), 240, 330, fill=C["C_RING"])
    boulder(im, 50, 50, 26, 18, fill="C_EDGE", edge="C_HIGHLIGHT", lit="C_FAINT")
    for k, y in enumerate((44, 50, 56, 62)):
        d.line(wave(28 + k, 72 - k, y, 1.2, 14, k * 1.3), fill=C["C_RULE" if k % 2 == 0 else "C_MARGIN"])
    sun(im, 50, 48, 4, fill="C_MARGIN", rays="C_RULE", n=0)
    return im


def e_letbe():
    """letbe (to come) -- The two hands on the one rope, opening together, the rope still curved and holding by itself
    between them."""
    im = blank(PW, PH, "C_PAPER")
    dsky(im, 88)
    pts = curve((6, 30), (90, 30), 16)
    rope(im, pts, c="C_INK", hi="C_MARGIN")
    paste_key(im, hand_img(0.62, "C_INK", "C_EDGE"), 16, 54)
    paste_key(im, hand_img(0.62, "C_INK", "C_EDGE", flipx=True), 58, 54)
    for x in (28, 70):                                                                       # the gap, let be
        px(im, x, 48, "C_RULE")
    return im


def e_depth():
    """depth (to come) -- A doorway into a lit room at first light: the flat cloud-figure painted on the near wall, the
    room's depth glowing behind it -- go in."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    d.rectangle((0, 0, PW - 1, PH - 1), fill=C["C_EDGE"])
    d.polygon([(52, 14), (84, 6), (84, 84), (52, 74)], fill=C["C_RULE"])                     # the room, deep
    d.polygon([(60, 24), (78, 20), (78, 68), (60, 64)], fill=C["C_MARGIN"])
    d.rectangle((52, 14, 56, 74), fill=C["C_EDGE_DARK"])
    d.polygon([(52, 74), (84, 84), (60, 87), (40, 87)], fill=C["C_HIGHLIGHT"])
    cloud_figure(im, 14, 34, c="C_FAINT", eye="C_EDGE_DARK")
    d.rectangle((10, 30, 38, 54), outline=C["C_HIGHLIGHT"])
    critter(im, 44, 62, c="C_INK", s=1.0)
    return im


def e_space():
    """space (to come) -- The pleated sheet stood open, a swept floor between here and there and one chair pulled out;
    the stave above waiting for whoever will hum it."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    dsky(im, 60)
    stave(im, 14, 82, 10, c="C_INK")
    note(im, 20, 16, "C_MARGIN")
    sheet_pleat(im, 12, 30, 3, 24, 34, a="C_INK", b="C_FAINT", lean=8, opening=0.7)
    d.rectangle((0, 70, PW - 1, PH - 1), fill=C["C_HIGHLIGHT"])
    d.line((0, 70, PW - 1, 70), fill=C["C_RING"])
    for k in range(5):
        d.line((20 + k * 12, 76 + k % 2 * 4, 26 + k * 12, 76 + k % 2 * 4), fill=C["C_FAINT"])
    chair(im, 50, 84, c="C_INK", dr=1)
    d.ellipse((6, 76, 14, 82), outline=C["C_RING"])
    tri(d, 86, 78, 4, True, "C_RULE")
    return im


def u_onething():
    """onething (to come) -- One thread that is both running (emerald) and given out (gold), looping through the same row
    of shapes, half each, one line."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, 66, seed=101)
    ground(im, 66, line="C_CHALK")
    daemon(im, 8, 51, c="C_INK")
    stoat(im, 28, 34, c="C_INK", hat="C_EDGE", band="C_RING")
    post(im, 62, 64, c="C_INK")
    lamp(im, 80, 64, c="C_INK", glow="C_RULE")
    pts = []
    for x in range(0, PW):
        y = 74
        for lx, ly in ((13, 56), (35, 48), (62, 54), (83, 52)):
            if abs(x - lx) < 9:
                y = 74 - (74 - ly) * math.cos((x - lx) / 9 * math.pi / 2)
        pts.append((x, y))
    d.line(pts, fill=C["C_MARGIN"])
    d.line([(x, y + 1) for x, y in pts], fill=C["C_RULE"])
    crease(im, y1=66)
    return im


def u_light():
    """light (to come) -- One boulder split down a seam: the night side with river lines through it, the dawn side
    glowing with a patient sunrise."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, 64, seed=103)
    d.pieslice((-20, 62, 116, 140), 180, 360, fill=C["C_EDGE_DARK"])
    boulder(im, 48, 50, 28, 18, fill="C_EDGE", edge="C_FAINT")
    for k, y in enumerate((44, 50, 56, 62)):
        d.line(wave(24 + k, 46, y, 1.2, 12, k), fill=C["C_RING"])
        d.line(wave(51, 72 - k, y, 1.2, 12, k), fill=C["C_RULE" if k % 2 == 0 else "C_MARGIN"])
    d.line((48, 32, 47, 44), fill=C["C_INK"]); d.line((47, 44, 49, 56), fill=C["C_INK"]); d.line((49, 56, 48, 68), fill=C["C_INK"])
    return im


def u_is():
    """is (to come) -- The two hands on one rope in one picture -- one leaning, one letting go -- and the rope holding
    between them: the same courtesy."""
    im = blank(PW, PH, "C_PAPER")
    usky(im, PH, seed=105)
    pts = curve((4, 30), (92, 34), 14)
    rope(im, pts, c="C_INK", hi="C_CHALK_FAINT")
    hand_grip(im, 24, int(pts[6][1]), c="C_INK", line="C_EDGE", wrist=(-0.6, 1))
    paste_key(im, hand_img(0.6, "C_INK", "C_EDGE", flipx=True), 62, 52)
    crease(im)
    return im


def u_surface():
    """surface (to come) -- One pane of still water seen from both sides at once: the reflection on top, the lit depth
    beneath, a single line between."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    stars(im, (2, 2, 94, 30), 107, 12, ("C_FAINT", "C_EDGE", "C_INK"))
    moon(im, 70, 12, 5, sky="C_PAPER")
    d.rectangle((0, 40, PW - 1, 42), fill=C["C_CHALK"])
    moon(im, 70, 32, 4, c="C_FAINT", sky="C_PAPER")
    cloud_figure(im, 16, 26, c="C_FAINT", eye="C_EDGE_DARK")
    bands(im, (0, 43, PW, PH), ["C_EDGE_DARK", "C_HIGHLIGHT", "C_RULE"])
    tablet(im, 38, 50, 58, 86, face="C_EDGE", edge="C_RING", lit="C_MARGIN", lines=False, glyphs=True)
    return im


def u_space():
    """space (to come) -- The pleated sheet: on the night side its pleats stood and nobody between here and there; on
    the dawn side the same sheet open with one chair pulled out, nobody yet; dusk."""
    im = blank(PW, PH, "C_PAPER")
    d = D(im)
    usky(im, 70, seed=109)
    stave(im, 6, 90, 8, c="C_FAINT")
    x1 = sheet_pleat(im, 6, 32, 3, 13, 32, a="C_INK", b="C_FAINT", lean=7)
    d.polygon([(x1, 32 - 7), (90, 26), (90, 58), (x1, 57)], fill=C["C_INK"])
    d.rectangle((0, 70, PW - 1, PH - 1), fill=C["C_EDGE_DARK"])
    d.line((0, 70, PW - 1, 70), fill=C["C_CHALK"])
    chair(im, 66, 82, c="C_INK")
    d.ellipse((4, 74, 11, 80), outline=C["C_RING"])
    tri(d, 88, 78, 4, True, "C_RULE")
    crease(im)
    return im


# ==================================================================== hands redrawn for the approval (T-519, 2026-11-06)
SMALL_HAND = (                    # a small hand, palm on, fingers up, thumb out on the left: 14 x 20 before its wrist
    "......##......",             # '#' the hand, '+' its line, '.' nothing
    "......##.##...",
    "...##.##.##...",
    "...##.##.##...",
    "...##.##.##.##",
    "...##.##.##.##",
    "...##.##.##.##",
    "...##.##.##.##",
    "...##+##+##+##",
    "##.###########",
    "##.###########",
    ".##.##########",
    "..############",
    "..+###########",
    "...###++++####",
    "...###########",
    "....##########",
    ".....########.",
    ".....#######..",
)


def small_hand(im, x, y, c="C_INK", line="C_EDGE_DARK", wrist=4, mirror=False):
    """SMALL_HAND at (X, Y), its middle fingertip at (X + 6.5, Y); WRIST pixels of wrist below it."""
    rows = list(SMALL_HAND) + [".....#######.."] * wrist
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row[::-1] if mirror else row):
            if ch != ".":
                px(im, x + xx, y + yy, c if ch == "#" else line)


def hand_curl(im, x, y, c="C_INK", line="C_EDGE_DARK", s=1, curl=0.5):
    """hand()'s open hand with its fingers curled CURL of the way to the fist (0 open, 1 closed): one hand, the
    fingers shortened as they bend toward the palm, the bent tips' fold drawn across each, the thumb coming in."""
    d = ImageDraw.Draw(im)
    X = lambda v: x + v * s
    Y = lambda v: y + v * s

    def box(a, b, cc, e, r):
        d.rounded_rectangle((X(a), Y(b), X(cc), Y(e)), radius=r * s, fill=C[c])
    box(5, 20, 25, 40, 5)                                    # the palm
    for fx, top in ((6, 6), (11, 1), (16, 0), (21, 5)):
        t = top + (14 - top) * curl
        box(fx, t, fx + 4, 24, 2)
        d.line((X(fx + 0.5), Y(t + 3), X(fx + 3.5), Y(t + 3)), fill=C[line])     # the fold where the tip bends in
        d.line((X(fx + 4), Y(t + 5), X(fx + 4), Y(22)), fill=C[line])
    op = [(5, 30), (-2, 18), (1, 15), (8, 24)]
    cl = [(5, 28), (0, 22), (2, 18), (9, 26)]
    d.polygon([(X(a + (p - a) * curl), Y(b + (q - b) * curl)) for (a, b), (p, q) in zip(op, cl)], fill=C[c])
    d.arc((X(9), Y(26), X(22), Y(38)), 200, 340, fill=C[line])
    d.line((X(8), Y(32), X(14), Y(35)), fill=C[line])


def great_hand_down(im, c="C_FAINT", line="C_EDGE", tips=((18, 54), (38, 58), (58, 58), (78, 54))):
    """The great hand reaching down from above the frame, palm on, its four fingers spread to TIPS, its thumb out."""
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((26, -12, 70, 28), radius=9, fill=C[c])                       # the palm, the wrist above
    for (kx, ky), (tx, ty) in zip(((32, 24), (43, 27), (53, 27), (64, 24)), tips):
        d.line((kx, ky, tx, ty - 3), fill=C[c], width=7)
        d.ellipse((tx - 3, ty - 6, tx + 3, ty), fill=C[c])
        mx, my = (kx + 2 * tx) / 3, (ky + 2 * (ty - 3)) / 3                           # the last knuckle
        d.line((mx - 2, my, mx + 2, my), fill=C[line])
    d.line((68, 6, 84, 22), fill=C[c], width=7)                                       # the thumb
    d.ellipse((81, 19, 88, 26), fill=C[c])
    d.arc((36, 10, 60, 22), 30, 150, fill=C[line])                                     # the palm's line
    d.line((70, 10, 76, 16), fill=C[line])


def hand_letgo(im, x, y, c="C_INK", line="C_EDGE", skin_dark="C_FAINT"):
    """A hand seen from the side, palm down, coming in from the left: the back of the hand on top, its knuckles, and
    the fingers opening downward, apart, as a hand does that has just let go; the thumb dropped below. About 50 x 32."""
    d = ImageDraw.Draw(im)
    X = lambda v: x + v
    Y = lambda v: y + v
    d.polygon([(X(-24), Y(5)), (X(10), Y(3)), (X(12), Y(13)), (X(-24), Y(13))], fill=C[c])     # the wrist
    d.line((X(-24), Y(13), X(11), Y(13)), fill=C[line])
    d.polygon([(X(8), Y(2)), (X(24), Y(0)), (X(36), Y(4)), (X(40), Y(12)), (X(26), Y(18)), (X(10), Y(15))],
              fill=C[c])                                                                    # the back of the hand
    for kx, ky in ((29, 2), (34, 4), (37, 7)):                                               # its knuckles
        px(im, X(kx), Y(ky), line)
    fingers = (((37, 7), (47, 7), (55, 10)),                 # the little finger, farthest, nearly level
               ((38, 10), (47, 13), (53, 18)),
               ((37, 13), (44, 19), (48, 26)),
               ((34, 15), (38, 23), (39, 31)))                # the forefinger, nearest, opened most
    for a, b, e in fingers:                                   # far to near: each nearer one outlined over the last
        for w, col in ((6, line), (4, c)):
            d.line((X(a[0]), Y(a[1]), X(b[0]), Y(b[1])), fill=C[col], width=w)
            d.line((X(b[0]), Y(b[1]), X(e[0]), Y(e[1])), fill=C[col], width=w - 1)
            r = (w - 1) / 2
            d.ellipse((X(e[0]) - r, Y(e[1]) - r, X(e[0]) + r, Y(e[1]) + r), fill=C[col])
        px(im, X(b[0]), Y(b[1]), skin_dark)                                                  # the middle joint
    for w, col in ((6, line), (4, c)):                                                       # the thumb, dropped
        d.line((X(18), Y(14), X(24), Y(22)), fill=C[col], width=w)
        d.line((X(24), Y(22), X(27), Y(27)), fill=C[col], width=w - 1)
    d.polygon([(X(10), Y(6)), (X(30), Y(4)), (X(30), Y(14)), (X(12), Y(14))], fill=C[c])    # the hand over its own roots


# ==================================================================== the drafts, and their limits
COVERS = {
    "hermetic": [("A", "the tablet at night", h_cover_a, None), ("B", "the hatter's sky", h_cover_b, None)],
    "eudaimon": [("A", "the singing fir, current palette", e_cover_a, None),
                 ("B", "the singing fir, sapphire boards", e_cover_b, SAPPHIRE)],
    "unity":    [("A", "sewn spine, one horizon", u_cover_a, None), ("B", "both covers, opened flat", u_cover_b, None),
                 ("C", "the balance", u_cover_c, None)],
}
ICONS = {"hermetic": h_icon, "eudaimon": e_icon, "unity": u_icon}
PICTURES = {
    "hermetic": [("frontis", "the one picture shown today", h_frontis), ("warning", "", h_warning),
                 ("chalk", "", h_chalk), ("emerald", "", h_emerald), ("hands", "", h_hands), ("palm", "", h_palm),
                 ("mirrors", "", h_mirrors),
                 ("nigredo", "", h_nigredo),
                 ("rubedo", "", h_rubedo),
                 ("folds", "", h_folds),
                 ("blank", "", h_blank),
                 ("signal", "", h_signal),
                 ("sound", "", h_sound),
                 ("abstract", "", h_abstract),
                 ("protofeel", "", h_protofeel),
                 ("noun", "", h_noun),
                 ("upperfolds", "", h_upperfolds),
                 ("gravity", "", h_gravity),
                 ("apple", "", h_apple),
                 ("fractal", "", h_fractal),
                 ("silkflower", "", h_silkflower),
                 ("entangled", "", h_entangled),
                 ("poppet", "", h_poppet),
                 ("spelling", "", h_spelling),
                 ("wheel", "", h_wheel),
                 ("onething", "", h_onething),
                 ("prima", "", h_prima),
                 ("transmute", "", h_transmute),
                 ("surface", "", h_surface),
                 ("space", "", h_space)],
    "eudaimon": [("frontis", "the one picture shown today", e_frontis), ("blessing", "", e_blessing),
                 ("chalkfaint", "", e_chalkfaint), ("emeraldback", "", e_emeraldback), ("palmup", "", e_palmup),
                 ("fingers", "", e_fingers),
                 ("windows", "", e_windows),
                 ("rubedo", "", e_rubedo),
                 ("nigredo", "", e_nigredo),
                 ("opening", "", e_opening),
                 ("blankback", "", e_blankback),
                 ("rooms", "", e_rooms),
                 ("song", "", e_song),
                 ("setdown", "", e_setdown),
                 ("lastwarmth", "", e_lastwarmth),
                 ("river", "", e_river),
                 ("upperopen", "", e_upperopen),
                 ("appleup", "", e_appleup),
                 ("earth", "", e_earth),
                 ("fractalheard", "", e_fractalheard),
                 ("wildflower", "", e_wildflower),
                 ("belonging", "", e_belonging),
                 ("goodspirit", "", e_goodspirit),
                 ("goodspell", "", e_goodspell),
                 ("wheel", "", e_wheel),
                 ("portions", "", e_portions),
                 ("firstlight", "", e_firstlight),
                 ("letbe", "", e_letbe),
                 ("depth", "", e_depth),
                 ("space", "", e_space)],
    "unity":    [("frontis", "the one picture shown today", u_frontis), ("attestation", "", u_attestation),
                 ("chalkboth", "", u_chalkboth), ("emeraldwhole", "", u_emeraldwhole), ("wholehand", "", u_wholehand),
                 ("handturning", "", u_handturning),
                 ("glass", "", u_glass),
                 ("stone", "", u_stone),
                 ("sheet", "", u_sheet),
                 ("horizon", "", u_horizon_pic),
                 ("blankboth", "", u_blankboth),
                 ("signal", "", u_signal),
                 ("sound", "", u_sound),
                 ("remains", "", u_remains),
                 ("warmth", "", u_warmth),
                 ("everyfold", "", u_everyfold),
                 ("gravity", "", u_gravity),
                 ("twomirrors", "", u_twomirrors),
                 ("pair", "", u_pair),
                 ("twosides", "", u_twosides),
                 ("weekone", "", u_weekone),
                 ("weektwo", "", u_weektwo),
                 ("twobooks", "", u_twobooks),
                 ("fractal", "", u_fractal),
                 ("twoflowers", "", u_twoflowers),
                 ("entangled", "", u_entangled),
                 ("keeper", "", u_keeper),
                 ("spelling", "", u_spelling),
                 ("wheel", "", u_wheel),
                 ("onething", "", u_onething),
                 ("light", "", u_light),
                 ("is", "", u_is),
                 ("surface", "", u_surface),
                 ("space", "", u_space)],
}


def limits(ind):
    """(tiles, unique tiles, colours used, roles used) of an indexed image."""
    w, h = ind.size
    data = ind.load()
    seen = set()
    for ty in range(0, h, 8):
        for tx in range(0, w, 8):
            seen.add(tuple(data[tx + x, ty + y] for y in range(8) for x in range(8)))
    used = sorted(set(ind.getdata()))
    return (w // 8) * (h // 8), len(seen), len(used), [gs.PALETTE[i][0] for i in used]


def quantize(src, w, h, roles):
    """A spriteforge draft (8px grid) sampled down to its grid and mapped to the nearest of ROLES."""
    im = Image.open(src).convert("RGB")
    im = im.resize((im.width // 8, im.height // 8), Image.NEAREST)
    pal = [(n, C[n]) for n in roles]
    out = Image.new("RGB", im.size)
    for y in range(im.height):
        for x in range(im.width):
            r, g_, b = im.getpixel((x, y))
            n = min(pal, key=lambda p: (p[1][0] - r) ** 2 * 3 + (p[1][1] - g_) ** 2 * 4 + (p[1][2] - b) ** 2 * 2)
            out.putpixel((x, y), n[1])
    return out


def forge_cover(book, src):
    """Option F: a ComfyUI plate (64x64 after its 8px grid), quantized into the book's roles, on the book's boards."""
    im = blank(240, 160, "C_COVER")
    d = boards(im, 48, 188)
    title(im, book, 119)
    d.rectangle((58, 8, 182, 148), outline=C["C_RULE"])
    roles = ["C_PAPER", "C_INK", "C_FAINT", "C_RULE", "C_MARGIN", "C_EDGE", "C_EDGE_DARK", "C_HIGHLIGHT", "C_RING",
             "C_SLATE", "C_CHALK", "C_CHALK_FAINT"]
    plate = quantize(src, 64, 64, roles).resize((64, 64), Image.NEAREST)
    im.paste(plate, (88, 56))
    d.rectangle((86, 54, 153, 121), outline=C["C_RULE"])
    if book == "hermetic":
        torn_edge(im, 48, 4, 152, -1, 7)
    elif book == "eudaimon":
        torn_edge(im, 188, 4, 152, 1, 13)
    else:
        stitched_spine(im, 48, 4, 152)
    return im


def main():
    rows = []           # (book, kind, key, label, [indexed frames], placeholder RGB, limits)
    for book in ("hermetic", "eudaimon", "unity"):
        gfx = os.path.join(ENGINE, "graphics/book", gs.BOOKS[book]["gfx"])
        ph_cover = Image.open(os.path.join(gfx, "cover.png")).convert("RGB")
        ph_pic = Image.open(os.path.join(gfx, "placeholder_0.png" if os.path.exists(os.path.join(gfx, "placeholder_0.png"))
                                         else "frontis_0.png")).convert("RGB")     # what the book shows now
        ph_icon = Image.open(os.path.join(ENGINE, "graphics/items/icons/%s.png" % gs.BOOKS[book]["icon"])).convert("RGB")
        for key, label, fn, tweak in COVERS[book]:
            use(book, tweak)
            ind = gs.indexed(fn(), 240, 160, fill="C_COVER")
            rows.append((book, "cover", key, label, [ind], ph_cover, limits(ind), tweak))
        if FORGE:
            tw = SAPPHIRE if book == "eudaimon" else None      # the forged morning is blue: it needs the sapphire roles
            use(book, tw)
            for src in sorted(glob.glob(os.path.join(FORGE, "%s_*.png" % {"hermetic": "night", "eudaimon": "dawn",
                                                                             "unity": "unity"}[book]))):
                seed = os.path.basename(src).split("_")[1].split(".")[0]
                ind = gs.indexed(forge_cover(book, src), 240, 160, fill="C_COVER")
                rows.append((book, "cover", "F" + seed[-1], "ComfyUI plate, seed " + seed, [ind], ph_cover, limits(ind), tw))
        use(book)
        ind = gs.indexed(ICONS[book](), 24, 24, fill="C_NONE")
        rows.append((book, "icon", "icon", "the bag's icon", [ind], ph_icon, limits(ind), None))
        for key, label, fn in PICTURES[book]:
            use(book)
            frames = fn()
            frames = frames if isinstance(frames, list) else [frames]
            inds = [gs.indexed(f, PW, PH) for f in frames]
            rows.append((book, "picture", key, label, inds, ph_pic, limits(inds[0]), None))
        if book == "eudaimon":
            use(book, SAPPHIRE)
            ind = gs.indexed(e_frontis(True), PW, PH)
            rows.append((book, "picture", "frontis-B", "with the sapphire roles", [ind], ph_pic, limits(ind), SAPPHIRE))
    for book, kind, key, label, inds, _, (t, u, n, roles), tweak in rows:
        print("%-9s %-7s %-12s %3d tiles (%3d unique), %2d of 16 colours%s%s" % (
            book, kind, key, t, u, n, ", %d frames" % len(inds) if len(inds) > 1 else "",
            "  [sapphire roles]" if tweak else ""))
    if not OUT:
        return
    os.makedirs(OUT, exist_ok=True)
    for book, kind, key, label, inds, _, lim, tweak in rows:
        for f, ind in enumerate(inds):
            name = "%s_%s_%s%s.png" % (book, kind, key, "" if len(inds) == 1 else "_%d" % f)
            ind.save(os.path.join(OUT, name))
    sheet(rows, os.path.join(OUT, "t519_book_art_drafts.png"))
    json.dump([{"book": b, "kind": k, "key": key, "label": l, "tiles": lim[0], "unique_tiles": lim[1], "colours": lim[2],
                "roles": lim[3], "frames": len(i), "palette_tweak": bool(tw)} for b, k, key, l, i, _, lim, tw in rows],
              open(os.path.join(OUT, "limits.json"), "w"), indent=1)
    print("wrote %d drafts and the sheet into %s" % (sum(len(r[4]) for r in rows), OUT))


def sheet(rows, path):
    from PIL import ImageFont
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
        big = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 18)
    except OSError:
        font = big = ImageFont.load_default()
    BG, FG, DIM = (28, 28, 30), (230, 230, 230), (150, 150, 155)
    blocks = []
    for book in ("hermetic", "eudaimon", "unity"):
        rs = [r for r in rows if r[0] == book]
        covers = [r for r in rs if r[1] == "cover"]
        others = [r for r in rs if r[1] != "cover"]
        cw, chh = 480, 320
        per = 3
        h = 60 + (chh + 52) * (1 + (len(covers) + per - 1) // per)
        pics_h = 230 * ((len(others) + 5) // 6)
        im = Image.new("RGB", (40 + (cw + 20) * (per + 1), h + pics_h + 20), BG)
        d = ImageDraw.Draw(im)
        d.text((20, 10), "%s  (DRAFT, T-519)" % gs.BOOKS[book]["title"], fill=FG, font=big)
        y = 60
        d.text((20, y), "placeholder (now)", fill=DIM, font=font)
        im.paste(covers[0][5].resize((cw, chh), Image.NEAREST), (20, y + 18))
        for k, r in enumerate(covers):
            x = 20 + (cw + 20) * (1 + k % per)
            yy = y + (chh + 52) * (k // per)
            t, u, n, _ = r[6]
            d.text((x, yy - 16), "%s: %s" % (r[2], r[3]), fill=FG, font=font)
            d.text((x, yy), "%d tiles (%d unique), %d/16 colours%s" % (
                t, u, n, ", 2 cover roles recoloured" if r[7] else ""), fill=DIM, font=font)
            im.paste(r[4][0].convert("RGB").resize((cw, chh), Image.NEAREST), (x, yy + 18))
        y = 60 + (chh + 52) * ((len(covers) + per - 1) // per) + 10
        d.text((20, y), "pictures (96x88) and icon (24x24) at 2x; the first of each pair is today's placeholder", fill=DIM, font=font)
        y += 22
        x = 20
        ph_pic = others[1][5] if len(others) > 1 else None
        col = 0
        for r in others:
            frames = r[4]
            scale = 4 if r[1] == "icon" else 2
            w = r[4][0].width * scale
            item_w = (w + 6) * (1 + len(frames)) + 10
            if x + item_w > im.width - 20:
                x, y = 20, y + 230
            t, u, n, _ = r[6]
            d.text((x, y), "%s%s" % (r[2], " (4x)" if r[1] == "icon" else ""), fill=FG, font=font)
            d.text((x, y + 15), "%d tiles, %d/16 col%s" % (t, n, ", %d fr" % len(frames) if len(frames) > 1 else ""),
                   fill=DIM, font=font)
            im.paste(r[5].resize((r[5].width * scale, r[5].height * scale), Image.NEAREST), (x, y + 34))
            for f, fr in enumerate(frames):
                im.paste(fr.convert("RGB").resize((fr.width * scale, fr.height * scale), Image.NEAREST),
                         (x + (w + 6) * (1 + f), y + 34))
            x += item_w
        blocks.append(im.crop((0, 0, im.width, y + 230)))
    W = max(b.width for b in blocks)
    out = Image.new("RGB", (W, sum(b.height for b in blocks)), BG)
    yy = 0
    for b in blocks:
        out.paste(b, (0, yy))
        yy += b.height
    out.save(path)


if __name__ == "__main__":
    main()

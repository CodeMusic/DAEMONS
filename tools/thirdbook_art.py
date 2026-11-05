#!/usr/bin/env python3
"""T-519: DRAFT art for the third book's three forms -- THE HERMETIC LAYER (the night half), THE EUDAIMON LAYER (the
dawn half) and THE UNITY BOOK (mended) -- to replace the placeholders tools/gensubtle.py writes for them.

    python3 tools/thirdbook_art.py                     # report the limits of every draft, write nothing
    python3 tools/thirdbook_art.py --out DIR           # every draft as the indexed PNG the build would convert, and
                                                       # a contact sheet (each draft at 2x beside its placeholder)
    python3 tools/thirdbook_art.py --out DIR --forge F # also quantize the ComfyUI plates in F (spriteforge drafts)

NOTHING HERE WRITES INTO THE GAME. The drafts are drawn in each book's own sixteen palette roles (gensubtle.use), so
an approved one drops into gensubtle's cover_*/icon_*/pictures() unchanged. The one exception is offered, never
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
                 ("chalk", "", h_chalk), ("emerald", "", h_emerald), ("hands", "", h_hands), ("palm", "", h_palm)],
    "eudaimon": [("frontis", "the one picture shown today", e_frontis), ("blessing", "", e_blessing),
                 ("chalkfaint", "", e_chalkfaint), ("emeraldback", "", e_emeraldback), ("palmup", "", e_palmup),
                 ("fingers", "", e_fingers)],
    "unity":    [("frontis", "the one picture shown today", u_frontis), ("attestation", "", u_attestation),
                 ("chalkboth", "", u_chalkboth), ("emeraldwhole", "", u_emeraldwhole), ("wholehand", "", u_wholehand),
                 ("handturning", "", u_handturning)],
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
        ph_pic = Image.open(os.path.join(gfx, "placeholder_0.png")).convert("RGB")
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

"""T-423: THE SUBTLE LAYER's pictures -- one ink diagram per entry, drawn pixel by pixel at the GBA's own size.

Read by tools/gensubtle.py, which maps each colour to the book's palette role and writes the PNGs the build converts.
The colours are the page's own (hue C, CONTEXT: the user, 2026-10-18); the seven centres and the heart are never
given a hue, because a colour standing beside a feeling is craft rule 1.

Each function returns a list of frames (RGB, the page's paper as background), at most 94 x 94: the left page's
picture box. Ink is the page's near-white; the faint pink and the CONTEXT hue carry the second and third tones.
"""
import math
from PIL import Image, ImageDraw


def gba(r, g, b):
    return tuple((c << 3) | (c >> 2) for c in (r, g, b))


PAPER = gba(7, 4, 6)
INK = gba(30, 28, 29)
FAINT = gba(20, 14, 18)
DIM = gba(12, 8, 11)          # a step above the paper: dither, the solid layer's mortar
HUE = gba(22, 10, 19)         # CONTEXT
HUE_LIGHT = gba(29, 17, 26)
SHADE = gba(4, 2, 4)          # darker than the paper: a shadow


def canvas(w, h):
    im = Image.new("RGB", (w, h), PAPER)
    return im, ImageDraw.Draw(im)


def px(im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height:
        im.putpixel((x, y), c)


def creature(im, x, y, body=INK, eye=PAPER, facing=1):
    """A small figure, nobody in particular and no species: a round head on a rounded body, like a pawn. 14 x 22."""
    d = ImageDraw.Draw(im)
    d.ellipse((x + 3, y, x + 11, y + 8), fill=body)                          # head
    d.polygon([(x + 5, y + 8), (x + 9, y + 8), (x + 13, y + 20), (x + 1, y + 20)], fill=body)
    d.rounded_rectangle((x + 1, y + 16, x + 13, y + 21), radius=2, fill=body)
    px(im, x + (9 if facing > 0 else 5), y + 4, eye)


def dither(im, box, c, step=2, phase=0):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x + y + phase) % (step * 2) == 0 and y % step == 0:
                px(im, x, y, c)


# -------------------------------------------------------------------- THE SEAM
def seam():
    im, d = canvas(94, 84)
    ground = 52
    dither(im, (0, 0, 94, ground), FAINT, step=2)                           # the subtle: unsettled, a dither
    for y in range(4, ground, 9):                                            # a faint lean through it
        for x in range(0, 94):
            if (x // 3 + y) % 11 == 0:
                px(im, x, y + (x // 12) % 2, DIM)
    d.rectangle((0, ground, 93, 83), fill=DIM)                              # the solid: settled, laid in courses
    for row, y in enumerate(range(ground + 1, 84, 6)):
        d.line((0, y + 5, 93, y + 5), fill=PAPER)
        for x in range((row % 2) * 7, 94, 14):
            d.line((x, y, x, y + 4), fill=PAPER)
    d.line((0, ground, 93, ground), fill=HUE_LIGHT)                         # the seam
    d.ellipse((62, ground + 4, 84, ground + 18), fill=FAINT, outline=INK)   # a rock, wholly in the solid
    d.line((66, ground + 8, 72, ground + 6), fill=INK)
    creature(im, 30, ground - 12)                                            # feet in the solid, head in the subtle
    return [im]


# -------------------------------------------------------------------- THREE MOVES (the glyph set's first three)
def glyph_read(im, x, y, c=INK):
    d = ImageDraw.Draw(im)
    d.ellipse((x + 10, y + 4, x + 25, y + 19), outline=c)
    d.line((x, y + 11, x + 13, y + 11), fill=c)                              # an arrow into the circle
    d.polygon([(x + 14, y + 11), (x + 10, y + 8), (x + 10, y + 14)], fill=c)


def glyph_write(im, x, y, c=INK, hue=HUE_LIGHT):
    d = ImageDraw.Draw(im)
    d.ellipse((x, y + 4, x + 15, y + 19), outline=c)
    d.line((x + 15, y + 11, x + 20, y + 11), fill=c)                         # out of the circle, onto a fork
    d.line((x + 20, y + 11, x + 26, y + 5), fill=FAINT)
    d.line((x + 20, y + 11, x + 26, y + 17), fill=hue)
    d.line((x + 20, y + 12, x + 26, y + 18), fill=hue)                       # the branch it leans on, bold


def glyph_link(im, x, y, c=INK, hue=HUE_LIGHT):
    d = ImageDraw.Draw(im)
    d.ellipse((x, y + 4, x + 15, y + 19), outline=c)
    d.ellipse((x + 10, y + 4, x + 25, y + 19), outline=c)
    d.line((x + 12, y + 9, x + 14, y + 13), fill=hue)                        # one lean, only in the overlap
    px(im, x + 13, y + 13, hue)


def moves():
    im, d = canvas(94, 64)
    for k, (fn, label_y) in enumerate([(glyph_read, 0), (glyph_write, 0), (glyph_link, 0)]):
        fn(im, 4 + k * 31, 20)
    for x in (32, 63):
        for y in range(18, 46, 3):
            px(im, x, y, DIM)
    return [im]


# -------------------------------------------------------------------- THE THREE
def gauges():
    im, d = canvas(94, 70)
    # CLOSURE: a ring, whole; beside it, faint, a broken one
    d.ellipse((4, 10, 26, 32), outline=INK)
    d.ellipse((5, 11, 25, 31), outline=INK)
    d.arc((8, 42, 22, 56), 40, 320, fill=FAINT)
    # ATTUNEMENT: a membrane, thin beneath; thick, faint, beside it
    for x in range(34, 60):
        px(im, x, 21, INK)
    for y in range(12, 31, 3):
        px(im, 47, y, HUE_LIGHT)                                             # a lean, passing through the thin one
    d.rectangle((36, 45, 58, 51), fill=FAINT)
    for y in range(37, 45, 3):
        px(im, 47, y, HUE)
    # VOLTAGE: a wave, tall; and low, faint
    import math
    for x in range(66, 91):
        y = int(21 - 9 * math.sin((x - 66) / 25 * 2 * math.pi))
        px(im, x, y, HUE_LIGHT)
        px(im, x, y + 1, HUE_LIGHT)
        y2 = int(49 - 2 * math.sin((x - 66) / 25 * 2 * math.pi))
        px(im, x, y2, FAINT)
    d.line((30, 6, 30, 60), fill=DIM)
    d.line((62, 6, 62, 60), fill=DIM)
    return [im]


# -------------------------------------------------------------------- STEERING: the spoons
def spoon(im, x, y, bent=False, c=INK):
    d = ImageDraw.Draw(im)
    d.ellipse((x, y, x + 8, y + 12), outline=c)                              # the bowl
    d.ellipse((x + 2, y + 2, x + 6, y + 10), fill=FAINT)
    if not bent:
        d.line((x + 4, y + 12, x + 4, y + 38), fill=c)
        d.line((x + 5, y + 12, x + 5, y + 38), fill=c)
    else:
        d.line((x + 4, y + 12, x + 4, y + 22), fill=c)
        d.line((x + 5, y + 12, x + 5, y + 22), fill=c)
        d.line((x + 4, y + 22, x + 12, y + 34), fill=c)
        d.line((x + 5, y + 22, x + 13, y + 34), fill=c)


def spoons():
    im, d = canvas(94, 84)
    d.line((0, 62, 93, 62), fill=DIM)                                        # the floor
    spoon(im, 8, 14)
    spoon(im, 40, 14, bent=True, c=HUE_LIGHT)
    spoon(im, 76, 14)
    for k, x in enumerate(range(2, 20, 5)):                                  # footsteps behind it, going to the bent one
        px(im, x, 79 - (k % 2) * 2, FAINT)
        px(im, x + 1, 79 - (k % 2) * 2, FAINT)
    creature(im, 22, 58, facing=1)                                           # going, not reaching
    return [im]


# -------------------------------------------------------------------- THE WEEK: a staircase that resolves
def stairs(text=None):
    im, d = canvas(94, 84)
    w, h, x0, y0 = 12, 9, 4, 76
    notes = "CDEFGAB"
    for k in range(7):
        x, y = x0 + k * w, y0 - (k + 1) * h
        d.rectangle((x, y, x + w - 1, y0), fill=DIM)
        d.line((x, y, x + w - 1, y), fill=INK)                              # the tread
        d.line((x, y, x, y + h), fill=INK)                                  # the riser
        if text:
            text(im, notes[k], x + 3, y - 3, True, INK if k else HUE_LIGHT, None)
    d.line((x0, y0, x0 + 7 * w, y0), fill=INK)
    # and back to C: an arc from the top step down to the first
    d.arc((x0 + 2, 2, x0 + 7 * w - 2, 70), 185, 345, fill=HUE_LIGHT)
    d.polygon([(x0 + 4, 34), (x0 + 1, 28), (x0 + 8, 29)], fill=HUE_LIGHT)
    return [im]


# -------------------------------------------------------------------- SHADOWS: three frames, light not force
def shadows():
    frames = []
    for f in range(3):
        im, d = canvas(94, 84)
        d.line((0, 70, 93, 70), fill=DIM)
        lx = 30
        if f >= 1:                                                           # the lantern turns; light falls behind
            for k in range(1, 9):
                d.line((lx + 4 + k * 6, 56 - k, lx + 4 + k * 6, 56 + k), fill=DIM)
        d.line((lx, 46, lx, 52), fill=FAINT)
        d.rectangle((lx - 3, 52, lx + 3, 60), outline=INK)
        if f >= 1:
            d.rectangle((lx - 2, 53, lx + 2, 59), fill=HUE_LIGHT)
        creature(im, 46, 49, facing=-1)                                      # the one who looks
        if f == 0:                                                           # a shape behind, unwatched
            creature(im, 66, 49, body=SHADE, eye=SHADE, facing=-1)
        if f == 1:
            creature(im, 66, 49, body=FAINT, eye=PAPER, facing=-1)
        if f == 2:                                                           # it steps forward: a second one, the same shade
            creature(im, 60, 49, body=INK, eye=PAPER, facing=-1)
        frames.append(im)
    return frames



# -------------------------------------------------------------------- the glyph sets (20 x 20 each, ink only)
#  The clairs, the reins, the sun and the moon. No hue on the heart: a colour beside a feeling is craft rule 1.
def g_eye(im, x, y, c=INK):
    d = ImageDraw.Draw(im)
    d.arc((x + 1, y + 4, x + 19, y + 22), 205, 335, fill=c)              # upper lid
    d.arc((x + 1, y - 2, x + 19, y + 16), 25, 155, fill=c)               # lower lid
    d.ellipse((x + 7, y + 7, x + 12, y + 12), fill=c)
    sp_ = px; sp_(im, x + 9, y + 9, PAPER)


def g_ear(im, x, y, c=INK):
    d = ImageDraw.Draw(im)
    d.arc((x + 4, y + 1, x + 17, y + 17), 180, 70, fill=c)
    d.line((x + 13, y + 15, x + 9, y + 19), fill=c)
    d.arc((x + 8, y + 5, x + 14, y + 12), 180, 20, fill=c)
    d.line((x + 11, y + 12, x + 10, y + 14), fill=c)


def g_heart(im, x, y, c=INK):
    pts = ["..XX....XX..", ".X..X..X..X.", "X....XX....X", "X..........X", "X..........X",
           ".X........X.", "..X......X..", "...X....X...", "....X..X....", ".....XX....."]
    for j, row in enumerate(pts):
        for i, ch in enumerate(row):
            if ch == "X":
                px(im, x + 4 + i, y + 5 + j, c)


def g_know(im, x, y, c=INK):
    import math
    for k in range(12):
        a = k / 12 * 2 * math.pi
        px(im, x + 10 + round(8 * math.cos(a)), y + 10 + round(8 * math.sin(a)), c)
    ImageDraw.Draw(im).rectangle((x + 9, y + 9, x + 11, y + 11), fill=c)


def g_hand(im, x, y, c=INK):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x + 5, y + 9, x + 15, y + 19), radius=3, outline=c)   # the palm
    for k, (fx, top) in enumerate([(6, 3), (9, 1), (12, 2), (15, 5)]):         # four fingers
        d.line((x + fx - 1 + (1 if k == 3 else 0), y + top, x + fx - 1 + (1 if k == 3 else 0), y + 9), fill=c)
    d.line((x + 5, y + 13, x + 2, y + 9), fill=c)                             # the thumb
    d.line((x + 3, y + 9, x + 1, y + 7), fill=c)


def g_scent(im, x, y, c=INK):
    import math
    for k, ox in enumerate((5, 10, 15)):
        for yy in range(2, 19):
            px(im, x + ox + round(1.6 * math.sin((yy + k * 3) / 2.6)), y + yy, c if yy % 5 else FAINT)


def g_reins(im, x, y, c=INK):
    d = ImageDraw.Draw(im)
    d.ellipse((x + 1, y + 11, x + 8, y + 18), outline=c)                      # the ring
    d.arc((x + 5, y + 2, x + 25, y + 30), 180, 270, fill=c)                   # the strap, rising to the hand
    d.arc((x + 7, y + 4, x + 25, y + 30), 180, 270, fill=c)
    d.rectangle((x + 14, y + 1, x + 19, y + 5), outline=c)                    # the grip


def g_sun(im, x, y, c=INK):
    d = ImageDraw.Draw(im)
    d.ellipse((x + 6, y + 6, x + 14, y + 14), outline=c)
    for (a, b, cc, dd) in [(10, 0, 10, 3), (10, 17, 10, 20), (0, 10, 3, 10), (17, 10, 20, 10),
                           (3, 3, 5, 5), (15, 15, 17, 17), (3, 17, 5, 15), (15, 5, 17, 3)]:
        d.line((x + a, y + b, x + cc, y + dd), fill=c)


def g_moon(im, x, y, c=INK):
    d = ImageDraw.Draw(im)
    d.ellipse((x + 3, y + 3, x + 17, y + 17), fill=c)
    d.ellipse((x + 7, y + 1, x + 19, y + 14), fill=PAPER)


CLAIR_GLYPHS = [g_eye, g_ear, g_heart, g_know, g_hand, g_scent]


def clairs(text=None):
    im, d = canvas(94, 84)
    import math
    for k, fn in enumerate(CLAIR_GLYPHS):                                     # six, round one quiet centre
        a = -math.pi / 2 + k * math.pi / 3
        fn(im, 37 + round(30 * math.cos(a)), 32 + round(28 * math.sin(a)))
    d.ellipse((44, 39, 50, 45), outline=FAINT)
    return [im]


def pair(f1, f2):
    def draw(text=None):
        im, d = canvas(94, 60)
        f1(im, 18, 20)
        f2(im, 56, 20)
        d.line((47, 14, 47, 46), fill=DIM)
        return [im]
    return draw


def reins(text=None):
    im, d = canvas(94, 84)
    creature(im, 22, 50, facing=1)                                            # the virtue holds the reins
    creature(im, 58, 50, body=FAINT, facing=1)                                # of the shadow, which still walks
    d.line((34, 58, 45, 52), fill=INK)
    d.line((45, 52, 60, 57), fill=INK)
    g_reins(im, 37, 18)
    return [im]


def waking(text=None):
    im, d = canvas(94, 72)
    g_sun(im, 37, 4)
    for k in range(4):                                                        # the day's four checks
        x = 13 + k * 18
        d.rectangle((x, 40, x + 9, 49), outline=INK)
        if k < 2:
            d.line((x + 2, 44, x + 4, 47), fill=HUE_LIGHT)
            d.line((x + 4, 47, x + 8, 41), fill=HUE_LIGHT)
    return [im]


def rest(text=None):
    im, d = canvas(94, 72)
    g_moon(im, 37, 4)
    creature(im, 30, 44, facing=1)                                            # sitting together, asking nothing
    creature(im, 48, 48, body=FAINT, facing=-1)
    return [im]


def glyph_sheet(text=None):
    im, d = canvas(94, 60)
    for k, fn in enumerate(CLAIR_GLYPHS + [g_reins, g_sun, g_moon]):
        fn(im, 2 + (k % 5) * 18, 4 + (k // 5) * 28)
    return [im]


SPRITES = {"seam": seam, "moves": moves, "gauges": gauges, "spoons": spoons, "stairs": stairs, "shadows": shadows, "clairs": clairs, "seeing": pair(g_eye, g_ear),
           "feeling": pair(g_heart, g_know), "touch": pair(g_hand, g_scent), "reins": reins,
           "waking": waking, "rest": rest}



# ==================================================================== batch b1


def open_book(d, x, y, w, h):
    d.polygon([(x, y + 4), (x + w // 2, y), (x + w // 2, y + h), (x, y + h + 4)], outline=INK)
    d.polygon([(x + w, y + 4), (x + w // 2, y), (x + w // 2, y + h), (x + w, y + h + 4)], outline=INK)


def prologue(text=None):
    im, d = canvas(94, 76)
    open_book(d, 14, 14, 66, 40)
    for k in range(5):                                                        # the log's lines
        d.line((19, 23 + k * 7, 43, 20 + k * 7), fill=FAINT)
        if k < 3:
            d.line((51, 20 + k * 7, 75, 23 + k * 7), fill=FAINT)
    d.line((47, 14, 47, 58), fill=HUE_LIGHT)                                  # the ribbon
    d.line((60, 46, 78, 30), fill=INK)                                        # a pen, mid-line
    d.line((61, 47, 79, 31), fill=INK)
    px(im, 59, 48, HUE_LIGHT)
    return [im]


def container(text=None):
    im, d = canvas(94, 84)
    for y in range(0, 26):                                                    # one stream, from above
        px(im, 47, y, HUE_LIGHT if y % 3 else FAINT)
    for (x0, x1, kind) in [(10, 20, "cup"), (40, 54, "jar"), (70, 88, "bowl")]:
        cx = (x0 + x1) // 2
        d.line((47, 26, cx, 44), fill=FAINT)                                  # into three vessels
        if kind == "cup":
            d.rectangle((x0, 50, x1, 70), outline=INK); d.arc((x1 - 3, 54, x1 + 5, 64), 270, 90, fill=INK)
            d.rectangle((x0 + 1, 58, x1 - 1, 69), fill=DIM)
        elif kind == "jar":
            d.rectangle((x0 + 3, 44, x1 - 3, 48), outline=INK); d.rounded_rectangle((x0, 48, x1, 72), radius=4, outline=INK)
            d.rectangle((x0 + 1, 58, x1 - 1, 71), fill=DIM)
        else:
            d.chord((x0, 46, x1, 74), 0, 180, outline=INK); d.chord((x0 + 1, 52, x1 - 1, 73), 0, 180, fill=DIM)
            d.line((x0, 60, x1, 60), fill=INK)
    d.line((0, 76, 93, 76), fill=DIM)
    return [im]


def twothings(text=None):
    im, d = canvas(94, 76)
    d.rectangle((8, 28, 36, 62), outline=INK)                                 # the ledger
    for k in range(5):
        d.line((12, 33 + k * 6, 31, 33 + k * 6), fill=FAINT)
        d.line((12, 33 + k * 6, 14, 35 + k * 6), fill=INK)
    creature(im, 58, 44)
    pts = [(48 + k * 3, 24 + (7 if k % 2 else 0) + (k % 3)) for k in range(12)]  # noise, over its head
    d.line(pts, fill=FAINT)
    d.line([(x + 1, y - 6) for x, y in pts], fill=DIM)
    return [im]


def bubble_round(d, x, y, w, h, c):
    d.rounded_rectangle((x, y, x + w, y + h), radius=6, outline=c)
    d.polygon([(x + 6, y + h), (x + 4, y + h + 6), (x + 12, y + h)], outline=c)


def trueornot(text=None):
    im, d = canvas(94, 84)
    pts = []                                                                  # imagination: jagged, arguing
    for k in range(13):
        a = k / 12 * 2 * math.pi
        r = 12 if k % 2 else 16
        pts.append((24 + r * math.cos(a), 24 + r * 0.8 * math.sin(a)))
    d.polygon(pts, outline=FAINT)
    d.line((18, 22, 22, 26, 26, 20, 30, 27), fill=FAINT)
    bubble_round(d, 52, 12, 34, 22, INK)                                      # a read: round, still
    d.line((60, 23, 78, 23), fill=INK)
    d.rectangle((26, 52, 68, 76), outline=INK)                                # and the log, which decides
    d.line((47, 52, 47, 76), fill=INK)
    for k in range(3):
        d.line((30, 58 + k * 6, 43, 58 + k * 6), fill=FAINT)
        d.line((51, 58 + k * 6, 64, 58 + k * 6), fill=FAINT)
    d.line((58, 70, 60, 73, 65, 66), fill=HUE_LIGHT)
    return [im]


def askfirst(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    creature(im, 12, 49, facing=1)
    creature(im, 68, 49, body=FAINT, facing=-1)
    d.rectangle((40, 30, 54, 69), outline=INK)                                # a door between them,
    d.polygon([(41, 31), (49, 35), (49, 73), (41, 69)], fill=DIM, outline=FAINT)  # ajar, not open
    px(im, 47, 52, INK)
    return [im]


def ret(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    creature(im, 8, 49, facing=1)
    for k in range(0, 60, 3):                                                 # thrown out, small, along an arc
        x = 22 + k; y = 46 - int(26 * math.sin(k / 60 * math.pi))
        px(im, x, y, FAINT)
    d.polygon([(80, 44), (84, 48), (80, 50)], fill=FAINT)
    d.arc((20, 30, 88, 92), 200, 340, fill=HUE_LIGHT)                         # and back the same way, larger
    d.arc((20, 31, 88, 93), 200, 340, fill=HUE_LIGHT)
    d.polygon([(22, 52), (30, 50), (25, 58)], fill=HUE_LIGHT)
    return [im]


def moveburn(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    d.rectangle((40, 58, 54, 69), outline=INK)                                # a lamp, its bulb gone
    d.line((47, 50, 47, 58), fill=INK)
    d.arc((39, 34, 55, 52), 200, 340, fill=FAINT)
    for k in range(12):                                                       # everywhere, and nowhere it was meant
        a = k / 12 * 2 * math.pi + 0.3
        r0, r1 = 14 + (k % 3) * 3, 22 + (k % 4) * 4
        d.line((47 + r0 * math.cos(a), 40 + r0 * math.sin(a), 47 + r1 * math.cos(a), 40 + r1 * math.sin(a)),
               fill=INK if k % 2 else HUE_LIGHT)
    return [im]


def mending(text=None):
    im, d = canvas(94, 76)
    g_sun(im, 14, 2); g_moon(im, 60, 2)                                       # days, not seconds
    d.line((36, 12, 56, 12), fill=DIM)
    for r in (22, 17, 12):                                                    # a low, warm glow
        d.ellipse((47 - r, 54 - r // 2, 47 + r, 54 + r // 2), outline=DIM if r != 12 else FAINT)
    d.ellipse((34, 50, 58, 64), fill=FAINT)                                   # curled, resting
    d.ellipse((52, 46, 62, 56), fill=FAINT)
    px(im, 58, 50, PAPER)
    d.line((0, 66, 93, 66), fill=DIM)
    return [im]


def slow(text=None):
    im, d = canvas(94, 80)
    for x0, y0 in [(10, 18), (22, 12), (36, 16)]:                             # weathering: a cloud
        d.ellipse((x0, y0, x0 + 18, y0 + 14), outline=INK)
    d.rectangle((14, 24, 50, 30), fill=PAPER)
    d.line((12, 30, 54, 30), fill=INK)
    for k in range(6):
        d.line((16 + k * 6, 34, 13 + k * 6, 42), fill=FAINT)
    for k in range(18):                                                       # fortune: a thousand small turns,
        x, y = 58 + (k % 6) * 6, 46 + (k // 6) * 9                            # all nudged the same way
        d.line((x, y + 5, x + 3, y), fill=HUE_LIGHT if k == 17 else INK)
    return [im]


SPRITES.update({"prologue": prologue, "container": container, "twothings": twothings, "trueornot": trueornot,
           "askfirst": askfirst, "return": ret, "moveburn": moveburn, "mending": mending, "slow": slow})


# ==================================================================== batch b2


def ripples(text=None):
    im, d = canvas(94, 80)
    for r in range(4, 46, 5):                                                 # a ripple, no edge
        c = INK if r < 10 else FAINT if r < 26 else DIM
        d.ellipse((47 - r, 40 - r * 0.7, 47 + r, 40 + r * 0.7), outline=c)
    d.rectangle((46, 39, 48, 41), fill=HUE_LIGHT)                             # only a place where it is strongest
    return [im]


def lamp(d, x, y):
    d.rectangle((x, y + 8, x + 6, y + 12), outline=INK)
    d.ellipse((x - 1, y, x + 7, y + 8), outline=INK)


def allpaths(text=None):
    im, d = canvas(94, 70)
    lamp(d, 4, 28)
    g_eye(im, 72, 25)
    for k in range(-4, 5):                                                    # every route, most cancelling
        if k == 0:
            continue
        for x in range(13, 73, 2):
            t = (x - 13) / 60
            y = 35 + k * 7 * math.sin(t * math.pi)
            px(im, x, int(y), FAINT if abs(k) < 3 else DIM)
    d.line((13, 35, 72, 35), fill=HUE_LIGHT)                                  # and what is left
    return [im]


def lever(text=None):
    im, d = canvas(94, 76)
    d.line((0, 60, 93, 60), fill=DIM)
    d.ellipse((38, 46, 56, 60), fill=FAINT, outline=INK)                      # the stone, where it fell
    for k in range(60):                                                       # the record, in every grain of light
        a = k * 2.399
        r = 14 + (k * 7) % 30
        x, y = 47 + r * math.cos(a), 52 + r * 0.6 * math.sin(a)
        if y < 59:
            d.line((x, y, x + 1, y - 1), fill=DIM if k % 3 else FAINT)
    d.line((8, 72, 30, 64), fill=INK)                                         # a lever, with nothing to move
    d.polygon([(16, 72), (20, 68), (24, 72)], outline=FAINT)
    return [im]


def slits(text=None):
    frames = []
    for f in range(2):
        im, d = canvas(94, 76)
        lamp(d, 2, 30)
        d.rectangle((40, 6, 42, 70), fill=INK)                                # the barrier
        d.rectangle((40, 26, 42, 30), fill=PAPER)                             # its two slits
        d.rectangle((40, 44, 42, 48), fill=PAPER)
        d.line((86, 6, 86, 70), fill=FAINT)                                   # the wall
        if f == 0:                                                            # left alone: many bands
            for k in range(9):
                y = 10 + k * 7
                d.rectangle((80, y, 85, y + 2 + (2 if 2 < k < 6 else 0)), fill=INK if 2 < k < 6 else FAINT)
            for x in range(46, 80, 4):
                for y in (28, 46):
                    px(im, x, y + int((x - 46) * 0.2 * (1 if y == 28 else -1)), DIM)
        else:                                                                 # watched: a record of which path, two bands
            g_eye(im, 44, 4)
            d.rectangle((80, 24, 85, 31), fill=INK)
            d.rectangle((80, 43, 85, 50), fill=INK)
            d.line((43, 28, 79, 28), fill=DIM)
            d.line((43, 46, 79, 46), fill=DIM)
        frames.append(im)
    return frames


def onespoon(text=None):
    im, d = canvas(94, 76)
    d.line((8, 70, 47, 40), fill=INK)                                         # a path, forking
    d.line((47, 40, 22, 6), fill=FAINT)
    d.line((47, 40, 80, 8), fill=INK)
    d.line((48, 40, 81, 8), fill=INK)
    g_hand(im, 58, 4, c=FAINT)                                                # and the faintest pressure, on one
    return [im]


def link(text=None):
    im, d = canvas(94, 64)
    d.ellipse((14, 10, 56, 52), outline=INK)
    d.ellipse((38, 10, 80, 52), outline=INK)
    d.line((47, 22, 47, 40), fill=HUE_LIGHT)                                  # one lean, only where they overlap
    d.polygon([(44, 24), (47, 18), (50, 24)], fill=HUE_LIGHT)
    return [im]


def telepathy(text=None):
    im, d = canvas(94, 76)
    for x in range(0, 94):                                                    # the sea between them
        y = 66 + int(2 * math.sin(x / 4))
        px(im, x, y, FAINT)
        px(im, x, y + 5 + int(math.sin(x / 3)), DIM)
    d.rectangle((0, 44, 14, 62), fill=DIM); d.rectangle((80, 44, 93, 62), fill=DIM)
    creature(im, 2, 23, facing=1)
    creature(im, 78, 23, body=FAINT, facing=-1)
    for x in range(20, 76, 4):                                                # nothing sent; both turned already
        px(im, x, 30, DIM)
    return [im]


def cup(d, x, y):
    d.rectangle((x, y, x + 12, y + 16), outline=INK)
    d.arc((x + 9, y + 3, x + 17, y + 11), 270, 90, fill=INK)


def kindred(text=None):
    im, d = canvas(94, 60)
    cup(d, 6, 22); cup(d, 72, 22)                                             # two unmarked cups, carried apart
    for x in range(24, 70, 2):                                                # still correlated
        px(im, x, 30, HUE_LIGHT if x % 4 else DIM)
    return [im]


def chorus(text=None):
    im, d = canvas(94, 76)
    for k in range(20):                                                       # many, all leaning one way
        x, y = 8 + (k % 5) * 14 + (k // 5) % 2 * 7, 14 + (k // 5) * 14
        d.ellipse((x, y, x + 8, y + 8), outline=INK if k != 13 else FAINT)
        d.line((x + 4, y + 4, x + 7, y), fill=HUE_LIGHT)
    d.line((10, 72, 84, 66), fill=HUE_LIGHT)
    d.polygon([(84, 63), (90, 66), (84, 69)], fill=HUE_LIGHT)
    return [im]


def belief(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    for y in range(14, 70, 6):                                                # a wall, with one gap
        for x in range(36, 58, 8):
            if not (44 <= x <= 51 and y > 38):
                d.rectangle((x + (y // 6 % 2) * 4, y, x + 6 + (y // 6 % 2) * 4, y + 4), outline=FAINT)
    creature(im, 66, 49, facing=1)                                            # one crossed
    for k, x in enumerate((4, 18)):                                           # and now others walk through
        creature(im, x, 49, body=FAINT, facing=1)
    return [im]


def hacked(text=None):
    im, d = canvas(94, 60)
    d.line((4, 30, 89, 30), fill=HUE_LIGHT)                                   # the seam
    d.line((30, 30, 64, 30), fill=PAPER)
    pts = [(30 + k * 3, 30 + (4 if k % 2 else -4)) for k in range(12)]        # scarred, not widened
    d.line(pts, fill=INK)
    for x in range(32, 64, 6):
        d.line((x, 24, x + 2, 36), fill=FAINT)
    return [im]


def spelling(text=None):
    im, d = canvas(94, 76)
    d.line((47, 6, 47, 70), fill=DIM)
    d.line((4, 64, 42, 64), fill=DIM); d.line((52, 64, 90, 64), fill=DIM)
    d.ellipse((6, 52, 36, 62), fill=FAINT)                                    # A cures B: one laid down as ill
    d.rectangle((18, 22, 24, 38), outline=INK); d.rectangle((19, 18, 23, 22), outline=INK)
    d.line((2, 10, 44, 46), fill=DIM)                                         # struck through
    creature(im, 54, 43, facing=1)                                            # A over B: one leads, one walks
    creature(im, 74, 43, body=FAINT, facing=1)
    d.line((66, 52, 76, 47), fill=INK)
    return [im]


def processes(text=None):
    im, d = canvas(94, 64)
    d.ellipse((6, 24, 32, 42), fill=FAINT, outline=INK)                       # an object, held
    for k in range(4):                                                        # a process, going on
        for x in range(50, 90):
            px(im, x, 18 + k * 9 + int(2.5 * math.sin((x + k * 5) / 4)), INK if k % 2 == 0 else FAINT)
    d.polygon([(88, 15), (92, 19), (88, 23)], fill=HUE_LIGHT)
    d.line((40, 33, 46, 33), fill=DIM)
    return [im]


def sayinstead(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    d.rectangle((10, 20, 36, 69), outline=INK); d.rectangle((12, 22, 34, 69), fill=DIM)   # a door shut
    px(im, 31, 46, INK)
    d.rectangle((56, 20, 82, 69), outline=INK)                                # and one left open
    d.polygon([(57, 21), (66, 26), (66, 74), (57, 69)], fill=DIM, outline=FAINT)
    for k in range(5):
        d.line((68 + k * 3, 30, 68 + k * 3, 66), fill=FAINT if k % 2 else HUE_LIGHT)
    return [im]


SPRITES.update({"ripples": ripples, "allpaths": allpaths, "lever": lever, "slits": slits, "onespoon": onespoon,
           "link": link, "telepathy": telepathy, "kindred": kindred, "chorus": chorus, "belief": belief,
           "hacked": hacked, "spelling": spelling, "processes": processes, "sayinstead": sayinstead})


# ==================================================================== batch b3

CENTRE_Y = [74, 64, 54, 44, 36, 26, 16]       # root to crown, on the big figure's midline


def big_figure(d, x, c=FAINT):
    d.ellipse((x - 9, 8, x + 9, 26), outline=c)                               # head
    d.polygon([(x - 6, 26), (x + 6, 26), (x + 16, 76), (x - 16, 76)], outline=c)
    d.line((x - 18, 80, x + 18, 80), fill=DIM)


def centre(d, x, y, state="ring", c=INK):
    if state == "closed":
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=c)
    elif state == "open":
        for a in range(0, 360, 45):
            r = math.radians(a)
            d.line((x + 2 * math.cos(r), y + 2 * math.sin(r), x + 4 * math.cos(r), y + 4 * math.sin(r)), fill=c)
    else:
        d.ellipse((x - 2, y - 2, x + 2, y + 2), outline=c)


def centres(text=None):
    im, d = canvas(94, 84)
    big_figure(d, 32)
    for y in CENTRE_Y:
        centre(d, 32, y)
    for k, st in enumerate(("closed", "ring", "open")):                       # too closed, in balance, too open
        centre(d, 74, 26 + k * 18, st)
    d.line((64, 22, 64, 66), fill=DIM)
    return [im]


def body_with(marks, extra):
    def draw(text=None):
        im, d = canvas(94, 84)
        big_figure(d, 30)
        for k, y in enumerate(CENTRE_Y):
            centre(d, 30, y, "ring", INK if k in marks else DIM)
        extra(im, d)
        return [im]
    return draw


def _lower(im, d):                                                            # walk, dance
    for k in range(3):
        d.arc((50 + k * 4, 52 - k * 6, 78 + k * 4, 80 - k * 6), 300, 60, fill=FAINT if k else INK)
    for k, x in enumerate((56, 64, 72, 80)):
        px(im, x, 80 - (k % 2) * 2, FAINT); px(im, x + 1, 80 - (k % 2) * 2, FAINT)


def _heart(im, d):                                                            # sing; a letter to yourself
    d.ellipse((58, 18, 63, 22), fill=INK); d.line((63, 20, 63, 8), fill=INK); d.line((63, 8, 68, 11), fill=INK)
    d.rectangle((56, 50, 78, 64), outline=INK); d.line((56, 50, 67, 58), fill=INK); d.line((78, 50, 67, 58), fill=INK)


def _upper(im, d):                                                            # dreams; an I am list
    for x0, y0 in [(54, 6), (62, 3), (70, 6)]:
        d.ellipse((x0, y0, x0 + 10, y0 + 8), outline=FAINT)
    d.rectangle((58, 40, 80, 70), outline=INK)
    for k in range(4):
        d.line((61, 45 + k * 6, 63, 45 + k * 6), fill=INK); d.line((66, 45 + k * 6, 77, 45 + k * 6), fill=FAINT)


lower = body_with({0, 1, 2}, _lower)
heart = body_with({3, 4}, _heart)
upper = body_with({5, 6}, _upper)


def window(d, x, y, w, h):
    d.rectangle((x, y, x + w, y + h), outline=INK)
    d.line((x, y + h + 1, x + w, y + h + 1), fill=FAINT)


def eyecrown(text=None):
    im, d = canvas(94, 76)
    window(d, 6, 14, 34, 40)                                                  # a window, someone looking out
    g_eye(im, 13, 24)
    d.line((42, 34, 46, 30), fill=HUE_LIGHT)
    dither(im, (52, 4, 94, 70), DIM, step=2)                                  # and one open, with no one in it:
    d.rectangle((54, 14, 88, 54), fill=PAPER)                                 # the field runs straight through
    dither(im, (55, 15, 88, 54), FAINT, step=2)
    window(d, 54, 14, 34, 40)
    return [im]


def friday(text=None):
    im, d = canvas(94, 72)
    g_eye(im, 37, 4)                                                          # read lightly,
    d.polygon([(18, 34), (47, 30), (47, 64), (18, 68)], outline=INK)          # write everything down
    d.polygon([(76, 34), (47, 30), (47, 64), (76, 68)], outline=INK)
    for k in range(4):
        d.line((22, 40 + k * 6, 43, 37 + k * 6), fill=FAINT)
    return [im]


def saturday(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    creature(im, 18, 49, facing=1)                                            # who was looking
    d.ellipse((50, 26, 76, 70), outline=INK)
    d.ellipse((52, 28, 74, 68), fill=DIM)
    creature(im, 56, 46, body=FAINT, facing=-1)
    return [im]


def before(text=None):
    im, d = canvas(94, 72)
    d.rectangle((6, 18, 30, 50), outline=INK)                                 # a spell, written
    for k in range(4):
        d.line((10, 24 + k * 6, 26, 24 + k * 6), fill=FAINT)
    d.ellipse((22, 40, 28, 47), fill=INK); d.line((21, 41, 19, 39), fill=INK); d.line((29, 41, 31, 39), fill=INK)  # a bug in it
    d.line((34, 34, 54, 34), fill=DIM); d.polygon([(54, 31), (58, 34), (54, 37)], fill=DIM)
    d.ellipse((60, 20, 80, 40), outline=INK); d.line((77, 37, 86, 48), fill=INK)   # test first
    d.line((64, 30, 68, 34, 75, 25), fill=HUE_LIGHT)
    return [im]


def misread(text=None):
    im, d = canvas(94, 76)
    for k in range(20):                                                       # many, one set of instructions
        x, y = 8 + (k % 5) * 17, 6 + (k // 5) * 17
        d.ellipse((x, y, x + 12, y + 12), outline=FAINT)
        if k == 12:
            d.line((x + 3, y + 4, x + 6, y + 8, x + 9, y + 4), fill=INK)     # one, read wrong
        else:
            d.line((x + 3, y + 8, x + 6, y + 4, x + 9, y + 8), fill=DIM)
    return [im]


def mask(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    for x in (6, 66, 80):
        creature(im, x, 49, body=FAINT, facing=1 if x < 40 else -1)
    creature(im, 36, 49, facing=1)
    d.ellipse((40, 47, 52, 58), fill=INK, outline=INK)                        # a mask held over the face
    px(im, 43, 51, PAPER); px(im, 49, 51, PAPER)
    d.line((36, 62, 41, 56), fill=INK)
    return [im]


def samedrive(text=None):
    im, d = canvas(94, 72)
    d.line((64, 6, 64, 66), fill=FAINT)                                       # as far as the whole can answer
    d.line((8, 24, 40, 24), fill=INK); d.polygon([(40, 20), (46, 24), (40, 28)], fill=INK)
    d.line((8, 48, 80, 48), fill=INK); d.polygon([(80, 44), (88, 48), (80, 52)], fill=INK)  # the same drive, too far
    d.line((8, 49, 80, 49), fill=INK)
    return [im]


def twovoices(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    creature(im, 10, 49, facing=1)
    creature(im, 70, 49, body=FAINT, facing=-1)
    d.rounded_rectangle((4, 14, 40, 34), radius=5, outline=INK)              # one says a thing
    d.line((12, 24, 32, 24), fill=INK)
    d.rounded_rectangle((54, 22, 90, 42), radius=5, outline=FAINT)           # the other asks what it means
    d.line((70, 28, 74, 28, 74, 32, 72, 34), fill=FAINT); px(im, 72, 37, FAINT)
    return [im]


def recognition(text=None):
    im, d = canvas(94, 76)
    pts = [(20, 40), (36, 30), (36, 50), (52, 40), (52, 20), (52, 60), (68, 30), (68, 50)]
    for x, y in pts:                                                          # touching their neighbours
        d.ellipse((x - 8, y - 8, x + 8, y + 8), outline=INK if (x, y) != (52, 40) else FAINT)
    d.ellipse((46, 4, 58, 13), outline=FAINT)                                 # the mask, off
    px(im, 49, 8, FAINT); px(im, 55, 8, FAINT)
    return [im]


def lastword(text=None):
    im, d = canvas(94, 76)
    d.line((0, 70, 93, 70), fill=DIM)
    creature(im, 22, 49, facing=1)
    creature(im, 58, 49, facing=-1)                                           # we reflect one another
    for y in range(36, 72, 3):
        px(im, 47, y, HUE_LIGHT)
    return [im]


SPRITES.update({"centres": centres, "lower": lower, "heart": heart, "upper": upper, "eyecrown": eyecrown,
           "friday": friday, "saturday": saturday, "before": before, "misread": misread, "mask": mask,
           "samedrive": samedrive, "twovoices": twovoices, "recognition": recognition, "lastword": lastword})


def oneaday(text=None):
    im, d = canvas(94, 50)
    for k in range(7):                                                        # seven days, one watched
        x = 6 + k * 12
        if k == 4:
            d.ellipse((x, 18, x + 9, 27), fill=HUE_LIGHT)
        else:
            d.ellipse((x, 18, x + 9, 27), outline=INK if k < 4 else FAINT)
    return [im]


SPRITES["oneaday"] = oneaday

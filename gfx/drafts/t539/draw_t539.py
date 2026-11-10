#!/usr/bin/env python3
"""T-539 (DRAFT): THE UNITY BOOK's LENS picture without the old ')' marks.

    ~/.pyenv/shims/python3 gfx/drafts/t539/draw_t539.py OUT_DIR [FRAME.png]

u_lens (tools/thirdbook_art.py) is the last picture drawing tools/thirdbook_art.py's motion() -- a few speed lines
closed by a ')' arc -- for "the Field faint outside" the lens. Batch 4 (T-519, 2026-11-06) redrew the FIELD's own
pictures with passing(): a round body smeared into speed lines, its sprout riding on top, the grass bent behind. The
LENS was not on that list. Three ways to draw the field outside the lens in that later language; everything else on
the page (the sky, the numbers, the lens, its 101, the two threads on the rim, the creases) is u_lens unchanged.

    A  PASSING        the FIELD page's own daemons, three, small and faint, where the marks stood
    B  FIELD BELOW    the page of numbers above, the FIELD's grass below it, the lens held over the line between
    C  BENT GRASS     no daemon at all: only the grass bent where they went, three tufts

Nothing here writes into the game; the pick goes into u_lens itself. FRAME, when given, is a 240x160 theatre shot of
a WHOLE page of THE UNITY BOOK: each draft is set into its picture window (book_reader.c SB_PIC_X 15, SB_PIC_Y 13).
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import thirdbook_art as ta
import gensubtle as gs
from thirdbook_art import C, D, PW, PH, blank, usky, numpage, lens_glass, digit, crease, ground, grass, passing, px

PIC_X, PIC_Y = 15, 13


def lens_over(im):
    """u_lens's lens, its number and its two threads, unchanged."""
    lens_glass(im, 46, 40, 16, rim="C_INK", handle=(1, 1), inside="C_EDGE_DARK")
    for k, n in enumerate((1, 0, 1)):
        digit(im, 41 + k * 4, 38, n, "C_INK")
    D(im).arc((30, 24, 62, 56), 200, 250, fill=C["C_RING"]); D(im).arc((30, 24, 62, 56), 290, 340, fill=C["C_RULE"])


def bent(im, x, y, c="C_FAINT", n=3):
    """A tuft of grass pressed one way, as passing() leaves it behind a daemon: N blades rising from one root, each
    standing a little, then bent over to the left; the last ones flatter, as if it went that way."""
    d = D(im)
    for k in range(n):
        bx = x + k * 3
        h = 4 if k < n - 1 else 2                                                 # the last, pressed flatter
        d.line((bx, y, bx, y - h + 1), fill=C[c])                                 # standing
        d.line((bx - 1, y - h, bx - 2, y - h), fill=C[c])                         # its tip bent over, to the left


def u_lens_now():
    return ta.u_lens()


def u_lens_a():
    """A PASSING: the FIELD's daemons, small and faint, where the marks stood."""
    im = blank(PW, PH, "C_PAPER")
    ta.usky(im, PH, seed=341)
    numpage(im, 4, 6, 91, 84, "C_HIGHLIGHT", 343, page="C_EDGE", edge="C_FAINT")
    for x, y, s, lead in ((24, 64, 1, "C_RING"), (86, 13, 2, "C_RULE"), (88, 67, 3, "C_MARGIN")):
        passing(im, x, y, "C_FAINT", lead, s, n=3, ln=13)
    lens_over(im)
    crease(im, y0=0, y1=6); crease(im, y0=85, y1=PH)
    return im


def u_lens_b():
    """B FIELD BELOW: the numbers above, the FIELD's grass below, the lens over the line between."""
    im = blank(PW, PH, "C_PAPER")
    ta.usky(im, PH, seed=341)
    numpage(im, 4, 6, 91, 58, "C_HIGHLIGHT", 343, page="C_EDGE", edge="C_FAINT")
    ground(im, 60, fill="C_EDGE_DARK", line="C_CHALK", x0=4, x1=92)
    D(im).rectangle((4, 60, 91, 84), outline=C["C_FAINT"])
    D(im).line((5, 60, 90, 60), fill=C["C_CHALK"])
    grass(im, 82, 347, "C_EDGE", 22, 6, 90)
    grass(im, 70, 348, "C_HIGHLIGHT", 12, 6, 90)
    for x, y, s, lead in ((22, 72, 1, "C_RING"), (88, 76, 2, "C_RULE")):
        passing(im, x, y, "C_FAINT", lead, s, n=3, ln=12)
    lens_over(im)
    crease(im, y0=0, y1=6); crease(im, y0=85, y1=PH)
    return im


def u_lens_c():
    """C BENT GRASS: no daemon, only the grass pressed flat where they went."""
    im = blank(PW, PH, "C_PAPER")
    ta.usky(im, PH, seed=341)
    numpage(im, 4, 6, 91, 84, "C_HIGHLIGHT", 343, page="C_EDGE", edge="C_FAINT")
    for x, y, lead in ((18, 70, "C_RING"), (76, 18, "C_RULE"), (78, 74, "C_MARGIN")):
        bent(im, x, y, "C_FAINT", 4)
        px(im, x - 3, y - 1, lead)                     # one seed of the thread's colour, where it went first
    lens_over(im)
    crease(im, y0=0, y1=6); crease(im, y0=85, y1=PH)
    return im


DRAFTS = [("now", "today: the old ')' marks", u_lens_now),
          ("A", "A  PASSING", u_lens_a),
          ("B", "B  FIELD BELOW", u_lens_b),
          ("C", "C  BENT GRASS", u_lens_c)]


def main():
    out = sys.argv[1]
    frame = Image.open(sys.argv[2]).convert("RGB") if len(sys.argv) > 2 else None
    os.makedirs(out, exist_ok=True)
    ta.use("unity")
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 15)
        big = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
    except OSError:
        font = big = ImageFont.load_default()
    BG, FG, DIM = (28, 28, 30), (230, 230, 230), (150, 150, 155)
    S = 3
    pics = []
    for key, label, fn in DRAFTS:
        ind = gs.indexed(fn(), PW, PH)
        t, u, n, roles = ta.limits(ind)
        ind.save(os.path.join(out, "unity_picture_lens_%s.png" % key))
        print("%-4s %3d tiles (%3d unique), %2d of 16 colours" % (key, t, u, n))
        pics.append((key, label, ind.convert("RGB"), "%d tiles, %d/16 colours" % (t, n)))
    cw = (240 * S if frame else PW * 4) + 30
    W = 20 + cw * 2
    rows = 2
    ch = (160 * S + 8 + PH * 2 if frame else PH * 4) + 60
    sheet = Image.new("RGB", (W, 70 + ch * rows), BG)
    d = ImageDraw.Draw(sheet)
    d.text((20, 12), "T-539  THE UNITY BOOK, THE CREASE: 11. LENS, read WHOLE -- the field outside the lens (DRAFT)",
           fill=FG, font=big)
    d.text((20, 40), "each draft set into a real theatre frame of a WHOLE page (7 Nov); the page's words blanked, "
           "they are another entry's. Under each, the game's own size (1x).", fill=DIM, font=font)
    for i, (key, label, pic, lim) in enumerate(pics):
        x = 20 + cw * (i % 2)
        y = 70 + ch * (i // 2)
        d.text((x, y), label, fill=FG, font=big)
        d.text((x + 330, y + 4), lim, fill=DIM, font=font)
        if frame:
            f = frame.copy()
            f.paste(pic, (PIC_X, PIC_Y))
            sheet.paste(f.resize((240 * S, 160 * S), Image.NEAREST), (x, y + 28))
            sheet.paste(f, (x, y + 28 + 160 * S + 8))
            sheet.paste(pic.resize((PW * 2, PH * 2), Image.NEAREST), (x + 260, y + 28 + 160 * S + 8))
        else:
            sheet.paste(pic.resize((PW * 4, PH * 4), Image.NEAREST), (x, y + 28))
    sheet.save(os.path.join(out, "t539_lens_marks.png"))
    print("wrote", os.path.join(out, "t539_lens_marks.png"))


if __name__ == "__main__":
    main()

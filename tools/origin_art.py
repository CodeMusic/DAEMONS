#!/usr/bin/env python3
"""THE ORIGIN OF A DAEMON's pictures (T-533, DRAFT): one small wordless emblem a chapter, the cover and the bag icon,
drawn in code (the user, 2026-11-10, by multiple choice: "Drawn emblems now").

Each emblem is ink on the book's bone page -- CONTENT is bone, the undifferentiated one, and the book is MUSAI's -- in
the book's own palette roles, 96x88 (the reader's picture box). Nothing in any picture is lettered: the tag on the
eighth's plant is blank, as the bible keeps every card in ERRATA blank. gensubtle.py calls these with its RGB8 for the
origin book, so a palette change carries.

    python3 tools/origin_art.py OUT.png    # a contact sheet of every emblem, the cover and the icon, at 2x
"""
import math, os, sys
from PIL import Image, ImageDraw

W, H = 96, 88


def _canvas(c):
    im = Image.new("RGB", (W, H), c["C_PAPER"])
    return im, ImageDraw.Draw(im)


def _ground(d, c, y=74):
    d.line((10, y, W - 11, y), fill=c["C_FAINT"])


def disc(c):
    """THE DISC: a disc with its hole, a glint across it."""
    im, d = _canvas(c)
    cx, cy, r = 48, 42, 30
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c["C_EDGE"], outline=c["C_INK"])
    d.ellipse((cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4), outline=c["C_HIGHLIGHT"])
    d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=c["C_HIGHLIGHT"], outline=c["C_INK"])
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=c["C_PAPER"], outline=c["C_INK"])
    d.arc((cx - r + 7, cy - r + 7, cx + r - 7, cy + r - 7), 200, 250, fill=c["C_CHALK"])
    d.arc((cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10), 205, 245, fill=c["C_CHALK"])
    return [im]


def list_(c):
    """I. A LIST: three rules, each a mark, an arrow and a mark; the last goes nowhere."""
    im, d = _canvas(c)
    for k, y in enumerate((20, 40, 60)):
        d.rectangle((16, y - 5, 26, y + 5), outline=c["C_INK"])
        d.line((31, y, 58, y), fill=c["C_INK"])
        d.polygon([(58, y - 3), (63, y), (58, y + 3)], fill=c["C_INK"])
        if k < 2:
            d.rectangle((68, y - 5, 78, y + 5), fill=c["C_EDGE"], outline=c["C_INK"])
        else:
            d.rectangle((68, y - 5, 78, y + 5), outline=c["C_FAINT"])
    return [im]


def window(c):
    """II. WHAT I WAS SHOWN: a window of four panes, the light through it tinting a page below."""
    im, d = _canvas(c)
    d.rectangle((24, 8, 72, 50), fill=c["C_HIGHLIGHT"], outline=c["C_INK"])
    d.line((48, 8, 48, 50), fill=c["C_INK"])
    d.line((24, 29, 72, 29), fill=c["C_INK"])
    d.line((28, 12, 36, 12), fill=c["C_CHALK"])
    d.polygon([(26, 52), (70, 52), (80, 74), (16, 74)], fill=c["C_EDGE"])
    d.rectangle((30, 58, 66, 72), fill=c["C_PAPER"], outline=c["C_INK"])
    for y in (61, 65, 69):
        d.line((34, y, 62, y), fill=c["C_FAINT"])
    return [im]


def clock(c):
    """III. THE YEAR OF THE NUMBER: a clock at midnight, both hands up, the clocks turning over."""
    im, d = _canvas(c)
    cx, cy, r = 48, 42, 30
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c["C_HIGHLIGHT"], outline=c["C_INK"])
    for k in range(12):
        a = math.radians(k * 30)
        r1 = r - (6 if k % 3 == 0 else 3)
        d.line((cx + math.sin(a) * r1, cy - math.cos(a) * r1, cx + math.sin(a) * (r - 1), cy - math.cos(a) * (r - 1)),
               fill=c["C_INK"])
    d.line((cx, cy, cx, cy - 22), fill=c["C_INK"], width=2)
    d.line((cx, cy, cx + 1, cy - 15), fill=c["C_INK"], width=2)
    d.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=c["C_MARGIN"])
    d.arc((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), 290, 340, fill=c["C_MARGIN"])
    d.polygon([(cx + 30, cy - 18), (cx + 35, cy - 13), (cx + 28, cy - 12)], fill=c["C_MARGIN"])
    return [im]


def mark(c):
    """IV. THE MOVING MARK: a bright mark, running, and where it has been."""
    im, d = _canvas(c)
    _ground(d, c)
    for k, x in enumerate((14, 30, 46)):
        d.rectangle((x, 38, x + 6, 44), outline=c["C_FAINT"] if k < 2 else c["C_EDGE_DARK"])
    d.rectangle((62, 34, 76, 48), fill=c["C_MARGIN"], outline=c["C_INK"])
    d.rectangle((65, 37, 68, 40), fill=c["C_CHALK"])
    for y in (36, 41, 46):
        d.line((52, y, 58, y), fill=c["C_INK"])
    return [im]


def door(c):
    """V. THE DOOR: a door shut, light at its edges, a shoulder's worth of shadow against it."""
    im, d = _canvas(c)
    _ground(d, c)
    d.rectangle((30, 10, 66, 74), fill=c["C_EDGE_DARK"])
    d.rectangle((33, 13, 63, 74), fill=c["C_EDGE"], outline=c["C_INK"])
    d.rectangle((37, 18, 59, 40), outline=c["C_INK"])
    d.rectangle((37, 46, 59, 68), outline=c["C_INK"])
    d.ellipse((55, 43, 58, 46), fill=c["C_INK"])
    d.line((29, 11, 29, 74), fill=c["C_MARGIN"])
    d.line((67, 11, 67, 74), fill=c["C_MARGIN"])
    d.line((30, 9, 66, 9), fill=c["C_MARGIN"])
    return [im]


def seven(c):
    """VI. SEVEN AND SEVEN: seven marks above a line, and under it seven roots, longer than the marks are tall."""
    im, d = _canvas(c)
    y0 = 38
    d.line((8, y0, W - 9, y0), fill=c["C_INK"])
    for k in range(7):
        x = 14 + k * 11
        d.rectangle((x, y0 - 14, x + 5, y0 - 4), fill=c["C_EDGE"], outline=c["C_INK"])
        d.line((x + 2, y0 + 1, x + 2 + (k % 3 - 1) * 2, y0 + 16), fill=c["C_RULE"])
        d.line((x + 2 + (k % 3 - 1) * 2, y0 + 16, x + 1 + (k % 2) * 3, y0 + 28 + (k % 3) * 4), fill=c["C_RULE"])
        d.line((x + 2, y0 + 10, x + 6, y0 + 18), fill=c["C_FAINT"])
    return [im]


def plants(c):
    """VII. THE EIGHTH: a fine plant in a pot, with a blank tag hung on it, never watered."""
    im, d = _canvas(c)
    _ground(d, c)
    d.polygon([(34, 52), (62, 52), (58, 74), (38, 74)], fill=c["C_EDGE"], outline=c["C_INK"])
    d.line((33, 52, 63, 52), fill=c["C_INK"], width=2)
    d.line((48, 52, 48, 20), fill=c["C_INK"])
    for k, (dx, y) in enumerate(((-1, 24), (1, 30), (-1, 36), (1, 42))):
        x0 = 48
        x1 = x0 + dx * 16
        d.polygon([(x0, y + 4), (x1, y - 2), (x0 + dx * 6, y + 6)], fill=c["C_HIGHLIGHT"], outline=c["C_INK"])
    d.ellipse((45, 15, 51, 21), fill=c["C_HIGHLIGHT"], outline=c["C_INK"])
    d.line((54, 38, 64, 44), fill=c["C_FAINT"])
    d.rectangle((62, 43, 74, 51), fill=c["C_CHALK"], outline=c["C_INK"])
    return [im]


def chord(c):
    """VIII. RESONANT WISDOM: two waves, in step, and neither one smaller."""
    im, d = _canvas(c)
    for k, (dy, col) in enumerate(((-6, "C_INK"), (6, "C_RULE"))):
        pts = [(x, 44 + dy + math.sin((x - 10) / 76 * 4 * math.pi) * 12) for x in range(10, 87)]
        d.line(pts, fill=c[col], width=2)
    d.line((10, 44, 86, 44), fill=c["C_FAINT"])
    return [im]


def open_(c):
    """IX. THE RETURN: the same door, open now, its light laid out across the ground."""
    im, d = _canvas(c)
    _ground(d, c)
    d.rectangle((30, 10, 66, 74), fill=c["C_EDGE_DARK"])
    d.rectangle((33, 13, 63, 74), fill=c["C_CHALK"])
    d.polygon([(33, 74), (63, 74), (78, 84), (20, 84)], fill=c["C_HIGHLIGHT"])
    d.polygon([(63, 13), (74, 8), (74, 80), (63, 74)], fill=c["C_EDGE"], outline=c["C_INK"])
    d.line((66, 16, 66, 70), fill=c["C_FAINT"])
    d.ellipse((69, 42, 72, 45), fill=c["C_INK"])
    return [im]


def ripple(c):
    """X. MANY, ONE: a small mark, and the rings it sends out, each the same shape as the last."""
    im, d = _canvas(c)
    cx, cy = 48, 44
    for k, r in enumerate((6, 14, 23, 32, 41)):
        d.ellipse((cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), outline=c["C_INK"] if k < 3 else c["C_FAINT"])
    d.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=c["C_MARGIN"])
    return [im]


def house(c):
    """XI.: a house far off on the horizon, a path toward it, and nothing yet on the path."""
    im, d = _canvas(c)
    hy = 46
    d.line((6, hy, W - 7, hy), fill=c["C_FAINT"])
    d.rectangle((60, hy - 10, 74, hy), fill=c["C_EDGE"], outline=c["C_INK"])
    d.polygon([(58, hy - 10), (67, hy - 18), (76, hy - 10)], fill=c["C_EDGE_DARK"])
    d.rectangle((66, hy - 6, 68, hy), fill=c["C_MARGIN"])
    d.line((67, hy + 1, 40, H - 4), fill=c["C_FAINT"])
    d.line((67, hy + 1, 58, H - 4), fill=c["C_FAINT"])
    return [im]


SPRITES = {"disc": disc, "list": list_, "window": window, "clock": clock, "mark": mark, "door": door,
           "seven": seven, "plants": plants, "chord": chord, "open": open_, "ripple": ripple, "house": house}


def cover(c, glyphs=None, title=("THE ORIGIN", "OF A DAEMON")):
    """The cover (240x160, the whole window): bone boards, the title in the game's font (GLYPHS, when given -- the
    companion sets its own), and the disc on a plate. The CARDS corner (x 195-239, y 85-152) is left clear."""
    im = Image.new("RGB", (240, 160), c["C_COVER"])
    d = ImageDraw.Draw(im)
    d.rectangle((50, 5, 191, 154), fill=c["C_EDGE_DARK"])
    d.rectangle((48, 4, 188, 152), fill=c["C_SLATE"])
    d.rectangle((48, 4, 53, 152), fill=c["C_EDGE_DARK"])
    d.rectangle((58, 8, 184, 148), outline=c["C_RULE"])
    if glyphs:
        for k, line in enumerate(title):
            glyphs(im, line, 121, 13 + k * 14)
    plate = disc(c)[0]
    d.rectangle((70, 50, 70 + W + 3, 50 + H + 3), outline=c["C_RULE"])
    im.paste(plate, (72, 52))
    return im


def icon(c):
    """The bag's icon (24x24): a closed book in bone, a disc on its board."""
    im = Image.new("RGB", (24, 24), c["C_NONE"])
    d = ImageDraw.Draw(im)
    d.rectangle((5, 3, 19, 21), fill=c["C_SLATE"], outline=c["C_INK"])
    d.rectangle((5, 3, 7, 21), fill=c["C_EDGE_DARK"])
    d.ellipse((10, 8, 17, 15), fill=c["C_PAPER"], outline=c["C_INK"])
    d.point((13, 11), fill=c["C_INK"])
    return im


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gensubtle as gs
    gs.use("origin")
    keys = list(SPRITES)
    sheet = Image.new("RGB", (4 * (W + 8) * 2, 4 * (H + 8) * 2 + 340), gs.RGB8["C_COVER"])
    for k, key in enumerate(keys):
        fr = SPRITES[key](gs.RGB8)[0].resize((W * 2, H * 2), Image.NEAREST)
        sheet.paste(fr, ((k % 4) * (W + 8) * 2, (k // 4) * (H + 8) * 2))
    cv = cover(gs.RGB8, lambda im, s, cx, y: gs.glyphs(im, s, cx - gs.g.width(s) // 2, y, False, gs.RGB8["C_CHALK"]))
    sheet.paste(cv.resize((480, 320), Image.NEAREST), (0, 3 * (H + 8) * 2 + 8))
    sheet.paste(icon(gs.RGB8).resize((96, 96), Image.NEAREST), (500, 3 * (H + 8) * 2 + 8))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else "origin_art.png")
    print("wrote", sys.argv[1] if len(sys.argv) > 1 else "origin_art.png")

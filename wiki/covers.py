#!/usr/bin/env python3
"""The two books' covers for the wiki's Books page, lettered (the user, 2026-10-19: "neither book cover shows the
title, we have to draw them in companion so the wiki images need to be rasterized with the text").

The covers carry no lettering of their own: the game's font is Nintendo's, and nothing of Nintendo's is published, so
the companion sets each title over the art in its own type (app/screens/Library.tsx CoverTitle, app/screens/Subtle.tsx).
This draws them the same way into still pictures, in a common monospace (Menlo, the Mac's -- only the picture is
published, never the font): the book cut from the game's 240x160 screen (x 54..185), at 3x, its pixels kept square.

    python3 wiki/covers.py            report what would change
    python3 wiki/covers.py --write    write wiki/images/guide_cover.png and subtle_cover.png

It reads the companion's data (the `companion` link, see CLAUDE.md): art/guide_cover.png and art/subtle_cover.png, and
the titles in guide.json and subtle.json. The Books page links the pictures from this repository's main branch.
"""
import io, json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "companion", "server", "data")
OUT = os.path.join(ROOT, "wiki", "images")
MENLO = "/System/Library/Fonts/Menlo.ttc"            # 0 regular, 1 bold, 2 italic, 3 bold italic
K = 3                                                # the scale: a whole multiple, so the art's pixels stay square


def font(size, face=1):
    return ImageFont.truetype(MENLO, size, index=face)


def spaced(d, text, f, y, w, colour, spacing):
    """`text` centred across `w` at `y`, with `spacing` pixels between letters (the app's letterSpacing)."""
    widths = [d.textlength(c, font=f) for c in text]
    x = (w - (sum(widths) + spacing * max(0, len(text) - 1))) / 2
    for c, cw in zip(text, widths):
        d.text((x, y), c, font=f, fill=colour)
        x += cw + spacing


def book(art):
    im = Image.open(os.path.join(DATA, "art", art)).convert("RGB").crop((54, 0, 186, 160))
    return im.resize((im.width * K, im.height * K), Image.NEAREST)


def guide():
    g = json.load(open(os.path.join(DATA, "guide.json")))
    im = book("guide_cover.png"); d = ImageDraw.Draw(im); w = im.width
    words = g["title"].split(" "); big = " ".join(words[-2:]); rest = words[:-2]
    cut = min(range(1, len(rest)), key=lambda k: abs(len(" ".join(rest[:k])) - len(" ".join(rest[k:])))) if len(rest) > 1 else len(rest)
    ink = "#f3f4f6"                                  # placed as the app places them (at 2x there: 10, 27, 50, 296)
    spaced(d, " ".join(rest[:cut]), font(20), 15, w, ink, 1.5)
    spaced(d, " ".join(rest[cut:]), font(20), 40, w, ink, 1.5)
    spaced(d, big, font(43), 72, w, ink, 3)
    spaced(d, g.get("author", ""), font(18), 444, w, ink, 1.5)   # under the art, clear of it (the user, 2026-10-19)
    return im


def subtle():
    s = json.load(open(os.path.join(DATA, "subtle.json")))
    im = book("subtle_cover.png"); d = ImageDraw.Draw(im); w = im.width
    spaced(d, s["title"], font(21), 36, w, "#f0e6f2", 1.5)       # a little below the border (the user, 2026-10-19)
    spaced(d, s.get("subtitle", ""), font(16, 2), 75, w, "#9a86a0", 0)
    return im


def png(im):
    b = io.BytesIO(); im.save(b, "PNG", optimize=True); return b.getvalue()


def main():
    write = "--write" in sys.argv
    for name, make in (("guide_cover.png", guide), ("subtle_cover.png", subtle)):
        path = os.path.join(OUT, name)
        body = png(make())
        old = open(path, "rb").read() if os.path.exists(path) else None
        state = "unchanged" if old == body else ("written" if write else "would write")
        if write and old != body:
            os.makedirs(OUT, exist_ok=True); open(path, "wb").write(body)
        print(f"  covers: {name} {state}")


if __name__ == "__main__":
    main()

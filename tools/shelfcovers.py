#!/usr/bin/env python3
"""Every book on the companion's LIBRARY shelf, a cover to stand face-out (C-320; the user, 2026-11-10: "some books do
not have a title art shown, it just saw a word. We should ensure all books have their appealing artwork ... usually the
books cover is enough").

    python3 tools/shelfcovers.py            report what would change
    python3 tools/shelfcovers.py --write    write companion/server/data/art/books/<book>.png

Every cover is 320 pixels tall; its width is the book's own, so the shelf stands books of different shapes side by side.

WHERE EACH COMES FROM -- nothing is drawn by hand, so a book reprinted or a cover redrawn is a rerun away:
  the printed books   page 1 of docs/DAEMONS-*.pdf, as tools/manual.py printed it (so `manual.py --write` reruns this)
  the GUIDE, THE SUBTLE LAYER   wiki/covers.py's lettered covers (the art without the game's font, set in Menlo)
  the third book's three forms  its cover cut from the game's screen where the book lies (app/ui/bookPicture.tsx
                      ON_COVER), lettered where the game letters it (BAND there), in Menlo
  THE ORIGIN OF A DAEMON  the same: its cover (art/origin_cover.png) cut where the book lies, its title's two lines
                      lettered where the game letters them, in Menlo (T-533)
  CALLOW SCHOOL       the TEXTBOOK's own cover (art/textbook_cover.png)
  NOTEBOOK, SONGBOOK, STREAM   cloth boards drawn here around the game's own pictures: the NOTEBOOK's item icon, the
                      SONGBOOK's twelve coloured notes (art/play_notes.png), the eight MARKS (art/mark_N.png)

Only the picture is published, never a font. Nothing of Nintendo's: the game's font never letters a cover.
"""
import io, json, os, random, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "companion", "server", "data")
ART = os.path.join(DATA, "art")
OUT = os.path.join(ART, "books")
H = 320                                              # every cover's height
MENLO = "/System/Library/Fonts/Menlo.ttc"            # 0 regular, 1 bold, 2 italic, 3 bold italic
GBA = os.path.join(ROOT, "engineGba")

sys.path.insert(0, os.path.join(ROOT, "wiki"))

# the printed books: the shelf's id -> the PDF (the companion's app/state/manual.ts names them the same)
PDFS = {"player": "DAEMONS-manual.pdf", "quick": "DAEMONS-quickstart.pdf", "social": "DAEMONS-social-manual.pdf",
        "tiiny": "DAEMONS-tiiny-manual.pdf", "word": "DAEMONS-etymology.pdf", "textbook": "DAEMONS-textbook.pdf",
        "companion": "DAEMONS-companion-manual.pdf"}
# the third book on the game's screen (app/ui/bookPicture.tsx ON_COVER and BAND, measured 2026-11-05/06)
ON_COVER = {"hermetic": (50, 4, 188, 152), "eudaimon": (50, 4, 193, 154), "unity": (6, 4, 191, 154)}
BAND = {"hermetic": (118, 18.5, 34, "#FFF7F7", "#846B94"), "eudaimon": (117, 18.5, 34, "#FFF7DE", "#8CADEF"),
        "unity": (97, 17.5, 33, "#FFF7E7", "#A58C84")}


def font(size, face=1):
    return ImageFont.truetype(MENLO, size, index=face)


def spaced(d, text, f, cx, y, colour, spacing=1.0, anchor_mid=True):
    """`text` centred on cx, its letters `spacing` apart; y the top (or the middle when anchor_mid)."""
    widths = [d.textlength(c, font=f) for c in text]
    x = cx - (sum(widths) + spacing * max(0, len(text) - 1)) / 2
    if anchor_mid:
        top, bottom = f.getbbox("H")[1], f.getbbox("H")[3]
        y = y - (top + bottom) / 2
    for c, cw in zip(text, widths):
        d.text((x, y), c, font=f, fill=colour)
        x += cw + spacing


def tall(im, smooth):
    """The picture at H pixels tall: whole multiples kept square when it is pixel art."""
    if smooth:
        return im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    k = H / im.height
    if abs(k - round(k)) < 1e-6:
        return im.resize((im.width * round(k), H), Image.NEAREST)
    big = im.resize((im.width * int(k + 1), im.height * int(k + 1)), Image.NEAREST)
    return big.resize((round(im.width * k), H), Image.LANCZOS)


# -- the printed books -----------------------------------------------------------------------------------------------

def printed(pdf):
    import fitz
    path = os.path.join(ROOT, "docs", pdf)
    if not os.path.exists(path):
        return None
    page = fitz.open(path)[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(H * 2 / page.rect.height, H * 2 / page.rect.height), alpha=False)
    return tall(Image.frombytes("RGB", (pix.width, pix.height), pix.samples), smooth=True)


# -- the game's books ------------------------------------------------------------------------------------------------

def lettered_wiki(which):
    import covers                                    # wiki/covers.py: the GUIDE and THE SUBTLE LAYER, at 3x
    return tall(getattr(covers, which)(), smooth=True)


def third(book):
    p = os.path.join(ART, f"{book}_cover.png")
    if not os.path.exists(p):
        return None
    t = json.load(open(os.path.join(DATA, f"{book}.json"), encoding="utf-8"))
    x0, y0, x1, y1 = ON_COVER[book]
    k = 3
    im = Image.open(p).convert("RGB").crop((x0, y0, x1 + 1, y1 + 1))
    im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    d = ImageDraw.Draw(im)
    cx, ty, sy, ink, faint = BAND[book]
    spaced(d, t.get("title", ""), font(9 * k), (cx - x0) * k, (ty - y0) * k, ink, 0.5 * k)
    if t.get("subtitle"):
        spaced(d, t["subtitle"].upper(), font(8 * k, 0), (cx - x0) * k, (sy - y0) * k, faint, 0.5 * k)
    return tall(im, smooth=True)


#  T-533: THE ORIGIN OF A DAEMON on the game's screen (tools/origin_art.py cover): the book at x 48..191, y 4..154, its
#  title in two lines whose caps the game letters on rows 17..23 and 31..37, centred on x 120, in its C_CHALK
ORIGIN_COVER = (48, 4, 191, 154)
ORIGIN_TITLE = ((20, "THE ORIGIN"), (34, "OF A DAEMON"))


def origin():
    p = os.path.join(ART, "origin_cover.png")
    if not os.path.exists(p):
        return None
    x0, y0, x1, y1 = ORIGIN_COVER
    k = 3
    im = Image.open(p).convert("RGB").crop((x0, y0, x1 + 1, y1 + 1))
    im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for y, line in ORIGIN_TITLE:
        spaced(d, line, font(9 * k), (120 - x0) * k, (y - y0) * k, "#F7EFDE", 0.5 * k)
    return tall(im, smooth=True)


def school():
    return tall(Image.open(os.path.join(ART, "textbook_cover.png")).convert("RGB"), smooth=True)


# -- the three the player writes: cloth boards, gilt, the game's own pictures ---------------------------------------

W1, H1 = 108, 160                                    # drawn at the game's scale, then 2x


def boards(cloth, seed):
    """A cloth-bound board: a little weave, the spine's hinge, a gilt double rule, gilt corners."""
    rnd = random.Random(seed)
    im = Image.new("RGB", (W1, H1), cloth)
    px = im.load()
    r0, g0, b0 = Image.new("RGB", (1, 1), cloth).getpixel((0, 0))
    for y in range(H1):
        for x in range(W1):
            n = rnd.randint(-7, 7) + (3 if (x + y) % 4 == 0 else 0)
            px[x, y] = (max(0, min(255, r0 + n)), max(0, min(255, g0 + n)), max(0, min(255, b0 + n)))
    d = ImageDraw.Draw(im)
    dark = tuple(int(c * 0.62) for c in (r0, g0, b0))
    d.rectangle((0, 0, 7, H1), fill=dark)                       # the hinge
    d.line((8, 0, 8, H1), fill=tuple(int(c * 1.25) if c * 1.25 < 255 else 255 for c in (r0, g0, b0)))
    gold, deep = (214, 178, 96), (150, 112, 48)
    d.rectangle((13, 6, W1 - 7, H1 - 7), outline=deep)
    d.rectangle((15, 8, W1 - 9, H1 - 9), outline=gold)
    for (x, y, sx, sy) in ((15, 8, 1, 1), (W1 - 9, 8, -1, 1), (15, H1 - 9, 1, -1), (W1 - 9, H1 - 9, -1, -1)):
        for i in range(6):                                        # a corner fleuron
            d.point((x + sx * i, y + sy * (5 - i)), fill=gold)
        d.point((x + sx * 2, y + sy * 2), fill=gold)
    return im


def gilt_title(im, title, sub=None):
    d = ImageDraw.Draw(im)
    cx = (im.width + 16) / 2                                      # centred on the board, right of the hinge
    for dx, dy, c in ((1, 1, (70, 50, 20)), (0, 0, (236, 204, 128))):
        spaced(d, title, font(19), cx + dx, 42 + dy, c, 2.2)
    if sub:
        spaced(d, sub, font(11, 2), cx, 64, (226, 206, 160), 0.6)
    return im


def paste_k(base, sprite, x, y, k):
    s = sprite.convert("RGBA").resize((sprite.width * k, sprite.height * k), Image.NEAREST)
    base.paste(s, (x, y), s)


def notebook():
    im = boards((122, 90, 46), 1)
    d = ImageDraw.Draw(im)
    d.rectangle((W1 - 22, 74, W1 - 18, H1), fill=(58, 36, 22))   # the elastic band, below the title
    raw = Image.open(os.path.join(GBA, "graphics/items/icons/notebook.png"))
    icon = raw.convert("RGBA")
    if raw.mode == "P":                                          # the palette's first colour is the clear one
        icon.putdata([(0, 0, 0, 0) if raw.getpixel((x, y)) == 0 else icon.getpixel((x, y))
                      for y in range(raw.height) for x in range(raw.width)])
    paste_k(im, icon, (W1 + 8) // 2 - icon.width, 82, 2)
    big = im.resize((W1 * 2, H1 * 2), Image.NEAREST)
    return tall(gilt_title(big, "NOTEBOOK", "the pages you found"), smooth=False)


def songbook():
    im = boards((45, 106, 116), 2)
    d = ImageDraw.Draw(im)
    top = 92
    for i in range(5):                                           # the staff
        d.line((20, top + i * 5, W1 - 12, top + i * 5), fill=(214, 178, 96))
    notes = Image.open(os.path.join(ART, "play_notes.png")).convert("RGBA")   # twelve 16x16, top to bottom
    steps = (4, 2, 3, 1, 2, 0, 1)
    for i, s in enumerate(steps):
        n = notes.crop((0, (i * 2 % 12) * 16, 16, (i * 2 % 12) * 16 + 16))
        n = n.resize((10, 10), Image.NEAREST)
        im.paste(n, (22 + i * 11, top - 4 + s * 3), n)
    big = im.resize((W1 * 2, H1 * 2), Image.NEAREST)
    return tall(gilt_title(big, "SONGBOOK", "the songs you learned"), smooth=False)


def stream():
    im = boards((61, 79, 138), 3)
    d = ImageDraw.Draw(im)
    import math
    pts = [(int((W1 + 8) / 2 + 22 * math.sin(y / 13.0)), y) for y in range(78, H1 - 12)]
    for w, c in ((9, (92, 120, 196)), (5, (128, 160, 226)), (1, (190, 210, 246))):
        for x, y in pts:
            d.line((x - w // 2, y, x + w // 2, y), fill=c)
    for i in range(8):                                           # the eight MARKS, carried down it
        m = Image.open(os.path.join(ART, f"mark_{i + 1}.png")).convert("RGBA")
        x, y = pts[min(len(pts) - 1, 2 + i * 9)]
        side = -1 if i % 2 == 0 else 1
        m = m.resize((9, 9), Image.NEAREST)
        light = Image.new("RGBA", m.size, (236, 224, 190, 255))
        light.putalpha(m.split()[3])
        im.paste(light, (x + side * 13 - 4, y - 4), light)
    big = im.resize((W1 * 2, H1 * 2), Image.NEAREST)
    return tall(gilt_title(big, "STREAM", "every lesson opened"), smooth=False)


def covers():
    out = {}
    for k, pdf in PDFS.items():
        im = printed(pdf)
        if im is not None:
            out[k] = im
    out["guide"] = lettered_wiki("guide")
    out["subtle"] = lettered_wiki("subtle")
    for b in ON_COVER:
        im = third(b)
        if im is not None:
            out[b] = im
    im = origin()                                    # T-533
    if im is not None:
        out["origin"] = im
    out["school"] = school()
    out["notebook"] = notebook()
    out["songbook"] = songbook()
    out["stream"] = stream()
    return out


def png(im):
    b = io.BytesIO()
    im.convert("RGB").save(b, "PNG", optimize=True)
    return b.getvalue()


def main(only=None):
    write = "--write" in sys.argv
    changed = []
    for name, im in covers().items():
        if only and name not in only:
            continue
        path = os.path.join(OUT, f"{name}.png")
        body = png(im)
        if not os.path.exists(path) or open(path, "rb").read() != body:
            changed.append(f"{name} ({im.width}x{im.height})")
            if write:
                os.makedirs(OUT, exist_ok=True)
                open(path, "wb").write(body)
    if not changed:
        print("  shelf covers: companion/server/data/art/books/ agrees")
    else:
        print(f"  shelf covers: {'wrote' if write else 'would write'} " + ", ".join(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())

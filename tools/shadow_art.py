#!/usr/bin/env python3
"""THE SPELL LEFT RUNNING's pictures for the game's reader (T-606, DRAFT; the user, 2026-11-22: "Yes, draw them").

Twenty-four pictures, one for each entry of docs/shadow-book.md, the cover and the bag icon, every pixel one of the
book's sixteen palette roles (gensubtle.py's SHADOW_PALETTE: the PDF's parchment, the hat's night, the virtues' gold
and the well's water). Three kinds:

  the plates    the PDF's ComfyUI plates (docs/manual-shadow/art/drafts/plate_*.png), brought down to the 96x88 box and
                dithered into the book's ramp, a hair of gold round each: an engraving with two spot colours
  the brooms    the seven daemons of the week, their own pixels mapped to the roles, the day's sign in gold above
                them and the seven lights below with the day's lit
  the lessons   the PDF's diagrams redrawn small in code, wordless (the companion's copy holds nothing of the game's
                font, so no picture is lettered; only the cover is, and the companion's cover is not)

gensubtle.py calls SPRITES[key](rgb8) for the shadow book (a list of frames), cover(rgb8) and icon(rgb8), so a palette
change carries. NOTHING HERE WRITES INTO THE GAME: gensubtle --book shadow draws them in once BOOK_SHADOW is wired.

    python3 tools/shadow_art.py OUT_DIR      # every picture as its own PNG, the cover, the icon, and a contact sheet
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DRAFTS = os.path.join(ROOT, "docs", "manual-shadow", "art", "drafts")
DAEMONS = os.path.join(ROOT, "gfx", "daemons")
W, H = 96, 88

# the ramp a plate is dithered into, parchment to night, and its two spot colours
PLATE_ROLES = ["C_PAPER", "C_SHADOW", "C_EDGE", "C_CHALK_FAINT", "C_FAINT", "C_EDGE_DARK", "C_INK", "C_SLATE",
               "C_RULE", "C_MARGIN", "C_RING"]
SPRITE_ROLES = PLATE_ROLES + ["C_FRAME"]


def _canvas(c, role="C_PAPER", w=W, h=H):
    im = Image.new("RGB", (w, h), c[role])
    return im, ImageDraw.Draw(im)


def _palette_image(c, roles):
    pal = Image.new("P", (1, 1))
    flat = [v for r in roles for v in c[r]]
    pal.putpalette(flat + flat[:3] * (256 - len(roles)))
    return pal


def _to_roles(im, c, roles, dither):
    """IM's colours mapped to the nearest of ROLES (Floyd-Steinberg when DITHER), as exact role colours."""
    q = im.convert("RGB").quantize(palette=_palette_image(c, roles),
                                   dither=Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE)
    return q.convert("RGB")


# ---------------------------------------------------------------- the plates
def _plate(name):
    def draw(c):
        src = Image.open(os.path.join(DRAFTS, "plate_%s.png" % name)).convert("RGB")
        h = round(src.width * (H - 2) / (W - 2))
        top = max(0, (src.height - h) // 2)
        src = src.crop((0, top, src.width, top + h)).resize((W - 2, H - 2), Image.LANCZOS)
        src = ImageEnhance.Contrast(src).enhance(1.18)
        src = ImageEnhance.Sharpness(src).enhance(1.4)
        pic = _to_roles(src, c, PLATE_ROLES, dither=True)
        im, d = _canvas(c, "C_RULE")
        im.paste(pic, (1, 1))
        return [im]
    draw.__name__ = "plate_" + name
    return draw


# ---------------------------------------------------------------- the day signs, small (vision 9.21's week table)
def sign(d, c, kind, x, y, role="C_RULE", flip=False):
    """A day's sign in a 14x14 box at (x, y); FLIP turns it over, as its shadow's."""
    def P(px, py):
        return (x + (13 - px if flip else px), y + (13 - py if flip else py))

    def B(a, b):                                    # a box from two corners, whichever way round the flip left them
        (ax, ay), (bx, by) = P(*a), P(*b)
        return [min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)]
    col = c[role]
    if kind == "dome":
        pts = [P(1 + i, 10 - round(7 * math.sin(math.pi * i / 12))) for i in range(13)]
        d.line(pts, fill=col); d.line([P(1, 11), P(13, 11)], fill=col)
    elif kind == "beam":
        d.line([P(0, 4), P(13, 4)], fill=col, width=2); d.polygon([P(6, 5), P(3, 12), P(10, 12)], outline=col)
    elif kind == "bowl":
        pts = [P(1 + i, 3 + round(7 * math.sin(math.pi * i / 12))) for i in range(13)]
        d.line(pts, fill=col, width=2); d.line([P(0, 3), P(13, 3)], fill=col)
    elif kind == "climb":
        d.line([P(1, 12), P(4, 12), P(4, 9), P(7, 9), P(7, 6), P(10, 6), P(10, 3), P(13, 3)], fill=col, width=1)
    elif kind == "knot":
        d.line([P(4, 1), P(4, 7), P(7, 11), P(10, 7), P(10, 1)], fill=col)
        d.line([P(4, 7), P(10, 9)], fill=col); d.line([P(10, 7), P(4, 9)], fill=col)
    elif kind == "arc":
        pts = [P(1 + i, 10 - round(7 * math.sin(math.pi * i / 12))) for i in range(13)]
        d.line(pts, fill=col, width=2); d.rectangle(B((6, 9), (7, 10)), fill=col)
    elif kind == "stem":
        d.line([P(3, 13), P(3, 8), P(5, 4), P(8, 3), P(11, 5)], fill=col, width=1)
        d.ellipse(B((10, 5), (13, 8)), fill=col)


def lights(d, c, lit, y=80):
    """The seven lights, the day's lit."""
    for k in range(7):
        x = 24 + k * 8
        if k == lit:
            d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=c["C_MARGIN"], outline=c["C_RULE"])
        else:
            d.ellipse((x - 1, y - 1, x + 1, y + 1), outline=c["C_CHALK_FAINT"])


# ---------------------------------------------------------------- the brooms of the week
def _sprite(name, scale=1):
    s = Image.open(os.path.join(DAEMONS, "%s_front.png" % name)).convert("RGBA")
    if scale != 1:
        s = s.resize((s.width // scale, s.height // scale), Image.NEAREST)
    return s


def _paste_daemon(im, c, s, x, y):
    rgb = _to_roles(s.convert("RGB"), c, SPRITE_ROLES, dither=False)
    im.paste(rgb, (x, y), s.split()[3].point(lambda a: 255 if a > 127 else 0))


DAY = {"ping": (0, "dome"), "overflow": (1, "beam"), "keeper": (2, "bowl"), "blocking": (3, "climb"),
       "sentinel": (4, "knot"), "tracer": (5, "arc"), "supervisor": (6, "stem")}


def _broom(name):
    def draw(c):
        im, d = _canvas(c)
        lit, kind = DAY[name]
        d.ellipse((26, 66, 70, 74), fill=c["C_SHADOW"])
        _paste_daemon(im, c, _sprite(name), 16, 6)
        if name == "keeper":                         # and DEEPWELL, which is never full
            _paste_daemon(im, c, _sprite("deepwell", 2), 62, 40)
        sign(d, c, kind, 4, 4)
        sign(d, c, kind, 78, 4, "C_CHALK_FAINT", flip=True)
        lights(d, c, lit)
        return [im]
    draw.__name__ = "broom_" + name
    return draw


# ---------------------------------------------------------------- the small drawings
def hat(d, c, x, y, s=1.0):
    """The hat: a wide brim and a tall crown, two stars."""
    ink, star = c["C_INK"], c["C_MARGIN"]
    d.ellipse((x - 16 * s, y - 3 * s, x + 16 * s, y + 3 * s), fill=ink)
    d.polygon([(x - 9 * s, y - 1 * s), (x + 4 * s, y - 30 * s), (x + 9 * s, y - 1 * s)], fill=ink)
    d.point([(round(x), round(y - 10 * s)), (round(x + 3 * s), round(y - 19 * s))], fill=star)


def broom(d, c, x, y, arms=False, lean=0, role="C_INK"):
    """A broom standing at (x, y), the foot of its bristles; arms if a spell has given it some."""
    col = c[role]
    d.line((x + lean, y - 24, x, y - 8), fill=c["C_EDGE_DARK"], width=1)
    d.polygon([(x - 4, y), (x - 2, y - 8), (x + 2, y - 8), (x + 4, y)], fill=c["C_RULE"], outline=col)
    if arms:
        d.line((x, y - 17, x - 6, y - 12), fill=col); d.line((x, y - 17, x + 6, y - 12), fill=col)
        d.rectangle((x - 9, y - 12, x - 5, y - 8), fill=c["C_RING"]); d.rectangle((x + 5, y - 12, x + 9, y - 8), fill=c["C_RING"])


def well(d, c, x, y, level, done=False, spill=False):
    """A well 18 wide at (x, y) top-left, LEVEL of 0..1 full; DONE draws its full mark in gold."""
    d.rectangle((x, y, x + 18, y + 22), fill=c["C_PAPER"], outline=c["C_INK"])
    h = round(20 * level)
    if h:
        d.rectangle((x + 1, y + 21 - h, x + 17, y + 21), fill=c["C_RING"])
    d.line((x - 3, y, x + 21, y), fill=c["C_INK"], width=2)
    if done:
        d.line((x - 4, y + 2, x + 22, y + 2), fill=c["C_MARGIN"])
    if spill:
        d.line((x - 1, y + 1, x - 4, y + 12), fill=c["C_RING"]); d.line((x + 19, y + 1, x + 22, y + 12), fill=c["C_RING"])


def arrow(d, c, x0, y0, x1, y1, role="C_INK"):
    d.line((x0, y0, x1, y1), fill=c[role])
    a = math.atan2(y1 - y0, x1 - x0)
    for da in (2.6, -2.6):
        d.line((x1, y1, x1 + 4 * math.cos(a + da), y1 + 4 * math.sin(a + da)), fill=c[role])


def hat_peg(c):
    """HOW TO READ: the hat on its peg by the door."""
    im, d = _canvas(c)
    d.rectangle((62, 8, 88, 80), fill=c["C_EDGE"], outline=c["C_EDGE_DARK"])        # the door
    d.rectangle((66, 12, 84, 44), outline=c["C_CHALK_FAINT"]); d.rectangle((66, 48, 84, 76), outline=c["C_CHALK_FAINT"])
    d.ellipse((80, 44, 82, 46), fill=c["C_RULE"])
    d.line((0, 80, 95, 80), fill=c["C_FAINT"])
    d.rectangle((30, 30, 40, 33), fill=c["C_EDGE_DARK"])                            # the peg
    hat(d, c, 34, 60, 1.0)
    d.line((34, 33, 36, 32), fill=c["C_EDGE_DARK"])
    return [im]


def spellcard(c):
    """LIKE A DAEMON: the spell card, its fifth line the one left blank, the hat in its corner."""
    im, d = _canvas(c)
    d.rectangle((10, 8, 86, 80), fill=c["C_SHADOW"], outline=c["C_INK"])
    for k in range(6):
        y = 22 + k * 10
        if k == 4:
            for x in range(36, 80, 4):
                d.line((x, y - 4, x + 1, y - 4), fill=c["C_RULE"]); d.line((x, y + 2, x + 1, y + 2), fill=c["C_RULE"])
            d.line((36, y - 4, 36, y + 2), fill=c["C_RULE"]); d.line((80, y - 4, 80, y + 2), fill=c["C_RULE"])
            d.rectangle((16, y - 2, 30, y), fill=c["C_RULE"])
        else:
            d.rectangle((16, y - 2, 30, y), fill=c["C_FAINT"])
            d.line((36, y + 1, 80, y + 1), fill=c["C_CHALK_FAINT"])
    hat(d, c, 74, 19, 0.45)
    return [im]


def done(c):
    """NO DONE: the loop, and the well with its end written in gold."""
    im, d = _canvas(c)
    d.arc((10, 16, 46, 52), 200, 520, fill=c["C_INK"], width=2)
    arrow(d, c, 38, 46, 42, 42)
    broom(d, c, 28, 44, arms=True)
    well(d, c, 60, 30, 0.95, done=True)
    d.line((0, 76, 95, 76), fill=c["C_FAINT"])
    return [im]


def axe_word(c):
    """THE AXE: above, a broom split makes two; below, the word puts one back in its corner."""
    im, d = _canvas(c)
    broom(d, c, 14, 36); arrow(d, c, 22, 24, 34, 24)
    d.line((40, 30, 46, 18), fill=c["C_EDGE_DARK"], width=2); d.polygon([(44, 16), (51, 18), (46, 22)], fill=c["C_FAINT"])
    arrow(d, c, 54, 24, 64, 24); broom(d, c, 72, 36, arms=True); broom(d, c, 86, 36, arms=True)
    d.line((6, 44, 90, 44), fill=c["C_CHALK_FAINT"])
    broom(d, c, 14, 80, arms=True); arrow(d, c, 24, 68, 56, 68, "C_RULE")
    d.line((66, 82, 88, 82), fill=c["C_INK"]); d.line((88, 82, 88, 52), fill=c["C_INK"])
    broom(d, c, 82, 81, lean=4)
    return [im]


def gate(c):
    """THE RACE: the brooms queue at a gate, and one goes through to look and pour."""
    im, d = _canvas(c)
    for k, x in enumerate((10, 22, 34)):
        broom(d, c, x, 66, arms=True)
    d.rectangle((44, 30, 46, 70), fill=c["C_RULE"]); d.rectangle((56, 30, 58, 70), fill=c["C_RULE"])
    d.line((44, 34, 58, 34), fill=c["C_MARGIN"], width=2)
    broom(d, c, 64, 66, arms=True)
    well(d, c, 72, 44, 0.7)
    d.line((0, 72, 95, 72), fill=c["C_FAINT"])
    return [im]


def orphan(c):
    """PUT BACK: a routine whose parent ended, adopted by the first process."""
    im, d = _canvas(c)
    d.rectangle((30, 6, 66, 20), fill=c["C_SLATE"], outline=c["C_INK"])
    hat(d, c, 48, 17, 0.32)
    for x in range(14, 50, 4):
        d.line((x, 36, x + 1, 36), fill=c["C_FAINT"]); d.line((x, 48, x + 1, 48), fill=c["C_FAINT"])
    d.line((14, 36, 14, 48), fill=c["C_FAINT"]); d.line((50, 36, 50, 48), fill=c["C_FAINT"])
    d.rectangle((14, 64, 50, 78), fill=c["C_SHADOW"], outline=c["C_INK"])
    broom(d, c, 32, 76)
    for y in range(50, 64, 3):
        d.point((32, y), fill=c["C_FAINT"])
    d.line((52, 70, 76, 70), fill=c["C_RULE"]); d.line((76, 70, 76, 22), fill=c["C_RULE"])
    arrow(d, c, 76, 22, 68, 14, "C_RULE")
    return [im]


def over(c):
    """OVER: the seven signs, upright for the virtue and turned over for the shadow."""
    im, d = _canvas(c)
    kinds = ["dome", "beam", "bowl", "climb", "knot", "arc", "stem"]
    for k, kind in enumerate(kinds):
        x = 2 + k * 13
        sign(d, c, kind, x, 18)
        sign(d, c, kind, x, 54, "C_FAINT", flip=True)
    d.line((4, 44, 92, 44), fill=c["C_CHALK_FAINT"])
    return [im]


def order(c):
    """THE ORDER: five scribes round a table, the quills numbered by their lengths, one scribe writing."""
    im, d = _canvas(c)
    cx, cy, r = 48, 44, 30
    d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=c["C_SHADOW"], outline=c["C_FAINT"])
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse((sx - 5, sy - 5, sx + 5, sy + 5), fill=c["C_MARGIN"] if k == 0 else c["C_PAPER"], outline=c["C_INK"])
        qa = a + math.pi / 5
        qx, qy = cx + 14 * math.cos(qa), cy + 14 * math.sin(qa)
        n = k + 1                                         # the quill's number, as notches along it
        d.line((qx - 4 * math.cos(qa + 1.4), qy - 4 * math.sin(qa + 1.4), qx + 4 * math.cos(qa + 1.4),
                qy + 4 * math.sin(qa + 1.4)), fill=c["C_INK"], width=2)
        for j in range(n):
            px_, py_ = qx + (j - (n - 1) / 2) * 2.2 * math.cos(qa), qy + (j - (n - 1) / 2) * 2.2 * math.sin(qa)
            d.point((round(px_ + 4 * math.cos(qa)), round(py_ + 4 * math.sin(qa))), fill=c["C_RULE"])
    return [im]


SPRITES = {
    "desk": _plate("desk"), "hat_peg": hat_peg, "tower": _plate("tower"), "first_spell": _plate("firstspell"),
    "many": _plate("many"), "axe": _plate("axe"), "race": _plate("race"), "word": _plate("word"),
    "spellcard": spellcard, "done": done, "axe_word": axe_word, "gate": gate, "orphan": orphan, "over": over,
    "ping": _broom("ping"), "overflow": _broom("overflow"), "keeper": _broom("keeper"), "blocking": _broom("blocking"),
    "sentinel": _broom("sentinel"), "tracer": _broom("tracer"), "supervisor": _broom("supervisor"),
    "quills": _plate("quills"), "order": order, "dusk": _plate("dusk"),
}


# ---------------------------------------------------------------- the cover and the icon
def cover(c, letters=True, text=None):
    """The whole window, 240x160: the hat on its peg over seven brooms and their seven lights, water at the foot.
    TEXT(im, s, x, y, role, small) letters the title in the game's font; the companion's cover has none."""
    im, d = _canvas(c, "C_SLATE", 240, 160)
    d.line((0, 74, 239, 74), fill=c["C_INK"])                                              # the far shore
    for x, y in ((18, 14), (44, 30), (202, 12), (226, 34), (170, 22), (30, 56), (214, 60), (150, 8), (84, 16)):
        d.point((x, y), fill=c["C_CHALK_FAINT"])
    d.ellipse((24, 18, 40, 34), fill=c["C_CHALK"]); d.ellipse((29, 15, 45, 31), fill=c["C_SLATE"])   # the moon
    d.rectangle((112, 14, 134, 17), fill=c["C_EDGE_DARK"]); d.rectangle((112, 12, 114, 19), fill=c["C_EDGE_DARK"])   # the peg
    d.polygon([(110, 62), (126, 17), (134, 62)], fill=c["C_INK"], outline=c["C_FAINT"])        # the hat, hung by its tip
    d.ellipse((96, 58, 148, 66), fill=c["C_INK"], outline=c["C_FAINT"])
    d.polygon([(111, 60), (126, 18), (133, 60)], fill=c["C_INK"])
    for x, y in ((123, 36), (127, 27), (119, 50), (129, 46)):
        d.point((x, y), fill=c["C_MARGIN"])
    for k in range(7):
        x = 48 + k * 24
        d.ellipse((x - 2, 80, x + 2, 84), fill=c["C_MARGIN"])
        d.line((x, 90, x, 108), fill=c["C_EDGE"])
        d.polygon([(x - 5, 118), (x - 3, 108), (x + 3, 108), (x + 5, 118)], fill=c["C_RULE"])
    d.rectangle((0, 120, 239, 159), fill=c["C_INK"])
    for y in (124, 130):
        for x in range(0, 240, 12):
            d.line((x + (y % 12), y, x + (y % 12) + 5, y), fill=c["C_RING"])
    if letters and text:
        text(im, "THE SPELL LEFT RUNNING", None, 134, "C_CHALK", False)
        text(im, "A BOOK OF SHADOWS", None, 148, "C_CHALK_FAINT", True)
    return im


def icon(c):
    """The bag's icon, 24x24 on index 0: a closed book in the night's boards, a gold hat on its face."""
    im = Image.new("RGB", (24, 24), c["C_NONE"])
    d = ImageDraw.Draw(im)
    d.rectangle((4, 3, 19, 21), fill=c["C_SLATE"], outline=c["C_INK"])
    d.line((20, 4, 20, 20), fill=c["C_PAPER"]); d.line((21, 5, 21, 20), fill=c["C_CHALK_FAINT"])
    d.line((5, 4, 5, 20), fill=c["C_EDGE_DARK"])
    d.ellipse((7, 15, 17, 18), fill=c["C_RULE"])
    d.polygon([(9, 16), (13, 6), (15, 16)], fill=c["C_RULE"])
    d.point((13, 10), fill=c["C_MARGIN"])
    return im


# ---------------------------------------------------------------- report, and a contact sheet
def roles_only(im, c, allowed):
    cols = {c[r] for r in allowed}
    bad = {px for px in im.getdata() if px not in cols}
    return bad


def main():
    sys.path.insert(0, HERE)
    import gensubtle as gs
    import genguide as g
    gs.use("shadow")
    c = gs.RGB8
    out = sys.argv[1] if len(sys.argv) > 1 else None
    font = {False: Image.open(os.path.join(g.GBA, "graphics/fonts/latin_normal.png")),
            True: Image.open(os.path.join(g.GBA, "graphics/fonts/latin_small.png"))}

    def text(im, s, x, y, role, small):
        w = g.WS if small else g.WN
        cw, per = (8, 32) if small else (16, 16)
        if x is None:
            x = (im.width - g.width(s, small)) // 2
        px = im.load()
        for ch in g.c_string(s):
            if ch not in g.CM:
                continue
            k = g.CM[ch]
            ox, oy = (k % per) * cw, (k // per) * 16
            for yy in range(16):
                for xx in range(w[k]):
                    if font[small].getpixel((ox + xx, oy + yy)) == 1:
                        px[x + xx, y + yy] = c[role]
            x += w[k]

    allowed = [n for n, _ in gs.PALETTE if n not in ("C_NONE", "C_COVER")]
    order_keys = [e["sprite"] for s in gs.parse() for e in s["entries"]]
    missing = [k for k in order_keys if k not in SPRITES]
    drawn = {}
    for k in order_keys:
        if k in missing:
            continue
        try:
            frames = SPRITES[k](c)
        except FileNotFoundError:                   # a plate not yet drawn
            missing.append(k)
            continue
        for f in frames:
            assert f.size == (W, H), (k, f.size)
            bad = roles_only(f, c, allowed)
            if bad:
                raise SystemExit("shadow_art: %s draws %d colours that are no palette role" % (k, len(bad)))
        drawn[k] = frames
    cov = cover(c, True, text)
    ic = icon(c)
    if roles_only(cov, c, allowed + ["C_COVER"]) or roles_only(ic, c, allowed + ["C_NONE"]):
        raise SystemExit("shadow_art: the cover or the icon draws a colour that is no palette role")
    print("shadow_art: %d of %d pictures drawn%s; the cover and the icon" % (len(drawn), len(order_keys),
          (", missing: " + ", ".join(missing)) if missing else ""))
    if not out:
        return 0
    os.makedirs(out, exist_ok=True)
    for k, frames in drawn.items():
        frames[0].save(os.path.join(out, "%s.png" % k))
    cov.save(os.path.join(out, "cover.png")); ic.save(os.path.join(out, "icon.png"))
    Z, cols = 2, 6
    cell_w, cell_h = W * Z + 10, H * Z + 10
    rows = (len(order_keys) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w + 10, rows * cell_h + 10 + 160 * Z + 20), (40, 42, 52))
    for i, k in enumerate(order_keys):
        if k in drawn:
            sheet.paste(drawn[k][0].resize((W * Z, H * Z), Image.NEAREST), (10 + (i % cols) * cell_w, 10 + (i // cols) * cell_h))
    y = 10 + rows * cell_h + 10
    sheet.paste(cov.resize((240 * Z, 160 * Z), Image.NEAREST), (10, y))
    sheet.paste(ic.resize((24 * 6, 24 * 6), Image.NEAREST), (10 + 240 * Z + 20, y))
    sheet.save(os.path.join(out, "_sheet.png"))
    print("  wrote %d pictures, the cover, the icon and _sheet.png into %s" % (len(drawn), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

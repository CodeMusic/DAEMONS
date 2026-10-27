#!/usr/bin/env python3
"""THE SUBTLE LAYER's purple in the field (T-459; docs/psychic-routines-notes.md D4).

    python3 tools/gensense.py                 # report: the frames as text, the palette, the three checks
    python3 tools/gensense.py --sheet OUT.png # a review sheet: every frame enlarged, and a line in the dialogue's purple
    python3 tools/gensense.py --write         # engineGba/graphics/misc/subtle_sense.png + .pal, and menu_message.png

WHAT IT IS. Once THE SUBTLE LAYER is held, the follower notices first: now and then, standing still, a small ripple
rises from it and it turns toward something unfound within a screen, and a faint glint shows where it looks
(src/daemons_follower.c, Sense). Both are drawn here, in the book's own hue -- the user chose CONTEXT's purple, the
book's, over a softer violet of its own (2026-10-27) -- so the colours are gensubtle.py's C_RULE (CONTEXT's hue, the
ink), C_MARGIN (the hue lit) and C_INK (the book's pinkish white, a glint's heart), read from that file and never
typed twice.

    frames 0-3   the ripple: a ring on still water seen from the side, widening and thinning as it rises
    frames 4-6   the glint: a four-point catch of light, small to full (the follower plays 4 5 6 5 4)

Seven frames of 16x16 in one row (112x16), so gbagfx's -mwidth 2 -mheight 2 lays them out as frames 0..6. One OBJ
palette, loaded while they show and freed after: 0 transparent, 1 C_RULE, 2 C_MARGIN, 3 C_INK.

THE TEXT COLOUR. {COLOR PURPLE} (charmap.txt, 0A) prints in C_RULE in the field's dialogue box only: slot 10 of the
dialogue's palette, which new_menu_helpers.c's LoadStdWindowFrameGfx sets after loading stdpal_0. Slot 10 was a SECOND
white there (stdpal_0 holds 255 255 255 at 1 and at 10), so the frame gives it up: --write redraws menu_message.png's
264 pixels of 10 as 1, the same white, and nothing on any screen that loads that frame changes. stdpal_0.pal itself is
not touched, because the MAIL prints in slots 10 and 11 of it (mail.c sTextColor) and the trainer card loads its brain's
lobes into 10-15 of the same palette after the frame (trainer_card.c LoadBrainLobeColors). The shadow is the box's own
LIGHT_GRAY: the dialogue palette has one slot to spare, not two.

THE CHECKS, in report mode: the frames and palette on disk are what this draws; menu_message.png draws nothing in 10;
the RGB() in new_menu_helpers.c is C_RULE; charmap.txt names 0A PURPLE.

Drawn directly at 16x16, pixel by pixel, as every small icon in this project is (genemoji, genopusicon): a ring two
pixels across is a pixel decision, not a reduction.
"""
import math, os, re, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT_PNG = os.path.join(GBA, "graphics", "misc", "subtle_sense.png")
OUT_PAL = os.path.join(GBA, "graphics", "misc", "subtle_sense.pal")
FRAME_PNG = os.path.join(GBA, "graphics", "text_window", "menu_message.png")
MENU_C = os.path.join(GBA, "src", "new_menu_helpers.c")
CHARMAP = os.path.join(GBA, "charmap.txt")
WRITE = "--write" in sys.argv

FRAMES = 7
SECOND_WHITE, WHITE = 10, 1


def book_colour(role):
    """A palette role from gensubtle.py's PALETTE, as five-bit channels -- read from the file, so there is one hue."""
    src = open(os.path.join(ROOT, "tools", "gensubtle.py")).read()
    m = re.search(r'\("%s",\s*\((\d+),\s*(\d+),\s*(\d+)\)\)' % role, src)
    return tuple(int(v) for v in m.groups())


RULE, MARGIN, INK = book_colour("C_RULE"), book_colour("C_MARGIN"), book_colour("C_INK")


def eight(c):
    return tuple((v << 3) | (v >> 2) for v in c)


PAL = [(0, 0, 0), eight(RULE), eight(MARGIN), eight(INK)] + [(0, 0, 0)] * 12


def ring(px, cx, cy, rx, ry, colour, dashed=False):
    for k in range(360):
        if dashed and (k // 30) % 2:
            continue
        a = math.radians(k)
        x, y = int(round(cx + rx * math.cos(a))), int(round(cy + ry * math.sin(a)))
        if 0 <= x < 16 and 0 <= y < 16:
            px[x, y] = colour


def cross(px, cx, cy, arm, near):
    for d in range(1, arm + 1):
        c = 2 if d <= near else 1
        for x, y in ((cx + d, cy), (cx - d, cy), (cx, cy + d), (cx, cy - d)):
            px[x, y] = c
    px[cx, cy] = 3


def frame(n):
    im = Image.new("P", (16, 16), 0)
    px = im.load()
    cx, cy = 7, 8
    if n == 0:
        ring(px, cx, cy, 2, 1, 2)
    elif n == 1:
        ring(px, cx, cy, 4, 2, 1)
        px[cx, cy] = 2
    elif n == 2:
        ring(px, cx, cy, 6, 3, 1)
        ring(px, cx, cy, 3, 1, 2)
    elif n == 3:
        ring(px, cx, cy, 7, 3, 1, dashed=True)   # fading: the outer ring alone, broken
    elif n == 4:
        cross(px, cx, cy, 1, 1)
    elif n == 5:
        cross(px, cx, cy, 3, 1)
    elif n == 6:
        cross(px, cx, cy, 5, 2)
        for d in (2,):
            for x, y in ((cx + d, cy + d), (cx - d, cy - d), (cx + d, cy - d), (cx - d, cy + d)):
                px[x, y] = 1
    return im


def sheet_image():
    im = Image.new("P", (16 * FRAMES, 16), 0)
    for n in range(FRAMES):
        im.paste(frame(n), (16 * n, 0))
    im.putpalette([v for c in PAL for v in c])
    return im


def jasc(pal):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal)


def frame_without_second_white():
    """menu_message.png with its 10s drawn as 1s (the same white in stdpal_0), its own palette and depth kept."""
    im = Image.open(FRAME_PNG)
    out = im.point(lambda v: WHITE if v == SECOND_WHITE else v)
    out.putpalette(im.getpalette())
    return out


def checks():
    bad = []
    if list(Image.open(FRAME_PNG).getdata()).count(SECOND_WHITE):
        bad.append("menu_message.png still draws %d pixels in slot 10 (--write redraws them as 1)"
                   % list(Image.open(FRAME_PNG).getdata()).count(SECOND_WHITE))
    m = re.search(r"sSubtlePurple\[\]\s*=\s*\{\s*RGB\((\d+),\s*(\d+),\s*(\d+)\)", open(MENU_C).read())
    if not m:
        bad.append("new_menu_helpers.c has no sSubtlePurple")
    elif tuple(int(v) for v in m.groups()) != RULE:
        bad.append("new_menu_helpers.c's sSubtlePurple is RGB%s, gensubtle's C_RULE is %s" % (m.groups(), RULE))
    if not re.search(r"^PURPLE\s*=\s*0A\b", open(CHARMAP).read(), re.M):
        bad.append("charmap.txt does not name 0A PURPLE")
    return bad


def same_png(path, im):
    if not os.path.exists(path):
        return False
    old = Image.open(path)
    return old.size == im.size and list(old.getdata()) == list(im.getdata()) \
        and (old.getpalette() or [])[:48] == (im.getpalette() or [])[:48]


def report():
    names = {0: ".", 1: "#", 2: "+", 3: "@"}
    for n in range(FRAMES):
        f = frame(n).load()
        print("  frame %d (%s)" % (n, "ripple" if n < 4 else "glint"))
        for y in range(16):
            row = "".join(names[f[x, y]] for x in range(16))
            if row.strip("."):
                print("    " + row)
    print("  palette: 1 C_RULE %s  2 C_MARGIN %s  3 C_INK %s" % (RULE, MARGIN, INK))
    png = sheet_image()
    pal_same = os.path.exists(OUT_PAL) and open(OUT_PAL, newline="").read() == jasc(PAL)
    print("  %s: %s" % (os.path.relpath(OUT_PNG, ROOT), "unchanged" if same_png(OUT_PNG, png) else "would change"))
    print("  %s: %s" % (os.path.relpath(OUT_PAL, ROOT), "unchanged" if pal_same else "would change"))
    print("  %s: %s" % (os.path.relpath(FRAME_PNG, ROOT),
                        "unchanged" if same_png(FRAME_PNG, frame_without_second_white()) else "would change"))
    bad = checks()
    for b in bad:
        print("  ! " + b)
    if not bad:
        print("  the dialogue's purple is C_RULE, in slot 10, named PURPLE; the frame no longer draws there.")
    return 1 if bad else 0


def review_sheet(out):
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import genguide as G
    S = 8
    w = 16 * FRAMES * S + 16 * (FRAMES + 1)
    img = Image.new("RGB", (w, 16 * S + 32 + 120), (24, 20, 28))
    for n in range(FRAMES):
        tile = Image.new("RGB", (16, 16), (232, 232, 216))
        f, t = frame(n).load(), tile.load()
        for y in range(16):
            for x in range(16):
                if f[x, y]:
                    t[x, y] = PAL[f[x, y]]
        img.paste(tile.resize((16 * S, 16 * S), Image.NEAREST), (16 + n * (16 * S + 16), 16))
    box = Image.new("RGB", (240, 48), (248, 248, 248))
    d = box.load()
    px, _ = G.glyphs("ELM keeps looking")
    for (a, b) in px:
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            if d[8 + a + dx, 4 + b + dy] != eight(RULE):
                d[8 + a + dx, 4 + b + dy] = (213, 213, 205)
    for (a, b) in px:
        d[8 + a, 4 + b] = eight(RULE)
    ImageDraw.Draw(box).rectangle((0, 0, 239, 47), outline=(74, 115, 164))
    img.paste(box.resize((240 * 2, 48 * 2), Image.NEAREST), (16, 16 * S + 32))
    img.save(out)
    return out


def main():
    if "--sheet" in sys.argv:
        print("wrote", review_sheet(sys.argv[sys.argv.index("--sheet") + 1]))
        return 0
    if WRITE:
        sheet_image().save(OUT_PNG, bits=4)
        open(OUT_PAL, "w", newline="").write(jasc(PAL))
        fr = frame_without_second_white()
        if not same_png(FRAME_PNG, fr):
            fr.save(FRAME_PNG, bits=4)
        print("wrote", os.path.relpath(OUT_PNG, ROOT), os.path.relpath(OUT_PAL, ROOT), "and", os.path.relpath(FRAME_PNG, ROOT))
        for b in [b for b in checks() if "menu_message" not in b]:
            print("  ! " + b)
        return 0
    return report()


if __name__ == "__main__":
    sys.exit(main())

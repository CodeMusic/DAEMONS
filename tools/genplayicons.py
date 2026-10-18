#!/usr/bin/env python3
"""The HARP's and the FLUTE's bag icons (T-417, the user 2026-10-17: "real HARP and FLUTE icons"; DRAFT art).

    python3 tools/genplayicons.py            # report (and previews, 8x, in $DAEMONS_SCRATCH or .theatre/)
    python3 tools/genplayicons.py --write    # graphics/items/icons/{harp,play_flute}.png, their .pal, and the tables

Until now ITEM_HARP wore vanilla's YELLOW FLUTE and ITEM_FLUTE the POKe FLUTE. Each is now drawn here, by hand in
Python as genflute.py and genlyrebird.py drew theirs: the shapes are laid out at eight times the size (PIL's polygons
and lines), cut down to 24x24 by coverage, then shaded by which way each pixel faces and outlined -- so the drawing
is the geometry below, not a pixel list, and a change to it is a change of a number.

  HARP   a small frame harp in gold: a pillar on the left, the neck curving over the top, the soundbox running down
         the diagonal, six pale strings between neck and soundbox, a red bead at the crown (CONTENT's, given by the
         LYREBIRD outside CALLOW SCHOOL).
  FLUTE  a bamboo cane lying on the diagonal in the gold and olive of BREATHVERSE's flute (genflute.py): two node
         rings, the mouth hole and four finger holes, a highlight along its upper edge (CONTEXT's).

Each icon has a sixteen-colour palette of its own (index 0 transparent, vanilla's key grey), so it is palette-safe
by construction: the bag loads an item's palette with its icon. The tables (src/data/graphics/items.h,
include/graphics.h, src/data/item_icon_table.h) are written once and then only checked.
"""
import os, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
ICONS = os.path.join(GBA, "graphics/items/icons")
PALS = os.path.join(GBA, "graphics/items/icon_palettes")
ITEMS_H = os.path.join(GBA, "src/data/graphics/items.h")
GRAPHICS_H = os.path.join(GBA, "include/graphics.h")
TABLE = os.path.join(GBA, "src/data/item_icon_table.h")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))
S = 8          # drawn at 8x, then cut to 24x24
N = 24

#  index: 0 clear, 1 outline, 2 dark, 3 mid, 4 light, 5 highlight, 6 string / hole, 7 accent
HARP_PAL = [(180, 180, 180), (58, 36, 20), (150, 92, 30), (206, 148, 48), (240, 200, 92), (255, 240, 180),
            (222, 222, 230), (200, 48, 48)] + [(0, 0, 0)] * 8
FLUTE_PAL = [(180, 180, 180), (60, 66, 24), (122, 120, 40), (180, 166, 66), (224, 206, 110), (250, 240, 186),
             (70, 40, 24), (84, 80, 28)] + [(0, 0, 0)] * 8
OUTLINE, DARK, MID, LIGHT, HIGH, STRING, ACCENT = 1, 2, 3, 4, 5, 6, 7


def coverage(draw_fn):
    """A 24x24 mask: a pixel is in when half the 8x8 cell under it is."""
    big = Image.new("L", (N * S, N * S), 0)
    draw_fn(ImageDraw.Draw(big), lambda *p: [(x * S, y * S) for x, y in p])
    small = big.resize((N, N), Image.BOX)
    return [[small.getpixel((x, y)) >= 128 for x in range(N)] for y in range(N)]


def shade(mask, g):
    """Light from the upper left: a pixel whose upper or left neighbour is empty is light, lower or right dark."""
    for y in range(N):
        for x in range(N):
            if not mask[y][x]:
                continue
            up = y > 0 and mask[y - 1][x]
            left = x > 0 and mask[y][x - 1]
            down = y < N - 1 and mask[y + 1][x]
            right = x < N - 1 and mask[y][x + 1]
            g[y][x] = LIGHT if not (up and left) else DARK if not (down and right) else MID


def outline(g, keep=()):
    ink = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            if ink[y][x] == 0 and any(0 <= x + dx < N and 0 <= y + dy < N and ink[y + dy][x + dx] and
                                      ink[y + dy][x + dx] not in keep
                                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g[y][x] = OUTLINE


def harp():
    def frame(d, P):
        d.line(P((5.0, 4.5), (5.0, 21.0)), fill=255, width=int(2.2 * S))                  # the pillar
        d.line(P((4.0, 3.5), (8.0, 5.0), (12.0, 6.0), (15.0, 4.5), (18.5, 3.5), (20.0, 5.0)), fill=255,
               width=int(2.0 * S), joint="curve")                                              # the neck
        d.polygon(P((5.0, 20.0), (7.5, 21.5), (21.0, 6.5), (19.0, 4.5)), fill=255)             # the soundbox
        d.ellipse(P((3.5, 19.0), (8.5, 22.5)), fill=255)                                       # the foot
    mask = coverage(frame)
    g = [[0] * N for _ in range(N)]
    shade(mask, g)
    #  the strings: from under the neck straight down to the soundbox, every other column
    for x in (7, 9, 11, 13, 15, 17):
        y = 0
        while y < N and not mask[y][x]:
            y += 1
        while y < N and mask[y][x]:
            y += 1
        while y < N and not mask[y][x]:
            g[y][x] = STRING
            y += 1
    #  a highlight down the pillar, the crown's bead
    for y in range(6, 19):
        if g[y][5] in (MID, LIGHT):
            g[y][5] = HIGH
    g[3][4] = ACCENT
    g[2][4] = HIGH if g[2][4] else ACCENT
    outline(g, keep=(STRING,))
    return g


def flute():
    def cane(d, P):
        d.line(P((3.0, 20.5), (20.5, 3.0)), fill=255, width=int(3.8 * S))
    mask = coverage(cane)
    g = [[0] * N for _ in range(N)]
    shade(mask, g)
    #  along the axis: t from 0 (the foot, lower left) to 1 (the head, upper right)
    def at(t, off=0.0):
        x = 3.0 + 17.5 * t + off * 0.7
        y = 20.5 - 17.5 * t + off * 0.7
        return int(round(x)), int(round(y))
    for t in (0.12, 0.145, 0.86, 0.885):                 # the node rings: across the cane, two pixels thick
        for off in (-1.4, -0.7, 0.0, 0.7, 1.4):
            x, y = at(t, off)
            if mask[y][x]:
                g[y][x] = ACCENT
    for t in (0.30, 0.40, 0.50, 0.60, 0.76):             # four finger holes, and the mouth hole near the head
        x, y = at(t, -0.3)
        g[y][x] = STRING
    for t in [i / 40 for i in range(4, 38)]:             # a highlight along the upper edge
        x, y = at(t, -1.5)
        if 0 <= x < N and 0 <= y < N and g[y][x] in (MID, LIGHT):
            g[y][x] = HIGH
    outline(g)
    return g


def image(g, pal):
    im = Image.new("P", (N, N), 0)
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    im.putdata([c for row in g for c in row])
    return im


def jasc(pal):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal)


ICON_LIST = [("harp", "Harp", "ITEM_HARP", harp, HARP_PAL), ("play_flute", "PlayFlute", "ITEM_FLUTE", flute, FLUTE_PAL)]


def tables():
    """{path: new text} for the three tables, each change anchored on a line that must be there exactly once."""
    out = {}
    s = open(ITEMS_H, encoding="utf-8").read()
    want = "".join('\nconst u32 gItemIcon_%s[] = INCBIN_U32("graphics/items/icons/%s.4bpp.lz");   // T-417: DAEMONS tools/genplayicons.py'
                   '\nconst u32 gItemIconPalette_%s[] = INCBIN_U32("graphics/items/icon_palettes/%s.gbapal.lz");\n'
                   % (sym, f, sym, f) for f, sym, _, _, _ in ICON_LIST)
    if want not in s:
        anchor = 'const u32 gItemIconPalette_Guide[] = INCBIN_U32("graphics/items/icon_palettes/guide.gbapal.lz");\n'
        assert s.count(anchor) == 1, "items.h: the GUIDE's palette line is the anchor"
        s = s.replace(anchor, anchor + want)
    out[ITEMS_H] = s
    s = open(GRAPHICS_H, encoding="utf-8").read()
    want = "".join("extern const u32 gItemIcon_%s[];   // T-417\nextern const u32 gItemIconPalette_%s[];\n" % (sym, sym)
                   for _, sym, _, _, _ in ICON_LIST)
    if want not in s:
        anchor = "extern const u32 gItemIconPalette_Guide[];\n"
        assert s.count(anchor) == 1, "graphics.h: the GUIDE's palette extern is the anchor"
        s = s.replace(anchor, anchor + want)
    out[GRAPHICS_H] = s
    s = open(TABLE, encoding="utf-8").read()
    for f, sym, item, _, _ in ICON_LIST:
        lines = [l for l in s.split("\n") if l.lstrip().startswith("[%s]" % item)]
        assert len(lines) == 1, "item_icon_table.h: one row for %s" % item
        row = "    %-22s= {gItemIcon_%s, gItemIconPalette_%s},   // T-417: DAEMONS tools/genplayicons.py" % (
            "[%s]" % item, sym, sym)
        s = s.replace(lines[0], row)
    out[TABLE] = s
    return out


def main():
    changes = []
    for f, sym, item, fn, pal in ICON_LIST:
        im = image(fn(), pal)
        png, pp = os.path.join(ICONS, f + ".png"), os.path.join(PALS, f + ".pal")
        same = os.path.exists(png) and list(Image.open(png).getdata()) == list(im.getdata()) and \
            Image.open(png).getpalette()[:48] == im.getpalette()[:48]
        if not same:
            changes.append(os.path.relpath(png, GBA))
            if WRITE:
                im.save(png)
        if not os.path.exists(pp) or open(pp, newline="").read() != jasc(pal):
            changes.append(os.path.relpath(pp, GBA))
            if WRITE:
                open(pp, "w", newline="").write(jasc(pal))
        if os.path.isdir(SCRATCH):
            im.convert("RGB").resize((N * 8, N * 8), Image.NEAREST).save(os.path.join(SCRATCH, "icon_%s.png" % f))
    for p, text in tables().items():
        if open(p, encoding="utf-8").read() != text:
            changes.append(os.path.relpath(p, GBA))
            if WRITE:
                open(p, "w", encoding="utf-8").write(text)
    print("  the HARP's and FLUTE's icons: %s" % ("unchanged" if not changes else
          ("written " if WRITE else "would write ") + ", ".join(changes)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

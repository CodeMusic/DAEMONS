#!/usr/bin/env python3
"""The DAEMON-EMOJI: the follower's bubble built from what it feels (T-431 P3; plan-feelings 4).

    python3 tools/genemoji.py                    # report: the 27 faces as text, the palette, its greys
    python3 tools/genemoji.py --draft DIR [--field PNG X Y]   # DIR/daemon_emoji.png (indexed, 4bpp-ready),
                                                 #   daemon_emoji.pal and sheet.png
    python3 tools/genemoji.py --sheet OUT.png [--field PNG X Y]   # the review sheet; a 240x160 field shot, the
                                                 #   bubble's top-left on it, shows one at scale over the follower
    python3 tools/genemoji.py --write            # engineGba/graphics/misc/daemon_emoji.png + .pal (P3's build)

WHAT IT IS. A daemon is a machine that evolved into a creature, so its bubble is not a speech balloon with a
human smiley in it: it is a SMALL SCREEN -- an outlined bezel, a dark glass, a glint in one corner, a power light
-- with a tail down to the follower, and on the glass a face made of glyph strokes. Three parts, each one feeling,
and none of them named (craft rule 1; never a word or a letter in it):

    EYES   from CALM-AFRAID   half-lidded (calm)   open                wide (afraid)
    MOUTH  from SAD-GLAD      down (sad)           flat                up (glad)
    TINT   from MAD           none (cool glass)    warm (amber)        hot (red glass)

27 frames, 3 x 3 x 3. Frame n = mad*9 + eyes*3 + mouth, and the sheet is 48x144 -- three frames a row, as
emoticons.png is three a row -- so row = mad*3 + eyes and column = mouth: the sideways axis is sad to glad and
the downward one calm to afraid, the same two axes the SUMMARY's grid uses (the user, 2026-10-21).

HOW IT IS DRAWN. Directly at 16x16, pixel by pixel, the way every small icon in this project is (genopusicon,
gennotebookicon, genbookicons, genthrashicon). The 512x512 rule is spriteforge's (CLAUDE.md: "draw sprites at
--size 512x512"), and T-164/T-170 measured what a model drawing reduced to sixteen pixels comes back as: speckle.
A glyph face two pixels an eye is a pixel decision, not a reduction.

THE PALETTE survives being greyed. At runtime it is ONE OBJ palette, sixteen colours, entry 0 transparent, and
friendship greys it (daemon_saturation.c: 12% colour at 0, about half at 70, all at 255) -- and in HALFTONE it keeps
its colour, because it is on the follower (the user, 2026-10-21). So nothing here is carried by hue alone: the
glyph is the brightest thing on every glass and the glass the darkest, and MAD also raises the glass's VALUE --
cool glass is near black, warm a dark amber, hot a lit red -- so a bubble greyed to nothing still reads calmer or
hotter by how much the glass glows. The power light takes the glyph's colour, a second place the tint shows.

    0 transparent  1 ink  2 bezel lit  3 bezel  4 bezel shaded  5 glint
    6-8 none: glass, glyph, glyph dim   9-11 warm: the same   12-14 hot: the same   15 spare (ink)

Colours are on the GBA's five-bit grid, so what this prints is what the hardware shows.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT_PNG = os.path.join(GBA, "graphics", "misc", "daemon_emoji.png")
OUT_PAL = os.path.join(GBA, "graphics", "misc", "daemon_emoji.pal")
WRITE = "--write" in sys.argv


def five(c):
    """Snap to the GBA's five bits a channel, shown as 8-bit the way gbagfx reads a .pal back."""
    return tuple((v >> 3) << 3 for v in c)


INK, LIT, BEZEL, SHADE, GLINT = 1, 2, 3, 4, 5
TINTS = ("none", "warm", "hot")
#  per tint: (glass, glyph, glyph dim). The glass's value rises with MAD; the glyph stays the brightest thing.
TINT_RGB = [
    ((24, 32, 48), (208, 240, 255), (96, 136, 168)),     # none: cool, near-black glass, a pale cyan glow
    ((80, 52, 24), (255, 216, 128), (176, 128, 64)),     # warm: amber glass, an amber glow
    ((168, 40, 32), (255, 224, 184), (232, 120, 88)),    # hot: lit red glass, a white-hot glow
]
PAL = [(0, 0, 0), (16, 16, 24), (216, 216, 232), (160, 160, 184), (104, 104, 128), (248, 248, 255)]
for t in TINT_RGB:
    PAL += list(t)
PAL += [(16, 16, 24)]
PAL = [five(c) for c in PAL]
assert len(PAL) == 16


def glass(m):
    return 6 + 3 * m


def glyph(m):
    return 7 + 3 * m


def dim(m):
    return 8 + 3 * m


EYES = ("calm", "open", "wide")
MOUTHS = ("down", "flat", "up")
LEFT_EYE, RIGHT_EYE = (4, 5), (10, 11)     # two pixels each, symmetric about the glass's middle (7.5)


def frame(mad, eyes, mouth):
    g = [[0] * 16 for _ in range(16)]

    def put(x, y, c):
        g[y][x] = c

    # the bezel: a rounded 16x13 screen, lit from the top left
    for x in range(2, 14):
        put(x, 0, INK)
        put(x, 12, INK)
        put(x, 1, LIT)
        put(x, 11, SHADE)
    for y in range(2, 11):
        put(0, y, INK)
        put(15, y, INK)
        put(1, y, LIT)
        put(14, y, SHADE)
    for (x, y) in ((1, 1), (14, 1), (1, 11), (14, 11)):    # the rounded corners
        put(x, y, INK)
    # the glass, its corners rounded into the bezel
    for y in range(2, 11):
        for x in range(2, 14):
            put(x, y, glass(mad))
    for (x, y) in ((2, 2), (13, 2), (2, 10), (13, 10)):
        put(x, y, BEZEL)
    put(3, 2, GLINT)                                  # the glint: it is glass
    put(2, 3, GLINT)
    put(12, 11, glyph(mad))                           # the power light, in the glyph's colour
    # the tail, down to the follower
    put(7, 12, SHADE)
    put(8, 12, SHADE)
    put(6, 13, INK)
    put(7, 13, SHADE)
    put(8, 13, SHADE)
    put(9, 13, INK)
    put(7, 14, INK)
    put(8, 14, INK)

    G, D = glyph(mad), dim(mad)
    for ex in (LEFT_EYE, RIGHT_EYE):
        if EYES[eyes] == "wide":                       # tall: three rows lit
            for x in ex:
                for y in (3, 4, 5):
                    put(x, y, G)
        elif EYES[eyes] == "open":                     # two by two
            for x in ex:
                for y in (4, 5):
                    put(x, y, G)
        else:                                          # half-lidded: the lid dim, the eye a slit under it
            for x in ex:
                put(x, 4, D)
                put(x, 5, G)

    if MOUTHS[mouth] == "up":
        put(5, 8, G)
        put(10, 8, G)
        for x in range(6, 10):
            put(x, 9, G)
    elif MOUTHS[mouth] == "down":
        for x in range(6, 10):
            put(x, 8, G)
        put(5, 9, G)
        put(10, 9, G)
    else:
        for x in range(6, 10):
            put(x, 9, G)
        put(5, 9, D)
        put(10, 9, D)
    return g


def index_of(mad, eyes, mouth):
    return mad * 9 + eyes * 3 + mouth


def sheet_image():
    """48x144, mode P: frame n at column n % 3, row n // 3 (built with -mwidth 2 -mheight 2, as emoticons.png)."""
    im = Image.new("P", (48, 144), 0)
    flat = []
    for c in PAL:
        flat += list(c)
    im.putpalette(flat)
    for mad in range(3):
        for eyes in range(3):
            for mouth in range(3):
                n = index_of(mad, eyes, mouth)
                ox, oy = (n % 3) * 16, (n // 3) * 16
                f = frame(mad, eyes, mouth)
                for y in range(16):
                    for x in range(16):
                        im.putpixel((ox + x, oy + y), f[y][x])
    return im


def jasc(pal):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal)


# ---- the runtime's grey, as daemon_saturation.c does it, on five-bit channels --------------------------------
def keep_of(friendship):
    rest = 255 - friendship
    return 31 + 225 * (65025 - rest * rest) // 65025


def desaturate(c, friendship):
    keep = keep_of(friendship)
    if keep >= 256:
        return c
    r, g, b = (v >> 3 for v in c)
    grey = (r * 77 + g * 150 + b * 29 + 128) >> 8

    def ch(v):
        # C's division truncates toward zero
        d = (v - grey) * keep
        q = abs(d) // 256
        return grey + (q if d >= 0 else -q)

    return tuple(ch(v) << 3 for v in (r, g, b))


def luma(c):
    return (c[0] * 77 + c[1] * 150 + c[2] * 29) >> 8


def rgb_frame(mad, eyes, mouth, friendship=255):
    pal = [PAL[0]] + [desaturate(c, friendship) for c in PAL[1:]]
    f = frame(mad, eyes, mouth)
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            if f[y][x]:
                im.putpixel((x, y), pal[f[y][x]] + (255,))
    return im


# ---- the review sheet -----------------------------------------------------------------------------------------
def font(size):
    for p in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def review_sheet(out, field=None):
    S = 8                                   # pixel scale
    F = 16 * S                              # one face
    GAP = 14
    BG, TXT, SUB = (28, 28, 34), (232, 232, 236), (150, 150, 162)
    big, small = font(15), font(12)
    left = 150                              # room for the row labels
    block_w = 3 * F + 2 * GAP + 40
    W = 20 + left + 3 * block_w
    H = 1600
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((20, 14), "T-431 P3 DRAFT -- the daemon-emoji: 27 faces (eyes x mouth x tint), x8. Labels are the "
           "sheet's, never the bubble's.", font=big, fill=TXT)
    y0 = 60
    eye_words = ("eyes: half-lidded", "eyes: open", "eyes: wide")
    eye_sub = ("(calm)", "", "(afraid)")
    mouth_words = ("mouth: down (sad)", "mouth: flat", "mouth: up (glad)")
    for mad in range(3):
        bx = 20 + mad * block_w
        d.text((bx + left, y0), "MAD: %s" % ("none", "warm", "hot")[mad], font=big, fill=TXT)
        for mouth in range(3):
            d.text((bx + left + mouth * (F + GAP), y0 + 24), mouth_words[mouth], font=small, fill=SUB)
        for eyes in range(3):
            fy = y0 + 46 + eyes * (F + GAP)
            if mad == 0:
                d.text((bx + 4, fy + F // 2 - 14), eye_words[eyes], font=small, fill=SUB)
                d.text((bx + 4, fy + F // 2 + 2), eye_sub[eyes], font=small, fill=SUB)
            for mouth in range(3):
                fx = bx + left + mouth * (F + GAP)
                face = rgb_frame(mad, eyes, mouth).resize((F, F), Image.NEAREST)
                im.paste(face, (fx, fy), face)
    y = y0 + 46 + 3 * (F + GAP) + 20
    d.line((20, y, W - 20, y), fill=(60, 60, 70))
    y += 14
    d.text((20, y), "Greyed by friendship at runtime (daemon_saturation.c: keep 12% at 0, 54% at 70, 100% at 255). "
           "Each group: friendship 0 / 70 / 255.", font=big, fill=TXT)
    y += 30
    picks = [(0, 0, 2, "calm, glad, no MAD"), (1, 1, 1, "open, flat, warm"), (2, 2, 0, "afraid, sad, hot"),
             (2, 0, 2, "calm, glad, hot"), (0, 2, 0, "afraid, sad, no MAD")]
    S2 = 5
    F2 = 16 * S2
    x = 20
    for (mad, eyes, mouth, words) in picks:
        d.text((x, y), words, font=small, fill=SUB)
        for i, fr in enumerate((0, 70, 255)):
            face = rgb_frame(mad, eyes, mouth, fr).resize((F2, F2), Image.NEAREST)
            im.paste(face, (x + i * (F2 + 6), y + 20), face)
            d.text((x + i * (F2 + 6) + F2 // 2 - 10, y + 24 + F2), str(fr), font=small, fill=SUB)
        x += 3 * (F2 + 6) + 30
    y += 20 + F2 + 40
    if field:
        path, fx, fy = field
        bgim = Image.open(path).convert("RGB")
        d.line((20, y, W - 20, y), fill=(60, 60, 70))
        y += 14
        d.text((20, y), "At scale over the follower (ROUTE 1, CONTENT; the field shot x2; the bubble at friendship "
               "255, then 70, then 0, as it would sit).", font=big, fill=TXT)
        y += 30
        x = 20
        for (mad, eyes, mouth, fr) in ((0, 0, 2, 255), (1, 1, 1, 70), (2, 2, 0, 0)):
            shot = bgim.copy()
            face = rgb_frame(mad, eyes, mouth, fr)
            shot.paste(face, (fx, fy), face)
            shot = shot.resize((shot.width * 2, shot.height * 2), Image.NEAREST)
            im.paste(shot, (x, y))
            x += shot.width + 20
        y += bgim.height * 2 + 20
    im = im.crop((0, 0, W, y + 10))
    im.save(out)
    return out


def report():
    print("genemoji (T-431 P3): 27 faces, 48x144, one OBJ palette")
    print("  palette (index: rgb, grey at friendship 255 / 70 / 0):")
    names = ["transparent", "ink", "bezel lit", "bezel", "bezel shaded", "glint"]
    for t in TINTS:
        names += ["%s glass" % t, "%s glyph" % t, "%s glyph dim" % t]
    names += ["spare (ink)"]
    for i, c in enumerate(PAL):
        lum = [luma(desaturate(c, f)) for f in (255, 70, 0)]
        print("   %2d %-16s %-16s %s" % (i, names[i], c, lum))
    print("  value contrast, glyph over glass (luma):")
    for m, t in enumerate(TINTS):
        print("   %-5s glyph %3d  glass %3d  difference %3d" % (t, luma(PAL[glyph(m)]), luma(PAL[glass(m)]),
                                                                luma(PAL[glyph(m)]) - luma(PAL[glass(m)])))
    seen = set()
    for mad in range(3):
        for eyes in range(3):
            for mouth in range(3):
                seen.add(tuple(tuple(r) for r in frame(mad, eyes, mouth)))
    print("  distinct frames: %d of 27" % len(seen))
    print("  three of them (calm/glad/none, open/flat/warm, wide/sad/hot):")
    rows = [frame(0, 0, 2), frame(1, 1, 1), frame(2, 2, 0)]
    for y in range(16):
        print("   " + "   ".join("".join(".123456789abcdef"[v] if v else "." for v in r[y]) for r in rows))
    if os.path.exists(OUT_PNG):
        same = list(Image.open(OUT_PNG).getdata()) == list(sheet_image().getdata())
        print("  %s: %s" % (os.path.relpath(OUT_PNG, ROOT), "up to date" if same else "WOULD CHANGE"))
    else:
        print("  %s: not in the engine yet (--write puts it there)" % os.path.relpath(OUT_PNG, ROOT))


def main():
    args = sys.argv[1:]
    field = None
    if "--field" in args:
        i = args.index("--field")
        field = (args[i + 1], int(args[i + 2]), int(args[i + 3]))
    if "--draft" in args:
        out = args[args.index("--draft") + 1]
        os.makedirs(out, exist_ok=True)
        sheet_image().save(os.path.join(out, "daemon_emoji.png"), bits=4)
        open(os.path.join(out, "daemon_emoji.pal"), "w", newline="").write(jasc(PAL))
        review_sheet(os.path.join(out, "sheet.png"), field)
        print("wrote %s/daemon_emoji.png, daemon_emoji.pal, sheet.png" % out)
        return 0
    if "--sheet" in args:
        out = args[args.index("--sheet") + 1]
        print("wrote", review_sheet(out, field))
        return 0
    if WRITE:
        sheet_image().save(OUT_PNG, bits=4)
        open(OUT_PAL, "w", newline="").write(jasc(PAL))
        print("wrote", os.path.relpath(OUT_PNG, ROOT), "and", os.path.relpath(OUT_PAL, ROOT))
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""The LYREBIRD outside CALLOW SCHOOL, who gives CONTENT its HARP (T-417 P3, DRAFT art).

    python3 tools/genlyrebird.py            # report, and a preview in the scratch dir
    python3 tools/genlyrebird.py --write    # graphics/object_events/pics/people/town_callow_lyrebird.png

The user, 2026-10-17 (docs/private/draft-play-2026-10-17.md 2): the HARP is given by a LYREBIRD standing two tiles
right of the school door -- the bird that learns every sound it hears, which is what the SONGBOOK does. Every person
is an animal (fable-actors-animals); this one is simply the bird, its lyre of a tail raised behind it: two banded
outer feathers curving out and up, fine white filaments between them.

Drawn by hand in Python. spriteforge's 512x512 draft (seed 4170) gave a crested blue fowl, not a lyrebird, so it
served only as a reminder of how much a raised tail reads at this size. Nine 16x32 frames like every walking sheet
(it never walks: the walking frames repeat the standing ones), in CALLOW's own sixteen colours
(npc_town_callow.pal), so it stands in PALSLOT_NPC_SPECIAL beside the town's people with the town's own tag and
spends no palette of its own (engine.md trap 17).
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_town_callow.pal")
OUT = os.path.join(GBA, "graphics/object_events/pics/people/town_callow_lyrebird.png")
RULES = os.path.join(GBA, "spritesheet_rules.mk")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

# npc_town_callow: a amber  b brown  t tan  c cream  w white  g grey-green  o dark olive  K black
INDEX = {" ": 0, "a": 5, "b": 10, "t": 9, "c": 8, "w": 14, "g": 12, "o": 13, "K": 15}


def mirror(halves):
    return [h + h[::-1] for h in halves]


#  The lyre: two outer feathers banded amber and brown, curling outward at the tips, with filaments between.
LYRE = [
    "        ",
    " KK     ",
    "KabK    ",
    "KbKK    ",
    "KaK  w  ",
    " KbK w g",
    " KaK w g",
    " KbK w g",
    "  KaK wg",
    "  KbK wg",
    "  KaK wg",
    "   KbK g",
]

FRONT = mirror(LYRE + [
    "   KaKKK",    # the head, in front of the lyre
    "   KbKbb",
    "    KwKb",    # the eye, and its light
    "    Kbbo",    # the beak, two dark pixels at the middle
    "    KKbt",
    "    Kbbt",    # a tan throat
    "   Kbbtt",
    "  Kbbbtc",
    "  Kbbttc",    # a pale breast
    " KKbbttt",
    " KabbbKt",    # the wing's edge
    " Kbabbbt",
    "  Kbbbbb",
    "  KKbbbb",
    "   KKKbb",
    "     KoK",    # thin dark legs
    "     KoK",
    "    KooK",
    "        ",
    "        ",
])

BACK = mirror(LYRE + [
    "   KaKKK",
    "   KbKbb",
    "    Kbbb",
    "    Kbbb",
    "    KKbb",
    "    Kbbb",
    "   Kbbbb",
    "  Kbbbbb",
    "  Kbabbb",
    " KKbbabb",
    " Kabbbab",
    " Kbabbbb",
    "  Kbbbbb",
    "  KKbbbb",
    "   KKKbb",
    "     KoK",
    "     KoK",
    "    KooK",
    "        ",
    "        ",
])

#  Facing left: the beak leads, the lyre rises behind it to the right.
SIDE = [
    "                ",
    "          KK    ",
    "         KabK   ",
    "        KbK KK  ",
    "       KaK KabK ",
    "   w   KbK KbK  ",
    "   w   KaKKaK   ",
    "    w  KbKbK    ",
    "    w  KaKbK    ",
    "     w KbKaK    ",
    "     wgKaKbK    ",
    "      gKbKaK    ",
    "    KKKKaKbK    ",
    "   KbbbKbKaK    ",
    "   KbKbbKKbK    ",    # the eye
    " KoobbbbbKbK    ",    # the beak points the way it faces
    "   KKtbbbbKK    ",
    "    Kttbbbbb K  ",
    "    Kttbbbbbb   ",
    "    Kctbbaabb   ",
    "    Kctbbbaab   ",
    "    Kcttbbbbb   ",
    "     Kctbbbab   ",
    "     KKttbbbK   ",
    "      KKKbbK    ",
    "        KKK     ",
    "        KoK     ",
    "        KoK     ",
    "       KooK     ",
    "                ",
    "                ",
    "                ",
]


def fix(rows):
    out = []
    for r in rows:
        r = r[:16]
        out.append(r + " " * (16 - len(r)))
    return out


def outline_side(rows):
    """the side view's body is drawn open on the right; close it with the outline where it meets the transparent."""
    g = [list(r) for r in rows]
    for y in range(len(g)):
        for x in range(16):
            if g[y][x] in "bta" and y >= 16 and (x == 15 or g[y][x + 1] == " "):
                g[y][x] = "K"
    return ["".join(r) for r in g]


def frames():
    f, b, s = fix(FRONT), fix(BACK), outline_side(fix(SIDE))
    for name, fr in (("front", f), ("back", b), ("side", s)):
        assert len(fr) == 32, "%s is %d rows" % (name, len(fr))
        for line in fr:
            assert not set(line) - set(INDEX), (name, line)
    return [f, b, s, f, f, b, b, s, s]


def jasc(path):
    lines = open(path, newline="").read().replace("\r\n", "\n").split("\n")
    return [tuple(int(v) for v in l.split()) for l in lines[3:19]]


def sheet():
    fr = frames()
    img = Image.new("P", (16 * len(fr), 32), 0)
    img.putpalette([v for c in jasc(PAL) for v in c] + [0] * (768 - 48))
    px = img.load()
    for n, f in enumerate(fr):
        for y, line in enumerate(f):
            for x, ch in enumerate(line):
                px[n * 16 + x, y] = INDEX[ch]
    return img


def ensure_rule():
    target = "$(OBJEVENTGFXDIR)/people/town_callow_lyrebird.4bpp"
    s = open(RULES).read()
    if target + ":" in s:
        return False
    open(RULES, "w").write(s.rstrip("\n") + "\n\n%s: %%.4bpp: %%.png\n\t$(GFX) $< $@ -mwidth 2 -mheight 4\n" % target)
    return True


def main():
    img = sheet()
    print("  the LYREBIRD: 9 frames (3 drawn), CALLOW's palette")
    os.makedirs(SCRATCH, exist_ok=True)
    prev = img.convert("RGBA")
    bg = Image.new("RGBA", prev.size, (120, 168, 96, 255))
    bg.alpha_composite(prev)
    bg.crop((0, 0, 48, 32)).resize((48 * 10, 32 * 10), Image.NEAREST).save(os.path.join(SCRATCH, "lyrebird_preview.png"))
    old = Image.open(OUT) if os.path.exists(OUT) else None
    rule = os.path.exists(RULES) and "town_callow_lyrebird.4bpp:" in open(RULES).read()
    if old is not None and list(old.getdata()) == list(img.getdata()) and rule:
        print("  town_callow_lyrebird.png is current")
        return
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % SCRATCH)
        return
    img.save(OUT, bits=4)
    ensure_rule()
    print("  written")


if __name__ == "__main__":
    main()

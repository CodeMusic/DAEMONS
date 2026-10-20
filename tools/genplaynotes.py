#!/usr/bin/env python3
"""PLAY's notes in colour (T-417 P1): one 16-colour palette and the shapes drawn in it.

    python3 tools/genplaynotes.py            # report
    python3 tools/genplaynotes.py --write    # engineGba/graphics/play/

docs/private/draft-play-2026-10-17.md secs. 5 and 6. ONE OBJ palette holds every colour a note can be, so the
instrument costs one palette slot however many notes are in the air (PALTAG_KEY_COLOURS, src/play.c), and T-415's
leaves and T-416's month notes can share it later:
   0      transparent
   1-12   the twelve keys, C to B, in the user's colours (2026-10-17): C red, C# red/orange, D orange, D# orange/yellow,
          E yellow, F green, F# green/blue, G blue, G# blue/indigo, A indigo, A# indigo/purple, B purple.
          A is INDIGO everywhere (the user, 2026-10-17) -- the fir's A too (src/field_specials.c, FIR_INDIGO).
   13     outline    14  highlight    15  gold-white glow (P5: the staff's heads fill with it when a song joins -- the
          design's "gold-white (index 15)", DRAFT)

The sheets, each frame in key order C..B:
   notes.png   16x16 x 12   the note that drifts up from the instrument, and the chosen key on the wheel
   small.png    8x8  x 38   12 wheel dots, 12 staff heads, 12 hollow heads (P5: the GHOSTS, a learned song's next
                            notes shown ahead on the staff), then 1 gold head (a joined song's heads), then the BAND'S
                            SHEET's glyph -- a scrap of staff paper with a B-flat head on it, set beside B FLAT on the
                            wheel once the sheet is held (the draft's sec. 4; DRAFT art)
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "engineGba", "graphics", "play")

KEYS = [  # 5-bit colours, as the GBA holds them
    (31, 0, 0), (31, 8, 0), (31, 16, 0), (31, 24, 0), (31, 31, 0), (0, 31, 0),
    (0, 24, 24), (0, 8, 31), (6, 0, 31), (12, 0, 31), (18, 0, 31), (24, 0, 31),
]
OUTLINE, HIGHLIGHT, GLOW = 13, 14, 15
PALETTE = [(0, 0, 0)] + KEYS + [(4, 3, 8), (31, 31, 26), (31, 28, 14)]

#  16x16: an eighth note, head low left, stem up the right of it, flag out to the right. '#' colour, 'o' outline,
#  'h' highlight.
NOTE = [
    "................",
    "........oo......",
    "........o#o.....",
    "........o##o....",
    "........o#o#o...",
    "........o#oo#o..",
    "........o#o.o#o.",
    "........o#o..o#o",
    "........o#o...oo",
    "........o#o.....",
    "....ooooo#o.....",
    "...o#h###o#o....",
    "..o#h#####o.....",
    "..o#######o.....",
    "...o#####o......",
    "....ooooo.......",
]
DOT = [
    "........",
    "..oooo..",
    ".o#h##o.",
    ".oh###o.",
    ".o####o.",
    ".o####o.",
    "..oooo..",
    "........",
]
HEAD = [
    "........",
    "........",
    "..ooo...",
    ".o###o..",
    ".o###o..",
    "..ooo...",
    "........",
    "........",
]
#  P5: a GHOST -- the head's ring in its key's colour, hollow; and the GOLD head a joined song's notes fill with.
HOLLOW = [
    "........",
    "........",
    "..###...",
    ".#...#..",
    ".#...#..",
    "..###...",
    "........",
    "........",
]
GOLD = [
    "........",
    "........",
    "..ooo...",
    ".ohwwo..",
    ".owwwo..",
    "..ooo...",
    "........",
    "........",
]
#  the BAND'S SHEET: a scrap of cream staff paper, two staff lines, a head on it in B FLAT's colour
SHEET = [
    ".oooooo.",
    ".ohhhhho",
    ".ooooooo",
    ".ohh##ho",
    ".oo###oo",
    ".ohh##ho",
    ".ooooooo",
    "........",
]
SHEET_KEY = 10                                            # B FLAT (src/play.c)


def paint(shape, key):
    m = {".": 0, "#": 1 + key, "o": OUTLINE, "h": HIGHLIGHT, "w": GLOW}
    return [[m[c] for c in row] for row in shape]


def sheet(frames, w, h):
    im = Image.new("P", (w, h * len(frames)))
    im.putpalette([c * 8 for rgb in PALETTE for c in rgb] + [0] * (768 - 48))
    for i, f in enumerate(frames):
        for y, row in enumerate(f):
            for x, v in enumerate(row):
                im.putpixel((x, i * h + y), v)
    return im


def jasc():
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c * 8 for c in rgb) for rgb in PALETTE)


def main():
    write = "--write" in sys.argv
    outs = {
        "notes.png": sheet([paint(NOTE, k) for k in range(12)], 16, 16),
        "small.png": sheet([paint(DOT, k) for k in range(12)] + [paint(HEAD, k) for k in range(12)]
                           + [paint(HOLLOW, k) for k in range(12)] + [paint(GOLD, 0), paint(SHEET, SHEET_KEY)], 8, 8),
    }
    changed = []
    for name, im in outs.items():
        p = os.path.join(OUT, name)
        same = os.path.exists(p) and list(Image.open(p).getdata()) == list(im.getdata()) \
            and Image.open(p).getpalette()[:48] == im.getpalette()[:48]
        if not same:
            changed.append(name)
            if write:
                os.makedirs(OUT, exist_ok=True)
                im.save(p)
    p = os.path.join(OUT, "key_colours.pal")
    old = open(p, "rb").read().decode() if os.path.exists(p) else None
    if old != jasc():
        changed.append("key_colours.pal")
        if write:
            os.makedirs(OUT, exist_ok=True)
            open(p, "wb").write(jasc().encode())
    print("  graphics/play: %s" % ("unchanged" if not changed else ("written: " if write else "would write: ") + ", ".join(changed)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""THE WISH TO SING's notes (T-596; the user, 2026-11-18). DRAFT art.

    python3 tools/genhumnotes.py                  # report: the frames as text; exit 1 if the engine's PNG differs
    python3 tools/genhumnotes.py --sheet OUT.png  # a review sheet: every frame enlarged, with its name
    python3 tools/genhumnotes.py --write          # engineGba/graphics/daemon_song/hum_notes.png

WHAT IT IS. As a daemon nears its evolution it wishes to sing: now and then the follower hums a bar of its song as it
knows it, and each note rises from its mouth as a small note in its pitch's colour (src/daemons_follower.c, the hum).
The user: "visual correctly colour coded notes emerge from the daemons mouth ... the player associates the fact the
daemon said it wants to sing along with the visual emergence of the notes creating an intuitive memory pointer".

THE COLOURS are PLAY's own (engineGba graphics/play/key_colours.pal, tools/genplaynotes.py), read from that file and
never typed twice, so a note the follower hums is the colour the same note is on the KEY WHEEL: 1-12 the twelve keys
C to B, 13 the outline, 14 the highlight. SYNESTHESIA (gensongs.py, companion/server/src/synesthesia.ts): C red,
D orange, E yellow, F green, G blue, A indigo, B violet, and a BLACK KEY THE TWO COLOURS EITHER SIDE OF IT -- so a
black key's note is split down the middle as T-594's sheets split it, the head in the white key below and the stem and
flag in the white key above (C# red then orange). PLAY's palette also holds a blend for each black key (2, 4, 7, 9,
11); the hum never draws them.

THE FRAMES, fifteen of 8x8 in one row (120x8; the generic %.4bpp rule cuts them in order):
    0-11   a note of each pitch class, C to B: an eighth note, head low left, stem up, flag out to the right
    12-14  STATIC: the note's own shape in snow (the outline and highlight, scattered), three seeds -- a note not yet
           learned is shown as this, and in its true colour only on the frames its true pitch is heard (matching the
           audio's flicker in src/daemon_song.c)

Drawn directly at 8x8, pixel by pixel, as every small icon in this project is.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PAL = os.path.join(GBA, "graphics", "play", "key_colours.pal")
OUT = os.path.join(GBA, "graphics", "daemon_song", "hum_notes.png")

OUTLINE, HIGHLIGHT = 13, 14
WHITE_KEYS = (0, 2, 4, 5, 7, 9, 11)
STATIC_FRAMES = 3

#  '#' its colour, 'o' outline, 'h' highlight. Split at x = SPLIT for a black key: left the white key below, right above.
NOTE = [
    "....ooo.",
    "...o###o",
    "...o#oo.",
    "...o#o..",
    ".ooo#o..",
    "o#h##o..",
    "o###o...",
    ".ooo....",
]
SPLIT = 4


def palette():
    lines = open(PAL).read().split("\n")
    assert lines[0].strip() == "JASC-PAL", PAL
    cols = [tuple(int(v) for v in l.split()) for l in lines[3:19]]
    assert len(cols) == 16, PAL
    return cols


def note_frame(pc):
    """A pitch class's note: one colour for a white key, the two either side for a black key."""
    if pc in WHITE_KEYS:
        left = right = pc + 1
    else:
        left, right = pc, pc + 2                           # the white key below (pc - 1) and above (pc + 1), +1 each
    px = []
    for y, row in enumerate(NOTE):
        for x, c in enumerate(row):
            px.append({".": 0, "o": OUTLINE, "h": HIGHLIGHT, "#": left if x < SPLIT else right}[c])
    return px


def static_frame(seed):
    """The note's shape in snow: every pixel of it the outline, the highlight or nothing, from a fixed little LCG."""
    px, s = [], seed * 2654435761 & 0xFFFFFFFF
    for row in NOTE:
        for c in row:
            s = (s * 1103515245 + 12345) & 0x7FFFFFFF
            px.append(0 if c == "." else (OUTLINE, HIGHLIGHT, HIGHLIGHT, 0)[(s >> 16) & 3])
    return px


def frames():
    return [note_frame(pc) for pc in range(12)] + [static_frame(i + 1) for i in range(STATIC_FRAMES)]


def image(pal):
    fs = frames()
    im = Image.new("P", (8 * len(fs), 8), 0)
    im.putpalette([v for rgb in pal for v in rgb] + [0] * (768 - 48))
    for i, f in enumerate(fs):
        for j, v in enumerate(f):
            im.putpixel((8 * i + j % 8, j // 8), v)
    return im


NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "STATIC 1", "STATIC 2", "STATIC 3"]


def review_sheet(path, pal):
    from PIL import ImageDraw
    src = image(pal)
    im = src.convert("RGBA")
    im.putalpha(Image.eval(src, lambda v: 255 if v else 0).convert("L"))   # 0 is transparent
    scale, cell = 8, 80
    out = Image.new("RGB", (cell * len(NAMES), cell + 24), (36, 40, 52))
    d = ImageDraw.Draw(out)
    for i, name in enumerate(NAMES):
        f = im.crop((8 * i, 0, 8 * i + 8, 8)).resize((8 * scale, 8 * scale), Image.NEAREST)
        out.paste(f, (cell * i + 8, 8), f)
        d.text((cell * i + 8, cell + 4), name, fill=(220, 220, 230))
    out.save(path)
    return path


def same_as_disk(im):
    if not os.path.exists(OUT):
        return False
    disk = Image.open(OUT)
    return disk.mode == "P" and disk.size == im.size and list(disk.getdata()) == list(im.getdata()) \
        and disk.getpalette()[:48] == im.getpalette()[:48]


def main():
    pal = palette()
    im = image(pal)
    if "--sheet" in sys.argv:
        print("wrote", review_sheet(sys.argv[sys.argv.index("--sheet") + 1], pal))
        return 0
    if "--write" in sys.argv:
        if same_as_disk(im):
            print("hum_notes.png: already current")
            return 0
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        im.save(OUT)
        print("wrote", OUT)
        return 0
    for i, f in enumerate(frames()):
        print("frame %2d %s" % (i, NAMES[i]))
        for y in range(8):
            print("   " + "".join(".123456789ABCDEF"[v] if v else "." for v in f[8 * y:8 * y + 8]))
    ok = same_as_disk(im)
    print("hum_notes.png:", "current" if ok else "DIFFERS from this draw (--write)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

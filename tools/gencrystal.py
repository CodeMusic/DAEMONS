#!/usr/bin/env python3
"""Draw CRYSTAL CLEAR's overworld sprite -- the professor's slot, redrawn.

    python3 tools/gencrystal.py            # preview to /tmp/crystal_ow.png
    python3 tools/gencrystal.py --write    # prof_oak.png and npc_crystal.pal

graphics/object_events/pics/people/prof_oak.png is nine 16x32 frames in the
order sPicTable_ProfOak loads them:

    0 down   1 up   2 left   3,4 down walk   5,6 up walk   7,8 left walk

Facing right is frame 2 with OAM's x-flip, so there is no right to draw. Index
0 is transparent.

DRAWN FROM REFERENCE, NOT RESAMPLED. The drafts came through the n8n
daemon/sprite workflow -- a front view from the local model, and the side and
back redrawn from that front by img2img so they stay one character -- and a
straight downsample of the front to 16x32 lost the face, the outline and the
coat in the same pass, exactly as tools/genplayer.py says it will. So the
drafts decide the colours and the silhouette, and the pixels are written here.

WHAT HAS TO READ AT SIXTEEN PIXELS, in order of what the eye finds first:

    the ears      tall, above where every human head in the game stops --
                  the one shape nobody else on the map has
    the coat      white, open, over purple: a scientist before a fox
    the tail      out from under the hem, on the side the drafts put it

VANILLA'S IDIOM FOR EVERYTHING ELSE. Same outline weight, walk frames drop the
whole figure one row and move the feet, and the head is large, because every
walking sprite in this game is -- 9.4's head-to-body rule is for the portraits,
and a sixteen-pixel adult drawn at adult proportions is a stick with a dot on it.
She is taller than the professor was instead: the ears start three rows higher.

HER OWN PALETTE. No NPC palette carries her: npc_white has greys and a tan the
professor's hair used, npc_blue has gold and purple and no greys to shade a
coat. The Clears are coloured by family (9.4), so she gets npc_crystal.pal.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PIC = os.path.join(GBA, "graphics/object_events/pics/people/prof_oak.png")
PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_crystal.pal")
PREVIEW = "/tmp/crystal_ow.png"
WRITE = "--write" in sys.argv

PALETTE = [
    (115, 197, 164),  # 0  transparent -- the key every object palette uses
    (255, 214,  66),  # 1  Y  fur, gold
    (230, 150,  32),  # 2  G  fur, shade
    (148,  90,  24),  # 3  B  fur, deep
    (255, 246, 214),  # 4  C  muzzle, throat, the tail's tip
    (172, 132, 230),  # 5  p  top, light
    (112,  72, 184),  # 6  P  top
    ( 66,  62,  92),  # 7  D  trousers
    (255, 255, 255),  # 8     (spare white)
    (198, 200, 216),  # 9  w  coat, shade
    (140, 140, 152),  # 10 v  coat, shadow
    ( 84,  84, 100),  # 11 g  hands
    (120,  72,  40),  # 12 n  inside the ear
    (  0,   0,   0),  # 13    (spare)
    (255, 255, 255),  # 14 W  coat
    (  0,   0,   0),  # 15 K  outline
]
INDEX = {" ": 0, "Y": 1, "G": 2, "B": 3, "C": 4, "p": 5, "P": 6, "D": 7,
         "w": 9, "v": 10, "g": 11, "n": 12, "W": 14, "K": 15}


def mirror(halves):
    """A symmetric row from its left eight columns."""
    return [h + h[::-1] for h in halves]


def overlay(rows, top, patch, left):
    """Lay an asymmetric part (the tail) over rows, skipping its spaces."""
    rows = list(rows)
    for i, line in enumerate(patch):
        r = list(rows[top + i])
        for j, ch in enumerate(line):
            if ch != " ":
                r[left + j] = ch
        rows[top + i] = "".join(r)
    return rows


# Rows 8..30 of each standing frame; 0..7 and 31 are empty.
EARS = ["   K    ", "  KGK   ", "  KnGK  ", "  KnYGKK"]

FRONT = mirror(EARS + [
    "  KGYYYY",
    " KGYYYYY",
    " KYYYKYY",   # the eyes, two rows tall, one column in from the outline
    " KYCYKYY",
    " KGCCCCK",   # the nose meets its mirror in the middle
    "  KGCCCC",
    "   KKCCC",
    "    KWWC",   # the throat, between the lapels
    "   KWWKP",
    "  KWWWKP",
    "  KWwWKP",
    "  KWwWKP",
    "  KgwWKP",
    "  KgKWKD",
    "   KWWKD",   # the coat stays open to the hem
    "   KwWKD",
    "    KDDK",
    "    KDDK",
    "   KKKK ",
])
# The tail comes out under the hem on her right, the viewer's left.
FRONT = overlay(FRONT, 17, [" KK ", "KGYK", "KYYK", "KYCK", " KK "], 0)

BACK = mirror([h.replace("n", "G") for h in EARS] + [
    "  KGYYYY",
    " KGYYYYY",
    " KGYYYYY",
    " KGYYYYY",
    " KGGYYYY",
    "  KGGYYY",
    "   KKGGG",
    "    KWWW",
    "   KWWWW",
    "  KWWWWW",
    "  KWwWWW",
    "  KWwWWW",
    "  KgwWWW",
    "  KgKWWW",
    "   KWWWW",
    "   KwWWW",
    "    KDDK",
    "    KDDK",
    "   KKKK ",
])
# From behind, the tail hangs down the middle of the coat.
BACK = overlay(BACK, 14, [" KK ", "KYGK", "KYYK", "KYGK", "KYCK", " KK "], 7)

SIDE = [
    "       K  K     ",
    "      KGKKGK    ",
    "      KnGKGYK   ",
    "     KYYYYYYK   ",
    "    KYYYYYYYGK  ",
    "  KKYKYYYYYYGK  ",   # the eye
    " KCCYKYYYYYYGK  ",
    "KKCCCYYYYYYGK   ",   # the snout, nose at the very edge
    " KCCCCCYYYGK    ",
    "  KKCCCCGGK     ",
    "    KKCCKK      ",
    "     KWCWK      ",
    "    KWWPWWK     ",
    "    KWWPWWK     ",
    "    KWwWWWK     ",
    "    KWWwWWK     ",
    "    KgWwWWK     ",
    "    KWWKWWKK    ",
    "    KWWWWwKYK   ",   # the tail, behind her
    "    KwWWWwKGYK  ",
    "     KDDDKKYCYK ",
    "     KDDDK KKK  ",
    "     KKKKK      ",
]

# Walking: the figure drops a row and the last three rows are the feet.
FRONT_STEPS = [
    ["    KDDKKDDK    ", "    KDDKKKKKK   ", "   KKKK         "],
    ["    KDDKKDDK    ", "   KKKKKKDDK    ", "         KKKK   "],
]
SIDE_STEPS = [
    ["    KDDKDDK YCYK", "   KDDK KDDKKK  ", "   KKK   KKK    "],
    ["     KDDDKKYCYK ", "     KDKDK KKK  ", "    KKK KKK     "],
]


def standing(rows):
    return [" " * 16] * 8 + rows + [" " * 16]


def walking(rows, feet):
    body = [" " * 16] * 9 + rows[:-3]
    return body + feet


def frames():
    out = [standing(FRONT), standing(BACK), standing(SIDE)]
    out += [walking(FRONT, f) for f in FRONT_STEPS]
    out += [walking(BACK, f) for f in FRONT_STEPS]
    out += [walking(SIDE, f) for f in SIDE_STEPS]
    for n, f in enumerate(out):
        assert len(f) == 32, "frame %d is %d rows" % (n, len(f))
        for r, line in enumerate(f):
            assert len(line) == 16, "frame %d row %d is %d wide: %r" % (n, r, len(line), line)
            bad = set(line) - set(INDEX)
            assert not bad, "frame %d row %d has %r" % (n, r, bad)
    return out


def sheet(fs):
    img = Image.new("P", (16 * len(fs), 32))
    flat = [c for rgb in PALETTE for c in rgb]
    img.putpalette(flat + [0] * (768 - len(flat)))
    px = img.load()
    for n, f in enumerate(fs):
        for y, line in enumerate(f):
            for x, ch in enumerate(line):
                px[n * 16 + x, y] = INDEX[ch]
    return img


def preview(img):
    """Each frame at x8, on the transparent key and on grey, beside the old professor."""
    rgb = img.convert("RGB")
    oak = Image.open(PIC).convert("RGB") if os.path.exists(PIC) else None
    w = img.width * 8
    out = Image.new("RGB", (w, 32 * 8 * 3), (60, 60, 60))
    out.paste(rgb.resize((w, 256), Image.NEAREST), (0, 0))
    grey = Image.new("RGB", rgb.size, (150, 150, 150))
    mask = Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata()))
    grey.paste(rgb, (0, 0), mask)
    out.paste(grey.resize((w, 256), Image.NEAREST), (0, 256))
    if oak is not None:
        out.paste(oak.resize((oak.width * 8, 256), Image.NEAREST), (0, 512))
    out.save(PREVIEW)


def write_pal(path):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in PALETTE]
    # CRLF, as .gitattributes has it for JASC-PAL (see tools/gbasprite.py)
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


img = sheet(frames())
preview(img)
print("  9 frames, 144x32 -> preview %s" % PREVIEW)
if WRITE:
    img.save(PIC, bits=4)
    write_pal(PAL)
    print("  written %s" % os.path.relpath(PIC, ROOT))
    print("  written %s" % os.path.relpath(PAL, ROOT))

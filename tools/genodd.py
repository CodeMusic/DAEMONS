#!/usr/bin/env python3
"""The sheets whose frames are not 16x32 (T-120; vision.md 9.4).

    python3 tools/genodd.py            # preview to /tmp/odd_ow.png
    python3 tools/genodd.py --write    # overwrite the sheets in place

genfolk.py's helpers all assume a 16x32 frame -- standing() pads to 32 rows, walk() swings the arms
at rows 16..28 and lifts a foot at row 31, check() demands 32x16, sheet() builds a strip 32 tall.
Five still-vanilla sheets are not that shape, so they get their own geometry here:

    biker          10 frames of 32x32   npc_pink    a boar on a machine  (35 objects)
    little_girl    10 frames of 16x16   npc_pink    a piglet             (16)
    little_boy      9 frames of 16x16   npc_white   a bear cub           (6, and no raised hand)
    tuber_m_water  10 frames of 16x16   npc_blue    a duckling in a ring (3)
    tuber_f        10 frames of 16x16   npc_white   a cygnet in a ring   (2)

A SMALL SPRITE IS A HEAD. Sixteen rows leaves about eight for the head and six for the body, which
is why vanilla's children read as heads on feet -- and it suits 9.4 exactly, where the head's size
carries age. The two tubers have no legs at all: the ring and the water take the bottom third.

THE FRAME COUNT AND THE FRAME SIZE ARE FIXED. The pic tables index a set number of frames of a set
tile size, and the ROM reads whatever follows if a sheet is short -- so every sheet is measured
against the file already on disk before a byte is written.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import read_pal, PEOPLE, WHITE
from genleaders import BLUE, PINK

PREVIEW = "/tmp/odd_ow.png"
WRITE = "--write" in sys.argv


# ------------------------------------------------------------------ geometry: a 16x16 sprite
def _fit(rows, n):
    """ljust(n)[:n] pads a short row but SILENTLY CLIPS a long one, and check() cannot see it: the
    mirror always yields the right final width. Say so instead."""
    for i, r in enumerate(rows):
        assert len(r) <= n, "row %d is %d wide, the limit is %d: %r" % (i, len(r), n, r)
    return [r.ljust(n)[:n] for r in rows]


def h16(rows):
    """half rows of eight, mirrored to sixteen"""
    return [r + r[::-1] for r in _fit(rows, 8)]


def s16(rows):
    return _fit(rows, 16)


# A MIRRORED HALF ROW MUST REACH THE CENTRE COLUMN. h16() pads a half to eight and mirrors it, so a
# seven-character row leaves column 7 blank -- and its reflection leaves column 8 blank too, opening
# a two-pixel transparent seam straight down the middle of the sprite. The first draft of all four
# of these had it: the heads read as two lobes and the biker as two riders side by side. Every row
# below runs to column 7. The one place a gap IS wanted is between the legs, and those rows stop
# short on purpose.
def small_mammal(fur, ear, muzzle):
    """six drawn rows of head: a crown with an ear in it, an eye, a muzzle, a chin"""
    front = ["", "", "  K" + ear + "KKKK", "  K" + fur * 5, "  K" + fur + "K" + fur * 3,
             "  K" + fur * 5, "  K" + fur * 2 + muzzle * 3, "   KK" + muzzle * 3]
    back = ["", "", "  K" + ear + "KKKK", "  K" + fur * 5, "  K" + fur * 5,
            "  K" + fur * 5, "  K" + fur * 5, "   KK" + fur * 3]
    side = ["", "", "    KKKK", "   K" + fur * 4 + "K", "   K" + fur + "K" + fur * 2 + "K",
            "  K" + muzzle * 2 + fur * 3 + "K", "   K" + muzzle + fur * 3 + "K", "    KK" + fur * 2 + "K"]
    return front, back, side


def small_bird(feather, beak):
    front = ["", "", "   KKKKK", "  K" + feather * 5, "  K" + feather + "K" + feather * 3,
             "  K" + feather * 4 + beak, "  K" + feather * 3 + beak * 2, "   KK" + feather * 3]
    back = ["", "", "   KKKKK", "  K" + feather * 5, "  K" + feather * 5,
            "  K" + feather * 5, "  K" + feather * 5, "   KK" + feather * 3]
    side = ["", "", "    KKKK", "   K" + feather * 4 + "K", "   K" + feather + "K" + feather * 2 + "K",
            " K" + beak * 2 + feather * 4 + "K", "  K" + beak + feather * 4 + "K", "    KK" + feather * 2 + "K"]
    return front, back, side


def small_body(shirt, foot):
    return ["   K" + shirt * 4, "  K" + shirt * 5, "  K" + shirt * 5, "  K" + shirt * 5,
            "   K" + shirt * 4, "   K" + foot * 2 + "K", "   K" + foot * 2 + "K", "   KKKK"]


def small_ring(ring, water):
    """no legs: the ring sits on the water and the bottom rows are the surface"""
    return ["   K" + ring * 4, "  K" + ring * 5, "  K" + ring * 5, "   K" + ring * 4,
            "   K" + water * 4, "    K" + water * 3, "     KKK", ""]


def small_side_body(shirt, foot):
    return ["    K" + shirt * 3 + "K", "   K" + shirt * 4 + "K", "   K" + shirt * 4 + "K", "   K" + shirt * 4 + "K",
            "    K" + shirt * 3 + "K", "    K" + foot * 2 + "K", "    K" + foot * 2 + "K", "    KKKK"]


def small_side_ring(ring, water):
    return ["    K" + ring * 3 + "K", "   K" + ring * 4 + "K", "   K" + ring * 4 + "K", "    K" + ring * 3 + "K",
            "    K" + water * 3 + "K", "     K" + water * 2 + "K", "      KKK", ""]


def small_fig(head, body, side_body):
    f, b, s = head
    return h16(list(f) + body), h16(list(b) + body), s16(list(s) + side_body)


def small_walk(frame, step):
    """half a body's worth of stride: drop a row, and lift the foot on one side"""
    f = [" " * 16] + list(frame[:-1])
    rows = [list(r) for r in f]
    lift = range(0, 8) if step == 1 else range(8, 16)
    for x in lift:
        if rows[15][x] != " ":
            rows[14][x] = rows[15][x] if rows[14][x] == " " else rows[14][x]
            rows[15][x] = " "
    return ["".join(r) for r in rows]


def small_raise(frame, colour):
    f = [list(r) for r in frame]
    for y in range(7, 12):
        f[y][13] = "K"; f[y][14] = colour; f[y][15] = "K"
    f[6][14] = "K"
    return ["".join(r) for r in f]


def small_figure(front, back, side, extra_hand=None):
    out = [front, back, side, small_walk(front, 1), small_walk(front, 2), small_walk(back, 1),
           small_walk(back, 2), small_walk(side, 1), small_walk(side, 2)]
    if extra_hand:
        out.append(small_raise(front, extra_hand))
    return out


# ------------------------------------------------------------------ geometry: a 32x32 sprite
def _to32(rows):
    """pad a drawing to a 32-row frame, sitting on the bottom row BUT ONE

    bob() makes its down-frame by prepending a row and dropping the last, so anything drawn on row
    31 loses its bottom edge on every other frame -- a wheel would flicker its rim. Leave 31 usable
    rows and keep the last empty.
    """
    rows = list(rows)
    assert len(rows) <= 31, "a 32x32 frame has 31 usable rows, got %d" % len(rows)
    return [""] * (31 - len(rows)) + rows + [""]


def h32(rows):
    return [r + r[::-1] for r in _fit(_to32(rows), 16)]


def s32(rows):
    return _fit(_to32(rows), 32)


def big_figure(front, back, side):
    """ten frames: the rider bobs and the wheels turn rather than legs walking"""
    def bob(frame, step):
        if step == 1:
            return [" " * 32] + list(frame[:-1])
        return list(frame[1:]) + [" " * 32]
    return [front, back, side, bob(front, 1), bob(front, 2), bob(back, 1), bob(back, 2),
            bob(side, 1), bob(side, 2), front]


# ================================================================== the five
# npc_pink: a s S peach  e dark brown  p pink  P rose  m dark rose  c light blue  B blue
#           n dark navy  w pale grey  g grey  G dark grey  W white  K black
PIGLET = small_fig(small_mammal("p", "P", "P"), small_body("c", "n"), small_side_body("c", "n"))

# npc_white: a s S peach  e dark red-brown  T sand-gold  t olive  u dark olive  R orange-red
#            r red-brown  E darkest brown  w pale grey  g grey  G dark grey  W white  K black
BEARCUB = small_fig(small_mammal("e", "E", "S"), small_body("w", "E"), small_side_body("w", "E"))
CYGNET = small_fig(small_bird("W", "T"), small_ring("R", "w"), small_side_ring("R", "w"))

# npc_blue: a s S peach  e dark brown  y yellow  o gold  Y dark gold  v light purple  V purple
#           D dark purple-grey  O orange  r red  d dark brown  W white  K black
DUCKLING = small_fig(small_bird("y", "O"), small_ring("W", "v"), small_side_ring("W", "v"))

# ------------------------------------------------------------------ the BIKER, 32x32: a boar
# The rider and the machine are one picture. Sixteen columns mirrored give the front and back; the
# side is drawn whole, because a bike in profile is not symmetric.
# A row that reaches column 15 becomes TWELVE pixels wide once mirrored, so the first draft's wheel
# was a bar across the machine and its snout was a band across the face. Head on, a wheel is narrow:
# it stops three columns from the centre. The handlebars are what give the thing its width instead.
# Measured off vanilla's own front frame rather than invented, which is what the first three drafts
# got wrong. Vanilla's ink occupies rows 10-31 ONLY, is at most FOURTEEN columns across (9..22), and
# tapers symmetrically to two pixels at the bottom: a lozenge, not a machine with its arms out. The
# bars are two small grips at the rider's shoulders, and the wheel is DARK with one rose stripe --
# a pale rectangle there reads as a licence plate.
BOAR_FRONT = h32([
    "              KK",      # the crown: vanilla starts 4 wide and widens by two a row
    "             KSS",
    "            KSSS",
    "           KSSSS",
    "          KSKSSS",      # the eye
    "         KSSeeee",      # the snout, dark
    "         KWeeeee",      # a tusk beside it
    "          KKeeee",
    "           Knnnn",      # the jacket
    "          Knnnnn",
    "         Knnnnnn",      # widest: mirrors to fourteen, exactly vanilla's
    "        KGnnnnnn",      # the grip, tucked at the shoulder
    "         Knnnnnn",
    "         Kgggggg",      # the machine, silver under him
    "        Kggggggg",
    "        KGgggggg",
    "         KGggggg",
    "          Kggggg",
    "          KnnGGG",      # darkening into the wheel
    "           Knnnn",
    "            KPnn",      # one rose stripe on the tyre
    "             Knn",
    "              KK",
])
BOAR_BACK = h32([
    "              KK",
    "             KSS",
    "            KSSS",
    "           KSSSS",
    "          KSSSSS",
    "         KSSSSSS",
    "         KSSSSSS",
    "          KKSSSS",
    "           Knnnn",
    "          Knnnnn",
    "         Knnnnnn",
    "        KGnnnnnn",
    "         Knnnnnn",
    "         Kgggggg",
    "        Kggggggg",
    "        KGgggggg",
    "         KGggggg",
    "          Kggggg",
    "          KnnGGG",
    "           Knnnn",
    "            KPnn",
    "             Knn",
    "              KK",
])
BOAR_SIDE = s32([
    "", "", "",
    "            KKKK",
    "           KSSSSK",
    "          KSSSSSSK",
    "         KSKSSSSSK",
    "        KWSSSSSSK",             # the tusk points the way he faces
    "       KeeeSSSSK",
    "        KKeeSSK",
    "          KKSSK",
    "         KnnnnnK",
    "        KnnnnnnnK",
    "       KnnnnnnnnK",
    "      KSnnnnnnnnK",
    "      KKnnnnnnnnK",
    "        KnnnnnnK",
    "     KKKKGGGGGGKKKK",
    "   KKGGGGggggggGGGGKK",
    "  KGGggggggggggggggGGK",
    "  KnnGGGGGGGGGGGGGGnnK",
    "  KnnnnnnnnnnnnnnnnnnK",
    "   KKnnnnKKKKKKnnnnKK",
    "  KwwwwK        KwwwwK",        # two wheels
    " KwGGGGwK      KwGGGGwK",
    " KwGGGGwK      KwGGGGwK",
    "  KwwwwK        KwwwwK",
    "   KKKK          KKKK",
])
BIKER = (BOAR_FRONT, BOAR_BACK, BOAR_SIDE)


SHEETS = [   # vanilla's sheet, ours, frames, frame size, palette letters, palette file, raised hand
    ("piglet",   "little_girl.png",   PIGLET,   10, 16, PINK,  "npc_pink.pal",  "p"),
    ("bear cub", "little_boy.png",    BEARCUB,   9, 16, WHITE, "npc_white.pal", None),
    ("duckling", "tuber_m_water.png", DUCKLING, 10, 16, BLUE,  "npc_blue.pal",  "y"),
    ("cygnet",   "tuber_f.png",       CYGNET,   10, 16, WHITE, "npc_white.pal", "W"),
]

# THE BIKER IS STILL NOT WRITTEN -- four drafts, and the halves failed in turn. BIKER above is kept
# because draft four solved one of them and that measurement should not be lost.
#
# Drafts 1-3 lost the MACHINE. Handlebars drawn as a one-pixel line standing clear of the body read
# as outstretched arms; the head-on wheel read as a white box, a licence plate rather than a wheel;
# and the whole thing was bulkier than the sprite it replaced. Only the side view ever worked.
#
# Draft 4 fixed exactly that, by MEASURING VANILLA instead of judging my own drawing: its front frame
# occupies rows 10-31 only, is at most FOURTEEN columns wide, and tapers symmetrically to two pixels
# at the bottom. Every earlier draft was wider than the thing it replaced. The silhouette and the
# side view are right now.
#
# What draft 4 still gets wrong is the FACE, and it is the vulture's failure again: a peach dome with
# a dark horizontal band reads as a person wearing something.
#
#   * the snout spans the full width of the head, so it reads as a visor, not a snout
#   * the tusks sit at the temples as two white pixels, where they read as ears or as highlights
#   * the crown is bare, where vanilla's rider has an unmistakable crest doing all the silhouette work
#
# Draft 5: narrow the snout to the bottom-centre four columns with the face left clear above it, put
# the tusks immediately beside the snout rising upward, and give the crown a feature -- a boar's ear
# pair or a bristle ridge -- so the head has a top silhouette instead of a dome. Keep the geometry.


def check(name, frames, index, side):
    for n, f in enumerate(frames):
        assert len(f) == side, "%s frame %d is %d rows, want %d" % (name, n, len(f), side)
        for r, line in enumerate(f):
            assert len(line) == side, "%s frame %d row %d is %d wide, want %d: %r" % (name, n, r, len(line), side, line)
            bad = set(line) - set(index)
            assert not bad, "%s frame %d row %d has %r" % (name, n, r, bad)


def build(frames, index, pal, side):
    img = Image.new("P", (side * len(frames), side))
    flat = [c for rgb in pal for c in rgb]
    img.putpalette(flat + [0] * (768 - len(flat)))
    px = img.load()
    for n, f in enumerate(frames):
        for y, line in enumerate(f):
            for x, ch in enumerate(line):
                px[n * side + x, y] = index[ch]
    return img


def main():
    rows, built = [], []
    for name, filename, art, want, side, index, palname, hand in SHEETS:
        if side == 16:
            frames = small_figure(art[0], art[1], art[2], extra_hand=hand)
        else:
            frames = big_figure(art[0], art[1], art[2])
        check(name, frames, index, side)
        old = Image.open(os.path.join(PEOPLE, filename))
        assert len(frames) == want, "%s: %d frames, the table wants %d" % (name, len(frames), want)
        img = build(frames, index, read_pal(palname), side)
        assert img.size == old.size, "%s: %s would change size %s -> %s" % (name, filename, old.size, img.size)
        built.append((filename, img))
        bg = Image.new("RGB", img.size, (150, 150, 150))
        bg.paste(img.convert("RGB"), (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        rows.append(bg)
        rows.append(old.convert("RGB"))
    w = max(r.width for r in rows) * 5
    h = sum(r.height * 5 + 12 for r in rows)
    out = Image.new("RGB", (w, h), (60, 60, 60))
    y = 0
    for r in rows:
        out.paste(r.resize((r.width * 5, r.height * 5), Image.NEAREST), (0, y))
        y += r.height * 5 + 12
    out.save(PREVIEW)
    print("  %d sheets -> preview %s (each: ours, then vanilla's under it)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
        print("  written %d sheets in place: %s" % (len(built), ", ".join(f for f, _ in built)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The PAIR classes, redrawn as the two animals that actually stand there (T-128; vision.md 9.4).

    python3 tools/genpairs.py            # preview to /tmp/pairs_<name>.png, before and after
    python3 tools/genpairs.py --write    # the portraits, and their palettes

A PAIR CLASS IS ONE TRAINER STANDING AS TWO MAP OBJECTS, so "one species per class" is the wrong
question to ask of it: the picture has to be the two animals those two sheets ALREADY are. T-126
settled the method on COOL_COUPLE -- two ibexes became a wolf and a falcon -- and gave the reason a
pair SHEET is not the answer: it would serve one battle in the game and leave both singles, which
are correct everywhere else they stand, still disagreeing with it.

    TWINS         two quails   -> two PIGLETS         both objects are LITTLE_GIRL       x8
    YOUNG_COUPLE  two swans    -> an OX and a GAZELLE MAN and BEAUTY                      x6
    SIS_AND_BRO   two rabbits  -> a DUCKLING and an AXOLOTL  TUBER_M and SWIMMER_F        x6
    CRUSH_KIN     two wolverines -> a KANGAROO and a wolverine  BLACK_BELT and CRUSH_GIRL x4

CRUSH_KIN is the one that was half right already: `crush_girl` IS the wolverine, so only the figure
standing for BLACK_BELT changes. SR_AND_JR and OLD_COUPLE are NOT here -- neither stands on a map.

NO COLOUR IS ADDED, AND THAT WAS CHECKED RATHER THAN ASSUMED. The obvious move is to re-dye the
indices the old head had to itself; there are NONE. Every one of these four heads draws from the
same ramp as the body it sits on, so a re-dye would repaint the clothes. Each new head is therefore
drawn inside the sixteen the picture already has -- a cream piglet with a red-brown snout, a
kangaroo in the wolverine's own greys -- which is the same constraint the overworld sheets work
under and it is the reason they look like they belong.

EACH HEAD IS A MIRRORED HALF. A nine- or ten-column half becomes an eighteen- or twenty-wide head,
which is both figures' own width, and it makes a symmetry error impossible rather than unlikely.
A head that is turned is drawn full width instead, as the couple's falcon is.

THE BODIES ARE ASSERTED BYTE-IDENTICAL after every run. Only the cleared boxes may change.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import GBA

WRITE = "--write" in sys.argv
PICS = os.path.join(GBA, "graphics/trainers/front_pics")
PALS = os.path.join(GBA, "graphics/trainers/palettes")


# ---------------------------------------------------------------- CRUSH_KIN: a KANGAROO (left)
# The wolverine on the right is already what `crush_girl` is and is not touched. The left figure
# stands for BLACK_BELT, whose own portrait is a kangaroo in a gi -- and MEASURING that portrait is
# what got this right on the fourth try. Two drafts built the head WIDE, filling the wolverine's own
# width, and both read as a helmet with horns: on a wide flat skull any pair of uprights at the
# corners is a horn, which engine.md has now recorded three times. The kangaroo's head is a NARROW
# WEDGE -- twelve columns against a twenty-column body -- tapering to a dark nose, and its ears
# angle OUT from the crown rather than standing on the corners.
# w cream  l pale grey  s mid  b warm mid  n brown  m dark brown  D darkest  K ink
KANGAROO = [
    "..Kl......",
    "..KlK.....",
    "..KslK....",
    "...KsslKKK",
    "...Kssssss",
    "...KsKssss",
    "...Ksssssb",
    "....Kssssb",
    "....Ksssbb",
    ".....Kssbb",
    ".....Kssbb",
    "......Ksbb",
    "......KsbK",
    "......Ksss",
]


# ---------------------------------------------------------------- TWINS: two PIGLETS
# Both objects are LITTLE_GIRL, whose sheet is a piglet. The read is the SNOUT -- a flat disc with
# two nostrils, set low on a round head -- and small ears at the corners, which are not horns
# because they lie over the crown rather than standing off it.
# w cream  b warm grey  m mid  r red-brown  d dark  K ink
PIGLET = [
    ".Kbbwwww",
    ".Kbbwwww",
    ".KbbKwww",
    ".Kwwwwww",
    ".KwKwwww",
    ".Kwwwwww",
    "..Kwwwww",
    "..KKrrrr",
    "..KKrKrr",
    "..KKrrrr",
    "...KKKKK",
    "...Kwwww",
    "....Kwww",
    "....Kmmm",
]

# ---------------------------------------------------------------- YOUNG_COUPLE: an OX and a GAZELLE
# MAN is an ox and BEAUTY is a gazelle, and both carry horns, so the two are separated by WHAT KIND:
# the ox's are white, short and curve in over a heavy grey muzzle; the gazelle's are dark, long and
# sweep back and out over a narrow cream wedge. The swans' necks go with them.
# W white  w pale  c cream  g grey  m grey  t tan  b brown  K ink
OX = [
    ".KW.....",
    "..KWK...",
    "...KWK..",
    "..KbbKKK",
    ".Kbbbbbb",
    ".Kbbbbbb",
    ".KbKbbbb",
    ".Kbbbbbb",
    ".Kbbbmmm",
    "..Kbmmmm",
    "..Kbmmmm",
    "..KbmmKm",
    "..Kbmmmm",
    "...KKmmm",
    "....Kmmm",
    "....Kmmm",
    "....Kbbb",
    "....Kbbb",
]
GAZELLE = [
    "...KbbK.",
    "...KbbK.",
    "..KbbK..",
    "..KbbK..",
    ".KbbK...",
    "..Kttttt",
    ".Ktttttt",
    "KtKttttt",
    "KtKcKttt",
    "KtKccttt",
    "..Kccctt",
    "..Kccctt",
    "...Kcccc",
    "...Kcccc",
    "....Kccc",
    "....KcKc",
    "....Kccc",
    ".....Ktt",
    ".....Ktt",
]

# ---------------------------------------------------------------- SIS_AND_BRO: a DUCKLING and an AXOLOTL
# TUBER_M is a duckling and SWIMMER_F is an axolotl, and the rabbits' long ears come off both. The
# axolotl is the harder one and its whole read is the FRILLS -- three stalks either side, drawn
# clear of the head so they are gills and not more ears.
# W cream  y pale  Y yellow  n tan  b brown  K ink
DUCKLING = [
    ".......", ".......", ".......", ".......", ".......",
    ".......", ".......", ".......", ".......",
    "...KKKK",
    "..KYYYY",
    ".KYYYYY",
    ".KYKYYY",
    ".KYYYYY",
    ".KYYYnn",
    "..KYnnn",
    "..KYKnn",
    "..KYYYY",
    "...KYYY",
    "....KYY",
    "....KYY",
    "....KYY",
    "....KYY",
]
AXOLOTL = [
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "...KKKKK",
    "..KWWWWW",
    "bbKWWWWW",
    "..KWKWWW",
    "bbKWWWWW",
    "..KWWWWW",
    "bbKWWWWW",
    "..KWWWWW",
    "..KWKKWW",
    "..KWWWWW",
    "...KWWWW",
    "....KWWW",
    "....KWWW",
    "....KWWW",
    "....KWWW",
]


# ---------------------------------------------------------------- and the FEET, which are not a detail
# A piglet on bird feet is the same contradiction one figure down. The twins stood on splayed quail
# feet and the couple on webbed ones; the legs above them are already thin enough for any of these
# four, so only the last few rows change -- a cleft trotter for the piglets, a cloven hoof for the ox
# and the gazelle. These are drawn FULL WIDTH rather than as mirrored halves, because the two legs of
# one figure are not symmetrical about the figure's own centre.
TROTTERS = [
    "....dd.......dd.....",
    "...Kddd.....Kddd....",
    "..KdddK.....KdddK...",
    "..KdKdK.....KdKdK...",
    "..KKKKK.....KKKKK...",
]
OX_FEET = [
    "......b......bb.........",
    ".....Kbb....Kbbb........",
    "....Kbbbb...Kbbbb.......",
    "....KbbbK...KbbbK.......",
    "....KbKbK...KbKbK.......",
    "....KKKKK...KKKKK.......",
]
GAZELLE_FEET = [
    ".........bb......b......",
    "........Kbbb....Kbb.....",
    ".......Kbbbb...Kbbbb....",
    ".......KbbbK...KbbbK....",
    ".......KbKbK...KbKbK....",
    ".......KKKKK...KKKKK....",
]


JOBS = [
    dict(pic="crush_kin", letters={".": None, "w": 1, "l": 2, "s": 5, "b": 6, "n": 7, "m": 10, "D": 13, "K": 15},
         figures=[dict(box=(6, 30, 12, 25), x0=9, y0=12, art=KANGAROO,
                       why="BLACK_BELT is a kangaroo, and this figure is standing for him")]),
    dict(pic="twins", letters={".": None, "w": 1, "l": 2, "f": 3, "s": 4, "m": 5, "b": 6, "r": 12, "d": 13, "K": 15},
         figures=[dict(box=(4, 27, 12, 25), x0=7, y0=12, art=PIGLET, why="both objects are LITTLE_GIRL, a piglet"),
                  dict(box=(38, 61, 12, 25), x0=41, y0=12, art=PIGLET, why="and so is the other one"),
                  dict(box=(5, 27, 59, 63), x0=6, y0=59, art=TROTTERS, why="and a piglet does not stand on quail feet"),
                  dict(box=(38, 60, 59, 63), x0=39, y0=59, art=TROTTERS, why="nor does the other one")]),
    dict(pic="young_couple", letters={".": None, "W": 1, "w": 2, "l": 3, "y": 4, "Y": 5, "c": 6, "g": 7,
                                      "G": 8, "t": 9, "m": 10, "b": 13, "v": 14, "K": 15},
         figures=[dict(box=(2, 27, 8, 25), x0=6, y0=8, art=OX, why="MAN is an ox"),
                  dict(box=(38, 63, 8, 26), x0=42, y0=8, art=GAZELLE, why="BEAUTY is a gazelle"),
                  dict(box=(3, 28, 58, 63), x0=4, y0=58, art=OX_FEET, why="and an ox has a cloven hoof, not a web"),
                  dict(box=(37, 62, 58, 63), x0=38, y0=58, art=GAZELLE_FEET, why="and so does a gazelle")]),
    dict(pic="sis_and_bro", letters={".": None, "W": 1, "y": 2, "Y": 3, "t": 5, "T": 6, "n": 9,
                                     "v": 11, "b": 13, "K": 15},
         figures=[dict(box=(2, 25, 0, 22), x0=6, y0=0, art=DUCKLING, why="TUBER_M is a duckling"),
                  dict(box=(38, 62, 0, 22), x0=42, y0=0, art=AXOLOTL, why="SWIMMER_F is an axolotl")]),
]


def mirrored(rows):
    out = []
    for r, row in enumerate(rows):
        assert 7 <= len(row) <= 64, "row %d is %d columns: %r" % (r, len(row), row)
        out.append(row if len(row) > 10 else row + row[::-1])   # ten or fewer is a HALF, and is mirrored
    assert len({len(r) for r in out}) == 1, "a head is drawn all one way or all the other"
    return out


def apply(img, job):
    px = img.load()
    for f in job["figures"]:
        x0, x1, y0, y1 = f["box"]
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px[x, y] = 0
        for r, row in enumerate(mirrored(f["art"])):
            for c, ch in enumerate(row):
                v = job["letters"][ch]
                if v is not None:
                    assert x0 <= f["x0"] + c <= x1 and y0 <= f["y0"] + r <= y1, \
                        "%s: the head draws outside the box it cleared at (%d,%d)" % (job["pic"], f["x0"] + c, f["y0"] + r)
                    px[f["x0"] + c, f["y0"] + r] = v


def main():
    for job in JOBS:
        name = job["pic"]
        src = Image.open(os.path.join(PICS, name + "_front_pic.png"))
        assert src.mode == "P" and src.size == (64, 64), "%s is %s %s" % (name, src.mode, src.size)
        pal = src.getpalette()[:48]
        out = src.copy()
        apply(out, job)
        boxes = [f["box"] for f in job["figures"]]
        sp, op = src.load(), out.load()
        for y in range(64):
            for x in range(64):
                if not any(x0 <= x <= x1 and y0 <= y <= y1 for x0, x1, y0, y1 in boxes):
                    assert sp[x, y] == op[x, y], "%s: the body changed at (%d,%d)" % (name, x, y)
        prev = Image.new("RGB", (64 * 6 * 2 + 12, 64 * 6), (48, 48, 52))
        prev.paste(src.convert("RGB").resize((384, 384), Image.NEAREST), (0, 0))
        prev.paste(out.convert("RGB").resize((384, 384), Image.NEAREST), (396, 0))
        prev.save("/tmp/pairs_%s.png" % name)
        print("  %-14s %d figure(s) redrawn -> /tmp/pairs_%s.png (before, after)" % (name, len(job["figures"]), name))
        for f in job["figures"]:
            print("                 %s" % f["why"])
        if WRITE:
            out.save(os.path.join(PICS, name + "_front_pic.png"), bits=4)
            with open(os.path.join(PALS, name + ".pal"), "w") as fh:
                fh.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join(
                    "%d %d %d\r\n" % tuple(pal[i * 3:i * 3 + 3]) for i in range(16)))
            #  T-177's outline, which every picture of ours carries: drawn by the same pass, so this write lands where the
            #  tree is and does not take it off again (T-293).
            import gbaoutline
            gbaoutline.main(only=[name], write=True)
            print("                 written, and its palette; no colour changed")


if __name__ == "__main__":
    main()

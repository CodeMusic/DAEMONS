#!/usr/bin/env python3
"""THE COOL COUPLE, redrawn as the two animals that actually stand there (T-126; vision.md 9.4).

    python3 tools/gencouple.py            # preview to /tmp/couple.png (before, after, and the two overworld sheets)
    python3 tools/gencouple.py --write    # the portrait, and its palette

COOL_COUPLE IS THE ONE PAIR CLASS IN THE MISMATCH, and a pair cannot be answered the way the other
four were. A Burglar is one trainer on one tile, so the fix is a sheet of its own. The couple is ONE
trainer standing as TWO objects -- VICTORY ROAD 3F puts a COOLTRAINER_M and a COOLTRAINER_F side by
side and both run the same battle -- and those two sheets are a WOLF and a FALCON under T-120. The
portrait drew them as two ibexes, so the screen showed a wolf and a falcon walking up to a picture of
two goats. Giving the couple a sheet would be the wrong move: it would need a new pair sprite for one
battle in the game and would leave the wolf and the falcon still wrong. Redrawing the PICTURE fixes
it exactly, and costs one picture.

NOTHING BELOW THE COLLAR CHANGES AND NO COLOUR IS ADDED. The two figures, their tunics, belts, boots
and stance are ours already and are correct; only the heads were the wrong species. Rows 0-23 hold
nothing but head -- measured, the green of the shoulders starts at row 24 -- so the heads are cleared
and redrawn in place, on the same sixteen colours, and the necks land on the same shoulders.

EACH HEAD IS DRAWN AS A HALF AND MIRRORED. Nine columns become eighteen, which is both figures' own
width, and it makes a symmetry error impossible rather than merely unlikely -- the thing that went
wrong four times when this project drew by eye.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import GBA, PEOPLE

PREVIEW = "/tmp/couple.png"
WRITE = "--write" in sys.argv
PIC = os.path.join(GBA, "graphics/trainers/front_pics/cool_couple_front_pic.png")
PAL = os.path.join(GBA, "graphics/trainers/palettes/cool_couple.pal")

HEAD_TOP, HEAD_END = 0, 24                 # the rows that hold head and nothing else
LEFT_X, RIGHT_X = 2, 44                    # where each figure's head sits, measured off the ibexes

# the portrait's own sixteen, by role rather than by number
LET = {".": None, "K": 15, "D": 14, "d": 13, "g": 12, "n": 10, "m": 9, "b": 6, "s": 5, "f": 3, "l": 2, "w": 1}

# ---------------------------------------------------------------- the WOLF (cooltrainer_m)
# THE SKULL IS TWELVE WIDE, NOT EIGHTEEN. The ibexes measured eighteen across because of the
# HORNS -- their faces were nine -- and a head drawn to the full width came out a bear.
# Ears up and forward, and the muzzle carried on the pale ramp so the nose reads as
# the darkest thing on the face. The glint is one pixel: two dark pixels alone are a mask, not an eye.
WOLF = [
    "..K......",
    ".KdK.....",
    ".KdbK....",
    ".KdbKKKKK",
    ".KKdsssss",
    "..Kdsssss",
    "..Kdfffff",
    "..Kdfffff",
    "..KdwKlff",
    "..KdfKlff",
    "..Kdffllf",
    "...Kdflww",
    "....Kflww",
    ".....KlwK",
    ".....Kwww",
    "......Kww",
    "......Kss",
    "......Kss",
]

# ---------------------------------------------------------------- the FALCON (cooltrainer_f)
# THE HEAD IS TURNED, AND THAT IS THE WHOLE FIX. Three front-facing drafts failed the same way: a
# beak pointed at the viewer is a nose, the cheeks either side of it are a face, and each one came
# out a person with a bowl cut. A bird turns its head, and in PROFILE the beak is a hooked wedge
# against the sky, which nothing else is. So this head is not mirrored -- it is drawn full width,
# looking left, across at the wolf -- and the neck still lands on the same shoulders.
FALCON = [
    "......KKKKK.......",
    "....KKdddddK......",
    "...KdddddddK......",
    "..KddddddddK......",
    "..KdddlllddK......",
    ".KwwwKlKlddK......",
    "KwwwwKlllddK......",
    ".KwwwKdddddK......",
    "..KnwKdddddK......",
    "...KKKdddddK......",
    "....KddddddK......",
    ".....KdddddK......",
    "......KddddK......",
    "......KddddK......",
    "......KssssK......",
    "......KssssK......",
    ".....KssssssK.....",
    ".....KssssssK.....",
]


def mirrored(rows):
    """nine columns mirrored to eighteen, or eighteen drawn outright where the head is turned"""
    for r, row in enumerate(rows):
        assert len(row) in (9, 18), "row %d is %d columns, not 9 or 18: %r" % (r, len(row), row)
        bad = set(row) - set(LET)
        assert not bad, "row %d has %r" % (r, bad)
    assert len(rows) == HEAD_END - 6, "%d rows drawn, %d to fill" % (len(rows), HEAD_END - 6)
    assert len({len(r) for r in rows}) == 1, "a head is drawn all one way or all the other"
    return [row if len(row) == 18 else row + row[::-1] for row in rows]


def draw(img, x0, half):
    px = img.load()
    for y in range(HEAD_TOP, HEAD_END):
        for x in range(max(0, x0 - 4), min(64, x0 + 22)):
            px[x, y] = 0
    for r, row in enumerate(mirrored(half)):
        for c, ch in enumerate(row):
            if LET[ch] is not None:
                px[x0 + c, 6 + r] = LET[ch]


def main():
    src = Image.open(PIC)
    assert src.mode == "P" and src.size == (64, 64), "%s is %s %s" % (PIC, src.mode, src.size)
    pal = src.getpalette()[:48]
    body = [(x, y) for y in range(HEAD_END, 64) for x in range(64) if src.load()[x, y]]
    out = src.copy()
    draw(out, LEFT_X, WOLF)
    draw(out, RIGHT_X, FALCON)
    assert [(x, y) for y in range(HEAD_END, 64) for x in range(64) if out.load()[x, y]] == body, \
        "the bodies changed; only the heads may"

    ow = [Image.open(os.path.join(PEOPLE, n)) for n in ("cooltrainer_m.png", "cooltrainer_f.png")]
    scale = 6
    prev = Image.new("RGB", (64 * scale * 2 + 16, 64 * scale + 16 + 32 * 4 * 2), (60, 60, 60))
    prev.paste(src.convert("RGB").resize((64 * scale,) * 2, Image.NEAREST), (0, 0))
    prev.paste(out.convert("RGB").resize((64 * scale,) * 2, Image.NEAREST), (64 * scale + 16, 0))
    for i, o in enumerate(ow):
        prev.paste(o.convert("RGB").resize((o.width * 4, 128), Image.NEAREST), (0, 64 * scale + 16 + 128 * i))
    prev.save(PREVIEW)
    print("  the couple -> preview %s (the ibexes, then the wolf and the falcon, then the two sheets they walk on)" % PREVIEW)

    if WRITE:
        out.save(PIC, bits=4)
        with open(PAL, "w") as fh:
            fh.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join(
                "%d %d %d\r\n" % tuple(pal[i * 3:i * 3 + 3]) for i in range(16)))
        print("  written the portrait and its palette; no colour changed")


if __name__ == "__main__":
    main()

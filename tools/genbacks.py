#!/usr/bin/env python3
"""The battle BACK pics -- the player seen from behind, throwing (T-120; vision.md 9.4).

    python3 tools/genbacks.py            # preview to /tmp/backs_ow.png
    python3 tools/genbacks.py --write    # the four strips, and their palettes

A back pic is not one picture. It is a STRIP of 64x64 frames making a throw, and the strip's
byte length is hard-coded in C:

    gTrainerBackPicTable[] = { ... gTrainerBackPic_Red, 0x2800 ... gTrainerBackPic_OldMan, 0x2000 }

0x2800 is FIVE frames of 64x64 at 4bpp and 0x2000 is FOUR. A strip of the wrong height is a size
mismatch rather than a cosmetic bug, so the counts here are fixed: red 5, leaf 5, pokedude 4,
old man 4.

WHO THEY ARE. 9.10 made playerGender a pure sprite selector, so red_back_pic is LOGIC and
leaf_back_pic is INTUITION -- the player, who is already drawn: gfx/characters/player_logic.jpeg
and the reference sheets player_ow_ref_back/side.png. The player is a GREY MONKEY (genfolk.py:
"MOM, a grey monkey, the player's own kind") in a wide brown hat and a long cream coat, a dark
satchel on a strap across the back, black boots, and a long curling tail. These backs match that
character; they do not invent a second one.

WHAT MOVES BETWEEN FRAMES. Measured off vanilla: 1100-2100 pixels change per frame, and the
bounding boxes span most of the canvas -- but laid out side by side, the body, hat and coat hold
still and it is the NEAR ARM sweeping forward with a shoulder and head tilt. So each character is
drawn ONCE from behind and the arm is redrawn per frame, which is how the walk cycles were built.

THE PALETTE IS OURS HERE, unlike the overworld sheets. Each back pic has its own 16 colours in
graphics/trainers/palettes/<name>.pal and this tool writes them -- so the player's cream and brown
can be exact. INDEX 0 IS THE TRANSPARENT SLOT AND ITS COLOUR DIFFERS PER FILE: red and leaf use a
lavender (131,123,164), the old man and the pokedude the usual key green. Each file keeps its own.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import GBA

PREVIEW = "/tmp/backs_ow.png"
WRITE = "--write" in sys.argv
BACKS = os.path.join(GBA, "graphics/trainers/back_pics")
PALS = os.path.join(GBA, "graphics/trainers/palettes")

# ---------------------------------------------------------------- the player's sixteen
#  0 transparent   1 coat cream   2 coat shade   3 hat brown   4 hat shade   5 fur grey
#  6 fur shade     7 fur dark     8 boot black   9 strap dark  10 satchel    11 satchel light
# 12 tail grey    13 tail shade  14 white       15 outline black
PLAYER = ["a", "c", "C", "h", "H", "f", "F", "d", "b", "s", "g", "G", "t", "T", "W", "K"]
LOGIC_PAL = [(131, 123, 164), (255, 246, 222), (222, 205, 172), (180, 131, 65), (139, 98, 41),
             (172, 164, 156), (131, 123, 115), (90, 82, 74), (33, 33, 41), (49, 49, 57),
             (106, 106, 115), (148, 148, 156), (164, 156, 148), (115, 106, 98), (255, 255, 255), (0, 0, 0)]
INTUITION_PAL = list(LOGIC_PAL)          # the same person; 9.10 makes the choice a sprite, not a species

LETTERS = {ch: i for i, ch in enumerate(PLAYER)}
LETTERS[" "] = 0


def rows(*lines):
    return list(lines)


# The body, seen from behind: hat brim, coat back, the strap crossing it, the satchel, boots, tail.
# 32 columns drawn and mirrored would put the strap down the centre, so these are drawn whole at 64.
BODY = rows(
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                      KKKKKKKKKKKKKKKKKKKK                      ",
    "                  KKKKhhhhhhhhhhhhhhhhhhhhKKKK                  ",
    "              KKKKhhhhhhhhhhhhhhhhhhhhhhhhhhhhKKKK              ",
    "          KKKKhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhKKKK          ",
    "        KKhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhKK        ",
    "        KHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHK        ",
    "         KKKKKKKKKKHHHHHHHHHHHHHHHHHHHHHHHHKKKKKKKKKKKK         ",
    "                   KffffffffffffffffffffffK                     ",
    "                   KffffffffffffffffffffffK                     ",
    "                   KffffffffffffffffffffffK                     ",
    "                   KFFFFFFFFFFFFFFFFFFFFFFK                     ",
    "                  KKcccccccccccccccccccccccKK                   ",
    "                 KcccccccccccccccccccccccccccK                  ",
    "                KccccccccccccsccccccccccccccccK                 ",
    "               KcccccccccccccsccccccccccccccccK                 ",
    "              KfcccccccccccccsccccccccccccccccfK                ",
    "              KFcccccccccccccsccccccccccccccccFK                ",
    "              KdcccccccccccccsccccccccccccccccdK                ",
    "              KKcccccccccccccsscccccccccccccccKK                ",
    "               KccccccccccccccsscccccccccccccK                  ",
    "               KcccccccccccccccsgggggKcccccccK                  ",
    "               KcccccccccccccccKgGggGKcccccccK                  ",
    "               KcccccccccccccccKggggGKcccccccK                  ",
    "               KcccccccccccccccKgggggKcccccccK                  ",
    "               KccccccccccccccccKKKKKccccccccK                  ",
    "               KccccccccccccccccccccccccccccK                   ",
    "               KCccccccccccccccccccccccccccCK                   ",
    "               KCccccccccccccccccccccccccccCK                   ",
    "               KCcccccccccccKttKcccccccccccCK                   ",
    "               KCccccccccccKtTTtKccccccccccCK                   ",
    "               KCcccccccccKtTKKtKcccccccccCK                    ",
    "               KCccccccccKtTKKKtKccccccccCK                     ",
    "                KCcccccccKtTKccKtKcccccccCK                     ",
    "                KCccccccKtTKcccKtKccccccCK                      ",
    "                KCccccccKtKcccccKtKcccccCK                      ",
    "                KCcccccccKKcccccKtKcccccCK                      ",
    "                KCcccccccccccccKtTKccccCK                       ",
    "                KCccccccccccccKtTKcccccCK                       ",
    "                KCcccccccccccKtTKccccccCK                       ",
    "                KCccccccccccKtTKcccccccCK                       ",
    "                KCccccccccccKtKccccccccCK                       ",
    "                KCcccccccccccKKccccccccCK                       ",
    "                KCccccccccccccccccccccCK                        ",
    "                KKCccccccccccccccccccCKK                        ",
    "                  KCccccccccccccccccCK                          ",
    "                  KKCccccccccccccccCKK                          ",
    "                    KbbbbbKKKKbbbbbbK                           ",
    "                    KbbbbbKKKKbbbbbbK                           ",
    "                    KbbbbbK  KbbbbbbK                           ",
    "                    KbbbbbK  KbbbbbbK                           ",
    "                    KKKKKKK  KKKKKKKK                           ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
)

# The near arm, per frame of the throw. Drawn over the body at the shoulder, sweeping forward:
# down at rest, lifting, across the chest, extended, and following through.
ARMS = [
    [],                                                      # 0: at rest, the body's own arm serves
    [(18, 40, "KffK"), (19, 40, "KfFK"), (20, 41, "KffK"), (21, 42, "KfK")],
    [(16, 44, "KffK"), (17, 46, "KfFK"), (18, 48, "KffK"), (19, 50, "KfK")],
    [(15, 48, "KffffK"), (16, 52, "KfFFfK"), (17, 56, "KffK")],
    [(17, 46, "KfffK"), (18, 50, "KfFfK"), (19, 53, "KffK")],
]


def frame(body, arm):
    out = [list(r) for r in body]
    for y, x, patch in arm:
        for i, ch in enumerate(patch):
            if ch != " " and 0 <= x + i < 64 and 0 <= y < 64:
                out[y][x + i] = ch
    return ["".join(r) for r in out]


def check(name, frames):
    for n, f in enumerate(frames):
        assert len(f) == 64, "%s frame %d is %d rows" % (name, n, len(f))
        for r, line in enumerate(f):
            assert len(line) == 64, "%s frame %d row %d is %d wide" % (name, n, r, len(line))
            bad = set(line) - set(LETTERS)
            assert not bad, "%s frame %d row %d has %r" % (name, n, r, bad)


def strip(frames, pal):
    img = Image.new("P", (64, 64 * len(frames)))
    flat = [c for rgb in pal for c in rgb]
    img.putpalette(flat + [0] * (768 - len(flat)))
    px = img.load()
    for n, f in enumerate(frames):
        for y, line in enumerate(f):
            for x, ch in enumerate(line):
                px[x, n * 64 + y] = LETTERS[ch]
    return img


SHEETS = [   # vanilla's strip, how many frames C demands, the palette
    ("LOGIC",     "red_back_pic.png",  5, LOGIC_PAL),
    ("INTUITION", "leaf_back_pic.png", 5, INTUITION_PAL),
]


def main():
    built, rowsout = [], []
    for name, filename, want, pal in SHEETS:
        frames = [frame(BODY, ARMS[k]) for k in range(want)]
        check(name, frames)
        old = Image.open(os.path.join(BACKS, filename))
        assert len(frames) == old.size[1] // 64, "%s: %d frames, %s holds %d" % (
            name, len(frames), filename, old.size[1] // 64)
        img = strip(frames, pal)
        assert img.size == old.size, "%s: %s would change size %s -> %s" % (name, filename, old.size, img.size)
        built.append((filename, img, pal))
        wide = Image.new("RGB", (64 * want, 64), (60, 60, 60))
        for k in range(want):
            wide.paste(img.crop((0, k * 64, 64, (k + 1) * 64)).convert("RGB"), (k * 64, 0))
        rowsout.append(wide)
    out = Image.new("RGB", (max(r.width for r in rowsout) * 2, sum(r.height * 2 for r in rowsout)), (40, 40, 46))
    y = 0
    for r in rowsout:
        out.paste(r.resize((r.width * 2, r.height * 2), Image.NEAREST), (0, y))
        y += r.height * 2
    out.save(PREVIEW)
    print("  %d strips -> preview %s" % (len(built), PREVIEW))
    if WRITE:
        for filename, img, pal in built:
            img.save(os.path.join(BACKS, filename), bits=4)
            with open(os.path.join(PALS, filename.replace(".png", ".pal")), "w") as f:
                f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal))
        print("  written %d strips and their palettes" % len(built))


if __name__ == "__main__":
    main()

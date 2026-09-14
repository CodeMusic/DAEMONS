#!/usr/bin/env python3
"""Draw the player's overworld sprites on foot -- REASON and INSTINCT.

    python3 tools/gbaplayer.py            # preview to /tmp/player_ow.png
    python3 tools/gbaplayer.py --write    # six sheets and player.pal

THE GBA PLAYER, not the Game Boy one -- tools/genplayer.py is the 16x16 DMG
figure and stays as it is. This is the grey monkey from the portraits in
gfx/characters/player_*.jpeg: a wide brown hat, a long cream coat open over
black, black boots, the strap across the chest to the BOX at the hip, and the
tail. The side and back were redrawn from the portrait through the n8n
daemon/sprite workflow so they stay one figure (player_ow_ref_*.png).

ON FOOT ONLY, THIS PASS. Per figure, the sheets it writes and what the engine
reads out of each:

    red_normal.png      9 frames   0 down  1 up  2 left  3,4 / 5,6 / 7,8 walk
    red_surf_run.png   14 frames   0-2 SURFING (kept exactly as they are)
                                   3-5 run down: the pose, then two strides
                                   6-8 run up    9-11 run left
                                   12,13 the head-shake, looking left, right
    red_item.png        9 frames   0-4 raise the arm (sAnim_FieldMove)
                                   0,1,5-8 hold up the VS SEEKER, flashing

and the same three for green_*. Bike, surf and fishing are the next pass.

THE PALETTE IS SHARED, SO IT IS REMAPPED BY ROLE. Both figures and all seven
sheets draw from player.pal, including the four this pass does not touch. So
each index keeps the job vanilla gave it -- the cap's red becomes the hat's
brown, skin becomes fur, the white shirt the cream coat, the backpack the
BOX -- and a vanilla bike or surf frame reads as a rough version of this
figure until it is drawn, rather than as noise.

ONE DIFFERENCE BETWEEN THE TWO, AND IT IS THE TAIL. 9.10: "two people, and the
player picks the one they would rather be", deliberately not a matched pair of
opposites. At sixteen pixels a face cannot carry that and a tail can: REASON's
curls up on its right, INSTINCT's hangs and curls down on its left. It reads
from every side and costs no colour.

VANILLA'S IDIOM FOR EVERYTHING ELSE. The hat brim is the widest line on the
figure, as the GB player's was. Walk frames drop a row and swing the arms
against the legs; run frames flare the coat.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
PAL = os.path.join(GBA, "graphics/object_events/palettes/player.pal")
PREVIEW = "/tmp/player_ow.png"
WRITE = "--write" in sys.argv

# Each entry keeps VANILLA'S ROLE for that index, so the sheets this pass does
# not draw still come out as roughly this figure.
PALETTE = [
    (131, 123, 164),  # 0     transparent (vanilla's key)
    (112, 104, 104),  # 1  f  fur, shade           (vanilla: skin, shade)
    (176, 168, 164),  # 2  F  fur, face and hands  (vanilla: skin)
    (144, 136, 132),  # 3  m  fur                  (vanilla: skin, mid)
    (104,  66,  40),  # 4  h  strap; hat, deep     (vanilla: hair, outline brown)
    ( 52,  52,  60),  # 5  B  black clothes        (vanilla: jeans)
    ( 34,  34,  40),  # 6  b  boots, black deep    (vanilla: jeans, shade)
    (156, 156, 166),  # 7  x  the BOX              (vanilla: light blue)
    (132,  84,  48),  # 8  H  hat band             (vanilla: cap, deep red)
    (240, 230, 204),  # 9  C  coat                 (vanilla: white)
    (202, 190, 160),  # 10 c  coat, shade          (vanilla: white, shade)
    (188, 128,  72),  # 11 T  hat                  (vanilla: cap red)
    (156, 100,  56),  # 12 M  hat, shade           (vanilla: cap, shade)
    (232, 226, 180),  # 13 p  the VS SEEKER's light (vanilla: backpack yellow)
    (100, 100, 112),  # 14 X  the BOX, shade       (vanilla: backpack, shade)
    (  0,   0,   0),  # 15 K  outline
]
INDEX = {" ": 0, "f": 1, "F": 2, "m": 3, "h": 4, "B": 5, "b": 6, "x": 7, "H": 8,
         "C": 9, "c": 10, "T": 11, "M": 12, "p": 13, "X": 14, "K": 15}

BLANK = " " * 16

# ------------------------------------------------------------------ STANDING
# Rows 8..30. The brim at row 14 is the widest line on the figure.
HAT = [
    "                ",
    "     KKKKKK     ",
    "    KTTTTTTK    ",
    "    KTTTTTTK    ",
    "    KHHHHHHK    ",   # the band
    " KKKTTTTTTTTKKK ",
    "KTTTTTTTTTTTTTTK",   # the brim
    " KKKKKKKKKKKKKK ",
]

FRONT = HAT + [
    "  KfmFFFFFFmfK  ",   # ears, and the pale face
    "  KfFKFFFFKFfK  ",   # the eyes
    "   KFFFmmFFFK   ",   # the muzzle
    "    KmFFFFmK    ",
    "   KChKBBKCCK   ",   # the strap starts at the shoulder
    "  KCCChBBKCCCK  ",
    "  KCcCKhBKCcCK  ",
    "  KCcCKBhKxXCK  ",   # and ends at the BOX
    "  KFcCKBBKxXFK  ",   # hands
    "  KKCCKBBKCCKK  ",
    "   KCCKBBKCCK   ",   # the coat stays open to the hem
    "   KcCKBBKCcK   ",
    "   KCCKbbKCCK   ",
    "    KBBKKBBK    ",   # boots
    "   KbbbKKbbbK   ",
]

BACK = HAT + [
    "  KfmmmmmmmmfK  ",
    "  KfmmmmmmmmfK  ",
    "   KmmmmmmmmK   ",
    "    KmmmmmmK    ",
    "   KChCCCCCCK   ",   # the strap, over the back of the coat
    "  KCCChCCCCCCK  ",
    "  KCcCChCCCcCK  ",
    "  KCcCCCChxXCK  ",
    "  KFcCCCCCxXFK  ",
    "  KKCCCCCCCCKK  ",
    "   KCCCCCCCCK   ",
    "   KcCCKKCCcK   ",   # the vent
    "   KCCKbbKCCK   ",
    "    KBBKKBBK    ",
    "   KbbbKKbbbK   ",
]

SIDE = [
    "                ",
    "      KKKKK     ",
    "     KTTTTTK    ",
    "     KTTTTTK    ",
    "     KHHHHHK    ",
    "  KKKTTTTTTTKK  ",
    " KTTTTTTTTTTTTK ",
    "  KKKKKKKKKKKK  ",
    "    KFFmmmfK    ",
    "   KFKFmmmfK    ",   # the eye
    "   KFFFmmmK     ",
    "    KFmmmK      ",
    "     KChCK      ",
    "    KCCChCK     ",
    "    KCCCxXK     ",   # the BOX at the hip
    "    KCFCxXK     ",
    "    KCcCCCK     ",
    "    KCcCCCK     ",
    "    KCCCCcK     ",
    "    KcCCCCK     ",
    "     KCCCK      ",
    "     KBBBK      ",
    "    KbbbbK      ",
]

# ---------------------------------------------------------------------- TAIL
# (top row, left column, rows) -- REASON's, drawn over the STANDING frame.
# INSTINCT's is the same patch mirrored, except from the side, where it curls
# down instead of up.
TAIL_FRONT = (20, 0, [" KK", "Km ", "Km ", "Km ", "Km ", "Km ", " Km", "  m"])
TAIL_BACK = (25, 8, ["   KK", "  KmK", " KmK ", "KmK  "])
TAIL_SIDE_UP = (22, 11, ["  KK", " KmK", "KmK ", "mK  ", "mK  "])
TAIL_SIDE_DOWN = (25, 11, ["m   ", "mK  ", "KmK ", " KmK", "  KK"])


def patch(frame, spec, drop=0, flip=False):
    top, left, rows = spec
    frame = list(frame)
    for i, line in enumerate(rows):
        if flip:
            line = line[::-1]
            col = 16 - left - len(line)
        else:
            col = left
        r = list(frame[top + drop + i])
        for j, ch in enumerate(line):
            if ch != " ":
                r[col + j] = ch
        frame[top + drop + i] = "".join(r)
    return frame


# ----------------------------------------------------------------- MOVEMENT
# Walking drops the figure a row; these rows are written over it, whole.
WALK = {
    "front1": {                   # his right hand forward and up, left tucked
        24: " KFCcCKBhKxXCK  ",
        25: "  KCcCKBBKxXCK  ",
        26: "  KKCCKBBKCCFK  ",
        27: "   KCCKBBKCCKK  ",
        30: "    KBBKKKKKK   ",
        31: "   KbbbK        ",
    },
    "front2": {
        24: "  KCcCKBhKxXCFK ",
        25: "  KCcCKBBKxXCK  ",
        26: "  KFCCKBBKCCKK  ",
        27: "  KKCCKBBKCCK   ",
        30: "   KKKKKKBBK    ",
        31: "        KbbbK   ",
    },
    "back1": {
        24: " KFCcCCCChxXCK  ",
        25: "  KCcCCCCCxXCK  ",
        26: "  KKCCCCCCCCFK  ",
        27: "   KCCCCCCCCKK  ",
        30: "    KBBKKKKKK   ",
        31: "   KbbbK        ",
    },
    "back2": {
        24: "  KCcCCCChxXCFK ",
        25: "  KCcCCCCCxXCK  ",
        26: "  KFCCCCCCCCKK  ",
        27: "  KKCCCCCCCCK   ",
        30: "   KKKKKKBBK    ",
        31: "        KbbbK   ",
    },
    "side1": {                    # the hand swings in front, a long stride
        24: "   KFKCCxXK     ",
        25: "    KCcCCCK     ",
        29: "    KCCKCCK     ",
        30: "   KBBK KBBK    ",
        31: "  KbbbK KbbbK   ",
    },
    "side2": {                    # and behind, feet passing
        24: "    KCCCxXFK    ",
        31: "   KbbbKbbK     ",
    },
}

# Running is walking with the coat flared at the hem.
FLARE_FRONT = {29: "  KCCCKbbKCCCK  "}
FLARE_SIDE = {29: "     KCCCCK     "}

# The head-shake faces you and moves only the eyes.
LOOK_LEFT = {17: "  KfKFFFFKFFfK  "}
LOOK_RIGHT = {17: "  KfFFKFFFFKfK  "}

# Raising an item, and the VS SEEKER, all facing you.
ITEM = {
    1: {22: " KFCcCKhBKCcCK  ", 24: "  KCcCKBBKxXFK  "},
    2: {20: "  KFChKBBKCCK   ", 24: "  KCcCKBBKxXFK  "},   # at the shoulder
    3: {16: " KFfmFFFFFFmfK  ", 17: " KmfFKFFFFKFfK  ",      # beside the head
        18: "  mKFFFmmFFFK   ", 20: "  KmChKBBKCCK   ", 24: "  KCcCKBBKxXFK  "},
    # Up past the brim, the BOX held over the hat. The brim is the widest line
    # on the figure, so an arm that stops under it never reads as raised.
    4: {8:  "KKK             ", 9:  "KxK  KKKKKK     ", 10: "KXK KTTTTTTK    ",
        11: "KFK KTTTTTTK    ", 12: "KmK KHHHHHHK    ", 13: "KmKKTTTTTTTTKKK ",
        15: "KmKKKKKKKKKKKKK ", 16: " KmfmFFFFFFmfK  ", 17: " KmfFKFFFFKFfK  ",
        18: "  mKFFFmmFFFK   ", 20: "  KmChKBBKCCK   ", 24: "  KCcCKBBKxXFK  "},
    5: {22: "  KCcCKFFKCcCK  ", 24: "  KCcCKBBKxXCK  "},
    6: {21: "  KCCCKxXKCCCK  ", 22: "  KCcCKFFKCcCK  ", 24: "  KCcCKBBKxXCK  "},
    7: {20: "   KChKppKCCK   ", 21: "  KCCCKxXKCCCK  ", 22: "  KCcCKFFKCcCK  ",
        24: "  KCcCKBBKxXCK  "},
    8: {21: "  KCCCKpXKCCCK  ", 22: "  KCcCKFFKCcCK  ", 24: "  KCcCKBBKxXCK  "},
}


def standing(rows):
    return [BLANK] * 8 + list(rows) + [BLANK]


def over(frame, replace):
    frame = list(frame)
    for r, line in replace.items():
        frame[r] = line
    return frame


def dropped(rows, replace=None):
    return over([BLANK] * 9 + list(rows), replace or {})


def figure(instinct):
    """Every on-foot frame for one figure, tails included."""
    flip = instinct

    def front(f, drop=0):
        return patch(f, TAIL_FRONT, drop, flip)

    def back(f, drop=0):
        return patch(f, TAIL_BACK, drop, flip)

    def side(f, drop=0):
        return patch(f, TAIL_SIDE_DOWN if instinct else TAIL_SIDE_UP, drop)

    stand_f, stand_b, stand_s = standing(FRONT), standing(BACK), standing(SIDE)
    normal = [
        front(stand_f), back(stand_b), side(stand_s),
        front(dropped(FRONT, WALK["front1"]), 1), front(dropped(FRONT, WALK["front2"]), 1),
        back(dropped(BACK, WALK["back1"]), 1), back(dropped(BACK, WALK["back2"]), 1),
        side(dropped(SIDE, WALK["side1"]), 1), side(dropped(SIDE, WALK["side2"]), 1),
    ]
    run = [
        front(dropped(FRONT), 1),
        front(dropped(FRONT, {**WALK["front1"], **FLARE_FRONT}), 1),
        front(dropped(FRONT, {**WALK["front2"], **FLARE_FRONT}), 1),
        back(dropped(BACK), 1),
        back(dropped(BACK, {**WALK["back1"], **FLARE_FRONT}), 1),
        back(dropped(BACK, {**WALK["back2"], **FLARE_FRONT}), 1),
        side(dropped(SIDE), 1),
        side(dropped(SIDE, {**WALK["side1"], **FLARE_SIDE}), 1),
        side(dropped(SIDE, {**WALK["side2"], **FLARE_SIDE}), 1),
        front(over(stand_f, LOOK_LEFT)),
        front(over(stand_f, LOOK_RIGHT)),
    ]
    item = [front(stand_f)] + [front(over(stand_f, ITEM[n])) for n in range(1, 9)]
    for name, fs in (("normal", normal), ("run", run), ("item", item)):
        for n, f in enumerate(fs):
            assert len(f) == 32, "%s %d is %d rows" % (name, n, len(f))
            for r, line in enumerate(f):
                assert len(line) == 16, "%s %d row %d is %d wide: %r" % (name, n, r, len(line), line)
                bad = set(line) - set(INDEX)
                assert not bad, "%s %d row %d has %r" % (name, n, r, bad)
    return normal, run, item


def sheet(frames, keep=None, keep_count=0):
    img = Image.new("P", (16 * (keep_count + len(frames)), 32))
    flat = [c for rgb in PALETTE for c in rgb]
    img.putpalette(flat + [0] * (768 - len(flat)))
    if keep is not None:
        img.paste(keep.crop((0, 0, 16 * keep_count, 32)), (0, 0))
    px = img.load()
    for n, f in enumerate(frames):
        for y, line in enumerate(f):
            for x, ch in enumerate(line):
                px[(keep_count + n) * 16 + x, y] = INDEX[ch]
    return img


def write_pal(path):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in PALETTE]
    # CRLF, as .gitattributes has it for JASC-PAL (see tools/gbasprite.py)
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


out = {}
for who, instinct in (("red", False), ("green", True)):
    normal, run, item = figure(instinct)
    # The surf frames at 0-2 of the run sheet are not ours yet: keep them.
    surf = Image.open(os.path.join(PEOPLE, "%s_surf_run.png" % who))
    assert surf.mode == "P" and surf.size == (224, 32), (who, surf.mode, surf.size)
    out["%s_normal" % who] = sheet(normal)
    out["%s_surf_run" % who] = sheet(run, keep=surf, keep_count=3)
    out["%s_item" % who] = sheet(item)

rows = [out[k].convert("RGB") for k in ("red_normal", "red_surf_run", "red_item",
                                        "green_normal", "green_surf_run", "green_item")]
prev = Image.new("RGB", (224 * 6, len(rows) * (32 * 6 + 6)), (48, 48, 56))
for i, r in enumerate(rows):
    prev.paste(r.resize((r.width * 6, 32 * 6), Image.NEAREST), (0, i * (32 * 6 + 6)))
prev.save(PREVIEW)
print("  REASON and INSTINCT, walk + run + item -> preview %s" % PREVIEW)

if WRITE:
    for name, img in out.items():
        path = os.path.join(PEOPLE, name + ".png")
        img.save(path, bits=4)
        print("  written %s" % os.path.relpath(path, ROOT))
    write_pal(PAL)
    print("  written %s" % os.path.relpath(PAL, ROOT))

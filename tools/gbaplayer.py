#!/usr/bin/env python3
"""Draw the player's overworld sprites -- REASON and INSTINCT, every sheet.

    python3 tools/gbaplayer.py            # preview to /tmp/player_ow.png
    python3 tools/gbaplayer.py --write    # every player sheet, player.pal, the surf blob

THE GBA PLAYER, not the Game Boy one -- tools/genplayer.py is the 16x16 DMG
figure and stays as it is. This is the grey monkey from the portraits in
gfx/characters/player_*.jpeg: a wide brown hat, a long cream coat open over
black, black boots, the strap across the chest to the BOX at the hip, and the
tail. The side and back were redrawn from the portrait through the n8n
daemon/sprite workflow so they stay one figure (player_ow_ref_*.png).

THE SHEETS, per figure, and what the engine reads out of each:

    red_normal.png          9 x 16x32   0 down  1 up  2 left  3,4 / 5,6 / 7,8 walk
    red_surf_run.png       14 x 16x32   0-2 sitting on the water (down, up, left)
                                        3-5 run down: the pose, then two strides
                                        6-8 run up    9-11 run left
                                        12,13 the head-shake, looking left, right
    red_item.png            9 x 16x32   0-4 raise the arm (sAnim_FieldMove)
                                        0,1,5-8 hold up the VS SEEKER, flashing
    red_bike.png            9 x 32x32   the walk order, seated
    red_vs_seeker_bike.png  6 x 32x32   0-3 raise it, 4,5 the flash
    red_fish.png           12 x 32x32   0-3 left  4-7 up  8-11 down; each is
                                        cock, lift, cast, and the bite

and green_* for INSTINCT. red_surf.png is not drawn: nothing in the engine
reads it (only its INCBIN exists), so it never reaches the screen.

THE PALETTE IS SHARED, SO IT IS REMAPPED BY ROLE. Both figures, all seven
sheets and the SURF BLOB draw from player.pal. Each index keeps the job vanilla
gave it -- the cap's red becomes the hat's brown, skin becomes fur, the white
shirt the cream coat, the backpack the BOX.

WHAT YOU RIDE ON THE WATER. TRAVERSE carries you on a generic mount, and
vanilla drew its body in the jeans' blues -- which are this figure's black
clothes, so it came out a black dome. Its body is moved onto the BOX's two
greys, its shape and its foam kept: you cross the water on something the
colour of the thing you carry daemons in. Provisional, and one table below.

ONE DIFFERENCE BETWEEN THE TWO, AND IT IS THE TAIL. 9.10: "two people, and the
player picks the one they would rather be", deliberately not a matched pair of
opposites. At sixteen pixels a face cannot carry that and a tail can: REASON's
curls up on its right, INSTINCT's hangs and curls down on its left. It reads
from every side, on the bike and on the water too, and costs no colour.

VANILLA'S IDIOM FOR EVERYTHING ELSE. The hat brim is the widest line on the
figure, as the GB player's was. Walk frames drop a row and swing the arms
against the legs; run frames flare the coat. ON THE BIKE THE WHEELS MOVE AND
THE RIDER DOES NOT: vanilla lurches the whole figure sideways, which at this
size reads as the rider falling -- so the spokes flicker instead, which is what
spokes do (the GB build's bike made the same call). The rod passes behind the
body when it is cocked and in front of it when it is cast.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
BLOB = os.path.join(GBA, "graphics/object_events/pics/misc/surf_blob.png")
PAL = os.path.join(GBA, "graphics/object_events/palettes/player.pal")
PREVIEW = "/tmp/player_ow.png"
WRITE = "--write" in sys.argv

# Each entry keeps VANILLA'S ROLE for that index, so vanilla art drawn with it
# still comes out as roughly this figure.
PALETTE = [
    (131, 123, 164),  # 0     transparent (vanilla's key)
    (112, 104, 104),  # 1  f  fur, shade           (vanilla: skin, shade)
    (176, 168, 164),  # 2  F  fur, face and hands  (vanilla: skin)
    (144, 136, 132),  # 3  m  fur                  (vanilla: skin, mid)
    (104,  66,  40),  # 4  h  strap; hat, deep     (vanilla: hair, outline brown)
    ( 52,  52,  60),  # 5  B  black clothes        (vanilla: jeans)
    ( 34,  34,  40),  # 6  b  boots, tyres, rod    (vanilla: jeans, shade)
    (156, 156, 166),  # 7  x  the BOX; metal       (vanilla: light blue)
    (132,  84,  48),  # 8  H  hat band             (vanilla: cap, deep red)
    (240, 230, 204),  # 9  C  coat                 (vanilla: white)
    (202, 190, 160),  # 10 c  coat, shade          (vanilla: white, shade)
    (188, 128,  72),  # 11 T  hat                  (vanilla: cap red)
    (156, 100,  56),  # 12 M  hat, shade           (vanilla: cap, shade)
    (232, 226, 180),  # 13 p  a light: the VS SEEKER, the rod's tip (vanilla: backpack)
    (100, 100, 112),  # 14 X  the BOX, shade; metal, shade (vanilla: backpack, shade)
    (  0,   0,   0),  # 15 K  outline
]
INDEX = {" ": 0, "f": 1, "F": 2, "m": 3, "h": 4, "B": 5, "b": 6, "x": 7, "H": 8,
         "C": 9, "c": 10, "T": 11, "M": 12, "p": 13, "X": 14, "K": 15}

# The surf blob's vanilla indices -> ours. Only the body's blues move.
BLOB_REMAP = {5: 7, 6: 14, 7: 9}

BLANK = " " * 16
W32 = " " * 32

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


def place(frame, rows, x, y):
    """Lay rows over a frame at (x, y), skipping spaces and clipping at the edges."""
    frame = list(frame)
    for i, line in enumerate(rows):
        yy = y + i
        if not 0 <= yy < len(frame):
            continue
        r = list(frame[yy])
        for j, ch in enumerate(line):
            xx = x + j
            if ch != " " and 0 <= xx < len(r):
                r[xx] = ch
        frame[yy] = "".join(r)
    return frame


def patch(frame, spec, drop=0, flip=False):
    top, left, rows = spec
    if flip:
        width = max(len(r) for r in rows)
        rows = [r.ljust(width)[::-1] for r in rows]
        left = 16 - left - width
    return place(frame, rows, left, top + drop)


# ----------------------------------------------------------------- MOVEMENT
# Walking drops the figure a row; these rows are written over it, whole.
WALK = {
    "front1": {                   # the right hand forward and up, left tucked
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

# ---------------------------------------------------------------------- BIKE
# A tyre seen end-on, front or back: two tones that trade places as it turns.
TYRE = {0: ["KXXK", "KbbK", "KbbK", "KbbK", " KK "],
        1: ["KXXK", "KbXK", "KXbK", "KbXK", " KK "],
        2: ["KXXK", "KXbK", "KbXK", "KXbK", " KK "]}
# A wheel seen from the side, with its hub; the spokes are the flicker.
WHEEL = {0: ["  KKKKK  ", " KbbbbbK ", "KbK   KbK", "KbK x KbK", "KbK   KbK", " KbbbbbK ", "  KKKKK  "],
         1: ["  KKKKK  ", " KbXbXbK ", "KXK X KbK", "KbKXxXKXK", "KbK X KbK", " KbXbXbK ", "  KKKKK  "],
         2: ["  KKKKK  ", " KXbXbXK ", "KbKX XKbK", "KXK x KbK", "KbKX XKXK", " KXbXbXK ", "  KKKKK  "]}


def seat(fig, first, last, x, y):
    """The figure from the hat to the hands, set into a blank 32x32 frame."""
    return place([W32] * 32, fig[first:last + 1], x, y)


def bike_front(fig, tone):
    f = seat(fig, 9, 24, 8, 11)                       # hands land on row 26
    f = place(f, ["KxFxxxxxxxxFxK"], 9, 26)           # the handlebar under them
    return place(f, TYRE[tone], 14, 27)


def bike_back(fig, tone):
    f = seat(fig, 9, 24, 8, 11)
    f = place(f, ["Kx", "KK"], 9, 26)                 # the grips, past the coat
    f = place(f, ["xK", "KK"], 21, 26)
    return place(f, TYRE[tone], 14, 27)


def bike_side(fig, tone, stroke):
    f = seat(fig, 9, 23, 9, 11)                       # the hand lands at (15, 25)
    f = place(f, WHEEL[tone], 2, 25)
    f = place(f, WHEEL[(tone + 1) % 3 if tone else 0], 20, 25)
    f = place(f, ["KxxxxxxxxxxxxxxxxK"], 7, 26)       # the frame
    f = place(f, ["KxK", " xK", " xK"], 12, 23)       # the stem and the bar
    leg = ["KBK", "KBK", "KBK", "Kbb"] if stroke == 0 else ["KBBK", "KBK ", "KbK "]
    return place(f, leg, 16 if stroke == 0 else 14, 27)


# ------------------------------------------------------------------- FISHING
def rod(frame, x0, y0, x1, y1):
    """A rod from the hands to its tip: a dark line, its outline, a light tip."""
    pts, dx, dy = [], abs(x1 - x0), -abs(y1 - y0)
    sx, sy, err, x, y = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1), dx + dy, x0, y0
    while True:
        pts.append((x, y))
        if (x, y) == (x1, y1):
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x += sx
        if e2 <= dx:
            err += dx; y += sy
    frame = [list(r) for r in frame]
    for x, y in pts:
        if 0 <= y < 32 and 0 <= x + 1 < 32 and frame[y][x + 1] == " ":
            frame[y][x + 1] = "K"
    for x, y in pts:
        if 0 <= y < 32 and 0 <= x < 32:
            frame[y][x] = "b"
    tx, ty = pts[-1]
    if 0 <= ty < 32 and 0 <= tx < 32:
        frame[ty][tx] = "p"
    return ["".join(r) for r in frame]


def fish(fig, grip, line, behind):
    f = [W32] * 32
    if behind:
        f = rod(f, *line)
    f = place(f, fig, 8, 0)
    if grip:
        f = place(f, [grip[2]], grip[0], grip[1])
    if not behind:
        f = rod(f, *line)
    return f


# Per direction: cock it back, lift it, cast, and the bite dips the tip.
FISH_SIDE = [((14, 22, 29, 6), True), ((14, 22, 13, 3), True),
             ((13, 23, 1, 19), False), ((13, 23, 1, 25), False)]
FISH_BACK = [((16, 23, 19, 31), False), ((16, 22, 22, 10), True),
             ((16, 22, 16, 2), True), ((16, 22, 13, 1), True)]
# Facing you, a cast straight down vanishes into the black trousers and boots,
# so it goes down and OUT, past the body, and the bite pulls it further.
FISH_FRONT = [((16, 23, 10, 1), True), ((16, 23, 22, 6), True),
              ((17, 24, 26, 30), False), ((17, 24, 29, 31), False)]


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
    """Every frame for one figure, tails included."""
    flip = instinct

    def front(f, drop=0):
        return patch(f, TAIL_FRONT, drop, flip)

    def back(f, drop=0):
        return patch(f, TAIL_BACK, drop, flip)

    def side(f, drop=0):
        return patch(f, TAIL_SIDE_DOWN if instinct else TAIL_SIDE_UP, drop)

    stand_f, stand_b, stand_s = standing(FRONT), standing(BACK), standing(SIDE)
    tail_f, tail_b, tail_s = front(stand_f), back(stand_b), side(stand_s)

    normal = [
        tail_f, tail_b, tail_s,
        front(dropped(FRONT, WALK["front1"]), 1), front(dropped(FRONT, WALK["front2"]), 1),
        back(dropped(BACK, WALK["back1"]), 1), back(dropped(BACK, WALK["back2"]), 1),
        side(dropped(SIDE, WALK["side1"]), 1), side(dropped(SIDE, WALK["side2"]), 1),
    ]
    # Sitting on the water: the figure from the hat to the hands, lowered so
    # the blob under it covers the rest; the tail still shows.
    def sit(fig, tailed):
        return tailed(place([BLANK] * 32, fig[9:25], 0, 15), 6)
    surf = [sit(stand_f, front), sit(stand_b, back), sit(stand_s, side)]
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
    item = [tail_f] + [front(over(stand_f, ITEM[n])) for n in range(1, 9)]

    bike = [bike_front(tail_f, 0), bike_back(tail_b, 0), bike_side(tail_s, 0, 0),
            bike_front(tail_f, 1), bike_front(tail_f, 2),
            bike_back(tail_b, 1), bike_back(tail_b, 2),
            bike_side(tail_s, 1, 1), bike_side(tail_s, 2, 0)]
    rest = bike_front(tail_f, 0)
    seeker = [
        rest,
        place(place(rest, ["x"], 20, 26), ["KFK"], 20, 22),                # the hand leaves the bar
        place(place(rest, ["x"], 20, 26), ["KxXK", "KFFK"], 19, 21),       # the SEEKER at the chest
        place(place(rest, ["x"], 20, 26), ["KxXK", "KXxK", " KFK"], 21, 15),  # raised beside the head
        place(place(rest, ["x"], 20, 26), ["p KpXK", "  KXpK", "   KFK"], 18, 15),  # the flash
        place(place(rest, ["x"], 20, 26), ["KxXK", "KXxK", " KFK"], 21, 15),
    ]
    fishing = ([fish(tail_s, None, line, behind) for line, behind in FISH_SIDE]
               + [fish(tail_b, (14, 23, "KFFK"), line, behind) for line, behind in FISH_BACK]
               + [fish(tail_f, (14, 23, "KFFK"), line, behind) for line, behind in FISH_FRONT])

    for name, fs, w in (("normal", normal, 16), ("run", surf + run, 16), ("item", item, 16),
                        ("bike", bike, 32), ("seeker", seeker, 32), ("fish", fishing, 32)):
        for n, f in enumerate(fs):
            assert len(f) == 32, "%s %d is %d rows" % (name, n, len(f))
            for r, line in enumerate(f):
                assert len(line) == w, "%s %d row %d is %d wide: %r" % (name, n, r, len(line), line)
                bad = set(line) - set(INDEX)
                assert not bad, "%s %d row %d has %r" % (name, n, r, bad)
    return normal, surf + run, item, bike, seeker, fishing


def sheet(frames, w):
    img = Image.new("P", (w * len(frames), 32))
    flat = [c for rgb in PALETTE for c in rgb]
    img.putpalette(flat + [0] * (768 - len(flat)))
    px = img.load()
    for n, f in enumerate(frames):
        for y, line in enumerate(f):
            for x, ch in enumerate(line):
                px[n * w + x, y] = INDEX[ch]
    return img


def blob():
    """The surf mount, its body moved off the clothes' blacks. Once only."""
    im = Image.open(BLOB)
    assert im.mode == "P", im.mode
    data = list(im.getdata())
    if 6 not in data:                  # already moved -- 6 was the body's shade
        return im, False
    out = Image.new("P", im.size)
    out.putdata([BLOB_REMAP.get(v, v) for v in data])
    flat = [c for rgb in PALETTE for c in rgb]
    out.putpalette(flat + [0] * (768 - len(flat)))
    return out, True


def write_pal(path):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in PALETTE]
    # CRLF, as .gitattributes has it for JASC-PAL (see tools/gbasprite.py)
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


out = {}
for who, instinct in (("red", False), ("green", True)):
    normal, surf_run, item, bike, seeker, fishing = figure(instinct)
    out["%s_normal" % who] = sheet(normal, 16)
    out["%s_surf_run" % who] = sheet(surf_run, 16)
    out["%s_item" % who] = sheet(item, 16)
    out["%s_bike" % who] = sheet(bike, 32)
    out["%s_vs_seeker_bike" % who] = sheet(seeker, 32)
    out["%s_fish" % who] = sheet(fishing, 32)
blob_img, blob_changed = blob()

order = ["red_normal", "red_surf_run", "red_item", "red_bike", "red_vs_seeker_bike", "red_fish",
         "green_normal", "green_surf_run", "green_item", "green_bike", "green_vs_seeker_bike", "green_fish"]
rows = [out[k].convert("RGB") for k in order]
b = blob_img.copy()
b.putpalette([c for rgb in PALETTE for c in rgb] + [0] * 720)
rows.append(b.convert("RGB"))
S = 3
prev = Image.new("RGB", (max(r.width for r in rows) * S, len(rows) * (32 * S + 4)), (48, 48, 56))
for i, r in enumerate(rows):
    prev.paste(r.resize((r.width * S, 32 * S), Image.NEAREST), (0, i * (32 * S + 4)))
prev.save(PREVIEW)
print("  REASON and INSTINCT, every sheet -> preview %s" % PREVIEW)

if WRITE:
    for name, img in out.items():
        path = os.path.join(PEOPLE, name + ".png")
        img.save(path, bits=4)
        print("  written %s" % os.path.relpath(path, ROOT))
    if blob_changed:
        blob_img.save(BLOB, bits=4)
        print("  written %s" % os.path.relpath(BLOB, ROOT))
    write_pal(PAL)
    print("  written %s" % os.path.relpath(PAL, ROOT))

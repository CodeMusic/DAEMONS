#!/usr/bin/env python3
"""Draw Blanche's people as a fable (T-68, T-69, T-70; vision.md 9.4 "the people are drawn as a fable").

    python3 tools/genfolk.py            # preview to /tmp/folk_ow.png
    python3 tools/genfolk.py --write    # the six sheets

Who they are, and why each is that animal -- the species is a ROLE, not a costume:

    MOM          mom.png        a grey monkey, the player's own kind, with red hair tied back
    VERA CLEAR   daisy.png      a young fox: the Clears are foxes, and she is the one who looks
    the sign woman woman_1.png  a MAGPIE: "Look, look!" -- collects what is written and repeats it
    the pond man fat_man.png    a POND TERRAPIN: carries his house and wonders what it is like
                                inside the PORT. Green-striped and smooth-shelled, so he is not
                                CAIRN's grey-green tortoise
    the aides    scientist.png  MOLES in white coats: the digging nobody sees -- "CRYSTAL signs
                                the work"
    the dry aide worker_f.png   a CROW: "Everyone says so. Very few of them have read her."

These sheets are shared with other maps, and that is accepted: a player reads a
shared sprite as someone else (T-70).

THE THREE CLAUSES (9.4): the animality integrated -- a head proportioned to the
body, paw or feathered hands, a tail -- never an animal head on a person;
drawn plainly, flat colour and no texture; and the head's size carries age, so
VERA's head is the largest here. At sixteen pixels every walking sprite's head
is large; VERA's is larger again.

PALETTES ARE THE SLOTS THEY LIVE IN. Each NPC slot loads one fixed palette on
every map, and dozens of other people draw from it, so no colour is changed:
each figure is drawn from what its slot already has. The white slot (4) has
greys, reds, olives and peach -- MOM, the terrapin, the moles and the crow. The
green slot (3) has black, white and green -- the magpie. VERA draws from the
Clears' own palette in the special slot, beside CRYSTAL and AL.

A WALK IS THE ARMS AND THE TAIL, NOT ONLY THE FEET (genclears.py): each walk
frame drops the figure a row, swings the arms against the legs and sways the
tail a column. Frame 9, where a sheet has it, is ANIM_RAISE_HAND.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
PALS = os.path.join(GBA, "graphics/object_events/palettes")
PREVIEW = "/tmp/folk_ow.png"
WRITE = "--write" in sys.argv


RULES = os.path.join(GBA, "spritesheet_rules.mk")


def ensure_rule(filename, mwidth=2, mheight=4):
    """a NEW sheet needs its own conversion rule, and nothing warns you when it has none.

    `spritesheet_rules.mk` names every object-event sheet explicitly and converts it with
    -mwidth/-mheight, which is what packs each frame's tiles together for overworld_frame(). A sheet
    wider than one frame WITHOUT a rule is converted in raster order across the whole strip: every
    frame comes out scrambled -- the head sheared off, and on the side frame the head down at the
    feet. Overwriting a vanilla sheet inherits vanilla's rule, which is why this only ever bites the
    sheets we ADD. Byte-checking the .4bpp against the ROM cannot catch it: a scrambled sheet
    verifies perfectly against its own scrambled self. Compare a decoded frame instead.
    """
    name = filename[:-4] if filename.endswith(".png") else filename
    target = "$(OBJEVENTGFXDIR)/people/%s.4bpp" % name
    s = open(RULES).read()
    if target + ":" in s:
        return False
    open(RULES, "w").write(s.rstrip("\n") + "\n\n%s: %%.4bpp: %%.png\n\t$(GFX) $< $@ -mwidth %d -mheight %d\n"
                          % (target, mwidth, mheight))
    return True


def read_pal(name):
    return [tuple(map(int, l.split())) for l in open(os.path.join(PALS, name)).read().replace("\r", "").split("\n")[3:19]]


# letter -> index, per palette
WHITE = {" ": 0, "a": 1, "s": 2, "S": 3, "e": 4, "T": 5, "t": 6, "u": 7, "R": 8, "r": 9, "E": 10,
         "w": 11, "g": 12, "G": 13, "W": 14, "K": 15}          # npc_white
GREEN = {" ": 0, "a": 1, "s": 2, "S": 3, "e": 4, "y": 5, "o": 6, "Y": 7, "l": 8, "J": 9, "N": 10,
         "p": 11, "q": 12, "b": 13, "W": 14, "K": 15}          # npc_green
CLEARS = {" ": 0, "Y": 1, "G": 2, "B": 3, "C": 4, "L": 5, "P": 6, "D": 7, "R": 8, "w": 9, "l": 10,
          "g": 11, "n": 12, "r": 13, "W": 14, "K": 15}         # npc_clears


def mirror(halves):
    return [h + h[::-1] for h in halves]


def overlay(rows, top, patch, left):
    rows = list(rows)
    for i, line in enumerate(patch):
        r = list(rows[top + i])
        for j, ch in enumerate(line):
            if ch != " " and 0 <= left + j < 16:
                r[left + j] = ch
        rows[top + i] = "".join(r)
    return rows


# ------------------------------------------------------------------ MOM (npc_white)
MOM_FRONT = mirror([
    "     KKK",
    "   KKRRR",
    "  KRRRRR",
    " KRRrRRR",
    " KRRgggg",    # the hair parts over grey fur
    " KgRwwwg",    # grey ears, the pale grey face the player has
    " KgwKwww",    # the eyes
    " Kgwwwwg",
    "  Kgwwgg",    # the muzzle
    "   KKwww",
    "   KttWW",    # an olive cardigan open over a white blouse
    "  KtttWW",
    " KtTttWW",
    " KtTttWW",
    " KwtttWW",    # grey hands
    " KKttttW",
    "  KeeeEe",    # a long brown skirt
    "  KeeeEe",
    "  KeeeEe",
    "  KeeeEe",
    "   KeeeE",
    "   KGGKK",
    "   KKKK ",
])
MOM_FRONT = overlay(MOM_FRONT, 9, ["KRK", "KrK", "KRK", " KK"], 12)       # the red hair, over one shoulder
MOM_FRONT = overlay(MOM_FRONT, 15, [" KK", "KgK", "KgK", "KgK", " KgK", "  KK"], 0)   # the tail, curling down

MOM_BACK = mirror([
    "     KKK",
    "   KKRRR",
    "  KRRRRR",
    " KRRrRRR",
    " KRRRRRR",
    " KgRRRRR",
    " KgRRrRR",
    " KgRRRRR",
    "  KgRRrR",
    "   KKRRR",
    "   KttKR",    # the hair tied back, down the cardigan
    "  KttttK",
    " KtTtttt",
    " KtTtttt",
    " Kwttttt",
    " KKttttt",
    "  Keeeee",
    "  Keeeee",
    "  Keeeee",
    "  KeeeEe",
    "   KeeeE",
    "   KGGKK",
    "   KKKK ",
])
MOM_BACK = overlay(MOM_BACK, 14, ["  KK", " KgK", "KgK ", "KgK ", " KgK", "  KK"], 10)

MOM_SIDE = [
    "      KKKK      ",
    "     KRRRRK     ",
    "    KRRRRRRK    ",
    "   KRRrRRRRRK   ",
    "   KwggRRRRRK   ",
    "  KwwKgRRRRRK   ",   # the eye
    "  KwwwggRRRK    ",
    "  KKwwwgRRRRK   ",
    "   KKwwgRrRRK   ",   # the hair falls down her back
    "     KKttKRrK   ",
    "     KttWtKRK   ",
    "    KtttWtK     ",
    "    KtTttttK    ",
    "    KtwtttK     ",   # the hand
    "    KttttttK    ",
    "    KeeeeeK     ",
    "    KeeeeeKK    ",
    "    KeeeeEKgK   ",   # the tail, behind her
    "    KeeeeEKgK   ",
    "    KeeeEEKKgK  ",
    "     KGGGK  KK  ",
    "     KGGGK      ",
    "     KKKKK      ",
]

# ------------------------------------------------------------------ VERA (npc_clears)
VERA_EARS = ["        ", "  KK    ", "  KnRK  ", "  KnRRKK"]
VERA_FRONT = mirror(VERA_EARS + [
    "  KRRRRR",
    " KrRRRRR",
    " KRRRKRR",    # the eyes, level
    " KRCRKRR",
    " KrCCCCK",
    "  KrCCCC",
    "   KKKKK",
    "    KCCC",    # her collar
    "   KLCCC",    # a lavender pinafore over a cream shirt
    "  KCLLLL",
    "  KCLLLL",
    "  KBLLLL",    # paws
    "  KKLLLL",
    "   KLLlL",
    "   KLLlL",
    "  KLLLlL",    # the hem flares
    "  KKKKKK",
    "    KBBK",
    "   KBBBK",
])
VERA_FRONT = overlay(VERA_FRONT, 16, ["KK  ", "KrRK", "KRRK", "KCRK", " KK "], 0)
VERA_BACK = mirror([h.replace("n", "R") for h in VERA_EARS] + [
    "  KRRRRR",
    " KrRRRRR",
    " KrRRRRR",
    " KrRRRRR",
    " KrrRRRR",
    "  KrrRRR",
    "   KKrrr",
    "    KCCC",
    "   KLLLL",
    "  KCLLLL",
    "  KCLLLL",
    "  KBLLLL",
    "  KKLLLL",
    "   KLLlL",
    "   KLLlL",
    "  KLLLlL",
    "  KKKKKK",
    "    KBBK",
    "   KBBBK",
])
VERA_BACK = overlay(VERA_BACK, 15, [" KK ", "KRRK", "KrRK", "KRRK", "KCCK", " KK "], 6)
VERA_SIDE = [
    "                ",
    "       K  K     ",
    "      KRKKRK    ",
    "      KnRKRRK   ",
    "     KRRRRRRK   ",
    "    KRRRRRRRrK  ",
    "  KKRKRRRRRRrK  ",
    " KCCRKRRRRRRrK  ",
    "KKCCCRRRRRRrK   ",
    " KCCCCCRRRrK    ",
    "  KKCCCCrrK     ",
    "    KKCCKK      ",
    "     KCCCK      ",
    "    KLLCCLK     ",
    "    KLLLLLK     ",
    "    KCLLLLK     ",
    "    KBLLLLK     ",
    "    KLLLLlKK    ",
    "    KLLLLlKRK   ",
    "   KLLLLLlKrRK  ",
    "   KKKKKKKKRCRK ",
    "     KBBK  KKK  ",
    "     KBBBK      ",
]

# ------------------------------------------------------------------ MAGPIE (npc_green)
MAGPIE_FRONT = mirror([
    "        ",
    "        ",
    "     KKK",
    "   KKbbb",
    "  KbbbbN",    # a green sheen on the black
    " KbWKbbb",    # a bright eye
    " KbbbbbY",    # the beak
    "  KbbbYY",
    "   KbWWW",    # the white breast
    "   KJJWW",    # a green jacket
    "  KJJJWW",
    " KWlJJWW",    # a white wing patch at the sleeve
    " KWlJJJW",
    " KblJJJJ",    # feathered hands
    " KKJJJJJ",
    "  KNNNNN",    # a dark green skirt
    "  KNNNNN",
    "  KNNNNN",
    "   KNNNN",
    "    KYYK",    # thin dark legs
    "    KYYK",
    "   KYYYK",
    "        ",
])
MAGPIE_FRONT = overlay(MAGPIE_FRONT, 17, ["KK ", "KbK", "KNbK", " KbK", "  K"], 12)
MAGPIE_BACK = mirror([
    "        ",
    "        ",
    "     KKK",
    "   KKbbb",
    "  KbbbbN",
    " KbbbbbN",
    " KbbbbNb",
    "  KbbbbN",
    "   KKbbb",
    "   KJJJJ",
    "  KJJJJJ",
    " KWlJJJJ",
    " KWlJJJJ",
    " KblJJJJ",
    " KKJJJKK",
    "  KNNKbb",    # the long tail, down the middle
    "  KNNKbN",
    "  KNNKbb",
    "   KNKbN",
    "    KKbb",
    "    KYKK",
    "   KYYK ",
    "        ",
])
MAGPIE_SIDE = [
    "                ",
    "                ",
    "      KKKK      ",
    "     KbbbbK     ",
    "    KbbbbNbK    ",
    "   KbWKbbbbK    ",   # the eye
    " KKYbbbbbbNK    ",   # the beak points the way she faces
    "KYYYKbbbbbK     ",
    " KKKbWWbbK      ",
    "    KWWJJK      ",
    "    KWJJJJK     ",
    "    KJWlJJK     ",
    "    KJWlJJK     ",
    "    KJblJJKK    ",
    "    KJJJJJKbK   ",
    "    KNNNNNKbbK  ",   # the long tail behind her
    "    KNNNNNKbNbK ",
    "    KNNNNNK KbbK",
    "     KNNNK   KK ",
    "      KYK       ",
    "      KYK       ",
    "     KYYK       ",
    "                ",
]

# ------------------------------------------------------------------ TERRAPIN (npc_white)
TERRAPIN_FRONT = mirror([
    "        ",
    "        ",
    "        ",
    "     KKK",
    "    KtTT",
    "   KttTT",
    "   KtKTT",    # a heavy-lidded eye
    "   KtttT",
    "   KTtTT",    # the yellow stripes down the neck
    "    KtTt",
    "  KKuRRR",    # the shell's rim behind the shoulders; a brown shirt
    " KuRRRRR",
    " KuRrRRR",
    "KtuRrRRR",    # green arms
    "KtuRRRRR",
    "KKuRRRRR",
    " KuRRRRR",
    "  KGGGGG",    # rolled grey trousers
    "  KGGGGG",
    "  KGGKGG",
    "  KttKtt",    # bare webbed feet
    "  KKKKKK",
    "        ",
])
TERRAPIN_BACK = mirror([
    "        ",
    "        ",
    "        ",
    "     KKK",
    "    KttT",
    "   KtttT",
    "   KtttT",
    "   KtttT",
    "    KttT",
    "  KKKKKK",
    " KTTTTTT",    # the smooth shell, worn like a pack
    " KTtttut",
    "KtTtuttu",
    "KtTtttut",
    "KtTtuttu",
    "KKTtttut",
    " KTTTTTT",
    "  KGGGGG",
    "  KGGGGG",
    "  KGGKGG",
    "  KttKtt",
    "  KKKKKK",
    "        ",
])
TERRAPIN_SIDE = [
    "                ",
    "                ",
    "                ",
    "     KKKK       ",
    "    KtTTtK      ",
    "  KKtKTTtK      ",   # the eye
    " KttttTTtK      ",   # a blunt snout
    " KKtttTTK       ",
    "   KKTtTK       ",
    "     KRRKKKK    ",
    "    KRRRKTTuK   ",   # the shell's hump behind him
    "    KRrRKTtuuK  ",
    "    KRrRKTttuK  ",
    "    KtRRKTtutK  ",   # the arm
    "    KtRRKTttuK  ",
    "    KRRRKTtuK   ",
    "    KRRRKKKK    ",
    "    KGGGGK      ",
    "    KGGGGK      ",
    "    KGGKGGK     ",
    "   KttK KttK    ",
    "   KKKK KKKK    ",
    "                ",
]

# ------------------------------------------------------------------ MOLE (npc_white)
MOLE_FRONT = mirror([
    "        ",
    "        ",
    "    KKKK",
    "   KGGGG",
    "  KGGGGG",
    " KsGwwGG",    # small pink ears; round spectacles
    " KGwKwGG",    # the eyes behind them
    "  KGwwGG",
    "  KGGGss",    # the pink nose
    "   KKGsS",
    "   KWWGG",    # the white coat's collar
    "  KWWWKw",    # open over a pale shirt
    " KWWWWKw",
    " KWwWWKw",
    " KssWWKw",    # broad pink digging hands
    " KKWWWKw",
    "  KWWWKw",
    "  KWwWKG",
    "   KGGGG",
    "   KGGKG",
    "   KssKs",
    "   KKKKK",
    "        ",
])
MOLE_BACK = mirror([
    "        ",
    "        ",
    "    KKKK",
    "   KGGGG",
    "  KGGGGG",
    " KsGGGGG",
    " KGGGGGG",
    "  KGGGGG",
    "  KGGGGG",
    "   KKGGG",
    "   KWWWW",
    "  KWWWWW",
    " KWWWWWW",
    " KWwWWWW",
    " KssWWWW",
    " KKWWWWW",
    "  KWWWWW",
    "  KWwWKK",
    "   KGGKs",    # a short pink tail
    "   KGGKs",
    "   KssKK",
    "   KKKK ",
    "        ",
])
MOLE_SIDE = [
    "                ",
    "                ",
    "      KKKK      ",
    "     KGGGGK     ",
    "    KGGGGGsK    ",
    "   KwwGGGGGK    ",   # the spectacles
    "  KwKwGGGGGK    ",
    " KsKwwGGGGK     ",
    "KssGGGGGGK      ",   # the long pink nose
    " KKKKGGGK       ",
    "     KWWK       ",
    "    KWwWWK      ",
    "    KWWWWK      ",
    "    KWsWWK      ",   # the hand
    "    KWssWK      ",
    "    KWWWWK      ",
    "    KWWWWKK     ",
    "    KWwWWKsK    ",   # the tail
    "     KGGGK K    ",
    "     KGGGK      ",
    "    KssKssK     ",
    "    KKK KKK     ",
    "                ",
]

# ------------------------------------------------------------------ CROW (npc_white)
CROW_FRONT = mirror([
    "        ",
    "        ",
    "     KKK",
    "   KKGGG",
    "  KGGGGG",
    " KGGGGGG",
    " KGWKGGG",    # a level, unimpressed eye
    " KGGGGgg",    # the grey beak
    "  KGGGgw",
    "   KKGgg",
    "   KWWWW",    # a white shirt
    "  KWWKgg",    # under a grey apron, its strap
    " KWWKggg",
    " KGWKggg",    # black feathered hands
    " KGWKggg",
    " KKWKggg",
    "  KWKggg",
    "  KGKggg",
    "   KGGGG",
    "   KGGKG",
    "   KggKg",
    "   KKKKK",
    "        ",
])
CROW_BACK = mirror([
    "        ",
    "        ",
    "     KKK",
    "   KKGGG",
    "  KGGGGG",
    " KGGGGGG",
    " KGGGGgG",
    " KGGGGGG",
    "  KGGGGG",
    "   KKGGG",
    "   KWWWW",
    "  KWWKWW",    # the apron's straps cross
    " KWWWKWW",
    " KGWWWKW",
    " KGWWWKW",
    " KKWWWWW",
    "  KWWWWK",
    "  KGKKGG",    # tail feathers below the shirt
    "   KGKGG",
    "   KGGKG",
    "   KggKg",
    "   KKKKK",
    "        ",
])
CROW_SIDE = [
    "                ",
    "                ",
    "      KKKK      ",
    "     KGGGGK     ",
    "    KGGGGGGK    ",
    "   KGWKGGGGK    ",
    " KKgGGGGGGGK    ",
    "KgwgKGGGGGK     ",   # the beak, sharp
    " KKKKGGGGK      ",
    "     KGGK       ",
    "    KWWWWK      ",
    "    KWggWK      ",
    "    KWgggK      ",
    "    KGgggK      ",   # the hand at the apron
    "    KGgggK      ",
    "    KWgggKK     ",
    "    KWgggKGK    ",   # tail feathers
    "    KGggKGGK    ",
    "     KGGGKK     ",
    "     KGKGK      ",
    "    KggKggK     ",
    "    KKK KKK     ",
    "                ",
]


# ------------------------------------------------------------------ frames
def standing(rows):
    return [" " * 16] * 8 + list(rows) + [" " * 16]


def shift_block(frame, cols, dy):
    """move the pixels in these columns (rows 16..27) up or down a row: an arm swinging."""
    f = [list(r) for r in frame]
    src = [r[:] for r in f]
    for y in range(16, 28):
        for x in cols:
            f[y][x] = src[y - dy][x] if 0 <= y - dy < 32 else " "
    return ["".join(r) for r in f]


def shift_cols(frame, rows, dx):
    """move the pixels in these rows sideways: a tail swaying, a stride opening."""
    f = [list(r) for r in frame]
    for y in rows:
        line = f[y]
        f[y] = ([" "] * dx + line[:16 - dx]) if dx > 0 else (line[-dx:] + [" "] * (-dx))
    return ["".join(r) for r in f]


def walk(frame, step, view):
    f = [" " * 16] + list(frame[:-1])              # the figure drops a row
    if view in ("front", "back"):
        left, right = range(0, 5), range(11, 16)
        f = shift_block(f, left, -1 if step == 1 else 1)    # one arm forward and up, the other back
        f = shift_block(f, right, 1 if step == 1 else -1)
        legs = [list(r) for r in f]
        lift = range(0, 8) if step == 1 else range(8, 16)   # one foot lifts
        for x in lift:
            legs[31][x] = " "
            if legs[30][x] == " " and f[31][x] != " ":
                legs[30][x] = f[31][x]
        f = ["".join(r) for r in legs]
    else:
        if step == 1:                                        # the stride opens
            f = shift_cols(f, [29, 30, 31], 0)
            lower = [list(r) for r in f]
            for y in (30, 31):
                row = lower[y]
                front = row[:8]; back = row[8:]
                lower[y] = front[1:] + [" "] + [" "] + back[:-1]
            f = ["".join(r) for r in lower]
        f = shift_block(f, range(3, 7), -1 if step == 1 else 1)
    return f


def raise_hand(frame, colour):
    f = [list(r) for r in frame]
    for y in range(10, 18):
        f[y][13] = "K"; f[y][14] = colour; f[y][15] = "K"
    f[9][14] = "K"
    return ["".join(r) for r in f]


def figure(front, back, side, extra_hand=None, still=False):
    fs, bs, ss = standing(front), standing(back), standing(side)
    if still:
        return [fs, bs, ss]
    out = [fs, bs, ss, walk(fs, 1, "front"), walk(fs, 2, "front"), walk(bs, 1, "back"), walk(bs, 2, "back"),
           walk(ss, 1, "side"), walk(ss, 2, "side")]
    if extra_hand:
        out.append(raise_hand(fs, extra_hand))
    return out


FIGURES = [
    ("mom", "mom.png", figure(MOM_FRONT, MOM_BACK, MOM_SIDE, still=True), WHITE, "npc_white.pal"),
    ("vera", "daisy.png", figure(VERA_FRONT, VERA_BACK, VERA_SIDE), CLEARS, "npc_clears.pal"),
    ("magpie", "woman_1.png", figure(MAGPIE_FRONT, MAGPIE_BACK, MAGPIE_SIDE, extra_hand="b"), GREEN, "npc_green.pal"),
    ("terrapin", "fat_man.png", figure(TERRAPIN_FRONT, TERRAPIN_BACK, TERRAPIN_SIDE), WHITE, "npc_white.pal"),
    ("mole", "scientist.png", figure(MOLE_FRONT, MOLE_BACK, MOLE_SIDE, extra_hand="s"), WHITE, "npc_white.pal"),
    ("crow", "worker_f.png", figure(CROW_FRONT, CROW_BACK, CROW_SIDE), WHITE, "npc_white.pal"),
]


def check(name, frames, index):
    for n, f in enumerate(frames):
        assert len(f) == 32, "%s frame %d is %d rows" % (name, n, len(f))
        for r, line in enumerate(f):
            assert len(line) == 16, "%s frame %d row %d is %d wide: %r" % (name, n, r, len(line), line)
            bad = set(line) - set(index)
            assert not bad, "%s frame %d row %d has %r" % (name, n, r, bad)


def sheet(frames, index, pal):
    img = Image.new("P", (16 * len(frames), 32))
    flat = [c for rgb in pal for c in rgb]
    img.putpalette(flat + [0] * (768 - len(flat)))
    px = img.load()
    for n, f in enumerate(frames):
        for y, line in enumerate(f):
            for x, ch in enumerate(line):
                px[n * 16 + x, y] = index[ch]
    return img


def main():
    rows = []
    built = []
    for name, filename, frames, index, palname in FIGURES:
        check(name, frames, index)
        pal = read_pal(palname)
        img = sheet(frames, index, pal)
        built.append((name, filename, img))
        rgb = img.convert("RGB")
        bg = Image.new("RGB", rgb.size, (150, 150, 150))
        mask = Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata()))
        bg.paste(rgb, (0, 0), mask)
        rows.append(bg)
        old = os.path.join(PEOPLE, filename)
        if os.path.exists(old):
            rows.append(Image.open(old).convert("RGB"))
    w = max(r.width for r in rows) * 6
    out = Image.new("RGB", (w, 32 * 6 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 6, 192), Image.NEAREST), (0, 192 * i))
    out.save(PREVIEW)
    print("  %d figures -> preview %s (each: ours on grey, then what is on disk)" % (len(built), PREVIEW))
    if WRITE:
        for name, filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
            print("  written people/%s" % filename)


if __name__ == "__main__":
    main()

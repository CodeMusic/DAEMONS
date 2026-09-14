#!/usr/bin/env python3
"""Draw the Clears' overworld sprites -- CRYSTAL and AL, one palette between them.

    python3 tools/genclears.py            # preview to /tmp/clears_ow.png
    python3 tools/genclears.py --write    # both sheets and npc_clears.pal

Each sheet is nine 16x32 frames, in the order the pic tables load them:

    0 down   1 up   2 left   3,4 down walk   5,6 up walk   7,8 left walk

Facing right is frame 2 with OAM's x-flip. Index 0 is transparent.

    CRYSTAL  -> graphics/object_events/pics/people/prof_oak.png
    AL       -> graphics/object_events/pics/people/blue.png

DRAWN FROM REFERENCE, NOT RESAMPLED. Crystal's drafts came through the n8n
daemon/sprite workflow and are kept in gfx/characters/crystal_ow_ref_*.png;
Al's reference is his three battle pieces, gfx/characters/al_*.jpeg. A straight
downsample to 16x32 loses the face, the outline and the clothes in the same
pass, exactly as tools/genplayer.py says it will -- so the references decide
the colours and the silhouette, and the pixels are written here.

WHAT HAS TO READ AT SIXTEEN PIXELS, in order of what the eye finds first:

    the ears      tall, above where every human head in the game stops --
                  the one shape nobody else on the map has
    the clothes   Crystal: a white coat open over purple, a scientist first.
                  Al: a cream collared shirt, belted, short-sleeved, so his
                  russet forearms and dark paws show
    the tail      out from under the hem, on the side the references put it

VANILLA'S IDIOM FOR EVERYTHING ELSE. Same outline weight, walk frames drop the
whole figure one row, and the head is large, because every
walking sprite in this game is -- 9.4's head-to-body rule is for the portraits,
and a sixteen-pixel adult drawn at adult proportions is a stick with a dot on
it. Crystal's ears start a row higher than Al's; that is the age, here.

A WALK IS THE ARMS, NOT THE FEET. The first cut moved only the feet and read as
someone sliding. Vanilla's rival swings both arms against the legs: the hand on
the side of the long stride pushes a column out and a row up, the other tucks
in and hangs a row lower, and the next step trades them. From the side the hand
passes in front of the body, then behind it. So each walk frame below is
written out from the shoulders down -- arms, legs, and the tail, which sways
one column each way from behind and hangs, then flicks out, from the front.

ONE PALETTE FOR THE FAMILY. 9.4's line is "three foxes, a palette apart --
Crystal golden-amber, Ty darker, Al somewhere between", and at overworld size
that is literal: both are drawn from npc_clears.pal, Crystal's fur from 1-2,
Al's from 8 and 13, and the dark browns at 3 and 12 are where Ty's goes.

It is also the only arrangement that works. No NPC palette has gold, russet,
purple and a grey to shade a coat, so the Clears are OBJ_EVENT_PAL_TAG_NPC_CLEARS
in PALSLOT_NPC_SPECIAL -- the one slot patched per object from its own tag.
Crystal and Al share three maps; two different tags in that slot would recolour
whichever spawned first. One tag cannot.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_clears.pal")
PREVIEW = "/tmp/clears_ow.png"
WRITE = "--write" in sys.argv

PALETTE = [
    (115, 197, 164),  # 0  transparent -- the key every object palette uses
    (255, 214,  66),  # 1  Y  Crystal's fur, gold
    (230, 150,  32),  # 2  G  Crystal's fur, shade
    (104,  60,  36),  # 3  B  Al's paws, belt and boots
    (255, 246, 214),  # 4  C  muzzles, throats, tail tips; Al's shirt
    (156, 136, 170),  # 5  L  Al's trousers
    (112,  72, 184),  # 6  P  Crystal's top
    ( 66,  62,  92),  # 7  D  Crystal's trousers
    (226, 108,  52),  # 8  R  Al's fur, russet
    (198, 200, 216),  # 9  w  Crystal's coat, shade; Al's shirt, shade
    (110,  94, 128),  # 10 l  Al's trousers, shade
    ( 84,  84, 100),  # 11 g  Crystal's hands
    (120,  72,  40),  # 12 n  inside the ear
    (164,  64,  32),  # 13 r  Al's fur, shade
    (255, 255, 255),  # 14 W  Crystal's coat
    (  0,   0,   0),  # 15 K  outline
]
INDEX = {" ": 0, "Y": 1, "G": 2, "B": 3, "C": 4, "L": 5, "P": 6, "D": 7,
         "R": 8, "w": 9, "l": 10, "g": 11, "n": 12, "r": 13, "W": 14, "K": 15}


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


# ---------------------------------------------------------------- CRYSTAL
# Rows 8..30 of each standing frame; 0..7 and 31 are empty.
EARS = ["   K    ", "  KGK   ", "  KnGK  ", "  KnYGKK"]

CRYSTAL_FRONT = mirror(EARS + [
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
CRYSTAL_FRONT = overlay(CRYSTAL_FRONT, 17, [" KK ", "KGYK", "KYYK", "KYCK", " KK "], 0)

CRYSTAL_BACK = mirror([h.replace("n", "G") for h in EARS] + [
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
# From behind, the tail hangs down the coat, off the centre seam.
CRYSTAL_BACK = overlay(CRYSTAL_BACK, 14, [" KK ", "KYGK", "KYYK", "KYGK", "KYCK", " KK "], 7)

CRYSTAL_SIDE = [
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

# Walking: the figure drops a row; everything below the shoulders is written out
# per step, because a walk is the arms and the tail as much as the feet.
CRYSTAL_WALKS = {
    "front1": {                   # her right hand forward and up, left tucked
        21: "   KWWKPPKWWK   ",
        22: "  KWWWKPPKWWWK  ",
        23: " KWwWWKPPKWwWK  ",
        24: " KgwWWKPPKWwWK  ",
        25: " KgKWWKPPKWwWK  ",
        26: " KKKWWKDDKWwgK  ",
        27: "KGYKWWKDDKWKgK  ",
        28: "KYYKwWKDDKWwK   ",
        29: "KYCKKDDKKDDK    ",   # the tail hangs to the ground
        30: " KK KDDKKKKKK   ",
        31: "   KKKK         ",
    },
    "front2": {                   # left hand forward, right tucked
        21: "   KWWKPPKWWK   ",
        22: "  KWWWKPPKWWWK  ",
        23: "  KWwWKPPKWWwWK ",
        24: "  KWwWKPPKWWwgK ",
        25: "  KWwWKPPKWWKgK ",
        26: "  KgwWKDDKWWKK  ",
        27: " KKgKWKDDKWWK   ",
        28: "KGYKwWKDDKWwK   ",   # and flicks up, out from behind the tucked hand
        29: "KYCKKDDKKDDK    ",
        30: " KKKKKKKKDDK    ",
        31: "         KKKK   ",
    },
    "back1": {
        21: "   KWWWWWWWWK   ",
        22: "  KWWWWWWWWWWK  ",
        23: " KWwWWWWKKWwWK  ",
        24: " KgwWWWKYGKwWK  ",
        25: " KgKWWWKYYKwWK  ",
        26: "  KKWWKYGKWwgK  ",   # the tail's lower half sways left
        27: "   KWWKYCKWKgK  ",
        28: "   KwWWKKWWwK   ",
        29: "    KDDKKDDK    ",
        30: "    KDDKKKKKK   ",
        31: "   KKKK         ",
    },
    "back2": {
        21: "   KWWWWWWWWK   ",
        22: "  KWWWWWWWWWWK  ",
        23: "  KWwWWWKKWWwWK ",
        24: "  KWwWWKYGKWwgK ",
        25: "  KWwWWKYYKWKgK ",
        26: "  KgwWWWKYGKKK  ",   # and right
        27: "  KgKWWWKYCKK   ",
        28: "   KwWWWWKKwK   ",
        29: "    KDDKKDDK    ",
        30: "   KKKKKKDDK    ",
        31: "         KKKK   ",
    },
    "side1": {                    # the near hand swings in front of her
        23: "    KWwWWWK     ",
        24: "   KWWwWWWK     ",
        25: "   KgKWwWWK     ",
        26: "   KgKWKWWKK    ",
        27: "    KWWWWwKYK   ",
        28: "    KwWWWwKGYK  ",
        29: "    KDDKDDK YCYK",
        30: "   KDDK KDDKKK  ",
        31: "   KKK   KKK    ",
    },
    "side2": {                    # and behind
        23: "    KWwWWWK     ",
        24: "    KWWwWWK     ",
        25: "    KWWwWgK     ",
        26: "    KWWKWgKK    ",
        27: "    KWWWWwKYK   ",
        28: "    KwWWWwKGYK  ",
        29: "     KDDDKKYCYK ",
        30: "     KDKDK KKK  ",
        31: "    KKK KKK     ",
    },
}

# --------------------------------------------------------------------- AL
# Younger, so his ears start a row lower and stand less tall.
AL_EARS = ["        ", "  KK    ", "  KnRK  ", "  KnRRKK"]

AL_FRONT = mirror(AL_EARS + [
    "  KRRRRR",
    " KrRRRRR",
    " KRRRKRR",   # the eyes
    " KRCRKRR",
    " KrCCCCK",   # the nose
    "  KrCCCC",
    "   KKKKK",   # the chin closes: his muzzle and his shirt are one cream
    "    KwCw",   # the collar, points out
    "  KwCCCw",   # a short sleeve, and the placket down the middle
    "  KRwCCC",
    "  KRKCCC",   # the russet forearm, outside the shirt
    "  KBKCCC",   # the dark paw
    "  KBKBBB",   # the belt
    "   KKLLL",
    "    KLLL",
    "    KLLK",
    "    KLLK",
    "    KBBK",   # boots
    "   KBBBK",
])
# His tail is on the viewer's left in all three battle pieces.
AL_FRONT = overlay(AL_FRONT, 17, ["KK  ", "KrRK", "KRRK", "KCRK", " KK "], 1)

AL_BACK = mirror([h.replace("n", "R") for h in AL_EARS] + [
    "  KRRRRR",
    " KrRRRRR",
    " KrRRRRR",
    " KrRRRRR",
    " KrrRRRR",
    "  KrrRRR",
    "   KKrrr",
    "    KCCC",
    "  KwCCCC",
    "  KRwCCC",
    "  KRKCCC",
    "  KBKwCC",
    "  KBKBBB",
    "   KKLLL",
    "    KLLL",
    "    KLLK",
    "    KLLK",
    "    KBBK",
    "   KBBBK",
])
AL_BACK = overlay(AL_BACK, 16, [" KK ", "KRRK", "KrRK", "KRRK", "KCCK", " KK "], 6)

AL_SIDE = [
    "                ",
    "       K  K     ",
    "      KRKKRK    ",
    "      KnRKRRK   ",
    "     KRRRRRRK   ",
    "    KRRRRRRRrK  ",
    "  KKRKRRRRRRrK  ",   # the eye
    " KCCRKRRRRRRrK  ",
    "KKCCCRRRRRRrK   ",   # the snout
    " KCCCCCRRRrK    ",
    "  KKCCCCrrK     ",
    "    KKCCKK      ",
    "     KCwCK      ",
    "    KCCCCCK     ",
    "    KCwCCCK     ",   # the sleeve
    "    KRKCCCK     ",   # the forearm
    "    KBKCCCK     ",   # the paw
    "    KBBBBBK     ",   # the belt
    "     KLLLLKK    ",
    "     KLLLlKRK   ",   # the tail, behind him
    "     KLlLKKrRK  ",
    "     KLLLKKRCRK ",
    "     KBBBK KKK  ",
]

AL_WALKS = {
    "front1": {                   # his right paw forward and out, left tucked lower
        23: " KRKCCCCCCCKRK  ",
        24: " KBKCCCCCCCKRK  ",
        25: "  KKBBBBBBBKBK  ",
        26: " KKKKLLLLLLKBK  ",
        27: " KrRKLLLLLLKK   ",
        28: " KRRKLLKKLLK    ",
        29: " KCRKLLKKLLK    ",   # the tail hangs to its tip
        30: "  KKKBBKKBBBK   ",
        31: "   KBBBK        ",
    },
    "front2": {
        23: "  KRKCCCCCCCKRK ",
        24: "  KRKCCCCCCCKBK ",
        25: "  KBKBBBBBBBKK  ",
        26: " KKBKLLLLLLKK   ",
        27: "KrRKKLLLLLLK    ",   # and swings out
        28: "KRRKKLLKKLLK    ",
        29: "KCK KLLKKLLK    ",
        30: "   KBBBKKBBK    ",
        31: "        KBBBK   ",
    },
    "back1": {
        23: " KRKCCCCCCCKRK  ",
        24: " KBKCwCCCCwKRK  ",
        25: "  KKBBBKKBBKBK  ",
        26: "   KKLKRRKLKBK  ",
        27: "    KLKrRKLKK   ",
        28: "    KKRRKLLK    ",   # the tail sways left
        29: "    KKCCKLLK    ",
        30: "    KBBKKBBBK   ",
        31: "   KBBBK        ",
    },
    "back2": {
        23: "  KRKCCCCCCCKRK ",
        24: "  KRKwCCCCwCKBK ",
        25: "  KBKBBKKBBBKK  ",
        26: "  KBKLKRRKLKK   ",
        27: "  KKKLKrRKLK    ",
        28: "    KLLKRRKK    ",   # and right
        29: "    KLLKCCKK    ",
        30: "   KBBBKKBBK    ",
        31: "        KBBBK   ",
    },
    "side1": {                    # the near paw in front
        24: "   KRKCCCCK     ",
        25: "   KBKCCCCK     ",
        26: "   KBKBBBBK     ",
        27: "     KLLLLKK    ",
        28: "     KLLLlKRK   ",
        29: "    KLLKLLKKRCRK",
        30: "   KLLK KBBKKK  ",
        31: "   KBBK  KBBK   ",
    },
    "side2": {                    # and behind
        24: "    KCCCRKK     ",
        25: "    KCCCKBK     ",
        26: "    KBBBKBK     ",
        27: "     KLLLLKK    ",
        28: "     KLLLlKRK   ",
        29: "     KLLLKKRCRK ",
        30: "     KBLBK KKK  ",
        31: "    KBBKBBK     ",
    },
}


def standing(rows):
    return [" " * 16] * 8 + rows + [" " * 16]


def walking(rows, replace):
    """Drop the standing figure a row, then write the step over it, whole rows."""
    f = [" " * 16] * 9 + list(rows)
    for r, line in replace.items():
        f[r] = line
    return f


def frames(front, back, side, walks, who):
    out = [standing(front), standing(back), standing(side)]
    out += [walking(front, walks["front1"]), walking(front, walks["front2"])]
    out += [walking(back, walks["back1"]), walking(back, walks["back2"])]
    out += [walking(side, walks["side1"]), walking(side, walks["side2"])]
    for n, f in enumerate(out):
        assert len(f) == 32, "%s frame %d is %d rows" % (who, n, len(f))
        for r, line in enumerate(f):
            assert len(line) == 16, "%s frame %d row %d is %d wide: %r" % (who, n, r, len(line), line)
            bad = set(line) - set(INDEX)
            assert not bad, "%s frame %d row %d has %r" % (who, n, r, bad)
    return out


FIGURES = [
    ("crystal", os.path.join(PEOPLE, "prof_oak.png"),
     frames(CRYSTAL_FRONT, CRYSTAL_BACK, CRYSTAL_SIDE, CRYSTAL_WALKS, "crystal")),
    ("al", os.path.join(PEOPLE, "blue.png"),
     frames(AL_FRONT, AL_BACK, AL_SIDE, AL_WALKS, "al")),
]


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


def preview(sheets):
    """Each figure at x8 on the transparent key, then on grey, then what is on disk now."""
    w = 144 * 8
    rows = []
    for name, path, img in sheets:
        rgb = img.convert("RGB")
        rows.append(rgb)
        grey = Image.new("RGB", rgb.size, (150, 150, 150))
        mask = Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata()))
        grey.paste(rgb, (0, 0), mask)
        rows.append(grey)
    for name, path, img in sheets:
        if os.path.exists(path):
            rows.append(Image.open(path).convert("RGB"))
    out = Image.new("RGB", (w, 256 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 8, 256), Image.NEAREST), (0, 256 * i))
    out.save(PREVIEW)


def write_pal(path):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in PALETTE]
    # CRLF, as .gitattributes has it for JASC-PAL (see tools/gbasprite.py)
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


sheets = [(name, path, sheet(fs)) for name, path, fs in FIGURES]
preview(sheets)
print("  %d figures, 144x32 each -> preview %s" % (len(sheets), PREVIEW))
if WRITE:
    for name, path, img in sheets:
        img.save(path, bits=4)
        print("  written %s" % os.path.relpath(path, ROOT))
    write_pal(PAL)
    print("  written %s" % os.path.relpath(PAL, ROOT))

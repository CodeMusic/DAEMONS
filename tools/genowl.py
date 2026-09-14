#!/usr/bin/env python3
"""Draw the Owl's overworld sprite -- MR. CONSTRUE, who is an owl (4.23, 4.24).

    python3 tools/genowl.py            # preview to /tmp/owl_ow.png
    python3 tools/genowl.py --write    # owl.png and npc_owl.pal

Nine 16x32 frames, in the order sPicTable_Owl loads them:

    0 down   1 up   2 left   3,4 down walk   5,6 up walk   7,8 left walk

Facing right is frame 2 with OAM's x-flip. Index 0 is transparent.

HIS OWN SLOT, NOT THE ONE HE WAS STANDING IN. Mr. Psychic's house used
OBJ_EVENT_GFX_BALDING_MAN, and that sheet is on twenty-nine maps: redrawing it
would put an owl behind every counter in the game. So he is OBJ_EVENT_GFX_OWL,
and the house is the only map that places him.

DRAWN FROM REFERENCE, NOT RESAMPLED. The draft came through the n8n
daemon/sprite workflow (gfx/characters/owl_ow_ref_front.png) -- an elderly
great horned owl in a tweed waistcoat. The fable rule holds at sixteen pixels:
the tufts and the face disc are what read, the waistcoat says scholar, and
nothing is textured. He is stouter and shorter-necked than the Clears, which is
the age.

WHAT HAS TO READ, in order:

    the tufts      two points above the head, where the Clears have ears --
                   so at a glance he is not a fox, and not a person
    the face disc  pale, round, two eyes and a beak in the middle of it
    the waistcoat  brown, buttoned, between folded wings

A WALK IS A WADDLE. The figure drops a row like every walker in the game; the
wing on the stride side hangs a row lower while the other folds in, and the
feet trade. From behind the tail feathers sway; from the side they flick.

HIS OWN PALETTE, in PALSLOT_NPC_SPECIAL: nothing else stands in that house.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PIC = os.path.join(GBA, "graphics/object_events/pics/people/owl.png")
PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_owl.pal")
PREVIEW = "/tmp/owl_ow.png"
WRITE = "--write" in sys.argv

PALETTE = [
    (115, 197, 164),  # 0  transparent
    (190, 168, 130),  # 1  F  feathers, light
    (140, 114,  82),  # 2  f  feathers
    ( 92,  70,  50),  # 3  d  feathers, dark
    (240, 228, 200),  # 4  C  face disc, breast
    (120,  72,  44),  # 5  V  waistcoat
    ( 84,  48,  30),  # 6  v  waistcoat, buttons
    (230, 190,  70),  # 7  Y  beak, talons
    (170, 130,  40),  # 8  y  beak, shade
    (150, 150, 160),  # 9  s  (spare grey)
    (250, 170,  40),  # 10 E  eyes
    (220, 216, 200),  # 11 w  (spare)
    (  0,   0,   0),  # 12
    (  0,   0,   0),  # 13
    (255, 255, 255),  # 14 W
    (  0,   0,   0),  # 15 K  outline
]
INDEX = {" ": 0, "F": 1, "f": 2, "d": 3, "C": 4, "V": 5, "v": 6, "Y": 7,
         "y": 8, "s": 9, "E": 10, "w": 11, "W": 14, "K": 15}


def mirror(halves):
    """A symmetric row from its left eight columns."""
    return [h + h[::-1] for h in halves]


# Rows 8..30 of each standing frame; 0..7 and 31 are empty.
TUFTS = ["        ", "        ", "   K    ", "  KdK   ", "  KfdKKK"]

FRONT = mirror(TUFTS + [
    " KfFFFFF",
    " KfCCCCC",   # the face disc
    " KfCEKCC",   # the eyes, amber, and their pupils
    " KfCCCCY",   # the beak meets its mirror
    "  KfCCCy",
    "   KffCC",
    "  KfFCVV",   # the breast shows above the waistcoat
    " KdfFVVV",
    " KdfFVvV",   # buttons
    " KdfFVVV",
    " KdfFVvV",
    " KdffVVV",
    "  KdfKVV",   # the wing tips end
    "   KKCCC",
    "    KCCC",
    "    KfCC",
    "    KYYK",   # talons
    "   KYKYK",
])

BACK = mirror(TUFTS + [
    " KfFFFFF",
    " KfFFFFF",
    " KfFFdFF",
    " KfFFFFF",
    "  KfFdFF",
    "   KffFF",
    "  KfFVVV",
    " KdfFVVV",
    " KdfFVVV",
    " KdfFVVV",
    " KdfFVVV",
    " KdffVVV",
    "  KdfKVV",
    "   KKdfF",   # tail feathers
    "    KdfF",
    "    KKdf",
    "    KYYK",
    "   KYKYK",
])

SIDE = [
    "                ",
    "                ",
    "       K        ",
    "      KdK  K    ",
    "     KfdKKKdK   ",
    "    KfFFFFFFfK  ",
    "   KCCCFFFFFFfK ",
    "   KEKCFFFFFFfK ",   # the eye
    "  YKCCCFFFFFfK  ",   # the beak, hooked at the very edge
    "  KyCCCFFFFfK   ",
    "   KKCCffffK    ",
    "    KCVVFffK    ",
    "    KVVVFFfdK   ",   # the near wing, folded over the waistcoat
    "    KVvVFFfdK   ",
    "    KVVVFFfdK   ",
    "    KVvVfFfdK   ",
    "    KVVVdffdK   ",
    "    KCCCKddK    ",
    "    KCCCCKdfK   ",   # tail feathers, behind
    "     KCCCKKdfK  ",
    "     KfCCK KKK  ",
    "     KYYK       ",
    "    KYKYK       ",
]

WALKS = {
    "front1": {                   # his right wing hangs, left folds in
        26: "  KdfKVVVVKKK   ",
        27: "  KdKCCCCCCKK   ",
        28: "  KKKCCCCCCK    ",
        29: "    KfCCCCfK    ",
        30: "    KYYKKKKK    ",
        31: "   KYKYK        ",
    },
    "front2": {
        26: "   KKKVVVVKfdK  ",
        27: "   KKCCCCCCKdK  ",
        28: "    KCCCCCCKKK  ",
        29: "    KfCCCCfK    ",
        30: "    KKKKKYYK    ",
        31: "        KYKYK   ",
    },
    "back1": {
        26: "  KdfKVVVVKKK   ",
        27: "  KdKdfFFfdKK   ",
        28: "  KKKdfFFfdK    ",
        29: "     KKdffdKK   ",   # the tail sways right
        30: "    KYYKKKKK    ",
        31: "   KYKYK        ",
    },
    "back2": {
        26: "   KKKVVVVKfdK  ",
        27: "   KKdfFFfdKdK  ",
        28: "    KdfFFfdKKK  ",
        29: "   KKdffdKK     ",   # and left
        30: "    KKKKKYYK    ",
        31: "        KYKYK   ",
    },
    "side1": {
        26: "    KCCCKdK     ",
        27: "    KCCCCKKdfK  ",   # the tail flicks up
        30: "    KYYK KYK    ",   # a stride
        31: "   KYKYK KK     ",
    },
    "side2": {
        28: "     KCCCKKdfKK ",   # and down
        30: "      KYYK      ",   # feet together
        31: "     KYKYK      ",
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


def frames():
    out = [standing(FRONT), standing(BACK), standing(SIDE)]
    out += [walking(FRONT, WALKS["front1"]), walking(FRONT, WALKS["front2"])]
    out += [walking(BACK, WALKS["back1"]), walking(BACK, WALKS["back2"])]
    out += [walking(SIDE, WALKS["side1"]), walking(SIDE, WALKS["side2"])]
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
    """The frames at x8 on the transparent key, then on grey."""
    rgb = img.convert("RGB")
    w = img.width * 8
    out = Image.new("RGB", (w, 512), (60, 60, 60))
    out.paste(rgb.resize((w, 256), Image.NEAREST), (0, 0))
    grey = Image.new("RGB", rgb.size, (150, 150, 150))
    mask = Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata()))
    grey.paste(rgb, (0, 0), mask)
    out.paste(grey.resize((w, 256), Image.NEAREST), (0, 256))
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

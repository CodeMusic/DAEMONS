#!/usr/bin/env python3
"""The battle BACK pics -- the player seen from behind, throwing (T-123; vision.md 9.4, 9.10).

    python3 tools/genbacks.py            # preview to /tmp/backs.png (vanilla above, ours below)
    python3 tools/genbacks.py --write    # the two strips, and their palettes

WHY THE FIRST DRAFT FAILED, AND WHAT REPLACED IT. It hand-wrote 64x64 ASCII and came out with no
head, no arms, a tail in the middle of the coat and an invisible throw. Hand-drawing works at 16x32
and does not at this size. So nothing here is drawn from nothing: VANILLA'S OWN FRAMES ARE THE
SKELETON, and they are repainted. Measured, its body, hat and coat hold still across the throw and
only the near arm, shoulder and head tilt move -- 1461, 1610, 1810 and 1530 pixels change between
consecutive frames, with boxes spanning most of the canvas -- so tracing keeps an animation that
would take many drafts to invent, and keeps it exactly.

THE PALETTE DOES MOST OF THE WORK, BECAUSE VANILLA'S INDICES ALREADY CARRY ROLES: 2/3/4 skin, 8 hair,
9/10 the white shirt, 5/6 the jeans, 11/12 the cap, 13/14 the backpack, 15 the outline, and 1 and 7
spare. Swapping the sixteen colours role for role changes the character without touching a single
index, so the silhouette and the throw survive intact.

BUT A ROLE-FOR-ROLE SWAP GETS THE PROPORTIONS WRONG, which is the finding. Vanilla is mostly BACKPACK
(830px) over a small white shirt (302px); ours is a long cream coat seen from behind with a dark
satchel on it. Mapping the pack to the satchel made a grey blob that swallowed the figure. So the
PACK'S AREA BECOMES THE COAT -- it is the big surface on a back -- and the satchel is drawn on top of
it out of the two spare indices.

THREE SHAPE EDITS, EACH DERIVED RATHER THAN PLACED BY HAND:

  * THE BRIM. Vanilla wears a cap; this figure wears a wide brown hat, and 9.4 says the brim is the
    widest line on it. The hat's own pixels are found per frame (indices 11/12), its lowest row taken,
    and the brim grown outward from there -- so it follows the head tilt for free.
  * THE SATCHEL. The dark disc in the middle of vanilla's pack is its ball emblem; left alone it reads
    as a hole punched in the coat. It becomes the satchel's body and clasp.
  * THE TAIL. 9.10 gives the two figures one difference and it is the tail: REASON's curls up on its
    right, INSTINCT's hangs and curls down on its left. It is drawn from the coat's own bottom edge,
    found per frame, so it emerges from behind the coat instead of sitting on it.

INDEX 0 IS THE TRANSPARENT SLOT AND ITS COLOUR DIFFERS PER FILE -- red and leaf carry a lavender
(131,123,164) -- so each file keeps the one it has.

FRAME COUNTS ARE HARD-CODED IN C. gTrainerBackPicTable[] gives 0x2800 = FIVE frames for red and leaf,
so a strip of the wrong height is a size mismatch rather than a cosmetic bug, and the size is asserted
against the file on disk before anything is written.

SCOPE IS TWO, NOT FOUR. The old man and the pokedude are not the player and have no species yet; that
wants a decision before drawing, so they keep vanilla's. RS_BRENDAN and RS_MAY are reachable only
through the Ruby/Sapphire link-partner path and stay vanilla under T-120's cut-off.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import GBA
from driftguard import refuse_over_later_work

PREVIEW = "/tmp/backs.png"
WRITE = "--write" in sys.argv
BACKS = os.path.join(GBA, "graphics/trainers/back_pics")
PALS = os.path.join(GBA, "graphics/trainers/palettes")

HAT, HATD = 11, 12                     # vanilla's cap
COAT, COATD = 13, 14                   # vanilla's backpack -- the big surface on a back
SATCHEL, SATCHELL = 1, 7               # vanilla leaves these two unused
FURL, FUR, FURD, FURK = 2, 3, 4, 8     # vanilla's skin ramp, and its hair
INK = 15

# role for role, and index 0 keeps whatever that file already had
OURS = {
    HAT:      (180, 131, 65),          # the wide brown hat
    HATD:     (139, 98, 41),
    COAT:     (226, 210, 178),         # the long cream coat, seen from behind
    COATD:    (198, 182, 150),
    9:        (255, 246, 222),          # its lit folds
    10:       (238, 228, 200),
    5:        (104, 86, 66),            # the satchel: vanilla's ball emblem is a disc on the back,
    6:        (68, 56, 42),             # and a dark disc on a cream coat is a bag without editing it
    FURL:     (214, 210, 202),          # grey fur
    FUR:      (176, 172, 164),
    FURD:     (120, 116, 110),
    FURK:     (88, 84, 80),
    SATCHEL:  (72, 62, 52),             # the satchel, and its lit edge
    SATCHELL: (104, 90, 74),
    INK:      (0, 0, 0),
}


def frames_of(img):
    px = img.load()
    return [[[px[x, k * 64 + y] for x in range(64)] for y in range(64)]
            for k in range(img.size[1] // 64)]


def brim(f):
    """The hat is vanilla's cap until its brim is grown. Found from the hat's own pixels, so it
    follows the head tilt without being placed by hand."""
    hat = [(x, y) for y in range(64) for x in range(64) if f[y][x] in (HAT, HATD)]
    if not hat:
        return
    low = max(y for _, y in hat)
    wide = [x for x, yy in hat if yy >= low - 2]
    cx = (min(wide) + max(wide)) // 2
    half = (max(wide) - min(wide)) // 2
    # 9.4: THE BRIM IS THE WIDEST LINE ON THE FIGURE. A few pixels either side only made a wider cap,
    # so it is grown half as far again as the crown and given a curve, which is what says "hat".
    for k, y in enumerate((low - 1, low, low + 1)):
        w = half + 4 - k * 2
        for x in range(cx - w, cx + w + 1):
            if 0 <= x < 64 and 0 <= y < 64 and f[y][x] not in (HAT, HATD, INK):
                f[y][x] = HATD if k else HAT
    for x in range(64):                                   # one black line under it, as vanilla edges its cap
        for y in range(low, min(64, low + 3)):
            if f[y][x] in (HAT, HATD) and (y + 1 >= 64 or f[y + 1][x] not in (HAT, HATD)):
                f[y][x] = INK
                break


def tail(f, right):
    """9.10's one difference between the two -- REASON's curls up on its right, INSTINCT's hangs and
    curls down on its left. Grown from the coat's own bottom edge, so it comes out from BEHIND the
    coat rather than sitting on top of it, which is how the first draft's read as a squiggle."""
    coat = [(x, y) for y in range(64) for x in range(64) if f[y][x] in (COAT, COATD, 9, 10)]
    if not coat:
        return
    low = max(y for _, y in coat)
    side = max(x for x, y in coat if y > low - 10) if right else min(x for x, y in coat if y > low - 10)
    step = 1 if right else -1
    x, y = side, low - 8
    # A thin line reads as a wire, so it thickens at the root and tapers, as a tail does.
    for k in range(11):
        x += step
        y += (1 if k < 3 else (0 if k < 6 else -1)) if right else (1 if k < 5 else 0)
        t = 4 if k < 4 else (3 if k < 8 else 2)
        for d in range(-t, t + 1):
            if 0 <= x < 64 and 0 <= y + d < 64 and f[y + d][x] == 0:
                f[y + d][x] = FURD if abs(d) == t else (FUR if abs(d) > 1 else FURL)
        for d in (-t - 1, t + 1):
            if 0 <= x < 64 and 0 <= y + d < 64 and f[y + d][x] == 0:
                f[y + d][x] = INK


# ONE SKELETON, TWO TAILS. Both files carry the SAME sixteen colours but use them for different
# things -- in red 11/12 are the cap (1425px), in leaf they are only the sunhat's band (210px) while
# 9/10 are the white hat and 4/8 are long hair (1978px) -- so one index map cannot serve both, and
# recolouring leaf by red's roles put a white hat on it. The deeper reason not to try is 9.10: these
# are ONE figure, "two people, and the player picks the one they would rather be", whose only
# difference is the tail. So both strips are traced from red's frames, and leaf's long hair -- which
# this character does not have -- never arises.
SHEETS = [("LOGIC", "red_back_pic.png", True), ("INTUITION", "leaf_back_pic.png", False)]
SKELETON = "red_back_pic.png"


def main():
    refuse_over_later_work("genbacks")          # T-293: its files carry later work; generator_drift.json says what
    built, rows = [], []
    for name, filename, right in SHEETS:
        src = Image.open(os.path.join(BACKS, filename))
        skel = Image.open(os.path.join(BACKS, SKELETON))
        assert src.mode == "P", "%s is %s, not paletted" % (filename, src.mode)
        assert src.size == skel.size, "%s is %s and the skeleton is %s" % (filename, src.size, skel.size)
        fs = frames_of(skel)
        assert len(fs) == 5, "%s holds %d frames, the C table wants 5" % (filename, len(fs))
        for f in fs:
            brim(f); tail(f, right)
        out = Image.new("P", src.size)
        pal = list(skel.getpalette()[:48])
        for i, c in OURS.items():
            pal[i * 3:i * 3 + 3] = list(c)
        out.putpalette(pal + [0] * (768 - 48))
        op = out.load()
        for k, f in enumerate(fs):
            for y in range(64):
                for x in range(64):
                    op[x, k * 64 + y] = f[y][x]
        assert out.size == src.size, "%s would change size" % filename
        built.append((filename, out, [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]))
        rows.append((src, out, len(fs)))
    w = max(n for _, _, n in rows) * 64 * 3
    sheet = Image.new("RGB", (w, len(rows) * (64 * 3 * 2 + 12)), (40, 40, 46))
    y = 0
    for src, out, n in rows:
        for k in range(n):
            sheet.paste(src.crop((0, k * 64, 64, (k + 1) * 64)).convert("RGB").resize((192, 192), Image.NEAREST), (k * 192, y))
            sheet.paste(out.crop((0, k * 64, 64, (k + 1) * 64)).convert("RGB").resize((192, 192), Image.NEAREST), (k * 192, y + 192))
        y += 64 * 3 * 2 + 12
    sheet.save(PREVIEW)
    print("  %d strips -> preview %s (vanilla above, ours below)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img, pal in built:
            img.save(os.path.join(BACKS, filename), bits=4)
            with open(os.path.join(PALS, filename.replace(".png", ".pal")), "w") as fh:
                fh.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal))
        #  T-177's outline, which every picture of ours carries: drawn by the same pass, so this write lands where the
        #  tree is and does not take it off again (T-293).
        import gbaoutline
        gbaoutline.main(only=[os.path.splitext(f)[0] for f, _, _ in built], write=True)
        print("  written %d strips and their palettes" % len(built))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The two teachers' BACK pics: the old man and CRYSTAL CLEAR (T-123; vision.md 9.4).

    python3 tools/genmentors.py            # preview to /tmp/mentors.png (vanilla above, ours below)
    python3 tools/genmentors.py --write    # both strips, and their palettes

TWO BACK PICS ARE NOT THE PLAYER, and genbacks.py left them for a species decision. There turned out
to be nothing left to decide -- the game had already said who both of them are:

  THE OLD MAN   is an OLD IGUANA. You walk up to him in VIRIDIAN on OBJ_EVENT_GFX_TOWN_CALLOW_ELDER,
                CALLOW's elder, and 9.4 makes the sprite you meet and the picture one species.
  THE POKEDUDE  is CRYSTAL CLEAR, a fox. Nobody is called that on screen any more: STREAM's host line
                is "This is a recording. CRYSTAL CLEAR, for the lecture series", and every battle demo
                is narrated "CRYSTAL: ...". The back the player watches during those demos is hers.

THE METHOD IS genbacks.py's: VANILLA'S OWN FRAMES ARE THE SKELETON AND THEY ARE REPAINTED. Both strips
are four frames of a three-quarter back view with the head turned, so each figure keeps vanilla's
throw exactly and only its colours and a few derived shapes change.

A PALETTE SWAP ALONE PUTS A PERSON'S FACE ON AN ANIMAL, which is the failure genbacks.py's first draft
named. A turned head shows a human PROFILE -- a nose, a chin -- and recolouring it green only makes a
green person. So each figure also gets the edits that carry its species, every one DERIVED from the
frame's own pixels so it follows the head through the throw:

  the iguana   a DEWLAP hung under the jaw, and a CREST of spikes along the crown
  the fox      two EARS standing off the top of the head, and a MUZZLE drawn out past the nose

INDEX ROLES DIFFER PER FILE, and the file on disk is read rather than assumed. Where one colour index
serves two things that must now differ -- CRYSTAL's skin index is her face AND her arms, which become
cream fur and white coat sleeves -- the split is made by CONNECTED COMPONENT rather than by row, because
a raised hand sits beside the head in half the frames and a row cut would paint it fur.
"""
import io, os, subprocess, sys
from collections import deque
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import GBA

PREVIEW = "/tmp/mentors.png"
WRITE = "--write" in sys.argv
BACKS = os.path.join(GBA, "graphics/trainers/back_pics")
PALS = os.path.join(GBA, "graphics/trainers/palettes")
INK = 15


def frames_of(img):
    px = img.load()
    return [[[px[x, k * 64 + y] for x in range(64)] for y in range(64)] for k in range(img.size[1] // 64)]


def components(f, members):
    """8-connected components of the pixels whose index is in MEMBERS"""
    seen, out = set(), []
    for y in range(64):
        for x in range(64):
            if f[y][x] in members and (x, y) not in seen:
                q, comp = deque([(x, y)]), []
                seen.add((x, y))
                while q:
                    cx, cy = q.popleft()
                    comp.append((cx, cy))
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < 64 and 0 <= ny < 64 and (nx, ny) not in seen and f[ny][nx] in members:
                                seen.add((nx, ny))
                                q.append((nx, ny))
                out.append(comp)
    return out


def touches(comp, f, members):
    for x, y in comp:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < 64 and 0 <= ny < 64 and f[ny][nx] in members:
                    return True
    return False


def put(f, x, y, v, only_empty=True):
    if 0 <= x < 64 and 0 <= y < 64 and (not only_empty or f[y][x] == 0):
        f[y][x] = v


# ====================================================================== the OLD IGUANA
# old_man.pal, by role:  1..4 skin  5..7 and 14 the white hair  9,10 the vest  11..13 the shirt  8 unused
OM_SKIN, OM_HAIR, OM_DEWLAP = (1, 2, 3, 4), (5, 6, 7, 14), 8
IGUANA = {
    1: (200, 214, 170), 2: (170, 186, 140), 3: (140, 156, 120), 4: (76, 88, 64),   # CALLOW's grey-green, faded
    5: (122, 142, 104), 6: (98, 116, 84), 7: (70, 84, 58), 14: (176, 192, 150),     # the crest and the back of the head
    8: (216, 160, 48),                                                                # the gold dewlap, as his sheet has
}


def iguana(f):
    # the head is the skin component that touches the hair; arms and a raised hand do not
    head = max((c for c in components(f, OM_SKIN) if touches(c, f, OM_HAIR)), key=len, default=None)
    if not head:
        return
    hs = set(head)
    edge = {(x, y) for x, y in head if any((x + dx, y + dy) not in hs and 0 <= x + dx < 64 and 0 <= y + dy < 64
                                          and f[y + dy][x + dx] not in OM_SKIN
                                          for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    # A GREEN PERSON IS NOT AN IGUANA. The profile's brow, closed eye, nose and lips are the dark skin
    # indices INSIDE the head, so they are smoothed into the face and the silhouette alone is kept.
    for x, y in head:
        if (x, y) not in edge and f[y][x] in (3, 4):
            f[y][x] = 2
    # A RAISED HAND THAT TOUCHES THE FACE JOINS THE HEAD'S COMPONENT, and in the fourth frame the
    # "frontmost" pixel was a fingertip -- the dewlap hung off the hand. The face cannot reach more than
    # a face's width past the back of the head, so the front is looked for only that far in front of the
    # hair, and everything past it is arm.
    hair_right = max(x for y in range(64) for x in range(64) if f[y][x] in OM_HAIR)
    face = [(x, y) for x, y in head if x <= hair_right + 11]
    xs, ys = [x for x, _ in face], [y for _, y in face]
    front, top, low = max(xs), min(ys), max(y for x, y in face if x >= max(xs) - 10)
    h = low - top
    # a round eye with a gold ring, set well forward on the head as a lizard's is
    ex, ey = front - 7, top + h * 2 // 5
    for dx, dy, v in ((0, 0, INK), (1, 0, INK), (0, 1, INK), (1, 1, INK), (-1, 0, OM_DEWLAP), (2, 1, OM_DEWLAP),
                      (0, -1, 4), (1, -1, 4)):
        if (ex + dx, ey + dy) in hs:
            f[ey + dy][ex + dx] = v
    # THE DEWLAP hangs from the CHIN, and over the collar. The first try hung it from the head
    # component's lowest row -- which is the bottom of the NECK -- and it landed on the shoulder. The
    # chin is the lowest pixel among the FRONTMOST columns, and the flap drapes back and down from it.
    chin_y = max(y for x, y in face if x >= front - 6)
    chin = [x for x, y in face if y == chin_y and x >= front - 6]
    chin_x = sum(chin) // len(chin)
    for k, (dx0, dx1) in enumerate(((-3, 0), (-4, 0), (-4, -1), (-4, -1), (-3, -2))):
        y = chin_y + 1 + k
        for x in range(chin_x + dx0, chin_x + dx1 + 1):
            if 0 <= x < 64 and 0 <= y < 64 and f[y][x] not in OM_SKIN:
                f[y][x] = OM_DEWLAP
        for x in (chin_x + dx0 - 1, chin_x + dx1 + 1):
            if 0 <= x < 64 and 0 <= y < 64 and f[y][x] not in OM_SKIN and f[y][x] != OM_DEWLAP:
                f[y][x] = INK
    for x in range(chin_x - 3, chin_x - 1):
        if 0 <= chin_y + 6 < 64 and f[chin_y + 6][x] not in OM_SKIN:
            f[chin_y + 6][x] = INK


# ====================================================================== CRYSTAL CLEAR, a fox
# pokedude.pal, by role:  1..4 skin  12, 7 the dark bob  5, 6, 8, 14 the vest  13 the lips  9..11 unused
#
# RECOLOURING THIS FIGURE DID NOT WORK AND THE REASON IS WORTH KEEPING. The PokeDude is a muscular man in
# a tank top with a bob: a gold bob is still a haircut, and his skin runs unbroken from face to neck to
# shoulder, so one component held the face AND an arm and the first draft painted one arm fur and the
# other a sleeve. So the HEAD IS REPLACED, the way genrhino.py replaced the cue ball's rider: vanilla's
# throw and body stay, one fox head is drawn, and it is placed per frame.
#
# ONE DRAWING SERVES ALL FOUR FRAMES BECAUSE THE HEAD IS THE SAME DRAWING IN ALL FOUR -- measured, not
# assumed: every one of the bob's 283 pixels in frame 0 lands on the same index in each other frame at a
# single offset, found by search. HEAD_AT is computed, never typed.
PD_SKIN, PD_HAIR, PD_LIPS, PD_VEST = (1, 2, 3, 4), (12, 7), 13, (5, 6, 8, 14)
BLOCK = (23, 4)                        # frame 0's head block, top-left: the bob starts at column 23, the ears need row 4
CRYSTAL = {
    7: (255, 214, 66), 12: (236, 176, 40), 11: (196, 120, 28),    # her gold, its shade, a rust edge
    9: (255, 246, 214),                                            # cream: the muzzle and the throat
    5: (240, 240, 244), 8: (212, 214, 226), 6: (170, 172, 190),   # the white coat where the vest was
    10: (84, 84, 100),                                              # grey paws
    13: (255, 246, 214),                                            # the lips go; their index is cream now
}
FOXL = {".": None, "K": 15, "Y": 7, "G": 12, "R": 11, "C": 9}
# Turned to the right, three-quarters from behind: the back of the head, both ears -- the near one taller --
# the eye as a slit, and the muzzle long and cream to a black nose. Twenty-eight columns, the bob's own width.
FOX_HEAD = [
    ".....K..........K...........",
    "....KK.........KKK..........",
    "....KGK.......KGGK..........",
    "...KGGK.......KGGGK.........",
    "...KGYGK.....KGYYGK.........",
    "..KGYYGK.....KGYYYGK........",
    "..KGYYYGKKKKKGYYYYGK........",
    ".KGYYYYYYYYYYYYYYYGGK.......",
    ".KGYYYYYYYYYYYYYYYYYGK......",
    "KGYYYYYYYYYYYYYYYYYYYGK.....",
    "KGYYYYYYYYYYYYYYYYYYYYGK....",
    "KGYYYYYYYYYYYYYYYYYYYYYGK...",
    "KGGYYYYYYYYYYYYYYYYKKYYYK...",
    "KGGYYYYYYYYYYYYYYYYYYYYYYK..",
    "KGGGYYYYYYYYYYYYYYYYYYYCCCKK",
    "KRGGGYYYYYYYYYYYYYYYYCCCCCCK",
    "KRGGGYYYYYYYYYYYYYYYCCCCCCKK",
    "KRRGGGYYYYYYYYYYYYYCCCCCKK..",
    "KRRGGGYYYYYYYYYYYYCCCCKK....",
    ".KRRGGGGYYYYYYYYYCCCCK......",
    ".KRRGGGGGYYYYYYYCCCCK.......",
    ".KRRGGGGGGYYYYYCCCCK........",
    "..KRRGGGGGGYYYCCCCK.........",
    "..KRRGGGGGGGGCCCCK..........",
    "..KRRGGGGGGGCCCCK...........",
    "..KRGGGGGGGGCCCCK...........",
    "..KRGGGGGGGGCCCCCK..........",
    "..KRGGGGGGGGGCCCCCK.........",
    "..KRGGGGGGGGGGCCCCCK........",
    "..KRGGGGGGGGGGCCCCCCK.......",
    "..KRGGGGGGGGGGGCCCCCCK......",
    "..KRGGGGGGGGGGGCCCCCCCK.....",
    "..KRGGGGGGGGGGGGCCCCCCCK....",
    ".KRRGGGGGGGGGGGGCCCCCCCCK...",
    ".KRRGGGGGGGGGGGGGCCCCCCCK...",
]
NECK_FROM = 25                         # art rows from here down are the RUFF. The back of the neck runs STRAIGHT
                                       # down from the back of the head: pinched in under the jaw and flared out
                                       # again, the silhouette read as an hourglass, and on a narrow throat before
                                       # that, as a lollipop


def head_offsets(fs):
    tmpl = [(x, y, fs[0][y][x]) for y in range(11, 39) for x in range(23, 51) if fs[0][y][x] in PD_HAIR]
    out = []
    for f in fs:
        best = max(((sum(1 for x, y, v in tmpl if 0 <= x + dx < 64 and 0 <= y + dy < 64 and f[y + dy][x + dx] == v), dx, dy)
                    for dy in range(-6, 7) for dx in range(-14, 15)))
        assert best[0] == len(tmpl), "a frame's head is not frame 0's head moved: %d of %d agree" % (best[0], len(tmpl))
        out.append((best[1], best[2]))
    return out


def fox_strip(fs):
    for f, (dx, dy) in zip(fs, head_offsets(fs)):
        ox, oy = BLOCK[0] + dx, BLOCK[1] + dy
        w, h = len(FOX_HEAD[0]), len(FOX_HEAD)
        # the old head goes: the bob and the lips anywhere in the block, and the face's pale eye in its top part.
        # Arm skin is NOT cleared by region -- in two frames an arm crosses the block.
        for y in range(max(0, oy), min(64, oy + h)):
            for x in range(max(0, ox), min(64, ox + w)):
                v = f[y][x]
                if v in PD_HAIR or v == PD_LIPS or (v == 14 and y - oy < NECK_FROM):
                    f[y][x] = 0
        # the human face's skin under the new head's silhouette goes too, and the new head is laid on
        for r, row in enumerate(FOX_HEAD):
            for c, ch in enumerate(row):
                x, y = ox + c, oy + r
                if 0 <= x < 64 and 0 <= y < 64 and FOXL[ch] is not None:
                    f[y][x] = FOXL[ch]
        # skin left in the face half above the throat is the old profile showing past the new one
        for y in range(max(0, oy), min(64, oy + NECK_FROM)):
            for x in range(max(0, ox + 12), min(64, ox + w)):
                if f[y][x] in PD_SKIN and FOX_HEAD[y - oy][x - ox] == ".":
                    f[y][x] = 0
        # the bob's own OUTLINE outlived the bob: ink with nothing left beside it is removed until none is
        changed = True
        while changed:
            changed = False
            for y in range(max(0, oy), min(64, oy + h)):
                for x in range(max(0, ox - 2), min(64, ox + w)):
                    if f[y][x] == INK and not any(0 <= x + dx < 64 and 0 <= y + dy < 64 and f[y + dy][x + dx] not in (0, INK)
                                                  for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):
                        f[y][x] = 0
                        changed = True
    # EVERYTHING STILL SKIN IS NOW AN ARM OR A SHOULDER: a white coat sleeve, grey at the paw -- the paw
    # being the pixels of each LIMB furthest from the middle of the coat. A scrap of old neck is not a limb
    # and has no paw; mapped by value, the sleeve came out a grey fur arm, so it is lifted a step.
    for f in fs:
        body = [(x, y) for y in range(64) for x in range(64) if f[y][x] in (5, 6, 8)]
        bx = sum(x for x, _ in body) / max(1, len(body)); by = sum(y for _, y in body) / max(1, len(body))
        for comp in components(f, PD_SKIN):
            far = max(((x - bx) ** 2 + (y - by) ** 2) ** 0.5 for x, y in comp)
            limb = len(comp) > 60
            for x, y in comp:
                d = ((x - bx) ** 2 + (y - by) ** 2) ** 0.5
                f[y][x] = 10 if limb and d > far - 6 else {1: 5, 2: 5, 3: 8, 4: 6}[f[y][x]]


FIGURES = [
    dict(name="the old iguana", file="old_man_back_pic.png", pal="old_man_back_pic.pal", colours=IGUANA, shape=iguana),
    dict(name="CRYSTAL CLEAR", file="pokedude_back_pic.png", pal="pokedude_back_pic.pal", colours=CRYSTAL, strip=fox_strip),
]


def main():
    rows, built = [], []
    for fig in FIGURES:
        #  Vanilla's frames are the skeleton, so they are read from UPSTREAM: the file on disk is this tool's own
        #  output, repainted and since outlined (T-184), and re-running on it failed its own head check (T-213).
        rel = os.path.relpath(os.path.join(BACKS, fig["file"]), GBA)
        src = Image.open(io.BytesIO(subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel],
                                                   check=True, capture_output=True).stdout))
        assert src.mode == "P" and src.size[0] == 64, "%s is %s %s" % (fig["file"], src.mode, src.size)
        fs = frames_of(src)
        if "strip" in fig:
            fig["strip"](fs)
        else:
            for f in fs:
                fig["shape"](f)
        pal = list(src.getpalette()[:48])
        for i, c in fig["colours"].items():
            pal[i * 3:i * 3 + 3] = list(c)
        out = Image.new("P", src.size)
        out.putpalette(pal + [0] * (768 - 48))
        op = out.load()
        for k, f in enumerate(fs):
            for y in range(64):
                for x in range(64):
                    op[x, k * 64 + y] = f[y][x]
        assert out.size == src.size, "%s would change size" % fig["file"]
        built.append((fig, out, [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]))
        rows.append((src, out, len(fs)))
    sheet = Image.new("RGB", (4 * 192, len(rows) * (192 * 2 + 12)), (40, 40, 46))
    y = 0
    for src, out, n in rows:
        for k in range(n):
            sheet.paste(src.crop((0, k * 64, 64, (k + 1) * 64)).convert("RGB").resize((192, 192), Image.NEAREST), (k * 192, y))
            sheet.paste(out.crop((0, k * 64, 64, (k + 1) * 64)).convert("RGB").resize((192, 192), Image.NEAREST), (k * 192, y + 192))
        y += 192 * 2 + 12
    sheet.save(PREVIEW)
    print("  %d strips -> preview %s (vanilla above, ours below)" % (len(built), PREVIEW))
    if WRITE:
        for fig, img, pal in built:
            img.save(os.path.join(BACKS, fig["file"]), bits=4)
            with open(os.path.join(PALS, fig["pal"]), "w") as fh:
                fh.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal))
        #  T-177's outline, which every picture of ours carries: drawn by the same pass, so this write lands where the
        #  tree is and does not take it off again (T-293).
        import gbaoutline
        gbaoutline.main(only=[os.path.splitext(fig["file"])[0] for fig, _, _ in built], write=True)
        print("  written %d strips and their palettes" % len(built))


if __name__ == "__main__":
    main()

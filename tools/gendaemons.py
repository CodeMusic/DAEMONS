#!/usr/bin/env python3
"""The four daemons the sprite server would not draw, authored in code (T-176; vision.md 9.4).

    python3 tools/gendaemons.py            # preview to /tmp/daemons_code.png
    python3 tools/gendaemons.py --write    # the eight drawings into gfx/daemons/, for gbasprite.py to colour

WHY THESE FOUR AND NOT THE OTHER THIRTY-NINE. T-176's batches drew twenty daemons from their Index entries and the
model drew them well. These four it would not draw, and they fail the same way: each is a CONCEPT rather than a
creature, so there is no animal for the model to reach for.

    PUNCHCARD   "It records by cutting. Every hole it makes is permanent"    -> it drew a lizard
    SUBSTRATE   "a mass, a temperature, and somewhere that it is"            -> it drew a robot
    OUTLIER     "far enough from the rest to be dropped from the average"    -> it drew a symmetrical blob
    RELEASE     "all of it, at once, and then dark"                          -> it drew a lamp POST beside it

T-131 adds a fifth, and it fails for a DIFFERENT reason worth keeping separate:

    DUPLEX      "It sends and receives at once, from opposite ends"          -> it drew a horse, eight times

DUPLEX is not an abstraction -- a body with a head at each end is a perfectly concrete animal. The model simply will
not draw ONE body with TWO heads: across three rounds and eight seeds it returned a single-headed quadruped or two
separate animals standing side by side. T-131 batch 7 hit the same wall on DUALCORE and settled it by drawing two
birds, which that entry allowed. This entry does not: "from opposite ends" is the whole of the daemon, so the two
heads have to share a body, and a body with a head at each end is four shapes to author.

Drawn here as genmisc.py and genships.py draw: every pixel authored, from shapes rather than from a prompt. A card
with real holes is trivial to author. One dark patch over one eye is trivial. A tail with a lamp on the end stays
attached, because it is drawn attached.

WHAT gbasprite.py EXPECTS, and what these files therefore are: 64x64 RGBA, the subject on transparency, the body in
NEUTRAL GREY -- it ramps the greys into the daemon's own type colour, so anything coloured here would fight it --
and the four STREAK MARKERS painted on the body in its own marker colours, one per routine slot (9.4 as amended).
"""
import ast, os, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "gfx/daemons")
PREVIEW = "/tmp/daemons_code.png"
WRITE = "--write" in sys.argv

#  The five greys gbasprite.py ramps, darkest last; K is the outline.
W, L, M, D, K = (243, 243, 242), (205, 205, 203), (163, 163, 161), (110, 110, 108), (28, 28, 30)


def markers():
    tree = ast.parse(open(os.path.join(ROOT, "tools/gbasprite.py")).read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "STREAK_MARKERS" for t in n.targets):
            return [tuple(c) for c in ast.literal_eval(n.value)]
    raise SystemExit("gbasprite.py no longer defines STREAK_MARKERS")


def canvas():
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def outline(im, ink=K):
    """ink every empty pixel that touches the drawing, so the figure reads at 64px the way the others do"""
    px, hits = im.load(), []
    for y in range(64):
        for x in range(64):
            if px[x, y][3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < 64 and 0 <= ny < 64 and px[nx, ny][3] and px[nx, ny][:3] != ink:
                    hits.append((x, y)); break
    for p in hits:
        px[p] = ink + (255,)


def streaks(im, x0, y0, step=4, length=9, down=3):
    """four parallel strokes across the body, one per routine slot, in gbasprite.py's marker colours"""
    d = ImageDraw.Draw(im)
    for i, mk in enumerate(markers()):
        x = x0 + i * step
        d.line([(x, y0), (x - down, y0 + length)], fill=mk + (255,))


# ---------------------------------------------------------------- PUNCHCARD (KABUTOPS)
def punchcard(back=False):
    im, d = canvas()
    d.rectangle([20, 10, 44, 52], fill=L + (255,))                 # the card itself
    d.polygon([(20, 10), (26, 10), (20, 16)], fill=(0, 0, 0, 0))   # the clipped corner, as a real card has
    d.rectangle([20, 46, 44, 52], fill=M + (255,))
    for row in range(5):                                           # rows of punched holes, cut clean through
        for col in range(6):
            x, y = 23 + col * 3, 16 + row * 6
            if (col + row) % 3 or back:
                d.rectangle([x, y, x + 1, y + 2], fill=(0, 0, 0, 0))
    d.polygon([(8, 30), (20, 22), (20, 30), (10, 36)], fill=M + (255,))    # two long blades, for the cutting
    d.polygon([(56, 30), (44, 22), (44, 30), (54, 36)], fill=M + (255,))
    d.line([(8, 30), (20, 23)], fill=W + (255,))
    d.line([(56, 30), (44, 23)], fill=W + (255,))
    d.rectangle([25, 53, 29, 57], fill=D + (255,))                 # two short feet
    d.rectangle([35, 53, 39, 57], fill=D + (255,))
    if not back:
        d.rectangle([27, 12, 31, 14], fill=D + (255,))             # two read heads, which are its eyes
        d.rectangle([34, 12, 38, 14], fill=D + (255,))
    streaks(im, 24, 34)
    outline(im)
    return im


# ---------------------------------------------------------------- SUBSTRATE (PORYGON)
def substrate(back=False):
    im, d = canvas()
    slabs = [(14, 30, 50, 42), (17, 20, 47, 31), (21, 12, 43, 21)]  # three stacked slabs: it HAS a mass
    for i, (x0, y0, x1, y1) in enumerate(slabs):
        d.rectangle([x0, y0, x1, y1], fill=(L if i % 2 else M) + (255,))
        d.line([(x0, y0), (x1, y0)], fill=W + (255,))               # the lit edge of each slab
        d.line([(x0, y1), (x1, y1)], fill=D + (255,))
    d.rectangle([20, 43, 27, 52], fill=D + (255,))                  # two blunt legs
    d.rectangle([37, 43, 44, 52], fill=D + (255,))
    if not back:
        d.rectangle([27, 15, 31, 18], fill=D + (255,))              # a plain front: two marks, no features
        d.rectangle([34, 15, 38, 18], fill=D + (255,))
        d.line([(28, 25), (36, 25)], fill=D + (255,))
    streaks(im, 22, 32)
    outline(im)
    return im


# ---------------------------------------------------------------- OUTLIER (CLEFABLE)
def outlier(back=False):
    im, d = canvas()
    d.ellipse([18, 20, 46, 50], fill=L + (255,))                    # a plain round body
    d.ellipse([22, 12, 42, 30], fill=L + (255,))
    d.polygon([(24, 16), (20, 4), (29, 12)], fill=L + (255,))       # one ear short
    d.polygon([(38, 14), (46, 2), (43, 17)], fill=L + (255,))       # and one LONGER: the one thing not average
    d.ellipse([19, 46, 27, 53], fill=M + (255,))
    d.ellipse([37, 46, 45, 53], fill=M + (255,))
    if not back:
        d.ellipse([24, 17, 31, 24], fill=D + (255,))                # the dark patch, over one eye only
        d.point((27, 20), fill=W + (255,))
        d.point((36, 20), fill=D + (255,))
        d.line([(30, 26), (34, 26)], fill=D + (255,))
    else:
        d.ellipse([25, 26, 33, 34], fill=M + (255,))                # the patch shows from behind too
    streaks(im, 24, 32)
    outline(im)
    return im


# ---------------------------------------------------------------- RELEASE (AMPHAROS)
def release(back=False):
    im, d = canvas()
    d.ellipse([12, 28, 46, 52], fill=L + (255,))                    # a deep woolly body, not a flat oval
    d.polygon([(24, 30), (34, 30), (32, 14), (26, 14)], fill=L + (255,))   # a long neck, tapering
    d.ellipse([21, 4, 39, 20], fill=L + (255,))                     # and the head set high on it
    d.ellipse([22, 16, 38, 24], fill=M + (255,))                    # the ruff where fleece meets neck
    for y in (34, 39, 44):                                          # the fleece, in bands
        d.line([(14, y), (44, y)], fill=M + (255,))
    for x in (17, 24, 32, 39):
        d.rectangle([x, 50, x + 4, 57], fill=D + (255,))            # four legs
    d.line([(45, 42), (55, 24)], fill=M + (255,), width=4)          # the tail, held up
    d.line([(45, 42), (55, 24)], fill=D + (255,), width=1)
    d.ellipse([46, 8, 62, 24], fill=W + (255,))                     # the lamp, large and ATTACHED
    d.ellipse([49, 11, 59, 21], fill=L + (255,))
    d.ellipse([52, 14, 56, 18], fill=W + (255,))
    if not back:
        d.rectangle([25, 10, 27, 12], fill=D + (255,))
        d.rectangle([33, 10, 35, 12], fill=D + (255,))
        d.line([(28, 15), (32, 15)], fill=D + (255,))
    streaks(im, 20, 33)
    outline(im)
    return im


# ---------------------------------------------------------------- DUPLEX (GIRAFARIG)
def duplex(back=False):
    """one body, a neck and a head at each end, facing opposite ways -- drawn side-on so both ends read at 64px"""
    im, d = canvas()
    d.ellipse([20, 30, 44, 46], fill=L + (255,))                    # the barrel body, shared
    d.rectangle([24, 34, 40, 44], fill=L + (255,))
    for x0, x1, sign in ((24, 15, -1), (40, 49, 1)):                # two necks, rising away from each other
        d.polygon([(x0, 35), (x0 + sign * 4, 35), (x1 + sign * 3, 16), (x1 - sign * 1, 14)], fill=L + (255,))
    for hx, sign in ((14, -1), (50, 1)):                            # two heads, each looking outward
        d.ellipse([hx - 6, 9, hx + 6, 19], fill=L + (255,))
        d.polygon([(hx + sign * 4, 12), (hx + sign * 8, 14), (hx + sign * 4, 17)], fill=M + (255,))   # muzzle
        d.rectangle([hx - 3, 4, hx - 2, 9], fill=M + (255,))        # two short horns apiece
        d.rectangle([hx + 2, 4, hx + 3, 9], fill=M + (255,))
        if not back:
            d.point((hx + sign * 2, 13), fill=D + (255,))           # an eye on each, looking its own way
    for x in (23, 29, 35, 41):                                    # four legs under the shared middle
        d.rectangle([x, 46, x + 3, 56], fill=D + (255,))
    d.line([(26, 34), (38, 34)], fill=W + (255,))                   # the lit top of the barrel
    if back:
        d.line([(32, 32), (32, 46)], fill=M + (255,))               # the seam down the middle: neither end leads
    streaks(im, 25, 36, step=3, length=7, down=2)
    outline(im)
    return im


SHEETS = [("punchcard", punchcard), ("substrate", substrate), ("outlier", outlier), ("release", release),
          ("duplex", duplex)]


def main():
    cells = []
    for name, make in SHEETS:
        for back in (False, True):
            im = make(back)
            cells.append((name + ("_back" if back else "_front"), im))
    S = 4
    out = Image.new("RGB", (len(cells) * (64 * S + 8), 64 * S + 4), (96, 150, 200))
    for i, (name, im) in enumerate(cells):
        big = im.resize((64 * S, 64 * S), Image.NEAREST)
        out.paste(big, (i * (64 * S + 8) + 4, 2), big)
    out.save(PREVIEW)
    print("  %d drawings -> %s" % (len(cells), PREVIEW))
    if WRITE:
        for name, im in cells:
            im.save(os.path.join(OUT, name + ".png"))
        print("  written: %s" % ", ".join(n for n, _ in cells))


if __name__ == "__main__":
    main()

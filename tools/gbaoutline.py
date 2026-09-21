#!/usr/bin/env python3
"""Give the 64px art a real OUTLINE, which is what T-177 found the broken portraits were missing.

    python3 tools/gbaoutline.py             # report: every picture's outline share, before and after
    python3 tools/gbaoutline.py --write     # draw it
    python3 tools/gbaoutline.py --only camper beauty [--write]

WHAT T-177 MEASURED, AND WHAT IT DID NOT. Nine statistics were tested against a list of broken portraits made by
eye. Crumbs, blobs and churn find TEXTURE, not breakage -- they rank a tweed jacket and a judo gi worst. Loose
pieces finds portraits with TWO FIGURES in them. Thin structures and fringe get closer. NONE of them reproduces
the eye's list, and the honest reading is that the eye was judging whether the SUBJECT is legible, which is not
a property of the pixels taken one at a time.

WHAT DID SEPARATE THEM was the silhouette's EDGE:

    the portraits that read draw 65-74% of their edge in their four darkest colours, and never the bright ones
    the portraits that do not draw their edge in EVERY colour they have -- 100% of the palette, for seven of nine

which is what a LANCZOS-resized anti-aliased drawing becomes after a 15-colour adaptive quantization. The edge is
not an outline, it is a BLEND, and it eats the palette slots the body needed: BEAUTY spends five of fifteen
colours on near-identical blues in one dress and has none left for her horns or her hands.

SO THE FIX IS NOT TO CLEAN FILES. It is to draw the outline the quantizer could not: every silhouette pixel takes
the darkest colour the picture already uses. Nothing is added to the palette, no colour is invented, and a picture
that already has an outline barely changes -- its edge was that colour anyway.

WHERE IT APPLIES: every 64px picture that is OURS -- trainer front pics, the hearsay portraits, the intro pictures
and the player's back pics. Vanilla's own art is never touched. The overworld is not in scope: T-170 measured that
16x32 is a different problem, and an outline at that size is most of the sprite.

The same pass runs inside gbachar.py, so a picture cut in future is outlined as it is written.
"""
import io, os, subprocess, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else []
ONLY = [a for a in ONLY if not a.startswith("--")]

FAMILIES = [
    ("trainer portraits", "graphics/trainers/front_pics"),
    ("hearsay portraits", "graphics/fame_checker"),
    ("intro pictures",    "graphics/oak_speech"),
    ("back pics",         "graphics/trainers/back_pics"),
]


def git(*a, binary=False):
    r = subprocess.run(["git", "-C", GBA] + list(a), capture_output=True)
    return r.stdout if binary else r.stdout.decode()


def is_ours(rel):
    """a picture vanilla never had, or one whose pixels differ from vanilla's -- never vanilla's own"""
    raw = git("show", "upstream/master:" + rel, binary=True)
    if not raw:
        return True
    try:
        theirs = Image.open(io.BytesIO(raw))
    except Exception:
        return True
    ours = Image.open(os.path.join(GBA, rel))
    return ours.size != theirs.size or ours.tobytes() != theirs.tobytes()


def luminance(im):
    p = im.getpalette() or []
    p = p + [0] * (768 - len(p))
    return np.array([(p[i * 3] * 299 + p[i * 3 + 1] * 587 + p[i * 3 + 2] * 114) // 1000 for i in range(256)])


def edge_of(a):
    fig = a != 0
    bg = ~fig
    nb = sum(np.roll(bg, s, ax) for s, ax in ((1, 0), (-1, 0), (1, 1), (-1, 1)))
    return fig, fig & (nb > 0)


def palette_of(rel, im):
    """the palette a trainer picture actually renders with is its .pal, not the one inside the PNG"""
    pf = os.path.join(GBA, "graphics/trainers/palettes",
                      os.path.basename(rel).replace("_front_pic.png", ".pal"))
    if os.path.exists(pf):
        rows = [l.split() for l in open(pf).read().splitlines()[3:] if l.split()]
        return pf, [[int(v) for v in r] for r in rows]
    #  ALL 256, not 16: the intro pictures are 8bpp and live in palette BANKS -- the player's indices start at
    #  65 and CRYSTAL's at 97 (engine.md) -- so a sixteen-entry read finds their colours all black and decides
    #  every one of them needs a new one.
    p = (im.getpalette() or []) + [0] * 768
    return None, [p[i * 3:i * 3 + 3] for i in range(256)]


def share(a, lum, k=4):
    """how much of the silhouette's edge is drawn in the picture's own darkest colours"""
    fig, edge = edge_of(a)
    if not edge.sum():
        return 100.0
    used = np.unique(a[fig])
    dark = used[np.argsort(lum[used])][:k]
    return float(np.isin(a[edge], dark).sum() / edge.sum() * 100)


INK = (16, 16, 20)          # near-black, and the same near-black for every picture


def choose_ink(a, lum, pal):
    """Which palette entry becomes the OUTLINE, and whether it has to be recoloured to get there.

    T-177 laid the outline in "the darkest colour the picture already uses", which spends nothing but gives a
    RED daemon a dark red edge and a grey one a near-black -- one rule, two looks, and the user saw it at once.
    A true black is worth one palette entry, so one entry is taken.

    WHICH ONE depends on what it costs. The darkest entry is the natural choice and usually already reads as
    black; but on a picture whose darkest shade is a mid-tone doing real work, forcing it to black darkens
    every pixel of that shade. So: take the darkest -- unless that would repaint more than a twelfth of the
    figure, in which case take the LEAST-USED entry instead and lose a highlight nobody counts.
    """
    fig, _ = edge_of(a)
    used = np.unique(a[fig])
    used = used[used != 0]
    if not len(used):
        return None, False
    counts = {int(i): int((a[fig] == i).sum()) for i in used}
    darkest = int(used[np.argmin(lum[used])])
    if lum[darkest] <= 48:
        return darkest, False                                  # already black enough; nothing is repainted
    if counts[darkest] <= fig.sum() / 12:
        return darkest, True
    return min(counts, key=lambda i: counts[i]), True


def outline(a, lum, ink_index):
    """the chosen entry, laid along the picture's own silhouette"""
    fig, edge = edge_of(a)
    if ink_index is None:
        return a
    b = a.copy()
    b[edge] = ink_index
    return b


def main():
    done = recoloured = 0
    for label, folder in FAMILIES:
        rows = []
        for base, _, files in os.walk(os.path.join(GBA, folder)):
            for f in sorted(files):
                if not f.endswith(".png"):
                    continue
                rel = os.path.relpath(os.path.join(base, f), GBA)
                name = os.path.splitext(f)[0]
                if name == "pic":                      # oak_speech/<who>/pic.png -- the folder is the name
                    name = os.path.basename(base)
                if ONLY and name not in ONLY and name.replace("_front_pic", "") not in ONLY:
                    continue
                if not is_ours(rel):
                    continue
                im = Image.open(os.path.join(GBA, rel))
                if im.mode != "P" or im.size[0] != 64:
                    continue
                a = np.array(im)
                palfile, pal = palette_of(rel, im)
                lum = np.array([(c[0] * 299 + c[1] * 587 + c[2] * 114) // 1000 for c in pal]
                               + [0] * (256 - len(pal)))
                ink, repaint = choose_ink(a, lum, pal)
                before = share(a, lum)
                #  A BACK PIC IS A STRIP of 64x64 frames stacked (red's is 64x320). Outlining the strip whole is
                #  wrong at the seams: one frame's feet sit against the next frame's head, so those pixels are not
                #  silhouette at all. Each frame is outlined on its own.
                #
                #  BUT ONLY A STRIP IS A STRIP. Splitting every picture on 64 drew a cut line straight across the
                #  four intro pictures, which are 64x96 -- one figure, not a frame and a half -- and the user saw it
                #  in play as "a black line in her middle" on CRYSTAL, the player in both poses and the rival. Rows
                #  63 and 64 carried three times the dark pixels of any other row. A strip's height is a MULTIPLE
                #  of 64; anything else is one picture and is outlined whole.
                h = a.shape[0]
                step = 64 if h > 64 and h % 64 == 0 else h
                b = a.copy()
                for top in range(0, h, step):
                    b[top:top + step] = outline(a[top:top + step], lum, ink)
                if repaint:
                    pal[ink] = list(INK)
                    lum[ink] = (INK[0] * 299 + INK[1] * 587 + INK[2] * 114) // 1000
                after = share(b, lum)
                rows.append((name, before, after, int((a != b).sum()), repaint))
                if WRITE and ((a != b).any() or repaint):
                    full = [v for c in pal for v in c] + [0] * (768 - 3 * len(pal))
                    out = Image.fromarray(b, "P")
                    out.putpalette(full)
                    out.save(os.path.join(GBA, rel))
                    if palfile and repaint:
                        with open(palfile, "w") as fh:
                            fh.write("JASC-PAL\n0100\n%d\n" % len(pal))
                            for c in pal:
                                fh.write("%d %d %d\n" % tuple(c))
                        recoloured += 1
                    done += 1
        if rows:
            print("  %-19s %d ours: edge in its darkest four, %.0f%% -> %.0f%%; %d took a true black"
                  % (label, len(rows), np.mean([r[1] for r in rows]), np.mean([r[2] for r in rows]),
                     sum(1 for r in rows if r[4])))
    print("  %s" % ("%d written, %d palettes given a near-black" % (done, recoloured)
                    if WRITE else "report only; pass --write"))


if __name__ == "__main__":
    main()

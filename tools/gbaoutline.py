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


def share(a, lum, k=4):
    """how much of the silhouette's edge is drawn in the picture's own darkest colours"""
    fig, edge = edge_of(a)
    if not edge.sum():
        return 100.0
    used = np.unique(a[fig])
    dark = used[np.argsort(lum[used])][:k]
    return float(np.isin(a[edge], dark).sum() / edge.sum() * 100)


def outline(a, lum):
    """the darkest colour the picture already uses, laid along its own silhouette"""
    fig, edge = edge_of(a)
    used = np.unique(a[fig])
    if not len(used):
        return a
    b = a.copy()
    b[edge] = used[np.argmin(lum[used])]
    return b


def main():
    done = 0
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
                lum = luminance(im)
                before = share(a, lum)
                #  A BACK PIC IS A STRIP of 64x64 frames stacked (red's is 64x320). Outlining the strip whole is
                #  wrong at the seams: one frame's feet sit against the next frame's head, so those pixels are not
                #  silhouette at all. Each frame is outlined on its own.
                b = a.copy()
                for top in range(0, a.shape[0], 64):
                    b[top:top + 64] = outline(a[top:top + 64], lum)
                after = share(b, lum)
                rows.append((name, before, after, (a != b).sum()))
                if WRITE and (a != b).any():
                    out = Image.fromarray(b, "P")
                    out.putpalette(im.getpalette())
                    out.save(os.path.join(GBA, rel))
                    done += 1
        if rows:
            print("  %-19s %d ours: edge in its darkest four, %.0f%% -> %.0f%% (%d px redrawn)"
                  % (label, len(rows), np.mean([r[1] for r in rows]), np.mean([r[2] for r in rows]),
                     sum(r[3] for r in rows)))
            for name, b4, af, n in sorted(rows, key=lambda r: r[1])[:5]:
                print("       %-26s %3.0f%% -> %3.0f%%" % (name, b4, af))
    print("  %s" % ("%d written" % done if WRITE else "report only; pass --write"))


if __name__ == "__main__":
    main()

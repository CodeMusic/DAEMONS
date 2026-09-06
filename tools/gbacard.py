"""TRAINER CARD -> USER CARD, BADGES -> MARKS.

Both are pixel lettering baked into trainer_card/tiles.png, which is why the
string renames never reached them -- gText_Badges has said MARKS for weeks.

CARD does not move: only the first word changes, and USER is shorter than
TRAINER, so the tail is cleared back to background. Two fonts are involved --
a 9-row header face and a 5-row label face -- and between them the sheet
already carries every letter except U and S in the big one and M, R and K in
the small one. Those five are drawn to match; the rest are lifted.
"""
import os, sys
import numpy as np
from PIL import Image

GBA = "engineGba"
P = os.path.join(GBA, "graphics/trainer_card/tiles.png")
WRITE = "--write" in sys.argv
im = Image.open(P); a = np.asarray(im).copy()

def glyphs(y0, y1, x0, x1, ink_vals, label):
    reg = a[y0:y1, x0:x1]
    ink = np.isin(reg, ink_vals)
    cols = ink.any(axis=0); runs = []; s = None
    for i, v in enumerate(cols):
        if v and s is None: s = i
        if not v and s is not None: runs.append((s, i)); s = None
    if s is not None: runs.append((s, len(cols)))
    return {ch: ink[:, r[0]:r[1]] for ch, r in zip(label, runs)}

def draw(bmp, y, x, ink, shade, bg):
    h, w = bmp.shape
    a[y:y+h, x:x+w] = np.where(bmp, ink, bg)

def parse(rows):
    return np.array([[c == '#' for c in r] for r in rows])

# ---- the header face -------------------------------------------------------
BIG = glyphs(28, 37, 60, 124, (8, 9), "TRAINER")
BIG['U'] = parse(["##...##"]*7 + ["#######"]*2)
BIG['S'] = parse(["#######", "##.....", "##.....", "#######", "#######",
                  ".....##", ".....##", "#######", "#######"])
a[28:37, 64:120] = 0xA                       # clear TRAINER
x = 64
for ch in "USER":
    g = BIG[ch]
    draw(g, 28, x, 8, 9, 0xA)
    x += g.shape[1] + 1
print("  header  TRAINER -> USER   (%d px of %d used)" % (x - 65, 56))

# ---- the label face --------------------------------------------------------
SM = glyphs(42, 47, 96, 128, (0xE,), "BADGES")
# M gets five columns: at four it is an H. There is room -- MARKS is
# shorter than BADGES either way.
SM['M'] = parse(["#...#", "##.##", "#.#.#", "#...#", "#...#"])
SM['R'] = parse(["####", "##.#", "####", "##.#", "##.#"])
SM['K'] = parse(["#..#", "#.#.", "##..", "#.#.", "#..#"])
a[42:47, 96:128] = 0xF                       # clear BADGES
x = 99
for ch in "MARKS":
    g = SM[ch]
    draw(g, 42, x, 0xE, 0xE, 0xF)
    x += g.shape[1] + 1
print("  label   BADGES  -> MARKS  (%d px of %d used)" % (x - 100, 29))

if WRITE:
    out = Image.new("P", im.size); out.putdata(a.flatten().tolist())
    out.putpalette(im.getpalette()); out.save(P)
    print("  written")

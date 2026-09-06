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

# NOT IDEMPOTENT BY NATURE: this lifts letters from the very words it is about
# to overwrite, so a second run finds USER where it expects TRAINER. Each
# section counts the glyphs already there and skips if the work is done.
def count(y0, y1, x0, x1, ink_vals):
    reg = np.isin(a[y0:y1, x0:x1], ink_vals)
    cols = reg.any(axis=0); n = 0; prev = False
    for v in cols:
        if v and not prev: n += 1
        prev = v
    return n

# ---- the header face -------------------------------------------------------
if count(28, 37, 60, 124, (8, 9)) == 7:
  BIG = glyphs(28, 37, 60, 124, (8, 9), "TRAINER")
  BIG['U'] = parse(["##...##"]*7 + ["#######"]*2)
  BIG['S'] = parse(["#######", "##.....", "##.....", "#######", "#######",
                    ".....##", ".....##", "#######", "#######"])
  a[28:37, 64:120] = 0xA                     # clear TRAINER
  x = 64
  for ch in "USER":
      g = BIG[ch]
      draw(g, 28, x, 8, 9, 0xA)
      x += g.shape[1] + 1
  print("  header  TRAINER -> USER   (%d px of %d used)" % (x - 65, 56))
else:
  print("  header  already USER CARD")

# ---- the label face --------------------------------------------------------
if count(42, 47, 96, 128, (0xE,)) == 6:
  SM = glyphs(42, 47, 96, 128, (0xE,), "BADGES")
  # M gets five columns: at four it is an H.
  SM['M'] = parse(["#...#", "##.##", "#.#.#", "#...#", "#...#"])
  SM['R'] = parse(["####", "##.#", "####", "##.#", "##.#"])
  SM['K'] = parse(["#..#", "#.#.", "##..", "#.#.", "#..#"])
  a[42:47, 96:128] = 0xF                     # clear BADGES
  x = 99
  for ch in "MARKS":
      g = SM[ch]
      draw(g, 42, x, 0xE, 0xE, 0xF)
      x += g.shape[1] + 1
  print("  label   BADGES  -> MARKS  (%d px of %d used)" % (x - 100, 29))
else:
  print("  label   already MARKS")

if WRITE:
    out = Image.new("P", im.size); out.putdata(a.flatten().tolist())
    out.putpalette(im.getpalette()); out.save(P)
    print("  written")

# ---------------------------------------------------------------------------
# FAME CHECKER -> HEARSAY, in the banner baked into fame_checker/bg.png.
#
# The device records what you were TOLD about people, which is 0.2's
# reproduction that loses the original wearing a key-item icon. HEARSAY is
# both what it holds and what the word means -- testimony that is not
# firsthand -- and it checks nothing, which the description now says.
#
# A 7-row face, ink 7 on ground 6. FAME<>CHECKER already carries H, E, A and
# R; only S and Y are drawn.
FP = os.path.join(GBA, "graphics/fame_checker/bg.png")
fim = Image.open(FP); fa = np.asarray(fim).copy()

def fglyphs(y0, y1, x0, x1, label):
    reg = fa[y0:y1, x0:x1]
    ink = reg == 7
    cols = ink.any(axis=0); runs = []; st = None
    for i, v in enumerate(cols):
        if v and st is None: st = i
        if not v and st is not None: runs.append((st, i)); st = None
    if st is not None: runs.append((st, len(cols)))
    return {ch: ink[:, r[0]:r[1]] for ch, r in zip(label, runs)}, runs

def fcount():
    reg = fa[13:20, 5:72] == 7
    cols = reg.any(axis=0); n = 0; prev = False
    for v in cols:
        if v and not prev: n += 1
        prev = v
    return n

if fcount() == 7:
    print("  banner  already HEARSAY")
    raise SystemExit
# The extraction that worked for the card does NOT work here: FAME<>CHECKER
# has a two-glyph symbol in the middle drawn in a different colour, so the
# run-splitting mismaps every letter after it. Seven glyphs at 4x7 is less
# code than teaching it about the symbol.
FONT = {
 "H": ["#..#", "#..#", "#..#", "####", "#..#", "#..#", "#..#"],
 "E": ["####", "#...", "#...", "####", "#...", "#...", "####"],
 "A": [".##.", "#..#", "#..#", "####", "#..#", "#..#", "#..#"],
 "R": ["###.", "#..#", "#..#", "###.", "#.#.", "#..#", "#..#"],
 "S": ["####", "#...", "#...", "####", "...#", "...#", "####"],
 "Y": ["#..#", "#..#", ".##.", "..#.", "..#.", "..#.", "..#."],
}
x0 = 9
fa[13:20, 5:72] = 6                              # clear the banner text
x = x0
for ch in "HEARSAY":
    g = parse(FONT[ch]); h, w = g.shape
    fa[13:13+h, x:x+w] = np.where(g, 7, 6)
    x += w + 1
print("  banner  FAME CHECKER -> HEARSAY  (%d px of %d)" % (x - x0 - 1, 72 - x0))

if WRITE:
    fout = Image.new("P", fim.size); fout.putdata(fa.flatten().tolist())
    fout.putpalette(fim.getpalette()); fout.save(FP)
    print("  written")

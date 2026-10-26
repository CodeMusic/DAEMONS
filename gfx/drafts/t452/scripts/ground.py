"""T-452: stand each redrawn daemon on the ground line -- its front_/back_pic_coordinates.h rows from the built art.

    ground.py SLOT ...           report
    ground.py --write SLOT ...   rewrite those species' rows in engineGba/src/data/pokemon_graphics/

The rule batch 1 used (engine c0eb28f32), measured back off its rows: .size is the opaque box rounded up to 8 each
way, .y_offset = 63 - the lowest opaque row, so every front's feet and every back's feet sit on the frame's bottom row
whatever size the drawing is. Reads graphics/pokemon/SLOT/{front,back}.png (the top 64 rows: PROTEUS's are 128)."""
import re, sys
import numpy as np
from PIL import Image
G = "/Users/christopherhicks/Projects/DAEMONS/engineGba/"
TAB = {"front": G + "src/data/pokemon_graphics/front_pic_coordinates.h", "back": G + "src/data/pokemon_graphics/back_pic_coordinates.h"}
WRITE = "--write" in sys.argv; slots = [a for a in sys.argv[1:] if not a.startswith("--")]

def measure(slot, k):
    a = np.array(Image.open(f"{G}graphics/pokemon/{slot}/{k}.png"))[:64]
    ys, xs = np.where(a > 0)
    up = lambda v: min(64, (v + 7) // 8 * 8)
    return up(xs.max() - xs.min() + 1), up(ys.max() - ys.min() + 1), 63 - ys.max()

for k, f in TAB.items():
    t = open(f).read()
    for s in slots:
        w, h, y = measure(s, k)
        pat = re.compile(r"(\[SPECIES_%s\] =\s*\{\s*\.size = MON_COORDS_SIZE\()(\d+), (\d+)(\),\s*\.y_offset = )(\d+)" % s.upper())
        m = pat.search(t)
        if not m: raise SystemExit(f"{s}: no {k} row")
        old = (int(m[2]), int(m[3]), int(m[5]))
        print("%-6s %-11s %s -> %s" % (k, s, old, (w, h, y)))
        t = pat.sub(lambda m: f"{m[1]}{w}, {h}{m[4]}{y}", t, count=1)
    if WRITE: open(f, "w").write(t)

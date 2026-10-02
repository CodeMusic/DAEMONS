#!/usr/bin/env python3
"""T-210 batch 2: clean each picked draft (PICKS.txt; backs from back2/ once picked) into gfx/drafts/t210b2/clean/,
then grey it -- batch 15's order (fix.py): the coloured draft is cleaned first and the CLEANED sprite greyed, every pixel
but gbasprite.py's four streak markers, so the body takes its type's colour. Run from the repo root.

    python3 gfx/drafts/t210b2/clean.py NAME VIEW DRAFT [NAME VIEW DRAFT ...]"""
import ast, os, subprocess, sys
from PIL import Image
tree = ast.parse(open("tools/gbasprite.py").read())
MARKS = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "STREAK_MARKERS" for t in n.targets))
MARKS = {tuple(m) for m in (MARKS.values() if isinstance(MARKS, dict) else MARKS)}
C = "gfx/drafts/t210b2/clean"
#  Where cleandraft's automatic placement finds no body (a narrow trunk), the streaks go in the box given here, in art px.
BOX = {}
os.makedirs(C, exist_ok=True)
args = sys.argv[1:]
for name, view, draft in zip(args[0::3], args[1::3], args[2::3]):
    out = "%s/%s_%s.png" % (C, name, view)
    box = BOX.get((name, view))
    r = subprocess.run(["python3", "tools/cleandraft.py", draft, out, "--streaks"] + (["--streak-box=" + box] if box else []),
                       capture_output=True, text=True)
    if not os.path.exists(out) and "no body to sit on" in r.stderr:
        #  The automatic placement found no body (a narrow trunk, a coiled eel): measure the outline without streaks
        #  and try boxes over the middle of the body, widest first, until all four streaks land.
        tmp = out + ".plain.png"
        subprocess.run(["python3", "tools/cleandraft.py", draft, tmp], capture_output=True, text=True)
        x0, y0, x1, y1 = Image.open(tmp).getchannel("A").getbbox()
        os.remove(tmp)
        w, h = x1 - x0, y1 - y0
        for fx, fy0, fy1 in ((0.15, 0.3, 0.7), (0.2, 0.35, 0.65), (0.1, 0.4, 0.8), (0.25, 0.25, 0.6), (0.2, 0.5, 0.85)):
            box = "%d,%d,%d,%d" % (x0 + w * fx, y0 + h * fy0, x1 - w * fx, y0 + h * fy1)
            r = subprocess.run(["python3", "tools/cleandraft.py", draft, out, "--streaks", "--streak-box=" + box],
                               capture_output=True, text=True)
            if os.path.exists(out):
                print("  %-10s %-5s streaks in box %s (the automatic place found no body)" % (name, view, box))
                break
    if not os.path.exists(out):
        print("  %-10s %-5s FAILED: %s" % (name, view, r.stderr.strip().splitlines()[-1:]))
        continue
    print("  %-10s %-5s %s" % (name, view, (r.stdout.strip().splitlines() or [r.stderr.strip()])[-1]))
    im = Image.open(out).convert("RGBA"); px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            rr, g, b, a = px[x, y]
            if a and (rr, g, b) not in MARKS:
                l = (rr * 299 + g * 587 + b * 114) // 1000
                px[x, y] = (l, l, l, a)
    im.save(out)

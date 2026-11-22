"""T-607: autumn again, as T-553 had to (gfx/drafts/t552_t553/scripts/autumn_grey.py): the coat prompt turned the whole
body orange, which the reduction keeps or rotates off the type. Grey fur, orange only in a few loose leaves. The same
references as seasons.py. Two seeds, 8101 and 8102. Nothing writes into the game."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t452/scripts")
import armc, importlib.util
_spec = importlib.util.spec_from_file_location("t607seasons", HERE + "/seasons.py")   # not tools/seasons.py
_s = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_s)
KEEP, T605, PICKS = _s.KEEP, _s.T605, _s.PICKS
OUT = D + "/autumn2"; os.makedirs(OUT, exist_ok=True)
COVER = {"songmusai": "its fur stays GREY exactly as in the image, not orange, not brown, in thick autumn fur, three or four "
                      "small orange autumn leaves caught on its grey fur and falling around it",
         "langmusai": "its scales and fur ruff stay GREY exactly as in the image, not orange, not brown, its ruff thick for "
                      "autumn, three or four small orange autumn leaves caught on it and falling around it"}
for n, src in PICKS.items():
    for seed in (8101, 8102):
        o = "%s/%s_autumn_%d" % (OUT, n, seed); print("drawing", o, flush=True)
        armc.draw(o, "pixel art sprite, chibi, the same creature as in the image, the same round helmet head, the same dark visor "
                  "with glowing eyes, " + KEEP[n] + ", the same body shape and markings, " + COVER[n] + ", nothing else changed, "
                  "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only the leaves coloured, "
                  "facing left three-quarter view, black outline, centered on a plain white background, full body, the whole body "
                  "inside the picture with white space on every side, no shadow, no text, game asset", seed,
                  refs=[T605 + "/" + src + ".png"])
print("ALLDONE", flush=True)

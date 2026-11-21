"""T-607 round two: after the first reduction (reduced/cand/), SONGMUSAI's winter read as its summer (the frost sparkles
float free and cleandraft drops them; white fur reduces to its light teal), and both autumns lost their loose leaves
the same way. So the season is put ON the body: SONGMUSAI's winter a thick white ruff and a fluffier tail, frost on the
helmet; each autumn's leaves caught in its fur, on its head and along its back and tail, the fur still grey (T-553's
autumn rule). Seeds 8301 and 8302. Nothing writes into the game."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t452/scripts")
import armc, importlib.util
_spec = importlib.util.spec_from_file_location("t607seasons", HERE + "/seasons.py")   # not tools/seasons.py
_s = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_s)
KEEP, T605, PICKS = _s.KEEP, _s.T605, _s.PICKS
OUT = D + "/round2"; os.makedirs(OUT, exist_ok=True)
HEAD = "pixel art sprite, chibi, the same creature as in the image, the same round helmet head, the same dark visor with glowing eyes, "
END = (", mostly greyscale, medium grey body with light grey highlights and dark grey shading, facing left three-quarter view, "
       "black outline, centered on a plain white background, full body, the whole body inside the picture with white space on "
       "every side, nothing floating around it, no sparkles, no shadow, no text, game asset")
JOBS = {
 ("songmusai", "winter"): "in its thick winter coat: a big fluffy white ruff of fur round its neck and chest like a scarf, its "
                          "curled tail twice as thick and fluffy, a cap of white frost and a little snow on top of its helmet, "
                          "the rest of its fur grey",
 ("songmusai", "autumn"): "its fur stays GREY exactly as in the image, not orange, not brown, four or five small orange and red "
                          "autumn leaves stuck in its fur, one on top of its helmet, two in its chest fur, two caught in its curled tail",
 ("langmusai", "autumn"): "its scales and fur ruff stay GREY exactly as in the image, not orange, not brown, four or five small orange "
                          "and red autumn leaves caught on it, one on top of its helmet, two tucked in its neck frill, two along "
                          "its back and tail",
}
for (n, s), part in JOBS.items():
    for seed in (8301, 8302):
        o = "%s/%s_%s_%d" % (OUT, n, s, seed); print("drawing", o, flush=True)
        armc.draw(o, HEAD + KEEP[n] + ", the same body shape and markings, " + part + END, seed,
                  refs=[T605 + "/" + PICKS[n] + ".png"])
print("ALLDONE", flush=True)

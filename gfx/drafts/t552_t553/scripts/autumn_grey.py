"""T-553: autumn again -- the seasons pass turned whole coats orange, and the reduction keeps or rotates an orange body off
its type (MUSAI's went blue). Grey fur; orange only in a few loose leaves. Same references as seasons.py. Two seeds."""
import os, sys
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts"); sys.path.insert(0, R + "/gfx/drafts/t552_t553/scripts")
import armc
D = R + "/gfx/drafts/t552_t553/"; OUT = D + "autumn2"; os.makedirs(OUT, exist_ok=True)
REF = {"musai": "round2/musai_summer_7301", "codemusai": "round2/codemusai_summer_7302", "lensmusai": "round2/lensmusai_spring_7301",
       "caremusai": "round2/caremusai_summer_7302", "maskmusai": "round3/maskmusai_winter_7402", "seekmusai": "round2/seekmusai_autumn_7301"}
PART = {"musai": "nothing else changed", "codemusai": "four big chunky round paws with deep treads like off-road tyres, dark stripes arching over its back like a roll cage",
        "lensmusai": "its gliding membranes spread", "caremusai": "slightly webbed paws, the small deck on its back",
        "maskmusai": "its hind feet a little longer and flatter than usual", "seekmusai": "its chunky tread paws and roll-cage stripes"}
for n, b in REF.items():
    if n == "seekmusai": continue   # its autumn is its home body, already grey
    for seed in (7601, 7602):
        o = "%s/%s_autumn_%d" % (OUT, n, seed); print("drawing", o, flush=True)
        armc.draw(o, "pixel art sprite, chibi, the same creature as in the image, the same round helmet head, the same dark visor with glowing eyes, "
                  "the same antennae, the same body shape and markings, its fur stays GREY exactly as in the image, not orange, not brown, "
                  "in thick autumn fur, three or four small orange autumn leaves caught on its grey fur and falling around it, " + PART[n] + ", "
                  "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only the leaves coloured, "
                  "facing left three-quarter view, black outline, centered on a plain white background, full body, the whole body inside the "
                  "picture with white space on every side, no shadow, no text, game asset", seed, refs=[D + b + ".png"])
print("ALLDONE", flush=True)

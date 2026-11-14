"""T-553: MASKMUSAI winter, pass b -- round two's 7302 (standing on skis) as the reference, its skis turned into its own feet."""
import os, sys
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts")
import armc
OUT = R + "/gfx/drafts/t552_t553/round3"
GREY = "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
P = ("pixel art sprite, chibi, the same creature as in the image, the same round helmet head, dark visor, antennae and fluffy tail, "
     "but the two skis are now its own two hind feet: each hind foot is one very long flat narrow furry foot exactly the length and "
     "shape of a ski, with a turned-up furry tip at the front, grey fur with a pale underside, joined to its legs, part of its body, "
     "two short front paws, crouched low, gliding, frost sparkles, " + GREY + "facing left three-quarter view, "
     "black outline, centered on a plain white background, full body, no shadow, game asset")
ref = R + "/gfx/drafts/t552_t553/round2/maskmusai_winter_7302.png"
for seed in (7411, 7412, 7413, 7414):
    o = "%s/maskmusai_winter_%d" % (OUT, seed); print("drawing", o, flush=True)
    armc.draw(o, P, seed, refs=[ref])
print("ALLDONE", flush=True)

"""T-553: MASKMUSAI winter again -- round two stood it ON skis; the skis must be its FEET. Four seeds."""
import os, sys
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts"); sys.path.insert(0, R + "/gfx/drafts/t552_t553/scripts")
import armc
OUT = R + "/gfx/drafts/t552_t553/round3"; os.makedirs(OUT, exist_ok=True)
GREY = "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
HEAD = ("keep exactly the same big round smooth helmet-like head as the creature in the image, with the same dark glossy visor "
        "across its face and two small glowing eyes showing through it and the same two little antennae, "
        "but below the head a natural furry animal body, soft fur, paws, a tail, ")
BODY = ("a snow hare body in thick white-grey winter fur, its two hind feet are enormous, very long, flat and narrow furry feet "
        "with turned-up toes, like a snowshoe hare's, lying flat on the snow and stretching far behind it, they are part of its body, "
        "furry feet not objects, there is nothing under it, no skis, no board, no sled, crouched low and leaning forward fast, "
        "a dark mask marking round the visor, frost sparkles")
TAIL = armc.TAIL.split("full body, ", 1)[1].replace(GREY, "")
ref = armc.rom_ref("musai")
for seed in (7401, 7402, 7403, 7404):
    o = "%s/maskmusai_winter_%d" % (OUT, seed); print("drawing", o, flush=True)
    armc.draw(o, armc.PFX + HEAD + BODY + ", " + GREY + "facing left three-quarter view, " + TAIL, seed, refs=[ref])
print("ALLDONE", flush=True)

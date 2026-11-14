"""T-553 round two (the user, 2026-11-14: "Keep MUSAI's head"): each form a natural creature body under the branch's
round helmet head and dark visor, the season's vehicle drawn large as anatomy; and T-552's ROVERSEER redrawn as a
body that IS the server. Reference: MUSAI's ROM front at 8x, for the head. Nothing writes into the game."""
import os, sys
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts")
import armc
OUT = R + "/gfx/drafts/t552_t553/round2"; os.makedirs(OUT, exist_ok=True)
GREY = "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
HEAD = ("keep exactly the same big round smooth helmet-like head as the creature in the image, with the same dark glossy visor "
        "across its face and two small glowing eyes showing through it and the same two little antennae, "
        "but below the head a natural furry animal body, soft fur, paws, a tail, ")
FORMS = {
 "musai_summer":     "a small fox-kit body sitting neatly, a fluffy tail curled round its paws, simple and plain, the base form",
 "codemusai_summer": "a sleek lean fox body standing alert and precise, four round spots in a row on its furry chest, two bright, one dark, one bright, red tips on its antennae",
 "maskmusai_winter": "a stoat body in thick white-grey winter fur, very long flat narrow hind feet shaped exactly like a pair of skis stretched out behind it, two short forepaws held out like handlebars, crouched low and fast, frost sparkles",
 "lensmusai_spring": "a sugar glider body with big wide gliding membranes of fur stretched between its front and back legs like the wings of a small model aeroplane, spread out wide, a long tail ending in a propeller-shaped tuft, gliding through the air, a small green sprout on its head",
 "caremusai_summer": "a round otter body floating, two big plump rounded webbed hind feet held out side by side like the twin floats of a pontoon boat, a flat broad back like a deck, wet glossy fur, calm and warm, a few water droplets",
 "seekmusai_autumn": "a low broad sturdy badger body, four big chunky round paws with deep treads like off-road tyres, strong dark stripes over its back and shoulders arching like a roll cage, a few orange autumn leaves caught in its fur, ready to run over rough ground",
}
SEER = (GREY + "a half-built robot dog whose whole lower body IS a heavy server chassis: its haunches are a box-shaped computer rack with "
        "vent slits and blinking drive lights, it cannot walk, it sits planted, thick cables grow out of its body down to the ground, "
        "its front legs are stiff metal struts, its head is a metal robot head just beginning to look like a dog, with two flat metal "
        "flaps for ears that are starting to droop like soft ears, one round glowing lens for an eye and one small dark eye, facing left three-quarter view")
ref = armc.rom_ref("musai")
for n, body in FORMS.items():
    for seed in (7301, 7302):
        o = "%s/%s_%d" % (OUT, n, seed); print("drawing", o, flush=True)
        armc.draw(o, armc.PFX + HEAD + body + ", " + GREY + "facing left three-quarter view, " + armc.TAIL.split("full body, ", 1)[1].replace("mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, ", ""), seed, refs=[ref])
for seed in (7301, 7302):
    o = "%s/roverseer_%d" % (OUT, seed); print("drawing", o, flush=True)
    armc.draw(o, armc.PFX + SEER + ", " + armc.TAIL.split("full body, ", 1)[1], seed)
print("ALLDONE", flush=True)

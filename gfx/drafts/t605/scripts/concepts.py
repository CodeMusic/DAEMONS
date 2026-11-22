"""T-605 concepts (the user, 2026-11-21: MUSAI grows into seven forms): SONGMUSAI (SIGNAL) and LANGMUSAI (EMERGENT),
drawn the way T-553's round two drew the other five -- a natural creature body under MUSAI's round helmet head and dark
visor, the form's nature drawn as anatomy (no season's vehicle: the four are taken, so the season will show only in
the coat, as MUSAI's own does). Reference: MUSAI's ROM front at 8x, for the head. Three seeds each. Nothing writes
into the game."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t452/scripts")
import armc
OUT = D + "/concepts"; os.makedirs(OUT, exist_ok=True)
GREY = "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
HEAD = ("keep exactly the same big round smooth helmet-like head as the creature in the image, with the same dark glossy visor "
        "across its face and two small glowing eyes showing through it and the same two little antennae, "
        "but below the head a natural furry animal body, soft fur, paws, a tail, ")
FORMS = {
 "songmusai": "a small fennec fox body sitting up tall, two very large cupped ears open like the bells of two horns, its long "
              "fluffy tail curled in the shape of a treble clef, its chest lifted as if singing, two tiny musical notes floating beside it",
 "langmusai": "a small long-tailed lizard-like body with soft scales and a little fur ruff, two small folded dragon wings, a frill "
              "round its neck shaped like a rounded speech balloon, faint rows of tiny marks like lines of writing along its back and tail",
}
for n, body in FORMS.items():
    for seed in (7901, 7902, 7903):
        o = "%s/%s_%d" % (OUT, n, seed); print("drawing", o, flush=True)
        armc.draw(o, armc.PFX + HEAD + body + ", " + GREY + "facing left three-quarter view, " +
                  armc.TAIL.split("full body, ", 1)[1].replace(GREY, ""), seed, refs=[armc.rom_ref("musai")])
print("ALLDONE", flush=True)

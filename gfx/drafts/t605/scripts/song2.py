"""T-605 SONGMUSAI, round two: the first round's fennec ears replaced MUSAI's helmet head (all three seeds), so the head
is kept explicitly -- no animal ears, the two antennae end in small horn bells -- and the song is in the body: a long
fluffy tail curled like a treble clef, chest lifted, singing. Three seeds. Nothing writes into the game."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t452/scripts")
import armc
OUT = D + "/concepts"
GREY = "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
BODY = ("keep exactly the same big round smooth helmet-like head as the creature in the image, no animal ears, with the same dark "
        "glossy visor across its face and two small glowing eyes showing through it, and the same two little antennae on top, "
        "each antenna ending in a tiny flared horn bell like a trumpet's, below the head a small natural furry fox-kit body sitting "
        "up tall with its chest lifted as if singing, soft fur, paws, a long fluffy tail curled into the shape of a treble clef, "
        "two tiny musical notes floating beside it")
for seed in (7911, 7912, 7913):
    o = "%s/songmusai_%d" % (OUT, seed); print("drawing", o, flush=True)
    armc.draw(o, armc.PFX + BODY + ", " + GREY + "facing left three-quarter view, " +
              armc.TAIL.split("full body, ", 1)[1].replace(GREY, ""), seed, refs=[armc.rom_ref("musai")])
print("ALLDONE", flush=True)

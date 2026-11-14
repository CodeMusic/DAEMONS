"""T-552 (the ROVER line's flow) and T-553 (the MUSAI branch, creature first): first concepts, 2026-11-14.
Arm C's settings (klein4b + the pixel-art LoRA, 512). Two seeds each. Nothing writes into the game."""
import os, sys
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts")
import armc
OUT = R + "/gfx/drafts/t552_t553/concepts"; os.makedirs(OUT, exist_ok=True)
PFX = armc.PFX
TAIL = armc.TAIL.replace("mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, ", "")
GREY = "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
ROVER = {
 "rovercub": GREY + "a tiny toy robot puppy, the most mechanical: a big boxy square screen head with two round speaker discs for ears and a short antenna, a cute face shown on the screen, a small boxy body on four short stubby block legs, bolts and panel seams, facing left three-quarter view",
 "roverseer": GREY + "a robot dog SITTING down on a heavy box-shaped server chassis like a computer rack, vent slits on its flank, two thick cables running from its body to the ground, its head halfway to a real dog's head with soft floppy ears starting to form, one glowing lens eye light, it cannot walk, planted and heavy, facing left three-quarter view",
 "roverbyte": "a real fluffy WHITE-furred puppy dog, soft white fur with pale grey shading, floppy ears, black nose, bright eyes, standing alert and happy, one small tuft of fur sticking straight up on its head like a little antenna, a small round tag on its collar glowing faintly blue, facing left three-quarter view",
}
COMMON = ("a small natural fox-kit creature with big ears and a fluffy tail, soft fur, a few faint seam-like lines in its fur like panel lines on a machine, "
          "its ear tips end in tiny rounded nubs like antennae, ")
MUSAI = {
 "musai_summer": COMMON + GREY + "plain and simple, the base form, curious, sitting, facing left three-quarter view",
 "codemusai_summer": COMMON + GREY + "sleek and angular, a dark band of fur across its eyes like a visor, four small round spots in a row on its chest, two bright, one dark, one bright, red tips on its ears, alert and precise, standing, facing left three-quarter view",
 "maskmusai_winter": COMMON + GREY + "an arctic fox kit in thick winter fur, a dark mask marking across its face, very long flat narrow hind feet shaped like skis, a smooth curved brow like a windscreen, frost on its fur, crouched low and fast, facing left three-quarter view",
 "lensmusai_spring": COMMON + GREY + "a sugar glider like fox kit with thin gliding membranes stretched between its legs like small aeroplane wings, huge round lens-like eyes, a tail ending in a little propeller-shaped tuft of fur, gliding, a small sprout on its head, facing left three-quarter view",
 "caremusai_summer": COMMON + GREY + "an otter like fox kit, round and soft, broad webbed feet like little floats, two plump rounded hips like twin pontoons, wet glossy fur, a calm warm face, floating and sitting, facing left three-quarter view",
 "seekmusai_autumn": COMMON + GREY + "a sturdy badger like fox kit, low and broad shouldered, big knobbly paws like rugged tyres, stripes along its back and ribs like a roll cage, a few autumn leaves caught in its fur, ready to run over rough ground, facing left three-quarter view",
}
which = sys.argv[1:] or ["rover", "musai"]
for group, d in (("rover", ROVER), ("musai", MUSAI)):
    if group not in which: continue
    for n, subj in d.items():
        for seed in (7201, 7202):
            o = "%s/%s_%d" % (OUT, n, seed); print("drawing", o, flush=True)
            armc.draw(o, PFX + subj + ", " + TAIL, seed)

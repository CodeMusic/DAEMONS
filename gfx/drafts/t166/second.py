#!/usr/bin/env python3
"""T-166 second pass (2026-09-19): the 46 backs the first pass could not fix, described from their APPROVED fronts --
what is actually drawn -- rather than from each batch's first prompt, which had drifted (COLDREAD was a woman, ENSEMBLE a
palm tree). Two kinds of back: REAR, the creature seen from directly behind; and THREE-QUARTER, turned away and to the
left, for fish, seahorses and serpents, which the model will not draw from dead behind and which the source games gave
a three-quarter back too. Round, featureless daemons are asked for a plain round back. Three seeds each."""
import subprocess, sys
G = ("full body, greyscale, dark grey body with mid grey highlights and black shading, clean black outline, isolated "
     "on plain white, centered, small in the frame with empty space all around, no shadow, no text")
N = ("face, eyes, eye, mouth, teeth, beak, nose, looking at viewer, looking back over shoulder, front view, human, person, "
     "white body, pale body, colorful, grey background, colored background, floor, ground, grass, water, frame, box, drop "
     "shadow, shadow, text, letters, watermark, scenery, photorealistic, blurry, cropped, border, lines")
R = "rear view, seen from directly behind, facing away from the viewer, the back of its head, no face visible"
Q = "three-quarter rear view, turned away from the viewer and to the left, seen mostly from behind, no face visible"
BACKS = {
 "apathy":     (R, "small chubby salamander creature crouching, spotted skin, frilly gills on its head", "its spotted back and short tail"),
 "blindspot":  (Q, "long plain serpent lying low", "its long plain back curving away"),
 "bristle":    (R, "round spiky pufferfish", "a plain round spiky back and a small tail fin"),
 "broadcast":  (R, "large crested bird with wings spread wide", "the spread wings and fanned tail from behind"),
 "chiller":    (R, "plump seal sitting up", "its smooth rounded back and flippers"),
 "coldread":   (R, "round snowy owl with a crest of feathers", "its folded wings and tail feathers from behind"),
 "cryogen":    (R, "sleek seal sitting up with a small horn", "its smooth back, the horn above, tail flippers"),
 "emergence":  (Q, "slender serpent dragon with a small horn, coiled upright", "its long smooth coils turned away"),
 "ensemble":   (R, "stocky creature with a crown of leaves and several round heads", "the backs of its round heads under the leaves"),
 "escalate":   (Q, "large coiled sea serpent with a crest of fins", "its crest fins down its back, coils turned away"),
 "ferry":      (R, "large sea turtle with a domed shell", "its domed shell from behind and the back flippers"),
 "fixation":   (R, "lean hound standing, pointed ears, thin tail", "its lean back, pointed ears and thin tail"),
 "fossilnet":  (R, "winged reptile with bony wings and a long tail", "its bony wings spread from behind, the long tail"),
 "grasp":      (R, "small monkey standing, a long tail ending in a hand", "its furry back and the long tail raised"),
 "grievance":  (Q, "huge armoured reptile with spiked plates down its back", "its spiked back plates and heavy tail"),
 "handler":    (R, "upright duck standing on two feet", "its rounded back, folded wings and tail feathers"),
 "hauntproc":  (R, "round dark ghost creature with short arms", "a plain round back"),
 "hotpath":    (Q, "galloping horse with a flowing mane", "its flowing mane and tail streaming, hindquarters"),
 "illusion":   (R, "deer with large branching antlers", "the antlers from behind, its rump and short tail"),
 "imitation":  (R, "small dog creature holding a paintbrush, a cap on its head", "its back, the cap, a tail"),
 "inference":  (R, "upright fox holding a spoon", "its back, pointed ears and bushy tail"),
 "jetstream":  (Q, "spiny seahorse with a curled tail", "its spiny back fins and curled tail turned away"),
 "nozzle":     (Q, "seahorse with a tube snout and a curled tail", "its back fin and curled tail turned away"),
 "omen":       (R, "crow with a wide brimmed hat-shaped crest", "its folded wings and the hat crest from behind"),
 "overdrive":  (Q, "galloping unicorn horse with a long mane", "its mane and tail streaming, hindquarters"),
 "ping":       (R, "small bird with spread wings", "its back and spread wings from behind"),
 "pipeline":   (R, "four-legged horned beast with a spiked back", "its spiked back, the horns above, a thick tail"),
 "ramrod":     (R, "stocky armoured rhino", "its plated back and rump from behind"),
 "repay":      (R, "round plump bird", "its round back and folded wings"),
 "resentment": (R, "round blob creature on two stubby feet", "a plain round back"),
 "revenant":   (R, "ghost with floating hands", "a plain back of the sheet-like ghost, hands at its sides"),
 "seedling":   (Q, "small slender sea serpent with fin ears", "its smooth coiled body turned away"),
 "sentinel":   (R, "round metal orb with a magnet on each side", "a plain round metal back with bolts, no eye"),
 "simmer":     (R, "small molten slug", "its lumpy dripping back"),
 "singular":   (R, "dragon with bat wings and a long tail", "its wings spread from behind and the tail"),
 "smogstack":  (R, "round gas ball with vents", "a plain round back with vents"),
 "spawn":      (Q, "fish with long flowing fins", "its dorsal fin and flowing tail turned away"),
 "starr":      (R, "tall stag with large branching antlers", "the antlers from behind, its rump and tail"),
 "stub":       (Q, "plain flat fish", "its dorsal fin and tail turned away"),
 "turbulence": (Q, "seahorse dragon with curled fins", "its curled back fins and spiral tail turned away"),
 "upstream":   (Q, "large spined fish", "its spined dorsal fin and tail turned away"),
 "vigilance":  (R, "round owl-like bird with small wings", "its round back and small folded wings"),
 "whim":       (R, "round puffball under a big leaf", "the big leaf from behind over its round back"),
 "wildfire":   (R, "fox with a big bushy tail", "its back and the big bushy tail"),
 "wisp":       (R, "round ghost blob", "a plain round back"),
 "axiomkick":  (R, "round-bodied creature with claw-like arms", "its plain round back and arms"),
}
only = sys.argv[1:]
for name, (view, body, back) in BACKS.items():
    if only and name not in only:
        continue
    for seed in (1917, 42, 88):
        subprocess.run(["python3", "tools/spriteforge.py", "t2i", "--size", "512x512", "--seed", str(seed),
                        "--out", "gfx/drafts/t166/alt2/%s_back_%d" % (name, seed),
                        "--prompt", "pure white background, pixel art game sprite of a single %s, %s, %s, %s" % (body, view, back, G),
                        "--negative", N])

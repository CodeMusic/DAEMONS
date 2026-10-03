#!/usr/bin/env python3
"""T-210 batch 5, the backs (2026-10-02). The first pass (run.sh) drew most backs as front views and many in colour, so
every back is redrawn here with T-166's settled rear-view recipe: a dark grey body, a hard face-and-colour negative,
three seeds. Where none of the three turns away, fourth.py's way is the fallback: the front mirrored (side-on daemons),
or mirrored with its face removed (face-on ones)."""
import subprocess, sys, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))
G = ("full body, greyscale, dark grey body with mid grey highlights and black shading, clean black outline, isolated "
     "on plain white, centered, small in the frame with empty space all around, no shadow, no text")
N = ("face, eyes, eye, mouth, beak, nose, looking at viewer, looking back over shoulder, front view, side view, profile, "
     "human, person, white body, pale body, colorful, grey background, colored background, floor, ground, grass, frame, "
     "box, drop shadow, shadow, text, letters, watermark, scenery, photorealistic, blurry, cropped, border, lines")
BODY = {
 "smudge": "small hyena pup with sooty fur",
 "eclipse": "large hyena with a jet black coat",
 "detour": "small raccoon cub with zigzag stripes",
 "unbranched": "long low sleek raccoon with straight stripes",
 "warmup": "tiny baby squirrel hanging from a twig",
 "shaping": "squirrel holding an acorn",
 "policy": "large squirrel with a huge fanned tail",
 "shortjump": "small barn swallow",
 "longjump": "barn swallow with a long forked tail in flight",
 "sparring": "young kangaroo joey wearing small boxing gloves",
 "checkmate": "tall muscular kangaroo with boxing gloves",
 "lowbit": "tiny rabbit with long folded ears",
 "shiftleft": "rabbit with big flared ears",
 "wraparound": "large hare with huge loudspeaker-shaped ears",
 "loopback": "kitten curled in a circle",
 "quine": "elegant long-haired cat sitting upright",
 "laced": "orchid mantis that looks like a pink flower",
 "syn": "small firefly beetle with a glowing tail",
 "ack": "small round firefly beetle with a glowing tail",
}
only = sys.argv[1:]
for name, body in BODY.items():
    if only and name not in only:
        continue
    for seed in (1917, 42, 88):
        out = "gfx/drafts/t210b5/back2/%s_back_%d" % (name, seed)
        if os.path.exists(out + ".png"):
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["python3", "tools/spriteforge.py", "t2i", "--size", "512x512", "--seed", str(seed), "--out", out,
                        "--prompt", "pure white background, pixel art game sprite of a single real animal, a %s, rear view, seen from "
                        "directly behind, facing away from the viewer, the back of its head, no face visible, %s" % (body, G),
                        "--negative", N])

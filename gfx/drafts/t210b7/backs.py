#!/usr/bin/env python3
"""T-210 batch 7, the backs (2026-10-02). The first pass (run.sh) drew most backs as front views and many in colour, so
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
 "pontus": "colossal ancient deep-sea whale",
 "gaia": "vast ancient tortoise with a mountain on its back",
 "ouranos": "long sky eel with feathered fins",
 "boreas": "white wolf with a streaming frosty mane",
 "brontes": "great tiger with lightning stripes",
 "typhon": "great lion with a mane of embers",
 "talos": "bronze guardian bull made of riveted plates",
 "deucalion": "ram made of stacked stones",
 "khione": "stag carved from clear ice",
 "castor": "sleek dark blue swan with swept wings",
 "polydeuces": "sleek pale red and white swan with swept wings",
 "kairos": "tiny hummingbird with blurred wings",
 "elpis": "small white moth with star-shaped wings on a jar",
}
only = sys.argv[1:]
for name, body in BODY.items():
    if only and name not in only:
        continue
    for seed in (1917, 42, 88):
        out = "gfx/drafts/t210b7/back2/%s_back_%d" % (name, seed)
        if os.path.exists(out + ".png"):
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["python3", "tools/spriteforge.py", "t2i", "--size", "512x512", "--seed", str(seed), "--out", out,
                        "--prompt", "pure white background, pixel art game sprite of a single legendary mythic creature based on a real animal, a %s, rear view, seen from "
                        "directly behind, facing away from the viewer, the back of its head, no face visible, %s" % (body, G),
                        "--negative", N])

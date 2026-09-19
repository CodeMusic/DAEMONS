#!/usr/bin/env python3
"""T-166: every redrawn daemon's back view checked, and the front-like ones redrawn (2026-09-19).

The audit (audit_*.png, similarity.txt) put all 169 fronts beside their backs; by eye, 67 backs show a face or are the
front's side view again. Each is redrawn here from its batch's own description (redo.json), BACK ONLY, with the rear
wording batches 7-15 settled on and a face-and-eyes negative, dark and small in the frame so the fill cannot take a
pale body, three seeds each. Symmetric daemons (CLUSTER, LOCUS, BEACON, PULSAR, the jellyfish, dragonflies and crabs)
look the same from behind and are not on the list. Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008."""
import json, subprocess, sys
G = ("full body, greyscale, dark grey body with mid grey highlights and black shading, clean black outline, isolated "
     "on plain white, centered, small in the frame with empty space all around, no shadow, no text")
N = ("face, eyes, eye, mouth, beak, nose, looking at viewer, looking back over shoulder, front view, side view, profile, "
     "human, person, white body, pale body, colorful, grey background, colored background, floor, ground, grass, frame, "
     "box, drop shadow, shadow, text, letters, watermark, scenery, photorealistic, blurry, cropped, border, lines")
redo = json.load(open("gfx/drafts/t166/redo.json"))
only = sys.argv[1:]
for name, d in redo.items():
    if only and name not in only:
        continue
    back = (", " + d["back"]) if d["back"] else ""
    for seed in (1917, 42, 88):
        subprocess.run(["python3", "tools/spriteforge.py", "t2i", "--size", "512x512", "--seed", str(seed),
                        "--out", "gfx/drafts/t166/alt/%s_back_%d" % (name, seed),
                        "--prompt", "pure white background, pixel art game sprite of a single %s, rear view, seen from "
                        "directly behind, facing away from the viewer, the back of its head, no face visible%s, %s" % (d["body"], back, G),
                        "--negative", N])

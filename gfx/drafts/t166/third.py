#!/usr/bin/env python3
"""T-166 third pass (2026-09-19): the 26 backs text could not turn. Each is drawn FROM ITS OWN APPROVED FRONT -- the
built 64px front, mirrored, scaled x8 onto the chroma-green key batch 1 used -- and redrawn image-to-image with a
rear-view prompt at three strengths (0.45, 0.55, 0.65). Low keeps the body as drawn; higher lets the head turn."""
import subprocess, sys
from PIL import Image
sys.path.insert(0, "gfx/drafts/t166")
BODY = {n: b for n, (_, b, _) in __import__("second").BACKS.items()} if False else None
import re
src = open("gfx/drafts/t166/second.py").read()
BODY = dict(re.findall(r'^ "(\w+)":\s*\([RQ], "([^"]+)"', src, re.M))
LEFT = ["coldread", "vigilance", "nozzle", "jetstream", "turbulence", "bristle", "stub", "upstream", "illusion", "starr",
        "hotpath", "overdrive", "apathy", "broadcast", "cryogen", "emergence", "escalate", "fixation", "grasp", "handler",
        "imitation", "omen", "repay", "simmer", "singular", "axiomkick"]
P = ("pixel art game sprite, full body, rear view, seen from directly behind, back of the head, no face visible, "
     "greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, flat solid "
     "green background, centered, no shadow, no text")
N = ("face, eyes, eye, mouth, beak, looking at viewer, front view, green body, green tint, pale body, drop shadow, shadow, "
     "colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, border")
only = sys.argv[1:]
for n in LEFT:
    if only and n not in only:
        continue
    f = Image.open("gfx/daemons/%s_front.png" % n).convert("RGBA").resize((64, 64), Image.NEAREST).transpose(Image.FLIP_LEFT_RIGHT)
    bg = Image.new("RGBA", (64, 64), (0, 200, 0, 255)); bg.alpha_composite(f)
    bg.convert("RGB").resize((512, 512), Image.NEAREST).save("gfx/drafts/t166/src3/%s.png" % n)
    for dn in ("0.45", "0.55", "0.65"):
        subprocess.run(["python3", "tools/spriteforge.py", "i2i", "--out", "gfx/drafts/t166/alt3/%s_back_%s" % (n, dn[2:]),
                        "--image", "gfx/drafts/t166/src3/%s.png" % n, "--denoise", dn, "--seed", "1917",
                        "--prompt", "a single %s, %s" % (BODY[n], P), "--negative", N])

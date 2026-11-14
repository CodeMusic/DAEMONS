"""T-552/T-553 (the user, 2026-11-14: "Yes, draw them"): a back and an icon for each of the 27 picked fronts, each drawn by
reference to its picked 512 front (arm C's back and icon prompts). One seed each, 7701 backs and 7741 icons; a failure is
redrawn on its own. Nothing writes into the game."""
import os, sys
R = "/Users/christopherhicks/Projects/DAEMONS"; D = R + "/gfx/drafts/t552_t553/"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts"); sys.path.insert(0, D + "scripts")
import json, armc
P = json.load(open(D + "reduced/picks.json"))
OUT = D + "backs_icons"; os.makedirs(OUT, exist_ok=True)
GREY = "the same grey body and colours"
KEEP = {"rover": "", "musai": "the same round helmet head seen from behind, the same antennae, the same fur, the same tail"}
for key, r in P.items():
    keep = KEEP["rover" if key.startswith("rover") else "musai"]
    if key == "rovercub": keep = "the same boxy square screen head seen from behind, the same speaker discs and antenna, the same block legs"
    if key == "roverseer": keep = "the same server chassis haunches with vents and cables, the same robot dog head from behind"
    if key == "roverbyte": keep = "the same white fluffy fur, the same floppy ears and the tuft on its head, the same tail"
    src = D + r["source"] + ".png"
    back = ("pixel art sprite, chibi, Turn this exact creature around: the same creature seen from directly behind, rear view, facing "
            "away from the viewer, the back of its head, no face visible, %s, the same size in the frame, the same proportions, "
            "%s, the same pixel art style, black outline, centered on a plain white background, full body, no shadow, game asset" % (keep, GREY))
    icon = ("pixel art sprite, chibi, the same creature as in the image drawn as a tiny party menu icon: a head and shoulders bust, "
            "its big head filling the picture, bold simple shapes, strong contrast between light, mid and dark grey, only small touches "
            "of colour, a thick black outline, facing the viewer, pure white background, centered, no text, game asset")
    for kind, prompt, seed in (("back", back, 7701), ("icon", icon, 7741)):
        o = "%s/%s_%s_%d" % (OUT, key, kind, seed); print("drawing", o, flush=True)
        armc.draw(o, prompt, seed, refs=[src])
# free the sprite server when the batch ends (the companion lane, 2026-11-14: FLUX stays loaded ~22 GB beside ACE-Step's 23 GB)
import urllib.request
urllib.request.urlopen(urllib.request.Request("http://roverbyteseer:8008/free", data=b'{"unload_models": true, "free_memory": true}',
                                              headers={"Content-Type": "application/json"}), timeout=30)
print("ALLDONE", flush=True)

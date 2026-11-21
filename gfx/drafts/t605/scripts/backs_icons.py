"""T-605: a back and an icon for each picked front, drawn by reference to its 512 front (T-552/T-553's backs_icons.py,
the same prompts). Seeds 7951 backs, 7961 icons. PICKS below names the picked concept. Nothing writes into the game."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t452/scripts")
import armc
P = json.load(open(D + "/picks.json"))
OUT = D + "/backs_icons"; os.makedirs(OUT, exist_ok=True)
KEEP = "the same round helmet head seen from behind, the same antennae, the same fur, the same tail"
for key, src in P.items():
    src = D + "/" + src + ".png"
    back = ("pixel art sprite, chibi, Turn this exact creature around: the same creature seen from directly behind, rear view, facing "
            "away from the viewer, the back of its head, no face visible, %s, the same size in the frame, the same proportions, "
            "the same grey body and colours, the same pixel art style, black outline, centered on a plain white background, full body, "
            "no shadow, game asset" % KEEP)
    icon = ("pixel art sprite, chibi, the same creature as in the image drawn as a tiny party menu icon: a head and shoulders bust, "
            "its big head filling the picture, bold simple shapes, strong contrast between light, mid and dark grey, only small touches "
            "of colour, a thick black outline, facing the viewer, pure white background, centered, no text, game asset")
    for kind, prompt, seed in (("back", back, 7951), ("icon", icon, 7961)):
        o = "%s/%s_%s_%d" % (OUT, key, kind, seed); print("drawing", o, flush=True)
        armc.draw(o, prompt, seed, refs=[src])
print("ALLDONE", flush=True)

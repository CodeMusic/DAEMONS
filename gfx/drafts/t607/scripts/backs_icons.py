"""T-607: a back and an icon for each picked seasonal front, drawn by reference to its 512 front (T-605's backs_icons.py,
T-552/T-553's prompts). Seeds 8201 backs, 8211 icons. Nothing writes into the game."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t452/scripts")
import armc
P = {k: v for k, v in json.load(open(D + "/picks.json")).items() if not k.startswith("_")}
OUT = D + "/backs_icons"; os.makedirs(OUT, exist_ok=True)
KEEP = "the same round helmet head seen from behind, the same antennae, the same fur, the same tail, the same seasonal coat"
for key, src in P.items():
    src = D + "/" + src + ".png"
    back = ("pixel art sprite, chibi, Turn this exact creature around: the same creature seen from directly behind, rear view, facing "
            "away from the viewer, the back of its head, no face visible, %s, the same size in the frame, the same proportions, "
            "the same grey body and colours, the same pixel art style, black outline, centered on a plain white background, full body, "
            "no shadow, game asset" % KEEP)
    icon = ("pixel art sprite, chibi, the same creature as in the image drawn as a tiny party menu icon: a head and shoulders bust, "
            "its big head filling the picture, bold simple shapes, strong contrast between light, mid and dark grey, only small touches "
            "of colour, a thick black outline, facing the viewer, pure white background, centered, no text, game asset")
    for kind, prompt, seed in (("back", back, 8201), ("icon", icon, 8211)):
        o = "%s/%s_%s_%d" % (OUT, key, kind, seed); print("drawing", o, flush=True)
        armc.draw(o, prompt, seed, refs=[src])
print("ALLDONE", flush=True)

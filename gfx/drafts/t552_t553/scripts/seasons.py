"""T-553 seasons (the user, 2026-11-14: "Fix MASKMUSAI, then seasons"): each form's other three seasons, drawn by reference
to its round-two body (MASKMUSAI's from round three, the snowshoe hare 7402). The home season is the fullest; elsewhere the
season shows in the coat and a lighter allusion. CODEMUSAI, the dialect, carries every season's vehicle (as its T-534 followers
do). MUSAI's seasons stay in its coat and antennae (T-532). Two seeds each. Nothing writes into the game."""
import os, sys
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts")
import armc
D = R + "/gfx/drafts/t552_t553/"; OUT = D + "seasons"; os.makedirs(OUT, exist_ok=True)
GREY = "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
BASE = {"musai": "round2/musai_summer_7301", "codemusai": "round2/codemusai_summer_7302", "lensmusai": "round2/lensmusai_spring_7301",
        "caremusai": "round2/caremusai_summer_7302", "seekmusai": "round2/seekmusai_autumn_7301", "maskmusai": "round3/maskmusai_winter_7402"}
HOME = {"musai": "summer", "codemusai": "summer", "lensmusai": "spring", "caremusai": "summer", "seekmusai": "autumn", "maskmusai": "winter"}
COAT = {"winter": "in thick fluffy white-grey winter fur, a few frost sparkles",
        "spring": "in light sleek spring fur, a small green sprout growing on its head, a few tiny blossoms",
        "summer": "in short glossy summer fur, a few water droplets",
        "autumn": "in warm thick autumn fur, a few orange leaves caught in it"}
FULL = {"winter": "its two hind feet very long, flat and narrow like a snowshoe hare's, stretched out behind it, crouched low and fast",
        "spring": "wide gliding membranes of fur between its front and back legs spread like a model aeroplane's wings, a propeller-shaped tuft on its tail",
        "summer": "two big plump rounded webbed hind feet side by side like twin floats, a flat broad back like a deck, floating",
        "autumn": "four big chunky round paws with deep treads like off-road tyres, dark stripes arching over its back like a roll cage"}
LIGHT = {"winter": "its hind feet a little longer and flatter than usual",
         "spring": "small folds of gliding skin along its sides",
         "summer": "slightly webbed paws",
         "autumn": "its paws a little chunkier with faint treads, a faint stripe over its shoulders"}
def prompt(n, s):
    if n == "musai": part = "nothing else changed, the season only in its coat"
    elif n == "codemusai": part = FULL[s]
    else: part = LIGHT[s]
    return ("pixel art sprite, chibi, the same creature as in the image, the same round helmet head, the same dark visor with glowing eyes, "
            "the same antennae, the same body shape and markings, now " + COAT[s] + ", " + part + ", " + GREY +
            "facing left three-quarter view, black outline, centered on a plain white background, full body, the whole body inside the "
            "picture with white space on every side, no shadow, no text, game asset")
for n, b in BASE.items():
    for s in ("winter", "spring", "summer", "autumn"):
        if s == HOME[n]: continue
        for seed in (7501, 7502):
            o = "%s/%s_%s_%d" % (OUT, n, s, seed); print("drawing", o, flush=True)
            armc.draw(o, prompt(n, s), seed, refs=[D + b + ".png"])
print("ALLDONE", flush=True)

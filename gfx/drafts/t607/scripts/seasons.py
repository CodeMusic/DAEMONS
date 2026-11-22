"""T-607: SONGMUSAI's and LANGMUSAI's winter, spring and autumn, drawn the way T-553 drew MUSAI's (gfx/drafts/t552_t553/
scripts/seasons.py): by reference to the picked T-605 front at 512 (gfx/drafts/t605/picks.json), the same creature, the
season only in its coat -- no vehicle (T-605: the four are taken, so the season shows in the coat, as MUSAI's own does).
Summer is the species' own T-605 picture. Two seeds each, 8001 and 8002. Nothing writes into the game."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts")
import armc
T605 = os.path.join(os.path.dirname(D), "t605")
PICKS = json.load(open(T605 + "/picks.json"))
OUT = D + "/seasons"; os.makedirs(OUT, exist_ok=True)
GREY = "mostly greyscale, medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
#  T-553's COAT, said of each form's own covering: SONGMUSAI is a furry fox kit, LANGMUSAI a scaled lizard with a fur ruff
COAT = {
 "songmusai": {"winter": "in thick fluffy white-grey winter fur, a few frost sparkles",
               "spring": "in light sleek spring fur, a small green sprout growing on its head, a few tiny blossoms",
               "autumn": "in warm thick autumn fur, a few orange leaves caught in it"},
 "langmusai": {"winter": "its fur ruff grown thick and fluffy white-grey for winter, frost on its scales, a few frost sparkles",
               "spring": "its scales fresh and smooth for spring, a small green sprout growing on its head, a few tiny blossoms",
               "autumn": "its fur ruff thick and warm for autumn, a few orange leaves caught in it"},
}
KEEP = {
 "songmusai": "the same two little antennae each ending in a tiny horn bell, the same fox-kit body sitting up, the same long tail "
              "curled like a treble clef",
 "langmusai": "the same two little antennae, the same small lizard body, the same small folded wings, the same rounded frill "
              "round its neck, the same rows of tiny marks like writing along its back and tail",
}
def prompt(n, s):
    return ("pixel art sprite, chibi, the same creature as in the image, the same round helmet head, the same dark visor with "
            "glowing eyes, " + KEEP[n] + ", the same body shape and markings, now " + COAT[n][s] + ", nothing else changed, the "
            "season only in its coat, " + GREY + "facing left three-quarter view, black outline, centered on a plain white "
            "background, full body, the whole body inside the picture with white space on every side, no shadow, no text, game asset")
if __name__ == "__main__":
    for n, src in PICKS.items():
        for s in ("winter", "spring", "autumn"):
            for seed in (8001, 8002):
                o = "%s/%s_%s_%d" % (OUT, n, s, seed); print("drawing", o, flush=True)
                armc.draw(o, prompt(n, s), seed, refs=[T605 + "/" + src + ".png"])
    print("ALLDONE", flush=True)

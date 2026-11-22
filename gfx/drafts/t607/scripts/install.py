"""T-607: file the picked seasonal drawings where tools/genmusaiseasons.py reads them (T-552/T-553's install.py):
picked/<name>_<season>_{front,back,icon}.png -> gfx/drafts/t532_musai_seasons/finals/. Their followers are gbafollower's
REDUCED from the front, as T-605's summers' are. genmusaiseasons builds them only while APPROVED_FINAL names them."""
import json, os, shutil
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
F = os.path.join(os.path.dirname(os.path.dirname(D)), "t532_musai_seasons", "finals") + "/"
for key in json.load(open(D + "picks.json")):
    if key.startswith("_"): continue
    for kind in ("front", "back", "icon"):
        shutil.copy(D + "picked/%s_%s.png" % (key, kind), F + "%s_%s.png" % (key, kind))
    print("filed", key)

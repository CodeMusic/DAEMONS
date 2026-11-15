"""T-552/T-553: file the approved art where the build reads it (the user, 2026-11-14: "Redraw weak, then build").
  MUSAI branch, 24 forms -> gfx/drafts/t532_musai_seasons/finals/<name>_<season>_{front,back,icon}.png (fronts and backs
     from finals/ here, export_check.py's round-tripped RGBA) and followers/<name>_<season>_follower.png
  ROVER line -> gfx/daemons/<name>_{front,back,icon}.png (the clean drawings, which place_rich turns into the approved
     pictures exactly; the follower is then gbafollower's REDUCED, from that front)
ROVERSEER's and ROVERBYTE's icons are now icon3's reduction of their own fronts (redraw_weak/): the drawn busts lost the
rack haunches and the white fur."""
import json, shutil
R = "/Users/christopherhicks/Projects/DAEMONS"; D = R + "/gfx/drafts/t552_t553/"
F = R + "/gfx/drafts/t532_musai_seasons/"
P = json.load(open(D + "reduced/picks.json"))
for key in P:
    if key.startswith("rover"):
        shutil.copy(D + "reduced/work/%s_clean.png" % key, R + "/gfx/daemons/%s_front.png" % key)
        shutil.copy(D + "reduced/work/%s_back_clean.png" % key, R + "/gfx/daemons/%s_back.png" % key)
        shutil.copy(D + "reduced/%s_icon.png" % key, R + "/gfx/daemons/%s_icon.png" % key)
    else:
        for kind in ("front", "back"):
            shutil.copy(D + "finals/%s_%s.png" % (key, kind), F + "finals/%s_%s.png" % (key, kind))
        shutil.copy(D + "reduced/%s_icon.png" % key, F + "finals/%s_icon.png" % key)
        shutil.copy(D + "followers/%s_follower.png" % key, F + "followers/%s_follower.png" % key)
    print("filed", key)

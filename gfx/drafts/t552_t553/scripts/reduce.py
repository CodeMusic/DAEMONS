"""T-552/T-553 (the user, 2026-11-14: "Yes, reduce my picks"): the picked fronts through arm C's reduction -- the ground keyed
(green, or blue for spring: its sprout is green), cleandraft, the type-hue fold, place_rich to 64x64 / 16 colours on the
daemon's TYPE ramp. Writes reduced/<name>.png and .pal. Fronts only; backs, icons and followers wait. Nothing in the game."""
import json, os, sys
R = "/Users/christopherhicks/Projects/DAEMONS"; D = R + "/gfx/drafts/t552_t553/"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts"); sys.path.insert(0, R + "/gfx/drafts/t532_musai_seasons/finals/redraw/scripts")
import armc, gbs
from keyed import keyed
PICKS = {
 "musai":     {"winter": "seasons/musai_winter_7501", "spring": "seasons/musai_spring_7502", "summer": "round2/musai_summer_7301", "autumn": "autumn2/musai_autumn_7601"},
 "codemusai": {"winter": "seasons/codemusai_winter_7501", "spring": "seasons/codemusai_spring_7501", "summer": "round2/codemusai_summer_7302", "autumn": "autumn2/codemusai_autumn_7601"},
 "seekmusai": {"winter": "seasons/seekmusai_winter_7501", "spring": "seasons/seekmusai_spring_7501", "summer": "seasons/seekmusai_summer_7502", "autumn": "round2/seekmusai_autumn_7301"},
 "caremusai": {"winter": "seasons/caremusai_winter_7501", "spring": "seasons/caremusai_spring_7502", "summer": "round2/caremusai_summer_7302", "autumn": "autumn2/caremusai_autumn_7602"},
 "lensmusai": {"winter": "seasons/lensmusai_winter_7501", "spring": "round2/lensmusai_spring_7301", "summer": "seasons/lensmusai_summer_7501", "autumn": "autumn2/lensmusai_autumn_7601"},
 "maskmusai": {"winter": "round3/maskmusai_winter_7402", "spring": "seasons/maskmusai_spring_7501", "summer": "seasons/maskmusai_summer_7501", "autumn": "autumn2/maskmusai_autumn_7602"},
}
ROVER = {"rovercub": "concepts/rovercub_7202", "roverseer": "round2/roverseer_7302", "roverbyte": "concepts/roverbyte_7201"}
os.makedirs(D + "reduced/work", exist_ok=True)
jobs = [(n, "%s_%s" % (n, s), p, s) for n, d in PICKS.items() for s, p in d.items()] + [(n, n, p, "") for n, p in ROVER.items()]
rec = {}
for n, key, p, s in jobs:
    t = armc.typ(n); src = D + p + ".png"; k = D + "reduced/work/%s_keyed.png" % key; cl = D + "reduced/work/%s_clean.png" % key
    keyed(src, k, key=(0, 0, 220) if s == "spring" else (0, 200, 0))
    ok, err = armc.clean(k, cl)
    if not ok: print(key, "CLEAN FAILED", err); continue
    folded = armc.fold(cl, t)
    grid, pal = gbs.place_rich(cl, gbs.TYPE_COLOR[t])
    gbs.write_png4(D + "reduced/%s.png" % key, grid, pal)
    with open(D + "reduced/%s.pal" % key, "w") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in (list(pal) + [(0, 0, 0)] * 16)[:16]))
    rec[key] = dict(source=p, type=t, folded=folded); print(key, t, "ok", flush=True)
json.dump(rec, open(D + "reduced/picks.json", "w"), indent=1)

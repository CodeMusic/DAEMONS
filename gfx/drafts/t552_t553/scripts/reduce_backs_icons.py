"""T-552/T-553: the backs reduced through their FRONT's palette (one palette a form, arm C's BACKS job), and the icons by icon3
(26 tall, frames 1 and 2 in a 32x64 strip). The ground keyed as in reduce.py. Writes reduced/<key>_back.png, <key>_icon.png."""
import json, os, sys
import numpy as np
from PIL import Image
R = "/Users/christopherhicks/Projects/DAEMONS"; D = R + "/gfx/drafts/t552_t553/"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts"); sys.path.insert(0, R + "/gfx/drafts/t532_musai_seasons/finals/redraw/scripts")
import armc, gbs, icon3
from keyed import keyed
P = json.load(open(D + "reduced/picks.json")); W = D + "reduced/work/"
for key, r in P.items():
    n = key.split("_")[0]; t = r["type"]; spring = key.endswith("spring")
    pal = armc.readpal(D + "reduced/%s.pal" % key)
    for kind, seed in (("back", 7701), ("icon", 7741)):
        src = D + "backs_icons/%s_%s_%d.png" % (key, kind, seed); k = W + "%s_%s_keyed.png" % (key, kind); cl = W + "%s_%s_clean.png" % (key, kind)
        keyed(src, k, key=(0, 0, 220) if spring else (0, 200, 0))
        ok, err = armc.clean(k, cl, streaks=(kind == "back"))
        if not ok: print(key, kind, "CLEAN FAILED", err); continue
        armc.fold(cl, t)
        try:
            if kind == "back":
                grid, p = gbs.place_rich(cl, gbs.TYPE_COLOR[t], shared=pal)
                gbs.write_png4(D + "reduced/%s_back.png" % key, grid, p)
            else:
                icon3.make(n, t, cl, D + "reduced/%s_icon.png" % key)
            print(key, kind, "ok", flush=True)
        except Exception as e:
            print(key, kind, "FAILED", repr(e)[:200], flush=True)

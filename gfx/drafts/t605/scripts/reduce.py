"""T-605: the picked fronts and their backs and icons through T-552/T-553's reduction -- the ground keyed, cleandraft
(armc.clean, the streaks placed), the type-hue fold, place_rich to 64x64 / 16 colours on the TYPE ramp (the back through
the front's palette), the icon by icon3. Writes reduced/ (the pictures, for the sheets) and picked/<name>_{front,back}.png
(the clean RGBA drawings, gbasprite's input, which place_rich turns into the reduced pictures) and picked/<name>_icon.png.
Nothing writes into the game: tools/gbamusaiforms.py --write copies picked/ into gfx/daemons/."""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE) + "/"
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts"); sys.path.insert(0, R + "/gfx/drafts/t532_musai_seasons/finals/redraw/scripts")
import armc, gbs, icon3
from keyed import keyed
TYPE = {"songmusai": "ELECTRIC", "langmusai": "DRAGON"}
P = json.load(open(D + "picks.json"))
W = D + "reduced/work/"; os.makedirs(W, exist_ok=True); os.makedirs(D + "picked", exist_ok=True)
for key, p in P.items():
    t = TYPE[key]
    srcs = {"front": D + p + ".png", "back": D + "backs_icons/%s_back_7951.png" % key, "icon": D + "backs_icons/%s_icon_7961.png" % key}
    pal = None
    for kind in ("front", "back", "icon"):
        if not os.path.exists(srcs[kind]):
            print(key, kind, "not drawn yet"); continue
        k = W + "%s_%s_keyed.png" % (key, kind); cl = W + "%s_%s_clean.png" % (key, kind)
        keyed(srcs[kind], k, key=(0, 200, 0))
        ok, err = armc.clean(k, cl, streaks=(kind != "icon"))
        if not ok: print(key, kind, "CLEAN FAILED", err); continue
        armc.fold(cl, t)
        if kind == "front":
            grid, pal = gbs.place_rich(cl, gbs.TYPE_COLOR[t])
            gbs.write_png4(D + "reduced/%s_front.png" % key, grid, pal)
            shutil.copy(cl, D + "picked/%s_front.png" % key)
        elif kind == "back":
            grid, p2 = gbs.place_rich(cl, gbs.TYPE_COLOR[t], shared=pal)
            gbs.write_png4(D + "reduced/%s_back.png" % key, grid, p2)
            shutil.copy(cl, D + "picked/%s_back.png" % key)
        else:
            icon3.make(key, t, cl, D + "reduced/%s_icon.png" % key)
            shutil.copy(D + "reduced/%s_icon.png" % key, D + "picked/%s_icon.png" % key)
        print(key, kind, "ok", flush=True)

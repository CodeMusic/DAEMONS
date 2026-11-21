"""T-607: the seasonal drafts through T-605's reduction (gfx/drafts/t605/scripts/reduce.py, after T-552/T-553's) -- the
ground keyed (green; blue for spring, whose sprout is green), cleandraft (armc.clean, the streaks placed), the type-hue
fold, place_rich to 64x64 / 16 colours on the TYPE ramp (SIGNAL teal, EMERGENT jade); backs through their front's
palette, icons by icon3.

    reduce.py cand                every drawn front candidate -> reduced/cand/<file>.png (for picking)
    reduce.py picks               picks.json's fronts, and their backs and icons once drawn -> reduced/<key>_{front,back,
                                  icon}.png, and picked/<key>_{front,back,icon}.png: the clean RGBA drawings gbasprite's
                                  place_rich reads (genmusaiseasons copies nothing: it reads finals/, where install.py
                                  files these)
Nothing writes into the game."""
import glob, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE) + "/"
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/gfx/drafts/t452/scripts"); sys.path.insert(0, R + "/gfx/drafts/t532_musai_seasons/finals/redraw/scripts")
import armc, gbs, icon3
from keyed import keyed
TYPE = {"songmusai": "ELECTRIC", "langmusai": "DRAGON"}
W = D + "reduced/work/"; os.makedirs(W, exist_ok=True)


def clean(src, key, kind, spring):
    k = W + "%s_%s_keyed.png" % (key, kind); cl = W + "%s_%s_clean.png" % (key, kind)
    keyed(src, k, key=(0, 0, 220) if spring else (0, 200, 0))
    ok, err = armc.clean(k, cl, streaks=(kind != "icon"))
    if not ok:
        print(key, kind, "CLEAN FAILED", err); return None
    armc.fold(cl, TYPE[key.split("_")[0]])
    return cl


if sys.argv[1:] == ["cand"]:
    os.makedirs(D + "reduced/cand", exist_ok=True)
    for src in sorted(glob.glob(D + "seasons/*.png") + glob.glob(D + "autumn2/*.png") + glob.glob(D + "round2/*.png")):
        b = os.path.basename(src)[:-4]; n = b.split("_")[0]
        cl = clean(src, b, "front", "_spring_" in b)
        if cl:
            grid, pal = gbs.place_rich(cl, gbs.TYPE_COLOR[TYPE[n]])
            gbs.write_png4(D + "reduced/cand/%s.png" % b, grid, pal); print(b, "ok", flush=True)
elif sys.argv[1:] == ["picks"]:
    P = json.load(open(D + "picks.json"))
    os.makedirs(D + "picked", exist_ok=True)
    for key, p in P.items():
        if key.startswith("_"): continue
        t = TYPE[key.split("_")[0]]; spring = key.endswith("spring")
        srcs = {"front": D + p + ".png", "back": D + "backs_icons/%s_back_8201.png" % key, "icon": D + "backs_icons/%s_icon_8211.png" % key}
        pal = None
        for kind in ("front", "back", "icon"):
            if not os.path.exists(srcs[kind]):
                print(key, kind, "not drawn yet"); continue
            cl = clean(srcs[kind], key, kind, spring)
            if not cl: continue
            if kind == "front":
                grid, pal = gbs.place_rich(cl, gbs.TYPE_COLOR[t])
                gbs.write_png4(D + "reduced/%s_front.png" % key, grid, pal)
                shutil.copy(cl, D + "picked/%s_front.png" % key)
            elif kind == "back":
                grid, p2 = gbs.place_rich(cl, gbs.TYPE_COLOR[t], shared=pal)
                gbs.write_png4(D + "reduced/%s_back.png" % key, grid, p2)
                shutil.copy(cl, D + "picked/%s_back.png" % key)
            else:
                icon3.make(key.split("_")[0], t, cl, D + "reduced/%s_icon.png" % key)
                shutil.copy(D + "reduced/%s_icon.png" % key, D + "picked/%s_icon.png" % key)
            print(key, kind, "ok", flush=True)

"""T-532 REDRAW of the weak seasonal forms (2026-11-08; the user: "Build the good ones now; redraw the weak"). DRAFT.

    redraw.py gen fronts|backs|icons [KEY ...]   (KEY = name_season)
    redraw.py reduce
    redraw.py export                              -> ../../finals/<name>_<season>_{front,back,icon,follower}.png

Same pipeline as gfx/drafts/t532_musai_seasons/finals/work/scripts/finals.py (arm C: klein4b + pixel LoRA on
roverbyteseer; cleandraft --streaks; place_rich in the type ramp; icon3; follower by icon3.reduce fit 20x22).

WHAT FAILED, MEASURED: cleandraft's black-shadow wear takes any thick dark mass that touches no light body pixel.
Black tyres, black skis and a black track ARE such masses -- SEEKMUSAI autumn lost 105 px of tyre (the spider legs),
MASKMUSAI winter 84, CODEMUSAI autumn 49. And a near-white windscreen is flooded as paper. So every vehicle part is
asked for in CHARCOAL / MID GREY with a thick black outline and a light highlight (a hub, a top edge), never solid
black and never near-white; the wear count is recorded per draft and penalised in the pick.
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image
R = "/Users/christopherhicks/Projects/DAEMONS"
FD = R + "/gfx/drafts/t532_musai_seasons/finals/work/scripts"
sys.path.insert(0, FD)
import finals as FN          # its DAEMONS, TAIL, draw(), rom_ref(), place rules; its OUT is never written here
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = R + "/gfx/drafts/t532_musai_seasons/finals"
PY = FN.PY
SEEDS = (5325, 5326, 5327, 5328, 5329, 5330)
ISEEDS = (5341, 5342, 5343)

SKI = ("two long thick curved snowmobile skis sticking far out in front in place of its feet, each ski mid grey with a "
       "thick black outline and a light grey top edge, a big chunky ridged track tread under its body, mid grey with a "
       "thick black outline and light grey ridges, and a tall smoke-grey windscreen crest, mid grey with a thick black "
       "outline, rising high over its mask")
TYRE = ("big round chunky knobby tyres, each tyre charcoal grey rubber with a thick black outline and a big round light "
        "silver hubcap in its middle")
BODY = {
    "maskmusai_winter": "its whole lower body IS a little snowmobile: " + SKI + ", snow spraying from the track, frost",
    "maskmusai_spring": SKI + ", mud on the skis and melting snow dripping",
    "maskmusai_summer": SKI.replace("a tall smoke-grey windscreen crest", "a tall windscreen crest tinted smoky like sunglasses")
                        + ", the ski tips lifted",
    "maskmusai_autumn": SKI + ", a few small fallen orange leaves on the skis, the first frost on the windscreen crest",
    "seekmusai_autumn": ("its whole lower body IS a rugged little side-by-side off-road buggy: four " + TYRE + ", as tall as "
                         "half its body, where its legs would be, a thick tubular roll-bar cage, light grey with a black "
                         "outline, arching over its helmet, a front bumper with two round headlights, golden yellow autumn "
                         "leaves caught in its fins"),
    "lensmusai_autumn": ("its whole body IS a little model aeroplane: two long straight rectangular model-aeroplane wings "
                         "spread far out from its sides, wider than its head, light grey balsa wood with a perfectly "
                         "straight leading edge, square wing tips and a thick black outline, a thin diagonal wing strut "
                         "under each wing, a big two-bladed propeller on its chest, a small tail fin behind it, three small "
                         "orange autumn leaves resting on top of the grey wings"),
    "codemusai_winter": ("a snowmobile's parts: two big long thick curved snowmobile skis under its feet sticking far out in "
                         "front, as long as its body is wide, mid grey with a thick black outline and a light grey top "
                         "edge, and a tall smoke-grey windscreen crest, mid grey with a thick black outline, rising from "
                         "its helmet, frost on its antennae, " + FN.GLYPH),
    "codemusai_autumn": ("an off-road buggy's parts: two " + TYRE + ", as tall as half its body, in place of its legs, and a "
                         "big thick tubular roll-bar frame, light grey with a thick black outline, arching high over its "
                         "helmet and wider than its helmet, " + FN.GLYPH),
}
CUE = {
    "maskmusai": "the tall windscreen crest with its black outline and the big thick skis",
    "seekmusai_autumn": "the thick roll-bar cage over its helmet and the big round tyres with light hubcaps",
    "lensmusai_autumn": "the long straight grey wings and the propeller",
    "codemusai_winter": "the windscreen crest and the big thick skis, the glyph lights on its chest",
    "codemusai_autumn": "the big thick roll-bar frame and the round tyres with light hubcaps, the glyph lights on its chest",
}
KEYS = list(BODY)


def split(k): n, s = k.split("_"); return n, s
def cue(k): return CUE.get(k) or CUE[split(k)[0]]


def front_prompt(k):
    n, s = split(k); home = FN.DAEMONS[n][3]
    lead = "its fullest, most complete seasonal form" if home == s else "its %s form" % s
    return ("pixel art sprite, chibi, the same creature as in the images redrawn as %s, the machine built into its body so "
            "it clearly reads, big bold vehicle parts: %s; it is %s, keeping its face and its colours, facing left "
            "three-quarter view, %s" % (lead, BODY[k], FN.DAEMONS[n][4], FN.TAIL))


def back_prompt(k):
    return ("pixel art sprite, chibi, Turn this exact creature around: the same creature seen from directly behind, rear view, "
            "facing away from the viewer, the back of its head, no face visible, still with %s, the same size in the frame, "
            "the same proportions, the same grey body and colours, the same pixel art style, black outline, centered on a "
            "plain white background, full body, no shadow, game asset" % cue(k))


def icon_prompt(k):
    n, s = split(k)
    return ("pixel art sprite, chibi, the same creature as in the image drawn as a tiny party menu icon: its head and upper body, "
            "%s, with %s clearly showing, its big head filling the picture, bold simple shapes, strong contrast between light, "
            "mid and dark grey, only small touches of colour, a thick black outline, facing the viewer, pure white background, "
            "centered, no text, game asset" % (FN.DAEMONS[n][4], cue(k)))


ROMONLY = (5328, 5329, 5330)     # MASKMUSAI: with its old draft as a reference the weak fin and thin skis came back on
                                 # every seed; the ROM front alone drew a real snowmobile (tread, skis, grey crest)
MAGENTA = {"seekmusai_autumn", "lensmusai_autumn", "maskmusai_autumn"}   # yellow/orange leaves lean green: key magenta


def refs(k, seed):
    n = split(k)[0]
    if n == "maskmusai" and seed in ROMONLY: return [FN.rom_ref(n)]
    return [old_front(k), FN.rom_ref(n)]


def old_front(k):
    P = json.load(open(OLD + "/work/picks.json")); return "%s/work/raw/%s_front_%d.png" % (OLD, k, P[k]["seed"])


def KEY(k): return (200, 0, 200) if k in MAGENTA else (0, 200, 0)


def picks(): return json.load(open(OUT + "/picks.json")) if os.path.exists(OUT + "/picks.json") else {}


def gen(stage, keys, seeds):
    os.makedirs(OUT + "/raw", exist_ok=True)
    for k in keys:
        n, s = split(k)
        if stage == "fronts":
            for seed in seeds:
                print("front", k, seed, flush=True)
                FN.draw("%s/raw/%s_front_%d" % (OUT, k, seed), front_prompt(k), seed, refs(k, seed))
        elif stage == "backs":
            for seed in seeds:
                f = "%s/raw/%s_front_%d.png" % (OUT, k, seed)
                if os.path.exists(f):
                    print("back", k, seed, flush=True); FN.draw("%s/raw/%s_back_%d" % (OUT, k, seed), back_prompt(k), seed, [f])
        elif stage == "icons":
            P = picks(); ref = "%s/raw/%s_front_%d.png" % (OUT, k, P[k]["seed"])
            for seed in ISEEDS:
                print("icon", k, seed, flush=True); FN.draw("%s/raw/%s_icon_%d" % (OUT, k, seed), icon_prompt(k), seed, [ref])


def clean(src, dst, streaks=True, key=(0, 200, 0)):
    """t452's KEYED clean: the white ground painted a key colour first, so cleandraft skips the black-shadow wear"""
    from keyed import keyed
    os.makedirs(OUT + "/key", exist_ok=True)
    src = keyed(src, OUT + "/key/" + os.path.basename(src), key)
    r = subprocess.run([PY, R + "/tools/cleandraft.py", src, dst] + (["--streaks"] if streaks else []), capture_output=True, text=True)
    if r.returncode and streaks:
        r = subprocess.run([PY, R + "/tools/cleandraft.py", src, dst], capture_output=True, text=True)
    m = re.search(r"(\d+) shadow", r.stdout)
    return r.returncode == 0, r.stderr[-300:], int(m.group(1)) if m else -1


def reduce_all():
    sys.path.insert(0, R + "/gfx/drafts/t452/trial")
    import gbs, icon3, armc
    from trial import measure, score
    import gbafollower as GF
    for d in ("clean", "reduced", "follower"): os.makedirs(OUT + "/" + d, exist_ok=True)
    M = json.load(open(OUT + "/metrics.json")) if os.path.exists(OUT + "/metrics.json") else {}
    keep = gbs.shift_off

    def place(cl, t, shared=None):
        if t in armc.ACHRO: gbs.place_rich.__globals__["shift_off"] = lambda acc, typ: acc
        try: return gbs.place_rich(cl, gbs.TYPE_COLOR[t], shared=shared)
        finally: gbs.place_rich.__globals__["shift_off"] = keep

    for k in KEYS:
        n, s = split(k); t = FN.DAEMONS[n][1]
        for seed in SEEDS:
            key = "%s_%d" % (k, seed)
            if not os.path.exists("%s/raw/%s_back_%d.png" % (OUT, k, seed)): continue
            m = dict(daemon=n, season=s, seed=seed, type=t); pal = gf = None
            for kind in ("front", "back"):
                src = "%s/raw/%s_%s_%d.png" % (OUT, k, kind, seed)
                cl = "%s/clean/%s_%s.png" % (OUT, key, kind)
                ok, err, worn = clean(src, cl, key=KEY(k))
                m[kind + "_worn"] = worn
                if not ok: m[kind + "_error"] = err; continue
                m[kind + "_folded"] = armc.fold(cl, t)
                try: grid, p = place(cl, t, pal if kind == "back" else None)
                except Exception as e: m[kind + "_error"] = repr(e)[:300]; continue
                if kind == "front": pal = p; gf = grid
                else:
                    fm = np.array(gf) > 0; bm = np.array(grid) > 0
                    iou = lambda a, b: float((a & b).sum()) / max(1, int((a | b).sum()))
                    m["sil"] = round(max(iou(fm, bm), iou(fm, bm[:, ::-1])), 2)
                gbs.write_png4("%s/reduced/%s_%s.png" % (OUT, key, kind), grid, p)
                m.update({kind + "_" + kk: v for kk, v in measure(grid, p, t).items()})
            if m.get("front_px") and m.get("back_px"): m["ratio"] = round(m["back_px"] / m["front_px"], 2)
            m["score"] = score(m) if m.get("front_px") and m.get("back_px") else 99
            #  the wear penalty: a vehicle part cleandraft took as a shadow is a part the player never sees
            m["score2"] = round(m["score"] + max(0, m.get("front_worn", 0) - 8) / 10, 2) if m["score"] < 99 else 99
            M[key] = m; print(key, {x: m.get(x) for x in ("ratio", "sil", "front_worn", "back_worn", "front_acc", "score", "score2")}, flush=True)
        for seed in ISEEDS:
            src = "%s/raw/%s_icon_%d.png" % (OUT, k, seed); key = "%s_icon_%d" % (k, seed)
            if not os.path.exists(src): continue
            cl = "%s/clean/%s.png" % (OUT, key); ok, err, worn = clean(src, cl, streaks=False, key=KEY(k))
            m = dict(daemon=n, season=s, seed=seed, kind="icon", worn=worn)
            if not ok: m["error"] = err; M[key] = m; continue
            try: info = icon3.make(n, t, cl, "%s/reduced/%s.png" % (OUT, key))
            except Exception as e: m["error"] = repr(e)[:300]; M[key] = m; continue
            m.update(icon_palette=info["icon_palette"], size=info["size"], **armc.icon_metrics("%s/reduced/%s.png" % (OUT, key)))
            M[key] = m; print(key, m, flush=True)
    json.dump(M, open(OUT + "/metrics.json", "w"), indent=1)
    P = autopick(M)
    for k in KEYS:
        n, s = split(k)
        if "seed" not in P.get(k, {}) or "icon_seed" not in P[k]: continue
        pi = M["%s_icon_%d" % (k, P[k]["icon_seed"])]["icon_palette"]
        r = icon3.reduce(FN.DAEMONS[n][1], "%s/clean/%s_%d_front.png" % (OUT, k, P[k]["seed"]), fit=(GF.MAX_H, GF.MAX_W), pal_index=pi)
        if r is None: print("no follower", k); continue
        g = GF.place([[int(v) for v in row] for row in r["grid"]])
        gbs.write_png4("%s/follower/%s_follower.png" % (OUT, k), g, gbs.icon_palettes()[pi], 32, 32)
        P[k]["follower_size"] = [r["grid"].shape[1], r["grid"].shape[0]]; P[k]["icon_palette"] = pi
    json.dump(P, open(OUT + "/picks.json", "w"), indent=1)


def autopick(M):
    P = picks()
    for k in KEYS:
        P.setdefault(k, {})
        c = [M.get("%s_%d" % (k, seed)) for seed in SEEDS]; c = [m for m in c if m and m["score"] < 99]
        if c and P[k].get("by") != "eye":
            b = min(c, key=lambda m: m["score2"]); P[k].update(seed=b["seed"], by="score", score=b["score"], score2=b["score2"])
        c = [M.get("%s_icon_%d" % (k, seed)) for seed in ISEEDS]; c = [m for m in c if m and "icon_sd" in m]
        if c and P[k].get("icon_by") != "eye":
            b = min(c, key=lambda m: (m["muddy"], m["icon_dom"] - m["icon_sd"] / 100 + 0.05 * m.get("icon_edge", 0)))
            P[k].update(icon_seed=b["seed"], icon_by="score")
    json.dump(P, open(OUT + "/picks.json", "w"), indent=1)
    return P


def export():
    import shutil
    d = os.path.dirname(OUT) + "/finals"; os.makedirs(d, exist_ok=True); P = picks()
    for k in KEYS:
        p = P[k]
        shutil.copy("%s/clean/%s_%d_front.png" % (OUT, k, p["seed"]), "%s/%s_front.png" % (d, k))
        shutil.copy("%s/clean/%s_%d_back.png" % (OUT, k, p["seed"]), "%s/%s_back.png" % (d, k))
        shutil.copy("%s/reduced/%s_icon_%d.png" % (OUT, k, p["icon_seed"]), "%s/%s_icon.png" % (d, k))
        shutil.copy("%s/follower/%s_follower.png" % (OUT, k), "%s/%s_follower.png" % (d, k))
        print(k, p)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "gen":
        keys = [x for x in a[2:] if not x.isdigit()] or KEYS
        seeds = tuple(int(x) for x in a[2:] if x.isdigit()) or SEEDS[:4]
        gen(a[1], keys, seeds)
    elif a[0] == "reduce": reduce_all()
    elif a[0] == "export": export()
    elif a[0] == "prompts":
        for k in KEYS: print(k, "::", front_prompt(k), "\n")

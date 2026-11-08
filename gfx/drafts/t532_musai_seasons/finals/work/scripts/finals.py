"""T-532 FINAL art (2026-11-08): the MUSAI branch's seasonal forms, arm C. DRAFT until built.

    finals.py gen fronts|backs|icons [NAME ...]   draw on roverbyteseer's ComfyUI through tools/spriteforge.py (klein4b + pixel LoRA)
    finals.py reduce                               cleandraft -> fold -> type ramp (gbs.place_rich) -> 64x64/16; backs in the
                                                   front's palette; icons by icon3; followers by icon3.reduce(fit 20x22)
    finals.py sheets                               per-species sheets, battle mocks, the 24-front sheet

The user's word on the concepts (2026-11-08): "Good, push vehicles more." Each form keeps its concept's direction --
the concept's chosen draft is the FIRST reference, the ROM front the second -- and the prompt now makes the vehicle a
readable part of the body. Two seeds a form (5321/5322, the concept's chosen seed among them); each back is drawn from
its own front by reference with its front's seed; icons 5341/5342 by reference to the chosen front.

TODAY'S ART AS SUMMER: only MUSAI's ROM front stands as its summer form (MUSAI wears the season itself, and 9.21's
summer is "the world as drawn"). The other five ROM fronts carry no vehicle at all, and the design puts a piece of the
vehicle on every season's body (CAREMUSAI's home IS summer), so each of those gets a summer form too: 23 forms.
"""
import json, os, sys, time, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/tools"); sys.path.insert(0, R + "/gfx/drafts/t452/scripts"); sys.path.insert(0, R + "/gfx/drafts/t452/trial")
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CON = R + "/gfx/drafts/t532_musai_seasons"
G = R + "/engineGba/graphics/pokemon/"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
LORA = [["klein4b_pixelart_limbicnation.safetensors", 1.0]]
SEEDS = (5321, 5322); ISEEDS = (5341, 5342)
SEASONS = ("winter", "spring", "summer", "autumn")

#  name: (ROM slot, type constant, type word, home season, identity, vehicle word)
DAEMONS = {
    "musai":     ("eevee", "NORMAL", "CONTENT", None,
                  "a little white astronaut robot, a big round white helmet with a dark visor face, two glowing eyes, two thin antennae", "the season itself"),
    "codemusai": ("flareon", "FIGHTING", "LOGIC", None,
                  "a little grey round robot, a big round helmet with one narrow dark visor slit straight across it, two red-tipped antennae", "the dialect: a piece of each"),
    "seekmusai": ("jolteon", "FLYING", "VECTOR", "autumn",
                  "a little astronaut robot, a round helmet with a dark visor and two glowing eyes, two wide flat fins sticking out sideways from its helmet", "side-by-side (UTV)"),
    "caremusai": ("vaporeon", "PSYCHIC", "CONTEXT", "summer",
                  "a little astronaut robot, big round padded headphones over its helmet, a dark visor with two soft eyes, one curly antenna", "pontoon boat"),
    "lensmusai": ("espeon", "PSYCHIC", "CONTEXT", "spring",
                  "a little robot whose whole face is one big round dark camera lens, one small antenna on the side of its head", "model plane"),
    "maskmusai": ("umbreon", "DARK", "OPAQUE", "winter",
                  "a little grey robot, a smooth light grey mask plate over its face with two narrow dark eye slits, round headphones", "snowmobile"),
}
ROM_SUMMER = {"musai"}   # today's ROM front stands as summer for these; every other summer is drawn

#  the vehicle IS the body (the fable rule): what every season keeps (KEEP), what the home season adds (FULL), and the
#  season's own flavour (FLAVOUR) -- the vehicle words first, so the model draws them
KEEP = {
    "seekmusai": "two big black knobby off-road tyres in place of its legs and a tubular roll-bar frame arching over its helmet",
    "caremusai": "two long silver pontoon floats side by side in place of its legs and a little metal deck railing round its middle",
    "lensmusai": "two straight model-aeroplane wings spread wide from its sides and a little two-bladed propeller on its chest",
    "maskmusai": "two curved snowmobile skis in place of its feet, a short rubber track tread under its body and a clear windscreen crest rising over its mask",
}
FULL = {
    "seekmusai": "its whole lower body IS a rugged little side-by-side off-road buggy: four big black knobby tyres where its legs would be, a tubular roll-bar cage built round and over its helmet, a front bumper with two round headlights, mud splashed on the tyres",
    "caremusai": "its whole lower body IS a little pontoon boat: two long silver pontoon tubes side by side in place of its legs, a flat deck on top of them with a metal deck railing all round it, a striped canopy roof over its head, water splashing round the pontoons",
    "lensmusai": "its whole body IS a little model aeroplane: two long straight balsa wings spread out wide from its sides, a big propeller spinning on its nose below the lens, a tail fin and tailplane behind it",
    "maskmusai": "its whole lower body IS a little snowmobile: two long curved skis out in front in place of its feet, a ridged rubber track tread under its body, a tall clear windscreen crest rising over its mask, snow spraying from the track",
}
FLAVOUR = {
    "seekmusai": {"winter": "snow chains on the tyres and snow on the roll bar", "spring": "fresh mud on the tyres and a green sprout tucked in the roll bar",
                  "summer": "dust on the tyres and a little sunshade on the roll bar", "autumn": "golden yellow autumn leaves caught in its fins"},
    "caremusai": {"winter": "the pontoons frozen into a small block of pale blue ice, snow on the railing and its headphones",
                  "spring": "a few rain drops, small blossoms on the railing", "summer": "warm sun",
                  "autumn": "fallen orange leaves on the deck and the pontoons"},
    "lensmusai": {"winter": "frost on the wings, two little skis under its feet", "spring": "pale yellow blossoms drifting",
                  "summer": "a bright sun glint on its lens", "autumn": "orange leaves caught on the wings"},
    "maskmusai": {"winter": "frost", "spring": "mud on the skis and melting snow dripping",
                  "summer": "the skis lifted, the windscreen crest tinted dark like sunglasses", "autumn": "fallen leaves under the skis and the first frost on the windscreen"},
}
MUSAI = {
    "winter": "a little cap of snow on its helmet, a short knitted scarf, frost on its antennae",
    "spring": "a small green sprout growing from the top of its helmet, tiny pink blossoms on its antennae",
    "summer": "a small sun-visor brim on its helmet, a tiny yellow sun charm on one antenna",
    "autumn": "a few orange fallen leaves stuck to its helmet, a little acorn on one antenna",
}
CODE = {   # a clear piece of the sibling whose season it is, and the glyph lights
    "winter": "a snowmobile's parts: two little curved skis for feet and a clear windscreen crest on its helmet, frost on its antennae",
    "spring": "a model plane's parts: two small straight model-aeroplane wings spread from its sides and a little propeller on its helmet",
    "summer": "a pontoon boat's parts: two small silver pontoon floats for feet and a short metal deck rail round its middle",
    "autumn": "an off-road buggy's parts: two small black knobby tyres at its sides and a little tubular roll-bar frame arching over its helmet",
}
GLYPH = "a row of glowing square glyph lights across its chest"
#  the cue for the icon and the back: the part of the vehicle that must still read
CUE = {
    "seekmusai": "the roll-bar frame over its helmet and the knobby tyres", "caremusai": "the deck railing and the pontoon floats",
    "lensmusai": "the spread model-aeroplane wings and the propeller", "maskmusai": "the windscreen crest and the skis",
}
CODECUE = {"winter": "the windscreen crest and the skis", "spring": "the little wings and the propeller",
           "summer": "the pontoon floats and the deck rail", "autumn": "the roll-bar frame and the knobby tyres"}

TAIL = ("full body, chibi proportions, big round head, soft shading, mostly greyscale, medium grey body with light grey "
        "highlights and dark grey shading, only small touches of colour, clean black outline, isolated on white, centered, "
        "large in the frame, the whole body inside the picture with white space on every side, no rider, no person, "
        "no shadow, no text, game asset")


def forms():
    for n in DAEMONS:
        for s in SEASONS:
            if s == "summer" and n in ROM_SUMMER: continue
            yield n, s


#  ROUND 2 (after the first reduction, 2026-11-08): at 64x64 some vehicles shrank to nothing -- CODEMUSAI's pieces,
#  MASKMUSAI's pale windscreen (cleandraft's flood fill took it as paper: no outline), LENSMUSAI's small wings,
#  SEEKMUSAI's tyres read as legs. These forms are drawn again on two more seeds with the parts BIG, dark and outlined,
#  and the pick is made among all four.
R2SEEDS = (5323, 5324)
SKI = ("two long curved black snowmobile skis sticking out in front in place of its feet, a big ridged black rubber track "
       "tread under its body and a smoke-grey tinted windscreen crest with a thick black outline rising over its mask")
WING = ("two big straight model-aeroplane wings spread far out from its sides, wider than its head, with a black outline, "
        "and a big two-bladed propeller on its chest")
TYRE = ("two big black knobby off-road tyres in place of its legs, as tall as its body, and a black tubular roll-bar frame "
        "arching high over its helmet")
R2 = {
    ("codemusai", "winter"): "a snowmobile's parts: two big long curved black snowmobile skis under its feet sticking out in front, and a tall smoke-grey tinted windscreen crest with a thick black outline rising from its helmet",
    ("codemusai", "spring"): "a model plane's parts: two big straight model-aeroplane wings sticking far out from its sides, wider than its head, with a black outline, and a big two-bladed propeller on top of its helmet",
    ("codemusai", "summer"): "a pontoon boat's parts: two big long silver pontoon floats with a black outline under it in place of its legs, as long as its body is wide, and a black metal deck rail round its middle",
    ("codemusai", "autumn"): "an off-road buggy's parts: two big black knobby tyres in place of its legs and a black tubular roll-bar frame arching high over its helmet",
    ("maskmusai", "winter"): "its whole lower body IS a little snowmobile: " + SKI + ", snow spraying from the track",
    ("maskmusai", "spring"): SKI, ("maskmusai", "summer"): SKI, ("maskmusai", "autumn"): SKI,
    ("lensmusai", "summer"): WING, ("lensmusai", "winter"): WING,
    ("seekmusai", "spring"): TYRE, ("seekmusai", "summer"): TYRE, ("seekmusai", "winter"): TYRE,
}


def seeds(n, s):
    return SEEDS + (R2SEEDS if (n, s) in R2 else ())


def body(n, s, seed=None):
    if seed in R2SEEDS:
        b = R2[n, s]
        if n == "codemusai": return b + ", " + GLYPH
        return b + ", " + FLAVOUR[n][s]
    return body1(n, s)


def body1(n, s):
    if n == "musai": return MUSAI[s]
    if n == "codemusai": return CODE[s] + ", " + GLYPH
    if DAEMONS[n][3] == s: return FULL[n] + ", " + FLAVOUR[n][s]
    return KEEP[n] + ", " + FLAVOUR[n][s]


def cue(n, s):
    if n == "musai": return MUSAI[s].split(",")[0]
    if n == "codemusai": return CODECUE[s] + ", the glyph lights on its chest"
    return CUE[n]


def front_prompt(n, s, seed=None):
    home = DAEMONS[n][3]
    lead = "its fullest, most complete seasonal form" if home == s else "its %s form" % s
    how = "wearing the season" if n == "musai" else "the machine built into its body so it clearly reads"
    return ("pixel art sprite, chibi, the same creature as in the images redrawn as %s, %s: %s; it is %s, keeping its face "
            "and its colours, facing left three-quarter view, %s" % (lead, how, body(n, s, seed), DAEMONS[n][4], TAIL))


def back_prompt(n, s):
    return ("pixel art sprite, chibi, Turn this exact creature around: the same creature seen from directly behind, rear view, "
            "facing away from the viewer, the back of its head, no face visible, still with %s, the same size in the frame, "
            "the same proportions, the same grey body and colours, the same pixel art style, black outline, centered on a "
            "plain white background, full body, no shadow, game asset" % cue(n, s))


def icon_prompt(n, s):
    return ("pixel art sprite, chibi, the same creature as in the image drawn as a tiny party menu icon: its head and upper body, "
            "%s, with %s clearly showing, its big head filling the picture, bold simple shapes, strong contrast between light, "
            "mid and dark grey, only small touches of colour, a thick black outline, facing the viewer, pure white background, "
            "centered, no text, game asset" % (DAEMONS[n][4], cue(n, s)))


def readpal(f):
    l = open(f).read().splitlines()[3:19]; return [tuple(int(v) for v in x.split()) for x in l]


def rom_ref(n): return CON + "/src/%s_romfront_512.png" % n


def concept_ref(n, s):
    P = json.load(open(CON + "/picks.json")); return "%s/raw/%s_%s_%d.png" % (CON, n, s, P["%s_%s" % (n, s)]["seed"])


def draw(out, text, seed, refs):
    import spriteforge as SF
    if os.path.exists(out + ".png"): return
    p = dict(mode="t2i", out=out, prompt=text, negative="", seed=seed, steps=None, cfg=None, sampler=None, scheduler=None,
             denoise=1.0, stop_at=None, size=(512, 512), model="klein4b", loras=LORA, references=list(refs))
    for k in range(3):
        try: SF.run(p); return
        except SystemExit as e: print("  retry", out, e, flush=True); time.sleep(10)
        except Exception as e: print("  retry", out, repr(e), flush=True); time.sleep(10)


def gen(stage, names):
    os.makedirs(OUT + "/raw", exist_ok=True)
    for n, s in forms():
        if names and n not in names: continue
        k = "%s_%s" % (n, s)
        if stage == "fronts":
            for seed in seeds(n, s):
                print("front", k, seed, flush=True)
                draw("%s/raw/%s_front_%d" % (OUT, k, seed), front_prompt(n, s, seed), seed, [concept_ref(n, s), rom_ref(n)])
        elif stage == "backs":
            for seed in seeds(n, s):
                f = "%s/raw/%s_front_%d.png" % (OUT, k, seed)
                if os.path.exists(f):
                    print("back", k, seed, flush=True); draw("%s/raw/%s_back_%d" % (OUT, k, seed), back_prompt(n, s), seed, [f])
        elif stage == "icons":
            P = json.load(open(OUT + "/picks.json"))
            ref = "%s/raw/%s_front_%d.png" % (OUT, k, P[k]["seed"])
            for seed in ISEEDS:
                print("icon", k, seed, flush=True); draw("%s/raw/%s_icon_%d" % (OUT, k, seed), icon_prompt(n, s), seed, [ref])


def reduce_all():
    import gbs, icon3, armc
    from trial import measure, score
    import gbafollower as GF
    for d in ("clean", "reduced"): os.makedirs(OUT + "/" + d, exist_ok=True)
    M = {}
    keep = gbs.shift_off

    def place(cl, t, shared=None):
        #  the concept job's shift_off rule: skipped on the near-grey types (armc.ACHRO), where the body has no hue to
        #  protect and the rotation turned MUSAI's orange leaves navy; kept elsewhere
        if t in armc.ACHRO: gbs.place_rich.__globals__["shift_off"] = lambda acc, typ: acc
        try: return gbs.place_rich(cl, gbs.TYPE_COLOR[t], shared=shared)
        finally: gbs.place_rich.__globals__["shift_off"] = keep

    for n, s in forms():
        t = DAEMONS[n][1]; k = "%s_%s" % (n, s)
        for seed in seeds(n, s):
            key = "%s_%d" % (k, seed); m = dict(daemon=n, season=s, seed=seed, type=t); pal = gf = None
            for kind in ("front", "back"):
                src = "%s/raw/%s_%s_%d.png" % (OUT, k, kind, seed)
                if not os.path.exists(src): continue
                cl = "%s/clean/%s_%s.png" % (OUT, key, kind)
                ok, err = armc.clean(src, cl)
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
            if pal is not None:
                with open("%s/reduced/%s_normal.pal" % (OUT, key), "w") as f:
                    f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in (list(pal) + [(0, 0, 0)] * 16)[:16]))
            if m.get("front_px") and m.get("back_px"): m["ratio"] = round(m["back_px"] / m["front_px"], 2)
            m["score"] = score(m) if m.get("front_px") and m.get("back_px") else 99
            M[key] = m; print(key, {x: m.get(x) for x in ("ratio", "sil", "front_acc", "front_edge", "back_edge", "score")}, flush=True)
        for seed in ISEEDS:
            src = "%s/raw/%s_icon_%d.png" % (OUT, k, seed); key = "%s_icon_%d" % (k, seed)
            if not os.path.exists(src): continue
            cl = "%s/clean/%s.png" % (OUT, key); ok, err = armc.clean(src, cl, streaks=False)
            m = dict(daemon=n, season=s, seed=seed, kind="icon")
            if not ok: m["error"] = err; M[key] = m; continue
            try: info = icon3.make(n, t, cl, "%s/reduced/%s.png" % (OUT, key))
            except Exception as e: m["error"] = repr(e)[:300]; M[key] = m; continue
            m.update(icon_palette=info["icon_palette"], size=info["size"], **armc.icon_metrics("%s/reduced/%s.png" % (OUT, key)))
            M[key] = m; print(key, m, flush=True)
    json.dump(M, open(OUT + "/metrics.json", "w"), indent=1)
    P = autopick(M)
    #  the follower: its own 32x32 picture, as tools/gbafollower.py makes one for a redrawn daemon (REDUCED) -- the
    #  chosen clean front by icon3.reduce fitted to 20x22, in the SAME shared palette as the form's chosen icon
    os.makedirs(OUT + "/follower", exist_ok=True)
    for n, s in forms():
        k = "%s_%s" % (n, s)
        if "seed" not in P.get(k, {}) or "icon_seed" not in P[k]: continue
        pi = M["%s_icon_%d" % (k, P[k]["icon_seed"])]["icon_palette"]
        r = icon3.reduce(DAEMONS[n][1], "%s/clean/%s_%d_front.png" % (OUT, k, P[k]["seed"]), fit=(GF.MAX_H, GF.MAX_W), pal_index=pi)
        if r is None: print("no follower", k); continue
        g = GF.place([[int(v) for v in row] for row in r["grid"]])
        gbs.write_png4("%s/follower/%s_follower.png" % (OUT, k), g, gbs.icon_palettes()[pi], 32, 32)
        P[k]["follower_size"] = [r["grid"].shape[1], r["grid"].shape[0]]; P[k]["icon_palette"] = pi
    json.dump(P, open(OUT + "/picks.json", "w"), indent=1)


def autopick(M):
    P = json.load(open(OUT + "/picks.json")) if os.path.exists(OUT + "/picks.json") else {}
    for n, s in forms():
        k = "%s_%s" % (n, s); P.setdefault(k, {})
        c = [M.get("%s_%d" % (k, seed)) for seed in seeds(n, s)]; c = [m for m in c if m and m["score"] < 99]
        if c and P[k].get("by") != "eye":
            b = min(c, key=lambda m: m["score"]); P[k].update(seed=b["seed"], by="score", score=b["score"])
        c = [M.get("%s_icon_%d" % (k, seed)) for seed in ISEEDS]; c = [m for m in c if m and "icon_sd" in m]
        if c and P[k].get("icon_by") != "eye":
            b = min(c, key=lambda m: (m["muddy"], m["icon_dom"] - m["icon_sd"] / 100 + 0.05 * m.get("icon_edge", 0)))
            P[k].update(icon_seed=b["seed"], icon_by="score")
    json.dump(P, open(OUT + "/picks.json", "w"), indent=1)
    return P


def frontpick(n, s):
    P = json.load(open(OUT + "/picks.json")); k = "%s_%s" % (n, s)
    if "seed" in P.get(k, {}): return P[k]
    return None


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "gen": gen(a[1], a[2:])
    elif a[0] == "reduce": reduce_all()
    elif a[0] == "prompts":
        for n, s in forms(): print(n, s, "::", front_prompt(n, s), "\n")

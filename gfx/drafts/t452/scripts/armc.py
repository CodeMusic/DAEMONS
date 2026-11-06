"""T-452 redraws in arm C (2026-11-06; the user chose arm C after the trial, gfx/drafts/t452/trial/).

    armc.py gen [fronts|backs|icons] [NAME ...]   draw on the sprite server through tools/spriteforge.py --model klein4b
    armc.py reduce                                  cleandraft -> type ramp -> 64x64 / 16 colours; icons by icon3; metrics
    armc.py sheets                                  the review sheets (sheets/)

FOUR JOBS, the roster walk's (docs/private/t452-roster-walk-2026-11-06.md):
  WORST  the worst ten: front from the prompt (the one key prop named first, the chibi subject), back from its own
         front by reference, icon drawn on its own as a head-and-shoulders bust by reference to the new front
  B13    batch 13 restyled to the roster's chibi charm, the same way (LODESTAR, PERIHELION, ILLUMINED are in WORST)
  BACKS  the ten mismatched backs: back only, drawn by reference to the APPROVED front in the ROM (shown at 8x on
         white), reduced through that front's own palette (one palette per species)
  ICONS  the muddy icons (the walk's list, less the daemons redrawn above): the bust by reference to the ROM front

Every draw is spriteforge.run with model klein4b and the Limbicnation pixel-art LoRA at 1.0, 512x512, so each draft's
JSON records the model, LoRA, reference, seed and prompt. Two seeds a daemon: 7101/7102 fronts (each back the seed of
its front), 7141/7142 icons. Drafts land in gfx/drafts/t452/c/armc/ (c/ itself is batch 1's folder). Nothing writes
into the game.
"""
import json, os, sys, subprocess, time, colorsys
from collections import Counter
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
R = "/Users/christopherhicks/Projects/DAEMONS"; sys.path.insert(0, R + "/tools"); sys.path.insert(0, R + "/gfx/drafts/t452/trial")
import spriteforge as SF
import subjects as SJ
OUT = R + "/gfx/drafts/t452/c/armc"
G = R + "/engineGba/graphics/pokemon/"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
LORA = [["klein4b_pixelart_limbicnation.safetensors", 1.0]]
FSEEDS = (7101, 7102); ISEEDS = (7141, 7142)

WORST = "perihelion lodestar illumined broadcast tracer fossilnet rovercub smogstack overloaded obsession".split()
B13_ALL = ['reflection', 'lodestar', 'perihelion', 'lyubov', 'multimal', 'illumined', 'lynx', 'bastet', 'stump', 'boosting',
           'canopy', 'coinflip', 'montecarlo', 'lasvegas', 'runoff', 'alluvium', 'delta', 'smudge', 'eclipse', 'detour', 'unbranched']
B13 = [n for n in B13_ALL if n not in WORST]
BACKS = "seethe heatdeath ensemble crawler wiretap manifold monolith outlier heartbeat corefile".split()
MUDDY = ("broadcast tracer fossilnet smogstack posterior overloaded singular castor ensemble skew blocking khione indexer "
         "multicast burstmode flocking dustdevil relay worm scheduler snare landfill rebuttal acquire circular keeper backpress "
         "sigkill cinder stampede escalate caremusai codemusai lensmusai magtape emergence starr syllabus entrapment sounding "
         "fakeroot grasp omen startle hardline crywolf oldbranch repay engram grievance armouring illusion stump canopy lasvegas "
         "eclipse cadence prefork sparring particle gradient backdoor blackwater sinkhole reforge fewshot zeroshot forgetting "
         "transfer forgery firmware syn ack savestate guesswork epiphany").split()
REDRAW = WORST + B13
ICONS = [n for n in MUDDY if n not in REDRAW]

PFX = "pixel art sprite, chibi, pure white background, pixel art game sprite of a single cute creature, "
TAIL = ("full body, chibi proportions, big round head, large expressive eyes, soft shading, mostly greyscale, medium grey "
        "body with light grey highlights and dark grey shading, only small touches of colour, clean black outline, "
        "isolated on white, centered, large in the frame, the whole body inside the picture with white space on every side, "
        "no shadow, no text, game asset")
#  what the walk asked of each, said to the model (no negatives at cfg 1, so in the positive)
EXTRA = {
    "perihelion": "standing on nothing, no disc, no circle, no frame and no starfield behind it, only a few tiny separate stars in its tail",
    "obsession": "its horns well inside the picture with white space above them",
    "lodestar": "one plain grey body with one small yellow star, no magenta",
    "illumined": "a pale grey cat with a pale halo",
    "eclipse": "the eclipse behind it is a dark grey disc with a thin bright white ring round its edge, not solid black, and its fur is mid grey",
    "lynx": "a grey kitten, not orange", "bastet": "a grey cat, no gold, only the collar coloured",
}
#  second-round backs (the first two seeds did not turn, or turned into another shape): more seeds, and what to keep
RETRY = {"monolith": (7103, 7104), "crawler": (7103, 7104)}   # SMUDGE and ECLIPSE: their 7101/7102 redrawn with the extra words
BACK_EXTRA = {
    "monolith": "we see only the smooth rocky back of the sphere: its big eye is on the far side and cannot be seen at all",
    "smudge": "we see only the back of its head and its back, its face and its eyes are hidden on the far side",
    "crawler": "still three small round green blobs in a row, low to the ground, each seen from behind, no faces",
}
SUBJ_ROVERCUB = dict(key="one big round camera lens eye and floppy metal puppy ears",
                     front="a small robot puppy, a four-legged robot dog standing on all four legs, a boxy grey metal body, four short "
                           "jointed metal legs with round paw feet, a big round robot head, a short antenna tail",
                     icon="a cute robot puppy head with floppy metal ears and one big round camera lens eye")
SPEC = json.load(open(R + "/companion/server/data/species.json")); BY = {v["name"].lower(): v for v in SPEC.values()}


def charm(n):
    if n == "rovercub": return SUBJ_ROVERCUB
    return dict(SJ.CHARM.get(n, {}), **getattr(SJ, "CHARM2", {}).get(n, {}))


def rom(n):
    """the daemon's built art: front, back, icon, palette paths"""
    slot = BY[n]["constant"].lower(); d = G + slot
    if not os.path.isdir(d): d = G + "nexus_" + n
    f = dict(front=d + "/front.png", back=d + "/back.png", icon=d + "/icon.png", pal=d + "/normal.pal", slot=slot)
    if n == "overloaded":   # the build joins castform/normal for the body (TODO T-452)
        f.update(front=d + "/normal/front.png", back=d + "/normal/back.png", pal=d + "/normal/normal.pal")
    return f


def typ(n):
    import gbs
    return gbs.primary_type(rom(n)["slot"])


def readpal(f):
    l = open(f).read().splitlines()[3:19]; return [tuple(int(v) for v in x.split()) for x in l]


def rom_ref(n):
    """the ROM's approved front at 8x on white, a 512 reference"""
    p = OUT + "/src/%s_romfront_512.png" % n
    if not os.path.exists(p):
        os.makedirs(OUT + "/src", exist_ok=True)
        im = Image.open(rom(n)["front"]); idx = np.array(im)[:64, :64]; pal = readpal(rom(n)["pal"])
        a = np.array([pal[i] if i else (255, 255, 255) for i in idx.flat], np.uint8).reshape(64, 64, 3)
        Image.fromarray(a).resize((512, 512), Image.NEAREST).save(p)
    return p


def front_prompt(n):
    c = charm(n)
    subj = c["front2"] if c.get("front2") else c["key"] + ", " + c["front"]
    if c.get("front2") and c["key"] not in subj: subj = c["key"] + ", " + subj
    s = PFX + subj + ", facing left three-quarter view"
    if n in EXTRA: s += ", " + EXTRA[n]
    return s + ", " + TAIL


def seeds(n):
    return FSEEDS + RETRY.get(n, ())


def back_prompt(n):
    keep = charm(n)["key"] + (", " + BACK_EXTRA[n] if n in BACK_EXTRA else "")
    return ("pixel art sprite, chibi, Turn this exact creature around: the same creature seen from directly behind, rear view, facing "
            "away from the viewer, the back of its head, no face visible, %s, the same size in the frame, "
            "the same proportions, the same grey body and colours, the same pixel art style, black outline, "
            "centered on a plain white background, full body, no shadow, game asset" % keep)


def icon_prompt(n):
    return ("pixel art sprite, chibi, the same creature as in the image drawn as a tiny party menu icon: a head and shoulders bust, %s, "
            "its big head filling the picture, bold simple shapes, strong contrast between light, mid and dark grey, only small touches "
            "of colour, a thick black outline, facing the viewer, pure white background, centered, no text, game asset" % charm(n)["icon"])


def draw(out, prompt, seed, refs=()):
    if os.path.exists(out + ".png"): return
    p = dict(mode="t2i", out=out, prompt=prompt, negative="", seed=seed, steps=None, cfg=None, sampler=None, scheduler=None,
             denoise=1.0, stop_at=None, size=(512, 512), model="klein4b", loras=LORA, references=list(refs))
    for k in range(3):
        try: SF.run(p); return
        except SystemExit as e: print("  retry", out, e, flush=True); time.sleep(10)
        except Exception as e: print("  retry", out, repr(e), flush=True); time.sleep(10)


def gen(stage, names):
    os.makedirs(OUT + "/raw", exist_ok=True)
    pick = lambda L: [n for n in L if not names or n in names]
    if stage in ("all", "fronts"):
        for n in pick(REDRAW):
            for s in FSEEDS: draw("%s/raw/%s_front_%d" % (OUT, n, s), front_prompt(n), s)
    if stage in ("all", "backs"):
        for n in pick(REDRAW):
            for s in FSEEDS:
                f = "%s/raw/%s_front_%d.png" % (OUT, n, s)
                if os.path.exists(f): draw("%s/raw/%s_back_%d" % (OUT, n, s), back_prompt(n), s, [f])
        for n in pick(BACKS):
            for s in seeds(n): draw("%s/raw/%s_back_%d" % (OUT, n, s), back_prompt(n), s, [rom_ref(n)])
    if stage in ("all", "icons"):
        P = json.load(open(OUT + "/picks.json")) if os.path.exists(OUT + "/picks.json") else {}
        for n in pick(REDRAW + ICONS):
            if n in REDRAW:
                if n not in P: print("  no front picked yet for", n); continue
                ref = "%s/raw/%s_front_%d.png" % (OUT, n, P[n]["seed"])
            else:
                ref = rom_ref(n)
            for s in ISEEDS: draw("%s/raw/%s_icon_%d" % (OUT, n, s), icon_prompt(n), s, [ref])


# ---- reduction and metrics ---------------------------------------------------------------------------------------
def clean(src, dst, streaks=True):
    r = subprocess.run([PY, R + "/tools/cleandraft.py", src, dst] + (["--streaks"] if streaks else []), capture_output=True, text=True)
    if r.returncode and streaks:
        r = subprocess.run([PY, R + "/tools/cleandraft.py", src, dst], capture_output=True, text=True)
    return r.returncode == 0, r.stderr[-300:]


ACHRO = {"NORMAL", "DARK", "ROCK", "STEEL"}


def fold(path, t):
    """THE TYPE-HUE TRAP, closed before the reducer sees it: a saturated pixel within 40 degrees of the type's own hue
    IS the type colour (GRASS's green leaves, FIRE's flames), but place_rich treats it as an accent and shift_off rotates
    it to the far side of the wheel -- CANOPY's leaves came out purple. Such pixels are made grey at their own luminance,
    so they join the body and the type ramp; streak markers are left alone. Achromatic types are skipped."""
    import gbs
    if t in ACHRO: return 0
    im = Image.open(path).convert("RGBA"); a = np.asarray(im).astype(int); rgb = a[..., :3]
    th = colorsys.rgb_to_hsv(*[v / 255 for v in gbs.TYPE_COLOR[t]])[0]
    sat = rgb.max(2) - rgb.min(2)
    mk = np.zeros(sat.shape, bool)
    for m in gbs.STREAK_MARKERS: mk |= np.abs(rgb - np.array(m)).max(2) <= gbs.STREAK_TOLERANCE
    f = rgb / 255.0; mx = f.max(2); mn = f.min(2); d = np.where(mx - mn == 0, 1, mx - mn)
    h = np.where(mx == f[..., 0], ((f[..., 1] - f[..., 2]) / d) % 6, np.where(mx == f[..., 1], (f[..., 2] - f[..., 0]) / d + 2, (f[..., 0] - f[..., 1]) / d + 4)) / 6
    hd = np.minimum(np.abs(h - th), 1 - np.abs(h - th)) * 360
    sel = (a[..., 3] > 127) & (sat >= gbs.SAT_ACCENT) & (hd <= 40) & ~mk
    L = (rgb[..., 0] * 299 + rgb[..., 1] * 587 + rgb[..., 2] * 114) // 1000
    a[sel, 0] = a[sel, 1] = a[sel, 2] = L[sel]
    Image.fromarray(a.astype(np.uint8), "RGBA").save(path)
    return int(sel.sum())


def icon_metrics(png):
    """the roster walk's muddy test (audit.py): colours, the one-colour share, luminance spread, on frame 1"""
    im = Image.open(png); idx = np.array(im)[:32]; p = im.getpalette()
    px = [int(v) for v in idx.flat if v]
    if not px: return dict(icon_cols=0, icon_dom=1, icon_sd=0, muddy=True)
    lum = lambda i: 0.299 * p[3 * i] + 0.587 * p[3 * i + 1] + 0.114 * p[3 * i + 2]
    c = Counter(px); dom = c.most_common(1)[0][1] / len(px); L = np.array([lum(v) for v in px])
    ys, xs = np.where(idx > 0)
    edge = int(((xs == 0) | (xs == 31) | (ys == 0)).sum())
    return dict(icon_cols=len(c), icon_dom=round(dom, 2), icon_sd=round(float(L.std()), 1), icon_edge=edge,
                muddy=bool(len(c) < 4 or dom > 0.6 or L.std() < 28))


def reduce_all():
    import gbs, icon3
    from trial import measure, score, grid_align
    for d in ("clean", "reduced"): os.makedirs(OUT + "/" + d, exist_ok=True)
    M = json.load(open(OUT + "/metrics.json")) if os.path.exists(OUT + "/metrics.json") else {}
    for n in REDRAW + BACKS:
        t = typ(n)
        for s in seeds(n):
            key = "%s_%d" % (n, s); m = dict(daemon=n, seed=s, type=t, job="BACKS" if n in BACKS else ("WORST" if n in WORST else "B13"))
            pal = gf = None
            if n in BACKS:
                pal = readpal(rom(n)["pal"]); gf = [list(map(int, r)) for r in np.array(Image.open(rom(n)["front"]))[:64]]
                m.update({"front_" + k: v for k, v in measure(gf, pal, t).items()})
            for kind in (("back",) if n in BACKS else ("front", "back")):
                src = "%s/raw/%s_%s_%d.png" % (OUT, n, kind, s)
                if not os.path.exists(src): continue
                m[kind + "_seconds"] = json.load(open(src[:-4] + ".json"))["seconds"]; m[kind + "_grid"] = grid_align(src)
                cl = "%s/clean/%s_%s.png" % (OUT, key, kind)
                ok, err = clean(src, cl)
                if not ok: m[kind + "_error"] = err; continue
                m[kind + "_folded"] = fold(cl, t)
                try: grid, p = gbs.place_rich(cl, gbs.TYPE_COLOR[t], shared=pal if kind == "back" else None)
                except Exception as e: m[kind + "_error"] = repr(e)[:300]; continue
                if kind == "front": pal = p; gf = grid
                else:
                    fm = np.array(gf) > 0; bm = np.array(grid) > 0
                    iou = lambda a, b: float((a & b).sum()) / max(1, int((a | b).sum()))
                    m["sil"] = round(max(iou(fm, bm), iou(fm, bm[:, ::-1])), 2)
                gbs.write_png4("%s/reduced/%s_%s.png" % (OUT, key, kind), grid, p)
                m.update({kind + "_" + k: v for k, v in measure(grid, p, t).items()})
            if pal is not None and n not in BACKS:
                with open("%s/reduced/%s_normal.pal" % (OUT, key), "w") as f:
                    f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in (list(pal) + [(0, 0, 0)] * 16)[:16]))
            if m.get("front_px") and m.get("back_px"): m["ratio"] = round(m["back_px"] / m["front_px"], 2)
            m["score"] = score(m) if m.get("front_px") and m.get("back_px") else 99
            M[key] = m
            print(key, {k: v for k, v in m.items() if k in ("ratio", "sil", "front_acc", "back_acc", "front_typ", "back_typ", "front_edge", "back_edge", "score")}, flush=True)
    for n in REDRAW + ICONS:
        t = typ(n)
        for s in ISEEDS:
            src = "%s/raw/%s_icon_%d.png" % (OUT, n, s); key = "%s_icon_%d" % (n, s)
            if not os.path.exists(src): continue
            cl = "%s/clean/%s.png" % (OUT, key); ok, err = clean(src, cl, streaks=False)
            m = dict(daemon=n, seed=s, kind="icon", icon_seconds=json.load(open(src[:-4] + ".json"))["seconds"])
            if not ok: m["error"] = err; M[key] = m; continue
            out = "%s/reduced/%s.png" % (OUT, key)
            try: info = icon3.make(n, t, cl, out)
            except Exception as e: m["error"] = repr(e)[:300]; M[key] = m; continue
            m.update(icon_palette=info["icon_palette"], size=info["size"], **icon_metrics(out))
            M[key] = m; print(key, m, flush=True)
    json.dump(M, open(OUT + "/metrics.json", "w"), indent=1)
    autopick(M)


def autopick(M):
    """the better seed by the trial's score (front/back) and the walk's muddy test (icon); picks.json can be edited by
    hand afterwards -- a pick marked "by": "eye" is never overwritten"""
    P = json.load(open(OUT + "/picks.json")) if os.path.exists(OUT + "/picks.json") else {}
    for n in REDRAW + BACKS:
        c = [M.get("%s_%d" % (n, s)) for s in seeds(n)]; c = [m for m in c if m and m["score"] < 99]
        if not c: continue
        if P.get(n, {}).get("by") != "eye":
            b = min(c, key=lambda m: m["score"]); P.setdefault(n, {}).update(seed=b["seed"], by="score")
    for n in REDRAW + ICONS:
        c = [M.get("%s_icon_%d" % (n, s)) for s in ISEEDS]; c = [m for m in c if m and "icon_sd" in m]
        if not c: continue
        if P.get(n, {}).get("icon_by") != "eye":
            b = min(c, key=lambda m: (m["muddy"], m["icon_dom"] - m["icon_sd"] / 100 + 0.05 * m.get("icon_edge", 0)))
            P.setdefault(n, {}).update(icon_seed=b["seed"], icon_by="score")
    json.dump(P, open(OUT + "/picks.json", "w"), indent=1)


# ---- sheets -------------------------------------------------------------------------------------------------------
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 15); FS = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
PAPER = (236, 234, 226); INK = (30, 30, 34); GROUND = (205, 205, 172); PARTY = (98, 156, 131); RED = (170, 40, 40)


def show(png, pal=None, h=64):
    im = Image.open(png)
    if pal: im.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    idx = np.array(im); a = np.array(im.convert("RGBA")); a[idx == 0, 3] = 0
    return Image.fromarray(a).crop((0, 0, im.width, h))


def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im)
    return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)


def battle(front, back):
    """a 1x battle composite, 240x160: the foe's front on its ground at the top right, the lead's back at the bottom
    left, the text box over the lead's lower rows (vanilla's positions, elevation left out)"""
    s = Image.new("RGBA", (240, 160), (248, 248, 232, 255)); d = ImageDraw.Draw(s)
    d.ellipse((136, 62, 216, 78), fill=(196, 206, 150, 255)); d.ellipse((8, 100, 120, 120), fill=(196, 206, 150, 255))
    if front: s.alpha_composite(front, (144, 16))
    if back: s.alpha_composite(back, (40, 48))
    d.rectangle((0, 112, 239, 159), fill=(40, 80, 104, 255)); d.rectangle((4, 116, 235, 155), outline=(232, 232, 232, 255), width=2)
    d.rectangle((140, 74, 236, 104), fill=(248, 248, 216, 255), outline=(60, 60, 60, 255))
    d.rectangle((4, 4, 100, 30), fill=(248, 248, 216, 255), outline=(60, 60, 60, 255))
    return s.convert("RGB")


def sheets():
    M = json.load(open(OUT + "/metrics.json")); P = json.load(open(OUT + "/picks.json"))
    os.makedirs(OUT + "/sheets", exist_ok=True)
    order = WORST + B13 + BACKS
    order = [n for n in order if n in P and "seed" in P[n]]
    groups = [order[:19], order[19:]] if len(order) > 22 else [order]
    for gi, grp in enumerate(groups):
        RH = 182; W = 1640
        sh = Image.new("RGB", (W, 64 + len(grp) * (RH + 14) + 30), PAPER); d = ImageDraw.Draw(sh)
        d.text((16, 10), "T-452 redraws in arm C (FLUX.2 klein 4B + pixel-art LoRA), 2026-11-06 -- DRAFTS, not in the ROM. Sheet %d of %d." % (gi + 1, len(groups)), fill=INK, font=F)
        d.text((16, 32), "IN ROM front/back/icon | DRAFT front/back/icon, each at 1x and 2x | the draft in battle at 1x (BACKS: the ROM's front and the new back) | ROM in battle at 1x", fill=INK, font=FS)
        y = 64
        for n in grp:
            v = BY[n]; f = rom(n); npal = readpal(f["pal"]); s = P[n]["seed"]; m = M["%s_%d" % (n, s)]; k = "%s/reduced/%s_%d_" % (OUT, n, s)
            job = m["job"]
            lab = "%d %s  [%s, %s]  seed %d  back/front %.2f  sil %.2f  accents f %s / b %s  type-hue f %s / b %s  edge f %s / b %s" % (
                v["national"], v["name"], job, m["type"], s, m.get("ratio", 0), m.get("sil", 0), m.get("front_acc"), m.get("back_acc"),
                m.get("front_typ"), m.get("back_typ"), m.get("front_edge"), m.get("back_edge"))
            d.text((16, y), lab, fill=RED if (m.get("front_edge") or m.get("back_edge") or (m.get("front_acc") or 0) > 15 or (m.get("back_acc") or 0) > 15) else INK, font=FS)
            yy = y + 18
            romims = [(show(f["front"], npal), GROUND), (show(f["back"], npal), GROUND), (show(f["icon"], None, 32), PARTY)]
            ip = P[n].get("icon_seed"); icn = "%s/reduced/%s_icon_%d.png" % (OUT, n, ip) if ip else None
            if job == "BACKS":
                fpal = npal
                new = [(show(f["front"], npal), GROUND), (show(k + "back.png", fpal), GROUND),
                       (show(icn, None, 32) if icn and os.path.exists(icn) else show(f["icon"], None, 32), PARTY)]
            else:
                new = [(show(k + "front.png"), GROUND), (show(k + "back.png"), GROUND),
                       (show(icn, None, 32), PARTY) if icn and os.path.exists(icn) else (Image.new("RGBA", (32, 32)), PARTY)]
            x = 16
            for part, ims in (("ROM", romims), ("DRAFT", new)):
                d.text((x, yy), part, fill=INK if part == "ROM" else RED, font=FS)
                for im, bg in ims:
                    sh.paste(on(im, bg, 1), (x, yy + 16)); sh.paste(on(im, bg, 2), (x + im.width + 6, yy + 16))
                    x += im.width * 3 + 16
                x += 20
            d.line((x - 10, yy, x - 10, yy + RH - 10), fill=INK, width=1)
            sh.paste(battle(new[0][0], new[1][0]), (x, yy)); x += 250
            sh.paste(battle(romims[0][0], romims[1][0]), (x, yy))
            d.text((x + 246, yy), "ROM", fill=INK, font=FS)
            y += RH + 14
        out = OUT + "/sheets/armc_redraws_%d.png" % (gi + 1); sh.save(out); print(out, sh.size)
    # the icons: every new icon beside the ROM's, 1x and 2x on the party ground, frame 1
    names = [n for n in REDRAW + ICONS if P.get(n, {}).get("icon_seed")]
    per = 6; CW = 240; RH = 104
    sh = Image.new("RGB", (16 + per * CW, 84 + ((len(names) + per - 1) // per) * RH), PAPER); d = ImageDraw.Draw(sh)
    d.text((16, 10), "T-452 icons redrawn in arm C as 32px head-and-shoulders busts, then icon3 -- DRAFTS. ROM | draft, 1x and 2x, frame 1.", fill=INK, font=F)
    d.text((16, 32), "under each: the walk's muddy test on the draft (colours / one-colour share / contrast); red = still muddy by it", fill=INK, font=FS)
    for i, n in enumerate(names):
        x = 16 + (i % per) * CW; y = 56 + (i // per) * RH
        m = M["%s_icon_%d" % (n, P[n]["icon_seed"])]
        d.text((x, y), BY[n]["name"] + (" *" if n in REDRAW else ""), fill=INK, font=FS)
        a = show(rom(n)["icon"], None, 32); b = show("%s/reduced/%s_icon_%d.png" % (OUT, n, P[n]["icon_seed"]), None, 32)
        sh.paste(on(a, PARTY, 1), (x, y + 16)); sh.paste(on(a, PARTY, 2), (x + 36, y + 16))
        sh.paste(on(b, PARTY, 1), (x + 112, y + 16)); sh.paste(on(b, PARTY, 2), (x + 148, y + 16))
        d.text((x, y + 16 + 66), "%d / %.0f%% / %.0f" % (m["icon_cols"], 100 * m["icon_dom"], m["icon_sd"]), fill=RED if m["muddy"] else INK, font=FS)
    d.text((16, sh.height - 18), "* = a redrawn daemon (the icon is of its new front)", fill=INK, font=FS)
    out = OUT + "/sheets/armc_icons.png"; sh.save(out); print(out, sh.size)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "gen": gen(a[1] if len(a) > 1 else "all", a[2:])
    elif a[0] == "reduce": reduce_all()
    elif a[0] == "sheets": sheets()

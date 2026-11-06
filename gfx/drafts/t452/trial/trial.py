"""T-452 pixel-model trial (2026-11-06): the same three daemons drawn by four arms, reduced by the existing reducer.

    trial.py gen [ARM ...]     draw (A shaper, B klein9b, C klein4b+pixel LoRA, D z-image turbo)
    trial.py reduce            cleandraft -> gbs.place_rich in the type ramp -> 64x64 4bpp + icon, and the metrics
    trial.py sheet             the comparison sheets

Drafts, records, reductions and sheets go to gfx/drafts/t452/trial/. Nothing writes into the game, and the server's
models are only read (POST /free between arms clears ComfyUI's own cache so two big models are never resident at once).
"""
import json, os, sys, time, uuid, subprocess, urllib.request, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = "/Users/christopherhicks/Projects/DAEMONS"
SC = R + "/gfx/drafts/t452/scripts"; sys.path.insert(0, SC)
OUT = R + "/gfx/drafts/t452/trial"
HOST = "http://roverbyteseer:8008"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
SEEDS = (7001, 7002, 7003)
ARMS = {"A": "spriteShaper (SDXL) -- today", "B": "klein 9B fp8 (on disk)",
        "C": "FLUX.2 klein 4B + Limbicnation pixel-art LoRA", "D": "Z-Image Turbo, no LoRA"}

TAIL = ("full body, chibi proportions, big round head, large expressive eyes, soft shading, mostly greyscale, medium grey "
        "body with light grey highlights and dark grey shading, only small touches of colour, clean black outline, "
        "isolated on white, centered, large in the frame, no shadow, no text")
BTAIL = ("full body, chibi proportions, big round head seen from behind, soft shading, mostly greyscale, medium grey body "
         "with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, large in "
         "the frame, no shadow, no text")
NEG = ("girl, human, photorealistic, 3d render, colorful, rainbow, colored background, grey background, dark background, "
       "scenery, floor, ground, text, letters, watermark, multiple creatures, two creatures, duplicate, human, person, "
       "cropped, blurry, drop shadow, border, white body, pale body")
BNEG = "face, eyes, nose, mouth, whiskers, front view, facing the viewer, side view, profile, " + NEG
#  the subjects, from the batch prompts that drew the ROM's sprites (gen2.py for ROVERCUB, batch 13's q/*.json)
SUBJ = {
 "rovercub": ("a small robot puppy, a four-legged robot dog standing on all four legs, a boxy grey metal body, four short "
              "jointed metal legs with round paw feet, a big round robot head with floppy metal puppy ears and one big round "
              "camera lens eye, a short antenna tail, facing left three-quarter view",
              "a small robot puppy seen from behind, rear view, facing away from the viewer, the back of its big round "
              "robot head and its floppy metal ears, a boxy grey metal body, four short jointed metal legs, a short antenna tail",
              "its big round robot head, floppy metal ears, boxy metal body, four legs and short antenna tail"),
 "lodestar": ("a small glowing five pointed star between its tall antlers, a cute slender deer with big eyes standing, "
              "facing left three-quarter view",
              "a small glowing five pointed star between its tall antlers, a slender deer seen from behind, rear view, tall "
              "branching antlers, a short tail, no face, facing away from the viewer",
              "its tall branching antlers with the small glowing star between them, slender legs and short tail"),
 "illumined": ("a big round halo ring of light behind it, a cute white fluffy cat sitting with big calm eyes, facing left "
               "three-quarter view",
               "a big round halo ring of light behind it, a white fluffy cat sitting seen from behind, rear view, a fluffy "
               "tail, no face, facing away from the viewer",
               "its round halo ring of light, fluffy fur and fluffy tail"),
}
PFX = "pure white background, pixel art game sprite of a single cute creature, "


def call(path, body=None, raw=False, ctype="application/json", timeout=60):
    data = body if (body is None or isinstance(body, bytes)) else json.dumps(body).encode()
    req = urllib.request.Request(HOST + path, data=data, headers={"Content-Type": ctype} if data else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        out = r.read()
    return out if raw else (json.loads(out) if out.strip() else {})


def upload(path):
    b = uuid.uuid4().hex; name = "t452trial_" + os.path.basename(path)
    body = (("--%s\r\nContent-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/png\r\n\r\n"
             % (b, name)).encode() + open(path, "rb").read() +
            ("\r\n--%s\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--%s--\r\n" % (b, b)).encode())
    return call("/upload/image", body, ctype="multipart/form-data; boundary=%s" % b)["name"]


def mem():
    try:
        d = call("/system_stats", timeout=10)["devices"][0]; return round(d["vram_free"] / 2**30, 1)
    except Exception:
        return None


def rss():
    try:
        o = subprocess.run(["ssh", "-o", "BatchMode=yes", "roverbyte@roverbyteseer",
                            "ps -o rss= -p $(pgrep -f 'main.py --listen 0.0.0.0 --port 8008' | head -1); "
                            "memory_pressure | tail -1"], capture_output=True, text=True, timeout=20).stdout.split("\n")
        return round(int(o[0]) / 2**20, 1), o[1].strip()
    except Exception:
        return None, None


# ---- graphs ---------------------------------------------------------------------------------------------------------
def g_shaper(pos, neg, seed):
    return {"1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "pixelArtDiffusionXL_spriteShaper.safetensors"}},
            "2": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
            "3": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["1", 1]}},
            "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 512, "height": 512, "batch_size": 1}},
            "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "seed": seed,
                  "steps": 28, "cfg": 6.5, "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0, "latent_image": ["4", 0]}},
            "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
            "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "t452trial"}}}


KLEIN = {"B": ("flux-2-klein-9b-fp8.safetensors", "qwen_3_8b_fp8mixed.safetensors", None),
         "C": ("flux-2-klein-4b.safetensors", "qwen_3_4b.safetensors", ("klein4b_pixelart_limbicnation.safetensors", 1.0))}


def g_klein(arm, pos, seed, ref=None):
    unet, clip, lora = KLEIN[arm]
    g = {"1": {"class_type": "UNETLoader", "inputs": {"unet_name": unet, "weight_dtype": "default"}},
         "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": clip, "type": "flux2"}},
         "3": {"class_type": "VAELoader", "inputs": {"vae_name": "flux2-vae.safetensors"}},
         "4": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["2", 0]}},
         "9": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": 512, "height": 512, "batch_size": 1}},
         "10": {"class_type": "Flux2Scheduler", "inputs": {"steps": 4, "width": 512, "height": 512}},
         "11": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
         "12": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
         "14": {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["3", 0]}},
         "15": {"class_type": "SaveImage", "inputs": {"images": ["14", 0], "filename_prefix": "t452trial"}}}
    model = ["1", 0]
    if lora:
        g["20"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": model, "lora_name": lora[0], "strength_model": lora[1]}}
        model = ["20", 0]
    cond = ["4", 0]
    if ref:
        g["30"] = {"class_type": "LoadImage", "inputs": {"image": ref}}
        g["31"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["30", 0], "vae": ["3", 0]}}
        g["32"] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": cond, "latent": ["31", 0]}}
        cond = ["32", 0]
    g["5"] = {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": cond}}
    g["6"] = {"class_type": "CFGGuider", "inputs": {"model": model, "positive": cond, "negative": ["5", 0], "cfg": 1.0}}
    g["13"] = {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["12", 0], "guider": ["6", 0], "sampler": ["11", 0],
               "sigmas": ["10", 0], "latent_image": ["9", 0]}}
    return g


def g_zimage(pos, seed):
    return {"1": {"class_type": "UNETLoader", "inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}},
            "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2"}},
            "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
            "4": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["2", 0]}},
            "5": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["4", 0]}},
            "6": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.0}},
            "7": {"class_type": "EmptySD3LatentImage", "inputs": {"width": 512, "height": 512, "batch_size": 1}},
            "8": {"class_type": "KSampler", "inputs": {"model": ["6", 0], "positive": ["4", 0], "negative": ["5", 0], "seed": seed,
                  "steps": 8, "cfg": 1.0, "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1.0, "latent_image": ["7", 0]}},
            "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
            "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "t452trial"}}}


def run(g, out, rec):
    t0 = time.time()
    pid = call("/prompt", {"prompt": g, "client_id": "t452trial"})["prompt_id"]
    while True:
        time.sleep(1.5)
        h = call("/history/" + pid)
        if pid in h:
            h = h[pid]; break
        if time.time() - t0 > 900: raise SystemExit("timeout " + out)
    st = h.get("status", {})
    if st.get("status_str") == "error": raise SystemExit("ComfyUI error %s: %s" % (out, json.dumps(st)[:800]))
    im = [i for n in h["outputs"].values() for i in n.get("images", [])][0]
    png = call("/view?filename=%s&subfolder=%s&type=%s" % (im["filename"], im["subfolder"], im["type"]), raw=True, timeout=120)
    open(out + ".png", "wb").write(png)
    secs = round(time.time() - t0, 1)
    r_, pr = rss()
    rec.update(seconds=secs, vram_free_gb_after=mem(), comfy_rss_gb_after=r_, memory_pressure_after=pr,
               graph=g, host=HOST, comfyui=call("/system_stats")["system"]["comfyui_version"], made=time.strftime("%Y-%m-%d %H:%M:%S"))
    json.dump(rec, open(out + ".json", "w"), indent=1)
    print("%-38s %5.1fs  free %s GB  rss %s GB  %s" % (os.path.basename(out), secs, rec["vram_free_gb_after"], r_, pr), flush=True)


def gen(arms):
    os.makedirs(OUT + "/raw", exist_ok=True)
    for arm in arms:
        try: call("/free", {"unload_models": True, "free_memory": True})
        except Exception as e: print("free:", e)
        time.sleep(3)
        print("== arm", arm, ARMS[arm], "free before %s GB" % mem(), flush=True)
        for n, (fs, bs, keep) in SUBJ.items():
            for seed in SEEDS:
                f = "%s/raw/%s_%s_front_%d" % (OUT, arm, n, seed); b = "%s/raw/%s_%s_back_%d" % (OUT, arm, n, seed)
                front = PFX + fs + ", " + TAIL
                back = PFX + bs + ", " + BTAIL
                if arm == "C":
                    front = "pixel art sprite, chibi, " + front + ", game asset"
                if not os.path.exists(f + ".png"):
                    rec = dict(arm=arm, model=ARMS[arm], daemon=n, view="front", seed=seed, prompt=front, size=[512, 512])
                    if arm == "A": rec["negative"] = "rear view, " + NEG; g = g_shaper(front, rec["negative"], seed)
                    elif arm in "BC": g = g_klein(arm, front, seed)
                    else: g = g_zimage(front, seed)
                    run(g, f, rec)
                if not os.path.exists(b + ".png"):
                    if arm in "BC":   # the back drawn FROM this seed's front, as an image (ReferenceLatent)
                        back = ("Turn this exact creature around: the same creature seen from directly behind, rear view, facing "
                                "away from the viewer, the back of its head, no face visible, %s, the same size in the frame, "
                                "the same proportions, the same grey body and colours, the same pixel art style, black outline, "
                                "centered on a plain white background, full body, no shadow" % keep)
                        if arm == "C": back = "pixel art sprite, chibi, " + back + ", game asset"
                        rec = dict(arm=arm, model=ARMS[arm], daemon=n, view="back", seed=seed, prompt=back, size=[512, 512],
                                   reference=os.path.relpath(f + ".png", R))
                        g = g_klein(arm, back, seed, ref=upload(f + ".png"))
                    else:
                        rec = dict(arm=arm, model=ARMS[arm], daemon=n, view="back", seed=seed, prompt=back, size=[512, 512])
                        if arm == "A": rec["negative"] = BNEG; g = g_shaper(back, BNEG, seed)
                        else: g = g_zimage(back, seed)
                    run(g, b, rec)


# ---- reduction (reduce.py's steps, into trial/) and metrics --------------------------------------------------------
def grid_align(png):
    """Share of the subject's 8x8 blocks that are one flat colour (max channel std < 6): 100 = drawn on the 64px grid."""
    a = np.asarray(Image.open(png).convert("RGB"), dtype=float)
    bl = a.reshape(64, 8, 64, 8, 3).transpose(0, 2, 1, 3, 4).reshape(64, 64, 64, 3)
    sd = bl.std(axis=2).max(axis=2); mean = bl.mean(axis=2)
    subj = ~((mean > 225).all(axis=2) & (sd < 6))   # not flat background
    return round(100 * float(((sd < 6) & subj).sum()) / max(1, int(subj.sum())), 1)


def reduce_all():
    import gbs
    os.makedirs(OUT + "/clean", exist_ok=True); os.makedirs(OUT + "/reduced", exist_ok=True)
    S = json.load(open(R + "/companion/server/data/species.json")); BY = {v["name"].lower(): v for v in S.values()}
    M = {}
    for arm in ARMS:
        for n in SUBJ:
            slot = BY[n]["constant"].lower(); typ = gbs.primary_type(slot)
            for seed in SEEDS:
                key = "%s_%s_%d" % (arm, n, seed); pal = None; gf = None; m = dict(arm=arm, daemon=n, seed=seed, type=typ)
                for kind in ("front", "back"):
                    src = "%s/raw/%s_%s_%s_%d.png" % (OUT, arm, n, kind, seed)
                    if not os.path.exists(src): continue
                    rec = json.load(open(src[:-4] + ".json")); m[kind + "_seconds"] = rec["seconds"]
                    m[kind + "_grid"] = grid_align(src)
                    clean = "%s/clean/%s_%s.png" % (OUT, key, kind)
                    r = subprocess.run([PY, R + "/tools/cleandraft.py", src, clean, "--streaks"], capture_output=True, text=True)
                    if r.returncode:
                        r = subprocess.run([PY, R + "/tools/cleandraft.py", src, clean], capture_output=True, text=True)
                        m[kind + "_streaks"] = False
                    if r.returncode: m[kind + "_error"] = r.stderr[-300:]; continue
                    try:
                        grid, p = gbs.place_rich(clean, gbs.TYPE_COLOR[typ], shared=pal if kind == "back" else None)
                    except Exception as e:
                        m[kind + "_error"] = repr(e)[:300]; continue
                    if kind == "front": pal = p; gf = grid
                    else:   # silhouette agreement with the front, either way round (a back is often the front turned)
                        fm = np.array(gf) > 0; bm = np.array(grid) > 0
                        iou = lambda a, b: float((a & b).sum()) / max(1, int((a | b).sum()))
                        m["sil"] = round(max(iou(fm, bm), iou(fm, bm[:, ::-1])), 2)
                    gbs.write_png4("%s/reduced/%s_%s.png" % (OUT, key, kind), grid, p)
                    m.update({kind + "_" + k: v for k, v in measure(grid, p, typ).items()})
                if gf is not None:
                    ic, info = gbs.derive_icon(gf, pal)
                    gbs.write_png4("%s/reduced/%s_icon.png" % (OUT, key), ic, gbs.icon_palettes()[info[0]], 32, 64)
                    m["icon_palette"] = info[0]; m["icon_err"] = round(info[1])
                if m.get("front_px") and m.get("back_px"): m["ratio"] = round(m["back_px"] / m["front_px"], 2)
                M[key] = m; print(key, {k: v for k, v in m.items() if k not in ("arm", "daemon", "seed")}, flush=True)
    json.dump(M, open(OUT + "/metrics.json", "w"), indent=1)


TYPE_COLOR = {"FLYING": (206, 70, 70), "FIRE": (222, 158, 46), "GHOST": (92, 70, 118), "ICE": (166, 206, 222), "NORMAL": (198, 188, 168),
 "FIGHTING": (96, 122, 158), "POISON": (84, 92, 52), "GROUND": (158, 122, 78), "ROCK": (130, 130, 138), "BUG": (128, 148, 72), "WATER": (70, 106, 176),
 "GRASS": (92, 158, 96), "ELECTRIC": (86, 190, 190), "PSYCHIC": (176, 86, 158), "DRAGON": (53, 125, 110), "STEEL": (196, 170, 96), "DARK": (40, 40, 46)}
ACHRO = {"DARK", "ROCK", "NORMAL"}


def measure(grid, p, typ):
    """The roster walk's accent and type-hue shares (audit.py analyse), on a reduced grid."""
    hsv = lambda c: colorsys.rgb_to_hsv(*[v / 255 for v in c])
    hd = lambda a, b: min(abs(a - b), 1 - abs(a - b)) * 360
    th = hsv(TYPE_COLOR.get(typ, (128, 128, 128)))[0]
    px = [(x, y) for y in range(64) for x in range(64) if grid[y][x]]
    if not px: return {"px": 0}
    acc = ty = 0
    for x, y in px:
        h_, s_, v_ = hsv(tuple(p[grid[y][x]]) if grid[y][x] < len(p) else (0, 0, 0))   # past the palette: write_png4 pads black
        if typ in ACHRO:
            if s_ > 0.25 and v_ > 0.2: acc += 1
            else: ty += 1
        else:
            if s_ < 0.12 or v_ < 0.18: continue
            if hd(h_, th) <= 35: ty += 1
            elif s_ > 0.25: acc += 1
    xs = [x for x, _ in px]; ys = [y for _, y in px]
    edge = sum(1 for x, y in px if x in (0, 63) or y == 0)
    return {"px": len(px), "acc": round(100 * acc / len(px), 1), "typ": round(100 * ty / len(px), 1),
            "box": [min(xs), min(ys), max(xs), max(ys)], "edge": edge}


def score(m):
    """Lower is better: back/front size off 1, accents over 15, the type hue not leading, clipping, errors."""
    if not m.get("front_px") or not m.get("back_px"): return 99
    s = abs(1 - m["ratio"]) * 4 + (1 - m.get("sil", 0)) * 3
    for k in ("front", "back"):
        s += max(0, m[k + "_acc"] - 15) / 5 + (0 if m[k + "_typ"] >= m[k + "_acc"] else 1.5) + min(m[k + "_edge"], 16) / 8
    return round(s, 2)


# ---- sheets ----------------------------------------------------------------------------------------------------------
def sheet():
    from sheet_r2 import show, on, readpal, BY, G, PAPER, INK, GROUND, PARTY, RED
    RED = RED
    F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 15); FS = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
    M = json.load(open(OUT + "/metrics.json"))
    for k, m in M.items(): m["score"] = score(m)
    json.dump(M, open(OUT + "/metrics.json", "w"), indent=1)
    best = {}
    for arm in ARMS:
        for n in SUBJ:
            c = [m for m in M.values() if m["arm"] == arm and m["daemon"] == n]
            c = [m for m in c if m.get("front_px")]
            best[arm, n] = min(c, key=lambda m: m["score"]) if c else None

    def cell(paths, scale):   # front, back, icon side by side at a scale
        ims = []
        for i, (pth, pal) in enumerate(paths):
            if not pth or not os.path.exists(pth): ims.append(Image.new("RGB", ((64 if i < 2 else 32) * scale, 64 * scale), (200, 200, 200))); continue
            im = show(pth, pal, 32 if i == 2 else 64)
            ims.append(on(im, PARTY if i == 2 else GROUND, scale))
        w = sum(i.width for i in ims) + 6 * (len(ims) - 1); h = max(i.height for i in ims)
        c = Image.new("RGB", (w, h), PAPER); x = 0
        for i in ims: c.paste(i, (x, 0)); x += i.width + 6
        return c

    def drafts(arm, n, seed):
        b = "%s/reduced/%s_%s_%d_" % (OUT, arm, n, seed)
        return [(b + "front.png", None), (b + "back.png", None), (b + "icon.png", None)]

    # main sheet: per daemon, the ROM now and each arm's best seed, 2x and 4x
    colw = 160 * 4 + 40; rowh = 64 * 6 + 130
    W = 20 + 5 * colw; H = 70 + 3 * rowh + 60
    s = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 12), "T-452 pixel-model trial, 2026-11-06 -- DRAFTS, not in the ROM. Each arm's best of 3 seeds (7001-7003) by the roster "
           "walk's checks, after the existing reducer (cleandraft -> type ramp -> 64x64/16 colours, icon derived).", fill=INK, font=F)
    d.text((20, 34), "front | back | icon at 2x, then 4x.  ratio = back/front area (1.0 is the aim; the walk flagged under 0.5).  acc = accents % (cap 15).  "
           "typ = type-hue %.  grid = % of the raw 512's 8x8 blocks that are flat (on the 64px grid).  s = seconds per image.", fill=INK, font=FS)
    for r, n in enumerate(SUBJ):
        v = BY[n]; rom = G + v["constant"].lower()
        if not os.path.isdir(rom): rom = G + "nexus_" + n
        npal = readpal(rom + "/normal.pal"); y = 70 + r * rowh
        d.text((20, y), "%d %s" % (v["national"], v["name"]), fill=INK, font=F)
        cols = [("IN ROM now", [(rom + "/front.png", npal), (rom + "/back.png", npal), (rom + "/icon.png", None)], None)]
        for arm in ARMS:
            m = best[arm, n]
            cols.append(("%s  %s" % (arm, ARMS[arm]) + ("" if m else ": DID NOT RUN, fp8 cannot sample on MPS"), drafts(arm, n, m["seed"]) if m else [(None, None)] * 3, m))
        for c, (lab, paths, m) in enumerate(cols):
            x = 20 + c * colw; yy = y + 22
            d.text((x, yy), lab[:70], fill=RED if c else INK, font=FS); yy += 16
            if m:
                d.text((x, yy), "seed %d  ratio %.2f  acc %.0f/%.0f  typ %.0f/%.0f" % (m["seed"], m.get("ratio", 0), m.get("front_acc", 0),
                       m.get("back_acc", 0), m.get("front_typ", 0), m.get("back_typ", 0)), fill=INK, font=FS); yy += 14
                d.text((x, yy), "sil %.2f  grid %.0f/%.0f%%  s %.0f/%.0f  score %.1f" % (m.get("sil", 0), m.get("front_grid", 0), m.get("back_grid", 0),
                       m.get("front_seconds", 0), m.get("back_seconds", 0), m["score"]), fill=INK, font=FS)
            yy += 18
            c2 = cell(paths, 2); s.paste(c2, (x, yy)); c4 = cell(paths, 4); s.paste(c4, (x, yy + c2.height + 8))
    d.text((20, H - 50), "BY EYE (the score is a screen, not a verdict -- it ranks A's ILLUMINED first because its draft's coloured frame survived cleaning and was "
           "counted as the creature): C draws the same creature front and back in all three, keeps LODESTAR's star and ILLUMINED's halo, in the chibi look.", fill=INK, font=FS)
    d.text((20, H - 32), "A's ROVERCUB back is another robot and its LODESTAR back is the same side view again; D turns well but its white ILLUMINED was eaten "
           "by the background fill (white on white) and it is half C's speed.", fill=INK, font=FS)
    os.makedirs(OUT + "/sheets", exist_ok=True)
    s.save(OUT + "/sheets/trial_best.png"); print(OUT + "/sheets/trial_best.png", s.size)

    # every seed, 2x, with its numbers: one sheet
    colw2 = 160 * 2 + 30; rowh2 = 64 * 2 + 46
    W = 20 + (1 + 4 * 3) * colw2 // 1; H = 60 + 3 * rowh2 + 20
    s = Image.new("RGB", (20 + 13 * colw2, H), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 12), "T-452 pixel-model trial -- every seed, 2x, DRAFTS. Columns: IN ROM, then A 7001-7003, B, C, D. Under each: ratio, accents f/b, score.", fill=INK, font=F)
    for r, n in enumerate(SUBJ):
        v = BY[n]; rom = G + v["constant"].lower()
        if not os.path.isdir(rom): rom = G + "nexus_" + n
        npal = readpal(rom + "/normal.pal"); y = 40 + r * rowh2
        s.paste(cell([(rom + "/front.png", npal), (rom + "/back.png", npal), (rom + "/icon.png", None)], 2), (20, y + 18))
        d.text((20, y), v["name"] + " IN ROM", fill=INK, font=FS)
        c = 1
        for arm in ARMS:
            for seed in SEEDS:
                m = M.get("%s_%s_%d" % (arm, n, seed)); x = 20 + c * colw2
                d.text((x, y), "%s %d" % (arm, seed), fill=RED, font=FS)
                s.paste(cell(drafts(arm, n, seed), 2), (x, y + 18))
                if m: d.text((x, y + 18 + 128 + 4), "r %.2f  a %.0f/%.0f  s %.1f" % (m.get("ratio", 0), m.get("front_acc", 0), m.get("back_acc", 0), m["score"]), fill=INK, font=FS)
                c += 1
    s.save(OUT + "/sheets/trial_all_seeds.png"); print(OUT + "/sheets/trial_all_seeds.png", s.size)

    # the raw 512 drafts of each arm's best, small, so the model's own drawing is seen before the reducer
    s = Image.new("RGB", (20 + 4 * 2 * 266, 50 + 3 * 290), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 12), "T-452 pixel-model trial -- the raw drafts (512 shown at 256) of each arm's best seed, front and back, before reduction", fill=INK, font=F)
    for r, n in enumerate(SUBJ):
        for c, arm in enumerate(ARMS):
            m = best[arm, n]
            if not m:
                d.text((20 + 2 * c * 266, 40 + r * 290 + 18), "%s: did not run (klein 9B fp8 cannot sample on MPS)" % arm, fill=RED, font=FS); continue
            for k, kind in enumerate(("front", "back")):
                pth = "%s/raw/%s_%s_%s_%d.png" % (OUT, arm, n, kind, m["seed"])
                x = 20 + (2 * c + k) * 266; y = 40 + r * 290
                d.text((x, y), "%s %s %s %d" % (arm, n.upper(), kind, m["seed"]), fill=INK, font=FS)
                s.paste(Image.open(pth).convert("RGB").resize((256, 256), Image.LANCZOS), (x, y + 18))
    s.save(OUT + "/sheets/trial_raw.png"); print(OUT + "/sheets/trial_raw.png", s.size)


if __name__ == "__main__":
    a = sys.argv[1]
    if a == "gen": gen(sys.argv[2:] or list(ARMS))
    elif a == "reduce": reduce_all()
    elif a == "sheet": sheet()

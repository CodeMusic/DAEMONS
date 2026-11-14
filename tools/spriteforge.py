#!/usr/bin/env python3
"""Draft sprites on the local ComfyUI, reproducibly (T-131; vision.md 9.4).

    python3 tools/spriteforge.py t2i --out gfx/drafts/nibble_front --prompt "..." [--negative "..."] [--seed N]
                                     [--size 1024x1024] [--steps 28] [--cfg 6.5] [--sampler dpmpp_2m] [--scheduler karras]
    python3 tools/spriteforge.py i2i --out gfx/drafts/nibble_back --image path.png --prompt "..." [--denoise 0.6] ...
    python3 tools/spriteforge.py again gfx/drafts/nibble_front.json     # regenerate a draft exactly from its record
    python3 tools/spriteforge.py t2i ... --stop-at 4                    # decode the latent 4 steps in, still noise

    #  T-452's arm C: FLUX.2 klein 4B + a pixel-art LoRA, a back drawn FROM its own front by reference
    python3 tools/spriteforge.py t2i --model klein4b --lora klein4b_pixelart_limbicnation.safetensors:1.0 \\
        --size 512x512 --out gfx/drafts/x_front --prompt "pixel art sprite, chibi, ..."
    python3 tools/spriteforge.py t2i --model klein4b --lora klein4b_pixelart_limbicnation.safetensors:1.0 \\
        --size 512x512 --reference gfx/drafts/x_front.png --out gfx/drafts/x_back --prompt "... seen from behind ..."

--stop-at N STOPS THE SAMPLER EARLY and decodes what it has, leftover noise and all: a latent before it has
been resolved into anything. T-250 wants exactly that for what a player sees without the RESOLVER -- the
same seed without --stop-at is the thing it would have become.

THE SERVER. ComfyUI at http://roverbyteseer:8008 (override with SPRITEFORGE_HOST). When the batch's process exits it
unloads ComfyUI's models if nothing else is queued (POST /free; 2026-11-14, so FLUX does not sit beside ACE-Step on the
seer); SPRITEFORGE_KEEP_LOADED=1 skips that. TWO MODELS (--model):

  shaper   (the default, and everything before T-452's trial) the checkpoint
           `pixelArtDiffusionXL_spriteShaper.safetensors` -- the same model the pixelbyte skill wraps, driven here
           directly so a draft can be scripted, batched and rebuilt. 28 steps, cfg 6.5, dpmpp_2m / karras.
  klein4b  FLUX.2 klein 4B (Apache 2.0): `flux-2-klein-4b.safetensors`, the qwen_3_4b text encoder and the flux2
           VAE. 4 steps, cfg 1.0, euler on the Flux2Scheduler. It takes no negative (cfg 1 zeroes it: --negative
           is refused rather than silently ignored), and does no image-to-image by denoise -- it EDITS instead:
           --reference IMAGE (repeatable) hands it an image through ReferenceLatent, and the prompt says what to
           change. T-452's trial (gfx/drafts/t452/trial/, 2026-11-06) chose it with the Limbicnation pixel-art
           LoRA because a back drawn from its own front by reference is the same creature both ways round.

--lora NAME[:STRENGTH] (repeatable, strength 1.0 if left out) loads a LoRA from the server's loras folder: into
the model and the text encoder for shaper (LoraLoader), into the model only for klein4b (LoraLoaderModelOnly, as
its LoRAs are trained). Leave --model, --lora and --reference out and the graph sent is exactly the one this tool
always sent.

It is a DRAFTING instrument: 9.4 says nothing in a finished sprite is accidental, and a diffusion output is all
accident until it has been cleaned.

EVERY DRAFT CARRIES ITS OWN RECORD. Beside each PNG is a JSON with the prompt, negative, seed, size, steps, cfg,
sampler, scheduler, denoise, source image, the model and its files, every LoRA and its strength, every reference
image, the checkpoint and server version. A sprite whose seed was not written down cannot be made again, and
cannot be told apart from one made differently -- the n8n endpoint's own comment says the same about echoing which
backend drew it. A record made before --model existed is a shaper record, and `again` reads it as one.

NOTHING HERE WRITES INTO THE GAME. Drafts land in gfx/drafts/; `gbasprite.py` is what builds sprites, and
only from art that has been cleaned and approved on a contact sheet.

ComfyUI's API: POST /prompt with a node graph, poll GET /history/<id>, fetch GET /view. Image-to-image and
reference images upload with POST /upload/image first.
"""
import argparse, json, os, random, sys, time, urllib.parse, urllib.request, uuid

#  roverbyteseer by name -- at home and, through Tailscale, away (the user, 2026-10-09: "don't use .local, just
#  roverbyteseer")
HOST = os.environ.get("SPRITEFORGE_HOST", "http://roverbyteseer:8008")
CKPT = "pixelArtDiffusionXL_spriteShaper.safetensors"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#  each model's files and the settings it is drawn with when a flag leaves them out
MODELS = {
    "shaper": dict(files=dict(checkpoint=CKPT),
                   steps=28, cfg=6.5, sampler="dpmpp_2m", scheduler="karras"),
    "klein4b": dict(files=dict(unet="flux-2-klein-4b.safetensors", clip="qwen_3_4b.safetensors",
                               vae="flux2-vae.safetensors"),
                    steps=4, cfg=1.0, sampler="euler", scheduler="flux2"),
}


def call(path, body=None, raw=False, ctype="application/json", timeout=30):
    data = body if (body is None or isinstance(body, bytes)) else json.dumps(body).encode()
    req = urllib.request.Request(HOST + path, data=data, headers={"Content-Type": ctype} if data else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        out = r.read()
    return out if raw else json.loads(out)


def upload(path):
    boundary = uuid.uuid4().hex
    name = os.path.basename(path)
    body = (("--%s\r\nContent-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/png\r\n\r\n"
             % (boundary, name)).encode() + open(path, "rb").read() +
            ("\r\n--%s\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--%s--\r\n" % (boundary, boundary)).encode())
    return call("/upload/image", body, ctype="multipart/form-data; boundary=%s" % boundary)["name"]


def graph(p):
    """The node graph for a draft's settings: the model's own graph, its LoRAs, its references."""
    if p.get("model", "shaper") == "klein4b":
        return graph_klein(p)
    g = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": p["prompt"], "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": p["negative"], "clip": ["1", 1]}},
        "5": {"class_type": "KSampler", "inputs": {
            "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "seed": p["seed"], "steps": p["steps"],
            "cfg": p["cfg"], "sampler_name": p["sampler"], "scheduler": p["scheduler"], "denoise": p["denoise"]}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "spriteforge"}},
    }
    if p.get("stop_at"):
        g["5"] = {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "add_noise": "enable",
            "noise_seed": p["seed"], "steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"],
            "scheduler": p["scheduler"], "start_at_step": 0, "end_at_step": p["stop_at"],
            "return_with_leftover_noise": "enable"}}
    if p["mode"] == "i2i":
        g["8"] = {"class_type": "LoadImage", "inputs": {"image": p["uploaded"]}}
        g["4"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["8", 0], "vae": ["1", 2]}}
    else:
        w, h = p["size"]
        g["4"] = {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}}
    g["5"]["inputs"]["latent_image"] = ["4", 0]
    #  LoRAs chain between the checkpoint and everything that reads its model and text encoder
    model, clip = ["1", 0], ["1", 1]
    for i, (name, strength) in enumerate(p.get("loras") or []):
        n = str(20 + i)
        g[n] = {"class_type": "LoraLoader", "inputs": {"model": model, "clip": clip, "lora_name": name,
                                                       "strength_model": strength, "strength_clip": strength}}
        model, clip = [n, 0], [n, 1]
    g["2"]["inputs"]["clip"] = clip
    g["3"]["inputs"]["clip"] = clip
    g["5"]["inputs"]["model"] = model
    return g


def graph_klein(p):
    """FLUX.2 klein 4B: T-452 trial arm C's graph (gfx/drafts/t452/trial/trial.py g_klein), node for node."""
    f = MODELS["klein4b"]["files"]
    w, h = p["size"]
    g = {"1": {"class_type": "UNETLoader", "inputs": {"unet_name": f["unet"], "weight_dtype": "default"}},
         "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": f["clip"], "type": "flux2"}},
         "3": {"class_type": "VAELoader", "inputs": {"vae_name": f["vae"]}},
         "4": {"class_type": "CLIPTextEncode", "inputs": {"text": p["prompt"], "clip": ["2", 0]}},
         "9": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
         "10": {"class_type": "Flux2Scheduler", "inputs": {"steps": p["steps"], "width": w, "height": h}},
         "11": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": p["sampler"]}},
         "12": {"class_type": "RandomNoise", "inputs": {"noise_seed": p["seed"]}},
         "14": {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["3", 0]}},
         "15": {"class_type": "SaveImage", "inputs": {"images": ["14", 0], "filename_prefix": "spriteforge"}}}
    model = ["1", 0]
    for i, (name, strength) in enumerate(p.get("loras") or []):
        n = str(20 + i)
        g[n] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": model, "lora_name": name, "strength_model": strength}}
        model = [n, 0]
    cond = ["4", 0]
    for i, up in enumerate(p.get("uploaded_refs") or []):
        n = 30 + 3 * i
        g[str(n)] = {"class_type": "LoadImage", "inputs": {"image": up}}
        g[str(n + 1)] = {"class_type": "VAEEncode", "inputs": {"pixels": [str(n), 0], "vae": ["3", 0]}}
        g[str(n + 2)] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": cond, "latent": [str(n + 1), 0]}}
        cond = [str(n + 2), 0]
    g["5"] = {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": cond}}
    g["6"] = {"class_type": "CFGGuider", "inputs": {"model": model, "positive": cond, "negative": ["5", 0], "cfg": p["cfg"]}}
    g["13"] = {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["12", 0], "guider": ["6", 0], "sampler": ["11", 0],
               "sigmas": ["10", 0], "latent_image": ["9", 0]}}
    return g


def check(p):
    """Refuse a combination the model would not honour, rather than draw something the record misdescribes."""
    m = p.get("model", "shaper")
    if m not in MODELS:
        raise SystemExit("unknown --model %r (one of %s)" % (m, ", ".join(MODELS)))
    if m == "shaper" and p.get("references"):
        raise SystemExit("--reference is klein4b's (ReferenceLatent); shaper takes an image by i2i --image")
    if m == "klein4b":
        if p["mode"] == "i2i":
            raise SystemExit("klein4b does no denoise image-to-image: use t2i with --reference IMAGE")
        if p.get("negative"):
            raise SystemExit("klein4b draws at cfg 1, where a negative prompt does nothing: leave --negative out")
        if p.get("stop_at"):
            raise SystemExit("--stop-at is shaper's (KSamplerAdvanced)")
        if p.get("scheduler") != "flux2":
            raise SystemExit("klein4b's sigmas come from the Flux2Scheduler: leave --scheduler out")


def resolve(p):
    """A flag left out takes the model's own setting; the record then holds what was actually used."""
    m = MODELS[p.get("model", "shaper")]
    for k in ("steps", "cfg", "sampler", "scheduler"):
        if p.get(k) is None:
            p[k] = m[k]
    return p


_FREE_ARMED = False


def free_when_idle():
    """Unload ComfyUI's models once this process's batch is done, as the hub does after its own paintings: POST /free
    {unload_models, free_memory}, but only when ComfyUI's queue is empty, so another client's job keeps its model. FLUX
    left loaded (~22 GB) beside ACE-Step filled roverbyteseer's 32 GB and swap on 2026-11-14 (the companion lane's
    report). Registered at exit by run(), so a tool that paints many images in a loop frees once, at the end. Never fatal."""
    try:
        q = call("/queue", timeout=10)
        if q.get("queue_running") or q.get("queue_pending"):
            print("  (spriteforge: ComfyUI still busy; models left loaded)")
            return
        call("/free", {"unload_models": True, "free_memory": True}, raw=True, timeout=30)
        print("  (spriteforge: ComfyUI's models unloaded)")
    except Exception as e:  # the painting is already saved; a failed unload must not fail the batch
        print("  (spriteforge: could not unload ComfyUI's models: %s)" % e)


def run(p):
    global _FREE_ARMED
    if not _FREE_ARMED and not os.environ.get("SPRITEFORGE_KEEP_LOADED"):
        import atexit
        atexit.register(free_when_idle)
        _FREE_ARMED = True
    p.setdefault("model", "shaper")
    p.setdefault("loras", [])
    p.setdefault("references", [])
    p["loras"] = [list(l) for l in p["loras"]]
    resolve(p)
    check(p)
    here = lambda f: os.path.join(ROOT, f) if not os.path.isabs(f) else f
    if p["mode"] == "i2i":
        p["uploaded"] = upload(here(p["image"]))
    if p["references"]:
        p["uploaded_refs"] = [upload(here(f)) for f in p["references"]]
    sent = call("/prompt", {"prompt": graph(p), "client_id": "spriteforge"})
    pid, t0 = sent["prompt_id"], time.time()
    while True:
        h = call("/history/%s" % pid)
        if pid in h and h[pid].get("outputs"):
            break
        if pid in h and h[pid].get("status", {}).get("status_str") == "error":
            raise SystemExit("ComfyUI reported an error: %s" % json.dumps(h[pid]["status"])[:600])
        if time.time() - t0 > 600:
            raise SystemExit("gave up after 600s waiting for %s" % pid)
        time.sleep(2)
    img = [i for o in h[pid]["outputs"].values() for i in o.get("images", [])][0]
    png = call("/view?" + urllib.parse.urlencode({"filename": img["filename"], "subfolder": img["subfolder"], "type": img["type"]}), raw=True)
    out = here(p["out"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out + ".png", "wb").write(png)
    record = {k: v for k, v in p.items() if k not in ("uploaded", "uploaded_refs")}
    files = MODELS[p["model"]]["files"]
    record.update(checkpoint=files.get("checkpoint", files.get("unet")), model_files=files, host=HOST,
                  seconds=round(time.time() - t0, 1),
                  comfyui=call("/system_stats")["system"]["comfyui_version"], made=time.strftime("%Y-%m-%d %H:%M:%S"))
    json.dump(record, open(out + ".json", "w"), indent=1)
    print("  %s.png  (%s, seed %d, %.0fs)" % (p["out"], p["model"], p["seed"], record["seconds"]))
    return out + ".png"


def lora(v):
    name, _, s = v.rpartition(":") if v.rsplit(":", 1)[-1].replace(".", "", 1).lstrip("-").isdigit() else (v, "", "")
    return [name, float(s) if s else 1.0]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    for mode in ("t2i", "i2i"):
        s = sub.add_parser(mode)
        s.add_argument("--out", required=True)
        s.add_argument("--prompt", required=True)
        s.add_argument("--negative", default="")
        s.add_argument("--seed", type=int, default=None)
        s.add_argument("--model", default="shaper", choices=sorted(MODELS))
        s.add_argument("--lora", type=lora, action="append", default=[], metavar="NAME[:STRENGTH]")
        s.add_argument("--steps", type=int, default=None, help="28 for shaper, 4 for klein4b")
        s.add_argument("--cfg", type=float, default=None, help="6.5 for shaper, 1.0 for klein4b")
        s.add_argument("--sampler", default=None, help="dpmpp_2m for shaper, euler for klein4b")
        s.add_argument("--scheduler", default=None, help="karras for shaper (klein4b: the Flux2Scheduler)")
        s.add_argument("--stop-at", type=int, default=None, dest="stop_at")
        if mode == "t2i":
            s.add_argument("--size", default="1024x1024")
            s.add_argument("--reference", action="append", default=[], metavar="IMAGE",
                           help="klein4b: an image to edit from (ReferenceLatent); repeatable")
        else:
            s.add_argument("--image", required=True)
            s.add_argument("--denoise", type=float, default=0.6)
    again = sub.add_parser("again")
    again.add_argument("record")
    a = ap.parse_args()
    if a.mode == "again":
        p = json.load(open(a.record))
        p["size"] = tuple(p["size"]) if p.get("size") else None
        run(p)
        return
    p = dict(mode=a.mode, out=a.out, prompt=a.prompt, negative=a.negative,
             seed=a.seed if a.seed is not None else random.randrange(2 ** 32), steps=a.steps, cfg=a.cfg,
             sampler=a.sampler, scheduler=a.scheduler, denoise=getattr(a, "denoise", 1.0), stop_at=a.stop_at,
             model=a.model, loras=a.lora, references=getattr(a, "reference", []))
    if a.mode == "t2i":
        p["size"] = tuple(int(v) for v in a.size.split("x"))
    else:
        p["image"] = a.image
    run(p)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Draft sprites on the local ComfyUI, reproducibly (T-131; vision.md 9.4).

    python3 tools/spriteforge.py t2i --out gfx/drafts/nibble_front --prompt "..." [--negative "..."] [--seed N]
                                     [--size 1024x1024] [--steps 28] [--cfg 6.5] [--sampler dpmpp_2m] [--scheduler karras]
    python3 tools/spriteforge.py i2i --out gfx/drafts/nibble_back --image path.png --prompt "..." [--denoise 0.6] ...
    python3 tools/spriteforge.py again gfx/drafts/nibble_front.json     # regenerate a draft exactly from its record
    python3 tools/spriteforge.py t2i ... --stop-at 4                    # decode the latent 4 steps in, still noise

--stop-at N STOPS THE SAMPLER EARLY and decodes what it has, leftover noise and all: a latent before it has
been resolved into anything. T-250 wants exactly that for what a player sees without the RESOLVER -- the
same seed without --stop-at is the thing it would have become.

THE SERVER. ComfyUI at http://roverbyteseer.local:8008 (override with SPRITEFORGE_HOST), checkpoint
`pixelArtDiffusionXL_spriteShaper.safetensors` -- the same model the pixelbyte skill wraps, driven here
directly so a draft can be scripted, batched and rebuilt. It is a DRAFTING instrument: 9.4 says nothing
in a finished sprite is accidental, and a diffusion output is all accident until it has been cleaned.

EVERY DRAFT CARRIES ITS OWN RECORD. Beside each PNG is a JSON with the prompt, negative, seed, size,
steps, cfg, sampler, scheduler, denoise, source image, checkpoint and server version. A sprite whose seed
was not written down cannot be made again, and cannot be told apart from one made differently -- the
n8n endpoint's own comment says the same about echoing which backend drew it.

NOTHING HERE WRITES INTO THE GAME. Drafts land in gfx/drafts/; `gbasprite.py` is what builds sprites, and
only from art that has been cleaned and approved on a contact sheet.

ComfyUI's API: POST /prompt with a node graph, poll GET /history/<id>, fetch GET /view. Image-to-image
uploads its source with POST /upload/image first.
"""
import argparse, json, os, random, sys, time, urllib.parse, urllib.request, uuid

HOST = os.environ.get("SPRITEFORGE_HOST", "http://roverbyteseer.local:8008")
CKPT = "pixelArtDiffusionXL_spriteShaper.safetensors"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    return g


def run(p):
    if p["mode"] == "i2i":
        p["uploaded"] = upload(os.path.join(ROOT, p["image"]) if not os.path.isabs(p["image"]) else p["image"])
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
    out = os.path.join(ROOT, p["out"]) if not os.path.isabs(p["out"]) else p["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out + ".png", "wb").write(png)
    record = {k: v for k, v in p.items() if k != "uploaded"}
    record.update(checkpoint=CKPT, host=HOST, seconds=round(time.time() - t0, 1),
                  comfyui=call("/system_stats")["system"]["comfyui_version"], made=time.strftime("%Y-%m-%d %H:%M:%S"))
    json.dump(record, open(out + ".json", "w"), indent=1)
    print("  %s.png  (seed %d, %.0fs)" % (p["out"], p["seed"], record["seconds"]))
    return out + ".png"


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    for mode in ("t2i", "i2i"):
        s = sub.add_parser(mode)
        s.add_argument("--out", required=True)
        s.add_argument("--prompt", required=True)
        s.add_argument("--negative", default="")
        s.add_argument("--seed", type=int, default=None)
        s.add_argument("--steps", type=int, default=28)
        s.add_argument("--cfg", type=float, default=6.5)
        s.add_argument("--sampler", default="dpmpp_2m")
        s.add_argument("--scheduler", default="karras")
        s.add_argument("--stop-at", type=int, default=None, dest="stop_at")
        if mode == "t2i":
            s.add_argument("--size", default="1024x1024")
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
             sampler=a.sampler, scheduler=a.scheduler, denoise=getattr(a, "denoise", 1.0), stop_at=a.stop_at)
    if a.mode == "t2i":
        p["size"] = tuple(int(v) for v in a.size.split("x"))
    else:
        p["image"] = a.image
    run(p)


if __name__ == "__main__":
    main()

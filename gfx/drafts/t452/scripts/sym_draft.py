"""T-452 SYMBOL drafts (2026-10-28, seed 6800, dir y): per form, image-to-image from its guide (guide.py) at 0.6 and 0.72
(SEED+21, +22), one job at a time, waiting for an idle queue before each and retrying a dropped network (batch.py's run).
    draft.py [--dn=0.6,0.72] [--seeds=21,22] FORM ..."""
import sys, os, json, subprocess, time, random, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symlib import *
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3"); SEED = 6800
opt = {a.split("=", 1)[0][2:]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--")}
forms = [a for a in sys.argv[1:] if not a.startswith("--")] or FORMS
DN = [float(v) for v in opt.get("dn", "0.6,0.72").split(",")]; SD = [int(v) for v in opt.get("seeds", "21,22").split(",")]
HEAD = "pure white background, pixel art game sprite of a single cute creature, "
STY = ("chibi, soft shading, mostly greyscale, medium grey body with light grey highlights and dark grey shading, "
       "only small touches of colour, clean black outline, isolated on white, centered, large in the frame, no shadow")
NEG = ("photorealistic, 3d render, colorful, rainbow, colored background, grey background, dark background, scenery, floor, "
       "ground, watermark, multiple creatures, two creatures, duplicate, human, person, cropped, blurry, drop shadow, border, "
       "frame, white body, pale body, pink, purple, many eyes, two eyes, mouth full of teeth, words, caption, small letters")
def name(f): return {"exclamation_mark": "exclamation mark", "question_mark": "question mark"}.get(f, "capital letter " + f.upper())
def prompt(f):
    return (HEAD + f"a little living glyph, its whole body is a thick rounded {name(f)} '{GLYPH[f]}', the shape of the "
            f"{name(f)} is clearly readable, one big round eye on it, two tiny stubby feet, a cute small creature, " + STY)
def idle():
    for _ in range(400):
        try:
            q = json.loads(urllib.request.urlopen("http://roverbyteseer:8008/queue", timeout=15).read())
            if len(q["queue_pending"]) + len(q["queue_running"]) == 0: return
        except Exception as e: print("queue?", e, flush=True)
        time.sleep(8 + random.random() * 6)
def run(a):
    out = a[a.index("--out") + 1]
    for k in range(30):
        if os.path.exists(out + ".png"): return
        idle()
        t = subprocess.run([PY, "tools/spriteforge.py"] + a, capture_output=True, text=True, cwd=R)
        print(os.path.basename(out), t.stdout.strip()[-60:], t.stderr.strip()[-300:], flush=True)
        if not os.path.exists(out + ".png"): time.sleep(60)
for f in forms:
    for dn, s in zip(DN, SD):
        run(["i2i", "--seed", str(SEED + s), "--denoise", str(dn), "--image", f"{D}/src/{f}_guide.png",
             "--out", f"{D}/{f}_front_i2i_{SEED + s}", "--prompt", prompt(f), "--negative", NEG])
print("ALL-DONE", flush=True)

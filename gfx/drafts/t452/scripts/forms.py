"""T-452 forms (the user, 2026-10-28): PROTEUS's three forms (hooded, ALL EDGES, SHELL) and OVERLOADED's three weather
forms (sunny, rainy, snowy), by the charm recipe (batch.py's prompt pieces), seed 6900, dir z. One job at a time on an
idle queue; a dropped network retried every 60 s (batch.py's run()).

    forms.py ov          OVERLOADED's weathers: i2i from batch 18's chosen 512 draft (its new normal form) at 0.66 and
                         0.76 (SEED+21, +22), and two t2i (SEED+1, +2), per weather
    forms.py pro         PROTEUS hooded: two t2i chibi (SEED+1, +2), i2i from today's hooded front at 0.8, 0.85 (+21, +22)
    forms.py proforms    ALL EDGES and SHELL: i2i from the CHOSEN new hooded front (choose.json "proteus") at 0.7 and 0.8
                         (+61, +62), and from today's edged / shell front at 0.8 (+21)
Writes only under the work dir (T452_ROOT)."""
import json, os, subprocess, sys, time, random, urllib.request
import numpy as np
from PIL import Image
W = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452forms_work"
D = W + "/z"; R = "/Users/christopherhicks/Projects/DAEMONS"; PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
B18 = W + "/../t452b18_work/w"
SEED = 6900
os.makedirs(D + "/src", exist_ok=True); os.chdir(R)

HEAD = "pure white background, pixel art game sprite of a single cute creature, "
G = ("full body, chibi proportions, big round head, large expressive eyes, soft shading, mostly greyscale, "
     "medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
     "clean black outline, isolated on white, centered, large in the frame, no shadow, no text")
GC = "facing left three-quarter view, " + G
N = ("photorealistic, 3d render, colorful, rainbow, colored background, grey background, dark background, scenery, "
     "floor, ground, text, letters, watermark, multiple creatures, two creatures, duplicate, human, person, cropped, "
     "blurry, drop shadow, border, white body, pale body")

def idle():
    for _ in range(240):
        try:
            q = json.loads(urllib.request.urlopen("http://roverbyteseer:8008/queue", timeout=15).read())
            if len(q["queue_pending"]) + len(q["queue_running"]) == 0: return
        except Exception as e:
            print("queue?", e, flush=True)
        time.sleep(8 + random.random() * 6)

def run(a):
    out = a[a.index("--out") + 1]
    for k in range(30):
        if os.path.exists(out + ".png"): return
        idle()
        t = subprocess.run([PY, "tools/spriteforge.py"] + a, capture_output=True, text=True)
        print(out[-60:], t.stdout.strip()[-60:], t.stderr.strip()[-300:], flush=True)
        if not os.path.exists(out + ".png"): time.sleep(60)

def src512(path, name):
    """a 64-grid (or any) picture on white at 512, nearest -- the i2i source"""
    dst = f"{D}/src/{name}_512.png"
    im = Image.open(path).convert("RGBA")
    if im.width != 512:
        if im.width != 64 or im.height != 64: im = im.resize((64, 64), Image.LANCZOS)
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
        bg.convert("RGB").resize((512, 512), Image.NEAREST).save(dst)
    else:
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); bg.convert("RGB").save(dst)
    return dst

def half(path, bottom):
    """one 64x64 half of a stacked 64x128 engine sheet, through its palette, transparent at index 0"""
    im = Image.open(path); a = np.array(im); rgba = np.array(im.convert("RGBA")); rgba[a == 0, 3] = 0
    return Image.fromarray(rgba[64:128] if bottom else rgba[:64])

def job(kind, name, seed, prompt, neg, image=None, dn=None):
    out = f"{D}/{name}_{seed}" if kind == "t2i" else f"{D}/{name}_i2i_{seed}"
    a = [kind, "--seed", str(seed), "--out", out, "--prompt", HEAD + prompt + ", " + GC, "--negative", neg]
    if kind == "t2i": a[1:1] = ["--size", "512x512"]
    else: a += ["--denoise", str(dn), "--image", image]
    run(a)

OV_FACE = "the same cute round fluffy cloud creature with big round shiny eyes and soft pink cheeks"
OV = {
    "sunny": ("a ring of round puffy sun rays all around its head like a sunflower, glowing warm",
              OV_FACE + ", puffed up warm and round like a little smiling sun, sunny weather"),
    "rainy": ("its body drawn up into one big teardrop raindrop shape with a pointed top, two small raindrops falling beside it",
              OV_FACE + ", turned into a cute raindrop, wet and shiny, rainy weather"),
    "snowy": ("a frosty snow cap with a curl of frost on top and short icicles hanging from its bottom edge",
              OV_FACE + ", frozen into a cute snow cloud, fluffy and frosty, snowy weather"),
}
OV_NEG = "rear view, angry, scary, sharp teeth, " + N

def ov():
    base = src512(f"{B18}/overloaded_front_i2i_6622.png", "overloaded_b18")
    for w, (key, front) in OV.items():
        p = key + ", " + front
        for k, dn in enumerate((0.66, 0.76)):
            job("i2i", f"overloaded_{w}_front", SEED + 21 + k, p, OV_NEG, base, dn)
        for k in range(2):
            job("t2i", f"overloaded_{w}_front", SEED + 1 + k, p, OV_NEG)

PRO_KEY = "a deep pointed hood pulled over its head, a shadowed face with one glowing round eye, a long ragged cloak"
PRO_FRONT = "a cute small hooded shapeshifter spirit creature, two thin bladed arms held low at its sides"
PRO_NEG = "rear view, human, girl, boy, knight, sword, weapon, gun, " + N
EDGE = ("its hood thrown back off its head, both arms raised high as two long sharp blades, every edge sharp, "
        "its cloak flared out into jagged points, " + "a cute small shapeshifter spirit creature with one glowing round eye")
SHELL = ("curled up tight inside its hood drawn shut like a cocoon, a smooth closed egg-shaped shell with seams, "
         "one small round glowing window eye, no arms, no legs, " + "a cute small shapeshifter spirit creature")

def pro():
    base = src512(f"{R}/gfx/daemons/proteus_front.png", "proteus_today")
    p = PRO_KEY + ", " + PRO_FRONT
    for k in range(2): job("t2i", "proteus_front", SEED + 1 + k, p, PRO_NEG)
    for k, dn in enumerate((0.8, 0.85)): job("i2i", "proteus_front", SEED + 21 + k, p, PRO_NEG, base, dn)

def proforms():
    ch = json.load(open(D + "/choose.json"))["proteus"]["front"]
    new = src512(f"{D}/{ch}", "proteus_newfront")
    for name, prompt, today in (("proteus_edges_front", EDGE, "proteus_front_attack.png"),
                                ("proteus_shell_front", SHELL, "proteus_front_defense.png")):
        for k, dn in enumerate((0.7, 0.8)):
            job("i2i", name, SEED + 61 + k, prompt, PRO_NEG, new, dn)
        job("i2i", name, SEED + 21, prompt, PRO_NEG, src512(f"{R}/gfx/daemons/{today}", name + "_today"), 0.8)

if __name__ == "__main__":
    if sys.argv[1] in ("ov", "pro", "proforms"): {"ov": ov, "pro": pro, "proforms": proforms}[sys.argv[1]]()
    print("ALL-DONE", flush=True)

#  round 2 (the i2i from the new hooded front would not change its pose): text-to-image with the hooded draft's own
#  look named (white pointed hood, dark face, ragged brown cloak), SEED+71, +72
LOOK = "a white pointed hood, a dark shadowed face with two small glowing eyes, a ragged brown cloak"
def proforms2():
    for name, prompt in (("proteus_edges_front", "both thin arms raised high above its head as two long sharp blades, " + LOOK +
                          ", a cute small hooded shapeshifter spirit creature, all edges and points"),
                         ("proteus_shell_front", "curled up tight inside its cloak and hood drawn shut like a round cocoon, egg-shaped, "
                          "no arms, no legs, only its two small glowing eyes peeking out, " + LOOK + ", a cute small hooded shapeshifter spirit creature")):
        for k in range(2): job("t2i", name, SEED + 71 + k, prompt, PRO_NEG)

if __name__ == "__main__" and sys.argv[1] == "proforms2":
    proforms2(); print("ALL-DONE2", flush=True)

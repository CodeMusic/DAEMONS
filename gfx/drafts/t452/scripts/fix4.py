"""T-452 batch 4's follow-ups (the user, 2026-10-27): STACK redrawn as a round boulder, QUORUM as three pods.

    fix4.py gen      the drafts (one job at a time): STACK t2i 5261/5262, i2i from today's front 0.8/0.85 5263/5264
                     (the new wording); QUORUM t2i 5265-5268 (three pods: today's four would come back by i2i)
    fix4.py backs    the chosen new fronts (fix4.json) turned, rear-view prompt, 0.75 = 5271, 0.85 = 5272
"""
import json, os, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from subjects import S
R = "/Users/christopherhicks/Projects/DAEMONS"; T = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452"); D = T + "/g"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
HEAD = "pure white background, pixel art game sprite of a single cute creature, "
G = ("full body, chibi proportions, big round head, large expressive eyes, soft shading, mostly greyscale, "
     "medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
     "clean black outline, isolated on white, centered, large in the frame, no shadow, no text")
GC = "facing left three-quarter view, " + G
GB = ("full body, chibi proportions, seen from behind, soft shading, mostly greyscale, "
      "medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, "
      "centered, large in the frame, no shadow, no text")
GBC = "rear view, seen from behind, facing away from the viewer, " + GB
N = ("photorealistic, 3d render, colorful, rainbow, colored background, grey background, dark background, scenery, "
     "floor, ground, text, letters, watermark, multiple creatures, two creatures, duplicate, human, person, cropped, "
     "blurry, drop shadow, border, white body, pale body")
NB = "face, eyes, nose, mouth, front view, facing the viewer, side view, profile, " + N
F = {
 "stack": dict(key="its whole body one big round cracked grey boulder",
   front="a cute round rocky boulder creature, two big round boulder fists on short stone arms, small stern eyes in the boulder, stubby stone feet, chips and cracks in the rock",
   neg="muscles, muscular, abs, bodybuilder, humanoid, tall, robot, girl, human",
   back="a round rocky boulder creature seen from behind, the round cracked back of the boulder, two big round boulder fists at its sides, stubby stone feet"),
 "quorum": dict(key="exactly three round metal pods stuck together in a triangle, two side by side below and one on top",
   front="each of the three pods with one single big round camera lens eye, floating, a cute little cluster",
   neg="four, four pods, quad, diamond, one creature with a face, mouth, arms, legs, grapes, bubbles, frog, girl, human",
   back="three round metal pods stuck together in a triangle seen from behind, smooth plain metal backs, no eyes"),
}

def run(a):
    out = a[a.index("--out") + 1]
    if os.path.exists(out + ".png"): return
    t = subprocess.run([PY, "tools/spriteforge.py"] + a, capture_output=True, text=True)
    print(out.split("/")[-1], t.stdout.strip()[-40:], t.stderr.strip()[-300:], flush=True)

def gen():
    os.chdir(R)
    s = F["stack"]; fp = HEAD + s["key"] + ", " + s["front"] + ", " + GC; fneg = "rear view, " + s["neg"] + ", " + N
    for k in range(2):
        run(["t2i", "--size", "512x512", "--seed", str(5261 + k), "--out", f"{D}/stack_front_{5261 + k}", "--prompt", fp, "--negative", fneg])
    for k, dn in enumerate((0.8, 0.85)):
        run(["i2i", "--seed", str(5263 + k), "--denoise", str(dn), "--image", f"{D}/src/stack_front_512.png",
             "--out", f"{D}/stack_front_i2i_{5263 + k}", "--prompt", fp, "--negative", fneg])
    q = F["quorum"]; fp = HEAD + q["key"] + ", " + q["front"] + ", " + GC; fneg = "rear view, " + q["neg"] + ", " + N
    for k in range(4):
        run(["t2i", "--size", "512x512", "--seed", str(5265 + k), "--out", f"{D}/quorum_front_{5265 + k}", "--prompt", fp, "--negative", fneg])

F2 = {"stack": ("its whole body one single big round grey boulder like a rock ball, two big round boulder fists raised up in front of it",
                "a cute boulder creature, small stern eyes in the rock, stubby stone feet, cracks and chips", 5281),
      "quorum": ("three identical round grey metal spheres stacked in a little pyramid, two at the bottom touching and one balanced on top",
                 "each sphere with one big round camera lens eye in its middle, a cute robot cluster floating", 5285)}

def gen2():
    """a second wording each: STACK's fists named first; QUORUM's three spheres as a pyramid"""
    os.chdir(R)
    for n, (key, fr, seed) in F2.items():
        fp = HEAD + key + ", " + fr + ", " + GC; fneg = "rear view, frame, border, card, " + F[n]["neg"] + ", " + N
        for k in range(4):
            run(["t2i", "--size", "512x512", "--seed", str(seed + k), "--out", f"{D}/{n}_front_{seed + k}", "--prompt", fp, "--negative", fneg])

def backs():
    os.chdir(R); ch = json.load(open(D + "/fix4.json"))
    for n, fr in ch.items():
        s = F[n]; src = f"{D}/src/{n}_newfront5_512.png"; Image.open(f"{D}/{fr}").convert("RGB").save(src)
        bp = HEAD + s["key"] + ", " + s["back"] + ", " + GBC; bneg = "girl, hair, " + s["neg"] + ", " + NB
        for k, dn in enumerate((0.75, 0.85)):
            run(["i2i", "--seed", str(5271 + k), "--denoise", str(dn), "--image", src,
                 "--out", f"{D}/{n}_back_fromfront_{5271 + k}", "--prompt", bp, "--negative", bneg])

if __name__ == "__main__":
    {"gen": gen, "gen2": gen2, "backs": backs}[sys.argv[1]]()

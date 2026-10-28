"""T-452 batch 8: option drafts for two of the user's questions (seeds 566x), into k/. One stage per call.

    extra8.py deadlock2   DEADLOCK as TWO (its INDEX entry: "Two of them are each waiting for the other to move first")
    extra8.py starrstar   STARR apart from the PRIMER deer: a stag whose antlers curl back into a ring round a small star"""
import os, sys, subprocess
R = "/Users/christopherhicks/Projects/DAEMONS"; PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
D = os.environ["T452_ROOT"] + "/k"
HEAD = "pure white background, pixel art game sprite, "
G = ("full body, chibi proportions, big round heads, large expressive eyes, soft shading, mostly greyscale, "
     "medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
     "clean black outline, isolated on white, centered, large in the frame, no shadow, no text, facing left three-quarter view")
N = ("photorealistic, 3d render, colorful, rainbow, colored background, grey background, dark background, scenery, "
     "floor, ground, text, letters, watermark, human, person, cropped, blurry, drop shadow, border")
def run(seed, out, prompt, neg):
    if os.path.exists(f"{D}/{out}.png"): return
    t = subprocess.run([PY, "tools/spriteforge.py", "t2i", "--size", "512x512", "--seed", str(seed), "--out", f"{D}/{out}",
                        "--prompt", prompt, "--negative", neg], capture_output=True, text=True, cwd=R)
    print(out, t.stdout.strip()[-80:], t.stderr.strip()[-300:], flush=True)
st = sys.argv[1]
if st == "deadlock2":
    p = HEAD + ("two cute round stone creatures sitting side by side pressed together shoulder to shoulder, each with a big "
                "padlock hanging on its chest, one chain looped round both of them, sleepy closed eyes, stubby arms folded, " + G)
    for k in range(2): run(5661 + k, f"deadlock_front_two_{5661 + k}", p, N + ", three creatures, girl, bear, snorlax")
if st == "starrstar":
    p = HEAD + ("a single cute creature, a slender stag with big eyes standing on thin legs, very large branching antlers "
                "that curl back round into a ring, a small glowing star floating inside the ring of its antlers, " + G)
    for k in range(2): run(5671 + k, f"starr_front_star_{5671 + k}", p, N + ", multiple creatures, two creatures, girl, reindeer sleigh, moose, fawn, spots")

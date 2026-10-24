# T-450 build (2026-10-24): rear views for the three picked concepts, the T-452 recipe (gfx/drafts/t452/scripts/genback.py)
import subprocess, os
R="/Users/christopherhicks/Projects/DAEMONS"; PY=os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
os.chdir(R)
GB=("full body, soft shading, greyscale, medium grey body with light grey highlights and dark grey shading, "
    "clean black outline, isolated on white, centered, large in the frame, no shadow, no text")
N=("face, eyes, nose, mouth, whiskers, front view, facing the viewer, side view, profile, photorealistic, 3d render, colorful, colored background, grey background, dark background, "
   "scenery, floor, ground, text, letters, watermark, multiple creatures, duplicate, human, person, cropped, blurry, drop shadow, border, white body, pale body")
B={
 "handshake":"a tiny baby sugar glider seen from behind peeking out of a small round cloth pouch bag, rear view, facing away from the viewer, back of the head and back of the round ears above the rim of the pouch",
 "tethering":"a young sugar glider seen from behind clinging to a bag strap, rear view, facing away from the viewer, back of the head and back of the round ears, a dark stripe down its back, long bushy tail wrapped once around the strap",
 "coroutine":"a sugar glider seen from behind gliding in mid air, rear view, facing away from the viewer, back of the head and back of the ears, arms and legs stretched wide, furry gliding membrane spread between wrists and ankles like a square wing, a dark stripe down its back, long fluffy tail",
}
for n,s in B.items():
    for seed in (4551,4552,4553):
        r=subprocess.run([PY,"tools/spriteforge.py","t2i","--size","512x512","--seed",str(seed),"--out",f"gfx/drafts/t450/{n}_back_{seed}",
             "--prompt",f"pure white background, pixel art game sprite of a single creature, {s}, {GB}","--negative",N],capture_output=True,text=True)
        print(n, seed, r.returncode, r.stdout.strip()[-120:], r.stderr[-300:], flush=True)

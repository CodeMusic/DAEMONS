import subprocess, os
R="/Users/christopherhicks/Projects/DAEMONS"; PY=os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
os.chdir(R)
GB=("full body, chibi proportions, big round head seen from behind, soft shading, greyscale, medium grey body with light grey highlights and dark grey shading, "
    "clean black outline, isolated on white, centered, large in the frame, no shadow, no text")
N=("face, eyes, nose, mouth, whiskers, front view, facing the viewer, side view, profile, photorealistic, 3d render, colorful, colored background, grey background, dark background, "
   "scenery, floor, ground, text, letters, watermark, multiple creatures, duplicate, human, person, cropped, blurry, drop shadow, border, white body, pale body")
B={
 "spike":"a small mouse seen from behind, rear view, facing away from the viewer, back of the head and back of the big round ears, a long thin tail ending in a zigzag lightning bolt shape curling up toward the viewer",
 "artsai":"a small rabbit seen from behind, rear view, facing away from the viewer, back of the head and back of the long tall ears, round fluffy tail",
 "packet":"a plump little pigeon bird seen from behind, rear view, facing away from the viewer, back of the head, folded wings and fanned tail feathers",
}
for n,s in B.items():
    for seed in (4541,4542,4543):
        r=subprocess.run([PY,"tools/spriteforge.py","t2i","--size","512x512","--seed",str(seed),"--out",f"gfx/drafts/t452/{n}_back_{seed}",
             "--prompt",f"pure white background, pixel art game sprite of a single creature, {s}, {GB}","--negative",N],capture_output=True,text=True)
        print(r.stdout.strip()[-120:], r.stderr[-300:], flush=True)

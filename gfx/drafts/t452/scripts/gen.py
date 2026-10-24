import subprocess, sys, os
from PIL import Image
R="/Users/christopherhicks/Projects/DAEMONS"; PY=os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
os.chdir(R)
G=("full body, chibi proportions, big round head, large expressive eyes, soft shading, greyscale, medium grey body with light grey highlights and dark grey shading, "
   "clean black outline, isolated on white, centered, large in the frame, no shadow, no text")
N=("photorealistic, 3d render, colorful, colored background, grey background, dark background, green, grass, scenery, floor, ground, "
   "text, letters, watermark, multiple creatures, two creatures, duplicate, human, person, cropped, blurry, drop shadow, border, white body, pale body")
S={
 "rovercub":"a small robot puppy, a quadruped robot dog with a boxy metal body, thin jointed metal legs, a round camera head with one big lens eye, standing, facing left three-quarter view",
 "packet":"a plump little pigeon bird holding a sealed paper envelope letter in its beak, standing on two small feet, folded wings, facing left three-quarter view",
 "spike":"a small mouse standing upright on its hind legs, big round ears, pink nose, a long thin tail ending in a zigzag lightning bolt shape, facing left three-quarter view",
 "backbone":"a long serpent made of a chain of round stone vertebrae segments, rising in a curve out of a pile of round boulders, rearing its small dragon-like head up, facing left",
 "dangling":"a round floating ghost blob with a wide smile and big round eyes, a wavy frilled bottom edge, hovering, no legs, facing the viewer",
 "artsai":"a small white rabbit sitting upright, long tall ears, curious red eyes, soft fluffy fur, facing left three-quarter view",
}
BACK={
 "spike":"a small mouse standing upright on its hind legs, rear view, facing away from the viewer, back of the head and back of the big round ears, a long thin tail ending in a zigzag lightning bolt shape curling toward the viewer",
 "artsai":"a small white rabbit sitting upright, rear view, facing away from the viewer, back of the head and back of the long tall ears, round fluffy tail",
 "packet":"a plump little pigeon bird, rear view, facing away from the viewer, back of the head, folded wings and tail feathers, the corner of an envelope in its beak",
}
def run(args):
    print(" ".join(args[:6]), flush=True)
    r=subprocess.run([PY,"tools/spriteforge.py"]+args,capture_output=True,text=True)
    print(r.stdout[-200:], r.stderr[-400:], flush=True)
only=sys.argv[1:] 
for n,s in S.items():
    if only and n not in only: continue
    src=f"gfx/drafts/t452/src/{n}_front_512.png"
    im=Image.open(f"gfx/daemons/{n}_front.png").convert("RGBA")
    if im.width!=64: im=im.resize((64,64),Image.LANCZOS)
    bg=Image.new("RGBA",im.size,(255,255,255,255)); bg.alpha_composite(im)
    bg.convert("RGB").resize((512,512),Image.NEAREST).save(src)
    for seed in (4521,4522,4523):
        run(["t2i","--size","512x512","--seed",str(seed),"--out",f"gfx/drafts/t452/{n}_front_{seed}",
             "--prompt",f"pure white background, pixel art game sprite of a single creature, {s}, {G}","--negative","rear view, "+N])
    for seed,dn in ((4531,0.6),(4532,0.72)):
        run(["i2i","--seed",str(seed),"--denoise",str(dn),"--image",src,"--out",f"gfx/drafts/t452/{n}_front_i2i_{seed}",
             "--prompt",f"pure white background, pixel art game sprite of a single creature, {s}, {G}","--negative","rear view, "+N])
for n,s in BACK.items():
    if only and n not in only: continue
    for seed in (4521,4522,4523):
        run(["t2i","--size","512x512","--seed",str(seed),"--out",f"gfx/drafts/t452/{n}_back_{seed}",
             "--prompt",f"pure white background, pixel art game sprite of a single creature, {s}, {G}",
             "--negative","face, eyes, nose, front view, side view, profile, "+N])

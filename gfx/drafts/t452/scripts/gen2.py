"""T-452 round two (the user, 2026-10-24): charm with each daemon's props spelled out in its prompt.

    gen2.py STAGE [NAME ...]      STAGE: front | back | packetback | icon

Every draft lands in gfx/drafts/t452/b/ with spriteforge's seed record beside it. 512x512 throughout.
The props come from each one's INDEX category and entry and from today's art (gfx/daemons/), named here so a
seed that drops them can be seen to have dropped them."""
import subprocess, sys, os
from PIL import Image
R = "/Users/christopherhicks/Projects/DAEMONS"; PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
os.chdir(R)
OUT = "gfx/drafts/t452/b"; os.makedirs(OUT, exist_ok=True); os.makedirs(OUT + "/src", exist_ok=True)

HEAD = "pure white background, pixel art game sprite of a single cute creature, "
#  Accents: the body is asked for in mid grey (cleandraft.py's recipe); colour is asked for ONLY on the named
#  small props, and "mostly grey, only small touches of colour" steers the rest toward the type's ramp.
G = ("full body, chibi proportions, big round head, large expressive eyes, soft shading, mostly greyscale, "
     "medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
     "clean black outline, isolated on white, centered, large in the frame, no shadow, no text")
GB = ("full body, chibi proportions, big round head seen from behind, soft shading, mostly greyscale, "
      "medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, "
      "centered, large in the frame, no shadow, no text")
N = ("photorealistic, 3d render, colorful, rainbow, colored background, grey background, dark background, scenery, "
     "floor, ground, text, letters, watermark, multiple creatures, two creatures, duplicate, human, person, cropped, "
     "blurry, drop shadow, border, white body, pale body")
NB = "face, eyes, nose, mouth, beak tip, whiskers, front view, facing the viewer, side view, profile, " + N

#  name -> (front subject, back subject, extra negative)
S = {
 "packet": (
  "a plump round pigeon, a grey city pigeon with a small round head, short beak and a shiny neck, "
  "holding a sealed paper envelope letter with a small red wax seal in its beak, standing on two small pink feet, "
  "folded wings, short fanned tail, facing left three-quarter view",
  "a plump round pigeon seen from behind, rear view, facing away from the viewer, back of the round head, "
  "folded wings crossed over its back, fanned tail feathers pointing at the viewer, two small feet, "
  "a white envelope corner peeking out beside its head",
  "sparrow, owl, penguin, chick, duck, parrot, open wings, flying"),
 "backbone": (
  "a long serpent made of a chain of stacked round grey boulders, each boulder one vertebra, the chain of stones "
  "rising in a tall curve out of a pile of rocks, its head is one round boulder with two big cute eyes and a small "
  "smile, no limbs, facing left",
  "a long serpent made of a chain of stacked round grey boulders seen from behind, rear view, facing away from the "
  "viewer, the back of its round boulder head, the chain of stones curving up out of a pile of rocks",
  "dragon, wings, horns, claws, legs, arms, scales, snake skin, fangs, spikes, fire, teeth"),
 "rovercub": (
  "a small robot puppy, a four-legged robot dog standing on all four legs, a boxy grey metal body, four short "
  "jointed metal legs with round paw feet, a big round robot head with floppy metal puppy ears and one big round "
  "camera lens eye, a short antenna tail, facing left three-quarter view",
  "a small robot puppy seen from behind, rear view, facing away from the viewer, a four-legged robot dog on all "
  "four legs, a boxy grey metal back panel, the back of its big round robot head and its floppy metal ears, "
  "a short antenna tail",
  "humanoid, standing upright, bipedal, two legs, arms, hands, android, mech, gun"),
 "spike": (
  "a small mouse standing upright on its hind legs, big round ears with pink inner ears, a small pink nose, "
  "whiskers, tiny paws, a long thin tail ending in a sharp zigzag lightning bolt shape, facing left three-quarter view",
  "a small mouse standing upright seen from behind, rear view, facing away from the viewer, back of the head and "
  "back of the big round ears, a long thin tail ending in a sharp zigzag lightning bolt shape curling up beside it",
  "pikachu, yellow body, rabbit, hamster"),
 "dangling": (
  "a round floating ghost blob, a white sheet ghost with a big round head, two big round black eyes and a wide "
  "smile, a wavy frilled bottom edge, hovering with no legs, facing the viewer",
  "a round floating ghost blob seen from behind, rear view, facing away from the viewer, the plain smooth back of "
  "its round head, a wavy frilled bottom edge, hovering with no legs",
  "legs, arms, skull, scary, horror, chain"),
 "artsai": (
  "a small rabbit sitting upright, long tall upright ears, round red eyes, a small pink nose, soft fluffy fur, "
  "a round fluffy tail, facing left three-quarter view",
  "a small rabbit sitting upright seen from behind, rear view, facing away from the viewer, back of the head and "
  "the backs of its long tall upright ears, a round fluffy cotton tail",
  "carrot, clothes, human ears"),
}
#  Party icons, drawn on their own (point 3): a head-and-shoulders bust that fills the frame, so the reduction
#  to 32 keeps the face instead of averaging a whole body into mud.
ICON = {
 "packet": "head and shoulders of a plump round grey pigeon with a white envelope in its beak",
 "backbone": "head and top of the neck of a serpent made of stacked round grey boulders, its head one round boulder with two big eyes",
 "rovercub": "head and shoulders of a small robot puppy, a big round robot head with floppy metal ears and one big camera lens eye",
 "spike": "head and shoulders of a small grey mouse with big round ears, pink inner ears and a pink nose, a zigzag lightning tail tip beside it",
 "dangling": "a round white ghost blob head with two big round eyes and a wide smile, wavy frilled edge",
 "artsai": "head and shoulders of a small white rabbit with long tall upright ears and red eyes",
}
GI = ("bust portrait, head and shoulders only, big round head filling the frame, very simple, large shapes, few details, "
      "thick black outline, flat shading, mostly greyscale, medium grey with light grey highlights, isolated on white, "
      "centered, no text")

def run(args):
    out = args[args.index("--out") + 1]
    if os.path.exists(out + ".png"):
        print("have", out); return
    t = subprocess.run([PY, "tools/spriteforge.py"] + args, capture_output=True, text=True)
    print(out, t.stdout.strip()[-80:], t.stderr.strip()[-300:], flush=True)

def src512(path, dst, flip=False):
    im = Image.open(path).convert("RGBA")
    if im.width != 64: im = im.resize((64, 64), Image.LANCZOS)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    bg.convert("RGB").resize((512, 512), Image.NEAREST).save(dst)
    return dst

def t2i(name, kind, seed, subj, neg):
    run(["t2i", "--size", "512x512", "--seed", str(seed), "--out", f"{OUT}/{name}_{kind}_{seed}",
         "--prompt", HEAD + subj + ", " + (GB if kind == "back" else G), "--negative", neg])

def i2i(name, kind, seed, dn, img, subj, neg, tag="i2i"):
    run(["i2i", "--seed", str(seed), "--denoise", str(dn), "--image", img, "--out", f"{OUT}/{name}_{kind}_{tag}_{seed}",
         "--prompt", HEAD + subj + ", " + (GB if kind == "back" else G), "--negative", neg])

#  Second wording, the prop FIRST: seeds 4601-4604 drew good pigeons and dropped the envelope every time in t2i
#  (only i2i from today's front kept it). A prop named first is a prop drawn.
S2 = {
 "packet": "a big white paper envelope letter with a red wax seal, held in the beak of a plump round grey pigeon, "
           "the envelope is large and clearly visible, the pigeon stands on two small pink feet, folded wings, facing left",
 "backbone": "a cute rock serpent: a chain of six big round grey boulders stacked like a spine, rising in an S curve out "
             "of a pile of rocks, the top boulder is its head with two big round cute eyes, simple round stones, no limbs",
 "rovercub": "a cute little robot puppy on four legs, a toy robot dog made of riveted grey metal plates, a boxy metal "
             "body with a panel seam and bolts, four stubby jointed metal legs, a big round metal head with two floppy "
             "metal plate ears, one large round camera lens eye, a small antenna on its head, a short antenna tail",
 "spike": "a cute little grey mouse standing on its hind legs, its long thin tail ends in a big sharp zigzag lightning bolt, "
          "big round ears, pink nose",
}

stage = sys.argv[1]; only = sys.argv[2:] or list(S)
for n in only:
    front, back, xneg = S[n]
    if stage == "front":
        for seed in (4601, 4602, 4603, 4604):
            t2i(n, "front", seed, front, "rear view, " + xneg + ", " + N)
        src = src512(f"gfx/daemons/{n}_front.png", f"{OUT}/src/{n}_front_512.png")
        for seed, dn in ((4611, 0.6), (4612, 0.72)):
            i2i(n, "front", seed, dn, src, front, "rear view, " + xneg + ", " + N)
    elif stage == "front2":
        for seed in (4605, 4606, 4607, 4608):
            t2i(n, "front", seed, S2[n], "rear view, " + xneg + ", " + N)
    elif stage == "front3":
        #  BACKBONE: G's "big round head" turned every t2i seed into a head on a plinth; the chain went. Here the
        #  whole length is the subject and the face is small, and i2i from today's front is tried nearer the source.
        GL = G.replace("chibi proportions, big round head, large expressive eyes", "cute chibi style, the whole long body visible, small cute face with two big round eyes")
        for seed in (4613, 4614, 4615, 4616):
            run(["t2i", "--size", "512x512", "--seed", str(seed), "--out", f"{OUT}/{n}_front_{seed}",
                 "--prompt", HEAD + S2[n] + ", " + GL, "--negative", "rear view, big head, " + xneg + ", " + N])
        src = f"{OUT}/src/{n}_front_512.png"
        for seed, dn in ((4617, 0.5), (4618, 0.55), (4619, 0.62), (4620, 0.66)):
            i2i(n, "front", seed, dn, src, front, "rear view, " + xneg + ", " + N)
    elif stage == "back":
        for seed in (4601, 4602):
            t2i(n, "back", seed, back, xneg + ", " + NB)
        src = src512(f"gfx/daemons/{n}_back.png", f"{OUT}/src/{n}_back_512.png")
        for seed, dn in ((4611, 0.6), (4612, 0.72)):
            i2i(n, "back", seed, dn, src, back, xneg + ", " + NB)
    elif stage == "packetback":      # point 4: try harder
        for seed in (4621, 4622, 4623, 4624, 4625, 4626):
            t2i(n, "back", seed, back, xneg + ", " + NB)
        sil = f"{OUT}/src/{n}_silhouette_flipped_512.png"   # made by silhouette.py from the chosen front
        for seed, dn in ((4631, 0.62), (4632, 0.72), (4633, 0.8)):
            i2i(n, "back", seed, dn, sil, back, xneg + ", " + NB, tag="sil")
    elif stage == "icon":
        for seed in (4641, 4642, 4643):
            run(["t2i", "--size", "512x512", "--seed", str(seed), "--out", f"{OUT}/{n}_icon_{seed}",
                 "--prompt", HEAD + ICON[n] + ", " + GI, "--negative", "full body, legs, feet, " + xneg + ", " + N])

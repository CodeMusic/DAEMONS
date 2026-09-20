#!/bin/bash
# T-176 batch 3: the three legendaries and nine more of the island set. Every prompt names a CONCRETE creature --
# batches 1 and 2 showed the model draws an animal well and a concept not at all.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t176/alt3
mkdir -p $S
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
while IFS='|' read -r name body front back; do
  for seed in 1917 42; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, profile, rear view, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, no face visible, $back, $G" --negative "face, eyes, mouth, beak, looking at viewer, front view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
orpheus|majestic long-tailed bird with a crested head and long trailing tail feathers, wings half spread, singing|the open beak mid-song, crest raised|the long trailing tail feathers and half-spread wings from behind
prometheus|large bird with broad wings carrying a burning brand in its talons, feathers like flame tips|the brand held out in its talons|the broad wings from behind and the brand below
asclepius|large bird with sharp jagged wings and a spiked crest, standing alert|a fierce open beak, jagged crest|the jagged wings spread from behind
sigkill|heavy armoured beetle-creature with two huge flat pincer claws held ready, thick plated shell|the two flat pincers raised|the plated back and the two raised pincers
overlay|round two-part creature whose outer shell is a second smooth layer over an inner body, a visible seam where they meet|the seam across its front, a calm face|the smooth outer layer from behind and the seam
engram|heavy tusked elephant-like creature with a ridged armoured hide, short thick legs|two long tusks and a ridged brow|the ridged armoured back and the short tail
withdrawal|round sealed pod creature covered in hard plates, no opening visible, small spikes|a sealed front plate, no face|the sealed round back and its plates
circular|spinning top-shaped creature balanced on one point, arms held out, always turning|the point it spins on, arms out|the spinning top from behind
obsession|lean hound with a long muzzle, ribbed plates on its back and curved horns|an open howling mouth, curved horns|the ribbed plates and curved horns from behind
craving|large shaggy bear standing upright, long claws, a ring mark on its chest|the ring mark and long claws|the shaggy back and the short tail
brooding|sealed cocoon creature with a hard cracked shell, hovering slightly off the ground|the cracked seam on the shell, no face|the smooth sealed back of the shell
clinging|octopus-like creature gripping a rock with its arms, a wide head and many suckers|the wide head and gripping arms|the wide head from behind and the arms wrapped round
LIST

#!/bin/bash
# T-131 batch 2, second pass: the views make.sh drew badly, three seeds each, to choose from.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch2/alt; mkdir -p $S
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, no shadow, no text"
N2="white body, pale body, grey background, colored background, floor, ground, pedestal, grid, tiles on the ground, people, human, drop shadow, shadow, pink, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, border, lines"
F="side view, profile, rear view, $N2"
B="face, eyes, mouth, nose, looking at viewer, side view, profile, front view, $N2"
while IFS='|' read -r name view neg prompt; do
  for seed in 7 42 2024; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_${view}_$seed \
      --prompt "pure white background, pixel art game sprite of a single $prompt, $G" --negative "${!neg}" 2>&1 | tail -1
  done
done <<'LIST'
heap|front|F|small creature that is a heap of rough stacked boulders with two stubby stone arms, front view, facing the viewer, a grumpy face with two eyes on the front boulder
heap|back|B|small creature that is a heap of rough stacked boulders with two stubby stone arms, rear view, facing away from the viewer, the rounded back of the boulder pile
sector|front|F|small round armadillo creature sitting upright, its shell made of square armour plates, front view, facing the viewer, round ears, small claws
sector|back|B|small round armadillo creature, rear view, facing away from the viewer, its curved back shell made of square armour plates in rows, short tail
backbone|back|B|huge serpent made of a long chain of large rounded stone blocks like vertebrae, rear view, facing away from the viewer, the chain coiling away, the back of its horned head
preempt|back|B|round furry pig-nosed monkey, rear view, facing away from the viewer, the back of its round furry head and body, fists raised to either side
worm|back|B|coiled snake whose long body is made of identical repeating segments, rear view, facing away from the viewer, the segmented coils from behind, back of its head
fork|front|F|small spiky rabbit-like creature with big ears, front view, facing the viewer, one short horn on its forehead split into two equal prongs like a tuning fork
LIST

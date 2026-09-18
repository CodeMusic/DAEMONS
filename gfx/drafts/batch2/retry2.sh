#!/bin/bash
# T-131 batch 2, third pass: the two serpents' backs (the head keeps turning to the camera) and FORK's horn.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch2/alt; mkdir -p $S
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, no shadow, no text"
N2="white body, pale body, grey background, colored background, floor, ground, pedestal, base, people, human, weapon, knife, sword, drop shadow, shadow, pink, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, border, lines"
F="side view, profile, rear view, $N2"
B="face, eyes, mouth, fangs, tongue, nose, looking at viewer, side view, profile, front view, $N2"
while IFS='|' read -r name view neg prompt; do
  for seed in 7 42 2024 88; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_${view}_$seed \
      --prompt "pure white background, pixel art game sprite of a single $prompt, $G" --negative "${!neg}" 2>&1 | tail -1
  done
done <<'LIST'
backbone|front|F|huge rock serpent made of a chain of large rounded boulders like a spine of vertebrae, front view, facing the viewer, a horned boulder head rearing up, the boulder chain curving down behind it
backbone|back|B|huge rock serpent made of a chain of large rounded boulders like a spine of vertebrae, seen from directly behind, the back of its horned boulder head at the top, the boulder chain curving down toward the viewer, no face visible
worm|back|B|snake made of identical repeating segments, seen from directly behind, the smooth back of its head at the top facing away, its segmented body coiled below toward the viewer, no face visible
fork|front|F|small spiky rabbit-like creature with big ears, front view, facing the viewer, two small matching horns side by side on its forehead, a spiny back
LIST
# BRANCH's first front held two blades; redrawn with weapons in the negative.
for seed in 7 42 2024 88; do
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/branch_front_$seed \
    --prompt "pure white background, pixel art game sprite of a single small spiky rabbit-like creature with large upright ears, front view, facing the viewer, one tall horn on its forehead that branches into two tines like a forked twig, empty paws, $G" \
    --negative "$F" 2>&1 | tail -1
done

#!/bin/bash
# T-176 batch 2, second round: MOOD came out a blob, LOOKOUT a stick figure, RELEASE lost its lamp. Each prompt now
# names a CONCRETE animal, the way TRUST's cracked shell landed -- the abstract clause is what fails.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t176/alt2
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, stick figure, grey background, colored background, floor, ground, water surface, pedestal, frame, box, drop shadow, text, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
while IFS='|' read -r name body front back; do
  for seed in 7 99 314; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_r2_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, profile, rear view, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_r2_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, no face visible, $back, $G" --negative "face, eyes, mouth, looking at viewer, front view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
mood|small round blue mouse with a round belly, tiny round ears and a long thin tail ending in a ball, sitting|round cheeks, the ball tail curled beside it|the round back, the thin tail and its ball
lookout|slender ferret standing upright on its hind legs, very long body stretched tall, small round ears, a long thick tail for balance|a small alert face at the top of the long body, forepaws held at its chest|the long stretched back and the thick tail
release|four-legged woolly creature with a long neck and a round lamp at the tip of its upright tail, striped fleece|a calm face, the tail lamp raised behind it|the striped fleece and the raised tail with its round lamp
LIST

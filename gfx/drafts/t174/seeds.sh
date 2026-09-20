#!/bin/bash
# T-174: four seeds each for CRYSTAL and the PLAYER, by the trial's recipe -- the ROM picture as the source, on white.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t174
N="human, human face, hair, person, anime, green background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry"
while IFS='|' read -r name body; do
  for seed in 1917 42 7 99; do
    python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise 0.45 --seed $seed --out $S/alt/${name}_s$seed \
      --prompt "pure white background, pixel art game sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
crystal|red fox scientist with a fox head, calm muzzle and bushy tail, in a white lab coat open over purple, one arm out presenting
logic|grey monkey trainer with a monkey face and long tail, in a wide brown hat and long cream coat over black, standing
intuition|grey monkey trainer with a monkey face and long tail, in a wide brown hat and long cream coat over black, walking
LIST

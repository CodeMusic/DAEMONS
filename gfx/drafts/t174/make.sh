#!/bin/bash
# T-174 trial: CRYSTAL and the PLAYER, the two most visible and the two hardest (64x96, 8bpp, their own palette banks).
# Restyled from the drawing the game already uses -- T-169's method, which keeps the animal, the clothes and the pose.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t174
N="human, human face, hair, person, man, woman, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  for dn in 0.4 0.5; do
    python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise $dn --seed 1917 --out $S/alt/${name}_$dn \
      --prompt "pure white background, pixel art game sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
crystal|red fox scientist with a fox head and bushy tail, in a white lab coat open over purple, one arm out, presenting
logic|grey monkey trainer with a monkey face and long tail, in a wide brown hat and a long cream coat over black, a strap across the chest
intuition|grey monkey trainer with a monkey face and long tail, in a wide brown hat and a long cream coat over black, walking
LIST

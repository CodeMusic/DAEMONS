#!/bin/bash
# T-165 second round: every first-round back had a face (T-166's old problem), and FORGE settled on an ox under a forge.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t165/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on pure white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, grey background, colored background, frame, box, border, floor, ground, pedestal, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
B="face, eyes, mouth, nose, looking at viewer, front view, side view, profile, $N2"
F="side view, profile, rear view, $N2"
for seed in 1917 42 7 99; do
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/pixelbyte_back2_$seed \
    --prompt "pure white background, pixel art game sprite of a small puppy seen from directly behind, sitting and facing away from the viewer, the back of its head and floppy ears, its rump and a stubby wagging tail toward the viewer, no face visible, $G" --negative "$B" 2>&1 | tail -1
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/forge_front2_$seed \
    --prompt "pure white background, pixel art game sprite of a single sturdy ox facing the viewer head-on, a small blacksmith furnace strapped on its back with a glowing mouth and a short chimney, an anvil hanging at its side, front view, $G" --negative "$F" 2>&1 | tail -1
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/forge_back2_$seed \
    --prompt "pure white background, pixel art game sprite of a single sturdy ox seen from directly behind, its rump and tail toward the viewer, a blacksmith furnace strapped on its back with a short chimney, no face visible, $G" --negative "$B" 2>&1 | tail -1
done

#!/bin/bash
# T-165 third round: FORGE's back only. Round two drew the ox side-on every time; PIXELBYTE's real back came from
# "sitting and facing away", so the same framing here, and more seeds.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t165/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on pure white, centered, small in the frame with empty space all around, no shadow, no text"
B="face, eyes, mouth, nose, horns in front, looking at viewer, front view, side view, profile, walking sideways, human, person, grey background, colored background, frame, box, border, floor, ground, drop shadow, shadow, text, watermark, multiple creatures, scenery, blurry, cropped"
for seed in 1917 42 7 99 314 2026; do
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/forge_back3_$seed \
    --prompt "pure white background, pixel art game sprite of a single sturdy ox seen from directly behind, standing and facing away from the viewer, its broad rump and tail toward the viewer, the backs of its horns just showing over a blacksmith furnace strapped on its back, a short chimney rising from the furnace, no face visible, rear view, $G" --negative "$B" 2>&1 | tail -1
done

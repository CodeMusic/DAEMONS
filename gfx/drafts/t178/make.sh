#!/bin/bash
# T-178: the five portraits an outline could not save, redrawn at 1024 instead of 512.
#
# WHY 1024, AND IT IS ARITHMETIC RATHER THAN TASTE. The checkpoint draws on a fixed 8px grid, so a 512 canvas gives
# 64 ART PIXELS and the figure lands in about 50 of them -- SMALLER than the 64x64 sprite it becomes. Every one of
# these five, and 28 of the 75 portrait sources, is therefore UPSCALED into the game. The portraits that read are
# the hand drafts, whose figures are 270-290px and get DOWNSCALED. Downscaling averages; upscaling invents.
#
# 1024 gives 128 art pixels, so the figure is drawn at roughly twice the sprite and reduced into it. T-131 measured
# the cost at 82-106s a view against 23s at 512, which for five portraits is nothing.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t178/alt
mkdir -p $S
N="human, human face, hair, person, girl, boy, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic, thin spindly limbs, scattered small objects"
while IFS='|' read -r name body; do
  for seed in 1917 42; do
    python3 tools/spriteforge.py t2i --size 1024x1024 --seed $seed --out $S/${name}_$seed \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, standing, clean black outline, bold simple shapes, isolated on white, centered" \
      --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
beauty|gazelle with a gazelle head and two swept-back horns, in a long pale blue dress, hooves, hands held together
gamer|jackal with a jackal head and tall pointed ears, in a blue tracksuit jacket and jeans, holding a small handheld console in both hands
ranger_m|pine marten with a marten head and a long body, in a green ranger uniform with a wide brimmed hat and a shoulder satchel
ranger_f|pine marten with a marten head and a long body, in an orange and blue ranger uniform with a cap and a shoulder satchel
juggler|octopus with a round head and many arms, in a red and white striped shirt and brown trousers, arms raised and curling
LIST

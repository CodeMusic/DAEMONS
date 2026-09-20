#!/bin/bash
# T-174's remainder, 2026-09-20: the nine named-cast pictures that are neither spriteforge nor code.
# The recipe the CRYSTAL experiment settled: restyle from the DRAWING at its own resolution (tools/prephires.py
# keys the backdrop with gbachar's own silhouette and pads to the sprite's aspect at 904px), denoise 0.45, and
# judge at the size the game shows -- 64x64 for a portrait, 64x96 for a speech pic.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t174
N="human, human face, hair, person, man, woman, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  for seed in 1917 7; do
    python3 tools/spriteforge.py i2i --image $S/src2/${name}_hi.png --denoise 0.45 --seed $seed --out $S/alt2/${name}_$seed \
      --prompt "pure white background, pixel art game sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" \
      --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
holt|brown river otter engineer with an otter head and a thick tapering tail, in blue-grey work coveralls and a tool belt, holding a coil of cable
vera|red fox woman with a fox head and a bushy tail, in a cream apron over a pale long-sleeved dress, hands together at her waist
init|basset hound with long drooping ears and a heavy muzzle, in a plain beige robe and sandals, standing still
cairn|green tortoise with a domed shell, in a white shirt and a dark work apron and brown boots, holding a slate tablet
scorn|red cobra with a hooded snake head and a long coiled tail, in a grey business suit with a red tie, one hand held out
al_speech|young red fox with a fox head and a bushy tail, in a cream shirt and purple trousers and brown boots, a satchel at his side, one hand on his hip
al_early|young red fox with a fox head and a bushy tail, in a cream shirt and purple trousers and brown boots, carrying a small grey computer under one arm
al_late|young red fox with a fox head and a bushy tail, in a cream shirt and purple trousers and brown boots, one arm raised
al_champion|young red fox with a fox head and a bushy tail, in a cream shirt and purple trousers and brown boots, one arm out with the palm forward
LIST

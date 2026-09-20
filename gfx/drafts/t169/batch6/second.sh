#!/bin/bash
# T-169 batch 6, corrected: AL is a FOX -- the Clears are foxes (9.4), and the first three drafts asked for an otter,
# which would have changed his species. The otter in the bible is HOLT, a different character.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch6
N="human, human face, hair, person, girl, boy, anime, otter, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise 0.5 --seed 1917 --out $S/alt/${name}_fox \
    --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
done <<'LIST'
al_early|red fox with a fox head, pointed muzzle and bushy tail, a confident young trainer in a pale shirt and dark trousers, holding a bag
al_late|red fox with a fox head, pointed muzzle and bushy tail, an older trainer in a pale shirt and dark trousers, one arm raised
al_champion|red fox with a fox head, pointed muzzle and bushy tail, a champion in a pale shirt and dark trousers, gloved hand raised
LIST

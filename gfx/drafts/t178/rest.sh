#!/bin/bash
# T-178 batch 2: the first eight of the remaining 24 under-resolved portrait sources, redrawn at 1024.
# Species come from gbachar.py's own comments, which is what checkfable.py reads -- and after batch 1 drew three
# foxes, every prompt names the animal's DISTINGUISHING FEATURES and puts fox in the negative where it could drift.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t178/alt
N="fox, red fox, vulpine, human, human face, hair, person, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic, thin spindly limbs"
while IFS='|' read -r name body; do
  for seed in 7 1917; do
    python3 tools/spriteforge.py t2i --size 1024x1024 --seed $seed --out $S/${name}_b2$seed \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, standing, clean black outline, bold simple shapes, isolated on white, centered" \
      --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
camper|raccoon with a black bandit mask across its eyes, round ears and a thick ringed tail, in a green outdoor shirt, shorts and boots
bug_catcher|swallow with a forked tail and blue-black wings, in a wide sun hat and shorts, holding a net
sailor|albatross with a long hooked bill and very long narrow wings, in a striped sailor shirt and cap
channeler|bat with large round ears, a small upturned nose and folded wings, in a long pale ceremonial robe
cool_trainer_f|hawk with a sharp hooked beak, keen eyes and a crest of feathers, in a green jacket and hiking gear
cue_ball|toad with a wide flat head, heavy brow and rough warty skin, bare-chested in a blue tracksuit bottom
picnicker|hedgehog with a coat of short spines, a small pointed snout and round ears, in a sun hat and apron
rocket_grunt_m|emperor penguin in a dark office suit, upright and blank-faced, flippers at its sides
LIST

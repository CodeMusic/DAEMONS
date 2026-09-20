#!/bin/bash
# T-178 batch 3. Batch 2 failed four ways out of eight, and three of the four are the SAME failure: at 1024 the
# model happily draws a LITERAL ANIMAL and forgets the clothes -- SAILOR came back a plain seagull in a cap and
# ROCKET GRUNT a plain penguin with no suit at all -- and BUG CATCHER drew a human child with wings, which 9.4
# forbids outright. So every prompt here leads with the CLOTHES and says upright on two legs, and "naked animal,
# wild animal, no clothes, feral" joins the negative beside fox and human.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t178/alt
N="naked animal, wild animal, no clothes, feral, on all fours, fox, red fox, vulpine, human, human face, human child, hair, person, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic, thin spindly limbs"
while IFS='|' read -r name body; do
  for seed in 7 1917; do
    python3 tools/spriteforge.py t2i --size 1024x1024 --seed $seed --out $S/${name}_b3$seed \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, standing upright on two legs, fully clothed, full body, clean black outline, bold simple shapes, isolated on white, centered" \
      --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
cool_trainer_m|wolf in a green field jacket, khaki trousers and boots, with a wolf head, upright pointed ears and a grey ruff
staff_brazen|rat in a long dark overcoat and waistcoat, with a rat head, large round ears and a long bare tail
staff_slate|young beaver in work dungarees and a tool belt, with a beaver head, big front teeth and a flat scaled tail
tamer|spotted hyena in a red ringmaster tailcoat and dark trousers, with a hyena head, rounded ears and a sloping back
burglar|weasel in a dark striped jumper and trousers, with a weasel head, a narrow face and a long low body
psychic_f|jellyfish in long flowing robes, with a translucent domed head and trailing frills instead of arms
leader_blaine|salamander in a heat-proof apron over a work shirt, with a broad amphibian head and a thick tail
staff_doldrum_swimmer|manatee in swimming gear, with a manatee head, a whiskered blunt snout and a heavy rounded body
LIST

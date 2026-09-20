#!/bin/bash
# T-178 batch 4, the last of the 28. Both standing failures are in the negative: SPECIES DRIFT (batch 1 drew three
# foxes, batch 3 drew a rodent for the hyena and a frog for the salamander) and DROPPED CLOTHES (a plain seagull,
# a plain penguin). Species is named by its features, clothes lead the prompt.
#
# STAFF_CALLOW is not here: its source is sf_rocket_grunt_m.png, which two jobs share, and that redraw was kept.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t178/alt
N="naked animal, wild animal, no clothes, feral, on all fours, fox, red fox, vulpine, frog, rodent, mouse, rat, human, human face, human child, hair, person, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic, thin spindly limbs"
while IFS='|' read -r name body; do
  for seed in 7 1917; do
    python3 tools/spriteforge.py t2i --size 1024x1024 --seed $seed --out $S/${name}_b4$seed \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, standing upright on two legs, fully clothed, full body, clean black outline, bold simple shapes, isolated on white, centered" \
      --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
leader_erika|bowerbird in a long gardener's apron over a work shirt, with a glossy blue-black bird head, a short stout beak and folded wings
swimmer_f|axolotl in a one-piece swimsuit, with a wide flat head, feathery external gills fanning out behind it and a finned tail
swimmer_m|newt in swimming trunks and goggles, with a blunt amphibian head, a crested back and a long flat tail
youngster|house mouse in a striped shirt and shorts, with a mouse head, big round ears, a pointed snout and a long thin tail
elite_four_bruno|kangaroo in a martial arts gi with a black belt, with a kangaroo head, long upright ears, heavy hind legs and a thick tail
leader_koga|toad in a dark high-collared robe, with a broad toad head, heavy brow ridges and rough warty skin
staff_doldrum_picnicker|capybara in a wide sun hat and a long apron, with a blunt rectangular muzzle, small round ears and a heavy calm body
staff_callow|emperor penguin in a dark office suit and tie, upright, flippers held at its sides
LIST

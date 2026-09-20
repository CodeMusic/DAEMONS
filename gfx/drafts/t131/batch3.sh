#!/bin/bash
# T-131 round 3, three views only.
#
# DUPLEX is the DUALCORE case again, and T-131 batch 7 already recorded the finding: the model will not draw one
# body with two heads. DUALCORE became two birds side by side, which is what its entry says anyway. So DUPLEX is
# asked for as TWO creatures joined at the tail facing opposite ways -- which is what "sends and receives at once,
# from opposite ends" describes, and is a shape the model can hold.
#
# FAKEROOT's and QUOTA's backs still came back as a plain tree and a plain flower: the creature vanishes the moment
# its face is not asked for. Both now name the BODY that must still be there.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t131/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, scenery, photorealistic, blurry, cropped"
NBACK="face, eyes, mouth, beak, nose, snout, looking at viewer, head turned toward viewer, front view, three-quarter view"

for seed in 7 1917; do
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/duplex_front_r3$seed \
    --prompt "pure white background, pixel art game sprite of a single creature made of TWO identical long-necked heads facing opposite directions, joined at the middle by one four-legged body, both heads raised and alert, $G" \
    --negative "one head, plain horse, deer, unicorn, two separate animals, $N2" 2>&1 | tail -1
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/duplex_back_r3$seed \
    --prompt "pure white background, pixel art game sprite of a single creature made of TWO identical long-necked heads facing opposite directions on one four-legged body, seen from the side so both heads are visible in profile, $G" \
    --negative "one head, plain horse, two separate animals, $N2" 2>&1 | tail -1
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/fakeroot_back_r3$seed \
    --prompt "pure white background, pixel art game sprite of a single stocky two-legged CREATURE with a thick brown trunk body, two short legs with feet on the ground and two arms raised, a round clump of leaves on each arm, seen from behind with its back toward the viewer, $G" \
    --negative "$NBACK, plain tree, forest, oak tree, roots, no limbs, no legs, $N2" 2>&1 | tail -1
  python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/quota_back_r3$seed \
    --prompt "pure white background, pixel art game sprite of a single small two-legged CREATURE with a round body, two short legs and two leaf arms, whose head is a wide flower, seen from behind with its back toward the viewer, $G" \
    --negative "$NBACK, flower only, plant only, stem only, pot, vase, no body, no legs, $N2" 2>&1 | tail -1
done

#!/bin/bash
# T-169 batch 1, the restyle test: from words the model keeps drawing humans (the lass, the picnicker, the falcon), so
# each CURRENT portrait -- already the right animal in the right clothes -- goes through image-to-image, which T-164
# found keeps the layout at 0.5-0.65. The two COOL TRAINERs start from their halves of the COOL COUPLE portrait.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch1
N="human, human face, hair, person, girl, boy, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  for dn in 0.5 0.65; do
    python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise $dn --seed 1917 --out $S/alt/${name}_i2i_$dn \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
lass|lamb girl in a blue dress, white apron and straw bonnet
picnicker|hedgehog girl in a straw sun hat and yellow blouse with a picnic basket
cool_trainer_m|grey wolf trainer in a green field jacket
cool_trainer_f|falcon trainer in a green field jacket
bird_keeper|ostrich bird keeper in a brown apron
LIST

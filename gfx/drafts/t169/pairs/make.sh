#!/bin/bash
# T-169, the pairs: restyled from the FINAL in-ROM picture, because that is the one carrying the right two animals --
# genpairs.py/gencouple.py draw each head onto the cut picture, inside the sixteen colours it already has (T-126/T-128).
# The prompt names BOTH animals, since a pair portrait is two figures and the sheets they stand for are fixed.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/pairs
N="human, human face, hair, person, girl, boy, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic, one character, single character"
while IFS='|' read -r name body; do
  for dn in 0.4 0.5; do
    python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise $dn --seed 1917 --out $S/alt/${name}_$dn \
      --prompt "pure white background, pixel art game trainer sprite of two anthropomorphic characters standing side by side, $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
twins|two piglets with pig heads and snouts, small children in matching blue dresses
young_couple|an ox with an ox head and horns in a blue jacket beside a gazelle with a gazelle head in a yellow dress
sis_and_bro|a duckling with a duck bill in shorts beside an axolotl with feathery gills in a yellow dress
crush_kin|a kangaroo with a kangaroo head in a green vest beside a wolverine with a wolverine head in a blue top
cool_couple|a grey wolf with a wolf head beside a falcon with a hooked beak, both in green field jackets
LIST

#!/bin/bash
# T-178 round 2: GAMER and the two RANGERS came back as FOXES.
#
# This is a fable failure, not a drawing failure -- the drawings are good. 9.4 gives each class ONE species and
# forbids repeating one already spent: GAMER is a JACKAL and gbachar's own comment says "never a fox (9.4)", the
# RANGERS are PINE MARTENS, and the FOX belongs to the CLEARS -- Crystal, Vera and Al. A fox-faced ranger would put
# the family's own animal on a route trainer.
#
# So the species is asked for by its distinguishing features rather than by name, and fox is named in the negative.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t178/alt
N="fox, fox face, red fox, orange fur, vulpine, bushy fox tail, human, human face, hair, person, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic, thin spindly limbs"
while IFS='|' read -r name body; do
  for seed in 7 1917; do
    python3 tools/spriteforge.py t2i --size 1024x1024 --seed $seed --out $S/${name}_sp$seed \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, standing, clean black outline, bold simple shapes, isolated on white, centered" \
      --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
gamer|black-backed JACKAL with a black and silver-grey saddle of fur down its back, tall narrow upright ears, a slender dark muzzle and a short bushy black-tipped tail, in a blue tracksuit jacket and jeans, holding a small handheld console in both hands
ranger_m|dark brown PINE MARTEN with a long low body, small rounded ears, a pale cream bib on its throat and a long dark bushy tail, in a green ranger uniform with a wide brimmed hat and a shoulder satchel
ranger_f|dark brown PINE MARTEN with a long low body, small rounded ears, a pale cream bib on its throat and a long dark bushy tail, in a navy and orange ranger uniform with a cap and a shoulder satchel
LIST

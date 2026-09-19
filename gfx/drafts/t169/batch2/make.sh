#!/bin/bash
# T-169 batch 2: the next ten most-faced portraits, by the method batch 1 settled -- image-to-image from the T-120
# drawing each class's overworld sheet was matched to, so the class keeps its animal and its clothes. Two strengths.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch2
N="human, human face, hair, person, girl, boy, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  for dn in 0.5 0.6; do
    python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise $dn --seed 1917 --out $S/alt/${name}_$dn \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
hiker|badger hiker with a badger head and striped face, in a heavy coat and pack
camper|raccoon camper with a raccoon head and masked face, in a scout shirt and shorts
swimmer_f|axolotl swimmer with an axolotl head and feathery gills, in a swimsuit
fisherman|pelican fisher with a pelican head and long bill, in a fishing vest, holding a rod
scientist|mole scientist with a mole head and small snout, in a white lab coat
pokemaniac|opossum collector with an opossum head and pointed snout, in a red shirt
channeler|bat medium with a bat head and large ears, in a long pale robe
cue_ball|rhinoceros tough with a rhinoceros head and horn, in a vest, arms folded
black_belt|kangaroo martial artist with a kangaroo head, in a white gi and black belt
crush_girl|wolverine fighter with a wolverine head, in a teal vest and shorts
LIST

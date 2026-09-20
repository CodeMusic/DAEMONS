#!/bin/bash
# T-169 batch 4: the named cast -- the eight BENCHMARK leaders and the Review Board's four. Image-to-image at 0.5 from
# the drawing each job already uses, so the character keeps its animal, its clothes and what it is doing.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch4
N="human, human face, hair, person, girl, boy, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise 0.5 --seed 1917 --out $S/alt/${name}_0.5 \
    --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
done <<'LIST'
cairn|tortoise with a tortoise head and shell, a patient old keeper of a stone museum
basin|hippopotamus with a hippo head and wide muzzle, a lido attendant in a swimsuit
gauge|hare with a hare head and tall ears, a line engineer in work clothes
trellis|bowerbird with a bird head and blue plumage, a gardener in an apron
tilt|toad with a toad head and wide mouth, a card dealer in a waistcoat
matte|chameleon with a chameleon head and turret eyes, a film editor in dark clothes
anneal|fire salamander with a salamander head and black and yellow skin, a metallurgist in heat gear
scorn|king cobra with a cobra head and spread hood, a corporate chief in a long coat
lorelei|polar bear with a polar bear head, a calm scholar in a cold blue coat
bruno|tiger with a tiger head and striped fur, a fighter in a training vest
agatha|wombat with a wombat head, an old grey figure in a dark shawl
lance|northern cardinal with a bird head and red crest, in a long cape
LIST

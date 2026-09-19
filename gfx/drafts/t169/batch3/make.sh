#!/bin/bash
# T-169 batch 3: ten single-figure classes -- the couples and twins are left out, because genpairs.py re-heads them
# AFTER gbachar.py cuts them (the COOL COUPLE trap). Image-to-image at 0.5, the strength batches 1 and 2 settled.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch3
N="human, human face, hair, person, girl, boy, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise 0.5 --seed 1917 --out $S/alt/${name}_0.5 \
    --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
done <<'LIST'
gamer|black-backed jackal gambler with a jackal head and large ears, in a neat jacket, holding cards
ruin_maniac|aardvark digger with an aardvark head and long snout, in a dusty shirt and shorts
sailor|albatross sailor with an albatross head and long bill, in a striped shirt
super_nerd|ring-tailed lemur scientist with a lemur head and ringed tail, in a white coat and glasses
beauty|gazelle with a gazelle head, slender horns and long neck, in an elegant dress
juggler|octopus juggler with an octopus head and many arms, juggling
staff_verdigris|poodle attendant with a poodle head and clipped curls, in a gym uniform
staff_quicksilver|laboratory rat with a rat head and pale fur, in a lab coat, holding a clipboard
staff_brazen|tarsier with a tarsier head and enormous round eyes, in a dark suit
staff_lurid|poison dart frog with a frog head and wide mouth, in a bright gym outfit
LIST

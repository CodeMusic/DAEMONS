#!/bin/bash
# T-169 batch 5: the rest of the gym staff and the low-use classes. Image-to-image at 0.5, the settled method.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch5
N="human, human face, hair, person, girl, boy, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise 0.5 --seed 1917 --out $S/alt/${name}_0.5 \
    --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
done <<'LIST'
staff_ardor|meerkat with a meerkat head, standing tall on watch, in a gym uniform
staff_slate|young beaver with a beaver head and flat tail, an apprentice in work clothes
staff_doldrum_picnicker|capybara with a capybara head and blunt muzzle, calm, in a sun hat and apron
staff_doldrum_swimmer|manatee with a manatee head and whiskered snout, broad and heavy, in swim gear
rocket_grunt_f|emperor penguin office worker in a grey suit skirt, polite and blank, holding a folder
tamer|spotted hyena ringmaster with a hyena head, in a red tailcoat
engineer|beaver with a beaver head and flat tail, an engineer in dungarees
lady|swan with a swan head and long neck, in a long evening gown
painter|toucan with a toucan head and a huge bill, a painter in a smock, holding a brush
pokemon_breeder|goose with a goose head and orange bill, in a farm apron
aroma_lady|honeybee with a bee head and antennae, striped and furred, in a flowing dress
burglar|weasel with a weasel head and narrow face, a thief in a dark striped jumper
LIST

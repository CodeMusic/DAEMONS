#!/bin/bash
# T-169 batch 6: the last of the faced portraits -- the two rangers (one pine marten, two uniforms), the jellyfish
# psychic (PSYCHIC_M is derived from her by genpsychic.py, which is re-run after), the rocker, the tuber, and AL the
# rival in his three pictures. Image-to-image at 0.5.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch6
N="human, human face, hair, person, girl, boy, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise 0.5 --seed 1917 --out $S/alt/${name}_0.5 \
    --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
done <<'LIST'
ranger_m|pine marten with a marten head and bushy tail, a ranger in a wide hat and green uniform
ranger_f|pine marten with a marten head and bushy tail, a ranger in a green uniform and cap
psychic_f|jellyfish with a translucent bell for a head and trailing tentacles, in a long pale robe
rocker|skunk with a skunk head and a white stripe like a mohawk, a rocker in a leather jacket with a guitar
tuber_f|cygnet with a downy grey bird head, a small child in a swim ring
al_early|young river otter with an otter head, a confident boy trainer in a neat shirt
al_late|river otter with an otter head, an older trainer in a smart jacket
al_champion|river otter with an otter head, a champion in a long formal coat
LIST

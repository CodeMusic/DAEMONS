#!/bin/bash
# T-169 batch 1, second round: the picnicker and the lass came back as human girls, the bug catcher as a man with a
# wing, the falcon and one ostrich as plain animals. So the ANIMAL HEAD is spelled out, "walking on two legs, wearing
# clothes" is said, and hair and human features are negative.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch1/alt
G="full body from head to feet, walking upright on two legs like a person and wearing clothes, clean black outline, soft muted colours, isolated on pure white, centered, small in the frame with empty space all around, no shadow, no text"
N="human, human face, human head, hair, person, man, woman, girl, boy, child, human skin, grey background, colored background, floor, ground, scenery, frame, border, drop shadow, shadow, text, watermark, multiple characters, two characters, pet, cropped, blurry, photorealistic, on all fours"
while IFS='|' read -r name body; do
  for seed in 7 99 314; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_r2_$seed \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, facing the viewer at a slight angle, $G" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
cool_trainer_f|peregrine falcon character with a falcon head, hooked beak and feathered face, a confident young trainer in a fitted navy jacket, short skirt and boots, feathered wings as arms
picnicker|hedgehog character with a hedgehog head, pointed snout and brown spines, a cheerful hiker in a wide straw sun hat, yellow blouse and blue shorts, carrying a wicker picnic basket
bird_keeper|ostrich character with an ostrich head, long bare neck and beak, a bird keeper in a brown canvas apron over a white shirt, a small hat
swimmer_m|orange newt character with a newt head, wide mouth and smooth damp skin, a swimmer wearing blue swim trunks, long tail
lass|lamb character with a lamb head, woolly face, floppy ears and a little muzzle, a girl in a blue dress with a white apron and a straw bonnet
bug_catcher|barn swallow character with a swallow head, short beak and forked tail, a bug catcher in a bucket hat, khaki shirt and shorts, holding a long bug net
LIST

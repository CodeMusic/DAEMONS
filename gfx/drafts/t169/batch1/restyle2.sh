#!/bin/bash
# T-169 batch 1, all ten restyled at 0.5 from the drawing their overworld sheet was matched to -- the method, because
# it keeps each class's ANIMAL where words alone drew humans. The COOL TRAINERs start from the wolf and falcon halves of
# the ROM's COOL COUPLE (gencouple.py re-headed its ibexes); the lass's prompt drops "girl", which pulled her human.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch1
N="human, human face, hair, person, girl, boy, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name dn body; do
  python3 tools/spriteforge.py i2i --image $S/src/$name.png --denoise $dn --seed 1917 --out $S/alt/${name}_i2i_$dn \
    --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" --negative "$N" 2>&1 | tail -1
done <<'LIST'
cool_trainer_m|0.5|grey wolf trainer with a wolf head and muzzle in a green field jacket
cool_trainer_f|0.5|falcon trainer with a falcon head and hooked beak in a green field jacket
rocket_grunt_m|0.5|emperor penguin office worker in a grey suit holding an ID badge
youngster|0.5|mouse boy in a striped shirt and brown shorts
swimmer_m|0.5|orange newt swimmer in blue swim trunks
biker|0.5|wild boar biker in a black leather vest
bug_catcher|0.5|swallow bird with a bug net and a bucket hat
lass|0.45|lamb with a woolly lamb face, muzzle and floppy ears, wearing a blue dress, white apron and straw bonnet
lass|0.55|lamb with a woolly lamb face, muzzle and floppy ears, wearing a blue dress, white apron and straw bonnet
LIST

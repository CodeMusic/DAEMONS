#!/bin/bash
# T-169 batch 1: the two COOL TRAINERs (the vanilla humans left, as the wolf and falcon their sheets are) and the eight
# most-faced portraits, each the animal gbachar.py's job names and in the outfit its current portrait wears.
# Portraits keep their own palettes, so they are drawn in COLOUR (daemons were grey for the type ramp).
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t169/batch1/alt
G="full body from head to feet, standing, clean black outline, soft muted colours, isolated on pure white, centered, small in the frame with empty space all around, no shadow, no text"
N="human, human face, person, man, woman, girl, boy, grey background, colored background, floor, ground, grass, scenery, frame, border, drop shadow, shadow, text, letters, watermark, multiple characters, cropped, blurry, photorealistic"
while IFS='|' read -r name body; do
  for seed in 1917 42; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_$seed \
      --prompt "pure white background, pixel art game trainer sprite of a single anthropomorphic $body, facing the viewer at a slight angle, $G" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
cool_trainer_m|grey wolf standing upright, a confident young trainer in a fitted navy jacket, dark trousers and boots, a pokeball-like capsule in one paw
cool_trainer_f|peregrine falcon standing upright, a sharp confident young trainer in a fitted navy jacket, a short skirt and boots, wings folded like arms
rocket_grunt_m|emperor penguin standing upright, an office worker in a grey business suit and tie, holding an ID badge, polite and blank
picnicker|hedgehog standing upright, a cheerful girl in a wide straw sun hat, yellow blouse and blue shorts, carrying a wicker picnic basket
bird_keeper|ostrich standing upright, a bird keeper in a brown canvas apron over a shirt, long neck, small hat
youngster|small mouse standing upright, a boy in a red cap, blue and white striped shirt and brown shorts, eager
swimmer_m|orange newt standing upright, a swimmer in blue swim trunks, long tail, smooth damp skin
biker|wild boar standing upright, a biker in a black leather vest and jeans, small tusks, heavy boots
lass|young lamb standing upright, a girl in a blue dress with a white apron and a straw bonnet, fluffy wool
bug_catcher|barn swallow standing upright, a bug catcher in a bucket hat, khaki shirt and shorts, holding a long bug net
LIST

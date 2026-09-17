#!/bin/bash
# T-131 batch 1, exactly as drafted 2026-09-17. Cleaned with tools/cleandraft.py --streaks; CRAWLER's front with
# --streak-box=12,26,47,36. Sheet: tools/contactsheet.py gfx/drafts/batch1 "BULBASAUR rovercub 5" ...
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch1
P="pixel art game sprite, full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, flat solid green background, centered, no shadow, no text"
N="green body, green tint, pale body, drop shadow, shadow, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, border"
mkdir -p $S/src
while IFS='|' read -r name file desc; do
  ext=${file##*.}; b=${file%.*}
  python3 tools/prepconcept.py gfx/front/$file $S/src/${name}_front.png 0,200,0
  python3 tools/prepconcept.py gfx/back/$b-back.$ext $S/src/${name}_back.png 0,200,0
  for v in front back; do
    view="front view"; [ $v = back ] && view="rear view, seen from behind"
    python3 tools/spriteforge.py i2i --out $S/${name}_$v --image $S/src/${name}_$v.png --denoise 0.55 --seed 1917 \
      --prompt "$desc, $view, $P" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
rovercub|rovercub.png|a small quadruped robot dog with a boxy head
label|labl.png|a small walking paper luggage tag creature with a string loop on top and little feet
cluster|clustr.png|a round ball made of many clustered circles of different greys
packet|packet.jpeg|a small round songbird carrying a sealed envelope
nibble|nibble.jpeg|a plump rat with a long thin tail and square notches bitten out along its back
crawler|crawler.jpeg|a long segmented caterpillar made of round alternating grey segments with tiny legs and big eyes
scraper|scraper.jpeg|a segmented grub larva with a curved hook horn on its head and a trailing tail
pending|pending.jpeg|a sleeping cocoon pupa wrapped in a curved shell with a calm closed-eyed face
buffer|buffer.jpeg|a hard cocoon pupa with a glossy shell and a hunched body
spike|spike.jpeg|a small standing mouse with round ears and a jagged lightning bolt shaped tail
LIST

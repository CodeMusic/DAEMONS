#!/bin/bash
# T-176 batch 3, second round: OVERLAY lost the SEAM between its two layers (which is the whole entry -- the first
# is still underneath, still wrong) and CIRCULAR came back as a spinning top with no creature in it.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t176/alt3
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, pedestal, frame, box, drop shadow, text, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
while IFS='|' read -r name extra body front back; do
  for seed in 7 99 314; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_r2_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $extra, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_r2_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, no face visible, $back, $G" --negative "face, eyes, mouth, looking at viewer, front view, $extra, $N2" 2>&1 | tail -1
  done
done <<'LIST'
overlay|plain round creature, smooth featureless body|duck-billed creature wearing a second smooth shell over its body like armour plating, the older rougher body clearly visible underneath at the neck, arms and legs, a hard rim where the outer shell ends|the rim of the outer shell and the older body showing beneath it|the outer shell plates from behind and the older body at the edges
circular|spinning top, toy, cone, featureless object|creature balanced upside down spinning on the point of its head, two long legs held straight up in a V, two arms out for balance, a conical crest on its head as the spinning point|the two legs up in a V and the arms held out|the spinning creature from behind, legs up and arms out
LIST

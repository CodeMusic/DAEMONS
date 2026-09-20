#!/bin/bash
# T-176 batch 4, the last seven. Concrete shapes throughout, by the rule the first three batches settled.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t176/alt4
mkdir -p $S
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
while IFS='|' read -r name body front back; do
  for seed in 1917 42; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, no face visible, $back, $G" --negative "face, eyes, mouth, looking at viewer, front view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
goldset|small flower-headed creature in a long leaf skirt, wide open bloom on its head, standing still|the open bloom and a calm face|the leaf skirt and the bloom from behind
heartbeat|large round egg-shaped creature with a pouch on its belly and short stubby arms, small tuft of hair|the pouch on its belly, a steady face|the round back and the short tail
proteus|lean angular creature with a crystalline core in its chest and long thin limbs, plates shifting|the core in its chest, thin limbs out|the plated back and the core showing through
abandon|round puffball creature with three cotton tufts hanging below it, drifting in the air|the round face and the tufts hanging below|the puffball from behind and its hanging tufts
buoyancy|broad flat ray-like creature with wide flat wings gliding, a long thin tail|the wide flat wings spread and a flat face|the broad flat back and the long tail
attachment|small fish creature with a wide sucker disc on top of its head, fins held close|the sucker disc on its head|the sucker disc from behind and the small tail fin
caprice|small round bud-headed creature with a closed bud on its head and two small leaves, on thin legs|the closed bud and two leaves|the bud from behind and the thin legs
LIST

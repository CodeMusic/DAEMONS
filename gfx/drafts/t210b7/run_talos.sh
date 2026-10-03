#!/bin/bash
# T-210 batch 7 (2026-10-02): the 13 legendaries, each an animal made mythic, drawn from their NAMES, one animal per family; FRONTS ONLY
# (batch 1 showed this recipe's backs mostly face the viewer: backs.py draws them with T-166's rear recipe). Two seeds,
# 512x512, a draft already drawn is skipped so a stopped run resumes.
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b7
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, dragon, wyvern, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body, colorful"
while IFS='|' read -r name body front; do
  [ -z "$name" ] && continue
  for seed in 88 7; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single legendary mythic creature based on a real animal, a $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
talos|bronze guardian bull made of riveted bronze plates, walking its rounds|the riveted bronze plates and glowing eyes
LIST

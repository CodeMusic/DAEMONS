#!/bin/bash
# T-165: PIXELBYTE -> FORGE (the SPRITEFORGE daemon), in the NUMEL -> CAMERUPT slot, ENTROPY/STRATUM.
# Drawn with the recipe they are named for: spriteforge.py driving pixelbyte's model, NIBBLE recipe (ai/README.md).
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t165/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, man, woman, knight, armour, skeleton, white body, pale body, grey background, colored background, floor, ground, grass, water surface, rocks, pedestal, base, frame, box, people, weapon, drop shadow, shadow, pink, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, border, lines"
F="side view, profile, rear view, $N2"
B="face, eyes, mouth, looking at viewer, side view, profile, front view, $N2"
while IFS='|' read -r name body front back; do
  for seed in 1917 42 7; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "$F" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, back of the head, no face visible, $back, $G" --negative "$B" 2>&1 | tail -1
  done
done <<'LIST'
pixelbyte|small puppy creature whose body is built from chunky square pixel blocks, a paw print mark on its side, a little cloud of glowing static sparks drifting off its back|big square eyes, one paw raised|the blocky back with the cloud of static sparks and a stubby tail
forge|large sturdy four-legged beast carrying a blacksmith forge on its back, a glowing furnace mouth and a small anvil, square pixel blocks cooling on its flanks|a determined face, the furnace glowing above its head|the forge and anvil on its back from behind, the furnace chimney
LIST

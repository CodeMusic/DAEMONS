#!/bin/bash
# T-210 batch 4, redrawn (2026-10-02): EPIPHANY's line as one real animal, drawn from their NAMES, one animal per family; FRONTS ONLY
# (batch 1 showed this recipe's backs mostly face the viewer: backs.py draws them with T-166's rear recipe). Two seeds,
# 512x512, a draft already drawn is skipped so a stopped run resumes.
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b4r
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, dragon, wyvern, fantasy creature, mythical creature, monster, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body, colorful"
while IFS='|' read -r name body front; do
  [ -z "$name" ] && continue
  for seed in 1917 42; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single real animal, a $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
inkling|small Draco gliding lizard with a hard bony rounded head, crouched, lowering its head to butt|the bony head and a determined face
gestalt|Draco gliding lizard curled tightly into a ball, its scaly armoured back and folded rib-wings wrapped around it like a shell, eyes peeking out|the curled armoured ball and the peeking eyes
epiphany|Draco gliding lizard gliding forward with its wide rib-supported skin wings spread out from its sides, long thin tail|the wide spread rib-wings and a sharp face
LIST

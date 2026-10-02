#!/bin/bash
# T-210 batch 2 (2026-10-02): the five Hoenn water families, drawn from their NAMES, one animal per family; FRONTS ONLY
# (batch 1 showed this recipe's backs mostly face the viewer: backs.py draws them with T-166's rear recipe). Two seeds,
# 512x512, a draft already drawn is skipped so a stopped run resumes.
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b2
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body, colorful"
while IFS='|' read -r name body front; do
  [ -z "$name" ] && continue
  for seed in 1917 42; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
tangent|sleek small tern seabird skimming forward with its wings held out perfectly straight like a ruled line|the straight wings and a focused face
jacobian|large pelican with an enormous throat pouch holding a neat grid of many small arrows pointing every way|the huge pouch full of little arrows and a calm face
undertow|small dark eel coiled low with a pale glowing eye and a long tapering tail|the glowing eye and the coiled body
riptide|long powerful moray eel surging forward, a narrow head and a strong body pulled straight|the narrow head and fierce eyes
saddle|plain flat dull flatfish lying still, both eyes on one side of its head, small fins|the flat body and the two eyes on top
optimum|long graceful sea serpent fish with trailing ribbon fins and a serene face, coiled elegantly|the trailing ribbon fins and a serene face
seepage|small damp turtle hatchling with a soft rounded shell and stubby legs, droplets on its shell|the droplets and a small curious face
aquifer|great old tortoise whose high domed shell holds a small calm lake on its top, thick legs|the lake on its shell and a wise old face
backflow|small round water beetle swimming backward, its legs paddling forward, a hard shiny shell|the round shell and the paddling legs
blackwater|large dark diving beetle with a broad armoured shell and strong grasping forelegs|the broad dark shell and the grasping forelegs
LIST

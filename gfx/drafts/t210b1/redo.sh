#!/bin/bash
# T-210 batch 1, two fronts redrawn: LASVEGAS (both seeds drew a man) and DELTA (the fanned tail never came).
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b1/redo
mkdir -p $S
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N="human, person, man, woman, humanoid, clothes, sword, weapon, hat, colored background, floor, ground, shadow, text, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, box"
for seed in 1917 42 88; do
  [ -f $S/lasvegas_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/lasvegas_front_$seed \
    --prompt "pure white background, pixel art game sprite of a single tall magpie bird standing upright on two strong bird legs, feathered wings folded like arms, a sharp black beak, a very long tail with round dice-like spots, a fighting stance, front view, facing the viewer, $G" --negative "side view, rear view, $N" 2>&1 | tail -1
  [ -f $S/delta_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/delta_front_$seed \
    --prompt "pure white background, pixel art game sprite of a single large broad beaver sitting up, an enormous flat tail spread wide behind it in a fan of branching channels like a river delta, powerful arms, a calm face, front view, facing the viewer, $G" --negative "side view, rear view, $N" 2>&1 | tail -1
done

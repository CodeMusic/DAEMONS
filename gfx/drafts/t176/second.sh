#!/bin/bash
# T-176 batch 1, second round: PUNCHCARD came back a lizard, SUBSTRATE a generic robot, OUTLIER a plain blob with
# no mark. Each prompt now names the thing its Index entry names, and what it must NOT be.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t176/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, grey background, colored background, floor, ground, pedestal, frame, box, drop shadow, text, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
while IFS='|' read -r name extra body front back; do
  for seed in 7 99 314; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_r2_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" \
      --negative "side view, profile, rear view, $extra, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_r2_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, no face visible, $back, $G" \
      --negative "face, eyes, mouth, looking at viewer, front view, side view, $extra, $N2" 2>&1 | tail -1
  done
done <<'LIST'
punchcard|lizard, dinosaur, reptile, animal, fur, scales|creature whose whole body is a stiff rectangular punched card, rows of small square holes cut across its flat torso, one corner clipped, two thin blade arms|the rows of punched holes across the flat card body and the blade arms|the flat back of the card, the same rows of holes showing through
substrate|robot, android, machine, screen, wires, humanoid|creature made of solid stacked slabs of material, thick and heavy and plain, like a block of stone or metal that stands, short blunt limbs|a flat plain front with one seam, no face features|the stacked slabs from behind, plain and heavy
outlier|pair, two creatures, twins, symmetrical markings|small round pale creature standing alone, with ONE conspicuous dark patch over one eye and one ear longer than the other, everything else plain|the single dark eye patch and the odd ear|the round back, one ear longer than the other
LIST

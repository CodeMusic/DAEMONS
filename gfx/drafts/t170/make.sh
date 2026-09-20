#!/bin/bash
# T-170 trial, second half: the first showed a 64px PORTRAIT does not survive reduction -- wrong proportions, no
# outline left. So ask for the overworld's own shape at 64px: two heads tall, a huge head, a thick black outline and
# flat colour, which is what a 16x32 frame is made of.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t170/alt
G="chibi game sprite, two heads tall, huge round head, tiny body, thick black outline, flat colours with one shade of shading, facing the viewer, standing, full body, isolated on pure white, centered, large in the frame, no shadow, no text"
N="realistic proportions, tall figure, human face, person, detailed shading, gradient, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  for seed in 1917 42; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_$seed \
      --prompt "pure white background, pixel art $body, $G" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
youngster|mouse boy in a blue and white striped shirt and brown shorts, red cap
crystal|fox scientist in a white lab coat over purple
tilt|toad in a purple waistcoat
LIST

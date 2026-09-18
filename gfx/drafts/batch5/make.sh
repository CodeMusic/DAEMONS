#!/bin/bash
# T-131 batch 5: the rest of the Doldrum area, Vermilion's SURGE and OVERFLOW, and the rival's first evolutions,
# 2026-09-18. SIX HAVE CONCEPTS and are redrawn from them exactly as batch 1 was (prepconcept on a chroma key, i2i
# 0.55, seed 1917); FIVE do not and are drawn from words as batches 3 and 4 were (two seeds per view).
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch5
P="pixel art game sprite, full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, flat solid green background, centered, no shadow, no text"
N="green body, green tint, pale body, drop shadow, shadow, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, border"
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
relay|relay.jpeg|a crested songbird carrying a sealed envelope in its beak
overflow|overflow.jpeg|a fat rat whose back is heaped with overlapping square tiles spilling over its sides, a long thin tail
surge|surge.jpeg|a muscular standing mouse with round ears and clenched fists, its long tail ending in a jagged lightning bolt
rubric|rubric.png|a boxy walking creature whose square body is a ruled grid table, two small eyes at the top and two short legs
locus|locus.png|a curved bean-shaped closed loop made of banded segments with round dots spaced along its edge
roverseer|roverseer.png|a large four-legged robot walker dog with a boxy armoured body and a small sensor head on top
LIST
S=$S/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, no shadow, no text"
N2="white body, pale body, grey background, colored background, floor, ground, grass, water surface, rocks, pedestal, base, frame, box, people, human, weapon, drop shadow, shadow, pink, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, border, lines"
F="side view, profile, rear view, $N2"
B="face, eyes, mouth, beak, looking at viewer, side view, profile, front view, $N2"
while IFS='|' read -r name body front back; do
  for seed in 1917 42; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "$F" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, back of the head, no face visible, $back, $G" --negative "$B" 2>&1 | tail -1
  done
done <<'LIST'
capsule|bivalve shellfish creature in a tightly closed ridged clam shell with a long tongue poking out|the shell barely open, two eyes in the dark gap|the ridged back of the closed shell
proof|small muscular humanoid creature with a ridged crest on its head, standing firmly|arms crossed, a steady serious face|the muscular back, the ridged crest
lull|chubby upright tapir-like creature with a short trunk nose and heavy-lidded sleepy eyes|drowsy half-closed eyes, arms held out|the round back, short tail, the back of its head
spinlock|round frog-like tadpole creature with a spiral swirl on its belly, gloved hands and legs|the spiral swirl on its belly, fists up|the round back, arms and legs
cookie|small cat creature sitting, a round coin charm on its forehead and a curled tail|whiskers, a sly smile|the back of its head and ears, the curled tail
LIST

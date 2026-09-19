#!/bin/bash
# T-131 batch 12: Victory Road, the League and the champion's teams --
# 2026-09-18. All twelve from words with the NIBBLE recipe (ai/README.md), two seeds per view, "small in the frame".
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch12/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, man, woman, knight, armour, skeleton, white body, pale body, grey background, colored background, floor, ground, grass, water surface, rocks, pedestal, base, frame, box, people, human, weapon, drop shadow, shadow, pink, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, border, lines"
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
pipeline|large upright horned beast with a thick tail, spiked back and a single long horn, broad chest|a fierce face, the horn, arms braced|the spiked back and thick tail
ferry|large gentle sea creature with a long neck, a round shell on its back and four flippers|a calm kind face on the long neck|the round shell from behind, the long neck rising
slurp|round pink-less creature with a huge long tongue curled out, stubby arms and a thick tail|the long tongue curled out, round eyes|the round back and thick tail
vice|large crab with one enormous claw much bigger than the other|the enormous claw raised, eyes on stalks|the rounded shell from behind, the enormous claw to one side
dragnet|large jellyfish creature with a wide dome head, two gem spots and many long trailing tentacles|two gem spots, tentacles spread wide|the dome and the spread tentacles from behind
coldvault|shellfish creature sealed inside a spiked spiral shell, only a dark gap showing|two eyes in the dark gap between the shell halves|the spiked shell from behind
tracker|sleek cat creature with a coin charm on its forehead, long tail and narrow eyes|narrow knowing eyes, sitting tall|the sleek back and the long tail
wiretap|three moles poking up out of the ground side by side, round noses|three faces with round noses|the backs of three round heads poking up
hauntproc|round grinning ghost creature with spiky back and short arms, wide red-less grin|a wide grin and narrow eyes|the spiky round back
coldread|tall slender frost creature with long flowing frosted hair and a calm face, arms folded into wide sleeves|a calm serene face, half closed eyes|the long flowing frosted hair from behind
resentment|round blue-less blob creature with a black tail with eyes on it, arms pressed to its sides|closed eyes, a flat patient face|the round back and the dark tail with eyes
fossilnet|winged prehistoric reptile with broad leathery wings, a jagged beak and a long tail|jagged teeth, wings spread wide|the broad wings spread from behind, the long tail
LIST

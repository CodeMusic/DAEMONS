#!/bin/bash
# T-176 batch 2: the islands' own, and the evolution arrivals -- the ones a player meets early on the water and in
# the grass. Same recipe: 512, two seeds per view, greyscale, "small in the frame".
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t176/alt2
mkdir -p $S
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, grey background, colored background, floor, ground, grass, water surface, pedestal, base, frame, box, people, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
F="side view, profile, rear view, $N2"
B="face, eyes, mouth, beak, looking at viewer, side view, profile, front view, $N2"
while IFS='|' read -r name body front back; do
  for seed in 1917 42; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "$F" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, no face visible, $back, $G" --negative "$B" 2>&1 | tail -1
  done
done <<'LIST'
trust|small round creature still half inside a cracked shell, facing forward|the shell halves and a trusting open face|the cracked shell from behind, a small round back
hope|small winged creature hovering just above the ground, short feathered wings held out|a calm upward face, wings out|the short wings from behind, hovering
mood|small round creature floating on water, a round body and a thin tail with a ball at the end|a placid face at water level|the round back and the ball-tipped tail
elation|round buoyant creature bobbing high, wide ears, a thin tail with a ball at the end|a bright wide-eyed face|the round buoyant back and the tail
lookout|very long slender creature standing upright on its hind legs, stretched tall to see|a watchful face at the top of a long body|the long slender back, standing tall
cunning|sleek dark creature with sharp claws and a single ear feather, waiting|narrow patient eyes, claws ready|the sleek back and the ear feather
torpor|slow round amphibian creature with a wide flat mouth, drifting|a blank wide-mouthed face|the round back and the flat tail
prescience|upright bird standing perfectly still with long legs and wide patterned wings|wide unmoving eyes, wings folded|the patterned wings from behind, standing still
entrapment|long-legged spider creature waiting on a finished web|many eyes, legs braced|the striped back and the long legs
gathering|round beetle creature with spotted shell and small wings, one of many|a friendly face, spots on the shell|the spotted shell from behind
buildup|woolly four-legged creature with a heavy tail, fleece standing on end with charge|a nervous face, fleece raised|the woolly back and the heavy tail
release|tall four-legged creature with a bright round lamp at the tip of its tail, striped|a calm face, the lamp glowing|the striped back and the tail lamp held high
LIST

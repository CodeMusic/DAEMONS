#!/bin/bash
# T-131 batch 7: Lavender and Halftone Tower, Routes 7, 8, 12 and 16, and Celadon's benchmark and the hideout
# beneath its Game Corner, 2026-09-18. None has a concept (gfx/front/ is spent), so all twelve are drawn from words
# with the NIBBLE recipe (ai/README.md), two seeds per view, chosen in PICKS.txt.
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch7/alt
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
wisp|small round ghostly gas ball with a wide grin, trailing wisps of vapour around it|wide eyes and a grin, wisps of vapour trailing|the round back of the gas ball, wisps of vapour trailing
dualcore|two-headed running bird with two round heads on long necks and long legs, no wings|both heads facing the viewer, one looking left and one right|the backs of both heads on their long necks, long legs
revenant|floating ghost with a spiked head, two detached clawed hands and a wide grin|the grin and narrowed eyes, both hands raised|the spiked back of its head, the two hands floating either side
bootstrap|cluster of six round eggs huddled together, each with a small face|six small faces, each looking a different way|the six round eggs from behind, cracks in their shells
blight|drooping plant creature with a large wilted flower on its head, dripping|half-closed eyes, a drop of fluid hanging from its mouth|the wilted flower from behind, drips falling
honeypot|pitcher plant creature with a large open bell-shaped mouth and a leaf on either side|the wide open mouth of the pitcher, a hooked lid above|the back of the pitcher, the stem and two leaves
outbreak|large cobra reared up with a hood marked with a pattern of repeated shapes|the spread hood, the pattern on it, fangs|the back of the spread hood, the coiled tail below
partition|upright armadillo-like mammal with long sharp spines down its back and big claws|long claws raised, a serious face|the long spines down its back in rows, the tail
ramrod|stocky armoured rhino-like beast with a single horn and plated hide, charging|the horn pointed at the viewer, head low|the plated back and the stub of its tail
mite|small round fuzzy bug with big compound eyes, two antennae and small legs|big round compound eyes, antennae up|the fuzzy round back, the antennae
tracer|large bat with a huge open mouth, big wings and small feet|the wide open mouth, fangs, wings spread|the backs of its wide wings, small feet
spaghetti|round tangled mass of long thin vines with two eyes peering out and two red feet|two eyes peering out of the tangle|the tangle of vines from behind, the feet
LIST

#!/bin/bash
# T-131 batch 3: Mt. Moon and Route 4, 2026-09-18. None has a concept and vanilla's sprites are never fed in, so
# all nine are drawn from words with the NIBBLE recipe (ai/README.md): the body kept recognisable, the detail from
# the name and Index entry. Batch 2's lessons are in the negative (ground, grass, pedestal, frame, weapons) and in
# the "seen from directly behind ... no face visible" rear wording; two seeds per view, chosen in PICKS.txt.
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch3/alt
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
echo|small bat with no eyes, huge pointed ears and wide spread wings|its wide open mouth calling out, fangs, hovering|the backs of its huge ears, wings spread wide on either side
anomaly|small plump round fairy creature with pointed ears, a curl of hair on its forehead and tiny wings|a calm round face, stubby arms, standing|the round back, tiny wings, a curled tail
payload|small six-legged beetle bug carrying two large round mushroom caps strapped to its back|small pincers, beady eyes, the two caps above it|the two large mushroom caps on its back, little legs below
nozzle|small seahorse with a long thin tube snout, a curled tail and a fin on its back|the tube snout pointed at the viewer, upright|the back fin and curled tail, the back of its head
pincer|crab with one claw much larger than the other|the huge claw raised in front, small claw lowered, eyes on stalks|the rounded shell, the huge claw to one side
stub|plain flat fish flopping on its tail, round blank eyes, an open mouth and two whiskers|a blank stare, fins flared|the flat side of its back, the tail fin, the dorsal fin
escalate|huge long sea serpent coiled upright, with crest fins along its back|a gaping fanged mouth, whiskers, rearing up|the crest fins down its back, the coil below
fault|duck-like creature holding its head with both hands|blank dazed round eyes, a flat bill, three hairs on top|both hands clasped to the back of its head, three hairs on top
driftnet|jellyfish with a clear dome head and two round gem spots|long trailing tentacles hanging below|the dome from behind, tentacles trailing below
LIST

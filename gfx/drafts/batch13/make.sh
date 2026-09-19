#!/bin/bash
# T-131 batch 13: the last of the League and the champion's teams, and LEMMA MIND (a space in its name) --
# 2026-09-18. All ten from words with the NIBBLE recipe (ai/README.md), two seeds per view, "small in the frame".
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch13/alt
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
lemma_mind|large muscular four-armed creature with a ridged crest and a belt, all four arms braced|a calm determined face, four fists|the broad back and four arms, the crest
bulldozer|huge armoured rhino-like beast standing upright on two legs with a drill horn and thick tail|the drill horn pointed forward, heavy fists|the plated back and thick tail
singular|large friendly round dragon with small wings, two antennae and a pale belly|a calm gentle face, arms at its sides|the round back and the small wings, the tail
impulse|round shaggy boar creature covered in long hair hiding its eyes, two tusks|two tusks poking out of the shaggy hair|the shaggy round back
dread|small floating ghost with long wavy hair like a veil and a round head, red beads at its neck|large wide eyes peering out|the long wavy hair from behind
hardline|huge serpent made of a chain of large square metal blocks, a heavy jaw|the heavy jaw and small eyes, rearing up|the chain of square blocks coiling away
multicast|bat with four wings, two large and two small, a wide mouth|the wide mouth, four wings spread|the four wings spread from behind
turbulence|seahorse dragon with curled fins, a long snout and a spiral tail|the long snout, curled fins|the curled back fins and spiral tail
drive|large beetle with a single tall horn, thick armoured body, standing on two legs|the tall horn above its head, arms braced|the armoured shell back and folded wings
grievance|huge armoured reptile with spiked plates down its back, a heavy tail and thick claws|a fierce face, claws raised|the spiked plates down its back and the heavy tail
LIST

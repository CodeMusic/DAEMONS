#!/bin/bash
# T-131 batch 4: the Mt. Moon trainers, the Doldrum routes and BASIN, 2026-09-18. None has a concept and vanilla's sprites are never fed in, so
# all eleven are drawn from words with the NIBBLE recipe (ai/README.md): the body kept recognisable, the detail from
# the name and Index entry. Batch 2's lessons are in the negative (ground, grass, pedestal, frame, weapons) and in
# the "seen from directly behind ... no face visible" rear wording; two seeds per view, chosen in PICKS.txt.
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch4/alt
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
sentinel|small floating round metal orb with one large eye and a horseshoe magnet on each side, screws in its body|the single eye watching the viewer, hovering|the round back of the orb, a magnet on each side
fuse|round ball creature with a band around its middle and a small fuse cap on top|narrowed angry eyes, still|the smooth round back, the band and the fuse cap
sludge|blob of thick oozing sludge with drippy arms and bits of scrap stuck in it|a wide gaping mouth and small eyes, arms raised|the lumpy back of the blob, drips running down
fumes|round floating gas ball with vents and craters leaking small puffs of smoke|a grinning face, puffs of smoke around it|the round back with its vents, puffs of smoke
spawn|small fish with a single horn on its forehead and long flowing fins and tail|swimming upright, fins flowing|the horn and flowing fins from behind, long tail
loop|round tadpole with a spiral swirl on its belly and a long tail|big eyes, the spiral swirl on its belly, standing on small feet|the round back, the long tail curling
hunch|small fox-like creature sitting cross-legged fast asleep, with long pointed ears and a thick tail|eyes closed, calm, arms folded|the back of its head and pointed ears, the thick tail curled round
snare|thin plant creature with a bell-shaped flower head, leaf arms and root feet|the bell head's wide open mouth, leaf arms out|the back of the bell-shaped head, the thin stem body, leaf arms
weed|small round bulb creature with a tuft of five long leaves on top and little feet|two small eyes, standing|the round bulb from behind, the tuft of leaves above
beacon|five-pointed star creature with a round gem in its centre|the gem in the centre facing the viewer, standing on two points|the plain back of the star, five points
pulsar|creature made of two overlapping five-pointed stars with a large gem in its centre|the large gem facing the viewer, ten points spread|the plain back of the overlapping stars
LIST

#!/bin/bash
# T-131 batch 6: Vermilion to Rock Tunnel, Diglett's Cave, and five evolutions that have concepts, 2026-09-18.
# FIVE HAVE CONCEPTS and are redrawn from them as batch 1 was (prepconcept on a chroma key, i2i 0.55, seed 1917);
# SEVEN do not and are drawn from words as batches 3-5 were (two seeds per view).
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch6
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
indexer|indexer.jpeg|a large moth with broad wings patterned in a chequered grid of squares, a thin segmented body and antennae
injector|injector.jpeg|a segmented wasp with translucent wings, a long needle stinger and two drill-like forelimbs
flood|flood.jpeg|a large bird with a very long thin pointed beak, a ruffled crest and wide wings
broadcast|broadcast.jpeg|a large crested bird with wings spread wide and a long fanned tail
hibernate|hibernate.jpeg|a round plump rabbit-eared puffball creature with long drooping ears, eyes closed asleep
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
sentry|alert dog with a shaggy mane and a bushy tail, standing watch|ears pricked, watching the viewer steadily|the shaggy mane and bushy tail from behind, ears up
hotpath|slim running horse with a flowing mane and tail like streaks of heat|mid-gallop toward the viewer, streaming mane|the flowing tail and mane streaming back, hooves
inference|upright fox-like creature holding a bent spoon, a star on its forehead, long moustache whiskers|the spoon held up, narrowed thoughtful eyes|the back of its head and pointed ears, the thick tail
latency|large slow lounging creature with a long curled tail, heavy lidded eyes and a blank smile|sitting, a vacant smile, long tail curling beside it|the round back, the long tail curling
stack|round creature made of stacked boulders with four stubby stone arms|a stern face in the top boulder, arms braced|the stacked boulders of its back, arms at the sides
relic|small creature wearing the skull of a larger animal as a helmet, holding a bone club|eyes shadowed under the skull helmet|the back of the skull helmet, the bone club held behind
tappoint|small mole poking up out of a hole, only its head and shoulders showing, a round nose|small eyes and a big round nose|the back of its round head poking up out of the hole
LIST

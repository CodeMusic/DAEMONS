#!/bin/bash
# T-131 batch 2: SLATE's benchmark and Route 3, 2026-09-18. PING and SUSPEND have approved concepts and are
# redrawn from them exactly as batch 1 was (i2i 0.55). The other seven have NO concept, and vanilla's sprites
# are never fed in (this repo carries no Nintendo-derived art): they are drawn from words with the NIBBLE
# recipe (ai/README.md) -- one seed, mirrored front and rear prompts -- the body kept recognisable, the
# detail taken from the daemon's name and Index entry.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch2
P="pixel art game sprite, full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, flat solid green background, centered, no shadow, no text"
N="green body, green tint, pale body, drop shadow, shadow, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, border"
mkdir -p $S/src
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
ping|ping.jpeg|a small fierce sparrow bird with a short sharp beak, ruffled head feathers and spread wings
suspend|suspend.jpeg|a round balloon-like puffball creature with big closed eyes and a curl of hair on its forehead
LIST
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, no shadow, no text"
N2="white body, pale body, grey background, colored background, drop shadow, shadow, pink, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, border, lines"
while IFS='|' read -r name body front back; do
  python3 tools/spriteforge.py t2i --size 512x512 --seed 1917 --out $S/${name}_front \
    --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" \
    --negative "side view, profile, rear view, $N2" 2>&1 | tail -1
  python3 tools/spriteforge.py t2i --size 512x512 --seed 1917 --out $S/${name}_back \
    --prompt "pure white background, pixel art game sprite of a single $body, rear view, facing away from the viewer, back of the head, $back, $G" \
    --negative "face, eyes, mouth, side view, profile, front view, $N2" 2>&1 | tail -1
done <<'LIST'
heap|small heap of rough stacked rocks with two stubby stone arms|a grumpy face in the front rock, arms held out|the back of the rock pile, arms at its sides
backbone|huge serpent made of a long chain of large rounded stone blocks like vertebrae|a horned stone head rearing up, the chain coiling behind it|the chain of stone blocks coiling away, the back of the horned head
sector|small upright armadillo-like mammal whose back is plated with square tiles in a neat grid|round ears, small claws, sitting up|the grid of square tiles across its back, a short tail
worm|coiled snake whose long body is made of identical repeating segments|its head raised, tongue out, coils below|the segmented coils seen from behind, the back of its head
preempt|round furry pig-nosed monkey with clenched fists|an angry face, fists raised, mid-leap|the round furry back, fists raised to either side
fork|small spiky rabbit-like creature with big ears and two identical short tails|a short horn split into two equal prongs, small spines along its back|two identical short tails, spines down its back, big ears
branch|small spiky rabbit-like creature with large upright ears|a tall horn that branches into two tines like a forked branch|spines down its back, the branching horn above its ears
LIST

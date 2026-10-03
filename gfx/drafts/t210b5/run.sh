#!/bin/bash
# T-210 batch 5 (2026-10-02): the early Hoenn routes, drawn from their NAMES, one animal per family; FRONTS ONLY
# (batch 1 showed this recipe's backs mostly face the viewer: backs.py draws them with T-166's rear recipe). Two seeds,
# 512x512, a draft already drawn is skipped so a stopped run resumes.
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b5
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, dragon, wyvern, fantasy creature, mythical creature, monster, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body, colorful"
while IFS='|' read -r name body front; do
  [ -z "$name" ] && continue
  for seed in 1917 42; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single real animal, a $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
smudge|small hyena pup with sooty smudged fur, crouching low|the sooty smudges and a sly face
eclipse|large hyena with a jet black coat and a thin pale rim of light around its outline, standing tall|the black coat and narrow pale eyes
detour|small raccoon cub with zigzag stripes on its fur, mid-step as if wandering off to one side|the zigzag stripes and a curious face
unbranched|long low sleek raccoon stretched out running perfectly straight, straight stripes along its back|the long straight body and a focused face
warmup|tiny baby squirrel hanging from a small twig by its paws|the little twig and a sleepy face
shaping|squirrel standing up holding an acorn as a prize, with a sly grin|the acorn and the sly grin
policy|large squirrel with a huge fanned tail like a leaf, standing stern and certain|the fanned tail and a stern face
shortjump|small barn swallow hopping between two close perches|the short wings and a bright face
longjump|barn swallow with a long forked tail in fast flight, wings swept back|the swept wings and the forked tail
sparring|young kangaroo joey wearing small boxing gloves, hopping|the little gloves and an eager face
checkmate|tall muscular kangaroo in a boxing stance with big gloves raised|the raised gloves and a calm face
lowbit|tiny rabbit with its long ears folded down, whispering|the folded ears and a shy face
shiftleft|rabbit with big ears flared like megaphones, shouting|the megaphone ears and an open mouth
wraparound|large hare with huge loudspeaker-shaped ears and a wide open mouth|the loudspeaker ears and the open mouth
loopback|kitten curled in a circle chasing its own tail|the curled tail and a playful face
quine|elegant long-haired cat sitting very upright, perfectly symmetrical, calm|the symmetrical pose and a calm face
laced|orchid mantis that looks exactly like a pink flower, with tiny thorny forelegs|the petal-shaped legs and small eyes
syn|small firefly beetle with a bright glowing tail, wings open|the glowing tail and big eyes
ack|small round firefly beetle with a softly glowing tail, wings folded|the glowing tail and gentle eyes
LIST

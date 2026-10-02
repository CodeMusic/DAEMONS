#!/bin/bash
# T-210 batch 4 (2026-10-02): the dragons and fossils, drawn from their NAMES, one animal per family; FRONTS ONLY
# (batch 1 showed this recipe's backs mostly face the viewer: backs.py draws them with T-166's rear recipe). Two seeds,
# 512x512, a draft already drawn is skipped so a stopped run resumes.
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b4
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body, colorful"
while IFS='|' read -r name body front; do
  [ -z "$name" ] && continue
  for seed in 1917 42; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
sinkhole|antlion larva with huge curved pincer jaws sitting at the bottom of a small cone-shaped sand pit|the big pincer jaws and small eyes
shimmer|slender antlion insect with four long clear veined wings beating so fast the air around it shimmers|the long clear wings and large round eyes
dustdevil|large antlion insect with four long wings spread wide inside a spinning swirl of sand and dust|the spinning sand swirl and red eyes
datagram|small round dove with a tiny tied bundle on one foot, fluffy wings|the little bundle and a bright face
tradewind|large graceful dove whose wings are made of soft white cloud, gliding|the cloud wings and a calm face
inkling|small stubby lizard with a hard bony rounded head, lowering its head to butt|the bony head and a determined face
gestalt|lizard curled tightly into a ball inside a hard rocky armoured shell, only its eyes peeking out|the round rocky shell and the peeking eyes
epiphany|flying lizard with wide skin wing flaps spread out from its sides, gliding forward|the wide spread wing flaps and a sharp face
savestate|small sea lily crinoid on a short stalk with frilly feathery arms, its body like carved fossil stone|the feathery arms and a small stone face
warmstart|tall sea lily crinoid on a long stalk with many long feathery arms grown out, stone and living parts mixed|the many feathery arms and a calm stone face
tokenring|small horseshoe crab holding a round flat token in one claw|the round token and the curved shell
trunkline|huge armoured horseshoe crab with a long spiked tail and a heavy ridged shell, rearing up|the heavy ridged shell and the long tail spine
LIST

#!/bin/bash
# T-210 batch 6 (2026-10-02): the last batch before the legendaries, drawn from their NAMES, one animal per family; FRONTS ONLY
# (batch 1 showed this recipe's backs mostly face the viewer: backs.py draws them with T-166's rear recipe). Two seeds,
# 512x512, a draft already drawn is skipped so a stopped run resumes.
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b6
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, dragon, wyvern, fantasy creature, mythical creature, monster, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body, colorful"
while IFS='|' read -r name body front; do
  [ -z "$name" ] && continue
  for seed in 1917 42; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single real animal, a $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
glidepath|colugo gliding downward with its wide skin flaps stretched between its limbs|the wide skin flaps and big round eyes
postulate|brown bear cub standing with its feet planted wide, immovable|the planted feet and a stubborn face
deduction|huge brown bear pushing forward with both front paws, heavy and steady|the pushing paws and a calm heavy face
backdoor|aye-aye lemur crouching in the dark with huge shining eyes and one long thin finger|the shining eyes and the long thin finger
honeytrap|alligator snapping turtle with its huge mouth open and a pink worm-shaped lure on its tongue|the open jaws and the pink lure
bootrom|tiny baby pangolin curled half open, covered in hard overlapping scales|the overlapping scales and a small face
firmware|pangolin standing on its hind legs with thick overlapping armoured scales|the thick armoured scales and a steady face
bigiron|enormous giant pangolin with heavy plated armour scales, standing firm like a fortress|the heavy plated armour and an old face
crackle|dingo pup whose fur stands on end and crackles with static sparks|the bristling fur and bright eyes
arcflash|lean dingo with a bristling crackling mane, a bright electric arc jumping from its mane|the crackling mane and a fierce face
anode|harvest mouse with red cheeks and a plus-shaped mark on its fur|the red cheeks and a cheerful face
cathode|harvest mouse with blue cheeks and a minus-shaped mark on its fur|the blue cheeks and a cheerful face
slowburn|old tortoise with grey smoke rising slowly from vents in its shell|the smoking shell and a sleepy face
hashcode|red panda wobbling on its hind legs, covered in irregular random spots|the random spots and a dizzy face
fewshot|small thorny devil lizard covered in spikes, sitting very still|the spikes and a patient face
zeroshot|large thorny devil lizard standing upright at night, spikes and a knowing look|the spikes and a sly knowing face
pristine|mongoose standing alert with clean bright white fur and one red stripe|the clean white fur and sharp eyes
forgery|long dark snake coiled with a sharp blade-shaped tail|the blade tail and narrow eyes
lilendian|Asiatic moon bear sitting with a pale crescent mark on its chest|the crescent mark and a calm face
bigendian|sun bear standing with a round golden mark on its chest|the golden chest mark and a bright face
transfer|giraffe with leaf-shaped ears and a bunch of fruit hanging from its neck|the hanging fruit and a gentle face
overtone|white bellbird perched with its beak open, ringing a bell-like call|the open beak and a calm face
redacted|white arctic fox sitting with a dark band of fur across its eyes like a blackout bar|the dark band across its eyes
lockfile|small round snowy owl chick sitting perfectly still, frost on its feathers|the still frosted feathers and big eyes
stalemate|huge snowy owl frozen perfectly still, thick ice on its feathers|the frozen feathers and a fixed stare
LIST

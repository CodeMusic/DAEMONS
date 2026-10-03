#!/bin/bash
# T-210 batch 7 (2026-10-02): the 13 legendaries, each an animal made mythic, drawn from their NAMES, one animal per family; FRONTS ONLY
# (batch 1 showed this recipe's backs mostly face the viewer: backs.py draws them with T-166's rear recipe). Two seeds,
# 512x512, a draft already drawn is skipped so a stopped run resumes.
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b7
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, dragon, wyvern, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body, colorful"
while IFS='|' read -r name body front; do
  [ -z "$name" ] && continue
  for seed in 1917 42; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single legendary mythic creature based on a real animal, a $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
pontus|colossal ancient deep-sea whale with barnacled skin and faint glowing markings|the huge calm eye and the barnacled skin
gaia|vast ancient tortoise carrying a mountain of earth, stone and roots on its back|the mountain on its back and an old calm face
ouranos|long sky eel coiling through the air with wide feathered fins and a cloud-pale belly|the feathered fins and a long proud head
boreas|white wolf of the north wind with a long frosty mane streaming like wind and one phoenix feather on its brow|the streaming mane and the single feather
brontes|great tiger whose stripes are jagged lightning, with one phoenix feather on its brow|the lightning stripes and the single feather
typhon|great lion with a smouldering mane of embers like a volcano, with one phoenix feather on its brow|the ember mane and the single feather
talos|bronze guardian bull made of riveted bronze plates, walking its rounds|the riveted bronze plates and glowing eyes
deucalion|ram made of stacked stones and boulders, with curling stone horns|the stacked stones and curling horns
khione|stag carved from clear ice with frosted antlers like branches of snow|the clear ice body and frosted antlers
castor|sleek dark blue swan with sharp swept wings, mythic and gleaming|the swept wings and a calm dark face
polydeuces|sleek pale red and white swan with soft swept wings, mythic and glowing|the soft swept wings and a gentle face
kairos|tiny hummingbird with a long forelock crest, its wings blurred like time passing, hovering|the blurred wings and the long forelock
elpis|small white moth with star-shaped wings resting on the rim of an open clay jar|the star-shaped wings and a small hopeful face
LIST

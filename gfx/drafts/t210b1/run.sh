#!/bin/bash
# T-210 batch 1 (2026-10-02): the six starter lines of Johto and Hoenn, drawn from their NAMES (the user: "draw them
# from their names") -- never from the vanilla creature. One animal per family so the line holds; concrete shapes,
# by T-176's rule. A draft already drawn is skipped, so a stopped run resumes. Two seeds each, front and back, at 512x512 (cleandraft.py's recipe).
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b1
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body"
while IFS='|' read -r name body front back; do
  [ -z "$name" ] && continue
  for seed in 1917 42; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
    [ -f $S/${name}_back_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, no face visible, $back, $G" --negative "face, eyes, mouth, looking at viewer, front view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
primer|tiny fawn with big ears and a single broad leaf growing from its forehead like an open page, stubby legs|the single leaf on its forehead and a calm face|its back and the leaf from behind
syllabus|young deer with a neat row of leaves running in order down its neck and back, slender legs|the row of leaves and an attentive face|the neat row of leaves down its back
curriculum|tall gentle deer with a full mane of leaves arranged in tidy rings and a wide flower collar, long legs|the flower collar and a kind face|the rings of leaves down its back and the flower collar
tepid|small newt-like salamander with a faint warm glow along its back, short legs, a long tail|the warm glow and a sleepy face|the glowing back and the long tail
seethe|lean salamander with wavering flickering flames all along its spine, crouched, a long tail|the flames along its spine and a restless face|the flames running down its spine and the tail
heatdeath|large calm salamander whose whole body glows evenly, thin wisps rising from it, eyes closed, a heavy tail|the evenly glowing body and its closed eyes|the glowing back, the wisps and the heavy tail
learnrate|small otter pup mid-pounce with oversized paws and an open mouth, a short thick tail|the big paws and an eager face|the round back and the short thick tail
momentum|sleek otter sliding forward on its belly with its paws tucked in, a long streamlined body|a determined face and tucked paws|the streamlined back and the long tail
steepest|large powerful river otter diving head-first downward, strong forelegs, a thick rudder tail|the strong forelegs and a fierce focused face|the broad back and the thick rudder tail
stump|small creature whose body is a short round tree stump with one leaf sprouting from the top and tiny legs|the leaf on top and two small eyes in the bark|the stump body and the single leaf from behind
boosting|slim sapling creature with many small leaves each a slightly different shape, leaning forward eagerly, thin legs|the many small leaves and a keen face|the thin trunk back and the uneven leaves
canopy|tall tree creature with a wide crown made of many smaller trees, thick trunk legs, standing like a guardian|the wide crown and a steady face in the trunk|the thick trunk back and the wide crown of small trees
coinflip|small round magpie chick holding a single round coin in its beak, fluffy, stubby wings|the coin in its beak|the fluffy back and the stubby wings
montecarlo|young magpie with a spray of tail feathers spotted like dice, standing alert on two legs|the dice-spotted tail fanned out and a sharp eye|the dice-spotted tail feathers from behind
lasvegas|tall magpie warrior standing upright in a fighting stance, long dice-spotted tail, strong legs ready to kick|the fighting stance and a certain, unhurried face|the long dice-spotted tail and the upright back
runoff|small beaver kit dripping with water, a flat paddle tail, little front teeth|dripping water and a curious face|the wet back and the flat paddle tail
alluvium|stocky beaver whose fur is banded in layers like stacked mud, a broad flat tail, standing on hind legs|the layered bands across its body and front teeth|the layered bands down its back and the flat tail
delta|large broad beaver whose huge flat tail spreads out in a fan of channels like a river delta, powerful arms|powerful arms and a calm face|the huge fan-shaped tail spreading in channels
LIST

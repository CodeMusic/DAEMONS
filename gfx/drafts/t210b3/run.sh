#!/bin/bash
# T-210 batch 3 (2026-10-02): the rest of the water-typed families, drawn from their NAMES, one animal per family; FRONTS ONLY
# (batch 1 showed this recipe's backs mostly face the viewer: backs.py draws them with T-166's rear recipe). Two seeds,
# 512x512, a draft already drawn is skipped so a stopped run resumes.
cd "$(dirname "$0")/../../.."
S=gfx/drafts/t210b3
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, white body, pale body, colorful"
while IFS='|' read -r name body front; do
  [ -z "$name" ] && continue
  for seed in 1917 42; do
    [ -f $S/${name}_front_$seed.png ] || python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
tempo|small round frog sitting on a floating lily pad tapping one foot in rhythm|the tapping foot and a cheerful face
cadence|frog standing up on two legs mid-step as if marching in time, long legs|the marching step and a focused face
cyclical|big jolly frog dancing on two legs with a wide lily pad on its head like a hat, arms out|the lily pad hat and a joyful dancing face
particle|tiny long-legged mayfly nymph skating on the water surface on thin legs|the thin legs spread wide and small eyes
flocking|mayfly with two pairs of broad wings marked with large round eyespots, hovering|the eyespot wings spread and a small face
oldbranch|small branching coral creature with stubby legs and several coral branches, one branch broken and regrowing|the branches and a small face in the coral
bifurcate|small round oyster creature with its shell slightly open showing a single shining pearl inside|the open shell and the pearl
deepwell|deep sea anglerfish with a long narrow body, a glowing lure on its head and needle teeth|the glowing lure and the toothy face
shallows|broad flat ray creature with wide gentle wing fins and a calm face, gliding|the wide flat fins and a calm face
confluence|small round fish with two tails curving together into one shape, small fins|the two curving tails and a sweet face
stillrun|ancient armoured coelacanth fish with heavy old scales, lobed fins and a stern face|the heavy scales and the lobed fins
stopgrad|small woolly mammoth calf covered in frost and icicles, short tusks, standing very still|the frosted fur and a still face
permafrost|huge woolly mammoth with long icy curved tusks and frost on its shaggy coat, standing firm|the long icy tusks and a heavy old face
LIST

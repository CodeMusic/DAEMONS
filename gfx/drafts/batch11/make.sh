#!/bin/bash
# T-131 batch 11: the rest of Fuchsia to Cinnabar -- Seafoam, the Power Plant, Saffron's and Cinnabar's trainers --
# 2026-09-18. All eleven from words with the NIBBLE recipe (ai/README.md), two seeds per view, "small in the frame".
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch11/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
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
cryogen|sleek seal creature with a horn on its head, long flowing tail flippers and a thick smooth body|a calm face, the horn, lying upright|the smooth long back and tail flippers, the horn
dynamo|upright stocky creature with striped fur, small antennae and fists crackling with sparks|fists raised, an intense face|the striped back and the antennae
shell|slow creature with a big spiral seashell clamped onto its tail, sitting upright|a vacant calm face|the spiral shell clamped on its tail from behind
flicker|small fox cub with six curled tails and a tuft of curled hair on its head|bright eyes, sitting|the six curled tails fanned out behind it
wildfire|elegant fox with nine long flowing tails and a thick mane|a calm knowing gaze, standing tall|the nine flowing tails fanned out, the mane
conjecture|upright fox-like creature holding a bent spoon in each hand, a long drooping moustache|eyes closed in thought, spoons held out|the back of its head and pointed ears, spoons at its sides
axiomkick|lean creature with no neck and extremely long springy legs, kicking one leg straight out|narrow eyes in its body, one leg kicked out|the back and the long coiled legs
rebuttal|upright creature wearing big padded boxing gloves and a short skirt of armour|gloves raised in a guard, a steady face|the back and the two gloves raised
overdrive|slim galloping horse with a single horn and a long streaming mane and tail|mid-gallop, horn forward, mane streaming|the streaming mane and tail from behind
scheduler|large armoured creature with a spiked back, heavy tail and thick arms, upright|a stern face, arms at its sides|the broad spiked armoured back and thick tail
guardian|large noble dog with a thick shaggy mane and tufted tail, standing firm|a calm watchful face, head high|the thick mane and tufted tail from behind
LIST

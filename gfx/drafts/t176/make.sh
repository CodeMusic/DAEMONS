#!/bin/bash
# T-176 batch 1: twelve daemons a player MEETS that T-131 missed -- they arrive by evolution, gift or legendary,
# and its meetable list came from wild tables and scripts. Same NIBBLE recipe as T-131: 512, two seeds per view,
# "small in the frame", greyscale so gbasprite.py can colour by type.
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/t176/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, grey background, colored background, floor, ground, grass, water surface, rocks, pedestal, base, frame, box, people, weapon, drop shadow, shadow, pink, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
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
mutex|muscular amphibian creature standing upright with one clenched fist held closed in front of it, broad shoulders|the closed fist held out, a steady stare|the broad back and the arm holding something closed
monolith|huge boulder creature curled into one sealed sphere, no seams, short thick limbs tucked in|a single slot of an eye in the stone|the smooth sealed back of the sphere
forge|creature made of banked embers with a chimney vent on its shoulder, holding a shaped ingot|the glowing vent and the ingot|the chimney vent and the heat rising from its back
drum|round sealed drum creature spinning on its axis, a hard rim at each end|the sealed face of the drum, small eyes on the rim|the spinning drum from behind, the far rim
punchcard|flat card-shaped creature with rows of punched holes and a sharp cutting jaw|the cutting jaw and rows of holes|the flat back of the card, the punched rows
magtape|spiral shell creature with a ribbon of tape wound round it, the loose end trailing|the wound spiral and the tape end|the spiral from behind, the tape trailing
mainframe|huge cabinet-shelled creature with a wide spiral front and heavy panels, too heavy to move|the spiral front and a row of small lights|the heavy panelled back of the cabinet
substrate|blocky angular creature with a solid material body, plain and heavy, unlike the others|a flat plain face, blocky limbs|the flat blocky back
blocking|armoured beetle with a huge pair of pincers held closed|the pincers closed in front of it|the armoured back and the closed pincers
edgecase|slim bird standing on one leg, carrying a single odd object under its wing|the odd object held close|the back and the object tucked under the wing
triplecore|three-headed bird, each head facing a different direction, long necks|three heads looking three ways|the three necks from behind
outlier|small round creature standing apart, plain and unremarkable, one mark that sets it apart|a plain face and the one odd mark|the round back and the mark
LIST

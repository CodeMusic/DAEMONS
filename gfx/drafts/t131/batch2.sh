#!/bin/bash
# T-131 round 2. Round 1 failed in exactly two ways, and both are prompt problems rather than model problems:
#
#   THE DEFINING FEATURE WENT MISSING on five. FAKEROOT drew a plain TREE with no creature in it; DUPLEX drew a
#   horse with an ordinary tail and no second head; QUOTA drew a flower on a stem with nobody inside it; PILOT lost
#   its two lamps; STARVED drew a creature wearing a leaf rather than a seed. Each is now asked for as a CREATURE
#   first and the feature second -- the shape rule T-176 settled, applied one level deeper.
#
#   THE BACKS CAME BACK AS FACES. "Seen from directly behind" was not enough; almost every back view returned eyes.
#   The back prompt now says what is toward the viewer and the negative names every facial part.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t131/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
NBACK="face, eyes, mouth, beak, nose, snout, looking at viewer, head turned toward viewer, front view, three-quarter view"

# ---- the five that lost their defining feature: front and back again
while IFS='|' read -r name body front back extra; do
  for seed in 7 1917; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_r2$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, profile, rear view, $extra, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_r2$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind with its back toward the viewer, $back, $G" --negative "$NBACK, $extra, $N2" 2>&1 | tail -1
  done
done <<'LIST'
fakeroot|stocky two-legged creature whose body is a thick knotted brown tree trunk, with two arms raised and a round clump of leaves on the end of each arm, and a small face on the trunk|the small face on the trunk and the two raised arms|the back of the trunk and the two clumps above it|plain tree, forest, oak tree, tree without limbs, roots, grass, leaves only
duplex|long-necked four-legged creature whose upright tail ends in a SECOND HEAD with its own eyes and mouth, both heads alert|the front head, and the tail head raised behind it|both heads from behind, the tail head facing away from the viewer|plain horse, ordinary tail, one head, deer, unicorn
quota|small two-legged creature with leaf arms whose HEAD is a wide open flower of broad petals with a face in the middle of it|the open flower head and the face in it|the back of the flower head and the two leaf arms|flower in a pot, potted plant, plant only, stem only, no creature, vase, soil
pilot|small round fish-creature with TWO long thin antennae rising from its head, each ending in a round glowing lamp|the two lamps held above it on their antennae|the round body from behind with both antennae above|one antenna, single lamp, anglerfish, one lure
starved|tiny creature that is a hard ribbed seed with a small face and two small leaves at the top, no arms and no legs, sitting still|the closed ribbed husk and the small face|the ribbed back of the husk and the two leaves|leaf hat, creature wearing a leaf, sprout, soil, plant pot, square border
LIST

# ---- the seven that drew well: their BACKS again, with the stronger back prompt
while IFS='|' read -r name body back; do
  for seed in 7 1917; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_r2$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind with its back toward the viewer, $back, $G" --negative "$NBACK, $N2" 2>&1 | tail -1
  done
done <<'LIST'
poll|small round owl with huge round eyes and a short beak, standing on one foot|the round back of its head and its folded wings, tail toward the viewer
watchdog|large owl with long pointed ear tufts and a heavy hooked beak|the back of its head with the ear tufts above, folded wings, tail toward the viewer
sounding|large deep-sea fish-creature with a round lamp on a long stalk above its head and broad fins|its broad tail fin toward the viewer and the stalk rising ahead of it
warning|small stocky bulldog-like creature with short thick legs|its wide stocky back and short curled tail toward the viewer
cache|round heavy cow-like creature with short blunt horns and small hooves|its broad back and short tail toward the viewer, the horns just visible past the head
triton|large sleek sea-dragon with broad wings and a row of blades along its back|the row of blades down its back and its wings from behind, tail toward the viewer
phoenix|large phoenix-like bird with a tall crest and long streaming tail feathers|its long streaming tail feathers toward the viewer and its wings from behind
LIST

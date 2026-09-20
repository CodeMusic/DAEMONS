#!/bin/bash
# T-131, the twelve gbareach.py found: species a player can reach that had never been converted at all.
# T-176's recipe unchanged -- 512 square, two seeds, a prompt that names a CONCRETE CREATURE rather than the
# concept, and "small in the frame" so cleandraft's fill has somewhere to start.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t131/alt
mkdir -p $S
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, water surface, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
while IFS='|' read -r name body front back; do
  for seed in 1917 42; do
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_front_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, front view, facing the viewer, $front, $G" --negative "side view, profile, rear view, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py t2i --size 512x512 --seed $seed --out $S/${name}_back_$seed \
      --prompt "pure white background, pixel art game sprite of a single $body, seen from directly behind, no face visible, $back, $G" --negative "face, eyes, mouth, beak, looking at viewer, front view, $N2" 2>&1 | tail -1
  done
done <<'LIST'
poll|small round owl with huge round eyes and a short beak, standing on one foot, feathers in a neat ring round the face|the two huge round eyes and the one raised foot|the round back of the head and the folded wings
watchdog|large owl with long pointed ear tufts, narrow half-closed eyes and a heavy hooked beak, wings folded|the narrow eyes and long ear tufts|the long ear tufts and folded wings from behind
pilot|small round fish-creature with two long thin antennae ending in round lamps above its head|the two lamps held above it and a small round mouth|the round body from behind and the two antennae
sounding|large deep-sea fish-creature with a single round lamp on a long stalk above its head, wide jaw, broad fins|the lamp on its stalk and the wide jaw|the broad fins and the stalk seen from behind
starved|tiny seed-creature with a hard ribbed husk and two small leaves at the top, no limbs, sitting still|the closed husk and two small leaves|the ribbed back of the husk
quota|small plant-creature whose head is a wide open flower of broad petals, on a short stalk body with two leaf arms|the open flower head facing forward|the back of the flower head and the stalk
fakeroot|stout tree-shaped creature with a thick knotted brown trunk for a body and three round clumps of leaves on its raised arms|the knotted trunk and the raised arms with their clumps|the trunk from behind and the clumps above
duplex|long-necked four-legged creature with a small second head at the end of its upright tail, both heads alert|the front head and the tail head raised behind it|both heads from behind, the tail head facing away
warning|small stocky bulldog-like creature with a huge under-bite jaw, a flat nose and short thick legs|the huge jaw and the flat nose|the wide stocky back and the short curled tail
cache|round heavy cow-like creature with short blunt horns, a broad body and small hooves, standing calm|the short horns and the broad calm face|the broad back and the short tail
triton|large sleek sea-dragon with a smooth pointed head, a long neck, broad wings held close and a row of blades along its back|the pointed head and the row of blades|the row of blades down the back and the broad wings
phoenix|large phoenix-like bird with a tall crest, a long neck, broad wings and long streaming tail feathers|the tall crest and the open wings|the long streaming tail feathers and the broad wings from behind
LIST

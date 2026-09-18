#!/bin/bash
# T-131 batch 8: Celadon's last four, and Fuchsia and the Safari Zone's wild tables, 2026-09-18. All twelve from
# words with the NIBBLE recipe (ai/README.md), two seeds per view, chosen in PICKS.txt. Batch 7's lesson is in G:
# "small in the frame with empty space all around", so a pale body no longer meets the edge and loses itself to the fill.
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch8/alt
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
tarpit|large pitcher plant creature with a wide open bell mouth, a long curled vine and a leaf lid|the gaping mouth of the pitcher, the leaf lid above|the back of the pitcher and the long curled vine
badseed|squat plant creature with a huge flat flower on its head with big spotted petals, dust drifting off it|a face under the flower, arms at its sides|the huge flower from behind, dust drifting
ensemble|tall palm tree creature with several round heads with faces clustered at its top, a thick trunk body and stubby feet|all the heads looking different ways|the back of the trunk, the heads clustered above
keeper|large upright armoured mother creature carrying a small young one in a belly pouch|a stern face, the small one peeking from the pouch|the broad armoured back, a thick tail
seedling|small slender sea serpent with a smooth body, a round head and small fin ears|big round eyes, coiled upright|the smooth coiled body from behind, the fin ears
upstream|large fish with a single horn on its forehead, spotted scales and long fins|swimming upright toward the viewer, horn forward|the dorsal fin and tail from behind
reaper|upright praying mantis creature with scythe blades for forearms and small wings|the scythes raised, sharp eyes|the wings folded down its back, scythes at its sides
uptime|round egg-shaped creature with a pouch holding an egg, stubby arms and small feet|a kind face, holding the egg out|the round back, the curled ends at its head
mock|small soft shapeless blob with a simple dot-eyed face|two dot eyes and a small mouth, sagging|the soft round back of the blob
rootkit|crab-like bug with a huge mushroom cap growing over its whole back|small eyes peering out from under the cap, pincers|the huge mushroom cap from behind, little legs
emergence|long slender serpent dragon with a smooth body, a small horn and a round orb on its neck|the small horn and the orb, coiled upright|the long smooth coils from behind, the orb on its neck
stampede|charging bull with three tails and curved horns|head down, horns forward|the three tails and the back of the horns
LIST

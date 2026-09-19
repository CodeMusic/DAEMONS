#!/bin/bash
# T-131 batch 14: THE MARGINS begin -- the islands' own daemons, whose names are a mind's words (0.6, 8.2b).
# No visual register for the islands was ever decided, so they are drawn like the rest, each from its name and entry --
# 2026-09-18. All twelve from words with the NIBBLE recipe (ai/README.md), two seeds per view, "small in the frame".
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch14/alt
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, man, woman, knight, armour, skeleton, white body, pale body, grey background, colored background, floor, ground, grass, water surface, rocks, pedestal, base, frame, box, people, human, weapon, drop shadow, shadow, pink, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, border, lines"
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
tension|small fluffy sheep with a thick round wool coat and a bobbled tail, standing on four short legs|a nervous face, wool bristling|the round wool coat from behind and the bobbled tail
apathy|small round smiling salamander sitting in mud, two feathery gills on its head|a vacant contented smile, half closed eyes|the round back and the feathery gills
blindspot|plain drill-tailed serpent creature with tiny wings, lying low|small unassuming eyes, a plain face|the plain segmented back and the drill tail
whim|small round puffball creature with a single large leaf on its head like a propeller, drifting|a light carefree face, floating|the leaf on its head from behind, the round body
ambush|round spider sitting still, a face pattern on its back, long thin legs|small eyes, still and waiting|the face pattern on its round back, legs spread
huddle|round ladybug creature with spotted wing cases and small arms, clinging|a shy face, arms held in|the spotted wing cases from behind
alarm|small upright striped rodent standing tall on its curled tail, alert|wide alert eyes, paws up|the striped back and the curled tail it stands on
recall|small round elephant with big ears and a long trunk|a gentle face, trunk curled|the round back and big ears, the short tail
fixation|lean hound with a skull-like face plate, bony ridges on its back and a thin tail|a fixed stare, ears back|the bony ridges down its back and the thin tail
simmer|small slug creature made of dripping molten rock|two dull eyes in the dripping body|the dripping lumpy back
omen|small crow with a wide brimmed hat-shaped head crest|a knowing narrow eye, beak forward|the hat-shaped crest and folded wings from behind
bristle|round pufferfish covered in spikes, puffed up large|round wide eyes, spikes all over|the spiked round back and the small tail fin
LIST

#!/bin/bash
# T-131 batch 10: Fuchsia to Cinnabar -- the Safari's edges, the Power Plant, Seafoam, Saffron's trainers --
# 2026-09-18. All twelve from words with the NIBBLE recipe (ai/README.md), two seeds per view, "small in the frame".
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch10/alt
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
quorum|three small floating metal orbs joined together in a triangle, each with one eye and magnets on its sides|all three eyes watching the viewer|the three round backs of the orbs joined together
chiller|round seal creature with a small horn on its head, flippers and a short tail|a calm face, whiskers, the small horn|the smooth round back and the horn, the tail
jetstream|seahorse with sharp spiky fins, a long tube snout and a curled tail|the spiky fins spread, snout forward|the spiky back fins and curled tail
smogstack|two round gas balls fused together, vents leaking puffs of smoke, two faces|two grinning faces, smoke puffs around|the two round backs with their vents, smoke puffs
trance|upright tapir-like creature holding a swinging pendulum on a string, a thick ruff of fur at its neck|heavy-lidded eyes, the pendulum held out|the ruff of fur from behind, the pendulum hanging to one side
breaker|round ball creature with a band around its middle, cracks across its casing, sparks|wide angry eyes, a jagged grin|the smooth round back with its band and cracks
theorem|muscular creature with a belt around its waist and a ridged crest on its head|arms flexed, a determined face|the broad muscular back, the belt, the crest
mime|slim clown-like figure with round padded hands pressed flat against an invisible wall, two tufts of hair|a calm painted face, hands pressed forward|the back of its head and tufts, hands raised flat
landfill|large heap of thick oozing sludge with two drippy arms and scraps stuck in it|a wide mouth and small eyes, arms raised|the lumpy back of the heap, drips running down
livelock|round furry pig-nosed monkey creature with clenched fists and bandaged arms, frantic|a furious face, fists raised|the round furry back, fists raised to either side
cairnling|small creature wearing a skull as a helmet, holding a bone club raised over its head|eyes shadowed under the skull|the back of the skull helmet, the bone club above
handler|upright blue-less duck-like creature with a gem on its forehead and webbed hands, calm|a calm focused face, the gem on its forehead|the back of its head and the gem glint, webbed feet
LIST

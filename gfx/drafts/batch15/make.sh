#!/bin/bash
# T-131 batch 15: THE MARGINS end -- the islands' own daemons, whose names are a mind's words (0.6, 8.2b).
# No visual register for the islands was ever decided, so they are drawn like the rest, each from its name and entry --
# 2026-09-18. All thirteen from words with the NIBBLE recipe (ai/README.md), two seeds per view, "small in the frame".
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch15/alt
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
vigilance|small round bird with huge unblinking round eyes and tiny wings, standing still|huge unblinking eyes staring straight ahead|the round back and tiny folded wings
ruminate|small armoured larva creature with a horn on its head and a hard rocky hide|a stubborn face, the horn|the rocky armoured back and the horn
periphery|large dragonfly with huge compound eyes and four wide clear wings|huge compound eyes, wings spread|the four clear wings spread from behind, a long tail
comfort|small round bear cub with a crescent mark on its chest, licking its paw|licking one paw, content|the round back and small ears
grasp|small monkey whose long tail ends in a large hand, tail raised|a mischievous grin, the tail hand raised|the back and the tail hand held high
hoarding|small creature hiding inside a round spotted shell, only small legs and a small head showing|small eyes peeking from the shell|the round spotted shell from behind
illusion|deer with large curled branching antlers holding round orbs|a calm gaze, the orbed antlers|the antlers from behind, the short tail
imitation|dog-like creature standing upright holding a paintbrush tail, a paint mark on its back|holding its brush tail forward, a beret-like head tuft|the paint mark on its back and the brush tail
startle|round hanging pine cone creature with a hard scaled shell, still|two small eyes between the scales|the scaled round back of the cone
instinct|small round pig creature covered in thick fur, a pink-less snout, burrowing|a snout poking out of thick fur|the round furry back
callous|snail creature with a hard stone shell, its body molten underneath|dull eyes, the molten body under the shell|the hard stone shell from behind
repay|small round bird carrying a sack in its tail, stubby wings|a cheerful face, the sack held out|the sack held in its tail from behind
armouring|tall armoured bird with sharp blade-edged metal wings and long legs|a sharp beak, wings half spread like blades|the blade-edged wings spread from behind
LIST

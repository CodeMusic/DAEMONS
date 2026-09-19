#!/bin/bash
# T-131 batch 9: the story's own daemons -- the three starters' last forms, the MUSAI line, ARTSAI and STARR --
# redrawn from their concepts as batch 1 was (i2i 0.55, seed 1917), and the Nidoran lines' middles and SPYWARE
# from words (two seeds per view, "small in the frame"), 2026-09-18.
# Off the home Wi-Fi, SPRITEFORGE_HOST=http://100.67.234.4:8008 (Tailscale).
cd /Users/christopherhicks/Projects/DAEMONS
S=gfx/drafts/batch9
P="pixel art game sprite, full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, flat solid green background, centered, no shadow, no text"
N="green body, green tint, pale body, drop shadow, shadow, colorful, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, frame, border"
while IFS='|' read -r name file desc; do
  ext=${file##*.}; b=${file%.*}
  python3 tools/prepconcept.py gfx/front/$file $S/src/${name}_front.png 0,200,0
  python3 tools/prepconcept.py gfx/back/$b-back.$ext $S/src/${name}_back.png 0,200,0
  for v in front back; do
    view="front view"; [ $v = back ] && view="rear view, seen from behind"
    python3 tools/spriteforge.py i2i --out $S/${name}_$v --image $S/src/${name}_$v.png --denoise 0.55 --seed 1917 \
      --prompt "$desc, $view, $P" --negative "$N" 2>&1 | tail -1
  done
done <<'LIST'
canon|canon.png|a boxy walking creature shaped like a thick ring binder, two eyes on its spine and two short legs
manifold|manifold.png|a long twisted folded ribbon creature, a flowing strip with round dots along it
roverbyte|roverbyte.png|a large sturdy robot dog with a boxy body, a square head and jointed legs
musai|musai.png|a small round robot creature sitting, a big round head with two eyes, headphones and two antennae
caremusai|caremusai.png|a small round robot creature sitting, a big round head with a round face and large headphones
codemusai|codemusai.png|a small round robot creature sitting, a round helmet head with a wide visor and two antennae
seekmusai|seekmusai.png|a small round robot creature sitting, a big round head with two eyes and a wide brimmed hat with antennae
artsai|artsai.png|a white rabbit sitting upright with long ears
starr|s.t.a.r.r..png|a tall stag deer standing, with large branching antlers
LIST
S=$S/alt
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
predictor|spiky rabbit-like creature with large ears and a tall horn, a spined back|the horn pointed forward, a sharp stare|the spined back and the horn above its ears
thread|spiky rabbit-like creature with large round ears and short spines, sturdy|a calm steady face|the spined back and round ears
spyware|large moth with broad patterned wings and big round compound eyes|the big compound eyes, wings spread|the patterned wings spread from behind
LIST

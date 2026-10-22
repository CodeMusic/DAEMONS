#!/bin/bash
# T-440: PROTEUS's two shapes for the battle and the party icon, redrawn FROM OUR hooded PROTEUS (T-176 batch 4,
# gfx/daemons/proteus_front.png / _back.png) by image-to-image at 512 on the T-131/T-176 recipe: the 64px drawing
# scaled 6x onto white, then each shape asked for in concrete words. DEFENSE (CONTEXT): the hood drawn shut, curled
# like a cocoon. ATTACK (CONTENT): the hood thrown back, the blades out.
cd /Users/christopherhicks/Projects/DAEMONS
export PATH="$HOME/.pyenv/versions/3.12.2/bin:$PATH"
S=gfx/drafts/t440
python3 - <<'PY'
from PIL import Image
for v in ("front", "back"):
    im = Image.open("gfx/daemons/proteus_%s.png" % v).convert("RGBA").resize((384, 384), Image.NEAREST)
    c = Image.new("RGB", (512, 512), (255, 255, 255)); c.paste(im, (64, 64), im)
    c.save("gfx/drafts/t440/src_%s.png" % v)
PY
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid face, grey background, colored background, floor, ground, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
DEF="the same hooded creature curled up into a closed cocoon shell, its hood drawn shut over the face, its long arms folded tight around its body like plates of a shell"
ATK="the same hooded creature with its hood thrown back showing a bare angular head, both arms held out ending in long sharp blades, all edges"
for seed in 1917 42; do
  for d in 0.6 0.7; do
    python3 tools/spriteforge.py i2i --image $S/src_front.png --denoise $d --seed $seed --out $S/def_front_${seed}_$d \
      --prompt "pure white background, pixel art game sprite of $DEF, front view, facing the viewer, $G" --negative "side view, rear view, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py i2i --image $S/src_back.png --denoise $d --seed $seed --out $S/def_back_${seed}_$d \
      --prompt "pure white background, pixel art game sprite of $DEF, seen from directly behind, no face visible, $G" --negative "face, eyes, front view, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py i2i --image $S/src_front.png --denoise $d --seed $seed --out $S/atk_front_${seed}_$d \
      --prompt "pure white background, pixel art game sprite of $ATK, front view, facing the viewer, $G" --negative "side view, rear view, hood over the head, $N2" 2>&1 | tail -1
  done
done

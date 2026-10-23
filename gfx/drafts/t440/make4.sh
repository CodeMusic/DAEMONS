#!/bin/bash
# T-440, round 4 (2026-10-23, the user: "draw an edged BACK for an owned CONTENT PROTEUS"): ALL EDGES from behind.
# T-439's overworld frames have no rear view, so two sources were tried: ow_atk.png (round 2's), and the approved
# edged front itself (gfx/daemons/proteus_front_attack.png) greyed by luminance with its face's red filled flat --
# the back of the head -- scaled 8x to 512 (src_atk_back.png). Picked: r4_atk_back_front_42_0.6 (the hood hanging
# down the back, the blades raised, no face), cleaned by tools/cleandraft.py into clean/atk_back.png =
# gfx/daemons/proteus_back_attack.png.
cd /Users/christopherhicks/Projects/DAEMONS
export PATH="$HOME/.pyenv/versions/3.12.2/bin:$PATH"
S=gfx/drafts/t440
python3 - <<'PY'
import colorsys
from PIL import Image
im = Image.open("gfx/daemons/proteus_front_attack.png").convert("RGBA"); px = im.load()
top = min(y for y in range(64) for x in range(64) if px[x, y][3])
out = Image.new("RGB", (64, 64), (255, 255, 255)); op = out.load()
for y in range(64):
    for x in range(64):
        r, g, b, a = px[x, y]
        if a:
            l = int(0.3 * r + 0.59 * g + 0.11 * b)
            if colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1] > 0.35 and y < top + 20:
                l = 150                                    # the face's red, on the head: the back of the head
            op[x, y] = (l, l, l)
out.resize((512, 512), Image.NEAREST).save("gfx/drafts/t440/src_atk_back.png")
PY
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
ATKB="a lean hooded creature with its hood thrown back from a bare angular head, both long arms raised high ending in sharp blades, a flared cloak below"
for src in ow_atk:$S/ow_atk.png front:$S/src_atk_back.png; do n=${src%%:*}; img=${src#*:}
  for seed in 1917 42; do for d in 0.5 0.6; do
    python3 tools/spriteforge.py i2i --image $img --denoise $d --seed $seed --out $S/r4_atk_back_${n}_${seed}_$d \
      --prompt "pure white background, pixel art game sprite of $ATKB, rear view, seen from directly behind, facing away from the viewer, back of the head, the hood hanging down its back, $G" \
      --negative "face, eyes, mouth, front view, facing the viewer, side view, $N2" 2>&1 | tail -1
  done; done
done
python3 tools/cleandraft.py $S/r4_atk_back_front_42_0.6.png $S/clean/atk_back.png
cp $S/clean/atk_back.png gfx/daemons/proteus_back_attack.png

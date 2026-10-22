#!/bin/bash
# T-440, round 3: round 2's cocoon drew right but cleaned to 34x39 in the 64px frame -- smaller than any battle
# front -- because the source sat the 32px frame's margin around it. Here the cocoon alone is cropped from T-439's
# frame and scaled to stand 420px of the 512 (about 52 of the 64), and drawn again at the round-2 settings.
cd /Users/christopherhicks/Projects/DAEMONS
export PATH="$HOME/.pyenv/versions/3.12.2/bin:$PATH"
S=gfx/drafts/t440
python3 - <<'PY'
from PIL import Image
im = Image.open("gfx/drafts/t440/ow_def.png").convert("L")
px = im.load(); W, H = im.size
xs = [x for x in range(W) for y in range(H) if px[x, y] < 250]; ys = [y for y in range(H) for x in range(W) if px[x, y] < 250]
box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
sub = Image.open("gfx/drafts/t440/ow_def.png").convert("RGB").crop(box)
sc = 420 / sub.height
sub = sub.resize((round(sub.width * sc), 420), Image.NEAREST)
c = Image.new("RGB", (512, 512), (255, 255, 255)); c.paste(sub, ((512 - sub.width) // 2, 46)); c.save("gfx/drafts/t440/ow_def_big.png")
print(box, sub.size)
PY
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
DEF="a hooded creature closed up inside its own shell like a cocoon, an upright egg-shaped body of overlapping hard plates, its hood drawn shut at the pointed top, a small crystalline core showing at the top of the seam"
DEFB="a hooded creature closed up inside its own shell like a cocoon, an upright egg-shaped body of overlapping hard plates, its hood drawn shut at the pointed top"
for seed in 1917 42; do
  python3 tools/spriteforge.py i2i --image $S/ow_def_big.png --denoise 0.6 --seed $seed --out $S/r3_def_front_$seed \
    --prompt "pure white background, pixel art game sprite of $DEF, front view, facing the viewer, $G" --negative "side view, rear view, arms, legs, face, $N2" 2>&1 | tail -1
  python3 tools/spriteforge.py i2i --image $S/ow_def_big.png --denoise 0.6 --seed $seed --out $S/r3_def_back_$seed \
    --prompt "pure white background, pixel art game sprite of $DEFB, seen from directly behind, no core visible, $G" --negative "face, eyes, core, front view, arms, legs, $N2" 2>&1 | tail -1
done

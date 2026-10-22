#!/bin/bash
# T-440, round 2: round 1 (make.sh) redrew the STANDING figure at 0.6-0.7 -- the model keeps a pose, it will not curl
# one up. So the source here is T-439's approved overworld shape itself (deoxys_d.png / deoxys_a.png, frame 0, 32px),
# greyed by luminance and scaled 12x onto white: the cocoon and the blades are already the composition, and the
# redraw only adds the battle sprite's detail. The back is the cocoon asked for from behind, with the core hidden.
cd /Users/christopherhicks/Projects/DAEMONS
export PATH="$HOME/.pyenv/versions/3.12.2/bin:$PATH"
S=gfx/drafts/t440
python3 - <<'PY'
from PIL import Image
G = "engineGba/graphics/object_events"
cols = open(G + "/palettes/daemon_type_psychic.pal").read().split()[3:]
cols = [tuple(int(v) for v in cols[i:i + 3]) for i in range(0, 48, 3)]
for f, k in (("deoxys_d", "def"), ("deoxys_a", "atk")):
    im = Image.open(G + "/pics/pokemon/%s.png" % f).crop((0, 0, 32, 32))
    out = Image.new("RGB", (32, 32), (255, 255, 255)); px, ip = out.load(), im.load()
    for y in range(32):
        for x in range(32):
            if ip[x, y]:
                r, g, b = cols[ip[x, y]]; l = int(0.3 * r + 0.59 * g + 0.11 * b); px[x, y] = (l, l, l)
    c = Image.new("RGB", (512, 512), (255, 255, 255)); c.paste(out.resize((384, 384), Image.NEAREST), (64, 64))
    c.save("gfx/drafts/t440/ow_%s.png" % k)
PY
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N2="human, person, humanoid, grey background, colored background, floor, ground, pedestal, base, frame, box, drop shadow, shadow, text, letters, watermark, multiple creatures, scenery, photorealistic, blurry, cropped"
DEF="a hooded creature closed up inside its own shell like a cocoon, an upright egg-shaped body of overlapping hard plates, its hood drawn shut at the pointed top, a small crystalline core showing at the top of the seam"
DEFB="a hooded creature closed up inside its own shell like a cocoon, an upright egg-shaped body of overlapping hard plates, its hood drawn shut at the pointed top"
ATK="a lean hooded creature with its hood thrown back from a bare angular head, both long arms raised high ending in sharp blades, a flared cloak below"
for seed in 1917 42; do
  for d in 0.5 0.6; do
    python3 tools/spriteforge.py i2i --image $S/ow_def.png --denoise $d --seed $seed --out $S/r2_def_front_${seed}_$d \
      --prompt "pure white background, pixel art game sprite of $DEF, front view, facing the viewer, $G" --negative "side view, rear view, arms, legs, face, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py i2i --image $S/ow_def.png --denoise $d --seed $seed --out $S/r2_def_back_${seed}_$d \
      --prompt "pure white background, pixel art game sprite of $DEFB, seen from directly behind, no core visible, $G" --negative "face, eyes, core, front view, arms, legs, $N2" 2>&1 | tail -1
    python3 tools/spriteforge.py i2i --image $S/ow_atk.png --denoise $d --seed $seed --out $S/r2_atk_front_${seed}_$d \
      --prompt "pure white background, pixel art game sprite of $ATK, front view, facing the viewer, $G" --negative "side view, rear view, hood over the head, $N2" 2>&1 | tail -1
  done
done

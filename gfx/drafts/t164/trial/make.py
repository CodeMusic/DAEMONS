#!/usr/bin/env python3
"""T-164's trial (2026-09-19): can the sprite model draw OVERWORLD art -- tiles, not creatures?
Two ways, one building and one ground each:
  FROM WORDS   text-to-image at 512 (the model's 8px grid makes that 64 art px = 4x4 metatiles), three seeds.
  RESTYLE      image-to-image from the CURRENT in-game art (a crop of Doldrum), scaled x8 onto the same grid, at 0.35
               and 0.50 -- which keeps the layout, and so the collision and seams, that a tileset cannot move."""
import subprocess
from PIL import Image
T = "gfx/drafts/t164/trial"
STYLE = "pixel art, Game Boy Advance RPG overworld tileset style, top-down three-quarter view, crisp 16-bit pixels, flat even lighting"
NEG = "text, letters, watermark, people, characters, animals, border, frame, vignette, blurry, photorealistic, 3d render, perspective distortion"
def t2i(name, prompt, seeds=(1917, 42, 88)):
    for s in seeds:
        subprocess.run(["python3", "tools/spriteforge.py", "t2i", "--size", "512x512", "--seed", str(s), "--out", "%s/%s_%d" % (T, name, s),
                        "--prompt", "%s, %s" % (prompt, STYLE), "--negative", NEG])
def i2i(name, ref, prompt):
    im = Image.open("%s/%s" % (T, ref)).convert("RGB"); w, h = im.size
    big = im.resize((w * 8 // 8 * 8, h * 8 // 8 * 8), Image.NEAREST) if False else im.resize((w * 8, h * 8), Image.NEAREST)
    W, H = (big.width + 7) // 8 * 8, (big.height + 7) // 8 * 8
    canvas = Image.new("RGB", (W, H), (0, 0, 0)); canvas.paste(big); canvas.save("%s/src_%s.png" % (T, name))
    for dn in ("0.35", "0.50"):
        subprocess.run(["python3", "tools/spriteforge.py", "i2i", "--out", "%s/%s_i2i_%s" % (T, name, dn[2:]), "--image", "%s/src_%s.png" % (T, name),
                        "--denoise", dn, "--seed", "1917", "--prompt", "%s, %s" % (prompt, STYLE), "--negative", NEG])
t2i("ground", "seamless repeating grass ground texture tile, soft green grass with small darker tufts and a few light blades, no objects")
t2i("house", "one small house isolated on flat green grass, blue-grey tiled roof, cream plaster walls, one wooden door and two windows, centered")
i2i("house", "ref_house.png", "a small house with a blue-grey roof and cream walls")
i2i("ground", "ref_ground.png", "grass ground with a low wooden fence")

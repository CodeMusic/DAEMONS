#!/usr/bin/env python3
"""T-164, people and objects (decided by the user 2026-09-19, after the building pilot). The trial:
  OBJECTS from words, the NIBBLE recipe on a green key, three seeds -- then scaled to the object's size.
  PEOPLE restyled as a WHOLE 9-frame sheet at once (image-to-image, x8 onto the model's grid), so the frames of a walk
  cycle stay one character; two strengths."""
import subprocess
from PIL import Image
T = "gfx/drafts/t164/people"; M = "engineGba/graphics/object_events/pics"
OBJ = ("pixel art game sprite, single object, top-down three-quarter view, Game Boy Advance RPG overworld style, crisp "
       "pixels, clean dark outline, flat solid green background, centered, no shadow, no text")
ONEG = "green object, text, letters, watermark, people, characters, scenery, ground, floor, frame, border, blurry, photorealistic, shadow"
for name, desc in [("sign", "a small white metal information signboard on two short legs"),
                   ("fossil", "an old fossil shell of a spiral ammonite, cracked stone"),
                   ("town_map", "a folded paper town map lying open, with roads and blocks drawn on it"),
                   ("lapras_doll", "a soft plush toy doll of a gentle sea creature with a shell on its back and a long neck")]:
    for s in (1917, 42, 88):
        subprocess.run(["python3", "tools/spriteforge.py", "t2i", "--size", "512x512", "--seed", str(s), "--out", "%s/obj_%s_%d" % (T, name, s),
                        "--prompt", "%s, %s" % (desc, OBJ), "--negative", ONEG])
PP = ("a row of nine small pixel art character walking frames, Game Boy Advance RPG overworld sprite sheet, crisp 16-bit "
      "pixels, clean dark outline, consistent character in every frame")
PN = "text, letters, watermark, background scenery, blurry, photorealistic, extra characters, merged frames"
for name in ("cameraman", "rich_boy", "town_doldrum_child"):
    im = Image.open("%s/people/%s.png" % (M, name)).convert("RGBA")
    bg = Image.new("RGBA", im.size, (0, 200, 0, 255)); bg.alpha_composite(im)
    bg.convert("RGB").resize((im.width * 8, im.height * 8), Image.NEAREST).save("%s/src_%s.png" % (T, name))
    for dn in ("0.40", "0.55"):
        subprocess.run(["python3", "tools/spriteforge.py", "i2i", "--out", "%s/ppl_%s_%s" % (T, name, dn[2:]), "--image", "%s/src_%s.png" % (T, name),
                        "--denoise", dn, "--seed", "1917", "--prompt", PP, "--negative", PN])

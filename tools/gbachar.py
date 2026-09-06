#!/usr/bin/env python3
"""Cut the character art down to the sprites the engine actually loads.

    python3 tools/gbachar.py            # report + /tmp/char.png
    python3 tools/gbachar.py --write

TWO SPRITES, TWO COMPLETELY DIFFERENT FORMATS, and getting either wrong
produces a screenful of confetti rather than an error.

  THE PLAYER -> graphics/oak_speech/{red,leaf}/pic.png, 64x96, 8bpp -- and a
     DIFFERENT palette bank from everyone else here. oak_speech.c loads the
     two player pics with LoadPalette(..., BG_PLTT_ID(4)) and the professor
     and rival with BG_PLTT_ID(6), so player indices start at 65 where the
     others start at 97. Vanilla's red/pic.png uses 0..95 and oak/pic.png
     uses 0..121, which is the same fact seen from the file. Wrong base is a
     screenful of confetti, not an error.

     9.10 made playerGender a pure sprite selector, so MALE_PLAYER_PIC is
     LOGIC and FEMALE_PLAYER_PIC is INTUITION -- the order the question
     offers them in.

  CRYSTAL -> graphics/oak_speech/oak/pic.png, 64x96, EIGHT bits per pixel.
     oak_speech.c loads its palette with LoadPalette(..., BG_PLTT_ID(6)),
     which is palette RAM 96 -- so the pixel values in the file are not 1..25,
     they are 97..121. An 8bpp background indexes palette RAM directly, so an
     image written with ordinary low indices would read the wrong end of the
     palette and come out as noise. The 32-colour .pal is bank 6, meaning its
     entry k is RAM 96+k.

  SCORN and AL's three battle pics -> graphics/trainers/front_pics/*.png,
     64x64, FOUR bits per pixel, sixteen colours, index 0 transparent.

     AND THE PNG DOES NOT CARRY THE COLOURS. trainers.h takes the picture
     from <name>_front_pic.4bpp.lz and the palette from a SEPARATE file,
     palettes/<name>.gbapal.lz, built from palettes/<name>.pal. Writing the
     PNG alone leaves the new indices addressing the OLD trainer's colours --
     Scorn shipped that way and rendered with Giovanni's palette, in which
     index 5 is magenta. Every 4bpp job writes its .pal.

AND NEITHER SPRITE CARRIES ITS OWN SHADOW. The generated art stands on a pale
ellipse, but oak_speech draws platform.png separately underneath and the
battle screen draws its own -- so the ellipse has to come off or the character
stands on two of them.
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gridsample import deringe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
KEY = (115, 197, 164)          # what vanilla puts in the transparent slot

JOBS = {
    "crystal":     dict(src="gfx/characters/crystal_speech.jpeg",
                        dst="engineGba/graphics/oak_speech/oak/pic.png",
                        pal="engineGba/graphics/oak_speech/oak/pal.pal",
                        size=(64, 96), colours=25, base=97, palsize=32),
    "al_speech":   dict(src="gfx/characters/al_speech.jpeg",
                        dst="engineGba/graphics/oak_speech/rival/pic.png",
                        pal="engineGba/graphics/oak_speech/rival/pal.pal",
                        size=(64, 96), colours=25, base=97, palsize=32),
    "scorn":       dict(src="gfx/characters/scorn.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/leader_giovanni_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_giovanni.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
    "al_early":    dict(src="gfx/characters/al_early.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/rival_early_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/rival_early.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
    "al_late":     dict(src="gfx/characters/al_late.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/rival_late_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/rival_late.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
    "logic":       dict(src="gfx/characters/player_logic.jpeg",
                        dst="engineGba/graphics/oak_speech/red/pic.png",
                        pal="engineGba/graphics/oak_speech/red/pal.pal",
                        size=(64, 96), colours=31, base=65, palsize=32),
    "intuition":   dict(src="gfx/characters/player_intuition.jpeg",
                        dst="engineGba/graphics/oak_speech/leaf/pic.png",
                        pal="engineGba/graphics/oak_speech/leaf/pal.pal",
                        size=(64, 96), colours=31, base=65, palsize=32),
    "al_champion": dict(src="gfx/characters/al_champion.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/champion_rival_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/champion_rival.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
}

def silhouette(a):
    """Background AND the shadow ellipse, which are both GREENISH.

    The ellipse is the background blended toward white, so it keeps the green
    bias; the lab coat is neutral and the suit is blue-grey, and neither does.
    Two comparisons separate them and nothing else in either picture is green."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return ~((g - r > 12) & (g - b > 4))

def cut(job):
    # Sampled on the grid it was drawn on: these are pixel drawings upscaled
    # to 1024 and exported as JPEG, so the ringing sits at block edges and
    # never has to be read. Matters less here than for the daemons -- a 2.7x
    # reduction averages most of it away -- but one pipeline, one behaviour.
    a = deringe(np.asarray(Image.open(os.path.join(ROOT, job["src"])).convert("RGB")).astype(int))
    ink = silhouette(a)
    ys, xs = np.where(ink)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    im = Image.fromarray(a.astype(np.uint8)).crop(box)
    mask = Image.fromarray((ink[box[1]:box[3], box[0]:box[2]] * 255).astype(np.uint8))

    W, H = job["size"]
    scale = min(W / im.width, H / im.height)
    w, h = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    im = im.resize((w, h), Image.LANCZOS)
    mask = mask.resize((w, h), Image.LANCZOS).point(lambda v: 255 if v > 140 else 0)

    cell = Image.new("RGB", (W, H), KEY)
    cell.paste(im, ((W - w) // 2, H - h), mask)      # feet on the floor, centred
    hold = Image.new("L", (W, H), 0)
    hold.paste(mask, ((W - w) // 2, H - h))
    return cell, hold

def index(cell, hold, job):
    # Quantize the SUBJECT ONLY. Quantizing the whole cell hands one of the
    # scarce slots to the transparent key, which is then zeroed out again --
    # 15 colours become 14, on a sprite that has 15 to spend.
    subj = np.asarray(cell)[np.asarray(hold) > 0].reshape(1, -1, 3).astype(np.uint8)
    q = Image.fromarray(subj).convert("P", palette=Image.ADAPTIVE,
                                      colors=job["colours"], dither=Image.NONE)
    pal = q.getpalette()[:job["colours"] * 3]
    table = [tuple(pal[i * 3:i * 3 + 3]) for i in range(job["colours"])]
    a = np.asarray(cell).astype(int)
    d = ((a[:, :, None, :] - np.array(table)[None, None, :, :]) ** 2).sum(axis=3)
    flat = (d.argmin(axis=2) + job["base"]).astype(np.uint8)
    flat[np.asarray(hold) == 0] = 0
    out = Image.new("P", cell.size)
    out.putdata(flat.flatten().tolist())
    full = [0] * 768
    full[0:3] = list(KEY)
    for i, c in enumerate(table):
        j = (job["base"] + i) * 3
        full[j:j + 3] = list(c)
    out.putpalette(full)
    return out, table

def main():
    prev, x = Image.new("RGB", ((64 * 6 + 40) * len(JOBS), 96 * 6), (18, 18, 24)), 0
    for name, job in JOBS.items():
        cell, hold = cut(job)
        out, table = index(cell, hold, job)
        print("  %-8s %-52s %dx%d, %d colours at index %d+"
              % (name, job["dst"].split("engineGba/")[-1], *job["size"], len(table), job["base"]))
        prev.paste(out.convert("RGB").resize((64 * 6, job["size"][1] * 6), Image.NEAREST), (x, 0))
        x += 64 * 6 + 40
        if "--write" in sys.argv:
            out.save(os.path.join(ROOT, job["dst"]))
            if job["pal"]:
                with open(os.path.join(ROOT, job["pal"]), "w") as f:
                    f.write("JASC-PAL\n0100\n%d\n" % job["palsize"])
                    rows = [KEY] + [(0, 0, 0)] * (job["palsize"] - 1)
                    for i, c in enumerate(table):          # entry 0 is the key; ours start at 1
                        rows[1 + i] = c
                    for c in rows:
                        f.write("%d %d %d\n" % c)
            print("           written")
    prev.save("/tmp/char.png")
    print("  preview   /tmp/char.png")

main()

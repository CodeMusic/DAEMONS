#!/usr/bin/env python3
"""The figures who run beside the credits are the player and AL, not vanilla's RED, LEAF and BLUE (T-290, DRAFT).

    python3 tools/gencreditrunners.py            # report, and a preview in the scratch dir
    python3 tools/gencreditrunners.py --write    # graphics/credits/player_male.png, player_female.png, rival.png

FireRed's credits run a large figure along the bottom of the screen: 64x64 frames, six of them stacked in one sheet,
drawn by hand for RED (or LEAF) running and BLUE tossing a ball. They were the last human beings in a game where
every person is an animal (the fable), and the one place the player stopped being themselves.

DRAWN (2026-10-01, DRAFT): each of the three poses in a run was redrawn through the sprite server from the overworld
frame itself (image to image, denoise 0.6, so the pose and the legs stay the frame's), keyed and brought down to
32x64 at its own resolution -- gfx/runners/<who>_<frame>.png, from gfx/drafts/t290/. Where a drawn frame is missing
the tool falls back to the first draft: the overworld frame doubled pixel for pixel. Both player sheets are the same
figure: the player is the same animal whichever PATH they chose.

The sheets carry their own sixteen colours (the credits load each sheet's palette from its PNG): a drawn sheet's are
the fifteen its frames share most, and index 0 is the clear one.

"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
PALS = os.path.join(GBA, "graphics/object_events/palettes")
CREDITS = os.path.join(GBA, "graphics/credits")
DRAWN = os.path.join(ROOT, "gfx/runners")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

#  (sheet, source sheet, the six 16x32 frames of it in order, palette file)
RUNNERS = [
    ("player_male",   "red_surf_run", [10, 9, 11, 9, 10, 9], "player.pal",     "player"),  # running, facing left
    ("player_female", "red_surf_run", [10, 9, 11, 9, 10, 9], "player.pal",     "player"),
    ("rival",         "blue",         [2, 7, 2, 8, 2, 7],    "npc_clears.pal", "al"),      # walking, facing left
]


def jasc(name):
    lines = open(os.path.join(PALS, name), newline="").read().replace("\r\n", "\n").split("\n")
    return [tuple(int(v) for v in l.split()) for l in lines[3:19]]


def sheet(source, frames, pal):
    src = Image.open(os.path.join(PEOPLE, source + ".png"))
    out = Image.new("P", (64, 64 * len(frames)), 0)
    out.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    for k, f in enumerate(frames):
        cell = src.crop((16 * f, 0, 16 * f + 16, 32)).resize((32, 64), Image.NEAREST)
        out.paste(cell, (16, 64 * k))
    return out


def drawn(who, frames):
    """The drawn sheet: each frame's 32x64 drawing on the bottom of its 64x64 cell, in fifteen shared colours."""
    paths = [os.path.join(DRAWN, "%s_%d.png" % (who, f)) for f in frames]
    if not all(os.path.exists(p) for p in paths):
        return None
    cells = [Image.open(p).convert("RGBA") for p in paths]
    opaque = [c for cell in cells for c in cell.getdata() if c[3] >= 128]
    strip = Image.new("RGB", (len(opaque), 1))
    strip.putdata([c[:3] for c in opaque])
    pal = strip.quantize(15, method=Image.Quantize.MEDIANCUT).getpalette()[:45]
    pal = [(0, 0, 0)] + [tuple(pal[i:i + 3]) for i in range(0, 45, 3)]
    out = Image.new("P", (64, 64 * len(frames)), 0)
    out.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    px = out.load()
    for k, cell in enumerate(cells):
        for y in range(64):
            for x in range(32):
                c = cell.getpixel((x, y))
                if c[3] >= 128:
                    px[16 + x, 64 * k + y] = 1 + min(range(15), key=lambda i: sum((a - b) ** 2 for a, b in zip(c, pal[1 + i])))
    return out


def main():
    made = []
    for name, source, frames, palname, who in RUNNERS:
        s = drawn(who, frames)
        how = "drawn"
        if s is None:
            s, how = sheet(source, frames, jasc(palname)), "doubled"
        made.append(s)
        print("  %-14s from %s frames %s, %s" % (name, source, frames, how))
        if WRITE:
            s.save(os.path.join(CREDITS, name + ".png"), bits=4)
    prev = Image.new("RGBA", (70 * len(made), 64 * 6), (40, 40, 40, 255))
    for i, s in enumerate(made):
        prev.paste(s.convert("RGBA"), (70 * i, 0))
    os.makedirs(SCRATCH, exist_ok=True)
    prev.resize((prev.width * 2, prev.height * 2), Image.NEAREST).save(os.path.join(SCRATCH, "credit_runners.png"))
    print("  written" if WRITE else "  report only; pass --write (preview in %s)" % SCRATCH)


if __name__ == "__main__":
    main()

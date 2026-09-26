#!/usr/bin/env python3
"""The figures who run beside the credits are the player and AL, not vanilla's RED, LEAF and BLUE (T-290, DRAFT).

    python3 tools/gencreditrunners.py            # report, and a preview in the scratch dir
    python3 tools/gencreditrunners.py --write    # graphics/credits/player_male.png, player_female.png, rival.png

FireRed's credits run a large figure along the bottom of the screen: 64x64 frames, six of them stacked in one sheet,
drawn by hand for RED (or LEAF) running and BLUE tossing a ball. They were the last human beings in a game where
every person is an animal (the fable), and the one place the player stopped being themselves.

This is the DRAFT that needs no generator: the player's and AL's own overworld frames -- the side view, running for
the player and walking for AL -- doubled pixel for pixel to 32x64 and set on the bottom of each 64x64 cell. It is
chunkier than the art around it, and it is the right people. A drawn version waits for the sprite sweep (T-210).
Both player sheets are the same figure: the player is the same animal whichever PATH they chose.

The sheets carry their own sixteen colours (the credits load each sheet's palette from its PNG): the player's
from player.pal, AL's from the Clears' palette.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
PALS = os.path.join(GBA, "graphics/object_events/palettes")
CREDITS = os.path.join(GBA, "graphics/credits")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

#  (sheet, source sheet, the six 16x32 frames of it in order, palette file)
RUNNERS = [
    ("player_male",   "red_surf_run", [10, 9, 11, 9, 10, 9], "player.pal"),     # running, facing left
    ("player_female", "red_surf_run", [10, 9, 11, 9, 10, 9], "player.pal"),
    ("rival",         "blue",         [2, 7, 2, 8, 2, 7],    "npc_clears.pal"), # walking, facing left
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


def main():
    made = []
    for name, source, frames, palname in RUNNERS:
        s = sheet(source, frames, jasc(palname))
        made.append(s)
        print("  %-14s from %s frames %s, doubled" % (name, source, frames))
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

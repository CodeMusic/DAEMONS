#!/usr/bin/env python3
"""THE (NOT A) HUNTER of THE NEXUS: a brown bear in red plaid (T-395, DRAFT art; docs/nexus.md).

    python3 tools/genhunter.py            # report, and a preview in the scratch dir
    python3 tools/genhunter.py --write    # graphics/object_events/pics/people/nexus_hunter.png

The user, 2026-10-09: an NPC in THE NEXUS, dressed in red plaid as in THE PAINTED MIRROR -- "Hunter? I'm no
hunter..." -- and a bear (fable-actors-animals: every person is an animal). Drawn with the town folk's own figure
(gentowns.fig, genfolk.figure): a brown bear's head, a red flannel shirt with its sleeves, dark trousers. The plaid is
a dark grid over the shirt, every third row and column, so it reads as check at sixteen pixels and not as stripes.

npc_white, nine frames like every walking sheet; THE NEXUS holds nobody else, so the slot is his.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import figure, check, sheet, read_pal, ensure_rule, PEOPLE, WHITE
from gentowns import mammal, fig

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PEOPLE, "nexus_hunter.png")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))
SHIRT, CHECK = WHITE["R"], WHITE["E"]          # orange-red flannel, the darkest brown for its grid

# npc_white: r red-brown  E darkest brown  T sand-gold  R orange-red  G dark grey  g grey
BEAR = fig(mammal("r", "E", "T"), "R", "R", "G", "G", "E")


def plaid(img):
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y] == SHIRT and (y % 3 == 0 or (x % 16) % 3 == 1):
                px[x, y] = CHECK
    return img


def main():
    frames = figure(*BEAR)
    check("hunter", frames, WHITE)
    img = plaid(sheet(frames, WHITE, read_pal("npc_white.pal")))
    print("  THE (NOT A) HUNTER: %d frames, a brown bear in red plaid, npc_white" % len(frames))
    os.makedirs(SCRATCH, exist_ok=True)
    img.convert("RGBA").resize((img.width * 6, img.height * 6), Image.NEAREST).save(os.path.join(SCRATCH, "hunter_preview.png"))
    old = Image.open(OUT) if os.path.exists(OUT) else None
    if old is not None and list(old.getdata()) == list(img.getdata()):
        print("  nexus_hunter.png is current")
        return
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % SCRATCH)
        return
    img.save(OUT, bits=4)
    ensure_rule("nexus_hunter.png")
    print("  written")


if __name__ == "__main__":
    main()

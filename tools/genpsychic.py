#!/usr/bin/env python3
"""DARIO's picture -- the one vanilla portrait a player of this game can still reach (T-126).

    python3 tools/genpsychic.py            # preview to /tmp/psychic.png
    python3 tools/genpsychic.py --write    # the portrait and its palette

OF THE 79 PORTRAITS STILL ON VANILLA ART, EXACTLY ONE IS REACHABLE. Measured, not assumed: 742
trainers, and the other 78 portraits belong to trainers that no script places and no map object
runs -- the Hoenn cast, the `rs_*` link-partner set, the triathletes, Steven, Red, Leaf, Wally.
They sit in `trainers.h` and nowhere else. `PSYCHIC_M` is the exception: TRAINER_PSYCHIC_DARIO
stands in SEVEN ISLAND's TRAINER TOWER, `data/scripts/trainers.inc` gives him a battle and a
rematch, and `vs_seeker.c` lists him. So he is drawn and the rest keep vanilla's, which is the
cut-off doing its job rather than being waived.

THE SPECIES IS NOT A NEW DECISION. `psychic_f` is a jellyfish -- chosen in T-120 when the first
draft came back a second octopus, which the juggler already holds -- and 9.4 binds a class to one
species. So this is that jellyfish, the way POKEMON_RANGER_M and _F are one pine marten in two
uniforms.

AND IT IS NOT NEWLY DRAWN, BECAUSE IT CANNOT BE. Every portrait in this project was drafted through
the n8n `daemon/sprite` webhook and fetched by hand into `gfx/characters/`; no tool here posts to
it. What a tool CAN do is what `genbacks.py` does for the back pics: take a figure that already
exists and repaint it. So this reads OUR OWN `psychic_f`, mirrors it, and re-dresses it -- the bell,
the limbs and the tentacle trails keep their blues, and the robe alone moves to a violet. The
silhouette is deliberately the same silhouette: they are one species and one class, and the picture
says so.

INDEX 0 IS THE TRANSPARENT SLOT and keeps whatever the source had. A 4bpp portrait's PNG does not
carry its colours -- `trainers.h` takes the picture from `<name>_front_pic.4bpp.lz` and the palette
from a separate `palettes/<name>.gbapal.lz` -- so the `.pal` is written every time.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import GBA

PREVIEW = "/tmp/psychic.png"
WRITE = "--write" in sys.argv
PICS = os.path.join(GBA, "graphics/trainers/front_pics")
PALS = os.path.join(GBA, "graphics/trainers/palettes")
SRC, DST = "psychic_f", "psychic_m"


def is_bell(rgb):
    """the jellyfish's own colour is CYAN -- blue well past red, and green past red with it.
    The robe is a lavender grey, where red and green sit together under the blue."""
    r, g, b = rgb
    return b - r > 24 and g - r > 6


def redress(rgb):
    """the same cloth, dyed: the lavender ramp taken DOWN into an indigo, not across into a pink.

    The first pass lifted red and came out a bright rose -- louder than any other portrait in the
    set, and the one reading nobody wanted on it. Value is what the muted register is made of, so
    the dye darkens: red and green both come down, blue is held, and the robe lands where the rest
    of the cast's cloth sits."""
    r, g, b = rgb
    return (max(0, int(r * 0.72)), max(0, int(g * 0.62)), max(0, int(b * 0.92)))


def main():
    src = Image.open(os.path.join(PICS, SRC + "_front_pic.png"))
    old = Image.open(os.path.join(PICS, DST + "_front_pic.png"))
    assert src.mode == "P" and src.size == (64, 64), "%s is %s %s" % (SRC, src.mode, src.size)
    assert old.size == src.size, "%s is %s and %s is %s" % (DST, old.size, SRC, src.size)

    pal = list(src.getpalette()[:48])
    kept = []
    for i in range(1, 16):
        rgb = tuple(pal[i * 3:i * 3 + 3])
        if is_bell(rgb):
            kept.append(i)
        else:
            pal[i * 3:i * 3 + 3] = list(redress(rgb))
    out = src.transpose(Image.FLIP_LEFT_RIGHT)       # he faces the other way; she keeps hers
    out.putpalette(pal + [0] * (768 - 48))
    colours = [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]

    prev = Image.new("RGB", (64 * 6 * 3 + 24, 64 * 6), (60, 60, 60))
    for k, im in enumerate((old, src, out)):
        prev.paste(im.convert("RGB").resize((384, 384), Image.NEAREST), (k * (384 + 12), 0))
    prev.save(PREVIEW)
    print("  %s: %d of 15 colours are the jellyfish and keep theirs; %d are the robe and are re-dyed"
          % (DST, len(kept), 15 - len(kept)))
    print("  -> preview %s (vanilla's, then psychic_f, then ours)" % PREVIEW)

    if WRITE:
        out.save(os.path.join(PICS, DST + "_front_pic.png"), bits=4)
        with open(os.path.join(PALS, DST + ".pal"), "w") as fh:
            fh.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in colours))
        #  T-177's outline, which every picture of ours carries: drawn by the same pass, so this write lands where the
        #  tree is and does not take it off again (T-293).
        import gbaoutline
        gbaoutline.main(only=[DST], write=True)
        print("  written the portrait and its palette")


if __name__ == "__main__":
    main()

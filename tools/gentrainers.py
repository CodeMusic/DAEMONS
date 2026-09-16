#!/usr/bin/env python3
"""The shared people sheets, redrawn as a fable -- one species per CLASS (T-120; vision.md 9.4).

    python3 tools/gentrainers.py            # preview to /tmp/trainers_ow.png
    python3 tools/gentrainers.py --write    # overwrite the sheets in place

These are VANILLA'S OWN SHEETS, not new graphics: a hiker is one sheet shared by thirty objects
across the routes, so redrawing it is the biggest move the census can make. Nothing is registered
and no map changes -- the PNG is overwritten and every object already pointing at it follows.

TWO THINGS ARE FIXED AND MUST NOT CHANGE, or the ROM reads past the end of a sheet:

    the PALETTE   each sheet draws from one of the four NPC slots, the same one on every map, and
                  no colour in it may change -- the figure is drawn from what its slot already has
    the FRAMES    the pic table indexes a fixed count; ten here (nine plus ANIM_RAISE_HAND)

THE SPECIES IS THE ROLE (9.4), and two sets are spoken for: the Clears are foxes, and the eight
BENCHMARK leaders are the tortoise, hippo, hare, bowerbird, toad, chameleon, salamander and cobra.
A class's portrait and its overworld sheet are ONE species, so these choices bind T-120's portraits
too -- the hiker's picture, when it is drawn, is this badger.

    hiker        a badger      digs in, carries the mountain on his back      npc_white
    fisher       a pelican     the bill IS the tackle                         npc_white
    channeler    a bat         at home in the dark the tower keeps            npc_white
    woman_2      a ewe                                                        npc_white
    balding_man  a vulture     bald by trade, patient by nature               npc_white
    picnicker    a hedgehog                                                   npc_green
    bug_catcher  a swallow     catches them on the wing                       npc_green
    youngster    a mouse                                                      npc_blue
    lass         a lamb                                                       npc_blue
    rocker       a skunk       the stripe was always a mohawk                 npc_blue
    sailor       an albatross  the one who is always at sea                   npc_pink
    old_man_1    an old goat                                                  npc_pink

Still to come in T-120: the biker (twenty frames, its own riding animation), the little girl
(a 16x16 sheet), the nine-frame worker and chef, the thirty-odd low-use sheets, and every
trainer portrait.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import overlay, figure, check, sheet, read_pal, PEOPLE, WHITE, GREEN
from genleaders import BLUE, PINK
from gentowns import mammal, bird, fig, put, pad, TAIL, CANE, CANE_X

PREVIEW = "/tmp/trainers_ow.png"
WRITE = "--write" in sys.argv


# ============================================================ npc_white
# a peach  s S skin  e dark red-brown  T sand-gold  t olive  u dark olive  R orange-red
# r red-brown  E darkest brown  w pale grey  g grey  G dark grey  W white  K black
_h = mammal("W", "g", "W")                                   # a BADGER: the stripe runs through the eye
_h = (put(put(put(_h[0], 4, 3, "K"), 5, 3, "K"), 6, 3, "K"),
      put(put(_h[1], 4, 3, "K"), 5, 3, "K"), put(put(_h[2], 4, 4, "K"), 5, 4, "K"))
BADGER = fig(_h, "g", "T", "G", "G", "E")

PELICAN = fig(bird("W", "g", "T"), "g", "w", "G", "T", "T")   # a PELICAN: the bill IS the tackle
PELICAN = (overlay(PELICAN[0], 6, ["KTTTTK"], 5), PELICAN[1], PELICAN[2])
PELICAN = (overlay(PELICAN[0], 7, ["KTTK"], 6), PELICAN[1], PELICAN[2])    # the pouch hangs below it
PELICAN = (PELICAN[0], PELICAN[1], overlay(PELICAN[2], 4, ["KTTTTTK"], 0))
PELICAN = (PELICAN[0], PELICAN[1], overlay(PELICAN[2], 5, ["KTTTK"], 1))

# A MOTH cannot be drawn here: sixteen pixels wide leaves two columns either side of the body, so
# its wings read as arms and its antennae as horns -- the first draft was a grey cow. A BAT keeps
# the tower's meaning and puts its whole silhouette in the EARS, which sixteen pixels can carry.
_h = mammal("w", "G", "W")                                   # a BAT: the ears are the read
BAT = fig(_h, "w", "W", "W", "w", "g")
for _l in (2, 11):
    BAT = (overlay(BAT[0], 0, ["KGK", "KGK", "KwK"], _l), overlay(BAT[1], 0, ["KGK", "KGK", "KGK"], _l), BAT[2])
BAT = (BAT[0], BAT[1], overlay(BAT[2], 0, ["KGK", "KGK", "KwK"], 5))
for _side, _col in ((0, 0), (14, 14)):                       # wings folded down the robe
    BAT = (overlay(BAT[0], 11, ["Kg" if _col == 0 else "gK"] * 4 + ["KK"], _col),
           overlay(BAT[1], 11, ["Kg" if _col == 0 else "gK"] * 4 + ["KK"], _col), BAT[2])

EWE = fig(mammal("W", "S", "a"), "W", "r", "r", "a", "E")     # a EWE

# Bald and peach with a gold bill at the centre, the first draft read as a MAN WITH A MOUSTACHE --
# the trap the walrus fell into. The beak has to be hooked and in profile, and the ruff has to be
# two rows of real feathers, or there is no bird here at all.
# Even hooked, a PEACH DOME with a gold mark at its centre is a man with a moustache. So the head
# goes dark and small, and the bare skin shrinks to a crown patch: a vulture is a dark bird with a
# bare head, not a bald person with a beak.
_h = bird("G", "S", "T")                                     # a VULTURE: bald by trade, patient by nature
_h = (put(put(_h[0], 2, 5, "S"), 3, 4, "S"), put(put(_h[1], 2, 5, "S"), 3, 4, "S"), put(_h[2], 2, 6, "S"))
VULTURE = fig(_h, "G", "G", "u", "T", "T")
VULTURE = (overlay(VULTURE[0], 7, ["KEEK"], 6), VULTURE[1], VULTURE[2])          # the hook, dark
VULTURE = (overlay(VULTURE[0], 8, ["KGGGGK"], 5), overlay(VULTURE[1], 8, ["KGGGGK"], 5),
           overlay(VULTURE[2], 8, ["KGGGK"], 4))
VULTURE = (overlay(VULTURE[0], 9, ["GGGGGG"], 5), overlay(VULTURE[1], 9, ["GGGGGG"], 5), VULTURE[2])
VULTURE = (VULTURE[0], VULTURE[1], overlay(VULTURE[2], 4, ["KTTTTK"], 0))        # a long beak in profile
VULTURE = (VULTURE[0], VULTURE[1], overlay(VULTURE[2], 5, ["KETK"], 1))          # hooked down at the tip

# ============================================================ npc_green
# a peach  s S skin  e red-brown  y gold  o dark gold  Y dark olive  l light green  J green
# N dark green  p pink  q magenta  b plum  W white  K black
# A gold EAR on a brown head is a horn: the first draft was a bull. A hedgehog's ears are nothing,
# and its crown is everything -- so the ear takes the fur's own colour and the spines run across it.
_h = mammal("o", "o", "e")                                   # a HEDGEHOG: a dark snout, or the face reads human
_h = (put(put(_h[0], 4, 4, "Y"), 4, 6, "Y"), put(put(put(_h[1], 4, 4, "Y"), 5, 6, "Y"), 6, 4, "Y"),
      put(_h[2], 4, 6, "Y"))
HEDGEHOG = fig(_h, "a", "p", "J", "a", "e")
HEDGEHOG = (overlay(HEDGEHOG[0], 3, ["KYoYoYK"], 4), overlay(HEDGEHOG[1], 3, ["KYoYoYK"], 4),
            overlay(HEDGEHOG[2], 3, ["KYoYoK"], 4))
HEDGEHOG = (overlay(HEDGEHOG[0], 2, ["KoYoK"], 5), overlay(HEDGEHOG[1], 2, ["KoYoK"], 5),
            overlay(HEDGEHOG[2], 2, ["KoYK"], 5))

SWALLOW = fig(bird("N", "l", "y"), "N", "W", "J", "y", "y")   # a SWALLOW: catches them on the wing
SWALLOW = (SWALLOW[0], overlay(SWALLOW[1], TAIL, ["KNNK", "KNJK", " KK "], 6), SWALLOW[2])

# ============================================================ npc_blue
# a peach  s S skin  e red-brown  y yellow  o gold  Y dark gold  v light purple  V purple
# D dark purple-grey  O orange  r red  d dark brown  W white  K black
MOUSE = fig(mammal("s", "S", "a"), "s", "y", "V", "s", "d")   # a MOUSE: round ears, a thin tail
for _l in (1, 11):
    MOUSE = (overlay(MOUSE[0], 3, ["KSSK", "KSSK", " KK "], _l), overlay(MOUSE[1], 3, ["KSSK", "KSSK", " KK "], _l), MOUSE[2])
MOUSE = (MOUSE[0], overlay(MOUSE[1], TAIL, ["KsK", " KsK", "  KK"], 7), overlay(MOUSE[2], TAIL, ["KsK", " KsK", "  KK"], 10))

LAMB = fig(mammal("W", "S", "a"), "W", "v", "v", "a", "d")    # a LAMB

_h = mammal("D", "D", "W")                                   # a SKUNK: the stripe was always a mohawk
_h = (put(put(put(_h[0], 4, 7, "W"), 5, 7, "W"), 6, 7, "W"),
      put(put(put(_h[1], 4, 7, "W"), 5, 7, "W"), 6, 7, "W"), put(_h[2], 4, 7, "W"))
SKUNK = fig(_h, "D", "r", "D", "D", "K")
SKUNK = (SKUNK[0], overlay(SKUNK[1], TAIL, ["KWWK", "KWDK", "KWWK", " KK "], 6),
         overlay(SKUNK[2], TAIL, ["KWWK", "KWDK", " KK "], 10))

# ============================================================ npc_pink
# a peach  s S skin  e red-brown  p pink  P rose  m dark rose  c light blue  B blue
# n dark navy  w pale grey  g grey  G dark grey  W white  K black
ALBATROSS = fig(bird("W", "g", "P"), "g", "W", "B", "P", "P")  # an ALBATROSS: always at sea
ALBATROSS = (overlay(ALBATROSS[0], 10, ["BB"], 7), overlay(ALBATROSS[1], 10, ["BB"], 7), ALBATROSS[2])

_h = mammal("w", "g", "W")                                    # an OLD GOAT: horns, beard, a cane
GOAT = fig(_h, "w", "c", "G", "w", "n")
GOAT = (overlay(GOAT[0], 2, ["KGK", "KGK"], 3), overlay(GOAT[1], 2, ["KGK", "KGK"], 3), overlay(GOAT[2], 2, ["KGK"], 4))
GOAT = (overlay(GOAT[0], 2, ["KGK", "KGK"], 12), overlay(GOAT[1], 2, ["KGK", "KGK"], 12), GOAT[2])
GOAT = (overlay(GOAT[0], 8, ["KWWK"], 6), GOAT[1], overlay(GOAT[2], 8, ["KWK"], 5))
GOAT = (overlay(GOAT[0], CANE, ["KK", "nK", "nK", "nK", "nK", "nK", "nK", "KK"], CANE_X), GOAT[1], GOAT[2])


SHEETS = [   # the sheet vanilla shipped, our species, the frames, its palette -- ten frames each
    ("badger",    "hiker.png",       BADGER,    "g", WHITE, "npc_white.pal"),
    ("pelican",   "fisher.png",      PELICAN,   "T", WHITE, "npc_white.pal"),
    ("bat",       "channeler.png",   BAT,       "w", WHITE, "npc_white.pal"),
    ("ewe",       "woman_2.png",     EWE,       "a", WHITE, "npc_white.pal"),
    ("vulture",   "balding_man.png", VULTURE,   "T", WHITE, "npc_white.pal"),
    ("hedgehog",  "picnicker.png",   HEDGEHOG,  "a", GREEN, "npc_green.pal"),
    ("swallow",   "bug_catcher.png", SWALLOW,   "y", GREEN, "npc_green.pal"),
    ("mouse",     "youngster.png",   MOUSE,     "s", BLUE,  "npc_blue.pal"),
    ("lamb",      "lass.png",        LAMB,      "a", BLUE,  "npc_blue.pal"),
    ("skunk",     "rocker.png",      SKUNK,     "D", BLUE,  "npc_blue.pal"),
    ("albatross", "sailor.png",      ALBATROSS, "P", PINK,  "npc_pink.pal"),
    ("goat",      "old_man_1.png",   GOAT,      "w", PINK,  "npc_pink.pal"),
]


def main():
    rows, built = [], []
    for name, filename, art, hand, index, palname in SHEETS:
        frames = figure(art[0], art[1], art[2], extra_hand=hand)
        check(name, frames, index)
        old = Image.open(os.path.join(PEOPLE, filename))
        assert len(frames) == old.width // 16, "%s: %d frames drawn, the pic table indexes %d" % (
            name, len(frames), old.width // 16)
        assert old.size[1] == 32, "%s: %s is %dpx tall, not 32" % (name, filename, old.size[1])
        img = sheet(frames, index, read_pal(palname))
        assert img.size == old.size, "%s: %s would change size %s -> %s" % (name, filename, old.size, img.size)
        built.append((filename, img))
        bg = Image.new("RGB", img.size, (150, 150, 150))
        bg.paste(img.convert("RGB"), (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        rows.append(bg)
        rows.append(old.convert("RGB"))
    w = max(r.width for r in rows) * 4
    out = Image.new("RGB", (w, 32 * 4 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 4, 128), Image.NEAREST), (0, 128 * i))
    out.save(PREVIEW)
    print("  %d sheets -> preview %s (each: ours on grey, then vanilla's underneath)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
        print("  written %d sheets in place: %s" % (len(built), ", ".join(f for f, _ in built)))


if __name__ == "__main__":
    main()

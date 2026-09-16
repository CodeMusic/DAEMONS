#!/usr/bin/env python3
"""The named and story characters, drawn as a fable (T-120; vision.md 9.4).

    python3 tools/gennamed.py            # preview to /tmp/named_ow.png
    python3 tools/gennamed.py --write    # overwrite the sheets in place

A CLASS gets a species for its ROLE. A NAMED PERSON gets one for WHO THEY ARE, and the design
already says who most of these are, so the species were read out of the bible and the game's own
dialogue rather than invented:

    lorelei     PHLEGMATIC   a polar bear   white, FROZEN, "there is no hurry. there never is"
    bruno       CHOLERIC     a tiger        hot, driven, "every battle is an argument"
    agatha      MELANCHOLIC  a wombat       black bile and earth; burrowing, heavy, LATENT
    lance       SANGUINE     a cardinal     red and air, EMERGENT, and he leads the Board
    bill        HOLT         a river otter  the bible names the species itself (4.20a)
    mr_fuji     INIT         a tapir        takes in every daemon left at his door
    celio       CELIO        a mongoose     builds the bridge between two systems (8.2a)
    captain     the captain  a cormorant    a seabird, and seasick
    gym_guy     the greeter  a hamster      says welcome, in two buildings
    trainer_tower_dude       a marmot       upright and watchful, on every floor of the tower
    gba_kid                  a chipmunk     a kid with a machine

THE REVIEW BOARD ARE THE FOUR HUMOURS and section 6 reserves their colours: *sanguine red, choleric
yellow, melancholic black, phlegmatic white -- and give them to nobody else.* Three of the four land
exactly. **CHOLERIC's yellow does not exist in the slot his sprite draws from**: `bruno` is locked to
npc_white, whose nearest is a sand-gold. 6804 says value carries the humours in greyscale anyway
(*melancholic dark, phlegmatic pale, sanguine and choleric mid*), which the sand-gold satisfies --
recorded here because it is a compromise, not a match.

HOLT IS AN OTTER AND DOLDRUM'S ADULT IS ALSO AN OTTER. 4.20a names his species and gives the reason
(*"a holt is specifically an otter's den... an otter is at home in two elements, which is the man who
held two frames in one address"*), which outranks a town local chosen later. He is a RIVER otter in
the blue slot; DOLDRUM's is a sea otter in the town's own palette, on maps he never stands on.

FRAME COUNTS ARE VANILLA'S. Six of these sheets hold nine frames; five hold THREE, because their pic
tables name ids 0,1,2 and repeat them, and every one of those objects is MOVEMENT_TYPE_FACE_DOWN.
Every sheet here overwrites a vanilla filename, so each inherits vanilla's own conversion rule.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import overlay, figure, check, sheet, read_pal, ensure_rule, PEOPLE, WHITE, GREEN
from genleaders import BLUE, PINK
from gentowns import mammal, bird, fig, put, TAIL

PREVIEW = "/tmp/named_ow.png"
WRITE = "--write" in sys.argv


# ============================================================ THE REVIEW BOARD -- section 6's colours
# npc_white: a peach  s S skin  e dark red-brown  T sand-gold  t olive  u dark olive  R orange-red
#            r red-brown  E darkest brown  w pale grey  g grey  G dark grey  W white  K black
_h = mammal("W", "w", "W")                                   # PHLEGMATIC: white, and it does not move
POLAR_BEAR = fig(_h, "W", "w", "g", "W", "g")
POLAR_BEAR = (overlay(POLAR_BEAR[0], 9, ["ww"], 7), POLAR_BEAR[1], POLAR_BEAR[2])

_h = mammal("T", "E", "W")                                   # CHOLERIC: the stripes are the argument
_h = (put(put(put(_h[0], 4, 4, "E"), 4, 6, "E"), 6, 3, "E"),
      put(put(put(_h[1], 4, 4, "E"), 5, 6, "E"), 6, 3, "E"), put(put(_h[2], 4, 5, "E"), 5, 7, "E"))
TIGER = fig(_h, "T", "R", "E", "T", "E")

# npc_pink: a s S peach  e dark brown  p pink  P rose  m dark rose  c light blue  B blue
#           n dark navy  w pale grey  g grey  G dark grey  W white  K black
WOMBAT = fig(mammal("G", "n", "g"), "G", "n", "n", "G", "n")  # MELANCHOLIC: black bile, earth, weight

_h = bird("R", "r", "T")                                     # SANGUINE: red, air, and he leads
CARDINAL = fig(_h, "R", "r", "E", "T", "T")
CARDINAL = (overlay(CARDINAL[0], 0, ["KRRK"], 6), overlay(CARDINAL[1], 0, ["KRRK"], 6),
            overlay(CARDINAL[2], 0, ["KRRK"], 5))            # the crest

# ============================================================ HOLT, and the rest
# npc_blue: a s S peach  e brown-red  y yellow  o gold  Y dark gold  v light purple  V purple
#           D dark purple-grey  O orange  r red  d dark brown  W white  K black
_h = mammal("d", "d", "a")                                   # HOLT: a river otter, at home in two elements
OTTER = fig(_h, "d", "v", "D", "d", "d")
OTTER = (OTTER[0], overlay(OTTER[1], TAIL, ["KddK", "KdDK", "KddK", " KK "], 6),
         overlay(OTTER[2], TAIL, ["KddK", "KdDK", " KK "], 10))

# INIT: a tapir, and the TRUNK is the whole read -- a pale patch on the chin is just a muzzle. It has
# to hang BELOW the jaw in front, and reach out past the face in profile, or there is no tapir here.
_h = mammal("G", "G", "w")
_h = (put(_h[0], 7, 5, "w"), _h[1], put(_h[2], 6, 2, "w"))
TAPIR = fig(_h, "G", "W", "w", "G", "E")
# Row 8 is the last HEAD row and row 9 is the shirt's first, so a trunk drawn there straddles the
# collar and reads as a white bib -- the vulture's failure again, a face part landing as clothing.
# It hangs from row 7, under the jaw, where the head still is.
TAPIR = (overlay(TAPIR[0], 7, ["KwwK"], 6), TAPIR[1], overlay(TAPIR[2], 6, ["KwwwK"], 0))
TAPIR = (overlay(TAPIR[0], 8, [" KK "], 6), TAPIR[1], overlay(TAPIR[2], 7, [" KKK"], 0))

MONGOOSE = fig(mammal("T", "t", "a"), "T", "W", "g", "T", "E")    # CELIO: alert, quick, at a machine

_h = bird("G", "g", "T")                                     # the captain: a cormorant in whites
CORMORANT = fig(_h, "G", "W", "G", "T", "T")
CORMORANT = (overlay(CORMORANT[0], 1, ["KWWWWK"], 5), overlay(CORMORANT[1], 1, ["KWWWWK"], 5),
             overlay(CORMORANT[2], 1, ["KWWWK"], 4))         # the cap

HAMSTER = fig(mammal("S", "p", "a"), "S", "c", "n", "S", "e")     # the greeter

MARMOT = fig(mammal("t", "t", "a"), "t", "T", "u", "t", "E")      # the tower's attendant

_h = mammal("S", "S", "a")                                   # a kid with a machine: the stripes
_h = (put(put(_h[0], 4, 4, "e"), 6, 4, "e"), put(put(_h[1], 4, 4, "e"), 5, 6, "e"), put(_h[2], 4, 6, "e"))
CHIPMUNK = fig(_h, "S", "p", "n", "S", "e")


# NOT ONE OF THESE HAS A RAISED HAND. The raised hand IS the tenth frame -- ANIM_RAISE_HAND indexes
# it -- and every nine-frame sheet here holds exactly nine, so asking for one drew a frame the file
# has no room for. Six sheets are nine frames of walks; five are three still frames.
SHEETS = [   # vanilla's sheet, who they are, the art, the palette, and whether it is a standing still
    ("polar bear", "lorelei.png",            POLAR_BEAR, None, WHITE, "npc_white.pal", False),
    ("tiger",      "bruno.png",              TIGER,      None, WHITE, "npc_white.pal", True),
    ("wombat",     "agatha.png",             WOMBAT,     None, PINK,  "npc_pink.pal",  True),
    ("cardinal",   "lance.png",              CARDINAL,   None, WHITE, "npc_white.pal", True),
    ("otter",      "bill.png",               OTTER,      None, BLUE,  "npc_blue.pal",  False),
    ("tapir",      "mr_fuji.png",            TAPIR,      None, WHITE, "npc_white.pal", False),
    ("mongoose",   "celio.png",              MONGOOSE,   None, WHITE, "npc_white.pal", False),
    ("cormorant",  "captain.png",            CORMORANT,  None, WHITE, "npc_white.pal", False),
    ("hamster",    "gym_guy.png",            HAMSTER,    None, PINK,  "npc_pink.pal",  False),
    ("marmot",     "trainer_tower_dude.png", MARMOT,     None, WHITE, "npc_white.pal", True),
    ("chipmunk",   "gba_kid.png",            CHIPMUNK,   None, PINK,  "npc_pink.pal",  True),
]


def main():
    rows, built = [], []
    for name, filename, art, hand, index, palname, still in SHEETS:
        frames = figure(art[0], art[1], art[2], extra_hand=hand, still=still)
        check(name, frames, index)
        old = Image.open(os.path.join(PEOPLE, filename))
        assert len(frames) == old.width // 16, "%s: %d frames drawn, %s holds %d" % (
            name, len(frames), filename, old.width // 16)
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
        added = 0
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
            added += ensure_rule(filename)     # every one of these is an overwrite, so none should be new
        print("  written %d sheets in place%s" % (len(built), "" if not added else "; %d NEEDED A RULE" % added))
        print("  " + ", ".join(f for f, _ in built))


if __name__ == "__main__":
    main()

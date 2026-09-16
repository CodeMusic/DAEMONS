#!/usr/bin/env python3
"""The four classes whose overworld sprite was somebody else's (T-126; vision.md 9.4).

    python3 tools/genclasses.py            # preview to /tmp/classes_ow.png, and what would be repointed
    python3 tools/genclasses.py --write    # four sheets, their registration, and the ten map objects

VANILLA REUSES SPRITES ACROSS CLASSES AND IT USED TO BE INVISIBLE. A Burglar walks the MANSION on
the Poke Maniac's sheet, a Juggler stands in SILPH on the Rocker's, a Breeder in PATTERN BUSH on the
Woman's, a Ruin Maniac in the LOST CAVE on the Hiker's -- and while all of them were generic humans
nobody could tell. T-120 made a class's portrait and its overworld sheet ONE SPECIES, and the moment
they became animals the reuse started reading as a contradiction: an opossum who battles as a weasel.

So these four get sheets of THEIR OWN. Not a redraw of somebody else's sheet -- that would move the
opossum, who is correct where she stands -- but four NEW object graphics, registered and pointed at
by the ten objects the join below finds.

    BURGLAR          a WEASEL     narrow enough to be already inside; the mask is the eye stripe
    JUGGLER          an OCTOPUS   eight arms, and the only honest way to keep six balls up
    POKEMON_BREEDER  a GOOSE      sits the egg, and will see you off the nest
    RUIN_MANIAC      an AARDVARK  digs where the ruin is, by the nose

A SHEET INHERITS THE SLOT OF THE SPRITE IT REPLACES, and that is not decoration. The engine patches
the palette named by a sprite's TAG into the SLOT named by its info, so two sprites that share a
slot with different tags repaint each other. Each of these four is registered on the same (tag,
slot) pair as the sheet standing in for it today -- pink/2 for the maniac, blue/1 for the rocker,
white/4 for the woman and the hiker -- so the palette is already loaded on every map it appears on
and nothing else on that map changes colour. Each figure is therefore drawn from the sixteen that
slot already has; no colour is added.

WHO IS REPOINTED IS DERIVED, NOT TYPED. `trainers.h` gives each trainer its portrait; every
`trainerbattle` in a map's scripts gives a script label its trainer; a map object names the script it
runs. Joining the three finds the objects that BATTLE as one of these four, which is the only test
that matters -- their current graphics_id is the wrong answer, not the question. Running again after
--write finds them already correct and does nothing.
"""
import glob, json, os, re, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import overlay, figure, check, sheet, read_pal, ensure_rule, PEOPLE, GBA, WHITE, GREEN
from genleaders import BLUE, PINK
from gentowns import mammal, bird, fig, put, pad, TAIL, register_one, camel

PREVIEW = "/tmp/classes_ow.png"
WRITE = "--write" in sys.argv


# ============================================================ BURGLAR: a WEASEL (npc_pink, slot 2)
# a peach  s S skin  e red-brown  p pink  P rose  m dark rose  c light blue  B blue
# n dark navy  w pale grey  g grey  G dark grey  W white  K black
# The eye stripe does two jobs at once: a stoat wears one, and so does a burglar. Without it a tan
# head over a cream muzzle is a person in a hood, which is what the first draft was.
_h = mammal("S", "S", "a")
_h = (put(put(_h[0], 5, 3, "e"), 5, 5, "e"), put(_h[1], 5, 3, "e"), put(_h[2], 5, 4, "e"))
WEASEL = fig(_h, "S", "e", "e", "S", "n")                    # a dark hood and dark boots
WEASEL = (WEASEL[0],
          overlay(WEASEL[1], 9, ["KwwwwK", "wwwwww", "wwwwww", "KwwwwK"], 5),   # the swag, carried on its back
          overlay(WEASEL[2], 10, ["Kww", "Kww", "KwK"], 10))
WEASEL = (WEASEL[0], overlay(WEASEL[1], TAIL, ["KSSK", "KSeK", "KSSK", " KK "], 6),
          overlay(WEASEL[2], TAIL, ["KSSK", "KSeK", " KK "], 10))


# ============================================================ JUGGLER: an OCTOPUS (npc_blue, slot 1)
# a peach  s S skin  e red-brown  y yellow  o gold  Y dark gold  v light purple  V purple
# D dark purple-grey  O orange  r red  d dark brown  W white  K black
# No ears and no muzzle, so mammal() cannot carry it: the read is a DOME that comes down to the
# shoulders, two wide eyes low on it, and arms that are tentacles. The shirt is striped by giving
# fig() four letters instead of one -- vertical stripes, which is what a juggler wears.
# The eye is a PALE BAND WITH A BLACK BAR UNDER IT -- the horizontal pupil is the thing everyone
# recognises, and two dark pixels alone read as a hood's eye holes rather than an animal's eye.
OCTO_FRONT = ["    KKKK", "  KKVVVV", " KVVVVVV", " KVVVVVV", " KVWWWvv", " KVKKKvv", "  KVvvvv", "   KVvvv", "    KKvv"]
OCTO_BACK = ["    KKKK", "  KKVVVV", " KVVVVVV", " KVVVVVV", " KVVVVVV", " KVVVVVV", "  KVVVVV", "   KVVVV", "    KKVV"]
OCTO_SIDE = ["   KKKKK", "  KVVVVVVK", " KVVVVVVVK", " KVVVVVVVK", "KVWWWVVVVK", "KVKKKvVVVK", " KvvvvvVVK", "  KvvvvVK", "   KKvvK"]
OCTOPUS = fig((OCTO_FRONT, OCTO_BACK, OCTO_SIDE), "V", "yoyo", "d", "V", "d")
for _side, _col in ((0, 0), (1, 13)):                        # tentacles hanging either side of the dome
    _patch = [" KV", "KVv", "KVV", "KvV", "KVv", " KK"] if _col == 0 else ["VK ", "vVK", "VVK", "VvK", "vVK", "KK "]
    OCTOPUS = (overlay(OCTOPUS[0], 5, _patch, _col), overlay(OCTOPUS[1], 5, _patch, _col), OCTOPUS[2])
OCTOPUS = (OCTOPUS[0], OCTOPUS[1], overlay(OCTOPUS[2], 6, ["KvK", "KVK", "KvK", "KK"], 8))
# Three balls in the air, one column clear of the dome on either side. Row 0 survives the walk
# frames -- standing() pads eight blank rows above the art and walk() drops the figure into them.
OCTOPUS = tuple(overlay(overlay(fr, 0, ["KOK"], 0), 1, ["KrK"], 13) for fr in OCTOPUS)


# ============================================================ POKEMON_BREEDER: a GOOSE (npc_white, slot 4)
# a peach  s S skin  e dark red-brown  T sand-gold  t olive  u dark olive  R orange-red
# r red-brown  E darkest brown  w pale grey  g grey  G dark grey  W white  K black
GOOSE = fig(bird("W", "W", "R"), "W", "t", "u", "R", "R")    # a white goose in an olive apron, orange-footed
GOOSE = (overlay(GOOSE[0], 12, ["KaaK", "KaaK"], 6), GOOSE[1], GOOSE[2])          # the egg, sat in both wings


# ============================================================ RUIN_MANIAC: an AARDVARK (npc_white, slot 4)
# The nose is the animal. A sand-coloured mammal with round ears is a mouse at this size, so the
# ears go tall and the snout is pushed a long way past the face on the side view, where a profile
# can carry it.
_h = mammal("T", "s", "T")
AARDVARK = fig(_h, "T", "t", "u", "T", "E")
for _l in (2, 11):
    AARDVARK = (overlay(AARDVARK[0], 0, ["KsK", "KTK", "KTK"], _l),
                overlay(AARDVARK[1], 0, ["KsK", "KTK", "KTK"], _l), AARDVARK[2])
AARDVARK = (AARDVARK[0], AARDVARK[1], overlay(AARDVARK[2], 0, ["KsK", "KTK", "KTK"], 5))
# The snout hangs PAST THE CHIN and onto the collar on the front view, and runs a long way out in
# profile: tall ears over a short face is a rabbit, and only the nose settles which animal this is.
AARDVARK = (overlay(overlay(AARDVARK[0], 8, ["KTTK"], 6), 9, ["KTTK"], 6), AARDVARK[1], AARDVARK[2])
AARDVARK = (AARDVARK[0], AARDVARK[1], overlay(overlay(overlay(overlay(
    AARDVARK[2], 5, ["KKKK"], 0), 6, ["KTTT"], 0), 7, ["KTTT"], 0), 8, ["KKKK"], 0))
AARDVARK = (AARDVARK[0], overlay(AARDVARK[1], TAIL, ["KTTK", "KTTK", "KTK", " KK"], 6),
            overlay(AARDVARK[2], TAIL, ["KTTTK", "KTTK", " KK"], 10))


# ============================================================ the second batch (T-126, widened)
# Eleven more classes, found once the join read all 726 battle labels instead of 258. Same rule as
# the four above and same method: the species is the portrait's, the palette is the slot's, and the
# sheet each replaces is the one vanilla was standing in with.

# ---- BIRD_KEEPER: an OSTRICH (npc_blue, slot 1) -- a small head a long way up
# bird() gives a head that sits ON the shoulders, which is every other bird here and wrong for this
# one: the whole read is the NECK. So the head is drawn small and high and the neck is four rows.
OSTRICH_F = ["     KKK", "    KDDD", "    KDKD", "    KDDD", "    KDDO", "      Ka", "      Ka", "      Ka", "      Ka"]
OSTRICH_B = ["     KKK", "    KDDD", "    KDDD", "    KDDD", "    KDDD", "      Ka", "      Ka", "      Ka", "      Ka"]
OSTRICH_S = ["     KKKK", "    KDDDK", "  KOODDDK", "    KDKDK", "    KDDDK", "    KaaK", "    KaaK", "    KaaK", "    KaaK"]
OSTRICH = fig((OSTRICH_F, OSTRICH_B, OSTRICH_S), "D", "D", "D", "a", "O")

# ---- GAMER: a JACKAL (npc_pink, slot 2) -- and never a fox, which is the Clears' (9.4)
_h = mammal("g", "g", "w")
JACKAL = fig(_h, "g", "n", "n", "g", "K")
for _l in (2, 11):                                            # the ears are tall and come to a point
    JACKAL = (overlay(JACKAL[0], 0, ["KgK", "KgK", "KgK"], _l),
              overlay(JACKAL[1], 0, ["KGK", "KGK", "KGK"], _l), JACKAL[2])
JACKAL = (JACKAL[0], JACKAL[1], overlay(JACKAL[2], 0, ["KgK", "KgK", "KgK"], 5))
JACKAL = (JACKAL[0], overlay(JACKAL[1], TAIL, ["KggK", "KGgK", "KggK", " KK "], 6),
          overlay(JACKAL[2], TAIL, ["KggK", "KGgK", " KK "], 10))

# ---- PAINTER: a TOUCAN (npc_blue, slot 1) -- MATTE owns the chameleon
# The bill is half the bird and has to be drawn that way; a toucan with a normal beak is a crow.
TOUCAN = fig(bird("d", "W", "y"), "d", "W", "D", "y", "y")
TOUCAN = (overlay(overlay(TOUCAN[0], 5, ["KyyK"], 6), 6, ["KyOK"], 6), TOUCAN[1],
          overlay(overlay(overlay(TOUCAN[2], 3, ["KyyyK"], 0), 4, ["KyyyyK"], 0), 5, ["KyOOK"], 1))

# ---- SUPER_NERD: a RING-TAILED LEMUR (npc_white, slot 4)
_h = mammal("g", "w", "W")
_h = (put(put(_h[0], 5, 3, "K"), 5, 5, "K"), _h[1], put(_h[2], 5, 4, "K"))     # the dark eye patches
LEMUR = fig(_h, "g", "W", "G", "g", "G")                      # a white coat, as the scientist wore
LEMUR = (LEMUR[0], overlay(LEMUR[1], TAIL, ["KWWK", "KGGK", "KWWK", " KK "], 6),
         overlay(LEMUR[2], TAIL, ["KWWK", "KGGK", "KWWK", " KK "], 10))

# ---- AROMA_LADY: a HONEYBEE (npc_white, slot 4) -- 8.2b's hive, which talks by dancing
# THE FIRST DRAFT WAS A BULL. mammal() gives a head with an ear at each top corner, and two straight
# stalks above a tan face are HORNS -- engine.md has this exact failure recorded twice already (a
# gold ear on a brown head, and the moth whose antennae read as horns). So there is no mammal head
# here: a bee is a pair of COMPOUND EYES that take the sides of the whole face, and the antennae are
# short, two rows not three, and end in a KNOB, which is what a horn never does.
BEE_F = ["", "", "    KKKK", "   KTTTT", "   KKKTT", "   KKKTT", "   KTTTT", "    KTTu", "     KKu"]
BEE_B = ["", "", "    KKKK", "   KTTTT", "   KTTTT", "   KTTTT", "   KTTTT", "    KTTu", "     KKu"]
BEE_S = ["", "", "    KKKKK", "   KTTTTTK", "  KKKKTTTK", "  KKKKTTTK", "   KTTTTTK", "    KTTuuK", "     KKuK"]
BEE = fig((BEE_F, BEE_B, BEE_S), "T", "TuTu", "u", "T", "u")   # the stripes are the shirt, four letters not one
for _col in (2, 11):                                           # antennae: a stalk and a knob, angled off the crown
    BEE = (overlay(overlay(BEE[0], 0, ["KwK"], _col), 1, ["KuK"], _col),
           overlay(overlay(BEE[1], 0, ["KwK"], _col), 1, ["KuK"], _col), BEE[2])
BEE = (BEE[0], BEE[1], overlay(overlay(BEE[2], 0, ["KwK"], 3), 1, ["KuK"], 3))
BEE = (BEE[0], overlay(overlay(BEE[1], 10, ["Kww", "Kww", "KwK"], 1), 10, ["wwK", "wwK", "KwK"], 12),
       overlay(BEE[2], 10, ["Kww", "Kww", "KwK"], 8))         # a pair of wings, folded at rest

# ---- PSYCHIC_F and PSYCHIC_M: a JELLYFISH (npc_green, slot 3) -- not a second octopus
JELLY_F = ["    KKKK", "  KKpppp", " Kpppppp", " Kpppppp", " KpKWKpp", " Kppppqq", "  KpqqqW", "   Kqqqq", "    KKqq"]
JELLY_B = ["    KKKK", "  KKpppp", " Kpppppp", " Kpppppp", " Kpppppp", " Kppppqq", "  Kpqqqq", "   Kqqqq", "    KKqq"]
JELLY_S = ["   KKKKK", "  KppppppK", " KpppppppK", " KpppppppK", "KpKWKppppK", "KppppppqqK", " KpqqqqqqK", "  KqqqqqK", "   KKqqK"]
def _jelly(robe, hem):
    """one jellyfish, two robes -- the same rule the two rangers are drawn under"""
    f = fig((JELLY_F, JELLY_B, JELLY_S), "p", robe, hem, "p", hem)
    for _col, _patch in ((0, [" Kp", "Kpq", "Kqp", "Kpq", " KK"]), (13, ["pK ", "qpK", "pqK", "qpK", "KK "])):
        f = (overlay(f[0], 5, _patch, _col), overlay(f[1], 5, _patch, _col), f[2])
    return f


JELLY = _jelly("q", "b")            # PSYCHIC_F, as her picture is
JELLY_MALE = _jelly("b", "N")       # PSYCHIC_M -- DARIO, the darker robe his picture now wears

# ---- POKEMON_RANGER_M / _F: one PINE MARTEN, in two builds (npc_green, slot 3)
_h = mammal("e", "e", "a")
MARTEN_M = fig(_h, "e", "J", "N", "e", "Y")                   # the bib is the marten's own mark
MARTEN_M = (overlay(MARTEN_M[0], 9, ["KaaK"], 6), MARTEN_M[1], overlay(MARTEN_M[2], 9, ["KaK"], 5))
MARTEN_M = (MARTEN_M[0], overlay(MARTEN_M[1], TAIL, ["KeeK", "KeYK", "KeeK", " KK "], 6),
            overlay(MARTEN_M[2], TAIL, ["KeeK", "KeYK", " KK "], 10))
MARTEN_F = fig(_h, "e", "l", "N", "e", "Y")                   # the same marten, the other uniform
MARTEN_F = (overlay(MARTEN_F[0], 9, ["KaaK"], 6), MARTEN_F[1], overlay(MARTEN_F[2], 9, ["KaK"], 5))
MARTEN_F = (MARTEN_F[0], overlay(MARTEN_F[1], TAIL, ["KeeK", "KeYK", "KeeK", " KK "], 6),
            overlay(MARTEN_F[2], TAIL, ["KeeK", "KeYK", " KK "], 10))
for _l in (2, 11):                                            # hers carries the ear tufts
    MARTEN_F = (overlay(MARTEN_F[0], 1, ["KaK", "KeK"], _l), overlay(MARTEN_F[1], 1, ["KaK", "KeK"], _l), MARTEN_F[2])

# ---- LADY: a SWAN (npc_white, slot 4) -- the neck, and nothing else needed
SWAN_F = ["     KKK", "    KWWW", "    KWKW", "    KWWR", "    KKRR", "      KW", "      KW", "      KW", "      KW"]
SWAN_B = ["     KKK", "    KWWW", "    KWWW", "    KWWW", "    KWWW", "      KW", "      KW", "      KW", "      KW"]
SWAN_S = ["     KKKK", "    KWWWK", "  KRKWKWK", "    KWWWK", "    KWWWK", "    KWWK", "    KWWK", "    KWWK", "    KWWK"]
SWAN = fig((SWAN_F, SWAN_B, SWAN_S), "W", "W", "w", "R", "R")

# ---- ENGINEER: a BEAVER (npc_white, slot 4) -- a record in a material that lasts
_h = mammal("r", "r", "T")
_h = (overlay(list(_h[0]), 8, ["KWWK"], 4), _h[1], overlay(list(_h[2]), 8, ["KWK"], 3))   # the incisors
BEAVER = fig(_h, "r", "t", "u", "r", "E")
BEAVER = (BEAVER[0], overlay(BEAVER[1], TAIL, ["KEEEEK", "KEEEEK", " KEEK ", "  KK  "], 5),
          overlay(BEAVER[2], TAIL, ["KEEEK", "KEEEK", " KKK "], 10))

# ---- TAMER: a HYENA ringmaster (npc_white, slot 4)
_h = mammal("T", "T", "w")
_h = (put(put(_h[0], 4, 3, "G"), 6, 5, "G"), put(put(_h[1], 4, 3, "G"), 6, 6, "G"), put(_h[2], 4, 5, "G"))
HYENA = fig(_h, "T", "R", "G", "T", "E")                      # the ringmaster's red coat
for _l in (2, 11):                                            # round ears, set wide and high
    HYENA = (overlay(HYENA[0], 1, ["KTTK", "KGGK"], _l - 1), overlay(HYENA[1], 1, ["KTTK", "KGGK"], _l - 1), HYENA[2])
HYENA = (HYENA[0], HYENA[1], overlay(HYENA[2], 1, ["KTTK", "KGGK"], 4))


CLASSES = [
    # the portrait's class, our species, the art, the sheet, the letters, the palette, tag and slot,
    # the sprite it stands in for today, and what it is
    ("BURGLAR", "weasel", WEASEL, "burglar", PINK, "npc_pink.pal",
     "OBJ_EVENT_PAL_TAG_NPC_PINK", "PALSLOT_NPC_2", "poke_maniac.png",
     "a weasel with the swag on its back; it battles as one, so it walks as one"),
    ("JUGGLER", "octopus", OCTOPUS, "juggler", BLUE, "npc_blue.pal",
     "OBJ_EVENT_PAL_TAG_NPC_BLUE", "PALSLOT_NPC_1", "rocker.png",
     "an octopus, three balls up and five arms spare"),
    ("POKEMON_BREEDER", "goose", GOOSE, "pokemon_breeder", WHITE, "npc_white.pal",
     "OBJ_EVENT_PAL_TAG_NPC_WHITE", "PALSLOT_NPC_4", "woman_2.png",
     "a goose sitting an egg, in the apron"),
    ("RUIN_MANIAC", "aardvark", AARDVARK, "ruin_maniac", WHITE, "npc_white.pal",
     "OBJ_EVENT_PAL_TAG_NPC_WHITE", "PALSLOT_NPC_4", "hiker.png",
     "an aardvark, digging where the ruin is"),

    ("BIRD_KEEPER", "ostrich", OSTRICH, "bird_keeper", BLUE, "npc_blue.pal",
     "OBJ_EVENT_PAL_TAG_NPC_BLUE", "PALSLOT_NPC_1", "rocker.png",
     "an ostrich, keeping smaller birds -- 18 objects, the largest disagreement in the game"),
    ("GAMER", "jackal", JACKAL, "gamer", PINK, "npc_pink.pal",
     "OBJ_EVENT_PAL_TAG_NPC_PINK", "PALSLOT_NPC_2", "old_man_1.png",
     "a black-backed jackal, never a fox"),
    ("PAINTER", "toucan", TOUCAN, "painter", BLUE, "npc_blue.pal",
     "OBJ_EVENT_PAL_TAG_NPC_BLUE", "PALSLOT_NPC_1", "lass.png",
     "a toucan, the bill half the bird"),
    ("SUPER_NERD", "lemur", LEMUR, "super_nerd", WHITE, "npc_white.pal",
     "OBJ_EVENT_PAL_TAG_NPC_WHITE", "PALSLOT_NPC_4", "scientist.png",
     "a ring-tailed lemur in the white coat"),
    ("AROMA_LADY", "honeybee", BEE, "aroma_lady", WHITE, "npc_white.pal",
     "OBJ_EVENT_PAL_TAG_NPC_WHITE", "PALSLOT_NPC_4", "woman_2.png",
     "a honeybee, and the hive talks by dancing"),
    ("PSYCHIC_F", "jellyfish", JELLY, "psychic_f", GREEN, "npc_green.pal",
     "OBJ_EVENT_PAL_TAG_NPC_GREEN", "PALSLOT_NPC_3", "woman_1.png",
     "a jellyfish, which is not a second octopus"),
    ("PSYCHIC_M", "jellyfish", JELLY_MALE, "psychic_m", GREEN, "npc_green.pal",
     "OBJ_EVENT_PAL_TAG_NPC_GREEN", "PALSLOT_NPC_3", "boy.png",
     "the same jellyfish in the darker robe -- DARIO, in the TRAINER TOWER"),
    ("POKEMON_RANGER_M", "pine marten", MARTEN_M, "pokemon_ranger_m", GREEN, "npc_green.pal",
     "OBJ_EVENT_PAL_TAG_NPC_GREEN", "PALSLOT_NPC_3", "camper.png",
     "a pine marten in the ranger's green"),
    ("POKEMON_RANGER_F", "pine marten", MARTEN_F, "pokemon_ranger_f", GREEN, "npc_green.pal",
     "OBJ_EVENT_PAL_TAG_NPC_GREEN", "PALSLOT_NPC_3", "picnicker.png",
     "the same marten, the other uniform"),
    ("LADY", "swan", SWAN, "lady", WHITE, "npc_white.pal",
     "OBJ_EVENT_PAL_TAG_NPC_WHITE", "PALSLOT_NPC_4", "woman_2.png",
     "a swan, carried by the neck"),
    ("ENGINEER", "beaver", BEAVER, "engineer", WHITE, "npc_white.pal",
     "OBJ_EVENT_PAL_TAG_NPC_WHITE", "PALSLOT_NPC_4", "balding_man.png",
     "a beaver, a record in a material that lasts"),
    ("TAMER", "hyena", HYENA, "tamer", WHITE, "npc_white.pal",
     "OBJ_EVENT_PAL_TAG_NPC_WHITE", "PALSLOT_NPC_4", "man.png",
     "a hyena ringmaster"),
]
FRAMES = 9                       # nine, so no raised hand: none of these is ever a script's greeter

# DEFERRED, and named here so it is not lost: CUE_BALL, a rhinoceros, 8 objects on Routes 16-18.
# It stands on BIKER, which is the one sheet in this batch that is not 16x32 -- 32x32, ten frames,
# and a MACHINE as well as a rider. Giving the class a 16x32 sheet would take the bike away from a
# trainer vanilla deliberately put in the gang, so it wants the biker's own geometry and its own
# ticket; the boar took six drafts and this would be a seventh.
DEFERRED = [("CUE_BALL", "rhinoceros", "biker.png", "32x32, ten frames, and the bike is half the sprite")]


# ---------------------------------------------------------------- who battles as what
def trainer_pics():
    s = open(os.path.join(GBA, "src/data/trainers.h")).read()
    out = {}
    for m in re.finditer(r"\[(TRAINER_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \}", s, re.S):
        p = re.search(r"\.trainerPic\s*=\s*TRAINER_PIC_([A-Z0-9_]+)", m.group(2))
        if p:
            out[m.group(1)] = p.group(1)
    return out


def script_trainers():
    """the label a map object runs -> the trainer the label starts a battle with.

    EVERY .inc, not `data/maps/*/scripts.inc`. That narrower glob is what this tool shipped with and
    it sees 258 of the game's 726 battle labels, because `data/scripts/trainers.inc` is ONE shared
    file holding 468 of them -- every route and island trainer there is. It did not fail; it returned
    38 pairings where there are 72, and the repointing that followed was a third of the job.
    """
    out = {}
    for f in glob.glob(os.path.join(GBA, "data/**/*.inc"), recursive=True):
        txt = open(f, errors="ignore").read()
        for m in re.finditer(r"^(\w+)::\s*\n(.*?)(?=^\w+::|\Z)", txt, re.S | re.M):
            t = re.search(r"trainerbattle\w*\s+(TRAINER_[A-Z0-9_]+)", m.group(2))
            if t:
                out[m.group(1)] = t.group(1)
    return out


def plan_maps():
    """(map path, object index, class) for every object that BATTLES as one of the four"""
    pics, labels, todo = trainer_pics(), script_trainers(), []
    mine = {c[0]: "OBJ_EVENT_GFX_" + c[0] for c in CLASSES}
    for mp in sorted(glob.glob(os.path.join(GBA, "data/maps/*/map.json"))):
        objs = json.load(open(mp)).get("object_events", [])
        for i, o in enumerate(objs):
            cls = pics.get(labels.get(o.get("script")), "")
            if cls in mine and o.get("graphics_id") != mine[cls]:
                todo.append((mp, i, cls, o.get("graphics_id", "")))
    return todo


def register():
    def edit(path, fn):
        p = os.path.join(GBA, path); s = open(p).read(); s2 = fn(s)
        if s2 != s:
            open(p, "w").write(s2)

    for cls, species, _art, fname, _letters, _pal, tag, slot, stood_in, note in CLASSES:
        register_one(edit, "OBJ_EVENT_GFX_" + cls, camel(cls), fname, tag,
                     "the %s (T-126): %s -- its own sheet, on %s's palette and slot, where it used to borrow %s"
                     % (cls.replace("_", " ").lower(), note, tag.replace("OBJ_EVENT_PAL_TAG_NPC_", "").lower(),
                        stood_in.replace(".png", "")),
                     frames=FRAMES, slot=slot)

    ev = open(os.path.join(GBA, "include/constants/event_objects.h")).read()
    ids = {c: int(n) for c, n in re.findall(r"#define (OBJ_EVENT_GFX_\w+) (\d+)", ev)
           if c in {"OBJ_EVENT_GFX_" + x[0] for x in CLASSES}}

    def colours(s):
        start = s.index("static const u8 sTextColorTable[] =")
        end = s.index("};", start)
        body = s[start:end]
        for const, n in sorted(ids.items(), key=lambda kv: kv[1]):
            if n % 2 == 0 and ("[%s / 2]" % const) not in body:
                body += "    [%s / 2] = COLORS(NPC_TEXT_COLOR_NEUTRAL, NPC_TEXT_COLOR_NEUTRAL),\n" % const
        return s[:start] + body + s[end:]
    edit("src/dynamic_placeholder_text_util.c", colours)


def main():
    built, rows = [], []
    for cls, species, art, fname, letters, palname, _tag, _slot, stood_in, _note in CLASSES:
        frames = figure(art[0], art[1], art[2])
        assert len(frames) == FRAMES, "%s: %d frames drawn, %d registered" % (species, len(frames), FRAMES)
        check(species, frames, letters)
        img = sheet(frames, letters, read_pal(palname))
        built.append((fname + ".png", img))
        bg = Image.new("RGB", img.size, (150, 150, 150))
        bg.paste(img.convert("RGB"), (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        rows.append(bg)
        rows.append(Image.open(os.path.join(PEOPLE, stood_in)).convert("RGB"))
        print("  %-16s %-9s %s, on %s -- stood in for by %s" % (cls, species, palname[4:-4], _slot, stood_in[:-4]))

    todo = plan_maps()
    for mp, i, cls, was in todo:
        print("  repoint %-28s object %-2d %-22s -> %s" % (
            os.path.basename(os.path.dirname(mp)), i, was.replace("OBJ_EVENT_GFX_", ""), cls))
    if not todo:
        print("  every object that battles as one of the four already points at its own sheet")

    w = max(r.width for r in rows) * 4
    out = Image.new("RGB", (w, 32 * 4 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 4, 128), Image.NEAREST), (0, 128 * i))
    out.save(PREVIEW)
    print("  %d sheets -> preview %s (each: ours on grey, then the sheet it replaces)" % (len(built), PREVIEW))

    if WRITE:
        rules = 0
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
            rules += ensure_rule(filename)       # a sheet we ADD has no conversion rule until we write one
        register()
        changed = {}
        for mp, i, cls, _was in todo:
            if mp not in changed:
                raw = open(mp).read()
                changed[mp] = (json.loads(raw), raw.endswith("\n"))
            changed[mp][0]["object_events"][i]["graphics_id"] = "OBJ_EVENT_GFX_" + cls
        for mp, (m, nl) in changed.items():
            open(mp, "w").write(json.dumps(m, indent=2) + ("\n" if nl else ""))
        print("  written %d sheets (%d new conversion rules), registered, %d objects repointed across %d maps"
              % (len(built), rules, len(todo), len(changed)))


if __name__ == "__main__":
    main()

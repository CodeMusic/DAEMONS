#!/usr/bin/env python3
"""Each town's own people, in the town's own colour (T-119; vision.md 3.1, 9.4).

    python3 tools/gentowns.py            # preview to /tmp/towns_ow.png, and what would be repointed
    python3 tools/gentowns.py --write    # sheets, palettes, engine registration, and the maps

A town's generic citizens -- the youngster, the lass, the gentleman, the old woman, who were the same
people in every town -- become that town's locals: a child, an adult and an elder of a species that
belongs to the town's colour and theme. They are NEW object graphics, so nothing outside the town
changes, and each town's locals share ONE palette of the town's own, in PALSLOT_NPC_SPECIAL: the
slot the engine loads per object from its tag, as the Clears (0x111E) and the Owl (0x111F) do.

One special tag per map: where a town map also shows a special-slot character (CRYSTAL, AL, VERA,
the Owl), its citizens are left as they are and listed, rather than fight over the slot.

Institutions (T-118), trainers, gym interiors and named characters are not citizens and are untouched.
Every step of --write is idempotent: a town already registered is not registered twice.

A town builds only the roles its own maps put on screen: HALFTONE and BRAZEN have no elder citizen
anywhere, and UMBRA's plateau has three adults and nobody else, so those sheets are never drawn.

    CALLOW       green, unripe            a tree frog, a parakeet, an old iguana
    SLATE        stone; dead hardware     a pangolin, a rock hyrax docent, an old armadillo
    DOLDRUM      a becalmed sea           a seal pup, a sea otter, an old walrus
    ARDOR        flush and heat; the port a red panda, a gull dockhand, an old rooster
    HALFTONE     dots that look like grey a dalmatian, a zebra
    VERDIGRIS    green corrosion on bronze a gecko, a peafowl, an old heron
    LURID        garish glow; toxicity    a flamingo, a mandrill, an old cockatoo
    BRAZEN       brass over base metal    a lion cub, a golden retriever
    QUICKSILVER  mercury; the ruined lab  a ferret, a silver pheasant, an old grey cat
    UMBRA        full shadow              a black panther

One map, one special palette -- so a town map with a special-slot character on it cannot simply
take the town's locals: whoever spawned last would repaint the other. Two maps are like that, and
they are answered differently. On DOLDRUM's city map AL becomes a GUEST: redrawn against the sea
town's own sixteen, keeping the Clears' rust, orange and purple-grey in three letters no seal,
otter or walrus uses, and registered as a variant on the town's tag -- so the six citizens there
become locals and AL still walks in his own colours. On QUICKSILVER's island the SEAGALLOP cannot
be made to fit (ten colours, four of them nowhere near mercury, two letters free), so that map
keeps vanilla's people and revert_plan() puts back the two this tool took.
"""
import glob, json, os, re, subprocess, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import overlay, figure, check, sheet, ensure_rule, PEOPLE, GBA
from genleaders import H, S

PREVIEW = "/tmp/towns_ow.png"
WRITE = "--write" in sys.argv
PALS = os.path.join(GBA, "graphics/object_events/palettes")
KEY = (115, 197, 164)

# one letter scheme; each town's palette says what the letters are
LETTERS = {" ": 0, "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12, "m": 13, "W": 14, "K": 15}

CHILD = {"YOUNGSTER", "BOY", "LITTLE_BOY", "LITTLE_GIRL", "LASS", "BUG_CATCHER", "GBA_KID"}
ADULT = {"MAN", "WOMAN_1", "WOMAN_2", "WOMAN_3", "BALDING_MAN", "GENTLEMAN", "FAT_MAN", "WORKER_M", "WORKER_F", "BEAUTY", "COOLTRAINER_M",
         "COOLTRAINER_F", "ROCKER", "FISHER", "HIKER", "POKE_MANIAC", "SAILOR", "BLACK_BELT", "SWIMMER_M_LAND", "SWIMMER_F_LAND", "CAMPER",
         "PICNICKER", "CHEF", "SUPER_NERD", "TUBER_M_LAND", "TUBER_F_LAND"}
ELDER = {"OLD_MAN_1", "OLD_MAN_2", "OLD_WOMAN"}
def special_gfx():
    """every OBJ_EVENT_GFX_* the engine draws from PALSLOT_NPC_SPECIAL, our own town locals aside.

    There is ONE special slot and it is patched per object from that object's tag, so the last
    special sprite to spawn on a map sets the sixteen colours every special sprite on it draws
    from. Naming the four Clears by hand missed the SEAGALLOP -- which shares QUICKSILVER's island
    and is added by script mid-scene -- so this is READ FROM THE ENGINE rather than typed.
    """
    if not hasattr(special_gfx, "cache"):
        info = open(os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")).read()
        slots = {m.group(1) for m in re.finditer(
            r"const struct ObjectEventGraphicsInfo (gObjectEventGraphicsInfo_\w+) = \{(.*?)\n\};", info, re.S)
            if "PALSLOT_NPC_SPECIAL" in m.group(2)}
        ptr = open(os.path.join(GBA, "src/data/object_events/object_event_graphics_info_pointers.h")).read()
        # a guest's variant sits on the TOWN's tag, so it contends with nothing: it is ours, not foreign.
        # (Missing this made the second --write see AL_DOLDRUM holding the map and revert its citizens.)
        mine = {"OBJ_EVENT_GFX_" + x["const"] for x in GUESTS}
        special_gfx.cache = {g.strip() for g, gi in re.findall(
            r"\[(OBJ_EVENT_GFX_\w+)\s*\]\s*= &(gObjectEventGraphicsInfo_\w+),", ptr)
            if gi in slots and not g.strip().startswith("OBJ_EVENT_GFX_TOWN_") and g.strip() not in mine}
    return special_gfx.cache


def pad(rows, n=23):
    return rows + [""] * (n - len(rows))


# ================================================================== CALLOW: green, unripe
# a light green  b green  c dark green  d yellow  e gold  f sky  g blue  h cream  i tan  j brown  k red  l grey-green  m dark grey-green
CALLOW_PAL = [(168, 224, 112), (88, 176, 64), (44, 106, 40), (240, 224, 96), (216, 160, 48), (112, 176, 232), (56, 104, 184),
              (244, 236, 200), (200, 168, 120), (128, 88, 56), (216, 72, 48), (140, 156, 120), (76, 88, 64)]
FROG_FRONT = H(pad(["", "", "  KK", " KkKKKKK", " KkkKbbb", " Kbbbbba", " Kbbbbbb", "  KbKKKK", "   KKbbb", "   Kffff",
                    "  Kbffff", " Kbbffff", " KbKffff", "  KKdddd", "   Kdddd", "   KddKd", "   KbbK", "   KbbK", "  KabbK", "  KKKKK"]))
FROG_BACK = H(pad(["", "", "  KK", " KbKbKKK", " Kbbbbbb", " Kbbbbba", " Kbbbbbb", "  Kbbbbb", "   KKbbb", "   Kffff",
                   "  Kbffff", " Kbbffff", " KbKffff", "  KKdddd", "   Kdddd", "   KddKd", "   KbbK", "   KbbK", "  KabbK", "  KKKKK"]))
FROG_SIDE = S(pad(["", "", "     KKK", "    KkKbKK", "    KkkbbbK", "  KKbbbbbbK", " KbbbbbbbK", " KKKKbbbbK", "    KKbbK",
                   "     KffK", "    KbfffK", "    KbfffK", "    KKfffK", "     KdddK", "     KdddK", "     KddK", "     KbbK",
                   "     KbbK", "    KabbbK", "    KKKKKK"]))

PARAKEET_FRONT = H(pad(["", "    KKKK", "   Kdddd", "  Kddddd", "  KdKddd", "  Kgdddm", "  Kdddmm", "   KKbbb", "   Khhbb",
                        "  Kbhhhh", " Kbbhhhh", " Kbbhhhh", " KbKhhhh", "  KKiiii", "   Kiiii", "   KiiKi", "   KiiK", "   KiiK",
                        "    KlK", "   KllK"]))
PARAKEET_BACK = H(pad(["", "    KKKK", "   Kdddd", "  Kddddd", "  Kbdddd", "  Kbbddd", "  Kbbbdd", "   KKbbb", "   Kbbbb",
                       "  Kbbbbb", " Kbbhhhh", " Kbbhhhh", " KbKhhhh", "  KKiiii", "   Kiiii", "   KiiKi", "   KiiK", "   KiiK",
                       "    KlK", "   KllK"]))
PARAKEET_BACK = overlay(PARAKEET_BACK, 14, ["KbbK", "KcbK", "KbcK", "KbbK", " KK "], 6)          # the long tail
PARAKEET_SIDE = S(pad(["", "     KKKK", "    KddddK", "   KdKddddK", " KmmgdddddK", "  KmdddddK", "   KKddddK", "     KbbK",
                       "    KhhbbK", "    KhhhbK", "   KbhhhbK", "   KbhhhhKK", "   KKhhhhKbK", "    KiiiiKbK", "    KiiiiKcK",
                       "    KiiiK KbK", "    KiiiK  KK", "    KiiK", "     KlK", "    KllK"]))

IGUANA_FRONT = H(pad(["", "", "    KKKK", "   Kllll", "  KlKlll", "  Klllll", "  Kmllll", "   Kllee", "    KKee", "   Kiiii",
                      "  Kliiii", " Klliihh", " KlKiihh", "  KKiiii", "   Kjjjj", "   Kjjjj", "   KjjKj", "   KjjK", "   KjjK",
                      "  KlllK", "  KKKKK"]))
IGUANA_FRONT = overlay(IGUANA_FRONT, 12, ["KK", "jK", "jK", "jK", "jK", "jK", "jK", "jK", "KK"], 12)    # a walking cane
IGUANA_FRONT = overlay(IGUANA_FRONT, 13, ["K", "KlK", " KlK", "  KlK", "  KlK", "   K"], 0)          # the long tail
IGUANA_BACK = H(pad(["", "", "    KKKK", "   Klllc", "  Kllllc", "  Kllllc", "  Kmlllc", "   Kllll", "    KKll", "   Kiiii",
                     "  Kliiii", " Kllliii", " KlKiiii", "  KKiiii", "   Kjjjj", "   Kjjjj", "   KjjKj", "   KjjK", "   KjjK",
                     "  KlllK", "  KKKKK"]))
IGUANA_BACK = overlay(IGUANA_BACK, 14, ["KllK", "KlmK", " KlK", " KlK", "  KK"], 6)
IGUANA_SIDE = S(pad(["", "", "     KKKK", "    KlllcK", "   KlKlllcK", " KlllllllcK", " KmmmllllK", "   KeellK", "    KeKK",
                     "    KiiiK", "   KliiiK", "   KlhiiK", "   KKhiiiK", "    KiiiiKK", "    KjjjjKlK", "    KjjjjK KlK",
                     "    KjjjK   KK", "    KjjjK", "    KjjK", "   KllllK", "   KKKKKK"]))

# ================================================================== SLATE: stone, a writing surface; the museum of dead hardware
# a light stone  b stone  c dark stone  d tan  e brown  f dark brown  g slate light  h slate  i slate dark  j pink-grey  k rust  l chalk  m moss
SLATE_PAL = [(200, 192, 176), (160, 152, 136), (108, 100, 88), (208, 168, 120), (156, 108, 68), (92, 60, 36), (152, 168, 184),
             (104, 120, 136), (64, 76, 88), (200, 160, 160), (176, 88, 56), (232, 228, 216), (124, 136, 88)]
PANGOLIN_FRONT = H(pad(["", "", "    KKKK", "   Kefef", "  Kefefe", "  Kddddd", "  KdKddd", "   Kdddd", "    KKdd", "   Kgggg",
                        "  Kegggg", " Kefgggg", " KdKgggg", "  KKhhhh", "   Khhhh", "   KhhKh", "   KeeK", "   KeeK", "  KdeeK",
                        "  KKKKK"]))
PANGOLIN_BACK = H(pad(["", "", "    KKKK", "   Kefef", "  Kefefe", "  Kfefef", "  Kefefe", "   Kfefe", "    KKef", "   Kefef",
                       "  Kefefe", " Kefefef", " KdKefef", "  KKhhhh", "   Khhhh", "   KhhKh", "   KeeK", "   KeeK", "  KdeeK",
                       "  KKKKK"]))
PANGOLIN_BACK = overlay(PANGOLIN_BACK, 13, ["KefK", "KfeK", "KefK", " KK "], 6)                    # the scaled tail
PANGOLIN_SIDE = S(pad(["", "", "     KKKK", "    KefefK", "   KdKefefK", " KddddefefK", "  KKddddeK", "     KKddK", "     KgggK",
                       "    KegggK", "    KdgggK", "    KKgggKK", "     KhhhKeK", "     KhhhKfeK", "     KhhK KeK", "     KeeK  K",
                       "     KeeK", "    KdeeK", "    KKKKK"]))

HYRAX_FRONT = H(pad(["", "", "   KK", "  KbKKKK", "  Kbbbbb", "  KbKbbb", "  Kbbbaa", "   Kbaaa", "    KKaK", "   Kiill",
                     "  Kbiill", " Kbbiill", " KbKiiil", "  KKiiii", "   Khhhh", "   Khhhh", "   KhhKh", "   KhhK", "   KhhK",
                     "  KfffK", "  KKKKK"]))
HYRAX_BACK = H(pad(["", "", "   KK", "  KbKKKK", "  Kbbbbb", "  Kbbbbb", "  Kbbbbb", "   Kbbbb", "    KKbb", "   Kiiii",
                    "  Kbiiii", " Kbbiiii", " KbKiiii", "  KKiiii", "   Khhhh", "   Khhhh", "   KhhKh", "   KhhK", "   KhhK",
                    "  KfffK", "  KKKKK"]))
HYRAX_SIDE = S(pad(["", "", "      KK", "     KbKKK", "    KbbbbbK", "  KKbKbbbbK", " KaabbbbbbK", "  KKaaabbK", "     KKbK",
                    "     KlliK", "    KbliiK", "    KbliiK", "    KKiiiK", "     KiiiK", "     KhhhK", "     KhhhK", "     KhhK",
                    "     KhhK", "     KhhK", "    KffffK", "    KKKKKK"]))

ARMADILLO_FRONT = H(pad(["", "", "   KK", "  KjKKKK", "  Kjjjjj", "  KjKjjj", "  Kjjjjj", "   Kjjjj", "    KKjj", "   Kllll",
                         "  Kjaaaa", " Kjjaaaa", " KjKaaaa", "  KKaaaa", "   Kcccc", "   Kcccc", "   KccKc", "   KccK", "   KccK",
                         "  KjjjK", "  KKKKK"]))
ARMADILLO_FRONT = overlay(ARMADILLO_FRONT, 12, ["KK", "fK", "fK", "fK", "fK", "fK", "fK", "KK"], 12)    # a cane
ARMADILLO_BACK = H(pad(["", "", "   KK", "  KjKKKK", "  Kjjjjj", "  Kjjjjj", "  Kjjjjj", "   Kjjjj", "    KKjj", "   Kllll",
                        "  Kcjcjc", " Kjcjcjc", " KjKjcjc", "  KKcjcj", "   Kcccc", "   Kcccc", "   KccKc", "   KccK", "   KccK",
                        "  KjjjK", "  KKKKK"]))
ARMADILLO_SIDE = S(pad(["", "", "      KK", "     KjKKK", "    KjjjjjK", "  KKjKjjjjK", " KjjjjjjjK", "  KKKjjjK", "     KllK",
                        "    KjcjcK", "    KacjcK", "   KjKjcjcK", "    KacjcjK", "    KKcjcK", "     KcccK", "     KcccK",
                        "     KccK", "     KccK", "     KccK", "    KjjjjK", "    KKKKKK"]))

stone = lambda rows: [r.replace("j", "b") for r in rows]      # stone grey, not pink: pink with ears read as a pig
ARMADILLO_FRONT, ARMADILLO_BACK, ARMADILLO_SIDE = stone(ARMADILLO_FRONT), stone(ARMADILLO_BACK), stone(ARMADILLO_SIDE)

# ================================================================== DOLDRUM: a becalmed sea, low spirits
# a pale sea  b sea blue  c navy  d seal grey  e grey  f otter brown  g dark brown  h walrus tan  i ivory  j sand  k buoy red  l lilac  m dark slate
DOLDRUM_PAL = [(184, 216, 232), (104, 152, 192), (48, 72, 104), (160, 168, 176), (108, 116, 128), (140, 100, 72), (84, 64, 44),
               (200, 156, 120), (240, 232, 208), (216, 200, 160), (200, 80, 64), (168, 152, 184), (60, 68, 80)]
SEAL_FRONT = H(pad(["", "", "    KKKK", "   Kdddd", "  Kddddd", "  KdKddd", "  Kdddii", "   Kdiii", "    KKiK", "   Kabab",
                    "  Kdbaba", " Kddabab", " KdKbaba", "  KKcccc", "   Kcccc", "   KccKc", "   KddK", "  KdddK", "  KKKKK"]))
SEAL_BACK = H(pad(["", "", "    KKKK", "   Kdddd", "  Kddddd", "  Kddddd", "  Kddddd", "   Kdddd", "    KKdd", "   Kbaba",
                   "  Kdabab", " Kddbaba", " KdKabab", "  KKcccc", "   Kcccc", "   KccKc", "   KddK", "  KdddK", "  KKKKK"]))
SEAL_SIDE = S(pad(["", "", "     KKKK", "    KddddK", "   KdKddddK", " KiiddddddK", "  KKiiiddK", "     KKddK", "     KbabK",
                   "    KdababK", "    KdbabaK", "    KKababK", "     KccccK", "     KccccK", "     KcccK", "     KddK", "    KdddK",
                   "    KKKKK"]))

OTTER_FRONT = H(pad(["", "", "   KKKK", "  Kfffff", "  KfKfff", "  Kfffff", "  Kffjjj", "   Kfjjj", "    KKjK", "   Kllll",
                     "  Kfllll", " Kffllll", " KfKllll", "  KKbbbb", "   Kbbbb", "   Kbbbb", "   KbbKb", "   KbbK", "   KbbK",
                     "  KgggK", "  KKKKK"]))
OTTER_BACK = H(pad(["", "", "   KKKK", "  Kfffff", "  Kfffff", "  Kfffff", "  Kfffff", "   Kffff", "    KKff", "   Kllll",
                    "  Kfllll", " Kffllll", " KfKllll", "  KKbbbb", "   Kbbbb", "   Kbbbb", "   KbbKb", "   KbbK", "   KbbK",
                    "  KgggK", "  KKKKK"]))
OTTER_BACK = overlay(OTTER_BACK, 13, ["KffK", "KfgK", "KffK", "KfgK", " KK "], 6)                 # the thick tail
OTTER_SIDE = S(pad(["", "", "     KKKK", "    KffffK", "   KjKfffK", " KKjjjfffK", "  KjjjffK", "   KKKffK", "     KllK",
                    "    KfllllK", "    KflllK", "    KKlllKKK", "     KbbbKffK", "     KbbbKfgK", "     KbbbK KK", "     KbbK",
                    "     KbbK", "     KbbK", "    KggggK", "    KKKKKK"]))

WALRUS_FRONT = H(pad(["", "", "    KKKK", "  KKhhhh", " Khhhhhh", " KhhKhhh", " Khjjjjj", " Kjjjjjj", "  KiKKKK", "  KiKkkk",
                      "  Khcccc", " Khhcccc", " Khhcccc", " KhKcccc", "  KKcccc", "   Kcccc", "   KccKc", "   KccK", "   KccK",
                      "  KhhhK", "  KKKKK"]))
WALRUS_BACK = H(pad(["", "", "    KKKK", "   Khhhh", "  Khhhhh", "  Khhhhh", "  Khhhhh", "  Khhhhh", "   KKhhh", "   Kkkkk",
                     "  Khcccc", " Khhcccc", " Khhcccc", " KhKcccc", "  KKcccc", "   Kcccc", "   KccKc", "   KccK", "   KccK",
                     "  KhhhK", "  KKKKK"]))
WALRUS_SIDE = S(pad(["", "", "     KKKK", "    KhhhhK", "   KhKhhhhK", " KjjjhhhhhK", " KjjjjhhhK", "  KKiKKhhK", "    KiKkkK",
                     "    KhhcccK", "   KhhccccK", "   KhKccccK", "    KKccccK", "     KccccK", "     KccccK", "     KcccK",
                     "     KcccK", "     KccK", "    KhhhhK", "    KKKKKK"]))

# ================================================================== the seven towns after the pilot
# Two heads carry them all, as the pilot's hand-drawn nine settled the idiom: a MAMMAL head (a small
# ear, a muzzle) and a BIRD head (a crown, a beak at the centre), on one torso. What separates a
# dalmatian from a zebra is the marks put into the half-rows before they are mirrored -- spots, a
# mane, a mask, a blue ridge -- and the tails and canes overlaid after. The species is still the
# ROLE (9.4): the town's child, its working adult, its elder.

def put(rows, r, c, ch):
    """set pixels in a row before it is mirrored or padded: a marking

    This clipped to EIGHT, because it was written for the half rows a front view mirrors -- but it
    is called on SIDE rows too, which run to eleven, and it was silently cutting the back off every
    side head it touched. Clip nothing: H() still trims a half to eight, S() still pads a side to
    sixteen, and check() catches anything wider.
    """
    rows = list(rows)
    row = rows[r].ljust(max(8, len(rows[r])))
    rows[r] = row[:c] + ch + row[c + len(ch):]
    return rows


def mammal(fur, ear, muzzle):
    front = ["", "", "   KK", "  K" + ear + "KKKK", "  K" + fur * 5, "  K" + fur + "K" + fur * 3,
             "  K" + fur * 3 + muzzle * 2, "   K" + fur + muzzle * 3, "    KK" + muzzle + "K"]
    back = ["", "", "   KK", "  K" + ear + "KKKK", "  K" + fur * 5, "  K" + fur * 5, "  K" + fur * 5,
            "   K" + fur * 4, "    KK" + fur * 2]
    side = ["", "", "      KK", "     K" + ear + "KKK", "    K" + fur * 5 + "K", "  KK" + fur + "K" + fur * 4 + "K",
            " K" + muzzle * 2 + fur * 6 + "K", "  KK" + muzzle * 3 + fur * 2 + "K", "     KK" + fur + "K"]
    return front, back, side


def bird(feather, cheek, beak, neck=None):
    n = neck or feather
    front = ["", "    KKKK", "   K" + feather * 4, "  K" + feather * 5, "  K" + feather + "K" + feather * 3,
             "  K" + cheek + feather * 3 + beak, "  K" + feather * 3 + beak * 2, "   KK" + n * 3, "    KK" + n * 2]
    back = ["", "    KKKK", "   K" + feather * 4, "  K" + feather * 5, "  K" + feather * 5, "  K" + feather * 5,
            "  K" + feather * 5, "   KK" + n * 3, "    KK" + n * 2]
    side = ["", "     KKKK", "    K" + feather * 4 + "K", "   K" + feather + "K" + feather * 4 + "K",
            " K" + beak * 2 + cheek + feather * 5 + "K", "  K" + beak + feather * 5 + "K", "   KK" + feather * 4 + "K",
            "     K" + n * 2 + "K", "     K" + n * 2 + "K"]
    return front, back, side


def fig(head, arm, shirt, pants, leg, foot):
    """a head (9 rows) on the one torso (11): shirt and trousers may be a letter or four"""
    s4, p4 = (shirt * 4)[:4] if len(shirt) == 1 else shirt, (pants * 4)[:4] if len(pants) == 1 else pants
    body = ["   K" + s4, "  K" + arm + s4, " K" + arm * 2 + s4, " K" + arm + "K" + s4,
            "  KK" + p4, "   K" + p4, "   K" + p4[:2] + "K" + p4[3],
            "   K" + leg * 2 + "K", "   K" + leg * 2 + "K", "  K" + foot + leg * 2 + "K", "  KKKKK"]
    side = ["     K" + s4[:2] + "K", "    K" + arm + s4[:3] + "K", "    K" + arm + s4[:3] + "K", "    KK" + s4[:3] + "K",
            "     K" + p4[:3] + "K", "     K" + p4[:3] + "K", "     K" + p4[:2] + "K",
            "     K" + leg * 2 + "K", "     K" + leg * 2 + "K", "    K" + foot + leg * 3 + "K", "    KKKKKK"]
    hf, hb, hs = head
    return H(pad(list(hf) + body)), H(pad(list(hb) + body)), S(pad(list(hs) + side))


TAIL, CANE = 13, 12          # the rows a tail hangs from behind, and where a cane starts, at the hand
CANE_X = 14                  # and the column it stands in: col 12 is the trousers' own outline, and a
                             # cane drawn there reads as a stripe painted down the leg

# ------------------------------------------------------ ARDOR: flush and heat, brash zeal; the port
# a light rust  b rust  c deep red  d cream  e sand  f charcoal  g harbour blue  h pale blue
# i white-grey  j gull grey  k comb red  l gold  m brown
ARDOR_PAL = [(232, 160, 112), (200, 96, 56), (140, 48, 40), (244, 232, 208), (216, 184, 136), (72, 64, 64),
             (72, 120, 168), (152, 192, 224), (232, 232, 232), (176, 176, 184), (216, 56, 48), (240, 192, 72), (120, 76, 48)]
# A red panda is the one species here that can read as a FOX, and foxes are the Clears' alone (9.4).
# So it is drawn the way a red panda is not a fox: a CREAM face under a rust crown, a rust tear stripe
# below the eye, cream-fringed round ears, black legs and underparts, and a thick ringed tail.
PANDA = (["", "", "  KK", "  KdKKKK", "  Kbbbbb", "  KdKddd", "  Kbdddd", "   Kdddd", "    KKfK"],
         ["", "", "  KK", "  KdKKKK", "  Kbbbbb", "  Kbbbbb", "  Kbbbbb", "   Kbbbb", "    KKbb"],
         ["", "", "      KK", "     KdKKK", "    KbbbbbK", "  KKdKdbbbK", " KddddddbK", "  KKdddbbK", "     KKbK"])
PANDA_F, PANDA_B, PANDA_S = fig(PANDA, "f", "g", "f", "f", "c")
PANDA_B = overlay(PANDA_B, TAIL, ["KbbK", "KddK", "KbbK", "KddK", " KK "], 6)
PANDA_S = overlay(PANDA_S, TAIL, ["KbbK", "KddK", "KbbK", " KK "], 10)

GULL_F, GULL_B, GULL_S = fig(bird("i", "j", "l"), "j", "g", "g", "l", "l")    # a gull dockhand in overalls

_h = bird("d", "k", "l")                                     # an old rooster: comb, wattle, a cane
ROOSTER_F, ROOSTER_B, ROOSTER_S = fig((put(_h[0], 7, 7, "k"), _h[1], put(_h[2], 6, 8, "k")), "d", "m", "e", "l", "l")
ROOSTER_F = overlay(ROOSTER_F, 0, ["KkkkkK"], 5)
ROOSTER_B = overlay(ROOSTER_B, 0, ["KkkkkK"], 5)
ROOSTER_S = overlay(ROOSTER_S, 0, ["KkkkK"], 5)
ROOSTER_F = overlay(ROOSTER_F, CANE, ["KK", "mK", "mK", "mK", "mK", "mK", "mK", "KK"], CANE_X)

# ------------------------------------------------------ HALFTONE: dots that only look like grey; the tower
# a white  b light grey  c mid grey  d dark grey  e black  f lavender  g dusty rose  h pale gold
# i brown  j sky  k ink  l cream  m moss
HALFTONE_PAL = [(240, 240, 240), (200, 200, 204), (152, 152, 160), (96, 96, 104), (40, 40, 48), (176, 160, 200),
                (192, 144, 152), (216, 192, 120), (128, 96, 64), (160, 184, 216), (64, 72, 88), (232, 224, 200), (120, 136, 104)]
_h = mammal("a", "e", "a")                                   # a dalmatian: the dots are the town itself
_h = (put(put(put(put(_h[0], 4, 3, "e"), 4, 6, "e"), 6, 3, "e"), 7, 7, "e"),
      put(put(put(put(_h[1], 4, 4, "e"), 5, 6, "e"), 6, 3, "e"), 7, 5, "e"),
      put(put(put(_h[2], 4, 5, "e"), 5, 8, "e"), 6, 4, "e"))
DALMATIAN_F, DALMATIAN_B, DALMATIAN_S = fig(_h, "a", "g", "j", "a", "d")

_h = mammal("a", "e", "d")                                   # a zebra: stripes over the crown, a brush mane
_h = (put(put(put(_h[0], 4, 3, "e"), 4, 5, "e"), 4, 7, "e"),
      put(put(put(put(put(_h[1], 4, 3, "e"), 4, 5, "e"), 5, 7, "e"), 6, 7, "e"), 7, 7, "e"),
      put(put(_h[2], 4, 5, "e"), 4, 7, "e"))
ZEBRA_F, ZEBRA_B, ZEBRA_S = fig(_h, "a", "f", "k", "a", "e")
ZEBRA_F = overlay(ZEBRA_F, 2, ["KeeK"], 6)
ZEBRA_B = overlay(ZEBRA_B, 2, ["KeeK"], 6)
ZEBRA_S = overlay(ZEBRA_S, 2, ["KeeK"], 6)

# ------------------------------------------------------ VERDIGRIS: green corrosion on bronze
# a pale verdigris  b verdigris  c deep teal  d bronze  e dark bronze  f gold  g leaf green  h cream
# i blue  j slate  k plum  l pale grey  m charcoal
VERDIGRIS_PAL = [(168, 216, 200), (88, 176, 152), (32, 96, 88), (176, 136, 72), (112, 80, 40), (232, 200, 104),
                 (96, 160, 72), (240, 236, 216), (72, 112, 168), (104, 112, 120), (144, 72, 112), (196, 200, 196), (56, 60, 64)]
_h = mammal("g", "g", "a")                                   # a gecko: a ridge rather than an ear
_h = (put(_h[0], 5, 3, "b"), put(_h[1], 5, 5, "b"), put(_h[2], 4, 6, "b"))
GECKO_F, GECKO_B, GECKO_S = fig(_h, "g", "f", "d", "g", "e")
GECKO_B = overlay(GECKO_B, TAIL, ["KggK", "KgbK", " KgK", " KgK", "  KK"], 6)
GECKO_S = overlay(GECKO_S, TAIL, ["KggK", " KgK", "  KgK", "   K"], 10)

PEAFOWL_F, PEAFOWL_B, PEAFOWL_S = fig(bird("b", "c", "f"), "c", "c", "d", "e", "e")     # a peafowl, the train behind
PEAFOWL_F = overlay(PEAFOWL_F, 0, ["KffK"], 6)
PEAFOWL_B = overlay(PEAFOWL_B, 0, ["KffK"], 6)
PEAFOWL_B = overlay(PEAFOWL_B, TAIL, ["KcfcK", "KfcfK", "KcfcK", "KfcfK", " KKK "], 5)
PEAFOWL_S = overlay(PEAFOWL_S, 0, ["KffK"], 5)
PEAFOWL_S = overlay(PEAFOWL_S, TAIL, ["KcfK", "KfcK", "KcfK", " KK "], 10)

_h = bird("l", "m", "f")                                     # an old heron, on bronze legs and a cane
HERON_F, HERON_B, HERON_S = fig((put(_h[0], 3, 3, "m"), _h[1], put(_h[2], 3, 5, "m")), "l", "h", "j", "d", "d")
HERON_F = overlay(HERON_F, CANE, ["KK", "eK", "eK", "eK", "eK", "eK", "eK", "KK"], CANE_X)

# ------------------------------------------------------ LURID: garish glow; spectacle and toxicity
# a hot pink  b magenta  c deep purple  d acid green  e green  f yellow  g orange  h white
# i cyan  j teal  k charcoal  l tan  m blue-violet
LURID_PAL = [(248, 120, 176), (200, 48, 128), (96, 32, 88), (168, 232, 80), (96, 184, 64), (248, 224, 88),
             (248, 152, 56), (248, 240, 240), (96, 216, 232), (40, 136, 152), (56, 48, 56), (216, 168, 128), (120, 96, 200)]
_h = bird("a", "b", "g")                                     # a flamingo: a dark-tipped beak
FLAMINGO_F, FLAMINGO_B, FLAMINGO_S = fig((put(_h[0], 6, 7, "k"), _h[1], put(_h[2], 5, 3, "k")), "b", "i", "m", "a", "g")

_h = mammal("l", "k", "h")                                   # a mandrill: the blue ridges, the red nose
_h = (put(put(put(_h[0], 5, 6, "i"), 6, 5, "i"), 7, 5, "b"),
      put(_h[1], 5, 5, "k"), put(put(_h[2], 5, 8, "i"), 6, 3, "b"))
MANDRILL_F, MANDRILL_B, MANDRILL_S = fig(_h, "l", "c", "k", "l", "k")

COCKATOO_F, COCKATOO_B, COCKATOO_S = fig(bird("h", "f", "k"), "h", "m", "c", "l", "l")   # an old cockatoo, crest up
COCKATOO_F = overlay(COCKATOO_F, 0, ["KffK"], 6)
COCKATOO_B = overlay(COCKATOO_B, 0, ["KffK"], 6)
COCKATOO_S = overlay(COCKATOO_S, 0, ["KffK"], 5)
COCKATOO_F = overlay(COCKATOO_F, CANE, ["KK", "kK", "kK", "kK", "kK", "kK", "kK", "KK"], CANE_X)

# ------------------------------------------------------ BRAZEN: brass over base metal; corporate capture
# a pale brass  b brass  c dark brass  d steel  e dark steel  f navy  g cream  h tan
# i brown  j gold  k maroon  l white  m black
BRAZEN_PAL = [(232, 208, 136), (200, 160, 64), (136, 100, 32), (152, 160, 168), (88, 96, 104), (240, 232, 208),
              (208, 168, 112), (128, 88, 48), (248, 224, 120), (136, 48, 48), (244, 244, 244), (40, 40, 44), (176, 132, 76)]
_h = mammal("h", "c", "a")                                   # a lion cub: the mane just coming in
_h = (put(put(put(put(_h[0], 4, 3, "i"), 5, 3, "i"), 6, 3, "i"), 7, 4, "i"),
      put(put(put(_h[1], 4, 3, "i"), 5, 3, "i"), 6, 3, "i"), put(put(_h[2], 4, 4, "i"), 5, 4, "i"))
LION_F, LION_B, LION_S = fig(_h, "h", "e", "d", "h", "i")
LION_F = overlay(LION_F, 3, ["KiiiiK"], 5)
LION_B = overlay(LION_B, 3, ["KiiiiK"], 5)
LION_S = overlay(LION_S, 3, ["KiiiK"], 5)
LION_B = overlay(LION_B, TAIL, ["KhK", "KhK", "KiK", " KK"], 7)

RETRIEVER_F, RETRIEVER_B, RETRIEVER_S = fig(mammal("b", "c", "a"), "b", "d", "e", "b", "m")   # the ears fall; a suit
for _l in (1, 11):                                           # the ears fall against the head, not beside it
    RETRIEVER_F = overlay(RETRIEVER_F, 5, ["KccK", "KccK", "KccK", " KK "], _l)
    RETRIEVER_B = overlay(RETRIEVER_B, 5, ["KccK", "KccK", "KccK", " KK "], _l)
RETRIEVER_S = overlay(RETRIEVER_S, 5, ["KccK", "KccK", "KccK", " KK "], 2)
RETRIEVER_F = overlay(RETRIEVER_F, 9, ["ll", "jj", "jj", "jj"], 7)       # a white collar and a gold tie

# ------------------------------------------------------ QUICKSILVER: mercury, alive and unstable; the ruined lab
# a bright silver  b silver  c grey  d dark grey  e mercury blue  f deep blue  g white  h cream
# i tan  j brown  k copper  l lab teal  m black
QUICKSILVER_PAL = [(232, 236, 240), (184, 192, 200), (128, 136, 148), (72, 80, 92), (136, 184, 216), (56, 88, 136),
                   (248, 248, 248), (232, 224, 200), (200, 168, 128), (120, 88, 56), (200, 132, 80), (96, 168, 168), (32, 36, 44)]
_h = mammal("h", "c", "g")                                   # a ferret: the mask, and the long tail
_h = (put(put(_h[0], 5, 3, "d"), 5, 5, "d"), _h[1], put(_h[2], 5, 6, "d"))
FERRET_F, FERRET_B, FERRET_S = fig(_h, "h", "l", "d", "h", "j")
FERRET_B = overlay(FERRET_B, TAIL, ["KiiK", "KijK", "KiiK", " KK "], 6)
FERRET_S = overlay(FERRET_S, TAIL, ["KiiK", "KijK", " KK "], 10)

_h = bird("a", "k", "k", "b")                                # a silver pheasant: black crest and tail
PHEASANT_F, PHEASANT_B, PHEASANT_S = fig(_h, "b", "f", "d", "k", "k")
PHEASANT_F = overlay(PHEASANT_F, 0, ["KmmK"], 6)
PHEASANT_B = overlay(PHEASANT_B, 0, ["KmmK"], 6)
PHEASANT_B = overlay(PHEASANT_B, TAIL, ["KmmK", "KmbK", "KmmK", "KmbK", " KK "], 6)
PHEASANT_S = overlay(PHEASANT_S, 0, ["KmmK"], 5)
PHEASANT_S = overlay(PHEASANT_S, TAIL, ["KmmK", "KmbK", "KmmK", " KK "], 10)

CAT_F, CAT_B, CAT_S = fig(mammal("c", "b", "g"), "c", "h", "d", "c", "m")    # an old grey cat, with a cane
CAT_B = overlay(CAT_B, TAIL, ["KcK", "KbK", "KcK", " KK"], 7)
CAT_F = overlay(CAT_F, CANE, ["KK", "jK", "jK", "jK", "jK", "jK", "jK", "KK"], CANE_X)

# ------------------------------------------------------ UMBRA: full shadow, all colour absorbed; the Review Board
# a near-black  b black  c charcoal  d dark blue-grey  e grey  f pale grey  g white  h gold
# i deep red  j purple  k green eye  l brown  m mid slate
UMBRA_PAL = [(48, 48, 56), (28, 28, 34), (72, 72, 84), (88, 92, 108), (128, 132, 144), (176, 180, 192),
             (232, 232, 240), (192, 160, 80), (120, 40, 48), (80, 56, 104), (120, 200, 120), (96, 72, 56), (104, 108, 124)]
_h = mammal("b", "a", "a")                                   # a black panther: only the eyes carry light
_h = (put(_h[0], 5, 4, "k"), _h[1], put(_h[2], 5, 5, "k"))
PANTHER_F, PANTHER_B, PANTHER_S = fig(_h, "b", "c", "a", "b", "c")
PANTHER_F = overlay(PANTHER_F, 9, ["hh"], 7)                 # one gold line at the collar
PANTHER_B = overlay(PANTHER_B, TAIL, ["KbbK", "KabK", "KbbK", " KK "], 6)
PANTHER_S = overlay(PANTHER_S, TAIL, ["KbbK", "KabK", " KK "], 10)

TOWNS = [   # vanilla map prefix, our name, palette tag, palette, {role: (front, back, side, species)}
    ("ViridianCity", "CALLOW", 0x1120, CALLOW_PAL, {
        "child": (FROG_FRONT, FROG_BACK, FROG_SIDE, "a tree frog"),
        "adult": (PARAKEET_FRONT, PARAKEET_BACK, PARAKEET_SIDE, "a parakeet"),
        "elder": (IGUANA_FRONT, IGUANA_BACK, IGUANA_SIDE, "an old iguana")}),
    ("PewterCity", "SLATE", 0x1121, SLATE_PAL, {
        "child": (PANGOLIN_FRONT, PANGOLIN_BACK, PANGOLIN_SIDE, "a pangolin"),
        "adult": (HYRAX_FRONT, HYRAX_BACK, HYRAX_SIDE, "a rock hyrax docent"),
        "elder": (ARMADILLO_FRONT, ARMADILLO_BACK, ARMADILLO_SIDE, "an old armadillo")}),
    ("CeruleanCity", "DOLDRUM", 0x1122, DOLDRUM_PAL, {
        "child": (SEAL_FRONT, SEAL_BACK, SEAL_SIDE, "a seal pup"),
        "adult": (OTTER_FRONT, OTTER_BACK, OTTER_SIDE, "a sea otter"),
        "elder": (WALRUS_FRONT, WALRUS_BACK, WALRUS_SIDE, "an old walrus")}),
    ("VermilionCity", "ARDOR", 0x1123, ARDOR_PAL, {
        "child": (PANDA_F, PANDA_B, PANDA_S, "a red panda"),
        "adult": (GULL_F, GULL_B, GULL_S, "a gull dockhand"),
        "elder": (ROOSTER_F, ROOSTER_B, ROOSTER_S, "an old rooster")}),
    ("LavenderTown", "HALFTONE", 0x1124, HALFTONE_PAL, {          # no elder: the tower's maps have none
        "child": (DALMATIAN_F, DALMATIAN_B, DALMATIAN_S, "a dalmatian"),
        "adult": (ZEBRA_F, ZEBRA_B, ZEBRA_S, "a zebra")}),
    ("CeladonCity", "VERDIGRIS", 0x1125, VERDIGRIS_PAL, {
        "child": (GECKO_F, GECKO_B, GECKO_S, "a gecko"),
        "adult": (PEAFOWL_F, PEAFOWL_B, PEAFOWL_S, "a peafowl"),
        "elder": (HERON_F, HERON_B, HERON_S, "an old heron")}),
    ("FuchsiaCity", "LURID", 0x1126, LURID_PAL, {
        "child": (FLAMINGO_F, FLAMINGO_B, FLAMINGO_S, "a flamingo"),
        "adult": (MANDRILL_F, MANDRILL_B, MANDRILL_S, "a mandrill"),
        "elder": (COCKATOO_F, COCKATOO_B, COCKATOO_S, "an old cockatoo")}),
    ("SaffronCity", "BRAZEN", 0x1127, BRAZEN_PAL, {               # no elder: SAFFRON's maps have none
        "child": (LION_F, LION_B, LION_S, "a lion cub"),
        "adult": (RETRIEVER_F, RETRIEVER_B, RETRIEVER_S, "a golden retriever")}),
    ("CinnabarIsland", "QUICKSILVER", 0x1128, QUICKSILVER_PAL, {
        "child": (FERRET_F, FERRET_B, FERRET_S, "a ferret"),
        "adult": (PHEASANT_F, PHEASANT_B, PHEASANT_S, "a silver pheasant"),
        "elder": (CAT_F, CAT_B, CAT_S, "an old grey cat")}),
    ("IndigoPlateau", "UMBRA", 0x1129, UMBRA_PAL, {               # the Review Board keeps three adults, no more
        "adult": (PANTHER_F, PANTHER_B, PANTHER_S, "a black panther")}),
]
ROLES = ("child", "adult", "elder")     # a town builds only the roles its own maps put on screen


def camel(s):
    return "".join(w.capitalize() for w in s.lower().split("_"))


def full_palette(colours):
    return [KEY] + list(colours) + [(255, 255, 255), (0, 0, 0)]


def plan_maps(prefix, name, roles=ROLES):
    """(map path, object index, role) for every citizen to repoint, and the maps left alone"""
    todo, left = [], []
    for mp in sorted(glob.glob(os.path.join(GBA, "data/maps/%s*/map.json" % prefix))):
        if mp.endswith("_Gym/map.json"):
            continue
        objs = json.load(open(mp)).get("object_events", [])
        held = [o.get("graphics_id") for o in objs if o.get("graphics_id") in special_gfx()]
        g = guest_of(name)
        if g and os.path.basename(os.path.dirname(mp)) == g["map"]:
            held = [h for h in held if h != g["source"]]      # the guest joins the town's palette
        special = bool(held)
        for i, o in enumerate(objs):
            g = o.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
            role = "child" if g in CHILD else "adult" if g in ADULT else "elder" if g in ELDER else None
            if role not in roles or o.get("trainer_type") not in (None, "TRAINER_TYPE_NONE", "0"):
                continue
            if special:
                left.append(os.path.basename(os.path.dirname(mp)))
                continue
            todo.append((mp, i, role))
    return todo, sorted(set(left))


# ---------------------------------------------------------------- a guest in the town's palette
# One map, one special palette. Where a special-slot character stands on a town map, the town's
# citizens cannot be repointed -- whoever spawns last would repaint the other. A GUEST is the way
# out: the character is redrawn against the town's own sixteen, keeping the colours that ARE its
# identity and collapsing the rest onto near neighbours the town already has, and is registered as
# a variant graphics id on the town's tag. Only that one map's object changes; the character is
# untouched everywhere else.
#
# AL on DOLDRUM's city map is the one that fits: the Clears' rust, orange and purple-grey go into
# 'e', 'm' and 'W', which no seal, otter or walrus draws with, and his browns, cream, lilac and
# pale blue land within 21-37 of colours the sea town already owns.
#
# QUICKSILVER's island is the one that DOES NOT: the SEAGALLOP needs ten colours, four of them
# (steel blue, indigo, magenta, a bright yellow) nowhere near a mercury palette with two letters
# free. That map keeps vanilla's citizens, and revert_plan() puts back the two this tool took.
GUESTS = [
    dict(town="DOLDRUM", map="CeruleanCity", source="OBJ_EVENT_GFX_BLUE", sheet="blue.png",
         palette="npc_clears.pal", const="AL_DOLDRUM", fname="al_doldrum", letters="emW", collapse=40.0),
]


def guest_of(town):
    for g in GUESTS:
        if g["town"] == town:
            return g
    return None


def used_letters(roles):
    """the palette letters a town's own sheets actually draw with"""
    u = set()
    for front, back, side, _ in roles.values():
        for rows in (front, back, side):
            for r in rows:
                u |= set(r)
    return u - {" "}


def merged_palette(name, colours, roles):
    """the town's sixteen, with a guest's own colours dropped into letters no local uses"""
    pal = full_palette(colours)
    g = guest_of(name)
    if not g:
        return pal, None
    lines = open(os.path.join(PALS, g["palette"])).read().replace("\r", "").split("\n")[3:19]
    src = [tuple(map(int, l.split())) for l in lines if l.strip()]
    im = Image.open(os.path.join(PEOPLE, g["sheet"]))
    free = [LETTERS[c] for c in g["letters"]]
    mine = {LETTERS[c] for c in used_letters(roles)}
    assert not (set(free) & mine), "%s: guest letters %r are drawn by the town's own sheets" % (name, g["letters"])
    dist = lambda a, b: sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
    remap, identity = {0: 0, 15: 15}, []
    for i in sorted(set(im.getdata())):
        if i in (0, 15):
            continue
        near = min((dist(src[i], pal[j]), j) for j in sorted(mine))
        if near[0] <= g["collapse"]:
            remap[i] = near[1]                       # near enough to a colour the town already has
        else:
            identity.append(i)                       # this one IS the character; it needs a letter
    assert len(identity) <= len(free), "%s: the guest needs %d colours of its own, %d letters free" % (
        name, len(identity), len(free))
    for i, slot in zip(identity, free):
        pal[slot] = src[i]
        remap[i] = slot
    return pal, remap


def guest_sheet(pal, remap, g):
    im = Image.open(os.path.join(PEOPLE, g["sheet"]))
    out = Image.new("P", im.size)
    flat = [c for rgb in pal for c in rgb]
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.putdata(bytes(remap[p] for p in im.getdata()))
    return out


def revert_plan():
    """a map a foreign special character holds cannot carry our locals: put its citizens back"""
    out = []
    for prefix, name, _tag, _colours, roles in TOWNS:
        g = guest_of(name)
        for mp in sorted(glob.glob(os.path.join(GBA, "data/maps/%s*/map.json" % prefix))):
            objs = json.load(open(mp)).get("object_events", [])
            held = [o.get("graphics_id") for o in objs if o.get("graphics_id") in special_gfx()]
            if g and os.path.basename(os.path.dirname(mp)) == g["map"]:
                held = [h for h in held if h != g["source"]]
            mine = [i for i, o in enumerate(objs) if o.get("graphics_id", "").startswith("OBJ_EVENT_GFX_TOWN_")]
            if not held or not mine:
                continue
            rel = os.path.relpath(mp, GBA)
            up = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel], capture_output=True, text=True).stdout
            upobjs = json.loads(up)["object_events"]
            assert len(upobjs) == len(objs), "%s: object count differs from upstream, cannot restore by index" % rel
            for i in mine:
                out.append((mp, i, upobjs[i]["graphics_id"], objs[i]["graphics_id"], ",".join(
                    h.replace("OBJ_EVENT_GFX_", "") for h in held)))
    return out


def register_one(edit, const, cname, fname, tag_name, note, frames=9):
    """one graphics id: the constant, the sheet, its frame table, its info and its pointer"""
    def constants(s):
        if ("#define %s " % const) in s:
            return s
        m = re.search(r"\n#define NUM_OBJ_EVENT_GFX\s+(\d+)\n", s); n = int(m.group(1))
        return s[:m.start()] + "\n#define %s %d" % (const, n) + "\n\n#define NUM_OBJ_EVENT_GFX     %d\n" % (n + 1) + s[m.end():]
    edit("include/constants/event_objects.h", constants)

    def graphics(s):
        if ("gObjectEventPic_%s[]" % cname) in s:
            return s
        anchor = 'const u16 gObjectEventPic_BenchmarkGuide[] = INCBIN_U16("graphics/object_events/pics/people/benchmark_guide.4bpp");\n'
        assert s.count(anchor) == 1
        return s.replace(anchor, anchor + 'const u16 gObjectEventPic_%s[] = INCBIN_U16("graphics/object_events/pics/people/%s.4bpp");\n' % (cname, fname))
    edit("src/data/object_events/object_event_graphics.h", graphics)

    def pictables(s):
        if ("sPicTable_%s[]" % cname) in s:
            return s
        start = s.index("static const struct SpriteFrameImage sPicTable_BenchmarkGuide[] = {")
        end = s.index("};\n", start) + 3
        block = "\nstatic const struct SpriteFrameImage sPicTable_%s[] = {\n%s};\n" % (cname, "".join(
            "    overworld_frame(gObjectEventPic_%s, 2, 4, %d),\n" % (cname, k) for k in range(frames)))
        return s[:end] + block + s[end:]
    edit("src/data/object_events/object_event_pic_tables.h", pictables)

    def info(s):
        if ("gObjectEventGraphicsInfo_%s =" % cname) in s:
            return s
        return s.rstrip("\n") + "\n\n// %s\n" % note + (
            "const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = {\n    .tileTag = TAG_NONE,\n    .paletteTag = %s,\n"
            "    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,\n    .size = 256,\n    .width = 16,\n    .height = 32,\n    .paletteSlot = PALSLOT_NPC_SPECIAL,\n"
            "    .shadowSize = SHADOW_SIZE_M,\n    .inanimate = FALSE,\n    .disableReflectionPaletteLoad = FALSE,\n    .tracks = TRACKS_FOOT,\n"
            "    .oam = &gObjectEventBaseOam_16x32,\n    .subspriteTables = gObjectEventSpriteOamTables_16x32,\n    .anims = sAnimTable_Standard,\n"
            "    .images = sPicTable_%s,\n    .affineAnims = gDummySpriteAffineAnimTable,\n};\n") % (cname, tag_name, cname)
    edit("src/data/object_events/object_event_graphics_info.h", info)

    def pointers(s):
        if ("&gObjectEventGraphicsInfo_%s," % cname) in s:
            return s
        decl = "const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_BenchmarkGuide;\n"
        entry_re = re.search(r"    \[OBJ_EVENT_GFX_BENCHMARK_GUIDE\s*\]\s*= &gObjectEventGraphicsInfo_BenchmarkGuide,\n", s)
        assert s.count(decl) == 1 and entry_re
        last = max(m.end() for m in re.finditer(r"    \[OBJ_EVENT_GFX_\w+\s*\]\s*= &gObjectEventGraphicsInfo_\w+,\n", s))
        s = s[:last] + "    [%s]%s = &gObjectEventGraphicsInfo_%s,\n" % (const, " " * max(1, 40 - len(const)), cname) + s[last:]
        return s.replace(decl, decl + "const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s;\n" % cname, 1)
    edit("src/data/object_events/object_event_graphics_info_pointers.h", pointers)


def register():
    def edit(path, fn):
        p = os.path.join(GBA, path); s = open(p).read(); s2 = fn(s)
        if s2 != s:
            open(p, "w").write(s2)

    for prefix, name, tag, colours, roles in TOWNS:
        pal_name = "npc_town_%s" % name.lower()
        tag_name = "OBJ_EVENT_PAL_TAG_NPC_TOWN_%s" % name
        pal, _remap = merged_palette(name, colours, roles)
        with open(os.path.join(PALS, pal_name + ".pal"), "w") as f:
            f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal))

        def movement(s):
            if tag_name not in s:
                assert ("0x%04X" % tag) not in s.upper().replace("0X", "0x"), "palette tag 0x%X already in use" % tag
                owl = "#define OBJ_EVENT_PAL_TAG_NPC_OWL                     0x111F\n"
                assert s.count(owl) == 1
                s = s.replace(owl, owl + "//  %s's locals share one palette of the town's own (T-119).\n#define %-45s 0x%04X\n" % (name, tag_name, tag))
                entry = "    {gObjectEventPal_NpcOwl,                  OBJ_EVENT_PAL_TAG_NPC_OWL},\n"
                assert s.count(entry) == 1
                s = s.replace(entry, entry + "    {gObjectEventPal_NpcTown%-18s %s},\n" % (camel(name) + ",", tag_name))
            return s
        edit("src/event_object_movement.c", movement)

        def graphics_pal(s):
            if ("gObjectEventPal_NpcTown%s[]" % camel(name)) in s:
                return s
            anchor = 'const u16 gObjectEventPal_NpcOwl[] = INCBIN_U16("graphics/object_events/palettes/npc_owl.gbapal");\n'
            assert s.count(anchor) == 1
            return s.replace(anchor, anchor + 'const u16 gObjectEventPal_NpcTown%s[] = INCBIN_U16("graphics/object_events/palettes/%s.gbapal");\n' % (camel(name), pal_name))
        edit("src/data/object_events/object_event_graphics.h", graphics_pal)

        for role in [r for r in ROLES if r in roles]:
            register_one(edit, "OBJ_EVENT_GFX_TOWN_%s_%s" % (name, role.upper()),
                         "Town%s%s" % (camel(name), role.capitalize()),
                         "town_%s_%s" % (name.lower(), role), tag_name,
                         "%s's %s (T-119): %s, in the town's own palette" % (name, role, roles[role][3]))

        g = guest_of(name)
        if g:
            register_one(edit, "OBJ_EVENT_GFX_" + g["const"], camel(g["const"]), g["fname"], tag_name,
                         "%s's guest (T-119): %s redrawn against the town's sixteen, so one map can hold both"
                         % (name, g["source"].replace("OBJ_EVENT_GFX_", "")))

    # the text colour table pairs gfx ids two at a time; locals speak in the neutral colour
    ev = open(os.path.join(GBA, "include/constants/event_objects.h")).read()
    pat = "|".join([r"OBJ_EVENT_GFX_TOWN_\w+"] + ["OBJ_EVENT_GFX_" + g["const"] for g in GUESTS])
    ids = {c: int(n) for c, n in re.findall(r"#define (%s) (\d+)" % pat, ev)}

    def colours(s):
        start = s.index("static const u8 sTextColorTable[] =")
        end = s.index("};", start)
        body = s[start:end]
        for const, n in sorted(ids.items(), key=lambda kv: kv[1]):
            if n % 2 == 1:
                continue                        # the odd id shares its even partner's line (or the guide's)
            if ("[%s / 2]" % const) not in body:
                body += "    [%s / 2] = COLORS(NPC_TEXT_COLOR_NEUTRAL, NPC_TEXT_COLOR_NEUTRAL),\n" % const
        return s[:start] + body + s[end:]
    edit("src/dynamic_placeholder_text_util.c", colours)


def main():
    rows, built, all_todo = [], [], []
    for prefix, name, tag, colours, roles in TOWNS:
        pal = full_palette(colours)
        for role in [r for r in ROLES if r in roles]:
            front, back, side, species = roles[role]
            frames = figure(front, back, side)
            check("%s %s" % (name, role), frames, LETTERS)
            img = sheet(frames, LETTERS, pal)
            built.append(("town_%s_%s.png" % (name.lower(), role), img))
            bg = Image.new("RGB", img.size, (150, 150, 150))
            bg.paste(img.convert("RGB"), (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
            rows.append(bg)
        todo, left = plan_maps(prefix, name, roles)
        all_todo += [(name, t) for t in todo]
        by_role = {r: sum(1 for t in todo if t[2] == r) for r in roles}
        print("  %-12s repoint %s%s" % (name, ", ".join("%s %d" % (r, by_role[r]) for r in ROLES if r in roles),
              ("; left alone on %s (a special-slot character shares the map)" % ", ".join(left)) if left else ""))
    guest_imgs = []
    for prefix, name, tag, colours, roles in TOWNS:
        g = guest_of(name)
        if not g:
            continue
        pal, remap = merged_palette(name, colours, roles)
        img = guest_sheet(pal, remap, g)
        guest_imgs.append((g, img))
        bg = Image.new("RGB", img.size, (150, 150, 150))
        bg.paste(img.convert("RGB"), (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        rows.append(bg)
        print("  %-12s guest %s -> %s, keeping %d colours of its own" % (
            name, g["source"].replace("OBJ_EVENT_GFX_", ""), g["const"], len([c for c in g["letters"]])))

    reverts = revert_plan()
    for mp, i, back, cur, held in reverts:
        print("  %-12s restore %s -> %s (%s holds that map's palette)" % (
            os.path.basename(os.path.dirname(mp)), cur.replace("OBJ_EVENT_GFX_", ""),
            back.replace("OBJ_EVENT_GFX_", ""), held))

    out = Image.new("RGB", (144 * 5, 32 * 5 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 5, 160), Image.NEAREST), (0, 160 * i))
    out.save(PREVIEW)
    print("  %d sheets -> preview %s (town by town: child, adult, elder; guests last)" % (len(rows), PREVIEW))
    if WRITE:
        rules = 0
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
            rules += ensure_rule(filename)       # a sheet we ADD has no conversion rule until we write one
        for g, img in guest_imgs:
            img.save(os.path.join(PEOPLE, g["fname"] + ".png"), bits=4)
            rules += ensure_rule(g["fname"] + ".png")
        register()
        changed = {}

        def load(mp):
            if mp not in changed:
                raw = open(mp).read()
                changed[mp] = (json.loads(raw), raw.endswith("\n"))
            return changed[mp][0]

        for name, (mp, i, role) in all_todo:
            load(mp)["object_events"][i]["graphics_id"] = "OBJ_EVENT_GFX_TOWN_%s_%s" % (name, role.upper())
        swapped = 0
        for g, _img in guest_imgs:
            for o in load(os.path.join(GBA, "data/maps/%s/map.json" % g["map"]))["object_events"]:
                if o.get("graphics_id") == g["source"]:
                    o["graphics_id"] = "OBJ_EVENT_GFX_" + g["const"]
                    swapped += 1
        for mp, i, back, _cur, _held in reverts:
            load(mp)["object_events"][i]["graphics_id"] = back
        for mp, (m, nl) in changed.items():
            open(mp, "w").write(json.dumps(m, indent=2) + ("\n" if nl else ""))
        print("  written %d sheets + %d guest, %d palettes, registered; %d citizens repointed, %d guest object(s) swapped, %d restored; %d maps"
              % (len(built), len(guest_imgs), len(TOWNS), len(all_todo), swapped, len(reverts), len(changed)))


if __name__ == "__main__":
    main()

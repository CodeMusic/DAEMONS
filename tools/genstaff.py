#!/usr/bin/env python3
"""Draw the BENCHMARK staff and their guide as a fable (T-116; vision.md 9.4).

    python3 tools/genstaff.py            # preview to /tmp/staff_ow.png
    python3 tools/genstaff.py --write    # the ten sheets

Their OWN sprites, not redraws: every gym trainer borrowed a shared class sheet (LASS is on 39 maps),
so the staff are new object graphics (OBJ_EVENT_GFX_STAFF_*, BENCHMARK_GUIDE) that only the eight
gyms use, and nothing outside them changes. One species per gym, chosen for the gym's idea:

    SLATE        staff_slate.png              a young beaver apprentice: a record in material that lasts
    DOLDRUM      staff_doldrum_swimmer.png    a manatee, afloat and content -- drawn low in the water,
                                              ten frames like the swimmer it replaces
                 staff_doldrum_picnicker.png  a capybara at ease under a sun hat
    ARDOR        staff_ardor.png              a meerkat on watch, the one who reacts first
    VERDIGRIS    staff_verdigris.png          a poodle clipped to one exact shape
    LURID        staff_lurid.png              a tailless poison dart frog, the harm in the touch
    BRAZEN       staff_brazen.png             a tarsier, huge eyes on whatever is framed for it
    QUICKSILVER  staff_quicksilver.png        a lab rat with a clipboard
    CALLOW       staff_callow.png             a penguin in a grey suit, cheerful and ordinary
    the guide    benchmark_guide.png          an old bloodhound who has sniffed out every room

Trainers walk up to a player they spot, so every sheet has the walk frames. Each draws from the
palette slot its object graphics name (the same slots the leaders use; no colour changes).
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import overlay, figure, check, sheet, read_pal, WHITE, GREEN, PEOPLE
from genleaders import H, S, BLUE, PINK

PREVIEW = "/tmp/staff_ow.png"
WRITE = "--write" in sys.argv

# ------------------------------------------------------------------ SLATE: a young beaver (npc_green)
BEAVER_FRONT = H([
    "",
    "   KK",
    "  KSSKKK",
    " KSSSSSS",
    " KSSKSSS",     # a keen eye; a child's head, large
    " KSSSSaa",
    " KSSSaaa",
    "  KSSaWW",     # the teeth
    "   KKaWW",
    "   KyyyJ",     # a yellow scout scarf, a green shirt
    "  KJJyyJ",
    " KSJJJyJ",
    " KSJJJJJ",
    " KSKJJJJ",
    "  KKoooo",     # olive shorts
    "   Koooo",
    "   KooKo",
    "   KSSK",
    "   KSSK",
    "  KeeeK",
    "  KeeeK",
    "  KKKKK",
    "",
])
BEAVER_FRONT = overlay(BEAVER_FRONT, 14, ["KKK", "KeeK", "KeYK", "KeeK", " KK"], 0)     # the flat tail
BEAVER_FRONT = overlay(BEAVER_FRONT, 11, ["KKKK", "KeWK", "KKKK"], 12)                  # his notebook
BEAVER_BACK = H([
    "",
    "   KK",
    "  KSSKKK",
    " KSSSSSS",
    " KSSSSSS",
    " KSSSSSS",
    " KeSSSSS",
    "  KeSSSS",
    "   KKSSS",
    "   KyyyJ",
    "  KJJyyy",
    " KSJJJJJ",
    " KSJJJJJ",
    " KSKJJJJ",
    "  KKoooo",
    "   Koooo",
    "   KooKo",
    "   KSSK",
    "   KSSK",
    "  KeeeK",
    "  KeeeK",
    "  KKKKK",
    "",
])
BEAVER_BACK = overlay(BEAVER_BACK, 15, ["KeeK", "KeYK", "KeeK", "KeYK", " KK "], 6)
BEAVER_SIDE = S([
    "",
    "      KK",
    "     KSSKK",
    "   KKSSSSSK",
    "  KSSKSSSSK",
    " KaaSSSSSSK",
    " KWaaSSSSK",
    "  KKaSSSK",
    "    KKSK",
    "    KyyJK",
    "   KJJyJJK",
    "   KSJJJJK",
    "   KSKJJJK",
    "    KJJJJK",
    "    KooooKKK",
    "    KooooKeeK",
    "    KoooKKeYeK",
    "     KSSK KeeK",
    "     KSSK  KK",
    "    KeeeK",
    "    KeeeeK",
    "    KKKKKK",
    "",
])

# ------------------------------------------------------------------ DOLDRUM: a manatee, afloat (npc_pink)
MANATEE_FRONT = H([
    "", "", "", "", "", "", "", "", "",
    "    KKKK",
    "   Knnnn",     # a navy swim cap
    "  KGnnnn",
    "  Kgwggg",
    "  KgKggg",     # a half-closed eye
    "  Kggggw",
    "  Kgwwww",     # the broad soft snout
    "  KKgggg",
    "KgKggggg",     # flippers at the waterline
    "  WcWWc ",     # the water, barely moving
    "   W  c",
    "", "", "",
])
MANATEE_BACK = H([
    "", "", "", "", "", "", "", "", "",
    "    KKKK",
    "   Knnnn",
    "  KGnnnn",
    "  Kggggg",
    "  Kggggg",
    "  Kggggg",
    "  KGgggg",
    "  KKgggg",
    "KgKggggg",
    "  WcWWc ",
    "   W  c",
    "", "", "",
])
MANATEE_SIDE = S([
    "", "", "", "", "", "", "", "", "",
    "     KKKK",
    "    KnnnnK",
    "   KGnnnnK",
    "  KgKggggK",
    " KwwgggggK",
    " KwwwgggggK",
    "  KKKgggggK",
    "    KggggKK",
    "   KgKggggK",
    "  WWc WWcW",
    "   W   c",
    "", "", "",
])

# ------------------------------------------------------------------ DOLDRUM: a capybara at ease (npc_blue)
CAPY_FRONT = H([
    "",
    "   KKKKK",     # a wide sun hat
    " KKyyyyy",
    "Kyyyyyyy",
    " KKSSSSS",
    "  KSKSSS",     # eyes nearly closed
    "  KSSSSS",
    "  KSSSee",
    "   KKSSS",
    "   KyWWW",     # a white collar on a yellow dress
    "  Kyyyyy",
    " KSyyyyy",
    " KSyyyyy",
    " KSKyyoy",
    "  KKyyyy",
    "   Kyyyy",
    "  Kyyyyy",
    "  KKKKKK",
    "    KSSK",
    "    KSSK",
    "   KeeeK",
    "   KKKKK",
    "",
])
CAPY_FRONT = overlay(CAPY_FRONT, 12, ["KKKK", "KoYK", "KooK", "KKKK"], 12)            # the picnic basket
CAPY_BACK = H([
    "",
    "   KKKKK",
    " KKyyyyy",
    "Kyyyyyyy",
    " KKSSSSS",
    "  KSSSSS",
    "  KSSSSS",
    "  KeSSSS",
    "   KKSSS",
    "   Kyyyy",
    "  Kyyyyy",
    " KSyyyyy",
    " KSyyyyy",
    " KSKyyyy",
    "  KKyyyy",
    "   Kyyyy",
    "  Kyyyyy",
    "  KKKKKK",
    "    KSSK",
    "    KSSK",
    "   KeeeK",
    "   KKKKK",
    "",
])
CAPY_SIDE = S([
    "",
    "     KKKK",
    "   KKyyyyKK",
    " KyyyyyyyyyyK",
    "  KSSSSSSSKK",
    " KSSSKSSSSK",
    "KeSSSSSSSSK",
    " KSSSSSSSK",
    "   KKSSSK",
    "    KWyyK",
    "    KyyyyK",
    "   KSyyyyK",
    "   KSKyyyK",
    "   KKyyyyK",
    "    KyyyyK",
    "   KyyyyyK",
    "   KyyyyyyK",
    "   KKKKKKKK",
    "     KSSK",
    "     KSSK",
    "    KeeeK",
    "    KKKKK",
    "",
])

# ------------------------------------------------------------------ ARDOR: a meerkat on watch (npc_white)
MEERKAT_FRONT = H([
    "",
    "",
    "    KKKK",
    "   KTTTT",
    "  KTTTTT",
    "  KGKTTT",     # the dark eye patch
    "  KTTTTa",
    "   KTTTa",
    "   KKTaK",
    "    KTTT",
    "   KeTTT",     # brown overalls
    "  KTeTTT",
    " KTTeeee",
    " KTKeeee",
    "  KKeueu",     # a tool belt
    "   Keeee",
    "   Keeee",
    "   KeeKe",
    "   KeeK",
    "   KeeK",
    "  KTTTK",
    "  KKKKK",
    "",
])
MEERKAT_FRONT = overlay(MEERKAT_FRONT, 4, ["K", "g"], 1)                                # the headset
MEERKAT_BACK = H([
    "",
    "",
    "    KKKK",
    "   KTTTT",
    "  KTTTTT",
    "  KTTTTT",
    "  KTTTTT",
    "   KTTTT",
    "   KKTTT",
    "    KTTT",
    "   KeTTe",
    "  KTeTeT",
    " KTTeeee",
    " KTKeeee",
    "  KKeueu",
    "   Keeee",
    "   KeeKe",
    "   KeeKT",
    "   KeeKT",     # the thin tail
    "   KeeKT",
    "  KTTTKK",
    "  KKKKK",
    "",
])
MEERKAT_SIDE = S([
    "",
    "",
    "     KKKK",
    "    KTTTTK",
    "   KGKTTTK",
    " KKaTTTTTK",
    "  KKaTTTK",
    "    KKTTK",
    "     KTTK",
    "     KeTK",
    "    KTeeK",
    "    KTeeeK",
    "   KTKeeeK",
    "    KeueuK",
    "    KeeeeK",
    "    KeeeeKK",
    "    KeeeKTK",
    "    KeeeK TK",
    "    KeeK  TK",
    "    KeeK   K",
    "   KTTTK",
    "   KKKKK",
    "",
])

# ------------------------------------------------------------------ VERDIGRIS: a poodle, clipped (npc_green)
POODLE_FRONT = H([
    "    KKKK",
    "   KWWWW",     # the topknot, clipped round
    "   KWaWW",
    "    KKWW",
    "   KWWWW",
    "  KaWKWW",
    "  KaWWWW",
    "   KaWWW",
    "    KaWK",
    "    KJJJ",     # a green smock
    "   KJJJJ",
    "  KWKJJJ",
    " KWWKJJJ",     # a pompom at each cuff
    "  KKNJJJ",
    "   KNNNN",     # a pressed dark skirt
    "   KNNNN",
    "  KNNNNN",
    "  KKKKKK",
    "    KWK",
    "    KWK",
    "   KeeK",
    "   KKKK",
    "",
])
POODLE_FRONT = overlay(POODLE_FRONT, 13, ["KK", "KWK", "KK"], 13)                      # the tail's pompom
POODLE_BACK = H([
    "    KKKK",
    "   KWWWW",
    "   KWWWW",
    "    KKWW",
    "   KWWWW",
    "  KaWWWW",
    "  KaWWWW",
    "   KaWWW",
    "    KKWW",
    "    KJJJ",
    "   KJJJJ",
    "  KWKJJJ",
    " KWWKJJJ",
    "  KKJJJJ",
    "   KNNNN",
    "   KNNNN",
    "  KNNNNN",
    "  KKKKKK",
    "    KWK",
    "    KWK",
    "   KeeK",
    "   KKKK",
    "",
])
POODLE_BACK = overlay(POODLE_BACK, 13, ["KWWK"], 6)
POODLE_SIDE = S([
    "     KKKK",
    "    KWWWWK",
    "    KWaWWK",
    "     KKWWK",
    "    KWWWWWK",
    "  KKWKWWWWK",
    " KWWWWWWWK",
    " KKaWWWWK",
    "   KKKWK",
    "     KJJK",
    "    KJJJJK",
    "   KWKJJJK",
    "  KWWKJJJKKK",
    "   KKJJJJKWK",
    "    KNNNNKKK",
    "    KNNNNK",
    "   KNNNNNK",
    "   KKKKKKK",
    "     KWK",
    "     KWK",
    "    KeeK",
    "    KKKK",
    "",
])

# ------------------------------------------------------------------ LURID: a tailless dart frog (npc_pink)
FROG_FRONT = H([
    "",
    "",
    "   KKKKK",
    "  KcWKBB",     # eyes up top
    " KBBBBBB",
    " KBnBBnB",     # the dark patches
    " KBBBBBB",
    "  KBnnnn",     # a lazy smile
    "   KKBBB",
    "   KWpPp",     # a harlequin waistcoat
    "  KWWPpP",
    " KBWWpPp",
    " KBWKPpP",
    " KBKGpPp",
    "  KKGGGG",
    "   KGGGG",
    "   KGGKG",
    "   KGGK",
    "   KGGK",
    "   KBBK",
    "  KeeeK",
    "  KKKKK",
    "",
])
FROG_FRONT = overlay(FROG_FRONT, 0, ["   P", "", "c      B"], 4)                       # three balls in the air
FROG_BACK = H([
    "",
    "",
    "   KKKKK",
    "  KBBBBB",
    " KBBnBBB",
    " KBBBBBn",
    " KBnBBBB",
    "  KBBBBn",
    "   KKBBB",
    "   KWPPP",
    "  KWWPPP",
    " KBWPPPP",
    " KBWPPPP",
    " KBKPPPP",
    "  KKGGGG",
    "   KGGGG",
    "   KGGKG",
    "   KGGK",
    "   KGGK",
    "   KBBK",
    "  KeeeK",
    "  KKKKK",
    "",
])
FROG_SIDE = S([
    "",
    "",
    "    KKKKK",
    "   KcWKBBK",
    "  KBBBBBnBK",
    " KBBBBnBBBK",
    " KnnnBBBBK",
    "  KKKBBBK",
    "     KBBK",
    "    KWpPK",
    "   KWWPpPK",
    "   KBWpPpK",
    "   KBKPpPK",
    "    KGGGGK",
    "    KGGGGK",
    "    KGGGGK",
    "    KGGGK",
    "    KGGGK",
    "    KGGGK",
    "    KBBBK",
    "    KeeeeK",
    "    KKKKKK",
    "",
])

# ------------------------------------------------------------------ BRAZEN: a tarsier, watching (npc_white)
TARSIER_FRONT = H([
    "",
    "  KTK",
    "  KKTKKK",
    "  KTTTTT",
    " KTKKKTT",     # eyes too big for the face
    " KTKeKTT",
    " KTKKKTT",
    "  KTTTTa",
    "   KKTTK",
    "   KgGGG",     # a dark turtleneck under a long grey coat
    "  KggGGG",
    " KTggGGG",
    " KTggGGG",
    " KTKgGGG",
    "  KKgGGG",
    "   KgGGG",
    "   KgGGG",
    "   KggKG",
    "   KggK",
    "   KGGK",
    "  KeeeK",
    "  KKKKK",
    "",
])
TARSIER_FRONT = overlay(TARSIER_FRONT, 15, [" K", "KTK", "K TK", "  TK", "  KTK", "   K"], 12)   # the long tail
TARSIER_BACK = H([
    "",
    "  KTK",
    "  KKTKKK",
    "  KTTTTT",
    " KTTTTTT",
    " KTTTTTT",
    " KeTTTTT",
    "  KeTTTT",
    "   KKTTT",
    "   Kgggg",
    "  Kggggg",
    " KTgggGg",
    " KTgggGg",
    " KTKgggg",
    "  KKgggg",
    "   Kgggg",
    "   Kgggg",
    "   KggKg",
    "   KggK",
    "   KGGK",
    "  KeeeK",
    "  KKKKK",
    "",
])
TARSIER_BACK = overlay(TARSIER_BACK, 16, ["KT", "KT", "KTK", " KT", " KK"], 7)
TARSIER_SIDE = S([
    "",
    "      KTK",
    "     KTTK",
    "   KKTTTTK",
    "  KKKKTTTTK",
    " KTKeKTTTTK",
    "  KKKKTTTK",
    " KaTTTTTK",
    "  KKKTTK",
    "    KKKgK",
    "   KgKKggK",
    "   KTKKggK",
    "   KTKgggK",
    "    KKggggK",
    "    KggggK",
    "    KggggKKK",
    "    KggggK TK",
    "    KgggK   TK",
    "    KgggK   TK",
    "    KGGGK    K",
    "    KeeeeK",
    "    KKKKKK",
    "",
])

# ------------------------------------------------------------------ QUICKSILVER: a lab rat (npc_pink)
RAT_FRONT = H([
    "",
    "  KpK",        # round pink ears
    "  KppKKK",
    "   KKggg",
    "   Kgggg",
    "  KgKggg",
    "  Kggggg",
    "   Kgggw",
    "    KKwp",     # the pink nose
    "   KWWWw",     # a white lab coat over grey
    "  KWWWGw",
    " KWWWWGw",
    " KWwWWGw",
    " KgKWWWw",
    "  KKWWWW",
    "   KWWWW",
    "   KWWKW",
    "   KGGK",
    "   KGGK",
    "   KGGK",
    "  KpppK",
    "  KKKKK",
    "",
])
RAT_FRONT = overlay(RAT_FRONT, 11, ["KKKK", "KWwK", "KWwK", "KKKK"], 11)                # the clipboard
RAT_FRONT = overlay(RAT_FRONT, 16, ["  KK", " KpK", "KpK", "KpK", "KpK", " KK"], 0)      # the long pink tail
RAT_BACK = H([
    "",
    "  KpK",
    "  KppKKK",
    "   KKggg",
    "   Kgggg",
    "  Kggggg",
    "  Kggggg",
    "   Kgggg",
    "    KKgg",
    "   KWWWW",
    "  KWWWWW",
    " KWWWWWW",
    " KWWwWWW",
    " KgKWWWW",
    "  KKWWWW",
    "   KWWWW",
    "   KWWKK",
    "   KGGKp",
    "   KGGKp",
    "   KGGKp",
    "  KpppKp",
    "  KKKKK",
    "",
])
RAT_SIDE = S([
    "",
    "      KpK",
    "     KppK",
    "    KKgggK",
    "   KgKggggK",
    " KwggggggggK",
    "KpwwggggggK",
    " KKKwggggK",
    "    KKKgK",
    "     KWGK",
    "    KWWWWK",
    "   KWWWWWK",
    "   KgKWWWK",
    "    KWWWWK",
    "    KWWWWK",
    "    KWWWWKK",
    "    KGGGGKpK",
    "    KGGGK  pK",
    "    KGGGK   pK",
    "    KGGGK   pK",
    "    KppppK  K",
    "    KKKKKK",
    "",
])

# ------------------------------------------------------------------ CALLOW: a penguin at work (npc_white)
PENGUIN_FRONT = H([
    "",
    "",
    "    KKKK",
    "   KGGGG",
    "  KGGWWW",
    "  KGWKWW",     # a pleasant eye
    "  KGWWWW",
    "  KGWWRR",     # the beak
    "   KKWWR",
    "   KgWRW",     # a red lanyard on a grey suit
    "  KggRWW",
    " KGggRWW",
    " KGggWRW",
    " KGKgggW",
    "  KKgggg",
    "   KgggW",
    "   KgggW",
    "   KggKK",
    "   KGGK",
    "   KGGK",
    "  KRRRK",      # orange feet
    "  KKKKK",
    "",
])
PENGUIN_FRONT = overlay(PENGUIN_FRONT, 12, ["KKK", "KWKK", "KKK"], 12)                  # a coffee mug
PENGUIN_BACK = H([
    "",
    "",
    "    KKKK",
    "   KGGGG",
    "  KGGGGG",
    "  KGGGGG",
    "  KGGGGG",
    "  KGGGGG",
    "   KKGGG",
    "   Kgggg",
    "  Kggggg",
    " KGggggg",
    " KGggggg",
    " KGKgggg",
    "  KKgggg",
    "   Kgggg",
    "   KgggG",
    "   KggKK",
    "   KGGK",
    "   KGGK",
    "  KRRRK",
    "  KKKKK",
    "",
])
PENGUIN_SIDE = S([
    "",
    "",
    "     KKKK",
    "    KGGGGK",
    "   KWKGGGGK",
    " RRWWWGGGGK",
    "  KWWWGGGK",
    "   KWWGGK",
    "    KKGGK",
    "    KRWgK",
    "   KWRgggK",
    "   KWggGgK",
    "   KWgGggK",
    "   KWggggK",
    "   KWggggK",
    "    KggggK",
    "    KggggK",
    "    KgggK",
    "    KGGGK",
    "    KGGGK",
    "  KRRRRK",
    "  KKKKKK",
    "",
])

# ------------------------------------------------------------------ the guide: an old bloodhound (npc_blue)
HOUND_FRONT = H([
    "",
    "",
    "    KKKK",
    "   KOOOO",
    "  KrOOOO",
    " KdrOKOO",     # long ears hanging either side of a patient eye
    " KdrOOOO",
    " KdrOOOO",
    " KddKOaa",
    "  KdKaaK",
    "   KeWWV",     # a brown cardigan, a lanyard
    "  KeeWWV",
    " KOeeWWV",
    " KOKeeWV",
    "  KKeeee",
    "   Kdddd",
    "   KddKd",
    "   KddK",
    "   KddK",
    "   KddK",
    "  KdddK",
    "  KKKKK",
    "",
])
HOUND_FRONT = overlay(HOUND_FRONT, 12, ["KvK", "KvK", "KKK"], 12)                     # a water bottle
HOUND_BACK = H([
    "",
    "",
    "    KKKK",
    "   KOOOO",
    "  KrOOOO",
    " KdrOOOO",
    " KdrOOOO",
    " KdrrOOO",
    " KddKrrO",
    "  KKKKrr",
    "   Keeee",
    "  Keeeee",
    " KOeeeee",
    " KOKeeee",
    "  KKeeee",
    "   Kdddd",
    "   KddKd",
    "   KddKr",
    "   KddKr",
    "   KddK",
    "  KdddK",
    "  KKKKK",
    "",
])
HOUND_SIDE = S([
    "",
    "",
    "     KKKK",
    "    KOOOOK",
    "   KOKOOOOK",
    " KaaOOOdddK",
    "KKaaOOOddrK",
    " KaKOOOddrK",
    "  KKKOOKdK",
    "     KKKK",
    "    KeVWK",
    "   KeeeWK",
    "   KOKeeK",
    "   KKeeeK",
    "    KeeeeKK",
    "    KddddKrK",
    "    KdddK KK",
    "    KdddK",
    "    KdddK",
    "    KdddK",
    "    KddddK",
    "    KKKKKK",
    "",
])

STAFF = [
    ("beaver",   "staff_slate.png",             figure(BEAVER_FRONT, BEAVER_BACK, BEAVER_SIDE),                    GREEN, "npc_green.pal"),
    ("manatee",  "staff_doldrum_swimmer.png",   (lambda f: f + [f[0]])(figure(MANATEE_FRONT, MANATEE_BACK, MANATEE_SIDE)), PINK,  "npc_pink.pal"),
    ("capybara", "staff_doldrum_picnicker.png", figure(CAPY_FRONT, CAPY_BACK, CAPY_SIDE),                          BLUE,  "npc_blue.pal"),
    ("meerkat",  "staff_ardor.png",             figure(MEERKAT_FRONT, MEERKAT_BACK, MEERKAT_SIDE),                 WHITE, "npc_white.pal"),
    ("poodle",   "staff_verdigris.png",         figure(POODLE_FRONT, POODLE_BACK, POODLE_SIDE),                    GREEN, "npc_green.pal"),
    ("frog",     "staff_lurid.png",             figure(FROG_FRONT, FROG_BACK, FROG_SIDE),                          PINK,  "npc_pink.pal"),
    ("tarsier",  "staff_brazen.png",            figure(TARSIER_FRONT, TARSIER_BACK, TARSIER_SIDE),                 WHITE, "npc_white.pal"),
    ("rat",      "staff_quicksilver.png",       figure(RAT_FRONT, RAT_BACK, RAT_SIDE),                             PINK,  "npc_pink.pal"),
    ("penguin",  "staff_callow.png",            figure(PENGUIN_FRONT, PENGUIN_BACK, PENGUIN_SIDE),                 WHITE, "npc_white.pal"),
    ("hound",    "benchmark_guide.png",         figure(HOUND_FRONT, HOUND_BACK, HOUND_SIDE),                       BLUE,  "npc_blue.pal"),
]


def main():
    rows, built = [], []
    for name, filename, frames, index, palname in STAFF:
        check(name, frames, index)
        img = sheet(frames, index, read_pal(palname))
        built.append((filename, img))
        bg = Image.new("RGB", img.size, (150, 150, 150))
        bg.paste(img.convert("RGB"), (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        rows.append(bg)
    out = Image.new("RGB", (160 * 6, 32 * 6 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 6, 192), Image.NEAREST), (0, 192 * i))
    out.save(PREVIEW)
    print("  %d staff sheets -> preview %s" % (len(built), PREVIEW))
    if WRITE:
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
            print("  written people/%s (%d frames)" % (filename, img.width // 16))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Redraw the institutions every town shares, as a fable (T-118; vision.md 9.4).

    python3 tools/geninst.py            # preview to /tmp/institutions_ow.png
    python3 tools/geninst.py --write    # the eight sheets, in place, and the deliveryman's slot

These are REDRAWS of vanilla's own sheets, not new sprites: an institution should look the same in
every town, so every map that uses one changes, which is the point. The species is the role:

    nurse.png                    the CHECKPOINT attendant, an elephant: a checkpoint is a saved state,
                                 and the elephant never forgets. Four frames; the fourth is her bow
    cable_club_receptionist.png  the link receptionist, a honeybee: a hive that talks by dancing
    union_room_receptionist.png  the same hive, with a red accent
    clerk.png                    THE REPO's clerk, a grey squirrel who keeps a cache of everything --
                                 grey, because orange fur and ears read as a fox, and the foxes are the Clears
    mg_deliveryman.png           the deliveryman, a homing pigeon -- moved to the pink slot, since the
                                 green slot has no grey for him
    policeman.png                the officer, an Alsatian with a notebook and a whistle
    rocket_m.png, rocket_f.png   CORPUS STAFF, penguins: the organisation CALLOW's gym staff belong to
                                 (4.31), so the man is the same drawing; cheerful, never a sneer

Frame counts are vanilla's: the attendant four, the receptionists and the deliveryman three still
frames, the clerk, the officer and the staff nine with their walks.
"""
import os, re, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import overlay, figure, standing, check, sheet, read_pal, WHITE, PEOPLE, GBA
from genleaders import H, S, BLUE, PINK
from genstaff import PENGUIN_FRONT, PENGUIN_BACK, PENGUIN_SIDE

PREVIEW = "/tmp/institutions_ow.png"
WRITE = "--write" in sys.argv

# ------------------------------------------------------------------ the CHECKPOINT attendant, an elephant (npc_pink)
ELEPHANT_FRONT = H([
    "",
    "",
    "   KKKKK",
    " KKggggg",
    "KwgKgggg",     # the great ears
    "KwgKgKgg",     # a kind eye
    "KwgKgggg",
    " KgKgggg",
    "  KKKgKg",     # the trunk down the middle
    "   KcKKg",
    "  Kccccc",     # a pale attendant's tunic
    " Kgccccc",
    " Kgccccc",
    " KgKcccc",     # careful hands folded
    "  KKcccc",
    "   KGGGG",
    "   KGGGG",
    "   KGGKG",
    "   KGGK",
    "   KGGK",
    "  KeeeK",
    "  KKKKK",
    "",
])
ELEPHANT_FRONT = overlay(ELEPHANT_FRONT, 10, ["WW"], 9)                                  # a plain badge
ELEPHANT_BACK = H([
    "",
    "",
    "   KKKKK",
    " KKggggg",
    "KwgKgggg",
    "KwgKgggg",
    "KwgKgggg",
    " KgKgggg",
    "  KKKggg",
    "   Kcccc",
    "  Kccccc",
    " Kgccccc",
    " Kgccccc",
    " KgKcccc",
    "  KKcccc",
    "   KGGGG",
    "   KGGGG",
    "   KGGKG",
    "   KGGK",
    "   KGGK",
    "  KeeeK",
    "  KKKKK",
    "",
])
ELEPHANT_BACK = overlay(ELEPHANT_BACK, 15, ["gK"], 7)                                    # a small tail
ELEPHANT_SIDE = S([
    "",
    "",
    "      KKKKK",
    "    KKgggggK",
    "   KgggKwwgK",
    "  KgKggKwwgK",
    " KgggggKwwK",
    "KgggggggKK",
    "KgK KgggK",
    "Kg  KcccK",    # the trunk hangs forward
    " K  KccccK",
    "    KgcccK",
    "    KgcccK",
    "    KKcccK",
    "    KccccK",
    "    KGGGGK",
    "    KGGGGK",
    "    KGGGK",
    "    KGGGK",
    "    KGGGK",
    "    KeeeeK",
    "    KKKKKK",
    "",
])


def bow(front):
    """the head dips a row and the eyes close"""
    head = [list(r) for r in front[2:10]]
    head[3][5] = "g"; head[3][10] = "g"
    return front[:2] + [" " * 16] + ["".join(r) for r in head[:-1]] + front[10:]


# ------------------------------------------------------------------ the link receptionists, honeybees (npc_white)
BEE_FRONT = H([
    "    K",        # antennae
    "     K",
    "    KKKK",
    "   KTTTT",
    "  KTTTTT",
    "  KKKTTT",     # the great dark eyes
    "  KKKTTT",
    "   KTTTT",
    "    KKTT",
    "   KGWWW",     # a dark blazer over a white shirt
    " KwKGGWW",     # clear wings at her shoulders
    "KwwKGGWG",
    "KwwKGGGG",
    " KKTKGGG",
    "   KGGGG",
    "   KTTKT",     # the striped abdomen below the jacket
    "   KKTTK",
    "    KTK",
    "    KTK",
    "    KTK",
    "   KKKK",
    "",
    "",
])
BEE_FRONT = overlay(BEE_FRONT, 5, ["K", "G", "K"], 1)                                     # the headset
BEE_BACK = H([
    "    K",
    "     K",
    "    KKKK",
    "   KTTTT",
    "  KTTTTT",
    "  KTTTTT",
    "  KTTTTT",
    "   KTTTT",
    "    KKTT",
    "   KGGGG",
    " KwKGGGG",
    "KwwKGGGG",
    "KwwKGGGG",
    " KKTKGGG",
    "   KGGGG",
    "   KTTKT",
    "   KKTTK",
    "    KTK",
    "    KTK",
    "    KTK",
    "   KKKK",
    "",
    "",
])
BEE_SIDE = S([
    "     K",
    "      K",
    "     KKKK",
    "    KTTTTK",
    "   KKKTTTTK",
    "   KKKTTTTK",
    "  KTKKTTTK",
    "   KTTTTK",
    "    KKTTKwK",
    "    KWGGKwwK",
    "   KWGGGKwwK",
    "   KTGGGGKK",
    "   KKGGGK",
    "    KGGGK",
    "    KTTKTK",
    "    KKTTKK",
    "     KTK",
    "     KTK",
    "     KTK",
    "    KKKK",
    "",
    "",
    "",
])
red = lambda rows: [r.replace("W", "R") for r in rows]                                   # the Union Room's hive

# ------------------------------------------------------------------ THE REPO's clerk, a red squirrel (npc_white)
SQUIRREL_FRONT = H([
    "",
    "   K",         # ear tufts, not a fox's points -- the Clears are the foxes
    "  KrK",
    "  KRRKKK",
    " KRRRRRR",     # a round head
    " KRKRRRR",
    " KRRRaaa",     # big cream cheeks
    "  KRaaaa",
    "   KKaaa",
    "   KWgWT",     # a striped shirt, apron straps
    "  KWgTTT",
    " KRWTTTT",
    " KRgTTTT",
    " KRKTTTT",
    "  KKTTTT",
    "   KTTTT",
    "   KeeKe",
    "   KeeK",
    "   KeeK",
    "   KeeK",
    "  KGGGK",
    "  KKKKK",
    "",
])
SQUIRREL_FRONT = overlay(SQUIRREL_FRONT, 9, ["KK", "KRRK", "KRrRK", "KRRRK", "KRrRK", "KRRRK", "KRRK", " KK"], 0)   # the big bushy tail
SQUIRREL_FRONT = overlay(SQUIRREL_FRONT, 12, ["KKKK", "KeeK", "KKKK"], 6)                 # a sealed parcel
SQUIRREL_BACK = H([
    "",
    "   KK",
    "  KRRK",
    "  KRRKKK",
    "  KRRRRR",
    "  KRRRRR",
    "  KRRRRR",
    "   KRRRR",
    "    KKRR",
    "   KWgWg",
    "  KWTWgW",
    " KRWgWgW",
    " KRgWgWg",
    " KRKWgWg",
    "  KKTTTT",
    "   KWgWg",
    "   KeeKe",
    "   KeeK",
    "   KeeK",
    "   KeeK",
    "  KGGGK",
    "  KKKKK",
    "",
])
SQUIRREL_BACK = overlay(SQUIRREL_BACK, 9, [" KKKK ", "KRRRRK", "KRrRRK", "KRRrRK", "KRRRRK", "KRrRRK", "KRRRRK", " KRRK ", "  KK  "], 5)
SQUIRREL_SIDE = S([
    "",
    "      KK",
    "     KRRK",
    "    KKRRKK",
    "   KRRRRRRK",
    "  KRKRRRRRK",
    " KaaRRRRRK",
    " KKaaRRRK",
    "    KKaK",
    "    KWgTK",
    "   KWgTTKKK",
    "   KRWTTKRRK",
    "   KRKTTKRrRK",
    "    KTTTKRRRK",
    "    KTTTKRrK",
    "    KTTTKRK",
    "    KeeeKK",
    "    KeeeK",
    "    KeeK",
    "    KeeK",
    "   KGGGK",
    "   KKKKK",
    "",
])

grey_squirrel = lambda rows: [r.replace("R", "g").replace("r", "G") for r in rows]   # grey, not red: orange and ears read as a fox,
SQUIRREL_FRONT, SQUIRREL_BACK, SQUIRREL_SIDE = grey_squirrel(SQUIRREL_FRONT), grey_squirrel(SQUIRREL_BACK), grey_squirrel(SQUIRREL_SIDE)   # and the Clears are the foxes

# ------------------------------------------------------------------ the deliveryman, a homing pigeon (npc_pink)
PIGEON_FRONT = H([
    "",
    "",
    "    KKKK",
    "   KnnBn",     # a small courier's cap
    "   Kgggg",     # the grey head shows under it
    "  KgKggg",
    "  Kggggg",
    "   KgggG",     # the beak
    "   Kgggg",     # the sheen shows from behind; from the front it read as eyes
    "   KBBnB",     # a courier-blue jacket, the satchel strap
    "  KBBBnB",
    " KgBBnBB",     # wings for hands
    " KgBnBBB",
    " KgKBBBB",
    "  KKgggg",
    "   Kgggg",
    "   KggKg",
    "    KPK",      # pink bird legs
    "    KPK",
    "   KPPK",
    "",
    "",
    "",
])
PIGEON_FRONT = overlay(PIGEON_FRONT, 12, ["KKKK", "KeWK", "KKKK"], 6)                   # a parcel
PIGEON_BACK = H([
    "",
    "",
    "    KKKK",
    "   Knnnn",
    "  KKnnnn",
    "   Kgggg",
    "  Kggggg",
    "   Kgggg",
    "   KBPBP",
    "   Keeee",
    "  Keeeee",
    " Kgemeee",
    " Kgeemee",
    " KgKemee",
    "  KKgggg",
    "   KGgGg",     # tail feathers
    "   KGGKG",
    "    KPK",
    "    KPK",
    "   KPPK",
    "",
    "",
    "",
])
PIGEON_SIDE = S([
    "",
    "",
    "     KKKK",
    "    KnnnnKK",
    "  KKnnnnnK",
    "   KgKgggK",
    " KGggggggK",
    "  KKgggggK",
    "   KBPBPK",
    "   KeeemK",
    "  KgeemeeK",
    "  KgeeeeeK",
    "  KKeeeeeKK",
    "   KggggKGGK",
    "   KggggKKGK",
    "    KgggK KK",
    "     KPK",
    "     KPK",
    "    KPPK",
    "",
    "",
    "",
    "",
])

recourier = lambda rows: [r.replace("e", "B").replace("m", "n") for r in rows]          # the same blue jacket from behind and beside
PIGEON_BACK, PIGEON_SIDE = recourier(PIGEON_BACK), recourier(PIGEON_SIDE)

# ------------------------------------------------------------------ the officer, an Alsatian (npc_blue)
DOG_FRONT = H([
    "",
    "   KK",        # upright ears
    "  KSdK",
    "  KSdKKK",
    "  KSSddd",
    "  KSKSSS",
    "  KSSSSs",
    "   KSsss",
    "    KKsK",     # the nose
    "   KDVDD",     # a navy uniform
    "  KDDDVD",
    " KSDDDDD",
    " KSDDDDD",
    " KSKDDDD",
    "  KKdddd",     # a plain belt
    "   KDDDD",
    "   KDDKD",
    "   KDDK",
    "   KDDK",
    "   KDDK",
    "  KKKKK",
    "  KKKKK",
    "",
])
DOG_FRONT = overlay(DOG_FRONT, 2, ["KKKK", "KyDK"], 6)                                  # the peaked cap
DOG_FRONT = overlay(DOG_FRONT, 12, ["KKK", "KWK", "KKK"], 12)                            # his notebook
DOG_FRONT = overlay(DOG_FRONT, 10, ["y"], 9)                                              # the whistle
DOG_BACK = H([
    "",
    "   KK",
    "  KSdK",
    "  KSdKKK",
    "  KSdddd",
    "  KSdddd",
    "  KSdddd",
    "   KSddd",
    "    KKdd",
    "   KDDDD",
    "  KDDDDD",
    " KSDDDDD",
    " KSDDDDD",
    " KSKDDDD",
    "  KKdddd",
    "   KDDDD",
    "   KDDKD",
    "   KDDKS",     # the tail
    "   KDDKS",
    "   KDDKd",
    "  KKKKK",
    "  KKKKK",
    "",
])
DOG_BACK = overlay(DOG_BACK, 2, ["KKKK", "KDDK"], 6)
DOG_SIDE = S([
    "",
    "      KK",
    "     KSdK",
    "    KKSdKK",
    "   KSSSdddK",
    "  KSKSSSddK",
    " KssSSSSSdK",
    "KKsssSSSK",
    " KKKKSSK",
    "     KVDK",
    "    KDDDDK",
    "   KSDDDDK",
    "   KSKDDDK",
    "    KDDDDK",
    "    KddddK",
    "    KDDDDKK",
    "    KDDDKSK",
    "    KDDDK SK",
    "    KDDK  SK",
    "    KDDK   K",
    "   KKKKK",
    "   KKKKK",
    "",
])
DOG_SIDE = overlay(DOG_SIDE, 2, ["KKKKK", "KDDyK"], 5)

# ------------------------------------------------------------------ CORPUS STAFF, a penguin in a skirt suit (npc_white)
PENGF_FRONT = H([
    "",
    "",
    "    KKKK",
    "   KGGGG",
    "  KGGWWW",
    "  KGWKWW",
    "  KGWWWW",
    "  KGWWRR",
    "   KKWWR",
    "   KgWRW",
    "  KggRWW",
    " KGggRWW",
    " KGggWRW",
    " KGKgggg",
    "  KKgggg",
    "  Kggggg",     # the skirt
    " Kgggggg",
    " KKKKKKK",
    "   KWWK",
    "   KWWK",
    "  KRRRK",
    "  KKKKK",
    "",
])
PENGF_FRONT = overlay(PENGF_FRONT, 11, ["KKKK", "KGgK", "KKKK"], 11)                    # a tablet
PENGF_BACK = H([
    "", "", "    KKKK", "   KGGGG", "  KGGGGG", "  KGGGGG", "  KGGGGG", "  KGGGGG", "   KKGGG",
    "   Kgggg", "  Kggggg", " KGggggg", " KGggggg", " KGKgggg", "  KKgggg", "  Kggggg", " Kgggggg",
    " KKKKKKK", "   KWWK", "   KWWK", "  KRRRK", "  KKKKK", "",
])
PENGF_SIDE = S([
    "", "", "     KKKK", "    KGGGGK", "   KWKGGGGK", " RRWWWGGGGK", "  KWWWGGGK", "   KWWGGK",
    "    KKGGK", "    KRWgK", "   KWRgggK", "   KWggGgK", "   KWgGggK", "   KWggggK", "   KWggggK",
    "   KgggggK", "  KggggggK", "  KKKKKKKK", "    KWWK", "    KWWK", "  KRRRRK", "  KKKKKK", "",
])

still = lambda f, b, s: [standing(f), standing(b), standing(s)]

SHEETS = [   # name, sheet, frames, letters, palette
    ("attendant", "nurse.png", still(ELEPHANT_FRONT, ELEPHANT_BACK, ELEPHANT_SIDE) + [standing(bow(ELEPHANT_FRONT))], PINK, "npc_pink.pal"),
    ("link receptionist", "cable_club_receptionist.png", still(BEE_FRONT, BEE_BACK, BEE_SIDE), WHITE, "npc_white.pal"),
    ("union receptionist", "union_room_receptionist.png", still(red(BEE_FRONT), BEE_BACK, red(BEE_SIDE)), WHITE, "npc_white.pal"),
    ("clerk", "clerk.png", figure(SQUIRREL_FRONT, SQUIRREL_BACK, SQUIRREL_SIDE), WHITE, "npc_white.pal"),
    ("deliveryman", "mg_deliveryman.png", still(PIGEON_FRONT, PIGEON_BACK, PIGEON_SIDE), PINK, "npc_pink.pal"),
    ("officer", "policeman.png", figure(DOG_FRONT, DOG_BACK, DOG_SIDE), BLUE, "npc_blue.pal"),
    ("corpus staff m", "rocket_m.png", figure(PENGUIN_FRONT, PENGUIN_BACK, PENGUIN_SIDE), WHITE, "npc_white.pal"),
    ("corpus staff f", "rocket_f.png", figure(PENGF_FRONT, PENGF_BACK, PENGF_SIDE), WHITE, "npc_white.pal"),
]


def move_deliveryman():
    path = os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")
    s = open(path).read()
    head = "const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_MGDeliveryman = {"
    assert s.count(head) == 1
    start = s.index(head); end = s.index("};", start)
    block, n1 = re.subn(r"\.paletteTag = OBJ_EVENT_PAL_TAG_NPC_\w+,", ".paletteTag = OBJ_EVENT_PAL_TAG_NPC_PINK,", s[start:end])
    block, n2 = re.subn(r"\.paletteSlot = PALSLOT_NPC_\w+,", ".paletteSlot = PALSLOT_NPC_2,", block)
    assert n1 == 1 and n2 == 1
    open(path, "w").write(s[:start] + block + s[end:])


def main():
    rows, built = [], []
    for name, filename, frames, index, palname in SHEETS:
        check(name, frames, index)
        old = Image.open(os.path.join(PEOPLE, filename))
        assert old.width == 16 * len(frames), "%s: vanilla has %d frames, drawn %d" % (filename, old.width // 16, len(frames))
        img = sheet(frames, index, read_pal(palname))
        built.append((filename, img))
        bg = Image.new("RGB", img.size, (150, 150, 150))
        bg.paste(img.convert("RGB"), (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        pair = Image.new("RGB", (144 + 8 + old.width, 32), (60, 60, 60))
        pair.paste(bg, (0, 0)); pair.paste(old.convert("RGB"), (152, 0))
        rows.append(pair)
    out = Image.new("RGB", (max(r.width for r in rows) * 5, 32 * 5 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 5, 160), Image.NEAREST), (0, 160 * i))
    out.save(PREVIEW)
    print("  %d institution sheets -> preview %s (ours on grey, then vanilla)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
            print("  written people/%s (%d frames)" % (filename, img.width // 16))
        move_deliveryman()
        print("  the deliveryman moved to the pink slot")


if __name__ == "__main__":
    main()

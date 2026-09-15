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

    CALLOW   green, unripe          a tree frog, a parakeet, an old iguana
    SLATE    stone; dead hardware   a pangolin, a rock hyrax docent, an old armadillo
    DOLDRUM  a becalmed sea         a seal pup, a sea otter, an old walrus
"""
import glob, json, os, re, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import overlay, figure, check, sheet, PEOPLE, GBA
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
SPECIAL = {"OBJ_EVENT_GFX_PROF_OAK", "OBJ_EVENT_GFX_BLUE", "OBJ_EVENT_GFX_DAISY", "OBJ_EVENT_GFX_OWL"}


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
]
ROLES = ("child", "adult", "elder")


def camel(s):
    return "".join(w.capitalize() for w in s.lower().split("_"))


def full_palette(colours):
    return [KEY] + list(colours) + [(255, 255, 255), (0, 0, 0)]


def plan_maps(prefix, name):
    """(map path, object index, role) for every citizen to repoint, and the maps left alone"""
    todo, left = [], []
    for mp in sorted(glob.glob(os.path.join(GBA, "data/maps/%s*/map.json" % prefix))):
        if mp.endswith("_Gym/map.json"):
            continue
        objs = json.load(open(mp)).get("object_events", [])
        special = any(o.get("graphics_id") in SPECIAL for o in objs)
        for i, o in enumerate(objs):
            g = o.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
            role = "child" if g in CHILD else "adult" if g in ADULT else "elder" if g in ELDER else None
            if not role or o.get("trainer_type") not in (None, "TRAINER_TYPE_NONE", "0"):
                continue
            if special:
                left.append(os.path.basename(os.path.dirname(mp)))
                continue
            todo.append((mp, i, role))
    return todo, sorted(set(left))


def register():
    def edit(path, fn):
        p = os.path.join(GBA, path); s = open(p).read(); s2 = fn(s)
        if s2 != s:
            open(p, "w").write(s2)

    for prefix, name, tag, colours, roles in TOWNS:
        pal_name = "npc_town_%s" % name.lower()
        tag_name = "OBJ_EVENT_PAL_TAG_NPC_TOWN_%s" % name
        with open(os.path.join(PALS, pal_name + ".pal"), "w") as f:
            f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in full_palette(colours)))

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

        for role in ROLES:
            const = "OBJ_EVENT_GFX_TOWN_%s_%s" % (name, role.upper())
            cname = "Town%s%s" % (camel(name), role.capitalize())
            fname = "town_%s_%s" % (name.lower(), role)

            def constants(s):
                if ("#define %s " % const) in s:
                    return s
                m = re.search(r"\n#define NUM_OBJ_EVENT_GFX\s+(\d+)\n", s); n = int(m.group(1))
                return s[:m.start()] + "\n#define %s %d" % (const, n) + "\n\n#define NUM_OBJ_EVENT_GFX     %d\n" % (n + 1) + s[m.end():]
            edit("include/constants/event_objects.h", constants)

            def graphics(s):
                if ("gObjectEventPic_%s[]" % cname) not in s:
                    anchor = 'const u16 gObjectEventPic_BenchmarkGuide[] = INCBIN_U16("graphics/object_events/pics/people/benchmark_guide.4bpp");\n'
                    assert s.count(anchor) == 1
                    s = s.replace(anchor, anchor + 'const u16 gObjectEventPic_%s[] = INCBIN_U16("graphics/object_events/pics/people/%s.4bpp");\n' % (cname, fname))
                if ("gObjectEventPal_NpcTown%s[]" % camel(name)) not in s:
                    anchor = 'const u16 gObjectEventPal_NpcOwl[] = INCBIN_U16("graphics/object_events/palettes/npc_owl.gbapal");\n'
                    assert s.count(anchor) == 1
                    s = s.replace(anchor, anchor + 'const u16 gObjectEventPal_NpcTown%s[] = INCBIN_U16("graphics/object_events/palettes/%s.gbapal");\n' % (camel(name), pal_name))
                return s
            edit("src/data/object_events/object_event_graphics.h", graphics)

            def pictables(s):
                if ("sPicTable_%s[]" % cname) in s:
                    return s
                start = s.index("static const struct SpriteFrameImage sPicTable_BenchmarkGuide[] = {")
                end = s.index("};\n", start) + 3
                block = "\nstatic const struct SpriteFrameImage sPicTable_%s[] = {\n%s};\n" % (cname, "".join("    overworld_frame(gObjectEventPic_%s, 2, 4, %d),\n" % (cname, k) for k in range(9)))
                return s[:end] + block + s[end:]
            edit("src/data/object_events/object_event_pic_tables.h", pictables)

            def info(s):
                if ("gObjectEventGraphicsInfo_%s =" % cname) in s:
                    return s
                return s.rstrip("\n") + "\n\n// %s's %s (T-119): %s, in the town's own palette\n" % (name, role, roles[role][3]) + (
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

    # the text colour table pairs gfx ids two at a time; locals speak in the neutral colour
    ev = open(os.path.join(GBA, "include/constants/event_objects.h")).read()
    ids = {c: int(n) for c, n in re.findall(r"#define (OBJ_EVENT_GFX_TOWN_\w+) (\d+)", ev)}

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
        for role in ROLES:
            front, back, side, species = roles[role]
            frames = figure(front, back, side)
            check("%s %s" % (name, role), frames, LETTERS)
            img = sheet(frames, LETTERS, pal)
            built.append(("town_%s_%s.png" % (name.lower(), role), img))
            bg = Image.new("RGB", img.size, (150, 150, 150))
            bg.paste(img.convert("RGB"), (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
            rows.append(bg)
        todo, left = plan_maps(prefix, name)
        all_todo += [(name, t) for t in todo]
        by_role = {r: sum(1 for t in todo if t[2] == r) for r in ROLES}
        print("  %-8s repoint child %d, adult %d, elder %d%s" % (name, by_role["child"], by_role["adult"], by_role["elder"],
              ("; left alone on %s (a special-slot character shares the map)" % ", ".join(left)) if left else ""))
    out = Image.new("RGB", (144 * 5, 32 * 5 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 5, 160), Image.NEAREST), (0, 160 * i))
    out.save(PREVIEW)
    print("  %d sheets -> preview %s (town by town: child, adult, elder)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
        register()
        changed = {}
        for name, (mp, i, role) in all_todo:
            if mp not in changed:
                raw = open(mp).read(); changed[mp] = (json.loads(raw), raw.endswith("\n"))
            changed[mp][0]["object_events"][i]["graphics_id"] = "OBJ_EVENT_GFX_TOWN_%s_%s" % (name, role.upper())
        for mp, (m, nl) in changed.items():
            open(mp, "w").write(json.dumps(m, indent=2) + ("\n" if nl else ""))
        print("  written %d sheets, %d palettes, registered; %d citizens repointed on %d maps" % (len(built), len(TOWNS), len(all_todo), len(changed)))


if __name__ == "__main__":
    main()

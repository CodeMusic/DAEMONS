#!/usr/bin/env python3
"""Draw the eight BENCHMARK leaders' overworld sprites as a fable (T-115; vision.md 9.4).

    python3 tools/genleaders.py            # preview to /tmp/leaders_ow.png
    python3 tools/genleaders.py --write    # the eight sheets, and each leader's palette slot

Drawn from the battle portraits (gfx/characters/), in genfolk.py's idiom and with its helpers --
the species is the ROLE, the animality integrated, drawn plainly, and an adult's head:

    CAIRN    brock.png      a grey-green tortoise in a cream shirt and dark apron, a clipboard,
                            a pencil behind the ear; his shell is his back
    BASIN    misty.png      a grey hippo in a pale blue tracksuit, a whistle on a cord
    GAUGE    lt_surge.png   a hare in an orange line engineer's jacket, a meter in his paw
    TRELLIS  erika.png      a blue-black bowerbird in a green apron, shears in her wing-hand
    TILT     koga.png       a squat, tailless olive toad in a plum waistcoat and green visor, cards
    MATTE    sabrina.png    a green chameleon in a dark turtleneck, brass glasses, her tail curled;
                            her framing hands stay in the portrait -- raised beside the head at
                            sixteen pixels, they read as ears
    ANNEAL   blaine.png     a charcoal salamander with orange spots, goggles up, a silver apron,
                            his gloves glowing
    SCORN    giovanni.png   the red cobra in a grey suit and red tie -- the only one who WALKS:
                            he crosses the hideout, Silph and the warehouse, so his sheet keeps
                            nine frames. The other seven stand in their rooms, and vanilla gave
                            them three.

PALETTES ARE STILL THE SLOTS -- but not vanilla's slot for each. A slot loads one fixed palette on
every map, and no colour in it changes; what changes is WHICH slot a leader draws from, so each
species finds its colours: the white slot's olives, greys and reds for CAIRN, ANNEAL and SCORN;
the green slot's olives, greens and plums for TRELLIS, TILT and MATTE; the pink slot's greys, pink
and pale blues for BASIN; the blue slot's orange for GAUGE. --write moves each leader's paletteTag
and paletteSlot in object_event_graphics_info.h to match.
"""
import os, re, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import mirror, overlay, figure, check, sheet, read_pal, WHITE, GREEN, PEOPLE, GBA

PREVIEW = "/tmp/leaders_ow.png"
WRITE = "--write" in sys.argv

# letter -> index for the two slots genfolk.py never needed
BLUE = {" ": 0, "a": 1, "s": 2, "S": 3, "e": 4, "y": 5, "o": 6, "Y": 7, "v": 8, "V": 9, "D": 10,
        "O": 11, "r": 12, "d": 13, "W": 14, "K": 15}            # npc_blue: peach, yellows, purples, orange, red
PINK = {" ": 0, "a": 1, "s": 2, "S": 3, "e": 4, "p": 5, "P": 6, "m": 7, "c": 8, "B": 9, "n": 10,
        "w": 11, "g": 12, "G": 13, "W": 14, "K": 15}            # npc_pink: peach, pinks, pale blues, greys


def H(rows):
    """halves padded to eight, mirrored to sixteen"""
    return mirror([r.ljust(8)[:8] for r in rows])


def S(rows):
    return [r.ljust(16)[:16] for r in rows]


# ------------------------------------------------------------------ CAIRN (npc_white): a tortoise
CAIRN_FRONT = H([
    "",
    "",
    "     KKK",
    "    Kttt",
    "   Ktttt",
    "   KtKtt",     # a heavy-lidded eye
    "   Ktttt",
    "   Kuttt",
    "    KKtt",
    "   KKwww",     # a cream collar
    "  KuKwGG",     # the shell's rim behind his arms; a dark apron
    " KuuKwGG",
    " KuuKwGG",
    " KuKttGG",     # olive paws
    " KuKKGGG",
    "  KKGGGG",
    "   KGGGG",
    "   KGGGG",
    "   KuuuG",
    "   KuuKK",
    "  KeeeK",      # brown boots
    "  KeeeK",
    "  KKKKK",
])
CAIRN_FRONT = overlay(CAIRN_FRONT, 11, ["KKKK", "KgwK", "KgwK", "KKKK"], 11)   # the clipboard
CAIRN_FRONT = overlay(CAIRN_FRONT, 1, [" K", "KT", "R "], 11)                  # the pencil behind his ear
CAIRN_BACK = H([
    "",
    "",
    "     KKK",
    "    Kttt",
    "   Ktttt",
    "   Ktttt",
    "   Ktttt",
    "   Kuttt",
    "   KKKtt",
    "  KuuuKK",     # the shell is his back: its plates
    " KuGuuGu",
    " KuuGGuu",
    "KuuGuuGu",
    "KuGuuGuu",
    "KuuGGuuG",
    " KuuuGuu",
    " KKuuuuu",
    "  KKKKKK",
    "   Kuuuu",
    "   KuuKK",
    "  KeeeK",
    "  KeeeK",
    "  KKKKK",
])
CAIRN_SIDE = S([
    "",
    "",
    "     KKKK",
    "    KttttK",
    "   KtKtttK",
    "  KttttttttK",
    "  KttttttttK",
    "   KKuttttK",
    "     KttKK",
    "    KwwwKuKK",
    "    KwGGKuuuK",
    "   KtwGGKuGuuK",
    "   KtwGGKuuGuK",
    "   KKGGGKuGuuK",
    "    KGGGKuuuK",
    "    KGGGGKKK",
    "    KGGGGK",
    "    KGGGGK",
    "    KuuuuK",
    "    KuuuK",
    "    KeeeK",
    "    KeeeeK",
    "    KKKKKK",
])

# ------------------------------------------------------------------ SCORN (npc_white): the red cobra
SCORN_FRONT = H([
    "",
    "   KKKKK",     # the hood
    "  KRRRRR",
    " KRRRRRR",
    " KRrRKRR",     # a level, pleased eye
    " KRrRRRR",
    " KRrRaaa",     # the cream throat
    "  KRRaaa",
    "   KKaaa",
    "   KgWWR",     # white collar, red tie
    "  KggWgR",
    " KggggWR",
    " KggggGR",
    " KgKgggG",
    " KRKgggg",     # a red hand
    "  KKgggg",
    "   Kgggg",
    "   Kgggg",
    "   KgggK",
    "   KgggK",
    "   KggK",
    "  KeeeK",      # brown shoes
    "  KKKKK",
])
SCORN_FRONT = overlay(SCORN_FRONT, 17, ["KK  ", "KRK ", "KRRK", " KRK", "  KK"], 0)   # the tail, behind him
SCORN_BACK = H([
    "",
    "   KKKKK",
    "  KRRRRR",
    " KRRRRRR",
    " KRRRRRR",
    " KRRrRRR",
    " KRRRrRR",
    "  KRRRRR",
    "   KKRRR",
    "   Kgggg",
    "  Kggggg",
    " KgggggG",
    " KgggggG",
    " KgggggG",
    " KRggggG",
    "  Kggggg",
    "   KggKK",
    "   KggKR",
    "   KggKR",
    "   KggKr",
    "   KggKR",
    "  KeeeKK",
    "  KKKKK",
])
SCORN_SIDE = S([
    "",
    "      KKKK",
    "     KRRRRK",
    "   KKRRRRRRK",
    "  KRKRRRRRRK",
    " KRRRRRRRRRK",
    " KaaRRRRRRK",
    "  KaaRRRRK",
    "   KaaaKK",
    "    KWRgggK",
    "   KgWRggggK",
    "   KggggggK",
    "   KgRgggggK",
    "   KgKggggK",
    "   KggggggK",
    "    KggggggKK",
    "    KggggKKRRK",
    "    KggggK KRRK",
    "    KggggK  KRK",
    "    KgggK    KK",
    "    KgggK",
    "    KeeeeK",
    "    KKKKKK",
])

# ------------------------------------------------------------------ TILT (npc_green): a tailless toad
TILT_FRONT = H([
    "",
    "",
    "   KKKKK",
    "  KJllll",     # the green visor
    " KJJJJJJ",
    "  KKoooo",
    " KoWKooo",     # an eye that has seen this before
    " Kyooooo",
    " KYYYYYY",     # the wide mouth
    "  Kyyyyy",
    "  KWKqqW",     # a white shirt, a plum waistcoat
    " KWWKqqq",
    "KoWWKqqq",
    "KoWKqqqq",
    "KoKbqqqq",
    " KKqqqqq",
    "  Kyyyyy",     # the belly below it
    "  Kyyyyy",
    "  KYyyyy",
    "   KooKK",
    "  KooK",       # short bowed legs, webbed feet
    " KooooK",
    " KKKKKK",
])
TILT_FRONT = overlay(TILT_FRONT, 11, ["KWKK", "WKWK", "KWWK"], 12)             # the cards, fanned
TILT_BACK = H([
    "",
    "",
    "   KKKKK",
    "  KJllll",
    " KJJJJJJ",
    " Koooooo",
    " Koooooo",
    " KoooYoo",
    " KYooooo",
    "  KYoooo",
    "  KWKqqq",
    " KWqqqqq",
    "KoWqqqqq",
    "KoWqqqqq",
    "KoKqqqqq",
    " KKbbbbb",
    "  Kyyyyy",
    "  Kyyyyy",
    "  KYyyyy",
    "   KooKK",
    "  KooK",
    " KooooK",
    " KKKKKK",
])
TILT_SIDE = S([
    "",
    "",
    "    KKKKKK",
    "   KllllllK",
    " KJJJJJJJJJK",
    "  KoKWooooK",
    " KooooooooK",
    " KYYYYooooK",
    "  KyyyyyyK",
    "   KKWqqqK",
    "   KWWqqqqK",
    "  KoWqqqqqK",
    "  KoKqqqqqK",
    "  KKqqqqqqK",
    "   KyyyyyyyK",
    "   KyyyyyyyK",
    "   KYyyyyyK",
    "    KoooooK",
    "   KooKKooK",
    "  KooK  KooK",
    " KoooK  KoooK",
    " KKKK    KKKK",
    "",
])

# ------------------------------------------------------------------ MATTE (npc_green): a chameleon
MATTE_FRONT = H([
    "",
    "      KK",
    "     KJl",     # the casque, a ridge up the middle of her head
    "    KJJl",
    "   KJJJJ",
    "  KJyKyJ",     # brass-rimmed glasses
    "  KJyyyJ",
    "  KJJJJJ",
    "   KKJJJ",
    "   Kbbbb",     # a dark turtleneck
    "  Kbbbbb",
    " KbKbbbb",
    " KbKbbbb",
    " KJKbbbb",     # green hands at her sides -- the framing gesture is her portrait's; at sixteen pixels
    "  KKbbbb",     # raised hands read as ears
    "   Kbbbb",
    "   Kbbbb",
    "   KbbKb",
    "   KbbKK",
    "   KbbK",
    "   KbbK",
    "  KeeeK",
    "  KKKKK",
])
MATTE_FRONT = overlay(MATTE_FRONT, 15, [" KKK", "KJ JK", "K JK", "KJK", " KK"], 11)   # the tail, curled
MATTE_BACK = H([
    "",
    "     KKK",
    "    KlJJ",
    "   KlJJJ",
    "   KJlll",
    "  KJllll",
    "  KJllll",
    "  KJJlll",
    "   KJJll",
    "   Kbbbb",
    "  Kbbbbb",
    " KlKbbbb",
    " KlKbbbb",
    "  KKbbbb",
    "   Kbbbb",
    "   Kbbbb",
    "   Kbbbb",
    "   KbbKb",
    "   KbbKK",
    "   KbbK",
    "   KbbK",
    "  KeeeK",
    "  KKKKK",
])
MATTE_BACK = overlay([r.replace("l", "J") for r in MATTE_BACK], 15, ["KJK", "KJK", "KJK", "KJJK", " KK"], 7)
MATTE_SIDE = S([
    "",
    "      KKKK",
    "     KlJJJK",
    "    KlllJJJK",
    "   KyyKllJJK",
    "  KlyKyllllK",
    "  KlllllllK",
    "   KKllllK",
    "     KbbK",
    "    KbbbbK",
    "  KlKbbbbK",
    "   KKbbbbK",
    "    KbbbbK",
    "    KbbbbK",
    "    KbbbbKKK",
    "    KbbbbKJJK",
    "    KbbbbK KJK",
    "    KbbbK  KJK",
    "    KbbbK KJJK",
    "    KbbbK KKK",
    "    KbbbK",
    "    KeeeeK",
    "    KKKKKK",
])
MATTE_SIDE = [r.replace("l", "J") for r in MATTE_SIDE]    # the same green from every side

# ------------------------------------------------------------------ TRELLIS (npc_green): a bowerbird
TRELLIS_FRONT = H([
    "",
    "      KK",
    "    KKbK",     # the crest
    "   Kbbbb",
    "  Kbbbbb",
    "  KbqKbb",     # a violet eye
    "  Kbbbbo",     # the beak
    "   Kbboo",
    "   Kbbbb",
    "   KbJJJ",     # a green apron
    "  KbbJJJ",
    " KbbbJJJ",
    " KbbKJJJ",
    " KbKNJJJ",
    "  KKNJJJ",
    "   KNJJJ",
    "   KNJJJ",
    "   KKNNN",
    "    KbbK",
    "     KYK",     # thin bird legs
    "     KYK",
    "    KYYK",
    "",
])
TRELLIS_FRONT = overlay(TRELLIS_FRONT, 12, ["KWK", "WKW", "K K"], 0)           # the shears
TRELLIS_FRONT = overlay(TRELLIS_FRONT, 14, ["Kb", "Kbb", "KbbK", " KbK", "  KK"], 12)   # the tail
TRELLIS_BACK = H([
    "",
    "      KK",
    "    KKbK",
    "   Kbbbb",
    "  Kbbbbb",
    "  Kbbbbb",
    "  Kbbbbb",
    "   Kbbbb",
    "   KNbbb",     # the apron's tie
    "   Kbbbb",
    "  Kbbbbb",
    " Kbbbbbb",
    " KbbKbbb",
    " KbKbbbb",
    "  KKbbbb",
    "   Kbbbb",
    "   KbbKb",
    "   KbbKb",
    "    KbKb",
    "     KYK",
    "     KYK",
    "    KYYK",
    "",
])
TRELLIS_BACK = overlay(TRELLIS_BACK, 15, ["KbbK", "KbbK", "KbbK", "KbbK", " KK "], 6)
TRELLIS_SIDE = S([
    "",
    "       KKK",
    "     KKbbK",
    "    KbbbbbK",
    "   KbqKbbbK",
    " KoobbbbbbK",
    "  KKKbbbbK",
    "     KbbbK",
    "    KJJbbK",
    "    KJJbbbK",
    "   KJJJbbbK",
    "   KJJJbbbK",
    "   KJJJbbbKK",
    "   KNJJbbbKbK",
    "   KNJJbbKbbK",
    "    KNNbbKbbK",
    "     KbbK KbbK",
    "      KYK  KbbK",
    "      KYK   KKK",
    "      KYK",
    "     KYYK",
    "",
    "",
])

# ------------------------------------------------------------------ GAUGE (npc_blue): a hare
GAUGE_FRONT = H([
    "    KK",       # long ears, up
    "   KsSK",
    "   KsSK",
    "   KsSK",
    "   KssK",
    "   KKsKK",
    "  Ksssss",
    "  KsKsss",     # the earpiece beside a wide eye
    "  Ksssaa",     # a pale muzzle
    "   KKsaa",
    "  KKOOdd",     # an orange jacket open over a dark shirt
    " KOyOOdd",     # reflective stripes
    " KOOOOdd",
    " KOyOOdd",
    " KsKOOOd",     # paws
    "  KKOOOO",
    "   Kdddd",
    "   KddK",
    "   KddK",
    "   KddK",
    "   KddK",
    "  KeeeK",
    "  KKKKK",
])
GAUGE_FRONT = overlay(GAUGE_FRONT, 13, ["KKKK", "KvvK", "KKKK"], 11)           # the meter
GAUGE_BACK = H([
    "    KK",
    "   KssK",
    "   KssK",
    "   KssK",
    "   KssK",
    "   KKsKK",
    "  Ksssss",
    "  Ksssss",
    "  Ksssss",
    "   KKsss",
    "  KKOOOO",
    " KOyOOOO",
    " KOOyyyy",     # the stripe across his back
    " KOyOOOO",
    " KsKOOOO",
    "  KKOOOO",
    "   Kdddd",
    "   KddK",
    "   KddK",
    "   KddK",
    "   KddK",
    "  KeeeK",
    "  KKKKK",
])
GAUGE_BACK = overlay(GAUGE_BACK, 15, ["WW"], 7)                                # a white scut
GAUGE_SIDE = S([
    "      KK",
    "     KsSK",
    "     KsSK KK",
    "     KsSKKsK",
    "     KssKsK",
    "    KsssssK",
    "   KssssssK",
    "  KsKsssssK",
    "  KaasssssK",
    "   KKaassK",
    "     KOOdK",
    "    KOOOOdK",
    "    KOyOOOK",
    "   KsKOyOOK",
    "    KKOOOOK",
    "     KOOOOKWK",
    "     KddddK",
    "     KddddK",
    "     KdddK",
    "     KdddK",
    "     KdddK",
    "     KeeeeK",
    "     KKKKKK",
])

# ------------------------------------------------------------------ BASIN (npc_pink): a hippo
BASIN_FRONT = H([
    "",
    "",
    "   KgK",       # small ears
    "   KKKKK",
    "  Kggggg",
    "  KgKggg",
    " Kgggggg",
    " Kggggpp",     # a pink muzzle, not a band across her face
    " KgggpPp",     # its nostrils
    "  KKggpp",
    "  KKBccc",     # a pale blue tracksuit, navy trim
    " KccccKw",     # the whistle on its cord
    "Kccccccc",
    "KgKccccc",     # grey paws
    "KgKBBBBB",
    " KKccccc",
    "  Kccccc",
    "  KWcccc",     # the white stripe down each leg
    "  KWcccK",
    "  KWcccK",
    "  KWccK",
    "  KnnnK",
    "  KKKKK",
])
BASIN_BACK = H([
    "",
    "",
    "   KgK",
    "   KKKKK",
    "  Kggggg",
    "  Kggggg",
    " Kgggggg",
    " Kgggggg",
    " KGggggg",
    "  KKgggg",
    "  KKBccc",
    " Kcccccc",
    "Kccccccc",
    "KgKccccc",
    "KgKBBBBB",
    " KKccccc",
    "  Kccccc",
    "  KWcccc",
    "  KWcccK",
    "  KWcccK",
    "  KWccK",
    "  KnnnK",
    "  KKKKK",
])
BASIN_BACK = overlay(BASIN_BACK, 15, ["gg"], 7)                                # a short tail
BASIN_SIDE = S([
    "",
    "       KK",
    "      KgK",
    "    KKKgggK",
    "   KgKgggggK",
    " KpppgggggggK",
    "KpPpppgggggK",
    " KpppppggggK",
    "  KKKKgggK",
    "    KBccccK",
    "   KccccccK",
    "   KccwccccK",
    "  KgKcccccccK",
    "  KKccccccccK",
    "   KBBBBBBBKgK",
    "   KcccccccKK",
    "   KWccccccK",
    "   KWcccccK",
    "   KWcccccK",
    "   KWccccK",
    "   KWccccK",
    "   KnnnnnK",
    "   KKKKKKK",
])

# ------------------------------------------------------------------ ANNEAL (npc_white): a salamander
ANNEAL_FRONT = H([
    "",
    "    KKKK",
    "   KwwKG",     # goggles, pushed up
    "  KGGGGG",
    "  KGRGGG",     # orange spots on charcoal
    "  KGTKGG",     # an amber eye
    "  KGGGGR",
    "  KGGGGG",
    "   KKGGG",
    "   KwKGG",     # a silver apron over dark clothes
    "  KGwwww",
    " KGRwwww",
    " KGGwwww",
    " KGKTwww",     # the glove glows
    "  KKwwww",
    "   Kwwgw",
    "   Kwwww",
    "   Kwwgw",
    "   KGGGK",
    "   KGGK",
    "   KGGK",
    "  KGGGK",
    "  KKKKK",
])
ANNEAL_FRONT = overlay(ANNEAL_FRONT, 15, [" KK", "KGK", "KGRK", "KGK", " KGK", "  KK"], 0)   # the tail
ANNEAL_BACK = H([
    "",
    "    KKKK",
    "   KwwKG",
    "  KGGGGG",
    "  KGGRGG",
    "  KGGGGG",
    "  KGRGGG",
    "  KGGGGR",
    "   KKGGG",
    "   KwKGG",
    "  KGGwKG",     # the apron's straps
    " KGRGGGG",
    " KGGGGRG",
    " KGKGGGG",
    "  KKwwKG",
    "   KGGGG",
    "   KGRGG",
    "   KGGGG",
    "   KGGGK",
    "   KGGK",
    "   KGGK",
    "  KGGGK",
    "  KKKKK",
])
ANNEAL_BACK = overlay(ANNEAL_BACK, 14, ["KGGK", "KGRK", "KGGK", "KRGK", "KGGK", " KK "], 6)
ANNEAL_SIDE = S([
    "",
    "     KKKKK",
    "    KwwKGGK",
    "   KGGGGGGK",
    "  KGTKGRGGK",
    " KGGGGGGGGK",
    " KKKGGGGGK",
    "    KKGGGK",
    "     KwGGK",
    "    KwwwGGK",
    "    KwwwwGK",
    "   KGKwwwwK",
    "   KTKwwwwK",
    "    KwwwwwK",
    "    KwwgwwKKK",
    "    KwwwwwKGGK",
    "    KGGGGKKRGK",
    "    KGGGGK KGGK",
    "    KGGGK   KRK",
    "    KGGGK    KK",
    "    KGGGK",
    "    KGGGGK",
    "    KKKKKK",
])

# name, sheet, frames, letters, palette, graphics info, tag, slot
LEADERS = [
    ("cairn",   "brock.png",    figure(CAIRN_FRONT, CAIRN_BACK, CAIRN_SIDE, still=True),       WHITE, "npc_white.pal", "Brock",    "WHITE", 4),
    ("basin",   "misty.png",    figure(BASIN_FRONT, BASIN_BACK, BASIN_SIDE, still=True),       PINK,  "npc_pink.pal",  "Misty",    "PINK",  2),
    ("gauge",   "lt_surge.png", figure(GAUGE_FRONT, GAUGE_BACK, GAUGE_SIDE, still=True),       BLUE,  "npc_blue.pal",  "LtSurge",  "BLUE",  1),
    ("trellis", "erika.png",    figure(TRELLIS_FRONT, TRELLIS_BACK, TRELLIS_SIDE, still=True), GREEN, "npc_green.pal", "Erika",    "GREEN", 3),
    ("tilt",    "koga.png",     figure(TILT_FRONT, TILT_BACK, TILT_SIDE, still=True),          GREEN, "npc_green.pal", "Koga",     "GREEN", 3),
    ("matte",   "sabrina.png",  figure(MATTE_FRONT, MATTE_BACK, MATTE_SIDE, still=True),       GREEN, "npc_green.pal", "Sabrina",  "GREEN", 3),
    ("anneal",  "blaine.png",   figure(ANNEAL_FRONT, ANNEAL_BACK, ANNEAL_SIDE, still=True),     WHITE, "npc_white.pal", "Blaine",   "WHITE", 4),
    ("scorn",   "giovanni.png", figure(SCORN_FRONT, SCORN_BACK, SCORN_SIDE),                   WHITE, "npc_white.pal", "Giovanni", "WHITE", 4),
]


def move_slots():
    """Point each leader's graphics info at the slot whose colours it was drawn from."""
    path = os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")
    s = open(path).read()
    for name, _, _, _, _, info, tag, slot in LEADERS:
        head = "const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = {" % info
        assert s.count(head) == 1, info
        start = s.index(head); end = s.index("};", start)
        block = s[start:end]
        block2, n1 = re.subn(r"\.paletteTag = OBJ_EVENT_PAL_TAG_NPC_\w+,", ".paletteTag = OBJ_EVENT_PAL_TAG_NPC_%s," % tag, block)
        block2, n2 = re.subn(r"\.paletteSlot = PALSLOT_NPC_\w+,", ".paletteSlot = PALSLOT_NPC_%d," % slot, block2)
        assert n1 == 1 and n2 == 1, info
        s = s[:start] + block2 + s[end:]
    open(path, "w").write(s)


def main():
    rows, built = [], []
    for name, filename, frames, index, palname, _, _, _ in LEADERS:
        check(name, frames, index)
        img = sheet(frames, index, read_pal(palname))
        built.append((filename, img))
        rgb = img.convert("RGB")
        bg = Image.new("RGB", rgb.size, (150, 150, 150))
        bg.paste(rgb, (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        old = Image.open(os.path.join(PEOPLE, filename)).convert("RGB")
        pair = Image.new("RGB", (144 + 8 + old.width, 32), (60, 60, 60))
        pair.paste(bg, (0, 0)); pair.paste(old, (152, 0))
        rows.append(pair)
    out = Image.new("RGB", (max(r.width for r in rows) * 6, 32 * 6 * len(rows)), (60, 60, 60))
    for i, r in enumerate(rows):
        out.paste(r.resize((r.width * 6, 192), Image.NEAREST), (0, 192 * i))
    out.save(PREVIEW)
    print("  %d leaders -> preview %s (each row: ours on grey, then what is on disk)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img in built:
            img.save(os.path.join(PEOPLE, filename), bits=4)
            print("  written people/%s" % filename)
        move_slots()
        print("  palette slots moved in object_event_graphics_info.h")


if __name__ == "__main__":
    main()

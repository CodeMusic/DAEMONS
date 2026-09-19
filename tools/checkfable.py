#!/usr/bin/env python3
"""A trainer's two pictures are ONE animal (vision.md 9.4; T-169).

    python3 tools/checkfable.py    # every trainer on a map: its overworld sheet, its portrait, both animals; exits 1 if any differ

WHY. The fable's actors are animals, and a player meets each trainer twice: walking on the map, then in the battle
portrait. T-120 made a class's sheet and portrait one species on purpose and T-128 matched the couples to the
sheets they stand on -- but nothing checked it, and at 16px a sheet's animal cannot be read off its pixels. So the
animals are READ FROM THE RECORDS: a portrait's from `gbachar.py`'s job comment ("# a hedgehog, as her sheet is"),
a sheet's from the table below, which is transcribed from the tools that drew them (gentrainers.py, genodd.py,
genleaders.py) and from T-116/T-118/T-120/T-126/T-128. A sheet not in the table is reported, not guessed.

A PAIR MATCHES when the sheet's animal is named in the portrait's comment -- a couple's portrait names both of its
animals, and each of its two sheets need only be one of them.
"""
import json, glob, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")

#  OBJ_EVENT_GFX_<sheet> -> the animal it was drawn as
SHEET = {
    "HIKER": "badger", "FISHER": "pelican", "CHANNELER": "bat", "PICNICKER": "hedgehog", "BUG_CATCHER": "swallow",
    "YOUNGSTER": "mouse", "LASS": "lamb", "ROCKER": "skunk", "SAILOR": "albatross",
    "LITTLE_GIRL": "piglet", "TUBER_M_WATER": "duckling", "TUBER_F": "cygnet", "BIKER": "boar",
    "GENTLEMAN": "lynx", "SWIMMER_M_WATER": "newt", "SWIMMER_M_LAND": "newt", "MAN": "ox", "BLACK_BELT": "kangaroo",
    "CRUSH_GIRL": "wolverine", "SWIMMER_F_WATER": "axolotl", "SWIMMER_F_LAND": "axolotl", "CAMPER": "raccoon",
    "BEAUTY": "gazelle", "COOLTRAINER_M": "wolf", "COOLTRAINER_F": "falcon", "POKE_MANIAC": "opossum",
    "AROMA_LADY": "honeybee", "BIRD_KEEPER": "ostrich", "BURGLAR": "weasel", "CUE_BALL": "rhinoceros",
    "ENGINEER": "beaver", "GAMER": "jackal", "JUGGLER": "octopus", "LADY": "swan", "PAINTER": "toucan",
    "POKEMON_BREEDER": "goose", "PSYCHIC_F": "jellyfish", "RUIN_MANIAC": "aardvark", "SUPER_NERD": "lemur",
    "TAMER": "hyena", "SCIENTIST": "mole",
}
#  and genclasses.py's own table, read rather than copied: ("RUIN_MANIAC", "aardvark", ...) -- the second word of a
#  two-word animal ("pine marten") is the one a portrait comment is matched on
#  PSYCHIC_M's portrait is written by genpsychic.py from psychic_f's: the same jellyfish (T-126)
PORTRAIT_EXTRA = {"psychic_m": "the same jellyfish, from genpsychic.py (T-126)"}

ANIMAL = re.compile(r"\b(?:an?|two|the same)\s+(?:young\s+|old\s+|ring-tailed\s+|pine\s+|polar\s+)?([a-z]+)", re.I)


def sheets():
    out = dict(SHEET)
    src = open(os.path.join(ROOT, "tools/genclasses.py")).read()
    for sheet, animal in re.findall(r'\(\s*"([A-Z_0-9]+)",\s*"([a-z -]+)",', src):
        out[sheet] = animal.split()[-1]
    return out


def portraits():
    """front-pic file stem -> the words of its gbachar.py job comment, or its source file's name when it has none
    (the hiker's job is uncommented, and its source is portrait_hiker_badger.png)"""
    s = open(os.path.join(ROOT, "tools/gbachar.py")).read()
    out = dict(PORTRAIT_EXTRA)
    for m in re.finditer(r'dict\(src="([^"]+)",\s*(?:#\s*([^\n]*))?\n\s*dst="engineGba/graphics/trainers/front_pics/(\w+)_front_pic\.png"', s):
        words = (m.group(2) or "").strip()
        if not words:
            stem = os.path.splitext(os.path.basename(m.group(1)))[0].split("_")
            words = "a " + stem[-1] if len(stem) > 2 else ""
        out[m.group(3)] = words
    return out


def pairs():
    tr = open(os.path.join(E, "src/data/trainers.h")).read()
    pic = dict(re.findall(r"\[(TRAINER_\w+)\]\s*=\s*\{.*?\.trainerPic = (TRAINER_PIC_\w+)", tr, re.S))
    g2f = dict(re.findall(r'(gTrainerFrontPic_\w+)\[\]\s*=\s*INCBIN_U32\("graphics/trainers/front_pics/(\w+)_front_pic\.4bpp',
                          open(os.path.join(E, "src/data/graphics/trainers.h")).read()))
    c2g = dict(re.findall(r"TRAINER_SPRITE\((\w+),\s*(gTrainerFrontPic_\w+)",
                          open(os.path.join(E, "src/data/trainer_graphics/front_pic_tables.h")).read()))
    text = "".join(open(f).read() + "\n" for f in glob.glob(os.path.join(E, "data/scripts/*.inc")) + glob.glob(os.path.join(E, "data/maps/*/scripts.inc")))
    labels = {m.group(1): m.group(2) for m in re.finditer(r"^(\w+)::\n(.*?)(?=^\w+::|\Z)", text, re.S | re.M)}
    out = defaultdict(set)
    for mj in glob.glob(os.path.join(E, "data/maps/*/map.json")):
        for o in json.load(open(mj)).get("object_events", []):
            t = re.search(r"trainerbattle\w*\s+(?:\w+,\s*)?(TRAINER_\w+)", labels.get(o.get("script", ""), ""))
            if t and t.group(1) in pic:
                f = g2f.get(c2g.get(pic[t.group(1)][len("TRAINER_PIC_"):], ""), "?")
                out[(o["graphics_id"][len("OBJ_EVENT_GFX_"):], f)].add(mj.split(os.sep)[-2])
    return out


def main():
    notes, SHEETS = portraits(), sheets()
    bad, unknown, ok = [], [], 0
    for (sheet, pic), maps in sorted(pairs().items()):
        words = notes.get(pic, "")
        named = [w.lower().rstrip("s") if w.lower().endswith("lets") or w.isupper() else w.lower() for w in ANIMAL.findall(words)]
        animal = SHEETS.get(sheet)
        if sheet.startswith(("STAFF_", "ROCKET_")) or sheet in ("BROCK", "MISTY", "LT_SURGE", "ERIKA", "KOGA", "SABRINA", "BLAINE", "GIOVANNI"):
            ok += 1                   # drawn FROM the portrait by the leaders' and staff tools: one drawing, two sizes
            continue
        if animal is None or not named:
            unknown.append((sheet, pic, animal, words, len(maps)))
        elif animal in named:
            ok += 1
        else:
            bad.append((sheet, pic, animal, words, len(maps)))
    for sheet, pic, animal, words, n in bad:
        print("  DIFFER   %-18s (%s)  vs  %-22s (%s)   %d maps" % (sheet, animal, pic, words[:50], n))
    for sheet, pic, animal, words, n in unknown:
        print("  UNREAD   %-18s (%s)  vs  %-22s (%s)   %d maps" % (sheet, animal or "no record", pic, words[:50] or "no comment", n))
    print("  %d pairs one animal, %d differ, %d unread" % (ok, len(bad), len(unknown)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

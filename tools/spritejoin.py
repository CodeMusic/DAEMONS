#!/usr/bin/env python3
"""Does the sprite you walk up to battle as the animal it is? (T-126; vision.md 9.4).

    python3 tools/spritejoin.py             # the census, and every disagreement
    python3 tools/spritejoin.py --pairs     # every pairing, agreeing or not

9.4 says a class's overworld sheet and its battle portrait are ONE species. Nothing in the engine
enforces that, because vanilla had no reason to: it reused one generic human sheet across a dozen
classes and the reuse was invisible while they were all people. Drawn as animals it is not.

THE ONLY TEST THAT MEANS ANYTHING IS THE ONE THE PLAYER MAKES -- walk up to an object, get a battle,
see a picture -- so this joins the engine end to end rather than reading any tool's comments:

    trainers.h            .trainerPic gives each trainer its portrait
    every *.inc           a script label that runs `trainerbattle` gives that label its trainer
    every map.json        an object names the script it runs, and the sheet it stands on

and then puts each side's SPECIES against the other, read out of the tools that drew them -- the
`(species, sheet)` tables in the gen* tools, and the note on each portrait job in `gbachar.py`.

***THE FIRST RUN OF THIS JOIN READ A THIRD OF THE EVIDENCE AND LOOKED COMPLETE.*** It globbed
`data/maps/*/scripts.inc` -- 258 labels -- and reported 38 pairings and five disagreements. But
`data/scripts/trainers.inc` is ONE shared file holding 468 more, which is every route and island
trainer in the game: the real numbers are 726 labels, 72 pairings and about twenty disagreements.
A narrow join does not fail. It returns a clean, plausible, wrong answer, and the fix that follows
it is correspondingly partial -- T-126 repointed ten objects out of roughly a hundred.

So this file prints WHAT IT EXAMINED before what it found, every time, and globs `data/**/*.inc`.

PAIR CLASSES ARE JUDGED, NOT MATCHED. TWINS, YOUNG_COUPLE, SIS_AND_BRO, CRUSH_KIN and COOL_COUPLE
are one trainer standing as TWO objects, so "same species" is the wrong question -- the portrait has
to be the two animals those two sheets are. They are listed separately, with both sides shown.
"""
import collections, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
TOOLS = os.path.dirname(os.path.abspath(__file__))
SHOW_ALL = "--pairs" in sys.argv

# the sheets a pair class is standing as, and therefore what its picture has to be
PAIRS = {"TWINS", "YOUNG_COUPLE", "SIS_AND_BRO", "CRUSH_KIN", "COOL_COUPLE", "SR_AND_JR", "OLD_COUPLE"}
# one animal, two poses -- a class's land and water sheets are the same creature
SAME = {"axolotl swimming": "axolotl", "newt swimming": "newt", "old ram": "ram", "bear cub": "bear"}
# the sheet and the portrait are the same class under different file names. Vanilla named them, not
# us, and the names disagree in both directions -- `fisher.png` serves TRAINER_PIC_FISHERMAN, and
# the BENCHMARK leaders' sheets are named for the LEADER while their pictures are `leader_*`.
ALIAS = {"fisher": "fisherman", "poke_maniac": "pokemaniac", "swimmer_m_land": "swimmer_m",
         "swimmer_m_water": "swimmer_m", "swimmer_f_land": "swimmer_f", "swimmer_f_water": "swimmer_f",
         "tuber_m_water": "tuber_m", "tuber_m_land": "tuber_m", "rocket_m": "rocket_grunt_m",
         "rocket_f": "rocket_grunt_f", "brock": "leader_brock", "misty": "leader_misty",
         "lt_surge": "leader_lt_surge", "erika": "leader_erika", "koga": "leader_koga",
         "sabrina": "leader_sabrina", "blaine": "leader_blaine", "giovanni": "leader_giovanni"}


def cls(name):
    n = name.lower()
    return ALIAS.get(n, n)


def norm(s):
    """the animal out of a note. A note may lead with the town or the role -- "CALLOW's staff,
    cheerful penguins" -- so an article is looked for anywhere, not only at the front."""
    s = (s or "").strip().lower()
    m = re.search(r"\b(?:a|an|two)\s+([a-z][a-z -]*)", s)
    s = m.group(1) if m else s
    s = re.split(r"[,:;.]| in | with | and | as | that | who | keeping | clipped | framing | -- ", s)[0]
    s = " ".join(w for w in s.split() if w not in
                 ("cheerful", "tailless", "poison", "dart", "young", "ring-tailed", "pine", "lab", "polar"))
    s = s.strip()
    if s.endswith("es") and not s.endswith("sses"):
        s = s[:-2] if s[-3:-2] in "shx" else s[:-1]
    elif s.endswith("s") and not s.endswith("ss"):
        s = s[:-1]
    return SAME.get(s, s)


def sheet_species():
    """(species, sheet.png) as the gen* tools themselves declare it -- read, never imported (trap 16)"""
    out = {}
    for f in sorted(glob.glob(os.path.join(TOOLS, "gen*.py"))):
        src = open(f).read()
        # ("skunk", "rocker.png", ...) -- the shape gentrainers, genfolk, genodd and gennamed use
        for species, sheet in re.findall(r'\(\s*"([^"]+)"\s*,\s*"([a-z0-9_]+)\.png"', src):
            if "." in species or "/" in species:
                continue          # ("cooltrainer_m.png", "cooltrainer_f.png") is a pair of FILES, not a species
            out.setdefault(sheet, species)
        # ("BURGLAR", "weasel", ART, "burglar", ...) -- genclasses declares the class first
        for _cls, species, fname in re.findall(
                r'\(\s*"([A-Z][A-Z_]+)"\s*,\s*"([a-z ]+)"\s*,\s*\w+\s*,\s*"([a-z0-9_]+)"', src):
            out.setdefault(fname, species)
    return out


def portrait_species():
    """the note on each front-pic job in gbachar.py -- the species is written there and nowhere else"""
    s = open(os.path.join(TOOLS, "gbachar.py")).read()
    out = {}
    for m in re.finditer(r'dict\(src="gfx/characters/[^"]+",\s*(#[^\n]*)?\n\s*'
                         r'dst="engineGba/graphics/trainers/front_pics/(\w+)_front_pic\.png"', s):
        out[m.group(2).upper()] = (m.group(1) or "").lstrip("# ").strip()
    return out


def trainer_pics():
    out = {}
    for m in re.finditer(r"\[(TRAINER_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \}",
                         open(os.path.join(GBA, "src/data/trainers.h")).read(), re.S):
        p = re.search(r"\.trainerPic\s*=\s*TRAINER_PIC_([A-Z0-9_]+)", m.group(2))
        if p:
            out[m.group(1)] = p.group(1)
    return out


def battle_labels():
    """EVERY script label that starts a battle, from EVERY .inc -- see the docstring"""
    out, files = {}, sorted(glob.glob(os.path.join(GBA, "data/**/*.inc"), recursive=True))
    for f in files:
        for m in re.finditer(r"^(\w+)::\s*\n(.*?)(?=^\w+::|\Z)", open(f, errors="ignore").read(), re.S | re.M):
            t = re.search(r"trainerbattle\w*\s+(TRAINER_[A-Z0-9_]+)", m.group(2))
            if t:
                out[m.group(1)] = t.group(1)
    return out, len(files)


def census():
    pics, (labels, nfiles) = trainer_pics(), battle_labels()
    sheets, portraits = sheet_species(), portrait_species()
    rows, objs, maps = [], 0, 0
    for mp in sorted(glob.glob(os.path.join(GBA, "data/maps/*/map.json"))):
        events = json.load(open(mp)).get("object_events", [])
        maps += 1
        for i, o in enumerate(events):
            objs += 1
            t = labels.get(o.get("script"))
            if t not in pics:
                continue
            g = o.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
            sheet = g.lower()
            rows.append(dict(map=os.path.basename(os.path.dirname(mp)), i=i, gfx=g, pic=pics[t],
                             sheet_sp=sheets.get(sheet, ""), pic_sp=portraits.get(pics[t], "")))
    return rows, dict(files=nfiles, labels=len(labels), trainers=len(pics), objects=objs, maps=maps,
                      sheets=len(sheets), portraits=len(portraits))


def main():
    rows, seen = census()
    print("  examined: %d trainers, %d .inc files holding %d battle labels, %d objects across %d maps;"
          % (seen["trainers"], seen["files"], seen["labels"], seen["objects"], seen["maps"]))
    print("            %d sheets and %d portraits carry a declared species" % (seen["sheets"], seen["portraits"]))
    pair = collections.Counter()
    for r in rows:
        pair[(r["gfx"], r["sheet_sp"], r["pic"], r["pic_sp"])] += 1
    print("  %d objects start a battle, on %d distinct (sheet, portrait) pairings\n" % (len(rows), len(pair)))

    agree, differ, pairs = [], [], []
    for k, n in pair.items():
        gfx, ssp, pic, psp = k
        if pic in PAIRS:
            # A PAIR's note names TWO animals, so the question is whether this sheet's animal is one
            # of them -- membership, not equality. Anything the note does not account for is a real
            # disagreement and is reported as one.
            pairs.append((k, n, bool(ssp) and norm(ssp) in {norm(w) for w in re.split(r"\band\b|,", psp or "")}))
        elif cls(gfx) == cls(pic) or (ssp and psp and norm(ssp) == norm(psp)):
            # THE TEST IS EITHER, AND THAT IS THE POINT. Matching NAMES alone reported 47 CORPUS
            # STAFF trainers as mismatched, because their portraits are filed under the job name and
            # not the convention. Matching SPECIES alone reported every town's staff against itself,
            # because one side's note leads with the town. A disagreement has to fail both.
            agree.append((k, n))
        else:
            differ.append((k, n))
    blind = [i for i in differ if not i[0][1] or not i[0][3]]
    show = lambda t: sorted(t, key=lambda i: -i[1])

    def dump(title, items):
        if not items:
            return
        print("%s (%d pairings, %d objects)" % (title, len(items), sum(i[1] for i in items)))
        for item in show(items):
            (gfx, ssp, pic, psp), n = item[0], item[1]
            mark = "" if len(item) < 3 else ("   accounted for" if item[2] else "   *** NOT IN THE PICTURE ***")
            print("  %-20s %-18s battles as %-20s %-22s x%d%s" % (gfx, ssp or "?", pic, psp or "?", n, mark))
        print()

    dump("DISAGREE -- the sprite and the picture are different animals", differ)
    dump("PAIR CLASSES -- one trainer, two objects; judged, not matched", pairs)
    dump("...of those, ones where a side declares NO SPECIES, so only the names were compared", blind)
    if SHOW_ALL:
        dump("AGREE", agree)
    else:
        print("AGREE: %d pairings, %d objects (--pairs to list)" % (len(agree), sum(i[1] for i in agree)))


if __name__ == "__main__":
    main()

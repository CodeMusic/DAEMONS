#!/usr/bin/env python3
"""T-120, the last trainer portraits: Hoenn's, which nobody can meet -- redrawn anyway, so no Nintendo art stays in.

    python3 tools/t120hoenn.py draft [NAME ...]   # draw two seeds of each on spriteforge into gfx/drafts/t120hoenn/
    python3 tools/t120hoenn.py sheet OUT.png       # the drafts side by side with the FireRed portrait they come from

GROUP 1 (the user, 2026-10-11: "redraw from our FireRed portrait", this group first): the 28 Hoenn copies of classes
FireRed already has. A class is one animal (T-120), so each takes its FireRed twin's -- drawn image to image from OUR
FireRed drawing of that class, in the Hoenn class's own outfit, so every picture is new and the family holds.
Picks go into tools/gbachar.py as jobs like any portrait; these 81 are on screen nowhere (e-Reader only).
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "gfx/drafts/t120hoenn"
SEEDS = (13001, 13002)
DENOISE = 0.62
STYLE = ("anthropomorphic animal, full body standing, facing the viewer, simple flat colours, clean outlines, "
         "game character portrait, plain white background")
NEG = "text, watermark, frame, border, scenery, background objects, human face, multiple characters"

#  Hoenn picture -> (our FireRed job in gbachar.py it is drawn from, what it is)
GROUP1 = {
    "rs_aroma_lady":         ("p_aroma",         "a honeybee woman in a long flowing flower-print dress, a flower in her hair"),
    "rs_beauty":             ("p_beauty",        "a gazelle woman in a sleek red evening dress"),
    "rs_bird_keeper":        ("p_birdkeeper",    "an ostrich in a safari vest and cap, a bird whistle on a cord"),
    "rs_black_belt":         ("p_blackbelt",     "a kangaroo in a white karate gi with a black belt and a headband"),
    "rs_bug_catcher":        ("bugcatcher",      "a young swallow in a straw hat and shorts, holding a bug net"),
    "rs_camper":             ("p_camper",        "a young raccoon in a scout shirt, shorts and a cap"),
    "rs_cool_trainer_f":     ("p_cooltrainer_f", "a falcon woman in a sporty top and a short skirt"),
    "rs_cool_trainer_m":     ("p_cooltrainer_m", "a wolf man in a sleeveless sporty jacket"),
    "rs_fisherman":          ("p_fisherman",     "a pelican in a rain hat and waders, holding a fishing rod"),
    "rs_gentleman":          ("p_gentleman",     "a lynx gentleman in a tailcoat and top hat with a cane"),
    "rs_hiker":              ("hiker",           "a badger hiker with a big backpack and a mountain cap"),
    "rs_lady":               ("p_lady",          "a young swan girl in a frilly party dress"),
    "rs_lass":               ("p_lass",          "a lamb girl in a school blouse and skirt"),
    "rs_picnicker":          ("picnicker",       "a hedgehog girl in a sun hat and overalls"),
    "rs_pokemaniac":         ("p_pokemaniac",    "an opossum wearing a monster costume hood"),
    "rs_pokemon_breeder_f":  ("p_breeder",       "a goose woman in an apron"),
    "rs_pokemon_breeder_m":  ("p_breeder",       "a goose man in an apron"),
    "rs_pokemon_ranger_f":   ("p_ranger_f",      "a pine marten woman in a park ranger uniform and hat"),
    "rs_pokemon_ranger_m":   ("p_ranger_m",      "a pine marten man in a park ranger uniform and hat"),
    "rs_psychic_f":          ("p_psychic_f",     "a jellyfish woman in a long robe"),
    "rs_psychic_m":          ("p_psychic_f",     "a jellyfish man in a long violet robe"),
    "rs_ruin_maniac":        ("p_ruinmaniac",    "an aardvark explorer in a pith helmet with a pickaxe"),
    "rs_sailor":             ("p_sailor",        "an albatross in a sailor's uniform and cap"),
    "rs_sis_and_bro":        ("p_sisandbro",     "a duckling boy and an axolotl girl side by side, in swimwear"),
    "rs_swimmer_f":          ("p_swimmer_f",     "an axolotl woman in a swimsuit and swim cap"),
    "rs_swimmer_m":          ("p_swimmer_m",     "a newt man in swim trunks and goggles"),
    "tuber_m":               ("p_tuber_f",       "a duckling boy in swim trunks with a swim ring"),
    "rs_twins":              ("p_twins",         "two identical twin girls side by side, the same animal, matching outfits"),
    "rs_young_couple":       ("p_youngcouple",   "an ox man and a gazelle woman side by side, holding hands"),
}


def source(job):
    s = open(os.path.join(ROOT, "tools/gbachar.py")).read()
    return re.search(r'"%s":\s*dict\(src="([^"]+)"' % re.escape(job), s).group(1)


def draft(names):
    for name in names or GROUP1:
        job, what = GROUP1[name]
        for seed in SEEDS:
            out = "%s/%s_%d" % (OUT, name, seed)
            if os.path.exists(os.path.join(ROOT, out + ".png")):
                continue
            r = subprocess.run([sys.executable, "tools/spriteforge.py", "i2i", "--out", out, "--image", source(job),
                                "--prompt", "%s, %s" % (what, STYLE), "--negative", NEG, "--seed", str(seed),
                                "--denoise", str(DENOISE)], cwd=ROOT, capture_output=True, text=True)
            print("  %-24s %d %s" % (name, seed, "ok" if r.returncode == 0 else "FAILED " + r.stderr[-200:]), flush=True)


def sheet(out):
    from PIL import Image, ImageDraw
    rows = list(GROUP1.items())
    W = 3 * 200 + 20
    img = Image.new("RGB", (W * 2, (len(rows) + 1) // 2 * 220 + 10), (24, 24, 32))
    d = ImageDraw.Draw(img)
    for k, (name, (job, what)) in enumerate(rows):
        x0, y0 = (k % 2) * W + 5, (k // 2) * 220 + 5
        tiles = [source(job)] + ["%s/%s_%d.png" % (OUT, name, s) for s in SEEDS]
        for i, p in enumerate(tiles):
            p = os.path.join(ROOT, p)
            if os.path.exists(p):
                im = Image.open(p).convert("RGB")
                im.thumbnail((190, 190))
                img.paste(im, (x0 + i * 200, y0 + 18))
        d.text((x0, y0 + 2), "%s  (from %s; %d / %d)" % (name, job, SEEDS[0], SEEDS[1]), fill="white")
    img.save(out)


if __name__ == "__main__":
    if sys.argv[1:2] == ["draft"]:
        draft(sys.argv[2:])
    elif sys.argv[1:2] == ["sheet"]:
        sheet(sys.argv[2])
    else:
        sys.exit(__doc__)

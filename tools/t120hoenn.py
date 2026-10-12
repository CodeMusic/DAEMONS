#!/usr/bin/env python3
"""T-120, the last trainer portraits: Hoenn's, which nobody can meet -- redrawn anyway, so no Nintendo art stays in.

    python3 tools/t120hoenn.py draft [NAME ...]   # draw two seeds of each on spriteforge into gfx/drafts/t120hoenn/
    python3 tools/t120hoenn.py sheet OUT.png       # the drafts side by side with the FireRed portrait they come from
    python3 tools/t120hoenn.py draft2 [NAME ...]  # GROUP 2: two seeds of each, over a Group 1 portrait
    python3 tools/t120hoenn.py sheet2 OUT.png      # GROUP 2's drafts side by side
    python3 tools/t120hoenn.py draft3|sheet3 ...   # GROUP 3, the same way
    python3 tools/t120hoenn.py redraw3|resheet3 ... # GROUP 3's redraws, three seeds each
    python3 tools/t120hoenn.py magmared            # MAGMA's five picks into MAGMA red (from magma_pre_red/, idempotent)

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
    "rs_tuber_f":            ("p_tuber_f",       "a cygnet girl in a swimsuit with a swim ring"),
    "rs_twins":              ("p_twins",         "two identical twin girls side by side, the same animal, matching outfits"),
    "rs_young_couple":       ("p_youngcouple",   "an ox man and a gazelle woman side by side, holding hands"),
}

# GROUP 2 (the user, 2026-10-11: "start group 2"): Hoenn classes FireRed has no twin for. Text to image drew them
# chunkier and less upright than the family (tried: a flamingo, 2026-10-11), so each is drawn image to image over a
# GROUP 1 portrait of a similar build at a high denoise -- a new animal, the family's stance and line. Hoenn name ->
# (the Group 1 pick it is drawn over, what it is). The animals are PROPOSALS (2026-10-11), drafted so the user can judge
# them as pictures; the two rival teams' grunts, admins and leaders are the user's to choose and are not here.
G2DENOISE = 0.85
GROUP2 = {
    "parasol_lady":             ("rs_beauty", "a flamingo woman in a sun dress holding a parasol"),
    "interviewer":              ("rs_young_couple", "a parrot reporter holding a microphone and a parrot camera operator with a video camera, side by side"),
    "rich_boy":                 ("rs_bug_catcher", "a young peacock boy in a fancy suit with a bow tie, tail feathers fanned"),
    "ninja_boy":                ("rs_bug_catcher", "a stick insect boy in a ninja outfit and headband"),
    "kindler":                  ("rs_black_belt", "a fire hawk man, a black kite bird, bare-chested in a sash, holding a torch"),
    "collector":                ("rs_hiker", "a packrat man with a big satchel full of trinkets"),
    "hex_maniac":               ("rs_lady", "a raven woman in a long dark hooded dress"),
    "guitarist":                ("rs_cool_trainer_m", "a howler monkey man in a leather jacket with an electric guitar"),
    "bug_maniac":               ("rs_ruin_maniac", "a chameleon man in a bug-collecting outfit with a net and jars"),
    "school_kid_m":             ("rs_camper", "a young koala boy in a school uniform with a satchel"),
    "school_kid_f":             ("rs_lass", "a young koala girl in a school uniform with a satchel"),
    "sr_and_jr":                ("rs_sis_and_bro", "two hare women side by side, a tall older one and a small younger one, matching outfits"),
    "pokefan_m":                ("rs_gentleman", "a meerkat man in a fan club shirt"),
    "pokefan_f":                ("rs_aroma_lady", "a meerkat woman in a fan club dress"),
    "expert_m":                 ("rs_gentleman", "an old orangutan man in a martial arts robe"),
    "expert_f":                 ("rs_lady", "an old orangutan woman in a martial arts robe"),
    "cycling_triathlete_m":     ("rs_swimmer_m", "a jaguar man in a cycling suit and helmet"),
    "cycling_triathlete_f":     ("rs_swimmer_f", "a jaguar woman in a cycling suit and helmet"),
    "running_triathlete_m":     ("rs_swimmer_m", "a jaguar man in running vest and shorts"),
    "running_triathlete_f":     ("rs_swimmer_f", "a jaguar woman in running vest and shorts"),
    "swimming_triathlete_m":    ("rs_swimmer_m", "a jaguar man in swim trunks and goggles"),
    "swimming_triathlete_f":    ("rs_swimmer_f", "a jaguar woman in a swimsuit and goggles"),
    "dragon_tamer":             ("rs_black_belt", "a monitor lizard man in a cape with a whip"),
    "battle_girl":              ("rs_swimmer_f", "a crane woman in a martial arts outfit"),
    "old_couple":               ("rs_young_couple", "an old elephant man and an old elephant woman side by side"),
}

# GROUP 3 (the user, 2026-10-12: "start group 3"): Hoenn's named people, drawn as GROUP 2 was. The animals are
# PROPOSALS, judged by the user as pictures -- except where the user chose (2026-10-12): BRENDAN and MAY are THE GREY
# MONKEY our own two are, in Hoenn's clothes, drawn over REASON's and INSTINCT's portraits; AQUA are SHARKS (ARCHIE a
# great white) and MAGMA are MOLES (MAXIE a star-nosed mole). A base with a / in it is a path, not a Group 1 pick.
GROUP3 = {
    "leader_roxanne":       ("rs_lass",           "a young tortoise woman with glasses in a school uniform, holding a book"),
    "leader_brawly":        ("rs_black_belt",     "a sea lion man in a surfer's rash vest and board shorts"),
    "leader_wattson":       ("rs_hiker",          "a jolly old platypus man in work overalls with a tool belt"),
    "leader_flannery":      ("rs_swimmer_f",      "a fire salamander young woman, black and orange, in a tank top and jeans"),
    "leader_norman":        ("rs_gentleman",      "a labrador dog father in a sweater vest and slacks"),
    "leader_winona":        ("rs_beauty",         "an osprey woman in a pilot's flight suit with a scarf"),
    "leader_tate_and_liza": ("rs_twins",          "two young twin lemurs side by side, a boy and a girl, matching outfits"),
    "leader_wallace":       ("rs_gentleman",      "a sea otter man in a flamboyant white cape and a fancy hat"),
    "elite_four_sidney":    ("guitarist",         "a spotted hyena punk in a leather vest"),
    "elite_four_phoebe":    ("rs_lass",           "a white barn owl girl in a simple dress with a bead necklace"),
    "elite_four_glacia":    ("rs_lady",           "an arctic fox woman in a long white coat"),
    "elite_four_drake":     ("rs_sailor",         "an old crocodile sea captain in a captain's coat"),
    "champion_steven":      ("rs_gentleman",      "a pangolin man in a sharp grey suit"),
    "wally":                ("rs_bug_catcher",    "a young fawn boy in a green shirt and shorts"),
    "ruby_sapphire_brendan": ("gfx/characters/player_logic.jpeg",
                              "a grey monkey boy in a white knit cap, an orange and black jacket and dark shorts, a long tail"),
    "ruby_sapphire_may":     ("gfx/characters/player_intuition.jpeg",
                              "a grey monkey girl in a red bandana, a red top and dark bike shorts, a long tail"),
    "aqua_grunt_m":         ("rs_cool_trainer_m", "a hammerhead shark man in a striped shirt, a blue bandana and dark trousers"),
    "aqua_grunt_f":         ("rs_swimmer_f",      "a hammerhead shark woman in a striped shirt, a blue bandana and dark trousers"),
    "aqua_admin_m":         ("rs_gentleman",      "a hammerhead shark man in a dark blue wetsuit and a captain's bandana"),
    "aqua_admin_f":         ("rs_beauty",         "a hammerhead shark woman in a dark blue wetsuit and a bandana"),
    "aqua_leader_archie":   ("rs_black_belt",     "a big great white shark man in a dark blue wetsuit, an anchor necklace and a bandana"),
    "magma_grunt_m":        ("rs_cool_trainer_m", "a mole man in a red hooded uniform with a hood up"),
    "magma_grunt_f":        ("rs_swimmer_f",      "a mole woman in a red hooded uniform with a hood up"),
    "magma_admin_m":        ("rs_gentleman",      "a mole man in a red and black uniform with a high collar"),
    "magma_admin_f":        ("rs_beauty",         "a mole woman in a red and black uniform with a high collar"),
    "magma_leader_maxie":   ("rs_gentleman",      "a star-nosed mole man with glasses in a red and black long coat"),
}

# GROUP 3's REDRAWS (the user, 2026-10-12: "redraw the nine"; FLANNERY "looks too person like"). FLANNERY drawn over
# the newt swimmer, already a salamander's shape; MAGMA over the badger hiker, a stocky digger, with the mole spelled
# out (the first drafts read as rats); ARCHIE and the AQUA admin over the AQUA grunt, whose shark fills the frame.
MOLE = "a mole with tiny eyes, a long pink pointed snout, velvety dark grey fur and huge pink digging claws"
REDRAW3 = {
    "leader_flannery":    ("rs_swimmer_m", "a fire salamander woman, glossy black skin with bright orange spots, a "
                           "salamander head with no hair, a long tail, wearing a tank top and baggy orange trousers"),
    "magma_grunt_m":      ("rs_hiker", MOLE + ", a man in a red hooded uniform with the hood up"),
    "magma_grunt_f":      ("rs_hiker", MOLE + ", a woman in a red hooded uniform with the hood up"),
    "magma_admin_m":      ("rs_hiker", MOLE + ", a man in a red and black uniform with a high collar"),
    "magma_admin_f":      ("rs_hiker", MOLE + ", a woman in a red and black uniform with a high collar"),
    "magma_leader_maxie": ("rs_hiker", "a star-nosed mole with a ring of pink tentacles on its nose, tiny eyes, velvety "
                           "dark fur, huge digging claws, round glasses, a red and black long coat"),
    "aqua_admin_m":       ("gfx/drafts/t120hoenn/g3_aqua_grunt_m_13002.png",
                           "a hammerhead shark man in a dark blue wetsuit and a captain's bandana"),
    "aqua_leader_archie": ("gfx/drafts/t120hoenn/g3_aqua_grunt_m_13002.png",
                           "a big burly great white shark man in a dark blue wetsuit, an anchor necklace and a bandana"),
}
RSEEDS = (13003, 13004, 13005)
RDENOISE = 0.80


def magma_red(path, coat=False):
    """MAGMA's uniforms came out grey-violet and magenta (the user, 2026-10-12: "fix the magma red"). Hot pink trim and
    violet cloth go to MAGMA red at their own brightness; the light pinks (snout, ears), dark fur and the ground shadow
    stay. MAXIE's coat is tan, so for him tan goes red too. The picks before this are in magma_pre_red/."""
    import numpy as np
    from PIL import Image
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float) / 255
    hsv = np.asarray(im.convert("HSV")).astype(float) / 255
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    notbg = np.sqrt(((a - a[5, 5]) ** 2).sum(-1)) > 0.06
    magenta = (h > 0.82) & (h < 0.97) & (s > 0.55) & notbg
    cloth = (h > 0.62) & (h < 0.82) & (s > 0.10) & (v > 0.40) & (v < 0.80) & notbg
    if coat:
        cloth = cloth | ((h > 0.03) & (h < 0.13) & (s > 0.30) & (v > 0.30) & notbg)
    out = hsv.copy()
    out[..., 0] = np.where(magenta | cloth, 0.995, h)
    out[..., 1] = np.where(cloth, np.clip(s * 2.6, 0.55, 0.85), np.where(magenta, np.maximum(s, 0.75), s))
    out[..., 2] = np.where(cloth, v * 0.92, v)
    return Image.fromarray((out * 255).astype(np.uint8), "HSV").convert("RGB")


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


def draft2(names, group=None, tag="g2", seeds=SEEDS, denoise=None):
    group = group or GROUP2
    for name in names or group:
        base, what = group[name]
        for seed in seeds:
            out = "%s/%s_%s_%d" % (OUT, tag, name, seed)
            if os.path.exists(os.path.join(ROOT, out + ".png")):
                continue
            r = subprocess.run([sys.executable, "tools/spriteforge.py", "i2i", "--out", out,
                                "--image", base if "/" in base else "gfx/characters/hoenn/%s.png" % base, "--prompt", "%s, %s" % (what, STYLE),
                                "--negative", NEG + ", plant", "--seed", str(seed), "--denoise", str(denoise or G2DENOISE)],
                               cwd=ROOT, capture_output=True, text=True)
            print("  %-24s %d %s" % (name, seed, "ok" if r.returncode == 0 else "FAILED " + r.stderr[-200:]), flush=True)


def sheet2(out, group=None, tag="g2", seeds=SEEDS):
    from PIL import Image, ImageDraw
    group = group or GROUP2
    rows = list(group)
    W = len(seeds) * 200 + 20
    img = Image.new("RGB", (W * 3, (len(rows) + 2) // 3 * 220 + 10), (24, 24, 32))
    d = ImageDraw.Draw(img)
    for k, name in enumerate(rows):
        x0, y0 = (k % 3) * W + 5, (k // 3) * 220 + 5
        for i, s in enumerate(seeds):
            p = os.path.join(ROOT, "%s/%s_%s_%d.png" % (OUT, tag, name, s))
            if os.path.exists(p):
                im = Image.open(p).convert("RGB")
                im.thumbnail((190, 190))
                img.paste(im, (x0 + i * 200, y0 + 18))
        d.text((x0, y0 + 2), "%s  (over %s; %d / %d)" % (name, os.path.basename(group[name][0]).replace("rs_", ""), seeds[0], seeds[-1]), fill="white")
    img.save(out)


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
    elif sys.argv[1:2] == ["draft2"]:
        draft2(sys.argv[2:])
    elif sys.argv[1:2] == ["sheet2"]:
        sheet2(sys.argv[2])
    elif sys.argv[1:2] == ["draft3"]:
        draft2(sys.argv[2:], GROUP3, "g3")
    elif sys.argv[1:2] == ["sheet3"]:
        sheet2(sys.argv[2], GROUP3, "g3")
    elif sys.argv[1:2] == ["magmared"]:
        import shutil
        for n in ("magma_grunt_m", "magma_grunt_f", "magma_admin_m", "magma_admin_f", "magma_leader_maxie"):
            pre = os.path.join(ROOT, OUT, "magma_pre_red", n + ".png")
            if not os.path.exists(pre):
                shutil.copy(os.path.join(ROOT, "gfx/characters/hoenn", n + ".png"), pre)
            magma_red(pre, coat=n == "magma_leader_maxie").save(os.path.join(ROOT, "gfx/characters/hoenn", n + ".png"))
            print("  red  " + n)
    elif sys.argv[1:2] == ["redraw3"]:
        draft2(sys.argv[2:], REDRAW3, "g3", RSEEDS, RDENOISE)
    elif sys.argv[1:2] == ["resheet3"]:
        sheet2(sys.argv[2], REDRAW3, "g3", RSEEDS)
    else:
        sys.exit(__doc__)

#!/usr/bin/env python3
"""Cut the character art down to the sprites the engine actually loads.

    python3 tools/gbachar.py            # report + /tmp/char.png
    python3 tools/gbachar.py --write

TWO SPRITES, TWO COMPLETELY DIFFERENT FORMATS, and getting either wrong
produces a screenful of confetti rather than an error.

  THE PLAYER -> graphics/oak_speech/{red,leaf}/pic.png, 64x96, 8bpp -- and a
     DIFFERENT palette bank from everyone else here. oak_speech.c loads the
     two player pics with LoadPalette(..., BG_PLTT_ID(4)) and the professor
     and rival with BG_PLTT_ID(6), so player indices start at 65 where the
     others start at 97. Vanilla's red/pic.png uses 0..95 and oak/pic.png
     uses 0..121, which is the same fact seen from the file. Wrong base is a
     screenful of confetti, not an error.

     9.10 made playerGender a pure sprite selector, so MALE_PLAYER_PIC is
     LOGIC and FEMALE_PLAYER_PIC is INTUITION -- the order the question
     offers them in.

  CRYSTAL -> graphics/oak_speech/oak/pic.png, 64x96, EIGHT bits per pixel.
     oak_speech.c loads its palette with LoadPalette(..., BG_PLTT_ID(6)),
     which is palette RAM 96 -- so the pixel values in the file are not 1..25,
     they are 97..121. An 8bpp background indexes palette RAM directly, so an
     image written with ordinary low indices would read the wrong end of the
     palette and come out as noise. The 32-colour .pal is bank 6, meaning its
     entry k is RAM 96+k.

  SCORN and AL's three battle pics -> graphics/trainers/front_pics/*.png,
     64x64, FOUR bits per pixel, sixteen colours, index 0 transparent.

     AND THE PNG DOES NOT CARRY THE COLOURS. trainers.h takes the picture
     from <name>_front_pic.4bpp.lz and the palette from a SEPARATE file,
     palettes/<name>.gbapal.lz, built from palettes/<name>.pal. Writing the
     PNG alone leaves the new indices addressing the OLD trainer's colours --
     Scorn shipped that way and rendered with Giovanni's palette, in which
     index 5 is magenta. Every 4bpp job writes its .pal.

AND NEITHER SPRITE CARRIES ITS OWN SHADOW. The generated art stands on a pale
ellipse, but oak_speech draws platform.png separately underneath and the
battle screen draws its own -- so the ellipse has to come off or the character
stands on two of them.
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gridsample import deringe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
KEY = (115, 197, 164)          # what vanilla puts in the transparent slot

JOBS = {
    # T-174, settled. THE INTRO THREE KEEP THEIR DRAWINGS. CRYSTAL and the player's LOGIC pose were written as
    # spriteforge restyles on 2026-09-20 and the user played them and called both distorted; the engine was reverted
    # and these jobs are back on the art they were drawn from. The rejected drafts are kept in gfx/drafts/t174/ as
    # sf_crystal_rejected.png and sf_logic_rejected.png. INTUITION never restyled at all -- a walking figure is thin
    # diagonals and every strength from 0.35 to 0.5 thinned them. What the experiment DID establish is the recipe the
    # portraits use (tools/prephires.py): restyle from the drawing at its own resolution, never from the ROM picture.
    "crystal":     dict(src="gfx/characters/crystal_speech.jpeg",
                        dst="engineGba/graphics/oak_speech/oak/pic.png",
                        pal="engineGba/graphics/oak_speech/oak/pal.pal",
                        size=(64, 96), colours=25, base=97, palsize=32, flip=True),
    "al_speech":   dict(src="gfx/characters/al_speech.jpeg",
                        dst="engineGba/graphics/oak_speech/rival/pic.png",
                        pal="engineGba/graphics/oak_speech/rival/pal.pal",
                        size=(64, 96), colours=25, base=97, palsize=32),
    "scorn":       dict(src="gfx/characters/style_d_scorn.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/leader_giovanni_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_giovanni.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
    "al_early":    dict(src="gfx/characters/al_early.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/rival_early_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/rival_early.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
    "al_late":     dict(src="gfx/characters/al_late.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/rival_late_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/rival_late.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
    "logic":       dict(src="gfx/characters/player_logic.jpeg",
                        dst="engineGba/graphics/oak_speech/red/pic.png",
                        pal="engineGba/graphics/oak_speech/red/pal.pal",
                        size=(64, 96), colours=31, base=65, palsize=32),
    "intuition":   dict(src="gfx/characters/player_intuition.jpeg",
                        dst="engineGba/graphics/oak_speech/leaf/pic.png",
                        pal="engineGba/graphics/oak_speech/leaf/pal.pal",
                        size=(64, 96), colours=31, base=65, palsize=32),
    # HEARSAY's portraits are 64x64 full-body figures with their own palettes,
    # the same shape as a trainer front pic. Crystal needs no new art: the
    # intro portrait fits a square frame, flipped to match how she stands
    # there.
    "crystal_fame": dict(src="gfx/characters/crystal_speech.jpeg",
                        dst="engineGba/graphics/fame_checker/prof_oak.png",
                        pal=None, size=(64, 64), colours=15, base=1, palsize=16,
                        flip=True),
    "holt":        dict(src="gfx/characters/holt.jpeg",
                        dst="engineGba/graphics/fame_checker/bill.png",
                        pal=None, size=(64, 64), colours=15, base=1, palsize=16),
    "vera":        dict(src="gfx/characters/vera_clear.jpeg",
                        dst="engineGba/graphics/fame_checker/daisy.png",
                        pal=None, size=(64, 64), colours=15, base=1, palsize=16),
    "init":        dict(src="gfx/characters/init.jpeg",
                        dst="engineGba/graphics/fame_checker/mr_fuji.png",
                        pal=None, size=(64, 64), colours=15, base=1, palsize=16),
    "cairn":       dict(src="gfx/characters/cairn.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/leader_brock_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_brock.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
    "al_champion": dict(src="gfx/characters/al_champion.jpeg",
                        dst="engineGba/graphics/trainers/front_pics/champion_rival_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/champion_rival.pal",
                        size=(64, 64), colours=15, base=1, palsize=16),
    # The six BENCHMARK leaders who had no art, drafted through n8n daemon/sprite under
    # 9.4's fable rule (2026-09-15); each species is the leader's role.
    "basin":   dict(src="gfx/characters/basin.png",       # a hippo lido attendant, settled in the pool she cannot climb out of
                        dst="engineGba/graphics/trainers/front_pics/leader_misty_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_misty.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "gauge":   dict(src="gfx/characters/gauge.png",       # a hare line engineer, ears as receptors, reacting first
                        dst="engineGba/graphics/trainers/front_pics/leader_lt_surge_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_lt_surge.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "trellis": dict(src="gfx/characters/sf_trellis.png",       # a bowerbird gardener, everything arranged to one exact shape
                        dst="engineGba/graphics/trainers/front_pics/leader_erika_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_erika.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    # T-120's portraits. A class's portrait and its overworld sheet are ONE species, so the hiker is
    # the badger his sheet already is. White ground from daemon/sprite, so hue=False as the leaders
    # are; no enclosed backdrop, so no holes.
    "hiker":   dict(src="gfx/characters/portrait_hiker_badger.png",
                        dst="engineGba/graphics/trainers/front_pics/hiker_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/hiker.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "picnicker": dict(src="gfx/characters/sf_picnicker.png",       # a hedgehog, as her sheet is
                        dst="engineGba/graphics/trainers/front_pics/picnicker_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/picnicker.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "youngster": dict(src="gfx/characters/sf_youngster.png",       # a mouse
                        dst="engineGba/graphics/trainers/front_pics/youngster_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/youngster.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "bugcatcher": dict(src="gfx/characters/sf_bug_catcher.png",    # a swallow, catching them on the wing
                        dst="engineGba/graphics/trainers/front_pics/bug_catcher_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/bug_catcher.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_biker": dict(src="gfx/characters/portrait_biker.png",             # a boar, as the sheet is
                        dst="engineGba/graphics/trainers/front_pics/biker_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/biker.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_swimmer_m": dict(src="gfx/characters/sf_swimmer_m.png",     # a newt
                        dst="engineGba/graphics/trainers/front_pics/swimmer_m_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/swimmer_m.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_lass": dict(src="gfx/characters/portrait_lass.png",               # a lamb
                        dst="engineGba/graphics/trainers/front_pics/lass_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/lass.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_channeler": dict(src="gfx/characters/sf_channeler.png",     # a bat, at home in the tower's dark
                        dst="engineGba/graphics/trainers/front_pics/channeler_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/channeler.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_camper": dict(src="gfx/characters/sf_camper.png",           # a raccoon
                        dst="engineGba/graphics/trainers/front_pics/camper_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/camper.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_swimmer_f": dict(src="gfx/characters/sf_swimmer_f.png",     # an axolotl
                        dst="engineGba/graphics/trainers/front_pics/swimmer_f_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/swimmer_f.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_fisherman": dict(src="gfx/characters/portrait_fisherman.png",     # a pelican: the bill IS the tackle
                        dst="engineGba/graphics/trainers/front_pics/fisherman_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/fisherman.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_scientist": dict(src="gfx/characters/portrait_scientist.png",     # a mole, the digging nobody sees
                        dst="engineGba/graphics/trainers/front_pics/scientist_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/scientist.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_pokemaniac": dict(src="gfx/characters/portrait_pokemaniac.png",   # an opossum
                        dst="engineGba/graphics/trainers/front_pics/pokemaniac_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/pokemaniac.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_blackbelt": dict(src="gfx/characters/portrait_black_belt.png",    # a kangaroo in a gi
                        dst="engineGba/graphics/trainers/front_pics/black_belt_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/black_belt.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_crushgirl": dict(src="gfx/characters/portrait_crush_girl.png",    # a wolverine
                        dst="engineGba/graphics/trainers/front_pics/crush_girl_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/crush_girl.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_sailor": dict(src="gfx/characters/sf_sailor.png",           # an albatross, always at sea
                        dst="engineGba/graphics/trainers/front_pics/sailor_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/sailor.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_gentleman": dict(src="gfx/characters/portrait_gentleman.png",     # a lynx in tweed
                        dst="engineGba/graphics/trainers/front_pics/gentleman_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/gentleman.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_beauty": dict(src="gfx/characters/sf_beauty.png",           # a gazelle
                        dst="engineGba/graphics/trainers/front_pics/beauty_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/beauty.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_tuber_f": dict(src="gfx/characters/portrait_tuber_f.png",         # a cygnet in its ring
                        dst="engineGba/graphics/trainers/front_pics/tuber_f_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/tuber_f.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_rocker": dict(src="gfx/characters/portrait_rocker.png",           # a skunk: the stripe was always a mohawk
                        dst="engineGba/graphics/trainers/front_pics/rocker_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/rocker.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    # THE REVIEW BOARD. Section 6 reserves their colours -- sanguine red, choleric yellow,
    # melancholic black, phlegmatic white -- and 6804 says value carries them: melancholic dark,
    # phlegmatic pale, sanguine and choleric mid. Same species as their overworld sheets.
    "p_phlegmatic": dict(src="gfx/characters/portrait_elite_four_lorelei.png",   # a polar bear, FROZEN
                        dst="engineGba/graphics/trainers/front_pics/elite_four_lorelei_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/elite_four_lorelei.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_choleric": dict(src="gfx/characters/sf_bruno.png",       # a tiger, LOGIC
                        dst="engineGba/graphics/trainers/front_pics/elite_four_bruno_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/elite_four_bruno.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_melancholic": dict(src="gfx/characters/portrait_elite_four_agatha.png",   # a wombat, LATENT
                        dst="engineGba/graphics/trainers/front_pics/elite_four_agatha_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/elite_four_agatha.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_sanguine": dict(src="gfx/characters/portrait_elite_four_lance.png",       # a cardinal, EMERGENT
                        dst="engineGba/graphics/trainers/front_pics/elite_four_lance_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/elite_four_lance.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    # The dozen with no overworld counterpart, at the agreed cut-off: a class earns a drawing if
    # three or more trainers use it. The PAIR classes are two figures of one species in one 64x64.
    "p_birdkeeper": dict(src="gfx/characters/portrait_bird_keeper.png",          # an ostrich, keeping smaller birds
                        dst="engineGba/graphics/trainers/front_pics/bird_keeper_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/bird_keeper.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_cueball": dict(src="gfx/characters/sf_cue_ball.png",                # a rhinoceros
                        dst="engineGba/graphics/trainers/front_pics/cue_ball_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/cue_ball.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_supernerd": dict(src="gfx/characters/portrait_super_nerd.png",            # a ring-tailed lemur
                        dst="engineGba/graphics/trainers/front_pics/super_nerd_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/super_nerd.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_gamer": dict(src="gfx/characters/sf_gamer.png",                     # a JACKAL -- and never a fox (9.4)
                        dst="engineGba/graphics/trainers/front_pics/gamer_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/gamer.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_ruinmaniac": dict(src="gfx/characters/portrait_ruin_maniac.png",          # an aardvark, the digger
                        dst="engineGba/graphics/trainers/front_pics/ruin_maniac_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/ruin_maniac.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_burglar": dict(src="gfx/characters/sf_burglar.png",                 # a weasel
                        dst="engineGba/graphics/trainers/front_pics/burglar_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/burglar.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_juggler": dict(src="gfx/characters/portrait_juggler.png",                 # an octopus: the arms are the act
                        dst="engineGba/graphics/trainers/front_pics/juggler_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/juggler.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_twins": dict(src="gfx/characters/portrait_twins.png",                     # two PIGLETS, as LITTLE_GIRL is (T-128)
                        dst="engineGba/graphics/trainers/front_pics/twins_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/twins.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_youngcouple": dict(src="gfx/characters/portrait_young_couple.png",        # an OX and a GAZELLE, as MAN and BEAUTY are (T-128)
                        dst="engineGba/graphics/trainers/front_pics/young_couple_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/young_couple.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_sisandbro": dict(src="gfx/characters/portrait_sis_and_bro.png",           # a DUCKLING and an AXOLOTL, as TUBER_M and SWIMMER_F are (T-128)
                        dst="engineGba/graphics/trainers/front_pics/sis_and_bro_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/sis_and_bro.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_crushkin": dict(src="gfx/characters/portrait_crush_kin.png",              # a KANGAROO and a WOLVERINE, as BLACK_BELT and CRUSH_GIRL are (T-128)
                        dst="engineGba/graphics/trainers/front_pics/crush_kin_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/crush_kin.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_coolcouple": dict(src="gfx/characters/portrait_cool_couple.png",          # a WOLF and a FALCON, as COOLTRAINER_M and _F are (T-126)
                        dst="engineGba/graphics/trainers/front_pics/cool_couple_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/cool_couple.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_srandjr": dict(src="gfx/characters/portrait_sr_and_jr.png",               # two porcupines
                        dst="engineGba/graphics/trainers/front_pics/sr_and_jr_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/sr_and_jr.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    # The ten that were AT OR ABOVE the cut-off and had been missed. A class must not wear a
    # BENCHMARK leader's species, and must not repeat one already spent on another class.
    "p_ranger_m": dict(src="gfx/characters/sf_ranger_m.png",       # a pine marten
                        dst="engineGba/graphics/trainers/front_pics/pokemon_ranger_m_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/pokemon_ranger_m.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_ranger_f": dict(src="gfx/characters/sf_ranger_f.png",       # the same marten
                        dst="engineGba/graphics/trainers/front_pics/pokemon_ranger_f_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/pokemon_ranger_f.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_breeder": dict(src="gfx/characters/portrait_pokemon_breeder.png",         # a goose
                        dst="engineGba/graphics/trainers/front_pics/pokemon_breeder_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/pokemon_breeder.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_aroma": dict(src="gfx/characters/portrait_aroma_lady.png",                # a honeybee, and the hive talks by dancing
                        dst="engineGba/graphics/trainers/front_pics/aroma_lady_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/aroma_lady.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_rsyoungster": dict(src="gfx/characters/portrait_rs_youngster.png",        # a vole
                        dst="engineGba/graphics/trainers/front_pics/rs_youngster_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/rs_youngster.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_lady": dict(src="gfx/characters/portrait_lady.png",                       # a swan
                        dst="engineGba/graphics/trainers/front_pics/lady_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/lady.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_engineer": dict(src="gfx/characters/portrait_engineer.png",               # a beaver, a record in material that lasts
                        dst="engineGba/graphics/trainers/front_pics/engineer_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/engineer.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_tamer": dict(src="gfx/characters/sf_tamer.png",                     # a hyena ringmaster
                        dst="engineGba/graphics/trainers/front_pics/tamer_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/tamer.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_psychic_f": dict(src="gfx/characters/sf_psychic_f.png",             # a jellyfish, not a second octopus
                        dst="engineGba/graphics/trainers/front_pics/psychic_f_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/psychic_f.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_painter": dict(src="gfx/characters/portrait_painter.png",                 # a toucan -- MATTE owns the chameleon
                        dst="engineGba/graphics/trainers/front_pics/painter_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/painter.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "tilt":    dict(src="gfx/characters/sf_tilt.png",       # a toad card dealer, poisonous, still, in no hurry
                        dst="engineGba/graphics/trainers/front_pics/leader_koga_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_koga.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "matte":   dict(src="gfx/characters/matte.png",       # a chameleon film editor, deciding what is shown
                        dst="engineGba/graphics/trainers/front_pics/leader_sabrina_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_sabrina.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False, holes=True),
    "anneal":  dict(src="gfx/characters/sf_anneal.png",       # a salamander metallurgist, at home in controlled heat
                        dst="engineGba/graphics/trainers/front_pics/leader_blaine_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/leader_blaine.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    # The BENCHMARK staff (T-116): one portrait per gym, DOLDRUM two; drafted through daemon/sprite.
    "staff_slate": dict(src="gfx/characters/sf_staff_slate.png",       # SLATE's apprentice, a young beaver
                        dst="engineGba/graphics/trainers/front_pics/staff_slate_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_slate.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "staff_doldrum_swimmer": dict(src="gfx/characters/sf_staff_doldrum_swimmer.png",       # DOLDRUM's swimmer, a manatee
                        dst="engineGba/graphics/trainers/front_pics/staff_doldrum_swimmer_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_doldrum_swimmer.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "staff_doldrum_picnicker": dict(src="gfx/characters/sf_staff_doldrum_picnicker.png",       # DOLDRUM's picnicker, a capybara
                        dst="engineGba/graphics/trainers/front_pics/staff_doldrum_picnicker_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_doldrum_picnicker.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "staff_ardor": dict(src="gfx/characters/staff_ardor_meerkat.png",       # ARDOR's staff, meerkats on watch
                        dst="engineGba/graphics/trainers/front_pics/staff_ardor_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_ardor.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "staff_verdigris": dict(src="gfx/characters/staff_verdigris_poodle.png",       # VERDIGRIS's staff, poodles clipped to shape
                        dst="engineGba/graphics/trainers/front_pics/staff_verdigris_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_verdigris.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "staff_lurid": dict(src="gfx/characters/staff_lurid_frog.png",       # LURID's staff, tailless poison dart frogs
                        dst="engineGba/graphics/trainers/front_pics/staff_lurid_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_lurid.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "staff_brazen": dict(src="gfx/characters/sf_staff_brazen.png",       # BRAZEN's staff, tarsiers framing what they watch
                        dst="engineGba/graphics/trainers/front_pics/staff_brazen_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_brazen.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "staff_quicksilver": dict(src="gfx/characters/staff_quicksilver_rat.png",       # QUICKSILVER's staff, lab rats
                        dst="engineGba/graphics/trainers/front_pics/staff_quicksilver_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_quicksilver.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    # T-169 batch 1: the sources marked sf_ are SPRITEFORGE drawings, restyled from the T-120 drawing each class's
    # sheet was matched to (gfx/drafts/t169/batch1/PICKS.txt); the old sources stay beside them as history.
    # The BIRD KEEPER, BIKER and LASS kept their T-120 drawings -- the restyle came back noisier, muddier and,
    # for the lass, half human again: a batch may keep what it has, and three of eleven did.
    "staff_callow": dict(src="gfx/characters/sf_rocket_grunt_m.png",       # CALLOW's staff, cheerful penguins
                        dst="engineGba/graphics/trainers/front_pics/staff_callow_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/staff_callow.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    # CORPUS STAFF (T-118): penguins, the organisation CALLOW's staff belong to -- the male is the same drawing.
    "corpus_m": dict(src="gfx/characters/sf_rocket_grunt_m.png",
                        dst="engineGba/graphics/trainers/front_pics/rocket_grunt_m_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/rocket_grunt_m.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    # The COOL TRAINERs (T-169): the last two faced portraits still vanilla's, drawn from the wolf and falcon halves of
    # the COOL COUPLE -- which gencouple.py re-headed AFTER this file cut it, so running every job here would put that
    # pair's two ibexes back. Name jobs (python3 tools/gbachar.py p_cooltrainer_m ...) when writing.
    "p_cooltrainer_m": dict(src="gfx/characters/sf_cool_trainer_m.png",     # a wolf, as COOLTRAINER_M is (T-126)
                        dst="engineGba/graphics/trainers/front_pics/cool_trainer_m_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/cool_trainer_m.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "p_cooltrainer_f": dict(src="gfx/characters/sf_cool_trainer_f.png",     # a falcon, as COOLTRAINER_F is (T-126)
                        dst="engineGba/graphics/trainers/front_pics/cool_trainer_f_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/cool_trainer_f.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
    "corpus_f": dict(src="gfx/characters/institution_penguin_f.png",
                        dst="engineGba/graphics/trainers/front_pics/rocket_grunt_f_front_pic.png",
                        pal="engineGba/graphics/trainers/palettes/rocket_grunt_f.pal",
                        size=(64, 64), colours=15, base=1, palsize=16, hue=False),
}

def silhouette(a, hue=True, holes=False):
    """Background AND the shadow ellipse, which are both GREENISH.

    The ellipse is the background blended toward white, so it keeps the green
    bias; the lab coat is neutral and the suit is blue-grey, and neither does.

    BUT THE HUE RULE ALONE IS TOO BRITTLE. Holt's backdrop came back a pale
    olive at (171,181,128) -- g-r = 10, two points under the threshold -- so
    none of it keyed out, the bounding box became the whole canvas, and he was
    cut at half the size of everyone else. A missed key does not look like a
    missed key; it looks like a framing bug.

    So the four corners are keyed as well, when they agree with each other.
    The hue rule still runs, because it is what removes the ellipse.

    AND ONLY WHAT TOUCHES THE BORDER IS BACKGROUND. Both rules are colour
    tests, and a colour test cannot tell the backdrop from a garment that
    happens to sit near it. Al's backdrop is a dark sage at (97,130,103), and
    the shaded lavender of his trousers and the grey of the box he holds are
    inside the 45 radius -- so the early pic shipped with its trousers mostly
    holes, and the late one speckled. A keyable pixel is background only if it
    connects to the edge of the image through other keyable pixels; the
    outline stops the fill, so the inside of the figure survives whatever
    colour it is. The ellipse touches the backdrop, so it still goes.

    AND THE HUE RULE IS FOR GREEN BACKDROPS ONLY. The leaders drafted through
    daemon/sprite (2026-09-15) stand on plain white with no ellipse, and two of
    them are green where it matters: TRELLIS's apron and MATTE's skin. With the
    hue rule on, both leaked out through gaps in the outline and the apron came
    back a hole. hue=False keys on the flat corners alone."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    keyable = (g - r > 12) & (g - b > 4) if hue else np.zeros(a.shape[:2], dtype=bool)
    corners = np.stack([a[2, 2], a[2, -3], a[-3, 2], a[-3, -3]])
    spread = corners.max(axis=0) - corners.min(axis=0)
    if spread.max() < 24:                       # a real flat backdrop
        key = np.median(corners, axis=0)
        keyable = keyable | (((a - key) ** 2).sum(axis=2) < 45 ** 2)
    background = connected_to_border(keyable)
    if holes and spread.max() < 24:
        # BACKDROP CAN BE ENCLOSED. MATTE's curled tail closes a loop against her
        # legs, and the white inside it touches no edge, so the rule above keeps
        # it as figure -- a white block in battle. Opt-in, per job: pockets that
        # match the corner colour closely AND are large are backdrop too, so eye
        # whites and highlights survive. Only for art with no white clothing.
        from scipy import ndimage
        near = (((a - key) ** 2).sum(axis=2) < 20 ** 2) & ~background
        labels, n = ndimage.label(near)
        sizes = ndimage.sum(near, labels, range(1, n + 1))
        floor = 0.0008 * a.shape[0] * a.shape[1]         # deringe has shrunk the art to its drawn grid,
        background = background | np.isin(labels, [i + 1 for i, v in enumerate(sizes) if v > floor])   # so a share, not a count
    return ~background

def connected_to_border(mask):
    """The part of mask reachable from the image's edge, 4-connected."""
    try:
        from scipy import ndimage
        labels, _ = ndimage.label(mask)
        edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
        return np.isin(labels, edge[edge > 0])
    except ImportError:
        reach = np.zeros_like(mask)
        reach[0], reach[-1], reach[:, 0], reach[:, -1] = mask[0], mask[-1], mask[:, 0], mask[:, -1]
        while True:
            grow = reach.copy()
            grow[1:] |= reach[:-1]; grow[:-1] |= reach[1:]
            grow[:, 1:] |= reach[:, :-1]; grow[:, :-1] |= reach[:, 1:]
            grow &= mask
            if (grow == reach).all():
                return reach
            reach = grow

def cut(job):
    # Sampled on the grid it was drawn on: these are pixel drawings upscaled
    # to 1024 and exported as JPEG, so the ringing sits at block edges and
    # never has to be read. Matters less here than for the daemons -- a 2.7x
    # reduction averages most of it away -- but one pipeline, one behaviour.
    a = deringe(np.asarray(Image.open(os.path.join(ROOT, job["src"])).convert("RGB")).astype(int))
    ink = silhouette(a, job.get("hue", True), job.get("holes", False))
    ys, xs = np.where(ink)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    im = Image.fromarray(a.astype(np.uint8)).crop(box)
    mask = Image.fromarray((ink[box[1]:box[3], box[0]:box[2]] * 255).astype(np.uint8))

    if job.get("flip"):
        # oak_speech spawns the box at x=100 and the daemon at x=96, both left
        # of centre because that is where OAK's hand was. Crystal reaches to
        # the right, so the box appeared beside the wrong hand. Mirroring the
        # art keeps vanilla's tested composition; moving the two coordinates
        # instead would push a 64-wide daemon into her at this size.
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        mask = mask.transpose(Image.FLIP_LEFT_RIGHT)

    W, H = job["size"]
    scale = min(W / im.width, H / im.height)
    w, h = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    im = im.resize((w, h), Image.LANCZOS)
    mask = mask.resize((w, h), Image.LANCZOS).point(lambda v: 255 if v > 140 else 0)

    cell = Image.new("RGB", (W, H), KEY)
    cell.paste(im, ((W - w) // 2, H - h), mask)      # feet on the floor, centred
    hold = Image.new("L", (W, H), 0)
    hold.paste(mask, ((W - w) // 2, H - h))
    return cell, hold

def index(cell, hold, job):
    # Quantize the SUBJECT ONLY. Quantizing the whole cell hands one of the
    # scarce slots to the transparent key, which is then zeroed out again --
    # 15 colours become 14, on a sprite that has 15 to spend.
    subj = np.asarray(cell)[np.asarray(hold) > 0].reshape(1, -1, 3).astype(np.uint8)
    q = Image.fromarray(subj).convert("P", palette=Image.ADAPTIVE,
                                      colors=job["colours"], dither=Image.NONE)
    pal = q.getpalette()[:job["colours"] * 3]
    table = [tuple(pal[i * 3:i * 3 + 3]) for i in range(job["colours"])]
    a = np.asarray(cell).astype(int)
    d = ((a[:, :, None, :] - np.array(table)[None, None, :, :]) ** 2).sum(axis=3)
    flat = (d.argmin(axis=2) + job["base"]).astype(np.uint8)
    flat[np.asarray(hold) == 0] = 0
    out = Image.new("P", cell.size)
    out.putdata(flat.flatten().tolist())
    full = [0] * 768
    full[0:3] = list(KEY)
    for i, c in enumerate(table):
        j = (job["base"] + i) * 3
        full[j:j + 3] = list(c)
    out.putpalette(full)
    return out, table

def main():
    # Name jobs to cut only those (python3 tools/gbachar.py basin tilt --write); with none, every job runs.
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    assert all(a in JOBS for a in only), "no such job: %s" % [a for a in only if a not in JOBS]
    todo = {k: v for k, v in JOBS.items() if not only or k in only}
    prev, x = Image.new("RGB", ((64 * 6 + 40) * len(todo), 96 * 6), (18, 18, 24)), 0
    for name, job in todo.items():
        cell, hold = cut(job)
        out, table = index(cell, hold, job)
        print("  %-8s %-52s %dx%d, %d colours at index %d+"
              % (name, job["dst"].split("engineGba/")[-1], *job["size"], len(table), job["base"]))
        prev.paste(out.convert("RGB").resize((64 * 6, job["size"][1] * 6), Image.NEAREST), (x, 0))
        x += 64 * 6 + 40
        if "--write" in sys.argv:
            out.save(os.path.join(ROOT, job["dst"]))
            if job["pal"]:
                with open(os.path.join(ROOT, job["pal"]), "w") as f:
                    f.write("JASC-PAL\n0100\n%d\n" % job["palsize"])
                    rows = [KEY] + [(0, 0, 0)] * (job["palsize"] - 1)
                    for i, c in enumerate(table):          # entry 0 is the key; ours start at 1
                        rows[1 + i] = c
                    for c in rows:
                        f.write("%d %d %d\n" % c)
            print("           written")
    prev.save("/tmp/char.png")
    print("  preview   /tmp/char.png")

if __name__ == "__main__":
    main()

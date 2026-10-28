# T-452 forms: install runbook (on "go", after SYMBOL installs and releases)

The user chose this on 2026-10-28:
- install PROTEUS's three forms and OVERLOADED's sunny, rainy and snowy forms as drawn;
- give PROTEUS one shared battle row at y_offset 11;
- fix OVERLOADED's per-form battle positions and its streaks;
- re-clean the normal form's open top on a keyed ground.

Paths used below:
- `W` = `/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452forms_work`
- `R` = `/Users/christopherhicks/Projects/DAEMONS`
- `E` = `R/engineGba` (pokefirered-daemons)
- `P` = `~/.pyenv/versions/3.12.2/bin/python3`

Run every tool from `R`.

**Everything is prepared in `W/prep/`. Nothing is in either repo yet.**

| prepared | what it is | checked how |
|---|---|---|
| `prep/gfx_daemons/` | the 17 source files for `R/gfx/daemons/` (below) | they are the hand grids and icon3 icons the sheets show |
| `prep/tools/gencastform.py` | NEW tool: `castform/{normal,sunny,rainy,snowy}/` from `gfx/daemons`, report / `--sheet` / `--write` / `--out DIR` | in a symlinked test root: (1) with today's sources, normal/ came out **byte-identical** to the engine's (batch 18's hand copy), so the tool reproduces the install it replaces; (2) the weathers equal the drafted `z/engine/castform` files; (3) its report mode writes only a preview (`daemonslib.preview`), as `check_generators.py` requires |
| `prep/tools/genproteus.py` (+ `prep/genproteus.diff`) | reads the drawn form icons `gfx/daemons/proteus_icon_{attack,defense}.png`; `ICON_PALETTE` 0 to 1 and refuses a drawn icon on another palette; its preview via `daemonslib.preview` | in the test root, all six files it writes are pixel- and palette-identical to the drafted `z/engine/deoxys` |
| `prep/new/` (+ `prep/engine.diff`, 240 lines against engine `0624b3b39`) | the engine edits: `src/battle_anim_mons.c`, `src/battle_gfx_sfx_util.c`, `src/daemon_streaks.c`, `include/daemon_streaks.h`, `src/pokemon_icon.c`, `src/data/pokemon_graphics/{front,back}_pic_coordinates.h` | the four `.c` files compiled with agbcc `-Werror` for FIRERED and LEAFGREEN into `prep/obj/` (exit 0); the build has not been run |

## 1. DAEMONS: sources, tools, drafts

1. **Sources.** Copy `W/prep/gfx_daemons/*` to `R/gfx/daemons/`, replacing in place:
   - **PROTEUS:**
     - `proteus_front.png` and `proteus_back.png` (hooded);
     - `proteus_front_attack.png` and `proteus_back_attack.png` (ALL EDGES);
     - `proteus_front_defense.png` and `proteus_back_defense.png` (SHELL);
     - `proteus_icon.png`, plus NEW `proteus_icon_attack.png` and `proteus_icon_defense.png` (icon3, palette 1).
   - **OVERLOADED:**
     - `overloaded_front.png` and `overloaded_back.png` (the normal form re-cleaned: top closed, batch 18's sun, snowflake and drop again, back flattened like the weathers);
     - NEW `overloaded_{sunny,rainy,snowy}_{front,back}.png`.
   - `overloaded_icon.png` is unchanged.

   Nothing else lists `gfx/daemons` by pattern in a way the new names would confuse. `companion_export.py` only builds a name set, and gbasprite's `rich_src` globs `<name>_<kind>.*`, which `overloaded_sunny_front` does not match.
2. **Tools.** Copy `W/prep/tools/gencastform.py` to `R/tools/` (new) and `W/prep/tools/genproteus.py` over `R/tools/genproteus.py`. `check_generators.py` finds gencastform by itself, since it has `--write` and `main()`.
3. **Drafts.** Copy into the repo:
   - `W/z` (all but `engine/`) to `R/gfx/drafts/t452/z`;
   - `W/questions.md`, this file and `W/sheets/t452forms_*.png` to `gfx/drafts/t452/z/`;
   - `W/scripts/*` to `R/gfx/drafts/t452/scripts/`. The new ones are `forms.py`, `prekey.py`, `prekey_hull.py`, `hand_pro.py`, `hand_ov.py`, `hand_normal.py`, `render.py`, `engine.py`, `sheet.py`, `grid.py` and `cands.py`; the rest are batch 18's.

## 2. Engine

1. **Apply the C edits:** `cd E && patch -p1 --dry-run < W/prep/engine.diff`, then without `--dry-run`. The diff's paths are `orig/...` and `new/...`, so `-p1` strips them. If the engine moved since `0624b3b39` and a hunk fails, copy by hand from `W/prep/new/`; every hunk names the function or table it touches. What it changes:
   - **`src/battle_anim_mons.c`:**
     - `gCastformFrontSpriteCoords` changes from {32x32,17}, {48x48,9}, {32x48,9}, {64x48,8} to **{64x56, 7}, {56x48, 10}, {48x48, 9}, {56x48, 8}**;
     - `sCastformBackSpriteYCoords` changes from 0, 0, 0, 0 to **7, 10, 9, 8**;
     - all measured off gencastform's output (63 minus the lowest opaque row);
     - `sCastformElevations` (the float) is unchanged.
   - **`src/data/pokemon_graphics/front_pic_coordinates.h` and `back_pic_coordinates.h`**, `[SPECIES_DEOXYS]`:
     - **`.size = MON_COORDS_SIZE(56, 48), .y_offset = 11`** in both, with a comment that it is the editions' shared row (edges 9, shell 14), and that ground.py must not measure it;
     - the old values were front {64x64, 1} and back {64x56, 13}.
   - **`src/pokemon_icon.c`:** `gMonIconPaletteIndices[SPECIES_DEOXYS]` changes 0 to **1**.
   - **Streaks** (the T-ticket below):
     - `daemon_streaks.c` and `.h` gain `Streaks_ApplyToLoadedOnBody` (`StreakColour` split into `StreakColourOnBody`, behaviour unchanged for every other caller) and `Streaks_ApplyToCastform(offset, form, moves)`. The latter maps form to its body type: NORMAL, FIRE, WATER, ICE.
     - `battle_gfx_sfx_util.c` calls `Streaks_ApplyToCastform` after each of the four castform palette reloads, and before `Saturation_ApplyToLoaded`, matching the buffer path's streaks-then-saturation order. The four reloads are: foe load, player load, the Forecast form change, and PERSPECTIVE onto a castform (with the target's moves).
2. **The forms:** `P tools/gencastform.py` (report: normal, sunny, rainy and snowy WOULD CHANGE), then `P tools/gencastform.py --write`.
3. **The species and PROTEUS:**
   - `P tools/gbasprite.py --write`. It is whole-tree: read `git -C engineGba diff --stat` and expect only `deoxys/` and `castform/` top-level files. The latter is the normal form's species copy, which the build does not join but the followers and genstreaks read.
   - Then `P tools/genproteus.py --write`. It writes `front_def.png` and `back_def.png`, the two form icons on palette 1, and `front.png` and `back.png` identical to gbasprite's.
4. `P tools/gbaowslots.py --write`. It remakes `object_events/pics/pokemon/deoxys_n.png` from the new hooded top. `deoxys_a` and `deoxys_d` (T-439's own drawings) stay.
5. `P tools/gbafollower.py --write` and `P tools/gbafollowerpal.py --write`. PROTEUS's follower comes from `icon.4bpp`, and both species' follower palettes from `normal.pal` and `shiny.pal`.
6. **Do NOT run the batches' `ground.py` on `deoxys`.** It reads the top 64 rows (the hooded form) and would write 5. Castform's species rows `gMonFrontPicCoords` and `gMonBackPicCoords` are already {64x56, 7}, and the re-cleaned normal measures the same.

## 3. Check and ship (the push routine)

1. Build all four ROMs and check each exit code:

   ```sh
   make -C engineGba firered_debug -j8 >/dev/null 2>&1; echo "exit=$?"
   ```

   Then `firered`, `leafgreen` and `leafgreen_debug` the same way.
2. Run the checks:
   - `check_lexicon.py`, `check_reach.py`, `check_agent_vocab.py`;
   - `companion_export.py --check`, then `--write`, since the companion's `art/` holds both fronts;
   - `check_generators.py gencastform genproteus gbasprite` (it must report no write).
3. **Theatre:**
   - **PROTEUS**, wild on THE ANNEX, in both editions (`tools/routes/t440c.json`): the CONTENT foe in ALL EDGES and the CONTEXT foe in the SHELL; an owned one from behind; the sprite's feet near the usual ground line at y_offset 11.
   - **OVERLOADED**, from the DEBUG build in THE WEATHERVERSE: SUNNY DAY, then a rain move, then HAIL. Each form change should keep **coloured streaks** (they were grey before), and each body should stand on the ground line. Also a PERSPECTIVE onto it, if a DEBUG daemon has the move.
4. Commit per ticket, engine first:
   - **engine:** "T-452 forms: PROTEUS's three forms and OVERLOADED's four bodies; castform rows; DEOXYS row 11; icon palette 1";
   - **engine, the streak ticket separately:** the `daemon_streaks` and `battle_gfx_sfx_util` hunks;
   - **then DAEMONS:** `gfx/daemons`, `tools/gencastform.py`, `tools/genproteus.py`, `gfx/drafts/t452/z` and scripts, and the TODO rows.
5. Review sheets: `W/sheets/t452forms_proteus.png` and `t452forms_overloaded.png`. Redo them from the ROM's files after the build, if wanted, by pointing `sheet.py`'s new-art paths at the engine. Then `qashot.py --ticket T-452`.

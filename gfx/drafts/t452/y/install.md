# T-452 SYMBOL -- install plan (not the one-species path)

**INSTALLED (2026-10-28, engine 6fd39fcf5, the user: as drawn; followers for every letter at the player's size; 'There are twenty-six' kept).** Done by `scripts/build_sym.py --write` (steps 1-4) and `tools/gbafollower.py --write` (step 5, now making the 27 letters' followers too; `sFollowerPics` sized `SPECIES_UNOWN_QMARK + 1`), then `tools/gbafollowerpal.py --write`. As built: `t452sym_built.png`.

**Why not the normal path.** The batches copy `<name>_{front,back,icon}.png` into `gfx/daemons/` and run
`tools/gbasprite.py --write`, which writes `graphics/pokemon/<slot>/{front,back,icon}.png` and `normal.pal`. SYMBOL is
vanilla's UNOWN (201): its art is **28 forms in `graphics/pokemon/unown/<form>/`** (a-z, `exclamation_mark`,
`question_mark`; each `front.png`, `back.png`, `icon.png`, and `a/follower.png`) drawn through **one palette**,
`graphics/pokemon/unown/{normal,shiny}.pal` (`gMonPalette_Unown`, which `palette_table.h` gives SPECIES_UNOWN and all
27 of SPECIES_UNOWN_B..QMARK). `symbol_front.png` in `gfx/daemons/` would make gbasprite write an unused
`unown/front.png`, an `unown/icon.png` and `normal.pal` from one form only -- **so it must not go there.** Today's
SYMBOL art is entirely vanilla's (only `footprint.png` and `a/follower.png` were ever changed).

Files ready in this dir: `hand/<form>_front.png` (clean 64 RGBA, the source), `reduced/<form>_{front,back}.png`
(4bpp, the built pictures, all in one palette), `reduced/<form>_icon.png` (32x64, shared icon palette 1),
`picks.json` (palette, icon3 report, choices), `coords.txt` (the grounding rows).

1. **Art in.** Copy the 28 into `gfx/daemons/symbol/<form>_{front,back,icon}.png` (a subfolder: gbasprite's `rich_src`
   globs only the top folder, so it never sees them). Fronts from `hand/`, backs and icons from `reduced/` (the back
   is made on the index grid -- the front mirrored, eye out -- so it is already 4bpp in the shared palette).
2. **A small tool** (`gfx/drafts/t452/scripts/build_sym.py`, from `scripts/process.py` here): for each form
   `gbs.place_rich(front, TYPE_COLOR["PSYCHIC"])`; **assert all 28 palettes are identical** (they are: BG + CONTEXT's
   ramp5, accents greyed); `write_png4` to `unown/<form>/front.png` and `back.png`; `write_pal` the one palette to
   `unown/normal.pal` and `genshiny.make_shiny(palette)` to `unown/shiny.pal` (CRLF, daemonslib); icons copied index
   for index (gbasprite's `drawn_icon` check) to `unown/<form>/icon.png`. Temp file then rename.
3. **Icon palette indices** in `src/pokemon_icon.c` `gMonIconPaletteIndices`: SPECIES_UNOWN and SPECIES_UNOWN_B ..
   SPECIES_UNOWN_QMARK from 0 to **1** (one digit for one digit, length asserted, as build17's iconpal).
4. **Grounding rows** in `front_pic_coordinates.h` and `back_pic_coordinates.h` for the 28 constants from
   `coords.txt` (ground.py's rule: size = the box rounded up to 8, y_offset = 63 - lowest row). ground.py itself takes
   a SLOT and reads `graphics/pokemon/SLOT/`; give it the form's path and the `SPECIES_UNOWN_*` constant (A is
   `SPECIES_UNOWN`, ! is `UNOWN_EMARK`, ? is `UNOWN_QMARK`).
5. **Followers (question 6).** `tools/gbafollower.py` skips `SPECIES_UNOWN_*` (line 54) but the follower draws the
   letter's species (`GetIconSpecies`), so with 28px icons each letter would walk oversized. Let it make all 28
   (REDUCED from `gfx/daemons/symbol/<form>_front.png`), writing `unown/<form>/follower.png` and `follower_gfx.h`
   rows for SPECIES_UNOWN_B..QMARK; `tools/gbafollowerpal.py --write` after. Then `gbafollower.py` (report) passes.
6. **Not touched:** footprint, no overworld object (UNOWN has none), the Index entry (question 7), streaks
   (SYMBOL has none), `gbaowslots.py` (nothing to move).
7. **Check:** `make -C engineGba firered_debug` exit 0; DEBUG catch a few letters (the form is the personality) and
   look at front, back, party icon, follower, shiny; `check_reach`, `check_lexicon`, `gbafollower.py`;
   `check_generators.py` -- **gbasprite must still skip SYMBOL** (no `gfx/daemons/symbol_*.png` at the top level).
8. **Companion (question 8)**: `companion_export.py` reads art only from `gfx/daemons/<name>_front.png`; point SYMBOL
   at `symbol/a_front.png` or leave it null.

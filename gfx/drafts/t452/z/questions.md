# T-452 forms -- PROTEUS's three forms and OVERLOADED's three weathers: questions (2026-10-28)

The user chose this on 2026-10-28: redraw all three of PROTEUS's forms (hooded, ALL EDGES, SHELL; the DEOXYS slot),
keeping T-440's stacked battle sheets and form icons, and OVERLOADED's sunny, rainy and snowy forms (the CASTFORM
slot; its normal form was redrawn in batch 18 and is in castform/normal/, engine be3388f75).

Charm recipe, seed 6900, drafted in `t452forms_work/z` (the repo's draft dir would be `gfx/drafts/t452/z`: y is
SYMBOL's, x batch 19's). **Nothing is in either repo.** Every option marked **(applied)** is what the sheets show;
the others are one change away. No new in-game words.

Sheets (`t452forms_work/sheets/`):
- `t452forms_proteus.png`: today's three forms over the new ones; front, back, icon and shiny; 1x and 3x.
- `t452forms_overloaded.png`: the four forms, today over new, each in its own form palette, plus the one icon.
- Candidates: `cand_pro.png` (hooded), `cand_proforms.png` (edges and shell), `cand_ov.png` (weathers).
- Grids: `g_*.png`.

## PROTEUS (410, the DEOXYS slot; PSYCHIC / CONTEXT)

1. **Hooded (the Index's form, the top half of every sheet).**
   - A. i2i 6921 from today's hooded front at 0.8: a small hooded spirit with a white pointed hood, a dark face, two glowing orange eyes, a ragged cloak and thin arms **(applied)**
   - B. t2i 6901: a chibi witch-hat hood, teal, two big eyes. It drifts the furthest from T-440's look.
   - C. t2i 6902: a hooded doll.
2. **ALL EDGES (CONTENT's battle form).**
   - A. i2i 6921 from today's edged front at 0.8: the hood still up, both arms raised as two long blades, its cloak cut into points **(applied)**
   - B. i2i 6961 or 6962 from the new hooded front. These kept the hooded pose: the model would not raise the arms.
   - C. t2i 6971: a hooded cloak with no blades.

   T-440 says ALL EDGES throws the hood back. No draft of eight did that. A gives the raised blades and keeps the hood.
3. **SHELL (CONTEXT's battle form).**
   - A. i2i 6921 from today's shell at 0.8: a closed round hood like a cocoon, a dark face window, two orange eyes peeking out **(applied)**
   - B. t2i 6971 or 6972: a bigger hooded penguin-like body (more charm, less shell).
4. **One creature across the three forms.**
   - A. The same two glowing orange eyes in every form **(applied)**:
     - drawn by hand on the hooded face, because the clean wore away the draft's eyes;
     - the edged form's red eyes turned that orange, and its cyan visor darkened to the face's shadow;
     - the shell's orange eyes kept.

     Orange (hue about 28) is far from PSYCHIC's 312, so it is out of the hue trap. Every view draws through the hooded front's one palette, so the forms must share their accents.
   - B. Cyan eyes, matching today's shell lens.
5. **The hooded form's rust cloak tatters** (an accent, 5.8% of the front; hue 15, outside the trap).
   - A. Kept **(applied)**.
   - B. Greyed into the ramp, so the whole creature is PSYCHIC's one hue.
6. **Hand fixes (applied):**
   - the hooded draft's ground shadow taken off;
   - the navy line on both hooded forms set to the one INK, and the hood's pale-blue flecks greyed;
   - the dark ears and blades lifted to the ramp's dark step, so they no longer fill solid ink: the darkest body step is INK, so a near-black limb became a black shape.
7. **Backs.**
   - A. Each front mirrored with the face flattened to the hood's own light **(applied)**: the hood from behind; ALL EDGES from behind with the blades still raised; the shell closed.
   - B. Keep T-440's edged back (`proteus_back_attack.png`: the hood hanging down, no face) for ALL EDGES, in the old style.
8. **Icons.**
   - A. Draw all three with icon3 from each new front, on shared icon palette **1** (icon3's best fit for PSYCHIC) **(applied)**. `gMonIconPaletteIndices[SPECIES_DEOXYS]` goes from 0 to 1. One species has one icon palette, and all three agree.
   - B. Leave them to `genproteus.py`'s derived icons on palette 0, as today.

   The hooded and edged icons are thin at 1x, like today's.
9. **The battle frame.** PROTEUS has one front row and one back row, and both editions use them.
   - The wild or owned battle shows the BOTTOM half: CONTENT's ALL EDGES needs y_offset 9, CONTEXT's SHELL 14.
   - Today the front row is 1, measured off the old art. The back row is 13 (T-440's hand-lowered value).
   - Choices:
     - A. y_offset 11 for both views, a compromise: edges 2 px high, shell 3 px low **(recommended)**.
     - B. Split the rows by edition (`#if defined(FIRERED)` in both coordinate tables), 9 and 14.
     - C. Edges' 9, the shell floating 5 px.

   `ground.py` measures only a sheet's top half (the hooded form), so it would write 5 here. Do not run it on DEOXYS.
10. **THE ANNEX's overworld shapes** (`object_events/pics/pokemon/deoxys_a.png` and `deoxys_d.png`) are T-439's own drawings. `gbaowslots.py` remakes only `deoxys_n` from the new hooded top.
    - A. Leave the two as they are for now, and redraw them from the new forms as a follow-up **(recommended)**.
    - B. Redraw them in this job.
11. **Batch 19** set PROTEUS aside (its questions.md 1). Nothing there overlaps.

## OVERLOADED (385, the CASTFORM slot; CONTENT, Forecast)

12. **The weather forms are drawn from the new normal form** (image-to-image from batch 18's chosen draft, `overloaded_front_i2i_6622`), so each is the same cloud with big eyes and pink cheeks, changed by weather.
    - **Sunny:** i2i 6922 at 0.76. A ring of puffy sun rays round its head **(applied)**. B: i2i 6921, rounder, few rays.
    - **Rainy:** i2i 6922 at 0.76. Drawn up to a raindrop point, drops on its crown **(applied)**. B: t2i 6902, a true teardrop creature: the strongest raindrop, but another body, on grass.
    - **Snowy:** i2i 6922 at 0.76. A frosty cap, with a row of short icicles hung from its lower edge by hand (no draft drew them) **(applied)**. B: t2i 6902, a snow-capped cloud on legs. C: i2i 6921, a frost swirl on top (echoes vanilla's snowy).
13. **Each weather's palette.**
    - A. Each form gets its own 16 colours in the type Forecast gives it **(applied)**:
      - sunny ENTROPY (FIRE);
      - rainy FLOW (WATER);
      - snowy FROZEN (ICE).

      The engine loads `castformPalette[form]` whole, and `CastformDataTypeChange` makes the form that type. Colour carries the type, as invariant 5 asks, and vanilla's per-form palettes do the same.
    - B. Every form in CONTENT's bone ramp, with the weather carried only by its shape.

    Sun and hail are reachable: SUNNY DAY and HAIL are in 12 learnsets, and a daemon has DROUGHT.
14. **The hue trap (applied).**
    - The drafts' blue line and blue drops sit inside FLOW's (220) and FROZEN's (197) reach. gbasprite would rotate them to orange and purple. Instead, the dark line goes to INK and the rest is greyed into the ramp.
    - On the sunny form, the blue rim flecks in the rays were greyed (blue is not in ENTROPY's trap, but it read as stray blue).
    - Snowy's orange beak became a small pink mouth, as the normal form has.
    - Cheeks stay pink in all three; pink is out of every trap here.
15. **The pale bodies.**
    - A. Deepened **(applied)**. The drafts are near-white clouds. place_rich spreads a body's values from the ink up, so a pale body landed on the highlight steps and the sunny form read pale peach. Each body's values were spread half by a straight stretch and half by rank onto 110..250, keeping their order. ENTROPY's amber, FLOW's blue and FROZEN's ice now show.
    - B. As drawn: paler, nearer the normal form's bone.
16. **Backs.**
    - A. The front mirrored with the face flattened to the body's grey **(applied)**.
    - B. Batch 18's blur, as on the normal back. It leaves soft dark eye shadows; it was tried here and looked like eyes through fog.
17. **Icon.** CASTFORM has ONE party icon for every form (batch 18's, a cloud with its weathers). There are no form icons to draw.
    - A. As is **(applied)**.
    - B. Redraw it plain, now that the weathers are bodies.
18. **The normal form's top outline** (batch 18, installed). Its clean wore away the outline across the top of the cloud (a white body on white), so beside the weathers it reads open at the top.
    - A. Re-clean batch 18's chosen draft on a keyed ground, as done here (`prekey_hull.py`), and redraw the batch-18 sun, snowflake and drop on it. A small follow-up **(recommended)**.
    - B. Leave it.

## Found on the way (engine; not art, nothing changed)

19. **OVERLOADED's battle rows are vanilla's for every form, and that includes the normal form batch 18 installed.** In battle, CASTFORM's position comes from per-form tables in `src/battle_anim_mons.c`, not from `gMonFrontPicCoords`:
    - `gCastformFrontSpriteCoords`: today {32x32, 17}, {48x48, 9}, {32x48, 9}, {64x48, 8};
    - `sCastformBackSpriteYCoords`: 0, 0, 0, 0.

    So the new normal form already battles about 10 px low. Measured by the batches' rule (63 minus the lowest row; the box rounded to 8):
    - normal {64x56, 7}, back 7;
    - sunny {56x48, 10}, back 10;
    - rainy {48x48, 9}, back 9;
    - snowy {56x48, 8}, back 8.

    Options:
    - A. Set both tables to these values with the install **(recommended)**.
    - B. Only the three new weathers.
20. **CASTFORM shows no streaks in battle.** `BattleLoadOpponentMonSpriteGfx` and `BattleLoadPlayerMonSpriteGfx` (`src/battle_gfx_sfx_util.c`) apply the streaks and saturation to the buffer, then reload the raw `castformPalette[form]` over it for CASTFORM. Only saturation is re-applied (`Saturation_ApplyToLoaded`), so OVERLOADED's four streak slots stay blank grey in every form, normal included. The new forms carry streak markers, so a fix would light them.
    - A. Open it as a ticket: re-apply the streaks after the castform reload **(recommended)**.
    - B. Leave it.

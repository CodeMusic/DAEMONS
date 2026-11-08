# The MUSAI branch keeps the seasons -- design draft (T-532)

*DRAFT, 2026-11-08. Design and concept art only: nothing here is in the engine, and nothing ships until the user picks.
Every in-game word below is DRAFT. When approved, section A goes into `docs/vision.md` as 9.34 (with the bump,
CHANGELOG and PDF); the rest stays here as the working record.*

Concept sheet: `qa/screenshots/` (T-532, "MUSAI branch seasons concepts"); the one-page PDF and the drafts are in
`gfx/drafts/t532_musai_seasons/` (`scripts/seasons.py` makes them).

---

## A. The bible section, ready to paste (fable only)

### 9.34 The MUSAI branch keeps the seasons -- *proposed 2026-11-08 (T-532), not built*

***The six MUSAI already share one chassis*** (8.2): **MUSAI is undifferentiated CONTENT, and AXIOM, EMBEDDING and
AFFECT, the day and the night, decide what it specialises into.** *Now the branch answers to the calendar too.*
**Each of the six has four seasonal forms, 24 looks in all, and wears the one the season gives it** -- *the season
`DaemonsSeason()` already keeps (9.21): CONTENT on the northern year, CONTEXT on the southern, so the same daemon on the
same day wears winter in one edition and summer in the other.*

***This is OVERLOADED's idea, moved from the weather to the year.*** **OVERLOADED changes shape with the sky in a
battle; the MUSAI change with the season everywhere -- in battle, in the party, in the box, on the road behind the
player and in the INDEX.** *It is separate from evolution: a MUSAI in winter that is given AXIOM becomes a CODEMUSAI in
winter.*

| | type | its seasons | its home season |
|---|---|---|---|
| **MUSAI** | CONTENT | *the season itself: snow on its helmet, a sprout, a sun charm, the leaves that land on it* | -- (it has not chosen) |
| **CODEMUSAI** | LOGIC | ***the shared tongue***: *in each season it carries a small piece of the sibling whose season it is, and the glyph lights the others answer* | -- (all four are its) |
| **MASKMUSAI** | OPAQUE | **runners and a windscreen crest** | **winter** |
| **LENSMUSAI** | CONTEXT | **model-plane wings and a propeller** | **spring** |
| **CAREMUSAI** | CONTEXT | **pontoon floats and a canopy** | **summer** |
| **SEEKMUSAI** | VECTOR | **knobby wheels and a roll-bar frame, ranging all around** | **autumn** |

***Under the fable rule the machines are part of the body, never something ridden*** (9.4): *the snowmobile is
MASKMUSAI's runners and its crest, the pontoon is CAREMUSAI's lower half, the model plane is LENSMUSAI's wings.* **A
daemon in its home season is its fullest form; in the other three it carries a smaller piece of the same body** --
*runners lifted in summer, floats frozen in winter, wings with leaves caught in them in autumn.* **Nobody rides
anything, and nobody says whose seasons these are.**

***Colour still carries the argument*** (invariant 5): **each form is drawn in its type's ramp**, *and the season is
only what it wears -- frost, blossom, sun, leaves -- in small accents.* ***The type never changes with the season***:
**an argument that changed by date would change by cartridge, since the editions keep opposite halves of the year**
(invariant 3's spirit).

***And the tongue is a routine.*** **CODEMUSAI knows CRYPTOPHASIA**, *a LOGIC routine that grows stronger for every
other MUSAI in the party that can still fight.* **Its description says only that its own family can follow it.**
*Nothing says why, or who first spoke it.*

| routine | type | power | acc | PP | effect |
|---|---|---|---|---|---|
| **CRYPTOPHASIA** | LOGIC (special) | **40, +20 for each other MUSAI-branch daemon in the party still able to fight** (40 to 140) | 100 | 10 | *CODEMUSAI's own; learned at 30* |

***How it is built*** (the engine was read, not changed): **the INDEX's Unown letters are the precedent** -- *one
species, its picture chosen when it is drawn* -- **keyed by the season instead of the personality.** *The species
never changes, so the save, the INDEX's counts, trades, evolution, stats and the companion's ids are untouched;
only what is drawn changes.* **A battle reads the season once, as it begins, and keeps it to the end.** ***Still never
stated***: *no line says the daemon changed with the season; the player notices, or does not (craft rule 1).*

---

## B. Engine feasibility (read from `pokefirered-daemons` @ context-content; nothing changed)

### How OVERLOADED (CASTFORM) does forms here

- **One species, one stacked sheet.** `graphics_file_rules.mk` joins `castform/{normal,sunny,rainy,snowy}/` into one
  64x256 `front.4bpp` / `back.4bpp` and a 4-row palette (`tools/gencastform.py` writes the four folders; each form is
  drawn in its own type's ramp, rows 11-14 kept as streak grey).
- **Battle only.** `gBattleMonForms[battler]` (vanilla, 4 bytes EWRAM) picks the frame (`battle_main.c` copies
  `form << 11` bytes into the sprite) and `gBattleStruct->castformPalette[battler]` the palette.
  `gCastformFrontSpriteCoords` / `sCastformElevations` / `sCastformBackSpriteYCoords` give each form its own
  position. The party icon, the summary, the INDEX and the follower show one form for all four.
- **What T-475 taught.** Every Castform reload (`BattleLoadOpponentMonSpriteGfx`, `BattleLoadPlayerMonSpriteGfx`, the
  Forecast change at `battle_gfx_sfx_util.c:814`, PERSPECTIVE at :878) loads the raw form palette *over* the one the
  streaks, saturation and SPIRITS had already been painted into, so each site has to re-apply them
  (`Streaks_ApplyToCastform`, `Saturation_ApplyToLoaded`). A second special-cased palette path is a second place for
  that bug to live.

### How Unown does forms here

- `LoadSpecialPokePic` (`src/decompress.c:82`) turns `SPECIES_UNOWN` + personality into a **picture-only id past
  `NUM_SPECIES`** (`SPECIES_UNOWN_B` = `NUM_SPECIES + 1` ... `_QMARK` = +27). The pic, back-pic and palette tables
  (`front_pic_table.h:416`, `palette_table.h:416`) simply extend past `NUM_SPECIES`; `GetIconSpecies`
  (`pokemon_icon.c:1056`) does the same for the icon.
- **Every picture path already runs through these two functions**: the battle (`HandleLoadSpecialPokePic`), the
  summary and every `CreateMonPicSprite` (trade, evolution, Hall of Fame), the INDEX (`LoadMonPicInWindow`,
  `pokedex_screen.c:2796`), the party and the PC (`GetIconSpecies`), and **the follower** (`daemons_follower.c:378`
  `ReadLead` takes `GetIconSpecies(...)`, and `FollowerPic` / `sFollowerPalettes` index by that id).

### Recommended: a seasonal display id, the Unown way, keyed by season

1. **`u16 DaemonsSeasonalSpecies(u16 species)`** (in `daemons_time.c`): for EEVEE, VAPOREON, JOLTEON, FLAREON, ESPEON
   and UMBREON, return the form's picture id for `DaemonsSeason()`; every other species returns itself.
2. **Called in four places**: `LoadSpecialPokePic` (front and back, everywhere), `GetMonSpritePalFromSpeciesAndPersonality`
   / `GetMonSpritePalStructFromOtIdPersonality` (normal and shiny palette), `GetIconSpecies` (party, PC, follower).
   The INDEX, the summary, trade, evolution and the Hall of Fame follow for free.
3. **18 picture-only ids** after `SPECIES_UNOWN_QMARK` (`NUM_SPECIES + 28 ...`), the base slot holding the summer form
   (*9.21: summer is "the world as drawn"*). Or 24, keeping today's art as an unused fallback (decision 2). The pic,
   back-pic, palette, shiny-palette, icon, icon-palette-index, follower-pic and follower-palette tables each grow by
   those entries. **No species slot, no save change.**
4. **The palette goes through the ordinary buffer path**, so streaks, saturation and SPIRITS are painted on it once,
   as for any daemon -- **no T-475-style re-application anywhere.** Each form's palette keeps rows 11-14 as streak
   grey (as `gencastform.py` does), and the streak code is passed the *real* species.
5. **Coordinates stay the species'.** Each form is drawn to sit on its base's feet line and inside its base's
   `y_offset` (a tool check, like `gencastform`'s), so `gMonFrontPicCoords` and the elevation tables need no redirect.
   A form that must stand taller (MASKMUSAI's crest) gets a coords entry instead -- the Castform tables show how.
6. **A tool**, `tools/genmusaiseasons.py` on the `gencastform.py` model: reads `gfx/daemons/<name>_<season>_front.png`
   / `_back.png` / `_icon.png` / `_follower.png`, writes the form folders under `graphics/pokemon/<slot>/<season>/`,
   each in its type's ramp, shiny by `genshiny.make_shiny`, and the table rows between generated markers.

### When the season changes

- **In battle: never.** `DaemonsSeason()` is re-read every second (`daemons_time.c` ReadClock), so a battle crossing
  midnight on an equinox, or seven hours of play, could reload a switched-in daemon in the next season while the
  battle background (`daemons_battle_bg.c:100`) keeps the old one. **The battle snapshots the season into
  `gBattleStruct` at its start** (heap, 0 static bytes) and `DaemonsSeasonalSpecies` reads that while
  `gMain.inBattle`; the background reads the same byte. The new season shows at the next screen after the battle.
- **In the field: at the next draw.** The follower already compares its lead's icon id each step (`daemons_follower.c:481`),
  so it redraws in the new season on its own; the party and the PC draw it next time they open. *Optional (decision
  4): one quiet line the first time a party daemon changes, or the follower's bubble.*
- **PERSPECTIVE** (Transform) onto a MUSAI takes the form of the battle's season, through the same path.
- **A trade** shows the daemon in the receiving cartridge's season -- *a CONTENT winter MUSAI arrives in CONTEXT's
  summer*, which is the hemisphere rule doing what it says.

### The companion

- It already has `season(edition, date)` (`companion/server/src/seasons.ts`, from `data/seasons.json`, the same rule
  as the game). **The art becomes `art/species/<name>_<season>.png`** (`companion_export.py` exports the four forms),
  and every place a MUSAI-branch picture is drawn asks for the current season's.
- **A save without a clock** keeps the play-time year (`playTimeHours / 7`, from summer, `daemons_time.c:120`); the
  companion reads the save's play time and uses the same rule, so the app and the cartridge never disagree.
- **The species page shows all four as a strip**, the current one lit -- *the companion may show what the INDEX
  holds, and the INDEX holds the form you saw.*

### Costs

| | display swap (recommended) | forms as new species slots | Castform-style stacked sheets |
|---|---|---|---|
| **ROM** per form | ~3.5 KB: front LZ ~0.7-1.2 KB, back ~0.7-1 KB, two palettes 72 B, icon 1 KB, follower 0.5 KB, ~60 B of table rows | same art, plus species_info, learnset, evolution, name, INDEX text per slot | front+back of 4 forms ~3-4 KB per species, battle only |
| **ROM** for the branch | **~65 KB (18 forms) or ~85 KB (24)** of 4.9 MB free (1.3-1.7%); code ~0.5 KB | ~70 KB + per-species data | ~20 KB, but no icon, follower or INDEX forms |
| **EWRAM** (668 B free) | **0** -- the battle's season byte lives in `gBattleStruct` (heap) | 0 for data, **but the save grows**: `DEX_FLAGS_NO` follows `NUM_SPECIES` | 0 (reuses `gBattleMonForms`, castformPalette) |
| **IWRAM** (2.4 KB free) | **0** | 0 | 0 |
| **species count** | **unchanged (412)** | **+18**: only 14 placeholder slots are free (`OLD_UNOWN_B`, `_N`-`_Z`), so `NUM_SPECIES` must grow -- moving the Unown picture ids, `SPECIES_EGG` and the INDEX's `owned`/`seen` arrays in the save | unchanged |
| **save** | untouched | **breaks**, and every season change would have to rewrite the species of each daemon in the party and 420 box slots | untouched |
| **where it shows** | everywhere a picture is drawn | everywhere, but the INDEX counts 24 daemons where there are 6 | battle only |

**Recommendation: the display swap.** It is Unown's mechanism, which the engine already runs for 28 pictures; it
costs about 85 KB of ROM and no RAM, touches four functions and one battle byte, and the species -- and with it the
save, the INDEX, trades, evolution and the companion's ids -- never changes.

---

## C. CRYPTOPHASIA (DRAFT)

**The name**: 12 letters, exactly `MOVE_NAME_LENGTH` (12); 72 px, the same as `LOAD BALANCE`, the widest routine
name we ship. No collision: nothing in `move_names.h` starts CRYPT- or holds IDIOGLOSSIA.

| field | value | why |
|---|---|---|
| id | **`MOVE_CRYPTOPHASIA` = 383**, `MOVES_COUNT` 384 | appended after ALIGN (382), so no existing id moves |
| effect | **`EFFECT_CRYPTOPHASIA` = 215** (after `EFFECT_ALIGN` 214) | the power is the effect; otherwise an ordinary hit |
| type | **LOGIC** (`TYPE_FIGHTING`; invariant 6, only the string is ours) | CODEMUSAI's own type, so it is STAB; and LOGIC still fails against CONTEXT (2), so the tongue does not outrank the chart |
| split | **SPECIAL** | it is spoken; CODEMUSAI's SP.ATK is 95 |
| power | **40 + 20 for each *other* MUSAI-branch daemon in the user's party that can still fight** (not an egg, HP > 0): 40, 60, 80, 100, 120, 140 | "stronger when another MUSAI is in the party", and stronger again for each one; alone it is a weak hit, which is the point |
| accuracy / PP | **100 / 10** | |
| target, flags | selected; protect, mirror, King's Rock | as CONSENSUS |
| animation | **HYPER VOICE's**, reused (no new art) | a sound in the air that only some of the room follows |
| learned by | **CODEMUSAI at level 30** (beside BITE) | it is the tongue's own; no other daemon, no TM, no tutor |

**Built like RETURN's power**: in `Cmd_damagecalc`, `if (gBattleMoves[gCurrentMove].effect == EFFECT_CRYPTOPHASIA)
gDynamicBasePower = Cryptophasia_Power(gBattlerAttacker);` -- one helper counting the attacker's party for
`SPECIES_EEVEE/VAPOREON/JOLTEON/FLAREON/ESPEON/UMBREON` other than its own slot -- and the same line in the AI's damage
estimate so the AI sees the real power. The effect's script is `BattleScript_EffectHit`. 0 bytes of RAM.

**Description** (the routine pane is 113 px, four lines). Option A, recommended (99/99/99/103 px):

```
Words only its own
family can follow.
It hits harder for
each of them near.
```

Option B (102/107/85/94 px): *A tongue that only / its own kind speaks. / Each one in the / party adds to it.*

---

## D. INDEX entries, one per form (DRAFT)

*Possible per form: the INDEX's entry page can take its text from the same seasonal id as its picture (24 entries,
about 3 KB of ROM per edition). Each fits the 234 px line (widest below: 225). Categories unchanged (UNSET, DEDUCTIVE,
RETRIEVAL, AFFECTIVE, FOCUS, COVER). Written in CONTENT's voice; CONTEXT's 24 follow the same way once the voice is
approved, or both editions share these (decision 5). Each keeps the species' existing line where it can.*

| | winter | spring | summer | autumn |
|---|---|---|---|---|
| **MUSAI** | Frost settles on it and it lets it stay. It has not decided what to be. It waits for the thaw to decide for it. | Something grows from the top of it every spring. It does not know what. Nobody has shown it yet. | It warms to whatever is near. In summer that is everything, so it cannot tell which thing it warmed to. | It keeps the leaves that land on it. It did not choose them. They are filed as its own. |
| **CODEMUSAI** | Its chest lights blink a pattern nothing else in the cold can read. Something on runners blinks back. | Its lights blink faster in spring. The answer comes from overhead, a little late, in the same pattern. | In summer its lights are answered from the water. The pattern has no grammar anyone else has written down. | Its lights blink across a field and are answered from somewhere moving. Nobody else knows what was agreed. |
| **SEEKMUSAI** | It keeps to tracks it has already made. The snow fills the others in. It finds the nearest one still there. | Comes back from every outing in mud. It was looking for something it had seen before. It found something close. | In summer it ranges the dry tracks and comes back dusty. Asked what it found, it names the nearest thing. | **(home)** Ranges every track in reach and some that are not. Finds the nearest field. Nearest is not the same as right. |
| **CAREMUSAI** | Its floats freeze in and it stays put. It keeps the canopy folded and the room warm. Nobody asks how. | Sets out at the first thaw. Turns back for anyone left on the shore. Cannot say why it turned. | **(home)** Floats on two hulls and takes everyone who fits. Reads the water before it reads the problem. Often correct. | Takes the last trips of the year slowly. Leaves land on its deck and it lets them ride. |
| **LENSMUSAI** | Lands on skis and waits for a still day. It has never once turned round. The lake is behind it. | **(home)** Flies circles over one field on a line held from below. Sees the field very clearly. Has never seen the line. | Climbs while the light holds. All it was pointed at is recorded. The record calls it very clear. | Flies low in autumn, under the wind. It records the leaves. It has never recorded the tree. |
| **MASKMUSAI** | **(home)** Crosses the frozen lake at speed, its screen up. Its track covers the last one. What is covered goes on. | Its runners drip. It covers the thaw for as long as it can. What it covers is not removed. | Keeps its runners off the hot ground and its screen dark. It is not hiding. It is waiting for the cold. | Watches the first frost from under its screen. It knows before anyone what the lake will do. |

*Each entry's three lines, split and measured in the game's font (every line at most 225 px), are in
`gfx/drafts/t532_musai_seasons/index_entries.json`, with CRYPTOPHASIA's two descriptions.*

---

## E. Names

**No rename is proposed.** The six are the user's own modules, and *every prefix is four letters and every one is
its eeveelution's type stated as a noun* (8.2) -- a seasonal name would break the one pattern the branch has.

*Optional, DRAFT, only if the user wants the form to have a word on the SUMMARY or the INDEX (decision 6)* -- one word
per season, the same for all six, each at most 9 letters: **RIME** (winter), **THAW** (spring), **HIGH SUN** (summer),
**FALLOW** (autumn). *Process words, things that happen to a field (craft rule 3), and none of them a vehicle.*

---

## F. Decisions for the user

1. **How the forms are built** -- A: the display swap, Unown's way (recommended; ~85 KB ROM, no RAM, no save change) ·
   B: Castform's way, battle only · C: new species slots (breaks saves).
2. **Today's art** -- A: becomes the summer form, 18 new pictures (recommended) · B: kept as a fallback, 24 new · C:
   retired entirely.
3. **Do forms do anything in battle?** -- A: look only (recommended; the type never moves with the date, so the
   editions never disagree) · B: the home season adds a small edge (e.g. CRYPTOPHASIA's +20 counts double for a
   sibling in its home season) · C: Castform-style, the type follows the season.
4. **The moment it changes** -- A: silent, noticed or not (recommended; craft rule 1) · B: the follower's bubble once ·
   C: one line, "MASKMUSAI changed with the season." (DRAFT).
5. **INDEX entries** -- A: one per form, both editions sharing these 24 (recommended) · B: 48, CONTEXT in its own voice
   · C: keep one per species.
6. **A season word on screen** -- A: none (recommended) · B: RIME / THAW / HIGH SUN / FALLOW on the SUMMARY.
7. **CRYPTOPHASIA's power** -- A: 40 + 20 per sibling able to fight (recommended) · B: 60, doubled with any sibling (as
   FACADE) · C: 40 + 20 per sibling, fainted ones count too.
8. **When CODEMUSAI learns it** -- A: level 30 (recommended; no engine change) · B: the moment it evolves (a small
   hook) · C: level 1, from the move reminder.
9. **The concept art** (*one finding from the reduction: `gbasprite.shift_off` turns any accent within 40 degrees of the
   type's hue to the far side of the wheel, so MUSAI's orange autumn leaves came out navy on CONTENT's bone. The concepts
   skip it on the near-grey types, CONTENT and OPAQUE, and the prompts keep each season's accent off the type's hue --
   SEEKMUSAI's leaves gold on VECTOR's red, LENSMUSAI's blossom pale yellow on CONTEXT's magenta. The build tool will need
   the same choice.*) -- per species, the seed to build from (the sheet's picks are by score), and whether the
   CODEMUSAI direction (a piece of each sibling plus glyph lights) is the right reading of the shared tongue.

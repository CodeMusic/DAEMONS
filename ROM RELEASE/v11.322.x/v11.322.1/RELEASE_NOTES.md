# DAEMONS v11.322.1 — release notes

*Released 2026-10-29 09:35 · built against the design bible v11.322*

- **Engine**: CodeMusic/pokefirered-daemons `4b19d34c3` (context-content)
- **Design**: CodeMusic/DAEMONS `2c824443`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `8da9b055e0745b897e5e643c2cddbde786ba9b3d` |
| `daemonsContext.gba` | CONTEXT | `d10250245ac983716cf48bc1b37d2fdd0a37231f` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `4f8888ee9729514570562fef0a5ee7f7ac2999ac` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `13fed1c5c91e85b1f924b1b244a954c3a65db566` |

## The engine since v11.320.4

- `4b19d34c3` T-484: the plateau's paving loses its magenta specks; a special-slot NPC's reflection takes its own colours
- `adf935265` T-449: the map's icons and cursor in ink
- `fe8df1f55` T-483: FLAG_GOT_HERMETIC_LAYER reserved (0x3F3, absolute 0xCF3) for THE HERMETIC LAYER, set in the game or by the companion

## The design and tools since v11.320.4

- `2c824443` T-484: gbageneral never steps onto an unfilled colour; check_palettes fails any redrawn map tile that does (engine 4b19d34c3)
- `a1c075f2` TODO: T-481 A drafted, the user's answers; T-449's icons and cursor kept (the user)
- `71ee6abe` TODO: T-484 filed -- batch G's findings in the theatre
- `baf0e81f` companion_export: THE HERMETIC LAYER (hermetic.json) and flags.hermetic_layer (T-483, C-238)
- `6aaa31c6` Bible v11.322: THE HERMETIC LAYER, SPELLCRAFT, and the one exception (4.39, 0.1)
- `76362233` qa: C-237 the witching hour's face, SPELLCRAFT, Halloween (a mock-up); C-239 the SPELLCRAFT card face
- `f06eda4a` C-238: THE HERMETIC LAYER's text, DRAFT -- the third book, SPELLCRAFT
- `70108e7e` T-449: gbaregionmap.py draws the map's cursor and icons in ink; the sheet
- `56aab6d1` Theatre: batch G, the CORPUS and REVIEW BOARD cards, pair 3 and OVERLOADED as the foe filmed (T-438, T-445, T-456, T-447, T-475)
- `7e16bf3f` T-481 A draft: tools/gbabattlebg.py, the battle terrains that keep the calendar (report and sheets, no --write)
- `0cada7a5` TODO: T-483 THE HERMETIC LAYER and SPELLCRAFT, the game's half; T-482 takes the shared pulse
- `91617987` TODO: T-481 backgrounds that keep the calendar; T-482 the witching hour's red-blue pulse in battle (the user)
- `59f6d7f1` Bible v11.321: the witching hour, as built (T-480, C-236)
- `949a903d` TODO: T-480 struck -- released v11.320.4
- `8fbfec33` manual: rebuilt for v11.320.4
- `fcda04b3` ROM release v11.320.4: T-480 the witching hour, the game's half (DRAFT)

## The design bible's own entry for v11.322

### v11.322 — 2026-10-29

### THE HERMETIC LAYER: SPELLCRAFT, and the one exception

- ***4.39, new (the user's brief and two multiple-choice answers)***: **a third book, a grimoire drawing on the GUIDE and THE SUBTLE LAYER, unlocks SPELLCRAFT**; SPELLBOOK in the game, readable only at night. **It is the one exception to 0.1**: its words may say some of the thesis, shadowed, behind a warning and an author who may be mad, and its spells may bend play; the type chart, the four secrets and the user's story stay fixed. Its contents (As Above So Below, THE TABLET OF THE HANDS and OF GRAVITY, the Folds, entanglement, THE BOOK OF THIRTEEN, the Blank Tablet), its pulse, its two unlocks, the hour's inverted pairs and Halloween recorded. **Built book first, the spells in steps.** Every word DRAFT.
- ***0.1***: a line naming the exception.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

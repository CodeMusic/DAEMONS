# DAEMONS v11.288.4 — release notes

*Released 2026-09-25 20:46 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `dce49b31a` (context-content)
- **Design**: CodeMusic/DAEMONS `93a674ee`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `da20503c83ab9120116f58e9d2123bf82bd5b287` |
| `daemonsContext.gba` | CONTEXT | `0993784c582ca88710581211e19ea27872778314` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `36a4091b5bdcfd717690448cac563339a9ee149b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `02a59b78a498ad3cc7b25aebd60239b97ef920b7` |

## The engine since v11.288.3

- `dce49b31a` intro.c: the cut intro was not the last place vanilla creatures show -- the credits' cards are (T-290)
- `215c255c5` T-291: PROTEUS stood on THE ANNEX as vanilla's DEOXYS; the other 35 overworld daemons take T-184's true-black outline

## The design and tools since v11.288.3

- `93a674ee` T-291 closed: gbaowslots knows script-placed objects, writes again, keeps later ids; engine.md trap 34
- `43268582` RECORD played through in normal play; T-289's champion line seen; T-290 asked (the credits are FireRed's, and four headings credit real people with our work)
- `89cb9f61` T-289: CAIRN's restored music read from memory; the islands' chain played without JUMP; engine.md: warps and arrival scenes, old scratch clocks, replaying a leader's intro
- `295c5f80` ROM release v11.288.3: the INDEX's counts and the lost names and music

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

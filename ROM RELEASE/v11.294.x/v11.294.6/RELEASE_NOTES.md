# DAEMONS v11.294.6 — release notes

*Released 2026-10-03 18:58 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `a97cf9746` (context-content)
- **Design**: CodeMusic/DAEMONS `6fb46b93`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ed898b1e7019083d51032a735acaa438f6101daa` |
| `daemonsContext.gba` | CONTEXT | `bd506f0a183030f909ab1f9e8530d07cab142cf7` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2be03d1de86de058fbdfd76c44f5b7cfa25e9bd2` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9deaea92906038499e00c516e4016296b46c448a` |

## The engine since v11.294.5

- `a97cf9746` CRYSTAL asks whether you remember his name, and laughs when you do (T-362)
- `ac66dd45d` CALLOW: a gate in the fence beside the school, the strip below the ledge's way out (T-361)

## The design and tools since v11.294.5

- `6fb46b93` T-361, T-362 closed; T-363 opened (the user chose A); check_reach finds traps (engine.md trap 42)
- `0aeb6cec` T-359: the seasons' cost against engine.md's budgets, and the one-pass join with the faded print and the watch
- `0dabf428` ROM release v11.294.5: OPUS's margins for all 110 of T-210's daemons (T-356)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

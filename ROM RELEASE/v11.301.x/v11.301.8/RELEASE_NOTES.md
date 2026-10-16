# DAEMONS v11.301.8 — release notes

*Released 2026-10-16 14:11 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `d7958c704` (context-content)
- **Design**: CodeMusic/DAEMONS `a5e63202`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `88ed2bc5bb53316dd5da6fa46b6c8b134765474c` |
| `daemonsContext.gba` | CONTEXT | `9cf68b9f31ec48d65c0a9c4341f41c079e252d48` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `849cc2d0b2e4c1115892ddd6d9ca3c80a85cb1e8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d6b76d0c4096fa4ac22b913524fbc082fdd0aa32` |

## The engine since v11.301.7

- `d7958c704` SCORN's party converged (the user, 2026-10-16: "go with the stack"): SCHEDULER, KEEPER, STAMPEDE, ESCALATE, MIGRATE, 47-50, perfect IVs, every one UPHEAVAL / DISCHARGE / FREEZE / RADIATE -- one streak on five bodies, nothing rolled on his side
- `5c949f388` T-409 (the user, 2026-10-16): the fir sings in B-flat, the painting's key -- green, purple x3, red, orange x4, red, orange, yellow, blue, red, purple; MUS_NEXUS a whole tone up with it

## The design and tools since v11.301.7

- `a5e63202` qa: the BOX-3's suggested mouths, for checking (companion C-138)
- `ddab37f7` T-413 (engine d7958c704): SCORN's party converges, the stack; T-409's blue confirmed
- `3c4bfbc5` TODO: the user's answers (2026-10-16) -- T-409 B-flat (built), T-406 parked, T-407 season and time homes, T-408 music from the user's songs
- `aa87150e` qa: T-409 in B-flat
- `d07b7e07` T-409 (engine 5c949f388): gennexustheme sounds MUS_NEXUS in B-flat
- `c4556d87` T-408: a grove-look pilot (GUESSWORK, THE EMPATHVERSE), not used -- the model drew no mask
- `7dc06f0c` TODO: T-405, T-410, T-411, T-412 drafted (field page q-push79); T-406, T-407 asked
- `9a0b479c` ROM release v11.301.7: the grove universes' NEXUS signs (T-408), the fir's notes seen and MUS_NEXUS (T-409, DRAFT), the glitch effect in DEBUG (goal B, DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

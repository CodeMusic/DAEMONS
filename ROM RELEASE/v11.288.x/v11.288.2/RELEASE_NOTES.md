# DAEMONS v11.288.2 — release notes

*Released 2026-09-25 18:35 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `ddee3e840` (context-content)
- **Design**: CodeMusic/DAEMONS `5cc0d672`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `47cd2fb887d105922852d4df6fe27e8a338bc0d7` |
| `daemonsContext.gba` | CONTEXT | `d90e4766794e29d1af3e6af4ea46fd545884eb45` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f9063c83ea6b6e840c6f7ad221c33b6afa278b0d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `bf8e48e7c57a88ad6ba8dfe09aa2adc6c34b772c` |

## The engine since v11.288.1

- `ddee3e840` T-287 (DEBUG only): a warp the theatre can fire -- gDaemonsDebugWarp, taken once the player has control

## The design and tools since v11.288.1

- `5cc0d672` T-286 seen on screen, T-287 closed, T-288 asked; engine.md: the theatre warp; CLAUDE.md: check_reach's doors and flags
- `913c6c7c` check_reach: doors and flags too; T-284/285 played, T-286 seen, T-287 closed (the theatre warp), T-288 asked (SCIENTIST GIDEON)
- `14a28300` ROM release v11.288.1; v11.287.x sealed (its last ROMs kept, seven notes in one PDF)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

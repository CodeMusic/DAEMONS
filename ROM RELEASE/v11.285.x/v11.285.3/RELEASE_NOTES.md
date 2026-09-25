# DAEMONS v11.285.3 — release notes

*Released 2026-09-25 10:37 · built against the design bible v11.285*

- **Engine**: CodeMusic/pokefirered-daemons `b8bbf0794` (context-content)
- **Design**: CodeMusic/DAEMONS `5e9d97e9`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4b4751ae030dcd1917b6494b4e6b1ea655896825` |
| `daemonsContext.gba` | CONTEXT | `12a8decce7a41ce58230a92beaae55fd5d5b8708` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `99ae7e193a624b76c2329b5be51b5d9f2c76d1a6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7f1e0e70444bb595d10c38cf68e4e14a7bb7c04e` |

## The engine since v11.285.2

- `b8bbf0794` T-270: the player on the trainer card is the monkey; B backs out of DEBUG

## The design and tools since v11.285.2

- `5e9d97e9` T-270 closed: the monkey on the trainer card; engine.md trap 32 (name gbachar's jobs when writing)
- `6eae4ebd` ROM release v11.285.2: the Guide reads on one wide page

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

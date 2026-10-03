# DAEMONS v11.292.4 — release notes

*Released 2026-10-03 11:17 · built against the design bible v11.292*

- **Engine**: CodeMusic/pokefirered-daemons `c969ebea2` (context-content)
- **Design**: CodeMusic/DAEMONS `ebd55857`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `775bf95eb303ef67c4a6d1f0b5f0b64659666d5b` |
| `daemonsContext.gba` | CONTEXT | `4e8bb7b3759dee71052888c97c159947bf396bb3` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `98e6935ead0320088f488695745493bde9b49dbc` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `01971d80a31d26ad928c27574781439a41c51595` |

## The engine since v11.292.3

- `c969ebea2` T-355: the school lift's lamp -- green at rest, blue from choosing a floor until the player can move again

## The design and tools since v11.292.3

- `ebd55857` T-355: the lift's lamp (engine c969ebea2); HOW_TO_PATCH says how a cartridge keeps its save across releases
- `e90f28d2` qa: T-352, the school's stairs before and after
- `8d68d8dd` ROM release v11.292.3: the playthrough's school notes (T-351..T-354) and the legendaries' routines

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

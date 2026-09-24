# DAEMONS v11.283.3 — release notes

*Released 2026-09-24 10:45 · built against the design bible v11.283*

- **Engine**: CodeMusic/pokefirered-daemons `f744e863b` (context-content)
- **Design**: CodeMusic/DAEMONS `c81a6b97`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0926d32c16133c7dfce167a444c6baad544a0cb5` |
| `daemonsContext.gba` | CONTEXT | `7ac70658387e3a0c4f82322e6ed8465952de07c4` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `526648365fa1065216a3ae402533442e7bbf2bb6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a27f49621704dfc9841c09ce8bed9497af699b8c` |

## The engine since v11.283.2

- `f744e863b` HELP: BUTTON MODE's page still offered the HELP setting T-179 removed

## The design and tools since v11.283.2

- `c81a6b97` T-262: a fresh clone and setup.sh from nothing both build the same game
- `244c4e36` The GBA build is where the game is: four files still called it a spike
- `2ebdf1bb` tools/check_fresh_clone.py: does a fresh clone build this machine's ROMs?
- `aebd7042` ROM release v11.283.2: nobody is son or lassie; four vanilla leftovers

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

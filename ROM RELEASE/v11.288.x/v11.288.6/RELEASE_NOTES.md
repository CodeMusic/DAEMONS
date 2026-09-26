# DAEMONS v11.288.6 — release notes

*Released 2026-09-25 22:37 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `b414d41d9` (context-content)
- **Design**: CodeMusic/DAEMONS `36a0f3b5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `196f8dc7460631eb8b8c66f2a1ae8076e8ea4b9b` |
| `daemonsContext.gba` | CONTEXT | `c9d805628d76f0ce80ee3f28adfcdf064549929a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `3f7327b5932209dbf5d97c9d92232b5112eedc3e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `cbf7d2b9fdfa7014509c171ba3015915997b76b9` |

## The engine since v11.288.5

- `b414d41d9` T-294: four receipts no longer announced twice; a trainer win names the player

## The design and tools since v11.288.5

- `36a0f3b5` T-294 closed, T-295 asked: a new game in CONTEXT, played to the forest
- `bd93d82a` ROM release v11.288.5: twelve daemons' streaks switched on; DARIO follows PSYCHIC F

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

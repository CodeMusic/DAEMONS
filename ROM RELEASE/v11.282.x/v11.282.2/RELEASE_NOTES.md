# DAEMONS v11.282.2 — release notes

*Released 2026-09-24 09:46 · built against the design bible v11.282*

- **Engine**: CodeMusic/pokefirered-daemons `796e6cbaa` (context-content)
- **Design**: CodeMusic/DAEMONS `19c51854`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c7d767dd8c696f245fa241afc4f406005ca7a096` |
| `daemonsContext.gba` | CONTEXT | `2ed2f1136900f17fb84b029a72a7325e920d40e1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `61ec05b9b64c0078005dd5f039196048406ec91f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d4ee2b8cd45038a17beed3af43e0c28d9510efa1` |

## The engine since v11.282.1

- `796e6cbaa` T-260: vanilla's GOLD TEETH is the WARDEN's TOKEN

## The design and tools since v11.282.1

- `19c51854` T-10: proposed for a grove's tree rather than BRAZEN's approved maze
- `5798e734` T-261: 8.6's adopted-not-built list is partly stale; the triangle is a question
- `3149ed06` T-260: the WARDEN's TOKEN, logged and closed
- `62dc7e48` ROM release v11.282.1; v11.281.x sealed into one PDF

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

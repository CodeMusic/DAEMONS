# DAEMONS v11.288.7 — release notes

*Released 2026-09-25 23:55 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `0257268e8` (context-content)
- **Design**: CodeMusic/DAEMONS `b5287e1f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7821d5a24b54f665433ac4aa0cd66e68b7b92b02` |
| `daemonsContext.gba` | CONTEXT | `fb36169af4174526f2a27bcdd116b4486f84eaa5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9eebd06125ba1942832bf01829f0f30eed343fc5` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4186a7460f85ffa4a018bef891f339f070f88999` |

## The engine since v11.288.6

- `0257268e8` T-295: CRYSTAL and AL in their own voices (DRAFTS); T-296: USERBOXES

## The design and tools since v11.288.6

- `b5287e1f` T-295 drafted and built (40 strings, waiting on the user's approval); T-296 closed (USERBOXES)
- `c42357e2` ROM release v11.288.6: receipts announced once; a trainer win names the player

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

# DAEMONS v11.283.2 — release notes

*Released 2026-09-24 10:12 · built against the design bible v11.283*

- **Engine**: CodeMusic/pokefirered-daemons `a1ba618c6` (context-content)
- **Design**: CodeMusic/DAEMONS `6e7e35d3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1cd530741df258c3e2d64398e936ba7d97117db0` |
| `daemonsContext.gba` | CONTEXT | `e8f373ad4aba25f0a71b2bae5a59f9b42a62378e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `4d4eaccccdeb67139a2c9cc1d62cb746f3754678` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b2001208dab036972761673288a3d34783f0f4dc` |

## The engine since v11.283.1

- `a1ba618c6` DEADSTACK in capitals, as the map and every other place name are
- `16d8280ed` Four lines vanilla left behind: a Pikachu in a cry, a Chansey in another, grasstype, Blanche

## The design and tools since v11.283.1

- `6e7e35d3` check_lexicon: vanilla species names in any case, as whole words
- `85b3f230` ROM release v11.283.1; v11.282.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

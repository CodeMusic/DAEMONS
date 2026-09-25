# DAEMONS v11.288.3 — release notes

*Released 2026-09-25 18:53 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `14278b042` (context-content)
- **Design**: CodeMusic/DAEMONS `ab6c54d2`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a8f55e17d2c21303d703e28d668a2736f7a6968b` |
| `daemonsContext.gba` | CONTEXT | `a2e0780fd6b8483180eb648ce9d78b034e453302` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `67e54120dfe2041db904077e47f01c70001301c6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4b925388198b791777fb4ee7a5a8b20ad3ff10ad` |

## The engine since v11.288.2

- `14278b042` T-289: the values and sounds port_dialogue dropped -- the INDEX rating's counts, the fossil's names, the champion's first daemon, seven leaders' music and VIRIDIAN's fanfare

## The design and tools since v11.288.2

- `ab6c54d2` T-289 closed: port_dialogue keeps Gen 1's values and vanilla's closing sound, and refuses a whole-tree --write; check_reach guards lost values
- `9b2b37e5` ROM release v11.288.2: the theatre warp in the DEBUG builds

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

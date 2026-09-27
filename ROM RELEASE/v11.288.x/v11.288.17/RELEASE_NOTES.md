# DAEMONS v11.288.17 — release notes

*Released 2026-09-27 11:22 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `c50c919f0` (context-content)
- **Design**: CodeMusic/DAEMONS `bafcd82e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7c156abee8a38df52aa48455d0982e1e2f07a1cc` |
| `daemonsContext.gba` | CONTEXT | `e6369fe5b4e70e33466608c55d086f0caddb6194` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `360a5908e0aeab2d493616087b3b358c09c1650e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `351cb5a312d9d660476c6d37df99eb67c58a365c` |

## The engine since v11.288.16

- `c50c919f0` DEBUG JUMP's second page: WARDEN, the singing FIR, the WITNESSES' reward; short DEBUG pages no longer cut their last row off (MART's BACK read RACK)

## The design and tools since v11.288.16

- `bafcd82e` JUMP's MORE page, the menu clip fix, the playtester kept current, the bible's status notes
- `7aeef7e5` ROM release v11.288.16: the map comes clear

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

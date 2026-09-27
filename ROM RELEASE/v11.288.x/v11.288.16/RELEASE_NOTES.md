# DAEMONS v11.288.16 — release notes

*Released 2026-09-27 10:00 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `e02af24dd` (context-content)
- **Design**: CodeMusic/DAEMONS `2552c54d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7c156abee8a38df52aa48455d0982e1e2f07a1cc` |
| `daemonsContext.gba` | CONTEXT | `e6369fe5b4e70e33466608c55d086f0caddb6194` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `59de9ad203b2274353787f0ac096817cefba58bf` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `dbcbe090c06fa778cf2371cb4d6f3680d1e08f74` |

## The engine since v11.288.15

- `e02af24dd` Understanding shown as clarity (T-317, DRAFT): the TOWN MAP's land and sea resolve as understandings arrive -- mosaic 2x2, then 2x1, then sharp; names, cursor and icons stay crisp

## The design and tools since v11.288.15

- `2552c54d` T-317 built: the map comes clear
- `691d91f8` ROM release v11.288.15: virtues with the MARKS; the witnesses' room

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

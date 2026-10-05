# DAEMONS v11.295.7 — release notes

*Released 2026-10-05 16:15 · built against the design bible v11.295*

- **Engine**: CodeMusic/pokefirered-daemons `33573b876` (context-content)
- **Design**: CodeMusic/DAEMONS `c4623472`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `fcbed96d28963b738f95ec8c5ba1c27b772ec0f0` |
| `daemonsContext.gba` | CONTEXT | `d334431cdaef199e94c6498ae8b3885bf30d9316` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f0d5b94e99cd1de1de9861468dcb83a41a8544d3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4f6f89d897284d8cc4762497f115267d28769055` |

## The engine since v11.295.6

- `33573b876` T-376: VERA's tending -- the line before it no longer names the daemon (it read "/235 settles."), and the narration is grey

## The design and tools since v11.295.6

- `c4623472` T-376 closed (engine); T-321: the gym statue, SAMMY and VERA seen; the walker fights through every routine slot
- `e0bca394` ROM release v11.295.6: the SLATE curator's exhibit is 'This exhibit' (T-375)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.290.6 — release notes

*Released 2026-10-01 19:12 · built against the design bible v11.290*

- **Engine**: CodeMusic/pokefirered-daemons `0cf2e6126` (context-content)
- **Design**: CodeMusic/DAEMONS `ab943ba6`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e15fc95cd8b68d23d56f3841799eb64e854be261` |
| `daemonsContext.gba` | CONTEXT | `cc3bc39f39314012f40e27684db21268507ebc3d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e6f1153052af50908bdcfe1b7563082094fecedc` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `195be509c96ef9c2ddd519c45111f9495cd041a1` |

## The engine since v11.290.5

- `0cf2e6126` T-297: DOLDRUM CAVE's hint -- a DOLDRUM resident looks out across the water and changes the subject (DRAFT; was vanilla's encyclopedia line)
- `7089b3d14` T-297: the NOTEBOOK's placed pages shimmer under REVEAL until read (src/data/notebook_finds.h, written by tools/gbadocs.py)

## The design and tools since v11.290.5

- `ab943ba6` T-297: gbadocs writes REVEAL's rows for the placed pages; the groves, the pages, DOLDRUM CAVE and OPUS recorded; FOLDS' corner waits on a verdigris_block rebuild
- `838ff915` ROM release v11.290.5: CRYSTAL hints at OPUS, the rival is eager, the attendant wishes for the GUIDE, quieter sparkles before REVEAL (T-338..T-343)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

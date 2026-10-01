# DAEMONS v11.290.7 — release notes

*Released 2026-10-01 19:26 · built against the design bible v11.290*

- **Engine**: CodeMusic/pokefirered-daemons `d0cacd32d` (context-content)
- **Design**: CodeMusic/DAEMONS `f90e1dd5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `300827e9b78d3062973fa639d85ddc19142a53c5` |
| `daemonsContext.gba` | CONTEXT | `002ed999bc6c6319b2433661a4758900ee13cee9` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e4ef457f62ce3f904b1871fda211230058eca542` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6285eb2e612a13fc8876ce471faaa0cae637eadf` |

## The engine since v11.290.6

- `d0cacd32d` T-297: FOLDS' blind tell -- a corner of paper under the bottom-left of the painting's frame (tools/gbainterior.py verdigris_block, rebuilt)

## The design and tools since v11.290.6

- `f90e1dd5` T-297 closed: gbainterior draws FOLDS' corner of paper into CONDOMINIUMS 3F; every approved find has its hint
- `838b4172` ROM release v11.290.6: the NOTEBOOK's pages shimmer under REVEAL, DOLDRUM's resident looks out across the water (T-297)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

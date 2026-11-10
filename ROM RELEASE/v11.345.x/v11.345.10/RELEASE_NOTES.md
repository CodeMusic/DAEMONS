# DAEMONS v11.345.10 — release notes

*Released 2026-11-10 15:06 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `18b63cf82` (context-content)
- **Design**: CodeMusic/DAEMONS `7e1a516e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `16d181346f20d7c58d5d936d72802cfe99b1563d` |
| `daemonsContext.gba` | CONTEXT | `ff4a7ea9116aebc9d5f4070a08c641248406a4e8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b88b1a60d8b9b63a33b28ff7b5d13db29f486e14` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3f1d8cc06ce48431fdd0093cd230f01fc55c6133` |

## The engine since v11.345.9

- `18b63cf82` T-541, A THE SLATE: SLATE's MUSEUM OF ERRATA's tileset (secondary/museum) redrawn in place, rows 8, 9, 10 recoloured -- ERRATA 1F/2F, the WARDEN's house, SELPHY's house (the user, 2026-11-10: "A The slate"; DRAFT)

## The design and tools since v11.345.9

- `7e1a516e` T-541 built (engine 18b63cf82), A THE SLATE: gbamuseum APPROVED {A}, in check_generators; qa 10Nov2026 T541 43-46; route t541_slate (DRAFT)
- `fd7e2161` T-541 drafted: SLATE's MUSEUM OF ERRATA inside, from 4.32 -- three directions (A THE SLATE, B THE INDEX, C THE STRATA), tools/gbamuseum.py; qa 10Nov2026 T541 39-42 (DRAFT)
- `62b77127` T-533: the user's picks and the core thread, 2026-11-10 -- recorded and drafted in docs/private/, nothing built
- `c0b1d539` ROM release v11.345.9: T-437 the SCREEN font (the user: ship it as is) and T-538 batch 3 A THE KEEPING (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

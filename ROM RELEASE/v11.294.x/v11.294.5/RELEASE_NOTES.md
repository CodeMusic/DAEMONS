# DAEMONS v11.294.5 — release notes

*Released 2026-10-03 17:17 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `bf8dbf7ff` (context-content)
- **Design**: CodeMusic/DAEMONS `b3d3eb12`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9a3697835122617f0c8501d9c3de42f7ec3c5ae5` |
| `daemonsContext.gba` | CONTEXT | `65e5d26c75d47ba5388dd3725d145b747006b12d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `413971c2bf8ba94a7739749379ab0d16797697f9` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9722aa39dba48df90ad30bbe496fe1f30b7d0628` |

## The engine since v11.294.4

- `bf8dbf7ff` OPUS's margins for T-210's batches 4-7: dragons and fossils, the Hoenn routes, the legendaries (T-356)

## The design and tools since v11.294.4

- `b3d3eb12` qa: T-356, the rest of batches 5-7's margin sheets
- `61a20ae6` T-356 closed: OPUS's margins for all 110 of T-210's daemons, batches 4-7
- `7e29ca6a` ROM release v11.294.4: OPUS's margins for the starters and the water families (T-356, batches 1-3)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.314.2 — release notes

*Released 2026-10-27 21:20 · built against the design bible v11.314*

- **Engine**: CodeMusic/pokefirered-daemons `b5f248bd9` (context-content)
- **Design**: CodeMusic/DAEMONS `5b22d1c2`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `64002143e5eb7fe7ad5c952b3c3ff2970cba7c89` |
| `daemonsContext.gba` | CONTEXT | `490f0cfb6daa202fc136003f76ddd06b55f0d965` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `5613907f7cc38acecb45d42701c880fbd01ad4aa` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `886b75265a4812a8315ea4a3279f0583643e683d` |

## The engine since v11.314.1

- `b5f248bd9` T-452 batch 5: HEATSINK to COREFILE (86-105) and the PREMISE line (106, 107, 236, 237) in the new style; grounding rows, icon palettes, overworld art, follower palettes

## The design and tools since v11.314.1

- `5b22d1c2` T-452 batch 5 built (engine b5f248bd9): HEATSINK to COREFILE and the PREMISE line as gbasprite's sources; BOOTSTRAP's six eggs, ENSEMBLE's heads, ACQUIRE's claw, AXIOMKICK's kick by hand
- `e1976361` ROM release v11.314.1: T-460 the arc closes; the SOUNDINGS words approved and the desk props raised; T-452 batches 3-4 fix-ups; T-454 THE THREE (with THE SUBTLE LAYER); T-461 object sprites past 255; T-459 A the follower's purple notice; v11.313.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

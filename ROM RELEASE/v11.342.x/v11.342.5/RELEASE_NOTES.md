# DAEMONS v11.342.5 — release notes

*Released 2026-11-07 01:46 · built against the design bible v11.342*

- **Engine**: CodeMusic/pokefirered-daemons `4f50673c4` (context-content)
- **Design**: CodeMusic/DAEMONS `ac776880`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `64edb4adf817709420a6fd59a09f30a9ca4ce01d` |
| `daemonsContext.gba` | CONTEXT | `880303f0cbecb54567a9fbf13c4089e59c28ae8c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `dcb48d290c6d9c584de05536e444aadaa6510608` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8a99758dbd00c692673333efba22f20b44f2827d` |

## The engine since v11.342.4

- `4f50673c4` T-525: batch 1 of the item icons built -- 41 drawn by hand in code (the user, 2026-11-07: "Build all 41")

## The design and tools since v11.342.4

- `ac776880` T-525: batch 2 of the item icons drafted -- 47 drawn by hand in code, nothing in the engine (DRAFT, the user away)
- `e779025d` T-525: batch 1 of the item icons built (engine 4f50673c4) -- the user, 2026-11-07: "Build all 41"
- `377beb70` T-525: batch 1 of the item icons drafted -- 41 drawn by hand in code, nothing in the engine (DRAFT, the user away)
- `7f5db205` ROM release v11.342.4: T-524 the battle UI in the TERMINAL family (2 Readout; the CAUGHT marker a USERBOX; the bracket out of the lean's slot)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

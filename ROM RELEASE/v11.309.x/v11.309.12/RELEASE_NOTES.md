# DAEMONS v11.309.12 — release notes

*Released 2026-10-23 20:02 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `d13cda5e9` (context-content)
- **Design**: CodeMusic/DAEMONS `4af92f28`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f08f3496d9ccb12a61f50f90c843aa4db74a4f50` |
| `daemonsContext.gba` | CONTEXT | `47f41f53041412fbc5de773adc00bf1398f874dc` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `82a64ab008d952383a9645eff254c624d991336c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `1ee8a944fcbe0b3d54542d6f1bcfaddba51f78e7` |

## The engine since v11.309.11

- `d13cda5e9` T-445: the eleven batch E caves' previews painted, and OTHER CAVE's follows its light

## The design and tools since v11.309.11

- `4af92f28` engine.md: the budget re-measured after T-445 (the painted previews, +30 KB of ROM)
- `85e6dc6d` T-445 BUILT (engine d13cda5e9): the eleven painted cave previews, OTHER CAVE's following its light
- `07a19993` T-438 batch F, the next four revised for the user's answers: palette moves, HALFTONE's roofs dotted whole, ARDOR's pantiles calmed
- `442d790f` TODO: the user's answers on batch F's next four
- `9379c6d3` T-438 batch F, the next four drafted: ARDOR (pantiles), HALFTONE (dot screen), VERDIGRIS (bronze, bloom, THE STREAK), BRAZEN (brass sheet, corporate grid)
- `9f90fffa` TODO: T-445 painted entrances approved; qa sheets
- `3f4e7d0f` ROM release v11.309.11: CALLOW, SLATE, DOLDRUM and THE UNDERTONE in their own looks, the busy roofs calmed (T-438 batch F); PROTEUS's owned back rests on the ground (T-440)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

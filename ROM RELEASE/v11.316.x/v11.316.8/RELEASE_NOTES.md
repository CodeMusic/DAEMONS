# DAEMONS v11.316.8 — release notes

*Released 2026-10-28 18:16 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `6fd39fcf5` (context-content)
- **Design**: CodeMusic/DAEMONS `b08205d6`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7824c721b415820a45e97d00d4a79d0aedc3e540` |
| `daemonsContext.gba` | CONTEXT | `32dc93c9a5149ee795c7998a1ab4aa0dc1d138b5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e76a32896e03d486edcc5bbf0f127c8ca29ab738` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `19a38b6e25405d5f986bf00c8c85ff76eb850ba6` |

## The engine since v11.316.7

- `6fd39fcf5` T-452 SYMBOL: the 28 forms (A-Z, ! and ?) redrawn as charm-style glyph creatures, as drawn (the user, 2026-10-28)

## The design and tools since v11.316.7

- `b08205d6` companion_export: SYMBOL's art from its A form (gfx/daemons/symbol/a_*.png, unown/a/front.4bpp) -- T-452's question 8
- `9408f53e` T-452 SYMBOL: the 28 forms installed (engine 6fd39fcf5) -- art, drafts, build_sym.py, gbafollower for the letters
- `a1f6c7ad` qa: T-452 batch 19 sheets (v11.316.7)
- `e35820e1` manual: rebuilt for v11.316.7
- `6cd8af92` ROM release v11.316.7: T-452 batch 19 (SINGLETON to OVERTONE) -- every regular daemon now in the new style

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

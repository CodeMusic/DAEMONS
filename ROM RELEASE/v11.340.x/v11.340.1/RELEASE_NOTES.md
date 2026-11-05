# DAEMONS v11.340.1 — release notes

*Released 2026-11-05 09:18 · built against the design bible v11.340*

- **Engine**: CodeMusic/pokefirered-daemons `d4a691fd9` (context-content)
- **Design**: CodeMusic/DAEMONS `7dac0893`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `44b9b2e285706515ed92e9e13cdd04662cfcdc66` |
| `daemonsContext.gba` | CONTEXT | `170f78a592907e1545255fe4e6a105dfb58e07a0` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8cca768ec9d4d3659d5ca81015b0e78c48154193` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2e00ee8ce02bd5bffdf2cebcaa5e10dc54bb30c7` |

## The engine since v11.338.4

- `d4a691fd9` T-445: the forests' and the SAFARI's name cards -- THE UNDERTONE (reseeded, 4493), THE SAME BUSH's own, DENSE WOOD, SAFARI ZONE

## The design and tools since v11.338.4

- `7dac0893` bookpdf: --review prints the torn book's three readings and all three side by side (T-519); the vault's key follows 'read it'
- `2da01983` TODO: T-445 the four place previews built (engine d4a691fd9)
- `7a433e0b` T-445: the place cards approved and built (engine d4a691fd9) -- THE UNDERTONE reseeded (4493), THE SAME BUSH's own card
- `e085239c` v11.340: 4.40, HALFTONE's tone follows the halves you hold (T-519, the user)
- `764d9ea3` v11.339: 4.40, the user's two open choices for THE UNITY BOOK (T-519)
- `b554590e` TODO: T-445 the four place previews approved (the user: replace all Nintendo art)
- `d1551163` T-445: the forests' and the SAFARI's name cards drafted (gbapreviews.py --places)
- `a418cf66` ROM release v11.338.4: T-519 the dawn half, THE EUDAIMON LAYER (DRAFT)

## The design bible's own entry for v11.340

### v11.340 — 2026-11-05

- **4.40, HALFTONE's tone follows the halves you hold (T-519, the user).** Greyscale with neither; emerald sepia with the night half; sapphire sepia, like a cyanotype, with the dawn half; with both unmended it follows the hour (emerald at night, sapphire by day); mended, full colour flows back. Opening a half at DAEMON TOWER deepens its tint for a moment. The mended town's hours stay grey and vivid. This replaces v11.339's tower moment.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.309.9 — release notes

*Released 2026-10-23 14:25 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `e2f7eea4f` (context-content)
- **Design**: CodeMusic/DAEMONS `9fe72907`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `34b3e52ab17d058c1e893a772d2e8c7bd39f99ff` |
| `daemonsContext.gba` | CONTEXT | `860adb96bdec44cabf8d68e4ffb241064c705b0c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `00c49658a9d660705b2c04e3af8d911f99f15c84` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `488ae67cfeff74d9119fbed4bc1c211844776214` |

## The engine since v11.309.8

- `e2f7eea4f` T-438 batch E: OTHER CAVE's light changes each visit -- a cycle of four (teal, amber, chrysoprase, rose quartz), and its wild daemons follow it
- `2007d739f` T-438 batch E: every approved cave redrawn -- DEADSTACK, TAPPOINT'S CAVE, THE BLACKOUT, THE TUNNEL, the KEEPALIVE PLANT, GLAUCOUS ISLES, MT. SMOULDER, THE DOTS; UMBRAL ASCENT, STILLFALL and OTHER CAVE as palette splits

## The design and tools since v11.309.8

- `9fe72907` T-438 batch E BUILT (engine 2007d739f, e2f7eea4f): every approved cave, three palette splits, OTHER CAVE's four lights
- `2859c40b` qa: T-438 batch D and T-440 built
- `d7a4429a` TODO: PROTEUS's edged back to draw; the timber recolour fine for now (the user)
- `12c4dbec` ROM release v11.309.8: the interiors redrawn in timber -- floors, walls, rugs, the TV set, the kitchen, the bookshelves, every PC a PORT, the stairs (T-438 batch D); a wild PROTEUS battles in its edition's own shape (T-440)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

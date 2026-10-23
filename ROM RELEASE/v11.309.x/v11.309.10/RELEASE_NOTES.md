# DAEMONS v11.309.10 — release notes

*Released 2026-10-23 15:01 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `3ac665a52` (context-content)
- **Design**: CodeMusic/DAEMONS `f06a4f6a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `efc97dd22efff2d87c3b92686de41fdc8334c250` |
| `daemonsContext.gba` | CONTEXT | `860adb96bdec44cabf8d68e4ffb241064c705b0c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f665f2681da74635c0059646157cc8260740e72d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `488ae67cfeff74d9119fbed4bc1c211844776214` |

## The engine since v11.309.9

- `3ac665a52` T-440: an owned CONTENT PROTEUS shows ALL EDGES from behind

## The design and tools since v11.309.9

- `f06a4f6a` T-445 drafted: tools/gbapreviews.py, the eleven batch E caves' previews (gfx/drafts/t445); TODO: T-440 edged back BUILT (engine 3ac665a52), T-445 drafted
- `d0b6bb52` T-440: PROTEUS's edged back -- ALL EDGES from behind, drawn at 512 on the sprite server
- `dc673ea2` qa: T-438 batch F draft sheets
- `23e80ea3` T-438 batch F draft: the town leftovers (not in the engine)
- `40d904ae` qa: T-438 batch E built
- `dd416b1a` ROM release v11.309.9: every cave has a look of its own -- DEADSTACK the stack, TAPPOINT the line, THE BLACKOUT the outage, THE TUNNEL, KEEPALIVE PLANT, GLAUCOUS ISLES, MT. SMOULDER, THE DOTS; UMBRAL ASCENT and STILLFALL in their own light; OTHER CAVE never holds the same light twice in a row (T-438 batch E)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.305.2 — release notes

*Released 2026-10-18 19:28 · built against the design bible v11.305*

- **Engine**: CodeMusic/pokefirered-daemons `36d4a590d` (context-content)
- **Design**: CodeMusic/DAEMONS `6947082f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `8e5478e5a88d47642ddf4de873437a48b0e5d091` |
| `daemonsContext.gba` | CONTEXT | `68701f745367711f881b366a1da7a9201fe765b7` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9bdcf007e68b69a668e17fca26847c7159725d53` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `1bbdc7f200d3a05a1e9830d3c0aace93a19abf3a` |

## The engine since v11.305.1

- `36d4a590d` T-423 fix: THE SUBTLE LAYER's layout goes at the END of layouts.json -- in the middle it renumbered every layout after it, and an older save in THE NEXUS opened on the wrong tiles (seen by the user)
- `3382b61d4` Merge t423-subtle-layer: THE SUBTLE LAYER (T-423, the psychic-book session)
- `22c2ac28e` T-423: THE SUBTLE LAYER is found in an INTERPRETER's home in BRAZEN (DRAFT lines)
- `15ed83ccc` T-423: THE SUBTLE LAYER, an open book with pictures (DRAFT)

## The design and tools since v11.305.1

- `6947082f` check_lexicon: layouts and maps keep their numbers between releases (a save holds them by number); T-421 note
- `7f1d36a5` ROM release v11.305.1: T-392's signature, the pilot of 31 routines; CORPUS STAFF's trainers named (T-421); seals v11.304.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

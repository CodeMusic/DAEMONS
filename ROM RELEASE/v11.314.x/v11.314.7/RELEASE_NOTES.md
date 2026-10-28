# DAEMONS v11.314.7 — release notes

*Released 2026-10-28 01:09 · built against the design bible v11.314*

- **Engine**: CodeMusic/pokefirered-daemons `e8c4afe1b` (context-content)
- **Design**: CodeMusic/DAEMONS `3734439b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `34a3fa2107848af3d20461a748a53a5bda5c5fbc` |
| `daemonsContext.gba` | CONTEXT | `cc5b1df61377af3e7a8c6cb63e863bb6b9c69f23` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2e72665b04c930bd1cda521fd3e7fa8ffd4a31cc` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b59b0f98584aeba917144f1126a5f617b43aa631` |

## The engine since v11.314.6

- `e8c4afe1b` T-459 D: words under words -- once THE SUBTLE LAYER is held, a purple line after four people's lines, what is meant under what is said

## The design and tools since v11.314.6

- `3734439b` T-459 D built (engine e8c4afe1b): words under words, four lines the user chose; A-D all built, the bible line left
- `83f3c230` qa: T-452 batch 7 and 8 sheets (v11.314.5, v11.314.6)
- `1ce22464` ROM release v11.314.6: T-452 batch 8 (DRUM to STEEPEST) on the user's answers

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

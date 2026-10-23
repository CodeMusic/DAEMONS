# DAEMONS v11.309.11 — release notes

*Released 2026-10-23 16:01 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `4063f2d6b` (context-content)
- **Design**: CodeMusic/DAEMONS `d650adfd`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0400099a97f268024dc170aa6706f51c17445b71` |
| `daemonsContext.gba` | CONTEXT | `c7ccee349a61c84c934c4b75ef8a9f0b7ebf2db5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `246996c223c1a65b7ab8cc0cb41e22bb71eedc9c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `112733dd1021df54ed4a271a1a02bbffcaa76c61` |

## The engine since v11.309.10

- `4063f2d6b` T-440: PROTEUS's owned back sits lower in the battle frame
- `6a5d9328a` T-438 batch F: CALLOW, SLATE, DOLDRUM and THE UNDERTONE's leftovers redrawn

## The design and tools since v11.309.10

- `d650adfd` T-445 drafted again, painted: the eleven batch E caves' previews painted on the sprite server
- `9317a80e` T-440: PROTEUS's owned back lowered (engine 4063f2d6b)
- `2dd412da` T-438 batch F BUILT (engine 6a5d9328a): CALLOW, SLATE, DOLDRUM, THE UNDERTONE
- `638c0798` TODO: the user's answers on batch F, T-440 and T-445; qa sheets
- `4e0e6d6c` ROM release v11.309.10: an owned PROTEUS shows ALL EDGES from behind in CONTENT (T-440)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

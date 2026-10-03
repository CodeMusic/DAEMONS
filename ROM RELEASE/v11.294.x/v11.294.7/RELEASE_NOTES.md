# DAEMONS v11.294.7 — release notes

*Released 2026-10-03 19:24 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `5c86ca0bb` (context-content)
- **Design**: CodeMusic/DAEMONS `1cd8d2a3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `bc815f08c1183072f91e4c90c95f2f59149142ef` |
| `daemonsContext.gba` | CONTEXT | `48f748060351f44109b2b6f5a0ca3e6ab447ff87` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ae0afd94cac253e3bbdc780b0c72dbc736b67f38` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `da4c84f16cf823827276da07a254783da0762d2e` |

## The engine since v11.294.6

- `5c86ca0bb` The name screen in our own look: the terminal, going on from the title screen (T-363)

## The design and tools since v11.294.6

- `1cd8d2a3` T-363 closed: the name screen, built (tools/gbanaming.py)
- `d973853f` ROM release v11.294.6: the gate beside CALLOW SCHOOL (T-361), and CRYSTAL asks if you remember (T-362)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

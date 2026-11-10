# DAEMONS v11.345.7 — release notes

*Released 2026-11-09 22:17 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `b1280ca99` (context-content)
- **Design**: CodeMusic/DAEMONS `51b760e1`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f0164705ee624e6e090018a38afc250e8d02a805` |
| `daemonsContext.gba` | CONTEXT | `e363a37fc7c7828a80934ff9286505d9d1e3f344` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f385598406cb2e9b334a3fb4368b3b9b8e2c9c45` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `60a1e9facfcad73ee112418ea1f1703904abaa47` |

## The engine since v11.345.6

- `b1280ca99` T-537 A, FOUNDRY STOCK: primary/building's desks and machines redrawn in place (DRAFT)

## The design and tools since v11.345.6

- `51b760e1` T-537 built (engine b1280ca99): A FOUNDRY STOCK, no blink -- the user, 2026-11-09: "A Foundry stock"; gbamachines APPROVED {A}, its report checks the engine; gbabuilding's LATER leaves the 97 tiles to it; four ROMs exit 0, sheets qa 9Nov2026 T537 50-56, route t537_machines (not filmed); DRAFT
- `9d3699b5` T-537 drafted: the desks and machines -- primary/building's last vanilla furniture, three directions (A FOUNDRY STOCK, B THE PORT'S FAMILY, C THE WIRELESS)
- `caa7636b` qa C311 40: the MUSAI faces as the user picked them, on their new pictures
- `c497cd7d` ROM release v11.345.6: T-536 FOUNDRY CO. and the CORPUS rooms in C, THE FOUNDRY (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

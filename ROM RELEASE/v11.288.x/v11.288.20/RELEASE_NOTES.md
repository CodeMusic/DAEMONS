# DAEMONS v11.288.20 — release notes

*Released 2026-10-01 08:04 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `8b6ffbd1a` (context-content)
- **Design**: CodeMusic/DAEMONS `e2ff84ab`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `38b314a10891cd91d3cf477b6eeb433d19f29267` |
| `daemonsContext.gba` | CONTEXT | `79844b7e66150275df1849e3fc96af816e92fc58` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `af1db66cfd2eaa379304f63514696363da7f3962` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9abe3f8d6e855365028d6a5bbf01db476f44cccf` |

## The engine since v11.288.19

- `8b6ffbd1a` T-234: DOLPHIN, PENGUIN and PENPHIN, and RESONANCE

## The design and tools since v11.288.19

- `e2ff84ab` T-234 closed: DOLPHIN, PENGUIN and PENPHIN are in (engine 8b6ffbd1a)
- `89124957` ROM release v11.288.19: a thank-you to Satoshi Tajiri

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

# DAEMONS v11.288.12 — release notes

*Released 2026-09-26 18:04 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `33bde8793` (context-content)
- **Design**: CodeMusic/DAEMONS `ac60585a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `53d459ae408c55ddfedcca711e0e1e7d9c41fbf1` |
| `daemonsContext.gba` | CONTEXT | `23d89e4550e15094020766e91b4feb08b09deea1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b876037b568e8f4d2ff323f82038fb9a822cca81` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `0f7838067ed42c7178f5a275935ee742d7de7279` |

## The engine since v11.288.11

- `33bde8793` The credits' runners are the player and AL (T-290, DRAFT: their overworld frames doubled)

## The design and tools since v11.288.11

- `ac60585a` T-319 built (engineAi 46495f0); T-290's runners drafted; port_prompts fenced by driftguard, check_generators keeps excused tools' drift entries; the surf-sheet note corrected
- `a622e98e` ROM release v11.288.11: DAVID's ship, the shoes, the QR codes

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

# DAEMONS v11.310.4 — release notes

*Released 2026-10-26 11:46 · built against the design bible v11.310*

- **Engine**: CodeMusic/pokefirered-daemons `2332f9e44` (context-content)
- **Design**: CodeMusic/DAEMONS `42bfffba`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `dfdaaf69fcdbd1939c49b94370773c26ff89c4b4` |
| `daemonsContext.gba` | CONTEXT | `eb90ceed740b48dc5a623cd95c6e3b3e5859fcc8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `10e56173a39fd72a710f5670942c4a0c59478bb5` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8dd49efd421b364cc1ec311cd52047d934b6cd2c` |

## The engine since v11.310.3

- `2332f9e44` T-447 pair 3: the REVIEW BOARD (UMBRA) and ERRATA (SLATE)
- `c0eb28f32` T-452: twenty-five daemons in the new style -- the six pilots and batch 1's charm picks (MANIFOLD kept for another round); drawn icons, shiny palettes, grounding tables

## The design and tools since v11.310.3

- `42bfffba` T-447 pair 3 built (engine 2332f9e44): the REVIEW BOARD and ERRATA; ERRATA's chalk a scrawl, no word
- `14a9f056` T-452 built (engine c0eb28f32): 25 daemons' new art as gbasprite's sources, drawn icons kept index for index
- `786686a3` TODO: T-447 pair 3 approved; ERRATA's chalk made unreadable
- `9283f477` T-447 pair 3 tweaked (the user's answers): the REVIEW BOARD's porch in dark stone and four seat places on its slab; ERRATA's erratum moved onto the slate roof
- `99baa06f` TODO: T-452 build the pilots and batch 1 (the user's answer)
- `845893ff` TODO: T-447 pair 3's tweaks (the user's answers)
- `25cee422` T-452 batch 1 redone for charm: twenty daemons by the chibi recipe, one key prop each (gfx/drafts/t452/d)
- `64a0205c` T-447 pair 3 drafted: the REVIEW BOARD (four vessels I-IV, red/yellow/black/pale, in a near-black hall under a bench slab) and ERRATA (roof a ruled slate, the pediment's struck line and red caret, stacked dead hardware, the annex a pinned card)
- `097826bc` qa: v11.310.3; T-446; T-452 batch 1
- `5ec2267a` ROM release v11.310.3: CORPUS's tower in riveted brass, the plate seen through its glass door, and DAEMON TOWER in halftone dots under a dotted dome (T-447 pair 2); the door tool pins its rooms (T-446)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

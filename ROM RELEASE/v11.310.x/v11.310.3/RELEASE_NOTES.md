# DAEMONS v11.310.3 — release notes

*Released 2026-10-25 00:47 · built against the design bible v11.310*

- **Engine**: CodeMusic/pokefirered-daemons `27e785a73` (context-content)
- **Design**: CodeMusic/DAEMONS `27e4eaea`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `855496d5430d093fd6c82c5a8816148cbba0876e` |
| `daemonsContext.gba` | CONTEXT | `30f22cc4bf117f9dedffc319f7bbd59ae520ecd0` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8905885bd9bf6ddc6a7b431d0d5cea63733ef0c1` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f3abb9bb74509145843980f1eec1eb9e978846db` |

## The engine since v11.310.2

- `27e785a73` T-447 pair 2: CORPUS's tower (BRAZEN) and DAEMON TOWER (HALFTONE, its top on ROUTE 10)
- `4c307ea22` T-446: safari_zone.png's own palette brought to LURID's row 9 (pixels unchanged)

## The design and tools since v11.310.2

- `27e4eaea` T-452 batch 1 redo (WIP)
- `1b1df146` TODO: T-445 the landmarks' name-card pictures are still vanilla
- `dd48d1d6` T-447 pair 2 built (engine 27e785a73): CORPUS's tower and DAEMON TOWER approved in gbalandmarks; CORPUS's door redrawn in gbadoors; theatre route landmarks-2
- `1e6f313e` TODO: T-452 batch 1 to be redone with more charm
- `5f715f43` TODO: T-447 pair 2 to build; the REVIEW BOARD's colour decided
- `dad1ac3c` T-452 roll-out batch 1 drafted: twenty daemons (ROVERSEER..FLOOD) by round two's method, through a batch runner (gfx/drafts/t452/c)
- `33afb443` T-446 closed: gbadoors pins five doors' rooms by palette index; its report checks the approved write
- `a219855f` T-447 pair 2 redrawn with 3/4 depth: CORPUS's tower and DAEMON TOWER (draft, not written)
- `7f6958c0` qa: v11.310.2 region map; T-447 pair 2 first draft
- `271f7c59` ROM release v11.310.2: the region map as a SCORE -- staff-line terrain, beamed routes, notehead towns, a sea of bits and notes that moves, the frame a closed score that opens; the overworld water shuffles bits and notes (T-449)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

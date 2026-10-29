# DAEMONS v11.320.2 — release notes

*Released 2026-10-28 23:58 · built against the design bible v11.320*

- **Engine**: CodeMusic/pokefirered-daemons `d45f8c799` (context-content)
- **Design**: CodeMusic/DAEMONS `fe86f45f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ef9105718e3bd9a11ca62cf8a0acaf0955e215a5` |
| `daemonsContext.gba` | CONTEXT | `f8aff2b42c84155f2f974ae0bbaa9563d1550182` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9f0a7b4ef73223fa9b32a8a88fbe534897ef6b64` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `df93560fb330690174f1a4e6e8bee9a8c4c662ff` |

## The engine since v11.320.1

- `d45f8c799` T-438 batch G: the endgame and the ships, redrawn by role (a DRAFT built while the user is away)

## The design and tools since v11.320.1

- `fe86f45f` QA: v11.320.1 play-tested in the theatre -- T-474 pair trades, T-473 loan release refused, T-475 OVERLOADED's forms, T-452 PROTEUS on THE ANNEX (routes t474_*.json)
- `b2d91dc2` T-438 batch G built as a DRAFT (engine d45f8c799): the endgame and the ships; engine.md's budget numbers refreshed
- `5e5aa244` T-438 batch G: gbatowns draws the endgame and the ships (engine d45f8c799)
- `971fe6c5` qa: C-220 OUT TOGETHER meeting
- `d01d68ad` TODO: T-474 struck -- released v11.320.1
- `0e3a5390` manual: rebuilt for v11.320.1
- `fa6b89b6` ROM release v11.320.1: T-474 PENPHIN only by a pair trade; T-476 generator drift read both ways; T-477 A-Z by our names; T-478 the cut-off texts; v11.319.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

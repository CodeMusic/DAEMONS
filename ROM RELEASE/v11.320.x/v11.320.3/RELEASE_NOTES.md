# DAEMONS v11.320.3 — release notes

*Released 2026-10-29 00:38 · built against the design bible v11.320*

- **Engine**: CodeMusic/pokefirered-daemons `a91a59a8e` (context-content)
- **Design**: CodeMusic/DAEMONS `4dbbfe17`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9697df2a55656ad23d9e8732d61827ca6ac0c666` |
| `daemonsContext.gba` | CONTEXT | `5988c97ad745bec880084be275384886dc12bf25` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a4ac3abbdb097b7f2ce2a76e15296611bfbfd34c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f1a19610785610c5f19caf1396fb8ff85bf9ae2e` |

## The engine since v11.320.2

- `a91a59a8e` T-479: a pair trade's child shows both ways in; a trade never writes FIRST MET over a species already seen

## The design and tools since v11.320.2

- `4dbbfe17` T-479 played in the theatre: PENPHIN's workings show both ways in; FIRST MET kept (engine a91a59a8e)
- `35c204b1` TODO: T-479 filed -- PENPHIN's INDEX shows one of its two ways in
- `cb3e7e37` theatre_route: --check holds every step to the shape the run reads (a burst's unquoted label); t474_index plays PENPHIN's and PENGUIN's workings and FIRST MET through the family page
- `06041a38` T-474 played in the theatre; T-438 batch G sheets filed (v11.320.2)
- `d24d84e0` manual: rebuilt for v11.320.2
- `9ca28cda` TODO: T-473 -- the PC's refusal to release a loan played in the theatre (with T-474, v11.320.2)
- `bc40d3c4` ROM release v11.320.2: T-438 batch G, the endgame and the ships (a DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

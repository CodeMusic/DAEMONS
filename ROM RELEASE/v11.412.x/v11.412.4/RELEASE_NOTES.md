# DAEMONS v11.412.4 — release notes

*Released 2026-11-21 21:39 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `f88c3ffff` (context-content)
- **Design**: CodeMusic/DAEMONS `479b1d3b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a1d1b509baf9dc338fd914ec191c3d55f595adbd` |
| `daemonsContext.gba` | CONTEXT | `fff44ac4ec18e67b5711a1b631578603f83f0964` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `3d4daf6b9892353d5781aa23f01c06d73ae97496` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e1686cb8a503ed5a957fbcd0c4ea3838443edda7` |

## The engine since v11.412.3

- `f88c3ffff` T-608: DEBUG's USE THE ITEM ON SLOT 1 with an evolution item ends on the field
- `e53272260` README: latest is v11.412.3

## The design and tools since v11.412.3

- `479b1d3b` Tickets mirror: T-608 closed
- `aaa1ce52` T-608: route t608_evolve_paths -- an evolution item's two paths, bag and DEBUG row, played back to the field
- `cb643cbb` qa: C-444 CAPS on the Cardputer Zero, the CC1101 + NFC cap found and 433 heard
- `86a2ef13` T-605 play-test: the 4F shop, SONGMUSAI and LANGMUSAI evolve in the theatre; theatre_route useitem ITEM_X evolve leaves the DEBUG menu open so an evolution item's scene plays (B cancels it)
- `70a26a0f` qa: C-455 THE ENGINE ROOM's LATER on the hub, the cadence on every plan
- `a40374ab` qa: T-607 SONGMUSAI and LANGMUSAI through the seasons (v11.412.3)
- `8b00c6ba` README and wiki: latest is v11.412.3
- `a20c4b78` ROM release v11.412.3: T-607 SONGMUSAI and LANGMUSAI through the seasons, their spoken lines, MUSAI's winter keeps all seven of its futures (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

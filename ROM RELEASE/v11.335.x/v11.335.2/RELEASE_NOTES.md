# DAEMONS v11.335.2 — release notes

*Released 2026-10-31 18:41 · built against the design bible v11.335*

- **Engine**: CodeMusic/pokefirered-daemons `d0ada0f2c` (context-content)
- **Design**: CodeMusic/DAEMONS `4681f795`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9d6db74ea024ae7f00fd9fcdb40c42d6404e0b16` |
| `daemonsContext.gba` | CONTEXT | `94c4b2e316fab9d9c6bee22df056a740a43b79f8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `4210b9d788057d3103d45cc26a922b3c828aba08` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `41db68c23df3636bd8f8b783b897166c10aa5ce4` |

## The engine since v11.335.1

- `d0ada0f2c` T-483 (5): THE PULL and THE GREAT HAND in the SPELLBOOK

## The design and tools since v11.335.1

- `4681f795` TODO: T-483 (5) THE PULL and THE GREAT HAND (engine d0ada0f2c)
- `26aa23d2` T-483 (5): theatre route t483_pull (3/3) and qa 31Oct2026 T483 59-61 -- THE PULL and THE GREAT HAND; t483_spellbook's cursor counts for the two new rows (6/6)
- `755eb939` theatre_route.py: choose reads a list row with no label (NULL) as empty instead of peeking address 0
- `3b1ce571` qa: T-496, her line passed on and her ball (v11.335.1)
- `e3b519c8` manual: rebuilt for v11.335.1
- `94fdae4f` README, wiki and TODO: v11.335.1 -- the lioness's ball and her passed-on line
- `3679666a` ROM release v11.335.1: T-494..T-496 the user's choices -- on the deck the lioness holds an orange ball, at the gangway she passes on the teacher's line; v11.334.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.333.2 — release notes

*Released 2026-10-31 14:32 · built against the design bible v11.333*

- **Engine**: CodeMusic/pokefirered-daemons `08789b380` (context-content)
- **Design**: CodeMusic/DAEMONS `bf777f8d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a75437164052026f2660c2cd699f9fe473027c61` |
| `daemonsContext.gba` | CONTEXT | `0a7a434f19115a18d4c0fd78a847ddbd6ad70cd9` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `907188fe1efc21099573fbbed64a1be6c3919b55` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `5f9c475c04f2f8374ce30c6f611169f5b759eb65` |

## The engine since v11.333.1

- `08789b380` T-493: the painting's words are the user's -- IT'S REAL. IT'S YOURS. (scrambled RG'H IVZO. RG'H BLFIH.), the user's choice 2026-10-31
- `d1aec064a` README: v11.333.1 is from 2026-10-31
- `513db8a6f` README: latest release v11.333.1

## The design and tools since v11.333.1

- `bf777f8d` T-499: reviewsheet's species_table keeps a C-nickname define on its slot's INDEX row (DOLPHIN, PENGUIN, PENPHIN); TODO struck
- `f9c99520` manual: T-499, the daemon cards find batch 15's numbers and INDEX entries
- `32d0351e` theatre_route: win stops at the battle's end, with no A after it
- `1a27cac6` TODO: T-493's words are the user's choice -- IT'S REAL. IT'S YOURS. (engine 08789b380)
- `c8e25e5d` T-493: the painting's words, the user's choice -- IT'S REAL. IT'S YOURS. (engine 08789b380); the route checks them
- `2d986323` TODO: T-483's Halloween released in v11.333.1; T-499 filed -- the manual's cards miss batch 15
- `c1a9af34` manual: rebuilt for v11.333.1
- `87befeda` qa: T-498, MATTE says forgiveness, in the ROM (played in the theatre; DRAFT)
- `27492c32` README, wiki and TODO: v11.333.1 -- T-493..T-496 released; a world page line on what waits (spoiler-light)
- `396d3afe` ROM release v11.333.1: T-493..T-496 the lioness met four times before the ship, the letter answered at home, a pair of paintings read in a mirror, not hard but unfamiliar; T-498 the sixth MARK brings FORGIVENESS over WRATH (all DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

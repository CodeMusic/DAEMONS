# DAEMONS v11.333.3 — release notes

*Released 2026-10-31 15:19 · built against the design bible v11.333*

- **Engine**: CodeMusic/pokefirered-daemons `2ff76a681` (context-content)
- **Design**: CodeMusic/DAEMONS `f39543c2`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `dabb81c0590f3c8e98c97b1a591c949c00616c61` |
| `daemonsContext.gba` | CONTEXT | `5f47a978d5092362a8532c3b8bc8a23b4c287ff6` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d366ef61801a5a813ffb3c27df5a31f8cd2e4ec6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `33dfdaf6e4c43c7596a4daca3ffabac8a732a498` |

## The engine since v11.333.2

- `2ff76a681` T-494: the card's line is the user's -- IT GOT THERE., her own words on the deck handed back (the user's choice, 2026-10-31)
- `2a291b5f3` T-483 (5): SPELLBOOK stays in the field (no leaving fade); CONTRAST turns DEBUG's forced night too; PATTERN's line reworded (DRAFT)
- `c8227b958` T-483 (5): the SPELLBOOK and the gentle spells -- AWAKENING, CONTRAST, PATTERN, LENS, FIELD (DRAFT)

## The design and tools since v11.333.2

- `f39543c2` engine.md: the numbers after the SPELLBOOK
- `9978df44` T-494: the card says IT GOT THERE. (the user's choice); the route checks it
- `e8794222` qa and route: T-483 (5), the SPELLBOOK and the gentle spells filmed in the theatre (6/6; DRAFT)
- `36c531b9` TODO: T-500..T-505 from the review of the three books and the story threads (the user, by multiple choice)
- `13d454f2` qa: T-493, the twin reads the user's words (v11.333.2)
- `f3988996` manual: rebuilt for v11.333.2
- `5de81d3b` README and wiki: v11.333.2
- `eb5e0563` ROM release v11.333.2: T-493 the painting's words are the user's -- IT'S REAL. IT'S YOURS.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

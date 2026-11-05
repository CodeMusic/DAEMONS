# DAEMONS v11.340.3 — release notes

*Released 2026-11-05 11:41 · built against the design bible v11.340*

- **Engine**: CodeMusic/pokefirered-daemons `2d0dcfbf7` (context-content)
- **Design**: CodeMusic/DAEMONS `f072fe01`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c3505ca2d59f4d1f1b1b4e57247330cf6238c617` |
| `daemonsContext.gba` | CONTEXT | `4e39435de8f046b4e47ae7fa09cad66e6f0ad40a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `57d112e93728eb2ad05c6c77986bb9bac3d5f110` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f6020ab159cebead239730fea14a4556f136b90a` |

## The engine since v11.340.2

- `2d0dcfbf7` T-519 item 3: THE UNITY BOOK's CARDS -- the night half's deck, which leaves the bag at the mending, dealt Both as One only (vision 4.40): the cover's tile, the hermetic day's card (its spellcraft hash and side bit, as the companion deals it), and a selector of that one entry; all four draws checked. DRAFT
- `b3ff94352` T-519: HALFTONE mended reads vivid in THE CREATOR'S HOUR (the user) -- the boost raised to 192 of 256 (four steps of 48), and inside the mended town the hour's gold eased to two-fifths, its dawn easing to six-eighths and its brighten halved, so the town's own colours show through the light

## The design and tools since v11.340.2

- `f072fe01` TODO: T-519 the mended town's vividness and THE UNITY BOOK's cards (engine b3ff94352, 2d0dcfbf7)
- `ec66d83f` qa: T-519 THE UNITY BOOK's cards (the book's own pages)
- `54d66060` qa: C-302's caption
- `3fd3893f` qa: C-302 the glass and the fruit, four stages each (DRAFT)
- `4756e1a8` qa: C-299 THE UNITY BOOK in the companion, the sheet sent (companion 77a2b8d)
- `1a9b3c40` ROM release v11.340.2: T-519 the mending -- HALFTONE's tints, THE UNITY BOOK, THE HORIZON (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

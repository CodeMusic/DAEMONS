# DAEMONS v11.304.5 — release notes

*Released 2026-10-18 13:58 · built against the design bible v11.304*

- **Engine**: CodeMusic/pokefirered-daemons `4182cdae4` (context-content)
- **Design**: CodeMusic/DAEMONS `e5d13a2e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `d3f9e13a76800e52e11916e371633c661c32d0e6` |
| `daemonsContext.gba` | CONTEXT | `d5b697ca039e81cd8be604a745530a90fc8f2f33` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `716f649bebfda9f4a7299b4722ed451d80cba729` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6206d2354d94d4e1b86aee00f62f656752d71f96` |

## The engine since v11.304.4

- `4182cdae4` T-422 (the user, 2026-10-18, confirmed by phone): the GAME CORNER plays as the companion's CASINO (DRAFT)

## The design and tools since v11.304.4

- `e5d13a2e` T-422: tools/gencasino.py -- the GAME CORNER's table, luck, art and tunes, carried in from the companion and held to it (engine 4182cdae4, DRAFT)
- `9f317253` qa: C-163 -- the watch's faces and its CARE grid, read off the watch
- `a74f2186` qa: C-158 the phone's casino, dressed
- `5264bb92` T-423: THE SUBTLE LAYER drafted -- 38 entries, 75 pages, measured and rule-checked; private until the user has read it
- `05fc2522` TODO: T-412 released; T-421 gains the NOTEBOOK's scroll arrows
- `e69a09fa` ROM release v11.304.4: the DREAM LOG -- "I had a dream.", a title for every dream, HER DREAMS with where each led (T-412)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

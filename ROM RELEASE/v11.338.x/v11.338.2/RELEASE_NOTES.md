# DAEMONS v11.338.2 — release notes

*Released 2026-11-04 23:18 · built against the design bible v11.338*

- **Engine**: CodeMusic/pokefirered-daemons `5a7fdc43d` (context-content)
- **Design**: CodeMusic/DAEMONS `77f25a33`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `703313649c8e7211224e7671c17b3b5497fe81bd` |
| `daemonsContext.gba` | CONTEXT | `061251ad0fd0452d918788146423d2f665dbc7ff` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2353725fb2fc305eb144ee4011f7e326a7f7315d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `846c85266df6c9f4b0105aa1c881fa0f3419f975` |

## The engine since v11.338.1

- `5a7fdc43d` THE HERMETIC LAYER's warning revised (T-519, the user's first line; OSRIC HATTER its reader; a hint of the other half) -- DAEMONS 715dbc00, gensubtle --write
- `fa8571314` T-519 item 1: SPIRITS' tone plainer, 10/32 of the way to white or black (the user, 2026-11-04; was 6)

## The design and tools since v11.338.1

- `77f25a33` T-519: THE UNITY BOOK, the third book mended, DRAFT for the user's read
- `96ffd2f5` T-519 item 1: SPIRITS' plainer tone (10/32) on the summary, filmed and filed
- `5839ea1b` TODO: T-519 the night half's warning revised
- `715dbc00` T-519: the night half's warning revised for THE UNITY BOOK (DRAFT)
- `c4be08fe` ROM release v11.338.1: T-519 the two hours (the catch-up, THE CREATOR'S HOUR, the LARK) and SPIRITS; v11.337.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

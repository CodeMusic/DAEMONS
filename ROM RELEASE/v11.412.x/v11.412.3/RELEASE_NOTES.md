# DAEMONS v11.412.3 — release notes

*Released 2026-11-21 15:50 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `28e9d5813` (context-content)
- **Design**: CodeMusic/DAEMONS `0e125d9e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a1d1b509baf9dc338fd914ec191c3d55f595adbd` |
| `daemonsContext.gba` | CONTEXT | `fff44ac4ec18e67b5711a1b631578603f83f0964` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b008087e2be99aa09852c6fafdfb7304901abe5b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `0b48bdf973b5c9b1003008daab9dc9e9a3e7aa6f` |

## The engine since v11.412.2

- `28e9d5813` T-607 (draft): MUSAI's winter INDEX entry keeps all seven of its futures (the user, 2026-11-21: one word, five -> seven)
- `fedec7def` T-607 (draft): SONGMUSAI and LANGMUSAI join the MUSAI branch's seasons -- six new seasonal forms, eight INDEX entries, every word DRAFT
- `df0204f37` README: latest is v11.412.2

## The design and tools since v11.412.2

- `0e125d9e` Tickets mirror: T-607 closed
- `1842a813` qa: C-455 MENTIONS on TODAY, the shelf and the book, on a scratch companion
- `8d9c21f1` T-607 (draft): MUSAI's winter INDEX entry keeps all seven of its futures (the user, 2026-11-21: one word, five -> seven)
- `27b3913b` T-607 (draft): SONGMUSAI and LANGMUSAI in the seasonal branch, their seasonal INDEX entries and spoken lines (engine fedec7def)
- `21ce068e` qa: T-605 the MUSAI branch and its new words (v11.412.2)
- `09be4839` README and wiki: latest is v11.412.2
- `bcd471c4` ROM release v11.412.2: T-605 MUSAI grows into seven forms -- SONGMUSAI (SIGNAL) and LANGMUSAI (EMERGENT), from WAVEFORM and UTTERANCE (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

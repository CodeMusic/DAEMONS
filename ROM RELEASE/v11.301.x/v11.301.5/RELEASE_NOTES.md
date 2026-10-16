# DAEMONS v11.301.5 — release notes

*Released 2026-10-15 22:39 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `0e07392a1` (context-content)
- **Design**: CodeMusic/DAEMONS `acaf9eac`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e3a045ba217939890ce5a91b8e68af44ec4c13ad` |
| `daemonsContext.gba` | CONTEXT | `b8fbc5c066b077d421a97254267bd2a79252c9a0` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `660a15d7579768f584c873d2dfbe4e3a6a198ac4` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e06309e2512e602d87c5b75e44fbc04ed9e2dbc6` |

## The engine since v11.301.4

- `0e07392a1` T-402 (the user's links, 2026-10-15): nine more songs -- Poly and Fields, Love Persists, Quantum Translations, Ty's Redemption (Part 1), S.T.A.R.R.'s Revelation, Desperate Shadows, Betrayal's Sting, Empire of Scorn, The Owl and the Code -- and fifteen more pages end on their track. Every page from a public song now carries its code.

## The design and tools since v11.301.4

- `acaf9eac` T-402 (engine 0e07392a1): the user's nine song links in tools/gbaqr.py; Crystal's Reply kept for LOOSE PAGES 6
- `4e48fb07` companion_export.py, C-125 (companion f5001c8; the user, 2026-10-15): the NOTEBOOK for the phone's PROFILE -- notebook.json, every page in notebook.c's order with the flags that file it, its one line and its words (notebook.c, notebook_documents.h, wisdom.h, the maps' text.inc); the player's pictures (the trainer card's and the first walking frame, REASON and INSTINCT); profile_layout gains the rival's name, the shoes, the NOTEBOOK and the understandings. check_generators: 131 clean.
- `b631aa00` qa: C-123 and C-121 -- the T-Deck: a message to everyone nearby, and on the bench
- `69e6f659` ROM release v11.301.4: the generators level -- 20 portraits outlined, 110 daemons' streaks on, the TOOLKIT in T-391's words, the four legendaries' overworld objects in their type palettes (T-404)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

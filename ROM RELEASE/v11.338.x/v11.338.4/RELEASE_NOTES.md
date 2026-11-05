# DAEMONS v11.338.4 — release notes

*Released 2026-11-05 00:27 · built against the design bible v11.338*

- **Engine**: CodeMusic/pokefirered-daemons `628294977` (context-content)
- **Design**: CodeMusic/DAEMONS `c94c64fc`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2b6800432607fa0d479cb55c64363e92cbabe085` |
| `daemonsContext.gba` | CONTEXT | `567fc38575f4c7a95ef57291b71b2321da004405` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d55ecea3dbc2c7d4852515f0b6be8e2427a17fd3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3692f1e5bf77e6a813391d757aa034521f1f0bb4` |

## The engine since v11.338.3

- `628294977` T-519 item 2 (6/6): DEBUG -> GAME EVENTS -> THE EUDAIMON LAYER gives or takes the dawn half (its flag and the book)
- `dfe8c3f22` T-519 item 2 (5/6): the nudge -- with the dawn half held and not the night half, in the witching hour, the first step outdoors says one purple line, once in the hour (one IWRAM byte), not in play's first minute. DRAFT
- `f57b761fa` T-519 item 2 (4/6): the gate removed -- THE HERMETIC LAYER is found at OSRIC HATTER's house at any hour, needing no other book (he hands it over at the end of a talk); the witching-routine unlock with the GUIDE and THE SUBTLE LAYER held is gone. DRAFT
- `545de140f` T-519 item 2 (3/6): the LARK under the singing FIR in the creator's hour -- beside the fir in all fourteen groves (FLAG_TEMP_1 hides her outside 4:24-5:12 or once given); sit with her and wait ten seconds, no button pressed, and she gives the dawn half. DRAFT
- `04387ca68` T-519 item 2 (2/6): THE EUDAIMON LAYER, the book -- ITEM_EUDAIMON_LAYER (was ITEM_0F9) and FLAG_GOT_EUDAIMON_LAYER (0x900 + 0x3FF), a third layer book in book_reader.c, opened from the bag at any hour, read only; BLESSING's observer line printed by the lead daemon's SPIRITS; no CARDS tile yet. DRAFT
- `059cc0e69` T-519 item 2 (1/6): THE EUDAIMON LAYER generated -- DAEMONS tools/gensubtle.py --book eudaimon writes src/data/eudaimon_layer.h (10 sections, 52 entries; the observer line's three readings, by SPIRITS class), a placeholder cover, picture and bag icon in the night half's style, recoloured for dawn. DRAFT

## The design and tools since v11.338.3

- `c94c64fc` TODO: T-519 the dawn half (engine 059cc0e69..628294977)
- `930501b4` T-519 item 2: THE EUDAIMON LAYER, the dawn half -- gensubtle makes src/data/eudaimon_layer.h in the night half's format (the observer line '% good | as is | low' as three readings by the lead's SPIRITS, each measured; placeholder dawn cover, picture and icon); companion_export gives eudaimon.json its flag; check_lexicon reads 'a EUDAIMON' as said 'you'; the book's pages filed (qa 5Nov2026 T519 1-2)
- `5563253b` docs: the manual reprinted for v11.338.3
- `4d39cac1` ROM release v11.338.3: PLAY made playable -- the button strip, and the seven songs re-taken from the user's recordings (T-521)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.302.2 — release notes

*Released 2026-10-17 21:13 · built against the design bible v11.302*

- **Engine**: CodeMusic/pokefirered-daemons `ec429e49a` (context-content)
- **Design**: CodeMusic/DAEMONS `7d777479`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `eb7572f5d38876831e6a50d6cc45147a6511f1da` |
| `daemonsContext.gba` | CONTEXT | `4410b37bb296e945ca3d2d1c0c24b41a40f8e7a7` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c1ea076fac02d3a80eb46b1af512684f6165081d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b9f1170ebaaf987a22021aadf67da5ffac1aa93b` |

## The engine since v11.302.1

- `ec429e49a` T-417 P2 (the user, 2026-10-17): O CHRISTMAS TREE -- PLAY listens, echoes, opens the fir, lights THE NEXUS; the SONGBOOK (DRAFT)
- `375c38aea` T-417 P0/P1 (the user, 2026-10-17): PLAY -- the HARP (CONTENT) and the FLUTE (CONTEXT), the KEY WHEEL, the STAFF and the notes in colour (DRAFT)

## The design and tools since v11.302.1

- `7d777479` companion_export: the SONGBOOK debug page's rows (T-417 P2)
- `ea3d2e15` TODO: T-417 P2 BUILT (engine ec429e49a)
- `6642cb97` T-417 P2 built (engine ec429e49a): O CHRISTMAS TREE played opens the fir and lights THE NEXUS; the SONGBOOK; gbanotebook spills into the second SEEN block
- `855de814` TODO: T-417's seven motifs chosen by ear (SLATE-3, the rest candidate 1)
- `401a66f0` qa: the pixel art crisp on the phone (companion C-147)
- `5ebf5ddd` TODO: T-417's three octaves approved by ear
- `c2a2e5f7` T-417 P0/P1 built (engine 375c38aea): tools/genplaysounds.py (the HARP's and FLUTE's note sounds) and tools/genplaynotes.py (the shared key-colour palette and note sheets); TODO notes what is left
- `ee836dd5` TODO: T-408's grove music sources are in (the user, 2026-10-17)
- `684330cc` ROM release v11.302.1: weather by season (T-415 phase 1 with the user's changes), the GUIDE's SECURITY page in shadows (T-418), STREAM's description; seals v11.301.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

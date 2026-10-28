# DAEMONS v11.316.3 — release notes

*Released 2026-10-28 13:22 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `d60c4d28f` (context-content)
- **Design**: CodeMusic/DAEMONS `8d20bd03`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `fee52666afdbd663ed43c40fdb7c18e231d13876` |
| `daemonsContext.gba` | CONTEXT | `e8cf8858d80e968ab5449ad083de40a20ffd9fe8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `7f9dab944b0823cf174cd85a8137e3e1a2ec7f35` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a5fca354ca5ff997e0f5c2f83dc114e8fb921e0f` |

## The engine since v11.316.2

- `d60c4d28f` T-452 batch 15: PARTICLE to RIPTIDE (311-331) and PENGUIN (341) in the new style, on the RECOMMENDED choices -- hand-drawn keys (PARTICLE's sparkle, FLOCKING's wing eye spots, PENPHIN's dolphin tail, QUINE's hand mirror, GRADIENT's needle nose, SLOWBURN's smoke, SEEPAGE's water drop, AQUIFER's shell pool, BACKFLOW's pincers; the water aqua, out of WATER's hue trap), RIPTIDE's streak marks moved onto its flank, the type-hue trap fixed (WATER blues greyed into the ramp), backs the front mirrored with the face out, grounds off; grounding rows, icon palettes, follower art and palettes

## The design and tools since v11.316.2

- `8d20bd03` TODO: T-469 -- the user: the cart alone earns the diploma
- `7ce74a8b` TODO: a row for T-468, the id skipped when two sessions filed at once (check_lexicon)
- `39fc0d5c` T-473: the game lane's calls -- TRADING beside AWAY in byte 0x13 (bit 3, its one spare), a LOAN bit the game can see (where: open, 0x1E's unused u16 the candidate), the finish's rule, companion_export's hunk, and the engine only on a hold and go
- `00782f19` TODO: T-452 batch 15 built (engine d60c4d28f): 311-331 + PENGUIN 341 on the RECOMMENDED choices; questions in gfx/drafts/t452/t/questions.md
- `af4bcf94` T-473, T-474 filed: trading between players, the game's half (the lock while offered, a received daemon finished on load, trade evolutions but none for a loan) and pair trade evolutions (design first); the companion's phase 1 is built (daemons-companion eb7369a, C-218 C-219); qa: C-219 sheets
- `e49f0c5e` T-452 batch 15 built (engine d60c4d28f): PARTICLE to RIPTIDE (311-331) with PENGUIN (341), on the RECOMMENDED choices (2026-10-28); drafts in gfx/drafts/t452/t, questions in t/questions.md (33 items) -- hand-drawn keys (PARTICLE's sparkle, FLOCKING's wing eye spots, PENPHIN's dolphin tail, QUINE's hand mirror, GRADIENT's needle nose, SLOWBURN's smoke, SEEPAGE's water drop, AQUIFER's shell pool, BACKFLOW's pincers), RIPTIDE's streak marks moved onto its flank, the type-hue trap fixed, backs the front mirrored with the face out; scripts batch15.py, chain15.sh, prep15.py, hand_b15.py, recolour15.py, icons15.py, ba15.py, ba15.sh, view15.py, grid15.py, grp15.py, build15.py and the batch 15 subjects
- `1252d6f9` TODO: T-467 the player's manual, done in 80f70cb1; qa: its sample sheets (v11.316.2)
- `80f70cb1` T-467 the player's manual: docs/DAEMONS-manual.pdf (47 pages, A5), made by tools/manual.py
- `0c6ef530` TODO: T-469..T-472 from the week's review (2026-10-28)
- `2cc757e5` companion_export: no place hints in the public companion -- events' debug labels lose their (PLACE), and no FLAG_UNDERSTANDING_<place> names in events, index_cards or marks (the review, 2026-10-28)
- `d53a60e7` T-319: kept current 2026-10-28 (engineAi 068c194, d066b8c); port_gamedata builds the object names from the engine
- `95331ef7` qa: T-452 batch 14 sheets (v11.316.2)
- `024533d4` ROM release v11.316.2: T-452 batch 14 (HASHSEED to JACOBIAN) on the recommended choices

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.315.3 — release notes

*Released 2026-10-28 05:50 · built against the design bible v11.315*

- **Engine**: CodeMusic/pokefirered-daemons `969b9630d` (context-content)
- **Design**: CodeMusic/DAEMONS `2420ff7e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `cb0a314dee8b7d1529885ebba91e20baf06281fa` |
| `daemonsContext.gba` | CONTEXT | `91106fc766665472afde4fa0cf85a19ab8bf875a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0b5db252f1c80591383abf492a4df83ca3f4d517` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `487e201b692c4807c0233bfc0da7d8e5ca385344` |

## The engine since v11.315.2

- `969b9630d` T-452 batch 10: GOLDSET to RESENTMENT (182-202) with VALENCE and RANKLE in the new style, on the RECOMMENDED choices while the user was away -- hand-drawn keys (VALENCE's tail ball, GRASP's tail hand, ABANDON's three cotton puffs, SEMAPHORE's flag), GOLDSET's and QUOTA's petals gold, the type-hue trap fixed (GRASS leaves into the ramp, STARVED's eyes blue, VALENCE's ears rose, TORPOR's eyes blank, RANKLE's blush red), every back the front mirrored with the face out; grounding rows, icon palettes, follower palettes

## The design and tools since v11.315.2

- `2420ff7e` T-452 batch 10 built (engine 969b9630d): GOLDSET to RESENTMENT (182-202) with VALENCE and RANKLE, on the RECOMMENDED choices while the user was away (2026-10-28); gfx/drafts/t452/n/questions.md queued for their review -- hand-drawn keys (VALENCE's tail ball, GRASP's tail hand, ABANDON's puffs, SEMAPHORE's flag), gold petals on GOLDSET and QUOTA, the type-hue trap fixed, backs the front mirrored with the face out; scripts batch10.py, chain10.sh, prep10.py, hand_b10.py, recolour10.py, icons10.py, ba10.py, view10.py, grid10.py, build10.py and the batch 10 subjects
- `e01bf7e8` ROM release v11.315.2: T-462 ITS DREAMS (DRAFT) -- the companion's dreams reach the game

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

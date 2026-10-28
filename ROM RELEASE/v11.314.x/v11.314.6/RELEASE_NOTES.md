# DAEMONS v11.314.6 — release notes

*Released 2026-10-28 00:22 · built against the design bible v11.314*

- **Engine**: CodeMusic/pokefirered-daemons `2b75b24ae` (context-content)
- **Design**: CodeMusic/DAEMONS `c4b5e8ab`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2820f05ec5c0dc4678f475f17b9453d58d44d082` |
| `daemonsContext.gba` | CONTEXT | `6cd868380927a3ca38bbe5d53bce968294c4a8a0` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9ae46ba6657dfe1918b56babe5ae65b72a8cccc7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ed1c021c498c30c370a43f4bb23d50ce4267a364` |

## The engine since v11.314.5

- `2b75b24ae` T-452 batch 8: DRUM to STEEPEST (140-160, less ARTSAI) in the new style, on the user's answers -- PROMETHEUS's crimson flame crest, DEADLOCK as two sitters, STARR's star, PUNCHCARD's holes; grounding rows, icon palettes, overworld art, follower palettes

## The design and tools since v11.314.5

- `c4b5e8ab` TODO: T-452 batch 8 built (engine 2b75b24ae) on the user's answers
- `7cf3ee8e` T-452 batch 8 built (engine 2b75b24ae): DRUM to STEEPEST as gbasprite's sources, on the user's answers -- PROMETHEUS's crimson flame crest, DEADLOCK as two sitters each with a lock, STARR's gold star, PUNCHCARD's rows of holes; mirrored backs for CANARY, SINGULAR, MOMENTUM, TEPID and the DEADLOCK pair; grounds off; DEADLOCK's and ASCLEPIUS's icons darker
- `d2b13144` ROM release v11.314.5: T-452 batch 7 (DYNAMO to MAINFRAME) on the user's answers; CRON's gem pale white-cyan

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

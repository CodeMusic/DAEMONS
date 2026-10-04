# DAEMONS v11.295.1 — release notes

*Released 2026-10-04 13:11 · built against the design bible v11.295*

- **Engine**: CodeMusic/pokefirered-daemons `8611a35b3` (context-content)
- **Design**: CodeMusic/DAEMONS `e64b39a5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2c99d1d22cb2892a915e0267c1108a8c57d0d469` |
| `daemonsContext.gba` | CONTEXT | `4838517568d094193ef4afedb76e6570e8d96db7` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c9c907fd147d09a9bbc6dab14e7ae2763f3f304a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d95d8545fa0eb59d36ef85db9f005e811a4189d4` |

## The engine since v11.294.10

- `8611a35b3` T-366: the OWL wears CALLOW SCHOOL's colours -- a green waistcoat with yellow buttons (tools/genowl.py)

## The design and tools since v11.294.10

- `e64b39a5` T-366 closed (engine 8611a35b3): the OWL in CALLOW SCHOOL's colours
- `633ecfae` companion_export: the PROFILE's offsets (global.h, flags.h through the preprocessor) and every map's place name, for companion C-23
- `84895d3f` qa C-20: the companion in each day's theme
- `6c41283e` v11.295: AWAY reshaped by the user (one at a time, SEND once the companion knows the save, an emergency way home) and the clock on the trainer card; T-370 to T-373; answers on T-349, T-350, T-356 (margins approved), T-359, T-265
- `1f726444` CLAUDE.md: the companion is public, and bindCompanion.sh starts it (C-12, C-19)
- `8bf0b2fd` T-366 decided (the OWL in CALLOW SCHOOL's colours, the user's choice C); T-367, T-368, T-369 for the morning run
- `f9b7cbb1` ROM release v11.294.10: the OWL's own colours (T-365); his note approved (T-364)

## The design bible's own entry for v11.295

### v11.295 — 2026-10-04

### AWAY reshaped, and the clock on the trainer card (2026-10-04)

- ***9.25, the user's answers (T-370)***: *one daemon at a time; SEND only once the companion's first SYNC has flagged the save, and the CHECKPOINT's second floor talks about the companion; an emergency way home in the game, with a warning, so a daemon is never stuck when the app cannot be reached; and the companion married to one save, so a daemon only goes home to the game it came from (the companion's PLAN 3). The menu's words stay OPEN.*
- ***9.25 (T-372)***: *the trainer card marks whether the real-time clock is on.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

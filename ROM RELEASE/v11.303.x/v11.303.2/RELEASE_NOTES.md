# DAEMONS v11.303.2 — release notes

*Released 2026-10-18 03:58 · built against the design bible v11.303*

- **Engine**: CodeMusic/pokefirered-daemons `aafcc8102` (context-content)
- **Design**: CodeMusic/DAEMONS `ade362f7`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7ecd9f0fa2f07b1dc8e1c96ab4611ac3fe52a1be` |
| `daemonsContext.gba` | CONTEXT | `3da2aa4aa8b4ec2ded03a3a09d4bab068fc1625b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d859539e74505f516a1a42cd850d15e9f02ac6b3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6233c6f6ae899d7704d3f58c19e1e524592b9231` |

## The engine since v11.303.1

- `aafcc8102` T-417 BREATHVERSE (the user, 2026-10-18): CONTEXT's FLUTE moves to an islet through a palm on ROUTE 2; THE NEXUS gets its own map section (DRAFT)

## The design and tools since v11.303.1

- `ade362f7` T-417 BREATHVERSE: tools/gbabreathverse.py and tools/genflute.py; gbagrove's REVEAL list knows its palms, gbanexusmap writes MAPSEC_NEXUS, skyodds follows the sky's bound (engine aafcc8102)
- `82941a07` qa: the companion's six tabs (C-156)
- `8332a038` TODO: the goal loop gains T-410/411/412 (place once approved) and T-392 (each routine's effect its own) (the user)
- `564c00b9` companion_export: SONGBOOK pages carry frames (C-156)
- `e4874186` qa: the companion rearranged, a mockup (companion C-156, to be decided)
- `c824385a` qa: C-154 -- notifications on the T-Watch S3: a jackpot and a wave from another board
- `b95d26c0` qa: T-417 P5, every song played
- `d8bc4db2` ROM release v11.303.1: PLAY finished -- ghost notes, the gold join, the echo during the event, THE NEXUS stays lit, every song played in both editions (T-417 P5); seals v11.302.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

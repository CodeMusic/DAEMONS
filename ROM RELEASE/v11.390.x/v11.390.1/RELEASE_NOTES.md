# DAEMONS v11.390.1 — release notes

*Released 2026-11-17 21:35 · built against the design bible v11.390*

- **Engine**: CodeMusic/pokefirered-daemons `7e6abcda8` (context-content)
- **Design**: CodeMusic/DAEMONS `72d9c527`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1226922848a071cad42561fe321fad0088dc65fb` |
| `daemonsContext.gba` | CONTEXT | `62b0d5dee4b70365ee2a1e18a56fc8ae8db06333` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b1bc0c2bcd0ce8f5ab00f9f6714d715bf8a3db08` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c0cb3b2be427732052792f24d86733508396b91b` |

## The engine since v11.389.1

- `7e6abcda8` T-565 batch 9: the islands, THE MARGINS, ours, in C -- in B-flat and B, the two keys with no colour: ONE to THREE ISLAND (one tune over major, then minor ground), FOUR and FIVE (phrases and white space, the harp writing in the margin), SIX and SEVEN (B-flat answered in B), the roads (the mainland road mirrored), the caves (sinking an octave), TANOBY (bars of seven), ONE ISLAND's CHECKPOINT (two halves meeting), over pret's in place (the user's pick, DRAFT; DAEMONS tools/genislandmusic.py)
- `e47f1463f` README: the release line names v11.389.1

## The design and tools since v11.389.1

- `72d9c527` T-565 batch 9: tools/genislandmusic.py, the islands in voice C (engine 7e6abcda8)
- `55ace913` Bible v11.390: the move sounds, a palette per type (T-565 batch 10, v11.389.1)
- `173e5fad` README and wiki Home name v11.389.1
- `4e8eede4` ROM release v11.389.1: T-565 batch 10, the 115 move sounds in C BOTH, a palette per type (DRAFT); seals v11.388.x

## The design bible's own entry for v11.390

### v11.390 — 2026-11-17

- Recorded from release v11.389.1 (4e8eede4, engine e97afa9cb), which sealed v11.388.x:
  - **The move sounds, a palette per type** (T-565 batch 10, the game lane): 115 in C BOTH. DRAFT. In 9.5, after the story and the field; three shared sounds left for T-583.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

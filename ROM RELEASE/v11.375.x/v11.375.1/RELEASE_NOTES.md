# DAEMONS v11.375.1 — release notes

*Released 2026-11-15 20:51 · built against the design bible v11.375*

- **Engine**: CodeMusic/pokefirered-daemons `45cae5c3d` (context-content)
- **Design**: CodeMusic/DAEMONS `26346254`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e3793be0ad25edbf9d596247098296b08d0c2216` |
| `daemonsContext.gba` | CONTEXT | `12272a8d787cb6f3b0528aa5a74b67fb3badf455` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `113dc00732c4fbbab472498f5e707a123cb91b03` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `32fe37004f3c7f0bd9f11b0bd110b5a1dbc9935d` |

## The engine since v11.374.1

- `45cae5c3d` T-571: the game's own words in newer writing -- trainer is USER in the four layer books, the spellbook and the debug kit (~74), bag is POOL, PC is PORT, flee is DETACH, a capture is a bind; the books' stage names, idioms (faint chalk, caught yourself, coals that catch) and hand-chosen breaks kept (the user's pick; port_vocab's drift read both ways)
- `d47e1aded` README: the release line names v11.374.1

## The design and tools since v11.374.1

- `26346254` T-571: port_vocab's guard acts only when it runs as its own command (companion_export and the font borrowers load it under their own --write)
- `9be95f12` T-571 DONE: the vocabulary misses applied by hand (engine), the guard kept
- `552c540b` T-571: port_vocab refuses a whole-tree write (driftguard; generator_drift.json lists its 22 files, read both ways)
- `1bdc2be3` Bible v11.375: a MOVE is a ROUTINE in the learning lines (T-567, v11.374.1)
- `5f4e7a6c` README and wiki Home name v11.374.1
- `4d16fc0b` ROM release v11.374.1: T-567 a MOVE is a ROUTINE in the learning lines -- the relearner, battle's four ROUTINES (reworded, DRAFT), none left, STRATUM routines, RECYCLE; seals v11.373.x; two recordings deferred

## The design bible's own entry for v11.375

### v11.375 — 2026-11-15

- Recorded from release v11.374.1 (4d16fc0b, engine 46045ed22), which sealed v11.373.x:
  - **A MOVE is a ROUTINE in the learning lines** (T-567): seven lines, two reworded to fit, DRAFT. Under "And moves become ROUTINES".
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

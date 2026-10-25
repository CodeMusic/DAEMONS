# DAEMONS v11.310.2 — release notes

*Released 2026-10-24 22:03 · built against the design bible v11.310*

- **Engine**: CodeMusic/pokefirered-daemons `fc361a133` (context-content)
- **Design**: CodeMusic/DAEMONS `6ca2d56b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c1b6151d1798df46f71194eab2a0cf8812c38aee` |
| `daemonsContext.gba` | CONTEXT | `212c50c6f53e8baac70bdd27fad7a887f6b1285e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8233d8490fac72a619cd35e38b19fbb8eef5724b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `194ecf37f918422a9a9c779e2f9af18aaaab5263` |

## The engine since v11.310.1

- `fc361a133` T-449: the TOWN MAP and GOTO map in SCORE; the sea a shuffle of bits and notes; the overworld water too

## The design and tools since v11.310.1

- `6ca2d56b` TODO: T-447 pair 2 to be redrawn with depth (the user's answers)
- `6a9d824c` docs: engine.md budgets and sprites.md census regenerated (gbabudget, gbaspritecensus --write) after T-449's build
- `e62437df` T-449 built: tools/gbaregionmap.py (SCORE, --write --approved) and gbawater's bits and notes (engine fc361a133)
- `84ae38f3` T-447 pair 2 draft: CORPUS's tower and DAEMON TOWER drawn into their footprints (not written)
- `a893bd2c` TODO: T-447 the user's answers on DAEMON TOWER, USER TOWER, THE ANNEX
- `301532f0` qa: v11.310.1 sheets; T-452 round two
- `fb169cf3` companion_export: a sealed release group keeps its patches.json rows (its notes are a PDF now)
- `5be3ccbe` TODO: T-446 the SAFARI door's frames after batch H
- `bc4c15bb` ROM release v11.310.1: SCORN SOLUTIONS and the burned MANSION drawn from the story (T-447); HANDSHAKE, TETHERING, COROUTINE (T-450); a daemon the companion grew or delivered finished on load, its new routines offered (T-448, T-455); THE SUBTLE LAYER's reviewed text. Seals v11.309.x.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

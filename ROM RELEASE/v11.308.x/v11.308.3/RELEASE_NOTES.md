# DAEMONS v11.308.3 — release notes

*Released 2026-10-21 16:40 · built against the design bible v11.308*

- **Engine**: CodeMusic/pokefirered-daemons `a5cd08bab` (context-content)
- **Design**: CodeMusic/DAEMONS `6521bcf3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `03f9493340f9d911770381bf5227e043a33f1b5b` |
| `daemonsContext.gba` | CONTEXT | `3494f8ca515344d9aff7e421df30474cda4c74d0` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `785d123abb14d31d90eee9749cbd300a4d8a45d2` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `df0588d9ef56028653d4ee5c7e7c03e121af7477` |

## The engine since v11.308.2

- `a5cd08bab` T-431 P1 (the user's answers): no calm push from the heal after a white-out -- Feelings_CheckpointHeal moves from TakeAndHealPkmn (which the white-out also calls) to the nurse's chosen heal; DEBUG FEELINGS gains +12 HOURS
- `78c0d4746` T-431 P1: feelings in the game -- GLAD, MAD, SAD and CALM in each daemon's unused contest-condition bytes (u16 stamp in tough+sheen, unusedRibbons bits 0-1), fading with a 3-hour half-life (145-byte table, nothing after a day) by the cart's clock or play time; pushed by battles won and lost, faints, poison, the CHECKPOINT's machine, walking with the follower, levels, vitamins, battle items, TMs, the massage, a held item, and coming back from a box (all DRAFT, include/daemons_feelings.h); eggs and AWAY skipped; DEBUG -> GAME EVENTS -> FEELINGS shows each party daemon's values and friendship, +3 HOURS, +1 DAY and PUSH rows. Save/EWRAM/IWRAM 0 (DEBUG 4 B EWRAM)

## The design and tools since v11.308.2

- `6521bcf3` T-431 P1: the user's answers -- the white-out's heal does not calm (engine a5cd08bab); feelings-p1 route gains the white-out check and twelve hours in a box (8 stops)
- `00df9053` T-431 P1 built (engine 78c0d4746): tools/routes/feelings-p1.json (7 stops, CONTENT; 1,2,4,5 in CONTEXT); theatre_route.py learns events, feelings, conditions and lose; companion_export leaves the FEELINGS debug page out; TODO notes P1
- `0b636824` qa: T-430 colour in Halftone, T-432 shiny colours, T-431 emoji draft
- `b7d7dd4d` ROM release v11.308.2: what you bring keeps its colour in HALFTONE (T-430); the tower's colour back floor by floor after INIT; shiny colours for every daemon (T-432); the follower goes into the healing machine (T-18 follow-up)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

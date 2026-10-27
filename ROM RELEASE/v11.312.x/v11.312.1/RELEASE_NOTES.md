# DAEMONS v11.312.1 — release notes

*Released 2026-10-27 04:44 · built against the design bible v11.312*

- **Engine**: CodeMusic/pokefirered-daemons `5465cf22d` (context-content)
- **Design**: CodeMusic/DAEMONS `b1699e0f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `cbcc009d11ae6be414e9cb430057cae62745ddf3` |
| `daemonsContext.gba` | CONTEXT | `f3d66ab64145b0eed6471cbd63df2b6e145fd1b1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `1e9d6175e19ae50f742ea400e2428a93d179470a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3581d0f214cf01f59b7b2248f524b9830917667d` |

## The engine since v11.311.1

- `5465cf22d` T-457: the user's words (DRAFT) and the receiver's sprite
- `64d79bbf4` T-456: UMBRA PLATEAU's name card -- the REVIEW BOARD (seed C, the hall neutral)
- `d656c4b36` T-457: CRYSTAL's one line moves to the receiver; both GLOBAL INDEX handovers say nothing from her

## The design and tools since v11.311.1

- `b1699e0f` T-457: the user's words in, DRAFT, and the receiver's sprite (engine 5465cf22d)
- `54c67a02` T-452 batch 3 WIP drafts (#44 SKEW to LOOP, 16 of 22; paused when the disk filled) -- not approved
- `ada7f06a` T-456: the REVIEW BOARD's name card BUILT (engine 64d79bbf4); seed C with the hall neutral
- `77785111` TODO: T-456 approved (the user's answers)
- `3ae57845` T-457: CRYSTAL's line at the receiver built (engine d656c4b36); the receiver's own sprite drafted (A indigo, B dark wood)
- `db9967e1` qa: T-456 REVIEW BOARD card draft
- `e8bccc6c` T-456: the REVIEW BOARD's name card drafted (gbapreviews --landmarks, a NEW card; not approved)
- `89599a0e` Bible v11.312: 4.37 as built (T-457)
- `102be180` TODO: T-457 point 2 corrected -- CRYSTAL's line at the receiver, not the handover (the user's answer)
- `94053f12` TODO: T-457 follow-ups (the user's answers)
- `6accac6e` qa: v11.311.1's sheets (T-452 round two, T-445 WAREHOUSE)
- `3c578a5c` ROM release v11.311.1: the landmarks' name cards (T-445), T-452 round two (46 daemons), the second joining (T-457, DRAFT placeholders); v11.310.x sealed

## The design bible's own entry for v11.312

### v11.312 — 2026-10-26

### The second joining, as built (T-457)

- ***4.37 (the user, after the build)***: **her aide hands over the GLOBAL INDEX with nothing from CRYSTAL** -- *in play it comes before THE ANNEX, so the record arrives while she is away* -- **and her one quiet line moves to the receiver, when the player finds her at it after THE ANNEX.** *The papers are PROSPECTUS 7 and 8 (school.md holds 4 to 6), on the lab shelf beside the INDEX unit. Built in v11.311.1, every word a DRAFT placeholder.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

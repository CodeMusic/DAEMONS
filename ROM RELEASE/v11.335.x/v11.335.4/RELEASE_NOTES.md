# DAEMONS v11.335.4 — release notes

*Released 2026-11-01 01:51 · built against the design bible v11.335*

- **Engine**: CodeMusic/pokefirered-daemons `fbb6616f1` (context-content)
- **Design**: CodeMusic/DAEMONS `184dffaf`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `758bfaeb435748adf64b007dfddf7377a1daacaf` |
| `daemonsContext.gba` | CONTEXT | `ba512766a57126b4e7e863b49b8746b3cb6e470b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `fc95254b1d16816dd4db495a4ebd22cb907cc6f7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f311ac8ba92abd1de227073baf43ebe71e9068e4` |

## The engine since v11.335.3

- `fbb6616f1` T-483 (5): THE RETURN and THE SMALL HAND in the SPELLBOOK, and both hands in one hour

## The design and tools since v11.335.3

- `184dffaf` TODO: T-483 (5) THE RETURN and THE SMALL HAND (engine fbb6616f1)
- `78be217e` T-483 (5): theatre route t483_return_hand (3/3) and qa 1Nov2026 T483 1-3 -- THE RETURN and THE SMALL HAND; t483_spellbook's and t483_pull's cursor counts for the two new rows (6/6, 3/3; t483_room_mirror 3/3 unchanged)
- `5501f8bd` Manuals: DAEMONS is said DAY-mons, not demons -- the micro start, the quick start and the player's manual
- `680e7fd7` ROM release v11.335.3: T-483 (5) THE ROOM and THE MIRROR in the SPELLBOOK

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

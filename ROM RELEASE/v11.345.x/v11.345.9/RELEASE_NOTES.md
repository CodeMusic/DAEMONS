# DAEMONS v11.345.9 — release notes

*Released 2026-11-10 13:33 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `56327cb07` (context-content)
- **Design**: CodeMusic/DAEMONS `f1a952d8`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1db646027e12f3bfb8cacc6fd96b389a15b14fc4` |
| `daemonsContext.gba` | CONTEXT | `82445992e3a4cb83d838242c074e17acaaeca89d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0ef6d824a171f29b80a048ca82fe4e87ca037a4a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ba2add1660e28b023d652cd7dd19d0dbf0a87a46` |

## The engine since v11.345.8

- `56327cb07` T-538 batch 3, A THE KEEPING: the fan club, the DAY-CAREs, INIT's house, DOLDRUM's burgled house and THE TUNNEL redrawn in place (the user, 2026-11-10: "A The keeping")
- `135347387` T-437: the book covers' titles re-lettered in SCREEN (genguide, gensubtle --write)
- `b5541a176` T-437 SCREEN, the DAEMONS typeface, in the four Latin font sheets (the user, 2026-11-10: "Ship it as is")

## The design and tools since v11.345.8

- `f1a952d8` T-538 batch 3 built (engine 56327cb07), A THE KEEPING: gbadwellings APPROVED {A}, in check_generators; qa 10Nov2026 T538 32-38; route t538_keeping (DRAFT)
- `1650bdda` T-538 batch 3 drafted: the fan club, the DAY-CAREs, INIT's house, DOLDRUM's burgled house and THE TUNNEL -- three directions (A THE KEEPING, B THE REGISTER, C MAKE DO), tools/gbadwellings.py; gbacaves keeps T538_TUNNEL; qa 10Nov2026 T538 22-27 (DRAFT)
- `3a2e528c` T-437: the sheets renumbered qa 10Nov2026 T437 28-31 (22-27 are T-538 batch 3's, filed in the main checkout)
- `31420225` T-437 shipped: SCREEN in the engine (b5541a176) and the book covers re-lettered (135347387)
- `95c01f93` T-437 shipped (engine b5541a176): tools/gbafont.py DRAFT = False -- the user, 2026-11-10, "Ship it as is"
- `52cdeb16` T-437: the user, 2026-11-10 -- "Ship it as is" (SCREEN approved from the rebuilt sheets)
- `002ae676` T-437 rebuilt for judging: SCREEN on today's engine (branch t437-screen-font-2 0e4ef2ddd, unmerged), filmed beside FireRed's face (qa 10Nov2026 T437 16-19)
- `97751cbe` ROM release v11.345.8: T-538 batch 1 A HEARTH and batch 2 A THE WORKBENCH, T-539 A PASSING (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

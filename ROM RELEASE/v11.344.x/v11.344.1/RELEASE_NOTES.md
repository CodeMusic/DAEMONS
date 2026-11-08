# DAEMONS v11.344.1 — release notes

*Released 2026-11-08 14:57 · built against the design bible v11.344*

- **Engine**: CodeMusic/pokefirered-daemons `c8985d8ce` (context-content)
- **Design**: CodeMusic/DAEMONS `9d472ba0`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `515261b6586d569ea49d981511ffac0d70c1faee` |
| `daemonsContext.gba` | CONTEXT | `ecf95109c427fbda1efad977174dc4012d8c7513` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0b4fed2e8770cac2f16bd2e6d9dfddfaba1206b8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `231c3744713a067666f673038a76af5d9bf3ca35` |

## The engine since v11.343.5

- `c8985d8ce` T-530 pass 2: the menus FireRed still drew, in A TERMINAL -- the TOOLKIT (its cards in their type's colours), the MART and the PLUGIN shop, the INDEX's category icons and its AREA map (B SCORE), the TRAP TABLE's pocket picture, the party's hold marks, the PC's box menu, scroll arrows, waveform and DATA panel

## The design and tools since v11.343.5

- `9d472ba0` engine.md regenerated (gbabudget): T-530 pass 2's figures
- `d61fa56d` vision v11.344: a day's symbol -- ring and horizon, the shadow reflected, the centre in ink (T-531)
- `183c1617` T-532 DRAFT: the MUSAI branch keeps the seasons -- design and concepts, nothing in the engine
- `6b674fe7` T-530 pass 2 built (engine c8985d8ce): the TOOLKIT, the MART, the INDEX's icons and area map (B SCORE), the TRAP TABLE's pocket, the hold marks, the PC's box menu/arrows/waveform/DATA panel; route t530_menus_pass2 8/8 (qa 8Nov2026 T530 8-15)
- `7bef9970` TODO: T-531 a day's symbol -- ring and horizon, petal count, the shadow reflected, the centre in ink (the user, 2026-11-08)
- `7c7be54f` T-530 pass 2 DRAFT: the TOOLKIT, the MART, the INDEX's icons and area map (A or B SCORE), the TRAP TABLE's pocket picture, the hold marks, the PC's box menu/arrows/waveform/DATA panel -- tools/gbamenus2.py, nothing in the engine (qa 8Nov2026 T530 1-7)
- `10de5b37` ROM release v11.343.5: T-530 the menus in A TERMINAL -- the party screen, the summary, ITEM STORAGE and the TRAP TABLE, the PC with the paw and 16 survey-plate wallpapers

## The design bible's own entry for v11.344

### v11.344 — 2026-11-08

- **9.21, a day's symbol (T-531, the user, by multiple choice; the seven marks approved as drawn).** Each weekday gets one wordless symbol: its centre as a ring of its traditional petal count, in ink; a level line through it, the word *over* made visible; the virtue's mark above in the day's colour, and its shadow below as the same mark reflected, faint and dashed. Chastity a closed dome, Temperance a level beam, Charity an open bowl, Diligence a climb, Forgiveness a knot opening, Kindness an arc sheltering a point, Humility a stem bowing. 4.38's "the seven centres never coloured" holds. First use: a daemon's dream, with a title of its own (still open).

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

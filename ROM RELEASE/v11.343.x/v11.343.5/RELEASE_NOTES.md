# DAEMONS v11.343.5 — release notes

*Released 2026-11-07 22:22 · built against the design bible v11.343*

- **Engine**: CodeMusic/pokefirered-daemons `33bc1e459` (context-content)
- **Design**: CodeMusic/DAEMONS `89f25184`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2ec870973e0c1730e270f5b3c284aef3e7e697f5` |
| `daemonsContext.gba` | CONTEXT | `39d656ebfa4e4b62778a54ff896a2cb76ac1a8d0` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `25d3f20b4cec31cec046a492617e7e5accd900f7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8e83218a0d08c3fa8398c27b590bfbe0bdda7ec3` |

## The engine since v11.343.4

- `33bc1e459` T-530 second pass: the party screen's boxes and ITEM STORAGE's badge belong to A TERMINAL
- `9f35e6950` T-530: the menus in A TERMINAL -- the party screen, the SUMMARY's bars, ITEM STORAGE and the TRAP TABLE, the PC (the PAW, all 16 wallpapers as survey plates, the backdrop lattice)

## The design and tools since v11.343.4

- `89f25184` gbanexusmap learns T-528's dawn chorus LARK scene; gbabattleui leaves a pixel-identical sheet alone (no more re-encode ping-pong with genthrashicon); engine.md and sprites.md regenerated
- `0716b649` T-530 second pass (engine 33bc1e459): the party's boxes in the TERMINAL palette, clear of CANCEL; ITEM STORAGE's badge clear of its title (qa 7Nov2026 T530 67-68)
- `596c1cc4` T-530 built in the game (engine 9f35e6950): the menus in A TERMINAL -- party screen, SUMMARY bars, ITEM STORAGE and the TRAP TABLE, the PC's paw and 16 survey-plate wallpapers; route tools/routes/t530_menus.json 8/8 (qa 7Nov2026 T530 56-66)
- `9460ad9b` T-530 DRAFT: the menus -- party screen, SUMMARY bars, item screens, PC -- in two directions, nothing in the engine
- `b6c1278c` ROM release v11.343.4: T-529 the mended book's lens -- L and R turn every page of THE UNITY BOOK between night, whole and dawn

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

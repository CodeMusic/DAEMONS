# DAEMONS v11.328.1 — release notes

*Released 2026-10-29 16:51 · built against the design bible v11.328*

- **Engine**: CodeMusic/pokefirered-daemons `2af4bd3a7` (context-content)
- **Design**: CodeMusic/DAEMONS `882693a2`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6f866ddf5e4852397107dc8c144dc3c39e9d1dc4` |
| `daemonsContext.gba` | CONTEXT | `3a904abcfe848573df00b1285eb54c8cce5dc795` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2927dbd3253cbe5819da763ebe2f1aed4d3b7135` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `86d46f93127e47d250737373d12814da3ec3f752` |

## The engine since v11.326.1

- `2af4bd3a7` T-487: AL's one crack -- once, the first time he speaks after the GLOBAL INDEX is held (FOUR ISLAND, SIX ISLAND's CHECKPOINT, or the champion's room after the first visit), behind FLAG_AL_CRACKED (DRAFT)
- `abc565f06` T-485: OSRIC HATTER's house on QUICKSILVER -- the leaning top hat at (9..11,11..13), door (10,13) (gbalandmarks, row 12, 28 tiles, 8 blocks); the room of stopped clocks on LAYOUT_HOUSE1's plan, a tileset of its own (gbainterior hatters_house); OSRIC a stoat in his own palette (genhatter, id 63, tag 0x112E); a riddle a visit, the book's after it, his 3:30 line, the glitch on every entry 3:00-3:59 (DRAFT)
- `78f03377d` T-486: the glitch's strength follows the clock -- 12 frames, +/-24px, palettes every other frame at 3:30; 4 frames, +/-10px, every 4th toward 3:00 and 3:59 (the weak end keeps its colour swap); the book's warning page at whatever night minute it is turned (the weakest outside 3-4); DEBUG WATCH gains 3:15 AM and 3:30 AM
- `f40235a86` README: latest release v11.326.1

## The design and tools since v11.326.1

- `882693a2` qa: C-242 watch BATTERY settings
- `a80b0d38` docs: engine.md, sprites.md, the type chart and retired names regenerated (the witching routines, OSRIC HATTER)
- `e5a83476` qa: C-247 GAME tab title
- `dc525413` companion_export: the GAME tab launcher's title art (title_files)
- `b3433ceb` TODO: T-488 -- the * SINK family, sold by type late (the user)
- `c0526f61` Bible v11.328: four mechanics decided -- resist items, ALIGN, the split in steps, CONSENSUS by overlap (T-488 to T-491)
- `c432aaaa` TODO: T-481 B and C drafted, the user's answers
- `5362e528` qa: T-485, T-486, T-487 in the theatre -- the hat, the room and its riddles, the entry glitch at 3:00/3:15/3:30, the glitch in the 3:30 line, AL's one crack
- `730007a7` T-485: OSRIC HATTER's house -- the hat in gbalandmarks (cinnabar_island, row 12, solid body, a doorway on top), the room in gbainterior (hatters_house), the stoat in genhatter.py; gbatowns' LANDMARKS keeps the hat's boxes (engine 2af4bd3a7)
- `25802345` tools: gbacalendar_ui.py, T-481 B and C drafted on sheets (menus, panes, the field); no write mode yet
- `3de20b96` Bible v11.327: the Open log audited -- thirteen answered questions struck
- `7adf7fde` wiki: the calendar's backgrounds after the roads' season slots, so 'with them' still means the seasons
- `3bb5a8f0` README and wiki: v11.326.1; the battle backgrounds keep the calendar (T-481 A)
- `b4ff0929` TODO: T-481 A released v11.326.1
- `48f1eb56` manual: rebuilt for v11.326.1
- `d2ea9d88` ROM release v11.326.1: T-481 A the battle backgrounds keep the calendar; v11.325.x sealed

## The design bible's own entry for v11.328

### v11.328 — 2026-10-29

### Four mechanics from 2.12, decided

- ***The user, by multiple choice***: **seventeen type-resist items** (T-488); **ALIGN, the reverse of the frame family** (T-489); **the physical / special split, in steps** (T-490); **CONSENSUS grows with overlap, a CONTEXT routine with divergence** (T-491). Every new name DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

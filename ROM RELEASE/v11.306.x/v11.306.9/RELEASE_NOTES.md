# DAEMONS v11.306.9 — release notes

*Released 2026-10-19 20:56 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `3187ca0fd` (context-content)
- **Design**: CodeMusic/DAEMONS `fba588fe`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1044d6cac4430b40097d037114a3776de6ba85c0` |
| `daemonsContext.gba` | CONTEXT | `2934dbb02fab29010949e03faca34ff92015f672` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e1368adb44327a648b2270ff83390c7b4f7a955b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a888b9d0ba5f48c555c6df9e316ad374e223b3da` |

## The engine since v11.306.8

- `3187ca0fd` T-422: FOOLS' DAY stands the reels' daemons and the dancing lead on their heads (casino.cpp's flip); vanilla's unused reel_icons removed
- `81f24effb` T-417: the BAND'S SHEET's glyph beside B FLAT on the KEY WHEEL once the sheet is held (DAEMONS tools/genplaynotes.py, DRAFT art)
- `d84c02a0d` T-415: WIND's overworld sprites recoloured from sand to autumn leaves (DAEMONS tools/genwindleaves.py, DRAFT art)
- `4ab096173` T-421: flags.h says what is really free -- 581 vanilla flags unused, not nine

## The design and tools since v11.306.8

- `fba588fe` TODO: T-415, T-417, T-422 leftovers (engine d84c02a0d, 81f24effb, 3187ca0fd); engine.md's budget
- `a4ebb2ad` T-422: gencasino carries a holiday's flip into the game's table (engine 3187ca0fd)
- `5f274d75` T-417: genplaynotes draws the BAND'S SHEET's glyph (engine 81f24effb)
- `4d5ec307` T-415: tools/genwindleaves.py -- WIND's leaves, drawn into the sandstorm sheet (engine d84c02a0d)
- `d5bdff7c` TODO: T-05, CALLOW's theme chosen by ear (the user)
- `c7d940c5` T-428: the playground's keys as in mGBA (X is A, Z is B) and its HELP -- how to play, the companion, the app and the boards (daemons-playground a7f4ecb); qa T-428
- `9b4f8db8` TODO: T-05 from the user's songs; T-406 from the quest log's space (the user)
- `5a1006ce` T-429: checkregister's table learns the 154 Gen 3 and NEXUS names it was missing; it exits 0
- `d27a7c2a` T-428: the playground's COMPANION tab on its own export of the companion's site -- no Expo dev server (daemons-playground a436519; companion C-169, 0ae73fd); qa T-428
- `34f9a55b` TODO: T-429, checkregister's table is behind (found by the T-421 pass)
- `c25fb0af` TODO: T-421 finished -- flags.h's truth (engine 4ab096173), --writes passes, the accidental helper copies folded
- `87778195` T-421: sixteen more vanilla readers go through daemonslib.upstream
- `234040a3` T-421: the palette copies that differed only by accident go through daemonslib
- `5f5dd36e` T-421: items.html and sprites.md regenerated -- the committed files were the stale side
- `ac9fea80` T-421: gbavoices and gentowns stop drifting where nothing changed
- `775413b8` T-421: check_generators' sandbox makes the build's generated headers (make generated)
- `52aa8865` T-428: the playground's own companion -- a daemon SENT in the browser's game appears in its COMPANION tab (daemons-playground 0a3d2e9; companion C-169, 43d6acf); qa T-428
- `79c5f864` qa: T-421
- `3c8d6392` ROM release v11.306.8: the INDEX's type label above the name, clear of the entry (T-421); the tools archived and shared (T-421)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

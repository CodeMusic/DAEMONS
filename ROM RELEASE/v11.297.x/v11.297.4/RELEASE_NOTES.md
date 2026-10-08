# DAEMONS v11.297.4 — release notes

*Released 2026-10-08 14:08 · built against the design bible v11.297*

- **Engine**: CodeMusic/pokefirered-daemons `5301eb7b5` (context-content)
- **Design**: CodeMusic/DAEMONS `e9fe3b1d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `19ee371e2dc33b0a9bd73337670ac63db14e831f` |
| `daemonsContext.gba` | CONTEXT | `d2ef6a8504dc8aa04d94547527bcf403f28c567c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `edcb9780956d7f2e4bfc7065eb55b2f6ff1d54f7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2125abd59ae0ad8c696a743324fc03c6a03801c8` |

## The engine since v11.297.3

- `5301eb7b5` T-394: a debug game starts as a normal one does, and DEBUG -> GAME EVENTS hands the kit out a piece at a time, in story order -- a scrolling list (daemons_debug_events.c), each row + held or · not, A giving or taking: EVERYTHING (the old kit, exactly), the ROSTER, EVERY DAEMON, the STOCK, the OPENING, shoes, INDEX, OPUS, MARKS (a page, each leader beaten or not), the NOTEBOOK (empty, or every page), the school, the ticket, the DRIVERS (a page), TEA and BRAZEN's gates, REVEAL, the RESOLVER, the INTERRUPT, every GOTO point, the GUIDE, the GLOBAL INDEX, the UNDERSTANDINGS (a page, each with what it needs; and the insights let arrive again), STREAM and HEARSAY, the companion's link. The kit is in pieces in new_game.c; SONG and SFX moved to a SOUND page to make room on DEBUG's first.

## The design and tools since v11.297.3

- `e9fe3b1d` T-394 done (engine 5301eb7b5): a debug game starts with nothing, and DEBUG -> GAME EVENTS gives or takes each piece in story order; CLAUDE.md says so
- `3929d57c` ROM release v11.297.3: the splash's bits and notes in battle, drafted on the debug ROMs (T-392)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

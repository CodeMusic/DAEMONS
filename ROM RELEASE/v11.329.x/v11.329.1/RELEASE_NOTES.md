# DAEMONS v11.329.1 — release notes

*Released 2026-10-29 17:59 · built against the design bible v11.329*

- **Engine**: CodeMusic/pokefirered-daemons `17b96eb4a` (context-content)
- **Design**: CodeMusic/DAEMONS `f26d696e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `804c749591d9da66d863834028b24f18c445ec70` |
| `daemonsContext.gba` | CONTEXT | `a303fe1d36c29e76ffc4c089a5c3dc76698eda62` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b90c71cc9e6622234907eb9d1a4d19378a558699` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c686e1fecfcadebfeee87c84e28fbdab4eec5e9e` |

## The engine since v11.328.1

- `17b96eb4a` T-481 B+C: the menus, the panes and the field keep the calendar -- DaemonsCalendarPane(pal, surface) after each pane's palette loads (text box, START, SUMMARY and its mon switch, the INDEX), on the table DAEMONS tools/gbacalendar_ui.py --write --approved writes (src/data/calendar_panes.h): the day's trim on one sparse slot, a non-quiet holiday's month colour on one (the INDEX's corners instead of the day), sWatchTint at a half on frame and backdrop slots only, never paper or ink; T-318's wash retired (START's frame keeps its style's colours, the day on the eight inner-corner pixels, styles 1/3/4/5); the text box relit with the field; the INDEX's flip fades to the tinted backdrop. Field: the water's crest (General rows 4 and 6, index 1) in the day's trim beside T-275, before the print and the watch; petal 11 in the month colour on a non-quiet holiday with no field look of its own
- `f7f0cefb6` README: latest release v11.328.1

## The design and tools since v11.328.1

- `f26d696e` companion_export: title art skipped in a tree never built (check_generators' sandbox); engine.md's numbers
- `379e16c4` T-481 B+C: gbacalendar_ui.py --write --approved writes the engine's calendar_panes.h (the panes' day, holiday and hour slots, START's frame styles measured from the drawings; a second write is a no-op; palettes read from the tracked .png, not the build's .gbapal); wired into check_generators; tools/routes/t481bc.json films it
- `c533f8cd` TODO: T-488 keeps * SINK beside MINUS's ability (the user)
- `6d9fd87c` TODO: T-485, T-486, T-487 struck -- released v11.328.1
- `976e1f50` Bible v11.329: T-488's resist items are the * SINK family, sold by type late; v11.328.1 recorded (T-485 to T-487)
- `e8cbabcd` README and wiki: the newest release is v11.328.1
- `5941f6cc` manual: rebuilt for v11.328.1
- `fef9ae99` ROM release v11.328.1: T-485 OSRIC HATTER's house on QUICKSILVER; T-486 the glitch follows the clock; T-487 Al's one crack; v11.326.x sealed

## The design bible's own entry for v11.329

### v11.329 — 2026-10-29

- **2.12 §2, the type-resist handlers: DECIDED (T-488).** The family is `* SINK` (a heat sink soaks one hit and is spent): sixteen, one per type but ORACLE. Each town's MART sells its leader's type and the types that beat it once that MARK is held, and a few are hidden on routes. The bible notes that `SINK` is already MINUS's ability name. Every name is DRAFT.
- **v11.328.1 released, so the bible records it:** OSRIC HATTER's house on QUICKSILVER (T-485). The only glitch now follows the clock (T-486): strongest at 3:30, faint toward 3:00 and 3:59. Al's one crack happens once, after the GLOBAL INDEX (T-487).
- **3.10:** the battle backgrounds were released in v11.326.1. The menus and the overworld come next (T-481 B, C).
- A Settled entry in section 10.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

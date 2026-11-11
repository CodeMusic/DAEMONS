# DAEMONS v11.346.2 — release notes

*Released 2026-11-11 03:01 · built against the design bible v11.346*

- **Engine**: CodeMusic/pokefirered-daemons `87f9e46d5` (context-content)
- **Design**: CodeMusic/DAEMONS `2712ee01`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `33ba4af8941e21844370dbbdc646545422aa8d34` |
| `daemonsContext.gba` | CONTEXT | `b9279a0bbd39eadc874096685bef2ff358a0a6f5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8c5c63ac57ef32964fc70952757428a13a38bb0d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `87c2efbf9d06130394e1ee1d19b80a4d9ff356c4` |

## The engine since v11.346.1

- `87f9e46d5` T-447 pair 5, THE PLACES THAT OUTLIVED THEIR USERS: KEEPALIVE PLANT as B GROWING UNTENDED and the seven TANOBY chambers as A CARVED, NOT LIT, redrawn in place -- the plant's other meaning: ivy up every housing, thick at the foot and thin at the cap, the status lights still green in the leaves, moss in the seams, the drums planters, a vine round each coil, and (extended over the 33 tiles the draft left as Nintendo drew them) moss on the housings' caps, a creeper round the girders and braces, tufts at the walkways' ends, grass through the grates, leaves over the drums' lids, ivy up the generators' domes and moss in their vents -- gbacaves' STILL RUNNING colours kept, three greens in row 8's free slots; TANOBY sandstone courses, each chamber's own colour a band of pigment at its slots 14/15, a frieze of a generated, unreadable script cut into the back wall and one line of it along every maze wall, doors into the dark. No block, palette row, behaviour (the generators' MB 0x95) or map moved, 0 new tiles; the chamber name cards (T-445) untouched (tools/gbalandmarkrooms.py --pair 5 --write --approved; the user, 2026-11-11: "PLANT B Growing untended, TANOBY A Carved, not lit"; DRAFT)

## The design and tools since v11.346.1

- `2712ee01` T-447 pair 5 BUILT (engine 87f9e46d5): KEEPALIVE PLANT B GROWING UNTENDED, TANOBY A CARVED, NOT LIT -- gbalandmarkrooms APPROVED = {man: A, tow: A, pp: B, tan: A} (the user, 2026-11-11); B extended over the 33 plant tiles its draft left as Nintendo drew them (caps, girders, ends, grates, drum lids, the generators), in its own slots, every drafted tile unchanged; a second write a no-op; check_generators runs --pair 5 --approved; route t447_pair5.json; qa 11Nov2026 T447 43-54
- `ae19847d` qa T447 34-42: pair 4 filmed in the theatre (the MANSION, ROUTE 21's station, DAEMON TOWER grey and colour)
- `853a0422` theatre_route: bag reads each item's pocket from items.json (the ORIGIN BOOK, item 251, landed in ITEMS by vanilla's id ranges)
- `08ae1587` qa: T-533 THE ORIGIN OF A DAEMON filmed in the running game (v11.346.1 debug, the theatre) -- the shelf, the book as found, MOM once, a page coming back, every chapter back with VII opened (qa 11Nov2026 T533 29-33); route tools/routes/film_t533_origin.json
- `d4f706be` T-447 pair 5 DRAFTED: KEEPALIVE PLANT + TANOBY, three directions each (nothing in the engine)
- `99eb08a8` TODO T-533 closed: THE ORIGIN OF A DAEMON released in v11.346.1 (DAEMONS 6896a1be + ec14d7cb, engine 73f874f9f + 2d4273219, companion 2eeabdd..2c65b27)
- `6687c1af` ROM release v11.346.1: T-533 THE ORIGIN OF A DAEMON and T-447 pair 4 (the MANSION A THE RACK HALL, DAEMON TOWER A THE DOT SCREEN); v11.345.x sealed (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

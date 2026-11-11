# DAEMONS v11.348.2 — release notes

*Released 2026-11-11 11:59 · built against the design bible v11.348*

- **Engine**: CodeMusic/pokefirered-daemons `4983f1ce3` (context-content)
- **Design**: CodeMusic/DAEMONS `f3aa696f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5b7f0e90363c40160e4aa60fbea94090a9a123c7` |
| `daemonsContext.gba` | CONTEXT | `1b984fee6b9637ea32278d5b05a7b667409c5b6c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b4d2bc02f8dc74e98aecd22bf96b6fad35f9d8db` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e93570a0c5a935995e048cd5669b8f626b002d7e` |

## The engine since v11.348.1

- `4983f1ce3` T-519: the torn lines -- THE UNITY BOOK's last line finishes both tears: "...It will not be, and it always was. Look again, and you will see them both." (the user, 2026-11-11, by multiple choice; DAEMONS docs/unity-book.md 1fc70acc; DRAFT). LAST WORD's last page now carries two lines onto the spread's right page; its spreads and every folio after it unchanged (DAEMONS tools/gensubtle.py --book unity --write: every line fits and every rule holds)
- `8f12384b5` T-528 (e): the conjugate light alone brings TULIKKO's sparks, on any night (the user, 2026-11-11: "Yes, conjugate alone") -- red over green, the book mended
- `aa76f9f20` T-528 (e), the last of it: the sparks rising from TULIKKO's snow -- on a night of light with the book mended, at FOUR ISLAND, a few at a time (four at most, one every 18 frames) from the fox's tail, rising and swaying, fading as they rise (a cross, a point, a speck, flickering out), carried by the camera as the fox is; in the edition's line (CONTENT RED_LINE, CONTEXT GREEN_LINE, the sky's exact RGB, each with a core halfway to white and embers at 5/8); under the conjugate light each spark rises green and turns red above it. None on a dark night, by day, in HALFTONE or before the mending. Six tiles drawn in code (DAEMONS tools/gentulikko.py), one palette taken only while two are free, the pool emptied and its tiles and palette given back off the map. Aurora_SparksTick, once a frame from main.c after Aurora_Tick. No words. RAM 0.

## The design and tools since v11.348.1

- `f3aa696f4` T-519 the torn lines are in the engine (4983f1ce3): gensubtle.py --book unity --write, THE UNITY BOOK ends "...It will not be, and it always was. Look again, and you will see them both." -- every line fits, spreads and folios unchanged; qa 11Nov2026 T519 83; not released
- `5c209edc7` T-528 (e) the sparks BUILT (engine aa76f9f20 + 8f12384b5): tools/gentulikko.py now draws TULIKKO's six spark tiles in code (a diamond, shade = frame + distance: cross, point, speck; red line then green), its palette read from daemons_aurora.c's RED_LINE/GREEN_LINE with SPARK_CORE/SPARK_DIM, reproducing the committed tulikko_sparks.png byte for byte; route tools/routes/t528_sparks.json (FOUR ISLAND by the fox at (40,14): a light night mended, the conjugate light on a dark night, none before the mending, by day, or on a dark night without it; --check passes); engine.md's budget; qa 11Nov2026 T528 82; not released
- `cd4d3903a` Every manual reprinted against v11.348.1 with its new cover (its colour and its device); THE COMPANION's too, now its T-Glass chapter is in; PLAYING TOGETHER re-recorded for its new hub address (863735271)
- `738514768` C-321: THE COMPANION re-recorded (friend) with the T-Glass chapter
- `863735271` Social manual: the hub's example address is http://daemons-hearth:4730 (the hub renamed from CoreMP135, 2026-11-11) -- source only; its PDF and PLAYING TOGETHER's recording follow at the next print
- `7fd668b0f` qa: C-167 the CORPUS ledger shows the figure the companion wrote (companion 24c20e7)
- `32b991899` Merge branch 'covers-d'
- `c1dcb9146` ROM release v11.348.1: T-447 pair 6 (the LEAGUE A THE FOUR VESSELS, the HALL OF FAME A THE INDEX CARD) and the DUET's tune DUET-1 (T-528 f); v11.346.x sealed (DRAFT)
- `536d80710` Every manual its own colour and its device on the cover (the user, 2026-11-11, picked D of four mockups: 'we should be able to differentiate guides for different devices more easily'): tools/manual_devices.py draws the GBA, the phone, the watch, two linked handhelds, the Tiiny and a scroll, a daemon on each screen; all seven printed books reprinted (THE COMPANION waits on its own edit). THE WATCH brought up to C-325 (companion e979115): BOOKS as tiles, chapters numbered, the daemon's page four tiles (CARE, INDEX, TALK, DREAM), the crown twice home from anywhere; re-recorded

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.296.1 — release notes

*Released 2026-10-06 13:28 · built against the design bible v11.296*

- **Engine**: CodeMusic/pokefirered-daemons `14ac74e70` (context-content)
- **Design**: CodeMusic/DAEMONS `b94c7d25`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e337ddce74f37703ce118dc7cf96a93ad7cc91fc` |
| `daemonsContext.gba` | CONTEXT | `cdc418adea8045b92a9974c2b4e48b278123cdab` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `6d2519b2f06e02d57f357be928e9f38769d2a2a0` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `64b3449d9cbfa5aca1b0c765d40db07a3e90b572` |

## The engine since v11.295.7

- `14ac74e70` T-383 (DRAFT): three lines the status sweep broke -- PHLEGMATIC's 'deep-freeze' is ice again (it said 'deep-hang'), the ice room's 'once they hang.' (it said 'hung solid'), Route 25's 'starts thrashing' (it said 'gets thrashing')

## The design and tools since v11.295.7

- `b94c7d25` T-383 struck (engine 14ac74e70, DRAFT); T-378 played: scenes.json passes -- the seven leaders' MARK lines (T-346 seen), PHLEGMATIC and SCORN (T-321 seen); the runner waits out a warp the music fade holds, and plays out whoever sees the player land
- `8d5e0894` T-378, first live run: the walker finds a .map symbol with no '= .' (gStringVar4); the runner reads gen 3's control codes by their real argument counts, and captions a message once, not on every frame
- `02526d10` T-378: trigger (a scene stepped into, its battles won on a debug route) and trainer steps; --check refuses a goto into a wall; tools/routes/scenes.json -- the seven leaders' MARK lines (T-346) and PHLEGMATIC's and SCORN's scenes (T-321), each checked by its words
- `d170c6c6` The walker plans across ice (goal item 3): a step onto MB_ICE lands where the slide stops, cracked ice is a wall, and it waits out a slide; STILLFALL B1F solved on paper, not yet walked
- `1c946862` T-378 (built, not yet played): tools/theatre_route.py plays a route file stop by stop -- goto, talk, look, says, music, flagis ... -- with a contact sheet per stop; tools/routes/field-test.json is the field page's route; the walker's flag() is a function now
- `857dc3d8` engine.md 5: the walker (tools/theatre_walk.py) -- its commands, what it handles, what it cannot; CLAUDE.md's tool list gains it
- `68ae87d7` T-377: check_reach finds a name printed before it is looked up (engine.md trap 43)
- `28131bf8` T-379-T-382 drafted for approval (field page q-push57); reviewsheet draws a tileset that borrows another's graphics
- `40b5d419` v11.296: the quest's two halves, MARKS and ROOTS (bible 0.7); T-379-T-382 drafted as tickets
- `4fff3a9d` T-377 (a name used before it is looked up) and T-378 (the walker as a route runner), for the 6 October work-day run
- `17c21746` T-321: CAIRN's gift and the Owl's thermostat scene seen; the walker can read and set a flag on a scratch save
- `ff0f6a63` ROM release v11.295.7: VERA's tending reads right (T-376)

## The design bible's own entry for v11.296

### v11.296 — 2026-10-06

### The quest's two halves: MARKS and ROOTS (2026-10-06)

- ***0.7, new (the user's decision)***: **the MARKS give intelligence, the ROOTS give understanding**, *and the user's
  sentence "Intelligence without understanding is artificial" (Seeing Sharp, 5 October 2026) is the spine of both
  halves -- never said in the game.* **ROOTS** *(chosen over GROUNDING, BEARINGS and leaving it unnamed)* **is a name,
  never a count**: *one label on the USER card's brain, opposite BENCHMARKS.* **The world shows the difference
  instead, in three DRAFTS for the user's approval**: *the borrowed daemon (its refusals), CORPUS's plastic plants
  against the CHECKPOINTS' real ones, and a fact collector with every MARK.* Tickets T-379--T-382; nothing built yet.
- ***`lineage.md` 7.3*** gains the article.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

# DAEMONS v11.299.4 — release notes

*Released 2026-10-11 12:39 · built against the design bible v11.299*

- **Engine**: CodeMusic/pokefirered-daemons `b54220b08` (context-content)
- **Design**: CodeMusic/DAEMONS `be17a9e5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `03ca2a3e79bda982a05ee6ca0acdc9f7a551e670` |
| `daemonsContext.gba` | CONTEXT | `d1e23caa871608ca5c21257906bdfe1d4b878e7c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d28663c7cd60b9fda83afc8a79aa5136c9ef1940` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7bc9b5b407f6c69cd368234b29854cf693a2d8aa` |

## The engine since v11.299.3

- `b54220b08` T-382: the fact collector at UMBRA PLATEAU's CHECKPOINT, every MARK word for word, nearly noticing when asked again, a young trainer beside him; and that CHECKPOINT's three real plants (T-381) (approved by the user 2026-10-11)
- `66d14f774` T-381: artificial flowers -- 84 FOUNDRY plants with a tag not to water them, SCORN's two the finest, 19 CHECKPOINT plants real (DAEMONS tools/gbaplants.py; approved by the user 2026-10-11)
- `742b33898` T-380: a borrowed daemon's refusals say it does not know you yet -- six lines, not a lazy daemon (approved by the user 2026-10-11)
- `8a00184f9` T-379: the USER card names both halves -- ROOTS under the brain, in the MARKS label's own small letters (approved by the user 2026-10-11)
- `94e5b57f2` T-399: the mart's BUY opens on kinds of thing, ALL first
- `ad0ea82e0` T-398: GAME EVENTS waits for A and B to be let go before it reads a press, and EVERYTHING asks first

## The design and tools since v11.299.3

- `be17a9e5` T-379..T-382 done (engine 8a00184f9, 742b33898, 66d14f774, b54220b08): ROOTS on the card, the borrowed daemon's refusals, artificial flowers (tools/gbaplants.py), the fact collector -- approved by the user and played (tools/routes/roots.json)
- `19b0e42d` T-400 logged: a real GitHub wiki for DAEMONS (the user, 2026-10-11) -- public writing, so never the four in SECRETS; waits on its first page
- `3e59c120` T-399 struck (engine 94e5b57f2): the mart opens on kinds of thing, played at LAVENDER's counter (qa 11Oct T399); tools/routes/t399.json replays it
- `0f03a9f0` T-398 struck (engine ad0ea82e0): GAME EVENTS waits for a fresh press, and EVERYTHING asks first; T-399 opened: the mart's kinds of thing
- `d12a37ac` T-395: every NEXUS connection played in the theatre -- the pier's fir in, all fourteen doors out and back (qa 11Oct T395 1); the route walker treats two objects on one tile as one place, whichever is shown
- `e4aa1e1e` qa: MESH open on the T-Deck (C-72)
- `950b6342` qa: the T-Display-S3 Pro's first screens (C-105)
- `25df317e` ROM release v11.299.3: THE NEXUS painted whole (T-395)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

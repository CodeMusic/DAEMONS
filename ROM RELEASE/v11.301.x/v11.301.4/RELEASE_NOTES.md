# DAEMONS v11.301.4 — release notes

*Released 2026-10-15 18:41 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `06523b4c9` (context-content)
- **Design**: CodeMusic/DAEMONS `88d70f62`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f8f2c3a770117894352ab6339bc9e7f2b2478400` |
| `daemonsContext.gba` | CONTEXT | `a9a4128ec7aa86454617f00b2de4913f40b086ca` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `015bf5e08de9c92740748ec787591f48fae4b6c1` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `375b098814f3737dcce9bbd3944114cd949a4b52` |

## The engine since v11.301.3

- `06523b4c9` T-404: ENTEI, RAIKOU, SUICUNE and CELEBI's overworld objects in their type palettes (T-133), written by gbaowslots now that it keeps the table's hand-added tail (TY, DAVID, the fir)
- `e114d237e` Generators level (2026-10-15 drift sweep): the 20 T-120 Hoenn portraits take the true-black outline everything else has (gbaoutline); 110 daemons drawn in T-210 batches 2-7 switch their streaks on (genstreaks -- T-293's failure again); the TOOLKIT shows T-391's routine words, fitted to its three lines (port_plugin_text); the move menu's comments say our names (gbamovemenu)

## The design and tools since v11.301.3

- `88d70f62` qa: the drift sweep's sheets -- 20 portraits outlined, the legendaries' overworld objects (T-404)
- `e6a8c7f1` T-404 struck: gbaowslots, gentowns and genty off generator_drift.json; sprites.md re-counted for the four legendaries
- `da5342e5` T-404 (engine 06523b4c9): gbaowslots keeps the graphics table's hand tail and puts its variants back in place; genty outlines TY itself; gentowns leaves T-371's companion lemur alone
- `ee5bdfff` TODO: T-404 -- gbaowslots, genty and gentowns made safe to write (the 2026-10-15 drift sweep)
- `c1598a90` generator_drift.json: gentowns, genty and port_pronoun recorded with the hand work each would undo; gbaowslots notes the four legendaries waiting on its tail fix; gbachar's list takes today's 20 outlined portraits and drops 54 line-ending-only entries
- `eac81383` gbaspritecensus: no engine commit stamped in sprites.md -- it drifted on every engine commit with nothing measured changed
- `967c2aa0` type-chart.pdf and items.pdf re-cut from today's regenerated pages
- `d2481eae` Drift sweep (engine e114d237e): check_generators' sandbox links engineAi and agbcc, gives gbadocs its private text, and ignores line endings; gbadocs keeps a page's sign in its slot; engine.md, the type chart, the items page and retired_names regenerated
- `f9e90e29` T-319 kept current (engineAi 701cb46): the brief knows the game as of 2026-10-15
- `30a51f28` qa: C-121 -- both T-Embeds and the T-Display-S3 Pro on the bench
- `355f41d0` ROM release v11.301.3: the NOTEBOOK marks what is unread, says what each page is, and shows where it was found (T-403); pages flow as they are handed over (T-401)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |

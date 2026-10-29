# DAEMONS v11.320.1 — release notes

*Released 2026-10-28 22:29 · built against the design bible v11.320*

- **Engine**: CodeMusic/pokefirered-daemons `a2a5bf5a5` (context-content)
- **Design**: CodeMusic/DAEMONS `48831e2f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f7e1af3afc21e83d4383457d9dfd90c84ffc098a` |
| `daemonsContext.gba` | CONTEXT | `e6bf7021f952d2e83dfb0cd413e3aa0034d273a5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `94343a133192e11af3c7b1e5cbb643a89822ca8e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `94dd33cd48340383cb82ad1164aa339dfa5b45e3` |

## The engine since v11.319.1

- `a2a5bf5a5` T-474: DOLPHIN and PENGUIN become PENPHIN only when traded for each other
- `77c2f5eb8` T-476: OVERLOADED's and PROTEUS's followers made again from the forms' new bodies (gbafollower: 87557e860 redrew both after their followers were cut)
- `bf62004cb` T-478: the ten dungeon descriptions and the START menu's INDEX line break with \n, as vanilla -- \l scrolls, and a printer with no prompt stops at it after two lines
- `553bb5271` T-477: A TO Z MODE sorts by our names (gPokedexOrder_Alphabetical from DAEMONS tools/genatoz.py, all 422 entries)
- `27b31c4a1` T-476: DEADLOCK's streaks switched on (genstreaks: batch 8 drew the markers, nothing set the flag); the credits' four cards made again from the T-452 daemons (gencreditcards)
- `c4f305bba` README: every daemon drawn again in the new style, its forms too (T-452); latest release v11.319.1; a pair trade evolution still to come

## The design and tools since v11.319.1

- `48831e2f` T-474 built (engine a2a5bf5a5): the pair trade; companion_export carries TRADE_PARTNER and the partner bits
- `538834ed` T-478: the dungeon descriptions and the INDEX's START-menu line break with \n again (engine bf62004cb)
- `94cc199e` T-477: A TO Z MODE by our names -- tools/genatoz.py writes the order (engine 553bb5271); played in tools/routes/t477.json
- `6535f654` T-476: generator drift read both ways -- DEADLOCK's streaks, the credits' cards and two followers were stale (engine 27b31c4a1, 77c2f5eb8); gendaemons and gbacivictown carry later work (generator_drift.json, gendaemons guarded); engine.md's numbers; manual excused from the sandbox
- `e938b63c` qa: C-232's shiny sheet labelled -- the second card was HOPE's ordinary face, there to compare, and said nothing (the manual session read it as a shiny that had not inverted); HOPE now in both
- `cbe4e0f1` qa: T-467 the manual's additions (the week, the holidays, the books asked, the cards, the Pocket Taco)
- `823adf90` manual (T-467): the user's additions -- POCKET TACO and the screen's own buttons (C-234, C-235); the books asked, REASON and INSTINCT: ASK THE GUIDE, ASK THE SUBTLE LAYER, TWO VOICES, TODAY'S QUESTION and THE JOURNAL (C-209, C-229, C-230); THE SUBTLE LAYER's 22 cards, their REASON and INSTINCT faces and the three draws (C-232); THE WEEK (name, note, colour; the companion's word, virtue over its shadow and centre); the hemispheres' seasons with their dates; the real sky on the companion; the year's 36 holidays by their in-world names. {{week}} and {{holidays}} drawn from companion_export.py and docs/holidays.json; 54 pages, v11.319.1
- `52d13c5c` README and wiki: every daemon drawn again (T-452, since v11.316.7), its forms too; the cart alone earns the diploma (T-469); v11.319.1; a pair trade evolution still to come (T-474)
- `962c3a65` Bible v11.320: PENPHIN only by a pair trade, the only pair (T-474)
- `f430b06c` qa: C-233 THE PLAYER'S MANUAL in the companion's LIBRARY (the site, and the iOS app on the iPhone simulator); manual.py notes the companion reads its PDF and the release in its subject
- `6c764464` qa: C-232 THE SUBTLE LAYER's cards (the 22 in their REASON and INSTINCT faces; the shiny ones)
- `8b6df802` manual: rebuilt for v11.319.1
- `a260dd34` ROM release v11.319.1: T-469 the diploma (cart alone), T-470 A-Z and the other sorts, T-471 FEEBAS evolves again, T-472 tool guards; v11.316.x sealed

## The design bible's own entry for v11.320

### v11.320 — 2026-10-28

### PENPHIN only by a pair trade (T-474)

- ***Penphin (the user, by multiple choice)***: **DOLPHIN and PENGUIN each evolve only when traded for the other**, and both arrive as PENPHIN; any other trade leaves them as they are (T-234 had either half evolve on any trade). **The only pair trade**: no other species gets one. Built by the game lane (T-473 b) and the companion (C-219).

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
